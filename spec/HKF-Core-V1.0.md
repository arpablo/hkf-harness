---
type: specification
title: HKF Core V1.0 — Henni Knowledge Format
description: Der Kern des Formats — typbezogene Ablage, Wertformen, Property-Typen, qualifizierte Wikilinks, Bundle-Format und Methoden. Ohne Vokabular.
status: draft
---

# HKF Core V1.0

Diese Spezifikation beschreibt zwei Dinge:

- **HKF** — das **Bundle-Format**: eine übertragbare, für sich lesbare
  Sammlung von Notizen samt ihrer Typdefinitionen.
- **HKB** — die **Henni Knowledge Base**: ein Obsidian-Vault, der beliebig
  viele HKF-Bundles importieren und wieder exportieren kann.

Beide teilen denselben Kern: typbezogene Ablage, native Obsidian-Properties,
qualifizierte Wikilinks. Sie unterscheiden sich nur in ihrer Wurzeldatei und
darin, was sie zusätzlich dürfen.

HKF ist kein Ontologiesystem. Ein Typ ist ein Verzeichnis mit einer
Beschreibung. Mehr nicht.

## Core und Config

Das Format ist auf zwei Dokumente verteilt, weil es zwei Fragen beantwortet:

- **HKF Core** — dieses Dokument. Wie eine Ablage funktioniert: Verzeichnisse,
  Wertformen, Verweise, Typdefinitionen als Bauform, das Bundle-Format und die
  drei Methoden. Es nennt **keine einzige konkrete Definition**.
- **[HKF Config](HKF-Config-V1.0.md)** — das Inventar: siebzehn
  Typdefinitionen und fünfzehn Property-Typen. Drei Typen und dreizehn
  Property-Typen davon bilden die Grundausstattung jeder Ablage; die übrigen
  vierzehn Typen und zwei Property-Typen kommen als Bundle `hkf-base` und sind
  freiwillig.

Konform ist eine Wissensbasis nach **Core** samt der Grundausstattung aus
Config. Wer nur das erfüllt, hat eine leere, aber vollständige Ablage und
definiert seine Typen selbst. Wer das Vokabular lädt, verpflichtet sich
zusätzlich auf die dort festgelegte Bedeutung jener vierzehn Typen — der Preis
dafür, dass Bundles zwischen fremden Wissensbasen austauschbar sind.

Der Schnitt liegt zwischen **Mechanik und Inventar**. Dass eine Notiz in dem
Verzeichnis ihres Typs liegt, sagt Core. Welche Typen es gibt und dass eine
Person `born` und `died` trägt, sagt Config.

---

# 1. Kurzfassung (genug, um eine Ablage zu lesen und zu schreiben)

```text
HKB — Knowledge Base              HKF — Bundle
──────────────────────────────    ──────────────────────────────
hkb.md                            hbundle.md   ← einziger feststehender Ort
<base>/Typedefs/<typ>.md
<base>/Proptypes/<prop-typ>.md    beliebige Verzeichnisse:
<base>/Bundles/<id>.md            eine .md-Datei mit `type` ist eine Notiz,
<base>/<verzeichnis>/…            jede andere Datei eine Mediendatei nach
<media_base>/images/…             ihrer Endung, alles Übrige wird übergangen
<media_base>/videos/…
<media_base>/audios/…
<media_base>/documents/…
```

Eine Wissensbasis ist typbezogen abgelegt; **ein Bundle ist es nicht.** Dort
entscheidet der Inhalt einer Datei, was sie ist, nicht ihr Ort (§4.3). Der Baum
einer Wissensbasis beginnt im Verzeichnis ihrer Wurzeldatei und muss nicht die
Wurzel des Vaults sein.

1. **Lies die Wurzeldatei** — `hkb.md` oder `hbundle.md`. Bei einer
   Wissensbasis nennt sie den Basispfad und alle Typen mit Verzeichnis und
   Zweck; danach ist die ganze Ablage bekannt. Eine Bundle-Notiz braucht nur
   `id` und `description` (§4.1).
2. **Brauchst du einen Typ genauer, lies genau eine Datei:**
   `<base>/Typedefs/<typ>.md`. Ihre Property-Tabelle ist der vollständige
   Vertrag des Typs.
3. **Jede Notiz hat genau eine Pflicht-Property:** `type`.
4. **Jeder interne Verweis ist ein qualifizierter Wikilink:**
   `[[<pfad-ohne-.md>]]`, optional mit `|Anzeigetext`. In einem Bundle ist das
   der Pfad in der Lieferung; der Import schreibt ihn auf den Ort um, an dem
   die Notiz danach liegt.
5. **Drei Methoden der HKB:** `hk-import`, `hk-export`, `hk-lint`.
6. **Dieses Dokument nennt keine inhaltlichen Typen.** Welche Typen eine
   Wissensbasis führt, steht in der Typtabelle ihrer Wurzeldatei; in einer
   Lieferung sagt es der `type` jeder Notiz. Ein verbreitetes
   Vokabular liefert **HKF Config**.
7. **Grundausstattung und Zuladung.** Die dreizehn Property-Typen und die drei
   Kern-Typen entstehen mit der Wissensbasis — ohne sie ließe sich nichts
   importieren. Alles Weitere kommt als Bundle dazu und ist freiwillig (§5.3).
8. **Ein unbekannter Typ hält einen Import nicht auf.** Eine Notiz mit einem
   Typ, den die Wissensbasis nicht kennt, wird übernommen; für ihn entsteht
   eine vorläufige Typdefinition (§5.4). Führt die Wissensbasis den Namen
   dagegen bereits, muss vor der Übernahme entschieden werden, ob beide
   dasselbe meinen (§5.5). Wie entschieden wurde, hält die Bundle-Notiz fest,
   damit die nächste Fassung nicht dieselbe Frage auslöst (§5.7).
9. **Der Import verknüpft die Lieferung mit dem Bestand.** Was ankommt, wird
   in einem Abschnitt `# Siehe auch` mit dem verbunden, was schon da ist —
   je Verweis ein Grund, und nur in der Notiz, deren Body den anderen nennt.
   Die Gegenrichtung ist die Backlink-Ansicht (§5.6).

Mehr Kontext ist für das Lesen und Schreiben nicht nötig.

---

# 2. Begriffe

| Begriff | Bedeutung |
|---|---|
| **HKF-Bundle** | Übertragbare Sammlung von Notizen mit `hbundle.md` in der Wurzel. |
| **HKB** | Knowledge Base: Vault mit `hkb.md` in der Wurzel. |
| **Ablage** | Sammelbegriff für beides: ein Baum nach den Regeln von §3. |
| **Notiz** | Markdown-Datei mit YAML-Frontmatter und Body. |
| **Typ** | Name einer Notizart, registriert durch eine Typdefinition. |
| **Typdefinition** | Notiz mit `type: typedef` in `Typedefs/`. |
| **Wertform** | Einer der sechs nativen Obsidian-Property-Typen. |
| **Property-Typ** | Notiz mit `type: proptype` in `Proptypes/`; schränkt eine Wertform ein. |
| **Bundle-Notiz** | Notiz mit `type: bundle`; die Wurzeldatei eines Bundles. |
| **Notiz-ID** | Pfad der Notiz relativ zum Basispfad, ohne `.md`. |
| **Vorläufige Typdefinition** | Beim Import erzeugte Typdefinition für einen Typ, den niemand mitgeliefert hat; trägt `provisional: true` (§5.4). |
| **Bedeutungsprüfung** | Entscheidung, ob zwei gleichnamige Typen dasselbe meinen (§5.5). |
| **Siehe auch** | Maschinell gepflegter Abschnitt am Ende einer Notiz; hält Verweise mit ihrem Grund (§5.6). |
| **Entscheidungsnachweis** | Abschnitt `# Entscheidungen` einer Bundle-Notiz; hält fest, was ein Mensch geurteilt hat und woran es hängt (§5.7). |

---

# 3. Gemeinsamer Kern

Dieses Kapitel gilt für HKBs und für HKF-Bundles — mit einer Ausnahme, die
zweimal auftritt: **Ein Bundle ist nicht typbezogen abgelegt.** §3.2 und §3.2.1
beschreiben, wo Notizen und Mediendateien einer Wissensbasis liegen; in einer
Lieferung dürfen sie liegen, wo sie wollen, und was eine Datei ist, sagt ihr
Inhalt (§4.3). Alles Übrige — Wertformen, Property-Typen, Verweise,
Typdefinitionen — gilt für beide unverändert.

## 3.1 Wurzeldatei und Basispfad

Jede Ablage hat genau eine Wurzeldatei in ihrem Wurzelverzeichnis: `hkb.md`
bei einer HKB, `hbundle.md` bei einem Bundle. Sie ist keine Notiz im Sinne von
§3.3 und liegt in keinem Typverzeichnis.

Ihr Frontmatter trägt mindestens:

```yaml
hkf: "1.0"
base: ""
media_base: media
```

`base` ist der Basispfad für die Typverzeichnisse, relativ zur Wurzel, ohne
führenden und ohne abschließenden `/`. Optional; Vorgabe ist der leere Wert,
also die Wurzel. In einem Bundle bleibt `base` **ohne Wirkung**: Dort gibt es
keine Typverzeichnisse, unter denen ein Basispfad etwas zu verschieben hätte
(§4.3).

Eine Ablage muss nicht das ganze Vault sein. Ihr Wurzelverzeichnis ist
schlicht das Verzeichnis, in dem ihre Wurzeldatei liegt. Bei einer HKB heißt
der Pfad dorthin, von der Vault-Wurzel aus gerechnet, **Ablagepfad**; er ist
leer, wenn die HKB in der Vault-Wurzel liegt, und er steht in jedem Wikilink
vor der Notiz-ID (§3.6).

**Ein Bundle hat keinen Ablagepfad.** Es wird ausgeliefert und landet beim
Empfänger an beliebiger Stelle; seine Verweise sind deshalb immer auf die
Bundle-Wurzel bezogen und tragen nie einen Präfix. Liegt ein Bundle innerhalb
eines Vaults, kann Obsidian seine Verweise darum nicht richtig auflösen — im
Zweifel zeigt `[[Persons/ada-lovelace]]` dort auf die gleichnamige Notiz der
Wissensbasis. Das ist der Preis dafür, dass ein Bundle überall auspackbar
bleibt, und es ist der richtige Tausch: Ein Bundle ist eine Lieferung, kein
Arbeitsbereich.

`media_base` ist der Basispfad für die Medienverzeichnisse (§3.2.1), ebenfalls
relativ zur Wurzel und ohne führenden und abschließenden `/`. Optional;
Vorgabe ist der leere Wert, also ebenfalls die Wurzel. In einem Bundle bleibt
auch er ohne Wirkung: Dort erkennt man eine Mediendatei an ihrer Endung, nicht
an ihrem Verzeichnis (§4.3).

Ihr Body enthält den Abschnitt `# Typen`:

```markdown
# Typen

| Typ | Verzeichnis | Zweck |
|---|---|---|
| typedef | typedefs | Registriert einen Typ. |
| proptype | proptypes | Schränkt eine Wertform ein. |
| bundle | bundles | Beschreibt eine Lieferung. |
| person | persons | Ein Mensch. |
```

Die Tabelle ist **abgeleitet**: Sie fasst alle Typdefinitionen der Ablage
zusammen und wird von `hk-lint --fix` neu erzeugt. Sie existiert allein
deshalb, damit ein Werkzeug die gesamte Ablage aus einer einzigen Datei
kennt. Bei Abweichung gewinnen immer die Typdefinitionen.

**In `hbundle.md` ist der Abschnitt freigestellt und erläuternd.** Ein Bundle
hat keine Typverzeichnisse, also hat die Spalte „Verzeichnis" dort nichts zu
bezeichnen; welches Verzeichnis eine Notiz bekommt, entscheidet erst die
aufnehmende Wissensbasis (§4.3).

## 3.2 Typbezogene Ablage

**Dieser Abschnitt gilt für eine HKB.** Ein Bundle kennt keine
Typverzeichnisse; für seine Dateien gilt §4.3.

Alle Notizen liegen typbezogen unter dem Basispfad:

```text
<base>/<verzeichnis des typs>/<dateiname>.md
```

Unterverzeichnisse innerhalb eines Typverzeichnisses sind erlaubt.

Im Basispfad existieren **immer** die Verzeichnisse `Typedefs`, `Proptypes`
und `Bundles`. Dort liegen die Typdefinitionen, die Property-Typen und die
Bundle-Notizen. In einem Bundle bleibt `Bundles/` leer oder entfällt, weil
die Bundle-Notiz dort in der Wurzel liegt (§4).

Ein Pflichtverzeichnis, das leer bliebe, darf entfallen. Git kann leere
Verzeichnisse nicht abbilden, und ein über Git verteiltes Bundle verlöre sie
still. Ein Werkzeug legt ein fehlendes Verzeichnis an, sobald es etwas
hineinschreibt, und meldet sein Fehlen nicht.

**Zur Ablage gehört**, was unter ihrem Wurzelverzeichnis liegt: die
Wurzeldatei, die Typverzeichnisse unter `base` und die Medienverzeichnisse
unter `media_base`. Alles andere im Vault ist außerhalb von HKF und wird
weder geprüft noch verwaltet — eine Spezifikation, ein README, Notizen, die
zu keiner Wissensbasis gehören.

Eine Ablage darf **keine zweite Ablage enthalten**. Ein Werkzeug erkennt eine
Ablage an ihrer Wurzeldatei; läge unter einer weitere, wäre für jede Notiz
darin unklar, zu welcher sie gehört. Mehrere Ablagen nebeneinander in einem
Vault sind dagegen zulässig und der Normalfall, sobald Bundles in
Unterverzeichnissen liegen.

Die Wurzeldatei eines Bundles heißt `hbundle.md` und nicht `bundle.md` — der
kürzere Name gehört bereits der Typdefinition des Kern-Typs `bundle`, die als
`Typedefs/bundle.md` in jeder Ablage liegt. Ein Werkzeug, das nach
Wurzeldateien sucht, hielte sonst jede Ablage mit registriertem `bundle`-Typ
für verschachtelt.

Zusätzlich erkennt man eine Wurzeldatei an der Property `hkf`, die keine Notiz
trägt. Der Name allein sollte genügen; die Prüfung auf `hkf` macht die
Erkennung unabhängig davon, ob jemand eine Notiz `hbundle` nennt.

**Regeln**

1. Der Pfad bestimmt den Typ. Eine Notiz gehört zu dem Typ, unter dessen
   Verzeichnis sie liegt. `type` im Frontmatter MUSS damit übereinstimmen.
2. Verzeichnisnamen der Typen sind eindeutig; keines darf unter einem anderen
   liegen.
3. Dateinamen sind `kebab-case` und innerhalb ihres Typverzeichnisses
   eindeutig. Derselbe Name darf in verschiedenen Typverzeichnissen
   vorkommen.
4. Die **Notiz-ID** ist der Pfad ab dem Basispfad ohne `.md`, etwa
   `Persons/ada-lovelace`. Sie ist die Identität der Notiz **innerhalb einer
   Ablage**. Über zwei Ablagen hinweg sagt sie nichts: Zwei Bundles dürfen
   beide `Persons/john-smith` liefern und dabei zwei verschiedene Menschen
   meinen. Was der Import damit macht, steht in §6.1 Schritt 5.
5. Umbenennen oder Verschieben ändert die Identität. Ein Werkzeug MUSS
   dabei alle Verweise mitziehen.

### 3.2.1 Medienverzeichnisse

Mediendateien sind keine Notizen: Bilder, Videos, Tonaufnahmen und Dokumente.
**Auch dieser Abschnitt gilt für eine HKB**; in einem Bundle liegt eine
Mediendatei, wo sie will, und ihre Art ergibt sich aus der Endung (§4.3).

Sie liegen nicht in den Typverzeichnissen, sondern unter `media_base` in genau
vier Verzeichnissen:

```text
<media_base>/images/
<media_base>/videos/
<media_base>/audios/
<media_base>/documents/
```

| Verzeichnis | Medienart | Inhalt |
|---|---|---|
| `images` | `image` | Bilder, Grafiken |
| `videos` | `video` | Bewegtbild |
| `audios` | `audio` | Tonaufnahmen |
| `documents` | `document` | PDFs und andere Dokumente |

- Diese vier Namen sind unter `media_base` reserviert. Unmittelbar unter
  `media_base` darf **kein** anderes Verzeichnis liegen.
- Innerhalb der vier Verzeichnisse ist jede Unterstruktur erlaubt, etwa
  `images/personen/portraets/`.
- Ein Verzeichnis wird angelegt, sobald Medien seiner Art vorkommen.
- Kein Typverzeichnis darf unter `media_base` liegen und keines der vier
  Medienverzeichnisse darf als `dir` einer Typdefinition beansprucht werden.
- Die Medienart ergibt sich allein aus dem Verzeichnis, nicht aus der
  Dateiendung.

## 3.3 Notizen

Jede Notiz beginnt mit YAML-Frontmatter. Pflicht ist genau eine Property:

```yaml
type: person
```

Alles Weitere ist optional und frei. Empfohlen, aber nicht gefordert:
`title`, `description`, `tags`, `status`, `created`, `updated`. Ohne `title`
gilt der Dateiname als Titel.

Dass `type` die einzige Pflicht ist, ist keine Sparsamkeit, sondern die
Bedingung dafür, dass eine Notiz überall ankommt: Eine Wissensbasis kann sie
übernehmen, auch wenn sie ihren Typ nicht kennt — sie legt ihn dann vorläufig
an (§5.4).

Drei Properties führen die Geschichte einer Notiz: `created`, `modified` und
`modified_by` (Anhang A.2). In einem Bundle sind sie freigestellt, in einer
HKB werden sie geführt. **Wer eine Notiz maschinell ändert, MUSS `modified`
und `modified_by` setzen** — ein Sprachmodell trägt dort seinen Modellnamen
ein. Ohne das lässt sich beim Import nicht entscheiden, welche Fassung die
jüngere ist (§6.1).

Der Body ist gewöhnliches Markdown. HKF leitet aus dem Body nichts ab,
ausgenommen die fünf ausdrücklich normativen Strukturen: `# Typen` (§3.1),
`# Properties` (§3.7), `# Siehe auch` (§5.6) sowie Entscheidungsnachweis
(§5.7) und Importnachweis (§5.1) einer Bundle-Notiz. Werkzeuge MÜSSEN
unbekannte Properties unverändert erhalten.

## 3.4 Wertformen

Es werden ausschließlich die nativen Obsidian-Property-Typen verwendet:

| Obsidian-Typ | Wertform | Beispiel |
|---|---|---|
| Text | `text` | `type: person` |
| Liste | `list` | `tags: [mathematik, geschichte]` |
| Zahl | `number` | `capacity: 120` |
| Checkbox | `checkbox` | `cancelled: false` |
| Datum | `date` | `born: 1815-12-10` |
| Datum & Uhrzeit | `datetime` | `starts_at: 2026-10-14T18:15:00` |

Verschachtelte Abbildungen und Listen von Abbildungen sind **nicht** zulässig.
Strukturierte Information gehört als Liste oder Tabelle in den Body.

Weitere Regeln:

- Property-Namen sind `snake_case`.
- Leere Werte und `null` werden nicht geschrieben; eine unbekannte Property
  entfällt.
- Ein `datetime`-Wert ohne Uhrzeit bezeichnet den Tagesbeginn: `2026-08-27`
steht für `2026-08-27T00:00:00`. `hk-lint --fix` schreibt ihn aus, damit
Vergleiche nicht von der Schreibweise abhängen.

Zeiten stehen ohne Versatz im Muster `JJJJ-MM-TTTHH:mm:ss`. Welche Zone
gemeint ist, hängt davon ab, wovon die Zeit handelt — und die Grenze verläuft
genau dort, wo auch sonst die Grenze zwischen Notiz und Gegenstand verläuft:

| Zeitangabe | Zone |
|---|---|
| `modified` und `imported` — was Werkzeuge vergleichen | **UTC** |
| jede andere `datetime`, etwa `starts_at` — was in der Welt geschah | Ortszeit |

Die Ortszeit nennt die Wurzeldatei über die optionale Property `timezone`
(IANA-Zonenname); ohne Angabe gilt die Systemzone.

**Warum `modified` UTC ist.** Der Import entscheidet allein daran, welche
Fassung die jüngere ist (§6.1 Schritt 5). Als Ortszeit ist das nicht
entscheidbar: Zwei Wissensbasen in verschiedenen Zonen liefern Werte, die sich
nicht vergleichen lassen, ohne beide `timezone`-Angaben zu kennen — und im
Herbst kommt jede Ortszeit einmal doppelt vor, sodass selbst innerhalb einer
Zone eine Stunde lang keine Reihenfolge feststeht. Eine Vergleichszahl, die
einmal im Jahr mehrdeutig wird, ist als Vergleichszahl unbrauchbar.

**Warum kein Versatz im Wert steht.** Ein Wert mit `Z` oder `+02:00` wäre
selbsterklärend, verließe aber die native Wertform aus dieser Tabelle. HKF
kauft die Eindeutigkeit stattdessen mit einer Regel: Diese zwei Properties
sind UTC, alle anderen sind Ortszeit. Der Preis ist, dass zwei gleich
aussehende Werte Verschiedenes bedeuten — tragbar, weil beide UTC-Properties
von Werkzeugen geschrieben werden und keine von Hand gepflegt wird.

## 3.5 Property-Typen

Ein Property-Typ schränkt eine Wertform ein — etwa auf eine URL, eine
geographische Breite oder einen Wikilink. Er ist eine Notiz in `Proptypes/`;
der **Dateiname ist der Name des Property-Typs**.

Ein Property-Typ ist ein *Werttyp*, kein Property-Name. Welche Property eines
Konzepttyps welchen Property-Typ hat, sagt die Property-Tabelle der
Typdefinition (§3.7).

```markdown
---
type: proptype
form: text
pattern: "^https?://\\S+$"
---

Absolute HTTP- oder HTTPS-Adresse.
```

- `form` ist Pflicht und nennt eine der sechs Wertformen aus §3.4.
- Optional: `pattern` (regulärer Ausdruck; bei `form: list` je Eintrag),
  `values` (Liste erlaubter Werte), `unit`, `min`, `max`.
- Namen sind `kebab-case`. Das Präfix `hkf-` ist den Property-Typen dieser
  Spezifikation vorbehalten — gleich ob sie zur Grundausstattung gehören
  (§3.5.1) oder mit einem Bundle wie `hkf-base` kommen.

Für die sechs Wertformen selbst wird **kein** Property-Typ angelegt. Ebenso
wenig für Obsidian-eigene Properties wie `tags`, `aliases` und `cssclasses`.

### 3.5.1 Die Standard-Property-Typen

Dreizehn Property-Typen kennt jede HKB. Sie sind Teil dieser Spezifikation und
gehören zur **Grundausstattung**: Eine HKB legt sie beim Anlegen als Notizen in
`Proptypes/` an (§5.3).

**Welche es sind, steht in [HKF Config §2.1](HKF-Config-V1.0.md).** Dort stehen
Name, Wertform und Einschränkung jedes einzelnen, dazu was `hkf-wikidata`,
`hkf-file` und `hkf-link-or-url` bedeuten. Dieses Dokument sagt nur, was ein
Property-Typ ist (§3.5) und wie eine Property-Tabelle ihn benutzt (§3.7).

Ihre Bedeutung ist festgelegt und darf von einer Ablage nicht umdefiniert
werden. Ein Bundle darf sie weglassen, weil jede HKB sie ohnehin kennt; jede
andere verwendete Property-Typ-Notiz muss es mitliefern (§4).

### 3.5.2 Listenformen

Zu jedem Property-Typ gehört ohne weitere Definition eine **Listenform**. Sie
heißt wie der Property-Typ mit angehängtem `-list`:

> `<property-typ>-list` bezeichnet eine Property der Wertform `list`, deren
> Einträge **je einzeln** den Property-Typ `<property-typ>` erfüllen.

Damit sind `hkf-url-list`, `hkf-email-list`, `hkf-phone-list` und jede weitere
Listenform sofort verwendbar, ohne dass eine Notiz in `Proptypes/` angelegt
wird. Geprüft werden `pattern`, `values`, `min`, `max` und ein etwaiger
Zieltyp je Eintrag; `unit` gilt für alle Einträge gemeinsam.

- Die Listenform gibt es nur zu Property-Typen, deren `form` **nicht** `list`
  ist. `hkf-link-list-list` existiert nicht.
- `hkf-link-list` ist genau die so abgeleitete Listenform von `hkf-link`. Sie
  liegt zusätzlich als Notiz vor, weil sie besonders häufig gebraucht wird;
  die Regel liefert dasselbe Ergebnis. Ein Werkzeug MUSS ein `-list` deshalb
  **zuerst abtrennen** und erst dann entscheiden, welche Argumente ein `:`
  zulässt — sonst hält es `hkf-link-list:person` für unzulässig, obwohl §3.7.1
  es ausdrücklich erlaubt.
- Der Name eines eigenen Property-Typs darf nicht auf `-list` enden, damit er
  nicht mit einer Listenform verwechselt wird.
- Eine leere Liste wird nicht geschrieben; die Property entfällt dann (§3.4).

## 3.6 Verweise

Die Grammatik steht als ABNF in **Anhang B.2** und ist normativ; dieser
Abschnitt erläutert sie und nennt die Bedingungen, die sie nicht ausdrückt.

Jeder Verweis auf eine Notiz derselben Ablage ist ein **qualifizierter
Wikilink**: das Ziel ist der vollständige Pfad, unter dem die Zieldatei liegt,
ohne die Endung `.md`. Er setzt sich zusammen aus dem Ablagepfad (§3.1), dem
`base` und der Notiz-ID.

```markdown
[[Persons/ada-lovelace|Ada Lovelace]]
[[wissen/Persons/ada-lovelace|Ada Lovelace]]   ← bei base: wissen
```

Ein Verweis trägt **standardmäßig einen Alias** — den Teil hinter `|`. Der
vollständige Pfad ist für Werkzeuge da, für Lesende ist er Ballast: ohne Alias
steht mitten im Satz `test/Persons/ada-lovelace` statt `Ada Lovelace`. Der
Alias ist der `title` des Ziels, ersatzweise sein Dateiname; bei einer
Mediendatei ihr Dateiname samt Endung. Ein Verweis ohne Alias bleibt zulässig
und auflösbar, ist aber nicht die Vorzugsform — `hk-lint` meldet ihn als
Hinweis und `hk-lint --fix` ergänzt ihn.

Ein abweichender Alias ist erlaubt, wo der Satzbau ihn verlangt, etwa eine
gebeugte Form oder eine Kurzform.

**In einer Markdown-Tabelle wird der senkrechte Strich maskiert.** Er trennt
dort die Spalten, und ein unmaskierter Alias-Strich zerlegt die Zelle und
zerstört den Link:

```markdown
| [[Persons/ada-lovelace\|Ada Lovelace]] | person | neu |
```

Das ist derselbe Verweis; nur die Tabellenzeile verlangt das `\`. Ausserhalb
von Tabellen steht der Strich unmaskiert. `hk-lint` prüft beide Formen und
meldet einen unmaskierten Strich in einer Tabellenzelle als Fehler.

Auch in Properties. YAML verlangt dort Anführungszeichen:

```yaml
organizer: "[[Organisations/analytical-society|Analytical Society]]"
participants:
  - "[[Persons/ada-lovelace|Ada Lovelace]]"
  - "[[Persons/charles-babbage|Charles Babbage]]"
```

- Ein Wikilink ohne Verzeichnisanteil wie `[[ada-lovelace]]` ist nur dann
  konform, wenn die Zieldatei unmittelbar in der Wurzel der Ablage liegt —
  dann ist der Dateiname bereits der vollständige Pfad. Das trifft in der
  Praxis auf die Wurzeldatei zu: `[[hkb]]` und `[[hbundle]]` sind konform.
  Nicht `[[bundle]]` — so heißt die Typdefinition `Typedefs/bundle.md`, und
  ein Verweis darauf ist nach dieser Regel unzulässig, weil sie nicht in der
  Wurzel liegt (§3.2).
  Für jede Notiz in einem Typverzeichnis ist ein verzeichnisloser Link
  **nicht** konform, auch wenn Obsidian ihn auflösen könnte.
- `.md`, `./` und `../` kommen im Ziel nicht vor. Mediendateien behalten
  dagegen **immer** ihre Dateiendung, weil sie dort zum Namen gehört:
  `[[media/images/portraet-ada.png|portraet-ada.png]]`.
- In einer HKB bilden Ablagepfad und `base` zusammen den **Präfix** jedes
  Verweises. Er ist genau der Pfad, unter dem Obsidian die Datei findet; damit
  bleibt ein Verweis klickbar, auch wenn die Wissensbasis nur ein
  Unterverzeichnis des Vaults ist.
- In einem Bundle gibt es keinen Präfix. Das Ziel ist der Pfad der Datei
  **in der Lieferung**, ab deren Wurzel, ohne `.md` — welcher Pfad das ist,
  steht dem Absender frei (§4). Weil ein Bundle klein und für sich lesbar ist,
  genügt dort auch ein Ziel ohne Verzeichnis, solange genau eine Datei diesen
  Namen trägt; bei mehreren ist es mehrdeutig und wird beim Import gemeldet,
  nicht geraten.
- Der Import schreibt jedes dieser Ziele auf den Ort um, an dem die Notiz in
  der Wissensbasis landet (§6.1). Das ist kein Austausch eines Präfixes mehr,
  sondern eine vollständige Neuberechnung — der Pfad in der Lieferung und der
  Pfad in der Wissensbasis haben nichts miteinander zu tun.
- Import und Export tauschen genau diesen Präfix aus (§6) — mehr geschieht mit
  einem Verweis beim Wechsel zwischen Lieferung und Wissensbasis nicht.
- **Die Wurzeldatei verweist relativ zu sich selbst.** In `hkb.md` und
  `hbundle.md` — und in einer begleitenden Datei, die ein Werkzeug daneben
  erzeugt — beginnt ein Ziel beim Wurzelverzeichnis der Ablage, ohne
  Ablagepfad: `[[Specifications/hkf-core-1.0|HKF Core 1.0]]`. Diese Dateien
  beschreiben die Ablage von innen und dürfen nicht wissen müssen, wo sie im
  Vault liegt;
  sonst stünde der Ablagepfad doppelt da und ein Verschieben der Wissensbasis
  erzwänge, die Wurzeldatei umzuschreiben.

  Der Preis ist, dass Obsidian ein solches Ziel nur auflöst, solange es im
  Vault eindeutig ist. Das ist hinnehmbar: Diese Dateien tragen wenige
  Verweise, während eine Notiz zwischen Tausenden stehen kann.
- Externe Ziele werden als gewöhnliche Markdown-Links geschrieben.
- Ein Link trägt keine Beziehungsart. Die ergibt sich aus dem Property-Namen
  oder aus dem umgebenden Text.

## 3.7 Typdefinitionen

Eine Typdefinition registriert einen Typ. Der **Dateiname ist der Typname**.
Das folgende Beispiel ist ein gekürzter Auszug des Typs `person` aus HKF Config;
dort steht seine verbindliche Fassung.

```markdown
---
type: typedef
title: Person
description: Ein Mensch als Gegenstand der Wissensbasis.
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| born | date | nein | — | Geburtsdatum |
| died | date | nein | — | Sterbedatum |
| homepage | hkf-url | nein | — | Persönliche Webseite |
| email | hkf-email | nein | — | Kontaktadresse |
| employer | hkf-link:organisation | nein | — | Arbeitgeber |
| memberships | hkf-link-list:organisation | nein | — | Mitgliedschaften |

# Konventionen

Dateiname ist Nachname-Vorname in kebab-case.
```

- `dir` ist der Ablageort der Instanzen als **Pfad relativ zum Basispfad**.
  Optional; Vorgabe ist der Typname mit **großem Anfangsbuchstaben** und
  angehängtem `s`: aus `person` wird `Persons`. Die Kern-Typen und das
  Vokabular aus HKF Config kommen damit aus; nur ein Typ, der abweichend
  abgelegt werden soll, schreibt ihn.

  Die Regel ist mechanisch und kein Sprachgefühl: erster Buchstabe groß, Rest
  unverändert, `s` angehängt. `werkstoff` wird zu `Werkstoffs`, `hkf-link` zu
  `Hkf-links`. Der große Anfangsbuchstabe trennt die Verzeichnisse der Ablage
  auf einen Blick von allem anderen, was in einem Vault daneben liegt —
  `media`, `.obsidian`, was ein Mensch dazulegt. Er ist Teil der Vorgabe, nicht
  des Typnamens: Typnamen sind und bleiben klein (§3.7).

  Der Pfad darf mehrere Abschnitte haben. Damit lassen sich Typverzeichnisse
  gruppieren, ohne die Typnamen zu verlängern:

  ```yaml
  dir: Reihen                  # ein Abschnitt
  dir: Veranstaltungen/Reihen  # mehrere
  dir: Stammdaten/Kunde        # Gruppierung nach Herkunft
  ```

  Es gelten die Regeln aus §3.2: Kein `dir` darf unter einem anderen liegen,
  auch nicht unter einem der drei Pflichtverzeichnisse. `Stammdaten/Kunde` und
  `Stammdaten/Lieferant` sind nebeneinander zulässig — sie teilen sich ein
  Elternverzeichnis, aber keines liegt im anderen. `Stammdaten` selbst wäre
  dann für keinen weiteren Typ mehr frei.

  Ein Gruppierungsverzeichnis wie `Stammdaten` ist selbst **kein**
  Typverzeichnis. Eine Notiz, die unmittelbar darin läge, gehörte zu keinem
  Typ und wäre ein Befund (§3.7.1).
- `description` ist Pflicht und eine Zeile lang. Sie erscheint in der
  Typtabelle der Wurzeldatei und ist damit oft die einzige Information, die
  ein Werkzeug über einen Typ liest.
- Typnamen sind kleingeschrieben, aus Buchstaben, Ziffern und Bindestrichen,
  und in der Ablage eindeutig.

### Die Property-Tabelle

Der Abschnitt `# Properties` ist optional. Ist er vorhanden, ist er
**normativ** und wird von `hk-lint` geprüft.

- **Property** — der `snake_case`-Name im Frontmatter.
- **Typ** — entweder eine Wertform aus §3.4 oder der Name eines
  Property-Typs aus `Proptypes/`. Bei `hkf-link` darf ein Zieltyp, bei
  `hkf-file` eine Medienart angehängt werden (§3.7.1). Mehrere zulässige
  Typen werden mit ` / ` getrennt, und die Beschreibung nennt sie in Worten
  (§3.7.2).
- **Pflicht** — `ja` oder `nein`.
- **Vorgabe** — der Wert, als der die **fehlende** Property gelesen wird.
  `—` heißt: keine Vorgabe. Siehe unten.
- **Beschreibung** — freier Text. Stehen in der Typ-Spalte Alternativen, nennt
  sie die Beschreibung ausdrücklich, damit die Zeile für sich verständlich ist.

`type` wird nicht aufgeführt; es gilt für jede Notiz. Properties, die nicht
in der Tabelle stehen, sind weiterhin erlaubt und werden nicht geprüft
(§3.3). Die Tabelle beschränkt also nicht, sie sichert zu. Wer sehen will,
was außerhalb der Zusicherungen liegt, ruft `hk-lint --strict` (§6.3).

#### Die Vorgabe

§3.4 sagt: Eine unbekannte Property entfällt. Abwesenheit heißt dort also
„weiß ich nicht". Eine Vorgabe ist die Ausnahme davon — sie sagt für eine
einzelne Property, dass Abwesenheit etwas Bestimmtes heißt.

Sie wird **gelesen, nicht geschrieben**. Fehlt die Property, gilt der Wert; in
die Notiz kommt nichts. So wirkt `dir` schon heute: Eine Typdefinition ohne
`dir` legt ihre Instanzen unter dem groß geschriebenen Typnamen mit
angehängtem `s` ab, und keine Datei hält das fest. In der Spalte steht `dir` trotzdem nicht — dort stehen
nur **Werte**, keine Rechenvorschriften. Eine Vorgabe, die sich erst aus dem
Typnamen ergibt, bleibt Prosa.

Der Wert steht in der Wertform der Property, so wie er im Frontmatter stünde.
`hk-lint` prüft ihn gegen die Typ-Angabe wie jeden anderen Wert. Eine Vorgabe
an einer Pflicht-Property ist ein Widerspruch — was gefordert wird, darf nicht
zugleich fehlen dürfen — und ist ein Befund.

**Eine Vorgabe steht nur dort, wo die Abwesenheit wirklich diesen Wert
bedeutet.** Bei `cancelled` tut sie das: Eine Veranstaltung, an der niemand
etwas vermerkt hat, ist nicht abgesagt. Bei `lang` einer Quelle tut sie es
nicht — dort heißt die Abwesenheit „unbekannt", und die Sprache der
Wissensbasis vorzugeben machte aus einem französischen Buch stillschweigend
ein deutsches. Wo Abwesenheit „unbekannt" heißt, bleibt die Spalte leer.

