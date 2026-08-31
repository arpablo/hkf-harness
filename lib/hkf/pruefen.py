# -*- coding: utf-8 -*-
"""Die strukturellen Pruefungen aus Core §6.3.

Frontmatter und Grammatik pruefen `schema` und `grammatik`; hier steht, was
sich erst aus dem Zusammenhang ergibt — ob ein Typ zu seinem Verzeichnis
passt, ob ein Verweis ankommt, ob die abgeleiteten Tabellen stimmen.

Jeder Befund nennt Datei, Schweregrad und einen Satz. `fehler` heisst: Die
Ablage ist nicht konform (§7.2). `hinweis` heisst: Es faellt auf, macht sie
aber nicht ungueltig.
"""
import io, os, re

import yaml

from . import TEMPLATES, ablage, frontmatter, notiz
from .importieren import (ARTVERZEICHNIS, KERN_TYPEN, OHNE, STANDARD_PROPTYPES,
                          _property_tabelle, _tabelle_voll, _verzeichnis)

FEHLER, HINWEIS = "fehler", "hinweis"
LINK = re.compile(r"\[\[([^\]|\\]+)(?:\\?\|([^\]]*))?\]\]")


def ohne_code(text):
    """Was in Backticks steht, ist ein Beispiel und kein Verweis.

    Die Grundausstattung zeigt in `proptypes/hkf-link.md` einen Wikilink als
    Muster her. Wer ihn aufzuloesen versuchte, faende ein Ziel, das es nicht
    gibt — und jede frisch angelegte Wissensbasis waere unkonform.
    """
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


class Befund(object):
    def __init__(self, datei, text, grad=FEHLER):
        self.datei, self.text, self.grad = datei, text, grad

    def __str__(self):
        return "%s: %s" % (self.datei, self.text)


class Bestand(object):
    """Was mehrere Pruefungen brauchen, einmal gelesen.

    `art` ist "hkb" oder "bundle". Ein Bundle hat keine Typverzeichnisse,
    keinen Ablagepfad und keinen Basispfad (§4); als Notiz gilt dort, was
    `type` traegt, gleich wo es liegt, und eine Mediendatei erkennt man an
    ihrer Endung (§4.3).
    """

    def __init__(self, hkb, art="hkb"):
        self.hkb = hkb
        self.art = art
        wurzeldatei = "hkb.md" if art == "hkb" else "hbundle.md"
        self.wurzel, self.wurzel_body = frontmatter.lesen(
            os.path.join(hkb, wurzeldatei))
        self.notizen, self.typdefs, self.proptypes = {}, {}, {}
        self.medien = set()
        if art == "hkb":
            self.basis = ablage.basis(hkb)
            self.ablagepfad = ablage.ablagepfad(hkb)
            self.media_basis = str(self.wurzel.get("media_base") or "").strip("/")
            self.base = str(self.wurzel.get("base") or "").strip("/")
            self._hkb_lesen()
        else:
            self.basis, self.ablagepfad = hkb, ""
            self.media_basis, self.base = "", ""
            self._bundle_lesen()
        self.nach_namen = {}
        for rel in self.notizen:
            self.nach_namen.setdefault(rel.rsplit("/", 1)[-1], []).append(rel)
        self.medien_namen = {}
        for rel in self.medien:
            self.medien_namen.setdefault(rel.rsplit("/", 1)[-1], []).append(rel)

    def _eintrag(self, p, rel):
        daten, body = frontmatter.lesen(p)
        kopf = notiz.teilen(io.open(p, encoding="utf-8").read())[0]
        return {"pfad": p, "rel": rel, "daten": daten, "body": body,
                "kopf": kopf, "typ": str(daten.get("type") or "")}

    def _hkb_lesen(self):
        for p in ablage.dateien(self.basis):
            rel = os.path.relpath(p, self.basis).replace(os.sep, "/")
            if "/" not in rel:
                continue
            e = self._eintrag(p, rel)
            if not e["typ"]:
                continue
            self.notizen[rel[:-3]] = e
            verz, name = rel.split("/", 1)
            if verz == "typedefs":
                self.typdefs[name[:-3]] = e
            elif verz == "proptypes":
                self.proptypes[name[:-3]] = e
        mb = os.path.join(self.hkb, self.media_basis) if self.media_basis else self.hkb
        for art in ARTVERZEICHNIS.values():
            for r, _dirs, fs in os.walk(os.path.join(mb, art)):
                for f in fs:
                    if f.startswith("."):
                        continue
                    rel = os.path.relpath(os.path.join(r, f), self.hkb)
                    self.medien.add(rel.replace(os.sep, "/"))

    def _bundle_lesen(self):
        """§4.3: eine `.md` mit `type` ist eine Notiz, alles andere Medium."""
        for r, dirs, fs in os.walk(self.hkb):
            dirs[:] = sorted(d for d in dirs if not d.startswith("."))
            for f in sorted(fs):
                if f.startswith("."):
                    continue
                p = os.path.join(r, f)
                rel = os.path.relpath(p, self.hkb).replace(os.sep, "/")
                if not f.endswith(".md"):
                    self.medien.add(rel)
                    continue
                if rel == "hbundle.md":
                    continue
                e = self._eintrag(p, rel)
                if not e["typ"]:
                    continue                  # uebergangen, nicht bemaengelt
                self.notizen[rel[:-3]] = e
                if e["typ"] == "typedef":
                    self.typdefs[f[:-3]] = e
                elif e["typ"] == "proptype":
                    self.proptypes[f[:-3]] = e

    def praefix(self):
        return "/".join(t for t in (self.ablagepfad, self.base) if t)

    def verzeichnisse(self):
        aus = {}
        for name, e in self.typdefs.items():
            aus.setdefault(_verzeichnis(name, e["daten"]), []).append(name)
        return aus

    def aufloesen(self, ziel, aus_wurzeldatei=False):
        """(art, rest) — art ist 'notiz', 'medium' oder None."""
        if self.art == "bundle":
            # In einer Lieferung genuegt ein Ziel ohne Verzeichnis, solange
            # genau eine Datei so heisst (§3.6).
            if ziel in self.notizen:
                return ("notiz", ziel)
            if ziel in self.medien:
                return ("medium", ziel)
            for tabelle, name in ((self.nach_namen, "notiz"),
                                  (self.medien_namen, "medium")):
                treffer = tabelle.get(ziel) or []
                if len(treffer) == 1:
                    return (name, treffer[0])
                if len(treffer) > 1:
                    return ("mehrdeutig", ziel)
            return (None, ziel)
        pre = self.praefix() if not aus_wurzeldatei else self.base
        if pre and ziel.startswith(pre + "/"):
            rest = ziel[len(pre) + 1:]
        elif pre:
            mpre = "/".join(t for t in (self.ablagepfad, self.media_basis) if t)
            if mpre and ziel.startswith(mpre + "/"):
                return ("medium", ziel[len(self.ablagepfad) + 1:]
                        if self.ablagepfad else ziel)
            return (None, ziel)
        else:
            rest = ziel
        if rest in self.notizen:
            return ("notiz", rest)
        if rest in self.medien or rest.split("/")[0] == self.media_basis:
            return ("medium", rest)
        return (None, rest)


