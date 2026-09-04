"""Testfälle für rules.py.

Aufruf: python3 test_rules.py

Der erste Block prüft jede Ablehnungsart einzeln. Ein Validator, der nichts
ablehnt, fällt sonst nicht auf. Der zweite Block prüft die Rangfolge nach K3
bis K6 und die Vereinigung der Datenlisten.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                "..", "..", "lib"))
from hkf.text import rules
from hkf.text.rules import RuleError, RuleSet, load, resolve

BASIS = {
    "writing_policy": {
        "version": 1,
        "checks": {
            "forbidden_characters": {"severity": "error", "characters": ["—", "–"]},
            "forbidden_punctuation": {"severity": "error", "characters": [";"]},
            "umlaut_replacements": {"severity": "error", "stems": ["fuer", "ueber"]},
            "forbidden_phrases": {"severity": "warning", "phrases": ["entscheidend"]},
            "sentence_length": {"severity": "warning", "maximum_words": 25},
            "structural_phrases": {"severity": "warning", "phrases": ["Fazit"]},
        },
    }
}


def satz(policy, origin="test", is_base=False) -> RuleSet:
    return rules._validate(policy, origin, is_base)


class AblehnungTest(unittest.TestCase):
    """Jede Ablehnungsart aus dem Plan, einzeln."""

    def ablehnen(self, policy, teil, is_base=False):
        with self.assertRaises(RuleError) as fall:
            satz(policy, "quelle.md, Fence 1", is_base)
        self.assertIn(teil, str(fall.exception))
        self.assertIn("quelle.md", str(fall.exception),
                      "Fehlermeldung nennt die Herkunft nicht")

    def test_kaputtes_json(self):
        with tempfile.TemporaryDirectory() as ordner:
            pfad = Path(ordner) / "regeln.json"
            pfad.write_text('{"writing_policy": {,}}', encoding="utf-8")
            with self.assertRaises(RuleError) as fall:
                load(pfad, is_base=True)
            self.assertIn("kein gültiges JSON", str(fall.exception))

    def test_unbekannte_pruefung(self):
        self.ablehnen({"checks": {"forbiden_phrases": {"phrases": ["x"]}}},
                      "unbekannte Prüfung")

    def test_unbekannter_schluessel(self):
        self.ablehnen({"schope": ["10 Journal"]}, "unbekannter Schlüssel")

    def test_unbekanntes_feld_in_pruefung(self):
        self.ablehnen({"checks": {"sentence_length": {"max_words": 20}}},
                      "kennt 'max_words' nicht")

    def test_ungueltige_severity(self):
        self.ablehnen({"checks": {"forbidden_phrases": {"severity": "hinweis"}}},
                      "severity 'hinweis'")

    def test_falscher_datentyp_liste(self):
        self.ablehnen({"checks": {"forbidden_phrases": {"phrases": "entscheidend"}}},
                      "muss eine Liste von")

    def test_falscher_datentyp_zahl(self):
        self.ablehnen({"checks": {"sentence_length": {"maximum_words": "25"}}},
                      "positive Ganzzahl")

    def test_null_als_zahl(self):
        self.ablehnen({"checks": {"sentence_length": {"maximum_words": 0}}},
                      "positive Ganzzahl")

    def test_boolean_als_zahl(self):
        # True ist in Python ein int. Ohne eigene Pruefung ginge das durch.
        self.ablehnen({"checks": {"sentence_length": {"maximum_words": True}}},
                      "positive Ganzzahl")

    def test_scope_kein_string(self):
        self.ablehnen({"scope": ["10 Journal", 7]}, "scope muss eine Liste")

    def test_scope_leer(self):
        self.ablehnen({"scope": ["  "]}, "scope muss eine Liste")

    def test_falsche_version(self):
        self.ablehnen({"version": 2}, "version 2")

    def test_doppelter_schluessel(self):
        with self.assertRaises(RuleError) as fall:
            rules._parse('{"a": 1, "a": 2}', "quelle.md, Fence 1")
        self.assertIn("zweimal", str(fall.exception))

    def test_doppelte_pruefung(self):
        roh = ('{"writing_policy": {"checks": '
               '{"forbidden_phrases": {"phrases": ["a"]}, '
               '"forbidden_phrases": {"phrases": ["b"]}}}}')
        with self.assertRaises(RuleError) as fall:
            rules._parse(roh, "quelle.md, Fence 1")
        self.assertIn("forbidden_phrases", str(fall.exception))

    def test_k6_senken_verboten(self):
        self.ablehnen({"scope": ["60 Fiction"],
                       "checks": {"umlaut_replacements": {"severity": "warning"}}},
                      "gilt nach K6 immer als error")

    def test_k6_abschalten_verboten(self):
        self.ablehnen({"checks": {"forbidden_characters": {"severity": "off"}}},
                      "gilt nach K6 immer als error")

    def test_k6_gilt_nicht_fuer_den_basissatz(self):
        # Der Basissatz darf seine eigenen Pruefungen definieren.
        satz({"checks": {"forbidden_characters": {"severity": "error",
                                                  "characters": ["—"]}}},
             is_base=True)

    def test_k6_ergaenzen_bleibt_erlaubt(self):
        satz({"checks": {"forbidden_characters": {"severity": "error",
                                                  "characters": ["​"]}}})

    def test_strichpunkt_darf_gesenkt_werden(self):
        # Der Strichpunkt steht bewusst nicht unter K6, er ist eine Stilregel.
        aufgeloest = resolve(
            [satz(BASIS["writing_policy"], "basis", is_base=True),
             satz({"scope": ["60 Fiction"],
                   "checks": {"forbidden_punctuation": {"severity": "off"}}},
                  "fiktion.md")],
            "60 Fiction/Kapitel.md")
        self.assertNotIn("forbidden_punctuation", aufgeloest)


class RangfolgeTest(unittest.TestCase):
    """K3 bis K6 in der Auflösung."""

    def setUp(self):
        self.basis = satz(BASIS["writing_policy"], "deutsch.json", is_base=True)

    def test_nur_basis(self):
        ergebnis = resolve([self.basis], "40 Wiki/Notes/A.md")
        self.assertEqual(ergebnis["sentence_length"]["maximum_words"], 25)
        self.assertEqual(ergebnis["forbidden_phrases"]["severity"], "warning")

    def test_vaultweiter_satz_schlaegt_basis(self):
        vault = satz({"checks": {"sentence_length": {"maximum_words": 30}}},
                     "Schreibregeln.md")
        ergebnis = resolve([self.basis, vault], "40 Wiki/Notes/A.md")
        self.assertEqual(ergebnis["sentence_length"]["maximum_words"], 30)

    def test_scope_schlaegt_vaultweit(self):
        vault = satz({"checks": {"sentence_length": {"maximum_words": 30}}}, "vault.md")
        journal = satz({"scope": ["10 Journal"],
                        "checks": {"sentence_length": {"maximum_words": 40}}},
                       "journal.md")
        saetze = [self.basis, vault, journal]
        self.assertEqual(
            resolve(saetze, "10 Journal/2026/07/22.md")["sentence_length"]["maximum_words"], 40)
        self.assertEqual(
            resolve(saetze, "40 Wiki/Notes/A.md")["sentence_length"]["maximum_words"], 30)

    def test_laengster_pfad_gewinnt(self):
        kurz = satz({"scope": ["50 Output"],
                     "checks": {"sentence_length": {"maximum_words": 30}}}, "kurz.md")
        lang = satz({"scope": ["50 Output/Publications/Agadir"],
                     "checks": {"sentence_length": {"maximum_words": 45}}}, "lang.md")
        ergebnis = resolve([self.basis, kurz, lang],
                           "50 Output/Publications/Agadir/Kap - 1.md")
        self.assertEqual(ergebnis["sentence_length"]["maximum_words"], 45)

    def test_scope_greift_nicht_bei_teilwort(self):
        # "50 Output" darf nicht auf "50 Outputs" oder "50 Output-Alt" passen.
        satz_output = satz({"scope": ["50 Output"],
                            "checks": {"sentence_length": {"maximum_words": 99}}},
                           "output.md")
        ergebnis = resolve([self.basis, satz_output], "50 Output-Alt/A.md")
        self.assertEqual(ergebnis["sentence_length"]["maximum_words"], 25)

    def test_off_schaltet_ab(self):
        fiktion = satz({"scope": ["60 Fiction"],
                        "checks": {"sentence_length": {"severity": "off"}}},
                       "fiktion.md")
        saetze = [self.basis, fiktion]
        self.assertNotIn("sentence_length", resolve(saetze, "60 Fiction/K1.md"))
        self.assertIn("sentence_length", resolve(saetze, "40 Wiki/A.md"))

    def test_listen_werden_vereinigt(self):
        vault = satz({"checks": {"forbidden_phrases": {"phrases": ["sodann"]}}},
                     "vault.md")
        ergebnis = resolve([self.basis, vault], "40 Wiki/A.md")
        self.assertEqual(ergebnis["forbidden_phrases"]["phrases"],
                         ["entscheidend", "sodann"])

    def test_severity_senken_behaelt_die_daten(self):
        # Die Fiktion senkt auf warning, verliert die Basisliste aber nicht.
        fiktion = satz({"scope": ["60 Fiction"],
                        "checks": {"forbidden_punctuation": {"severity": "warning"}}},
                       "fiktion.md")
        ergebnis = resolve([self.basis, fiktion], "60 Fiction/K1.md")
        self.assertEqual(ergebnis["forbidden_punctuation"]["severity"], "warning")
        self.assertEqual(ergebnis["forbidden_punctuation"]["characters"], [";"])

    def test_k5_gleicher_rang_ist_fehler(self):
        eins = satz({"scope": ["40 Wiki"],
                     "checks": {"sentence_length": {"maximum_words": 30}}}, "eins.md")
        zwei = satz({"scope": ["40 Wiki"],
                     "checks": {"sentence_length": {"maximum_words": 40}}}, "zwei.md")
        with self.assertRaises(RuleError) as fall:
            resolve([self.basis, eins, zwei], "40 Wiki/A.md")
        text = str(fall.exception)
        self.assertIn("eins.md", text)
        self.assertIn("zwei.md", text)
        self.assertIn("K5", text)

    def test_k5_greift_nicht_bei_verschiedenen_pruefungen(self):
        eins = satz({"scope": ["40 Wiki"],
                     "checks": {"sentence_length": {"maximum_words": 30}}}, "eins.md")
        zwei = satz({"scope": ["40 Wiki"],
                     "checks": {"forbidden_phrases": {"phrases": ["x"]}}}, "zwei.md")
        resolve([self.basis, eins, zwei], "40 Wiki/A.md")

    def test_k5_greift_nicht_gegen_den_basissatz(self):
        vault = satz({"checks": {"sentence_length": {"maximum_words": 30}}}, "vault.md")
        resolve([self.basis, vault], "40 Wiki/A.md")

    def test_aktive_pruefung_ohne_daten_ist_fehler(self):
        nackt = satz({"checks": {"forbidden_phrases": {"severity": "error"}}}, "nackt.md")
        with self.assertRaises(RuleError) as fall:
            resolve([nackt], "40 Wiki/A.md")
        self.assertIn("phrases", str(fall.exception))


class FenceTest(unittest.TestCase):

    def test_findet_nur_json_fences(self):
        text = ("Prosa.\n\n```yaml\nnicht: dies\n```\n\n"
                "```json\n{\"writing_policy\": {}}\n```\n\n"
                "```\n{\"auch\": \"nicht\"}\n```\n")
        self.assertEqual(rules.json_fences(text), ['{"writing_policy": {}}'])

    def test_mehrere_fences_in_einer_datei(self):
        with tempfile.TemporaryDirectory() as ordner:
            pfad = Path(ordner) / "Schreibregeln.md"
            eins = json.dumps({"writing_policy": {"checks": {
                "forbidden_phrases": {"phrases": ["a"]}}}})
            zwei = json.dumps({"writing_policy": {"scope": ["10 Journal"], "checks": {
                "sentence_length": {"maximum_words": 40}}}})
            pfad.write_text(f"# Regeln\n\n```json\n{eins}\n```\n\n"
                            f"Mehr Prosa.\n\n```json\n{zwei}\n```\n", encoding="utf-8")
            saetze = load(pfad)
            self.assertEqual(len(saetze), 2)
            self.assertIn("Fence 2", saetze[1].origin)

    def test_fence_ohne_writing_policy_wird_uebergangen(self):
        with tempfile.TemporaryDirectory() as ordner:
            pfad = Path(ordner) / "Doku.md"
            pfad.write_text('```json\n{"beispiel": 1}\n```\n', encoding="utf-8")
            self.assertEqual(load(pfad), [])

    def test_kaputtes_beispiel_blockiert_nicht(self):
        # Ein Doku-Beispiel ohne writing_policy darf den Pruefer nicht anhalten.
        with tempfile.TemporaryDirectory() as ordner:
            pfad = Path(ordner) / "Doku.md"
            pfad.write_text('```json\n{ so nicht, }\n```\n', encoding="utf-8")
            self.assertEqual(load(pfad), [])

    def test_kaputter_regelsatz_blockiert_sehr_wohl(self):
        with tempfile.TemporaryDirectory() as ordner:
            pfad = Path(ordner) / "Schreibregeln.md"
            pfad.write_text('```json\n{"writing_policy": {,}}\n```\n', encoding="utf-8")
            with self.assertRaises(RuleError) as fall:
                load(pfad)
            self.assertIn("kein gültiges JSON", str(fall.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
