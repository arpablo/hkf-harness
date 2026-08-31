---
name: hkb-notiz
description: "Eine Notiz in einer Wissensbasis nach HKF Core anlegen oder fortschreiben — Typ wählen, nur zugesicherte Properties setzen, Verweise qualifizieren, Zeitangaben führen. Verwenden bei: Notiz anlegen, etwas in die Wissensbasis schreiben, Notiz ergänzen, Person/Ort/Quelle erfassen."
---

# Eine Notiz schreiben

Zuerst [[hkb]] lesen. Das hier ist die Operation, die kein Script erledigt —
Inhalt entsteht nicht mechanisch. Alles Formale drumherum aber schon, und das
prüfst du am Ende mit `hk-lint`.

## Ablauf

**① Typ wählen.** Die Typtabelle in `hkb.md` nennt alle Typen mit Verzeichnis
und Zweck. Passt keiner, ist das eine Frage an [[hkb-typ]] — und keine, die
du nebenbei mit einem neuen Verzeichnis beantwortest.

**② Die Typdefinition lesen.** `typedefs/<typ>.md`. Dort steht der
vollständige Vertrag: welche Properties es gibt, welchen Typ sie haben, was
Pflicht ist, und in den Konventionen, was der Typ meint.

**③ Prüfen, ob es die Notiz schon gibt.** Suche nach Titel und Aliasen, bevor
du anlegst. Zwei Notizen über denselben Gegenstand sind teurer als eine
Rückfrage.

**④ Schreiben.** Nach `<base>/<verzeichnis des typs>/<dateiname>.md`. Der
Dateiname ist `kebab-case` und beschreibt den Gegenstand, nicht die Notiz.

**⑤ Prüfen.**

```bash
hk-lint
```

## Das Frontmatter

```yaml
---
type: person
title: Ada Lovelace
born: 1815-12-10
birthplace: "[[places/london|London]]"
created: 2026-08-31
modified: 2026-08-31T09:14:00
modified_by: claude-opus-5
---
```

- **`type` ist die einzige Pflicht** (§3.3) — alles andere sagt die
  Property-Tabelle des Typs.
- **Erfinde keine Properties.** Was nicht in der Tabelle steht, ist zwar
  erlaubt, wird aber von niemandem geprüft und taucht in `hk-lint --strict`
  als undeklariert auf. Wenn du eine brauchst, die es nicht gibt: sag es,
  statt sie stillschweigend zu setzen.
- **Lies die Spalte `Vorgabe`.** Steht dort ein Wert, heißt die Abwesenheit
  der Property genau diesen Wert — `cancelled` ohne Eintrag heißt „nicht
  abgesagt", nicht „unbekannt". Dann schreibst du ihn **nicht** hin; er gilt
  ohnehin (§3.7). Steht dort `—`, heißt Abwesenheit „weiß ich nicht", und du
  darfst sie offen lassen, statt etwas zu erfinden.
- **Flach bleiben** (§3.4): Text, Liste, Zahl, Checkbox, Datum, Datum mit
  Uhrzeit. Keine verschachtelten Abbildungen, keine leeren Werte — eine leere
  Property wird weggelassen, nicht leer geschrieben.
- **Ein Wikilink in einer Property gehört in Anführungszeichen**, sonst liest
  YAML die eckigen Klammern als Liste.
- **`created` ist ein Datum, `modified` ein Zeitpunkt in UTC.** Beim Ändern
  einer fremden Notiz: `modified` auf jetzt, `modified_by` auf deinen
  Modellnamen. Vorhandenes `created` bleibt.

## Verweise

Ein Verweis ist ein **qualifizierter Wikilink mit Alias**: der volle Pfad ab
der Vault-Wurzel ohne `.md`, dann `|`, dann der Anzeigetext — in der Regel
der `title` des Ziels.

```markdown
[[wissen/persons/ada-lovelace|Ada Lovelace]]
```

Der erste Abschnitt ist der Ablagepfad; er entfällt, wenn die Wissensbasis in
der Vault-Wurzel liegt. In `hkb.md` und `AGENTS.md` steht er nie — diese
beiden verweisen relativ zu sich selbst.

**Im Body verlinkst du beim Schreiben**, wo der Text es hergibt. Was nicht
aus dem Text hervorgeht, kommt unter `# Siehe auch` — als letzter Abschnitt,
alphabetisch, jede Zeile mit ` — ` und einem Grund:

```markdown
# Siehe auch

- [[maschines/analytical-engine|Analytical Engine]] — beide Notizen nennen einander
```

**Der Grund ist Pflicht.** Er sagt, *warum* verlinkt wurde, nicht, was am Ziel
steht. Und: hinzufügen ja, entfernen nein.

## Eine fremde Notiz fortschreiben

- **Ergänzen, nicht ersetzen.** Was dasteht, hat jemand hingeschrieben.
- **Widerspricht deine Quelle dem Bestand**, schreib beides hin, mit Datum
  und Herkunft. Aus Uneinigkeit einen Konsens zu machen ist der teuerste
  Fehler, den ein Modell in einer Wissensbasis machen kann: Eine saubere
  Notiz strahlt Autorität aus, die ihr Inhalt nicht deckt.
- **`# Siehe auch` bleibt vollständig.** Du darfst Zeilen hinzufügen — mit
  Grund —, aber keine entfernen. Ein Ziel in `rejected_links` verlinkst du
  nicht.
- **`typedefs/` und `proptypes/` fasst du nicht an.**
