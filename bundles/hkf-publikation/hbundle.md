---
hkf: "1.0"
type: bundle
id: hkf-publikation
title: Publikation und Text
description: Zwei Typen für Ablagen, die aus ihrem Bestand etwas veröffentlichen. Ein Text steht für sich, eine Publikation ordnet Texte zu einer Lesereihenfolge.
version: "2026-09-04"
---

Diese beiden Typen gehören nicht in die Grundausstattung. Eine Wissensbasis, die nichts veröffentlicht, braucht sie nicht, und was sie nicht braucht, soll sie nicht tragen.

Wer sie will, importiert die Lieferung:

```bash
hk-import <pfad-zu-dieser-lieferung>
```

Danach kennt die Ablage `text` und `publication`, und `hk-publikation`, `hk-buch` und `hk-epub` finden, womit sie arbeiten.

# Typen

| Typ | Verzeichnis | Zweck |
|---|---|---|
| essay | Essays | Ein Text, der eine eigene These vertritt und sie aus dem Bestand belegt. |
| publication | Publications | Eine Folge von Texten in einer festgelegten Lesereihenfolge. |
| text | Texts | Ein Stück Prosa, das für sich steht. |
