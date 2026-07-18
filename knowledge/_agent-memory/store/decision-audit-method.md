---
name: decision-audit-method
description: "Correctness-audit method for the decision corpus — runbook designed 2026-07-05, not yet run; where it lives + how it works"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5e768e8c-07ed-4330-9dbd-2c553b8da5ec
---

Method for the ADR-0007 §5 correctness audit is DESIGNED (2026-07-05, in a loaded session) but
NOT YET RUN. Don't re-derive it — read the runbook.

**Runbook:** `knowledge/_RUNBOOK-decision-audit.md`. **Interim ledger:** `knowledge/_DECISION-AUDIT.md`
(coverage table + one-line verdict log). Tracked as OPEN in `_LIVE-STATE.md`.

**How it works:** validation state (`unaudited → vouched / amend / overturn / defer`) is orthogonal
to lifecycle (live/dead). Triage the corpus into Tier A (foundational: 7 ADRs + charter §4/§4b/§9/§9a
+ LIVE-STATE entries, ~20 nodes — do first), B (process/method memories), C (long-tail DS rulings —
sampled + on-touch). Batch protocol: 5–8 nodes, **fresh context per batch**; Claude builds a
one-screen dossier + a devil's-advocate case + a recommendation; **Dave adjudicates**. Promotion to
`vouched` is human-only, never derived (the [[derivation-governance]] rule applied to decisions).

**Why:** the KG retains state but nothing is checked for correctness — a wrong decision with a tidy
edge looks vetted (the graph launders it). This is the guard.

**How to apply:** RUN it only in a cold session (a loaded one can't impartially grade its own
decisions). First run = Tier A batch 1: ADR-0006, charter §9/§9a, ADR-0007, ADR-0005,
[[derivation-governance]]. Pairs with [[pm-knowledge-graph-direction]] (the KG this validates) and
[[critical-review-2026-07-02]] (D-items). Commit `882361e`.
