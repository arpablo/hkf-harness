#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rauchprobe: hk-init legt eine saubere Ablage an, hk-lint findet, was kaputt ist.

    python3 test/smoke.py

Kein Testrahmen, keine Fremdpakete. Der Lauf endet mit 0, wenn alle Proben
zutreffen, sonst mit 1 und einer Zeile pro Fehlschlag.
"""
import io, os, re, shutil, subprocess, sys, tempfile

WURZEL = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
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
        t.replace("---\n\n", "bundles:\n  - \"[[bundles/probe|Probe]]\"\n---\n\n", 1))
    os.makedirs(os.path.join(bundle, "woanders"), exist_ok=True)
    io.open(os.path.join(bundle, "woanders", "zwei.md"), "w",
            encoding="utf-8").write(
        "---\ntype: ding\ntitle: Noch ein Zweites\n"
        "modified: 2026-01-01T00:00:00\n---\n\nDoppelter Dateiname.\n")
    io.open(os.path.join(bundle, "typedefs", "kiste.md"), "w",
            encoding="utf-8").write(
        "---\ntype: typedef\nprovisional: true\n"
        "description: Vorläufig, gehört nicht in eine Lieferung.\n"
        "modified: 2026-01-01T00:00:00\n---\n")


def _tabellenfehler(ziel):
    """Eine Typdefinition, die gegen §3.7.1 verstoesst, und Notizen dazu."""
    os.makedirs(os.path.join(ziel, "dinge"), exist_ok=True)
    io.open(os.path.join(ziel, "typedefs", "ding.md"), "w", encoding="utf-8").write(
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
    io.open(os.path.join(ziel, "dinge", "eins.md"), "w", encoding="utf-8").write(
        "---\ntype: ding\ntitle: Das Erste\ncreated: 2026-01-01\n"
        "modified: 2026-01-01T00:00:00\nnetz: kein-url\n"
        "kiste: \"[[dinge/zwei|Das Zweite]]\"\n"
        "bild: \"[[dinge/zwei|Das Zweite]]\"\n---\n\nEins.\n")
    io.open(os.path.join(ziel, "dinge", "zwei.md"), "w", encoding="utf-8").write(
        "---\ntype: ding\ntitle: Das Zweite\nmenge: 2\ncreated: 2026-01-01\n"
        "modified: 2026-01-01T00:00:00\n---\n\nZwei.\n")


def _kaputt(ziel):
    """Baut in eine frische Ablage ein, was --fix wieder gerade zieht."""
    import re as _re
    p = os.path.join(ziel, "hkb.md")
    t = io.open(p, encoding="utf-8").read()
    io.open(p, "w", encoding="utf-8").write(
        _re.sub(r"^\| bundle \|.*\n", "", t, flags=_re.M))
    os.remove(os.path.join(ziel, "proptypes", "hkf-phone.md"))
    os.makedirs(os.path.join(ziel, "dinge"), exist_ok=True)
    io.open(os.path.join(ziel, "typedefs", "ding.md"), "w", encoding="utf-8").write(
        "---\ntype: typedef\ntitle: Ding\ndescription: Ein Ding.\ndir: dinge\n"
        "created: 2026-01-01\nmodified: 2026-01-01T00:00:00\n---\n")
    io.open(os.path.join(ziel, "dinge", "zwei.md"), "w", encoding="utf-8").write(
        "---\ntype: ding\ntitle: Das Zweite\ncreated: 2026-01-01\n"
        "modified: 2026-01-01T00:00:00\n---\n\nEin Ding.\n")
    io.open(os.path.join(ziel, "dinge", "eins.md"), "w", encoding="utf-8").write(
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
    for sub in ("typedefs", "dinge", "bilder"):
        os.makedirs(os.path.join(pfad, sub))
    def schreib(rel, text):
        io.open(os.path.join(pfad, rel), "w", encoding="utf-8").write(text)
    schreib("hbundle.md",
            "---\nhkf: \"1.0\"\ntype: bundle\nid: probe\ntitle: Probe\n"
            "description: Zwei Dinge und ein Bild.\nversion: \"1\"\n---\n\n"
            "Eine Lieferung für die Rauchprobe.\n")
    schreib("typedefs/ding.md",
            "---\ntype: typedef\ntitle: Ding\ndescription: Ein Ding.\ndir: dinge\n"
            "modified: 2026-01-01T00:00:00\n---\n\n# Properties\n\n"
            "| Property | Typ | Pflicht | Beschreibung |\n|---|---|---|---|\n"
            "| menge | number | nein | Wie viele |\n")
    schreib("dinge/eins.md",
            "---\ntype: ding\ntitle: Das Erste\nmodified: 2026-01-01T00:00:00\n---\n\n"
            "Es steht neben Das Zweite, ohne es zu verlinken.\n\n"
            "![[bilder/bild.png|bild.png]]\n")
    schreib("dinge/zwei.md",
            "---\ntype: ding\ntitle: Das Zweite\nmodified: 2026-01-01T00:00:00\n---\n\n"
            "Ein Ding für sich.\n")
    io.open(os.path.join(pfad, "bilder", "bild.png"), "wb").write(b"\x89PNG\r\n")


def main():
    ziel = tempfile.mkdtemp(prefix="hkb-probe-")
    shutil.rmtree(ziel)
    try:
        print("hk-init")
        r = lauf(os.path.join(BIN, "hk-init"), ziel, "--name", "Probe")
        probe("legt an", r.returncode == 0, r.stderr.strip())
        probe("16 Notizen", "16 Notizen" in r.stdout, r.stdout.strip())
        probe("Wurzeldatei traegt den Namen",
              "name: Probe" in io.open(os.path.join(ziel, "hkb.md"), encoding="utf-8").read())
        probe("Git-Repository mit einem Commit",
              lauf("git", "-C", ziel, "log", "--oneline").stdout.count("\n") == 1)
        probe("AGENTS.md liegt da", os.path.exists(os.path.join(ziel, "AGENTS.md")))
        probe("AGENTS.md ist nicht versioniert",
              "AGENTS.md" not in lauf("git", "-C", ziel, "ls-files").stdout)
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
        io.open(os.path.join(ziel, "typedefs", "kaputt.md"), "w", encoding="utf-8").write(
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
              os.path.exists(os.path.join(ziel, "proptypes", "hkf-phone.md")))
        probe("erzeugt die Typtabelle neu",
              "| ding | dinge |" in io.open(os.path.join(ziel, "hkb.md"),
                                            encoding="utf-8").read())
        eins = io.open(os.path.join(ziel, "dinge", "eins.md"), encoding="utf-8").read()
        probe("qualifiziert den verzeichnislosen Verweis",
              "[[dinge/zwei|Das Zweite]]" in eins and "[[zwei]]" not in eins, eins)
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
                 "verschiedene Wertformen")):
            probe("meldet %s" % was, muster in r.stdout, r.stdout)
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
        probe("--check schreibt nichts", not os.path.exists(os.path.join(ziel, "dinge")))

        r = lauf(os.path.join(BIN, "hk-import"), bundle, ziel)
        probe("übernimmt die Lieferung", r.returncode == 0, r.stdout + r.stderr)
        for f in ("typedefs/ding.md", "dinge/eins.md", "dinge/zwei.md",
                  "bundles/probe.md", "media/images/bilder/bild.png"):
            probe("legt %s an" % f, os.path.exists(os.path.join(ziel, f)))
        eins = io.open(os.path.join(ziel, "dinge", "eins.md"), encoding="utf-8").read()
        probe("trägt die Zugehörigkeit ein", "bundles/probe|Probe" in eins, eins)
        probe("schreibt den Verweis, den der Body hergibt",
              "# Siehe auch" in eins and "dinge/zwei|Das Zweite" in eins, eins)
        probe("führt ihn auch in related", "related:" in eins, eins)
        zwei = io.open(os.path.join(ziel, "dinge", "zwei.md"), encoding="utf-8").read()
        probe("und keinen Gegeneintrag (§5.6)", "# Siehe auch" not in zwei, zwei)
        probe("schreibt den Wikilink auf den Pfad der HKB um",
              "[[media/images/bilder/bild.png|" in eins, eins)
        probe("Typtabelle in hkb.md ergänzt",
              "| ding | dinge |" in io.open(os.path.join(ziel, "hkb.md"),
                                            encoding="utf-8").read())

        vorher = _abbild(ziel)
        lauf(os.path.join(BIN, "hk-import"), bundle, ziel)
        probe("ein zweiter Lauf ändert nichts", _abbild(ziel) == vorher)

        # Bedeutungspruefung: derselbe Name, andere Beschreibung
        p = os.path.join(ziel, "typedefs", "ding.md")
        t = io.open(p, encoding="utf-8").read()
        io.open(p, "w", encoding="utf-8").write(
            t.replace("description: Ein Ding.", "description: Ein Datensatz."))
        vorher = _abbild(ziel)
        r = lauf(os.path.join(BIN, "hk-import"), bundle, ziel)
        probe("weist bei offener Bedeutungsprüfung ab",
              r.returncode == 1 and "abgewiesen" in r.stdout, r.stdout)
        probe("und schreibt dabei nichts", _abbild(ziel) == vorher)
        io.open(p, "w", encoding="utf-8").write(t)          # wieder herstellen

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
        for f in ("hbundle.md", "typedefs/ding.md", "dinge/eins.md",
                  "dinge/zwei.md", "media/images/bilder/bild.png"):
            probe("legt %s an" % f, os.path.exists(os.path.join(aus, f)))
        hb = io.open(os.path.join(aus, "hbundle.md"), encoding="utf-8").read()
        probe("hbundle traegt base und media_base",
              'base: ""' in hb and "media_base: media" in hb, hb)
        probe("und eine frische Typtabelle", "| ding | dinge |" in hb, hb)
        probe("ohne Importnachweis", "# Import" not in hb, hb)
        eins_aus = io.open(os.path.join(aus, "dinge", "eins.md"),
                           encoding="utf-8").read()
        probe("streift bundles ab (§4.2)", "bundles:" not in eins_aus, eins_aus)
        probe("behaelt die Zeitangaben", "modified:" in eins_aus, eins_aus)
        probe("behaelt den Verweis innerhalb der Lieferung",
              "# Siehe auch" in eins_aus and "[[dinge/zwei|" in eins_aus, eins_aus)
        probe("verweist auf die Mediendatei ohne Ablagepfad",
              "[[media/images/bilder/bild.png|" in eins_aus, eins_aus)

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
        for rel in ("dinge/eins.md", "dinge/zwei.md", "typedefs/ding.md"):
            a, ab = fm.lesen(os.path.join(ziel, rel))
            b, bb = fm.lesen(os.path.join(zurueck, rel))
            fuer = lambda d: {k: v for k, v in d.items() if k not in fluechtig}
            if fuer(a) != fuer(b) or ab.strip() != bb.strip():
                unterschiede.append(rel)
        probe("Bundle → HKB → Bundle → HKB gibt dieselben Notizen",
              not unterschiede, ", ".join(unterschiede))
        probe("und schickt keinen Kern-Typ mit (§7.1)",
              not os.path.exists(os.path.join(aus, "typedefs", "typedef.md")))
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
