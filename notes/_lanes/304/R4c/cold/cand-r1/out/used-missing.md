# Used / missing — CEO international-banking prototype (cand-r1)

Lane: **on-canon** (Apollo Spider v1.0.14 candidate, skills in `pack/skills/`). Brief: `briefs/2026-09-26-ceo-banking-grill.md`. Theme Common, light + dark.

**Seed:** `python3 knowledge/_compose_slice.py "<brief>" --out seed.json --explain` → `proof/seed/seed.json` (17 components, 49 governing rulings, 68 obeys). Charts beyond the seed's `change-over-time` intent were chosen from `showroom/index.json` and each chart meta.

## Decision table (question → role → part → why)

| question | role | part (snippet) | why |
|---|---|---|---|
| Where am I / where can I go? | page-frame | App-shell-side-nav (its own nav, app bar, crumbs, footer) | desktop app frame with persistent vertical nav; masterbrand already bound |
| What is this page? | page-title | Page-header-lockup `.ph` | title + eyebrow + tertiary/primary actions |
| Narrow everything at once | filter | Filter-toolbar-bar `#ftbA` + its script (extended) | the bar that drives a consumer by `apollo:filter-change` |
| Can we fund our plans? | headline-metric | Kpi-tile `.as-link` ×4 per lead row | a series exists (kpi-tile `when` beats stat-card); canon's lead row is four |
| Change over time | chart-panel | Chart-line (line, multiline), Chart-stacked-area, Chart-combo (two units), Chart-candlestick (OHLC), Chart-sparkline | chart metas' `answers` |
| Compare across entities / regions / currencies | chart-panel | Chart-bar (column, bar, grouped, stacked), Chart-butterfly-h, Chart-scatter, Chart-boxplot, Chart-histogram | categorical comparison, two-measure mirror, relationship, distribution |
| Share of a whole (≤5 parts) | chart-panel | Chart-donut, Chart-pie | composition; top 4 + Other keeps dv-pie-009 |
| Against a target or cap | chart-panel / meter | Chart-bullet, Limits-meter | "a target is the point" (kpi-tile yields to bullet); allowance reading |
| What needs my attention? | arrangement | Cards `.card.action` + Links + Status-indicator chips | summary with actions that open the record |
| Records read down columns | record-list | Table + Pagination + Dropdown (sort) | "if a field must be read DOWN a column, it is a table" (list-items `when`) |
| Records as cards | record-list | List-items `.list` | the filter bar's Table/Cards view switch |
| The transaction ledger | record-list | Data-grid `#dg` + its script (extended one line) | sort, column filters, selection, paging, edit-in-place |
| Look at one record | overlay | Drawer (detail, task) + Summary + Timeline | read-mostly inspection and short tasks keep context |
| A blocking decision | overlay | Modals `.overlay` + Textarea `#t1` | approvals, rejections, acknowledgements need a decision and a note |
| Tell me it worked | feedback | Toast, Alert, Empty-state | confirmations, breach callout, no-results |
| Preferences | input | Segmented-control, Selection-controls (switch), Dropdown | theme / records view, notifications, landing view |

## Tokens and grammar
Grounds `--surface-subtle` (rails `bentoBg: grey`) with the dark leg transparent; spacing through `--padding-fixed-medium` (16) and `--gap-fixed-subsection-xsmall` (24); bento grammar `cn-template-dashboard-bento` › `.tpl-page` › `.c-bento.tpl-wall` › `.tpl-group-lead|evidence|context` › tiles at `data-c` 1 (lead row), 3 and 6 only.

## Missing / gaps
See `RUN-REPORT.md` → Gaps.
