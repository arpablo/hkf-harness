---
type: proptype
form: text
values:
  - article
  - book
  - paper
  - podcast
  - transcript
  - video
  - web
created: 2026-09-01
modified: 2026-09-01T17:00:00
modified_by: claude-opus-5
---

Welcher Art ein Werk ist, auf das sich die Wissensbasis beruft.

Anders als die beiden anderen Aufzählungen wird dieser Property-Typ **nicht**
als Liste verwendet: Ein Werk ist ein Buch oder ein Video, nicht beides.

| Wert | Gemeint ist |
|---|---|
| `article` | Beitrag in einem größeren Zusammenhang: Zeitschrift, Zeitung, Sammelband, Blog |
| `book` | ein Werk für sich, mit Verlag und meist einer ISBN |
| `paper` | wissenschaftliche Arbeit: Aufsatz mit Begutachtung, Preprint, Dissertation, Bericht |
| `podcast` | Tonaufnahme einer Folge oder Sendung |
| `transcript` | Mitschrift: Vortrag, Gespräch, Sitzung |
| `video` | Bewegtbild, auch ein aufgezeichneter Vortrag |
| `web` | eine Webseite, die keines der übrigen ist |

Die Werte sind bewusst grob. Was ein Werk darüber hinaus auszeichnet — Verlag,
Auflage, Jahrgang, Seitenzahl —, ist Zitationsapparat und gehört in den Body
oder in eine eigene Property der Wissensbasis.

Ein aufgezeichneter Vortrag ist `video`, seine Mitschrift `transcript`: Es sind
zwei Ausfertigungen, und wer die Mitschrift liest, hat den Vortrag nicht
gesehen.
