---
type: typedef
title: Beurteilung
description: Das Urteil über einen Text, getrennt von ihm geführt, mit einem Abschnitt je Prüfer.
created: 2026-09-04
modified: 2026-09-04T00:00:00
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| assesses | hkf-link:text | ja | — | Der Text, über den geurteilt wird |
| reviewed | date | nein | — | Wann zuletzt gelesen wurde |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Konventionen

**Die Zahl steht am Text, die Begründung steht hier.** Der Grund ist eine Eigenheit von Obsidians Bases: Sie rechnen ohne Join. Bestand, Durchschnitt und die Frage, wo zwei Urteile auseinandergehen, entstehen nur dort, wo auch Publikation, Status und Wortzahl liegen.

Die Property heißt `assesses` und nicht `about`. `about` führt der Typ `note` als Liste, und ein Name trägt in einer Ablage genau eine Wertform (§3.7.3). Eine Beurteilung gilt genau einem Text.

Der Body führt einen Abschnitt je Prüfer, jeden mit seinem eigenen Lesedatum. **Ein Kommentar wird nie aus seinem Abschnitt herausgelöst und einem anderen Prüfer zugerechnet.** Zwei unabhängige Urteile sind mehr wert als eines, aber nur solange sie unabhängig bleiben.

**Liegt `modified` des Textes nach `reviewed`, ist die Beurteilung veraltet.** Sie gilt für eine Fassung, die es nicht mehr gibt. Das ist prüfbar, und `hk-kontinuitaet` prüft es.

Eine Beurteilung wird fortgeschrieben und nicht ersetzt. Was beim letzten Mal galt und heute behoben ist, bleibt lesbar: Es sagt, woran gearbeitet wurde.
