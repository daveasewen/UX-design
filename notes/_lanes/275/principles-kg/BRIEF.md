# LANE RP — BRIEF — the 145 UX principles + the 22 polarity edges into the knowledge graph
#275 · 2026-09-15 · s269-D1 STEP 3 · written by the conductor · model: opus

## The job in one line
Mirror lane RK (#274) exactly: a generator that PROPOSES `ux:` principle nodes and their edges, a dry-run,
a selftest, a review page of ≤ 6 decisions for Dave — and NOTHING landed. Dave ratifies; a later land lane (RL shape) lands.

## Read first, in this order (all read-only)
1. `notes/_lanes/274/rules-kg/REPORT.md` — the shape of your report and the "two vocabularies, not one list" finding.
2. `knowledge/gen_kg_rules.py` — the generator to mirror (CLI contract, refusal on `--land`, `ref: null` + `$note`, selftest bites).
3. `notes/_lanes/274/rules-kg/_build_page.py`, `rules-kg-decisions-2026-09-15.json`, `REVIEW-rules-into-graph-2026-09-15-v1.html` — the review page to mirror, including its EXPORT control and format (Dave exports his a/b/null + notes; the read-back in chat is where a sentence becomes a plan).
4. `notes/_lanes/269/kg-gaps/A-inventory.json` — the entries for the principles family and "brain — polarities and polarity edges" (candidate node kind, candidate edge kinds, measured counts).
5. `knowledge/brain/principles.json` (145 · grades A6 B28 C75 D9 L27 · 31 families) · `knowledge/brain/polarities.json` (30) · `knowledge/brain/_generated/polarity-edges.json` (22 edges / 18 polarities with edges / 12 without / 17 parties not edgeable) · `knowledge/brain/schema/polarity.schema.json` · `knowledge/brain/stubs.json` · `knowledge/brain/polarity-status.json`.
6. In `knowledge/_rulings.json`: s269-D1..D6 (the order, the `ux:` prefix, "tokens at tier grain", "hub that carries nothing earns no edge" via s274-D9) and s274-D7..D12 (the rules precedent: node kind, four edge types, destiny = attribute, nulls declared not dropped, reader in the same commit, rule→component authored the other way).

## Deliverables (all under `notes/_lanes/275/principles-kg/` unless named otherwise)
1. **`knowledge/gen_kg_principles.py`** — node kind `ux:<id>` (s269-D2, e.g. `ux:pr-fitts`). PROVE the prefix is free by MEASURING the live node kinds the way RK did (read `notes/_KG-EXPLORER.html` / `_build_kg_explorer.py`), not by assuming. Attributes: id · statement · family · originator · year · grade · grade_alt · grade_reason · evidence · scope_conditions · known_misreadings · refutation_probe (statement text is the register lane's own words — carry it as-is).
   Edges FROM EXISTING DATA ONLY — measure each, count resolved vs `ref: null`:
   - `tensionWith` ux → ux from `polarity-edges.json` (22), carrying polarity id + mediating_variable as edge attributes. NEW edge type ⇒ a decision.
   - polarity `links` (e.g. `{type:"explainedBy", ref:"s151-D1"}`) → `ruling:<id>` or whatever kind the ref resolves to. Enumerate every link `type` in `polarities.json`; each distinct type is a candidate edge type; measure resolution against the live graph.
   - `family` and `grade`: ATTRIBUTES by default (the s274-D9 precedent). Offer `--family-edges` (family hubs, for a picture on demand) behind a flag exactly like `--destiny-edges`, OFF, counted, not recommended unless you can show a hub that carries something.
   - Principles in the WCAG-adjacent families (fam-wcag22 11 · fam-coga 6 · fam-aria-apg 1 · fam-en301549 1 · fam-eaa 1): link to an existing `principle:` / `guideline:` / `sc:` node ONLY where a field in the data names it explicitly. NEVER by regex or name-matching on statement text — s274-D12 refused 27 regex candidates. If no explicit field exists, say so with the count, and make it a decision (candidate: "authored, not generated").
   - s269-D5 (component metas cite the six A-grade laws: pr-fitts · pr-hick · pr-steering · pr-klm · pr-speed-accuracy · pr-graphical-perception) is AUTHORED THE OTHER WAY (s274-D12 shape) — NOT this generator. Measure only: does any `knowledge/components/*.meta.json` already name a `pr-` id or one of those six law names verbatim? Report the count (0 is a fine answer). Make it a decision: which lane and when.
   - Polarities as NODES vs no node at all (A-inventory's own either/or): a decision, with the 12 edgeless polarities and 17 non-edgeable parties DECLARED as `ref: null` + `$note` naming the party text.
2. **`--dry-run` is the default** → writes `dry-run.json` in this folder and nothing else. **`--land` REFUSES** unless `--ratified sNNN-DN` names a ruling that exists in `knowledge/_rulings.json` (mutation-tested). Lands to `knowledge/_ux_principle_nodes.json` in the `knowledge/_rule_nodes.json` shape. On land, `$description` must NAME the ratifying ruling (the #275 fence, commit `ef1213b`) — never the dry-run's "PROPOSED … NOT RATIFIED" text. ⚠ `gen_kg_rules.py`'s "NO CONSUMER YET" warning is now STALE (explorer v1.11 reads `_rule_nodes.json`): do not copy that pattern — grep `_build_kg_explorer.py` at runtime for your landed filename and print the measured answer.
3. **`--selftest`** with ≥ 10 bites; list in the report every mutant you drove and the exact CLAUSE each one proves (a mutation test proves the clause, not the feature).
4. **Review page** `REVIEW-principles-into-graph-2026-09-15-v1.html`, built by `_build_page.py` from `principles-kg-decisions-2026-09-15.json`: ≤ 6 decisions RP-1..RP-6, options a/b/(c), YOUR RECOMMENDATION FIRST with a one-line why, the option that carries weight marked, export control identical to RK's. Swiss design system (`/swiss-design-system` skill); bake `type.css` per the label-crop pattern; render in chromium (`source knowledge/_render/seat_env.sh`) → `screenshot.png` in this folder, 0 console errors. Nothing on the page in ALL-CAPS names (nam-002).
5. **`REPORT.md`** in RK's shape: central finding (existing vs new, two vocabularies), every count with the command that produced it, decisions with recommendations, gates run (`_validate_kg.py`, selftest, `_validate_compose.py` if anything you touch is composed — it is not), mutants caught.

## Fences (⛔)
- READ-ONLY on the corpus: never edit any `*.meta.json`, `principles.json`, `polarities.json`, `meta.schema.json`, `_rulings.json`, `_build_kg_explorer.py`, `_rules-index.json`. Never add a principle. Never land.
- NEVER INVENT a node or an edge target: an unresolvable target is `{"ref": null, "$note": "<the evidence>"}` and is counted in `unresolved`.
- Never run `gen_kg_edges.py`. Never `git stash`. Never `git checkout` a path.
- Any sentence you present as Dave's must pass `python3 knowledge/_quote_gate.py "<words>"`; its index covers neither `notes/_lanes/` nor `says`, so on 0 verify against the source file and say which.
- ONE commit of your own files at the end, message beginning `#275 2026-09-15 — lane RP:`. If `.git/index.lock` exists, STOP and report it — do not delete or move it.
- Textual span edits only if you must touch any shared file (you should not need to).

## Report back to the conductor (≤ 400 words)
Counts (nodes · edges by type · unresolved) · the decisions RP-1..N one line each with your recommendation · gates and their exact results · mutants caught · commit hash · anything you could not do and the first obstacle.
