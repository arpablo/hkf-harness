# -*- coding: utf-8 -*-
"""Die Wissensbasis finden und aufschlagen.

Der Harness kennt keinen festen Pfad. Er nimmt, was im Aufruf steht, sonst
HKB_PATH, sonst die Vorgabe — und prueft, ob dort ueberhaupt eine Ablage
liegt. Raten waere die eine Sache, die er hier nicht darf: Ein Werkzeug, das
sein Ziel errraet, schreibt irgendwann in ein fremdes Verzeichnis.
"""
import os

from . import frontmatter

VORGABE = "~/hkb"


class KeineAblage(Exception):
    pass


def herkunft(arg=None):
    if arg:
        return "dem Aufruf"
    if os.environ.get("HKB_PATH"):
        return "HKB_PATH"
    return "der Vorgabe %s" % VORGABE


def finde(arg=None):
    """Absoluter Pfad zur Wissensbasis. Reihenfolge: Aufruf, HKB_PATH, Vorgabe."""
    pfad = arg or os.environ.get("HKB_PATH") or VORGABE
    pfad = os.path.abspath(os.path.expanduser(pfad))
    wurzel = os.path.join(pfad, "hkb.md")
    if not os.path.isfile(wurzel):
        raise KeineAblage("%s: keine hkb.md — dort liegt keine Wissensbasis.\n"
                          "Der Pfad kommt aus %s." % (pfad, herkunft(arg)))
    daten, _ = frontmatter.lesen(wurzel)
    if "hkf" not in daten:
        raise KeineAblage("%s: hkb.md traegt kein `hkf` — das ist keine "
                          "Wurzeldatei (§3.1)." % pfad)
    return pfad


def basis(pfad):
    """Basispfad der Typverzeichnisse (§3.1), absolut."""
    daten, _ = frontmatter.lesen(os.path.join(pfad, "hkb.md"))
    return os.path.join(pfad, str(daten.get("base") or "").strip("/"))


def typen(pfad):
    """Die Typtabelle aus dem Abschnitt `# Typen` der Wurzeldatei."""
    _, body = frontmatter.lesen(os.path.join(pfad, "hkb.md"))
    if "\n# Typen\n" not in "\n" + body:
        return []
    rows = []
    for zeile in body.split("# Typen", 1)[1].splitlines():
        if not zeile.startswith("|"):
            if rows:
                break
            continue
        spalten = [s.strip() for s in zeile.strip("|").split("|")]
        if spalten[0] in ("Typ", "") or set(spalten[0]) <= set("- "):
            continue
        rows.append(spalten)
    return rows


def dateien(wurzel):
    """Alle Markdown-Dateien unterhalb von wurzel, ohne Punktverzeichnisse."""
    for r, dirs, fs in os.walk(wurzel):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in sorted(fs):
            if f.endswith(".md"):
                yield os.path.join(r, f)
