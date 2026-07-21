# 2026-07-21 — The decision-graph edge convention: audit first, taxonomy second (Fable, cold)

*Narrative dossier (capture ritual step 1b). WHAT lives in `docs/decisions/ADR-0012` (proposed),
`notes/_decision-graph-seed-2026-07-21.json` (the 88 audited edges) and `_LIVE-STATE.md` LATEST DELTA;
this is the WHY/HOW. Both-way links: ADR-0012 · ADR-0007 · the previous day's dossier
(`2026-07-21-rag-completion-and-decision-graph.md` thread 3, which tasked this session) ·
`reviews/DECISION-GRAPH-CONVENTION-2026-07-21-v1.html` (the rulings sheet, awaiting Dave).*

---

## The shape of the session

Opened cold on Fable, per the routing pin (big / high-stakes / hands-off; wrong taxonomy = corpus-wide
rot). The brief said: audit ~35 nodes → author the edge convention → build generator + conflict gate,
with two guardrails (conflicts queued for Dave, never auto-resolved; the who-authors-the-edges sub-call
decided *after* the audit). The session ran in exactly that order, and the order did the work: **every
design decision in ADR-0012 traces to something the audit found, not to taxonomy theory.**

## Finding 1 — the census was ~2× the estimate, and granularity is not uniform

Counted, not assumed: 20 R-D + 14 T-D + 6 B-D + 6 DV-D + 11 ADRs = **57 primary nodes**, plus 35
REVIEW rules, plus two fuzzy zones — the TYPE ledger's **pre-T-D era** (~15 unnumbered ruling sections
from 2026-07-17/18: the D1–D6 round, the retrofit rules, the reverse-text/chroma arc) and ~39 DataViz
batch pins. Two ledgers use clean per-ruling IDs; one is batch-and-pin; one is narrative-then-numbered.
**Consequence:** the convention had to answer "what is a node?" before "what are the edges?" — answered
as *IDs are nodes; anchors minted at need; no retro-renumbering* (don't over-build ahead of use,
ADR-0007 §10). Small drift caught en route: the GOOD-MORNING standing list said "T-D1…T-D16"; the
ledger holds T-D1..14 (errata E1).

## Finding 2 — three edge vocabularies already existed; the job was reconciliation, not invention

Survey-before-build earned its keep twice:

- `_DATAVIZ-DECISIONS.md` **already carries YAML front-matter** with `relations: refines / governs /
  gated_by` — a working prototype of exactly this convention, authored 2026-07-16 and never generalised.
- ADR headers already carry `**Extends:** / **Relates:**` — proto-edges in a parseable position.
- `notes/_STATE-MACHINE-TARGET.md` §6 had specced nine edge types that nothing implements.

The resolution: a small core taxonomy + an **alias map normalised in the generated view** — source
files keep their native syntax. That is ADR-0008's "diverge-but-keep-machine-mappable" applied to our
own record, and it means the DataViz prototype becomes conformant retroactively without an edit.

## Finding 3 — the corpus contains relation kinds a naive taxonomy cannot express

The reason this was a Fable job. Three kinds, all real, all from the read:

1. **Scoped supersession.** R-D16 supersedes `col25-011` *for Apollo Mono only* — Grey-8 stays
   Legacy-law. A bare `supersedes` would kill a live Legacy rule. → the `scope=` qualifier.
