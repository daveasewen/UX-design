# Read log — this session

**The slash command resolved to:** `/generate-from-canon` → `.github/prompts/generate-from-canon.prompt.md` (a VS Code / Copilot prompt file, `mode: agent`). Its only instruction is "Read `skills/generate-from-canon/SKILL.md` … and follow it", so the effective instruction set was **`skills/generate-from-canon/SKILL.md`** (frontmatter name `ADS-generate-from-canon`). There is no `.claude/commands/` in the pack, and the slash command is not a registered Claude Code skill in this environment.

Off-limits by session rule, and **not read**: any `_*.py` source (run only, when a skill said to run it), `notes/`, `reviews/`, `_DECISION-HISTORY/`, `_CHAIN.md`, `GOOD-MORNING.md`, `_LIVE-STATE.md`, `knowledge/_rulings.json`; `_memento_search.py` was not run. Not opened by choice: every template snippet and template meta (SKILL rule 1a), `skills/check-with-gates/SKILL.md` (gates could not be run this session), `README.md`, `FIRST-SESSION.md`, `AGENTS.md`, `_MANIFEST.json`, `showroom/`.

## Files opened, and how much

| # | file | how much | why |
|---|---|---|---|
| 1 | `CLAUDE.md` | whole (4,180 B): supplied in the session context, not opened by a tool | design contract: lane, grill, the five rules |
| 2 | folder listings: `/`, `skills/`, `skills/*/`, `out/`, `.vscode/`, `.github/`, `knowledge/`, `knowledge/canon/`, `knowledge/components/` (names), `knowledge/snippets/` (names + sizes), `knowledge/assets/logos/` | names only | orientation; `briefs/` confirmed absent |
| 3 | `.github/prompts/generate-from-canon.prompt.md` | whole (≈20 lines) | slash-command resolution |
| 4 | `skills/generate-from-canon/SKILL.md` | whole, 359 lines | the instruction set |
| 5 | `skills/grill-me/SKILL.md` | whole, 209 lines | `briefs/` absent, so the grill fires |
| 6 | `skills/grill-me/brief-template.md` | whole, 41 lines | brief shape |
| 7 | `knowledge/_compose_slice.py` | **source not read**. Run: `--help` (prints its contract docstring), two seed runs, six `--ask` runs | SKILL step 1 |
| 8 | seed outputs (scratchpad `seed.json`, `seed-panel-list.json`) | fields extracted by script: components with `when`/`snippet`/`meta`; `unresolved`; `$nulls`; `governs` ids per component; BLOCKING `obeys` ids | step 1–2 |
| 9 | `knowledge/_RUNBOOK-compose-from-canon.md` | whole, 205 lines | the SKILL's "long version" of step 5 |
| 10 | `knowledge/_render/_bento_edit_rails.json` | whole, read as a JSON dump (≈42 KB; numeric-only option lines elided by the filter) | rule 7: dials, defaults, grouping |
| 11 | `knowledge/components/*.meta.json` | **fields only**, by script, never whole files. `when` and `provides` for ~33 metas (list-items, data-grid, table, transaction-row, pagination, tabs, search-field, dropdown, multi-select, combobox, badge, status-indicator, chip, date-picker, segmented-control, button, icon-button, popover, headers, section-heading-lockup, stat-card, kpi-tile, tooltip, empty-state, …). Full `purpose / when / variants / edges / behaviour / antiPatterns / relationships / accessibility / props` (each truncated to ~1.8 KB) for `list-items` and `filter-toolbar-bar`, plus the toolbar's `edges.$contract` and `props[4:]` in full. `edges.groupsWith / mustNotNeighbour / yieldsTo` and `behaviour` (first 260 chars) for 16 metas. `purpose` and `variants` for page-header-lockup, section-heading-lockup, pagination and tabs | step 2–3 contracts |
| 12 | `knowledge/snippets/App-shell-top-nav.reference.html` | whole, 773 lines | shell |
| 13 | `knowledge/canon/canon.css` (1.84 MB) | **targeted reads only** (it is linked, not read). Scope-class inventory (grep); lines 925–960 (base); 1074–1246 (AUTO-BENTO, whole); ~6240–6330 (app-shell-top-nav scope head) plus a grep of its `.sh-*` rules; 1414–1459 (list-items vars); 12236–12250 (toolbar `[hidden]` remedy); 17500–17660 (dashboard-bento scope vars); ~18100–18290 (dashboard-bento placement rules 1–11); greps for console-theme selectors, metric `.board`, chart `figure.dv`, `.dv-empty-frame`, toolbar atoms, `.ftb-msg`, drawer `.sheet`, stat-card, section-heading `.l-stack` | what each scope provides, so nothing is restyled |
| 14 | `knowledge/snippets/Metric.reference.html` | lines 1–123, 124–140, 380–394, 396–725 of 749 (CSS 141–379 not read) | headline metric markup |
| 15 | `knowledge/snippets/Filter-toolbar-bar.reference.html` | lines 1–50 and 410–1091 of 1091 (CSS 51–409 not read) | toolbar markup + script |
| 16 | `knowledge/snippets/List-items.reference.html` | whole, 262 lines | record list |
| 17 | `knowledge/snippets/Table.reference.html` | whole, 258 lines | table view |
| 18 | `knowledge/snippets/Pagination.reference.html` | whole, 174 lines | paging |
| 19 | `knowledge/snippets/Summary.reference.html` | whole, 92 lines | drawer body |
| 20 | `knowledge/snippets/Drawer.reference.html` | whole, 248 lines | detail overlay |
| 21 | `knowledge/snippets/Stat-card.reference.html` | whole, 165 lines | chart-tile carrier |
| 22 | `knowledge/snippets/Section-heading-lockup.reference.html` | lines 155–224 + a structure grep (CSS not read) | group band heading |
| 23 | `knowledge/canon/dv-render.js` | whole, 393 lines | the engine's spec contract (rule 18) |
| 24 | `knowledge/canon/dv-legend.js` | lines 1–60 + a grep of its listeners | legend state model (why the legend host is replaced on re-render) |
| 25 | `knowledge/canon/dv-behaviour.js` | grep of listeners and its load guard only | delegation check |
| 26 | `knowledge/canon/dv-render-bar.js` | grep of the type registrations only | confirms `stacked-column` is registered |
| 27 | `knowledge/snippets/Chart-stacked-area.reference.html` | lines 1–60, 276–390, 1466–1685 of 1684 + a structure grep. **Lines 388–1465 (the dv-behaviour, dv-legend and dv-render AUTO-BEHAVIOUR blocks) were spliced without being read line by line.** dv-render's source was read whole as row 23; dv-behaviour and dv-legend only as rows 24–25 | chart markup + engine |
| 28 | `knowledge/snippets/Chart-bar.reference.html` | lines 595–676 and 1992–2069 of 2069 + a structure grep. **Lines 1824–1992 (dv-render-bar block) spliced without a line-by-line read** | stacked-column markup + bar partial |

