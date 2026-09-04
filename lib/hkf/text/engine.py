"""Prüfmaschine für die Textprüfung.

``segment.py`` bestimmt, welcher Text geprüft wird. ``rules.py`` bestimmt,
welche Regeln für eine Datei gelten. Dieses Modul wendet das eine auf das
andere an und liefert Befunde.

Die sechs Prüfungen teilen sich drei Verfahren:

* ``forbidden_characters`` und ``forbidden_punctuation`` suchen einzelne
  Zeichen.
* ``forbidden_phrases`` und ``structural_phrases`` suchen Wortfolgen an
  Wortgrenzen, ohne Rücksicht auf Gross- und Kleinschreibung. Sie treffen damit
  nur die exakte Wortform, nicht die flektierte.
* ``forbidden_stems`` und ``umlaut_replacements`` suchen Stämme innerhalb eines
  Wortes und melden das ganze Wort, damit die Meldung brauchbar ist. Für ein
  deutsches Adjektiv ist das die richtige Form: "entscheidende" und
  "entscheidenden" sind derselbe Verstärker wie "entscheidend".
* ``sentence_length`` zählt Wörter je Satz.

Jeder Befund nennt Datei, Zeile, Spalte, Prüfung, Schweregrad und den
Regelsatz, aus dem die Regel stammt. Die Positionen zeigen auf die
Originaldatei, weil ``segment.mask`` die Zeilenstruktur unangetastet lässt.

Nur Standardbibliothek.
"""

from __future__ import annotations

import bisect
import re
from typing import NamedTuple

from .segment import mask

# Abkuerzungen, nach denen ein Punkt keinen Satz beendet.
ABBREVIATIONS = {
    "bzw", "ca", "ggf", "evtl", "usw", "etc", "dr", "prof", "nr", "abb",
    "vgl", "ebd", "bd", "jh", "chr", "hrsg", "sog", "inkl", "max", "min",
}

WORD = re.compile(r"\w+", re.UNICODE)
# Nach dem Schlusszeichen duerfen Auszeichnung und schliessende Zeichen
# stehen. Ohne sie brach der Satz an `**So endet ein Satz.**` nicht, und
# der naechste zaehlte doppelt.
SENTENCE_END = re.compile(r"[.!?]+[*_`'\"\u201c\u201d\u00bb)\]]*(?=\s|$)")
LAST_TOKEN = re.compile(r"([\w]+)\s*$", re.UNICODE)
SKIP_LINE = re.compile(r"^\s*(#{1,6}\s|\||---\s*$|===)")
# Ein Listeneintrag ist eine eigene Einheit. Ohne diese Grenze verschmelzen
# aufeinanderfolgende Eintraege ohne Schlusspunkt zu einem einzigen Satz.
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+")


class Finding(NamedTuple):
    path: str
    line: int
    column: int
    check: str
    severity: str
    message: str
    origin: str

    def format(self) -> str:
        return (f"{self.path}:{self.line}:{self.column} [{self.severity}] "
                f"{self.check}: {self.message}  ({self.origin})")


def check(raw: str, resolved: dict, path: str = "") -> list[Finding]:
    """Prüft einen Rohtext gegen die für ihn aufgelösten Regeln."""
    text = mask(raw)
    starts = _line_starts(text)
    befunde: list[Finding] = []

    for name, regel in resolved.items():
        verfahren = VERFAHREN.get(name)
        if verfahren is None:
            continue
        for offset, meldung in verfahren(text, regel):
            zeile, spalte = _position(starts, offset)
            befunde.append(Finding(path, zeile, spalte, name,
                                   regel["severity"], meldung, regel["origin"]))

    befunde.sort(key=lambda b: (b.line, b.column, b.check))
    return befunde


def has_errors(befunde) -> bool:
    return any(b.severity == "error" for b in befunde)


def _characters(text: str, regel: dict):
    for zeichen in regel.get("characters", []):
        if not zeichen:
            continue
        start = text.find(zeichen)
        while start != -1:
            yield start, f"unzulässiges Zeichen {_zeige(zeichen)}"
            start = text.find(zeichen, start + 1)


def _phrases(text: str, regel: dict):
    for phrase in regel.get("phrases", []):
        muster = _phrase_muster(phrase)
        if muster is None:
            continue
        for treffer in muster.finditer(text):
            yield treffer.start(), f"unerwünschte Wendung {treffer.group(0)!r}"


