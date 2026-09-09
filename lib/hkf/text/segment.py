"""Segmentierung von Markdown für die Textprüfung.

Die einzige öffentliche Funktion ist ``mask``. Sie bekommt den Rohtext einer
Markdown-Datei und liefert eine Fassung gleicher Länge zurück, in der alle
nicht zu prüfenden Bereiche durch Leerzeichen ersetzt sind. Zeilenumbrüche
bleiben unangetastet, damit Zeilen- und Spaltennummern eines Befunds weiterhin
auf die Originaldatei zeigen.

Ignoriert werden:

* Code-Fences mit Backticks und mit Tilden, auch innerhalb von Callouts und
  eingerückt in einem Listenpunkt.
* Inline-Code, auch mit mehrfachen Backticks.
* Callouts, deren Typ mit ``ai-`` beginnt, samt aller Folgezeilen. Sie tragen
  englische Bildprompts. Jeder andere Callout wird geprüft. Ausgenommen von
  dieser Ausnahme ist der Wert einer ``alt:``-Zeile in ihrem Kopf: er ist
  deutsche Prosa und wird geprüft.
* Der Callout-Marker ``[!typ]`` selbst, denn er ist Syntax und keine Prosa.
* Ziele von Markdown-Links und Bildern.
* Wikilink-Ziele, sofern sie kebab-case sind oder wie ein Pfad aussehen. Ein
  gewöhnlicher Notizname bleibt stehen, weil er deutsche Prosa ist.
* Frontmatter-Werte, die Bezeichner, Pfade oder Adressen tragen.

Geprüft wird die übrige Frontmatter. ``summary``, ``name`` und ``description``
tragen deutsche Prosa und sind Text.

Nur Standardbibliothek.
"""

from __future__ import annotations

import re

# Callout-Typen mit diesem Präfix werden nicht geprüft.
AI_CALLOUT_PREFIX = "ai-"
# Die einzige Zeile in einem solchen Callout, deren Wert doch geprüft wird.
ALT_ZEILE = re.compile(r"^alt:[ \t]*(\S.*?)[ \t]*$")

# Frontmatter-Schlüssel, deren Wert ein Bezeichner und keine Prosa ist.
IDENTIFIER_KEYS = {
    "slug", "id", "uuid", "permalink", "cssclass", "cssclasses",
    "created", "modified", "date", "publish", "pinned", "position",
}
IDENTIFIER_SUFFIXES = ("_ref", "_path", "_url", "_id", "_slug", "_type", "_skip")

CALLOUT_HEAD = re.compile(r"^(\[!([A-Za-z0-9_-]+)\][+-]?)")
# Ein Fence darf eingerückt stehen, etwa in einem Listenpunkt. Die Einrückung
# des Öffners und die des Schlusszeichens müssen nicht übereinstimmen.
FENCE_HEAD = re.compile(r"^[ \t]*(`{3,}|~{3,})")
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)+$")
FRONTMATTER_KEY = re.compile(r"^\s*(?:-\s*)?([A-Za-z_][A-Za-z0-9_]*)\s*:\s*")
FRONTMATTER_ITEM = re.compile(r"^\s*-\s+(\S.*?)\s*$")
SCALAR = re.compile(r"^(true|false|null|~|-?\d+(\.\d+)?)$", re.IGNORECASE)
MD_LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]*)\)")
# Eine nackte Adresse im Fliesstext ist ein Bezeichner und keine Prosa.
BARE_URL = re.compile(r"<?\b(?:https?|henni)://[^\s<>)\]]+>?")
EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
WIKILINK = re.compile(r"!?\[\[([^\]\n|]*)(\|[^\]\n]*)?\]\]")
BACKTICK_RUN = re.compile(r"`+")

# Der Em-Dash ist in HKF Core an zwei Stellen Formatzeichen und nicht
# Gedankenstrich: als Trenner in `# Verbindungen` (§5.6) und als leere Vorgabe in
# einer Property-Tabelle (§3.7). Beides schreibt die Spezifikation vor, und die
# Werkzeuge setzen es selbst. Ein Regelsatz kann das nicht auffangen, weil
# `forbidden_characters` sich nicht senken laesst und `scope` nur Pfade kennt,
# keine Abschnitte.
EM_DASH = "\u2014"
# Der Trenner steht nach dem Wikilink und nur einmal je Eintrag (§5.6). Was
# dahinter kommt, ist der Grund, und der ist Prosa.
TRENNER = re.compile(r"(?:\]\]|\))\s*(\u2014)")
UEBERSCHRIFT = re.compile(r"^#{1,6}\s+\S")
SIEHE_AUCH = re.compile(r"^#{1,6}\s+Verbindungen\s*$")
TABELLENZEILE = re.compile(r"^\s*\|")


