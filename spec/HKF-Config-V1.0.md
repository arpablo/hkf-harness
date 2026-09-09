---
type: specification
title: HKF Config V1.0 — Typen und Property-Typen
description: "Zwanzig Typdefinitionen und achtzehn Property-Typen an einem Ort: die Grundausstattung jeder Wissensbasis und das Vokabular, das als Bundle dazukommt."
status: draft
---

# HKF Config V1.0

Dieses Dokument enthält alles, was HKF konkret festlegt: **jede Typdefinition
und jeden Property-Typ** — zwanzig und achtzehn. HKF Core beschreibt daneben nur noch, wie eine
Ablage funktioniert — Verzeichnisse, Wertformen, Verweise, Typdefinitionen als
Bauform, das Bundle-Format, die drei Methoden — und verweist für jede einzelne
Definition hierher.

Der Schnitt liegt zwischen **Mechanik und Inventar**. Core sagt, was eine
Typdefinition ist und wie eine Property-Tabelle gelesen wird; hier steht,
welche es gibt. Wer wissen will, ob `born` ein `date` ist, schlägt hier nach;
wer wissen will, was eine Property-Tabelle überhaupt zusichert, in Core.

Verweise der Form „Core §3.6" zeigen in jenes Dokument.

---

# 1. Wie das hier in eine Ablage kommt

Alles in diesem Dokument gehört zur **Grundausstattung** einer Wissensbasis:
Es wird angelegt, wenn die Ablage entsteht, und niemals geliefert.

Für die drei Kern-Typen ist das zwingend. Ein Import muss Typdefinitionen
ablegen, Property-Typen einordnen und die Lieferung verbuchen können, bevor er
irgendetwas anderes tut; er setzt `typedef`, `proptype` und `bundle` also
voraus. Ein Bundle, das sie mitbrächte, müsste sich selbst schon kennen. Core
§5.3 führt das aus.

Für die übrigen gilt dieselbe Antwort aus einem einfacheren Grund: **Was jede
Wissensbasis ohnehin bekommt, muss niemand ausliefern.** Ein Bundle bringt
Inhalte mit und, wenn es einen Typ braucht, den dieses Dokument nicht kennt,
dessen Typdefinition dazu. Einen Typ von hier liefert es nie (Core §7.1).

Eine Wissensbasis darf einzelne Typen ungenutzt lassen — ein Typverzeichnis,
das leer bliebe, darf entfallen (Core §3.2). Sie darf keinen abwandeln: Wer
einen Typ dieses Namens führt, führt ihn in der hier festgelegten Bedeutung
und unter dem hier festgelegten Verzeichnis. Nur so bleiben Bundles zwischen
verschiedenen Wissensbasen austauschbar. Wer mehr braucht, legt einen eigenen
Typ daneben (Core §3.7).

---

# 2. Property-Typen

Was ein Property-Typ ist und wie er wirkt, steht in Core §3.5. Hier stehen
die, die es gibt: vierzehn, die jede Ablage kennt, und drei, die nur mit den
Typen aus §3 Sinn ergeben.

## 2.1 Die fünfzehn Standard-Property-Typen

Diese fünfzehn Property-Typen kennt jede HKB. Sie sind Teil dieser
Spezifikation und gehören zur **Grundausstattung**: Eine HKB legt sie beim
Anlegen als Notizen in `Proptypes/` an (Core §5.3).

Die Tabelle unten ist für Menschen. **Maschinenlesbar stehen dieselben Namen
als `#/$defs/standard-proptypes` im Schema** (Core Anhang B.4), und bei
Abweichung gilt das Schema. Ein Werkzeug liest sie dort; wer die Tabelle
ändert, ändert das Schema mit.

| Property-Typ | Wertform | Einschränkung |
|---|---|---|
| `hkf-geo` | `list` | `items: 2`, je Eintrag `pattern: "^-?[0-9]{1,3}([.,][0-9]+)?$"`; **erst die Breite, dann die Länge** |
| `hkf-url` | `text` | `pattern: "^(https?://\\S+|\\[[^\\]\\n]+\\]\\(https?://\\S+\\))$"` |
| `hkf-email` | `text` | `pattern: "^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$"` |
| `hkf-phone` | `text` | `pattern: "^\\+[1-9]\\d{6,14}$"` — E.164, also `+4993131885` |
| `hkf-lang` | `text` | `pattern: "^[a-z]{2}$"` — ISO 639-1, also `de`, `en` |
| `hkf-country` | `text` | `pattern: "^[A-Z]{2}$"` — ISO 3166-1 alpha-2, also `DE`, `GB` |
| `hkf-latitude` | `number` | `min: -90`, `max: 90`, `unit: Grad` |
| `hkf-longitude` | `number` | `min: -180`, `max: 180`, `unit: Grad` |
| `hkf-year` | `number` | `min: -4000`, `max: 9999` |
| `hkf-wikidata` | `text` | `pattern: "^Q[1-9]\\d*$"` — Wikidata-Kennung, etwa `Q7259` |
| `hkf-file` | `text` | Wikilink auf eine Mediendatei, **mit** Dateiendung |
| `hkf-link` | `text` | genau ein qualifizierter Wikilink nach Core §3.6 |
| `hkf-link-list` | `list` | jeder Eintrag ein qualifizierter Wikilink nach Core §3.6 |
| `hkf-link-or-url` | `text` | entweder ein qualifizierter Wikilink nach Core §3.6 oder eine Adresse nach `hkf-url` |
| `hkf-link-or-text` | `text` | entweder ein qualifizierter Wikilink nach Core §3.6 oder ein beliebiger Text |

`hkf-year` trägt eine Jahreszahl, wenn kein vollständiges Datum bekannt ist.
Negative Werte bezeichnen Jahre vor der Zeitenwende. Ein bekanntes Datum
gehört als `date` ins Frontmatter, nicht als Jahr.

`hkf-wikidata` verankert eine Notiz an einem Gegenstand der realen Welt.
Anders als alle übrigen Property-Typen beschreibt er nicht die Notiz, sondern
das, worüber sie handelt: `Q7259` bezeichnet Ada Lovelace, gleich wie die
Notiz heißt und in welcher Wissensbasis sie liegt. Damit lässt sich erkennen,
dass zwei Notizen aus verschiedenen Lieferungen dasselbe meinen — was die
pfadbasierte Identität aus Core §3.2 nicht leisten kann.

Er ist der einzige standardisierte Normdaten-Bezug, weil Wikidata als
einziges Verzeichnis Personen, Körperschaften, Orte, Werke und Begriffe
gleichermaßen abdeckt. Fachliche Normdateien wie GND, VIAF oder ORCID gehören
als eigene Property-Typen in die jeweilige Wissensbasis (Core §3.5).

Der Body der Notiz `Proptypes/hkf-wikidata.md` beschreibt, wie sich aus der
Kennung weitere Angaben beschaffen lassen. Eine Wissensbasis SOLLTE diesen
Text führen: Er ist die einzige Stelle, an der ein Werkzeug erfährt, was mit
der Kennung anzufangen ist.

`hkf-file` verweist auf eine Mediendatei, nicht auf eine Notiz. Der Wert ist
ein qualifizierter Wikilink nach Core §3.6, der aber die **Dateiendung behält**,
weil sie bei einer Mediendatei zum Namen gehört:

```yaml
portrait: "[[Media/Images/personen/portraet-ada.png|portraet-ada.png]]"
```

- Das Ziel MUSS in einem der fünf Medienverzeichnisse aus Core §3.2.1 liegen.
- Die Dateiendung ist **nicht** `.md` — außer bei der Art `clipping`. Ein
  Clipping ist eine erfasste Webseite und liegt als Markdown vor; es ist
  trotzdem eine Datei und keine Notiz, und `hkf-file:clipping` ist der einzige
  Weg, darauf zu zeigen.
- In Properties steht der Link ohne `!`. Einbettungen wie `![[…]]` sind
  gewöhnliches Markdown und nur im Body erlaubt.
- `hkf-file` darf mit einer **Medienart** eingeschränkt werden:
  `hkf-file:image`, `hkf-file:image,video`. Ohne Angabe ist jede Art
  zulässig. Das Verfahren entspricht dem der Zieltypen (Core §3.7.1).
- Die Listenform `hkf-file-list` ergibt sich aus Core §3.5.2 und darf ebenfalls
  eine Medienart tragen: `hkf-file-list:image`.

Ihre Bedeutung ist festgelegt und darf von einer Ablage nicht umdefiniert
werden. Ein Bundle darf sie weglassen, weil jede HKB sie ohnehin kennt; jede
andere verwendete Property-Typ-Notiz muss es mitliefern (Core §4).

