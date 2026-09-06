#!/usr/bin/env python3
"""next_chapter.py - bestimmt das naechste offene Kapitel einer Publikationsstrecke
und prueft, was ihm zum Publizieren auf HenniBock noch fehlt.

Aufruf:
    python3 next_chapter.py next            # naechstes offenes Kapitel als JSON
    python3 next_chapter.py queue           # ganze Warteschlange als Uebersicht
    python3 next_chapter.py attached <Kap>  # haengt das Kapitel in seiner Publikation?

Die Steuerung steht im Vault, nicht in einer Config-Datei:

  Pub - <Name>.md    hennibock_queue: <n>            dabei in der Rotation, Zahl nur als Tiebreak
                     hennibock_chapter_type: essay   Typ, den die Kapitel erben, Default essay
                     hennibock_areas:                HenniBock-Bereiche der Kapitel
                       - Wirtschaft
  Kap - <Name>.md    hennibock_skip: true            Kapitel nie publizieren (etwa Danksagung)
                     hennibock_ref: <uuid>           Identitaet, vom Publish-Skill gesetzt

Ob ein Kapitel publiziert ist, steht nicht im Vault, sondern auf dem Server. Die
Frontmatter-Felder taugen dafuer nicht: hennibock_ref traegt auch ein blosses
Verweisziel, das nie publiziert wurde, hennibock_published setzt schon ein
analyze, und hennibock_slug stammt aus der Zeit vor der UUID-Identitaet. Nach dem
Zuruecksetzen der Instanz am 19.07. behaupteten alle drei Felder eine
Veroeffentlichung, die es nicht mehr gab. Deshalb wird der Bestand einmal je Lauf
ueber GET /documents abgefragt und mit der document_ref der Notiz verglichen.

hennibock_type der Pub-Datei ist ausdruecklich NICHT die Vorlage fuer die Kapitel.
Es ist der eigene Typ der Publikation (publication, sobald sie selbst publiziert
wird) und geht dieses Skript nichts an. Frueher meinte das eine Feld beides, was
mit dem Typ publication kollidierte. Deshalb traegt die Vererbung jetzt einen
eigenen Namen. Fehlt hennibock_chapter_type, gilt essay, es gibt keinen Rueckfall
auf hennibock_type: der wuerde die alte Zweideutigkeit wieder einschleppen und
einer Publikation ihre Kapitel als Typ publication vererben.

Zwei Reihenfolgen, die nicht zu verwechseln sind:

  Welche Publikation ist dran?  Reihum. Dran ist die, deren letztes publiziertes
  Kapitel am laengsten zurueckliegt, abgeleitet aus hennibock_published der
  Kapitel. Gleichstand loest hennibock_queue auf. Eine durchgelaufene Strecke
  faellt von selbst raus.

  Welches Kapitel dieser Publikation?  Das erste offene in der Reihenfolge des
  Inhaltsverzeichnisses der Pub-Datei, nie aus der Dateiliste.

Der Rotationszustand steht damit im Vault selbst, nicht in einer Zustandsdatei.
Er ueberlebt jeden Abbruch und laesst sich in Obsidian nachvollziehen.

next liefert das faellige Kapitel samt Befund, was ihm fehlt (Datei, summary,
Callouts, Bilder). Gibt es keines mehr, ist "chapter" null.

attached ist die Gegenprobe nach dem Publizieren: liegt das Kapitel in den
document_chapters seiner Publikation? Ein Verzeichnispunkt traegt das Ziel, das
er beim letzten Import des Publikations-Bodys hatte. War die Kapitelnotiz damals
noch keine Datei, blieb der Punkt Text, und das Kapitel erscheint als loser
Beitrag ohne "Erscheint in" und ohne Nachbarnavigation. Exit 0 heisst
eingehaengt, Exit 1 nennt Befund und Abhilfe.

Das Skript aendert nichts, es liest nur.

Nur Standardbibliothek.
"""

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

def _vault_root(arg=None) -> Path:
    """Die Ablage dieses Laufs, aufgeloest wie in jedem Werkzeug des Harness."""
    from .. import ablage
    try:
        return Path(ablage.finde(arg))
    except ablage.KeineAblage as fehler:
        raise SystemExit("FEHLER: " + str(fehler))


# Die Ablage wird erst in `main` bestimmt und nicht beim Import. Vorher stand
# hier `VAULT = _vault_root(...)` als Modulglobale, und das hatte drei Folgen:
# `--ablage` konnte nicht wirken, weil die Aufloesung vor dem Lesen der
# Argumente lief; das Modul liess sich ohne auflösbare Ablage nicht einmal
# importieren, auch nicht fuer eine Probe seiner reinen Funktionen; und der
# Pfad hing an der Umgebung eines Prozesses statt am Aufruf.
VAULT = None
INDEX = None


