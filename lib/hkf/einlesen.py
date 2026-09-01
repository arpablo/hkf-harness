# -*- coding: utf-8 -*-
"""Eine Quelle in eine Lieferung einlesen (der Anfang der Kette).

Das Werkzeug baut aus einer Quelle eine Lieferung: eine Quellennotiz mit dem,
was sich sicher feststellen laesst, dazu `hbundle.md`. Was es *nicht* tut:
abrufen, extrahieren, zusammenfassen. Der Harness hat genau eine
Fremdabhaengigkeit und soll keinen Scraping-Stapel bekommen; das Lesen ist
Sache eines Sprachmodells (Harness §2).

Zwei Wege fuehren herein, und beide enden im selben Codepfad:

    aus der Inbox     ein Stueck, das dort liegt
    von Hand          Angaben auf der Kommandozeile

Eine Regel entscheidet, was kopiert wird:

    Eine `.md` wird nie kopiert — sie *ist* die Notiz.
    Alles andere wird kopiert.
"""
import hashlib, io, os, re, shutil, unicodedata

from . import TEMPLATES, ablage, frontmatter, notiz
from .importieren import _property_tabelle, grundtypen

VORGABE_INBOX = "~/hkf-inbox"
ERLEDIGT = "erledigt"

# Die Werkarten (HKF Config §2.2). Ein Typ, sieben Arten.
QUELLTYP = "source"
WERKARTEN = ("article", "book", "paper", "podcast", "transcript", "video",
             "web")
# In einer Lieferung liegt die Quellennotiz unter diesem Verzeichnis; wohin
# sie beim Import kommt, entscheidet allein ihr Typ (§4.3).
QUELLVERZEICHNIS = "Sources"

# Was der Obsidian Web Clipper schreibt, auf `source` abgebildet.
# `site` — der Name der Website — hat kein Ziel: Er steht im Host der `url`,
# und wo er mehr sagt, gehoert er in die Zusammenfassung (Config §3.8).
CLIPPER = {"title": "title", "source": "url", "author": "authors",
           "published": "published_year", "created": "accessed",
           "description": "description", "tags": "tags"}

MEDIEN = ("Media", "Documents")
# Ein Clipping ist eine Datei, keine Notiz (Core §3.2.1). In einer Lieferung
# ist `Clippings/` dafuer reserviert (§4.3).
CLIPPINGS = ("Media", "Clippings")

# In jeder Notiz erlaubt (Core A.2) — sie brauchen keinen Tabelleneintrag.
ALLGEMEIN = ("type", "title", "description", "tags", "aliases", "cssclasses",
             "status", "created", "modified", "modified_by", "extends",
             "sources")


class KeineInbox(Exception):
    pass


# ── Die Inbox ───────────────────────────────────────────────────────────

def herkunft(arg=None):
    if arg:
        return "dem Aufruf"
    if os.environ.get("HKF_INBOX"):
        return "HKF_INBOX"
    return "der Vorgabe %s" % VORGABE_INBOX


def finde_inbox(arg=None, anlegen=False):
    """Absoluter Pfad zur Inbox. Reihenfolge: Aufruf, HKF_INBOX, Vorgabe.

    Dieselbe Ordnung wie bei der Wissensbasis (Harness §3): Kein Werkzeug
    schreibt einen Pfad fest, und geraten wird auch hier nicht.
    """
    pfad = arg or os.environ.get("HKF_INBOX") or VORGABE_INBOX
    pfad = os.path.abspath(os.path.expanduser(pfad))
    if not os.path.isdir(pfad):
        if not anlegen:
            raise KeineInbox("%s: kein Verzeichnis — dort liegt keine Inbox.\n"
                             "Der Pfad kommt aus %s." % (pfad, herkunft(arg)))
        os.makedirs(pfad)
    return pfad


def stuecke(inbox):
    """Was in der Inbox wartet, ohne `erledigt/` und ohne Punktdateien."""
    aus = []
    for f in sorted(os.listdir(inbox)):
        if f.startswith(".") or f == ERLEDIGT:
            continue
        p = os.path.join(inbox, f)
        if os.path.isfile(p):
            aus.append(p)
    return aus


# ── Was ein Stueck ist ──────────────────────────────────────────────────

def sieht_wie_clipping_aus(daten):
    """Das Frontmatter des Obsidian Web Clipper, an seiner Form erkannt.

    Nicht am `type`: Ein Vault, aus dem die Datei kommt, traegt dort seine
    eigene Bezeichnung ein — `[[Clipping]]` etwa —, und die ist kein HKF-Typ.
    Die Form ist verlaesslicher als die Selbstauskunft.
    """
    return bool(daten.get("source")) and bool(
        daten.get("author") or daten.get("published"))


