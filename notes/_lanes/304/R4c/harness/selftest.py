"""selftest.py — the harness's own test (R4c, 'test it hard'). Reads the fixture runs' scorecards
and asserts the planted-bad and known-good pages SEPARATE, that each mutant moves ONLY its own
detector, and that a re-run reproduces every mechanical score. Produce the runs first (one seat
call each, seat env sourced):

  python3 notes/_lanes/304/R4c/harness/build_fixtures.py
  for id in good:good-composed bad:bad-traced wrong-theme:good--wrong-theme clipped:good--clipped-chart \\
            no-persist:good--no-persist good-rerun:good-composed; do
    python3 notes/_lanes/304/R4c/harness/score.py all --force --run-id fx-${id%%:*} --kind fixture \\
      --copy-out notes/_lanes/304/R4c/harness/fixtures --page notes/_lanes/304/R4c/harness/fixtures/${id#*:}.html
  done
  python3 notes/_lanes/304/R4c/harness/score.py selftest
"""
import json, os
from score import RUNS, jload, jdump, LANE

def card(i):
    c = jload(os.path.join(RUNS, i, "scorecard.json"))
    if not c: raise SystemExit("missing run %s — see the docstring for how to produce it" % i)
    return c

def dims(c):
    return {k: v["score"] for k, v in c["dimensions"].items()}

def main():
    g, b = card("fx-good"), card("fx-bad")
    wt, cl, npz, rr = card("fx-wrong-theme"), card("fx-clipped"), card("fx-no-persist"), card("fx-good-rerun")
    T = lambda c: (c["sections"].get("composed_vs_traced") or {}).get("verdict")
    TH = lambda c: c["sections"]["theme"]["verdict"]
    CL = lambda c: len(c["sections"]["charts_vs_ask"]["clipped"])
    A = []
    def check(name, ok, detail):
        A.append({"assert": name, "ok": bool(ok), "detail": detail})
    check("trace: good COMPOSED, bad TRACED", T(g) == "COMPOSED" and T(b) == "TRACED", "%s vs %s" % (T(g), T(b)))
    check("theme: good PASS, bad FAIL", TH(g) == "PASS" and TH(b) == "FAIL", "%s vs %s" % (TH(g), TH(b)))
    check("clip: good 0 clipped charts, bad >=1", CL(g) == 0 and CL(b) >= 1, "%d vs %d" % (CL(g), CL(b)))
    check("total: good > bad", (g["total"] or 0) > (b["total"] or 0), "%s vs %s" % (g["total"], b["total"]))
    check("mutant wrong-theme: theme FAIL, four scores unchanged", TH(wt) == "FAIL" and dims(wt) == dims(g), "%s %s" % (TH(wt), dims(wt)))
    check("mutant clipped: >=1 clipped, theme and trace unchanged", CL(cl) >= 1 and TH(cl) == TH(g) and T(cl) == T(g), "%d clipped" % CL(cl))
    check("mutant no-persist: persistent drops, theme/trace/clip unchanged",
          dims(npz).get("persistent", 9) < dims(g).get("persistent", 0) and TH(npz) == TH(g) and CL(npz) == 0,
          "persistent %s vs good %s" % (dims(npz).get("persistent"), dims(g).get("persistent")))
    same = dims(rr) == dims(g) and T(rr) == T(g) and TH(rr) == TH(g) and CL(rr) == CL(g) and rr["total"] == g["total"]
    facts = all(rr["dimensions"][k]["fact"] == g["dimensions"][k]["fact"] for k in g["dimensions"])
    check("reproducible: an independent re-run of good gives the same scores and the same earning facts", same and facts,
          "%s / facts identical: %s" % (dims(rr), facts))
    ok = all(a["ok"] for a in A)
    out = {"verdict": "PASS" if ok else "FAIL", "asserts": A,
           "scores": {i: {"dims": dims(c), "total": c["total"], "trace": T(c), "theme": TH(c), "clipped": CL(c)}
                      for i, c in (("fx-good", g), ("fx-bad", b), ("fx-wrong-theme", wt), ("fx-clipped", cl), ("fx-no-persist", npz), ("fx-good-rerun", rr))}}
    jdump(out, os.path.join(LANE, "runs", "selftest.json"))
    for a in A: print("%s  %s — %s" % ("PASS" if a["ok"] else "FAIL", a["assert"], a["detail"]))
    print("SELFTEST", out["verdict"])
    return 0 if ok else 1
