# #104 — A unit error in a measurement brief, and an enactment that passed its own mutation test while being broken

provenance: kind-peaceful-lamport #104 · 2026-08-05
status: observed

## The arc

**1 · The chain-diet brief opened on Dave's own words, and his words were a cross-unit comparison.**
The #104 worklist carried a chain-size complaint from the opener: *"`_CHAIN.md` is 10,288 real vs
its 4,917 warn line"* — an apparent ~109% overshoot, big enough to justify an aggressive cut.
Measuring before cutting (the six-beat ladder's own discipline) found the premise was comparing two
different units: `CHAIN_BUDGET_TK = (4917, 6417)` (`_capture_gate.py:1035`) is denominated in
**tape** (cl100k) — its own consumers print `warn … tape` (`:2208,:2216`), and the #48 restatement
calls it *"the measured 417-**tape** wrapper"*. The 10,288 figure is **real** Claude tokens
(`_gauge_tokens.count`). Measuring both units on the artefact, never converting one into the other:
`_CHAIN.md` = **6,577 tape** vs the **4,917 tape** warn line — over by **1,660 tape (34%)** — and
separately **10,292 real** (`_gen_chain --check`: `FILE 10,292 real = slice 7,724 + wrapper 2,568`).
The cross-unit pairing implied roughly double the real overshoot, and a diet sized from it would
have cut roughly twice what the chain actually needs to clear its ceiling.

**2 · This is not a new mistake — it is the fourth recorded instance of the identical mechanism.**
`_capture_gate.py`'s own comment history names the pattern: #54 ruled the unit (real tokens, never
convert), #80 re-discovered the ruling from scratch because the vocabulary had no word for "real",
#82-D1 enacted the fix, and #90 caught the same defect living inside the size-stamp line itself. A
planning brief written this session, working from Dave's own opener sentence, reproduced it a
fifth time — which is the point worth keeping: **the instruction was right and the premise inside
it was stale**, and verifying a premise against the source (`_capture_gate.py`'s own constant
definition, not the sentence that quoted it) is what caught it before a cut was sized from it.
[[measure-dont-convert-units]] [[tape-unit-is-not-real-tokens]].

**3 · Where the real weight sits, once the unit was fixed.** The GM standing header carries 4,787
real — 46.2% of the whole chain — and three lines inside it are 3,718 real (36% of the file): `H2`
STATE (1,437), `H4` PRICE (1,274), `H1` SIZE STAMP (1,007). All three are fat with accreted
`⛔ CORRECTED AT SOURCE #N` provenance narratives (nine of them). A cut sized ~2,000–2,600 real is
homed in `notes/_briefs/2026-08-05-104-chain-diet-measurement-brief.md`, **not enacted**: it is
[[home-by-addition-then-cut]] surgery on Dave's own canon header, and two prior sessions (#87, #94)
both blew the stop line attempting exactly that kind of surgery at peak fill. It also collides with
an already-open item, `G5` (the four advisory size caps as a set, closing when re-measured in real
and Dave ratifies) — the cut needs no ruling, but the TARGET the caps get re-measured against does.
Rolled to #105, to be enacted at wrap-open rather than late in a window.

**4 · Separately: ds-029's #103 enactment was declared done on evidence that could not see its own
defect.** #103 ruled a second Replay-detection idiom (direct `@keyframes`/`animation:`, alongside
the existing `dv-animate` class toggle) and declared it enacted on two pieces of evidence: a
selftest (11 bites) and a mutation test (removing the detection clause disabled Replay both ways).
Both passed. The #104 worklist carried "replay visual confirm" as owed rather than assumed — not
because anything looked wrong, but because it was the one piece of evidence #103 had not produced.

**5 · Driving the real page found the mutation test had been testing the wrong half of the
feature.** Clicking Replay on the real `Confirmation` page restarted three of its four animated
elements (`.confirm__title`, `.confirm__msg`, `.confirm__actions`) but not the fourth: `svg.success`
stayed at `currentTime = 460, finished` — visually inert. The detection clause #103's mutation test
exercised was working correctly (it correctly identified that `svg.success` has an animation and
should restart it); the RESTART MECHANISM the detection clause hands off to was silently failing
for that one element only.

