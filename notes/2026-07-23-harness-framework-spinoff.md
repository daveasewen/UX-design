# Spin-off idea — the session harness as a replicable framework / pro-forma

*Recorded 2026-07-23 (routing side-quest session, worker, Fable) at Dave's ask: "can you record
this idea so i can retrieve later, i think this process is quite solid, i think some people on my
team might feel the benefit." Provenance of the idea: Dave in-session — "this harness that we've
built, do you think it's replicatable, i.e. could we use it as a pro-forma if others wanted to use
it?" … "or a framework, however we phrase it." Status: IDEA, registered for `_FUTURE-STATE` via the
session receipt (`notes/_receipts/2026-07-23-routing-sidequest-audit.md`); conductor makes that
write.*

## The idea in one line

Extract the Apollo session-operating harness — the memento architecture + method runbooks, minus
the design-system knowledge — as a standalone framework Dave's team can adopt for their own
agent-assisted work.

## Why we believe it separates cleanly (evidence, not hope)

The 2026-07-23 routing audit (`reviews/ROUTING-AUDIT-2026-07-23-v1.html`, all 13 proposals
ratified) mapped the whole corpus onto a three-layer model and found the seam already exists:

- **Invariant layer** (travels as-is): the memento *format* — GOOD-MORNING §A/§B/§C, `_LIVE-STATE`
  spine, capture ritual, receipts, divvy plans, supersession discipline, the tattoo/Polaroid trust
  hierarchy, evidence-pointered "done" claims (#7, now inscribed).
- **Method layer** (travels as skeletons): conductor/worker parallel model · context gauge ·
  MODEL-ROUTING (freshly Fable-era-audited — the most portable single file) · review-overlay loop
  (`_make_review.py` — already ruled product-grade) · verification-as-enforcement as a PATTERN
  (build runner + selftests-as-build-steps + assertions register; the shape, not Apollo's checks) ·
  runbook house style + generated index.
- **Knowledge layer** (stays home): tokens, gates' actual checks, ledgers, ADRs — the Apollo
  design system itself. A team adopting the framework brings their own.

Independent evidence of portability: Dave's external routing research mapped onto the corpus with
almost no friction — much of the doc's advice turned out to be things the harness had already
invented (toolkit-tranche = the "older-model appendix" pattern; Mode 3 = route-at-the-seam).

## What does NOT travel verbatim

- **Environment quirks** → become an "environment appendix": sandbox git lock dance, the ~200k
  gauge numbers, the render-verify pipeline, Cowork/Code surface differences.
- **Dave-specifics** → scrub/parameterise: rulings-as-examples, comms preferences, HSBC material.
- **The operating culture.** The habits (reflect-back, verify-before-asking, supersession
  discipline) are encoded in the documents' WHY-prose — a bare template hands over files, not
  habits. This argues for **framework-with-narrative** over bare template.

## Packaging options (Dave rules when picked up)

1. **Cowork plugin** — skills for capture-ritual / conductor / gauge / routing; installable, not
   copyable; the create-cowork-plugin skill exists. Likely best for the team.
2. **Template repo** — skeleton GOOD-MORNING, runbook set, build-runner shape. Cheapest.
3. **Framework document** — a written charter first; slowest to adopt, best carrier of the why.

## First concrete step when resurrected

One-page **harness charter** naming the invariant/method seam, then extract file-by-file. Related
standing memory: `spin-off-candidates` (generalise reusable tools; register in `_LIVE-STATE`) and
`graphify-tool` (the sibling precedent).
