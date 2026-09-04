---
name: hkb-hennibock
description: "Eine Notiz aus der Wissensbasis an eine HenniBock-Instanz übertragen und die Kapitelkette einer Publikation führen. Verwenden bei: publizieren, veröffentlichen, HenniBock, nächstes Kapitel, Beitrag senden, Alt-Text schreiben."
---

# Nach HenniBock veröffentlichen

Zuerst [[hkb]] lesen.

HenniBock ist ein Dienst, kein Format. Der Harness liefert die Werkzeuge, die
Notiz trägt die Angaben, und Index, Kaskade und Idempotenz bleiben drüben.

```bash
hk-kapitel queue                    # die Warteschlange und wer dran ist
hk-kapitel next                     # das nächste offene Kapitel
hk-publish analyze <notiz>          # Metadaten, Bilder, Alt-Texte
hk-publish build <notiz> --send     # bauen und übertragen
hk-publish attached <notiz>         # hängt der Beitrag in seiner Publikation?
```

Ziel und Zugang stehen in der Umgebung: `HENNIBOCK_URL` und
`HENNIBOCK_IMPORT_TOKEN`. **Es gibt keinen Standardwert für das Ziel.** Ohne
beide wird nicht gesendet.

## Welche Angaben eine Notiz trägt

| Property | Was sie sagt |
|---|---|
| `hennibock_type` | die Dokumentart, etwa `title_story`, `essay`, `publication` |
| `hennibock_areas` | die Bereiche der Instanz, Pflicht |
| `hennibock_ref` | die Kennung des Dokuments, wird beim ersten Publish geschrieben |
| `hennibock_published` | wann es erschien, wird beim ersten Publish geschrieben |
| `hennibock_cover` | ein anderes Titelbild als das erste im Body |
| `hennibock_skip` | ein Kapitel, das aus dem Verzeichnis fällt |
| `hennibock_queue` | an einer Publikation: sie nimmt an der Rotation teil |
| `hennibock_chapter_type` | an einer Publikation: welchen Typ ihre Kapitel erben |

**Der Harness deklariert diese Properties nicht.** Sie gehören zu einem Dienst
und nicht zum Format. Eine Ablage, die veröffentlicht, nimmt sie in ihre
eigenen Typdefinitionen auf, sonst meldet `hk-lint --strict` sie als
undeklariert.

Der Autorname und das Bereichsvokabular stehen fest im Werkzeug. Sie gehören
der Instanz und bleiben gleich, aus welcher Ablage ein Text kommt.

## Was das Werkzeug am Body tut

Es entfernt die `ai-image`-Callouts und den Abschnitt `# Siehe auch`, löst
Wikilinks auf und schreibt Bild-Einbettungen auf `image/<slug>` um. Ein
Verweis auf eine publizierte Notiz wird ein Link, ein Verweis auf eine noch
nicht publizierte bleibt Anzeigetext und wächst beim nächsten Publish nach.

Bei `hennibock_type: publication` ist der Body das Inhaltsverzeichnis. Die
Auflösung der Verweise macht daraus von selbst das Gewünschte.

## Der Gate

**Vor jedem Bundle läuft `hk-text --gate` über die enthaltenen Texte.** Ein
Befund der Severity `error` hält an, es entsteht kein Bundle und es wird nichts
gesendet. Fehlt der Prüfer, bricht der Lauf ab: Ein Gate, das sich still
abschaltet, ist schlechter als keins.

## Alt-Texte

Ein Bild ohne Alt-Text meldet `analyze` unter `missing_alt`. Dann schreibst du
einen deutschen Alt-Text und übergibst ihn an `write-alts`, das ihn in den
Callout schreibt. Danach findet `build` ihn dort, und der nächste Publish
erzeugt ihn nicht noch einmal.

**Schreib nur für die Bilder, die gemeldet sind.** Ein Alt-Text, der schon im
Callout steht, ist die dauerhafte Quelle und wird nicht überschrieben.

`write-alts` ist ein eigenes Kommando und kein Seiteneffekt von `build`. Sonst
wäre die Trennung zwischen einer einmaligen Abweichung und der dauerhaften
Quelle wieder aufgehoben.

## Ablauf einer Veröffentlichung

1. `hk-kapitel next` sagt, was dran ist.
2. `hk-publish analyze <notiz>` lesen. Fehlt ein Alt-Text, schreiben und mit
   `write-alts` festhalten.
3. `hk-publish build <notiz> --send`.
4. Der Lauf prüft danach selbst, ob der Beitrag in seinen Publikationen hängt,
   und zieht eine nach, der er fehlt.

## Grenzen

Der Harness erzeugt Inhalt und Bundle. Was drüben damit geschieht, entscheidet
HenniBock.

`sips` für die Bildmaße und `curl` für die Übertragung sind macOS-Werkzeuge.
Auf einem anderen System läuft der Bau nicht.
