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

Der Harness ist eine **Umsetzung**, und er führt die Spezifikation mit, die er
umsetzt. Sie liegt unter [`spec/`](spec/) und gilt; alles daneben ist eine Art,
sie zu tun.

| Repository | Inhalt |
|---|---|
| [`hkf-kb-template`](https://github.com/arpablo/hkf-kb-template) | Vorlage für eine neue Wissensbasis; `hk-init` schöpft aus derselben Grundausstattung |
| [`hkf-base`](https://github.com/arpablo/hkf-base) | Stillgelegt — das Vokabular gehört seit Config 1.0 zur Grundausstattung |
| [`hkf-spec`](https://github.com/arpablo/hkf-spec) | Stillgelegt — die Spezifikation steht seit dem 07.09.2026 unter [`spec/`](spec/) |
| [`hkf-harness`](https://github.com/arpablo/hkf-harness) | Dieses Repository |

## Die Ablage wird nicht geraten

Kein Werkzeug hier kennt einen festen Pfad. Es fragt in fünf Stufen und bricht
ab, wenn am Ende keine Wurzeldatei liegt.

| Stufe | Woher |
|---|---|
| 1 | der Aufruf, als letztes Argument |
| 2 | `HKB_PATH` aus der Umgebung |
| 3 | die gemerkte Wahl, siehe `hk-ablage` |
| 4 | eine Aufwärtssuche ab dem Arbeitsverzeichnis |
| 5 | die Vorgabe `~/hkb` |

Jede Fehlermeldung nennt die Stufe, aus der ihr Pfad stammt. Stufe 4 deckt den
Fall ab, dass eine Sitzung in einer Ablage startet, dann ist nichts zu wählen.
Liegen mehrere Ablagen nebeneinander, greift Stufe 3.

```bash
export PATH="$PATH:$(pwd)/bin"

hk-ablage --liste          # was zur Wahl steht
hk-ablage ~/wissen         # gemerkt für dieses Arbeitsverzeichnis
hk-lint                    # nimmt sie ohne Argument
```

Gemerkt wird auf der Platte, unter `~/.cache/hkf-harness/ablagen.json`, und
geschlüsselt nach Arbeitsverzeichnis. Der Grund ist eine Eigenheit der
Werkzeugumgebung: Ein `export HKB_PATH` in einem Aufruf überlebt den Aufruf
nicht. Zwischen zwei Aufrufen bleibt das Arbeitsverzeichnis, sonst nichts.
Zwei Sitzungen an verschiedenen Ablagen stellen sich so nicht gegenseitig um.

Die Wurzeldatei sagt auch, womit man es zu tun hat. `hkb.md` heißt
Wissensbasis, `hbundle.md` heißt Lieferung, und `vault.md` heißt: ein
gewöhnlicher Obsidian-Vault, für den die Schreibregeln und die Suche gelten,
aber keine Operation, die Typen und qualifizierte Verweise voraussetzt.

Python bringt der Harness selbst mit; `./bootstrap-python.sh` baut die venv,
und jedes Werkzeug startet sich darunter neu. Wer das nicht will, braucht
Python 3 und PyYAML.

## Die Methoden

| | | |
|---|---|---|
| `hk-init <ziel>` | legt eine Wissensbasis an: Grundausstattung, Obsidian-Konfiguration, README, `.gitignore`, `git init` und ein erster Commit | **läuft** |
| `hk-lint [--fix] [--strict]` | prüft eine Wissensbasis **oder eine Lieferung** (§6.3): Frontmatter gegen Anhang B.4, Grammatik gegen Anhang B, dazu die strukturellen Prüfungen; `--fix` führt die zwölf erlaubten Handgriffe aus | **läuft** |
| `hk-import <bundle>` | übernimmt eine Lieferung (§6.1): Typen abgleichen, Notizen und Mediendateien einsortieren, Verweise umschreiben, verknüpfen, Bundle-Notiz und Typtabelle fortschreiben | **läuft** |
| `hk-export <id> <ziel>` | schreibt eine Lieferung heraus (§6.2): Notizen, Typdefinitionen und Mediendateien der Lieferung in den typbezogenen Baum, Verweise ohne Ablagepfad | **läuft** |
| `hk-ingest [<stück>]` | liest eine Quelle ein: Typ feststellen, Ausfertigung ablegen oder verzeichnen, `sha256` bilden, Quellennotiz und `hbundle.md` schreiben, die Lücken melden. Mit `--hkb` gleich importieren | **läuft** |
| `hk-tranchen <quellennotiz>` | führt die Tranchen einer großen Quelle im Abschnitt `# Tranchen` der Quellennotiz: `--anlegen` legt die Liste an, `--naechste` sagt, welche dran ist, `--abhaken` schreibt eine fest | **läuft** |
| `hk-types [--umstellen]` | legt Typseiten und Bases an, damit `type` ein Verweis sein darf (§3.3) | **läuft** |
| `hk-ablage [<pfad>]` | sagt, welche Ablage bearbeitet wird, und merkt eine Wahl für dieses Arbeitsverzeichnis. `--liste` zeigt, was zur Wahl steht | **läuft** |
| `hk-text [--gate] [--rhythm]` | prüft deutschsprachige Texte gegen die Schreibregeln. `--gate` blockiert, der Bericht nicht | **läuft** |
| `hk-install [--check]` | hängt den Harness als Plugin unter `~/.claude/skills/hkf` ein und räumt die alten Zeiger weg | **läuft** |
| `hk-suche <muster>` | findet Notizen: Volltext, `--typ`, `--hat`, `--verweist-auf`, `--fundstellen` | **läuft** |
| `hk-erwaehnungen <ziel>` | macht unverlinkte Erwähnungen einer Notiz zu qualifizierten Verweisen | **läuft** |
| `hk-verweise [--setzen]` | macht kurze Wikilinks zu qualifizierten (§3.6); Mehrdeutiges wird gemeldet, nicht geraten | **läuft** |
| `hk-kontext [--stimme]` | gibt aus, was in dieser Ablage gilt: Lage, Kanon, Stimme, Hinweise | **läuft** |
| `hk-publikation <notiz>` | führt die Lesereihenfolge einer Publikation: `--aufnehmen`, `--vor`, `--check`, `--richten` | **läuft** |
| `hk-buch <publikation>` | schreibt die Texte einer Publikation als ein Manuskript heraus, außerhalb der Ablage | **läuft** |
| `hk-epub <publikation>` | baut daraus mit `pandoc` ein EPUB | **läuft** |
| `hk-kontinuitaet [--richten]` | prüft einen Erzählbestand: Zeiträume, abgeleitete Listen, veraltete Beurteilungen | **läuft** |
| `hk-publish <kommando> <notiz>` | überträgt eine Notiz an eine HenniBock-Instanz: `analyze`, `build --send`, `attached` | **läuft** |
| `hk-kapitel next\|queue` | welches Kapitel als nächstes erscheint, aus der Rotation der Publikationen | **läuft** |

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

`--fix` darf ausschließlich die zwölf Handgriffe aus §6.3 — Typtabelle neu
erzeugen, fehlende Standard-Property-Typen anlegen, einen verzeichnislosen
Wikilink qualifizieren (nur bei genau einem Ziel), einen fehlenden Alias aus
dem `title` ergänzen, den Trenner ` / ` ausschreiben, ein `datetime` ohne
Uhrzeit auf den Tagesbeginn bringen, `created` und `modified` ergänzen,
`# Verbindungen` ordnen und ans Ende stellen, `related` daraus ergänzen, leere
Properties entfernen. Danach wird erneut geprüft.

**Was `--fix` nicht tut**, und beides steht so in §6.3: Es ergänzt keinen
Eintrag unter `# Verbindungen` und entfernt keinen — Verknüpfen ist Sache des
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
  derselben Lieferung gegenseitig, steht das danach unter `# Verbindungen` und
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
`# Verbindungen`. Gleiche `hkf-wikidata`-Kennungen werden als
Zusammenführungskandidat vorgelegt; unbelegte Properties mit Zieltyp noch
nicht.

## Was wo liegt

```
spec/        HKF Core und Config: die Spezifikation selbst, siehe spec/README.md
lib/hkf/     ablage, frontmatter, schema, grammatik, pruefen, korrigieren,
             importieren, exportieren, einlesen, notiz, vorlage, fassung
lib/hkf/text/ der Schreibregelprüfer: segment, engine, rules, rhythm_lint
lib/hkf/hennibock/ die Übertragung an eine HenniBock-Instanz
rules/       deutsch.json, der Basissatz der Schreibregeln
bin/         hk-init, hk-lint, hk-import, hk-export, hk-ingest,
             hk-tranchen, hk-types, hk-ablage, hk-text, hk-install,
             hk-suche, hk-erwaehnungen, hk-kontext, hk-publikation, hk-verweise,
             hk-buch, hk-epub, hk-kontinuitaet, hk-publish, hk-kapitel
py           das Python des Harness — baut die venv und startet sie
tools/       inventar.py hält Prosa, Schema und Grundausstattung gegeneinander,
             grundausstattung.py die Vorlage gegen Anhang A und §3.5.1
templates/   die Grundausstattung, aus der hk-init schöpft
bundles/     Typen, die nicht jede Ablage braucht, als Lieferung zum Import
skills/      die KI-Schicht: hkb und sieben Operationen, siehe skills/README.md
agents/      die Subagenten: wilma liest, marlene schreibt, astrid lektoriert,
             doris liest den Bestand
commands/    die Slash-Kommandos, siehe hk-install
hooks/       sitzung.py spielt den Kanon ein, schreibregeln.py blockt
core/        der Kanon: Identität, Zusammenarbeit, Sprache, Schreibregeln, YAML
profiles/    die Stimmen, aus denen eine Ablage eine wählt
.claude-plugin/  plugin.json und marketplace.json, sonst nichts
test/        Rauchprobe: python3 test/smoke.py
```

**Die Spezifikation liegt unter `spec/`, und zwar im Original.** Bis zum
07.09.2026 stand sie in einem eigenen Repository und hier nur als Kopie, die
ein Skript gleich hielt. Die Trennung trug, solange HKF für Dritte zitierbar
sein sollte. Der Anspruch ist aufgegeben, und damit blieb von ihr nur der
Preis: zwei Orte und die Möglichkeit, dass der eine zurückfällt.

Ein Harness setzt genau eine Fassung um, und welche, geht jetzt unmittelbar
aus seiner Auslieferung hervor. Die Nummer steht in `lib/hkf/__init__.py` und
nirgends sonst. Fortgeschrieben wird die Spezifikation hier.

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

Unter [`skills/`](skills/) liegen sieben Skills, die ein Sprachmodell durch die
Methoden führen. [`hkb`](skills/hkb/SKILL.md) ist die Grundlage, die übrigen
setzen ihn voraus: [`hkb-notiz`](skills/hkb-notiz/SKILL.md),
[`hkb-typ`](skills/hkb-typ/SKILL.md),
[`hkb-import`](skills/hkb-import/SKILL.md),
[`hkb-export`](skills/hkb-export/SKILL.md),
[`hkb-lint`](skills/hkb-lint/SKILL.md),
[`hkb-quelle`](skills/hkb-quelle/SKILL.md).

Unter [`agents/`](agents/) liegen drei Subagenten.
[`wilma`](agents/wilma.md) liest eine Quelle in ihrem eigenen Kontext und gibt
ein belegtes Destillat zurück. `hkb-quelle` ruft sie und liest nie selbst —
wer ein Buch im laufenden Gespräch liest, hat es danach im Rücken, und die
Notizen aus den letzten Kapiteln werden flacher als die aus den ersten. Ein
Agent liest, er schreibt nicht; für die Regel oben ändert er nichts.

[`marlene`](agents/marlene.md) schreibt die Erstfassung eines längeren
Sachtextes, [`astrid`](agents/astrid.md) lektoriert ihn. Beide schreiben in die
Ablage, und für sie gilt dieselbe Regel wie für einen Skill: Was mechanisch
geht, messen sie mit `hk-text` und `hk-lint`, statt danach zu urteilen. Ihre
Stimme holen sie sich mit `hk-kontext` — ein Subagent sieht nicht, was die
Hauptsitzung bekommen hat.

**Damit ein Modell sie findet**, ist der Harness ein Plugin. Das Manifest steht
in `.claude-plugin/`, die Bausteine liegen an der Wurzel: `skills/`, `agents/`,
`commands/` und `bin/`. Das Plugin heißt `hkf`, und alles darin trägt den
Namensraum davor, also `hkf:hkb-quelle` und `hkf:wilma`. Die Werkzeuge aus
`bin/` liegen dabei auf dem Pfad, ohne dass jemand ihn pflegt.

```bash
hk-install --check     # was fehlt
hk-install             # einhängen
```

Auf der Maschine, auf der das Repository selbst liegt, hängt `hk-install` es
unter `~/.claude/skills/hkf` ein. Claude Code lädt jedes Verzeichnis dort, das
ein `.claude-plugin/plugin.json` trägt, als Plugin. Ein Symlink genügt, und das
Repository bleibt die gelesene Fassung. Der Weg über den Marktplatz kopiert
dagegen in einen Cache, was für die Verteilung an andere richtig ist und für
die Entwicklung falsch.

`hk-install` räumt dabei weg, was früher von Hand gesetzt wurde: je ein Symlink
unter `~/.claude/skills/` und `~/.claude/agents/`. Solche Einträge verdrängen
die Fassung aus dem Plugin stillschweigend. Genau daran ist `hkb-typseite` nach
seiner Entstehung monatelang unsichtbar geblieben, weil niemand den neunten
Symlink nachgezogen hat. Ein Zeiger auf einen **fremden** Harness wird nicht
angefasst, sondern gemeldet.

### Der Kanon kommt aus der Sitzung, nicht aus der Ablage

Zwei Hooks liegen im Plugin. Beim Start einer Sitzung sagt `hooks/sitzung.py`,
welche Ablage aktiv ist und woher ihr Pfad kommt, und spielt ein, was gilt: den
Kanon aus [`core/`](core/), die Stimme, die die Wurzeldatei unter `voice`
nennt, und die `hint`-Notizen der Ablage. Ist keine Ablage gewählt und liegt
die Sitzung nicht in einer, zählt er auf, was zur Wahl steht. Geraten wird
nicht.

**In der Ablage entsteht dabei nichts.** Das ist der Unterschied zu einem
Generator, der aus einem Manifest eine `CLAUDE.md` in den Vault schreibt, dazu
Agentenfassungen, Hook-Einträge und Skill-Zeiger. Acht erzeugte Artefakte, die
auseinanderlaufen können, in einer Ablage, die nach §4 keine Werkzeugdatei
tragen soll. Ein Hook braucht nichts davon, und ein fremder Vault bleibt
unangetastet.

Der zweite, `hooks/schreibregeln.py`, hält einen Schreibvorgang an, der gegen
die harten Regeln verstößt: unzulässige Zeichen, verbotene Interpunktion,
Umlaut-Ersatzformen. Warnungen zu Satzlänge und Wortwahl halten niemanden auf.
Außerhalb einer Ablage tut er nichts, und wenn der Prüfer nicht laufen kann,
lässt er durch und sagt warum. Ein Prüfer, der nicht läuft, ist kein
Regelverstoß.

Die Wurzeldatei steuert beides über zwei freigestellte Properties:

| Property | Was sie sagt | Vorgabe |
|---|---|---|
| `voice` | welches Profil aus `profiles/voices/` gilt | `henni-knowledge` |
| `hints` | wo die `hint`-Notizen liegen | `Hints` unter `wiki_base` |

Sie fügen nichts hinzu, was die Werkzeuge nicht können — sie tun genau das,
was ein Programm nicht darf. Am deutlichsten bei `hkb-import`: `hk-import`
legt eine Bedeutungsprüfung vor und weist ab, der Skill urteilt und trägt das
Urteil als Zeile in `# Entscheidungen` der Bundle-Notiz ein (§5.7). Ohne
diesen Eintrag stellt der nächste Lauf dieselbe Frage neu.

## Welche Fassung gilt

`CORE` in [`lib/hkf/__init__.py`](lib/hkf/__init__.py) nennt die Fassung, die
dieser Harness umsetzt; unter [`spec/`](spec/) liegt sie im Wortlaut. Beides
gehört zusammen und wird zusammen fortgeschrieben, in einem Commit.

Wer Core oder Config ändert, prüft, ob die Werkzeuge noch dasselbe Inventar
kennen wie die Prosa:

```
python3 tools/inventar.py          Prosa, Schema und Grundausstattung gegeneinander
python3 tools/grundausstattung.py  die Vorlage gegen Anhang A und §3.5.1
```

Die Rauchprobe ruft beide mit auf. Eine Abweichung fällt beim nächsten
Testlauf auf, nicht erst beim nächsten Import.

**Was der Harness liest** (§8): jede Fassung mit derselben Major-Nummer, deren
Minor nicht größer ist als die eigene. Minor-Fassungen ergänzen Regeln, ohne
Bestehendes ungültig zu machen — was Core 1.0 schrieb, versteht ein Harness
1.2. Umgekehrt gilt es nicht, und §8 sagt, was dann geschieht: Die Dateien
sind lesbar, übernommen wird nichts. `hk-import` weist eine solche Lieferung
ab, `hk-lint` meldet eine Ablage, die neuer ist als er selbst.

## Die Grundausstattung gegen die Spezifikation

Die Kern-Typen stehen zweimal: als Markdown-Block in Anhang A und als
ausgelieferte Datei unter `templates/hkb/Typedefs/`. Die vierzehn
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
Beispiel-Wissensbasis der Werkbank abgeleitet — alle Notizen in
`90-System/Typedefs/` und `90-System/Proptypes/`, die keine
`bundles`-Property tragen (§5.3):

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
