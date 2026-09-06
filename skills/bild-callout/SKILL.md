---
name: bild-callout
model: opus
description: "In eine Notiz an den passenden Stellen ai-image-Callouts schreiben, mit englischem Szenen-Prompt und deutschem Alt-Text, parametrisiert mit note, style, project und character. Verwenden bei: schreib die Bild-Callouts für X, plane die Bilder für Kapitel Y. Erzeugt keine Bilder, das macht bild-notiz."
---

# Bild-Callouts schreiben

In eine Notiz an den passenden Stellen `> [!ai-image]`-Callouts schreiben. Jeder Callout trägt den englischen Szenen-Prompt und den deutschen Alt-Text des geplanten Bildes. Der volle Bildstil-Block wird nicht eingebettet, er kommt erst bei der Generierung über [[bild]] aus dem aktiven Bildprofil. Dieses Skill erzeugt keine Bilder, es schreibt nur die Callouts. Die Bilder erzeugt anschließend [[bild-notiz]].

## Wann dieser Skill greift

Trigger sind Anfragen wie:

- "Schreib die AI-Image-Callouts für die Notiz X"
- "Setze die Bildprompts in Kapitel Y"
- "Plane die Bilder für die ganze Publication Z"
- "Schreib die HenniBock-Callouts für die Notiz X"

Für HenniBock-Inhalte gilt derselbe Skill mit gesetztem `project`, siehe Parameter. Eine eigene HenniBock-Variante gibt es nicht.

Der Skill ist nicht auf Kapitel und Publications beschränkt. Er arbeitet auf jeder Prosa-Notiz mit H2-Gliederung. Bei einer ganzen Publication die Kapitel-Wikilinks aus dem Inhaltsverzeichnis sammeln und der Reihe nach abarbeiten.

## Vor der Ausführung lesen

1. Das aktive Bildprofil frisch auflösen, für Palette, Detailgrad-Regel, Requisiten-Sperre und Negativliste:

   ```bash
   hk-kontext --bild
   ```
2. Bei einer getypten Notiz ihre Typdefinition unter `<config_base>/Typedefs/` für die Konvention des Body und der Callouts. Die Bereiche nennt `hk-ablage --bereiche`.

## Parameter

- **note** ist die zu bearbeitende Notiz. Pflichtparameter. In der Regel ein Text unter `output_base`, der Skill arbeitet aber auf jeder Prosa-Notiz mit H2-Gliederung.
- **style** ist die ID des Bildprofils, das die Formulierung der Prompts steuert. Vorgabe ist das Profil, das die Wurzeldatei unter `image_style` nennt. Aus ihm kommen Palette, Detailgrad-Regel, Requisiten-Sperre und Negativliste. Den Stil immer frisch auflösen, nie aus dem Gedächtnis zitieren. Er wird nicht in den Callout eingebettet, er lenkt nur die Wortwahl. Eine abweichende Profil-ID kann übergeben werden, dann tritt sie an die Stelle des Defaults.
- **project** ist das Magnific-Projekt, das als Metadatenzeile in jeden Callout gestempelt wird. Optional, Vorgabe leer. Leer heißt kein Projekt-Feld. Für alles, was auf HenniBock erscheint, `Hennibock` setzen. [[bild-notiz]] liest die Zeile aus und reicht sie an [[bild]] weiter.
- **character** ist der Magnific-Library-Character für wiederkehrende Figuren. Optional, Default leer. Anders als `project` wird er nicht in jeden Callout gestempelt, sondern nur in die, deren Szene die Figur tatsächlich zeigt, siehe Schritt 6. Bei HenniBock-Reportagen ist der übliche Wert `hennireporter`.

## Ablauf

1. **Notiz öffnen.** Die Notiz `note` lesen, ihre Prosa und H2-Sektionen erfassen, die Länge abschätzen.

2. **Bildprofil auflösen.** Das Profil aus `style` frisch auflösen, siehe oben. Palette, Detailgrad-Regel, Requisiten-Sperre und Negativliste steuern jede Formulierung.

3. **Bildstellen bestimmen.** Über die ganze Notiz verteilen, nicht in der ersten Hälfte häufen. Richtwert ist **ein Bild je H2-Sektion**, keine starre Obergrenze nach oben. Auch die zweite Hälfte und der Schluss brauchen Bilder. Pro Stelle den passenden Beat wählen:
   - oberes Drittel (Aufmacher, Schauplatz),
   - Mitte (Schlüsselfigur, Wendepunkt),
   - unteres Drittel (Karte, Übersicht),
   - dramaturgische Spitzen und ein Schlussbild nicht vergessen.

   Der Richtwert ist eine Untergrenze, kein erreichtes Ziel. Ein grüner Audit ist kein Grund aufzuhören, solange Sektionen ohne Bild bleiben.

