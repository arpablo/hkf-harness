---
name: hkb-quelle
description: "Aus einer Quelle eine Lieferung machen — Quellennotiz mit Zitationsangaben und Zusammenfassung, dazu die Notizen, die aus ihr entstehen. Wahlweise gleich in die Wissensbasis importieren. Verwenden bei: Quelle einlesen, diese URL einlesen, ein Buch erfassen, ein Clipping verarbeiten, Ingest, Bundle aus einer Quelle bauen."
---

# Aus einer Quelle eine Lieferung machen

Zuerst [[hkb]] lesen. Du bekommst eine Quelle — eine Adresse, eine Datei, ein
Stück aus der Inbox — und lieferst eine fertige Lieferung: die Quellennotiz
mit ihren Zitationsangaben und einer Zusammenfassung, **die Notizen, die aus
ihr entstehen**, `hbundle.md`, und `hk-lint` sagt grün.

Mit `--hkb` geht dieselbe Lieferung anschließend in die Ablage. Das ist der
einzige Unterschied zwischen den beiden Fällen.

## Wozu das Ganze

> „A single source can trigger updates across 5-15 wiki pages. This is normal
> and desired — it's the compounding effect."

**Eine Lieferung mit nur einer Quellennotiz ist in aller Regel eine
unfertige Lieferung.** Die Quellennotiz sagt, was gelesen wurde; sie ist der
Beleg, nicht das Ergebnis. Das Ergebnis sind die Begriffe, Konzepte, Personen
und Vergleiche, die daraus in den Bestand wachsen — und die Verweise, mit
denen sie am Bestand hängen. Wer nur zusammenfasst, hat die Quelle abgelegt,
nicht eingelesen.

Diese Notizen gehören **in die Lieferung**. Dafür braucht es keine
Wissensbasis: Ein Bundle trägt Notizen jedes Typs, und wohin sie kommen,
entscheidet erst der Import (§4.3).

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

**⑤ Eintragen — zuerst die Quellennotiz.** Die Zitationsangaben aus Wilmas
Abschnitt `## Zitationsangaben`, die Zusammenfassung nach ihrem Abschnitt
`## Aufbau`. Was sie unter `## Lücken und Widersprüche` gefunden hat, gehört
in einen eigenen Abschnitt am Ende — es steht nicht in der Quelle und darf
nicht so aussehen, als stünde es dort.

**⑥ Eintragen — dann die Notizen, die daraus entstehen.** Geh Wilmas
`## Notiz-Kandidaten` **einzeln** durch und entscheide je Kandidat: eigene
Notiz, Abschnitt in einer anderen Notiz, oder nichts. Die Schwelle steht
unten. Für jeden, der eine Notiz wird:

- Typ wählen (`concept`, `term`, `person`, `comparison`, `note` …) und die
  Property-Tabelle des Typs lesen, bevor du ein Feld setzt.
- `sources` auf die Quellennotiz setzen — das ist die Verbindung, an der der
  Bestand später hängt.
- Untereinander verlinken, wo der Body es hergibt; einen Verweis unter
  `# Siehe auch` auch in `related` führen (§5.6).
- Der Inhalt kommt **allein aus dem Destillat**. Was Wilma nicht belegt hat,
  steht nicht drin.

**⑦ Berichten.** `hk-lint <ziel>` und `hk-lint --strict <ziel>` müssen grün
sein. Dann sag:

- was in der Lieferung liegt, nach Typ,
- **welche Kandidaten du verworfen hast und warum** — nicht die Zahl, die
  Gruppen,
- welche Zitationsangaben offen blieben.

**Liefert der Lauf nur die Quellennotiz**, ist das ein Ergebnis, das begründet
werden muss, kein Ergebnis, das einfach eintritt. Sag dann ausdrücklich, nach
welcher Schwelle du gegangen bist und warum kein Kandidat sie erreicht hat.
Fehlt eine Ablage, ist das **kein** Grund: Die Notizen gehören in die
Lieferung.

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
brauchbarer Anfang: **eine eigene Notiz, wenn ein Gegenstand in zwei Quellen
vorkommt oder in dieser einen zentral ist** — für eine beiläufige Erwähnung
keine.

Drei Fälle, in denen ein Kandidat trotzdem keine Notiz wird:

| Fall | Wohin statt dessen |
|---|---|
| Er ist ein **Bestandteil** eines größeren Gegenstands der Quelle | ein Abschnitt in dessen Notiz |
| Er ist eine **Aufzählung** ohne eigenen Begriff dahinter — „zwölf Prüfungen", „dreizehn Kennzahlen" | bleibt in der Zusammenfassung der Quellennotiz |
| Die Quelle nennt ihn nur **im Vorbeigehen** | gar nicht; höchstens ein Wikilink, wenn es die Notiz schon gibt |

Eine `comparison` verlangt `compares` mit mindestens zwei Verweisen. Gibt die
Quelle nur einen der verglichenen Gegenstände her, entsteht **keine** — sonst
schriebest du eine Notiz über etwas, worüber die Quelle nichts sagt.

## Nicht tun

- **Nicht bei der Quellennotiz aufhören.** Sie ist der Beleg, nicht das
  Ergebnis. Wer die Kandidaten überspringt, hat abgelegt statt eingelesen —
  und das Fehlen der Notizen zu *berichten* macht es nicht zum Ergebnis.
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
