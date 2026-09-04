---
type: typedef
title: Bundle
description: Beschreibt eine Lieferung.
created: 2026-08-27
modified: 2026-08-31T17:54:51
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| id | text | ja | — | Kennung der Lieferreihe in `kebab-case` (Core §4.1). In der HKB gleich dem Dateinamen |
| version | text | nein | — | Unveränderliche Kennung der gelieferten Fassung. Ohne sie hat die Lieferung keine Geschichte, nur einen letzten Stand (Core §4.1) |
| description | text | ja | — | Ein Satz darüber, was die Lieferung enthält |
| required_bundles | list | nein | — | Bundles, die vorher importiert sein sollen (Core §4.1) |
| source | text | nein | — | Herkunft, etwa eine URL oder ein Repository |
| imported | datetime | nein | — | Zeitpunkt der Übernahme, in **UTC** (Core §3.4). Nur in der HKB (Core §5.1). Fehlt es an einer Bundle-Notiz der HKB, wurde die Lieferung geprüft und nicht übernommen (Core §5.7) |

# Konventionen

Als `hbundle.md` in der Wurzel eines Bundles trägt die Notiz zusätzlich die Wurzeldatei-Properties aus Core A.1 und die Typtabelle im Body. `imported` entfällt dort. In der HKB liegt sie als `Bundles/<id>.md` ohne diese Zusätze.

`source` ist `text` und nicht `hkf-url`, weil auch ein Repository-Verweis oder ein Datenträger als Herkunft in Frage kommt.

`description` ist bei einer Bundle-Notiz **Pflicht**, obwohl Core A.2 sie sonst freistellt. Wer eine Lieferung vor sich hat, müsste ohne sie den Body lesen oder die Dateien zählen, um zu erfahren, worum es geht. Sie ist außerdem die einzige Angabe, die in der Bundle-Liste einer Wissensbasis abfragbar ist.
