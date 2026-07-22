# Brief — per-theme neutral primitives + per-theme state mechanism (for a FABLE clean-room)

> Status: **DRAFT capture** (2026-07-22 08:15 BST). Facts below are Dave-stated/observed; the
> architecture shape is my synthesis, **pending Dave's confirm + a Fable design pass.** Raised during
> the ruling-batch session (tabs/active §C·1d) — the tabs decision surfaced that themes carry their own
> neutral ramps, which is an architecture change, not a slot fill. Dave: *"this probably needs Fable to
> redesign the architecture."* Sits under ADR-0011 (four-theme override sets) + ADR-0009 (state mechanism).

## The spine (Dave, 2026-07-22) — sibling pairs on one flexible DNA
All four themes share **one flexible root DNA**; the differences are dials, not forks. *"At any point we
could engineer 3 to align completely to one we choose."* Two sibling pairs:
- **{Mono, Console} — closest siblings.** Share the **same** neutral palette, **interaction opacity
  values**, **status palette**, and **dataviz**. (Console inherits Mono on these layers; its broader
  branded chromatic palette sits on top — ⚠ reconcile with the older "Console carries the broader new
  palette" note, don't silently override.)
- **{Legacy, Supercharge} — the other pair.** Similar structure to each other; **different colour
  palettes**. Some component-structural overlap.

## What is now FIRM (Dave, this session)

**1. Each theme brings its OWN neutral primitive ramp** (already true for Mono vs Legacy; now explicit + extended):
- **Mono** — `color/mono/1–15`, truly neutral (existing).
- **Legacy** — the HSBC brand neutral scale (exact, from Dave's swatch sheet):

  | token | hex | | token | hex |
  |---|---|---|---|---|
  | neutral-white | `#FFFFFF` | | neutral-grey-5 | `#9B9B9B` |
  | neutral-grey-1 | `#F3F3F3` | | neutral-grey-6 | `#767676` |
  | neutral-grey-2 | `#EDEDED` | | neutral-grey-7 | `#545454` |
  | neutral-grey-3 | `#D7D8D6` | | neutral-grey-8 | `#333333` |
  | neutral-grey-4 | `#B7B7B7` | | neutral-black | `#000000` |

  Legacy **dark-mode-only** neutrals (separate 6-step set): `dark-mode-grey-1 #656565 · -2 #474747 · -3 #404040 · -4 #212121 · -5 #1D1D1D · -6 #101010`.
- **Supercharge** — its own **warm/taupe** ramp (15 steps; cast peaks mid-low). **Values TBD** — extract from Figma `DS3tkWgaM1OsJg9ZC7nVLK` (nodes `1105-47322…47350`). `get_variable_defs` returned `{}` on the swatch nodes (fills, not bound vars) → use `get_design_context` or the variable-collection node.
- **Console** — own palette (parked).

**2. State mechanism — ONE test, not a per-theme hardcode** (refines ADR-0009's `{colour|opacity|both}`):
> **Opacity for states is allowed iff the composite is engineered to land on one of that theme's
> primitive ramp steps** (the snap). Otherwise use colour.
- **Hueless neutrals (Mono, Legacy)** → opacity is clean; fade over the surface snaps to a neutral grey
  step. Mono+Console use the **shared** opacity values (button-sheet v7 method; tabs v4 tuner); two
  tokens stored (operational α + portable colour).
- **Hued neutrals (Supercharge warm ramp)** → **colour-only by default** (a fade drags the hue off-ramp);
  opacity permissible **only if** the value is engineered to snap to a warm primitive step.
- Practical upshot: Mono/Console opacity · Legacy opacity-capable (neutral) · Supercharge colour, opacity
  by exception. `snapPass` is parameterised by the **active theme's** ramp.

**3. Ink per theme** (`text/default` resolves per active theme):
- Mono `#1A1A1A` / `#FFFFFF` · **Legacy `#333333`** (grey-8) · **Supercharge `#13110E`** (Dave: "I think we can use"). Dark-mode inks per theme TBD (Legacy dark likely off the dark-mode grey set).

## Architecture questions for the Fable pass
1. Token-schema home for per-theme neutral ramps under ADR-0011 — naming (`color/supercharge/*`?), and confirm every semantic role aliases to the **active theme's** ramp (retrieval-not-recall holds).
2. Make **state-mechanism a theme property** (Mono=opacity, Legacy/SC=colour); parameterise `snapPass` by the active ramp so a warm theme snaps to warm steps.
3. Per-theme **ink** + per-theme **dark-mode** ramps (Legacy has a distinct dark set).
4. Extract + inscribe the **Supercharge ramp** hexes (Figma) — first build step.
5. Reconcile with the tabs decision: **Mono tabs = opacity-snap (ink bar, red badge) STANDS**; Legacy/SC tabs = solid colour swaps.

## Reference
- Legacy Figma: `mI8hvIkV98nquoqWzKh5Kn` (HSBC Common Toolkit MCP) nodes `2092-27610`, `13833-18200`.
- Supercharge Figma: `DS3tkWgaM1OsJg9ZC7nVLK` (Digital Supercharge 0.5).
- Tabs review live: `reviews/TABS-ACTIVE-ink-vs-legacy-2026-07-21-v4.html`.
- Precedents: button sheet `reviews/APOLLO-MONO-PRIMARY-ACTION-2026-07-20-v7.REVIEW.html`; ADR-0009, ADR-0011, R-D22.
