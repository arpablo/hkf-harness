---
name: humanize
description: "Prüft deutschsprachigen Text auf KI-Schreibmuster und überarbeitet die betroffenen Stellen, ohne Substanz oder Belege zu verlieren. Für das Entfernen von KI-Tells, nicht für reines Korrektorat."
---

# Text humanisieren

## Zweck

Einen deutschsprachigen Text auf KI-Schreibmuster prüfen und nur die betroffenen Stellen überarbeiten. Substanz, Register und belegbare Aussagen bleiben. Der Text wird nicht glatter als nötig.

## Verhältnis zu hk-text und zur Stimme

Dieser Skill ergänzt `hk-text`, er ersetzt es nicht. `hk-text` prüft deterministisch die harten Regeln: Verbotswörter, Typografie, versteckte Unicode-Zeichen. Dieser Skill übernimmt das urteilende Stück, also die weichen Muster nach Cluster-Regel und das Umschreiben. Die Tonebene misst er an der Stimme, die die Wurzeldatei nennt. Welche Notiztypen welche Struktur brauchen, sagt die Ablage und nicht dieser Skill.

## Modi

Ein generisches Gerüst, die Zuordnung zu Notiztypen ist lokal.

- Locker: volle Stimme, aber nicht künstlich. Journal, Log, Tagebuch.
- Sachlich: dezent, neutral, am Voice-Profil ausgerichtet. Der Standard.
- Formal: keine Stimme einbringen, nur KI-Tells entfernen. Fach-, Rechts-, Vertragstext.

Ist der Modus unklar, nimm Sachlich an und sage das.

## Zwei Ebenen der Bewertung

- Harte Regeln, schon im Einzelfall: Verbotswörter und -phrasen, verbotene Satzkonstruktionen, Typografie. Diese prüft `hk-text`.
- Weiche Muster, Cluster-Regel: Rhythmus, Satzanfänge, Absatzlängen, kontextabhängiges Vokabular. Ein Einzelsignal ist kein Grund zum Umschreiben, erst die Häufung mehrerer unabhängiger Muster.

## Leitplanken über alle Pässe

Nichts erfinden, keine Quellen, keine Ich-Erfahrung, keine Anekdoten. Zahlen, Namen, Daten, Zitate, Begriffe und Wikilinks vor und nach jeder Änderung abgleichen. Substanz nie kürzen. Saubere Grammatik und Fachbegriffe sind kein KI-Tell. Direkte Zitate, Code, technische Spezifikationen und juristische Formulierungen nicht stilistisch umschreiben. Ist der Text sauber, sage das und höre auf.

## Ablauf

Fünf Pässe in fester Reihenfolge. Spätere Pässe dürfen frühere nicht invalidieren. Rhythmus immer zuletzt.

**Pass 0, Triage.** Modus, Texttyp, Umfang und Ziel bestimmen. Bei Datei-Input beide Messungen laufen lassen und die Kennzahlen notieren:

```bash
hk-text <pfad>
hk-text --rhythm <pfad>
```

Der erste Aufruf liefert die harten Befunde, der zweite die Rhythmus-Signale als JSON. Braucht der Rhythmus einen anderen Modus als `sachlich`, kommt er als Argument dazu:

```bash
hk-text --rhythm --mode locker <pfad>
```

Beide Messungen laufen im selben Werkzeug, damit Regelprüfung und Rhythmus denselben Text sehen und nicht zwei Vorstellungen davon pflegen, was Prosa ist. Beide messen denselben Text. Code, Linkziele, Adressen, Frontmatter-Bezeichner und Callouts mit `ai-`-Präfix fallen heraus. Ein englischer Bildprompt taucht deshalb weder als Regelverstoss noch als Rhythmus-Signal auf.

Bei Inline-Text den Rohtext zuerst in eine temporäre UTF-8-Datei schreiben, nie Nutzereingaben in einen Shell-Befehl interpolieren. Läuft ein Skript nicht, das melden und nicht blind von Hand ersetzen.

