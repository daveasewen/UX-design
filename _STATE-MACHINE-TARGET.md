# _STATE-MACHINE-TARGET — the context machine (north-star)

*The target definition for the project state mechanism. Extends **ADR-0007** (the accepted
decision) with the full goal, so it stops living only in our heads. Read alongside `_LIVE-STATE.md`
(the current ledger) and `ADR-0007`. Memory: `pm-knowledge-graph-direction`.*

*Written 2026-07-10 (Dave: "a context machine, not a checklist… I'll need this to combat drift and
lost decisions"). Status: **agreed target, partially built** — see §7 for what exists vs what's next.*

---

## 1 · One line

**A context machine for the project — not a checklist of ticked tasks.** It records the whole
journey across three tenses and every kind of thing we produce, and can **compile, on demand, a
narrative of what happened**: drifts, completions, sub-quests, side-projects, new tools, and the
decisions and insights behind them. Its job is to **combat drift and lost decisions** — nothing
we decide, learn, or spin up should silently rot or disappear.

## 2 · The three tenses (one mechanism spans all three)

- **Past** — decisions made, what superseded what, drifts caught and corrected, things tried and
  dropped. History is *invalidated, not deleted* (Graphiti's `t_valid → t_invalid`).
- **Present** — current truth: what's LIVE, what's DEAD (do-not-build-on).
- **Future** — goals, targets, open threads, and the ideas/insights discovered along the way.

The load-bearing idea (Dave, 2026-07-05): **"decisions and goals are the same object at different
tenses."** A goal is a node that hasn't happened yet; a decision is one that has. Same edges
(`blocks` / `depends-on` / `superseded-by`), same machine. The staleness gate that flags a live doc
citing a dead decision is the same gate that flags a goal blocked on something abandoned.

## 3 · Entity taxonomy (every kind is first-class)

Each node carries: `id` · `type` · `title` · `status` (lifecycle, §4) · `validation`
(unaudited → vouched, §5) · dates (`created`, and per-type `ruled`/`shipped`/`invalidated`) ·
`edges` (§6) · `source` (who/where). Types:

| Type | What it is | Lives today in |
|---|---|---|
| **decision** | a ruling / ADR / charter clause | ADRs, `_FIXED-FLEX-CHARTER.md`, LIVE bullets |
| **goal / target** | where we intend to be (what · why · blockers) | `_LIVE-STATE` PLANNED / TARGET |
| **open-thread** | a live question / propagation gap not yet resolved | `_LIVE-STATE` OPEN |
| **insight / finding** | something learned along the way (evidence, not a ruling) | `_FINDINGS-*.md`, memory |
| **sub-quest / side-project** | an emergent project surfaced mid-work | memory `spin-off-candidates`, `_LIVE-STATE` SPIN-OFF |
| **tool / artifact** | a thing built (script, doc, mock, dossier) | `knowledge/_*.py`, mocks, this doc |

The substrate already exists as prose sections in `_LIVE-STATE.md` (LIVE · DEAD · OPEN · PLANNED ·
SPIN-OFF). The target formalises those prose sections into **typed nodes with lifecycle + edges**,
so they can be queried and compiled rather than only read.

## 4 · Lifecycle states (per type — the "status" field)

- **decision:** proposed → accepted → *superseded* / *amended* (never deleted).
- **goal/target:** open → in-progress → done · or → abandoned (with reason). *Flag a target whose
  blockers cleared but status still reads "blocked" — the Sutherland failure.*
- **open-thread:** open → resolved (→ becomes a decision) · or → parked.
- **insight/finding:** captured → acted-on (→ links to the decision it drove) · or → superseded by
  a later finding.
- **sub-quest/side-project:** raised → active → parked · shipped · or dropped.
- **tool/artifact:** built → in-use → deprecated / tombstoned.

Lifecycle is **mechanical** (recorded at ruling-time). It says nothing about correctness — see §5.

## 5 · Validation ⊥ lifecycle (the anti-laundering guard, ADR-0007 §5)

The machine records **provenance, not correctness.** A clean node with a tidy edge *looks vetted* —
the graph launders bad decisions. So every node carries a **validation state separate from its
lifecycle**: `unaudited → vouched` (or `amend` / `overturn` / `defer`). Rules that never bend:

- Everything seeds in as **`unaudited`** (honest by default).
- Promotion to **`vouched` is a human correctness-audit only, never derived** (engine records,
  Dave vouches — the §9a gestalt principle applied to decisions).
- The staleness gate enforces **consistency, never validity.** A green check ≠ a right decision.

## 6 · Edges (the relationships that make it a graph, not a list)

`supersedes` / `superseded-by` · `amends` · `propagates-to` · `depends-on` / `blocks` ·
`derived-from` · `evidences` (insight → decision) · `realises` (tool → goal) · `spun-off-from`
(sub-quest → parent) · `tests`. Each edge is written **at ruling-time** — that discipline, not the
storage engine, is what prevents rot (the load-bearing lesson from all three research lines, §8).

## 7 · The headline capability — compile a narrative on demand

The thing that makes it a *context machine*: from the typed nodes + edges + dates, **generate a
document over any window** (a session, a week, "since we last shipped"). Views to support:

1. **Drift report** — freshness, dead-node resurrection, orphan edges, blocked-but-cleared targets.
   *(BUILT — `_build_live_state.py`, the staleness gate.)*
2. **Period / session digest** — what changed: decisions ruled, goals moved, drifts fixed,
   insights captured, tools built. The "what happened while I was away" document.
3. **Goal tree** — targets with their blockers and dependency edges; what's unblocked now.
4. **Spin-off / side-project register** — every sub-quest raised, its status, its parent.
5. **Tool catalog** — everything built along the way (this session: the trace dossier +
   `_build_live_state.py`), with what goal each realises.
6. **Decision trail** — for any node: what it superseded, what superseded it, the insights that
   evidenced it, its validation state.

Any of these is a query over the same graph — "compile" = render a view, not maintain a separate doc.

## 8 · Provenance — the research this rests on (done 2026-07-05)

Three independent communities converged on the same pattern (full record: `ADR-0007` Context +
memory `pm-knowledge-graph-direction`):

- **ADR-as-knowledge-graph** — NILUS; Cosmos SDK `Status: Superseded by` header + back-ref
  discipline; OIDA typed/signed/time-indexed decision graph. Failure mode named:
  *"superseded decisions remain active forever because nobody tracks lifecycle."*
- **Temporal / bitemporal agent-memory graphs** — **Zep / Graphiti** (OSS): edges carry a validity
  window (`t_valid → t_invalid`); on conflict a fact is *invalidated, not discarded*. Built for the
  "cold start resurrected a dead node" symptom. **The named graduation path** if volume justifies a
  real temporal-KG engine.
- **Data lineage** — OpenLineage / dbt: downstream-impact + auto-notify (generalises our token
  blast-radius).

Load-bearing lesson: **the graph is a queryable view over well-recorded edges; writing the edge at
ruling-time prevents rot — not the storage engine.** Hence lightweight-first (markdown + front-matter),
Graphiti later, Neo4j never (for a solo-run project).

## 9 · Build path — where we are vs the target

- ✅ **State-retention spine** — `_LIVE-STATE.md` seeded, wired into the cold-start sequence
  (GOOD-MORNING → _LIVE-STATE → README), refreshed each session.
- ✅ **Drift gate** — `_build_live_state.py` (the checker slice): 5 consistency checks, advisory in
  `_build_all.py`, negative-tested. *Combats drift — the immediate pain.*
- ⬜ **Front-matter edge/entity convention** — the prerequisite for everything below. Give
  decisions/goals/insights/sub-quests/tools a `type` + `status` + `edges` header (ADRs first, then
  memory + artifacts). *Next slice.*
- ⬜ **Generator** — walk the typed nodes to *generate* the LIVE/DEAD/OPEN/goal-tree blocks of
  `_LIVE-STATE.md`, so the ledger stops being hand-maintained (removes the drift-at-source).
- ⬜ **Compile views** (§7 items 2–6) — the narrative-document capability. The point of the machine.
- ⬜ **Extract as a portable plugin** — only *after* it's proven self-generating here
  (`pm-knowledge-graph-direction`: packaging an unproven pattern is the trap).

## 10 · Guardrails (don't repeat past mistakes)

- **Lightweight-first.** Markdown + front-matter until volume proves it insufficient. No graph DB now.
- **Edge-at-ruling-time.** The discipline is the product; the storage is incidental.
- **Validation is never derived.** Consistency ≠ correctness; only a human vouches.
- **Prove-then-package.** Self-generating on THIS project before extracting a plugin.
- **Don't over-build ahead of use.** Each slice earns the next by being used, per ADR-0005 §5
  (advisory → earns blocking by bite-test).

---

*Compile target: when the generator + compile views land, "show me drifts, completions, sub-quests,
side-projects and new tools since <date>" becomes one command over this graph. That is done.*
