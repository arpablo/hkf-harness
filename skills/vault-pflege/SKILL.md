---
name: vault-pflege
description: "Einen Obsidian-Vault pflegen, ohne ihn zu beschädigen: Frontmatter, Links, Anhänge und die Einstellungen unter .obsidian. Verwenden bei: Notizen umbauen, Links reparieren, aufräumen, Ordner verschieben."
---

# Einen Vault pflegen

Diese Regeln gelten für jeden Obsidian-Vault, auch für einen ohne HKF. Wo eine
Wissensbasis vorliegt, kommen die Werkzeuge dazu: `hk-lint` findet mehr als ein
Blick, und `hk-verweise` schreibt Verweise um, ohne zu raten.

## Grundsätze

**Erst sehen, dann anfassen.** Der Git-Status und die vorhandene Struktur sagen,
womit du es zu tun hast. Siehe [[git-sicherheit]].

**`.obsidian/` gehört dem Menschen.** Einstellungen, Themes, Plugin-Zustand,
Workspace. Nichts davon wird geändert oder gelöscht, außer der Auftrag nennt es.

**Anhänge und Mediendateien bleiben.** Eine Notiz zu löschen ist eine
Entscheidung, ein Bild zu löschen auch, und ein verwaistes Bild ist kein Grund.

**Klein bleiben und nachsehen.** Nach einem Umbau die betroffenen Verweise und
das Frontmatter prüfen. Ein Ordner, der umzieht, nimmt jeden Verweis mit, der
seinen Pfad trägt.

## Was leicht kaputtgeht

| | |
|---|---|
| Ein Wikilink über einen Zeilenumbruch | Beim Umformatieren fällt er auseinander. |
| Ein Alias mit `\|` in einer Tabelle | Der Strich beendet die Zelle, wenn er nicht maskiert ist. |
| Ein `.base`-Embed mit Alias | Der Teil hinter dem Strich wählt dort eine **Ansicht**, keinen Anzeigenamen. |
| YAML mit einem unquotierten Doppelpunkt | Das Frontmatter ist danach unlesbar, und die Notiz verliert jede Property. |
| Eine Vorlage unter `Templates/` | Sie ist keine Notiz und entgeht den meisten Prüfungen, bestimmt aber jede neue. |

## Zum Schluss

Die geänderten Dateien knapp benennen. Offene Verweise, Konflikte und
ungeprüfte Annahmen ausdrücklich nennen, statt sie im Ergebnis untergehen zu
lassen.