**Pass 1, Typografie und Evidenz.** Die harten Befunde aus `hk-text` abarbeiten: Striche, Strichpunkte, versteckte Zeichen, Umlaut-Ersatz, gemischte Anführungszeichen, Chatbot- und Brieffloskeln, vage Zuschreibungen ohne Beleg. Keine Stilarbeit in diesem Pass. Fehlende Belege markieren statt spekulativ füllen.

**Pass 2, Lexik.** Weiches Vokabular nach Cluster-Regel, harte Verbote im Einzelfall: Bedeutungs-Verstärker, Schaufenster- und Marketing-Vokabular, mechanische Übergangswörter, Füllformeln, KI-Marker, Pseudo-Verben statt Kopula, Abstrakta und Hypernyme. Hypernyme und Nominalstil nur dort auflösen, wo der konkrete Sachverhalt belegt im Text oder Kontext steht.

**Pass 3, Struktur.** Cluster-Regel: schematische Schluss-Abschnitte (Fazit, Ausblick, bewertender Zusammenfassungssatz), Zusammenfassungsmarker, hybride Fett-Listen, Stichpunkt-Listen statt Prosa im Fließtext, mechanisches Fettdrucken, Title Case in Überschriften, isometrische Blöcke. Erst nach diesem Pass steht die endgültige Absatzstruktur. Die Struktur-Pflichten je Notiztyp stehen in der Typdefinition.

**Pass 4, Rhythmus.** Aus den Signalen von `rhythm_lint.py`, standardmäßig in Locker und Sachlich, in Formal nur auf Wunsch: Vorfeld rotieren (höchstens etwa zwei von drei Sätzen subjektinitial), Satzlänge spreizen, Absatzlängen entzerren, höchstens ein mechanischer Konnektor pro Absatz. Nicht auffüllen, sondern Sätze teilen oder zusammenziehen.

## Selbstcheck

**Pass 5, Selbst-Audit.** Eigene Änderungen gegen die Regeln und das Zielprofil prüfen: neue Monotonie erzeugt (dieselbe Ersatzkonstruktion dreimal, dann Strategie rotieren)? Keine erfundene Quelle, keine erfundene Erfahrung, keine neuen Faktenanker, keine Substanzkürzung? Wikilinks und Frontmatter unversehrt?

Ausgabe, nie den vollständigen Text, nur die geänderten Stellen:

1. Modus, eine Zeile.
2. Gefundene Muster, höchstens sechs Bullet Points mit kurzem Zitat und Regelbezug.
3. Geänderte Stellen, Vorher- und Nachher-Paare nur für bearbeitete Passagen.
4. Kurzaudit, höchstens drei verbleibende Tells oder "Keine gefunden".

## Was aus der Ablage kommt

Die Zuordnung der Modi zu Typen, die Struktur-Pflichten je Typ, der Kanon und was die Ablage für sich festgelegt hat. Das steht in den Typdefinitionen und den `hint`-Notizen, und der Sitzungskontext bringt es mit. Dieser Skill liefert die Prozedur und die weiche-Muster-Ebene.

Damit ist er bewusst unvollständig. Findet sich in der Ablage nichts über die Struktur eines Typs, bleiben die Struktur-Pässe bei dem, was der Text selbst hergibt, und erfinden keine Vorgaben.

## Herkunft

Die Prüf-Mechanik ist abgeleitet aus `humanizer-de` in der Fassung 4.0.2 von Martin Moeller (MIT, https://www.martin-moeller.biz), einer deutschen Ableitung von https://github.com/blader/humanizer. Übernommen sind Cluster-Regel, feste Pass-Reihenfolge, Selbst-Audit und der Verzicht auf Volltextausgabe.

Der Fremd-Skill selbst ist nicht mehr installiert. Diese Angaben sind daher die einzige verbliebene Quelle der Zuschreibung.

Dieser Skill bringt keine eigenen Skripte mit. Beide Messungen liegen in `hk-text`.
