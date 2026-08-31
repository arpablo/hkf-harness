---
type: typedef
title: Quelle
description: 'Eine zitierbare Quelle: Buch, Aufsatz, Webseite, Vortrag.'
created: 2026-08-27
modified: 2026-08-31T15:25:58
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| authors | hkf-link-list:person | nein | — | Urheber |
| year | hkf-year | nein | — | Erscheinungsjahr |
| publisher | hkf-link:organisation | nein | — | Verlag oder Herausgeber |
| url | hkf-url | nein | — | Fundstelle im Netz |
| doi | hkf-url | nein | — | DOI, vollständig als `https://doi.org/…` |
| isbn | text | nein | — | ISBN |
| lang | hkf-lang | nein | — | Sprache der Quelle |
| accessed | date | nein | — | Datum des Abrufs |
| file | hkf-file:document | nein | — | Beigelegtes Dokument |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Eine Quellennotiz beschreibt das zitierte Werk, nicht die eigene Auswertung.
Was man daraus gelernt hat, gehört in eine `note`, die per `sources` auf die
Quelle verweist.

`url` und `file` sind bewusst zwei Properties und keine Alternative (Core §3.7.2):
`url` ist die Fundstelle des Werks, `file` eine in der Ablage liegende
Ausfertigung. Beide dürfen nebeneinander gesetzt sein.
