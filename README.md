# HKF Harness

Die Werkzeuge zu einer Wissensbasis nach **HKF Core 1.0** — anlegen, prüfen,
importieren, exportieren —, dazu die Fassung der Spezifikation, die sie
umsetzen.

Der Satz, aus dem der Zuschnitt folgt:

> Eine HKB ist ein gewöhnlicher Obsidian-Vault. Sie lässt sich ohne KI
> benutzen und füllen.

Deshalb liegt hier nichts, was in eine Wissensbasis gehört, und in keiner
Wissensbasis liegt etwas, was hierher gehört. Zwei Proben:

- **Nimm den Harness weg.** Die Wissensbasis bleibt ein Obsidian-Vault, den
  ein Mensch liest, füllt und verlinkt. Es fehlt die Prüfung, sonst nichts.
- **Nimm die Wissensbasis weg.** Der Harness bleibt ein Werkzeugkasten, der
  jede andere HKB bedient.

## Die Ablage wird nicht geraten

Kein Werkzeug hier kennt einen festen Pfad. Es nimmt, was im Aufruf steht,
sonst `HKB_PATH`, sonst `~/hkb` — und bricht ab, wenn dort keine `hkb.md`
liegt.

```bash
export HKB_PATH=~/wissen
export PATH="$PATH:$(pwd)/bin"

hk-lint
```

Gebraucht werden Python 3 und PyYAML (`pip3 install pyyaml`).

## Die Methoden

| | | |
|---|---|---|
| `hk-init <ziel>` | legt eine Wissensbasis an: Grundausstattung, Obsidian-Konfiguration, README, `.gitignore`, `git init` und ein erster Commit | **läuft** |
| `hk-lint [pfad]` | prüft Frontmatter gegen das Schema aus Anhang B.4 und die Grammatik der Wikilinks und Typangaben aus Anhang B | **teilweise** |
| `hk-import <bundle>` | übernimmt eine Lieferung (§6.1) | Platzhalter |
| `hk-export <id> <ziel>` | schreibt eine Lieferung heraus (§6.2) | Platzhalter |

`hk-lint --help` nennt, welche Prüfungen aus §6.3 noch fehlen. Die beiden
Platzhalter sagen beim Aufruf, was sie tun sollen, und enden mit 3.

## Was wo liegt

```
spec/        die Fassung, die dieser Harness umsetzt
lib/hkf/     ablage, frontmatter, schema, grammatik
bin/         hk-init, hk-lint, hk-import, hk-export
templates/   AGENTS.md und die Grundausstattung, aus der hk-init schöpft
skills/      die KI-Schicht — noch leer, siehe skills/README.md
test/        Rauchprobe: python3 test/smoke.py
```

**Die Spezifikation liegt als Kopie unter `spec/`, nicht als Submodul.** Ein
Harness setzt genau eine Fassung um; welche, muss aus seiner Auslieferung
hervorgehen und nicht aus dem Zustand eines fremden Repositorys. Die Nummer
steht in `lib/hkf/__init__.py` und nirgends sonst.

Die Spezifikation selbst wird in [`hkf-spec`](https://github.com/arpablo/hkf-spec)
fortgeschrieben, das Vokabular als Bundle in [`hkf-base`](https://github.com/arpablo/hkf-base).

## AGENTS.md gehört dem Werkzeug

`hk-init` schreibt eine `AGENTS.md` neben die Wurzeldatei — die wenigen
Regeln, deren Verletzung Schaden anrichtet, dazu die Typtabelle aus `hkb.md`.
Sie steht aber in der `.gitignore` der erzeugten Wissensbasis: Sie ist keine
Notiz, sie wird weder geprüft noch ausgeliefert, und ihr Inhalt ist bis auf
den Abschnitt `# Hinweise` abgeleitet. Eine `CLAUDE.md` entsteht gar nicht
mehr — sie nannte ein Produkt.

Core führte dafür einmal einen Abschnitt „Einstieg für Werkzeuge"; er ist
gestrichen. Den ersten Satz sagt der Harness, nicht die Ablage.

## Offen

- **Doppelte Werkzeuge.** `check-frontmatter.py` und `check-grammar.py` in
  `HenniHKF-Lab/tools/` sind die Vorlagen für `lib/hkf/schema.py` und
  `lib/hkf/grammatik.py`. Solange beide bestehen, laufen sie auseinander. Das
  Lab sollte den Harness aufrufen, statt eigene Kopien zu führen.
- **`hk-import` und `hk-export`** — der mechanische Teil zuerst.
- **`HKF_BUNDLE_PATH`** — Vorgabeverzeichnis für Lieferungen; festlegen, wenn
  `hk-export` steht.
- **`hk-lint --fix`** — die abgeleiteten Tabellen in `hkb.md` und die
  `AGENTS.md` neu erzeugen.
