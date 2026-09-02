---
name: hkb-typseite
description: "Typseiten und Bases für die Typen einer Wissensbasis anlegen, damit `type` als Verweis geschrieben werden kann statt als Wort. Verwenden bei: Typseiten anlegen, Types und Bases erzeugen, hk-types, Typ soll anklickbar sein, auf die Linkform umstellen."
---

# Typseiten anlegen

Zuerst [[hkb]] lesen. Angelegt wird mit `hk-types`; von Hand schreibst du
weder eine Typseite noch eine Base.

## Worum es geht

`type` trägt den Typnamen als Text oder einen Verweis auf eine **Typseite**
(Core §3.3):

```yaml
type: person
type: "[[90-System/Types/Type Person|Type Person]]"
```

Beide nennen denselben Typ. Als Text ist der Typ ein Wort, an dem nichts
hängt. Als Verweis ist er anklickbar, sammelt Backlinks, und auf der Typseite
steht, was ihn ausmacht — eine Erklärung, eine eingebettete Tabelle aller
Notizen dieses Typs.

Eine Typseite liegt unter `<config_base>/Types/` und bindet sich über
`definition` an genau eine Typdefinition. **Sie trägt kein `type`**: Sie ist
keine Notiz, sondern Grammatik, wie die Typdefinition, auf die sie zeigt.

## Erst prüfen, ob die Ablage sie will

Die Linkform ist eine Möglichkeit und keine Vorschrift. Drei Fragen vorher:

- **Wird die Wissensbasis in Obsidian benutzt?** Der Gewinn ist ein
  Obsidian-Gewinn — Backlinks, Klick, Bases. Eine Ablage, die nur von
  Werkzeugen gelesen wird, hat nichts davon.
- **Für alle Typen oder für keinen?** Zwei Schreibweisen nebeneinander sind
  zulässig, aber niemand liest sie gern. Wenn schon, dann alle.
- **Ist das die Entscheidung des Benutzers?** Die Umstellung berührt jede
  Notiz. Frag, statt sie anzunehmen.

## Anlegen

```bash
hk-types --check          # was entstünde
hk-types                  # Typseiten und Bases anlegen
hk-types --umstellen      # dazu `type` in allen Notizen auf die Linkform
hk-lint
```

Je Typ entsteht `Types/Type <Typ>.md` und, sofern nicht `--ohne-bases`,
`Bases/<Typ>.base`. Vorhandene bleiben unberührt; das Skript ist
wiederholbar. Ein neuer Typ braucht danach einen weiteren Lauf — oder keinen,
wenn die Ablage bei der Textform bleibt.

**`--umstellen` schreibt in jede Notiz.** Nur auf einem sauberen Git-Stand
und nachdem der Benutzer zugestimmt hat. Ohne die Option ändert sich an den
Notizen nichts, und beide Schreibweisen bleiben gültig.

## Was das Skript nicht entscheidet

**Den Namen der Typseite.** Es schreibt `Type <Typ>`, weil ein Name gewählt
sein muss. Das Format schreibt keinen vor: Aufgelöst wird über `definition`
und nie über den Dateinamen. Wer die Seiten anders nennen will — `Person`,
`Menschen`, `Personen` —, benennt sie um und zieht die Verweise mit; Obsidian
tut das von allein. Danach `hk-lint`.

**Was auf der Typseite steht.** Das Skript legt den Rumpf an: `definition`,
`aliases`, die eingebettete Base. Der Body ist der Ort, an dem eine
Wissensbasis sagt, wofür sie diesen Typ führt und wofür nicht — was in der
Typdefinition als `# Konventionen` überall gilt, steht hier für dieses Haus.
Das schreibst du, nicht das Skript, und du schreibst es nur, wenn es etwas zu
sagen gibt.

**Ob es Bases geben soll.** `.base` ist Obsidian und nicht HKF. Der Ordner
liegt außerhalb der Ablage und kommt in keiner Prüfung vor. Braucht die
Wissensbasis keine Tabellen, dann `--ohne-bases`.

## Was danach von allein geschieht

`hk-import` schreibt `type` in der Schreibweise des Hauses: als Verweis,
sobald es eine Typseite für den Typ gibt, sonst als Text — auch in der
Bundle-Notiz und in einer vorläufigen Typdefinition, die es selbst anlegt.
`hk-export` schreibt immer zurück in die Textform: **Die Linkform reist nicht
mit** (Core §4.2). Eine Typseite gehört der Wissensbasis, aus der die
Lieferung kommt; beim Empfänger gibt es sie nicht oder sie heißt anders.

Um beides musst du dich nicht kümmern. Was du prüfst, ist der Befund danach.

## Die Befunde, die dabei anfallen

| Befund | Was zu tun ist |
|---|---|
| `zeigt auf keine Typseite` | Die Typseite fehlt oder wurde umbenannt. `hk-types` erneut laufen lassen, oder den Verweis auf die vorhandene Seite ziehen. |
| `trägt kein definition` | Eine Datei unter `Types/`, die keine Typseite ist. Entweder `definition` ergänzen oder sie dort wegnehmen. |
| `definition nennt … — dort liegt keine Typdefinition` | Der Verweis zeigt daneben, meist auf einen Property-Typ. |
| `Für den Typ … gibt es mehrere Typseiten` | Zwei Seiten nennen dieselbe Typdefinition. Der Import wüsste nicht, welche er nehmen soll. Eine davon löschen — das ist ein Urteil, keine Mechanik. |
| `liegt in X/, der Typ … gehört nach Y/` | Der Verweis hat aufgelöst, und der Typ passt nicht zum Verzeichnis. Die Linkform ändert an Regel 1 nichts. |

## Was du nicht tust

- **Keine Typseite von Hand schreiben.** Dafür ist `hk-types` da.
- **`type` in einer Lieferung nicht verlinken.** Dort steht der Typname als
  Text (Core §4.2). `hk-lint` meldet es.
- **Keine Typdefinition anfassen.** Eine Typseite zeigt auf sie und ersetzt
  sie nicht. Was ein Typ zusichert, steht weiter in `Typedefs/` — dafür gibt
  es [[hkb-typ]].
