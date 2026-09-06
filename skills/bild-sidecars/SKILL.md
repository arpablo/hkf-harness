---
name: bild-sidecars
description: "Für alle Bilder eines Verzeichnisses die Metadaten-JSONs daneben erzeugen (Name, Alt-Text, Beschreibung, Tags), ohne die Bilder in diesen Kontext zu holen. Verwenden bei: Sidecars erzeugen, Metadaten für die Bilder in X, Bilder für die Bildablage vorbereiten."
---

# Bild-Sidecars erzeugen

Für jede Bilddatei entsteht eine gleichnamige `.json` daneben, im Format
`henni-image` Version 1.

**Die Bilder siehst du nie an.** Das erledigen Agenten vom Typ
[[../agents/bild-sidecar|bild-sidecar]], damit weder Bilddaten noch Bildlisten
in diesem Kontextfenster landen. Bei hundert Bildern ist das der Unterschied
zwischen einem Lauf und einer Sitzung, die danach nichts mehr kann.

## Ablauf

**① Kandidaten sammeln.** Ein Verzeichnis ist Pflicht:

```bash
hk-bilder <verzeichnis>
```

Optionen: `--no-recursive` (nur oberste Ebene), `--force` (auch Bilder mit
vorhandener Sidecar, zum Nachfüllen leerer Felder), `--batch-size N` (Vorgabe
5).

Das Werkzeug legt die Bildpfade in Batch-Dateien ab und gibt nur die
Zusammenfassung samt Batch-Pfaden aus. Die Zusammenfassung melden.

**② Die Batch-Dateien nicht öffnen.** Sie sind für die Agenten da. Wer sie
liest, hat den Zweck der Übung verfehlt.

**③ Je Batch einen Agenten starten**, alle Aufrufe in einer Nachricht, damit
sie nebeneinander laufen:

- `subagent_type`: `bild-sidecar`
- `prompt`: `Verarbeite die Bilder aus der Batch-Datei <absoluter pfad>.`
- `description`: `Sidecars Batch <nr>`

Bei mehr als acht Batches in Wellen von acht arbeiten und zwischen den Wellen
den Zwischenstand nennen.

**④ Ergebnis melden.** Geschriebene Sidecars und übersprungene Dateien mit
Grund. Gab das Werkzeug eine Konfliktliste aus, also zwei Bilddateien mit
gleichem Basename im selben Ordner, diese nennen. Solche Bilder brauchen erst
eindeutige Dateinamen, sonst teilten sie sich eine Sidecar.

## Grenzen

Erfasst werden `.jpg`, `.jpeg`, `.png`, `.webp`, `.avif`, `.gif`, `.tif` und
`.tiff`. SVG bleibt draußen.

`*.collection.json` sind Sammlungsdateien und keine Bild-Sidecars. Sie werden
nie als solche behandelt.

Ohne `--force` bleibt eine vorhandene Sidecar unberührt. Mit `--force` behält
der Agent `folderCover`, `coverFor`, `favorite`, `persona` und die vorhandenen
Tags. Gesetzt wird nur, was leer ist.

**Der Lauf schreibt ausschließlich `.json`-Dateien.** Keine Bilddatei wird
angefasst, nichts gelöscht, nichts umbenannt.

Das verbindliche Schema steht in der Definition des Agenten.