def _stamm_treffer(text: str, regel: dict, vorlage: str, links: str):
    """Gemeinsame Mechanik der stammbasierten Pruefungen.

    Ein Stamm trifft das ganze Wort, in dem er steckt. Das ist der Grund, warum
    es diese Form neben ``_phrases`` gibt: eine Phrase matcht nur die exakte
    Wortform, und im Deutschen ist die flektierte der Normalfall.

    ``links`` entscheidet, ob vor dem Stamm noch Wortzeichen stehen duerfen. Eine
    Ersatzform steckt auch mitten im Wort, etwa "reissen" in "Preissenkungen".
    Ein Verstaerker dagegen steht am Wortanfang: "wesentlich" ist einer,
    "unwesentlich" ist ein anderes Wort, und "kriegsentscheidend" ist ein
    Fachbegriff und kein Werbesprech.
    """
    ausnahmen = {wort.lower() for wort in regel.get("exceptions", [])}
    # Zwei Staemme koennen dasselbe Wort treffen, etwa "foerder" und "aender"
    # in "Foerderlaender". Das ist ein Befund, nicht zwei.
    gesehen = set()
    for stamm in regel.get("stems", []):
        if not stamm:
            continue
        muster = re.compile(links + re.escape(stamm) + r"\w*", re.IGNORECASE)
        for treffer in muster.finditer(text):
            wort = treffer.group(0)
            if wort.lower() in ausnahmen or treffer.start() in gesehen:
                continue
            gesehen.add(treffer.start())
            yield treffer.start(), vorlage.format(wort=wort)


def _stems(text: str, regel: dict):
    yield from _stamm_treffer(
        text, regel,
        "{wort!r} nutzt eine Ersatzform statt echter Umlaute oder ß", r"\w*")


def _forbidden_stems(text: str, regel: dict):
    yield from _stamm_treffer(
        text, regel,
        "unerwünschte Wendung {wort!r}, auch flektiert unerwünscht", r"\b")


def _sentence_length(text: str, regel: dict):
    grenze = regel.get("maximum_words", 25)
    for start, satz in _sentences(text):
        anzahl = len(WORD.findall(satz))
        if anzahl > grenze:
            yield start, (f"Satz mit {anzahl} Wörtern, erlaubt sind {grenze}: "
                          f"{_kurz(satz)}")


VERFAHREN = {
    "forbidden_characters": _characters,
    "forbidden_punctuation": _characters,
    "forbidden_phrases": _phrases,
    "forbidden_stems": _forbidden_stems,
    "structural_phrases": _phrases,
    "umlaut_replacements": _stems,
    "sentence_length": _sentence_length,
}


def _phrase_muster(phrase: str):
    phrase = phrase.strip()
    if not phrase:
        return None
    kern = r"\s+".join(re.escape(teil) for teil in phrase.split())
    links = r"\b" if phrase[0].isalnum() else ""
    rechts = r"\b" if phrase[-1].isalnum() else ""
    return re.compile(links + kern + rechts, re.IGNORECASE)


def _sentences(text: str):
    """Sätze mit ihrem Startversatz, Überschriften und Tabellen ausgenommen."""
    for absatz_start, absatz in _prose_blocks(text):
        pos = 0
        for ende in SENTENCE_END.finditer(absatz):
            if not _ends_sentence(absatz, ende.start()):
                continue
            satz = absatz[pos:ende.end()]
            if satz.strip():
                yield absatz_start + pos + (len(satz) - len(satz.lstrip())), satz
            pos = ende.end()
        rest = absatz[pos:]
        if rest.strip():
            yield absatz_start + pos + (len(rest) - len(rest.lstrip())), rest


def _prose_blocks(text: str):
    """Zusammenhängende Prosazeilen mit ihrem Versatz in der Datei."""
    offset = 0
    block_start = None
    stuecke: list[str] = []
    for zeile in text.split("\n"):
        if zeile.strip() and not SKIP_LINE.match(zeile):
            if block_start is not None and LIST_ITEM.match(zeile):
                yield block_start, "\n".join(stuecke)
                block_start = None
            if block_start is None:
                block_start = offset
                stuecke = []
            stuecke.append(zeile)
        else:
            if block_start is not None:
                yield block_start, "\n".join(stuecke)
                block_start = None
        offset += len(zeile) + 1
    if block_start is not None:
        yield block_start, "\n".join(stuecke)


def _ends_sentence(absatz: str, punkt: int) -> bool:
    davor = LAST_TOKEN.search(absatz[:punkt])
    if davor is None:
        return True
    token = davor.group(1)
    if len(token) == 1 and token.isalpha():
        return False
    if token.lower() in ABBREVIATIONS:
        return False
    # Ordnungszahl wie "am 1. Juli", aber keine Jahreszahl wie "1911."
    if token.isdigit() and len(token) <= 2:
        return False
    return True


def _line_starts(text: str) -> list[int]:
    starts = [0]
    for treffer in re.finditer(r"\n", text):
        starts.append(treffer.end())
    return starts


def _position(starts: list[int], offset: int) -> tuple[int, int]:
    index = bisect.bisect_right(starts, offset) - 1
    return index + 1, offset - starts[index] + 1


def _zeige(zeichen: str) -> str:
    sichtbar = {"—": "Em-Dash", "–": "En-Dash", "­": "Soft-Hyphen",
                "​": "Zero-Width-Space", "﻿": "BOM"}
    return sichtbar.get(zeichen, repr(zeichen))


def _kurz(satz: str, laenge: int = 60) -> str:
    text = " ".join(satz.split())
    return text if len(text) <= laenge else text[:laenge] + " ..."
