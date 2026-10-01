# #311 overnight lane D1–D3 — the edge register gets why, maker, the outside term, the fold, and five new edges

COUNTS: commits 6 (D1 ccc094fe + stamp a14eb4c5 · D2 e7e2f863, its stamps carried by 5227ccc4 · D3 a7fdf39d + the stamp commit that carries this report) · register rows 64 → 68 · graph edges 11,793, ends/shape/maker all pass, coverage OK · new edges 125 (aliasOf 35, providesCapability 4, ariaRole 84, replacedBy 2) + 2 defaultFor nulls now point at a theme · rulings stamped enacted 5 (s308-D21, D22, D23, D24, D28) · rows closed 4 (W-308ij, W-308il, W-308iq, W-308in), noted open 2 (W-308ii, W-308ip) · validator selftest 53/53 · test_gates 36/0 · WHY-MISSING 138 (advisory; lives in the metas)

Verdict: D1, D2 and D3 are built and committed. Two rows stay open for one reason each, both outside this lane's files tonight: the metas still spell the reason `$why` and carry 138 required reasons nobody has written (W-308ii), and each component's Open UI name belongs on its meta (W-308ip; the candidate map is ready).

## D1 — one reason field, one maker field (s308-D20, s308-D21)

An earlier instance of this lane had written the D1 work into the tree and stopped before committing (files dated 21:27–21:47 UTC; its script `notes/_lanes/312/D/d1/d1_register.py`). This instance read every hunk, re-ran the gates on it and committed it unchanged.

- `knowledge/_edge_register.json`: every row has `why` (required on the nine hand-made judgements s308-D20 names; served by evidence on the ten ruling-to-ruling types; not required on generated structure; obeys floor 40 kept) and `maker` (one rule per type: hand with whose and ruling, generated with the script, or ratified with the ruling; `cases` for the 12 hand logo lines, the principle sources and the subcomponent lines).
- `knowledge/_build_kg_explorer.py` 1.36 stamps `maker` on every edge and no longer writes `authored`; the template's edge card shows "made by". The 12 logo lines carry `maker: hand:Dave/s282-D5` in `knowledge/_logo_nodes.json`; `gen_kg_icons.py` keeps hand lines by maker (the old flag still honoured, selftest 24/24).
- `_validate_edges.py --check` (advisory): WHY-MISSING, WHY-SHORT, NO-MAKER, BAD-MAKER, AUTHORED-FLAG. Live: 0 edges without a maker, 0 carrying `authored`, 138 required reasons missing (mustNotNeighbour 64, yieldsTo 51, governedBy 6, groupsWith 6, composedOf 5, drivesConsumer 5, delegatesTo 1).
- Commits ccc094fe (build), a14eb4c5 (s308-D21 stamped enacted; W-308ij closed; W-308ii noted).

## D2 — the outside term and the fold (s308-D22, s308-D27, s308-D23)

- Every row has `outside`: term, vocabulary, grade (exact 9, close 36, loose 17, none 2 — flaggedBy and hasDataShape are Apollo's own), design-system vocabulary first, then SKOS, Dublin Core or PROV, as s308-D27 orders. Grades come from the research page's word map (v2 §05).
- `outside.name` is the neatest-name call per type. None of the 64 existing words is replaced: where the match is exact, Apollo's word already is the outside word or the plainer one; where it is close or loose, adopting the term would name a relation the edge does not hold. The two new words in D3 (aliasOf, replacedBy) are the outside terms, adopted.
- `$folded` maps the older decision graph's nine types: refines, supersedes, bounds as themselves; enacted-by → enacts (reversed); relates → mentions; subsumes → extends; verified-by → verifiedBy. conflicts-with and diverges-from have no match and are brought forward as proposals in `$proposed` (not rows, no edges). "depends on" is noted for later.
- `_validate_edges.py --coverage` (blocking) refuses FOLD-MISSING, FOLD-DANGLING, PROPOSED-HAS-EDGES and a row without a graded `outside`.
- Open UI names: `notes/_lanes/312/D/d2/openui-names.json`, 80 of 138 components matched to the Open UI component-name matrix (fetched 2026-10-01), each with the matrix's match share and a grade. Not written to the metas (C0's tonight).
- Commit e7e2f863. Its store writes (s308-D22 and D23 enacted, W-308il closed, W-308ip noted) were in the tree when C0 committed, and rode in 5227ccc4.

