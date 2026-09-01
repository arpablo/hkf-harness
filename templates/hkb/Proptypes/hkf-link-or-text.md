---
type: proptype
form: text
created: 2026-09-01
modified: 2026-09-01T10:00:00
modified_by: claude-opus-5
---

Entweder ein qualifizierter Wikilink auf eine Notiz dieser Ablage oder ein
beliebiger Text. Beide Formen sind Text, die Property hat also eine
eindeutige Wertform.

Er ist für die Fälle gedacht, in denen dasselbe Feld mal auf eine Notiz zeigt
und mal nur einen Namen trägt: Ein Verfasser ist manchmal eine Personennotiz
und manchmal die Zeile auf einem Titelblatt, eine Zugehörigkeit manchmal eine
`organisation` und manchmal die Angabe unter einem Aufsatztitel. Für jeden
davon eine Notiz anzulegen hieße, die Ablage mit Namen zu füllen, über die
nichts weiter zu sagen ist.

Geprüft wird der Reihe nach: Sieht der Wert wie `[[…]]` aus, gilt Core §3.6
samt Zieltyp — ein Tippfehler im Pfad bleibt also ein Befund. Sonst ist es
Text und immer gültig.

Er nimmt **einen** `:`-Zusatz, anders als `hkf-link-or-url`. Dort ist die
zweite Alternative eine Adresse im Netz, die keinen Typ hat, den man fordern
könnte; hier ist sie ein Text. Der Zieltyp betrifft in beiden Fällen allein
die erste Alternative.

Die Listenform `hkf-link-or-text-list` ergibt sich nach Core §3.5.2 von selbst
und ist die übliche Verwendung — etwa in `authors` und `affiliations`.
