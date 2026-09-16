# Design system — knowledge base

The reference data the Copilot skills read. **Pre-built** from the live design
system — don't hand-edit, and don't try to regenerate it; ask the design-system
team for a refreshed pack instead. Baked from commit eb2ff7c (2026-09-16) plus the #279 lane PK release commit that carries this bake — every shipped path equals eb2ff7c except knowledge/_compose_slice.py, whose pack allow-set bite lands in that same commit.

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
- `_compose_slice.py` — **the reader** (v2.1). `generate-from-canon` step 1 runs it
  once for a seed, and its `--ask` door answers the 12 designer questions from the
  files beside it — including `_rulings.json`, **the Constitution**: what was ruled,
  by whom, when, and what it governs. It reads these files LIVE, from this folder;
  nothing here reaches back to the design-system repo. Needs `python3` (and
  `pip install tiktoken` for measured token counts; without it counts are
  labelled estimates). `_rulings.json`, `_ruling_edges.json`, `_rule_nodes.json`,
  `_ux_principle_nodes.json`, `_icon_nodes.json`, `_logo_nodes.json`,
  `roles.json`, `chart-intents.json`, `component-types.json`,
  `_consult-lexicon.json`, `guidelines/_rules-index.json`,
  `guidelines/_scope.json` and `tokens/_blast-radius.json` are what it reads.

**Two honest notes.** The guidelines are *reference* — a designer or a skill
consults them (they matter most when **creating a new pattern**). And the
*authoritative* compliance checks (real contrast maths, token fidelity,
accessibility) run as executable gates in CI, not here — the in-editor check
applies the same rules as guidance so you catch drift early.

Intentionally left out: the build scripts, audit/working docs, and
process/governance guidelines — this folder is the design reference, not the
workshop.
