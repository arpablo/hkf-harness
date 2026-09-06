#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rauchprobe: hk-init legt eine saubere Ablage an, hk-lint findet, was kaputt ist.

    python3 test/smoke.py

Kein Testrahmen, keine Fremdpakete. Der Lauf endet mit 0, wenn alle Proben
zutreffen, sonst mit 1 und einer Zeile pro Fehlschlag.
"""
import glob
import pathlib
import io
import json, os, re, shutil, subprocess, sys, tempfile

WURZEL = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# Die vier Bereiche (Core §3.1)
WIKI, QUELLEN, MEDIEN, KONFIG = "40-Wiki", "50-Sources", "80-Media", "90-System"
AUSGABE = "60-Output"   # der fuenfte Bereich (Core §3.2.4)
# Wo eine Ablage ihre eigenen Festlegungen fuehrt (Harness §7)
ablage_hinweise = "Hints"
BIN = os.path.join(WURZEL, "bin")
fehler = []


def lauf(*args, **kw):
    return subprocess.run(list(args), capture_output=True, text=True, **kw)


def _schreib(pfad, inhalt):
    ordner = os.path.dirname(pfad)
    if ordner and not os.path.isdir(ordner):
        os.makedirs(ordner)
    io.open(pfad, "w", encoding="utf-8").write(inhalt)


def probe(name, bedingung, hinweis=""):
    print("  %-52s %s" % (name, "ok" if bedingung else "FEHLT"))
    if not bedingung:
        fehler.append(name + ((" — " + hinweis) if hinweis else ""))


def _lieferung_kaputt(bundle):
    """Was §7.1 einer Lieferung verbietet."""
    io.open(os.path.join(bundle, "hbundle.md"), "a", encoding="utf-8").write(
        "\n# Import 1\n\nGehoert der aufnehmenden Wissensbasis.\n")
    io.open(os.path.join(bundle, "dinge", "eins.md"), "a", encoding="utf-8")
    p = os.path.join(bundle, "dinge", "eins.md")
    t = io.open(p, encoding="utf-8").read()
    io.open(p, "w", encoding="utf-8").write(
        t.replace("---\n\n", "bundles:\n  - \"[[Bundles/probe|Probe]]\"\n---\n\n", 1))
    os.makedirs(os.path.join(bundle, "woanders"), exist_ok=True)
    io.open(os.path.join(bundle, "woanders", "zwei.md"), "w",
            encoding="utf-8").write(
        "---\ntype: ding\ntitle: Noch ein Zweites\n"
        "modified: 2026-01-01T00:00:00\n---\n\nDoppelter Dateiname.\n")
    io.open(os.path.join(bundle, "Typedefs", "kiste.md"), "w",
            encoding="utf-8").write(
        "---\ntype: typedef\nprovisional: true\n"
        "description: Vorläufig, gehört nicht in eine Lieferung.\n"
        "modified: 2026-01-01T00:00:00\n---\n")


def _tabellenfehler(ziel):
    """Eine Typdefinition, die gegen §3.7.1 verstoesst, und Notizen dazu."""
    os.makedirs(os.path.join(ziel, WIKI, "dinge"), exist_ok=True)
    io.open(os.path.join(ziel, KONFIG, "Typedefs", "ding.md"), "w", encoding="utf-8").write(
        "---\ntype: typedef\ntitle: Ding\ndescription: Ein Ding.\ndir: dinge\n"
        "created: 2026-01-01\nmodified: 2026-01-01T00:00:00\n---\n\n"
        "# Properties\n\n| Property | Typ | Pflicht | Beschreibung |\n"
        "|---|---|---|---|\n"
        "| menge | number | ja | Wie viele |\n"
        "| netz | hkf-url | nein | Eine Adresse |\n"
        "| kiste | hkf-link:kiste | nein | Zeigt auf eine Kiste |\n"
        "| bild | hkf-file:image | nein | Ein Bild |\n"
        "| krumm | hkf-krumm | nein | Gibt es nicht |\n"
        "| falsch | hkf-url:person | nein | Zusatz am falschen Typ |\n"
        "| gemischt | text / number | nein | Zwei Wertformen |\n")
    io.open(os.path.join(ziel, KONFIG, "Typedefs", "wurf.md"), "w", encoding="utf-8").write(
        "---\ntype: typedef\ntitle: Wurf\ndescription: Vorgaben, gute und schlechte.\n"
        "created: 2026-01-01\nmodified: 2026-01-01T00:00:00\n---\n\n"
        "# Properties\n\n| Property | Typ | Pflicht | Vorgabe | Beschreibung |\n"
        "|---|---|---|---|---|\n"
        "| offen | checkbox | nein | false | So geht eine Vorgabe |\n"
        "| zaehlt | number | nein | viele | Vorgabe ist keine Zahl |\n"
        "| noetig | text | ja | irgendwas | Pflicht und Vorgabe zugleich |\n")
    io.open(os.path.join(ziel, WIKI, "dinge", "eins.md"), "w", encoding="utf-8").write(
        "---\ntype: ding\ntitle: Das Erste\ncreated: 2026-01-01\n"
        "modified: 2026-01-01T00:00:00\nnetz: kein-url\n"
        "kiste: \"[[" + WIKI + "/dinge/zwei|Das Zweite]]\"\n"
        "bild: \"[[" + WIKI + "/dinge/zwei|Das Zweite]]\"\n---\n\nEins.\n")
    io.open(os.path.join(ziel, WIKI, "dinge", "zwei.md"), "w", encoding="utf-8").write(
        "---\ntype: ding\ntitle: Das Zweite\nmenge: 2\ncreated: 2026-01-01\n"
        "modified: 2026-01-01T00:00:00\n---\n\nZwei.\n")


def _kaputt(ziel):
    """Baut in eine frische Ablage ein, was --fix wieder gerade zieht."""
    import re as _re
    p = os.path.join(ziel, "hkb.md")
    t = io.open(p, encoding="utf-8").read()
    io.open(p, "w", encoding="utf-8").write(
        _re.sub(r"^\| bundle \|.*\n", "", t, flags=_re.M))
    os.remove(os.path.join(ziel, KONFIG, "Proptypes", "hkf-phone.md"))
    os.makedirs(os.path.join(ziel, WIKI, "dinge"), exist_ok=True)
    io.open(os.path.join(ziel, KONFIG, "Typedefs", "ding.md"), "w", encoding="utf-8").write(
        "---\ntype: typedef\ntitle: Ding\ndescription: Ein Ding.\ndir: dinge\n"
        "created: 2026-01-01\nmodified: 2026-01-01T00:00:00\n---\n")
    io.open(os.path.join(ziel, WIKI, "dinge", "zwei.md"), "w", encoding="utf-8").write(
        "---\ntype: ding\ntitle: Das Zweite\ncreated: 2026-01-01\n"
        "modified: 2026-01-01T00:00:00\n---\n\nEin Ding.\n")
    io.open(os.path.join(ziel, WIKI, "dinge", "eins.md"), "w", encoding="utf-8").write(
        "---\ntype: ding\ntitle: Das Erste\nstatus:\n---\n\n"
        "Es zeigt auf [[zwei]].\n")


def _obsidian_kaputt(ziel):
    """Eine Vorlage und eine Base, wie Obsidian sie fuehrt, beide fehlerhaft.

    Nachgestellt sind die drei Faelle vom 06.09.2026: eine Vorlage mit einem
    `type`, das auf keine Typseite zeigt, eine Vorlage mit einer Property, die
    ihr Typ nicht kennt, und eine Base, die ueber ein Feld rechnet, das es
    nicht gibt, plus eine Einbettung, deren Alias keine Ansicht benennt.
    """
    v = os.path.join(ziel, KONFIG, "Templates")
    os.makedirs(v, exist_ok=True)
    _schreib(os.path.join(v, "Template Ding.md"),
             '---\ntype: "[[%s/Types/Kiste|Kiste]]"\nfarbe:\n---\n\nEin Ding.\n'
             % KONFIG)
    _schreib(os.path.join(v, "Template Note.md"),
             "---\ntype: note\nunfug: ja\n---\n\nEine Notiz.\n")
    bs = os.path.join(ziel, KONFIG, "Bases")
    os.makedirs(bs, exist_ok=True)
    _schreib(os.path.join(bs, "Note.base"),
             "filters:\n  and:\n    - type == link(\"note\")\n"
             "formulas:\n  wo: note.gibtsnicht\n"
             "views:\n  - type: table\n    name: Alle\n")
    _schreib(os.path.join(ziel, WIKI, "Notes", "schaufenster.md"),
             "---\ntype: note\ntitle: Schaufenster\ncreated: 2026-01-01\n"
             "modified: 2026-01-01T00:00:00\n---\n\n"
             "![[%s/Bases/Note.base|Note]]\n" % KONFIG)


def hkf_venv():
    return os.environ.get("HKF_VENV") or os.path.join(
        os.path.expanduser("~"), ".cache", "hkf-harness", "venv")


def _abbild(wurzel):
    """Was unter wurzel liegt, samt Inhalt — ohne .git."""
    aus = {}
    for r, dirs, fs in os.walk(wurzel):
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in fs:
            p = os.path.join(r, f)
            aus[os.path.relpath(p, wurzel)] = io.open(p, "rb").read()
    return aus


def _bundle_bauen(pfad):
    """Eine kleine Lieferung: ein Typ, zwei Notizen, eine Mediendatei."""
    shutil.rmtree(pfad, ignore_errors=True)
    for sub in ("Typedefs", "dinge", "bilder"):
        os.makedirs(os.path.join(pfad, sub))
    def schreib(rel, text):
        io.open(os.path.join(pfad, rel), "w", encoding="utf-8").write(text)
    schreib("hbundle.md",
            "---\nhkf: \"1.0\"\ntype: bundle\nid: probe\ntitle: Probe\n"
            "description: Zwei Dinge und ein Bild.\nversion: \"1\"\n---\n\n"
            "Eine Lieferung für die Rauchprobe.\n")
    schreib("Typedefs/ding.md",
            "---\ntype: typedef\ntitle: Ding\ndescription: Ein Ding.\ndir: dinge\n"
            "created: 2026-01-01\nmodified: 2026-01-01T00:00:00\n---\n\n"
            "# Properties\n\n"
            "| Property | Typ | Pflicht | Vorgabe | Beschreibung |\n"
            "|---|---|---|---|---|\n"
            "| menge | number | nein | — | Wie viele |\n"
            "| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands |\n")
    schreib("dinge/eins.md",
            "---\ntype: ding\ntitle: Das Erste\nwikidata_id: Q1\nmenge: 3\n"
            "created: 2026-01-01\nmodified: 2026-01-01T00:00:00\n---\n\n"
            "Es steht neben Das Zweite, ohne es zu verlinken.\n\n"
            "![[bilder/bild.png|bild.png]]\n")
    schreib("dinge/zwei.md",
            "---\ntype: ding\ntitle: Das Zweite\ncreated: 2026-01-01\n"
            "modified: 2026-01-01T00:00:00\n---\n\n"
            "Ein Ding für sich.\n")
    io.open(os.path.join(pfad, "bilder", "bild.png"), "wb").write(b"\x89PNG\r\n")


def main():
    ziel = tempfile.mkdtemp(prefix="hkb-probe-")
    shutil.rmtree(ziel)
    try:
        print("hk-init")
        r = lauf(os.path.join(BIN, "hk-init"), ziel, "--name", "Probe")
        probe("legt an", r.returncode == 0, r.stderr.strip())
        probe("35 Notizen", "35 Notizen" in r.stdout, r.stdout.strip())
        wurzel = io.open(os.path.join(ziel, "hkb.md"), encoding="utf-8").read()
        probe("Wurzeldatei traegt den Namen", "name: Probe" in wurzel)
        probe("und die vier Bereiche (§3.1)",
              all(('%s: "%s"' % (k, v)) in wurzel for k, v in
                  (("wiki_base", "40-Wiki"), ("source_base", "50-Sources"),
                   ("media_base", "80-Media"), ("config_base", "90-System"))),
              wurzel)
        probe("der Quellenbereich steht bereit und ist leer (§3.2.2)",
              os.path.isdir(os.path.join(ziel, "50-Sources"))
              and not [d for d in os.listdir(os.path.join(ziel, "50-Sources"))
                       if not d.startswith(".")])
        probe("und `Clippings` ist das fünfte Medienverzeichnis (§3.2.1)",
              all(os.path.isdir(os.path.join(ziel, "80-Media", d))
                  for d in ("Images", "Videos", "Audios", "Documents",
                            "Clippings")))
        probe("Typedefs und Proptypes liegen unter config_base",
              os.path.isdir(os.path.join(ziel, "90-System", "Typedefs"))
              and os.path.isdir(os.path.join(ziel, "90-System", "Proptypes")))
        probe("und kein Typverzeichnis liegt in der Wurzel",
              not os.path.isdir(os.path.join(ziel, "Typedefs"))
              and not os.path.isdir(os.path.join(ziel, "Books")))
        probe("die Typtabelle nennt den vollen Ort (§3.1)",
              "| source | 50-Sources |" in wurzel
              and "| typedef | 90-System/Typedefs |" in wurzel, wurzel)
        probe("Git-Repository mit einem Commit",
              lauf("git", "-C", ziel, "log", "--oneline").stdout.count("\n") == 1)
        probe("legt keine AGENTS.md an",
              not os.path.exists(os.path.join(ziel, "AGENTS.md")))
        probe("und ignoriert sie auch nicht",
              "AGENTS.md" not in io.open(os.path.join(ziel, ".gitignore"),
                                         encoding="utf-8").read())
        probe("CLAUDE.md gibt es nicht", not os.path.exists(os.path.join(ziel, "CLAUDE.md")))
        probe("verweigert ein nicht leeres Ziel",
              lauf(os.path.join(BIN, "hk-init"), ziel).returncode == 2)

        print("hk-lint")
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("frische Ablage ist sauber", r.returncode == 0, r.stdout.strip())
        probe("findet die Ablage ueber HKB_PATH",
              lauf(os.path.join(BIN, "hk-lint"), env=dict(os.environ, HKB_PATH=ziel)).returncode == 0)
        probe("weist ein Verzeichnis ohne hkb.md ab",
              lauf(os.path.join(BIN, "hk-lint"), tempfile.gettempdir()).returncode == 2)

        # eine Notiz mit falschem Frontmatter und kaputtem Wikilink
        io.open(os.path.join(ziel, KONFIG, "Typedefs", "kaputt.md"), "w", encoding="utf-8").write(
            "---\ntype: typedef\ntitle: \ncreated: gestern\n---\n\n"
            "Siehe [[persons/ada|Ada]] in einer Tabelle:\n\n"
            "| a | b |\n|---|---|\n| [[persons/ada|Ada]] | x |\n")
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("meldet Befunde", r.returncode == 1)
        probe("nennt das leere title", "title" in r.stdout, r.stdout)
        probe("nennt das falsche Datum", "created" in r.stdout, r.stdout)
        probe("nennt den unmaskierten Strich", "Tabellenzelle" in r.stdout, r.stdout)


        print("hk-lint --fix")
        # frisch anfangen: der Block davor hat absichtlich kaputt gemacht,
        # was --fix nicht reparieren darf
        shutil.rmtree(ziel)
        lauf(os.path.join(BIN, "hk-init"), ziel, "--name", "Probe")
        _kaputt(ziel)
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("findet die eingebauten Fehler",
              "Typtabelle nennt" in r.stdout and "hkf-phone` fehlt" in r.stdout,
              r.stdout)
        # Ein Ziel ohne Datei ist in einer HKB eine Vormerkung und kein
        # Defekt (§3.6). In einer Lieferung bleibt es ein Fehler, weil sie
        # zusagt, fuer sich lesbar zu sein.
        probe("ein Verweis ohne Ziel ist hier ein Hinweis",
              "zeigt auf keine Datei" in r.stdout, r.stdout[-400:])
        hinweisteil = r.stdout.split("Hinweise", 1)[-1]
        probe("und steht unter den Hinweisen, nicht unter den Befunden",
              "zeigt auf keine Datei" in hinweisteil, hinweisteil[:300])
        r = lauf(os.path.join(BIN, "hk-lint"), ziel, "--fix")
        probe("legt den fehlenden Standard-Property-Typ an",
              os.path.exists(os.path.join(ziel, KONFIG, "Proptypes", "hkf-phone.md")))
        probe("erzeugt die Typtabelle neu",
              "| ding | 40-Wiki/dinge |" in io.open(os.path.join(ziel, "hkb.md"),
                                                    encoding="utf-8").read())
        eins = io.open(os.path.join(ziel, WIKI, "dinge", "eins.md"), encoding="utf-8").read()
        probe("qualifiziert den verzeichnislosen Verweis",
              "[[40-Wiki/dinge/zwei|Das Zweite]]" in eins and "[[zwei]]" not in eins, eins)
        probe("ergaenzt created und modified",
              "created:" in eins and "modified:" in eins, eins)
        probe("setzt modified_by auf hk-lint", "modified_by: hk-lint" in eins, eins)
        probe("entfernt die leere Property", "status:" not in eins, eins)
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("danach ist die Ablage sauber", r.returncode == 0, r.stdout)
        r = lauf(os.path.join(BIN, "hk-lint"), ziel, "--strict")
        probe("--strict fasst je Typ zusammen",
              "ding: menge" not in r.stdout, r.stdout)
        # §3.1: zwei benannte Bereiche duerfen nicht ineinander liegen. Der
        # leere Bereich ist ausgenommen, ihn erlaubt dieselbe Stelle
        # ausdruecklich.
        wurzel = os.path.join(ziel, "hkb.md")
        vorher_wurzel = io.open(wurzel, encoding="utf-8").read()
        _schreib(wurzel, vorher_wurzel.replace(
            'source_base: "%s"' % QUELLEN, 'source_base: "%s/Quellen"' % WIKI))
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("ein Bereich im anderen ist ein Befund (§3.1)",
              "liegt unter `wiki_base`" in r.stdout, r.stdout[-400:])
        _schreib(wurzel, vorher_wurzel.replace('wiki_base: "%s"' % WIKI,
                                               'wiki_base: ""'))
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("ein leerer Bereich ist keiner, den erlaubt §3.1",
              "liegt unter" not in r.stdout, r.stdout[-400:])
        _schreib(wurzel, vorher_wurzel)
        # Der Abschnitt hiess bis zum 05.09.2026 `Siehe auch`. `--fix` ist der
        # Weg, auf dem eine Ablage aus jener Zeit den neuen Namen bekommt.
        alt = os.path.join(ziel, WIKI, "dinge", "alt.md")
        _schreib(alt, """---
