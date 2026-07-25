# Brief — Legend prototype v5 (apply Dave's 5 review edits, 2026-07-25)

**Source:** Dave's 5 pins from the `reviews/LEGEND-ISOLATE-TOGGLE-PROTOTYPE-2026-07-24-v4.REVIEW.html` overlay export (this session).
**Output:** **v5** — `reviews/LEGEND-ISOLATE-TOGGLE-PROTOTYPE-2026-07-24-v5.html` (VERSION, don't overwrite v4), then regenerate `…v5.REVIEW.html` via `python3 knowledge/_review/_make_review.py <file>`.
**Verify:** render-verify light+dark @2 widths (1180/560) + states (a checkbox OFF, an isolate ACTIVE) per `knowledge/_RUNBOOK-render-verify.md`. Pipeline gotchas re-banked: sandbox `$HOME` **rotates between calls** + bash cap is **hard 45s** ⇒ download+libs+fonts+render in ONE call; alias **BOTH** font strings (`"Univers Next for HSBC"` + `"Univers Next HSBC"`); set `data-theme` via `add_init_script` on DOMContentLoaded (NOT after goto) or the 160ms theme cross-fade greys the shot.

## THE MODEL (reconciled — RESTORES v3's dual gesture)
v4 collapsed the two gestures into one isolate button; **Dave VETOED that** ("I can't check the swatches"). v5 restores the dual control:
- **Swatch = checkbox** — additive show/hide per series, independently operable. `role="checkbox"` + `aria-checked` + `tabindex="0"` + click and Space/Enter toggle that one series. Checked = filled square; unchecked/hidden = **hollow square + grey-primitive border**.
- **Label = isolate** — click shows ONLY that series (radio-feel); click the active one again, or Reset, restores all. (Resting-state a11y call is settled: exclusive toggle-buttons `aria-pressed`, not a radiogroup.)
- **Hover** = fade the OTHER series' bars/segments **and their letter keys** (keep v4's `.is-faded`, wired to legend items + `.dv-series`).
- **KEEP from v4:** square swatches (no shape-coding) · donut **Reset under the last legend item** + the radial-sweep intro (from the canon `data-cx/-cy/-ro/-ri/-a1/-a2` contract) · bar keys ranged LEFT / Reset right-inline · **no** strike-through, **no** "only"/"Showing only X" text · sr-only live region for AT.

## THE 5 EDITS
1. **Bar entry animation — animate the on-chart key (A/B/C) ALPHA in sync with each bar's grow.** Today the `text.dv-barkey` all fade at once (`dvFade`, no delay) while bars grow staggered (0,45,…495ms). Give each key an `animation-delay` matching its bar + a fade that tracks the grow, so the letter arrives as its bar settles. (Donut keys already alpha-in via the sweep — bar only.)
2. **Reset button states — "ref canon" (B-D4).** DEFAULT = **disabled**, styled per canon disabled: text = `text/on-disabled` **#9D9D9D light / #808080 dark**; border = `border/subtle` **#E1E1E1** (= `--line`). ENABLED = the other controls' resting look: **light border (`--line`) + dark text (`--ink`)**. Enable when any series is hidden (checkbox off) OR an isolate is active; disable again at "all shown".
3. **Off/hidden legend rows = RESTING, not muted.** The row keeps **light border (`--line`) + dark text (`--ink`)**. ONLY the **swatch** changes: hollow (transparent fill) + **grey-primitive border** = `--muted` (mono/7 `#626262` light / mono/9 `#9D9D9D` dark). ⚠ This **supersedes** the earlier ruling (first-pass point 5) that muted the whole item's border+text — the grey primitive now lives on the **swatch border only**.
4. **Restore the dual radio+checkbox.** Structure per row: `<li class="legrow">[swatch checkbox][isolate label button]</li>` (swatch OUTSIDE the isolate button so both are independently operable — a button can't nest an interactive checkbox). This is the direct fix for "I can't check the swatches".
5. **Donut `.seg` hover.** KEEP the per-button light-grey background hover; ADD **`.seg:hover { border-color: var(--ink) }`** so the whole container's outer border darkens to ink, matching the other controls. (Consider `:focus-within` too for keyboard parity.)

## WHY / ARC (so a cold reader has the reasoning, not just the values)
- v4 simplified to isolate-only on the read that "click a key → isolate + reset" implied one gesture. Dave's edits 3+4 show the intent was always **two** gestures: check individual series on/off (swatch) AND focus one (label). The vetoed simplification is the lesson — when an interpretation call is flagged and reversed, both beats are recorded (this brief + the spine).
- Off-state moved from "mute the whole item" → "resting item, hollow-grey swatch" because muting the text/border made hidden rows look disabled/unclickable; the swatch alone carries on/off, keeping every row fully legible + operable.
- Reset "ref canon" = stop inventing a disabled look; reuse B-D4's `text/on-disabled` + `border/subtle` so the control reads like the rest of the system.

## STILL OPEN (Dave)
- **ds-010** — fold the one-line `Chart-bar` `fill:var(--sc,…)` drop into the bar lane, OR fix now + rebuild (`_DS-IMPROVEMENTS.md`).
- **Legend NOT inscribed to canon** — v5 stays a review candidate; inscribe the model to `_DATAVIZ-DECISIONS`/ADR only after Dave signs off the fixed version.
- **Donut sweep × 16KB cap** — the animated sweep in CANON pushes `dv-behaviour.js` past the 16KB gate; the cap-fork (amend vs modularise per family) rides the donut lane.
- After sign-off, the legend redesign is the SHARED SERIAL (dv-behaviour legend logic) feeding the **donut + bar + combo** wave; line + sparkline are done.
