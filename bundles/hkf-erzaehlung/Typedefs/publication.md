---
type: typedef
base: output
title: Publikation
description: Eine Folge von Texten in einer festgelegten Lesereihenfolge.
created: 2026-09-04
modified: 2026-09-04T00:00:00
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| subtitle | text | nein | — | Untertitel |
| authors | hkf-link-or-text-list | nein | — | Wer sie verantwortet, als Notiz oder als Name |
| publisher | text | nein | — | Wer sie herausgibt |
| rights | text | nein | — | Rechtevermerk, wie er im Werk erscheint |
| cover | hkf-file:image | nein | — | Das Titelbild |
| contents | hkf-link-list:text | nein | — | Die Texte in ihrer Lesereihenfolge. Wird von `hk-publikation` geführt |
| status | text | nein | — | Stand, etwa `offen`, `fertig`, `veröffentlicht` |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Konventionen

Eine Publikation trägt selbst keinen Fließtext des Werkes. Sie sagt, was dazugehört und in welcher Reihenfolge, und der Body erklärt, was sie zusammenhält.

**`contents` ist geordnet.** Das ist die einzige Property des Formats, bei der die Reihenfolge etwas bedeutet, und deshalb steht es hier. Ein Werkzeug, das sie umsortiert, ändert das Werk.

Der Abschnitt `# Inhalt` im Body zeigt dieselbe Reihenfolge lesbar an. `hk-publikation` schreibt beides und hält es gleich.

Eine Publikation ohne `contents` ist kein Fehler, sondern eine, die noch leer ist.
