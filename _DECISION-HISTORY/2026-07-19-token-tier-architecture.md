# Token architecture ruled: strict three-tier stack (primitives → semantic → component)

**Date:** 2026-07-19 · **Ruled by:** Dave · **Status:** RATIFIED, being enacted (elevation = reference example)
**Home of the standard:** `_STANDARDS.md` §1 (standing doc). **This file = the why.**

## Context
Enacting the dark-surface elevation fix surfaced how the token store actually binds: component-named
tokens (`tertiary/background/*`, `tabs/*`, …) carried a resolved hex plus an `$alias` pointing straight
at a **primitive** (`color/grey/600`). Effectively a two-tier store — components sat on primitives, with
no semantic layer between. When Claude proposed wiring the new elevation values, Dave stopped it:

> "yes don't use the primitives, i need a proper three layer stack primitives semantic and components …
> lets use best practice for this, i don't want anything less than awesome … this isn't a hobby it's
> going to a professional product."

## Decision
Adopt a strict **three-tier reference model**, the industry-standard taxonomy (Material 3 ref/sys/comp;
DTCG; Style Dictionary):
- **Primitive** — raw value, references nothing (`color/mono/raise-1 = #1F1F1F`).
- **Semantic** — intent, references exactly one primitive per mode (`surface/raised` → `{color.mono.raise-1}`).
- **Component** — references a **semantic** token, **never a primitive, never a raw value**
  (`tertiary/background/default` → `{surface.raised}`).

If no semantic token fits a component's need, you **add a semantic token** — you do not reach past the tier.

**Storage contract:** `$alias` (per mode) is the source of truth; `$value` (per mode) is a build-time
**resolved cache**. `_validate_token_tiers.py` gates `$value == resolve($alias)` along the chain AND that
component-tier aliases target semantic tokens. `gen_canon_tokens.py` emits the real `var()` chain into
`canon.css`. This is the Style Dictionary model — it keeps every existing hex-consuming gate working while
making the three tiers real at runtime.

## Reference example
Dark-mode elevation. Primitives `color/mono/raise-1/2/3` (`#1F1F1F / #232323 / #272727`, dialled by Dave
on the v2 tuner) → semantic `surface/raised`, `surface/subtle`, `surface/raised-hover` → the ~10 surface
component tokens that R-D16 had flattened onto the `#1A1A1A` ground. Press/active recede to the ground
(valid press feedback); `raise-3` is reserved for the interaction-state work.

## Consequences
- New blocking gate `_validate_token_tiers.py` (tier discipline + value/alias consistency).
- The rest of the store is still two-tier (components alias primitives); it migrates onto proper tiers as
  a deliberate follow-up pass, not one big sweep — elevation proves the pattern first.
- `_STANDARDS.md` created as the standing standards hub (reachability-gated, STAND-002).

## Related
`_STANDARDS.md` · `four-theme-architecture` (one store, four themes) · `token-collection-architecture` ·
memory `token-tier-architecture`.
