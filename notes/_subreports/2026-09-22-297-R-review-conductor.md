# #297 lane R — review conductor: a review of the plain deck for Friday

provenance: 297 · 2026-09-22 ~22:10–23:10 BST · lane R (review conductor)
status: observed — analysis and ideas only; NOTHING in the deck was changed
deck reviewed: `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html` at `57e885b0` (blob `c68c6640…`, identical to the working tree; re-hashed after every render in this lane — unchanged)

## What Dave gets

- **The review:** `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain-REVIEW.html` (≈1.8 MB, self-contained, 47 embedded JPEGs + inline SVG). One-screen summary (verdict + the eight that matter) → the deck at a glance → 1 diagrams → 2 type and alignment → 3 copy → 4 story and pace → 5 anything else → collapsed Technical.
- **37 numbered suggestions: 32 BEFORE FRIDAY, 5 AFTER FRIDAY** (6, 7, 14, 15, 16). Seven carry the "your words — a question" mark (19 in part, 22 in part, 23, 24, 25, 27, 29).
- **Verdict:** the story holds; the ask is a placeholder, the rail runs into the content at laptop width, and 04 and 11 are drawn in a heavier hand than the drawings. The rest is polish.

## The eight that matter (as ranked on the page)

29 write the ask · 8 give the rail its own margin · 1 (with 2–5) redraw 04 and 11 in the drawings' hairline grammar · 30 move 11 to straight after 06 · 17 make 07's numbers add up (125 + 12 + 8 = 145 ≠ 137) · 18 file names and build numbers off 07/08 (13's paths in 3) · 31 tell the room what the demo builds · 33 the map to a backup slide.

## Findings that correct the record

- **The rail overlap is not four slides.** Measured at 1440×900: the rail title touches or overlaps content on 12 of the 14 rail slides (03 04 05 06 07 08 11 12 13 14 15 16) and stacks under the eyebrow on 09/10; at 1680×1050 on 07–10 only; at 1920×1080 none. Standard slides clear from ≈1540px wide, drawing cards from ≈1780px. A `padding-left:max(6vw,232px)` gutter (plus `#s10map`) clears all of them at 1440 — rendered.
- **04's black and red box borders never render** — specificity (0,1,1,0 loses to 0,1,1,1); computed rgb(215,216,214) on steps 2, 4, 5.
- **07's sum:** 125 components + 12 templates + 8 foundations = 145; the headline's 137 = 125 + 12.
- **12's brain plate** is contained at 0.317 against 0.517 for the 600×420 prints — drawn at 61% of the others' scale.
- **Typeface:** the stack names "Univers Next" then "Helvetica Neue"; neither is at the render seat; the bank's Univers is installed there as "HSBC_MtUnivers_Latin", which the stack never names.

## Filed reports

- `notes/_subreports/2026-09-22-297-R1-art-director-diagrams.md` — inventory, disagreements, one grammar, per-slide keep/change
- `notes/_subreports/2026-09-22-297-R2-typography-alignment.md` — measured type scale, rail collision table and thresholds, breaks, edges
- `notes/_subreports/2026-09-22-297-R3-copy-editor.md` — before → after, his copy marked
- `notes/_subreports/2026-09-22-297-R4-publisher-story-pace.md` — chapters, estimated minutes, seams, recommended running order

## Receipts

- `notes/_lanes/297/R/measure.py` → `notes/_lanes/297/R/_measure.json` (Playwright on the mount via `ensure_env.sh` + `seat_env.sh`, `page.goto(file://…)`, 1440×900 / 1680×1050 / 1920×1080; 85 s, 0 page errors)
- `notes/_lanes/297/R/sketch_render.py` → `notes/_lanes/297/R/sketch/P*.png` — the proposals injected as CSS/DOM at render time only; deck blob re-hashed after: unchanged
- `notes/_lanes/297/R/review_shot.py` — the review page rendered at 1440 wide (top screen + 17 segments), looked at, fixed (SVG tick overlapping a list item; 12/13 comparisons re-stacked for legibility; rail crops re-paired; hero tightened to one screen), re-rendered; no horizontal overflow, 0 page errors. Check renders kept outside git in `outputs/_297R-scratch/`.
- Dave's 22:05 BST words appended by addition to `notes/_lanes/297/DAVE-RULINGS-2026-09-22.md`.

## Deviations, declared

1. **No Agent tool at this seat** — the four passes (R1–R4) ran in sequence at the conductor's seat and were filed under the four names; "four subs" did not happen.
2. The review's "sketch" renders go beyond the brief's SVG sketches: both are present (two hand-drawn SVG pairs + a grammar sheet, and nine CSS-injected renders), each labelled SKETCH.
3. Minutes per slide are estimates (spoken pace), labelled so on the page and in R4.
4. Nothing inscribed; no ruling ids on the page; no push.
