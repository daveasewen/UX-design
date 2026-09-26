#!/usr/bin/env python3
"""R5 / 5a — mutation bites for validate_a2ui.py: a harness that passes everything proves nothing.
Each mutation breaks the dashboard catalogue ONE way (in memory) and the harness must notice.
Seat: $HOME/.r5venv/bin/python notes/_lanes/304/R5/validate_mutations.py  (writes nothing)"""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location("va", os.path.join(os.path.dirname(os.path.abspath(__file__)), "validate_a2ui.py"))
src = open(spec.origin).read().split("res = {\"$spec\"")[0]          # the library half only, not the run
va = {"__file__": spec.origin, "__name__": "va"}; exec(compile(src, spec.origin, "exec"), va)
cat = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "catalogue-dashboard.json")))
def props(c, cid): return c["components"][cid]["allOf"][-1]["properties"]
M = []
c = copy.deepcopy(cat); props(c, "StatCard")["label"] = {"type": "strin"}; M.append(("M1 illegal JSON Schema type", c, "C1"))
c = copy.deepcopy(cat); props(c, "ChartLine")["series"] = {"$ref": "https://a2ui.org/specification/v0_9/common_types.json#/$defs/ChildLst"}; M.append(("M2 dangling $ref into common_types", c, "entry"))
c = copy.deepcopy(cat); c["components"]["StatCard"]["unevaluatedProperties"] = True; M.append(("M3 entry accepts unknown props (E2 must catch)", c, "entry"))
c = copy.deepcopy(cat); props(c, "Button")["component"] = {"const": "Buttn"}; M.append(("M4 discriminator const mismatch", c, "entry"))
c = copy.deepcopy(cat); c["$defs"]["anyComponent"]["oneOf"] = [x for x in c["$defs"]["anyComponent"]["oneOf"] if not x["$ref"].endswith("/KpiTile")]; M.append(("M5 part missing from anyComponent (E3 must catch)", c, "entry"))
for name, c, where in M:
    try:
        r = va["run"](c, name)
        caught = (not r["C1_valid_2020_12_schema"]) or r["entries_valid"] < r["entries_total"]
        detail = "C1=%s entries %d/%d" % (r["C1_valid_2020_12_schema"], r["entries_valid"], r["entries_total"])
    except Exception as e:
        caught, detail = True, "raised %s: %s" % (type(e).__name__, str(e)[:90])
    print("%-50s %s  (%s)" % (name, "CAUGHT" if caught else "NOT CAUGHT", detail))
