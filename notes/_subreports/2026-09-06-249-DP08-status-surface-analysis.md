# `#249`-`DP08` — DP-08 debt: the two status tiles, and three rendered ways to give them their own surface

session: `#249` · 2026-09-06
window: `W2 debt · lane DP08 (status surface analysis)`
sub index: `DP08`
brief: conductor chat brief (#249, lane DP08) — no `notes/_briefs` file named
tokens: `UNMEASURED — subagent cannot read message.usage; harness counter 15,000,000 − 14,888,342 ≈ 112K QUOTA across 27 tool calls (six PNG reads)`

Evidence lives in `outputs/w2-debt/dp08/` (the lane rule forbids writing under `notes/` beyond this file, so no `assets/` dir was created — see § Evidence).

## VERDICT

DONE. The DP-08 miss is precise and unfixable inside the KPI grammar: the two status tiles carry a value but NO signed delta and NO named period (`dashboard.html` L283 `14 payments · 5 need you`, L309 `40% drawn · Reviewed 1 Sep`), and the Undrawn sparkline is twelve identical y=23.0 points (L316) — a shape with no information, drawn because the kpi-tile has no other slot. Three options were built as byte-clean copies and measured at 1440×900 light. **None moves the first chart** (710.6 in all seven renders) and none changes the lead row (y488.1 h150.5): the debt is a composition question, not a density one. **A (status strip in the header's existing status row + 4 equal tiles)** meets DP-08 4/4 and s247-D3 literally ("in tandem with a status bar component at the top") at +1 signal carrier. **B (Needs-attention promoted + 4 tiles)** meets DP-08 and DP-10's count-against-total at zero signal cost, but puts the statuses at y913.7 — below a 900px fold — unless the rail is reordered (B2: y678.6, +1 carrier, +126px page). **C (distinct tile kind in-row)** is the weakest against s247-D3's own words: however differently drawn, the statuses still "sit inside the other cards". Recommendation is Dave's; the numbers favour A or B2, and the choice between them is the open W5/DP-10 question s247-D3 already named.

COUNTS: findings `11` · ruling-shaped `4` · UNPROVEN `3`

## What was done

1. Read s247-D2/D3/D4 verbatim (`knowledge/_rulings.json` L6092–6140) and DP-06/07/08/10/20 (`reviews/DASHBOARD-PRINCIPLES-2026-09-05-v1.html` L405–470, L603–606) and the DP-08 fact in `notes/_dp-scores/w2.json` (`rows/DP-08`: verdict `missed`).
2. Library survey: `knowledge/components/kpi-tile.meta.json` (variants display/compact/with-table-cta; props size, trend up/down/flat; ONE slot `spark`; no status/count kind), `stat-card.meta.json` (display/compact/flat — flat = "No change, full ink, no arrow"), `status-indicator.meta.json` (atom; variants approved/cancelled/declined/pending; forms A dot+label, B tint chip, G17-B filled cell), `stats-band-lockup.meta.json` (organism; heading-only/heading-kpi/heading-action; tileType stat-card|kpi-tile), `badge.meta.json` (simple/number count), `progress-bar.meta.json` (the meter reading; `Limits-meter` canon.css L12835 reuses `.pb-track/.pb-fill` 4px). The composed page already binds `.status.ok/warn/err/inf` chips in its scope (canon.css L17128–17137) and `.summary__row` (L17120–17124).
3. Built `outputs/w2-debt/dp08/_build.py` → `dp08-current.html` (byte-identical copy), `dp08-A.html`, `dp08-A1.html`, `dp08-B.html`, `dp08-B2.html`, `dp08-C.html`, `dp08-C1.html`. Every edit is page-level `<style>` plus markup in the copy; `diff` against the source shows only the intended hunks (strip row L145–147, the two tiles L280–291/L306–317, the Needs-attention head L482–485).
4. Rendered all seven with `_render.py` (Playwright, 1440×900, light): full page + a 1440×430 crop from y=230 (header status row → lead row) + probe JSON (lead box, grid tracks, per-tile anatomy, first-chart-y, Needs-attention box, page height, and a signal census: every element in the first 900px whose computed color/background/fill/stroke resolves to a `--success/--warning/--error/--info/--up/--down/--spark-*/-tint` value, grouped to its nearest `.status` or `.kpi-tile` carrier).
5. Wrote `outputs/w2-debt/dp08/OPTIONS.json` (per option: numbers, library need, dp_scores, crop path).

## Findings

1. **Per-tile anatomy on the composed page** (probe `probe-dp08-current.json` `tiles[]`, source `outputs/w2-rhythm/arm-B-sighted/dashboard.html`): Group liquidity L240 · Receipts L254 · Payments L267 · Net FX L293 each carry value + `.delta.up|.down` with arrow + `vs yesterday` + `spark-inline[data-trend]` — 4/4 of DP-08. Awaiting approval L280–291: value `$2.7m`, `.delta` with NO up/down class, text `14 payments` + `5 need you` (a count and a sub-count, no period). Undrawn facilities L306–317: value `$120.0m`, `.delta` text `40% drawn` + `Reviewed 1 Sep` (a ratio and a date, no period, no sign).
2. **The Undrawn sparkline is a flat line by construction**: L316 `points="3.0,23.0 20.6,23.0 … 197.0,23.0"` — twelve points at y=23.0. The Awaiting spark (L290) is a synthetic wobble 20.0–27.5 with `data-trend="flat"`. Both render in `--spark-flat` (= `var(--text)`, canon.css L17094) — the black lines in `crop-lead-1440.png`. A sparkline of a facility headroom that is "Reviewed 1 Sep" has no series to draw; the slot forced one.
3. **Why they cannot meet DP-08 as KPIs**: DP-08's three parts are value, *signed delta against a named period*, *trend shape*. A queue count (14 awaiting, 5 for me) and a utilisation ratio (40% of a cap) are STATES, not flows: their honest second line is a count-against-total (DP-10's grammar, "[on card] of [total]") or a ratio-to-limit (Limits-meter's grammar, canon L12835 "a limit is something you must NOT complete"), and neither has a period. Reading a signed delta onto them ("+3 vs yesterday") would be inventing a KPI the role does not check.
4. **Signal cost on the current page (DP-20)**: 18 rag-coloured elements in the first 900px, grouped to 5 carriers — the nostro chip (y248, `--success-tint` + dot) and four KPI tiles (arrow fill `--up/--down` + spark stroke/end `--spark-up/--spark-down`), with no dominant (`probe-dp08-current.json` `signals_above_fold`). The two status tiles add ZERO colour today — they are hidden precisely because they are the only tiles without a signal, the inverse of s247-D3's "if they are important … aren't these lost in the foliage".
5. **No option moves the fold**: `first_chart_y` = 710.6 and lead `{y:488.1, h:150.5}` in current, A, A1, B, B2, C, C1 (seven probe JSONs). Removing two tiles does not shorten the row; adding a strip to the header's existing 24px status row (y248) does not add height. The DP-08 debt is orthogonal to W1/W2 density.
6. **Option A (4 equal tiles) vs A1 (4 of 6 tracks)**: A1 keeps `data-c="1"` in the six-track grid → tiles 223.3px wide, 453px void to the right (`dp08-A1-1440-lead.png`). A re-declares the lead group's grid to four tracks → 337.0px tiles filling 1360px (`dp08-A-1440-lead.png`). A reads as s247-D4's row; A1 reads as an unfinished one. Cost of A: the page rule `.tpl-group-lead > .c-bento__grid{--bento-cols-now:4}` out-specifies canon's band rules at every width (the template comment L222–225 chose six because "six divides every band count"; four does not divide three) — a 4/2/1 band line is owed to the recipe. UNPROVEN at 820/1100 (not rendered, budget).
7. **Option A's strip** (`dp08-A.html` L151–157): the header's existing `l-row` grows from one chip to three items — `status ok` nostro (kept, L146), `a.status.warn` "Awaiting approval · 14 payments · 5 need you" linking to `#p2` (the Payments tab), and a plain legal span "Undrawn facilities $120.0m · 40% drawn · reviewed 1 Sep" behind a 1px divider. Measured: strip box `{x:40,y:248,w:796.5,h:24}`; signals 20 elements / 6 carriers (+1 = the warn chip, which is now the only amber above the fold and therefore reads as the dominant). Library need: none new — Status-indicator form B is canon in this scope; the undrawn line deliberately carries no chip because "40% drawn" has no RAG meaning (a rag/neutral chip does not exist — status-indicator meta `tokenValidation`).
8. **Option B's promotion** (`dp08-B.html` L482–491): two `.summary__row`s head the Needs-attention card — "Awaiting approval / 5 of 14 need you · $2.7m" and "Undrawn facilities / 40% drawn · reviewed 1 Sep · $120.0m" — above the three existing rows. Measured: card `{x:973.3,y:913.7,w:426.7,h:329.5}` (+126.5px on 203), page 1299 (+126), signals unchanged 18/5. **The card top is at y913.7 — 13.7px below a 900px fold** (it was there before, `probe-page.json` NA y913.7): promoting the statuses into it puts the most-important-things-to-notice off the first viewport. The first "View all 3 of 8" I wrote was an invented total and was removed — the specimen has no list total, so DP-10's BLOCKING "a truncated list states its count" is still open on this card (only the 5-of-14 row carries a count).
9. **Option B2 = B with the rail reordered** (Needs attention above Balances by entity): card at y678.6, in view; signals 20/6 (the card's "Approval due 18:00" warn chip enters the fold). Same page height 1299. This is the version of B that actually answers s247-D3; it reorders the context rail, which is the template's business (RSQ Q5, DP-10 binds).
10. **Option C** (`dp08-C.html`): six tiles kept; the two statuses become `.kpi-tile--status` — no `.kpi-spark`, a 4px ratio bar in its place (35.7% = 5/14; 40%), and a `status warn` chip "5 need you" in the delta slot. Signals 20/6 (+1, the chip inside the row). Two sub-findings: (a) a rule on the tile is IMPOSSIBLE — canon sets `border:0px none` on dashboard tiles (probed computed style on `.kpi-tile--status`; keylines OFF, s219-D2(4)); (b) the wall-ground variant C1 makes the two tiles read as two HOLES in the row (`dp08-C1-1440-lead.png`) — a different ground is not a different kind, it is an absence. So C's "displayed differently" reduces to content shape (bar instead of spark, chip instead of arrow), which is real but small at 223px, and the tiles still sit inside the row s247-D3 says they must not sit in.
11. **Library has no status-metric surface today**: kpi-tile has ONE slot (`spark`, meta `slots`); stat-card's `flat` variant is "No change" (a zero delta, not a no-delta); stats-band-lockup composes only stat-card|kpi-tile; badge carries a count but on an icon/link; status-indicator is the chip. What exists for a status line is exactly what A uses (the header status row already on the page). What B needs is a Needs-attention molecule with a count slot (RSQ Q5 in DP-10's row). What C needs is a kpi-tile `kind=status` variant — a new prop, a snippet specimen, and a gate arm to exempt it from DP-08's checkable part.

## Options table

| | current | A strip + 4 | B NA promoted + 4 | B2 (rail reordered) | C status kind in-row |
|---|---|---|---|---|---|
| first_chart_y | 710.6 | 710.6 (Δ0) | 710.6 (Δ0) | 710.6 (Δ0) | 710.6 (Δ0) |
| lead row | y488.1 h150.5 · 6×223.3 | h150.5 · 4×337.0 | h150.5 · 4×337.0 | same as B | h150.5 · 6×223.3 |
| KPI count | 6 (4 true) | 4 | 4 | 4 | 6 (4 true + 2 status kind) |
| signals <900px (elements/carriers) | 18/5 | 20/6 (+1 warn chip, dominant) | 18/5 (Δ0) | 20/6 (+1) | 20/6 (+1) |
| page_h | 1173 | 1173 | 1299 (+126) | 1299 | 1173 |
| statuses' y | 488 (in row) | 248 (header) | 913.7 (below fold) | 678.6 | 488 (in row) |
| DP-06 | met | met | met | met | met |
| DP-07 (3–6) | met, 6 | met, 4 | met, 4 | met, 4 | met, 6 |
| DP-08 | **missed** 2/6 (F1) | met 4/4 | met 4/4 | met 4/4 | at-risk: 2 exempt only if a status kind is ruled |
| DP-10 | at-risk (View all, no count) | at-risk (unchanged) | met-in-part (5 of 14; list total open) | met-in-part | at-risk (unchanged) |
| DP-20 (≤3, one dominant) | missed 5, none dominant | missed 6, warn dominant | missed 5, none dominant | missed 6, warn dominant | missed 6, none dominant |
| s247-D3 (not inside the cards; own surface / status bar) | **missed** | met (bar at top) | at-risk (own surface, below fold) | met | at-risk (still inside the row) |
| s247-D4 (a row) | met | met (needs 4/2/1 band line) | met (same) | met | met |
| library need | — | none new; a recipe band line | NA molecule with count slot (RSQ Q5) | same + rail order | kpi-tile `kind=status` variant + gate exemption |
| crop | `dp08-current-1440-lead.png` | `dp08-A-1440-lead.png` | `dp08-B-1440-lead.png` + full | `dp08-B2-1440-full.png` | `dp08-C-1440-lead.png` |

## RULING-SHAPED QUESTIONS

1. **Where does a status metric live on an overview** — the header's status line (A, "in tandem with a status bar component at the top"), or the Needs-attention region (B2, DP-10), or both (strip carries the one-line state, the card carries the actionable count)? s247-D3 named this as open and Dave's; the renders now exist to look at.
2. **May a headline row be four tiles at four tracks** (A/B: 337px tiles, a 4/2/1 band rule) — or is the row count's flexibility (s247-D4) meant to stay on six-track multiples? A1 shows the alternative reading (4 of 6, a void).
3. **Does a `kind=status` kpi-tile variant exist at all** (C) — a count + ratio bar in the spark slot — or is DP-08 to be read strictly: anything without a period delta is not a headline metric and leaves the row? C is built so the "no" can be a seen no.
4. **DP-20's signal budget is already exceeded (5 carriers) before any option**; A and B2 each add the one amber that would be the dominant. Is the amber the intended dominant of a treasury overview (the thing the role must act on), which would make the four coloured sparklines the foliage to cut — or is three the number and this page needs a different fix first?

## UNPROVEN / CLAIMED

1. UNPROVEN — A/B at 820 and 1100: the four-track override is a page rule with higher specificity than canon's band rules, so it is predicted to stay four columns at every width (a 4-across squeeze at 820). Price: two renders, ~2 tool calls.
2. UNPROVEN — dark theme for all options (light only was rendered; the warn chip's amber-tint contrast and the ratio bar's `--border` track on dark are not seen). Price: 7 renders.
3. CLAIMED — the "5 of 14" and "35.7%" in B and C are derived from the specimen's own "14 payments · 5 need you" (L283); the specimen has no list total, so no "n of N" on "View all" was written (an invented "3 of 8" was removed).

## Evidence

- Source page: `outputs/w2-rhythm/arm-B-sighted/dashboard.html` (L146 nostro chip; L236–320 lead group; L280–291, L306–317 status tiles; L480–498 Needs attention).
- Builds: `outputs/w2-debt/dp08/_build.py`, `_render.py`; pages `dp08-{current,A,A1,B,B2,C,C1}.html`.
- Renders: `dp08-<tag>-1440-full.png`, `dp08-<tag>-1440-lead.png` (1440×430 crop from y=230: header status row → lead row); peeks `_peek-A-strip.png`, `_peek-A1-lead.png`, `_peek-B-na.png`, `_peek-C-lead.png`.
- Probes: `probe-dp08-<tag>.json` (lead, leadCols, tiles[], first_chart_y, needs_attention, strip, signals_above_fold{elements,carriers,detail[]}, page_h); `OPTIONS.json`.
- Rulings: `knowledge/_rulings.json` L6092 (s247-D2), L6108 (s247-D3), L6125 (s247-D4). Principles: `reviews/DASHBOARD-PRINCIPLES-2026-09-05-v1.html` L405 (DP-06), L418 (DP-07), L431 (DP-08), L462 (DP-10), L603 (DP-20). Score: `notes/_dp-scores/w2.json` rows/DP-08.
- Canon: `knowledge/canon/canon.css` L17079–17107 (kpi-tile in the bento scope), L17120–17124 (summary), L17128–17137 (status chip), L17239 (lead row unit 120px), L12835 (Limits-meter), L1448 (list-items status).
