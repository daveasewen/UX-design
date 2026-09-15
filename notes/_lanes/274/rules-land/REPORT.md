# Lane RL — s274-D7..D12 ENACTED: the 470 guideline rules landed in the graph (#274, 2026-09-15)

Lane RK proposed; this lane landed. `_rulings.json`, `_rules-index.json`, every `*.meta.json`,
`meta.schema.json` and `gen_kg_rules.py` are UNTOUCHED.

## 1. What landed — `knowledge/_rule_nodes.json` (new file, 521 nodes / 634 edges)

```
python3 knowledge/gen_kg_rules.py --selftest          -> SELFTEST PASS (12 bites) — run BEFORE anything
python3 knowledge/gen_kg_rules.py --land --ratified s274-D8
-> LANDED — ratified s274-D8 · knowledge/_rule_nodes.json · 521 nodes · 634 edges
   {'definedIn': 470, 'cites': 51, 'enforcedBy': 63, 'flaggedBy': 50}
```

Confirmed against the rulings: **D7** 470 `rule:` nodes (+51 `artefact:`), each with
id/file/destiny/destinyFull/text · **D8** only those four types, 0 others · **D9** `destiny`/`destinyFull`
as attributes, 0 `destiny:` hubs and 0 `hasDestiny` edges · **D10** 19 edges
`{"t": null, "note": "cites SC x.y.z — no sc:x.y.z node in knowledge/compliance/rules/"}` · **D12** 0
`appliesTo` edges.

**Against `dry-run.json`: identical** — 521 nodes, 634 edges, same per-type counts. The dry run's
`unresolved` list holds 23 (19 `cites` + 4 `flaggedBy` on `*.canon.html` pages); the landed file carries the
19 as null-target edges and REFUSES the 4 (they are not snippet nodes) — 19 nulls, matching bite 6.

17 distinct criteria are missing (19 citations): 1.2.3 · 1.2.4 · 1.3.3 · 1.4.2 · 1.4.5 · 1.4.8 · 2.4.13 ·
2.5.1 · 2.5.2 · 2.5.3 · 3.1.1 · 3.1.2 · 3.1.4 · 3.2.2 · 3.2.4 · 3.3.7 · 3.3.8 -> parked as **P-274-2**.

## 2. The reader (D11 — same commit, so no unread file ever exists)

`knowledge/_build_kg_explorer.py` (29,643 B -> 30,846 B), four spans + two one-line changes:

- `rule_nodes()` — reads `_rule_nodes.json`, the shape of the `ruling_edges()` reader it sits beside.
- `extract_extra()` **section C** — adds the nodes, then the edges, skipping a node another family
  already owns and carrying a `t: null` edge rather than dropping it.
- the end-filter `edges = [e for e in edges if e['s'] in known and e['t'] in known]` became
  `... and (e['t'] is None or e['t'] in known)` — **without this the 19 declared nulls are silently dropped**
  and D10 is unenacted on the page. One clause, commented `# s274-D10`.
- `place_extra()` lays the family out at `cx = 2.2` (its own parking spot; no base position moves).
- `VERSION` 1.10 -> **1.11**; one report line prints the family's counts.

`knowledge/_kg_explorer.template.html` (46,985 B -> 47,928 B), 8 spans: `--c-rule` + `--f-guidelinerules`
in the light block and both dark blocks; `'rule'` into `TYPES2`; the four types into `FAMILY`;
`FAMLABEL`/`NEWFAM`/`famOn` (**loads OFF**, like the other two additive families); the four `READ` label
pairs (`READ[t]` is indexed unguarded when a relation group renders — without them the panel throws).

**Reconstruction proof**: removing every inserted span returned the original bytes —
`_build_kg_explorer.py True 29643 29643` · `_kg_explorer.template.html True 46985 46985` · `_parked.json`
likewise. No JSON file was re-dumped; every JSON edit is a textual span.

WARNING — **the family key is `guidelinerules`, not `rules`**: `rules` is taken by the base "Rules &
wiring" chip, which loads ON; keying it `rules` would have merged 634 edges into that chip and put 508
nodes on screen at first paint. The chip reads **"Guideline rules"**; colour is one deep green
(`#2E6B1F` / `#8FD67A` dark) for node type and family — not a red, TWO-RED LAW (s151-D1) untouched.

**No schema span was needed.** `_validate_kg.py` loads its closed edge vocabulary from
`meta.schema.json -> edges.properties` and checks COMPONENT METAS only (RK section 1) — rules are not
components and `_rule_nodes.json` is not a meta. Nothing else asserts a closed vocabulary over this file.

