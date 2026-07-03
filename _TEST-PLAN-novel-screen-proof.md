# Test plan — novel-screen proof (D2, first real external test)

*The forcing function for review decision 2, shaped 2026-07-03. Two colleagues on novel
work are engaged — this is the **ceiling / craft** track. The churn / floor test (the
business case) runs separately with the other teams; don't collapse them. Built on the kit
already in the repo: `knowledge/_TEST-BRIEF-v2-sme-payments.md` (brief format) ·
`payments-interview-guide.md` · `runs/contract-001-sme-payments/contract.json` (contract
format) · `knowledge/_FIXED-FLEX-CHARTER.md` (the curbs) · `knowledge/_RUNBOOK-criteria-contract.md`.*

## Purpose (read first)

Get a signal from **outside the system** — the thing every green score so far has lacked.
Take **one real screen** from a colleague's novel project, run it through the built engine
with the colleague as the external judge, and prove (or disprove) that
**generate → enforce → compose → register-spread → promote** works on *foreign, real*
material rather than on our own worked example.

## Scope fence — the whole point

**IN — the engine's job, bounded to what's built:**

- one defined screen;
- generate a **register spread** as the **inference ramp** (sober = retrieve · balanced =
  extend · expressive = invent — charter §9, *not* a described look) on **retrieved** curbs —
  **each band in an isolated pass** (no cross-anchoring), with a **divergence probe** on the spread;
- run the blocking gates (compose, contrast, a11y, icons, dark-surface) + advisory (states);
- compose from canon; if the screen needs a **new cluster/lock-up**, derive → gate →
  **promote it** — this is the least-proven, highest-value bit;
- render + one ~20-second taste call.

**OUT — not this test (this fence is what protects against the disappointment scenario):**

- discovery, research, problem-framing — **the colleague owns this** (their job, and the
  engine's weakest, still-unbuilt area);
- the whole journey / multi-screen flow;
- the iteration-machine shell — it's a facade, not used here.

*If the engine stumbles on something OUT of scope, that is not a fail — it's a logged goal.*

## Setup & roles

- **Stakeholder / external judge:** the colleague whose project it is. Not you.
- **Their job:** pick the screen — **one with real compositional latitude** (a cardinal-heavy
  screen like a dense payments table has a narrow road, so the spread will legitimately look
  similar; choose one with room to diverge); write the brief in the `_TEST-BRIEF-v2` five-part format
  (intent + structural licence · register dial · immutable data · correctness rules ·
  design system); own all discovery; and independently supply **their own version** of the
  screen — the comparison baseline (ideally produced without seeing the engine's output).
- **The engine's job:** everything IN scope above.
- **You:** operate the engine, make the taste call visible, capture findings honestly.

## Sequence

1. Colleague picks the one screen and fills a brief-v2 for it (~30 min, with the interview guide).
2. Compile the brief → criteria contract (`_RUNBOOK-criteria-contract.md`).
3. **Colleague agrees the contract — `agreedBy` set — BEFORE anything generates.** Eval-first:
   the definition of done is signed first. A run against an unsigned contract is exploration, not a test.
4. Generate the register spread on the retrieved curbs.
5. Gates run; render; capture what blocked and why.
6. New cluster needed? derive → gate → promote to canon; note it.
7. ~20-second taste call on the survivors.
8. Compare against the colleague's baseline.
9. Capture findings — every gap is a goal, attributed to *built* vs *unbuilt*.

## Success criteria — agreed with the colleague UP FRONT

Not graded by us after the fact. Three bands, all agreed before generation:

- **Built-capability (objective):** gates green; 0 rogue hex / 0 recalled brand values;
  figure fidelity holds; required a11y + safety patterns present (high-value confirm,
  masked refs); any new cluster promoted cleanly; build stays green.
- **Comparison vs the colleague's baseline:** as-good-or-better on-brand fidelity; caught
  ≥1 thing their hand version missed (an a11y fail, a missing state, an inconsistency);
  faster / less rework. **Record honestly if it's worse** — that's the useful bit.
- **The colleague's verdict (the real signal):** "would I take one of these forward?" and
  "did the spread give me a genuine choice, not noise?"

## What a result means

- **Pass** — the loop works on a real stakeholder's real screen. The single most valuable
  evidence in the repo, and the arbiter for D2 / ADR-0006: if the engine breaks on
  *coordination*, add discipline agents on top; if on *thin criteria*, keep going as-is.
- **Fail** — each break is a named, attributed goal. Cheaper and more useful than another
  self-graded pass.

## Honesty

This produces an external signal — nothing more, nothing less. The mock proves nothing;
the gates prove reproducibility; **this** proves it generalises to someone else's real
work. Keep the churn / floor test as the parallel business-case track.
