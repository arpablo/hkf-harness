# -*- coding: utf-8 -*-
"""Frontmatter gegen spec/hkf-core-1.0.schema.json pruefen.

Das Schema ist die Norm (Core Anhang B.4). Hier steht ein kleiner Auswerter
fuer genau die Schluesselwoerter, die darin vorkommen — type, const, enum,
pattern, minLength, minimum, maximum, minItems, items, required, properties,
additionalProperties, propertyNames, oneOf, allOf, not, $ref. Wer jsonschema
installiert hat, pruefe damit; das Ergebnis muss dasselbe sein.
"""
import io, json, os, re

from . import SCHEMA

TYPEN = {"object": dict, "array": list, "string": str, "number": (int, float),
         "boolean": bool, "null": type(None)}


def laden(pfad=None):
    return json.load(io.open(pfad or SCHEMA, encoding="utf-8"))


def passt_typ(wert, name):
    if name == "number":
        return isinstance(wert, (int, float)) and not isinstance(wert, bool)
    if name == "boolean":
        return isinstance(wert, bool)
    if name == "object":
        return isinstance(wert, dict)
    return isinstance(wert, TYPEN[name])


def pruefen(wert, schema, wurzel, wo=""):
    """Gibt eine Liste von Befunden zurueck. Leer heisst gueltig."""
    if "$ref" in schema:
        ziel = wurzel
        for teil in schema["$ref"].lstrip("#/").split("/"):
            ziel = ziel[teil]
        return pruefen(wert, ziel, wurzel, wo)

    f = []
    if "type" in schema:
        namen = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(passt_typ(wert, n) for n in namen):
            return ["%s: %r ist kein %s" % (wo or ".", wert, "/".join(namen))]
    if "const" in schema and wert != schema["const"]:
        f.append("%s: %r statt %r" % (wo, wert, schema["const"]))
    if "enum" in schema and wert not in schema["enum"]:
        f.append("%s: %r nicht in %s" % (wo, wert, schema["enum"]))
    if "pattern" in schema and isinstance(wert, str):
        if not re.search(schema["pattern"], wert):
            f.append("%s: %r passt nicht auf %s" % (wo, wert, schema["pattern"]))
    if "minLength" in schema and isinstance(wert, str) and len(wert) < schema["minLength"]:
        f.append("%s: leer" % wo)
    if "minimum" in schema and isinstance(wert, (int, float)) and wert < schema["minimum"]:
        f.append("%s: %r < %r" % (wo, wert, schema["minimum"]))
    if "maximum" in schema and isinstance(wert, (int, float)) and wert > schema["maximum"]:
        f.append("%s: %r > %r" % (wo, wert, schema["maximum"]))
    if "minItems" in schema and isinstance(wert, list) and len(wert) < schema["minItems"]:
        f.append("%s: leere Liste" % wo)
    if "items" in schema and isinstance(wert, list):
        for i, x in enumerate(wert):
            f += pruefen(x, schema["items"], wurzel, "%s[%d]" % (wo, i))
    if isinstance(wert, dict):
        for k in schema.get("required", []):
            if k not in wert:
                f.append("%s: %s fehlt" % (wo or ".", k))
        for k, v in wert.items():
            if "propertyNames" in schema:
                f += pruefen(k, schema["propertyNames"], wurzel, "%s/%s (Name)" % (wo, k))
            if k in schema.get("properties", {}):
                f += pruefen(v, schema["properties"][k], wurzel, "%s/%s" % (wo, k))
            elif "additionalProperties" in schema:
                f += pruefen(v, schema["additionalProperties"], wurzel, "%s/%s" % (wo, k))
    if "allOf" in schema:
        for s in schema["allOf"]:
            f += pruefen(wert, s, wurzel, wo)
    if "oneOf" in schema:
        treffer = [s for s in schema["oneOf"] if not pruefen(wert, s, wurzel, wo)]
        if len(treffer) != 1:
            f.append("%s: %r erfuellt keine der %d Formen"
                     % (wo or ".", wert, len(schema["oneOf"])))
    if "not" in schema and not pruefen(wert, schema["not"], wurzel, wo):
        f.append("%s: %r ist ausgeschlossen" % (wo, wert))
    return f


def einstieg(pfad):
    """Welche Form gilt: Wurzeldatei einer HKB, eines Bundles, oder Notiz."""
    name = os.path.basename(pfad)
    return "hkb" if name == "hkb.md" else "hbundle" if name == "hbundle.md" else "notiz"
