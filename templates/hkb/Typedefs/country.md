---
type: typedef
title: Staat
description: Ein Staat.
created: 2026-08-31
modified: 2026-08-31T18:06:05
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| code | hkf-country | nein | — | Kennung nach ISO 3166-1 alpha-2, etwa `DE` |
| capital | hkf-link:city | nein | — | Hauptstadt |
| founded_year | hkf-year | nein | — | Jahr der Staatsgründung |
| dissolved_year | hkf-year | nein | — | Jahr des Untergangs, wenn der Staat nicht mehr besteht |
| flag | hkf-file:image / hkf-url | nein | — | Flagge, als Datei in der Ablage oder als Adresse im Netz |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

`code` und der Property-Typ `hkf-country` sagen dasselbe auf zwei Wegen, und
beide werden gebraucht. `place` trägt die Kennung unmittelbar, weil ein Ort in
einem Staat liegen kann, zu dem die Wissensbasis keine Notiz führt. Führt sie
eine, verweist sie darauf — und `code` verbindet die beiden Schreibweisen.

`dissolved_year` macht den Typ für historische Bestände brauchbar: Ein Staat,
der untergegangen ist, bleibt der Staat, in dem jemand geboren wurde. Er wird
nicht gelöscht und nicht durch seinen Nachfolger ersetzt.

Ein Staat ist kein `organisation`. Die Regierung eines Staates ist eine
Körperschaft und bekommt eine eigene Notiz.
