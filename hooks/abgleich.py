#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Meldet zu Sitzungsbeginn, wenn Ablage und Remote auseinandergelaufen sind.

Eine Ablage wird auf mehreren Rechnern bearbeitet, und oft laeuft daneben eine
zweite Sitzung. Der `post-commit`-Hook schiebt jeden Commit still zum Remote,
aber die Gegenrichtung sieht niemand: Wer zu arbeiten beginnt, ohne vorher zu
ziehen, merkt es erst beim Push, und dann liegen die Aenderungen bereits
nebeneinander.

**Der Hook schweigt, solange alles zusammenpasst.** Ein Hinweis, der bei jedem
Sitzungsstart erscheint, wird nach dem dritten Mal nicht mehr gelesen.

**Er blockiert nie.** Ein Remote kann auf einem Netzlaufwerk liegen, erreichbar
ueber ein VPN, und ein haengender Fetch darf keine Sitzung aufhalten. Ein
Fetch, der nicht laufen kann, ist kein Befund.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import gemeinsam   # noqa: E402
from hkf import ablage   # noqa: E402

# Ueber ein VPN ist ein Fetch spuerbar langsamer als im Heimnetz. Nach acht
# Sekunden ist die Antwort auf die Frage "hat sich drueben etwas getan" weniger
# wert als eine Sitzung, die sofort beginnt.
FETCH_ZEIT = 8
GIT_ZEIT = 5


def git(wurzel, *args, **kw):
    try:
        e = subprocess.run(("git", "-C", wurzel) + args, capture_output=True,
                           text=True, timeout=kw.get("timeout", GIT_ZEIT))
    except (OSError, subprocess.SubprocessError):
        return None
    return e.stdout.strip() if e.returncode == 0 else None


def main():
    e = gemeinsam.ereignis()
    try:
        wurzel, _woher = ablage.aufloesen(wo=gemeinsam.arbeitsverzeichnis(e))
    except Exception:
        return 0
    if not ablage.art_von(wurzel) or not os.path.exists(
            os.path.join(wurzel, ".git")):
        return 0

    zweig = git(wurzel, "rev-parse", "--abbrev-ref", "HEAD")
    if not zweig or zweig == "HEAD":
        return 0
    # Der Remote-Name steht nicht fest. Ein Klon nennt ihn `origin`, ein
    # gewachsenes Repo kann ihn anders nennen.
    remote = git(wurzel, "config", "branch.%s.remote" % zweig) or "origin"
    if git(wurzel, "remote", "get-url", remote) is None:
        return 0

    git(wurzel, "fetch", "--quiet", remote, zweig, timeout=FETCH_ZEIT)
    zaehlung = git(wurzel, "rev-list", "--left-right", "--count",
                   "%s...%s/%s" % (zweig, remote, zweig))
    if not zaehlung:
        return 0
    try:
        voraus, zurueck = (int(t) for t in zaehlung.split())
    except ValueError:
        return 0
    if not voraus and not zurueck:
        return 0

    zeilen = []
    if zurueck:
        zeilen.append("%d Commit(s) liegen auf %s/%s und fehlen hier. Vor der "
                      "Arbeit ziehen: git pull --rebase %s %s"
                      % (zurueck, remote, zweig, remote, zweig))
    if voraus:
        zeilen.append("%d Commit(s) sind hier und noch nicht auf %s/%s."
                      % (voraus, remote, zweig))
    if voraus and zurueck:
        zeilen.append("Beide Seiten sind weitergelaufen. Erst ziehen, dann "
                      "prüfen, ob dieselbe Notiz zweimal geändert wurde.")

    return gemeinsam.kontext("# Stand gegenüber dem Remote\n\n"
                             + "\n".join("- " + z for z in zeilen),
                             "HKF: Ablage und Remote laufen auseinander")


if __name__ == "__main__":
    sys.exit(main())