**6 · The cause: a well-known DOM API is HTMLElement-only, and the loop treats every element the
same.** The restart trick in both idioms is a reflow-forcing read between setting `animation:none`
and restoring it — `void el.offsetWidth` in the original `dv-animate` idiom, and the same pattern
carried into ds-029's generic `querySelectorAll('*')` loop for the second idiom. `offsetWidth` is
defined on `HTMLElement`; per the CSSOM View spec it does **not** exist on `SVGElement`. On a bare
`<svg>` root, `void el.offsetWidth` reads `undefined` and forces nothing — the browser never
flushes the `none` state, so the `none→prev` toggle collapses into a no-op and the animation simply
never restarts. Every other element ds-029 touches happens to be an HTML element, so the defect
had exactly one failing member in the entire showroom and nothing else exposed it.

**7 · Why a mutation test — normally strong evidence — could not have caught this.** A mutation test
proves that the code you deliberately broke was load-bearing for the behaviour you asserted. #103's
mutation removed the *detection* clause and asserted Replay stopped working; that is a true and
useful test of detection. It is structurally incapable of exercising a defect that lives in the
*restart mechanism* the detection clause calls into, because the mutation never touches that code
path — it removes the caller, not the callee's most fragile line. **The general lesson, worth
carrying forward: a mutation test proves the mutated clause is load-bearing; it does not prove the
feature works end to end.** That gap is exactly what "logic-verification is not the same as
click-observed" was naming when it registered the visual-confirm item as owed rather than closing
ds-029 on the mutation test alone.

**8 · The fix, and proving it both ways.** `void el.getBoundingClientRect()` replaces
`void el.offsetWidth` at `knowledge/gen_showroom.py:285` — `getBoundingClientRect()` is defined on
`Element` itself (the common ancestor of both `HTMLElement` and `SVGElement`) and forces layout for
either. Showroom regenerated (75 pages). Proof, all four Confirmation elements, before → immediately
after click → settled: `svg.success` 460,finished → **0,running** → 460,finished;
`.confirm__title` 500 → **0,running** → 500; `.confirm__msg` 580 → **0,running** → 580;
`.confirm__actions` 660 → **0,running** → 660. Mutation-tested in both directions: reverting the
one-line fix reproduces the `svg.success` defect exactly (the three text elements still restart,
confirming the defect is scoped to the SVG root, not a general regression); restoring the fix
returns all four to green. Snippet and showroom gates re-run green throughout.

## Resolved / open

Resolved: the chain-diet brief's unit (measured, both units, homed — not converted); the ds-029
enactment defect (root-caused, fixed, mutation-tested both directions, gates green).

Also landed same window, mechanical rather than reasoning-heavy (not the subject of this dossier,
recorded for completeness): **#97 flag ② CLOSED** — `.shell{align-content:start}` at ≤760px
(`gen_showroom.py:338`, one line), gap `intro.top − tree.bottom` measured 700px 322.5px→24px and
375px 259px→24px (24px = `.intro`'s own padding-top), 1180px rects byte-identical before/after.

Open → #105 (rolled, none ridden past the stop line): ① the chain-diet cut itself — measured, homed,
sized, NOT enacted; enact at wrap-open, not late ② memory-compaction pass (`MEMORY.md` →
`MEMORY-ARCHIVE.md`, sized by entry COUNT 113 — a count, not a measurement; the memory dir sits
outside every sandbox mount) ③ Dave's eye on legend-centring, Option A (−109px, constant) vs Option
B (0px) — `reviews/LEGEND-CENTRING-SPREAD-2026-08-05-v1.html` ④ Dave's word on `--pri-hover`
promotion (measured, not decided) — `reviews/PRI-HOVER-MEASUREMENT-2026-08-05-v1.{md,html}` ⑤ the
`type.css:180` dark-mode specificity finding — corpus-wide, pre-existing, unruled ⑥ ds-029's FIRST
idiom (`gen_showroom.py:273`) shares the same `offsetWidth`-on-SVGElement blind spot the fix at
`:285` closed — flagged, not fixed, because no current snippet puts `dv-animate` on an SVG root
(grepped, none) — it is out of today's failing scope but will bite the first one that does.

⚠ One working-tree path is unattributed this window: `_RESEARCH-graph-engineering-2026-08-05-v1.html`
(repo root, untracked) — no sub reported writing it. Not staged; recorded in `_LIVE-STATE.md` §OPEN,
awaiting Dave.

Links: spine `_LIVE-STATE.md` ⏱ #104 · ledger `notes/_MEMENTO-DECISIONS.md` § ★ #103 (correction by
addition) · `knowledge/_REVIEW-SIGNOFF.md` (#98 row, correction + two new rows) · brief
`notes/_briefs/2026-08-05-104-chain-diet-measurement-brief.md` · fix `knowledge/gen_showroom.py:285`
(and the #97 flag ② fix at `:338`).