`hkf-link` und `hkf-link-list` sind die einzige Art, einen Verweis in einer
Property zu führen. Auf welchen Typ der Verweis zeigt, legt die
Property-Tabelle fest, nicht der Property-Typ — siehe Core §3.7.1.

`hkf-link-or-url` lässt beides zu: einen Verweis in die eigene Ablage oder eine
Adresse im Netz. Er ist für Properties gedacht, bei denen das Ziel ebenso gut
außerhalb liegen kann — die verwandte Sache ist mal eine Notiz, mal ein
Aufsatz irgendwo. Beide Formen sind `text`, die Property hat also eine
eindeutige Wertform.

Geprüft wird der Reihe nach: Sieht der Wert wie `[[…]]` aus, gilt Core §3.6, sonst
das Muster von `hkf-url`. Erfüllt er keines von beiden, ist das ein Befund, der
beide nennt — geraten wird nicht.

**Er nimmt keinen `:`-Zusatz.** Wer einen Zieltyp fordern will und trotzdem
eine Adresse zulassen, schreibt die Alternative aus: `hkf-link:person /
hkf-url` (Core §3.7.2). Das ist dasselbe in ausführlich und sagt in der Tabelle
deutlicher, was gemeint ist. `hkf-link-or-url` ist die Abkürzung für den
häufigen Fall, in dem der Zieltyp gleichgültig ist.

`hkf-link-or-text` lässt einen Verweis oder freien Text zu. Er ist für die
Fälle gedacht, in denen dasselbe Feld mal auf eine Notiz zeigt und mal nur
einen Namen trägt. Ein Verfasser ist manchmal eine Personennotiz und
manchmal die Zeile auf einem Titelblatt. Eine Zugehörigkeit ist manchmal
eine `organisation` und manchmal die Angabe unter einem Aufsatztitel. Für
jeden davon eine Notiz anzulegen hieße, die Ablage mit Namen zu füllen, über
die nichts weiter zu sagen ist.

Geprüft wird der Reihe nach wie bei `hkf-link-or-url`: Sieht der Wert wie
`[[…]]` aus, gilt Core §3.6 samt Zieltyp, und ein Tippfehler im Pfad bleibt
ein Befund. Sonst ist es Text und immer gültig.

**Er nimmt einen `:`-Zusatz**, anders als `hkf-link-or-url`, und das ist kein
Widerspruch, sondern folgt aus dem Unterschied der zweiten Alternative: Dort
ist sie eine Adresse im Netz, die keinen Typ hat, den man fordern könnte, hier
ein Text. Der Zieltyp betrifft in beiden Fällen allein die erste. Die
Grammatik führt ihn darum als eigene Produktion (Core Anhang B.3).

**Und er ist nicht dasselbe wie die Alternative `hkf-link:person / text`.**
Die wird nach Core §3.7.2 der Reihe nach durchprobiert, und `text` erfüllt
*jeder* Wert: Ein Wikilink auf den falschen Typ fiele durch die erste
Alternative und würde von der zweiten stillschweigend als Text angenommen. Die
Zieltypprüfung wäre wirkungslos. `hkf-link-or-text` entscheidet stattdessen an
der Form des Wertes, welche Alternative gilt, und prüft dann nur diese.

## 2.2 Die drei Aufzählungen

Drei Property-Typen zählen Werte auf, statt eine Form einzuschränken. Sie
stehen für sich, weil sie ohne die Typen `person`, `organisation` und `source`
nichts zu tun hätten.

| Property-Typ | Wertform | Einschränkung |
|---|---|---|
| `hkf-person-category` | `text` | `values: [artist, athlete, author, cleric, diplomat, engineer, entrepreneur, jurist, musician, physician, politician, ruler, scholar, scientist, soldier]` |
| `hkf-organisation-category` | `text` | `values: [association, authority, company, foundation, institute, ngo, party, religious, school, union, university]` |
| `hkf-source-kind` | `text` | `values: [article, book, paper, podcast, transcript, video, web]` |

`hkf-source-kind` sagt, **welcher Art** ein Werk ist, und ersetzt damit die
Typunterscheidung, die HKF bis dahin über vier Quelltypen führte (§3.8). Ein
Wert ist genug: Ein Werk ist ein Buch oder ein Video, nicht beides. Die sieben
sind grob und decken ab, was tatsächlich vorkommt; wer eine Dissertation, einen
Bericht oder einen Vortrag ablegt, nimmt `paper`, `web` oder `transcript`. Eine
Wissensbasis, der das nicht reicht, legt einen eigenen Property-Typ an — sie
darf `hkf-source-kind` nicht umdefinieren, wohl aber eine eigene Property
danebenstellen.

Die ersten beiden werden als **Listenform** verwendet (Core §3.5.2), also als
`hkf-person-category-list` und `hkf-organisation-category-list`. Eine Person
ist selten nur eines: Wer regiert hat, hat oft auch geschrieben und gedient.
Ebenso ist eine Landesuniversität zugleich `university` und `authority`. Ein
einwertiges Feld erzwänge eine Wahl, die die Sache nicht hergibt.

Die Werte beschreiben die **Rolle**, nicht den Beruf und nicht den Rang. Sie
sind bewusst grob: Feinere Unterscheidungen gehören in den Body oder in eigene
Property-Typen der jeweiligen Wissensbasis. Das gilt für alle drei
Aufzählungen: Eine spätere Fassung von HKF Config darf Werte ergänzen;
entfernen darf sie keine, weil das vorhandene Notizen ungültig machte.

---

## 2.3 Die Properties des Vokabulars

Die 75 Property-Namen, die die zwanzig Typdefinitionen aus §3 zusichern —
an einer Stelle, damit sich nachschlagen lässt, was ein Name bedeutet, ohne
jede Typdefinition zu öffnen. Die notizübergreifenden Properties aus Core A.2
stehen nicht darin; sie gelten ohnehin für jede Notiz.

**Ein Name, eine Typangabe** (Core §3.7.3): Verschieden sein dürfen allein die
Argumente hinter dem `:` — die Zieltypen eines `hkf-link`, die Medienarten
eines `hkf-file`. Wo diese Tabelle unter einem Namen zwei Angaben nennt, mit
`·` getrennt, ist genau das der Fall: `broader` verweist in `concept` auf ein
Konzept und in `term` auf einen Begriff, und beides ist ein `hkf-link`.

**Die Tabelle ist abgeleitet.** Zugesichert wird eine Property in der
Property-Tabelle ihres Typs (Core §3.7); dort steht auch, was sie im
Einzelnen heißt. Bei Abweichung gewinnen die Typdefinitionen — wie bei der
Typtabelle einer Wurzeldatei (Core §3.1). `tools/inventar.py` im Harness hält
beide gegeneinander.

**Fett gesetzt ist der Typ, in dem die Property Pflicht ist.**

