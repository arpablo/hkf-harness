# -*- coding: utf-8 -*-
"""Ein Bundle in die Wissensbasis uebernehmen — Core §6.1.

Der Ablauf hat zehn Schritte, und drei davon enden mit einem Urteil, das
dieses Modul nicht faellt: die Bedeutungspruefung (§5.5), die Identitaet einer
ankommenden Notiz (§6.1 Schritt 5) und die Verknuepfung ueber die drei
mechanischen Beobachtungen hinaus (§5.6). Wo geurteilt werden muss, wird der
Fall vorgelegt, nicht geraten.

Der Plan entsteht vollstaendig, bevor irgendetwas geschrieben wird. `--check`
laesst es beim Plan; ohne das Kennzeichen wird derselbe Plan ausgefuehrt.

Eine Auslegung sei genannt: §5.5 nennt eine vorhandene vorlaeufige
Typdefinition als Anlass einer Bedeutungspruefung. Liefert das Bundle fuer
diesen Namen selbst keine Typdefinition, behaupten beide Seiten nichts, und
die Unterlagen, die §5.5 vorlegen laesst — die `description` beider Seiten —
gibt es nicht. Dieses Modul meldet dann einen Hinweis statt einer Frage, die
niemand beantworten kann.
"""
import datetime, hashlib, io, os, re, shutil

from . import CORE, ablage, fassung, frontmatter, notiz

WERKZEUG = "hk-import"

_ARTEN = [("image", "png jpg jpeg gif webp svg avif bmp tif tiff heic"),
          ("video", "mp4 mov webm mkv avi m4v"),
          ("audio", "mp3 m4a wav flac ogg opus aac")]
ENDUNGEN = {e: art for art, liste in _ARTEN for e in liste.split()}
ARTVERZEICHNIS = {"image": "images", "video": "videos",
                  "audio": "audios", "document": "documents"}

# §3.5.1 — ein Bundle darf sie nicht umdefinieren (§6.1 Schritt 3)
# §3.8 — die Kern-Typen der Grundausstattung. Jede konforme HKB fuehrt sie
# in derselben Fassung (§7.2), also stellt sich die Frage nach der Bedeutung
# fuer sie nicht.
KERN_TYPEN = {"typedef", "proptype", "bundle"}

STANDARD_PROPTYPES = {
    "hkf-country", "hkf-email", "hkf-file", "hkf-lang", "hkf-latitude",
    "hkf-link", "hkf-link-list", "hkf-link-or-url", "hkf-longitude",
    "hkf-phone", "hkf-url", "hkf-wikidata", "hkf-year"}


def medienart(name):
    """Aus der Endung, im Zweifel `document` (§4.3)."""
    return ENDUNGEN.get(name.rsplit(".", 1)[-1].lower(), "document")


def jetzt():
    n = datetime.datetime.now()
    return n.strftime("%Y-%m-%d"), n.strftime("%Y-%m-%dT%H:%M:%S")


def sha(pfad):
    return hashlib.sha256(io.open(pfad, "rb").read()).hexdigest()


class Befund(object):
    """art: konflikt | entscheidung | hinweis. `tun` ist der naechste Schritt."""

    def __init__(self, art, text, tun=None):
        self.art, self.text, self.tun = art, text, tun


class Plan(object):
    def __init__(self, hkb, quelle):
        self.hkb = hkb
        self.quelle = os.path.abspath(quelle)
        self.basis = ablage.basis(hkb)
        self.ablagepfad = ablage.ablagepfad(hkb)
        daten, _ = frontmatter.lesen(os.path.join(hkb, "hkb.md"))
        self.media_basis = str(daten.get("media_base") or "").strip("/")
        self.bundle = {}
        self.bundle_body = ""
        self.notizen = []          # dicts: quelle ziel typ zustand kopf body titel
        self.medien = []           # dicts: quelle ziel art zustand
        self.typen = {}            # name -> dict: dir zustand quelle
        self.verweise = []         # (von_link, nach_link, grund, zieldatei)
        self.befunde = []
        self.abgewiesen = None

    # ── Hilfen ──────────────────────────────────────────────────────────
    def melde(self, art, text, tun=None):
        self.befunde.append(Befund(art, text, tun))

    def abweisen(self, grund, tun=None):
        self.abgewiesen = grund
        self.melde("konflikt", grund, tun)

    def link(self, rel, alias):
        """Qualifizierter Wikilink nach §3.6 — mit Ablagepfad, ohne `.md`."""
        ziel = "%s/%s" % (self.ablagepfad, rel) if self.ablagepfad else rel
        return "[[%s|%s]]" % (ziel, alias)

    def konflikte(self):
        return [b for b in self.befunde if b.art == "konflikt"]

    def zu_entscheiden(self):
        return [b for b in self.befunde if b.art == "entscheidung"]

    def hinweise(self):
        return [b for b in self.befunde if b.art == "hinweis"]

    def zaehlung(self):
        z = {"neu": 0, "aktualisiert": 0, "übersprungen": 0, "abgelehnt": 0}
        for n in self.notizen:
            z[n["zustand"]] = z.get(n["zustand"], 0) + 1
        return z


# ── Schritt 1: die Lieferung aufnehmen ──────────────────────────────────

def _sammeln(quelle):
    """(notizen, medien, uebergangen) nach §4.3."""
    notizen, medien, uebergangen = [], [], []
    for r, dirs, fs in os.walk(quelle):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for f in sorted(fs):
            if f.startswith("."):
                continue
            p = os.path.join(r, f)
            rel = os.path.relpath(p, quelle).replace(os.sep, "/")
            if not f.endswith(".md"):
                medien.append((p, rel))
                continue
            if rel == "hbundle.md":
                continue
            kopf, body = notiz.teilen(io.open(p, encoding="utf-8").read())
            if kopf is None:
                uebergangen.append(rel)
                continue
            daten, _ = frontmatter.lesen(p)
            if "type" not in daten:
                uebergangen.append(rel)
                continue
            notizen.append((p, rel, daten, kopf, body))
    return notizen, medien, uebergangen


