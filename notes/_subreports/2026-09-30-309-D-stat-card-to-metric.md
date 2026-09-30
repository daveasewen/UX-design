# #309 lane D — the stat card pages move to Metric, the arrow in the right RAG ink

COUNTS: rulings inscribed 2 (s309-D3, s309-D4; store 836 → 838) · stamped enacted 1 (s309-D3 at d6d570bf) · live pages moved 4 (banking demo, progress dashboard, receipt-bearing regen, FAB overlay test) + 1 receipt selftest · arrows moved to the ink seat 3 (2 on the banking demo, 1 on the receipt page) · before/after PNGs 3 · stat card drawing retired 0 (still needed) · clone survey 167 of 167 asked: 155 pass · 0 FAIL · 3 ADVISORY-warn · 9 COULD-NOT-ASK · state-contrast sweep 137 of 137 snippets, 0 text failures, 0 carrier failures, 78 declared holes · seat-only reds 0 · commits 06062e9f, d6d570bf + this report's · pushed no

machinery: 0 instrument / 1 feature (the receipt generator drops APOLLO-DEMO fenced CSS from a style splice, as gen_canon_components.py already does — s258-D3)

Asked: the conductor, #309, on Dave's 07:07 BST words (`notes/_lanes/309/DAVE-WORDS-2026-09-30-0707.md`): "1. Moving to metric is probably a good idea but the arrow must be the the right RAG ink" / "2. We'll recut towards the end of the week". Brief: `notes/_lanes/309/D/BRIEF.md`.

## 1. His two answers (06062e9f)

s309-D3 (the stat card pages move to Metric; the trend arrow must be the right RAG ink) and s309-D4 (the designer pack is re-cut towards the end of the week, not now), through `_inscribe_ruling.py`, dry run then write, reconstruction proof passed both times; lane I's shape, his words verbatim, said to be given in chat, the conductor's two open items quoted from the words file. Entries: `notes/_lanes/309/D/entries/`. s309-D3 stamped enacted at d6d570bf after the move.

## 2. The right RAG ink — canon settles it

| Change | Arrow ink | Light mode | Dark mode |
|---|---|---|---|
| Up (good) | rag/success-ink | #137F3C | #66CC8D |
| Down (bad) | rag/error-ink | #DA1A00 | #F6604C |
| No change | the standing ink (Metric: text/default at 60%) | — | — |

The same in all four themes (mono, common, console, supercharge); only the mode forks it.

