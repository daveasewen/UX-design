#!/usr/bin/env python3
"""305 B2 — write-free copy of _build_integrity.py's SCHEMA check (1): every components/*.meta.json
against meta.schema.json, Draft7, same resolver. Prints pass count and every error; --json OUT saves them."""
import glob, json, os, sys
import jsonschema
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "knowledge"))
COMP = os.path.join(ROOT, "components")
schema = json.load(open(os.path.join(COMP, "meta.schema.json")))
v = jsonschema.Draft7Validator(schema, resolver=jsonschema.RefResolver(base_uri="", referrer=schema))
metas = sorted(f for f in glob.glob(os.path.join(COMP, "*.meta.json"))
               if not os.path.basename(f).startswith("EXAMPLE") and os.path.basename(f) != "meta.schema.json")
out, ok = {}, 0
for f in metas:
    d = json.load(open(f))
    errs = sorted(v.iter_errors(d), key=lambda e: list(e.path))
    if errs:
        out[os.path.basename(f)] = ["/".join(map(str, e.path)) + ": " + e.message[:140] for e in errs]
    else:
        ok += 1
print("schema valid: %d/%d" % (ok, len(metas)))
for k, es in out.items():
    for e in es: print("  %s  %s" % (k, e))
if "--json" in sys.argv:
    json.dump({"valid": ok, "total": len(metas), "errors": out}, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
