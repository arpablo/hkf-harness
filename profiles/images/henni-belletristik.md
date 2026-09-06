# Bildprofil henni-belletristik

Dieses Profil beschreibt die Bildsprache der Henriette-Einstein-Belletristik. Es gilt für die Stories, die Kapitel ihrer Publikationsreihen und die Essays, die zu dieser Strecke gehören. Sachliche Inhalte, historische Kapitel und alle übrigen Essays bleiben bei `henni-default`.

Der Unterschied zum Hausstil ist der Render. `henni-default` verlangt einen sauberen, leicht stilisierten 3D-Render, und genau das kostet in der Belletristik die Wiedererkennbarkeit der Figur. Das Modell stilisiert Gesichter so weit, dass eine mitgegebene Personenreferenz nicht mehr durchkommt. Deshalb arbeitet dieses Profil fotografisch.

## Visuelle DNA

Hochwertig, editorial und cinematisch, mit ruhiger Komposition und Atemraum. Der Look ist eine natürliche Fotografie mit realistischer Haut, echtem Tageslicht und glaubwürdigen Materialien. Keine Renderanmutung, keine geglätteten CGI-Oberflächen, keine Puppenhaftigkeit.

Die Bilder dürfen wie Reportagefotos wirken. Was sie nicht dürfen, ist wie ein Werbefoto aussehen: keine Hochglanzretusche, keine Studioblitze, keine perfekte Haut.

## Farbpalette

- Leitakzent: warmes Orange bis Terrakotta und Koralle.
- Gegenpol: entsättigtes Schiefer-Blaugrau bis Anthrazit.
- Basis: gebrochenes Weiß, weiche Hellgrautöne.
- Sparsamer Zweitakzent: Senfgelb, nur als Tupfer.
- Prinzip: ein warmer Akzent gegen einen kühlen Neutralton, oft als warm-kühle Aufteilung der Szene.

Die Palette bleibt dieselbe wie im Hausstil. Sie hält die Reihe zusammen, auch wenn der Render wechselt.

## Die Figur

Zeigt eine Szene Henriette erkennbar, gelten drei Bedingungen zusätzlich zur Bildreferenz aus dem Vault.

Der Ausschnitt reicht höchstens bis zur Hüfte. Bewährt ist `medium editorial composition, the woman framed from the waist up and filling a large part of the frame, her face clearly readable`. Eine Totale mit ganzer Figur trifft die Ähnlichkeit nie, weil dem Gesicht die Auflösung fehlt.

Das Haar wird als kurzes Lockenhaar beschrieben, nicht als gewelltes und nicht als lange Mähne: `chin- to collarbone-length layered blonde shag with a soft fringe and loose natural curls`. Zwei ältere Fassungen sind überholt, `shoulder-length wavy` ergibt glattes Haar und `shoulder-length voluminous curly` eine zu lange Mähne. An der Länge scheitert die Wiedererkennung genauso schnell wie an der Struktur.

Die Erkennbarkeit entscheidet, nicht der Bildtyp. Trägt ein als Sachbild geplantes Motiv eine Spiegelung, einen Schatten oder eine angeschnittene Figur, die der Leser als Henriette lesen soll, ist es ein Personenbild und braucht Referenz und Character-Feld.

Dazu immer die Zusicherung `exactly one woman in the image, no duplicate, no twin`. Bei einer Personenreferenz verdoppelt das Modell die Figur sonst.

## Motiv und Requisiten

Das Bild zeigt genau das, was der Inhalts-Prompt beschreibt, und nicht mehr. Keine dekorativen Stillleben-Requisiten von sich aus ergänzen, also keine Vasen, Schalen, Früchte, Trockenblumen oder Zimmerpflanzen, sofern die Szene sie nicht verlangt.

## Beschriftungen

Ein vom Bildmodell erzeugtes Bild trägt keinen Text. Keine Schilder, keine Etiketten, keine Titel, keine Marken. Das Modell rendert Text unzuverlässig, und es schreibt in der Sprache des Prompts, also englisch in einer deutschen Notiz.

Für Marken gilt derselbe Grundsatz mit einer Ausnahme. Wo eine Karosserieform stimmen muss, nennt der Prompt das Modell und verbietet im selben Satz Embleme, Nabendeckel-Logos, Schriftzüge und Kennzeichen. Eine Form ist keine Beschriftung, ein Emblem schon.

