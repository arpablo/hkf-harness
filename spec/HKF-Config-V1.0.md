---
type: specification
title: HKF Config V1.0 — Typen und Property-Typen
description: Zwanzig Typdefinitionen und sechzehn Property-Typen an einem Ort: die Grundausstattung jeder Wissensbasis und das Vokabular, das als Bundle dazukommt.
status: draft
---

# HKF Config V1.0

Dieses Dokument enthält alles, was HKF konkret festlegt: **jede Typdefinition
und jeden Property-Typ** — zwanzig und sechzehn. HKF Core beschreibt daneben nur noch, wie eine
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
die, die es gibt: vierzehn, die jede Ablage kennt, und zwei, die nur mit den
Typen aus §3 Sinn ergeben.

## 2.1 Die vierzehn Standard-Property-Typen

Diese vierzehn Property-Typen kennt jede HKB. Sie sind Teil dieser
Spezifikation und gehören zur **Grundausstattung**: Eine HKB legt sie beim
Anlegen als Notizen in `Proptypes/` an (Core §5.3).

| Property-Typ | Wertform | Einschränkung |
|---|---|---|
| `hkf-url` | `text` | `pattern: "^https?://\\S+$"` |
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

- Das Ziel MUSS in einem der vier Medienverzeichnisse aus Core §3.2.1 liegen und
  eine Dateiendung tragen, die nicht `.md` ist.
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
einen Namen trägt: Ein Verfasser ist manchmal eine Personennotiz und manchmal
die Zeile auf einem Titelblatt, eine Zugehörigkeit manchmal eine
`organisation` und manchmal die Angabe unter einem Aufsatztitel. Für jeden
davon eine Notiz anzulegen hieße, die Ablage mit Namen zu füllen, über die
nichts weiter zu sagen ist.

Geprüft wird der Reihe nach wie bei `hkf-link-or-url`: Sieht der Wert wie
`[[…]]` aus, gilt Core §3.6 samt Zieltyp — ein Tippfehler im Pfad bleibt also
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

## 2.2 Die beiden Aufzählungen

Zwei Property-Typen zählen Werte auf, statt eine Form einzuschränken. Sie
stehen für sich, weil sie ohne die Typen `person` und `organisation` nichts zu
tun hätten.

| Property-Typ | Wertform | Einschränkung |
|---|---|---|
| `hkf-person-category` | `text` | `values: [artist, athlete, author, cleric, engineer, entrepreneur, jurist, musician, physician, politician, ruler, scholar, scientist, soldier]` |
| `hkf-organisation-category` | `text` | `values: [association, authority, company, foundation, institute, ngo, party, religious, school, union, university]` |

Beide werden als **Listenform** verwendet (Core §3.5.2), also als
`hkf-person-category-list` und `hkf-organisation-category-list`. Eine Person
ist selten nur eines: Wer regiert hat, hat oft auch geschrieben und gedient.
Ebenso ist eine Landesuniversität zugleich `university` und `authority`. Ein
einwertiges Feld erzwänge eine Wahl, die die Sache nicht hergibt.

Die Werte beschreiben die **Rolle**, nicht den Beruf und nicht den Rang. Sie
sind bewusst grob: Feinere Unterscheidungen gehören in den Body oder in eigene
Property-Typen der jeweiligen Wissensbasis. Eine spätere Fassung von HKF Config
darf Werte ergänzen; entfernen darf sie keine, weil das vorhandene Notizen
ungültig machte.

---

# 3. Typdefinitionen

