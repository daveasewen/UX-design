#!/usr/bin/env python3
"""#283 wrap, step 2 — the DECLARE-LAST `size:` stamp, written AFTER 2c/2d/2f, after the new
stratum and after the banner's compression passes, so it grades the files this wrap actually
leaves behind."""
import os, sys
from run_ops import run

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))

NEW = ("> **size:** GM **34.9K tape** (34,869 exact — whole-file `tiktoken cl100k_base`, the figure this "
 "stamp is graded against at 10% tolerance) · §A **7.0K tape** (6,957 real by `_gm_usage.py`) — ✅ **THE §A "
 "BYTE-IDENTITY PROBE WAS RUN AT THIS SEAT AND §A IS BYTE-IDENTICAL TO ITS STATE AT THE #272…#282 WRAPS** "
 "(`sha256 4311cce4…` over **198 lines** between the `§A` and `§C` markers, the gate's OWN pinned probe shape "
 "`_capture_gate.section_a_digest(lines, spans)`, returning exactly what all eleven of those stamps recorded — so "
 "**§A has not moved in FIFTEEN sessions**; the gate reports it EXEMPT by ruling: measured and reported, never "
 "charged). ⚠ **THE TWO-PROBE-SHAPE QUESTION #272 RAISED IS STILL NOT SETTLED AND IS NOT SETTLED HERE:** "
 "#269/#270/#271 all recorded `sha256 b9aef5f5…` over 169 lines, #272…#283 all record `4311cce4…` over 198; two "
 "probe shapes, not a change in §A, and **which shape the stamp should quote is ruling-shaped and remains Dave's "
 "— now at its fifteenth session, standing in `_CARRIES.md` § `residual → #284`.** · LS **67.5K tape** (67,450 "
 "real) · corpus GM+LS **102.3K tape** (102,319 real, the RETRIEVAL surface, not the chain) · ⛔ **the chain's own "
 "size is NOT copied here — RETIRED #45; its ONE home is `_CHAIN.md`'s generated footer, exact by construction and "
 "`--check`-blocked** · measured 2026-09-18 at the #283 wrap, DECLARE-LAST — after 2c, 2d and 2f, after the new "
 "stratum, and after the banner's five compression passes, so it grades the files this wrap actually leaves "
 "behind. ⚠ **ONE KNOWN, MEASURED DRIFT IS DECLARED RATHER THAN LEFT TO BE DISCOVERED: the `s214-D6` line in the "
 "stratum carries a chain figure that can only be read AFTER this stamp exists (the stamp is itself inside the "
 "chain slice — the #241 rule), so it is substituted into that line after this reading was taken.** The "
 "substitution changes digits only and moves GM by single-digit tape against a 10% tolerance; the stamp is NOT "
 "re-taken for it, and saying so is cheaper and truer than a second reading nobody can reconcile. ⛔ **THE ROLLS "
 "DID NOT PAY FOR THEIR REPLACEMENT ON EITHER FILE THIS TIME — measured, not a trim order:** against #282's stamp "
 "(**34,681 / 65,762 / 100,443 tape**) GM is **188 tape UP**, LS **1,688 UP**, corpus **1,876 UP**. #281's "
 "twelve-line banner and #280's eighteen-line delta rolled OUT, and GM still rose, because the #283 stratum is "
 "longer than the #282 one it replaced; LS rose because a `Last refreshed` segment and a ⏱ LATEST DELTA carrying "
 "the disk diagnosis take more words than the #280 delta and #279 chain segment that left. ⚠ **A session with ONE "
 "ruling and NO lanes made the corpus BIGGER, and that is worth reading twice: the cost driver here was FINDINGS, "
 "not work** — what to do about it is Dave's. ⛔ **AND THE BANNER'S HEADROOM IS AGAIN ESSENTIALLY ZERO: 1,196 tape "
 "of a 1,200 cap over 10 of 10 substantive lines**, reached in FIVE measured compression passes (1,327 → 1,196) "
 "with nothing dropped — the disk breakdown is a pointer at the ⏱ LATEST DELTA, not an omission. ⚠ **AND THE "
 "INSTRUMENT DISAGREED WITH ITSELF, DECLARED RATHER THAN SMOOTHED: the same banner text measured 1,123 tape on one "
 "run and 1,327 on the next**, because step 4c's `--clean` had removed `~/tmp/data-gym-cache` and `tiktoken` fell "
 "back to an estimate until it re-downloaded its encoding. **The cl100k reading binds and is the one published.** "
 "⛔ **#272…#282's standing warning that the next wrap has no room in this idiom is NOT withdrawn, and the cap is "
 "Dave's.** ⛔ **NEITHER FILE SIZE IS A TRIM ORDER; all of these are measurements, and what to do about them is "
 "Dave's.**")


def old_line():
    for ln in open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8"):
        if ln.startswith("> **size:**"):
            return ln.rstrip("\n")
    raise SystemExit("REFUSED — no `size:` stamp line found")


if __name__ == "__main__":
    OPS = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [old_line()], "replace": [NEW]}]
    sys.exit(run("stamp", OPS, write="--write" in sys.argv, min_bytes=1500))
