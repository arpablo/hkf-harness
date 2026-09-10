---
title: Ingest, was ich verstanden habe
status: zur Abnahme
date: 2026-09-10
---

# Ingest: was ich verstanden habe

Diese Datei sagt, was ich glaube tun zu sollen. Sie enthält keinen Entwurf und
keine Architektur. Sie ist zur Abnahme da: Was hier falsch steht, wird
korrigiert, bevor irgendetwas gebaut wird.

## 1. Der Zweck

Aus einer Quelle soll eine **belegte Erklärung dessen werden, was das Werk
sagt**, und nicht eine Sammlung der Namen, die darin vorkommen.

Zwei Fragen müssen danach beantwortbar sein:

- **Wer oder was kommt vor?** Eine Person, ein Ereignis, eine Organisation
  bekommt ihre Notiz mit den Aussagen der Quelle.
- **Was erklärt das Werk, und wie?** Die zentrale Frage des Autors, seine
  Begriffe, seine Kausalketten, seine Grenzen, belegt und ihm zugeschrieben.

Die zweite Frage ist die, an der der heutige Ablauf scheitert. Der Beleg dafür
steht im Bestand: Die Fromkin-Lieferung führt 53 Personen und 47 Ereignisse,
aber 9 Konzepte und 3 Begriffe, und keinen davon zu Imperialismus,
Kolonialismus oder Nationalismus. Die Wörter kommen in 14, 9 und 6 Notizen
vor, aber kein Lemma trägt sie. Der Stoff ist verstreut, nicht erklärt.

## 2. Was am Ende dasteht

Ein **importierbares HKF-Bundle**: `hbundle.md`, die Quellennotiz, die
abgeleiteten Notizen, die nötigen Typ- und Property-Definitionen. Kein
Patchsatz, keine lose Sammlung.

Fertig heißt: `hk-lint`, `hk-text --gate` und `hk-import --check` sind grün,
und die Lieferung sagt selbst, welcher Teil der Quelle gelesen wurde und
welcher nicht.

## 3. Woran ich den Erfolg messe

| Maßstab | Prüfbar woran |
|---|---|
| Die Werkfrage ist beantwortet | `# Kernaussagen` sagt, was der Autor erklärt, nicht was vorkommt |
| Die tragenden Begriffe sind erklärt | Ein Begriff, der die These trägt, hat eine Notiz mit seiner Verwendung im Werk |
| Jede Aussage hat ihren Ort | Behauptung, Mechanismus, Fundstelle |
| Die Grenzen stehen da | Was die Quelle nicht hergibt und wo sie spekuliert, ist benannt |
| Nichts ist erfunden | Keine Behauptung ohne Grundlage, keine geglättete Uneinigkeit |
| Der Bestand wächst zusammen | Eine vorhandene Notiz wird fortgeschrieben, nicht gedoppelt |

## 3a. Der Maßstab, an dem alles gemessen wird

Festgelegt am 10.09.2026 nach der Prüfung von `fromkin-neu`.

### Die Quellennotiz ist das Produkt

**Sie hat bestanden, wenn ein Leser nach fünfzehn Zeilen weiß, was das Werk
behauptet.** Nicht, worüber es handelt. Was es behauptet.

Alles andere in der Lieferung ist Belegapparat. Die Entitätsnotizen tragen die
Fundstellen, an denen sich die Behauptung prüfen lässt. Sie sind nicht das
Ergebnis.

Der heutige Stand besteht das nicht. `fromkin-neu/Sources/a-peace-to-end-all-peace.md`
misst 43.101 Zeichen über 195 Zeilen und referiert 34 Kapitel, je in ein bis
drei Sätzen. Kapitel 5 lautet vollständig: „Das Porträt Churchills im Jahr
1914 und sein Weg zur Admiralität." Von 331 Wikilinks führen 9 zu einem
Konzept, also zwei von hundert zu etwas, das erklärt. Ein Abschnitt
`# Kernaussagen` fehlt ganz, obwohl die ältere Fassung vom 03.09. neun
kausale Thesen trug.

**Eine Zusammenfassung, die dem Aufbau der Quelle folgt, ist der Fehler und
nicht die Form.** Wer ein Buch nach Kapiteln referiert, hat es nicht
verstanden. Wer es verstanden hat, sagt zuerst die These und benutzt die
Kapitel danach als Beleg.

### Die Hauptthesen stehen namentlich da

Die Notiz nennt die Thesen des Werks, jede mit dem, was sie aussagt, und dem,
woran der Autor sie zeigt. Nicht die Themen, die er berührt, sondern die
Sätze, für die er einsteht, mit dem Mechanismus dahinter.

