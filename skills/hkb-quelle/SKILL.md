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

**Die Zahl ist eine Beobachtung und kein Soll.** Wie viele Notizen aus einer
Quelle entstehen, sagt die Quelle und nicht dieser Skill. Eine Aufforderung,
auf fünf bis fünfzehn zu kommen, erzeugt genau die Notizen, für die es keinen
Grund gibt. Was einen Grund hergibt, steht unter „Wann eine Notiz entsteht".

**Eine Lieferung mit nur einer Quellennotiz ist in aller Regel eine
unfertige Lieferung.** Die Quellennotiz sagt, was gelesen wurde; sie ist der
Beleg, nicht das Ergebnis. Das Ergebnis sind die Begriffe, Konzepte, Personen
und Vergleiche, die daraus in den Bestand wachsen — und die Verweise, mit
denen sie am Bestand hängen. Wer nur zusammenfasst, hat die Quelle abgelegt,
nicht eingelesen.

**Wofür aufbereitet wird.** Nicht zum Wiederlesen der Quelle. Später greift
jemand darauf zu, ein Mensch oder ein Modell, und fragt nach einem Gegenstand
und nicht nach einem Kapitel. Was dann trägt, ist eine Notiz, die sagt, was ihr
Gegenstand ist, mit welchen anderen er zusammenhängt und was welche Quelle über
ihn behauptet. Ein Destillat, das der Gliederung des Werks folgt, beantwortet
nur Fragen, die schon wissen, in welchem Kapitel die Antwort steht.

Diese Notizen gehören **in die Lieferung**. Dafür braucht es keine
Wissensbasis: Ein Bundle trägt Notizen jedes Typs, und wohin sie kommen,
entscheidet erst der Import (§4.3).

## Die Reihenfolge steht fest

> `hk-ingest` → **Wilma** liest → **Marlene** schreibt → du entscheidest und fügst zusammen.
>
> Bei einer großen Quelle je Tranche einmal, geführt von `hk-tranchen`.

Erst das Mechanische: kopieren oder nicht, `sha256`, die Quellennotiz mit dem,
was sicher bekannt ist, und eine Liste der Lücken. Dann liest **Wilma** die
Quelle und gibt ein belegtes Destillat zurück. Dann schreibt **Marlene** die
Notizen daraus. Das ist „erst `bin/`, dann `skills/`" auf einen einzelnen Lauf
angewandt.

**Warum das Schreiben ebenso delegiert wird wie das Lesen.** Wilma bekommt
einen eigenen Kontext, damit die Quelle nicht in deinen wandert. Marlene
bekommt einen, damit nichts anderes in ihren wandert: Wer eine Notiz nach
zwanzig Werkzeugläufen, drei Commit-Botschaften und einer Spezifikationsdebatte
schreibt, holt die Schreibregeln aus dem Gedächtnis statt aus der Ablage und
schleppt die Gewohnheiten der letzten Aufgabe mit. Marlene liest `hk-kontext`,
[[hkb-notiz]] und die Typdefinition, bevor sie den ersten Satz schreibt. Deine
Aufgabe bleibt das Urteil: welcher Kandidat eine Notiz wird, was in die
Quellennotiz gehört, und ob das Ergebnis trägt.

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

**⑥ Eintragen — dann die Entitäten.** Geh Wilmas `## Notiz-Kandidaten`
**einzeln** durch und gib jedem Kandidaten eine der drei Behandlungen
`create_or_extend`, `link_if_exists` oder `context_only`. Sie stehen unten,
zusammen mit der Frage, an der sie sich entscheiden. Diese Entscheidung ist
deine.

**Geschrieben wird von `marlene`, nicht von dir.** Gib ihr **den Pfad zum
Destillat** statt der abgeschriebenen Blöcke, dazu die Namen ihrer Gruppe, den
Zielpfad und die Zitierform. Sie liest die Blöcke selbst, und dein Kontext
bleibt frei.

**Wenige große Läufe statt vieler kleiner.** Ein Lauf trägt eine ganze Gruppe,
und eine Tranche kommt mit zwei bis drei Läufen aus. Jeder Lauf kostet einen
eigenen Kontextaufbau, und dreißig Einzelläufe kosten dreißigmal davon. Sie liest die
Schreibregeln, [[hkb-notiz]] und den `# Aufbau` des Typs selbst und prüft mit
`hk-text --gate`, bevor sie meldet. Was sie schreiben soll, ist unten
beschrieben, und sie kennt es aus ihrem eigenen Auftrag:

1. **Bestimmen.** Was *ist* der Gegenstand? Der erste Absatz beantwortet das,
   bevor irgendetwas aus der Quelle erzählt wird: was für ein Ding er ist, wann
   und wo er bestand, wofür er einsteht. Wilmas Zeile `Ist:` ist das Material,
   und was du ohnehin in `description` schreibst, gehört ausformuliert auch in
   den Text. Dann Typ wählen und die Typdefinition lesen — die
   Property-Tabelle, bevor du ein Feld setzt, und den `# Aufbau`, der sagt,
   welche Fragen eine Notiz dieses Typs beantwortet und in welcher Reihenfolge.
   Dazu `aliases` aus den Benennungen der Quelle.
2. **Verknüpfen.** Mit welchen anderen Entitäten hängt er zusammen, und wie?
   Die Verweise stehen in der Prosa, wo der Text sie hergibt; was nicht aus dem
   Text hervorgeht, kommt unter `# Verbindungen` und in `related` (§5.6). Eine
   Entität ohne Verknüpfung ist eine Sackgasse: Wer später sucht, findet sie
   nur, wenn er ihren Namen schon kennt.
3. **Behaupten.** Was sagt **diese Quelle** über ihn? Das steht hinter der
   Bestimmung, mit Fundstelle und der Quelle zugeschrieben. Die Trennung ist
   der Zweck der Übung: Was der Gegenstand ist, gilt unabhängig davon, wer
   darüber geschrieben hat. Was ein Werk behauptet, gehört diesem Werk. Wer
   beides vermischt, schreibt ein Kapitelreferat unter einem Lemma.
4. **`sources` setzen** — die Verbindung, an der der Bestand später hängt.

### Zwei Schichten, und nur eine davon wird belegt

Eine Notiz muss **für sich lesbar** sein. Wer sie öffnet, ohne die Quelle zu
kennen, muss verstehen, worum es geht. Dafür trägt sie zwei Schichten:

**Das Allgemeinwissen schreibst du selbst, und zwar unbelegt.** Was die
Dardanellen sind, wo sie liegen, was sie verbinden: Das steht in jedem
Nachschlagewerk und braucht keine Fundstelle. Ohne diese Schicht ist die
zweite unverständlich, und die Notiz hängt an einer einzigen Quelle. Gibt es
einen Wikipedia-Artikel, nimm ihn als Grundlage und setze `wikidata_id`.

**Belegt wird, was die Quelle beiträgt.** Das Spezifische, das Strittige, die
Deutung, die Zahl, das Zitat. Dort steht die Fundstelle, und dort gehört sie
hin.

Die Grenze verläuft nicht zwischen „aus der Quelle" und „nicht aus der
Quelle", sondern zwischen **allgemein zugänglich** und **spezifisch**. Ein
Beleg ist kein Selbstzweck. Er sagt, wem eine Aussage gehört, die nicht jedem
gehört.

**Was die Quelle beiträgt, wird zeitlich verortet.** „Durch die Meerengen
gingen 50 Prozent des russischen Exports" ist ohne Jahr eine Behauptung über
die Gegenwart. Sie galt vor 1914. Ein Beleg ersetzt keine Zeitangabe.

**Erfunden wird trotzdem nichts.** Bist du dir beim Allgemeinwissen nicht
sicher, sieh nach oder lass es weg. Eine Lücke ist besser als eine geratene
Jahreszahl.

**Gibt es die Notiz schon, wird sie erweitert und nicht ersetzt.** Eine zweite
Quelle über denselben Gegenstand ist der Normalfall, nicht die Ausnahme: Die
Bestimmung bleibt stehen und wird höchstens genauer, die Verknüpfungen kommen
hinzu, und die Behauptungen der neuen Quelle treten neben die der alten, jede
der ihren zugeschrieben. In einer Lieferung leistet das `extends` (siehe
unten).

**Widerspricht die neue Quelle der alten, gewinnt keine von beiden.** Ein
Widerspruch zwischen zwei Werken ist eine Auskunft über den Gegenstand und
kein Fehler, den der Ingest wegräumt. Steht er für sich, wird er eine
`comparison`, deren `compares` auf beide Quellennotizen zeigt und die die
strittigen Punkte als Dimensionen führt. Ist er klein, steht er als solcher in
der Notiz. Überschrieben wird er nie.

### Die Zitierform trägt über Quellen hinweg

Ein Beleg nennt **Verfasser, Jahr und Stelle**: `(Fromkin 1989, S. 79)`, und
wo eine Ausfertigung keine gedruckten Seiten hat, `(Fromkin 1989, Kap. 7)`.
Kapitel sind ausgabenunabhängig, Seiten eines PDF-Exports nicht.

