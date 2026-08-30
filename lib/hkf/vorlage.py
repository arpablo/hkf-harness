# -*- coding: utf-8 -*-
"""Was ein Werkzeug neben eine Wissensbasis legt.

Die AGENTS.md und die .gitignore stehen hier, damit es sie genau einmal gibt.
Beide gehoeren dem Werkzeug und nicht der Ablage: Die eine wird erzeugt, die
andere haelt sie samt CLAUDE.md aus der Versionierung.
"""
import io, os

from . import CORE, TEMPLATES, ablage

GITIGNORE = """# Sitzungsprotokolle und Suchindex der Werkzeugumgebung
.memsearch/

# Anleitungen, die ein Werkzeug erzeugt — sie gehören nicht zur Ablage
AGENTS.md
CLAUDE.md

# persönliches Fensterlayout von Obsidian
.obsidian/workspace.json

# macOS
.DS_Store
"""


def gitignore_schreiben(ziel):
    io.open(os.path.join(ziel, ".gitignore"), "w", encoding="utf-8").write(GITIGNORE)


def agents_schreiben(ziel, name, tz, zeilen=None):
    """Regeln woertlich aus der Vorlage, Kopf und Typtabelle aus der Ablage.

    `zeilen` sind fertige Tabellenzeilen; ohne sie kommen sie aus `hkb.md`.
    """
    src = io.open(os.path.join(TEMPLATES, "AGENTS.md"), encoding="utf-8").read()
    regeln = src[src.index("## Sieben Regeln"):src.index("## Typen")]
    schluss = src[src.index("Mediendateien"):]
    kopf = ("# %s\n\nEine Wissensbasis im Format **HKF Core %s**. Einstieg "
            "ist `hkb.md`.\nZeiten gelten in `%s`.\n\n" % (name, CORE, tz))
    if zeilen is None:
        zeilen = ["| %s |" % " | ".join(r) for r in ablage.typen(ziel)]
    tabelle = ("## Typen dieser Wissensbasis\n\n| Typ | Verzeichnis | Zweck |\n"
               "|---|---|---|\n" + "\n".join(zeilen) + "\n\n")
    io.open(os.path.join(ziel, "AGENTS.md"), "w", encoding="utf-8").write(
        kopf + regeln + tabelle + schluss)
