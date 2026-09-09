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
| geo | hkf-geo | nein | — | Koordinate als Paar, erst Breite, dann Länge |
| country | hkf-link:country | nein | — | Staat, in dem der Ort liegt |
| address | text | nein | — | Anschrift in einer Zeile |
| part_of | hkf-link:place,city,country | nein | — | Übergeordneter Ort |
| image | hkf-file:image / hkf-url | nein | — | Ansicht, als Datei in der Ablage oder als Adresse im Netz |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Ein Abschnitt, für den keine Quelle etwas hergibt, bleibt weg und wird nicht leer hingeschrieben. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Was für ein Ort: wo er liegt, wozu er gehört, wofür er bekannt ist. |
| `## Geschichte` | Was an ihm geschah, soweit es hier zählt. |
| `## Bedeutung` | Warum er hier steht. |

# Konventionen

`geo` trägt beide Werte in einer Angabe, erst die Breite, dann die Länge. `part_of` bildet die räumliche Schachtelung ab, also Gebäude in Stadt und Stadt in Region.

`country` ist ein Verweis und keine Kennung. Es hieße sonst auf `place` etwas anderes als auf `city`, und ein Property-Name bedeutet überall dasselbe (Core §3.7.3). Der Preis ist, dass ein Ort in einem Staat ohne eigene Notiz seinen Staat nicht nennen kann: Dann bleibt `country` leer, und der Staat steht im Body oder wird als Notiz angelegt.
