#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueft, dass die Grundausstattung und HKF Config dasselbe sagen.

Das ganze Inventar steht zweimal: als eingebetteter Markdown-Block in HKF
Config §3 und als ausgelieferte Datei unter templates/hkb/. Die Property-Typen
ebenso — als Tabellen in §2. Die Spezifikation ist die normative Fassung.

Seit das Vokabular zur Grundausstattung gehoert, ist dies die einzige
Gegenprobe; `check-config.py` im Spec-Repository ist entfallen. Fuer die
Kern-Typen fehlte sie lange, und genau deshalb konnte `bundle` monatelang
`version` als Pflicht fuehren, obwohl die Spezifikation sie freistellt.

    python3 tools/grundausstattung.py [vorlagenverzeichnis]
"""
import difflib, io, os, re, sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WURZEL, "lib"))
import hkf                                                    # noqa: E402,F401
import yaml                                                   # noqa: E402
from hkf import CONFIG, frontmatter                           # noqa: E402

BLOCK = re.compile(r"^## 3\.\d+ `(\w+)`\n\n```markdown\n(.*?)\n```", re.S | re.M)
TYPEN, PROPTYPES = 17, 17
KONFIG = "90-System"   # Core §3.1, Vorgabe fuer config_base
ZEITEN = re.compile(r"^(created|modified|modified_by):.*\n", re.M)
EINSCHRAENKUNG = re.compile(r"`([a-z]+): ([^`]+)`")


def spec_text():
    return io.open(os.path.join(WURZEL, "spec", "HKF-Config-V%s.md" % CONFIG),
                   encoding="utf-8").read()


def kern_typen(spec, vorlage, melde):
    bloecke = BLOCK.findall(spec)
    if len(bloecke) != TYPEN:
        melde("§3 enthält %d Typdefinitionen, erwartet %d" % (len(bloecke), TYPEN), True)
        return
    for typ, block in bloecke:
        p = os.path.join(vorlage, KONFIG, "Typedefs", typ + ".md")
        if not os.path.exists(p):
            melde("%-10s fehlt in der Vorlage" % typ, True)
            continue
        a = block.strip().splitlines()
        b = ZEITEN.sub("", io.open(p, encoding="utf-8").read()).strip().splitlines()
        if a == b:
            melde("%-10s ok" % typ, False)
            continue
        melde("%-10s WEICHT AB (- Spezifikation, + Vorlage)" % typ, True)
        for l in difflib.unified_diff(a, b, lineterm="", n=0):
            if l[:2] not in ("--", "++"):
                melde("    " + l, False)


def standard_proptypes(spec, vorlage, melde):
    m = re.search(r"^## 2\.1 .*$", spec, re.M)
    assert m, "Config §2.1 nicht gefunden"
    teil = spec[m.end():]
    teil = teil.split("\n# 3.", 1)[0]
    erwartet = {}
    for zeile in teil.splitlines():
        m = re.match(r"^\| `(hkf-[a-z-]+)` \| `(\w+)` \| (.*?) \|$", zeile)
        if not m:
            continue
        name, form, rest = m.groups()
        soll = {"form": form}
        for schluessel, wert in EINSCHRAENKUNG.findall(rest):
            try:
                soll[schluessel] = yaml.safe_load(wert)
            except yaml.YAMLError:
                soll[schluessel] = wert
        erwartet[name] = soll
    if len(erwartet) != PROPTYPES:
        melde("§2 nennt %d Property-Typen, erwartet %d" % (len(erwartet), PROPTYPES), True)

    verz = os.path.join(vorlage, KONFIG, "Proptypes")
    vorhanden = set(f[:-3] for f in os.listdir(verz) if f.endswith(".md"))
    for name in sorted(erwartet):
        if name not in vorhanden:
            melde("%-18s fehlt in der Vorlage" % name, True)
            continue
        daten, _ = frontmatter.lesen(os.path.join(verz, name + ".md"))
        abweichung = []
        for schluessel, soll in sorted(erwartet[name].items()):
            ist = daten.get(schluessel)
            if ist != soll:
                abweichung.append("%s: %r statt %r" % (schluessel, ist, soll))
        for schluessel in ("pattern", "values", "min", "max"):
            if schluessel in daten and schluessel not in erwartet[name]:
                abweichung.append("%s: %r, §2.1 nennt keins"
                                  % (schluessel, daten[schluessel]))
        if abweichung:
            melde("%-18s WEICHT AB" % name, True)
            for a in abweichung:
                melde("    " + a, False)
        else:
            melde("%-18s ok" % name, False)
    for name in sorted(vorhanden - set(erwartet)):
        melde("%-18s liegt in der Vorlage, §2.1 nennt ihn nicht" % name, True)


def main(argv):
    if "--help" in argv or "-h" in argv:
        print(__doc__.strip())
        return 0
    args = [a for a in argv if not a.startswith("-")]
    vorlage = args[0] if args else os.path.join(WURZEL, "templates", "hkb")
    if not os.path.isdir(os.path.join(vorlage, KONFIG, "Typedefs")):
        sys.stderr.write("Keine Vorlage unter %s\n" % os.path.abspath(vorlage))
        return 2

    schlecht = [0]

    def melde(text, fehler):
        if fehler:
            schlecht[0] += 1
        print(("  " if text.startswith("    ") else "  ") + text)

    spec = spec_text()
    print("Vorlage: %s" % vorlage)
    print("Spezifikation: HKF Config %s" % CONFIG)
    print()
    print("Typdefinitionen (§3)")
    kern_typen(spec, vorlage, melde)
    print()
    print("Property-Typen (§2)")
    standard_proptypes(spec, vorlage, melde)
    print()
    if schlecht[0]:
        print("%d Abweichungen. Die Spezifikation gilt." % schlecht[0])
        return 1
    print("Die Grundausstattung entspricht der Spezifikation.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
