# -*- coding: utf-8 -*-
"""Deutschsprachige Texte gegen die Schreibregeln pruefen.

Der Pruefer kam aus dem Skill `check-writing` des Henni-Harness und liegt hier,
weil er ein Werkzeug ist und kein Skill: Was mechanisch geht, macht ein Script.
`bin/hk-text` ist der Einstieg.

Zwei Regelquellen. Der Basissatz `rules/deutsch.json` liegt im Harness und gilt
fuer jede Ablage. Was **diese** Ablage fuer sich festgelegt hat, steht als
Notiz vom Typ `hint` darin (Harness §7) und wird als `json`-Block mit dem
Schluessel `writing_policy` gelesen.

Nur Standardbibliothek.
"""
import os
from pathlib import Path

from .. import ablage
from . import engine, rules

WURZEL = Path(__file__).resolve().parents[3]
BASISSATZ = WURZEL / "rules" / "deutsch.json"

# Wo eine Ablage ihre Hinweise fuehrt, wenn die Wurzeldatei nichts anderes
# sagt. Der Typ `hint` liegt nach HKF Config unter `wiki_base`.
HINWEISE = "Hints"


def sammeln(pfade):
    """Markdown-Dateien aus Dateien und Verzeichnissen, ohne Doppelte."""
    gefunden, gesehen = [], set()
    for roh in pfade:
        pfad = Path(roh)
        if not pfad.exists():
            raise OSError("%s gibt es nicht" % pfad)
        kandidaten = sorted(pfad.rglob("*.md")) if pfad.is_dir() else [pfad]
        for kandidat in kandidaten:
            aufgeloest = kandidat.resolve()
            if aufgeloest not in gesehen:
                gesehen.add(aufgeloest)
                gefunden.append(kandidat)
    return gefunden


def wurzel_von(dateien):
    """Die Ablage, in der diese Dateien liegen — sonst None.

    Gesucht wird ab der ersten Datei nach oben und ab dem Arbeitsverzeichnis.
    Findet sich keine, gilt allein der Basissatz, und der Bericht sagt es.
    """
    start = [str(dateien[0].resolve().parent)] if dateien else []
    for anfang in start + [os.getcwd()]:
        treffer = ablage.aufwaerts(anfang)
        if treffer:
            return Path(treffer)
    return None


def regelort(wurzel):
    """Das Verzeichnis mit den `hint`-Notizen dieser Ablage."""
    if wurzel is None:
        return Path(HINWEISE)
    try:
        daten, _ = _frontmatter(wurzel)
    except Exception:
        daten = {}
    eigen = str(daten.get("hints") or "").strip("/")
    if eigen:
        return wurzel / eigen
    try:
        basis = ablage.bereiche(str(wurzel)).get("wiki_base", "")
    except Exception:
        basis = ""
    return wurzel / basis / HINWEISE if basis else wurzel / HINWEISE


def _frontmatter(wurzel):
    from .. import frontmatter
    return frontmatter.lesen(ablage.wurzeldatei(str(wurzel)))


def laden(wurzel):
    """Basissatz plus die Regelsaetze der Ablage."""
    return rules.load_all(BASISSATZ, regelort(wurzel))


def pruefen(dateien, wurzel, regelsaetze):
    """[Befund] ueber alle Dateien, in der Reihenfolge der Eingabe."""
    befunde = []
    for datei in dateien:
        rel = relativ(datei, wurzel)
        text = datei.read_text(encoding="utf-8")
        aufgeloest = rules.resolve(regelsaetze, rel)
        befunde.extend(engine.check(text, aufgeloest, rel))
    return befunde


def relativ(datei, wurzel):
    if wurzel is None:
        return str(datei)
    try:
        return str(datei.resolve().relative_to(wurzel))
    except ValueError:
        return str(datei)


def fehler_darin(befunde):
    return engine.has_errors(befunde)
