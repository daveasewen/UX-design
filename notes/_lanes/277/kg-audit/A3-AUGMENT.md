# A3 — AUGMENT — what is orthogonal, lateral or meta that would make this graph a better designer brain
#277 · 2026-09-16 · lane A3 (Fable) · brief `BRIEF-A2-A3.md` § LANE A3 · reads A1 (`13a4cf2`) · **pinned sha `bedf383`** for every graph figure · READ-ONLY, nothing enacted · every external claim carries the URL read THIS session (§6, 33 sources)

Dave's ask, verbatim (`notes/_lanes/277/DAVE-RULINGS-2026-09-16.md`): *"is there anything orthogonal, lateral or meta we can employ to augment the graph"* · *"please research as much as you see fit, its always useful to check the state of the art"*. n-grams were his earlier thread and he is NOT proposing them; the six n-gram uses are parked as `P-269-1..5` and are not re-proposed here.

**Declaration.** Working tree dirty exactly as A1 declared (three `notes/` files + the parallel lanes); nothing under `knowledge/` dirty. Graph read by importing `_build_kg_explorer.extract()` + `extract_extra()` in memory — `main()` never called, `notes/_KG-EXPLORER.html` untouched. `_consult.py` was run with `--json` only (that path never reaches the `record_observation` writer at `_consult.py:199`); `knowledge/_graph-mark-observations.jsonl` mtime unchanged (Sep 14 17:04). `_compose_slice.py --explain` prints only. Token counts are tiktoken `cl100k_base`.

---

## 0 — The answer, in plain prose

**The graph's weakness is not its shape. It is that nothing that designs ever reads it.** The skill the agent runs at design time (`designer-skills-v2/generate-from-canon/SKILL.md`, step 1) says *read `knowledge/components/*.meta.json`*. That is 138 files, 414,755 tokens. The two doors that exist answer different questions: `_consult.py` is a keyword search over a 765-record index that holds 63 rulings — the graph holds 593 — and `_compose_slice.py`, the one door that actually walks edges, is a PROPOSAL that nothing calls. The exported pack (`designer-skills-v2/knowledge/`) ships metas, tokens, canon, snippets, guidelines and compliance — no graph, and `_rulings.json` is deliberately excluded as *"Dave's record"* (`_gen_pack_manifest.py:515`). So the 6,616 edges are visible to a human in a 2.9 MB HTML page and to no agent at all. A1 measured the symptom: 12 edge types with no consumer, 47% of the graph.

**Measured (§1): answering the 12 canonical questions the way the agent must today costs about 2.6 million tokens of reading; the answering slices of the graph total about 2,100.** The whole graph serialised is 798,152 tokens — it cannot be put in a context window either. The efficiency half of Dave's question therefore has a blunt answer: the single most powerful augmentation is a **query surface** — a door that takes one of the twelve questions and returns the ≤ 1K-token slice, with the join class and the `$note` on each edge. That is "meta" in the sense that matters: structure about how the structure is read.

**What the state of the art says, read this session (§2).** Most of it is built for the opposite problem — extracting a graph from prose with an LLM (GraphRAG, Graphiti/Zep, HippoRAG). This graph is the other kind: it is ratified, structural, small, and its whole value is that every edge is either a typed field or Dave's sentence. The `s274-D12` shape — a plausible edge nobody ruled — is exactly what those systems manufacture by design. So the useful imports are the *meta* ones: inverse and transitive closure computed at build and labelled derived (OWL's `inverseOf`/`TransitiveProperty`, without an OWL reasoner); shape validation of the kind SHACL does (`_validate_kg.py` checks grammar and resolution, not that `obeys` points at a `rule:` or that a rule binds anything); and the persistence-semantics distinction the 2026 "Missing Knowledge Layer" paper draws — rulings are *knowledge* with supersession, not memories that decay. The one *orthogonal* addition that pays for itself is token nodes (Q9 costs 595K tokens today and has no node kind; the join is structural and the generator chain already exists — `P-269-7`). The one *lateral* addition worth having is an embedding neighbourhood over nodes, advisory only, shown dashed like `mentions`, never landed as an edge.

**Ranked shortlist (§4):** 1 ASK (the typed-question door) · 2 CLOSURE (derived inverse/transitive edges at build) · 3 SHAPES (per-type endpoint and per-kind minimum-connectivity checks, advisory) · 4 TOKENS (token nodes + `bindsToken`/`aliasOf`) · 5 NEIGHBOURS (embedding index, advisory). Refusals in §5.

---

## 1 — Query-time reality, measured

### 1.1 How the agent reads the graph today — plain

It does not. It reads files. The four consumption paths that exist:

| path | what it is | reads the graph? | tokens |
|---|---|---|---|
| `designer-skills-v2/generate-from-canon/SKILL.md` step 1 | "look in `knowledge/components/*.meta.json` for the contract" — the agent picks metas by judgement, then reads them | the meta's own `edges` block only (one node's out-edges) | 2,576 median per meta · 414,755 all 138 |
| `knowledge/_consult.py "<q>"` | keyword search + lexicon over `_consult-index.json` (765 records: 470 rule · 105 open-item · 63 ruling · 54 defect · 48 gate · 17 adr · 8 assertion); `_graph_edges.py` appends `supersedes/refines/bounds` neighbours from `_decision-graph.json` (172 edges, a different graph) | no — text match; 63 of 593 rulings; 3 of 51 edge types, from the OLD decision graph | index 109,270 · one answer 2,706–5,602 (five components sampled) |
| `knowledge/_compose_slice.py "<task>" --explain` | the compose-time door — roles → components → edges → rules → composites → icons → token tiers → rulings | YES — `commonPattern`, `usedInContext`, `consumes`, `hasPart`, `composedOf`, `containedBy`, `family`, `groupsWith`, `governedBy`, `mustNotNeighbour` | 895 for "a bar chart comparing spend by category" — **but ⛔ PROPOSAL, ADVISORY, NOT WIRED** (its own docstring) |
| `notes/_KG-EXPLORER.html` | the baked page | yes, for a human | 953,148 — unreadable by an agent |

The pack (`designer-skills-v2/knowledge/` = `assets canon compliance components guidelines snippets tokens`) carries no graph file and no `_rulings.json` (`_gen_pack_manifest.py:515` excludes it as "Apollo's ruling store — Dave's record"). **An adopter's Copilot has the metas and nothing else of the graph.** Every augmentation below is therefore judged twice: does it help the in-repo agent, and does it travel in the pack.

### 1.2 The cost table — the 12 canonical questions, today

Method: for each question, the file(s) the agent must read TODAY to answer it (no query surface for that question exists unless named), counted whole because grep is not a token-saver for a model that must *read* what grep returns and cannot know in advance which lines matter; the door output where a door exists; and the GRAPH SLICE — the answering edges serialised as `{type, s, t, label, note}` — averaged over five sample components (`button`, `chart-bar`, `notifications`, `list-items`, `data-grid`) or five sample rules/rulings/intents. Full per-sample figures in `A3-shortlist.json → measure`.

