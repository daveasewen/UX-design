---
name: check-against-design-system
description: Review a UI candidate against the Apollo design system and flag where it drifts — invented components or variants, hard-coded values instead of tokens, raw type instead of composites, theme leaks, red-law breaches, off-rails layout, anti-pattern violations and missing states. Use to check whether a design conforms before it advances. Pairs with check-with-gates, which proves mechanically what this skill judges by reading.
---

# Check against the design system

Inspect a design or its code against the canon and report where it strays.

**Run the gates first.** This pack ships the same executable checks Apollo runs on
itself — contrast maths, token fidelity, icon provenance, accessibility targets. They are
cheaper and more certain than reading, and they will find the mechanical drift before you
spend attention on it. Start with the `check-with-gates` skill, then come back here for
everything a gate cannot see: whether the right component was chosen, whether the states
make sense, whether the layout obeys the rails, whether the copy is right.

Green gates are not a pass. A gate only sees what its glob reaches, and it cannot tell
you that a perfectly-tokenised card was the wrong component for the job.

## What to catch

**Mechanical — a gate can prove these. Cite the gate's own words.**

- **hard-coded value** — a raw hex, or a raw px for spacing / border-radius / border
  width, where a token belongs. (`_validate_no_hardcode.py`)
- **invented-token** — a token name that isn't defined in `knowledge/tokens/`. A
  plausible name that doesn't exist is as dangerous as an invented component, and renders
  as nothing at all. (`_validate_binds_resolve.py`, `_validate_property_resolves.py`)
- **raw-type** — `font-size` / `font-weight` / `line-height` set directly instead of a
  composite class from `knowledge/canon/type.css` (`.t-cm-*` component, `.t-ed-*`
  editorial; 31 of them). (`_validate_type_composites.py`)
- **invented-icon** — a glyph that isn't in `knowledge/assets/icons/`, or a shape-only
  `<svg>` with no library path behind it, not marked `data-bespoke`.
  (`_validate_icons.py`)
- **contrast failure** — a text or UI pair under its threshold in either mode.
  (`_validate_snippets.py`, `_validate_a11y.py`)
- **missing focus / reduced-motion** — `outline:none` with no visible replacement;
  something that animates with no `prefers-reduced-motion` block. (`_validate_a11y.py`)
- **target too small** — a control under the 24px floor with no hit-expander.
  (`_validate_a11y.py`)
- **case-drift** — `text-transform:uppercase`, or ALL-CAPS runs outside acronyms.
  (`_validate_snippets.py`)
- **local redefinition** — a screen's own `<style>` redefining a `.c-*` or `.cn-*` class,
  or carrying a rogue hex. This is *the* drift vector: it re-derives a component
  per-screen. (`_validate_compose.py`)

**By reading — no gate sees these. This is where your attention goes.**

- **invented-component** — an element that isn't in `showroom/index.json` (135
  components, 8 foundations). Search by alias and blurb before concluding it's missing.
- **invented-variant** — a variant the component's `knowledge/components/<slug>.meta.json`
  doesn't define.
- **deprecated-component** — `status: "deprecated"` in the index. Name the successor.
- **wrong-component** — the right shape, the wrong meaning. Read `purpose` and
  `relationships.commonPatterns` in the meta.
- **theme-leak** — a colour belonging to another theme's set on this theme's surface.
  `knowledge/tokens/themes/_themes.json` records `ownsHexes` per theme — e.g. legacy red
  `#DB0011`, legacy teal `#00847F`. Four themes ship: mono, legacy, console, supercharge.
  Also flag a candidate that never declares which theme it is in
  (`data-apollo-theme` + `data-theme` on the root).
- **red-law breach** — the reds are keyed to the background behind them, not to
  light/dark mode: dark red `#DA1A00` on white, light red `#F6604C` on everything else.
  Coloured red or green **text** belongs to monetary values only, always with a symbol.
  Error checks and radios take red on the **mark**, never the label. In mono, glyphs and
  labels on an error surface are default dark ink — white-on-error does not exist.
- **ink hardcode** — pure black, or any literal, where the ink token belongs. Ink
  resolves per theme.
- **off-rails layout** — a spacing value outside the ruled stops `{1, 2, 4, 16, 24, 40}`,
  or a combination of layout dials the rails manifest excludes. One file has the answer:
  `knowledge/_render/_bento_edit_rails.json` — legal options, per-theme defaults, legal
  chords and exclusions.
- **anti-pattern** — violates the component's `antiPatterns`, or
  `relationships.mustNotNeighbour`.
- **missing-state** — an interactive component missing a state its meta defines: default
  / hover / pressed / focus / disabled / loading / error / empty.
- **copy drift** — title case where sentence case is the standard; alt text opening
  "Image of…"; bare "click here" links.

## Procedure

1. **Run the gates** (`check-with-gates`). Record what each said, verbatim.
2. For each element, confirm the **component exists** in `showroom/index.json` and is not
   deprecated — and that it is the right one for the job, per its `purpose`.
3. Confirm the **variant** is defined in the meta.
4. Confirm the candidate **declares its theme**, and scan its colours against the theme
   registry for leaks and against the red law.
5. Check the **layout dials** against `_bento_edit_rails.json`.
6. Check `antiPatterns` and `relationships`.
7. Confirm the required **states** are covered.
8. Read the **copy**.

## Output

A list of issues, each with:

- a **severity** — blocker / warning;
- **where** it is;
- a **specific, actionable fix** — "bind the background to `tertiary/background/hover`",
  not "fix the colours";
- and, for the mechanical ones, **which gate said so**, quoted.

End with a one-line verdict: fail if any blocker. Then say, in one sentence, **what you
did not check** — the gate that could not ask, the surface you didn't open. An honest gap
is worth more than a clean-looking summary.

*Experimental.*
