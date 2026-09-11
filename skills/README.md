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
| [`hkb-suche`](hkb-suche/SKILL.md) | Eine Frage gegen die Wissensbasis beantworten und mit Verweisen belegen |
| [`hkb-wikidata`](hkb-wikidata/SKILL.md) | Unter den Kandidaten von `hk-wikidata` den richtigen Gegenstand wählen und eintragen |
| [`hkb-text`](hkb-text/SKILL.md) | Einen Text messen, seine Muster beurteilen und ihn heben |
| [`hkb-hinweis`](hkb-hinweis/SKILL.md) | Festhalten, was für diese eine Ablage gilt |
| [`hkb-publikation`](hkb-publikation/SKILL.md) | Texte zu einer Publikation ordnen und die Reihenfolge führen |
| [`hkb-erzaehlung`](hkb-erzaehlung/SKILL.md) | Einen Erzählbestand führen: Kanon, Kontinuität, Beurteilung |
| [`hkb-hennibock`](hkb-hennibock/SKILL.md) | Eine Notiz an eine HenniBock-Instanz übertragen und die Kapitelkette führen |

Was auf jeden Vault passt und keine Wissensbasis voraussetzt, trägt kein
Präfix:

| Skill | Wofür |
|---|---|
| [`humanize`](humanize/SKILL.md) | Einen Text auf KI-Schreibmuster prüfen und die betroffenen Stellen heben |
| [`artefakt-pruefen`](artefakt-pruefen/SKILL.md) | Ein Artefakt gegen Mechanik, Stimme und Kanon prüfen und übergeben |
| [`git-sicherheit`](git-sicherheit/SKILL.md) | Sicher mit Git in einer Ablage arbeiten |
| [`vault-pflege`](vault-pflege/SKILL.md) | Einen Obsidian-Vault pflegen, ohne ihn zu beschädigen |
| [`memory`](memory/SKILL.md) | Festhalten, was über die Sitzung hinaus gilt |
| [`skill-bauen`](skill-bauen/SKILL.md) | Einen neuen Skill für dieses Plugin anlegen |

Die Bildkette hängt am Magnific-Connector, den ein Plugin nicht mitliefern
kann. Ohne ihn brechen die vier oberen ab und sagen warum:

| Skill | Wofür |
|---|---|
| [`bild-callout`](bild-callout/SKILL.md) | Die `ai-image`-Callouts in eine Notiz schreiben, ohne Bilder zu erzeugen |
| [`bild`](bild/SKILL.md) | Ein einzelnes Bild erzeugen und ablegen. Der Motor der Kette |
| [`bild-notiz`](bild-notiz/SKILL.md) | Alle Callouts einer Notiz umsetzen und die Bilder einbetten |
| [`bild-cover`](bild-cover/SKILL.md) | Das Hochformat-Cover einer Publikation für `hk-epub` |
| [`bild-sidecars`](bild-sidecars/SKILL.md) | Die Metadaten-JSONs neben die Bilder eines Verzeichnisses schreiben |

**Ein Skill ruft einen Agenten.** Wo viel gelesen und wenig zurückgegeben
wird, gehört die Arbeit in einen eigenen Kontext. `bild-notiz` sieht kein Bild
an, das tut [`bebildern`](../agents/bebildern.md). Für die Regel oben ändert
das nichts: Ein Agent ist ein Kontext, kein Ersatz für ein Skript.

Drei davon tragen die eigentliche Last. **`hkb-import`** ist der Ort, an dem
die drei Urteile aus der Spezifikation fallen und als Zeile in
`# Entscheidungen` festgehalten werden (§5.7) — ohne das fragt jeder weitere
Lauf dieselbe Frage neu. **`hkb-notiz`** ist die einzige Operation, die kein
Script erledigt: Inhalt entsteht nicht mechanisch.

## Wo sie liegen

Sie werden nicht einzeln eingehängt, sondern als Plugin ausgeliefert. Das
Manifest steht in `.claude-plugin/plugin.json`, die Bausteine liegen an der
Wurzel des Repositorys. Alles trägt danach den Namensraum `hkf`, also
`hkf:hkb-notiz` und `hkf:marlene`. `hk-install` hängt das Plugin ein und
entfernt die Zeiger, die früher von Hand gesetzt wurden.

Ein Slash-Kommando liegt daneben: `/hkf:ablage` sagt, an welcher Wissensbasis
gearbeitet wird, und merkt eine Wahl.
