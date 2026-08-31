---
type: typedef
title: Property-Typ
description: Schränkt eine Wertform ein.
created: 2026-08-27
modified: 2026-08-31T17:54:51
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| form | text | ja | — | Eine der sechs Wertformen aus Core §3.4 |
| pattern | text | nein | — | Regulärer Ausdruck; nur bei `text` und `list`, dort je Eintrag |
| values | list | nein | — | Erlaubte Werte; als Text geführt, auch wenn sie wie Zahlen aussehen |
| unit | text | nein | — | Maßeinheit; beschreibend, nicht geprüft |
| min | number | nein | — | Kleinster zulässiger Wert; nur bei `form: number` |
| max | number | nein | — | Größter zulässiger Wert; nur bei `form: number` |

# Konventionen

Der Dateiname ist der Name des Property-Typs (Core §3.5) und endet nicht auf
`-list`. Für eine der sechs Wertformen wird kein Property-Typ angelegt. `min`
und `max` gibt es nur für Zahlen: Obsidian ordnet einem Property-Namen genau
eine Wertform zu, sie könnten also nicht zugleich Datumsgrenzen sein.
