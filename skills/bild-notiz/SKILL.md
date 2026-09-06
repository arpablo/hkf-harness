---
name: bild-notiz
model: sonnet
description: "Für alle ai-image-Callouts einer Notiz die Bilder erzeugen, notiz-eigen ablegen und einbetten. Verwenden bei: erzeuge die Bilder für Notiz X, bebildere Kapitel Y. Setzt vorhandene Callouts voraus, die zuvor bild-callout schreibt."
---

# Die Bilder einer Notiz erzeugen

Für eine Notiz alle bereits vorhandenen `> [!ai-image]`-Callouts in Bilder umsetzen. Für jeden Callout erzeugt der Skill ein Bild über [[bild]] und legt es in einem notiz-eigenen Ordner ab, dann setzt er einen pfadbasierten Embed direkt vor den Callout. Die Callouts schreibt zuvor [[bild-callout]], dieser Skill setzt sie nur um. Zusammen ersetzen die beiden den früheren `illustrate-chapter`, der Schreiben und Generieren in einem Durchgang machte, hier aber sauber getrennt und komposabel.

## Wann dieser Skill greift

Trigger sind Anfragen wie:

- "Erzeuge die Bilder für die Notiz X"
- "Bebildere das Kapitel Y"
- "Setze die Bilder zu den Callouts in Z um"

## Voraussetzung

Der Skill baut auf [[bild]] auf und braucht damit dasselbe: ein verbundenes Magnific MCP. Fehlt es, bricht der Skill ab und meldet es dem Nutzer. Außerdem muss die Notiz mindestens einen `> [!ai-image]`-Callout enthalten, sonst gibt es nichts zu erzeugen.

## Parameter

- **note** ist die zu prozessierende Notiz. Pflichtparameter. Eine Prosa-Notiz mit einem oder mehreren `> [!ai-image]`-Callouts.
- **style** ist die ID des zu verwendenden Bildprofils. Optional, Vorgabe ist das Profil, das die Wurzeldatei unter `image_style` nennt. Der Wert geht unverändert an [[bild]] weiter, das Auflösen macht dieser Skill nicht selbst.

  Eine Ablage mit einheitlichem Bestand setzt ihr Profil in der Wurzeldatei und braucht hier keinen Parameter. Eine mit gemischtem Bestand setzt das häufigere als Vorgabe und übergibt für den selteneren Fall `style`.

  Ein Profil für erzählende Bilder mit wiederkehrender Figur arbeitet fotografisch statt gerendert, weil ein 3D-Render die Wiedererkennbarkeit der Figur zerstört.
- **aspect-ratio** ist das Seitenverhältnis der Bilder. Optional, Default `16:9`. Wird an [[bild]] weitergereicht. Das Ausgabeformat ist fest JPG.
- **project** und **character** sind keine skill-weiten Parameter, sondern stammen je Callout aus dessen Metadatenzeilen (`> project:` und `> character:`, wie sie [[bild-callout]] bei gesetzten gleichnamigen Parametern stempelt). Sie werden pro Callout ausgelesen und an [[bild]] durchgereicht. Fehlen sie im Callout, wird der jeweilige Parameter weggelassen und der Default von [[bild]] greift.
- **reference** ist der Pfad eines Referenzbildes, das für alle Callouts dieses Laufs gilt. Optional. Ohne Angabe wählt der Skill die Referenz je Callout selbst, siehe Schritt 5a. Ein gesetzter Wert schlägt die automatische Wahl und wird unverändert an [[bild]] weitergereicht.

## Ablauf

1. **Notiz lesen.** Die Notiz `note` öffnen. Im Frontmatter den Typ aus dem Feld `type` lesen und etwaige Wikilink-Klammern entfernen, aus einem Verweis auf die Typseite wird also der Typname. Den Dateinamen der Notiz ohne Endung als Namen der Notiz merken.

