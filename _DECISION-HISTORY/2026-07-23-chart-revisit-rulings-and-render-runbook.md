# 2026-07-23 — Chart-revisit session 1: two rulings, a runbook, and Dave's eye beating the machine

*Fable solo (chart-revisit session 1, brief `notes/_briefs/2026-07-23-chart-revisit-fable-brief.md`).
Landed WHATs: ADR-0015 (behaviour partials) · DV-D07 (`_DATAVIZ-DECISIONS.md`) ·
`knowledge/_RUNBOOK-render-verify.md` · `reviews/DATA-AXIS-GRID-2026-07-23-v1.html` ·
two `_FUTURE-STATE` entries + the responsive-type entry. This dossier is the WHY/HOW.
Spine: `_LIVE-STATE.md` 2026-07-23 Fable delta. Wrapped at Red, ~16:00 BST.*

## Arc 1 — Q6 from "show me" to a two-channel schema

Dave asked to *see* Q6 (mint `data/axis`+`data/grid`) rather than rule blind. Survey first: the five
chart snippets ink chrome as `ink@0.6` (axis) and `ink@.10/.16` (grid) because R-D16 left the kit's
greys homeless — worker D receipted the gap rather than inventing tokens (correct governance). The
sheet showed the flattened equivalents bracketed by ramp steps (light axis #767676 sits between
neutral/7's 6.10:1 and neutral/8's 3.95:1), so the decision became "which step", not "what colour".
**The ruling then moved twice, and both moves were Dave's:** (1) option 1 (solid snaps) accepted BUT
amended — *"store a null or 100% value plus the colour … many levels to pull on"* — which is not a
compromise between options 1 and 2, it is ADR-0010's declared-slot posture + ADR-0009's two-channel
physics arriving at the dataviz tier; (2) the ID: my reflection said DV-D06, the ledger said DV-D06
was taken (delta indicators) — **the ledger won, the ruling is DV-D07.** Lesson re-proven: reflect
back before inscribing, and read the ledger before naming. Gate consequence inscribed with the
ruling, not deferred: alpha<1 ⇒ contrast computes from the composite, or dv-016 lies.

## Arc 2 — the render runbook: a misdiagnosis corrected by running the thing

Dave: *"there should be a runbook for chromium and playwright btw."* He was pointing at a structural
fault, not asking for a document: the recipe lived in agent memory — a Polaroid holding a durable
rule. Standing GOOD-MORNING said the 07-22 sessions' downloads were REFUSED; render-verify was OWED
everywhere. **Running the pipeline fresh falsified the standing claim:** the download SUCCEEDS; what
fails is the installer's host-requirements validation AFTER the browser lands (exit non-zero, cache
populated). The 07-22 "refusal" is consistent with reading that exit as a download failure and
stopping. Runbook rule born from it: **check `~/.cache/ms-playwright/` before believing a refusal.**
Second find: a fontconfig alias (`"Univers Next for HSBC"` → `HSBC_MtUnivers_Latin`) makes every
repo file render real-font with zero CSS edits — removes the last friction from in-sandbox
real-type verification. ADR-0013/0014's owed render-verify is UNBLOCKED by this (still owed until
run). The runbook carries the whole failure-mode table dated; memory demoted to a pointer.

## Arc 3 — three defects, all caught by eye or render, none by mechanics

The Q6 sheet passed node-parse, anchor checks, and python-verified contrast maths, then:
1. **First render** caught dark-on-dark dial text (dials inherited page ink inside the dark stage).
2. **Dave's browser** caught the specimen scaling — `width:100%` against a 320-unit viewBox let text
   and strokes scale with pane width (~3× at his window): accidental fluid type, the exact physics
   DV-D02 bans, distorting the very grid-weight judgment the sheet existed for.
3. **Dave again** — *"it never seems to hit 12px"*: the specimen was AUTHORED at 11px, sub-floor,
   off-scale. `reviews/` isn't gate-globbed (gate-scope rule working as designed — reviews are
   scratch), so nothing fired.
Fixes: dials = page-ground chrome strip; svg pinned 1:1 (`width:320px; max-width:100%`, shrink-only);
text = `t-cm-legal` metrics (12/400); proof = measured 320px svg + identical label boxes at 1400 AND
840 viewports. **Runbook amended same hour: render responsive surfaces at ≥2 widths** — one width
proves one layout, nothing else. The meta-lesson for the minimal-review ambition: mechanical gates +
one render ≠ seen; the verification ladder gained a rung.

## Arc 4 — the seam Dave's eye surfaced, now Q8

Chasing the 12px question exposed a real corpus inconsistency: the 07-22 proforma label snap went to
12/**500**, canon chart snippets bind `t-cm-legal` = 12/**400**. Two live label weights. Dave's
standing instinct ("base = lowest size + MEDIUM") is one candidate answer; the exemplar build must
not pick silently — **flagged as chart-revisit Q8.**

## Also this session (logged, not built)

ADR-0015 accepted on Dave's one-line confirmation with the constraint made GATEABLE (≤16KB source —
observed proforma baseline 9.9KB raw/3.2KB gz — + banned patterns + delegation/rAF + JS-off
survival). Theme-builder **channel dials** + **token compressor** (assessed: bytes wrong scoreboard;
subsetting/governance/flattening real, flattening-vs-runtime-theming = the dial) + **curve-snapped
responsive type** (verified: NO fluid type exists anywhere today; responsiveness = layout only,
mixed `@container`/`@media`) — all in `_FUTURE-STATE` with verbatim anchors.

## Open at wrap

Chart-revisit Q2–5, 7 + **Q8 (label weight)** · the 16-Q batch + dataviz sign-off · scatter eyeball ·
render-verify for ADR-0013/0014 (unblocked, owed) · NEXT: Chart-line exemplar, fresh full-budget
window.
