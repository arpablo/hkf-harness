---
title: hkb-ingest
status: vorgeschlagen
tags:
  - hkf
  - quellen
  - ingest
  - wissensbasis
---

# hkb-ingest

## Auftrag

`hkb-ingest` macht aus einer Quelle keine Sammlung von Namen, sondern eine nachvollziehbare, belegte Erklärung dessen, was ein Werk sagt. Das Zielformat ist immer ein importierbares **HKF-Bundle**, nicht ein Patchsatz und nicht eine lose Sammlung von Markdown-Dateien. Das Bundle hat `hbundle.md` in seiner Wurzel, eine Quellennotiz, die daraus abgeleiteten Notizen sowie die für einen Import nötigen Typ- und Property-Definitionen.

Das Ergebnis muss zwei Zugänge zugleich bieten:

- Wer nach einer Person, einem Ereignis oder einer Institution fragt, findet die zugehörige Notiz mit den Aussagen der Quelle.
- Wer nach der Erklärung des Werkes fragt, findet eine quellengebundene Antwort mit ihren Begriffen, Kausalzusammenhängen, Grenzen und Fundstellen.

Der heutige Ablauf erfüllt den ersten Zugang oft, den zweiten nicht zuverlässig. Die Fromkin-Lieferung zeigt den Fehler deutlich. Sie führt Akteure und Episoden aus den ersten zwölf Kapiteln, aber keine Erklärung, wie Fromkin die Instabilität des Nahen Ostens herleitet, und keine Begriffsnotizen zu Imperialismus oder Kolonialismus.

> [!important] Maßstab
> Ein Buch-Ingest ist nicht fertig, wenn er Namen verlinkt hat. Er ist fertig, wenn die zentrale Frage des Werks in einer dem Autor zugeschriebenen, belegten Synthese beantwortet werden kann.

## Nicht verhandelbare Leistungsanforderungen

Der heutige Ingest kontrolliert seine Formate und Übergaben zu oft, während er die tragenden Erklärungen eines Werks verlieren kann. Das ist ein Fehler des Produkts, nicht eine Eigenschaft, die Benutzer hinnehmen müssen.

Der neue Ablauf muss daher gleichzeitig diese Ziele erfüllen:

| Anforderung | Messbarer Nachweis |
|---|---|
| Wesentliches zuerst | Der Aufbau-Lauf führt zentrale Frage, These und Erklärungsthemen. Eine Tranche darf nicht abgeschlossen werden, wenn sie ein berührtes Thema ohne Behandlung lässt. |
| Halbiertes Tokenbudget | Für einen vergleichbaren Ingest darf der Gesamtverbrauch höchstens 50 Prozent des bisherigen Referenzlaufs betragen. Der gemessene Referenzwert von 233.739 Token setzt damit ein Ziel von höchstens 116.870 Token. |
| Fünf Minuten je Arbeitseinheit | Eine Tranche ist so geschnitten, dass Lesen, Evidenzdatei und Schreiben jeweils innerhalb von fünf Minuten enden. Reicht ein Kapitel nicht, wird es vor dem Start in kleinere, inhaltlich zusammenhängende Einheiten geteilt. |
| Fortsetzbar ohne Wiederholung | Nach jeder Einheit stehen Karte, Evidenzdatei und geänderte Notizen auf der Platte. Eine Fortsetzung liest nur den offenen Abschnitt. |
| Prüfen mit Zweck | Jeder Prüfschritt muss einen bekannten Fehler verhindern. Er prüft nur die geänderten Dateien und darf keinen neuen KI-Lauf auslösen, wenn ein Script den Befund entscheiden kann. |

Die Anforderungen gelten gemeinsam. Ein Lauf, der unter dem Budget bleibt und die Erklärung des Werks verfehlt, ist fehlgeschlagen. Ebenso ist ein inhaltlich guter Lauf fehlgeschlagen, wenn er den Quelltext oder die Evidenzkarten mehrfach durch Kontexte kopiert, bis sein Verbrauch den Nutzen übersteigt.