| Property | Typangabe | In den Typen |
|---|---|---|
| `about` | `hkf-link-list` | daily, note, quote |
| `accessed` | `date` | source |
| `address` | `text` | place |
| `affiliations` | `hkf-link-or-text-list:organisation` | person |
| `applies_to` | `hkf-link-list` | hint |
| `authority` | `hkf-link-or-text:organisation` | specification |
| `authors` | `hkf-link-or-text-list:person` | source |
| `base` | `text` | typedef |
| `geo` | `hkf-geo` | city, country, place |
| `items` | `number` | proptype |
| `birthplace` | `hkf-link:place,city,country` | person |
| `born` | `date` | person |
| `born_year` | `hkf-year` | person |
| `broader` | `hkf-link:concept · hkf-link:term` | concept, term |
| `cancelled` | `checkbox` | event |
| `capital` | `hkf-link:city` | country |
| `checksum` | `text` | source |
| `code` | `hkf-country` | country |
| `compares` | `hkf-link-list` | **comparison** |
| `country` | `hkf-link:country` | city, place |
| `covers` | `text` | summary |
| `date` | `date` | event |
| `description` | `text` | **bundle**, **typedef** |
| `died` | `date` | person |
| `died_year` | `hkf-year` | person |
| `dir` | `text` | typedef |
| `dissolved` | `date` | organisation |
| `dissolved_year` | `hkf-year` | country, organisation |
| `email` | `hkf-email` | organisation, person |
| `ends_at` | `datetime` | event |
| `file` | `hkf-file:document / hkf-url · hkf-file:document,clipping / hkf-url` | source, specification |
| `flag` | `hkf-file:image / hkf-url` | country |
| `form` | `text` | **proptype** |
| `founded` | `date` | organisation |
| `founded_year` | `hkf-year` | city, country, organisation |
| `full_name` | `text` | person |
| `homepage` | `hkf-url` | event, organisation, person |
| `id` | `text` | **bundle** |
| `image` | `hkf-file:image / hkf-url` | city, place |
| `imported` | `datetime` | bundle |
| `kind` | `hkf-source-kind` | source |
| `lang` | `hkf-lang` | quote, source, specification, **term** |
| `locator` | `text` | quote |
| `location` | `hkf-link:place,city,country` | event |
| `logo` | `hkf-file:image / hkf-url` | organisation |
| `max` | `number` | proptype |
| `min` | `number` | proptype |
| `o_categories` | `hkf-organisation-category-list` | organisation |
| `organizer` | `hkf-link:person,organisation` | event |
| `p_categories` | `hkf-person-category-list` | person |
| `parent` | `hkf-link:organisation · hkf-link:topic` | organisation, topic |
| `part_of` | `hkf-link:place,city,country · hkf-link:place,country` | city, place |
| `participants` | `hkf-link-list:person,organisation` | event |
| `pattern` | `text` | proptype |
| `phone` | `hkf-phone` | organisation, person |
| `portrait` | `hkf-file:image / hkf-url` | person |
| `provisional` | `checkbox` | typedef |
| `published` | `date` | source |
| `published_year` | `hkf-year` | source |
| `quotes` | `hkf-link:source` | quote |
| `related` | `hkf-link-or-url-list` | city, comparison, concept, country, daily, event, hint, note, organisation, person, place, quote, source, specification, summary, term, topic |
| `required_bundles` | `list` | bundle |
| `said_at` | `date` | quote |
| `said_by` | `hkf-link-or-text:person` | quote |
| `seat` | `hkf-link:place,city,country` | organisation |
| `source` | `text` | bundle |
| `starts_at` | `datetime` | event |
| `summarizes` | `hkf-link:source` | **summary** |
| `supersedes` | `hkf-link:specification` | specification |
| `terms` | `hkf-link-list:term` | concept |
| `unit` | `text` | proptype |
| `url` | `hkf-url` | source, specification |
| `values` | `list` | proptype |
| `version` | `text` | bundle, **specification** |
| `wikidata_id` | `hkf-wikidata` | city, concept, country, event, organisation, person, place, source, term, topic |

---

# 3. Typdefinitionen

Zwanzig Typen. Die ersten drei sind die **Kern-Typen** — ohne sie ließe sich
keine Ablage beschreiben. Die siebzehn danach sind das **Vokabular**: Gegenstände,
die in nahezu jeder Wissensbasis vorkommen, die Quellen, auf die sie sich
beruft, was aus ihnen gelesen und wörtlich übernommen wurde, und die
wenigen Typen, mit denen eine
Ablage über sich selbst spricht.

| Typ | Verzeichnis | Zweck |
|---|---|---|
| `typedef` | `Typedefs` | Registriert einen Typ und legt sein Verzeichnis fest. |
| `proptype` | `Proptypes` | Schränkt eine Wertform ein. |
| `bundle` | `Bundles` | Beschreibt eine Lieferung. |
| `person` | `Persons` | Ein Mensch. |
| `organisation` | `Organisations` | Eine Körperschaft: Unternehmen, Institut, Verein, Behörde. |
| `place` | `Places` | Ein geographischer Ort. |
| `city` | `Cities` | Eine Stadt. |
| `country` | `Countries` | Ein Staat. |
| `event` | `Events` | Ein Geschehen zu einer bestimmten Zeit. |
| `source` | — | Ein Werk, auf das sich die Wissensbasis beruft. |
| `summary` | `Summaries` | Was eine Quelle sagt, auf drei Seiten. |
| `quote` | `Quotes` | Ein wörtlich übernommener Satz und seine Herkunft. |
| `term` | `Terms` | Ein definierter Begriff. |
| `concept` | `Concepts` | Eine Sache und der Stand des Wissens über sie. |
| `comparison` | `Comparisons` | Eine Gegenüberstellung mehrerer Gegenstände entlang benannter Dimensionen. |
| `topic` | `Topics` | Ein Themengebiet als Einstiegspunkt. |
| `note` | `Notes` | Eine Notiz ohne spezifischeren Typ. |
| `daily` | — | Was an einem Tag anfiel. |
| `specification` | `Specifications` | Ein normatives Dokument, an das sich die Wissensbasis hält. |
| `hint` | `Hints` | Eine Festlegung, wie diese Wissensbasis geführt wird. |

**Drei Typen tragen ein `dir`, die übrigen nicht.** Deren
Verzeichnisse ergeben sich aus der Vorgabe „Typname groß geschrieben, mit
angehängtem `s`" (Core §3.7); ein Werkzeug kennt den Ablageort damit, ohne die
Typdefinition zu lesen.

**Zwei Typen haben gar kein Verzeichnis.** `source` liegt unmittelbar unter
seinem Bereich, also nach Vorgabe in `50-Sources/` (Core §3.2.2), `daily`
ebenso unter `journal_base`, dort nach Jahr und Monat geteilt (Core §3.2.5).
Die Spalte oben lässt ihre Zellen darum leer.

Die Vorgabe ist mechanisch und kein Sprachgefühl — bei `city`, `country` und
`summary` ergäbe sie `Citys`, `Countrys` und `Summarys`. Alle drei schreiben
darum ein `dir` und heißen `Cities`, `Countries` und `Summaries`. Der Preis ist
genau der, gegen den die Vorgaberegel sonst schützt: Wer diese Verzeichnisse
sucht, muss die Typdefinition lesen. Für drei Namen, die jeder Leser sonst für
einen Fehler hielte, ist er tragbar.

Nicht zu verwechseln mit der Property `dir`, die `typedef` in §3.1 zusichert:
Die trägt eine *andere* Typdefinition, wenn sie abweichen will.

**Acht Properties sind Pflicht**, alle übrigen optional: `description` in
`typedef`, `form` in `proptype`, `id` und `description` in `bundle`, `version`
in `specification`, `compares` in `comparison`, `lang` in `term` und
`summarizes` in `summary`. Jede trägt den Gegenstand ihrer Notiz — ein
Property-Typ ohne Wertform, eine Spezifikation ohne Fassung, ein Vergleich ohne
Verglichene, ein Begriff ohne Sprache und eine Zusammenfassung ohne ihr Werk
sagen nichts. Sonst fordert keiner dieser Typen etwas über `type`
hinaus; er sichert nur zu, was die genannten Properties bedeuten.

Eine **Vorgabe** (Core §3.7) tragen genau zwei Properties, beide Checkboxen:
`provisional` in `typedef` und `cancelled` in `event`. Eine Typdefinition, an
der es niemand vermerkt hat, ist nicht vorläufig; eine Veranstaltung nicht
abgesagt. Überall sonst heißt eine fehlende Angabe „unbekannt", und das ist
eine andere Aussage als jeder konkrete Wert.

## 3.1 `typedef`

```markdown
---
type: typedef
title: Typdefinition
description: Registriert einen Typ und legt sein Verzeichnis fest.
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| description | text | ja | — | Einzeiliger Zweck, erscheint in der Typtabelle der Wurzeldatei |
| base | text | nein | wiki | Bereich, unter dem die Instanzen liegen: `wiki`, `source`, `output` oder `config` (Core §3.2) |
| dir | text | nein | — | Verzeichnis der Instanzen. Vorgabe ist der groß geschriebene Typname mit angehängtem `s` (Core §3.7) |
| provisional | checkbox | nein | false | Beim Import angelegt, weil niemand den Typ definiert hat (Core §5.4) |

# Konventionen

Der Dateiname ist der Typname (Core §3.7). Der Body trägt die
Property-Tabelle und die Konventionen des Typs. `dir` ist ein relativer Pfad
zum Basispfad, mit `/` als Trennzeichen und beliebig vielen Abschnitten,
ohne führenden und abschließenden `/` und ohne `.`- oder `..`-Abschnitte. Er
darf weder unter `media_base` noch unter `source_base` liegen (Core §3.2.1
und §3.2.2). Der Typ `source` trägt kein `dir`: Er liegt unmittelbar unter
seinem Bereich.

`base` sagt, in welchem Bereich die Notizen des Typs liegen (Core §3.2). Ohne
die Angabe gilt `wiki`. Drei Typnamen brauchen sie nicht, weil ihr Bereich
schon im Namen steht: `typedef` und `proptype` liegen unter `config_base`,
`source` unter `source_base`. `base: media` gibt es nicht, dort liegen Dateien
und keine Notizen.

`provisional` steht nur an einer Typdefinition, nur mit dem Wert `true` und
nur in einer HKB. Ein Bundle enthält keine vorläufige Typdefinition (Core §7.1).
Eine solche Notiz trägt kein `dir`, keinen Abschnitt `# Properties` und kein
`bundles`.

