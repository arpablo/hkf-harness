---
type: typedef
title: Notiz
description: Eine Notiz ohne spezifischeren Typ.
created: 2026-08-27
modified: 2026-08-31T15:25:58
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| about | hkf-link-list | nein | — | Worauf sich die Notiz bezieht |
| sources | hkf-link-list:source | nein | — | Verwendete Quellen |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Auffangtyp. Er wird verwendet, wenn kein anderer Typ passt — nicht, um die
Wahl eines Typs zu vermeiden. `about` nimmt Verweise beliebigen Typs auf.

Eine Notiz hält fest, was bei einem Anlass anfiel: die Auswertung einer
Quelle, ein Protokoll, ein Gedanke. Überlebt ihr Gegenstand den Anlass, gehört
er in ein `concept`, und die Notiz verweist per `about` dorthin.
