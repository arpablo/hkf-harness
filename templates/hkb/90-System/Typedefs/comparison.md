---
type: typedef
title: Vergleich
description: Eine Gegenüberstellung mehrerer Gegenstände entlang benannter Dimensionen.
created: 2026-08-31
modified: 2026-08-31T15:25:58
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| compares | hkf-link-list | ja | — | Die verglichenen Gegenstände, mindestens zwei |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Hier bleibt kein Abschnitt weg: Ein Vergleich ohne Dimensionen ist eine Behauptung, einer ohne Urteil eine Tabelle. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Was verglichen wird und welche Frage der Vergleich beantworten soll. |
| `## Dimensionen` | In welchen Hinsichten verglichen wird, als Tabelle mit einer Zeile je Hinsicht. |
| `## Urteil` | Das eigene Urteil, mit seiner Begründung. |

**Der Vergleich spricht in eigenen Worten.** Zwei Werke gebrauchen denselben Begriff selten gleich, und wer die Sprache eines der beiden übernimmt, hat die Frage schon zu dessen Gunsten entschieden. Die Dimensionen werden darum so benannt, dass beide Seiten sich darin wiederfinden, und die Begriffe der Verglichenen stehen als deren Begriffe da.

**Ein Widerspruch wird festgehalten und nicht geglättet (Core §3.3).** Dass zwei Quellen dasselbe verschieden sehen, ist eine Auskunft über den Gegenstand. Jede Deutung steht bei ihrer Quelle, und das Urteil sagt, welche von beiden warum weiter trägt. Trägt keine weiter, sagt es das.

# Konventionen

Der Gegenstand eines Vergleichs ist kein Ding, sondern ein Verhältnis. Der Body nennt zuerst, was verglichen wird und warum, dann die Dimensionen, am besten als Tabelle mit einer Zeile je Dimension, zuletzt das Urteil. Ein Vergleich ohne Urteil ist eine Tabelle und gehört in die Notiz eines der Verglichenen.

`compares` nimmt Verweise beliebigen Typs auf: Verglichen wird, was sich vergleichen lässt, zwei Konzepte ebenso wie zwei Körperschaften. Was nur einen der Gegenstände betrifft, gehört in dessen eigene Notiz.