def _bundle_notizen(plan):
    """Die Bundle-Notizen der HKB, nach id."""
    verz = os.path.join(plan.basis, "bundles")
    aus = {}
    if os.path.isdir(verz):
        for f in sorted(os.listdir(verz)):
            if f.endswith(".md"):
                daten, body = frontmatter.lesen(os.path.join(verz, f))
                aus[str(daten.get("id") or f[:-3])] = (daten, body)
    return aus


def _fassung(text):
    teile = re.findall(r"\d+", str(text or ""))
    return tuple(int(t) for t in teile) if teile else None


def _required(plan, vorhandene):
    """Schritt 1: `required_bundles` gegen den Bestand. Warnung, kein Abbruch.

    Zurueck kommt, was vorliegt, und ob etwas fehlt. Das Zweite entscheidet
    §5.5: Nur wenn ein vorausgesetztes Bundle fehlt, ist die Bedeutung eines
    Typs offen, den die Lieferung selbst nicht definiert — sonst deckt ihn der
    Bestand, und es gibt nichts zu fragen.
    """
    vorliegend, fehlt = set(), False
    for eintrag in plan.bundle.get("required_bundles") or []:
        m = re.match(r"^\s*([a-z][a-z0-9-]*)\s*(?:(>=|=)\s*(\S+))?\s*$", str(eintrag))
        if not m:
            plan.melde("hinweis", "required_bundles: %r ist nicht lesbar" % eintrag)
            continue
        name, _, mindest = m.groups()
        if name not in vorhandene:
            plan.melde("hinweis",
                       "%s ist vorausgesetzt, aber nicht importiert." % eintrag,
                       "Erst %s importieren, dann diesen Import wiederholen." % name)
            fehlt = True
            continue
        haben = _fassung(vorhandene[name][0].get("version"))
        soll = _fassung(mindest)
        if soll and haben and haben < soll:
            plan.melde("hinweis",
                       "%s liegt nur in Fassung %s vor."
                       % (name, vorhandene[name][0].get("version")),
                       "%s aktualisieren und den Import wiederholen." % name)
            fehlt = True
            continue
        vorliegend.add(name)
    return vorliegend, fehlt


# ── Schritt 2 und 3: Typen ──────────────────────────────────────────────

def _property_tabelle(body):
    """{property: (typ, pflicht)} aus dem Abschnitt `# Properties` (§3.7)."""
    aus = {}
    teil = notiz.abschnitt(body or "", "Properties")
    if not teil:
        return aus
    for zeile in teil.splitlines():
        if not zeile.startswith("|"):
            continue
        s = [x.strip() for x in zeile.strip("|").split("|")]
        if len(s) < 3 or s[0] in ("Property", "") or set(s[0]) <= set("- "):
            continue
        aus[s[0]] = (s[1], s[2])
    return aus


def _tabelle_schreiben(properties):
    zeilen = ["# Properties", "", "| Property | Typ | Pflicht | Beschreibung |",
              "|---|---|---|---|"]
    for name in properties:
        typ, pflicht, beschreibung = properties[name]
        zeilen.append("| %s | %s | %s | %s |" % (name, typ, pflicht, beschreibung))
    return "\n".join(zeilen) + "\n"


def _tabelle_voll(body):
    """{property: (typ, pflicht, beschreibung)} — fuer das Zusammenfuehren."""
    aus = {}
    teil = notiz.abschnitt(body or "", "Properties")
    for zeile in (teil or "").splitlines():
        if not zeile.startswith("|"):
            continue
        s = [x.strip() for x in zeile.strip("|").split("|")]
        if len(s) < 4 or s[0] in ("Property", "") or set(s[0]) <= set("- "):
            continue
        aus[s[0]] = (s[1], s[2], s[3])
    return aus


def _vorhandene_typen(plan):
    """{name: (daten, body)} aus <base>/typedefs/."""
    verz = os.path.join(plan.basis, "typedefs")
    aus = {}
    if os.path.isdir(verz):
        for f in sorted(os.listdir(verz)):
            if f.endswith(".md"):
                daten, body = frontmatter.lesen(os.path.join(verz, f))
                aus[f[:-3]] = (daten, body)
    return aus


def _verzeichnis(name, daten):
    return str(daten.get("dir") or (name + "s"))