type: ding
name: Alt
created: 2026-01-01
modified: 2026-01-01T00:00:00
---

Eine Notiz aus der Zeit vor der Umbenennung.

# Siehe auch

- [[40-Wiki/dinge/eins|Das Erste]] — steht hier als Muster.
""")
        lauf(os.path.join(BIN, "hk-lint"), ziel, "--fix")
        inhalt = io.open(alt, encoding="utf-8").read()
        probe("`--fix` benennt `# Siehe auch` in `# Verbindungen` um",
              "# Verbindungen" in inhalt and "# Siehe auch" not in inhalt, inhalt)
        probe("und die Leerzeile hinter der Ueberschrift bleibt",
              "# Verbindungen\n\n- [[" in inhalt, repr(inhalt[-120:]))
        shutil.rmtree(ziel)
        lauf(os.path.join(BIN, "hk-init"), ziel, "--name", "Probe")

        print("Property-Tabellen gegen die Werte")
        shutil.rmtree(ziel)
        lauf(os.path.join(BIN, "hk-init"), ziel, "--name", "Probe")
        _tabellenfehler(ziel)
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        for was, muster in (
                ("Pflichtangabe", "`menge` ist Pflicht und fehlt"),
                ("pattern", "passt nicht auf das `pattern`"),
                ("Zieltyp eines hkf-link", "zeigt auf `ding`, verlangt ist kiste"),
                ("Medienart eines hkf-file", "zeigt auf keine Mediendatei"),
                ("unbekannten Typ in der Tabelle",
                 "weder Wertform noch Property-Typ"),
                ("nicht registrierten Zieltyp", "ist nicht registriert"),
                ("den :-Zusatz am falschen Typ", "`:`-Zusatz steht nur"),
                ("Alternativen mit verschiedenen Wertformen",
                 "verschiedene Wertformen"),
                ("eine Vorgabe, die ihre Wertform verfehlt",
                 "Die Vorgabe ist kein number"),
                ("eine Vorgabe an einer Pflicht-Property",
                 "ist Pflicht und trägt zugleich die Vorgabe")):
            probe("meldet %s" % was, muster in r.stdout, r.stdout)
        probe("und laesst die gueltige Vorgabe in Ruhe",
              "`offen`" not in r.stdout, r.stdout)
        probe("und keine dieser Meldungen ist behebbar",
              "menge" not in lauf(os.path.join(BIN, "hk-lint"), ziel,
                                  "--fix").stdout.split("Korrigiert")[-1]
              .split("Dateien geprüft")[0])
        shutil.rmtree(ziel)
        lauf(os.path.join(BIN, "hk-init"), ziel, "--name", "Probe")

        print("Vorlagen und Bases: was Obsidian gehört, aber Notizen macht")
        _obsidian_kaputt(ziel)
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        for was, muster in (
                ("eine Vorlage, deren `type` auf keine Typseite zeigt",
                 "dort liegt keine Typseite mit Typdefinition"),
                ("eine Vorlage mit einer Property, die ihr Typ nicht führt",
                 "nennt Properties, die `note` nicht führt: unfug"),
                ("eine Base, die über ein unbekanntes Feld rechnet",
                 "rechnet über Properties, die keine Typdefinition führt: "
                 "`gibtsnicht`"),
                ("eine Einbettung, deren Alias keine Ansicht benennt",
                 "führt keine Ansicht `Note`, sondern `Alle`")):
            probe("meldet %s" % was, muster in r.stdout, r.stdout)
        probe("und `--fix` rät keine Ansicht",
              "Alle]]" not in io.open(
                  os.path.join(ziel, WIKI, "Notes", "schaufenster.md"),
                  encoding="utf-8").read()
              if lauf(os.path.join(BIN, "hk-lint"), ziel, "--fix") else True)
        shutil.rmtree(ziel)
        lauf(os.path.join(BIN, "hk-init"), ziel, "--name", "Probe")

        print("hk-import")
        bundle = os.path.join(ziel, "..", "probe-bundle")
        bundle = os.path.abspath(bundle)
        _bundle_bauen(bundle)
        r = lauf(os.path.join(BIN, "hk-import"), "--check", bundle, ziel)
        probe("--check meldet die drei neuen Notizen",
              "3 neu" in r.stdout and "Nichts wurde geschrieben" in r.stdout, r.stdout)
        probe("--check schreibt nichts", not os.path.exists(os.path.join(ziel, WIKI, "dinge")))

        r = lauf(os.path.join(BIN, "hk-import"), bundle, ziel)
        probe("übernimmt die Lieferung", r.returncode == 0, r.stdout + r.stderr)
        for f in (KONFIG + "/Typedefs/ding.md", WIKI + "/dinge/eins.md",
                  WIKI + "/dinge/zwei.md", WIKI + "/Bundles/probe.md",
                  MEDIEN + "/Images/bilder/bild.png"):
            probe("legt %s an" % f, os.path.exists(os.path.join(ziel, f)))
        eins = io.open(os.path.join(ziel, WIKI, "dinge", "eins.md"), encoding="utf-8").read()
        probe("trägt die Zugehörigkeit ein", "Bundles/probe|Probe" in eins, eins)
        probe("schreibt den Verweis, den der Body hergibt",
              "# Verbindungen" in eins and "dinge/zwei|Das Zweite" in eins, eins)
        probe("führt ihn auch in related", "related:" in eins, eins)
        zwei = io.open(os.path.join(ziel, WIKI, "dinge", "zwei.md"), encoding="utf-8").read()
        probe("und keinen Gegeneintrag (§5.6)", "# Verbindungen" not in zwei, zwei)
        probe("schreibt den Wikilink auf den Pfad der HKB um",
              "[[80-Media/Images/bilder/bild.png|" in eins, eins)
        probe("Typtabelle in hkb.md ergänzt",
              "| ding | 40-Wiki/dinge |" in io.open(os.path.join(ziel, "hkb.md"),
                                                    encoding="utf-8").read())

        vorher = _abbild(ziel)
        lauf(os.path.join(BIN, "hk-import"), bundle, ziel)
        probe("ein zweiter Lauf ändert nichts", _abbild(ziel) == vorher)

        # Bedeutungspruefung: derselbe Name, andere Beschreibung
        p = os.path.join(ziel, KONFIG, "Typedefs", "ding.md")
        t = io.open(p, encoding="utf-8").read()
        io.open(p, "w", encoding="utf-8").write(
            t.replace("description: Ein Ding.", "description: Ein Datensatz."))
        vorher = _abbild(ziel)
        r = lauf(os.path.join(BIN, "hk-import"), bundle, ziel)
        probe("weist bei offener Bedeutungsprüfung ab",
              r.returncode == 1 and "abgewiesen" in r.stdout, r.stdout)
        probe("und schreibt dabei nichts", _abbild(ziel) == vorher)
        io.open(p, "w", encoding="utf-8").write(t)          # wieder herstellen

        # §3.7: Eine Vorgabe sagt, was Abwesenheit bedeutet — zwei Typen, die
        # darin auseinandergehen, sind nicht dasselbe.
        io.open(p, "w", encoding="utf-8").write(
            t.replace("| menge | number | nein | — |",
                      "| menge | number | nein | 0 |"))
        assert "| menge | number | nein | 0 |" in io.open(p, encoding="utf-8").read()
        vorher = _abbild(ziel)
        r = lauf(os.path.join(BIN, "hk-import"), bundle, ziel)
        probe("eine abweichende Vorgabe hebt die Zusicherung auf (§3.7)",
              r.returncode == 1 and "Bedeutungsprüfung" in r.stdout, r.stdout)
        probe("und auch dann wird nichts geschrieben", _abbild(ziel) == vorher)
        io.open(p, "w", encoding="utf-8").write(t)

        # §8 — eine Lieferung aus einer spaeteren Fassung wird gelesen,
        # aber nicht uebernommen
        fremd = os.path.join(os.path.dirname(bundle), "probe-fremd")
        _bundle_bauen(fremd)
        hb = os.path.join(fremd, "hbundle.md")
        text = io.open(hb, encoding="utf-8").read()
        io.open(hb, "w", encoding="utf-8").write(
            text.replace('hkf: "1.0"', 'hkf: "9.9"').replace("id: probe", "id: fremd"))
        vorher = _abbild(ziel)
        r = lauf(os.path.join(BIN, "hk-import"), fremd, ziel)
        probe("weist eine unbekannte Fassung ab (§8)",
              r.returncode == 1 and "§8" in r.stdout, r.stdout)
        probe("und schreibt auch dann nichts", _abbild(ziel) == vorher)

        print("Eigenes Python")
        zeig = os.path.join(os.path.dirname(bundle), "zeig.py")
        io.open(zeig, "w", encoding="utf-8").write(
            "import os, sys\n"
            "sys.path.insert(0, %r)\n"
            "import hkf\n"
            "import yaml\n"
            "print(sys.executable)\n"
            "print(sys.version.split()[0], yaml.__version__)\n"
            % os.path.join(WURZEL, "lib"))
        r = lauf(sys.executable, zeig)
        zeilen = r.stdout.strip().splitlines()
        soll = io.open(os.path.join(WURZEL, ".python-version"),
                       encoding="utf-8").read().strip()
        probe("ein Skript laeuft unter der venv des Harness",
              zeilen and zeilen[0].startswith(hkf_venv()), r.stdout + r.stderr)
        probe("und zwar unter Python %s" % soll,
              len(zeilen) > 1 and zeilen[1].startswith(soll), r.stdout + r.stderr)
        r = lauf(sys.executable, "-c", "import sys; print(sys.executable)")
        probe("python -c wird nicht umgeleitet",
              r.stdout.strip() == sys.executable, r.stdout)

        print("Die KI-Schicht")
        skills = os.path.join(WURZEL, "skills")
        namen = sorted(d for d in os.listdir(skills)
                       if os.path.isdir(os.path.join(skills, d)))
        probe("es gibt Skills", len(namen) >= 5, ", ".join(namen))
        befehle, fehlt = set(), []
        for name in namen:
            p_skill = os.path.join(skills, name, "SKILL.md")
            if not os.path.isfile(p_skill):
                fehlt.append("%s/SKILL.md" % name)
                continue
            t = io.open(p_skill, encoding="utf-8").read()
            kopf = t.split("---")[1] if t.startswith("---") else ""
            if ("name: %s" % name) not in kopf or "description:" not in kopf:
                fehlt.append("%s: Frontmatter" % name)
            befehle |= set(re.findall(r"\bhk-[a-z]+", t))
        probe("jeder hat ein SKILL.md mit passendem Frontmatter",
              not fehlt, ", ".join(fehlt))
        ohne = sorted(b for b in befehle
                      if not os.path.exists(os.path.join(BIN, b)))
        probe("jeder genannte Befehl liegt in bin/", not ohne, ", ".join(ohne))

        # Bis hierher stand nur die Skillseite unter Aufsicht. Ein Agent, den
        # ein Skill ruft, konnte fehlen, ohne dass es auffiel — und ein Verweis
        # auf einen Agenten, den es nicht gibt, ist genau der Fehler, der sich
        # beim Zusammenlegen zweier Bestaende fortpflanzt.
        ordner = os.path.join(WURZEL, "agents")
        agenten = sorted(d[:-3] for d in os.listdir(ordner)
                         if d.endswith(".md"))
        probe("es gibt Agenten", len(agenten) >= 1, ", ".join(agenten))
        maengel = []
        for name in agenten:
            t_ag = io.open(os.path.join(ordner, name + ".md"),
                           encoding="utf-8").read()
            kopf = t_ag.split("---")[1] if t_ag.startswith("---") else ""
            for feld in ("name: %s" % name, "description:", "tools:", "model:"):
                if feld not in kopf:
                    maengel.append("%s: %s" % (name, feld.rstrip(":")))
        probe("jeder hat Frontmatter mit name, description, tools, model",
              not maengel, ", ".join(maengel))
        gerufen = set()
        for name in namen:
            t_sk = io.open(os.path.join(skills, name, "SKILL.md"),
                           encoding="utf-8").read()
            # Die Rueckversicherung sind die Backticks, nicht das naechste
            # Wort. Ohne sie las die Probe aus "je Batch einen Agenten
            # starten" den Agentennamen `starten` und meldete ihn als
            # unbekannt. Ein Agentenname steht in diesen Texten immer als
            # Code, entweder hinter "Agent" oder als `subagent_type`.
            gerufen |= set(re.findall(
                r"(?:Subagenten?|Agenten?(?:typ)?)\s+`([a-z][a-z0-9-]*)`", t_sk))
            gerufen |= set(re.findall(
                r"`subagent_type`\s*:\s*`([a-z][a-z0-9-]*)`", t_sk))
        unbekannt = sorted(g for g in gerufen if g not in agenten)
        probe("jeder von einem Skill gerufene Agent liegt in agents/",
              not unbekannt, ", ".join(unbekannt))

        # Ein Verweis auf eine Datei, die es nicht gibt, faellt niemandem auf.
        # In einem fremden Vault zeigte ein Skill zwei Jahre lang auf zwei
        # Ordner, die mit einem Umzug verschwunden waren.
        bausteine = ([os.path.join(WURZEL, "skills", "README.md")] +
                     [os.path.join(skills, n, "SKILL.md") for n in namen] +
                     [os.path.join(ordner, a + ".md") for a in agenten] +
                     sorted(glob.glob(os.path.join(WURZEL, "commands", "*.md"))))
        tot = []
        for datei in bausteine:
            text = io.open(datei, encoding="utf-8").read()
            kurz = os.path.relpath(datei, WURZEL)
            for zielpfad in re.findall(r"\]\(([^)\s]+)\)", text):
                if zielpfad.startswith(("http", "#", "mailto:")):
                    continue
                voll = os.path.normpath(os.path.join(
                    os.path.dirname(datei), zielpfad.split("#")[0]))
                if not os.path.exists(voll):
                    tot.append("%s -> %s" % (kurz, zielpfad))
            # Ein blosser `[[name]]` in kebab-case meint einen Baustein von
            # hier. Die Beispiele in den Skills tragen einen Pfad oder einen
            # Alias und fallen nicht darunter.
            for wl in re.findall(r"\[\[([a-z][a-z0-9-]*)\]\]", text):
                if wl not in namen and wl not in agenten:
                    tot.append("%s -> [[%s]]" % (kurz, wl))
        probe("jeder Verweis zwischen den Bausteinen trägt", not tot,
              "; ".join(tot))

        print("Das Plugin")
        p_manifest = os.path.join(WURZEL, ".claude-plugin", "plugin.json")
        p_markt = os.path.join(WURZEL, ".claude-plugin", "marketplace.json")
        try:
            manifest = json.load(io.open(p_manifest, encoding="utf-8"))
        except Exception as e:
            manifest = {}
            probe("das Manifest ist lesbar", False, str(e))
        probe("das Manifest nennt Name, Fassung und Zweck",
              all(k in manifest for k in ("name", "version", "description")),
              ", ".join(sorted(manifest)))
        try:
            markt = json.load(io.open(p_markt, encoding="utf-8"))
        except Exception as e:
            markt = {}
            probe("der Marktplatz ist lesbar", False, str(e))
        eintraege = markt.get("plugins") or []
        probe("der Marktplatz nennt dasselbe Plugin",
              len(eintraege) == 1
              and eintraege[0].get("name") == manifest.get("name")
              and eintraege[0].get("source") == "./",
              str(eintraege))
        # Nur `plugin.json` gehoert in `.claude-plugin/`. Die Bausteine liegen
        # an der Wurzel, sonst findet Claude Code sie nicht.
        drin = sorted(os.listdir(os.path.join(WURZEL, ".claude-plugin")))
        probe("in .claude-plugin/ liegen nur die beiden Manifeste",
              drin == ["marketplace.json", "plugin.json"], ", ".join(drin))
        ohne = []
        for datei in sorted(glob.glob(os.path.join(WURZEL, "commands", "*.md"))):
            text = io.open(datei, encoding="utf-8").read()
            kopf = text.split("---")[1] if text.startswith("---") else ""
            if "description:" not in kopf:
                ohne.append(os.path.basename(datei))
        probe("jedes Slash-Kommando hat eine Beschreibung", not ohne,
              ", ".join(ohne))
        r = lauf(os.path.join(BIN, "hk-install"), "--check")
        probe("hk-install berichtet, ohne zu ändern", r.returncode in (0, 1),
              (r.stdout + r.stderr)[-300:])

        print("hk-text: die Schreibregeln gelten auch in einer Ablage")
        r = lauf(os.path.join(BIN, "hk-text"), "--help")
        probe("das Werkzeug laeuft", r.returncode == 0, r.stdout + r.stderr)
        muster = os.path.join(ziel, WIKI, "Notes", "probe.md")
        _schreib(muster, """---
