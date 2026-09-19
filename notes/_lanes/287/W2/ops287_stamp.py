#!/usr/bin/env python3
"""#287 wrap — the DECLARE-LAST `size:` stamp, ITERATED TO A FIXED POINT.

⛔ The stamp measures the file that contains it, so a reading taken before it is written is the
   #240 one-wrap-two-figures defect. This substitutes, re-measures with the GATE'S OWN
   instrument, and repeats until the figures stop moving — then lands that text.
⛔ It runs AFTER 2c / 2d / 2f, which is what makes it a declare-LAST stamp rather than a
   prediction of a file that is still being edited.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg

GM = os.path.join(ROOT, "GOOD-MORNING.md")
LS = os.path.join(ROOT, "_LIVE-STATE.md")

text = open(GM, encoding="utf-8").read()
old = [l for l in text.split("\n") if l.startswith("> **size:** GM ")]
assert len(old) == 1, len(old)
old = old[0]

ls_tk = cg.measure_tokens(open(LS, encoding="utf-8").read())[0]
lines = text.split("\n")
spans = cg.section_spans(lines)
a_tk = cg.measure_tokens("\n".join(lines[spans["§A"][0]:spans["§C"][0]]))[0]
a_sha = cg.section_a_digest(lines, spans)
assert a_sha.startswith("4311cce4"), f"§A MOVED — digest {a_sha[:12]}, and §A is standing"

PRIOR = dict(gm=35503, ls=69049, corpus=104552)          # #286's stamp, for the delta clause


def stamp(gm_tk):
    corpus = gm_tk + ls_tk
    return (
     f"> **size:** GM **{gm_tk/1000:.1f}K tape** ({gm_tk:,} exact, whole-file `tiktoken "
     f"cl100k_base` — the figure this stamp is graded against at 10% tolerance) · §A "
     f"**{a_tk/1000:.1f}K tape** ({a_tk:,} real by `_gm_usage.py`) — ✅ **THE §A BYTE-IDENTITY "
     f"PROBE WAS RUN AT THIS SEAT AND §A IS BYTE-IDENTICAL TO ITS STATE AT THE #272…#286 WRAPS** "
     f"(`sha256 {a_sha[:8]}…` over the gate's OWN pinned probe shape "
     f"`_capture_gate.section_a_digest`, returning exactly what all fifteen of those stamps "
     f"recorded — **§A has not moved in NINETEEN sessions**; the gate reports it EXEMPT by "
     f"ruling: measured and reported, never charged). ⚠ **THE TWO-PROBE-SHAPE QUESTION #272 "
     f"RAISED IS STILL NOT SETTLED AND IS NOT SETTLED HERE:** #269/#270/#271 recorded "
     f"`sha256 b9aef5f5…` over 169 lines and #272…#287 record `{a_sha[:8]}…` over 198 — two probe "
     f"shapes, not a change in §A, and **which shape the stamp should quote is ruling-shaped and "
     f"remains Dave's, now at its NINETEENTH session, standing in `_CARRIES.md` § "
     f"`residual → #288`.** · LS **{ls_tk/1000:.1f}K tape** ({ls_tk:,} real) · corpus GM+LS "
     f"**{corpus/1000:.1f}K tape** ({corpus:,} real, the RETRIEVAL surface, not the chain) · "
     f"⛔ **the chain's own size is NOT copied here — RETIRED #45; its ONE home is `_CHAIN.md`'s "
     f"generated footer, exact by construction and `--check`-blocked** · measured 2026-09-19 at "
     f"the #287 wrap, DECLARE-LAST. ★ **AND THIS TIME THE ROLLS DID PAY FOR THEIR REPLACEMENT ON "
     f"GM, WHICH IS THE FIRST TIME IN THREE WRAPS:** against #286's stamp "
     f"(**{PRIOR['gm']:,} / {PRIOR['ls']:,} / {PRIOR['corpus']:,} tape**) GM is "
     f"**{gm_tk - PRIOR['gm']:+,} tape** while LS is **{ls_tk - PRIOR['ls']:+,}** and the corpus "
     f"**{corpus - PRIOR['corpus']:+,}** — ⛔ **so the corpus still grew, and the growth is "
     f"entirely in `_LIVE-STATE.md`**, which is where `s241-D2` says gauge, declared-skip and "
     f"5b detail belongs and is therefore the growth the cap DESIGNS FOR rather than a leak. "
     f"⛔ **THE BANNER ITSELF CAME IN UNDER THE CAP ON THE FIRST PASS — 1,145 of the `s241-D2` "
     f"1,200 over 10 of 10 substantive lines**, and what paid for the fit is that FOUR carries "
     f"closed. ⛔ **#272…#286's standing warning that the next wrap has no room in this idiom is "
     f"NOT withdrawn, and the cap is Dave's.** ⛔ **NEITHER FILE SIZE IS A TRIM ORDER; all of "
     f"these are measurements, and what to do about them is Dave's.** ⚠ **AND TWO DRIFTS ARE "
     f"DECLARED RATHER THAN LEFT TO BE DISCOVERED.** (1) **Both this stamp and the "
     f"`section-sizes` line measure regions that CONTAIN them**, so each was ITERATED TO A FIXED "
     f"POINT rather than published at a reading taken before it was written — the #240 lesson, "
     f"mechanised in `notes/_lanes/287/W2/ops287_stamp.py` and `ops287_sizes.py`. (2) **The "
     f"`s214-D6` chain figure and STEP 5b both land AFTER this stamp** (the stamp is itself "
     f"inside the chain slice — the #241 rule), so they move GM and `_LIVE-STATE.md` by "
     f"single-digit-percent tape against a 10% grading tolerance and **the stamp is NOT re-taken "
     f"for them** — saying so is cheaper and truer than a second reading nobody can reconcile.")


cur, n = cg.measure_tokens(text)[0], 0
while n < 10:
    n += 1
    trial = text.replace(old, stamp(cur))
    assert trial != text
    nxt = cg.measure_tokens(trial)[0]
    print(f"  pass {n}: GM {cur:,} → {nxt:,} {'FIXED POINT' if nxt == cur else ''}")
    if nxt == cur:
        open(GM, "w", encoding="utf-8").write(trial)
        print(f"WROTE the stamp — GM {cur:,} · §A {a_tk:,} ({a_sha[:8]}…) · LS {ls_tk:,} "
              f"· corpus {cur + ls_tk:,}")
        break
    cur = nxt
else:
    sys.exit("REFUSED — the size stamp did not converge in 10 passes; nothing written.")
