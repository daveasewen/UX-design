#!/usr/bin/env python3
"""305 B6 — the four accepted rules at their seam: the chooser (R5's when_eval.py, default reading) with each
new/changed meta as it was BEFORE (this lane's backups, swapped in memory only) and AFTER (live). Probes are this
lane's, not R5's; they only show whether each rule parses and fires. Writes probe-new-rules.json beside it."""
import copy, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "notes", "_lanes", "304", "R5"))
import when_eval as W
AFTER = W.load_metas()
BEFORE = copy.deepcopy(AFTER)
for s in ["button", "filter-toolbar-bar", "footer", "template-dashboard-bento"]:
    b = json.load(open(os.path.join(HERE, "..", "backup", "knowledge", "components", s + ".meta.json")))
    if b.get("when"): BEFORE[s] = b
    else: BEFORE.pop(s, None)
CHOOSE = [("P1", "action", {"actions": 3}), ("P2", "action", {"actions": 1, "label": "text", "emphasis": "primary"}),
          ("P3", "action", {}), ("P4", "action", {"actions": 3, "interrupts": "none"})]
GATES = [("G1", "filter-toolbar-bar", {"records": 10, "needs": "filter"}), ("G2", "filter-toolbar-bar", {"records": 10, "needs": "none"}),
         ("G3", "footer", {"platform": "app"}), ("G4", "footer", {"platform": "marketing"}),
         ("G5", "template-dashboard-bento", {"layout.grammar": "bento"}), ("G6", "template-dashboard-bento", {"layout.grammar": "grid"}),
         ("G7", "button", {"actions": 2})]
out = []
for pid, role, ctx in CHOOSE:
    W.PARSED.clear(); b = W.choose(ctx, role, metas=BEFORE)
    W.PARSED.clear(); a = W.choose(ctx, role, metas=AFTER)
    out.append({"id": pid, "role": role, "ctx": ctx, "before": b["pick"], "after": a["pick"], "after_excluded": a["excluded"]})
    print("%s %-7s %-45s before %-14s after %-14s %s" % (pid, role, json.dumps(ctx), b["pick"], a["pick"], "FLIP" if a["pick"] != b["pick"] else ""))
for gid, slug, ctx in GATES:
    res = lambda M: (W.eval_gate(W.parse_when(M[slug]["when"]), ctx)[0] if slug in M else "no rule")
    rb, ra = res(BEFORE), res(AFTER)
    out.append({"id": gid, "slug": slug, "ctx": ctx, "before": rb, "after": ra})
    print("%s %-26s %-40s before %-8s after %s" % (gid, slug, json.dumps(ctx), rb, ra))
json.dump(out, open(os.path.join(HERE, "probe-new-rules.json"), "w"), indent=1)