4. **Bestehende Callouts.** Einen schon vorhandenen `> [!ai-image]`-Callout unverändert stehen lassen und den neuen, stil-bewussten Callout direkt darunter schreiben. An Stellen ohne Bild neue Callouts ergänzen.

5. **Callout formulieren.** Form `> [!ai-image]` und darunter eine Zeile `> ` mit einem englischen Prompt-Absatz, also Szene, Personen oder Objekte, Lichtstimmung und Bildaufbau. Stil-bewusst, aber ohne den vollen Stil-Block:
   - **Ein Bild zeigt etwas, es illustriert keine These.** Das ist die erste Frage an jeden Callout: Sieht der Leser hier etwas, das er sonst nicht sähe? Einen Ort, eine Handlung, eine Figur, einen Gegenstand ihrer Zeit. Ein Bild soll den Text ergänzen, nicht bebildert wiederholen, was der Absatz daneben schon sagt.

     Der typische Fehlgriff ist das **Studio-Stillleben als Metapher**: zwei Seile mit unterschiedlich festen Knoten für ein festes und ein loses Bündnis, zwölf Siegel und eins abseits für eine Abstimmung, ein Magnet mit Eisenspänen für Druck, der zusammenschweißt. Solche Bilder sind hübsch, hausstilkonform und tragen keinerlei Information. Sie erklären nichts, sie schmücken eine Aussage, die im Text ohnehin steht, und ein Leser lernt aus ihnen nichts über Tanger, Algeciras oder das Jahr 1905.

     Stattdessen konkret werden. Zum selben Absatz gehört die Szene, aus der die Aussage stammt: der Hafen mit der ankernden Jacht, die Gasse mit dem Empfangskomitee, der Konferenzsaal mit den Delegationen, das Kabinettszimmer, der Schreibtisch des Geheimrats, das Kanonenboot vor der Küste. Personen dürfen vorkommen, angeschnitten und ohne erkennbare Gesichter, wie es der Hausstil ohnehin verlangt.

     Eine Metapher bleibt zulässig, wo die Aussage selbst keine Szene hat, etwa bei einem reinen Struktur- oder Systemgedanken. Sie ist dann die Ausnahme und nicht der Normalfall, und sie sollte im Kapitel einzeln bleiben. Der Audit in `hk-kapitel` meldet den Befund `callouts-zu-abstrakt`, wenn ein Callout die Studio-Signatur trägt (Gegenstand auf weißem Grund, Blick von oben) und dabei weder Menschen noch einen Ort nennt.
   - **Keine widersprechenden Stilworte** wie "oil painting", "painterly", "illustration", "sepia" oder "cartographic". Der Stil kommt aus dem Bildprofil.
   - **Detailgrad nach Szenendichte.** Dichte oder volle Szenen detailreich, ruhige oder offene Motive minimalistisch mit Atemraum.
   - **Palette nur andeuten**, wo die Szene es hergibt, warmes Orange oder Terrakotta gegen kühles Schiefer-Blaugrau.
   - **Keine Deko-Requisiten** erfinden, die der Inhalt nicht verlangt.
   - **Diagramme und Datenvisualisierungen niemals auf Text-Beschriftungen bauen.** Text in KI-generierten Bildern ist unzuverlässig und oft unleserlich oder falsch. Zwei zugelassene Alternativen: (a) **Ikonische Objekte** - jedes Element durch ein eindeutiges Bildobjekt identifizieren, das die Periode, Kategorie oder Aussage selbst symbolisiert, z.B. fünf Wirtschaftswellen mit Dampfmaschine, Lokomotive, Glühbirne, Automobil und Serverrack an den Gipfeln statt Textetiketten. (b) **Physisches Dokument** - das Diagramm als greifbares Objekt darstellen, z.B. als grossformatigen Ausdruck auf einem Tisch, Kreide-Zeichnung an einer Tafel oder aufgerolltes Papier mit Gewichten, so dass das Dokument selbst das Motiv ist und Lesbarkeit nicht voraussetzt. Abstrakte Kurven auf einer Wand oder einem Bildschirm ohne Kontext immer meiden.
   - **Chart-artige Begriffe als echtes Chart auf einem physischen Dokument zeigen, nie als Naturmetapher.** Wenn der Inhalt selbst eine Datenbeziehung ist (Überlagerung mehrerer Wellen, verschiedene Frequenzen oder Dauern, Summenkurve, Phasenkurve), das Diagramm konkret auf Tafel, Millimeterpapier oder Ausdruck zeichnen lassen, mit den Kurven als Bildgegenstand. Naturmetaphern dafür scheitern, das Modell rendert "vier überlagerte Sinuswellen auf dem Meer" als bedeutungslose Düne oder Bergtextur. Die Metapher darf die Aussage illustrieren, aber sie nicht ersetzen, wo die Aussage selbst die Kurvenform ist.
   - **Symmetrische und wiederholende Layouts vermeiden, sie erzeugen Duplikat-Artefakte.** Konzentrische Ringe, gespiegelte Querschnitte oder gerasterte Wiederholungen verleiten das Modell zu doppelten Hälften, Naht in der Bildmitte oder verdoppelten Elementen (zwei Loks, zwei Schächte). Eine einzige, durchgehende, asymmetrische Komposition verlangen und im Prompt ausdrücklich "one continuous, not mirrored, not repeated, no seam down the middle" o.ä. setzen.
   - **Ein Callout mit `character` sichert die Personenzahl zu.** Zeigt die Szene eine wiederkehrende Figur, gibt [[bild-notiz]] in Schritt 5a ein Referenzbild der Person mit, und bei einer Personenreferenz neigt das Modell zur Verdopplung. Der Prompt trägt deshalb ausdrücklich `exactly one woman in the image, no duplicate, no twin`, sinngemäß angepasst an die Figur. Die Zusicherung gehört in den Prompt und nicht in den Aufruf: der Callout ist die Bestellung, und was nicht in ihm steht, ist beim nächsten Lauf weg. Aus demselben Grund nennt der Prompt das Aussehen der Figur in einem knappen Einschub (Haar, Statur, ein Erkennungsmerkmal), damit er auch ohne Referenz noch dieselbe Person bestellt.
   - **Zahl der unterscheidbaren Einzelelemente klein halten.** Viele verschiedene beschriftete Teilmotive in einem Bild führen zu Unordnung. Lieber wenige, klar getrennt positionierte Elemente, jedes mit eigenem Platz.
   - **Abstrakte Monolithe und Reliefskulpturen für Abfolgen und Vergleiche meiden, sie werden bedeutungslos.** "Drei Säulen mit je einer Kurve", "Zeitstrahl als Relief mit Klippe" und ähnliche reine Daten-Skulpturen rendern als nichtssagende Blöcke, weil die Aussage (Abfolge, Vollständigkeit, offenes Ende) in der Form untergeht. Das bewährte Mittel ist stattdessen das ikonische-Objekt-auf-Welle-Motiv: eine durchgehende Wellenlinie mit je einem eindeutigen Objekt am Gipfel jeder Welle (Glühbirne, Computer, Serverrack), die letzte Welle bei einem offenen Ausgang nur angerissen und mit einem einzelnen leuchtenden Fragezeichen markiert. Es ist legibel, hausstilkonform und mehrfach erprobt.
   - **Diagramm- und Konzeptbilder hell und sauber halten, keine düstere Low-Key-Stimmung.** Auch Szenen, die Infrastruktur oder Aufbau zeigen (Rechenzentrum, Baustelle), im hellen, klaren Hausstil mit der Warm-Kühl-Palette rendern, nicht in dunklem Dämmerlicht mit matschigen Formen. Dunkle, kontrastarme Renders verschlucken die Bildaussage und brechen mit dem Stil der übrigen Bilder. Keine bedeutungslosen Schwung-Elemente (frei geschwungene Kabelbündel, Nebel) in den Vordergrund setzen.

