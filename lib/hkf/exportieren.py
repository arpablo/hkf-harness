# -*- coding: utf-8 -*-
"""Ein Bundle aus der Wissensbasis herausschreiben — Core §6.2.

Streng im Schreiben, grosszuegig im Lesen: Ein Bundle duerfte beliebig
aufgebaut sein (§4), aber geschrieben wird der typbezogene Baum mit
`Typedefs/`, `Proptypes/` und `Media/<art>/`.

Zwei Lesarten seien genannt, wo §6.2 offen ist:

Schritt 8 sagt, Verweise auf Notizen ausserhalb des Bundles blieben
„unveraendert erhalten". Das heisst hier: Sie werden nicht entfernt — der
Praefix der Wissensbasis faellt trotzdem, wie bei jedem anderen Verweis auch
(Schritt 5). Ein Ziel, das den Ablagepfad des Absenders mitfuehrt, waere beim
Empfaenger nicht nur unaufloesbar, sondern irrefuehrend.

Und `related`: §5.6 fuehrt die Property als aus `# Siehe auch` abgeleitet. Was
Schritt 7 aus dem Abschnitt nimmt, wird darum auch aus `related` genommen. Was
dort nie aus dem Abschnitt kam — eine Adresse, ein von Hand gesetzter Verweis
—, bleibt und wird nach Schritt 8 gemeldet.
"""
import io, os, re, shutil

from . import CORE, ablage, frontmatter, notiz
QUELLVERZEICHNIS = "Sources"   # wo eine Quellennotiz in der Lieferung liegt

from .importieren import (ARTVERZEICHNIS, STANDARD_PROPTYPES, grundtypen,
                          medienart, _bereich, _property_tabelle,
                          _verzeichnis)

WERKZEUG = "hk-export"


class Plan(object):
    def __init__(self, hkb, bundle_id, ziel, media_base="Media"):
        self.hkb = hkb
        self.bundle_id = bundle_id
        self.ziel = os.path.abspath(ziel)
        self.basis = ablage.basis(hkb)
        self.ablagepfad = ablage.ablagepfad(hkb)
        daten, _ = frontmatter.lesen(os.path.join(hkb, "hkb.md"))
        self.bereiche = ablage.bereiche(hkb)
        self.hkb_media = self.bereiche["media_base"]
        self.hkb_base = self.bereiche["wiki_base"]
        self.quellbasis = self.bereiche["source_base"]
        self.konfig = os.path.join(hkb, self.bereiche["config_base"])
        self.media_base = media_base.strip("/")
        self.bundle = {}
        self.bundle_body = ""
        self.notizen = []       # {quelle, rel, kopf, body, typ}
        self.typdefs = []       # rel der mitgeschriebenen Typdefinitionen
        self.proptypes = []
        self.medien = []        # {quelle, rel, art}
        self.befunde = []       # (art, text, tun)
        self.abgebrochen = None

    def melde(self, art, text, tun=None):
        self.befunde.append((art, text, tun))

    def praefix_notizen(self, bereich="wiki_base"):
        teile = [t for t in (self.ablagepfad, self.bereiche[bereich]) if t]
        return "/".join(teile)

    def praefixe(self):
        """Alle Praefixe, unter denen eine Notiz liegen kann (§3.1)."""
        return [p for p in (self.praefix_notizen(k) for k in
                            ("wiki_base", "source_base", "config_base")) if p]

    def praefix_medien(self):
        teile = [t for t in (self.ablagepfad, self.hkb_media) if t]
        return "/".join(teile)


def _mitglied(daten, bundle_id):
    """Traegt die Notiz dieses Bundle in `bundles` (§5.2)?"""
    ziel = "Bundles/%s" % bundle_id
    for l in daten.get("bundles") or []:
        m = re.match(r"^\[\[([^\]|]+)", str(l))
        if m and m.group(1).endswith(ziel):
            return True
    return False


def _gelieferte_typen(plan, vorausgesetzt):
    """Typen und Property-Typen, die ein vorausgesetztes Bundle liefert.

    §7.1: Ein Bundle muss nur mitschreiben, was weder zur Grundausstattung
    gehoert noch aus einem vorausgesetzten Bundle kommt.
    """
    aus = set()
    if not vorausgesetzt:
        return aus
    for verz in ("Typedefs", "Proptypes"):
        d = os.path.join(plan.konfig, verz)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith(".md"):
                continue
            daten, _ = frontmatter.lesen(os.path.join(d, f))
            for l in daten.get("bundles") or []:
                m = re.search(r"Bundles/([a-z][a-z0-9-]*)\|", str(l))
                if m and m.group(1) in vorausgesetzt:
                    aus.add("%s/%s" % (verz, f[:-3]))
    return aus


