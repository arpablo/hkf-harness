# -*- coding: utf-8 -*-
"""Was zu Beginn gilt: die Lage, der Kanon, die Stimme, die Hinweise.

Der SessionStart-Hook braucht diesen Text, und ein Subagent braucht ihn auch —
er laeuft in seinem eigenen Kontext, und was die Sitzung bekommen hat, sieht er
nicht. Deshalb steht die Zusammensetzung hier und nicht im Hook. `hk-kontext`
gibt sie auf der Kommandozeile aus.
"""
import io
import os
import re

from . import CORE, ablage, frontmatter

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.realpath(__file__))))
KANON = ("identitaet.md", "zusammenarbeit.md", "deutsche-sprache.md",
         "schreibregeln.md", "yaml.md")
VORGABE_STIMME = "henni-knowledge"
# Eine Hinweisnotiz ist so lang, wie sie sein muss. Der Sitzungskontext ist es
# nicht: Was hier steht, kostet in jeder Sitzung, auch wenn es nie gebraucht
# wird. Der Kanon ist bekannt und begrenzt, die Hinweise sind es nicht — also
# gilt die Grenze fuer sie.
HOECHSTENS = 6000


def _ohne_frontmatter(text):
    if not text.startswith("---"):
        return text.strip()
    ende = text.find("\n---", 3)
    return text if ende == -1 else text[ende + 4:].strip()


def _lies(pfad):
    try:
        return io.open(pfad, encoding="utf-8").read().strip()
    except OSError:
        return ""


def kanon():
    aus = []
    for name in KANON:
        text = _lies(os.path.join(WURZEL, "core", name))
        if text:
            aus.append(text)
    return aus


def stimme(pfad):
    """Der Text des Profils, das die Wurzeldatei nennt."""
    try:
        daten, _ = frontmatter.lesen(ablage.wurzeldatei(pfad))
    except Exception:
        daten = {}
    kennung = str(daten.get("voice") or VORGABE_STIMME).strip()
    if not re.fullmatch(r"[a-z][a-z0-9-]*", kennung):
        return "", kennung
    datei = os.path.join(WURZEL, "profiles", "voices", kennung + ".md")
    return _ohne_frontmatter(_lies(datei)), kennung


def hinweise(pfad):
    """Die `hint`-Notizen der Ablage, ohne Frontmatter (Harness §7)."""
    ordner = ablage.hinweise(pfad)
    if not os.path.isdir(ordner):
        return []
    aus = []
    for name in sorted(os.listdir(ordner)):
        if not name.endswith(".md"):
            continue
        text = _ohne_frontmatter(_lies(os.path.join(ordner, name)))
        if text:
            aus.append(text)
    return aus


def _gekuerzt(notizen):
    """Die Hinweise bis zur Grenze, danach ein Verweis statt des Textes."""
    aus, laenge = [], 0
    for i, text in enumerate(notizen):
        if laenge + len(text) > HOECHSTENS:
            aus.append("(%d weitere Hinweisnotizen stehen in `%s`.)"
                       % (len(notizen) - i, ablage.HINWEISE))
            break
        aus.append(text)
        laenge += len(text)
    return aus


def lage(wo):
    """Die Kopfzeilen: welche Ablage, welche Art, woher der Pfad."""
    pfad, woher = ablage.aufloesen(wo=wo)
    art = ablage.art_von(pfad)
    if art:
        return pfad, art, "\n".join([
            "# Die Ablage dieser Sitzung",
            "",
            "%s — %s „%s“." % (pfad, ablage.ARTNAME[art], ablage.name_von(pfad)),
            "Der Pfad kommt aus %s. `hk-ablage` zeigt und ändert die Wahl."
            % woher,
        ])

    zeilen = ["# Es ist keine Ablage gewählt", "",
              "%s ist keine Ablage, und der Pfad kommt aus %s." % (pfad, woher)]
    kandidaten = ablage.daneben(wo) or ablage.bekannt()
    if kandidaten:
        zeilen += ["", "Zur Wahl steht:", ""]
        zeilen += ["- `%s` — %s „%s“" % (p, ablage.ARTNAME[a], n)
                   for p, n, a in kandidaten]
        zeilen += ["", "**Frag nach, statt eine zu nehmen.** Steht die Wahl "
                        "fest: `hk-ablage <pfad>`."]
    else:
        zeilen += ["", "Hier liegt keine. `hk-init <ziel>` legt eine an."]
    return pfad, None, "\n".join(zeilen)


def zusammensetzen(wo=None, teile_gewuenscht=("lage", "kanon", "stimme",
                                              "hinweise")):
    """(text, pfad, art) — der Kontext, aus dem gewaehlt wird, was gebraucht ist."""
    pfad, art, kopf = lage(wo)
    teile = []
    if "lage" in teile_gewuenscht:
        teile.append(kopf)
    if art and "lage" in teile_gewuenscht:
        teile.append("Die Werkzeuge stehen in `bin/`, die Regeln in den Skills "
                     "`hkf:hkb…`. HKF Core %s." % CORE)
    if "kanon" in teile_gewuenscht:
        teile += kanon()
    if art and "stimme" in teile_gewuenscht:
        text, kennung = stimme(pfad)
        teile.append(text or (
            "# Stimme\n\nDie Wurzeldatei nennt `%s`, der Harness führt kein "
            "solches Profil." % kennung))
    if art and "hinweise" in teile_gewuenscht:
        eigene = _gekuerzt(hinweise(pfad))
        if eigene:
            teile.append("# Was diese Ablage für sich festgelegt hat\n\n"
                         "Das geht dem Vorstehenden vor, wo es sich berührt.")
            teile += eigene
    return "\n\n".join(t for t in teile if t).strip(), pfad, art
