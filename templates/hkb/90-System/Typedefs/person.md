---
type: typedef
title: Person
description: Ein Mensch.
created: 2026-08-27
modified: 2026-08-31T18:06:05
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| full_name | text | nein | — | Vollständiger Name, wenn er vom Titel abweicht |
| born | date | nein | — | Geburtsdatum |
| born_year | hkf-year | nein | — | Geburtsjahr, wenn kein vollständiges Datum bekannt ist |
| died | date | nein | — | Sterbedatum |
| died_year | hkf-year | nein | — | Sterbejahr, wenn kein vollständiges Datum bekannt ist |
| birthplace | hkf-link:place,city,country | nein | — | Geburtsort |
| p_categories | hkf-person-category-list | nein | — | Rollen der Person |
| affiliations | hkf-link-or-text-list:organisation | nein | — | Zugehörigkeiten: als Verweis auf eine Organisationsnotiz oder als Name |
| homepage | hkf-url | nein | — | Persönliche Webseite |
| email | hkf-email | nein | — | Kontaktadresse |
| phone | hkf-phone | nein | — | Telefonnummer |
| portrait | hkf-file:image / hkf-url | nein | — | Bild der Person, als Datei in der Ablage oder als Adresse im Netz |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Ein Abschnitt, für den keine Quelle etwas hergibt, bleibt weg und wird nicht leer hingeschrieben. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Wer der Mensch ist: Lebensdaten, Herkunft, Rolle, wofür sein Name steht. |
| `## Werdegang` | Welchen Weg er genommen hat, bis er für diese Wissensbasis wichtig wird. |
| `## Wirken` | Was er getan hat und was daraus folgte. |
| `## Bedeutung` | Warum er hier steht und wie er beurteilt wird. |

# Konventionen

`born` und `born_year` schließen einander aus, ebenso `died` und `died_year`. Der Dateiname ist `vorname-nachname` in kebab-case.
