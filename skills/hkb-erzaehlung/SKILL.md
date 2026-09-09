---
name: hkb-erzaehlung
description: "Eine Wissensbasis führen, die Erzählprosa enthält: Figuren, Schauplätze, Motive und Requisiten als Kanon, den Zeitraum als Kontinuität, die Beurteilung neben dem Text. Verwenden bei: Geschichte schreiben, Figur anlegen, Kanon prüfen, Text überarbeiten, Motiv, Kontinuität, Beurteilung."
---

# Einen Erzählbestand führen

Zuerst [[hkb]] lesen.

Eine Wissensbasis kann Erzählprosa führen. Was dabei zusammenhält, sind nicht
die Texte, sondern das, was zwischen ihnen gleich bleibt.

```bash
hk-import <harness>/bundles/hkf-erzaehlung
```

Sieben Typen: `text` und `publication` wie in `hkf-publikation`, dazu
`character`, `location`, `beat`, `prop` und `assessment`. **Importiere entweder
diese Lieferung oder `hkf-publikation`, nicht beide.**

## Die Schwelle

**Ein Blatt entsteht beim zweiten Auftritt.** Eine Figur, ein Motiv oder ein
Requisit, das einmal vorkommt, braucht keine Notiz. Beim ersten Mal steht der
Name als bloßer Text in der Liste, ohne Verweis. Wer wiederkommt, braucht ein
Blatt, weil sich sonst niemand merkt, wie er beim ersten Mal war.

Bei einem Schauplatz zählt etwas anderes: Er bekommt ein Blatt, sobald zwei
Texte sich darin bewegen und ein Leser merken würde, dass die Küche einmal
links und einmal rechts liegt.

**Wer die Schwelle nicht zieht, füllt die Ablage mit Namen, über die nichts
weiter zu sagen ist.**

## Die Kontinuität

```bash
hk-kontinuitaet              # was auseinandergelaufen ist
hk-kontinuitaet --richten    # die abgeleiteten Listen nachziehen
```

Drei Prüfungen. Der Zeitraum aus `story_date` und `story_end`: Zwei Texte, die
denselben Tag belegen, sind ein Befund, weil eine Figur beides an einem Tag
schaffen muss. Die Listen `characters`, `locations`, `beats` und `props`: Sie
folgen aus dem Body und werden nicht daneben gepflegt. Und die Beurteilungen,
deren Lesedatum älter ist als der Text.

**Nachgezogen werden allein die Listen.** Ob eine Überschneidung im Zeitraum
Absicht ist, entscheidet ein Mensch.

## Einen Text heben

Für die Mechanik gilt [[hkb-text]]. Was hier dazukommt, ist die Frage, warum
ein Stück nicht trägt.

**Zuerst die Frage, ob es die Arbeit wert ist.** Der Grenznutzen fällt steil.
Ein Stück, das weit unten steht, gewinnt mehrere Notenpunkte, ein fast fertiges
einen. Wer ein gelungenes Stück weiter poliert, arbeitet an der falschen
Stelle, und das gehört gesagt, bevor der erste Satz geändert wird. Führt die
Ablage eine Beurteilung je Text, steht der benannte Abzug dort und sagt, wo der
Eingriff ansetzt.

**Ein Text, der an einer Kette hängt, ist ein eigener Fall.** Ein Kapitel in
einer Publikation trägt Voraussetzungen aus dem vorigen und Zusagen an das
nächste. Was dort geändert wird, wird gegen die Nachbarn geprüft und nicht
gegen den Text allein.

**Diagnose vor Eingriff.** Fünf Fragen, in dieser Reihenfolge. Die erste, die
mit Nein oder mit Nichts beantwortet wird, ist die Ursache. Weitersuchen lohnt
erst danach.

1. **Was steht auf dem Spiel, und was kostet der Ausgang konkret?** Ein Preis
   muss benennbar sein. Zwanzig Minuten Verspätung sind keiner.
2. **Hat das Gegenüber eine eigene Logik, oder liefert es Stichworte?** Wer
   scheitert, muss vorher fast durchkommen. Ohne einen Moment echter Kompetenz
   ist der Sieg wertlos.
3. **Bleibt die Hauptfigur sauber, und gibt der Text ihr recht?** Das ist der
   häufigste Befund. Die starken Stücke sind die, in denen sie selbst etwas
   falsch macht oder etwas verliert.
