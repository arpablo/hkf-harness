#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Haelt einen Schreibvorgang an, der gegen die harten Schreibregeln verstoesst.

Geblockt wird nur bei Severity `error`, also bei unzulaessigen Zeichen,
verbotener Interpunktion und Umlaut-Ersatzformen. Warnungen zu Satzlaenge und
Wortwahl sind Hinweise und halten niemanden auf.

Geprueft wird nur, was in einer Ablage liegt. Ausserhalb tut der Hook nichts:
Der Harness bringt seine Regeln in eine Wissensbasis mit, er erklaert nicht die
ganze Platte zu seinem Gegenstand.

**Kann der Pruefer nicht laufen, laesst der Hook durch und sagt warum.** Ein
Pruefer, der nicht laeuft, ist kein Regelverstoss.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import gemeinsam   # noqa: E402
from hkf import ablage, text as textmodul   # noqa: E402

HOECHSTENS = 20


def main():
    e = gemeinsam.ereignis()
    wo = gemeinsam.arbeitsverzeichnis(e)
    pfad, _woher = ablage.aufloesen(wo=wo)
    if not ablage.art_von(pfad):
        return 0

    dateien = [d for d in gemeinsam.geaendert(e, pfad)
               if d.lower().endswith(".md") and os.path.isfile(d)]
    if not dateien:
        return 0

    from pathlib import Path
    # realpath, damit der Befund einen Pfad relativ zur Ablage nennt. Auf macOS
    # ist `/tmp` ein Zeiger auf `/private/tmp`, und ohne das steht in jedem
    # Befund der absolute Pfad.
    wurzel = Path(os.path.realpath(pfad))
    try:
        regelsaetze = textmodul.laden(wurzel)
        befunde = [b for b in textmodul.pruefen([Path(d) for d in dateien],
                                                wurzel, regelsaetze)
                   if b.severity == "error"]
    except Exception as fehler:
        sys.stderr.write("Hinweis: Schreibregeln nicht geprüft, %s\n" % fehler)
        return 0

    if not befunde:
        return 0
    zeilen = ["  %s:%s:%s %s: %s" % (b.path, b.line, b.column, b.check, b.message)
              for b in befunde[:HOECHSTENS]]
    if len(befunde) > HOECHSTENS:
        zeilen.append("  und %d weitere" % (len(befunde) - HOECHSTENS))
    return gemeinsam.blockieren(
        "VERSTOSS gegen die harten Schreibregeln:\n" + "\n".join(zeilen)
        + "\n\nKorrigieren, dann erneut schreiben. `hk-text <datei>` zeigt alles.")


if __name__ == "__main__":
    sys.exit(main())
