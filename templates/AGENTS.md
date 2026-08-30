<!-- Vorlage für die AGENTS.md einer Wissensbasis.

     Ein Werkzeug erzeugt daraus die Datei neben der Wurzeldatei: Kopf und
     Typtabelle kommen aus `hkb.md`, wörtlich übernommen werden nur die
     Regeln und der letzte Abschnitt über die Medienverzeichnisse. Kopf
     und Tabelle unten
     stammen aus der Beispiel-Wissensbasis und werden nicht verwendet; sie
     stehen hier, damit die Vorlage für sich lesbar bleibt.

     Die erzeugte Datei gehört dem Werkzeug, nicht der Ablage — die
     .gitignore hält sie aus der Versionierung. -->

# Wissensbasis

Eine Wissensbasis im Format **HKF Core 1.0**. Einstieg ist `hkb.md`; dort
steht unter `spec` auch, wo die geltende Spezifikation zu lesen ist. Zeiten
gelten in `Europe/Berlin`.

## Sieben Regeln, bevor du etwas änderst

1. **Der Pfad bestimmt den Typ.** Eine Notiz gehört zu dem Typ, unter dessen
   Verzeichnis sie liegt; `type` im Frontmatter muss dazu passen.
2. **Erfinde keine Properties.** Was ein Typ zusichert, steht in
   `typedefs/<typ>.md`. Lies die Datei, bevor du ein Feld setzt.
3. **Verweise in Notizen sind qualifizierte Wikilinks mit Alias.** Das Ziel
   ist der vollständige Pfad ab der Vault-Wurzel ohne `.md`: das Verzeichnis,
   in dem diese Datei liegt, dann das Typverzeichnis, dann der Dateiname.
   Dahinter `|` und der Anzeigetext, in der Regel der `title` des Ziels. In
   einer Tabellenzelle wird der Strich als `\|` maskiert. Diese Datei und
   `hkb.md` verweisen dagegen relativ zu sich selbst, also ohne den ersten
   Abschnitt.
4. **Frontmatter bleibt flach.** Nur Text, Liste, Zahl, Checkbox, Datum,
   Datum mit Uhrzeit. Keine verschachtelten Abbildungen, keine leeren Werte.
5. **Wenn du änderst, schreib es hin.** `modified` auf jetzt **in UTC**,
   `modified_by` auf deinen Modellnamen. UTC, weil ein Import allein an
   `modified` entscheidet, welche Fassung die jüngere ist — Ortszeit ist
   dafür nicht vergleichbar. Ereigniszeiten wie `starts_at` bleiben Ortszeit.
6. **`typedefs/` und `proptypes/` sind tabu.** Sie gehören zur
   Grundausstattung oder kommen aus einem Bundle. Eigene Typen legst du
   daneben.
7. **`# Siehe auch` wird ergänzt, nicht gekürzt.** Der Abschnitt steht am Ende
   einer Notiz; jede Zeile ist ein Verweis, ein ` — ` und der Grund, warum er
   dasteht. Du darfst Zeilen hinzufügen — mit Grund —, aber keine entfernen:
   Entfernen ist Sache eines Menschen. Ein Ziel, das in `rejected_links`
   steht, verlinkst du nicht.

## Typen dieser Wissensbasis

| Typ | Verzeichnis | Zweck |
|---|---|---|
| typedef | typedefs | Registriert einen Typ und legt sein Verzeichnis fest. |
| proptype | proptypes | Schränkt eine Wertform ein. |
| bundle | bundles | Beschreibt eine Lieferung. |
| person | persons | Ein Mensch. |
| organisation | organisations | Eine Körperschaft: Unternehmen, Institut, Verein, Behörde. |
| place | places | Ein geographischer Ort. |
| event | events | Ein Geschehen zu einer bestimmten Zeit. |
| source | sources | Eine zitierbare Quelle: Buch, Aufsatz, Webseite, Vortrag. |
| term | terms | Ein definierter Begriff. |
| topic | topics | Ein Themengebiet als Einstiegspunkt. |
| note | notes | Eine Notiz ohne spezifischeren Typ. |
| specification | specifications | Ein normatives Dokument, an das sich die Wissensbasis hält. |
| maschine | maschines | Vorläufig beim Import von babbage-maschinen angelegt; keine Typdefinition geliefert. |

Mediendateien liegen unter `media/` in `images`, `videos`, `audios` oder
`documents` — Verweise darauf behalten die Dateiendung.

## Hinweise

<!-- Dieser Abschnitt bleibt bei einer Neuerzeugung erhalten. -->

Noch keine.
