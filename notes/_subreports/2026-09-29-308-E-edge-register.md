# #308 lane E — the edge register and the ends check (items 1 and 2)

COUNTS: types registered 65 · edges checked 11,472 · pass 11,460 → 11,472 · fail 12 → 0 (before the move: WRONG-FROM 12, WRONG-TO 12, all governedBy logo→rule; every other class 0) · coverage refusals 0 · logo lines moved 12 of 12 · selftest 13 of 13 bites

Asked: Dave, chat #308, 09:26 BST, verbatim: '1. Write one edge register — Take it' (s308-D16) and '2. Check every edge’s two ends against its row — Take it' (s308-D17). His words: notes/_lanes/308/DAVE-RULINGS-2026-09-29-0926-edge-definitions.md. The page he answered: notes/_RESEARCH-308-design-system-ontologies-2026-09-29-v1.html.
Build commit: a7742aee.

## What exists now

1. **knowledge/_edge_register.json** — the one home. 65 rows, one per edge type in the graph the explorer builds (knowledge/_build_kg_explorer.py extract() + extract_extra(), 11,472 edges, 5,943 nodes, measured 2026-09-29 ~08:45Z). Each row has v1 item 1's fields: word, plain, verb, from, to (plus `pairs` where from × to would admit a wrong mix: obeys, under, evidencedBy), nulls, opposite, shape, count, reason, maker, outside, and family and $measured. The `$schema` block says what each field means and which ones the check reads. Every row names where its edges are made: authored by hand (in which file), generated (by which script), or ratified (by whose verdicts).
2. **knowledge/_validate_edges.py** — reads the register and the graph, never writes.
   - `--check` (ADVISORY, build step 164): UNKNOWN-TYPE, WRONG-FROM, WRONG-TO, WRONG-PAIR, NULL-NOT-ALLOWED, OVER-COUNT. It prints the COUNTS line first, then every failure by name. Measured drift in a row's tallies is printed, never failed.
   - `--coverage` (BLOCKING, build step 165): NO-ROW, ROW-WITHOUT-EDGES, UNREGISTERED-NAME (a type named by meta.schema.json, _kg_verbs.json or the template's FAMILY map with no row and no `$absent` entry), ABSENT-HAS-EDGES, REGISTER-SHAPE.
   - `--selftest` (ABORT, build step 166): a control arm on the real graph (every edge classified once, a second run agrees), then one planted red per refusal class, each required to go up by exactly one. 13 bites, all green. A mutant of the checker with WRONG-FROM switched off turned bite 2 red, so the arms are live.
   - If numpy is absent (CI installs only tiktoken and jsonschema), numpy is stubbed: extract() never uses it. This was proved by running --check and --selftest with numpy blocked. If the explorer cannot be imported at all, the check refuses with exit 77 and a COULD-NOT-ASK line.
3. **The move** (s308-D17): the 12 logo→rule lines in knowledge/_logo_nodes.json change type from governedBy to obeys. Their ends, `why`, `ruling` and `authored: "hand"` marker are unchanged, and a `$s308-D17` block records the move. The generator (notes/_lanes/277/icons-propose/gen_kg_icons.py) now declares its unbound-lockup null under obeys, so a regenerate still suppresses it by (source, type), as before. Its selftest stays at 24 bites, all green. Explorer 1.31 draws obeys in the assets family instead of governedBy and carries each logo line's `why`. The explorer was rebuilt and the schematic regenerated. _CHAIN.md was also regenerated, because the commit gate named it stale.

## The baseline (first real run)

- Before the move, 11,472 edges were checked: 11,460 passed and 12 failed. The 12 are the logo governedBy lines, each both WRONG-FROM (starts on a logo; the row allows component) and WRONG-TO (ends on a rule; the row allows ruling). The full list is in outputs/308/E/baseline-premove.txt.
- After the move, 11,472 of 11,472 pass. Coverage is 65 rows for 65 types, with 1 declared absent (`overrides`: a FAMILY key and a mention-verb stem with no edge anywhere) and 0 refusals.
- OVER-COUNT is 0. Counts are declared only where a definition says one: renderedBy, ruledIn, under, enClause, boundBy, definedIn, inFamily, inGroup. The check counts distinct targets, so the 42 repeated `under` pairs do not trip it (those repeats are item 4's).

Measured for items 3–6, recorded in each row's `today`, not checked:
- **Opposites (item 3):** governedBy has 18 of 28 lines mirrored by governs. hasPart has 0 of 10 component→component lines (self-lines excluded) mirrored by containedBy. yieldsTo's inverse is read by traversal and never stored. triggeredBy↔delegatesTo and ruledBy↔governs are lane O's candidate pairings, not ruled.
- **Shape (item 4):** self-lines are family 9, mustNotNeighbour 7, hasPart 4 and groupsWith 2. Two-step loops are containedBy 1, mustNotNeighbour 1, mentions 2 and yieldsTo 7. Repeated pairs are under 42, governs 14 and hasPart 4.
- **Reason (item 5):** on the graph edge, obeys carries one on 180 of 180 lines and restsOn on 75 of 75. The ten ruling→ruling types carry `evidence` in storage on every line. Only the metas' obeys `$why` is required (40-character floor, meta.schema.json).
- **Maker (item 6):** the `authored` flag is absent on 1,648 edges and "True" on the generated bindsToken, as lane O measured. Each row names its maker plainly.

## Owed to items 3–9 (not started)

- Item 3 (s308-D18): `opposite.declared` in every row, and which side is stored.
- Item 4 (s308-D19): `shape.declared`, and the 22 self-lines moved to the fields they mean.
- Item 5 (s308-D20): one field, `why`, required by type. The logo lines already use `why`; the metas use `$why`.
- Item 6 (s308-D21): one maker field on every edge.
- Item 7 (s308-D22): choose and grade the outside terms. `outside.candidates` holds lane O's v2 terms, ungraded. v2's changes to items 4, 7 and 9 are not ruled and were not used beyond that.
- Item 8 (s308-D23): the ten ruling→ruling rows carry `owedAlso`. _decision-graph.json's nine types have no rows because they are not graph edges.
- Item 9 (s308-D24): no rows until those edges exist. defaultFor and acceptsCapability carry notes pointing at 9c and 9b.
- The rest of item 1 (row W-308ie): the meta schema, the verbs map and the explorer still hold their own partial copies. Making them read the register is not done here. Until then, --coverage refuses any type one of them names that the register lacks.

## Calls I made

1. **Coverage is BLOCKING.** It was born with zero backlog. It is the one thing that keeps "defined once" true: inFamily entered with no verb because nothing checked this. Its remedy is always one row, written by the lane that adds the type. The ends check stays ADVISORY, as Dave's "advisory first" says.
2. **`from` and `to` are the definitions, not only today's measurements.** They agree with today's measurements for 64 types. For governedBy the row says component→ruling, as s308-D17 rules. `governs` also allows `snippet`, because gov_target() in the builder can emit one (0 today).
3. **I changed the ratified generator at the null route.** Without that, the next `gen_kg_icons.py --land` would re-declare 6 logo governedBy nulls beside the moved lines, since the merge keys on (source, type). The move would not have held.
4. **`--coverage` is not a --check or --selftest argument, so _build_survey.py lists it as "not asked".** I ran it directly: OK, exit 0. The build and CI run it.
5. **No `$why` was invented.** The 12 logo lines already carried a `why` of 150+ characters from s282-D5, so part (c) did not need to stop.

## Things Dave should see

- **14 of Dave's defaultActive answers never reach the graph.** _icon_nodes.json holds 15 defaultActive edges; the explorer draws 1, a declared null. Its asset pass skips any type not in ASSET_DRAWN, and defaultActive is not in it. These are the answers he gave at #280, which gen_kg_icons.py reproduces. The skip is counted in the builder (asset_edges_skipped 14) and printed nowhere. It is noted on the register's defaultActive row. Fixing it is not in this slice.
- _compose_slice.py --selftest (not a build step) shows 6 of 79 bites red: logos.md scope, ruleFacets overrides, the inFamily verb gap and a rests-on $source. None of them reads the moved lines.

## Verification (bounded)

- Survey steps 164–166: 2 pass. Step 165 is not asked (its argument is not --check or --selftest); run directly, it is OK.
- Survey steps 84–85: step 85, the _validate_kg selftest, passes. Step 84 has no arguments, so the survey does not ask it; run directly, `_validate_kg.py: OK`, exit 0.
- `_wrap_regen.py --checks-only --session 308`: only the schematic was stale, and it was regenerated. _gen_titles refuses until the wrap, as expected.
- The two surveys appended lines to notes/_BUILD-VERDICT-LOG.jsonl. I did not commit that file; it is shared.