# ── Die Pruefungen ──────────────────────────────────────────────────────

def _wurzeldatei(b, befunde):
    if b.art != "hkb":
        return
    if not b.wurzel.get("hkf"):
        befunde.append(Befund("hkb.md", "`hkf` fehlt (§3.1)."))
    if not b.wurzel.get("name"):
        befunde.append(Befund("hkb.md", "`name` fehlt (Anhang A.1)."))
    if not os.path.isdir(b.basis):
        befunde.append(Befund("hkb.md", "`base` zeigt auf kein Verzeichnis."))
    for verz in ("typedefs", "proptypes", "bundles"):
        if not os.path.isdir(os.path.join(b.basis, verz)):
            befunde.append(Befund("hkb.md",
                                  "%s/ fehlt im Basispfad (§7.2)." % verz))


def _typen(b, befunde):
    if b.art != "hkb":
        return
    verz = b.verzeichnisse()
    for d, namen in sorted(verz.items()):
        if len(namen) > 1:
            befunde.append(Befund("typedefs/", "Das Verzeichnis %s beanspruchen "
                                  "%s (§6.3)." % (d, " und ".join(sorted(namen)))))
        if d.startswith("/") or d.endswith("/") or ".." in d.split("/"):
            befunde.append(Befund("typedefs/%s.md" % namen[0],
                                  "`dir` ist kein wohlgeformter relativer Pfad: %r" % d))
    for a in sorted(verz):
        for c in sorted(verz):
            if a != c and c.startswith(a + "/"):
                befunde.append(Befund("typedefs/", "Die Typverzeichnisse %s und %s "
                                      "liegen ineinander (§6.3)." % (a, c)))
    for rel, e in sorted(b.notizen.items()):
        typ = e["typ"]
        if typ not in b.typdefs:
            befunde.append(Befund(e["rel"], "Der Typ `%s` hat keine Typdefinition "
                                            "(§3.7)." % typ))
            continue
        soll = _verzeichnis(typ, b.typdefs[typ]["daten"])
        ist = rel.rsplit("/", 1)[0]
        if ist != soll:
            befunde.append(Befund(e["rel"], "liegt in %s/, der Typ `%s` gehört "
                                  "nach %s/ (§3.2)." % (ist, typ, soll)))


def _vorlaeufige(b, befunde):
    for name, e in sorted(b.typdefs.items()):
        vor = e["daten"].get("provisional")
        if vor is None:
            continue
        if vor is not True:
            befunde.append(Befund(e["rel"], "`provisional` trägt %r; erlaubt ist "
                                            "nur `true` (§5.4)." % vor))
            continue
        if b.art == "bundle":
            befunde.append(Befund(e["rel"], "Ein Bundle enthält keine vorläufige "
                                            "Typdefinition (§7.1)."))
            continue
        d = _verzeichnis(name, e["daten"])
        anzahl = sum(1 for r, n in b.notizen.items() if n["typ"] == name)
        befunde.append(Befund(e["rel"], "Der Typ `%s` ist vorläufig; %d Notizen "
                              "liegen in %s/ (§5.4)." % (name, anzahl, d), HINWEIS))
        if notiz.abschnitt(e["body"], "Properties") is not None:
            befunde.append(Befund(e["rel"], "Eine vorläufige Typdefinition trägt "
                                            "keinen Abschnitt `# Properties` (§5.4)."))
        if e["daten"].get("bundles"):
            befunde.append(Befund(e["rel"], "Eine vorläufige Typdefinition trägt "
                                            "kein `bundles` (§5.4)."))
    for rel, e in sorted(b.notizen.items()):
        if e["typ"] != "typedef" and e["daten"].get("provisional") is not None:
            befunde.append(Befund(e["rel"], "`provisional` steht nur an einer "
                                            "Typdefinition (§6.3)."))


