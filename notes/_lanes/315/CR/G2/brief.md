# Grill brief — corporate international banking dashboard

Date: 2026-10-02
Task: A financial dashboard for corporate international banking (a treasurer's view of a multi-entity, multi-currency group), with every interactive element working: filtering and navigation above all.
Lane: **on-canon** (`skills/generate-from-canon/SKILL.md`, invoked as `/generate-from-canon` → `.github/prompts/generate-from-canon.prompt.md`).

> This brief lives at `out/brief.md` because the session asked for every output to go in `out/`. The grill skill's own home for it is `briefs/2026-10-02-treasury-dashboard-grill.md`. That folder was not created, so the next session's grill will fire again unless this file is copied there.

| # | question | answer |
|---|---|---|
| 1 | Theme | **Console**: answered by the designer. Console is the one theme with rounded corners on controls and surfaces. |
| 2 | Light, dark or both | *skipped (full skip called after Q1) → default: **both*** (the question's stated usual answer). The page follows the OS setting, `?mode=light\|dark` overrides it, and the override is remembered. |
| 3 | Density and width | *skipped → fallback: **comfortable, wide desktop** (≈1280–1440px).* The bento bands still re-pack at 1100 / 820 / 520px container width, and the shell collapses at 900 / 600. |
| 4 | Brand assets | *skipped → default: **the HSBC masterbrand** on the masthead* (`masterbrand-light-colour.svg` / `masterbrand-dark-colour.svg`, rule 8a). No photography, no other brand colour, no product name supplied. |
| 5 | Data | *skipped → fallback: **placeholder, generated rich and deep**.* One `DATA` object holds 5 currencies with fixed USD rates; 5 legal entities of a fictional "Halden Group" (UK, Germany, US, Hong Kong, Singapore); 11 accounts; 12 month-end balances per account; 24 named beneficiaries in 11 countries; 12 payment rails; and roughly 400 payments over 180 days (2–4 per weekday, occasionally one at a weekend; the exact count is whatever the seeded generator yields, and the page reports it) with statuses, value dates, settlement times and rejection reasons. It is seeded, so it is identical on every load. |
| 6 | Fixed and off-limits | *skipped → fallback: **nothing extra fixed**.* The design contract's five rules apply as standing defaults: invent nothing, copy markup, theme asked, bento-first, check before showing. The accessibility floor is what the parts carry (WCAG 2.2 AA targets, 44px hit areas, reduced motion). |

Skipped: 2, 3, 4, 5, 6 (full skip called after question 1). Discovery: **not run**. The full skip ends questioning, so the build's own judgement calls are listed under "Decisions" below, each marked as mine.
Defaults used: Q2 → both modes · Q3 → comfortable, wide desktop · Q4 → masterbrand · Q5 → generated placeholder data · Q6 → none beyond the contract.
Bento check ("dashboard bento — is that right?"): *skipped → counts as yes* (rule 7a). The page is laid out on canon's bento grammar.

Notes: the designer's own words were "build me a financial dashboard for corporate international banking. Please make the all the interactive elements work such as filtering and navigation."

---

## Decisions (mine, because discovery did not run). Each one should go back to the designer.

1. **Who the page is for:** a group treasurer at a multi-entity corporate client. The questions it answers are below.
2. **How many groups, and what is in each:** four. Group count is the designer's product decision (rule 7b). I made it here, and it is on the Gaps list.
3. **Navigation:** three views, Overview, Liquidity and Payments. Each composes the wall from the same groups.
4. **Currency of record:** USD equivalent at fixed rates. Payment rows also show their own currency and amount.

## Used / missing note

**Seed commands run (step 1):**
```
python3 knowledge/_compose_slice.py "Financial dashboard for corporate international banking: an app shell with navigation, KPI figures, cash positions by currency and entity over time, a filterable sortable paged list of international payments, and filters by entity, currency and status." --out seed.json --explain
python3 knowledge/_compose_slice.py "A list of international payments that the treasurer filters by entity, currency and status from a toolbar, searches, sorts and pages; each row shows a monetary amount and a payment status." --roles record-list,input,wayfinding,status-surface --out seed-panel-list.json --explain
python3 knowledge/_compose_slice.py --ask "which components answer filter?"        # REFUSED: no node (named obstacle)
python3 knowledge/_compose_slice.py --ask "what governs component:<x>?"   # for filter-toolbar-bar, pagination, table, section-heading-lockup, stat-card
```
Seed 1 returned 26 components, 62 governing rulings, 80 obeys (49 BLOCKING), 30 mustNot rows (24 `ref:null`) and 12 unresolved items. The seed files were written to the session scratchpad; they are not part of the deliverable.

**Decision table (step 2):** question → role → component → the `when` clause that is true for this data → rulings that govern it.

| # | question the screen must answer | role | component chosen | `when` true for this data | governing rulings |
|---|---|---|---|---|---|
| 0 | Where am I, and how do I move between views? | page-frame | `app-shell-top-nav` (form inline) | "primaryNavigation = present AND platform = app — THE DEFAULT FRAME FOR AN APPLICATION" | s313-D22, s313-D24, s272-D70, s272-D72, s230-D2 |
| 0a | Which part of the bank am I in? | wayfinding | `breadcrumbs` (inside the shell, as the shell copies it) | "shape = ancestor-path × links AND depth >= 2" (Home / Corporate banking / view) | s305-D60, s272-D68, s272-D72 |
| 0b | Where does the page end? | — (footer) | `footer` slim legal bar (inside the shell) | "platform = app — every app page shell ends in the app footer" | s305-D60, s272-D58, s263-D7, s263-D12, s261-D3, s261-D8 |
| 1 | Where does the group stand right now? | headline-metric | `metric` ×4 (default size with the trend slot) | "shape = one-measure × value-and-delta AND delta != none"; trend slot because a series exists (s247-D3) | s314-D28, s314-D18, s313-D6, s313-D52, s310-D1, s310-D2, s309-D3, s309-D5, s309-D6 |
| 2 | How is liquidity moving, and in which currencies? | chart | `chart-stacked-area` | "answers spans change-over-time AND composition AND cumulative bands share ONE total": the group total is meaningful. Beats `chart-line` on the most-claims test (b). | ds-026 (+ obeys dv-004, dv-016, dv-017, dv-line-011) |
| 3 | Which entities are paying out, in which currencies? | chart | `chart-bar`, stacked-column type | "answers = comparison AND axis.x = categorical … the stacked variant takes composition across categories" | s305-D60, s277-D1, s277-D3, s276-D5, s249-D4, s248-D2, s245-D7, s218-D5, s184-D3, s116-D2 |
| 4 | Which payments are moving, and which need me? | record-list | `list-items` (transaction rows) | "records >= 2 AND the records are the same kind, each read ACROSS its own row … AND needs in (none, sort, filter)" | s313-D27, s274-D1…D6, s273-D3, s160-D2 |
| 4a | …and when I need to read amounts down a column? | record-list | `table` (passive), behind the toolbar's view switch | `table` has no authored `when` (null). Chosen because list-items' own `when` says "if a field must be read DOWN a column across records, it is a table". | s313-D4, s313-D50 |
| 5 | How do I narrow everything to what I care about? | input (driver) | `filter-toolbar-bar`, arrangement dashboard | "records >= 2 AND needs in (filter, sort) — one row of controls that drives the record-list and the panels beside it" | s305-D60, s272-D76 |
| 6 | How do I get through 100+ rows? | wayfinding | `pagination` (basic) | `when` null. It is the only paging part in the role, so this is a judgement call. | s313-D15 |
| 7 | What exactly is this payment, and can I act on it? | overlay | `drawer` + `summary` body | drawer `when` null; summary "shape = rows × name-value-pairs AND rows >= 2" | drawer s313-D20, s272-D4, s272-D52, s272-D53, ds-032 · summary s314-D10, s314-D28, s305-D60, s246-D4 |
| 8 | What is each group about? | page-title (section) | `section-heading-lockup` arrangement A, as the group band | `when` null. s313-D29 rules "B, a band inside the group" as the default group header. | s313-D29, s272-D60 |
| 9 | What surface does a chart tile sit on? | (carrier) | `stat-card` surface, holding the chart | none. s245-D7's ruled group note describes "a Stat-card carrying Chart-bar's column specimen". | s309-D3 (moves stat-card pages to Metric; **in tension**, see Gaps) |

**Theme:** `data-apollo-theme="console"` on `<html>`, plus `class="canon"` and `data-theme`. Cited from this brief, Q1.

**Tokens:** none are bound by the page itself. Every value resolves inside the copied parts' `.cn-*` scopes in `knowledge/canon/canon.css`. Chart fills are the engine's `var(--data-series-1…5)`; deltas use the Metric's ink seats.

**Layout:** canon bento grammar (rule 7a). The wall is `.c-bento.tpl-wall[data-bento-role=dashboard]` inside `.cn-template-dashboard-bento`, holding four `.tpl-group` sections with role words lead / evidence / evidence / context. Spans come from the rails vocabulary (`data-c` 1/3/6 on a 6-column wall; the lead group is pinned at four across). Gutters, radius and grounds are the scope's defaults: main 40px and sub 4px for Console, as the rails' `mainSpacing`/`subSpacing` defaults say. The page never sets them.

**Missing:** see `out/GAPS.md`.