type: note
name: Probe
created: 2026-01-01
---

# Zweck

Ein Satz mit einem Gedankenstrich \u2014 der ist verboten.

| Property | Vorgabe | Zweck |
|---|---|---|
| `name` | \u2014 | Der Name; mit Strichpunkt. |

# Verbindungen

- [[40-Wiki/Notes/anderes|Anderes]] \u2014 der Grund steht hier.
""")
        r = lauf(os.path.join(BIN, "hk-text"), muster)
        probe("der Bericht endet mit 0", r.returncode == 0, r.stdout + r.stderr)
        probe("der Gedankenstrich im Fliesstext ist ein Fehler",
              "7:35" in r.stdout or "Em-Dash" in r.stdout, r.stdout)
        probe("der Strichpunkt in der Tabelle auch",
              "forbidden_punctuation" in r.stdout, r.stdout)
        probe("die leere Vorgabe `\u2014` ist keiner (§3.7)",
              r.stdout.count("Em-Dash") == 1, r.stdout)
        probe("der Trenner in `# Verbindungen` auch nicht (§5.6)",
              r.stdout.count("Em-Dash") == 1, r.stdout)
        r = lauf(os.path.join(BIN, "hk-text"), "--gate", muster)
        probe("--gate endet mit 1", r.returncode == 1, r.stdout + r.stderr)
        os.remove(muster)
        # Ein `ai-`-Callout traegt einen englischen Bildprompt und bleibt
        # ungeprueft. Sein `alt:`-Feld ist deutsche Prosa. Ohne die Ausnahme
        # von der Ausnahme faellt es durch jedes Netz, denn der Hook springt
        # zwar bei jedem Schreibzugriff an, ueberspringt aber den Callout.
        _schreib(muster, """---
type: note
name: Probe
created: 2026-01-01
---

# Zweck

> [!ai-image]
> alt: "Ein Blick ueber die Kueste."
> project: Hennibock
>
> A coastal view — an English prompt with an em-dash and a semicolon; both fine.

Ein gewoehnlicher Satz.
""")
        r = lauf(os.path.join(BIN, "hk-text"), muster)
        probe("die Ersatzform im Alt-Text ist ein Fehler",
              "umlaut_replacements" in r.stdout, r.stdout)
        probe("der Bildprompt darunter bleibt ungeprueft",
              "Em-Dash" not in r.stdout
              and "forbidden_punctuation" not in r.stdout, r.stdout)
        os.remove(muster)
        # Die Grundausstattung wandert in jede neue Ablage. Was hier
        # steht, steht ueberall, und darum steht es unter derselben Regel.
        r = lauf(os.path.join(BIN, "hk-text"), "--gate", ziel)
        probe("eine frische Ablage kommt durch den Gate",
              r.returncode == 0, (r.stdout + r.stderr)[-400:])
        # Was **diese** Ablage fuer sich festlegt, steht als Notiz vom Typ
        # `hint` darin (Harness §7). Der Lader kennt json-Bloecke in Markdown
        # schon, es braucht dafuer keine zweite Mechanik.
        _schreib(os.path.join(ziel, WIKI, "Hints", "schreibregeln.md"), """---
type: hint
name: Schreibregeln dieser Ablage
created: 2026-01-01
---

# Zweck

Diese Ablage verbietet ein Wort mehr als der Basissatz.

```json
{"writing_policy": {"version": 1, "checks": {
  "forbidden_stems": {"severity": "error", "stems": ["Zeitenwende"]}}}}
```
""")
        _schreib(muster, """---
type: note
name: Probe
created: 2026-01-01
---

# Zweck

Die Zeitenwende kam, und mit ihr eine entscheidende Frage.
""")
        r = lauf(os.path.join(BIN, "hk-text"), muster)
        probe("eine `hint`-Notiz steuert eigene Regeln bei",
              "Zeitenwende" in r.stdout, r.stdout)
        probe("der Basissatz gilt daneben weiter",
              "entscheidende" in r.stdout, r.stdout)
        os.remove(muster)
        # Die Probe raeumt hinter sich auf. Was sie stehen liesse, faende die
        # naechste als Befund wieder.
        shutil.rmtree(os.path.join(ziel, WIKI, "Hints"))

        for name in ("test_deutsch", "test_engine", "test_rules",
                     "test_segment"):
            r = lauf(sys.executable,
                     os.path.join(WURZEL, "test", "text", name + ".py"))
            probe("%s laeuft durch" % name, r.returncode == 0,
                  (r.stdout + r.stderr)[-400:])

        print("hk-ablage: welche Ablage bearbeitet wird")
        wahl = os.path.join(ziel, "wahl.json")
        umgebung = dict(os.environ, HKF_WAHL=wahl)
        umgebung.pop("HKB_PATH", None)
        r = lauf(os.path.join(BIN, "hk-ablage"), ziel, env=umgebung, cwd=ziel)
        probe("eine Ablage laesst sich waehlen", r.returncode == 0,
              r.stdout + r.stderr)
        probe("die Wahl steht auf der Platte", os.path.isfile(wahl))
        r = lauf(os.path.join(BIN, "hk-ablage"), env=umgebung, cwd=ziel)
        probe("und gilt beim naechsten Aufruf",
              "der gemerkten Wahl" in r.stdout, r.stdout)
        r = lauf(os.path.join(BIN, "hk-lint"), env=umgebung, cwd=ziel)
        probe("hk-lint nimmt sie ohne Argument", r.returncode == 0,
              (r.stdout + r.stderr)[-300:])
        oben = os.path.dirname(ziel)
        r = lauf(os.path.join(BIN, "hk-ablage"), "--liste", env=umgebung,
                 cwd=oben)
        probe("--liste zeigt, was danebenliegt",
              os.path.basename(ziel) in r.stdout, r.stdout)
        r = lauf(os.path.join(BIN, "hk-ablage"), "--loeschen", env=umgebung,
                 cwd=ziel)
        probe("die Wahl laesst sich zuruecknehmen", r.returncode == 0,
              r.stdout + r.stderr)
        r = lauf(os.path.join(BIN, "hk-ablage"), env=umgebung, cwd=ziel)
        probe("dann gilt wieder das Arbeitsverzeichnis",
              "dem Arbeitsverzeichnis" in r.stdout, r.stdout)

        print("hk-suche: Notizen finden, ohne das Dateisystem abzugrasen")
        _schreib(os.path.join(ziel, WIKI, "Persons", "ada-lovelace.md"), """---
type: person
name: Ada Lovelace
aliases:
  - Ada Byron
created: 2026-01-01
---

# Zweck

Mathematikerin.
""")
        _schreib(os.path.join(ziel, WIKI, "Events", "erste.md"), """---
type: event
name: Erste
created: 2026-01-01
---

# Zweck

Ada Lovelace schrieb das erste Programm.

## Ein Titel mit Ada Lovelace darin

| Spalte | Ada Lovelace |
|---|---|
| a | b |

Und `Ada Lovelace` in Code.
""")
        _schreib(os.path.join(ziel, WIKI, "Events", "zweite.md"), """---
type: event
name: Zweite
created: 2026-01-01
---

# Zweck

Hier steht [[40-Wiki/Persons/ada-lovelace|Ada Lovelace]] schon verlinkt.
""")
        r = lauf(os.path.join(BIN, "hk-suche"), "--typ", "person", ziel)
        probe("--typ findet die Notizen eines Typs",
              "ada-lovelace" in r.stdout and r.returncode == 0, r.stdout[-200:])
        r = lauf(os.path.join(BIN, "hk-suche"), "Mathematikerin", ziel)
        probe("der Volltext findet sie auch", "ada-lovelace" in r.stdout,
              r.stdout[-200:])
        r = lauf(os.path.join(BIN, "hk-suche"), "--verweist-auf",
                 "ada-lovelace", ziel)
        probe("--verweist-auf findet den Rückverweis",
              "Events/zweite" in r.stdout and "Events/erste" not in r.stdout,
              r.stdout[-300:])
        r = lauf(os.path.join(BIN, "hk-suche"), "gibtesnicht", ziel)
        probe("ohne Treffer endet der Lauf mit 1", r.returncode == 1, r.stdout)

        print("hk-erwaehnungen: was schon dasteht, wird ein Verweis")
        vorher = _abbild(ziel)
        r = lauf(os.path.join(BIN, "hk-erwaehnungen"), "ada-lovelace", ziel)
        probe("der Bericht nennt die Fundstelle",
              "Events/erste" in r.stdout, r.stdout[-300:])
        probe("und die Notiz, die schon verlinkt, bleibt aussen vor",
              "Events/zweite" not in r.stdout, r.stdout[-300:])
        probe("die Grundausstattung wird nicht angefasst (Regel 6)",
              "Proptypes/" not in r.stdout and "Typedefs/" not in r.stdout,
              r.stdout[-300:])
        probe("ohne --setzen ändert sich nichts", _abbild(ziel) == vorher)
        r = lauf(os.path.join(BIN, "hk-erwaehnungen"), "ada-lovelace", ziel,
                 "--setzen")
        probe("--setzen schreibt", r.returncode == 0, r.stdout[-200:])
        gesetzt = io.open(os.path.join(ziel, WIKI, "Events", "erste.md"),
                          encoding="utf-8").read()
        probe("der Verweis ist qualifiziert und trägt den alten Text",
              "[[40-Wiki/Persons/ada-lovelace|Ada Lovelace]] schrieb" in gesetzt,
              gesetzt[-400:])
        probe("die Überschrift bleibt unberührt",
              "## Ein Titel mit Ada Lovelace darin" in gesetzt)
        probe("die Tabellenzeile auch", "| Spalte | Ada Lovelace |" in gesetzt)
        probe("und der Inline-Code", "`Ada Lovelace` in Code" in gesetzt)
        probe("nur die erste Fundstelle je Notiz",
              gesetzt.count("[[40-Wiki/Persons/ada-lovelace|") == 1, gesetzt[-400:])
        probe("`modified_by` steht drin (Regel 5)",
              "modified_by: hk-erwaehnungen" in gesetzt, gesetzt[:200])
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("die Ablage bleibt konform", r.returncode == 0,
              (r.stdout + r.stderr)[-300:])
        for f in ("Persons/ada-lovelace.md", "Events/erste.md",
                  "Events/zweite.md"):
            os.remove(os.path.join(ziel, WIKI, f))
        for d in ("Persons", "Events"):
            os.rmdir(os.path.join(ziel, WIKI, d))

        print("hkf-geo: eine Koordinate ist ein Paar")
        geo = os.path.join(tempfile.mkdtemp(prefix="hkb-geo-"), "ablage")
        lauf(os.path.join(BIN, "hk-init"), geo)
        tp = os.path.join(geo, KONFIG, "Typedefs", "city.md")
        _schreib(tp, io.open(tp, encoding="utf-8").read().replace(
            "| latitude |",
            "| location | hkf-geo | nein | — | Breite und Länge als Paar |\n| latitude |", 1))
        for name, ort in (("berlin", '  - "52.5200"\n  - "13.4050"'),
                          ("drei", '  - "52.5"\n  - "13.4"\n  - "99"'),
                          ("text", '  - "Berlin"\n  - "13.4"')):
            _schreib(os.path.join(geo, WIKI, "Cities", name + ".md"), """---