| Q | question | what the agent reads today | **today (tokens)** | door today | **graph slice (tokens / edges)** | A1 verdict |
|---|---|---|---|---|---|---|
| Q1 | what governs this component? | `_rulings.json` (`governs[]` names the component; 813 KB) + the meta | **237,934** | `_consult.py` 4,374 avg — keyword, not the edge | 305 / 7 | ANSWERED 78% |
| Q2 | which components does this rule bind? | the rule's row + all 138 metas for `edges.obeys` | **464,205** | none | 36 / 1 | PARTIAL 22.8% |
| Q3 | what principle underlies this rule, and its grade? | `_rules-index.json` + `_ux_principle_nodes.json`, and guess | **102,363** | none | 0 / 0 | UNANSWERABLE — `rule→ux` 0 edges |
| Q4 | which rules conflict for this component? | the meta's `obeys` + the cited rows + the guideline `.md`s (conflict is stated nowhere) | **168,737** | none | 441 / 13 (the obeys list; no conflict type exists) | PARTIAL 7.3% |
| Q5 | what did Dave rule about this, and when? | `_rulings.json` whole — the date and `ruled` sentence live only there | **232,648** | `_consult.py` 4,374 avg (63 of 593 rulings indexed) | 563 / 6 (governs → ruling.date + ruledIn) | ANSWERED at 2 hops; typed 0% |
| Q6 | what evidence supports that ruling? | `_rulings.json` to find the entry (the entry itself is 300–600 once found) | **232,648** | `--fetch <id>` if indexed | 204 / 2 | ANSWERED 100% |
| Q7 | which components answer this intent / shape? | `chart-intents.json` + `roles.json` + 138 metas | **419,098** | `_compose_slice` 895 (unwired) | 96 / 3 | ANSWERED 100% |
| Q8 | what must this component not sit next to? | the meta (51 of 70 `mustNotNeighbour` are `ref:null` + `$note`) | **5,286** | `_compose_slice` 895 (unwired) | 20 / 0.4 | PARTIAL 12.4% typed |
| Q9 | what tokens does it consume; what breaks if I change one? | the meta's `tokens` strings + `canon.css` 588,102 (or `tokens/*.json` 528,168); reach only in `_GRAPH-REPORT.md` 1,854 | **595,242** | none | 0 / 0 | UNANSWERABLE — no `token:` kind |
| Q10 | which pattern / context is it used in? | the meta | **5,286** | `_compose_slice` 895 (unwired) | 284 / 7 | ANSWERED 100 / 99.3% |
| Q11 | what is the WCAG / accessible-name obligation? | the 55 `compliance/rules/*.json` (`applies_to`) | **27,009** | none — `sc` is not a consult record kind | 190 / 5 | ANSWERED 97.8% |
| Q12 | what icon / logo / photo may I use here? | `icons.manifest.json` 40,943 + photography manifest 66,529 + the snippet, by eye | **112,758** | none | 0 / 0 | UNANSWERABLE — no `asset:` kind; lane RI proposes 688 nodes / 1,299 edges (`5520d43`) |
| | **total** | | **≈ 2,603,000** | | **≈ 2,140** | |

Three more numbers that frame every augmentation:

- **the whole graph serialised as the explorer serialises it: 798,152 tokens** (2,465,653 bytes). A lean `[s, type, t]` edge list alone is 181,531. Neither fits a working context beside a design task. Any "just give the agent the graph" plan is dead on this number.
- **a component's full 1-hop neighbourhood (all types, in and out, with notes): mean 901 tokens, max 3,057, min 391.** That is the natural unit of a design-time read — roughly a third of one meta.
- **what one keyword consult costs versus what it answers:** 2,706–5,602 tokens per query, returning text matches over 63 rulings; the typed `governs` slice for the same component is 179–463 tokens and is complete over all 593.

**Plain reading.** Today the ratio between "what the agent reads" and "what it needed" is about 1,200 : 1. The graph already holds the answers to 8 of 12 questions in slices of a few hundred tokens; the agent cannot ask for them. The two UNANSWERABLE questions with no node kind (Q9, Q12) are also the two with the largest today-cost (595K, 113K). That ordering is the ranking in §4.

### 1.3 What each augmentation does to the cost — summary (detail per item in §2)

| augmentation | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 | Q11 | Q12 | build-time cost | pack? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **ASK door** (typed question → slice) | 238K→0.3K | 464K→0.04K | — | 169K→0.4K | 233K→0.6K | 233K→0.2K | 419K→0.1K | 5K→0.02K | — | 5K→0.3K | 27K→0.2K | — | none at query time; pure Python over the JSON the explorer already bakes | yes if the baked graph JSON ships (356 KB gz-able) — a pack decision, Dave's |
| **CLOSURE** (derived inverse/transitive) | adds `governedBy*` so the meta alone answers Q1 | adds `boundBy*` on rules | — | — | Q5 becomes 1 typed hop | — | — | — | — | — | adds `mustMeet*` on components | — | +≈ 2,000 derived edges, +≈ 8% payload | yes (they are in the baked JSON) |
| **SHAPES** (validator) | no query change | no | no | no | no | no | no | no | no | no | no | no | one validator run per build | n/a (a gate) |
| **TOKENS** (token nodes) | — | — | — | — | — | — | — | — | 595K→≈ 1K | — | — | — | +≈ 950 nodes / +≈ 3,000 edges from existing generators | yes — `tokens/*.json` already ships |
| **NEIGHBOURS** (embeddings, advisory) | — | candidates for the 77% of rules with no `obeys` | candidates for the 0% | candidates | — | — | recall on synonyms | — | — | — | — | — | an index build (+ a model or the pure-Python shingle fallback `_ngram.py` already has) | no — advisory, in-repo only |

---

## 2 — The survey: nine named areas plus two found, each against this graph

Format per item: **plain** (what it adds for the hyper-designer, one sentence) · **what I read** (URL, this session) · **technical** · **class** (orthogonal = a new dimension · lateral = a second index over the same nodes · meta = structure about the structure) · **closes** (A1 gap, numbered in §3) · **touches** (P-id / ruling) · **s274-D12 test** · **verdict**.

### 2.1 GraphRAG — community summaries, local/global search, LazyGraphRAG

**Plain.** GraphRAG builds a graph out of prose with an LLM, then writes summaries of each cluster so a question about "the whole corpus" can be answered; for us the cluster summaries are the only transferable idea, and only as a compile view, never as nodes.

**What I read.** Edge et al., *From Local to Global*, arXiv 2404.16130 (v2, 19 Feb 2025) — abstract: an LLM derives an entity graph from documents, then "pregenerate[s] community summaries for all groups of closely related entities"; each summary yields a partial answer, reduced to a final one; gains are on *global sensemaking* questions over ~1M-token corpora [S1]. Microsoft Research blog, *LazyGraphRAG* (25 Nov 2024, updated 6 Jun 2025) — indexing at "0.1% of the costs of full GraphRAG" by replacing LLM extraction with noun-phrase co-occurrence and deferring all LLM use to query time; "more than 700 times lower query cost" than global search for comparable quality; the authors' own caveat that a summarised index still "has use value beyond question answering (e.g., reading and sharing as reports)" [S2]. GraphRAG docs, local search: combines "structured data from the knowledge graph with unstructured data from the input documents to augment the LLM context … at query time" [S3].

