"""Testfälle für engine.py.

Aufruf: python3 test_engine.py

Geprüft wird je Verfahren, dass ein Verstoss gefunden wird, dass die Position
auf die Originaldatei zeigt und dass die naheliegenden Falschbefunde
ausbleiben. Der letzte Block prüft das Zusammenspiel mit segment.py: was
maskiert ist, darf keinen Befund erzeugen.
"""

from __future__ import annotations

import unittest

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                "..", "..", "lib"))
from hkf.text import rules
from hkf.text.engine import check, has_errors

BASIS = {
    "version": 1,
    "checks": {
        "forbidden_characters": {"severity": "error", "characters": ["—", "–"]},
        "forbidden_punctuation": {"severity": "error", "characters": [";"]},
        "umlaut_replacements": {"severity": "error",
                                "stems": ["fuer", "ueber", "groess", "strasse"]},
        "forbidden_phrases": {"severity": "warning",
                              "phrases": ["entscheidend", "wesentlich",
                                          "nicht nur", "im Grunde genommen"]},
        "forbidden_stems": {"severity": "warning",
                            "stems": ["nachhaltig", "meisterhaft"],
                            "exceptions": ["Nachhaltigkeit"]},
        "sentence_length": {"severity": "warning", "maximum_words": 10},
        "structural_phrases": {"severity": "warning", "phrases": ["Fazit"]},
    },
}


def regeln(pfad="40 Wiki/A.md"):
    satz = rules._validate(BASIS, "deutsch.json", is_base=True)
    return rules.resolve([satz], pfad)


def pruefe(text, pfad="40 Wiki/A.md"):
    return check(text, regeln(pfad), pfad)


class ZeichenTest(unittest.TestCase):

    def test_em_dash_wird_gefunden(self):
        befunde = pruefe("Ein Satz — mit Gedankenstrich.\n")
        self.assertEqual(len(befunde), 1)
        self.assertEqual(befunde[0].check, "forbidden_characters")
        self.assertEqual(befunde[0].severity, "error")
        self.assertIn("Em-Dash", befunde[0].message)
        self.assertTrue(has_errors(befunde))

    def test_strichpunkt_ist_eigene_pruefung(self):
        befunde = pruefe("Erst dies; dann das.\n")
        self.assertEqual([b.check for b in befunde], ["forbidden_punctuation"])

    def test_position_zeigt_auf_das_original(self):
        text = "Zeile eins.\nZeile zwei.\nHier steht — der Strich.\n"
        befund = pruefe(text)[0]
        self.assertEqual(befund.line, 3)
        self.assertEqual(text.split("\n")[2][befund.column - 1], "—")

    def test_bindestrich_ist_erlaubt(self):
        self.assertEqual(pruefe("Ein ASCII-Bindestrich ist in Ordnung.\n"), [])


class UmlautTest(unittest.TestCase):

    def test_ersatzform_wird_gefunden(self):
        befunde = pruefe("Das gilt dafuer auch.\n")
        self.assertEqual(befunde[0].check, "umlaut_replacements")
        self.assertIn("dafuer", befunde[0].message)

    def test_echtes_wort_bleibt_unbehelligt(self):
        # "Feuer" enthaelt kein "fuer", "Steuer" ebenso wenig.
        self.assertEqual(pruefe("Das Feuer und die Steuer bleiben.\n"), [])

    def test_ganzes_wort_wird_gemeldet(self):
        befunde = pruefe("Die Groessenordnung stimmt.\n")
        self.assertIn("Groessenordnung", befunde[0].message)

    def test_echte_umlaute_erzeugen_nichts(self):
        self.assertEqual(pruefe("Für die Größe der Straße über alles.\n"), [])


class PhrasenTest(unittest.TestCase):

    def test_wendung_wird_gefunden(self):
        befunde = pruefe("Das ist entscheidend für den Ausgang.\n")
        namen = [b.check for b in befunde]
        self.assertIn("forbidden_phrases", namen)

    def test_wortgrenze_verhindert_falschbefund(self):
        # "unwesentlich" enthaelt "wesentlich", ist aber ein anderes Wort.
        befunde = [b for b in pruefe("Das ist unwesentlich.\n")
                   if b.check == "forbidden_phrases"]
        self.assertEqual(befunde, [])

    def test_mehrwortphrase_ueber_zeilenumbruch(self):
        befunde = [b for b in pruefe("Es ist nicht\nnur eine Frage.\n")
                   if b.check == "forbidden_phrases"]
        self.assertEqual(len(befunde), 1)

    def test_gross_und_kleinschreibung_egal(self):
        befunde = [b for b in pruefe("Entscheidend ist der Ausgang.\n")
                   if b.check == "forbidden_phrases"]
        self.assertEqual(len(befunde), 1)

    def test_strukturphrase_ist_eigene_pruefung(self):
        befunde = [b for b in pruefe("Ein Fazit steht am Ende.\n")]
        self.assertIn("structural_phrases", [b.check for b in befunde])


