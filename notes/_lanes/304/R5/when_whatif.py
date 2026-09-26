#!/usr/bin/env python3
"""R5 / 5c — what-if: the two variant-A misses, re-run with ONE clause added to a meta's `when` IN MEMORY
(no meta is edited). Shows what the when-rules lane (4d) would have to author. System python3."""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import when_eval as W
M = W.load_metas()
T = {t["id"]: t for t in W.TESTS}
def run(label, patch, tid):
    m2 = copy.deepcopy(M)
    for slug, add in patch.items():
        g, _, p = m2[slug]["when"].partition("—")
        m2[slug]["when"] = g.rstrip() + " AND " + add + " —" + p
    W.PARSED.clear()
    r = W.choose(T[tid]["ctx"], T[tid]["role"], metas=m2)
    # regression: every other test must keep its variant-A result
    regress = []
    for t in W.TESTS:
        W.PARSED.clear(); a = W.choose(t["ctx"], t["role"], metas=M)["pick"]
        W.PARSED.clear(); b = W.choose(t["ctx"], t["role"], metas=m2)["pick"]
        if a != b and t["id"] != tid:
            regress.append((t["id"], a, b))
    print("%-4s %-55s pick %-18s expect %-18s %s | other tests changed: %s" % (tid, label, r["pick"], T[tid]["expect"], "OK" if r["pick"] == T[tid]["expect"] else "MISS", regress))
    return {"test": tid, "patch": patch, "pick": r["pick"], "ok": r["pick"] == T[tid]["expect"], "regressions": regress}
out = [run("chart-line gains `units = same`", {"chart-line": "units = same"}, "W10"),
       run("chart-line gains `shape = time-series × 1–5-series`", {"chart-line": "shape = time-series × 1–5-series"}, "W1c"),
       run("both, together (W1c)", {"chart-line": "units = same AND shape = time-series × 1–5-series"}, "W1c"),
       run("both, together (W10)", {"chart-line": "units = same AND shape = time-series × 1–5-series"}, "W10")]
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "when-whatif-results.json"), "w"), indent=1, ensure_ascii=False)
