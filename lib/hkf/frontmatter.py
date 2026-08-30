# -*- coding: utf-8 -*-
"""Frontmatter lesen.

YAML kennt Datum und Zeitpunkt als eigene Typen. Sie kommen hier als ISO-Text
zurueck, damit das Schema sie mustern kann (Core Anhang B.4).
"""
import datetime, io, re, sys

try:
    import yaml
except ImportError:                                    # pragma: no cover
    sys.exit("PyYAML wird gebraucht: pip3 install pyyaml")

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


def lesen(pfad):
    """(daten, body). Ohne Frontmatter ist daten ein leeres dict."""
    kopf, body = roh(pfad)
    if kopf is None:
        return {}, body
    daten = normalisieren(yaml.safe_load(kopf) or {})
    if not isinstance(daten, dict):
        raise ValueError("%s: Frontmatter ist keine Abbildung" % pfad)
    return daten, body