def setze_ablage(arg=None):
    """Bestimmt die Ablage dieses Laufs und baut den Notiz-Index."""
    global VAULT, INDEX
    VAULT = _vault_root(arg)
    from . import kern
    INDEX = kern.build_note_index(VAULT)
    return VAULT


def split_frontmatter(text: str):
    if not text.startswith("---"):
        return "", text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return "", text
    return parts[1], parts[2]


def fm_scalar(fm: str, key: str):
    m = re.search(r"^" + re.escape(key) + r":\s*(.*)$", fm, re.M)
    if not m:
        return None
    v = m.group(1).strip().strip('"').strip("'")
    return v or None


def fm_list(fm: str, key: str):
    m = re.search(r"^" + re.escape(key) + r":\s*$\n((?:[ \t]+-.*\n?)+)", fm, re.M)
    if m:
        return [re.sub(r'^[ \t]*-\s*', '', l).strip().strip('"').strip("'")
                for l in m.group(1).strip("\n").split("\n") if l.strip()]
    inline = fm_scalar(fm, key)
    if inline and inline.startswith("["):
        return [x.strip().strip('"').strip("'")
                for x in inline[1:-1].split(",") if x.strip()]
    return []


def embed_ziel(ziel: str) -> str:
    """Der Dateipfad eines Embeds, ohne Alias und ohne Anker.

    Anders als `kern.strip_wikilink` bleibt der Pfad stehen, denn hier wird
    damit auf die Datei zugegriffen. Ohne diesen Schnitt meldete der Audit in
    einer HKB jedes Bild als ins Leere zeigend: HKF Core §3.6 verlangt den
    Alias, und `80-Media/Images/x.jpg|x.jpg` ist kein Dateiname.
    """
    return ziel.split("|", 1)[0].split("#", 1)[0].strip()


def toc_chapters(pubtext: str):
    """Kapitel-Wikilinks in Dokumentreihenfolge, ohne den Verweisapparat.

    Ruft `kern.publication_order_text`, statt die Regel ein zweites Mal zu
    fuehren. Die frueher hier stehende Fassung hatte drei eigene Annahmen: sie
    schnitt nur bei `# Siehe auch`, verlangte das Praefix `Kap - ` im
    Verweisziel und kannte keinen qualifizierten Verweis. Alle drei gelten in
    HenniPKA und keine in einer HKB, und deshalb sah sie dort in drei von
    zwoelf Publikationen ueberhaupt kein Kapitel mehr.
    """
    from . import kern
    return kern.publication_order_text(pubtext)


# Stilworte, die dem Hausstil widersprechen. Kommen aus Alt-Callouts, die vor
# der Bildstil-Regel geschrieben wurden. Ein Bild aus so einem Callout passt
# weder zum Hausstil noch zu den uebrigen Bildern der Strecke.
STILWIDRIG = [
    "oil painting", "oil-painting", "painterly", "painted in", "painting",
    "illustration", "illustrated", "sepia", "cartographic", "watercolor",
    "engraving", "etching", "expressionist", "impressionist", "art nouveau",
    "poster style", "woodcut", "lithograph", "photorealistic", "film still",
]

# Wortgrenze am Anfang, Suffix-Toleranz am Ende. Die Grenze vorn verhindert
# Falsch-Positive mitten im Wort ("stretching" ist kein "etching"), die offene
# Endung faengt die Beugungen mit ("etchings", "lithography", "engravings").
STILWIDRIG_RX = [(w, re.compile(r"\b" + re.escape(w) + r"\w*", re.I))
                 for w in STILWIDRIG]

# Ein verneintes Stilwort ist keine Bestellung, sondern ihr Gegenteil. Der
# Standard-Baustein aus [[Bildstil]] schliesst die Stile ausdruecklich aus
# ("not a photograph and not a photographic film still"), und ein Callout darf
# einen Stil auch selbst sperren ("explicitly not a realistic historical
# illustration and not a painting"). Ohne diese Sperre meldet der Audit genau
# die Callouts als stilwidrig, die den Stil am deutlichsten ausschliessen, und
# ein Lauf loescht sie samt ihrer Bilder. Am 2026-07-28 traf das zwei
# einwandfreie Callouts von Kapitel 7 der Strecke Der sechste Kondratieff.
# Das Vorbild ist die Sperre in bestellt_text(), die ein "no text" genauso
# auswertet.
#
# Zwischen Verneinung und Stilwort duerfen bis zu vier Fuellwoerter stehen, das
# deckt Artikel und Adjektive ab. Ein Satzzeichen beendet die Reichweite, sonst
# deckte ein "not a photo, use an oil painting look" seine eigene Anweisung zu.
# Gesucht wird ueber den ganzen Text statt in einem Fenster vor der Fundstelle:
# ein Fenster kann ein Wort zerschneiden und aus dem Ende von "casino" ein
# verneinendes "no" machen.
VERNEINT_RX = re.compile(
    r"\b(?:not|no|never|avoid|without)\s+(?:[\w-]+\s+){0,4}"
    r"(?=(?:" + "|".join(re.escape(w) for w in STILWIDRIG) + r")\w*\b)",
    re.I,
)