def planen(hkb, bundle_id, ziel, media_base="Media"):
    plan = Plan(hkb, bundle_id, ziel, media_base)
    quelle = os.path.join(plan.basis, "Bundles", bundle_id + ".md")
    if not os.path.isfile(quelle):
        plan.abgebrochen = ("Die Wissensbasis führt kein Bundle `%s` — "
                            "%s gibt es nicht." % (bundle_id, quelle))
        return plan
    plan.bundle, plan.bundle_body = frontmatter.lesen(quelle)

    vorausgesetzt = set()
    for e in plan.bundle.get("required_bundles") or []:
        m = re.match(r"^\s*([a-z][a-z0-9-]*)", str(e))
        if m:
            vorausgesetzt.add(m.group(1))
    von_anderen = _gelieferte_typen(plan, vorausgesetzt)

    # 1. Die Notizen der Lieferung
    #
    # Der Quellenbereich gehoert der Wissensbasis und nicht der Lieferung
    # (§4.3): Er wird beim Sammeln abgestreift, sonst truege das Bundle den
    # `source_base` des Absenders. Wo `base` nicht leer ist, liegt er neben
    # den Typverzeichnissen und wird eigens durchlaufen.
    wurzeln, gesehen = [], set()
    for k in ("wiki_base", "source_base", "config_base"):
        w = os.path.join(plan.hkb, plan.bereiche[k])
        if os.path.isdir(w) and w not in gesehen:
            gesehen.add(w)
            wurzeln.append((k, w))
    for k, w in wurzeln:
        for p in ablage.dateien(w):
            rel = os.path.relpath(p, w).replace(os.sep, "/")
            # Ohne Typverzeichnis liegt nur die Quellennotiz (§3.2.2).
            if ("/" not in rel and k != "source_base") \
                    or rel.startswith("Bundles/"):
                continue
            daten, body = frontmatter.lesen(p)
            if "type" not in daten or not _mitglied(daten, bundle_id):
                continue
            kopf = notiz.teilen(io.open(p, encoding="utf-8").read())[0]
            if "/" not in rel:
                # Die Quellennotiz liegt in der HKB ohne Typverzeichnis
                # (§3.2.2). In der Lieferung bekommt sie eines — sonst laege
                # sie neben `hbundle.md` und saehe nach Beiwerk aus. Wohin sie
                # beim Import kommt, entscheidet ohnehin ihr Typ (§4.3).
                rel = "%s/%s" % (QUELLVERZEICHNIS, rel)
            plan.notizen.append({"quelle": p, "rel": rel, "kopf": kopf,
                                 "body": body, "typ": str(daten["type"])})
    if not plan.notizen:
        plan.melde("hinweis", "Keine Notiz trägt dieses Bundle in `bundles`.",
                   "Prüfen, ob die `id` stimmt.")

    # 3. Typdefinitionen und Property-Typen
    typen = sorted({n["typ"] for n in plan.notizen})
    schon = {n["rel"] for n in plan.notizen}
    proptypes = set()
    for typ in typen:
        if typ in grundtypen():
            # §7.1: Was zur Grundausstattung gehoert (§3.8), muss ein Bundle
            # nicht mitbringen — jede konforme HKB fuehrt es ohnehin.
            continue
        rel = "Typedefs/%s" % typ
        p = os.path.join(plan.konfig, rel + ".md")
        if not os.path.isfile(p):
            plan.melde("konflikt", "Der Typ %s hat keine Typdefinition." % typ,
                       "Die Ablage mit hk-lint prüfen.")
            continue
        daten, body = frontmatter.lesen(p)
        if daten.get("provisional"):
            plan.melde("konflikt",
                       "Der Typ %s ist nur vorläufig registriert (§5.4) und "
                       "wird nicht mitgeschrieben." % typ,
                       "Die richtige Typdefinition beschaffen, bevor die "
                       "Lieferung weitergegeben wird.")
            continue
        for _, (t, _p2) in _property_tabelle(body).items():
            for stueck in re.split(r"\s*/\s*", t):
                proptypes.add(stueck.split(":", 1)[0].strip())
        if rel in von_anderen:
            continue
        if rel + ".md" not in schon:
            plan.typdefs.append(rel)
    for name in sorted(proptypes):
        rel = "Proptypes/%s" % name
        if name in STANDARD_PROPTYPES or rel in von_anderen:
            continue
        if not os.path.isfile(os.path.join(plan.konfig, rel + ".md")):
            continue
        if rel + ".md" not in schon:
            plan.proptypes.append(rel)

    # 5. und 7. Verweise umschreiben, Abschnitt filtern (vor dem Nachweis,
    # damit plan.medien gefuellt ist)
    drin = {n["rel"][:-3] for n in plan.notizen} | \
           {r for r in plan.typdefs + plan.proptypes}
    for n in plan.notizen:
        n["kopf"], n["body"] = _umschreiben(plan, n, drin)
    for rel in plan.typdefs + plan.proptypes:
        p = os.path.join(plan.konfig, rel + ".md")
        kopf, body = notiz.teilen(io.open(p, encoding="utf-8").read())
        e = {"rel": rel + ".md", "kopf": kopf, "body": body, "quelle": p}
        e["kopf"], e["body"] = _umschreiben(plan, e, drin)
        plan.notizen.append(dict(e, typ=os.path.dirname(rel)[:-1], mit=True))

    _unverwiesene_medien(plan)
    return plan


