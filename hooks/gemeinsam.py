# -*- coding: utf-8 -*-
"""Was beide Hooks brauchen: das Ereignis lesen und die Ablage finden.

Ein Hook bekommt sein Ereignis als JSON auf der Standardeingabe. Darin steht
unter anderem das Arbeitsverzeichnis der Sitzung, und das ist der Ausgangspunkt
fuer die Ablagesuche. Der Prozess des Hooks selbst laeuft irgendwo, sein `cwd`
sagt nichts.
"""
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, os.path.join(WURZEL, "lib"))
from hkf import ablage   # noqa: E402

# Wo ein Dateipfad unmittelbar steht. Mehr braucht es fuer Claude Code nicht:
# `Write` und `Edit` uebergeben `file_path`.
PFADFELDER = {"file_path", "path", "file"}


def ereignis():
    try:
        daten = json.load(sys.stdin)
    except Exception:
        return {}
    return daten if isinstance(daten, dict) else {}


def arbeitsverzeichnis(e):
    for roh in (e.get("cwd"), os.environ.get("CLAUDE_PROJECT_DIR"), os.getcwd()):
        if roh:
            return os.path.abspath(os.path.expanduser(roh))
    return os.getcwd()


def geaendert(e, wurzel):
    """Die geaenderten Dateien unterhalb der Ablage, absolut und ohne Doppelte."""
    roh = []

    def sammeln(wert, schluessel=""):
        if isinstance(wert, dict):
            for k, v in wert.items():
                sammeln(v, k)
        elif isinstance(wert, list):
            for v in wert:
                sammeln(v, schluessel)
        elif isinstance(wert, str) and schluessel in PFADFELDER:
            roh.append(wert)

    sammeln(e.get("tool_input") or e.get("input") or {})
    aus = []
    for wert in roh:
        pfad = wert if os.path.isabs(wert) else os.path.join(wurzel, wert)
        pfad = os.path.realpath(pfad)
        if not pfad.startswith(os.path.realpath(wurzel) + os.sep):
            continue
        if pfad not in aus:
            aus.append(pfad)
    return aus


def blockieren(meldung):
    """Claude Code haelt bei Rueckgabewert 2 an und zeigt die Standardfehlerausgabe."""
    sys.stderr.write(meldung + "\n")
    return 2


def kontext(text, meldung=None):
    """Die Ausgabeform, mit der ein SessionStart-Hook Kontext beisteuert."""
    aus = {"hookSpecificOutput": {"hookEventName": "SessionStart",
                                  "additionalContext": text}}
    if meldung:
        aus["systemMessage"] = meldung
    sys.stdout.write(json.dumps(aus, ensure_ascii=False))
    return 0