Der Kopf der Notiz trägt in dieser Reihenfolge:

1. **Die Frage des Werks.** Ein Satz.
2. **Die Antwort.** Ein Absatz, mit den Mechanismen, die sie tragen.
3. **Die Hauptthesen einzeln**, je eine Zeile Behauptung und eine Zeile,
   woran der Autor sie zeigt.
4. **Wo die Erklärung dünn wird.** Was der Autor selbst offenlässt.

Erst danach der Aufbau des Werks, und der ist Apparat.

### Wissen, nicht Daten

**Angesammelt wird, was über das Werk hinaus gilt.** Nicht, wer darin
vorkommt.

Der heutige Stand besteht das nicht. `fromkin-neu` führt **239 Notizen mit
zusammen 1.191.587 Zeichen aus sechs von zwölf Tranchen**, darunter 138
Personen bei einer mittleren Größe von 3.702 Zeichen. Gedeckt sind rund 348
Buchseiten, also grob 870.000 bis 1.044.000 Zeichen Text. **Die Lieferung ist
größer als das, woraus sie stammt.**

Daraus folgen zwei Prüfsteine:

| Prüfstein | Maß |
|---|---|
| **Verdichtung** | Die Lieferung ist um mindestens eine Größenordnung kleiner als der gelesene Text. Heute: Faktor 1. Ziel: Faktor 10. |
| **Schwelle je Notiz** | Eine Notiz entsteht, wenn über ihren Gegenstand etwas gilt, das über seine Rolle in diesem einen Werk hinausreicht. |

Eine Person, die in einem Kapitel eine Funktion ausübt, ist eine Erwähnung und
keine Notiz. Sie steht im Fließtext der Quellennotiz, mit Namen und ohne
Verweis. Wer wiederkommt und wessen Handeln eine These trägt, bekommt ein
Blatt.

**Ein Detail rechtfertigt sich durch die These, der es dient.** Zahlen, Daten
und Namen gehören dorthin, wo sie eine Behauptung stützen. Ein Detail ohne
diese Aufgabe ist Ballast, gleich wie sicher es belegt ist.

## 4. Die Rahmenparameter, wie ich sie verstehe

**Kosten.** Ein Buch muss in **ein Nutzungsfenster des Max-Plans** passen,
also in fünf Stunden Kontingent. Die Zahl dahinter ist nicht veröffentlicht und
hängt vom Modell ab, deshalb bindet der Entwurf sich an eine Herleitung statt
an eine Zahl.

Für Fromkin, 686 Seiten zu rund 2.750 Zeichen, also 1,89 Mio Zeichen:

| | |
|---|---:|
| Untergrenze, das Buch einmal lesen | 472 k Token |
| heutiger Preis, hochgerechnet aus `fromkin-neu` | rund 10 Mio Token |
| Verhältnis | 22 zu 1 |

**Fünfundneunzig Prozent der heutigen Kosten entstehen nicht beim Lesen.** Sie
entstehen daraus, dass aus 1,0 Mio Zeichen Text 1,19 Mio Zeichen Notizen
werden. Die Hochrechnung benutzt das gemessene Verhältnis von 4,31 Token je
Ausgabezeichen und gilt als Größenordnung, nicht als exakte Zahl.

**Zielmarke: rund 1,5 Mio Token für ein Buch dieser Größe.** Das ist die
Untergrenze plus das Zehnfache an Verarbeitung, und es folgt aus dem
Verdichtungsprüfstein: Fällt die Ausgabe um Faktor 10, fällt der Preis mit ihr.
Ein Entwurf, der darüber liegt, wird verworfen und nicht nachgebessert.

Für eine mittlere Quelle bleibt es bei der Marke aus `hkb-ingest.md`:
höchstens 116.870 Token für 41.637 Zeichen. Der gemessene Referenzlauf lag bei
233.739.

**Zeit.** Eine Arbeitseinheit soll in fünf Minuten enden. Gemessen: Der
Lesezug lag bei 3:27, der Schreiblauf bei 18:42.

**Kostentreiber.** Nicht die Größe des Kontexts, sondern die Zahl der
Werkzeugaufrufe: 2 Aufrufe kosteten 39k, 49 Aufrufe kosteten 194k. Dazu der
feste Aufbau je Agentenlauf und die Größe dessen, was zwischen zwei Kontexten
übergeben wird.

**Die harte Untergrenze.** Wer ein Werk ganz liest, zahlt mindestens seinen
Textumfang einmal als Eingabe. Für ein Buch von 895 Seiten sind das grob
400.000 Token, gleich welcher Aufbau. Ersparnis ist danach nur noch bei allem
möglich, was **nach** dem Lesen kommt, oder dadurch, dass ein Teil ungelesen
bleibt.

