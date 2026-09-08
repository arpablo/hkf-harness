---
type: typedef
title: Organisation
description: 'Eine Körperschaft: Unternehmen, Institut, Verein, Behörde.'
created: 2026-08-27
modified: 2026-08-31T18:06:05
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| founded | date | nein | — | Gründungsdatum |
| founded_year | hkf-year | nein | — | Gründungsjahr, wenn kein Datum bekannt ist |
| dissolved | date | nein | — | Auflösungsdatum |
| dissolved_year | hkf-year | nein | — | Auflösungsjahr, wenn kein Datum bekannt ist |
| o_categories | hkf-organisation-category-list | nein | — | Art der Körperschaft |
| seat | hkf-link:place,city,country | nein | — | Sitz |
| parent | hkf-link:organisation | nein | — | Übergeordnete Körperschaft |
| homepage | hkf-url | nein | — | Webseite |
| email | hkf-email | nein | — | Kontaktadresse |
| phone | hkf-phone | nein | — | Telefonnummer |
| logo | hkf-file:image / hkf-url | nein | — | Bildmarke, als Datei in der Ablage oder als Adresse im Netz |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Ein Abschnitt, für den keine Quelle etwas hergibt, bleibt weg und wird nicht leer hingeschrieben. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Was für eine Körperschaft: wann gegründet, wo ansässig, wozu. |
| `## Verfassung und Träger` | Wer sie trug, wie sie verfasst war, wer für sie sprach. |
| `## Wirken` | Was sie getan hat und was daraus folgte. |
| `## Bedeutung` | Warum sie hier steht und wie sie beurteilt wird. |

# Konventionen

Rechtsform und Untergliederungen gehören in den Body, nicht in den Namen.