Listen und Verweise brauchen darum keine: Eine fehlende Liste ist die leere
Liste und ein fehlender Verweis ist keiner, beides schon nach §3.4. Eine
fehlende Checkbox dagegen ist ohne Vorgabe schlicht unbekannt — deshalb tragen
`cancelled` und `provisional` eine.

Und eine Vorgabe reist mit der Typdefinition, nicht mit der Wissensbasis. Sie
darf nichts vorgeben, was von der aufnehmenden Ablage abhinge, sonst änderte
eine Notiz beim Import ihre Bedeutung. Aus demselben Grund führt `term` in HKF
Config seine Sprache als Pflicht und nicht als Vorgabe: Ein Bundle muss für sich
lesbar bleiben (§4).

### 3.7.1 Die Typ-Angabe

Ein Verweis in einer Property hat den Property-Typ `hkf-link` (ein Verweis)
oder `hkf-link-list` (mehrere). Beide sagen für sich nur, dass der Wert ein
qualifizierter Wikilink ist — nicht, worauf er zeigt. Der **Zieltyp** legt das
fest. Er steht in der Typ-Spalte der Property-Tabelle, nicht im Property-Typ,
denn derselbe Property-Typ wird an vielen Stellen mit verschiedenen Zielen
verwendet.

#### Schreibweise

Die Grammatik steht als ABNF in **Anhang B.3**; sie ist normativ, dieser
Abschnitt erläutert sie. Kurz gefasst: eine Wertform, ein Property-Typ mit
optionalem `-list`, oder `hkf-link` beziehungsweise `hkf-file` mit optionalem
`-list` und optionalem `:`-Zusatz. Mehrere Angaben werden mit ` / ` getrennt.

Die beiden Trennzeichen bedeuten Verschiedenes und stehen auf verschiedenen
Ebenen:

- `,` trennt **Argumente eines Typs**, ohne Leerzeichen — welche Zieltypen
  oder Medienarten er zulässt.
- ` / ` trennt **ganze Typen**, mit Leerzeichen auf beiden Seiten — welche
  Property-Typen der Wert überhaupt haben darf (§3.7.2). Die Leerzeichen sind
  Pflicht: Ohne sie liest sich `image/hkf-url` wie ein Pfad.

- Zwischen `hkf-link`, `:`, den Typnamen und den `,` steht **kein**
  Leerzeichen.
- `typname` ist der Dateiname einer Typdefinition ohne `.md`, also der
  Typname selbst — nicht sein Verzeichnis.
- Mehrere Typnamen bedeuten **oder**: das Ziel muss von einem der genannten
  Typen sein.
- Ohne `:` ist jeder Typ zulässig.
- Der `:`-Zusatz ist **ausschließlich** bei `hkf-link` und `hkf-file` samt
  ihren Listenformen erlaubt: bei `hkf-link` mit Typnamen, bei `hkf-file` mit
  Medienarten. An einer Wertform oder einem anderen Property-Typ ist er ein
  Fehler in der Typdefinition.

| Zelle | Bedeutung |
|---|---|
| `hkf-link` | ein Verweis auf eine Notiz beliebigen Typs |
| `hkf-link:organisation` | ein Verweis auf eine Notiz vom Typ `organisation` |
| `hkf-link:person,organisation` | ein Verweis auf eine Notiz vom Typ `person` **oder** `organisation` |
| `hkf-link-list:person` | eine Liste; **jeder** Eintrag verweist auf eine `person` |
| `hkf-file` | ein Verweis auf eine Mediendatei beliebiger Art |
| `hkf-file:image` | ein Verweis auf eine Datei unter `<media_base>/images/` |
| `hkf-file-list:image,video` | eine Liste aus Bildern und Videos |
| `hkf-file:image / hkf-url` | eine Datei **oder** eine Adresse — Alternative, §3.7.2 |

#### Auflösung

Der Typ eines Verweisziels wird **allein aus dem Pfad** bestimmt. Die
Zieldatei wird dafür nicht geöffnet. Das ist der Zweck der typbezogenen
Ablage aus §3.2: Ein Werkzeug prüft einen Verweis, ohne die verlinkte Notiz zu
lesen.

Für einen Wert wird der Reihe nach ermittelt:

1. **Wikilink erkennen.** Der Wert muss als Ganzes `[[ziel]]` oder
   `[[ziel|anzeigetext]]` sein. Der Anzeigetext ist für die Prüfung ohne
   Bedeutung. Ein Wert mit Text vor oder nach den Klammern ist kein Verweis
   und damit ein Formfehler.
2. **Ziel entnehmen.** `ziel` ist der Pfad ab der Wurzel der Ablage — bei
   einer Notiz ohne `.md`, bei einem Anhang mit seiner Dateiendung (§3.6).
   Ein verzeichnisloses oder relatives Ziel ist ein Verstoß gegen §3.6 und
   wird nicht geraten.
3. **Basispfad abziehen.** Beginnt `ziel` mit dem `base` der Ablage, wird
   dieses Präfix samt folgendem `/` entfernt. Übrig bleibt die Notiz-ID.
4. **Mediendatei erkennen.** Liegt `ziel` unter `<media_base>/images/`,
   `/videos/`, `/audios/` oder `/documents/`, ist es eine Mediendatei und
   keine Notiz. Die Medienart ergibt sich aus dem Verzeichnis. Ist eine
   Medienart gefordert, MUSS sie eine der genannten sein. Zulässig ist das
   nur für `hkf-file`; für `hkf-link` ist es ein Fehler. Die Prüfung endet
   hier. Für `hkf-file` endet sie umgekehrt hier auch dann, wenn das Ziel
   **keine** Mediendatei ist — dann als Fehler.
5. **Typverzeichnis suchen.** Gesucht wird die Typdefinition, deren `dir` ein
   **segmentweises Präfix** der Notiz-ID ist. Der Vergleich läuft über ganze
   Pfadsegmente: `Persons` ist ein Präfix von `Persons/historisch/ada`,
   aber nicht von `Persons-archiv/ada`. Nach §3.2 trifft höchstens eine
   Typdefinition zu.
6. **Tatsächlichen Typ bestimmen.** Er ist der Typname der gefundenen
   Typdefinition.
7. **Vergleichen.** Ist ein Zieltyp angegeben, MUSS der tatsächliche Typ
   einer der genannten sein. Der Vergleich ist exakt und
   groß-/kleinschreibungsempfindlich.

HKF kennt **keine** Ober- oder Untertypen. Ein Zieltyp passt nur auf sich
selbst; `hkf-link:organisation` akzeptiert keine Notiz vom Typ `verein`, auch
wenn ein Verein fachlich eine Organisation ist. Sollen beide zulässig sein,
werden beide genannt: `hkf-link:organisation,verein`.

Bei `hkf-link-list` wird jeder Eintrag einzeln nach diesem Verfahren geprüft.
Alle Einträge unterliegen derselben Zieltypangabe.

#### Beispiel

Gegeben `base: wissen` und die Typdefinitionen `person` → `Persons` sowie
`organisation` → `Organisations`:

```yaml
# in wissen/Persons/ada-lovelace.md
employer: "[[wissen/Organisations/analytical-society|Analytical Society]]"
```

| Schritt | Ergebnis |
|---|---|
| 1. Wikilink | Ziel `wissen/Organisations/analytical-society` |
| 2. Ziel | vollständiger Pfad, konform zu §3.6 |
| 3. Basispfad `wissen` abziehen | Notiz-ID `Organisations/analytical-society` |
| 4. Mediendatei? | nein, `Organisations` ist kein Medienverzeichnis |
| 5. Typverzeichnis | `Organisations` |
| 6. Tatsächlicher Typ | `organisation` |
| 7. Vergleich mit `hkf-link:organisation` | erfüllt |

#### Fehlerfälle

| Fall | Befund |
|---|---|
| Wert ist kein reiner Wikilink | Formfehler an der Notiz |
| Ziel ohne Verzeichnis, obwohl die Zieldatei nicht in der Wurzel liegt, oder Ziel mit `./`, `../`, `.md` | Verstoß gegen §3.6 an der Notiz |
| Ziel ist eine Mediendatei, der Typ ist `hkf-link` | Verweis auf eine Mediendatei statt auf eine Notiz |
| Ziel ist **keine** Mediendatei, der Typ ist `hkf-file` | Verweis auf eine Notiz statt auf eine Mediendatei |
| `hkf-file`-Ziel ohne Dateiendung oder mit `.md` | keine Mediendatei |
| Medienart des Verzeichnisses nicht unter den geforderten | Medienartfehler an der Notiz |
| Verzeichnis unmittelbar unter `media_base` ist keines der vier | Verstoß gegen §3.2.1 an der Ablage |
| Kein Typverzeichnis ist Präfix der Notiz-ID | Ziel ist keine Notiz — etwa `hkb.md` oder eine Datei außerhalb der Typverzeichnisse |
| Zieldatei existiert nicht | toter Verweis; der Zieltyp gilt trotzdem als geprüft, weil er aus dem Pfad folgt |
| Tatsächlicher Typ nicht unter den Zieltypen | Zieltypfehler an der Notiz |
| Genannter Zieltyp ist in der Ablage nicht registriert | Fehler an der **Typdefinition**, nicht an der Notiz |
| `:` an einer Wertform oder an einem anderen Property-Typ | Fehler an der Typdefinition |

Zieltypen gelten ausschließlich für Properties. Wikilinks im Body sind an
keinen Typ gebunden; sie müssen nur §3.6 erfüllen und auflösbar sein.

Was in einem Code-Span oder Codeblock steht, ist kein Verweis. Obsidian
verlinkt es nicht, und `hk-lint` prüft es nicht. Beispiel-Wikilinks in
erläuterndem Text — etwa in einer `proptype`-Notiz — gehören deshalb in
Backticks; sonst sind sie echte Verweise und müssen auflösbar sein.

### 3.7.2 Alternativen

Manche Properties dürfen auf zwei verschiedene Weisen belegt sein. Ein
Porträt etwa liegt entweder als Bild in der Ablage oder es steht im Netz. Für
solche Fälle nennt die Typ-Spalte mehrere Property-Typen, getrennt durch
` / ` — mit Leerzeichen, damit der Schrägstrich nicht als Pfadtrenner gelesen
wird:

```text
| portrait | hkf-file:image / hkf-url | nein | — | als Datei in der Ablage oder als Adresse im Netz |
```

**Die Beschreibung nennt die Alternativen in Worten.** Das ist keine Zierde:
Eine Typdefinition soll den vollständigen Vertrag ihres Typs tragen, ohne dass
man die Grammatik dieser Spezifikation kennt. Wer nur die Tabelle liest, muss
aus der Beschreibungsspalte erfahren, dass beides zulässig ist.

```yaml
portrait: "[[media/images/portraet-ada.png|portraet-ada.png]]"   # erste Alternative
portrait: https://example.org/ada.jpg                           # zweite Alternative
```

Ein Werkzeug liest den Trenner auch ohne Leerzeichen; geschrieben wird er mit.
`hk-lint --fix` ergänzt sie.

**Prüfung.** Die Alternativen werden der Reihe nach durchprobiert. Erfüllt der
Wert eine davon vollständig, ist die Property gültig. Erfüllt er keine, meldet
`hk-lint` einen Befund, der alle Alternativen nennt — er rät nicht, welche
gemeint war.

**Einschränkung.** Alle Alternativen MÜSSEN dieselbe Wertform haben. Obsidian
ordnet einem Property-Namen genau einen Property-Typ zu; eine Property, die
mal `text` und mal `number` wäre, ließe sich dort nicht führen.

- `hkf-file:image / hkf-url` ist zulässig — beide sind `text`.
- `hkf-file-list:image / hkf-url-list` ist zulässig — beide sind `list`.
- `hkf-url / hkf-year` ist unzulässig — `text` gegen `number`.
- `hkf-file:image / hkf-url-list` ist unzulässig — `text` gegen `list`.

Damit ergibt sich die Wertform der Property eindeutig aus jeder ihrer
Alternativen. Ein Verstoß ist ein Fehler an der Typdefinition, nicht an der
Notiz.

Eine Alternative ist kein Ersatz für zwei Properties. Sie ist am Platz, wenn
beide Formen **dasselbe** bezeichnen und sich ausschließen. Bezeichnen sie
Verschiedenes — etwa die Fundstelle einer Quelle und ihr beigelegtes
Dokument —, gehören sie in zwei Properties.

## 3.8 Kern-Typen

Jede Ablage registriert mindestens diese drei Typen. Die Vorgabe für `dir`
ergibt genau die drei Pflichtverzeichnisse aus §3.2.

| Typ | Verzeichnis | Zweck |
|---|---|---|
| `typedef` | `Typedefs` | Registriert einen Typ und legt sein Verzeichnis fest. |
| `proptype` | `Proptypes` | Schränkt eine Wertform ein. |
| `bundle` | `Bundles` | Beschreibt eine Lieferung. |

Ihre Typdefinitionen und die erlaubten Properties stehen in
[HKF Config §3.1 bis §3.3](HKF-Config-V1.0.md), zusammen mit allen übrigen.
Die Properties der Wurzeldateien und die notizübergreifenden Properties stehen
in Anhang A.

Mehr definiert dieses Dokument nicht. Jede Ablage ergänzt die Typen, die sie
braucht; ein verbreitetes Vokabular liefert **HKF Config**.

Die drei Kern-Typen und die dreizehn Property-Typen aus §3.5.1 bilden zusammen
die **Grundausstattung** einer HKB. Sie entsteht mit der Wissensbasis und wird
nicht geliefert: Ohne den Typ `typedef` ließe sich keine Typdefinition
ablegen, ohne `bundle` keine Lieferung verbuchen, ohne `proptype` kein
Property-Typ einordnen. Ein Import setzt sie voraus.

---

# 4. HKF — das Bundle-Format

Ein Bundle ist eine übertragbare, für sich lesbare Auswahl von Notizen. Es
folgt dem Kern aus §3, **mit einer Ausnahme: Es ist keine typbezogene Ablage.**
Seine Dateien dürfen liegen, wo sie wollen.

Darin liegt der Unterschied zwischen einer Wissensbasis und einer Lieferung. In
einer Wissensbasis bestimmt der Pfad den Typ (§3.2), weil dort tausend Notizen
nebeneinander liegen und ein Werkzeug jede einordnen können muss, ohne sie zu
öffnen. Eine Lieferung wird ausgepackt und ist danach vorbei; ihr
Verzeichnisbaum überlebt den Import nicht. Ihn vorzuschreiben hieße, dem
Absender eine Ordnung abzuverlangen, die niemand je zu Gesicht bekommt — und
die ihn zwänge, seinen Bestand vor dem Ausliefern umzusortieren.

Drei Festlegungen bleiben:

1. Die Wurzeldatei heißt `hbundle.md`, liegt in der Wurzel des Bundles und ist
   zugleich die Bundle-Notiz. Sie ist die einzige Datei, deren Ort feststeht.
2. **Was übernommen wird, entscheidet der Inhalt einer Datei, nicht ihr Ort**
   (§4.3). Eine Markdown-Datei mit `type` im Frontmatter ist eine Notiz; jede
   andere wird übergangen.
3. Das Bundle enthält **jede** Typdefinition und jeden Property-Typ, den
   seine Notizen verwenden, sowie jede Mediendatei, auf die sie verweisen.
   Zwei Ausnahmen, und beide beruhen darauf, dass die Sache garantiert
   vorhanden ist:

   - die **Grundausstattung** aus §3.8, die jede HKB führt;
   - alles, was ein **vorausgesetztes Bundle** liefert (§4.1). Wer `hkf-base`
     voraussetzt, darf die Typen aus HKF Config weglassen.

   Ohne eine solche Voraussetzung liefert ein Bundle auch die zugeladenen
   Typen mit, die es benutzt: Eine HKB muss sie nicht führen, ein Bundle darf
   sich ungefragt nicht auf sie verlassen.

Beide Bäume sind zulässig — der geordnete, den `hk-export` schreibt, und der
gewachsene, den jemand von Hand zusammenstellt:

```text
biografie-2026/                              rezeption/
  hbundle.md                                   hbundle.md
  Typedefs/person.md                           README.md          ← übergangen
  Typedefs/organisation.md                     typen/person.md
  Proptypes/hkf-url.md                         leute/ada.md
  media/images/portraet-ada.png                leute/babbage.md
  media/documents/notes-1843.pdf               scans/portraet.png
  Persons/ada-lovelace.md                      scans/notizen.pdf
  Organisations/analytical-society.md
```

Links steht, was ein Export erzeugt; rechts, was ein Import ebenso annimmt.
`typen/person.md` ist eine Typdefinition, weil sie `type: typedef` trägt, nicht
weil sie in einem Verzeichnis dieses Namens läge. `scans/portraet.png` wird ein
Bild, weil `.png` das sagt. `README.md` hat kein `type` und bleibt liegen.

Für Werkzeuge gilt damit: **streng im Schreiben, großzügig im Lesen.**
`hk-export` schreibt den geordneten Baum (§6.2), `hk-import` nimmt jeden (§6.1).

## 4.1 Die Bundle-Notiz

```markdown
---
type: bundle
id: biografie-2026
description: Fünf Notizen aus dem Umfeld der Analytical Engine, mit zwei Mediendateien.
---

Kurzbeschreibung des Inhalts.

# Typen

| Typ | Verzeichnis | Zweck |
|---|---|---|
| person | persons | Ein Mensch. |
| organisation | organisations | Eine Körperschaft. |
```

- `id` ist Pflicht und eine stabile Kennung der Lieferreihe. Sie ist
  `kebab-case`: Kleinbuchstaben, Ziffern und Bindestriche, beginnend mit einem
  Buchstaben.

  Das ist keine Formsache. Die `id` wird in der aufnehmenden Wissensbasis zum
  Dateinamen `Bundles/<id>.md` (§5.1), und in `required_bundles` trennt ein
  Leerzeichen sie von der Fassungsbedingung. Eine `id` mit Leerzeichen zerlegt
  also den Eintrag, der sie voraussetzt; eine mit `/` beansprucht ein
  Verzeichnis; eine mit Großbuchstaben kollidiert auf einem Dateisystem, das
  Groß- und Kleinschreibung nicht unterscheidet. Innerhalb einer Wissensbasis
  ist sie damit auch eindeutig — sie ist ja der Dateiname.
- `description` ist Pflicht: ein Satz darüber, was die Lieferung enthält.