### Schlanke Qualitätskontrolle

Die Kontrolle richtet sich auf Ergebnis und Belegkette, nicht auf Selbstüberwachung des Prozesses:

1. **Vor der Tranche:** Die offene Erklärungskarte nennt die Frage, die beantwortet werden soll.
2. **Nach dem Evidenz-Lauf:** Jede Evidenzkarte enthält Behauptung, Mechanismus und Lokator. Fehlt eines davon, geht sie nicht in den Themen-Compiler.
3. **Nach dem Themen-Compiler:** Jede neue Notiz beantwortet entweder ihre vorgesehene Frage oder markiert ehrlich, was die Quelle dazu nicht trägt.
4. **Nach der letzten Tranche:** Die Kernaussagen beantworten die zentrale Werkfrage. Sie dürfen keine bloße Liste von Personen, Kapiteln oder Ereignissen sein.
5. **Danach:** `hk-lint`, `hk-text --gate` und `hk-import --check` prüfen ausschließlich das entstandene Bundle.

Mehr Kontrolle braucht der Standardweg nicht. Insbesondere gibt es keine Vollprüfung des Bestands, kein zweites Lektorat und keinen erneuten Quellenabruf als Routine.

## Architektur ist offen

`hkb-ingest` beschreibt ein Ergebnis, keinen Umbau des heutigen `hkb-quelle` in kleinen Schritten. Kein bestehender Agent, kein Dateiformat, kein Script und keine Trennung von Lesen und Schreiben ist gesetzt, wenn eine andere Architektur die Leistungsanforderungen besser erfüllt.

Die bestehende Rollenverteilung ist deshalb nur eine Vergleichsarchitektur. Zulässig sind unter anderem:

- ein Quellenagent, der Analyse und Schreiben in einem Lauf verbindet;
- getrennte Lese- und Schreibagenten mit dateibasierter Übergabe;
- eine programmatische Extraktion mit einem Modell nur für Belegauswahl und Synthese;
- ein hierarchischer Ablauf mit kleinen Leseeinheiten und einer materialisierten Gesamtsynthese;
- zusätzliche oder entfallende Rollen, sofern sie Ergebnisqualität erhöhen oder den gemessenen Verbrauch senken.

Keine Variante darf aufgrund ihrer Nähe zur bisherigen Implementierung bevorzugt werden. Sie wird an derselben Quelle gegen dieselben Kriterien gemessen: zentrale Erklärung gefunden, Belege und Lokatoren korrekt, Ergebnis lesbar, höchstens fünf Minuten je Arbeitseinheit und höchstens die Hälfte des Referenzbudgets.

> [!tip] Entscheidungsregel
> Nicht fragen: „Passt das in den heutigen Ablauf oder die aktuelle Spezifikation?“ Fragen: „Liefert es die beste belegte Erklärung innerhalb des Budgets?“ Erst die erfolgreiche Variante bestimmt die künftigen Rollen, Dateien und Specs.

## Konkreter Vorschlag: Evidenz-Compiler

Der erste zu bauende Kandidat ist kein Umbau von `hkb-quelle`, sondern ein neuer, evidenzbasierter Compiler. Er trennt nicht primär Agenten, sondern Datenstufen. Ein Modell liest eine Textstelle genau einmal und legt daraus maschinenlesbare Belege ab. Ein zweites Modell schreibt nur aus den gefilterten Belegen. Dazwischen arbeiten Scripts.

```text
Quelldatei
  │
  ├─ hk-extract ──────────────► Textsegmente mit stabilen Seitenmarken
  │                                  │
  ├─ Plan-Lauf ───────────────► Fragen- und Themenplan
  │                                  │
  ├─ Evidenz-Läufe ───────────► Evidenzjournal und Abdeckungsstand
  │                                  │
  ├─ Themen-Compiler ─────────► Bundle-Notizen im Build-Baum
  │                                  │
  └─ Synthese-Compiler ───────► Kernaussagen, offene Grenzen, Abschluss
                                     │
                                     └─ Scripts: Struktur, Links, Bundle-Check und gezielter Lint
```

