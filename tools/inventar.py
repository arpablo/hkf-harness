#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueft, dass Prosa, Schema und Grundausstattung dasselbe Inventar nennen.

Drei Stellen sagen, was HKF Config enthaelt, und sie sind schon einmal
auseinandergelaufen: Die Tabelle in Config §2.1 fuehrte vierzehn
Standard-Property-Typen, die Menge im Harness dreizehn, und die Zahlwoerter in
Core standen auf einem noch aelteren Stand. Gemerkt hat es niemand, weil
nichts die Stellen gegeneinander hielt.

    python3 tools/inventar.py

Geprueft wird gegen die Fassung unter `spec/` — die, die dieser Harness
umsetzt. `HKF_SPEC` zeigt auf eine andere; `tools/spec.py` sagt, ob die Kopie
noch stimmt.

- Config §2.1 gegen `#/$defs/standard-proptypes` im Schema (Core §3.5.1),
- jeder aufgezaehlte Name hat auch ein `$defs` mit seinem Muster (Anhang B.4),
- Config §2.1 und §2.2 zusammen gegen `templates/hkb/` — die Property-Typen
  der Grundausstattung,
- die Abschnitte `## 3.x` gegen deren Typdefinitionen,
- die Zahlwoerter in Core und Config gegen die gezaehlten Mengen,
- die abgeleitete Tabelle in Config §2.3 gegen die Property-Tabellen der
  Typdefinitionen (Core §3.7.3).
