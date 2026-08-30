---
type: proptype
form: text
pattern: '^Q[1-9]\d*$'
created: 2026-08-27
modified: 2026-08-29T07:55:00
modified_by: claude-opus-5
---

Kennung des Gegenstands in Wikidata, etwa `Q7259` für Ada Lovelace. Der Wert
ist die nackte Kennung, keine Adresse.

Anders als alle übrigen Property-Typen beschreibt diese Kennung nicht die
Notiz, sondern das, worüber sie handelt. Zwei Notizen mit derselben Kennung
meinen denselben Gegenstand — auch wenn sie verschieden heißen und aus
verschiedenen Lieferungen stammen.

# Weitere Angaben beschaffen

Aus der Kennung `Q…` führen drei Wege zu maschinenlesbaren Daten:

| Zweck | Adresse |
|---|---|
| Alle Aussagen zu einem Gegenstand | `https://www.wikidata.org/wiki/Special:EntityData/Q7259.json` |
| Einzelner Gegenstand, kompakter | `https://www.wikidata.org/w/rest.php/wikibase/v1/entities/items/Q7259` |
| Abfrage über viele Gegenstände | SPARQL an `https://query.wikidata.org/sparql` |

Für Menschen: `https://www.wikidata.org/wiki/Q7259`.

Die Angaben stehen als nummerierte Eigenschaften. Diese lohnen sich für die
Typen dieser Wissensbasis:

| Eigenschaft | Bedeutung | Ziel-Property |
|---|---|---|
| `P31` | ist ein / Art des Gegenstands | Typwahl prüfen |
| `P569`, `P570` | Geburts-, Sterbedatum | `born`, `died` |
| `P19`, `P20` | Geburts-, Sterbeort | `birthplace` |
| `P571` | Gründung | `founded` |
| `P625` | Koordinaten | `latitude`, `longitude` |
| `P17` | Staat | `country` |
| `P856` | offizielle Webseite | `homepage` |
| `P18` | Bild | `portrait`, `logo`, `image` |
| `P227`, `P214`, `P496` | GND, VIAF, ORCID | eigene Property-Typen |

# Regeln für den Umgang

- **Die Kennung bleibt der Anker, die Daten kommen in eigene Properties.**
  Ein abgerufenes Geburtsdatum gehört nach `born`, nicht als Kopie eines
  Wikidata-Datensatzes in die Notiz. Die Wissensbasis spiegelt Wikidata
  nicht.
- **Vorhandene Werte nicht stillschweigend überschreiben.** Weicht ein
  abgerufener Wert von dem in der Notiz ab, ist das zu melden, nicht zu
  ersetzen — die Notiz kann recht haben.
- **Vor dem Übernehmen prüfen, ob die Kennung den gemeinten Gegenstand
  bezeichnet.** `P31` und das Label sind dafür der schnellste Test.
  Verwechselte Kennungen sind der häufigste Fehler.
- **Zusammenführungen behandeln.** Wird ein Eintrag mit einem anderen
  vereinigt, antwortet die Abfrage mit einer Weiterleitung auf die neue
  Kennung. Das ist kein Fehler; die Notiz sollte auf die neue Kennung
  umgestellt werden.
- **Ohne Netz arbeiten können.** Die Kennung ist eine Zugabe. Jede Notiz
  bleibt ohne sie vollständig benutzbar, und keine Prüfung nach §6.3 hängt an
  einem Abruf.
- **Nicht alles hat eine Kennung.** Eigene Vorhaben, Kolleginnen und Kollegen,
  interne Vorgänge stehen nicht in Wikidata. Die Property ist deshalb nirgends
  Pflicht.