6. **Metadaten stempeln.** Die Metadatenzeilen stehen direkt unter `> [!ai-image]`, danach trennt eine leere `>`-Zeile sie vom Prompt-Absatz. Der Prompt selbst bleibt reiner Szenen-Prompt und trägt keinen Alt-, Projekt- oder Character-Text.

   Zulässig sind genau drei Schlüssel: `alt`, `project` und `character`. Jede andere Zeile ist ein Fehler und bricht den Publish-Lauf ab. Das ist Absicht, denn ein Tippfehler wie `alr:` würde sonst still zum Prompt gerechnet, und der Alt-Text wäre spurlos weg.

   `alt` ist Pflicht in jedem neu geschriebenen Callout, dazu unten Schritt 6a. `project` kommt in jeden geschriebenen Callout. `character` nur in die, deren Szene die Figur wirklich zeigt. Sach-, Szenen- und Landschaftsbilder bekommen kein `character`-Feld, sonst zwingt Magnific eine Person ins Bild. Ein Sachkapitel bekommt in der Regel gar keins, die Reporterin hat dort nichts zu suchen.

   ```
   > [!ai-image]
   > alt: "Eine Reporterin mit Mikrofon auf einer belebten Straße."
   > project: Hennibock
   > character: hennireporter
   >
   > A reporter with a microphone on a busy street, warm daylight, editorial look.
   ```

   Ohne Personen-Bezug entfällt die character-Zeile:

   ```
   > [!ai-image]
   > alt: "Eine Küstenstadt im ersten Morgenlicht."
   > project: Hennibock
   >
   > A quiet coastal town at dawn, soft warm light over rooftops.
   ```

   Sind `project` und `character` leer, bleibt der Kopf aus der `alt`-Zeile allein. Ein Callout ganz ohne Kopf gibt es nur noch im Altbestand.

