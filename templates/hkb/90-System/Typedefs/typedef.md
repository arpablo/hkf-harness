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
| is_source | checkbox | nein | false | Die Instanzen dieses Typs sind Quellen; ihr Verzeichnis liegt unter `source_base` statt unter `wiki_base` (Core §3.2.2) |

# Konventionen

Der Dateiname ist der Typname (Core §3.7). Der Body trägt die Property-Tabelle und
die Konventionen des Typs. `dir` ist ein relativer Pfad zum Basispfad, mit
`/` als Trennzeichen und beliebig vielen Abschnitten, ohne führenden und
abschließenden `/` und ohne `.`- oder `..`-Abschnitte; er darf nicht unter
`media_base` liegen und, wenn der Typ nicht `is_source: true` trägt, auch nicht
unter `source_base` (Core §3.2.2).

`provisional` steht nur an einer Typdefinition, nur mit dem Wert `true` und
nur in einer HKB — ein Bundle enthält keine vorläufige Typdefinition (Core §7.1).
Eine solche Notiz trägt kein `dir`, keinen Abschnitt `# Properties` und kein
`bundles`.

**Warum `is_source` und nicht `source`.** Der kürzere Name ist vergeben: `source`
ist die Property, mit der eine Bundle-Notiz sagt, woher die Lieferung stammt
(§3.3). Zwei Bedeutungen unter einem Namen wären genau die Namensdrift, gegen
die dieselbe Ablage anderswo lintet — und ein Schema, das über alle Notizen
gilt, könnte sie nicht auseinanderhalten.

`is_source` verschiebt allein den Ort und sonst nichts: Ein Quelltyp bestimmt
sein Verzeichnis über `dir` wie jeder andere, und die Vorgabe gilt
unverändert; nur hängt das Verzeichnis dann unter `source_base` statt unter
`wiki_base`. Die Angabe steht an der Typdefinition und nicht als Liste in der
Wurzeldatei, weil dort schon alles andere über den Typ steht — und weil eine
Ablage, die einen eigenen Quellentyp anlegt, sonst zwei Stellen ändern
müsste.
