---
name: bild
model: sonnet
description: "Ein einzelnes Bild über den Magnific-Connector erzeugen und in der Ablage ablegen, mit Vorgaben für Modell, Seitenverhältnis, Format, Zielordner, Name, Stil, Sprache und Referenzbild. Verwenden bei: erzeuge ein Bild von X, mach ein 16:9-Bild zu Y. Der Bildmotor hinter bild-notiz."
---

# Ein Bild erzeugen

Aus einem Prompt ein Bild über den Magnific-Connector erzeugen und in der
Ablage ablegen. **Der Skill trifft keine inhaltliche Entscheidung.** Der
Bildinhalt kommt fertig als `prompt` herein, der Stil als Baustein aus dem
Bildprofil.

## Voraussetzung

Der Magnific-Connector (auch Freepik) muss verbunden sein. Vor dem ersten
Schritt prüfen, ob `images_generate`, `creations_wait` und `creations_show`
verfügbar sind. Fehlt eines, **abbrechen und sagen warum**. Keine Ersatzwege
über andere Bildquellen suchen.

Ein Plugin kann diesen Connector nicht mitliefern. Er wird einmal eingerichtet
und gilt dann für die Sitzung.

Je nach Parameter kommen dazu: `folders_list` für `project`, `library_list`
für `character`, `creations_request_upload` und `creations_finalize_upload`
für ein Referenzbild, `simulate_cost` für gesetzte `resolution` oder `quality`.

## Parameter

Nur `prompt` ist Pflicht.

| Parameter | Vorgabe | Wofür |
|---|---|---|
| `prompt` | — | der Bildinhalt |
| `model` | `imagen-nano-banana-2-flash` | der Slug des Bildmodells |
| `aspect-ratio` | `16:9` | Seitenverhältnis |
| `format` | JPG | Dateiformat der Ablage |
| `target-folder` | `<media_base>/Images/Inbox` | Zielordner |
| `name` | — | Dateiname ohne Endung |
| `style` | das Profil der Wurzeldatei | Bildprofil |
| `project` | leer | Magnific-Projekt |
| `character` | leer | Magnific-Library-Character |
| `language` | `prompt` | Sprache der Bildtexte, oder `deutsch` |
| `reference` | leer | Pfad einer lokalen Vorlage |
| `reference-type` | `image` | `image`, `style` oder `composition` |
| `resolution`, `quality` | leer | höhere Werte kosten spürbar mehr |
| `count` | 1 | Zahl der Varianten |

**Der Modell-Slug wird immer gesetzt und nie leer gelassen.** Ein leeres `mode`
im Aufruf bedeutet `auto`, und der Dienst wählt dann ein Modell mit einer
anderen Bildgröße als die Parallelläufe am selben Kapitel. Am 20.08.2026 sind
so in einem Kapitel zwei Bilder mit 1376x768 und eines mit 2048x1152
entstanden.

`model: sonnet` im Frontmatter ist das ausführende Sprachmodell, nicht das
Bildmodell. Der Ablauf ist mechanisch und verlangt keine anspruchsvolle
Sprachleistung.

`name` ist kurz und sprechend, mit echten Umlauten und dem ASCII-Bindestrich
als einzigem Strichzeichen. Eine bestehende Datei wird nicht überschrieben,
bei Kollision kommt ein Suffix dazu.

## Ablauf

**① Connector prüfen.** Fehlt er, abbrechen.

**② Zielordner und Bildprofil holen.**

```bash
hk-ablage --bereiche
hk-kontext --bild
```

Das erste nennt `media_base`, das zweite den Stiltext. **Immer frisch
auflösen, nie aus dem Gedächtnis zitieren.** Ist `style` gesetzt, gilt das
genannte Profil statt des Vorgabeprofils.

**③ Prompt bauen.** Der übergebene `prompt`, eine Leerzeile, dann der
Stil-Baustein aus dem Profil. Bei einem Referenzbild die Änderung gegenüber
der Vorlage ausdrücklich benennen.

