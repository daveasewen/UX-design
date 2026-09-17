#!/usr/bin/env python3
"""#280 wrap, step 1: stamp `Last refreshed` from `date` and demote #279's segment to
`Previous:`. ONE textual span inserted, ONE prefix rewritten, both asserted by reconstruction in
this process before the write. The date comes from `date`, never belief."""
import os, subprocess, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
LS = os.path.join(ROOT, "_LIVE-STATE.md")
orig = open(LS, encoding="utf-8").read()
TODAY = subprocess.check_output(["date", "+%Y-%m-%d (%a"], text=True).strip()
assert TODAY.startswith("2026-09-17 (Thu"), TODAY

OLD_HEAD = "*Last refreshed: 2026-09-16 (Wed from `date` — **#279 wrap**."
NEW_HEAD = "Previous: 2026-09-16 (Wed from `date` — **#279 wrap**."
assert orig.count(OLD_HEAD) == 1, orig.count(OLD_HEAD)

SEG = (
 "*Last refreshed: 2026-09-17 (Thu from `date` — **#280 wrap**. ⚠ **WRAP DATE SPLIT: THE SESSION "
 "OPENED 2026-09-16 IN THE EVENING AND ITS EIGHT LANE COMMITS CARRY THAT DATE OR 09-17; THE RITUAL "
 "AND THIS WRAP'S COMMITS ARE 2026-09-17.** ⛔ **No key, filename, ruling id, report stem or stamp "
 "was re-dated to match** — that would be the T-D12 false inscription in reverse; the #241 shape BY "
 "ADDITION, and ⬛ **#241's ruling-shaped question — what a midnight-spanning wrap should stamp — is "
 "still Dave's, now at AGE 39, asked twelve times and unanswered.** ⚠ **The two registers COUNT "
 "DIFFERENTLY and both readings are published rather than reconciled here:** `GOOD-MORNING.md`'s "
 "standing notices count FOUR before this one (#241, #248, #261, #277) while this file's #277 segment "
 "calls itself the FIFTH because it counts #272 as well. ⛔★★★ **READ "
 "`_HANDOFF-131-the-matrix-and-the-front-door.md` FIRST — IT IS NEWER THAN `_CHAIN.md` AND OUTRANKS "
 "IT**, and it does NOT replace `_HANDOFF-130`, whose open items still stand. ★★ **TWO RULINGS, "
 "`knowledge/_rulings.json` 605 → 607, BOTH BY TEXTUAL SPAN AND BOTH INSCRIBED BY THE LANE THAT "
 "BUILT THEM — `git show --numstat` reads `19  0` and `18  0`, ZERO deletions, verified here rather "
 "than restated.** **`s280-D1`** (`53a91bd`, lane LM), on his sketches export at 20:30Z — *\"Okay I "
 "want all of these plus the original view, in 2d and 3d for all of them. just keep force as the "
 "default\"* — **THE LAYOUT MATRIX: force · strata · shells × 2D · 3D, six cells, force the "
 "default**; the four sketches map onto it without remainder (FLOORS is strata-3D, ORBITS is "
 "shells-2D), and storage is untouched. **`s280-D2`** (`9e04796`, lane EX4), on *\"I want to see any "
 "artifact that exists here, including a render of the actual component snippet\"* — **THE EXPLORER "
 "IS THE FRONT DOOR: INSPECT opens the ARTEFACT, by kind** (a component with its snippet RENDERING, "
 "a rule at its own highlighted row, a ruling's record, an icon drawn at 48 and 16 px), edges are "
 "doors too, and it is **SERVED, not double-clicked** (`knowledge/_serve_explorer.py`). ★★★ **THE "
 "EXPLORER WENT 1.16 → 1.20 IN FIVE STEPS ACROSS SIX LANES, AND THE ICONS AND THE CENSUS LANDED "
 "BESIDE IT**: LY `b212ca2` + `aa75fed` (1.17 strata, default pixel-identical by canvas md5) · LS "
 "`a7ecd8f` + `53deb46` (four sketches on one page, answered by his export) · LM `53a91bd` `b5df9c9` "
 "`eddf87a` `c3805ec` `94204dc` (1.18, six cells, contact sheet "
 "`notes/_lanes/280/layout-matrix/MATRIX-2026-09-16.html`) · EX3 `2a406f1` + `5e3ba3b` (1.19, the "
 "legend stops moving by itself — his word was *\"good\"* — and INSPECT opens a modal) · EX4 "
 "`9e04796` `e518cd6` `3b92a63` (1.20) · IN `c4d0d22` + IN2 `850acbf` (**14 of his 15 icon bases "
 "settled**, `knowledge/_ICON-GAPS.md` born, and `gen_kg_icons.py` now rebuilds the fourteen from his "
 "own exports and REFUSES on disagreement, 22/22 with mutants 32/32) · OC `82359a5` (**157 of 4,618 "
 "nodes with no drawable line**, four causes, ten sets; his word was *\"cool\"*). ★ **THE METHOD THAT "
 "REPEATED IS THE FINDING: ASK WITH A PICTURE, THEN BUILD WHAT THE ANSWER SAYS** — one option, then "
 "four sketches, then his export, then the matrix; **no lane ruled anything it had not shown him.** "
 "⬛ **HIS AND OPEN AT THE CLOSE, each written as the QUESTION IT IS (`s271-D4`): the ORPHAN CENSUS "
 "EXPORT** — ten radios on `notes/_lanes/280/orphan-census/ORPHANS-2026-09-17.html`, **NOT RECEIVED**, "
 "**#281's first move**, and the census becomes the orphan plan on export · **the EYE-CHECK of the "
 "six matrix cells**, asked and unanswered (the conductor expects Floors or Orbits to go — an "
 "expectation, not a finding) · **`jade-lifestyle`**, open by his own word with his lean recorded ON "
 "THE NULL. ⚙ **GAUGE, MEASURED AT THIS SEAT: FILL 191,294 real over 28 turns**, read first-hand "
 "against the conductor's own transcript (its first user record is his own opener, which is what "
 "makes the subtraction legal), against **185,127 real / 25 turns DECLARED** at the brief cut ⇒ "
 "**delta 6,167**. ✅ **THE 200,000 WORKING LINE WAS NOT BREACHED — the first wrap in three able to "
 "say so**; ⛔ the **ruled 180,000 stop line** (`s260-D2`/`s271-D1`) is passed by **11,294**, inside "
 "the ≤220,000 tolerance and DECLARED, not excused. **BOOT 75,740 real, n=1** against the `s129-D1` "
 "floor 70,794 — **+4,946, NOT a re-base**, `BOOT_FIRSTTURN_TK` untouched and n=1 published as n=1. "
 "**subs 1,833,788 across n=8** — QUOTA and never FILL — **written because the harness MEASURED each "
 "lane** (LY 221,093 · IN 205,442 · LS 197,571 · IN2 209,660 · LM 247,259 · EX3 284,250 · OC 204,942 "
 "· EX4 263,571), which is the one condition `s214-D5` sets. ⛔ **`/sessions` 99%, 158,032 KB free, "
 "measured here**; nothing in the repo fixes it. ⛔ **SEVEN BLOCKING GATE FAILS ARE CARRIED IN THE "
 "`#243` FORM, ALL INHERITED AND ALL ANOTHER SESSION'S APPEND-ONLY TESTIMONY** — the boot-drift "
 "ceiling breach, the boot-drift step change, and five boot double-counts (#243, #264, #272, #273, "
 "#274); ⚠ **the wrap brief DECLARES SIX and this seat MEASURES SEVEN — two readings, both published, "
 "neither smoothed into one.** ⛔ **`_validate_roles_resolve.py` READS FAIL(6) and "
 "`_validate_lane_ownership.py --selftest` READS 2/3, both measured here and both INHERITED**; "
 "`showroom/` holds **138** top-level `.html` here against an inscribed *\"108 stale\"* — the figure "
 "is NOT rewritten, both readings stand, and it is HIS call. ✅★★ **CLOUD MEMORY (step 3) WAS WRITTEN "
 "FROM THIS WRAP SUB'S OWN SEAT — THE SECOND CONSECUTIVE WRAP TO MEASURE THE RUNBOOK'S \"STRUCTURAL\" "
 "SEAT LIMIT FALSE** (`wrap-280-the-matrix-and-the-front-door.md`, **7,607 B**; `index.md` now "
 "**6,882 B of the 49,152 B cap**), and ⛔ **the runbook line is STILL NOT EDITED — amending a "
 "ratified step is Dave's word.** ⚠ **Step 3 was run BEFORE step 2 at this wrap, declared and "
 "deliberate:** #279 wrote its banner while the claim was unmeasured and had to correct two files in "
 "a post-wrap addendum; running the store write first means every surface here states a MEASURED "
 "result. Gauge, declared skips (each with its size) and not-done: the ⏱ LATEST DELTA below. "
 "**`_CARRIES.md` § `## residual → #281` is the carry set (`s225-D2`); the banner carries the pointer "
 "and the probeable count.** **This wrap's own filed report (`s218-D7`): "
 "`notes/_subreports/2026-09-17-280-W-wrap.md`.** **Narrative dossier (1b): "
 "`_DECISION-HISTORY/2026-09-17-280-the-matrix-and-the-front-door.md`.** **His words verbatim: "
 "`notes/_lanes/280/DAVE-RULINGS-2026-09-17.md`.**)*  ")

i = orig.find(OLD_HEAD)
new = orig[:i] + SEG + NEW_HEAD + orig[i + len(OLD_HEAD):]
chk = new[:i] + OLD_HEAD + new[i + len(SEG) + len(NEW_HEAD):]
assert chk == orig, "REFUSED — reconstruction failed"
if "--write" not in sys.argv:
    print(f"DRY: insert {len(SEG)} chars at {i}; prefix demoted; reconstruction PASSED"); sys.exit(0)
open(LS, "w", encoding="utf-8").write(new)
print(f"WROTE: Last refreshed stamped #280 from `date` ({TODAY}); #279 demoted to Previous:; "
      f"span {len(SEG)} chars; reconstruction PASSED before the write")