type: city
name: %s
location:
%s
created: 2026-01-01
modified: 2026-01-01T00:00:00
---

# Zweck

Da.
""" % (name, ort))
        r = lauf(os.path.join(BIN, "hk-lint"), geo)
        probe("ein Paar aus zwei Dezimalgraden geht durch",
              "berlin.md: `location`" not in r.stdout, r.stdout[-500:])
        probe("drei Einträge sind ein Befund (`items`)",
              "hat 3 Einträge, hkf-geo verlangt 2" in r.stdout, r.stdout[-500:])
        probe("ein Eintrag, der keine Zahl ist, auch",
              "text.md: `location` passt nicht auf das `pattern`" in r.stdout,
              r.stdout[-500:])
        shutil.rmtree(os.path.dirname(geo), ignore_errors=True)

        print("Was Obsidian mitbringt, sperrt HKF nicht aus")
        # Zwei Regeln, die an einem gewachsenen Vault zu eng waren.
        _schreib(os.path.join(ziel, QUELLEN, "quelle.md"), """---
type: source
name: Eine Quelle
kind: book
created: 2026-01-01
modified: 2026-01-01T00:00:00
---

# Zweck

Da.
""")
        _schreib(os.path.join(ziel, WIKI, "Notes", "obsidian.md"), """---
type: note
name: Probe
sources:
  - "[[50-Sources/quelle|Eine Quelle]]"
  - "https://example.org/etwas"
  - "[Ein Titel](https://example.org/anderes)"
  - "[Mit Klammern](https://example.org/Cairo_Conference_(1921))"
banner-x: 0.5
to-publish: true
created: 2026-01-01
modified: 2026-01-01T00:00:00
---

# Zweck

Verweist auf [[50-Sources/quelle|Eine Quelle]].
""")
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("`sources` nimmt Notiz, Adresse und Markdown-Link (A.2)",
              "sources" not in r.stdout.split("Hinweise", 1)[0],
              r.stdout.split("Hinweise", 1)[0][-400:])
        probe("ein Property-Name mit Bindestrich ist zulässig (§3.4)",
              "banner-x" not in r.stdout.split("Hinweise", 1)[0]
              and "to-publish" not in r.stdout.split("Hinweise", 1)[0],
              r.stdout.split("Hinweise", 1)[0][-400:])
        probe("die Ablage bleibt ohne Befund", r.returncode == 0,
              (r.stdout + r.stderr)[-300:])
        os.remove(os.path.join(ziel, WIKI, "Notes", "obsidian.md"))
        os.remove(os.path.join(ziel, QUELLEN, "quelle.md"))
        shutil.rmtree(os.path.join(ziel, WIKI, "Notes"), ignore_errors=True)

        print("Ein leerer Bereich fällt mit der Wurzel zusammen (§3.1)")
        # Ein gewachsener Vault legt seinen Inhalt nicht unter einen
        # Basispfad, sondern in Ordner nebeneinander. Dafuer darf ein Bereich
        # leer sein. Zwei Fehler steckten darin, und beide fielen erst an
        # einem echten Bestand auf: Jede Notiz wurde zweimal gelesen, und ein
        # Verweis unter dem leeren Bereich loeste nie auf.
        leer = os.path.join(tempfile.mkdtemp(prefix="hkb-leer-"), "ablage")
        lauf(os.path.join(BIN, "hk-init"), leer)
        w = io.open(os.path.join(leer, "hkb.md"), encoding="utf-8").read()
        _schreib(os.path.join(leer, "hkb.md"),
                 w.replace('wiki_base: "40-Wiki"', 'wiki_base: ""'))
        lauf(os.path.join(BIN, "hk-lint"), leer, "--fix")
        # `Bundles/` liegt unter `wiki_base` (§7.2). Faellt der mit der Wurzel
        # zusammen, liegt es dort.
        os.makedirs(os.path.join(leer, "Bundles"), exist_ok=True)
        io.open(os.path.join(leer, "Bundles", ".gitkeep"), "w").close()
        _schreib(os.path.join(leer, "Persons", "ada.md"), """---
type: person
name: Ada
created: 2026-01-01
modified: 2026-01-01T00:00:00
---

# Zweck

Da.
""")
        _schreib(os.path.join(leer, "Notes", "probe.md"), """---
type: note
name: Probe
created: 2026-01-01
modified: 2026-01-01T00:00:00
---

# Zweck

Ein Verweis auf [[Persons/ada|Ada]].
""")
        r = lauf(os.path.join(BIN, "hk-lint"), leer)
        probe("ein Verweis unter dem leeren Bereich löst auf",
              "zeigt auf keine Datei" not in r.stdout, r.stdout[-400:])
        probe("die Ablage ist ohne Befund", r.returncode == 0,
              (r.stdout + r.stderr)[-500:])
        import subprocess as _sp
        zahl = _sp.run([sys.executable, "-c",
                        "import sys; sys.path.insert(0, %r); "
                        "from hkf import pruefen; "
                        "print(len(pruefen.Bestand(%r, 'hkb').notizen))"
                        % (os.path.join(WURZEL, "lib"), leer)],
                       capture_output=True, text=True).stdout.strip()
        probe("jede Notiz steht genau einmal im Bestand",
              zahl == "37", "%s statt 37" % zahl)
        shutil.rmtree(os.path.dirname(leer), ignore_errors=True)

        print("hk-verweise: aus einem kurzen Verweis wird ein qualifizierter")
        vw = os.path.join(tempfile.mkdtemp(prefix="hkb-vw-"), "ablage")
        lauf(os.path.join(BIN, "hk-init"), vw)
        for name, typ in (("ada-lovelace", "person"), ("babbage", "person")):
            _schreib(os.path.join(vw, WIKI, "Persons", name + ".md"), """---
type: %s
name: %s
created: 2026-01-01
modified: 2026-01-01T00:00:00
---

# Zweck

Da.
""" % (typ, name))
        bild = os.path.join(vw, MEDIEN, "Images", "portraet.png")
        os.makedirs(os.path.dirname(bild), exist_ok=True)
        open(bild, "w").close()
        _schreib(os.path.join(vw, WIKI, "Notes", "probe.md"), """---
type: note
name: Probe
related:
  - "[[ada-lovelace]]"
created: 2026-01-01
modified: 2026-01-01T00:00:00
---

# Zweck

Ein Verweis auf [[ada-lovelace]] und einer mit Alias auf [[babbage|Babbage]].

Ein Bild: ![[portraet.png]]

Ins Leere: [[gibt-es-nicht]].

| Person | Rolle |
|---|---|
| [[ada-lovelace]] | mit `code` davor und [[babbage]] dahinter |

In Backticks bleibt `[[ada-lovelace]]` stehen.
""")
        vorher = _abbild(vw)
        r = lauf(os.path.join(BIN, "hk-verweise"), vw)
        probe("der Bericht zählt die kurzen Verweise",
              "6 Verweise" in r.stdout, r.stdout[-300:])
        probe("ohne --setzen ändert sich nichts", _abbild(vw) == vorher)
        probe("ein Ziel ohne Datei bleibt eine Vormerkung",
              "Vormerkungen" in r.stdout, r.stdout[-300:])
        r = lauf(os.path.join(BIN, "hk-verweise"), vw, "--setzen")
        probe("--setzen schreibt", r.returncode == 0, (r.stdout + r.stderr)[-200:])
        text_vw = io.open(os.path.join(vw, WIKI, "Notes", "probe.md"),
                          encoding="utf-8").read()
        probe("der Verweis trägt jetzt Pfad und Alias",
              "[[40-Wiki/Persons/ada-lovelace|ada-lovelace]]" in text_vw,
              text_vw[-500:])
        probe("ein vorhandener Alias bleibt stehen",
              "[[40-Wiki/Persons/babbage|Babbage]]" in text_vw, text_vw[-500:])
        probe("das Bild bekommt den Medienbereich",
              "![[80-Media/Images/portraet.png|portraet.png]]" in text_vw,
              text_vw[-500:])
        probe("in einer Tabellenzelle ist der Trenner maskiert (§3.6)",
              "[[40-Wiki/Persons/ada-lovelace\\|ada-lovelace]] | mit" in text_vw,
              text_vw[-400:])
        # Inline-Code teilt die Zeile nicht: auch dahinter ist es eine Zelle.
        probe("auch hinter einem Inline-Code in derselben Zeile",
              "[[40-Wiki/Persons/babbage\\|babbage]] dahinter" in text_vw,
              text_vw[-400:])
        probe("was in Backticks steht, bleibt unangetastet",
              "`[[ada-lovelace]]`" in text_vw, text_vw[-300:])
        probe("das Ziel ohne Datei steht noch da",
              "[[gibt-es-nicht]]" in text_vw, text_vw[-400:])
        probe("das Frontmatter bleibt in Anführungszeichen",
              '- "[[40-Wiki/Persons/ada-lovelace|ada-lovelace]]"' in text_vw,
              text_vw[:400])
        r = lauf(os.path.join(BIN, "hk-lint"), vw)
        probe("die Ablage ist danach ohne Befund", r.returncode == 0,
              (r.stdout + r.stderr)[-400:])
        # Zwei Dateien gleichen Namens: geraten wird nicht.
        _schreib(os.path.join(vw, WIKI, "Terms", "babbage.md"), """---
type: term
name: Babbage
lang: de
created: 2026-01-01
modified: 2026-01-01T00:00:00
---

# Zweck

Ein Begriff.
""")
        _schreib(os.path.join(vw, WIKI, "Notes", "zweite.md"), """---
type: note
name: Zweite
created: 2026-01-01
modified: 2026-01-01T00:00:00
---

# Zweck

Ein Verweis auf [[babbage]].
""")
        vorher = _abbild(vw)
        r = lauf(os.path.join(BIN, "hk-verweise"), vw, "--setzen")
        probe("bei zwei gleichnamigen Dateien wird nicht geraten",
              "Mehrdeutig" in r.stdout and "Terms/babbage" in r.stdout,
              r.stdout[-400:])
        probe("und der Verweis bleibt stehen",
              "[[babbage]]" in io.open(os.path.join(vw, WIKI, "Notes",
                                                    "zweite.md"),
                                       encoding="utf-8").read())
        shutil.rmtree(os.path.dirname(vw), ignore_errors=True)

        print("hkf-publikation: zwei Typen als Lieferung, nicht als Grundausstattung")
        # Auf einer Kopie. `hk-import` schreibt einen Nachweis in die
        # Lieferung zurueck, und eine Probe fasst das Repository nicht an.
        lieferung_pub = os.path.join(tempfile.mkdtemp(prefix="hkb-lief-"),
                                     "hkf-publikation")
        shutil.copytree(os.path.join(WURZEL, "bundles", "hkf-publikation"),
                        lieferung_pub)
        r = lauf(os.path.join(BIN, "hk-lint"), lieferung_pub)
        probe("die Lieferung ist konform", r.returncode == 0,
              (r.stdout + r.stderr)[-300:])
        r = lauf(os.path.join(BIN, "hk-publikation"), "irgendwas", ziel)
        probe("ohne die Typen sagt hk-publikation, was fehlt",
              r.returncode == 2 and "hk-import" in r.stderr, r.stderr[:200])
        r = lauf(os.path.join(BIN, "hk-import"), lieferung_pub, ziel)
        probe("sie lässt sich importieren", r.returncode == 0,
              (r.stdout + r.stderr)[-300:])
        wurzel_text = io.open(os.path.join(ziel, "hkb.md"),
                              encoding="utf-8").read()
        probe("und trägt sich in die Typtabelle ein",
              "| publication |" in wurzel_text and "| text |" in wurzel_text)

        print("hk-publikation: die Lesereihenfolge steht an drei Stellen gleich")
        _schreib(os.path.join(ziel, AUSGABE, "Publications", "sammlung.md"), """---
type: publication
name: Eine Sammlung
created: 2026-01-01
---

# Zweck

Drei Texte, die zusammen gelesen werden wollen.
""")
        for n in ("eins", "zwei", "drei"):
            _schreib(os.path.join(ziel, AUSGABE, "Texts", n + ".md"), """---
type: text
name: Stück %s
created: 2026-01-01
---

# Zweck

