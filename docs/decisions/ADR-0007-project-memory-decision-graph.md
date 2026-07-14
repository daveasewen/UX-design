# ADR-0007 — Project memory as a temporal decision-graph (lightweight-first); `_LIVE-STATE` is the cold-start spine

**Date:** 2026-07-05 · **Status:** accepted (Dave) · **Relates:** ADR-0005, ADR-0006 · **Method:** AGENTS.md "supersession discipline"

## Context

**Intent, in one line: this is *state management for project knowledge.*** Current state, recorded
transitions, one source of truth with derived views, no stale reads — the same discipline you'd
apply to application state, pointed at the project's own decisions instead of a UI. Everything
below (supersession edges, `_LIVE-STATE`, the staleness gate, the unaudited→vouched states) is that
one idea made concrete.

A cold-start session (2026-07-05) wasted most of a sitting reasoning from a **retired
artifact** (`sme-payments-registers.html`, the old looks-based register dial) as if it were
live, because nothing marked it dead and nothing recorded that the §9 looks→inference ruling
had superseded it. Root cause, named: **context staleness is an unrecorded supersession edge.**
The `knowledge/` design layer already solved this class for *design* knowledge (authored nodes
+ edges + generated views + integrity gate); the **project/process layer had no equivalent** —
it lived in prose docs + atomised memory, which is exactly why it rots.

Desk research (2026-07-05) found three independent communities have built the fix, converging
on the same pattern:

- **ADR-as-knowledge-graph** (NILUS; Cosmos SDK's `Status: Superseded by` header + back-ref
  discipline; the OIDA typed/signed/time-indexed decision graph). Named failure mode:
  *"superseded decisions remain active forever because nobody tracks lifecycle."*
- **Temporal / bitemporal agent-memory graphs** (Zep / Graphiti, open source): every edge
  carries a validity window (`t_valid → t_invalid`); on conflict a fact is **invalidated, not
  discarded** — history preserved, current view clean. Purpose-built for the "cold start
  resurrected a dead node" symptom ("memory contamination").
- **Data lineage** (OpenLineage / dbt): downstream-impact + auto-notify when an upstream node
  changes — the generalisation of our token `_blast-radius`.

The load-bearing lesson from all three: **the graph is just a queryable view over well-recorded
edges. The discipline of writing the edge at ruling-time is what actually prevents rot — not the
storage engine.** A full graph DB (Neo4j) would be gold-plating for a solo-run project; the top
80% is text-achievable (Cosmos SDK = markdown headers; "Decision Graph" = a text-based KG).

> **North-star target elaborated 2026-07-10 → `_STATE-MACHINE-TARGET.md`.** This ADR is the
> accepted decision; that doc is the full goal Dave holds — a *context machine* spanning three
> tenses (past decisions · present state · future goals) and every entity kind (decisions · goals ·
> insights · sub-quests/side-projects · tools), whose headline capability is to **compile a
> narrative on demand** (drifts · completions · sub-quests · side-projects · new tools). "Combat
> drift and lost decisions." Build status tracked there (§9); the staleness gate below is slice 1.

## Decision

Adopt the **temporal decision-graph pattern, implemented lightweight-first** — the same
nodes/edges/derived-view/gate shape already proven on the design layer, retargeted to decisions
and artifacts. Four parts:

1. **Edges as front-matter data.** Rulings/ADRs and killable artifacts carry explicit edges:
   `supersedes:` / `superseded-by:` / `propagates-to:` plus a validity date (`ruled:` and, when
   killed, `superseded-on:`). This is Graphiti's `t_valid`/`t_invalid` idea expressed in
   markdown. Tombstone banners (AGENTS supersession discipline) are the artifact-level form.

