---
type: typedef
title: Veranstaltung
description: Ein Geschehen zu einer bestimmten Zeit.
created: 2026-08-27
modified: 2026-08-31T18:06:05
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| date | date | nein | — | Tag, wenn keine Uhrzeit bekannt ist |
| starts_at | datetime | nein | — | Beginn |
| ends_at | datetime | nein | — | Ende |
| location | hkf-link:place,city,country | nein | — | Veranstaltungsort |
| organizer | hkf-link:person,organisation | nein | — | Ausrichter |
| participants | hkf-link-list:person,organisation | nein | — | Beteiligte |
| cancelled | checkbox | nein | false | Abgesagt |
| homepage | hkf-url | nein | — | Ankündigung |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Ein Abschnitt, für den keine Quelle etwas hergibt, bleibt weg und wird nicht leer hingeschrieben. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Was geschehen ist: wann, wo, zwischen wem. |
| `## Vorgeschichte` | Was dahin führte. |
| `## Verlauf` | Wie es sich abspielte. |
| `## Folgen` | Was sich danach anders verhielt. |

# Konventionen

Eine Veranstaltung trägt entweder `starts_at` oder `date`, nicht beides. Zeiten gelten in der `timezone` der Ablage (Core §3.4).
