# Read log

## Slash command resolution

`/generate-from-canon` is not one of the session's registered skills. It resolved to **`.github/prompts/generate-from-canon.prompt.md`** (the pack's VS Code / Copilot prompt file), whose whole instruction is "Read `skills/generate-from-canon/SKILL.md` … and follow it". So the governing skill was **`skills/generate-from-canon/SKILL.md`** (`ADS-generate-from-canon`).

## Rules of this session, as kept

- Nothing outside `Apollo-Spider-v1.0.15/` was read.
- No `_*.py` source was read. `knowledge/_compose_slice.py` was **run**: `--help`, which prints its docstring, three seed runs and one `--ask`, as the skill directs. `_memento_search.py` was not run.
- No `notes/`, `reviews/` or `_DECISION-HISTORY/` folder was opened, and none of `_CHAIN.md`, `GOOD-MORNING.md`, `_LIVE-STATE.md` or `knowledge/_rulings.json`. Ruling text below comes only from the seed's `governs` rows, which the reader produced.
- No render, screenshot, browser, Playwright, node check, gate or validator.

## Files opened

"Full" means every line was read. Byte and line counts are the file's own.

| # | file | how much | why | copied vs re-drawn |
|---|---|---|---|---|
| 1 | `CLAUDE.md` | full (4,180 B), provided in context | the design contract | — |
| 2 | `.github/prompts/generate-from-canon.prompt.md` | full (~0.5 KB) | slash-command resolution | — |
| 3 | `skills/generate-from-canon/SKILL.md` | full (359 lines) | the governing skill | — |
| 4 | `skills/grill-me/SKILL.md` | full (209 lines) | grill (no `briefs/`) | — |
| 5 | `skills/grill-me/brief-template.md` | full | brief shape | brief follows its table shape |
| 6 | `skills/check-with-gates/SKILL.md` | full (170 lines) | CLAUDE.md rule "check before you show" | nothing run (session forbids). Commands owed are listed in GAPS.md |
| 7 | `knowledge/_RUNBOOK-compose-from-canon.md` | full (206 lines) | named by the skill (step 5) | — |
| 8 | `knowledge/_compose_slice.py` | **source not read**. Ran `--help` (docstring output) | seed reader | — |
| 9 | `out/seed.json`, `out/seed-filters.json`, `out/seed-payments.json` (my own seed output) | read through python: components (id, roles, when ≤700 chars, snippet, meta), `unresolved`, `$nulls`, `governs` rows filtered to the chosen parts (`ruled` ≤200 chars) | decision table | — |
| 10 | `knowledge/snippets/App-shell-top-nav.reference.html` | **full** (773 lines, 52 KB) | page frame | **copied**: masthead, menu button, logo `<img>` pair, nav, actions, breadcrumb strip, `main.sh-main`, slim footer, scrim + sheet markup; sprite symbols `ic-menu`, `ic-close`, `ic-search`, `ic-account` spliced byte-identical by script; off-canvas script carried (open order verbatim), extended for one shell + view switching. Its own `<style>` (hex theme blocks) **not** copied: the `.cn-app-shell-top-nav` scope in canon.css paints it. Skeleton bones not copied (real content instead). |
| 11 | `knowledge/canon/canon.css` (1.8 MB) | **partial**: grep counts for ~40 scoped selectors; lines 925–945 (`.canon` base); 1074–1246 (AUTO-BENTO, full); 1413–1511 (cn-list-items selectors, via grep); ~6271–6400 (cn-app-shell-top-nav, via grep); 11687–11708 (cn-drawer positioning, grep); 12386–12479 (cn-filter-toolbar-bar lnk / ftb-outer / ftb-msg, grep); 13963–14036 (cn-metric board/spark, grep); 17530–18330 (**full**: the `.cn-template-dashboard-bento` scope: vars, bento splice, layout primitives, module recipes, masthead, footer, instance dials 1–11) | layout grammar, scope existence, defects | **linked, not copied into the page**. A byte-identical copy is placed beside the page as `out/canon.css` (sha256 5922da9bfc1a…) |
| 12 | `knowledge/canon/type.css` | grep only (composite names, `--uf`) | type composites | linked; byte-identical copy at `out/type.css` |
| 13 | `knowledge/_render/_bento_edit_rails.json` (42 KB) | **partial**, through python: top-level outline; `rail`; dials `mainSpacing`, `subSpacing`, `grouping` (full); `defaults.values.dashboard` (full); `legality`, `$open_questions`, `constraints.exclusions` (first 2 KB) | layout dials / defaults | nothing set by hand: defaults ship through the scope |
| 14 | `knowledge/components/metric.meta.json` | fields `edges`, `purpose`, `when`, `with`, `props`, `variants`, `slots`, `accessibility`, `antiPatterns`, `states`, `responsive`, `count` (each ≤1.5 KB printed) + lines 330–360 | contract | — |
| 15 | `knowledge/components/{chart-line, chart-stacked-area, filter-toolbar-bar, list-items, pagination, drawer, summary, page-header-lockup, dropdown, search-field, segmented-control, footer, app-shell-top-nav, status-indicator}.meta.json` | key list + `edges.groupsWith`, `edges.mustNotNeighbour`, `edges.yieldsTo`, `behaviour` (each ≤900 chars) | contract, grouping, prohibitions | — |
| 16 | `knowledge/components/pagination.meta.json` | + `purpose`, `props`, `variants`, `accessibility`, `antiPatterns`, `states` (≤900 chars each) | contract | — |
| 17 | `knowledge/components/section-heading-lockup.meta.json` | `purpose`, `props` (incl. the full `placement` note), `variants`, `antiPatterns` | contract | — |
| 18 | `knowledge/components/*.meta.json` | `grep -l groupsWith` (filenames only); `grep -n groupsWith` on metric / chart-bar / navigations (single lines) | rule 7b | `template-dashboard-bento.meta.json` appeared as a **filename in a grep listing only**. Its content was never opened (rule 1a). |
| 19 | `knowledge/snippets/Metric.reference.html` (749 lines) | lines 1–60 (header) and **396–749 (full body)** + a grep map | headline metric | **copied**: `.metric` anatomy (label, value + unit, delta with glyph / figure / period, spark svg `dv-base` / `dv-area` / `dv-series`, the `is-empty` note form); symbols `metric-up`, `-down`, `-flat`, `-none` spliced byte-identical by script. **Authored**: the values and the spark polyline/polygon points, computed from DATA on the snippet's own 200×48 viewBox recipe. `.board` wrapper not used (the bento group is the board). |
| 20 | `knowledge/snippets/Chart-line.reference.html` (1,895 lines) | grep map; lines **376–550** (markup + manifests) and **1778–1895** (engine call), full | the chart | **copied**: the multi-series figure (figcaption, `dv-head`, title, Copy CSV button, `details.dv-tbl` table spine, `dv-stage`/`dv-chart-area`/`svg.dv-fit` canvas, legend rows, `dv-sr` live region), with ids and series names changed. **Spliced byte-identical by script** (bytes not read line by line): the four AUTO-BEHAVIOUR blocks dv-behaviour, dv-legend, dv-render, dv-render-line. **Authored**: the `dvRender(figure, spec)` call from DATA, re-run on every filter. |
| 21 | `knowledge/canon/dv-render.js` | lines 1–140 (contract header, `fmt`, `validate`) + grep for `bad(` | spec contract | not linked; the page carries the snippet's injected copy |
| 22 | `knowledge/canon/dv-behaviour.js` | lines 218–240, 336–400 + grep for listeners | resize / seg / init behaviour | — |
| 23 | `knowledge/canon/dv-legend.js`, `dv-render-line.js` | grep only | listener style, `multiline` registration | — |
| 24 | `knowledge/snippets/Chart-stacked-area.reference.html` | grep map; lines 277–340, 373–387, 1656–1690 | evaluated, then **rejected** (dv-014 mustNotNeighbour) | nothing copied; its shared engine blocks were checked byte-equal to Chart-line's |
| 25 | `knowledge/snippets/Filter-toolbar-bar.reference.html` (1,091 lines) | grep map; lines **412–596** and **685–1091**, full | the filter bar | **copied**: the bar (`ftb-outer`, `form.ftb[role=search]`, search, Add-filter dropdown with grouped `optgrp` menu, Date-range dropdown, `seg l` sort group taken from the compact specimen, status line, hint, chips row, Clear all), the `.ftb-msg` empty message; symbols `ic-clear`, `ic-filter`, `ic-calendar`, `ic-alert` spliced byte-identical; Search-field / Dropdown / Segmented / Tags JS **verbatim**; toolbar IIFE **extended** (facets, range, sort, URL, consumer = whole page). **Not carried**: View-as and Density segs, Export menu, the demo consumer table, the segmented control's own resize listener. |
| 26 | `knowledge/snippets/List-items.reference.html` | body (line 120 to end), full | record list | **copied**: `ul.list` › `li` › `button.row` › avatar / body / line / title / `status` chip / desc / amount; roving-focus script extended to delegation. Density dial (APOLLO-DEMO) not copied. |
| 27 | `knowledge/snippets/Pagination.reference.html` | body, full | paging | **copied**: `nav.pg` › `ul` › `.ctrl` prev/next with their inline chevron paths, page `a`s, `aria-current`, ellipsis; script logic carried, delegated, pages rendered from the count |
| 28 | `knowledge/snippets/Drawer.reference.html` | body, full | detail overlay | **copied**: scrim, `sheet[role=dialog]`, head with `close` (inline close path), body, foot with `dbtn primary` / `secondary`; open order (show · 2 frames · focus · inert) and Tab trap carried; opener tracking added |
| 29 | `knowledge/snippets/Summary.reference.html` | body, full | key/value panels | **copied**: `dl.summary` › `.summary__row` › `dt.summary__k` / `dd.summary__v` |
| 30 | `knowledge/snippets/Page-header-lockup.reference.html` | body, first ~150 non-blank lines (arrangements 1–2 and the start of the tabs script) | page title | **copied**: arrangement 1 (`ph-outer` › `ph` › `ph-row` › titleblock: eyebrow / `h1.ph-title` / lede; `ph-actions` with `btn tertiary` + `btn primary`). Tabs foot not used. |
| 31 | `knowledge/snippets/Section-heading-lockup.reference.html` | body, full | group headers | **copied**: arrangement A (`l-stack` › `h2.t-cm-section-label`) and B (`l-row` justify-between › h2 + `a.arrow` › `lbl` + `tip`); symbol `sh-arrow-tip` spliced byte-identical |
| 32 | `knowledge/assets/logos/`, `knowledge/assets/fonts/` | directory listings only | masterbrand | `masterbrand-light-colour.svg` and `masterbrand-dark-colour.svg` copied byte-identical into `out/` |
| 33 | `knowledge/snippets/*` | `wc -c` / `ls` listings | sizing | — |