def _typen_abgleichen(plan, kandidaten, vorliegende_bundles, fehlende_bundles,
                      entscheidungen):
    geliefert = {}
    for p, rel, daten, kopf, body in kandidaten:
        if daten.get("type") == "typedef":
            geliefert[os.path.basename(rel)[:-3]] = (daten, body)

    vorhanden = _vorhandene_typen(plan)
    belegt = {_verzeichnis(n, d): n for n, (d, _) in vorhanden.items()}

    benutzt = set(geliefert)
    for p, rel, daten, kopf, body in kandidaten:
        benutzt.add(str(daten["type"]))

    for name in sorted(benutzt):
        gel = geliefert.get(name)
        if name not in vorhanden:
            # ── neu, aus der Lieferung oder vorlaeufig (§5.4)
            verz = _verzeichnis(name, gel[0]) if gel else name + "s"
            if verz in belegt and belegt[verz] != name:
                plan.abweisen(
                    "Verzeichnis %s gehoert schon dem Typ %s; %s kann dort nicht "
                    "angelegt werden (§5.4)." % (verz, belegt[verz], name),
                    "Einen der beiden Typen umbenennen und den Import wiederholen.")
                continue
            belegt[verz] = name
            plan.typen[name] = {"dir": verz, "zustand": "neu" if gel else "vorläufig",
                                "geliefert": gel}
            continue

        vd, vb = vorhanden[name]
        verz = _verzeichnis(name, vd)
        vorlaeufig = bool(vd.get("provisional"))

        # ── Zusicherung (§5.5)
        aus_required = any(re.search(r"\[\[[^\]]*bundles/(%s)\|" % re.escape(b), l)
                           for b in vorliegende_bundles
                           for l in (vd.get("bundles") or []))
        gleich_in_der_sache = bool(gel) and not vorlaeufig and (
            str(gel[0].get("description") or "") == str(vd.get("description") or "")
            and _property_tabelle(gel[1]) == _property_tabelle(vb))
        urteil = entscheidungen.get(("typ", name))

        if name in KERN_TYPEN or aus_required or gleich_in_der_sache:
            zugesichert = True
        elif urteil and gel and urteil[1] == str(gel[0].get("description") or ""):
            if urteil[0] != "gleich":
                plan.abweisen("Typ %s wurde als verschieden beurteilt (§5.7)." % name,
                              "Einen der beiden Typen umbenennen und neu liefern.")
                continue
            zugesichert = True
        else:
            zugesichert = False

        if not zugesichert and gel is None and not vorlaeufig and not fehlende_bundles:
            # §5.5: Die Frage stellt sich nur, wenn ein vorausgesetztes Bundle
            # fehlt. Deckt der Bestand den Typ, gibt es nichts zu entscheiden.
            zugesichert = True

        if not zugesichert:
            if gel is None and vorlaeufig:
                plan.melde("hinweis",
                           "Typ %s bleibt vorläufig — die Lieferung bringt keine "
                           "Typdefinition mit." % name,
                           "Das Bundle nachladen, das %s definiert." % name)
            elif gel is None:
                plan.melde("entscheidung",
                           "%s  Die Lieferung bringt keine Typdefinition mit, und das "
                           "Bundle, das sie liefern müsste, fehlt.\n"
                           "          hier    %s"
                           % (name, vd.get("description") or "(ohne description)"),
                           "Bedeutungsprüfung für %s entscheiden oder das fehlende "
                           "Bundle nachladen." % name)
                plan.abweisen("Bedeutungsprüfung für %s ist offen (§5.5)." % name)
                continue
            else:
                plan.melde("entscheidung",
                           "%s  Gleicher Name, Bedeutung nicht zugesichert.\n"
                           "          hier    %s\n"
                           "          Bundle  %s"
                           % (name, vd.get("description") or "(ohne description)",
                              gel[0].get("description") or "(ohne description)"),
                           "Bedeutungsprüfung für %s entscheiden. Bei „verschieden\" "
                           "einen der beiden Typen umbenennen und den Import "
                           "wiederholen." % name)
                plan.abweisen("Bedeutungsprüfung für %s ist offen (§5.5)." % name)
                continue

        # ── Schritt 3: zusammenfuehren
        zustand = "unverändert"
        if gel:
            gverz = _verzeichnis(name, gel[0])
            if vorlaeufig:
                zustand = "abgelöst"
                if gverz != verz:
                    plan.melde("hinweis",
                               "Typ %s zieht von %s nach %s; die Notizen ziehen mit "
                               "(§3.2 Regel 5)." % (name, verz, gverz))
                verz = gverz
            elif gverz != verz:
                plan.abweisen(
                    "dir weicht ab: %s (Bundle) gegen %s (hier), Typ %s."
                    % (gverz, verz, name),
                    "Für %s entscheiden, welches Verzeichnis gilt. Ein Umzug zieht "
                    "alle Verweise mit." % name)
                continue
            else:
                alt, neu = _tabelle_voll(vb), _tabelle_voll(gel[1])
                streit = [p for p in neu if p in alt and alt[p][:2] != neu[p][:2]]
                if streit:
                    for p in streit:
                        plan.abweisen(
                            "Property %s des Typs %s: %s/%s (hier) gegen %s/%s (Bundle)."
                            % (p, name, alt[p][0], alt[p][1], neu[p][0], neu[p][1]),
                            "Für %s entscheiden, welche Zusicherung gilt." % p)
                    continue
                ergaenzt = [p for p in neu if p not in alt]
                if ergaenzt:
                    zustand = "ergänzt"
                if str(gel[0].get("description") or "") != str(vd.get("description") or ""):
                    plan.melde("hinweis",
                               "description von %s weicht ab; die der Wissensbasis "
                               "bleibt (§6.1 Schritt 3)." % name)
        plan.typen[name] = {"dir": verz, "zustand": zustand, "geliefert": gel}


def _proptypes_abgleichen(plan, kandidaten):
    verz = os.path.join(plan.basis, "proptypes")
    for p, rel, daten, kopf, body in kandidaten:
        if daten.get("type") != "proptype":
            continue
        name = os.path.basename(rel)[:-3]
        if name in STANDARD_PROPTYPES:
            plan.abweisen(
                "Der Standard-Property-Typ %s darf nicht umdefiniert werden (§3.5.1)."
                % name, "Die Datei aus dem Bundle nehmen und neu liefern.")
            continue
        ziel = os.path.join(verz, name + ".md")
        if not os.path.exists(ziel):
            continue
        vd, _ = frontmatter.lesen(ziel)
        for feld in ("form", "pattern", "values", "unit", "min", "max"):
            if str(vd.get(feld) or "") != str(daten.get(feld) or ""):
                plan.abweisen(
                    "Property-Typ %s: %s ist %r (hier) gegen %r (Bundle)."
                    % (name, feld, vd.get(feld), daten.get(feld)),
                    "Für %s entscheiden, welche Fassung gilt." % name)


# ── Schritt 5: Entscheidungen von frueher (§5.7) ────────────────────────

def _entscheidungen(body):
    """{("typ", name)|("notiz", ziel): (urteil, beurteilt)} aus `# Entscheidungen`."""
    aus = {}
    teil = notiz.abschnitt(body or "", "Entscheidungen")
    for zeile in (teil or "").splitlines():
        if not zeile.startswith("|"):
            continue
        s = [x.strip() for x in zeile.strip("|").split("|")]
        if len(s) < 5 or s[0] in ("Gegenstand", "") or set(s[0]) <= set("- "):
            continue
        m = re.match(r"^Typ `([^`]+)`$", s[0])
        if m:
            aus[("typ", m.group(1))] = (s[1], s[3])
            continue
        m = re.match(r"^Notiz \[\[([^\]|]+)", s[0])
        if m:
            aus[("notiz", m.group(1))] = (s[1], s[3])
    return aus


# ── Schritte 4 bis 6: die Notizen ───────────────────────────────────────

