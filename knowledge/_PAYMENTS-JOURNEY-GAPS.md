# Payments journey — end-to-end proof: gap report

*Walked the real journey **Dashboard → Make a payment → Review & confirm → Confirmation** by hand, assembling ONLY from canon components + tokens (KB-only). Prototype: `_fitness-test/payments-journey.html`. Purpose (per [[pipeline-mental-model]]): pressure-test the 12 refined ★ components **together** and catch ≥1 real thing the component-level work couldn't — the first signal from OUTSIDE the system. Date: 2026-06-24.*

## Headline finding (the signal from outside the system)

**The 12 refined ★ components are not sufficient to build a single real screen — and there is no mechanism to *compose* them.** Two distinct problems the component-by-component program could never surface:

1. **Coverage:** every screen of the core journey depends on at least one **un-refined** component (Headers, Navigations, Avatar, Dropdown) *and* at least one pattern with **no canon component at all** (page shell, key-value summary, sticky action bar, balance/amount type). Refining 12 components to 9/9 does not get you one shippable screen.
2. **Composition:** the canon snippets are **standalone reference HTML documents, not importable partials.** To assemble the journey I had to **re-implement every component by hand** (re-deriving its CSS + tokens), which immediately drifted from canon (I reintroduced a list-item title/subtitle stacking bug, and a thinner button without the calibrated scale-physics). There is no shared stylesheet / web-component / partial layer — so "assembly" today = hand re-coding, which defeats the whole point of having gated materials.

This is the proof's job done: the unit of value is the **screen/journey**, and neither the canon set nor the component-level gates cover screen assembly yet.

## A. Journey-critical components NOT yet refined (used on every screen)

| Component | Score | Where it's used in the journey |
|---|---|---|
| **Headers** | 6.5/9 | App bar on all 4 screens (title, back, kebab) |
| **Navigations** | 6.5/9 | Bottom tab bar on the dashboard (+ no nav icon set — I hand-drew home/cards/payments) |
| **Avatar** | 7.0/9 | Payee + transaction initials on dashboard and (implied) payee picker |
| **Dropdown** | 7.5/9 | Payee selector on Make-a-payment — I fell back to a native `<select>`; the canon Dropdown was not composable here |

## B. Patterns with NO canon component (had to invent)

| Pattern | Note |
|---|---|
| **App/page shell** | Phone frame, scrollable screen region, safe areas — no canon for the page scaffold a screen lives in. |
| **Sticky bottom action bar** | Button has the action-bar *pattern*, but "pinned to the bottom of a scrolling screen" (border, elevation, z-index, safe-area inset) is undefined. |
| **Key-value summary list** | The Review screen's label→value rows. Table = tabular/multi-row data; List-items = transaction-shaped (leading + title/sub + trailing). A plain key/value review summary has no home — hand-built as `.kv`. |
| **Account / balance card** | Cards is a generic surface; no "account summary" composition (masked number, big balance, status). |
| **Balance / amount typography + money format** | No display/amount type token for the big balance; the debit-neutral / credit-teal colour convention and currency formatting are conventions with no token or rule. |

## C. Journey-level concerns no component rubric captures

| Concern | Detail |
|---|---|
| **Focus management on navigate** | Moving between screens (SPA-style) needs focus moved to the new screen's H1 and step changes announced (aria-live). Each component is individually accessible; the *journey* AT is unhandled. The prototype-grade rubric is per-component and can't see this. |
| **Status chip vs Tag semantics** | Dashboard shows a Status-indicator chip ("Up to date") next to a Tag ("Everyday"). When is something a Tag vs a status chip? No composition rule — they look interchangeable. |
| **Progress-tracker colour roles** | Done segments use rag/success (teal), current uses brand red (primary). Mixing success-teal for "done" with brand-red for "current" reads oddly; the canon tracker never defined in-context step colours for a linear task. |
| **In-journey validation** | Input-fields has an error state, but where the validation Notification sits, and journey rules (amount > balance, empty reference), are uncovered. |

## D. Recommended next moves (prioritised)

1. **Refine the journey-critical tranche to 9/9:** Headers, Navigations (+ a nav icon set), Avatar, Dropdown. Without these, no screen is shippable.
2. **Add the missing patterns as canon:** account/summary card, key-value summary list, page shell, sticky action bar, display/amount type + money-format tokens.
3. **Introduce journey/composition-level checks** (a new gate tier above the per-component rubric): focus-on-navigate + step-announce, status-vs-tag rule, money formatting.
4. **Solve composition** — the big one: the materials need to be *importable* (a shared token+component CSS layer, or the Sutherland React components) so a screen is assembled from canon, not hand-re-coded. This is the "materials swap snippets→Sutherland" + "harness/conveyor" work in [[pipeline-mental-model]]. Until then, every assembled screen risks silent drift from canon.

## Minor (assembly bugs I hit + fixed — themselves evidence of D2)
- List-item title/subtitle ran together (re-implemented `.t/.s` as inline, not block) — fixed.
- Hand-re-coded Button lacks the calibrated fixed-px scale-physics; uses a simple scale(1.02/.97).
- Dropdown is a raw native `<select>`, not the canon Dropdown treatment.