2. **Präfix aus dem Namen strippen.** Trägt der Dateiname ein Typ-Präfix vor einem ` - `, etwa `Kap - ` oder `Text - `, fällt es für den Ordnernamen weg. So bleibt der Zielordner beim Titel und ändert sich nicht, wenn ein Vault sein Präfix ändert. 

3. **Callouts finden.** Alle `> [!ai-image]`-Callouts der Reihe nach finden und je den englischen Prompt-Absatz darunter auslesen. Trägt ein Callout am Kopf Metadatenzeilen der Form `> key: value` (erlaubte Keys `alt`, `project` und `character`, gesetzt von [[bild-callout]]), diese je Callout mit auslesen. Der Prompt ist dann der Absatz nach der leeren `>`-Trennzeile. Fehlen die Metadatenzeilen, ist der Callout feldlos und der ganze `>`-Text ist der Prompt, das kommt nur noch im Altbestand vor. Eine Metadatenzeile mit einem anderen Schlüssel ist ein Fehler und wird gemeldet, nicht stillschweigend zum Prompt gerechnet.

4. **Zielordner bestimmen.** `<media_base>/Images/<Typ der Notiz>/<Name der Notiz>/`, mit dem in Schritt 2 angepassten Namen. Die Bereiche nennt `hk-ablage --bereiche`. Den Ordner mit `mkdir -p` anlegen, falls er fehlt. Den Ordner immer zuerst anlegen, damit `sips` keine Artefaktdateien erzeugt.

5. **Bildnamen ableiten.** Je Callout einen sprechenden Bildnamen aus dem Prompt bilden: kurz und beschreibend, aus dem Kern der Szene, echte Umlaute, ASCII-Bindestrich als einziges Strichzeichen. Innerhalb eines Laufs eindeutig halten, bei Kollision ein Suffix anhängen.

5a. **Referenzbild wählen.** Trägt ein Callout ein `character`-Feld, zeigt sein Bild eine wiederkehrende Figur, und dann braucht es eine Bildreferenz. Die Character-Referenz des Dienstes allein genügt nicht, sie beschreibt einen groben Typ und trifft die Figur nicht.

   **Wo die Vorlagen liegen und welche wann gilt, sagt die Ablage.** Das steht in einer `hint`-Notiz, die der Sitzungskontext mitbringt. Ein Ordnername in diesem Skilltext gälte für eine Ablage und bräche in der nächsten.

   Was allgemein gilt:

   - **Den Ordner vor der Wahl auflisten, statt aus dem Gedächtnis zu greifen.** Neue Vorlagen kommen dazu, sobald ein Lauf eine Lage nicht getroffen hat, und die Dateinamen benennen die Szene.
   - **Setzt der Prompt die Figur in eine neue Umgebung, gewinnt die freigestellte Vorlage** vor weißem Grund. Spielt die Szene dort, wo ein fertiges Szenenbild aufgenommen ist, liefert dieses zusätzlich Licht, Outfit und Haltung und ist dann besser.
   - **Erste Frage an jede Szene: trägt die Figur ihre üblichen Erkennungsmerkmale?** Nimmt der Text ihr eines ab, etwa eine Brille, taugt keine Vorlage mit diesem Merkmal, denn was darunter liegt, kennt das Modell nicht und erfindet es.
   - **Callouts ohne `character` bekommen keine Referenz.** Ein Sach-, Szenen- oder Landschaftsbild zeigt keine Person, und eine Personenreferenz zwingt sonst eine Figur ins Bild.
   - **Die Grenze verläuft an der Erkennbarkeit, nicht am Bildtyp.** Trägt ein als Sachbild geplantes Motiv eine Spiegelung, einen Schatten oder eine angeschnittene Figur, die der Leser als die Figur lesen soll, dann ist es ein Personenbild und braucht `character` und Referenz. Ein Schaufensterbild ohne Referenz hat am 30.07.2026 genau daran eine fremde Frau erzeugt.