Die Rollen können als getrennte Agenten, als Modi desselben Agenten oder teilweise als Programme implementiert werden. Die Dateien zwischen den Stufen sind die Schnittstellen, nicht Chat-Antworten.

### Agenten des ersten Prototyps

Der erste Prototyp arbeitet ausschließlich mit eigenen Agenten für den Evidenz-Compiler.

| Agent | Aufgabe | Schreibt |
|---|---|---|
| `alva` | Quellenplan mit Werkfrage, Erklärungsthemen und offenen Fragen | `plan.yaml` |
| `berta` | lokatorgenaue Evidenz aus einem Textsegment | segmentbezogenes JSONL und Status |
| `cora` | lesbare Änderungen aus einem Themenpaket | isolierter Bundle-Patch |
| `dina` | abschließende, quellengebundene Synthese | Synthese-Patch für den Bundle-Baum |

Keiner dieser Agenten gibt ein Langdestillat im Chat zurück. Der Agentenvertrag selbst begrenzt seine Eingabe auf die Daten seiner Stufe und seine Ausführung auf fünf Minuten.

### Arbeitsartefakte und Lieferbaum

Die Arbeitsartefakte liegen außerhalb der späteren Lieferung. Sie sind Laufzustand und dürfen bei einer neuen Fassung der Quelle neu erstellt werden. Der Build-Baum `bundle/` ist dagegen bereits die Lieferung: Nach dem Merge wird er ohne Umformung mit `hk-import --check` geprüft und kann importiert werden.

| Datei | Zweck | Schreibt | Liest |
|---|---|---|---|
| `manifest.json` | Quelle, Ausgabe, Prüfsumme, Seiten- und Segmentgrenzen, Budgets | `hk-extract` | alle Stufen |
| `plan.yaml` | zentrale Werkfrage, Erklärungsthemen, offene Fragen, erwartete Ausgaben | Plan-Lauf | Evidenz- und Themen-Compiler |
| `evidence.jsonl` | eine belastbare Behauptung je Zeile mit Lokator und Themenkennungen | Evidenz-Lauf | Index und Compiler |
| `coverage.json` | je Segment und Thema: offen, belegt, nicht tragfähig oder Synthese offen | Script | Koordination und Synthese |
| `patches/` | isolierte, noch nicht übernommene Änderungen am Bundle-Baum | Themen- und Synthese-Compiler | Merge-Schritt |
| `bundle/` | HKF-Bundle mit `hbundle.md`, Notizen, `Typedefs/`, `Proptypes/` und bei Bedarf `Media/` | Build- und Merge-Schritt | Lint, Text-Gate, Import-Check |

`bundle/hbundle.md` enthält die Bundle-Kennung und Beschreibung. Die Quellennotiz und alle abgeleiteten Notizen liegen innerhalb von `bundle/`; Links in ihnen sind bundle-relativ. Jeder verwendete nicht-basale Typ und Property-Typ wird im Bundle mitgeliefert oder über `required_bundles` explizit vorausgesetzt. Arbeitsdateien wie `evidence.jsonl` werden nicht in das Bundle übernommen.

Ein Evidenzeintrag hat einen kleinen, festen Vertrag:

```json
{
  "segment": "p. 88-102",
  "themes": ["instabilitaet-nahost", "imperiale-ordnung"],
  "claim": "<dem Autor zugeschriebene Teilbehauptung>",
  "mechanism": "<Annahme oder Entscheidung führt zu einer Folge>",
  "locator": "S. 96",
  "kind": "causal_claim",
  "qualification": "<Grenze, Gegenbeleg oder leer>"
}
```

Das Schema erzwingt, was im bisherigen Lauf fehlte: Eine Person, ein Ereignis oder ein Begriff wird nur dann zum Kernbestandteil, wenn er zu einer Werkfrage oder einem Mechanismus beiträgt. Ein bloßer Name bleibt zulässiger Kontext, aber er verdrängt keine Erklärung.