## What was copied and what was drawn

**Copied byte-for-byte** (spliced by a scratch assembler that refuses a mismatched boundary or any `APOLLO-DEMO` marker):

| source | lines | bytes | sha256 (first 16) |
|---|---|---|---|
| `Chart-stacked-area.reference.html`: AUTO-BEHAVIOUR dv-behaviour, dv-legend, dv-render, dv-render-stacked-area | 388–1655 | 77,866 | 60e73c349c8abba0 |
| `Chart-bar.reference.html`: AUTO-BEHAVIOUR dv-render-bar | 1824–1992 | 9,694 | dc1fbe7b23f13e6b |
| `Filter-toolbar-bar.reference.html`: Search-field, Dropdown, Segmented-control, Tags scripts | 814–891 | 5,878 | 96641d82b1435577 |
| `App-shell-top-nav.reference.html`: off-canvas nav script (with its `<script>` tags) | 716–770 | 3,486 | 97a4509670615e5c |

**Copied markup.** Structure and classes were taken from the snippet as read. Content, ids and data hooks were changed, and every `APOLLO-DEMO` span was dropped.
- Shell: masthead, nav, crumbs, `sh-main`/`sh-title`, slim footer, scrim, sheet, and the masterbrand `<img>` pair. Changes: the bone placeholders and the profile button were dropped; the logo `src` is re-pathed to `../knowledge/assets/logos/`.
- Toolbar `form.ftb`: search, add-filter, range, view, density, export, and the context row with count, chips and clear. Changes: the option lists are rendered from `DATA` in the snippet's own `optgrp`/`opt` markup; a Sort `.seg` was added in the shape of the snippet's dense "Sort by" seg; the export list is CSV + Excel.
- The toolbar's `.ftb-msg` empty message.
- Metric `.metric` default (label, value, delta, spark), and the `metric-note` empty reading. Rendered by a JS template, in the same markup.
- List-items `ul.list > li > button.row` transaction row: avatar, two-line body, status chip or tag, amount. Rendered by a JS template.
- Table `.wrap > .scroll > table` with caption and sub-caption, `th scope`, `data-label`, `.v` and `.num`.
- Pagination `nav.pg` with `.ctrl` chevrons, numbered links and `.ellipsis`. Rendered by a JS template.
- Drawer `.scrim` + `.sheet` with head, body and foot, and `.dbtn` primary/secondary.
- Summary `dl.summary > .summary__row`.
- Chart `figure.dv`: head, title, controls, CSV button, `details.dv-tbl`, stage, `svg.dv-fit`, legend, live region. Copied from `Chart-stacked-area` csa1 and `Chart-bar` cb5 with the canvas **emptied** (the engine draws it) and the table spine reduced to its caption (the engine writes the rows).
- The chart `dv-empty-frame` empty state.
- Section-heading-lockup arrangement A (`.l-stack[data-gap=xxs] > h2.t-cm-section-label`).
- The Stat-card `.stat-card` surface.
- Legend rows: the snippet's `li.dv-legrow` markup, generated per series.
- Icon `<symbol>` paths, copied from the shell, toolbar and Metric sprites (each already byte-matched to `knowledge/assets/icons/` by its snippet).

