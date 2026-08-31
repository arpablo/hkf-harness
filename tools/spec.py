#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Haelt die Kopie unter spec/ mit dem Spezifikations-Repository gleich.

Der Harness fuehrt die Spezifikation als Kopie, nicht als Submodul: Welche
Fassung er umsetzt, muss aus seiner Auslieferung hervorgehen. Der Preis ist,
dass die Kopie veralten kann, ohne dass es jemand merkt — dagegen steht dieses
Skript.

    python3 tools/spec.py            berichtet, ob die Kopie stimmt
    python3 tools/spec.py --update   holt den Stand des Repositorys

Gefunden wird die Quelle ueber HKF_SPEC, sonst neben diesem Repository.
Ohne Quelle endet der Lauf mit 0 und sagt es — ein Klon des Harness soll
sich nicht daran stoeren, dass das Spec-Repository nicht danebenliegt.
"""
import io, os, re, shutil, sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIEL = os.path.join(WURZEL, "spec")

# Unter dem Python des Harness laufen. `hkf` wird allein dafuer geholt: Der
# Import startet den Prozess unter der venv neu, wenn er nicht schon darunter
# laeuft. Das Paket selbst braucht dieses Skript nicht — welche Fassung der
# Harness umsetzt, liest `unsere()` aus der Datei. Es vergleicht Dateien, also
# soll es auch hier die Datei lesen und nicht ein Modul, das laengst geladen
# sein koennte.
sys.path.insert(0, os.path.join(WURZEL, "lib"))
import hkf                                                 # noqa: E402,F401


def quelle():
    if os.environ.get("HKF_SPEC"):
        kandidaten = [os.environ["HKF_SPEC"]]
    else:
        kandidaten = [os.path.join(WURZEL, "..", n)
                      for n in ("HenniHKF-Spec", "hkf-spec")]
    for k in kandidaten:
        if os.path.isfile(os.path.join(k, "README.md")) and \
           any(f.startswith("HKF-Core-V") for f in os.listdir(k)):
            return os.path.abspath(k)
    return None


def dateien(q):
    """[(name, quellpfad)] — die Spezifikationen und das Schema."""
    aus = []
    for f in sorted(os.listdir(q)):
        if re.match(r"^HKF-(Core|Config)-V\d+\.\d+\.md$", f):
            aus.append((f, os.path.join(q, f)))
    schema = os.path.join(q, "schema")
    if os.path.isdir(schema):
        for f in sorted(os.listdir(schema)):
            if f.endswith(".schema.json"):
                aus.append((f, os.path.join(schema, f)))
    return aus


def kernfassung(namen):
    for n in namen:
        m = re.match(r"^HKF-Core-V(\d+\.\d+)\.md$", n)
        if m:
            return m.group(1)
    return None


def unsere():
    text = io.open(os.path.join(WURZEL, "lib", "hkf", "__init__.py"),
                   encoding="utf-8").read()
    m = re.search(r'^CORE = "([^"]+)"', text, re.M)
    return m.group(1) if m else "?"


def main(argv):
    if "--help" in argv or "-h" in argv:
        print(__doc__.strip())
        return 0
    holen = "--update" in argv

    q = quelle()
    if q is None:
        print("Kein Spezifikations-Repository gefunden — spec/ bleibt, wie es ist.")
        print("Setze HKF_SPEC, wenn es woanders liegt.")
        return 0

    liste = dateien(q)
    neu_fassung = kernfassung(n for n, _ in liste)
    print("Quelle:  %s (Core %s)" % (q, neu_fassung))
    print("Harness: Core %s, Python %s aus %s"
          % (unsere(), sys.version.split()[0], os.path.dirname(
              os.path.dirname(sys.executable))))
    print()

    abweichend, fehlend = [], []
    for name, pfad in liste:
        ziel = os.path.join(ZIEL, name)
        if not os.path.exists(ziel):
            zustand, fehlend = "fehlt", fehlend + [name]
        elif io.open(pfad, "rb").read() != io.open(ziel, "rb").read():
            zustand, abweichend = "abweichend", abweichend + [name]
        else:
            zustand = "gleich"
        print("  %-30s %s" % (name, zustand))

    # Nur was aussieht wie eine Auslieferung des Spec-Repositorys zaehlt als
    # verwaist. Alles andere unter spec/ hat jemand mit Absicht dorthin
    # gelegt, und --update ist kein Grund, es wegzuraeumen.
    gehoert_uns = re.compile(r"^(HKF-(Core|Config)-V\d+\.\d+\.md|.*\.schema\.json)$")
    verwaist = [f for f in sorted(os.listdir(ZIEL))
                if gehoert_uns.match(f) and f not in [n for n, _ in liste]]
    for f in verwaist:
        print("  %-30s nicht mehr in der Quelle" % f)
    print()

    if holen:
        for name, pfad in liste:
            shutil.copy2(pfad, os.path.join(ZIEL, name))
        for f in verwaist:
            os.remove(os.path.join(ZIEL, f))
        print("Kopie geholt.")
        if neu_fassung and neu_fassung != unsere():
            print("→ CORE in lib/hkf/__init__.py auf \"%s\" setzen und die Regeln"
                  % neu_fassung)
            print("  nachziehen, die %s ergänzt." % neu_fassung)
            return 1
        return 0

    if not abweichend and not fehlend and not verwaist:
        if neu_fassung and neu_fassung != unsere():
            print("→ Die Dateien stimmen, aber die Quelle ist bei Core %s und der"
                  % neu_fassung)
            print("  Harness bei %s. CORE in lib/hkf/__init__.py nachziehen."
                  % unsere())
            return 1
        print("Der Harness ist auf dem Stand der Spezifikation.")
        return 0
    print("→ python3 tools/spec.py --update holt den Stand.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
