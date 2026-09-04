---
name: hkb-suche
description: "Eine Frage gegen eine Wissensbasis beantworten: die Notizen finden, sie lesen, die Antwort aus ihnen bilden und mit Verweisen belegen. Verwenden bei: was steht in der Wissensbasis zu, frag die Ablage, Recherche, wer verweist auf, welche Notizen gibt es zu."
---

# Eine Frage gegen die Wissensbasis beantworten

Zuerst [[hkb]] lesen.

Die Antwort entsteht aus dem, was in der Ablage steht, und wird mit Verweisen
belegt. Was nicht dasteht, wird nicht ergänzt, sondern benannt.

## Suchen

```bash
hk-suche <muster>                     # Volltext über Frontmatter und Body
hk-suche --typ person                 # alle Notizen eines Typs
hk-suche <muster> --typ event         # beides zusammen
hk-suche --hat wikidata               # Notizen mit dieser Property
hk-suche --verweist-auf <notiz>       # wer auf diese Notiz zeigt
hk-suche <muster> --fundstellen       # die getroffenen Zeilen
```

**Grase nicht das Dateisystem ab.** `hk-suche` kennt die Bereiche, die Typen
und die Verweise. Ein `grep` über die Ablage findet auch Vorlagen, Medien und
Beispiele in Codeblöcken.

Ohne Treffer endet der Lauf mit 1. Das heißt „nichts gefunden" und nicht
„nicht gelaufen".

## Ablauf

1. **Einstieg finden.** Mit `hk-suche` die Notizen bestimmen, bevor du eine
   liest. Findet die Suche nichts, prüfe Schreibvarianten und Aliase. Erst
   danach ist die Aussage „dazu steht hier nichts" belegt.
2. **Lesen.** Die Treffer ganz lesen und den Verweisen darin folgen, soweit
   sie zur Frage gehören. Eine Trefferliste ist kein Beleg.
3. **Den Rand abtasten.** `--verweist-auf` zeigt, was auf eine gefundene Notiz
   zeigt. Dort steht oft der Zusammenhang, den die Notiz selbst nicht nennt.
4. **Antworten.** Knapp, im Ton der Sitzung, mit qualifizierten Verweisen als
   Belegstellen. Was die Ablage nicht hergibt, wird als offen benannt und
   nicht aus dem Modellwissen ergänzt. Wenn doch, steht dabei, dass es von
   außen kommt.

## Wenn die Antwort etwas wert ist

Eine Antwort, die einen Zusammenhang herstellt, den bisher keine Notiz trägt,
ist selbst eine Notiz wert. Typisch `concept` für einen Sachverhalt,
`comparison` für eine Gegenüberstellung, `topic` für einen Einstieg. Dafür
gilt [[hkb-notiz]].

**Das ist keine Pflicht.** Eine Antwort, die nur wiederholt, was schon in
einer Notiz steht, wird keine zweite.

## Grenzen

Der Volltext ist eine Zeichensuche und kein Verständnis. Sie findet, was
dasteht, nicht was gemeint ist. Bei einem Begriff, der anders heißen könnte,
suche mit mehreren Begriffen, bevor du eine Fehlanzeige meldest.
