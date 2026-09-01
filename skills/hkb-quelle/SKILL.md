---
name: hkb-quelle
description: "Aus einer Quelle eine Lieferung machen — Quellennotiz mit Zitationsangaben und Zusammenfassung, dazu die Notizen, die aus ihr entstehen. Wahlweise gleich in die Wissensbasis importieren. Verwenden bei: Quelle einlesen, diese URL einlesen, ein Buch erfassen, ein Clipping verarbeiten, Ingest, Bundle aus einer Quelle bauen."
---

# Aus einer Quelle eine Lieferung machen

Zuerst [[hkb]] lesen. Du bekommst eine Quelle — eine Adresse, eine Datei, ein
Stück aus der Inbox — und lieferst eine fertige Lieferung: die Quellennotiz
mit ihren Zitationsangaben und einer Zusammenfassung, die Notizen, die aus ihr
entstehen, `hbundle.md`, und `hk-lint` sagt grün.

Mit `--hkb` geht dieselbe Lieferung anschließend in die Ablage. Das ist der
einzige Unterschied zwischen den beiden Fällen.

## Die Reihenfolge steht fest

> `hk-ingest` → **Wilma** → du trägst ein.

Erst das Mechanische: kopieren oder nicht, `sha256`, die Quellennotiz mit dem,
was sicher bekannt ist, und eine Liste der Lücken. Dann liest **Wilma** die
Quelle und gibt ein belegtes Destillat zurück. Dann trägst du ein, was sie
liefert. Das ist „erst `bin/`, dann `skills/`" auf einen einzelnen Lauf
angewandt.

## Ablauf

**① Einlesen.** Ohne Argumente zeigt `hk-ingest`, was in der Inbox liegt und
schreibt nichts.

```bash
hk-ingest
hk-ingest --alles --bundle <ziel>
```

Eine `.md` sagt ihren Typ selbst; eine nackte Datei nicht. Dann verlangt das
Werkzeug `--typ` und nennt die vier: `book`, `article`, `clipping`, `webpage`.
**Rate ihn nicht** — frag lieber zurück. Für eine Quelle, die gar nicht in der
Inbox liegt, nimm den händischen Weg:

```bash
hk-ingest --bundle <ziel> --typ book --title T --url U \
          --ausfertigung https://nas.example.org/buch.pdf
```

`--ausfertigung` kopiert nichts; es hält fest, wo das Original liegt. Genau
dafür ist es da: Ein Buch auf einem Dateiserver gehört nicht in die Ablage.

**② Lesen lassen.** Starte den Subagenten `wilma` mit der Quelle und der
Lückenliste aus Schritt ① als Auftrag. Sie liest in ihrem eigenen Kontext und
gibt Zitationsangaben, Aufbau, belegte Substanz und Notiz-Kandidaten zurück.

**Lies die Quelle nicht selbst.** Auch nicht „nur kurz nachschauen": Wandert
sie nachträglich in deinen Kontext, war Wilmas Lauf umsonst. Reicht das
Destillat für eine Notiz nicht, starte sie erneut mit einer engeren Frage.

**③ Besprechen.** Sag dem Nutzer, was in der Quelle steht und was daraus
entstehen soll — auf Grundlage des Destillats, nicht der Quelle. Erst danach
schreiben.

**④ Prüfen, was es schon gibt.** Durchsuche `Sources/`, `Concepts/`, `Terms/`
und `Persons/` nach den Notiz-Kandidaten. Eine zweite Notiz über dieselbe
Sache ist teurer als eine Ergänzung.

**⑤ Eintragen.** In die Quellennotiz die Zitationsangaben und die
Zusammenfassung; daneben, was aus ihr entsteht.

**⑥ Berichten.** `hk-lint <ziel>` muss grün sein. Dann sag, was in der
Lieferung liegt und welche Lücken offen blieben.

## Die Zusammenfassung folgt dem Aufbau der Quelle

Nicht einer eigenen Gliederung: je Kapitel oder Hauptabschnitt eine
Überschrift, die den Titel der Quelle spiegelt, darunter Prosa. Sie bildet
Aufbau **und** Inhalt ab, nicht nur die Kernaussagen — Wilmas Abschnitt
`## Aufbau` ist dafür das Gerüst.

Was die Quelle sagt, gehört in die Quellennotiz. Was du daraus für die eigene
Sache schließt, in eine `note` oder ein `concept`, verbunden über `sources`.

## Eine bestehende Notiz fortschreiben

Soll die Lieferung eine Notiz erweitern, die es in der Wissensbasis schon
gibt, trägt sie `extends` mit deren Notiz-ID:

```yaml
extends: Concepts/analytical-engine
```

Der Import hängt den Body dann an, statt zu ersetzen, vereinigt die Listen und
legt einen abweichenden Skalar vor (§6.1 Schritt 5). Die Notiz behält ihre
Herkunft und führt danach beide Lieferungen.

## Große Quellen: Tranchen entlang des Aufbaus

Ab einer Größe, die auch ein Destillat nicht mehr trägt — ein ganzes Buch, ein
langes Transkript —, reicht ein Wilma-Lauf nicht.

1. Ein erster Lauf holt nur den **Aufbau**. Er wird zum Überschriften-Gerüst
   der Zusammenfassung und zugleich zur Tranchenliste.
2. Je Tranche eine Zeile in der Quellennotiz: welches Material sie umfasst,
   welche Notizen sie voraussichtlich auslöst.
3. Je Tranche dann: Wilma mit der Tranche als Abgrenzung → Notizen schreiben →
   den zugehörigen Abschnitt der Zusammenfassung füllen → Tranche abhaken.

**Entlang der Struktur der Quelle, nicht nach Notiztypen gruppiert.** Eine
Person und das Ereignis, in dem sie vorkommt, entstehen im selben Durchgang
und tragen dieselben Wikilinks. Nach Typ gruppiert würde derselbe Zusammenhang
zwei- oder dreimal gelesen.

Weil die Tranche selbst nie in deinem Kontext lag, trägt eine Sitzung mehrere.

## Wann eine Notiz entsteht

Das schreibt dieser Skill **nicht** fest. Es gehört in die Ablage, als `hint`
mit `applies_to` (Harness §7). Lies ihn, bevor du entscheidest.

Gibt es keinen, sag, wonach du gehst, und schlag vor, einen anzulegen. Ein
brauchbarer Anfang: eine eigene Notiz, wenn ein Gegenstand in zwei Quellen
vorkommt oder in einer zentral ist — für eine beiläufige Erwähnung keine.

## Nicht tun

- **Die Quelle nicht selbst lesen.** Dafür gibt es Wilma.
- **Keine glatte Zusammenfassung.** Widerspricht die Quelle dem Bestand, steht
  danach **beides** da, mit Datum und Herkunft. Ein Modell, das aus
  Uneinigkeit einen Konsens macht, schreibt eine saubere Notiz mit einer
  Autorität, die ihr Inhalt nicht deckt (Harness §7).
- **Nichts entfernen.** Eine Ergänzung fügt hinzu; Streichen ist Sache eines
  Menschen (§5.6).
- **Keine Angabe raten.** Was Wilma nicht gefunden hat, bleibt leer und wird
  gemeldet. Eine erfundene Jahreszahl in einer Zitation ist schlimmer als
  keine.
