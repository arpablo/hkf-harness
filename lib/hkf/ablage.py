# -*- coding: utf-8 -*-
"""Die Wissensbasis finden und aufschlagen.

Der Harness kennt keinen festen Pfad. Er nimmt, was im Aufruf steht, sonst
HKB_PATH, sonst die Vorgabe — und prueft, ob dort ueberhaupt eine Ablage
liegt. Raten waere die eine Sache, die er hier nicht darf: Ein Werkzeug, das
sein Ziel errraet, schreibt irgendwann in ein fremdes Verzeichnis.
"""
import json
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
# `Hints` haelt, was diese eine Ablage fuer sich festgelegt hat (Harness §7).
HINWEISE = "Hints"
TYPEDEFS, PROPTYPES, TYPES = "Typedefs", "Proptypes", "Types"
KONFIGVERZEICHNISSE = (TYPEDEFS, PROPTYPES, TYPES)

# Die drei Wurzeldateien (§3.1). Eine Wissensbasis traegt `hkb.md` mit der
# Property `hkf`, eine Lieferung `hbundle.md`. `vault.md` ist der dritte Fall:
# ein gewoehnlicher Obsidian-Vault, den der Harness bedient, ohne dass dort das
# Format gilt. Er bekommt die Schreibregeln, die Rollen und die Suche, aber
# keine Operation, die Typen und qualifizierte Verweise voraussetzt.
WURZELDATEIEN = (("hkb.md", "hkb"), ("hbundle.md", "bundle"),
                 ("vault.md", "vault"))
ARTNAME = {"hkb": "Wissensbasis", "bundle": "Lieferung", "vault": "Vault"}

# Wo die gemerkte Wahl liegt. Sie steht auf der Platte und nicht in der
# Umgebung, weil ein `export` einen Werkzeugaufruf nicht ueberlebt: Zwischen
# zwei Aufrufen bleibt das Arbeitsverzeichnis, sonst nichts. Geschluesselt wird
# nach Arbeitsverzeichnis, damit zwei Sitzungen an verschiedenen Ablagen sich
# nicht gegenseitig umstellen.
WAHL = os.environ.get("HKF_WAHL") or os.path.join(
    os.path.expanduser("~"), ".cache", "hkf-harness", "ablagen.json")


class KeineAblage(Exception):
    pass


def art_von(pfad):
    """"hkb", "bundle" oder "vault" — None, wenn dort keine Ablage liegt."""
    for datei, art in WURZELDATEIEN:
        if os.path.isfile(os.path.join(pfad, datei)):
            return art
    return None


def wurzeldatei(pfad):
    """Der Pfad der Wurzeldatei — `hkb.md`, `hbundle.md` oder `vault.md`."""
    for datei, _art in WURZELDATEIEN:
        voll = os.path.join(pfad, datei)
        if os.path.isfile(voll):
            return voll
    raise KeineAblage("%s: keine Wurzeldatei." % pfad)


def name_von(pfad):
    """Der Name aus der Wurzeldatei, sonst der Verzeichnisname."""
    try:
        daten, _kopf = frontmatter.lesen(wurzeldatei(pfad))
        wert = str(daten.get("name") or "").strip()
    except Exception:
        wert = ""
    return wert or os.path.basename(pfad.rstrip("/")) or pfad


def _stand():
    try:
        with open(WAHL, encoding="utf-8") as f:
            daten = json.load(f)
    except (OSError, ValueError):
        return {}
    return daten if isinstance(daten, dict) else {}