### Stufe 1: Text vorbereiten

`hk-extract` extrahiert den Text lokal, bewahrt Seitenmarken und Inhaltsverzeichnis und schneidet ihn in feste, zusammenhängende Segmente. Die Segmentgröße wird anhand einer Tokenzählung gewählt, nicht anhand von Kapitelnummern. Ist ein Kapitel zu groß für das Fünf-Minuten-Budget, entsteht daraus mehr als ein Segment.

Diese Stufe enthält kein Modell und kostet keine Modelltoken. Sie verhindert, dass einzelne Agenten PDF-Werkzeuge, Seitenzählung und Textumbruch jeweils neu lösen.

### Stufe 2: Plan statt Figurenliste

Der Plan-Lauf sieht nur Titelmaterial, Inhaltsverzeichnis, Einleitung, Schluss und eine kleine Auswahl von Kapitelanfängen. Er schreibt `plan.yaml`.

Für jedes Werk sind darin verpflichtend:

- die zentrale Frage des Autors;
- höchstens zwölf Erklärungsthemen;
- die zu jedem Thema erwartete Frage;
- die Begriffe, die ein Thema tragen könnten;
- die Fragen, die erst nach vollständiger Lektüre beantwortet werden dürfen.

Für Fromkin müssten vor dem ersten analytischen Segment mindestens diese Fragen im Plan stehen:

- Welche Mechanismen verbindet er mit der späteren Instabilität der Region?
- Welche Rolle spielen imperiale oder koloniale Ordnungsannahmen in seiner Darstellung?
- Welche Fehldeutungen regionaler Akteure und Institutionen schreibt er europäischen Entscheidungsträgern zu?
- Welche Teile dieser Erklärung sind nach der ersten Tranche noch nicht gedeckt?

Der Plan ist kein Aufsatz und keine Prognose. Er ist eine explizite Abnahmevereinbarung für die folgenden Läufe.

### Stufe 3: Ein Lesezug pro Segment

Der Evidenz-Lauf erhält genau ein Textsegment und die wenigen Themen, die laut Plan dort wahrscheinlich berührt werden. Er schreibt Evidenzeinträge, aber keine Notizen und keine Kapitelzusammenfassung.

Er hat drei Prioritäten:

1. Kausalsätze und Definitionen finden, die eine Werkfrage beantworten.
2. Nur die Akteure, Ereignisse und Begriffe erfassen, die einen solchen Satz tragen.
3. Neue, klar zentrale Themen als Vorschlag markieren, statt sie still zu verschweigen.

Ein Segment ist nach höchstens fünf Minuten fertig. Überschreitet es sein Budget, wird es durch `hk-extract` weiter geteilt und nicht in einem längeren Kontext fortgesetzt. Das bereits geschriebene Evidenzjournal bleibt gültig.

### Stufe 4: Deterministischer Index und Abdeckungstest

`hk-evidence index` gruppiert Evidenzeinträge nach Thema und Segment. `hk-evidence coverage` prüft ohne Modell:

- Hat jedes bearbeitete Segment einen Abschlusszustand?
- Hat jedes berührte Erklärungsthema mindestens einen Evidenzeintrag oder den Status `nicht_tragfaehig`?
- Verweist jede vorgesehene Synthesenotiz auf mindestens einen Lokator?
- Welche Planfragen sind nach den bisher gelesenen Segmenten noch offen?

Der Test prüft nicht, ob eine Notiz schön klingt. Er verhindert das konkrete Versagen des bisherigen Ingests: dass der Lauf mit vielen Personen fertig wirkt, obwohl eine zentrale Werkfrage nirgends bearbeitet wurde.

### Stufe 5: Themen-Compiler schreibt in den Bundle-Baum

Der Themen-Compiler liest ein Themenpaket aus dem Index, nicht die Quelle. Ein Paket enthält nur die Evidenzen für eine Frage, die bestehende Zielnotiz und die erforderliche Typdefinition.

