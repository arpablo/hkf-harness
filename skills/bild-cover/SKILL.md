---
name: bild-cover
model: sonnet
description: "Ein Hochformat-Coverbild für eine Publikation erzeugen, mit Titel, Autor und Verlag im Bild, und es dort ablegen, wo hk-epub es findet. Verwenden bei: Cover erzeugen, Coverbild für die Publikation, E-Book-Cover bauen."
---

# Ein Cover erzeugen

Aus einer Publikationsnotiz einen Cover-Prompt bauen, das Bild über
[[bild]] erzeugen und so ablegen, dass `hk-epub` es findet.

**Die eigene Leistung ist der Prompt, nicht die Mechanik.** Stilauflösung,
Projektwahl, Kostenabschätzung, Generierung und Konvertierung stehen in
[[bild]] und werden hier nicht wiederholt.

## Eingaben

Der Name der Publikation, mit oder ohne `Pub - `. Wahlweise ein gewünschtes
Motiv, wenn eine Richtung vorgegeben ist.

## Ablauf

**① Namen normalisieren.** `Pub - ` und `.md` entfernen.

**② Publikation lesen.** Die Notiz liegt unter `output_base` im Verzeichnis
des Typs `publication`:

```bash
hk-ablage --bereiche
```

Zu erfassen: `title`, `subtitle`, `summary`, `author`, `publisher`, `rights`,
`cover_title`, `cover_subtitle`, `cover_author`, `cover_publisher`,
`cover_image`, `tags` sowie die Kapitelüberschriften. Aus der Struktur das
zentrale Motiv ableiten.

**Leere Cover-Felder fallen auf die bibliografischen zurück:** `cover_title`
auf `title`, `cover_subtitle` auf `subtitle`, `cover_author` auf `author`,
`cover_publisher` auf `publisher`.

**③ Prompt bauen.** Englisch, nach der Schablone unten. Den Stil-Baustein
nicht selbst anhängen, das macht [[bild]].

Ein gutes Cover zeigt ein zentrales Symbol oder eine verdichtete Szene des
Themas. Es trägt genau den Cover-Titel, die Autorenzeile und den Verlag,
sonst kein Wort. Es funktioniert im Hochformat und bleibt in der Palette des
Bildprofils. Dekorative Stillleben-Requisiten, die nicht aus dem Thema kommen,
bleiben draußen.

**④ Erzeugen** über [[bild]]:

| Parameter | Wert |
|---|---|
| `prompt` | der Cover-Prompt |
| `model` | `gpt-2` |
| `aspect-ratio` | `2:3` |
| `resolution` | `2k` |
| `quality` | `high` |
| `format` | JPG |
| `target-folder` | `<media_base>/Images/Covers` |
| `name` | `Cover - <Name>` |
| `count` | 1, oder 4 auf Wunsch |

**Nicht das Vorgabemodell.** Bei einem typografischen Cover ist exakter Text
wichtiger als Szenenkohärenz, und `gpt-2` setzt Schrift zuverlässiger.
`resolution` und `quality` stehen hier hoch, anders als bei Kapitelbildern:
Ein Cover wird groß angesehen und einmal erzeugt.

Liefert der Dienst PNG statt JPG, ist das zulässig. `hk-epub` erkennt `.jpg`,
`.jpeg`, `.png` und `.webp`.

**Bei Varianten** legt [[bild]] alle mit Zähler-Suffix ab. Nach der Sichtung
durch einen Menschen die gewählte Datei auf `Cover - <Name>.jpg` umbenennen
und die übrigen löschen. Nur dieser eine Dateiname wird gefunden.

**⑤ Prüfen.** Datei vorhanden, Hochformat, Titel und Autor und Verlag lesbar,
keine zusätzlichen Fantasiewörter, Motiv passend, Stil wie im Profil.

**⑥ Melden.** Den Pfad nennen.

## Prompt-Schablone

```text
Create a vertical ebook cover image for a German book about <theme>.
The exact cover text must be:
Title: "<cover_title>"
Subtitle: "<cover_subtitle>"
Author: "<cover_author>"
Publisher imprint at the bottom: "<cover_publisher>"

No other words, no random letters, no logos. The cover shows <central scene or
symbol>. The composition is vertical 2:3, strong readable silhouette, calm
premium editorial atmosphere, clean book cover typography, legible text.
```

## Abgrenzung

Dieser Skill erzeugt kein EPUB, das macht `hk-epub`, und kein Manuskript, das
macht `hk-buch`. Er ruft den Bilddienst nicht selbst auf, das macht [[bild]].

**Das Bild im Body einer Publikation ist ein anderes Cover.** Es entsteht aus
dem `ai-image`-Callout ganz oben in der Notiz über [[bild-notiz]]. Die beiden
nicht verwechseln: Das eine steht im EPUB vorn, das andere in der Notiz.
