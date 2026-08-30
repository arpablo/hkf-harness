---
type: specification
title: HKF Base V1.0 — Standardvokabular
description: Neun Typdefinitionen und zwei Property-Typen für Person, Körperschaft, Ort, Ereignis, Quelle, Begriff, Thema, Notiz und Spezifikation. Wird als Bundle geliefert.
status: draft
---

# HKF Base V1.0

Diese Spezifikation legt ein **Vokabular** fest: neun Typen, die in nahezu
jeder Wissensbasis vorkommen und zugleich die häufigsten Verweisziele sind,
dazu zwei Property-Typen, die nur mit ihnen Sinn ergeben.

Sie setzt **HKF Core 1.0** voraus und wiederholt nichts daraus. Wie eine
Ablage aufgebaut ist, wie Property-Typen wirken, was ein qualifizierter
Wikilink ist und wie eine Typdefinition aussieht, steht dort. Verweise der
Form „Core §3.6" zeigen in jenes Dokument.

Der Unterschied ist keiner des Rangs, sondern der Verbindlichkeit. Core
beschreibt, was gilt, damit eine Ablage überhaupt lesbar ist. Base beschreibt
eine Verabredung darüber, wie man über Personen und Orte redet — nützlich,
weit verbreitet, aber ersetzbar. Eine Wissensbasis über Werkstoffe oder
Wertpapiere kommt ohne sie aus.

---

# 1. Lieferung

Base wird nicht angelegt, sondern **importiert**. Es kommt als Bundle mit der
Kennung `hkf-base`; seine `version` ist die Fassung dieses Dokuments, hier `1.0`.
Der Import ist der gewöhnliche `hk-import` aus Core §6.1, und danach steht in
`bundles/` eine Notiz, die festhält, was übernommen wurde.

Das Bundle enthält ausschließlich die Typdefinitionen aus §3 und die
Property-Typen aus §2. Keine Notizen, keine Mediendateien, keine
Grundausstattung — die hat die aufnehmende Wissensbasis bereits (Core §5.3).

Eine Wissensbasis **muss** Base nicht führen. Führt sie aber einen Typ dieses
Namens, MUSS er die hier festgelegte Bedeutung und das hier festgelegte
Verzeichnis haben. Nur so bleiben Bundles zwischen verschiedenen
Wissensbasen austauschbar.

Weil Base freiwillig ist, darf sich ein Inhalts-Bundle nicht darauf verlassen:
Es liefert die Typen mit, die es benutzt, oder nennt Base in
`required_bundles` (Core §4.1).

---

# 2. Property-Typen

Zwei Property-Typen gehören zu diesem Vokabular. Sie sind nicht Teil der
Grundausstattung, weil sie ohne die Typen `person` und `organisation` nichts
zu tun hätten.

| Property-Typ | Wertform | Werte |
|---|---|---|
| `hkf-person-category` | `text` | `artist`, `athlete`, `author`, `cleric`, `engineer`, `entrepreneur`, `jurist`, `musician`, `physician`, `politician`, `ruler`, `scholar`, `scientist`, `soldier` |
| `hkf-organisation-category` | `text` | `association`, `authority`, `company`, `foundation`, `institute`, `ngo`, `party`, `religious`, `school`, `union`, `university` |

Beide werden als **Listenform** verwendet (Core §3.5.2), also als
`hkf-person-category-list` und `hkf-organisation-category-list`. Eine Person
ist selten nur eines: Wer regiert hat, hat oft auch geschrieben und gedient.
Ebenso ist eine Landesuniversität zugleich `university` und `authority`. Ein
einwertiges Feld erzwänge eine Wahl, die die Sache nicht hergibt.

Die Werte beschreiben die **Rolle**, nicht den Beruf und nicht den Rang. Sie
sind bewusst grob: Feinere Unterscheidungen gehören in den Body oder in eigene
Property-Typen der jeweiligen Wissensbasis. Eine spätere Fassung von HKF Base
darf Werte ergänzen; entfernen darf sie keine, weil das vorhandene Notizen
ungültig machte.

---

# 3. Typdefinitionen

| Typ | Verzeichnis | Zweck |
|---|---|---|
| `person` | `persons` | Ein Mensch. |
| `organisation` | `organisations` | Eine Körperschaft: Unternehmen, Institut, Verein, Behörde. |
| `place` | `places` | Ein geographischer Ort. |
| `event` | `events` | Ein Geschehen zu einer bestimmten Zeit. |
| `source` | `sources` | Eine zitierbare Quelle: Buch, Aufsatz, Webseite, Vortrag. |
| `term` | `terms` | Ein definierter Begriff. |
| `topic` | `topics` | Ein Themengebiet als Einstiegspunkt. |
| `note` | `notes` | Eine Notiz ohne spezifischeren Typ. |
| `specification` | `specifications` | Ein normatives Dokument, an das sich die Wissensbasis hält. |

