# Worker receipt — wave lane ③: Chart-combo (bar + line overlay, dual axis — NET-NEW)

*2026-07-24 ~16:48 BST (date from `date`) · FABLE WORKER · effort HIGH (per the ratified divvy) ·
brief `notes/_briefs/2026-07-24-chart-wave-lane3-combo.md` · baseline `fa29858` (verified
`git log --oneline -1` at lane start) · **NO GIT — conductor commits.** Fences honoured: wrote ONLY
`snippets/Chart-combo.reference.html` (NEW) + `components/chart-combo.meta.json` (NEW) + this
receipt. No writes to component-types.json / dv-behaviour.js / _build_all / MIGRATED_SNIPPETS /
CATEGORIES / spine / proforma / GOOD-MORNING / _LIVE-STATE.*

***Context gauge at authoring: 🔴 RED ~65% (in-head tally, ESTIMATE ±15 — Half-2 measure broken).***
*Per the authoring-time-stamp practice: Red-authored ⇒ re-verify render/gate claims before trusting.
Everything below IS re-runnable: the parity script, gate-import call and render script shapes are
all recorded here.*

## Outcome

**The net-new combo type is designed + built end-to-end:** bars (primary axis, zero-based) + line
(secondary floating axis, page-casing intersection mechanism), full exemplar Layer-2, verified
mechanically + gate-by-import (0 blocking) + render-verified at 2 widths × light/dark/HC/filtered/
JS-off with the real font — **all renders SEEN**. The render pass caught and fixed one real
collision (below). Census zero-growth (32). **Snippet is UNREGISTERED — behaviour markers are an
EMPTY PAIR until the conductor's registration serial injects dv-behaviour.**

## ⚠⚠ Q2 — NEW SNIPPET vs Chart-bar variant: DAVE'S CALL, FLAGGED LOUD

Built as a **NEW snippet** per the standing recommendation (revisit brief §combo + this lane's
brief). If Dave rules "variant inside Chart-bar" instead, the fold is mechanical: the figure block +
the combo-specific CSS (~40 lines: .dv-casing, .dv-axis2, the Layer-2 controls Chart-bar lacks)
move across; the meta merges as a variant entry; grammar decisions all survive. **Nothing inscribed
assumes the answer.**

## Live absorb — composed against `fa29858`, NOT the brief's snapshot

The brief predates Friday's control rulings. The combo consumes the LATEST Chart-line control
language: single-cell seg toggle (`.dv-toggle-seg`, 2px inset + floating `:has` fill) for Target
rate · copy⇄tick CSV (label static) · dropdown table toggle with SOLID rotating arrow (label
static) · ONE literal `--control-h` 32px across all 3 controls. Icons byte-copied from Chart-line
(library-path assets, already 0-UNKNOWN under the icon gate).

## The five design decisions (each: what, why, alternatives)

1. **Secondary-axis grammar = right-edge rule + suffixed tick text, no axis titles.** Ticks
   "85%…100%" carry the unit IN the text (self-labelling, stays inside DV-D08 type); the right
   rule renders in the **data/axis role** (DV-D07) — deliberately QUIETER than the ink baseline,
   encoding hierarchy: bars own the plot floor, the overlaid scale is chrome. Primary ticks stay
   bare numbers (unit in figcaption + legend + table header — existing canon idiom). *Rejected:
   axis titles (no axis-title idiom exists anywhere in canon — that's a bigger mint than this lane
   should make; dv-bar-002 advisory noted, labels judged non-obvious-proof via legend+suffix);
   rejected: a second gridline set for the secondary scale (competing grids = unreadable; grid
   follows the primary only, dv-bar-003).* Governs: **dv-line-006 honoured in full** — different
   units only, clearly labelled, and the LEGEND states the axis per series ("Payments — left axis,
   £ thousands" / "STP rate — right axis, %").
2. **Series assignment: bars = data/series/1 (DV-D09 column default) · line = data/series/2.**
   Both ≥3:1 vs page both modes (5.26/5.04 L · 3.31/3.46 D; HC ≥6.40). **The intersection
   finding, measured: line-vs-bar direct contrast = 1.04:1** — the categorical set is isoluminant
   BY DESIGN, so NO series pair can ever separate a crossing line. **Mechanism = a PAGE-COLOUR
   CASING** (`.dv-casing`, 6.5px page stroke under the 2.5px series stroke — the markers' own
   series-fill + page-stroke-2.5 halation idiom generalised to the line). Every crossing boundary
   then reads at page-vs-bar-fill = **the bar's own gate-checked ≥3:1** (5.26 L / 3.31 D; holds in
   HC). *Rejected: ink-coloured line (max contrast but loses series identity + legend/filter
   coherence); rejected: dashed line as the only separator (fails at the fill boundary, not a
   contrast mechanism).* Casing deliberately NOT class `dv-series` (the gate must never
   contrast-check page-vs-page) but DOES carry `data-series-group="2"` so filter/isolate/highlight
   take it with its line (render-asserted: hiding B hides the casing).
