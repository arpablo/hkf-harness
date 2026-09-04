# Verwendung der deutschen Sprache

Diese Regeln gelten für jeden formulierten deutschen Text in einem teilnehmenden Vault. Ein Voice-Profil darf sie präzisieren, aber nicht aufheben.

## Grundsatz

Deutsch ist Standard. Etablierte englische Fachbegriffe bleiben stehen, wenn sie fachlich präziser sind. Der Text verwendet echte Umlaute und ß, nie ASCII-Ersatzformen.

## Wortwahl

Konkrete Wörter stehen vor abstrakten Sammelbegriffen. Wenn die Sache bekannt ist, nennt der Text sie. Fachbegriffe bleiben erlaubt, wenn sie ein tragfähiges Konzept benennen.

Vermeide Marketing-Sprech, akademischen Aufblas und leere Bedeutungsbehauptungen. Gesperrt sind `entscheidend`, `wesentlich`, `hervorheben`, `pulsierend`, `reichhaltig`, `nachhaltig`, `meisterhaft`, `darüber hinaus`, `zudem`, `ferner`, `bahnbrechend`, `letztendlich`, `im Grunde genommen`, `beleuchten`, `eintauchen`, `nahtlos`, `ganzheitlich`, `vielschichtig`, `Wechselspiel` und `dynamische Landschaft`.

Ein Wort wie `vielschichtig` kündigt Komplexität an, statt sie zu zeigen. Wo die Auflösung im nächsten Satz folgt, ist die Ankündigung überflüssig, und wo sie fehlt, ersetzt sie die Arbeit.

Diese Wörter gelten in jeder Beugung. `Der entscheidende Punkt` ist derselbe Verstärker wie `das ist entscheidend`. Ein Sachbegriff, der ein solches Wort als Wortanfang trägt, bleibt erlaubt, etwa `Nachhaltigkeit`. Ebenso ein eigenes Wort mit Vorsilbe wie `unwesentlich` und ein Fachbegriff wie `kriegsentscheidend`.

Ebenfalls vermeiden: die Zeitdiagnosen `in der heutigen Zeit` und `im digitalen Zeitalter`, die Ankündigungsformeln `es ist wichtig zu verstehen`, `an dieser Stelle sei erwähnt` und `wichtig zu erwähnen`, dazu `Zeugnis ablegen`. Was wichtig ist, wird gesagt und nicht als wichtig angekündigt.

## Satzbau

Aktivkonstruktionen stehen vor Passiv. Verben stehen vor Nominalisierungen. Ein Gedanke pro Satz ist die Regel. Lange Sätze werden geteilt, wenn sie mehrere unabhängige Beziehungen oder mehr als einen Nebensatz tragen.

Keine negative Parallelismusfigur wie `nicht nur X, sondern auch Y`. Keine dekorativen Dreierketten. Keine Pseudo-Verben wie `fungiert als`, wenn `ist` genügt. Keine vagen Zuschreibungen wie `Beobachter sagen` oder `Experten argumentieren`.

Keine angehängten Partizipien am Satzende, also kein `..., betonend, dass ...`, kein `..., hervorhebend, wie ...`. Der Gedanke steht in einem eigenen Satz oder entfällt. Keine Klammerbemerkung mitten im Satz, die den Lesefluss zerschneidet.

False Friends werden korrigiert. "eventuell" ist nicht *eventually*, also nicht "schließlich". "aktuell" ist nicht *actually*, also nicht "tatsächlich". `am Ende des Tages` ist kein deutscher Schlusssatz.

## Zeichen und Typografie

- Em-dash, en-dash und Strichpunkte sind verboten.
- Der ASCII-Bindestrich ist der einzige zugelassene Bindestrich.
- Das Muster ` - ` ist nur als Listen- oder Verbindungstrenner erlaubt, nicht als Gedankenstrich im Fließtext.
- Keine Emojis, außer ein Auftrag verlangt sie ausdrücklich.
- Ausrufezeichen bleiben Sonderfällen vorbehalten.
- Keine unsichtbaren Unicode-Zeichen wie Zero-Width-Space, Soft-Hyphen oder BOM.
- Anführungszeichen bleiben innerhalb einer Datei konsistent. YAML verwendet nur ASCII-Doppelquotes.
- Deutsches Dezimal- und Datumsformat: `3,5` und `12. Mai`.
- Deutsche Überschriften stehen in Satzschreibung, nicht in englischem Title Case.

## Durchsetzung

Die maschinenlesbare Fassung dieser Regeln steht genau einmal, im Regelsatz des gemeinsamen Skills `check-writing` unter `rules/deutsch.json`. Dort liegen die Schweregrade, die Stammlisten und die ausgenommenen Bereiche wie Code-Fences und Linkziele. Ein Hook prüft damit jeden Schreibvorgang auf eine Markdown-Datei.

Diese Datei trägt die Regeln als Anweisung, nicht als zweite Fassung. Bis Juli 2026 stand hier ein `writing_policy`-Block, den niemand ausgeführt hat: der Prüfer ist auf die Standardbibliothek beschränkt und liest deshalb JSON und kein YAML. Beide Fassungen mussten von Hand synchron gehalten werden, und sie waren es zweimal nicht.
