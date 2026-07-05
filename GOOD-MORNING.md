# Good morning, Dave ☕

*Session briefing — written end of 2026-07-05, session "Decision audit — Tier A batch 1."
Supersedes the earlier 07-05 "From provenance to project-memory: the decision-graph turn" brief.
**Read this, then `_LIVE-STATE.md`, then `knowledge/README.md`.***

## The session in one line

Ran the ADR-0007 §5 correctness audit for the first time — Tier A, batch 1 — moving five
foundational decision nodes out of `unaudited`, fresh-context, with Dave adjudicating each. The
KG's load-bearing claims are no longer taken on trust.

## What landed

Five verdicts (recorded two ways per runbook §5 — ledger line in `knowledge/_DECISION-AUDIT.md`
+ state in `_LIVE-STATE`):

1. **ADR-0005** (engine pivot) — **vouch.** Most-proven node (gates green, GOV.UK second system).
   Note kept open: the token-store history-purge is *conditionally-accepted, not resolved.*
2. **ADR-0007** (decision-graph pattern) — **vouch**, circularity noted (vouched by its own process).
3. **Charter §9/§9a** (inference ramp) — **vouch framing + DEFER proven/safe.** The definition is
   right; the claim it's *demonstrated/safe* is deferred — no worked spread exists, safety
   machinery is named-not-built. Tracked as an explicit **audit-deferred verification** ("we can't
   forget this").
4. **ADR-0006** (flexing engine) — **amend.** Register dial "cool/warm/hot" corrected to the §9
   inference ramp (retrieve/extend/invent). Amended text re-enters `unaudited`.
5. **`derivation-governance`** — **amend.** Core (human-only promotion) vouched; promotion refined
   to a **staged multi-human path** (holding-pen/sandbox → colleague review → **extension library**
   → general canon if broadly useful). Amended text re-enters `unaudited`.

**The batch's real finding:** no *bad* decisions surfaced — the pattern was **decisions ratified
ahead of their proof** (three of five lean on specced-not-built machinery). That's exactly what the
`defer` state exists to hold honestly.

**Forward idea captured (Dave):** the state-management tool should also track **goals + forward
planning** in the same graph ("decisions and goals are the same object at different tenses"), and
be extracted into a **transferable plugin**. Parked with a guardrail — *prove it self-generating
here before packaging.* Memory: `pm-knowledge-graph-direction`.

## On your desk

- **Pushed & clean** — the audit commit (`5cf9837`) is on `origin/master`. Nothing pending.
- **Tier A is not done** — batch 1 of ~3. Two amended nodes still owe a re-audit.

## Queue next (fresh session)

1. **Tier A batch 2 — decision audit.** ADR-0001–0004 + charter §4/§4b. Same protocol: fresh
   context, dossier + devil's-advocate + recommendation per node, Dave adjudicates. Runbook:
   `knowledge/_RUNBOOK-decision-audit.md`; ledger: `knowledge/_DECISION-AUDIT.md`. **Never run in a
   loaded session.**
2. **Re-audit the two amended nodes** — ADR-0006 (register dial) + `derivation-governance` (staged
   promotion). Their edits re-entered `unaudited`; fold into a batch.
3. **PM-KG MVP** — build `_build_live_state.py` + the advisory staleness gate (ADR-0007). This is
   the "prove it self-generating" step that must land *before* the forward-planning / plugin idea
   can be scoped. Own focused session.

Parallel/standing: D2 novel-screen test (waiting on colleague brief) · toolkit tranche 2
(Dropdowns, cheap model).

> Next-session opener: **"Title this chat: <pick one>."** Read GOOD-MORNING.md → `_LIVE-STATE.md`
> → `knowledge/README.md`. Everything is committed and pushed.

## The meter

The audit worked the way it was meant to: fresh context, a written case *against* every node before
a verdict, and honest split/defer/amend outcomes rather than a rubber-stamp. The most valuable thing
it produced wasn't a stack of vouches — it was naming the *shape* of the risk (ratified-ahead-of-
proof) and pinning the deferred proofs so they can't quietly evaporate. Next move is either to keep
clearing Tier A, or to build the MVP that makes the whole ledger self-generating.
