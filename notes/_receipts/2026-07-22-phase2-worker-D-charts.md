# Receipt — Phase-2 wave 2, WORKER D: Charts / data-viz kit lane (itinerary row 53)

*2026-07-22 evening BST (date from `date`). Brief: `notes/_briefs/2026-07-22-phase2-worker-D-brief.md`.
Role from Dave's opener line. NO commits made — git untouched; files + this receipt only.*

## Landed — 4/4 worklist items, NO cut line

| # | Snippet | Meta | Figures |
|---|---|---|---|
| 1 | `snippets/Chart-bar.reference.html` | `components/chart-bar.meta.json` | column categorical · horizontal bar · status ramp · no-data |
| 2 | `snippets/Chart-line.reference.html` | `components/chart-line.meta.json` | single series · 3-series multi (shapes+letters+legend) · no-data |
| 3 | `snippets/Chart-donut.reference.html` | `components/chart-donut.meta.json` | spider letters + legend · direct labels · no-data |
| 4 | `snippets/Chart-sparkline.reference.html` | `components/chart-sparkline.meta.json` | standalone (+table) · inline 44px (KPI scale) · no-data |

**Shape call (justified per brief):** one snippet PER CHART TYPE, not one Charts-kit file. DV-D01's
consolidate-to-one-file governs the pro-forma REVIEW kit; canon's grain is per-component (showroom
pages, metas, categories are all per-component — Stat-card/Table precedent).

**⚠ EVERYTHING here is PROVISIONAL-AGENT** — the kit is PARKED (9 rounds, "good enough", NOT signed
off; open-014). Each snippet head-comment + manifest `$note` says so. Dave's dataviz sign-off flips it.

## Verification (all in-session; authoritative serial build = conductor's)

- **DataViz gate: 8/8 figures, 0 BLOCKING / 0 ADVISORY** — run by IMPORT (the gate's own
  `theme_vars`/`check_chart` executed against my files; discovery glob doesn't reach snippets — see
  gate-wiring proposal below). Pro-forma kit untouched + its gate run still passes.
- Wired gates green over the tree incl. my files: icons (svgs declared `data-bespoke`) · grid ·
  snippets · a11y · no-hardcode · descender-clip · legacy-leak.
- `gen_snippet_tokens --check`: **0 drift** (1962 bindings, 64 snippets) — every theme-block literal
  matches the resolved store.
- `_validate_partials`: **0 strict, census 32→32** — zero press-shaped growth (hover = filter, not
  transform; no pressables promoted).
- `_validate_radius`: 0 fails (role tokens from birth; nothing radius-bearing beyond the empty-frame).
- `gen_canon_components` regenerated (64 components — my 4 self-healed in, incl. the 14→16px fix);
  `gen_showroom` 64 pages + index.
