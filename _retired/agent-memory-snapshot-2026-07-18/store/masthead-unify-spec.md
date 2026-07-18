---
name: masthead-unify-spec
description: "NEXT BUILD (Dave 2026-07-16): Global header + content-heavy mega-masthead are ONE pattern with switches. Build a single parameterised .masthead organism + a control row: nav mode (exposed | mega | minimal) + search/account toggles; dedupe the two existing demos. Full spec in notes/HANDOFF-2026-07-16-tranche7-masthead.md."
metadata:
  node_type: memory
  type: project
---

**Dave's insight (2026-07-16, via the review tool):** the Tranche 7 **Global header** (exposed L1 + utility, CDC Frame 1)
and the **content-heavy masthead** (brand + hamburger → mega, CDC Frame 2) are **not two components — one masthead
pattern with different switches.** He wants to *see a variation of the Global header that also invokes a mega menu*, and
framed it as "one component with a set of switches / tabs, same pattern, different use-cases."

**Decision:** spec'd into the handoff; **build first next session** (chose "spec into handoff, build next" — it's the
biggest, most open-ended item and context was stretched).

**Build = one parameterised `.masthead` organism + a control row of switches** reconfiguring one live instance:
- **nav reveal mode**: `exposed` · `mega` (incl. the exposed-header-invokes-mega variation) · `minimal`
- **utility**: search on/off · account on/off
- responsive priority+ → hamburger drawer stays automatic
- **dedupe**: fold the current separate Global-header + `.mm-masthead` demos into this one component.
Constraints: mono tokens, **CSS-only motion** (reuse the fixed grid/`.mm-clip` mega reveal), real icons, disclosure
a11y, ink underbar for current (red is a mode concern). Switch UI = segmented/toggle, behaviour JS only. Consider a
`data-mode` attribute driving CSS so mode-switching is declarative. Strong "one component, many use-cases" proof for the
factory story. Full spec + this session's context: `notes/HANDOFF-2026-07-16-tranche7-masthead.md`. See [[proforma-programme]], [[cdc-nav-alignment]], [[nav-pattern-catalog]].
