---
type: typedef
title: Stadt
description: Eine Stadt.
dir: Cities
created: 2026-08-31
modified: 2026-09-02T15:28:03
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| geo | hkf-geo | nein | — | Koordinate als Paar, erst Breite, dann Länge |
| country | hkf-link:country | nein | — | Staat, in dem die Stadt liegt |
| part_of | hkf-link:place,country | nein | — | Übergeordnete Einheit, etwa Region, Provinz oder Staat |
| founded_year | hkf-year | nein | — | Jahr der Gründung, soweit überliefert |
| image | hkf-file:image / hkf-url | nein | — | Ansicht, als Datei in der Ablage oder als Adresse im Netz |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Ein Abschnitt, für den keine Quelle etwas hergibt, bleibt weg und wird nicht leer hingeschrieben. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Welche Stadt: wo sie liegt, zu welchem Staat sie gehört, wofür sie steht. |
| `## Geschichte` | Was in ihr geschah, soweit es hier zählt. |
| `## Bedeutung` | Warum sie hier steht. |

# Konventionen

Eine Stadt ist ein Ort, aber **HKF kennt keine Untertypen** (Core §3.7.1): `hkf-link:place` nimmt keine `city` an. Wo ein Verweis beides zulassen soll, werden beide genannt. `birthplace`, `seat` und `location` tun das und schreiben `hkf-link:place,city,country`, ebenso `part_of` an `place`. Das `part_of` einer Stadt lässt `city` aus: Eine Stadt liegt in einer Region oder einem Staat, nicht in einer anderen Stadt.

Wer die Unterscheidung nicht braucht, führt `city` nicht und legt Städte als `place` ab. Wer sie führt, entscheidet einmal und bleibt dabei: Dieselbe Stadt zweimal, einmal als `place` und einmal als `city`, sind für jedes Werkzeug zwei Gegenstände.

`geo` trägt beide Werte in einer Angabe, erst die Breite, dann die Länge.
