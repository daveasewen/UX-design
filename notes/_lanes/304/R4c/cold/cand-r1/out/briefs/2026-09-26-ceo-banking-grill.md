# Brief — CEO international-banking prototype (grill, 2026-09-26)

Source: the task prompt's SETTINGS block answered all six standard questions up front ("already decided, do not ask"). No designer was available for discovery questions, so each one is recorded with the default this build took.

## The six questions

1. **Theme** — Common. Set as `data-apollo-theme="common"` on `<html>`.
2. **Light, dark, or both** — both, with a theme switch (app bar and Settings), persisted.
3. **Density and width** — bento, comfortable density, wide desktop (built and measured at 1440 px; also measured at 1100 and 820). The section the bento sits in takes the lightest grey (`--surface-subtle`, the rails' `bentoBg: grey`); page and title area unchanged.
4. **Brand assets** — the supplied HSBC masterbrand (the shell's own `masterbrand-light-colour.svg` / `masterbrand-dark-colour.svg`) and Apollo tokens. Nothing else.
5. **Data** — realistic placeholder entities and currencies, GBP reporting with explicit illustrative FX rates, 30-day series (7 / 30 / 90-day range), enough rows to sort, filter and page.
6. **Fixed / off-limits** — Apollo accessibility defaults and existing patterns only; no invented components, variants, colours or icons; components at their own size; no live banking connections or credentials.

## Discovery questions I would have asked, and the default taken

| question | default taken |
|---|---|
| Dashboard bento — is that right? (rule 7a) | Yes — the prompt names bento. |
| Which group entity is the parent, and which entities/regions exist? | Six placeholder entities of "Aldergrove Group" across Europe, Americas, Asia Pacific and Middle East. |
| What is the CEO's approval threshold, and when is an audit note mandatory? | Payments of £5m or more route to the CEO; an audit note is mandatory at £10m or more and for every rejection. |
| What counts as a "material" risk exception? | Any limit above 100% and named compliance/hedging items; acknowledging one needs a 15-character note. |
| How is funding headroom defined? | Available liquidity (cash + undrawn committed facilities) less a £400m minimum liquidity buffer and debt due within three months, pro-rated to the entities in view. |
| Should the overview carry exactly three KPI tiles? | Four: canon's lead row is four tiles at every band (s247-D4); the fourth is days of cash cover. |
| Sub-pages as separate files or views? | Views inside one page (`index.html?view=…`), each addressable and restored on reload. |
| Custom date ranges? | Not offered — the filter bar hands custom ranges to the Date-range picker, which is not wired here (named as a gap). |
