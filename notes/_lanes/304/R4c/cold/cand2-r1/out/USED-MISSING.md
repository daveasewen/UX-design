# Used / missing — CEO international-banking prototype (cand2-r1)

Lane: **on-canon** (ADS skills from the pack). Brief: `briefs/2026-09-27-ceo-international-banking-grill.md` (theme Common, light+dark, bento, comfortable, wide desktop, masterbrand only, placeholder data, no invention).
Seed: `python3 knowledge/_compose_slice.py "<brief>" --out seed.json --explain` (in `_proof/seed.json`).

## Decision table (question → role → component → `when` → rulings)
| question | role | component | why (graph) |
|---|---|---|---|
| page frame, 10 destinations | page-frame | app-shell-side-nav (+ its footer) | top-nav `when` = destinations ≤ 7; 10 > 7 ⇒ side nav |
| can we fund our plans? (series exists) | headline-metric | kpi-tile, `as-link` variant | kpi-tile `when`: series ≠ none beats stat-card |
| layout | arrangement | template-dashboard-bento `$bentoGrammar` (c-bento, tpl-group lead/evidence/context) | rule 7a, s217-D2/D3, s245-D6/D7; spans 6 only (square at every band) |
| section ground | dial | rails `bentoBg=grey` → `--surface-subtle` | the prompt; `_bento_edit_rails.json` |
| change over time | chart-panel | chart-line (multiline), stacked-area, combo, column, candlestick, sparkline | dvRender specs from DATA |
| compare across entities/regions/currencies | chart-panel | chart-bar (bar, grouped, stacked), butterfly-h, bullet, scatter, boxplot, histogram | idem |
| share of a whole | chart-panel | chart-donut, chart-pie | ≤ 6 slices (dv-pie-009) |
| records read down columns | record-list | data-grid (verbatim markup + verbatim script) | comparison test (s274-D4) ⇒ table; grid owns sort/filter/select |
| records read across a row | record-list | list-items (+ search-field, pagination) | s274-D6 default provider |
| record detail / workflow | overlay | drawer (verbatim #scrim/#sheet) | one modal surface at a time ⇒ approve is two-step inside the drawer |
| bulk / destructive confirm | overlay | modals (ids renamed) | never opened over the drawer |
| confirmation | feedback | toast (verbatim region) | transient, never the only record |
| in-flow warnings | feedback | alert | persists until resolved |
| name-value facts | — | summary | rows ≥ 2 |
| audit trail | — | timeline | happened, newest-first by entry |
| limit use | — | limits-meter (lim-stack) | cap spent against; full = blocked |
| filters / prefs | input | dropdown (boxed), segmented-control, search-field, textarea, input-fields, selection-controls | textarea `when`: a sentence expected |

## Tokens and rules drawn on
canon.css + type.css; theme attrs on `<html>`; `.t-cm-*`/`.t-ed-*` composites only; one page token (`--surface-subtle`); icons byte-copied from `assets/icons` (sprite) and the snippets' own sprites; masterbrand light/dark logos.

## Gaps (see RUN-REPORT for the full list)
Shell ships at a 640px specimen height; dark-mode ground = tile colour; nested-scope text-box-trim shrinks chart legend buttons; data-grid pager has no ellipsis; receipt gate requires the APOLLO-DEMO-fenced grid script; JS-off shows empty charts/tables; composition C9 cannot read linked CSS.
