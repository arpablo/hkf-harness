---
type: proptype
form: list
items: 2
pattern: '^-?[0-9]{1,3}([.,][0-9]+)?$'
unit: Grad
created: 2026-09-04
modified: 2026-09-04T00:00:00
modified_by: claude-opus-5
---

Eine geographische Koordinate als Paar aus zwei Dezimalgraden. **Erst die Breite, dann die Länge**, wie in `hkf-latitude` und `hkf-longitude`, wie auf jeder Karte und wie in jedem Kartendienst.

Die Reihenfolge steht hier so ausdrücklich, weil sie sich nicht am Wert ablesen lässt: Berlin trägt 52.5200 und 13.4050, und beide Zahlen wären für sich genommen auch als Länge denkbar. Wer sie vertauscht, verschiebt jeden Ort, und auffallen würde es erst auf einer Karte.

Für einen Ort, der beide Werte getrennt führen soll, gibt es `hkf-latitude` und `hkf-longitude`. Der Paartyp steht daneben, weil eine Ablage die Koordinate oft als eine Angabe schreibt und weil ein Kartenplugin sie so liest.

`items: 2` prüft, dass es ein Paar ist. Dass die Breite zwischen -90 und 90 liegt und die Länge zwischen -180 und 180, prüft der Ausdruck nicht: Eine Grenze je Eintragsstelle kennt HKF nicht.
