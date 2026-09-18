#!/usr/bin/env python3
"""#285 wrap — the DECLARE-LAST `size:` stamp, written AFTER 2c/2d/2f have run.

The stamp is graded against the gate's OWN measurement at 10% tolerance, so it is taken after
the steps that move the files it measures — writing it earlier would make it a prediction, not
a measurement (the #240 lesson, which this wrap met again at the banner cap).

⛔ The CHAIN's own size is NOT copied here — RETIRED #45; its ONE home is `_CHAIN.md`'s generated
footer, exact by construction and `--check`-blocked.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
from run_ops import run
import _gauge_tokens as G
import _capture_gate as cg

gm_text = open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8").read()
ls_text = open(os.path.join(ROOT, "_LIVE-STATE.md"), encoding="utf-8").read()
gm, _ = G.count(gm_text)
ls, _ = G.count(ls_text)
lines = gm_text.split("\n")
digest = cg.section_a_digest(lines, cg.section_spans(lines))
assert digest.startswith("4311cce4"), f"REFUSED — §A digest moved: {digest}"

P_GM, P_LS, P_CORP = 34_845, 67_414, 102_259          # #284's stamp, for the delta only

NEW = (f"> **size:** GM **{gm/1000:.1f}K tape** ({gm:,} exact, whole-file `tiktoken cl100k_base` — "
       f"the figure this stamp is graded against at 10% tolerance) · §A **7.0K tape** (6,957 real by "
       f"`_gm_usage.py`) — ✅ **THE §A BYTE-IDENTITY PROBE WAS RUN AT THIS SEAT AND §A IS "
       f"BYTE-IDENTICAL TO ITS STATE AT THE #272…#284 WRAPS** (`sha256 {digest[:8]}…` over the gate's "
       f"OWN pinned probe shape `_capture_gate.section_a_digest`, returning exactly what all thirteen "
       f"of those stamps recorded — **§A has not moved in SEVENTEEN sessions**; the gate reports it "
       f"EXEMPT by ruling: measured and reported, never charged). ⚠ **THE TWO-PROBE-SHAPE QUESTION "
       f"#272 RAISED IS STILL NOT SETTLED AND IS NOT SETTLED HERE:** #269/#270/#271 recorded "
       f"`sha256 b9aef5f5…` over 169 lines and #272…#285 record `{digest[:8]}…` over 198 — two probe "
       f"shapes, not a change in §A, and **which shape the stamp should quote is ruling-shaped and "
       f"remains Dave's, now at its seventeenth session, standing in `_CARRIES.md` § "
       f"`residual → #286`.** · LS **{ls/1000:.1f}K tape** ({ls:,} real) · corpus GM+LS "
       f"**{(gm+ls)/1000:.1f}K tape** ({gm+ls:,} real, the RETRIEVAL surface, not the chain) · ⛔ "
       f"**the chain's own size is NOT copied here — RETIRED #45; its ONE home is `_CHAIN.md`'s "
       f"generated footer, exact by construction and `--check`-blocked** · measured 2026-09-18 at the "
       f"#285 wrap, DECLARE-LAST. ⚠ **ONE KNOWN DRIFT IS DECLARED RATHER THAN LEFT TO BE DISCOVERED: "
       f"the `s214-D6` line in the #285 stratum carries a chain figure that can only be read AFTER "
       f"this stamp exists (the stamp is itself inside the chain slice — the #241 rule), so it is "
       f"substituted into that line after this reading was taken. The substitution changes digits in "
       f"§C only, moves GM by single-digit tape against a 10% tolerance, and the stamp is NOT re-taken "
       f"for it** — saying so is cheaper and truer than a second reading nobody can reconcile. "
       f"⚠ **THE ROLLS DID NOT PAY FOR THEIR REPLACEMENT ON GM THIS TIME, AND THAT IS PUBLISHED RATHER "
       f"THAN SMOOTHED:** against #284's stamp (**{P_GM:,} / {P_LS:,} / {P_CORP:,} tape**) GM is "
       f"**{gm-P_GM:+,} tape**, LS **{ls-P_LS:+,}**, corpus **{(gm+ls)-P_CORP:+,}** — the corpus fell "
       f"and GM did not, because this session's stratum is longer than the one it replaced (seven "
       f"lanes, two closures and a dead sub all had to be declared) while the banner came in UNDER "
       f"#284's. ⛔ **THE BANNER CLOSED AT 1,196 OF THE `s241-D2` CAP OF 1,200 OVER 10 OF 10 "
       f"SUBSTANTIVE LINES**, reached in five measured compression passes with nothing dropped. "
       f"⛔ **#272…#284's standing warning that the next wrap has no room in this idiom is NOT "
       f"withdrawn, and the cap is Dave's.** ⛔ **NEITHER FILE SIZE IS A TRIM ORDER; all of these are "
       f"measurements, and what to do about them is Dave's.**")

old = [l.rstrip("\n") for l in gm_text.split("\n") if l.startswith("> **size:**")]
assert len(old) == 1, len(old)
print(f"GM {gm:,} · LS {ls:,} · corpus {gm+ls:,} · §A {digest[:8]}… "
      f"(deltas vs #284: GM {gm-P_GM:+,} · LS {ls-P_LS:+,} · corpus {(gm+ls)-P_CORP:+,})")

ops = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [old[0]], "replace": [NEW]}]
sys.exit(run("stamp", ops, write="--write" in sys.argv, min_bytes=1_500))