Zwanzig Typen. Die ersten drei sind die **Kern-Typen** — ohne sie ließe sich
keine Ablage beschreiben. Die siebzehn danach sind das **Vokabular**: Gegenstände,
die in nahezu jeder Wissensbasis vorkommen, die vier Arten von Quellen, und die
wenigen, mit denen eine Wissensbasis über sich selbst spricht.

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
| `book` | `Books` | Ein Werk für sich: Monographie, Sammelband, Bericht. |
| `article` | `Articles` | Ein Beitrag in einem größeren Werk: Zeitschrift, Zeitung, Sammelband. |
| `clipping` | `Clippings` | Eine erfasste Webseite; ihr Text steht im Body der Notiz. |
| `webpage` | `Webpages` | Eine zitierte Webseite; ihr Text bleibt draußen. |
| `term` | `Terms` | Ein definierter Begriff. |
| `concept` | `Concepts` | Eine Sache und der Stand des Wissens über sie. |
| `comparison` | `Comparisons` | Eine Gegenüberstellung mehrerer Gegenstände entlang benannter Dimensionen. |
| `topic` | `Topics` | Ein Themengebiet als Einstiegspunkt. |
| `note` | `Notes` | Eine Notiz ohne spezifischeren Typ. |
| `specification` | `Specifications` | Ein normatives Dokument, an das sich die Wissensbasis hält. |
| `hint` | `Hints` | Eine Festlegung, wie diese Wissensbasis geführt wird. |

**Zwei Typen tragen ein `dir`, die anderen achtzehn nicht.** Deren
Verzeichnisse ergeben sich aus der Vorgabe „Typname groß geschrieben, mit
angehängtem `s`" (Core §3.7); ein Werkzeug kennt den Ablageort damit, ohne die
Typdefinition zu lesen.

**Vier Typen tragen `is_source: true`** — `book`, `article`, `clipping` und
`webpage`. Ihre Verzeichnisse liegen nicht unter `wiki_base`, sondern unter
`source_base`, also nach Vorgabe in `Sources/Books`, `Sources/Articles`,
`Sources/Clippings` und `Sources/Webpages` (Core §3.2.2). Die Spalte oben
nennt das `dir`, nicht den vollen Pfad.

**Warum vier Typen und nicht ein `source` mit einer Werkart-Property.** Ein
Buch, ein Zeitschriftenaufsatz und eine Webseite wollen Verschiedenes: Das
Buch hat Verlag, Auflage und ISBN, der Aufsatz ein aufnehmendes Werk und
Seiten, die Webseite ein Abrufdatum. In einem Typ zusammengelegt stünden an
jeder Quellennotiz zwei Dutzend Properties, von denen die meisten immer leer
blieben — und keine Property-Tabelle könnte noch sagen, welche zu einer
vollständigen Zitation gehören. Der Typ trägt die Werkart besser als ein Feld
darin.

`clipping` gegen `webpage` ist die Unterscheidung zwischen **erfasst** und
**zitiert**. Ein Clipping bringt den Text der Seite mit und hält ihn im Body;
eine Webpage nennt nur die Adresse. Damit braucht HKF keine eigene
Rohtextschicht neben den Notizen — ein Clipping ist sie.

Die Vorgabe ist mechanisch und kein Sprachgefühl — bei `city` und `country`
ergäbe sie `Citys` und `Countrys`. Beide schreiben darum ein `dir` und heißen
`Cities` und `Countries`. Der Preis ist genau der, gegen den die Vorgaberegel
sonst schützt: Wer diese beiden Verzeichnisse sucht, muss die Typdefinition
lesen. Für zwei Namen, die jeder Leser sonst für einen Fehler hielte, ist er
tragbar.

Nicht zu verwechseln mit der Property `dir`, die `typedef` in §3.1 zusichert:
Die trägt eine *andere* Typdefinition, wenn sie abweichen will.

**Sieben Properties sind Pflicht**, alle übrigen optional: `description` in
`typedef`, `form` in `proptype`, `id` und `description` in `bundle`, `version`
in `specification`, `compares` in `comparison` und `lang` in `term`. Jede
trägt den Gegenstand ihrer Notiz — ein Property-Typ ohne Wertform, eine
Spezifikation ohne Fassung, ein Vergleich ohne Verglichene und ein Begriff
ohne Sprache sagen nichts. Sonst fordert keiner dieser Typen etwas über `type`
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
| description | text | ja | — | Einzeiliger Zweck; erscheint in der Typtabelle der Wurzeldatei |
| dir | text | nein | — | Verzeichnis der Instanzen; Vorgabe ist der groß geschriebene Typname mit angehängtem `s` (Core §3.7) |
| provisional | checkbox | nein | false | Beim Import angelegt, weil niemand den Typ definiert hat (Core §5.4) |
| is_source | checkbox | nein | false | Die Instanzen dieses Typs sind Quellen; ihr Verzeichnis liegt unter `source_base` statt unter `wiki_base` (Core §3.2.2) |

