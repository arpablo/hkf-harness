---
name: hkb-export
description: "Ein Bundle aus einer Wissensbasis herausschreiben und die Befunde beurteilen, die dabei anfallen — vorläufige Typen, Verweise aus der Lieferung hinaus, Mediendateien ohne Verweis. Verwenden bei: Bundle exportieren, Lieferung herausschreiben, hk-export, etwas weitergeben."
---

# Eine Lieferung herausschreiben

Zuerst [[hkb]] lesen. `hk-export` erledigt die acht Schritte aus §6.2. Zu
entscheiden gibt es nichts — zu **beurteilen** aber schon: ob das Ergebnis
weitergegeben werden kann.

## Ablauf

```bash
hk-export <bundle-id> <zielpfad>
```

Welche Bundles es gibt, sagt `<base>/Bundles/`. Geschrieben wird der
typbezogene Baum mit `Typedefs/`, `Proptypes/`, je einem Verzeichnis pro Typ
und `media/<art>/` — auch wenn ein Bundle beliebig aufgebaut sein dürfte.
Streng im Schreiben, großzügig im Lesen.

Danach prüfst du die Lieferung, denn `hk-lint` kann das auch:

```bash
hk-lint <zielpfad>
```

## Was du beurteilst

### Ein vorläufiger Typ (§5.4)

> `Der Typ maschine ist nur vorläufig registriert und wird nicht mitgeschrieben.`

Das Bundle ist damit **in seinen Typen nicht geschlossen**. Eine vorläufige
Typdefinition behauptet nichts; sie mitzuschicken hieße, eine Vermutung als
Vertrag auszugeben. Sag dem Menschen, welches Bundle die richtige
Typdefinition liefern müsste, und dass die Lieferung bis dahin unvollständig
ist.

### Verweise aus dem Bundle hinaus (§6.2 Schritt 8)

> `[[Maschines/analytical-engine]] zeigt aus dem Bundle hinaus und bleibt stehen.`

Sie bleiben erhalten und zeigen beim Empfänger ins Leere. Das ist zulässig —
das Bundle ist dann in seinen Typen, aber nicht in allen Verweisen
geschlossen. Nenne sie beim Namen, damit der Absender entscheiden kann, ob er
die fehlenden Notizen mitliefert oder die Verweise streicht.

Einträge unter `# Siehe auch`, die hinauszeigen, entfernt der Export von
selbst: Sie gelten nur hier, und beim Empfänger entstehen sie beim Import neu.

### Mediendateien, die zurückbleiben (§6.2 Schritt 4)

> `2 Mediendateien kamen mit der Lieferung, hängen aber an keiner Notiz.`

Der Import nimmt jede Datei mit, der Export nur die, auf die eine Notiz
zeigt. Wer die Dateien mitgeben will, verweist sie in einer Notiz — das ist
eine inhaltliche Entscheidung und keine des Werkzeugs.

## Was der Export nicht mitnimmt

Sag es dazu, wenn der Empfänger es wissen muss:

- `bundles` und `rejected_links` — sie beschreiben, wie **diese**
  Wissensbasis die Lieferung einsortiert und beurteilt hat (§4.2).
- `imported`, die Importnachweise und der Entscheidungsnachweis (§5.1, §5.7).
- Die Grundausstattung und alles, was ein vorausgesetztes Bundle liefert
  (§7.1) — dafür steht `required_bundles` im `hbundle.md`.

## Der Rundlauf ist nicht buchstäblich

Ein Bundle, das importiert und sofort wieder exportiert wird, kommt nicht
byte-gleich zurück: Verweise zwischen zwei Notizen **derselben** Lieferung
überstehen den Export und stehen im Ergebnis unter `# Siehe auch`. Das ist
gewollt — der Import hat etwas erkannt, was in der Lieferung nicht stand.
Erkläre es, wenn jemand den Unterschied bemerkt; es ist kein Fehler.