6a. **Alt-Text schreiben.** Der Alt-Text entsteht im selben redaktionellen Schritt wie der Prompt, denn beide beschreiben dasselbe Bild. Er ist zunächst die Beschreibung des beabsichtigten Bildes, [[bild-notiz]] gleicht ihn später gegen das erzeugte Bild ab.

   - Deutsch, ein knapper vollständiger Satz.
   - Er beschreibt die erkennbare Szene, bei einer Infografik die dargestellte Beziehung.
   - Er wiederholt weder Kapitelüberschrift noch Bildtitel und beginnt nicht mit "Bild von" oder "Abbildung zeigt".
   - Dekorative Einzelheiten, Farben und Stilbegriffe bleiben weg, sofern sie für die Aussage nicht nötig sind. Der Alt-Text ist keine Kurzfassung des Stil-Blocks.
   - Er behauptet nichts, was nicht im geplanten Motiv steckt. Wer die Person auf dem Bild nicht benennen kann, benennt sie nicht.

   Der Wert steht in ASCII-Doppelquotes und folgt den Schreibregeln wie jede Prosa: nur ASCII-Bindestriche, keine Halbgeviert- oder Geviertstriche, keine Strichpunkte, keine typografischen Anführungszeichen, echte Umlaute statt Ersatzformen.

   Der Schreibregel-Hook nimmt einem diese Prüfung nicht ab. Er springt bei jedem `Edit` an, überspringt aber Blockquotes und damit den ganzen Callout, weil dort der englische Prompt steht. Ein von Hand gesetzter Alt-Text ist deshalb ungeprüft und wird selbst gegengelesen. Der Grund: Der Prompt steht auf Englisch im selben Blockquote, und eine Prüfung, die ihn mitläse, meldete jeden englischen Satz.

7. **Platzierung.** Den Callout direkt nach dem passenden Prosa-Absatz oder am Ende der Sektion setzen, mit einer Leerzeile davor und danach. Nicht in die Verbindungen-Sektion, nicht in eine Wikilink-Zeile.

8. **Schreibregeln.** Der englische Callout-Text steht als Prosa in der Datei und wird vom Hook geprüft. Keine Em-Dashes, keine En-Dashes, keine Strichpunkte, nur ASCII-Bindestrich, Komma oder Punkt. Vor dem Abschluss `grep -nE "—|–|;"` auf die Notiz, ohne Treffer.

## Infografiken und Datendiagramme (eigener Bildtyp)

Manche Inhalte sind echte Datendiagramme, kein Szenenbild: ein Hype-Zyklus, ein Phasenvergleich über mehrere Epochen, eine beschriftete Mehr-Panel-Karte, Kurven mit Achsen. Hier tragen die Beschriftungen (Achsen, Phasennamen, Jahreszahlen, Titel) die Aussage. Das Bildmodell nano-banana rendert Text unzuverlässig, deshalb scheitern solche Diagramme als Foto-Prompt, und das Ikonen-Behelfsbild bleibt blass. Der zuverlässige Weg ist deterministisch, nicht generativ: eine von Hand geschriebene SVG, gerendert über Headless Chrome.