**Mehr nicht.** `id` und `description` sind die beiden einzigen Pflichten einer
Bundle-Notiz. Das Beispiel oben ist ein vollständiges, konformes `hbundle.md`.
Alles Weitere ist Zugabe:

| Property | Wirkung, wenn sie fehlt |
|---|---|
| `version` | Die Lieferung führt keine Fassung. Der Importnachweis wird bei jedem Lauf neu geschrieben und ersetzt den vorherigen (§5.1); ein `>= X.Y` in einem fremden `required_bundles` ist damit nie erfüllt. |
| `hkf` | Die Lieferung erhebt keinen Anspruch auf eine Formatfassung. Die aufnehmende Wissensbasis liest sie nach ihrer eigenen und meldet es als Hinweis (§8). |
| `required_bundles` | Die Lieferung setzt nichts voraus. |
| `title`, `source` | Kein Anzeigename, keine Herkunftsangabe. |
| `base`, `media_base` | Nichts. Sie werden in einem Bundle **nicht ausgewertet** — es gibt dort keine Typverzeichnisse und keine Medienverzeichnisse (§4). Wo eine Datei liegt, ist gleichgültig; was sie ist, sagt ihr Inhalt (§4.3). Ein Bundle darf sie tragen, aber niemand liest sie. |

Der Body ist frei. Der Abschnitt `# Typen` aus §3.1 darf darin stehen und ist
dann **erläuternd, nicht normativ**: Die Spalte „Verzeichnis" hat in einem
Bundle nichts zu bezeichnen, weil die aufnehmende Wissensbasis das Verzeichnis
selbst bestimmt (§4.3).

**Die Property-Namen sind dieselben wie in einer Notiz** — kleingeschrieben,
Wörter durch `_` getrennt, also `snake_case` nach §3.4. `required_bundles`,
nicht `requiredBundles`; `media_base`, nicht `mediaBase`. Eine Bundle-Notiz ist
eine Notiz vom Typ `bundle` und wird in der Wissensbasis auch als solche
abgelegt (§5.1); zwei Schreibweisen für dieselbe Sache gäbe es nur, wenn die
Wurzeldatei eine eigene Welt wäre. Sie ist keine.

Ein Bundle enthält keine Bundle-Notizen anderer Bundles. Verschachtelte
Lieferungen gibt es nicht.

### Voraussetzungen

Ein Bundle darf verlangen, dass andere Bundles bereits in der Wissensbasis
liegen:

```yaml
required_bundles:
  - hkf-base >= 1.0
  - firmenglossar
```

Jeder Eintrag ist ein Text aus der `id` des vorausgesetzten Bundles und einer
optionalen Fassungsbedingung, getrennt durch ein Leerzeichen.

- **Ohne Bedingung** genügt jede Fassung. Das ist die allgemein anwendbare
  Form.
- **`>= X.Y`** ist erfüllt, wenn die vorhandene Fassung dieselbe Zahl vor dem
  Punkt trägt und die Zahl dahinter mindestens `Y` ist. `>= 1.0` wird also von
  `1.0` und `1.7` erfüllt, nicht von `0.9` und nicht von `2.0`.

`>=` ist der einzige Operator. Eine Obergrenze gibt es nicht: Ein Bundle kann
sinnvoll einen Mindeststand verlangen, aber nicht wissen, was künftige
Fassungen bringen. Dass die Zahl vor dem Punkt übereinstimmen muss, vertritt
die Obergrenze — sie wird erhöht, wenn eine Fassung Bestehendes bricht.

Führt das vorausgesetzte Bundle gar keine `version` (§4.1), ist eine
Fassungsbedingung nie erfüllt — es gibt nichts zu vergleichen. Wer ohne
Fassung ausliefert, lässt sich nur ohne Bedingung voraussetzen.

**Eine Fassungsbedingung ist nur zulässig, wenn beide Fassungen die Form
`Zahl.Zahl` haben.** Für `version` lässt §4.1 auch einen Versionsnamen oder
einen Commit-Hash zu; über solche Werte gibt es keine Ordnung, und ein
Werkzeug darf sie nicht raten. Ein Bundle, das mit Hashes versioniert wird,
lässt sich nur ohne Bedingung voraussetzen.

Ein Bundle darf sich nicht selbst voraussetzen, und Voraussetzungen dürfen
keinen Kreis bilden.

Eine unerfüllte Voraussetzung hält den Import nicht auf. Sie wird gemeldet,
und die Typen, die das fehlende Bundle definiert hätte, bleiben so lange
vorläufig (§5.4, §6.1). Eine Voraussetzung sagt also, in welcher Reihenfolge
zu laden ist, nicht, was ohne sie unmöglich wäre.

## 4.2 Zugehörigkeit

Notizen eines Bundles tragen **keine** Markierung ihrer Zugehörigkeit. Sie
liegen im Bundle, also gehören sie dazu. Ein Manifest gibt es nicht; das
Dateisystem ist das Manifest.

Erst beim Import in eine HKB entsteht daraus mehr: die Zugehörigkeit als
Property jeder Notiz (§5.2), der Importnachweis in der Bundle-Notiz (§5.1)
und die Verknüpfung mit dem Bestand (§5.6). Die erste sagt, was jetzt gilt;
der zweite, was damals geliefert wurde; die dritte, wie die Lieferung mit dem
zusammenhängt, was schon da war. Keines davon steht im Bundle, weil keines
die Lieferung beschreibt.

## 4.3 Was übernommen wird

Ein Bundle darf enthalten, was der Absender für nützlich hält — ein README,
eine Lizenz, Arbeitsdateien, einen Ordner mit Rohmaterial. Was davon in die
Wissensbasis gelangt, entscheidet allein der Inhalt der einzelnen Datei.

### Markdown-Dateien

Eine `.md`-Datei wird übernommen, **wenn sie YAML-Frontmatter mit `type`
trägt**. Mehr wird nicht verlangt; `type` ist auch in einer Wissensbasis die
einzige Pflicht (§3.3).

Jede andere `.md`-Datei wird **übergangen** — kommentarlos, nicht als Befund.
Sie ist kein Fehler, sondern Beiwerk der Lieferung. Genau das erlaubt einem
Bundle, ein README zu haben, ohne dass es als Notiz in der Wissensbasis landet.

`hbundle.md` ist ausgenommen: Sie trägt `type: bundle`, ist aber keine Notiz
(§3.1), sondern die Wurzeldatei. Eine weitere Datei mit `type: bundle` gehört
nicht in ein Bundle (§4.1).

**Wohin die Notiz kommt.** Nicht dorthin, wo sie in der Lieferung lag, sondern
nach `<base>/<dir des Typs>/<dateiname>` in der aufnehmenden Wissensbasis. Das
`dir` steht in deren Typdefinition; kennt sie den Typ nicht, entsteht eine
vorläufige und es gilt die Vorgabe aus §3.7 (§5.4). Der Dateiname bleibt.

Tragen zwei Dateien einer Lieferung denselben Typ **und** denselben
Dateinamen, ergäben sie dieselbe Notiz-ID. Das ist ein Konflikt: melden, nichts
schreiben. In der Lieferung lagen sie in verschiedenen Verzeichnissen und
konnten nebeneinander bestehen; in der Wissensbasis können sie es nicht.

### Alle anderen Dateien

Jede Datei, die nicht auf `.md` endet, wird als **Mediendatei** übernommen.
Ihre Medienart ergibt sich aus der Dateiendung:

| Medienart | Endungen |
|---|---|
| `image` | `png` `jpg` `jpeg` `gif` `webp` `svg` `avif` `bmp` `tif` `tiff` `heic` |
| `video` | `mp4` `mov` `webm` `mkv` `avi` `m4v` |
| `audio` | `mp3` `m4a` `wav` `flac` `ogg` `opus` `aac` |
| `document` | alle übrigen |

**Im Zweifel `document`.** Eine unbekannte Endung ist kein Grund, eine Datei
liegen zu lassen — sie ist ein Dokument, bis jemand es besser weiß. Die drei
anderen Arten sind Ausnahmen von dieser Regel, keine Bedingung für die
Übernahme.

Nicht übernommen wird, was offensichtlich nicht zum Inhalt gehört: Dateien und
Verzeichnisse, deren Name mit einem Punkt beginnt — `.git`, `.obsidian`,
`.DS_Store`. Ohne diese Ausnahme trüge jede über Git verteilte Lieferung ihre
Versionsgeschichte als Dokumente in die Wissensbasis.

**Wohin die Mediendatei kommt.** Nach `<media_base>/<medienart>/<restpfad>`.
Der `restpfad` ist der Pfad in der Lieferung, von dem ein führendes `media/`
und ein anschließendes Verzeichnis mit dem Namen der Medienart entfernt wurden:

```text
media/images/personen/portraet.png   →  <media_base>/images/personen/portraet.png
scans/portraet.png                  →  <media_base>/images/scans/portraet.png
portraet.png                        →  <media_base>/images/portraet.png
```

Die erste Zeile ist der geordnete Baum aus §6.2: Er kommt unverändert an. Die
zweite behält ihr Verzeichnis, weil es sonst zwei `portraet.png` gäbe, sobald
eine Lieferung dasselbe Bild in zwei Ordnern führt.

### Die Umkehrung der Medienregel

In der Wissensbasis ergibt sich die Medienart **allein aus dem Verzeichnis**,
nicht aus der Dateiendung (§3.2.1). In der Lieferung ist es umgekehrt. Das ist
kein Widerspruch, sondern die Übersetzung, die der Import leistet: Er liest die
Endung und schreibt das Verzeichnis. Danach gilt wieder das Verzeichnis, und
eine falsch benannte Datei lässt sich durch Verschieben richtigstellen, ohne
sie umzubenennen.

---

# 5. HKB — die Knowledge Base

Eine HKB ist eine Ablage nach §3 in einem Obsidian-Vault, mit diesen
Zusätzen:

1. Ihre Wurzeldatei heißt `hkb.md` und liegt in ihrem Wurzelverzeichnis. Das
   darf die Vault-Wurzel sein, muss es aber nicht: Eine HKB darf ebenso gut
   in einem Unterverzeichnis liegen, dann ist dessen Pfad ihr Ablagepfad.
2. `base` darf gesetzt sein und verschiebt alle Typverzeichnisse innerhalb
   der HKB dorthin.
3. Sie enthält die Standard-Property-Typen aus §3.5.1.
4. Sie führt `Bundles/` mit einer Notiz je importiertem oder exportierbarem
   Bundle.
5. Sie stellt die Methoden aus §6 bereit.

```markdown
---
hkf: "1.0"
name: Henni Knowledge Base
base: ""
media_base: media
timezone: Europe/Berlin
---

# Typen

| Typ | Verzeichnis | Zweck |
|---|---|---|
| typedef | typedefs | Registriert einen Typ. |
| proptype | proptypes | Schränkt eine Wertform ein. |
| bundle | bundles | Beschreibt eine Lieferung. |
| person | persons | Ein Mensch. |
```

`name` ist ein freier Anzeigename und Pflicht. `timezone` ist optional.

Beispiel mit `base: wissen`:

```text
hkb.md
wissen/Typedefs/person.md
wissen/Proptypes/hkf-url.md
wissen/Bundles/biografie-2026.md
wissen/Persons/ada-lovelace.md
media/images/portraet-ada.png
```

`base` und `media_base` sind voneinander unabhängig. Die Medienverzeichnisse
liegen hier neben dem Basispfad, nicht darin.

## 5.1 Bundle-Notizen in der HKB

Ein importiertes Bundle wird als `<base>/Bundles/<id>.md` abgelegt. Es ist
dieselbe Notiz wie `hbundle.md` im Bundle, mit zwei Unterschieden:

- Die Wurzeldatei-Properties `hkf`, `base` und `media_base` sowie die
  Typtabelle im Body entfallen, weil sie in der HKB von `hkb.md` kommen.
- `imported` (datetime) hält den Zeitpunkt der Übernahme fest.

```markdown
---
type: bundle
id: biografie-2026
title: Biografische Notizen, Ausgabe 2026
description: Fünf Notizen aus dem Umfeld der Analytical Engine, mit zwei Mediendateien.
source: https://example.org/biografie.git
version: "4c73e21"
imported: 2026-08-27T11:00:00
---

Kurzbeschreibung des Inhalts.
```

Der Dateiname entspricht der `id`. Eine HKB darf beliebig viele Bundles
importieren.

Im Body steht zuerst die Kurzbeschreibung, dann der Abschnitt
`# Entscheidungen` (§5.7), dann die Importnachweise. Die Reihenfolge folgt der
Haltbarkeit: Entscheidungen gelten weiter, Nachweise sind Geschichte.

### Der Importnachweis

Der Body der Bundle-Notiz hält fest, was eine Lieferung **zum Zeitpunkt ihres
Imports** enthielt. Je übernommener Fassung entsteht ein Abschnitt
`# Import <version>`, die neueste zuerst:

```markdown
# Import a3f9c21

Übernommen am 2026-08-27T12:45:00.

| Notiz | Typ | Zustand |
|---|---|---|
| [[Persons/ada-lovelace\|Ada Lovelace]] | person | neu |
| [[Persons/charles-babbage\|Charles Babbage]] | person | neu |
| [[Places/london\|London]] | place | aktualisiert |

| Mediendatei | Medienart | Zustand |
|---|---|---|
| [[media/images/portraet-ada.png\|portraet-ada.png]] | image | neu |

| Verweis | Gegenstelle | Grund |
|---|---|---|
| [[Persons/ada-lovelace\|Ada Lovelace]] | [[Places/london\|London]] | beide nennen einander |
```

- Die erste Spaltenüberschrift unterscheidet die drei Tabellen: `Notiz`,
  `Mediendatei` und `Verweis`. Eine Tabelle entfällt, wenn die Lieferung
  nichts der Art hervorgebracht hat.
- Die dritte Tabelle hält fest, was die Verknüpfung angelegt hat (§5.6).
  Sie ist die einzige Stelle, an der ein Import nachweist, dass er eine
  Notiz **außerhalb** der Lieferung angefasst hat; die Gegenstelle steht
  darum ausdrücklich dabei.
- Die Einträge sind qualifizierte Wikilinks nach §3.6, also die Pfade **in
  der HKB**, nicht die der Lieferung.
- `Zustand` ist `neu`, `aktualisiert` oder `übersprungen` — was der Import mit
  dem Eintrag getan hat.
- Ein Abschnitt wird **einmal** geschrieben, wenn seine Fassung zum ersten Mal
  ankommt. Ein wiederholter Import derselben `version` lässt ihn unverändert;
  sonst stünde beim zweiten Lauf überall `übersprungen` und der Nachweis
  bezeichnete nicht mehr den Zeitpunkt des Imports.
- Führt die Lieferung **keine `version`** (§4.1), gibt es nichts, woran ein
  Abschnitt festzumachen wäre. Die Überschrift lautet dann `# Import`, und
  jeder Lauf ersetzt ihn. Eine Lieferung ohne Fassung hat keine Geschichte,
  nur einen letzten Stand.
- Das Frontmatter nennt mit `version` und `imported` immer die **neueste**
  übernommene Fassung.

Der Importnachweis ist ein **Protokoll, keine Zugehörigkeitsangabe**. Was
aktuell zu einem Bundle gehört, sagt allein die Property `bundles` der Notizen
(§5.2). Beide können auseinanderlaufen, und das ist beabsichtigt: Eine später
gelöschte oder aus dem Bundle genommene Notiz bleibt im Nachweis der Fassung
stehen, in der sie geliefert wurde. `hk-lint` prüft darum nur die Form des
Nachweises; ein Eintrag ohne vorhandenes Ziel ist ein Hinweis, kein Fehler.

## 5.2 Zugehörigkeit in der HKB

Weil in der HKB alle Notizen typbezogen zusammenliegen, geht die Trennung
nach Lieferung verloren. Sie wird deshalb als Property geführt:

```yaml
bundles:
  - "[[Bundles/biografie-2026|Biografische Notizen, Ausgabe 2026]]"
```

`bundles` hat den Typ `hkf-link-list:bundle` (§3.7.1). Eine Notiz
darf zu mehreren Bundles gehören. Notizen ohne `bundles` sind eigener Bestand
der HKB und werden von keinem Export erfasst.

Damit ist der Inhalt eines Bundles jederzeit abfragbar, ohne dass eine Liste
gepflegt oder geparst werden muss.

## 5.3 Grundausstattung und Zuladung

Eine HKB entsteht mit ihrer **Grundausstattung**: den dreizehn Property-Typen aus
§3.5.1 und den drei Kern-Typen `typedef`, `proptype` und `bundle`. Sie wird
nicht geliefert, sondern angelegt, denn ein Import setzt sie voraus — er muss
Typdefinitionen ablegen, Property-Typen einordnen und die Lieferung verbuchen
können, bevor er irgendetwas anderes tut. Damit ist die Wissensbasis konform,
wenn auch leer.

Alles Weitere wird zugeladen. Das nächstliegende Bundle ist `hkf-base`, das
Vokabular aus **HKF Config**: vierzehn Typdefinitionen und die beiden Property-Typen,
die nur mit ihnen Sinn ergeben. Notizen, Mediendateien, die Kern-Typen und die
Property-Typen der Grundausstattung enthält es nicht — die hat die
Wissensbasis bereits.

Der Import ist **freiwillig**. Eine Wissensbasis, die keine Personen und Orte
verwaltet, kommt ohne ihn aus und definiert stattdessen eigene Typen. Wer aber
einen Typ dieses Namens führt, führt ihn in der Fassung aus HKF Config — nur so
bleiben Bundles austauschbar.

Warum die Grundausstattung nicht ebenfalls ein Bundle ist: Sie zu importieren
setzte voraus, dass sie schon da ist. Der Typ `typedef` müsste sich selbst
ablegen, bevor er registriert wäre. Diese Schleife lässt sich zwar durch die
Vorgaberegel aus §3.7 auflösen — Verzeichnis gleich groß geschriebener
Typname mit angehängtem
`s` —, aber sie zu vermeiden ist einfacher, als sie zu beschreiben.

Fortschreibung ist ein erneuter Import. Bringt eine spätere Fassung einen
neuen Typ oder eine geänderte Property-Tabelle, entscheidet der Vergleich aus
§6.1 Schritt 5 je Notiz: geänderte werden übernommen, unveränderte
übersprungen. Welche Fassung eine HKB führt, sagt die `version` ihrer
Bundle-Notiz `Bundles/hkf-base.md`.

Weder die Grundausstattung noch einen zugeladenen Typ darf eine HKB
abwandeln. Wer
eigene Typen oder Property-Typen braucht, legt sie daneben — dafür sind §3.5
und §3.7 da.

