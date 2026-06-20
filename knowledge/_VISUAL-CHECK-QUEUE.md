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

_Updated 2026-06-20._