def _wikidata_properties(plan, typ):
    """Properties, die der Typ als `hkf-wikidata` zusichert (§3.5.1)."""
    eintrag = plan.typen.get(typ) or {}
    tabelle = {}
    if eintrag.get("geliefert"):
        tabelle = _property_tabelle(eintrag["geliefert"][1])
    if not tabelle:
        p = os.path.join(plan.basis, "typedefs", typ + ".md")
        if os.path.exists(p):
            tabelle = _property_tabelle(frontmatter.lesen(p)[1])
    return [k for k, (t, _) in tabelle.items() if t.split(" / ")[0] == "hkf-wikidata"]


def _notizen_planen(plan, kandidaten, bundle_id, entscheidungen, force):
    vergeben = {}
    for p, rel, daten, kopf, body in kandidaten:
        typ = str(daten["type"])
        if typ not in plan.typen:
            continue                                  # Typ abgewiesen
        dirn = plan.typen[typ]["dir"]
        dateiname = os.path.basename(rel)
        ziel_rel = "%s/%s" % (dirn, dateiname)
        if ziel_rel in vergeben:
            plan.abweisen(
                "%s und %s ergäben dieselbe Notiz-ID %s (§4.3)."
                % (vergeben[ziel_rel], rel, ziel_rel[:-3]),
                "Eine der beiden umbenennen und neu liefern.")
            continue
        vergeben[ziel_rel] = rel

        titel = str(daten.get("title") or dateiname[:-3])
        e = {"quelle": p, "rel": rel, "ziel_rel": ziel_rel, "typ": typ,
             "daten": daten, "kopf": kopf, "body": body, "titel": titel,
             "zustand": "neu", "dieselbe": False}
        ziel = os.path.join(plan.basis, ziel_rel)
        if os.path.exists(ziel):
            _identitaet(plan, e, ziel, bundle_id, entscheidungen, force)
        plan.notizen.append(e)


def _identitaet(plan, e, ziel, bundle_id, entscheidungen, force):
    """Schritt 5 — erst ob dieselbe Notiz, dann welche Fassung gilt."""
    vd, vb = frontmatter.lesen(ziel)
    id_link = e["ziel_rel"][:-3]
    if vd.get("type") == "typedef" and vd.get("provisional"):
        # Abloesung (§5.4): die vorlaeufige Typdefinition sichert nichts zu,
        # also gibt es nichts zu vergleichen und nichts zu entscheiden.
        e["dieselbe"] = True
        e["zustand"] = "aktualisiert"
        return
    voll = ("%s/%s" % (plan.ablagepfad, id_link)) if plan.ablagepfad else id_link

    dieselbe = None
    if any(re.search(r"\[\[[^\]]*bundles/%s\|" % re.escape(bundle_id), l)
           for l in (vd.get("bundles") or [])):
        dieselbe = True
    else:
        for prop in _wikidata_properties(plan, e["typ"]):
            a, b = vd.get(prop), e["daten"].get(prop)
            if a and b:
                if str(a) == str(b):
                    dieselbe = True
                else:
                    plan.melde("konflikt",
                               "%s trägt hier %s=%s, in der Lieferung %s — "
                               "verschiedene Notizen." % (id_link, prop, a, b),
                               "Eine der beiden umbenennen (§3.2 Regel 5).")
                    e["zustand"] = "abgelehnt"
                    return
                break
    if dieselbe is None:
        urteil = entscheidungen.get(("notiz", voll)) or entscheidungen.get(("notiz", id_link))
        if urteil and urteil[1] == e["titel"]:
            dieselbe = urteil[0] == "dieselbe"
            if not dieselbe:
                plan.melde("konflikt",
                           "%s wurde als verschieden beurteilt (§5.7)." % id_link,
                           "Eine der beiden umbenennen (§3.2 Regel 5).")
                e["zustand"] = "abgelehnt"
                return
    if dieselbe is None:
        plan.melde("entscheidung",
                   "%s gibt es schon, und nichts verankert die beiden aneinander.\n"
                   "          hier    %s\n"
                   "          Bundle  %s"
                   % (id_link, vd.get("title") or "(ohne title)", e["titel"]),
                   "Entscheiden, ob %s dieselbe Notiz ist. Bei „verschieden\" eine "
                   "der beiden umbenennen." % id_link)
        e["zustand"] = "abgelehnt"
        return

    e["dieselbe"] = True
    neu, alt = e["daten"].get("modified"), vd.get("modified")
    if not neu or not alt:
        e["zustand"] = "aktualisiert" if force else "abgelehnt"
        if not force:
            plan.melde("hinweis",
                       "%s: `modified` fehlt auf einer Seite, die Fassungen sind "
                       "nicht vergleichbar." % id_link,
                       "Mit --force übernehmen, wenn die Lieferung gelten soll.")
    elif str(neu) > str(alt):
        e["zustand"] = "aktualisiert"
    elif str(neu) == str(alt):
        e["zustand"] = "übersprungen"
        # §5.6: Was die Verknuepfung angelegt hat, ist kein Inhaltsunterschied
        # — sonst meldete jeder zweite Lauf die Notizen des ersten.
        hier = notiz.ohne_abschnitt(
            notiz.teilen(io.open(ziel, encoding="utf-8").read())[1], "Siehe auch")
        dort = notiz.ohne_abschnitt(e["body"], "Siehe auch")
        if hier.strip() != dort.strip():
            plan.melde("hinweis",
                       "%s: gleiche `modified`, aber abweichender Inhalt." % id_link)
    else:
        e["zustand"] = "aktualisiert" if force else "abgelehnt"
        if not force:
            plan.melde("hinweis",
                       "%s ist hier neuer als in der Lieferung (%s gegen %s)."
                       % (id_link, alt, neu),
                       "Prüfen, ob die Lieferung veraltet ist; sonst nichts tun.")


# ── Schritt 7: Mediendateien ────────────────────────────────────────────