Dasselbe gilt für Alltagsgegenstände, und dort wird es regelmäßig übersehen. Sporttaschen, Trikots, Schuhe, Jacken, Flaschen und Bar-Regale bekommen vom Modell von sich aus eine Marke, auch wenn niemand danach gefragt hat. Am 05.09.2026 haben fünf von sechs Bildern einer einzigen Geschichte Marken getragen. Darunter waren ein Nike-Logo auf einer Sporttasche, ein Ford-Emblem, die Schriftzüge Punto und Vectra, ein britisches Kennzeichen in einer deutschen Straße und ein gesticktes Monogramm auf einem Trikot.

Der Prompt zählt deshalb die Gegenstände der Szene auf und nennt sie ausdrücklich blank, etwa `the gym bags are plain unbranded canvas, the sports shirt carries no crest and no maker's mark`. Danach steht das harte Verbot, `absolutely no brand logos anywhere in the image, no swoosh, no stripes, no wordmarks, no emblems, not even small or partly hidden ones`.

Beides gehört in den Motivteil des Prompts und nicht als Nachsatz an sein Ende. Der Nachsatz am Ende hat in allen Fehlläufen nicht gegriffen, die Aufzählung im Motivteil in allen Neuläufen. Das ist dieselbe Mechanik wie beim bedruckten Papier: Ein Verbot wirkt dort, wo das Modell den Gegenstand baut.

## Register

Die Reihe hat ein erotisches Register, und die Bilder tragen es mit. Wirkung entsteht über Haltung, Blick und Stoff, nicht über Entblößung. Was den NSFW-Filter zuverlässig auslöst, ist anliegender oder durchscheinender Stoff im Prompt. Was durchgeht, ist die Kante, etwa `unbuttoned to the middle, the lace edge of a black bra visible in the open collar`, dazu `fully clothed, nothing bared`.

Ein Teil der Läufe fällt trotzdem in den Filter. Das ist eingepreist und kein Grund, das Register zu senken.

## Detailgrad

Der Detailgrad richtet sich nach der Szene. Ruhige Einzelmotive dürfen minimalistisch sein, mit Atemraum und klaren Formen. Dichte oder belebte Szenen behalten Detailreichtum und räumliche Tiefe und werden nie ins Schematische vereinfacht.

## Prompt-Baustein (englisch, zum Anhängen)

```
Natural editorial photography with realistic skin, believable adult anatomy and
authentic materials, shot in available daylight. Premium editorial aesthetic,
calm composition with room to breathe. Color palette: warm orange and terracotta
accents against desaturated slate blue-grey and charcoal, on off-white and soft
light-grey, with an occasional mustard accent. Soft directional light, gentle
shadows, restrained contrast. Match the level of detail to the scene, keeping
dense or crowded scenes rich in depth and reserving negative space for calm,
single-subject motifs. Show only what the scene describes. Do not add decorative
props, vases, bowls, fruit, dried flowers or potted plants unless they are
explicitly part of the scene. No text anywhere in the image: no lettering,
labels, captions, signage or titles, not even small or blurred ones. No brand
logos, no emblems, no number plates. Full-bleed edge-to-edge composition that
completely fills the frame, no borders, no margins. Not a 3D render, not CGI,
not stylized, no smoothed plastic surfaces, no doll-like faces, no cartoon, no
airbrushed advertising retouch.
```

## Negativliste

Vermeiden: die Renderanmutung mit geglätteten Oberflächen und puppenhaften Gesichtern, Hochglanz-Werbefotografie mit retuschierter Haut, jede Art von Text im Bild, Marken-Embleme und Kennzeichen, dekorative Stillleben-Requisiten, die der Inhalt nicht verlangt, grelle Sättigung, harte Schlagschatten, dunkle oder neon-laute Paletten, Retro- und Vintage-Anmutung, das Studio-Stillleben als Metapher und die Totale, in der ein Gesicht zu klein für die Wiedererkennung wird.

## Infografiken

Braucht ein Inhalt der Belletristik eine beschriftete Grafik, gilt unverändert der Weg aus `henni-default`: eine von Hand geschriebene SVG in der Hauspalette, gerendert über Headless Chrome. Das kommt in dieser Strecke selten vor.
