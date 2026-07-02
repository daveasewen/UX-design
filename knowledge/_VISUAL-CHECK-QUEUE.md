# Visual-check queue — needs Dave's eyes

Autonomous work is gate-verified for *correctness* (tokens, contrast, ARIA, build). This queue
collects the things a gate **can't** judge — appearance, motion feel, layout/canon calls. Skim
when you're back; nothing here is blocking.

| # | Item | What to check | Where |
|---|------|---------------|-------|
| ~~V1~~ | ~~`text/secondary` token~~ | ✅ **SIGNED OFF (Dave, 2026-06-20)** — visual review, values unchanged; promoted to `asserted`. (Inverting-label canon confirmed in the same pass.) | — |
| V2 | 4 baseline organisms | Layout/canon review — these were built as baselines, not yet design-signed. | Navigations, Headers, Hero, Video-player `.reference.html` |
| V3 | Screen-reader / keyboard pass | Static a11y is fixed + gated, but AT behaviour needs a human: Modal focus-trap + return, Dropdown listbox announce order, Tabs arrow-key/roving-tabindex. | `_A11Y-AUDIT.md` §"Priority for the human pass" |
| V4 | Zoom / reflow (1.4.10) | 200% zoom + text-spacing on the organisms — does layout hold? | organism snippets |
| V5 | Table (newly built) | Baseline — semantic/tokens/contrast gated, but **sort affordance** and **small-screen reflow strategy** need design review (currently horizontal-scroll). | `Table.reference.html` |
| V6 | Button fidelity vs. prior dev (Dave flag, 2026-06-20) | Gated `Button.reference.html` looks more basic than the button developed in an earlier session — check if the snippet drifted from / is behind better prior work, and reconcile. Token bindings are signed off; this is component polish, not tokens. | `Button.reference.html`, git history, `_fitness-test/` |
| V7 | Cards uses wrong link atom (Dave flag, 2026-06-20) | Gated `Cards.reference.html` embeds a link treatment that isn't the canonical `Links` atom — verify and rebind to the real atom. Cross-component consistency, not a token call. | `Cards.reference.html` vs `Links.reference.html` |

_Updated 2026-06-20._
| V6 | Minted token proposals (2026-07-02) | 10 PROPOSED tokens in the holding pen (`tokens/_proposals/semantic-colour.proposals.json`) — NOT in the resolving store — `inverse/surface`+`inverse/text` (the balanced dark band), `gradient/expressive/*` (4 stops, expressive-only), `data/series-1..4` (G7 — likely superseded: Dave supplying a real palette; derivation stays as format spec). All derived+aliased from existing primitives, all contrast-receipted, build green. Judge the LOOK: band value (#1D1D1D vs alternatives), gradient warmth, series distinctness incl. colour-blind check. | `tokens/_proposals/semantic-colour.proposals.json` + `_fitness-test/v6-token-proposals.html` |
| V7 | Charting series assignment from the OFFICIAL supporting palette | Dave supplied the brand-refresh supporting palette (50 values, 10 families — `tokens/_proposals/supporting-palette.proposals.json`, provenance + per-value contrast receipts inside). Judgment needed: which family/step becomes `data/series-1..N` in light and dark (33/50 are indicator-legal on white, 39/50 on black — the pastels need their 4/5 steps in light mode). Guidance captured: no rainbow treatments; two complementary hues where possible. Supersedes the V6 `data/*` derivation. **DEFERRED 2026-07-03 →** sheet ready (`_fitness-test/v7-series-assignment-AB.html`, candidates A/B/C, all receipts); rules ingested (`guidelines/data-visualisation.md`); standing recommendation: **B + usage rule** (mint B as series-1..4; ≤2 data sets → series-1+3, the complementary pair; ordered data → family ramp — satisfies both guidance rules by selection). | `tokens/_proposals/supporting-palette.proposals.json` |

