# -*- coding: utf-8 -*-
"""Die Wissensbasis finden und aufschlagen.

Der Harness kennt keinen festen Pfad. Er nimmt, was im Aufruf steht, sonst
HKB_PATH, sonst die Vorgabe — und prueft, ob dort ueberhaupt eine Ablage
liegt. Raten waere die eine Sache, die er hier nicht darf: Ein Werkzeug, das
sein Ziel errraet, schreibt irgendwann in ein fremdes Verzeichnis.
"""
import os

from . import frontmatter, notiz

VORGABE = "~/hkb"

# Die vier Bereiche einer Ablage (§3.1) mit ihren Vorgaben. Die Zahlenpraefixe
# ordnen sie in der Anzeige jedes Dateibrowsers.
BEREICHE = ("wiki_base", "source_base", "media_base", "config_base")
VORGABEN = {"wiki_base": "40-Wiki", "source_base": "50-Sources",
            "media_base": "80-Media", "config_base": "90-System"}

# Unter `config_base` liegen genau zwei Typen: `typedef` und `proptype`
# (§3.2). Ihre Verzeichnisse stehen hier als Namen und nicht als `dir` der
# Typdefinition — wer sie dort umbenennt, verlegt gerade die Datei, in der es
# steht, und keines der Werkzeuge faende sie danach wieder. `Types` haelt die
# Typseiten (§3.3); es ist freigestellt und enthaelt keine Notizen.
TYPEDEFS, PROPTYPES, TYPES = "Typedefs", "Proptypes", "Types"
KONFIGVERZEICHNISSE = (TYPEDEFS, PROPTYPES, TYPES)


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


def bereich_von(bereiche, rel):
    """(Bereich, Pfad ab dem Bereich) fuer eine Datei unter der Wurzel.

    Liegt sie unter keinem der vier, kommt (None, rel) zurueck. Bereiche
    liegen nicht ineinander (§3.1); der laengste Treffer gewinnt trotzdem,
    damit ein leerer Bereich, der mit der Wurzel zusammenfaellt, keinen
    benannten verdeckt.
    """
    rel = rel.replace(os.sep, "/")
    treffer = None
    for k in BEREICHE:
        b = bereiche.get(k) or ""
        if not b or not (rel == b or rel.startswith(b + "/")):
            continue
        if treffer is None or len(b) > len(bereiche[treffer]):
            treffer = k
    if treffer is None:
        return None, rel
    b = bereiche[treffer]
    return treffer, rel[len(b) + 1:] if rel != b else ""


def konfigfremd(bereich, rel):
    """Liegt unter `config_base`, aber in keinem seiner Typverzeichnisse.

    Zur Ablage gehoeren die Wurzeldatei und die vier Bereiche (§3.2), und
    unter `config_base` liegen genau zwei Typen. Ein anderes Verzeichnis dort
    gehoert nicht dazu und wird weder geprueft noch verwaltet — ein
    Vorlagenordner etwa, dessen Dateien `type` tragen, weil sie den Typ
    nennen, den sie anlegen sollen, ohne darum Notizen zu sein.
    """
    return (bereich == "config_base"
            and rel.replace(os.sep, "/").partition("/")[0]
            not in KONFIGVERZEICHNISSE)


def typseiten(konfig):
    """{"Types/<datei>": <typname>} — die Typseiten unter einem `config_base`.

    Eine Typseite bindet sich ueber `definition` an genau eine Typdefinition;
    deren Dateiname ist der Typname (§3.3). Wer keine Typseiten fuehrt,
    bekommt ein leeres Verzeichnis zurueck und merkt von der Linkform nichts.

    `hk-lint` liest sie mit allem anderen ueber `Bestand`; das hier ist fuer
    Import und Export, die ohne einen solchen auskommen.
    """
    verz = os.path.join(konfig, TYPES)
    aus = {}
    if not os.path.isdir(verz):
        return aus
    for p in dateien(verz):
        try:
            daten, _ = frontmatter.lesen(p)
        except frontmatter.Unlesbar:
            continue
        ziel = notiz.linkziel((daten or {}).get("definition"))
        teile = (ziel or "").split("/")
        if len(teile) >= 2 and teile[-2] == TYPEDEFS:
            aus["%s/%s" % (TYPES, os.path.basename(p)[:-3])] = teile[-1]
    return aus


def dateien(wurzel):
    """Alle Markdown-Dateien unterhalb von wurzel, ohne Punktverzeichnisse."""
    for r, dirs, fs in os.walk(wurzel):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in sorted(fs):
            if f.endswith(".md"):
                yield os.path.join(r, f)
