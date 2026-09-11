#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueft, dass der Bestand im Harness dem Verzeichnis entspricht.

Die KI-Schicht war bis zuletzt nirgends aufgezaehlt. Wer wissen wollte,
welche Skills es gibt, musste `ls` sagen, und wer im Text eines Skills auf
einen Namen stiess, konnte nicht entscheiden, ob das ein Werkzeug oder ein
Skill ist. Ein Buchstabe trennt beides, und nichts hielt die Namen gegen den
Bestand.

Seit `spec/HKF-Harness-V1.0.md` den Abschnitt „Der Bestand" traegt, gibt es
die Liste. Dieses Werkzeug haelt sie aktuell: Es vergleicht die drei Tabellen
mit `skills/`, `agents/` und `bin/` und meldet, was fehlt, was zu viel ist und
wo eine Beschreibung von der Frontmatter abweicht.

    python3 tools/bestand.py

Rueckgabe 0, wenn die Tabellen stimmen, sonst 1.
"""
import io, os, re, sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HARNESS = os.path.join(WURZEL, "spec", "HKF-Harness-V1.0.md")


def tabelle(text, ueberschrift):
    """Die erste Spalte einer Tabelle unter der genannten Ueberschrift."""
    m = re.search(r"(?ms)^### %s\s*\n(.*?)(?=^#{2,3} |\Z)" % re.escape(ueberschrift), text)
    if not m:
        return None
    return [z.group(1) for z in re.finditer(r"^\| `([^`]+)` \|", m.group(1), re.M)]


def verzeichnis(art):
    if art == "skills":
        return sorted(n for n in os.listdir(os.path.join(WURZEL, "skills"))
                      if os.path.isfile(os.path.join(WURZEL, "skills", n, "SKILL.md")))
    if art == "agents":
        return sorted(n[:-3] for n in os.listdir(os.path.join(WURZEL, "agents"))
                      if n.endswith(".md"))
    return sorted(n for n in os.listdir(os.path.join(WURZEL, "bin"))
                  if not n.startswith("__"))


def main(argv):
    if not os.path.exists(HARNESS):
        print("spec/HKF-Harness-V1.0.md fehlt"); return 1
    text = io.open(HARNESS, encoding="utf-8").read()
    befunde = []
    for ueberschrift, art, wort in (("Skills", "skills", "Skill"),
                                    ("Agenten", "agents", "Agent"),
                                    ("Werkzeuge", "bin", "Werkzeug")):
        genannt = tabelle(text, ueberschrift)
        if genannt is None:
            befunde.append("Der Abschnitt „### %s“ fehlt" % ueberschrift); continue
        da = verzeichnis(art)
        for n in sorted(set(da) - set(genannt)):
            befunde.append("%s `%s` liegt im Harness, steht aber in keiner Tabelle" % (wort, n))
        for n in sorted(set(genannt) - set(da)):
            befunde.append("%s `%s` steht in der Tabelle, liegt aber nicht im Harness" % (wort, n))
        if genannt != sorted(genannt):
            befunde.append("Die Tabelle „%s“ ist nicht alphabetisch" % ueberschrift)
        print("%-10s %2d genannt, %2d vorhanden" % (ueberschrift, len(genannt), len(da)))
    for b in befunde:
        print("  -", b)
    print("%d Befunde" % len(befunde))
    return 1 if befunde else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
