# Tomorrow — Tabs fitness-for-purpose test

**Goal:** find out whether the knowledge base can actually drive a good, compliant component — and exactly where it falls short. The component is the *probe*; the **gap report is the deliverable**. Success = a clear answer to "does this KB work?" plus a prioritised fix list — *not* a pretty component.

## Method — two routes, KB-only FIRST

1. **Route B — the real test (do this first).** Build Tabs in **HTML + CSS variables** using *only* the knowledge base: `components/tabs.meta.json`, the token stores, `compliance/`, `guidelines/`. No live Figma, no outside design judgement, no filling blanks from memory. **Log every gap the moment I hit it** — anything I have to guess, anything missing, anything the KB states that's wrong.
2. **Route A — the ceiling ("for fun").** Then build the best Tabs I can, unconstrained: full design judgement, motion, all states, polish. This is "what good looks like."
3. **Side-by-side + dual critique.** Put A and B together. Grade both, independently, on:
   - **Engineering correctness** — compiles, tokens resolve, passes the WCAG 2.2 AA checks we encoded.
   - **Design craft** — would an HSBC designer ship it? Spacing rhythm, state transitions, hierarchy, motion, empty/loading/error states. Use the `design-critique` + `accessibility-review` skills against our *own* output.
4. **Gap report → `knowledge/_FITNESS-TEST-tabs.md`.** The A–B delta + the live gap log = a concrete, prioritised list of what the KB needs to drive codegen (schema fields, missing tokens, guideline detail, structured bindings, etc.).

**Why B before A:** if I build the polished one first I'll "know" the answers and unconsciously patch B's gaps from memory — contaminating the test. Recording what the KB gives me before I know better is the whole point.

## What Tabs should stress (predictions — check the KB surfaces these unaided)

- **P3:** selected indicator bound to the `color/primary` primitive → should be a mode-aware `tabs/active`; dark mode breaks otherwise.
- `color/primary` dark-mode leak (from `_DARK-MODE-AUDIT.md`).
- 2 deprecated bindings whose rebind targets are REVIEW-tier guesses.
- 6 WCAG SCs incl. 2.4.11 Focus Not Obscured, 2.5.8 Target Size, keyboard + roles (4.1.2).
- Responsive horizontal-scroll / overflow behaviour.
- **Token bindings are prose, not structured** — can I even resolve them cleanly into CSS variables? This is the softness I flagged; the test will expose it.

## Bigger questions to hold in mind (the honest critique)

- Fitness-for-purpose, not internal consistency — does an agent produce *better* code because of this KB?
- Single-author provenance — no second eyes, no validation against the real Sutherland library yet.
- Are we out of the "productivity bubble"? This task is a validation, not more building. Keep it that way.

## Out of scope tomorrow

- No new derived views / generators unless the gap report proves one is needed.
- Sutherland migration stays parked (JSON ~late June/early July).
