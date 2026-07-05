# Runbook — decision-corpus correctness audit

*The method for moving decision nodes from `unaudited` → `vouched` (or `amend` / `overturn` /
`retire`). Designed 2026-07-05 in a loaded session; **executed only in fresh, batched sessions.**
Anchor: ADR-0007 §5 (validity ≠ provenance; promotion is human-only, never derived). Reuses
`_CONFIDENCE.md` tiers + the `_REVIEW-QUEUE` pattern. This runbook is a method, not a run — running
it is the OPEN thread in `_LIVE-STATE.md`.*

---

## Summary (read this, skip the rest until you run it)

1. **The problem it solves.** The KG now retains state but nothing in it is checked for
   *correctness*. Every node is `unaudited`. A wrong decision with a tidy edge *looks vetted* — the
   graph launders it. This audit is the guard.
2. **The one rule.** Promotion to `vouched` is **Dave's judgment, in a fresh context, never
   derived** by the engine. Claude assembles evidence and argues both sides; Dave adjudicates.
3. **The shape.** Triage the corpus into three tiers by cost-of-being-wrong. Audit Tier A first,
   in **small batches (5–8 nodes)**, one fresh session per batch. For each node Claude builds a
   one-screen dossier + a recommended verdict + a **devil's-advocate case against it**; Dave rules.
4. **The teeth.** Verdicts are recorded in `_DECISION-AUDIT.md` (interim ledger) and written back
   as a `validation:` state on the node. The staleness gate stays *consistency-only* and must never
   imply a node is valid.
5. **Where to start.** Tier A = the 7 ADRs + the charter's ratified rulings (§4, §4b, §9/§9a) + the
   `_LIVE-STATE` LIVE entries. ~20 nodes, ~3 batches. Do these before anything else.

> **Do NOT run this in a loaded context** (this session included). A session that already argued a
> decision cannot impartially audit it. Fresh context per batch is the safeguard, not a formality.

---

## 1. What a "decision node" is

The unit of audit. A node is one recorded decision, wherever it lives:

| Source | Examples | Node granularity |
|---|---|---|
| **ADRs** (`docs/decisions/`) | ADR-0001…0007 | one node per ADR |
| **Charter rulings** (`_FIXED-FLEX-CHARTER.md`) | §4 ratified curbs, §4b temperature, §9 inference ramp, §9a provenance | one node per ratified ruling/section |
| **Memory decisions** (`MEMORY.md` → files) | `feedback` + `project` type memories that encode a ruling (e.g. `git-push-method`, `derivation-governance`, `type-rule-sentence-case`) | one node per memory that asserts a decision |
| **`_LIVE-STATE` LIVE entries** | the current-truth bullets | audited via their source ADR/charter/memory (don't double-count) |
| **Design-system rulings / logs** | `_DS-IMPROVEMENTS.md`, desk-ruling batches, ingest register (~462 items) | Tier C — sampled, not exhaustively audited |

A node carries, for the audit: an **id**, the **decision statement** (one sentence), **ruled date +
source**, its **lifecycle state** (live / superseded — already in `_LIVE-STATE`), and the thing this
runbook adds: a **validation state**.

## 2. The validation-state machine (distinct from lifecycle)

Lifecycle answers *is it in force?* Validation answers *is it right?* They are orthogonal (a live
node can be unaudited; a superseded node can have been vouched before it was replaced).

```
unaudited  ──audit──▶  vouched      (correct as written — promote)
                   ├─▶  amend        (right intent, wrong detail — edit, then re-audit the edit)
                   ├─▶  overturn      (wrong — supersede it via normal discipline; log propagation)
                   └─▶  defer         (can't judge yet — needs evidence/a colleague/a test first)
```

Rules (from ADR-0007 §5):

- The whole backlog **seeds as `unaudited`** — honest by default.
- `unaudited → vouched` is a **human correctness-audit only, never derived.** No generator, gate, or
  heuristic may set `vouched`.
- The staleness gate enforces *consistency* (live docs don't cite dead nodes) and **must never
  imply validity.** A clean, consistent node is not a vetted one.
- `amend` and `overturn` both re-enter the supersession discipline (tombstone + propagation log);
  `overturn` on a foundational node is a real event — expect follow-on work.

## 3. Triage — audit the expensive-to-be-wrong first

Score each node on **cost of being wrong = blast-radius × irreversibility.** Bucket into three
tiers; depth of audit differs per tier.

- **Tier A — foundational (full audit, one node at a time).** Nodes other decisions stand on:
  the 7 ADRs, charter §4 / §4b / §9 / §9a, and any `_LIVE-STATE` LIVE entry not covered by those.
  Being wrong here corrupts everything downstream. **Start here.** ~20 nodes.
- **Tier B — method / process rulings (batched audit, 5–8 per session).** The `feedback` and
  `project` memories and runbook rules that shape how work is done (e.g. git split, derivation
  governance, sentence-case, code-binding hub-and-spoke). Wrong here wastes effort but is
  recoverable. ~30–40 nodes.
- **Tier C — long-tail design rulings (sampled, not exhaustive).** The ingest register (~462),
  `_DS-IMPROVEMENTS`, per-token desk rulings. Audit by **spot-sample** (e.g. 10% + every entry a
  Tier A/B node depends on) and **audit-on-touch** (validate a Tier C item the first time a live
  build actually leans on it). Exhaustive audit here is not worth Dave's time.

Produce the tiering **before** the first audit session (Claude can generate a first-pass tiered
worklist; Dave corrects it). Reuse the `_REVIEW-QUEUE` 🔴/🟡 convention for within-tier urgency.

## 4. The batch protocol (what a fresh audit session does)

Each audit session is self-contained. It opens cold, audits one batch, records verdicts, closes.

**Setup (fresh context — this is load-bearing).**
Open a new session. Read `GOOD-MORNING` → `_LIVE-STATE` → this runbook → the tiered worklist. Do
**not** load the session that authored the decisions under audit. Title it e.g. *"Decision audit —
Tier A batch 1."*

**Per node, Claude prepares a one-screen dossier** (retrieval, not recall — cite the file/line):

1. **Statement** — the decision in one sentence, as recorded.
2. **Provenance** — where/when it was ruled, by whom, what it superseded.
3. **Rationale as recorded** — why it was made (quote the source, don't reconstruct).
4. **Dependencies** — what now stands on it (from `_LIVE-STATE` / edges / blast-radius).
5. **Challenge (the devil's-advocate case)** — the strongest honest argument that it is *wrong,
   outdated, or wrongly scoped.* Kept **visually separate** from the recommendation (Dave's method:
   convergent and divergent stay apart). Include any contradicting signal already in the repo.
6. **Recommended verdict + confidence** — Claude's call (`vouched` / `amend` / `overturn` /
   `defer`) with a one-line why, explicitly marked as a *recommendation, not a ruling.*

**Dave adjudicates.** He rules per node: vouch / amend / overturn / defer. He can accept, invert,
or ignore the recommendation — the recommendation exists to save reading time, not to anchor him.
One question at a time where a call is genuinely his (contested or judgement-heavy nodes).

**Batch size 5–8.** Small enough that each node gets real attention; a 40-node "batch" is a
rubber-stamp with extra steps. Stop the session at the batch boundary even if there's appetite —
fatigue is where laundering creeps back in.

## 5. Recording verdicts (the teeth)

Two writes per adjudicated node:

1. **Node write-back.** Set the validation state on the node — front-matter `validation: vouched`
   when the generated system exists; until then, an entry in the interim ledger below. `amend`
   edits the node then resets it to `unaudited` (the edit must itself be audited). `overturn`
   triggers the supersession discipline (tombstone + `_LIVE-STATE` move + propagation-gap log).
2. **Audit-ledger append.** One line in `_DECISION-AUDIT.md` (new, interim — mirrors
   `_LIVE-STATE`'s interim status): `node-id · verdict · date · one-line basis · auditor=Dave`.
   This is the provenance of the *audit itself*, so a future session can see not just that a node is
   vouched but why and when.

The staleness gate later reads validation states to **report coverage** (“Tier A: 14/20 vouched, 2
deferred”) — it reports, it never promotes.

## 6. Definition of done + cadence

- **Per batch:** every node in the batch has a verdict + two writes; `_DECISION-AUDIT.md` and
  `_LIVE-STATE` updated; a one-line handoff of what's left.
- **Per tier:** Tier A fully vouched/amended/overturned (no `unaudited` foundational nodes) is the
  first real milestone — it's the point the KG stops laundering its *load-bearing* claims.
- **Cadence:** run Tier A to completion first (≈3 batches), then Tier B opportunistically (one batch
  as a warm-up in otherwise-light sessions), Tier C by sample + on-touch indefinitely.
- **Never "done" globally** — audit is standing hygiene. But *Tier A clean* is the bar that retires
  the "everything is unaudited" risk named in `GOOD-MORNING` / `_LIVE-STATE`.

## 7. Anti-rubber-stamp safeguards (why this won't just bless everything)

- **Fresh context per batch** — the session that made a case can't impartially grade it.
- **Mandatory challenge** — every node gets a written case *against* before a verdict; a node with
  no honest counter-argument is suspicious, not safe.
- **Human-only promotion** — no automated path to `vouched`; the gate can flag inconsistency but
  never vouches.
- **Bounded batches** — 5–8 nodes; fatigue-driven blessing is designed out.
- **Recommendation ≠ ruling** — Claude's call is labelled and separable so it informs rather than
  anchors.
- **Defer is first-class** — "can't judge yet" is a valid, honest outcome; it does not decay into a
  soft yes.

## 8. First run — concrete starting worklist

When the first fresh session opens, Tier A batch 1 should be the highest-blast-radius nodes:

1. **ADR-0006** — flexing-engine product shape (everything about generation stands on it).
2. **Charter §9 / §9a** — register = inference ramp + provenance of "reads HSBC."
3. **ADR-0007** — the decision-graph pattern itself (audit the auditor's foundation).
4. **ADR-0005** — knowledge-engine pivot ratification.
5. **`derivation-governance`** — engine never derives-and-promotes (the rule this whole audit
   embodies; vouch it deliberately).

Batches 2–3 clear the remaining ADRs (0001–0004) and charter §4 / §4b. Then Tier B.

---

*Cross-refs: ADR-0007 (anchor) · `_CONFIDENCE.md` (tiers) · `_REVIEW-QUEUE.*` (pattern reused) ·
`_LIVE-STATE.md` (lifecycle ledger this complements) · AGENTS.md (supersession discipline that
`overturn`/`amend` re-enter).*
