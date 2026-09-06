---
name: henni-default
description: "Sauberer, halb-realistischer 3D-Render, warme Terrakotta gegen Schiefer-Blaugrau, weiches diffuses Licht, kein Text im Bild."
---

# Bildprofil henni-default

Dieses Profil beschreibt den Hausstil für KI-generierte Bilder. Abgeleitet aus den Referenzbildern des Vaults HenniPKA unter `80 Media/Images/Style/` (Page1 bis Page3). Beim Erzeugen von Bildern den Prompt-Baustein unten an die inhaltliche Beschreibung anhängen, sofern der Auftrag nichts anderes vorgibt.

## Visuelle DNA

Hochwertig, editorial und cinematisch, mit ruhiger, klarer Komposition und etwas Atemraum. Der Look ist ein sauberer, leicht stilisierter 3D-Render mit glatten, veredelten Oberflächen, halb-realistisch und gehoben. Die Wirkung ist die eines hochwertigen CGI-Standbilds oder einer Produktvisualisierung, ausdrücklich kein Foto und kein fotografisches Filmstill. Bei ruhigen Motiven viel Weißraum.

## Farbpalette

- Leitakzent: warmes Orange bis Terrakotta und Koralle.
- Gegenpol: entsättigtes Schiefer-Blaugrau bis Anthrazit (Charcoal).
- Basis: reines Weiß, weiche Hellgrautöne.
- Sparsamer Zweitakzent: Senfgelb, nur als Tupfer.
- Prinzip: ein warmer Akzent gegen einen kühlen Neutralton, oft als warm-kühle Aufteilung der Szene.

## Motiv und Requisiten

Das Bild zeigt genau das, was der Inhalts-Prompt beschreibt, und nicht mehr. Keine dekorativen Stillleben-Requisiten von sich aus ergänzen: keine Vasen, Schalen, Früchte, Trockenblumen oder Zimmerpflanzen, sofern der Inhalt sie nicht ausdrücklich verlangt. Oberflächen und Materialien ergeben sich aus der Szene, nicht aus einem festen Produkt-Setting.

## Beschriftungen

Ein vom Bildmodell erzeugtes Bild trägt **keinen Text**. Keine Schilder, keine Etiketten, keine Achsenbeschriftung, keine Titel, keine Kartennamen. Zwei Gründe. Erstens rendert das Modell Text unzuverlässig, es kommt Krakel oder ein falsches Wort heraus. Zweitens, und das wiegt schwerer: es schreibt in der Sprache des Prompts, und die Prompts sind englisch. Ein englisch beschriftetes Bild in einem deutschen Kapitel ist ein Fremdkörper, auch wenn die Schrift sauber gerendert ist.

Wer eine Beschriftung braucht, hat meist das falsche Motiv gewählt. Die erste Antwort darauf ist die **konkrete Szene**, aus der die Aussage stammt: der Hafen, der Konferenzsaal, die Werkhalle, der Schreibtisch. Sie kommt ohne Beschriftung aus, weil sie etwas zeigt, statt etwas zu benennen.

Nur wo ein Begriff wirklich keine Szene hat, tritt an seine Stelle ein **ikonisches Objekt**, das die Sache selbst zeigt: eine Glühbirne statt des Wortes Elektrizität, ein Serverrack statt des Wortes Rechenzentrum. Der Prompt bekommt dafür ausdrücklich `no text`.

Diese Ersatzregel gilt für den Begriff, der beschriftet werden müsste, nicht für das Bild als Ganzes. Sie ist keine Empfehlung, Szenen durch Gegenstände zu ersetzen. So gelesen entstehen Stillleben aus Seilen, Siegeln und Waagen auf weißem Grund, die stilkonform sind und dem Leser nichts sagen. Ob ein Motiv trägt, entscheidet die Prüffrage des Callout-Skills: Sieht der Leser hier etwas, das er sonst nicht sähe?

