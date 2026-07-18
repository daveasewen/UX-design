---
name: pm-knowledge-graph-direction
description: "Context-staleness (superseded artifacts resurrected by cold starts) is a missing-edge problem; the recursive fix = apply the design-KG pattern (nodes/edges/derived-views/gate) to the PROJECT/PROCESS layer — supersession as a first-class edge, generated _LIVE-STATE view, staleness gate. MVP not full graph."
metadata: 
  node_type: memory
  type: project
  originSessionId: 894cbd65-929b-4fca-b61c-0d3eeef00e57
---

RAISED 2026-07-05 (Dave, after a cold start wasted a session resurrecting the retired looks-based register dial). Dave: "I need a foolproof repeatable solution… would a knowledge graph for project management help with context and arbitration?"

**Root cause named:** context staleness is a **missing graph edge**. §9 (decision) *superseded* registers.html (artifact) but that edge was never recorded → no "what's live" view existed, no gate flagged the live-looking corpse, so a grep resurrected it.

**The recursion (the key insight):** Dave ALREADY solved this — for the DESIGN domain. knowledge/ = authored nodes (components/tokens/rules) + edges (relationships, `_blast-radius.json`) + derived views (generated, never hand-edited) + integrity gate. The PROJECT/PROCESS layer has none of that (prose docs + atomized memory) — which is exactly why it rots. Fix = mirror the same shape onto decisions & artifacts:
- **Nodes:** decisions (ADRs/rulings), artifacts (files/mocks/spreads), open threads, experiments.
- **Edges:** `supersedes`/`superseded-by`, `propagates-to`, `derived-from`, `tests`, `blocks`; status = live/superseded/experimental.
- **Derived view (generated):** `_LIVE-STATE.md` — what's alive · what's dead · open propagation gaps · orphaned artifacts. Becomes the cold-start entry point.
- **Gate:** integrity fails if a live doc points at a superseded node / a superseded decision has un-tombstoned downstream = blast-radius + `_build_integrity.py` retargeted from tokens to decisions.
- **Arbitration:** contradictions become detectable (two live nodes asserting conflicting things = flagged edge); supersession gives resolution order. Makes the reconciliation-register (proto-arbitration) systematic — "stale"/"contradiction" become graph queries.

