#!/usr/bin/env python3
"""#284 wrap, 5b — the POST-WRAP ADDENDUM, homed in the ⏱ LATEST DELTA rather than on the
★ LATEST banner. Step 5b says append it to the banner; the `s241-D2` cap is BLOCKING at 10
lines / 1,200 tape and this banner closed at 1,199 / 10, so an eleventh line would be refused,
correctly. The cap's own words license the home (*the ⏱ LATEST DELTA is the sole home for
gauge / declared-skip / not-done detail*), and the delta is IN the read chain.
⛔ The 5b-vs-cap conflict is ruling-shaped, Dave's, and carried."""
import sys
from run_ops import run

LINE = ("- ⬛ **POST-WRAP ADDENDUM (5b) — HOMED HERE AND NOT ON THE ★ LATEST BANNER, DECLARED RATHER "
 "THAN QUIET** (the `s241-D2` cap is BLOCKING at 10 lines / 1,200 tape and this banner closed at "
 "**1,199 / 10**, so an eleventh line would be refused, correctly; the cap's own words make the ⏱ "
 "LATEST DELTA the sole home for this detail, and the delta is IN the read chain — ⛔ **the "
 "5b-vs-cap conflict is ruling-shaped, Dave's, and carried, this being the FOURTH wrap to meet it "
 "and the THIRD to answer it this way**). ✅ **SHIPPED `9a97e006` on the `#243` DECLARED not-a-wrap "
 "path, the TENTH wrap running. It took THREE runs and both refusals were the script working:** "
 "`_gen_chain.py --check` caught `_CHAIN.md` stale against the final tree · the `#208` MENTION-MAP "
 "gate found `knowledge/_graph-mention-map.json` stale, regenerated it and **refused to stage a path "
 "this seat had not named** (the P5 rule); each was repaired with a FRESH uniquely-named msgfile and "
 "the path named, never by widening the stage. ★ **THREE runs here against SIX for `ade8a403`, and "
 "the difference is runbook step 0: the `allow_cowork_file_delete` grant was ACTIVE at this seat, so "
 "no `.git/index.lock` was ever stranded and `/tmp/gitshim` — which is gone — was never needed.** ✅ "
 "**PUSHED AND VERIFIED, the script's own literal verdict line quoted and not paraphrased:** `✅ "
 "pushed and VERIFIED: remote master == local 9a97e006de3e2496e7f5b1015706d40793c418b6` "
 "(`2345543e..9a97e006  master -> master`; the conductor's `ade8a403`, unpushed at the ritual's open, "
 "is on the remote with this wrap's). ⚙ **CI WAS READ AND ONLY WHAT WAS READ IS CLAIMED:** "
 "`GET /repos/daveasewen/UX-design/actions/runs?per_page=2` returned run **`35350595685`** "
 "(`gates`, `head_sha 9a97e006…`, created 2026-09-18T13:30:19Z) at **`status: in_progress`, "
 "`conclusion: null`**, and beneath it run **`35341072505`** (`gates`, `head_sha 2345543e` — #283's "
 "shipped wrap commit, NOT this session's) **`completed` / `failure`**. ⛔ **NO COLOUR IS CLAIMED FOR "
 "THIS SESSION'S COMMITS: an in-progress run has no conclusion, and the `failure` is INHERITED and "
 "predates every commit of #284** — `notes/_lanes/284/DISK-LEVER-2026-09-18.md` recorded the same run "
 "at the session's open. The conductor may read it back at the #285 opener. ⛔ **AND THE `s271-D4` "
 "RE-READ RAN AS THE RITUAL'S FINAL BEAT WITH NOTHING TO STRIKE BY CONSTRUCTION — #284 inscribed no "
 "ruling — and is recorded in full at `notes/_lanes/284/W/WRAP-REPORT.md`, where three items that "
 "MOVED WITHOUT BEING RULED (the masters' acceptance, the disk act, and Dave's correction of what the "
 "stop line is for) are NAMED rather than struck.**")

ANCHOR = "- ⚠ **THE CARRY SET IS `_CARRIES.md` § `## residual → #285`"
OPS = [{"op": "insert", "file": "_LIVE-STATE.md", "at": {"regex": "^" + "- ⚠ \\*\\*THE CARRY SET IS `_CARRIES\\.md` § `## residual → #285`"},
        "where": "after", "lines": ["", LINE]}]
if __name__ == "__main__":
    sys.exit(run("addendum", OPS, write="--write" in sys.argv, min_bytes=800))