def stilwidrige_treffer(text: str):
    """Stilworte im Text. Ein Treffer, der ganz in einem laengeren steckt,
    faellt weg, damit "oil painting" nicht zusaetzlich "painting" meldet.
    Ein verneinter Treffer faellt ebenfalls weg, siehe VERNEINT_RX."""
    verneint = {m.end() for m in VERNEINT_RX.finditer(text)}
    roh = [(m.start(), m.end(), w)
           for w, rx in STILWIDRIG_RX for m in rx.finditer(text)]
    treffer = {w for s, e, w in roh
               if s not in verneint
               and not any((s2, e2) != (s, e) and s2 <= s and e <= e2
                           for s2, e2, _ in roh)}
    return sorted(treffer)


# Wendungen, mit denen ein Callout Text im Bild bestellt. Das Bildmodell setzt
# ihn in der Sprache des Prompts, also englisch, und die Prompts sind englisch.
# Ein englisch beschriftetes Bild in einem deutschen Kapitel ist ein Fremdkoerper,
# siehe Bildstil, Abschnitt Beschriftungen.
TEXT_IM_BILD = [
    "labeled", "labelled", "label", "labels", "small text", "caption",
    "captioned", "annotated", "annotation", "lettering", "signage",
    "axis name", "axis label", "titled", "written",
]
TEXT_IM_BILD_RX = [(w, re.compile(r"\b" + re.escape(w) + r"\w*", re.I))
                   for w in TEXT_IM_BILD]


def callout_bloecke(body: str):
    """Jeder ai-image-Callout als Textblock, inklusive seiner Metadatenzeilen."""
    return re.findall(r"^>\s*\[!ai-image\]\s*\n((?:^>.*\n)+)", body, re.M)


# Signatur des Studio-Stilllebens: ein Gegenstand auf neutralem Grund, von oben
# oder frontal, mit viel Leerraum. Das ist die uebliche Form eines Callouts, der
# eine These illustriert, statt eine Szene zu zeigen.
ABSTRAKT_RX = re.compile(
    r"\b(?:(?:plain |on a )white (?:surface|ground|table)|white ground|"
    r"neutral (?:white |grey )?(?:surface|background)|seen from directly above|"
    r"close overhead view|from a low three-quarter angle|"
    r"arranged in a (?:widening )?(?:ring|arc|row)|laid out (?:on|to form))\b",
    re.I,
)
# Woran ein Bild mit Informationsgehalt erkennbar ist: Menschen oder ein Ort.
# Eine blosse Zeitangabe zaehlt ausdruecklich nicht: "of about 1900" steht auch
# in einem Stillleben aus Koffern und sagt nichts darueber, ob eine Szene zu
# sehen ist.
KONKRET_RX = re.compile(
    r"\b(?:men|women|man|woman|people|crowd|delegates?|officers?|"
    r"soldiers?|sailors?|ministers?|diplomats?|street|alley|harbou?r|quay|port|city|"
    r"town|square|hall|chamber|room|ship|boat|vessel|train|railway|palace|mosque|"
    r"fortress|coast|desert|landscape)\b",
    re.I,
)

