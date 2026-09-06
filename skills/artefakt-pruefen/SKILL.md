---
name: artefakt-pruefen
description: "Ein einzelnes Artefakt gegen Mechanik, Stimme und Kanon prüfen und die Befunde nach Schwere übergeben, ohne den Text selbst zu ändern. Verwenden bei: prüf das mal, Schlussprüfung, ist das freigabereif."
---

# Ein Artefakt prüfen

Ein fertiges oder halbfertiges Artefakt gegen die geltenden Regeln prüfen und
die Befunde so übergeben, dass die verantwortliche Rolle sie abarbeiten kann.
**Der Skill bewertet, er ändert den Text nicht.**

## Geltungsbereich

Ein Artefakt ist ein einzelner Gegenstand mit Text: eine Notiz, eine
Geschichte, ein Kapitel, eine Lieferung vor dem Export. Ein ganzer Bestand ist
kein Artefakt. Dafür läuft `hk-text` über ein Verzeichnis.

## Die drei Ebenen

**① Mechanik.** Zeichen, Umlaut-Ersatzformen, Verbotswörter, Satzlänge. Diese
Ebene wird nicht gelesen, sondern gemessen:

```bash
hk-text --gate <pfad>
```

Die Befundliste kommt unverändert in den Bericht. **Wer hier nach Gefühl
urteilt, erzeugt eine zweite Wahrheit neben dem Prüfer.**

**② Stimme.** Das Profil, das die Wurzeldatei nennt, zu holen mit
`hk-kontext --stimme`. Ein Satz kann mechanisch sauber und trotzdem gegen die
Stimme sein. Diese Ebene ist Urteil und lässt sich nicht messen.

**③ Kanon.** Figuren, Orte, Fakten, Typregeln und Pflichtfelder der Ablage.
Ein stilistisch sauberer Satz ist falsch, wenn er den Kanon bricht. In einer
Wissensbasis prüft `hk-lint` das Formale davon, und bei Erzählprosa
`hk-kontinuitaet` die Zeiträume und die Kanonlisten.

Die eigene Leistung liegt auf ② und ③. Ebene ① wird eingesammelt und
weitergereicht.

Welche Ebenen greifen, entscheidet der Auftrag. Ein Lektorat prüft Stimme und
Kanon, eine Schlussprüfung zusätzlich die Mechanik.

## Ablauf

**① Gegenstand bestimmen.** Was für ein Artefakt, welcher Typ, welche Stimme,
welche Kanonblätter sind einschlägig.

**② Den Text ganz lesen, bevor der erste Befund entsteht.** Eine Stichprobe
übersieht die Muster, auf die es ankommt, und die Muster sind der Grund, warum
ein Mensch das nicht selbst macht.

**③ Je Ebene prüfen.** Jeder Befund nennt die Stelle, die verletzte Regel, die
Schwere und eine konkrete Umschreibung oder Streichung. Ein Befund ohne
Vorschlag ist eine Meinung.

**④ Nach Defekt, Warnung und Beobachtung ordnen.** Ein Defekt blockiert die
Freigabe, eine Beobachtung nicht.

**⑤ Übergeben.** An die Rolle, die abarbeitet. Der Skill setzt nichts um,
sofern der Auftrag es nicht ausdrücklich vorsieht.

## Grenzen

**Kein stillschweigendes Ändern.** Wer prüft und zugleich schreibt, kann
hinterher nicht mehr sagen, was am Text falsch war.

**Keine erfundenen Befunde**, damit eine Prüfung ergiebig aussieht. Ein
sauberer Text bekommt einen kurzen, klaren Bescheid ohne Befunde.
