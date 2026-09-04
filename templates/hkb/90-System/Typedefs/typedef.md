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
| description | text | ja | — | Einzeiliger Zweck, erscheint in der Typtabelle der Wurzeldatei |
| base | text | nein | wiki | Bereich, unter dem die Instanzen liegen: `wiki`, `source`, `output` oder `config` (Core §3.2) |
| dir | text | nein | — | Verzeichnis der Instanzen. Vorgabe ist der groß geschriebene Typname mit angehängtem `s` (Core §3.7) |
| provisional | checkbox | nein | false | Beim Import angelegt, weil niemand den Typ definiert hat (Core §5.4) |

# Konventionen

Der Dateiname ist der Typname (Core §3.7). Der Body trägt die Property-Tabelle und die Konventionen des Typs. `dir` ist ein relativer Pfad zum Basispfad, mit `/` als Trennzeichen und beliebig vielen Abschnitten, ohne führenden und abschließenden `/` und ohne `.`- oder `..`-Abschnitte. Er darf weder unter `media_base` noch unter `source_base` liegen (Core §3.2.1 und §3.2.2). Der Typ `source` trägt kein `dir`: Er liegt unmittelbar unter seinem Bereich.

`base` sagt, in welchem Bereich die Notizen des Typs liegen (Core §3.2). Ohne die Angabe gilt `wiki`. Drei Typnamen brauchen sie nicht, weil ihr Bereich schon im Namen steht: `typedef` und `proptype` liegen unter `config_base`, `source` unter `source_base`. `base: media` gibt es nicht, dort liegen Dateien und keine Notizen.

`provisional` steht nur an einer Typdefinition, nur mit dem Wert `true` und nur in einer HKB. Ein Bundle enthält keine vorläufige Typdefinition (Core §7.1). Eine solche Notiz trägt kein `dir`, keinen Abschnitt `# Properties` und kein `bundles`.

**Welcher Bereich gilt, sagt der Typname und nicht eine Property.** `typedef` und `proptype` liegen unter `config_base`, `source` unter `source_base`, jeder andere unter `wiki_base` (Core §3.2). Eine Property dafür lohnt sich erst, wenn eine Ablage mehrere Quelltypen hätte. HKF führte kurz ein `is_source`. Eine Ablage hat einen Quelltyp, und die Werkart trägt `kind` (§3.8).