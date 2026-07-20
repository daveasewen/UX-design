# ADR-0009 — State styling: colour is the universal substrate; opacity is an optional operational layer

**Date:** 2026-07-20 · **Status:** accepted (Dave) · **Extends:** R-D15 (four-theme architecture), ADR-0004 (WCAG 2.2 AA floor), ADR-0008 (canonical core)

## Context

Minting the Apollo Mono **primary-action** button forced a question that is not about one
button: *how is an interaction state (hover, pressed, …) styled, such that the same component
skeleton serves very different themes?* Three concrete pulls surfaced in the same conversation:

- **Mono wants efficiency.** Mono is monochrome UI (colour only in dataviz/RAG/status). Its
  natural hover is the fill **fading over the page** — i.e. opacity — not a second bespoke
  colour to maintain.
- **A future consumer wants colour alone.** Some target codebases can't (or won't) render a
  state via runtime opacity; they need a **solid colour token** for the hover ground.
- **A future mode is fully chromatic.** Dave: *"we might have a mode that is red for default,
  blue for hover and green for active."* Distinct hues per state, no opacity involved.

If hover were modelled as *either* "an opacity" *or* "a colour," one of these three loses. The
architecture must hold all three on one skeleton, and every result must still pass AA.

## Decision

**1. The colour token per state is the universal substrate.** Every interaction state
(`default`, `hover`, `pressed`/`active`, `disabled`) is expressed as a **colour token that
always exists**, supplied per theme via override sets (R-D15). A fully chromatic theme —
red default / blue hover / green active — is *just an override set with distinct hues*; it needs
**no new machinery**. Colour is the portable, lowest-common-denominator form every consumer can
render.

**2. Opacity is an optional operational layer, never the substrate.** A state *may also* carry an
**opacity** value. When a theme renders a state via opacity, the fill fades over the surface
(`background/default`) at that alpha; the state's **colour token is then the stored opaque
equivalent** (for Mono, the ramp-snapped flatten of the default ground over the page bg), so the
state stays portable to colour-only consumers. Opacity buys efficiency and a single-source fill;
it never replaces the colour token.

**3. Render-mechanism is a per-state SET, theme/consumer-selectable — `{colour}`, `{opacity}`, or
both.** These are **not mutually exclusive**: a state can be a distinct colour, a fade, or a
distinct colour *that is also* faded. Colour-alone is first-class. Mono hover = `{opacity}` (with
the colour equivalent stored); a chromatic mode's hover = `{colour}`; a consumer that can't do
opacity resolves any `{opacity}` state through its stored colour equivalent. The choice is the
theme's/consumer's, per state.

**4. Accessibility is invariant across mechanism (ADR-0004).** Whatever mechanism or values a
theme selects, the **resolved label-on-ground must pass WCAG 2.2 AA**. Tooling only ever offers
passing selections — the Mono primary review editor disables ramp steps that fail label contrast
and **clamps the opacity dial to the range where the flattened ground still passes**. AA is a
property of the *resolved* state, not of the mechanism.

**5. Skeleton now, style-builder interface later.** The per-state config (mechanism set + opacity)
is carried as a **non-breaking DTCG vendor extension**, `$extensions.apollo.state`, on the state's
colour token — reference implementation: `button/primary/background/hover`. It migrates to a
first-class number/opacity token (the stores already hold `duration`/`dimension`/`number` types)
when the **style-builder interface** (see `_FUTURE-STATE.md`) and the snippet rebind land. The
style builder is where a user configures mechanism + values per state, within the AA guarantee.

## Consequences

- **One skeleton, many themes.** Mono (opacity-efficient), a colour-only consumer, and a fully
  chromatic mode all sit on the *same* `button/*/background/{default,hover,pressed,disabled}`
  tokens. New modes are override sets, not forks — the four-theme model (R-D15) absorbs them.
- **Portability is guaranteed.** Because the colour token always exists, no state is ever
  *only* expressible as opacity; every `{opacity}` state has a colour fallback for adapters
  (ADR-0008).
- **AA can't be dialled away.** The mechanism is free; the resolved contrast is not. Builders
  and review editors enforce it at selection time.
- **Migration debt (tracked).** Until the dedicated opacity/number token + generator wiring
  land, opacity lives in `$extensions.apollo.state`; the snippet rebind that makes hover
  operationally opacity is the same deferred pass as the rest of the `button/*` rebind
  (queue #4). No gated-code depends on the extension yet.

*Reference material: `reviews/APOLLO-MONO-PRIMARY-ACTION-2026-07-20-v4.html` (opacity operational
+ colour stored + AA-clamped) and the v5 editor (mechanism switch + chromatic example).*