# Konventionen

Der Dateiname ist der Typname (Core §3.7). Der Body trägt die Property-Tabelle und
die Konventionen des Typs. `dir` ist ein relativer Pfad zum Basispfad, mit
`/` als Trennzeichen und beliebig vielen Abschnitten, ohne führenden und
abschließenden `/` und ohne `.`- oder `..`-Abschnitte; er darf nicht unter
`media_base` liegen und, wenn der Typ nicht `is_source: true` trägt, auch nicht
unter `source_base` (Core §3.2.2).

`provisional` steht nur an einer Typdefinition, nur mit dem Wert `true` und
nur in einer HKB — ein Bundle enthält keine vorläufige Typdefinition (Core §7.1).
Eine solche Notiz trägt kein `dir`, keinen Abschnitt `# Properties` und kein
`bundles`.

**Warum `is_source` und nicht `source`.** Der kürzere Name ist vergeben: `source`
ist die Property, mit der eine Bundle-Notiz sagt, woher die Lieferung stammt
(§3.3). Zwei Bedeutungen unter einem Namen wären genau die Namensdrift, gegen
die dieselbe Ablage anderswo lintet — und ein Schema, das über alle Notizen
gilt, könnte sie nicht auseinanderhalten.

`is_source` verschiebt allein den Ort und sonst nichts: Ein Quelltyp bestimmt
sein Verzeichnis über `dir` wie jeder andere, und die Vorgabe gilt
unverändert; nur hängt das Verzeichnis dann unter `source_base` statt unter
`wiki_base`. Die Angabe steht an der Typdefinition und nicht als Liste in der
Wurzeldatei, weil dort schon alles andere über den Typ steht — und weil eine
Ablage, die einen eigenen Quellentyp anlegt, sonst zwei Stellen ändern
müsste.
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
| pattern | text | nein | — | Regulärer Ausdruck; nur bei `text` und `list`, dort je Eintrag |
| values | list | nein | — | Erlaubte Werte; als Text geführt, auch wenn sie wie Zahlen aussehen |
| unit | text | nein | — | Maßeinheit; beschreibend, nicht geprüft |
| min | number | nein | — | Kleinster zulässiger Wert; nur bei `form: number` |
| max | number | nein | — | Größter zulässiger Wert; nur bei `form: number` |

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
| id | text | ja | — | Kennung der Lieferreihe in `kebab-case` (Core §4.1); in der HKB gleich dem Dateinamen |
| version | text | nein | — | Unveränderliche Kennung der gelieferten Fassung; ohne sie hat die Lieferung keine Geschichte, nur einen letzten Stand (Core §4.1) |
| description | text | ja | — | Ein Satz darüber, was die Lieferung enthält |
| required_bundles | list | nein | — | Bundles, die vorher importiert sein sollen (Core §4.1) |
| source | text | nein | — | Herkunft, etwa eine URL oder ein Repository |
| imported | datetime | nein | — | Zeitpunkt der Übernahme, in **UTC** (Core §3.4); nur in der HKB (Core §5.1). Fehlt es an einer Bundle-Notiz der HKB, wurde die Lieferung geprüft und nicht übernommen (Core §5.7) |

# Konventionen

Als `hbundle.md` in der Wurzel eines Bundles trägt die Notiz zusätzlich die
Wurzeldatei-Properties aus Core A.1 und die Typtabelle im Body; `imported` entfällt
dort. In der HKB liegt sie als `Bundles/<id>.md` ohne diese Zusätze.

`source` ist `text` und nicht `hkf-url`, weil auch ein Repository-Verweis oder
ein Datenträger als Herkunft in Frage kommt.