def _proptypes(b, befunde):
    if b.art == "hkb":
        for name in sorted(STANDARD_PROPTYPES - set(b.proptypes)):
            befunde.append(Befund("proptypes/", "Der Standard-Property-Typ `%s` "
                                                "fehlt (§3.5.1)." % name))
    else:
        for name in sorted(STANDARD_PROPTYPES & set(b.proptypes)):
            befunde.append(Befund(b.proptypes[name]["rel"],
                                  "Ein Bundle definiert keinen "
                                  "Standard-Property-Typ um (§7.1)."))
    for name, e in sorted(b.proptypes.items()):
        if name in WERTFORMEN:
            befunde.append(Befund(e["rel"], "Für eine Wertform wird kein "
                                            "Property-Typ angelegt (§3.5)."))
        if name.endswith("-list") and name not in STANDARD_PROPTYPES:
            befunde.append(Befund(e["rel"], "Ein Property-Typ endet nicht auf "
                                            "`-list`; die Listenform entsteht aus "
                                            "dem Namen (§3.5.2)."))
        form = str(e["daten"].get("form") or "")
        if form and form not in ("text", "list", "number", "checkbox",
                                 "date", "datetime"):
            befunde.append(Befund(e["rel"], "`form` trägt %r; erlaubt sind die "
                                  "Wertformen aus §3.4." % form))


def _zeiten(b, befunde):
    for rel, e in sorted(b.notizen.items()):
        d = e["daten"]
        if b.art == "hkb":
            for feld in ("created", "modified"):
                if feld not in d:
                    befunde.append(Befund(e["rel"], "`%s` fehlt (§6.3)." % feld,
                                          HINWEIS))
        c, m = str(d.get("created") or ""), str(d.get("modified") or "")
        if c and m and m[:10] < c[:10]:
            befunde.append(Befund(e["rel"], "`modified` (%s) liegt vor `created` "
                                            "(%s)." % (m, c)))
        if m and "T" not in m and len(m) == 10:
            befunde.append(Befund(e["rel"], "`modified` trägt keine Uhrzeit; "
                                            "datetime verlangt sie (§3.4).", HINWEIS))


def _leere_properties(b, befunde):
    for rel, e in sorted(b.notizen.items()):
        for k, v in sorted(e["daten"].items()):
            if v is None or (isinstance(v, (list, dict, str)) and len(v) == 0):
                grad = FEHLER if k in ("bundles", "rejected_links") else HINWEIS
                befunde.append(Befund(e["rel"], "`%s` ist leer (§3.4)." % k, grad))
        if b.art == "bundle":
            for k in ("bundles", "rejected_links"):
                if k in e["daten"]:
                    befunde.append(Befund(e["rel"], "`%s` beschreibt, wie eine "
                                          "Wissensbasis die Lieferung einsortiert "
                                          "hat; in einem Bundle steht es nicht "
                                          "(§7.1)." % k))


def _verweise(b, befunde):
    for rel, e in sorted(b.notizen.items()):
        text = notiz.bauen(e["kopf"], ohne_code(e["body"]))
        for m in LINK.finditer(text):
            ziel, alias = m.group(1), m.group(2)
            art, rest = b.aufloesen(ziel)
            if art == "mehrdeutig":
                befunde.append(Befund(e["rel"], "[[%s]] ist mehrdeutig — mehrere "
                                      "Dateien heißen so (§3.6)." % ziel))
            elif art is None:
                befunde.append(Befund(e["rel"], "[[%s]] lässt sich nicht auflösen "
                                                "(§3.6)." % ziel))
            elif art == "medium" and rest not in b.medien:
                befunde.append(Befund(e["rel"], "[[%s]] zeigt auf keine vorhandene "
                                                "Mediendatei (§3.2.1)." % ziel))
            if alias is None:
                befunde.append(Befund(e["rel"], "[[%s]] trägt keinen Alias (§3.6)."
                                      % ziel, HINWEIS))
        if b.art != "hkb" or rel.split("/", 1)[0] == "bundles":
            continue
        for l in e["daten"].get("bundles") or []:
            m = re.match(r"^\[\[([^\]|]+)", str(l))
            if not m:
                continue
            art, rest = b.aufloesen(m.group(1))
            if art != "notiz" or not rest.startswith("bundles/"):
                befunde.append(Befund(e["rel"], "`bundles` nennt %s — dort liegt "
                                      "keine Bundle-Notiz (§5.2)." % m.group(1)))


