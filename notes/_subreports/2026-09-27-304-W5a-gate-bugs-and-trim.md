# #304 W5a — gate bugs and the trim scope: five no-ruling defects from candidate 2's cold runs, fixed at their generators

provenance: 304 · Sun 2026-09-27 · seat W5a (Opus 5.5) · mount HEAD `3100da99` · nothing committed, no git writes on the mount, no `git status` on the mount, no Project memory, no `_build_all.py`/survey/`_capture_gate.py --wrap` on the mount · every build, regen, re-drive and the survey in a throwaway clone `$HOME/w5a` (W4a's idle clone `$HOME/c4a` renamed and hard-reset to `3100da99`, full history; dies with the VM) · writes on the mount: the 41 tracked files below (byte-identical to the surveyed clone commit; every mount copy equalled `3100da99` before the copy), `notes/_lanes/304/W5a/`, this report
status: observed — every figure below was printed by a gate, a selftest, the survey, the harness or a browser probe at the seat; every render named was looked at

## The answer

All five fixed, each at its generator, none needing a ruling. On candidate 2's three runs, as the pack's own gates read them:

| | before (HEAD) | after (W5a) |
|---|---|---|
| receipt gate, pages red | r1 6/10 · r2 6/10 · r3 10/10 | r1 0/10 · r2 0/10 · r3 10/10 (only BEHAVIOUR-ADDRESS-DISAGREES left — Dave's line, below) |
| screen gate icon-source | r2 ❌ on 10/10 | ✅ 10/10 on all three |
| screen gate RESULT | FAIL · FAIL · FAIL | **PASS · PASS** · FAIL (r3: the same address line) |
| own-size findings | 82 · 104 · 146 | **0 · 0 · 0** (same 743 parts matched, page for page) |
| right-edge chart text cut (R4s2's probe) | 2 · 4 · 4 | **0 · 0 · 0**, 0 page errors |
| harness collisions (affected tiles) | 7 · 5 · 0 | **1 · 0 · 0** (the 1 is a real line end-key clash, DV-D10) |
| harness size drift | 23 · 31 · 25 | **0 · 0 · 0** |
| harness ink per view | 4.7 · 4.4 · 6.2 (mean 5.10) | **1.8 · 0.8 · 3.7 (mean 2.10)** |

Dead ink, cut ink (all Kpi-tile label crop, held for Dave) and markers do not move — none was in this lane. Nothing went up on any class of any run.

**One premise was wrong and is corrected here (fix 3).** R4s2 and the brief name the shell's and bento's per-scope trim copies as the cause of the 16.7px legend. They are not the binding one: with both removed the legend still measured 16.7px, because canon.css's ROOT default (`:where(.canon) :where(button,…,span,…)`) also reaches it. Removing all three restores 20px. Both are fixed. And **the KPI +4px is not a trim at all** — it is the bento template's own `.spark-inline{height:44px}` outranking Kpi-tile's 40px; it is NOT fixed here and is a Dave question (Q2).

## 1 · The receipt gate counted the Data-grid's fenced demo script

**Cause (confirmed).** `_validate_receipt.inline_scripts()` skipped AUTO-BEHAVIOUR spans only, so `knowledge/snippets/Data-grid.reference.html#script` resolved to TWO scripts: the real 23,863 B one and the 1,439 B state switcher inside `<!-- ===== APOLLO-DEMO script START … -->` (snippet :1140–1166), which s258-D3 forbids copying. Every page that carried the real script byte for byte still failed BEHAVIOUR-NOT-LOADED on the switcher.

**Fix.** `demo_fenced_spans(html)` — the HTML-comment form of the fence the snippets already carry, found with the gate's own `DEMO_FENCE_RE` marker string, depth-counted (as `_validate_own_size.py` walks the same fence), an unclosed START fences nothing. `inline_scripts(…, exclude_demo=True)` skips a `<script>` inside one. Of the 18 metas with a `#script` address, only data-grid's resolution moves (2 parts → 1); the other 17 resolve to the same bytes. `gen_component_partials --check` and `_validate_behaviour` stay green (they import the resolver).

**Tested.** `_validate_receipt.py --selftest` PASS with five new arms: AF (#script resolves the real script only), AG (real script carried, harness not → PASS — the Data-grid false red), AH (neither carried → still NOT-LOADED), AI (a snippet whose only script is fenced → UNRESOLVABLE), AJ (nested fences, unclosed START). Mutation: with `exclude_demo` off, AF/AG/AI/AJ all fail. On cand2-r2 the grid's edited copy now reads NOTE:AUTHORED-JS (s258-D1), as the gate intends.

## 2 · `gate_icons` read inside script bodies

**Cause (confirmed).** The icon regex `<svg\b…>.*?</svg>` ran from the string `<svg>` in dv-render.js's own comment ("everything inside the <svg> …") to the next `</svg>` and read engine source (`d="M' + p.join(' L') + ' Z…"`, `arc(cx, cy, …)`) as icon paths. It fires on any page that inlines the engine (cand2-r2 inlines it on all ten).

**Fix.** `_validate_screen.markup_only(html)`: every live inline `<script>` body blanked (tags and newlines kept), located on the comment-masked copy with the receipt gate's `SCRIPT_EL_RE` + the one `mask_comments`, so a commented-out `<script>` never blanks the markup after it. HTML comments are not blanked — the icon step's reach over them is unchanged. Declared: an svg a script builds at runtime is not read (it was only ever read by accident of the regex).

**Tested.** `notes/_lanes/304/W5a/test_icons_markup.py <knowledge-dir>` PASS: P1 engine source then a library icon → 0; P2 engine source then an invented icon → still 1; P3 invented icon → 1; P4 invented icon only in a script string → 0; P5 a commented-out `<script>` does not blank the markup after it → 1; P6 data-bespoke skipped; M1 the raw-html (pre-W5a) reading reds on P1. `_validate_screen.py` has no selftest of its own; the test file is the planted leg.

## 3 · The leading-trim scaffold reached into nested components

**Cause (measured, `probe/trim_rules.py`, CDP matched rules).** On cand2-r1's overview the chart legend button matched THREE trim rules: canon.css:974 (root default), :5667 (app shell copy), :17642 (bento copy). Stripping the shell and bento copies alone: still 16.69px. Stripping the root too: 20px, trim none (the Chart-bar snippet: 20px, trim none). 111 snippets carry a private copy of the scaffold; 26 carry none (14 charts, Alert, Banner, Drawer, Toast, Popover, Modal-lightbox, Stat-card, Empty-state, Icon-button, Account-selector, File-upload, Skeleton-loader) and render untrimmed in their reviewed snippet. Projected, every copy — and the root default — had no lower edge.

**The pattern it restores.** The generator's own #215 note: the scope class "exists to stop one component's rules reaching another component's markup". The own-size contract: a part keeps its own size on any page. So: the NEAREST component scope decides the trim — its own copy, or its absence.

**Fix.**
- `gen_canon_components.py`: `is_trim_scaffold()` recognises exactly the 111 copies (`:where(button,…)` selector, body = the default trim); `trim_bounded()` appends `:not(:where(.cn-x [class^="cn-"] *, .cn-x [class*=" cn-"] *))` to each (paren-aware top-level split). ZERO specificity, so the #215/#268 cascade holds: `_validate_descender_clip` PASS, SPECIFICITY RATCHET AT ZERO.
- `canon.css` root default (hand source, outside AUTO-COMPONENTS): `:not(:where([class^="cn-"] *, [class*=" cn-"] *))`, with a comment. Only the element-list selector; the `.c-eyebrow…` selector is untouched.
- canon.css regenerated (137 components; 111 bounded copies). `gen_canon_components --check` OK.

**Tested.**
- cand2 own-size: 82/104/146 → 0/0/0, same parts matched on all 30 pages (`measure/os-*`).
- Attribution (`probe/trim_diff.py`, before v after staging of the same page): every group listed (the 25 largest per page, r1 overview and payments, r2 messages) sits inside a `cn-chart-*` scope — legend buttons 16.7→20, their spans 8.7→12, chart data-table cells +3.3, the legend Reset wrap 8.7→22 (it was clipping Reset). The tail beyond the 25 was not listed, so "nothing else moved" is not claimed; the harness's dead/cut/collision classes did not move on any view.
- Geometry @1440, HEAD tree + HEAD gate v W5a tree + W5a gate: 166 pages (138 showroom, 13 chart test pages, 14 chart snippets, the bento) 142 → 142 findings, 0 pages differ; `_fitness-test` 58 pages 148 → 148, 0 differ.
- Own-size on the 13 test pages + 58 `_fitness-test` screens: 238 → 249. **Declared, not a false positive:** −8 (seven legend Reset buttons, one Account-selector trigger now at their reference size) and +13 on `canon-gallery.canon.html`, whose legend items are 16px text because that screen links canon.css but NOT type.css (measured: 16px/normal vs the reference's 12px/12px). The trim had squashed the 29px box to 19.6px, inside the tolerance by accident; the finding is now true.
- Renders looked at (`renders/legend-c2r1-payments-{before,after}-{light,dark}-4x.png`): glyphs whole both sides, both themes; after, the Reset button is whole (before it was cut at the list's foot).
- Not touched: the held-back Kpi-tile descender change (`notes/_lanes/304/W3a/held-back/`); `p.kpi-lbl` is not in the scaffold list, so its lock-up is unchanged (14px label box on both sides).

## 4 · Right-edge chart labels cut (engine)

**Cause.** The right padding was a fixed `data-pr` (default 12). A label placed on a fraction of the plot and growing right — the last centred category ("Middle East and Afric"), the last value tick ("600 £", "1500 £") — ran 5–19px past the svg's right edge. The left side was fixed by ds-012(b) ("the plot area is computed from the widest label, not a fixed number … (b) fixes the class"); this is its right-hand twin, same licence.

**Fix (`dv-behaviour.js`).** `gutterPR(svg, PL, PR, W)`, called after `gutterPL`: for every `text[data-fx]`, ink right of its anchor = `bbox.x + bbox.width − x` (any anchor, as rendered); a label at fraction f moves left f px per px of PR, so PR = the smallest value at which every such label ends `PL_EDGE_PAD` inside the box. `data-pr` stays the floor; the ceiling is the existing provisional `PL_MAX_FRAC` of the width (ds-012 point 3). Nothing scales (DV-D02); the plot narrows by the overhang only.

**Budget.** Chart-combo sat at 34,704 of 34,816 code-only bytes. The saving came first: two one-line readers, `num(el,k,d)` (= `parseFloat(el.getAttribute(k) || d)`, 19 call sites) and `up(e,s)` (the guarded `.closest`, 6 sites), same semantics. Net +64 → **34,768 of 34,816** (48 bytes headroom). `_validate_behaviour` OK. dv-render (the shared core) was not used to hide bytes.

**Regenerated in the clone:** `gen_component_partials.py` (15 consumer blocks: 14 Chart-* + the bento), `gen_showroom.py` (15 pages), `_validate_behaviour.py --write`, and all 27 chart receipts re-driven with R3's `drive_shim.py` in four batches: **27/27 FRESH, 54 changed leaves, every one a hash (self_sha256, source sha); 0 measurement values changed.**

**Tested.** R4s2's edge measure on page files (`probe/edge_pages.py`): cut texts 2/4/4 → 0/0/0, 0 page errors. Renders looked at: `renders/edge-c2r2-region-{before,after}-light.png` ("Middle East and Afric" → whole, plot ~14px narrower) and `renders/edge-c2r1-accounts-{before,after}-light.png` ("600 £" → "600 £m"). Geometry on showroom + test pages unchanged (above).

## 5 · Grid rows hidden in the grid's own scroll box counted as collisions

**Cause.** In `_validate_geometry.py`'s `visibleRect`, a run unrolled through a scroll box takes `virt = up.virt || (outside ? e : null)`: through two nested scroll boxes (the grid's 380px box inside the app shell's `.sh-content`) it took the OUTER box alone. Hidden rows, unrolled, sit exactly where the pager and `#dgHint` sit under the grid box, and both were "in the shell's frame" — so they collided. The harness measures with the gate's own COLLECT, so the bug was in the gate, not a harness copy.

**Fix.** The frame is the CHAIN of scroll boxes a run is unrolled through (`vid()` per box, `'v3>v1'`); runs compare only within one chain. New cause lever `X-nest` restores W4b's reading. Harness: `views.measure_here(…, levers=())` passes levers through (selftest only).

**Tested.**
- New guard `guard-nest` in both geometry fixtures (a grid box inside a shell, both below their folds, a hint under the box), from `notes/_lanes/304/W5a/gen_fixtures.py` — W4b's generator extended, W4b's copy left as it was; this is the fixtures' home now. Own-size fixtures byte-identical.
- `_validate_geometry.py --selftest`: GEOMETRY SELFTEST OK — 13 planted, 4 sub-cases, 4 levers (X-nest "moves nothing on the planted page but its own false-positive guard"), both guards fire under their levers, 13 mutations, the #288 and v1013-r2 real legs.
- `score.py selftest-views` (R4C_RUNS redirected): VIEWS SELFTEST PASS, with a new assert: clean fixture collisions 0, and 1 with `X-nest` through the harness.
- cand2 views, gate change only (HEAD pages): collisions 7/5/0 → 1/0/0; every one removed was a grid row v pager/hint/"Rows per page"; the one left is the line end-key clash on r1 FX (`measure/views-gate/`).

## Test it hard — the whole diff

- **Survey, all 148 steps**, clone at `3100da99` + this diff (committed in the clone `2a8d2b59`, then the C1 serial `_render_rulings` → blast radius → memento index → mention map → `_gen_chain` → schematic, all rc 0, committed), `--include-mutating --resume --timeout 60`, six chunks: FAIL `[81] [86] [94] [127] [128] [132] [134] [135] [144]` · could-not-ask `[10] [13] [61] [68] [136]` · timeout `[73]`. **0 green→red: every failure-detail block identical to V4's after logs** (`measure/fails.py`, paths normalised; logs `survey/`). The survey re-dirtied none of the 41 files.
- On the mount after the copy: `gen_canon_components --check` OK (137) · `gen_component_partials --check` OK · `gen_showroom --check` OK (137 + index) · `_validate_behaviour` OK · `_drive_chart_engine --check` 27 FRESH · `_validate_receipt --selftest` PASS · `_validate_descender_clip` PASS · `_validate_dataviz` PASS (15) · `test_icons_markup.py` PASS.

## Changed files (41 tracked; list at `notes/_lanes/304/W5a/changed-files.txt`)

- Sources (7): `knowledge/_validate_receipt.py`, `knowledge/_validate_screen.py`, `knowledge/_validate_geometry.py`, `knowledge/canon/gen_canon_components.py`, `knowledge/canon/canon.css` (root default by hand + regenerated block), `knowledge/canon/dv-behaviour.js`, `notes/_lanes/304/R4c/harness/views.py`.
- Regenerated (34): 15 snippets (14 `Chart-*` + `Template-dashboard-bento`), 15 showroom pages (14 `chart-*` + `template-dashboard-bento`), `knowledge/_BEHAVIOUR-GATE.md`, `knowledge/_tests/chart-engine/_receipts.json`, `knowledge/_tests/geometry/geometry-{clean,planted}.html`.
- Untracked, rides with it: `notes/_lanes/304/W5a/` (gen_fixtures.py, test_icons_markup.py, restage_engine.py, probe/, renders/, edge/, gates/, measure/, survey/), this report.

## Regen recipe (for the commit seat; nothing needs re-running — the mount bytes are the surveyed bytes)

Edit sources → `python3 knowledge/gen_component_partials.py` → `python3 knowledge/canon/gen_canon_components.py` → `python3 knowledge/gen_showroom.py` → `python3 knowledge/_validate_behaviour.py --write` → re-drive the 27 receipts at the seat (`source knowledge/_render/seat_env.sh`; `python3 notes/_lanes/304/R3/drive_shim.py --page …` in four batches of ≤7) → fixtures: `python3 notes/_lanes/304/W5a/gen_fixtures.py` from the repo root. Then the C1 serial as `--check`. Step count unchanged (148): nothing for the `[121]` trap.

## For Dave (Tuesday's page)

**Q1 · Which script does a chart carry — one line.** The mint and the meta disagree, so every chart region on a page minted by the pack reads FAIL:BEHAVIOUR-ADDRESS-DISAGREES (cand2-r3: 10/10 pages; cand2-r2 hand-patched its receipts around it; reproduced on a page built only by `--compose`).
- The mint (`gen_provenance_receipt.behaviour_address`) takes the FIRST registered AUTO-BEHAVIOUR name in the snippet's document order → `knowledge/canon/dv-behaviour.js`.
- All 14 chart metas say `"script": "knowledge/canon/dv-render.js"`, with dv-behaviour listed among their `partial`s.
- The receipt gate already says "the meta is the ONE HOME (s234-D5) and the receipt is a copy".
- **(a)** the chart's script is **dv-render.js** (the core, `dvRender`, priced once per page by s260-D1): the mint reads the meta's `script` instead of the first block name — one function, no meta or page changes; or **(b)** it is **dv-behaviour.js** (the first block every chart carries): 14 metas change, and the address stops naming the engine that draws. Recommendation: (a).

**Q2 · A Kpi-tile inside the bento: 40px spark (its own snippet) or 44px (the bento's own tiles)?** `:where(.cn-template-dashboard-bento) .spark-inline{height:44px}` (canon.css ~17942, the bento snippet :628, for its own demo tiles) outranks `:where(.cn-kpi-tile) .spark-inline{height:40px}` by source order, so a real Kpi-tile in the bento is 4px taller than its snippet (measured on cand2-r3: spark 44 v 40). Same scope-bleed class as fix 3, but the general cure (outer scopes stop at nested scopes) would also cut the bento's deliberate child rules (`figure.dv-fit-on .dv-svg`, W4a's ring rule), so it needs your word on which size is right, not a generator rule.

**Q3 · Seen, not fixed (engine; for the next engine lane).** Under reduced motion, charts on cand2-r1 and r3 intermittently never fit: the svg keeps its baked 580-wide viewBox in a 990px box and every glyph renders ~1.7x (cand2-r1 overview 7/8 loads at HEAD, 8/8 with this diff; r3 2/4; r1 fx 3/4; 0/3 without reduced motion; `probe/fitrate.py`). It matches W4a's ring cause (a width transition mid-flight when the fit measures) on non-ring charts. It is pre-existing, and the harness measures with reduced motion, so ink rows for r1/r3 carry that noise.

**Declared, no ruling taken.** The right gutter reuses the provisional `PL_MAX_FRAC` (0.42) and `PL_EDGE_PAD` (2) that ds-012 point 3 left to your eye; the 26 untrimmed components now render at their snippet's (untrimmed) size on `.canon` pages, which is visible wherever they sat in the shell or bento (chart legends, data tables, Reset).

## Limits

Everything at the arm64 seat with the HSBC face, 1440 only for views and renders (390 not looked at); the survey baseline compared is V4's after logs (wave-four content, one commit before `3100da99`), not a fresh HEAD run; own-size references are HEAD snippets; the attribution probe sampled three pages; the cand2 stage copies were deleted after measuring (disk) — `restage_engine.py` rebuilds the engine half.

## `_state` row spec

```json
{"id":"W-304fa","title":"#304 W5a filed report - five no-ruling defects from candidate 2 fixed at their generators: receipt gate skips APOLLO-DEMO-fenced scripts, icon-source reads markup only, leading-trim scaffold stops at the next component scope (root default + 111 copies), right chart gutter computed from labels (ds-012b twin), geometry frames = the chain of nested scroll boxes","home":"notes/_subreports/2026-09-27-304-W5a-gate-bugs-and-trim.md","links":["knowledge/_validate_receipt.py","knowledge/_validate_screen.py","knowledge/_validate_geometry.py","knowledge/canon/gen_canon_components.py","knowledge/canon/canon.css","knowledge/canon/dv-behaviour.js","notes/_lanes/304/R4c/harness/views.py","notes/_lanes/304/W5a/gen_fixtures.py","notes/_lanes/304/W5a/test_icons_markup.py","notes/_lanes/304/W5a/measure/"],"project":"apollo","opened":304,"state":"open","owner":"claude","condition":"stated","body":"s218-D7 filed report, wave five seat W5a (#304). cand2 r1/r2/r3: receipt reds 6/6/10 -> 0/0/10 (r3 = address line, Dave's), screen gate FAIL x3 -> PASS/PASS/FAIL, own-size 82/104/146 -> 0/0/0, right-edge cut text 2/4/4 -> 0, harness collisions 7/5/0 -> 1/0/0, ink/view 5.10 -> 2.10. Premise corrected: the binding trim was canon.css's root default, not only the shell/bento copies; the KPI +4px is the bento's spark height, not a trim (Dave Q2). Combo page 34,768/34,816 after a num()/up() saving. 27 receipts re-driven, 0 measurement changes. Geometry 166+58 pages unchanged. 148-step clone survey: failure blocks identical to V4, no green-to-red.","closes_when":"a verifier that built none of it re-runs _validate_receipt --selftest, _validate_geometry --selftest, score.py selftest-views and test_icons_markup.py at the seat, re-measures own-size on one cand2 run restaged on the W5a canon (0 findings), and files under notes/_subreports/ citing this report; Dave has answered Q1 (chart script address) and Q2 (Kpi spark in the bento)"}
```