class StammTest(unittest.TestCase):
    """forbidden_stems deckt die Luecke, die forbidden_phrases offen laesst.

    Eine Phrase trifft nur die exakte Wortform. Im Deutschen ist die flektierte
    der Normalfall: "entscheidende" kam im Vault 236 mal vor und "entscheidend"
    118 mal, gefunden wurde nur das zweite.
    """

    def test_flektierte_form_wird_gefunden(self):
        befunde = [b for b in pruefe("Eine nachhaltige Politik zahlt sich aus.\n")
                   if b.check == "forbidden_stems"]
        self.assertEqual(len(befunde), 1)
        self.assertIn("nachhaltige", befunde[0].message)

    def test_grundform_wird_nur_einmal_gemeldet(self):
        """Sonst meldeten Phrase und Stamm dieselbe Stelle zweimal."""
        befunde = [b for b in pruefe("Das Ergebnis war meisterhaft.\n")
                   if b.severity == "warning"]
        self.assertEqual(len(befunde), 1)

    def test_ausnahme_bleibt_unberuehrt(self):
        befunde = [b for b in pruefe("Nachhaltigkeit ist ein Sachbegriff.\n")
                   if b.check == "forbidden_stems"]
        self.assertEqual(befunde, [])

    def test_praefix_bleibt_unberuehrt(self):
        """Ein Stamm am Wortanfang ist der Verstaerker, mitten im Wort nicht.

        "kriegsentscheidend" ist ein Fachbegriff, "unwesentlich" ein eigenes
        Wort. Beide traegt umlaut_replacements bewusst anders, dort steckt die
        Ersatzform auch mitten im Wort.
        """
        befunde = [b for b in pruefe("Die unnachhaltige Variante war teuer.\n")
                   if b.check == "forbidden_stems"]
        self.assertEqual(befunde, [])


class SatzlaengeTest(unittest.TestCase):

    def lang(self, text):
        return [b for b in pruefe(text) if b.check == "sentence_length"]

    def test_langer_satz_wird_gemeldet(self):
        text = "Eins zwei drei vier fünf sechs sieben acht neun zehn elf zwölf.\n"
        befunde = self.lang(text)
        self.assertEqual(len(befunde), 1)
        self.assertIn("12 Wörtern", befunde[0].message)

    def test_kurzer_satz_bleibt_still(self):
        self.assertEqual(self.lang("Eins zwei drei.\n"), [])

    def test_zwei_saetze_werden_getrennt_gezaehlt(self):
        text = ("Eins zwei drei vier fünf sechs. "
                "Sieben acht neun zehn elf zwölf dreizehn.\n")
        self.assertEqual(len(self.lang(text)), 0)

    def test_abkuerzung_beendet_keinen_satz(self):
        # Ohne Schutz waere das zwei kurze Saetze statt eines langen.
        text = "Das gilt bzw. wirkt eins zwei drei vier fünf sechs sieben acht.\n"
        self.assertEqual(len(self.lang(text)), 1)

    def test_ordnungszahl_beendet_keinen_satz(self):
        text = "Am 1. Juli eins zwei drei vier fünf sechs sieben acht neun.\n"
        self.assertEqual(len(self.lang(text)), 1)

    def test_jahreszahl_beendet_sehr_wohl(self):
        text = ("Das geschah 1911. Danach kam eins zwei drei vier fünf.\n")
        self.assertEqual(self.lang(text), [])

    def test_ueberschrift_ist_kein_satz(self):
        text = ("## Eins zwei drei vier fünf sechs sieben acht neun zehn elf zwölf\n\n"
                "Kurzer Satz.\n")
        self.assertEqual(self.lang(text), [])

    def test_tabellenzeile_ist_kein_satz(self):
        text = "| Eins zwei drei vier fünf sechs sieben acht neun zehn elf | Ja |\n"
        self.assertEqual(self.lang(text), [])

    def test_listeneintraege_verschmelzen_nicht(self):
        # Am echten Bestand gefunden: ohne Grenze wurden aufeinanderfolgende
        # Eintraege ohne Schlusspunkt zu einem Satz mit 1202 Woertern.
        text = ("- [[Eins]] - eins zwei drei vier fünf sechs sieben acht\n"
                "- [[Zwei]] - eins zwei drei vier fünf sechs sieben acht\n"
                "- [[Drei]] - eins zwei drei vier fünf sechs sieben acht\n")
        self.assertEqual(self.lang(text), [])

    def test_langer_listeneintrag_wird_gemeldet(self):
        text = "- eins zwei drei vier fünf sechs sieben acht neun zehn elf zwölf.\n"
        self.assertEqual(len(self.lang(text)), 1)

    def test_nummerierte_liste_zaehlt_ebenso(self):
        text = ("1. eins zwei drei vier fünf sechs sieben acht\n"
                "2. eins zwei drei vier fünf sechs sieben acht\n")
        self.assertEqual(self.lang(text), [])

    def test_fortsetzungszeile_bleibt_beim_eintrag(self):
        text = ("- eins zwei drei vier fünf sechs\n"
                "  sieben acht neun zehn elf zwölf.\n")
        self.assertEqual(len(self.lang(text)), 1)


