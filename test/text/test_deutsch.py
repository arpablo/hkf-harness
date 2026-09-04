"""Prüft den deutschen Basisregelsatz rules/deutsch.json.

Aufruf: python3 test_deutsch.py

Der Regelsatz stammt aus core/deutsche-sprache.md und
core/allgemeine-schreibregeln.md. Beide Quellen decken sich, seit die Regeldrift
aufgelöst ist. Der frühere Abgleich gegen die abgelösten Referenz-YAMLs ist
entfallen, weil es sie nicht mehr gibt.

Zwei Eigenheiten des Regelsatzes sind nicht offensichtlich und deshalb hier
festgehalten:

- Der Strichpunkt liegt unter ``forbidden_punctuation`` und nicht unter
  ``forbidden_characters``. Er ist eine Stilregel und keine formale, und nach K6
  wäre er in der anderen Prüfung für einen Vault unantastbar.
- Die Satzlängengrenze steht auf 35 Wörtern. Bei 25 waren in einem Vault mit
  2579 Dateien 14658 Sätze auffällig, der Median lag bei 30 und das
  90-Prozent-Quantil bei 39. Eine Warnung, die jeden zweiten Satz trifft, ist
  Rauschen. 35 richtet die Regel auf das oberste Viertel.

Nur Standardbibliothek.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                "..", "..", "lib"))
from hkf.text import rules

HIER = Path(__file__).resolve().parent
REGELN = HIER.parents[1] / "rules" / "deutsch.json"



class LadbarkeitTest(unittest.TestCase):
    """Der Regelsatz muss durch die eigene Validierung kommen."""

    def test_laedt_als_basissatz(self):
        saetze = rules.load(REGELN, is_base=True)
        self.assertEqual(len(saetze), 1)
        self.assertTrue(saetze[0].is_base)

    def test_jede_pruefung_des_schemas_ist_aktiv(self):
        """Gegen das Schema geprueft, nicht gegen eine Zahl im Testnamen.

        Der Test hiess bis zur Aufnahme von forbidden_stems "alle sechs
        Pruefungen", da waren es schon sieben.
        """
        aufgeloest = rules.resolve(rules.load(REGELN, is_base=True), "40 Wiki/A.md")
        self.assertEqual(set(aufgeloest), set(rules.CHECK_SCHEMA))

    def test_ausnahmen_kommen_durch(self):
        aufgeloest = rules.resolve(rules.load(REGELN, is_base=True), "40 Wiki/A.md")
        self.assertIn("Fuerteventura", aufgeloest["umlaut_replacements"]["exceptions"])

    def test_korrigierte_phrasen_greifen_am_echten_text(self):
        from hkf.text.engine import check
        aufgeloest = rules.resolve(rules.load(REGELN, is_base=True), "40 Wiki/A.md")
        for satz, erwartet in (("Darüber hinaus gilt das auch.\n", "forbidden_phrases"),
                               ("Abschließend bleibt der Befund.\n", "structural_phrases")):
            namen = [b.check for b in check(satz, aufgeloest, "a.md")]
            self.assertIn(erwartet, namen, satz.strip())

    def test_revolutionaer_erzeugt_keinen_befund_mehr(self):
        from hkf.text.engine import check
        aufgeloest = rules.resolve(rules.load(REGELN, is_base=True), "40 Wiki/A.md")
        befunde = check("Mossadegh war kein Revolutionär im üblichen Sinne.\n",
                        aufgeloest, "a.md")
        self.assertEqual([b for b in befunde if b.check == "forbidden_phrases"], [])

    def test_keine_phrase_in_der_ersatzform(self):
        """Eine Regel in der Form, die sie selbst verbietet, kann nie greifen.

        Genau das war bei "darueber hinaus" und "abschliessend" der Fall. Beide
        standen im Kanon und trafen null Stellen, weil sie die Ersatzform
        enthielten, die eine andere Prüfung als Fehler führt.
        """
        satz = json.loads(REGELN.read_text(encoding="utf-8"))["writing_policy"]["checks"]
        stems = satz["umlaut_replacements"]["stems"]
        for name in ("forbidden_phrases", "structural_phrases"):
            for phrase in satz[name]["phrases"]:
                for stamm in stems:
                    self.assertNotIn(stamm, phrase.lower(),
                                     f"{name}: {phrase!r} enthält die Ersatzform {stamm!r}")

    def test_grenze_greift_erst_ab_sechsunddreissig(self):
        from hkf.text.engine import check
        aufgeloest = rules.resolve(rules.load(REGELN, is_base=True), "40 Wiki/A.md")
        for anzahl, erwartet in ((35, 0), (36, 1)):
            satz = " ".join(["Wort"] * anzahl) + ".\n"
            lang = [b for b in check(satz, aufgeloest, "a.md")
                    if b.check == "sentence_length"]
            self.assertEqual(len(lang), erwartet, f"{anzahl} Wörter")


if __name__ == "__main__":
    unittest.main(verbosity=2)
