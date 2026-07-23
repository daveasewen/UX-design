# Fable brief — Chart revisit: lift every canon chart to the proforma standard

*Cut 2026-07-23 (Thu, BST) by the Opus scatter-exemplar session. Role: **Fable, solo → conductor**
(start solo on the exemplar; divvy the fan-out into worker lanes once the pattern is proven).
Model routing: **Fable builds** (fresh full budget), **Opus conducts/verifies** the reconcile if you
split into workers. Read `GOOD-MORNING.md` → this brief → `_LIVE-STATE.md` top delta first.*

---

## The ask (Dave, verbatim intent — 2026-07-23)

> "I see [the proforma] as the best example so far — the animations, layout, colours, table view,
> popover, and they are all responsive. I want to do **as little review work as possible**. The work
> done so far is good, but not quite there. I want Fable to **revisit every chart component produced
> so far**. All five. The **legends also act as filters**. Can we have some **other ideas for deeper
> data manipulation**. Make sure **all the charts have an optional title**. And **we've completely
> missed the bar with line overlay**."

**The reference file — the gold standard, study it first:**
`knowledge/_proforma/DataViz-interactive.html`

**The gap it exposes:** when the round-one kit was promoted to canon snippets (Phase-2 wave 2), the
**entire Layer-2 was stripped** — "no pressables, no JS, native `<title>` tooltips, static geometry."
Dave has now ruled that **Layer-2 IS the bar.** The promoted snippets
(`snippets/Chart-{bar,line,donut,sparkline,scatter}.reference.html`) are the "good but not quite
there" tier. This brief brings the proforma's richness **into** canon.

---

## Scope — all 5 canon chart snippets, to the proforma bar

