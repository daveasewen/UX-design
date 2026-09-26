# Grill brief — CEO international-banking prototype (2026-09-26)

Source: the designer's prompt, SETTINGS block ("already decided, do not ask"). No live designer was available; every answer is quoted or paraphrased from the prompt, and gaps are recorded as defaults.

## The six questions

1. Theme — Common (`data-apollo-theme="common"`; square corners). Quoted: "Theme: Common."
2. Light, dark or both — both, with a theme switch. Quoted: "Light and dark, with a theme switch."
3. Density and width — comfortable density, wide desktop, bento layout. The section the bento sits in takes the lightest grey; the rest of the page and the title area stay as they are.
4. Brand assets — the supplied HSBC masterbrand and Apollo tokens. No other assets.
5. Data — placeholder: realistic entities and currencies, GBP reporting with explicit illustrative FX rates, 30-day time series, enough rows to sort, filter and page.
6. Fixed / off-limits — Apollo accessibility defaults and existing patterns only; invent no components, variants, colours or icons; each component as the pack gives it, at its own size; no live banking connections or real credentials. Do not overwrite the treasurer screen, canon, tokens or validators.

## Discovery (no designer present — questions recorded, defaults taken)

- Q: dashboard bento — is that right? A: yes, stated in the prompt ("Layout: bento").
- Q: ten destinations — top bar or side column? Default: App-shell-side-nav, because its roles.json when is "> 7 destinations" and the prompt lists ten.
- Q: one page with views, or ten files? Default: one file (index.html) with ten hash-routed views.
- Q: reporting date? Default: figures to 25 September 2026, 30 daily points.
- Q: what makes a payment need a second look? Default: GBP 5m or more asks for an approval note; a rejection always needs a reason.
- Q: which risk exceptions are material? Default: limit utilisation at or above 100%, or at or above 90% for a counterparty rated below A-.
- discovery ended by designer after 0 questions (no designer present); the defaults above are fallbacks, not choices.
