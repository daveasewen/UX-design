# #229 brief — the cold-start ACCEPTANCE TEST (design intent, revisited)

provenance: chat #228 2026-08-31 — Dave's words, verbatim: "I really don't think we have
settled the whole design intent question yet, we need to revisit and test, I want someone
to prompt for a dashboard and get the result that I got after 5 or so rounds of fettling."

## The shape

The pass condition is HIS: a genuinely cold seat — the v1.0.4 pack installed, nothing else,
no repo access, no session history — is prompted for a dashboard, and the FIRST result
stands comparison with Dave's own rescued international-banking dashboard, which took him
~5 rounds of fettling to reach. Not "follows the contract"; *reaches the destination*.

## What already exists (do not rebuild)

- The #227 regen-diff lane: his artefact beside a by-the-book rebuild, 25 findings —
  `notes/_subreports/2026-08-30-227-dashboard-regen-diff.md` +
  `reviews/DASHBOARD-REGEN-COMPARE-2026-08-30-v1.html`.
- The premise correction that reframed it: his artefact was produced COLD by Sol with NO
  skills loaded — so the bar is what a cold start reaches, not whether the system was used right.
- The cold-start contract (30/40-line DESIGN-CONTRACT + projections), red-teamed, repaired
  #228, C8 landed, SHIPPED in v1.0.4.
- The UNWORKED 32-card dashboard-diff decisions page — the findings the test should
  probably be graded against.

## The test, sketched (for #229 to plan properly, not to enact from here)

1. Cold seat: fresh session, v1.0.4 pack only. Prompt: a dashboard ask phrased the way a
   designer would ask it — NOT phrased to steer toward the contract.
2. Grade the output against his fettled artefact using the 25 regen-diff findings +
   the 32-card page as the rubric. Count: reached cold / reachable with one question /
   unreachable without fettling.
3. The gaps become the next round of skill/contract retuning — the test is the instrument,
   run per cut (this is Memento-shaped: a TEST per item, not a vibe).

## Pitfalls to replay at #229

- The tester must be genuinely cold — a sub with this repo mounted is NOT cold; isolation
  is the hard part of the design. Decide the seat mechanics FIRST.
- Do not let the rubric drift into "matches the contract" — the contract is the means;
  his fettled artefact is the standard (his word, above).
- One cold run is an anecdote, not a measurement — decide n before running.
