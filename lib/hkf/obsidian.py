# -*- coding: utf-8 -*-
"""Die Obsidian-CLI ansprechen.

Sie kann, was kein Werkzeug hier kann: Obsidian haelt den Vault im Speicher,
mit aufgeloesten Verweisen und ausgewerteten Bases. Was sie nicht kann, ist
sich wie ein Unix-Programm verhalten, und dieses Modul faengt genau das ab.
Vier Eigenschaften, an jeder Aufrufstelle einzeln dieselben Fehler:

**Der Exit-Code traegt nichts.** Ein unbekannter Befehl, ein fehlender
Pflichtparameter, eine nicht gefundene Datei — alles endet mit 0 und einer
Zeile Text. Geprueft wird deshalb die Ausgabe: Was mit `Error:` beginnt, ist
ein Fehlschlag.

**Ein falscher Parameterwert wird stillschweigend uebergangen.**
`obsidian vault info=quatsch` liefert die volle Auskunft, als waere nichts
gewesen. Wer sich auf einen Parameter verlaesst, prueft besser das Ergebnis.

**`vault=` gilt nur an erster Stelle**, vor dem Befehl. Steht es dahinter,
greift klaglos der zuletzt benutzte Vault — und der Aufruf liefert richtig
aussehende Daten aus der falschen Ablage. Das ist der gefaehrlichste der vier.

**Ein Aufruf startet die App, wenn sie nicht laeuft.** Auf einem Rechner ohne
Bildschirm wartet er stattdessen bis ins Zeitlimit. Darum wird vorher gefragt,
und gestartet wird nur, wer ausdruecklich darum bittet.

Dazu die fuenfte, die keine Eigenschaft der CLI ist, sondern eine des
Zusammenspiels: **Leer und kaputt sehen gleich aus.** `base:query` auf eine
Base, die es nicht gibt, liefert dasselbe wie eine Base ohne Treffer. Wo es
geht, stellt dieses Modul deshalb eine Kontrollfrage, deren Antwort bekannt
ist, und macht aus dem stillen Nichts einen Fehlschlag.
"""
import json, os, shutil, subprocess

# **Es sind zwei Programme, und nur eines taugt.** Im App-Bundle liegen
# `obsidian-cli` und `obsidian` nebeneinander. Sie fuehren dieselben 105
# Befehle und antworten auf viele gleich — aber `obsidian` fuehrt einen Teil
# davon stillschweigend nicht aus: `search` liefert dort fuer jede Anfrage
# null Zeilen, waehrend `obsidian-cli` in derselben Ablage 125 findet. Kein
# Fehler, keine Meldung, Exit 0. Darum steht `obsidian-cli` hier zuerst, und
# `obsidian` bleibt nur der Rueckfall.
NAMEN = ("obsidian-cli", "obsidian")
RUMPF = "%s/Contents/MacOS/%%s"
ORTE = tuple(RUMPF % b % n
             for n in NAMEN
             for b in ("/Applications/Obsidian.app",
                       os.path.expanduser("~/Applications/Obsidian.app")))

# Ein Aufruf gegen die laufende App ist eine Sache von Millisekunden. Das
# Limit faengt den Fall ab, dass sie gerade startet oder haengt.
ZEITLIMIT = 20
# Der erste Aufruf darf die App hochfahren; das dauert laenger als alles Uebrige.
ZEITLIMIT_START = 90


class Fehlschlag(Exception):
    """Die CLI hat nicht geliefert, was verlangt war."""


def programm():
    """Pfad zur CLI, oder None. `obsidian-cli` geht vor (siehe NAMEN)."""
    for name in NAMEN:
        gefunden = shutil.which(name)
        if gefunden:
            return gefunden
    return next((p for p in ORTE if os.path.isfile(p)), None)


def laeuft():
    """Laeuft die App? Ohne sie beantwortet die CLI nichts.

    `-i` ist noetig und nicht Bequemlichkeit: Der Hauptprozess heisst je nach
    Fassung und Startweg `Obsidian` oder `obsidian`. Ein Vergleich auf eine
    der beiden Schreibweisen meldet die laufende App als nicht vorhanden, und
    der Aufrufer startet dann eine zweite.
    """
    return subprocess.run(["pgrep", "-ix", "obsidian"],
                          capture_output=True).returncode == 0


