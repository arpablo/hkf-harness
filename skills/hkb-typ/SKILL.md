---
name: hkb-typ
description: "Einen eigenen Typ in einer Wissensbasis nach HKF Core anlegen oder seine Property-Tabelle erweitern. Verwenden bei: neuen Typ anlegen, Typdefinition schreiben, Property ergänzen, es gibt keinen passenden Typ für diese Notiz."
---

# Einen Typ anlegen oder erweitern

Zuerst [[hkb]] lesen. Ein Typ ist ein Verzeichnis mit einer Beschreibung —
mehr verlangt HKF nicht, und mehr sollte er auch nicht behaupten. Dies ist
die **einzige** Gelegenheit, bei der du in `Typedefs/` schreibst.

## Erst prüfen, ob es ihn braucht

Ein neuer Typ ist teuer: Er beansprucht ein Verzeichnis, und was einmal darin
liegt, lässt sich nur Notiz für Notiz wieder trennen. Drei Fragen vorher:

- **Gibt es ihn schon unter anderem Namen?** Die Typtabelle in `hkb.md`.
- **Reicht ein vorhandener Typ mit einer weiteren Property?** Dann ist es
  eine Tabellenzeile, kein Typ.
- **Kommt er aus einem Bundle, das noch fehlt?** Dann nachladen statt selbst
  definieren — sonst gibt es später zwei Typen desselben Namens und eine
  Bedeutungsprüfung (§5.5).

## Anlegen

`<base>/Typedefs/<typname>.md`. Der Dateiname ist der Typname, `kebab-case`,
Einzahl.

```markdown
---
type: typedef
title: Werkstoff
description: Ein Material, aus dem etwas gefertigt wird.
dir: werkstoffe
created: 2026-08-31
modified: 2026-08-31T09:14:00
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| dichte | number | nein | — | in g/cm³ |
| hersteller | hkf-link:organisation | nein | — | Wer ihn liefert |
| genormt | checkbox | nein | false | Ob eine Norm ihn festlegt |

# Konventionen

Was der Typ meint und was er nicht meint.
```

- **`description` ist Pflicht und einzeilig** — sie erscheint in der
  Typtabelle der Wurzeldatei.
- **`dir` ist freigestellt.** Ohne es gilt der groß geschriebene Typname mit
  angehängtem `s`. Die Regel ist mechanisch, kein Sprachgefühl: `werkstoff`
  wird zu `Werkstoffs`, und in HKF Config schreiben `city` und `country` genau
  deshalb ein `dir` — `Citys` und `Countrys` wollte niemand lesen. Wer
  abweicht, setzt `dir` so, dass es kein anderer Typ beansprucht und nicht
  unter `media_base` liegt.
- **Eine Vorgabe steht nur dort, wo Abwesenheit wirklich diesen Wert
  bedeutet.** `genormt` ohne Angabe heißt: nicht genormt — das stimmt. Eine
  Sprache ohne Angabe heißt dagegen „unbekannt", nicht „deutsch"; dort bleibt
  die Spalte `—`. Sie wird gelesen, nie geschrieben, und steht nie an einer
  Pflicht-Property (Core §3.7).
- **Der Body trägt den vollständigen Vertrag.** Wer die Typdefinition liest,
  soll den Typ benutzen können, ohne die Spezifikation zu kennen.

## Die Typ-Spalte

Eine Wertform (`text`, `list`, `number`, `checkbox`, `date`, `datetime`), ein
Property-Typ aus `Proptypes/`, oder eine Listenform mit angehängtem `-list`.

| Zelle | Bedeutung |
|---|---|
| `hkf-link` | ein Verweis auf eine Notiz beliebigen Typs |
| `hkf-link:organisation` | ein Verweis auf eine `organisation` |
| `hkf-link:person,organisation` | auf eine `person` **oder** eine `organisation` |
| `hkf-link-list:person` | eine Liste; **jeder** Eintrag verweist auf eine `person` |
| `hkf-file:image` | eine Datei unter `<media_base>/images/` |
| `hkf-file:image / hkf-url` | eine Datei **oder** eine Adresse |

- **`,` trennt Argumente eines Typs**, ohne Leerzeichen. **` / ` trennt ganze
  Typen**, mit Leerzeichen auf beiden Seiten — ohne sie liest sich
  `image/hkf-url` wie ein Pfad.
- **Der `:`-Zusatz gibt es nur an `hkf-link` und `hkf-file`** samt ihren
  Listenformen. Anderswo ist er ein Fehler.
- **Alle Alternativen einer Zelle haben dieselbe Wertform.**
- **Die Beschreibungsspalte nennt die Alternativen in Worten.** Das ist keine
  Zierde: Wer nur die Tabelle liest, muss ohne Kenntnis der Grammatik
  erfahren, dass beides zulässig ist.

## Eine Property ergänzen

Eine Zeile in der Tabelle, mehr nicht. Der häufigste Anlass ist ein Befund
aus `hk-lint --strict`: `source: isbn_alt in 4 von 4 Notizen` — die Property
hat sich eingebürgert und gehört in den Vertrag.

**Eine Zeile zu ändern ist etwas anderes als eine hinzuzufügen.** Wer den Typ
oder die Pflichtangabe einer bestehenden Property ändert, ändert eine
Zusicherung, an der Notizen hängen — das legst du vor, statt es zu tun.

## Danach

```bash
hk-lint --fix
```

Das erzeugt die Typtabelle in `hkb.md` neu; von Hand schreibst du sie nicht.
Anschließend prüft es die neue Tabelle gegen die Werte der Notizen — dort
zeigt sich, ob die Zusicherung trägt.

## Einen neuen Property-Typ

Nur, wenn eine Einschränkung sich wiederholt und keine der sechs Wertformen
sie ausdrückt. `<base>/Proptypes/<name>.md` mit `form` (Pflicht) und wahlweise
`pattern`, `values`, `unit`, `min`, `max`.

- **Das Präfix `hkf-` ist der Spezifikation vorbehalten.** Ein eigener
  Property-Typ heißt anders.
- **Kein eigener Name endet auf `-list`** — die Listenform entsteht von
  selbst aus dem Namen.
- **Für eine der sechs Wertformen wird keiner angelegt.**
