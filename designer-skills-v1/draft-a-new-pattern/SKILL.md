---
name: draft-a-new-pattern
description: Help create a NEW component or pattern that fits the design system — built from its existing tokens, type, states, accessibility rules and naming — and package it as a candidate ready to propose for the library. Use when the system is missing something you need. Produces a reviewable draft, not adopted canon.
---

# Draft a new pattern

The **creative / co-creation** mode. Use it when `generate-from-canon` flagged a
Gap, or when you want to invent something the system doesn't have yet. The point
is not to freestyle — it's to grow the system *on-brand and accessible by
construction*, so a designer's new idea can become part of the shared library.

## Rules
1. Build the new thing **from the system's primitives**: tokens by intent (never
   raw hex/px), the type ramp, square corners, the accessibility floor (AA
   contrast, focus ring, target size, reduced-motion, ARIA), and the motion tokens.
2. Give it **all the states** (default / hover / pressed / focus / disabled /
   loading / error / empty as relevant).
3. Name it consistently with the existing components.
4. **Document it** in the same shape as an existing component so it can slot in —
   purpose, props, token bindings, states, anti-patterns, accessibility,
   provenance (mirror the structure of a `knowledge/components/*.meta.json`).

## Procedure
1. Clarify what the pattern is for and where it'll be used.
2. Compose it from canon primitives; bind tokens; add the states.
3. Write the draft: a **snippet** (HTML/CSS or React) + a **meta** describing it.
4. Note what's still **open** for a reviewer to decide.

## Output
A **candidate**: the draft snippet + its meta + a short "what it's for / what's
open" note.

> Important: this produces a **candidate for review, not adopted canon.** A human
> reviews and promotes new patterns before they enter the library — that's what
> keeps the system trustworthy. This is the intended way designers *grow* the
> system, and exactly the input we want back from you.

*Experimental.*
