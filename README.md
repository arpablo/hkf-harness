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


Was ein Harness ist und wo die Grenze zur Wissensbasis verläuft, steht in
[`HKF-Harness-V1.0.md`](HKF-Harness-V1.0.md). Diese Datei sagt, wie man ihn
benutzt; jene sagt, was er ist.
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
| `hk-import <bundle>` | übernimmt eine Lieferung (§6.1): Typen abgleichen, Notizen und Mediendateien einsortieren, Verweise umschreiben, verknüpfen, Bundle-Notiz und Typtabelle fortschreiben | **läuft** |
| `hk-export <id> <ziel>` | schreibt eine Lieferung heraus (§6.2) | Platzhalter |

`hk-lint --help` nennt, welche Prüfungen aus §6.3 noch fehlen. `hk-export`
sagt beim Aufruf, was es tun soll, und endet mit 3.

`hk-import --check` führt den Lauf bis zu dem Punkt aus, an dem geschrieben
würde, und berichtet in drei Abschnitten: was geschieht, was zu entscheiden
ist, was zu tun ist. `--force` entscheidet, welche von zwei Fassungen gilt —
nie, ob zwei Dinge dasselbe meinen.

## Was der Import nicht entscheidet

Drei Stellen der Spezifikation enden mit einem Urteil, und keines davon fällt
ein Programm: die Bedeutungsprüfung zweier gleichnamiger Typen (§5.5), die
Identität einer ankommenden Notiz, die es unter demselben Namen schon gibt
(§6.1 Schritt 5), und alles an der Verknüpfung, was über die mechanischen
Beobachtungen hinausgeht (§5.6).

`hk-import` legt diese Fälle vor und **schreibt nichts**, solange eine
Bedeutungsprüfung offen ist. Eine offene Identitätsfrage lässt nur die eine
Notiz liegen; die übrigen laufen durch. Ist die Frage einmal beantwortet und
als Zeile in `# Entscheidungen` der Bundle-Notiz festgehalten (§5.7), fragt
der nächste Lauf nicht wieder — das Aufzeichnen selbst ist Sache dessen, der
geurteilt hat, also eines Menschen oder eines Skills.

Selbsttätig verknüpft wird nur die erste der drei Beobachtungen aus §6.1
Schritt 9: Nennt der Body einer Notiz den Titel oder einen Alias einer anderen
wörtlich und verlinkt ihn nicht ohnehin schon, entsteht ein Eintrag unter
`# Siehe auch`. Gleiche `hkf-wikidata`-Kennungen werden als
Zusammenführungskandidat vorgelegt; unbelegte Properties mit Zieltyp noch
nicht.

## Was wo liegt

```
spec/        die Fassung, die dieser Harness umsetzt
lib/hkf/     ablage, frontmatter, schema, grammatik, vorlage, fassung
bin/         hk-init, hk-lint, hk-import, hk-export
tools/       spec.py — hält die Kopie unter spec/ auf Stand
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

## Welche Fassung gilt

`CORE` in [`lib/hkf/__init__.py`](lib/hkf/__init__.py) nennt die Fassung, die
dieser Harness umsetzt; unter `spec/` liegt sie im Wortlaut. Beides gehört
zusammen, und beides veraltet, sobald die Spezifikation fortgeschrieben wird.

```
python3 tools/spec.py            berichtet, ob die Kopie noch stimmt
python3 tools/spec.py --update   holt den Stand des Spec-Repositorys
```

Das Skript findet die Quelle über `HKF_SPEC`, sonst neben diesem Repository;
ohne Quelle endet es mit 0 und sagt es, damit ein Klon sich nicht daran stört.
Kommt eine neue Fassung, nennt es sie und fordert, `CORE` nachzuziehen. Die
Rauchprobe ruft es mit auf: Ein Rückstand fällt beim nächsten Testlauf auf,
nicht erst beim nächsten Import.

**Was der Harness liest** (§8): jede Fassung mit derselben Major-Nummer, deren
Minor nicht größer ist als die eigene. Minor-Fassungen ergänzen Regeln, ohne
Bestehendes ungültig zu machen — was Core 1.0 schrieb, versteht ein Harness
1.2. Umgekehrt gilt es nicht, und §8 sagt, was dann geschieht: Die Dateien
sind lesbar, übernommen wird nichts. `hk-import` weist eine solche Lieferung
ab, `hk-lint` meldet eine Ablage, die neuer ist als er selbst.

## Woher `templates/hkb` kommt

Die Grundausstattung wird nicht hier gepflegt, sondern aus der
Beispiel-Wissensbasis der Werkbank abgeleitet — alle Notizen in `typedefs/`
und `proptypes/`, die keine `bundles`-Property tragen (§5.3):

```
cd ../HenniHKF-Lab
python3 tools/make-hkb-template.py ../HenniHKF-Harness/templates/hkb --nackt --force
```

Umgekehrt prüft und erzeugt die Werkbank mit dieser Bibliothek, statt eigene
Kopien zu führen. Sie findet den Harness über `HKF_HARNESS`, sonst nebenan.

## Offen

- **`hk-export`** — die Umkehrung: Ablagepfad aus jedem Verweis
  herausrechnen, `bundles`, `imported` und die Nachweise draußen lassen,
  Mediendateien nach ihrer Endung mitnehmen (§4.3, §6.2).
- **Vorschläge aus unbelegten Properties** (§6.1 Schritt 9, dritte
  Beobachtung).
- **`HKF_BUNDLE_PATH`** — Vorgabeverzeichnis für Lieferungen; festlegen, wenn
  `hk-export` steht.
- **`hk-lint --fix`** — die abgeleiteten Tabellen in `hkb.md` und die
  `AGENTS.md` neu erzeugen.
