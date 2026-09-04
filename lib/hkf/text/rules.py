"""Regel-Lader und Regelauflösung für die Textprüfung.

Ein Regelsatz steht als ``writing_policy`` in einer JSON-Datei oder in einem
``json``-Fence einer Markdown-Datei. Dieses Modul findet solche Fences, prüft
sie gegen ein festes Schema und entscheidet je Datei, welche Fassung einer
Prüfung gilt.

Ein Regelsatz mit einem Tippfehler ist gefährlicher als gar keiner, weil er
stillschweigend weniger prüft als gedacht. Jeder Verstoss gegen das Schema
führt deshalb zu einer ``RuleError`` und damit zum Abbruch, bevor eine einzige
Textdatei angefasst wird. Es gibt kein Überspringen.

Rangfolge, wenn mehrere Regelsätze dieselbe Prüfung nennen:

* Der Basissatz des Skills ist der Boden und hat den Rang -1.
* Ein Vault-Regelsatz ohne ``scope`` gilt vaultweit und hat den Rang 0.
* Ein Vault-Regelsatz mit passendem ``scope`` hat den Rang der Präfixlänge.

Der höchste Rang bestimmt die ``severity``. Die Datenlisten, also Zeichen,
Stämme und Phrasen, werden über alle zutreffenden Regelsätze vereinigt. So kann
ein Bereich eine Prüfung senken oder abschalten, ohne die Liste des Basissatzes
zu verlieren, und er kann sie ergänzen, ohne sie abzuschreiben. Bei einem
Skalar wie ``maximum_words`` gewinnt allein der höchste Rang.

Nur Standardbibliothek.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

# Die vollständige und geschlossene Liste der Prüfungen. Jede nennt ihr
# Datenfeld und dessen Typ. Ein Name ausserhalb dieser Liste ist ein Fehler.
CHECK_SCHEMA = {
    "forbidden_characters": ("characters", list),
    "forbidden_punctuation": ("characters", list),
    "umlaut_replacements": ("stems", list),
    "forbidden_phrases": ("phrases", list),
    "forbidden_stems": ("stems", list),
    "structural_phrases": ("phrases", list),
    "sentence_length": ("maximum_words", int),
}

# Ein Stamm trifft auch quer ueber eine Kompositionsfuge. "reissen" steckt in
# "Preissenkungen", "fuer" in "Fuerteventura". Beide sind richtig geschrieben.
# Solche Woerter stehen als Ausnahme im Regelsatz, damit der Stamm bleiben kann.
# Bei forbidden_stems gilt dasselbe fuer Sachbegriffe, die einen Verstaerker als
# Wortbestandteil tragen, etwa "Nachhaltigkeit".
OPTIONAL_FIELDS = {
    "umlaut_replacements": {"exceptions": list},
    "forbidden_stems": {"exceptions": list},
}

SEVERITIES = ("error", "warning", "off")

# K6: diese Prüfungen darf ein Vault-Regelsatz nicht senken.
PROTECTED = ("forbidden_characters", "umlaut_replacements")

POLICY_KEYS = ("version", "scope", "checks")

FENCE = re.compile(r"^(`{3,}|~{3,})[ \t]*([A-Za-z0-9_+-]*)[ \t]*$")

BASE_RANK = -1


class RuleError(Exception):
    """Ein Regelsatz verstösst gegen das Schema oder gegen K5 oder K6."""


class RuleSet:
    """Ein geprüfter ``writing_policy``-Block mit seiner Herkunft."""

    def __init__(self, origin: str, is_base: bool, scope, checks):
        self.origin = origin
        self.is_base = is_base
        self.scope = tuple(scope)
        self.checks = checks

    def rank(self, relative_path: str) -> int | None:
        """Rang für diese Datei, oder None wenn der Regelsatz nicht greift."""
        if self.is_base:
            return BASE_RANK
        if not self.scope:
            return 0
        treffer = [len(p) for p in self.scope if _under(relative_path, p)]
        return max(treffer) if treffer else None

    def __repr__(self) -> str:
        return f"RuleSet({self.origin!r})"


def load(path, is_base: bool = False) -> list[RuleSet]:
    """Liest alle Regelsätze einer JSON- oder Markdown-Datei."""
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as fehler:
        raise RuleError(f"{path}: nicht lesbar, {fehler}") from fehler

    if not text.strip():
        # Eine leere Datei ist kein Regelsatz, sondern ein Versehen. Sie legt
        # den Pruefer nicht lahm: bis zum 25.08.2026 brach eine leere .json im
        # Regelordner eines Vaults mit Exit 2 ab, und damit wurde gar nichts
        # mehr geprueft. Ein Regelsatz mit Inhalt, dem writing_policy fehlt,
        # bleibt ein Fehler.
        return []

    if path.suffix.lower() == ".json":
        bloecke = [(str(path), text)]
    else:
        # Nur Fences, die sich als Regelsatz ausgeben. Ein Doku-Beispiel in
        # einer Regeldatei darf den Pruefer nicht blockieren, ein kaputter
        # Regelsatz dagegen schon.
        bloecke = [(f"{path}, Fence {nummer}", roh)
                   for nummer, roh in enumerate(json_fences(text), start=1)
                   if "writing_policy" in roh]

    saetze = []
    for origin, roh in bloecke:
        daten = _parse(roh, origin)
        if not isinstance(daten, dict) or "writing_policy" not in daten:
            if path.suffix.lower() == ".json":
                raise RuleError(f"{origin}: kein Schlüssel writing_policy")
            continue
        saetze.append(_validate(daten["writing_policy"], origin, is_base))
    return saetze


def load_all(base_file, vault_rules_dir) -> list[RuleSet]:
    """Basissatz plus alle Regelsätze aus dem Regelverzeichnis des Vaults."""
    saetze = load(base_file, is_base=True)
    if not saetze:
        raise RuleError(f"{base_file}: enthält keinen Regelsatz")
    wurzel = Path(vault_rules_dir)
    if wurzel.is_dir():
        for datei in sorted(wurzel.rglob("*")):
            if datei.is_file() and datei.suffix.lower() in (".md", ".json"):
                saetze.extend(load(datei))
    return saetze


def resolve(rulesets: list[RuleSet], relative_path: str) -> dict:
    """Die für diese Datei geltende Fassung jeder Prüfung."""
    zutreffend = []
    for satz in rulesets:
        rang = satz.rank(relative_path)
        if rang is not None:
            zutreffend.append((rang, satz))

    _check_konflikte(zutreffend, relative_path)

    ergebnis = {}
    for name, (feld, typ) in CHECK_SCHEMA.items():
        quellen = [(rang, satz) for rang, satz in zutreffend if name in satz.checks]
        if not quellen:
            continue
        bester = max(quellen, key=lambda paar: paar[0])
        severity = bester[1].checks[name].get("severity", "error")
        if severity == "off":
            continue

        if typ is list:
            daten = _vereinigen(quellen, name, feld)
        else:
            daten = bester[1].checks[name].get(feld)

        if daten is None or (typ is list and not daten):
            raise RuleError(
                f"{bester[1].origin}: Prüfung {name} ist aktiv, aber {feld} "
                f"fehlt in allen zutreffenden Regelsätzen")

        eintrag = {"severity": severity, feld: daten, "origin": bester[1].origin}
        for zusatz in OPTIONAL_FIELDS.get(name, {}):
            eintrag[zusatz] = _vereinigen(quellen, name, zusatz)
        ergebnis[name] = eintrag
    return ergebnis


def _vereinigen(quellen, name: str, feld: str) -> list:
    """Listenfeld über alle zutreffenden Regelsätze vereinigen, Reihenfolge stabil."""
    werte, gesehen = [], set()
    for _, satz in sorted(quellen, key=lambda paar: paar[0]):
        for wert in satz.checks[name].get(feld, []):
            if wert not in gesehen:
                gesehen.add(wert)
                werte.append(wert)
    return werte


def json_fences(text: str) -> list[str]:
    """Inhalt aller json-Fences einer Markdown-Datei."""
    treffer, offen, gesammelt = [], None, []
    for zeile in text.split("\n"):
        kopf = FENCE.match(zeile)
        if offen is None:
            if kopf and kopf.group(2).lower() == "json":
                offen = kopf.group(1)
                gesammelt = []
            continue
        if kopf and kopf.group(1)[0] == offen[0] and len(kopf.group(1)) >= len(offen):
            treffer.append("\n".join(gesammelt))
            offen = None
            continue
        gesammelt.append(zeile)
    return treffer


def _parse(roh: str, origin: str):
    def kein_duplikat(paare):
        gesehen = set()
        for schluessel, _ in paare:
            if schluessel in gesehen:
                raise RuleError(f"{origin}: Schlüssel {schluessel!r} kommt zweimal vor")
            gesehen.add(schluessel)
        return dict(paare)

    try:
        return json.loads(roh, object_pairs_hook=kein_duplikat)
    except json.JSONDecodeError as fehler:
        raise RuleError(f"{origin}: kein gültiges JSON, {fehler}") from fehler


def _validate(policy, origin: str, is_base: bool) -> RuleSet:
    if not isinstance(policy, dict):
        raise RuleError(f"{origin}: writing_policy ist kein Objekt")

    for schluessel in policy:
        if schluessel not in POLICY_KEYS:
            raise RuleError(f"{origin}: unbekannter Schlüssel {schluessel!r}, "
                            f"erlaubt sind {', '.join(POLICY_KEYS)}")

    version = policy.get("version", 1)
    if version != 1:
        raise RuleError(f"{origin}: version {version!r} wird nicht unterstützt")

    scope = policy.get("scope", [])
    if not isinstance(scope, list) or any(
            not isinstance(p, str) or not p.strip() for p in scope):
        raise RuleError(f"{origin}: scope muss eine Liste nicht leerer Zeichenketten sein")

    checks = policy.get("checks", {})
    if not isinstance(checks, dict):
        raise RuleError(f"{origin}: checks ist kein Objekt")

    for name, regel in checks.items():
        if name not in CHECK_SCHEMA:
            raise RuleError(f"{origin}: unbekannte Prüfung {name!r}, erlaubt sind "
                            f"{', '.join(sorted(CHECK_SCHEMA))}")
        if not isinstance(regel, dict):
            raise RuleError(f"{origin}: Prüfung {name} ist kein Objekt")

        feld, typ = CHECK_SCHEMA[name]
        zusatz = OPTIONAL_FIELDS.get(name, {})
        erlaubt = ("severity", feld, *zusatz)
        for schluessel in regel:
            if schluessel not in erlaubt:
                raise RuleError(f"{origin}: Prüfung {name} kennt {schluessel!r} nicht, "
                                f"erlaubt sind {', '.join(erlaubt)}")

        severity = regel.get("severity", "error")
        if severity not in SEVERITIES:
            raise RuleError(f"{origin}: Prüfung {name} hat severity {severity!r}, "
                            f"erlaubt sind {', '.join(SEVERITIES)}")

        if feld in regel:
            _check_typ(regel[feld], typ, name, feld, origin)
        for name_zusatz, typ_zusatz in zusatz.items():
            if name_zusatz in regel:
                _check_typ(regel[name_zusatz], typ_zusatz, name, name_zusatz, origin)

        if not is_base and name in PROTECTED and severity != "error":
            raise RuleError(f"{origin}: Prüfung {name} darf nicht auf {severity!r} "
                            f"gesenkt werden, sie gilt nach K6 immer als error")

    return RuleSet(origin, is_base, scope, checks)


def _check_typ(wert, typ, name: str, feld: str, origin: str) -> None:
    if typ is list:
        if not isinstance(wert, list) or any(not isinstance(e, str) for e in wert):
            raise RuleError(f"{origin}: {name}.{feld} muss eine Liste von "
                            f"Zeichenketten sein")
        return
    if isinstance(wert, bool) or not isinstance(wert, int) or wert <= 0:
        raise RuleError(f"{origin}: {name}.{feld} muss eine positive Ganzzahl sein")


def _check_konflikte(zutreffend, relative_path: str) -> None:
    """K5: gleicher Rang, gleiche Prüfung, zwei Dateien."""
    for name in CHECK_SCHEMA:
        nach_rang = {}
        for rang, satz in zutreffend:
            if rang == BASE_RANK or name not in satz.checks:
                continue
            nach_rang.setdefault(rang, []).append(satz)
        for rang, saetze in nach_rang.items():
            if len(saetze) > 1:
                orte = " und ".join(sorted(s.origin for s in saetze))
                raise RuleError(
                    f"{relative_path}: Prüfung {name} ist in {orte} mit gleich "
                    f"langem Geltungsbereich definiert. Nach K5 wird das nicht "
                    f"aufgelöst, einer der beiden Regelsätze muss weichen.")


def _under(relative_path: str, prefix: str) -> bool:
    pfad = relative_path.replace("\\", "/").strip("/")
    praefix = prefix.replace("\\", "/").strip("/")
    return pfad == praefix or pfad.startswith(praefix + "/")