def mask(text: str) -> str:
    """Ersetzt alle nicht zu prüfenden Bereiche durch Leerzeichen."""
    chars = list(text)
    lines = _line_spans(text)
    fm_end = _frontmatter_end(text, lines)

    fence: str | None = None          # offener Fence, sonst None
    stack: list[tuple[int, str]] = []  # aktive Callouts als (Tiefe, Typ)
    siehe_auch = False                 # innerhalb des Abschnitts `# Verbindungen`
    ai_kopf = False                    # im Metadatenkopf eines `ai-`-Callouts

    for index, (start, end) in enumerate(lines):
        line = text[start:end]
        depth, offset = _quote_prefix(line)
        content = line[offset:]
        body = start + offset

        if fence is not None:
            _blank(chars, start, end)
            if _closes_fence(content, fence):
                fence = None
            continue

        opener = FENCE_HEAD.match(content)
        if opener:
            fence = opener.group(1)
            _blank(chars, start, end)
            continue

        if depth == 0:
            stack.clear()
            ai_kopf = False
        else:
            while stack and stack[-1][0] > depth:
                stack.pop()

        head = CALLOUT_HEAD.match(content) if depth > 0 else None
        if head:
            while stack and stack[-1][0] >= depth:
                stack.pop()
            stack.append((depth, head.group(2).lower()))
            # Der Marker ist Syntax, nie Prosa.
            _blank(chars, body, body + len(head.group(1)))
            ai_kopf = head.group(2).lower().startswith(AI_CALLOUT_PREFIX)

        if any(typ.startswith(AI_CALLOUT_PREFIX) for _, typ in stack):
            _blank(chars, start, end)
            if ai_kopf:
                _alt_wert(chars, text, body, content)
                # Die leere `>`-Zeile trennt den Kopf vom Prompt.
                if not content.strip():
                    ai_kopf = False
            continue

        if UEBERSCHRIFT.match(content):
            siehe_auch = bool(SIEHE_AUCH.match(content))
        if siehe_auch:
            _trenner(chars, body, content)
        elif TABELLENZEILE.match(content):
            _leere_zelle(chars, body, content)

        in_frontmatter = fm_end is not None and 0 < index < fm_end
        _mask_line(chars, text, body, content, in_frontmatter)

    return "".join(chars)


def _alt_wert(chars: list[str], text: str, body: int, content: str) -> None:
    """Nimmt den Wert einer `alt:`-Zeile von der Maskierung wieder aus.

    Ein `ai-`-Callout trägt einen englischen Bildprompt und bleibt deshalb
    ungeprüft. Sein `alt:`-Feld trägt aber deutsche Prosa, und ohne diese
    Rücknahme fiele es durch jedes Netz: der Schreibregel-Hook springt bei
    jedem Schreibzugriff an, überspringt jedoch den ganzen Callout. Genau so
    sind am 04.09.2026 die Ersatzformen eines Agenten unbemerkt durchgekommen.

    Geprüft wird nur der Kopf des Callouts, also die Zeilen vor der leeren
    `>`-Trennzeile. Was dahinter steht, ist der Prompt.
    """
    treffer = ALT_ZEILE.match(content)
    if not treffer:
        return
    for pos in range(body + treffer.start(1), min(body + treffer.end(1), len(chars))):
        chars[pos] = text[pos]


def _trenner(chars: list[str], body: int, content: str) -> None:
    """Der Trenner in `# Verbindungen` (§5.6), und nur er.

    Er folgt dem Verweis und kommt je Eintrag einmal vor. Der Verweis ist ein
    Wikilink oder eine Adresse (§5.6), endet also auf `]]` oder auf `)`. Der
    Grund dahinter ist deutsche Prosa und bleibt geprüft.
    """
    treffer = TRENNER.search(content)
    if treffer:
        _blank(chars, body + treffer.start(1), body + treffer.end(1))


def _leere_zelle(chars: list[str], body: int, content: str) -> None:
    """`—` als leere Vorgabe in einer Property-Tabelle (§3.7).

    Nur eine Zelle, die nichts anderes enthält. Die Beschreibungsspalte ist
    deutsche Prosa und bleibt geprüft.
    """
    pos = 0
    for stueck in content.split("|"):
        if stueck.strip() == EM_DASH:
            versatz = stueck.index(EM_DASH)
            _blank(chars, body + pos + versatz, body + pos + versatz + 1)
        pos += len(stueck) + 1