Der Text von Stück %s, mit ein paar Wörtern für die Zählung.
""" % (n, n))
        for n in ("eins", "zwei", "drei"):
            r = lauf(os.path.join(BIN, "hk-publikation"), "sammlung",
                     "--aufnehmen", n, ziel)
            if r.returncode:
                break
        probe("Texte lassen sich aufnehmen", r.returncode == 0,
              (r.stdout + r.stderr)[-300:])
        pub = io.open(os.path.join(ziel, AUSGABE, "Publications", "sammlung.md"),
                      encoding="utf-8").read()
        probe("`contents` steht in der Reihenfolge der Aufnahme",
              pub.index("Texts/eins") < pub.index("Texts/zwei") <
              pub.index("Texts/drei"), pub[:400])
        probe("`# Inhalt` im Body zeigt dieselbe Reihenfolge",
              "1. [[60-Output/Texts/eins|Stück eins]]" in pub, pub[-300:])
        eins = io.open(os.path.join(ziel, AUSGABE, "Texts", "eins.md"),
                       encoding="utf-8").read()
        probe("der Text nennt die Publikation zurück",
              "[[60-Output/Publications/sammlung|Eine Sammlung]]" in eins,
              eins[:300])
        r = lauf(os.path.join(BIN, "hk-publikation"), "sammlung", "--vor",
                 "drei", "--nach", "eins", ziel)
        pub = io.open(os.path.join(ziel, AUSGABE, "Publications", "sammlung.md"),
                      encoding="utf-8").read()
        probe("--vor stellt um", pub.index("Texts/drei") < pub.index("Texts/eins"),
              pub[:400])
        r = lauf(os.path.join(BIN, "hk-publikation"), "sammlung", "--check", ziel)
        probe("--check findet nichts, solange alles stimmt", r.returncode == 0,
              r.stdout[-200:])
        zwei = os.path.join(ziel, AUSGABE, "Texts", "zwei.md")
        _schreib(zwei, io.open(zwei, encoding="utf-8").read().replace(
            'publications:\n  - "[[60-Output/Publications/sammlung|Eine Sammlung]]"\n', ""))
        r = lauf(os.path.join(BIN, "hk-publikation"), "sammlung", "--check", ziel)
        probe("und meldet, wenn ein Rückverweis fehlt",
              r.returncode == 1 and "Texts/zwei" in r.stdout, r.stdout[-300:])
        r = lauf(os.path.join(BIN, "hk-publikation"), "sammlung", "--richten", ziel)
        probe("--richten zieht ihn nach", r.returncode == 0, r.stdout[-200:])
        r = lauf(os.path.join(BIN, "hk-publikation"), "sammlung", "--check", ziel)
        probe("danach stimmt es wieder", r.returncode == 0, r.stdout[-200:])
        probe("und `words` steht am Text",
              "words:" in io.open(zwei, encoding="utf-8").read())
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("die Ablage bleibt konform", r.returncode == 0,
              (r.stdout + r.stderr)[-300:])
        # Leeres `contents` heisst "keine Angabe" und nicht "keine Texte".
        # Ohne diese Sperre schloss `--richten` das eine aus dem anderen und
        # nahm jedem Text seinen Rueckverweis: 114 Texte einer migrierten
        # Ablage am 04.09.2026.
        pubdat = os.path.join(ziel, AUSGABE, "Publications", "sammlung.md")
        vorher_pub = io.open(pubdat, encoding="utf-8").read()
        vorher_txt = io.open(zwei, encoding="utf-8").read()
        _schreib(pubdat, re.sub(r"^contents:\n(?:[ \t]+-.*\n)+", "",
                                vorher_pub, flags=re.M))
        r = lauf(os.path.join(BIN, "hk-publikation"), "sammlung", "--richten", ziel)
        probe("`--richten` verweigert sich bei leerem `contents`",
              r.returncode == 2, (r.stdout + r.stderr)[-300:])
        probe("und laesst die Rueckverweise unangetastet",
              io.open(zwei, encoding="utf-8").read() == vorher_txt,
              io.open(zwei, encoding="utf-8").read()[:200])
        _schreib(pubdat, vorher_pub)

        print("hk-buch und hk-epub: was daraus wird, ist ein Erzeugnis")
        artefakte = tempfile.mkdtemp(prefix="hkb-art-")
        umg_art = dict(os.environ, HKF_ARTEFAKTE=artefakte)
        r = lauf(os.path.join(BIN, "hk-buch"), "sammlung", ziel, env=umg_art)
        probe("das Manuskript entsteht", r.returncode == 0,
              (r.stdout + r.stderr)[-300:])
        manuskript = os.path.join(artefakte, os.path.basename(ziel),
                                  "sammlung.md")
        probe("es liegt außerhalb der Ablage", os.path.isfile(manuskript),
              artefakte)
        probe("und nichts davon in der Ablage",
              not os.path.isfile(os.path.join(ziel, MEDIEN, "Documents",
                                              "sammlung.md")))
        text_m = io.open(manuskript, encoding="utf-8").read()
        probe("der Kopf trägt den Titel für pandoc",
              'title: "Eine Sammlung"' in text_m, text_m[:200])
        probe("die Texte stehen in der Reihenfolge aus `contents`",
              text_m.index("# Stück drei") < text_m.index("# Stück eins"),
              text_m[:400])
        probe("die Überschriften der Texte rücken eine Ebene tiefer",
              "## Zweck" in text_m and "\n# Zweck" not in text_m, text_m[:400])
        probe("kein Frontmatter eines Textes ist mitgekommen",
              text_m.count("---") == 2, text_m[:400])
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("das Erzeugnis stört die Ablage nicht", r.returncode == 0,
              (r.stdout + r.stderr)[-300:])
        r = lauf(os.path.join(BIN, "hk-epub"), "sammlung", ziel, env=umg_art)
        wenn_pandoc = "pandoc` ist nicht da" not in r.stderr
        if wenn_pandoc:
            probe("das EPUB entsteht", r.returncode == 0,
                  (r.stdout + r.stderr)[-300:])
            probe("und liegt neben dem Manuskript",
                  os.path.isfile(os.path.join(artefakte,
                                              os.path.basename(ziel),
                                              "sammlung.epub")))
        else:
            probe("ohne pandoc sagt hk-epub, was fehlt", r.returncode == 2,
                  r.stderr[:200])
        gitignore = io.open(os.path.join(ziel, ".gitignore"),
                            encoding="utf-8").read()
        probe("ein gebautes EPUB gehört nicht ins Repository",
              "*.epub" in gitignore, gitignore)
        shutil.rmtree(artefakte, ignore_errors=True)
        shutil.rmtree(os.path.join(ziel, AUSGABE, "Publications"))
        shutil.rmtree(os.path.join(ziel, AUSGABE, "Texts"))
        shutil.rmtree(os.path.dirname(lieferung_pub), ignore_errors=True)

        print("hkf-erzaehlung: der Kanon einer Reihe")
        lief_erz = os.path.join(tempfile.mkdtemp(prefix="hkb-erz-"),
                                "hkf-erzaehlung")
        shutil.copytree(os.path.join(WURZEL, "bundles", "hkf-erzaehlung"),
                        lief_erz)
        r = lauf(os.path.join(BIN, "hk-lint"), lief_erz)
        probe("die Lieferung ist konform", r.returncode == 0,
              (r.stdout + r.stderr)[-300:])
        erz = os.path.join(tempfile.mkdtemp(prefix="hkb-erzz-"), "ablage")
        r = lauf(os.path.join(BIN, "hk-init"), erz)
        r = lauf(os.path.join(BIN, "hk-import"), lief_erz, erz)
        probe("sie lässt sich in eine frische Ablage importieren",
              r.returncode == 0, (r.stdout + r.stderr)[-300:])
        r = lauf(os.path.join(BIN, "hk-lint"), erz)
        probe("und die Ablage bleibt konform", r.returncode == 0,
              (r.stdout + r.stderr)[-400:])

        print("hk-kontinuitaet: Zeitraum, Listen, Beurteilungen")
        _schreib(os.path.join(erz, WIKI, "Characters", "figur.md"), """---
type: character
name: Eine Figur
created: 2026-01-01
---

# Zweck

Kommt öfter vor.
""")
        _schreib(os.path.join(erz, AUSGABE, "Texts", "abend.md"), """---
type: text
name: Der Abend
story_date: 2026-06-12
created: 2026-01-01
modified: 2026-01-05
---

Der Abend beginnt. [[40-Wiki/Characters/figur|Eine Figur]] kommt zu spät.
""")
        _schreib(os.path.join(erz, AUSGABE, "Texts", "morgen.md"), """---
type: text
name: Der Morgen
story_date: 2026-06-12
story_end: 2026-06-13
created: 2026-01-01
---

Am Morgen danach.
""")
        _schreib(os.path.join(erz, WIKI, "Assessments", "abend.md"), """---
type: assessment
name: Beurteilung Der Abend
assesses: "[[60-Output/Texts/abend|Der Abend]]"
reviewed: 2026-01-01
created: 2026-01-01
---

# Erster Prüfer

Trägt.
""")
        r = lauf(os.path.join(BIN, "hk-kontinuitaet"), erz)
        probe("zwei Texte am selben Tag sind ein Befund",
              "belegen dieselben Tage" in r.stdout, r.stdout[-500:])
        probe("eine Liste, die dem Body nicht folgt, auch",
              "`characters`" in r.stdout and "Characters/figur" in r.stdout,
              r.stdout[-500:])
        probe("und eine Beurteilung, die älter ist als der Text",
              "gelesen am" in r.stdout, r.stdout[-500:])
        probe("mit Befund endet der Lauf mit 1", r.returncode == 1)
        r = lauf(os.path.join(BIN, "hk-kontinuitaet"), erz, "--richten")
        abend = io.open(os.path.join(erz, AUSGABE, "Texts", "abend.md"),
                        encoding="utf-8").read()
        probe("--richten zieht die Liste dem Body nach",
              '- "[[40-Wiki/Characters/figur|Eine Figur]]"' in abend,
              abend[:300])
        r = lauf(os.path.join(BIN, "hk-kontinuitaet"), erz)
        probe("danach bleibt nur, was ein Mensch entscheidet",
              "Abgeleitete Listen (0)" in r.stdout, r.stdout[-400:])
        r = lauf(os.path.join(BIN, "hk-lint"), erz)
        probe("die Ablage bleibt konform", r.returncode == 0,
              (r.stdout + r.stderr)[-400:])
        shutil.rmtree(os.path.dirname(erz), ignore_errors=True)
        shutil.rmtree(os.path.dirname(lief_erz), ignore_errors=True)

        print("hk-publish und hk-kapitel: die Übertragung nach HenniBock")
        for befehl in ("hk-publish", "hk-kapitel"):
            r = lauf(os.path.join(BIN, befehl), "--help")
            probe("%s läuft" % befehl, r.returncode == 0,
                  (r.stdout + r.stderr)[-200:])
        hb = os.path.join(tempfile.mkdtemp(prefix="hkb-hb-"), "ablage")
        lauf(os.path.join(BIN, "hk-init"), hb)
        lief_hb = os.path.join(tempfile.mkdtemp(prefix="hkb-hbl-"),
                               "hkf-publikation")
        shutil.copytree(os.path.join(WURZEL, "bundles", "hkf-publikation"),
                        lief_hb)
        lauf(os.path.join(BIN, "hk-import"), lief_hb, hb)
        r = lauf(os.path.join(BIN, "hk-kapitel"), "queue",
                 env=dict(os.environ, HKB_PATH=hb))
        probe("ohne Warteschlange sagt hk-kapitel das",
              "hennibock_queue" in r.stderr, (r.stdout + r.stderr)[-200:])
        _schreib(os.path.join(hb, WIKI, "Texts", "probe.md"), """---
type: text
name: Eine Probe
summary: Ein Text, der nur prüfen soll, ob der Bau trägt.
hennibock_type: title_story
hennibock_areas:
  - Geschichte
created: 2026-01-01
---

Ein kurzer Text ohne Bild.
""")
        r = lauf(os.path.join(BIN, "hk-publish"), "analyze", "probe",
                 "--ablage", hb)
        probe("eine Notiz ohne Titelbild wird abgewiesen",
              "Titelbild" in (r.stdout + r.stderr),
              (r.stdout + r.stderr)[-200:])
        # Ein winziges PNG, damit der Bau bis zum Bundle kommt.
        import zlib as _zlib, struct as _struct

        def _brocken(art, daten):
            k = art + daten
            return (_struct.pack(">I", len(daten)) + k
                    + _struct.pack(">I", _zlib.crc32(k) & 0xffffffff))

        roh = b"".join(b"\x00" + bytes([90, 110, 140]) * 8 for _ in range(8))
        png = (b"\x89PNG\r\n\x1a\n"
               + _brocken(b"IHDR", _struct.pack(">IIBBBBB", 8, 8, 8, 2, 0, 0, 0))
               + _brocken(b"IDAT", _zlib.compress(roh)) + _brocken(b"IEND", b""))
        bildpfad = os.path.join(hb, MEDIEN, "Images", "probe.png")
        os.makedirs(os.path.dirname(bildpfad), exist_ok=True)
        open(bildpfad, "wb").write(png)
        _schreib(os.path.join(hb, WIKI, "Texts", "probe.md"), """---
type: text
name: Eine Probe
summary: Ein Text, der nur prüfen soll, ob der Bau trägt.
hennibock_type: title_story
hennibock_areas:
  - Geschichte
created: 2026-01-01
---

![[80-Media/Images/probe.png]]

> [!ai-image]
> alt: Ein einfarbiges Feld, das allein der Prüfung dient.
>
> A plain field, used only to verify the build.

Ein kurzer Text.

# Verbindungen

- [[40-Wiki/Texts/probe|Eine Probe]] — steht hier nur als Muster.
""")
        r = lauf(os.path.join(BIN, "hk-publish"), "analyze", "probe",
                 "--ablage", hb)
        if r.returncode == 0:
            daten = json.loads(r.stdout)
            probe("der Titel kommt aus `name`, nicht aus dem Dateinamen",
                  daten.get("title") == "Eine Probe", str(daten.get("title")))
            probe("der Alt-Text kommt aus dem Callout",
                  daten["images"][0].get("alt_source") == "callout",
                  str(daten["images"][0]))
            r = lauf(os.path.join(BIN, "hk-publish"), "build", "probe",
                     "--ablage", hb)
            probe("das Bundle entsteht und wird nicht gesendet",
                  r.returncode == 0 and "Nicht gesendet" in r.stdout,
                  (r.stdout + r.stderr)[-300:])
            probe("die Textprüfung lief davor",
                  "Textpruefung bestanden" in r.stdout, r.stdout[-300:])
        else:
            probe("analyze braucht `sips` für die Bildmaße",
                  "sips" in (r.stdout + r.stderr).lower(),
                  (r.stdout + r.stderr)[-200:])
        shutil.rmtree(os.path.dirname(hb), ignore_errors=True)
        shutil.rmtree(os.path.dirname(lief_hb), ignore_errors=True)

        # HKF Core §3.6 macht den qualifizierten Verweis zur Pflicht. Der
        # Publisher fuehrt seinen Notiz-Index aber ueber Stems und vergleicht
        # gegen `path.stem`. Solange `strip_wikilink` den Pfad stehen liess,
        # fand in einer HKB kein Kapitel mehr seine Publikation, und zwar
        # lautlos: die Menge kam leer zurueck, nicht falsch.
        print("hk-publish: der qualifizierte Verweis (§3.6) fuehrt auf den Stem")
        sys.path.insert(0, os.path.join(WURZEL, "lib"))
        try:
            from hkf.hennibock import kern as _hbkern
        except Exception as e:
            probe("kern ist importierbar", False, str(e))
            _hbkern = None
        if _hbkern is not None:
            probe("ein qualifizierter Verweis wird auf den Stem gekuerzt",
                  _hbkern.strip_wikilink(
                      "[[50 Output/Texts/Kap - Eins|Kap - Eins]]") == "Kap - Eins",
                  _hbkern.strip_wikilink("[[50 Output/Texts/Kap - Eins|Kap - Eins]]"))
            probe("ein kurzer Verweis bleibt, was er ist",
                  _hbkern.strip_wikilink("[[Kap - Eins]]") == "Kap - Eins",
                  _hbkern.strip_wikilink("[[Kap - Eins]]"))
            pubdatei = os.path.join(ziel, WIKI, "Pubs", "pub.md")
            _schreib(pubdatei, """---
type: publication
name: Ein Werk
created: 2026-01-01
---

1. [[50 Output/Texts/Kap - Eins|Kap - Eins]]
2. [[Kap - Zwei]]

## Verbindungen