**MVP (don't gold-plate — advisory→bite-test like everything else):** NOT a graph DB. (1) extend ADR front-matter with `supersedes:`/`propagates-to:` fields (edges as data); (2) `_build_live_state.py` walks ADRs + tombstone banners → emits `_LIVE-STATE.md`; (3) staleness check into `_build_all.py`, advisory first. Grow to a real graph only if it earns its keep.

**RULED 2026-07-05 → `ADR-0007` (accepted): adopt the temporal decision-graph pattern lightweight-first.** Desk research (3 converging lines: ADR-as-KG + Cosmos-SDK supersession discipline / OIDA; temporal bitemporal agent-memory = **Zep/Graphiti** `t_valid→t_invalid`, invalidate-not-discard, open-source = the graduation path; data-lineage OpenLineage/dbt = blast-radius analogue). Load-bearing lesson: **the graph is a view over well-recorded edges; the discipline of writing the edge at ruling-time prevents rot, not the storage** — full graph DB = gold-plating. MVP = (1) edges as ADR front-matter (`supersedes/superseded-by/propagates-to` + validity dates), (2) `_build_live_state.py` → `_LIVE-STATE.md`, (3) advisory staleness gate in `_build_all.py`, (4) Graphiti later if volume justifies.

**⚠️ ANTI-LAUNDERING GUARD (Dave's catch 2026-07-05 → ADR-0007 §5):** the KG records PROVENANCE not CORRECTNESS — a clean node *looks* vetted (the graph launders bad decisions). Fix = validation state SEPARATE from lifecycle, reuse `_CONFIDENCE.md` (asserted/inferred/review) + `_REVIEW-QUEUE`: lifecycle=live/superseded, validation=**unaudited→vouched**. Whole backlog seeds `unaudited` (honest default); promote to vouched = HUMAN correctness-audit ONLY, never derived (engine records, Dave vouches; = §9a gestalt applied to decisions); staleness gate enforces CONSISTENCY, never implies VALIDITY. **OPEN:** decision-corpus correctness audit — batched FRESH-context passes (loaded session = worst place to rubber-stamp a corpus), method TBD. `_LIVE-STATE` now carries an "everything is RECORDED not VALIDATED" banner.

**SHIPPED 2026-07-05 (state-retention spine):** `_LIVE-STATE.md` seeded (interim, hand-maintained until generated) = the live/dead/open ledger; wired into AGENTS cold-start sequence **GOOD-MORNING → _LIVE-STATE → knowledge/README**; refresh at end of every session. Supersession rule in AGENTS; registers.html tombstoned.

**✅ STALENESS GATE SHIPPED 2026-07-10 (Dave: "lets get this foundation piece sorted, we've spun our wheels before because of this").** `knowledge/_build_live_state.py` — the CHECKER slice of the ADR-0007 spec (generator half still deferred). Parses the ledger's existing prose markers (LIVE bullets, `→ superseded-by` DEAD lines, ADR `**Status:**`/audit banners, tombstones — the clean front-matter edge convention was NOT there, so the gate reads prose for now). 5 checks: **freshness drift** (stamp vs newest decision-doc git date — the exact bug that triggered this: the stamp had silently drifted 5 days), **dead-node resurrection** (DEAD node cited in LIVE / dead artifact referenced un-tombstoned), **tombstone consistency** (DEAD file exists + carries a banner), **ADR lifecycle contradiction** (deferred/superseded ADR cited as LIVE — catches ADR-0003), **orphan supersession edge**. Writes `_LIVE-STATE-CHECK.md`. **Advisory** by default (`--strict` gates; wired non-gating into `_build_all.py` step 7) per §5 anti-laundering (enforces consistency, NEVER validity). Negative-tested: catches all 5 injected drifts; clean on the live ledger (0 warnings). **Still deferred:** the generator half (regenerate LIVE/DEAD from edges) — needs the front-matter edge convention on ADRs first (the natural next slice). Trigger to build it: when hand-maintaining the DEAD/LIVE blocks itself starts drifting.

**EXTENSION RAISED 2026-07-05 (Dave, after Tier A audit batch 1) — two natural next rings:**
(1) **State ⇒ forward planning in the same graph.** The tool shouldn't only track past decisions
(live/dead/right) — it should track *goals and their state* too. Latent already: `_LIVE-STATE`'s
**OPEN** section is proto-planning. Goals = nodes at a different *tense*; same edges
(`blocks`/`depends-on`/`superseded-by`); the staleness gate that flags a live doc citing a dead
decision is the same machine that flags a goal blocked on something abandoned. "Decisions and
goals are the same object at different tenses." (2) **Package as a transferable plugin.** Extract
the runbooks + `_build_live_state.py` + staleness gate + audit ledger into portable machinery any
project mounts — this stops being UX-design scaffolding and becomes a reusable tool. Roots exist:
[[graphify-tool]], ADR-0007 §4 Graphiti graduation path.
**⚠️ Guardrail (don't repeat the audit's own finding — ratifying ahead of proof):** the pattern is
still HAND-RUN here (generator + gate unbuilt). Sequence = **prove it self-generating on THIS
project first, then extract the plugin.** Packaging an unproven pattern is the trap. Status: PARKED
as next-ring evolution / scope in a dedicated session (Dave's call pending).

**🎯 NORTH-STAR TARGET WRITTEN 2026-07-10 → `_STATE-MACHINE-TARGET.md` (root, in cold-start sequence).**
Dave confirmed the goal is a **context machine, not a checklist** ("I'll need this to combat drift and
lost decisions"): three tenses (past decisions · present state · future goals — "decisions and goals
are the same object at different tenses") × 6 first-class entity types (decision · goal/target ·
open-thread · insight/finding · sub-quest/side-project · tool/artifact), each with lifecycle +
validation⊥lifecycle + edges. **Headline capability = compile-a-narrative on demand:** drift report
(BUILT) · session/period digest · goal tree · spin-off register · tool catalog · decision trail —
each a view over the same graph. Build path (doc §9): ✅ spine + ✅ drift gate → ⬜ front-matter
edge/entity convention (next slice, prerequisite) → ⬜ generator → ⬜ compile views → ⬜ extract plugin.
The prose sections of `_LIVE-STATE` (LIVE/DEAD/OPEN/PLANNED/SPIN-OFF) already ARE the entity types,
just untyped — formalising them is the work.

**How to apply:** this IS [[graphify-tool]] pointed at the PM layer, not just code-ingestion; matches [[procedural-debt-and-method]] (write the method down; verification=enforcement) and the [[pipeline-mental-model]] derived-view+gate discipline applied recursively. Deserves its own focused session to spec. Related: [[review-session-progress]], [[process-doc-language-review]] (the "stale" finding = the periodic catch), [[decision-audit-method]] (batch 1 run 2026-07-05).