def art_erkennen(pfad):
    """(werkart, grund). Was das Stueck ist, soweit es sich sagen laesst.

    Der Typ steht fest — jede Quelle wird eine `source` (Config §3.8). Offen
    ist die Werkart, und die laesst sich nur bei einer Webseite mechanisch
    feststellen: Ein Clipping bringt die Angaben des Clippers mit. Bei einer
    nackten Datei bleibt sie leer und wird als Luecke gemeldet; geraten wird
    sie nicht.
    """
    if not pfad.lower().endswith(".md"):
        return None, "eine %s sagt ihre Werkart nicht" % (
            os.path.splitext(pfad)[1].lstrip(".").upper() or "Datei")
    daten, _ = frontmatter.lesen(pfad)
    art = str(daten.get("kind") or "").strip()
    if art in WERKARTEN:
        return art, "steht im Frontmatter"
    if str(daten.get("type") or "").strip() == QUELLTYP:
        return None, "eine Quellennotiz ohne `kind`"
    if sieht_wie_clipping_aus(daten):
        return "web", "sieht nach einem Web-Clipping aus"
    return "web", "eine Markdown-Datei ohne `type` — wird als Clipping gelesen"


def slug(text):
    """kebab-case aus einem Titel oder Dateinamen (§3.2 Regel 3)."""
    # Erst die Umlaute, dann zerlegen: NFKD macht aus "ä" ein "a" mit
    # kombinierendem Zeichen, und danach greift kein Ersatz mehr.
    t = unicodedata.normalize("NFC", str(text))
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("Ä", "ae"),
                 ("Ö", "oe"), ("Ü", "ue"), ("ß", "ss")):
        t = t.replace(a, b)
    t = "".join(c for c in unicodedata.normalize("NFKD", t)
                if not unicodedata.combining(c))
    t = re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-").lower()
    return t or "quelle"


def pruefsumme(pfad=None, text=None):
    """`sha256:<hex>` ueber den erfassten Text oder die Datei."""
    h = hashlib.sha256()
    if text is not None:
        h.update(text.encode("utf-8"))
    else:
        with open(pfad, "rb") as f:
            for block in iter(lambda: f.read(65536), b""):
                h.update(block)
    return "sha256:" + h.hexdigest()


# ── Der Plan ────────────────────────────────────────────────────────────

class Plan(object):
    def __init__(self, ziel, hkb=None, quellbasis="Sources"):
        self.ziel = os.path.abspath(ziel)
        # Gegen wen die Pruefsumme verglichen wird. Beim direkten Ingest ist
        # die Lieferung ein Zwischenverzeichnis und immer leer; dann zaehlt,
        # was in der Wissensbasis liegt.
        self.hkb = os.path.abspath(hkb) if hkb else None
        self.quellbasis = quellbasis
        self.notizen = []        # {rel, kopf, body, typ, titel, quelle}
        self.medien = []         # {quelle, rel}
        self.erledigt = []       # Stuecke, die danach umziehen
        self.befunde = []        # (art, text, tun)
        self.abgebrochen = None

    def melde(self, art, text, tun=None):
        self.befunde.append((art, text, tun))

    def luecken(self):
        return [t for a, t, _ in self.befunde if a == "lücke"]


def _kopf_bauen(daten):
    """Frontmatter in fester Reihenfolge; leere Angaben entfallen (§3.4)."""
    reihe = ["type", "kind", "title", "description", "authors", "published",
             "published_year", "lang", "url", "file", "accessed", "checksum",
             "wikidata_id", "tags", "related"]
    zeilen = []
    for key in reihe + [k for k in sorted(daten) if k not in reihe]:
        wert = daten.get(key)
        if wert is None or wert == "" or wert == []:
            continue
        if isinstance(wert, list):
            zeilen.append("%s:" % key)
            for w in wert:
                zeilen.append('  - "%s"' % w if str(w).startswith("[[")
                              else "  - %s" % w)
        else:
            zeilen.append("%s: %s" % (key, notiz.skalar(wert)
                                      if isinstance(wert, str) else wert))
    return "\n".join(zeilen)


