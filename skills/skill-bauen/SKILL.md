---
name: skill-bauen
description: "Einen neuen Skill für das hkf-Plugin anlegen: Ordner, Frontmatter, Namensregel und die Frage, was ein Skill überhaupt tun darf. Verwenden bei: neuen Skill anlegen, Skill schreiben, Ablauf festhalten."
---

# Einen Skill anlegen

## Die Regel, die vor allem anderen kommt

> **Kein Skill tut etwas, das kein Script tut.**

Ein Skill wählt aus, erklärt, fragt zurück und urteilt dort, wo die
Spezifikation ein Urteil verlangt. Alles Mechanische steht in `bin/` und
`lib/`.

Der Grund ist eine Zusage des Harness: Eine Wissensbasis lässt sich ohne KI
benutzen und füllen. Sobald eine Operation nur über ein Modell erreichbar ist,
stimmt das nicht mehr. Dazu kommt die Verlässlichkeit. Ein Programm findet
einen gebrochenen Wikilink immer, ein Modell meistens.

**Also die erste Frage vor jedem neuen Skill:** Was davon ist mechanisch? Das
gehört in ein Werkzeug, und der Skill ruft es auf. Bleibt danach nichts übrig,
braucht es keinen Skill.

## Der Ort

```
skills/<name>/SKILL.md
```

Der Ordnername ist der Skillname und das Slash-Kommando. Es gibt keine zweite
Fassung und keinen Mirror. Skripte, die nur dieser eine Skill braucht, liegen
darunter in `scripts/`. Alles, was ein zweiter gebrauchen könnte, gehört nach
`bin/`.

Das Plugin heißt `hkf`, also erscheint der Skill als `hkf:<name>`.

## Der Name

Der **Ordnername** bestimmt das Kommando. Das Frontmatter-Feld `name` ist laut
Dokumentation nur ein Anzeigename, hier trägt es trotzdem denselben Wert.
Sonst heißt derselbe Skill an zwei Stellen verschieden, und niemand merkt,
welcher gilt. Die Probe in `test/smoke.py` prüft das.

Was eine Wissensbasis nach HKF bedient, trägt das Präfix `hkb-`. Was für jeden
Vault gilt, trägt keins.

## Das Frontmatter

Pflicht sind `name` und `description`. Die `description` entscheidet, ob der
Skill überhaupt greift, und sie wird gelesen, wenn der Skill noch nicht geladen
ist. Sie nennt deshalb beides: **was** er tut und **woran** man erkennt, dass
er gemeint ist. Ein Satz zur Sache, dann `Verwenden bei:` mit den Formulierungen,
die ein Mensch tatsächlich benutzt.

Weitere Felder, alle optional:

| Feld | Wofür |
|---|---|
| `when_to_use` | zusätzlicher Hinweis auf den Auslöser |
| `argument-hint`, `arguments` | erwartete Argumente |
| `disable-model-invocation` | verhindert, dass das Modell den Skill von selbst startet |
| `user-invocable` | Aufruf als Slash-Kommando |
| `allowed-tools`, `disallowed-tools` | Werkzeuggrenzen |
| `model`, `effort` | Modellwahl und Aufwand |
| `context`, `agent`, `background` | Ausführung in einem eigenen Kontext |
| `hooks` | erzwingbare Vor- und Nachbedingungen |
| `paths` | greift nur bei bestimmten Dateien |

**Keines davon wird nebenbei gesetzt.** `allowed-tools` und `hooks` erst nach
ausdrücklicher Prüfung. Bei einem Skill, der veröffentlicht oder schreibt,
`disable-model-invocation` bewusst entscheiden. `context: fork` nur für Arbeit,
die keine Freigabe im Hauptkontext braucht, und `background` nur zusammen
damit.

`model` lohnt sich, wo der Ablauf rein mechanisch ist und keine anspruchsvolle
Sprachleistung verlangt. `bild` läuft deshalb auf einem günstigen Tier.

## Ein Skill ruft einen Agenten

Wo viel gelesen und wenig zurückgegeben wird, gehört die Arbeit in einen
eigenen Kontext. `bild-notiz` sieht kein Bild an, das tut `bild-callout`.

Der Gewinn ist nicht Parallelität, sondern dass der Bestand nicht im
Hauptkontext liegen bleibt. Ein Agent, der zwölf Bilder ansieht und einen Pfad
zurückgibt, kostet einmal. Dieselbe Arbeit im Hauptkontext kostet für den Rest
der Sitzung.

## Was einen Skill übertragbar macht

Ein Skill ohne feste Pfade, Typnamen, Rollen oder Stimmannahmen läuft in jeder
Ablage. Was ablagespezifisch ist, holt er sich zur Laufzeit: die Bereiche über
`hk-ablage`, die Stimme über `hk-kontext --stimme`, das Bildprofil über
`hk-kontext --bild`, die Politik dieser einen Ablage aus ihren `hint`-Notizen.

**Ein Ordnername im Skilltext ist fast immer ein Fehler.** Er gilt für eine
Ablage und bricht in der nächsten. Genau daran ist die alte Fassung dieses
Harness gescheitert.

## Zum Schluss

Nachsehen, dass der Skill unter seinem Namen erscheint, und `python3
test/smoke.py` laufen lassen. Die Proben prüfen, dass jeder Skill im Plugin
ankommt, dass sein `name` zum Ordner passt und dass jeder genannte Agent
existiert.

## Fehlschläge aufschreiben

Ein Skill, der aus mehreren Anläufen entstanden ist, trägt die gescheiterten
Anläufe im Text. Nicht als Chronik, sondern als Warnung: Wer den Skill später
ändert, probiert sonst genau das wieder, was schon einmal nicht funktioniert
hat. Ein Satz je Anlauf, mit dem Grund des Scheiterns.
