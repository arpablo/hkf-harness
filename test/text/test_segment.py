"""Testfälle für segment.py, die Fallliste aus dem Plan.

Aufruf: python3 test_segment.py

Jeder Fall prüft zweierlei: dass geprüfter Text im maskierten Ergebnis erhalten
bleibt und dass ignorierter Text verschwunden ist. Zusätzlich prüft jeder Fall,
dass die Maskierung die Zeilenstruktur unangetastet lässt. Ohne diese Zusage
zeigen Zeilennummern eines Befunds nicht mehr auf die Originaldatei.
"""

from __future__ import annotations

import unittest

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                "..", "..", "lib"))
from hkf.text.segment import mask


class SegmentTest(unittest.TestCase):

    def pruefe(self, text, sichtbar=(), verborgen=()):
        """Maskiert und prüft Sichtbarkeit, Länge und Zeilenstruktur."""
        ergebnis = mask(text)
        self.assertEqual(len(ergebnis), len(text), "Länge verändert")
        self.assertEqual(ergebnis.count("\n"), text.count("\n"),
                         "Zeilenzahl verändert")
        for zeile_alt, zeile_neu in zip(text.split("\n"), ergebnis.split("\n")):
            self.assertEqual(len(zeile_alt), len(zeile_neu),
                             "Zeilenlänge verändert")
        for wort in sichtbar:
            self.assertIn(wort, ergebnis, f"fehlt, wurde faelschlich maskiert: {wort}")
        for wort in verborgen:
            self.assertNotIn(wort, ergebnis, f"steht noch da, nicht maskiert: {wort}")
        return ergebnis

    # Callouts

    def test_note_callout_wird_geprueft(self):
        self.pruefe(
            "> [!note]\n> Eine Größe für über tausend Häuser.\n",
            sichtbar=["Größe für über tausend Häuser"],
            verborgen=["[!note]"],
        )

    def test_hennibock_intro_wird_geprueft(self):
        self.pruefe(
            "> [!hennibock-intro]\n> Dieses Buch erzählt die Krise.\n",
            sichtbar=["Dieses Buch erzählt die Krise"],
        )

    def test_ai_image_callout_wird_ignoriert(self):
        self.pruefe(
            "Vorher.\n> [!ai-image]\n> A wide editorial scene, warm light.\n\nNachher.\n",
            sichtbar=["Vorher.", "Nachher."],
            verborgen=["editorial scene", "warm light"],
        )

    def test_ai_image_prompt_wird_ignoriert(self):
        self.pruefe(
            "> [!ai-image-prompt]\n> project: Hennibock\n> A quiet harbour at dawn.\n",
            verborgen=["quiet harbour", "Hennibock"],
        )

    def test_fence_in_note_callout(self):
        # Der Callout wird geprüft, der Fence darin nicht.
        self.pruefe(
            "> [!note]\n> Erklärung dazu.\n> ```python\n> geheim = 1\n> ```\n> Schluss.\n",
            sichtbar=["Erklärung dazu.", "Schluss."],
            verborgen=["geheim", "python"],
        )

    def test_fence_in_ai_callout(self):
        self.pruefe(
            "> [!ai-image]\n> A prompt.\n> ```text\n> more prompt\n> ```\n",
            verborgen=["A prompt", "more prompt", "text"],
        )

    def test_ai_callout_in_note_callout(self):
        ergebnis = self.pruefe(
            "> [!note]\n> Äußerer Text.\n> > [!ai-image]\n> > Inner english prompt.\n> Wieder außen.\n",
            sichtbar=["Äußerer Text.", "Wieder außen."],
            verborgen=["Inner english prompt"],
        )
        self.assertIn("Wieder außen", ergebnis)

    def test_callout_endet_ohne_leerzeile(self):
        self.pruefe(
            "> [!ai-image]\n> English prompt here.\nDeutscher Fließtext folgt.\n",
            sichtbar=["Deutscher Fließtext folgt."],
            verborgen=["English prompt here"],
        )

    # Fences

    def test_tilde_fence_und_vier_backticks(self):
        self.pruefe(
            "Davor.\n~~~\ntilde geheim\n~~~\n\n````\nvier geheim\n````\n\nDanach.\n",
            sichtbar=["Davor.", "Danach."],
            verborgen=["tilde geheim", "vier geheim"],
        )

    def test_offener_fence_bis_dateiende(self):
        self.pruefe(
            "Davor.\n```\nnie geschlossen\nauch das noch\n",
            sichtbar=["Davor."],
            verborgen=["nie geschlossen", "auch das noch"],
        )

    def test_drei_backticks_inline_starten_keinen_fence(self):
        self.pruefe(
            "Man schreibt ```code``` mitten im Satz und über allem steht Größe.\n"
            "Die nächste Zeile bleibt sichtbar.\n",
            sichtbar=["mitten im Satz", "Die nächste Zeile bleibt sichtbar."],
            verborgen=["```code```"],
        )

    def test_inline_code_einfach_und_mehrfach(self):
        self.pruefe(
            "Der Wert `fuer` und ``ein ` Sonderfall`` bleiben außen vor.\n",
            sichtbar=["Der Wert", "bleiben außen vor."],
            verborgen=["`fuer`", "Sonderfall"],
        )

    # Frontmatter

    def test_frontmatter_prosa_wird_geprueft(self):
        self.pruefe(
            "---\nsummary: \"Eine Erklärung über den Panthersprung\"\n---\n\nText.\n",
            sichtbar=["Eine Erklärung über den Panthersprung"],
        )

    def test_frontmatter_bezeichner_werden_ignoriert(self):
        self.pruefe(
            "---\n"
            "hennibock_ref: 3f2a1c9d-0000-4444-8888-abcdefabcdef\n"
            "slug: der-panthersprung-nach-agadir\n"
            "cover: 80 Media/Images/Chapter/Agadir/hafen.jpg\n"
            "summary: \"Prosa bleibt stehen\"\n"
            "---\n",
            sichtbar=["Prosa bleibt stehen"],
            verborgen=["3f2a1c9d", "der-panthersprung-nach-agadir", "hafen.jpg"],
        )

    def test_frontmatter_tags_sind_bezeichner(self):
        # Gefunden am echten Bestand: blosse Listeneintraege ohne Schluessel
        # blieben ungemaskt, obwohl Tags nach Konvention kebab-case-Slugs sind.
        self.pruefe(
            "---\n"
            "tags:\n"
            "  - deutsches-kaiserreich\n"
            "  - imperialismus\n"
            "aliases:\n"
            "  - Der Panthersprung nach Agadir\n"
            "---\n",
            sichtbar=["Der Panthersprung nach Agadir"],
            verborgen=["deutsches-kaiserreich", "imperialismus"],
        )

    def test_datei_ohne_frontmatter(self):
        self.pruefe("Nur Text, keine Frontmatter.\n",
                    sichtbar=["Nur Text, keine Frontmatter."])

    # Links

    def test_linkziele_werden_ignoriert(self):
        self.pruefe(
            "Siehe [die Erklärung](https://example.org/fuer-alle) im Netz.\n",
            sichtbar=["die Erklärung", "im Netz."],
            verborgen=["example.org", "fuer-alle"],
        )

    def test_wikilink_notizname_bleibt_kebab_verschwindet(self):
        self.pruefe(
            "Vergleiche [[Schreibregeln]] und [[skill-konvention]] sowie "
            "![[80 Media/Images/haus.jpg]].\n",
            sichtbar=["Schreibregeln"],
            verborgen=["skill-konvention", "80 Media/Images/haus.jpg"],
        )

    def test_nackte_adresse_wird_ignoriert(self):
        # rhythm_lint schuetzte nackte URLs bisher selbst. Das gehoert in die
        # gemeinsame Segmentierung, sonst gilt es nur fuer den Rhythmus.
        self.pruefe(
            "Siehe https://example.org/fuer-alle und schreib an post@beispiel.de.\n",
            sichtbar=["Siehe", "und schreib an"],
            verborgen=["example.org", "fuer-alle", "post@beispiel.de"],
        )

    def test_adresse_in_klammern_bleibt_erkannt(self):
        self.pruefe("Die Quelle (https://example.org/ueber) ist alt.\n",
                    sichtbar=["Die Quelle", "ist alt."],
                    verborgen=["example.org"])

    # Randfaelle

    def test_leerer_text(self):
        self.assertEqual(mask(""), "")

    def test_zeilennummern_bleiben_stehen(self):
        text = ("---\nslug: a-b\n---\n\n"
                "> [!ai-image]\n> English.\n\n"
                "Der Befund steht in Zeile 8.\n")
        ergebnis = mask(text)
        zeilen = ergebnis.split("\n")
        self.assertEqual(zeilen[7], "Der Befund steht in Zeile 8.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