**Where it comes from.**
- s263-D1 (Dave, #263): "KPI tile delta glyph sits on the INK seat (rag/success-ink / rag/error-ink), not fill … Stat card moves with it." s261-D4 (4): "use the dark versions of the colours on the arrows."
- s182-D3: the trend colour "should just follow the red and green ink colours for all themes"; it derives from trend direction and background; neutrals take the default ink, white on dark.
- s151-D1 (the two-red law): dark red ink #DA1A00 on white, light red #F6604C everywhere else; coloured red/green only on values carrying a symbol. s155-D1: green mirrors it (#137F3C / #66CC8D). s144-D1: the four values, tuned to 4.5:1 on #F1F1F1 (light) and #272727 (dark).
- canon.css: `--rag-success-ink` / `--rag-error-ink` are declared once in `:root` and once in `[data-theme="dark"]`, and no theme overrides them; `.cn-metric` binds `--pos-ink` / `--neg-ink` to them.

**Direction, not the metric's sense.** Canon keys the colour to direction: col26-016 ("RAG red … for downward, and RAG green for upward position movement, stat-card style"), dv-017 (a) (gain/loss deltas, sign and arrow mandatory), s182-D3 ("derives from trend direction"). Nothing in canon, the metas or the rulings lets a metric invert it (a cost going up shown red). One live case: the banking demo's "Net FX exposure −8.1%" is red. That is correct under canon, but a reader might count a falling exposure as good. If Dave wants sense-keyed colour, that's a new decision for him.

**What each did before.** Metric already had the ruled ink (#261 K3). The stat card still used the FILL seat, `--up: rag/success` / `--down: rag/error`, with per-theme overrides: mono #66CC8D / #F6604C in both modes (1.98:1 for that green on a white card); common/legacy #00847F / #A8000B (the legacy fills of s131-D1, #A8000B being the third red of s308-D13); console and supercharge #5DAC7B / #B92F1E. Measured at the seat on the banking demo in all 4 themes × 2 modes; each ink is printed beside its crop on the before/after PNG.

## 3. The move (d6d570bf)

- **The #227 banking demo** (`dashboards/international-banking-dashboard.canon.html`): its four stat tiles take Metric's markup (`.cn-metric` › `.metric` › `.metric-lbl` / `.metric-val` / `.metric-delta` / `.metric-per`). The two triangle symbols are replaced by Metric's `direction` arrows, read from `Metric.reference.html` and never retyped. The page's own two layout rules are renamed. Done by `notes/_lanes/309/D/move_banking.py`, which refuses on any count mismatch.
- **The progress dashboard**: `gen_dashboard.py` writes Metric tiles and the page is regenerated. Its counts carry no delta, so there's no arrow; the tiles are a touch tighter (Metric's lock-up).
- **The receipt test**: the spec and `gen_provenance_receipt.py --selftest` now splice Metric (selftest 6 of 6 green). Metric's style carries a fenced demo block the receipt gate refuses (DEMO-CHROME-COPIED), so the generator now drops fenced CSS from a style splice, the same span `gen_canon_components.py` drops from canon.
- **The FAB overlay test** (`verify_apollo_fab_227.js`): the mock tile is Metric's, since the demo it copies moved. `apollo-fab-meta.json` is regenerated by `gen_fab_meta.py` (it had been stale since #227: +metric, +legend, +template-dashboard-bento; stat-card and kpi-tile now read as aliases). 64 of 64 pass.
- **Kept**: `Stat-card.reference.html` and `.cn-stat-card` in canon. They're still needed by the snippet's own showroom page and gallery section, and by the frozen #227 pair `_detect_retrieval.py` grades (`regen-v1.html`). The pair's hand half, which is the demo itself, is now frozen at `knowledge/_tests/retrieval/international-banking-dashboard.canon-227.html` (bytes at b690a19b). Without that, N1 went red (Template-dashboard-bento 0.345 vs 0.327: Metric markup brought the live demo closer to the template). The `stat-card` alias resolves to Metric as before; its `$snippetDisposition` is rewritten to say what is kept and why. The nio-dash fitness pages use `.stat-card` as a template panel class, not `.cn-stat-card`, and were not touched.

Measured after the move (seat, all 4 themes × 2 modes, banking demo): up #137F3C / down #DA1A00 in light on #FFFFFF and on supercharge #F7F6F4; up #66CC8D / down #F6604C in dark on #1F1F1F and on supercharge #2A2621.

## 4. For his eye

`notes/_lanes/309/D/banking-demo-before-after.png`, `progress-dashboard-before-after.png`, `receipt-page-before-after.png`. Each shows the page at 1440 in light and dark, with before (b690a19b, from a `git archive` extract) on the left and after on the right. Below that are the stat row at 4x and each arrow cropped in, labelled with the measured inks. The banking demo's crops run all four themes × two modes. Drivers: `capture.py`, `compose.py`.

Two things on the receipt page are not from the move, and its PNG says so:
- Its chart is empty after, because the page was already stale at HEAD (`--check`: RECEIPT-STALE) and regenerates against today's Chart-line. HEAD's own Stat-card spec regenerates to the same empty chart (probed).
- Neither side draws an arrow, because a receipt splices the element, not its icon sprite.

Its gate verdict moves from FAIL:BEHAVIOUR-ADDRESS-DISAGREES + stale to FAIL:BEHAVIOUR-NOT-LOADED (Chart-line's dv-render scripts). The page is in no CI gate.

## 5. Checks

- In the clone (`/tmp/pp` at d6d570bf, lane E's routine), `--include-mutating --no-record --timeout 60`, chunks 1:12 (99 s), 13:55 (71 s), 56:140 (94 s), 141:167 (93 s): 155 pass · 0 FAIL · 3 ADVISORY-warn ([140], [150], [163]) · 9 COULD-NOT-ASK ([10], [13], [61], [68], [73], [74], [142], [153], [154]) — the same profile as lane E's run on 054aee4b. `test_gates.py` 32 of 32, `test_advisory.py` 19 bite, `_git_commit.sh --selftest` OK, `_validate_evidence.py notes/_claims` PASS. **Reds: none. Seat-only reds: none.**
- On the mount, by hand, after vs before: `_validate_geometry.py --build` 56 findings as before, banking demo 1 (the same G6 on the treasury snapshot); `_validate_own_size.py --build` 6 as before; `_detect_retrieval.py --selftest` green (N1 6 better, 1 tied, 0 worse); `gen_kg_sources --check` in sync; the `_wrap_regen.py --checks-only` staleness (rulings page, KG titles, schematic, memento index) regenerated in its order and committed.
- **State-contrast, full sliced sweep** at the seat, CI fonts (`FONTCONFIG_FILE` unset), 8 slices in two calls of four (144 s + 128 s), then `--merge`, rc 0: 0 text failures across 137 snippets, 0 carrier failures, 78 declared holes. That is lane E's CI-identical reading, and no snippet, canon file or default path of the gate has changed since 054aee4b. `knowledge/_STATE-CONTRAST-AUDIT.md` is regenerated from it and committed (it was the 3-snippet partial).

## Open

- **Dave's eye** on the three before/after PNGs.
- **Sense-keyed colour** (a cost going up shown red) is not in canon. It's his call if he wants it (the FX exposure tile is the live example).
- **The third red**: the stat card in Common painted #A8000B, and after the move Common's down arrow is #DA1A00. s308-D13 keeps the #A8000B question open (W-308ia), and s282-D2 records his "readable secondary red for 1 or two of the themes" as unproven, with no token. Neither is touched here.
- **Metric's "No change" glyph** is text/default at alpha-60. The snippet's own comment says "full ink", and s182-D3 says default ink for neutrals. None of the moved pages shows a flat arrow, so it was left as drawn.
- **The receipt page's Chart-line** BEHAVIOUR-NOT-LOADED is pre-existing, and the page is outside CI.
- **The designer pack re-cut** (s309-D4) is his, towards the end of the week. No row was minted for it.