# Zwei Motive, die [[Skill - AI-Callouts schreiben]] in Schritt 5 ausdruecklich
# zulaesst, wo ein Begriff keine Szene hat. Sie tragen die Studio-Signatur und
# nennen weder Menschen noch einen Ort, sind aber gerade kein Stillleben als
# Metapher.
#
# Erstens die ikonischen Objekte auf einer Wellenlinie, je eins am Gipfel einer
# Welle, im Skill als "legibel, hausstilkonform und mehrfach erprobt" gefuehrt
# und dort mit genau dieser Reihe belegt: Dampfmaschine, Lokomotive, Gluehbirne,
# Automobil, Serverrack. Zweitens das Diagramm als greifbarer Gegenstand, also
# als Ausdruck auf einem Tisch, Kreidezeichnung an einer Tafel oder aufgerolltes
# Papier.
#
# Der Unterschied zum Fehlgriff liegt darin, was das Objekt tut. Ein Ikon zeigt
# seine Sache selbst, eine Gluehbirne die Elektrizitaet, ein Serverrack das
# Rechenzentrum, siehe [[Bildstil]], Abschnitt Beschriftungen. Zwei Seile mit
# unterschiedlich festen Knoten stehen dagegen fuer eine Behauptung ueber
# Buendnisse und zeigen nichts. Deshalb zaehlt die Ausnahme erst ab zwei
# verschiedenen Ikonen und nur zusammen mit der Wellenform: ein einzelnes Objekt
# auf weissem Grund ist der Fehlgriff und nicht das Motiv. Am 2026-07-28 hat der
# Befund das Wellen-Motiv von Kapitel 6 der Strecke Der sechste Kondratieff
# getroffen, obwohl der Callout-Skill es empfiehlt.
IKON = [
    "steam engine", "locomotive", "light bulb", "lightbulb", "automobile",
    "motor car", "server rack", "microchip", "printing press", "dynamo",
    "telegraph key", "telephone", "satellite dish", "spinning frame",
    "water wheel", "waterwheel", "blast furnace", "oil derrick",
]
IKON_RX = [(w, re.compile(r"\b" + re.escape(w) + r"s?\b", re.I)) for w in IKON]

# Nur der Plural. Das Motiv ist eine Reihe von Wellen mit je einem Objekt am
# Gipfel, es hat immer mehrere. Ein einzelnes "curve" oder "arc" faellt dagegen
# in jedem zweiten Prompt und wuerde die Ausnahme aufweichen, etwa bei der
# "gentle curve" eines Seils in einem Stillleben.
WELLE_RX = re.compile(r"\b(?:waves|swells|arcs)\b", re.I)

DOKUMENT_RX = re.compile(
    r"\b(?:blackboard|chalkboard|chalk drawing|graph paper|squared paper|"
    r"printout|printed sheet|rolled(?:-up)? paper|"
    r"open (?:book|ledger|atlas|notebook))\b",
    re.I,
)


def sanktioniertes_motiv(block: str) -> bool:
    """Traegt dieser Callout eines der beiden zugelassenen Ersatzmotive?"""
    ikone = {w for w, rx in IKON_RX if rx.search(block)}
    if len(ikone) >= 2 and WELLE_RX.search(block):
        return True
    return bool(DOKUMENT_RX.search(block))


def zu_abstrakt(block: str) -> bool:
    """Illustriert dieser Callout eine These, statt eine Szene zu zeigen?

    Ein Bild soll dem Leser etwas zeigen, das er sonst nicht saehe: einen Ort,
    eine Handlung, eine Figur, einen Gegenstand seiner Zeit. Ein Stillleben aus
    Seilen, Siegeln oder Waagen auf weissem Grund traegt dagegen keinen
    Informationsgehalt, es wiederholt nur bildlich, was der Text schon sagt.
    Armin am 2026-07-19 zu einem so bebilderten Kapitel: die Bilder haetten
    "eigentlich keinen Informationsgehalt".

    Die Pruefung ist bewusst grob. Sie schlaegt an, wenn ein Callout die
    Studio-Signatur traegt und zugleich keine Menschen, keinen Ort und keine
    Zeitangabe nennt. Ein Gegenstand vor konkretem Hintergrund faellt nicht
    darunter, ein Diagramm-Ersatz auf weisser Flaeche schon.

    Die beiden vom Callout-Skill zugelassenen Ersatzmotive sind ausgenommen,
    siehe sanktioniertes_motiv().
    """
    if sanktioniertes_motiv(block):
        return False
    return bool(ABSTRAKT_RX.search(block)) and not KONKRET_RX.search(block)


def bestellt_text(block: str):
    """Verlangt dieser Callout Text im Bild? Ein 'no text' hebt das auf.

    Die Sperre darf Zwischenwoerter tragen. Die uebliche Formel lautet
    "no written text, no letters, no numbers", und ein Muster, das nur das
    nackte "no text" kennt, sieht darin das Wort "written" und meldet genau
    den Callout als textbestellend, der Text am deutlichsten verbietet.
    """
    if re.search(r"\bno\s+(?:\w+\s+){0,2}"
                 r"(?:text|lettering|letters?|labels?|writing|captions?)\b",
                 block, re.I):
        return []
    return sorted({w for w, rx in TEXT_IM_BILD_RX if rx.search(block)})


