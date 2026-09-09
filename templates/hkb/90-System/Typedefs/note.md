---
type: typedef
title: Notiz
description: Eine Notiz ohne spezifischeren Typ.
created: 2026-08-27
modified: 2026-08-31T15:25:58
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| about | hkf-link-list | nein | — | Worauf sich die Notiz bezieht |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Der Typ ist ein Auffangtyp, und die Gliederung ist entsprechend weit: Ein Abschnitt, für den es nichts gibt, bleibt weg. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Was festgehalten wird und bei welchem Anlass. |
| `## Befund` | Was sich gezeigt hat, mit Fundstelle, wo es eine gibt. |
| `## Was daraus folgt` | Was zu tun, zu prüfen oder weiterzuverfolgen ist. |

**Hält die Notiz eine Lektüre fest, trennt sie drei Dinge sichtbar:** was das Werk behauptet, was über den Gegenstand berichtet wird, und was der Lesende selbst einwendet. Ein Einwand, der aussieht wie eine Aussage des Autors, ist ein Fehler und keine Geschmacksfrage. Die Fundstelle steht bei der Behauptung, nicht beim Einwand.

# Konventionen

Auffangtyp. Er wird verwendet, wenn kein anderer Typ passt, und nicht, um die Wahl eines Typs zu vermeiden. `about` nimmt Verweise beliebigen Typs auf.

Eine Notiz hält fest, was bei einem Anlass anfiel: die Auswertung einer Quelle, ein Protokoll, ein Gedanke. Überlebt ihr Gegenstand den Anlass, gehört er in ein `concept`, und die Notiz verweist per `about` dorthin.
