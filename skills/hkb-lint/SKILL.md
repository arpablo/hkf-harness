---
name: hkb-lint
description: "Eine Wissensbasis oder eine Lieferung gegen HKF Core prüfen, die erlaubten Korrekturen anwenden und die Befunde beurteilen, die kein Werkzeug beheben darf. Verwenden bei: Ablage prüfen, hk-lint, Befunde abarbeiten, aufräumen, ist die Wissensbasis konform."
---

# Eine Ablage prüfen und in Ordnung bringen

Zuerst [[hkb]] lesen. `hk-lint` prüft alles aus §6.3 und behebt mit `--fix`
die elf Handgriffe, die es beheben **darf**. Deine Aufgabe fängt bei den
übrigen Befunden an.

## Ablauf

**① Erst ansehen, dann anfassen.**

```bash
hk-lint
```

Gemeldet wird in drei Gruppen — Frontmatter (Anhang B.4), Grammatik
(Anhang B), Struktur (§6.3) — und getrennt nach Schweregrad:

| | |
|---|---|
| **fehler** | Die Ablage ist nicht konform (§7.2). Muss weg. |
| **hinweis** | Fällt auf, macht sie aber nicht ungültig. Darf stehenbleiben. |

Der Rückgabewert ist 1 nur bei Fehlern.

**② Was mechanisch geht, macht das Werkzeug.**

```bash
hk-lint --fix
```

Danach wird von selbst erneut geprüft. Was dann noch dasteht, ist deins.

**③ `--strict`, wenn es um Sauberkeit geht.**

```bash
hk-lint --strict
```

Meldet undeklarierte Properties, je Typ und Name zusammengefasst:
`person: country in 1 von 2 Notizen`. Die Zahl trennt die beiden Fälle —
**wenige** Notizen sind meist ein Versehen und die Property gehört entfernt;
**fast alle** heißt, sie hat sich eingebürgert und gehört in die
Property-Tabelle des Typs (siehe [[hkb-typ]]). Welcher Fall vorliegt,
entscheidest du nicht allein: leg es vor.

## Was `--fix` darf

Typtabelle neu erzeugen · fehlende Standard-Property-Typen anlegen · einen
verzeichnislosen Wikilink qualifizieren, **wenn genau ein Ziel existiert** ·
einen fehlenden Alias aus dem `title` ergänzen · den Trenner ` / `
ausschreiben · ein `datetime` ohne Uhrzeit auf den Tagesbeginn bringen ·
`created` und `modified` ergänzen · `# Siehe auch` ordnen und ans Ende
stellen · `related` daraus ergänzen · leere Properties entfernen.

## Was `--fix` nicht darf — und du auch nicht

- **Keinen Eintrag unter `# Siehe auch` ergänzen oder entfernen.**
  Verknüpfen ist Sache des Imports (§6.1 Schritt 9), Entfernen Sache eines
  Menschen (§5.6). Soll ein Verweis dauerhaft weg, kommt sein Ziel in
  `rejected_links` — und das schreibt ein Mensch.
- **Keine vorläufige Typdefinition anlegen oder entfernen.** Dazwischen liegt
  eine Entscheidung über Bedeutung (§5.4).
- **Bei mehrdeutigen Zielen nicht raten.** Zwei Dateien mit demselben Namen:
  vorlegen.

## Die Befunde, die dir bleiben

| Befund | Was zu tun ist |
|---|---|
| `[[…]] lässt sich nicht auflösen` | Die Notiz gibt es nicht (mehr). Ziel suchen, Verweis berichtigen oder mit dem Menschen klären — nicht raten. |
| `modified liegt vor created` | Eine der beiden Angaben ist falsch. Welche, weiß nur, wer die Notiz kennt. |
| `X steht zugleich unter # Siehe auch und in rejected_links` | Ein Widerspruch. Ein Mensch entscheidet, welche der beiden Absichten gilt. |
| `Der Typ X ist vorläufig` | Das Bundle nachladen, das ihn definiert. Bis dahin bleibt es so. |
| `X und Y tragen dieselbe Kennung Q…` | Zusammenführungskandidat. Die beiden Notizen gehören zusammengelegt, nicht verlinkt — und das ist eine inhaltliche Arbeit. |
| `Auf diese Notiz zeigt kein Verweis` | Sie ist nicht erreichbar. Wo gehört sie hin? Ein Verweis von der passenden Notiz aus, mit Grund. |
| `X ist Pflicht und fehlt` | Der Wert fehlt. Ihn zu erfinden ist schlimmer, als ihn offen zu lassen — frag nach. |
| `bloßer Rückverweis` | Der Eintrag verdoppelt, was die Backlink-Ansicht ohnehin zeigt. Ein Mensch darf ihn streichen, du nicht. |

## Auch eine Lieferung

```bash
hk-lint <bundle-pfad>
```

Die Wurzeldatei entscheidet: `hkb.md` heißt Wissensbasis, `hbundle.md` heißt
Lieferung. Dort gilt §7.1 statt §7.2 — kein `bundles`, kein
`rejected_links`, kein Importnachweis, keine vorläufige Typdefinition, und
die verwendeten Typen liegen bei oder stehen in `required_bundles`.

**`--fix` gilt dort nicht.** Eine Lieferung wird gelesen, nicht geändert. Was
an ihr falsch ist, berichtigt der Absender.