def body_ohne_verbindungen(body: str):
    """Der Prosa-Teil, den hennibock-publish spaeter auch sendet."""
    m = re.search(r"^#{1,2}\s+Verbindungen\s*$", body, re.M)
    return body[: m.start()] if m else body


def bild_deckung(body: str):
    """Genug Callouts, und liegen sie ueber den ganzen Text verteilt?

    [[Skill - AI-Callouts schreiben]] verlangt einen Callout je H2-Sektion und
    ausdruecklich Bilder auch in der zweiten Haelfte und am Schluss. Ohne diese
    Pruefung meldet der Audit ein Kapitel mit drei Alt-Callouts auf elf
    Sektionen als vollstaendig, und der Lauf erzeugt drei Bilder im oberen
    Drittel. Genau so ist es am 2026-07-16 passiert.

    Bis 2026-07-19 stand hier eine Untergrenze von einem Callout je zwei
    Sektionen. Sie war als Minimum gemeint, wurde aber als Ziel gelesen: der
    Lauf hoerte auf, sobald `zu_duenn` auf False sprang, und lieferte fuenf
    Bilder auf neun Sektionen, waehrend die gepflegten Kapitel derselben
    Strecke bei etwa einem Bild je Sektion liegen. Ein Schwellwert, den ein
    Agent als erreichtes Ziel behandelt, muss dort stehen, wo das Ergebnis gut
    ist, nicht dort, wo es gerade noch vertretbar ist.
    """
    prosa = body_ohne_verbindungen(body)
    h2 = re.findall(r"^##\s+\S", prosa, re.M)
    soll = max(1, len(h2))
    stellen = [m.start() for m in re.finditer(r"^>\s*\[!ai-image\]", prosa, re.M)]
    # Verteilung am letzten Drittel messen: ein Schlussbild ist Pflicht, und
    # ein bildloses letztes Drittel ist der haeufigste Verteilungsfehler.
    letztes_drittel = len(prosa) * 2 // 3
    schluss_leer = bool(h2) and not any(s >= letztes_drittel for s in stellen)
    return {
        "h2_sektionen": len(h2),
        "callouts_soll": soll,
        "callouts_ist": len(stellen),
        "zu_duenn": len(stellen) < soll,
        "schluss_ohne_bild": schluss_leer,
    }


def audit_chapter(path: Path):
    """Was fehlt diesem Kapitel zum Publizieren."""
    if not path.exists():
        return {"exists": False, "needs": ["kapitel-schreiben", "callouts",
                                           "bilder", "summary"]}
    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    needs = []

    summary = fm_scalar(fm, "summary")
    if not summary:
        needs.append("summary")

    embeds = [embed_ziel(e) for e in re.findall(r"!\[\[([^\]]+)\]\]", body)]
    callouts = re.findall(r"^>\s*\[!ai-image\]", body, re.M)
    if not embeds:
        needs.append("bilder")
    if not callouts:
        needs.append("callouts")

    # Alt-Callouts erkennen: stilwidrige Worte, fehlendes Magnific-Projekt oder
    # bestellter Text im Bild.
    bloecke = callout_bloecke(body)
    stilwidrig, ohne_projekt, mit_text, abstrakt = [], 0, [], 0
    ohne_alt = 0
    for b in bloecke:
        treffer = stilwidrige_treffer(b)
        if treffer:
            stilwidrig.append(treffer)
        if not re.search(r"^>\s*project:", b, re.M):
            ohne_projekt += 1
        # Seit dem 29.07.2026 traegt jeder neue Callout seinen deutschen
        # Alt-Text selbst. Im Altbestand fehlt er, und ohne diesen Befund
        # merkte das erst der Publish-Lauf.
        if not re.search(r"^>\s*alt:", b, re.M):
            ohne_alt += 1
        t = bestellt_text(b)
        if t:
            mit_text.append(t)
        if zu_abstrakt(b):
            abstrakt += 1
    if stilwidrig:
        needs.append("callouts-stilwidrig")
    if bloecke and ohne_projekt:
        needs.append("callouts-ohne-projekt")
    if ohne_alt:
        needs.append("alt-text-fehlt")
    if mit_text:
        needs.append("callouts-mit-text")
    if abstrakt:
        needs.append("callouts-zu-abstrakt")

    # Deckung und Verteilung. Greift auch dann, wenn schon Callouts da sind,
    # sonst gilt ein duenn bebildertes Kapitel faelschlich als fertig.
    deckung = bild_deckung(body)
    if callouts and deckung["zu_duenn"]:
        needs.append("callouts-zu-duenn")
    if callouts and deckung["schluss_ohne_bild"]:
        needs.append("callouts-schlecht-verteilt")

    # Bilder ohne unmittelbar folgenden Callout haben keine Alt-Text-Quelle.
    ohne_callout = []
    for m in re.finditer(r"!\[\[([^\]]+)\]\]", body):
        rest = body[m.end():].lstrip("\n")
        if not rest.startswith("> [!ai-image]"):
            ohne_callout.append(embed_ziel(m.group(1)))
    if ohne_callout:
        needs.append("alt-quelle-fehlt")

    fehlend = [e for e in embeds if not (VAULT / e).exists()]
    if fehlend:
        needs.append("embed-zeigt-ins-leere")

    return {
        "exists": True,
        "summary": summary,
        "n_embeds": len(embeds),
        "n_callouts": len(callouts),
        "bild_deckung": deckung,
        "callouts_stilwidrig": stilwidrig,
        "callouts_ohne_projekt": ohne_projekt,
        "callouts_ohne_alt": ohne_alt,
        "callouts_zu_abstrakt": abstrakt,
        "callouts_mit_text": mit_text,
        "bilder_ohne_callout": ohne_callout,
        "embeds_ins_leere": fehlend,
        "needs": needs,
    }