- [[40-Wiki/Sources/quelle|Eine Quelle]]
""")
            ordnung = _hbkern.publication_order(pathlib.Path(pubdatei))
            probe("das Inhaltsverzeichnis liefert beide Kapitel als Stem",
                  ordnung == ["Kap - Eins", "Kap - Zwei"], repr(ordnung))
            probe("`## Verbindungen` zaehlt nicht als Kapitel",
                  "quelle" not in ordnung, repr(ordnung))
            # Die Rotation und das Publizieren muessen dieselbe Reihenfolge
            # sehen. Sie standen als zwei Fassungen nebeneinander und sind
            # auseinandergelaufen: gemessen ueber zwoelf Publikationen einer
            # migrierten Ablage zwoelf Abweichungen, drei davon mit null
            # erkannten Kapiteln. Jetzt ruft die eine die andere.
            try:
                from hkf.hennibock import kette as _hbkette
            except Exception as e:
                probe("kette ist ohne Ablage importierbar", False, str(e))
                _hbkette = None
            probe("kette ist ohne Ablage importierbar", _hbkette is not None,
                  "Import beim Laden der Ablage gescheitert")
            if _hbkette is not None:
                text = io.open(pubdatei, encoding="utf-8").read()
                probe("Rotation und Publizieren sehen dieselbe Reihenfolge",
                      _hbkette.toc_chapters(text) == ordnung,
                      repr(_hbkette.toc_chapters(text)))
                probe("ein Embed-Ziel verliert seinen Alias (§3.6)",
                      _hbkette.embed_ziel("80-Media/Images/x.jpg|x.jpg")
                      == "80-Media/Images/x.jpg",
                      _hbkette.embed_ziel("80-Media/Images/x.jpg|x.jpg"))
                probe("ein Praefix faellt aus dem Namen, ein anderer Name nicht",
                      _hbkette.strip_praefix("Pub - Eins") == "Eins"
                      and _hbkette.strip_praefix("Der erste Text")
                      == "Der erste Text",
                      _hbkette.strip_praefix("Der erste Text"))
            os.remove(pubdatei)

        print("Die Hooks: der Kanon kommt aus der Sitzung, nicht aus der Ablage")
        p_hooks = os.path.join(WURZEL, "hooks", "hooks.json")
        try:
            hooks = json.load(io.open(p_hooks, encoding="utf-8"))
        except Exception as e:
            hooks = {}
            probe("hooks.json ist lesbar", False, str(e))
        ereignisse = sorted((hooks.get("hooks") or {}))
        probe("hooks.json nennt SessionStart und PostToolUse",
              ereignisse == ["PostToolUse", "SessionStart"], ", ".join(ereignisse))
        befehle = re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/([\w./-]+)",
                             json.dumps(hooks))
        fehlend = sorted(set(b for b in befehle
                             if not os.path.exists(os.path.join(WURZEL, b))))
        probe("jede genannte Datei liegt im Repository", not fehlend,
              ", ".join(fehlend))

        umg = dict(os.environ, HKF_WAHL=os.path.join(ziel, "wahl.json"))
        umg.pop("HKB_PATH", None)
        sitzung = os.path.join(WURZEL, "hooks", "sitzung.py")
        vorher = _abbild(ziel)
        # Ein Subagent laeuft in seinem eigenen Kontext und sieht nicht, was
        # die Sitzung bekommen hat. `hk-kontext` gibt ihm denselben Text.
        r = lauf(os.path.join(BIN, "hk-kontext"), "--stimme", ziel, env=umg)
        probe("hk-kontext gibt die Stimme aus",
              "Voice-Profil" in r.stdout, r.stdout[:200])
        r = lauf(os.path.join(BIN, "hk-kontext"), "--lage", ziel, env=umg)
        probe("und die Lage, ohne den ganzen Kanon",
              ziel in r.stdout and "Zusammenarbeit" not in r.stdout,
              r.stdout[:200])
        r = lauf(os.path.join(WURZEL, "py"), sitzung, input='{"cwd": "%s"}' % ziel,
                 env=umg)
        try:
            aus = json.loads(r.stdout)
            k = aus["hookSpecificOutput"]["additionalContext"]
        except Exception as e:
            aus, k = {}, ""
            probe("der Sitzungshook antwortet in der erwarteten Form", False,
                  str(e) + r.stdout[:200] + r.stderr[:200])
        probe("er nennt die Ablage und woher ihr Pfad kommt",
              ziel in k and "Der Pfad kommt aus" in k, k[:200])
        probe("er spielt den Kanon ein",
              "# Zusammenarbeit" in k and "Wer hier arbeitet" in k, k[:200])
        probe("und die Stimme, die die Wurzeldatei nennt",
              "Voice-Profil" in k or "# Stimme" in k, k[-300:])
        probe("in der Ablage entsteht dabei nichts", _abbild(ziel) == vorher)

        # Was diese eine Ablage fuer sich festlegt, steht als `hint`-Notiz
        # darin (Harness §7) und geht dem Kanon vor.
        _schreib(os.path.join(ziel, WIKI, ablage_hinweise, "kuration.md"), """---
type: hint
name: Kuration
created: 2026-01-01
---

# Zweck

Eine Person bekommt hier erst ab dem zweiten Auftritt ein Blatt.
""")
        r = lauf(os.path.join(WURZEL, "py"), sitzung, input='{"cwd": "%s"}' % ziel,
                 env=umg)
        k = json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]
        probe("die `hint`-Notizen der Ablage kommen dazu",
              "ab dem zweiten Auftritt" in k, k[-300:])
        shutil.rmtree(os.path.join(ziel, WIKI, ablage_hinweise))

        oben = os.path.dirname(ziel)
        r = lauf(os.path.join(WURZEL, "py"), sitzung, input='{"cwd": "%s"}' % oben,
                 env=dict(umg, HKF_WAHL=os.path.join(ziel, "leer.json")))
        k = json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]
        probe("ohne Ablage zählt er auf, statt zu raten",
              "keine Ablage gewählt" in k and "Frag nach" in k, k[:300])
        probe("und spielt den Kanon dabei noch nicht ein",
              "# Zusammenarbeit" not in k, k[:300])
        # In einem fremden Projekt hat der Harness nichts zu sagen. Ein Hook,
        # der dort trotzdem 17 000 Zeichen einspielt, kostet in jeder Sitzung.
        fremd = tempfile.mkdtemp(prefix="hkb-fremd-")
        r = lauf(os.path.join(WURZEL, "py"), sitzung,
                 input='{"cwd": "%s"}' % fremd,
                 env=dict(umg, HKF_WAHL=os.path.join(ziel, "leer.json")))
        probe("wo keine Ablage liegt, schweigt er ganz",
              r.returncode == 0 and not r.stdout.strip(), r.stdout[:200])
        shutil.rmtree(fremd, ignore_errors=True)
        r = lauf(os.path.join(BIN, "hk-ablage"), ziel, env=umg, cwd=ziel)
        probe("nach der Wahl gibt hk-ablage den Kanon aus",
              "# Zusammenarbeit" in r.stdout, r.stdout[:300])

        regeln = os.path.join(WURZEL, "hooks", "schreibregeln.py")
        muster = os.path.join(ziel, WIKI, "Notes", "hook.md")
        kopf = "---\ntype: note\nname: Hook\ncreated: 2026-01-01\n---\n\n# Zweck\n\n"
        ereignis = ('{"cwd": "%s", "tool_input": {"file_path": "%s"}}'
                    % (ziel, muster))
        _schreib(muster, kopf + "Ein sauberer Satz ohne Beanstandung.\n")
        r = lauf(os.path.join(WURZEL, "py"), regeln, input=ereignis, env=umg)
        probe("ein sauberer Text kommt durch", r.returncode == 0,
              r.stdout + r.stderr)
        _schreib(muster, kopf + "Ein Satz mit einem Strichpunkt; das ist ein Fehler.\n")
        r = lauf(os.path.join(WURZEL, "py"), regeln, input=ereignis, env=umg)
        probe("ein Fehler hält den Schreibvorgang an", r.returncode == 2,
              r.stdout + r.stderr)
        probe("und der Befund nennt den Pfad ab der Ablage",
              "40-Wiki/Notes/hook.md" in r.stderr, r.stderr[:200])
        _schreib(muster, kopf + ("Dieser Satz ist mit Bedacht so lang geraten, dass "
                 "er die Grenze von fünfunddreißig Wörtern überschreitet, denn eine "
                 "Warnung soll niemanden aufhalten, sondern nur im Bericht "
                 "auftauchen, wo sie in Ruhe gelesen werden kann.\n"))
        r = lauf(os.path.join(WURZEL, "py"), regeln, input=ereignis, env=umg)
        probe("eine Warnung hält niemanden auf", r.returncode == 0,
              r.stdout + r.stderr)
        r = lauf(os.path.join(WURZEL, "py"), regeln,
                 input='{"cwd": "%s", "tool_input": {"file_path": "%s"}}'
                       % (oben, muster),
                 env=dict(umg, HKF_WAHL=os.path.join(ziel, "leer.json")))
        probe("außerhalb einer Ablage tut er nichts", r.returncode == 0,
              r.stdout + r.stderr)
        os.remove(muster)

        print("Fassung")
        r = lauf(sys.executable, os.path.join(WURZEL, "tools", "grundausstattung.py"))
        probe("Grundausstattung entspricht Anhang A und §3.5.1",
              r.returncode == 0, r.stdout + r.stderr)
        r = lauf(sys.executable, os.path.join(WURZEL, "tools", "spec.py"))
        probe("spec.py meldet keinen Rueckstand",
              r.returncode == 0, r.stdout + r.stderr)
        soll = io.open(os.path.join(WURZEL, ".python-version"),
                       encoding="utf-8").read().strip()
        probe("spec.py sagt, unter welchem Python der Harness steht",
              ("Python %s aus %s" % (soll, hkf_venv())) in r.stdout, r.stdout)

        print("hk-lint auf einer Lieferung")
        r = lauf(os.path.join(BIN, "hk-lint"), bundle)
        probe("erkennt eine Lieferung an hbundle.md",
              "— Lieferung" in r.stdout and r.returncode == 0, r.stdout)
        r = lauf(os.path.join(BIN, "hk-lint"), bundle, "--fix")
        probe("--fix gilt dort nicht", r.returncode == 2, r.stdout + r.stderr)
        _lieferung_kaputt(bundle)
        r = lauf(os.path.join(BIN, "hk-lint"), bundle)
        for was, muster in (
                ("bundles in einer Lieferung", "in einem Bundle steht es nicht"),
                ("zwei Notizen mit derselben Notiz-ID", "dieselbe Notiz-ID"),
                ("eine vorläufige Typdefinition",
                 "keine vorläufige Typdefinition"),
                ("den Importnachweis", "weder Import- noch Entscheidungsnachweis")):
            probe("meldet %s" % was, muster in r.stdout, r.stdout)
        shutil.rmtree(bundle)
        _bundle_bauen(bundle)

        # Gegenprobe: In einer Lieferung ist derselbe Verweis ein Fehler.
        tot = os.path.join(tempfile.mkdtemp(prefix="hkb-tot-"), "lieferung")
        _schreib(os.path.join(tot, "hbundle.md"), """---
hkf: "1.0"
type: bundle
id: probe-tot
title: Probe
description: Prüft, dass ein Verweis ohne Ziel in einer Lieferung ein Fehler bleibt.
version: "2026-01-01"
---

# Typen

| Typ | Verzeichnis | Zweck |
|---|---|---|
""")
        _schreib(os.path.join(tot, "Notes", "probe.md"), """---
type: note
name: Eine Notiz
created: 2026-01-01
modified: 2026-01-01T00:00:00
---