def _typtabelle(b, befunde):
    """Die abgeleitete Tabelle gegen die Typdefinitionen (§3.1)."""
    if b.art != "hkb":
        return
    ist = {}
    teil = notiz.abschnitt(b.wurzel_body, "Typen") or ""
    for zeile in teil.splitlines():
        if not zeile.startswith("|"):
            continue
        s = [x.strip() for x in zeile.strip("|").split("|")]
        if len(s) < 3 or s[0] in ("Typ", "") or set(s[0]) <= set("- "):
            continue
        ist[s[0]] = (s[1], s[2])
    soll = {n: (_verzeichnis(n, e["daten"]), str(e["daten"].get("description") or ""))
            for n, e in b.typdefs.items()}
    for name in sorted(set(soll) - set(ist)):
        befunde.append(Befund("hkb.md", "Die Typtabelle nennt `%s` nicht (§3.1)."
                              % name))
    for name in sorted(set(ist) - set(soll)):
        befunde.append(Befund("hkb.md", "Die Typtabelle nennt `%s`, den es nicht "
                              "gibt (§3.1)." % name))
    for name in sorted(set(ist) & set(soll)):
        if ist[name] != soll[name]:
            befunde.append(Befund("hkb.md", "Die Typtabelle sagt zu `%s` %r, die "
                                  "Typdefinition %r (§3.1)."
                                  % (name, ist[name], soll[name])))


def _siehe_auch(b, befunde):
    for rel, e in sorted(b.notizen.items()):
        teil = notiz.abschnitt(e["body"], "Siehe auch")
        if teil is None:
            continue
        ueberschriften = re.findall(r"^# (.+)$", e["body"], re.M)
        if ueberschriften and ueberschriften[-1] != "Siehe auch":
            befunde.append(Befund(e["rel"], "`# Siehe auch` ist nicht der letzte "
                                            "Abschnitt (§5.6).", HINWEIS))
        abgelehnt = [str(x) for x in (e["daten"].get("rejected_links") or [])]
        verwandt = [str(x) for x in (e["daten"].get("related") or [])]
        aliase, ziele = [], []
        for zeile in teil.strip("\n").splitlines():
            if not zeile.strip():
                continue
            m = re.match(r"^- (\[\[([^\]|\\]+)(?:\|([^\]]*))?\]\])(.*)$", zeile)
            if not m:
                befunde.append(Befund(e["rel"], "Zeile unter `# Siehe auch` ist kein "
                                      "qualifizierter Wikilink: %r" % zeile.strip()))
                continue
            link, ziel, alias, rest = m.group(1), m.group(2), m.group(3), m.group(4)
            if not rest.startswith(" — ") or not rest[3:].strip():
                befunde.append(Befund(e["rel"], "%s steht ohne Grund unter "
                                      "`# Siehe auch` (§5.6)." % link))
            aliase.append((alias or ziel).lower())
            ziele.append((ziel, link))
            if any(ziel in x for x in abgelehnt):
                befunde.append(Befund(e["rel"], "%s steht zugleich unter `# Siehe "
                                      "auch` und in `rejected_links` (§5.6)." % link))
            if b.art == "hkb" and not any(ziel in x for x in verwandt):
                andere = notiz.entfernen(notiz.entfernen(
                    e["kopf"], "related"), "rejected_links")
                if ziel not in andere:
                    befunde.append(Befund(e["rel"], "%s fehlt in `related` (§5.6)."
                                          % link, HINWEIS))
        if aliase != sorted(aliase):
            befunde.append(Befund(e["rel"], "Die Einträge unter `# Siehe auch` stehen "
                                            "nicht alphabetisch (§5.6).", HINWEIS))
        for ziel, link in (ziele if b.art == "hkb" else []):
            art, rest = b.aufloesen(ziel)
            if art != "notiz":
                continue
            gegen = b.notizen[rest]
            eigener = notiz.ohne_abschnitt(e["body"], "Siehe auch")
            titel = [str(gegen["daten"].get("title") or "")] + \
                    [str(a) for a in (gegen["daten"].get("aliases") or [])]
            zurueck = re.findall(r"\[\[([^\]|\\]+)",
                                 notiz.abschnitt(gegen["body"], "Siehe auch") or "")
            if any(rel == b.aufloesen(z)[1] for z in zurueck) and \
               not any(t and t in eigener for t in titel):
                befunde.append(Befund(e["rel"], "%s ist ein bloßer Rückverweis; die "
                                      "Auskunft steht in der Backlink-Ansicht "
                                      "(§5.6)." % link, HINWEIS))


def _bundle_notizen(b, befunde):
    if b.art != "hkb":
        return
    for rel, e in sorted(b.notizen.items()):
        if not rel.startswith("bundles/") or e["typ"] != "bundle":
            continue
        name = rel.split("/", 1)[1]
        kennung = str(e["daten"].get("id") or "")
        if kennung != name:
            befunde.append(Befund(e["rel"], "`id` ist %r, der Dateiname %r (§5.1)."
                                  % (kennung, name)))
        if not re.match(r"^[a-z][a-z0-9-]*$", kennung):
            befunde.append(Befund(e["rel"], "`id` ist nicht kebab-case (§4.1)."))
        if not e["daten"].get("description"):
            befunde.append(Befund(e["rel"], "`description` fehlt (§4.1)."))
        if not e["daten"].get("version"):
            befunde.append(Befund(e["rel"], "`version` fehlt; der Importnachweis "
                                  "wird dann bei jedem Lauf ersetzt (§5.1).", HINWEIS))
        for eintrag in e["daten"].get("required_bundles") or []:
            m = re.match(r"^\s*([a-z][a-z0-9-]*)\s*(?:>=\s*(\d+\.\d+))?\s*$",
                         str(eintrag))
            if not m:
                befunde.append(Befund(e["rel"], "`required_bundles`: %r hat nicht "
                                      "die Form aus §4.1." % eintrag))
            elif m.group(1) == kennung:
                befunde.append(Befund(e["rel"], "`required_bundles` setzt das eigene "
                                                "Bundle voraus (§6.3)."))
        _entscheidungen(e, befunde)