`description` ist bei einer Bundle-Notiz **Pflicht**, obwohl sie nach Core A.2 sonst
freigestellt ist: Wer eine Lieferung vor sich hat, muss ohne sie den Body lesen
oder die Dateien zählen, um zu erfahren, worum es geht. Sie ist zudem die
einzige Angabe, die in der Bundle-Liste einer Wissensbasis abfragbar ist.
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
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

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
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

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
| latitude | hkf-latitude | nein | — | Geographische Breite |
| longitude | hkf-longitude | nein | — | Geographische Länge |
| country | hkf-country | nein | — | Staat |
| address | text | nein | — | Anschrift in einer Zeile |
| part_of | hkf-link:place,city,country | nein | — | Übergeordneter Ort |
| image | hkf-file:image / hkf-url | nein | — | Ansicht, als Datei in der Ablage oder als Adresse im Netz |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

`latitude` und `longitude` werden nur gemeinsam gesetzt. `part_of` bildet die
räumliche Schachtelung ab — Gebäude in Stadt, Stadt in Region.
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
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Eine Veranstaltung trägt entweder `starts_at` oder `date`, nicht beides.
Zeiten gelten in der `timezone` der Ablage (Core §3.4).
```

## 3.8 `book`

```markdown
---
type: typedef
title: Buch
description: 'Ein Werk für sich: Monographie, Sammelband, Bericht.'
is_source: true
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| authors | hkf-link-or-text-list:person | nein | — | Urheber: als Verweis auf eine Personennotiz oder als Name, wie das Werk ihn nennt |
| subtitle | text | nein | — | Untertitel, wenn er zur Zitation gehört |
| editors | hkf-link-or-text-list:person | nein | — | Herausgeber, wenn sie von den Urhebern abweichen |
| publisher | hkf-link-or-text:organisation | nein | — | Verlag: als Verweis oder als Name |
| place | text | nein | — | Erscheinungsort |
| year | hkf-year | nein | — | Erscheinungsjahr |
| edition | text | nein | — | Auflage, etwa `2., überarbeitete Auflage` |
| volume | text | nein | — | Band; Text, weil auch `12A` vorkommt |
| pages | text | nein | — | Seitenzahl oder Umfang |
| isbn | text | nein | — | ISBN |
| doi | hkf-url | nein | — | DOI, vollständig als `https://doi.org/…` |
| lang | hkf-lang | nein | — | Sprache des Werks |
| url | hkf-url | nein | — | Fundstelle des Werks: wo es veröffentlicht ist |
| file | hkf-file:document / hkf-url | nein | — | Ausfertigung des Werks: als Datei in der Ablage oder als Adresse, etwa auf einem Dateiserver |
| accessed | date | nein | — | Datum des Abrufs |
| checksum | text | nein | — | `sha256:<hex>` über den erfassten Text; sagt beim nächsten Einlesen, ob sich die Quelle geändert hat |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Werks in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Ein Buch steht für sich: Es hat einen Verlag, oft eine ISBN, und es ist nicht
Teil eines größeren Werks. Ein Beitrag darin — ein Kapitel in einem
Sammelband — ist ein `article` mit diesem Buch als `container`.

`url` und `file` bezeichnen Verschiedenes und stehen darum als zwei
Properties da, nicht als Alternative (Core §3.7.2): `url` ist, **wo das Werk
veröffentlicht ist** — die Verlagsseite, die DOI-Adresse —, und damit
zitierfähig. `file` ist, **wo die eigene Ausfertigung liegt**: als Datei in
der Ablage oder als Adresse, etwa auf einem Dateiserver im eigenen Netz. Ein
Original muss also nicht in die Ablage kopiert werden, um verzeichnet zu sein.
Beide dürfen nebeneinander stehen.