5b. **Den Stilblock bei Personenbildern weglassen.** Bei einem Bild mit erkennbarer Figur hängt [[bild]] den Prompt-Baustein des Bildprofils nicht an. Der Baustein verlangt `gently stylized`, `not a photograph` und `no hyper-real skin`, und das stilisiert das Gesicht so weit weg, dass die Referenz nicht mehr durchkommt.

   Stattdessen endet der Prompt mit `Believable adult anatomy, realistic skin and materials, natural daylight, no cartoon, no toy or mascot look`. Palette und Lichtführung bleiben im Prompt selbst stehen, also warmes Terrakotta gegen kühles Schiefer-Blaugrau, damit das Bild zur Reihe passt.

   Dazu zwei Angaben, ohne die die Ähnlichkeit auch mit Referenz scheitert. Der Ausschnitt wird gesteuert, bewährt ist `medium editorial composition, the woman framed from the waist up and filling a large part of the frame, her face clearly readable`. Eine Totale mit ganzer Figur trifft nie.

   **Das Gesicht steht nie unscharf im Hintergrund.** Das Modell wendet die Vorlage nur auf scharfe Gesichtspixel an, sonst erfindet es ein Gesicht, und die Referenz im Aufruf ändert daran nichts. Bei einem Motiv, dessen Gegenstand ein Detail ist, etwa eine Hand auf einem Gegenstand, gibt es deshalb zwei zulässige Fassungen. Entweder liegen Detail und Gesicht beide im Fokus, dann steht die Figur halbnah dahinter und der Prompt sagt `her face clearly readable and in sharp focus`. Oder im Bild ist gar keine Person zu sehen, dann trägt es nur Hand und Gegenstand. Ein weichgezeichnetes Gesicht im Hintergrund scheitert verlässlich. Wie die Figur aussieht und mit welchen englischen Wendungen der Prompt sie bestellt, sagt die `hint`-Notiz der Ablage.

   Sach-, Szenen- und Landschaftsbilder folgen dem Bildprofil unverändert. 

   Die Vorlage liefert Gesicht, Haar und Statur, die Szene bestimmt weiter der Prompt. Deshalb bleibt `reference-type` auf dem Default `image`. Trägt der Callout-Prompt keine Zusicherung wie `exactly one woman, no duplicate`, neigt das Modell bei einer Personenreferenz zur Verdopplung, siehe [[bild]], Abschnitt Bekannte Fallstricke bei Referenzbildern.

6. **Je Callout einen Subagenten `bebildern` starten.** Alle Aufrufe stehen in einer Nachricht, damit sie nebeneinander laufen. Bei mehr als acht Callouts in Wellen von acht arbeiten.

   Der Auftrag je Agent nennt sechs Werte. `prompt` ist der Callout-Prompt aus Schritt 3, unverändert und vollständig. `alt` ist das vorhandene Alt-Feld des Callouts. `target-folder` ist der Ordner aus Schritt 4, `name` der Bildname aus Schritt 5, dazu `style` und `aspect-ratio` dieses Skills.

   Trägt der Callout ein `project` oder `character`, gehen sie mit, sonst bleiben sie weg. Die Referenz aus Schritt 5a geht als `reference` mit, falls dort eine bestimmt wurde.

   **Der Agent erzeugt, sieht an und legt ab. Er fasst die Notiz nicht an.** Das Einbetten in Schritt 8 und das Setzen des Alt-Texts in Schritt 7 macht dieser Skill, nachdem alle Agenten zurück sind. Zwei gleichzeitige Edits auf dieselbe Notiz überschreiben einander, und genau deshalb liegt die Grenze hier.

   Der Grund für die Delegation ist der Kontext. Ein Personenbild läuft mit drei bis vier Varianten, die jemand ansehen muss, und bei zwölf Callouts sind das bis zu achtundvierzig Bilder plus die Referenzvorlagen. Im Hauptkontext bleiben sie für den Rest der Sitzung liegen. Der Agent gibt einen Pfad und zwei Sätze zurück.

   Meldet die Sitzung den Agententyp als unbekannt, ist die Definition seit dem Sitzungsstart neu. Dann `general-purpose` nehmen und als Prompt geben: "Lies die Agentendefinition bebildern des hkf-Plugins und befolge sie exakt, den Frontmatter-Block ignorierst du", gefolgt von den Parametern.

   **Personenbilder laufen mit `count` 3 bis 4, nie mit 1.** Dieselbe Referenz trifft mal und mal nicht, ein einzelner Lauf ist ein Münzwurf. Der Agent erkennt den Fall am gesetzten `character` und wählt die Variante nach Gesichtsform, Wangenknochen, Haarlänge und Haarstruktur. Drei zusätzliche Varianten kosten weniger als eine Rückmeldung, dass die Person auf dem Bild nicht die Figur ist. Für Sach- und Szenenbilder ohne Person genügt ein Lauf. 

   **Ausnahme Infografik-Callouts.** Ist ein Callout ein echtes Datendiagramm mit nötiger Beschriftung (Hype-Zyklus, Phasenvergleich, beschriftete Achsen oder Mehr-Panel-Karte), dann nicht das Bildmodell verwenden, weil nano-banana Text verstümmelt. Stattdessen den deterministischen Weg aus [[bild-callout]], Abschnitt Infografiken und Datendiagramme: eine SVG in der Hauspalette (feste Hex) von Hand schreiben, über Headless Chrome rendern und mit `sips` nach JPG wandeln, dann am selben Zielpfad ablegen. SVG-Quelle aufheben. Der Embed in Schritt 8 ist identisch. Für diesen Callout wird kein Agent gestartet, es entsteht kein Bild über das Modell.