## Not opened (and why)

- `Template-dashboard-bento.reference.html`, `Template-dashboard.reference.html` and all `Template-*` files and metas: fenced examples (rule 1a).
- `Footer.reference.html`: the shell carries Footer's slim form verbatim, and that copy was used.
- `Navigations.reference.html`, `Breadcrumbs.reference.html`: likewise carried inside the shell snippet.
- `Dropdown`, `Search-field`, `Segmented-control`, `Tags` snippets: the filter bar carries their markup and JS "unedited", and those copies were used.
- `showroom/` pages and thumbnails: no eyes in this session.
- `knowledge/tokens/*.json`: no token was bound by hand. Every value comes from the scopes.
- `knowledge/guidelines/`: the binding rules arrived through the seed's `obeys` rows.

## Files written

- `out/dashboard.html`: the page (266 KB, of which DATA is ~109 KB and the chart engine is ~75 KB). It needs its siblings `out/canon.css`, `out/type.css`, `out/masterbrand-light-colour.svg` and `out/masterbrand-dark-colour.svg`, all byte-identical copies of the pack's files.
- `out/brief.md`, `out/GAPS.md`, `out/READ-LOG.md`.
- `out/seed.json`, `out/seed-filters.json`, `out/seed-payments.json`: the reader's output (provenance).
- `briefs/2026-10-02-corporate-banking-dashboard-grill.md`: the grill brief where ADS-grill-me saves it (`briefs/` created).
- Scratch only (session scratchpad, outside the pack): `gen_data.py` (deterministic DATA generator), `template.html`, `build.py` (splices snippet bytes and DATA into the page and copies the siblings).
