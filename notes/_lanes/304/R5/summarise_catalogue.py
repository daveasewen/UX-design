#!/usr/bin/env python3
"""R5 / 5a — derive the validity LEVELS and the per-part gap list from catalogue-report.json +
a2ui-validation.json (both in this lane folder). Writes catalogue-summary.json. System python3.
  L1 A2UI-valid     : the entry passes E1-E3 in validate_a2ui.py (the spec, draft 2020-12)
  L2 honest         : L1 AND the meta passes Apollo's own meta.schema.json AND the part is not deprecated
  L3 run-time ready : L2 AND a `when` AND a data shape that resolves in shapes.json AND status stable
                      AND at least one ruling/rule attached AND it can carry content (a text/number/data
                      prop or a slot)
"""
import json, os
LANE = os.path.dirname(os.path.abspath(__file__))
rep = json.load(open(os.path.join(LANE, "catalogue-report.json")))
val = json.load(open(os.path.join(LANE, "a2ui-validation.json")))
cat = json.load(open(os.path.join(LANE, "catalogue-all.json")))
dash = json.load(open(os.path.join(LANE, "catalogue-dashboard.json")))
CONTENT = ("DynamicString", "DynamicNumber", "DataBinding", "ChildList", "ComponentId")
def carries_content(cid):
    props = cat["components"][cid]["allOf"][-1]["properties"]
    for k, v in props.items():
        if k == "component":
            continue
        blob = json.dumps(v)
        if any(c in blob for c in CONTENT):
            return True
    return False
rows = {}
for cid, e in rep["entries"].items():
    g = set(e["gaps"])
    l1 = val["catalogue-all.json"]["entries"][cid]["valid"]
    l2 = l1 and "G-SCHEMA" not in g and "G-DEPRECATED" not in g
    content = carries_content(cid)
    l3 = l2 and not ({"G-WHEN", "G-SHAPE", "G-SHAPE-UNRESOLVED", "G-STATUS", "G-STATUS-BETA", "G-RULINGS"} & g) and content
    why = sorted(g & {"G-SCHEMA", "G-DEPRECATED", "G-WHEN", "G-SHAPE", "G-SHAPE-UNRESOLVED", "G-STATUS", "G-STATUS-BETA", "G-RULINGS"})
    if not content:
        why.append("G-NO-CONTENT")
    rows[cid] = {"slug": e["slug"], "L1": l1, "L2": l2, "L3": l3, "blocks_L3": why,
                 "slots": "declared" if "G-SLOTS" not in g else "undeclared",
                 "status": e["status"], "gaps": e["gaps"], "loss_count": len(e["loss"])}
def count(ids):
    return {k: sum(1 for i in ids if rows[i][k]) for k in ("L1", "L2", "L3")}
from collections import Counter
blk = Counter(b for r in rows.values() if not r["L3"] for b in r["blocks_L3"])
single = Counter(r["blocks_L3"][0] for r in rows.values() if not r["L3"] and len(r["blocks_L3"]) == 1)
out = {"levels_all": count(list(rows)), "levels_dashboard": count(list(dash["components"])),
       "total_all": len(rows), "total_dashboard": len(dash["components"]),
       "L3_blockers_all": dict(blk.most_common()), "L3_sole_blocker_all": dict(single.most_common()),
       "no_content_parts": sorted(r["slug"] for r in rows.values() if "G-NO-CONTENT" in r["blocks_L3"]),
       "dashboard_parts": {cid: rows[cid] for cid in dash["components"]},
       "L3_all": sorted(r["slug"] for r in rows.values() if r["L3"])}
json.dump(out, open(os.path.join(LANE, "catalogue-summary.json"), "w"), indent=1, ensure_ascii=False)
print("levels all", out["levels_all"], "of", out["total_all"], "| dashboard", out["levels_dashboard"], "of", out["total_dashboard"])
print("L3 parts:", out["L3_all"])
print("L3 blockers (all):", out["L3_blockers_all"]); print("sole blocker:", out["L3_sole_blocker_all"])
print("no-content parts:", len(out["no_content_parts"]), out["no_content_parts"][:40])
for cid, r in out["dashboard_parts"].items():
    print("%-18s L1 %-5s L2 %-5s L3 %-5s slots %-10s status %-10s blocks %s" % (cid, r["L1"], r["L2"], r["L3"], r["slots"], r["status"], r["blocks_L3"]))
