---
name: hkb-quelle
description: "Aus einer Quelle eine Lieferung machen — Quellennotiz mit Zitationsangaben und Zusammenfassung, dazu die Notizen, die aus ihr entstehen. Wahlweise gleich in die Wissensbasis importieren. Eine große Quelle wird in Tranchen gelesen, einzeln oder auf Anordnung im Durchlauf. Verwenden bei: Quelle einlesen, diese URL einlesen, ein Buch erfassen, ein Clipping verarbeiten, Ingest, Bundle aus einer Quelle bauen, Tranche lesen, alle Tranchen durchlaufen."
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
>
> Bei einer großen Quelle je Tranche einmal, geführt von `hk-tranchen`.

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

Jede Quelle wird eine `source`; offen ist nur ihre **Werkart**. Eine
Web-Clipper-`.md` sagt sie selbst (`web`), eine nackte Datei nicht — dann
bleibt `kind` leer und wird als Lücke gemeldet. **Rate sie nicht**; Wilma
liest die Quelle und sagt sie. Zur Wahl stehen `article`, `book`, `paper`,
`podcast`, `transcript`, `video` und `web`.

Für eine Quelle, die gar nicht in der Inbox liegt, nimm den händischen Weg:

```bash
hk-ingest --bundle <ziel> --kind book --title T --url U \
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

Ist die Quelle zu groß für einen Lauf — ein Buch, ein langes Transkript —,
geht es hier in Tranchen weiter; der Abschnitt dazu steht unten.

**③ Besprechen.** Sag dem Nutzer, was in der Quelle steht und was daraus
entstehen soll — auf Grundlage des Destillats, nicht der Quelle. Erst danach
schreiben.

**④ Prüfen, was es schon gibt.** Durchsuche die Typverzeichnisse der
Wissensbasis nach den Notiz-Kandidaten — die Quellen, die Konzepte, die
Begriffe, die Personen; wie sie heißen, sagt die Typtabelle in `hkb.md`. Eine zweite Notiz über dieselbe
Sache ist teurer als eine Ergänzung.

**⑤ Eintragen — zuerst die Quellennotiz.** Die Zitationsangaben aus Wilmas
Abschnitt `## Zitationsangaben`, die Zusammenfassung nach ihrem Abschnitt
`## Aufbau`. Was sie unter `## Lücken und Widersprüche` gefunden hat, gehört
in einen eigenen Abschnitt hinter die Zusammenfassung — es steht nicht in der
Quelle und darf nicht so aussehen, als stünde es dort.

**Der erfasste Text gehört nicht in die Notiz.** Ein Clipping liegt als Datei
unter `<media_base>/Clippings/`, und `file` zeigt darauf; die Notiz trägt die
Zusammenfassung. `hk-ingest` legt beides an.

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

**Die Wikilinks gehören in die Prosa.** Jede Notiz, die eine Tranche
hervorgebracht hat, wird im zugehörigen Abschnitt genannt und dorthin
verlinkt. Damit wird die Zusammenfassung zum Einstieg in den Bestand: Wer
chronologisch lesen will, geht der Reihe nach; wer eine Person oder ein
Ereignis sucht, springt über den Verweis. Eine Zusammenfassung ohne diese
Verweise erzählt die Quelle ein zweites Mal, statt an den Bestand zu führen.

Bei einer tranchierten Quelle steht **vor** den Abschnitten ein kurzer
Abschnitt `# Kernaussagen` — was das Werk im Ganzen behauptet, in wenigen
Punkten. Er entsteht **nach der letzten Tranche** und nicht vorher: Vorher
wüsstest du nur, was die ersten Kapitel behaupten.

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
langes Transkript —, reicht ein Wilma-Lauf nicht. Dann wird die Quelle in
Tranchen gelesen, **entlang ihrer eigenen Struktur und nicht nach Notiztypen
gruppiert.** Eine Person und das Ereignis, in dem sie vorkommt, entstehen im
selben Durchgang und tragen dieselben Wikilinks. Nach Typ gruppiert würde
derselbe Zusammenhang zwei- oder dreimal gelesen.

**Alle Tranchen arbeiten in derselben Lieferung.** Tranche 7 ergänzt einfach
die Notizdatei, die Tranche 3 angelegt hat; `extends` braucht es dafür nicht,
das gilt erst gegenüber dem Bestand einer Ablage. Mit `--hkb` geht die
Lieferung **einmal am Ende** hinüber — ein Import, ein Bundle-Eintrag, ein
Importnachweis.

### Die Liste anlegen

Ein erster Wilma-Lauf holt **nur den Aufbau**, nicht die Substanz. Er wird
zum Überschriften-Gerüst der Zusammenfassung und zugleich zur Tranchenliste:

```bash
hk-tranchen <quellennotiz> --anlegen -     # Wilmas `## Tranchenvorschlag`, Zeile für Zeile
hk-tranchen <quellennotiz>                 # zeigt die Liste
```

Durchgereicht wird **nur dieser Abschnitt**, nicht das ganze Destillat: Sonst
würde jede Aufzählung darin eine Tranche.

Die Liste steht danach als Abschnitt `# Tranchen` in der Quellennotiz und ist
**der Stand des Laufs, nicht dein Gedächtnis**. Das ist der Grund, warum sie
dort steht und nicht im Gespräch: Ein Buch trägt ein Dutzend Tranchen, und
keine darf davon abhängen, dass die vorige noch im Kontext liegt. Nach einer
Kompaktierung sagt `--naechste`, wo der Lauf steht; nach einem Abbruch morgen
ebenso.