Eine Quellennotiz beschreibt das zitierte Werk und fasst zusammen, **was es
sagt** — gegliedert nach seinem eigenen Aufbau, je Kapitel oder Hauptabschnitt
eine Überschrift. Was man daraus **für die eigene Sache schließt**, gehört
nicht hierher, sondern in eine `note` oder ein `concept`, das per `sources`
auf die Quelle verweist.
```

## 3.9 `article`

```markdown
---
type: typedef
title: Aufsatz
description: 'Ein Beitrag in einem größeren Werk: Zeitschrift, Zeitung, Sammelband.'
is_source: true
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| authors | hkf-link-or-text-list:person | nein | — | Urheber: als Verweis auf eine Personennotiz oder als Name, wie der Beitrag ihn nennt |
| subtitle | text | nein | — | Untertitel, wenn er zur Zitation gehört |
| editors | hkf-link-or-text-list:person | nein | — | Herausgeber des aufnehmenden Werks |
| container | text | nein | — | Das aufnehmende Werk: Zeitschrift, Zeitung, Sammelband |
| publisher | hkf-link-or-text:organisation | nein | — | Verlag: als Verweis oder als Name |
| place | text | nein | — | Erscheinungsort |
| year | hkf-year | nein | — | Erscheinungsjahr |
| volume | text | nein | — | Band oder Jahrgang; Text, weil auch `12A` vorkommt |
| pages | text | nein | — | Seitenbereich, etwa `34–56` |
| doi | hkf-url | nein | — | DOI, vollständig als `https://doi.org/…` |
| lang | hkf-lang | nein | — | Sprache des Werks |
| url | hkf-url | nein | — | Fundstelle des Werks: wo es veröffentlicht ist |
| file | hkf-file:document / hkf-url | nein | — | Ausfertigung des Werks: als Datei in der Ablage oder als Adresse, etwa auf einem Dateiserver |
| accessed | date | nein | — | Datum des Abrufs |
| checksum | text | nein | — | `sha256:<hex>` über den erfassten Text; sagt beim nächsten Einlesen, ob sich die Quelle geändert hat |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Werks in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Ein Aufsatz ist ein Beitrag und kein Werk für sich; `container` nennt, worin
er steht. Ohne diese Angabe lässt er sich nicht zitieren, sie ist aber
trotzdem nicht Pflicht: Eine Quelle wird oft eingelesen, bevor alle Angaben
beisammen sind, und eine Pflicht machte die Notiz bis dahin unschreibbar.

`url` und `file` bezeichnen Verschiedenes und stehen darum als zwei
Properties da, nicht als Alternative (Core §3.7.2): `url` ist, **wo das Werk
veröffentlicht ist** — die Verlagsseite, die DOI-Adresse —, und damit
zitierfähig. `file` ist, **wo die eigene Ausfertigung liegt**: als Datei in
der Ablage oder als Adresse, etwa auf einem Dateiserver im eigenen Netz. Ein
Original muss also nicht in die Ablage kopiert werden, um verzeichnet zu sein.
Beide dürfen nebeneinander stehen.

Eine Quellennotiz beschreibt das zitierte Werk und fasst zusammen, **was es
sagt** — gegliedert nach seinem eigenen Aufbau, je Kapitel oder Hauptabschnitt
eine Überschrift. Was man daraus **für die eigene Sache schließt**, gehört
nicht hierher, sondern in eine `note` oder ein `concept`, das per `sources`
auf die Quelle verweist.
```

## 3.10 `clipping`

```markdown
---
type: typedef
title: Erfasste Webseite
description: Eine erfasste Webseite; ihr Text steht im Body der Notiz.
is_source: true
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| authors | hkf-link-or-text-list:person | nein | — | Urheber: als Verweis auf eine Personennotiz oder als Name, wie die Seite ihn nennt |
| container | text | nein | — | Name der Website, auf der die Seite erschien |
| year | hkf-year | nein | — | Jahr der Veröffentlichung |
| lang | hkf-lang | nein | — | Sprache des Werks |
| url | hkf-url | nein | — | Fundstelle des Werks: wo es veröffentlicht ist |
| file | hkf-file:document / hkf-url | nein | — | Ausfertigung des Werks: als Datei in der Ablage oder als Adresse, etwa auf einem Dateiserver |
| accessed | date | nein | — | Datum des Abrufs |
| checksum | text | nein | — | `sha256:<hex>` über den erfassten Text; sagt beim nächsten Einlesen, ob sich die Quelle geändert hat |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Werks in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Der Body trägt zuerst die **Zusammenfassung**, darunter den **erfassten Text
der Seite**, so wie er abgerufen wurde. Die Reihenfolge ist nicht gleichgültig:
Ein Clipping bringt leicht tausend Zeilen mit, und was ein Leser zuerst
braucht, ist die Zusammenfassung — sie unter den Rohtext zu setzen macht sie
unauffindbar.