Der Grund steht in der Zukunft dieser Notiz: Sobald eine zweite Quelle
dasselbe Lemma berührt, muss der Leser sehen, welche Aussage wem gehört. Ein
Beleg wie `(Kap. 7, PDF 79)` sagt das nicht und wird beim Zusammenführen
wertlos. Die vollständigen Angaben stehen in der Quellennotiz, im Text steht
der Kurzbeleg.

**⑦ Berichten.** `hk-lint <ziel>` und `hk-lint --strict <ziel>` müssen grün
sein. Dann sag:

- was in der Lieferung liegt, nach Typ,
- **welche Kandidaten welche Behandlung bekommen haben** — die beiden ohne
  eigene Notiz nach Gruppen und mit dem Grund, nicht als Zahl. Das ist der
  Ort, an dem eine Entscheidung über einen Kandidaten festgehalten wird:
  Kommt er in einer späteren Tranche wieder, behält er seine Behandlung,
  statt neu erwogen zu werden,
- **welche Notizen ohne Bestimmungssatz blieben**, weil die Quelle ihn nicht
  hergibt — sie warten auf eine zweite Quelle,
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

**Der Body wird nicht umbrochen** — ein Absatz ist eine Zeile. Eine
Zusammenfassung über zwölf Teile ist der Ort, an dem sich ein harter Umbruch am
teuersten rächt: In Obsidian wird daraus ein Stapel kurzer Zeilen, und ein
Wikilink über einen Umbruch löst dort nicht auf. Der Abschnitt dazu steht in
[[hkb-notiz]].

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
   **Einmal je Tranche, nicht je Notiz.** Ein Lauf über die Lieferung sagt
   dasselbe wie dreißig Läufe über einzelne Dateien und kostet ein
   Dreißigstel. Dasselbe gilt für `hk-text`: Der Gate gehört ans Ende eines
   Schreibdurchgangs, nicht zwischen zwei Absätze.
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

### Drei Behandlungen, und jede wird begründet

Ein Kandidat bekommt genau eine davon:

| Behandlung | Wann sie gilt | Was daraus folgt |
|---|---|---|
| `create_or_extend` | Der Gegenstand trägt eine eigene Frage oder Erklärung, die auch außerhalb dieser Quelle etwas erklärt. | Seine Notiz entsteht oder wird fortgeschrieben. |
| `link_if_exists` | Er hilft dem Zusammenhang, rechtfertigt aber keine eigene Notiz. | Gibt es die Notiz schon, wird dorthin verlinkt. Sonst geschieht nichts. |
| `context_only` | Die Erwähnung erklärt eine Szene, ein Zitat, eine Nebenbemerkung. | Sie bleibt in der Quellennotiz oder im Fließtext stehen. |

**Über die Behandlung entscheidet die Rolle für die Frage der Quelle und nicht
der Bekanntheitsgrad.** Churchill kann in einem Buch über die Dardanellen ein
unverzichtbarer Bezugspunkt sein oder eine dekorative Nennung. Beide Male
heißt er Churchill. Was die beiden Fälle trennt, ist die Frage, ob das Werk
ohne ihn eine andere stellte. Dass ein Name im Text vorkommt, sagt darüber
nichts, und dass ein Leser ihn kennt, erst recht nicht.

**Die Gegenprobe für `create_or_extend`:** Nenne in einem Halbsatz die Frage
oder die Erklärung, die dieser Gegenstand trägt. Geht das nicht, ist es keine,
und der Kandidat gehört in eine der beiden anderen Behandlungen.

Drei Fälle, die regelmäßig vorkommen und in denen die Antwort feststeht:

| Fall | Behandlung |
|---|---|
| Er ist ein **Bestandteil** eines größeren Gegenstands der Quelle | `create_or_extend`, aber für den größeren Gegenstand. Der Bestandteil wird ein Abschnitt in dessen Notiz. |
| Er ist eine **Aufzählung** ohne eigenen Begriff dahinter, etwa „zwölf Prüfungen" oder „dreizehn Kennzahlen" | `context_only` |
| Die Quelle nennt ihn nur **im Vorbeigehen** | `link_if_exists` |

**Eine Erwähnung ist noch kein Arbeitsauftrag.** Eine Notiz über einen
Gegenstand, zu dem die Quelle nichts zu sagen hatte, ist teurer als keine. Sie
steht danach im Bestand und behauptet allein dadurch, dass es hier etwas zu
wissen gibt.

Das ist keine Aufforderung, sparsam zu sein. Oben steht, dass eine Lieferung
mit nur einer Quellennotiz unfertig ist, und beides gilt: je Kandidat eine
Behandlung, und je `create_or_extend` ein Grund.

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
