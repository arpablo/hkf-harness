---
hkf: "1.0"
type: bundle
id: hkf-erzaehlung
title: Erzählbestand
description: Sieben Typen für eine Wissensbasis, die Erzählprosa führt. Texte in Publikationen, dazu Figuren, Schauplätze, Motive, Requisiten und die Beurteilung, die neben dem Text steht.
version: "2026-09-04"
---

Diese Lieferung ist die erzählende Fassung von `hkf-publikation`. Sie enthält deren beide Typen und erweitert `text` um das, was eine Reihe zusammenhält: die Erzählperspektive, den Zeitraum der Handlung und die Verweise auf das, was wiederkehrt.

**Importiere entweder diese Lieferung oder `hkf-publikation`, nicht beide.** Beide führen `text` und `publication`, und zwei Fassungen desselben Typs verlangen bei jedem Import eine Bedeutungsprüfung, deren Antwort immer dieselbe wäre.

```bash
hk-import <pfad-zu-dieser-lieferung>
```

Der Zuschnitt kommt aus einem Vault, der ihn über zwei Jahre gebaut hat. Zwei Entscheidungen daraus wiegen schwerer als der Rest.

**Es gibt genau einen Texttyp.** Ob ein Stück als Kapitel gelesen wird, entscheidet die Lesereihenfolge seiner Publikation. Eine Trennung in Einzelstück und Kapitel trug zwei Verzeichnisse, zwei Vorlagen und zwei Abläufe für denselben Gegenstand, und jede Aufnahme in eine Reihe verlangte eine Umwidmung.

**Ein Blatt entsteht beim zweiten Auftritt.** Eine Figur, ein Motiv oder ein Requisit, das einmal vorkommt, braucht keine Notiz. Wer diese Schwelle nicht zieht, füllt die Ablage mit Namen, über die nichts weiter zu sagen ist.

# Typen

| Typ | Verzeichnis | Zweck |
|---|---|---|
| assessment | Assessments | Das Urteil über einen Text, getrennt von ihm geführt, mit einem Abschnitt je Prüfer. |
| beat | Beats | Eine wiederkehrende Geste, Wendung oder Szene, die über mehrere Texte hinweg dieselbe bleibt. |
| character | Characters | Ein Mensch, der in mehreren Texten vorkommt und über sie hinweg gleich bleiben soll. |
| location | Locations | Ein Ort, an dem gespielt wird und dessen Beschaffenheit über mehrere Texte gleich bleiben soll. |
| prop | Props | Ein Gegenstand, der in mehreren Texten vorkommt und dabei derselbe bleiben soll. |
| publication | Publications | Eine Folge von Texten in einer festgelegten Lesereihenfolge. |
| text | Texts | Ein Stück Prosa, das für sich steht. |
