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


## Round 2 — items 3 and 4 (s308-D18, s308-D19, s308-D26), 2026-09-29 afternoon

COUNTS (round 2): register rows 65 (64 stored types + hasPart, now read-only) · edges checked 11,499 · ends pass 11,499 · shape advisories 21 (READ-SIDE-STORED 18: governedBy 10, ruledBy 8 · SELF-LINE 1 · LOOP 1 · BOTH-WAYS-STORED 1) · coverage refusals 0 · self-lines moved 20 of 22 · selftest 24 of 24 bites

Asked: the conductor, 14:44 BST, relaying Dave's rulings s308-D18 (item 3), s308-D19 (item 4, v1) and s308-D26 (item 4, v2: "The 4 part-names become a subcomponent kind"), under D27's neatest-name note.

**The rule for the stored side.** Dave named both pairs he was shown: governs over governedBy, containedBy over hasPart. The same rule decides any other pair: store the side written on the record that makes the claim (the ruling for governance, the contained part for containment), and read the other by walking backwards. The rule is recorded on each row as `opposite.basis`.

**The agreement check, run before the switch** (`notes/_lanes/308/E/agreement-before-switch-2026-09-29.json`):
- governedBy: 28 lines. 18 were mirrored by governs, and 10 stood alone.
- containedBy/hasPart: 0 of 102 mirrored. That is containedBy 88 and hasPart→component 14, with 22 hasPart lines in all.
- ruledBy: all 8 are mirrored by a governs line to the icon's .svg.
- alert and toast carry the one both-ways mustNotNeighbour pair.
- triggeredBy and delegatesTo: 0 of 3 mirrored. They are not opposites. delegatesTo is a hand-off contract with `when` (s268-D5), and triggeredBy is a prose trigger.

**What moved, at the source:**
- **gen_kg_edges.py:**
  - hasPart is RETIRED. A part that a ruled PROMOTE names as another component is now a `containedBy` line on that component, with a `part` field. There are 10 such lines.
  - An s135-D4 ATTACH row is written as governedBy only when the ruling's own `governs[]` does not already carry it. That drops 18 lines and keeps 10.
  - A self-line whose fact is now a field is folded away. `count` takes 5 mustNotNeighbour lines and 2 groupsWith lines, and `covers` takes 9 family lines.
  - The generator is two-pass and idempotent. It reads `_rulings.json`, and refuses loudly if that file is missing.
- **Subcomponents (s308-D26):** the 12 part names with no component of their own are `subcomponent:<component>/<part>` nodes, with canStandAlone false. The explorer and `_compose_slice.py` derive them from the container's own `subComponents`, so nothing is stored twice.
- **Metas:** 17 metas gained `count` or `covers` by text splice. kpi-tile's and stat-card's groupsWith self-lines moved into `count`, with their s245-D7 notes verbatim. meta.schema.json gains `count`, `covers` and the edge's `part`, and drops `edges.hasPart`.
- **Readers:**
  - The explorer is now 1.33. It reads each type's two readings from the register (the `read` block), and adds a `subcomponent` type chip.
  - `_kg_verbs.json` drops hasPart from `contains`.
  - `_compose_slice.py` reads a component's parts through containedBy walked backwards. For example, data-grid needs button, pagination, search-field and selection-controls.
  - `_validate_kg.py` (f) now checks that every ATTACH row is stored exactly once, and that hasPart PROMOTEs land as part lines. It also mirrors `_rulings.json` into the scratch copy it regenerates from. Three planted mutants went red.
- **Register:**
  - `opposite` is now {type, stored, basis, agreement}, and `reads` is {forward, back}.
  - `shape` is {self, loops, bothWays, chains, basis, measured} on all 65 rows. No type may point at itself. containedBy, under, supersedes and composedOf chain. groupsWith, family, tensionWith and mustNotNeighbour are symmetric and stored once. Order-like types may not loop.
  - The "owed to item 3/4" markers are gone.
- **_validate_edges.py:**
  - `--check` adds SELF-LINE, LOOP (Tarjan, once per cycle), BOTH-WAYS-STORED and READ-SIDE-STORED, all advisory.
  - `--coverage` requires the new fields, and spares a read-only row that has no edges.
  - Selftest arms 17–24 plant each shape class and go red.

**Left for Dave: `notes/_REVIEW-308-edge-questions-2026-09-29-v1.html`**, five calls, each with a recommendation:
1. carousel↔cards, drawn side by side. A is recommended: a carousel holds cards.
2. The 10 governedBy lines that no ruling lists. Keep six (Badge, Tabs, Banner ×2, Button, Selection controls) by adding each to its ruling's list. Drop four: Banner←s125-D1 is a word match on "chain banner", and Legend ×3 are not named.
3. Retire ruledBy, a second copy of s264-D3's list, from the icon generator's ratified six.
4. Point tab-bar's self-line at Tabs.
5. Keep Alert's line and drop Toast's.

The page was rendered at 1440 and 390 and checked by eye.

**Calls made:**
- I did not move the 10 governedBy lines, the 8 ruledBy lines, tab-bar's line or Toast's line. Each needs a record changed that only Dave can rule on.
- All 22 part names became something. The 4 self-lines and the 8 nulls became subcomponents, because hasPart is no longer stored and D26 names the subcomponent kind as the home for part names. The 10 that are real components became containedBy part lines.
- A first cut stored subcomponents in a new registry file and read the ATTACH rows from `reviews/`. That broke the designer pack's reader boundary (compose bites 65, 66 and 68), so it was replaced by the design above. The stray registry file was moved to `outputs/308/E/_to_delete/` (ignored), because deleting is off.

**Verification:**
- `_validate_kg` passes, including the regeneration check.
- `_validate_edges --coverage` is OK, and `--selftest` passes 24 of 24.
- Survey 164–166: selftest pass, check ADVISORY-warn (the 21 above), coverage not asked, and OK when run directly. Survey 85: pass.
- `_compose_slice --selftest`: 6 of 79 red, the same six as before round 2.
- Explorer 1.33 loads with no page errors and shows 12 subcomponent nodes.
- The regen serial: the memento index and graph mention map were rebuilt, and everything else was fresh. _gen_titles refuses until the wrap, as expected.
- The verdict log was restored from HEAD after the surveys.

**Rows:** W-308ig is closed against this commit. W-308io stays open until Dave rules on carousel↔cards. W-308e2 is the page, born closed. W-308e3 is live, owned by Dave: rule the edge questions.
