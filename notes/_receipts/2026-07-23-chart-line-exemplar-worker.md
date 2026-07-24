# Worker receipt — Chart-line exemplar lane (Phase 1, chart-revisit)

*2026-07-23 ~22:05 BST (date from `date`) · FABLE WORKER, full budget, solo lane · brief:
`notes/_briefs/2026-07-23-chart-revisit-fable-brief.md` + conductor addendum + LIVE RULINGS ·
baseline certified by conductor: `8c0e742` (verified via `git log --oneline -1` at lane start) ·
**NO GIT — conductor commits the ONE reconcile.** Fences honoured: no writes to GOOD-MORNING /
_LIVE-STATE / _FUTURE-STATE / briefs / BAR-CHART-AUDIT / ledger spines.*

## Outcome — Phase 1 landed end-to-end, build 51→**53/53 GREEN**

The ADR-0015 behaviour layer + both mints + the Chart-line Layer-2, all gated, render-verified at
2 widths + dark + high-contrast + filtered + JS-off. **The one chart is ready for Dave's eyeball**
(showroom pane `showroom/chart-line.html` regenerated; review overlay rides it as standard).

## Files landed (worker-owned, per fences)

**NEW**
- `knowledge/canon/dv-behaviour.js` — THE behaviour source (ADR-0015): popover `dvTip` · fit
  reflow · table-view popover · legend-as-filter. **8,313 bytes of the 16,384 cap** (proforma
  whole-kit baseline was 9.9KB). One rAF-debounced resize listener; document-level delegated
  events; every module inside try/catch-shaped progressive enhancement; `window.__dvBehaviour`
  double-init guard. Tip node is JS-created and takes its type via composite class
  (`t-cm-chart-value`, T-D14 markup-class pattern).
- `knowledge/_validate_behaviour.py` + report `_BEHAVIOUR-GATE.md` — the ADR-0015 performance
  contract made executable: ≤16KB · banned setInterval/fetch/XHR/sendBeacon/WebSocket/EventSource ·
  DEF-003 boundary (`.style.transform` / `transform:scale` / `--hs`/`--ps` banned in JS) · exactly
  ONE rAF-debounced resize listener · members carry no external `<script src>`. Selftest = 9 bites
  (oversize, each banned class, 0 and 2 resize listeners, external src, clean pass).

**EXTENDED**
- `knowledge/gen_component_partials.py` — behaviour-partial pass (ADR-0015 rides the ADR-0013
  machinery): `$behaviour` blocks inject a whole provenance-commented `<script>` between
  `<!-- ===== AUTO-BEHAVIOUR … ===== -->` HTML-comment markers; same `--check` byte-exact sync,
  same contract checks (requires.vars / declarations / $manifestBinds). Selftest +5 behaviour
  cases (empty-pair match, idempotence, tamper teeth, payload shape).
- `knowledge/component-types.json` — new **`dataviz` group**: member Chart-line + the
  `dv-behaviour` contract ($manifestBinds = the DV-D07 roles; declarations = the Layer-2 hooks;
  $description records the Q5 quiet-utility posture + the per-capability-split-later wave note).
- `knowledge/_build_all.py` — 2 new steps (**51→53**): behaviour gate + its selftest, with their
  own failure branch.