**Welcher Bereich gilt, sagt der Typname und nicht eine Property.**
`typedef` und `proptype` liegen unter `config_base`, `source` unter
`source_base`, jeder andere unter `wiki_base` (Core §3.2). Eine Property
dafür lohnt sich erst, wenn eine Ablage mehrere Quelltypen hätte. HKF führte
kurz ein `is_source`. Eine Ablage hat einen Quelltyp, und die Werkart trägt
`kind` (§3.8).
```

## 3.2 `proptype`

```markdown
---
type: typedef
title: Property-Typ
description: Schränkt eine Wertform ein.
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| form | text | ja | — | Eine der sechs Wertformen aus Core §3.4 |
| items | number | nein | — | Zahl der Einträge, wenn sie feststeht. Nur bei `form: list` |
| pattern | text | nein | — | Regulärer Ausdruck, nur bei `text` und `list`, dort je Eintrag |
| values | list | nein | — | Erlaubte Werte, als Text geführt, auch wenn sie wie Zahlen aussehen |
| unit | text | nein | — | Maßeinheit, beschreibend und nicht geprüft |
| min | number | nein | — | Kleinster zulässiger Wert, nur bei `form: number` |
| max | number | nein | — | Größter zulässiger Wert, nur bei `form: number` |

# Konventionen

Der Dateiname ist der Name des Property-Typs (Core §3.5) und endet nicht auf
`-list`. Für eine der sechs Wertformen wird kein Property-Typ angelegt. `min`
und `max` gibt es nur für Zahlen: Obsidian ordnet einem Property-Namen genau
eine Wertform zu, sie könnten also nicht zugleich Datumsgrenzen sein.
```

Die Tabelle beschreibt die Properties **einer** `proptype`-Notiz. Die
Typdefinition selbst liegt als `Typedefs/proptype.md` und trägt wie jede
Typdefinition `type: typedef`.

## 3.3 `bundle`

```markdown
---
type: typedef
title: Bundle
description: Beschreibt eine Lieferung.
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| id | text | ja | — | Kennung der Lieferreihe in `kebab-case` (Core §4.1). In der HKB gleich dem Dateinamen |
| version | text | nein | — | Unveränderliche Kennung der gelieferten Fassung. Ohne sie hat die Lieferung keine Geschichte, nur einen letzten Stand (Core §4.1) |
| description | text | ja | — | Ein Satz darüber, was die Lieferung enthält |
| required_bundles | list | nein | — | Bundles, die vorher importiert sein sollen (Core §4.1) |
| source | text | nein | — | Herkunft, etwa eine URL oder ein Repository |
| imported | datetime | nein | — | Zeitpunkt der Übernahme, in **UTC** (Core §3.4). Nur in der HKB (Core §5.1). Fehlt es an einer Bundle-Notiz der HKB, wurde die Lieferung geprüft und nicht übernommen (Core §5.7) |

# Konventionen

Als `hbundle.md` in der Wurzel eines Bundles trägt die Notiz zusätzlich die
Wurzeldatei-Properties aus Core A.1 und die Typtabelle im Body. `imported`
entfällt dort. In der HKB liegt sie als `Bundles/<id>.md` ohne diese
Zusätze.

`source` ist `text` und nicht `hkf-url`, weil auch ein Repository-Verweis oder
ein Datenträger als Herkunft in Frage kommt.

`description` ist bei einer Bundle-Notiz **Pflicht**, obwohl Core A.2 sie
sonst freistellt. Wer eine Lieferung vor sich hat, müsste ohne sie den Body
lesen oder die Dateien zählen, um zu erfahren, worum es geht. Sie ist
außerdem die einzige Angabe, die in der Bundle-Liste einer Wissensbasis
abfragbar ist.
```

## 3.4 `person`

```markdown
---
type: typedef
title: Person
description: Ein Mensch.
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| full_name | text | nein | — | Vollständiger Name, wenn er vom Titel abweicht |
| born | date | nein | — | Geburtsdatum |
| born_year | hkf-year | nein | — | Geburtsjahr, wenn kein vollständiges Datum bekannt ist |
| died | date | nein | — | Sterbedatum |
| died_year | hkf-year | nein | — | Sterbejahr, wenn kein vollständiges Datum bekannt ist |
| birthplace | hkf-link:place,city,country | nein | — | Geburtsort |
| p_categories | hkf-person-category-list | nein | — | Rollen der Person |
| affiliations | hkf-link-or-text-list:organisation | nein | — | Zugehörigkeiten: als Verweis auf eine Organisationsnotiz oder als Name |
| homepage | hkf-url | nein | — | Persönliche Webseite |
| email | hkf-email | nein | — | Kontaktadresse |
| phone | hkf-phone | nein | — | Telefonnummer |
| portrait | hkf-file:image / hkf-url | nein | — | Bild der Person, als Datei in der Ablage oder als Adresse im Netz |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Ein Abschnitt, für den keine Quelle etwas hergibt, bleibt weg und wird nicht leer hingeschrieben. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Wer der Mensch ist: Lebensdaten, Herkunft, Rolle, wofür sein Name steht. |
| `## Werdegang` | Welchen Weg er genommen hat, bis er für diese Wissensbasis wichtig wird. |
| `## Wirken` | Was er getan hat und was daraus folgte. |
| `## Bedeutung` | Warum er hier steht und wie er beurteilt wird. |

# Konventionen

`born` und `born_year` schließen einander aus, ebenso `died` und `died_year`.
Der Dateiname ist `vorname-nachname` in kebab-case.
```

## 3.5 `organisation`

```markdown
---
type: typedef
title: Organisation
description: 'Eine Körperschaft: Unternehmen, Institut, Verein, Behörde.'
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| founded | date | nein | — | Gründungsdatum |
| founded_year | hkf-year | nein | — | Gründungsjahr, wenn kein Datum bekannt ist |
| dissolved | date | nein | — | Auflösungsdatum |
| dissolved_year | hkf-year | nein | — | Auflösungsjahr, wenn kein Datum bekannt ist |
| o_categories | hkf-organisation-category-list | nein | — | Art der Körperschaft |
| seat | hkf-link:place,city,country | nein | — | Sitz |
| parent | hkf-link:organisation | nein | — | Übergeordnete Körperschaft |
| homepage | hkf-url | nein | — | Webseite |
| email | hkf-email | nein | — | Kontaktadresse |
| phone | hkf-phone | nein | — | Telefonnummer |
| logo | hkf-file:image / hkf-url | nein | — | Bildmarke, als Datei in der Ablage oder als Adresse im Netz |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Ein Abschnitt, für den keine Quelle etwas hergibt, bleibt weg und wird nicht leer hingeschrieben. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Was für eine Körperschaft: wann gegründet, wo ansässig, wozu. |
| `## Verfassung und Träger` | Wer sie trug, wie sie verfasst war, wer für sie sprach. |
| `## Wirken` | Was sie getan hat und was daraus folgte. |
| `## Bedeutung` | Warum sie hier steht und wie sie beurteilt wird. |

# Konventionen

Rechtsform und Untergliederungen gehören in den Body, nicht in den Namen.
```

## 3.6 `place`

```markdown
---
type: typedef
title: Ort
description: Ein geographischer Ort.
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| geo | hkf-geo | nein | — | Koordinate als Paar, erst Breite, dann Länge |
| country | hkf-link:country | nein | — | Staat, in dem der Ort liegt |
| address | text | nein | — | Anschrift in einer Zeile |
| part_of | hkf-link:place,city,country | nein | — | Übergeordneter Ort |
| image | hkf-file:image / hkf-url | nein | — | Ansicht, als Datei in der Ablage oder als Adresse im Netz |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Ein Abschnitt, für den keine Quelle etwas hergibt, bleibt weg und wird nicht leer hingeschrieben. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Was für ein Ort: wo er liegt, wozu er gehört, wofür er bekannt ist. |
| `## Geschichte` | Was an ihm geschah, soweit es hier zählt. |
| `## Bedeutung` | Warum er hier steht. |

# Konventionen

`geo` trägt beide Werte in einer Angabe, erst die Breite, dann die Länge. `part_of` bildet
die räumliche Schachtelung ab, also Gebäude in Stadt und Stadt in Region.

