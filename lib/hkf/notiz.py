# -*- coding: utf-8 -*-
"""Frontmatter aendern, ohne den Rest umzuschreiben.

Ein Import fasst wenige Properties an — `bundles`, die drei Zeitangaben,
`related`. Alles andere soll Zeichen fuer Zeichen so bleiben, wie es kam. Wer
eine Notiz durch einen YAML-Serialisierer schickt, bekommt sie anders
formatiert zurueck, und der Textunterschied zeigt dann Aenderungen, die keine
sind.
"""
import re

TRENNER = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)


CODE = re.compile(r"```.*?```|~~~.*?~~~|`[^`\n]*`", re.S)


def ausserhalb_code(text, fn):
    """`fn` auf alles anwenden, was nicht in Backticks steht.

    Was dort steht, ist ein Beispiel und kein Verweis. Eine Typdefinition
    zeigt Wikilinks als Muster her, und ein Clipping bringt die fremden
    Wikilinks der erfassten Seite mit — beide umzuschreiben verfaelschte sie.
    `pruefen.ohne_code` haelt es beim Pruefen ebenso.
    """
    aus, stand = [], 0
    for m in CODE.finditer(text):
        aus.append(fn(text[stand:m.start()]))
        aus.append(m.group(0))
        stand = m.end()
    aus.append(fn(text[stand:]))
    return "".join(aus)


def teilen(text):
    """(kopf, body). Ohne Frontmatter ist kopf None."""
    m = TRENNER.match(text)
    return m.groups() if m else (None, text)


def bauen(kopf, body):
    return "---\n%s\n---\n\n%s" % (kopf.strip("\n"), body.lstrip("\n"))


def hat(kopf, key):
    return re.search(r"^%s:" % re.escape(key), kopf, re.M) is not None


def entfernen(kopf, key):
    kopf = re.sub(r"^%s:\n(?:  - .*\n?)+" % re.escape(key), "", kopf, flags=re.M)
    kopf = re.sub(r"^%s:.*\n?" % re.escape(key), "", kopf, flags=re.M)
    return kopf.rstrip("\n")


def lies_liste(kopf, key):
    m = re.search(r"^%s:\n((?:  - .*\n?)+)" % re.escape(key), kopf + "\n", re.M)
    if not m:
        return []
    werte = []
    for z in m.group(1).strip("\n").splitlines():
        w = z.strip()[2:].strip()
        if len(w) > 1 and w[0] == w[-1] and w[0] in "\"'":
            w = w[1:-1]
        werte.append(w)
    return werte


def setze_skalar(kopf, key, wert):
    zeile = "%s: %s" % (key, wert)
    if hat(kopf, key):
        return re.sub(r"^%s:.*$" % re.escape(key), zeile, kopf, count=1, flags=re.M)
    return kopf.rstrip("\n") + "\n" + zeile


def setze_liste(kopf, key, werte):
    """Liste als Block. Wikilinks werden gequotet, weil `[` YAML sonst als
    Flow-Folge liest (§3.4)."""
    if not werte:
        return entfernen(kopf, key)
    zeilen = ["%s:" % key]
    for w in werte:
        zeilen.append('  - "%s"' % w if w.startswith("[[") else "  - %s" % w)
    neu = "\n".join(zeilen)
    if hat(kopf, key):
        kopf = entfernen(kopf, key)
    return kopf.rstrip("\n") + "\n" + neu


def abschnitt(body, ueberschrift):
    """(text des Abschnitts ohne Ueberschrift, oder None)."""
    m = re.search(r"^# %s\n(.*?)(?=^# |\Z)" % re.escape(ueberschrift), body, re.M | re.S)
    return m.group(1) if m else None


def ohne_abschnitt(body, ueberschrift):
    return re.sub(r"^# %s\n.*?(?=^# |\Z)" % re.escape(ueberschrift), "",
                  body, flags=re.M | re.S)


LINKWERT = re.compile(r"^\[\[([^\]|]+)(?:\|([^\]]*))?\]\]$")


def linkziel(wert):
    """Das Ziel, wenn der Wert genau ein Wikilink ist — sonst None.

    Fuer Properties, die zwei Schreibweisen zulassen: `type` traegt den
    Typnamen als Text oder einen Verweis auf eine Typseite (§3.3).
    """
    m = LINKWERT.match(str(wert if wert is not None else "").strip())
    return m.group(1) if m else None


def skalar(wert):
    """Ein Wert so, dass YAML ihn wieder als denselben Text liest.

    `version: 1.0` ist eine Zahl, `version: "1.0"` ist Text — und §4.1 meint
    Text. Wer eine Fassung ohne Anfuehrungszeichen schreibt, macht aus 1.10
    spaeter 1.1.
    """
    text = str(wert)
    try:
        import yaml
        gleich = yaml.safe_load(text) == text
    except Exception:                                  # pragma: no cover
        gleich = False
    if gleich or "\n" in text:
        return text
    return '"%s"' % text.replace('\\', '\\\\').replace('"', '\\"')