def _line_spans(text: str) -> list[tuple[int, int]]:
    """Anfang und Ende jeder Zeile, ohne den Zeilenumbruch."""
    spans = []
    start = 0
    for match in re.finditer(r"\n", text):
        spans.append((start, match.start()))
        start = match.end()
    spans.append((start, len(text)))
    return spans


def _frontmatter_end(text: str, lines: list[tuple[int, int]]) -> int | None:
    """Index der schliessenden ---Zeile, oder None ohne Frontmatter."""
    if not lines or text[lines[0][0]:lines[0][1]].rstrip() != "---":
        return None
    for index in range(1, len(lines)):
        if text[lines[index][0]:lines[index][1]].rstrip() == "---":
            return index
    return None


def _quote_prefix(line: str) -> tuple[int, int]:
    """Zitattiefe und Länge des Zitatpräfixes einer Zeile."""
    pos = 0
    while pos < len(line) and pos < 3 and line[pos] == " ":
        pos += 1
    depth = 0
    while pos < len(line) and line[pos] == ">":
        depth += 1
        pos += 1
        if pos < len(line) and line[pos] == " ":
            pos += 1
    return (depth, pos) if depth else (0, 0)


def _closes_fence(content: str, fence: str) -> bool:
    match = FENCE_HEAD.match(content)
    return bool(match and match.group(1)[0] == fence[0]
                and len(match.group(1)) >= len(fence))


def _blank(chars: list[str], start: int, end: int) -> None:
    for pos in range(start, min(end, len(chars))):
        if chars[pos] != "\n":
            chars[pos] = " "


def _mask_line(chars, text, body, content, in_frontmatter) -> None:
    """Maskiert Inline-Code, Linkziele und Bezeichner einer einzelnen Zeile."""
    code = _inline_code_spans(content)
    for begin, stop in code:
        _blank(chars, body + begin, body + stop)

    def free(begin: int) -> bool:
        return not any(a <= begin < b for a, b in code)

    for match in MD_LINK.finditer(content):
        if free(match.start()):
            _blank(chars, body + match.start(1), body + match.end(1))

    for muster in (BARE_URL, EMAIL):
        for match in muster.finditer(content):
            if free(match.start()):
                _blank(chars, body + match.start(), body + match.end())

    for match in WIKILINK.finditer(content):
        if not free(match.start()):
            continue
        target = match.group(1)
        if _is_identifier(target):
            _blank(chars, body + match.start(1), body + match.end(1))

    if in_frontmatter:
        key = FRONTMATTER_KEY.match(content)
        if key:
            wert = content[key.end():].strip().strip("\"'")
            if _is_identifier_key(key.group(1)) or _is_identifier(wert):
                _blank(chars, body + key.end(), body + len(content))
            return
        # Blosser Listeneintrag ohne Schluessel, etwa ein Tag.
        eintrag = FRONTMATTER_ITEM.match(content)
        if eintrag and _is_identifier(eintrag.group(1).strip().strip("\"'")):
            _blank(chars, body + eintrag.start(1), body + eintrag.end(1))


def _inline_code_spans(content: str) -> list[tuple[int, int]]:
    """Spannen von Inline-Code, Begrenzer eingeschlossen."""
    spans = []
    runs = list(BACKTICK_RUN.finditer(content))
    used = 0
    while used < len(runs):
        opener = runs[used]
        width = len(opener.group(0))
        closer = None
        for candidate in range(used + 1, len(runs)):
            if len(runs[candidate].group(0)) == width:
                closer = runs[candidate]
                used = candidate
                break
        if closer is None:
            break
        spans.append((opener.start(), closer.end()))
        used += 1
    return spans


def _is_identifier_key(key: str) -> bool:
    return key.lower() in IDENTIFIER_KEYS or key.lower().endswith(IDENTIFIER_SUFFIXES)


def _is_identifier(value: str) -> bool:
    """Wahr, wenn der Wert ein Bezeichner, ein Pfad oder eine Adresse ist."""
    value = value.strip()
    if not value:
        return False
    if value.startswith(("http://", "https://", "henni://")):
        return True
    if "/" in value:
        return True
    if KEBAB.match(value):
        return True
    if SCALAR.match(value):
        return True
    # Ein einzelnes kleingeschriebenes Wort in der Frontmatter ist ein Tag oder
    # ein Statuswert, keine Prosa. Ein grosser Anfangsbuchstabe spricht dagegen.
    if " " not in value and value == value.lower() and value.isalnum():
        return True
    return False
