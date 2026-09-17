# LANE OC — BRIEF — the ORPHAN CENSUS: which nodes have no wiring, by family and by cause, and what each cause costs to fix. MEASURE, do not wire.
#280 · 2026-09-17 · conductor (Fable 5.1) · **model: opus** · bash root `/sessions/intelligent-serene-curie/mnt/UX-design/`

## Dave's words, verbatim, on a screenshot of the UX (pink) family in explorer 1.18 — a cloud of dots with almost no lines
*"do we have a plan to wire up the orphans etc?"* The honest answer today is: pieces, not a plan. This lane turns the pieces into one page he can rule from.

## Read first (retrieval)
`_HANDOFF-130-the-wave-lands-and-the-graph-question.md` (the wave: scope `s277-D9` took rules reaching a component 107 → 408 of 470; verbs `s277-D11` 36 of 58 edge types; icons `s277-D4..D7` 32 declared nulls; `s277-D12` tokens NOT STARTED) · `notes/_subreports/2026-09-16-279-SC-scope.md` and `-VB-verbs.md` §9 (the open questions) · `s276-D3` and `s277-D8` in `knowledge/_rulings.json` (the 14 obeys→ux edges; force is the edge's not the node's) · `knowledge/_validate_kg.py` (declared nulls vocabulary). Data: the embedded KG in `notes/_KG-EXPLORER.html` or the node/edge files under `knowledge/` it is built from (`_build_kg_explorer.py` names them).

## Measure
1. **Degree-zero census** at three chip settings (page defaults · every chip on · every chip on + Constitution): per family and per node type, count nodes with zero drawn edges, and nodes whose ONLY edges are declared nulls. Report the full table; name the ten largest orphan sets.
2. **Cause per set** — for each orphan set say WHY, from the data, one of: (a) no edge type exists yet for this relation (the 13th-verb class, `usesIcon`/`usesLogo`); (b) the edge type exists but the source never emitted it (generator gap — name the generator); (c) the relation is real but has no declared home in the schema (a ruling is owed); (d) the node is a true leaf by design (say so — not every dot needs a line). The pink UX cloud in his screenshot is the first case to explain: 145 UX nodes, which of them have edges, from what, and what would wire the rest (the polarities → principles → components chain of `s276-D3`).
3. **Cost per cause**, in the record's units: a lane (hours of one Opus sub), a ruling (Dave's word, one question), or both. No numbers typed that the data can compute.

## The page — `notes/_lanes/280/orphan-census/ORPHANS-2026-09-17.html`, swiss-design-system idiom (`/sessions/intelligent-serene-curie/mnt/.claude/skills/swiss-design-system/SKILL.md`), single file
Plain prose for Dave. Top: one sentence with the headline count. Then the table (family × setting), then one block per orphan set: what it is, why it is orphaned, what wires it, what it costs, and ONE radio per block: (a) wire it — cut the lane · (b) it is a leaf by design — declare and stop counting it · (c) needs a ruling first — put the question. Export button, envelope `{exportedAt, page, answers:{<set>:{choice, note}}}`. No ruling ids in body copy.

## Gates
Nothing outside `notes/_lanes/280/orphan-census/` changes except `_state.json` (row `W-280oc`, close = Dave's export) and `_CHAIN.md` if regenerated. Page errors `[]` never-driven; 1280 light screenshot via `knowledge/_render/seat_env.sh`. `/sessions` at 99%: download NOTHING, never copy `knowledge/`, scratch under `/sessions/intelligent-serene-curie/mnt/outputs/oc/`, removed at the end. Never `git stash` / `gen_kg_edges.py` / `_build_all.py`.

## Report — `notes/_lanes/280/orphan-census/REPORT.md` + `notes/_subreports/2026-09-17-280-OC-orphan-census.md`. Plain prose first: the headline, the ten sets in one line each with cause and cost.
Commit via `SESSION_N=280 SHOWROOM_ACK=1 bash knowledge/_git_commit.sh --reconciled <fresh msgfile> <paths…> < /dev/null`, msgfile `/tmp/_msg-280-OC-$(date +%s).txt`, bare subject `#280 lane OC: the orphan census — N degree-zero nodes in M sets, each with its cause and its price`. Do not push. Return: page path, sha, the headline and the ten one-liners.