## 3. Driven in chromium (`source knowledge/_render/seat_env.sh`, playwright, `goto("file://...")`)

```
FAMILY CHIPS: ['Structure144','Usage788','Rendering137','Rules & wiring198',
               'Governance3118','Guidelines1052','Guideline rules634']
stats (as loaded):     939 nodes · 1,474 relations · 16 edge types · 137 components · 109 declared, unresolved
stats (rules chip on): 1447 nodes · 2,009 relations · 20 edge types · 137 components · 109 unresolved
KG totals: nodes 3680 · edges 6316 · rule nodes 470 · definedIn 470 / cites 51 / enforcedBy 63 / flaggedBy 50 · nulls 19
search "aca-001" -> rule · aca-001 · panel shows rule:aca-001 + the rule text + 2 relations
CONSOLE ERRORS/WARNINGS: none (0)
```

With all three additive chips on, `aca-007` renders its groups and its null, verbatim from the panel:
`definedIn — is defined in — knowledge/guidelines/accessibility-content-authoring.md` ·
`enforcedBy — is enforced by — knowledge/_validate_advisory.py` ·
`declared, unresolved — cites SC 1.3.3 — no sc:1.3.3 node in knowledge/compliance/rules/`. 0 errors.

Screenshots, both reviewed by eye: `notes/_lanes/274/rules-land/explorer.png` (rules chip alone, aca-001)
· `explorer-all-layers.png` (all three chips, aca-007).

**Finding, declared:** with the rules chip on ALONE, 99 of the 634 edges do not draw — 38 `definedIn` +
29 `enforcedBy` point at `artefact:` nodes governance owns, 32 `cites` at `sc:` nodes guidelines owns; an
edge draws only when BOTH ends' families are on. The existing family model, not a defect introduced here.

## 4. Gates (verbatim)

```
### _validate_kg.py
metas checked: 139
ref:null + $note (declared, awaiting Dave's-eye migration): 90
resolutions consumed (s135-D4, KG-REVIEW-VERDICTS-2026-08-08-s135-v1.json): 82 ruled verdicts asserted present (MERGE 5 / PROMOTE 52 / ATTACH 25)

_validate_kg.py: OK — every ref parses+resolves, every null carries a note, every meta has provenance, edges match schema, gen_kg_edges.py is idempotent-clean, and the s135-D4 resolutions input was consumed.

### gen_kg_rules.py --selftest
  ok    bite 12: edge_status marks appliesTo EXISTS and the other four NEW
SELFTEST PASS

### _validate_compose.py   (real 0m0.269s)
RESULT: PASS

### _parked.py --check
PARKED DUE — 2 of 18 parked item(s) due     (P-274-2 and P-274-3 both listed)
```

`_build_kg_explorer.py` -> `notes/_KG-EXPLORER.html` · v1.11 · 3680 nodes · 6316 edges ·
`rules family: 508 new nodes / 615 edges + 19 declared nulls` (508 not 521: 13 `artefact:` nodes already
existed in the governance family and were joined, not restated; 0 skipped).

## 5. Ruling-shaped, met and NOT decided

1. **The chip key and label.** `rules` was taken; I used `guidelinerules` / "Guideline rules" to keep the
   base chip's count and first-paint behaviour honest. If Dave wants a different word on the chip it is one
   span in the template.
2. **A rule's edges are invisible unless Governance and Guidelines are also on** (99 of 634). Both
   alternatives (auto-switching the needed layers; the rules family claiming shared nodes) change the
   family model, so neither was taken.
3. **`$description` in `_rule_nodes.json` still reads "PROPOSED ... NOT RATIFIED"** while the file carries
   `"ratified": "s274-D8"` — generator text; fixing it means editing `gen_kg_rules.py`, fenced from this
   lane. One line, whenever the generator is next opened.

## 6. Not done

- Did not edit `gen_kg_rules.py`, `_rulings.json`, `_rules-index.json`, any meta, `meta.schema.json`; did
  not run `gen_kg_edges.py` / `_build_all.py`; did not stash/checkout/reset.
- Did not add the new types to any schema — measured as unnecessary (section 2), not assumed.
- Did not stage the pre-existing dirty files (`_REHEARSAL-LOG.jsonl`, `_dream/_GRADE-DECISIONS.jsonl`);
  `knowledge/_gen_titles_receipt.json` was not dirty.
