# #304 Run 6 seat 6b — three decision pages for Tuesday: the CI calls, the uncertain stamps, housekeeping and lines

provenance: 304 · 2026-09-26 (Saturday evening) · Run 6 seat 6b (Opus 5.5), dispatched by the #304 conductor · repo HEAD `571d458c` plus Runs 1 and 2 in the working tree · no commit, no push
status: observed for every count (printed by `notes/_lanes/304/R6b/counts.py` → `counts.json`); the kind assignment of the 109 is this seat's hand reading; every recommendation is a recommendation. Nothing ruled, stamped, closed or parked.
window: UNMEASURED (a seat cannot read its own usage)
COUNTS: pages 3 · decisions 25 (4 + 10 + 11) · decision boxes 38 · renders 6 (1440 + 390 × 3), overflow 0, clipped 0, console errors 0, broken images 0, broken links 0 · badge photographs 8 (2 snippets × 7px/8px × row + chip) · uncertain rulings sorted 109 into 6 kinds, asserted exhaustive and exclusive
CITES: s295-D2 · s295-D3 · s251-D6 · s219-D4(2) · s294-D5 · s260-D2 · s271-D1 · s272-D93 · #74-D1 · the plan (Run 6, "What you decide" 2–5, 7–10)

## THE ANSWER FIRST

Three pages, built from the house CSS and the decisions overlay copied out of `notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html` (never redrawn), answer first, each decision a plain question with a recommendation, a one-clause why and a decision box; ruling ids and paths only in each page's Technical section.

1. `notes/_DECIDE-304-ci-calls-2026-09-26-v1.html` — 4 calls: badge 8px · declare all four forks · port the chain script now · retire the seven #268 drivers. The schema is cross-linked to R6a's `notes/_DECIDE-304-schema-2026-09-26-v1.html`.
2. `notes/_DECIDE-304-uncertain-stamps-2026-09-26-v1.html` — 10 calls: six kinds for the 109 (carried 6 · overtaken 10 · in force, nothing to build 14 · half built 7 · no trace 8 · in the tree, no commit names it 64), retire s135-D3, park s114-D2 + s246-D3, move P-272-1/P-277-4 to enacted, close doc rows at birth then flip REGROWTH_BLOCKING after the 75.
3. `notes/_DECIDE-304-housekeeping-and-lines-2026-09-26-v1.html` — 11 calls: Friday closes (95) + what came back + the Common prompt · park 102 stale questions · close 22 release rows, cut v1.0.14 on Tuesday's evidence, which pack is on the work machine · inscribe 256K/300K and 236K/276K · boot ceiling 130,000 until the Mac seat · token to a credential helper · 17 passed-event rows · the 14 legacy dispositions · carry diet 342 of 709 · park 12 component-wave rows · park 20 unreturned exports.

## CORRECTIONS FOUND ON THE WAY (each stated on its page)

1. **"Four chart forks" is three chart forks and one table fork.** `_validate_token_forks.py` at the seat today: `--status-positive`, `--status-negative`, `--status-neutral` (bar `canon.css:7432-7435` graphic tones vs sparkline `:9804-9806` ink tones) and `--cell-py` (`.cn-table` 10px `:2879` vs compact data grid 4px `:10646`). A4 and the plan named two tokens. Contrast vs white: bar 3.07 / 3.42 / 3.13, line 5.09 / 5.09 / 17.4.
2. **The badge at 8px moves nothing for one digit.** min-width 24px holds; "12" 27.92 → 29.92, "128" 34.89 → 36.89 CSS px (HSBC_MtUnivers_Latin forced and asserted). The glyph-parked counts use their own 4px and are untouched; Tab-bar's reference shows no 7px chip at 1440.
3. **The boot-ceiling premise.** A2 and the plan read Dave's #301 19:45 "raise the ceiling" as pointing to `BOOT_CEILING_TK`; `_HANDOFF-152` records that at 19:47 ("1. is right, might be a good experiment.") he chose the WINDOW over the boot ceiling, which stayed 72,768. The page puts 130,000 to him as overruling himself twice (s295-D3 and 19:47).
4. **A2's counts after Run 2.** Union 305 → 301 live (D2 105 → 102, D3 23 → 22); D4's 58 is A2's keyword upper bound and is not a call of its own.
5. **s229-D2** was listed "not traced" by Run 2 but its own text says the fix landed the same day; placed in kind 6 (content probe), not kind 5.
6. **s216-D1** is in both Run 2's UNCERTAIN list and the eleven; counted in kind 5 and routed to the delivery-shape page.
7. **Bare `ruled` now reads 245** by an exact-string count (Run 2 reported 248 by its own counter); the page quotes Run 2's figures only.

## RECEIPTS

- `notes/_lanes/304/R6b/counts.py` → `counts.json`: the kind assignment (asserts 109, no duplicates, no unknown ids), A2 lists vs the live store, carry classes (342 = 111 + 58 + 57 + 23 + 93 series; asserted 342 + 367 = 709), R1 verdicts (130 / 9 / 7 after, 127 / 15 / 4 before), fork contrasts.
- `render_badge.py` → `badge_measure.json`, `shots/badge-*.png` (3×, `file://`, font asserted). A first run over-applied 8px to Tab-bar's glyph-parked chip; fixed (only computed-7px chips move), its shots moved to `shots/_superseded/`.
- `build.py` (fills every `%%TOKEN%%`, asserts none left, asserts each copied block appears once) · `render.py` → `render_report.json`, `shots/{ci,stamps,house}-w{1440,390}-*.png`. Looked at by eye: CI page all of 1440 and 390 parts 1, 4, 5; stamps 1440 parts 1–3, 6–7, 390 part 5; housekeeping 1440 parts 1–6, 390 part 6. Fixed on sight: figcaption and swatch labels inheriting `.beats b` block/18px, the four-up stat labels wrapping (now two-up), ids breaking mid-token in the Technical lists, three wording errors (dates, "four parts", the boot-ceiling order).

## FOR THE CONDUCTOR

- The pages link to R6a's schema, delivery-shape and when-rules pages by their filenames in `notes/` (all present at render time).
- The CI page reads Run 1's clone verdict. After the wave-1 push, if CI's failure set differs by name, the "130 / 6 / 3 / 7" block and the red table need one rebuild (`python3 notes/_lanes/304/R6b/build.py` after editing `counts.py` inputs).
- Doc rows owed for the commit seat: this report; the three pages are review surfaces under `notes/`.

## NOT DONE, BY FENCE

No git write, no `git status`, no commit, no Project memory, no store write, nothing inscribed. The "in force, nothing to build" and "part-enacted" status words are proposals; whether `--set-status` should carry them is part of Dave's answer. Estimates on the pages are labelled.

## FILES

- `notes/_DECIDE-304-ci-calls-2026-09-26-v1.html` · `notes/_DECIDE-304-uncertain-stamps-2026-09-26-v1.html` · `notes/_DECIDE-304-housekeeping-and-lines-2026-09-26-v1.html`
- `notes/_lanes/304/R6b/`: `ci.src.html`, `stamps.src.html`, `house.src.html`, `common.css`, `counts.py`, `counts.json`, `build.py`, `render.py`, `render_report.json`, `render_badge.py`, `badge_measure.json`, `shots/`
- this report
