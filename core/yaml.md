# YAML-Metadaten

Diese Datei ist die gemeinsame Grammatik für YAML-Frontmatter. Welche Felder ein Vault oder ein Notiztyp braucht, bestimmen die lokalen Typdefinitionen. Alles, was hier nicht steht, folgt der YAML-Spezifikation.

Frontmatter steht am Anfang der Datei zwischen zwei `---`-Zeilen, ohne Leerzeile und ohne Überschrift davor. Jede neu geschriebene oder bearbeitete Datei mit Frontmatter muss parsen. Ein YAML-Fehler ist ein Defekt und wird vor Weiterverarbeitung, Commit oder Publikation korrigiert.

## Hausregeln über die Spezifikation hinaus

Deutscher Fließtext in `name`, `description`, `summary` und in den Einträgen von `aliases` steht in doppelten Anführungszeichen, auch wenn der Wert kein problematisches Zeichen enthält. Wikilinks stehen immer in doppelten Anführungszeichen, weil sie eckige Klammern tragen.

Mehrfachwerte stehen als Blockliste. Komma-Strings und Inline-Arrays sind nicht zulässig. Obsidian verwendet ausschließlich `aliases` als Liste, und das Feld `alias` wird nie benutzt, auch nicht bei einem einzigen Alias.

```yaml
type: "[[Geschichte]]"
aliases:
  - "Henni"
```

Werte mit Zwischenstufen, führenden Nullen oder bedeutenden Vorzeichen stehen als String, ebenso Koordinaten. Datumsfelder verwenden `YYYY-MM-DD`, und ob sie gequotet werden, entscheidet der lokale Parser. Ein bewusst offenes Datum ist ein leerer String und kein fehlendes Feld.

```yaml
wordCount: 1858
score: "1-"
reviewedCodex: ""
```

Tags sind kleingeschrieben und kebab-case und bestehen nie nur aus Ziffern. Ein Jahr wird Teil eines sinntragenden Tags oder entfällt ganz. Status und Lifecycle gehören in ein eigenes `status`-Feld und werden nicht als thematische Tags geführt. Die zulässigen Statuswerte bestimmt der lokale Vault.
