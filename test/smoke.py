#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rauchprobe: hk-init legt eine saubere Ablage an, hk-lint findet, was kaputt ist.

    python3 test/smoke.py

Kein Testrahmen, keine Fremdpakete. Der Lauf endet mit 0, wenn alle Proben
zutreffen, sonst mit 1 und einer Zeile pro Fehlschlag.
"""
import io, os, re, shutil, subprocess, sys, tempfile

WURZEL = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# Die vier Bereiche (Core §3.1)
WIKI, QUELLEN, MEDIEN, KONFIG = "40-Wiki", "50-Sources", "80-Media", "90-System"
BIN = os.path.join(WURZEL, "bin")
fehler = []


def lauf(*args, **kw):
    return subprocess.run(list(args), capture_output=True, text=True, **kw)


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
        probe("34 Notizen", "34 Notizen" in r.stdout, r.stdout.strip())
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
              "Typtabelle nennt" in r.stdout and "hkf-phone` fehlt" in r.stdout
              and "lässt sich nicht auflösen" in r.stdout, r.stdout)
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
              "# Siehe auch" in eins and "dinge/zwei|Das Zweite" in eins, eins)
        probe("führt ihn auch in related", "related:" in eins, eins)
        zwei = io.open(os.path.join(ziel, WIKI, "dinge", "zwei.md"), encoding="utf-8").read()
        probe("und keinen Gegeneintrag (§5.6)", "# Siehe auch" not in zwei, zwei)
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
              "# Siehe auch" in eins_aus and "[[dinge/zwei|" in eins_aus, eins_aus)
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
        # Zeile unter `# Siehe auch` — ueberlebt das Aktualisieren (§5.6).
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
            "Ein Satz, der angehängt gehört.\n\n# Siehe auch\n\n"
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
        probe("und steht vor `# Siehe auch`",
              eins.index("angehängt gehört") < eins.index("# Siehe auch"), eins)
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
