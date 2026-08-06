# Proposal — foundational hit-area rule + gate tightening (2026-07-25)

**Status: PENDING DAVE SIGN-OFF.** Nothing here is inscribed or wired yet. This is the spec that
becomes execution on your nod (Opus scopes once → enact). Source: Dave's v5.1 ask —
*"check that all controls follow the hit-area principle — this is foundational, we can make mistakes
on this, everything interactable must have this."*

## What v5.1 already did (enacting the EXISTING rule — no new ruling needed)
The 44 target is already canon (aid-009: HSBC default 44×44, min-exception 24×24, WCAG 2.5.8/2.5.5).
v5.1 enacted it on surfaces that were missed:
- Toolbar `.dv-vt` / `.dv-tbl-toggle` (were 32px, no target) → invisible `::before` 44 expander.
  **Canon gap — propagated to the 4 toolbar snippets** `Chart-{bar,combo,donut,line}.reference.html`.
  Build green (53/53); the a11y gate already treats a `::before` expander as satisfying the target.
- Demo-chrome buttons + BOTH legend swatches (bar + donut) present **44** — Dave ruled 2026-07-25 the
  swatch is **component-invariant** (same hit area regardless of layout; no 2.5.8 dense-case downsizing).
  The horizontal bar rows are spaced (`.lg.bar` gap) so the 44 targets tile. Prototype only.

## The two GATE BLIND SPOTS this surfaced (why "wire a gate" is real)
`_validate_a11y.py` today does NOT catch the toolbar at all — it passed only by omission:
1. **Selector allowlist.** It flags targets only for a hardcoded `CTRL` list
   (`button`, `a.<class>`, `.x/.close/.clear/.trigger/.handle/.page/.step`). `.dv-vt`,
   `.dv-tbl-toggle`, and `summary` are **not** in it → never checked.
2. **Literal-px only.** It reads `width:Npx` + `height:Npx`. `.dv-vt{height:var(--control-h)}`
   (32 via a variable) is invisible to the regex.
3. **44 is advisory, not blocking.** Only `<24` fails the build; `24–43` is a warning. So a 32px
   control is a silent warning at most.

## Proposed RULE (candidate text — for the a11y guideline / _DATAVIZ-DECISIONS)
> *Every interactive **control** presents a target ≥ `target/min` (44 HSBC default; 24 the WCAG 2.5.8
> dense-case floor with an exception out) — met by the visible box or the canon invisible `::before`
> expander. **Data marks are held to the 24×24 dense-case MINIMUM** ⚠ SUPERSEDED-CORRECTION #116 (`s116-D1`, Dave): they are exempt from the **44** control target, NOT from the check. The recommendation below ("no min floor") was NOT taken. ~~EXEMPT~~: a chart mark's target is its data geometry, and its accessible
> path is keyboard focus + the table view + the tooltip (all already wired). A control is any
> `button`, `summary`, `a[href]`, or `[role=button|checkbox|switch|tab|option]`; a data mark is any
> `.dv-series` / `.dv-marker` / dataviz `rect|path` carrying `data-series-group`.*
>
> *A component’s target is **invariant across layout** — don’t invoke the 2.5.8 dense-case
> exception to shrink a control that presents 44 elsewhere (Dave 2026-07-25, the bar/donut swatch).*

## Proposed GATE tightening (on sign-off)
Redesign `_validate_a11y.py` target check to be **markup-driven, not selector-allowlist**:
- Enumerate interactive elements from the MARKUP (the control set above), minus the data-mark set.
- For each, require EITHER a declared box ≥44 OR a `::before/::after` hit-expander on its selector
  OR a claimed 2.5.8 exception. Promote **44 to BLOCKING for controls**; keep `<24` blocking; keep
  the `::before`-exemption (static CSS can't size the expander — the render axis owns that).
- Ship a selftest (bite-test) as a build step, per "every new gate ships one AND wires it."
- Scope the glob to `snippets/*.reference.html` (+ proforma) as today.

## Open sub-questions for you
1. **Data marks exempt — confirm?** (Recommend: yes.) And **a min floor for very small marks**
   (e.g. thin donut slices / <8px bars), or none? (Recommend: none — geometry + keyboard + table
   is the equivalent path; a min floor distorts the chart.)
2. **Sparkline discrepancy (repo vs brief).** The brief said "all 5"; the repo has the `.dv-vt`
   toolbar in **4** files. Sparkline uses a native `<details>/<summary>` "View as table" whose
   `summary` is an interactive control at ~text height — **not** yet ≥44, and a different mechanism
   (a `summary` can't take the same `::before` cleanly; it needs padding or a wrapping target).
   Fold it into this same ruling? (Recommend: yes — it's the same principle, different fix.)
3. **Scope of enactment.** Just dataviz controls now, or sweep the whole **75**-snippet library (67 was STALE — measured 75 at #116, `s116-D3`) for
   allowlist-missed controls in the same pass? (Recommend: sweep — foundational.)

## 2026-08-06 #114 (Dave) — addendum
Expander applied to the 8 <24-floor offenders. Chart tooltip trigger-points are a LESSER concern —
the table fallback always exists, making a11y rulings there more nuanced. The 44-promote half was **RULED THE SAME SESSION** by `s114-D6`
(*"Promoting 44 to blocking for controls, good"*), ordered AFTER `s114-D5` lands — this line's
earlier "remains UNRULED" was STALE and is corrected at #116.

## On sign-off, the enactment (one Sonnet-to-spec session)
Inscribe the rule (a11y guideline + `_DATAVIZ-DECISIONS` for the mark exemption) → rebuild the gate
markup-driven + selftest + wire into `_build_all.py` → run it → fix any newly-surfaced controls →
build green → feed the decision-graph seed same hour. Legend model inscribes in the same beat once
you sign off the v5.1 render.

## 2026-08-06 #116 — ENACTED (`s114-D5` / `s116-D1` / `s116-D2` / `s116-D3`)

**The gate half is BUILT.** `_validate_a11y.py` no longer measures CSS selector text: the
measurement engine is `knowledge/_a11y_target.py` — a real element tree, a subject-aware
cascade and resolved custom properties. It enumerates controls from the MARKUP, so the six
PHANTOM failures and the `axs-003` detector quirk close together, as one cause. Measured on the
library: **446 controls + 201 focusable data marks across 75 snippets**, 0 failures.

**What the rebuild also killed:** the old blanket `::before` exemption. An expander's
`min-width:var(--hit,44px)` is a NUMBER once var() resolves, so expanders are now MEASURED.
That converted 30-odd silent "NOT MEASURED" passes into honest 36×36 / 24×24 warnings.

**⚠ THE 44-PROMOTE IS BIGGER THAN IT LOOKED.** `s114-D6` is now unblocked, but the sweep
measures **72 controls in the 24–43 band**, not six. Flipping `CONTROL_TIER_44` to `"fail"`
without clearing them is a gate that fails on the library it governs. That is a remediation
lane for Dave to scope, not a flag flip.

**Sub-24 data marks (the OWED measurement, `s116-D1`): 107**, across 6 snippets —
`Chart-line` 60 · `Chart-butterfly-h` 12 · `Chart-combo` 12 · `Chart-stacked-area` 12 ·
`Chart-bar` 6 · `Chart-butterfly-v` 5. Not waived, not remedied: Dave's call.

**Scope boundary, declared:** form FIELDS (`input`/`textarea`/`select`) are outside the ruled
control set and are UNSWEPT — sweeping them re-created the phantom shape (every `width:100%`
field read as 0px, every visually-hidden native checkbox as 0×0). UNSWEPT is not clean.