## D3 — five edges and the theme node kind (s308-D28, extending s308-D24)

- `knowledge/gen_kg_standards.py` (new) lands `knowledge/_standard_nodes.json`; the explorer reads it in pass E4 (builder 1.37).
- (a) aliasOf token → token: 35 group lines from 355 leaf aliases across the token files; the loop check runs at leaf grain and refuses to land on a cycle; one target per leaf per mode is checked.
- (b) providesCapability: 4 lines by name match only (breadcrumbs, footer, icon-button, summary); 25 capabilities are listed as unprovided, not guessed.
- (c) theme node kind: theme:<id> for the four registered themes plus theme:light and theme:dark (s230-D2 calls the mode a theme). The two logo defaultFor nulls now point at theme:dark and theme:light; `_logo_nodes.json` is unchanged.
- (d) ariaRole component → aria:<role>: 84 lines, 17 roles, from each meta's `accessibility.role` field. Four roles named after NOT or never are refused (carousel tab, cascader combobox, tags-input combobox, toast alert).
- (e) replacedBy with version: `knowledge/_replaced_by.json`, 2 ratified lines — the stat card and the KPI tile are replaced by Metric (s308-D42), in 1.0.15 (`released: false`; enacted at #309 after v1.0.14 was cut at #305). No token has been replaced by a ruling, so none is drawn.
- Register: four rows added (68), defaultFor `to` = theme; validator selftest bites 50–53.
- Commits a7fdf39d (build), and the stamp commit that carries this report (s308-D24 and s308-D28 stamped enacted; W-308iq and W-308in closed; this report).

## Gates run

`_validate_edges.py --check / --coverage / --selftest` (53/53), `_validate_kg.py` + `--selftest`, `gen_kg_icons.py --selftest`, `gen_kg_standards.py --check / --selftest`, `test_gates.py` 36/0. The seat's call wall cut the whole suite twice, so it ran in slices through `notes/_lanes/312/D/tg_slice.py` (control and preamble, then CASES in three slices).

## Found, not fixed

- The metas spell the reason `$why`, and `meta.schema.json` requires `$why` on obeys. The rename to `why` belongs to the meta owner (C0 tonight, D4 next). The explorer reads both meanwhile.
- 138 required reasons are missing on metas' mustNotNeighbour, yieldsTo, governedBy, groupsWith, composedOf, drivesConsumer and delegatesTo lines. Each is a sentence to write, not a migration.
- Each component's Open UI name goes on its meta. The input is `notes/_lanes/312/D/d2/openui-names.json`.
- `gen_kg_standards.py --check` is not wired into `knowledge/_build_all.py`. Adding steps there renumbers the survey slices the conductor runs tonight. It needs wiring beside gen_kg_tokens/gen_kg_sources, and it goes stale when a meta's accessibility.role, a token alias, a capability or a theme changes.
- The explorer page (`notes/_KG-EXPLORER.html`) is not rebuilt; that is D5's job (107 s at the seat).
- ARIA's required-context and required-owned checks against containedBy and hasPart (the reason for edge d) are not built.
- The seat's commit lock: this lane held it 00:54–01:26 UTC (two commits cut by the call wall and re-run); F2 took it as stale at 01:26, after this lane's commit had landed. While cleaning its own test copies, this lane once ran `rm -rf /tmp/gate-tests-*`, which could have removed another lane's running test_gates copy around 02:09 UTC. If a test_gates run failed then, re-run it.
- The D2 stamp commit could not finish (the call wall dropped to about 10 s around 02:15 UTC). The lock was released; another lane's commit carried the stamps.

## Ruling-shaped questions

None. Every item was already his click.