**Technical.** Our graph is not extracted; it is minted from typed fields (STRUCTURAL 6,277 of 6,616). GraphRAG's index stage is the thing `s274-D12` refused (the 27 regex candidates; 52 of 78 generated edges wrong at #267). Its *query* stage — local search = "fan out from the matched entity to its neighbours and hand that to the model" — is exactly the ASK door in §4.1, and we can do it without embeddings because our entities have ids. Community summaries map onto `P-269-8` compile views (period digest, goal tree, decision trail): derived documents a human reads, regenerated each build, never node ids. LazyGraphRAG's design lesson is the one that fits: defer the expensive step to query time and budget it — our "relevance test budget" is a token cap on the slice.

**Class** meta (query mechanism) / lateral (summaries). **Closes** G6 (no-consumer types) via the door; nothing structural. **Touches** `P-269-8`. **s274-D12** — extraction stage FAILS the test outright; local-search stage passes (it reads ratified edges). **Verdict:** import the query pattern (→ §4.1), refuse the extraction and the LLM-written community nodes (→ §5).

### 2.2 Property graph versus RDF/OWL reasoning — inverse, transitive, chain inference

**Plain.** OWL lets you declare that `governedBy` is the inverse of `governs` and that `containedBy` chains, and a reasoner then fills in the missing direction — we can have that filling-in at build time as labelled derived edges without adopting OWL or a triple store.