Er erstellt einen isolierten, konfliktfrei mergbaren Patch **gegen `bundle/`** für:

- die zugehörige Passage der Quellennotiz;
- eine Begriffsnotiz oder Ergänzung, wenn der Begriff die Frage tatsächlich trägt;
- eine quellengebundene Notiz, wenn eine Erklärung nicht als allgemeines Konzept ausgegeben werden darf.

Das Patchformat erlaubt mehrere Themenläufe ohne konkurrierende Änderungen an denselben Dateien. Ein Script übernimmt nur konfliktfreie Patches in `bundle/`. Es legt bei neuen Typen zugleich die nötigen Dateien in `bundle/Typedefs/` und `bundle/Proptypes/` an. Konflikte werden als eine klare Entscheidung vorgelegt, nicht durch einen weiteren Volltextlauf gelöst.

### Stufe 6: Synthese nur aus dem Evidenzjournal

Der Synthese-Compiler liest die zentralen Fragen aus `plan.yaml`, ihren Abdeckungsstand und die gruppierten Evidenzen. Er darf keine neue Behauptung erzeugen, die keine Evidenzkarte trägt. Sein Patch verändert ausschließlich `bundle/`.

Er schreibt `# Kernaussagen` und gegebenenfalls eine Note wie „Fromkins Erklärung der späteren Instabilität des Nahen Ostens“. Ist eine Frage noch offen, schreibt er nicht ersatzweise eine glatte Gesamtthese, sondern nennt den noch ungelesenen Bereich.

### Budget für den ersten Vergleichslauf

Für die bereits gemessene Quelle mit 41.637 Zeichen gilt zunächst dieses harte Budget:

| Stufe | Obergrenze |
|---|---:|
| Plan-Lauf | 8.000 Token |
| Evidenz-Läufe insgesamt | 55.000 Token |
| Themen-Compiler insgesamt | 32.000 Token |
| Synthese und gezielte Prüfung | 18.000 Token |
| **Gesamt** | **113.000 Token** |

Damit bleibt der Lauf unter dem Ziel von 116.870 Token. Für ein ganzes Buch wird das Budget proportional zur tatsächlich gelesenen Textmenge fortgeschrieben. Es ist keine Zusage, dass ein 895-Seiten-Buch mit dem Budget eines kurzen Artikels lesbar wird. Die harte Kennzahl ist die Halbierung gegenüber dem alten Ablauf für denselben Textumfang und dieselbe erwartete Abdeckung.

### Fromkin als Pilot

Der Pilot beginnt nicht mit allen 895 Seiten, sondern mit Teilen I und II. Er gilt nur dann als erfolgreich, wenn er zugleich:

- die erste Tranche als begrenzt markiert und keine Gesamtthese vortäuscht;
- eine Evidenzkette zu imperialen Ordnungsannahmen, Großmachtkonkurrenz und Fehldeutungen regionaler Ordnung erzeugt, soweit die Tranche sie trägt;
- sichtbar sagt, welche Teile der Frage nach späterer Instabilität erst in den folgenden Teilen beantwortet werden können;
- weniger als die Hälfte der Token des alten Referenzlaufs für denselben Ausschnitt braucht;
- je Lese- und Schreibsegment innerhalb von fünf Minuten bleibt.

Erst danach wird derselbe Entwurf an einer kurzen Webseite und einer mittleren Fachquelle gemessen. Besteht er diese drei Fälle nicht, wird die Architektur geändert oder verworfen, nicht mit weiteren Kontrollen überdeckt.

## Das Ziel hat Vorrang vor der bestehenden Spezifikation

HKF Core, HKF Config und der Harness sind Mittel für eine lesbare, überprüfbare Wissensbasis. Sie sind kein Grund, ein besseres Ingest-Ergebnis abzulehnen oder es in eine unpassende Ausnahme zu zwängen. Das Ziel bleibt dabei verbindlich: Die Lieferung muss als HKF-Bundle importierbar sein.