def _sichern(daten):
    ordner = os.path.dirname(WAHL)
    if ordner and not os.path.isdir(ordner):
        os.makedirs(ordner)
    with open(WAHL, "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def gewaehlt(wo=None):
    """Der Pfad, der fuer dieses Arbeitsverzeichnis gemerkt ist."""
    wo = os.path.abspath(wo or os.getcwd())
    pfad = _stand().get("wahl", {}).get(wo)
    return pfad if pfad and art_von(pfad) else None


def waehlen(pfad, wo=None):
    """Die Wahl merken und die Ablage ins Verzeichnis der bekannten eintragen."""
    pfad = os.path.abspath(os.path.expanduser(pfad))
    if not art_von(pfad):
        raise KeineAblage("%s: weder hkb.md noch hbundle.md noch vault.md — "
                          "dort liegt keine Ablage." % pfad)
    daten = _stand()
    daten.setdefault("wahl", {})[os.path.abspath(wo or os.getcwd())] = pfad
    if pfad not in daten.setdefault("bekannt", []):
        daten["bekannt"].append(pfad)
        daten["bekannt"].sort()
    _sichern(daten)
    return pfad


def vergessen(wo=None):
    """Die Wahl fuer dieses Arbeitsverzeichnis zuruecknehmen."""
    daten = _stand()
    weg = daten.get("wahl", {}).pop(os.path.abspath(wo or os.getcwd()), None)
    if weg is not None:
        _sichern(daten)
    return weg


def bekannt():
    """[(pfad, name, art)] der Ablagen, die schon einmal benutzt wurden."""
    aus = []
    for pfad in _stand().get("bekannt", []):
        art = art_von(pfad)
        if art:
            aus.append((pfad, name_von(pfad), art))
    return aus


def daneben(wo=None):
    """[(pfad, name, art)] der Ablagen unmittelbar unter einem Verzeichnis.

    Der Regelfall ist ein Arbeitsverzeichnis, unter dem mehrere Ablagen
    nebeneinander liegen. Dann ist keine davon die eine, und geraten wird
    nicht — aber aufzaehlen laesst sich, was zur Wahl steht.
    """
    wo = os.path.abspath(wo or os.getcwd())
    aus = []
    try:
        eintraege = sorted(os.listdir(wo))
    except OSError:
        return aus
    for eintrag in eintraege:
        voll = os.path.join(wo, eintrag)
        art = art_von(voll) if os.path.isdir(voll) else None
        if art:
            aus.append((voll, name_von(voll), art))
    return aus


def aufwaerts(start=None):
    """Die naechste Ablage vom Verzeichnis aus nach oben, sonst None."""
    hier = os.path.abspath(start or os.getcwd())
    while True:
        if art_von(hier):
            return hier
        oben = os.path.dirname(hier)
        if oben == hier:
            return None
        hier = oben


def aufloesen(arg=None, wo=None):
    """(pfad, herkunft) — die fuenf Stufen in ihrer Reihenfolge.

    Aufruf, HKB_PATH, die gemerkte Wahl, eine Aufwaertssuche ab dem
    Arbeitsverzeichnis, die Vorgabe. Die Aufwaertssuche steht vor der Vorgabe
    und hinter der Wahl: Wer ausdruecklich gewaehlt hat, meint das auch, wenn
    er gerade in einer anderen Ablage steht.
    """
    if arg:
        return os.path.abspath(os.path.expanduser(arg)), "dem Aufruf"
    aus_umgebung = os.environ.get("HKB_PATH")
    if aus_umgebung:
        return os.path.abspath(os.path.expanduser(aus_umgebung)), "HKB_PATH"
    wahl = gewaehlt(wo)
    if wahl:
        return wahl, "der gemerkten Wahl (hk-ablage)"
    oben = aufwaerts(wo)
    if oben:
        return oben, "dem Arbeitsverzeichnis"
    return os.path.abspath(os.path.expanduser(VORGABE)), "der Vorgabe %s" % VORGABE


def herkunft(arg=None):
    return aufloesen(arg)[1]


def finde(arg=None):
    """Absoluter Pfad zur Wissensbasis."""
    pfad, woher = aufloesen(arg)
    wurzel = os.path.join(pfad, "hkb.md")
    if not os.path.isfile(wurzel):
        raise KeineAblage("%s: keine hkb.md — dort liegt keine Wissensbasis.\n"
                          "Der Pfad kommt aus %s." % (pfad, woher))
    daten, _ = frontmatter.lesen(wurzel)
    if "hkf" not in daten:
        raise KeineAblage("%s: hkb.md traegt kein `hkf` — das ist keine "
                          "Wurzeldatei (§3.1)." % pfad)
    return pfad


def finde_ablage(arg=None, arten=("hkb", "bundle")):
    """(pfad, art) — art ist "hkb", "bundle" oder "vault" (§3.1).

    `hk-lint` gilt fuer die ersten beiden (§6.3). Ein Bundle hat keine
    Typverzeichnisse und keinen Ablagepfad; was dort sonst noch anders ist,
    entscheidet die Art. Ein `vault` ist kein HKF-Gegenstand und wird nur
    zurueckgegeben, wer ausdruecklich danach fragt.
    """
    pfad, woher = aufloesen(arg)
    art = art_von(pfad)
    if art == "hkb":
        finde(pfad)
    if art in arten:
        return pfad, art
    if art:
        raise KeineAblage("%s: dort liegt %s, gebraucht wird %s.\nDer Pfad "
                          "kommt aus %s."
                          % (pfad, ARTNAME[art],
                             " oder ".join(ARTNAME[a] for a in arten), woher))
    raise KeineAblage("%s: keine Wurzeldatei — dort liegt keine Ablage "
                      "(§3.1).\nDer Pfad kommt aus %s." % (pfad, woher))


def hinweise(pfad):
    """Das Verzeichnis mit den `hint`-Notizen einer Ablage.

    Was **diese** Ablage fuer sich festgelegt hat, steht als gewoehnliche Notiz
    darin (Harness §7). Der Ort ist `Hints/` unter `wiki_base`, oder was die
    Wurzeldatei unter `hints` nennt.
    """
    try:
        daten, _ = frontmatter.lesen(wurzeldatei(pfad))
    except Exception:
        daten = {}
    eigen = str(daten.get("hints") or "").strip("/")
    if eigen:
        return os.path.join(pfad, eigen)
    try:
        basis = bereiche(pfad).get("wiki_base", "")
    except Exception:
        basis = ""
    return os.path.join(pfad, basis, HINWEISE) if basis \
        else os.path.join(pfad, HINWEISE)


def bereiche(pfad):
    """{name: relativer Pfad} der vier Bereiche (§3.1).

    Fehlt einer, gilt die Vorgabe. Ein ausdruecklich leerer Wert bleibt leer —
    dann faellt der Bereich mit der Wurzel zusammen, was erlaubt, aber nicht
    die Vorgabe ist.
    """
    daten, _ = frontmatter.lesen(wurzeldatei(pfad))
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
