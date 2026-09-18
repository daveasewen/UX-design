#!/usr/bin/env python3
"""#282 wrap, step 5b — the post-wrap addendum: the shipped sha, the push verdict quoted verbatim,
and the CI reading read back through the public API.

⛔ HOMED IN THE ⏱ LATEST DELTA AND NOT ON THE ★ LATEST BANNER, DECLARED RATHER THAN QUIET.
Step 5b says to append it to the banner; the banner stands at 1,200 tape of a 1,200 cap
(`s241-D2`) over 10 of 10 lines, so one more line would breach a BLOCKING gate. The contradiction
between step 5b and the cap is ALREADY a carried item — #281 met it first and chose the same home,
and this is its second occurrence. Resolving it is Dave's."""
import sys
from run_ops import run

LINES = [
 "",
 "- ⚠ **POST-WRAP ADDENDUM (5b) — HOMED HERE AND NOT ON THE ★ LATEST BANNER, DECLARED RATHER THAN "
 "QUIET.** Step 5b says append to the banner; the banner is at **1,200 tape of the 1,200 `s241-D2` "
 "cap over 10 of 10 lines**, so one more line would breach a BLOCKING gate. **The step-5b-versus-cap "
 "contradiction is a CARRIED item and this is its SECOND occurrence** (#281 met it first and chose "
 "this same home); resolving it is Dave's. ★ **THE SHIPPED SHA IS `e292b14`** — a commit cannot name "
 "itself, which is why `COMMIT STATE #282` declares the gap and this line closes it. ✅ **PUSHED, and "
 "the script's own verdict line is quoted verbatim, not paraphrased:** `✅ pushed and VERIFIED: remote "
 "master == local e292b14ba0f75ca1916c86e5cb775d40e5e859e8` (`3f009cc..e292b14`). ⛔ **CI READ BACK "
 "THROUGH THE PUBLIC API (`gh` is absent from this sandbox), run `35331649780` on `e292b14`: "
 "`release` SUCCESS · `render` IN PROGRESS at read time · `gates` FAILING at \"Survey the COMMITTED "
 "tree\" and \"Knowledge build\".** ⚠ **Those are the SAME two steps the wrap brief quotes as failing "
 "on `854ea12`, `8591829` and `3f009cc` — INHERITED RED, unchanged by this wrap, quoted and not "
 "softened.** ⛔ **NO CLAIM IS MADE THAT THIS WRAP CAUSED OR CLEARED THEM**, and `render`'s colour is "
 "UNKNOWN at write time rather than assumed [[feedback-measuring-tool-must-not-guess]]. ⬛ **THE "
 "`s271-D4` RE-READ RAN AS THE RITUAL'S FINAL BEAT and is recorded at "
 "`notes/_lanes/282/W/WRAP-REPORT.md`: TWO items STRUCK with their ruling ids named (the 15 rule "
 "notes by `s282-D1`, the eye-check at `6bac5e4`) and FOUR near misses NAMED rather than struck.**",
]

ANCHOR = ("- **`_CARRIES.md` § `## residual → #283` is the carry set (`s225-D2`); the banner carries the "
          "pointer, the retrieval id and the probe command that recomputes the count.**")

if __name__ == "__main__":
    line = None
    for ln in open("/sessions/tender-hopeful-allen/mnt/UX-design/_LIVE-STATE.md", encoding="utf-8"):
        if ln.startswith(ANCHOR[:60]):
            line = ln.rstrip("\n"); break
    assert line, "REFUSED — anchor not found in _LIVE-STATE.md"
    OPS = [{"op": "insert", "file": "_LIVE-STATE.md", "at": line, "where": "after", "lines": LINES}]
    sys.exit(run("addendum", OPS, write="--write" in sys.argv, min_bytes=800))
