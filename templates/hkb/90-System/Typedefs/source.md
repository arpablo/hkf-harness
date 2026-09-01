---
type: typedef
title: Quelle
description: Ein Werk, auf das sich die Wissensbasis beruft.
created: 2026-09-01
modified: 2026-09-01T17:00:00
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| kind | hkf-source-kind | nein | — | Werkart: Buch, Aufsatz, Video, Webseite und die übrigen |
| authors | hkf-link-or-text-list:person | nein | — | Urheber: als Verweis auf eine Personennotiz oder als Name, wie das Werk ihn nennt |
| published | date | nein | — | Erscheinungsdatum |
| published_year | hkf-year | nein | — | Erscheinungsjahr, wenn kein vollständiges Datum bekannt ist |
| lang | hkf-lang | nein | — | Sprache des Werks |
| url | hkf-url | nein | — | Fundstelle des Werks: wo es veröffentlicht ist |
| file | hkf-file:document,clipping / hkf-url | nein | — | Ausfertigung des Werks: als Datei in der Ablage oder als Adresse, etwa auf einem Dateiserver |
| accessed | date | nein | — | Datum des Abrufs |
| checksum | text | nein | — | `sha256:<hex>` über die Ausfertigung; sagt beim nächsten Einlesen, ob sich die Quelle geändert hat |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Werks in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Eine Quellennotiz beschreibt das Werk, auf das sich die Wissensbasis beruft,
und fasst zusammen, **was es sagt** — gegliedert nach seinem eigenen Aufbau,
je Kapitel oder Hauptabschnitt eine Überschrift. Was man daraus **für die
eigene Sache schließt**, gehört nicht hierher, sondern in eine `note` oder ein
`concept`, das per `sources` auf die Quelle verweist.

**Die Werkart ist eine Property und kein Typ.** Ein Buch, ein Aufsatz, ein
Video und eine Webseite unterscheiden sich in dem, was über sie zu wissen ist,
kaum: Wer es gemacht hat, wann es erschien, wo es liegt. Was sie unterscheidet
— Verlag, Auflage, Seitenzahl —, ist Zitationsapparat und steht dort, wo er
gebraucht wird: im Body oder in einer Property, die eine Wissensbasis selbst
anlegt. Als vier Typen kostete die Unterscheidung vier Verzeichnisse und
zwanzig Properties, von denen die meisten immer leer blieben — und eine
Quelle, deren Art keiner der vier entspricht, hätte gar keinen Ort gehabt.
`kind` kennt sieben Werte (§2.2), und eine spätere Fassung darf ergänzen.

**Die Quellennotiz liegt direkt unter `source_base`**, ohne Typverzeichnis
(Core §3.2.2). Bei einem einzigen Quelltyp wäre es reine Verdopplung, und die
Notiz-ID ist damit der bloße Dateiname.

`url` und `file` bezeichnen Verschiedenes und stehen darum als zwei
Properties da, nicht als Alternative (Core §3.7.2): `url` ist, **wo das Werk
veröffentlicht ist** — die Verlagsseite, die DOI-Adresse —, und damit
zitierfähig. `file` ist, **wo die eigene Ausfertigung liegt**: als Datei in
der Ablage oder als Adresse, etwa auf einem Dateiserver im eigenen Netz. Ein
Original muss also nicht in die Ablage kopiert werden, um verzeichnet zu sein.
Beide dürfen nebeneinander stehen.

**Ist `file` ein Clipping, steht der erfasste Text dort und nicht im Body.**
Ein Clipping ist eine Mediendatei unter `<media_base>/Clippings/` (Core
§3.2.1) — Rohmaterial, das niemand pflegt und das darum auch niemand prüft.
Die Notiz daneben trägt die Zusammenfassung. Das ist der ganze Unterschied
zwischen einer erfassten und einer bloß zitierten Seite, und er verlangt
keinen eigenen Typ: Die Datei ist da oder sie ist es nicht.

`checksum` sagt beim nächsten Einlesen, ob sich die Quelle geändert hat. Eine
Webseite ändert sich still, und ohne die Prüfsumme fiele das erst auf, wenn
die Zusammenfassung schon nicht mehr stimmt.

`published` und `published_year` schließen einander aus, wie `born` und
`born_year` bei einer Person (§3.4). Ein Buch von 1989 hat einen Tag, der
niemanden interessiert, ein Beitrag vom 28. Juli 2026 hat einen, der zählt.
Eine Angabe zu erzwingen, die die Quelle nicht hergibt, brächte nur falsche
Genauigkeit — und beide in eine Property zu legen ginge nicht: Alternativen
müssen dieselbe Wertform haben (§3.7.2).
