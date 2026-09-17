#!/usr/bin/env python3
"""#281 wrap, step 1: stamp `Last refreshed` from `date` and demote #280's segment to
`Previous:`. ONE textual span inserted, ONE prefix rewritten, both asserted by reconstruction in
this process before the write. The date comes from `date`, never belief."""
import os, subprocess, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
LS = os.path.join(ROOT, "_LIVE-STATE.md")
orig = open(LS, encoding="utf-8").read()
TODAY = subprocess.check_output(["date", "+%Y-%m-%d (%a"], text=True).strip()
assert TODAY.startswith("2026-09-17 (Thu"), TODAY

OLD_HEAD = "*Last refreshed: 2026-09-17 (Thu from `date` — **#280 wrap**."
NEW_HEAD = "Previous: 2026-09-17 (Thu from `date` — **#280 wrap**."
assert orig.count(OLD_HEAD) == 1, orig.count(OLD_HEAD)

SEG = (
 "*Last refreshed: 2026-09-17 (Thu from `date` — **#281 wrap**. ✅ **NO DATE SPLIT: the session, "
 "its nine commits, this ritual and its own commit are ALL 2026-09-17** — #281 opened and closed "
 "inside one day. The four standing WRAP DATE SPLIT notices belong to #241, #248, #261 and "
 "#272/#277, and ⬛ **#241's ruling-shaped question — what a midnight-spanning wrap should stamp — "
 "is still Dave's, now at AGE 40, asked thirteen times and unanswered.** ⛔★★★ **READ "
 "`_HANDOFF-132-the-orphan-plan-and-the-brain-learns-why.md` FIRST — IT IS NEWER THAN `_CHAIN.md` "
 "AND OUTRANKS IT**, and it does NOT replace `_HANDOFF-130` or `_HANDOFF-131`, whose open items "
 "still stand — with two named exceptions: ✅ **#131's ORPHAN CENSUS EXPORT is CLOSED** (it arrived "
 "11:02Z carrying ELEVEN radios, not the predicted ten, every one on the recommendation, and five "
 "lanes enacted it) and ⛔ **#131's EYE-CHECK OF THE SIX MATRIX CELLS IS STILL NOT DONE**, asked "
 "twice now and #282's second move. ★★ **SIX RULINGS, `knowledge/_rulings.json` 607 → 613, EVERY "
 "ONE BY TEXTUAL SPAN AND EVERY ONE INSCRIBED BY THE LANE THAT BUILT IT — `git show --numstat` "
 "reads `22  0` (`b95042c`), `52  0` (`ea2c87e`), `47  0` (`d23aed9`) and `28  0` (`7f714f0`), "
 "ZERO deletions anywhere, and a `json.load` counts 613 entries; verified here rather than "
 "restated.** **`s281-D1`** (PH) research families are NODES, `inFamily` + `evidencedBy` on · "
 "**`s281-D2`** (record rode in RO's `ea2c87e` — **carrier wrong, declared in FO's own report**; "
 "enacted `fd85bbe`) the guideline family owns a double-named file and the BUILDER declares the "
 "tie · **`s281-D3`** (RO) **`restsOn` rule→ux is an AUTHORED edge type**, the 59 BLOCKING rules "
 "first · **`s281-D4`** (TV) a design's citation of a principle is drawn in the third view, "
 "governance stays at three provenances, **force by grade NOT ruled** · **`s281-D5`** (TV) the "
 "triad is SYSTEM · GOVERNANCE · THEORY, labels only · **`s281-D6`** (RL) `restsOn` is "
 "many-to-many, his *\"both\"* lands both, and **a rule NOTE is not a rule EDIT**. ★★★ **THE "
 "EXPLORER WENT 1.20 → 1.25 IN FIVE STEPS AND THE DARK DOTS WENT 157 → 8**: CM `06e28bb` (1.21, "
 "six edge types get a family, 157 → 108) · PH `b95042c` (1.22, 32 family nodes, 145 `inFamily`, "
 "134 `evidencedBy` + 11 nulls, 108 → 8) · RO `ea2c87e` (the 59-card page — 52 on a principle, 7 "
 "convention proposed, **nothing landed by design**) · FO `fd85bbe` (1.23, **14 files tied, not "
 "the brief's 3**, 5 re-homed, census set 06 24 → 0) · TV `d23aed9` (1.24, 14 citation lines, the "
 "triad renamed, `$why` on 168 metas) · RL `7f714f0` (1.25, **65 `restsOn` edges + 8 declared "
 "nulls across 52 of 59 rules**, 13 doubles, **36 lines carrying his own sentence unedited**); "
 "conductor `2904db0` `0a9a297` `402bf9d`. ★ **THE METHOD WENT THREE ROUNDS IN ONE DAY: ASK WITH A "
 "PAGE, TAKE THE ANSWER WHOLE** — the census was recut as a PLAN with a recommendation on every "
 "set through the twelve-designer-questions lens, **his 11:02Z export took ALL ELEVEN**, the five "
 "harder calls came back **all (a)** at 11:58Z with three *\"let's talk\"* notes settled by "
 "*\"Okay these all look good to me, thanks for the explanation\"*, and then **59 cards, one per "
 "BLOCKING rule, all answered at 14:49Z**. ⬛ **HIS AND OPEN AT THE CLOSE, each written as the "
 "QUESTION IT IS (`s271-D4`): the 15 RULE NOTES** "
 "(`notes/_lanes/281/rests-on-land/RULE-NOTES-2026-09-17.md` — 13 rows arguing with the rule, 2 "
 "riding on a *\"both\"* answer; **nothing inscribed, no guideline file changed**) — **#282's "
 "first move** · **the eye-check of the six cells** · **force by grade** (TV declined to rule it "
 "and named the `restsOn` export as its precondition; that export has now landed, so it is live) "
 "and **the ghost layer's colour** — two lanes met it, both recommend as shipped, both say ONE "
 "LINE freezes the default canvas if he wants it · **FO's two untied governance artefacts and "
 "whether a repo tool deserves its own family** (`W-281fo`) · **three ASKs** — `col26-012`, "
 "`aid-009` (whose note is that the rule is *\"too boolean\"*, a RULE conversation), `type26-002` "
 "landed BOTH ways — **and `type26-003` NOT landed**, a borderline RL declined to infer · **the "
 "LOGO REVIEW, raised TWICE today**, parked with a tripwire since #277. ⚙ **GAUGE, MEASURED AT "
 "THIS SEAT against the conductor's own transcript** (first user record his *\"Good Morning!\"*, "
 "which is what makes the subtraction legal): **FILL 261,606 real over 56 turns** against "
 "**256,287 real / 54 turns DECLARED** at the brief cut ⇒ **delta 5,319**. ⛔⛔★★★ **THE 256,000 "
 "HARD LINE IS BREACHED BY 5,606 — the second breach on the record after #277's — 81,606 past the "
 "ruled 180,000 stop line and 41,606 OUTSIDE the ≤220,000 tolerance**; ⛔ **the conductor DECLARED "
 "the breach on every turn from 232,843 onward and kept cutting lanes on Dave's exports rather "
 "than wrapping, and that is the session's finding about itself.** **BOOT 77,400 real, n=1** "
 "against the `s129-D1` floor 70,794 — **+6,606, NOT a re-base**, `BOOT_FIRSTTURN_TK` untouched; "
 "⚠ **the conductor did not record boot at the opener, so this is THIS SEAT'S measurement of his "
 "transcript.** ★ **subs 1,273,123 across n=6** — QUOTA and never FILL — written because the "
 "harness MEASURED each lane (CM 244,833 · PH 203,180 · FO 178,058 · RO 160,515 · TV 239,310 · RL "
 "247,227), the one condition `s214-D5` sets. ⛔ **NO PACE PANEL WAS ASKED FOR AND NONE IS "
 "INVENTED.** ⛔ **`/sessions` 99%** (145,744 KB free at his opener, 153,932 KB free here). ⛔ "
 "**SIX BLOCKING GATE FAILS CARRIED IN THE `#243` FORM — the SEVENTH consecutive wrap on that "
 "path — all of them another session's append-only testimony in `notes/_GAUGE-LOG.md`** (the "
 "boot-drift ceiling breach and five boot double-counts: #243, #264, #272, #273, #274). ✅ **A "
 "SEVENTH WAS RED AT THIS SEAT AND IS HEALED HERE — `notes/_RULINGS.html` was STALE against "
 "`_rulings.json`** after six rulings landed and no lane re-rendered it; rebuilt and staged at "
 "step 4d, exactly the `s263-D10` case. ⛔ **`_validate_roles_resolve.py` READS FAIL(6) and "
 "`_validate_lane_ownership.py --selftest` READS 2/3, both measured here and both INHERITED**; "
 "`showroom/` holds **138** top-level `.html` against an inscribed *\"108 stale\"* — both readings "
 "stand, neither is rewritten, and it is HIS call. Gauge, declared skips (each with its size), the "
 "cloud-store result and not-done: the ⏱ LATEST DELTA below. **`_CARRIES.md` § `## residual → "
 "#282` is the carry set (`s225-D2`), 521 probeable items; the banner carries the pointer and the "
 "probeable count.** **This wrap's own filed report (`s218-D7`): "
 "`notes/_subreports/2026-09-17-281-W-wrap.md`.** **Narrative dossier (1b): "
 "`_DECISION-HISTORY/2026-09-17-281-the-orphan-plan-and-the-brain-learns-why.md`.** **His words "
 "verbatim: `notes/_lanes/281/DAVE-RULINGS-2026-09-17.md`.**)*  ")

i = orig.index(OLD_HEAD)
new = orig[:i] + SEG + NEW_HEAD + orig[i + len(OLD_HEAD):]
assert new.count("*Last refreshed: ") == 1, new.count("*Last refreshed: ")
assert orig[i + len(OLD_HEAD):] == new[len(orig[:i] + SEG + NEW_HEAD):], "REFUSED — tail moved"
if "--write" not in sys.argv:
    print(f"DRY: segment {len(SEG)} chars; head demoted; tail identical — PASSED"); sys.exit(0)
open(LS, "w", encoding="utf-8").write(new)
print(f"STAMPED {TODAY} — segment {len(SEG)} chars inserted, #280 demoted to Previous:")
