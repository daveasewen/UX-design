# #245 — the reds, then the cut: nine rulings, the ceiling arm discharged, one red left that is Dave's, and v1.0.6 baked PROPOSED

```
provenance: 245 · 2026-09-03
status: observed
```

*Spine entry: `_LIVE-STATE.md` § `## ⏱ LATEST DELTA — 2026-09-03 … #245`. Ledger: `knowledge/_rulings.json`
§ `s245-D1` … `s245-D9`. Banner: `GOOD-MORNING.md` § ★ LATEST #245. Reports:
`notes/_subreports/2026-09-03-245-L4-row-height-renders.md` · `notes/_subreports/2026-09-03-245-L3-composition-edge.md` ·
`notes/_subreports/2026-09-03-245-D-discharge-arm.md` · `notes/_subreports/2026-09-03-245-R-reds.md` ·
`notes/_subreports/2026-09-03-245-L2-populate.md` · `notes/_subreports/2026-09-03-245-K-rung-ladder.md` ·
`notes/_subreports/2026-09-03-245-L5-cut.md` · `notes/_subreports/2026-09-03-245-wrap-brief.md` ·
`notes/_subreports/2026-09-03-245-wrap.md`. Review surfaces: `reviews/ROW-HEIGHT-RENDERS-2026-09-03-v1.html` ·
`reviews/RUNG-LADDER-2026-09-03-v1.html` · `_REVIEW-L3-composition-edge-2026-09-03-v1.html` ·
`reviews/RELEASE-SPIDER-2026-08-26-v1.html` (rewritten by the bake). Both-way: each of those files names this
dossier's session.*

*This is the WHY and HOW. The WHAT — figures, paths, hashes, receipts — lives in the ⏱ delta, the banner, the
stratum and the nine reports, and is not restated here except where the reasoning needs the number.*

---

## 1. Why the reds came first, and what each red turned out to be

Dave opened with *"lets get 1.0.6 ready for tomorrow, use fable liberally, watch out for dependencies"*, and
`s244-D2` had already fixed the order: the reds, then the tuner. The reasoning behind that order was not
tidiness. A release is a claim that the gates are green, and CI run #482 had painted the `gates` job red on
the very commit (`9628bae`) whose content the release would carry. Cutting over a red CI would have shipped a
zip whose own proving job disagreed with it.

Lane R's method was the one that worked at #194: reproduce at a BARE CLONE with CI's own `--timeout 60`, not
in the working tree, because the working tree carries local drift CI never sees. That is how it separated
**[61]** — red locally, refused as 77 (the legal "cannot measure") in CI — from the four that CI actually
fails on: [13] [18] [124] [136]. The lesson that survives the session is the split itself: **a red you can
only reproduce in the working tree is not the red CI is showing you.**

Each red had a different owner, and naming the owner was the work. **[13]** was a Claude-owned fixture that
rotted when the `s241-D2` diet cut 2,415 tape out of the chain the fixture measures — a gate testing a
number that a ruling had legitimately moved; fixed, and the fix proven exit 1 → 77 in the clone. **[124]**
was the `7f8801f` port into the two "frozen" `memento-package` copies — Claude-portable, but with the
`s228-D3` precedent that the last such port rode beside a version move; R recommended holding it for the
cut, and L5 took it inside the cut, which is where it belonged. **[136]** was the manifest saying v1.0.5
with no zip — the cut clears it by construction. **[18]** is two `#218` `section-usage` testimonies in
`notes/_GAUGE-LOG.md` that disagree (`:2276` says R, `:2294` says U), and the reader refuses to pick a
winner by design. R priced three repairs and recommended AGAINST the smallest one — "later wins" — because
silently picking a winner is exactly the behaviour the reader was built to refuse. **So the session ended
with one red, and it is the one no lane could clear without Dave's word.** CI step 6 will stay red until
[18] is ruled, and the wrap says so rather than hoping the next run reads differently.

## 2. Why two review surfaces were built before one line of canon moved

