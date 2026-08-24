# Sub brief — live bento parameter tuner (#217, Opus build sub)

**Dave's word (#217, verbatim):** *"We need to promote all the various types of bento to canon, i just need to decide on some of the parameters like gutters etc"*.

**What this is:** a DECISION CONTROLLER, not the promotion. Promotion is Dave's ruling and it fires when he exports chosen values; the tuner is how he decides. Precedent: the live radius/corner tuner (BUILT+RULED #199) — grep for it and follow its conventions (controls layout, live readouts, export affordance).

## Context (verified this session)
- The four bento types (#216, all AWAITING his eye — copy, never re-draw): `knowledge/_fitness-test/bento-gallery-showcase-v1…v4.html` — v1 presets · v2 photography gallery (masonry/grid + zero-JS lightbox) · v3 container-query full-scale · v4 12-col snap designer.
- The Foundations photography page (this session) uses: fixed rows + `1fr auto` tiles, every-5th-tile 2×2 emphasis (PROPOSED, position not preference), span thresholds 4:1→3 cols / 1.45:1→2 / 1:1.15→2 rows (PROPOSED). These are exactly the open parameters.
- Real content: `knowledge/assets/photography-web/` (12 derivatives) + mixed card content in the style of the showcases.

## Scope
1. One page: `knowledge/_fitness-test/bento-tuner-v1.html`. Live dials for at minimum: **gutter/gap scale · outer padding · row height · aspect→span thresholds · emphasis rhythm (every Nth, and N=off) · tile radius**. Add container-query breakpoint bands if v3's machinery makes it cheap; skip if it muddies the page.
2. Preview on REAL content — a photography bento and a mixed-card bento side by side or switchable, so a dial moves both.
3. **Four themes × light/dark** switchable in-page; live contrast readouts where text sits on tinted ground.
4. **Export**: a button that produces the chosen values as a mint-ready block (JSON + CSS custom properties) rendered on-page for copy — mint-time derivation discipline (`s200-D1`): the export is concrete values, no live var chains.
5. Current in-force values pre-loaded as the starting position, labelled PROPOSED-NOT-RULED.
6. Render-proof per `knowledge/_RUNBOOK-render-verify.md` (read first; no `set_content`; chunk near 45s). Probe: dials actually move the grid (drive one dial, measure a computed gap change), export block contains the dialled values, dangling-var check across all 8 states.
7. Rows: store row at creation, `_REVIEW-SIGNOFF.md` AWAITING row, DS defects by addition.

## DO-NOT-RULE (hard fence)
- NO canon minting, no canon.css/token/theme edits — the promotion happens after Dave exports, not here.
- No default-parameter judgments presented as settled — everything dialled is proposed until he rules.
- `knowledge/_rulings.json` READ-ONLY. No gauge/lane/worklist edits. No commit/push, no git-checkout/reset.

## Pitfalls to carry (mandatory replay, Dave #165)
- (a) A tuner whose export differs from what the preview showed is worse than no tuner — the export MUST be generated from the same state object that drives the preview, proven by the probe.
- (b) Radius interacts with the segmented-switch carve-out (radius tuner v2 territory) — bento tile radius is in scope, component-level radii are NOT; say so on the page.
- (c) Dave is astigmatic; red/yellow hues are unstable for him — keep controller chrome to stable hues (blue/green/neutral), content untouched.
- (d) Version don't overwrite (`-vN`); mv to `_to_delete/`, never rm.

## Report back (replayed in-window)
Path · dials list with ranges · probe evidence (dial-drive measured, export parity, 8-state vars) · rows · residuals · what a failed probe would invalidate · token spend.
