---
type: typedef
title: Konzept
description: Eine Sache und der Stand des Wissens über sie.
created: 2026-08-31
modified: 2026-08-31T15:25:58
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| terms | hkf-link-list:term | nein | — | Die Begriffe, unter denen die Wissensbasis die Sache führt |
| broader | hkf-link:concept | nein | — | Übergeordnetes Konzept |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Ein Abschnitt, für den keine Quelle etwas hergibt, bleibt weg und wird nicht leer hingeschrieben. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Was die Sache ist, in einem Satz, der ohne die Quellen verständlich bleibt. |
| `## Stand des Wissens` | Was über sie bekannt ist und worauf das beruht. |
| `## Strittig` | Was offen ist oder von wem bestritten wird. |

# Konventionen

Ein Begriff definiert einen Ausdruck, ein Konzept sammelt, was über eine Sache bekannt ist. Darum ist eine Begriffsnotiz mit ihrer Definition fertig, während eine Konzeptnotiz mit jeder ausgewerteten Quelle wächst: Der Body trägt den Stand des Wissens und die offenen Fragen.

Ein Begriff ist sprachgebunden und führt `lang` als Pflicht, ein Konzept nicht: Dieselbe Sache hat in drei Sprachen drei Begriffe und bleibt dieselbe Sache. `terms` nimmt sie alle auf.

Hat eine Konzeptnotiz keine eigenen Aussagen, sondern nur Verweise, ist sie ein `topic`.