`Chart-bar` · `Chart-line` · `Chart-donut` · `Chart-sparkline` · `Chart-scatter`.
(Scatter's snippet is also static + native-tooltip — it joins the pass, it is not exempt.)
Plus **one net-new type** (below): the **bar + line overlay combo**.

### Confirmed requirements — every chart carries these (all present + proven in the proforma):

1. **Interactive value popover** (`dvTip`) — replaces the native `<title>`. Port the proforma's
   `#dvTip` (role=status, aria-live=polite) + the `data-tip` mechanism: shows on `pointermove` AND
   `focusin` (keyboard-accessible — non-negotiable, Apollo a11y aspiration), edge-flips at the
   viewport bounds, hides on `focusout`/pointer-leave. Every series element gets a `data-tip`.
2. **Responsive reflow** (`fitCharts()`) — port the `data-fx`/`data-fxs`/`data-ys`/`data-fx2`/`data-x0`
   baked-fraction system: the chart relayouts to its container width, **text never scales** (DV-D02,
   RULED). Recompute on `resize` (rAF-debounced). The baked SVG must still render if JS fails
   (progressive enhancement — the proforma's try/catch posture).
3. **Table-view POPOVER panel** — ★ Dave corrected this 2026-07-23: **forget the frosted drawer — the
   table is a floating popover panel** (his mock: a bar chart with a **"View as table" ⇄ "Hide table"**
   toggle top-right, and a **floating card** — white/surface ground, thin border, soft drop shadow —
   containing the title + the real `<table>`). Anchored near the toggle, over the chart, edge-aware.
   `aria-controls` + `aria-expanded` on the toggle; the panel is a labelled region, keyboard-dismissible
   (Esc), focus-managed. Keep a real `<table class="dv-table">` inside (dv-005 spine is mandatory).
   *Mock detail (for fidelity): heading "Spend by category this month, pounds"; columns Category |
   Amount (£); ground = surface token + border + shadow, NOT frosted/blurred. Card corners = role token.*
4. **Legend-as-filter** — the proforma's `button[data-series-toggle]` pattern: clicking a legend row
   shows/hides that series (`aria-pressed`, keyboard-operable). Multi-series only; single-series legend
   stays a static key. **Consider also click-to-ISOLATE** (solo a series, dim the rest) as the second
   gesture — propose to Dave (idea menu below).
5. **Optional visible title** — a `dv-title` slot on every chart (dv-006: "title reflects the main
   insight"). Optional (renders only when supplied); a type composite heading (sentence case, gated),
   sitting above the chart. When absent, the sr-only figcaption still names the chart.
6. **Full motion parity** — the proforma's animations: line draw (pathLength), marker cadence, donut
   radial sweep, bar grow, fade-ins. **Decorative motion stays CSS** (fades/draws); JS is allowed only
   for BEHAVIOUR + data-driven GEOMETRY (donut arc growth, fit reflow) — see the gate note below.
7. **High-contrast mode** — port the proforma's `data-contrast="high"` palette swap if it carries
   cleanly (advisory — confirm it survives the token-manifest projection; flag if it needs new tokens).

### ★ The named gap — bar + line overlay (combo / dual-axis)

Dave: "we've completely missed the bar with line overlay." Build a **combo chart**: bars (primary
axis) + a line overlaid on a **secondary axis** (e.g. volume bars + a running-average line, or revenue
bars + a margin-% line). This is a net-new type — no proforma precedent to promote, so **design it to
the same method** (semantic SVG + tokens + CSS/data-driven motion + real table + popover + fit +
optional title). Decisions to make + surface: secondary-axis labelling, the line's series token vs the
bars', dv-bar-009 zero-baseline still applies to the bar axis, dv-line-011 straight segments for the
line. Likely lives as a new `Chart-combo.reference.html` (or a variant inside `Chart-bar`) — recommend
a **new snippet**; confirm with Dave.

---

## ★ Decision #1 — where the behaviour lives (resolve FIRST, recommend to Dave, then build)

The proforma has **one shared script** for all its charts. Five separate snippet files must not each
**re-type** that behaviour — that is the exact ADR-0013 anti-pattern (never re-implement a shared
rule; accrete a generated partial). Options:

- **(a) Generated JS partial (RECOMMENDED)** — one source `dv-behaviour` (popover · fit · drawer ·
  legend-filter), injected into each snippet between `AUTO-PARTIAL`-style markers by a generator
  (mirror `gen_component_partials.py`), sync-gated (`--check`), single source of truth. Honours
  ADR-0013 ("retrieval reaches behaviour, never re-type"). Likely warrants a **short ADR-0015** or a
  ruling extending ADR-0013 to behaviour partials.
- **(b) Shared referenced module** — `canon/dv-behaviour.js`, all snippets `<script src>` it; showroom
  injects it into the payload. DRY but snippets stop being self-contained single-file artefacts.
- **(c) Inline per snippet** — self-contained/portable, but 5× duplication (rejected by ADR-0013
  unless Dave rules portability wins here).

**Recommendation: (a).** It is the ADR-0013-consistent answer and keeps "one behaviour, many
consumers." Reflect the choice back to Dave, inscribe it, THEN build. This is the "correctness + best
practice over expedience" call Dave favours — do not shortcut to (c) silently.

---

## ★ Deeper data-manipulation ideas — the menu Dave asked for (PROPOSE, he picks by number)

Do **not** build all of these — surface them as a **pick-list** so Dave rules cheaply (governance:
the engine proposes, Dave promotes). Recommend building the ✅ core now (low review, mirrors what he
already blessed) and parking the rest behind his pick. All must be **keyboard-accessible + gate-clean +
token-bound + reflected in the table** (the table is the accessible truth surface).

Core (recommend build now):
- ✅ **Legend filter** (confirmed) + **click-to-isolate** (solo a series).
- ✅ **Hover/focus highlight** — hovering a legend/point emphasises that series, dims the others.
- ✅ **Table POPOVER with SORTABLE columns** — sorting the table re-orders the chart (bar/column);
  chart and table stay bound (one data source).

Proposed (Dave picks):
- **Sort toggle** (bar/column) — original / ascending / descending, from the toolbar.
- **Value ⇄ % toggle** (stacked, donut) — absolute vs share-of-total.
- **Cumulative toggle** (line/bar) — discrete vs running total.
- **Threshold / target line** — a reference line the user toggles; points above/below flagged (and in
  the table).
- **Brush / range-select** (scatter, line, combo) — drag an x-range → filters the table to the
  selection. Advanced (pointer + keyboard equivalent needed).
- **Compare / ghost series** — overlay a previous period as a muted series.
- **Copy / download data** — export the table as CSV (utility + a11y win).
- **Annotate a point** — pin a note (ties to the existing review-overlay pattern).

---

## Architecture + gate guidance (so you pass first try, minimal review)

- **DEF-003 (CSS-governed motion) does NOT glob snippets** (only `_proforma/*.html` with an
  `icon-manifest`). It bans only JS that computes **scale / sets `--hs`/`--ps` / assigns
  `transform:scale`**. Behaviour JS (open/close, filter) + **data-driven geometry** (fit reflow, donut
  arc `setAttribute('d',…)`, bar width) are **explicitly allowed** — the proforma passes DEF-003 with
  exactly this JS. Keep decorative motion (fades/draws) in CSS; keep the banned patterns out. If you
  add an `icon-manifest` to a snippet, you opt it INTO DEF-003 — don't, unless intended.
- **DataViz gate** (`_validate_dataviz.py`, globs `snippets/Chart-*.reference.html` automatically):
  all existing blocking rules still bite — `dv-017` var() fills only · `dv-016` ≥3:1 series+axis both
  modes · `dv-009` flat fills · `dv-bar-009` zero baseline (bar family) · `dv-line-011` straight
  segments · `dv-pie-009/010` donut · `§04.3` letters when ≥2 series. Run `--selftest` after any gate
  touch. The popover/fit/drawer/filter are invisible to it (behaviour) — but keep `data-tip` values
  **in sync with the table** (single source).
- **Legend buttons are now PRESSABLES** — this reverses the "charts have no pressables" posture. Decide
  their control identity: they are **toolbar/utility controls** (like the demo-controls), **not** the
  primary button-family — so they should **NOT** inherit B-D7 press physics (no scale/translate). Give
  them a quiet, accessible pressed/selected state (aria-pressed + a token-bound visual). Flag this to
  Dave as a ruling (it touches the button-states posture).
- **Tokens** — every colour/space/radius stays token-bound (DEF-004 no-hardcode). New needs likely:
  the long-receipted **`data/axis` + `data/grid`** quiet-ink tokens (mint them now if you touch axes —
  closes that gap), a **`data/target`** token if the threshold line is built, secondary-axis label
  ink. Do not derive-and-promote — propose values, Dave rules.
- **Type** — composites only (`t-cm-*`), sentence case, 4px grid, weights {100,300,400,500,700} no 600.
  The optional title = a heading composite; axis/legend/table = `.t-cm-legal`/`.t-cm-caption` as now.
- **Showroom** — the harness embeds each snippet as a base64 payload in an iframe; **snippet `<script>`
  runs there** (the review overlay proves it). Regenerate `gen_showroom.py` + `gen_theme_cascade.py`
  after edits. The 4-theme × light/dark projection must still hold via each snippet's `#token-manifest`.
- **Coverage / census / radius** — every snippet needs its `components/*.meta.json` (coverage gate,
  65/65 now) · no press-shaped locals unless registered (partials ratchet, census currently 32) ·
  radius = role tokens only (snippets are radius-strict in `MIGRATED_SNIPPETS`).
- **Accessibility is the bar, not a checkbox** — popover on focus, legend filter operable by keyboard,
  drawer aria wired, series toggles announced, the table always the full truth. Target WCAG 2.2 AA.

---

## Run plan — prove-one-then-wave (mirror the scatter exemplar)

**Phase 1 (solo, DO FIRST):** resolve Decision #1 (behaviour home) with Dave → build the shared
behaviour + apply to **ONE exemplar chart end-to-end** (recommend **Chart-line** — richest: multi-
series, markers, legend-filter, draw motion). Wire popover + fit + drawer + legend-filter + optional
title. Green the build. **Hand to Dave to eyeball the one** before fanning out. Also draft the
deeper-manipulation pick-list (above) as a short review artefact in the SAME window.

**Phase 2 (wave — divvy):** apply the proven pattern to the rest. Suggested lanes (fenced = NEW/edited
snippet files + receipts only, no git; conductor runs the serial set + ONE commit):
- **Lane 1:** Chart-bar + Chart-scatter (point/bar geometry + fit).
- **Lane 2:** Chart-donut (radial sweep + variant tabs) + Chart-sparkline (compact; popover + fit).
- **Lane 3:** ★ Chart-combo (bar + line overlay) — the net-new type, dual-axis.
- **Conductor (Opus):** registry/CATEGORIES/MIGRATED_SNIPPETS/coverage metas/cascade/showroom + the
  behaviour-partial generator wiring + reconcile receipt + ONE commit. Dave pushes via GitHub Desktop.

---

## Self-verify checklist (Dave wants MINIMAL review — earn it)

Before handing anything back, per chart:
- [ ] `python3 knowledge/_build_all.py` green (51+ steps; note new gate/selftest counts).
- [ ] DataViz gate 0 blocking (run direct + `--selftest`).
- [ ] Geometry sanity: every plotted point/bar inside the plot bounds; chart↔table parity exact
      (script it, as the scatter exemplar did).
- [ ] Popover: shows on hover AND keyboard focus; edge-flips; hides correctly. Values == table.
- [ ] Fit: reflows across the showroom width slider; text does not scale; baked SVG survives JS-off.
- [ ] Legend filter + table popover: keyboard-operable (toggle + Esc-dismiss), aria correct.
- [ ] Census unchanged (or every new registered) · radius strict-clean · coverage N/N · type/blast
      gates green.
- [ ] Render-verify OWED note if Playwright still refuses (standing project-wide) — substitute
      mechanical proofs.
- [ ] Review overlay rides every showroom pane (async pin-comments = how Dave reviews with least effort).

## Open questions for Dave (numbered, cheap — rule any window)

1. Behaviour home = generated JS partial (rec) / shared module / inline? (Decision #1)
2. Combo chart = new `Chart-combo` snippet (rec) or a variant inside `Chart-bar`?
3. Legend gesture = filter only, or filter + click-to-isolate?
4. Which deeper-manipulation ideas to build now vs park (pick from the menu)?
5. Legend/toolbar pressables = quiet utility state, NO B-D7 press physics — confirm.
6. Mint `data/axis` + `data/grid` (+ `data/target` if threshold built) now? (closes the receipted gap)
7. Optional title: also a `dv-subtitle`/source-note slot, or title only?
8. **Label weight seam (found 2026-07-23, Dave's eye):** the proforma's 07-22 snap made chart labels
   12/**500**; canon chart snippets bind `t-cm-legal` = 12/**400**. Two live weights. Reconcile —
   Dave's floor instinct ("smallest size wants MEDIUM") is one candidate; a 500 form-label composite
   question (wave-1 Q1) is adjacent. Don't pick silently; T-D15-flavoured.
   *(Post-cut addenda: Decision #1 = RESOLVED, ADR-0015 accepted 2026-07-23 — behaviour partial,
   ≤16KB gated. Q6 = RULED, DV-D07 — two-channel mint, values on the Q6 sheet. Q1–5, 7, 8 open.)*

*Provenance: this brief continues the chart-expansion programme (prove-one-then-wave). The scatter
exemplar (`snippets/Chart-scatter.reference.html`, build green 51/51) is the layout/lock-up reference;
`_proforma/DataViz-interactive.html` is the INTERACTION reference. Both are the source of truth — do
not re-invent, port + accrete.*

---

## ★ CONDUCTOR ADDENDUM — 2026-07-23 (Thu ~17:45 BST) · role split RULED by Dave

**Dave ruled mid-afternoon: the bar-audit session becomes CONDUCTOR; a fresh Fable window runs
Phase 1 of this brief as the WORKER lane.** Single worker, so fences are wide — but they are fences.

### What changed since the brief was cut (read before building)

1. **ADR-0015 + DV-D07 are RULED** (see the parenthetical addenda above — behaviour partial ≤16KB
   gated; two-channel axis/grid mint, values on the Q6 sheet `reviews/DATA-AXIS-GRID-2026-07-23-v1.html`).
2. **★ BAR AUDIT LANDED (this session):** `reviews/BAR-CHART-AUDIT-2026-07-23-v1(.REVIEW).html`.
   Confirmed: responsive reflow absent from ALL FIVE canon charts (restore = confirmed req #2);
   grouped/stacked unpromoted (B1, Dave's call, bar lane); h-bar recolour flag (B3, bar lane).
3. **Q8 / B2 is formally OPEN — DO NOT resolve it in the exemplar.** The 07-22 snap FLATTENED the
   kit's reviewed weight ladder (labels 400 · values 600 · keys 700 → uniform 500); one 12/500
   composite would inscribe the flattening. **Exemplar binds the EXISTING canon composites
   (`t-cm-legal` 12/400 etc.), zero type mints; Dave's B2 ruling retro-propagates as a composite
   swap.** (Tokens for DV-D07 colour/alpha are NOT type — that mint rides your build as briefed.)
4. **Proforma scatter section has no fit wiring** (audit B4). NOT your scope — it rides the
   scatter lane in the wave. Do not edit `_proforma/DataViz-interactive.html` at all.

### Lane fences (worker = the fresh window)

**Worker OWNS (write freely):** `knowledge/canon/dv-behaviour.js` (new source) · the partials
generator extension + its selftest · new/extended gate(s) + selftests · `knowledge/component-types.json`
(dataviz group entry — single-worker wave, direct write is safe; contracts fire on registration) ·
token stores for the DV-D07 mint + theme override sets · `snippets/Chart-line.reference.html` + its
`components/*.meta.json` · regenerated artefacts (canon/cascade/showroom ride your builds).

**Worker does NOT touch:** `GOOD-MORNING.md` · `_LIVE-STATE.md` · `_FUTURE-STATE.md` ·
`notes/_briefs/*` · `reviews/BAR-CHART-AUDIT*` · ledger spines beyond your own inscription lines ·
**git (NO commits — conductor commits ONE reconcile).**

**Receipt:** `notes/_receipts/2026-07-23-chart-line-exemplar-worker.md` — landed files · gate/selftest
results · judged deltas · open Qs · any Dave ruling absorbed mid-flight VERBATIM.

**Baseline:** conductor certified **51/51 green** pre-lane (commit noted in-receipt when you start —
`git log --oneline -1`). Build serially as you land pieces; the authoritative final serial run +
reconcile + commit are the conductor's.

### ★ LIVE RULINGS ABSORBED — 2026-07-23 evening (conductor; ledger inscribed, seed fed)

- **B2 / Q8 = RULED → DV-D08.** Chart text ladder: **12/500 floor** (labels · axis · legend text ·
  values; values tabular) + **700 emphasis** (legend alphas, on-chart keys). 600 stays banned.
  **The addendum's "no type mint" instruction is LIFTED** — mint the composite(s) per DV-D08
  (T-D14 markup-class pattern, register in `_type-bindings.json`, blast-radius gate) and bind the
  exemplar to them.
- **B1 = RULED:** grouped + stacked PROMOTE in the WAVE (bar lane) — not your exemplar scope.
- **B3 = RULED → DV-D09:** bar-family defaults orientation-distinct (column `series-1` · h-bar
  `series-3`) — bar lane, noted for the wave briefs, not yours.
- **Mini chart ramp (12–20) is PARKED** (`_FUTURE-STATE`) — do NOT build it.