Kein Typ dieses Vokabulars trägt ein `dir`. Ihre Verzeichnisse ergeben sich
ausnahmslos aus der Vorgabe „Typname mit angehängtem `s`" (Core §3.7). Ein
Werkzeug kennt den Ablageort damit, ohne die Typdefinition zu lesen.

Alle aufgeführten Properties sind optional. Keiner dieser Typen fordert etwas
über `type` hinaus; er sichert nur zu, was die genannten Properties bedeuten.

## 3.1 `person`

```markdown
---
type: typedef
title: Person
description: Ein Mensch.
---

# Properties

| Property | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| full_name | text | nein | Vollständiger Name, wenn er vom Titel abweicht |
| born | date | nein | Geburtsdatum |
| born_year | hkf-year | nein | Geburtsjahr, wenn kein vollständiges Datum bekannt ist |
| died | date | nein | Sterbedatum |
| died_year | hkf-year | nein | Sterbejahr, wenn kein vollständiges Datum bekannt ist |
| birthplace | hkf-link:place | nein | Geburtsort |
| p_categories | hkf-person-category-list | nein | Rollen der Person |
| affiliations | hkf-link-list:organisation | nein | Zugehörigkeiten |
| homepage | hkf-url | nein | Persönliche Webseite |
| email | hkf-email | nein | Kontaktadresse |
| phone | hkf-phone | nein | Telefonnummer |
| portrait | hkf-file:image / hkf-url | nein | Bild der Person, als Datei in der Ablage oder als Adresse im Netz |
| wikidata_id | hkf-wikidata | nein | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

`born` und `born_year` schließen einander aus, ebenso `died` und `died_year`.
Der Dateiname ist `vorname-nachname` in kebab-case.
```

## 3.2 `organisation`

```markdown
---
type: typedef
title: Organisation
description: 'Eine Körperschaft: Unternehmen, Institut, Verein, Behörde.'
---

# Properties

| Property | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| founded | date | nein | Gründungsdatum |
| founded_year | hkf-year | nein | Gründungsjahr, wenn kein Datum bekannt ist |
| dissolved | date | nein | Auflösungsdatum |
| dissolved_year | hkf-year | nein | Auflösungsjahr, wenn kein Datum bekannt ist |
| o_categories | hkf-organisation-category-list | nein | Art der Körperschaft |
| seat | hkf-link:place | nein | Sitz |
| parent | hkf-link:organisation | nein | Übergeordnete Körperschaft |
| homepage | hkf-url | nein | Webseite |
| email | hkf-email | nein | Kontaktadresse |
| phone | hkf-phone | nein | Telefonnummer |
| logo | hkf-file:image / hkf-url | nein | Bildmarke, als Datei in der Ablage oder als Adresse im Netz |
| wikidata_id | hkf-wikidata | nein | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Rechtsform und Untergliederungen gehören in den Body, nicht in den Namen.
```

## 3.3 `place`

```markdown
---
type: typedef
title: Ort
description: Ein geographischer Ort.
---

# Properties

| Property | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| latitude | hkf-latitude | nein | Geographische Breite |
| longitude | hkf-longitude | nein | Geographische Länge |
| country | hkf-country | nein | Staat |
| address | text | nein | Anschrift in einer Zeile |
| part_of | hkf-link:place | nein | Übergeordneter Ort |
| image | hkf-file:image / hkf-url | nein | Ansicht, als Datei in der Ablage oder als Adresse im Netz |
| wikidata_id | hkf-wikidata | nein | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

`latitude` und `longitude` werden nur gemeinsam gesetzt. `part_of` bildet die
räumliche Schachtelung ab — Gebäude in Stadt, Stadt in Region.
```

## 3.4 `event`

```markdown
---
type: typedef
title: Veranstaltung
description: Ein Geschehen zu einer bestimmten Zeit.
---

# Properties

| Property | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| date | date | nein | Tag, wenn keine Uhrzeit bekannt ist |
| starts_at | datetime | nein | Beginn |
| ends_at | datetime | nein | Ende |
| location | hkf-link:place | nein | Veranstaltungsort |
| organizer | hkf-link:person,organisation | nein | Ausrichter |
| participants | hkf-link-list:person,organisation | nein | Beteiligte |
| cancelled | checkbox | nein | Abgesagt |
| homepage | hkf-url | nein | Ankündigung |
| related | hkf-link-or-url-list | nein | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Eine Veranstaltung trägt entweder `starts_at` oder `date`, nicht beides.
Zeiten gelten in der `timezone` der Ablage (Core §3.4).
```

## 3.5 `source`