**Fortsetzbarkeit.** Nach jeder Einheit steht der Stand auf der Platte. Eine
Fortsetzung liest den offenen Rest und nicht den Verlauf.

**Quellenarten.** Buch als PDF, mittlere Fachquelle, Webseite. Dazu laut
Werkarten des Harness Transkript, Podcast, Video, Aufsatz.

**Sprache.** Die Quellen sind überwiegend englisch, die Notizen deutsch.

## 5. Was ich als gesetzt annehme

- Das Zielformat ist ein HKF-Bundle nach Core §4.
- Die vorhandenen Werkzeuge in `bin/` bleiben die Grundlage, wo sie passen.
  Was fehlt, wird gebaut, nicht in einem Prompt nachgebildet.
- Was ein Skript entscheiden kann, entscheidet kein Modell.
- Ein Zwischenergebnis geht als Datei weiter, nie als Chat-Antwort.
- Die Wissensbasis bleibt ohne KI benutzbar.

## 6. Entschieden am 10.09.2026

| Frage | Entscheidung |
|---|---|
| Lesetiefe | **Gezielt, mit Nachforderung.** Ein billiger Orientierungslauf setzt die Werkfragen. Analytisch gelesen wird, was sie trägt. Offene Fragen lösen gezielte Nachlesungen aus, bis die Frage gedeckt ist oder als nicht deckbar gilt. |
| Bestand | **Isoliert.** Der Ingest kennt die vorhandenen Notizen nicht. Der Abgleich geschieht beim Import. |
| Automatik | **Halt nur bei echten Urteilen.** Der Lauf entscheidet selbst und hält an, wo eine Entscheidung nicht ableitbar ist. |
| Budget | **Token binden, Laufzeit ist frei.** Ein Buch darf über Nacht laufen. |

### Was daraus folgt

**Parallelität entfällt.** Sie kauft Wanduhr und kostet Token. Wenn die
Laufzeit frei ist, gibt es keinen Grund, zwei Läufe gleichzeitig zu starten.
Ein Lauf wird nur dann geteilt, wenn sein Kontext sonst zu groß und damit zu
teuer würde. Die Fünf-Minuten-Vorgabe aus `hkb-ingest.md` ist damit kein Ziel
mehr, sondern höchstens eine Faustregel für die Größe einer Leseeinheit.

**Das Lesen wird nachfragegesteuert.** Nicht das Buch bestimmt, was gelesen
wird, sondern die Werkfrage. Der Orientierungslauf sieht Titelmaterial,
Inhaltsverzeichnis, Einleitung, Schluss und Kapitelanfänge, also wenige
Prozent des Umfangs. Alles Weitere wird angefordert, nicht abgearbeitet.

**Das Extrakt muss dauerhaft liegen bleiben.** Eine Nachforderung kommt später
und darf nicht zum erneuten Lesen führen. Was einmal gelesen wurde, wird
einmal extrahiert und nie wieder aus der Quelle geholt. Das ist die einzige
harte Regel, die aus dem Budget folgt.

**Wiedererkennung wandert in die Lieferung.** Weil der Ingest den Bestand
nicht kennt, muss das Bundle die Mittel mitbringen, mit denen der Import eine
Dublette erkennt: Titel, `aliases` und, wo es sie gibt, `wikidata_id`.

**„Echtes Urteil" braucht eine abschließende Liste.** Woran der Lauf anhält,
und woran nicht, muss vorher feststehen, sonst hält er entweder nie oder
dauernd. Mein Vorschlag für die Liste:

1. Zwei Gegenstände könnten derselbe sein.
2. Die Quelle widerspricht sich selbst an einer tragenden Stelle.
3. Eine Werkfrage lässt sich mit dem Gelesenen nicht decken, und die
   Nachforderung wäre teuer.
4. Ein Typ fehlt, den die Lieferung bräuchte.
5. Die Quelle sagt etwas, das eine bestehende Festlegung der Ablage verletzt.

Alles andere entscheidet der Lauf und berichtet es am Ende.

## 7. Was noch zu bestätigen ist

**Die Größe des Nutzungsfensters.** Die Zielmarke von 1,5 Mio Token ist aus
der Verdichtung abgeleitet und nicht aus dem tatsächlichen Kontingent. Sobald
die Zahl feststeht, wird sie hier eingetragen. Liegt das Fenster darunter, muss
der Entwurf schärfer werden, liegt es darüber, bleibt die Marke trotzdem
stehen: Sie folgt aus dem Maßstab und nicht aus dem Kontingent.