def ruf(befehl, *parameter, **kw):
    """Einen Befehl absetzen und seine Ausgabe zurueckgeben.

        ruf("bases", vault="HenniHKF-Core")
        ruf("base:query", 'path=90-System/Bases/Person.base', "format=json",
            vault="HenniHKF-Core")

    `vault` wandert vor den Befehl, weil es nur dort wirkt. `starten=True`
    laesst zu, dass der Aufruf die App hochfaehrt.
    """
    vault = kw.pop("vault", None)
    starten = kw.pop("starten", False)
    zeitlimit = kw.pop("zeitlimit", None)
    if kw:
        raise TypeError("unbekannte Argumente: %s" % ", ".join(sorted(kw)))

    prog = programm()
    if not prog:
        raise Fehlschlag("Die Obsidian-CLI ist nicht da. Auf dem Mac liegt sie "
                         "in /Applications/Obsidian.app/Contents/MacOS/obsidian.")
    if not laeuft():
        if not starten:
            raise Fehlschlag("Obsidian läuft nicht. Die CLI beantwortet ohne "
                             "die App nichts; ein Aufruf würde sie starten.")
        zeitlimit = zeitlimit or ZEITLIMIT_START
    zeitlimit = zeitlimit or ZEITLIMIT

    argv = [prog]
    if vault:
        argv.append("vault=%s" % vault)      # nur an erster Stelle wirksam
    argv.append(befehl)
    argv.extend(parameter)
    try:
        r = subprocess.run(argv, capture_output=True, text=True,
                           timeout=zeitlimit)
    except subprocess.TimeoutExpired:
        raise Fehlschlag("`%s` hat nach %g Sekunden nicht geantwortet."
                         % (befehl, zeitlimit))
    aus = (r.stdout or "") + (r.stderr or "")
    for zeile in aus.splitlines():
        # Der Exit-Code ist auch hier 0. Die Zeile ist das ganze Signal.
        if zeile.startswith("Error:"):
            raise Fehlschlag("%s: %s" % (befehl, zeile[len("Error:"):].strip()))
    return aus.strip("\n")


def vaults(starten=False):
    """{name: absoluter Pfad} der Vaults, die Obsidian kennt."""
    aus = {}
    for zeile in ruf("vaults", "verbose", starten=starten).splitlines():
        if "\t" in zeile:
            name, pfad = zeile.split("\t", 1)
            aus[name.strip()] = pfad.strip()
    return aus


def vault_fuer(pfad, starten=False):
    """(vaultname, praefix) fuer eine Ablage, oder (None, None).

    Eine Wissensbasis darf in einem Unterverzeichnis ihres Vaults liegen
    (Core §3.1). Gesucht wird deshalb der Vault, unter dem sie liegt, und der
    laengste Treffer gewinnt: Ein verschachtelter Vault ist naeher dran als
    der darueber. Der Rest des Weges ist genau der Ablagepfad, den jeder
    qualifizierte Verweis vor dem Bereich traegt.
    """
    ziel = os.path.realpath(pfad)
    treffer, tiefe = (None, None), -1
    for name, wurzel in vaults(starten=starten).items():
        w = os.path.realpath(wurzel)
        if ziel == w:
            rest = ""
        elif ziel.startswith(w + os.sep):
            rest = os.path.relpath(ziel, w).replace(os.sep, "/")
        else:
            continue
        if len(w) > tiefe:
            treffer, tiefe = (name, rest), len(w)
    return treffer


def bases(vault, starten=False):
    """Die `.base`-Dateien eines Vaults, vault-relativ."""
    aus = ruf("bases", vault=vault, starten=starten)
    return [z.strip() for z in aus.splitlines() if z.strip()]


def base_query(vault, basepfad, view=None, starten=False):
    """Die Zeilen einer Base als Liste von dicts.

    Die Kontrollfrage vorweg: Gibt es die Datei ueberhaupt? Ohne sie waere
    eine Base, die es nicht gibt, von einer ohne Treffer nicht zu
    unterscheiden — beide antworten `[]`.
    """
    if basepfad not in bases(vault, starten=starten):
        raise Fehlschlag("%s führt keine Base %s." % (vault, basepfad))
    argv = ["path=%s" % basepfad, "format=json"]
    if view:
        argv.append("view=%s" % view)
    aus = ruf("base:query", *argv, vault=vault, starten=starten)
    if not aus.strip():
        return []
    try:
        daten = json.loads(aus)
    except ValueError:
        raise Fehlschlag("%s: die Antwort auf base:query ist kein JSON: %s"
                         % (basepfad, aus[:120]))
    return daten if isinstance(daten, list) else [daten]
