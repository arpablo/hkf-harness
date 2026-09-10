---
type: typedef
title: Quelle
description: Ein Werk, auf das sich die Wissensbasis beruft.
created: 2026-09-01
modified: 2026-09-09T11:01:00
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| kind | hkf-source-kind | nein | — | Werkart: Buch, Aufsatz, Video, Webseite und die übrigen |
| authors | hkf-link-or-text-list:person | nein | — | Urheber: als Verweis auf eine Personennotiz oder als Name, wie das Werk ihn nennt |
| published | date | nein | — | Erscheinungsdatum |
| published_year | hkf-year | nein | — | Erscheinungsjahr, wenn kein vollständiges Datum bekannt ist |
| lang | hkf-lang | nein | — | Sprache des Werks |
| url | hkf-url | nein | — | Fundstelle des Werks: wo es veröffentlicht ist |
| file | hkf-file:document,clipping / hkf-url | nein | — | Ausfertigung des Werks: als Datei in der Ablage oder als Adresse, etwa auf einem Dateiserver |
| accessed | date | nein | — | Datum des Abrufs |
| checksum | text | nein | — | `sha256:<hex>` über die Ausfertigung. Sagt beim nächsten Einlesen, ob sich die Quelle geändert hat |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Werks in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Die Zitationsangaben in Prosa, und in ein bis zwei Sätzen, wovon das Werk als Ganzes handelt. |
| `# Kernaussagen` | Was das Werk behauptet: die Frage, die Antwort, die Hauptthesen einzeln. |
| `# Was die Quelle offenlässt` | Wo das Werk selbst spekuliert, sich widerspricht oder eine Frage offen nennt. |
| je Hauptabschnitt eine Überschrift | Der Aufbau des Werks, knapp, mit Verweisen auf die Notizen daraus. Apparat und nicht Ergebnis. |
| `# Tranchen` | Bei einer großen Quelle der Stand des Lesens. Wird von `hk-tranchen` geführt und nicht von Hand. |

**Die Notiz hat bestanden, wenn ein Leser nach fünfzehn Zeilen weiß, was das Werk behauptet.** Nicht, worüber es handelt. Was es behauptet. Alles Weitere in einer Lieferung ist Belegapparat: Die Entitätsnotizen tragen die Fundstellen, an denen sich die Behauptung prüfen lässt. Sie sind nicht das Ergebnis.

**Der erste Satz ist der schwerste und wird trotzdem verlangt.** Wovon ein Werk als Ganzes handelt, in ein bis zwei Sätzen: Wer das nicht sagen kann, hat das Werk nicht verstanden, sondern nur seine Kapitel gelesen. Der Satz entsteht nach der ersten Durchsicht und wird genauer, je weiter die Lektüre kommt.

**`# Kernaussagen` trägt drei Teile, in dieser Reihenfolge.** Erst die Frage des Werks in einem Satz. Dann die Antwort in einem Absatz, mit den Mechanismen, die sie tragen. Dann die Hauptthesen einzeln, je eine Zeile Behauptung und eine Zeile, woran der Autor sie zeigt. Eine These ist ein Satz, den man bestreiten kann. Ein Thema ist keine These.

**Eine Zusammenfassung, die dem Aufbau der Quelle folgt, ist der Fehler und nicht die Form.** Wer ein Buch nach Kapiteln referiert, hat es nicht verstanden. Wer es verstanden hat, sagt zuerst die These und benutzt die Kapitel danach als Beleg. Darum steht der Aufbau des Werks hinter den Kernaussagen und nicht davor, und er bleibt kurz.

**`# Kernaussagen` entsteht zuletzt.** Vor der letzten Tranche wüsste man nur, was die ersten Kapitel behaupten.