- **Contrast (computed, both modes vs page):** series/1–5 = 5.26/3.31 · 5.04/3.46 · 4.61/3.78 ·
  4.36/4.00 · 3.52/4.95. Status: error 6.02/3.66 · warning 3.02/5.76 (graphic-grade by design,
  R-D3 — note the light-mode 3.02 is the floor with no margin) · success 5.00/4.80 · info 5.03/3.82.
  Axis effective (ink@.6) 4.54/6.90; grid effective (ink@alpha) 1.23/1.65 (advisory-class, matches
  the kit's reviewed quietness).
- **NOT runnable here:** full `_build_all.py` (see environment note) and `_validate_state_contrast`
  (playwright absent — the known project-wide render-verify refusal). Render-verify remains OWED
  project-wide; nothing new.

## Promoted (OBSERVED, kit-verbatim) vs newly judged (my calls — each receipted in the file heads)

**OBSERVED:** 580×260 frame + 46/568/14/230 plot; bar w48.7 / row pitch 36 / h20.2; line stroke 2.5,
pathLength=2400 (Batch 9), draw 2400ms bezier(.33,0,.3,1) (Batch 6), Batch-8 EASED marker cadence
(0·369·507·…·2400ms) lifted verbatim; marker shapes circle r4.2 / square 8.4 / diamond ±4.9
(dv-line-002); donut ro100/ri60 arcs + 2px page strokes + spider/direct annos + vert legend; spark
580×90→340×64 + inline 200×48@44; grow 760ms + 45ms stagger; hover brightness 1.12/1.22; series =
`data/series/1–5`; letters A/B/C repeated in legends (§04.3).

**JUDGED (all flagged for Dave, retro-propagate as token/CSS edits):**
1. **Axis/label/grid inks:** kit's `#545454/#9B9B9B/#EDEDED/#3A3A3A` have NO post-R-D16 semantic
   home → axis/labels = ink @.6 (house treatment), gridlines = ink @ per-mode alpha `.10/.16`
   (reproduces the reviewed quiet grid). Alternative considered + rejected: `divider/border/break`
   (dark #808080 = loud grid, halation-hostile). **Token gap receipted below.**
2. **Table affordance = native `<details>`** — the kit's drawer overlay + toolbar are JS Layer-2.
   Zero-JS equivalent affordance ("View as table" summary). NOT registered as a pressable (native
   disclosure, not a button atom).
3. **dv-014 correction:** kit's horizontal bar painted the SAME data (spend by category) in
   `series-3` while the column used `series-1` — journey-consistency violation kit-side; both mine
   bind series-1.
4. **Status bars = direct-labelled** (`data-labelling="direct"`): 4 distinct rag fills would trip
   the §04.3 letters advisory as "4 series"; each bar IS directly labelled by its status word —
   semantically true, colour never alone (R-D6 A′).
5. **Markers = the kit's BACKGROUND mode** (series fill + page stroke @2.5): the White/Background
   toggle comparison is UNRESOLVED kit-side; background is theme-adaptive + adds no absolute white
   on dark (halation-aware). **Open for Dave** — flipping = a CSS pair swap.
6. **Donut letters-ON-segments variant HELD BACK:** its letters are `#FFFFFF` on series fills —
   collides with type26-013 white-type-red-only (BLOCKING). Spider + direct (both ink) promoted;
   Dave's Batch-2 #7 three-way comparison stays open, now with this constraint named.
7. **Grid-gate bite on resurrection (stepper precedent):** kit legend margin 14px → 16px.
8. **Type promotions per DV-D05:** kit 11px axis text → `.t-cm-legal` (12, the KB step); donut
   centre 22px → `.t-cm-figure-3` (24/500); direct-label value line weight **600 → 500** (no 600
   on brand).
9. **DV-D02 static answer:** fixed geometry + `.dv-stage` horizontal scroll (text NEVER scales);
   the kit's runtime `fit()` relayout is JS Layer-2. Spark keeps `preserveAspectRatio:none` —
   no text in a spark, so the rule is vacuously held (kit's own exception).
10. **Donut entry motion NOT promoted:** the radial sweep + label sequencing are rAF JS ("no CSS
    transform here" — kit's own comment). Specimens bake visible arcs (the kit's no-JS state).
    Bar grow / line draw / marker fade ARE promoted (pure CSS, DEF-003).
11. **No progress-ring variant:** the kit has none — nothing invented (loader atom stays queued
    §C·4b, untouched).

## `$members` JSON — NONE (deliberate)

Zero pressables promoted: the kit's legend series-toggles, tooltips, table-drawer and Replay-chrome
are Layer-2 JS. Legends are static lists; charts are passive figures. **No button-family membership,
no `--spring`/`--press`, no partials markers.** (Snippet demo chrome keeps the Stat-card-style
themeToggle/Replay buttons only.)

## MIGRATED_SNIPPETS basenames (conductor, radius strict-list)

`Chart-bar` · `Chart-line` · `Chart-donut` · `Chart-sparkline`

## Category proposal (conductor; gen_showroom untouched by me)

New **"Charts"** bucket: Chart-bar · Chart-line · Chart-donut · Chart-sparkline. If B-Q7's
Data-display split lands, Stat-card/Amount-display sit beside (not inside) Charts.

## ★ Gate-wiring proposal (conductor serial — the "new surface never ships ungated" rule)

`_validate_dataviz.py` discovers `_proforma/*.html` only — chart snippets are an UNGATED dataviz
surface until its discovery also globs `snippets/Chart-*.reference.html` (files carry the full DOM
contract + the APOLLO-DATAVIZ… actually the SIGNATURE string is absent from my snippets — add the
signature match OR glob by filename; either is one line in `find files`). My files verified against
the gate's own functions by import (results above), so the flip should land green. **Recommend it
rides the wave commit.**

## Token gaps (promotion = Dave's; none block the snippets)

1. **R-D9 status-ramp values not in the store:** resolved ramp greens/blues (`#36A467`/`#527EBE`)
   await the v8 pin + promotion; status bars bind existing `rag/*` meanwhile (amber = graphic-grade
   `#C58900` per R-D3). Retro-propagates as a token edit.
2. **Quiet chart inks:** no `data/axis` / `data/grid` roles (post-R-D16 the kit's greys are
   homeless). My ink+alpha judgment stands in; if Dave wants tokens, mint `data/axis` + `data/grid`
   per mode and rebind.
3. **Delta seam (flag, no action):** chart-side `data/delta/gain·loss` (#16864E/#1AA05C ·
   #B92F1E/#CC4333) vs Stat-card's R-D5 `rag/success·error` arrows — two live delta conventions
   in canon. Reconcile question for the dataviz sign-off (D2 value-split was ruled for the
   vibrating-boundaries legs; Stat-card receipted rag pairs).
4. **Motion tokens:** chart curves/durations (`--grow` 760 · `--draw` 1000 · `--draw-slow` 2400)
   are local reviewed values — candidates for the queued composite-motion-tokens enact item (§C·4).

## Icon gaps

None — charts are icon-free this pass (chart canvases declared `data-bespoke`; empty states are
text-carried per the Empty-state pattern; the spot-illustration set remains wave-1's logged gap).

## Composition seam (brief-required): Sparkline ↔ Stat-card

The kit composes the inline spark inside its KPI tile. Canon's Stat-card (wave 1) is a PASSIVE atom
with no spark slot — I did NOT re-type the tile to demo it (never re-type a sub-atom). The inline-
scale specimen is the spark half of the seam; **adding a `spark` slot to Stat-card = a Stat-card
variant decision for Dave/conductor** (pairs with B's linked-tile question B-Q6).

## Open questions for Dave (rule by number)

1. **D-Q1 marker fill:** Background (promoted default) vs White — the kit toggle he never ruled on.
2. **D-Q2 donut labelling pick:** spider vs direct as canon default; letters-on-segments needs a
   white-type ruling (type26-013) if he wants it.
3. **D-Q3 grouped/stacked:** kit has reviewed grouped + stacked bars — NOT in my brief's worklist;
   promote next wave? (Chevron stays gauge-only per DV-D04 regardless.)
4. **D-Q4 amber floor:** status-watch light mode = 3.02:1 vs page — passes the 3:1 graphic floor
   with zero margin (R-D3 by design). Comfortable, or lift for charts?
5. **D-Q5 delta-token seam** (gap 3 above): one delta convention for canon, or chart/card split?

## Environment notes (for the conductor)

- **Background builds die with the launching call here** (bwrap `--die-with-parent`, per-call PID
  namespaces — `pgrep` even self-matches its own wrapper, the exact wave-1 pkill trap). Full
  `_build_all.py` exceeds the 45s call cap → per-gate verification above; **the authoritative
  51-step serial run is yours.**
- **Parallel-lane observations (no action taken):** canon/showroom regenerating under other live
  lanes throughout (Data-grid, Date-picker, Time-picker, File-upload, Stepper landing); my
  Chart-line 14px was briefly healed INTO canon by a sibling build before my fix — regenerated
  clean. `git status` also showed `_validate_radius.py` modified by another lane mid-session —
  not mine, not touched.
- The unwired `_validate_type_composites` tool flags my `th{font-weight:500}` + `.amt{500}` — same
  corpus-wide debt class as gated Table/Cards (its deferral is logged in `_DS-IMPROVEMENTS.md`);
  composite-clean everywhere else.

## Files touched (ALL NEW; zero shared-file writes, zero git)

- `knowledge/snippets/Chart-{bar,line,donut,sparkline}.reference.html`
- `knowledge/components/chart-{bar,line,donut,sparkline}.meta.json`
- `notes/_receipts/2026-07-22-phase2-worker-D-charts.md` (this file)
- *(Generated artefacts — canon.css components block / showroom / gate reports — refreshed by
  regenerate-always steps I ran; deterministic, any build reproduces them.)*

## Proposed §C lines

- **Charts kit PROMOTED (worker D, 4/4):** Bar · Line · Donut · Sparkline as gated reference
  snippets, PROVISIONAL-AGENT pending Dave's dataviz sign-off (kit stays PARKED, untouched).
  8 figures 0-blocking/0-advisory by gate-import; census zero-growth; no pressables.
- **Wire the dataviz gate to chart snippets** (one-line discovery change — new-surface rule).
- **D-Q1–D-Q5 await Dave** (marker fill · donut labelling · grouped/stacked · amber floor ·
  delta-token seam).