def _entscheidungen(e, befunde):
    teil = notiz.abschnitt(e["body"], "Entscheidungen")
    if teil is None:
        return
    gesehen = set()
    for zeile in teil.splitlines():
        if not zeile.startswith("|"):
            continue
        s = [x.strip() for x in zeile.strip("|").split("|")]
        if not s or s[0] in ("Gegenstand", "") or set(s[0]) <= set("- "):
            continue
        if len(s) != 5:
            befunde.append(Befund(e["rel"], "Entscheidungszeile hat %d statt 5 "
                                  "Spalten (§5.7): %r" % (len(s), zeile.strip())))
            continue
        gegenstand, urteil, von, beurteilt, grund = s
        if urteil not in ("gleich", "verschieden", "dieselbe"):
            befunde.append(Befund(e["rel"], "Urteil %r ist nicht erlaubt (§5.7)."
                                  % urteil))
        for feld, wert in (("Von", von), ("Beurteilt", beurteilt), ("Grund", grund)):
            if not wert:
                befunde.append(Befund(e["rel"], "%s ist leer (§5.7)." % feld))
        if not re.match(r"^(Typ `[^`]+`|Notiz \[\[)", gegenstand):
            befunde.append(Befund(e["rel"], "Gegenstand %r ist weder ein Typ noch "
                                  "eine Notiz; strukturelle Konflikte werden nicht "
                                  "aufgezeichnet (§5.7)." % gegenstand))
        if gegenstand in gesehen:
            befunde.append(Befund(e["rel"], "Zweites Urteil über %s — welches gälte, "
                                  "wäre nicht bestimmt (§5.7)." % gegenstand))
        gesehen.add(gegenstand)


def _wikidata(b, befunde):
    werte = {}
    for rel, e in sorted(b.notizen.items()):
        tabelle = _property_tabelle(b.typdefs.get(e["typ"], {}).get("body", ""))
        for prop, (t, _p) in tabelle.items():
            if t.split(" / ")[0] != "hkf-wikidata":
                continue
            if e["daten"].get(prop):
                werte.setdefault(str(e["daten"][prop]), []).append(e["rel"])
    for wert, wo in sorted(werte.items()):
        if len(wo) > 1:
            befunde.append(Befund(wo[0], "%s tragen dieselbe Kennung %s und sind ein "
                                  "Zusammenführungskandidat (§6.3)."
                                  % (" und ".join(wo), wert), HINWEIS))


def _verwaist(b, befunde):
    if b.art != "hkb":
        return
    zeigt_auf = set()
    for rel, e in sorted(b.notizen.items()):
        for m in LINK.finditer(notiz.bauen(e["kopf"], ohne_code(e["body"]))):
            art, rest = b.aufloesen(m.group(1))
            if art == "notiz" and rest != rel:
                zeigt_auf.add(rest)
    for m in LINK.finditer(b.wurzel_body):
        art, rest = b.aufloesen(m.group(1), aus_wurzeldatei=True)
        if art == "notiz":
            zeigt_auf.add(rest)
    for rel, e in sorted(b.notizen.items()):
        if rel in zeigt_auf or e["typ"] in KERN_TYPEN or rel.startswith("proptypes/"):
            continue
        befunde.append(Befund(e["rel"], "Auf diese Notiz zeigt kein Verweis; sie ist "
                              "über die Wissensbasis nicht erreichbar (§6.3).", HINWEIS))


def undeklariert(b):
    """--strict: je Typ und Property-Name, mit der Zahl der Notizen (§6.3)."""
    allgemein = {"type", "title", "description", "tags", "aliases", "cssclasses",
                 "status", "created", "modified", "modified_by", "bundles",
                 "related", "rejected_links"}
    je_typ, gesamt = {}, {}
    for rel, e in sorted(b.notizen.items()):
        typ = e["typ"]
        gesamt[typ] = gesamt.get(typ, 0) + 1
        if typ in KERN_TYPEN:
            continue
        erlaubt = set(_property_tabelle(
            b.typdefs.get(typ, {}).get("body", ""))) | allgemein
        for k in e["daten"]:
            if k not in erlaubt:
                je_typ.setdefault((typ, k), []).append(e["rel"])
    return ["%s: %s in %d von %d Notizen" % (typ, k, len(wo), gesamt[typ])
            for (typ, k), wo in sorted(je_typ.items())]


PRUEFUNGEN = (_wurzeldatei, _typen, _vorlaeufige, _proptypes, _zeiten,
              _leere_properties, _verweise, _typtabelle, _siehe_auch,
              _bundle_notizen, _wikidata, _verwaist)


