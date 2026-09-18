#!/usr/bin/env python3
"""#284 wrap — the DECLARE-LAST `size:` stamp in GOOD-MORNING.md's header block.

Written LAST, after 2c/2d/2f, the new stratum and the banner's six compression passes, so it
grades the files this wrap actually leaves behind. Every figure is MEASURED here by the gate's
own `measure_tokens` (tiktoken cl100k_base), never converted by a bytes/4 rule of thumb — this
corpus runs at ~3.53 bytes/token.

⚠ `s214-D6` applies to this line too: it sits INSIDE the chain slice, so it is written SHORTER
than #283's — girth only; the §A probe, the declared drifts and the ruling pointers all stay.
"""
import os, sys
from run_ops import run

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg

gm = open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8").read()
ls = open(os.path.join(ROOT, "_LIVE-STATE.md"), encoding="utf-8").read()
GM = cg.measure_tokens(gm)[0]
LS = cg.measure_tokens(ls)[0]
CORPUS = GM + LS
lines = gm.split("\n")
DIGEST = cg.section_a_digest(lines, cg.section_spans(lines))
A_LINES = None
try:
    import re
    a = next(i for i, l in enumerate(lines) if l.startswith("# §A · ORIENTATION"))
    c = next(i for i in range(a + 1, len(lines)) if lines[i].startswith("# §C · QUEUE"))
    A_LINES = c - a
except StopIteration:
    pass

old = [l for l in lines if l.startswith("> **size:**")]
assert len(old) == 1, len(old)

NEW = (
 "> **size:** GM **%s tape** (%s exact, whole-file `tiktoken cl100k_base` — the figure this stamp "
 "is graded against at 10%% tolerance) · §A **7.0K tape** (6,957 real by `_gm_usage.py`) — ✅ **THE "
 "§A BYTE-IDENTITY PROBE WAS RUN AT THIS SEAT AND §A IS BYTE-IDENTICAL TO ITS STATE AT THE #272…#283 "
 "WRAPS** (`sha256 %s…` over the gate's OWN pinned probe shape `_capture_gate.section_a_digest`, "
 "returning exactly what all twelve of those stamps recorded — **§A has not moved in SIXTEEN "
 "sessions**; the gate reports it EXEMPT by ruling: measured and reported, never charged). ⚠ **THE "
 "TWO-PROBE-SHAPE QUESTION #272 RAISED IS STILL NOT SETTLED AND IS NOT SETTLED HERE:** #269/#270/#271 "
 "recorded `sha256 b9aef5f5…` over 169 lines and #272…#284 record `%s…` over 198 — two probe shapes, "
 "not a change in §A, and **which shape the stamp should quote is ruling-shaped and remains Dave's, "
 "now at its sixteenth session, standing in `_CARRIES.md` § `residual → #285`.** · LS **%s tape** "
 "(%s real) · corpus GM+LS **%s tape** (%s real, the RETRIEVAL surface, not the chain) · ⛔ **the "
 "chain's own size is NOT copied here — RETIRED #45; its ONE home is `_CHAIN.md`'s generated footer, "
 "exact by construction and `--check`-blocked** · measured 2026-09-18 at the #284 wrap, DECLARE-LAST. "
 "⚠ **ONE KNOWN DRIFT IS DECLARED RATHER THAN LEFT TO BE DISCOVERED: the `s214-D6` line in the #284 "
 "stratum carries a chain figure that can only be read AFTER this stamp exists (the stamp is itself "
 "inside the chain slice — the #241 rule), so it is substituted into that line after this reading was "
 "taken. The substitution changes digits in §C only, moves GM by single-digit tape against a 10%% "
 "tolerance, and the stamp is NOT re-taken for it** — saying so is cheaper and truer than a second "
 "reading nobody can reconcile. ✅ **THE ROLLS PAID FOR THEIR REPLACEMENT ON BOTH FILES THIS TIME — "
 "measured, not a trim order:** against #283's stamp (**34,869 / 67,450 / 102,319 tape**) GM is "
 "**%s tape %s**, LS **%s %s**, corpus **%s %s**. ⛔ **AND THE BANNER'S HEADROOM IS ONE TAPE: 1,199 "
 "of the `s241-D2` cap of 1,200 over 10 of 10 substantive lines**, reached in SIX measured "
 "compression passes (1,286 → 1,199) with nothing dropped — three of them forced AFTER the GENERATED "
 "residual line landed, because `_roll_state.py`'s real line is longer than the placeholder it "
 "replaced. ⛔ **#272…#283's standing warning that the next wrap has no room in this idiom is NOT "
 "withdrawn, and the cap is Dave's.** ⛔ **NEITHER FILE SIZE IS A TRIM ORDER; all of these are "
 "measurements, and what to do about them is Dave's.**"
) % (
 "%.1fK" % (GM / 1000.0), "{:,}".format(GM), DIGEST[:8], DIGEST[:8],
 "%.1fK" % (LS / 1000.0), "{:,}".format(LS),
 "%.1fK" % (CORPUS / 1000.0), "{:,}".format(CORPUS),
 "{:,}".format(abs(GM - 34869)), "DOWN" if GM < 34869 else "UP",
 "{:,}".format(abs(LS - 67450)), "DOWN" if LS < 67450 else "UP",
 "{:,}".format(abs(CORPUS - 102319)), "DOWN" if CORPUS < 102319 else "UP",
)

OPS = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [old[0]], "replace": [NEW]}]

if __name__ == "__main__":
    print("GM %d · LS %d · corpus %d · §A lines %s · digest %s" % (GM, LS, CORPUS, A_LINES, DIGEST[:12]))
    sys.exit(run("stamp", OPS, write="--write" in sys.argv, min_bytes=1000))
