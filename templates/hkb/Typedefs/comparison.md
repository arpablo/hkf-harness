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
| sources | hkf-link-list:source | nein | — | Quellen des Vergleichs |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Der Gegenstand eines Vergleichs ist kein Ding, sondern ein Verhältnis. Der
Body nennt zuerst, was verglichen wird und warum, dann die Dimensionen — am
besten als Tabelle mit einer Zeile je Dimension —, zuletzt das Urteil. Ein
Vergleich ohne Urteil ist eine Tabelle und gehört in die Notiz eines der
Verglichenen.

`compares` nimmt Verweise beliebigen Typs auf: Verglichen wird, was sich
vergleichen lässt — zwei Konzepte ebenso wie zwei Körperschaften. Was nur
einen der Gegenstände betrifft, gehört in dessen eigene Notiz.
