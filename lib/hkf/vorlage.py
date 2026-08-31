# -*- coding: utf-8 -*-
"""Was ein Werkzeug neben eine Wissensbasis legt.

Die .gitignore steht hier, damit es sie genau einmal gibt. Mehr legt kein
Werkzeug daneben: Eine erzeugte Anleitung fuer Modelle gab es einmal, sie ist
in die Skills gewandert (siehe skills/).
"""
import io, os

GITIGNORE = """# Sitzungsprotokolle und Suchindex der Werkzeugumgebung
.memsearch/

# persönliches Fensterlayout von Obsidian
.obsidian/workspace.json

# macOS
.DS_Store
"""


def gitignore_schreiben(ziel):
    io.open(os.path.join(ziel, ".gitignore"), "w", encoding="utf-8").write(GITIGNORE)