def _pflichtlücken(plan, typ, daten):
    """Was zu einer Zitation gehoert und fehlt — benannt, nicht geraten.

    Die Liste ist kein Konformitaetsbefund: Nichts davon ist Pflicht (Config
    §3.8ff). Sie ist der Auftrag an das Sprachmodell, das die Quelle liest.
    """
    if not daten.get("kind"):
        plan.melde("lücke",
                   "%s: die Werkart (`kind`) steht nicht fest."
                   % (daten.get("title") or "die Quelle"),
                   "Die Quelle lesen lassen; zur Wahl stehen: %s."
                   % ", ".join(WERKARTEN))
    noetig = {"book": ("title", "authors", "published_year"),
              "paper": ("title", "authors", "published_year"),
              "article": ("title", "authors", "published_year", "url"),
              "web": ("title", "url", "accessed"),
              "video": ("title", "url", "accessed"),
              "podcast": ("title", "url", "accessed"),
              "transcript": ("title", "authors")}.get(
                  str(daten.get("kind") or ""), ("title",))
    fehlt = [k for k in noetig if not daten.get(k)]
    if fehlt:
        plan.melde("lücke",
                   "%s: %s konnte nicht ermittelt werden."
                   % (daten.get("title") or "die Quelle", ", ".join("`%s`" % k
                                                                    for k in fehlt)),
                   "Die Quelle lesen lassen und nachtragen.")
    return fehlt


def _entlinken(wert):
    """`[[A|B]]` → `B`, `[[A]]` → `A` ohne Pfad. Sonst unveraendert.

    Ein Wikilink aus einem fremden Vault zeigt dorthin und loest hier nirgends
    auf (§3.6). Als Text ist er richtig — dafuer nimmt `hkf-link-or-text`
    beides (Config §2.1).
    """
    s = str(wert).strip()
    if not (s.startswith("[[") and s.endswith("]]")):
        return wert
    innen = s[2:-2]
    return (innen.split("|", 1)[1] if "|" in innen
            else innen.rsplit("/", 1)[-1]).strip()


def _erlaubt(typ):
    """Was die Typdefinition der Grundausstattung zusichert, plus A.2."""
    p = os.path.join(TEMPLATES, "hkb", ablage.VORGABEN["config_base"],
                     "Typedefs", typ + ".md")
    if not os.path.isfile(p):
        return None
    return set(_property_tabelle(frontmatter.lesen(p)[1])) | set(ALLGEMEIN) \
        | set(("related",))


def _gefiltert(plan, daten, typ, quelle):
    """Fremdes Frontmatter auf das beschraenken, was der Typ zusichert.

    Eine `.md` aus einem anderen Vault bringt dessen Vokabular mit. Es
    ungefiltert zu uebernehmen hiesse, eine fremde Ordnung einzuschleppen —
    und `hk-lint --strict` faende sie spaeter als undeklarierte Properties
    wieder. Was nicht passt, wird verworfen und gemeldet, wie beim Clipping.
    """
    erlaubt = _erlaubt(typ)
    if erlaubt is None:
        return dict(daten)
    aus, verworfen = {}, []
    for key, wert in sorted(daten.items()):
        if key in erlaubt:
            aus[key] = wert
        else:
            verworfen.append(key)
    if verworfen:
        plan.melde("hinweis",
                   "%s: %s gehört nicht zu `%s` und wurde verworfen."
                   % (os.path.basename(quelle), ", ".join("`%s`" % k
                                                          for k in verworfen), typ),
                   "Von Hand nachtragen, was davon zählt.")
    return aus


def _clipping_abbilden(plan, daten, quelle):
    """Das Frontmatter des Web Clipper auf `clipping` abbilden.

    Was nicht abbildbar ist, wird verworfen und gemeldet — nicht
    stillschweigend uebernommen, sonst landen verschachtelte Werte im
    Frontmatter und verletzen Anhang B.4.
    """
    aus, verworfen = {"type": QUELLTYP, "kind": "web"}, []
    for key, wert in sorted(daten.items()):
        if key == "type":
            continue
        ziel = CLIPPER.get(key, "?")
        if ziel == "?":
            if key in ("title", "url", "authors", "published_year", "accessed",
                       "kind", "lang", "tags", "related", "description"):
                ziel = key                     # schon HKF-Namen
            else:
                verworfen.append(key)
                continue
        if ziel is None:
            continue                           # `description` geht in den Body
        if ziel == "published_year" and wert:
            m = re.search(r"\d{4}", str(wert))
            wert = int(m.group(0)) if m else None
        elif ziel == "accessed" and wert:
            wert = str(wert)[:10]
        elif ziel in ("authors", "editors") and wert:
            roh = wert if isinstance(wert, list) else [wert]
            wert = [_entlinken(w) for w in roh]
            if [str(w) for w in roh] != [str(w) for w in wert]:
                plan.melde("hinweis",
                           "%s: `%s` stand als Wikilink in einen fremden Vault "
                           "und wurde zu Text." % (os.path.basename(quelle), key),
                           "Auf eine Personennotiz umstellen, wenn es sie gibt.")
        if isinstance(wert, (dict,)) or (isinstance(wert, list)
                                         and any(isinstance(x, (dict, list))
                                                 for x in wert)):
            verworfen.append(key)
            continue
        if wert not in (None, "", []):
            aus[ziel] = wert
    if verworfen:
        plan.melde("hinweis",
                   "%s: %s ließ sich nicht abbilden und wurde verworfen."
                   % (os.path.basename(quelle),
                      ", ".join("`%s`" % k for k in verworfen)),
                   "Von Hand nachtragen, was davon zählt.")
    return aus