Ein Bundle ohne eigene Typdefinitionen muss dafür nichts weiter tun. Der
`type` jeder Notiz nennt den Typ, und die aufnehmende Wissensbasis schlägt ihn
in ihrem eigenen Bestand nach — kennt sie ihn nicht, legt sie ihn vorläufig an
(§5.4). Welches Verzeichnis dabei herauskommt, bestimmt sie selbst; das Bundle
hat dazu nichts zu sagen und keines vorzuschlagen (§4.3).

## 5.4 Vorläufige Typdefinitionen

Ein Bundle bringt jede Typdefinition mit, die seine Notizen verwenden (§4).
Zwei Fälle durchbrechen das: Ein vorausgesetztes Bundle liegt noch nicht vor
(§4.1), oder das Bundle hält sich nicht an §7.1. In beiden kommt eine Notiz
an, deren Typ die Wissensbasis nicht kennt.

Sie wird trotzdem übernommen. Eine Notiz trägt als einzige Pflicht ihren
`type` (§3.3); mehr braucht es nicht, um sie abzulegen. Der Import legt dafür
eine **vorläufige Typdefinition** an:

```markdown
---
type: typedef
title: werkstoff
provisional: true
description: Vorläufig beim Import von biografie-2026 angelegt; keine Typdefinition geliefert.
created: 2026-08-27
modified: 2026-08-27T12:45:00
modified_by: hk-import
---
```

- `title` ist der **Typname**, unverändert. Nach A.2 gälte ohne ihn der
  Dateiname, der dasselbe sagt — aber nur für den, der ihn sieht. Eine
  Auswertung, die Titel vergleicht, fände nichts, und in jeder Notiz, die den
  Typ nennt, steht er ohnehin so: `werkstoff`, nicht `Werkstoff`.
- `provisional: true` kennzeichnet sie. Das ist die einzige Property, die eine
  vorläufige Typdefinition von einer endgültigen unterscheidet.
- `dir` bleibt weg, es gilt also die Vorgabe aus §3.7: der groß geschriebene
  Typname mit angehängtem `s`. Die Regel ist mechanisch und kein Sprachgefühl
  — `werkstoff` wird zu `Werkstoffs`. Genau darauf kommt es an: Sie liefert
  denselben Ort, den auch die nachgereichte Typdefinition beansprucht, solange
  diese kein abweichendes `dir` setzt.
- Sie trägt **keinen** Abschnitt `# Properties`. Eine Property-Tabelle sichert
  zu (§3.7); eine vorläufige Typdefinition weiß nichts, was sie zusichern
  könnte.
- Sie trägt **kein** `bundles`. Sie wurde nicht geliefert, sondern beim Import
  erfunden; sie gehört der Wissensbasis, nicht der Lieferung.
- Ist das errechnete Verzeichnis bereits von einem anderen Typ belegt, lässt
  sie sich nicht anlegen, ohne §3.2 zu verletzen. Das ist ein Konflikt, und
  der Import wird abgewiesen (§6.1 Schritt 2).

Damit bleibt die Ablage vollständig: Jede Notiz hat genau eine Typdefinition,
die Typtabelle der Wurzeldatei nennt den Typ samt Verzeichnis wie jeden
anderen, die Auflösung eines Verweises über den Pfad (§3.7.1) findet ihn, und
`hkf-link:werkstoff` lässt sich prüfen. Was fehlt, ist allein die Bedeutung —
und die fehlt sichtbar.

**Ablösung.** Kommt die endgültige Typdefinition später an — meist mit dem
nachgeladenen vorausgesetzten Bundle —, ersetzt sie die vorläufige
vollständig. Das ist kein Konflikt nach §6.1 Schritt 3: Eine vorläufige
Typdefinition sichert nichts zu, also kann sie nichts bestreiten. Setzt die
ankommende ein `dir`, das vom errechneten Verzeichnis abweicht, MÜSSEN die
Notizen dorthin verschoben und alle Verweise mitgezogen werden (§3.2 Regel 5).

**Export.** Eine vorläufige Typdefinition wird nicht ausgeliefert (§6.2). Sie
behauptet nichts über den Typ; ein Bundle, das sie mitschriebe, gäbe eine
Vermutung als Vertrag aus. Der Export meldet sie stattdessen — das Bundle ist
dann in seinen Typen nicht geschlossen und braucht die richtige Typdefinition,
bevor es weitergegeben wird.

Eine vorläufige Typdefinition ist ein offener Posten, kein Dauerzustand.
`hk-lint` meldet jede als Hinweis, mit Verzeichnis und der Zahl der Notizen,
die daran hängen.

## 5.5 Gleicher Name, gleiche Bedeutung

HKF kennt keine Namensräume. Ein Typ heißt `person`, und ob damit ein Mensch
gemeint ist oder der Datensatz einer Personalverwaltung, steht nicht im Namen.
Solange eine Wissensbasis für sich bleibt, ist das gleichgültig. Beim Import
wird es zur Frage: Zwei gleichnamige Typen werden zu einem, und was einmal in
einem Verzeichnis zusammenliegt, lässt sich nur Notiz für Notiz wieder
trennen.

**Wann die Frage entfällt.** In zwei Lagen ist die Gleichheit zugesichert und
wird nicht geprüft:

1. Der Typ kommt aus einem **vorausgesetzten Bundle, das vorliegt** (§4.1).
   Genau dafür gibt es `required_bundles`: Beide Seiten beziehen sich auf
   dieselbe Lieferung, also auf dieselbe Definition.
2. Das Bundle liefert eine Typdefinition mit, die der vorhandenen **in der
   Sache gleicht** — gleiche `description` und gleiche Property-Tabelle. Dann
   steht die Übereinstimmung schwarz auf weiß.

Damit ist der Regelfall abgedeckt. Ein Import, dem beide Seiten dasselbe
Vokabular zugrunde legen, läuft ohne Rückfrage durch.

**Wann sie gestellt wird.** Bleibt der Name gleich und die Zusicherung aus,
geht der Übernahme eine **Bedeutungsprüfung** voraus:

- Das Bundle liefert eine abweichende Typdefinition für einen Namen, den die
  Wissensbasis führt, und kein vorliegendes vorausgesetztes Bundle deckt ihn.
- Das Bundle liefert für diesen Namen gar keine Typdefinition, und das Bundle,
  das sie liefern müsste, fehlt.
- Der vorhandene Typ ist selbst **vorläufig** (§5.4). Er sichert nichts zu,
  also kann er nichts bestätigen.

**Wie sie entschieden wird.** Nicht mechanisch. Ein Werkzeug legt die
Unterlagen vor — die `description` beider Seiten, ihre Property-Tabellen, die
Konventionen im Body und eine Stichprobe der ankommenden Notizen —, und ein
Mensch oder ein Sprachmodell urteilt. Ein Sprachmodell prüft dabei genau die
Frage, die die Typdefinition stellt: Sind die ankommenden Notizen Menschen im
Sinne der hinterlegten Beschreibung von `person`, oder etwas anderes, das nur
so heißt?

Ist dieselbe Frage schon einmal beantwortet worden und bringt die Lieferung
dieselbe `description` wie damals, gilt das aufgezeichnete Urteil und es wird
nicht erneut gefragt (§5.7).

Es gibt drei Ausgänge, und nur einer führt weiter:

| Urteil | Folge |
|---|---|
| gleich | Die Typen werden zusammengeführt; der Import läuft weiter (§6.1 Schritt 3). |
| verschieden | Der Import wird abgewiesen. |
| nicht entscheidbar | Der Import wird abgewiesen. |

**Im Zweifel wird abgewiesen.** Zwei Typen zusammenzulegen, die nicht dasselbe
meinen, vermischt zwei Bestände in einem Verzeichnis, und jede Notiz darin
trägt danach denselben `type`; wer sie trennen will, muss jede einzeln
beurteilen. Ein abgewiesener Import kostet dagegen einen zweiten Anlauf.

Der Ausweg ist in beiden Fällen ein anderer Name. Wer das Bundle herausgibt,
benennt seinen Typ um und liefert neu; wer es empfängt, benennt seinen eigenen
um und zieht die Verweise mit (§3.2 Regel 5). Beides ist die Entscheidung
eines Menschen, und `--force` ersetzt sie nicht.

## 5.6 Verknüpfung

Eine Lieferung kommt als Insel an. Ihre Notizen verweisen aufeinander, aber
auf nichts, was schon da war — und weil niemand hinauszeigt, zeigt auch nichts
zurück. Wer die Wissensbasis durchläuft, stößt nicht auf sie.

Die Verknüpfung schließt diese Lücke. Sie ist der Teil des Imports, der aus
zwei Beständen einen macht — und der einzige, der eine Notiz anfasst, die gar
nicht zur Lieferung gehört. Darum ist sie hier ausführlicher beschrieben als
das Schreiben der Notizen selbst.

### Der Abschnitt `# Siehe auch`

Verweise, die nicht aus dem Text hervorgehen, stehen am Ende des Body in einem
eigenen Abschnitt:

```markdown
# Siehe auch

- [[Organisations/analytical-society|Analytical Society]] — beide Notizen nennen einander
- [[Persons/charles-babbage|Charles Babbage]] — im Body dieser Notiz genannt
- [[Places/london|London]] — mit der Lieferung biografie-2026 als Wirkungsort gekommen
```

- Der Abschnitt heißt `# Siehe auch` und ist der **letzte** der Notiz.
- Jede Zeile ist ein Listenpunkt aus einem qualifizierten Wikilink nach §3.6,
  dann ` — `, dann **der Grund**: ein Halbsatz, warum der Verweis dasteht.
- **Der Grund ist Pflicht.** Ohne ihn wäre der Abschnitt nur eine zweite,
  schlechtere Backlink-Ansicht — die hat Obsidian schon. Mit ihm sieht der
  nächste Leser, Mensch oder Modell, ob der Verweis noch trägt, ohne beide
  Notizen zu öffnen. Der Grund sagt, **warum** verlinkt wurde, nicht, was am
  Ziel steht.
- Die Einträge stehen alphabetisch nach Anzeigetext. Damit löst ein Nachtrag
  keinen Ordnungswechsel aus und ein Textunterschied zeigt genau die eine neue
  Zeile.

### Was Maschinen dürfen

**Beim Verknüpfen in der Wissensbasis fügt eine Maschine hinzu und entfernt
nie.** Das ist die ganze Absicherung, die der Abschnitt braucht: Was ein Mensch
hineingeschrieben oder umformuliert hat, übersteht jeden weiteren Import, weil
kein Import etwas herausnimmt.

Die Einschränkung auf die Wissensbasis ist wörtlich zu nehmen. Der Export
**entfernt** Einträge, die aus dem Bundle hinausweisen (§6.2), und `hk-lint
--fix` ordnet den Abschnitt um. Beides greift die Zusage nicht an: Der Export
schreibt nicht in die Wissensbasis, sondern liest aus ihr in eine Lieferung,
und der Linter ordnet, ohne wegzunehmen. Was hier zugesichert wird, ist
allein, dass keine Notiz der Wissensbasis einen Eintrag verliert, den sie
einmal hatte.

Entfernen ist eine menschliche Handlung. Soll ein Verweis dauerhaft weg und
nicht beim nächsten Import wiederkehren, nennt die Notiz sein Ziel in
`rejected_links`:

```yaml
rejected_links:
  - "[[Places/london|London]]"
```

`rejected_links` hat den Typ `hkf-link-list` und ist in jeder Notiz erlaubt
(A.2). Ein Ziel, das dort steht, wird nie wieder selbsttätig verlinkt — weder
in `# Siehe auch` noch in einer Property. Die Property hält die **Absicht**
fest, nicht den Textunterschied: Dass dieser Verweis nicht gewollt ist, gilt
weiter, auch wenn beide Notizen sich seither geändert haben.

Wer den Verweis später doch will, nimmt sein Ziel aus `rejected_links` und
setzt ihn. Beides zugleich wäre widersprüchlich, und `hk-lint` meldet es als
Fehler (§6.3).

**Eine Ablehnung gilt dem Paar, nicht der Richtung.** Sie sagt, dass diese
beiden Notizen nichts miteinander zu tun haben — und das gilt von beiden Seiten
aus. Ein Werkzeug prüft darum **beide** `rejected_links`, bevor es einen Eintrag
setzt: das der schreibenden Notiz und das des Ziels.

Es genügt also, die Ablehnung auf einer Seite zu vermerken. Das ist keine
Bequemlichkeit, sondern notwendig — die andere Seite gehört womöglich zur
Grundausstattung oder zu einer Lieferung, die man nicht anfassen will, und ein
Vermerk dort verließe die Wissensbasis beim nächsten Export ohnehin (§6.2).
Wer sie dennoch auf beiden Seiten notiert, schadet nichts.

**Verknüpfen ändert `modified` nicht.** Ein Eintrag unter `# Siehe auch` sagt
nichts über den Gegenstand der Notiz, sondern darüber, wie die Wissensbasis
verdrahtet ist. Zählte er als Änderung, wäre jede gelieferte Notiz gleich nach
ihrer Ankunft jünger als die Lieferung, aus der sie stammt — und der Vergleich
aus §6.1 Schritt 5 lehnte sie beim nächsten Import derselben Fassung ab. Dass
eine Notiz verknüpft wurde, steht im Importnachweis (§5.1), nicht in ihren
Zeitangaben.

Das gilt allein für die Verknüpfung. Wer eine Notiz sonst maschinell ändert,
setzt `modified` und `modified_by` wie immer (§3.3).

### Auch als Property: `related`

Ein Abschnitt im Body ist für Menschen da. Abfragen kann man ihn nicht — keine
Obsidian-Ansicht, keine Auswertung und kein Werkzeug kommt an eine Liste heran,
die als Fließtext dasteht. Was verknüpft wurde, steht deshalb **zusätzlich** in
der Property `related` vom Typ `hkf-link-or-url-list` (A.2):

```yaml
related:
  - "[[Persons/charles-babbage|Charles Babbage]]"
  - https://example.org/analytical-engine
```

**Die Regel.** Jeder Eintrag unter `# Siehe auch` steht auch in `related` —
**es sei denn, sein Ziel steht bereits in einer anderen Property derselben
Notiz.** Wer als `employer` auf eine Körperschaft zeigt, sagt damit Genaueres,
als `related` je sagen könnte; denselben Verweis ein zweites Mal und unschärfer
zu führen, verwirrt nur. Die genauere Property gewinnt, und `related` bleibt
für alles, wofür es keine gibt.

**Welche Seite gilt.** `# Siehe auch` ist die Quelle, `related` ist daraus
**abgeleitet** — dasselbe Verhältnis wie zwischen den Typdefinitionen und der
Typtabelle der Wurzeldatei (§3.1). Bei Abweichung gewinnt der Abschnitt, weil
nur er den Grund trägt. `hk-lint --fix` erzeugt `related` daraus neu.

**Nur in dieser Richtung.** `related` darf **mehr** enthalten, als der
Abschnitt hergibt, und das ist kein Befund:

- **Adressen.** Unter `# Siehe auch` steht je Zeile ein qualifizierter
  Wikilink; eine URL kann dort nicht stehen. In `related` schon — dafür lässt
  `hkf-link-or-url` beides zu.
- **Von Hand gesetzte Verweise.** Wer einen Zusammenhang kennt, trägt ihn ein,
  ohne ihn zu begründen. Ein Werkzeug nimmt ihn nicht wieder heraus; es gilt
  auch hier: hinzufügen ja, entfernen nein.

Ein Ziel in `rejected_links` steht in keinem von beiden (§5.6 oben).

### Nur eine Richtung

**Ein Eintrag steht in der Notiz, deren Body den anderen nennt** — und nur
dort. Einen Gegeneintrag in der Zielnotiz gibt es nicht.

Der Grund ist derselbe, aus dem HKF die Typtabelle als abgeleitet führt und
Medienarten aus dem Verzeichnis liest: **Was sich errechnen lässt, wird nicht
zusätzlich hingeschrieben.** Sobald der Eintrag steht, ist er ein Wikilink, und
Obsidian zeigt ihn der Zielnotiz als Backlink an. Ihn dort noch einmal
einzutragen verdoppelt eine Auskunft, die die Oberfläche ohnehin gibt — und
schafft zwei Stellen, die auseinanderlaufen können.

Nennen **beide** Notizen einander, bekommen auch beide einen Eintrag. Das ist
keine Verdopplung: Jeder der beiden steht auf eigenen Füßen, weil der Body der
jeweiligen Notiz ihn trägt. Der Grund lautet dann „beide nennen einander".

Damit löst sich auch die Sammelpunkt-Frage weitgehend von selbst. Eine viel
genannte Notiz — ein Ort, den jede zweite Lieferung streift — sammelte unter der
Gegenseitigkeit eine lange Liste von Rückverweisen. Jetzt trägt sie nur, was
ihr **eigener** Body nennt; wer auf sie zeigt, steht in der Backlink-Ansicht.
Was doch zu viel wird, streicht ein Mensch, und was gestrichen bleiben soll,
kommt in `rejected_links`.

Der Preis ist, dass eine Notiz für sich gelesen nicht mehr sagt, wer auf sie
zeigt. Das ist derselbe Preis wie bei jeder abgeleiteten Angabe in diesem
Format, und er ist hier gering: Die Auskunft ist nicht verloren, sie steht nur
woanders.

### Der zweite Ort: unbelegte Properties

Eine leere Property, deren Property-Tabelle einen Zieltyp fordert, ist die
andere Stelle, an der eine Verknüpfung landet:

```text
| employer | hkf-link:organisation | nein | — | Arbeitgeber |
```

Steht `employer` leer und liegt im Bestand eine `organisation`, die in Frage
kommt, ist das ein Kandidat. **Gesetzt wird er nie selbsttätig.** Eine Property
behauptet eine bestimmte Beziehung — dass diese Person dort gearbeitet hat —,
ein Eintrag unter `# Siehe auch` nur, dass zwei Notizen miteinander zu tun
haben. Das erste ist eine Tatsachenbehauptung und verlangt ein Urteil; das
zweite ist ein Fingerzeig und kommt mit einem Namensvergleich aus.

Eine bereits belegte Property wird nicht angerührt, auch nicht, wenn ein
besserer Kandidat auftaucht.

### Was nicht geschieht

Erwähnungen im laufenden Text werden **nicht** zu Wikilinks gemacht. Gewachsener
Text ist die Stelle, an der Handarbeit am ehesten verlorengeht, und der Gewinn
wäre klein: Derselbe Verweis steht bereits unter `# Siehe auch`, dort mit
seinem Grund und an einem Ort, den man gefahrlos neu schreiben kann.

