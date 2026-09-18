#!/usr/bin/env python3
"""#282 wrap, step 2 — the DECLARE-LAST `size:` stamp, written AFTER 2c/2d/2f, after the new
stratum and after the banner's second compression pass, so it grades the files this wrap
actually leaves behind."""
import sys
from run_ops import run

NEW = ("> **size:** GM **34.7K tape** (34,681 exact — whole-file `tiktoken cl100k_base`, the figure this "
 "stamp is graded against at 10% tolerance) · §A **7.0K tape** (6,957 real by `_gm_usage.py`) — ✅ **THE §A "
 "BYTE-IDENTITY PROBE WAS RUN AT THIS SEAT AND §A IS BYTE-IDENTICAL TO ITS STATE AT THE #272…#281 WRAPS** "
 "(`sha256 4311cce4…` over **198 lines** between the `§A` and `§C` markers, the gate's OWN pinned probe shape "
 "`_capture_gate.section_a_digest(lines, spans)`, returning exactly what all ten of those stamps recorded — so "
 "**§A has not moved in FOURTEEN sessions**; the gate reports it EXEMPT by ruling: measured and reported, never "
 "charged). ⚠ **THE TWO-PROBE-SHAPE QUESTION #272 RAISED IS STILL NOT SETTLED AND IS NOT SETTLED HERE:** "
 "#269/#270/#271 all recorded `sha256 b9aef5f5…` over 169 lines, #272…#282 all record `4311cce4…` over 198; two "
 "probe shapes, not a change in §A, and **which shape the stamp should quote is ruling-shaped and remains Dave's "
 "— now at its fourteenth session, standing in `_CARRIES.md` § `residual → #283`.** · LS **65.8K tape** (65,762 "
 "real) · corpus GM+LS **100.4K tape** (100,443 real, the RETRIEVAL surface, not the chain) · ⛔ **the chain's own "
 "size is NOT copied here — RETIRED #45; its ONE home is `_CHAIN.md`'s generated footer, exact by construction and "
 "`--check`-blocked** · measured 2026-09-18 at the #282 wrap, DECLARE-LAST — after 2c, 2d and 2f, after the new "
 "stratum, and after the banner's second compression pass, so it grades the files this wrap actually leaves "
 "behind. ⚠ **ONE KNOWN, MEASURED DRIFT IS DECLARED RATHER THAN LEFT TO BE DISCOVERED: the `s214-D6` line in the "
 "stratum carries a chain figure that can only be read AFTER this stamp exists (the stamp is itself inside the "
 "chain slice — the #241 rule), so it is substituted into that line after this reading was taken.** The "
 "substitution changes digits only and moves GM by single-digit tape against a 10% tolerance; the stamp is NOT "
 "re-taken for it, and saying so is cheaper and truer than a second reading nobody can reconcile. ✅ **THE ROLLS "
 "PAID FOR THEIR REPLACEMENT ON GM THIS TIME AND DID NOT ON LS — measured, not a trim order:** against #281's "
 "stamp (**35,374 / 64,466 / 99,840 tape**) GM is **693 tape DOWN**, LS **1,296 UP**, corpus **603 UP**. #280's "
 "twelve-line banner and #279's twenty-line delta rolled OUT and the new banner is capped, which is why GM fell; "
 "LS rose because this session's ⏱ LATEST DELTA and `Last refreshed` segment are larger than the #279 delta and "
 "#278 chain segment that left — six rulings, two corrections and the largest hard-line breach on record take more "
 "words to state truly. ⛔ **AND THE BANNER'S HEADROOM IS NOW EXACTLY ZERO: 1,200 tape of a 1,200 cap over 10 of 10 "
 "substantive lines**, reached in SIX measured compression passes (1,249 → 1,200) with nothing dropped — the "
 "thirteen commit shas are a pointer at the ⏱ LATEST DELTA, named on the banner as *pointer, not omission*. "
 "⚠ **AND A SECOND INSTRUMENT DISAGREED, DECLARED RATHER THAN SMOOTHED: `banner282.py` read 1,200 while the GATE'S "
 "OWN `_latest_banner_region()` read 1,235 for what looked like the same text** — the difference is the GENERATED "
 "`residual` line, whose final text is longer than the PENDING placeholder measured at draft time. **The gate's "
 "reading is the one that binds and the one published.** ⛔ **#272…#281's standing warning that the next wrap has "
 "no room in this idiom is NOT withdrawn — it is now arithmetic, and the cap is Dave's.** ⛔ **NEITHER FILE SIZE IS "
 "A TRIM ORDER; all of these are measurements, and what to do about them is Dave's.**")


def old_line():
    for ln in open("/sessions/tender-hopeful-allen/mnt/UX-design/GOOD-MORNING.md", encoding="utf-8"):
        if ln.startswith("> **size:**"):
            return ln.rstrip("\n")
    raise SystemExit("REFUSED — no `size:` stamp line found")


if __name__ == "__main__":
    OPS = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [old_line()], "replace": [NEW]}]
    sys.exit(run("stamp", OPS, write="--write" in sys.argv, min_bytes=1500))
