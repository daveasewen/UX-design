# Brief — "dark-mode-in-light-mode" (O1 architecture) + chart follow-ups

> **★ UPDATE 2026-07-24 PM (Opus solo) — DESIGN NOW RULED + INSCRIBED; only the MECHANISM BUILD remains.**
> Dave confirmed the O1 sub-decisions by number and ruled **DV-D10** (combo/line labelling) by eye on
> `reviews/COMBO-LABELLING-SOLUTIONS-2026-07-24-v1.html`. Records are on tattoos: **ADR-0014 addendum
> (Decisions 7+8)**, **DV-D10** in `_DATAVIZ-DECISIONS.md`, decision-graph fed, build **53/53 green**.
> ★ Correction verified: `type26-013` has **no running gate** (asserted-only) — the biting gate is
> **`dv-016`**; O1's gate work = **extend `data-surface` with `inverse` + fix dv-016's contrast base**,
> not "exempt white text". **The turnkey 5-step build spec is the `_LIVE-STATE` top delta** — open on
> that. The sections below are the original design reasoning (still valid; superseded only where the
> addendum/DV-D10 narrowed scope: combo end-key is DV-D10's lockups, NOT O1).

*Cut 2026-07-24 ~19:23 BST (date from `date`) by the Opus chart-conductor window, at Dave's
direction: "lets do it but it will probably needs its own sesh." Self-contained — a fresh window
should be able to open cold on this. Read `_LIVE-STATE` top delta + this file.*

---

## ★★ THE BIG ONE — "dark island in a light page re-resolves its own ink" (O1)

**Dave's framing, verbatim (2026-07-24):** *"is this a solid solution for all light-mode-on-dark
situations… essentially we need a dark-mode in Light-mode when the background is dark."* He arrived
independently at the general pattern — this is NOT a per-spot carve-out, it's a reusable mechanism.

### The problem
Text/graphics that sit on a **dark surface within a light-mode page** (a dark series fill, a dark
section div, a dark card) need **light ink** to be legible — but `type26-013` (BLOCKING brand gate:
*white type is red-only*) forbids it. Lane ③'s COMBO-LINE-INVERT sheet measured it: white text
mechanically PASSES 4.5:1 on every dark-ish Apollo surface (series fills 4.61–5.26, ink panel 17.4),
while page-ink on those same fills FAILS (3.31–3.78). So the maths and the brand gate point at
different inks. Point-token carve-outs patch one spot and fight the gate; the real fix generalises.

### The solution shape (O1 — RULED by Dave "do it", own session)
A **surface that declares itself dark and re-resolves the ink (and text roles) for its subtree** —
"dark-mode resolution, scoped to a light-mode island." Reusable for any dark background.

**★ KEY INSIGHT — this is NOT new architecture. It POPULATES AN EXISTING SLOT under ADR-0014.**
ADR-0014 already (a) classifies surfaces, (b) has the neutral DNA tier (semantic roles alias
`color/neutral/1–15` as SEMANTIC POSITIONS, and SC already remaps its anchor), and (c) carries
inverse resolution. "Dark island re-resolves its ink" = a **classified dark surface** that remaps
the neutral anchor locally — the same move SC's dark provisional already makes, scoped to a subtree
rather than a theme. Reference the ADR; do not duplicate. (memory: `reference-the-adr-dont-duplicate`.)

### What a real solution needs (the two load-bearing pieces — why it's a small ADR, not a quick win)
1. **A scoped dark-surface token/attribute** (e.g. `data-surface="dark"` or `.on-dark`) that within
   its subtree re-points `--ink` (+ text roles) to the light/inverse values via the ADR-0014
   classified-surface mechanism. Must work in BOTH modes: in dark mode the island stays dark (Dave's
   rule, demonstrated live on the combo sheet — *dark-in-light is NOT inverted again in dark mode*;
   per-mode surface values, no double inversion).
2. **Gate scope for `type26-013`** — the gate must EXEMPT light ink inside a declared-dark surface
   (a scoped exemption keyed on the surface classification, like `LEGACY_THEME_EXEMPTIONS` is scoped).
   Without this the gate correctly blocks the very thing we're minting. This is the new-surface-gate
   rule: wire the exemption's condition, don't just suppress.

### Deliver as a FIRST SLICE, then generalise
- **Slice (the session):** mint the scoped dark-surface classification + the gate scope, apply to
  the chart **in-fill text** that currently fails (stacked/grouped bar in-segment letter keys =
  page-ink on fills; donut letters-on-segments if resurrected; combo's B if it ever lands on a bar).
  Render-verify light+dark @2 widths (brand-gate change — DESERVES a look; render was owed all wave).
- **Generalise (flag):** roll the same classification to dark section divs / dark cards system-wide.
  That's the full O1; the slice proves the mechanism.

### Open sub-questions for the session (do not settle blind)
- Token shape: a new `text/on-dark` semantic ink slot, vs re-resolving the existing `--ink` under the
  classified surface (the ADR-0014-consistent move — RECOMMEND this, it's the "dark-mode" answer not
  a paired-token answer). COMBO-LINE-INVERT sheet labels these O1 (re-resolution, REC) vs O2 (paired
  on-* tokens). Dave's framing points squarely at O1.
- Does the classification also remap **borders/lines/RAG** inside the island, or ink only? (Probably
  ink + hairlines; RAG stays RAG. Decide with evidence.)
- Naming: `data-surface="dark"` (attribute, cascades cleanly, gate-readable) is the current front-runner.
- The COMBO-LINE-INVERT sheet's R-B (tokenisation) + R-C (type26-013 carve-out) are THIS. R-A (the
  line's page-casing) is already DAVE-SEEN-PROVISIONAL and unaffected.

### Evidence + prior art to read first
- `reviews/COMBO-LINE-INVERT-2026-07-24-v1.REVIEW.html` (Dave-seen; O1/O2/O3 with measured contrasts).
- Lane ③ receipt `notes/_receipts/2026-07-24-wave-lane3-combo.md` §SIDE-QUEST (the seam, measured).
- ADR-0014 (`docs/decisions/ADR-0014-per-theme-neutral-primitives-state-snap.md`) — the slot this fills.
- `type26-013` in the guidelines + its gate. Memory: `four-theme-architecture`, `theming-dna-adr-0014`.

---

## Chart follow-ups (smaller — could ride the same session or an enact window)

### ✅ DONE this window (already in the tree, uncommitted at brief-cut → in the wrap commit)
- **Popover-over-trigger FIXED** (`dv-behaviour.js` `tblToggle`): the table panel now anchors just
  BELOW its trigger button (measured via `getBoundingClientRect` vs the offset parent) instead of a
  brittle fixed `top:44px` that a title pushed the toolbar past. Applies to all 5 charts. Module now
  15,066 B (14.7 KB / 16). **Render-verify OWED** (Dave to eyeball a live pane). Build 53/53 green.

### PROPOSED — legend isolate/toggle redesign (Dave 2026-07-24, reflected back, AWAITING his confirm)
Split the legend row into two affordances (retires today's hidden shift/double-click isolate):
- **Click the label/entity → ISOLATE, radio-style** — solos that series; clicking another label
  moves the solo.
- **Click the swatch box → CHECKBOX** — toggles that one series on/off, additively.
- **Interplay:** isolate A (radio → just A) → click B's swatch (checkbox → A+B) → click C's label
  (radio → just C). Coherent: radio = set-to-one, checkbox = additive toggle.
- **Why it's flagged not built:** it's an a11y-real redesign — two roles per row, each needing ARIA
  (`role=radio`/`radiogroup` on labels, checkbox semantics on swatches) + keyboard (arrow between the
  radios, space toggles the checkbox). Current code: `dv-behaviour.js` `legendToggle`/`isolate`/`setSeries`
  (isolate is shift/dblclick today). **CONFIRM the model with Dave, then build + render-verify.**

### NOTE — the mini text ramp (no change needed; seam flagged)
Dave's rule holds and is applied: **T-D15** = `t-cm-ctl-12` medium/12 · `-14` medium/14 · `-16`
regular/16. Chart axis labels + toolbar buttons all sit on **12/500 (medium)** — correct at the 12
step. Wrinkle: charts use a PARALLEL composite set (`t-cm-chart-label`/`value` 12/500, `-key` 12/700)
rather than the `ctl-*` ramp; they agree at 12/500 so nothing's broken. **Optional later: unify the
two ramps into one** (or leave aligned). If a label ever READS as regular to Dave's eye, that's a
render check — the composite is 500.

---

## Model / gauge note
Cut at Opus, gauge 🟡 warming ~60% (Dave: "we're probably get warm right now"). Red-adjacent ⇒ next
reader re-verify the render/gate claims. The O1 session should open FRESH (Opus or a focused ADR
window) with render-verify working.
