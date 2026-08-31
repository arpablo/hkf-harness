# -*- coding: utf-8 -*-
"""Welche Fassungen dieser Harness liest — Core §8.

Minor-Fassungen ergaenzen Regeln, ohne Bestehendes ungueltig zu machen. Ein
Harness liest darum jede Fassung mit derselben Major-Nummer, deren Minor nicht
groesser ist als die eigene: Was 1.0 schrieb, versteht 1.2. Umgekehrt gilt es
nicht — was 1.2 schrieb, kann Regeln benutzen, die 1.0 nicht kennt.

Fuer den unbekannten Fall ist §8 ausdruecklich: „Erkennt eine HKB die
`hkf`-Version eines Bundles nicht, liest sie die Dateien, leitet aber keine
Identitaeten ab und importiert nicht."
"""
import re

from . import CORE

GLEICH, AELTER, NEUER, FREMD, UNLESBAR = (
    "gleich", "älter", "neuer", "fremd", "unlesbar")


def teilen(wert):
    m = re.match(r"^\s*(\d+)\.(\d+)\s*$", str(wert or ""))
    return (int(m.group(1)), int(m.group(2))) if m else None


def lage(wert, unsere=None):
    """Wie sich `wert` zur Fassung dieses Harness verhaelt."""
    ihre = teilen(wert)
    meine = teilen(unsere or CORE)
    if ihre is None:
        return UNLESBAR
    if ihre[0] != meine[0]:
        return FREMD
    if ihre[1] < meine[1]:
        return AELTER
    if ihre[1] > meine[1]:
        return NEUER
    return GLEICH


def lesbar(wert, unsere=None):
    return lage(wert, unsere) in (GLEICH, AELTER)


def satz(wert, unsere=None):
    """Ein Halbsatz fuer den Bericht, wenn es nicht passt."""
    l = lage(wert, unsere)
    unsere = unsere or CORE
    if l == NEUER:
        return ("Fassung %s ist neuer als dieser Harness (Core %s)"
                % (wert, unsere))
    if l == FREMD:
        return ("Fassung %s gehört zu einer anderen Major-Fassung als Core %s"
                % (wert, unsere))
    if l == UNLESBAR:
        return "Fassung %r ist keine Angabe der Form <major>.<minor>" % (wert,)
    return ""
