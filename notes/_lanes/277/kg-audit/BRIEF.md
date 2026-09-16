# KG AUDIT — BRIEF — the whole graph, structure and efficiency, against six success criteria
#277 · 2026-09-16 · Dave's ask · written by the conductor · **pinned sha `bedf383`** · READ-ONLY, nothing enacted

## Dave's words — the purpose (verbatim, `notes/_lanes/277/DAVE-RULINGS-2026-09-16.md`)
> *"we have a lot of new nodes with very little edges connecting them some are pretty much orphaned or at least only local to their node type … a full re-audit might be a good use of the fable tokens"*
> *"the analysis needs to be deep so you can help me with the decisions, recommendations are useful so is plain prose as well as the technical prose … remember this is about creating a designer brain or memory system for the agent to make good decisions so we can create designs automatically and autonomously. remember lovable on rails, give the agent all the context a designer has access too (if they can be bothered looking at it) so we have a hyper-designer."*

**The test of every finding:** does it help an agent that has to design a screen autonomously, on rails, reach the same thing a good HSBC designer would reach — with the context that designer *could* have consulted? A gap that would never change a design decision is low. A gap that leaves the agent guessing where the designer would have known is high.

## Two lanes, in sequence
- **A1 — MEASURE (Opus, mechanical).** Produces the numbers, all of them, as JSON + a table. No judgement.
- **A2 — JUDGE (Fable, deep).** Reads A1 and the graph's sources, answers the six criteria, writes the decisions page. Plain prose AND technical prose, recommendation first on every item.

## The six success criteria (proposed by the conductor, accepted by Dave: "lets run it")
1. **A designer's question answers or declares.** A fixed set of ~12 canonical questions. Each is answered by a graph path, or declared unanswerable with the missing edge type named. The answer rate is the headline.
2. **Connectivity has an intent, per kind.** "Orphan" means something only against a stated minimum. Propose the minimum for each of the 20 kinds; measure the gap against it.
3. **Zero silent structure.** Dangling edges = 0 or declared; the explorer's orphan/island count agrees with an independent measurement; every island explained.
4. **Every edge type has a consumer or a retirement.** 51 types; name synonyms; propose merges; nothing merged.
5. **Every edge has a join class** — structural / authored / prose. Count the prose-derived tier.
6. **Output is decisions, not repairs.** Ranked gap list with cost; ≤ 6 decisions on a page; nothing enacted.

## The conductor's own measurement (2026-09-16, `bedf383`, via `_build_kg_explorer.extract()+extract_extra()`) — A1 must reproduce or correct every figure
3,897 nodes · 6,616 edges after dropping **105 edges with a `None` target** (`mustNotNeighbour`/`yieldsTo`, anaphoric `when` prose) · 51 edge types · explorer header says `islands 2 · orphans 0` while **99 `ux` nodes have degree 0**.
| kind | nodes | deg 0 | deg ≤1 | intra-kind edges | cross-kind edge-ends | cross/node |
|---|---|---|---|---|---|---|
| evidence | 886 | 0 | 818 | 0 | 1243 | 1.40 |
| artefact | 618 | 0 | 417 | 0 | 1728 | 2.80 |
| ruling | 593 | 0 | 0 | 288 | 2977 | 5.02 |
| rule | 470 | 0 | 305 | 0 | 788 | 1.68 |
| pattern | 380 | 0 | 341 | 0 | 421 | 1.11 |
| context | 222 | 0 | 176 | 0 | 367 | 1.65 |
| ux | 145 | 99 | 109 | 22 | 65 | 0.45 |
| component | 137 | 0 | 0 | 269 | 2404 | 17.55 |
| snippet | 137 | 0 | 87 | 0 | 187 | 1.36 |
| session | 92 | 0 | 47 | 0 | 199 | 2.16 |
| axe | 64 | 0 | 60 | 0 | 68 | 1.06 |
| sc | 55 | 0 | 0 | 0 | 1116 | 20.29 |
| polarity | 30 | 0 | 5 | 0 | 74 | 2.47 |
| shape | 23 | 0 | 20 | 0 | 26 | 1.13 |
| intent | 14 | 0 | 8 | 0 | 28 | 2.00 |
| guideline | 13 · role 12 · principle 4 · standard 1 · policy 1 | | | | | |
Top edge types: governs 1484 · evidencedBy 1243 · appliesTo 826 · definedIn 470 · commonPattern 421 · usedInContext 367 · mentions 240 · ruledIn 199 · obeys 168 · renderedBy 137 · under 110 · providesRole 108 …

