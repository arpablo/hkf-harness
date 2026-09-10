# -*- coding: utf-8 -*-
"""Was die Werkzeuge an einer Quellennotiz gemeinsam brauchen.

`hk-tranchen` fuehrt den Stand des Lesens, `hk-lesekarte` den Stand der
Entitaeten, `hk-extrakt` das Evidenzjournal. Alle drei bekommen eine
Quellennotiz als Argument und muessen sie erst einmal als eine erkennen, und
zwar auch dann, wenn `type` in der Linkform steht und erst ueber eine Typseite
auf `source` fuehrt (Core §3.3). Das stand zweimal da, bis es hier landete.

Ihre Arbeitszettel liegen am selben Ort, und `arbeitszettel()` sagt, wo.
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


DASHBOARD = "AgentDashboard"


def arbeitszettel(quellpfad, name):
    """Wo ein Arbeitszettel zu dieser Quellennotiz liegt.

    Prozesszustand ist kein Inhalt. Er liegt darum nicht in der Quellennotiz,
    sondern unter `<inbox_base>/AgentDashboard/`. Dieser Bereich ist der
    einzige, den Core ausdruecklich von der Pruefung ausnimmt: „Unsortiertes,
    von HKF nicht geprueft" (§3.2.6). Genau dorthin gehoert ein Zettel, den
    niemand liest und der keine Aussage ueber den Gegenstand macht.

    `name` traegt ein `%s` fuer den Stamm der Quellennotiz, etwa
    `"lesekarte-%s.yaml"`. Eine Lieferung hat keine Bereiche (§4), dort gilt
    die Vorgabe `00-Inbox`.
    """
    wurzel = ablage.aufwaerts(os.path.dirname(os.path.abspath(quellpfad)))
    if not wurzel:
        raise Fehler("%s liegt in keiner Ablage (§3.1)." % quellpfad)
    try:
        inbox = ablage.bereiche(wurzel)["inbox_base"]
    except Exception:
        inbox = ablage.VORGABEN["inbox_base"]
    stamm = os.path.basename(quellpfad)[:-3]
    return os.path.join(wurzel, inbox or ablage.VORGABEN["inbox_base"],
                        DASHBOARD, name % stamm)
