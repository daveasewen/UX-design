# ADR-0010 — Token schema: explicit nullable slots for the dimensions we flex

**Date:** 2026-07-20 · **Status:** accepted (Dave) — direction ratified; implementation staged (pilot: the RAG green set) · **Extends:** ADR-0009 (state-styling / style-builder) · R-D15 (four-theme architecture) · ADR-0004 (WCAG 2.2 AA floor) · **Relates:** R-D17 + `_validate_legacy_leak.py` (the Legacy-colour leakage gate)

## Context

Rebinding the Apollo Mono button surfaced a leak: the "Done" success state rendered the **Legacy
teal** `#00847F` because the R-D14 Mono green set was **half-built** — `rag/success-background` was
complete in both modes, but `rag/success-glyph` had **no dark value at all**. The dark slot was not
`null`; it was simply **absent**. A missing key is invisible: nothing in the store, the generators,
or the gates could see that a decision was owed, so the component silently fell back to the Legacy
role and shipped the wrong colour. We only found it by eye.

This is the general failure mode of a **sparse** token schema (omit a slot until it's decided):
"undecided" and "doesn't exist" look identical, so holes are silent until they surface as bugs.

Two forces push the other way:

- **Max flexibility (Dave).** *"We always have to think about max flexibility and save all possible
  values for the architecture… the value can be a value or null, like placeholders."* A future RAG
  may set **light ≠ dark** as independent hues (not shades); a future theme adds an override set; a
  future state carries opacity as well as colour. The schema should have the slot ready.
- **A style-builder is coming (ADR-0009).** The style-builder is where a user configures mechanism +
  values per state, per mode, per theme, within the AA guarantee. It needs a **complete, uniform
  slot substrate** to expose those dimensions — it cannot offer to set a value that has no home.

Dave's own refinement bounds this: *"probably not every possible parameter, but the ones we need to
flex."* Not a blanket dense schema — reserved slots for the dimensions we **anticipate flexing**.

## Decision

**1. Complete schema across the anticipated flex dimensions.** A token declares a slot for every
dimension we expect to flex — today **per-mode** (light/dark); by design also **per-theme** (override
sets), **per-state mechanism** (colour / opacity / both, per ADR-0009), and **opacity** — rather than
omitting the ones not yet decided. The set of dimensions is defined by what the **style-builder will
expose**, not by "every property that exists."

**2. `null` is a first-class placeholder — declared-but-unset — and is distinct from two neighbours.**
Three states, never conflated:
- **absent** — the dimension does not apply to this token (e.g. a token that is legitimately mode-agnostic). Avoid where a flex dimension is anticipated; prefer an explicit slot.
- **`null`** — the slot exists and a value **is owed but not yet decided**. A visible, queryable hole.
- **a value** (or an explicit *inherit* marker) — decided. "Same as light" is expressed by an explicit inherit/alias, **never** by leaving the slot missing.

**3. A gate turns silent holes into build failures: no `null` under a live binding.** A slot *may* be
`null` while undecided — that is the point. But a token that is **bound by a live component** must not
resolve to `null` in any mode/theme that component renders in. The gate makes "someone still owes this
green" a red build instead of a shipped bug. (Sibling to R-D17's leakage gate: that one stops the
**wrong** colour landing in a Mono surface; this one stops a **missing** colour doing the same.)

**4. `resolve()` treats `null` deliberately.** Null resolves to *unresolved*, never to a silent
fallback. Under a live binding → gate failure (see 3). An intentional "inherit from light" is an
explicit marker the resolver honours, not the absence of a value.

**5. AA remains invariant (ADR-0004).** Placeholders and flex slots change *where values live*, not
the floor. Whatever a slot is finally set to — and whatever mechanism resolves it — the resolved state
still passes AA. The style-builder configures within that clamp (ADR-0009 §5, B-D5).

**6. Incremental, not big-bang.** Slots are added as flex dimensions are identified; tokens are not
mass-rewritten. `text/on-success` (minted per-mode this session, both `#000000` today, so a future RAG
can diverge the modes without a structural change) is the first token authored to this ADR.

## Consequences

- **Pilot = the RAG green set.** `rag/success-glyph.dark` becomes an explicit `null` (declared hole),
  and `rag/success-tint` dark (still teal `#001615`) is flagged the same way — instead of a missing
  key and a stale value. Once a live Mono component binds them, the null gate blocks the build until
  Dave rules the dark glyph-green + tints (the ruling that also clears the seven `_validate_legacy_leak`
  waivers). Missing-green stops being findable-only-by-eye.
- **Two gates, two halves of one guarantee.** Leakage gate (R-D17): no *wrong* (Legacy) colour in a
  Mono surface. Null gate (this ADR): no *missing* colour under a live binding. Together they close the
  "component silently renders something unintended" class.
- **Cost accepted, within scope.** More verbose tokens and null-aware tooling — bounded by the
  "anticipated flex only" rule (Decision 1, Dave), so the schema stays legible rather than exhaustive.
- **Feeds the style-builder (ADR-0009).** The complete slot substrate is precisely what the builder
  configures against; `$extensions.apollo.state` is the current skeleton those slots will formalise.

*Provenance: session "Mono primary-action / state-styling" follow-on, 2026-07-20. See R-D17
(`knowledge/_proforma/_RAG-DECISIONS.md`), B-D6 (`_BUTTON-DECISIONS.md`), and the forward entry in
`_FUTURE-STATE.md`. Null-gate + slot rollout are staged work, not yet implemented.*
