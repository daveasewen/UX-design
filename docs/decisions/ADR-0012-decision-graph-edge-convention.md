# ADR-0012 — Decision-graph edge convention: typed edges on the record corpus

**Date:** 2026-07-21 · **Status:** **proposed** (drafted by the Fable audit session; Dave accepts/amends on
`reviews/DECISION-GRAPH-CONVENTION-2026-07-21-v1.REVIEW.html`) · **Extends:** ADR-0007 (temporal decision-graph
— this is its unbuilt first half) · **Relates:** `notes/_STATE-MACHINE-TARGET.md` §6 · `_build_live_state.py`
(slice 1) · `knowledge/guidelines/_RECONCILIATION.md` (the generated REVIEW-rule register)

## Context

Rulings cross-reference in **prose** ("subsumes the R-D3 amber exemption", "supersedes col25-011 for Mono"),
so recall = keyword search and reconciliation = manual archaeology. The 2026-07-21 icon-011 ↔ R-D6 ↔ R-D3
reconciliation was done by hand; ADR-0007 had already decided the fix (typed edges + generated views + gate)
but the edge convention was never authored, so the generator half never landed.

**The full-corpus audit (2026-07-21, this session) established ground truth:**

- **Census:** 57 primary decision nodes — R-D1..20 · T-D1..14 · B-D1..6 · DV-D01..06 · ADR-0001..0011 —
  plus 35 REVIEW rules (generated into `_RECONCILIATION.md`), a pre-T-D narrative era in the TYPE ledger
  (~15 unnumbered ruling sections, 2026-07-17/18), and ~39 DataViz batch pins. The "~35 nodes" planning
  estimate undercounted by ~2×.
- **Three edge vocabularies already exist in the wild** and must be reconciled, not overwritten:
  `_DATAVIZ-DECISIONS.md` YAML front-matter (`refines / governs / gated_by`); ADR header keys
  (`Extends: / Relates: / Method:`); `_STATE-MACHINE-TARGET.md` §6's nine types.
