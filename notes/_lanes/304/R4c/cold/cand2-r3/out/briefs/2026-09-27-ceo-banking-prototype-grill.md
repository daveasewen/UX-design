# Grill brief — CEO international-banking prototype

Date: 2026-09-27
Task: Interactive prototype for CEOs of HSBC corporate and institutional clients — overview plus nine linked sub-pages with simulated workflows. Separate from the group-treasurer dashboard.

| # | question | answer |
|---|---|---|
| 1 | Theme | Common (`data-apollo-theme="common"`) — given in the prompt's SETTINGS, not asked |
| 2 | Light, dark or both | Both, with a theme switch |
| 3 | Density and width | Comfortable · wide desktop |
| 4 | Brand assets | The supplied HSBC masterbrand and Apollo tokens. No other assets |
| 5 | Data | Placeholder: realistic entities and currencies, GBP reporting with explicit illustrative FX, 30-day series, enough rows to sort, filter and page |
| 6 | Fixed and off-limits | Apollo accessibility defaults and existing patterns only; invent no components, variants, colours or icons; each component at its own size; no live banking connections or credentials |

Skipped: none (all six answered by the prompt's SETTINGS; nobody was asked — cold run)
Defaults used: none for the six.

Layout (rule 7a "dashboard bento — is that right?"): answered yes by SETTINGS — bento, the section the bento sits in takes the lightest grey, page and title area unchanged.

Discovery — questions I would have asked, and the default taken (nobody could answer):
- Your approval authority? — default: £25m personal limit; payments of £5m and over need two approvers and an audit note.
- How is funding headroom defined? — default: available liquidity (cash + undrawn committed facilities) minus a minimum liquidity buffer (£600m for the group, scaled to the entity/region in view) minus drawn facilities maturing within 60 days.
- Which entities and regions? — default: fictional Meridian Holdings, 8 entities across UK, Europe, Americas, Asia-Pacific, Middle East.
- What makes a risk exception material? — default: utilisation over 100% is a breach (material); 92–100% is near limit.
- Top or side navigation for ten destinations? — default: side navigation (the graph's page-frame `when`: more than 7 destinations).
- In dark mode the ruled grey ground equals the tile surface — acceptable? — default: keep the ruled token, report it.
discovery ended by designer after 0 questions (cold run: questions recorded, defaults taken)
