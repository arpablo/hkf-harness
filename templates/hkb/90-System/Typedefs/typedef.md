---
type: typedef
title: Typdefinition
description: Registriert einen Typ und legt sein Verzeichnis fest.
created: 2026-08-27
modified: 2026-08-31T17:54:51
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| description | text | ja | — | Einzeiliger Zweck; erscheint in der Typtabelle der Wurzeldatei |
| dir | text | nein | — | Verzeichnis der Instanzen; Vorgabe ist der groß geschriebene Typname mit angehängtem `s` (Core §3.7) |
| provisional | checkbox | nein | false | Beim Import angelegt, weil niemand den Typ definiert hat (Core §5.4) |

# Konventionen

Der Dateiname ist der Typname (Core §3.7). Der Body trägt die Property-Tabelle und
die Konventionen des Typs. `dir` ist ein relativer Pfad zum Basispfad, mit
`/` als Trennzeichen und beliebig vielen Abschnitten, ohne führenden und
abschließenden `/` und ohne `.`- oder `..`-Abschnitte; er darf weder unter
`media_base` noch unter `source_base` liegen (Core §3.2.1 und §3.2.2). Der Typ
`source` trägt kein `dir`: Er liegt unmittelbar unter seinem Bereich.

`provisional` steht nur an einer Typdefinition, nur mit dem Wert `true` und
nur in einer HKB — ein Bundle enthält keine vorläufige Typdefinition (Core §7.1).
Eine solche Notiz trägt kein `dir`, keinen Abschnitt `# Properties` und kein
`bundles`.

**Welcher Bereich gilt, sagt der Typname und nicht eine Property.** `typedef`
und `proptype` liegen unter `config_base`, `source` unter `source_base`, jeder
andere unter `wiki_base` (Core §3.2). Eine Property dafür — HKF führte kurz ein
`is_source` — lohnt sich erst, wenn eine Ablage mehrere Quelltypen hätte; sie
hat einen, und die Werkart trägt `kind` (§3.8).