def _medien_planen(plan, medien, force):
    for p, rel in medien:
        art = medienart(rel)
        verz = ARTVERZEICHNIS[art]
        teile = rel.split("/")
        if teile[0] == "media":
            teile = teile[1:]
        if teile and teile[0] == verz:
            teile = teile[1:]
        ziel_rel = "/".join(x for x in ([plan.media_basis, verz] + teile) if x)
        ziel = os.path.join(plan.hkb, ziel_rel)
        zustand = "neu"
        if os.path.exists(ziel):
            if sha(ziel) == sha(p):
                zustand = "übersprungen"
            elif force:
                zustand = "aktualisiert"
            else:
                zustand = "abgelehnt"
                plan.melde("konflikt",
                           "%s liegt schon da, mit anderem Inhalt." % ziel_rel,
                           "Prüfen, welche Fassung gilt; --force überschreibt.")
        plan.medien.append({"quelle": p, "rel": rel, "ziel_rel": ziel_rel,
                            "art": art, "zustand": zustand})


# ── Schritt 8: Verweise umschreiben ─────────────────────────────────────

def _abbildung(plan):
    karte, namen = {}, {}
    def merken(quelle, ziel):
        karte[quelle] = ziel
        namen.setdefault(quelle.rsplit("/", 1)[-1], []).append(ziel)
    for n in plan.notizen:
        if n["zustand"] == "abgelehnt":
            continue
        merken(n["rel"][:-3], n["ziel_rel"][:-3])
    for m in plan.medien:
        if m["zustand"] == "abgelehnt":
            continue
        merken(m["rel"], m["ziel_rel"])
    return karte, namen


def _umschreiben(plan, text, karte, namen, woher):
    """Jeden Wikilink auf seinen Pfad in der HKB bringen (§3.6, §6.1 Schritt 8)."""
    def ersetzen(m):
        roh, ziel = m.group(0), m.group(1)
        if ziel in karte:
            neu = karte[ziel]
        elif "/" not in ziel and len(namen.get(ziel, [])) == 1:
            neu = namen[ziel][0]
        elif "/" not in ziel and len(namen.get(ziel, [])) > 1:
            plan.melde("hinweis", "%s: [[%s]] ist mehrdeutig und bleibt stehen." % (woher, ziel))
            return roh
        else:
            plan.melde("hinweis",
                       "%s: [[%s]] zeigt auf nichts, was übernommen wurde, und bleibt "
                       "stehen." % (woher, ziel))
            return roh
        if plan.ablagepfad:
            neu = "%s/%s" % (plan.ablagepfad, neu)
        return roh.replace("[[" + ziel, "[[" + neu, 1)
    return re.sub(r"\[\[([^\]|\\]+)", lambda m: ersetzen(m), text)


# ── Schritt 9: Verknuepfen (§5.6) ───────────────────────────────────────

def _bestand(plan):
    """Alle Notizen, wie sie nach dem Import dastuenden."""
    aus = {}
    for p in ablage.dateien(plan.basis):
        rel = os.path.relpath(p, plan.basis).replace(os.sep, "/")
        if "/" not in rel:
            continue
        daten, body = frontmatter.lesen(p)
        if "type" not in daten:
            continue
        aus[rel[:-3]] = {"typ": str(daten.get("type") or ""),
                         "titel": str(daten.get("title") or rel.rsplit("/", 1)[-1][:-3]),
                         "aliase": [str(a) for a in (daten.get("aliases") or [])],
                         "body": body, "kopf": notiz.teilen(io.open(p, encoding="utf-8").read())[0],
                         "abgelehnt": [str(x) for x in (daten.get("rejected_links") or [])],
                         "datei": p, "neu": False}
    for n in plan.notizen:
        if n["zustand"] in ("abgelehnt", "übersprungen"):
            continue
        aus[n["ziel_rel"][:-3]] = {
            "typ": n["typ"],
            "titel": n["titel"],
            "aliase": [str(a) for a in (n["daten"].get("aliases") or [])],
            "body": n["body"], "kopf": n["kopf"],
            "abgelehnt": [str(x) for x in (n["daten"].get("rejected_links") or [])],
            "datei": os.path.join(plan.basis, n["ziel_rel"]), "neu": True}
    return aus


def _nennt(text, namen):
    """Woertlich (§6.1 Schritt 9) heisst: als Wort, nicht als Wortteil.

    Der Body der Analytical Engine nennt „Lochkarten"; das ist nicht die Notiz
    „Lochkarte". Ohne Wortgrenze zoege jede Mehrzahl einen Verweis nach sich.
    """
    for n in namen:
        if not n:
            continue
        # Ein Titel darf im Fliesstext umbrochen sein: Leerraum passt auf
        # Leerraum, nicht nur auf genau dasselbe Zeichen.
        muster = r"\s+".join(re.escape(w) for w in n.split())
        if re.search(r"(?<!\w)%s(?!\w)" % muster, text):
            return True
    return False


def _verknuepfen(plan):
    """Nur die erste der drei Beobachtungen wird selbsttaetig gesetzt (§6.1
    Schritt 9): Nennt der Body der einen Notiz den Titel oder einen Alias der
    anderen woertlich, bekommt die nennende Notiz einen Eintrag. Die beiden
    anderen Beobachtungen werden vorgelegt."""
    bestand = _bestand(plan)
    beteiligt = [n["ziel_rel"][:-3] for n in plan.notizen
                 if n["zustand"] not in ("abgelehnt", "übersprungen")]

    for a in beteiligt:
        if bestand[a]["typ"] in KERN_TYPEN:
            continue
        namen_a = [bestand[a]["titel"]] + bestand[a]["aliase"]
        for b in sorted(bestand):
            if a == b or (b in beteiligt and b < a):
                continue
            if bestand[b]["typ"] in KERN_TYPEN:
                # Die Kern-Typen sind die Buchfuehrung der Ablage, keine
                # Notizen ueber einen Gegenstand: Eine Typdefinition nennt
                # jeden Typnamen, ohne ihn zu meinen, und eine Bundle-Notiz
                # zaehlt in ihrem Nachweis jeden Titel der Lieferung auf.
                continue
            namen_b = [bestand[b]["titel"]] + bestand[b]["aliase"]
            a_in_b = _nennt(bestand[b]["body"], namen_a)
            b_in_a = _nennt(bestand[a]["body"], namen_b)
            if a_in_b and b_in_a:
                _eintragen(plan, bestand, b, a, "beide Notizen nennen einander")
                _eintragen(plan, bestand, a, b, "beide Notizen nennen einander")
            elif a_in_b:
                _eintragen(plan, bestand, b, a, "im Body dieser Notiz genannt")
            elif b_in_a:
                _eintragen(plan, bestand, a, b, "im Body dieser Notiz genannt")

    # Beobachtung 2 und 3 werden nur vorgelegt (§6.1 Schritt 9)
    for a in beteiligt:
        for prop in _wikidata_properties(plan, _typ_von(plan, a)):
            wert = _wert(plan, a, prop)
            if not wert:
                continue
            for b in sorted(bestand):
                if b == a or b in beteiligt:
                    continue
                if _wert_aus_datei(bestand[b]["datei"], prop) == wert:
                    plan.melde("entscheidung",
                               "%s und %s tragen dieselbe Kennung %s=%s."
                               % (a, b, prop, wert),
                               "Die beiden Notizen zusammenlegen; ein Verweis wäre "
                               "hier falsch (§6.3).")


