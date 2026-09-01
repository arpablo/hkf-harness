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

`$HKB_PATH`, sonst `~/hkb`. Jeder Befehl nimmt einen Pfad als letztes
Argument, wenn es eine andere sein soll. **Nirgends einen Pfad festschreiben**
— auch nicht in einem Beispiel.

```bash
hk-lint                      # die Ablage aus $HKB_PATH
hk-lint /pfad/zur/ablage     # eine andere
```

Bevor du etwas tust: `hkb.md` lesen — dort stehen `name`, die vier
Bereiche, `timezone` und die Typtabelle. Führt die Ablage den Typ `hint`,
lies auch `Hints/`: Dort steht, was **diese** Wissensbasis für sich festgelegt
hat, und das geht den sieben Regeln vor, wo es sie berührt.

## Die vier Werkzeuge

| | |
|---|---|
| `hk-init <ziel>` | legt eine Wissensbasis an: Grundausstattung, Obsidian-Konfiguration, Git |
| `hk-import <bundle>` | übernimmt eine Lieferung (§6.1) |
| `hk-export <id> <ziel>` | schreibt eine Lieferung heraus (§6.2) |
| `hk-lint [--fix] [--strict]` | prüft eine Wissensbasis oder eine Lieferung (§6.3) |

`hk-import --check` und `hk-lint` ohne `--fix` schreiben nichts. **Fang immer
damit an.**

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
