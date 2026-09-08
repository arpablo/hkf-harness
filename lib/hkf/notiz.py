# -*- coding: utf-8 -*-
"""Frontmatter aendern, ohne den Rest umzuschreiben.

Ein Import fasst wenige Properties an — `bundles`, die drei Zeitangaben,
`related`. Alles andere soll Zeichen fuer Zeichen so bleiben, wie es kam. Wer
eine Notiz durch einen YAML-Serialisierer schickt, bekommt sie anders
formatiert zurueck, und der Textunterschied zeigt dann Aenderungen, die keine
sind.
"""
import datetime
import io
import re

TRENNER = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)


CODE = re.compile(r"```.*?```|~~~.*?~~~|`[^`\n]*`", re.S)


def ausserhalb_code(text, fn):
    """`fn` auf alles anwenden, was nicht in Backticks steht.

    Was dort steht, ist ein Beispiel und kein Verweis. Eine Typdefinition
    zeigt Wikilinks als Muster her, und ein Clipping bringt die fremden
    Wikilinks der erfassten Seite mit — beide umzuschreiben verfaelschte sie.
    `pruefen.ohne_code` haelt es beim Pruefen ebenso.
    """
    aus, stand = [], 0
    for m in CODE.finditer(text):
        aus.append(fn(text[stand:m.start()]))
        aus.append(m.group(0))
        stand = m.end()
    aus.append(fn(text[stand:]))
    return "".join(aus)


def teilen(text):
    """(kopf, body). Ohne Frontmatter ist kopf None."""
    m = TRENNER.match(text)
    return m.groups() if m else (None, text)


def bauen(kopf, body):
    return "---\n%s\n---\n\n%s" % (kopf.strip("\n"), body.lstrip("\n"))


def hat(kopf, key):
    return re.search(r"^%s:" % re.escape(key), kopf, re.M) is not None


def entfernen(kopf, key):
    kopf = re.sub(r"^%s:\n(?:  - .*\n?)+" % re.escape(key), "", kopf, flags=re.M)
    kopf = re.sub(r"^%s:.*\n?" % re.escape(key), "", kopf, flags=re.M)
    return kopf.rstrip("\n")


def lies_liste(kopf, key):
    m = re.search(r"^%s:\n((?:  - .*\n?)+)" % re.escape(key), kopf + "\n", re.M)
    if not m:
        return []
    werte = []
    for z in m.group(1).strip("\n").splitlines():
        w = z.strip()[2:].strip()
        if len(w) > 1 and w[0] == w[-1] and w[0] in "\"'":
            w = w[1:-1]
        werte.append(w)
    return werte


def setze_skalar(kopf, key, wert):
    zeile = "%s: %s" % (key, wert)
    if hat(kopf, key):
        return re.sub(r"^%s:.*$" % re.escape(key), zeile, kopf, count=1, flags=re.M)
    return kopf.rstrip("\n") + "\n" + zeile


def setze_liste(kopf, key, werte):
    """Liste als Block. Wikilinks werden gequotet, weil `[` YAML sonst als
    Flow-Folge liest (§3.4)."""
    if not werte:
        return entfernen(kopf, key)
    zeilen = ["%s:" % key]
    for w in werte:
        zeilen.append('  - "%s"' % w if w.startswith("[[") else "  - %s" % w)
    neu = "\n".join(zeilen)
    if hat(kopf, key):
        kopf = entfernen(kopf, key)
    return kopf.rstrip("\n") + "\n" + neu


def abschnitt(body, ueberschrift):
    """(text des Abschnitts ohne Ueberschrift, oder None)."""
    m = re.search(r"^# %s\n(.*?)(?=^# |\Z)" % re.escape(ueberschrift), body, re.M | re.S)
    return m.group(1) if m else None


def ohne_abschnitt(body, ueberschrift):
    return re.sub(r"^# %s\n.*?(?=^# |\Z)" % re.escape(ueberschrift), "",
                  body, flags=re.M | re.S)


# Was eine eigene Struktur beginnt und darum nie an die vorige Zeile
# angehaengt wird (§3.3). `---` steht dabei fuer eine Trennlinie im Body; das
# Frontmatter liegt ausserhalb.
STRUKTUR = re.compile(r"^(#{1,6} |[-*+] |\d+[.)] |\||>|```|~~~|---\s*$)")
# Ein Listenpunkt und ein Zitat nehmen eine Fortsetzungszeile auf, eine
# Ueberschrift oder Tabellenzeile nicht.
NIMMT_AUF = re.compile(r"^([-*+] |\d+[.)] |>)")
ZAHLPUNKT = re.compile(r"^\d+[.)] ")
# Woran ein abgeschlossener Satz endet. Der Gedankenstrich zaehlt dazu: Er
# kuendigt oefter eine Liste an, als dass er einen Umbruch hinterlaesst.
ABGESCHLOSSEN = (".", "!", "?", ":", ";", ")", "]", '"', "'", "\u00bb",
                 "\u201c", "\u201d", "\u2014", "*")
ZAUN = ("```", "~~~")


