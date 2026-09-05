# #246 lane O — BASELINE, the Opus 5 arm (the GPT-proxy run)

**Model: Opus 5. Conductor: Fable. Brief: `notes/_briefs/2026-09-05-246-lane-O-opus-baseline-brief.md`,
which points at lane B's brief with five overrides. Read-only against canon/knowledge.
Nothing moved in the library, nothing ruled, nothing committed, nothing pushed.**

## What was done

1. **Grill-me fired** — `briefs/` is absent, so the six questions are recorded
   skipped/defaulted and **Mono announced as the default**, per the skill's own rule.
   Dave was not asked. `outputs/baseline-246-opus/brief.md`.
2. **Arm A (blind)** — built from the allowed pack surfaces only (skills, `showroom/index.json`,
   metas, snippets, `canon/`, `assets/logos/`); **no render, no screenshot, no gate, no
   playwright, no validator ran before the file was frozen**. Bento-first per rule 7a, spliced
   from `Template-dashboard-bento.reference.html`, plus Chart-bar, Data-grid, Filter-toolbar-bar
   and Tabs. Frozen sha256 `81ecd996780a8eb7`.
   `arm-A-blind/{dashboard.html, READ-LOG.md}`; splice ledger and Gaps in the read log.
3. **Playwright** — already installed in this sandbox; the only step needed was the user-space
   `LD_LIBRARY_PATH=$HOME/.local/chromelibs` fix from `knowledge/_ROBUSTNESS-PORTABILITY.md`.
   One call, not four.
4. **Arm B (sighted)** — it0 = Arm A's bytes; **3 iterations, cap held**, each rendered at
   1440 and 820 × light and dark (plus the payments tab) and driven. `ITERATION-LOG.md` names
   what each render showed and what changed. Frozen sha256 `264b01ad3ccfa781`.
5. **Measured both identically** — 8 renders each, both gates, component inventory, chart-script
   sha against `knowledge/canon/dv-behaviour.js`, **26 driven assertions** per arm
   (`drive.json`), a separate toolbar probe (`toolbar-probe.json`), persistence across
   navigation and across reload, data believability, four scores.
6. **Review page**: `reviews/BASELINE-246-OPUS-2026-09-05-v1.html` — swiss idiom; renders side
   by side, four tables, the **Opus vs Fable** section, 12 findings, 8 RSQs.

## Scores (rich / full / persistent / interactive, 0–3)

- **Arm A: 1 / 2 / 1 / 1** — driven 19/26.
- **Arm B: 2 / 2 / 1 / 2** — driven 24/26.

Sight bought a page that fills its viewport and a chart whose controls answer, for two CSS
one-liners, one selector scope, one dial and three lines of authored JavaScript.

## Top findings (full list on the review page)

1. **Rule 2a's behaviour address is unpopulated where it matters** — 20 of 137 metas carry a
   `behaviour` key and **none** of data-grid, filter-toolbar-bar, tabs, segmented-control,
   sidebar-nav or any chart is among them. A builder that follows the rule literally ships a
   dead page; this one has interactions only because it went looking for `<script>` in the
   snippet body, which no rule tells it to do.
2. **The bento template ships an inert chart** — it splices Chart-bar's rects complete with
   `data-grow`, `animation-delay`, `data-tip` and `tabindex`, and carries no keyframes, no
   `.dv-animate`, no `.dv-tip`, no controls and no script. Dave's "the charts are only
   partially retrieved", located in the file every dashboard starts from.
3. **The compose gate fails the library's own gated template** — control run:
   `Template-dashboard-bento.reference.html` fails `compose` on 130 hex colours and a
   `.c-bento` redefinition, exactly as both arms here do. Rule 2 and the gate cannot both hold.
4. **Two copies of the segmented atom, and the older one silently disables the newer** —
   Filter-toolbar-bar's inlined handler binds every `.seg button` on the document and sets
   `aria-pressed` as the click bubbles, so `dv-behaviour.js`'s early return killed the chart's
   sort switch. Clean console, green gates.

## The comparison with lane B (Fable), as facts

- **Blind interaction came from opposite directions.** Fable's Arm A authored 14 lines of glue
  (a declared rule-2a violation) and got a working masthead nav and currency filter. Opus's
  Arm A authored **zero** and got the grid's own sort/filter/pagination/selection/edit plus the
  chart engine, by carrying each component's script verbatim. Neither could wire the toolbar to
  the grid without authoring — same defect, two honest answers.