def _unverwiesene_medien(plan):
    """Mediendateien, die einmal mit der Lieferung kamen und heute an keiner
    Notiz haengen.

    §6.2 Schritt 4 nimmt mit, worauf die Notizen verweisen — mehr nicht. Eine
    Datei, die niemand nennt, bleibt also zurueck. Das ist richtig so, aber
    still: Wer eine Lieferung weitergibt, soll es erfahren. Gefragt wird der
    juengste Importnachweis (§5.1) — ein Protokoll, keine
    Zugehoerigkeitsangabe, darum ein Hinweis und kein Befund.
    """
    teil = re.split(r"^# Import", plan.bundle_body, flags=re.M)
    if len(teil) < 2:
        return
    pre = plan.praefix_medien()
    haben = {m["rel"] for m in plan.medien}
    fehlen = []
    for zeile in teil[1].splitlines():
        m = re.match(r"^\| \[\[([^\]|\\]+)", zeile)
        if not m:
            continue
        ziel = m.group(1)
        if pre and not ziel.startswith(pre + "/"):
            continue
        neu = _medienziel(plan, ziel)
        if neu not in haben and neu not in fehlen:
            fehlen.append(neu)
    if fehlen:
        plan.melde("hinweis",
                   "%d Mediendateien kamen mit der Lieferung, hängen aber an "
                   "keiner Notiz und bleiben zurück: %s"
                   % (len(fehlen), ", ".join(f.rsplit("/", 1)[-1]
                                             for f in fehlen)) + ".",
                   "Sie in einer Notiz verweisen, wenn sie mitgehen sollen.")


def _medienziel(plan, ziel):
    """`<ablagepfad>/<media_base>/Images/x.png` → `Media/Images/x.png`."""
    pre = plan.praefix_medien()
    rest = ziel[len(pre) + 1:] if pre else ziel
    return "%s/%s" % (plan.media_base, rest) if plan.media_base else rest


