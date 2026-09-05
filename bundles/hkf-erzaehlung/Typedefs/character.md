---
type: typedef
title: Figur
description: Ein Mensch, der in mehreren Texten vorkommt und über sie hinweg gleich bleiben soll.
created: 2026-09-04
modified: 2026-09-04T00:00:00
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| aliases | list | nein | — | Wie sie sonst noch genannt wird |
| portrait | hkf-file:image / hkf-url | nein | — | Ein Bild, das den Kanon festhält |
| born_year | hkf-year | nein | — | Geburtsjahr, wenn es für die Rechnung gebraucht wird |
| based_on | hkf-link-or-text | nein | — | Wenn sie einer wirklichen Person nachgebildet ist |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Konventionen

**Ein Blatt entsteht ab dem zweiten Auftritt.** Wer einmal vorkommt, ist eine Nebenfigur und braucht keine Notiz. Wer wiederkommt, braucht eine, weil sich sonst niemand merkt, wie sie beim ersten Mal war.

Der Body hält fest, woran sich jeder Text messen lässt: Aussehen, Herkunft, Beruf, Prinzipien, Gewohnheiten. Er erzählt nichts. Was in einem Text geschieht, steht in diesem Text.

Eine Figur ist keine `person`. Der Typ `person` beschreibt einen Menschen, den es gibt, und stützt sich auf Quellen. Eine Figur wird gemacht und stützt sich auf die Texte, in denen sie vorkommt. `based_on` verbindet beides, wenn es einen Zusammenhang gibt.

Widerspricht ein neuer Text dem Blatt, ist das eine Entscheidung und kein Tippfehler: Entweder ändert sich der Text, oder das Blatt ändert sich und sagt, ab wann.