Der erfasste Text steht unter einer eigenen Überschrift, damit er sich vom
Geschriebenen trennen lässt und nicht so aussieht, als wäre er es.

Dass er überhaupt da ist, ist der Unterschied zu `webpage`, und er ist der
ganze Unterschied: Die Property-Tabellen der beiden sind gleich, aber ein
Clipping hat den Text, eine Webpage nur die Adresse. Wer wissen will, was
tatsächlich im Haus ist, sieht in `Clippings/` nach.

Damit braucht HKF keine eigene Rohtextschicht neben den Notizen: Ein Clipping
**ist** sie. `checksum` sagt beim nächsten Einlesen, ob sich die Seite seither
geändert hat — eine Webseite ändert sich still.

`url` und `file` bezeichnen Verschiedenes und stehen darum als zwei
Properties da, nicht als Alternative (Core §3.7.2): `url` ist, **wo das Werk
veröffentlicht ist** — die Verlagsseite, die DOI-Adresse —, und damit
zitierfähig. `file` ist, **wo die eigene Ausfertigung liegt**: als Datei in
der Ablage oder als Adresse, etwa auf einem Dateiserver im eigenen Netz. Ein
Original muss also nicht in die Ablage kopiert werden, um verzeichnet zu sein.
Beide dürfen nebeneinander stehen.

Eine Quellennotiz beschreibt das zitierte Werk und fasst zusammen, **was es
sagt** — gegliedert nach seinem eigenen Aufbau, je Kapitel oder Hauptabschnitt
eine Überschrift. Was man daraus **für die eigene Sache schließt**, gehört
nicht hierher, sondern in eine `note` oder ein `concept`, das per `sources`
auf die Quelle verweist.
```

## 3.11 `webpage`

```markdown
---
type: typedef
title: Webseite
description: Eine zitierte Webseite; ihr Text bleibt draußen.
is_source: true
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| authors | hkf-link-or-text-list:person | nein | — | Urheber: als Verweis auf eine Personennotiz oder als Name, wie die Seite ihn nennt |
| container | text | nein | — | Name der Website, auf der die Seite erschien |
| year | hkf-year | nein | — | Jahr der Veröffentlichung |
| lang | hkf-lang | nein | — | Sprache des Werks |
| url | hkf-url | nein | — | Fundstelle des Werks: wo es veröffentlicht ist |
| file | hkf-file:document / hkf-url | nein | — | Ausfertigung des Werks: als Datei in der Ablage oder als Adresse, etwa auf einem Dateiserver |
| accessed | date | nein | — | Datum des Abrufs |
| checksum | text | nein | — | `sha256:<hex>` über den erfassten Text; sagt beim nächsten Einlesen, ob sich die Quelle geändert hat |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Werks in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Eine Webseite wird zitiert, nicht erfasst: Der Body trägt die
Zusammenfassung, nicht den Text der Seite. Wer den Text behalten will, legt
ein `clipping` an.

`accessed` wiegt hier schwerer als bei jedem anderen Quelltyp. Eine Webseite
hat kein Erscheinungsjahr, auf das man sich verlassen könnte, und sie kann
morgen anders lauten; das Abrufdatum ist oft das einzige, was die Zitation
festhält.

