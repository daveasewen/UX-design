---
name: ds-knowledge-graph-revisit
description: "Reopened 2026-07-05 (ADR-0003 audit DEFER): revisit whether the whole DS corpus should be one interlinked knowledge graph; root cause = ingestion never completed; overlay/index layer (not monolith, not GraphRAG); 2026-07-10 design direction attached"
metadata: 
  node_type: memory
  type: project
  originSessionId: bc7111a5-79d4-40ca-8ab0-04bd883a3e1d
---

**REOPENED 2026-07-05 (decision audit, Tier A batch 2 — Dave).** ADR-0003 (knowledge
representation per stage, not one store) was **deferred, not vouched**. Dave's founding instinct:
the *whole* design-system corpus — component specs, foundations, tokens, snippets, and the
create.hsbc guidelines — is **naturally one interlinked knowledge graph** (entities cross-link
across many subjects). ADR-0003 scoped that down to graphs for components + compliance only, with
tokens→DTCG JSON and guidelines→Markdown. Today the cross-entity interlink is modelled **only
inside the compliance graph**.

**Root cause (Dave):** the idea wasn't wrong in principle — **ingestion was never completed.**
It was attempted, got some way, and was curtailed. So the unified KG was never actually built and
tested; it was scoped-around rather than disproven.

**Decision:** treat this as a **separate, structured work thread with its own audit-grade method**
(like the decision audit) — *stated aim: do it correctly this time.* NOT part of the decision
audit session (keep that impartial + bounded).

**Scope of the spike:** (1) map the entity/edge model across the full corpus (token, component,
snippet, foundation, guideline, WCAG rule; edges: uses, derived-from, references, governed-by);
(2) compare against what the hybrid already captures (component `*.meta.json`, the real compliance
KG, `_blast-radius.json`, `graph-index.json`, `_GRAPH-REPORT.md`); (3) rule keep-hybrid /
go-unified / **overlay-index layer**. **Leading hypothesis:** an overlay/index graph that links
across the existing specialised stores (don't collapse DTCG token JSON etc. into one monolith —
that's the curation-cost trap ADR-0003 rightly feared); `_blast-radius.json` is a proto version.
Connect to [[graphify-tool]] and the ADR-0007 decision-graph infra.

**🟠 DESIGN DIRECTION (Dave, 2026-07-10 — from the deep-review KG question; folded into the plan).**
The compliance "KG" is today an **inverted index, not a graph** (`_build_compliance_kg.py:61-78`:
self-asserted `relatedSC` arrays → two lookup tables; no SC→SC / component→component edges; meta
`relationships` never compiled; `query.py` = one-hop dict joins + substring match). Verdict:
**fine for its current job, wrong for the roadmap** (the layout tier, blast-radius, this thread all
need cross-store traversal). Chosen approach when taken up:
1. **NOT GraphRAG.** GraphRAG *extracts* a graph from unstructured prose for fuzzy sense-making; our
   entities are already structured records with IDs — the need is **connection, not extraction** →
   **overlay-index / small property graph** over existing stores (sources of truth stay; edge-layer
   derived + regenerable; no monolith). Tiny embedded property graph (typed edges in JSON, or
   Kùzu/DuckDB-PGQ) if real path queries wanted — no RAG machinery.
2. **Guideline granularity — not finer text, typed EDGES.** Rules already ~1-bullet granular; split
   only where one *bundles* several constraints so each atom → one target (**ACT atomic-vs-composite**),
   then add the edge rule→token/component/SC/pattern (today prose `[REVIEW]`/`F1` notes).
3. **Import, don't hand-type, the SC↔rule leg** — W3C **ACT Rules Format 1.1** (Rec, Feb 2026) +
   **axe-core** rule metadata publish rule↔SC machine-readably. Hand-curate only the **component↔SC**
   leg (the genuine novelty). = report **R6**.
4. **Type the edges: `applies_to` (claimed) vs `verified_by` (executable rule exists AND passes)** —
   turns the graph from bookkeeping into "which compliance claims are actually enforced."
5. **Keep two retrieval needs separate:** structural compliance graph ≠ the advisory "massive-brain
   reads the 462 rules per run" need — *that* is retrieval-over-prose = the one place a vector/light-
   graph layer fits.
**Sequencing:** NOT standalone infra now — it **rides with the layout/library tier (R4) + Ingestion
Phase 3** (both graph-shaped; natural moment for typed edges; the compliance index becomes one
*projection* of the overlay). **The governance-KG also grows as a BYPRODUCT of the library build-out**
— each promoted component adds its edges (make "add edges" part of the promote checklist). Cheap-now
slice: type existing edges + import ACT. Recorded in `_LIVE-STATE` OPEN + Phase-3 target. Unaudited.

**⭐ DETAILED ASSESSMENT WRITTEN 2026-07-05** → `knowledge/_INGESTION-ASSESSMENT_2026-07-05.md`
(cockroach doc; file-level survey). 3 siloed strands (guidelines 462 rules HEALTHY · component/
compliance CONSISTENT-BUT-NARROW = WCAG↔component only · tokens HALF-MIGRATED); only cross-entity
graph is the compliance KG. Sutherland export landed 2026-06-17 (migration unblocked; manifest was
stale). 147 depricate tokens await retirement; 21 legacy guideline files await upgrade. Phased
worklist (Phase 0 un-stale → 1 Sutherland migration → 2 finish capture → 3 overlay graph → 4 wire
into state machine). Target state recorded in `_LIVE-STATE` PLANNED/TARGET.

**Spot-check 2026-07-07 (Dave asked "is it just canon that's graphed?"):** confirmed — the live graph
(`_build_xref_index.py` joining `components/` metas + `tokens/_blast-radius.json` +
`compliance/graph-index.json`) covers component/token/compliance core only. Guidelines attached via a
**hand-typed `GLOBAL`+`TOPICAL` map inside the script** (pointed-*at*, not graphed-*through*);
snippets, assets, register, `_sources/`, TOV/copy corpus, ADRs are NOT nodes.

**How to apply:** own focused session; complete-the-ingestion is the enabling precondition; but the
2026-07-10 direction says build the graph incrementally *with* the library/layout work, not as a big
separate infra project. Read the assessment doc first. Pairs with [[pm-knowledge-graph-direction]]
(decision/memory graph — adjacent but distinct), [[library-composition-tier-gap]],
[[component-library-buildout-plan]], [[deep-analysis-report-2026-07-10]] (R6).
