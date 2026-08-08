# s131-D2 edge investigation — what to enact, measured on the corpus (#133, pre-enactment)

**Status:** INVESTIGATION, nothing enacted. Dave asked (#133): verify the scoped edges, and — since
the KG is a *knowledge base* — check whether other edge types belong. Every figure below measured
this session on the live corpus (76 metas in `knowledge/components/`, +1 at
`knowledge/_proforma/icon-button.meta.json`, per ASSERT-009).

## A — the scoped baseline REPRODUCES

The ruling's "559 edges across 4 untyped prose fields" = exactly
`relationships.{livesInside, mustNotNeighbour, commonPatterns, triggeredBy}`:
274 + 40 + 223 + 22 = **559** ✓. Unresolvable-as-node-refs reproduced within resolver tolerance
(ruling 514; a naive name/stem resolver here finds 531 for these 4 fields — the delta is resolver
strictness, not corpus drift).

## B — the four scoped fields are NOT one kind of edge

Migration cannot be one mechanical rule; each field wants its own treatment:

| field | n | what the targets actually are | proposed typing |
|---|---|---|---|
| `livesInside` | 274 | MIX: real components (Card, Form, Page…) ~28 resolve; the rest are **contexts** ("Dashboards", "Reports") | split: `containedBy` (component ref) vs `usedInContext` (context node or `$note`) |
| `mustNotNeighbour` | 40 | 40/40 prose constraints ("A second chart re-using data/series/1…") — anti-pattern statements, not nodes | typed constraint edge where a target is nameable; else demote to `antiPatterns`/`$note` |
| `commonPatterns` | 223 | 223/223 pattern/use-case names ("FAQ list", "salary bands by grade") | new node type `pattern`, or `$note` — **Dave's call, this is the volume decision** |
| `triggeredBy` | 22 | journey/event prose ("form submission") | `event`/`journey` node type or `$note` |

The ruling's own watch line stands: **edge migration needs Dave's eye where prose becomes a
reference** — B is exactly where.

## C — edge types PRESENT in the corpus but NOT scoped (the KB additions Dave asked about)

1. **`tokens` → token store: 495 edges, the highest-value parse-gate target.** Every meta claims
   token bindings; values are prose-contaminated (measurements, ruling ids, rationale embedded in
   the value string). This is the field where `banner.meta.json` went stale against s131-D1 — the
   defect that caused this ruling. A parse-gate here checks claims against `knowledge/tokens/*.json`
   (the verified spine, per the derivation-governance split). Recommend: **in scope, first-class.**
2. **Component-to-component edges already live in 5 other fields:** `$consumes` (18), `$reuses` (2),
   `subComponents` (5 metas), `$partials` (5), `$family` (12). Genuine, mostly resolvable, unscoped.
   Cheap to type. Recommend: **in scope.**
3. **`renderedBy` → snippet: implicit today, 75/76 metas have a matching
   `knowledge/snippets/` file.** Unrecorded as an edge; `gen_canon_components` already consumes
   snippets, so the edge is checkable for free. The 1 gap is itself a finding.
4. **`governedBy` → rulings: only 1 meta cites any `sNNN-DN` id**, while `_rulings.json` governs
   the corpus wholesale. The Memento standard's provenance-on-claims requirement points here:
   per-component ruling edges, by addition.
5. **Cross-system edges:** `provenance.figma_node` (76, existence-checkable via Figma MCP),
   `codeBindings` (4). Typed but never verified — candidates for the index's freshness gate, not
   necessarily the parse-gate v1.
6. **`tokenValidation` is a dated conclusion** ("PASS — 2026-06-17") — [[conclusions-are-debt]]
   class: true when written, nothing re-checks. Under a parse-gate it becomes GENERATED or gets an
   expiry. Recommend: **generate, retire the hand-written field by addition.**
7. **`accessibility` carries floated `REVIEW:` claims in prose** — open items living inside a spec
   with no register. Not an edge; flag for the index so retrieval surfaces them.

## D — proposed enactment shape (unchanged from the ruling, refined by A–C)

Index (join `_memento-index.json`, freshness-gated) → schema v2 by addition (typed edges + `$note`
demotion; old fields stay, per archive-never-delete) → parse-gate (edges resolve + token claims
parse against the store; new-meta refusal without provenance) → checklist line. Migration order:
mechanical first (C2, C3, B-resolvable), Dave's-eye batch second (B prose→reference, C4).

## E — open to Dave before enactment

1. `commonPatterns`: mint a `pattern` node type (223 nodes) or demote to `$note`?
2. Context targets of `livesInside`: `context` node type or `$note`?
3. Ratify C1 (token claims) + C2 (component edges) + C3 (renderedBy) as in-scope additions?
4. C4 `governedBy` per-component ruling edges — v1 or later?