Spielt die Szene in einem Innenraum, kommt der Innenraum-Block des Profils
dazu. Ohne ihn baut das Modell den Raum gern als schwebenden Kubus mit offenen
Seiten auf leeren Grund. Bei Landschaften und Außenszenen entfällt er.

**③a Projekt auflösen**, falls `project` gesetzt: `folders_list(onlyProjects=true)`,
den Eintrag mit passendem Namen suchen, seine `reference` merken. Kein
Treffer: ohne weitermachen und knapp hinweisen.

**③b Character auflösen**, falls `character` gesetzt:
`library_list(type=character, search=<name>)`, die numerische `id` merken.
Kein Treffer: ohne weitermachen und knapp hinweisen.

**③c Sprache erzwingen**, falls `language` auf `deutsch` steht: nach dem
Stil-Baustein eine Leerzeile und `All text, labels and headings rendered
inside the image must be in German, regardless of the language of this prompt.
Use correct German umlauts.` Bei der Vorgabe `prompt` entfällt der Zusatz.

**③d Referenzbild hochladen**, falls `reference` gesetzt: Datei prüfen,
`creations_request_upload` mit passendem `mimeType`, die Bytes per
`curl -s -X PUT -H "Content-Type: <mime>" --data-binary @"<pfad>" "<url>"`
hochladen, HTTP 200 erwarten, `creations_finalize_upload` mit dem `path`
aufrufen, den `identifier` merken. Bei einer Personenreferenz den Stil
zurückhaltend dosieren, damit die Vorlage erkennbar bleibt.

**③e Kosten abschätzen**, falls `resolution` oder `quality` gesetzt sind:
`simulate_cost` vor der Generierung.

**④ Erzeugen.** `images_generate` mit `mode=<model-Slug>`,
`aspectRatio=<aspect-ratio>` und `count=<count>`, dazu `folderReference`,
`resolution` und `quality`, soweit vorhanden. In `references` kommen
`{type:"character", identifier:<id>}` und
`{type:<reference-type>, identifier:<upload-identifier>}`.

**⑤ Warten.** `creations_wait`, dann je Ergebnis die PNG-URL holen.

**⑥ Ablegen.** Jedes PNG nach `/tmp/` laden (`curl -sL`) und mit
`sips -s format <format> <png> --out "<target-folder>/<name>.<endung>"`
wandeln. Den Zielordner zuvor anlegen. Bei `count` über 1 einen Zähler
anhängen.

**⑦ Zeigen.** `creations_show` mit den Identifiern, damit die Bilder inline
erscheinen.

**⑧ Melden.** Je Datei ein Pfad-Link und eine knappe Beschreibung. Keine
internen Identifier nennen.

## Bekannte Fallstricke bei Referenzbildern

**Personen-Verdopplung.** Bei einer Personenreferenz neigt das Modell dazu,
die Person zu verdoppeln. Wenn genau eine gemeint ist, das im Prompt
erzwingen: `exactly one woman, only one person, no duplicate, no twin`.

**Falschtreffer des Filters.** Bei figurbetonten Referenzen blockt der Filter
gelegentlich grundlos. Dann neutraler formulieren (`tasteful, fully dressed,
refined editorial portrait`) und erneut starten.

**Freigestellte Vorlage bevorzugen.** Setzt die Anweisung die Person in eine
neue Szene, gewinnt die freigestellte Variante der Vorlage, nicht das Original
mit Hintergrund.

## Nicht tun

- Nicht ungefragt committen oder pushen. Der Zielordner ist Ablage, kein
  freigegebener Stand.
- Nicht nach Parametern fragen, für die eine Vorgabe existiert. Nur wenn
  `prompt` fehlt, wird nachgefragt.

## Abgrenzung

`bild-callout` schreibt die `> [!ai-image]`-Callouts, erzeugt aber keine
Bilder. `bild-notiz` ruft diesen Skill über alle Callouts einer Notiz auf und
bettet die Ergebnisse ein. `bild-cover` erzeugt das Hochformat-Cover eines
EPUB mit eigenem Modell und eigener Schablone.
