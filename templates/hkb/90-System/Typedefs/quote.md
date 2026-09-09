---
type: typedef
title: Zitat
description: Ein wörtlich übernommener Satz und seine Herkunft.
created: 2026-09-09
modified: 2026-09-09T11:09:12
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| quotes | hkf-link:source | nein | — | Die Quelle, aus der das Zitat stammt |
| locator | text | nein | — | Fundstelle im Werk: Seite, Kapitel oder Zeitmarke, etwa `S. 112` oder `00:14:20` |
| said_by | hkf-link-or-text:person | nein | — | Wer den Satz gesagt oder geschrieben hat: als Verweis auf eine Personennotiz oder als Name |
| said_at | date | nein | — | Tag, an dem der Satz fiel, wenn er nicht mit dem Erscheinen der Quelle zusammenfällt |
| lang | hkf-lang | nein | — | Sprache des Zitats, wie es im Body steht |
| about | hkf-link-list | nein | — | Worauf sich das Zitat bezieht |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Ein Abschnitt, für den keine Quelle etwas hergibt, bleibt weg und wird nicht leer hingeschrieben. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Das Zitat selbst, als Blockzitat und wörtlich. |
| `## Original` | Der Wortlaut in der Ausgangssprache, wenn oben eine Übersetzung steht. |
| `## Zusammenhang` | Wovon im Werk die Rede ist und an welcher Stelle der Satz fällt. |
| `## Zuschreibung` | Worauf die Zuschreibung beruht, wenn keine Quelle sie belegt. |

# Konventionen

**Nicht jedes Zitat wird eine Notiz.** Ein Zitat im Fließtext bleibt dort, wo es etwas belegt, mitsamt seiner Fundstelle. Eine eigene Notiz bekommt ein Satz, der an mehreren Stellen gebraucht wird oder selbst zum Gegenstand geworden ist. Ohne diese Schranke zerfällt der Bestand in Schnipsel, die niemand mehr einordnet.

**Der Wortlaut ist unantastbar.** Wörtlich heißt wörtlich: keine Glättung, keine stille Kürzung, keine angepasste Zeitform. Eine Auslassung steht als `[…]`, eine Einfügung in eckigen Klammern, eine Hervorhebung stammt aus dem Original oder wird als eigene gekennzeichnet. Wer den Satz ändern will, zitiert ihn nicht mehr, sondern gibt ihn wieder, und das gehört in die Notiz zur Sache.

**Das Zitat steht im Body und nicht in einer Property.** Ein Satz mit Anführungszeichen, Doppelpunkten und Zeilenumbrüchen wäre in YAML nur maskiert unterzubringen und in keiner Ansicht mehr lesbar. Als Blockzitat im Body bleibt er, was er ist, und lässt sich einbetten: Eine Notiz, die den Wortlaut braucht, schreibt `![[Quotes/…]]` und nicht die Abschrift. So steht der Satz einmal in der Ablage und nicht dreimal in drei Fassungen.

**Ohne `quotes` bleibt es eine Zuschreibung.** Ein geflügeltes Wort ohne Werk darf eine Notiz bekommen, aber es steht schwächer da als ein belegter Satz, und die Notiz sagt das selbst: `said_by` trägt den Namen, `## Zuschreibung` sagt, wer den Satz wem seit wann zuschreibt und was dagegen spricht. Wo eine Quelle vorliegt, gehört sie in `quotes`, und `locator` SOLLTE die Stelle nennen. Ein Zitat, das sich nicht nachschlagen lässt, ist ein Gerücht über einen Satz.

**`said_by` ist nicht der Urheber der Quelle.** In einem Interview spricht der Befragte, verfasst hat das Werk der Fragende, und in einem Geschichtswerk fällt der Satz bei einem Dritten. Fehlt die Angabe, gilt der Urheber der Quelle aus `authors` (§3.8).

`said_at` trägt den Tag der Äußerung und nicht den der Veröffentlichung: Das Werk erschien 1998, gesagt wurde der Satz 1919. Fallen beide zusammen, bleibt die Property weg, denn `published` an der Quelle sagt es dann schon.

**Eine Übersetzung ohne Original ist kein Zitat.** Steht oben eine Übersetzung, gehört der Ausgangswortlaut unter `## Original`, und `lang` nennt die Sprache dessen, was oben steht. Wer nur die Übersetzung führt, führt eine Wiedergabe, und die gehört in die Notiz zur Sache.

**Ein Zitat belegt ein Werk und ersetzt es nicht.** Es ist so lang wie nötig und so kurz wie möglich. Eine Wissensbasis, die ganze Kapitel als Zitate führt, ist eine Textsammlung mit fremdem Recht daran, und dagegen hilft keine Property.