- **Register**: flache, klare, editoriale Infografik. Das ist die eine bewusste Ausnahme vom 3D-Render-Bildstil. Runde Karten, dünne Achsen, einfache Linien-Icons, lesbare Labels.
- **Palette strikt aus dem Hausstil, als Hex fest**: Terrakotta `#C2603A`, Schiefer-Blaugrau `#4E6076`, Anthrazit `#2E3640`, warmes Off-White `#F4F2EE`, weisse Karten, Hellgrau, warmes Orange `#D98E4F`, Senf nur als Tupfer. Kein Grün, kein Türkis, keine fremden Farbtöne. Die grüne KI-Spalte eines Altbilds war genau der Fehler.
- **Text ist hier erwünscht und korrekt**, weil die SVG ihn exakt setzt. Achsen, Phasen, Jahre und Titel ausschreiben. Serif (Georgia) für Titel, Sans (Helvetica) für Labels passt zum Hausstil.
- **Erzeugung**: SVG mit `viewBox="0 0 1456 819"` (16:9) schreiben, Hintergrundrechteck in `#F4F2EE`. Rendern und konvertieren:
  ```
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
    --hide-scrollbars --force-device-scale-factor=2 --window-size=1456,819 \
    --screenshot=/tmp/x.png /tmp/x.html
  sips -s format jpeg /tmp/x.png --resampleWidth 1456 --out "<Zielpfad>.jpg" --setProperty formatOptions 92
  ```
  Die SVG-Quelle als Beleg aufheben, damit das Diagramm reproduzierbar und nachbesserbar bleibt.
- **Einbetten** wie jedes Bild, pfadbasiert direkt vor dem Callout.

Faustregel: Szene zu 3D-Render-Bildstil über das Bildmodell, ohne Text. Echtes Datendiagramm mit Beschriftung zu SVG-Infografik über Chrome. Das Ikonen-auf-Welle-Motiv bleibt der Mittelweg für einfache Abfolgen, die ohne Beschriftung auskommen.

## Ergebnis

Die Notiz trägt an den passenden Stellen hausstilkonforme `> [!ai-image]`-Callouts. Bestehende alte Callouts bleiben darüber stehen. Die Prompts sind ohne Umschreibung an [[bild]] übergebbar, das den Stil-Block anhängt. In der Regel folgt als nächster Schritt [[bild-notiz]].

## Selbstcheck

- Je geplanter Stelle ein neuer `> [!ai-image]`-Callout, ein etwaiger alter steht unverändert darüber.
- Der neue Callout enthält keine widersprechenden Stilworte und keinen eingebetteten Stil-Block.
- Detailgrad passt zur Szenendichte.
- Jeder neue Callout trägt eine nicht-leere `> alt:`-Zeile mit einem deutschen Satz, der die Szene beschreibt und nicht den Stil.
- Bei gesetztem `project`: jeder neue Callout trägt die `> project:`-Zeile.
- Bei gesetztem `character`: die `> character:`-Zeile steht nur in Callouts, deren Szene die Figur zeigt, und nirgends sonst. Deren Prompt sichert die Personenzahl zu und nennt das Aussehen der Figur knapp.
- Eine leere `>`-Zeile trennt die Metadaten vom Prompt, und der Prompt-Absatz nennt weder Alt-Text noch Projekt noch Character.
- Keine Metadatenzeile außer `alt`, `project` und `character`.
- `grep -nE "—|–|;"` ohne Treffer.
- Bei einer ganzen Publication ist jedes Kapitel des Inhaltsverzeichnisses abgearbeitet.

## Modellwahl

Anders als die reinen Bildgenerierungs-Skills trifft dieser Skill kreative und redaktionelle Entscheidungen. Er verteilt Bildstellen über die ganze Notiz, wählt je Stelle den passenden Beat, formuliert stil-bewusste Szenen-Prompts, die den Hausstil treffen, ohne ihm zu widersprechen, und hält dabei die Schreibregeln ein. Deshalb läuft er auf einem starken Tier, im Frontmatter als `model: opus` gesetzt. Hier gilt die umgekehrte Empfehlung wie bei [[bild]] und [[bild-notiz]], die als mechanische Skills ein günstiges Tier vertragen.

## Nicht tun

- Keine Bilder erzeugen. Das übernimmt [[bild-notiz]].
- Den vollen Stil-Block nicht in den Callout einbetten, er kommt erst bei der Generierung.
- Kein `character`-Feld in Sach- oder Landschaftsbildern, sonst zwingt Magnific eine Person ins Bild.

## Abgrenzung

- [[bild-notiz]] erzeugt die Bilder für die vorhandenen Callouts und bettet sie ein.
- [[bild]] erzeugt aus einem Callout-Prompt ein einzelnes Bild und hängt den Stil-Block an.
- Eine eigene HenniBock-Variante gibt es nicht mehr. Wer HenniBock-Callouts will, ruft diesen Skill mit `project=Hennibock` auf, bei Reportagen mit Reporterin zusätzlich `character=hennireporter`.

## Verbindungen

- [[bild-notiz]] als nachfolgender Generierungsschritt
- [[bild]] als zugrunde liegender Bildmotor
- `hk-kontext --bild` als Quelle des Bildprofils
