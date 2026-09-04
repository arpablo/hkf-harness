---
type: typedef
base: output
title: Essay
description: Ein Text, der eine eigene These vertritt und sie aus dem Bestand belegt.
created: 2026-09-04
modified: 2026-09-04T00:00:00
modified_by: claude-opus-5
---

# Properties

| Property | Typ | Pflicht | Vorgabe | Beschreibung |
|---|---|---|---|---|
| subtitle | text | nein | — | Untertitel, wenn der Titel allein zu wenig sagt |
| authors | hkf-link-or-text-list | nein | — | Wer ihn geschrieben hat, als Notiz oder als Name |
| publications | hkf-link-list:publication | nein | — | In welchen Publikationen er steht. Wird von `hk-publikation` geführt |
| status | text | nein | — | Stand der Arbeit, etwa `entwurf`, `lektorat`, `fertig` |
| words | number | nein | — | Wortzahl des Body, ohne Frontmatter |
| sources | hkf-link-list | nein | — | Worauf der Essay sich beruft |
| related | hkf-link-or-url-list | nein | — | Verwandtes: Notizen oder Adressen. Nimmt auf, was unter „Siehe auch“ steht |

# Konventionen

Ein Essay behauptet etwas. Das unterscheidet ihn von einer Wissensnotiz, die sagt, was der Fall ist, und von einem `text`, der erzählt. Er darf sich irren, und er muss sagen, worauf er sich stützt.

Der Body beginnt mit der These und nicht mit einer Hinführung. Was gegen sie spricht, steht darin und nicht in einer Fußnote.

**Ein Essay ist ein Erzeugnis und liegt darum unter `output_base`.** Er beruft sich auf den Bestand, der Bestand beruft sich nicht auf ihn. Eine Wissensnotiz, die einen Essay als Beleg führte, hätte ihre Aussage aus einer Behauptung genommen.

`sources` trägt hier keinen Zieltyp. Eine Lieferung muss in ihren Typen geschlossen sein (§7.1), und `source` liegt außerhalb. Wer den Typ nach dem Import enger fassen will, schreibt `hkf-link-list:source` in seine Fassung der Typdefinition.