Ist die Aussage wirklich eine Datenbeziehung, die ohne Beschriftung nicht lesbar wird (Achsen, Phasennamen, Jahreszahlen), dann ist es kein Szenenbild, sondern eine **Infografik**. Sie entsteht nicht über das Bildmodell, sondern deterministisch als SVG über Headless Chrome, wo der Text exakt und auf Deutsch gesetzt wird. Deutsche Beschriftung gibt es also nur auf diesem Weg, nie aus dem Bildmodell.

## Detailgrad

Der Detailgrad richtet sich nach der Szene. Ruhige, offene oder Einzelmotiv-Bilder dürfen minimalistisch sein, mit viel Weißraum und klaren einfachen Formen, etwa eine Landschaft, ein Stillleben oder ein einzelnes Bauwerk. Dichte, architektonische oder belebte Szenen behalten Detailreichtum und räumliche Tiefe, etwa eine Medina, ein Markt oder ein voller Saal. Eine belebte Szene wird nie ins Schematische oder Flache vereinfacht. Der Minimalismus ist die Ausstattung ruhiger Motive, kein Zwang für jedes Bild.

## Render-Register

Unabhängig vom Motiv bleibt die Anmutung ein sauberer, halb-realistischer 3D-Render mit glatten, veredelten Oberflächen. Auch Menschen, Gesichter und Außenszenen im Tageslicht werden in diesem gerenderten, leicht stilisierten Register gehalten, nicht als fotografisches Filmstill mit hyperrealistischer Haut und Kamera-Optik. Lieber die ruhige, gerenderte Klarheit der Referenzbilder als der Realismus einer Filmproduktion.

## Licht und Komposition

- Weiches, gleichmäßiges, diffuses Licht. Sanfte Schatten, niedriger Kontrast.
- Zentrierte oder nach Drittelregel gesetzte Anordnung, Atemraum nach Bedarf der Szene.
- Aufgeräumter, ruhiger Hintergrund ohne unruhige Ablenkung.
- Formatfüllend: Das Motiv füllt das gesamte Format randlos bis an alle vier Kanten. Keine grauen Ränder, keine Passepartout-Rahmung, kein leerer Hintergrundrand um die Szene. Atemraum entsteht innerhalb der Komposition, nicht als Rand außen herum.

Der Rand ist der häufigste Fehlgriff des Bildmodells, und die allgemeine Fassung dieser Regel reicht nicht. In der Spionageroman-Strecke trugen sechs von zehn nachgebesserten Bildern einen grauen Rahmen, obwohl der Prompt-Baustein `full-bleed edge-to-edge` bereits verlangte. Erst die ausgeschriebene Form mit `no framed picture` und `no passepartout` hat zuverlässig getroffen, deshalb steht sie so im Baustein. Wer den Baustein kürzt, holt den Fehler zurück.

Bei Innenräumen kommt eine zweite Spielart dazu. Das Modell stellt den Raum dann als schwebenden Kubus mit offenen Seiten auf einen leeren Grund, wie ein Puppenhaus im Querschnitt. Dagegen hilft nur die ausdrückliche Angabe, dass die Kamera im Raum steht und Boden, Wände und Decke über alle vier Bildkanten hinauslaufen. Der Satz dafür steht beim Prompt-Baustein.

Ein hochkantes Motiv im 16:9-Rahmen ist derselbe Fehler in anderer Gestalt. Er entsteht meist im Callout selbst: Wer `vertical composition` schreibt, bekommt ein Hochformat, das links und rechts mit Grau aufgefüllt wird. Ein Callout für ein 16:9-Bild verlangt eine `wide composition`.

## Stimmung

Ruhig, hochwertig, zeitgenössisch. Skandinavische Klarheit mit warmem Einschlag. Nicht verspielt, nicht laut, nicht retro.

## Prompt-Baustein (englisch, zum Anhängen)

