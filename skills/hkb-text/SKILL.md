---
name: hkb-text
description: "Einen deutschsprachigen Text prüfen und heben: die harten Regeln messen, die weichen Muster beurteilen, die Stimme und den Kanon der Ablage prüfen. Verwenden bei: Text prüfen, überarbeiten, humanisieren, KI-Muster entfernen, Schreibregeln, vor der Freigabe, klingt nach KI."
---

# Einen Text prüfen und heben

Zuerst [[hkb]] lesen.

Drei Ebenen, und nur die erste lässt sich messen.

| Ebene | Womit | Wer urteilt |
|---|---|---|
| Mechanik | `hk-text` | das Werkzeug |
| Muster | die Cluster-Regel unten | du |
| Stimme und Kanon | das Profil der Sitzung, die `hint`-Notizen | du |

## Ebene 1: messen, nicht lesen

```bash
hk-text <datei|verzeichnis>       # Bericht, endet immer mit 0
hk-text --gate <datei>            # endet mit 1, sobald ein Fehler auftritt
hk-text --rhythm <datei>          # Rhythmus-Signale als JSON
```

Die Befundliste kommt unverändert in den Bericht. **Wer hier nach Gefühl
urteilt, erzeugt eine zweite Wahrheit neben dem Prüfer.** Ein Fehler
blockiert, eine Warnung nicht.

Ein Verstoß gegen die harten Regeln hält beim Schreiben ohnehin an, dafür
sorgt der Hook. Der Bericht ist trotzdem der Anfang: Er zeigt auch die
Warnungen, die niemanden aufhalten.

## Ebene 2: die Cluster-Regel

Harte Regeln gelten im Einzelfall. Weiche Muster gelten erst in der Häufung:
Ein einzelnes Signal ist kein Grund umzuschreiben, mehrere unabhängige schon.

Fünf Durchgänge, in dieser Reihenfolge, und ein späterer macht einen früheren
nicht wieder zunichte.

1. **Typografie und Belege.** Die harten Befunde abarbeiten. Keine Stilarbeit.
   Ein fehlender Beleg wird markiert und nicht spekulativ gefüllt.
2. **Wortwahl.** Verstärker, Schaufenstervokabular, mechanische Übergänge,
   Füllformeln, Pseudo-Verben statt `ist`, Abstrakta. Ein Hypernym wird nur
   dort aufgelöst, wo der konkrete Sachverhalt im Text belegt steht.
3. **Struktur.** Schematische Schlussabschnitte, Zusammenfassungsmarker,
   Listen mit fett gesetzten Inline-Überschriften, Stichpunkte statt Prosa,
   mechanischer Fettdruck, Title Case in Überschriften. Erst danach steht die
   Absatzstruktur.
4. **Rhythmus.** Aus den Signalen von `--rhythm`: das Vorfeld rotieren,
   höchstens etwa zwei von drei Sätzen mit dem Subjekt beginnen, die Satzlänge
   spreizen, höchstens ein mechanischer Konnektor je Absatz. Nicht auffüllen,
   sondern Sätze teilen oder zusammenziehen.
5. **Selbstprüfung.** Erzeugt die Überarbeitung neue Monotonie, etwa dieselbe
   Ersatzkonstruktion dreimal? Ist eine Quelle, eine Erfahrung oder ein
   Faktenanker dazugekommen? Sind Zahlen, Namen, Zitate, Wikilinks und
   Frontmatter unversehrt?

## Ebene 3: Stimme und Kanon

Ein Satz kann mechanisch sauber und trotzdem gegen die Stimme sein. Die Stimme
steht im Sitzungskontext, die Festlegungen dieser Ablage in ihren
`hint`-Notizen. Ein stilistisch sauberer Satz ist falsch, wenn er dem Kanon
widerspricht.

## Leitplanken

**Nichts erfinden.** Keine Quelle, keine Erfahrung, keine Anekdote. Zahlen,
Namen, Daten, Zitate und Verweise vor und nach jeder Änderung abgleichen.
Substanz wird nie gekürzt.

Saubere Grammatik und ein Fachbegriff sind kein KI-Muster. Zitate, Code und
Spezifikationstext werden nicht stilistisch umgeschrieben.

**Ist der Text sauber, sag das und hör auf.** Ein sauberer Text bekommt einen
kurzen Bescheid, keine konstruierten Mängel.

## Der Bericht

Nie den ganzen Text, nur die geänderten Stellen.

1. Was gemessen wurde, eine Zeile mit den Zahlen aus `hk-text`.
2. Die gefundenen Muster, höchstens sechs, je mit kurzem Zitat und Regelbezug.
3. Vorher und Nachher, nur für die bearbeiteten Passagen.
4. Was übrig bleibt, höchstens drei Punkte, oder „nichts gefunden".

## Herkunft

Die Durchgänge, die Cluster-Regel, die Selbstprüfung und der Verzicht auf eine
Volltextausgabe sind abgeleitet aus `humanizer-de` in der Fassung 4.0.2 von
Martin Moeller (MIT, https://www.martin-moeller.biz), einer deutschen
Ableitung von https://github.com/blader/humanizer.
