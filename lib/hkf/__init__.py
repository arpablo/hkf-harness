# -*- coding: utf-8 -*-
"""HKF Harness — Werkzeuge fuer eine Wissensbasis nach HKF Core.

Dieser Harness setzt genau die Fassung um, die unter spec/ liegt. Welche das
ist, steht hier und nirgends sonst; aendert sich die Spezifikation, aendert
sich diese Nummer mit.
"""
import os

CORE = "1.0"
BASE = "1.0"

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
SPEC = os.path.join(WURZEL, "spec")
TEMPLATES = os.path.join(WURZEL, "templates")
SCHEMA = os.path.join(SPEC, "hkf-core-%s.schema.json" % CORE)
