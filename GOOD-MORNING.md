# Good morning, Dave ☕

Here's where we left things — read this first, then dive in.

## Yesterday in one line

We ran the Tabs fitness-for-purpose test, and it did its job: it told us something true and slightly uncomfortable, which is exactly what we wanted from it.

## The headline finding

Built **faithfully from the knowledge base**, Tabs is correct in light mode but **broken in dark mode** — the label and the selected indicator render white-on-white (1.0:1 contrast, invisible). That's a hard WCAG failure produced by following the tokens exactly as written. The unconstrained build (Route A) passes every contrast check in both themes.

The deeper lesson: **our integrity gate waved this through green.** Internal consistency (references resolve, schema valid) is not the same as fitness for purpose. We had the warning in prose; we lacked the severity, which only building surfaced.

Honest state of the project: the KB is a strong **correctness + provenance + migration-safety** layer. It is **not yet** able to drive *shippable* output, because it holds almost none of the craft — focus indicators, geometry, motion, considered dark values — that separates "correct" from "good." That's a defined backlog, not a redesign.

## What we shipped after your review

- **Motion is now real** — `tokens/motion.json` (DTCG duration + easing) and a `motion` block in the Tabs meta. First motion tokens in the store. (Gap-report fix #4 ✅)
- **Brand fixes from your notes:** square corners (angular rule — with Badge + Avatar as the *only* exemptions, captured), constant type weight so tabs don't jump, and the dark-mode indicator set to **core brand red `#DB0011`** (it passes 1.4.11 at 3.46:1, so brand fidelity wins).
- All changes still pass the build gate: 32/32 metas valid.

## What's queued (in priority order)

The full backlog is in `knowledge/_FITNESS-TEST-tabs.md`. The big ones:

1. **🔴 Fix the dark token values + make the dark-mode audit contrast-aware** — it currently rates a token "clean" if it merely *has* a dark value, even when that value is wrong.
2. **🔴 Add a focus-indicator standard** (token + guideline) — systemic; affects all 32 components.
3. **🟡 Add a geometry block to the meta schema** — metas carry colours but no measurements.

## Two decisions waiting on you / me

- **Reconcile the dark values to real HSBC primitives** (my Route A hexes were demo judgment, not canon — need to map to `neutral-dark-mode` / `rag-dark` before storing).
- **Can the Figma connector *write* variable values?** Unverified. This is the gate on the whole "apply the dark-mode fix back into Figma" idea — a small, bounded check worth doing early.

## Suggested first move

Verify the Figma write capability (15 min, bounded) — it tells us whether the write-back plan is even viable and shapes everything after. Then fixes #1–#3, and when they're in, **re-run the Tabs test and watch the A–B gap shrink.** That re-run is the real progress metric — not another derived view.

Have a good one. The work's in good shape, and we're pointed at the right question.
