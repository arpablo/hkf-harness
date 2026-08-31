---
type: specification
title: HKF Harness V1.0 — Werkzeuge für eine Wissensbasis
description: Die Festlegungen, die vor den Werkzeugen kommen — wo die Ablage liegt, was im Harness liegt und was nicht, und wer die Kurationspolitik führt.
status: draft
---

# HKF Harness V1.0

Das Repository, das eine Wissensbasis nach **HKF Core 1.0** bedienbar macht:
die Werkzeuge, dazu die Fassung der Spezifikation, die sie umsetzen, und
obenauf eine dünne Schicht für Sprachmodelle. Es steht auf GitHub und ist von
jeder Wissensbasis getrennt, die es bedient.

Der Satz, aus dem alles Übrige folgt:

> Eine HKB ist ein gewöhnlicher Obsidian-Vault. Sie lässt sich ohne KI
> benutzen und füllen.

## Drei Teile, zwei Proben

| | Was es ist | Wo |
|---|---|---|
| **HKF** | die Spezifikation: wie ein Bundle und eine konforme HKB aufgebaut sind. Sonst nichts. | `hkf-spec` |
| **Harness** | Werkzeuge und die Spezifikation, die sie umsetzen | `hkf-harness` |
| **Wissensbasis** | Inhalt | ein Vault, irgendwo |

- **Nimm den Harness weg.** Die Wissensbasis bleibt ein Obsidian-Vault, den
  ein Mensch liest, füllt und verlinkt. Es fehlt die Prüfung, sonst nichts.
- **Nimm die Wissensbasis weg.** Der Harness bleibt ein Werkzeugkasten, der
  jede andere HKB bedient.

Was eine der beiden Proben nicht besteht, liegt am falschen Ort.

## 1. Was im Harness liegt

```
hkf-harness/
  HKF-Harness-V1.0.md   dieses Dokument
  spec/                 die Fassung von HKF Core und Base, die er umsetzt
  bin/                  hk-init, hk-lint, hk-import, hk-export
  lib/hkf/              Ablage, Frontmatter, Schema, Grammatik, Vorlage, Fassung
  py                    das Python des Harness
  tools/                spec.py — hält die Kopie unter spec/ auf Stand
  templates/            die Grundausstattung für hk-init
  skills/               die KI-Schicht: hkb und fünf Operationen
  test/                 die Rauchprobe
```

**Die Spezifikation liegt als Kopie im Harness, nicht als Submodul.** Ein
Harness setzt genau eine Fassung um; welche, muss aus seiner Auslieferung
hervorgehen und nicht aus dem Zustand eines fremden Repositorys. Die Kopie
trägt die Nummer, gegen die `hk-lint` prüft, und `tools/spec.py` hält sie
gleich mit dem Spec-Repository.

**Der Harness bringt sein eigenes Python mit.** Er nimmt nicht, was im PATH
steht: Zwei Interpreter mit zwei Fassungen derselben Bibliothek liegen auf
einer Maschine schnell nebeneinander, und dann hinge das Ergebnis einer
Prüfung daran, welcher zuerst gefunden wurde. Interpreterfassung und
Abhängigkeiten sind festgenagelt, die Umgebung liegt außerhalb des
Repositoriums, und die Werkzeuge finden sie von selbst. Das ist dieselbe
Trennung wie bei `HKB_PATH`, nur nach unten: Was der Harness zum Laufen
braucht, gehört ihm und nicht der Maschine.

**Dieses Dokument liegt nicht unter `spec/`.** Dort steht allein, was aus
`hkf-spec` kommt; `tools/spec.py --update` räumt dort auf, was die Quelle
nicht mehr führt. Die Harness-Spezifikation gehört dem Harness und steht
darum in seiner Wurzel, neben der `README.md` — die sagt, wie man ihn
benutzt, dieses Dokument sagt, was er ist.

## 2. Die KI-Schicht liegt obenauf und kann nichts allein

**Kein Skill tut etwas, das kein Script tut.** Ein Skill wählt aus, erklärt,
fragt zurück und urteilt dort, wo die Spezifikation ein Urteil verlangt — die
Bedeutungsprüfung (§5.5), die Identität einer ankommenden Notiz (§6.1), die
Verknüpfung (§5.6). Alles Mechanische gehört ins Script.

Der Grund ist der Satz oben. Sobald eine Operation nur über ein Modell
erreichbar ist, stimmt „geht auch ohne KI" nicht mehr. Dazu kommt die
Verlässlichkeit: Ein Programm findet einen gebrochenen Wikilink immer, ein
Modell meistens.

Daraus folgt die Reihenfolge beim Bauen: erst `bin/`, dann `skills/`.

## 3. Die Wissensbasis wird über eine Umgebungsvariable gefunden