def load_queue():
    """Die Publikationen mit `hennibock_queue`, nach ihrer Nummer sortiert.

    Gesucht wird ueber das Frontmatter und nicht ueber Ordner und Dateinamen.
    Vorher stand hier `PUBDIR.glob("*/Pub - *.md")` mit `PUBDIR` fest auf
    `50 Output/Publications`, und das setzte drei Dinge voraus: den
    Ordnernamen von HenniPKA, je ein eigenes Unterverzeichnis pro Werk und das
    Praefix `Pub - ` im Dateinamen. In einer HKB gilt keines davon, dort liegen
    die Publikationen flach unter `<output_base>/Publications` und tragen kein
    Praefix (§4). `kern.publikationsnotizen` sucht seit jeher so, und die
    Docstring dort nennt den Grund: ein gemeinsames Werkzeug kennt die Ablage
    eines Vaults nicht.
    """
    pubs = []
    for pubfile in sorted(INDEX.values()):
        try:
            text = pubfile.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        fm, _ = split_frontmatter(text)
        if fm_scalar(fm, "hennibock_type") != "publication":
            continue
        q = fm_scalar(fm, "hennibock_queue")
        if q is None:
            continue
        try:
            q = int(q)
        except ValueError:
            continue
        pubs.append({
            "queue": q,
            "name": pub_name(fm, pubfile),
            "pubfile": str(pubfile.relative_to(VAULT)),
            # Der an die Kapitel vererbte Typ, nicht der eigene Typ der Pub.
            # Kein Rueckfall auf hennibock_type, siehe Kopfkommentar.
            "chapter_type": fm_scalar(fm, "hennibock_chapter_type") or "essay",
            "areas": fm_list(fm, "hennibock_areas"),
            "chapters": toc_chapters(text),
        })
    pubs.sort(key=lambda p: p["queue"])
    return pubs


def pub_name(fm: str, pubfile: Path) -> str:
    """Der Name eines Werkes, wie ein Mensch ihn nennt.

    Vorher war es der Name des Elternordners. Das traf in HenniPKA zu, wo jedes
    Werk sein eigenes Verzeichnis hat, und ergab in einer HKB fuer jedes Werk
    denselben Namen `Publications`.
    """
    return fm_scalar(fm, "title") or strip_praefix(pubfile.stem)


def strip_praefix(stem: str) -> str:
    """Ein Typ-Praefix wie `Pub - ` ordnet einen Vault und gehoert nicht zum
    Namen. Eine HKB kennt es nicht, HenniPKA schon."""
    for p in ("Pub - ", "Kap - ", "Text - "):
        if stem.startswith(p):
            return stem[len(p):]
    return stem


def kapitel_pfad(name: str):
    """Der Pfad eines Kapitels, ueber den Notiz-Index.

    Vorher stand hier `pub["dir"] / (name + ".md")`, also die Annahme, ein
    Kapitel liege im selben Verzeichnis wie seine Publikation. In HenniPKA ist
    das so, in einer HKB liegen die Texte unter `<output_base>/Texts` und die
    Publikationen daneben.
    """
    from . import kern
    return INDEX.get(kern.nfc(name))


