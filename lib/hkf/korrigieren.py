# -*- coding: utf-8 -*-
"""Was `hk-lint --fix` aendern darf — und nur das (Core §6.3).

Elf Handgriffe, alle mechanisch. Bei mehrdeutigen oder unbekannten Zielen wird
nicht geraten.

Zwei Grenzen nennt §6.3 ausdruecklich, und sie sind der Grund, warum diese
Datei kurz bleibt: `--fix` ergaenzt keinen Eintrag unter `# Siehe auch` und
entfernt keinen — Verknuepfen ist Sache des Imports, Entfernen Sache eines
Menschen. Und es legt keine vorlaeufige Typdefinition an und entfernt keine:
Dazwischen liegt eine Entscheidung ueber Bedeutung, und die trifft kein
Linter.
"""
import datetime, io, os, re, shutil

from . import TEMPLATES, ablage, frontmatter, notiz
from .importieren import STANDARD_PROPTYPES, _property_tabelle, _verzeichnis
from .pruefen import Bestand, ohne_code

WERKZEUG = "hk-lint"


def _schreiben(e, kopf, body):
    io.open(e["pfad"], "w", encoding="utf-8").write(notiz.bauen(kopf, body))


def _typtabelle(b, getan):
    zeilen = ["# Typen", "", "| Typ | Verzeichnis | Zweck |", "|---|---|---|"]
    for name in sorted(b.typdefs):
        d = b.typdefs[name]["daten"]
        zeilen.append("| %s | %s | %s |" % (name, b.ort(name, d),
                                            d.get("description") or ""))
    neu = "\n".join(zeilen) + "\n"
    if (notiz.abschnitt(b.wurzel_body, "Typen") or "").strip() == \
       "\n".join(zeilen[1:]).strip():
        return
    p = os.path.join(b.hkb, "hkb.md")
    kopf, body = notiz.teilen(io.open(p, encoding="utf-8").read())
    rest = notiz.ohne_abschnitt(body, "Typen").rstrip("\n")
    io.open(p, "w", encoding="utf-8").write(
        notiz.bauen(kopf, (rest + "\n\n" if rest else "") + neu))
    getan.append("hkb.md: Typtabelle neu erzeugt")


def _standard_proptypes(b, getan):
    quelle = os.path.join(TEMPLATES, "hkb",
                          ablage.VORGABEN["config_base"], "Proptypes")
    ziel = os.path.join(b.konfig, "Proptypes")
    for name in sorted(STANDARD_PROPTYPES - set(b.proptypes)):
        vorlage = os.path.join(quelle, name + ".md")
        if not os.path.isfile(vorlage):
            continue
        os.makedirs(ziel, exist_ok=True)
        shutil.copy2(vorlage, os.path.join(ziel, name + ".md"))
        getan.append("Proptypes/%s.md: angelegt (§3.5.1)" % name)


def _verweise(b, getan):
    """Verzeichnislose Ziele qualifizieren, fehlende Aliase ergaenzen (§3.6)."""
    nach_namen = {}
    for rel in b.notizen:
        nach_namen.setdefault(rel.rsplit("/", 1)[-1], []).append(rel)
    pre = b.praefix()

    for rel, e in sorted(b.notizen.items()):
        geaendert = []

        def ersetzen(m):
            ganz, ziel, alias = m.group(0), m.group(1), m.group(2)
            art, rest = b.aufloesen(ziel)
            if art is None and "/" not in ziel:
                treffer = nach_namen.get(ziel) or []
                if len(treffer) != 1:
                    return ganz               # mehrdeutig — nicht raten
                rest = treffer[0]
                ziel_neu = "%s/%s" % (pre, rest) if pre else rest
                geaendert.append("[[%s]] qualifiziert" % ziel)
                art = "notiz"
            elif art == "notiz":
                ziel_neu = ziel
            else:
                return ganz
            if alias is None:
                titel = str(b.notizen[rest]["daten"].get("title") or
                            rest.rsplit("/", 1)[-1])
                geaendert.append("Alias für [[%s]] ergänzt" % ziel_neu)
                return "[[%s|%s]]" % (ziel_neu, titel)
            return ganz.replace("[[" + ziel, "[[" + ziel_neu, 1)

        muster = re.compile(r"\[\[([^\]|\\]+)(?:\|([^\]]*))?\]\]")
        kopf = muster.sub(ersetzen, e["kopf"])
        teile = re.split(r"(```.*?```|`[^`\n]*`)", e["body"], flags=re.S)
        body = "".join(t if i % 2 else muster.sub(ersetzen, t)
                       for i, t in enumerate(teile))
        if geaendert:
            _schreiben(e, kopf, body)
            e["kopf"], e["body"] = kopf, body
            for g in sorted(set(geaendert)):
                getan.append("%s: %s" % (e["rel"], g))