Vorbild ist der Skill
[`llm-wiki`](file:///Users/arminpfarr/.hermes/skills/research/llm-wiki/SKILL.md),
der keinen Pfad nennt, sondern eine Variable:

```bash
HKB="${HKB_PATH:-$HOME/hkb}"
```

| | |
|---|---|
| Variable | `HKB_PATH` |
| Vorgabe | `~/hkb`, wenn nicht gesetzt |
| Ort der Definition | Umgebung des Aufrufers, `~/.claude/settings.json` unter `env`, oder eine `.env` |
| Prüfung | `$HKB/hkb.md` lesen und die Property `hkf` prüfen. Fehlt die Datei, ist der Pfad keine Ablage — abbrechen, nicht raten. |

- **Kein Werkzeug schreibt einen Pfad fest.** Nicht in Beispielen, nicht in
  Prüfroutinen.
- **Das Arbeitsverzeichnis ist nicht die Ablage.** Wer `.` annimmt, schreibt
  irgendwann in ein fremdes Verzeichnis.
- **Mehrere Wissensbasen sind der Normalfall.** Die Reihenfolge ist:
  Argument auf der Kommandozeile → `HKB_PATH` → Vorgabe.

## 4. Keine Werkzeugdatei liegt in der Wissensbasis

`HenniHKF-Core` führte einmal `AGENTS.md` und `CLAUDE.md`. Beide gehören dem
Werkzeug, nicht der Ablage, und beide gehen denselben Weg.

`CLAUDE.md` ist der klarere Fall: ein Satz, der auf `AGENTS.md` zeigt, benannt
nach genau einem Produkt. Die Spezifikation kennt die Datei nicht — kein
Vorkommen in Core, kein Wort in §7.2 —, aber `make-hkb-template.py` kopiert
sie in jede neu erzeugte Wissensbasis.

`AGENTS.md` war der schwierigere Fall, weil Core sie in einem eigenen
Abschnitt „Einstieg für Werkzeuge" empfahl. **Der Abschnitt ist gestrichen**,
und die nachfolgenden Nummern sind nachgerückt: aus §5.5 bis §5.8 wurde §5.4
bis §5.7.

Die Spezifikation sagte dort schon fast alles selbst: Die Datei „ist keine
Notiz und gehört nicht zur Ablage", sie wird „weder geprüft noch
ausgeliefert", ihr Inhalt ist „zum größten Teil abgeleitet". Zuerst zog der
Harness daraus den Schluss, sie ins Arbeitsverzeichnis zu erzeugen und über
die `.gitignore` draußen zu halten.

**Auch das ist gestrichen.** Der Grund liegt in der KI-Schicht: Seit die
Skills unter `skills/` liegen, stehen die sieben Regeln dort — einmal, beim
Werkzeug, versioniert und geprüft. Eine erzeugte Kopie daneben sagte
dasselbe noch einmal, veraltete für sich und trug an eigenem Inhalt nur die
Typtabelle, die ohnehin in `hkb.md` steht. Was ein Modell wissen muss, bringt
es mit; was diese eine Wissensbasis auszeichnet, steht in ihr.

Der Einwand, den der gestrichene Core-Abschnitt vorbrachte, war: „Ein Modell,
das einen Vault öffnet, sieht zunächst nur Markdown-Dateien." Das stimmt —
aber ein Modell öffnet keinen Vault allein. Es kommt mit einem Harness, und
der bringt die Spezifikation mit. Wer ohne Harness kommt, findet den Einstieg
im Format selbst: `hkb.md` trägt `spec` mit der URL.

Wer für **seine** Wissensbasis etwas aufschreiben will, legt eine `AGENTS.md`
von Hand an. Sie gehört dann ihm, nicht dem Werkzeug, und wird versioniert wie
jede andere Datei — kein Werkzeug überschreibt sie, keine `.gitignore` hält
sie zurück.

Aus demselben Grund ist **§7.2 Punkt 9 entfallen**. Dort hing die Konformität
einer HKB daran, dass `hk-import`, `hk-export` und `hk-lint` „verfügbar sind"
— eine Eigenschaft der Umgebung, nicht der Ablage. Eine HKB in einem
Zip-Archiv hat keine Werkzeuge und ist trotzdem korrekt aufgebaut.

Was daraus folgt:

- `CLAUDE.md` und `AGENTS.md` aus `HenniHKF-Core` entfernen.
- Die Kopierzeile für `CLAUDE.md` und die Erzeugung von `AGENTS.md` aus
  `make-hkb-template.py` und aus `hk-init` herausnehmen; `templates/AGENTS.md`
  entfällt.
- Den Abschnitt „Einstieg für Werkzeuge" in `HenniHKF-Lab/README.md`
  nachziehen; er beschreibt beide Dateien noch als Teil der Beispiel-HKB.

## 5. Jede Wissensbasis ist ein Git-Repository

Eine Wissensbasis ohne Geschichte ist ein Verzeichnis, in dem gearbeitet wird,
ohne dass jemand nachsehen kann. `hk-init` legt deshalb nicht nur die
Grundausstattung an, sondern auch das Repository:

1. `git init`
2. `.gitignore` schreiben
3. alles hinzufügen, ein erster Commit: `hkb: Grundausstattung`

`make-hkb-template.py` schreibt die `.gitignore` heute schon, ruft aber kein
`git init` auf. Das ist die Lücke.

```gitignore
# Sitzungsprotokolle und Suchindex der Werkzeugumgebung
.memsearch/

# persönliches Fensterlayout von Obsidian
.obsidian/workspace.json

# macOS
.DS_Store
```

Der Rest von `.obsidian/` **bleibt versioniert**: Wikilinks, vollständige
Pfade, die registrierten Property-Typen. Das ist Teil des Formats, nicht
Geschmack — ein Vault ohne diese Konfiguration zeigt Datum, Zahl und Liste
falsch an. Es ist zugleich der Grund, warum die Trennung nicht am Wort
„Obsidian" verläuft: Die Vault-Konfiguration gehört der Ablage, die Anleitung
für Modelle dem Werkzeug.

Für die Werkzeuge gilt: **Commit nach jedem abgeschlossenen Vorgang**, nicht
nach jeder Datei — ein Import ist ein Commit, ein `hk-lint --fix` ist ein
Commit. **Nie blind `git add -A`.** **Kein Push ohne Auftrag.**

## 6. Obsidian ohne Bildschirm

Läuft der Harness auf einer Maschine ohne Oberfläche — Server, Cron, Agent im
Hintergrund —, gibt es keine Obsidian-App, die den Vault abgleicht.
`obsidian-headless` erledigt das über Obsidian Sync ohne GUI.

```bash
# Node.js 22+
npm install -g obsidian-headless

ob login --email <adresse> --password '<passwort>'
ob sync-create-remote --name "Meine Wissensbasis"

cd "$HKB_PATH"
ob sync-setup --vault "<vault-id>"
ob sync
```

Dauerhaft mit `ob sync --continuous`, unter systemd oder als LaunchAgent, mit
dem Arbeitsverzeichnis auf `$HKB_PATH`.

Das ist **Zubehör, keine Voraussetzung**: Es betrifft die Maschine, auf der
der Harness läuft, nicht das Format. Zwei Dinge dabei — `.git/` gehört nicht
in den Sync, und vor einem größeren Schreibvorgang einmal `ob sync`, danach
noch einmal, sonst entstehen Konflikte, die niemand gesehen hat.

## 7. Die Kurationspolitik ist Inhalt

Ken Moriwakis minimales LLM-Wiki
([Medium, 24. Mai 2026](https://medium.com/@ken.moriwaki/building-a-minimal-llm-wiki-19a2fb0e9ac7))
führt eine `schema.md` — die Datei, die das Modell liest, bevor es schreibt.
Sie erfüllt vier Aufgaben auf einmal:

| Was in `schema.md` steht | Wo es in HKF steht |
|---|---|
| Gegenstand der Wissensbasis | `name` in `hkb.md` |
| „Concept pages live in `wiki/concepts/`" | der Abschnitt `# Typen` in `hkb.md`, normativ die `typedefs/` |
| Frontmatter-Block, Tag-Taxonomie | Property-Tabelle des Typs, `proptypes/`, Anhang B.4 |
| Konventionen für Verweise und Zeitangaben | die Spezifikation |
| **wann eine Notiz entsteht, was bei Widerspruch geschieht** | **nirgends** |

Die ersten vier stehen in HKF als Tabellen da und nicht als Fließtext, also
prüft `hk-lint` sie. Moriwakis Prototyp muss dafür ein Modell ein Audit
schreiben lassen — und der Artikel hält selbst fest, dass dieses Audit
Widersprüche übersehen, übertreiben oder erfinden kann. Genau der Unterschied,
der in §2 die Reihenfolge bestimmt.

Die letzte Zeile ist die Lücke, und sie gehört nicht in die Spezifikation:
Core beschreibt das Format, nicht den Gebrauch.

Sie gehört aber auch nicht in den Harness. Wann in **dieser** Wissensbasis
etwas eine eigene Notiz wert ist, welche Quellen als belastbar gelten, wie
weit zusammengefasst werden darf — das gehört zu dieser einen Wissensbasis und
zieht mit ihr um. Der Vorschlag: **eine gewöhnliche Notiz in der Ablage**,
Typ `specification` aus HKF Base. Sie ist dann Inhalt wie jeder andere —
versioniert, verlinkbar, prüfbar — und sie besteht die erste Probe: Ein
Mensch, der die Wissensbasis ohne KI führt, hat denselben Nutzen davon.

Der Harness liest sie, wenn es sie gibt. Was er selbst mitbringt, ist die
Politik, die für **jede** HKB gilt: der Ablauf eines Ingests, wann committet
wird, wann zurückgefragt statt entschieden wird, und das Verbot der glatten
Zusammenfassung. Moriwaki nennt das Risiko `over-synthesis` und hält es für
gefährlicher als Halluzination — ein Modell macht aus Uneinigkeit einen
Konsens, und eine saubere Notiz strahlt Autorität aus, die ihr Inhalt nicht
deckt.

## Offen

- **Name und Ort des Repositorys** — `hkf-harness` neben `hkf-spec` und
  `hkf-base`, und was aus `HenniHKF-Lab` wird.
- **`HKF_BUNDLE_PATH`** — Vorgabeverzeichnis für `hk-export` und `hk-import`;
  festlegen, wenn `hk-export` steht.
