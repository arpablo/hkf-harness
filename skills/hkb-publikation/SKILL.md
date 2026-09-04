---
name: hkb-publikation
description: "Aus Texten einer Wissensbasis eine Publikation bauen: den Container anlegen, Texte in eine Lesereihenfolge bringen, den Stand prüfen. Verwenden bei: Publikation anlegen, Sammlung, Buch zusammenstellen, Kapitel einsortieren, Reihenfolge ändern, Inhaltsverzeichnis."
---

# Eine Publikation führen

Zuerst [[hkb]] lesen.

Eine Wissensbasis kann veröffentlichen, was in ihr steht. Dafür gibt es zwei
Typen, und sie sind nicht Teil der Grundausstattung: Eine Ablage, die nichts
veröffentlicht, soll sie nicht tragen.

```bash
hk-import <harness>/bundles/hkf-publikation
```

Danach kennt die Ablage `text` und `publication`.

Die Typen liegen unter `output_base`, dem fünften Bereich (Core §3.2.4), nach
Vorgabe `60-Output`. Ein Erzeugnis ist gemacht und nicht gewusst: Es beruft
sich auf den Bestand, und der Bestand beruft sich nicht auf es.

## Die drei Typen

Ein **`text`** ist ein Stück Prosa, das für sich steht. Es gibt genau einen
Texttyp. Ob ein Stück als Kapitel gelesen wird, entscheidet die
Lesereihenfolge seiner Publikation und nicht der Text selbst. Eine Trennung in
Einzelstück und Kapitel trüge zwei Verzeichnisse, zwei Vorlagen und zwei
Abläufe für denselben Gegenstand.

Ein **`essay`** behauptet etwas. Das unterscheidet ihn von einer Wissensnotiz,
die sagt, was der Fall ist, und von einem `text`, der erzählt. Er darf sich
irren, und er muss sagen, worauf er sich stützt.

Eine **`publication`** sagt, was dazugehört und in welcher Reihenfolge. Sie
trägt selbst keinen Fließtext des Werkes.

## Die Reihenfolge

```bash
hk-publikation <notiz>                       # zeigt sie
hk-publikation <notiz> --aufnehmen <text>    # hängt hinten an
hk-publikation <notiz> --vor <t> --nach <u>  # stellt t vor u
hk-publikation <notiz> --entfernen <text>    # nimmt heraus
hk-publikation <notiz> --check               # prüft den Stand
hk-publikation <notiz> --richten             # zieht ihn gleich
```

Die Reihenfolge steht an drei Stellen: in `contents` der Publikation, im
Abschnitt `# Inhalt` ihres Body, und in `publications` jedes Textes.
**Schreib keine davon von Hand.** Das Werkzeug hält sie gleich, und `--check`
sagt, wenn sie auseinandergelaufen sind.

`contents` ist die einzige Liste des Formats, bei der die Reihenfolge etwas
bedeutet. Wer sie umsortiert, ändert das Werk.

## Ablauf

1. **Die Publikationsnotiz anlegen** nach [[hkb-notiz]]. Titel, Untertitel,
   wer sie verantwortet, und im Body, was sie zusammenhält.
2. **Die Texte schreiben oder finden.** `hk-suche --typ text` zeigt, was schon
   da ist. Für eine Erstfassung gibt es den Agenten `marlene`.
3. **Aufnehmen**, in der Reihenfolge, in der gelesen werden soll.
4. **`--richten`**, wenn du fertig bist. Das zieht die Rückverweise nach und
   schreibt `words` an jeden Text.
5. **`hk-lint`**, wie nach jedem Schreibvorgang.

## Was das Werkzeug nicht entscheidet

**Die Reihenfolge.** Sie ist eine Aussage über das Werk, und ein Programm hat
dazu nichts zu sagen. Wenn du nicht weißt, wohin ein Text gehört, frag nach.

**Ob ein Text dazugehört.** Ein Stück, das thematisch passt, gehört deshalb
noch nicht in die Sammlung.

## Daraus ein Werk machen

```bash
hk-buch <publikation>          # das Manuskript als eine Datei
hk-epub <publikation> --neu    # daraus ein EPUB, mit vorherigem Neubau
```

`hk-buch` schreibt die Texte in der Reihenfolge aus `contents` in eine Datei
**außerhalb der Ablage**, unter `$HKF_ARTEFAKTE/<name der ablage>/`, Vorgabe
`~/hkf-artefakte`. Mit einem Kopf, den `pandoc` liest. Das
Frontmatter der Texte, ihr `# Siehe auch` und der `# Inhalt` der Publikation
fallen weg, die Überschriften rücken eine Ebene tiefer. Eingebettete Bilder
werden zu Pfaden, die `pandoc` auflöst.

**Der Text wird dabei nicht geglättet.** Was gegen die Schreibregeln verstößt,
wird gemeldet und bleibt stehen. Ein Bauschritt, der still am Text ändert,
macht aus dem Manuskript etwas anderes als das, was in der Ablage steht. Wer
das Manuskript sauber will, räumt vorher in den Texten auf, mit `hk-text` und
[[hkb-text]].

`hk-epub` braucht `pandoc`. Fehlt es, sagt der Lauf das und bricht ab, statt
mitten im Bau zu scheitern. Das Titelbild kommt aus `cover`.

Beides sind Artefakte und keine Notizen. Sie lassen sich jederzeit neu bauen
und tragen nichts, was nicht schon in den Notizen steht. Darum liegen sie
nicht in der Ablage.

## Grenzen

`contents` ist eine flache Folge. Ein Werk mit Teilen, die wieder Kapitel
enthalten, lässt sich damit nicht abbilden. Solange niemand es braucht, bleibt
es dabei.
