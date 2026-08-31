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
## Wo der Rest liegt

Der Harness ist eine **Umsetzung**, nicht die Spezifikation. Was gilt, steht
nebenan; was hier liegt, ist eine Art, es zu tun.

| Repository | Inhalt |
|---|---|
| [`hkf-spec`](https://github.com/arpablo/hkf-spec) | Die Spezifikation: HKF Core 1.0 und HKF Config 1.0 |
| [`hkf-kb-template`](https://github.com/arpablo/hkf-kb-template) | Vorlage für eine neue Wissensbasis; `hk-init` schöpft aus derselben Grundausstattung |
| [`hkf-base`](https://github.com/arpablo/hkf-base) | Stillgelegt — das Vokabular gehört seit Config 1.0 zur Grundausstattung |
| [`hkf-harness`](https://github.com/arpablo/hkf-harness) | Dieses Repository |

## Die Ablage wird nicht geraten

Kein Werkzeug hier kennt einen festen Pfad. Es nimmt, was im Aufruf steht,
sonst `HKB_PATH`, sonst `~/hkb` — und bricht ab, wenn dort keine `hkb.md`
liegt.

```bash
export HKB_PATH=~/wissen
export PATH="$PATH:$(pwd)/bin"

hk-lint
```

Python bringt der Harness selbst mit; `./bootstrap-python.sh` baut die venv,
und jedes Werkzeug startet sich darunter neu. Wer das nicht will, braucht
Python 3 und PyYAML.

## Die Methoden

| | | |
|---|---|---|
| `hk-init <ziel>` | legt eine Wissensbasis an: Grundausstattung, Obsidian-Konfiguration, README, `.gitignore`, `git init` und ein erster Commit | **läuft** |
| `hk-lint [--fix] [--strict]` | prüft eine Wissensbasis **oder eine Lieferung** (§6.3): Frontmatter gegen Anhang B.4, Grammatik gegen Anhang B, dazu die strukturellen Prüfungen; `--fix` führt die elf erlaubten Handgriffe aus | **läuft** |
| `hk-import <bundle>` | übernimmt eine Lieferung (§6.1): Typen abgleichen, Notizen und Mediendateien einsortieren, Verweise umschreiben, verknüpfen, Bundle-Notiz und Typtabelle fortschreiben | **läuft** |
| `hk-export <id> <ziel>` | schreibt eine Lieferung heraus (§6.2): Notizen, Typdefinitionen und Mediendateien der Lieferung in den typbezogenen Baum, Verweise ohne Ablagepfad | **läuft** |

Was geprüft wird, entscheidet die Wurzeldatei: `hkb.md` heißt Wissensbasis,
`hbundle.md` heißt Lieferung. §6.3 gilt für beide, mit den Unterschieden aus §4
und §7.1 — ein Bundle hat keine Typverzeichnisse, seine Notizen liegen, wo sie
wollen, `bundles` und `rejected_links` stehen dort nicht, und geprüft wird
stattdessen, ob es in seinen Typen geschlossen ist und ob zwei Notizen beim
Import dieselbe Notiz-ID ergäben. `--fix` gilt nur für eine Wissensbasis: Eine
Lieferung wird gelesen, nicht geändert.

Gemeldet wird
in drei Gruppen und getrennt nach Schweregrad: `fehler` heißt, die Ablage ist
nicht konform (§7.2); `hinweis` heißt, es fällt auf, macht sie aber nicht
ungültig. Der Rückgabewert ist 1 nur bei Fehlern.

`--fix` darf ausschließlich die elf Handgriffe aus §6.3 — Typtabelle neu
erzeugen, fehlende Standard-Property-Typen anlegen, einen verzeichnislosen
Wikilink qualifizieren (nur bei genau einem Ziel), einen fehlenden Alias aus
dem `title` ergänzen, den Trenner ` / ` ausschreiben, ein `datetime` ohne
Uhrzeit auf den Tagesbeginn bringen, `created` und `modified` ergänzen,
`# Siehe auch` ordnen und ans Ende stellen, `related` daraus ergänzen, leere
Properties entfernen. Danach wird erneut geprüft.

**Was `--fix` nicht tut**, und beides steht so in §6.3: Es ergänzt keinen
Eintrag unter `# Siehe auch` und entfernt keinen — Verknüpfen ist Sache des
Imports (§6.1 Schritt 9), Entfernen Sache eines Menschen (§5.6). Und es legt
keine vorläufige Typdefinition an und entfernt keine: Dazwischen liegt eine
Entscheidung über Bedeutung, und die trifft kein Linter (§5.4).

Geprüft wird dabei auch die **Property-Tabelle jedes Typs gegen die Werte
seiner Notizen**: Pflichtangaben, Wertform, `pattern`, `values`, `min`, `max`,
bei `hkf-link` der Zieltyp und bei `hkf-file` die Medienart — bei Alternativen
genügt eine (§3.7.2). Dazu die Tabelle selbst: ob jeder genannte Typ existiert,
jeder Zieltyp registriert ist, der `:`-Zusatz nur an `hkf-link` und `hkf-file`
steht und alle Alternativen dieselbe Wertform haben.

`--strict` meldet zusätzlich undeklarierte Properties, je Typ und Name
zusammengefasst — `maschine: designed_year in 2 von 2 Notizen`. Wenige Notizen
sind meist ein Versehen; fast alle bedeuten, die Property gehört in die
Property-Tabelle des Typs. Welcher Fall vorliegt, entscheidet ein Mensch.

`hk-import --check` führt den Lauf bis zu dem Punkt aus, an dem geschrieben
würde, und berichtet in drei Abschnitten: was geschieht, was zu entscheiden
ist, was zu tun ist. `--force` entscheidet, welche von zwei Fassungen gilt —
nie, ob zwei Dinge dasselbe meinen.

## Der Rundlauf

Ein Bundle, das importiert und wieder exportiert wird, kommt bis auf zwei
Stellen zurück, wie es kam. Beide sind gewollt:

- **Verweise, die der Import erkannt hat, bleiben.** Nennen sich zwei Notizen
  derselben Lieferung gegenseitig, steht das danach unter `# Siehe auch` und
  geht mit hinaus. Was in den Bestand zeigt, fällt weg — es gilt nur hier
  (§6.2 Schritt 7).
- **Mediendateien folgen den Verweisen.** Der Import nimmt jede Datei der
  Lieferung mit, der Export nur die, auf die eine Notiz zeigt (§6.2 Schritt 4).
  Was zurückbleibt, meldet `hk-export`, damit es nicht still verschwindet.

Die abgeleitete Typtabelle in `hbundle.md` wird alphabetisch geschrieben; §3.1
legt keine Reihenfolge fest.

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
lib/hkf/     ablage, frontmatter, schema, grammatik, pruefen, korrigieren,
             importieren, exportieren, notiz, vorlage, fassung
bin/         hk-init, hk-lint, hk-import, hk-export
py           das Python des Harness — baut die venv und startet sie
tools/       spec.py hält die Kopie unter spec/ auf Stand,
             grundausstattung.py die Vorlage gegen Anhang A und §3.5.1
templates/   die Grundausstattung, aus der hk-init schöpft
skills/      die KI-Schicht: hkb und fünf Operationen, siehe skills/README.md
test/        Rauchprobe: python3 test/smoke.py
```

**Die Spezifikation liegt als Kopie unter `spec/`, nicht als Submodul.** Ein
Harness setzt genau eine Fassung um; welche, muss aus seiner Auslieferung
hervorgehen und nicht aus dem Zustand eines fremden Repositorys. Die Nummer
steht in `lib/hkf/__init__.py` und nirgends sonst.

Die Spezifikation selbst wird in [`hkf-spec`](https://github.com/arpablo/hkf-spec)
fortgeschrieben, das Inventar daneben in `HKF-Config-V1.0.md`.

## Kein Werkzeug legt eine Anleitung daneben

`hk-init` schrieb einmal eine `AGENTS.md` neben die Wurzeldatei: sieben
Regeln und die Typtabelle. Beides gibt es jetzt besser. Die Regeln stehen in
den Skills unter `skills/` — einmal, versioniert, geprüft —, die Typtabelle
steht in `hkb.md`, wo sie hingehört. Eine erzeugte Kopie daneben veraltete für
sich und sagte nichts, was nicht schon dastand. Eine `CLAUDE.md` entsteht
ebenfalls nicht; sie nannte ein Produkt.

Die Hinweise, die einmal in ihrem letzten Abschnitt standen, haben einen
besseren Ort bekommen: HKF Config führt den Typ `hint`. Jede Festlegung, wie
diese Wissensbasis geführt wird, ist dort eine Notiz unter `Hints/` — geprüft,
verlinkt, versioniert, und mit `applies_to` an der Typdefinition, für die sie
gilt. Wer daneben trotzdem eine `AGENTS.md` will, legt sie von Hand an; kein
Werkzeug fasst sie an.

Core führte dafür einmal einen Abschnitt „Einstieg für Werkzeuge"; er ist
gestrichen. Den ersten Satz sagt der Harness, nicht die Ablage.

## Der Harness bringt sein eigenes Python mit

Auf einer Maschine liegen leicht zwei Interpreter nebeneinander — hier
`/opt/homebrew/bin/python3` und `/usr/bin/python3`, mit zwei PyYAML-Fassungen.
Welcher zuerst im PATH steht, ist Zufall und darf nicht entscheiden, was eine
Prüfung findet. Der Harness baut sich darum eine eigene Umgebung:

```
./bootstrap-python.sh     baut die venv, wenn sie fehlt oder veraltet ist
./py bin/hk-lint          dasselbe wie bin/hk-lint, nur ausdrücklich
./py -c "import yaml; …"  ein Einzeiler in derselben Umgebung
```

Festgenagelt ist beides: die Interpreterfassung in
[`.python-version`](.python-version), die eine Abhängigkeit in
[`requirements.txt`](requirements.txt). Gebaut wird mit `uv`, gelagert unter
`~/.cache/hkf-harness/venv` — nicht im Repository, damit ein Klon nichts
mitschleppt. `HKF_VENV` verlegt den Ort.

**Die `bin/hk-*` brauchen den Shim nicht.** Beim Import von `hkf` startet sich
der Prozess unter dem Python des Harness neu, wenn er nicht schon darunter
läuft; `hk-lint` bleibt `hk-lint`. Fehlt die venv, läuft alles wie zuvor
weiter — dann sagt der Frontmatter-Leser, wenn PyYAML fehlt, und nennt den
Bootstrap. Ein `python -c` wird nicht umgeleitet: Dort steht in `argv[0]` kein
Skript, und ein Neustart verlöre den Code.

## Die KI-Schicht

Unter [`skills/`](skills/) liegen sechs Skills, die ein Sprachmodell durch die
Methoden führen. [`hkb`](skills/hkb/SKILL.md) ist die Grundlage, die übrigen
setzen ihn voraus: [`hkb-notiz`](skills/hkb-notiz/SKILL.md),
[`hkb-typ`](skills/hkb-typ/SKILL.md),
[`hkb-import`](skills/hkb-import/SKILL.md),
[`hkb-export`](skills/hkb-export/SKILL.md),
[`hkb-lint`](skills/hkb-lint/SKILL.md).

Sie fügen nichts hinzu, was die Werkzeuge nicht können — sie tun genau das,
was ein Programm nicht darf. Am deutlichsten bei `hkb-import`: `hk-import`
legt eine Bedeutungsprüfung vor und weist ab, der Skill urteilt und trägt das
Urteil als Zeile in `# Entscheidungen` der Bundle-Notiz ein (§5.7). Ohne
diesen Eintrag stellt der nächste Lauf dieselbe Frage neu.

## Welche Fassung gilt

`CORE` in [`lib/hkf/__init__.py`](lib/hkf/__init__.py) nennt die Fassung, die
dieser Harness umsetzt; unter `spec/` liegt sie im Wortlaut. Beides gehört
zusammen, und beides veraltet, sobald die Spezifikation fortgeschrieben wird.

```
python3 tools/spec.py            berichtet, ob die Kopie noch stimmt
python3 tools/spec.py --update   holt den Stand des Spec-Repositorys
```

Der Kopf des Berichts nennt beides, woran ein Harness hängt — die Fassung, die
er umsetzt, und den Interpreter, unter dem er läuft:

```
Quelle:  …/HenniHKF-Spec (Core 1.0)
Harness: Core 1.0, Python 3.12.13 aus ~/.cache/hkf-harness/venv
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

## Die Grundausstattung gegen die Spezifikation

Die Kern-Typen stehen zweimal: als Markdown-Block in Anhang A und als
ausgelieferte Datei unter `templates/hkb/Typedefs/`. Die dreizehn
Standard-Property-Typen ebenso — dort als Tabelle in §3.5.1.

```
python3 tools/grundausstattung.py
```

Seit das Vokabular zur Grundausstattung gehört, ist dies die einzige Gegenprobe. Für
Core fehlte es, und genau deshalb konnte `bundle` die Property `version` als
Pflicht führen, obwohl §4.1 eine Lieferung ohne Fassung ausdrücklich zulässt.
Gefunden hat das erst die Prüfung der Property-Tabellen gegen die Werte — an
einer Bundle-Notiz, die in Ordnung war. Die Rauchprobe ruft es jetzt mit auf.

## Woher `templates/hkb` kommt

Die Grundausstattung wird nicht hier gepflegt, sondern aus der
Beispiel-Wissensbasis der Werkbank abgeleitet — alle Notizen in `Typedefs/`
und `Proptypes/`, die keine `bundles`-Property tragen (§5.3):

```
cd ../HenniHKF-Lab
python3 tools/make-hkb-template.py ../HenniHKF-Harness/templates/hkb --nackt --force
```

Umgekehrt prüft und erzeugt die Werkbank mit dieser Bibliothek, statt eigene
Kopien zu führen. Sie findet den Harness über `HKF_HARNESS`, sonst nebenan.

## Offen

- **Vorschläge aus unbelegten Properties** (§6.1 Schritt 9, dritte
  Beobachtung).
- **`HKF_BUNDLE_PATH`** — Vorgabeverzeichnis für Lieferungen; festlegen, wenn
  eine Lieferung öfter am selben Ort landet.
