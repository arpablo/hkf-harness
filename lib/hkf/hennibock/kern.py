#!/usr/bin/env python3
"""hennibock_publish.py - erzeugt aus einer Vault-Notiz ein HenniBock-Bundle und
uebertraegt es per POST /import an eine HenniBock-Instanz.

Aufruf:
    python3 hennibock_publish.py analyze "<Notiz>" [--alts alts.json]
    python3 hennibock_publish.py write-alts "<Notiz>" --alts alts.json
    python3 hennibock_publish.py build "<Notiz>" [--alts alts.json] [--send]
    python3 hennibock_publish.py attached "<Notiz>"

analyze liest die Notiz, stellt die Identitaet her (schreibt hennibock_ref und
hennibock_published beim ersten Publish zurueck) und gibt als JSON die Metadaten
plus je Bild den englischen ai-image-Prompt, den wirksamen Alt-Text (alt_de) und
dessen Herkunft (alt_source) aus.

Der Alt-Text hat zwei Quellen, in dieser Reihenfolge:

1. Ein Wert aus alts.json ueberschreibt alles. Das ist die bewusste Abweichung
   fuer genau diesen Publish, und sie wird nie in die Notiz zurueckgeschrieben.
2. Sonst gilt das alt-Feld des ai-image-Callouts. Es steht im Vault und ist die
   dauerhafte Quelle.

Fehlt beides, meldet analyze den Slug unter missing_alt. Der Agent schreibt dann
allein fuer diese Bilder einen deutschen Alt-Text und uebergibt ihn an write-alts,
das ihn in den Callout schreibt. Danach findet build ihn dort, und der naechste
Publish derselben Notiz erzeugt ihn nicht noch einmal.

write-alts ist bewusst ein eigenes Kommando. Als Seiteneffekt von build waere die
Trennung zwischen Override und dauerhafter Quelle wieder aufgehoben.

build saeubert den Body (entfernt ai-image-Callouts und den Verweisapparat,
loest Wikilinks auf, schreibt Bild-Einbettungen auf image/<slug> um), baut die
HenniBock-Frontmatter, die Medien-Sidecars und das ZIP-Bundle. Mit --send geht
das Bundle erst an $HENNIBOCK_URL/import/validate und dann an /import, mit\nBearer $HENNIBOCK_IMPORT_TOKEN. Beide
Variablen sind Pflicht, es gibt keinen Default fuer das Ziel.

Nach einem gelungenen Import prueft build, ob der Beitrag in den Publikationen
haengt, die ihn im Inhaltsverzeichnis fuehren, und zieht eine Publikation nach,
der er noch fehlt. attached macht dieselbe Pruefung fuer sich, ohne zu
publizieren. Warum das noetig ist, steht im Abschnitt Einhaengung in die
Publikation.

Bei hennibock_type: publication ist der Body ein Inhaltsverzeichnis. Die
Wikilink-Aufloesung macht daraus von selbst das Gewuenschte: ein publiziertes
Kapitel wird ein Link, ein unpubliziertes bleibt Anzeigetext und waechst beim
naechsten Publish nach. Einzige Sonderlogik ist hennibock_skip: ein so markiertes
Kapitel wird ganz aus der Liste entfernt, statt als Text stehen zu bleiben, und
beim Aufloesen der Verweise ueberlaufen.

hennibock_chapter_type liest dieses Skript nicht. Es ist die Vorlage, aus der
publish-next-chapter den Typ an die Kapitel vererbt, und steht allein in
next_chapter.py. Hier zaehlt immer der eigene hennibock_type der Notiz.

Der Skill erzeugt nur Inhalt und Bundle. Index, Kaskade und Idempotenz bleiben
allein bei HenniBock (siehe Spec - HenniBock).

Nur Standardbibliothek plus die macOS-Werkzeuge sips (Bildmasse) und curl (POST).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile
from datetime import date
from pathlib import Path


SCHEMA_VERSION = "2"
# Grenzen aus dem Bundle-Format bzw. der Publish-Skill-Spec.
SLUG_BASE_MAX = 96
BILDNAME_MAX = 48
GENERATOR = "hennibock-publish 0.1"
# Autor und Bereiche gehoeren der HenniBock-Instanz, nicht einem Vault. Die
# Plattform hat genau eine Autorinnenfigur und ein festes Bereichsvokabular,
# und beide bleiben gleich, aus welchem Vault ein Text kommt. Der Wert steht
# deshalb hier und nicht im Manifest. Ein Text mit anderem Autor setzt
# "hennibock_author" in seinem Frontmatter.
DEFAULT_AUTHOR = "Henriette Einstein"
VALID_AREAS = {"Geschichte", "Wirtschaft", "Technik", "Henni privat"}

# Der Typ, dessen Body ein Inhaltsverzeichnis ist. Nur bei ihm werden
# uebersprungene Kapitel aus der Liste entfernt.
PUBLICATION_TYPE = "publication"

# Die Typ-Praefixe der Vault-Dateinamen (siehe Wiki-Konventionen). Sie ordnen
# den Vault und fallen beim Verlassen des Vault-Kontexts weg, siehe
# strip_vault_prefix. Laengere zuerst, damit kein kuerzeres vorher greift.
# Eine Liste fuer beide Zwecke, Slug und Titel. Bis zum 21.08.2026 standen
# zwei getrennte Listen im selben Skript, und sie sind auseinandergelaufen:
# der Slug verlor sein Praefix, der Titel behielt es. Aufgefallen ist das bei
# einem Text ohne Alias, denn nur dort faellt der Dateiname auf die Anzeige
# durch. Laengere zuerst, damit kein kuerzeres vorher greift.
VAULT_PREFIXES = ("Beurteilung - ", "Essay - ", "Story - ", "Idee - ",
                  "Text - ", "Book - ", "MOC - ", "Bild - ", "Prj - ",
                  "Pub - ", "Kap - ", "Src - ")

UMLAUTS = {
    "ä": "ae", "ö": "oe", "ü": "ue",
    "Ä": "ae", "Ö": "oe", "Ü": "ue",
    "ß": "ss",
}



# ---------------------------------------------------------------------------
# Vault-Basis und Textwerkzeuge
# ---------------------------------------------------------------------------

def vault_root(arg=None) -> Path:
    """Die Ablage, in der gearbeitet wird.

    Frueher kam sie aus einem Manifest ausserhalb des Formats. Jetzt aus
    `ablage.finde`, also in fuenf Stufen und mit derselben Antwort wie jedes
    andere Werkzeug des Harness.
    """
    from .. import ablage
    try:
        return Path(ablage.finde(arg))
    except ablage.KeineAblage as fehler:
        raise SystemExit("FEHLER: " + str(fehler))


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def rel_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def slugify(text: str, max_len: int = 0) -> str:
    """Normalisiert Prosa zu einem Slug-Anteil.

    Die Ersetzung der Umlaute durch ae/oe/ue/ss steht vor dem Zerlegen der
    Diakritika, sonst wuerde aus "ue" ein "u" und Buecher fiele mit Bucher
    zusammen. Sie widerspricht nicht den Schreibregeln des Vaults: die gelten
    fuer Prosa, ein Slug ist ein technischer Bezeichner in einer URL, und die
    Grammatik laesst dort nur ASCII-Kleinbuchstaben zu.

    `max_len` kappt am letzten vollstaendigen Bindestrich-Abschnitt, damit kein
    Wort mitten entzweigeht.
    """
    text = nfc(text)
    for key, value in UMLAUTS.items():
        text = text.replace(key, value)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    if max_len and len(text) > max_len:
        text = text[:max_len]
        if "-" in text:
            text = text.rsplit("-", 1)[0]
        text = text.strip("-")
    return text


# ---------------------------------------------------------------------------
# Frontmatter lesen und schreiben
# ---------------------------------------------------------------------------

def split_frontmatter(text: str):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return [], text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], "\n".join(lines[i + 1:])
    return [], text


def frontmatter_value(fm_lines, key: str) -> str:
    prefix = key + ":"
    for line in fm_lines:
        if line.startswith(prefix):
            return line.split(":", 1)[1].strip().strip("'\"")
    return ""


def frontmatter_list(fm_lines, key: str):
    values = []
    in_block = False
    for line in fm_lines:
        if line.startswith(key + ":"):
            in_block = True
            tail = line.split(":", 1)[1].strip()
            if tail and tail != "[]":
                values.append(tail.strip("'\""))
            continue
        if in_block:
            if re.match(r"^[A-Za-z0-9_]+:", line):
                break
            m = re.match(r"^\s*-\s*(.+?)\s*$", line)
            if m:
                values.append(m.group(1).strip().strip("'\""))
    return values


def first_alias(fm_lines) -> str:
    for i, line in enumerate(fm_lines):
        if line.startswith("aliases:"):
            tail = line.split(":", 1)[1].strip()
            if tail and tail != "[]":
                return tail.strip("'\"")
            for nxt in fm_lines[i + 1:]:
                if re.match(r"^[A-Za-z0-9_]+:", nxt):
                    return ""
                m = re.match(r"^\s*-\s*(.+?)\s*$", nxt)
                if m:
                    return m.group(1).strip().strip("'\"")
    return ""


def set_frontmatter_fields(raw: str, updates: dict) -> str:
    """Setzt oder ersetzt flache Scalar-Felder in der Frontmatter. Body bleibt
    unveraendert. Legt bei fehlender Frontmatter keine an (Fehler)."""
    lines = raw.split("\n")
    if not lines or lines[0].strip() != "---":
        raise ValueError("Notiz hat keine Frontmatter")
    close = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            close = i
            break
    if close is None:
        raise ValueError("Frontmatter nicht geschlossen")

    fm = lines[1:close]
    remaining = dict(updates)
    for i, line in enumerate(fm):
        m = re.match(r"^([A-Za-z0-9_]+):", line)
        if m and m.group(1) in remaining:
            key = m.group(1)
            fm[i] = key + ": " + remaining.pop(key)
    for key, value in remaining.items():
        fm.append(key + ": " + value)

    return "\n".join(lines[:1] + fm + lines[close:])


# ---------------------------------------------------------------------------
# Notiz lokalisieren und Vault-Index
# ---------------------------------------------------------------------------

def build_note_index(root: Path):
    index = {}
    for path in root.rglob("*.md"):
        parts = path.relative_to(root).parts
        if parts and parts[0].startswith("."):
            continue
        index.setdefault(nfc(path.stem), path)
    return index


def locate_note(root: Path, arg: str, index):
    arg = arg.strip()
    candidate = Path(arg)
    if candidate.is_file():
        return candidate.resolve()
    rel = root / arg
    if rel.is_file():
        return rel.resolve()
    stem = arg[:-3] if arg.endswith(".md") else arg
    hit = index.get(nfc(stem))
    if hit:
        return hit.resolve()
    return None


def note_title(fm_lines, path: Path) -> str:
    """Der Titel aus dem Frontmatter, sonst der Dateiname.

    `name` steht hier neben `title`, weil eine HKF-Notiz ihren Namen dort
    traegt und der Dateiname ein Slug ist. Ohne diese Stufe hiesse jeder
    Beitrag wie seine Datei.
    """
    title = (frontmatter_value(fm_lines, "title")
             or frontmatter_value(fm_lines, "name")
             or first_alias(fm_lines))
    if title:
        return title
    return strip_vault_prefix(path.stem)


# ---------------------------------------------------------------------------
# Bilder und Callouts
# ---------------------------------------------------------------------------

EMBED_RE = re.compile(r"!\[\[([^\]]+)\]\]")

# Ein Wikilink als Listenpunkt, geordnet (1.) oder ungeordnet (-, *, +). Genau
# das ist laut Spec ein Kapitel: ein Link im Fliesstext ist keines.
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s*\[\[([^\]]+)\]\]")

# Der Metadatenkopf eines ai-image-Callouts. Er steht zwischen der Marker-Zeile
# und dem englischen Prompt und endet an der ersten Leerzeile oder der ersten
# Zeile, die nicht "schluessel: wert" ist.
CALLOUT_META_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$")

# Mehr Schluessel gibt es nicht. Ein Tippfehler wie "alr:" wuerde sonst still zum
# Prompt gerechnet und der Alt-Text waere spurlos weg.
CALLOUT_META_KEYS = ("alt", "project", "character")

# Zeichen, die die Schreibregeln des Vaults in Prosa verbieten. Ein Alt-Text
# wandert in eine Inhaltsnotiz und laeuft dort in den Schreibregel-Hook. Ihn
# vorher zu pruefen ist billiger, als einen Publish-Lauf daran scheitern zu
# lassen.
VERBOTENE_ZEICHEN = {"—": "Geviertstrich", "–": "Halbgeviertstrich",
                     ";": "Strichpunkt",
                     "„": "typografisches Anfuehrungszeichen",
                     "“": "typografisches Anfuehrungszeichen",
                     "”": "typografisches Anfuehrungszeichen"}


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value.replace('\\"', '"').strip()


def parse_callout(lines, start: int, line_offset: int = 0) -> dict:
    """Zerlegt den Callout ab Zeile ``start`` in Metadatenkopf und Prompt.

    Der Kopf endet an der ersten Leerzeile oder an der ersten Zeile, die nicht
    wie ``schluessel: wert`` aussieht. Beides kommt vor: 860 Callouts im Bestand
    beginnen direkt mit dem Prompt, ohne jeden Kopf.

    ``alt_line`` ist die Zeilennummer eines vorhandenen alt-Feldes, sonst None.
    ``head_lines`` zaehlt die Kopfzeilen, damit ein Schreiber weiss, ob er beim
    Einfuegen zusaetzlich eine Trennzeile braucht.

    ``line_offset`` verschiebt die Zeilennummer in Fehlermeldungen. ``lines`` ist
    mal der Body und mal die ganze Datei, und eine Nummer, die auf die falsche
    Zeile zeigt, ist schlechter als keine.
    """
    meta = {}
    alt_line = None
    prompt_teile = []
    kopf_offen = True
    kopf_zeilen = 0
    j = start + 1
    while j < len(lines) and lines[j].lstrip().startswith(">"):
        text = re.sub(r"^>\s?", "", lines[j].lstrip())
        if kopf_offen:
            if not text.strip():
                kopf_offen = False
                j += 1
                continue
            m = CALLOUT_META_RE.match(text.strip())
            if m:
                schluessel = m.group(1).lower()
                if schluessel not in CALLOUT_META_KEYS:
                    raise SystemExit(
                        "FEHLER: unbekannte Metadatenzeile im ai-image-Callout in "
                        "Zeile " + str(j + 1 + line_offset) + ": " + text.strip()
                        + ". Zulaessig "
                        "sind " + ", ".join(CALLOUT_META_KEYS) + ".")
                meta[schluessel] = unquote(m.group(2))
                if schluessel == "alt":
                    alt_line = j
                kopf_zeilen += 1
                j += 1
                continue
            kopf_offen = False
        if text.strip():
            prompt_teile.append(text.strip())
        j += 1
    return {
        "marker_line": start,
        "end_line": j,
        "alt_line": alt_line,
        "head_lines": kopf_zeilen,
        "alt": meta.get("alt", ""),
        "project": meta.get("project", ""),
        "character": meta.get("character", ""),
        "prompt_en": " ".join(prompt_teile).strip(),
    }


def find_callouts(lines, line_offset: int = 0) -> list:
    callouts = []
    i = 0
    while i < len(lines):
        if re.match(r"^>\s*\[!ai-image\]", lines[i]):
            callout = parse_callout(lines, i, line_offset)
            callouts.append(callout)
            i = callout["end_line"]
            continue
        i += 1
    return callouts


def image_dimensions(path: Path):
    try:
        proc = subprocess.run(
            ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
            text=True, capture_output=True,
        )
    except FileNotFoundError:
        return None, None
    if proc.returncode != 0:
        return None, None
    width = height = None
    for line in proc.stdout.split("\n"):
        m = re.search(r"pixelWidth:\s*(\d+)", line)
        if m:
            width = int(m.group(1))
        m = re.search(r"pixelHeight:\s*(\d+)", line)
        if m:
            height = int(m.group(1))
    return width, height


def collect_images(body: str, root: Path, slug_base: str, uuid12: str,
                   line_offset: int = 0):
    """Findet Bild-Embeds in Reihenfolge und paart jeden mit dem englischen
    Prompt des ai-image-Callouts, der ihm am naechsten folgt (bis zum naechsten
    Embed). Ein Embed ohne Callout traegt einen leeren Prompt."""
    lines = body.split("\n")
    belegt = {}
    embeds = []  # (line_idx, target, bildname, media_slug, ext)
    for idx, line in enumerate(lines):
        m = EMBED_RE.search(line)
        if not m:
            continue
        target = m.group(1).split("|", 1)[0].strip()
        if not target:
            continue
        source = root / target
        stem = Path(target).stem
        bildname = slugify(stem, BILDNAME_MAX)
        if not bildname:
            raise SystemExit(
                "FEHLER: aus dem Bildnamen bleibt nach der Normalisierung nichts "
                "uebrig: " + target)
        # Der Dokument-Slug taugt als Grundlage nicht: den vergibt der Server,
        # und der Skill kennt ihn beim Bauen noch gar nicht. Die zwoelf
        # Hex-Zeichen der UUID sind im Vault bekannt und machen den Medien-Slug
        # ueber Dokumentgrenzen hinweg eindeutig.
        media_slug = slug_base + "-" + uuid12 + "-" + bildname
        # Erst die Normalisierung kann zwei verschiedene Bildnamen
        # zusammenfuehren, etwa "Strasse" und "Strasze". Innerhalb eines
        # Dokuments wird dann durchnummeriert.
        if media_slug in belegt:
            belegt[media_slug] += 1
            media_slug = media_slug + "-" + str(belegt[media_slug])
        else:
            belegt[media_slug] = 1
        ext = Path(target).suffix.lower() or ".jpg"
        embeds.append({
            "line": idx, "target": target, "source": source,
            "bildname": bildname, "media_slug": media_slug, "ext": ext,
        })

    # Jeden Callout dem naechsten vorangehenden Embed zuordnen. Prompt und
    # Alt-Text stammen damit aus derselben Quelle und koennen nicht auseinander
    # laufen.
    for callout in find_callouts(lines, line_offset):
        best = None
        for emb in embeds:
            if (emb["line"] < callout["marker_line"]
                    and (best is None or emb["line"] > best["line"])):
                best = emb
        if best is not None and "prompt_en" not in best:
            best["prompt_en"] = callout["prompt_en"]
            best["alt_callout"] = callout["alt"]
            best["callout_line"] = callout["marker_line"]
    for emb in embeds:
        emb.setdefault("prompt_en", "")
        emb.setdefault("alt_callout", "")
        emb.setdefault("callout_line", None)
    return embeds


def resolve_alts(images, overrides: dict) -> dict:
    """Die wirksame Zuordnung media_slug -> Alt-Text.

    Vorrang hat ein Wert aus ``alts.json``: er ist die bewusste Abweichung fuer
    genau diesen Publish. Sonst gilt das ``alt``-Feld des Callouts, das im Vault
    steht und dort auch bleibt. Fehlt beides, steht der Slug in ``fehlend``.
    """
    aufgeloest, quellen, fehlend = {}, {}, []
    for emb in images:
        slug = emb["media_slug"]
        override = (overrides.get(slug) or "").strip()
        callout = (emb.get("alt_callout") or "").strip()
        if override:
            aufgeloest[slug], quellen[slug] = override, "override"
        elif callout:
            aufgeloest[slug], quellen[slug] = callout, "callout"
        else:
            quellen[slug] = "missing"
            fehlend.append(slug)
    return {"alts": aufgeloest, "sources": quellen, "missing": fehlend}


# ---------------------------------------------------------------------------
# Identitaet
# ---------------------------------------------------------------------------

def ensure_ref(path: Path, fm_lines):
    """Stellt sicher, dass eine Notiz ein hennibock_ref traegt, und gibt es
    zurueck. Zweiter Rueckgabewert sagt, ob geschrieben wurde.

    Die UUID entsteht im Vault, lange bevor der Server das Dokument kennt. Nur
    so laesst sich ein Verweis auf ein noch ungeschriebenes Ziel ueberhaupt
    formulieren. Eine Kollisionspruefung entfaellt, die UUID traegt sie in sich.
    """
    ref = frontmatter_value(fm_lines, "hennibock_ref")
    if ref:
        return ref, False
    ref = str(uuid.uuid4())
    raw = path.read_text(encoding="utf-8")
    path.write_text(
        set_frontmatter_fields(raw, {
            "hennibock_ref": ref,
            "modified": '"' + date.today().isoformat() + '"',
        }),
        encoding="utf-8",
    )
    return ref, True


def ensure_identity(path: Path, fm_lines, title: str, redate: bool = False):
    """Gibt (document_ref, slug_base, published, changed) zurueck.

    Der Slug ist keine Angabe des Produzenten mehr: er entsteht serverseitig aus
    slug_base und der Strategie der Instanz. Der Skill schlaegt nur den lesbaren
    Anteil vor und kann ihn nicht vorwegnehmen.

    `redate` setzt das Veroeffentlichungsdatum auf heute. Ohne die Ansage bleibt
    ein einmal gesetztes Datum stehen, auch bei einem erneuten Publish.
    """
    ref, changed = ensure_ref(path, fm_lines)
    if changed:
        fm_lines, _ = split_frontmatter(path.read_text(encoding="utf-8"))
    published = frontmatter_value(fm_lines, "hennibock_published")
    updates = {}
    today = date.today()
    slug_base = slugify(strip_vault_prefix(path.stem), SLUG_BASE_MAX) or "dokument"
    if not published or redate:
        published = today.isoformat()
        updates["hennibock_published"] = '"' + published + '"'
        changed = True
        updates["modified"] = '"' + today.isoformat() + '"'
        raw = path.read_text(encoding="utf-8")
        path.write_text(set_frontmatter_fields(raw, updates), encoding="utf-8")

    return ref, slug_base, published, changed


# ---------------------------------------------------------------------------
# Body saeubern (build)
# ---------------------------------------------------------------------------

# Die Ueberschrift, ab der der Verweisapparat einer Notiz beginnt. HKF Core
# §5.6 nennt ihn `# Verbindungen`, und so heisst er auch in den gewachsenen
# Obsidian-Vaults. `Siehe auch` ist die Altform: so hiess der Abschnitt in der
# Spezifikation bis zum 05.09.2026, und eine Wissensbasis, die noch nicht
# umgestellt ist, traegt ihn so. Der Publisher hat den Apparat abzuschneiden,
# wie immer er heisst: was dahinter steht, sind Quellen, MOCs und
# Kapitelketten, also Vault-Geruest und kein Lesertext. Nur den einen Namen zu
# kennen hiesse den halben Bestand ungeprueft nach draussen zu geben.
VERWEISUEBERSCHRIFT = re.compile(r"#{1,2}\s+(?:Verbindungen|Siehe auch)\b")
VERWEISUEBERSCHRIFT_ZEILE = re.compile(
    r"^#{1,2}\s+(?:Verbindungen|Siehe auch)\s*$", re.M)

def strip_callouts_and_verbindungen(body: str) -> str:
    """Schneidet alles ab der Verweisueberschrift ab und behandelt die
    beiden Callout-Typen, die eine Notiz mitbringen darf. Alles vor dem Schnitt
    bleibt erhalten, insbesondere ein vorangestellter `## Externe Quellen`-
    Abschnitt und externe Markdown-Links.

    Ein `ai-image`-Callout wird verworfen: er ist die Bestellung des Bildes, das
    Ergebnis steht als Embed daneben.

    Ein `hennibock-intro`-Callout wird ausgepackt: Marker-Zeile weg, Blockquote-
    Prefix weg, der Klappentext geht als gewoehnliche Prosa ins Bundle. Der
    Callout ist Vault-Semantik fuer Obsidian, HenniBock kennt keine Callouts und
    wuerde die Marker-Zeile sonst woertlich anzeigen.

    Die Ueberschrift wird auch erkannt, wenn sie ohne Zeilenumbruch
    an eine Vorzeile geklebt ist (etwa an das Ende einer Quellenliste). Der Teil
    der Zeile davor bleibt dann erhalten."""
    lines = body.split("\n")
    for i, line in enumerate(lines):
        m = VERWEISUEBERSCHRIFT.search(line)
        if m:
            head = line[:m.start()].rstrip()
            lines = lines[:i] + ([head] if head else [])
            break
    cleaned = []
    i = 0
    while i < len(lines):
        if re.match(r"^>\s*\[!ai-image\]", lines[i]):
            i += 1
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                i += 1
            continue
        if re.match(r"^>\s*\[!hennibock-intro\]", lines[i]):
            i += 1
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                cleaned.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            continue
        cleaned.append(lines[i])
        i += 1
    return "\n".join(cleaned)


def strip_wikilink(text: str) -> str:
    """Der Stem, auf den ein Wikilink zeigt, ohne Alias, Anker und Pfad.

    Der Pfad faellt weg, weil jeder Aufrufer den Stem braucht: der Notiz-Index
    ist ueber Stems gefuehrt, und `publikationen_der_notiz` vergleicht gegen
    `path.stem`. In einem gewachsenen Obsidian-Vault stehen kurze Verweise und
    beides ist dasselbe. In einer HKB nicht: HKF Core §3.6 macht den
    qualifizierten Verweis zur Pflicht, und ohne diesen Schnitt findet dort
    kein Kapitel mehr seine Publikation und keine Publikation mehr ihre
    Kapitel. Der Fehler faellt nicht auf, er liefert nur leere Mengen.

    Dass der Stem allein genuegt, ist keine Verkuerzung: derselbe §3.6 macht
    einen mehrdeutigen Verweis zum Fehler, ein Stem ist also ablageweit
    eindeutig.
    """
    t = text.strip()
    if t.startswith("[[") and t.endswith("]]"):
        t = t[2:-2]
    t = t.split("|", 1)[0].split("#", 1)[0].strip()
    return t.rsplit("/", 1)[-1]


def is_skipped(index, stem: str) -> bool:
    """Traegt das Kapitel hennibock_skip? Ein solches Kapitel erscheint nie auf
    HenniBock und bekommt darum auch nie einen Slug."""
    n = index.get(nfc(stem))
    if not n or not n.is_file():
        return False
    fm, _ = split_frontmatter(n.read_text(encoding="utf-8"))
    return (frontmatter_value(fm, "hennibock_skip") or "").strip().lower() == "true"


def publication_order(pub_note: Path):
    """Kapitelreihenfolge aus dem Inhaltsverzeichnis einer Publication: die
    Ziel-Stems aller Wikilink-Listenpunkte in Dokumentreihenfolge. Geordnete und
    ungeordnete Listen zaehlen gleich, beide Schreibweisen sind im Bestand in
    Gebrauch. Der Verweisapparat wird abgeschnitten: seine Quellen, MOCs und
    Areas stehen ebenfalls als Wikilink-Listenpunkte da, sind aber keine Kapitel,
    und ohne den Schnitt bekaeme das letzte Kapitel eine Quelle als next."""
    return publication_order_text(pub_note.read_text(encoding="utf-8"))


def publication_order_text(text: str):
    """Dasselbe, aber auf dem Text statt auf der Datei.

    Es gibt diese Fassung, damit `kette.toc_chapters` sie rufen kann statt eine
    zweite zu fuehren. Die beiden sind auseinandergelaufen, und der Schaden war
    genau der, vor dem die Docstring dort seit jeher warnt: die Rotation waehlt
    ein anderes Kapitel, als das Publizieren in die Kette haengt. Gemessen am
    04.09.2026 ueber zwoelf Publikationen einer migrierten Ablage: zwoelf
    Abweichungen, drei davon mit null erkannten Kapiteln. Eine Regel, die an
    zwei Stellen steht, gilt frueher oder spaeter nur an einer.
    """
    toc = VERWEISUEBERSCHRIFT_ZEILE.split(text)[0]
    order, gesehen = [], set()
    for line in toc.split("\n"):
        m = LIST_ITEM_RE.match(line)
        if not m:
            continue
        stem = strip_wikilink(m.group(1))
        if stem and stem not in gesehen:
            gesehen.add(stem)
            order.append(stem)
    return order


# Seriennavigation gibt es nicht mehr. Die Reihenfolge steht allein im
# Inhaltsverzeichnis der Publikation, HenniBock leitet die Nachbarn daraus ab.
# Ein Kapitel, das seine Nachbarn selbst benennt, koennte davon abweichen und
# stuende in zwei Werken zwangslaeufig falsch. Das erspart dem Skill zugleich
# den Nachtrags-Publish, mit dem ein spaeter erschienener Nachbar frueher
# eingetragen werden musste.


def prune_skipped_toc(body: str, index) -> str:
    """Aus dem Inhaltsverzeichnis einer Publikation die Listenpunkte entfernen,
    deren Kapitel hennibock_skip traegt. Nicht auf Anzeigetext reduzieren wie
    ein unpubliziertes Kapitel: ein Punkt, der nie ein Link wird, waere auf
    HenniBock ein Versprechen, das niemand einloest. Im Vault bleibt der Eintrag
    stehen, dort gehoert das Kapitel weiter zum Werk und wandert ins eBook."""
    out = []
    for line in body.split("\n"):
        m = LIST_ITEM_RE.match(line)
        if m and is_skipped(index, strip_wikilink(m.group(1))):
            continue
        out.append(line)
    return "\n".join(out)


def strip_vault_prefix(name: str) -> str:
    """Das Typ-Praefix eines Vault-Dateinamens fuer die Anzeige entfernen.

    Die Praefixe aus Wiki-Konventionen ordnen den Vault, nach aussen sind sie
    Jargon: auf einer HenniBock-Seite hat "Kap - Einleitung" nichts zu suchen.
    Der Vault kennt das Strippen schon, create-note-images bildet damit seine
    Ordnernamen. Greift nur, wenn der Autor keinen Anzeigenamen gesetzt hat,
    denn ein gesetzter Anzeigename ist seine Entscheidung.
    """
    for p in VAULT_PREFIXES:
        if name.startswith(p) and len(name) > len(p):
            return name[len(p):]
    return name


def resolve_links(body: str, root: Path, index, beruehrt=None,
                  pflicht_refs=None):
    """Wikilinks aufloesen. Eine publizierbare Zielnotiz wird zu
    `henni://document/<UUID>`, sonst bleibt nur der Anzeigetext. Bild-Embeds
    (![[...]]) schuetzt der Negative-Lookbehind.

    Der Zweig haengt an der Publizierbarkeit (hennibock_type), nicht mehr an
    einem Slug. Frueher hing er daran, ob das Ziel schon auf HenniBock lag: ein
    Verweis auf eine geplante, aber ungeschriebene Notiz ging dabei verloren,
    und niemand merkte es, weil der Anzeigetext ja stehen blieb.

    `pflicht_refs` enthaelt die Ziel-Stems, die eine UUID auch dann bekommen,
    wenn die Zielnotiz noch kein `hennibock_type` traegt. Das sind die Punkte
    des Inhaltsverzeichnisses einer Publikation. Ohne sie kannte ein einmal
    publiziertes Verzeichnis nur die Kapitel, die zu diesem Zeitpunkt schon
    publikationsreif waren, und jedes spaeter erschienene Kapitel blieb Text,
    bis jemand die Publikation erneut publizierte. Gefahrlos ist das, weil
    HenniBock einen Verweis ohne Ziel als reinen Text rendert und ihn erst zum
    Link macht, wenn das Kapitel eintrifft, siehe Spec - HenniBock
    Dokumentidentitaet und offene Links, Abschnitt Markdown-zu-HTML.

    Fehlt der Zielnotiz die UUID, wird sie dort angelegt. Der Publish-Lauf
    aendert damit gelegentlich eine fremde Notiz; die Pfade sammelt `beruehrt`
    fuer die Meldung am Ende des Laufs ein.
    """
    pflicht = pflicht_refs or set()

    def repl(match):
        inner = match.group(1)
        parts = inner.split("|", 1)
        target = parts[0].strip()
        display = (parts[1].strip() if len(parts) > 1
                   else strip_vault_prefix(target))
        note = index.get(nfc(target))
        if note and note.is_file():
            fm, _ = split_frontmatter(note.read_text(encoding="utf-8"))
            if frontmatter_value(fm, "hennibock_type") or nfc(target) in pflicht:
                ref, geschrieben = ensure_ref(note, fm)
                if geschrieben and beruehrt is not None:
                    beruehrt.append(rel_to_root(note, root))
                return "[" + display + "](henni://document/" + ref + ")"
        return display

    return re.sub(r"(?<!!)\[\[([^\]]+)\]\]", repl, body)


def toc_stems(body: str) -> set:
    """Die Ziel-Stems der Listenpunkte eines Inhaltsverzeichnisses, gemessen an
    dem Body, der schon von Callouts, Verweisapparat und uebersprungenen Kapiteln
    befreit ist. Ein Kapitel mit `hennibock_skip` faellt vorher aus der Liste
    und bekommt darum auch hier keine UUID."""
    stems = set()
    for line in body.split("\n"):
        m = LIST_ITEM_RE.match(line)
        if m:
            stems.add(nfc(strip_wikilink(m.group(1))))
    return stems


def cover_aus_property(fm_lines, root: Path, slug_base: str, uuid12: str):
    """Das Titelbild aus der Property `cover`, wenn der Body keins einbettet.

    Die Typdefinition `publication` des Bundles `hkf-publikation` nennt `cover`
    als das Titelbild eines Werkes, und `hk-epub` liest es auch. Nur hier wurde
    allein der Body durchsucht, weil eine Pub-Notiz in HenniPKA ihr Titelbild
    einbettet. Eine Publikation, die der Typdefinition folgt, war damit nicht
    publizierbar, und die Meldung nannte den Grund nicht.

    Der Zusatz ist additiv: er greift nur, wenn der Body gar kein Bild traegt,
    und `rewrite_body` setzt ein Bild ohne Fundstelle im Body dort auch nicht
    ein. Es wird Titelbild und Medium des Bundles, mehr nicht.
    """
    wert = frontmatter_value(fm_lines, "cover")
    ziel = strip_wikilink_pfad(wert)
    if not ziel or not (root / ziel).is_file():
        return []
    return collect_images("![[" + ziel + "]]", root, slug_base, uuid12)


def strip_wikilink_pfad(text: str) -> str:
    """Wie `strip_wikilink`, aber der Pfad bleibt stehen: hier wird damit auf
    eine Datei zugegriffen und nicht im Notiz-Index gesucht."""
    t = (text or "").strip()
    if t.startswith("[[") and t.endswith("]]"):
        t = t[2:-2]
    return t.split("|", 1)[0].split("#", 1)[0].strip()


def rewrite_body(body: str, root: Path, index, images, cover_slug, alts,
                 doc_type=None, beruehrt=None):
    body = strip_callouts_and_verbindungen(body)
    pflicht_refs = None
    if doc_type == PUBLICATION_TYPE:
        # Vor resolve_links: sonst waere der Punkt schon zu Anzeigetext
        # geworden und nicht mehr als uebersprungenes Kapitel erkennbar.
        body = prune_skipped_toc(body, index)
        pflicht_refs = toc_stems(body)
    by_line = {emb["line"]: emb for emb in images}

    def repl(match):
        target = match.group(1).split("|", 1)[0].strip()
        emb = next((e for e in images if e["target"] == target), None)
        if emb is None:
            return ""
        if emb["media_slug"] == cover_slug:
            return ""  # Cover kommt in die Frontmatter, nicht in den Body.
        alt = alts.get(emb["media_slug"], "")
        return "![" + alt + "](image/" + emb["media_slug"] + ")"

    body = EMBED_RE.sub(repl, body)
    body = resolve_links(body, root, index, beruehrt, pflicht_refs)
    body = re.sub(r"\n{3,}", "\n\n", body).strip("\n")
    return body


# ---------------------------------------------------------------------------
# Frontmatter und Sidecars bauen
# ---------------------------------------------------------------------------

def yaml_scalar(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_document_frontmatter(meta: dict) -> str:
    # Identitaet und Typ stehen im Manifest, der oeffentliche Slug entsteht
    # serverseitig. Keines davon gehoert ins Frontmatter, ein Bundle mit einem
    # dieser Felder wird abgewiesen. Felder fuer Seriennavigation gibt es nicht. status faellt auf die Vorgabe
    # "published", author auf "Henriette Einstein". Ein Bundle traegt keine
    # Angabe, die nichts aussagt.
    lines = ["---"]
    lines.append("title: " + yaml_scalar(meta["title"]))
    lines.append("summary: " + yaml_scalar(meta["summary"]))
    if meta["author"] != DEFAULT_AUTHOR:
        lines.append("author: " + yaml_scalar(meta["author"]))
    lines.append("published: " + yaml_scalar(meta["published"]))
    lines.append("areas:")
    for area in meta["areas"]:
        lines.append("  - " + yaml_scalar(area))
    lines.append("cover: " + yaml_scalar("image/" + meta["cover_slug"]))
    if meta.get("tags"):
        lines.append("tags:")
        for tag in meta["tags"]:
            lines.append("  - " + yaml_scalar(tag))
    lines.append("---")
    return "\n".join(lines)


def build_sidecar(alt: str, width, height) -> dict:
    """Sidecar fuers Cover. Ohne slug und type, die stehen im Pfad.

    Nur das Cover braucht ueberhaupt eine: die Bilder im Body tragen ihren
    Alt-Text in der Einbettung "![Alt](image/<slug>)", und genau von dort holt
    HenniBock ihn. Das Cover wird aber aus dem Body entfernt, weil es ins
    Frontmatter gehoert, und hat deshalb keine Einbettung, aus der ein Alt-Text
    kommen koennte. Ohne diese Sidecar fiele es auf den Dokumenttitel zurueck
    und verloere den aus dem Callout gewonnenen Text.
    """
    sidecar = {"alt": alt}
    if width:
        sidecar["width"] = width
    if height:
        sidecar["height"] = height
    return sidecar


# ---------------------------------------------------------------------------
# Gemeinsame Vorbereitung
# ---------------------------------------------------------------------------

def prepare(root: Path, note_arg: str, redate: bool = False):
    index = build_note_index(root)
    path = locate_note(root, note_arg, index)
    if path is None:
        raise SystemExit("FEHLER: Notiz nicht gefunden: " + note_arg)
    raw = path.read_text(encoding="utf-8")
    fm_lines, body = split_frontmatter(raw)
    if not fm_lines:
        raise SystemExit("FEHLER: Notiz hat keine Frontmatter: " + str(path))

    hb_type = frontmatter_value(fm_lines, "hennibock_type")
    if not hb_type:
        raise SystemExit("FEHLER: hennibock_type fehlt in der Notiz")
    areas = frontmatter_list(fm_lines, "hennibock_areas")
    if not areas:
        raise SystemExit("FEHLER: hennibock_areas fehlt in der Notiz")
    bad = [a for a in areas if a not in VALID_AREAS]
    if bad:
        raise SystemExit("FEHLER: unbekannte hennibock_areas: " + ", ".join(bad))
    if not frontmatter_value(fm_lines, "summary").strip():
        raise SystemExit("FEHLER: summary fehlt oder ist leer in der Notiz")

    title = note_title(fm_lines, path)
    ref, slug_base, published, changed = ensure_identity(
        path, fm_lines, title, redate=redate)

    # Frontmatter nach dem Writeback neu lesen.
    fm_lines, body = split_frontmatter(path.read_text(encoding="utf-8"))

    uuid12 = ref.replace("-", "")[:12]
    # Der Body beginnt hinter der Frontmatter. Der Offset macht aus einer
    # Body-Zeile die Zeile in der Datei, wie sie im Editor steht.
    fm_offset = len(path.read_text(encoding="utf-8").split("\n")) - len(body.split("\n"))
    images = collect_images(body, root, slug_base, uuid12, fm_offset)
    if not images:
        images = cover_aus_property(fm_lines, root, slug_base, uuid12)
    if not images:
        raise SystemExit(
            "FEHLER: Notiz hat kein Bild als Titelbild. Entweder ein Embed im "
            "Body oder die Property `cover`.")
    for emb in images:
        if not emb["source"].is_file():
            raise SystemExit("FEHLER: Bilddatei fehlt: " + emb["target"])
        emb["width"], emb["height"] = image_dimensions(emb["source"])

    cover_hint = frontmatter_value(fm_lines, "hennibock_cover")
    cover = None
    if cover_hint:
        hint = slugify(Path(cover_hint).stem)
        cover = next((e for e in images if e["bildname"] == hint
                      or e["media_slug"] == cover_hint
                      or Path(e["target"]).name == cover_hint), None)
    if cover is None:
        cover = images[0]

    meta = {
        "path": path,
        "index": index,
        "fm_lines": fm_lines,
        "body": body,
        "type": hb_type,
        "areas": areas,
        "tags": frontmatter_list(fm_lines, "tags"),
        "title": title,
        "summary": frontmatter_value(fm_lines, "summary"),
        "author": frontmatter_value(fm_lines, "hennibock_author") or DEFAULT_AUTHOR,
        "ref": ref,
        "slug_base": slug_base,
        "published": published,
        "changed": changed,
        "images": images,
        "cover": cover,
        "beruehrt": [],
    }
    return meta


# ---------------------------------------------------------------------------
# analyze
# ---------------------------------------------------------------------------

def load_alts(pfad: str) -> dict:
    if not pfad:
        return {}
    alts_path = Path(pfad)
    if not alts_path.is_file():
        raise SystemExit("FEHLER: alts-Datei nicht gefunden: " + pfad)
    daten = json.loads(alts_path.read_text(encoding="utf-8"))
    if not isinstance(daten, dict):
        raise SystemExit("FEHLER: alts-Datei ist kein Objekt media_slug -> Alt-Text")
    return daten


def cmd_analyze(root: Path, args):
    meta = prepare(root, args.note)
    aufloesung = resolve_alts(meta["images"], load_alts(args.alts))
    out = {
        "note": rel_to_root(meta["path"], root),
        "document_ref": meta["ref"],
        "slug_base": meta["slug_base"],
        "type": meta["type"],
        "title": meta["title"],
        "summary": meta["summary"],
        "author": meta["author"],
        "published": meta["published"],
        "areas": meta["areas"],
        "tags": meta["tags"],
        "identity_written": meta["changed"],
        "cover_slug": meta["cover"]["media_slug"],
        "images": [
            {
                "target": e["target"],
                "bildname": e["bildname"],
                "media_slug": e["media_slug"],
                "ext": e["ext"],
                "width": e["width"],
                "height": e["height"],
                "is_cover": e["media_slug"] == meta["cover"]["media_slug"],
                "prompt_en": e["prompt_en"],
                # alt_de ist der wirksame Text, alt_source sagt woher er kommt.
                # Nur bei "missing" muss der Agent selbst einen schreiben, und
                # zwar allein fuer dieses Bild.
                "alt_de": aufloesung["alts"].get(e["media_slug"], ""),
                "alt_source": aufloesung["sources"][e["media_slug"]],
                "has_callout": e["callout_line"] is not None,
            }
            for e in meta["images"]
        ],
        "missing_alt": aufloesung["missing"],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


# ---------------------------------------------------------------------------
# write-alts
# ---------------------------------------------------------------------------

def textcheck_pfad(root: Path | None = None) -> Path | None:
    """`hk-text`, der Schreibregelpruefer des Harness.

    Er lag frueher als gespiegelter Skill im Vault, und ein Vault ohne diesen
    Spiegel blieb ungeprueft. Jetzt gehoert er zum Werkzeugkasten.
    """
    pfad = Path(__file__).resolve().parents[3] / "bin" / "hk-text"
    return pfad if pfad.is_file() else None


def pruefe_gegen_regelsatz(root: Path, slug: str, text: str) -> None:
    """Prueft den Alt-Text als freistehende Prosa gegen den Schreibregelsatz.

    Der Umweg ueber eine Wegwerfdatei ist noetig, weil der Pruefer Callouts
    ausnimmt: in einem ai-image-Callout steht der englische Prompt, und den auf
    deutsche Regeln zu pruefen waere Unsinn. Die Ausnahme trifft aber auch das
    alt-Feld, das mitten in diesem Blockquote steht. Ein Alt-Text bleibt damit
    ungeprueft, gleich ob ihn ein Skript oder ein Edit schreibt.

    Freistehend geprueft gilt fuer ihn wieder der volle Regelsatz, mit --gate
    also dieselbe Schwelle wie beim Hook.
    """
    pruefer = textcheck_pfad(root)
    if pruefer is None:
        return
    probe = scratch_dir() / ("alt-check-" + slugify(slug, 40) + ".md")
    try:
        probe.write_text(text + "\n", encoding="utf-8")
        proc = subprocess.run([sys.executable, str(pruefer), "--gate", str(probe)],
                              text=True, capture_output=True)
        if proc.returncode == 1:
            raise SystemExit(
                "FEHLER: der Alt-Text fuer " + slug + " verletzt die "
                "Schreibregeln, nichts geschrieben.\n" + proc.stdout.strip())
    finally:
        probe.unlink(missing_ok=True)


def pruefe_alt_text(root: Path, slug: str, text: str) -> None:
    text = text.strip()
    if not text:
        raise SystemExit("FEHLER: leerer Alt-Text fuer " + slug)
    if "\n" in text:
        raise SystemExit("FEHLER: Alt-Text fuer " + slug + " ist mehrzeilig")
    # Die harte Zeichenliste bleibt neben dem Regelsatz stehen. Sie greift auch
    # ohne erreichbaren Pruefer, und sie faengt die typografischen
    # Anfuehrungszeichen, die im gequoteten alt-Feld das Feld selbst zerlegen.
    for zeichen, name in VERBOTENE_ZEICHEN.items():
        if zeichen in text:
            raise SystemExit(
                "FEHLER: Alt-Text fuer " + slug + " enthaelt einen " + name
                + " (" + zeichen + "). Die Schreibregeln lassen in Prosa nur den "
                "ASCII-Bindestrich und ASCII-Anfuehrungszeichen zu.")
    pruefe_gegen_regelsatz(root, slug, text)


def cmd_write_alts(root: Path, args):
    """Schreibt Alt-Texte in die zugehoerigen Callouts der Notiz zurueck.

    Ohne diesen Schritt lebte ein beim Publish erzeugter Alt-Text nur in der
    alts.json und muesste beim naechsten Lauf neu erfunden werden. Der Vault ist
    die Quelle, nicht das Bundle.

    Bewusst ein eigenes Kommando und kein Seiteneffekt von build: der Uebergabe-
    weg --alts von build bleibt damit die reine Abweichung fuer einen einzelnen
    Publish, ohne die Notiz zu ueberstimmen.
    """
    meta = prepare(root, args.note)
    neue = load_alts(args.alts)
    if not neue:
        raise SystemExit("FEHLER: keine Alt-Texte uebergeben")

    lines = meta["path"].read_text(encoding="utf-8").split("\n")
    # collect_images zaehlt ab Body-Anfang, geschrieben wird in die ganze Datei.
    fm_len = len(lines) - len(meta["body"].split("\n"))

    unbekannt = sorted(set(neue) - {e["media_slug"] for e in meta["images"]})
    if unbekannt:
        raise SystemExit("FEHLER: kein Bild zu diesen Slugs: " + ", ".join(unbekannt))

    # Von hinten nach vorn, sonst verschieben die Einfuegungen die noch
    # ausstehenden Zeilennummern.
    aufgaben = []
    for emb in meta["images"]:
        text = (neue.get(emb["media_slug"]) or "").strip()
        if not text:
            continue
        pruefe_alt_text(root, emb["media_slug"], text)
        if emb["callout_line"] is None:
            raise SystemExit(
                "FEHLER: zu " + emb["target"] + " gehoert kein ai-image-Callout. "
                "Ein Alt-Text braucht ein Ziel im Vault, siehe Befund "
                "alt-quelle-fehlt. Erst den Callout nachtragen.")
        aufgaben.append((emb["callout_line"] + fm_len, text, emb))
    if not aufgaben:
        print("Nichts zu schreiben.")
        return 0

    geschrieben = []
    for marker, text, emb in sorted(aufgaben, key=lambda a: a[0], reverse=True):
        if not re.match(r"^>\s*\[!ai-image\]", lines[marker]):
            raise SystemExit(
                "FEHLER: erwartete einen ai-image-Callout in Zeile "
                + str(marker + 1) + ", gefunden: " + lines[marker].strip())
        callout = parse_callout(lines, marker)
        zeile = "> alt: " + yaml_scalar(text)
        if callout["alt_line"] is not None:
            lines[callout["alt_line"]] = zeile
        elif callout["head_lines"]:
            lines.insert(marker + 1, zeile)
        else:
            # Ohne vorhandenen Kopf braucht der Prompt eine Trennzeile, sonst
            # zaehlte seine erste Zeile beim naechsten Lesen zum Kopf.
            lines[marker + 1:marker + 1] = [zeile, ">"]
        geschrieben.append((emb["media_slug"], text))

    meta["path"].write_text("\n".join(lines), encoding="utf-8")
    print("Alt-Texte zurueckgeschrieben in " + rel_to_root(meta["path"], root) + ":")
    for slug, text in geschrieben:
        print("  - " + slug + ": " + text)
    return 0


# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------

def scratch_dir() -> Path:
    base = os.environ.get("CLAUDE_SCRATCHPAD")
    if base and Path(base).is_dir():
        return Path(base)
    return Path(os.environ.get("TMPDIR", "/tmp"))





def gate_dateien(meta) -> list:
    """Welche Notizen der Gate prueft.

    Essay, Titelstory und Bild der Woche bringen genau eine mit. Eine
    Publikation bringt sich selbst und jedes Kapitel ihres
    Inhaltsverzeichnisses mit, ausser den mit hennibock_skip markierten -- die
    erscheinen nie auf HenniBock und muessen deshalb auch nicht bestehen.

    Ein Punkt, dessen Kapitelnotiz es noch nicht gibt, faellt weg statt zu
    scheitern: Er ist ein angekuendigtes Kapitel und kein fehlerhafter Text.
    """
    dateien = [meta["path"]]
    if meta["type"] != PUBLICATION_TYPE:
        return dateien

    index = meta["index"]
    for stem in publication_order(meta["path"]):
        if is_skipped(index, stem):
            continue
        kapitel = index.get(nfc(stem))
        if kapitel and kapitel.is_file():
            dateien.append(kapitel)
    return dateien


def gate(root: Path, meta) -> None:
    """Vor der Bundle-Erzeugung: keiner der enthaltenen Texte darf einen Befund
    der Severity error tragen.

    Er verhaelt sich wie die Pruefung auf einen leeren summary: Abbruch mit
    FEHLER: und Befundliste, kein Bundle, kein Versand. Er laeuft am Anfang von
    cmd_build, damit im Fehlerfall kein Artefakt im Scratchpad zurueckbleibt.

    Geprueft wird gegen `hk-text --gate`. Nur error blockiert; eine Warnung
    erscheint im Bericht und haelt nichts auf. Ob ein Text nach KI klingt, ist
    ein Urteil und kein Messwert -- das beurteilt humanize, und es verhindert
    keine Publikation.
    """
    pruefer = textcheck_pfad()
    if pruefer is None:
        raise SystemExit(
            "FEHLER: `hk-text` ist nicht erreichbar. Ohne den Pruefer wird "
            "nicht publiziert. Ein Gate, das sich still abschaltet, ist "
            "schlechter als keins.")

    dateien = gate_dateien(meta)
    proc = subprocess.run(
        [sys.executable, str(pruefer), "--gate", *[str(d) for d in dateien]],
        text=True, capture_output=True,
    )
    if proc.returncode == 0:
        print("Textpruefung bestanden: " + str(len(dateien)) + " Notiz(en).")
        return

    befunde = (proc.stdout or "").strip()
    fehlerstrom = (proc.stderr or "").strip()
    raise SystemExit(
        "FEHLER: Die Textpruefung hat Befunde der Severity error gemeldet. Es "
        "wurde kein Bundle gebaut und nichts gesendet.\n"
        + (befunde + "\n" if befunde else "")
        + (fehlerstrom + "\n" if fehlerstrom else "")
        + "Die Befunde beheben und erneut bauen. Warnungen halten nichts auf, "
          "nur error blockiert.")


def cmd_build(root: Path, args):
    meta = prepare(root, args.note, redate=args.redate)

    # Der Gate steht am Anfang der einzigen Engstelle: ein Bundle entsteht
    # ausschliesslich hier, und send_bundle wird ausschliesslich von hier
    # gerufen. Wer eine neue Publikationsroute baut, ruft cmd_build auf und
    # legt keinen zweiten Bundle-Bau daneben.
    gate(root, meta)

    aufloesung = resolve_alts(meta["images"], load_alts(args.alts))
    alts = aufloesung["alts"]
    if aufloesung["missing"]:
        raise SystemExit(
            "FEHLER: Alt-Text fehlt fuer: " + ", ".join(aufloesung["missing"])
            + ". Der Text steht im alt-Feld des Callouts. Fehlt er dort, ihn "
            "schreiben und mit write-alts zurueckschreiben, danach erneut bauen.")

    doc_body = rewrite_body(meta["body"], root, meta["index"], meta["images"],
                            meta["cover"]["media_slug"], alts, meta["type"],
                            meta["beruehrt"])
    frontmatter = build_document_frontmatter({
        "title": meta["title"],
        "summary": meta["summary"], "author": meta["author"],
        "published": meta["published"], "areas": meta["areas"],
        "cover_slug": meta["cover"]["media_slug"],
        "tags": meta["tags"],
    })
    document = frontmatter + "\n\n" + doc_body + "\n"

    # Der Pfad im ZIP ist ein reiner Transportpfad: er traegt die Identitaet,
    # nicht die spaetere Adresse. Die vergibt der Server aus slug_base.
    doc_path = meta["type"] + "/" + meta["ref"] + ".md"
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "bundle_id": str(uuid.uuid4()),
        "created": date.today().isoformat(),
        "generator": GENERATOR,
        "documents": [{
            "path": doc_path,
            "type": meta["type"],
            "document_ref": meta["ref"],
            "slug_base": meta["slug_base"],
            # Nur auf ausdrueckliche Ansage. Ohne sie behaelt ein bekanntes
            # Dokument sein Datum: wann ein Beitrag erschienen ist, aendert
            # sich nicht dadurch, dass jemand einen Tippfehler behebt.
            **({"update_published": True} if args.redate else {}),
        }],
    }

    bundle_path = scratch_dir() / (meta["slug_base"] + ".hbbundle")
    with zipfile.ZipFile(bundle_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
        zf.writestr(doc_path, document)
        cover_slug = meta["cover"]["media_slug"]
        for emb in meta["images"]:
            arc_img = "image/" + emb["media_slug"] + emb["ext"]
            zf.write(emb["source"], arc_img)
            # Sidecar nur fuers Cover, siehe build_sidecar.
            if emb["media_slug"] == cover_slug:
                sidecar = build_sidecar(alts[emb["media_slug"]],
                                        emb["width"], emb["height"])
                zf.writestr("image/" + emb["media_slug"] + ".json",
                            json.dumps(sidecar, ensure_ascii=False))

    rel_bundle = bundle_path
    print("Bundle: " + str(rel_bundle))
    print("Dokument: " + meta["type"] + "/" + meta["ref"])
    print("slug_base: " + meta["slug_base"] + " (die Adresse vergibt der Server)")
    print("Cover: image/" + meta["cover"]["media_slug"])
    print("Bilder: " + str(len(meta["images"])))
    if meta["changed"]:
        print("Identitaet zurueckgeschrieben: hennibock_ref=" + meta["ref"]
              + ", hennibock_published=" + meta["published"])
    if meta["beruehrt"]:
        # Der Lauf hat fremde Notizen geaendert. Das steht deshalb sichtbar in
        # der Ausgabe und nicht nur im Vault.
        print("UUID in referenzierten Notizen angelegt:")
        for pfad in meta["beruehrt"]:
            print("  - " + pfad)

    if args.send and not args.validate_only:
        rc = send_bundle(bundle_path)
        if rc != 0:
            return rc
        # Der Import ist durch. Damit ist der Beitrag auf der Instanz, aber
        # noch nicht gesagt, dass ihn seine Publikation kennt. Siehe Abschnitt
        # Einhaengung in die Publikation.
        return nach_dem_senden(root, meta, reparieren=not args.no_repair)
    if args.send or args.validate_only:
        return send_bundle(bundle_path, validate_only=True)
    print("Nicht gesendet (kein --send).")
    return 0


def _post_bundle(endpoint: str, token: str, bundle_path: Path):
    """Schickt das Bundle und liefert (http_code, body). curl streamt die Datei
    vom Dateisystem: sie laeuft nie durch den Agenten."""
    proc = subprocess.run(
        [
            "curl", "-sS", "-w", "\n%{http_code}", "-X", "POST",
            "--data-binary", "@" + str(bundle_path),
            "-H", "Authorization: Bearer " + token,
            "-H", "Content-Type: application/zip",
            endpoint,
        ],
        text=True, capture_output=True,
    )
    if proc.returncode != 0:
        print("FEHLER: curl fehlgeschlagen: " + proc.stderr.strip(), file=sys.stderr)
        return None, None
    parts = proc.stdout.rsplit("\n", 1)
    return (parts[1].strip() if len(parts) > 1 else "?"), parts[0]


def _summarize(payload) -> str:
    docs = payload.get("applied") or []
    media = payload.get("media") or []
    zeilen = [f"{len(docs)} Dokument(e), {len(media)} Medium/Medien"]
    for d in docs:
        zeilen.append(f"  {d.get('type')}/{d.get('public_slug')}")
    for m in media:
        zeilen.append(f"  image/{m.get('slug')}")
    return "\n".join(zeilen)


def ziel() -> tuple[str, str]:
    """(url, woher) der HenniBock-Instanz, in zwei Stufen.

    Erst `HENNIBOCK_URL`, dann die gemerkte Wahl aus `hk-publish --ziel`.
    **Geraten wird nie.** Es gibt keinen Standardwert: Ein falsch geratenes
    Ziel schriebe in eine fremde Instanz, und das faellt erst dort auf.

    Das Token bleibt in der Umgebung und wird nicht gemerkt. Eine Adresse ist
    Konfiguration, ein Token ist ein Geheimnis, und die gemerkte Wahl liegt
    unverschluesselt im Cache.
    """
    from .. import ablage
    url = (os.environ.get("HENNIBOCK_URL") or "").strip().rstrip("/")
    if url:
        return url, "HENNIBOCK_URL"
    url = str(ablage.gemerkt("hennibock_url") or "").strip().rstrip("/")
    if url:
        return url, "der gemerkten Wahl (hk-publish --ziel)"
    return "", ""


KEIN_ZIEL = ("FEHLER: kein HenniBock-Ziel. Kein Default, das Ziel wird nie "
             "geraten.\n  hk-publish --ziel <url>   merkt es für dieses Gerät\n"
             "  HENNIBOCK_URL=<url>       gilt für den einzelnen Aufruf und "
             "geht vor")


def send_bundle(bundle_path: Path, validate_only: bool = False) -> int:
    url, _woher = ziel()
    if not url:
        print(KEIN_ZIEL + "\nBundle nicht gesendet.", file=sys.stderr)
        return 1
    token = os.environ.get("HENNIBOCK_IMPORT_TOKEN")
    if not token:
        print("FEHLER: HENNIBOCK_IMPORT_TOKEN nicht gesetzt, Bundle nicht gesendet.",
              file=sys.stderr)
        return 1

    # 1. Pruefen. Die Route bricht vor dem ersten Schreibvorgang ab und sagt,
    #    was ein Import taete. Ein Bundle, das hier scheitert, wird gar nicht
    #    erst angewandt.
    code, body = _post_bundle(url + "/import/validate", token, bundle_path)
    if code is None:
        return 1

    # Ob die Route ueberhaupt existiert, entscheidet der Antwortkoerper und nicht
    # der Status. Eine Instanz ohne Pruefroute liefert 404 mit einer HTML-Seite,
    # und ein 404 allein hiesse sonst faelschlich "Bundle abgelehnt" -- damit
    # koennte eine aeltere Instanz gar nicht mehr beliefert werden.
    try:
        antwort = json.loads(body)
    except ValueError:
        antwort = None

    vorschau = None
    if antwort is not None and antwort.get("dry_run"):
        vorschau = antwort
        print("Pruefung bestanden:")
        print(_summarize(vorschau))
    elif antwort is not None and code.startswith("4"):
        # JSON mit einem Fehler: ein echter Formfehler des Bundles. Nicht senden.
        print("FEHLER: Die Pruefung hat das Bundle abgelehnt, es wurde nicht "
              "importiert.", file=sys.stderr)
        print("HTTP " + code + " von " + url + "/import/validate", file=sys.stderr)
        print(json.dumps(antwort, ensure_ascii=False), file=sys.stderr)
        return 1
    else:
        # Kein JSON: die Instanz kennt die Route noch nicht. Das ist kein Grund,
        # das Publizieren zu verweigern -- es ging vorher auch ohne.
        print("WARNUNG: " + url + "/import/validate hat nicht wie erwartet "
              "geantwortet (HTTP " + code + ", kein JSON). Dort laeuft "
              "vermutlich noch ein aelteres Image ohne die Pruefroute. Es wird "
              "ohne Vorpruefung importiert.", file=sys.stderr)

    if validate_only:
        print("Nur geprueft (--validate-only), nichts importiert.")
        return 0

    # 2. Anwenden.
    endpoint = url + "/import"
    code, body = _post_bundle(endpoint, token, bundle_path)
    if code is None:
        return 1
    print("HTTP " + code + " von " + endpoint)
    print(body)
    if not code.startswith("2"):
        return 1

    # 3. Gegenlesen. Weicht das Ergebnis von der Vorschau ab, hat sich zwischen
    #    Pruefung und Import etwas geaendert -- das gehoert gesagt, nicht
    #    verschwiegen.
    if vorschau is not None:
        try:
            ergebnis = json.loads(body)
        except ValueError:
            ergebnis = None
        if ergebnis is not None:
            erwartet = {(d.get("type"), d.get("public_slug")) for d in vorschau.get("applied", [])}
            bekommen = {(d.get("type"), d.get("public_slug")) for d in ergebnis.get("applied", [])}
            if erwartet != bekommen:
                print("WARNUNG: Der Import weicht von der Vorschau ab. "
                      "Erwartet " + str(sorted(erwartet)) + ", bekommen "
                      + str(sorted(bekommen)) + ".", file=sys.stderr)
    return 0


# ---------------------------------------------------------------------------
# Einhaengung in die Publikation
# ---------------------------------------------------------------------------
#
# Ein Kapitel wird nicht dadurch Teil seines Werks, dass es publiziert ist.
# HenniBock leitet die document_chapters einer Publikation aus den
# henni://document-Zielen ihres Inhaltsverzeichnisses ab, und dieses
# Verzeichnis steht so auf dem Server, wie es beim letzten Import ihres Bodys
# aussah. Ein Punkt, der damals schon eine UUID trug, loest sich spaeter von
# selbst ein; ein Punkt, der erst danach ins Verzeichnis kam, existiert dort
# gar nicht und wird von keinem Kapitel-Publish nachgezogen.
#
# Genau das ist am 21.08.2026 mit "Die Freisprecheinrichtung" passiert: die
# Titelstory lag als eigener Beitrag auf der Instanz, und die Werksseite von
# "Geschichten von Henriette Einstein" kannte sie nicht. Aufgefallen ist es
# von Hand, Tage spaeter.
#
# Deshalb prueft jeder Publish-Lauf am Ende selbst nach und zieht die
# Publikation nach, wenn sie den Punkt noch nicht traegt. Das ist kein
# Nachtrag auf Verdacht -- die Pub-Datei geht nur an den Server, wenn der
# Server selbst gesagt hat, dass ihr der Punkt fehlt.


def server_url() -> str:
    url = (os.environ.get("HENNIBOCK_URL") or "").rstrip("/")
    if not url:
        raise SystemExit(
            "FEHLER: HENNIBOCK_URL nicht gesetzt. Ob ein Beitrag in seiner "
            "Publikation haengt, steht auf dem Server und nicht im Vault.")
    return url


_dokumente = None


def dokumente_vom_server(neu_laden: bool = False):
    """Was auf der Instanz liegt: document_ref -> Datensatz, einmal je Lauf.

    Der Server ist die einzige verlaessliche Auskunft darueber, was
    veroeffentlicht ist. Die Frontmatter taugt dafuer nicht: hennibock_ref
    traegt auch ein blosses Verweisziel, das nie publiziert wurde, und
    hennibock_published setzt schon ein analyze, lange bevor ein Import
    ueberhaupt versucht wird.
    """
    global _dokumente
    if _dokumente is not None and not neu_laden:
        return _dokumente
    url = server_url()
    try:
        with urllib.request.urlopen(url + "/documents", timeout=20) as r:
            daten = json.loads(r.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, ValueError) as e:
        raise SystemExit("FEHLER: Bestand von " + url + " nicht abfragbar: " + str(e))
    docs = daten if isinstance(daten, list) else daten.get("documents", [])
    _dokumente = {d["document_ref"]: d for d in docs if d.get("document_ref")}
    return _dokumente


def punkt_bedienbar(pub_slug: str, kap_typ: str, kap_slug: str):
    """Kennt die Publikation dieses Kapitel als Verzeichnispunkt mit Ziel?

    Die Auskunft gibt der Endpunkt, der das Kapitel auf der Werksseite
    aufklappt. Er antwortet nur, wenn das Kapitel in den document_chapters der
    Publikation steht, und genau die entstehen beim Import ihres Bodys. Ein 404
    heisst also: der Punkt trug beim letzten Import kein Ziel.
    """
    q = urllib.parse.quote
    url = (server_url() + "/api/publication/" + q(pub_slug)
           + "/chapter/" + q(kap_typ) + "/" + q(kap_slug))
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return r.status == 200, url
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False, url
        raise SystemExit("FEHLER: " + url + " antwortet HTTP " + str(e.code))
    except (urllib.error.URLError, OSError) as e:
        raise SystemExit("FEHLER: " + url + " nicht abfragbar: " + str(e))


def ist_publikation(path: Path) -> bool:
    """Traegt diese Notiz selbst hennibock_type: publication?

    Eine Pub-Datei ohne dieses Feld ist eine Gliederung des Vaults und kein
    Werk auf HenniBock. Sie kann dort keine Kapitel fuehren, denn sie liegt
    dort gar nicht.
    """
    try:
        fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        return False
    return frontmatter_value(fm, "hennibock_type") == PUBLICATION_TYPE


def publikationsnotizen(index) -> list:
    """Jede Notiz des Vaults, die selbst eine Publikation ist.

    Gesucht wird ueber hennibock_type und nicht ueber einen Dateinamen oder
    einen Ordner. Ein gemeinsamer Skill kennt die Ablage eines Vaults nicht,
    und die beiden bestehenden Vaults legen ihre Werke verschieden ab: einmal
    die Kapitel neben ihrer Pub-Datei, einmal die Texte in einem eigenen
    Ordner weit weg von ihr.
    """
    return sorted(path for path in index.values() if ist_publikation(path))


def publikationen_der_notiz(index, path: Path, fm_lines):
    """(traegt, genannt) -- wer diese Notiz als Kapitel fuehrt.

    Massgeblich ist das Inhaltsverzeichnis, denn genau daraus leitet HenniBock
    seine Kapitel ab. Die Property `publications` der Notiz ist nur die Absicht
    des Autors und keine zweite Wahrheit: weicht sie ab, ist das ein Befund und
    kein Grund, ihr zu folgen.

    Der Abgleich laeuft ueber den Dateinamen und kennt kein Typ-Praefix. Die
    Kapitel des einen Vaults heissen "Kap - ...", die des anderen "Text - ...",
    und eine Pruefung, die nur das eine kennt, meldet dem anderen Vault jedes
    Kapitel als nicht im Verzeichnis stehend.
    """
    stem = nfc(path.stem)
    genannt = []
    for name in frontmatter_list(fm_lines, "publications"):
        ziel = index.get(nfc(strip_wikilink(unquote(name))))
        if ziel and ziel.is_file() and ziel != path:
            genannt.append(ziel)
    if is_skipped(index, path.stem):
        # Ein uebersprungenes Kapitel faellt beim Publizieren der Publikation
        # ganz aus dem Verzeichnis. Dass es nirgends haengt, ist die Absicht.
        return [], genannt
    traegt = []
    for pub in publikationsnotizen(index):
        if pub == path:
            continue
        if stem in {nfc(s) for s in publication_order(pub)}:
            traegt.append(pub)
    return traegt, genannt


ABHILFE = {
    "punkt-ohne-ziel":
        "Die Notiz ist juenger als der zuletzt importierte Body der "
        "Publikation, ihr Verzeichnispunkt trug deshalb kein Ziel. Die "
        "Pub-Datei einmal erneut senden, ohne --redate.",
    "publikation-fehlt-auf-server":
        "Der Container liegt nicht auf der Instanz, es gibt also gar keine "
        "Kapitel. Die Pub-Datei einmal publizieren.",
    "nicht-im-inhaltsverzeichnis":
        "Die Notiz nennt die Publikation, deren Inhaltsverzeichnis sie aber "
        "nicht. Ein Re-Import haengt nichts ein, was dort fehlt -- der "
        "Verzeichniseintrag ist eine Autorenentscheidung.",
    "kapitel-fehlt-auf-server":
        "Der Beitrag selbst liegt nicht auf der Instanz. Erst ihn publizieren.",
    "publikation-ohne-hennibock-typ":
        "Die genannte Publikation traegt kein hennibock_type: publication und "
        "erscheint deshalb nie auf HenniBock. Ein Kapitel kann in einem Werk "
        "nicht haengen, das dort nicht liegt. Entweder die Pub-Datei fuer "
        "HenniBock einrichten und publizieren, oder die Zugehoerigkeit gilt "
        "allein im Vault.",
}

# Ein Befund, der den Lauf nicht scheitern laesst. Dass eine Pub-Datei kein
# Werk auf HenniBock ist, ist eine Entscheidung des Autors und kein Fehler des
# Publish-Laufs; es gehoert gesagt und nicht bestraft.
NUR_HINWEIS = ("publikation-ohne-hennibock-typ",)


def einhaengung_pruefen(index, path: Path):
    """Haengt diese Notiz in jeder Publikation, die sie fuehrt?

    `eingehaengt` ist None, wenn keine Publikation sie fuehrt und auch keine
    genannt ist -- ein Essay fuer sich ist kein Fehlerfall.
    """
    fm_lines, _ = split_frontmatter(path.read_text(encoding="utf-8"))
    traegt, genannt = publikationen_der_notiz(index, path, fm_lines)
    kap_ref = frontmatter_value(fm_lines, "hennibock_ref")

    bericht = {
        "eingehaengt": None,
        "chapter": path.stem,
        "publication": None,
        "pubfile": None,
        "endpunkt": None,
        "befund": None,
        "abhilfe": None,
        "publikationen": [],
    }

    if not traegt:
        if genannt:
            # Die Notiz behauptet eine Zugehoerigkeit, die kein
            # Inhaltsverzeichnis deckt. Das faellt sonst niemandem auf, denn
            # auf HenniBock fehlt dann einfach ein Punkt, den dort nie jemand
            # vermisst. Zwei Gruende sind zu unterscheiden: die Pub-Datei ist
            # gar kein HenniBock-Werk, oder sie ist eins und fuehrt die Notiz
            # nicht.
            ohne_typ = [g for g in genannt if not ist_publikation(g)]
            quelle = ohne_typ[0] if ohne_typ else genannt[0]
            befund = ("publikation-ohne-hennibock-typ" if ohne_typ
                      else "nicht-im-inhaltsverzeichnis")
            bericht.update({
                "eingehaengt": False,
                "publication": quelle.stem,
                "pubfile": quelle.name,
                "befund": befund,
                "abhilfe": ABHILFE[befund],
            })
        return bericht

    docs = dokumente_vom_server()
    kap_doc = docs.get(kap_ref) if kap_ref else None

    for pub in traegt:
        fm_pub, _ = split_frontmatter(pub.read_text(encoding="utf-8"))
        pub_ref = frontmatter_value(fm_pub, "hennibock_ref")
        pub_doc = docs.get(pub_ref) if pub_ref else None

        eintrag = {"publication": pub.stem, "pubfile": pub.name,
                   "eingehaengt": False, "endpunkt": None,
                   "befund": None, "abhilfe": None}
        if kap_doc is None:
            eintrag["befund"] = "kapitel-fehlt-auf-server"
        elif pub_doc is None:
            eintrag["befund"] = "publikation-fehlt-auf-server"
        else:
            ok, endpunkt = punkt_bedienbar(pub_doc["slug"], kap_doc["type"],
                                           kap_doc["slug"])
            eintrag["eingehaengt"] = ok
            eintrag["endpunkt"] = endpunkt
            if not ok:
                eintrag["befund"] = "punkt-ohne-ziel"
        if eintrag["befund"]:
            eintrag["abhilfe"] = ABHILFE[eintrag["befund"]]
        bericht["publikationen"].append(eintrag)

    offen = [e for e in bericht["publikationen"] if not e["eingehaengt"]]
    erste = offen[0] if offen else bericht["publikationen"][0]
    bericht.update({
        "eingehaengt": not offen,
        "publication": erste["publication"],
        "pubfile": erste["pubfile"],
        "endpunkt": erste["endpunkt"],
        "befund": erste["befund"],
        "abhilfe": erste["abhilfe"],
    })
    return bericht


# Die beiden Befunde, die ein erneuter Import der Publikation aus der Welt
# schafft. Der dritte, nicht-im-inhaltsverzeichnis, tut es ausdruecklich nicht:
# ein Re-Import haengt nichts ein, was im Verzeichnis fehlt, und den Eintrag
# setzt der Autor und nicht dieses Skript.
REPARIERBAR = ("punkt-ohne-ziel", "publikation-fehlt-auf-server")


def _publiziere_publikation(root: Path, pubfile: Path) -> int:
    """Die Pub-Datei erneut senden, ohne --redate und ohne eigene Reparatur.

    Ohne --redate, weil das Erscheinungsdatum der Publikation stehen bleibt:
    Ein nachgezogenes Verzeichnis ist keine Neuveroeffentlichung des Werks.
    """
    args = argparse.Namespace(note=str(pubfile), alts=None, send=True,
                              validate_only=False, redate=False, no_repair=True)
    try:
        return cmd_build(root, args)
    except SystemExit as e:
        # Der Beitrag selbst ist an dieser Stelle schon publiziert. Ein
        # Abbruch der Publikation darf ihn nicht als gescheitert erscheinen
        # lassen, aber auch nicht stillschweigend durchgehen.
        print(str(e.code), file=sys.stderr)
        return 1


def nach_dem_senden(root: Path, meta, reparieren: bool) -> int:
    """Nach einem erfolgreichen Import: haengt der Beitrag in seinem Werk?

    Diese Pruefung ist der Grund, warum der Lauf ueberhaupt weiterlaeuft,
    nachdem der Server 200 gesagt hat. Ein 200 belegt, dass der Beitrag auf der
    Instanz liegt -- nicht, dass ihn dort jemand findet.
    """
    bericht = einhaengung_pruefen(meta["index"], meta["path"])

    if bericht["eingehaengt"] is None:
        return 0
    if bericht["eingehaengt"]:
        for e in bericht["publikationen"]:
            print("Eingehaengt in: " + e["publication"])
        return 0

    nachgezogen = []
    if reparieren:
        for e in bericht["publikationen"]:
            if e["befund"] not in REPARIERBAR:
                continue
            print("Die Publikation " + e["publication"] + " fuehrt diesen "
                  "Beitrag noch nicht (" + e["befund"] + "). Sie wird "
                  "nachgezogen.")
            pubfile = meta["index"].get(nfc(e["publication"]))
            if pubfile is None or _publiziere_publikation(root, pubfile) != 0:
                print("FEHLER: " + e["publication"] + " konnte nicht "
                      "nachgezogen werden.", file=sys.stderr)
                continue
            nachgezogen.append(e["publication"])
        if nachgezogen:
            dokumente_vom_server(neu_laden=True)
            bericht = einhaengung_pruefen(meta["index"], meta["path"])
            if bericht["eingehaengt"]:
                for e in bericht["publikationen"]:
                    print("Eingehaengt in: " + e["publication"])
                return 0

    offen = [e for e in (bericht["publikationen"] or [bericht])
             if not e.get("eingehaengt")]
    if all(e.get("befund") in NUR_HINWEIS for e in offen):
        for e in offen:
            print("WARNUNG: " + str(e.get("publication")) + ": "
                  + str(e.get("befund")), file=sys.stderr)
            print("  " + str(e.get("abhilfe")), file=sys.stderr)
        return 0

    print("FEHLER: Der Beitrag ist importiert, haengt aber nicht in seiner "
          "Publikation. Der Import selbst ist gelungen -- ein zweiter Lauf "
          "wiederholt ihn nur, er haengt ihn nicht ein.", file=sys.stderr)
    for e in offen:
        print("  " + str(e.get("publication")) + ": " + str(e.get("befund")),
              file=sys.stderr)
        print("  " + str(e.get("abhilfe")), file=sys.stderr)
    return 1


def cmd_attached(root: Path, args):
    """Die Pruefung fuer sich, ohne zu publizieren."""
    index = build_note_index(root)
    path = locate_note(root, args.note, index)
    if path is None:
        raise SystemExit("FEHLER: Notiz nicht gefunden: " + args.note)
    bericht = einhaengung_pruefen(index, path)
    print(json.dumps(bericht, ensure_ascii=False, indent=2))
    # None heisst: keine Publikation fuehrt diese Notiz. Das ist kein Fehler,
    # sondern ein Essay fuer sich. Ein blosser Hinweis ebenso wenig.
    if bericht["eingehaengt"] is not False:
        return 0
    return 0 if bericht["befund"] in NUR_HINWEIS else 1


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv):
    parser = argparse.ArgumentParser(prog="hennibock_publish.py")
    sub = parser.add_subparsers(dest="command", required=True)

    p_an = sub.add_parser("analyze", help="Notiz pruefen und Metadaten ausgeben")
    p_an.add_argument("note")
    p_an.add_argument("--alts", help="JSON-Datei media_slug -> Alt-Text, "
                                     "nur um Overrides schon hier zu sehen")

    p_wa = sub.add_parser("write-alts",
                          help="Alt-Texte in die Callouts der Notiz zurueckschreiben")
    p_wa.add_argument("note")
    p_wa.add_argument("--alts", required=True,
                      help="JSON-Datei media_slug -> Alt-Text")

    p_bu = sub.add_parser("build", help="Bundle bauen und optional senden")
    p_bu.add_argument("note")
    p_bu.add_argument("--alts", help="JSON-Datei media_slug -> Alt-Text. Override "
                                     "fuer diesen Publish, nicht zurueckgeschrieben")
    p_bu.add_argument("--send", action="store_true", help="Bundle an HenniBock senden")
    p_bu.add_argument(
        "--validate-only",
        action="store_true",
        help="Nur gegen /import/validate pruefen und melden, was ein Import "
             "taete. Schreibt nichts.",
    )
    p_bu.add_argument(
        "--redate",
        action="store_true",
        help="Veroeffentlichungsdatum auf heute setzen. Ohne diese Ansage "
             "behaelt ein bereits publizierter Beitrag sein Datum.",
    )
    p_bu.add_argument(
        "--no-repair",
        action="store_true",
        help="Die Publikation nach dem Import nicht nachziehen, auch wenn sie "
             "den Beitrag nicht fuehrt. Der Lauf meldet den Befund dann nur.",
    )

    p_at = sub.add_parser(
        "attached",
        help="Prueft, ob eine Notiz in den Publikationen haengt, die sie fuehren")
    p_at.add_argument("note")

    for unter in (p_an, p_wa, p_bu, p_at):
        unter.add_argument("--ablage", help="Pfad zur Wissensbasis; sonst gilt "
                                            "die aktive (siehe hk-ablage)")
    args = parser.parse_args(argv[1:])
    root = vault_root(getattr(args, "ablage", None))
    if args.command == "analyze":
        return cmd_analyze(root, args)
    if args.command == "write-alts":
        return cmd_write_alts(root, args)
    if args.command == "build":
        return cmd_build(root, args)
    if args.command == "attached":
        return cmd_attached(root, args)
    parser.error("unbekanntes Kommando")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