4. **Trägt ein einzelnes Muster die Szene allein?** Dann braucht das Stück eine
   zweite Achse, die ohne dieses Muster läuft.
5. **Erklärt der Text nach der Pointe noch einmal, was sie bedeutet?** Nachlauf
   ist der billigste Abzug und der leichteste Eingriff.

**Der Einsatz kommt aus Material, das schon im Text liegt.** Das ist die
tragende Regel und der Grund, warum die geglückten Überarbeitungen keine neue
Handlung erfunden haben. Gesucht wird die Nebensache, die zur zweiten Achse
taugt, nicht die Ergänzung, die fehlt.

Die zweite Achse beginnt vor dem Auftritt des Gegenübers und geht nach ihm
weiter. Der Preis wird eine Zahl, die ein Leser mitrechnen kann. Die
Hauptfigur handelt, statt zu reagieren. Und die Gegenfigur bekommt eine eigene
Rechnung statt einer Kontrastfunktion.

**Gegen die eigene Arbeit geprüft**, bevor der Text zurückgeht:

- Lässt sich der Preis in einem Satz mit einer Zahl sagen? Wenn nicht, ist die
  zweite Achse nicht eingezogen.
- Stand jedes Element der neuen Achse schon im alten Text? Wenn nicht, benenne
  die Erfindung ausdrücklich.
- Beginnt der Einsatz der Hauptfigur vor dem Auftritt des Gegenübers?
- Kommt die Note aus dem Text und nicht aus dem Auftrag?
- Ist der Umfang gleich geblieben oder gesunken? Eine Überarbeitung, die
  dreihundert Wörter zulegt, hat meist erklärt statt gezeigt.

## Der Nachzug

Ein Eingriff endet nicht am Text. Danach:

1. `hk-text <datei>` und `hk-lint`.
2. `hk-kontinuitaet --richten`, wenn Figuren, Orte oder Motive dazugekommen
   sind.
3. Jede neue Figur, jedes neue Motiv gegen die Schwelle prüfen: zweiter
   Auftritt oder nicht.
4. Widerspricht der Text einem Blatt, ist das eine Entscheidung. Entweder
   ändert sich der Text, oder das Blatt ändert sich und sagt, ab wann.
5. Die Beurteilung fortschreiben, mit neuem Lesedatum. Was beim letzten Mal
   galt und heute behoben ist, bleibt lesbar.
6. `hk-publikation --richten`, wenn der Text in einer Publikation steht.

## Die Rollen

Der Agent `frida` schreibt die Erstfassung eines erzählenden Textes, `herta`
lektoriert sie. Für analytische Texte stehen daneben `marlene` und `astrid`. Wer
den falschen Auftrag bekommt, gibt ihn zurück, statt in der fremden Stimme zu
arbeiten.

Der Agent `doris` liest den Bestand als Ganzes und schreibt eine Agenda. Nur sie
sieht, was über viele Texte hinweg passiert, und sie schreibt genau eine Datei.
Das ist der Grund, warum man sie laufen lassen kann.

**Wie eine Ablage ihre Rollen zuschneidet, steht in ihren `hint`-Notizen und
nicht im Agenten.** Welcher Zweig eines Bestandes noch verfolgt wird, in welchem
Rhythmus eine Agenda entsteht, wie lang sie werden darf: Das ist eine Festlegung
dieser Ablage (siehe `hkf:hkb-hinweis`). Ein Agent, der so etwas eingebaut hat,
taugt für genau eine Ablage.

## Was nicht geklappt hat

**Schreib auf, was schiefgegangen ist.** Ein Verfahren, das nur seine Erfolge
kennt, wiederholt seine Fehler. In der Vorlage dieses Skills sind drei
Anläufe gescheitert, und jedes Mal stimmte die Diagnose, während der Eingriff
danebengriff. Ein zweiter Handlungsstrang wurde erfunden statt gefunden. Ein
Preis wurde beschrieben statt beziffert. Ein Nachlauf wurde gekürzt statt
gestrichen.

Solche Sätze gehören in eine `hint`-Notiz der Ablage (siehe [[hkb-hinweis]]),
nicht in den Kopf des Nächsten, der es versucht.
