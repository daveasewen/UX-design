# Grill brief — corporate international banking dashboard

Date: 2026-10-02
Task: A financial dashboard for corporate international banking (treasury view of a multinational client group), with working filtering and navigation. Requested via `/generate-from-canon`.
Lane: **on-canon** (skills/grill-me → skills/generate-from-canon).

`briefs/` did not exist, so the grill fired. The session conditions route outputs to `out/`, so this brief sits at `out/brief.md` and not at `briefs/2026-10-02-corporate-banking-dashboard-grill.md` (where `skills/grill-me/SKILL.md` would put it). `briefs/` was not created.

| # | question | answer |
|---|---|---|
| 1 | Theme | **Console** — answered. The one theme with rounded corners on controls and surfaces. Root: `class="canon" data-apollo-theme="console"`. |
| 2 | Light, dark or both | **skipped/defaulted, 2026-10-02.** Fallback: **both**. The skill says "both is the usual answer and costs nothing". The page follows `prefers-color-scheme` on first load, and `?mode=light` or `?mode=dark` pins it. No on-screen switch (see GAPS). |
| 3 | Density and width | **skipped/defaulted, 2026-10-02.** No default is declared, so the fallback is stated here: **comfortable** density (the data grid's own default, which the grid's density switch can change); target width **laptop to wide desktop**, built on the 1440px bento wall. The bento bands reflow it at 1100, 820 and 520px container widths. |
| 4 | Brand assets | **skipped/defaulted, 2026-10-02.** Declared default: **mastheads carry the HSBC masterbrand**: `masterbrand-light-colour.svg` on light chrome, `masterbrand-dark-colour.svg` on dark (rule 8a, s230-D2). No other logos, no photography. User-visible product copy says HSBC (s261-D8). |
| 5 | Data | **skipped/defaulted, 2026-10-02.** Fallback: **placeholder, invented rich and deep** (s258-D2). One fictional client group, *Meridian Northwind*: 7 legal entities in 3 regions, 16 accounts in 5 currencies (USD, EUR, GBP, HKD, CNY), 25 month-end balances per account, about 1,200 outgoing payments over 24 months plus about 70 scheduled for the next 30 days, 7 payment statuses, and FX rates to the USD reporting currency. It is generated from one seeded `DATA` builder, so every reload gives the same figures. |
| 6 | Fixed and off-limits | **skipped/defaulted, 2026-10-02.** Fallback: **no extra commitments beyond canon's own**. That means WCAG AA, keyboard operation, and colour never the only channel, all of which the components already carry. Off-limits: the contract's five rules (no invented component, variant, colour or icon; markup from snippets). |

Skipped: 2, 3, 4, 5, 6. A full skip was called after question 1. Discovery did not run (discovery ended by designer after 0 questions).
Bento check, *"dashboard bento — is that right?"*: **skipped, which counts as a yes**. The build is bento-first, on canon's bento grammar.
Defaults used: Q2 both modes · Q3 comfortable, laptop to wide desktop · Q4 HSBC masterbrand · Q5 invented, seeded data · Q6 canon's own a11y floor. Every one was announced in the reply before the build.

Notes: the designer's words, verbatim: "build me a financial dashboard for corporate international banking. Please make the all the interactive elements work such as filtering and navigation."

---

## Decisions the build made in the absence of discovery

Rule 7b says the number of groups and what goes in each is the designer's product decision. Discovery was skipped, so these are **my fallbacks, not choices**. They are listed so they can be overturned.

1. **The questions the screen answers.** (a) Where does our cash stand? (b) How have balances moved, by currency? (c) What is the currency mix? (d) Do balances cover what is already scheduled to go out in the next 30 days? (e) What is driving that outflow? (f) Which payments need action?
2. **Navigation destinations.** Overview (all six groups), Liquidity (a–e), Payments (a, d, e, f). The view lives in `?view=`.
3. **Global filters.** Region, entity and currency, applied through the filter toolbar's "Add filter" menu (OR within a facet, AND across facets). Free-text search covers entity, account, beneficiary and reference. Period presets are 3, 6 and 12 months. All of these drive every KPI, both charts, the runway, the upcoming list and the grid.
4. **Status filtering stays local to the grid** (its own column filter). Status is a property of payments, not balances, so letting it drive the balance charts would be a false claim.
5. **Reporting currency is USD.** All cross-currency totals are converted at the DATA's fixed rates.
6. **Up is bad** (s309-D5, s310-D2 precedent) for *Net FX exposure* and *Failed or returned payments*.
