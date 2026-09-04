---
type: typedef
title: Schauplatz
description: Ein Ort, an dem gespielt wird und dessen Beschaffenheit über mehrere Texte gleich bleiben soll.
created: 2026-09-04
modified: 2026-09-04T00:00:00
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| part_of | hkf-link:location | nein | — | Wo er liegt, wenn das für die Kontinuität zählt |
| based_on | hkf-link-or-text | nein | — | Wenn er einem wirklichen Ort nachgebildet ist |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Siehe auch“ steht |

# Konventionen

**Ein Blatt entsteht, sobald räumliche Kontinuität zählt.** Solange ein Ort nur genannt wird, genügt der Name im Text. Sobald sich zwei Texte darin bewegen und ein Leser merken würde, dass die Küche einmal links und einmal rechts liegt, braucht er eine Notiz.

Der Body beschreibt, was ein Text voraussetzen darf: Räume, Wege, Materialien, was von wo aus zu sehen ist.

Ein Schauplatz ist kein `place`. Ein `place` ist ein geographischer Ort, über den die Wissensbasis etwas weiß. Ein Schauplatz wird für die Kontinuität geführt, und dazu gehört auch, was es dort in Wirklichkeit nicht gibt. `based_on` verbindet beides.

`part_of` nennt hier nur `location`. Eine Lieferung muss in ihren Typen geschlossen sein (§7.1), und `place`, `city` und `country` liegen außerhalb. Wer einen Schauplatz in einer wirklichen Stadt verorten will, erweitert die Angabe nach dem Import um diese Typen.