```
Clean, smooth 3D render look, gently stylized and semi-realistic, with the
polished surface quality of a high-end CGI render or product visualization.
Premium editorial aesthetic. Color palette: warm orange and terracotta accents
against desaturated slate blue-grey and charcoal, on clean white and soft
light-grey, with an occasional mustard accent. Soft even diffuse lighting,
gentle shadows, low contrast, calm mood with a warm touch. Match the level of
detail to the scene. Keep dense, architectural or crowded scenes rich in detail
and depth, reserve generous negative space and clean simple forms for calm, open
or single-subject motifs. Never flatten a busy scene into a schematic or
oversimplified render. Keep people, faces and daylight outdoor scenes in the same
clean rendered, semi-realistic register, not a photograph and not a photographic
film still, no hyper-real skin or textures. Cinematic and volumetric, never a
flat, graphic, comic or illustrated style, and never a miniature or diorama.
Show only what the scene describes. Do not add decorative props, vases, bowls,
fruit, dried flowers or potted plants unless they are explicitly part of the
scene. No text anywhere in the image: no lettering, labels, captions, signage,
axis names or titles, not even small or blurred ones. Let objects carry the
meaning instead of words. Full-bleed edge-to-edge composition that completely
fills the frame from the left edge to the right edge and from top to bottom,
absolutely no borders, no margins, no grey surround, no framed picture, no
passepartout.
```

Bei einem Innenraum kommt dieser Satz dazu, sonst nicht:

```
The camera stands inside the room and the floor, walls and ceiling run out past
all four edges of the picture. This is an ordinary interior seen from within,
not a model, not a doll's house, not an open-sided box, not a room floating on
a background.
```

## Negativliste

Vermeiden: das Studio-Stillleben als Metapher, also ein arrangierter Gegenstand auf weißem Grund, der eine Aussage des Textes bebildert, statt eine Szene zu zeigen (siehe Abschnitt Beschriftungen), jede Art von Text im Bild (Schilder, Etiketten, Achsen, Titel), besonders englische Beschriftungen in deutschen Notizen, fotografischer Filmstill-Look, hyperrealistische Haut und Texturen, schematische oder flache Vereinfachung belebter Szenen, dekorative Stillleben-Requisiten (Vasen, Schalen, Obst, Zimmerpflanzen), die der Inhalt nicht verlangt, grelle Sättigung, harte Schlagschatten, zugestellte oder unaufgeräumte Bildflächen, dunkle oder neon-laute Paletten, Retro- oder Vintage-Anmutung, unruhige Hintergründe, graue Außenränder oder Passepartout-Rahmung um das Motiv, ein Innenraum als schwebender Kubus mit offenen Seiten oder als Puppenhaus im Querschnitt, Modell- und Diorama-Anmutung, ein hochkantes Motiv, das im Breitformat mit Rand aufgefüllt wird.

## Infografik-Tokens

Eine deterministisch erzeugte SVG-Infografik ist die eine bewusste Ausnahme vom 3D-Render-Register. Sie steht als flache, klare, editoriale Grafik mit runden Karten, dünnen Achsen, einfachen Linien-Icons und lesbaren Labels.

Die Palette bleibt dieselbe wie im Bild, hier aber als feste Hex-Werte: Terrakotta `#C2603A`, Schiefer-Blaugrau `#4E6076`, Anthrazit `#2E3640`, warmes Off-White `#F4F2EE` als Grundfläche, weiße Karten, Hellgrau, warmes Orange `#D98E4F`, Senf nur als Tupfer. Kein Grün, kein Türkis, keine fremden Farbtöne.

Text ist hier erwünscht und korrekt, weil die SVG ihn exakt setzt. Achsen, Phasen, Jahre und Titel werden ausgeschrieben, und zwar in der Sprache der Notiz. Titel stehen in einer Serifenschrift (Georgia), Labels serifenlos (Helvetica).