`country` ist ein Verweis und keine Kennung. Es hieße sonst auf `place`
etwas anderes als auf `city`, und ein Property-Name bedeutet überall dasselbe
(Core §3.7.3). Der Preis ist, dass ein Ort in einem Staat ohne eigene Notiz
seinen Staat nicht nennen kann: Dann bleibt `country` leer, und der Staat
steht im Body oder wird als Notiz angelegt.
```

## 3.7 `event`

```markdown
---
type: typedef
title: Veranstaltung
description: Ein Geschehen zu einer bestimmten Zeit.
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| date | date | nein | — | Tag, wenn keine Uhrzeit bekannt ist |
| starts_at | datetime | nein | — | Beginn |
| ends_at | datetime | nein | — | Ende |
| location | hkf-link:place,city,country | nein | — | Veranstaltungsort |
| organizer | hkf-link:person,organisation | nein | — | Ausrichter |
| participants | hkf-link-list:person,organisation | nein | — | Beteiligte |
| cancelled | checkbox | nein | false | Abgesagt |
| homepage | hkf-url | nein | — | Ankündigung |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Ein Abschnitt, für den keine Quelle etwas hergibt, bleibt weg und wird nicht leer hingeschrieben. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Was geschehen ist: wann, wo, zwischen wem. |
| `## Vorgeschichte` | Was dahin führte. |
| `## Verlauf` | Wie es sich abspielte. |
| `## Folgen` | Was sich danach anders verhielt. |

# Konventionen

Eine Veranstaltung trägt entweder `starts_at` oder `date`, nicht beides.
Zeiten gelten in der `timezone` der Ablage (Core §3.4).
```

## 3.8 `source`

```markdown
---
type: typedef
title: Quelle
description: Ein Werk, auf das sich die Wissensbasis beruft.
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| kind | hkf-source-kind | nein | — | Werkart: Buch, Aufsatz, Video, Webseite und die übrigen |
| authors | hkf-link-or-text-list:person | nein | — | Urheber: als Verweis auf eine Personennotiz oder als Name, wie das Werk ihn nennt |
| published | date | nein | — | Erscheinungsdatum |
| published_year | hkf-year | nein | — | Erscheinungsjahr, wenn kein vollständiges Datum bekannt ist |
| lang | hkf-lang | nein | — | Sprache des Werks |
| url | hkf-url | nein | — | Fundstelle des Werks: wo es veröffentlicht ist |
| file | hkf-file:document,clipping / hkf-url | nein | — | Ausfertigung des Werks: als Datei in der Ablage oder als Adresse, etwa auf einem Dateiserver |
| accessed | date | nein | — | Datum des Abrufs |
| checksum | text | nein | — | `sha256:<hex>` über die Ausfertigung. Sagt beim nächsten Einlesen, ob sich die Quelle geändert hat |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Werks in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Der
mittlere Teil folgt dem Werk und nicht einer eigenen Gliederung: je
Teil, Kapitel oder Hauptabschnitt eine Überschrift. `# Verbindungen`
steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Die Zitationsangaben in Prosa, und in ein bis zwei Sätzen, wovon das Werk als Ganzes handelt. |
| `# Kernaussagen` | Was das Werk im Ganzen behauptet, in wenigen Punkten. |
| je Hauptabschnitt eine Überschrift | Was dort verhandelt wird, in Prosa, mit Verweisen auf die Notizen, die daraus entstanden sind. |
| `# Was die Quelle offenlässt` | Wo das Werk selbst spekuliert, sich widerspricht oder eine Frage offen nennt. |
| `# Tranchen` | Bei einer großen Quelle der Stand des Lesens. Wird von `hk-tranchen` geführt und nicht von Hand. |

**Der erste Satz ist der schwerste und wird trotzdem verlangt.** Wovon
ein Werk als Ganzes handelt, in ein bis zwei Sätzen: Wer das nicht sagen
kann, hat das Werk nicht verstanden, sondern nur seine Kapitel gelesen.
Der Satz entsteht nach der ersten Durchsicht und wird genauer, je weiter
die Lektüre kommt.

**`# Kernaussagen` entsteht zuletzt.** Vor der letzten Tranche wüsste
man nur, was die ersten Kapitel behaupten.

**`# Was die Quelle offenlässt` steht nicht in der Quelle.** Der
Abschnitt sagt das einleitend, sonst liest er sich wie ein Befund des
Werks. Was hier steht, ist beobachtet und nicht behauptet: eine
Spekulation, die der Autor selbst kennzeichnet, ein Widerspruch zwischen
zwei Kapiteln, eine Frage, die er als offen bezeichnet. Ein eigener
Einwand gehört nicht hierher, sondern in eine `note`.

# Konventionen

Eine Quellennotiz beschreibt das Werk, auf das sich die Wissensbasis beruft,
und fasst zusammen, **was es sagt**, gegliedert nach seinem eigenen Aufbau,
je Kapitel oder Hauptabschnitt eine Überschrift. Was man daraus **für die
eigene Sache schließt**, gehört nicht hierher, sondern in eine `note` oder ein
`concept`, das per `sources` auf die Quelle verweist.

**Die Quellennotiz wächst mit dem Werk, eine Zusammenfassung nicht.** Wer die
Lektüre verdichtet braucht, legt daneben eine `summary` an: drei Seiten, die
Kernaussagen und fünf Vorschläge, was sich daraus schreiben ließe (§3.19). Die
Quellennotiz bleibt davon unberührt.

**Die Werkart ist eine Property und kein Typ.** Ein Buch, ein Aufsatz, ein
Video und eine Webseite unterscheiden sich in dem, was über sie zu wissen
ist, kaum: Wer es gemacht hat, wann es erschien, wo es liegt. Was sie
unterscheidet, also Verlag, Auflage und Seitenzahl, ist Zitationsapparat und
steht dort, wo er gebraucht wird: im Body oder in einer Property, die eine
Wissensbasis selbst anlegt. Als vier Typen kostete die Unterscheidung vier
Verzeichnisse und zwanzig Properties, von denen die meisten immer leer
blieben. Eine Quelle, deren Art keiner der vier entspricht, hätte gar keinen
Ort gehabt. `kind` kennt sieben Werte (§2.2), und eine spätere Fassung darf
ergänzen.

**Die Quellennotiz liegt direkt unter `source_base`**, ohne Typverzeichnis
(Core §3.2.2). Bei einem einzigen Quelltyp wäre es reine Verdopplung, und die
Notiz-ID ist damit der bloße Dateiname.

`url` und `file` bezeichnen Verschiedenes und stehen darum als zwei
Properties da, nicht als Alternative (Core §3.7.2): `url` ist, **wo das Werk
veröffentlicht ist**, also die Verlagsseite oder die DOI-Adresse, und damit
zitierfähig. `file` ist, **wo die eigene Ausfertigung liegt**: als Datei in
der Ablage oder als Adresse, etwa auf einem Dateiserver im eigenen Netz. Ein
Original muss also nicht in die Ablage kopiert werden, um verzeichnet zu
sein. Beide dürfen nebeneinander stehen.

**Ist `file` ein Clipping, steht der erfasste Text dort und nicht im Body.**
Ein Clipping ist eine Mediendatei unter `<media_base>/Clippings/` (Core
§3.2.1), also Rohmaterial, das niemand pflegt und das darum auch niemand
prüft. Die Notiz daneben trägt die Zusammenfassung. Das ist der ganze
Unterschied zwischen einer erfassten und einer bloß zitierten Seite, und er
verlangt keinen eigenen Typ: Die Datei ist da oder sie ist es nicht.

`checksum` sagt beim nächsten Einlesen, ob sich die Quelle geändert hat. Eine
Webseite ändert sich still, und ohne die Prüfsumme fiele das erst auf, wenn
die Zusammenfassung schon nicht mehr stimmt.

`published` und `published_year` schließen einander aus, wie `born` und
`born_year` bei einer Person (§3.4). Ein Buch von 1989 hat einen Tag, der
niemanden interessiert, ein Beitrag vom 28. Juli 2026 hat einen, der zählt.
Eine Angabe zu erzwingen, die die Quelle nicht hergibt, brächte nur falsche
Genauigkeit. Beide in eine Property zu legen ginge auch nicht, weil
Alternativen dieselbe Wertform haben müssen (§3.7.2).

```

## 3.9 `term`

```markdown
---
type: typedef
title: Begriff
description: Ein definierter Begriff.
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| lang | hkf-lang | ja | — | Sprache des Begriffs |
| broader | hkf-link:term | nein | — | Übergeordneter Begriff |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Ein Abschnitt, für den keine Quelle etwas hergibt, bleibt weg und wird nicht leer hingeschrieben. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Die Definition: was der Begriff bezeichnet. |
| `## Herkunft` | Woher der Begriff kommt und wer ihn geprägt hat. |
| `## Abgrenzung` | Wovon er zu unterscheiden ist und womit er verwechselt wird. |

