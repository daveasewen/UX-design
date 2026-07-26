# 2026-07-26 — Legend v5.x sign-off: the additive-isolate reversal + seg coherence (v5.4/v5.5 → DV-D11/12/13)

provenance: keen-vigilant-bohr · 2026-07-26
status: ruled — `knowledge/_proforma/_DATAVIZ-DECISIONS.md` DV-D11 · DV-D12 · DV-D13

*Main-queue session (Fable solo). Opened as "Dave's next batch on v5.3 → sign-off"; became the
session where the fade model REVERSED shape, gained the additive isolate, gained seg-numeric
coherence, and signed off — all in one sitting. Spine entry: `_LIVE-STATE.md` ⏱ LATEST 2026-07-26.
Ledger: DV-D11/12/13. Reference implementation: `reviews/LEGEND-ISOLATE-TOGGLE-PROTOTYPE-2026-07-24-v5.5.html`.*

## The arc, finding by finding

### 1 · The two v5.3 defaults didn't survive contact with Dave — and the reversal is the model
v5.3 (built 07-25, Amber-authored) shipped two agent-chosen defaults flagged vetoable: (a) the
swatch checkbox fully REMOVES at 0% while isolate ghosts at 12%; (b) hover suppressed during
isolate + any swatch toggle exits isolate. Asked to confirm, Dave rejected (a) outright ("retune —
checkbox also ghosts") and answered (b) with a spec that reframed the whole mode: *"On isolate mode
the checkboxes should be blank, with a border, and the check should add segments in this mode."*

**Why this matters recorded loud:** the v5.3 three-level ladder (full/ghost/gone) rested on a
distinction — *remove ≠ focus* — that Dave didn't want. His model has NO fully-gone state anywhere:
two levels only (full / ghost 12%), and isolate becomes an **additive focus set** — enter on one
series, the other checkboxes go blank, checking one ADDS it to the view. Both beats are in DV-D11
(the B-D7 pattern: a reversal inscribed as loudly as the original).

### 2 · "Let's try 1" — an ambiguous ruling handled by reflect-back + cheap build
Dave's hover answer was "lets try 1, it sounds interesting." Ambiguous (which "1"?). Rather than
block on clarification, the interpretation was reflected back in writing — hover FIRES during
isolate, read as an *add-preview* (a ghosted row lifts 12%→24% on hover) — flagged as vetoable, and
built. Dave's sign-off of the built behaviour is what settled it. Method note: for prototype-tier
choices, reflect-back + build + judge-by-eye beats a second clarifying round-trip; the reflect-back
is what keeps it honest (feedback-clarify-reflect-back satisfied without stalling).

### 3 · The implementation insight that made the additive isolate cheap
The key structural choice: `visible[]` (the outside-isolate checkbox state) is **never touched
during isolate** — the focus set is its own map, consulted via one `activeMap()` switch. Release
therefore restores the pre-isolate mix *by construction*, no snapshot machinery. The whole v5.4
delta is one state variable + one indirection. Flagged-open edge (in DV-D11): unchecking the SEED
series while others sit in the focus set leaves the isolate ring on a blank row.

### 4 · Seg coherence (v5.5): tooltip typed, centre figure follows the selection
Dave: the Value⇄Percent seg only visibly changing the centre figure read as confusing. Two-part
fix, his direction + one interpretation call:
- Tooltip carries ONLY the selected number-type. Mechanically free: `dv-behaviour.js` reads
  `data-tip` live at hover-time, so the seg just rewrites the attribute from
  `data-tip-value`/`data-tip-percent` — the canon layer needed no re-wire.
- Mid-build, Dave added "the figure in the middle should change dependent on what's selected."
  **Interpretation call:** "selected" = the LEGEND selection (not the seg — the seg already
  switched the centre). Centre recomputes over the active series; percent = share of the grand
  total (isolate Housing → 950 / 41%; add Savings → 1250 / 54%). Signed off as read.
- **Deliberate a11y asymmetry (agent call, Dave-visible, unruled):** `aria-label`s keep BOTH
  forms — a screen-reader user shouldn't lose data to a toggle they may not perceive. Rides the
  wave's a11y pass (DV-D13 ⚠).

### 5 · Verification method — numeric interaction checks in the render pipeline
New for this arc: Playwright drove the *interactions* and asserted computed opacities/text
numerically (14/14 on v5.4, 14/14 on v5.5: 0.12 ghost / 0.24 peek / blank-box aria states /
release-restores-mix / centre sums at every step), alongside the usual font-check + PNGs read.
Two pipeline potholes worth banking: (a) `FONTCONFIG_FILE` pointed at a rules-only conf REPLACES
the whole fontconfig → every glyph vanishes; use `~/.config/fontconfig/fonts.conf` (merge) per the
runbook. (b) The dv-tip rides `pointermove`/`focusin`, NOT `mouseover` — test hover via
`el.focus()` (segments carry tabindex) or a real pointermove; and Playwright's `.hover()` on arc
paths times out (bbox centre lands in the donut hole) — dispatch/focus instead.

## Resolved state
v5.5 signed off (*"good done, love this"*) = the legend model. DV-D11 (legend model) · DV-D12
(trapezoidal sweep easing, carried from v5.2) · DV-D13 (typed tooltip + selection-following
centre) inscribed; seed fed (81 nodes / 138 edges); build 55/55 GREEN post-inscription.
`_REVIEW-SIGNOFF.md` legend strand → ✅ LOCKED.

## Still open
The donut+bar+combo WAVE enacts DV-D11/12/13 into `dv-behaviour.js` + the chart snippets (next
window, conductor model). Riding the wave: ds-010 (bar `--sc` fill bug, Dave's open call — bar
lane) · DV-D13's aria asymmetry · DV-D11's seed-uncheck edge · the hit-area rule + gate rebuild
(separate sign-off, `notes/_briefs/2026-07-25-hit-area-rule-and-gate-proposal.md`, still pending).
The ruling batch (§C·2, items 8–22 + wave-1's 7) remains at Dave's appetite.
