# #297 lane R2 — typography, alignment and layout, all 16 slides

provenance: 297 · 2026-09-22 · lane R (pass run by the review conductor — no Agent tool at this seat)
status: observed — analysis and ideas only; the deck was not changed
deck: `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html` at `57e885b0`
measured: `notes/_lanes/297/R/measure.py` → `notes/_lanes/297/R/_measure.json` — Playwright, every slide via `deckGo(n)`, computed styles, bounding boxes, word-level line boxes, rail title rect vs every text line box (8px clearance). Viewports 1440×900, 1680×1050, 1920×1080.
font caveat: the stack asks for "Univers Next", then "Helvetica Neue". Neither exists at the render seat (fc-match → DejaVu; Chromium falls to the Helvetica alias, Nimbus Sans / Liberation Sans). The bank's Univers IS installed at the seat, as family "HSBC_MtUnivers_Latin", which the stack never names. On Dave's Mac the deck most likely sets in Helvetica Neue; line breaks may move by a word.

## 1 · The rail collides almost everywhere at laptop width

Rail title: fixed, left 72px, 12px/500/.14em; right edge 166–195px ("THE ASK" … "EVALUATION"); centre y = 0.38 × viewport height.
Content left edge = max(6vw, (W − 1120)/2 + …) — 160px on standard slides, 86px on the drawing cards 07–10 (their grid is 1360 wide) at 1440.

| viewport | slides where the rail title touches or overlaps content |
|---|---|
| 1440×900 | 03, 04, 05, 06, 07, 08, 11, 12 (plate 01's keyline), 13 (tile 12), 14, 15, 16 (eyebrow dash) — **12 of 14**; 09 and 10 stack two red labels 5.5–6.9px apart |
| 1680×1050 | 07, 08, 09, 10 (the 1360 grid) |
| 1920×1080 | none |

Thresholds (computed): standard slides clear from ≈1540px wide; drawing cards from ≈1780px. The known list (06, 07, 08, 11) understates it.
**Fix options:** (a) reserve a gutter — `.slide{padding-left:max(6vw,232px)}` plus `#s10map` (it sets its own padding); rendered at 1440 it clears every slide (content x 232–233 vs rail right ≤195) — `notes/_lanes/297/R/sketch/`; (b) drop the rail title below ~1780px and keep only the numbered circle; (c) present only at ≥1920 wide — fragile, depends on the room. Recommend (a).
**Also:** hide the rail on 16 as on 01/02 — the close shows "5 THE ASK" beside the payoff.

## 2 · Type in use (1440×900, CSS px)

| role | sizes in use | weights |
|---|---|---|
| wordmark | 132 (01), 124 (16) | 600 |
| headline h2 | 64 (03 05 06 12 14), 53.28 (04), 42 (13), 40 (02 11), 34 (07–10) | 300 + 600 split; all-600 on 03 06 12 13 14; all-300 on 02 |
| lead | 26 (03 05 14 15), 19 (07–10), 32 close line, 40 ask | 300 |
| body | 16.56 (06), 16 (15), 15.84 (04), 15 (08 09 11), 13 (12), 11.5 (13) | 400 |
| diagram title | 22 (06), 18 (12), 15 (13) | 600, 600, 500 |
| eyebrow | 12 / 500 / .14em caps — consistent | |
| diagram labels | 13, 12, 11.5, 11, 9.5, 8.5 mono | 600, 500, 400 |
| foot | 12 — consistent | 400 |
| page number | 13 | 400 |

≈27 distinct sizes. Proposed ≈11: wordmark 132 · headline 64 / 40 / 34 · lead 26 / 19 · diagram title 18 · body 16 · label 12 · foot 12 · (02's numerals 48 and the hub 55 as named exceptions).
Weight rule already half in use: light = set-up, bold = the point. 07 runs it backwards ("**The first improvement:** the catalogue…") against 08–10.

## 3 · Breaks, widows, runts

- 04 h2 (53.28px, 3 lines): "…available. The / work checked automatically and by a / human." — the bold sentence opens with a lone "The" at the line end and ends on a one-word line.
- 06 h2 (64px): "We asked: what else is slowing / design?" — one-word last line.
- 10 h2 (34px): "Fourth: a designer's / judgement, built into the / system." — one-word last line.
- 11 h2 (40px): "…three things / at once." — runt.
- 06 cause titles wrap 2 / 3 / 2 / 4 / 1 lines → the five descriptions start at four different heights (538, 567, 538, 596, 509 px).
`text-wrap:balance` is used only on 02's headline and the cover subtitle. Rendered on all h2 it fixes 06, 10 and 11; 04 also needs a break before "The work".

## 4 · Alignment

- **Two left edges:** 160px (standard) vs 86px (07–10) at 1440 — the eyebrow and headline jump 74px left at 07 and back at 11. At 1920: 400 vs 280.
- **No top line:** every slide is vertically centred, so the eyebrow sits anywhere from y 48 (13) to 329 (01): 01 329 · 02 317 · 03 238 · 04 149 · 05 258 · 06 188 · 07 289 · 08 260 · 09 313 · 10 312 · 11 228 · 12 112 · 13 48 · 14 290 · 15 214 · 16 324. The headline moves on every advance.
- 12: the plate content box is 328×217; the brain print is contained at 0.317, the others at 0.517.
- 11: card centres 316 / 720 / 1124 vs chip and bus centres 320 / 720 / 1120 — 4px, not worth a change.
- 13 at 1440×900 fills y 166–851; page number at 852. Tight, but clear.

## 5 · Recommended

Before Friday: the gutter; hide the rail on 16; balance h2 + one manual break on 04; three headline sizes (04 → 40, 13 → 40); flip 07's weights; one wordmark size (16 → 132).
After Friday: one left edge for every slide (flush-left inner rather than centred); one top line for content slides (≈17% down), statements stay centred; decide the typeface — name the house Univers in the stack or stay on Helvetica Neue on purpose.