def _typ_von(plan, ziel_rel):
    for n in plan.notizen:
        if n["ziel_rel"][:-3] == ziel_rel:
            return n["typ"]
    return ""


def _wert(plan, ziel_rel, prop):
    for n in plan.notizen:
        if n["ziel_rel"][:-3] == ziel_rel:
            return str(n["daten"].get(prop) or "")
    return ""


def _wert_aus_datei(pfad, prop):
    daten, _ = frontmatter.lesen(pfad)
    return str(daten.get(prop) or "")


def _eintragen(plan, bestand, von, nach, grund):
    """Einen Eintrag in `# Siehe auch` von `von` auf `nach` vormerken."""
    link_nach = plan.link(nach, bestand[nach]["titel"])
    link_von = plan.link(von, bestand[von]["titel"])
    ziel_kurz = "[[%s|" % (("%s/%s" % (plan.ablagepfad, nach)) if plan.ablagepfad else nach)
    if any(ziel_kurz in x or nach in x for x in bestand[von]["abgelehnt"]):
        return
    if any(ziel_kurz in x or von in x for x in bestand[nach]["abgelehnt"]):
        return
    if ziel_kurz in bestand[von]["body"]:
        # §5.6: Der Abschnitt ist fuer Verweise, die *nicht* aus dem Text
        # hervorgehen. Was der Body schon verlinkt, wird nicht noch einmal
        # unten aufgezaehlt.
        return
    if any(v[0] == link_von and v[1] == link_nach for v in plan.verweise):
        return
    plan.verweise.append((link_von, link_nach, grund, bestand[von]["datei"], von, nach))


def _siehe_auch_schreiben(body, kopf, link, grund):
    """Eintrag alphabetisch einfuegen; `related` daraus ableiten (§5.6)."""
    teil = notiz.abschnitt(body, "Siehe auch")
    zeile = "- %s — %s" % (link, grund)
    if teil is None:
        body = body.rstrip("\n") + "\n\n# Siehe auch\n\n" + zeile + "\n"
    else:
        zeilen = [z for z in teil.strip("\n").splitlines() if z.startswith("- ")]
        zeilen.append(zeile)
        zeilen.sort(key=lambda z: z.split("|", 1)[-1].split("]]")[0].lower())
        body = notiz.ohne_abschnitt(body, "Siehe auch").rstrip("\n") + \
            "\n\n# Siehe auch\n\n" + "\n".join(zeilen) + "\n"
    ziel = link.split("|", 1)[0][2:]
    andere = notiz.entfernen(notiz.entfernen(kopf, "related"), "rejected_links")
    if ziel not in andere:
        rel = notiz.lies_liste(kopf, "related")
        if link not in rel:
            rel.append(link)
            kopf = notiz.setze_liste(kopf, "related", sorted(rel))
    return kopf, body
# ── Schritt 10: die Bundle-Notiz (§5.1) ─────────────────────────────────

def _nachweis(plan, zeitpunkt):
    version = plan.bundle.get("version")
    kopf = "# Import %s" % version if version else "# Import"
    zeilen = [kopf, "", "Übernommen am %s." % zeitpunkt, ""]
    notizen = [n for n in plan.notizen if n["zustand"] != "abgelehnt"]
    if notizen:
        zeilen += ["| Notiz | Typ | Zustand |", "|---|---|---|"]
        for n in sorted(notizen, key=lambda x: x["titel"].lower()):
            zeilen.append("| %s | %s | %s |"
                          % (plan.link(n["ziel_rel"][:-3], n["titel"]).replace("|", "\\|", 1),
                             n["typ"], n["zustand"]))
        zeilen.append("")
    medien = [m for m in plan.medien if m["zustand"] != "abgelehnt"]
    if medien:
        zeilen += ["| Mediendatei | Medienart | Zustand |", "|---|---|---|"]
        for m in medien:
            name = m["ziel_rel"].rsplit("/", 1)[-1]
            zeilen.append("| %s | %s | %s |"
                          % (plan.link(m["ziel_rel"], name).replace("|", "\\|", 1),
                             m["art"], m["zustand"]))
        zeilen.append("")
    if plan.verweise:
        zeilen += ["| Verweis | Gegenstelle | Grund |", "|---|---|---|"]
        for von, nach, grund, datei, a, b in plan.verweise:
            zeilen.append("| %s | %s | %s |" % (von.replace("|", "\\|", 1),
                                                nach.replace("|", "\\|", 1), grund))
        zeilen.append("")
    return "\n".join(zeilen).rstrip("\n") + "\n"


def _neue_fassung(plan, alt_body):
    """Ob dieser Lauf einen Nachweis schreibt — sonst bleibt die Notiz stehen."""
    version = plan.bundle.get("version")
    if not version:
        return True
    return ("# Import %s\n" % version) not in (alt_body or "")


