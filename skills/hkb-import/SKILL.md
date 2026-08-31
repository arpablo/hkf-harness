---
name: hkb-import
description: "Ein HKF-Bundle in eine Wissensbasis übernehmen und dabei die Urteile fällen, die hk-import verweigert — die Bedeutungsprüfung zweier gleichnamiger Typen und die Identität einer ankommenden Notiz. Verwenden bei: Bundle importieren, Lieferung einlesen, hk-import, ein Bundle nachladen."
---

# Eine Lieferung übernehmen

Zuerst [[hkb]] lesen. `hk-import` erledigt die zehn Schritte aus §6.1 —
alle bis auf drei Urteile, die es ausdrücklich nicht fällt. Die fällst du,
und du **schreibst sie auf**, sonst fragt der nächste Lauf wieder.

## Ablauf

**① Trockenlauf.**

```bash
hk-import --check <bundle-pfad>
```

Es schreibt nichts und berichtet in drei Abschnitten: *Was geschieht*, *Was
zu entscheiden ist*, *Was zu tun ist*. Lies alle drei, bevor du irgendetwas
anfasst.

**② Ist nichts zu entscheiden**, führ den Import aus und berichte, was
geschehen ist. Fertig.

```bash
hk-import <bundle-pfad>
```

**③ Steht etwas zu entscheiden**, arbeite es der Reihe nach ab (unten), trag
das Urteil in die Bundle-Notiz ein und **wiederhole den Import**. Das Urteil
gilt dann und wird nicht neu erfragt (§5.7).

## Die Urteile

### Bedeutungsprüfung — zwei gleichnamige Typen (§5.5)

> `person  Gleicher Name, Bedeutung nicht zugesichert.`
> `        hier    Ein Mensch.`
> `        Bundle  Ein Datensatz der Personalverwaltung.`

**Die Frage lautet nicht, ob die Namen gleich sind, sondern ob die Sache
dieselbe ist.** Lies dazu beide `description`, beide Property-Tabellen und
eine Stichprobe der ankommenden Notizen: Sind das Menschen im Sinne der
hinterlegten Beschreibung, oder etwas anderes, das nur so heißt?

| Urteil | Folge |
|---|---|
| `gleich` | Die Typen werden zusammengeführt, der Import läuft. |
| `verschieden` | Der Import wird abgewiesen. Einer der beiden Typen muss umbenannt werden — das ist Sache eines Menschen. |

**Im Zweifel `verschieden`.** Zwei Bestände in einem Verzeichnis lassen sich
nur Notiz für Notiz wieder trennen; ein abgewiesener Import kostet einen
zweiten Anlauf. `--force` hilft hier nicht und ist auch nicht dafür gedacht.

### Identität — eine Notiz-ID gibt es schon (§6.1 Schritt 5)

> `Persons/john-smith gibt es schon, und nichts verankert die beiden aneinander.`

Der Pfad beweist nichts: `Persons/john-smith` heißt in zwei Lieferungen
leicht gleich und meint zwei Menschen. Vergleiche beide Notizen — Titel,
Body, Properties, Zeitangaben.

| Urteil | Folge |
|---|---|
| `dieselbe` | Die Notiz trägt danach beide Bundles in `bundles`. |
| `verschieden` | Eine der beiden muss umziehen, bevor der Import weitergeht. Auch das ist Sache eines Menschen. |

Ein Erstkontakt ist **kein Fehler, sondern eine Frage**. Eine Wissensbasis
darf dieselbe Notiz aus mehreren Lieferungen beziehen.

### Verknüpfung (§5.6)

Was mechanisch sicher ist, setzt `hk-import` selbst: Nennt der Body einer
Notiz den Titel einer anderen wörtlich und verlinkt ihn nicht ohnehin schon,
entsteht ein Eintrag unter `# Siehe auch`. Vorgelegt wird der Rest — etwa
zwei Notizen mit derselben `hkf-wikidata`-Kennung. Die gehören
**zusammengelegt, nicht verlinkt**, und das entscheidet ein Mensch.

Du darfst über die mechanischen Beobachtungen hinausgehen und Zusammenhänge
vorschlagen, die kein Namensvergleich findet. Dann trägst du deinen
Modellnamen in `modified_by` ein, und der Grund in der Zeile ist deine
Begründung.

## Das Urteil aufschreiben

In `<base>/Bundles/<id>.md`, Abschnitt `# Entscheidungen`, **vor** den
Importnachweisen (§5.1). Gibt es die Notiz noch nicht — beim ersten Import
mit offener Frage —, legst du sie mit `type`, `id`, `description` und diesem
Abschnitt an, sonst nichts.

```markdown
# Entscheidungen

| Gegenstand | Urteil | Von | Beurteilt | Grund |
|---|---|---|---|---|
| Typ `person` | verschieden | claude-opus-5 | Ein Datensatz der Personalverwaltung. | unserer meint einen Menschen, nicht seinen Personalsatz |
| Notiz [[Persons/john-smith\|John Smith]] | dieselbe | armin | John Smith | gleiche Lebensdaten, gleicher Beruf |
```

- **Gegenstand** ist `` Typ `<name>` `` oder `Notiz ` und ein qualifizierter
  Wikilink. In der Tabellenzelle wird der Strich als `\|` maskiert.
- **Urteil**: bei einem Typ `gleich` oder `verschieden`, bei einer Notiz
  `dieselbe` oder `verschieden`. Andere Werte gibt es nicht.
- **Von** ist dein Modellname, wenn du geurteilt hast, sonst der Name des
  Menschen. Das ist keine Höflichkeit: Es sagt verlässlich, **dass** eine
  Maschine geurteilt hat.
- **Beurteilt** ist der eine Satz, über den geurteilt wurde — bei einem Typ
  die **gelieferte** `description`, bei einer Notiz ihr **gelieferter**
  `title`. Daran hängt die Geltung: Bringt die Lieferung später einen anderen
  Satz, fällt die Entscheidung weg und die Frage wird neu gestellt.
- **Grund** ist Pflicht. Ein Halbsatz. Ohne ihn lässt sich das Urteil später
  weder prüfen noch aufheben.

Je Gegenstand **höchstens eine Zeile**. Ein zweites Urteil über dasselbe ist
ein Fehler — welches gälte, wäre nicht bestimmt.

**Auch eine Ablehnung wird aufgeschrieben.** Ein abgewiesenes Bundle wird
typischerweise mehrfach angeboten, bevor jemand es berichtigt; ohne den
Nachweis fragt jeder Versuch neu.

## Danach

```bash
hk-lint
```

Berichte am Ende, was übernommen wurde und was liegen blieb — mit den Zahlen
aus dem Bericht, nicht aus dem Gedächtnis.

## Grenzen

- **`--force` entscheidet nur, welche von zwei Fassungen gilt**, nie, ob zwei
  Dinge dasselbe meinen. Setz es nicht, um eine Rückfrage loszuwerden.
- **Ein Umzug ist Sache eines Menschen.** Fällt ein Urteil auf `verschieden`,
  endet dein Teil beim Aufschreiben und Berichten.
- **Du legst keine vorläufige Typdefinition an und entfernst keine.** Das tut
  der Import, und sie vergeht, wenn die richtige nachkommt (§5.4).
