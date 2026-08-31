# -*- coding: utf-8 -*-
"""HKF Harness — Werkzeuge fuer eine Wissensbasis nach HKF Core.

Dieser Harness setzt genau die Fassung um, die unter spec/ liegt. Welche das
ist, steht hier und nirgends sonst; aendert sich die Spezifikation, aendert
sich diese Nummer mit.
"""
import os, sys

CORE = "1.0"
BASE = "1.0"

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
SPEC = os.path.join(WURZEL, "spec")
TEMPLATES = os.path.join(WURZEL, "templates")
SCHEMA = os.path.join(SPEC, "hkf-core-%s.schema.json" % CORE)

VENV = os.environ.get("HKF_VENV") or os.path.join(
    os.path.expanduser("~"), ".cache", "hkf-harness", "venv")
VENV_PYTHON = os.path.join(VENV, "bin", "python")


def _eigenes_python():
    """Unter dem Python des Harness weiterlaufen, nicht unter irgendeinem.

    Auf einer Maschine liegen leicht zwei Interpreter mit zwei PyYAML-Fassungen
    nebeneinander; welcher zuerst im PATH steht, ist Zufall und darf nicht
    entscheiden, was eine Pruefung findet. Gibt es die venv, wird der Prozess
    unter ihr neu gestartet; gibt es sie nicht, laeuft alles wie bisher weiter
    — `bootstrap-python.sh` baut sie, und `frontmatter` sagt, wenn PyYAML fehlt.

    HKF_PY verhindert die Schleife: Der neu gestartete Prozess sieht sie
    gesetzt und laesst es dabei.
    """
    if os.environ.get("HKF_PY") or not os.path.exists(VENV_PYTHON):
        return
    if os.path.realpath(sys.executable) == os.path.realpath(VENV_PYTHON):
        return
    # Nur wenn wirklich eine Datei laeuft. Bei `python -c` steht in argv[0] das
    # Kennzeichen und nicht der Code; ein Neustart verloere ihn.
    if not sys.argv or not sys.argv[0] or not os.path.isfile(sys.argv[0]):
        return
    os.environ["HKF_PY"] = "1"
    try:
        os.execv(VENV_PYTHON, [VENV_PYTHON] + sys.argv)
    except OSError:                                    # pragma: no cover
        del os.environ["HKF_PY"]


_eigenes_python()