def _umschreiben(plan, e, drin):
    """Praefix entfernen, Mediendateien einsammeln, `# Siehe auch` filtern."""
    pre_m = plan.praefix_medien()
    entfernt = []

    def ziel_neu(ziel):
        if pre_m and ziel.startswith(pre_m + "/"):
            neu = _medienziel(plan, ziel)
            quelle = os.path.join(plan.hkb, ziel[len(plan.ablagepfad) + 1:]
                                  if plan.ablagepfad else ziel)
            if os.path.isfile(quelle) and \
               not any(m["rel"] == neu for m in plan.medien):
                plan.medien.append({"quelle": quelle, "rel": neu,
                                    "art": medienart(neu)})
            return neu, True
        # Jeder Bereich bleibt zu Hause (§4.3): In der Lieferung liegt die
        # Notiz unter ihrem blossen Typverzeichnis.
        neu = ziel
        for pre in plan.praefixe():
            if neu.startswith(pre + "/"):
                neu = neu[len(pre) + 1:]
                break
        else:
            if plan.ablagepfad and neu.startswith(plan.ablagepfad + "/"):
                neu = neu[len(plan.ablagepfad) + 1:]
        return neu, neu in drin

    def ersetzen(m):
        roh, ziel = m.group(0), m.group(1)
        neu, bekannt = ziel_neu(ziel)
        if not bekannt:
            plan.melde("hinweis",
                       "%s: [[%s]] zeigt aus dem Bundle hinaus und bleibt stehen."
                       % (e["rel"], neu))
        return roh.replace("[[" + ziel, "[[" + neu, 1)

    body = e["body"]
    teil = notiz.abschnitt(body, "Siehe auch")
    if teil is not None:
        bleiben = []
        for zeile in teil.strip("\n").splitlines():
            m = re.match(r"^- \[\[([^\]|]+)", zeile)
            if not m:
                continue
            neu, bekannt = ziel_neu(m.group(1))
            if bekannt:
                bleiben.append(zeile.replace("[[" + m.group(1), "[[" + neu, 1))
            else:
                entfernt.append("[[%s|" % neu)
        rest = notiz.ohne_abschnitt(body, "Siehe auch").rstrip("\n")
        body = rest + ("\n\n# Siehe auch\n\n" + "\n".join(bleiben) + "\n"
                       if bleiben else "\n")

    kopf = notiz.entfernen(notiz.entfernen(e["kopf"], "bundles"), "rejected_links")
    rel = notiz.lies_liste(kopf, "related")
    if rel:
        bleiben = [r for r in rel if not any(r.startswith(x.replace("[[", "[["))
                                             or x[2:-1] in r for x in entfernt)]
        kopf = notiz.setze_liste(kopf, "related", bleiben)
    umschreiben = lambda s: re.sub(r"\[\[([^\]|\\]+)", ersetzen, s)
    kopf = notiz.ausserhalb_code(kopf, umschreiben)
    body = notiz.ausserhalb_code(body, umschreiben)
    return kopf, body


def _hbundle(plan):
    # Keine Bereiche: In einer Lieferung sind sie ohne Wirkung (A.1, §4.3),
    # und was niemand liest, gehoert nicht hinein.
    felder = ["hkf: \"%s\"" % (plan.bundle.get("hkf") or CORE),
              "type: bundle", "id: %s" % plan.bundle_id]
    if plan.bundle.get("required_bundles"):
        felder.append("required_bundles:")
        felder += ["  - %s" % e for e in plan.bundle["required_bundles"]]
    for k in ("title", "description", "source", "version"):
        if plan.bundle.get(k) is not None:
            felder.append("%s: %s" % (k, notiz.skalar(plan.bundle[k])))
    kopf = "\n".join(felder)

    body = plan.bundle_body
    body = notiz.ohne_abschnitt(body, "Entscheidungen")
    body = re.split(r"^# Import", body, 1, flags=re.M)[0].strip("\n")
    # Die Tabelle nennt, was die Lieferung an Typen ausmacht: die Typen ihrer
    # Notizen und die Typdefinitionen, die sie mitbringt. Die Grundausstattung
    # bleibt draussen — sie hat jede HKB (§3.8).
    typen = {n["typ"] for n in plan.notizen} - grundtypen()
    for n in plan.notizen:
        if n["rel"].startswith("Typedefs/"):
            typen.add(os.path.basename(n["rel"])[:-3])
    zeilen = ["# Typen", "", "| Typ | Verzeichnis | Zweck |", "|---|---|---|"]
    for typ in sorted(typen):
        p = os.path.join(plan.konfig, "Typedefs", typ + ".md")
        d = frontmatter.lesen(p)[0] if os.path.isfile(p) else {}
        # Eine Lieferung kennt keine Bereiche (§4.3): das blosse `dir`.
        zeilen.append("| %s | %s | %s |" % (typ, _verzeichnis(typ, d),
                                            d.get("description") or ""))
    return kopf, (body + "\n\n" if body else "") + "\n".join(zeilen) + "\n"


def ausfuehren(plan):
    if plan.abgebrochen:
        return plan
    os.makedirs(plan.ziel, exist_ok=True)
    for n in plan.notizen:
        ziel = os.path.join(plan.ziel, n["rel"])
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        io.open(ziel, "w", encoding="utf-8").write(notiz.bauen(n["kopf"], n["body"]))
    for m in plan.medien:
        ziel = os.path.join(plan.ziel, m["rel"])
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        shutil.copy2(m["quelle"], ziel)
    kopf, body = _hbundle(plan)
    io.open(os.path.join(plan.ziel, "hbundle.md"), "w", encoding="utf-8").write(
        notiz.bauen(kopf, body))
    return plan
