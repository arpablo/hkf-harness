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

from . import ablage, frontmatter, notiz
from .importieren import (ARTVERZEICHNIS, KERN_TYPEN, STANDARD_PROPTYPES,
                          _property_tabelle, _verzeichnis)

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
    """Was mehrere Pruefungen brauchen, einmal gelesen."""

    def __init__(self, hkb):
        self.hkb = hkb
        self.basis = ablage.basis(hkb)
        self.ablagepfad = ablage.ablagepfad(hkb)
        self.wurzel, self.wurzel_body = frontmatter.lesen(
            os.path.join(hkb, "hkb.md"))
        self.media_basis = str(self.wurzel.get("media_base") or "").strip("/")
        self.base = str(self.wurzel.get("base") or "").strip("/")
        self.notizen = {}
        self.typdefs = {}
        self.proptypes = {}
        for p in ablage.dateien(self.basis):
            rel = os.path.relpath(p, self.basis).replace(os.sep, "/")
            if "/" not in rel:
                continue
            daten, body = frontmatter.lesen(p)
            if "type" not in daten:
                continue
            kopf = notiz.teilen(io.open(p, encoding="utf-8").read())[0]
            e = {"pfad": p, "rel": rel, "daten": daten, "body": body,
                 "kopf": kopf, "typ": str(daten["type"])}
            self.notizen[rel[:-3]] = e
            verz, name = rel.split("/", 1)
            if verz == "typedefs":
                self.typdefs[name[:-3]] = e
            elif verz == "proptypes":
                self.proptypes[name[:-3]] = e
        self.medien = set()
        mb = os.path.join(hkb, self.media_basis) if self.media_basis else hkb
        for art in ARTVERZEICHNIS.values():
            d = os.path.join(mb, art)
            for r, _dirs, fs in os.walk(d):
                for f in fs:
                    if f.startswith("."):
                        continue
                    rel = os.path.relpath(os.path.join(r, f), self.hkb)
                    self.medien.add(rel.replace(os.sep, "/"))

    def praefix(self):
        return "/".join(t for t in (self.ablagepfad, self.base) if t)

    def verzeichnisse(self):
        aus = {}
        for name, e in self.typdefs.items():
            aus.setdefault(_verzeichnis(name, e["daten"]), []).append(name)
        return aus

    def aufloesen(self, ziel, aus_wurzeldatei=False):
        """(art, rest) — art ist 'notiz', 'medium' oder None."""
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
    fehlen = sorted(STANDARD_PROPTYPES - set(b.proptypes))
    for name in fehlen:
        befunde.append(Befund("proptypes/", "Der Standard-Property-Typ `%s` fehlt "
                                            "(§3.5.1)." % name))
    for name, e in sorted(b.proptypes.items()):
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
        for feld in ("created", "modified"):
            if feld not in d:
                befunde.append(Befund(e["rel"], "`%s` fehlt (§6.3)." % feld, HINWEIS))
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


def _verweise(b, befunde):
    for rel, e in sorted(b.notizen.items()):
        text = notiz.bauen(e["kopf"], ohne_code(e["body"]))
        for m in LINK.finditer(text):
            ziel, alias = m.group(1), m.group(2)
            art, rest = b.aufloesen(ziel)
            if art is None:
                befunde.append(Befund(e["rel"], "[[%s]] lässt sich nicht auflösen "
                                                "(§3.6)." % ziel))
            elif art == "medium" and rest not in b.medien:
                befunde.append(Befund(e["rel"], "[[%s]] zeigt auf keine vorhandene "
                                                "Mediendatei (§3.2.1)." % ziel))
            if alias is None:
                befunde.append(Befund(e["rel"], "[[%s]] trägt keinen Alias (§3.6)."
                                      % ziel, HINWEIS))
        if "/" in rel and rel.split("/", 1)[0] == "bundles":
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
            if not any(ziel in x for x in verwandt):
                andere = notiz.entfernen(notiz.entfernen(
                    e["kopf"], "related"), "rejected_links")
                if ziel not in andere:
                    befunde.append(Befund(e["rel"], "%s fehlt in `related` (§5.6)."
                                          % link, HINWEIS))
        if aliase != sorted(aliase):
            befunde.append(Befund(e["rel"], "Die Einträge unter `# Siehe auch` stehen "
                                            "nicht alphabetisch (§5.6).", HINWEIS))
        for ziel, link in ziele:
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


def pruefen(hkb):
    b = Bestand(hkb)
    befunde = []
    for f in PRUEFUNGEN:
        f(b, befunde)
    return b, befunde
