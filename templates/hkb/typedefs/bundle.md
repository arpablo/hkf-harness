---
type: typedef
title: Bundle
description: Beschreibt eine Lieferung.
created: 2026-08-27
modified: 2026-08-31T13:39:27
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| id | text | ja | Kennung der Lieferreihe in `kebab-case` (§4.1); in der HKB gleich dem Dateinamen |
| version | text | nein | Unveränderliche Kennung der gelieferten Fassung; ohne sie hat die Lieferung keine Geschichte, nur einen letzten Stand (§4.1) |
| description | text | ja | Ein Satz darüber, was die Lieferung enthält |
| required_bundles | list | nein | Bundles, die vorher importiert sein sollen (§4.1) |
| source | text | nein | Herkunft, etwa eine URL oder ein Repository |
| imported | datetime | nein | Zeitpunkt der Übernahme, in **UTC** (§3.4); nur in der HKB (§5.1). Fehlt es an einer Bundle-Notiz der HKB, wurde die Lieferung geprüft und nicht übernommen (§5.7) |

# Konventionen

Als `hbundle.md` in der Wurzel eines Bundles trägt die Notiz zusätzlich die
Wurzeldatei-Properties und die Typtabelle im Body; `imported` entfällt dort.
In der HKB liegt sie als `bundles/<id>.md` ohne diese Zusätze.

`source` ist `text` und nicht `hkf-url`, weil auch ein Repository-Verweis oder
ein Datenträger als Herkunft in Frage kommt.