## 5.7 Entscheidungen

Drei Stellen dieser Spezifikation enden mit „ein Mensch oder ein Sprachmodell
entscheidet": die Bedeutungsprüfung (§5.5), die Identität einer ankommenden
Notiz (§6.1 Schritt 5) und die Verknüpfung (§5.6). Die dritte hält ihr Ergebnis
schon fest — ein gesetzter Verweis steht da, ein abgelehnter in
`rejected_links`. Die ersten beiden hielten nichts fest, und damit stellte jede
neue Fassung dieselben Fragen noch einmal. Eine Fortschreibung, die jedes Mal
dieselbe Rückfrage auslöst, ist keine.

Die Bundle-Notiz führt sie deshalb in einem Abschnitt `# Entscheidungen`, vor
den Importnachweisen:

```markdown
# Entscheidungen

| Gegenstand | Urteil | Von | Beurteilt | Grund |
|---|---|---|---|---|
| Typ `person` | gleich | armin | Ein Mensch als Gegenstand der Wissensbasis. | dieselbe Sache, die Lieferung ergänzt nur Felder |
| Notiz [[Persons/john-smith\|John Smith]] | verschieden | claude-opus-5 | John Smith | Toningenieur; unserer ist Botaniker |
```

- **Gegenstand** ist entweder ein Typ, geschrieben als `` Typ `<name>` ``, oder
  eine Notiz, geschrieben als `Notiz ` und ein qualifizierter Wikilink nach
  §3.6 auf die Notiz der Wissensbasis.
- **Urteil** ist bei einem Typ `gleich` oder `verschieden`, bei einer Notiz
  `dieselbe` oder `verschieden`. Andere Werte gibt es nicht.
- **Von** nennt, wer entschieden hat — ein Mensch mit seinem Namen, ein
  Sprachmodell mit seinem Modellnamen. Dieselbe Selbstauskunft wie bei
  `modified_by` (A.2), und aus demselben Grund: Sie sagt verlässlich, *dass*
  eine Maschine geurteilt hat.
- **Grund** ist ein Halbsatz. Er ist Pflicht, wie bei `# Siehe auch`: Eine
  Entscheidung ohne Grund lässt sich später weder prüfen noch aufheben.

### Woran eine Entscheidung hängt

**Beurteilt** ist der Kern des Ganzen. Dort steht der eine Satz, über den
geurteilt wurde: bei einem Typ die **gelieferte `description`**, bei einer
Notiz ihr **gelieferter `title`**. Beide sind nach §3.7 und §3.3 einzeilig, und
beide sind genau das, woran ein Mensch die Frage entscheidet.

Daraus folgt die Geltung: **Eine Entscheidung gilt, solange die Lieferung
denselben Satz bringt.** Weicht er ab, fällt sie weg und die Frage wird neu
gestellt. Ein Bundle kann damit die Bedeutung seines Typs ändern, ohne dass
eine alte Zustimmung stillschweigend weitergilt — genau der Fall, den §5.5
verhindern soll — und es kann zugleich beliebig oft fortgeschrieben werden,
ohne dieselbe Frage erneut auszulösen.

Bewusst hängt sie **nicht** an der `version` des Bundles. Fortschreibung ist bei
HKF der Normalfall; eine Entscheidung, die mit jeder neuen Fassung verfällt,
wäre keine.

Und sie hängt nicht an der Property-Tabelle. Ob zwei Tabellen zusammenpassen,
entscheidet §6.1 Schritt 3 strukturell und bei jedem Import neu. Die
Bedeutungsprüfung urteilt über die Sache, nicht über die Felder.

### Wann sie herangezogen wird

Eine aufgezeichnete Entscheidung wird **nach** den mechanischen Regeln
befragt, nie vor ihnen:

1. Zuerst die Regeln, die von sich aus entscheiden — die beiden zugesicherten
   Lagen aus §5.5, die drei Beobachtungen aus §6.1 Schritt 5.
2. Erst wenn keine greift: die Zeile in `# Entscheidungen`, sofern ihr
   **Beurteilt** mit dem Gelieferten übereinstimmt.
3. Erst wenn auch die fehlt: die Frage an einen Menschen.

Die Reihenfolge ist der Grund, warum eine Aufzeichnung ungefährlich ist. Zwei
verschiedene `hkf-wikidata`-Kennungen bedeuten „verschiedene Notizen", und
keine noch so alte Zeile hebt das auf. Aufgezeichnet wird nur, was ohnehin
niemand mechanisch beantworten konnte.

### Was nicht aufgezeichnet wird

Die strukturellen Konflikte aus §6.1 Schritt 3 und 7 — abweichendes `dir`,
widersprüchliche Zeile in einer Property-Tabelle, abweichender Property-Typ,
Mediendatei mit gleichem Pfad und anderem Inhalt. Sie sind keine Urteile,
sondern Reparaturen: Danach stimmen beide Seiten überein, oder das Bundle
gehört berichtigt. Eine Zeile „ich habe damals unser `dir` genommen"
unterdrückte einen echten Konflikt für immer, ohne ihn zu beheben.

### Auch eine Ablehnung wird aufgezeichnet

Fällt eine Bedeutungsprüfung auf „verschieden", wird der Import abgewiesen und
keine Notiz geschrieben (§6.1 Schritt 2). Für den Entscheidungsnachweis gilt
das **nicht**: Er entsteht trotzdem, als `<base>/Bundles/<id>.md` mit dem
Abschnitt `# Entscheidungen` und sonst nichts.

Anders ginge es nicht. Eine Ablehnung, die nirgends steht, wird bei jedem
Versuch neu erfragt — und das ist der Fall, der am häufigsten wiederkehrt, weil
ein abgewiesenes Bundle typischerweise mehrfach angeboten wird, bevor jemand
es berichtigt.

Eine solche Bundle-Notiz trägt `id`, `version` und `description` der
angebotenen Lieferung, aber **kein `imported`** und keinen Importnachweis. Das
Fehlen von `imported` ist die Auskunft: Diese Lieferung wurde geprüft und nicht
übernommen. Keine Notiz der Wissensbasis nennt sie in `bundles`.

Der Abschnitt gehört der Wissensbasis, nicht der Lieferung. Er steht nur in
`<base>/Bundles/<id>.md` und geht bei einem Export nicht mit — wie `imported`
und die Importnachweise (§6.2).

---

# 6. Methoden

Jede HKB stellt drei Methoden bereit, als Befehl oder als gleichwertige
Schnittstelle. Ein Bundle stellt keine Methoden bereit.

## 6.1 `hk-import <bundle-pfad>`

Übernimmt ein HKF-Bundle in die HKB.

1. `hbundle.md` lesen und prüfen: `id` und `description` müssen da sein, mehr
   nicht (§4.1). Fehlt `hkf`, wird die eigene Fassung angenommen und das als
   Hinweis gemeldet.

   Dann den Baum der Lieferung durchgehen und **auswählen, was überhaupt in
   Frage kommt** (§4.3): jede `.md`-Datei mit `type` im Frontmatter, jede
   Datei ohne `.md`-Endung als Mediendatei ihrer Endung. Alles Übrige bleibt
   liegen. Wo die Dateien liegen, spielt dabei keine Rolle.

   Dann jeden Eintrag aus
   `required_bundles` gegen die Bundle-Notizen der HKB halten. Fehlt eines
   oder ist seine Fassung zu niedrig, ist das eine **Warnung**, kein Abbruch:
   Der Import läuft weiter, und der Befund nennt das fehlende Bundle samt der
   Aufforderung, es nachzuladen und den Import zu wiederholen.

   Der naheliegende Einwand — ein Bundle, das sich auf fremde Typdefinitionen
   verlässt, hinterließe Notizen in Verzeichnissen ohne Typ — trägt nicht: Ein
   Typ ohne Definition bekommt eine vorläufige (§5.4), und die Notiz liegt
   damit in einem registrierten Verzeichnis. Was fehlt, ist die Bedeutung, und
   die steht im Befund.

   Ein Werkzeug weiß nicht, welche Typen ein Bundle mitbrächte, das es nicht
   hat. Der Befund nennt deshalb das fehlende Bundle, nicht die Typen, die
   von ihm zu erwarten wären — auch dann nicht, wenn es `hkf-base` ist. Core
   kennt das Vokabular nicht und nennt es nicht.
2. **Typen abgleichen.** Bevor irgendetwas geschrieben wird, wird jeder Typ
   bestimmt, den die Lieferung verwendet: aus den mitgelieferten
   Typdefinitionen und aus dem `type` jeder Notiz. Für jeden gilt:

   | Lage | Folge |
   |---|---|
   | Die HKB kennt den Namen nicht | Der Typ wird angelegt — aus der gelieferten Typdefinition, sonst vorläufig (§5.4). |
   | Die HKB kennt ihn, die Gleichheit ist zugesichert (§5.5) | Der Typ wird zusammengeführt (Schritt 3). |
   | Die HKB kennt ihn, die Gleichheit ist offen | **Bedeutungsprüfung** (§5.5), sofern §5.7 sie nicht schon beantwortet. |

   Fällt eine Bedeutungsprüfung nicht auf „gleich", **wird der Import
   abgewiesen** — ohne dass eine Notiz geschrieben wird. `--force` hebt das
   nicht auf: Ob zwei Typen dasselbe meinen, ist keine Frage, die ein
   Kennzeichen beantwortet.

   Eine einzige Ausnahme: Fiel das Urteil auf „verschieden", entsteht die
   Bundle-Notiz mit dem Entscheidungsnachweis und sonst nichts (§5.7). Sonst
   stünde die Ablehnung nirgends und würde beim nächsten Versuch neu erfragt.

   Ebenso abgewiesen wird ein Import, dessen vorläufiges Verzeichnis bereits
   einem anderen Typ gehört (§5.4).
3. Typdefinitionen und Property-Typen des Bundles übernehmen. Nicht jede
   Abweichung ist ein Konflikt — eine Property-Tabelle schränkt nicht ein,
   sondern sichert zu (§3.7), und Zusicherungen lassen sich zusammenführen:

   - Fehlt ein Typ oder ein Property-Typ in der HKB, wird er angelegt.
   - Für einen Typ, den keine Typdefinition beschreibt, entsteht eine
     vorläufige (§5.4). Eine schon vorhandene vorläufige Typdefinition wird
     von einer gelieferten vollständig ersetzt; weicht deren `dir` vom
     errechneten Verzeichnis ab, ziehen die Notizen mit (§3.2 Regel 5).
   - Ein abweichendes `dir` ist ein **Konflikt**. Die Ablage der HKB hängt
     daran; sie darf nicht stillschweigend umziehen.
   - Property-Tabellen werden **zusammengeführt**. Eine Zeile, die die HKB
     noch nicht kennt, wird ergänzt. Eine Zeile, die dieselbe Property mit
     anderer Typ-Angabe oder anderer Pflichtangabe belegt, ist ein
     **Konflikt**.
   - Bei einem Property-Typ ist jede Abweichung in `form`, `pattern`,
     `values`, `unit`, `min` oder `max` ein **Konflikt**.
   - Die Standard-Property-Typen aus §3.5.1 darf ein Bundle nicht
     umdefinieren.
   - `title`, `description` und der übrige Body einer vorhandenen
     Typdefinition bleiben unverändert. Weichen sie ab, wird das gemeldet,
     ist aber kein Konflikt.

   Bei einem Konflikt hält das Werkzeug an und meldet ihn; ein Mensch
   entscheidet. Nichts wird stillschweigend zusammengelegt.
4. Jede Notiz nach `<base>/<dir des typs>/<dateiname>` schreiben.
5. Existiert die Ziel-Notiz-ID bereits, ist zuerst zu klären, **ob es
   dieselbe Notiz ist**. Der Pfad allein beweist das nicht (§3.2 Regel 4):
   `Persons/john-smith` heißt in zwei Lieferungen leicht denselben Dateinamen
   und meint zwei verschiedene Menschen.

   Entschieden wird an drei Beobachtungen, in dieser Reihenfolge:

   | Lage | Folge |
   |---|---|
   | Die vorhandene Notiz führt dieses Bundle schon in `bundles` | **Dieselbe Notiz.** Eine frühere Fassung derselben Lieferreihe; weiter mit dem Vergleich unten. |
   | Beide tragen denselben Wert in einer Property vom Typ `hkf-wikidata` | **Dieselbe Notiz.** Sie bezeichnen denselben Gegenstand der Welt — dafür gibt es die Kennung (§3.5.1). |
   | Beide tragen einen solchen Wert, und die Werte sind **verschieden** | **Verschiedene Notizen.** Konflikt; nichts wird geschrieben. |
   | Eine Zeile in `# Entscheidungen` beantwortet die Frage, und der gelieferte `title` stimmt mit ihrem **Beurteilt** überein | Das aufgezeichnete Urteil gilt (§5.7). |
   | Sonst — die Notiz kommt zum ersten Mal aus dieser Lieferung, und nichts verankert sie | **Offen.** Konflikt; ein Mensch oder ein Sprachmodell entscheidet. |

   Der letzte Fall ist der wichtige. Eine Wissensbasis darf dieselbe Notiz
   durchaus aus mehreren Lieferungen beziehen (§5.2) — deshalb ist ein
   Erstkontakt kein Fehler, sondern eine Frage. Sie ungefragt mit „dieselbe
   Notiz" zu beantworten hieße, zwei fremde Bestände über einen Dateinamen zu
   verschmelzen; sie ungefragt mit „verschieden" zu beantworten hieße,
   Fortschreibung unmöglich zu machen. Vorgelegt werden beide Notizen, und die
   Entscheidung wird sichtbar: Wird auf „dieselbe" entschieden, trägt die Notiz
   danach beide Bundles in `bundles` und trägt damit ihren eigenen Nachweis.
   In beiden Fällen entsteht eine Zeile in `# Entscheidungen`, damit die
   nächste Fassung nicht wieder fragt (§5.7).

   Wird auf „verschieden" entschieden, muss eine der beiden umziehen, bevor
   der Import weitergeht. Das ist eine Umbenennung nach §3.2 Regel 5, keine
   Sache des Werkzeugs allein.

   **Warum keine eigene Kennung.** Eine UUID je Notiz löste den Fall
   mechanisch, verdoppelte aber die Identität: Neben dem Pfad, an dem §3.2 und
   §3.7.1 alles aufhängen, stünde eine zweite Wahrheit, die mit ihm auseinander
   laufen kann und die niemand von Hand pflegt. HKF hat mit `hkf-wikidata`
   bereits einen Anker für die Fälle, in denen es einen gibt; für die übrigen
   ist eine Frage an einen Menschen ehrlicher als eine Zahl, die
   Eindeutigkeit nur behauptet.

   Steht fest, dass es dieselbe Notiz ist, entscheidet `modified`, welche
   Fassung gilt:

   | Ankommende Fassung | Verhalten |
   |---|---|
   | `modified` jünger als in der HKB | übernehmen, Zustand `aktualisiert` |
   | gleich | überspringen; weicht der Inhalt ab, melden |
   | älter | **ablehnen**, die Fassung der HKB bleibt |
   | `modified` fehlt auf einer der beiden Seiten | ablehnen, weil nicht vergleichbar |

   Eine Ablehnung ist ein gemeldeter Befund, kein Abbruch: Die übrigen Notizen
   der Lieferung werden weiter verarbeitet. `--force` übernimmt die ankommende
   Fassung in allen vier Fällen — auch die ältere und die unvergleichbare.
   Ohne dieses Kennzeichen verliert ein Import niemals eine neuere Fassung.

   Auf die Frage davor, ob es überhaupt dieselbe Notiz ist, wirkt `--force`
   **nicht**. Es entscheidet, welche von zwei Fassungen gilt, nicht, ob zwei
   Dateien dasselbe meinen — dieselbe Grenze wie bei der Bedeutungsprüfung
   (§5.5).
6. `bundles` jeder übernommenen Notiz um den Wikilink auf die Bundle-Notiz
   ergänzen. Fehlt `created`, `modified` oder `modified_by`, wird es gesetzt:
   `created` auf den Tag des Imports, `modified` auf seinen Zeitpunkt,
   `modified_by` auf den Namen des importierenden Werkzeugs. Vorhandene Werte
   bleiben unangetastet — sie beschreiben die Notiz, nicht die Lieferung, und
   ein Zurücksetzen auf den Importzeitpunkt zerstörte den Vergleich aus
   Schritt 5.
7. Mediendateien nach `<media_base>/<medienart>/<restpfad>` übernehmen; die
   Medienart folgt aus der Dateiendung, der `restpfad` aus §4.3. Trifft ein
   Pfad auf eine vorhandene Datei mit abweichendem Inhalt, ist das ein
   Konflikt: melden und ohne `--force` nicht überschreiben. Mediendateien
   tragen kein `modified`; für sie entscheidet allein das Kennzeichen.
8. Wikilinks in Body und Properties auf die Pfade der HKB umschreiben. Aus den
   Schritten 4 und 7 liegt für jede übernommene Datei ein Paar vor — ihr Pfad
   in der Lieferung und ihr Pfad in der Wissensbasis —, und genau diese
   Zuordnung wird angewandt. Ein Ziel ohne Verzeichnis wird aufgelöst, wenn
   genau eine Datei der Lieferung so heißt (§3.6).

   Ein Ziel, das auf eine übergangene Datei zeigt — ein README etwa —, wird
   **nicht** umgeschrieben und gemeldet: Es zeigt in der Wissensbasis ins
   Leere, weil die Datei dort nie ankam. Ebenso jedes mehrdeutige und jedes
   unauflösbare Ziel; geraten wird nicht.
