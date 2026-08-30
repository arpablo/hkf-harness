---
type: typedef
title: Typdefinition
description: Registriert einen Typ und legt sein Verzeichnis fest.
created: 2026-08-27
modified: 2026-08-28T13:51:33
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| description | text | ja | Einzeiliger Zweck; erscheint in der Typtabelle der Wurzeldatei |
| dir | text | nein | Verzeichnis der Instanzen; Vorgabe ist der Typname mit angehängtem `s` |
| provisional | checkbox | nein | Beim Import angelegt, weil niemand den Typ definiert hat |

# Konventionen

Der Dateiname ist der Typname. Der Body trägt die Property-Tabelle und die
Konventionen des Typs. `dir` ist ein relativer Pfad ohne führenden und
abschließenden `/` und ohne `..`; er darf nicht unter `media_base` liegen.

`provisional: true` kennzeichnet eine Typdefinition, die beim Import entstanden
ist, weil weder das Bundle noch die Wissensbasis den Typ definiert hat. Sie
trägt kein `dir`, keinen Abschnitt `# Properties` und kein `bundles`, und sie
wird nicht ausgeliefert. Sobald die richtige Typdefinition nachkommt, ersetzt
sie diese.