2. **`_LIVE-STATE.md` — the generated derived view AND the cold-start spine.** A single ledger of
   what is **LIVE** (current truth), **SUPERSEDED/DEAD** (do-not-build-on, with the edge to what
   replaced it), and **OPEN** (propagation gaps + parked threads). Hand-seeded now; generated
   later by `_build_live_state.py` walking the front-matter edges + tombstones. **This is the
   state-retention mechanism** — the thing a successive session reads to pick up current truth
   without archaeology.

3. **Staleness gate** in `knowledge/_build_all.py` — advisory first, earns blocking by bite-test
   (per ADR-0005 §5): fail/flag if a LIVE doc references a SUPERSEDED node, or a superseded ruling
   has un-tombstoned downstream. The review-dossier "stale" pass is the periodic human catch.

4. **Graphiti as the graduation path** — if/when agent-memory volume justifies a real temporal
   KG engine, adopt Graphiti rather than inventing one. Not now.

5. **Validity is not provenance — the anti-laundering guard (added 2026-07-05, Dave's catch).**
   The graph records *that* a decision was made, by whom, when, superseding what. It does **not**
   establish the decision was *correct*. A wrong decision, once a clean node with a tidy edge,
   *looks vetted* — the graph launders it. So every node carries a **validation state distinct
   from its lifecycle state**, reusing `_CONFIDENCE.md` (`asserted / inferred / review`) + the
   review-queue: lifecycle = live/superseded; validation = **unaudited → vouched**. Rules: the
   whole existing backlog **seeds in as `unaudited`** (honest by default); promotion to `vouched`
   is a **human correctness-audit only, never derived** (engine records, Dave vouches — validity
   is the §9a gestalt principle applied to decisions); the staleness gate enforces *consistency*
   and must **never imply validity**. The correctness audit runs as **batched, fresh-context
   passes** (a loaded session is the worst place to rubber-stamp a decision corpus) — method TBD,
   an open thread, reusing the `_REVIEW-QUEUE` tiering.

**State-retention wiring (the hard requirement):** `_LIVE-STATE.md` joins the cold-start entry
sequence in `AGENTS.md` — **GOOD-MORNING (latest handoff) → `_LIVE-STATE` (live/dead/open ledger)
→ `knowledge/README` (the build)** — and is refreshed at end-of-session alongside the handoff.
It complements, not duplicates: GOOD-MORNING = session narrative; `MEMORY.md` = atomised memory
index; `_LIVE-STATE` = the supersession ledger / graph view.

## Consequences

- The next focused session builds `_build_live_state.py` + the staleness gate from this spec
  rather than a blank page. Until then, `_LIVE-STATE.md` is hand-maintained and **must be marked
  as interim** (a hand-maintained derived-view is itself a rot risk — the honesty tag mitigates).
  - **✅ STALENESS GATE BUILT 2026-07-10 (lightweight-first slice).** `knowledge/_build_live_state.py`
    validates the ledger against reality — 5 checks (freshness drift · dead-node resurrection ·
    tombstone consistency · ADR lifecycle contradiction · orphan supersession edge) → writes
    `_LIVE-STATE-CHECK.md`. Advisory by default (`--strict` gates); wired non-gating into
    `_build_all.py` (per §5 anti-laundering: it enforces *consistency*, never *validity*). Negative-
    tested (catches all 5 injected drifts) and clean on the live ledger. **Still deferred:** the
    *generator* half (walking front-matter edges to regenerate LIVE/DEAD blocks) — needs the
    front-matter edge convention on ADRs first; the gate parses the existing prose markers for now.
- Every ruling now has a two-step close: record the edge (front-matter/tombstone) **and** update
  `_LIVE-STATE`. This is the AGENTS supersession discipline made systematic.
- Low-regret and reversible: it reuses the existing generator+gate machinery; if it doesn't earn
  its keep it collapses back to plain ADRs with no loss.
- Related direction: `graphify-tool` (KG engine, previously scoped at code-ingestion) is the same
  pattern; this points it at the PM layer. Memory: `pm-knowledge-graph-direction`.
