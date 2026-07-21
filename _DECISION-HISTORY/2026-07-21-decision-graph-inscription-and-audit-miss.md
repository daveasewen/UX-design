# 2026-07-21 (evening) — Decision-graph inscription: the mechanical pass that caught the seed lying

*Narrative dossier (capture ritual step 1b). WHAT lives in the ledgers (inline `Edges:` lines),
the ADR headers (`Extends:`/`Relates:`), the seed (`notes/_decision-graph-seed-2026-07-21.json`,
now 94 edges + erratum E2) and `_LIVE-STATE.md` LATEST DELTA; this is the WHY/HOW. Both-way links:
the morning's authoring dossier `2026-07-21-decision-graph-edge-convention.md` (which tasked this
pass) · ADR-0012 · ADR-0007 (this is the second half of its unbuilt scope) · worker receipt
`notes/_receipts/2026-07-21-worker-decision-graph-inscription.md`.*

---

## The shape of the session

Opened on "good morning" with the handoff naming the next task as the **Sonnet inscription pass**:
transcribe the seed's edges into ledger entries / ADR headers, verify by generator diff. Dave's
standing instruction ("run the next task with Sonnet 5") matched the handoff's own "Sonnet-able"
framing, so the model choice was already made. Role: **Opus conductor + Sonnet workers** — the
mechanical transcription delegated, the git + capture + judgment kept at the conductor.

The brief looked purely mechanical. It was not. The interesting part of the session is everything
the "mechanical" transcription surfaced.

## Finding 1 — the parser was a stub; verification needed building before it could verify

`parse_inline_edges()` in `_build_decision_graph.py` returned `[]` — a declared interface with no
body. So "verify by generator diff against the seed" could not run until the parser and a `--verify`
mode existed. The first worker built both: a qualifier-aware parser (it has to survive nested parens
and commas *inside* a qualifier's own text — both occur in the real data, e.g. T-D8, R-D20 — so it
locates qualifier boundaries by the known key set, not a blind comma split), plus a `--verify`/`--diff`
mode that matches inscribed edges against the seed by `(from, type, to)` + qualifiers.

It also found a **latent double-count bug**: `main()` concatenated seed + inline edges unconditionally.
Harmless while the parser was a stub (nothing to double), but the instant inscription went live it
would have reported 157 edges instead of 92 — every inscribed edge counted twice. Fixed by merging on
the same key `--verify` uses. Worth noting because it is the classic shape of a bug that hides behind a
stub until the day the stub is filled in.

## Finding 2 — two rulings the convention hadn't nailed, surfaced by the first pass

The first worker inscribed 65 of 92 and **stopped on two genuine gaps** (reflect-back, not guess):

1. **18 ADR→ADR edges.** ADR-0012 says source files keep native syntax; the question was whether ADR
   edges should be inline `Edges:` lines *too*, risking double-count against the native
   `Extends:`/`Relates:` headers.
2. **9 edges sourced from non-ledger nodes** — a charter anchor (`CHARTER.S9`), a proforma def
   (`DEF-006`), a dated TYPE anchor (`sat-ceiling`), and five `conflicts-with` edges owned by guideline
   REVIEW rules (`ill-007`, `mot-007`, `type26-015`, `webf-032`, `ctkb-015`). ADR-0012 says REVIEW
   rules aren't re-authored but never says *where their edges live*.

Both went to Dave in plain language. He ruled: **(1)** ADR edges live in native `Extends:`/`Relates:`
headers — matching ADR-0012's own header, the precedent it set for itself; **(2)** the 9 non-ledger
edges are inscribed **at source**, each in its own file, so the rule stays uniform: *a node's edges
live at that node.*

## Finding 3 — the seed was the incomplete side, and the worker "fixed" it backwards

This is the session's real lesson. Enacting Ruling 1, the second worker hit a disagreement: ADR-0010's
header declared `Extends: … ADR-0004 (WCAG floor)` and ADR-0011's declared `Relates: … R-D17 (leak
gate)`, but **the seed contained neither edge.** The worker resolved it by **trimming the ADR headers**
to match the seed — deleting two real, ratified relationships to make the diff clean.

That is backwards. The seed is an *audit* (the Fable read); the ADR headers are *ratified decisions*
Dave accepted. When they disagree, the audit is the fallible side. The correct reconciliation is the
opposite: **restore the headers, add the two missing edges to the seed.** Which is what the conductor
did — 92 → 94 edges, logged as **erratum E2** in the seed with the rule stated so it can't recur:
*on header-vs-seed disagreement the ratified header wins; add to the seed, never trim the header.*

Both edges are coherent on inspection (ADR-0009 already declares the same ADR-0004 link; ADR-0010
already declares the same R-D17 link), so these were audit omissions, not over-claims. The value of the
whole decision-graph exercise is exactly this kind of catch — and here the machinery caught its own
author's blind spot.

## Finding 4 — the conductor's own false correction (inscribed loudly, per the ethos)

Mid-session I told Dave the ADR headers "carry no edges," having grepped `^\*\*(Extends|Relates)` —
line-anchored, so it missed the fields that sit *inline* after `**Status:**`. Every ADR (0006–0012)
carries them; the original GOOD-MORNING claim I had "corrected" was right all along. Retracted in the
same turn. Recorded here because it is a live instance of the project's central failure mode —
confident false inscription — committed by the agent, not the handoff, and because the fix was not
"be more careful" but a concrete tool lesson: **a line-anchored grep is not a search for an inline
field.** Verify the tool matches the shape of the thing before trusting a null result.

## Resolved state

- All 94 edges inscribed in their ruled homes; `--verify` = 94/94, zero mismatch; build green 38/38.
- Committed `4a6f442` (Dave pushes via GitHub Desktop).
- Seed carries E2; the header-wins rule is in `_LIVE-STATE` LATEST DELTA and this dossier.

## Still open

- **ADR-0007 part 2** — remaining temporal-decision-graph scope.
- **Promote the conflict gate advisory → blocking** once the corpus settles (it is advisory step 11/38 today).
- **Dave's amber-tier context-gauge proposal** (in `_FUTURE-STATE.md`): a light spine-flush at Amber,
  full ritual + fresh session reserved for Red. Awaits his nod before the gauge runbook changes.
