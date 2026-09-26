# Run report — v1013-r1 (Spider v1.0.13, Opus 5.5)

**Lane: on-canon.** Pack zip sha256 `5d4df132…282c6`, matched. The frozen build is `out/`, and the entry page is `out/index.html`. Ten linked pages, separate files, referencing `../pack/` in place.

## Pack files read, in order
1. CLAUDE.md (= AGENTS.md)
2. FIRST-SESSION.md
3. README.md
4. skills/generate-from-canon, check-with-gates, grill-me, check-against-design-system and usability-review
5. showroom/index.json
6. knowledge/_RUNBOOK-compose-from-canon.md
7. `--help` for gen_provenance_receipt, _validate_receipt, _validate_screen and _validate_compose
8. _render/_bento_edit_rails.json
9. The bodies of about 23 component snippets and all 14 chart snippets, with the APOLLO-DEMO fences stripped
10. The dv-render*.js headers, the relevant canon.css scopes, and the metas of the components I used

## What I built
- **Pages:** Overview, Accounts and transactions, Liquidity and funding, Payments and approvals, FX and markets, Risk and limits, Trade finance, Reports, Messages and service requests, Settings.
- **Frame:** the App-shell-side-nav frame. Inside it sit the Template-dashboard-bento header and bento wall, with lead, evidence and context groups, using spans of 6 and 3 plus the 4+2 split. The wall sits on `--surface-subtle`. The Common dashboard dial is set to 24 for the wall and 4 for the groups.
- **Components:** Kpi-tile, Filter-toolbar-bar, Data-grid, Drawer, Modals, Toast, Summary, Status-indicator, Limits-meter, Timeline, Alert, Input-fields, Textarea, Selection-controls, Segmented-control and Empty-state.
- **Charts:** all 14 chart snippet types, drawn by the pack engine (`dvRender`), each with its legend, tooltip, table and CSV copy.
- **Data:** one seeded `DATA` object: 9 entities, 8 currencies, 30-day series and 360 transactions, plus payments, positions, exceptions, trade, hedges and messages. FX rates are illustrative and fixed.
- **Workflows:** approve and reject (dual control above £10m), risk acknowledgement with an audit note, drawdown, hedge quote, trade instructions, service request, reply, report run, CSV exports and settings. All are validated, persisted to localStorage and audited.
- **Drill-through:** exposure columns and links open Risk scoped to that region, at the positions and limits.
- **Persistence:** filters, theme, navigation and grid state are kept in URL query parameters and in localStorage.

## Questions I would have asked, and the default taken
- Shell for ten destinations: the side-nav frame.
- Dark page ground: the rail's grey equals the tile surface in dark (measured 31,31,31 on both). I used `--background-default` in dark.
- Wall spacing: 24/4, the rails' Common default, where the template ships 40.
- Thresholds: £10m dual control, a £400m buffer and a 75% ceiling.
- Mobile: not a target.

All six grill answers came from the prompt. They are recorded in `out/briefs/`.

## Proof

| Step | Command | Result |
|---|---|---|
| Baseline before building | `python3 ci-template/run-gates.py` | 34 pass, 7 FAIL (all inherited: composition, grid, polarities, receipt, roles_resolve, token_forks, type_blast_radius) |
| Runner after the build | same | Identical 34/7 verdict set. My pages are **not** in the runner's population. |
| Provenance | `gen_provenance_receipt.py --compose` for the splice, then `--mint` on each page, then `--check` | PASS on every page. |
| Receipt | `_validate_receipt.py` on all 10 pages | PASS (+2 UNPROVEN: retrievalSet, and meta:NONE on the spliced shell footer) |
| Screen checks | `_validate_screen.py` on all 10 pages | PASS on all 10. Compose ✅, icon-source ✅, a11y ✅. Composition is UNPROVEN (C9 bands), because the pages link canon.css and carry no bento grammar of their own. |
| State contrast | `_validate_screen.py --render index.html` | **Not run.** It was killed at the 180 s call cap before finishing. |
| Driven | `_proof/drive/drive1.py`, `drive2.py`, `drive3.py` | 31/31 and 41/41 PASS: filters, persistence, theme, grids, drawer focus, tooltip, legend, drill-through, every workflow's invalid and valid path, downloads. |
| Geometry and spacing | `spacing.py`, 800–1600px, light and dark | Wall gaps 24, group gaps 4, card padding 24, KPI padding 16, header 24/32, left edges aligned. No overlaps, clipping or horizontal scroll at 1280–1600. |
| Console | `allprobe.py`, light and dark | 0 errors, 0 warnings on all pages |

Visual review is **unavailable** (vision disabled); screenshots are not evidence.

## Fixes made from measurement
Charts rendered after dv-behaviour's init now get `dv-fit-on`. The template's chart CSS leaked onto a nested donut, repaired with `width:auto`. Drill links got a 16px gap clear of the legend's hit areas. Focus now returns after close on re-rendered rows. Long forms moved from Modal to Drawer, because the modal does not scroll.

## Gaps
1. The chart engine is loaded by `<script src>`, not inlined as AUTO-BEHAVIOUR splices. Inlining trips `_validate_screen`'s icon-source step on engine source text. This is inherited: a comment containing "<svg>" in dv-render.js, and `d="' + arc(` in dv-render-donut.js.
2. Composition C9 is UNPROVEN on every page, and state contrast was never measured.
3. Some charts are scoped by design and labelled on screen: as-at snapshots ignore dates; market rates, group messages and reports ignore entity and region.
4. The Data-grid keyboard model is simplified: no cell arrow navigation, column filters or resize.
5. The approval modal does not scroll, so it could clip on short viewports.
6. Phone width (390px) overflows the content column by about 57px. It was not targeted.
7. Legend key letters inside bars block the tooltip when you hover directly over the letter. This is inherited.
8. There is no licensed HSBC typeface in the pack, so text falls back to Helvetica/Arial.
9. Everything is simulated, per browser, with no live connections; this is not production banking capability. With JavaScript off there is no data.
