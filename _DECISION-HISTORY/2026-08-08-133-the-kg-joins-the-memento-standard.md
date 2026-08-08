# #133 — the design KG joins the Memento standard (s131-D2 enacted mechanical-half, s133-D1 widens the scope)

provenance: local_47c7b4cf · 2026-08-08
status: ruled — knowledge/_rulings.json § s133-D1 · notes/_MEMENTO-DECISIONS.md § s133-D1

**Spine entry:** `_LIVE-STATE.md` ⏱ LATEST DELTA #133 · **Rulings:** `s131-D2` (scope parent) · `s133-D1` (this session, Dave's)

## Finding 1 — the investigation Dave asked for changed the enactment

Dave's opener: verify the scoped edges before enacting, and — the KG being a knowledge BASE — ask
whether other edge types belong. The baseline reproduced exactly: the "559 edges / 4 untyped fields"
of s131-D2 = `relationships.{livesInside 274, mustNotNeighbour 40, commonPatterns 223, triggeredBy 22}`.
But the four fields are NOT one kind of edge: livesInside mixes component refs with contexts;
mustNotNeighbour and triggeredBy are prose constraints; commonPatterns are use-case names. And the
corpus carries edge families the ruling never scoped: token claims (495 — the field where
banner.meta.json went stale, the ruling's own origin), component edges in 5 `$`-fields (~40),
implicit renderedBy→snippet (75/76), governedBy→rulings (1 citation in 76 metas). The brief:
`notes/_briefs/2026-08-08-133-s131-D2-edge-investigation-brief.md`.

## Finding 2 — Dave ruled the widening (s133-D1)

On readback ("I think so, i want rigour"): pattern + context become REAL node types, not $note
demotions; all four edge families ratified into scope. ~559/4 → ~1,100/10 + 2 node types. The
mechanical/Dave's-eye split honours s131-D2's own watch line: prose→reference conversions await his eye.

## Finding 3 — what was built (all by addition, two Sonnet subs, replayed in-window)

Schema v2 (`edges` field + edge definition in meta.schema.json) · registries `_nodes-pattern.json`
(214) / `_nodes-context.json` (139) · `gen_kg_edges.py` (idempotent, round-trip-verified per file) —
653 resolved typed edges + 98 declared `ref:null`+`$note` prose edges across 76 metas + the proforma.
Parse-gate `_validate_kg.py`: refs parse+resolve in the consumer's grammar, null-needs-note,
provenance refusal, schema check, freshness half (regen+diff). Index: `_build_memento_index.py`
extended, 642 → 1073 records (component-meta 77 · pattern-node 214 · context-node 139) — the corpus
is retrieval-reachable for the first time. The five-media class ("true when written, nothing
re-checks it") has its fifth medium gated.

## Finding 4 — the mutation test was run on the LIVE gate, and both halves caught it

A live ref broken in accordion.meta.json → rc=1 naming file+edge+reason, AND the freshness half
independently flagged the drift; restore byte-identical, rc=0. A first confound was caught and
attributed: /tmp on the shared volume is unwritable, so a first run's rc=1 was the REDIRECT failing,
not the gate — re-run via /var/tmp (the #129 pothole class, same fix).

## Finding 5 — what awaits Dave (the review doc is the product)

`reviews/KG-EDGES-REVIEW-2026-08-08-s133-v1.html` (+ .md twin): 35 near-miss nodes (context:card vs
cards, context:form vs form-layout, context:tab-panel vs tabs — string-identity resolver rightly
refused to fuzzy-match), 98 prose edges grouped, 47 unvetted governedBy candidates, token-claim
grammar proposal. Nothing converted without his eye; nothing deleted anywhere (archive-never-delete
held: old fields all intact, edges added beside them).

## Still open

Dave's-eye batch off the review doc (near-miss merges · prose→reference · governedBy vetting · token
value/$note split grammar) → then gen_kg_edges regenerates and the ref:null count falls · the carried
#130 set · error-mark image confirm · mark-vs-fill 3.0 gate (Dave's) · SC info-tint re-hue (unruled).
