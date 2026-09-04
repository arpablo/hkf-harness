---
name: hkb-hinweis
description: "Festhalten, was für diese eine Wissensbasis gilt: wann eine Notiz entsteht, welche Quellen zählen, wie weit zusammengefasst wird. Verwenden bei: merk dir das, das gilt hier immer, Regel für diese Ablage, Kurationspolitik, Hinweis anlegen, Feedback festhalten."
---

# Was für diese Ablage gilt

Zuerst [[hkb]] lesen.

HKF Core beschreibt das Format, nicht den Gebrauch. Wann in **dieser**
Wissensbasis etwas eine eigene Notiz wert ist, welche Quellen als belastbar
gelten, wie weit zusammengefasst werden darf: Das gehört zu dieser einen
Ablage und zieht mit ihr um.

Also eine gewöhnliche Notiz vom Typ `hint`, unter `Hints/`. Sie ist dann
Inhalt wie jeder andere, versioniert, verlinkbar und prüfbar. Und sie besteht
die Probe, an der sich hier alles messen lassen muss: Ein Mensch, der die
Ablage ohne KI führt, hat denselben Nutzen davon.

**Der Sitzungskontext liest sie.** Was in `Hints/` steht, liegt zu Beginn
jeder Sitzung vor und geht dem gemeinsamen Kanon vor, wo es ihn berührt. Ein
Hinweis ist damit das Gedächtnis dieser Ablage.

## Wann einer entsteht

Wenn eine Festlegung künftig gelten soll und sich nicht aus der Spezifikation,
den Typdefinitionen oder dem Bestand ableiten lässt. Was der Typ ohnehin
zusichert, gehört in seine Typdefinition und nicht hierher.

Eine einmalige Beobachtung ist kein Hinweis. Eine Korrektur, die der Benutzer
ausgesprochen hat, schon.

## Ablauf

1. **Prüfen, ob es ihn schon gibt.** `hk-suche --typ hint` zeigt den Bestand.
   Deckt ein vorhandener dieselbe Sache ab, wird er fortgeschrieben. Ein
   widerlegter Hinweis wird gelöscht und nicht ergänzt.
2. **Anlegen** nach [[hkb-notiz]], mit `applies_to`, wenn er nur für einen Typ
   gilt. Ohne `applies_to` gilt er für die ganze Ablage.
3. **Den Grund hinschreiben.** Der Body sagt in einem Satz, was gilt, und
   danach, warum. Der Grund wiegt schwerer als die Regel: Ein Hinweis ohne ihn
   lässt sich später weder prüfen noch aufheben.
4. **Relative Zeitangaben in Daten wandeln.** „Seit letzter Woche" ist in einem
   Jahr nicht mehr lesbar.

## Maschinenlesbar, wo es geht

Ein Hinweis darf einen `json`-Block mit dem Schlüssel `writing_policy` tragen.
Dann gilt er auch für `hk-text`, und ein Verstoß wird gemessen statt bemerkt. Der Basissatz des Harness bleibt daneben gültig,
die beiden werden verrechnet.

## Grenzen

Kein Hinweis für das, was die Spezifikation ohnehin regelt. Keine erfundene
Herkunft. Ein Hinweis, dessen Gültigkeit offen ist, wird als offen geschrieben
und nicht als Tatsache.
