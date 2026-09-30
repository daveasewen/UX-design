# #309 lane G — his review answers: three rulings, three builds, four looks

COUNTS: rulings inscribed 3 (s309-D5, s309-D6, s309-D7; store 838 → 841) · stamped enacted 3 (all at 7e58f84a) · rows minted 5 (W-309f1 lane F's missing doc row, W-309g2 dave, W-309g3 and W-309g4 claude, W-309g1 this report) · builds 3 (no-change mark at full ink; Metric's up-is-bad setting; the pre-push routine in the Worker checklist) · live pages switched to up-is-bad 0 · looks 4: caused by the move 1 (fixed), predating it 3 (reported, not fixed) · chart receipts re-driven 27 of 27 FRESH, no measurement moved · clone survey 167 of 167 asked: 155 pass · 0 FAIL · 3 ADVISORY-warn · 9 COULD-NOT-ASK · state-contrast sweep 137 of 137 snippets, 0 text failures, 0 carrier failures, 78 declared holes, audit byte-identical to the committed one · seat-only reds 0 · commits d1c0f8b7, 7e58f84a, e649da06 + this report's · pushed no

machinery: 0 instrument / 1 feature (Metric's up-is-bad setting)

Asked: the conductor, #309, on Dave's 11:04 BST export of `notes/_REVIEW-309-metric-and-the-arrow-2026-09-30-v1.html`, saved verbatim at `notes/_lanes/309/DAVE-RULINGS-2026-09-30-1104-metric-and-the-arrow.md`. Brief: `notes/_lanes/309/G/BRIEF.md`.

## A. The rulings (d1c0f8b7)

Through `_inscribe_ruling.py`, dry run then write, reconstruction proof passed each time, in lane I's by-click shape. Every quoted label, question and recommendation is asserted against the export and the page by `notes/_lanes/309/G/build_entries.py` before it is written. Entries: `notes/_lanes/309/G/entries/`.

| Ruling | Call | His click |
|---|---|---|
| s309-D5 | 6a · "Should a cost going up show red?" | "Let a metric say up is bad" — NOT the recommendation ("Keep direction for now") |
| s309-D6 | 6b · "The no-change mark: full ink or 60%?" | "Full ink, as ruled" (the recommendation) |
| s309-D7 | 6c · "Every lane runs the pre-push check before handing back?" | "Yes" (the recommendation) |

The arrow (item 2) was not answered, so nothing is inscribed for it. Items 3 and 5 are comments, recorded as rows (section D). Lane F's report had no store row (its commit passed on DOC_ROW_ACK); that row is W-309f1.

## B. The builds (7e58f84a)

1. **The no-change mark at full ink (s309-D6).** `Metric.reference.html` drops `opacity:var(--alpha-60)` from `.metric-delta.flat .glyph`, so the mark takes the standing ink: #1A1A1A on light, #FFFFFF on dark, opacity 1 (measured). The meta's delta note and flat token now say full ink.
2. **Up is bad (s309-D5).** There is one optional setting. The meta calls it prop `upIsBad` (boolean, default false); in the markup it is the class `up-is-bad` on the tile. With it, a rise takes the fall ink and a fall takes the rise ink, on the arrow and on the trend line. The arrow still points the way the number moved, and the sign and the word are unchanged. It adds no new colour, only canon's two RAG inks swapped. No live page sets it.
   - Measured: light, default up #137F3C / down #DA1A00; up-is-bad up #DA1A00 / down #137F3C. Dark, #66CC8D / #F6604C and the swap. Spark strokes follow.
   - **Render for his eye:** `notes/_lanes/309/G/up-is-bad.png`. It shows default against up-is-bad for a rise, a fall and no change, light and dark. The tiles are copied from the snippet by `build_up_is_bad.py`, and the page is `up-is-bad.html`. The demo labels are the snippet's ("Net cash flow" going up shown red is only a demonstration).
   - canon.css is regenerated. `.cn-metric` and its generated `.cn-kpi-tile` alias both gain the two rules; no page shows a flat kpi-tile delta. Theme cascade in sync, showroom `metric.html` regenerated. The 27 chart receipts were re-driven at the seat (all FRESH, every measurement identical to HEAD's), and the dataviz gate passes.
3. **The pre-push routine (s309-D7).** It is added as step 5 of the Worker checklist in `knowledge/_RUNBOOK-parallel-conductor.md`: lane E's routine, with its timings, citing s309-D7.

## C. The four looks

1. **Banking demo, "the filters are stacking vertically here".** This was the same before the move (b690a19b) and after. The cause: the demo (#227) still marks its filter row `.ftb-row`, with `.ftb-filter` and `.ftb-view` inside. #261 re-drew the bar as `.ftb-primary` / `.ftb-ctl`, and canon, regenerated at #267 (e470ae08), has no `.ftb-row` rule. The row is therefore a plain block, and its four children stack at 250 px. Probe: renaming the row to `.ftb-primary` alone puts all four on one line. **Not fixed.** The likely fix is to move the demo's bar onto the current anatomy (W-309g3).
2. **Receipt page, "the sparkline has become an area chart, but weird".** This one was caused by the move. The spec cut Metric's first tile, which carries the trend slot, across the full 1360 px row. It painted solid because the page's CSS loses every `--alpha-*` value (see 4). **Fixed (e649da06):** the spec now cuts Metric's compact tile (no trend slot; the DP-06 four-tile row's default), and the page is regenerated. Before/after: `notes/_lanes/309/G/receipt-before-after.png`. The tile goes from 151 to 83 px, and the page from 1349 to 1281 px. The gate verdict is unchanged (FAIL:BEHAVIOUR-NOT-LOADED, pre-existing) and the generator selftest passes.
3. **Receipt page, "I though we had a rule for the minimum items in a stat bar".** The nearest record is `metric.meta.json` `count`: `{"min": 2, "per": "group"}`, twice. Both came from s245-D7's bento groups and were moved to a count by s308-D19. s245-D7 Q3 (a) also says "A ONE-MEMBER GROUP IS LEGAL as a DECLARED CARVE-OUT". I found no rule named for a stat bar, and no gate that checks a page against that count (my search was not exhaustive). The receipt page shows one tile, and did before the move too. This is his call (W-309g4).
4. **Receipt page, "where has tall that blank space come from on the after".** This predates the move. The committed page at b690a19b was stale, and the old Stat-card spec regenerated at HEAD gives the same 685 px empty chart. Chart-line is now drawn by `dv-render`, which the spec does not splice (BEHAVIOUR-NOT-LOADED), so the empty svg sizes by its viewBox, not its 260 px. I also found that the generator writes its splice markers as HTML comments inside `<style>`. CSS does not read those as comments, so each marker swallows the rule after it, and that loses the `--alpha-*` tokens page-wide. **Not fixed** (W-309g4).

## D. Rows

- **W-309g2 (dave):** decide dark-mode ground and tile colour. It quotes his item 3 note verbatim, and nothing is built.
- **W-309g3 (claude):** the stacked filters.
- **W-309g4 (claude):** the blank space, the splice markers and the minimum count.
- **W-309f1:** lane F's report.
- **W-309g1:** this report.

## Checks

- **Clone** `/tmp/pp` at e649da06, `--include-mutating --no-record --timeout 60`. Chunks 1:12 (125 s), 13:55, 56:140, 141:167: 155 pass · 0 FAIL · 3 ADVISORY-warn ([140], [150], [163]) · 9 COULD-NOT-ASK ([10], [13], [61], [68], [73], [74], [142], [153], [154]). This is lane D's profile.
- **Tests:** `test_gates.py` 32 of 32, `test_advisory.py` 19 bite, `_validate_evidence.py` PASS, `_git_commit.sh --selftest` OK.
- **State-contrast**, full sliced sweep at the seat with CI fonts: 143 s + 120 s, `--merge` rc 0. The audit is byte-identical to the committed one.
- **Metas:** none added or removed, so ASSERT-009 is untouched. `gen_kg_sources --check` is in sync.
