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

# Die vier Bereiche einer Ablage (§3.1) mit ihren Vorgaben. Die Zahlenpraefixe
# ordnen sie in der Anzeige jedes Dateibrowsers.
BEREICHE = ("wiki_base", "source_base", "media_base", "config_base")
VORGABEN = {"wiki_base": "40-Wiki", "source_base": "50-Sources",
            "media_base": "80-Media", "config_base": "90-System"}


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


def finde_ablage(arg=None):
    """(pfad, art) — art ist "hkb" oder "bundle" (§3.1).

    `hk-lint` gilt fuer beide (§6.3). Ein Bundle hat keine Typverzeichnisse und
    keinen Ablagepfad; was dort sonst noch anders ist, entscheidet die Art.
    """
    pfad = arg or os.environ.get("HKB_PATH") or VORGABE
    pfad = os.path.abspath(os.path.expanduser(pfad))
    if os.path.isfile(os.path.join(pfad, "hkb.md")):
        return finde(pfad), "hkb"
    if os.path.isfile(os.path.join(pfad, "hbundle.md")):
        return pfad, "bundle"
    raise KeineAblage("%s: weder hkb.md noch hbundle.md — dort liegt keine "
                      "Ablage (§3.1).\nDer Pfad kommt aus %s."
                      % (pfad, herkunft(arg)))


def bereiche(pfad):
    """{name: relativer Pfad} der vier Bereiche (§3.1).

    Fehlt einer, gilt die Vorgabe. Ein ausdruecklich leerer Wert bleibt leer —
    dann faellt der Bereich mit der Wurzel zusammen, was erlaubt, aber nicht
    die Vorgabe ist.
    """
    daten, _ = frontmatter.lesen(os.path.join(pfad, "hkb.md"))
    aus = {}
    for k in BEREICHE:
        wert = daten.get(k, VORGABEN[k])
        aus[k] = str("" if wert is None else wert).strip("/")
    return aus


def basis(pfad):
    """Bereich des Inhalts (§3.2), absolut. Frueher `base`."""
    return os.path.join(pfad, bereiche(pfad)["wiki_base"])


def ablagepfad(pfad):
    """Pfad von der Vault-Wurzel zur Ablage (§3.1), ohne fuehrenden Strich.

    Die Vault-Wurzel ist das naechste Verzeichnis auf dem Weg nach oben, in dem
    `.obsidian` liegt. Liegt die HKB selbst dort, ist der Ablagepfad leer. Er
    steht in jedem qualifizierten Wikilink vor der Notiz-ID (§3.6).
    """
    pfad = os.path.abspath(pfad)
    p = pfad
    while True:
        if os.path.isdir(os.path.join(p, ".obsidian")):
            rel = os.path.relpath(pfad, p)
            return "" if rel == "." else rel.replace(os.sep, "/")
        eltern = os.path.dirname(p)
        if eltern == p:
            return ""
        p = eltern


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
