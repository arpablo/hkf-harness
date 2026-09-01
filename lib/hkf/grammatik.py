# -*- coding: utf-8 -*-
"""Wikilinks und Typangaben gegen Anhang B von HKF Core pruefen.

Die Ausdruecke unten sind eine woertliche Uebersetzung der ABNF; steht dort
etwas anderes, gilt die ABNF, und dieses Modul ist falsch.
"""
import re

from . import frontmatter

# ── B.1 Gemeinsame Bausteine ────────────────────────────────────────────
KEBAB   = r"[a-z][a-z0-9-]*"
SEGZ    = r"[^\x00-\x1f/\]|]"          # seg-zeichen
SEGMENT = SEGZ + "+"
PFAD    = SEGMENT + r"(?:/" + SEGMENT + r")*"
ALIASZ  = r"[^\x00-\x1f\]|]"           # alias-zeichen

# ── B.2 Wikilinks ───────────────────────────────────────────────────────
WIKILINK = re.compile(r"\A\[\[(" + PFAD + r")(?:\|(" + ALIASZ + r"+))?\]\]\Z")
ZELLE    = re.compile(r"\A\[\[(" + PFAD + r")(?:\\\|(" + ALIASZ + r"+))?\]\]\Z")
ROH      = re.compile(r"!?\[\[[^\n]*?\]\]")

# ── B.3 Typangaben ──────────────────────────────────────────────────────
WERTFORM = r"text|list|number|checkbox|date|datetime"
MEDIENART = r"image|video|audio|document|clipping"
TYPANGABE = re.compile(
    r"\A(?:"
    + r"(?:" + WERTFORM + r")"
    + r"|hkf-link(?:-list)?(?::" + KEBAB + r"(?:," + KEBAB + r")*)?"
    + r"|hkf-file(?:-list)?(?::(?:" + MEDIENART + r")(?:,(?:" + MEDIENART + r"))*)?"
    + r"|hkf-link-or-text(?:-list)?(?::" + KEBAB + r"(?:," + KEBAB + r")*)?"
    + r"|" + KEBAB
    + r")\Z")


def pruefe_datei(pfad, befunde, name=None):
    name = name or pfad
    kopf, body = frontmatter.roh(pfad)
    if kopf is None:
        return
    ohne_code = re.sub(r"```.*?```", "", body, flags=re.S)
    ohne_code = re.sub(r"`[^`\n]*`", "", ohne_code)

    # Wikilinks: in einer Tabellenzeile gilt die Zellen-Regel
    for quelle, zeilen in (("frontmatter", kopf.splitlines()),
                           ("body", ohne_code.splitlines())):
        for nr, zeile in enumerate(zeilen, 1):
            in_tabelle = quelle == "body" and zeile.lstrip().startswith("|")
            regel = ZELLE if in_tabelle else WIKILINK
            for treffer in ROH.finditer(zeile):
                roh = treffer.group(0).lstrip("!")
                if not regel.match(roh):
                    befunde.append("%s: %s Zeile %d: %s entspricht B.2 nicht%s"
                                   % (name, quelle, nr, roh[:60],
                                      " (Tabellenzelle)" if in_tabelle else ""))

    # Typangaben: zweite Spalte des Abschnitts `# Properties`
    if "\n# Properties\n" in body:
        gesehen = False
        for zeile in body.split("\n# Properties\n", 1)[1].splitlines():
            if not zeile.startswith("|"):
                if gesehen and zeile.strip():
                    break          # Tabelle zu Ende
                continue
            gesehen = True
            spalten = [s.strip() for s in zeile.strip("|").split("|")]
            if len(spalten) < 2 or spalten[0] in ("Property", "") or set(spalten[0]) <= set("- "):
                continue
            for angabe in spalten[1].split(" / "):
                if not TYPANGABE.match(angabe.strip()):
                    befunde.append("%s: Typangabe %r entspricht B.3 nicht"
                                   % (name, angabe.strip()))
