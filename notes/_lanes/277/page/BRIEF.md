# LANE CP — BRIEF — rebuild the review page on ONE number, cards first
#277 · 2026-09-15 · written by the conductor after lane CV's verdict · **model: opus** · PROPOSE-ONLY

## The verdict you are acting on
Lane CV (`d84eb72`, `notes/_lanes/277/verify/VERIFY.md`) graded lane CO **21 GREEN · 8 RED · 8 AMBER** and returned the **#268 verdict**: *"the page passes its driver … then fails on sight, because the card carrying the biggest number on the page says two different things about it."*

**Dave has not seen this page and must not until it is fixed.** He is the bottleneck; a page that makes him adjudicate our arithmetic spends the one budget that actually binds.

## Read first
1. `notes/_lanes/277/verify/VERIFY.md` — **the whole thing.** Its "what the conductor must change" list is your worklist, items 1–8 and 12.
2. `notes/_lanes/277/charts/REPORT.md` + `REVIEW-charts-2026-09-15-v1.html` + `_build_page.py` — what you are rebuilding.
3. `notes/_lanes/277/judgement/RECOMMEND.md` — CJ's recommendations, which are the page's recommendation text.
4. `notes/_lanes/276/tie-off/REVIEW-tie-off-2026-09-15-v1.html` — the page Dave actually exported from. Match its export-JSON shape exactly.

## The work — in this order
1. **Rebuild D-3 on ONE number: 47.** CV measured both lanes' matrices, found they differ in exactly 3 cells, settled 2 of them (`dv-008` DOES bind pie — `chart-pie.responsive.rule` says `.dv-stage` scrolls; `dv-015` does NOT bind line), and reconciles to **47**, or 48 if Dave keeps `dv-013` on bar. Lead the card with **"two blind lanes agreed on 16 of 19"** and name `dv-013`-on-bar as **the single open cell**. Recompute every derived figure on the page from that one matrix — the "8", the "13", the "49" all move or go.
2. **Delete or attribute the unlabelled CJ paragraph** under D-2 and D-3. If a sentence is CJ's, it says so where it sits, not 1,900px lower in Receipts.
3. **Fix D-3 option (b)'s contradiction**: it says `dv-013`/`dv-015` "land on at most one" while the footer says "none of the three". One statement of fact per fact.
4. **Move the three decision cards ABOVE Parts A and B.** Today D-1 begins 64% down a 9,558px page and Dave reads 43 table rows before the first ask. Evidence goes behind the ask, in a marked section — the house rule (`[[decide-fast-dave-is-the-bottleneck-254]]`).
5. **Reword D-1 so (a) and (b) are exclusive** — "land now" vs "land after a per-component read".
6. **Add to D-2** that choosing (b) **strands `dv-pie-003` on no component at all** — the doughnut-centre rule then binds nothing.
7. **Surface the `≤ 5 parts` vs `max 6` conflict as its own line.** `chart-pie.meta.json` carries BOTH, 8 lines apart; `chart-donut` too; `_validate_dataviz.py` (a gate) carries the 6; no ingested source carries the 5. ⛔ **Do NOT resolve it and do NOT make it a decision option** — it is ruling-shaped and Dave's. One line, flagged, with the file list.
8. **State the combined cost ONCE in the hero**: D-1 + D-3 = **76 edges, 81 → 157**. Today the hero says 110, which is D-1 alone.
9. **Rewrite two `$why` sentences** (CV A-6): `dv-pie-001` cites `data-a1`/`-a2`, which live in `Chart-donut.reference.html`, not in `chart-pie.meta.json` — the meta's `motion.entry` is the right pointer. `dv-bar-002` names no checkable mechanism. If `dv-013` survives on bar, cite grouped/stacked, not `orientation`. Write the corrected metas into `notes/_lanes/277/page/proposed-metas/` — **do not edit CO's committed files**; corrections are BY ADDITION.

## What you do NOT do
- ⛔ Nothing under `knowledge/` is written. Nothing lands.
- ⛔ Do not re-open scope. `s276-D5` names three components; CJ's donut/sparkline/combo analysis is the "look again" the ruling asked for and belongs on the page as a **flagged finding under the decisions**, not as a fourth decision and not as authored metas.
- ⛔ Do not edit `notes/_lanes/277/charts/` or `.../judgement/` or `.../verify/`. Your writes live in `notes/_lanes/277/page/`.

## Gates
Drive the rebuilt page with `_drive_page.py` (adapt CO's) — both themes, 390px and 1280px, worst descender clip, no horizontal scroll, the two-red values, and the export button producing valid JSON naming the page **with** its `.html`. `source knowledge/_render/seat_env.sh` for chromium. **Then look at the screenshots yourself and say what you see** — the driver went green on a page that contradicted itself, so a green driver is not the test. `python3 knowledge/_validate_kg.py` must be OK.

## Deliverable
`notes/_lanes/277/page/REVIEW-charts-2026-09-15-v2.html` + `REPORT.md` (what changed, item by item against CV's list, with the before/after figure) + screenshots both themes. One commit: `#277 2026-09-15 — lane CP: …` with `--numstat` **re-read from the shipped sha** — both earlier lanes shipped receipts quoting amended-away shas (CV R-3, R-8). Do not repeat it.

## Cautions
Never `git stash` · never `gen_kg_edges.py` · never `_build_all.py` · textual span only · stale `.git/index.lock` → `mv` to `.git/_orphan-locks/`, never delete · another lane (CH) is running this wave — commit serially, stay in your directory.
