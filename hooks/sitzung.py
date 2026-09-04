#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sagt zu Beginn einer Sitzung, wo gearbeitet wird und welche Regeln gelten.

Bis hierher gab es dafuer einen Generator, der aus einem Manifest eine
`CLAUDE.md` in den Vault schrieb, dazu Agentenfassungen, Hook-Eintraege und
Skill-Zeiger. Das waren acht erzeugte Artefakte, die auseinanderlaufen konnten,
in einer Ablage, die nach §4 keine Werkzeugdatei tragen soll.

Ein Hook braucht davon nichts. **In der Ablage entsteht nichts.** Ein fremder
Vault bleibt unangetastet.

Zusammengesetzt wird in `hkf.kontext`, nicht hier. Ein Subagent laeuft in
seinem eigenen Kontext und sieht nicht, was die Sitzung bekommen hat; er holt
sich denselben Text ueber `hk-kontext`.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import gemeinsam   # noqa: E402
from hkf import ablage, kontext   # noqa: E402


def main():
    e = gemeinsam.ereignis()
    wo = gemeinsam.arbeitsverzeichnis(e)
    text, pfad, art = kontext.zusammensetzen(wo)
    if not text:
        # Hier gibt es nichts zu sagen. Ein Hook, der in jedem fremden
        # Projekt etwas einspielt, kostet dort in jeder Sitzung.
        return 0
    kurz = ("%s (%s)" % (ablage.name_von(pfad), ablage.ARTNAME[art])
            if art else "keine Ablage gewählt")
    return gemeinsam.kontext(text, "HKF: " + kurz)


if __name__ == "__main__":
    sys.exit(main())