- **The corpus contains relation kinds the naive taxonomy misses:** *scoped* supersession (R-D16 supersedes
  `col25-011` **for Mono only**); *claim-level* supersession inside a still-live node (R-D11 kills R-D10's
  "mode-stable fills" claim while R-D10's dark values stay ruled); and **deliberate divergence** (DEF-005
  exempts intrinsic squares, DEF-006 pointedly does not — "a future reader will try to reconcile them.
  Do not."). A conflict gate with no way to record intentional divergence would flag that pair forever.
- **Two live conflicts surfaced** (queued for Dave on the review sheet, per the guardrail — never
  auto-resolved): R-D2's "red/green/blue hold the SAME value in both roles" vs the later per-role splits
  (R-D18/R-D20); R-D7's "red = mode-stable, one value" vs R-D20's per-mode error-glyph `#B92F1E`/`#CC4333`.

## Decision

### 1 · Node identity — IDs are nodes; anchors at need, no retro-renumbering

A node is any unit that already carries a stable ID: `R-D*`, `T-D*`, `B-D*`, `DV-D*`, `ADR-*`, and guideline
rules `{#id}`. Sub-rulings use a dot suffix on the ledger's own naming (`R-D6.A`, `R-D6.A′`, `R-D12.B`).
The pre-T-D era and batch pins are **not** retro-numbered: where an edge genuinely lands on one, it gets a
lightweight anchor (`TYPE:2026-07-18:sat-ceiling`, `DV:B5#1`) minted at edge-authoring time. Edge-at-need,
per the ADR-0007 §10 guardrail (don't over-build ahead of use).

### 2 · Edge taxonomy — seven types + qualifiers; small core, nuance in qualifiers

| edge | meaning | audit exemplar |
|---|---|---|
| `supersedes(X)` | X (or a claim/scope of X) is no longer operative; this node replaces it | R-D14 supersedes R-D13 (light values) |
| `refines(X)` | sharpens, extends, or answers an open carried from X — X stays live | R-D6.A′ refines R-D6.A; ADR-0011 refines R-D15 |
| `subsumes(X)` | absorbs X's content; X remains as record, pointing here | R-D6.A′ subsumes the icon-015 amber roundel-leg exemption |
| `bounds(X)` | limits X's scope without killing it | R-D6.A′ bounds icon-011's "all instances" |
| `conflicts-with(X, resolution=…)` | recorded tension; **`resolution` mandatory**: `ruled` \| `interim` \| `deferred` \| `parked` \| `queued` \| `open` | R-D3 conflicts-with dv-017, resolution=ruled (by R-D5) |
| `diverges-from(X, reason=…)` | **deliberate** divergence — not a conflict, never to be "reconciled" | DEF-006 diverges-from DEF-005 (box dims vs type inside) |
| `verified-by(A)` | evidence artifact or gate backing this node | T-D12 verified-by the 21-file pixel diff + NO_SNAP control |

Qualifiers: `scope=` (a theme/tier/role the edge is confined to — `supersedes(col25-011, scope=mono)`),
`claim=` (the specific assertion superseded while the node stays live — `supersedes(R-D10, claim=fills-mode-stable)`),
`ref=` (where the resolution is recorded). Untyped `relates(X)` is retained for weak links; it carries **no**
gate semantics.

**Alias map (normalise in the generated view; source files are NOT rewritten to conform):**
ADR `Extends:` → `refines` · DV `gated_by:` → `verified-by` · DV `governs:` → `bounds` (rules constrain the
artifact) · `Relates:` → `relates`. Existing records keep their native syntax; the parser normalises. This is
ADR-0008's "diverge-but-keep-machine-mappable" applied to our own record.

### 3 · Syntax and location — one visible line per node, in the node's own home

- **Ledger entries:** one line at the end of the entry, human-visible and grep-stable:
  `Edges: supersedes(R-D8, claim=band-A-values) · refines(R-D9) · verified-by(reviews/RAG-…-v9)`
- **ADRs:** the existing header line gains the same grammar (legacy `Extends:`/`Relates:` keys stay valid
  via the alias map).
- **DataViz front-matter:** stays as-is (the existing prototype is conformant via aliases).
- **REVIEW rules:** not re-authored. They live in their guideline files with `{#id}`; edges land on the
  ledger/ADR side pointing at them, and `_RECONCILIATION.md` remains their generated register (its
  resolution language parses into `conflicts-with` resolutions).

One source of truth per edge — written **at ruling-time, in the ruling's home** (the discipline is the
product; ADR-0007 §8). Denormalisation happens only in generated views.

### 4 · Status ⊥ validation per node (ADR-0007 §5, unchanged)

Lifecycle `status`: `proposed | accepted | amended | superseded` (mechanical, recorded at ruling time).
`validation`: `unaudited | vouched | defer` — **human-only, never derived** (anti-laundering). Existing
states carry over: ADR-0003 `defer`, ADR-0006 `vouched` (Tier A), everything else seeds `unaudited`.

### 5 · Generator — `knowledge/_build_decision_graph.py`

Parses the seed (`notes/_decision-graph-seed-2026-07-21.json`, this session's audited edges) and, once
inscription lands, the inline `Edges:` lines + front-matter. Emits `knowledge/_DECISION-GRAPH.md` + `.json`:

1. **LIVE / AMENDED / DEAD / OPEN ledger** — DEAD = a whole-node `supersedes` points at it; claim-scoped
   supersession marks AMENDED with the dead claim named (this is the Graphiti invalidated-not-deleted idea).
2. **Reconciliation view** — every `conflicts-with` with `resolution=open|queued` surfaces at the top;
   `diverges-from` entries listed as *intentional* (never flagged).
3. **"What touches this" map** — per-node inbound/outbound adjacency (the icon-011 question, answered
   by generation).
4. **Validation rollup** — vouched / defer / unaudited counts, per ADR-0007 §5's honest-by-default rule.

The same parse is architected to later drive `_LIVE-STATE` generation (ADR-0007's part 2, still deferred).

### 6 · Conflict gate — advisory first, day-one-honest

`_build_decision_graph.py --strict` exits non-zero on any `conflicts-with` lacking a resolution, any
`resolution=open`, or a `supersedes` target that can't be resolved to a known node. Wired into
`_build_all.py` **advisory** on acceptance of this ADR; earns blocking by bite-test (ADR-0005 §5).
Known conflicts enter with their real resolution states (`queued` for the two live ones until Dave rules),
so the build is green-and-honest on day one and bites on the **next** unresolved edge.

### 7 · Who authors what (the routing sub-call, resolved by the audit)

The audit showed edge-authoring is **not** mechanical (scoped/claim-level supersession, deliberate
divergence). The judgment half — reading the corpus and deciding the edges — was therefore done **in this
Fable session** and captured in the seed file. What remains delegable: the mechanical **inscription** of
seed edges into ledger entries/ADR headers (Sonnet, verified by the generator diffing inscribed edges
against the seed), DataViz batch-pin anchors, and future edge-at-ruling-time upkeep (the capture ritual
gains a step). Conflicts remain **queued for Dave, never auto-resolved**.

## Consequences

- The icon-011 ↔ R-D6 ↔ R-D3 class of reconciliation becomes a generated view; the two conflicts this
  audit surfaced would have been flagged automatically.
- Cost at ruling-time: one `Edges:` line per node. Cost of adoption: seed inscription (~45 edges, mechanical).
- Reversible: if the convention doesn't earn its keep, the `Edges:` lines remain readable prose and the
  generator is deletable with no loss (the same low-regret shape as ADR-0007's slice 1).
- `_RECONCILIATION.md` and `_LIVE-STATE-CHECK.md` are unchanged today; the graph view complements them and
  may later generate the `_LIVE-STATE` LIVE/DEAD blocks (part 2).