def server_url():
    # Dieselbe Aufloesung wie beim Senden. Zwei Wege zum selben Ziel liefen
    # auseinander, sobald einer davon eine Stufe mehr kennt.
    from . import kern
    url, _woher = kern.ziel()
    if not url:
        raise SystemExit(
            kern.KEIN_ZIEL + "\nOb ein Kapitel publiziert ist, steht auf dem "
            "Server, nicht in der Ablage."
        )
    return url


_dokumente = None


def dokumente_vom_server():
    """Was auf der Instanz liegt: document_ref -> Datensatz. Einmal je Lauf geholt.

    Der Server ist die einzige verlaessliche Auskunft darueber, was
    veroeffentlicht ist. Faellt die Abfrage aus, bricht das Skript ab, statt zu
    raten: ein leerer Bestand sieht sonst aus wie eine unbediente Strecke, und
    der naechste Lauf publizierte ein Kapitel ein zweites Mal.
    """
    global _dokumente
    if _dokumente is not None:
        return _dokumente
    url = server_url()
    docs_by_ref = {}
    try:
        for typ in ("essay", "title_story", "weekly_image", "publication"):
            with urllib.request.urlopen(url + "/documents?type=" + typ, timeout=20) as r:
                daten = json.loads(r.read().decode("utf-8"))
            docs = daten if isinstance(daten, list) else daten.get("documents", [])
            for d in docs:
                if d.get("document_ref"):
                    docs_by_ref[d["document_ref"]] = d
    except (urllib.error.URLError, OSError, ValueError) as e:
        raise SystemExit("FEHLER: Bestand von " + url + " nicht abfragbar: " + str(e))
    _dokumente = docs_by_ref
    return docs_by_ref


_bestand = None


def bestand_vom_server():
    """document_ref -> published, abgeleitet aus dem einmal geholten Bestand."""
    global _bestand
    if _bestand is None:
        _bestand = {ref: (d.get("published") or NIE)
                    for ref, d in dokumente_vom_server().items()}
    return _bestand


def chapter_state(pub, name):
    path = kapitel_pfad(name)
    if path is None or not path.exists():
        return "fehlt", path
    fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
    if (fm_scalar(fm, "hennibock_skip") or "").lower() == "true":
        return "skip", path
    ref = fm_scalar(fm, "hennibock_ref")
    # Ohne Identitaet kann das Kapitel nicht auf dem Server liegen. Mit einer
    # ist erst die Abfrage entscheidend: eine UUID traegt auch ein Kapitel, das
    # bisher nur als Verweisziel einer Publikation angelegt wurde.
    if ref and ref in bestand_vom_server():
        return "publiziert", path
    return "offen", path


# "Noch nie bedient" sortiert vor jedem echten Datum.
NIE = "0000-00-00"


def last_served(pub):
    """Datum, an dem diese Publikation zuletzt ein Kapitel bekommen hat.

    Aus dem Bestand des Servers, nicht aus dem Frontmatter. Ein Datum in der
    Notiz sagt nur, dass dort einmal publiziert wurde, nicht dass es noch steht:
    nach dem Zuruecksetzen der Instanz meldete eine Strecke ohne ein einziges
    Dokument auf dem Server, sie sei heute bedient worden, und haette damit die
    Rotation an sich gezogen.
    """
    bestand = bestand_vom_server()
    dates = []
    for name in pub["chapters"]:
        path = kapitel_pfad(name)
        if path is None or not path.exists():
            continue
        fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        ref = fm_scalar(fm, "hennibock_ref")
        if ref and ref in bestand:
            dates.append(bestand[ref])
    return max(dates) if dates else NIE


def first_open(pub):
    """Erstes offenes Kapitel dieser Publikation in Inhaltsverzeichnis-Reihenfolge."""
    for name in pub["chapters"]:
        state, path = chapter_state(pub, name)
        if state not in ("skip", "publiziert"):
            return name, path
    return None, None


def pick():
    """Reihum: dran ist die Publikation, die am laengsten nichts bekommen hat.

    Gleichstand loest hennibock_queue auf. Publikationen ohne offenes Kapitel
    fallen raus, die Rotation ueberspringt eine durchgelaufene Strecke von
    selbst.
    """
    kandidaten = []
    for pub in load_queue():
        name, path = first_open(pub)
        if name is None:
            continue
        kandidaten.append((last_served(pub), pub["queue"], pub, name, path))
    if not kandidaten:
        return None
    kandidaten.sort(key=lambda k: (k[0], k[1]))
    return kandidaten[0]


