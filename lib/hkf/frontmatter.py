# -*- coding: utf-8 -*-
"""Frontmatter lesen.

YAML kennt Datum und Zeitpunkt als eigene Typen. Sie kommen hier als ISO-Text
zurueck, damit das Schema sie mustern kann (Core Anhang B.4).
"""
import datetime, io, re, sys

try:
    import yaml
except ImportError:                                    # pragma: no cover
    sys.exit("PyYAML fehlt in %s.\n"
             "Einmal ./bootstrap-python.sh aufrufen — der Harness bringt "
             "sein eigenes Python mit." % sys.executable)

FM = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)


def normalisieren(wert):
    if isinstance(wert, datetime.datetime):
        return wert.strftime("%Y-%m-%dT%H:%M:%S")
    if isinstance(wert, datetime.date):
        return wert.strftime("%Y-%m-%d")
    if isinstance(wert, dict):
        return {k: normalisieren(v) for k, v in wert.items()}
    if isinstance(wert, list):
        return [normalisieren(v) for v in wert]
    return wert


def roh(pfad):
    """(frontmatter-text, body) oder (None, text), wenn kein Frontmatter da ist."""
    text = io.open(pfad, encoding="utf-8").read()
    m = FM.match(text)
    return m.groups() if m else (None, text)


class Unlesbar(Exception):
    """Das Frontmatter ist kein YAML. Traegt den Pfad und den Grund."""

    def __init__(self, pfad, grund):
        self.pfad, self.grund = pfad, grund
        Exception.__init__(self, "%s: Frontmatter ist kein YAML — %s"
                           % (pfad, grund))


def lesen(pfad):
    """(daten, body). Ohne Frontmatter ist daten ein leeres dict.

    Ist das Frontmatter kein YAML, wird `Unlesbar` geworfen — mit dem Pfad,
    damit ein Werkzeug sagen kann, welche Datei gemeint ist, statt mit einem
    Stapelabzug abzubrechen (Anhang B.4).
    """
    kopf, body = roh(pfad)
    if kopf is None:
        return {}, body
    try:
        geladen = yaml.safe_load(kopf)
    except yaml.YAMLError as e:
        # Der Wortlaut von PyYAML ist mehrzeilig und wiederholt die Zeile.
        # Gebraucht wird der Grund und wo er steht.
        grund = str(getattr(e, "problem", None) or e).split("\n")[0].strip()
        mark = getattr(e, "problem_mark", None)
        if mark is not None:
            grund += " (Zeile %d, Spalte %d)" % (mark.line + 2, mark.column + 1)
        raise Unlesbar(pfad, grund)
    daten = normalisieren(geladen or {})
    if not isinstance(daten, dict):
        raise Unlesbar(pfad, "es ist keine Abbildung")
    return daten, body