Verweis auf [[Notes/gibt-es-nicht|etwas]].
""")
        r = lauf(os.path.join(BIN, "hk-lint"), tot)
        probe("in einer Lieferung bleibt derselbe Verweis ein Fehler",
              r.returncode == 1 and "zeigt auf keine Datei" in
              r.stdout.split("Hinweise", 1)[0], r.stdout[-300:])
        shutil.rmtree(os.path.dirname(tot), ignore_errors=True)

        print("hk-export")
        aus = os.path.join(os.path.dirname(bundle), "wieder-raus")
        shutil.rmtree(aus, ignore_errors=True)
        r = lauf(os.path.join(BIN, "hk-export"), "probe", aus, ziel)
        probe("schreibt heraus", r.returncode == 0, r.stdout + r.stderr)
        for f in ("hbundle.md", "Typedefs/ding.md", "dinge/eins.md",
                  "dinge/zwei.md", "Media/Images/bilder/bild.png"):
            probe("legt %s an" % f, os.path.exists(os.path.join(aus, f)))
        hb = io.open(os.path.join(aus, "hbundle.md"), encoding="utf-8").read()
        probe("hbundle traegt keine Bereiche (A.1)",
              "base:" not in hb and "config_base" not in hb, hb)
        probe("und eine frische Typtabelle", "| ding | dinge |" in hb, hb)
        probe("ohne Importnachweis", "# Import" not in hb, hb)
        eins_aus = io.open(os.path.join(aus, "dinge", "eins.md"),
                           encoding="utf-8").read()
        probe("streift bundles ab (§4.2)", "bundles:" not in eins_aus, eins_aus)
        probe("behaelt die Zeitangaben", "modified:" in eins_aus, eins_aus)
        probe("behaelt den Verweis innerhalb der Lieferung",
              "# Verbindungen" in eins_aus and "[[dinge/zwei|" in eins_aus, eins_aus)
        probe("verweist auf die Mediendatei ohne Ablagepfad",
              "[[Media/Images/bilder/bild.png|" in eins_aus, eins_aus)

        # Der Rundlauf: wieder einlesen ergibt dieselben Notizen
        zurueck = os.path.join(os.path.dirname(bundle), "kreis")
        shutil.rmtree(zurueck, ignore_errors=True)
        lauf(os.path.join(BIN, "hk-init"), zurueck, "--name", "Probe")
        lauf(os.path.join(BIN, "hk-import"), aus, zurueck)
        # Verglichen wird das gelesene Frontmatter, nicht seine Zeilenfolge:
        # `bundles` wandert ans Ende, weil der Export es abstreift und der
        # Import es wieder anhaengt. Das ist dieselbe Notiz.
        sys.path.insert(0, os.path.join(WURZEL, "lib"))
        from hkf import frontmatter as fm
        fluechtig = ("created", "modified", "modified_by")
        unterschiede = []
        for rel in ("dinge/eins.md", "dinge/zwei.md", "Typedefs/ding.md"):
            wo = KONFIG if rel.startswith("Typedefs/") else WIKI
            a, ab = fm.lesen(os.path.join(ziel, wo, rel))
            b, bb = fm.lesen(os.path.join(zurueck, wo, rel))
            fuer = lambda d: {k: v for k, v in d.items() if k not in fluechtig}
            if fuer(a) != fuer(b) or ab.strip() != bb.strip():
                unterschiede.append(rel)
        probe("Bundle → HKB → Bundle → HKB gibt dieselben Notizen",
              not unterschiede, ", ".join(unterschiede))
        probe("und schickt keinen Kern-Typ mit (§7.1)",
              not os.path.exists(os.path.join(aus, "Typedefs", "typedef.md")))

        print("hk-import: eine zweite Lieferung derselben Notiz")
        # §6.1 Schritt 5 verlangt danach *beide* Bundles. Und was nur in der
        # Wissensbasis steht — `rejected_links`, eine von Hand geschriebene
        # Zeile unter `# Verbindungen` — ueberlebt das Aktualisieren (§5.6).
        p = os.path.join(ziel, WIKI, "dinge", "eins.md")
        vorher_text = io.open(p, encoding="utf-8").read()
        io.open(p, "w", encoding="utf-8").write(
            vorher_text
            .replace("related:\n", "rejected_links:\n  - \"[[Typedefs/ding|Ding]]\"\n"
                     "related:\n  - \"[[Bundles/probe|Probe]]\"\n", 1)
            .rstrip("\n") + "\n- [[Bundles/probe|Probe]] — von Hand eingetragen\n")
        zwei_b = os.path.abspath(os.path.join(ziel, "..", "probe-bundle-2"))
        _bundle_bauen(zwei_b)
        for rel in ("dinge/zwei.md", "bilder/bild.png"):
            os.remove(os.path.join(zwei_b, rel))
        q = os.path.join(zwei_b, "hbundle.md")
        text = io.open(q, encoding="utf-8").read()
        io.open(q, "w", encoding="utf-8").write(
            text.replace("id: probe", "id: probe2")
                .replace("title: Probe", "title: Probe 2"))
        q = os.path.join(zwei_b, "dinge", "eins.md")
        text = io.open(q, encoding="utf-8").read()
        io.open(q, "w", encoding="utf-8").write(
            text.replace("2026-01-01T00:00:00", "2026-06-01T00:00:00").rstrip("\n")
            + "\n\nEin Satz aus der zweiten Lieferung.\n")
        r = lauf(os.path.join(BIN, "hk-import"), zwei_b, ziel)
        eins = io.open(p, encoding="utf-8").read()
        probe("wird als dieselbe Notiz erkannt und aktualisiert",
              "1 aktualisiert" in r.stdout, r.stdout)
        probe("danach stehen beide Bundles darin (§6.1 Schritt 5)",
              "Bundles/probe|Probe]]" in eins and "Bundles/probe2|Probe 2" in eins, eins)
        probe("rejected_links überlebt den Import (§5.6)",
              "rejected_links:" in eins, eins)
        probe("die von Hand geschriebene Zeile bleibt (§5.6)",
              "von Hand eingetragen" in eins, eins)
        probe("die maschinell gesetzte Zeile bleibt auch",
              "dinge/zwei|Das Zweite]] — im Body" in eins, eins)
        probe("der Body kommt aus der Lieferung",
              "Ein Satz aus der zweiten Lieferung." in eins, eins)
        shutil.rmtree(zwei_b, ignore_errors=True)
        io.open(p, "w", encoding="utf-8").write(vorher_text)

        print("hk-import/hk-export: der Quellenbereich")
        # Eine Lieferung kennt keinen Quellenbereich (§4.3): Sie traegt die
        # Notiz unter dem blossen `dir`, die Wissensbasis unter source_base.
        q_b = os.path.abspath(os.path.join(ziel, "..", "probe-quelle"))
        shutil.rmtree(q_b, ignore_errors=True)
        os.makedirs(os.path.join(q_b, "Sources"))
        io.open(os.path.join(q_b, "hbundle.md"), "w", encoding="utf-8").write(
            "---\nhkf: \"1.0\"\ntype: bundle\nid: quelle\ntitle: Quelle\n"
            "description: Ein Buch.\nversion: \"1\"\n---\n\nEine Quelle.\n")
        io.open(os.path.join(q_b, "Sources", "economy.md"), "w",
                encoding="utf-8").write(
            "---\ntype: source\nkind: book\ntitle: On the Economy of Machinery\n"
            "authors:\n  - Charles Babbage\npublished_year: 1832\n"
            "created: 2026-01-01\nmodified: 2026-01-01T00:00:00\n---\n\n"
            "Über Fabrikarbeit.\n")
        r = lauf(os.path.join(BIN, "hk-import"), q_b, ziel)
        probe("die Lieferung wird übernommen", r.returncode == 0, r.stdout + r.stderr)
        probe("die Quellennotiz landet unter source_base (§4.3)",
              os.path.exists(os.path.join(ziel, QUELLEN, "economy.md")))
        probe("und ohne Typverzeichnis darunter (§3.2.2)",
              not os.path.isdir(os.path.join(ziel, QUELLEN, "Sources")))
        probe("`authors` nimmt einen blossen Namen (§2.1)",
              lauf(os.path.join(BIN, "hk-lint"), ziel).returncode == 0
              or "authors" not in lauf(os.path.join(BIN, "hk-lint"), ziel).stdout)
        raus = os.path.abspath(os.path.join(ziel, "..", "probe-quelle-raus"))
        shutil.rmtree(raus, ignore_errors=True)
        r = lauf(os.path.join(BIN, "hk-export"), "quelle", raus, ziel)
        probe("der Export streift den Quellenbereich ab (§4.3)",
              os.path.exists(os.path.join(raus, "Sources", "economy.md"))
              and not os.path.exists(os.path.join(raus, QUELLEN, "economy.md")),
              r.stdout)
        probe("die Lieferung ist für sich sauber",
              lauf(os.path.join(BIN, "hk-lint"), raus).returncode == 0)
        shutil.rmtree(q_b, ignore_errors=True)
        shutil.rmtree(raus, ignore_errors=True)

        print("hk-import: extends")
        # §6.1 Schritt 5: Eine Notiz mit `extends` haengt an, sie ersetzt nicht.
        e_b = os.path.abspath(os.path.join(ziel, "..", "probe-extends"))
        shutil.rmtree(e_b, ignore_errors=True)
        os.makedirs(os.path.join(e_b, "dinge"))
        io.open(os.path.join(e_b, "hbundle.md"), "w", encoding="utf-8").write(
            "---\nhkf: \"1.0\"\ntype: bundle\nid: nachtrag\n"
            "required_bundles:\n  - probe\ntitle: Nachtrag\n"
            "description: Schreibt Das Erste fort.\nversion: \"1\"\n---\n\n"
            "Ein Nachtrag.\n")
        io.open(os.path.join(e_b, "dinge", "nachtrag.md"), "w", encoding="utf-8").write(
            "---\ntype: ding\ntitle: Das Erste\nextends: dinge/eins\n"
            "menge: 7\ncreated: 2026-01-01\nmodified: 2026-06-01T00:00:00\n---\n\n"
            "Ein Satz, der angehängt gehört.\n\n# Verbindungen\n\n"
            "- [[Typedefs/ding|Ding]] — aus dem Nachtrag\n")
        r = lauf(os.path.join(BIN, "hk-lint"), e_b)
        probe("eine Lieferung mit extends ist konform (§7.1)",
              r.returncode == 0, r.stdout)
        r = lauf(os.path.join(BIN, "hk-import"), "--check", e_b, ziel)
        probe("--check meldet den Zustand `ergänzt`", "1 ergänzt" in r.stdout, r.stdout)
        r = lauf(os.path.join(BIN, "hk-import"), e_b, ziel)
        eins = io.open(os.path.join(ziel, WIKI, "dinge", "eins.md"), encoding="utf-8").read()
        probe("keine eigene Notiz entsteht",
              not os.path.exists(os.path.join(ziel, WIKI, "dinge", "nachtrag.md")))
        probe("der Body ist angehängt",
              "Ein Satz, der angehängt gehört." in eins, eins)
        probe("und steht vor `# Verbindungen`",
              eins.index("angehängt gehört") < eins.index("# Verbindungen"), eins)
        probe("`extends` wird abgestreift (§4.2)", "extends:" not in eins, eins)
        probe("die Zeile aus der Ergänzung kommt dazu (§5.6)",
              "aus dem Nachtrag" in eins, eins)
        probe("beide Bundles stehen darin",
              "Bundles/probe|Probe]]" in eins and "Bundles/nachtrag|" in eins, eins)
        probe("ein abweichender Skalar wird vorgelegt, nicht gesetzt",
              "menge" in r.stdout and "menge: 7" not in eins, r.stdout)
        probe("die Ablage bleibt konform",
              lauf(os.path.join(BIN, "hk-lint"), ziel).returncode == 0)
        io.open(os.path.join(ziel, WIKI, "dinge", "drei-extends.md"), "w",
                encoding="utf-8").write(
            "---\ntype: ding\ntitle: X\nextends: dinge/eins\n"
            "created: 2026-01-01\nmodified: 2026-01-01T00:00:00\n---\n\nX.\n")
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("`extends` in einer Wissensbasis ist ein Befund (§7.2)",
              "extends" in r.stdout and r.returncode == 1, r.stdout)
        os.remove(os.path.join(ziel, WIKI, "dinge", "drei-extends.md"))
        shutil.rmtree(e_b, ignore_errors=True)

        print("hk-ingest")
        inbox = os.path.abspath(os.path.join(ziel, "..", "probe-inbox"))
        shutil.rmtree(inbox, ignore_errors=True)
        os.makedirs(inbox)
        umg = dict(os.environ, HKF_INBOX=inbox)
        io.open(os.path.join(inbox, "artikel.md"), "w", encoding="utf-8").write(
            "---\ntitle: Die Maschine von Turin\n"
            "source: https://example.org/turin\nauthor: Jean Rossi\n"
            "published: 2024-03-11\ncreated: 2026-08-30T09:12:00\n"
            "site: Computing History Review\n"
            "description: Ein Überblick.\nseltsam:\n  tief: ja\n---\n\n"
            "Der erfasste Text der Seite.\n")
        io.open(os.path.join(inbox, "buch.md"), "w", encoding="utf-8").write(
            "---\ntype: source\nkind: book\n"
            "title: On the Economy of Machinery\n"
            "url: https://example.org/verlag/economy\n"
            "file: https://nas.example.org/economy.pdf\n"
            "published_year: 1832\n---\n")
        io.open(os.path.join(inbox, "scan.pdf"), "wb").write(b"%PDF-1.4\n%%EOF\n")

        r = lauf(os.path.join(BIN, "hk-ingest"), env=umg)
        probe("ohne Argumente zeigt es die Inbox",
              "3 Stück" in r.stdout and "Es wurde nichts geschrieben" in r.stdout,
              r.stdout)
        probe("und lässt die Werkart der PDF offen",
              "scan.pdf" in r.stdout and "Werkart offen" in r.stdout, r.stdout)
        probe("dabei entsteht keine Lieferung",
              set(os.listdir(inbox)) == {"artikel.md", "buch.md", "scan.pdf"})

        lief = os.path.abspath(os.path.join(ziel, "..", "probe-lieferung"))
        shutil.rmtree(lief, ignore_errors=True)
        r = lauf(os.path.join(BIN, "hk-ingest"), "--alles", "--bundle", lief,
                 "--id", "probe-ingest", env=umg)
        probe("--alles liest die .md-Stücke ein", r.returncode == 0, r.stdout)
        clip = os.path.join(lief, "Sources", "die-maschine-von-turin.md")
        probe("ein Clipping wird zur Quellennotiz", os.path.isfile(clip))
        c = io.open(clip, encoding="utf-8").read() if os.path.isfile(clip) else ""
        probe("das Clipper-Frontmatter ist abgebildet",
              "type: source" in c and "kind: web" in c
              and "url: https://example.org/turin" in c
              and "- Jean Rossi" in c and "published_year: 2024" in c, c)
        roh = os.path.join(lief, "Media", "Clippings",
                           "die-maschine-von-turin.md")
        probe("der erfasste Text wird kopiert, statt in den Body zu wandern",
              os.path.isfile(roh)
              and "Der erfasste Text der Seite."
              in io.open(roh, encoding="utf-8").read()
              and "Der erfasste Text der Seite." not in c, c)
        probe("und `file` zeigt darauf",
              "file: \"[[Media/Clippings/die-maschine-von-turin.md" in c, c)
        probe("`checksum` ist gesetzt", "checksum: sha256:" in c, c)
        hb = io.open(os.path.join(lief, "hbundle.md"), encoding="utf-8").read()
        probe("die Typtabelle nennt keinen Typ der Grundausstattung (§3.8)",
              "# Typen" in hb and "| source |" not in hb, hb)
        probe("Unabbildbares wird verworfen und gemeldet",
              "seltsam" not in c and "seltsam" in r.stdout, r.stdout)
        buch = os.path.join(lief, "Sources", "on-the-economy-of-machinery.md")
        probe("ein .md mit `type: source` wird die Notiz und kopiert nichts",
              os.path.isfile(buch)
              and "file: https://nas.example.org/economy.pdf"
              in io.open(buch, encoding="utf-8").read()
              and not os.path.isfile(os.path.join(
                  lief, "Media", "Clippings",
                  "on-the-economy-of-machinery.md")))
        probe("fehlende Zitationsangaben werden gemeldet, nicht geraten",
              "authors" in r.stdout and "Was noch fehlt" in r.stdout, r.stdout)
        probe("eine nackte Datei wird eingelesen, die Werkart bleibt offen",
              os.path.isfile(os.path.join(lief, "Sources", "scan.md"))
              and "die Werkart (`kind`) steht nicht fest" in r.stdout, r.stdout)
        probe("die eingelesenen Stücke sind verschoben, nicht gelöscht",
              os.path.isfile(os.path.join(inbox, "erledigt", "probe-ingest",
                                          "artikel.md")))
        probe("die Lieferung ist konform",
              lauf(os.path.join(BIN, "hk-lint"), lief).returncode == 0)

        probe("die PDF landet unter Media/Documents/",
              os.path.isfile(os.path.join(lief, "Media", "Documents", "scan.pdf")),
              r.stdout)
        # Dasselbe Stueck noch einmal, diesmal mit genannter Werkart.
        io.open(os.path.join(inbox, "scan2.pdf"), "wb").write(
            b"%PDF-1.4\n% zweiter\n%%EOF\n")
        r = lauf(os.path.join(BIN, "hk-ingest"), "scan2.pdf", "--kind", "book",
                 "--bundle", lief, "--id", "probe-ingest", env=umg)
        s2 = os.path.join(lief, "Sources", "scan2.md")
        probe("mit --kind steht die Werkart in der Notiz",
              os.path.isfile(s2)
              and "kind: book" in io.open(s2, encoding="utf-8").read(),
              r.stdout)
        probe("und die Lücke wird dann nicht mehr gemeldet",
              "die Werkart (`kind`) steht nicht fest" not in r.stdout, r.stdout)

        l2 = os.path.abspath(os.path.join(ziel, "..", "probe-lieferung-2"))
        shutil.rmtree(l2, ignore_errors=True)
        r = lauf(os.path.join(BIN, "hk-ingest"), "--bundle", l2, "--kind", "book",
                 "--title", "On the Economy of Machinery",
                 "--authors", "Charles Babbage", "--published-year", "1832",
                 "--ausfertigung", "https://nas.example.org/economy.pdf",
                 "--id", "haendisch", env=umg)
        probe("händisch mit --ausfertigung kopiert nichts",
              not os.path.isdir(os.path.join(l2, "Media")), r.stdout)
        probe("und schreibt dieselbe Quellennotiz",
              os.path.isfile(os.path.join(l2, "Sources",
                                          "on-the-economy-of-machinery.md")))
        # Ein Codepfad, zwei Eingaenge: der direkte Ingest ist der
        # Bundle-Ingest mit sofortigem Import.
        io.open(os.path.join(inbox, "seite.md"), "w", encoding="utf-8").write(
            "---\ntype: source\nkind: web\ntitle: Eine zitierte Seite\n"
            "url: https://example.org/seite\n---\n\nEine Zusammenfassung.\n")
        r = lauf(os.path.join(BIN, "hk-ingest"), "--alles", "--hkb", ziel, env=umg)
        probe("--hkb importiert die Lieferung gleich mit",
              "1 neu" in r.stdout and "Übernommen" in r.stdout, r.stdout)
        probe("die Quellennotiz landet unter source_base",
              os.path.isfile(os.path.join(ziel, QUELLEN,
                                          "eine-zitierte-seite.md")))
        probe("und die Ablage bleibt konform",
              lauf(os.path.join(BIN, "hk-lint"), ziel).returncode == 0)
        shutil.copy(os.path.join(inbox, "erledigt", "eine-zitierte-seite",
                                 "seite.md"), os.path.join(inbox, "seite.md"))
        r = lauf(os.path.join(BIN, "hk-ingest"), "--alles", "--hkb", ziel, env=umg)
        probe("ein zweiter Lauf erkennt die unveränderte Quelle",
              "nicht geändert" in r.stdout, r.stdout)

        for d in (inbox, lief, l2):
            shutil.rmtree(d, ignore_errors=True)

        print("hk-ingest: was der erste Praxiseinsatz zutage brachte")
        k = os.path.abspath(os.path.join(ziel, "..", "probe-kolon"))
        shutil.rmtree(k, ignore_errors=True)
        r = lauf(os.path.join(BIN, "hk-ingest"), "--bundle", k, "--kind", "web",
                 "--title", "Ein Titel: mit Doppelpunkt",
                 "--url", "https://example.org/x", "--id", "kolon", env=umg)
        probe("ein Titel mit Doppelpunkt bleibt gültiges YAML (B.4)",
              lauf(os.path.join(BIN, "hk-lint"), k).returncode == 0, r.stdout)
        probe("und die Lieferung meldet auch --strict nichts",
              lauf(os.path.join(BIN, "hk-lint"), "--strict", k).returncode == 0,
              lauf(os.path.join(BIN, "hk-lint"), "--strict", k).stdout)

        # Eine Lieferung liefert keinen Typ der Grundausstattung mit (§7.1
        # Punkt 2); `--strict` darf ihre Properties nicht fuer undeklariert
        # halten, nur weil die Typdefinition nicht beiliegt.
        r = lauf(os.path.join(BIN, "hk-lint"), "--strict", k)
        probe("Grundausstattungs-Properties gelten nicht als undeklariert",
              "source: url" not in r.stdout, r.stdout)

        # Unlesbares Frontmatter ist ein Befund, kein Stapelabzug.
        p = os.path.join(k, "hbundle.md")
        text = io.open(p, encoding="utf-8").read()
        io.open(p, "w", encoding="utf-8").write(
            text.replace('title: "Ein Titel: mit Doppelpunkt"',
                         "title: Ein Titel: mit Doppelpunkt"))
        r = lauf(os.path.join(BIN, "hk-lint"), k)
        probe("unlesbares Frontmatter wird gemeldet, nicht geworfen",
              r.returncode == 1 and "kein YAML" in r.stdout
              and "Traceback" not in r.stderr, (r.stdout + r.stderr)[-400:])
        probe("und der Befund nennt Datei und Stelle",
              "hbundle.md" in r.stdout and "Zeile 5" in r.stdout, r.stdout)
        probe("und steht genau einmal da",
              r.stdout.count("kein YAML") == 1, r.stdout)
        shutil.rmtree(k, ignore_errors=True)

        print("hk-lint: der Quellenbereich ist reserviert")
        p = os.path.join(ziel, KONFIG, "Typedefs", "zettel.md")
        io.open(p, "w", encoding="utf-8").write(
            "---\ntype: typedef\ntitle: Zettel\ndescription: Ein Zettel.\n"
            "dir: 50-Sources/Zettel\ncreated: 2026-01-01\n"
            "modified: 2026-01-01T00:00:00\n---\n\n# Properties\n\n"
            "| Property | Typ | Pflicht | Vorgabe | Beschreibung |\n"
            "|---|---|---|---|---|\n| menge | number | nein | — | Wie viele |\n")
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("kein `dir` darf unter source_base liegen (§3.2.2)",
              "`dir` liegt unter `source_base`" in r.stdout, r.stdout)
        os.remove(p)

        print("Clippings sind Dateien, keine Notizen")
        cl = os.path.join(ziel, MEDIEN, "Clippings", "roh.md")
        os.makedirs(os.path.dirname(cl), exist_ok=True)
        # Ohne `type` und mit einer Ueberschrift, die keine Notiz haette —
        # geprueft wird sie nicht, weil sie unter `media_base` liegt (§3.2.1).
        io.open(cl, "w", encoding="utf-8").write(
            "---\nseltsam:\n  tief: ja\n---\n\n# Der Rohtext\n\n"
            "[[Zeigt/Ins/Leere]]\n")
        r = lauf(os.path.join(BIN, "hk-lint"), "--strict", ziel)
        probe("eine `.md` unter media_base wird nicht geprüft (§3.2.1)",
              r.returncode == 0 and "roh.md" not in r.stdout, r.stdout)
        q = os.path.join(ziel, QUELLEN, "mit-clipping.md")
        io.open(q, "w", encoding="utf-8").write(
            "---\ntype: source\nkind: web\ntitle: Mit Clipping\n"
            'file: "[[%s/Clippings/roh.md|roh.md]]"\n'
            "created: 2026-01-01\nmodified: 2026-01-01T00:00:00\n---\n\n"
            "Eine Zusammenfassung.\n" % MEDIEN)
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("`hkf-file` nimmt ein Clipping trotz `.md` (Config §2.1)",
              r.returncode == 0, r.stdout)
        io.open(q, "w", encoding="utf-8").write(
            "---\ntype: source\nkind: web\ntitle: Mit Clipping\n"
            'file: "[[%s/Documents/roh.md|roh.md]]"\n'
            "created: 2026-01-01\nmodified: 2026-01-01T00:00:00\n---\n\n"
            "Eine Zusammenfassung.\n" % MEDIEN)
        os.makedirs(os.path.join(ziel, MEDIEN, "Documents"), exist_ok=True)
        io.open(os.path.join(ziel, MEDIEN, "Documents", "roh.md"), "w",
                encoding="utf-8").write("Kein Clipping.\n")
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("unter Documents/ bleibt `.md` ein Befund",
              "Dateiendung" in r.stdout, r.stdout)
        os.remove(q)
        os.remove(os.path.join(ziel, MEDIEN, "Documents", "roh.md"))
        os.remove(cl)

        print("hk-lint: Unterverzeichnis eines Typverzeichnisses")
        # §3.2 erlaubt sie ausdruecklich, §3.7.1 loest den Typ ueber ein
        # segmentweises Praefix auf — nicht ueber Gleichheit.
        os.makedirs(os.path.join(ziel, WIKI, "dinge", "kiste"), exist_ok=True)
        io.open(os.path.join(ziel, WIKI, "dinge", "kiste", "drei.md"), "w",
                encoding="utf-8").write(
            "---\ntype: ding\ntitle: Das Dritte\ncreated: 2026-01-01\n"
            "modified: 2026-01-01T00:00:00\n---\n\nLiegt eine Ebene tiefer.\n")
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("eine Notiz darin liegt nicht am falschen Ort (§3.2)",
              "gehört nach dinge/" not in r.stdout, r.stdout)
        shutil.rmtree(os.path.join(ziel, WIKI, "dinge", "kiste"))

        print("Verweise in Backticks sind Beispiele, keine Verweise")
        # Ein Clipping bringt die Wikilinks der erfassten Seite mit, eine
        # Typdefinition zeigt welche als Muster her. Beide umzuschreiben
        # verfaelschte sie.
        lief = os.path.abspath(os.path.join(ziel, "..", "code-lieferung"))
        shutil.rmtree(lief, ignore_errors=True)
        os.makedirs(os.path.join(lief, "Persons"))
        io.open(os.path.join(lief, "hbundle.md"), "w", encoding="utf-8").write(
            '---\nhkf: "1.0"\ntype: bundle\nid: code-probe\n'
            "title: Code-Probe\ndescription: Eine Notiz mit einem Beispiel.\n"
            'version: "1.0"\n---\n\nEine Notiz.\n\n# Typen\n\n'
            "| Typ | Verzeichnis | Zweck |\n|---|---|---|\n")
        io.open(os.path.join(lief, "Persons", "grace-hopper.md"), "w",
                encoding="utf-8").write(
            "---\ntype: person\ntitle: Grace Hopper\n"
            "created: 2026-01-01\nmodified: 2026-01-01T00:00:00\n---\n\n"
            "So schreibt man einen Verweis: `[[Persons/grace-hopper]]`.\n\n"
            "```markdown\n[[Persons/grace-hopper]]\n```\n\n"
            "Und so steht er im Text: [[Persons/grace-hopper|sie selbst]].\n")
        r = lauf(os.path.join(BIN, "hk-import"), lief, ziel)
        probe("der Import nimmt die Lieferung an", r.returncode == 0, r.stdout)
        g = io.open(os.path.join(ziel, WIKI, "Persons", "grace-hopper.md"),
                    encoding="utf-8").read()
        probe("ein Verweis im Text bekommt seinen Ablagepfad (§6.1 Schritt 8)",
              "[[%s/Persons/grace-hopper|sie selbst]]" % WIKI in g, g)
        probe("einer in Backticks bleibt, wie er war",
              "`[[Persons/grace-hopper]]`" in g, g)
        probe("und einer im Codeblock ebenso",
              "```markdown\n[[Persons/grace-hopper]]\n```" in g, g)
        shutil.rmtree(lief, ignore_errors=True)

        print("§3.3: ein Absatz ist eine Zeile")
        n = os.path.join(ziel, WIKI, "Persons", "grace-hopper.md")
        vorher = io.open(n, encoding="utf-8").read()
        io.open(n, "w", encoding="utf-8").write(
            vorher.rstrip("\n") + "\n\nEin Absatz, der\numbrochen ist, mit einem\n"
            "[[%s/Persons/grace-hopper|Verweis über\nden Umbruch]].\n" % WIKI)
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("ein umbrochener Absatz ist ein Hinweis",
              "Der Fließtext ist umbrochen" in r.stdout, r.stdout)
        probe("und ein Wikilink über einen Umbruch auch",
              "reicht über einen Umbruch" in r.stdout, r.stdout)
        probe("aber kein Fehler",
              "Struktur (§6.3)            0" in r.stdout, r.stdout)
        r = lauf(os.path.join(BIN, "hk-lint"), "--fix", ziel)
        probe("`--fix` entfaltet ihn", "Fließtext entfaltet" in r.stdout, r.stdout)
        g = io.open(n, encoding="utf-8").read()
        probe("danach steht der Absatz in einer Zeile",
              "Ein Absatz, der umbrochen ist, mit einem" in g, g)
        probe("und der Verweis löst wieder auf",
              "|Verweis über den Umbruch]]" in g, g)
        r = lauf(os.path.join(BIN, "hk-lint"), "--strict", ziel)
        probe("die Ablage ist danach ohne Befund",
              "Hinweise                   0" in r.stdout, r.stdout)
        # Tabellen, Listen und Codebloecke bleiben, wie sie sind.
        io.open(n, "w", encoding="utf-8").write(vorher)
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("die Grundausstattung selbst ist entfaltet",
              "umbrochen" not in r.stdout, r.stdout)

        print("hk-tranchen: der Stand einer großen Quelle steht in der Notiz")
        q = os.path.join(ziel, QUELLEN, "eine-zitierte-seite.md")
        HK_TR = os.path.join(BIN, "hk-tranchen")
        r = lauf(HK_TR, q, "--anlegen", "-",
                 input="## Tranchenvorschlag\n- Teil I (Kap. 1-7)\n"
                       "- Teil II: Kitchener | Khartoum (Kap. 8-12)\n"
                       "\n3. Teil III (Kap. 13-25)\n")
        probe("--anlegen macht aus dem Vorschlag drei Tranchen",
              r.returncode == 0 and "3 Tranchen angelegt" in r.stdout, r.stdout)
        g = io.open(q, encoding="utf-8").read()
        probe("die Liste steht als Abschnitt `# Tranchen` in der Quellennotiz",
              "\n# Tranchen\n" in g, g)
        probe("ein `|` in der Abgrenzung bleibt in der Zelle geschützt",
              "Kitchener \\| Khartoum" in g, g)
        probe("und die Notiz sagt, dass sie geändert wurde (Regel 5)",
              "modified_by: hk-tranchen" in g.split("---")[1], g)
        r = lauf(HK_TR, q, "--naechste")
        probe("--naechste nennt die erste offene Tranche",
              r.returncode == 0 and "Tranche 1 von 3" in r.stdout, r.stdout)
        r = lauf(HK_TR, q, "--abhaken", "1", "--ertrag", "3 neu, 5 fortgeschrieben")
        probe("--abhaken schreibt sie fest",
              r.returncode == 0 and "Noch offen: 2 von 3" in r.stdout, r.stdout)
        r = lauf(HK_TR, q, "--abhaken", "1")
        probe("und ein zweites Mal nur mit --force",
              r.returncode == 2 and "--force" in r.stderr, r.stderr)
        r = lauf(HK_TR, q, "--naechste")
        probe("der Lauf steht danach bei Tranche 2",
              "Tranche 2 von 3" in r.stdout, r.stdout)
        lauf(HK_TR, q, "--abhaken", "2")
        lauf(HK_TR, q, "--abhaken", "3")
        r = lauf(HK_TR, q, "--naechste")
        probe("ist nichts mehr offen, gibt --naechste 1 zurück",
              r.returncode == 1 and "erledigt" in r.stdout, r.stdout)
        probe("der Ertrag der ersten Tranche steht noch da",
              "3 neu, 5 fortgeschrieben"
              in io.open(q, encoding="utf-8").read())
        probe("die Ablage bleibt konform",
              lauf(os.path.join(BIN, "hk-lint"), ziel).returncode == 0)
        r = lauf(HK_TR, os.path.join(ziel, WIKI, "Persons", "grace-hopper.md"))
        probe("eine Notiz, die keine Quelle ist, wird abgewiesen",
              r.returncode == 2 and "nicht `source`" in r.stderr, r.stderr)

        print("hk-types: Typseiten, Bases und die Linkform von `type`")
        r = lauf(os.path.join(BIN, "hk-types"), ziel, "--umstellen")
        probe("das Skript läuft durch", r.returncode == 0, r.stdout)
        seite = os.path.join(ziel, KONFIG, "Types", "Type Person.md")
        probe("es legt eine Typseite an", os.path.isfile(seite), r.stdout)
        probe("sie bindet sich über `definition` (§3.3)",
              "definition:" in io.open(seite, encoding="utf-8").read()
              and "type:" not in io.open(seite, encoding="utf-8").read(),
              io.open(seite, encoding="utf-8").read())
        probe("und eine Base daneben",
              os.path.isfile(os.path.join(ziel, KONFIG, "Bases", "Person.base")),
              r.stdout)
        g = io.open(os.path.join(ziel, WIKI, "Persons", "grace-hopper.md"),
                    encoding="utf-8").read()
        probe("`--umstellen` bringt `type` auf die Linkform",
              "Types/Type Person" in g.split("---")[1], g)
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("die Ablage bleibt konform", "Struktur (§6.3)            0" in r.stdout,
              r.stdout)
        r = lauf(os.path.join(BIN, "hk-types"), ziel)
        probe("ein zweiter Lauf legt nichts an", "nichts anzulegen" in r.stdout,
              r.stdout)
        r = lauf(os.path.join(BIN, "hk-tranchen"),
                 os.path.join(ziel, QUELLEN, "eine-zitierte-seite.md"))
        probe("hk-tranchen erkennt eine Quellennotiz auch in der Linkform",
              r.returncode == 0 and "3 Tranchen" in r.stdout,
              r.stdout + r.stderr)
        # Der Export schreibt die Textform zurueck (§4.2).
        aus = os.path.abspath(os.path.join(ziel, "..", "typ-lieferung"))
        shutil.rmtree(aus, ignore_errors=True)
        r = lauf(os.path.join(BIN, "hk-export"), "code-probe", aus, ziel)
        h = os.path.join(aus, "Persons", "grace-hopper.md")
        probe("der Export schreibt `type` als Text zurück (§4.2)",
              os.path.isfile(h)
              and "type: person" in io.open(h, encoding="utf-8").read(),
              r.stdout)
        shutil.rmtree(aus, ignore_errors=True)

        print("§3.7.3: ein Name, eine Typangabe")
        td = os.path.join(ziel, KONFIG, "Typedefs", "person.md")
        vorher = io.open(td, encoding="utf-8").read()
        io.open(td, "w", encoding="utf-8").write(
            vorher.replace("| homepage | hkf-url |", "| homepage | text |", 1))
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("zwei Typdefinitionen mit verschiedener Angabe sind ein Befund",
              "verschiedene Typangaben" in r.stdout, r.stdout)
        io.open(td, "w", encoding="utf-8").write(vorher)
        r = lauf(os.path.join(BIN, "hk-lint"), ziel)
        probe("und die Grundausstattung selbst ist frei davon",
              "verschiedene Typangaben" not in r.stdout, r.stdout)

        print("Das Inventar: Prosa, Schema und Grundausstattung")
        # Die Pruefung braucht keine Ablage — sie haelt den Harness gegen die
        # Fassung unter spec/, die er umsetzt.
        r = lauf(sys.executable, os.path.join(WURZEL, "tools", "inventar.py"))
        probe("Config, Schema und templates/hkb/ nennen dasselbe",
              r.returncode == 0, r.stdout + r.stderr)
    finally:
        shutil.rmtree(ziel, ignore_errors=True)

    print()
    if fehler:
        print("%d Proben fehlgeschlagen:" % len(fehler))
        for f in fehler:
            print("  -", f)
        return 1
    print("alle Proben ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