"""
import io, os, re, sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WURZEL, "lib"))
from hkf import CORE, SPEC, TEMPLATES, ablage, frontmatter      # noqa: E402
from hkf.importieren import _property_tabelle                   # noqa: E402
from hkf import schema as schemamodul                           # noqa: E402

ZAHLWORT = {13: "dreizehn", 14: "vierzehn", 15: "fünfzehn", 16: "sechzehn",
            17: "siebzehn", 18: "achtzehn", 19: "neunzehn", 20: "zwanzig"}


def tabelle(text, von, bis, muster=r"^\| `([a-z][a-z0-9-]*)`"):
    """Die Namen in der ersten Spalte einer Tabelle zwischen zwei Ueberschriften."""
    if von not in text:
        return []
    ab = text.split(von, 1)[1]
    if bis and bis in ab:
        ab = ab.split(bis, 1)[0]
    return re.findall(muster, ab, re.M)


def main(argv=()):
    if "--help" in argv or "-h" in argv:
        print(__doc__.strip())
        return 0
    spec = os.environ.get("HKF_SPEC") or SPEC
    befunde = []

    def melde(text):
        befunde.append(text)

    core = io.open(os.path.join(spec, "HKF-Core-V%s.md" % CORE),
                   encoding="utf-8").read()
    cfg = io.open(os.path.join(spec, "HKF-Config-V1.0.md"),
                  encoding="utf-8").read()
    # Das Schema aus derselben Quelle wie die Prosa, nicht das des Harness:
    # Sonst hielte die Pruefung zwei Auslieferungen gegeneinander und uebersaehe
    # gerade die Abweichung, die sie finden soll. Unter `spec/` liegt es neben
    # den Dokumenten, im Spezifikations-Repository unter `schema/`.
    name = "hkf-core-%s.schema.json" % CORE
    for kandidat in (os.path.join(spec, name), os.path.join(spec, "schema", name)):
        if os.path.isfile(kandidat):
            break
    else:
        sys.stderr.write("%s: kein %s.\n" % (spec, name))
        return 2
    defs = schemamodul.laden(kandidat)["$defs"]

    # 1. Config §2.1 gegen das Schema
    aus_prosa = tabelle(cfg, "## 2.1", "## 2.2")
    aus_schema = defs.get("standard-proptypes", {}).get("enum")
    if aus_schema is None:
        melde("Das Schema führt kein `#/$defs/standard-proptypes` (Core §3.5.1).")
        aus_schema = []
    if sorted(set(aus_prosa) - set(aus_schema)):
        melde("In Config §2.1, nicht im Schema: %s"
              % ", ".join(sorted(set(aus_prosa) - set(aus_schema))))
    if sorted(set(aus_schema) - set(aus_prosa)):
        melde("Im Schema, nicht in Config §2.1: %s"
              % ", ".join(sorted(set(aus_schema) - set(aus_prosa))))

    # 2. Jeder Standard-Property-Typ hat sein Muster
    ohne = sorted(n for n in aus_schema if n not in defs)
    if ohne:
        melde("Aufgezählt, aber ohne `$defs` mit Muster (Anhang B.4): %s"
              % ", ".join(ohne))

    # 3. Die Grundausstattung
    # Die Grenze ist §2.3 und nicht das Typkapitel: Dazwischen liegt die
    # abgeleitete Tabelle der Properties, deren Zeilen genauso aussehen.
    aufzaehlungen = tabelle(cfg, "## 2.2", "## 2.3")
    grund = os.path.join(TEMPLATES, "hkb", ablage.VORGABEN["config_base"])
    for teil, erwartet, wo in (
            ("Proptypes", set(aus_prosa) | set(aufzaehlungen),
             "Config §2.1 und §2.2"),
            ("Typedefs",
             set(re.findall(r"^## 3\.\d+ `([a-z][a-z0-9-]*)`", cfg, re.M)),
             "die Abschnitte Config §3.x")):
        verz = os.path.join(grund, teil)
        if not os.path.isdir(verz):
            melde("Die Grundausstattung führt kein %s/." % teil)
            continue
        da = set(f[:-3] for f in os.listdir(verz) if f.endswith(".md"))
        if da - erwartet:
            melde("In der Grundausstattung, nicht in %s: %s"
                  % (wo, ", ".join(sorted(da - erwartet))))
        if erwartet - da:
            melde("In %s, nicht in der Grundausstattung: %s"
                  % (wo, ", ".join(sorted(erwartet - da))))

    # 4. Die Zahlwörter
    n_typen = len(re.findall(r"^## 3\.\d+ `", cfg, re.M))
    n_props = len(aus_prosa) + len(aufzaehlungen)
    for datei, text in (("HKF-Core-V%s.md" % CORE, core),
                        ("HKF-Config-V1.0.md", cfg)):
        for m in re.finditer(r"(\w+)\s+Typdefinitionen und\s+(\w+)\s+Property-Typen",
                             text):
            if m.group(1).lower() != ZAHLWORT.get(n_typen) or \
               m.group(2).lower() != ZAHLWORT.get(n_props):
                melde("%s: „%s Typdefinitionen und %s Property-Typen\" — gezählt "
                      "sind %s und %s."
                      % (datei, m.group(1), m.group(2),
                         ZAHLWORT.get(n_typen, n_typen),
                         ZAHLWORT.get(n_props, n_props)))
    if ZAHLWORT.get(len(aus_prosa)) and \
            "## 2.1 Die %s Standard-Property-Typen" % ZAHLWORT[len(aus_prosa)] \
            not in cfg:
        melde("Die Überschrift von Config §2.1 nennt nicht %s."
              % ZAHLWORT[len(aus_prosa)])

    # 5. Config §2.3 gegen die Property-Tabellen der Grundausstattung
    reg = {}
    verz = os.path.join(grund, "Typedefs")
    if os.path.isdir(verz):
        for f in sorted(os.listdir(verz)):
            if not f.endswith(".md"):
                continue
            body = frontmatter.lesen(os.path.join(verz, f))[1]
            for prop, (angabe, _pflicht) in _property_tabelle(body).items():
                reg.setdefault(prop, set()).add(angabe)
    aus_23 = {}
    for zeile in tabelle(cfg, "## 2.3", "# 3. Typdefinitionen",
                         muster=r"^\| `([a-z_]+)` \| `([^`]+)` \|"):
        aus_23[zeile[0]] = set(x.strip() for x in zeile[1].split("·"))
    if not aus_23:
        melde("Config §2.3 führt keine Tabelle der Properties (Core §3.7.3).")
    else:
        if sorted(set(reg) - set(aus_23)):
            melde("In den Typdefinitionen, nicht in Config §2.3: %s"
                  % ", ".join(sorted(set(reg) - set(aus_23))))
        if sorted(set(aus_23) - set(reg)):
            melde("In Config §2.3, nicht in den Typdefinitionen: %s"
                  % ", ".join(sorted(set(aus_23) - set(reg))))
        for prop in sorted(set(reg) & set(aus_23)):
            if reg[prop] != aus_23[prop]:
                melde("`%s`: Config §2.3 nennt %s, die Typdefinitionen %s."
                      % (prop, " · ".join(sorted(aus_23[prop])),
                         " · ".join(sorted(reg[prop]))))

    print("%d Typdefinitionen, %d Property-Typen (%d Standard, %d Aufzählungen), "
          "%d Properties" % (n_typen, n_props, len(aus_prosa),
                             n_props - len(aus_prosa), len(reg)))
    for b in befunde:
        print("  -", b)
    print("%d Befunde" % len(befunde))
    return 1 if befunde else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