9. **Verknüpfen.** Die übernommenen Notizen mit dem Bestand verbinden (§5.6).
   Kandidaten entstehen aus drei mechanischen Beobachtungen:

   | Beobachtung | Folge |
   |---|---|
   | `title` oder ein `aliases`-Eintrag der einen Notiz kommt im Body der anderen wörtlich vor | Eintrag in `# Siehe auch` **der nennenden Notiz**, mit dem Grund „im Body dieser Notiz genannt"; nennen beide einander, bekommen beide einen, mit „beide nennen einander" (§5.6) |
   | Beide tragen dieselbe `hkf-wikidata`-Kennung | **kein** Verweis, sondern ein Zusammenführungskandidat: Sie meinen denselben Gegenstand, und zwei Notizen darüber gehören zusammengelegt, nicht verlinkt (§6.3) |
   | Eine leere Property fordert einen Zieltyp, und im Bestand liegt eine Notiz dieses Typs | Vorschlag; nie selbsttätig gesetzt (§5.6) |

   Selbsttätig geschrieben wird allein die erste Zeile, und auch sie nur, wenn
   das Ziel nicht in `rejected_links` steht. Alles Übrige wird vorgelegt: Ein
   Mensch oder ein Sprachmodell entscheidet und schreibt den Grund dazu. Die
   Arbeitsteilung ist dieselbe wie bei der Bedeutungsprüfung (§5.5) —
   mechanisch, was mechanisch geht; geurteilt, was nicht.

   Ein Sprachmodell darf über die drei Beobachtungen hinausgehen und
   Zusammenhänge vorschlagen, die kein Namensvergleich findet. Es trägt dann
   seinen Modellnamen in `modified_by` ein wie bei jeder anderen Änderung
   (A.2), und der Grund in der Zeile ist seine Begründung.

   Jeder gesetzte Eintrag wird zugleich in `related` geführt, sofern sein Ziel
   nicht schon in einer anderen Property der Notiz steht (§5.6).

   Dieser Schritt lässt `modified` und `modified_by` unangetastet, auch an
   den Notizen des Bestands (§5.6). Sonst wäre jede Lieferung nach ihrem
   eigenen Import veraltet.

   `--no-link` überspringt den Schritt. Eine Lieferung, die unverändert
   liegenbleiben soll, kommt so an.
10. Bundle-Notiz nach §5.1 als `<base>/Bundles/<id>.md` anlegen oder
   aktualisieren: `version` und `imported` auf die eben übernommene Fassung
   setzen und den Importnachweis `# Import <version>` mit allen Notizen und
   Mediendateien voranstellen, dazu die angelegten Verweise samt Gegenstelle
   und Grund. Jede in diesem Lauf getroffene Entscheidung wird als Zeile in
   `# Entscheidungen` festgehalten (§5.7); eine Zeile, deren **Beurteilt**
   nicht mehr zutrifft, wird entfernt. Ist die Fassung schon nachgewiesen, bleibt ihr Abschnitt
   unverändert. Anschließend die Typtabelle in `hkb.md` neu erzeugen.

Der Vorgang ist wiederholbar: dieselbe `id` mit derselben `version` erzeugt
keine zusätzlichen Notizen. Das Ergebnis nennt die Zahl der angelegten,
aktualisierten, übersprungenen und fehlerhaften Notizen.

### `--check`

`hk-import --check <bundle-pfad>` führt den Import bis zu dem Punkt aus, an
dem er schreiben würde, und schreibt nichts. Er beantwortet drei Fragen, und
in dieser Reihenfolge wird berichtet.

**Was geschieht.** Wie viele Notizen neu angelegt, aktualisiert, übersprungen
oder abgelehnt würden; welche Typen angelegt und welche nur vorläufig angelegt
würden, jeweils mit Verzeichnis; welche Mediendateien hinzukämen.

**Was zu entscheiden ist.** Jede fällige Bedeutungsprüfung (§5.5), jede offene
Identitätsfrage aus Schritt 5 — eine Notiz-ID, die es schon gibt, ohne dass
Bundle oder `hkf-wikidata` sie verankern —, jeder vorgelegte
Verknüpfungskandidat (§5.6) und jeder Konflikt aus Schritt 3 —
abweichendes `dir`, widersprüchliche Zeile in einer Property-Tabelle,
abweichender Property-Typ, belegtes vorläufiges Verzeichnis, Mediendatei mit
gleichem Pfad und anderem Inhalt. Jeder Eintrag nennt **beide
Seiten**, damit er ohne Nachschlagen zu beurteilen ist.

**Was zu tun ist.** Zu jedem Befund ein Satz in der Befehlsform, der den
nächsten Schritt nennt. Das ist der eigentliche Zweck des Modus: Ein Befund,
der nur eine Lage beschreibt, lässt den Benutzer mit ihr allein.

```text
hk-import --check biografie-2026/

Was geschieht
  14 Notizen: 12 neu, 1 aktualisiert, 1 abgelehnt (ältere Fassung)
  2 Mediendateien neu
  Typ angelegt:  quelle → quellen
  Vorläufig:     werkstoff → Werkstoffs (3 Notizen)
  Verknüpfung:   7 Verweise mechanisch sicher, 4 vorgelegt

Was zu entscheiden ist
  person   Gleicher Name, Bedeutung nicht zugesichert.
           hier    Ein Mensch als Gegenstand der Wissensbasis. (eigene Definition)
           Bundle  Datensatz der Personalverwaltung. (Typedefs/person.md)
  place    dir weicht ab: orte (Bundle) gegen places (hier).

Was zu tun ist
  → Bedeutungsprüfung für person entscheiden. Bei „verschieden" einen der
    beiden Typen umbenennen und den Import wiederholen.
  → Für place entscheiden, welches Verzeichnis gilt. Ein Umzug zieht alle
    Verweise mit.
  → hkf-base >= 1.0 ist vorausgesetzt, aber nicht importiert. Erst hkf-base
    importieren, dann diesen Import wiederholen; werkstoff bleibt bis dahin
    vorläufig.
  → Persons/ada-lovelace ist hier neuer als in der Lieferung. Prüfen, ob die
    Lieferung veraltet ist; sonst nichts tun.
  → 4 Verknüpfungen entscheiden, darunter employer an zwei Personen. Was
    nicht gewollt ist, gehört nach rejected_links, sonst kommt es beim
    nächsten Import wieder.

Nichts wurde geschrieben.
```

Der Abschnitt „Was geschieht" rechnet damit, dass jede offene Entscheidung auf
Übernahme fällt. Er sagt also, was höchstens geschähe — fällt eine
Bedeutungsprüfung auf „verschieden", geschieht gar nichts (Schritt 2).

Ein Import ohne `--check` gibt dieselben drei Abschnitte aus, bezogen auf das,
was tatsächlich geschehen ist. Der Modus ändert nicht, was geprüft wird,
sondern nur, ob geschrieben wird.

## 6.2 `hk-export <bundle-id> <zielpfad>`

Schreibt ein HKF-Bundle heraus.

Ein Bundle darf beliebig aufgebaut sein (§4), aber `hk-export` nutzt diese
Freiheit nicht: Es schreibt den typbezogenen Baum, mit `Typedefs/`,
`Proptypes/` und `media/<art>/`. Streng im Schreiben, großzügig im Lesen — ein
Ergebnis, das aussieht wie eine Wissensbasis, ist leichter zu prüfen und zu
lesen als eines, das jede erlaubte Form annehmen dürfte.

1. Alle Notizen sammeln, deren `bundles` auf `<base>/Bundles/<bundle-id>`
   verweist.
2. Jede Notiz nach `<zielpfad>/<dir des typs>/<dateiname>` schreiben, die
   Properties `bundles` und `rejected_links` dabei entfernen (§4.2). Beide
   beschreiben, wie **diese** Wissensbasis die Lieferung einsortiert und
   beurteilt hat; beim Empfänger bezeichnen sie nichts.
3. Die Typdefinitionen und Property-Typen mitschreiben, die von diesen
   Notizen verwendet werden; die Standard-Property-Typen aus §3.5.1 dürfen
   entfallen. Eine vorläufige Typdefinition (§5.4) wird **nicht**
   mitgeschrieben, sondern gemeldet: Das Bundle ist in seinen Typen dann nicht
   geschlossen und braucht die richtige Typdefinition, bevor es weitergegeben
   wird.
4. Jede Mediendatei mitschreiben, auf die diese Notizen verweisen — aus dem
   `media_base` der HKB in den `media_base` des Bundles, unter derselben
   Medienart und demselben Pfad darunter.
5. Wikilinks anpassen: bei Notizen den Präfix der HKB aus Ablagepfad und
   `base` entfernen, bei Mediendateien Ablagepfad und `media_base` der HKB
   durch den `media_base` des Bundles ersetzen.
6. Die Bundle-Notiz nach §4.1 als `<zielpfad>/hbundle.md` schreiben, mit
   `hkf`, `base: ""`, dem gewählten `media_base` und frisch erzeugter
   Typtabelle. `imported`, die Importnachweise und der Entscheidungsnachweis
   entfallen — sie beschreiben, wie die abgebende HKB die Lieferung
   eingeordnet und beurteilt hat, nicht die Lieferung selbst.
7. Aus jedem Abschnitt `# Siehe auch` die Einträge entfernen, die aus dem
   Bundle hinausweisen (§5.6). Sie zeigten beim Empfänger ins Leere, und der
   Abschnitt ist maschinell gepflegt — was hier wegfällt, entsteht dort beim
   Import neu. Bleibt kein Eintrag übrig, entfällt der Abschnitt.
8. Wikilinks im übrigen Body und in Properties, die auf Notizen außerhalb des
   Bundles zeigen, melden. Sie bleiben unverändert erhalten — das Bundle ist
   dann in seinen Typen, aber nicht in allen Verweisen geschlossen.

Der Export gibt den aktuellen Stand wieder. Ein bytegleicher historischer
Stand erfordert ein Archiv der jeweiligen Fassung.

**Der Rundlauf ist damit nicht mehr buchstäblich.** Ein Bundle, das importiert
und sofort wieder exportiert wird, kommt nicht byte-gleich zurück: Verweise
zwischen zwei Notizen **derselben** Lieferung überstehen Schritt 7 und stehen
im Ergebnis unter `# Siehe auch`. Das ist gewollt — der Import hat etwas
erkannt, was in der Lieferung nicht stand, und ein Export, der es wieder
wegwürfe, verlöre Arbeit. Verweise in den Bestand hinein fallen dagegen weg,
denn sie gelten nur hier.

## 6.3 `hk-lint [--fix]`

Prüft eine Ablage, ohne sie zu verändern. Anwendbar auf eine HKB und auf ein
Bundle; die letzten vier Punkte gelten nur für eine HKB.

- Wurzeldatei vorhanden, `hkf` gesetzt, `base` und `media_base` auflösbar,
- `Typedefs`, `Proptypes` und `Bundles` im Basispfad vorhanden — **nur in
  einer HKB**; ein Bundle hat keine Typverzeichnisse (§4),
- jede Notiz hat `type`, und in einer HKB passt der Typ zu ihrem Verzeichnis.
  In einem Bundle gilt als Notiz, was `type` trägt; jede andere `.md`-Datei
  wird übergangen und nicht geprüft (§4.3),
- in einem Bundle ergäben keine zwei Notizen desselben Typs denselben
  Dateinamen — sonst fielen sie beim Import zu einer Notiz-ID zusammen,
- jeder `type` hat genau eine Typdefinition; `dir`-Werte sind wohlgeformte
  relative Pfade, eindeutig und nicht ineinander verschachtelt,
- jede vorläufige Typdefinition ist ein Hinweis, kein Fehler; die Meldung
  nennt ihr Verzeichnis und die Zahl der Notizen darin (§5.4),
- `provisional` steht nur an einer Typdefinition und nur mit dem Wert `true`;
  eine vorläufige Typdefinition trägt weder einen Abschnitt `# Properties`
  noch `bundles`,
- Dateinamen innerhalb eines Typverzeichnisses eindeutig,
- alle Frontmatter-Werte entsprechen §3.4, keine verschachtelten Werte,
- jeder Property-Typ hat eine gültige `form`; kein Property-Typ für eine
  native Wertform; kein eigener Property-Typ endet auf `-list`; die
  Standard-Property-Typen entsprechen §3.5.1,
- jede in einer Property-Tabelle aufgeführte Property erfüllt ihren Typ:
  Wertform, `pattern`, `values`, `min`, `max`, und bei `hkf-link` und
  `hkf-file` Zieltyp beziehungsweise Medienart nach §3.7.1; bei mehreren
  Alternativen genügt eine (§3.7.2),
- alle Alternativen einer Typ-Angabe haben dieselbe Wertform,
- jede als Pflicht markierte Property ist vorhanden,
- jede Vorgabe erfüllt die Typ-Angabe ihrer Property, und keine
  Pflicht-Property trägt eine (§3.7),
- jeder in einer Property-Tabelle genannte Typ existiert als Wertform, als
  Property-Typ oder als dessen Listenform nach §3.5.2, jeder genannte Zieltyp
  ist registriert, und der `:`-Zusatz steht nur an `hkf-link` oder
  `hkf-link-list`,
- alle internen Verweise sind qualifizierte Wikilinks nach §3.6 und auflösbar;
  in der Wurzeldatei ohne Ablagepfad, in Notizen mit,
- interne Verweise tragen einen Alias — fehlt er, ist das ein Hinweis, kein
  Fehler (§3.6),
- `modified` liegt nicht vor `created`,
- in einer HKB trägt jede Notiz `created` und `modified` — fehlt eines, ist
  das ein Hinweis, kein Fehler,
- unmittelbar unter `media_base` liegen nur `images`, `videos`, `audios` und
  `documents`; kein Typverzeichnis liegt unter `media_base`,
- jeder `hkf-file`-Wert zeigt auf eine vorhandene Datei in einem
  Medienverzeichnis, trägt eine Dateiendung, endet nicht auf `.md` und
  erfüllt die geforderte Medienart,
- die Typtabelle der Wurzeldatei stimmt mit den Typdefinitionen überein,
- alle Standard-Property-Typen aus §3.5.1 sind vorhanden,
- jede Bundle-Notiz hat eine `id` gleich ihrem Dateinamen, in der Form aus
  §4.1, dazu eine `version` und eine `description`,
- jeder Eintrag in `required_bundles` hat die Form aus §4.1, setzt nicht das
  eigene Bundle voraus und bildet keinen Kreis; eine Fassungsbedingung steht
  nur an einer Fassung der Form `Zahl.Zahl`,
- jeder Importnachweis hat die Form aus §5.1; ein Eintrag ohne vorhandenes
  Ziel ist ein Hinweis, kein Fehler,
- jeder Entscheidungsnachweis hat die Form aus §5.7: fünf Spalten, ein Urteil
  aus der erlaubten Menge, ein nichtleeres **Von**, **Beurteilt** und **Grund**,
  und je Gegenstand höchstens eine Zeile. Ein zweites Urteil über denselben
  Gegenstand ist ein Fehler — welches gälte, wäre nicht bestimmt,
- keine Zeile des Entscheidungsnachweises nennt einen strukturellen Konflikt
  als Gegenstand; aufgezeichnet werden nur Bedeutungs- und Identitätsurteile
  (§5.7),
- jeder Wikilink in `bundles` zeigt auf eine vorhandene Bundle-Notiz,
- keine zwei Notizen tragen denselben Wert in einer Property vom Typ
  `hkf-wikidata` — sie bezeichnen dann denselben Gegenstand und sind ein
  Zusammenführungskandidat; das ist ein Hinweis, kein Fehler,
- jeder Abschnitt `# Siehe auch` hat die Form aus §5.6: ein Listenpunkt je
  Zeile aus qualifiziertem Wikilink, ` — ` und einem Grund. Ein fehlender
  Grund ist ein Fehler; eine gestörte alphabetische Ordnung und ein Abschnitt,
  der nicht der letzte ist, sind Hinweise,
- kein Ziel steht zugleich unter `# Siehe auch` und in `rejected_links` —
  das ist ein Fehler, weil beide einander widersprechen,
- kein Eintrag unter `# Siehe auch` ist ein bloßer Rückverweis: Zeigt die
  Zielnotiz bereits hierher und nennt der eigene Body sie nicht, ist der
  Eintrag ein Hinweis — die Auskunft steht schon in der Backlink-Ansicht
  (§5.6),
- jeder Eintrag unter `# Siehe auch` steht auch in `related`, es sei denn, sein
  Ziel steht in einer anderen Property derselben Notiz; fehlt er, ist das ein
  Hinweis. Die Umkehrung wird nicht geprüft — `related` darf Adressen und von
  Hand gesetzte Verweise enthalten (§5.6),
- eine Notiz, auf die kein einziger Verweis zeigt, ist ein Hinweis: Sie ist
  über die Wissensbasis nicht erreichbar,
- keine Notiz trägt `bundles` oder `rejected_links` mit leerer Liste.

Jeder Befund nennt Datei, Zeile soweit bestimmbar, Schweregrad und eine
verständliche Meldung.

`--fix` darf ausschließlich:

- die Typtabelle der Wurzeldatei neu erzeugen,
- fehlende Standard-Property-Typen anlegen,
- einen verzeichnislosen Wikilink auf eine Notiz in einem Typverzeichnis
  qualifizieren, **wenn genau ein Ziel existiert**,
- einen fehlenden Alias aus dem `title` des Ziels ergänzen,
- die Leerzeichen um einen Alternativen-Trenner ` / ` ergänzen,
- einen `datetime`-Wert ohne Uhrzeit auf den Tagesbeginn ausschreiben,
- fehlendes `created` und `modified` in einer HKB ergänzen und `modified_by`
  auf `hk-lint` setzen. Der Linter weiß nicht, wer die Notiz zuvor geändert
  hat — aber er selbst hat sie soeben geändert, und §3.3 verlangt beide
  Felder von jedem, der das tut. Ein leeres `modified_by` neben einem frisch
  gesetzten `modified` wäre die Behauptung, niemand sei es gewesen,
- die Einträge eines Abschnitts `# Siehe auch` alphabetisch ordnen und den
  Abschnitt ans Ende der Notiz stellen,
- `related` um die Ziele aus `# Siehe auch` ergänzen, die dort fehlen und in
  keiner anderen Property stehen; entfernt wird daraus nichts,
- leere Properties und `null`-Werte entfernen.

Bei mehrdeutigen oder unbekannten Zielen wird nicht geraten. Nach einem
Korrekturlauf wird erneut geprüft.

`--fix` ergänzt keinen Eintrag unter `# Siehe auch` und entfernt keinen. Es
ordnet nur, was dasteht: Verknüpfen ist Sache des Imports (§6.1 Schritt 9),
Entfernen Sache eines Menschen (§5.6).

`--fix` legt keine vorläufige Typdefinition an und entfernt keine. Sie
entsteht beim Import, und sie vergeht, wenn die richtige Typdefinition
nachgeliefert wird (§5.4); dazwischen liegt eine Entscheidung über Bedeutung,
und die trifft kein Linter.

### `--strict`

`hk-lint --strict` meldet zusätzlich **undeklarierte Properties**: jede
Property einer Notiz, die weder in der Property-Tabelle ihres Typs steht noch
zu den notizübergreifenden Properties gehört (Anhang A.2).

Diese Befunde sind **Hinweise, keine Fehler**. Sie ändern nichts an §3.3:
zusätzliche flache Properties bleiben zulässig, und eine Notiz wird davon
nicht unkonform. Der Modus macht nur sichtbar, was die Property-Tabelle nicht
abdeckt — sonst bliebe es unbemerkt, etwa ein versehentlich im Editor
gesetztes `country` an einer `person`.

