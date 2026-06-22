# A vs B — gated composer vs Figma Make

*Same job. Same spec. Same fixed dataset. Two generators. One gate.*
*Route A = composed from HSBC canon (emits `route-A.screen.json`). Route B = Figma Make, fresh generation from `figma-make-prompt.md` (code export, hand-transcribed to `route-B.screen.json`).*

## Verdict — read this first
**Both screens PASS gate 2** (6/6 blocking; A: 0 advisory flags · B: 1 advisory flag). The headline is **not**
"the commodity tool fails." Given a tight, explicit spec with exact figures and consistency rules, **Figma Make
produced a sound, consistent, gate-passing screen** — a world away from the earlier restyle that failed 6/6.
The real differences are narrower and more interesting than pass/fail.

## The scorecard
| Check | Route A — canon | Route B — Figma Make |
|---|---|---|
| DATA-1 cross-panel amounts reconcile | ✅ | ✅ |
| DATA-2 stated total = Σ rows | ✅ | ✅ *(computed from rows)* |
| DATA-3 coverage backed by the data | ✅ | ✅ |
| A11Y-1 action-tile contrast | ✅ | ✅ *(no tiles rendered — nothing to test)* |
| BRAND-1 no decorative red | ✅ | ✅ *(no rainbow tiles)* |
| FLOW-1 high-value approval needs confirm | ✅ *(static note)* | ✅ **modal + "exceeds £10k, verify signatory"** |
| COPY-1 one currency format | ✅ | ✅ |
| COPY-2 no all-caps | ✅ | 🟡 7 all-caps labels |
| PII-1 masking | ✅ | ✅ |
| **Gate exit code** | **0** | **0** |
| — *not yet gated* — | | |
| Checkable by construction | ✅ native `screen.json` | ❌ 625 lines of React, hand-transcribed |
| Brand-token fidelity | ✅ `#DB0011` + teal `#00847F` + square + sentence case | ⚠️ `#DB0011` + square ✓; **generic green not teal**, 7 caps |

*(On FLOW-1, Route B was actually **better** than my canon composer — a real confirmation modal vs a static note. Worth saying plainly.)*

## What this actually proves — three findings
1. **The spec did the heavy lifting.** The first Figma Make screen (a restyle of a buggy image) failed 6/6 —
   garbage in. The *same tool*, given a clean spec + exact dataset + explicit consistency rules, passed. This
   validates **spec/eval-first (station ①)**: the criteria are the lever, not the generator.
2. **The gate's real job is impartial verification — not catching dumb tools.** It cleared A and B alike. Its
   value is that *you can ship generated UI in a bank because something independent verified it*, whatever made
   it. That's the moat: **spec (upstream) + enforcement (gate)**. Generation is genuinely commodity — exactly
   the locked strategy, now with evidence instead of assertion.
3. **Two residual edges for the canon route — one structural, one a gap to close:**
   - *Checkability asymmetry (structural, real):* Route A emitted a data model → the gate ran in milliseconds.
     Route B had to be reverse-engineered from 625 lines of React before it could be checked at all. Gated
     generation is **verifiable by construction**; commodity output is opaque and must be transcribed. At scale
     that's the gap between continuous enforcement and manual audit.
   - *Brand-token fidelity (the gate can't see this yet):* B nailed brand red and square corners but used a
     generic green for "positive" instead of your `rag/success` teal `#00847F`, and 7 ALL-CAPS labels. A used
     exact canon tokens. **Gate 2 doesn't test token fidelity** — so it scored this a tie. That's the next gate
     to build, and it's where canon has a measurable, defensible edge.

## Honest caveats
- **n = 1.** One spec, one run each — a demo, not proof. Repeat across several specs before claiming a measured win.
- **"Route A composer" = hand-assembly from canon** (the manual station ②), not an automated composer yet.
- **Gate 2 is six checks.** It doesn't yet test token fidelity, focus order, reflow, or states.

## The demo story (sharper + honest)
> "Same spec, two generators. **Both pass the gate — because the gate and the spec are the product, not the
> generator.** The differences left are that one screen is checkable by construction and token-faithful; the
> other had to be reverse-engineered and only approximates the brand."

## Next build this points to
A **brand-token-fidelity check** (gate 2.1): does the screen use canon token *values* (the teal success token,
sentence-case labels)? That's the one place B measurably trailed A — and the gate can't currently see it.

## Update — gate 2.1 built, and it separates them
`gate2_1_tokens.py` loads the real palette and **derives** the success/primary anchors from `semantic-colour.json`
(nothing hand-coded). Result:

| Check | Route A — canon | Route B — Figma Make |
|---|---|---|
| TOKEN-1 positive = canon success teal | ✅ `#00847F` | 🔴 `#1A7A3C` (generic green) |
| TOKEN-2 primary = canon brand red | ✅ | ✅ |
| TOKEN-3 square corners | ✅ | ✅ |
| TOKEN-4 palette drift *(advisory)* | 🟡 2/15 off (`#F7F7F7`, `#1A1A1A`) | 🟡 10/12 off-canon |
| TYPE-1 sentence case *(advisory)* | ✅ | 🟡 7 ALL-CAPS |
| **Gate 2.1 exit** | **0 — PASS** | **1 — FAIL** |

**The two gates together tell the whole story.** On *soundness* (gate 2) A and B **tie** — the spec carried the
commodity tool. On *brand fidelity* (gate 2.1) they **separate**: B got the brand red and square corners but
rendered "positive" in a generic green instead of your `rag/success` teal, plus 10 off-canon colours and 7
all-caps labels. The canon composer is faithful by construction; the commodity tool approximates — **and that
difference is now enforceable, not a matter of opinion.**

*(Honest note: Route A isn't spotless either — 2 of its neutrals are off-canon and the gate flagged them. Good.
An impartial gate that also dings your own output is working correctly.)*
