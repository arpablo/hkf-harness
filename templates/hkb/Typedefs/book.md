---
type: typedef
title: Buch
description: 'Ein Werk für sich: Monographie, Sammelband, Bericht.'
source: true
created: 2026-09-01
modified: 2026-09-01T10:00:00
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| authors | hkf-link-or-text-list:person | nein | — | Urheber: als Verweis auf eine Personennotiz oder als Name, wie das Werk ihn nennt |
| subtitle | text | nein | — | Untertitel, wenn er zur Zitation gehört |
| editors | hkf-link-or-text-list:person | nein | — | Herausgeber, wenn sie von den Urhebern abweichen |
| publisher | hkf-link-or-text:organisation | nein | — | Verlag: als Verweis oder als Name |
| place | text | nein | — | Erscheinungsort |
| year | hkf-year | nein | — | Erscheinungsjahr |
| edition | text | nein | — | Auflage, etwa `2., überarbeitete Auflage` |
| volume | text | nein | — | Band; Text, weil auch `12A` vorkommt |
| pages | text | nein | — | Seitenzahl oder Umfang |
| isbn | text | nein | — | ISBN |
| doi | hkf-url | nein | — | DOI, vollständig als `https://doi.org/…` |
| lang | hkf-lang | nein | — | Sprache des Werks |
| url | hkf-url | nein | — | Fundstelle des Werks: wo es veröffentlicht ist |
| file | hkf-file:document / hkf-url | nein | — | Ausfertigung des Werks: als Datei in der Ablage oder als Adresse, etwa auf einem Dateiserver |
| accessed | date | nein | — | Datum des Abrufs |
| checksum | text | nein | — | `sha256:<hex>` über den erfassten Text; sagt beim nächsten Einlesen, ob sich die Quelle geändert hat |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Werks in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Ein Buch steht für sich: Es hat einen Verlag, oft eine ISBN, und es ist nicht
Teil eines größeren Werks. Ein Beitrag darin — ein Kapitel in einem
Sammelband — ist ein `article` mit diesem Buch als `container`.

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
