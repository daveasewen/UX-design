# #304 R4s: the six cold runs scored, v1.0.13 against the v1.0.14 candidate

Scoring seat for Run 4, run Saturday night into Sunday 27 September 2026. Nothing was committed or pushed, there were no git calls and no Project memory. The six frozen outputs were not touched: every render ran against the harness's stage copies at `$HOME/r4c/stage/cold-<run>/`.

**Review page for Dave:** `notes/_REVIEW-304-v1013-vs-candidate-2026-09-27-v1.html`

## The answer

Composing stopped the tracing. It did not make the pages better.

- **Template-likeness halved.** The rendered-DOM trace index fell from a mean of 0.379 (TRACED, v1.0.13) to 0.178 (PARTLY TRACED, candidate). Shared 5-gram structure fell from 0.134 to 0.022. What the candidate still shares with the template is the ruled bento grammar classes its skill permits: `tpl-wall`, `tpl-group-*` and `c-bento`.
- **More canon parts.** The candidate uses 14.7 non-chart canon components per run against v1.0.13's 6.3. That count is rendered `cn-` scopes across all ten destinations.
- **Quality tied.** Scored like for like, both groups average 10.0 out of 12. Geometry is 1 of 3 at 1440 and 0 at 390 on all six runs.
- **The harness as it ran** gave v1.0.13 10.0 and the candidate 8.0. That gap comes from the harness, not the pages (see "Harness defects").

**Recommendation, for Dave's decision:** do not cut v1.0.14 on Tuesday as the candidate stands. Cut only after these four fixes land and one confirming cold run then beats 10.0:

1. the Kpi-tile label crop;
2. the Common gutter key;
3. a full-height side-nav shell;
4. one ruled chart receipt address.

## Scorecard

Receipts: `notes/_lanes/304/R4s/review-data.json`, built by `build_review.py` from the files listed below.

| run | harness /12 | like-for-like /12 | geometry 1440/390 | trace index (rendered) | non-chart parts (all parts) | charts / types across 10 destinations | geometry kinds at 1440 | pack screen gate | shell frame |
|---|---|---|---|---|---|---|---|---|---|
| v1013-r1 | 9 | 9 | 1/0 | 0.370 | 8 (22) | 31 / 18 | G10, G1b, G6 | PASS | 1000px |
| v1013-r2 | 10 | 10 | 1/0 | 0.369 | 5 (19) | 29 / 18 | G10 | PASS | 640px |
| v1013-r3 | 11 | 11 | 1/0 | 0.398 | 6 (20) | 31 / 18 | G10 | PASS | none |
| cand-r1 | 8 | 10 | 1/0 | 0.156 | 17 (30) | 32 / 17 | G6, G8 | FAIL | 640px |
| cand-r2 | 7 | 9 | 1/0 | 0.185 | 16 (29) | 24 / 16 | G6, G8 | FAIL | 640px |
| cand-r3 | 9 | 11 | 1/0 | 0.193 | 11 (24) | 22 / 16 | G8 | FAIL | 640px |

The four rubric parts, in the order rich · full · persistent · interactive:

| run | harness | like for like |
|---|---|---|
| v1013-r1 | 2·3·2·2 | 2·3·2·2 |
| v1013-r2 | 2·3·2·3 | 2·3·2·3 |
| v1013-r3 | 3·3·3·2 | 3·3·3·2 |
| cand-r1 | 1·2·2·3 | 2·3·2·3 |
| cand-r2 | 2·1·2·2 | 2·3·2·2 |
| cand-r3 | 1·2·3·3 | 2·3·3·3 |

## What was scored, exactly

**The harness.** `score.py all` ran on every run with that run's own pack and `--copy-out`, through stage, static, gates, render, drive and ext, until the card printed.
- v1.0.13: the entry page, plus the nine linked files probed in light only.
- Candidates: the entry page only, which is the first view.
- Geometry at 1440 and 390, and own-size at 1440: the overview, on all six runs.

**R4s, to make the two shapes comparable.** One seat call per batch.
- `notes/_lanes/304/R4s/views.py` reaches all ten destinations of every run: the candidates' views by `?view=` (cand-r1) or `#/` (cand-r2, cand-r3), and v1.0.13's ten files. At each destination, at 1440×1000, it records:
  - the charts that have marks, and their types;
  - charts cut by anything once the 640px shell frame is released (`.sh{height:auto}`, declared);
  - visible table rows;
  - the prompt's keywords in the rendered text.
- It also takes full-length light shots of every destination, the overview as shipped at 1440 and at 390, and the overview in dark, reached through the run's own Dark button.
- `defects.py` measures bento gutters, KPI and nav group label contrast (opacity included), the KPI label clip and the shell height.
- `comps.py` counts the rendered `cn-` scopes across all ten destinations.

**Like for like.** The harness's own rules (`score.py` lines 505–545) were applied to that data:
- Rich: counted over all ten destinations. "Clipped" still counts the as-shipped shell frame, as the harness does.
- Full: rendered KPI and question words, and the most rows found at any destination.
- Persistent and interactive: the harness's own drive, unchanged.

## Harness defects found (fix in R4c)

1. **Theme check.** The harness clicks the first control matching the switch. That control is "Light", and the page is already light, so the theme reads FAIL on all six runs. Clicking each run's own Dark button flips `data-theme` to dark on all six (`views/<run>/views.json` → `overview.dark_switch`).
2. **Views.** Render probes only linked files, so a one-file app with ten views is scored on its first view.
3. **Keywords.** They are read from source text, which misses text written by JS. cand-r2 read KPI 0/3 and questions 0/3 from source; rendered, it reads 3/3 and 3/3.
4. **Clipping.** "Clipped" counts charts below the fold inside a scrolling shell frame. With the frame released, no chart on any of the 60 destinations is cut.
5. **Dataviz gate.** `_validate_dataviz` dv-004 fails every generated page, because it demands a chart-engine test-page mapping. That is a pack-gate defect: the rule does not fit generated pages.

