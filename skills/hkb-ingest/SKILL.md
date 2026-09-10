---
name: hkb-ingest
description: "Aus einer Quelle eine Lieferung machen, in der die Quellennotiz sagt, was das Werk behauptet, und die Notizen den Beleg tragen. Die Thesen des Werks stehen fest, bevor die erste Zeile gelesen wird. Verwenden bei: Quelle einlesen, ein Buch erfassen, diese URL einlesen, ein Clipping verarbeiten, Ingest, Bundle aus einer Quelle bauen, weiterlesen."
---

# Aus einer Quelle eine Lieferung machen

Zuerst [[hkb]] lesen. Du bekommst eine Quelle und lieferst ein Bundle: die
Quellennotiz, die Notizen, die ihre Behauptungen tragen, `hbundle.md`, und
`hk-lint` sagt grün.

## Der Satz, aus dem alles Weitere folgt

> **Die These kommt vor der Notiz.**

Wer liest und dabei schreibt, kennt die Thesen des Werks noch nicht. Damit ist
die Frage, ob ein Gegenstand eine Notiz verdient, beim Schreiben gar nicht
entscheidbar. Wer nicht entscheiden kann, legt an. So entstanden aus 348
Buchseiten einmal 239 Notizen mit mehr Zeichen, als das Buch hatte.

Deshalb steht der Plan vor dem Lesen und das Lesen vor dem Schreiben, und
dazwischen liegt ein Journal, in das kein Fließtext passt.

## Der Maßstab

**Die Quellennotiz ist das Produkt.** Sie hat bestanden, wenn ein Leser nach
fünfzehn Zeilen weiß, was das Werk behauptet. Nicht, worüber es handelt. Was
es behauptet. Alles andere in der Lieferung ist Belegapparat.

**Angesammelt wird, was über das Werk hinaus gilt.** Eine Person, die in einem
Kapitel eine Funktion ausübt, ist eine Erwähnung und keine Notiz. Sie steht im
Fließtext, mit Namen und ohne Verweis. Wer wiederkommt und wessen Handeln eine
These trägt, bekommt ein Blatt.

**Ein Detail rechtfertigt sich durch die These, der es dient.** Ein Detail ohne
diese Aufgabe ist Ballast, gleich wie sicher es belegt ist.

**Die Lieferung ist um eine Größenordnung kleiner als der gelesene Text.** Wird
sie es nicht, ist etwas falsch, und zwar nicht am Ende, sondern am Anfang.

## Die Reihenfolge steht fest

> `hk-ingest` → **alva** plant → **berta** liest, so oft wie nötig →
> `hk-extrakt --gegenstaende` entscheidet → **edith** bestimmt →
> **cora** schreibt → **dina** setzt den Kopf → prüfen.

Den Stand führen die Werkzeuge und nicht dein Kontext. Nach jedem Schritt
liegt er auf der Platte, und `hk-extrakt <quellennotiz>` sagt jederzeit, wo der
Lauf steht. Ein Abbruch, eine Kompaktierung oder ein Sitzungswechsel kostet
darum nichts.

**Du liest die Quelle nie selbst.** Auch nicht kurz zur Kontrolle. Wandert sie
in deinen Kontext, zahlt jeder weitere Zug dafür.

## Ablauf

### ① Die Lieferung anlegen

```bash
hk-ingest
hk-ingest --bundle <ziel> --kind book --title T --url U
```

Ohne Argumente zeigt `hk-ingest`, was in der Inbox liegt, und schreibt nichts.
Er legt die Quellennotiz mit dem an, was sicher bekannt ist, und meldet die
Lücken. **Rate die Werkart nicht.** `--ausfertigung` hält fest, wo das
Original liegt, und kopiert nichts.

### ② Den Plan machen lassen

Starte `alva` mit der Quellennotiz und den Auszügen: Titelei,
Inhaltsverzeichnis, Einleitung, Schluss, Kapitelanfänge. Sie gibt Werkfrage,
fünf bis neun Thesen und die Lesestrecken zurück.

**Lies den Plan und urteile.** Das ist deine Arbeit an dieser Stelle. Steht da
ein Thema statt einer These, geht der Plan zurück. „Imperialismus" ist ein
Thema. „Die Aufteilung folgte den Ressortinteressen konkurrierender Behörden"
ist eine These, weil man sie bestreiten kann.

Ist die Quelle klein genug, dass ein Lauf sie ganz liest, bekommt `alva` und
`berta` derselbe Auftrag und der Plan trägt eine Strecke. Es gibt keine zweite
Betriebsart: Der Unterschied zwischen einem Buch und einer Webseite ist die
Zahl der Strecken.

### ③ Lesen lassen, so oft wie nötig

```bash
hk-extrakt <quellennotiz> --naechste
```

Das Werkzeug nennt die Strecke, die eine unbelegte These trägt. Starte `berta`
damit. Sie liest in ihrem eigenen Kontext und hängt ihre Karten selbst an.

Dann wieder `--naechste`. Der Lauf endet, wenn das Werkzeug meldet, dass keine
offene Strecke mehr eine unbelegte These trägt. **Nicht, wenn das Buch zu Ende
ist.** Eine ungelesene Strecke ist kein Mangel, sondern der Grund, warum das
hier bezahlbar ist.