def _fortsetzung(zeile, vorige):
    """Ob eine Zahl mit Punkt am Zeilenanfang die vorige Zeile fortsetzt.

    `10. Maerz schlug es um` sieht fuer Markdown aus wie der zehnte Punkt
    einer Liste und ist doch der Rest eines Satzes, den ein Umbruch
    zerschnitten hat. In der Anzeige wird daraus eine nummerierte Liste, die
    bei zehn beginnt. Entschieden wird an der vorigen Zeile: Ein Listenpunkt
    folgt auf eine Leerzeile, auf eine Struktur oder auf einen abgeschlossenen
    Satz, eine Fortsetzung auf einen offenen.
    """
    if not ZAHLPUNKT.match(zeile.lstrip()):
        return False
    vorige = vorige.rstrip()
    if not vorige or STRUKTUR.match(vorige.lstrip()):
        return False
    return not vorige.endswith(ABGESCHLOSSEN)


def entfalten(body):
    """(entfalteter Body, Zeilennummern der angehaengten Zeilen).

    Ein Absatz ist eine Zeile (§3.3). Angefasst wird allein Fliesstext: Was
    eine eigene Struktur beginnt, bleibt stehen, eine Leerzeile bleibt
    Absatzgrenze, und in einem Codeblock wird nichts veraendert. Eine
    eingerueckte Fortsetzungszeile gehoert zu ihrem Listenpunkt.

    Die Nummern zaehlen ab 1 im Body und sagen, wo ein Absatz umbrochen war.
    """
    aus, nummern, im_code = [], [], False
    for nr, zeile in enumerate(body.split("\n"), 1):
        blank = zeile.strip() == ""
        if zeile.lstrip().startswith(ZAUN):
            im_code = not im_code
            aus.append(zeile)
        elif im_code or blank or not aus or aus[-1].strip() == "":
            aus.append(zeile)
        elif STRUKTUR.match(zeile.lstrip()) and not _fortsetzung(zeile, aus[-1]):
            aus.append(zeile)
        elif STRUKTUR.match(aus[-1].lstrip()) and not NIMMT_AUF.match(aus[-1].lstrip()):
            aus.append(zeile)
        else:
            aus[-1] = aus[-1].rstrip() + " " + zeile.strip()
            nummern.append(nr)
    return "\n".join(aus), nummern


def gebrochene_verweise(body):
    """Zeilennummern, in denen ein Wikilink offen bleibt (§3.3).

    Ein `[[` ohne `]]` in derselben Zeile heisst, dass der Verweis ueber einen
    Umbruch reicht. Er erfuellt §3.6 buchstaeblich und loest doch nicht auf.
    """
    aus, im_code, offen = [], False, 0
    for nr, zeile in enumerate(body.split("\n"), 1):
        if zeile.lstrip().startswith(ZAUN):
            im_code = not im_code
            continue
        if im_code:
            continue
        vorher = offen
        offen = max(0, offen + zeile.count("[[") - zeile.count("]]"))
        # Gemeldet wird die Zeile, in der der Verweis aufgeht — nicht die, in
        # der er sich schliesst.
        if offen and not vorher:
            aus.append(nr)
    return aus


LINKWERT = re.compile(r"^\[\[([^\]|]+)(?:\|([^\]]*))?\]\]$")


def linkziel(wert):
    """Das Ziel, wenn der Wert genau ein Wikilink ist — sonst None.

    Fuer Properties, die zwei Schreibweisen zulassen: `type` traegt den
    Typnamen als Text oder einen Verweis auf eine Typseite (§3.3).
    """
    m = LINKWERT.match(str(wert if wert is not None else "").strip())
    return m.group(1) if m else None


def skalar(wert):
    """Ein Wert so, dass YAML ihn wieder als denselben Text liest.

    `version: 1.0` ist eine Zahl, `version: "1.0"` ist Text — und §4.1 meint
    Text. Wer eine Fassung ohne Anfuehrungszeichen schreibt, macht aus 1.10
    spaeter 1.1.
    """
    text = str(wert)
    try:
        import yaml
        gleich = yaml.safe_load(text) == text
    except Exception:                                  # pragma: no cover
        gleich = False
    if gleich or "\n" in text:
        return text
    return '"%s"' % text.replace('\\', '\\\\').replace('"', '\\"')


def sichern(pfad, kopf, body, werkzeug):
    """Schreiben und die Aenderung hinschreiben (Core §3.3, Regel 5).

    Wer aendert, schreibt hin, dass er geaendert hat: `modified` auf jetzt in
    UTC, `modified_by` auf den Namen des Werkzeugs. Die Zeile stand zweimal in
    `bin/`, und zwei Fassungen derselben Regel laufen irgendwann auseinander.

    Gibt das Datum zurueck, damit ein Aufrufer es in seinen Bericht nehmen
    kann, ohne es ein zweites Mal zu bilden.
    """
    jetzt = datetime.datetime.now(datetime.timezone.utc)
    kopf = setze_skalar(kopf, "modified",
                        skalar(jetzt.strftime("%Y-%m-%dT%H:%M:%S")))
    kopf = setze_skalar(kopf, "modified_by", werkzeug)
    io.open(pfad, "w", encoding="utf-8").write(bauen(kopf, body))
    return jetzt.strftime("%Y-%m-%d")