# Konventionen

Ein Begriff ist ein Ausdruck in **einer** Sprache, und `lang` nennt sie.
Darum ist sie Pflicht und keine Vorgabe. Derselbe Gegenstand heißt in drei
Sprachen dreierlei. Welche gemeint ist, darf nicht davon abhängen, in
welcher Wissensbasis die Notiz gerade liegt, sonst bliebe ein Bundle nicht
für sich lesbar (Core §4).

Der Body beginnt mit einer Definition in einem Satz. Synonyme werden als
Obsidian-`aliases` geführt und nicht als eigene Property. Sie sind Ausdrücke
derselben Sprache. Die fremdsprachige Entsprechung ist kein Alias, sondern
ein eigener Begriff.

Ein Begriff legt einen Ausdruck fest und ist mit seiner Definition fertig.
Wird die Notiz länger, gehört, was über die Definition hinausgeht, in ein
`concept`.
```

## 3.10 `concept`

```markdown
---
type: typedef
title: Konzept
description: Eine Sache und der Stand des Wissens über sie.
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| terms | hkf-link-list:term | nein | — | Die Begriffe, unter denen die Wissensbasis die Sache führt |
| broader | hkf-link:concept | nein | — | Übergeordnetes Konzept |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Ein Abschnitt, für den keine Quelle etwas hergibt, bleibt weg und wird nicht leer hingeschrieben. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Was die Sache ist, in einem Satz, der ohne die Quellen verständlich bleibt. |
| `## Stand des Wissens` | Was über sie bekannt ist und worauf das beruht. |
| `## Strittig` | Was offen ist oder von wem bestritten wird. |

# Konventionen

Ein Begriff definiert einen Ausdruck, ein Konzept sammelt, was über eine Sache
bekannt ist. Darum ist eine Begriffsnotiz mit ihrer Definition fertig, während
eine Konzeptnotiz mit jeder ausgewerteten Quelle wächst: Der Body trägt den
Stand des Wissens und die offenen Fragen.

Ein Begriff ist sprachgebunden und führt `lang` als Pflicht, ein Konzept
nicht: Dieselbe Sache hat in drei Sprachen drei Begriffe und bleibt dieselbe
Sache. `terms` nimmt sie alle auf.

Hat eine Konzeptnotiz keine eigenen Aussagen, sondern nur Verweise, ist sie
ein `topic`.
```

## 3.11 `comparison`

```markdown
---
type: typedef
title: Vergleich
description: Eine Gegenüberstellung mehrerer Gegenstände entlang benannter Dimensionen.
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| compares | hkf-link-list | ja | — | Die verglichenen Gegenstände, mindestens zwei |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Hier
bleibt kein Abschnitt weg: Ein Vergleich ohne Dimensionen ist eine
Behauptung, einer ohne Urteil eine Tabelle. `# Verbindungen` steht immer
zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Was verglichen wird und welche Frage der Vergleich beantworten soll. |
| `## Dimensionen` | In welchen Hinsichten verglichen wird, als Tabelle mit einer Zeile je Hinsicht. |
| `## Urteil` | Das eigene Urteil, mit seiner Begründung. |

**Der Vergleich spricht in eigenen Worten.** Zwei Werke gebrauchen
denselben Begriff selten gleich, und wer die Sprache eines der beiden
übernimmt, hat die Frage schon zu dessen Gunsten entschieden. Die
Dimensionen werden darum so benannt, dass beide Seiten sich darin
wiederfinden, und die Begriffe der Verglichenen stehen als deren
Begriffe da.

**Ein Widerspruch wird festgehalten und nicht geglättet.** Dass zwei
Quellen dasselbe verschieden sehen, ist eine Auskunft über den
Gegenstand. Jede Deutung steht bei ihrer Quelle, und das Urteil sagt,
welche von beiden warum weiter trägt. Trägt keine weiter, sagt es das.

# Konventionen

Der Gegenstand eines Vergleichs ist kein Ding, sondern ein Verhältnis. Der
Body nennt zuerst, was verglichen wird und warum, dann die Dimensionen, am
besten als Tabelle mit einer Zeile je Dimension, zuletzt das Urteil. Ein
Vergleich ohne Urteil ist eine Tabelle und gehört in die Notiz eines der
Verglichenen.

`compares` nimmt Verweise beliebigen Typs auf: Verglichen wird, was sich
vergleichen lässt, zwei Konzepte ebenso wie zwei Körperschaften. Was nur
einen der Gegenstände betrifft, gehört in dessen eigene Notiz.
```

## 3.12 `topic`

```markdown
---
type: typedef
title: Thema
description: Ein Themengebiet als Einstiegspunkt.
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| parent | hkf-link:topic | nein | — | Übergeordnetes Thema |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. `#
Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Was das Thema umfasst und wo seine Grenzen liegen. |
| `## Einstiege` | Über welche Notizen man das Thema betritt, jede mit einem Satz dazu, wofür sie steht. |

**Ein Thema trägt keine eigenen Tatsachen.** Was hier stünde, stünde ein
zweites Mal da und veraltete an einer der beiden Stellen. Die
Einstiegsliste ist geordnet und nicht vollständig: Sie nennt die
Notizen, mit denen ein Leser anfangen soll, nicht alle, die zum Thema
gehören. Wer alle sucht, fragt den Bestand ab.

# Konventionen

Ein Thema ordnet, ein Begriff definiert, ein Konzept sammelt. Der Body ist
eine Einstiegsseite mit Verweisen. Inhalte, die anderswo hingehören, stehen
nicht hier.
```

## 3.13 `note`

```markdown
---
type: typedef
title: Notiz
description: Eine Notiz ohne spezifischeren Typ.
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| about | hkf-link-list | nein | — | Worauf sich die Notiz bezieht |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Der Typ
ist ein Auffangtyp, und die Gliederung ist entsprechend weit: Ein
Abschnitt, für den es nichts gibt, bleibt weg. `# Verbindungen` steht
immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Was festgehalten wird und bei welchem Anlass. |
| `## Befund` | Was sich gezeigt hat, mit Fundstelle, wo es eine gibt. |
| `## Was daraus folgt` | Was zu tun, zu prüfen oder weiterzuverfolgen ist. |

**Hält die Notiz eine Lektüre fest, trennt sie drei Dinge sichtbar:**
was das Werk behauptet, was über den Gegenstand berichtet wird, und was
der Lesende selbst einwendet. Ein Einwand, der aussieht wie eine Aussage
des Autors, ist ein Fehler und keine Geschmacksfrage. Die Fundstelle
steht bei der Behauptung, nicht beim Einwand.

# Konventionen

Auffangtyp. Er wird verwendet, wenn kein anderer Typ passt, und nicht, um
die Wahl eines Typs zu vermeiden. `about` nimmt Verweise beliebigen Typs
auf.

Eine Notiz hält fest, was bei einem Anlass anfiel: die Auswertung einer
Quelle, ein Protokoll, ein Gedanke. Überlebt ihr Gegenstand den Anlass, gehört
er in ein `concept`, und die Notiz verweist per `about` dorthin.
```

## 3.14 `specification`

```markdown
---
type: typedef
title: Spezifikation
description: Ein normatives Dokument, an das sich die Wissensbasis hält.
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| version | text | ja | — | Fassung, etwa `1.0` |
| url | hkf-url | nein | — | Kanonische Adresse |
| authority | hkf-link-or-text:organisation | nein | — | Herausgebende Stelle: als Verweis oder als Name |
| supersedes | hkf-link:specification | nein | — | Abgelöste Fassung |
| lang | hkf-lang | nein | — | Sprache des Dokuments |
| file | hkf-file:document / hkf-url | nein | — | Volltext: als Datei in der Ablage oder als Adresse |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Konventionen

Eine Quelle wird zitiert, eine Spezifikation wird eingehalten. Was man aus
einem Dokument erfahren hat, gehört als `source` in die Wissensbasis. Was
für sie verbindlich ist, gehört als `specification` hinein.

Der Body darf den Volltext tragen oder ihn nur zusammenfassen und über `url`
oder `file` auf ihn verweisen. Beides ist zulässig: Ein kurzes Dokument liegt
bequem in der Notiz, ein umfangreiches kostet Platz, den die meisten
Wissensbasen nie lesen.

