# -*- coding: utf-8 -*-
"""Was die Werkzeuge an einer Quellennotiz gemeinsam brauchen.

`hk-tranchen` fuehrt den Stand des Lesens einer grossen Quelle. Es bekommt
eine Quellennotiz als Argument und muss sie erst einmal als eine erkennen,
auch dann, wenn `type` in der Linkform steht und erst ueber eine Typseite auf
`source` fuehrt (Core §3.3).
"""
import io, os

from . import ablage, frontmatter, notiz

QUELLTYP = "source"


class Fehler(Exception):
    pass


def typname(pfad, wert):
    """Der Typ einer Notiz, in Text- wie in Linkform (Core §3.3)."""
    ziel = notiz.linkziel(wert)
    if ziel is None:
        return str(wert or "").strip()
    seite = "/".join(ziel.split("/")[-2:])
    verz = os.path.dirname(os.path.abspath(pfad))
    while True:
        try:
            wurzel, art = ablage.finde_ablage(verz)
        except ablage.KeineAblage:
            eltern = os.path.dirname(verz)
            if eltern == verz:
                return ""
            verz = eltern
            continue
        if art != "hkb":
            return ""
        konfig = os.path.join(wurzel, ablage.bereiche(wurzel)["config_base"])
        return ablage.typseiten(konfig).get(seite, "")


def quellennotiz(pfad):
    """(kopf, body) einer Quellennotiz — sonst `Fehler`."""
    if not os.path.isfile(pfad):
        raise Fehler("%s: keine Datei." % pfad)
    daten, _ = frontmatter.lesen(pfad)
    typ = typname(pfad, daten.get("type"))
    if typ != QUELLTYP:
        raise Fehler("%s: `type` ist %s und nicht `source`. Tranchen und "
                     "Lesekarte führt eine Quellennotiz."
                     % (pfad, typ and "`%s`" % typ or "leer"))
    kopf, body = notiz.teilen(io.open(pfad, encoding="utf-8").read())
    return kopf, body