# ── Ein Stueck einlesen ─────────────────────────────────────────────────

def _vorhandene(plan, rel):
    """Die Quellennotiz, die es schon gibt — in der Lieferung oder der Ablage."""
    orte = [os.path.join(plan.ziel, rel)]
    if plan.hkb:
        orte.append(os.path.join(plan.hkb, plan.quellbasis,
                                 os.path.basename(rel)))
    for p in orte:
        if os.path.isfile(p):
            return frontmatter.lesen(p)[0]
    return None


WERKZEUG = "hk-ingest"


def stueck(plan, quelle, art=None, angaben=None, kopieren=True, heute=None,
           zeitpunkt=None):
    """Ein Stueck einlesen: Notiz bauen, Datei kopieren, Luecken melden."""
    angaben = dict(angaben or {})
    quelle = os.path.abspath(quelle) if quelle else None
    ist_md = bool(quelle) and quelle.lower().endswith(".md")

    # Eine `.md` mit `type: source` ist die Notiz. Jede andere `.md` ist ein
    # Clipping — der erfasste Text einer Seite — und wird kopiert, weil sie
    # eine Datei ist und keine Notiz (Core §3.2.1).
    body, daten, clipping = "", {}, None
    if ist_md:
        roh_daten, roh_body = frontmatter.lesen(quelle)
        if str(roh_daten.get("type") or "").strip() == QUELLTYP:
            daten = _gefiltert(plan, roh_daten, QUELLTYP, quelle)
            body = roh_body.strip("\n")
        else:
            daten = _clipping_abbilden(plan, roh_daten, quelle)
            clipping = True
    if art and art not in WERKARTEN:
        plan.abgebrochen = ("%s ist keine Werkart. Zur Wahl stehen: %s."
                            % (art, ", ".join(WERKARTEN)))
        return None

    daten.update((k, v) for k, v in angaben.items() if v not in (None, "", []))
    if art:
        daten["kind"] = art
    daten["type"] = QUELLTYP
    titel = str(daten.get("title") or
                os.path.splitext(os.path.basename(quelle or "quelle"))[0])
    daten["title"] = titel
    name = slug(titel)
    if heute:
        daten.setdefault("accessed", heute)

    # Die Ausfertigung, in vier Faellen
    if clipping:
        # Ein Clipping ist Rohmaterial und wird kopiert; die Notiz daneben
        # traegt die Zusammenfassung (Config §3.8).
        rel_medium = "%s/%s/%s.md" % (CLIPPINGS[0], CLIPPINGS[1], name)
        plan.medien.append({"quelle": quelle, "rel": rel_medium})
        daten["file"] = "[[%s|%s.md]]" % (rel_medium, name)
        daten["checksum"] = pruefsumme(pfad=quelle)
    elif quelle and not ist_md and kopieren:
        endung = os.path.splitext(quelle)[1]
        rel_medium = "%s/%s/%s%s" % (MEDIEN[0], MEDIEN[1], name, endung)
        plan.medien.append({"quelle": quelle, "rel": rel_medium})
        daten["file"] = "[[%s|%s%s]]" % (rel_medium, name, endung)
        daten["checksum"] = pruefsumme(pfad=quelle)
    elif ist_md and body.strip():
        daten["checksum"] = pruefsumme(text=body)
    elif daten.get("file"):
        pass                                   # --ausfertigung: nichts kopieren

    rel = "%s/%s.md" % (QUELLVERZEICHNIS, name)
    alt = _vorhandene(plan, rel)
    if alt and daten.get("checksum") and alt.get("checksum") == daten["checksum"]:
        plan.melde("hinweis",
                   "%s gibt es schon und die Quelle hat sich nicht geändert."
                   % rel, "Nichts zu tun.")
        # Erledigt ist erledigt: Sonst laege das Stueck bei jedem Lauf wieder da.
        if quelle:
            plan.erledigt.append(quelle)
        return None
    if alt and daten.get("checksum") and alt.get("checksum"):
        plan.melde("hinweis",
                   "%s hat sich seit dem letzten Einlesen geändert (Drift)."
                   % rel, "Die Notiz gegen die neue Fassung prüfen.")

    # §6.1 Schritt 5 vergleicht ueber `modified`. Ohne die Angabe lehnte ein
    # zweiter Import die neu eingelesene Fassung als unvergleichbar ab.
    if zeitpunkt:
        daten["modified"] = zeitpunkt
        daten["modified_by"] = WERKZEUG

    _pflichtlücken(plan, QUELLTYP, daten)
    plan.notizen.append({"rel": rel, "kopf": _kopf_bauen(daten), "body": body,
                         "typ": QUELLTYP, "titel": titel, "quelle": quelle})
    if quelle:
        plan.erledigt.append(quelle)
    return rel


