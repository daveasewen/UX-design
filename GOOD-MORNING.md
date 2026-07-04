# Good morning, Dave ☕

*Session briefing — written end of 2026-07-04, session "Flexing engine, the register
inference-ramp & the review instrument." Supersedes the 07-03 "Toolkit tranche 1" brief
(that thread is paused, not dropped — see On your desk).*

## The session in one line

A strategy-and-governance session, not an ingestion one: the product got a name and shape
(a *flexing* engine, ADR-0006), the register became an *inference ramp* with real machinery
(charter §9), your sketch became a clickable front-end, D2 turned into a real scoped test with
engaged colleagues, and we built a reusable review instrument and used it to reconcile the
three cold-start docs — 6 commits, all pushed.

## What landed

1. **The product shape — a *flexing* engine (ADR-0006).** Re-examined "designer-in-a-box vs
   multidisciplinary agents" (desk research recovered, not re-run) and reaffirmed engine-first
   on necessary-vs-optional + reversibility grounds. Product = ONE engine that flexes by dials
   per work-type: **floor** (churn / "vibe" — BA-instruction → compliant screen = standards-
   compliant Figma Make, the wedge) and **ceiling** (novel / "analysis" — discovery → journey).
   Library compounds via cluster-level promote (least-proven, highest-value bit).

2. **Front-end vision realised — the iteration machine** (`_VISION-iteration-machine_2026-07-03.html`).
   Your notebook sketch → a clickable loop: input → shape (analysis/vibe) → result (cool/warm/hot
   register spread) → refine → loop. **Facade, not wired** — an alignment artifact; palette
   retrieved real, everything else simulated. Proves nothing; the proof is the gates + GOV.UK +
   the real test.

3. **Register = an inference ramp (charter §9).** The big one. Register redefined as the **level
   of inference** (sober = retrieve · balanced = extend · expressive = invent), realised as a
   curb ramp with a floor: **cardinal** curbs (colour, type, angle, logo, a11y, safety) never
   lift; **foundational** curbs (composition, density, motion, red-forwardness…) lift only at
   expressive. Two machinery pieces specced but **NOT built**: isolated generation (kills the
   pollution you spotted) + a divergence probe. Resolved the parked §4 register-reach question.

4. **D2 shaped into a real test.** You've spoken to two colleagues (both novel work). First test
   = a **scoped novel-work screen**: they own the discovery, the engine is bounded to generate →
   enforce → compose → register → promote, success + a comparison baseline agreed up front.
   Churn/floor test = the parallel leadership track. Plan: `_TEST-PLAN-novel-screen-proof.md`.

5. **A reusable review instrument.** A Swiss-styled dossier (frames+stages navigation, HSBC
   colour-coded tags, GitHub-style diffs, severe filter, manual tagging) where I pre-flag
   language and you decide; the export is a **reconciliation register** = decision record + git
   rollback. `_REVIEW-DOSSIER-*.html`.

6. **Reconciled the cold-start trio with it.** Charter (8/8), AGENTS.md (5/5), README (5/5) —
   all agreed, enacted, committed, recorded (`_RECONCILIATION-*-language.md`). **Two were
   propagation catches** — the charter §9 edit left AGENTS' T3 contradicting it; ADR-0005 had
   left README still teaching the retired two-machine rule. The three now agree with each other.

## On your desk

- **The novel-screen test — waiting on the colleague's brief.** When it lands (they fill a
  brief-v2 for one screen + produce their own baseline + sign the contract before generation),
  the engine finally meets someone else's real work. This is **D2, the #1 unlock**.
- **Morning task flagged: "tighten the inference levels — the provenance of 'HSBC-ness'."** The
  qualitative band terms ("must still read HSBC" etc.) need retrieval provenance, not vibes, or
  they default to the model's priors (§5 recall-drift at the register layer). Memory:
  `register-inference-ramp`.
- **Build the divergence machinery** (isolated generation + divergence probe) — named-not-built;
  the unlock for genuine innovation (your F2 question: expressive is *safe* within cardinals by
  construction; whether it *innovates* depends on this).
- **_NEXT-SESSION.md retired** — superseded by this doc (repointed).
- **Parked (longer horizon):** guidance-ingestion-at-scale (the "massive-brain designer" — an
  advisory judge that reads the guidelines per run = G5 at full scale); a11y-depth (the
  compliance KG maps 31 SCs but the gate enforces few — "mapped not enforced" turned inward).
- **Parallel thread paused, not dropped:** the Common Toolkit ingestion — tranche 2 (Dropdown
  ×4) queued for a cheap-model session (memory: `common-toolkit-survey`). Separate workstream.

## Queue next

1. **The colleague's screen → run the novel-screen test (D2).** Everything waits on this.
2. **Provenance tightening** — the "HSBC-ness" morning task (charter §9 qualitative terms).
3. **Continue the review rollout** if wanted — ADRs + runbooks next, same tool, swap the findings.
4. **Build the divergence probe** — the real-innovation unlock.
5. Parallel: toolkit tranche 2 (Dropdowns) on a cheap model when you want a different mode.

> Next-session opener: **"Title this chat: <pick one>."** Read GOOD-MORNING.md first, then
> `knowledge/README.md` for the build. Everything was pushed at writing. The cold-start trio
> (charter / AGENTS / README) is now mutually consistent — trust it.

## The meter

This was the session where the project stopped being "a very good HSBC knowledge base" and
became a *shaped* thing: a named product (flexing engine), a governed generation model (the
inference ramp), a real proof lined up (the colleague's screen), and a governance-hygiene loop
that keeps the docs honest. The review instrument compounding is the tell — two of ten findings
were staleness *we* created that same day, caught automatically. The next real progress is a
conversation (the colleague's brief) and a build (the divergence probe), not more documents.