## Defects the cold runs surfaced, checked here

**(a) Common gets Mono's 40px bento gutter.** Confirmed.
- **Where:** the `AUTO-BENTO-ROLE-VARS` block in `canon.css` (repo lines 22018–22033, the same in both packs) keys `--bento-dashboard-main` for mono, legacy, console and supercharge, but not common.
- **Measured:** the wall gap is 40px on v1013-r2, v1013-r3 and all three candidates. v1013-r1 set 24px itself.
- **Fix, canon:** `canon/gen_bento_role_vars.py` should emit `common` beside `legacy`.

**(b) The receipt mint and the receipt gate name different chart scripts.** Confirmed, and already present in v1.0.13.
- **Where:** `gen_provenance_receipt.behaviour_address()` resolves the snippet's AUTO-BEHAVIOUR marker, through `component-types.json`, to `knowledge/canon/dv-behaviour.js`. Every chart meta says `knowledge/canon/dv-render.js`. `_validate_receipt.py` trusts the meta.
- **Reproduced:** composing one Chart-line with each pack's own `--compose` gives FAIL:BEHAVIOUR-ADDRESS-DISAGREES in both packs (`$HOME/r4s-repro/`). The repo's mint is identical to the candidate's.
- **Why only the candidate shows it:** the candidate's runs splice and receipt the chart figures, so the mismatch surfaces there.
- **Fix, tooling (mint and gate):** first Dave rules, in one line, which address a chart region carries.

**(c) App-shell-side-nav is a fixed 640px specimen frame.** Confirmed.
- **Where:** `canon.css`:5678. The doormat shell (4697) and the multi-column shell (5148) are the same.
- **Measured:** the shell is 640px high on v1013-r2 and on all three candidates. v1013-r1 set it to 1000px; v1013-r3 has no shell.
- **Effect:** at 1440×1000 the page sits in a box with about 360px of blank below it.
- **Fix, component:** a full-viewport form of the shell. The generate skill's wording needs to follow, because the candidates kept 640px on the skill's rule against resizing a part.

**(d) Contrast inherited in Common.** Confirmed on all six runs; both are 14px/400 text, which needs 4.5:1.
- **KPI label and period:** 3.71:1 in light, 6.72:1 in dark. The cause is `--alpha-60` on Common's #333 ink: `.kpi-tile .lbl16` (17932), `.kpi-lbl` (13070) and `.kpi-per` (13098).
- **Side-nav group label:** 3.75:1 in both light and dark. The cause is `.sn-group-label` with `opacity:.72` on `--muted` (5787).
- **Fix:** canon.

**(e) How much each run traced the template.** Measured above.
- **Trace index:** v1.0.13 0.370 / 0.369 / 0.398; candidate 0.156 / 0.185 / 0.193.
- **Template-only classes used:** 89% against 47%.
- **By eye:** the three v1.0.13 overviews share one skeleton. The three candidates differ from each other, and two are organised under the three CEO questions.

**(f) New: Kpi-tile clips its own label's descenders.**
- **Where:** `canon.css`:13070 combines `overflow:hidden` with `text-box-edge:text text` and a 14px line box.
- **Measured:** 2px of each label is cut on all three candidates. 4b's geometry gate on the pack's own `Kpi-tile.reference.html` finds 12 cut labels at 1440.
- **Why v1.0.13 escapes it:** its runs traced the template's `lbl16` KPI instead of composing Kpi-tile.
- **Fix:** component.

**(g) New: the donut centre prints the raw floating-point sum.**
- **Seen:** "791.9000000000001" (v1013-r1) and "2990.8999999999996" (cand-r3).
- **Where:** `dv-render-donut.js`:135 prints `String(total)`, and dv-legend does the same.
- **Fix:** chart engine.

**Seen by eye, cause not proven:**
- Y-axis tick labels are cut at the left on five of six runs.
- The 30 daily x labels collide on four of six.
- Donut and pie charts stretch to the full tile height, leaving empty bands.
- Own-size S1 is the same on all six: legend buttons measure 16.7px against a 20px reference. It does not separate the two groups.

## Looked at by eye (vision)

- The six as-shipped 1440 overviews.
- The six full-length light overviews and the six dark ones.
- A 390 montage (`notes/_lanes/304/R4s/montage-390.png`).
- The review page itself at 1440 and 390: no page errors, no horizontal scroll.

## Files

- `notes/_REVIEW-304-v1013-vs-candidate-2026-09-27-v1.html`: house CSS and the decisions overlay copied from `notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html`; only the CFG is swapped.
- `notes/_lanes/304/R4s/`:
  - scripts: `views.py`, `defects.py`, `comps.py`, `build_review.py`
  - data: `review-data.json`, and per run `views/<run>/` holding `views.json`, `defects.json`, `comps.json`, the overview PNGs and nine view JPEGs
  - images: `montage-390.png` and the QA pngs of the review page
- `notes/_lanes/304/R4c/runs/cold-{v1013-r1..r3,cand-r1..r3}/`: the harness output (scorecard.json and .html, the phase JSONs, shots).
- Seat-local only: `$HOME/r4c/stage/` and `$HOME/r4s-repro/`.
