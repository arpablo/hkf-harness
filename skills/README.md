# Die KI-Schicht

Noch leer.

Hier kommen die Skills hin, die ein Sprachmodell durch die Methoden führen.
Für sie gilt eine Regel:

> **Kein Skill tut etwas, das kein Script tut.**

Ein Skill wählt aus, erklärt, fragt zurück und urteilt dort, wo die
Spezifikation ein Urteil verlangt — die Bedeutungsprüfung (§5.5), die
Identität einer ankommenden Notiz (§6.1 Schritt 5), die Verknüpfung (§5.6).
Alles Mechanische gehört nach `bin/` und `lib/`.

Der Grund ist die Zusage aus dem README: Eine Wissensbasis lässt sich ohne KI
benutzen und füllen. Sobald eine Operation nur über ein Modell erreichbar ist,
stimmt das nicht mehr. Dazu kommt die Verlässlichkeit — ein Programm findet
einen gebrochenen Wikilink immer, ein Modell meistens.

Daraus folgt die Reihenfolge: erst `bin/`, dann `skills/`. Solange
`hk-import` und `hk-export` Platzhalter sind, gibt es hier nichts zu tun.
