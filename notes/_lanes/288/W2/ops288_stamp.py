#!/usr/bin/env python3
"""#288 wrap — the DECLARE-LAST `size:` stamp, ITERATED TO A FIXED POINT.

⚠ THE STAMP MEASURES A FILE THAT CONTAINS IT, so a reading taken before the write is wrong the
moment it lands — the #240 one-wrap-two-figures lesson, mechanised rather than remembered.
Substitute, re-measure, repeat until the GM figure stops moving.

⚠ DECLARED DEVIATION: a whole-file write, NOT a mover op — the mover has no iterate-to-fixed-point
op, and this is a fill of THIS wrap's own stamp. §A's digest is asserted unchanged either side.

⛔ THE `K` IS REQUIRED in the canonical form (`GM 25.6K tk`): without it `GM 25618 tk` parses as
25.6M and passes a drift check by accident.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
GM = os.path.join(ROOT, "GOOD-MORNING.md")
LS = os.path.join(ROOT, "_LIVE-STATE.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg


def digest():
    lines = open(GM, encoding="utf-8").read().splitlines()
    return cg.section_a_digest(lines, cg.section_spans(lines))


def tk(path):
    return cg.measure_tokens(open(path, encoding="utf-8").read())[0]


A_TK = 6957          # §A, from `_gm_usage.py --sizes` at this wrap — measured, not carried
A_DIGEST = "4311cce4"
PRIOR = (35238, 70303, 105541)   # #287's stamp: GM · LS · corpus


def build(gm_tk, ls_tk):
    corpus = gm_tk + ls_tk
    dgm, dls, dc = gm_tk - PRIOR[0], ls_tk - PRIOR[1], corpus - PRIOR[2]
    return (
     "> **size:** GM **%.1fK tape** (%s exact, whole-file `tiktoken cl100k_base` — the figure this "
     "stamp is graded against at 10%% tolerance) · §A **7.0K tape** (%s real by `_gm_usage.py`) — "
     "✅ **THE §A BYTE-IDENTITY PROBE WAS RUN AT THIS SEAT AND §A IS BYTE-IDENTICAL TO ITS STATE AT "
     "THE #272…#287 WRAPS** (`sha256 %s…` over the gate's OWN pinned probe shape "
     "`_capture_gate.section_a_digest`, returning exactly what all sixteen of those stamps recorded "
     "— **§A has not moved in TWENTY sessions**; the gate reports it EXEMPT by ruling: measured and "
     "reported, never charged). ⚠ **THE TWO-PROBE-SHAPE QUESTION #272 RAISED IS STILL NOT SETTLED "
     "AND IS NOT SETTLED HERE:** #269/#270/#271 recorded `sha256 b9aef5f5…` over 169 lines and "
     "#272…#288 record `%s…` over 198 — two probe shapes, not a change in §A, and **which shape the "
     "stamp should quote is ruling-shaped and remains Dave's, now at its TWENTIETH session, "
     "standing in `_CARRIES.md` § `residual → #289`.** · LS **%.1fK tape** (%s real) · corpus GM+LS "
     "**%.1fK tape** (%s real, the RETRIEVAL surface, not the chain) · ⛔ **the chain's own size is "
     "NOT copied here — RETIRED #45; its ONE home is `_CHAIN.md`'s generated footer, exact by "
     "construction and `--check`-blocked** · measured 2026-09-19 at the #288 wrap, DECLARE-LAST. "
     "⛔ **AND THIS TIME THE ROLLS DID NOT PAY FOR THEIR REPLACEMENT, ON EITHER FILE:** against "
     "#287's stamp (**%s / %s / %s tape**) GM is **%+d tape**, LS **%+d** and the corpus **%+d**. "
     "⚠ **THE CAUSE IS NAMEABLE RATHER THAN MYSTERIOUS AND IT IS THE SESSION, NOT THE RITUAL: "
     "#288 DISCHARGED almost nothing and ACCRUED seventeen carries**, and `s241-D2` puts gauge, "
     "declared-skip and 5b detail in the ⏱ LATEST DELTA, which is `_LIVE-STATE.md`. ⛔ **#272…#287's "
     "standing warning that the next wrap has no room in this idiom is NOT withdrawn — and this "
     "wrap MET it: the ★ LATEST banner did not fit on the first pass (1,250 against the 1,200 cap) "
     "and was compressed by tightening sentences, never by dropping an item, a carry, a declared "
     "skip or a receipt name** (`s214-D6`: *\"SHORTER, never decide-what-to-drop\"*). ⛔ **NEITHER "
     "FILE SIZE IS A TRIM ORDER; all of these are measurements, and what to do about them is "
     "Dave's.** ⚠ **AND TWO DRIFTS ARE DECLARED RATHER THAN LEFT TO BE DISCOVERED.** (1) **Both "
     "this stamp and the `section-sizes` line measure regions that CONTAIN them**, so each was "
     "ITERATED TO A FIXED POINT rather than published at a reading taken before it was written — "
     "the #240 lesson, mechanised in `notes/_lanes/288/W2/ops288_stamp.py` and `ops288_sizes.py`, "
     "and both are DECLARED whole-file writes rather than mover ops because the mover has no "
     "iterate-to-fixed-point op. (2) **The `s214-D6` chain figure and STEP 5b both land AFTER this "
     "stamp** (the stamp is itself inside the chain slice — the #241 rule), so they move GM and "
     "`_LIVE-STATE.md` by single-digit-percent tape against a 10%% grading tolerance and **the "
     "stamp is NOT re-taken for them** — saying so is cheaper and truer than a second reading "
     "nobody can reconcile."
    ) % (gm_tk / 1000.0, f"{gm_tk:,}", f"{A_TK:,}", A_DIGEST, A_DIGEST,
         ls_tk / 1000.0, f"{ls_tk:,}", (gm_tk + ls_tk) / 1000.0, f"{gm_tk + ls_tk:,}",
         f"{PRIOR[0]:,}", f"{PRIOR[1]:,}", f"{PRIOR[2]:,}", dgm, dls, dc)


before = digest()
prev = None
for i in range(8):
    txt = open(GM, encoding="utf-8").read()
    old = [l for l in txt.split("\n") if l.startswith("> **size:**")]
    assert len(old) == 1, f"expected one size stamp, got {len(old)}"
    new = build(tk(GM), tk(LS))
    if new == old[0]:
        print(f"FIXED POINT after {i} substitution(s)")
        break
    assert txt.count(old[0]) == 1
    open(GM, "w", encoding="utf-8").write(txt.replace(old[0], new, 1))
    print(f"  pass {i+1}: GM {tk(GM):,} · LS {tk(LS):,}")
else:
    sys.exit("DID NOT CONVERGE in 8 passes")

after = digest()
assert before == after, f"§A DIGEST MOVED: {before} -> {after}"
print(f"§A digest unchanged: {after}")
print(f"FINAL: GM {tk(GM):,} · LS {tk(LS):,} · corpus {tk(GM)+tk(LS):,}")
