# Fitness-for-purpose test — Tabs

**Question:** can the knowledge base actually drive a good, compliant component, and where does it fall short? **Method:** build Tabs twice — Route B from the KB *only* (gap-logged live), Route A unconstrained (the quality ceiling) — then critique both and measure the delta. Files in `knowledge/_fitness-test/`. Date: 2026-06-19.

## Verdict

**The KB drives a structurally correct, accessible-in-light-mode component — and a dark-mode failure.** Following the tokens faithfully (Route B) produces Tabs whose label and selected indicator are **invisible in dark mode (1.0:1 contrast)**. Everything that makes a component feel finished — focus indicator, geometry, motion, type detail — the KB does not supply; in Route B it is ~90% my invention. The correctness scaffolding (ARIA, SC list, token resolution, and — genuinely impressive — the KB flagging its *own* P3 defect and shipping the `tabs/*` fix) is real and valuable. But "passes our integrity gate" and "is usable" turned out to be different things, and that gap is the most important result.

## Accessibility audit (WCAG 2.2 AA) — measured

Contrast ratios computed from the actual token values:

| Element | Route B (KB-only) | Route A (unconstrained) | Need |
|---|---|---|---|
| Tab label — light | #333 on #FFF → **12.6:1 ✅** | #5b5b5b on #FFF → **6.8:1 ✅** | 4.5:1 |
| Tab label — **dark** | #FFF on #FFF → **1.0:1 🔴 FAIL** | #a9a9ad on #161617 → **7.7:1 ✅** | 4.5:1 |
| Selected indicator — light | #DB0011 on #FFF → 5.2:1 ✅ | #DB0011 on #FFF → 5.2:1 ✅ | 3:1 |
| Selected indicator — **dark** | #FFF on #FFF → **1.0:1 🔴 FAIL** | #DB0011 (core red) on #161617 → 3.46:1 ✅ | 3:1 |
| Focus indicator | **none defined 🔴** (invented) | #005fcc/#4d9fff → 6.0/6.7:1 ✅ | 3:1 |

Other AA dimensions: both pass **2.5.8 Target Size** (44px), **2.1.1 Keyboard**, **4.1.2 Name/Role/Value** (correct `tablist/tab/tabpanel` + roving tabindex from the meta). **2.4.7 Focus Visible** is only met because I invented a focus ring — the KB defines none.

**Bottom line:** Route B fails 1.4.3 and 1.4.11 in dark mode and can only meet 2.4.7 by guesswork. Route A passes all of the above in both themes.

## Design critique — A vs B

| Dimension | Route B (KB-only) | Route A (ceiling) |
|---|---|---|
| First impression | Reads as an unstyled default; flat, no depth | Finished, branded, considered |
| Visual hierarchy | Selected = colour only (weight not specified) | Selected = colour **+** weight + sliding indicator |
| Motion | None (KB has no motion guidance) | Indicator slides; panel fades; honours reduced-motion |
| States | hover/pressed only; no disabled, no focus design | hover/pressed/selected/disabled + designed focus |
| Dark mode | **Broken** (white-on-white) | Real raised dark surface, lightened-red indicator keeps brand |
| Geometry | All guessed (height, padding, indicator/track widths, gaps) | Considered rhythm (48px, 20px pad, 3px indicator) |
| Richness | Plain labels | Count badge, polished overflow menu w/ keyboard nav |

**The delta = the design judgment the KB doesn't hold.** Sitting them side by side, the distance between "technically correct" and "would ship" is almost entirely craft the knowledge base has no representation for.

## What the KB needs — prioritised fixes