# ── Die Property-Tabellen gegen die Werte (§3.7.1, §6.3) ────────────────

WERTFORMEN = ("text", "list", "number", "checkbox", "date", "datetime")
MIT_ZUSATZ = ("hkf-link", "hkf-file")
DATUM = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ZEITPUNKT = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")


def zerlege(angabe):
    """`hkf-link-list:person,organisation` → ('hkf-link', True, [...]).

    Das `-list` wird **zuerst** abgetrennt (§3.5.2): Sonst hielte ein Werkzeug
    `hkf-link-list:person` für unzulässig, obwohl §3.7.1 es erlaubt.
    """
    rest, _, args = angabe.strip().partition(":")
    liste = rest.endswith("-list")
    basis = rest[:-5] if liste else rest
    return basis, liste, [a for a in args.split(",") if a]


def _wertform(b, basis, liste):
    """Die Wertform hinter einer Typ-Angabe, oder None, wenn unbekannt."""
    if basis in WERTFORMEN:
        return "list" if liste else basis
    d = _proptype_daten(b, basis)
    if d is None:
        return None
    return "list" if liste else str(d.get("form") or "")


def _proptype_daten(b, name):
    """Das Frontmatter eines Property-Typs — auch wenn er nicht beiliegt.

    Eine Lieferung schickt die Standard-Property-Typen nicht mit (§7.1); jede
    Wissensbasis hat sie ohnehin. Der Harness kennt sie aus seiner Vorlage und
    kann eine Lieferung darum pruefen, ohne dass sie ihm etwas mitgibt.
    """
    e = b.proptypes.get(name)
    if e is not None:
        return e["daten"]
    if name not in STANDARD_PROPTYPES:
        return None
    p = os.path.join(TEMPLATES, "hkb", "proptypes", name + ".md")
    if not os.path.isfile(p):
        return None
    return frontmatter.lesen(p)[0]


def _form_passt(wert, form):
    if form == "text":
        return isinstance(wert, str)
    if form == "number":
        return isinstance(wert, (int, float)) and not isinstance(wert, bool)
    if form == "checkbox":
        return isinstance(wert, bool)
    if form == "date":
        return isinstance(wert, str) and bool(DATUM.match(wert))
    if form == "datetime":
        return isinstance(wert, str) and bool(ZEITPUNKT.match(wert))
    if form == "list":
        return isinstance(wert, list)
    return True


def _skalar_passt(b, wert, basis, args):
    """(ok, Grund). Prueft einen Einzelwert gegen eine Typ-Angabe."""
    if basis in WERTFORMEN:
        return (_form_passt(wert, basis),
                "ist kein %s" % basis)
    d = _proptype_daten(b, basis)
    if d is None:
        return True, ""                       # der Typ selbst wird eigens gemeldet
    form = str(d.get("form") or "text")
    if not _form_passt(wert, form):
        return False, "ist kein %s (%s verlangt es)" % (form, basis)
    if basis == "hkf-link":
        return _link_passt(b, wert, args, medien=False)
    if basis == "hkf-file":
        return _link_passt(b, wert, args, medien=True)
    text = str(wert)
    muster = d.get("pattern")
    if muster and not re.search(str(muster), text):
        return False, "passt nicht auf das `pattern` von %s" % basis
    werte = d.get("values")
    if werte and text not in [str(v) for v in werte]:
        return False, "steht nicht in den `values` von %s" % basis
    for grenze, name, schlechter in ((d.get("min"), "min", lambda a, g: a < g),
                                     (d.get("max"), "max", lambda a, g: a > g)):
        if grenze is not None and isinstance(wert, (int, float)) and \
           schlechter(wert, grenze):
            return False, "verletzt `%s: %s` von %s" % (name, grenze, basis)
    return True, ""


def _link_passt(b, wert, args, medien):
    m = re.match(r"^\[\[([^\]|\\]+)(?:\|[^\]]*)?\]\]$", str(wert).strip())
    if not m:
        return False, "ist kein qualifizierter Wikilink (§3.6)"
    art, rest = b.aufloesen(m.group(1))
    if medien:
        if art != "medium":
            return False, "zeigt auf keine Mediendatei (§3.7.1)"
        if rest not in b.medien:
            return False, "zeigt auf keine vorhandene Datei"
        name = rest.rsplit("/", 1)[-1]
        if "." not in name or name.endswith(".md"):
            return False, "trägt keine brauchbare Dateiendung (§6.3)"
        teile = rest.split("/")
        verz = teile[1] if b.media_basis else teile[0]
        ist = {v: k for k, v in ARTVERZEICHNIS.items()}.get(verz)
        if args and ist not in args:
            return False, "ist ein %s, verlangt ist %s" % (ist, " oder ".join(args))
        return True, ""
    if art != "notiz":
        return False, "lässt sich nicht auf eine Notiz auflösen (§3.6)"
    typ = b.notizen[rest]["typ"]
    if args and typ not in args:
        return False, "zeigt auf `%s`, verlangt ist %s" % (typ, " oder ".join(args))
    return True, ""