Eine Tranche ist so groß, dass **ein** Wilma-Lauf sie trägt — ein Teil, ein
Kapitelblock, ein Stundenabschnitt eines Transkripts. Zu klein geschnitten
zerreißt sie Zusammenhänge, zu groß geschnitten liefert sie ein dünnes
Destillat.

### Ein Durchgang je Tranche

```bash
hk-tranchen <quellennotiz> --naechste
```

Dann, für genau diese Tranche:

1. **Wilma starten**, mit der Abgrenzung als Auftrag. Ein Auftrag, eine
   Tranche — auch im Durchlauf.
2. **Prüfen, was es schon gibt** (Schritt ④ oben), und zwar in der Ablage
   *und* in der Lieferung: Die frühere Tranche hat vielleicht schon eine
   Notiz angelegt, an die diese hier anschließt.
3. **Eintragen**: die Notizen aus den Kandidaten, den zugehörigen Abschnitt
   der Zusammenfassung, und was Wilma unter Lücken gefunden hat.
4. **`hk-lint <ziel>`** muss grün sein, bevor die Tranche abgehakt wird.
5. **Abhaken:**

```bash
hk-tranchen <quellennotiz> --abhaken 3 --ertrag "3 neu, 5 fortgeschrieben"
```

**Welche Notizen dabei entstanden sind, schreibst du nicht in die
Quellennotiz.** Das steht am Ende im Importnachweis der Bundle-Notiz, je
Notiz mit Typ und Zustand, maschinell und vollständig (§5.1). Es dort und
hier zu führen hieße, zwei Fassungen derselben Auskunft zu pflegen. `Ertrag`
trägt eine Zeile, mehr nicht.

### Einzelschritt ist die Vorgabe

Nach einer Tranche hältst du an, berichtest wie in Schritt ⑦ und sagst, was
die nächste umfasst. Der Benutzer sieht dann, ob der Schnitt trägt und ob die
Notizen die Schwelle treffen — beim zweiten Dutzend ist das nicht mehr zu
korrigieren.

### Ein Durchlauf läuft nur auf Anordnung

Ein Durchlauf arbeitet die offenen Tranchen ohne Rückfrage nacheinander ab.
Er kostet ein Vielfaches eines gewöhnlichen Laufs — je Tranche ein
Wilma-Lauf und ein Schreibdurchgang —, und darum **ordnet ihn der Benutzer
an**. Dass er eine große Quelle einlesen ließ, ist keine Anordnung, und ein
knapper Auftrag ist keine Vollmacht für zwölf Läufe.

Bevor du startest, sag drei Dinge und warte auf ein klares Ja:

- wie viele Tranchen offen sind und welches Material sie umfassen,
- dass jede davon einen eigenen Wilma-Lauf und einen Schreibdurchgang
  bedeutet, der Lauf also ungefähr so viel kostet wie diese Zahl einzelner
  Läufe,
- dass er jederzeit unterbrochen werden kann: Der Stand steht in der
  Quellennotiz, die halbe Lieferung ist gültig, und ein späterer Aufruf setzt
  bei der nächsten offenen Tranche fort.

Im Durchlauf gilt:

- **Je Tranche eine Zeile Bericht** — Nummer, Abgrenzung, was entstanden ist.
  Der ausführliche Bericht kommt am Ende, über den ganzen Lauf.
- **Nicht nach jeder Tranche zurückfragen.** Das wäre der Einzelschritt, und
  der Benutzer hat etwas anderes angeordnet.
- **Den Stand nach jeder Tranche festschreiben**, bevor die nächste beginnt.
  Ein Durchlauf, der drei Tranchen im Kopf behält und dann abbricht, hat sie
  verloren.
- **Die Quelle nie selbst lesen**, auch nicht bei der letzten Tranche, wenn
  das Destillat der ersten längst aus dem Kontext gefallen ist.

**Der Durchlauf hält an, wenn:**

| Fall | Was du tust |
|---|---|
| Wilma kommt an die Tranche nicht heran | nicht abhaken, anhalten, sagen woran es lag |
| `hk-lint` bleibt rot und der Befund verlangt ein Urteil | anhalten und vorlegen (§6.3) |
| Ein Kandidat trifft auf eine Notiz, deren Identität fraglich ist | anhalten. Raten ist der eine Fehler, den ein Durchlauf vervielfacht |
| Der Aufbau erweist sich als falsch geschnitten | anhalten, den Rest der Liste zur Korrektur vorlegen |
| Der Benutzer unterbricht | nichts weiter; der Stand steht in der Liste |

### Was am Ende steht

Wenn die letzte Tranche abgehakt ist, fehlt noch das, was erst über die ganze
Quelle zu sagen ist: der Abschnitt `# Kernaussagen` der Quellennotiz und der
Bericht nach Schritt ⑦, über den Lauf im Ganzen statt über eine Tranche.

Mit `--hkb` folgt der Import **erst dann** und folgt dem Skill `hkb-import`:
Die Urteile, die er verlangt, fällt ein Mensch, und ein Durchlauf fällt sie
nicht nebenbei mit. Danach steht in der Quellennotiz die Zusammenfassung
entlang des Aufbaus, verlinkt in den Bestand, und darunter die Tranchenliste
als Nachweis, welches Material gelesen wurde und wann. Welche Notizen dabei
entstanden sind, steht im Importnachweis der Bundle-Notiz.

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
- **Keinen Durchlauf ohne Anordnung.** Zwölf Tranchen kosten zwölf Läufe, und
  wer sie ungefragt startet, hat über fremde Mittel entschieden. Der
  Einzelschritt ist die Vorgabe.
- **Keine Angabe raten.** Was Wilma nicht gefunden hat, bleibt leer und wird
  gemeldet. Eine erfundene Jahreszahl in einer Zitation ist schlimmer als
  keine.