## Read first (both lanes)
- `notes/_lanes/269/kg-gaps/A-inventory.json` + `_PROPOSAL-kg-entity-and-edge-gaps-2026-09-14-v1.html` — the last structural look (#269): 13 families at zero, 12 edge types, and what has landed since (#273 roles, #274 rules, #275 principles, #276/#277 obeys).
- `knowledge/_build_kg_explorer.py` — the extractor IS the graph definition. `knowledge/_validate_kg.py` — the grammar. `knowledge/_GRAPH-REPORT.md` if present.
- `knowledge/_rulings.json` ids `s269-D1`..`D10`, `s270-D2`, `s274-D7`..`D12`, `s275-D1`..`D6`, `s276-D3`, `s277-D1`..`D3` — what was RULED about the graph's shape; an audit that proposes undoing a ruling must say so by id.
- `knowledge/roles.json` · `knowledge/components/meta.schema.json` · `knowledge/guidelines/_rules-index.json` · `knowledge/_ux_principle_nodes.json` (or wherever #275 put the principles — find it).
- `notes/_STATE-MACHINE-TARGET.md` §7 (the compile views that were planned and never built — `P-269-8`) and `knowledge/_parked.json` (every parked graph item; do not re-propose what is parked without naming the P-id).

---
## LANE A1 — MEASURE (Opus) · output `notes/_lanes/277/kg-audit/A1-measure.json` + `A1-MEASURE.md`
Every number with the command. Pin to `bedf383` (`git stash` is banned — if the tree is dirty, measure and DECLARE the dirt).
1. **Reproduce the conductor's table** above; correct it where wrong. Add: per-kind degree histogram (0/1/2/3–5/6–20/>20), median and max degree, top-10 hubs by kind.
2. **Dangling edges**: list all 105 (source, type, note) grouped by source kind and edge type. Say which extractor line drops or keeps them and what the explorer does with a `None` target.
3. **Islands and orphans, independently**: connected components of the undirected graph (size distribution, the two "islands" named), degree-0 nodes by kind with ids. Then read the explorer's own `islands`/`orphans` computation and say WHY it prints 0 — different graph, different definition, or a defect.
4. **Edge-type census**: for each of the 51: count, source kind(s) → target kind(s), the extractor function that mints it, the source file/field it comes from, and its CONSUMERS (grep `knowledge/`, `system-manager/`, `designer-skills-v2/`, the explorer JS, `_consult*`) — a type nothing reads is a candidate for retirement (`[[instrument-without-a-consumer]]`). Flag candidate synonyms by shared endpoint kinds (e.g. `governs`/`governedBy`/`boundBy`/`enforcedBy`/`under`/`appliesTo`).
5. **Join class per edge**: classify every edge STRUCTURAL (a typed field or filename join) / AUTHORED (a human-written sentence, e.g. `obeys.$why`) / PROSE (regex or mention over free text, e.g. `mentions`) — by the extractor path that minted it. Counts per class per type.
6. **Kind × kind adjacency matrix** (20×20, edge counts) — the map of what is connected to what, and the empty cells.
7. **Reachability seeds for A2**: for each of the 12 canonical questions in A2 §1, compute mechanically whether a path exists from a sample of 10 start nodes, and the path length. Output a table A2 will read.
Gates: `_validate_kg.py` OK · `git status` shows only `notes/_lanes/277/kg-audit/A1-*`. One commit `#277 2026-09-16 — lane A1: …`, `--numstat` re-read from the shipped sha.

---
## LANE A2 — JUDGE (Fable) · output `notes/_lanes/277/kg-audit/A2-AUDIT.md` + `REVIEW-kg-audit-2026-09-16-v1.html` + screenshot
Read A1 first, then the sources. Go deep — this is the judgement Dave asked for. Every section: **plain prose first** (what it means for the hyper-designer), then **technical prose** (the evidence, ids, counts), then **recommendation** in one line.
1. **The 12 canonical questions** — define them as the questions a designer actually asks mid-task, e.g.: *what governs this component? · which components does this rule bind? · what principle underlies this rule and what is its grade? · which rules conflict for this component? · what did Dave rule about this and when? · what evidence supports that ruling? · which components can answer this intent/data shape? · what must this component not sit next to? · what tokens does this component consume and what breaks if I change one? · which pattern/context is this component used in? · what is the accessible-name / WCAG obligation here? · what icon/logo/photo may I use here?* Score each: ANSWERED (path, length), PARTIAL, UNANSWERABLE (missing edge type named). **The answer rate is the headline of the whole audit.**
2. **Per-kind intent**: for each of the 20 kinds, say what a node of that kind is FOR in the designer brain and what its minimum connectivity should be (e.g. a `rule` that binds no component is a rule the agent can never apply; an `evidence` node with one edge may be correct). Then the gap per kind against that intent, with the count.
3. **Silent structure**: the 105 dangling edges — what they mean, whether the anaphora is resolvable structurally (`yieldsTo` "it" = the sibling named in `when`?), and the explorer's false 0. Recommendation for each.
4. **Edge-type efficiency**: the synonym clusters with A1's endpoint evidence; a proposed merged vocabulary; which types have no consumer; what a 51-type vocabulary costs the agent versus a ~25-type one. Name every ruling a merge would touch.
5. **The prose tier**: what the PROSE-class edges are, how many, and whether they should stay (as advisory hints), be promoted (authored), or go — against `s274-D12`/`s276-D5`.
6. **Structure and efficiency overall**: is a star-around-components topology the right shape for a designer brain, or does it need a middle layer (family nodes, pattern hierarchies, token nodes — `P-269-*`)? What does the graph look like from the agent's seat when it has 30 seconds to decide a layout? What is missing that a designer *could* consult (Figma specs, brand book, photography, copy tone — the parked families)?
7. **Ranked gap list with cost** — each gap: what the designer would have known · what the agent currently guesses · the edge type/node kind that closes it · join class available (structural/authored/prose) · cost (nodes, edges, lanes) · rulings touched · P-ids touched.
8. **The decisions page** — ≤ 6 decisions, recommendation first, (a)/(b) options, export JSON in the shape of `notes/_lanes/277/page/charts-decisions-2026-09-15-v2.json` (copy `_build_page.py` from `notes/_lanes/277/page/` and adapt). Decisions above evidence. Bake type.css if there is a srcdoc; drive at 1280 and 390, both themes; screenshot; **look at it**.
9. **"What I would refuse"** — the attractive fixes that are the `s274-D12` shape.
Gates: nothing under `knowledge/` written · `git status` shows only `notes/_lanes/277/kg-audit/`. One commit `#277 2026-09-16 — lane A2: …`, `--numstat` re-read from the shipped sha.

## Cautions (both)
Never `git stash` · never `gen_kg_edges.py` · never `_build_all.py` · stale `.git/index.lock` → `.git/_orphan-locks/` · commit serially — an icons propose lane runs in parallel under `notes/_lanes/277/icons-propose/` · quote Dave only from `notes/_lanes/277/DAVE-RULINGS-2026-09-16.md` or `_rulings.json` `says` fields, verbatim.
