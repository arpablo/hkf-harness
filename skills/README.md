# Die KI-Schicht

Die Skills, die ein Sprachmodell durch die Methoden führen. Für sie gilt eine
Regel:

> **Kein Skill tut etwas, das kein Script tut.**

Ein Skill wählt aus, erklärt, fragt zurück und urteilt dort, wo die
Spezifikation ein Urteil verlangt — die Bedeutungsprüfung (§5.5), die
Identität einer ankommenden Notiz (§6.1 Schritt 5), die Verknüpfung (§5.6).
Alles Mechanische steht in `bin/` und `lib/`.

Der Grund ist die Zusage aus dem README: Eine Wissensbasis lässt sich ohne KI
benutzen und füllen. Sobald eine Operation nur über ein Modell erreichbar ist,
stimmt das nicht mehr. Dazu kommt die Verlässlichkeit — ein Programm findet
einen gebrochenen Wikilink immer, ein Modell meistens.

| Skill | Wofür |
|---|---|
| [`hkb`](hkb/SKILL.md) | Die Grundlage: wo die Ablage liegt, welche Regeln gelten, welche Werkzeuge es gibt. Die übrigen setzen ihn voraus. |
| [`hkb-notiz`](hkb-notiz/SKILL.md) | Eine Notiz anlegen oder fortschreiben |
| [`hkb-typ`](hkb-typ/SKILL.md) | Einen eigenen Typ anlegen oder seine Property-Tabelle erweitern |
| [`hkb-typseite`](hkb-typseite/SKILL.md) | Typseiten und Bases anlegen, damit `type` ein Verweis sein kann |
| [`hkb-import`](hkb-import/SKILL.md) | Eine Lieferung übernehmen — und die Urteile fällen und aufschreiben, die `hk-import` verweigert |
| [`hkb-export`](hkb-export/SKILL.md) | Eine Lieferung herausschreiben und beurteilen, ob sie weitergegeben werden kann |
| [`hkb-lint`](hkb-lint/SKILL.md) | Prüfen, korrigieren lassen, und die Befunde abarbeiten, die kein Werkzeug beheben darf |
| [`hkb-quelle`](hkb-quelle/SKILL.md) | Aus einer Quelle eine Lieferung machen — und wahlweise gleich importieren |

**Ein Skill ruft einen Agenten.** `hkb-quelle` liest eine Quelle nie
selbst, sondern schickt [`wilma`](../agents/wilma.md) — sie liest in ihrem
eigenen Kontext und gibt ein belegtes Destillat zurück. Für die Regel oben
ändert das nichts: Ein Agent liest, er schreibt nicht.

Drei davon tragen die eigentliche Last. **`hkb-import`** ist der Ort, an dem
die drei Urteile aus der Spezifikation fallen und als Zeile in
`# Entscheidungen` festgehalten werden (§5.7) — ohne das fragt jeder weitere
Lauf dieselbe Frage neu. **`hkb-notiz`** ist die einzige Operation, die kein
Script erledigt: Inhalt entsteht nicht mechanisch.