Sieh zwischendurch auf `--stand`. Das Journal soll verdichten und nicht
mitwachsen. Meldet es die Marke von 300.000 Zeichen, brich ab und sag warum.

### ④ Entscheiden, wer ein Blatt bekommt

```bash
hk-extrakt <quellennotiz> --gegenstaende | hk-lesekarte <quellennotiz> --anlegen -
```

Die Schwelle ist zwei Thesen, oder in einer Thesenbehauptung genannt. Wer
darunter bleibt, wird Erwähnung und keine Notiz.

**Das ist ein Näherungsmaß, und du darfst streichen.** Aufnehmen darfst du nur,
wenn du die These benennst, der die Notiz dient. Trag sie dann mit
`hk-lesekarte --nachtragen` ein, damit sichtbar bleibt, dass sie nicht aus der
Schwelle kam.

### ⑤ Die Gegenstände bestimmen

Starte `edith` mit der Lesekarte. Sie schreibt für jeden Eintrag die
Gegenstandsschicht: was er unabhängig von dieser Quelle ist, mit
`wikidata_id`. Sie liest die Quelle nicht und belegt nichts.

Das ist zugleich die Wiedererkennung: Der Ingest kennt den Bestand nicht, also
muss die Lieferung Titel, `aliases` und `wikidata_id` mitbringen, damit der
Import eine Dublette findet.

### ⑥ Schreiben lassen

`cora`, ein Lauf je Ziel, in dieser Reihenfolge:

1. **Je These ein Lauf.** Sie holt sich `--these <id>` und schreibt zwei Zeilen
   unter `# Kernaussagen`: die Behauptung, und woran der Autor sie zeigt. In
   der Reihenfolge des Plans.
2. **Je Gegenstand ein Lauf.** Sie holt sich `--gegenstand <name>` und schreibt
   die Quellenschicht der Notiz, die `edith` angelegt hat.

Dann `dina` für den Kopf: die Frage des Werks, die Antwort mit ihren
Mechanismen, und aus `--grenzen` der Abschnitt `# Was die Quelle offenlässt`.

**Schreib die Notizen nicht selbst.** Nicht weil du es nicht könntest, sondern
weil ein Lauf nach zwanzig Werkzeugaufrufen die Schreibregeln aus dem
Gedächtnis holt statt aus der Ablage.

### ⑦ Den Nachweis und die Prüfung

```bash
hk-extrakt <quellennotiz> --strecken | hk-tranchen <quellennotiz> --anlegen -
hk-lint <lieferung>
hk-text --gate <lieferung>
hk-import --check <lieferung>
```

Der Plan liegt unter `AgentDashboard/` und reist nicht mit. Ohne den ersten
Schritt weiß nach dem Import niemand mehr, welcher Teil des Werks gelesen
wurde. Hak danach die gelesenen Tranchen mit `hk-tranchen --abhaken` ab.

## Wann du anhältst und fragst

Der Lauf entscheidet selbst und berichtet am Ende. Er hält bei fünf Dingen an,
und nur bei diesen:

1. Zwei Gegenstände könnten derselbe sein.
2. Die Quelle widerspricht sich an einer tragenden Stelle.
3. Eine These lässt sich mit dem Gelesenen nicht decken, und die Nachforderung
   wäre teuer.
4. Ein Typ fehlt, den die Lieferung bräuchte.
5. Die Quelle sagt etwas, das eine Festlegung dieser Ablage verletzt.

Alles andere entscheidest du und schreibst es in den Schlussbericht.

## Der Schlussbericht

Am Ende sagst du in wenigen Zeilen: die Werkfrage, welche Thesen gedeckt sind
und welche nicht, wie viele Strecken gelesen und wie viele übergangen wurden.
Dazu, wie viele Notizen entstanden sind und wie groß die Lieferung gegen den
gelesenen Text ist. Die letzte Zahl ist die wichtigste.

## Was hier schon einmal nicht funktioniert hat

**Je Tranche lesen und sofort schreiben.** Zwei Durchgänge an derselben Quelle,
der zweite mit mehr Lektüre als der erste, brachten ein Konzept weniger. Mehr
Lesen bringt mehr Namen und nicht mehr Erklärung, solange die Thesen nicht
zuerst feststehen.

**Ein Destillat als Prosa weitergeben.** Was frei formuliert werden darf,
wächst. Darum sind die Karten auf feste Felder mit Zeichengrenzen begrenzt,
und `hk-extrakt` weist einen ganzen Stapel ab, wenn eine Zeile ausschert.

**Die Zusammenfassung dem Aufbau der Quelle folgen lassen.** Wer ein Buch nach
Kapiteln referiert, hat es nicht verstanden. Eine solche Notiz besteht
`hk-lint`, aber sie sagt niemandem, was das Werk behauptet.

**Parallele Läufe.** Sie kaufen Wanduhr und kosten Token. Die Laufzeit ist
frei, ein Buch darf über Nacht laufen.

## Nicht tun

- Die Quelle nicht selbst lesen, auch nicht auszugsweise.
- Keine Notiz vor Schritt ⑥ anlegen, auch keinen Entwurf.
- Keine Notiz für einen Gegenstand, der die Schwelle nicht genommen hat und
  für den du keine These benennen kannst.
- Den Plan nicht während des Lesens umschreiben. Fehlt eine These, ist das
  Haltegrund 3.
- Nichts committen und nichts publizieren.