The bento row-height model and the rung ladder are both "just CSS", and the temptation to enact a
reasonable-looking value and move on was real with a release due tomorrow. The reason it was not done that
way is rB's #234 warning, carried on the L4 brief: the nested tile grid and the outer wall are TWO levels,
and a fix applied at the wrong level reads as a fix at both. Lane L4 therefore rendered the three models on
the REAL dashboard wall — the snippet's `<main>` spliced byte-for-byte, cloned into every column so the
columns are identical by construction — and held the outer level fixed at what ships, so the only variable
on the page was the one the question was about.

The page then said something nobody had asserted: under the FIXED model, the shipped rail rung (184px) is
already shorter than the rail tiles' content (247px / 200px) in every theme and mode — the shipped dashboard
was leaning on its floor already, and 8 of the 681 assertions failed on that ONE fact. Dave's ruling came
off that page, not off a description of it: *"Okay it's 2 but I do prefer the spacing on 3."* Model 2 was
the floor with `auto` as its max; the page's toggle showed canon's `1fr` as the alternative, so L4's Q4
resolved with the same sentence. The second half of his sentence — preferring the spacing on 3, the
mis-rung column — was not a contradiction but a clue, and it was lane K's job to read it.

## 3. Why a ladder whose numbers never paint was still the right ruling

Lane K put four ladders under the floor Dave had just ruled and measured the content heights live. Its
first finding was deflating and decisive: **under the floor, a rung below content never paints.** Three of
the four ladders therefore rendered identical rail and chart rows; ladder B's three numbers (120/240/96)
were invisible on the page. Only D (the 2:1 level, 160/548/272) produced rows that were exactly their
rungs.

Dave's answer is quoted whole in `s245-D9` because it is a design position, not a pick: *"the grid snapping
is 4px not 8px, im almost certain … the grid is there to line up adjacent and stacked components, these are
containers that line up anyway, the grid might simply be unnecessary … maybe the attention should be paid
to the components etc and until thats done we just round to the nearest pixel, which would make B the
best."* Read with K's finding 1, B is the honest choice for v1.0.6 precisely BECAUSE its numbers never
paint — the rows become pure content above the floor, which is the spacing he said he preferred on
column 3 of L4's page. D is his stated preference once the constituents are audited for 4px multiples.
**The audit is a carry in his words and was not tonight's build**; the wrap holds that line because the
ruling holds it.

## 4. Why the composition edge was proposed, not populated — and then enacted in the same evening

Lane L3 was briefed to build the `groupsWith` edge for Dave's eye and to populate nothing, and it did that:
a one-line schema fragment, eight proposed edges (four `ref:null` each naming what only he could settle), a
grouping dial DERIVED from the proposed edges through the live generator's own function, and an arithmetic
gate. The gate found a defect by REFUSING: run on the real snippet it returned UNPROVEN, exit 77, because
the snippet never declared its base column count — and the render showed the consequence, a KPI board
stacked 4×1 at 1440 where the snippet's own comment promised 2×2. A gate that refuses honestly where the
artefact under-declares is worth more than one that guesses, and this one earned its C9-BLOCKING seat on
that evidence.

Dave ruled all seven recommendations in one line (*"I'll go with all the recommendations"*), and L5 enacted
them inside the cut. Two near-misses in the enactment are the part worth remembering: `gen_kg_edges.py`
would have silently DROPPED `groupsWith` on its next regeneration, and `gen_canon_bento.py` was rewriting
the PROJECTED copy of its own block inside `.cn-template-dashboard-bento`. Both were generator behaviours
that only show when a new edge type or a re-spliced block goes through them for the first time — the
class of defect a proposal-only lane cannot find and an enactment lane must.

## 5. Why the ceiling arm's discharge was built tonight and not last night

`s244-D1` was ruled at #244 and deliberately not built there, on `s172-D3`(e): an instrument is never built
in the same breath as the finding that motivates it. Tonight lane D built it BY ADDITION: a declaration line
discharges the breach only when every figure on it matches what the gate itself computes, a mis-stated
line fails louder under its own name, and a later over-ceiling reading un-discharges. It was mutation-tested
against the GATE, not against the fixture — eight scratch mutations, all caught, two escapes found and
closed inside the lane.