class ZusammenspielTest(unittest.TestCase):
    """Was segment.py maskiert, darf keinen Befund erzeugen."""

    def test_code_fence_erzeugt_keinen_befund(self):
        self.assertEqual(pruefe("```python\nwert = 1; fuer = 2\n```\n"), [])

    def test_ai_callout_erzeugt_keinen_befund(self):
        self.assertEqual(
            pruefe("> [!ai-image]\n> A scene; wide and fuer bright.\n"), [])

    def test_note_callout_erzeugt_sehr_wohl_einen_befund(self):
        befunde = pruefe("> [!note]\n> Das gilt dafuer auch.\n")
        self.assertEqual(befunde[0].check, "umlaut_replacements")
        self.assertEqual(befunde[0].line, 2)

    def test_inline_code_erzeugt_keinen_befund(self):
        self.assertEqual(pruefe("Der Wert `fuer` ist gesetzt.\n"), [])

    def test_linkziel_erzeugt_keinen_befund(self):
        self.assertEqual(
            pruefe("Siehe [die Quelle](https://example.org/fuer-alle) dort.\n"), [])

    def test_tag_erzeugt_keinen_befund(self):
        self.assertEqual(pruefe("---\ntags:\n  - fuer-alle\n---\n\nText.\n"), [])


class SortierungTest(unittest.TestCase):

    def test_befunde_kommen_nach_zeile_sortiert(self):
        text = "Dritter dafuer.\n\nErster — Strich.\n"
        befunde = pruefe(text)
        self.assertEqual([b.line for b in befunde], [1, 3])

    def test_format_nennt_alles_noetige(self):
        zeile = pruefe("Ein Satz — hier.\n")[0].format()
        for teil in ("40 Wiki/A.md:1:", "[error]", "forbidden_characters",
                     "deutsch.json"):
            self.assertIn(teil, zeile)


class AusnahmeTest(unittest.TestCase):
    """Am echten Bestand gefunden: Staemme treffen quer ueber Kompositionsfugen."""

    def regeln_mit(self, ausnahmen):
        policy = {"version": 1, "checks": {"umlaut_replacements": {
            "severity": "error", "stems": ["reissen", "fuer", "foerder", "aender"],
            "exceptions": ausnahmen}}}
        satz = rules._validate(policy, "deutsch.json", is_base=True)
        return rules.resolve([satz], "40 Wiki/A.md")

    def test_kompositionsfuge_ohne_ausnahme_ist_falschbefund(self):
        befunde = check("Die Preissenkungen kamen spät.\n", self.regeln_mit([]), "a.md")
        self.assertEqual(len(befunde), 1, "Der Falschbefund muss ohne Ausnahme auftreten")

    def test_ausnahme_unterdrueckt_den_falschbefund(self):
        regeln = self.regeln_mit(["Preissenkungen", "Fuerteventura"])
        self.assertEqual(check("Die Preissenkungen kamen spät.\n", regeln, "a.md"), [])
        self.assertEqual(check("Ferien auf Fuerteventura.\n", regeln, "a.md"), [])

    def test_ausnahme_ist_gross_klein_egal(self):
        regeln = self.regeln_mit(["preissenkungen"])
        self.assertEqual(check("Preissenkungen.\n", regeln, "a.md"), [])

    def test_ausnahme_deckt_nicht_den_echten_verstoss(self):
        regeln = self.regeln_mit(["Preissenkungen"])
        befunde = check("Sie wollten das Papier zerreissen.\n", regeln, "a.md")
        self.assertEqual(len(befunde), 1)
        self.assertIn("zerreissen", befunde[0].message)

    def test_zwei_staemme_ein_wort_ergeben_einen_befund(self):
        # "foerder" und "aender" treffen beide "Foerderlaender".
        befunde = check("Die Foerderlaender trafen sich.\n", self.regeln_mit([]), "a.md")
        self.assertEqual(len(befunde), 1)
        self.assertIn("Foerderlaender", befunde[0].message)


if __name__ == "__main__":
    unittest.main(verbosity=2)