Welche Spezifikation für die Wissensbasis selbst gilt, sagt `spec` in ihrer
Wurzeldatei (Core A.1).
```

## 3.15 `hint`

```markdown
---
type: typedef
title: Hinweis
description: Eine Festlegung, wie diese Wissensbasis geführt wird.
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| applies_to | hkf-link-list | nein | — | Worauf sich der Hinweis bezieht, meist eine Typdefinition |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Konventionen

Was ein Typ überall zusichert, steht im Abschnitt `# Konventionen` seiner
Typdefinition und reist mit ihr in jedes Bundle. **Ein Hinweis bindet
niemanden außerhalb.** In der Typdefinition steht darum, was `person`
überall bedeutet, in einem Hinweis, wie hier mit Personen verfahren wird.
Wer ihn gleichwohl weitergeben will, nimmt ihn in ein Bundle auf. Dann gilt
für ihn, was für jede gelieferte Notiz gilt (Core §5.5).

Eine Spezifikation kommt von außen und wird eingehalten, ein Hinweis wird
selbst gefasst. Deshalb trägt er weder `version` noch `authority`: Wer ihn
ändern will, ändert ihn.

Der Body sagt in einem Satz, was gilt, und danach, warum. Der Grund wiegt
schwerer als die Regel. Ein Hinweis ohne ihn lässt sich später weder prüfen
noch aufheben.

`applies_to` zeigt meist auf eine Typdefinition. Dann gilt der Hinweis für
jede Notiz dieses Typs. Ohne `applies_to` gilt er für die ganze
Wissensbasis.
```

## 3.16 `city`

```markdown
---
type: typedef
title: Stadt
description: Eine Stadt.
dir: Cities
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| geo | hkf-geo | nein | — | Koordinate als Paar, erst Breite, dann Länge |
| country | hkf-link:country | nein | — | Staat, in dem die Stadt liegt |
| part_of | hkf-link:place,country | nein | — | Übergeordnete Einheit, etwa Region, Provinz oder Staat |
| founded_year | hkf-year | nein | — | Jahr der Gründung, soweit überliefert |
| image | hkf-file:image / hkf-url | nein | — | Ansicht, als Datei in der Ablage oder als Adresse im Netz |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Ein Abschnitt, für den keine Quelle etwas hergibt, bleibt weg und wird nicht leer hingeschrieben. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Welche Stadt: wo sie liegt, zu welchem Staat sie gehört, wofür sie steht. |
| `## Geschichte` | Was in ihr geschah, soweit es hier zählt. |
| `## Bedeutung` | Warum sie hier steht. |

# Konventionen

Eine Stadt ist ein Ort, aber **HKF kennt keine Untertypen** (Core §3.7.1):
`hkf-link:place` nimmt keine `city` an. Wo ein Verweis beides zulassen soll,
werden beide genannt. `birthplace`, `seat` und `location` tun das und
schreiben `hkf-link:place,city,country`, ebenso `part_of` an `place`. Das
`part_of` einer Stadt lässt `city` aus: Eine Stadt liegt in einer Region oder
einem Staat, nicht in einer anderen Stadt.

Wer die Unterscheidung nicht braucht, führt `city` nicht und legt Städte als
`place` ab. Wer sie führt, entscheidet einmal und bleibt dabei: Dieselbe Stadt
zweimal, einmal als `place` und einmal als `city`, sind für jedes Werkzeug
zwei Gegenstände.

`geo` trägt beide Werte in einer Angabe, erst die Breite, dann die Länge.
```

## 3.17 `country`

```markdown
---
type: typedef
title: Staat
description: Ein Staat.
dir: Countries
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| code | hkf-country | nein | — | Kennung nach ISO 3166-1 alpha-2, etwa `DE` |
| capital | hkf-link:city | nein | — | Hauptstadt |
| founded_year | hkf-year | nein | — | Jahr der Staatsgründung |
| dissolved_year | hkf-year | nein | — | Jahr des Untergangs, wenn der Staat nicht mehr besteht |
| geo | hkf-geo | nein | — | Koordinate als Paar, erst Breite, dann Länge |
| flag | hkf-file:image / hkf-url | nein | — | Flagge, als Datei in der Ablage oder als Adresse im Netz |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Ein Abschnitt, für den keine Quelle etwas hergibt, bleibt weg und wird nicht leer hingeschrieben. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Welcher Staat: seit wann, in welchen Grenzen, mit welcher Verfassung. |
| `## Geschichte` | Was ihn hierher brachte, soweit es hier zählt. |
| `## Bedeutung` | Warum er hier steht. |

# Konventionen

`code` trägt die Kennung nach ISO 3166-1, mit der sich eine Staatsnotiz
gegen fremde Datenbestände abgleichen lässt. Sie ist eine Angabe **über**
den Staat und nicht der Weg, auf einen zu verweisen: Wer einen Staat nennt,
verweist auf seine Notiz (Core §3.7.3). Führt die Wissensbasis keine, bleibt
die Property leer.

`dissolved_year` macht den Typ für historische Bestände brauchbar: Ein Staat,
der untergegangen ist, bleibt der Staat, in dem jemand geboren wurde. Er wird
nicht gelöscht und nicht durch seinen Nachfolger ersetzt.

Ein Staat ist kein `organisation`. Die Regierung eines Staates ist eine
Körperschaft und bekommt eine eigene Notiz.
```

## 3.18 `daily`

```markdown
---
type: typedef
title: Tageseintrag
description: Was an einem Tag anfiel.
base: journal
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| about | hkf-link-list | nein | — | Worauf sich der Eintrag bezieht |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Konventionen

Der Gegenstand ist der Tag und nicht die Sache. Was den Tag überdauert,
bekommt eine eigene Notiz, und der Eintrag verweist per `about` dorthin.
Derselbe Schnitt wie bei `note`, nur vom Datum her: `note` hält einen Anlass
fest, `daily` einen Tag.

Der Eintrag liegt unter `journal_base`, nach Jahr und Monat geteilt, und trägt
kein Typverzeichnis (Core §3.2.5). Der Dateiname ist `jjjj-mm-tt` und stimmt
mit den Verzeichnissen über ihm überein.

**Es gibt keine Property `date`.** Der Pfad und der Dateiname sagen den Tag
schon, und eine Property daneben wäre die zweite Wahrheit über dieselbe
Tatsache, die Core §3.2 für den Ort ausschließt. Wer nach Datum sucht, sucht
nach dem Dateinamen.

Ein Tageseintrag ist keine Wissensnotiz und wird nicht zu einer. Er darf roh
bleiben, unvollständig und ohne Verbindungen. Geprüft wird an ihm dasselbe wie
an jeder Notiz, nicht mehr.
```

## 3.19 `summary`

```markdown
---
type: typedef
title: Zusammenfassung
description: Was eine Quelle sagt, auf drei Seiten.
dir: Summaries
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| summarizes | hkf-link:source | ja | — | Die Quelle, die zusammengefasst wird |
| covers | text | nein | — | Welcher Teil des Werks, wenn nicht das ganze, etwa `Kapitel 1 bis 3` |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Anders als bei
den übrigen Typen bleibt hier kein Abschnitt weg: Eine Zusammenfassung ohne
Kernaussagen oder ohne Vorschläge ist keine. `# Verbindungen` steht immer
zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Worum es in der Quelle geht, in wenigen Sätzen. |
| `## Kernaussagen` | Die tragenden Argumente und Erkenntnisse, jedes mit seiner Fundstelle im Werk. |
| `## Essayvorschläge` | Fünf Vorschläge, was sich aus der Quelle schreiben ließe, jeder mit seiner These in einem Satz. |

# Konventionen

Eine Quellennotiz gibt das Werk wieder, gegliedert nach dessen eigenem Aufbau,
und wächst mit ihm (§3.8). Eine Zusammenfassung ist die **Lektüre**: verdichtet,
begrenzt und um das ergänzt, was sich aus dem Werk machen ließe. Beide stehen
nebeneinander, weil das eine so lang wird wie sein Gegenstand und das andere
nicht.

**Drei Seiten sind die Grenze.** Der Body SOLLTE 9.000 Zeichen nicht
überschreiten, also rund drei Seiten DIN A4. Die Grenze ist der Zweck des Typs
und keine Formalie: Wer eine Zusammenfassung liest, will nicht das Werk noch
einmal lesen. Was nicht hineinpasst, gehört in die Quellennotiz oder in ein
`concept`.

