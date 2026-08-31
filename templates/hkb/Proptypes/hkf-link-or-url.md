---
type: proptype
form: text
created: 2026-08-29
modified: 2026-08-29T08:40:00
modified_by: claude-opus-5
---

Entweder ein qualifizierter Wikilink auf eine Notiz dieser Ablage oder eine
absolute HTTP- oder HTTPS-Adresse. Beide Formen sind Text, die Property hat
also eine eindeutige Wertform.

Geprüft wird der Reihe nach: Sieht der Wert wie `[[…]]` aus, gilt Core §3.6,
sonst das Muster von `hkf-url`. Erfüllt er keines von beiden, nennt der Befund
beide Möglichkeiten — geraten wird nicht.

Er nimmt **keinen** `:`-Zusatz. Wer einen Zieltyp fordern und trotzdem eine
Adresse zulassen will, schreibt die Alternative aus: `hkf-link:person /
hkf-url`. `hkf-link-or-url` ist die Abkürzung für den häufigen Fall, in dem der
Zieltyp gleichgültig ist.

Die Listenform `hkf-link-or-url-list` ergibt sich nach Core §3.5.2 von selbst
und ist die übliche Verwendung — etwa in der Property `related`, die aufnimmt,
was unter `# Siehe auch` steht.
