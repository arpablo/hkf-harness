# Henni Knowledge Format — Spezifikation

Das **HKF** beschreibt zwei Dinge: ein übertragbares **Bundle-Format** für
Notizen samt ihrer Typdefinitionen, und eine **Knowledge Base** als
Obsidian-Vault, der solche Bundles importiert und wieder exportiert. Beide
teilen denselben Kern — typbezogene Ablage, native Obsidian-Properties,
qualifizierte Wikilinks.

HKF ist kein Ontologiesystem. Ein Typ ist ein Verzeichnis mit einer
Beschreibung.

Die Struktur ist darauf ausgelegt, dass ein Sprachmodell eine Wissensbasis mit
möglichst wenig Kontext benutzen kann: Eine einzige Datei nennt alle Typen samt
Verzeichnis, eine weitere den vollständigen Vertrag eines Typs.

## Die vier Dateien

| | |
|---|---|
| [`HKF-Core-V1.0.md`](HKF-Core-V1.0.md) | Wie eine Ablage aufgebaut ist |
| [`HKF-Config-V1.0.md`](HKF-Config-V1.0.md) | Alle Typdefinitionen und Property-Typen |
| [`HKF-Harness-V1.0.md`](HKF-Harness-V1.0.md) | Wie eine Umsetzung gebaut ist, und welche Skills, Agenten und Werkzeuge sie enthält |
| [`hkf-core-1.0.schema.json`](hkf-core-1.0.schema.json) | Das Frontmatter als JSON Schema, normativ (Core Anhang B.4) |

**Core** beschreibt Verzeichnisse, Wertformen, Verweise, Typdefinitionen als
Bauform, das Bundle-Format und die drei Methoden `hk-import`, `hk-export` und
`hk-lint`. Es nennt keine einzige konkrete Definition.

**Config** ist das Inventar: zwanzig Typdefinitionen und achtzehn
Property-Typen. Alle zusammen bilden die Grundausstattung: Jede Ablage bekommt
sie beim Anlegen, geliefert wird davon nichts.

**Harness** beschreibt die Umsetzung: die sieben Bereiche einer Ablage, die
Schicht aus Skills und Agenten darüber, und im Abschnitt „Der Bestand" jeden
Skill, jeden Agenten und jedes Werkzeug mit einer Zeile dazu, was er tut. Diese
Tabellen sind normativ, und `tools/bestand.py` hält sie gegen das Verzeichnis.
Core und Config gelten für jede Umsetzung, Harness nur für diese.

Der Schnitt liegt zwischen **Mechanik und Inventar**. Dass eine Notiz im
Verzeichnis ihres Typs liegt, sagt Core. Welche Typen es gibt, sagt Config.
Dass eine Person `born` und `died` trägt, ist dabei eine Verabredung, die man
auch anders treffen kann — eine Wissensbasis über Werkstoffe oder Wertpapiere
kommt ohne sie aus und führt nur die Grundausstattung.

Beide Fassungen werden **getrennt fortgeschrieben**. Die Property `hkf` in der
Wurzeldatei einer Ablage nennt die Fassung von Core, `spec` das Dokument, dem
sie folgt. Config 1.0 setzt Core 1.0 voraus.

## Warum die Spezifikation im Harness liegt

Bis zum 07.09.2026 stand sie in einem eigenen Repository `hkf-spec`, und der
Harness führte eine Kopie unter `spec/`. Das trennte sauber, was zu trennen
war, solange HKF für Dritte gedacht war: eine normative Fassung, die man
zitieren kann, und daneben eine Umsetzung. Diesen Anspruch gibt es nicht mehr.
Übrig blieb der Preis — zwei Orte, ein Skript, das sie gleich hielt, und die
Möglichkeit, dass die Kopie zurückfällt, ohne dass es jemand merkt.

Jetzt gibt es nur noch diesen Ort. Was hier steht, ist die Spezifikation und
zugleich die Fassung, die der Harness umsetzt. `CORE` in
[`lib/hkf/__init__.py`](../lib/hkf/__init__.py) nennt ihre Nummer.

Wer HKF umsetzen will, ohne den Harness zu benutzen, braucht Core, Config und
das Schema und sonst nichts daraus. `HKF-Harness-V1.0.md` beschreibt diese eine
Umsetzung und bindet niemanden sonst.

## Wo der Rest liegt

| Repository | Inhalt |
|---|---|
| [`hkf-kb-template`](https://github.com/arpablo/hkf-kb-template) | Vorlage für eine neue Wissensbasis: die Grundausstattung, sonst nichts. „Use this template" erzeugt daraus ein eigenes Repository. |
| [`hkf-harness`](https://github.com/arpablo/hkf-harness) | Dieses Repository: die Umsetzung der Methoden aus §6 und die KI-Schicht darüber |

## Prüfung

Drei Skripte halten die Spezifikation gegen das, was daneben liegt. Wer sie
ändert, führt beide aus, bevor er den Rest für unverändert hält.

```
python3 tools/inventar.py          Prosa, Schema und Grundausstattung gegeneinander
python3 tools/grundausstattung.py  die Vorlage gegen Anhang A und §3.5.1
python3 tools/bestand.py           die Tabellen in Harness gegen skills/, agents/ und bin/
```

Das Inventar steht dreimal: als Tabelle in `HKF-Config-V1.0.md`, als `$defs`
im Schema und als ausgelieferte Datei unter `templates/hkb/`. `inventar.py`
vergleicht die drei und meldet jede Abweichung, bis hin zu den Zahlwörtern im
Fließtext. Die Rauchprobe ruft beide mit auf.
