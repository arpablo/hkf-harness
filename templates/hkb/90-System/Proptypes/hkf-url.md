---
type: proptype
form: text
pattern: '^(https?://\S+|\[[^\]\n]+\]\(https?://\S+\))$'
created: 2026-08-27
modified: 2026-08-27T12:41:08
modified_by: claude-opus-5
---

Absolute HTTP- oder HTTPS-Adresse, blank oder als Markdown-Link mit Anzeigetext: `https://example.org/x` oder `[Ein Titel](https://example.org/x)`.

Der zweite Fall ist für eine Adresse dasselbe, was `[[ziel|alias]]` für einen Verweis ist. Eine Quellenangabe ohne Titel zwingt den Leser, die Adresse zu deuten, und in einem Bestand, der Quellen sammelt, steht der Titel fast immer schon da.

Die Adresse darf Klammern tragen: `…/Cairo_Conference_(1921)` ist eine gewöhnliche Wikipedia-Adresse. Der Ausdruck greift deshalb bis zur letzten Klammer und nicht bis zur ersten.