6a. **Lenkrad links prüfen.** Diesen Durchgang macht der Agent, hier steht die Regel, gegen die er prüft. Zeigt ein erzeugtes Bild einen Fahrzeuginnenraum, wird vor der Ablage geprüft, auf welcher Seite das Lenkrad sitzt. Jedes Fahrzeug des Vaults ist ein Linkslenker: Lenkrad vor der Fahrerin, Fahrertür an ihrer linken Schulter, Mittelkonsole und Beifahrersitz rechts von ihr.

   Sitzt es falsch, wird nicht neu generiert, sondern das Ergebnis horizontal gespiegelt, `sips --flip horizontal <bild> --out <ziel>`. Das Modell setzt diese Szene auch bei ausdrücklicher Anweisung überwiegend als Rechtslenker, weitere Läufe kosten nur Zeit. Das Spiegeln dreht den Innenraum vollständig und lässt Rechtsverkehr und Fahrbahnmarkierung stimmig. Vorher prüfen, ob lesbare Schrift oder ein Kennzeichen im Bild steht, weil beides beim Spiegeln unlesbar wird. 

6b. **Bedrucktes Papier flach anschneiden.** Zeigt ein Motiv Papier, ein Schild oder einen Bildschirm frontal und scharf, setzt das Modell lesbaren Buchstabensalat darauf, obwohl der Stilblock jeden Text verbietet. Das Verbot am Ende des Prompts reicht dafür nicht. Die bedruckte Fläche kommt in einen flachen Blickwinkel, `the printed page is seen at a shallow grazing angle, so that any lettering on it stays illegible`, und das Verbot steht zusätzlich hart im Motivteil, `Absolutely no readable writing anywhere, no headline, no words, no letters, no numbers`. 

7. **Alt-Texte setzen.** Den Abgleich hat der Agent gemacht, er hat das Bild gesehen und dieser Skill nicht. Meldet seine Rückgabe eine berichtigte Fassung, wird sie in das `alt`-Feld des zugehörigen Callouts geschrieben. Meldet er `unverändert`, bleibt das Feld stehen. Nur das `alt`-Feld anfassen, Prompt, Projekt und Character bleiben unberührt.

   Ein Bild ungesehen zu übernehmen ist hier kein Mangel, sondern der Zweck: Der Agent hat es angesehen, damit dieser Kontext es nicht muss. Was ihm auffiel, steht in seinen Befunden und geht in die Antwort.

   Trägt ein Callout aus dem Altbestand gar kein `alt`-Feld, eines nach den Regeln aus [[bild-callout]], Schritt 6a, ergänzen. Das ist der Weg, auf dem der Bestand nachwächst, ohne dass jemand 1372 Callouts von Hand umschreibt.