def hbundle(plan, bundle_id, beschreibung, version, titel=None):
    """Die Wurzeldatei der Lieferung (§4.1)."""
    if not titel:
        titel = (plan.notizen[0]["titel"] if len(plan.notizen) == 1
                 else "%d Quellen" % len(plan.notizen))
    # Jeder Wert durch `skalar`: Ein Titel mit Doppelpunkt waere sonst
    # kein YAML mehr, und genau die tragen Aufsaetze staendig.
    kopf = ("hkf: \"1.0\"\ntype: bundle\nid: %s\ntitle: %s\n"
            "description: %s\nversion: %s"
            % (bundle_id, notiz.skalar(titel), notiz.skalar(beschreibung),
               notiz.skalar(version)))
    # Die Tabelle nennt, was die Lieferung an Typen ausmacht — die
    # Grundausstattung bleibt draussen, sie hat jede HKB ohnehin (§3.8).
    # Die vier Quelltypen gehoeren dazu; die Tabelle bleibt darum in aller
    # Regel leer, so wie bei jeder Lieferung, die nur Bekanntes liefert.
    zeilen = ["# Typen", "", "| Typ | Verzeichnis | Zweck |", "|---|---|---|"]
    bekannt = grundtypen()
    for typ in sorted({n["typ"] for n in plan.notizen} - bekannt):
        d = _typdefinition(typ)
        zeilen.append("| %s | %s | %s |"
                      % (typ, QUELLVERZEICHNIS, d.get("description") or ""))
    return kopf, "\n".join(zeilen) + "\n"


def _typdefinition(typ):
    """Die Typdefinition aus der Vorlage, fuer den Zweck in der Typtabelle."""
    p = os.path.join(TEMPLATES, "hkb", ablage.VORGABEN["config_base"],
                     "Typedefs", typ + ".md")
    return frontmatter.lesen(p)[0] if os.path.isfile(p) else {}


def ausfuehren(plan, bundle_id, beschreibung, version, inbox=None):
    """Die Lieferung schreiben und die Stuecke nach `erledigt/` umlegen."""
    if plan.abgebrochen or not plan.notizen:
        return plan
    os.makedirs(plan.ziel, exist_ok=True)
    for n in plan.notizen:
        p = os.path.join(plan.ziel, n["rel"])
        os.makedirs(os.path.dirname(p), exist_ok=True)
        io.open(p, "w", encoding="utf-8").write(
            notiz.bauen(n["kopf"], n["body"]).rstrip("\n") + "\n")
    for m in plan.medien:
        p = os.path.join(plan.ziel, m["rel"])
        os.makedirs(os.path.dirname(p), exist_ok=True)
        shutil.copy2(m["quelle"], p)
    kopf, body = hbundle(plan, bundle_id, beschreibung, version)
    io.open(os.path.join(plan.ziel, "hbundle.md"), "w",
            encoding="utf-8").write(notiz.bauen(kopf, body))

    # Verschoben, nie geloescht.
    if inbox:
        fertig = os.path.join(inbox, ERLEDIGT, bundle_id)
        for q in plan.erledigt:
            if not q.startswith(os.path.abspath(inbox) + os.sep):
                continue
            os.makedirs(fertig, exist_ok=True)
            shutil.move(q, os.path.join(fertig, os.path.basename(q)))
    return plan