```markdown
---
type: typedef
title: Quelle
description: 'Eine zitierbare Quelle: Buch, Aufsatz, Webseite, Vortrag.'
---

# Properties

| Property | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| authors | hkf-link-list:person | nein | Urheber |
| year | hkf-year | nein | Erscheinungsjahr |
| publisher | hkf-link:organisation | nein | Verlag oder Herausgeber |
| url | hkf-url | nein | Fundstelle im Netz |
| doi | hkf-url | nein | DOI, vollständig als `https://doi.org/…` |
| isbn | text | nein | ISBN |
| lang | hkf-lang | nein | Sprache der Quelle |
| accessed | date | nein | Datum des Abrufs |
| file | hkf-file:document | nein | Beigelegtes Dokument |
| wikidata_id | hkf-wikidata | nein | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Eine Quellennotiz beschreibt das zitierte Werk, nicht die eigene Auswertung.
Was man daraus gelernt hat, gehört in eine `note`, die per `sources` auf die
Quelle verweist.

`url` und `file` sind bewusst zwei Properties und keine Alternative (Core §3.7.2):
`url` ist die Fundstelle des Werks, `file` eine in der Ablage liegende
Ausfertigung. Beide dürfen nebeneinander gesetzt sein.
```

## 3.6 `term`

```markdown
---
type: typedef
title: Begriff
description: Ein definierter Begriff.
---

# Properties

| Property | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| lang | hkf-lang | nein | Sprache des Begriffs |
| broader | hkf-link:term | nein | Übergeordneter Begriff |
| sources | hkf-link-list:source | nein | Belege der Definition |
| wikidata_id | hkf-wikidata | nein | Kennung des Gegenstands in Wikidata |
| related | hkf-link-or-url-list | nein | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Der Body beginnt mit einer Definition in einem Satz. Synonyme werden als
Obsidian-`aliases` geführt, nicht als eigene Property.
```

## 3.7 `topic`

```markdown
---
type: typedef
title: Thema
description: Ein Themengebiet als Einstiegspunkt.
---

# Properties

| Property | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| parent | hkf-link:topic | nein | Übergeordnetes Thema |
| related | hkf-link-or-url-list | nein | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Ein Thema ordnet, ein Begriff definiert. Der Body ist eine Einstiegsseite mit
Verweisen; Inhalte, die anderswo hingehören, stehen nicht hier.
```

## 3.8 `note`

```markdown
---
type: typedef
title: Notiz
description: Eine Notiz ohne spezifischeren Typ.
---

# Properties

| Property | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| about | hkf-link-list | nein | Worauf sich die Notiz bezieht |
| sources | hkf-link-list:source | nein | Verwendete Quellen |
| related | hkf-link-or-url-list | nein | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

# Konventionen

Auffangtyp. Er wird verwendet, wenn kein anderer Typ passt — nicht, um die
Wahl eines Typs zu vermeiden. `about` nimmt Verweise beliebigen Typs auf.
```

## 3.9 `specification`

```markdown
---
type: typedef
title: Spezifikation
description: Ein normatives Dokument, an das sich die Wissensbasis hält.
---

# Properties

| Property | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| version | text | ja | Fassung, etwa `1.0` |
| url | hkf-url | nein | Kanonische Adresse |
| authority | hkf-link:organisation | nein | Herausgebende Stelle |
| supersedes | hkf-link:specification | nein | Abgelöste Fassung |
| lang | hkf-lang | nein | Sprache des Dokuments |
| file | hkf-file:document | nein | Beigelegter Volltext |
| related | hkf-link-or-url-list | nein | Verwandtes: Notizen oder Adressen; nimmt auf, was unter „Siehe auch" steht |

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

---

# 4. Konformität

Eine Wissensbasis führt HKF Base konform, wenn

1. sie HKF Core 1.0 erfüllt,
2. jeder geführte Typ aus §3 der dortigen Fassung entspricht — Verzeichnis,
   Property-Namen und deren Typangaben,
3. kein geführter Typ aus §3 ein `dir` trägt,
4. die beiden Property-Typen aus §2 vorhanden sind, sofern ein geführter Typ
   sie verwendet, und ihre `values` nicht gekürzt wurden, und
5. die Bundle-Notiz die Fassung nennt, in der das Vokabular übernommen wurde.

Eine Wissensbasis darf einzelne Typen aus §3 führen und andere weglassen.
Sie darf keinen davon abwandeln; wer mehr braucht, legt einen eigenen Typ
daneben (Core §3.7).

---

# 5. Versionierung

Diese Fassung ist **HKF Base 1.0** und setzt HKF Core 1.0 voraus.

Base wird getrennt von Core fortgeschrieben. Eine Minor-Version darf Typen
ergänzen, Properties ergänzen und die `values` der Property-Typen aus §2
erweitern. Sie darf keine Property und keinen Wert entfernen und keine
Bedeutung ändern, weil das vorhandene Notizen ungültig machte.

Fortschreibung in einer Wissensbasis ist ein erneuter Import: Der Vergleich
aus Core §6.1 übernimmt geänderte Notizen und überspringt unveränderte.
Welche Fassung geführt wird, sagt die `version` der Bundle-Notiz.