2. **Claim-level supersession inside a live node.** R-D11 kills R-D10's "fills are mode-stable" claim
   while R-D10's dark *values* stay ruled canon. Node-level lifecycle can't say that; the graph would
   either falsely kill R-D10 or falsely keep the dead claim. → `claim=` + the **AMENDED** state
   (Graphiti's invalidated-not-deleted, at claim granularity).
3. **Deliberate divergence.** DEF-005 exempts intrinsic squares; DEF-006 pointedly does not, and the
   ledger says *"a future reader will spot them disagreeing and try to reconcile. Do not."* A conflict
   gate with no way to record intentional divergence flags that pair forever — the gate would train
   people to ignore it. → `diverges-from(reason=…)`, listed in the reconciliation view as intentional,
   never flagged. (Offered to Dave as Decision 1, since it could also be expressed as
   `conflicts-with(resolution=intentional)` — recommended against, because the name invites the exact
   behaviour the record forbids.)

## Finding 4 — the audit caught two live conflicts, which is the build justifying itself

Both queued for Dave (guardrail held; `resolution=queued` never auto-resolves, never fails the gate):

- **C1.** R-D2: *"red/green/blue hold the SAME value in both roles; only amber diverges."* Since then:
  success-glyph ≠ success-background (R-D18/R-D14) and error-glyph dark `#CC4333` ≠ error fill
  `#B92F1E` (R-D20). The uniformity claim died in practice, unmarked. Recommended: confirm superseded
  (glyphs need glyph-strength contrast, fills need salience — different jobs).
- **C2.** R-D7: *"red = mode-stable, one value light+dark"* vs R-D20's per-mode error-glyph. Likely a
  never-recorded scope bound (R-D7 governs the fill role). Recommended: record the bound.

Yesterday's icon-011 ↔ R-D6 ↔ R-D3 reconciliation was the pain that justified this build; C1/C2 are
the proof it recurs — found by the same kind of read the generator now automates.

## Finding 5 — the sub-call dissolved once the audit was done

The open call was "Fable authors all edges vs stops at spec+gate and hands authoring to Sonnet."
The audit showed the split was drawn in the wrong place: the expensive half of edge-authoring is the
**judgment** (scoped/claim supersession, divergence, conflict detection), and doing the audit *is*
doing that judgment. So the seed file — 69 nodes, 88 edges, authored this session — already contains
the judgment half. What remains is **transcription** (inscribe `Edges:` lines into ledger entries /
ADR headers), which is mechanical *because* the seed exists, and machine-checkable (the generator
diffs inscribed edges against the seed). Recommended routing: Sonnet inscribes, generator verifies.

## What was built (all live, none wired until Dave rules)

- **ADR-0012** (proposed) — the convention: node identity · 7 types + qualifiers · alias map ·
  syntax/location · status ⊥ validation · generator · gate semantics · routing.
- **`notes/_decision-graph-seed-2026-07-21.json`** — the audited edges, grammar-conformant.
- **`knowledge/_build_decision_graph.py`** — generator (LIVE/AMENDED/DEAD/OPEN ledger · reconciliation
  view · what-touches-this map · validation rollup) + conflict gate (`--strict`). Selftest bites on
  unresolved/open/orphan; stays green on queued + diverges-from. Ran clean on the seed: 69 nodes,
  88 edges, 2 queued surfaced, 1 divergence listed. **Not in `_build_all.py`** (Decision 8 on the sheet).
- **`reviews/DECISION-GRAPH-CONVENTION-2026-07-21-v1.html`** (+ `.REVIEW` overlay copy) — the rulings
  sheet: 8 decision controls (taxonomy ×4, conflicts ×2, routing, gate wiring), defaults =
  recommendations, live export block emitting a paste-ready ruling set.

## Process notes

- CONSULT ran but its lexicon is design-layer (expanded the query to "dataviz") — the decisions layer
  has no consult surface, which is itself evidence for this build. Worth folding the graph JSON into
  the consult index later.
- Ledgers were read in full, not grepped: the regex sweep found 38 candidate lines; the read found 88
  real edges. Verbless prose relations ("the R-D18 move for the last three") are invisible to pattern
  matching — the reason the inscription verifier diffs against the seed rather than re-deriving.
- Nothing was inscribed into any ledger or wired into the build: the reflect-back guardrail held
  end-to-end. The only repo changes are new files + this capture.

## Resolved state / still open

- **Resolved:** the convention exists (proposed) · the audit is durable (seed) · the generator + gate
  run green · the sub-call has a recommendation grounded in evidence.
- **Open (Dave, on the sheet):** the 8 decisions — notably C1/C2, divergence-as-own-type, and gate
  wiring. Then: inscription pass (Sonnet, generator-verified) · advisory wiring · the capture ritual
  gains an edge-at-ruling-time step (post-acceptance, not before) · fold the graph into consult ·
  ADR-0007 part 2 (generate `_LIVE-STATE` blocks from the same parse) stays the horizon.