def cmd_next():
    gewaehlt = pick()
    if gewaehlt is None:
        print(json.dumps({"chapter": None,
                          "message": "Warteschlange leer, alles publiziert."},
                         ensure_ascii=False, indent=2))
        return 0
    served, _q, pub, name, path = gewaehlt
    print(json.dumps({
        "publication": pub["name"],
        "pubfile": pub["pubfile"],
        "queue": pub["queue"],
        "zuletzt_bedient": None if served == NIE else served,
        "hennibock_type": pub["chapter_type"],
        "hennibock_areas": pub["areas"],
        "chapter": name,
        "path": str(path.relative_to(VAULT)),
        "position": pub["chapters"].index(name) + 1,
        "of": len(pub["chapters"]),
        "audit": audit_chapter(path),
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_attached(argv):
    """Prueft nach dem Publizieren, ob das Kapitel in seiner Publikation haengt.

    Die Pruefung selbst steht seit dem 22.08.2026 in hennibock-publish und wird
    hier nur noch gerufen. Sie gehoert an die Engstelle, durch die jeder
    Publish laeuft, und sie stand hier in einer zweiten Fassung mit zwei
    Annahmen: die Pub-Datei liege im selben Ordner wie das Kapitel, und ein
    Kapitel heisse "Kap - ...". Beides gilt nur fuer einen der beiden Vaults.
    Im anderen liegen die Texte weit weg von ihrer Pub-Datei und heissen
    anders, und dort meldete diese Pruefung jedes Kapitel als nicht im
    Verzeichnis stehend -- also gerade dort nichts, wo sie gebraucht wurde.

    hennibock-publish prueft ausserdem nach jedem eigenen Import selbst und
    zieht eine Publikation nach, der der Punkt fehlt. Dieser Aufruf ist damit
    die zweite Ansicht auf denselben Befund und in aller Regel eine
    Bestaetigung. Das Befund-Vokabular ist unveraendert.
    """
    if not argv:
        print("FEHLER: Pfad der Kapitelnotiz fehlt.", file=sys.stderr)
        return 2
    skript = Path(__file__).resolve().parents[3] / "bin" / "hk-publish"
    if not skript.is_file():
        print("FEHLER: `hk-publish` fehlt unter " + str(skript)
              + ". Ohne es gibt es weder Publish noch Pruefung.",
              file=sys.stderr)
        return 2
    return subprocess.run([sys.executable, str(skript), "attached", argv[0],
                           "--ablage", str(VAULT)], text=True).returncode


def cmd_queue():
    pubs = load_queue()
    if not pubs:
        print("FEHLER: keine Publikation traegt hennibock_queue.", file=sys.stderr)
        return 1
    gewaehlt = pick()
    dran = gewaehlt[2]["name"] if gewaehlt else None
    for pub in pubs:
        counts = {"offen": 0, "publiziert": 0, "skip": 0, "fehlt": 0}
        for name in pub["chapters"]:
            counts[chapter_state(pub, name)[0]] += 1
        served = last_served(pub)
        marke = "  <== als naechstes dran" if pub["name"] == dran else ""
        print(f"[{pub['queue']}] {pub['name']}{marke}")
        print(f"     Kapiteltyp {pub['chapter_type']}, Bereiche {', '.join(pub['areas']) or '<keine>'}")
        print(f"     zuletzt bedient: {'noch nie' if served == NIE else served}")
        print(f"     {len(pub['chapters'])} Kapitel im Inhaltsverzeichnis: "
              f"{counts['publiziert']} publiziert, {counts['offen']} offen, "
              f"{counts['fehlt']} ohne Datei, {counts['skip']} uebersprungen")
    if gewaehlt:
        print(f"\nRotation: dran ist die Publikation, die am laengsten nichts "
              f"bekommen hat.\nNaechstes Kapitel: {strip_praefix(gewaehlt[3])}")
    return 0


def main():
    argv = sys.argv[1:]
    # `--ablage <pfad>` gilt wie in jedem Werkzeug des Harness. Es wird hier
    # von Hand aus der Liste genommen, weil `attached` seine restlichen
    # Argumente selbst auswertet.
    ablage_arg = None
    if "--ablage" in argv:
        i = argv.index("--ablage")
        if i + 1 >= len(argv):
            print("FEHLER: --ablage braucht einen Pfad", file=sys.stderr)
            return 2
        ablage_arg = argv[i + 1]
        del argv[i:i + 2]
    if not argv or argv[0] not in ("next", "queue", "attached"):
        print(__doc__)
        return 2
    setze_ablage(ablage_arg or os.environ.get("HKB_PATH"))
    if argv[0] == "attached":
        return cmd_attached(argv[1:])
    return cmd_next() if argv[0] == "next" else cmd_queue()


if __name__ == "__main__":
    sys.exit(main())
