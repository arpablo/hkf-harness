---
type: typedef
title: Tageseintrag
description: Was an einem Tag anfiel.
base: journal
created: 2026-09-07
modified: 2026-09-07T14:20:00
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| about | hkf-link-list | nein | — | Worauf sich der Eintrag bezieht |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Konventionen

Der Gegenstand ist der Tag und nicht die Sache. Was den Tag überdauert, bekommt eine eigene Notiz, und der Eintrag verweist per `about` dorthin. Derselbe Schnitt wie bei `note`, nur vom Datum her: `note` hält einen Anlass fest, `daily` einen Tag.

Der Eintrag liegt unter `journal_base`, nach Jahr und Monat geteilt, und trägt kein Typverzeichnis (Core §3.2.5). Der Dateiname ist `jjjj-mm-tt` und stimmt mit den Verzeichnissen über ihm überein.

**Es gibt keine Property `date`.** Der Pfad und der Dateiname sagen den Tag schon, und eine Property daneben wäre die zweite Wahrheit über dieselbe Tatsache, die Core §3.2 für den Ort ausschließt. Wer nach Datum sucht, sucht nach dem Dateinamen.

Ein Tageseintrag ist keine Wissensnotiz und wird nicht zu einer. Er darf roh bleiben, unvollständig und ohne Verbindungen. Geprüft wird an ihm dasselbe wie an jeder Notiz, nicht mehr.
