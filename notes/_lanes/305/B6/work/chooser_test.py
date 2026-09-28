#!/usr/bin/env python3
"""305 B6 (copied from B2) — the chooser (notes/_lanes/304/R5/when_eval.py) on the LIVE metas after calls 20/21/22/24/8.
R5's 20 tests (expectations R5's, written before its run) for the rules-only reading (A) and the chooser's
default reading (B, call 21), plus this lane's added cases. Writes notes/_lanes/305/B6/work/chooser-results.json."""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "notes", "_lanes", "304", "R5"))
import when_eval as W
W.METAS = W.load_metas()
ADDED = [
 {"id": "W18n", "why": "call 22: the same grid question with the need stated", "role": "record-list",
  "ctx": {"records": 40, "surface": "none", "needs": "sort"}, "expect": "data-grid"},
 {"id": "W13n", "why": "call 22: the list question with needs = none stated", "role": "record-list",
  "ctx": {"records": 3, "surface": "none", "needs": "none"}, "expect": "list-items"},
 {"id": "W20", "why": "call 24: a consequential confirmation must stop the person", "role": "overlay",
  "ctx": {"interrupts": "required"}, "expect": "modals"},
 {"id": "W21", "why": "call 24: one main action with related ones, nothing must stop the person", "role": "action",
  "ctx": {"actions": 3, "interrupts": "none"}, "expect": "split-button"},
 {"id": "W22", "why": "call 24: one choice from seven, made in place", "role": "input",
  "ctx": {"options": 7, "interrupts": "none"}, "expect": "dropdown"},
 {"id": "W8w", "why": "call 8: a composition with a printed total offered a FULL-WIDTH tile", "role": "chart-panel",
  "ctx": {"answers": "composition", "total": "printed", "parts": 4, "span.cols": 12}, "expect": "not chart-donut/chart-pie"},
]
rows = []
for t in W.TESTS + ADDED:
    W.PARSED.clear()
    a = W.choose(t["ctx"], t["role"], implicit=False)
    t0 = time.perf_counter(); b = W.choose(t["ctx"], t["role"]); ms = (time.perf_counter() - t0) * 1000
    exp = t["expect"]
    ok = (lambda p: p not in ("chart-donut", "chart-pie")) if exp.startswith("not ") else (lambda p: p == exp)
    rows.append({"id": t["id"], "expect": exp, "A": a["pick"], "A_ok": ok(a["pick"]), "B": b["pick"], "B_ok": ok(b["pick"]),
                 "B_eligible": b["eligible"][:5], "B_excluded": b["excluded"][:8], "ms": round(ms, 3)})
    print("%-5s exp %-26s A %-18s %s  B(default) %-18s %s" % (t["id"], exp, a["pick"], "OK " if ok(a["pick"]) else "MISS",
                                                              b["pick"], "OK " if ok(b["pick"]) else "MISS"))
r5 = [r for r in rows if r["id"] in {t["id"] for t in W.TESTS}]
summ = {"r5_tests": len(r5), "A": sum(r["A_ok"] for r in r5), "B_default": sum(r["B_ok"] for r in r5),
        "added": len(ADDED), "added_B_ok": sum(r["B_ok"] for r in rows if r["id"] not in {t["id"] for t in W.TESTS}),
        "B_ms_median": sorted(r["ms"] for r in rows)[len(rows) // 2]}
print("summary:", json.dumps(summ))
json.dump({"$run_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "summary": summ, "rows": rows},
          open(os.path.join(HERE, "chooser-results.json"), "w"), indent=1, ensure_ascii=False)