3. **Zero-baseline posture — THE COMBO PRECEDENT:** bar axis zero-based ALWAYS (`dv-bar-009`,
   `data-domain-min="0"` declared); the line's secondary axis MAY FLOAT (dv-line-001 asymmetry) —
   here 85–100% so the rate's movement is legible — and when it floats it shows its FULL suffixed
   tick run, keeping the floating floor explicit, never silent. Stated in the header comment, meta
   antiPatterns, and manifest $note.
4. **X-grammar = BAND CENTRES (new for the line family):** 12 bands across the 522 plot, bars
   centred in bands (width 28), the line's points ride the SAME centres — every point sits over
   its bar. Chart-line's endpoint spread (f=i/11) does not compose with bars; the bar convention
   wins the shared axis. dv-line-011 straight polylines · enlarged markers (r5.5/page-stroke 2.5) ·
   line-end letter key **B in ink** (DV-D08 700).
5. **ONE table spine:** single `<table>` carries both series with unit column headers (Payments
   £000 · STP rate %); † flags at/above the 95% target (Dec); tips == aria == table (parity
   scripted); CSV serialises it via the standard behaviour module.

**Layer-2 carried (exemplar canon):** popover (unit-named tips: "A · Payments · Jun: 802" /
"B · STP rate · Mar: 88.6%"; bars are focus stops too — 12 rects + 12 markers, tabindex 0, aria ==
tip) · fit (bars data-fx/data-fw + line data-fxs/data-ys + both axes' ticks — dual-axis parity
under fit PROVEN, below) · table-view popover (Esc + focus-managed) · optional title · H-stack
head (wrap verified at 560) · legend filter/isolate/highlight (shaped swatches: plain square = the
bar idiom, circle = the line's marker; hollow AA off-state inherited) · CSV · **target overlay on
the SECONDARY scale** (dashed data/target + label, single-cell seg toggle).
**NO seg-view built (the brief's optional):** a cumulative view of a RATE series = a
weighted-running-average semantics question (cumulative % is not a sum) — a design decision of its
own, not a lane default. Receipted as deferred, not omitted by oversight.

## ⚠ For the conductor (serials + 2 judged infra needs — both OUTSIDE my fence)

1. **Registration serial (standard):** add Chart-combo to `component-types.json` group `dataviz`
   ($members + the dv-behaviour contract) → `gen_component_partials.py` injects between the EMPTY
   AUTO-BEHAVIOUR pair · MIGRATED_SNIPPETS (radius-strict) + CATEGORIES "Charts" · showroom regen ·
   build. **No new behaviour hooks needed — the combo consumes the existing module set verbatim**
   (fitOne already handles rect data-fx/data-fw; no dv-behaviour edit required).
2. **★ GATE WIRING — `"combo"` is not in `_validate_dataviz.py`'s type contract.** Two-token edit
   at absorb: add `"combo"` to `BAR_FAMILY` (arms dv-bar-009/007 teeth) + to the dv-line-011 type
   list. This lane ran the gate BY IMPORT under BOTH contracts (stock + proposed): **0 blocking
   both; 10 advisories = the DV-D07 gridline decorative reads (permanent-by-design, same class as
   Chart-line's 16).** Without the edit the gate still passes the file but silently skips the
   bar-family teeth — the new-surface-gate rule says wire it.
3. Docstring contract in the gate ("kpi|column|bar|…") and the meta could gain "combo" in the same
   edit.

## Verification (all run this lane)

- **Geometry/parity script — ALL CLEAN:** 12 bars (table==baked y/h, y+h=230 zero baseline, band
  centring, fx/fw) · casing points/fxs/ys BYTE-EQUAL to line · 12 markers on line points, tips ==
  aria == table · both tick sets recompute from their scale formulas (±0.11) · target at
  secondary-95 exactly · all points in bounds · **dual-axis fit parity at 1180 + 560 (bar-centre
  == marker-x under fitOne's own maths, ≤0.6px)**.
- **Gate by import** (no `_DATAVIZ-GATE.md` write — fence): 0 blocking under stock AND proposed
  wiring; dv-line-011 manually asserted (polylines only).
- **Contrast maths:** quoted in decision 2; axis roles 6.10/6.42; target 13.01/8.68.
- **Render-verify per the runbook — RUN AND SEEN** (headless shell + fontconfig alias,
  `document.fonts.check` asserted): **1180 + 560** (viewBox pinned 1076/456 × 260 — labels
  computed 12px at both widths, endkey 700) · dark + table popover open (grey-outline card) ·
  high-contrast · filtered (line off ⇒ casing `visibility:hidden` asserted — the 07-23
  animation-vs-opacity lesson holds) · **JS-off on the REPO file** (static 580, no fit class, no
  tip — the honest unregistered state renders correctly). Live DOM asserts: marker + BAR popovers
  on keyboard focus · target toggle aria + variant group · table open/Esc/refocus · live fit
  parity 0.05–0.10px. PNGs in session outputs (agent self-verification only).
- **Census: 32, zero growth** — no strict fails, no census entries naming Chart-combo.
- Sentence case throughout; icons byte-copied library assets; composites-only type; radius via
  role token only.

## ★ Render-verify earned its keep (again)

The first target-ON render caught a REAL collision no mechanical check saw: the right-anchored
"Target 95%" label (Chart-line's anchor) landed on the endkey B + Dec marker — **the 95 target and
Dec's 95.4 nearly coincide in y, and the right edge is already the endkey + secondary-tick zone.**
Fix: the combo's target label anchors LEFT (x=50, data-fx=0), where the short early bars leave
clear air at every width (label baseline 82 vs Jan bar top 96.1 — y is fixed under fit).
Re-rendered + clearance asserted (922px @1180, 328px @560). **Wave note: on any chart with a
right-hand secondary axis, right-anchored overlay labels are contested space — anchor overlays
opposite the secondary axis.**

## Judged deltas (call them out loud)

1. **`.dv-axis2` class minted locally** (secondary rule, data/axis stroke) — the substring keeps it
   inside the gate's `dv-axis` regex so the rule's contrast IS checked (6.10/6.42). Snippet-local
   CSS, no type.css touch, no blast radius.
2. **Stage padding-right 32px** (vs the exemplar's 24): the suffixed right ticks ("100%") paint
   past the svg edge; the letter zone alone was too tight. Same clip-at-padding-box mechanism.
3. **Endkey B sits between the last marker and the right rule** (x 558.3, clears the rule by ~3px
   at 580; more at width) — tight-but-clean, render-verified. With target ON, B overlaps the
   dashed target line when the data coincide (ink 700 on a thin grey dash — legible, seen).
4. **Bars are popover focus stops** (tabindex 0 + aria-label) — extends the exemplar's
   marker-as-focus-stop posture to rects; same sub-24px receipt logic (read points, not click
   targets).
5. **Control CSS duplicated by copy from Chart-line** (toolbar/toggle-seg/legend/panel/tip ≈ 90
   lines) — the third chart file carrying it. **OBSERVED duplication accretion evidence** for a
   dataviz-controls partial or the quiet-utility family (ADR-0013 ruling 3: propose, don't
   promote — noted, not minted).
6. **Casing + line draw as one** (same pathLength/duration/easing — the casing must never lead its
   line); casing joins the dv-quiet/filter selectors via data-series-group, not class.

## Open Qs (Dave)

- **Q2 combo home** (top of receipt — loudest flag).
- Grouped-combo (2 bar series + line) — future variant; rides the bar lane's grouped promote
  (D-Q3) if wanted.
- Secondary-axis tick count posture (4 here) and whether the floating floor should ever be
  REQUIRED to include the target value — worked here by data (85 < 95 < 100).
- The a11y dim-caution remains OPEN programme-wide (controls never dim-only — honoured here
  verbatim from the exemplar recipe).

## Reconcile intel — shared-tree observation at wrap (~16:48)

`git status` at receipt time shows SIBLING LANES LIVE: Chart-bar + Chart-donut/sparkline sources
+ metas modified, gate reports + canon.css + showroom regenerated (someone ran a build mid-wave),
`reviews/RADIUS-CORNER-TUNER-2026-07-24-v2.html` untracked (another window's). **⚠ Untracked
`showroom/chart-combo.html` is NOT mine** — a sibling's showroom regen picked up my new
snippet+meta automatically. My lane wrote EXACTLY three paths: the snippet, the meta, this
receipt. Conductor: attribute the showroom pane to whichever lane ran the regen (it will
regenerate cleanly at absorb either way — and note the mid-wave build also rewrote
`_DATAVIZ-GATE.md`, so my file already appears in the shared gate report despite my import-only
discipline).

## ★ SIDE-QUEST — Dave's live ask in-lane (2026-07-24, post-receipt, VERBATIM absorbed)

> "this is interesting, could we try the css invert on the line rather than a halo. show me both
> in a review … This throughs up and interesting question about dark surfaces in light mode and
> how text shows up … This might happen on a section div how might we deal with this tokenisation
> … not a problem in dark mode, the standard rule it that dark in light isn't inverted in dark
> more, maybe some research is in order."

**Read as (reflected back in-chat before building):** (A) live compare — casing vs
`mix-blend-mode:difference` on the combo line; (B) text-on-locally-dark-surface tokenisation laid
out as RESEARCH. Nothing inscribed; Dave rules on the sheet.

**FENCE EXPANSION (his ask):** two additive files —
`reviews/COMBO-LINE-INVERT-2026-07-24-v1.html` + its generated `.REVIEW.html` (overlay via
`_make_review.py`). Render-verified light@1180 + dark@700, real font, SEEN. My lane total is now
FIVE paths (snippet · meta · receipt · sheet · sheet-REVIEW).

**Findings baked into the sheet (measured, quotable):**
- Difference-invert over the brand mid-tones lands on mid-tones: series-1→#89997D **1.73:1** ·
  series-2→#5BA3C5 1.80:1 · series-3→#A88387 1.37:1; only extremes work (page 21:1). The inverted
  line also stops being a TOKEN (colour = f(ground); dv-016/dv-017 can't resolve it; identity
  flips per ground and per mode). Casing is the only treatment the gates can see. REC = A2 casing.
- **★ THE SEAM (Q-B):** white text mechanically PASSES 4.5 on every dark-ish Apollo surface
  (series fills 4.61–5.26; ink panel 17.4) but **type26-013 blocks white type outside red** — the
  brand gate and the maths point at different inks. Tokenisation options sheeted: O1 scoped
  inverse-surface re-resolution (REC — the ADR-0014 classified-surface move; surface carries its
  ink slot the DV-D07 two-channel way) · O2 paired on-* tokens · O3 CSS invert/contrast-color()
  (rejected for text by the maths; track only). Gate consequence named: an inverse-surface
  carve-out to type26-013 + body text ON series fills stays prohibited (3.31–3.78 vs ink).
- Dave's mode rule held and demonstrated live: the dark panel stays dark in dark mode (per-mode
  surface values — no inversion of dark-in-light).
- Sheet self-catch: first render had `isolation:isolate` on the A3 specimen, which stopped the
  blend reaching the page (white-on-white page-side) — removed so the specimen tells the truth;
  re-rendered both modes.

**Conductor:** the sheet pair joins the reconcile (additive, no shared-file touches). Ruling lines
R-A/R-B/R-C at the sheet foot; if Dave rules R-B = O1, that's an ADR-shaped session (surface
classification + cascade), not an enact-window edit.

**★ R-A SOFT-RULED IN-LANE (Dave, 2026-07-24, verbatim): "okay the halo is fine for now, i love
to tweak so i might think of something else pal."** Read as: **A2 casing STANDS — provisional by
temperament, not contested** ("for now" = he reserves the tweak, his standing style). No snippet
change needed (casing is what's built). Ledger line, if the conductor inscribes: mark the casing
DAVE-SEEN-AND-ACCEPTED-PROVISIONAL, not RULED-FIRM — do not close the revisit door. **R-B
(tokenisation) + R-C (type26-013 carve-out) remain OPEN** — the sheet stays live for those.

*Rulings absorbed beyond the brief: the `fa29858` control constructions (single-cell segs ·
copy⇄tick · solid-arrow dropdown · literal `--control-h`) — consumed as canon, none re-ruled.*
