---
name: hkb
description: "Grundlagen für die Arbeit an einer Wissensbasis nach HKF Core: wo sie liegt, welche Regeln gelten, welche Werkzeuge es gibt. Verwenden, bevor eine der Operationen hk-init, hk-import, hk-export oder hk-lint gebraucht wird, und immer dann, wenn in einer HKB gelesen oder geschrieben werden soll."
---

# Eine Wissensbasis nach HKF Core bedienen

Dieser Skill ist die Grundlage der übrigen. Er trägt nichts bei, was nicht
schon in der Spezifikation steht — er sagt nur, wo alles liegt und was ein
Modell hier **nicht** tun soll.

## Der Satz, aus dem alles folgt

> Eine HKB ist ein gewöhnlicher Obsidian-Vault. Sie lässt sich ohne KI
> benutzen und füllen.

Daraus folgt die Arbeitsteilung: **Was mechanisch geht, macht ein Script.**
Du prüfst keinen Wikilink von Hand, du zählst keine Notizen, du schreibst
keine Typtabelle. Dafür gibt es `bin/`. Du urteilst dort, wo die
Spezifikation ein Urteil verlangt, und schreibst das Urteil auf.

## Wo die Ablage liegt

Fünf Stufen, in dieser Reihenfolge: der Aufruf, `HKB_PATH`, die gemerkte Wahl,
eine Aufwärtssuche ab dem Arbeitsverzeichnis, die Vorgabe `~/hkb`.
**Nirgends einen Pfad festschreiben**, auch nicht in einem Beispiel.

```bash
hk-ablage                    # welche Ablage gilt und woher der Pfad kommt
hk-ablage --liste            # was zur Wahl steht
hk-lint                      # die aktive Ablage
hk-lint /pfad/zur/ablage     # eine andere
```

**Fang eine Sitzung mit `hk-ablage` an**, wenn nicht ohnehin klar ist, worin
gearbeitet wird. Liegen mehrere Ablagen nebeneinander, wählt niemand für dich,
und die Vorgabe `~/hkb` wäre geraten. Nennt der Benutzer eine Ablage, merk sie
mit `hk-ablage <pfad>`, dann findet jeder weitere Befehl sie von selbst.

Drei Wurzeldateien. `hkb.md` heißt Wissensbasis, `hbundle.md` heißt Lieferung,
`vault.md` heißt gewöhnlicher Obsidian-Vault. Im dritten Fall gelten die
Schreibregeln und die Suche, aber nichts, was Typen und qualifizierte Verweise
voraussetzt.

Bevor du etwas tust: `hkb.md` lesen — dort stehen `name`, die vier
Bereiche, `timezone` und die Typtabelle. Führt die Ablage den Typ `hint`,
lies auch `Hints/`: Dort steht, was **diese** Wissensbasis für sich festgelegt
hat, und das geht den sieben Regeln vor, wo es sie berührt.

## Die Werkzeuge

| | |
|---|---|
| `hk-init <ziel>` | legt eine Wissensbasis an: Grundausstattung, Obsidian-Konfiguration, Git |
| `hk-import <bundle>` | übernimmt eine Lieferung (§6.1) |
| `hk-export <id> <ziel>` | schreibt eine Lieferung heraus (§6.2) |
| `hk-ingest <stück> --bundle <ziel>` | macht aus einer Quelle eine Lieferung; ohne Argumente zeigt es die Inbox |
| `hk-tranchen <quellennotiz>` | führt die Tranchen einer großen Quelle: `--anlegen`, `--naechste`, `--abhaken` |
| `hk-lint [--fix] [--strict]` | prüft eine Wissensbasis oder eine Lieferung (§6.3) |
| `hk-types [--umstellen]` | legt Typseiten und Bases an, damit `type` ein Verweis sein kann (§3.3) |
| `hk-ablage [<pfad>]` | welche Ablage bearbeitet wird: `--liste`, `<pfad>` merkt, `--loeschen` nimmt zurück |
| `hk-text [--gate]` | prüft deutschsprachige Texte gegen die Schreibregeln |

`hk-import --check` und `hk-lint` ohne `--fix` schreiben nichts. **Fang immer
damit an.**

## Die Schreibregeln gelten auch hier

Eine Notiz ist deutscher Fließtext, und dafür gibt es Regeln. Sie stehen im
Basissatz `rules/deutsch.json` des Harness und gelten für jede Ablage: keine
Gedankenstriche, keine Strichpunkte, keine Umlaut-Ersatzformen, dazu Warnungen
zu Satzlänge, Wortwahl und Schlussfloskeln.

```bash
hk-text <datei|verzeichnis>       # Bericht, endet immer mit 0
hk-text --gate <datei>            # endet mit 1, sobald ein Fehler auftritt
```

**Prüf, was du geschrieben hast, bevor du es stehen lässt.** Ein Fehler
blockiert, eine Warnung nicht. Nicht geprüft werden Code, Linkziele und
Bezeichner. Ebenso wenig der Em-Dash dort, wo das Format ihn verlangt: als
Trenner in `# Siehe auch` (§5.6) und als leere Vorgabe in einer
Property-Tabelle (§3.7).

Was **diese** Ablage darüber hinaus festgelegt hat, steht in ihren
`hint`-Notizen als `json`-Block mit dem Schlüssel `writing_policy`.

## Die sieben Regeln

Sie stehen hier und nirgends sonst — du brauchst sie ständig:

1. **Der Pfad bestimmt den Typ.** Eine Notiz gehört zu dem Typ, unter dessen
   Verzeichnis sie liegt; `type` muss dazu passen.
2. **Erfinde keine Properties.** Was ein Typ zusichert, steht in
   `Typedefs/<typ>.md`. Lies die Datei, bevor du ein Feld setzt.
3. **Verweise sind qualifizierte Wikilinks mit Alias** — voller Pfad ab der
   Vault-Wurzel ohne `.md`, dann `|` und der Anzeigetext.
4. **Frontmatter bleibt flach.** Nur Text, Liste, Zahl, Checkbox, Datum,
   Datum mit Uhrzeit.
5. **Wenn du änderst, schreib es hin.** `modified` auf jetzt in **UTC**,
   `modified_by` auf deinen Modellnamen.
6. **`Typedefs/` und `Proptypes/` sind tabu** — sie liegen unter
   `config_base` —, außer du legst ausdrücklich
   einen neuen Typ an (dafür gibt es `hkb-typ`).
7. **`# Siehe auch` wird ergänzt, nicht gekürzt.** Entfernen ist Sache eines
   Menschen; was weg soll, kommt in `rejected_links`.

## Was du nie tust

- **Raten.** Ein mehrdeutiger Verweis, eine offene Identitätsfrage, eine
  ungeklärte Bedeutung: vorlegen, nicht entscheiden und weitermachen.
- **Nachbauen, was ein Script kann.** Wenn du dabei bist, Wikilinks von Hand
  umzuschreiben oder eine Typtabelle zu tippen, ist der falsche Weg
  eingeschlagen.
- **Einen Befund wegräumen, statt ihn zu beheben.** `hk-lint` meldet, was es
  meldet; ein Hinweis darf stehenbleiben, ein Fehler nicht.
