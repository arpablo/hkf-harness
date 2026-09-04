#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sagt zu Beginn einer Sitzung, wo gearbeitet wird und welche Regeln gelten.

Bis hierher gab es dafuer einen Generator, der aus einem Manifest eine
`CLAUDE.md` in den Vault schrieb, dazu Agentenfassungen, Hook-Eintraege und
Skill-Zeiger. Das waren acht erzeugte Artefakte, die auseinanderlaufen konnten,
in einer Ablage, die nach §4 keine Werkzeugdatei tragen soll.

Ein Hook braucht davon nichts. Er liest die Wurzeldatei, setzt zusammen und
gibt den Text als Sitzungskontext zurueck. **In der Ablage entsteht dabei
nichts.** Ein fremder Vault bleibt unangetastet.

Vier Schichten, in dieser Reihenfolge:

    1. wer hier arbeitet und wie zusammengearbeitet wird  (core/)
    2. die Stimme, die die Wurzeldatei unter `voice` nennt (profiles/voices/)
    3. was **diese** Ablage fuer sich festgelegt hat       (`hint`-Notizen, §7)
    4. welche Ablage aktiv ist und woher ihr Pfad kommt

Ist keine Ablage gewaehlt und liegt die Sitzung nicht in einer, zaehlt der Hook
auf, was zur Wahl steht. Geraten wird nicht.
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import gemeinsam   # noqa: E402
from hkf import CORE, ablage, frontmatter   # noqa: E402

WURZEL = gemeinsam.WURZEL
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


def main():
    e = gemeinsam.ereignis()
    wo = gemeinsam.arbeitsverzeichnis(e)
    pfad, art, kopf = lage(wo)

    teile = [kopf]
    if art:
        text, kennung = stimme(pfad)
        teile.append("Die Werkzeuge stehen in `bin/`, die Regeln in den Skills "
                     "`hkf:hkb…`. HKF Core %s." % CORE)
        teile += kanon()
        teile.append(text or (
            "# Stimme\n\nDie Wurzeldatei nennt `%s`, der Harness führt kein "
            "solches Profil." % kennung))
        eigene = _gekuerzt(hinweise(pfad))
        if eigene:
            teile.append("# Was diese Ablage für sich festgelegt hat\n\n"
                         "Das geht dem Vorstehenden vor, wo es sich berührt.")
            teile += eigene
    else:
        teile += kanon()

    text = "\n\n".join(t for t in teile if t).strip()
    kurz = ("%s (%s)" % (ablage.name_von(pfad), ablage.ARTNAME[art])
            if art else "keine Ablage gewählt")
    return gemeinsam.kontext(text, "HKF: " + kurz)


if __name__ == "__main__":
    sys.exit(main())