`url` und `file` bezeichnen Verschiedenes und stehen darum als zwei
Properties da, nicht als Alternative (Core §3.7.2): `url` ist, **wo das Werk
veröffentlicht ist** — die Verlagsseite, die DOI-Adresse —, und damit
zitierfähig. `file` ist, **wo die eigene Ausfertigung liegt**: als Datei in
der Ablage oder als Adresse, etwa auf einem Dateiserver im eigenen Netz. Ein
Original muss also nicht in die Ablage kopiert werden, um verzeichnet zu sein.
Beide dürfen nebeneinander stehen.

Eine Quellennotiz beschreibt das zitierte Werk und fasst zusammen, **was es
sagt** — gegliedert nach seinem eigenen Aufbau, je Kapitel oder Hauptabschnitt
eine Überschrift. Was man daraus **für die eigene Sache schließt**, gehört
nicht hierher, sondern in eine `note` oder ein `concept`, das per `sources`
auf die Quelle verweist.
```

## 3.12 `term`

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
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Ein Begriff ist ein Ausdruck in **einer** Sprache, und `lang` nennt sie.
Darum ist sie Pflicht und keine Vorgabe: Derselbe Gegenstand heißt in drei
Sprachen dreierlei, und welche gemeint ist, darf nicht davon abhängen, in
welcher Wissensbasis die Notiz gerade liegt — ein Bundle bliebe sonst nicht
für sich lesbar (Core §4).

Der Body beginnt mit einer Definition in einem Satz. Synonyme werden als
Obsidian-`aliases` geführt, nicht als eigene Property; sie sind Ausdrücke
derselben Sprache. Die fremdsprachige Entsprechung ist kein Alias, sondern ein
eigener Begriff.

Ein Begriff legt einen Ausdruck fest und ist mit seiner Definition fertig.
Wird die Notiz länger, gehört, was über die Definition hinausgeht, in ein
`concept`.
```

## 3.13 `concept`

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
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

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

## 3.14 `comparison`

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
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Der Gegenstand eines Vergleichs ist kein Ding, sondern ein Verhältnis. Der
Body nennt zuerst, was verglichen wird und warum, dann die Dimensionen — am
besten als Tabelle mit einer Zeile je Dimension —, zuletzt das Urteil. Ein
Vergleich ohne Urteil ist eine Tabelle und gehört in die Notiz eines der
Verglichenen.

`compares` nimmt Verweise beliebigen Typs auf: Verglichen wird, was sich
vergleichen lässt — zwei Konzepte ebenso wie zwei Körperschaften. Was nur
einen der Gegenstände betrifft, gehört in dessen eigene Notiz.
```

## 3.15 `topic`

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
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Ein Thema ordnet, ein Begriff definiert, ein Konzept sammelt. Der Body ist
eine Einstiegsseite mit Verweisen; Inhalte, die anderswo hingehören, stehen
nicht hier.
```

## 3.16 `note`

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
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Auffangtyp. Er wird verwendet, wenn kein anderer Typ passt — nicht, um die
Wahl eines Typs zu vermeiden. `about` nimmt Verweise beliebigen Typs auf.

Eine Notiz hält fest, was bei einem Anlass anfiel: die Auswertung einer
Quelle, ein Protokoll, ein Gedanke. Überlebt ihr Gegenstand den Anlass, gehört
er in ein `concept`, und die Notiz verweist per `about` dorthin.
```

## 3.17 `specification`

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
| file | hkf-file:document | nein | — | Beigelegter Volltext |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Eine Quelle wird zitiert, eine Spezifikation wird eingehalten. Was man aus
einem Dokument erfahren hat, gehört als `source` in die Wissensbasis; was für
sie verbindlich ist, als `specification`.

Der Body darf den Volltext tragen oder ihn nur zusammenfassen und über `url`
oder `file` auf ihn verweisen. Beides ist zulässig: Ein kurzes Dokument liegt
bequem in der Notiz, ein umfangreiches kostet Platz, den die meisten
Wissensbasen nie lesen.

Welche Spezifikation für die Wissensbasis selbst gilt, sagt `spec` in ihrer
Wurzeldatei (Core A.1).
```

## 3.18 `hint`

