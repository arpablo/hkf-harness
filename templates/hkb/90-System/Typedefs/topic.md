---
type: typedef
title: Thema
description: Ein Themengebiet als Einstiegspunkt.
created: 2026-08-27
modified: 2026-08-31T15:25:58
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| parent | hkf-link:topic | nein | — | Übergeordnetes Thema |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Was das Thema umfasst und wo seine Grenzen liegen. |
| `## Einstiege` | Über welche Notizen man das Thema betritt, jede mit einem Satz dazu, wofür sie steht. |

**Ein Thema trägt keine eigenen Tatsachen.** Was hier stünde, stünde ein zweites Mal da und veraltete an einer der beiden Stellen. Die Einstiegsliste ist geordnet und nicht vollständig: Sie nennt die Notizen, mit denen ein Leser anfangen soll, nicht alle, die zum Thema gehören. Wer alle sucht, fragt den Bestand ab.

# Konventionen

Ein Thema ordnet, ein Begriff definiert, ein Konzept sammelt. Der Body ist eine Einstiegsseite mit Verweisen. Inhalte, die anderswo hingehören, stehen nicht hier.