def _typangaben(b, getan):
    """Die Leerzeichen um den Alternativen-Trenner ` / ` (§3.7.2)."""
    for name, e in sorted(b.typdefs.items()):
        teil = notiz.abschnitt(e["body"], "Properties")
        if teil is None:
            continue
        neu = []
        aenderung = False
        for zeile in e["body"].splitlines():
            if zeile.startswith("|"):
                s = zeile.split("|")
                if len(s) > 3 and "/" in s[2]:
                    ordentlich = " / ".join(x.strip() for x in s[2].split("/"))
                    if s[2].strip() != ordentlich:
                        s[2] = " %s " % ordentlich
                        zeile = "|".join(s)
                        aenderung = True
            neu.append(zeile)
        if aenderung:
            body = "\n".join(neu)
            _schreiben(e, e["kopf"], body)
            e["body"] = body
            getan.append("%s: Trenner ` / ` ausgeschrieben" % e["rel"])


def _zeiten(b, getan):
    """datetime ohne Uhrzeit ausschreiben, created/modified ergaenzen."""
    heute = datetime.datetime.now()
    tag, jetzt = heute.strftime("%Y-%m-%d"), heute.strftime("%Y-%m-%dT%H:%M:%S")
    for rel, e in sorted(b.notizen.items()):
        kopf, geaendert = e["kopf"], []
        felder = {"modified": "datetime"}
        for prop, (t, _p) in _property_tabelle(
                b.typdefs.get(e["typ"], {}).get("body", "")).items():
            if t.strip() == "datetime":
                felder[prop] = "datetime"
        for feld in sorted(felder):
            wert = str(e["daten"].get(feld) or "")
            if re.match(r"^\d{4}-\d{2}-\d{2}$", wert):
                kopf = notiz.setze_skalar(kopf, feld, wert + "T00:00:00")
                geaendert.append("`%s` auf den Tagesbeginn ausgeschrieben" % feld)
        if "created" not in e["daten"]:
            kopf = notiz.setze_skalar(kopf, "created", tag)
            geaendert.append("`created` ergänzt")
        if "modified" not in e["daten"]:
            kopf = notiz.setze_skalar(kopf, "modified", jetzt)
            geaendert.append("`modified` ergänzt")
        if geaendert:
            # §3.3: Wer aendert, schreibt es hin — und geaendert hat soeben
            # dieses Werkzeug.
            kopf = notiz.setze_skalar(kopf, "modified_by", WERKZEUG)
            _schreiben(e, kopf, e["body"])
            e["kopf"] = kopf
            getan.append("%s: %s" % (e["rel"], ", ".join(geaendert)))


def _leere_properties(b, getan):
    for rel, e in sorted(b.notizen.items()):
        leer = [k for k, v in e["daten"].items()
                if v is None or (isinstance(v, (list, dict, str)) and len(v) == 0)]
        if not leer:
            continue
        kopf = e["kopf"]
        for k in sorted(leer):
            kopf = notiz.entfernen(kopf, k)
        _schreiben(e, kopf, e["body"])
        e["kopf"] = kopf
        getan.append("%s: leere Properties entfernt (%s)"
                     % (e["rel"], ", ".join(sorted(leer))))


def _siehe_auch(b, getan):
    """Ordnen und ans Ende stellen; `related` daraus ergaenzen (§5.6)."""
    for rel, e in sorted(b.notizen.items()):
        teil = notiz.abschnitt(e["body"], "Siehe auch")
        if teil is None:
            continue
        zeilen = [z for z in teil.strip("\n").splitlines() if z.startswith("- ")]
        if not zeilen:
            continue
        geordnet = sorted(zeilen, key=lambda z: (
            re.sub(r"^- \[\[[^\]|]*\|?", "", z).split("]]")[0] or z).lower())
        rest = notiz.ohne_abschnitt(e["body"], "Siehe auch").rstrip("\n")
        body = rest + "\n\n# Siehe auch\n\n" + "\n".join(geordnet) + "\n"
        geaendert = []
        if body.rstrip("\n") != e["body"].rstrip("\n"):
            geaendert.append("`# Siehe auch` geordnet und ans Ende gestellt")

        kopf = e["kopf"]
        verwandt = notiz.lies_liste(kopf, "related")
        andere = notiz.entfernen(notiz.entfernen(kopf, "related"), "rejected_links")
        neu = list(verwandt)
        for z in geordnet:
            m = re.match(r"^- (\[\[([^\]|\\]+)(?:\|[^\]]*)?\]\])", z)
            if not m:
                continue
            link, ziel = m.group(1), m.group(2)
            if ziel in andere or any(ziel in x for x in verwandt):
                continue
            neu.append(link)
        if neu != verwandt:
            kopf = notiz.setze_liste(kopf, "related", sorted(neu))
            geaendert.append("`related` ergänzt")
        if geaendert:
            _schreiben(e, kopf, body)
            e["kopf"], e["body"] = kopf, body
            getan.append("%s: %s" % (e["rel"], ", ".join(geaendert)))


KORREKTUREN = (_standard_proptypes, _verweise, _typangaben, _zeiten,
               _leere_properties, _siehe_auch, _typtabelle)


def korrigieren(hkb):
    """Der Reihe nach; die Typtabelle zuletzt, damit sie das Ergebnis zeigt."""
    b = Bestand(hkb)
    getan = []
    for f in KORREKTUREN:
        f(b, getan)
    return getan
