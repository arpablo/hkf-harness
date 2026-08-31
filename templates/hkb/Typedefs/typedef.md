---
type: typedef
title: Typdefinition
description: Registriert einen Typ und legt sein Verzeichnis fest.
created: 2026-08-27
modified: 2026-08-31T16:49:53
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| description | text | ja | — | Einzeiliger Zweck; erscheint in der Typtabelle der Wurzeldatei |
| dir | text | nein | — | Verzeichnis der Instanzen; Vorgabe ist der groß geschriebene Typname mit angehängtem `s` (§3.7) |
| provisional | checkbox | nein | false | Beim Import angelegt, weil niemand den Typ definiert hat (§5.4) |

# Konventionen

Der Dateiname ist der Typname (§3.7). Der Body trägt die Property-Tabelle und
die Konventionen des Typs. `dir` ist ein relativer Pfad zum Basispfad, mit
`/` als Trennzeichen und beliebig vielen Abschnitten, ohne führenden und
abschließenden `/` und ohne `.`- oder `..`-Abschnitte; er darf nicht unter
`media_base` liegen.

`provisional` steht nur an einer Typdefinition, nur mit dem Wert `true` und
nur in einer HKB — ein Bundle enthält keine vorläufige Typdefinition (§7.1).
Eine solche Notiz trägt kein `dir`, keinen Abschnitt `# Properties` und kein
`bundles`.