def _typangaben(b, befunde):
    """Was in der Typ-Spalte steht, muss es geben (§3.7.1)."""
    for name, e in sorted(b.typdefs.items()):
        for prop, (angabe, _pflicht) in sorted(
                _property_tabelle(e["body"]).items()):
            formen = []
            for teil in re.split(r"\s*/\s*", angabe):
                basis, liste, args = zerlege(teil)
                form = _wertform(b, basis, liste)
                if form is None:
                    befunde.append(Befund(e["rel"], "`%s`: %r ist weder Wertform "
                                          "noch Property-Typ (§3.7.1)." % (prop, teil)))
                    continue
                formen.append(form)
                if args and basis not in MIT_ZUSATZ:
                    befunde.append(Befund(e["rel"], "`%s`: Der `:`-Zusatz steht nur "
                                          "an hkf-link und hkf-file (§3.7.1), nicht "
                                          "an %r." % (prop, basis)))
                if basis == "hkf-link":
                    for ziel in args:
                        if ziel not in b.typdefs:
                            befunde.append(Befund(e["rel"], "`%s`: Der Zieltyp `%s` "
                                                  "ist nicht registriert (§3.7.1)."
                                                  % (prop, ziel)))
                if basis == "hkf-file":
                    for a in args:
                        if a not in ARTVERZEICHNIS:
                            befunde.append(Befund(e["rel"], "`%s`: %r ist keine "
                                                  "Medienart (§3.7.1)." % (prop, a)))
            if len(set(formen)) > 1:
                befunde.append(Befund(e["rel"], "`%s`: Die Alternativen haben "
                                      "verschiedene Wertformen (%s) — §6.3 verlangt "
                                      "dieselbe." % (prop, ", ".join(sorted(set(formen))))))


def _werte(b, befunde):
    """Jede Property gegen ihre Typ-Angabe; bei Alternativen genügt eine."""
    for rel, e in sorted(b.notizen.items()):
        tabelle = _property_tabelle(b.typdefs.get(e["typ"], {}).get("body", ""))
        for prop, (angabe, pflicht) in sorted(tabelle.items()):
            if prop not in e["daten"]:
                if pflicht.lower().startswith("ja"):
                    befunde.append(Befund(e["rel"], "`%s` ist Pflicht und fehlt "
                                          "(§3.7)." % prop))
                continue
            for grund in _passt(b, e["daten"][prop], angabe)[:1]:
                befunde.append(Befund(e["rel"], "`%s` %s." % (prop, grund)))


def _passt(b, wert, angabe):
    """Gruende, warum `wert` die Typ-Angabe verfehlt; leer heisst: er passt."""
    gruende = []
    for teil in re.split(r"\s*/\s*", angabe):
        basis, liste, args = zerlege(teil)
        if liste:
            if not isinstance(wert, list):
                gruende.append("ist keine Liste (%s verlangt es)" % teil)
                continue
            schlecht = [(w, g) for w, g in
                        ((w, _skalar_passt(b, w, basis, args)) for w in wert)
                        if not g[0]]
            if schlecht:
                gruende.append("Eintrag %r %s" % (schlecht[0][0], schlecht[0][1][1]))
                continue
            return []
        ok, grund = _skalar_passt(b, wert, basis, args)
        if ok:
            return []
        gruende.append(grund)
    return gruende


def _vorgaben(b, befunde):
    """Eine Vorgabe erfuellt ihre Typ-Angabe und steht an keiner Pflicht (§3.7)."""
    for _name, e in sorted(b.typdefs.items()):
        for prop, (angabe, pflicht, vorgabe, _t) in sorted(
                _tabelle_voll(e["body"]).items()):
            if vorgabe == OHNE:
                continue
            if pflicht.lower().startswith("ja"):
                befunde.append(Befund(e["rel"], "`%s` ist Pflicht und trägt "
                                      "zugleich die Vorgabe `%s`; was gefordert "
                                      "wird, darf nicht fehlen dürfen (§3.7)."
                                      % (prop, vorgabe)))
                continue
            try:
                wert = yaml.safe_load(vorgabe)
            except yaml.YAMLError:
                befunde.append(Befund(e["rel"], "`%s`: Die Vorgabe `%s` ist kein "
                                      "Wert (§3.7)." % (prop, vorgabe)))
                continue
            for grund in _passt(b, wert, angabe)[:1]:
                befunde.append(Befund(e["rel"], "`%s`: Die Vorgabe %s (§3.7)."
                                      % (prop, grund)))


def _medienverzeichnisse(b, befunde):
    """Unter media_base liegen nur die vier Arten (§3.2.1)."""
    if b.art != "hkb":
        return
    mb = os.path.join(b.hkb, b.media_basis) if b.media_basis else b.hkb
    if not b.media_basis or not os.path.isdir(mb):
        return
    erlaubt = set(ARTVERZEICHNIS.values())
    for f in sorted(os.listdir(mb)):
        if f.startswith("."):
            continue
        if os.path.isdir(os.path.join(mb, f)) and f not in erlaubt:
            grad = FEHLER if f in b.verzeichnisse() else HINWEIS
            befunde.append(Befund("%s/%s" % (b.media_basis, f),
                                  "liegt unter `media_base`; dort liegen nur "
                                  "images, videos, audios und documents (§3.2.1).",
                                  grad))


PRUEFUNGEN = PRUEFUNGEN + (_typangaben, _werte, _vorgaben, _medienverzeichnisse)


# ── Was nur für ein Bundle gilt (§4, §7.1) ──────────────────────────────

