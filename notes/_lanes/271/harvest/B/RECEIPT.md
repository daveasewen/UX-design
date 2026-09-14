# #271 HARVEST LANE B — RECEIPT

**Slice B** — record-list + chart-panel + headline-metric + status-surface.
Date 2026-09-14 · session 271 · READ-ONLY on `knowledge/` (nothing under it was opened for writing).

## Counts

| Count | Value |
|---|---|
| Components in the slice | 45 |
| **Components covered** | **45 / 45 — no component skipped** |
| Our own sources cited (`ours`) | 16 |
| **External rules found (verbatim quotes)** | **113** |
| Distinct external systems that SPOKE | 9 |
| Longest quote | 14 words (RUNBOOK cap: < 15) |
| Proposals written | 45 |
| — confidence `canon` | 29 |
| — confidence `consensus-external` | 8 |
| — confidence `single-external` | 2 |
| — confidence `none` | 6 |
| **Unanimous** — the review page's test: the proposal's `disagreements` opens with the word *none* | **6** (timeline, view-options, Chart-boxplot, Chart-candlestick, Chart-histogram, limits-meter) |
| **Non-unanimous** (a real fork for Dave) = the decision-table rows | **24** |
| **No external system cited in `sources` at all** | **15** (domain components + our own lock-up layer; silence expected, not a gap). Distinct from `confidence: none`, which is **6** — the word *none* was doing two jobs in the first version of this receipt and is no longer allowed to |
| Decision-table rows | **24** (**21** system disagreements + **3** internal, flagged `kind: internal`: B-17, B-23, B-24) |
| Findings with `component: null` (they have it, we don't) | 6 |

**These measures are not a partition and must not be added up.** Proposals are per-COMPONENT; decision-table rows are per-RULE. The three highlighted numbers overlap — `view-options` and `limits-meter` are both "unanimous" and among the 15 with no external system cited. Recount with `python3 notes/_lanes/271/harvest/_recount.py B`.

## Systems consulted — SPOKE (9)

GOV.UK · USWDS · IBM Carbon · Shopify Polaris (repo source) · Adobe Spectrum (react-spectrum docs) · Ant Design (repo source) · NN/g · Datawrapper · FT Visual Vocabulary

Two chart-specific systems were added for this slice per the brief: **Datawrapper** and the **FT Visual Vocabulary**. The FT's full `chartTypes.csv` (74 chart types, 9 intent categories) was retrieved and is the single richest chart-choice source in the record.

## Fetch failures — named, never guessed

| Source | What happened |
|---|---|
| **Material 3** (`m3.material.io` cards / carousel / badges / progress-indicators) | HTTP 200, client-rendered, **zero** text extracted. M3 is UNREACHABLE here, not silent. |
| **Apple HIG** (charts / gauges / progress-indicators / lists-and-tables) | HTTP 200, client-rendered, zero text extracted. |
| **Atlassian** (lozenge / badge / tag / avatar / avatar-group / pagination / progress-bar) | HTTP 200 but only cookie + feedback chrome renders server-side. **This is why `avatar-group` is recorded as UNMEASURED silence, not absent guidance.** |
| **Adobe Spectrum** (`spectrum.adobe.com/page/*`) | zero bytes of extractable text → **SUBSTITUTED** with `react-spectrum.adobe.com` component docs, which carry the same guidance prose. Declared in `refused`, not laundered. |
| **IBM Carbon data-viz** (`/data-visualization/chart-types/`) | client-rendered → fell back to the carbon-website repo `.mdx`, which is a **taxonomy only** (Comparisons · Trends · Part-to-whole · Correlations · Connections · Geospatial) with no per-chart prose. `src/data/data-visualization.js` = 404. **Carbon's chart-CHOICE prose is missing from this record.** |
| **Fluent 2** | serves a "page may no longer be available" shell + "Microsoft employee? Sign in to see internal-only content." UNREACHABLE. |
| **NN/g `/articles/pie-charts/`** | 404 → position taken instead from `/articles/dashboards-preattentive/`, which states it directly. |
| **Datawrapper bar + scatter guides** | 11 slug guesses probed, all 404. Datawrapper is therefore **genuinely silent here on bar and scatter** in this record. |
| **USWDS pagination** | fetched fine; the page carries **no** when-to-use section. Measured silence, not a failure. |
| **Figma (HSBC Common Toolkit)** | no access — carried forward from #270. Every `ours` entry is repo prose, **not HSBC guidance**. |

## Declared gaps

1. **No component was skipped.** Depth was traded for coverage as instructed.
2. **Carbon's chart guidance is the one real hole.** It is the system whose data-viz opinion would have carried most weight for our fintech charts, and its per-chart prose was unreachable by three routes.
3. **`avatar-group` and `avatar` are under-sourced** because Atlassian (which ships published guidance for both) would not render. Their `none` / `single-external` confidence is a *fetch* artefact.
4. **Three** rows in the decision table (**B-17 summary role/meta mismatch**, **B-23 view-options superseded**, **B-24 alias metas and a when-gate**) are **internal** findings, not system disagreements. They are in the table because all three are ruling-shaped and B-24 bites *before* any `when` lands as a gated field. B-24's `component` field carries the single stem `limits-meter` (corrected 2026-09-14 from the comma-joined `"limits-meter, progress-bar"`, which was not a stem); `progress-bar` is the same kind of alias and is carried on the row as a `note`, since it is slice A's component.
5. **One internal inconsistency found and not fixed** (read-only lane): `roles.json` says chart-pie is `≤ 5 parts`; both `chart-pie` and `chart-donut` antiPatterns say `More than 6 slices`. Row **B-04**.
6. **One role/meta mismatch found and not fixed**: `roles.json` describes `summary` as a count board; `summary.meta.json` describes a payment-review receipt. Row **B-17**.

## What this lane did NOT do

- Did not re-litigate `s270-D1` (single-select cut-off 5). Cited as `canon` where it bears.
- Did not redo record-list `when`s — they are adopted `s252-D1` in `knowledge/roles.json` and were **cited**, and #270's table / data-grid / list-items proposals were **referenced and extended**, not rewritten.
- Did not invent an atom. Every `component` value is an existing meta stem; six external findings carry `component: null` (USWDS `collection`, treemap, sankey, waterfall, lollipop, Carbon's intent taxonomy).
- Did not touch `knowledge/`.

## Recount — 2026-09-14

Every number above re-derived from this slice's three JSONs by script, so the receipt states what the JSONs carry and not what the lane remembered.

```
$ python3 notes/_lanes/271/harvest/_recount.py B
SLICE B
  SOURCES     ours 16 · external 113 · refused 12
  quotes      longest 14 words · at-or-over the <15 cap: 0
  proposals   45
  confidence  canon 29 · consensus-external 8 · single-external 2 · none 6
  unanimous   6  (page test: `disagreements` opens with "none") -> timeline, view-options, Chart-boxplot, Chart-candlestick, Chart-histogram, limits-meter
  expected silence recorded in `disagreements`: 17 -> document-row, transaction-row, standing-order-mandate-row, account-card, carousel, filter-toolbar-bar, chart-sparkline, Chart-bullet, Chart-butterfly-v, kpi-tile, runway-bar, amount-display, stats-band-lockup, avatar, avatar-group, payment-card-visual, qr-code
  decision rows 24 · distinct components named by a row 22 · proposals a row touches 22
  rows flagged kind=internal: 3 -> B-17, B-23, B-24
  system-disagreement rows: 21
  proposals citing NO external system in `sources`: 15
  component values that are not an existing meta stem: 0
  external findings with component: null: 6
```