D also corrected the brief's premise. The brief said the post-breach readings were "#243, #244"; the log
held only #243, because #244's reading was still in `GOOD-MORNING.md`'s stratum and reaches the log at THIS
wrap's 2f roll. A declaration listing #244 would have been a MISMATCH by the form's own rule. D
forward-simulated the roll and showed the discharge stands afterwards and grades #244 fresh. That is why
this wrap could run `_git_commit.sh --wrap` — the first `--wrap` FINAL since #242 — and why the wrap still
carries a question rather than a claim: whether ONE `--wrap` commit at #245 retires the TWO owed at #243 and
#244 is not something a wrap sub may decide.

## 6. Why the cut needed four commits and not two

The L5 brief carried a two-commit recipe: content, then cut. The dry-run refused it — `⚠ DRIFT:
memento-package/_state.json typed v1.0.5 and was stamped to v1.0.6` ×3, and `--check` red on three blobs.
The stamp is byte-neutral only when the repo copies already carry the manifest's version, so the four
carried literals had to be in the commit the manifest is generated AT. That is `f6a8340`, between content
and cut. The fourth commit re-seeds the frozen ledger after the zip is in history — the #228 shape. L5 named
this the #224 class at its fourth cut and priced the derivation (one writer, one gate) as RSQ 2. The
recurrence count is the argument; the fix is Dave's to order.

L5 also touched `_build_all.STEPS` and REVERTED it. Adding the composition selftest moved the step count the
read chain derives (142 → 143), which made `_CHAIN.md` stale and the commit gate refuse — the chain is the
wrap's file, not a lane's. Wiring the gate as an ARM instead and carrying the STEPS entry as RSQ 1 was the
right refusal to make mid-cut.

## 7. Why the citation check went quiet, and why the wrap cited by hand anyway

The wrap's `subreport_citation_check` keys "the last wrap" on the newest commit whose subject opens
`after #<n>`. L5's four commits all open `after #245`, so the check saw `5a196d4` as the last wrap and
reported "none filed since" for seven reports filed BEFORE those commits. A check that reports agreement
because it looked in the wrong window is the [[instrument-without-a-consumer]] class in a new coat. The
wrap cited all seven by path on the banner, in the delta and in its own report regardless, and carries the
blindness as ruling-shaped rather than patching the key.

## 8. What the lanes cost, and what the conductor paid

Seven Fable lanes, no 529 today: 1,604,099 delegated tokens (n=7) — QUOTA, never window FILL. The
conductor's FILL was 157,157 real at his last check-in and ~175,000 at the brief cut, both past the 150,929
advisory, which is why the wrap was delegated; this seat read his transcript first-hand at 183,491 real over
49 turns. Delegation stayed cheap in FILL and dear in QUOTA, as the #110 hook says, and the day's shape —
six build lanes then a serial cut lane — is the reason the conductor's window survived to brief a wrap at
all.

## 9. What is resolved, and what is still open

**Resolved.** Nine rulings in the store. The ceiling arm discharged and the wrap gate green by name. Four of
five reds cleared. L2, L3, L4 and K enacted at their ONE sources. v1.0.6 baked, byte-matched, `--check`
green, PROPOSED.

**Open, and every one of them is Dave's or #246's.** The push, and five `s203-D1` read-backs behind it. [18].
The cold test of v1.0.6 and the ratify / hold word — two acts. The radius candidate set and whether it
scopes to Console or all four themes. The 4px audit, then ladder D and whether the container grid is needed
at all. The #218 duplicate gauge line. L5's RSQs 1, 2, 4; L2's 2; L3's Q7 (c); L4's 3 and 5; K's 2, 3, 4;
D's 1; R's 1. The four UNRULED escapes, `BOOT_BAND_SIGMA`, diet S2/S3/S4/S6 and the `SCHEMA-LOOSENED` word,
each at its own age in `_CARRIES.md` § residual → #246.