Wenn eine bestehende Festlegung verhindert, dass ein Ingest die Erklärung eines Werkes zuverlässig, belegbar und tokeneffizient festhält, wird die Festlegung geändert. Das gilt insbesondere für:

- die zulässigen Bestandteile einer Quellennotiz und eines Bundles;
- den Status einer unvollständigen oder vollständigen Lektüre;
- die Definition von `summary`, `note`, `concept` und gegebenenfalls eines neuen Arbeitsartefakts;
- die Regeln für Lesekarten, Evidenzkarten und die abschließende Synthese;
- die Prüfungen von `hk-lint` und die Import- und Exportlogik.

> [!warning] Keine Sonderwege
> Eine geänderte Anforderung wird nicht als stillschweigende Ausnahme im Skill umgesetzt. Die Spezifikation, Typdefinitionen, Scripts, Tests und Dokumentation werden gemeinsam angepasst. Danach ist die neue Regel wieder für jede Wissensbasis nachvollziehbar und prüfbar.

Der Maßstab für eine Spezifikationsänderung lautet: Erhöht sie die Fähigkeit, Quellen wahrheitsgemäß, nutzbar und überprüfbar in Wissen zu überführen, oder senkt sie nachweislich vermeidbaren Kontextverbrauch? Wenn ja, darf die bisherige Form kein Einwand sein.

## Was der Skill nicht versprechen darf

Eine inspektive Lektüre und eine erste Tranche sind kein vollständiger Buch-Ingest. Der Skill muss diesen Zustand sichtbar führen und in seiner Abschlussmeldung sagen:

- welcher Bereich tatsächlich analytisch gelesen wurde;
- welche Tranchen noch offen sind;
- welche Aussagen deshalb nur vorläufig sind;
- welche Gesamtfragen erst nach der letzten Tranche beantwortet werden können.

Eine Lieferung darf erst `complete` heißen, wenn alle geplanten Tranchen abgeschlossen und die Synthesephase gelaufen sind. Eine erste Tranche darf eine vorläufige Erklärung für ihren Bereich schreiben, aber keine Erklärung für die gesamte spätere Ordnung des Nahen Ostens ausgeben.

## Grundsatz: Gegenstände und Erklärungen sind verschiedene Arbeitsobjekte

Der Ingest führt zwei Karten, die nicht gegeneinander ausgespielt werden.

| Karte | Führt | Beispiel bei Fromkin |
|---|---|---|
| Gegenstandskarte | Personen, Orte, Organisationen, Ereignisse und Begriffe, die eine eigene Notiz oder einen Verweis brauchen | Kitchener, Hussein, Sykes-Picot, Kalifat |
| Erklärungskarte | zentrale Fragen, Begriffe, Mechanismen und Gegenargumente des Werks | Imperialismus, Kolonialismus, Großmachtkonkurrenz, Fehldeutung regionaler Ordnungen, widersprüchliche Zusagen |

Die Gegenstandskarte beantwortet: „Wer oder was kommt vor?“ Die Erklärungskarte beantwortet: „Welche Ursache, Annahme oder Entscheidung erklärt nach dem Autor welche Folge?“

Keine der beiden Karten enthält langen Quelltext. Sie verweist auf dauerhaft gespeicherte Evidenzkarten mit Lokatoren.

## Schreibregeln für Begriffe und Synthesen

Ein Begriff wie Imperialismus, Kolonialismus oder Nationalismus wird nicht allein deshalb zur Notiz, weil er in einem Inhaltsverzeichnis vorkommt. Er wird angelegt oder erweitert, wenn mindestens eines gilt:

- Der Autor verwendet ihn als Teil seiner Erklärung.
- Er verbindet mehrere Handlungen oder Kapitel.
- Seine zeitgenössische Bedeutung unterscheidet sich von einer heutigen Verwendung.
- Ohne seine Erklärung lässt sich die These des Werks nicht verstehen.

