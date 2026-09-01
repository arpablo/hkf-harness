---
type: typedef
title: Aufsatz
description: 'Ein Beitrag in einem größeren Werk: Zeitschrift, Zeitung, Sammelband.'
source: true
created: 2026-09-01
modified: 2026-09-01T10:00:00
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| authors | hkf-link-or-text-list:person | nein | — | Urheber: als Verweis auf eine Personennotiz oder als Name, wie der Beitrag ihn nennt |
| subtitle | text | nein | — | Untertitel, wenn er zur Zitation gehört |
| editors | hkf-link-or-text-list:person | nein | — | Herausgeber des aufnehmenden Werks |
| container | text | nein | — | Das aufnehmende Werk: Zeitschrift, Zeitung, Sammelband |
| publisher | hkf-link-or-text:organisation | nein | — | Verlag: als Verweis oder als Name |
| place | text | nein | — | Erscheinungsort |
| year | hkf-year | nein | — | Erscheinungsjahr |
| volume | text | nein | — | Band oder Jahrgang; Text, weil auch `12A` vorkommt |
| pages | text | nein | — | Seitenbereich, etwa `34–56` |
| doi | hkf-url | nein | — | DOI, vollständig als `https://doi.org/…` |
| lang | hkf-lang | nein | — | Sprache des Werks |
| url | hkf-url | nein | — | Fundstelle des Werks: wo es veröffentlicht ist |
| file | hkf-file:document / hkf-url | nein | — | Ausfertigung des Werks: als Datei in der Ablage oder als Adresse, etwa auf einem Dateiserver |
| accessed | date | nein | — | Datum des Abrufs |
| checksum | text | nein | — | `sha256:<hex>` über den erfassten Text; sagt beim nächsten Einlesen, ob sich die Quelle geändert hat |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Werks in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Ein Aufsatz ist ein Beitrag und kein Werk für sich; `container` nennt, worin
er steht. Ohne diese Angabe lässt er sich nicht zitieren, sie ist aber
trotzdem nicht Pflicht: Eine Quelle wird oft eingelesen, bevor alle Angaben
beisammen sind, und eine Pflicht machte die Notiz bis dahin unschreibbar.

`url` und `file` bezeichnen Verschiedenes und stehen darum als zwei
Properties da, nicht als Alternative (Core §3.7.2): `url` ist, **wo das Werk
veröffentlicht ist** — die Verlagsseite, die DOI-Adresse —, und damit
zitierfähig. `file` ist, **wo die eigene Ausfertigung liegt**: als Datei in
der Ablage oder als Adresse, etwa auf einem Dateiserver im eigenen Netz. Ein
Original muss also nicht in die Ablage kopiert werden, um verzeichnet zu sein.
Beide dürfen nebeneinander stehen.

Eine Quellennotiz beschreibt das zitierte Werk und fasst zusammen, **was es
sagt** — gegliedert nach seinem eigenen Aufbau, je Kapitel oder Hauptabschnitt
eine Überschrift. Was man daraus **für die eigene Sache schließt**, gehört
nicht hierher, sondern in eine `note` oder ein `concept`, das per `sources`
auf die Quelle verweist.
