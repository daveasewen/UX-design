---
name: feedback-type-composites-mandatory
description: "RULE: every component build uses the canon type.css composites (.t-cm-* / .t-ed-*) — never raw font shorthand; hard-wire via a gate"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2dfa173d-e98a-4a20-a372-c4ba279c0769
---

RULE (Dave 2026-07-17, FIRM): **"everything we produce should use these font rules and the styles for component builds, we need to hard wire this."** All component text must use the promoted canon type composites in `knowledge/canon/type.css` — never ad-hoc `font: 13px/1.3` shorthand.

**The composites:**
- **Component set** `.t-cm-*` (label 16/slot20, caption 14/20, legal 12/16, button 16/20, section-label 20/24, heading 32/40, figure-1/2): cap-trimmed (line-height:1 + text-box-trim) seated in a **4px grid slot** (min-height). Use for **single-line** UI labels.
- **Editorial set** `.t-ed-*` (body 16/24, body-small 14/20, caption 12/16, headings/displays): full **4px line-heights**. Use for **wrapping / prose** text (multi-line Component text drifts off-grid — the N1 caveat).
- **Stacking:** Component blocks stack on **4px spacing tokens, slot-edge to slot-edge** — the descender guard is baked into the slot (vertical-stack rule). See [[type-body-weight-rule]] (no light on body sizes), [[leading-trim-label-decision]].

**Why:** I shipped the reconciled Stepper/Tab-bar labels with raw shorthand; Dave caught it. Fixed by binding to composite metrics.

**How to apply / hard-wire (TODO — build alongside the component index):**
1. Component scaffolds **link/inline** `type.css` composites, not redefine fonts.
2. A **gate** (`_validate_type_composites.py`, wire into `_build_all.py`) that flags raw `font-size`/`font`-shorthand in component CSS unless it's a composite class or a token — verification = enforcement, so it can't be skipped. Sibling to the component-index + duplicate-guard work ([[feedback-survey-before-build]]).