**Bento grammar:** SKILL rule 7a's grammar, using classes defined in `canon.css`. No template file was opened or copied.

**Re-drawn: no component.** One piece is generated geometry: the Metric spark polyline and polygon, computed from `DATA` in the snippet's exact 200×48 viewBox scheme (baseline y=45, x from 3 to 197). Metric ships no script, and its spark was static.

**Authored** (rule 2a / s258-D1, reported as `NOTE:AUTHORED-JS`):
- the `DATA` model, built by a seeded generator
- the page wiring: state, URL persistence, filter logic, KPIs, chart specs, list/table/pager rendering, view composition, export, drawer content, approve
- the toolbar driver, extended from the snippet's (the diff is described in the page's `#behaviour-manifest`)
- the Pagination, Drawer and List-items scripts, extended to delegated or rendered forms

**Page CSS:** an empty placement-only `<style>` block. No colour, size, type or `.c-*`/`.cn-*` redefinition. Inline `style` attributes appear only where the snippets themselves use them: the visually-hidden dropdown labels, and the legend swatch `--sc:var(--data-series-N)`.

## Sibling files

None were created. `out/dashboard.html` resolves its stylesheets and logos from the pack itself, by relative path: `../knowledge/canon/canon.css`, `../knowledge/canon/type.css`, `../knowledge/assets/logos/masterbrand-{light,dark}-colour.svg`. It must stay in `out/` inside the pack. Moved elsewhere, those four paths break.
