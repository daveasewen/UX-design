# ADR-0011 — Four-theme token architecture: themes as override sets, not forks

**Date:** 2026-07-20 · **Status:** accepted (Dave — "we need to wire this up properly with the themes") — architecture ratified; migration staged · **Extends:** R-D15 (four-theme architecture, the intent), ADR-0009 (state-styling / override sets), ADR-0010 (nullable flex slots), ADR-0008 (canonical core) · **Relates:** R-D19 (Legacy red vs Mono red) · R-D17 + `_validate_legacy_leak.py` (Legacy-colour leakage gate)

## Context

R-D15 declared the product model: **one token store · one baseline library · four themes**
(Apollo Legacy · Apollo Mono · Apollo Console · Apollo Supercharge), where *"adding a theme = adding
an override set, never forking."* But the store never implemented it. The reality found on
2026-07-20 while consolidating `_fitness-test`, `_proforma`, `_review`, and `snippets`:

- **The semantic store (`semantic-colour.json`) has no theme dimension.** Every role carries only
  `light`/`dark` modes. There is a single flat set of values.
- So **Legacy and Mono values coexist in the same roles.** `primary/background` = `#DB0011` (Legacy
  CTA red). `tabs/active` = `#DB0011`. `progress/complete` = `#DB0011`. Bare `rag/error` =
  `#A8000B`/`#DB0011`. The grey inks resolve to the Legacy `color/grey/*` scale in places where Mono
  should use `color/mono/*`.
- The only reason a Mono button isn't red is that it was **rebound to a new decoupled role**
  (`button/primary/*`). The old red roles are still live and still consumed. Divergence-by-forking,
  exactly what R-D15 said not to do.
- The **leak gate can't see most of it.** `_validate_legacy_leak.py` seeds one hex (the teal) and
  resolves against the flat store; it has no notion of "under which theme should this resolve?", so
  a Mono surface pulling a Legacy red is invisible to it.

The looseness is a **direct consequence of a missing architecture**, not sloppiness in any one file.
"Align to Apollo Mono, with Apollo Legacy in mind" is unenforceable while the two themes share one
set of values.

## Decision

**Themes are override sets at the semantic tier. The three-tier stack gains a theme dimension.**

```
tier 1  PRIMITIVES        shared raw material — color/mono/1-15, color/grey/100-800, the hues.
                          Themes SELECT among these; primitives belong to no theme.
tier 2  SEMANTIC ROLES    role = base value + per-theme OVERRIDE where the theme diverges.
        + THEME OVERRIDES  Resolving a role means: resolve under a THEME. Override wins; else base.
tier 3  COMPONENT         binds a semantic role. Never sees a theme or a primitive. Unchanged.
```

**The four themes (canonical order):**

| Theme | Role in the system | Colour posture | Override-set status |
|---|---|---|---|
| **Apollo Legacy** | Retained for legacy interfaces; superseded over time, never deleted | HSBC brand: red `#DB0011` actions, teal `#00847F` status, `color/grey/*` ramp | **Populated** (holds today's Legacy values, migrated out of the base) |
| **Apollo Mono** | ★ the baseline we build now — "very mono" | Monochrome `color/mono/*`; colour **only** in RAG status + dataviz; Mono red `#B92F1E` for status/RAG only (R-D19) | **Base** (the default the store resolves to) |
| **Apollo Console** | The branded HSBC library (was Apollo UI) | Broader new-colour palette | **Declared nullable slots** (ADR-0010) — wired, unset |
| **Apollo Supercharge** | Brand-uplift rework | Broader new-colour palette | **Declared nullable slots** (ADR-0010) — wired, unset |

**Mechanism (chosen).** A theme is an **override map** keyed by semantic role path. It supplies a
value only where it diverges from the base; everything else inherits the base. This is the ADR-0009
"a chromatic mode is just an override set" principle applied to whole themes, and the ADR-0010
"declared-but-unset" pattern for the two themes whose palettes aren't ruled yet — Console and
Supercharge exist as **explicit null override slots** so the schema, the generators, the gates, and
the coming style-builder can all see them as *wired and waiting*, never as holes.

**Why base = Mono, overrides = Legacy** (not the reverse, despite Legacy being listed first): Mono is
the library we build and ship now, so it is the default path and the value most reads resolve to
without an override lookup. Legacy is the divergence we carry deliberately. This keeps the hot path
cheap and makes "a Mono surface accidentally pulls a Legacy value" a *detectable override-set
violation* rather than an untraceable flat-store coincidence.

**Selection.** A consumer (a snippet, a rendered screen, an adapter target) declares its theme once;
resolution is `resolve(role, mode, theme)`. Components stay theme-blind — they bind roles, the active
theme decides the hex. Adding a theme is adding an override file; no component changes. (R-D15, now
mechanised.)

## The theme-provenance gate (makes R-D19 mechanically true)

`_validate_theme_provenance.py` resolves every Mono-designated surface **under the Mono theme** and
flags any value that belongs to another theme's override set (Legacy red `#DB0011`/`#A8000B`, teal
`#00847F`, Legacy `color/grey/*` inks). It also scans Mono-designated files for **hardcoded** Legacy
hexes — the blind spot the token-resolution leak gate cannot see. The file→theme map is
`knowledge/_STYLE-PROVENANCE.md` (the record), so the gate's scope is the record: add a Mono file →
it must stay clean.

**Staged as ADVISORY first** (records to `_THEME-PROVENANCE-GATE.md` every build, does not block), so
the canonical build stays green through the migration. Promoted to **blocking** once the semantic
roles are migrated into override sets and the flagged surfaces are re-homed. This mirrors the
advisory→blocking path used for prior gates, and honours "verification = enforcement" without
flipping the whole store red in one pass.

## Consequences

- **The record is real, and it's the gate's input.** `_STYLE-PROVENANCE.md` classifies every file and
  every divergent role by theme; the gate enforces it; "we don't miss this in future" is structural.
- **Migration is bounded and stageable.** Only the roles where themes *diverge* (the reds, teal, grey
  inks, the RAG set) need override sets; theme-agnostic roles stay as shared base. Sonnet throughput
  against this ADR, guarded by the blast-radius gate (canonical-store change).
- **Console + Supercharge are unblocked-by-design.** When their palettes are ruled, they fill their
  null slots; nothing forks.
- **Adapters (ADR-0008) get a clean seam.** A consumer codebase maps to *a theme's* resolved set, not
  to a flat ambiguous store.

## What is NOT decided here (backlog, in `_STYLE-PROVENANCE.md`)

- The per-role Mono values for roles that only ever held a Legacy red: `tabs/active`,
  `progress/complete` (Mono ≠ red — needs a ruling each). Bare `rag/error` Mono = `#B92F1E` is known
  but rebinds with the error/warning/info set (R-D17).
- The physical file layout of the override sets (single `$themes` block per role vs per-theme
  override files) — pinned at implementation; the resolver contract above holds either way.
- Promotion of the theme-provenance gate to blocking (after migration).
