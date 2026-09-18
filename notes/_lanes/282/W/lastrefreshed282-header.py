#!/usr/bin/env python3
"""#282 wrap, step 1 — PREPEND the new `Last refreshed` segment to `_LIVE-STATE.md`'s header
zone, demoting #281's segment to `Previous:`. The date comes from `date`, never from belief
(T-D12). Span reconstruction asserted in this process before anything is written.

⛔ DATE SPLIT, FIFTH OCCURRENCE — the session opened 2026-09-17 and this ritual runs 2026-09-18.
The #241 shape BY ADDITION: the ritual stamps ITS OWN date and NOTHING is re-dated backwards.
"""
import os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
LS = os.path.join(ROOT, "_LIVE-STATE.md")

NEW = (
 "*Last refreshed: 2026-09-18 (Fri from `date` — **#282 wrap**. "
 "⚠ **WRAP DATE SPLIT, FIFTH OCCURRENCE: THE SESSION OPENED 2026-09-17 AND ITS FIRST SIX COMMITS CARRY THAT DATE; "
 "THE LAST SEVEN, THIS RITUAL AND ITS COMMIT ARE 2026-09-18.** ⛔ **No key, filename, ruling id, report stem or stamp "
 "was re-dated to match** — the #241 shape BY ADDITION, and ⬛ **#241's ruling-shaped question — what a "
 "midnight-spanning wrap should stamp — is still Dave's, now at AGE 41, asked fourteen times and unanswered.** "
 "⛔★★★ **READ `_HANDOFF-133-the-rule-notes-land-and-the-logo-is-ruled.md` FIRST — IT IS NEWER THAN `_CHAIN.md` AND "
 "OUTRANKS IT**, and it does NOT replace `_HANDOFF-130`, `-131` or `-132`, whose open items still stand — with one "
 "named exception: ✅ **#131's EYE-CHECK OF THE SIX MATRIX CELLS IS CLOSED** (`6bac5e4`, on his own word *\"sorry I "
 "though this was settled\"* — it WAS, by `s280-D1`; the carry was the conductor's expectation and never his ask, "
 "and **that is the session's lesson about its own record: a carry only the conductor wants is not Dave's open item**). "
 "★★ **SIX RULINGS, `knowledge/_rulings.json` 613 → 619, EVERY ONE VERIFIED BY TEXTUAL SPAN AT THIS SEAT RATHER THAN "
 "RESTATED — `git show --numstat` reads `34  0` (`56c5690`), `17  0` (`bb016c6`), `18  0` (`0acb019`), `20  0` "
 "(`da9f824`), `33  0` (`eaf1236`) and `17  0` (`03fe8ff`), with TWO amended-in-place corrections showing `3  3` "
 "(`c143a1b`) and `2  2` (`6df8b64`) by design, and a `json.load` counting 619.** "
 "⚠ **MEASURED AGAINST THE BRIEF AND PUBLISHED RATHER THAN SMOOTHED: the wrap brief DECLARES *three* amended-in-place "
 "commits and this seat finds TWO** (every other #282 commit touches `_rulings.json` not at all), **and it declares "
 "*14 commits* where `git log --oneline 8591829..HEAD` counts THIRTEEN.** Both readings stand; neither is rewritten. "
 "**`s282-D1`** (`56c5690`, lane RN) a rule NOTE becomes a rule EDIT when he says so — **11 guideline edits in his "
 "own words across 8 files**, 2 second `restsOn` edges, `col26-012` NOT edited · **`s282-D2`** (`bb016c6`) the "
 "red-text ban is on the PRIMARY red and the exception is a SECONDARY red only; the `col26-012` ASK closed on the "
 "cross-reference already present; backlog `W-282a` (universal icon list) and `W-282b` (SC 2.2.2 on `mot-005`) born · "
 "**`s282-D3`** (`0acb019`, corrected `c143a1b`) **logo size by RAW HEIGHT and width, five steps 24 · 28 · 32 · 36 · 40** "
 "— the first cut (32–56) stood for ONE commit and is named inside the ruling rather than erased · **`s282-D4`** "
 "(`da9f824`) **the identifier lockup is SCRAPPED**: 8 variants gone, `_logo_nodes.json` **12 → 8 nodes** (verified "
 "here), the files held in gitignored `_to_delete/logos-identifier-282/` and out of the tree · **`s282-D5`** "
 "(`eaf1236`, lane LL) **the logo review LANDED**: ONE logo guideline (`logos.md`, Apollo's decisions overriding the "
 "refresh), masthead default full colour on both grounds in all four themes (`logo26-008` BLOCKING), vertical "
 "clear-space floor 0.25 × height snapped up to 4px (`logo26-009` BLOCKING), hexagon alone on nav-rail head / app "
 "tile / favicon and at responsive small sizes (`logo26-010` ADVISORY), 8 logo nodes bound **27 → 33 edges** "
 "(verified here) with `governedBy` widened from declared-null-only, **ruling-shaped and declared as the lane's own "
 "call** · **`s282-D6`** (`03fe8ff`, corrected `6df8b64`) horizontal clear space = **0.25 × the LOGOMARK's width** "
 "snapped up to 4px, on the OPEN side by alignment (centre both · right-aligned left only · left-aligned right only), "
 "same floors for both lockups 12/16/16/20/20; the lockup-width cut also stood for one commit and is named. "
 "★★★ **THE EXPLORER WENT 1.25 → 1.26 AND THE RULE STORE GREW BY THREE**: `knowledge/_rule_nodes.json` reads "
 "**rules 470 → 473 · BLOCKING 59 → 61 · `restsOn` 73 → 75** measured at this seat against `8591829`; ⚠ **the brief "
 "DECLARES 474 and 62 — one more of each than the store holds — and `restsOn` 73 → 75 agrees exactly.** "
 "★ **THE METHOD, THIRD DAY RUNNING: ASK WITH A PAGE, TAKE THE ANSWER WHOLE.** The 15 rule notes became a 15-row "
 "decision page and came back **14 of 15 on the recommendation** at 19:10Z (`col26-012` → *\"Discuss first\"*, a note "
 "on `col26-016` green); the 12 lockups became a review page and came back **9 answered, 3 moot, four notes** at "
 "08:20Z. ⬛ **HIS AND OPEN AT THE CLOSE, each written as the QUESTION IT IS (`s271-D4`): the PER-SIZE LOGO MASTERS — "
 "#283's FIRST MOVE, fully specified, 8 lockups × 5 steps = 40 SVGs drawn at raw pixel height AND width, no viewBox, "
 "stems snapped to the grid** (his *\"is it possible to 'hint' svgs so they are as sharp as possible?\"* answered in "
 "kind) · **THE THREE DIALS — his own frame, layers is dial 1, the tone-of-voice temperature map was OFFERED AS DIAL 2 "
 "AND REFUSED (*\"no dial 2 isn't right. I'll take a look\"*), and the third is unknown and HIS** · **THE THEORY DOOR / "
 "THREE POSTURES** — his *\"what harm is there to an agent having the principle as guidance … make it the hyper-designer "
 "I'm aiming for\"* and *\"other modes that aren't so strict … form opinions instead of simply following a rules decision "
 "tree\"*, answered by the conductor with strictness on the GRADE not the mode and postures obey / weigh / argue, and "
 "his *\"this all sounds great, I really like this idea\"* — ⛔ **AN IDEA HE LIKED, NOT A RULING: ONE PAGE WHEN HE ASKS, "
 "NOT BEFORE** · **`col26-012`, the ONE rule note he did not take** · `W-282a` · `W-282b` · **`W-282ll` \"Ask create\"** "
 "(*\"in the future we will re-integrate this material as an AI readable version of create\"*). "
 "⚙ **GAUGE, MEASURED AT THIS SEAT against the conductor's own transcript** `007425ee-af8f-4c21-bd81-dd1a56befbc3.jsonl` "
 "— the session's top-level window, this wrap seat being a subagent log beneath it, which is what makes the subtraction "
 "legal: **FILL 337,559 real over 141 turns** against **326,763 real / 137 turns DECLARED** at the brief cut ⇒ **delta "
 "10,796**. ⛔⛔★★★ **THE 256,000 HARD LINE IS BREACHED BY 81,559 — THE THIRD BREACH ON THE RECORD after #277 and #281, "
 "and by far the largest — 157,559 past the ruled 180,000 stop line and 117,559 OUTSIDE the ≤220,000 tolerance.** "
 "⛔ **The conductor DID NOT GAUGE between the logo review landing and the horizontal clear-space ruling and cut two "
 "Opus lanes past the wall**; Dave asked *\"whats the context temp like, can we squeeze it in?\"*, was told no, and "
 "answered *\"ouch, better wrap\"*. **BOOT 77,474 real, n=1** against the `s129-D1` floor 70,794 — **+6,680, NOT a "
 "re-base**, `BOOT_FIRSTTURN_TK` untouched and n=1 published as n=1; confirmed first-hand here, agreeing to the token "
 "with the brief. ★ **subs 546,920 across n=3** — QUOTA and never FILL — written because the harness MEASURED each "
 "lane (RN 163,406 · LR 190,478 · LL 193,036). ⛔ **NO PACE PANEL WAS ASKED FOR AND NONE IS INVENTED.** "
 "⛔ **`/sessions` 99%** (145,964 KB free here; the sandbox was rebuilt overnight from 100%). "
 "⛔ **SIX BLOCKING GATE FAILS CARRIED IN THE `#243` FORM — the EIGHTH consecutive wrap on that path — every one of them "
 "another session's append-only testimony in `notes/_GAUGE-LOG.md`** (the boot-drift ceiling breach and five boot "
 "double-counts: #243, #264, #272, #273, #274). ⛔ **A WRAP MAY NOT REPAIR AN INHERITED GATE FAIL and this one did not "
 "try.** ✅ **A SEVENTH WAS RED AT THIS SEAT AND IS HEALED HERE — `notes/_RULINGS.html` was STALE against "
 "`_rulings.json`** after six rulings landed and no lane re-rendered it; rebuilt and staged at step 4d, the `s263-D10` "
 "case exactly, and **the same fail #281 met and healed one session ago**. "
 "⚠ **TWO INSTRUMENTATION APPENDS WERE COMMITTED AT `3f009cc` TO CLEAR THE PUSH GATE and two more accrued during this "
 "ritual; the POLICY on them is still Dave's (dream pass 6 P2, floated).** Gauge, declared skips with their sizes, the "
 "cloud-store result and not-done: the ⏱ LATEST DELTA below. "
 "**`_CARRIES.md` § `## residual → #283` is the carry set (`s225-D2`); the banner carries the pointer and the probeable "
 "count.** **This wrap's own filed report (`s218-D7`): `notes/_subreports/2026-09-18-282-W-wrap.md`.** "
 "**Narrative dossier (1b): `_DECISION-HISTORY/2026-09-18-282-the-rule-notes-land-and-the-logo-is-ruled.md`.** "
 "**His words verbatim: `notes/_lanes/282/DAVE-RULINGS-2026-09-17.md`, with his two exports beside them.**)*  "
 "Previous: "
)

OLD_HEAD = "*Last refreshed: 2026-09-17 (Thu from `date` — **#281 wrap**."
NEW_HEAD = "2026-09-17 (Thu from `date` — **#281 wrap**."

orig = open(LS, encoding="utf-8").read()
assert orig.count(OLD_HEAD) == 1, ("anchor must be unique", orig.count(OLD_HEAD))
new = orig.replace(OLD_HEAD, NEW + NEW_HEAD, 1)
assert new.count("*Last refreshed: 2026-09-18") == 1
assert len(new) == len(orig) + len(NEW) + len(NEW_HEAD) - len(OLD_HEAD)
if "--write" not in sys.argv:
    print(f"DRY: new segment {len(NEW)} chars; file {len(orig)} → {len(new)}"); sys.exit(0)
open(LS, "w", encoding="utf-8").write(new)
print(f"WROTE: new `Last refreshed` segment, {len(NEW)} chars; file {len(orig)} → {len(new)}")
