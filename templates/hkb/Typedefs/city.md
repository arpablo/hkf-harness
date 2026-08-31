---
type: typedef
title: Stadt
description: Eine Stadt.
created: 2026-08-31
modified: 2026-08-31T18:06:05
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| latitude | hkf-latitude | nein | — | Geographische Breite |
| longitude | hkf-longitude | nein | — | Geographische Länge |
| country | hkf-link:country | nein | — | Staat, in dem die Stadt liegt |
| part_of | hkf-link:place,country | nein | — | Übergeordnete Einheit, etwa Region, Provinz oder Staat |
| founded_year | hkf-year | nein | — | Jahr der Gründung, soweit überliefert |
| image | hkf-file:image / hkf-url | nein | — | Ansicht, als Datei in der Ablage oder als Adresse im Netz |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Eine Stadt ist ein Ort, aber **HKF kennt keine Untertypen** (Core §3.7.1):
`hkf-link:place` nimmt keine `city` an. Wo ein Verweis beides zulassen soll,
werden beide genannt — `birthplace`, `seat`, `location` und `part_of` tun das
und schreiben `hkf-link:place,city,country`.

Wer die Unterscheidung nicht braucht, führt `city` nicht und legt Städte als
`place` ab. Wer sie führt, entscheidet einmal und bleibt dabei: Dieselbe Stadt
zweimal, einmal als `place` und einmal als `city`, sind für jedes Werkzeug
zwei Gegenstände.

`latitude` und `longitude` werden nur gemeinsam gesetzt.