**Die fünf Vorschläge gehören zur Notiz und sind kein Anhang.** Jeder nennt
eine These und einen Satz dazu, warum sie trägt. Geschrieben wird der Essay
woanders, unter `output_base` (Core §3.2.4). Ein Vorschlag behauptet nichts
über die Welt, darum bleibt die Zusammenfassung eine Wissensnotiz und wandert
nicht selbst unter die Erzeugnisse.

Fünf ist eine gesetzte Zahl und keine gemessene. Sie ist groß genug, dass es
beim Naheliegenden nicht bleibt, und klein genug, dass jeder Vorschlag noch
durchdacht ist.

`summarizes` nimmt genau eine Quelle und ist Pflicht: Eine Zusammenfassung
ohne ihr Werk sagt nicht, wovon sie handelt. Zwei Werke nebeneinanderzustellen
ist Sache eines `comparison` (§3.11).

Eine Quelle darf mehrere Zusammenfassungen tragen, etwa je Lesart oder je
Zweck, und sie braucht keine. Welcher Teil des Werks gemeint ist, sagt
`covers`. Ohne die Angabe gilt das ganze. Ein umfangreiches Werk wird oft in
Tranchen gelesen, und eine Zusammenfassung je Tranche ist besser als keine.

**Das Verzeichnis heißt `Summaries`.** Die Vorgabe aus Core §3.7 ergäbe
`Summarys`, wie sie bei `city` und `country` `Citys` und `Countrys` ergäbe
(§3.16, §3.17).
```

## 3.20 `quote`

```markdown
---
type: typedef
title: Zitat
description: Ein wörtlich übernommener Satz und seine Herkunft.
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| quotes | hkf-link:source | nein | — | Die Quelle, aus der das Zitat stammt |
| locator | text | nein | — | Fundstelle im Werk: Seite, Kapitel oder Zeitmarke, etwa `S. 112` oder `00:14:20` |
| said_by | hkf-link-or-text:person | nein | — | Wer den Satz gesagt oder geschrieben hat: als Verweis auf eine Personennotiz oder als Name |
| said_at | date | nein | — | Tag, an dem der Satz fiel, wenn er nicht mit dem Erscheinen der Quelle zusammenfällt |
| lang | hkf-lang | nein | — | Sprache des Zitats, wie es im Body steht |
| about | hkf-link-list | nein | — | Worauf sich das Zitat bezieht |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Verbindungen“ steht |

# Aufbau

Was eine Notiz dieses Typs beantwortet, in dieser Reihenfolge. Ein Abschnitt, für den keine Quelle etwas hergibt, bleibt weg und wird nicht leer hingeschrieben. `# Verbindungen` steht immer zuletzt (§5.6).

| Abschnitt | Beantwortet |
|---|---|
| ohne Überschrift | Das Zitat selbst, als Blockzitat und wörtlich. |
| `## Original` | Der Wortlaut in der Ausgangssprache, wenn oben eine Übersetzung steht. |
| `## Zusammenhang` | Wovon im Werk die Rede ist und an welcher Stelle der Satz fällt. |
| `## Zuschreibung` | Worauf die Zuschreibung beruht, wenn keine Quelle sie belegt. |

# Konventionen

**Nicht jedes Zitat wird eine Notiz.** Ein Zitat im Fließtext bleibt dort, wo
es etwas belegt, mitsamt seiner Fundstelle. Eine eigene Notiz bekommt ein
Satz, der an mehreren Stellen gebraucht wird oder selbst zum Gegenstand
geworden ist. Ohne diese Schranke zerfällt der Bestand in Schnipsel, die
niemand mehr einordnet.

**Der Wortlaut ist unantastbar.** Wörtlich heißt wörtlich: keine Glättung,
keine stille Kürzung, keine angepasste Zeitform. Eine Auslassung steht als
`[…]`, eine Einfügung in eckigen Klammern, eine Hervorhebung stammt aus dem
Original oder wird als eigene gekennzeichnet. Wer den Satz ändern will,
zitiert ihn nicht mehr, sondern gibt ihn wieder, und das gehört in die Notiz
zur Sache.

**Das Zitat steht im Body und nicht in einer Property.** Ein Satz mit
Anführungszeichen, Doppelpunkten und Zeilenumbrüchen wäre in YAML nur
maskiert unterzubringen und in keiner Ansicht mehr lesbar. Als Blockzitat im
Body bleibt er, was er ist, und lässt sich einbetten: Eine Notiz, die den
Wortlaut braucht, schreibt `![[Quotes/…]]` und nicht die Abschrift. So steht
der Satz einmal in der Ablage und nicht dreimal in drei Fassungen.

**Ohne `quotes` bleibt es eine Zuschreibung.** Ein geflügeltes Wort ohne Werk
darf eine Notiz bekommen, aber es steht schwächer da als ein belegter Satz,
und die Notiz sagt das selbst: `said_by` trägt den Namen, `## Zuschreibung`
sagt, wer den Satz wem seit wann zuschreibt und was dagegen spricht. Wo eine
Quelle vorliegt, gehört sie in `quotes`, und `locator` SOLLTE die Stelle
nennen. Ein Zitat, das sich nicht nachschlagen lässt, ist ein Gerücht über
einen Satz.

**`said_by` ist nicht der Urheber der Quelle.** In einem Interview spricht der
Befragte, verfasst hat das Werk der Fragende, und in einem Geschichtswerk
fällt der Satz bei einem Dritten. Fehlt die Angabe, gilt der Urheber der
Quelle aus `authors` (§3.8).

`said_at` trägt den Tag der Äußerung und nicht den der Veröffentlichung: Das
Werk erschien 1998, gesagt wurde der Satz 1919. Fallen beide zusammen, bleibt
die Property weg, denn `published` an der Quelle sagt es dann schon.

**Eine Übersetzung ohne Original ist kein Zitat.** Steht oben eine
Übersetzung, gehört der Ausgangswortlaut unter `## Original`, und `lang` nennt
die Sprache dessen, was oben steht. Wer nur die Übersetzung führt, führt eine
Wiedergabe, und die gehört in die Notiz zur Sache.

**Ein Zitat belegt ein Werk und ersetzt es nicht.** Es ist so lang wie nötig
und so kurz wie möglich. Eine Wissensbasis, die ganze Kapitel als Zitate
führt, ist eine Textsammlung mit fremdem Recht daran, und dagegen hilft keine
Property.
```

---

# 4. Konformität

Eine Wissensbasis führt HKF Config konform, wenn

1. sie HKF Core 1.0 erfüllt,
2. jede Typdefinition aus §3 und jeder Property-Typ aus §2 vorhanden ist und
   der dortigen Fassung entspricht — Verzeichnis, Property-Namen und deren
   Typangaben,
3. allein `city`, `country` und `summary` ein `dir` tragen, und zwar
   `Cities`, `Countries` beziehungsweise `Summaries`, und
4. die `values` der beiden Aufzählungen aus §2.2 nicht gekürzt wurden.

Vorhanden heißt: als Notiz in `Typedefs/` beziehungsweise `Proptypes/`. Ob
darunter Instanzen liegen, ist gleichgültig — eine Wissensbasis über
Werkstoffe führt `person` und benutzt es nie. Abwandeln darf sie keinen; wer
mehr braucht, legt einen eigenen Typ daneben (Core §3.7).

---

# 5. Versionierung

Diese Fassung ist **HKF Config 1.0** und setzt HKF Core 1.0 voraus.

Config wird getrennt von Core fortgeschrieben. Eine Minor-Version darf Typen
ergänzen, Property-Typen ergänzen, Properties ergänzen und die `values` der
Aufzählungen aus §2.2 erweitern. Sie darf keinen Typ, keinen Property-Typ,
keine Property und keinen Wert entfernen und keine Bedeutung ändern, weil das
vorhandene Notizen ungültig machte.

Eine Property, deren Typ-Angabe **erweitert** wird, ist davon nicht betroffen:
`hkf-link-list:person` zu `hkf-link-or-text-list:person` zu machen lässt jeden
bisher geschriebenen Wert gültig, weil er die erste Alternative erfüllt. Was
zulässig wird, ist eine Ergänzung; was unzulässig wird, ein Bruch.

Die Schranke wiegt hier schwerer als bei einer Lieferung: **Eine neue Fassung
erreicht bestehende Wissensbasen durch keinen Import**, weil nichts von hier
geliefert wird (§1). Wer fortschreibt, ergänzt in einer bestehenden Ablage von
Hand oder legt sie neu an. Was hier steht, muss beim Anlegen stimmen.

Welche Fassung eine Wissensbasis führt, sagt darum nicht sie selbst, sondern
`spec` in ihrer Wurzeldatei (Core A.1) — der Verweis auf das Dokument, dem sie
folgt.
