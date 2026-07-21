# Design system — knowledge base

The reference data the Copilot skills read. **Pre-built** from the live design
system — don't hand-edit, and don't try to regenerate it; ask the design-system
team for a refreshed pack instead. Baked from commit 7071538 (build green 38/38), 2026-07-21.

- `components/` — one `*.meta.json` per component (props, variants, token
  bindings, states, anti-patterns, accessibility) + the schema.
- `tokens/` — the design tokens (colour, type, spacing, elevation, motion, …).
- `tokens/themes/` — the theme override sets (+ `_themes.json` registry). The
  components bind semantic roles; the active theme decides the hex. **Apollo Mono
  is the baseline** — monochrome, colour only in RAG status + data-vis.
- `canon/canon.css` — the composition layer (tokens + reviewed component CSS).
- `canon/type.css` — the type composites (`.t-cm-*` component / `.t-ed-*`
  editorial). Component text binds a composite class, never raw font values.
- `snippets/` — the reviewed reference markup for each component.
- `compliance/` — the WCAG map (which accessibility criteria apply to which
  component) + the rule set.
- `assets/icons/` — the real icon library + manifest (skills use these, never
  invent icons).
- `guidelines/` — design standards for reference (brand, colour, type,
  accessibility, tone, component standards, …).

**Two honest notes.** The guidelines are *reference* — a designer or a skill
consults them (they matter most when **creating a new pattern**). And the
*authoritative* compliance checks (real contrast maths, token fidelity,
accessibility) run as executable gates in CI, not here — the in-editor check
applies the same rules as guidance so you catch drift early.

Intentionally left out: the build scripts, audit/working docs, and
process/governance guidelines — this folder is the design reference, not the
workshop.
