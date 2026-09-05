---
type: typedef
base: output
title: Text
description: Ein Stück Prosa, das für sich steht.
created: 2026-09-04
modified: 2026-09-04T00:00:00
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| subtitle | text | nein | — | Untertitel, wenn der Titel allein zu wenig sagt |
| authors | hkf-link-or-text-list | nein | — | Wer ihn geschrieben hat, als Notiz oder als Name |
| publications | hkf-link-list:publication | nein | — | In welchen Publikationen er steht. Wird von `hk-publikation` geführt |
| perspective | text | nein | — | Erzählperspektive, etwa `dritte-person` oder `ich` |
| story_date | date | nein | — | Wann die Handlung einsetzt |
| story_end | date | nein | — | Wann sie endet, wenn sie über einen Tag hinausgeht |
| characters | hkf-link-list:character | nein | — | Wer darin vorkommt. Wird aus dem Body abgeleitet |
| locations | hkf-link-list:location | nein | — | Wo er spielt. Wird aus dem Body abgeleitet |
| beats | hkf-link-list:beat | nein | — | Welche Motive er aufnimmt. Wird aus dem Body abgeleitet |
| props | hkf-link-list:prop | nein | — | Welche Dinge darin eine Rolle spielen |
| status | text | nein | — | Stand der Arbeit, etwa `entwurf`, `lektorat`, `fertig` |
| words | number | nein | — | Wortzahl des Body, ohne Frontmatter |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Konventionen

**Es gibt genau einen Texttyp.** Ob ein Stück als Kapitel gelesen wird, entscheidet die Lesereihenfolge seiner Publikation und nicht der Text selbst. Eine Trennung in Einzelstück und Kapitel trüge zwei Verzeichnisse, zwei Vorlagen und zwei Abläufe für denselben Gegenstand, und jede Aufnahme in eine Reihe verlangte eine Umwidmung.

Der Body ist der Text. Er beginnt ohne Vorrede und endet mit seinem letzten inhaltlichen Punkt.

`publications` und `contents` an der Publikation sagen dasselbe von zwei Seiten. Geführt werden beide von `hk-publikation`, von Hand geschrieben wird keines von beiden.

`words` ist eine Kennzahl und keine Zusicherung. Sie steht da, damit sich ein Bestand ohne Öffnen jeder Datei überblicken lässt.

**`characters`, `locations` und `beats` werden abgeleitet und nicht daneben gepflegt.** Wer im Body vorkommt, steht dort als Verweis, und die Liste im Frontmatter folgt daraus. Zwei Stellen, die dasselbe behaupten und getrennt gepflegt werden, laufen auseinander.

`story_date` und `story_end` spannen einen Zeitraum. Sie sind die Grundlage der Kontinuitätsprüfung: Zwei Texte dürfen denselben Tag nur belegen, wenn eine Figur beides an einem Tag schafft. `hk-kontinuitaet` meldet die Überschneidungen, entscheiden muss sie ein Mensch.
