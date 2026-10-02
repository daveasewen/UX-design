# Read log

**Slash command resolution:** `/generate-from-canon` resolved to `.github/prompts/generate-from-canon.prompt.md`, which says "Read `skills/generate-from-canon/SKILL.md` … and follow it". That SKILL.md is the instruction set I followed. The grill came first, from `skills/grill-me/SKILL.md`, because `briefs/` did not exist (CLAUDE.md §2).

**Not opened, by the session's conditions or the skill's rules:**
- Any `notes/`, `reviews/` or `_DECISION-HISTORY/` folder, plus `_CHAIN.md`, `GOOD-MORNING.md`, `_LIVE-STATE.md` and `knowledge/_rulings.json`. `_memento_search.py` was not run.
- The source of any `_*.py`. `knowledge/_compose_slice.py` was **run** only, because the skill says to run it; its `--help` prints its own docstring, which I read as program output.
- Any template snippet or meta (rule 1a).
- `FIRST-SESSION.md`, `README.md`, `AGENTS.md`, `_MANIFEST.json` and `.vscode/settings.json`.
- Any showroom `.html` page or `_thumbs/*.png`, because there are no eyes in this session.
- No gate, validator, browser or node run.

## Files opened

| file | how much | why |
|---|---|---|
| `CLAUDE.md` | whole (4,180 B; given in context) | design contract |
| `.github/prompts/generate-from-canon.prompt.md` | whole, 16 lines | slash-command resolution |
| `skills/generate-from-canon/SKILL.md` | whole, 359 lines | the instruction set |
| `skills/grill-me/SKILL.md` | whole, 209 lines | the grill |
| `skills/grill-me/brief-template.md` | whole, 42 lines | the brief's shape (its filled example was **not** used as answers) |
| directory listings (`ls`/`wc`) | root, `skills/*`, `.github/prompts`, `.vscode`, `out`, `knowledge`, `knowledge/canon`, `knowledge/_render`, `knowledge/tokens`, `showroom/_foundations`; sizes of candidate metas and snippets | orientation |
| `knowledge/_compose_slice.py` — **run output only** | `--help` first 60 lines; three seed runs with `--explain` (summary printouts); one `--ask` (first 40 lines) | step 1 |
| scratch `seed.json` (110,628 B) | python-extracted: all 21 `components` (id, roles, when, snippet, meta, consumes, hasPart); all 38 `governs` (id, over, ruled text up to the print width); all 11 `mustNot`; all 15 `unresolved`; all 18 `assets`. `obeys` only as the 12 rows `--explain` printed; `tokens` only its one summary line | step 1 |
| scratch `seed-chart-trend.json`, `seed-chart-mix.json` | python-extracted: components (when, snippet, meta), governs (ruled up to 260 chars), mustNot | `unresolved` role:chart |
| `showroom/index.json` (91,957 B) | python-extracted: slug, level, status and blurb (first 90 chars) for every component | what exists |
| `knowledge/_render/_bento_edit_rails.json` | whole, 1,271 lines | layout dials and console defaults |
| `knowledge/_RUNBOOK-compose-from-canon.md` | whole, 206 lines | step 5's long version |
| `knowledge/canon/canon.css` (1,835,661 B) | **grep and line ranges only**, never whole: L1100–1215 (bento core); L17538–17650, L17760–17800, L18050–18104, L18100–18320 (dashboard-bento scope rules); L6320–6340 plus grep (app-shell-top-nav); one-line greps for the scope list, `sh-*`, `is-full`, `.dg{`, `.dv-stage`, `.dv-leg`, `.dbtn`, `.ftb-*`, `.rwy`, `.metric`, `.sheet`, `[hidden]`, `up-is-bad` and theme selectors. About 650 lines in all | to know which classes exist; not copied |
| `knowledge/canon/type.css` | grep of the composite class list only | type composites |
| `knowledge/canon/dv-render.js` | L1–140, L155–384 | the engine's spec contract |
| `knowledge/canon/dv-legend.js` | L20–129 plus grep | the lazy legend cache (`__dv`) |
| `knowledge/canon/dv-render-line.js` | L1–60 plus grep | marker shapes, zero-baseline note |
| `knowledge/canon/dv-behaviour.js`, `dv-donut-sweep.js` | grep only (hooks, globals) | load order |
| `knowledge/tokens/themes/_themes.json` | first 60 lines | console theme registry |
| `knowledge/components/*.meta.json` (python field extracts, not read whole) | metric, runway-bar, data-grid, list-items, table, filter-toolbar-bar: purpose, when, priority, shape, answers, variants, antiPatterns, behaviour, edges (truncated 500–1,500 chars each). app-shell-top-nav, navigations, footer, page-header-lockup, section-heading-lockup, chart-line, chart-donut, drawer: purpose, when, span, props, variants, antiPatterns, behaviour, edges. metric props (each up to 400 chars). status-indicator (when, variants, antiPatterns). cards (purpose, when, provides, variants, antiPatterns) | step 3 contracts |
| `knowledge/snippets/App-shell-top-nav.reference.html` | whole except its 284-line `<style>` (viewed through a style-eliding viewer) | markup and script |
| `knowledge/snippets/Navigations.reference.html` | L332–397 (body) and L492–677 (manifest and script) | behaviour address and script |
| `knowledge/snippets/Page-header-lockup.reference.html` | whole except `<style>` | markup |
| `knowledge/snippets/Section-heading-lockup.reference.html` | whole except `<style>` | markup (A, C) |
| `knowledge/snippets/Metric.reference.html` | L1–124 (header) and L396–720 (body); `<style>` and token-manifest not read | markup and states |
| `knowledge/snippets/Runway-bar.reference.html` | body and manifest; `<style>` elided | markup |
| `knowledge/snippets/Chart-line.reference.html` | L1–54, L377–502, L535–549, L1778–1894. AUTO-BEHAVIOUR blocks were extracted programmatically and confirmed to contain the canon `dv-*.js` sources, not read by eye | figure markup and call pattern |
| `knowledge/snippets/Chart-donut.reference.html` | L1–52, L327–469, L505–520, L1486–1516. AUTO-BEHAVIOUR blocks extracted programmatically | figure markup, call, load order |
| `knowledge/snippets/Data-grid.reference.html` | L1–83 (header), L441–464 (to see the fenced demo CSS), L476–1175 (body and scripts) | markup and script |
| `knowledge/snippets/Filter-toolbar-bar.reference.html` | L1–50 and L412–1091 | markup and script |
| `knowledge/snippets/Status-indicator.reference.html` | body (style elided) | `.stat` markup |
| `knowledge/snippets/Drawer.reference.html` | body and script (style elided) | markup and script |
| `knowledge/snippets/Summary.reference.html` | body (style elided) | `dl.summary` markup |
| `knowledge/snippets/Footer.reference.html` | body and script (style elided) | markup and script part (a) |
| `knowledge/snippets/List-items.reference.html` | body (style elided) and L237–261 (script) | transaction-row markup and roving script |
| `knowledge/snippets/Cards.reference.html` | grep only | looking for a static panel (none fit) |
| scratch `dashboard.src.html`, `splice.py` | written by me | build source and verbatim splicer |
| `out/brief.md`, `out/GAPS.md`, `out/dashboard.html` | written by me | outputs |

