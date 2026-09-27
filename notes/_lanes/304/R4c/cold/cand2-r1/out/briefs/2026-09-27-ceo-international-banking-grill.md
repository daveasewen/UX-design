# Brief — CEO international-banking prototype (grill, 27 Sep 2026)

Task: interactive prototype for CEOs of HSBC corporate and institutional clients — overview + nine linked sub-pages. New project, separate from the group-treasurer dashboard (not touched).

## The six questions (answered in the prompt's SETTINGS; nobody asked, nobody skipped)

1. Theme — **Common** (`data-apollo-theme="common"`; code key legacy). Square corners.
2. Light / dark — **both**, with a theme switch.
3. Density and width — **comfortable**, **wide desktop**; layout **bento**. The section the bento sits in takes the lightest grey (`--surface-subtle`); the rest of the page and the title area stay on the page ground.
4. Brand assets — **the supplied HSBC masterbrand and Apollo tokens only**. No other assets.
5. Data — **placeholder, realistic**: fictional group "Meridian Global Holdings" (8 entities, 4 regions, 10 currencies), GBP reporting with explicit illustrative FX rates (as at 25 Sep 2026, not live), 30-day time series, enough rows to sort, filter and page.
6. Fixed / off-limits — Apollo accessibility defaults and existing patterns only; invent no components, variants, colours or icons; each component at its own size; no live banking connections or real credentials.

## Discovery (questions I would have asked; nobody to answer — default taken)

- Q: dashboard bento — is that right? → prompt says bento. Taken: yes.
- Q: which three KPIs, and may a fourth join the lead row? → prompt names cash, available liquidity, funding headroom. Default taken: add **committed outflows (next 30 days)** as a fourth tile, because the bento lead group is ruled four across and a 3-of-4 row would be ragged; it also answers "can we fund our plans?".
- Q: how is funding headroom defined? → Default: available liquidity − committed 30-day outflows − policy minimum liquidity buffer. Stated on the page.
- Q: who approves what? → Default: the CEO is the approver of record for payments of £1m equivalent and above; a rejection or a hold needs an audit note (≥ 12 characters); an approval above £10m needs a note too.
- Q: what does "acknowledge a risk exception" commit to? → Default: an audit note (≥ 20 characters) plus a confirmation checkbox; the acknowledgement is time-stamped into the exception's audit trail and persists.
- Q: may exports be real files? → Default: yes, CSV generated in the browser from the filtered data; nothing leaves the machine.
- Q: page frame — side nav or top nav? → The graph's `when` decides: 10 destinations > 7 ⇒ app-shell-side-nav.

discovery ended by designer after 0 questions (cold run — defaults recorded above)