8. **Einbetten.** Den erzeugten Pfad als Vault-Embed direkt vor den zugehörigen Callout setzen, pfadbasiert `![[<media_base>/Images/<Typ der Notiz>/<Name der Notiz>/<Bildname>.jpg]]`, mit einer Leerzeile davor und danach. Pfadbasiert, weil die kurzen Bildnamen sich sonst vault-weit überschneiden könnten. Bei einem erneuten Lauf denselben Bildnamen verwenden und die Datei am gleichen Pfad überschreiben, damit der Embed stabil bleibt.

8a. **Embeds zählen.** Nach dem Einbetten prüfen, dass die Notiz genauso viele `![[`-Embeds wie `> [!ai-image]`-Callouts trägt und dass vor keinem Embed eine verwaiste Callout-Kopfzeile steht. Wer den Embed über einen Edit auf die `alt`-Zeile einfügt, lässt die Kopfzeile leicht doppelt zurück, und der Callout darüber bleibt leer im Text stehen.

   ```bash
   grep -c '^!\[\[' "<notiz>"
   grep -c '^> \[!ai-image\]$' "<notiz>"
   ```

   Beide Zahlen müssen gleich sein. Ein Treffer auf `> \[!ai-image\]` unmittelbar vor einer Embed-Zeile ist die verwaiste Kopfzeile und wird entfernt.

9. **Schreibregeln.** Das Einbetten ändert die Notiz, die der Hook prüft. Keine Em-Dashes, keine En-Dashes, keine Strichpunkte. Vor dem Abschluss `grep -nE "—|–|;"` auf die Notiz, ohne Treffer. Ein echter Umlaut in einem Dateinamen des Embed-Pfads ist kein Verstoß.

## Nicht tun

- Die erzeugten Bilder nicht selbst ansehen. Dafür gibt es den Agenten, und ein einziger Blick aus diesem Kontext heraus macht die Delegation wertlos.
- Den Stil-Block nicht selbst zusammenbauen, das übernimmt [[bild]].
- Vorhandene Bilder am Zielpfad bei einem erneuten Lauf bewusst überschreiben statt mit Suffixen zu duplizieren.

## Modellwahl

Der Skill orchestriert nur. Er liest die vorhandenen Callouts aus, bildet Ordner und Namen nach festen Regeln und verteilt die Arbeit an die Agenten. Ein Urteil bleibt bei ihm, die Wahl des Referenzbildes zur Szene in Schritt 5a, und das ist eine Zuordnung entlang sprechender Dateinamen. Die Auswahl der Variante und der Abgleich des Alt-Texts liegen beim Agenten.

Deshalb läuft er auf einem günstigen Tier, im Frontmatter als `model: sonnet` gesetzt. `bebildern` und [[bild]] tragen dasselbe Tier, die ganze Bildgenerierungs-Kette bleibt also auf einem günstigen Modell. Der `model: sonnet`-Override gilt für den ganzen Turn dieses Skills. Ein Subagent erbt ihn nicht, er bringt sein eigenes Modell aus seiner Definition mit.

## Abgrenzung

- [[bild-callout]] schreibt die Callouts, erzeugt aber keine Bilder. Erst danach greift dieser Skill.
- [[bild]] erzeugt ein einzelnes Bild, dieser Skill ruft es je Callout auf und bettet die Ergebnisse ein.

## Verbindungen

- [[bild-callout]] als vorgelagerter Schritt, der die Callouts schreibt
- `bebildern` als je Callout gestarteter Agent, der erzeugt, ansieht und ablegt
- [[bild]] als Bildmotor, den der Agent aufruft
- die `hint`-Notiz der Ablage als Quelle der Referenzregel in Schritt 5a
