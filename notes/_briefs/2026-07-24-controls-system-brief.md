# Brief — "the Controls System" (SOLO, Opus) — cut 2026-07-24 pm

*Cut by the morning/afternoon Opus conductor window as it wrapped at Amber. Role from Dave's opener
("Apollo — the CONTROLS SYSTEM"). This is ONE coupled brief — three strands that meet in a single
control. **Read first, in order:** this brief → `_LIVE-STATE.md` top (the in-flight "controls system"
bullet) → `reviews/CHART-CONTROLS-vs-ATOMS-2026-07-24-v1.html` (the compare sheet — the evidence that
started this) → `snippets/View-options.reference.html` + `snippets/Chart-line.reference.html` (control
CSS) → `knowledge/guidelines/accessibility-interaction-design.md` (ID-15/ID-26 target size) →
`_proforma/_TYPE-DECISIONS.md` (T-D14/T-D15 territory) → run `python3 knowledge/_consult.py "<what
you're about to design>"` before designing.*

*Baseline: if you are running PARALLEL to the window that cut this, treat its wrap commit as your
baseline (`git log --oneline -1` at lane start) — it committed the spine + this brief + the compare
sheet. Single-writer holds: it finished its writes before you start yours.*

*Gauge-stamp your receipt at authoring (`_RUNBOOK-context-gauge.md` § authoring-time stamp).*

## The three CONFIRMED rulings (Dave, 2026-07-24 — reflect-back confirmed in-chat)

1. **Segmented control → promote View-options into a SEGMENTED-CONTROL ATOM.** The chart's view-switch
   **drops its hand-rolled `.dv-seg`** and **consumes the promoted View-options atom**, which carries
   the **sliding indicator + pill-style padding** (the Day/Week/Month look on the compare sheet). NOT a
   compact/quiet variant — the chart adopts the full atom.
2. **Hit-area standard — invisible 44 target on all interactive elements.** Dave: *"comfortable with
   different sized buttons as long as there's an invisible hit area."* Small VISIBLE controls are fine
   provided each carries an accessible hit area at the **44 default**.
3. **Mini text ramp — 12 / 14 / 16 (3 variants)** as size variants for labels + controls. **Ceiling =
   16, VERIFIED:** 18 is absent from the type scale (steps: 12/14/16/20/24/28/32/40/52 — 18 appears
   only as leading/paragraph); 20 dropped (Dave changed his mind). Lands on HSBC's own "16px and below
   = standard text" band.

## Repo-standards finding (DONE — do not re-derive, build on it)

- **HSBC DEFAULT target size = 44×44**, 24px = the EXCEPTION — `aid-009` [REVIEW], `ID-26` [2024],
  `ID-15` (2.5.5 basis; **≥1px inactive gap** between targets). `accessibility-framework.md`: declared
  bar is WCAG 2.2 AA, 2.5.8 target-size adopted.
- **The invisible / SHARED hit-area technique is ALREADY sanctioned in our guidelines** — this is the
  precedent for Dave's ask, not a new idea:
  - tags/chips: font-6 (20px line) + 12px above + 12px below = **44 effective**, and **adjacent rows may
    SHARE the 12px band** "so long as it doesn't overlap the actual physical target area."
  - links: "surrounding target area of 44px, unless they are inline."
  - `icon-005` (**BLOCKING**): functional icons need a min **44×44** target area.

## Deliverables (proposal/review docs + the atom; NO type mints without Dave)

1. **Segmented-control atom** — CONSULT + survey first (`component-types.json` registry, View-options
   `.meta.json`, Tab-bar/Table `.seg` — they share the sliding-indicator pattern). Promote View-options
   into a registered segmented-control atom: sliding indicator + pill padding, **size variants (the
   mini ramp)**, and an **invisible hit area**. Rebind `Chart-line.reference.html` to consume it
   (replaces `.dv-seg`). Radius/type via role + composite tokens (no raw shorthand).
2. **Apollo hit-area standard (review doc)** — industry cross-check (Material 48dp · Apple 44pt ·
   GOV.UK · Carbon · WCAG 2.5.5 vs 2.5.8), then propose the standard: **mechanism** (pseudo-element
   expanded target / min-size overlay + a `hit-area` token), the shared-band exception (already ours),
   and a **gate** proposal so it's enforceable. Apply to the small chart controls + the segmented atom.
3. **Mini text ramp (proposal sheet)** — 12/14/16 as size variants for label + control composites
   (`t-cm-chart-label` etc.). T-D15 candidate. **PROPOSAL ONLY — no type.css mints without Dave's
   ruling** (derivation governance; the parked note's constraint).

## Still OPEN (not ruled — propose, don't force)

Homes for the chart's other controls: the `.dv-vt` **outline toggle** (Target line / Last year) + the
**Copy CSV** action button, and the `.dv-legbtn` **legend-filter** (swatch + letter + hollow off-state,
likely stays **dataviz-scoped**). Candidate: a small **quiet-utility control family** (registry group
#2) OR fold into the segmented-atom family. Surface the OBSERVED duplication; Dave rules.

## Fences + verify

Self-conduct if you are the only live window; if you commit, follow `_RUNBOOK-git-commit.md` (lock
dance). Build green (`_build_all.py`); render-verify per `_RUNBOOK-render-verify.md` (≥2 widths + dark).
The compare sheet is committed context — extend/version it (`-v2`), never overwrite.