**What I read.** W3C OWL 2 Primer (Recommendation 11 Dec 2012) — `ObjectInverseOf`, `TransitiveObjectProperty(:hasAncestor)`, the property characteristics a reasoner uses "to infer triples that are not explicitly stated" [S4]; Stanford JTP note on RDFS/OWL reasoning capability and `owl:TransitiveProperty` enforcement [S5]; a 2013 lecture on OWL 2 profiles and the SROIQ basis, chains and inverses [S6]. Property graphs (Figma's variable API, Neo4j-style) carry no such axioms — an inverse is a second stored edge or nothing.

**Technical.** A1 found the only true inverse pair is `governs`/`governedBy`, 1,484 vs 28, and that **12 of 20 kinds are pure sinks** — `artefact`, `evidence`, `session`, `pattern`, `context`, `role`, `intent`, `shape`, `axe`, `principle`, `standard`, `policy` emit nothing. That is not a modelling error; it is the one-home rule (`s270-D2`: derived, generation chain not copy chain). But at query time a sink cannot be *started from*: "which components sit in `context:dashboards`?" is answerable only by scanning every component's out-edges. The fix OWL would give a reasoner, we give the extractor: for a declared list of pairs, mint the inverse with `$derived: "inverseOf governs"`; for `containedBy`, `under`, `hasPart`, `composedOf`, mint the transitive closure with `$derived: "transitive, depth n"`. Nothing is written to a meta or to `_rulings.json`; the derived edges exist only in the baked graph and are dashed, like `mentions`. Chain inference (component `obeys` rule ∧ rule `cites` sc ⇒ component `appliesTo` sc) is a different animal: it manufactures a *claim* about the component from a PROSE edge (`cites` is regex-minted, 51 edges) — refuse.

**Class** meta. **Closes** G10 (inverse asymmetry), G11 (sinks unreadable as starts), G13 (Q5 becomes one typed hop from the component). **Touches** `s270-D2` (one home — respected, since derived edges have no home but the build), `s274-D10` (nulls kept). **s274-D12** — an inverse of a ratified edge asserts nothing new: PASS; transitive closure over structural containment: PASS if labelled; chain inference across a PROSE edge: FAIL. **Verdict:** shortlist (→ §4.2), closure only.

### 2.3 Temporal / bi-temporal validity — Graphiti, Zep

**Plain.** Zep's graph stamps every fact with when it became true and when it stopped, so an agent can ask "what was the rule last March" — our rulings already carry a date and 48 authored supersession edges, so the missing half is a query ("is this still in force?"), not a new store; and it is parked already.

**What I read.** Rasmussen et al., *Zep: A Temporal Knowledge Graph Architecture for Agent Memory*, arXiv 2501.13956 (20 Jan 2025): Graphiti "dynamically synthesizes both unstructured conversational data and structured business data while maintaining historical relationships"; DMR 94.8% vs MemGPT 93.4%; LongMemEval up to +18.5% [S7]. Graphiti README (getzep/graphiti, read 2026-09-16): "tracking what's true now and what was true before"; facts carry an *as of* [S8]. Zep's own glossary: bi-temporal = valid time plus ingestion time; "superseded facts are invalidated, not deleted" [S9].

**Technical.** `_rulings.json` entries carry `date`, `status`, and the `_ruling_edges.json` layer carries `supersedes` 3 · `supersedesClause` 9 · `retires` 1 · `corrects` 1 · `narrows` 2 (AUTHORED, `s267-D3`). That is valid-time on the ruling node and invalidation as an edge — the Graphiti shape, minus a `t_invalid` on the *edge*. `P-269-6` already parks the edge-level window for the decision graph ("we need this recorded with tripwires", not before the demo). What the *designer* needs at design time is one derived boolean — `inForce` — computed by walking `supersedes*`/`retires` closure (free with §4.2) and surfaced by the ASK door as `⛔ superseded by s…` — the mark `_graph_edges.py` already prints on the OLD decision graph (#115 step 3) and never on this one. Graphiti as a runtime (LLM extraction per episode, a Neo4j dependency) is the wrong size for a pure-Python pack.

**Class** orthogonal (time). **Closes** none of A1's numbered gaps directly; makes Q5 honest. **Touches** `P-269-6` (do not re-propose; name it), `s267-D3`. **s274-D12** — a validity window on an authored edge is metadata, PASS; Graphiti's extraction FAILS. **Verdict:** not shortlisted as a build (parked); the `inForce` derivation rides on §4.2 and its display on §4.1.

### 2.4 Hypergraphs and n-ary relations — a ruling that binds three things at once

**Plain.** When one decision ties a component, a rule and a context together, a plain edge cannot hold all three — but a *node* for the decision can, and that is precisely what a `ruling:` node already is; we do not need hyperedges.

**What I read.** W3C Working Group Note *Defining N-ary Relations on the Semantic Web* (12 Apr 2006): "In Semantic Web languages … a property is a binary relation"; Pattern 1 "create a new class and n new properties to represent an n-ary relation" (the reified relation instance); Pattern 2 lists; and the explicit warning that RDF reification talks about *statements*, whereas n-ary arguments "provide additional information about the relation instance itself" [S10]. Ontotext on RDF-star as edge-annotation [S11].

**Technical.** `ruling:s274-D12` `governs` 4 artefacts, is `evidencedBy` 1 evidence node, `ruledIn` a session — one node, five arms: Pattern 1 exactly. `polarity:` nodes with `hasParty` (68) are the same pattern for tensions (`s275-D2`). The three-arm case Dave might mean — *this rule binds this component in this context* — has no home today: `obeys` is component→rule, `usedInContext` is component→context, and nothing joins the two. The cheap n-ary form is what `edges.obeys` already carries under `$obeys-contract`: a `$when`/`$why` sentence on the edge (AUTHORED). If a typed scope is ever wanted, it is a field on the `obeys` edge (`scope: context:dialog`), not a hyperedge and not a new node kind.

**Class** meta. **Closes** nothing today; keeps a door open for Q4 ("conflict" is an n-ary judgement: rule A vs rule B *for* component C — a `polarity`-shaped node, authored). **Touches** `s275-D2`, `s276-D3` (the `obeys` grammar). **s274-D12** — n/a (modelling, not minting). **Verdict:** no build; a note for A2 that `ruling`/`polarity` are the reified relations already, and Q4 conflicts, when authored, should be `polarity`-shaped.

### 2.5 Embeddings as a lateral index — semantic neighbours the graph does not state

**Plain.** An embedding index would let the agent ask "what is like this?" across all 3,897 nodes and get back things no edge connects — useful as *suggestions* for the 77% of rules that bind no component, dangerous the moment a suggestion is drawn as an edge.

**What I read.** HippoRAG (NeurIPS 2024) — Personalized PageRank over an LLM-built KG with query concepts as seeds, "up to 20%" over RAG on multi-hop QA [S12]; HippoRAG 2, arXiv 2502.14802 (Feb 2025) — the honest finding that graph-augmented RAG "performance on more basic factual memory tasks drops considerably below standard RAG" until passages are integrated [S13]; SubgraphRAG, arXiv 2410.20724 — a lightweight scorer retrieves a *budgeted* subgraph, "encoding directional structural distances", trading retrieval size against effectiveness [S14]; the 2026 graph-memory survey, arXiv 2602.05665 — taxonomy knowledge vs experience memory, structural vs non-structural, and retrieval by "traversal, subgraph extraction, and multi-hop relational queries" [S15].

**Technical.** Our nodes have short labels and, on 2,971 edges, a human sentence. Embedding node label + attached notes gives a vector per node; nearest-neighbour over 3,897 vectors is trivial. Two honest limits: (i) the #269 research chose pure Python for the retrieval spine because `_search_core.py` ships byte-identical in the pack — an embedding model is a dependency the pack does not carry; the shingle/Jaccard code in `_ngram.py` (`P-269-3`) is the dependency-free fallback and was measured at 22 useful near-duplicate pairs; (ii) HippoRAG's own second paper says naive graph-first retrieval loses on factual questions — the typed slice (§4.1) must come first and the neighbours ride behind it as a separate, labelled section. PPR over *our* graph with the question's nodes as seeds is a good ranker for the slice when it overflows the budget (e.g. `sc:4.1.2` has degree 111) — that is a lateral use with no new claims.

**Class** lateral. **Closes** none structurally; raises *candidate* recall for G3 (`rule→ux` 0%), G4 (`obeys` 7.3%), G2. **Touches** `P-269-3` (its shingle sibling), `s274-D12`, `s276-D5` (name-match tier NOT widened — an embedding neighbour is a softer name-match). **s274-D12** — FAILS if landed; PASSES as advisory display with the `proposedType`/dashed treatment `mentions` already has. **Verdict:** shortlist last (→ §4.5), advisory, in-repo only, pure-Python fallback first.

### 2.6 Typed-schema / SHACL-style shape validation versus `_validate_kg.py`

**Plain.** SHACL checks not just "is this well-formed" but "does every node of kind X have the edges a node of kind X must have, pointing at the kinds it may point at" — our validator checks grammar and that refs resolve, and never that a rule binds anything or that `obeys` lands on a rule.

**What I read.** W3C SHACL (Recommendation 20 Jul 2017): "a language for validating RDF graphs against a set of conditions"; node shapes, property shapes, `sh:targetClass`, and a validation *report* listing each violation [S16]; SHACL 1.2 Core editor's draft adds "node expressions" to compute target lists [S17]; xpSHACL (2025) on making violation reports explainable [S18].

**Technical.** `_validate_kg.py` (633 lines) does (a) grammar + resolution per ref, (b) null-with-note, (c) provenance presence, (d) schema keys, (e) generator idempotence, (f) ruled verdicts present. What it cannot say: `obeys` → `rule:|ux:` only (the schema's `obeysEdge` definition constrains it; other types accept any `kind:`); `governedBy` → `ruling:` only; a `rule` with zero in-edges of type `obeys`/`appliesTo` (363 of 470 today); a `ux` with degree 0 (99); an `sc` that `appliesTo` nothing; the explorer's island/orphan header computed over the right graph (A1 §3: scope defect at `main():534-539`). BRIEF criterion 2 — *connectivity has an intent, per kind* — is a SHACL shape by another name: `kind → {min in-degree by type, allowed target kinds by type}`. Written as a JSON table beside `meta.schema.json` and read by the validator, it is 150 lines of Python, advisory at birth (report, exit 0), promotable per `AGENTS` principle 5. It gives A2's per-kind minimums a home that outlives the audit.

**Class** meta. **Closes** G7 (7 schema-only types acquire a consumer — the validator), G8 (islands/orphans on the full graph), G9 (99 `ux:` orphans become a reported count), and gives G2/G3/G4 a *measured* line per build. **Touches** `s131-D2`/`s133-D1` (the parse gate's scope), `s274-D9` (advisory vs blocking is Dave's). **s274-D12** — n/a, mints nothing. **Verdict:** shortlist (→ §4.3).

### 2.7 Provenance — PROV-O against the ruling → evidence → session trail

**Plain.** PROV-O's three words — Entity, Activity, Agent — are already our `ruling`/`evidence`/`artefact`, `session`, and Dave; the trail exists, it is just not named in a way another tool could read, and the "Agent" is a string, not a node.

**What I read.** W3C PROV-O (Recommendation 30 Apr 2013): PROV-O "expresses the PROV Data Model … using OWL2"; classes `prov:Entity`, `prov:Activity`, `prov:Agent`; `wasDerivedFrom`, `wasGeneratedBy`, `used`, `wasAttributedTo`, `wasAssociatedWith` [S19]; the CASRAI/FAIR summaries of the same [S20].

**Technical.** Mapping, exact: `ruling` = Entity; `evidence` = Entity (`evidencedBy` ≈ `wasDerivedFrom`); `session` = Activity (`ruledIn` ≈ `wasGeneratedBy`); `artefact` = Entity (`governs` ≈ an influence relation with no PROV term — it is ours); `by: "Dave"` = Agent (`wasAttributedTo`) — a **string on 593 rulings, not a node**. The lane that enacted a ruling is an Activity with no node either (`evidence` nodes like `commit d57a1e9` stand in). The value of naming this is small in-repo and larger in the pack: a PROV-shaped export is what an adopter's own governance tooling could ingest. Not a build; a paragraph in the explorer's legend and, if the pack ever ships the graph, an `@context` mapping. `agent:dave` as a node would give Q5 a true start ("what did *Dave* rule") but it is one node of degree 593 — a hub that tells the agent nothing it did not know.

**Class** meta. **Closes** nothing numbered. **Touches** `s267-D3`. **s274-D12** — n/a. **Verdict:** no build; record the mapping (done here) and let A2 use it when naming the governance layer.

### 2.8 Design-token graphs — DTCG 2025.10 aliasing, Figma variables

**Plain.** The token spec now says a token's value may be a *reference* to another token and tools must follow the chain to the real value — that chain is a graph, ours already exists in `tokens/*.json` and `canon.css`, and it is the missing kind that would answer "what breaks if I change this" in one hop instead of a 595K-token read.

**What I read.** DTCG *Design Tokens Format Module 2025.10* (draft report dated 08 Sep 2026; "Latest published version" 2025.10): §3.8 "A design token's value can be a reference to another token. The same value can have multiple names or *aliases*"; §7 curly-brace and JSON-Pointer reference syntax, chained references, circular-reference detection, property-level references; `$extends` on groups as "syntactic sugar for JSON Schema's `$ref`" [S21]; the W3C CG announcement that 2025.10 is the "first stable version" (28 Oct 2025) [S22]. Figma plugin API: `VariableCollection.modes`, `Variable.valuesByMode`, `scopes`, alias values (`VARIABLE_ALIAS`) [S23]; Figma help on aliasing as the mechanism of a three-tier token architecture [S24].

**Technical.** The join is structural and already parsed: `_GRAPH-REPORT.md` prints per-token reach (`text/default` → 107 components) from the `tokens` field every meta carries (136 of 138; the value string starts with the token path, e.g. `"text/default @ .t-cm-label — …"`), and `gen_canon_tokens.py` resolves `tokens/*.json` (343 vars + 116 dark overrides) into `canon.css`. Token nodes: `token:<path>` (≈ 460 semantic/component + the primitive tier ≈ 932 leaves per `_compose_slice.py`'s own limit note — the tier grain is the right node grain, the leaves are `aliasOf` targets); edges `aliasOf` token→token (the DTCG reference chain, structural), `bindsToken` component→token (from the meta `tokens` field, structural prefix parse), `composite` type-composite→token (from `typography-composites.json`). Q9 becomes a 2-hop query; `P-269-7`'s blast-radius gate becomes a graph count. Modes (light/dark, the three `data-apollo-theme`s) are the DTCG "mode" dimension — a property on `aliasOf`, not a node.

**Class** orthogonal (a new node kind and dimension). **Closes** G1 (Q9, the largest today-cost). **Touches** `P-269-7` (the gate — this is its data), `s269-D1` (the entity-gaps list), `meta.schema.json` (a grammar ADDITION in lane RI's shape: `token:` in the node-id grammar, a `bindsToken` edge type). **s274-D12** — structural joins only: PASS; the prose tail of the `tokens` strings (" — the canvas beside the column") stays a `$note`. **Verdict:** shortlist (→ §4.4).

### 2.9 Agent memory architectures — what "memory" means for an autonomous design agent

**Plain.** The literature splits agent memory into working, episodic, semantic and procedural, and the newest paper adds that *knowledge* must not be treated like *memory* — it does not fade, it is superseded; this graph is knowledge plus procedure, it is not episodic memory, and it must not be given decay.

**What I read.** CoALA, arXiv 2309.02427 (Princeton, Sep 2023): working / episodic / semantic / procedural memory, a structured action space, a decision cycle [S25]; *The Missing Knowledge Layer in Cognitive Architectures for AI Agents*, arXiv 2604.11364 (13 Apr 2026): CoALA and JEPA "both lack an explicit Knowledge layer with its own persistence semantics … systems apply cognitive decay to factual claims"; four layers "Knowledge, Memory, Wisdom, Intelligence" with "indefinite supersession, Ebbinghaus decay, evidence-gated revision, and ephemeral inference respectively" [S26]; *Externalization in LLM Agents*, arXiv 2604.08224 (Apr 2026): "memory externalizes state across time, skills externalize procedural expertise, protocols externalize interaction structure, and harness engineering serves as the unification layer" [S27]; *Corpus2Skill / Don't Retrieve, Navigate*, arXiv 2604.14572 (Apr 2026): an offline compiler "distills the corpus into a hierarchical skill directory, and at serve time an LLM agent navigates it, drilling from a bird's-eye view through progressively finer summaries" [S28]; the graph-memory survey [S15]; Mem0 and Letta READMEs as the product shape ("memory layer", "stateful agents") [S29, S30].

**Technical — where this graph is, and is not, each memory.**

| memory type (CoALA) | persistence (2604.11364) | what we have | what we do not |
|---|---|---|---|
| **semantic / knowledge** | indefinite supersession | `rule` 470 · `sc` 55 · `ux` 145 · `component` 137 with typed edges; `supersedes*` on rulings | supersession is authored on 48 ruling pairs only; rules have no supersession at all |
| **procedural** | evidence-gated revision | the four skills, `AGENTS.md`, gates (`_validate_*`), `roles.json` | none of it is in the graph as nodes — `artefact:` nodes name the files but the *procedure* (step 1 read metas) is prose |
| **episodic** | decay | `session` 92 · `evidence` 886 · `_SESSIONS.jsonl`, the Memento index | correct that it is NOT in this graph beyond the ruling→session hop; Memento is the episodic store and its door is separate |
| **working** | ephemeral | nothing — the agent's context at design time is whatever files it opened | **this is the gap §1 measures**: no slice, no budget, no door |

The design-time consequence the papers converge on (Corpus2Skill, the Skills progressive-disclosure pattern [S31], SubgraphRAG's budget): give the agent a *navigable* top level of a few hundred tokens and let it descend. For us the top level exists — `roles.json` (4,343 tokens, 12 roles) and the 14 intents / 23 shapes — and `_compose_slice.py` is the descent. What no paper recommends is applying forgetting to knowledge; `s274-D9`'s "durable/scalable" worry and the `s276-D5` "then STOP and look again" are evidence-gated revision, the right semantics for rules.

**Class** meta. **Closes** G6 (a consumer), G13. **Touches** `P-269-8` (compile views are Corpus2Skill's "hierarchical directory"), `P-269-9` (persona/JTBD would be the *task* axis of the working slice). **s274-D12** — n/a. **Verdict:** the framing for §4.1; explicitly refuse decay (→ §5).

### 2.10 Found, not on the list — query-skill graphs and a token-budgeted slice

**What I read.** SkillTrace, arXiv 2608.02356 (Aug 2026): decompose a task into atomic skill queries, bipartite match to seed skills, "traverse the skill subgraph with personalized PageRank and selection constraints to retrieve a composable skill bundle" [S32]; TEMPR / "Hindsight is 20/20", arXiv 2512.12818: recall that "fits within a specified token budget" [S33].

**Technical.** Both describe `_compose_slice.py` with one addition it lacks: a *budget* argument and a ranker for overflow. `--budget 1200` with PPR from the task's role/intent seeds would make the slice deterministic in size. Folded into §4.1.

### 2.11 Found — the meta/explorer "no consumer" is itself the state-of-the-art failure mode

Every graph-memory paper read this session measures retrieval, not storage. A1's "12 types, 3,125 edges, no consumer" is the graph equivalent of an index nobody queries. It is the strongest argument in this document for building the door before any new node kind — except tokens, whose today-cost (595K) dwarfs the rest.

---

## 3 — The A1 gaps, numbered, and which augmentation closes each

| # | A1 gap (source) | closed by | how | class |
|---|---|---|---|---|
| G1 | Q9 no `token:` kind (A1 §7) | TOKENS | `token:` nodes + `aliasOf` + `bindsToken`, structural | orthogonal |
| G2 | Q12 no `asset:` kind (A1 §7) | lane RI (`5520d43`), not this lane | 688 nodes / 1,299 edges proposed | orthogonal |
| G3 | `rule→ux` 0 edges, Q3 (A1 §7) | not closable by augmentation — authored work (`s269-D5` shape) | NEIGHBOURS supplies ranked *candidates* only | — |
| G4 | `obeys` 7.3% of components, Q4 (A1 §7) | not closable by augmentation (`s274-D12`: authored the other way) | NEIGHBOURS candidates; SHAPES reports the count per build | — |
| G5 | `mustNotNeighbour` 12.4% typed, 51 dangling (A1 §2) | SHAPES reports; A2 judges the anaphora | — | meta |
| G6 | 12 types / 3,125 edges with no consumer (A1 §4) | ASK | the door reads `evidencedBy`, `appliesTo`, `definedIn`, `ruledIn`, `checkedBy`, `hasParty`, `enforcedBy`, `boundBy`, `enClause`, `flaggedBy`, `tensionWith`, `verifiedBy` | meta |
| G7 | 7 schema-only types incl. `obeys` (A1 §4) | SHAPES + ASK | validator checks target kinds; door reads them | meta |
| G8 | explorer `islands 2 / orphans 0` scope defect (A1 §3) | SHAPES | recompute after `extract_extra()`; the validator prints the true figure | meta |
| G9 | 99 `ux:` orphans (A1 §3) | SHAPES (visibility) · authored `obeys` (closure) | reported per build | meta |
| G10 | `governs` 1,484 vs `governedBy` 28 (A1 §4) | CLOSURE | derived inverse, labelled | meta |
| G11 | 12 of 20 kinds are pure sinks (A1 §6) | CLOSURE | every sink gains derived out-edges at query time | meta |
| G12 | PROSE tier 291; `cites` presented as hard (A1 §5) | SHAPES (join-class carried on every edge; `cites` dashed) | a `joinClass` field on the baked edge | meta |
| G13 | Q5 `ruledIn` unreachable typed from a component (A1 §7) | CLOSURE + ASK | `governs⁻¹ ∘ ruledIn` as a named path | meta |

---

## 4 — Recommendation: the ranked shortlist (≤ 5), one-lane estimates

Ranking rule: today-cost saved × questions touched, divided by build risk, with `s274-D12` as a hard filter. Estimates are one lane each, Opus unless judgement is named.

### 4.1 ASK — the typed-question door (`_ask_kg.py`), rank 1

**Plain.** A command that takes one of the twelve questions and a node id and returns the answering slice — a few hundred tokens with the join class and Dave's sentence on every edge — so the agent stops reading 200K-token files to answer questions the graph already holds.

**Technical.** Pure Python over the baked nodes/edges (import `extract()`+`extract_extra()` or read a `_kg.json` the explorer build also writes). Twelve verbs = the twelve questions (`governs`, `binds`, `principle`, `conflicts`, `ruled`, `evidence`, `answers`, `avoid`, `tokens`, `usedIn`, `wcag`, `assets`); each returns `{q, node, edges:[{type, t, label, joinClass, note, derived?}], declared:[{missing edge type}]}` and honours `--budget N` (PPR-ranked overflow, §2.10). Declares UNANSWERABLE with the missing type named, never invents. Same two-stage posture as `_consult.py` (refs, then `--fetch`). Wire `_compose_slice.py` as its composite verb (`compose "<task>"`). The one decision with weight — whether `generate-from-canon` step 1 becomes "ask, then read the metas it names" — is Dave's, already framed in `notes/_PROPOSAL-compose-time-door-2026-09-14-v1.html`. **Pack:** needs the baked graph JSON to ship (356 KB per lane RI's measure of one family; whole graph 2.4 MB, gzips well) — a pack change, therefore a release, therefore Dave's (the `P-269-1` pin).

**Cost:** one Opus lane, ~1 day: door + 12 selftest bites (one per question, known-answer) + runbook paragraph. Query-time cost: 20–600 tokens per question (§1.2 column). **Closes:** G6, G7 (consumer side), G13; every ANSWERED/PARTIAL question's cost. **Touches:** `_RUNBOOK-consult.md`, `generate-from-canon/SKILL.md` step 1 (Dave), `P-269-8` (the door is compile-view-shaped), `s274-D10` (nulls carried as `declared`). **s274-D12:** PASS — reads only.

### 4.2 CLOSURE — derived inverse and transitive edges at build, rank 2

**Plain.** Compute the missing direction of every ratified edge, and the chains for containment, at build time, mark them "derived", and never write them anywhere a human authors — so a sink like `context:dashboards` can be a starting point.

**Technical.** In `_build_kg_explorer.py` after `extract_extra()`: a table `INVERSE = {governs: governedBy*, appliesTo: mustMeet*, evidencedBy: evidences*, ruledIn: ruled*, definedIn: defines*, commonPattern: patternOf*, usedInContext: contextOf*, providesRole: providedBy*, answersIntent: answeredBy*, hasDataShape: shapeOf*, renderedBy: renders*, obeys: obeyedBy*}` (starred = derived, dashed, `$derived: "inverseOf <type>"`); `TRANSITIVE = {containedBy, under, hasPart, composedOf}` with depth cap 4; `inForce` on rulings from `supersedes*`/`retires` closure. Expected +≈ 6,600 inverse edges (one per live edge with a listed type) — the explorer may want them off by default (chip), the door wants them always. No file under `knowledge/` other than the extractor changes; no meta, no `_rulings.json`.

**Cost:** half an Opus lane (~half a day) + the explorer chip. Build-time only; payload +≈ 40% if all inverses bake, +≈ 8% if only the door reads them from an index. **Closes:** G10, G11, G13. **Touches:** `s270-D2` (one home — kept: derived edges have no authored home), `s274-D10`, `s267-D3`, `P-269-6` (`inForce` is the query half of it; the window itself stays parked). **s274-D12:** PASS for inverse/transitive; chain inference across `cites` refused (§5).

### 4.3 SHAPES — per-type endpoint kinds and per-kind minimum connectivity in the validator, rank 3

**Plain.** Write down, once, what a node of each kind must be connected to, and have the build report every node that falls short — so "orphan" means something and the explorer's header stops printing 0.

**Technical.** A `knowledge/_kg-shapes.json`: per edge type `{src: [kinds], tgt: [kinds]}`; per kind `{min: {edgeType: n}}` (A2's §2 minimums become this file's content); `_validate_kg.py` gains check (g): shape conformance, advisory (report, exit 0), plus (h): islands/orphans on the full graph (fixes A1 §3's scope defect at source or asserts against the explorer's number). Every baked edge carries `joinClass` (STRUCTURAL/AUTHORED/PROSE — A1's classifier is by minting path, so it is a lookup) and PROSE edges are dashed in the explorer like `mentions` (G12).

**Cost:** half an Opus lane. **Closes:** G7, G8, G9 (visibility), G12; gives G2/G3/G4/G5 a number per build. **Touches:** `s131-D2`/`s133-D1` (the gate's charter — widened by addition), `s274-D9`/`s276-D6` (advisory vs blocking is Dave's; land advisory). **s274-D12:** n/a.

### 4.4 TOKENS — token nodes, `aliasOf`, `bindsToken`, rank 4

**Plain.** Put the design tokens in the graph the way the DTCG spec already models them — a token points at the token it aliases, a component points at the tokens it binds — so "what breaks if I change `text/default`" is a two-hop count instead of a 595K-token read.

**Technical.** Generator `gen_kg_tokens.py` in lane RI's shape (`--dry-run` default, `--land --ratified <id>` refuses without a ruling id): nodes `token:<path>` from `tokens/*.json` at TIER grain (semantic / component-type / foundation), primitives as leaves; edges `aliasOf` (the JSON reference chain — DTCG §7), `bindsToken` component→token (prefix parse of the meta `tokens` values; the sentence after ` — ` stays `$note`), `composite` for `typography-composites.json`; mode as an edge property. Grammar addition to `meta.schema.json` (`token:` id kind; `bindsToken` is DERIVED like `providesRole`, one home = the meta's `tokens` field). Sixth additive family `tokens`, chip default off.

**Cost:** one Opus lane, ~1 day, including 10+ selftest bites and a validator simulation as RI did. Expected ≈ 950 nodes / ≈ 3,000 edges; payload +≈ 15%. **Closes:** G1 / Q9. **Touches:** `P-269-7` (its data), `s269-D1`, `meta.schema.json`, `gen_canon_tokens.py` (read only). **s274-D12:** PASS — structural joins only.

### 4.5 NEIGHBOURS — an embedding (or shingle) neighbourhood, advisory, rank 5

**Plain.** For any node, show the ten nodes that *read* most like it, marked "unratified, semantic" — a place for Dave and a lane to find the rule→component and rule→principle bindings the graph is missing, never a place the agent takes an edge from.

**Technical.** Index over node label + attached `$note`/`$why` text; nearest-neighbour; surfaced only as a trailing section of the ASK door (`--neighbours`) and a dashed "semantic" chip in the explorer, `proposedType: null`. Dependency choice is Dave's: a small local embedding model (a new dependency the pack does not carry) or the pure-Python `_ngram.py` shingle/Jaccard already measured at #269 (`P-269-3` — this is that item widened from ruling pairs to all nodes). Output feeds a review page in the `s276-D5` shape ("flag any extra you think are applicable"), never `gen_kg_edges.py`.

**Cost:** one lane (Opus build, Fable review of the first candidate page). **Closes:** nothing structurally; candidate recall for G2, G3, G4. **Touches:** `P-269-3`, `s274-D12`, `s276-D5`. **s274-D12:** manufactures plausible links by construction — **advisory at most, exactly the ruling's shape**; refused as edges (§5).

### Not shortlisted, with the reason
- **Bi-temporal windows on edges** — parked `P-269-6`; the query half rides on 4.2.
- **PROV-O naming** — a legend paragraph, not a lane; A2 may use it for the governance-layer name.
- **Hypergraph / n-ary** — already the `ruling`/`polarity` node pattern; no build.
- **Community summaries** — `P-269-8` compile views, already parked, Dave's scope.
- **Persona / JTBD** — `P-269-9`, Dave's route choice, not an augmentation of the graph's mechanics.

---

## 5 — What I would refuse (the `s274-D12` test applied)

`s274-D12`: *"RULE → COMPONENT STAYS OUT OF WAVE 1 (the 27 regex candidates do not land); THE DURABLE ROUTE IS AUTHORED THE OTHER WAY"* — Dave: *"So A for now I guess and then D, is that correct?"* → confirmed. The test: does the augmentation put an edge in front of the agent that nobody ruled and that reads like one that was? Each refusal below is attractive and would pass a demo.

1. **LLM entity/relationship extraction over the guidelines or the rulings (GraphRAG's index stage, Graphiti's episode ingestion).** It is `s274-D12`'s 27 candidates at scale: 52 of 78 generated edges were wrong at #267; `va25-013` matched "Avatar". An LLM extractor produces more, faster, and each one wears a type. **Refuse as a minting path.** Allowed: as a *candidate* page (§4.5), dashed, never landed.
2. **LLM-written community summaries as nodes.** A summary node is prose wearing an id; it will be cited as if ratified. Compile views (`P-269-8`) are the right container: regenerated, unaddressable, read by humans.
3. **Embedding-derived edges landed in metas or `_ruling_edges.json`.** Same shape, softer name-match; `s276-D5` explicitly did not widen the name-match tier.
4. **Chain inference across a PROSE edge** — component `obeys` rule ∧ rule `cites` sc ⇒ component "appliesTo" sc. `cites` is regex (51 edges, A1 §5, presented today with structural authority — G12). An inferred obligation on a component from a regex hit is a manufactured claim about what the agent must do. Inverse and transitive closure over STRUCTURAL edges (§4.2) is the line; this is over it.
5. **A triple store / OWL reasoner / RDF-star migration.** The pack is pure Python by ruling-shaped precedent (`P-269-1` pin); the reasoning we need is two dictionaries. Reification is already done by `ruling:` nodes (§2.4).
6. **Graphiti/Zep or Mem0/Letta as the runtime memory.** LLM extraction per episode (refusal 1) plus a database dependency; and their persistence semantics are memory-shaped (decay, salience) where ours must be knowledge-shaped (supersession) [S26].
7. **Decay, salience or recency weighting on rules and rulings.** The 2026 paper's "category error" exactly: a ruling from #151 with 27 edges is not less true because it is old; it is superseded or it is in force. `inForce` (§4.2) is the only temporal signal the designer needs.
8. **Auto-resolving the 51 dangling `mustNotNeighbour` notes by name-match to a sibling** — the anaphora ("it" in a `when` clause) is A2's to judge and Dave's to ratify; a resolver would land 51 edges nobody read.
9. **Widening `appliesTo` (sc→component, 826, structural from `applies_to[]`) into `obeys`** to fix Q4's 7.3% at a stroke. `appliesTo` is the compliance corpus's own claim; `obeys` is the component's authored citation (`s276-D3`). Merging them erases the join class A1 just measured.
10. **A "just ship the whole graph in the pack and let Copilot read it" plan.** 798,152 tokens. It would be read never or read wrong.

---

## 6 — Sources read this session (2026-09-16), 33

| # | what | URL |
|---|---|---|
| S1 | Edge et al., *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*, arXiv 2404.16130 v2 (abstract page) | https://arxiv.org/abs/2404.16130 |
| S2 | Microsoft Research blog, *LazyGraphRAG: Setting a new standard for quality and cost* (25 Nov 2024, note 6 Jun 2025) | https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ |
| S3 | GraphRAG docs, Local Search | https://microsoft.github.io/graphrag/query/local_search/ |
| S4 | W3C OWL 2 Web Ontology Language Primer (Rec. 11 Dec 2012) — inverse and transitive properties | https://www.w3.org/TR/owl2-primer/ |
| S5 | Stanford KSL JTP, RDF/RDFS/OWL reasoning capabilities | http://www.ksl.stanford.edu/software/jtp/doc/owl-reasoning.html |
| S6 | Polleres, *OWL2 (in a nutshell) & OWL Reasoning* lecture (2013) | https://aic.ai.wu.ac.at/~polleres/teaching/SemWebTech_2013/20130603lecture6.pdf |
| S7 | Rasmussen et al., *Zep: A Temporal Knowledge Graph Architecture for Agent Memory*, arXiv 2501.13956 (abstract page) | https://arxiv.org/abs/2501.13956 |
| S8 | Graphiti README (getzep/graphiti, main) | https://github.com/getzep/graphiti |
| S9 | Zep, *What Is a Temporal Knowledge Graph?* | https://www.getzep.com/ai-agents/temporal-knowledge-graph/ |
| S10 | W3C WG Note, *Defining N-ary Relations on the Semantic Web* (12 Apr 2006) | https://www.w3.org/TR/swbp-n-aryRelations/ |
| S11 | Ontotext, *What Is RDF-star* | https://www.ontotext.com/knowledgehub/fundamentals/what-is-rdf-star/ |
| S12 | *HippoRAG: Neurobiologically Inspired Long-Term Memory for LLMs*, NeurIPS 2024 | https://proceedings.neurips.cc/paper_files/paper/2024/file/6ddc001d07ca4f319af96a3024f6dbd1-Paper-Conference.pdf |
| S13 | *From RAG to Memory: Non-Parametric Continual Learning for LLMs* (HippoRAG 2), arXiv 2502.14802 | https://arxiv.org/abs/2502.14802 |
| S14 | *Simple Is Effective: … SubgraphRAG*, arXiv 2410.20724 | https://arxiv.org/abs/2410.20724 |
| S15 | *Graph-based Agent Memory: Taxonomy, Techniques, and Applications*, arXiv 2602.05665 | https://arxiv.org/abs/2602.05665 |
| S16 | W3C SHACL (Rec. 20 Jul 2017) | https://www.w3.org/TR/shacl/ |
| S17 | SHACL 1.2 Core, editor's draft | https://w3c.github.io/data-shapes/shacl12-core/ |
| S18 | *xpSHACL: Explainable SHACL Validation*, arXiv 2507.08432 | https://arxiv.org/pdf/2507.08432 |
| S19 | W3C PROV-O (Rec. 30 Apr 2013) | https://www.w3.org/TR/prov-o/ |
| S20 | FAIR Cookbook, provenance information (PROV-O summary) | https://fairplus.github.io/the-fair-cookbook/content/recipes/reusability/provenance.html |
| S21 | DTCG *Design Tokens Format Module 2025.10* (draft report 08 Sep 2026; §3.8 alias, §7 references) | https://www.designtokens.org/tr/drafts/format/ |
| S22 | W3C Design Tokens CG, *Design Tokens specification reaches first stable version* (28 Oct 2025) | https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/ |
| S23 | Figma Plugin API, `VariableCollection` / `Variable` (modes, valuesByMode, scopes, alias) | https://developers.figma.com/docs/plugins/api/VariableCollection/ · https://developers.figma.com/docs/plugins/api/Variable/ |
| S24 | Figma Learn, *Create and manage variables and collections* / *Modes for variables* | https://help.figma.com/hc/en-us/articles/15145852043927-Create-and-manage-variables-and-collections |
| S25 | *Cognitive Architectures for Language Agents* (CoALA), arXiv 2309.02427 (abstract via arXiv API) | https://arxiv.org/abs/2309.02427 |
| S26 | Roynard, *The Missing Knowledge Layer in Cognitive Architectures for AI Agents*, arXiv 2604.11364 (13 Apr 2026) | https://arxiv.org/abs/2604.11364 |
| S27 | *Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering*, arXiv 2604.08224 | https://arxiv.org/abs/2604.08224 |
| S28 | *Don't Retrieve, Navigate: Distilling Enterprise Knowledge into Navigable Agent Skills* (Corpus2Skill), arXiv 2604.14572 | https://arxiv.org/abs/2604.14572 |
| S29 | Mem0 README | https://github.com/mem0ai/mem0 |
| S30 | Letta README | https://github.com/letta-ai/letta |
| S31 | Progressive disclosure in agent skills (search summary, 2026) — the ≈200-token top level | https://github.com/VoltAgent/awesome-ai-agent-papers |
| S32 | *SkillTrace: Traversing a Query–Skill Graph for Composable LLM Agents*, arXiv 2608.02356 | https://arxiv.org/html/2608.02356v1 |
| S33 | *Hindsight is 20/20: Building Agent Memory that Retains, Recalls, and Reflects* (TEMPR), arXiv 2512.12818 | https://arxiv.org/pdf/2512.12818 |

Count: 33 entries (S23 is two pages of one API reference; S1–S3 are one project). The arXiv abstracts were read via the arXiv API (`export.arxiv.org/api/query`) or the abstract page; W3C/Figma/DTCG pages were fetched and the quoted phrases grepped from the fetched text. Nothing in §2 is presented from memory as current.

Internal sources: `A1-MEASURE.md` + `A1-measure.json` (`13a4cf2`) · `_build_kg_explorer.py` · `_validate_kg.py` · `_consult.py` · `_graph_edges.py` · `_compose_slice.py` (docstring: PROPOSAL, NOT WIRED) · `_RUNBOOK-consult.md` · `designer-skills-v2/README.md` + `generate-from-canon/SKILL.md` · `_release/_gen_pack_manifest.py:515` · `_parked.json` (`P-269-1..9`, `P-274-1..3`) · `_rulings.json` (`s267-D3`, `s269-D1/D5`, `s270-D2`, `s274-D7..12`, `s275-D1/D2`, `s276-D3/D5`, `s277-D1..3`) · `_RESEARCH-ngram-lookups-2026-09-13-v1.html` · `_ngram.py` · `_quote_gate.py` · lane RI `REPORT.md` (`5520d43`) · `_GRAPH-REPORT.md` · `components/meta.schema.json`.