**`# Was die Quelle offenlässt` steht nicht in der Quelle.** Es ist die vierte Schicht aus Core §3.3. Der Abschnitt sagt das einleitend, sonst liest er sich wie ein Befund des Werks. Was hier steht, ist beobachtet und nicht behauptet: eine Spekulation, die der Autor selbst kennzeichnet, ein Widerspruch zwischen zwei Kapiteln, eine Frage, die er als offen bezeichnet. Ein eigener Einwand gehört nicht hierher, sondern in eine `note`.

# Konventionen

Eine Quellennotiz beschreibt das Werk, auf das sich die Wissensbasis beruft, und sagt, **was es behauptet**. Der Aufbau des Werks steht danach, je Kapitel oder Hauptabschnitt eine Überschrift, und er ist knapp. Was man daraus **für die eigene Sache schließt**, gehört nicht hierher, sondern in eine `note` oder ein `concept`, das per `sources` auf die Quelle verweist.

**Die Quellennotiz wächst mit dem Werk, eine Zusammenfassung nicht.** Wer die Lektüre verdichtet braucht, legt daneben eine `summary` an: drei Seiten, die Kernaussagen und fünf Vorschläge, was sich daraus schreiben ließe (§3.19). Die Quellennotiz bleibt davon unberührt.

**Die Werkart ist eine Property und kein Typ.** Ein Buch, ein Aufsatz, ein Video und eine Webseite unterscheiden sich in dem, was über sie zu wissen ist, kaum: Wer es gemacht hat, wann es erschien, wo es liegt. Was sie unterscheidet, also Verlag, Auflage und Seitenzahl, ist Zitationsapparat und steht dort, wo er gebraucht wird: im Body oder in einer Property, die eine Wissensbasis selbst anlegt. Als vier Typen kostete die Unterscheidung vier Verzeichnisse und zwanzig Properties, von denen die meisten immer leer blieben. Eine Quelle, deren Art keiner der vier entspricht, hätte gar keinen Ort gehabt. `kind` kennt sieben Werte (§2.2), und eine spätere Fassung darf ergänzen.

**Die Quellennotiz liegt direkt unter `source_base`**, ohne Typverzeichnis (Core §3.2.2). Bei einem einzigen Quelltyp wäre es reine Verdopplung, und die Notiz-ID ist damit der bloße Dateiname.

`url` und `file` bezeichnen Verschiedenes und stehen darum als zwei Properties da, nicht als Alternative (Core §3.7.2): `url` ist, **wo das Werk veröffentlicht ist**, also die Verlagsseite oder die DOI-Adresse, und damit zitierfähig. `file` ist, **wo die eigene Ausfertigung liegt**: als Datei in der Ablage oder als Adresse, etwa auf einem Dateiserver im eigenen Netz. Ein Original muss also nicht in die Ablage kopiert werden, um verzeichnet zu sein. Beide dürfen nebeneinander stehen.

**Ist `file` ein Clipping, steht der erfasste Text dort und nicht im Body.** Ein Clipping ist eine Mediendatei unter `<media_base>/Clippings/` (Core §3.2.1), also Rohmaterial, das niemand pflegt und das darum auch niemand prüft. Die Notiz daneben trägt die Zusammenfassung. Das ist der ganze Unterschied zwischen einer erfassten und einer bloß zitierten Seite, und er verlangt keinen eigenen Typ: Die Datei ist da oder sie ist es nicht.

`checksum` sagt beim nächsten Einlesen, ob sich die Quelle geändert hat. Eine Webseite ändert sich still, und ohne die Prüfsumme fiele das erst auf, wenn die Zusammenfassung schon nicht mehr stimmt.

`published` und `published_year` schließen einander aus, wie `born` und `born_year` bei einer Person (§3.4). Ein Buch von 1989 hat einen Tag, der niemanden interessiert, ein Beitrag vom 28. Juli 2026 hat einen, der zählt. Eine Angabe zu erzwingen, die die Quelle nicht hergibt, brächte nur falsche Genauigkeit. Beide in eine Property zu legen ginge auch nicht, weil Alternativen dieselbe Wertform haben müssen (§3.7.2).