Die Ausgabe wird **je Typ und Property-Name zusammengefasst**, mit der Zahl
der betroffenen Notizen:

```text
person: country in 1 von 2 Notizen
source: isbn_alt in 4 von 4 Notizen
```

Diese Zusammenfassung trennt die beiden Fälle, die hinter einer undeklarierten
Property stecken können:

- **Wenige Notizen** — meist ein Versehen. Die Property gehört entfernt.
- **Fast alle Notizen eines Typs** — die Property hat sich eingebürgert und
  gehört in die Property-Tabelle des Typs.

`--strict` verändert nichts. `--fix` legt keine Tabellenzeilen an; welcher der
beiden Fälle vorliegt, entscheidet ein Mensch.

---

# 7. Konformität

## 7.1 Ein HKF-Bundle ist konform, wenn

1. `hbundle.md` in seiner Wurzel liegt und §4.1 erfüllt — `id` und
   `description`, mehr wird nicht verlangt,
2. es jede verwendete Typdefinition und jeden verwendeten Property-Typ
   enthält, die nicht zur Grundausstattung aus §3.8 gehören und die kein
   vorausgesetztes Bundle liefert, sowie jede referenzierte Mediendatei —
   **gleich in welchem Verzeichnis** (§4.3),
3. keine zwei Notizen desselben Typs denselben Dateinamen tragen,
4. jede Notiz `type` trägt; wo sie liegt, ist gleichgültig,
5. alle Frontmatter-Werte den Wertformen aus §3.4 entsprechen und die
   Property-Tabellen ihrer Typen erfüllen,
6. alle internen Verweise Wikilinks nach §3.6 auf Dateien der Lieferung sind
   und sich eindeutig auflösen,
7. kein Standard-Property-Typ umdefiniert wird,
8. keine Notiz die Property `bundles` oder `rejected_links` trägt,
9. `hbundle.md` weder Import- noch Entscheidungsnachweis enthält,
10. jeder Eintrag in `required_bundles` §4.1 erfüllt, und
11. keine Typdefinition `provisional: true` trägt (§5.4).

## 7.2 Eine HKB ist konform, wenn

1. `hkb.md` mit `hkf: "1.0"` und `name` im Wurzelverzeichnis der HKB liegt
   und keine weitere Ablage darunter liegt,
2. `Typedefs`, `Proptypes` und `Bundles` im Basispfad existieren, soweit sie
   nicht leer wären, und unter `media_base` nur die vier Medienverzeichnisse
   aus §3.2.1 liegen,
3. die Grundausstattung aus §3.8 vorhanden ist — die Kern-Typen `typedef`,
   `proptype` und `bundle` sowie die dreizehn Property-Typen aus §3.5.1,
4. jeder geführte Typ aus HKF Config dessen Fassung entspricht,
5. jede Notiz `type` trägt und im passenden Typverzeichnis liegt,
6. alle Frontmatter-Werte den Wertformen aus §3.4 entsprechen und die
   Property-Tabellen ihrer Typen erfüllen,
7. alle internen Verweise qualifizierte Wikilinks nach §3.6 sind, jeder
   `hkf-file`-Wert auf eine vorhandene Mediendatei der geforderten Art zeigt
   und jeder Abschnitt `# Siehe auch` §5.6 erfüllt, und
8. jede Bundle-Notiz §5.1 samt Import- und Entscheidungsnachweis erfüllt und
   jeder `bundles`-Eintrag auflösbar ist.

Unbekannte zusätzliche Properties und freie Markdown-Struktur machen eine
Notiz nicht ungültig. Vorläufige Typdefinitionen machen eine HKB nicht
unkonform: Der Typ ist registriert, seine Notizen liegen am richtigen Ort und
seine Verweise sind prüfbar — ungeklärt ist allein die Bedeutung (§5.4). Ein
Bundle darf eine solche Typdefinition dagegen nicht enthalten (§7.1).

---

# 8. Versionierung

Diese Fassung ist **HKF Core 1.0**. Minor-Versionen ergänzen Regeln, ohne
bestehende Bundles oder HKBs ungültig zu machen. Eine Major-Version darf
Identität, Wertformen, die Standard-Property-Typen oder die Ablagestruktur
ändern.

**Core und Config werden getrennt fortgeschrieben.** Die Property `hkf` in der
Wurzeldatei nennt die Fassung von Core und sonst nichts. Welche Fassung des
Vokabulars eine Wissensbasis führt, steht in der `version` der zugehörigen
Bundle-Notiz — dort, wo jede andere Lieferung auch verbucht wird. Config darf
damit Typen und Werte ergänzen, ohne dass Core eine neue Nummer bekommt; und
Core darf sich ändern, ohne dass jede Wissensbasis ihr Vokabular neu lädt.
Config 1.0 setzt Core 1.0 voraus.

Erkennt eine HKB die `hkf`-Version eines Bundles nicht, liest sie die Dateien,
leitet aber keine Identitäten ab und importiert nicht.

---

# Anhang A — Wurzeldateien und allgemeine Properties

Dieser Anhang beantwortet abschließend, welche Properties wo erlaubt sind: in
den Wurzeldateien, in jeder Notiz unabhängig vom Typ, und in den drei
Kern-Typen aus §3.8.

## A.1 Wurzeldateien

`hkb.md` und `hbundle.md` sind keine Notizen (§3.1). Sie tragen ausschließlich
diese Properties:

| Property | Typ | `hkb.md` | `hbundle.md` | Beschreibung |
|---|---|---|---|---|
| `hkf` | text | Pflicht | optional | Formatversion, in dieser Fassung `"1.0"` |
| `name` | text | Pflicht | — | Anzeigename der HKB |
| `base` | text | optional | ohne Wirkung | Basispfad der Typverzeichnisse |
| `media_base` | text | optional | ohne Wirkung | Basispfad der Medienverzeichnisse |
| `timezone` | text | optional | optional | IANA-Zonenname für Ortszeiten (§3.4) |
| `spec` | text | optional | optional | Wo die geltende Spezifikation steht |

„Ohne Wirkung" heißt: Ein Bundle darf die Property tragen, aber kein Werkzeug
wertet sie aus. Ein Bundle hat weder Typ- noch Medienverzeichnisse (§4.3).
Alle Namen sind `snake_case` wie in jeder Notiz (§3.4) — die Wurzeldatei ist
keine eigene Welt.

`spec` sagt, **wo** die Spezifikation zu lesen ist; `hkf` sagt, **welche
Fassung** von Core gilt. Der Wert ist entweder ein Wikilink auf eine Notiz vom Typ
`specification` oder eine URL — dieselbe Alternative wie in §3.7.2, beide
Formen sind `text`. Als Wikilink verweist er nach §3.6 relativ zur
Wurzeldatei, also ohne Ablagepfad:

```yaml
spec: "[[Specifications/hkf-core-1.0|HKF Core 1.0]]"
spec: https://example.org/hkf/1.0
```

Die Wikilink-Form setzt voraus, dass die Wissensbasis den Typ `specification`
führt — er kommt aus HKF Config oder wird selbst definiert. Eine Wissensbasis,
die nur Core erfüllt, kennt ihn nicht und schreibt eine URL.

`hbundle.md` ist zugleich die Bundle-Notiz und trägt darum zusätzlich alle
Properties des Typs `bundle` aus HKF Config §3.3.

Der Body beider Dateien enthält den Abschnitt `# Typen` (§3.1).

## A.2 Notizübergreifende Properties

Diese Properties sind in **jeder** Notiz erlaubt, gleich welchen Typs. Sie
brauchen keinen Eintrag in einer Property-Tabelle.

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| `type` | text | ja | — | Typ der Notiz; MUSS zum Verzeichnis passen (§3.2) |
| `title` | text | nein | — | Anzeigetitel; ohne ihn gilt der Dateiname |
| `description` | text | nein | — | Einzeiler zum Inhalt |
| `tags` | list | nein | — | Obsidian-eigen |
| `aliases` | list | nein | — | Obsidian-eigen; auch für Synonyme |
| `cssclasses` | list | nein | — | Obsidian-eigen |
| `status` | text | nein | — | Bearbeitungsstand |
| `created` | date | nein | — | Tag der Entstehung |
| `modified` | datetime | nein | — | Zeitpunkt der letzten Änderung, in **UTC** (§3.4) |
| `modified_by` | text | nein | — | Wer zuletzt geändert hat |
| `bundles` | hkf-link-list:bundle | nein | — | Zugehörigkeit; nur in einer HKB (§5.2) |
| `related` | hkf-link-or-url-list | nein | — | Verwandtes: Verweise in die eigene Ablage oder Adressen im Netz (§5.6) |
| `rejected_links` | hkf-link-list | nein | — | Ziele, die nicht selbsttätig verlinkt werden; nur in einer HKB (§5.6) |

### Die drei Zeitangaben

`created` ist ein Tag, `modified` ein Zeitpunkt in UTC. Beide Asymmetrien sind
gewollt: Für die Entstehung genügt der Tag, für die Reihenfolge zweier
Fassungen nicht — und diese Reihenfolge muss über Zonen und über den
Zeitumstellungstermin hinweg feststehen (§3.4). Ein `modified` ohne Uhrzeit
bezeichnet den Tagesbeginn.

`modified_by` nennt, wer die Notiz zuletzt geändert hat. **Ein Sprachmodell
MUSS dort seinen Modellnamen eintragen**, etwa `claude-opus-5`; ein Werkzeug
seinen eigenen Namen, etwa `hk-import`. Bei einer Änderung von Hand bleibt das
Feld dem Menschen überlassen — Obsidian setzt es nicht, und `hk-lint` kann es
nicht nachprüfen. Der Wert ist deshalb keine Zusicherung über den letzten
Bearbeiter, sondern eine Selbstauskunft der Maschinen: Er sagt verlässlich,
*dass* eine Maschine zuletzt geschrieben hat, und welche.

In einem Bundle sind alle drei freigestellt (§4). In einer HKB werden sie
geführt: Fehlt eines beim Import oder beim Anlegen, wird es gesetzt (§6.1);
`hk-lint` meldet ein fehlendes als Hinweis und `--fix` ergänzt es.

Die Property-Tabelle eines Typs darf eine dieser Properties **verschärfen**,
also als Pflicht führen — so verlangt `bundle` eine `description`
(HKF Config §3.3). Was
hier steht, ist die Vorgabe, nicht die Obergrenze.

Darüber hinaus darf jede Notiz weitere flache Properties tragen; sie werden
nicht geprüft und müssen erhalten bleiben (§3.3). `hk-lint --strict` listet
sie als Hinweis auf (§6.3). Wer `status` auf feste Werte
festlegen will, definiert dafür einen eigenen Property-Typ mit `values` — HKF
schreibt keine vor, weil die Werte sich je Wissensbasis unterscheiden.

## A.3 Die Kern-Typen

Die Typdefinitionen von `typedef`, `proptype` und `bundle` stehen in
[HKF Config §3.1 bis §3.3](HKF-Config-V1.0.md) — zusammen mit allen übrigen,
damit keine Typdefinition an zwei Orten gepflegt wird.

Sie gehören zur Grundausstattung: angelegt, nicht geliefert (§5.3), und von
einem Bundle nicht mitzubringen (§7.1). Welches Verzeichnis sie beanspruchen,
sagt §3.8.

---

# Anhang B — Grammatik

**Normativ.** Dieser Anhang legt die Schreibweise zweier Dinge fest, die überall
im Format vorkommen und die ein Werkzeug erkennen muss, bevor es irgendetwas
beurteilen kann: **Wikilinks** (§3.6) und **Typangaben** in einer
Property-Tabelle (§3.7.1).

Notation ist ABNF nach RFC 5234. `ALPHA`, `DIGIT` und `SP` sind dort definiert;
`*` heißt „beliebig oft", `1*` „mindestens einmal", `[…]` „freigestellt",
`/` trennt Alternativen. Bei Abweichung zwischen Prosa und Grammatik gilt die
Grammatik.

## B.1 Gemeinsame Bausteine

```abnf
kebab        = LOWER *( LOWER / DIGIT / "-" )
LOWER        = %x61-7A

pfad         = segment *( "/" segment )
segment      = 1*seg-zeichen

; jedes Zeichen ausser Steuerzeichen, "/", "]" und "|"
seg-zeichen  = %x20-2E / %x30-5C / %x5E-7B / %x7D-10FFFF
```

`kebab` beschreibt Typnamen (§3.7), Property-Typ-Namen (§3.5), Dateinamen von
Notizen (§3.2) und die `id` eines Bundles (§4.1) — überall dieselbe Form:
Kleinbuchstaben, Ziffern und Bindestriche, beginnend mit einem Buchstaben.

`segment` ist bewusst weiter gefasst. Ein Wikilink-Ziel enthält den Ablagepfad,
und der ist ein Verzeichnis im Vault, das sich niemand nach unseren Regeln
aussucht.

## B.2 Wikilinks

```abnf
wikilink     = "[[" ziel [ "|" alias ] "]]"
einbettung   = "!" wikilink

ziel         = pfad
alias        = 1*alias-zeichen

; jedes Zeichen ausser Steuerzeichen, "]" und "|"
alias-zeichen = %x20-5C / %x5E-7B / %x7D-10FFFF
```

**In einer Markdown-Tabellenzelle** wird der Trennstrich maskiert; die Zelle
enthält dann nicht `wikilink`, sondern:

```abnf
wikilink-zelle = "[[" ziel [ "\|" alias ] "]]"
```

Das `\` gehört zur Tabelle, nicht zum Verweis (§3.6). Ein Werkzeug entfernt es,
bevor es das Ziel auflöst.

**Was die Grammatik nicht ausdrückt** und was zusätzlich gelten muss:

1. Kein `segment` ist `.` oder `..`, und `ziel` endet nicht auf `.md` (§3.6).
2. Zeigt `ziel` auf eine Mediendatei, trägt es deren Dateiendung; zeigt es auf
   eine Notiz, trägt es keine (§3.6).
3. In einer HKB beginnt `ziel` mit Ablagepfad und `base`; in einem Bundle ist
   es der Pfad in der Lieferung (§3.6, §4.3).
4. `einbettung` steht nur im Body, nie in einer Property (§3.5.1).

## B.3 Typangaben

```abnf
typzelle      = typangabe *( " / " typangabe )

typangabe     = wertform / link-angabe / file-angabe / proptyp-angabe

wertform      = "text" / "list" / "number" / "checkbox" / "date" / "datetime"

link-angabe   = "hkf-link" [ "-list" ] [ ":" zieltypen ]
file-angabe   = "hkf-file" [ "-list" ] [ ":" medienarten ]
proptyp-angabe = proptyp-name [ "-list" ]

zieltypen     = typname *( "," typname )
medienarten   = medienart *( "," medienart )
medienart     = "image" / "video" / "audio" / "document"

typname       = kebab
proptyp-name  = kebab
```

**Die Alternativen sind in dieser Reihenfolge zu versuchen.** `hkf-link` und
`hkf-file` erfüllen als Zeichenketten auch `proptyp-name`; nur weil ihre
eigenen Regeln zuerst greifen, ist der `:`-Zusatz an ihnen erlaubt und
anderswo nicht. Ein Werkzeug, das `proptyp-angabe` zuerst probiert, hielte
`hkf-link:person` für einen Property-Typ namens `hkf-link` mit unerklärtem
Rest.

Ebenso wird ein `-list` **zuerst abgetrennt** und erst dann entschieden, welche
Argumente zulässig sind (§3.5.2) — sonst gilt `hkf-link-list:person` als
unzulässig, obwohl §3.7.1 es ausdrücklich erlaubt.

**Was die Grammatik nicht ausdrückt:**

1. `proptyp-name` endet nicht auf `-list`; die Listenform entsteht durch die
   Regel aus §3.5.2, nicht durch eine eigene Notiz (§3.5).
2. Jeder `typname` in `zieltypen` ist in der Ablage registriert, sonst ist es
   ein Fehler an der Typdefinition (§3.7.1).
3. Alle `typangabe` einer `typzelle` haben dieselbe Wertform (§3.7.2).
4. Die Leerzeichen um das `/` sind Pflicht. Ein Werkzeug liest den Trenner auch
   ohne sie; geschrieben wird er mit, und `hk-lint --fix` ergänzt sie (§3.7.2).
5. `hkf-link-or-url` ist ein gewöhnlicher `proptyp-name` und nimmt darum keinen
   `:`-Zusatz (§3.5.1).

## B.4 Das Frontmatter-Schema

Für das Frontmatter gibt es keine ABNF, sondern ein **JSON Schema**:
`schema/hkf-core-1.0.schema.json` im Repository dieser Spezifikation. Es ist
normativ, und es deckt ab, was sich ohne Kenntnis der Typdefinitionen prüfen
lässt:

- die sechs Wertformen und das Verbot verschachtelter Werte (§3.4),
- `snake_case` als Form jedes Property-Namens (§3.4),
- `type` als einzige Pflicht einer Notiz (§3.3),
- die notizübergreifenden Properties samt ihrer Typen (A.2),
- die dreizehn Standard-Property-Typen als Muster und Grenzen (§3.5.1),
- die beiden Wurzeldateien mit ihren Pflichten (A.1, §4.1).

Drei Einstiegspunkte: `#/$defs/notiz`, `#/$defs/hkb`, `#/$defs/hbundle`.

**Warum JSON Schema und nicht ABNF.** Eine Grammatik beschreibt eine
Zeichenkette; Frontmatter ist eine Abbildung von Namen auf Werte, und was
daran zu prüfen ist — welcher Name welche Wertform verlangt, was Pflicht ist,
was zusätzlich erlaubt bleibt — sind Aussagen über diese Abbildung, nicht über
ihre Schreibweise. Die Schreibweise ist YAML und anderswo festgelegt.

**Was es nicht prüfen kann.** Alles, was die Typdefinitionen der Ablage
angeht: ob eine Property in der Tabelle ihres Typs steht, ob eine dort als
Pflicht geführte fehlt, ob ein `hkf-link` auf den geforderten Zieltyp zeigt.
Das Schema kennt den Typ einer Notiz, aber nicht seine Definition — die liegt
in der Ablage, nicht in der Spezifikation.

**Datum und Zeitpunkt.** YAML liest `1815-12-10` als Datum, nicht als Text. Vor
der Prüfung sind solche Werte in ihre ISO-Schreibweise zu bringen; das Schema
mustert sie dann als Text. Ein Werkzeug, das YAML anders lädt, muss dasselbe
tun, sonst prüft es an dieser Stelle nichts.