```markdown
---
type: typedef
title: Hinweis
description: Eine Festlegung, wie diese Wissensbasis geführt wird.
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| applies_to | hkf-link-list | nein | — | Worauf sich der Hinweis bezieht; meist eine Typdefinition |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Was ein Typ überall zusichert, steht im Abschnitt `# Konventionen` seiner
Typdefinition und reist mit ihr in jedes Bundle. **Ein Hinweis bindet
niemanden außerhalb.** In der Typdefinition steht darum, was `person` überall
bedeutet; in einem Hinweis, wie hier mit Personen verfahren wird. Wer ihn
gleichwohl weitergeben will, nimmt ihn in ein Bundle auf — dann gilt für ihn,
was für jede gelieferte Notiz gilt (Core §5.5).

Eine Spezifikation kommt von außen und wird eingehalten, ein Hinweis wird
selbst gefasst. Deshalb trägt er weder `version` noch `authority`: Wer ihn
ändern will, ändert ihn.

Der Body sagt in einem Satz, was gilt, und danach, warum. Der Grund wiegt
schwerer als die Regel — ein Hinweis ohne ihn lässt sich später weder prüfen
noch aufheben.

`applies_to` zeigt meist auf eine Typdefinition; dann gilt der Hinweis für
jede Notiz dieses Typs. Ohne `applies_to` gilt er für die ganze Wissensbasis.
```

## 3.19 `city`

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
| latitude | hkf-latitude | nein | — | Geographische Breite |
| longitude | hkf-longitude | nein | — | Geographische Länge |
| country | hkf-link:country | nein | — | Staat, in dem die Stadt liegt |
| part_of | hkf-link:place,country | nein | — | Übergeordnete Einheit, etwa Region, Provinz oder Staat |
| founded_year | hkf-year | nein | — | Jahr der Gründung, soweit überliefert |
| image | hkf-file:image / hkf-url | nein | — | Ansicht, als Datei in der Ablage oder als Adresse im Netz |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Eine Stadt ist ein Ort, aber **HKF kennt keine Untertypen** (Core §3.7.1):
`hkf-link:place` nimmt keine `city` an. Wo ein Verweis beides zulassen soll,
werden beide genannt — `birthplace`, `seat`, `location` und `part_of` tun das
und schreiben `hkf-link:place,city,country`.

Wer die Unterscheidung nicht braucht, führt `city` nicht und legt Städte als
`place` ab. Wer sie führt, entscheidet einmal und bleibt dabei: Dieselbe Stadt
zweimal, einmal als `place` und einmal als `city`, sind für jedes Werkzeug
zwei Gegenstände.

`latitude` und `longitude` werden nur gemeinsam gesetzt.
```

## 3.20 `country`

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
| flag | hkf-file:image / hkf-url | nein | — | Flagge, als Datei in der Ablage oder als Adresse im Netz |
| wikidata_id | hkf-wikidata | nein | — | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

`code` und der Property-Typ `hkf-country` sagen dasselbe auf zwei Wegen, und
beide werden gebraucht. `place` trägt die Kennung unmittelbar, weil ein Ort in
einem Staat liegen kann, zu dem die Wissensbasis keine Notiz führt. Führt sie
eine, verweist sie darauf — und `code` verbindet die beiden Schreibweisen.

`dissolved_year` macht den Typ für historische Bestände brauchbar: Ein Staat,
der untergegangen ist, bleibt der Staat, in dem jemand geboren wurde. Er wird
nicht gelöscht und nicht durch seinen Nachfolger ersetzt.

Ein Staat ist kein `organisation`. Die Regierung eines Staates ist eine
Körperschaft und bekommt eine eigene Notiz.
```

---

# 4. Konformität

Eine Wissensbasis führt HKF Config konform, wenn

1. sie HKF Core 1.0 erfüllt,
2. jede Typdefinition aus §3 und jeder Property-Typ aus §2 vorhanden ist und
   der dortigen Fassung entspricht — Verzeichnis, Property-Namen und deren
   Typangaben,
3. allein `city` und `country` ein `dir` tragen, und zwar `Cities`
   beziehungsweise `Countries`, und
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
