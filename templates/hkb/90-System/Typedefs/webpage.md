---
type: typedef
title: Webseite
description: Eine zitierte Webseite; ihr Text bleibt draußen.
is_source: true
created: 2026-09-01
modified: 2026-09-01T10:00:00
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| authors | hkf-link-or-text-list:person | nein | — | Urheber: als Verweis auf eine Personennotiz oder als Name, wie die Seite ihn nennt |
| container | text | nein | — | Name der Website, auf der die Seite erschien |
| year | hkf-year | nein | — | Jahr der Veröffentlichung |
| lang | hkf-lang | nein | — | Sprache des Werks |
| url | hkf-url | nein | — | Fundstelle des Werks: wo es veröffentlicht ist |
| file | hkf-file:document / hkf-url | nein | — | Ausfertigung des Werks: als Datei in der Ablage oder als Adresse, etwa auf einem Dateiserver |
| accessed | date | nein | — | Datum des Abrufs |
| checksum | text | nein | — | `sha256:<hex>` über den erfassten Text; sagt beim nächsten Einlesen, ob sich die Quelle geändert hat |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Werks in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Eine Webseite wird zitiert, nicht erfasst: Der Body trägt die
Zusammenfassung, nicht den Text der Seite. Wer den Text behalten will, legt
ein `clipping` an.

`accessed` wiegt hier schwerer als bei jedem anderen Quelltyp. Eine Webseite
hat kein Erscheinungsjahr, auf das man sich verlassen könnte, und sie kann
morgen anders lauten; das Abrufdatum ist oft das einzige, was die Zitation
festhält.

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