**MINTS (both enacted per the LIVE RULINGS — the addendum's "no type mint" was lifted by DV-D08)**
- `knowledge/tokens/semantic-colour.json` — **DV-D07**: `data/axis` + `data/grid`, each TWO-CHANNEL
  (`color` per-mode aliased to the neutral ramp: axis 7L `#626262`/9D `#9D9D9D`, grid 12L
  `#E1E1E1`/6D `#484848` — the Q6 sheet values) + declared `alpha` slot `$value: 1` (modeless
  number; Dave's verbatim in the $note). Theme override sets deliberately untouched (ADR-0010
  declared-but-unset). `data/target` NOT minted (defers to Q4, per the ledger).
- `knowledge/canon/type.css` — **DV-D08** composites: `.t-cm-chart-label` 12/500 ·
  `.t-cm-chart-value` 12/500+tabular · `.t-cm-chart-key` 12/700+tabular (comment block carries the
  ruling + supersessions). **No `_type-bindings.json` entry needed — the blast-radius gate skips
  pure `.t-cm-*` composites by design (it guards APPENDED selectors; these bind via markup class
  only). Gate ran green.** If the conductor reads DV-D08's "register" line as requiring an entry
  anyway, say so and I'll add it — but the gate's own COMPOSITE regex is the mechanism ruling here.
- Unitless-alpha convention: `data/*/alpha` added to the shared no-px namespace in ALL THREE
  formatters (`gen_snippet_tokens._unitless` · `gen_theme_cascade.css_value` ·
  `gen_canon_tokens.UNITLESS`) — kept deliberately in lockstep, same as press-travel/darken.

**THE EXEMPLAR**
- `knowledge/snippets/Chart-line.reference.html` — full Layer-2: optional visible titles
  (`.dv-title`, bound `t-cm-section-label` — JUDGED, see below) · popover (`data-tip` on all 48
  markers, tabindex=0 + aria-label == tip == table) · fit (data-fx fractions on every x-positioned
  element; frame data-pl/pr/h 46/12/260; `.dv-fit-on` JS-on opt-in) · table-view popover (Dave's
  mock: surface card + elevation border/shadow recipe, aria-controls/expanded, region, Esc,
  focus-managed — replaces `<details>`) · legend-filter buttons (aria-pressed; off = dim +
  line-through) · high-contrast port (`data-contrast="high"` remap onto data/series-high-contrast,
  +demo toggle) · DV-D07 rebind (axis text/ticks + gridline attrs onto the roles) · DV-D08 rebind
  (ticks→chart-value, month labels+legend+toggles→chart-label, keys→chart-key). Kit geometry,
  cadence, draw motion untouched.
- `knowledge/components/chart-line.meta.json` — purpose/props/tokens/motion/responsive/a11y/
  antiPatterns/tokenValidation refreshed to match.
- `knowledge/_validate_snippets.py` — **infra fix (flag to conductor):** semantic resolver now
  handles modeless number leaves (the alpha slots) → unitless string, matching `_fmt`. Was
  "token not found in store" on any number-in-semantic-store.
- `knowledge/_validate_legacy_leak.py` — **infra fix (flag to conductor):** crashed
  (`int.upper()`) walking the alpha leaves; non-string leaves now skipped (can never be a colour).
- Regenerated: canon.css (DV-D07 vars in the spine, 511 root vars) · theme cascade · showroom
  (65 pages) · gate reports.

## Verification (all run this lane, self-verify checklist worked through)

- **`_build_all.py` = 53/53 GREEN** (was 51; +behaviour gate + selftest). All selftests wired + passing.
- **DataViz gate**: Chart-line 0 blocking / **16 advisory — ALL the gridline decorative reads**
  (`#E1E1E1` 1.31:1 L · `#484848` 1.90:1 D), which is DV-D07 working as ruled (quiet chrome,
  1.4.11-exempt, gate's own posture says gridline contrast is advisory by design). No grid
  contrastPair declared in the manifest for the same reason. `--selftest` ✅.
- **Geometry/parity script** (mechanical): 2 figures · 4 polylines · 48 markers — table→y recompute
  == baked ys == polyline points (±0.15) · data-fx→X == baked x == data-x0 · tip == aria == table
  values · all points in plot bounds. ALL CLEAN.
- **Contrast maths**: axis 6.10:1 L / 6.42:1 D (role, blocking-clean) · series ≥3.31:1 both modes ·
  HC series ≥6.40:1 · grid 1.31/1.90 (decorative).
- **Render-verify per `_RUNBOOK-render-verify.md` — RUN AND SEEN** (headless shell + fontconfig
  alias, `document.fonts.check` asserted true): **1400 + 840 widths** (viewBox pinned 1:1 at
  1328/768; label computed 12px/500 at BOTH widths — text does not scale; key 700) · table popover
  open (matches the mock) · **dark mode** (grey-outline card, no dark-on-dark) · high-contrast ·
  filtered state · **JS-off** (baked viewBox 580×260, no fit class, no tip node — DV-D02 static
  answer intact). PNGs in the session outputs; not repo artefacts.
- **Live DOM behaviour** (headless): popover shows on keyboard focus ("Jan: 82") · table panel
  opens (aria-expanded, label swap, focus→panel) · Esc closes + refocuses toggle · legend toggle
  aria-pressed + series hidden.
- **★ RENDER-VERIFY EARNED ITS KEEP:** the filtered-state render caught markers still painted
  after legend-off — the entry animation (`dvFade` fill:both) **outranks inline opacity**. Fixed:
  filter sets `visibility` too (transitioned, so the fade still plays); re-tested live
  (visibility:hidden confirmed), rebuilt green. A mechanical check would never have seen this.
- Census/radius/coverage/type-blast all green inside the 53 (census unmoved; no press-shaped
  locals added; radius strict via role token only).

## Judged deltas (call them out loud)

1. **Title composite = `t-cm-section-label` (20/500)** — DV-D08 covers the 12px floor only; no
   title rung exists and minting one is beyond the ladder ruling. Existing composite, no new type.
   If Dave wants a dedicated chart-title rung it joins Q7's subtitle question.
2. **Month labels moved 14→12** (t-cm-caption → t-cm-chart-label): DV-D08 names "labels" at the
   12 floor; the 14px was worker-D's promotion-time bind, superseded. Attribute-the-diff: this is
   a RULING enactment, not drift.
3. **Table text stays `t-cm-legal` 12/400** — read DV-D08's "values" as ON-CHART text (labels ·
   axis · legend · values); the table is the tabular truth surface, not chart canvas. Flag if the
   ladder was meant to reach it.
4. **svg role img → group** — markers are now focusable; role=img would make them presentational
   to AT. aria-label kept on the svg; manifest requiredAria updated (role="status" removed from
   the STATIC contract — the tip node is runtime-created; noted in $note).
5. **Markers = focus stops at sub-24px geometry** — they are read/focus points (popover), not
   click targets; pointer reads ride document-level pointermove. Receipted vs the 24px target-size
   posture.
6. **JS-off fallback = fixed-580 + scroll** (not baked-fluid): progressive enhancement per
   ADR-0015; the alternative (viewBox scaling) is DV-D02's banned physics.
7. **Anchored-overlay recipe reused** for tip + table panel (background/default + elevation/
   functional + elevation/border) — accretion evidence for the standing anchored-overlay family
   (~7 files, now +1); did NOT mint a partial (ADR-0013 ruling 3: propose, don't promote).

## The manipulation-menu sheet (Phase-1 deliverable #2)

`reviews/DATA-MANIPULATION-MENU-2026-07-23-v1.html` — 11 numbered candidates + the confirmed
Layer-2 row + a paste-ready ruling line; REC chips on 1 (isolate = Q3) · 2 (hover highlight) ·
3 (sortable table). Render-verified light 1180 + dark 700, real font. Comment overlay omitted
(one-line rulings, not pixel judgments) — noted in the sheet header, flag if wanted.

## Sixth refinement + ★ NEXT-WINDOW QUEUE (Dave, late window — gauge RED, triaged live)

- **LANDED NOW — H-stack head (Dave: "all the controls on the same line as the title… switch to
  V-stack when we run out of space"):** title + ALL controls (seg view · overlays · CSV · table
  toggle) = ONE `.dv-head` flex row, `justify-content:space-between`; controls wrap to their own
  row under the title purely by flex-wrap (no JS, no breakpoint). Verified 1400 (inline) + 700
  (wrapped). Old `.dv-toolbar` removed. Table-panel anchor (top:44px) unreviewed against the
  wrapped head — eyeball note.
- **ANSWERED FROM THE REPO — "do we have atoms for the button lock-up contents?":** NO standalone
  quiet-toolbar-control atom exists. Nearest kin: the segmented-control PATTERN in View-options
  (sliding `.ind`), Tab-bar, Table (`.seg button`, registered type binding); Button = B-D7 press
  family, deliberately NOT consumed (Q5). The exemplar's `.dv-vt`/`.dv-seg` are hand-rolled
  cousins = OBSERVED duplication evidence (ADR-0013 ruling 3 accretion candidate: quiet-utility
  control family).
- **QUEUED next window (Dave's picks, verbatim intents):**
  1. **Atoms compare sheet** — live side-by-side (visual-compare doctrine): `.dv-vt`/`.dv-seg` vs
     View-options `.seg` / Tab-bar / demo-controls; Dave rules whether the chart controls consume
     the seg atom language or a quiet-utility family gets minted.
  2. **★ Mini type ramps** — Dave: *"I think we might have mini ramps for some items like buttons
     and labels, from 12-16 or maybe 20."* Type-architecture exploration (T-D15-flavoured; joins
     the PARKED 12–20 chart mini-ramp in `_FUTURE-STATE` + the curve-snapped-type riff).
     PROPOSAL SHEET only — no mints without his ruling.

## ★ DIVVY PLAN proposed for the wave (Dave asked for routing; effort knob = HIS, manual)

**NEW OBSERVED FACT (Dave, 2026-07-23 late): effort IS manually selectable in Cowork** — supersedes
the routing-audit #8 "no effort knob" observation; conductor should amend `MODEL-ROUTING.md` §Fable-era
notes (outside this worker's fence). Ratified split, Dave's knob per session:
- Lane ① bar+scatter (D-Q3 promote · DV-D09 defaults · B4 fit) — **Fable · medium** (pattern-following).
- Lane ② donut+sparkline — **Fable · medium**.
- Lane ③ combo (net-new dual-axis) — **Fable · high** (the one real design problem).
- Conductor (reconcile + serials + ONE commit) — **Opus · high**.
- Compare-sheet + mini-ramps solo (parallel-safe: reviews/ + notes only) — **Opus · high**.
Lane briefs must carry this session's SIX refinements as canon: enlarged markers · shaped legend
swatches · AA off-state (hollow border + axis-grey) · line-end letter keys (+ stage letter zone) ·
seg-view + per-view additive overlays · H-stack head with flex-wrap V-fallback.

## Open Qs / for the conductor

- **Q2–5, 7 remain Dave's** (combo home · legend isolate gesture · manipulation menu picks ·
  quiet-pressable confirm · subtitle slot). The exemplar builds NONE of the menu items beyond the
  confirmed set — menu artefact: see below.
- The two gate infra fixes (+`_validate_snippets` resolver, `_validate_legacy_leak` guard) are
  worker-judged necessities for the ruled token shape — review in reconcile.
- Advisory count: the 16 gridline advisories are permanent-by-design under DV-D07; if the noise
  bothers the report, a decorative-class suppression in the gate is a conductor call, not mine.
- Wave note in the registry $description: hook contract is the LINE set; sparkline/donut lanes may
  need a per-capability split — from observed need, not now.
- Playwright/fonts pipeline re-stood per runbook in this sandbox (fresh env) — all steps behaved
  as documented, incl. the expected host-validation exit.

---

## ★ RULING ABSORBED MID-FLIGHT — the manipulation menu (Dave, 2026-07-23 evening, VERBATIM)

> "really like all of these these suggestions, make sure that all of these suggestions but lets be
> wary of Ally [a11y], the 'dimmed' technique might be the wrong move, maybe, I'm not sure it might
> be okay for isolating data but when the legend acts as buttons we might have an issue here. Do as
> you hav esuggested and we can review and maybe make changes, and I might have to take advice
> sometime Ally decisions can be quite nuanced. But I'd really like to see this all in action"

**Read as (reflected back in-chat before enacting):** all 11 menu items RULED IN across the
programme; Q3 isolate = yes (item 1). A11y caution absorbed as a DESIGN CONSTRAINT, not a ruling:
**controls never signal state by dimming alone — a still-operable legend button keeps the AA text
floor (the ADR-0014 inactive ≠ disabled principle); dimming stays legitimate on the DATA layer**
(isolate/highlight emphasis). Marked OPEN — Dave may take advice; do NOT inscribe as settled.

**Enacted this window (line-shaped set, all verified live + rendered):**
- **1 Isolate** — shift-click / double-click a legend row solos the series (Shift+Enter = keyboard
  path); same gesture restores. **2 Highlight** — hover/focus on legend row or marker dims the
  OTHER series to .25 (`.dv-quiet`, !important outranks the entry animation); pointer + keyboard
  parity. **6 Year to date · 7 Target line · 9 Last year** — BAKED VARIANT GROUPS
  (`data-dv-view`, nested so target/ghost retire with the discrete scale): geometry is
  generation-time, behaviour only toggles — the method's answer to "deeper manipulation" without
  runtime chart math. Cumulative axis re-ticks 0/400/800/1200; table mirrors ALL of it (Last year +
  Year to date columns; † flags above-target rows). **10 Copy CSV** — serialises the figure's real
  table, clipboard + button feedback, no network.
- **A11y off-state (Dave refined in-session, supersedes the strike-through draft — "hollowed
  swatch and changing the colour on the swatch and the text to a grey that passes contrast
  ratios"):** legend OFF = HOLLOW swatch (transparent fill + 2px inset ring) with ring, letter-key
  and label all in the **data/axis grey** (6.10:1 L / 6.42:1 D — existing DV-D07 role, no new
  token; the key's resting .6 dim lifts to 1 in this state or it would sink below the floor; one
  scoped !important to beat the swatch's inline series background). Verified computed
  (#626262 text · no decoration · transparent bg · key opacity 1) + rendered.
  **Second refinement same session (Dave): hollow = a real BORDER on the swatch (2px, inside the
  12px border-box), not a background trick; and legend swatches now CARRY THE MARKER SHAPES**
  (circle A · square B · diamond C — `.sw-circle/.sw-square/.sw-diamond`; circle = the 50% idiom,
  diamond = 8px rotated 45°, on-grid). Third non-colour channel in the legend, mirrored from the
  chart. Rendered + verified; wave lanes should mirror shapes in their legends too.
  Still OPEN for his adviser; rebuild after the changes: 53/53 green.
- **Fifth refinement (Dave, two messages read together — "year to date is a view whereas the other
  two are additive so the interaction of states needs work" + "unless all three are supposed to be
  additive toggles and it just doesn't work"): the STATE MODEL fixed.** The scale pair is a
  SEGMENTED VIEW SWITCH (`.dv-seg`, Monthly ⇄ Year to date, exclusive, active = filled — reads as
  a different control class from the outline additive toggles); the overlays are FULLY ADDITIVE —
  **each view carries its OWN baked overlay variants** (year-to-date target = the 90-a-month RAMP
  to 1080, straight line; last year = its running total), one toggle governs both copies, so
  Target/Last-year now WORK in the year-to-date view instead of silently dying. Nothing disables.
  Ink letters confirmed fine by Dave ("they don't have to be in the right colour"). `viewSwap`
  replaced by `segView` in dv-behaviour (13,266 bytes of 16K, gate green). Verified live (matrix:
  overlays on → view flip both ways) + rendered both states. Judged: the cumulative last-year
  column is derivable (running sum of the table's Last-year column) and was NOT added to the
  table — flag if the truth-surface reading should be stricter. Wave note: the seg-view +
  per-view-overlay pattern is the state-model canon for any chart carrying scale views.
- **Fourth refinement (Dave): line-end LETTER KEYS** — A/B/C at each line's end (multi-series),
  `t-cm-chart-key` (DV-D08 700 emphasis), **ink not series hue** (12px text in series colours sits
  below the AA floor on dark — consistent with the day's a11y line; adjacency + shape + legend do
  the tying, flag if Dave wants them series-coloured anyway). They carry `data-series-group` so
  filter/isolate/highlight take them along (verified live); fade in as the draw completes; ride
  the fit (`data-fx=1 dx=12`). **Layout catch:** the stage scroll-container clipped them at the
  svg edge → `.dv-stage` gains `padding-right:24px` (the letter zone; clip is at the padding box;
  fit auto-recomputes). Rendered + rebuilt green. Wave lanes: end-keys join the lock-up pattern.
- **Third refinement (Dave): markers ENLARGED so the shapes read** — circle r4.2→**5.5** · square
  8.4→**11** · diamond ±4.9→**±6.5** (~×1.3, page-stroke 2.5 unchanged; 60 shapes recomputed
  around their unchanged centres, so all geometry/parity holds). **SUPERSEDES the observed kit
  marker sizes** — deliberate Dave ruling, not drift; wave lanes (scatter especially) should adopt
  the enlarged family and the proforma stays untouched as the historical record. Rendered +
  rebuilt: 53/53 green.
- **`data/target` MINTED** (DV-D07 two-channel pattern): colour neutral/5 L `#313131` /
  neutral/10 D `#B7B7B7` + alpha slot 1.0 — **values agent-PROPOSED (derivation governance), Dave
  re-dials**; dash = the non-colour channel. Contrast 12.4:1 L / 9.0:1 D, pair declared.
- dv-behaviour now **12,733 bytes (12.4 KB of 16)** — gate green; build re-run **53/53 GREEN**;
  projection 0-drift; new-variant parity scripted clean (cumsum ✓ scales ✓ target-y ✓ tips ✓ flags ✓);
  renders seen (target+ghost · cumulative · isolated · highlight).

**Rides the WAVE (per the same ruling — add to the lane briefs):** 3/4 sort (bar/column lanes) ·
5 value⇄% (donut + stacked) · 8 brush (scatter/line — needs its keyboard design before build) ·
11 annotate (EDIT-MODE adjacent — placement decision rides the wave divvy). The isolate/highlight/
CSV/variant modules are already in dv-behaviour — wave lanes get them by carrying the hooks.

*Other rulings absorbed: none beyond the brief's LIVE RULINGS block (DV-D07 · DV-D08 · DV-D09
noted for the wave · B1/D-Q3 wave scope · ADR-0015).*
