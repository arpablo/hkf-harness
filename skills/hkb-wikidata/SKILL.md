---
name: hkb-wikidata
description: "Die `wikidata_id` einer Notiz bestimmen: Kandidaten holen, den richtigen wählen, eintragen. Verwenden bei: Wikidata-Kennung suchen, Q-Nummer für diese Notiz, wikidata_id setzen, Notizen mit Wikidata verknüpfen."
---

# Die Wikidata-Kennung einer Notiz bestimmen

Zuerst [[hkb]] lesen. Gesucht und geschrieben wird mit `hk-wikidata`; von Hand
trägst du keine Kennung ins Frontmatter.

## Die Arbeitsteilung

`hk-wikidata <ziel>` sucht und legt vor. Es filtert weg, was in Wikidata kein
Gegenstand ist, holt zu jedem Kandidaten `P31` und die Lebensdaten und hält
sie gegen die Notiz. Es entscheidet nicht.

**Du entscheidest, und zwar an der Beschreibung der Notiz.** Das ist die ganze
Aufgabe. `Hussein ibn Ali` liefert nach dem Filter zwei Menschen: den König
des Hedschas und den dritten Imam der Schiiten. Beide heißen so, beide sind
Menschen, und nur die `description` der Notiz sagt, welcher gemeint ist.

`hk-wikidata <ziel> --setzen Q…` trägt die gewählte Kennung ein und prüft
dabei noch einmal: Form, Existenz, keine Begriffsklärung, Typ passt, keine
andere Notiz führt sie schon.

## Die Regeln stehen in der Ablage

Der Property-Typ `hkf-wikidata` unter `<config_base>/Proptypes/` trägt sie
ausformuliert. **Lies ihn, bevor du eine Kennung setzt**, und wiederhole ihn
nicht hier. Das Wichtigste daraus:

- Die Kennung ist der Anker. Abgerufene Daten gehören in eigene Properties,
  nicht als Kopie eines Wikidata-Datensatzes in die Notiz.
- Vorhandene Werte werden nicht stillschweigend überschrieben.
- Verwechselte Kennungen sind der häufigste Fehler.
- Nicht alles hat eine Kennung. Die Property ist nirgends Pflicht.

## Der Ablauf für eine Notiz

```bash
hk-wikidata 40-Wiki/Persons/hussein-ibn-ali
```

Der Bericht nennt je Kandidaten die Kennung, das Label, die Beschreibung, `ist:`
aus `P31`, die Lebensdaten und die Belege. Verworfene stehen mit ihrem Grund
dabei, damit du siehst, worauf das Urteil beruht.

Dann entscheidest du:

**`eindeutig`** heißt, ein Kandidat blieb übrig und ein Beleg stützt ihn. Lies
trotzdem die Beschreibung gegen die Notiz. Ein Beleg ist ein Beleg und kein
Beweis.

**`mehrdeutig`** ist der Regelfall und dein eigentlicher Auftrag. Halte die
`description`, die `sources` und den Zusammenhang der Notiz gegen die
Beschreibungen der Kandidaten. Was der Bestand über den Gegenstand sagt, steht
in seiner Notiz, nicht in Wikidata.

**`nichts`** heißt nicht „gibt es nicht", sondern „unter diesem Namen nicht
gefunden". Bevor die Property leer bleibt, sieh zweimal nach: einmal mit dem
vollen Namen, einmal mit der englischen Transliteration. Die Suche von
Wikidata trifft eine abweichende Umschrift nicht, und ein Bestand mit
arabischen, osmanischen oder russischen Namen führt sie in Dutzenden
Varianten.

Bleibt es dabei, ist das kein Mangel. Eigene Denkfiguren einer Wissensbasis
stehen in keinem Weltverzeichnis, und die Property ist nirgends Pflicht.

Passt keiner, setzt du keinen. Bist du zwischen zweien unsicher, legst du
beide vor und fragst. Eine falsche Kennung ist schlimmer als keine: Sie sieht
belegt aus.

```bash
hk-wikidata 40-Wiki/Persons/hussein-ibn-ali --setzen Q128906
```

## Ein ganzer Bestand

```bash
hk-wikidata --alle --typ person
```

**In Tranchen, nicht in einem Zug.** Zwanzig Notizen, vorlegen, was du
gewählt hast, schreiben, weiter. Ein Lauf, der siebzig Kennungen auf einmal
setzt, ist nicht mehr zu prüfen, und ein Vertipper darin fällt nie auf.

Der Bericht am Ende einer Tranche nennt je Notiz die gesetzte Kennung mit dem
Label, die übergangenen mit dem Grund, und die offenen mit der Frage, die noch
zu klären ist.

`--json` gibt denselben Bestand maschinenlesbar, wenn du über viele Notizen
zählen oder sortieren willst.

## Was danach möglich wird

Sobald Kennungen dastehen, findet man Dubletten, die über den Namen nie
auffielen: Zwei Notizen mit derselben Kennung meinen denselben Gegenstand.
`--setzen` weist das schon beim Schreiben ab und nennt die andere Notiz.

Aus der Kennung lassen sich `born`, `died`, Koordinaten und Normdatennummern
nachziehen. Das ist ein eigener Arbeitsgang und gehört nicht hierher: Erst
steht der Anker, dann füllt man die Properties, und jeder abgerufene Wert wird
gegen den vorhandenen gehalten, statt ihn zu ersetzen.

## Was nicht funktioniert hat

**Den ersten Treffer nehmen.** Die Suche ordnet nach Namensähnlichkeit und
nicht nach Bekanntheit. Bei einem historischen Namen steht regelmäßig ein
anderer Mensch aus einem anderen Jahrhundert oben.

**Begriffsklärungsseiten über eine feste Liste von `P31` erkennen.** Wikimedia
legt für sein eigenes Inventar ständig neue Klassen an, und eine Liste hängt
ihnen hinterher. Das Werkzeug prüft deshalb zusätzlich die Bezeichnung der
Klasse. Wer den Filter erweitert, erweitert beides.

**Auf Lebensdaten als Unterscheidung bauen.** Sie trennen zuverlässig, wo sie
dastehen, und in einem frisch aufgebauten Bestand steht `born` fast nie. Der
Beleg ist ein Gewinn, kein Verlass.

**`nichts` für bare Münze nehmen.** In der ersten Tranche einer Ablage über den
Nahen Osten waren zwei von drei solchen Meldungen falsch: `Aziz Ali al-Masri`
steht dort als `'Aziz 'Ali al-Misri`, `David Hogarth` als `David George
Hogarth`. Beide fand die zweite Suche sofort. Der Fehler liegt nicht in der
Notiz und nicht in Wikidata, sondern zwischen zwei Umschriften desselben
Namens.

**Den zweiten Anlauf ins Werkzeug legen.** Erwogen und verworfen: Eine
automatische Nachsuche über Namensbestandteile bringt bei jedem Namen weitere
Kandidaten und verwässert die Liste, die gerade deshalb brauchbar ist, weil
sie kurz bleibt. Die zweite Suche ist Urteilsarbeit und gehört hierher.
