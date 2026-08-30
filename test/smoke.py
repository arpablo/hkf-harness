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

        print("hk-import / hk-export")
        for name in ("hk-import", "hk-export"):
            r = lauf(os.path.join(BIN, name))
            probe("%s sagt, dass es fehlt" % name,
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
