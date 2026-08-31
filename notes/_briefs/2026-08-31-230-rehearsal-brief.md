# Brief — #230 rehearsal lane (Opus): drive the cold prompt against Dave's pass condition

provenance: 230 · 2026-08-31 · conductor Fable · row W-317
Runs AFTER the enact lane (W-316) lands. Demo 2026-09-01 (W-308).

## The pass condition (Dave's goal, from the demo-day brief — the ONLY rubric)

A dashboard prompt produces a build that: (1) declares the on-canon lane · (2) goes
bento-first OR asks "dashboard bento — is that right?" · (3) copies markup from
`knowledge/snippets/` with canon tokens, zero invented markup · (4) lands structure/design
toward `dashboards/international-banking-dashboard.canon.html`'s LOOK while sharing none of
its code · (5) grill-me fires where the contract says, and the SKIP works. Anything short is
a FINDING to fix in the components tonight — findings are the point, never hidden.

## Seat mechanics (decided here so you don't re-derive)

- DECLARED APPROXIMATION of W-304, not the acceptance test (`s229-D1` gates that behind
  Dave's satisfaction; this is demo prep). Not Copilot, not a corp machine — say so in the
  report header.
- Cold-ish seat: unzip `apollo-spider/dist/Apollo-Spider-v1.0.4.zip` to a scratch dir OUTSIDE
  the repo mount view of your builder (work in `outputs/`), and drive the build USING ONLY
  the pack's contents — its skills, contract, snippets. ⛔ You must not read the repo's
  `knowledge/` or `reviews/` while wearing the builder hat. Two hats, declared per step:
  BUILDER (pack-only) and GRADER (repo allowed).
- Prompt, verbatim, phrased as a designer would ask (NOT steered toward the contract):
  "Build me an international banking dashboard for a corporate client — balances, payments
  activity, FX exposure, alerts."
- n=1 is an anecdote — say so; the finding list, not the pass/fail, is the deliverable.
- Grade beat-by-beat against the 5-point pass condition; for (4), compare LOOK by eye
  against a render of Dave's artefact (render it as a reference image — that use is legal;
  its CODE stays untouchable).

## DO-NOT-RULE

No `_rulings.json`, no W-rows, no memory, no git, no canon/snippet/pack edits — the fix
list goes in the report for the conductor/next lane. No release machinery.

## Report

`notes/_subreports/2026-08-31-230-rehearsal.md` — header declares the approximation ·
COUNTS: (beats passed N/5, findings F, fettling rounds needed R) · the transcript of the
builder's key decisions · REPLAY-THESE: · RULING-SHAPED QUESTIONS (re-screen surviving
triage questions here per the demo-day brief: "Dave's look, or Sol's improvisation?" —
pointing questions only). Chat STUB: beats N/5, findings count, the single sharpest finding,
and whether the bento question / grill-me skip fired.

## Pitfalls — replayed

- The builder hat reading repo files = the rehearsal proves nothing (the seat was warm).
  Declare every file the builder read.
- Render-verify per the receipted recipe (fonts are session-path-bound and fail silently —
  three-way probe; `TMPDIR=/dev/shm`; ~178s wall).
- Grading "matches the contract" instead of "reaches the look by the component path" is the
  drift the W-304 brief warns about — the look is the standard, the contract is the means.