def _lieferung(b, befunde):
    if b.art != "bundle":
        return
    d = b.wurzel
    if not d.get("id"):
        befunde.append(Befund("hbundle.md", "`id` fehlt (§4.1)."))
    elif not re.match(r"^[a-z][a-z0-9-]*$", str(d["id"])):
        befunde.append(Befund("hbundle.md", "`id` ist nicht kebab-case (§4.1)."))
    if not d.get("description"):
        befunde.append(Befund("hbundle.md", "`description` fehlt (§4.1)."))
    if "hkf" not in d:
        befunde.append(Befund("hbundle.md", "Die Lieferung nennt keine Fassung; "
                              "die aufnehmende Wissensbasis liest sie nach ihrer "
                              "eigenen (§8).", HINWEIS))
    if not d.get("version"):
        befunde.append(Befund("hbundle.md", "`version` fehlt; die Lieferung hat "
                              "dann keine Geschichte, nur einen letzten Stand "
                              "(§5.1).", HINWEIS))
    for eintrag in d.get("required_bundles") or []:
        m = re.match(r"^\s*([a-z][a-z0-9-]*)\s*(?:>=\s*(\d+\.\d+))?\s*$",
                     str(eintrag))
        if not m:
            befunde.append(Befund("hbundle.md", "`required_bundles`: %r hat nicht "
                                  "die Form aus §4.1." % eintrag))
        elif m.group(1) == str(d.get("id") or ""):
            befunde.append(Befund("hbundle.md", "`required_bundles` setzt das "
                                                "eigene Bundle voraus (§6.3)."))
    for schluessel in ("imported",):
        if schluessel in d:
            befunde.append(Befund("hbundle.md", "`%s` gehört der aufnehmenden "
                                  "Wissensbasis, nicht der Lieferung (§5.1)."
                                  % schluessel))
    for ueberschrift in ("Import", "Entscheidungen"):
        if re.search(r"^# %s\b" % ueberschrift, b.wurzel_body, re.M):
            befunde.append(Befund("hbundle.md", "Ein Bundle trägt weder Import- "
                                  "noch Entscheidungsnachweis (§7.1)."))
            break

    # §4.1: eine zweite Notiz mit `type: bundle` gehört nicht in ein Bundle
    for rel, e in sorted(b.notizen.items()):
        if e["typ"] == "bundle":
            befunde.append(Befund(e["rel"], "Eine zweite Notiz vom Typ `bundle` "
                                            "gehört nicht in eine Lieferung (§4.1)."))

    # §4.3: zwei Notizen desselben Typs mit demselben Dateinamen faelen beim
    # Import zu einer Notiz-ID zusammen
    gesehen = {}
    for rel, e in sorted(b.notizen.items()):
        schluessel = (e["typ"], rel.rsplit("/", 1)[-1])
        if schluessel in gesehen:
            befunde.append(Befund(e["rel"], "ergäbe beim Import dieselbe Notiz-ID "
                                  "wie %s (§4.3)." % gesehen[schluessel]))
        gesehen[schluessel] = e["rel"]

    # §7.1: jede verwendete Typdefinition und jeder Property-Typ liegt bei,
    # sofern nicht Grundausstattung oder aus einem vorausgesetzten Bundle
    vorausgesetzt = bool(b.wurzel.get("required_bundles"))
    fehlend = sorted({e["typ"] for e in b.notizen.values()} - set(b.typdefs)
                     - KERN_TYPEN)
    def melde_fehlend(mehrzahl, einzahl, namen):
        if not namen:
            return
        liste = ", ".join("`%s`" % n for n in namen)
        if vorausgesetzt:
            # §6.1: Ein Werkzeug weiss nicht, welche Typen ein Bundle
            # mitbraechte, das es nicht hat.
            text = ("%s %s liegt nicht bei; er muss aus einem vorausgesetzten "
                    "Bundle kommen (§7.1)." % (einzahl, liste)
                    if len(namen) == 1 else
                    "%s %s liegen nicht bei; sie müssen aus einem vorausgesetzten "
                    "Bundle kommen (§7.1)." % (mehrzahl, liste))
            befunde.append(Befund("hbundle.md", text, HINWEIS))
            return
        for n in namen:
            befunde.append(Befund("hbundle.md",
                                  "%s `%s` wird verwendet, aber weder geliefert "
                                  "noch vorausgesetzt (§7.1)." % (einzahl, n)))

    melde_fehlend("Die Typen", "Der Typ", fehlend)
    gebraucht = set()
    for name, e in b.typdefs.items():
        for _prop, (angabe, _p) in _property_tabelle(e["body"]).items():
            for teil in re.split(r"\s*/\s*", angabe):
                basis, _liste, _args = zerlege(teil)
                if basis not in WERTFORMEN:
                    gebraucht.add(basis)
    melde_fehlend("Die Property-Typen", "Der Property-Typ",
                  sorted(gebraucht - set(b.proptypes) - STANDARD_PROPTYPES))


PRUEFUNGEN = PRUEFUNGEN + (_lieferung,)


def pruefen(hkb, art="hkb"):
    b = Bestand(hkb, art)
    befunde = []
    for f in PRUEFUNGEN:
        f(b, befunde)
    return b, befunde
