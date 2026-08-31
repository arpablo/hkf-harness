#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rauchprobe: hk-init legt eine saubere Ablage an, hk-lint findet, was kaputt ist.

    python3 test/smoke.py

Kein Testrahmen, keine Fremdpakete. Der Lauf endet mit 0, wenn alle Proben
zutreffen, sonst mit 1 und einer Zeile pro Fehlschlag.
"""
import io, os, shutil, subprocess, sys, tempfile

WURZEL = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
BIN = os.path.join(WURZEL, "bin")
fehler = []


def lauf(*args, **kw):
    return subprocess.run(list(args), capture_output=True, text=True, **kw)


def probe(name, bedingung, hinweis=""):
    print("  %-52s %s" % (name, "ok" if bedingung else "FEHLT"))
    if not bedingung:
        fehler.append(name + ((" — " + hinweis) if hinweis else ""))


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

        print("Fassung")
        r = lauf(sys.executable, os.path.join(WURZEL, "tools", "spec.py"))
        probe("spec.py meldet keinen Rueckstand",
              r.returncode == 0, r.stdout + r.stderr)
        soll = io.open(os.path.join(WURZEL, ".python-version"),
                       encoding="utf-8").read().strip()
        probe("spec.py sagt, unter welchem Python der Harness steht",
              ("Python %s aus %s" % (soll, hkf_venv())) in r.stdout, r.stdout)

        print("hk-export")
        r = lauf(os.path.join(BIN, "hk-export"))
        probe("hk-export sagt, dass es fehlt",
              r.returncode == 3 and "Noch nicht umgesetzt" in r.stderr)
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