Die Notiz trennt dabei drei Schichten:

1. allgemeine Bestimmung des Begriffs, nur wenn sie nachschlagbar gesichert ist;
2. Fromkins Verwendung und seine belegten Aussagen;
3. offene Einwände, Gegenliteratur oder Grenzen seiner Perspektive.

Die Synthese „Warum hielten handelnde Personen ihre Nation oder ihr Reich für überlegen?“ ist daher keine psychologische Ferndiagnose. Sie muss als historische Frage geführt werden: Welche zeitgenössischen politischen, imperialen, religiösen oder rassifizierenden Annahmen schreibt Fromkin welchen Akteuren zu, in welchem Zusammenhang und mit welchem Beleg?

## Abschlusskriterien

Ein vollständiger Buch-Ingest besteht erst, wenn:

- jede geplante Tranche einen dokumentierten Zustand hat;
- die Quellennotiz ihren gesamten abgedeckten Bereich entlang des Buchaufbaus zusammenfasst;
- `# Kernaussagen` die zentrale Frage des Werks beantwortet;
- jede zentrale Erklärungskarte entweder zu einer belegten Synthese geführt oder ausdrücklich als nicht tragfähig verworfen wurde;
- zentrale Begriffe nicht nur erwähnt, sondern in ihrer Verwendung im Werk erklärt sind;
- die Grenzen von Fromkins Perspektive als Grenzen der Quelle sichtbar bleiben;
- die Quelldatei, das Destillat und die Evidenzkarten nicht unnötig durch den Hauptkontext kopiert wurden;
- `bundle/hbundle.md` in der Bundle-Wurzel liegt und der Bundle-Vertrag erfüllt ist;
- alle Notizen, Typdefinitionen und Property-Typen im Bundle liegen oder Abhängigkeiten in `required_bundles` ausdrücklich benannt sind;
- Links innerhalb des Bundles bundle-relativ auflösbar sind;
- `hk-lint`, `hk-text --gate` und `hk-import --check bundle/` für die neue Lieferung grün sind.

## Umsetzungsvorschlag

1. Drei feste Testquellen und ihre Fragen definieren: kurze Webseite, mittlere Fachquelle, Fromkin Teile I und II. Den heutigen Ablauf als Baseline sichern.
2. `hk-extract` bauen. Das Werkzeug liefert reproduzierbare, seitenmarkierte Segmente und eine Tokenzählung, aber noch keine semantische Deutung.
3. `plan.yaml`, `evidence.jsonl` und `coverage.json` als Formatvertrag bauen, einschließlich des rein programmatischen Abdeckungstests.
4. Einen einzigen Evidenz-Lauf als Prompt-Modus implementieren. Er schreibt ausschließlich valides JSONL in die Arbeitsdatei und beendet ein Segment innerhalb des Budgets.
5. Einen leeren, gültigen Bundle-Baum mit `hbundle.md`, den nötigen Typdefinitionen und Property-Typen erzeugen. Den Themen-Compiler zuerst für eine einzige Frage bauen, etwa Fromkins Erklärung der Instabilität. Er erzeugt einen Patch gegen diesen Baum und darf keine Aussage ohne Evidenzeintrag schreiben.
6. Synthese, Patch-Merge, gezielten Lint und `hk-import --check` ergänzen. Erst dann wird der gesamte Teil I und II durchlaufen.
7. Gegen Baseline messen. Nur wenn Qualität, Zeit und Tokenbudget gleichzeitig bestehen, werden die Formate in Core, Config, Harness und Tests übernommen. Andernfalls wird der Kandidat ersetzt, nicht mit Ausnahmen gerettet.

Der Vorschlag reduziert Kontrolle auf einen maschinell prüfbaren Belegvertrag. Seine Hauptleistung ist nicht, weniger Notizen zu schreiben. Er stellt sicher, dass die zentrale Erklärung eines Buches zuerst geplant, während der Lektüre belegt und am Ende wirklich geschrieben wird.
