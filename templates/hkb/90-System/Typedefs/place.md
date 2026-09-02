---
type: typedef
title: Ort
description: Ein geographischer Ort.
created: 2026-08-27
modified: 2026-09-02T15:28:03
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| latitude | hkf-latitude | nein | — | Geographische Breite |
| longitude | hkf-longitude | nein | — | Geographische Länge |
| country | hkf-link:country | nein | — | Staat, in dem der Ort liegt |
| address | text | nein | — | Anschrift in einer Zeile |
| part_of | hkf-link:place,city,country | nein | — | Übergeordneter Ort |
| image | hkf-file:image / hkf-url | nein | — | Ansicht, als Datei in der Ablage oder als Adresse im Netz |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

`latitude` und `longitude` werden nur gemeinsam gesetzt. `part_of` bildet die
räumliche Schachtelung ab — Gebäude in Stadt, Stadt in Region.

`country` ist ein Verweis und keine Kennung. Es hieße sonst auf `place`
etwas anderes als auf `city`, und ein Property-Name bedeutet überall dasselbe
(Core §3.7.3). Der Preis ist, dass ein Ort in einem Staat ohne eigene Notiz
seinen Staat nicht nennen kann: Dann bleibt `country` leer, und der Staat
steht im Body oder wird als Notiz angelegt.
