---
type: typedef
title: Begriff
description: Ein definierter Begriff.
created: 2026-08-27
modified: 2026-08-31T15:25:58
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| lang | hkf-lang | ja | — | Sprache des Begriffs |
| broader | hkf-link:term | nein | — | Übergeordneter Begriff |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Ein Abschnitt, für den keine Quelle etwas hergibt, bleibt weg und wird nicht leer hingeschrieben. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Die Definition: was der Begriff bezeichnet. |
| `## Herkunft` | Woher der Begriff kommt und wer ihn geprägt hat. |
| `## Abgrenzung` | Wovon er zu unterscheiden ist und womit er verwechselt wird. |

# Konventionen

Ein Begriff ist ein Ausdruck in **einer** Sprache, und `lang` nennt sie. Darum ist sie Pflicht und keine Vorgabe. Derselbe Gegenstand heißt in drei Sprachen dreierlei. Welche gemeint ist, darf nicht davon abhängen, in welcher Wissensbasis die Notiz gerade liegt, sonst bliebe ein Bundle nicht für sich lesbar (Core §4).

Der Body beginnt mit einer Definition in einem Satz. Synonyme werden als Obsidian-`aliases` geführt und nicht als eigene Property. Sie sind Ausdrücke derselben Sprache. Die fremdsprachige Entsprechung ist kein Alias, sondern ein eigener Begriff.

Ein Begriff legt einen Ausdruck fest und ist mit seiner Definition fertig. Wird die Notiz länger, gehört, was über die Definition hinausgeht, in ein `concept`.