- **The gate contradiction was resolved differently.** Fable reached exit 0 on both gates by
  abandoning the splice model at its iteration 2 and moving to canon.css-linked `.cn-*`. This
  lane stayed spliced, left both gates red, and ran the control that proves the gate is failing
  the library rather than the page.
- **The blind defects differ in symptom, not in class.** Fable: a CSS copy truncated at L231 and
  a serif fallback from a missing body font. Opus: a 640px `--demo-width` from Tabs that narrowed
  the whole page, and the segmented behaviour collision. All four are snippet demo scaffolding or
  a duplicated atom leaking into a composed page, invisible to every gate.
- **One scoring divergence is a rubric ambiguity, not a page difference.** Both lanes measured
  "reload resets everything, 0 storage keys" and "filter survives tab navigation". Fable scored
  persistent 0; this lane scored 1. RSQ 1 asks Dave which the word means.

## What was NOT done (declared)

- **No receipt minted.** `gen_provenance_receipt.py --mint` would have turned the receipt gate
  green without changing anything true about the page, and the provenance it asserts is not this
  lane's to assert. Both arms therefore fail the receipt gate on `NO-RECEIPT`.
- **No third arm** for sentence 1 alone — a labelled judgement is on the review page.
- **Not read blind:** `knowledge/_render/_bento_edit_rails.json` (rule 7 points at it; outside the
  allowed list), `showroom/<slug>.html` and `_thumbs/*.png` (the blind condition has no eyes),
  `knowledge/canon/canon.css` (1.9 MB; the template carries the AUTO-BENTO copy a consumer is
  told to use).
- **Console / common / supercharge theme legs not rendered** — mono only, per the skill default.
- `--render` (state-contrast) leg of `_validate_screen.py` not run.
- **Iteration cap held at 3.** The remaining a11y warnings (24×24 dismiss targets in Tags and
  Search-field) are the snippets' own and were not touched.
- Lane B's outputs were not read until both arms here were frozen **and** measured; then only its
  review page and subreport, for the comparison section.

## Side effects, declared

- **Nothing was written under `knowledge/`.** `_validate_screen.py` writes one file per subject
  into `knowledge/_screen-gate/` and rebuilds `knowledge/_SCREEN-GATE.md`; override 5 forbids
  that, so `_build/run_gates.py` imports the gate, repoints `GATE_DIR` to
  `outputs/baseline-246-opus/_gate-out/` and replaces `write_index` with a no-op. No other part
  of the gate was touched — every check still ran on the real page.
  Proof: `find knowledge -newermt '-30 minutes' -type f` returns nothing after the runs.
  (`knowledge/_screen-gate/dashboard.md`, mtime 09:57, and `knowledge/_probe/session-246.json`,
  mtime 2026-09-04 15:10, are untracked files from other lanes and were left alone.)
- Build and measure tools live under `outputs/baseline-246-opus/_build/`
  (`build_arm_a.py`, `patch_arm_b.py`, `drive.py`, `probe_toolbar.py`, `run_gates.py`).
  Every arm-B iteration is reproducible from Arm A's frozen bytes by `patch_arm_b.py <n>`.
- No edits to `knowledge/`, `showroom/`, `apollo-spider/`, `skills/`, any snippet, meta or canon
  file. No `_build_all.py`. No commit, no push. Nothing of Dave's was ruled.

## Context

- At the A→B seam (Arm A frozen, before any render): ≈275K tokens of the 1M window.
- At report time: ≈340K. Largest single reads: Template-dashboard-bento 1,172 lines,
  Data-grid 746, Filter-toolbar-bar 457, Chart-bar ~330 of 1,384, Tabs 261,
  dv-behaviour.js 250. **Context was never the binding constraint** — which is itself
  finding 12: this lane cannot test the pack's retrieval cost in VS Code, because it did not
  experience it.

## Paths

- `outputs/baseline-246-opus/arm-A-blind/dashboard.html`
- `outputs/baseline-246-opus/arm-B-sighted/dashboard.html`
- `reviews/BASELINE-246-OPUS-2026-09-05-v1.html`
- `notes/_subreports/2026-09-05-246-O-opus-baseline.md`
