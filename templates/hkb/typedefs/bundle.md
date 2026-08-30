---
type: typedef
title: Bundle
description: Beschreibt eine Lieferung.
created: 2026-08-27
modified: 2026-08-27T15:16:52
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| id | text | ja | Kennung der Lieferreihe; in der HKB gleich dem Dateinamen |
| version | text | ja | Unveränderliche Kennung der gelieferten Fassung |
| source | text | nein | Herkunft, etwa eine URL oder ein Repository |
| imported | datetime | nein | Zeitpunkt der Übernahme |

# Konventionen

Als `hbundle.md` in der Wurzel eines Bundles trägt die Notiz zusätzlich die
Wurzeldatei-Properties und die Typtabelle im Body; `imported` entfällt dort.
In der HKB liegt sie als `bundles/<id>.md` ohne diese Zusätze.

`source` ist `text` und nicht `hkf-url`, weil auch ein Repository-Verweis oder
ein Datenträger als Herkunft in Frage kommt.