def _bundle_notiz(plan, zeitpunkt, tag, vorher):
    """Frontmatter und Body der Notiz `<base>/bundles/<id>.md`."""
    alt_kopf, alt_body = vorher if vorher else (None, "")
    kopf = alt_kopf
    if kopf is None:
        felder = ["type: bundle", "id: %s" % plan.bundle["id"]]
        for k in ("title", "description", "source", "version"):
            if plan.bundle.get(k) is not None:
                felder.append("%s: %s" % (k, notiz.skalar(plan.bundle[k])))
        if plan.bundle.get("required_bundles"):
            felder.append("required_bundles:")
            felder += ["  - %s" % e for e in plan.bundle["required_bundles"]]
        kopf = "\n".join(felder)
        kopf = notiz.setze_skalar(kopf, "created", tag)
    for k in ("title", "description", "source", "version"):
        if plan.bundle.get(k) is not None:
            kopf = notiz.setze_skalar(kopf, k, notiz.skalar(plan.bundle[k]))
    neue_fassung = _neue_fassung(plan, alt_body)
    if neue_fassung or alt_kopf is None:
        kopf = notiz.setze_skalar(kopf, "imported", zeitpunkt)
        kopf = notiz.setze_skalar(kopf, "modified", zeitpunkt)
        kopf = notiz.setze_skalar(kopf, "modified_by", WERKZEUG)

    # Kurzbeschreibung: der Body der Lieferung ohne die Typtabelle (§5.1)
    beschreibung = notiz.ohne_abschnitt(plan.bundle_body, "Typen").strip("\n")
    if alt_kopf is not None:
        vorhandene = notiz.ohne_abschnitt(alt_body, "Entscheidungen")
        beschreibung = re.split(r"^# Import", vorhandene, 1, flags=re.M)[0].strip("\n")
        nachweise = ["# Import" + t for t in re.split(r"^# Import", vorhandene, flags=re.M)[1:]]
    else:
        nachweise = []

    version = plan.bundle.get("version")
    marke = "# Import %s\n" % version if version else "# Import\n"
    if version and any(n.startswith(marke) for n in nachweise):
        # §5.1: Ein Abschnitt wird einmal geschrieben. Sonst staende beim
        # zweiten Lauf ueberall „uebersprungen", und der Nachweis bezeichnete
        # nicht mehr den Zeitpunkt des Imports.
        neu = []
    else:
        nachweise = [n for n in nachweise if not n.startswith(marke)]
        neu = [_nachweis(plan, zeitpunkt)]

    ent = notiz.abschnitt(alt_body, "Entscheidungen") if alt_kopf is not None else None
    teile = [beschreibung]
    if ent:
        teile.append("# Entscheidungen\n\n" + ent.strip("\n"))
    teile += [t.strip("\n") for t in neu + nachweise]
    return kopf, "\n\n".join(t for t in teile if t).rstrip("\n") + "\n"


# ── Der Plan ────────────────────────────────────────────────────────────

def planen(hkb, quelle, force=False, ohne_verknuepfung=False):
    plan = Plan(hkb, quelle)
    hb = os.path.join(quelle, "hbundle.md")
    if not os.path.isfile(hb):
        plan.abweisen("%s: keine hbundle.md — das ist kein Bundle (§3.1)." % quelle,
                      "Den Pfad auf das Wurzelverzeichnis der Lieferung richten.")
        return plan
    plan.bundle, plan.bundle_body = frontmatter.lesen(hb)
    if not plan.bundle.get("id"):
        plan.abweisen("hbundle.md trägt keine `id` (§4.1).", "Die Lieferung berichtigen.")
        return plan
    if not plan.bundle.get("description"):
        plan.abweisen("hbundle.md trägt keine `description` (§4.1).",
                      "Die Lieferung berichtigen.")
        return plan
    if "hkf" not in plan.bundle:
        plan.melde("hinweis", "hbundle.md nennt keine Fassung; die eigene wird "
                              "angenommen.")
    elif not fassung.lesbar(plan.bundle["hkf"]):
        # §8: Was die HKB nicht erkennt, liest sie, leitet aber keine
        # Identitaeten daraus ab und importiert es nicht.
        plan.abweisen(
            "%s. Die Dateien sind lesbar, übernommen wird nichts (§8)."
            % fassung.satz(plan.bundle["hkf"]),
            "Einen Harness benutzen, der Core %s umsetzt, oder die Lieferung "
            "für Core %s neu ausgeben." % (plan.bundle["hkf"], CORE))
        return plan

    kandidaten, medien, uebergangen = _sammeln(quelle)
    vorhandene = _bundle_notizen(plan)
    vorliegend, fehlt = _required(plan, vorhandene)
    bundle_id = str(plan.bundle["id"])
    ent = _entscheidungen(vorhandene.get(bundle_id, ({}, ""))[1])

    _typen_abgleichen(plan, kandidaten, vorliegend, fehlt, ent)
    _proptypes_abgleichen(plan, kandidaten)
    if plan.abgewiesen:
        return plan

    _notizen_planen(plan, kandidaten, bundle_id, ent, force)
    _medien_planen(plan, medien, force)
    if plan.abgewiesen:
        return plan

    karte, namen = _abbildung(plan)
    for n in plan.notizen:
        if n["zustand"] in ("abgelehnt", "übersprungen"):
            continue
        n["kopf"] = _umschreiben(plan, n["kopf"], karte, namen, n["rel"])
        n["body"] = _umschreiben(plan, n["body"], karte, namen, n["rel"])
    if not ohne_verknuepfung:
        _verknuepfen(plan)
    return plan


# ── Ausfuehren ──────────────────────────────────────────────────────────

def _vorlaeufige_typdefinition(plan, name, tag, zeitpunkt):
    kopf = "\n".join([
        "type: typedef",
        "provisional: true",
        "description: Vorläufig beim Import von %s angelegt; keine Typdefinition "
        "geliefert." % plan.bundle["id"],
        "created: %s" % tag,
        "modified: %s" % zeitpunkt,
        "modified_by: %s" % WERKZEUG])
    return notiz.bauen(kopf, "")


