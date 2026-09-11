---
type: typedef
title: Zusammenfassung
description: Was eine Quelle sagt, auf drei Seiten.
dir: Summaries
created: 2026-09-09
modified: 2026-09-09T11:01:45
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| summarizes | hkf-link:source | ja | — | Die Quelle, die zusammengefasst wird |
| covers | text | nein | — | Welcher Teil des Werks, wenn nicht das ganze, etwa `Kapitel 1 bis 3` |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Anders als bei den übrigen Typen bleibt hier kein Abschnitt weg: Eine Zusammenfassung ohne Kernaussagen oder ohne Vorschläge ist keine. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Worum es in der Quelle geht, in wenigen Sätzen. |
| `## Kernaussagen` | Die tragenden Argumente und Erkenntnisse, jedes mit seiner Fundstelle im Werk. |
| `## Essayvorschläge` | Fünf Vorschläge, was sich aus der Quelle schreiben ließe, jeder mit seiner These in einem Satz. |

# Konventionen

Eine Quellennotiz gibt das Werk wieder, gegliedert nach dessen eigenem Aufbau, und wächst mit ihm (§3.8). Eine Zusammenfassung ist die **Lektüre**: verdichtet, begrenzt und um das ergänzt, was sich aus dem Werk machen ließe. Beide stehen nebeneinander, weil das eine so lang wird wie sein Gegenstand und das andere nicht.

**Drei Seiten sind die Grenze.** Der Body SOLLTE 9.000 Zeichen nicht überschreiten, also rund drei Seiten DIN A4. Die Grenze ist der Zweck des Typs und keine Formalie: Wer eine Zusammenfassung liest, will nicht das Werk noch einmal lesen. Was nicht hineinpasst, gehört in die Quellennotiz oder in ein `concept`.

**Die fünf Vorschläge gehören zur Notiz und sind kein Anhang.** Jeder nennt eine These und einen Satz dazu, warum sie trägt. Geschrieben wird der Essay woanders, unter `output_base` (Core §3.2.4). Ein Vorschlag behauptet nichts über die Welt, darum bleibt die Zusammenfassung eine Wissensnotiz und wandert nicht selbst unter die Erzeugnisse.

Fünf ist eine gesetzte Zahl und keine gemessene. Sie ist groß genug, dass es beim Naheliegenden nicht bleibt, und klein genug, dass jeder Vorschlag noch durchdacht ist.

`summarizes` nimmt genau eine Quelle und ist Pflicht: Eine Zusammenfassung ohne ihr Werk sagt nicht, wovon sie handelt. Zwei Werke nebeneinanderzustellen ist Sache eines `comparison` (§3.11).

Eine Quelle darf mehrere Zusammenfassungen tragen, etwa je Lesart oder je Zweck, und sie braucht keine. Welcher Teil des Werks gemeint ist, sagt `covers`. Ohne die Angabe gilt das ganze.

**Das Verzeichnis heißt `Summaries`.** Die Vorgabe aus Core §3.7 ergäbe `Summarys`, wie sie bei `city` und `country` `Citys` und `Countrys` ergäbe (§3.16, §3.17).