## Copied vs re-drawn

**Copied from the snippet** (whole markup; `APOLLO-DEMO` spans and `demo-*` classes dropped):
- The App-shell-top-nav frame: skip link, masthead, logo pair, nav, actions, sheet and scrim. The breadcrumbs region and the profile action were left out, and the nav labels changed.
- Page-header-lockup "simple" with the meta line.
- Section-heading-lockup arrangements A and C.
- The Filter-toolbar-bar form: search, three dropdowns, context row and `.ftb-msg`.
- Data-grid: head, toolbar, chips bar, the grid's header anatomy (sort, colf, rsz, colmenu, selection-controls checkbox) and the foot. Columns re-keyed to seven.
- Chart-line and Chart-donut figures: dv-head, controls, details/table spine, stage, svg canvas, legend and live region. The donut "No data" frame and the line one are the snippets' own Empty-state-by-reference markup.
- Drawer sheet, head, body and foot (`.dbtn`).
- Footer default.
- Icon `<symbol>`s, from the snippets that byte-matched them to `knowledge/assets/icons`.

**Copied verbatim as script:**
- The six engine `AUTO-BEHAVIOUR` blocks, spliced byte for byte by `splice.py`.
- Footer script part (a).
- From Filter-toolbar-bar's script: the Search-field clear, `wireDD`/`ddLabel` and `wireDismiss` blocks.

**Rendered by authored JS, using the snippet's own markup pattern** (the pattern was copied; the data is mine):
- Metric tiles, including the spark polyline computed with the snippet's 200×48 recipe.
- Runway-bar readout.
- List-items transaction rows.
- Grid rows, carried from the grid's own template and extended to seven columns.
- Summary rows in the drawer.
- Status-indicator `.stat` spans.
- Legend rows, carried from the chart snippets' legend `<li>`.
- Dropdown options, carried from the toolbar's `.optgrp`/`.opt` markup.

**Carried and extended (authored JS):**
- Shell off-canvas: one shell.
- Navigations selection: switches the view.
- Toolbar driver: no view or density, seed from the URL.
- Data-grid script: row source, columns, drawer hand-off, URL state, windowed pager.
- Drawer script: content, approve, opener focus.
- List-items roving walk: re-armed per render.

**Re-drawn: nothing.** No component CSS was written. The page's one CSS rule is placement.

**Authored outright:** the `DATA` builder, the selection, KPI, runway and chart arithmetic, URL/mode persistence, CSV export and approval logic.
