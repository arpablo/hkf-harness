# Der Kanon

Was in jeder Sitzung gilt, unabhängig von Ablage, Rolle und Stimme. Der
SessionStart-Hook `hooks/sitzung.py` setzt diese Dateien in dieser Reihenfolge
zusammen und gibt sie als Sitzungskontext zurück.

| Datei | Was darin steht |
|---|---|
| `identitaet.md` | wer der Benutzer ist |
| `zusammenarbeit.md` | wie der Dialog geführt wird |
| `deutsche-sprache.md` | Wortwahl, Satzbau, Zeichen |
| `schreibregeln.md` | Inhalt, Struktur, Rhythmus |
| `yaml.md` | wie Frontmatter geschrieben wird |

**`identitaet.md` ist die einzige personenbezogene Datei.** Wer den Harness für
sich übernimmt, ersetzt sie und lässt den Rest stehen.

Die maschinenlesbare Fassung der Sprach- und Schreibregeln steht daneben in
`rules/deutsch.json`. Sie ist es, gegen die `hk-text` prüft. Was hier in Prosa
steht und dort nicht, gilt trotzdem, ist aber nicht messbar.

Was **eine einzelne Ablage** für sich festlegt, gehört nicht hierher, sondern
als Notiz vom Typ `hint` in die Ablage (Harness §7).