1. **🔴 Fix the dark token values, and make the dark-mode audit contrast-aware.** `tabs/active`, `tabs/background`, `tabs/standard-border`, `tabs/overflow-border` all resolve to `#FFFFFF` in dark — invisible UI, not merely "flat". Two actions: (a) correct these dark values (and sweep the other 43 flat semantic tokens for the same defect); (b) upgrade `_build_dark_mode_audit.py` to check *resolved contrast* (text vs its surface) — today it only flags raw-primitive bindings and rates a token "clean" if it merely *has* a dark value, even when that value is wrong. A token can be internally valid and still unusable.
2. **🔴 Add a focus-indicator standard to the KB.** No token, no guideline, no spec — yet every interactive component is graded against 2.4.7 / 2.4.11. Add a `focus/*` token (ring colour/width/offset, mode-aware) and a short `guidelines/focus-indicators.md`. Systemic: this gap affects all 32 components, not just Tabs.
3. **🟡 Give the meta schema a geometry block.** Metas carry colour bindings but **no measurements** — height, padding (which token), indicator/border widths, gap. Add a `dimensions`/`layout` object so a generator isn't forced to guess every size. This is the single biggest "had to invent" category.
4. **🟡 Ingest motion guidance + add transition tokens.** Nothing in the KB covers timing/easing or reduced-motion. Add a motion foundation doc and `motion/*` tokens.
5. **🟡 Fix token data-quality nits:** `typography/font-weight` values are unmapped strings (`"medium"` → needs a numeric/`font-weight`), `letter-spacing/font-5` is empty, and the proprietary font has no fallback stack recorded. (NB: `border-radius/default: null` is **not** a nit — it's correct; see #8.)
8. **🟡 Operationalize the "angular" brand rule.** `brand-principles.md` states the brand is angular (90°/45°), and `border-radius/default` is intentionally `null` — but neither is expressed as a concrete component constraint, so a builder doesn't connect them. Evidence it's a real gap: **both** my builds got it wrong — Route B's gap log mis-flagged the null radius as missing data, and Route A (unconstrained, full design judgement) added rounded corners until Dave caught it. Fix: an explicit rule/anti-pattern ("components use square corners; do not add border-radius unless a future rounded mode is adopted") that surfaces in the meta or a shared design-rules doc. **Exemptions (Dave):** Badge (fully round) and Avatar (round) are the only components exempt from the angular rule — the rule must encode its own exceptions. Also caught in review: selection must not change type weight (causes width jump) — capture as a states rule.
6. **🟡 Fix the guideline mapping + add the overflow pattern.** `horizontal-scroll.md` is mapped to Tabs but is **carousel** guidance, not the tab-overflow-dropdown pattern. Correct the xref map and capture real overflow guidance (breakpoint, collapse count, menu a11y).
7. **🟢 Complete the `tabs/*` group:** it has active/background/border but no hover/pressed surface tokens, so states fall back to `tertiary/*` (also flat in dark).

## Meta-findings — about our own tooling

- **The integrity gate passed a component that's broken in dark mode.** Internal consistency (references resolve, schema valid) is necessary but not sufficient; it says nothing about whether resolved values are *usable*. Worth stating plainly in the README so we don't over-trust a green gate.
- **The dark-mode audit's model is too shallow.** "Binds a primitive" is one failure mode; "binds a semantic token whose dark value is wrong" is another, and the current audit would rate Tabs **clean** once rewired to `tabs/*` — despite it being invisible. Fix #1b addresses this.
- **The confidence layer earned its keep:** the meta's own `tokenValidation` predicted the dark-mode problem in prose. We had the warning; what we lacked was the severity, which only building surfaced.

## So, is the project on track?

Yes — but with a sharpened definition of "done." The KB is a strong **correctness and provenance** layer and a genuinely useful **migration-safety** layer. It is **not yet** a layer that can drive *shippable* output, because it holds almost none of the craft (focus, geometry, motion, considered dark values) that separates correct from good. That's a tractable, well-defined backlog (the seven fixes above), not a redesign. The most valuable next step after these fixes is to **re-run this exact test** and watch the A–B gap shrink — that, not another derived view, is the real progress metric.

---

## Re-run #1 — gap closure measured (2026-06-19, after fixes #1–#4)

The re-run measures the A–B gap by the only thing that matters: **for each gap that forced invention in `route-b-gap-log.md`, can the KB now supply a concrete answer?** Each closure below was verified live against the current stores (`query.py "Tabs"`, token resolution, schema-valid build), not asserted.

**The four structural blockers — the categories that separated "correct" from "shippable" — are all closed:**

| Gap (Route B) | Severity then | State now | Where |
|---|---|---|---|
| Dark surface = white-on-white (1.0:1, fails 1.4.3/1.4.11) | 🔴 WCAG fail | **Closed** — `tabs/*` dark reconciled to canon (`#1D1D1D`/`#474747`); dark-mode audit now contrast-aware | fix #1 (yesterday) |
| Focus-ring spec — nothing, anywhere | 🔴 invented | **Closed** — `focus/ring` (mode-aware, canon blue, ≥3:1 verified) + `layout/focus` width/offset + `guidelines/focus-indicators.md` (GLOBAL → reaches all 32) + Tabs binding & anti-pattern; `2.4.7` now cited | fix #2 (today) |
| All component geometry | 🔴 invented | **Closed for Tabs** — `dimensions` block in the meta schema (height 48, padding 20, indicator 3px, track 1px, target 44); schema now supports it system-wide | fix #3 (today) |
| Motion / transitions | 🔴 invented | **Closed** — `tokens/motion.json` + Tabs `motion` block | fix #4 (prior) |

**Result:** in the first build, Route B **failed WCAG in dark mode and had no focus design** — it would not ship. Re-built from today's KB, those four invention-categories are now answered *from the base*. The component the KB describes is now structurally **shippable and accessible in both themes** without the builder inventing focus, geometry, motion, or dark values.

**Residual A–B delta (all 🟡 — refinement, not blockers, none are WCAG failures):**

- Type detail (fix #5): `typography/font-weight` is an unmapped string (`"medium"`), `letter-spacing/font-5` is empty, proprietary font has no fallback stack.
- `tabs/*` incomplete (fix #7): no hover/pressed surface tokens, so those states still fall back to `tertiary/*` (flat in dark).
- Overflow + guideline mapping (fix #6): overflow breakpoint/collapse-count/menu sizing unspecified; `horizontal-scroll.md` mapped to Tabs is carousel guidance, not the tab-overflow pattern.
- Minor semantics: tab activation model (auto vs manual) and `selected-first/middle/last` positioning not spelled out in the meta.

**Bottom line:** the gap shrank from *"correct but unshippable (dark-mode WCAG break + no focus)"* to *"shippable and accessible; remaining delta is type polish and overflow richness."* The dangerous gap — internally-valid-but-unusable — is closed; what's left is craft refinement that won't fail a conformance gate.

**Tooling caveat still standing:** the integrity gate passed both the broken and the fixed Tabs. The new contrast-aware audits (fix #1b) now catch resolved-value failures the old gate missed, but "green gate" still means "internally consistent," not "fit for purpose." Keep the fitness re-run, not the gate, as the progress metric.