def _umziehen(plan, typ, von, nach):
    """§3.2 Regel 5 — die Notizen ziehen mit, die Verweise auch."""
    alt = os.path.join(plan.basis, von)
    neu = os.path.join(plan.basis, nach)
    if not os.path.isdir(alt):
        return
    os.makedirs(neu, exist_ok=True)
    umbenannt = {}
    for f in sorted(os.listdir(alt)):
        if not f.endswith(".md"):
            continue
        shutil.move(os.path.join(alt, f), os.path.join(neu, f))
        umbenannt["%s/%s" % (von, f[:-3])] = "%s/%s" % (nach, f[:-3])
    if not os.listdir(alt):
        os.rmdir(alt)
    if not umbenannt:
        return
    pre = (plan.ablagepfad + "/") if plan.ablagepfad else ""
    for p in ablage.dateien(plan.basis):
        text = io.open(p, encoding="utf-8").read()
        neu_text = text
        for a, b in umbenannt.items():
            neu_text = neu_text.replace("[[" + pre + a, "[[" + pre + b)
        if neu_text != text:
            io.open(p, "w", encoding="utf-8").write(neu_text)


def _typtabelle(plan):
    """Die abgeleitete Tabelle in `hkb.md` neu erzeugen (§3.1)."""
    hkbmd = os.path.join(plan.hkb, "hkb.md")
    kopf, body = notiz.teilen(io.open(hkbmd, encoding="utf-8").read())
    zeilen = ["# Typen", "", "| Typ | Verzeichnis | Zweck |", "|---|---|---|"]
    verz = os.path.join(plan.basis, "typedefs")
    for f in sorted(os.listdir(verz)):
        if not f.endswith(".md"):
            continue
        daten, _ = frontmatter.lesen(os.path.join(verz, f))
        name = f[:-3]
        zeilen.append("| %s | %s | %s |" % (name, _verzeichnis(name, daten),
                                            daten.get("description") or ""))
    body = notiz.ohne_abschnitt(body, "Typen").rstrip("\n")
    io.open(hkbmd, "w", encoding="utf-8").write(
        notiz.bauen(kopf, (body + "\n\n" if body else "") + "\n".join(zeilen) + "\n"))


def ausfuehren(plan):
    if plan.abgewiesen:
        return plan
    tag, zeitpunkt = jetzt()
    bundle_id = str(plan.bundle["id"])
    bundle_rel = "bundles/%s" % bundle_id
    bundle_link = plan.link(bundle_rel, str(plan.bundle.get("title") or bundle_id))

    # Umzuege zuerst, damit die Notizen danach am richtigen Ort landen
    for name, t in plan.typen.items():
        p = os.path.join(plan.basis, "typedefs", name + ".md")
        if t["zustand"] == "abgelöst" and os.path.exists(p):
            alt = _verzeichnis(name, frontmatter.lesen(p)[0])
            if alt != t["dir"]:
                _umziehen(plan, name, alt, t["dir"])

    # 3. vorlaeufige Typdefinitionen (§5.4)
    for name, t in plan.typen.items():
        if t["zustand"] != "vorläufig":
            continue
        p = os.path.join(plan.basis, "typedefs", name + ".md")
        if not os.path.exists(p):
            os.makedirs(os.path.dirname(p), exist_ok=True)
            io.open(p, "w", encoding="utf-8").write(
                _vorlaeufige_typdefinition(plan, name, tag, zeitpunkt))

    # 4. bis 6. die Notizen
    for n in plan.notizen:
        if n["zustand"] not in ("neu", "aktualisiert"):
            continue
        ziel = os.path.join(plan.basis, n["ziel_rel"])
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        kopf, body = n["kopf"], n["body"]
        t = plan.typen.get(n["typ"], {})
        if n["typ"] == "typedef" and os.path.exists(ziel):
            name = os.path.basename(n["ziel_rel"])[:-3]
            if plan.typen.get(name, {}).get("zustand") == "ergänzt":
                body = _zusammenfuehren(ziel, body)
        # Schritt 6
        links = notiz.lies_liste(kopf, "bundles")
        if bundle_link not in links:
            links.append(bundle_link)
        kopf = notiz.setze_liste(kopf, "bundles", sorted(links))
        for schluessel, wert in (("created", tag), ("modified", zeitpunkt),
                                 ("modified_by", WERKZEUG)):
            if not notiz.hat(kopf, schluessel):
                kopf = notiz.setze_skalar(kopf, schluessel, wert)
        io.open(ziel, "w", encoding="utf-8").write(notiz.bauen(kopf, body))

    # 7. Mediendateien
    for m in plan.medien:
        if m["zustand"] not in ("neu", "aktualisiert"):
            continue
        ziel = os.path.join(plan.hkb, m["ziel_rel"])
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        shutil.copy2(m["quelle"], ziel)

    # 9. Verknuepfung — ohne `modified` anzufassen (§5.6)
    for von, nach, grund, datei, a, b in plan.verweise:
        if not os.path.exists(datei):
            continue
        kopf, body = notiz.teilen(io.open(datei, encoding="utf-8").read())
        if kopf is None:
            continue
        kopf, body = _siehe_auch_schreiben(body, kopf, nach, grund)
        io.open(datei, "w", encoding="utf-8").write(notiz.bauen(kopf, body))

    # 10. Bundle-Notiz und Typtabelle
    p = os.path.join(plan.basis, "bundles", bundle_id + ".md")
    vorher = notiz.teilen(io.open(p, encoding="utf-8").read()) if os.path.exists(p) else None
    kopf, body = _bundle_notiz(plan, zeitpunkt, tag, vorher)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, "w", encoding="utf-8").write(notiz.bauen(kopf, body))
    _typtabelle(plan)
    return plan


def _zusammenfuehren(ziel, neuer_body):
    """Property-Tabellen vereinen; die Zeilen der Wissensbasis gewinnen."""
    alt_text = io.open(ziel, encoding="utf-8").read()
    _, alt_body = notiz.teilen(alt_text)
    alt, neu = _tabelle_voll(alt_body), _tabelle_voll(neuer_body)
    zusammen = dict(alt)
    for k, v in neu.items():
        zusammen.setdefault(k, v)
    rest = notiz.ohne_abschnitt(alt_body, "Properties").rstrip("\n")
    tabelle = _tabelle_schreiben(zusammen)
    return (tabelle + "\n" + rest + "\n") if rest else tabelle
