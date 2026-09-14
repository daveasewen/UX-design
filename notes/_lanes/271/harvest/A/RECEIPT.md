# #271 HARVEST LANE A — RECEIPT

**Slice A — input + action + feedback + overlay.** Read-only on canon: nothing under `knowledge/` was opened for writing, no meta, schema, roles.json, rules index, runbook or gate was touched. All four outputs live under `notes/_lanes/271/harvest/A/`.

## Counts

| | |
|---|---|
| Components in the slice (brief) | **50** |
| Components covered | **50** (45 new predicates + 5 referenced from #270, not redone) |
| Components skipped | **0** |
| Rules found (proposed `when` predicates) | **45** |
| — unanimous, by the review page's test (`disagreements` opens with the word *none*) | **5** — input-fields, textarea, icon-button, alert, popover |
| — expected silence, stated separately so nothing hides inside "unanimous" | **9** — amount-input, date-range-picker, tags-input, split-button, quick-actions, cta-lockup, countdown-timer, modal-lightbox, command-palette |
| — non-unanimous (a decision-table row) | **30** rows, naming 36 distinct components, touching 33 of the 45 proposals |
| — `confidence: none` (no external support at all) | **8** |
| Confidence spread | canon 4 · consensus-external 22 · single-external 11 · none 8 |
| Longest quote | **14 words** (RUNBOOK cap: < 15) — 22 quotes were re-cut from the live pages on 2026-09-14; see the Recount section below and `../VERIFY.md` § REPAIR |
| Our own sources recorded (`ours`) | **47** |
| External verbatim quotes recorded (`external`) | **264** |
| Distinct components an external quote attaches to | **40** |
| External findings with `component: null` (they ship it, we don't) | **3** |
| Fetch failures / declared workarounds (`refused`) | **11** |
| Decision-table rows (non-unanimous only) | **30** |

**These measures are not a partition and must not be added up.** Proposals are per-COMPONENT; decision-table rows are per-RULE, and one row can name several components while one component can appear in several rows. The earlier version of this receipt printed "unanimous 15" as `45 − 30`, which silently treated the two axes as commensurable. The number above is the review page's own test instead — the proposal's `disagreements` field opening with the word *none* — which is what section 3 of the page bulk-accepts. Recount with `python3 notes/_lanes/271/harvest/_recount.py A`.

## Systems consulted

All eleven named in the brief, in order, all of them spoke:

GOV.UK 25 · USWDS 14 · Material 3 25 · IBM Carbon 32 · Shopify Polaris 20 · Adobe Spectrum 20 · Atlassian 34 · Ant Design 27 · Fluent 2 27 · Apple HIG 14 · NN/g 26.

## Fetch failures, named

Five systems do not serve their guidance as HTML to a plain fetch. Each workaround is declared in `SOURCES.json.refused`, never laundered:

1. **Material 3** — every `/components/*/guidelines` page returns a JavaScript shell (14 bytes of text). Harvested through a JS-rendering fetch.
2. **Adobe Spectrum** — Next.js RSC payload, not server-rendered. Text recovered from the embedded `__next_f` flight payload. **Three pages returned an empty payload and yielded nothing**: `/page/dialog/`, `/page/date-picker/`, `/page/illustrated-message/`. Spectrum's dialog and date-picker positions are therefore NOT OBTAINED, not silent.
3. **Atlassian** — SPA shell only (3.4 KB) on a plain fetch; the Gatsby `page-data.json` endpoints 404. Harvested through a JS-rendering fetch.
4. **Shopify Polaris** — `polaris.shopify.com/components/*` still 301s to shopify.dev, which carries no usage prose (identical to the #270 finding). Quotes taken from the Polaris repo `.mdx` source and marked `note` per entry.
5. **Carbon** — `/components/skeleton/usage/` and `/components/combo-button/usage/` are 404. Carbon has no standalone skeleton page (its guidance lives in `/patterns/loading-pattern/`, harvested) and **no split-button at all** — recorded as measured silence.
6. **NN/g** — four article slugs 404'd. Two were recovered under other slugs (`/articles/sliders-knobs/`, `/articles/button-states-communicate-interaction/`). Two were not: **NN/g's link-vs-button position and NN/g's empty-state position were NOT OBTAINED.** That matters for row R-A-02, where NN/g would have been a sixth voice.
7. **USWDS alert** — the page's "When to use" body did not survive extraction as a quotable sentence. USWDS's alert-vs-banner position is NOT OBTAINED, not silent.
8. **Figma (HSBC Common Toolkit)** — no access today, carried forward from #270. The HSBC component-choice prose is almost certainly there and is not in our ingested corpus. This is why the lane exists.

## Declared gaps

- **Not a fetch failure, but worth naming:** GOV.UK has **no analogue at all** for eleven slice-A components — slider, toast, drawer, popover, command-palette, tags-input, transfer-list, cascader, rating, fab, split-button. Recorded as measured silence, not as a gap in the harvest.
- **Eight predicates have `confidence: none`** — date-range-picker, tags-input, secure-entry, quick-actions, cta-lockup, countdown-timer, modal-lightbox, command-palette. Eight names for the count eight. (`amount-input` was listed here in the first version of this receipt and is **not** one of them: its `confidence` is `single-external`. Corrected 2026-09-14.) For four of them the silence is *expected* (domain components: date-range-picker, modal-lightbox, cta-lockup, countdown-timer). For three it is a genuine gap where an external system might have helped and none does: **tags-input, quick-actions, command-palette**. `secure-entry` is the eighth and is neither: USWDS contradicts our form directly, so the `none` there is a conflict, not an absence.
- **Two internal defects surfaced, not resolved** (both are decision-table rows, neither is mine to rule): our Drawer and our Modals "Partial modal" describe one surface under two names (R-A-24); our Search-field and our Combobox describe one widget under two names (R-A-27).
- **`notifications` has no proposed `when`** by design — it is the Legacy umbrella over Alert / Banner / Toast / inline validation. Proposing a predicate would open a fifth door into four rooms. R-A-30 asks what to do with the record instead.
- **No atom was invented.** Every `component` value in `PROPOSED-WHEN.json` and every non-null `component` in `SOURCES.json` is an existing meta stem under `knowledge/components/`. Three external findings carry `component: null` — GOV.UK warning-text, GOV.UK inset-text, and the onboarding spotlight/tour that Atlassian, Ant and Carbon all ship and we do not. Findings, not proposals.

## Already-ruled, cited not re-litigated

- `s270-D1` — single-select cut-off 5 (radio ≤ 4, dropdown ≥ 5, provisional). Cited as `canon`; not reopened.
- `s252-D1` — `roles.json` action-role whens (button / icon-button / split-button / links). Four predicates in this lane are copies, not inventions.
- `s210-D5` — Progress-bar is the progress reading of the one Meter molecule; its record exists for findability.
- `s201-D2` — the 44px floor. Apple HIG's 44pt quote is recorded as corroboration only; the rule is already ours and was not re-asked.
- #270's five selection-family proposals are referenced under `$already_done` and extended only where search-field, tags-input and transfer-list collide with them.

## Recount — 2026-09-14

Every number above re-derived from this slice's three JSONs by script, so the receipt states what the JSONs carry and not what the lane remembered.

```
$ python3 notes/_lanes/271/harvest/_recount.py A
SLICE A
  SOURCES     ours 47 · external 264 · refused 11
  quotes      longest 14 words · at-or-over the <15 cap: 0
  proposals   45
  confidence  canon 4 · consensus-external 22 · single-external 11 · none 8
  unanimous   5  (page test: `disagreements` opens with "none") -> input-fields, textarea, icon-button, alert, popover
  expected silence recorded in `disagreements`: 9 -> amount-input, date-range-picker, tags-input, split-button, quick-actions, cta-lockup, countdown-timer, modal-lightbox, command-palette
  decision rows 30 · distinct components named by a row 36 · proposals a row touches 33
  rows flagged kind=internal: 0 -> 
  system-disagreement rows: 30
  proposals citing NO external system in `sources`: 5
  component values that are not an existing meta stem: 0
  external findings with component: null: 3
```
