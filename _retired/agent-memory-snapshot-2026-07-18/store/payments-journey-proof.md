---
name: payments-journey-proof
description: End-to-end payments-journey proof (2026-06-24) — outcome of walking Dashboard→Pay→Review by hand from canon; the two headline gaps (coverage + composition) and next moves
metadata: 
  node_type: memory
  type: project
  originSessionId: 29f62e34-4096-4e20-9fcc-10f2a34ec864
---

**RAN 2026-06-24** (after all 12 ★ hit 9/9): the walk-one-journey-by-hand proof from [[pipeline-mental-model]]. Built Dashboard → Make-a-payment → Review & confirm → Confirmation, KB-only, from canon components+tokens. Artifacts: `_fitness-test/payments-journey.html` + `knowledge/_PAYMENTS-JOURNEY-GAPS.md`. Rendered light/dark, 0 overflow to 320px.

**Two headline findings (the signal from outside the system):**
1. **Coverage** — refining 12 components to 9/9 does NOT yield one shippable screen. Every screen needs an UN-refined component (Headers 6.5, Navigations 6.5 + no nav-icon set, Avatar 7.0, Dropdown 7.5 — I fell back to a native `<select>`) AND a pattern with NO canon at all (app/page shell, sticky bottom action bar, key-value summary list, account/balance card, display/amount type + money-format).
2. **Composition (the big one)** — canon snippets are standalone reference HTML, NOT importable partials. Assembling = hand re-coding each component → immediate drift (reintroduced a list-item stacking bug; button lost its calibrated scale-physics). No shared token+component CSS / web-component / partial layer. Maps to "materials swap snippets→Sutherland" + "harness/conveyor barely built". Until solved, every assembled screen risks silent canon drift.

**Journey-level concerns no per-component rubric can catch:** focus-on-navigate + step-announce (SPA AT), Status-chip vs Tag semantics, Progress-tracker in-context colour roles (done=teal vs current=red reads odd), in-journey validation placement.

**Proof #2 — SME business-banking Payments screen (2026-06-24, `_fitness-test/sme-payments.html`):** a denser finance-admin screen from a fixed-figures brief (cash position / coverage / pending approvals / upcoming). NEW findings: (a) **brand red-primary doesn't fit a business/approvals screen** — the brief's "red = destructive only" rule forced primary actions to a NEUTRAL/ink button (black→white inverting), which reads more sober/correct; canon Button is red-primary, so a non-red "ink/neutral primary" mode (or a reserve-red rule) is a real gap. (b) More missing patterns: metric/stat grid (cash position 2×2), a contextual "insight/coverage statement" card, an approval action-card with dual actions + high-value confirmation step, a list totals row. (c) This screen IS a contextual finance-admin dashboard (cash + coverage insight + approvals) → live tie to [[vision-contextual-dashboard]]. Maths/rules all honoured exactly.

**Next moves (in the gap report):** (1) refine journey tranche Headers/Navigations/Avatar/Dropdown; (2) add missing patterns as canon (account card, key-value summary, page shell, sticky action bar, amount type/tokens); (3) a journey/composition gate TIER above the per-component rubric; (4) solve composition = importable materials (shared CSS or Sutherland). Relates to [[component-review-program]], [[procedural-debt-and-method]], [[promenaut-product-vision]].
