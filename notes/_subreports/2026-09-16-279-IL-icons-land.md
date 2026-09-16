# LANE IL — REPORT — the icons landed: A3/A4 pre-land fixes, the door opened, `--land --ratified s277-D4`

#279 · 2026-09-16 · enacting `s277-D4..D7` · LAND lane, opus seat. Everything below was RUN, not recalled.

**Result: LANDED.** `knowledge/_icon_nodes.json` + `knowledge/_logo_nodes.json` — 688 nodes, 1,299 edges,
32 declared nulls, 0 `themedBy`, 0 `defaultActive`. Selftest 18/18, mutants 26/26 caught, `_validate_kg.py`
rc 0 on the live tree with the grammar carrying three more kinds BY ADDITION.

---

## 1. A3 — the mechanism I chose, and the bite that proves it

**Chosen: the ruling's own clause.** `s230-D2`'s `says` literally reads
*"App-shell-nav-rail deliberately NOT rebound (56px rail head, no lockup fits …)"*. A new module constant
reads THAT CLAUSE and takes the name out of it:

```python
RESIDUE_RX = re.compile(r"([A-Za-z0-9][A-Za-z0-9._-]*)\s+deliberately NOT rebound", re.I)
```

`residue_clauses(dr)` returns `[(name, clause)]` — the name the clause names, plus the ruling's own sentence
quoted back (cut at the first `. `, capped at 200 chars). `build()` now iterates THOSE names and looks each
one up in the metas case-folded; it no longer asks of every component slug "are you a substring of this
ruling's English?".

Two consequences, both deliberate:
* the residue's `why` no longer hardcodes "56px rail head, no lockup fits" — the reason is now the RULING'S
  OWN WORDS, carried in the `note`. A fourth substring slug can no longer inherit the rail's reason, because
  it can no longer produce a null at all.
* a clause that names a component with no meta is DECLARED (`source: null`, the clause quoted), never dropped
  and never attached to a guess.

**The bite — 18 (new), plus 10 (rewritten).** The mini corpus gained a component `chrome.meta.json`: its slug
IS a substring of the mini ruling's English ("on light chrome"), it binds no logo, and the clause does not
name it. Under the old test it got a declared null with the rail's reason; bite 18 asserts

* `"chrome"` really is in the ruling text and really is a component (so the bite can fail), and
* `residue_clauses()` names exactly `["rail"]`, and
* the set of `usesLogo` declared-null sources is exactly `{"component:rail"}`.

Bite 10 additionally asserts the rail's note quotes `deliberately NOT rebound` and that the string `56px`
appears nowhere in the generator's own `why`/`note` — the reason is the ruling's, not ours.

**The mutant — M26 (new).** `_mutate.py` grew a 26th mutant that puts the substring-over-English test back:
`RED 10,18`. M16 (the residue quietly completed) was re-anchored on the new loop and still goes `RED 10,18`.

## 2. A4 — the bytes dropped

Fixed in `notes/_lanes/277/icons-propose/meta.schema.diff`, both `edges` descriptions — the only text in the
diff that would LAND under `knowledge/` and go stale:

| dropped | from |
| --- | --- |
| `758` (distinct normalised path keys) | `usesIcon` description |
| `Measured live: 371 pairs across 105 components and 81 of the 666 icons.` | `usesIcon` description |
| `81 of 666 … illuminates 12% … a twelfth of it` (limit 2) | `usesIcon` description |
| `102` inline paths (limit 3) | `usesIcon` description |
| `835` `<svg>` elements (limit 4) | `usesIcon` description |
| `Measured live: 18 entries across 9 components and 4 of the 12 lockups.` | `usesLogo` description |
| `the 9 metas that say 'logo'` → `the metas that say 'logo'` | `usesLogo` description |

**The four declared limits stay, all four, in substance** — reference-render-not-contract; a minority of the
library is used; unmatched inline paths get no entry; sprite `<use>` `<svg>`s mean the pair set is right and
the frequency is not measured. Each description now says out loud WHERE the number lives instead: re-derived
on every run by `gen_kg_icons.py` into the generated node file. `grep` for `758|Measured live|102 inline|835
<svg>| 371 |12%` in the diff returns nothing.

**"whatever in the generator emits it":** nothing in `gen_kg_icons.py` ever emitted those integers — `grep`
for `Measured live|758|835` over the generator is empty, and its only description strings are the `$source`
/ `via` sentences, which carry no counts. The one piece of code that WRITES schema text is
`_simulate_validator.py`'s `ASSET_EDGE` / `nep[...]` block, and those descriptions were already count-free;
they are unchanged. So A4 was a one-file fix, and I am saying so rather than inventing an edit.

## 3. The door

`RATIFIES = ("s277-D4", "s277-D5", "s277-D6", "s277-D7")` — the four ids that ratify THIS proposal and no
others. Prose updated where it said the door was shut: the docstring's `#75` paragraph, the "WHERE IT WOULD
LAND" paragraph (now "WHERE IT LANDS"), the Usage block (a `--land` line), the `RATIFIES` comment, `land()`'s
docstring, the allowlist refusal message (it no longer claims "no s277-D* id names this family yet"), and the
dry-run footer print.

Bites 12 and 17 were rewritten to test the door WITH THE ALLOWLIST OPEN. The mini corpus gained a recorded
`s277-D4` ruling so the open door has something legitimate to open on:

* **bite 12** — with the list open, `--land` still refuses (a) no id, (b) `not-a-ruling`, (c) `s999-D9`
  (unrecorded), (d) each LIVE ruling not in the list (`s001-D1`, `s230-D2`) — each at its own gate, with its
  own message, and no file written.
* **bite 17** — the landing path is now reached through the REAL allowlist (`land(k, "s277-D4")`), not by
  temporarily mutating the global. It asserts the two files are written, the ruling is named in `ratified`
  and in `$description`, `PROPOSED` / `NOT RATIFIED` are gone, and every input byte is unchanged.

M18 (allowlist bypassed) → `RED 12,17`; M19 (`--land` accepts any string) → `RED 12`; M20 (PROPOSED text
kept) → `RED 17`. The door's mutants still bite with it open.

## 4. Gate lines, verbatim

```
$ python3 notes/_lanes/277/icons-propose/gen_kg_icons.py --selftest
  ok    bite 1: every manifest record becomes an icon: node carrying its own fields verbatim + its group key
  ok    bite 2: active<->slug agreement is re-derived (0 mismatches) and inGroup covers every icon once
  ok    bite 3: activeVariantOf draws the resolvable twins, declares the orphan as t:null, and declares B4 without drawing defaultActive
  ok    bite 4: usesIcon comes from the gate's own normalised byte-match (whitespace-insensitive) and a DRIFTED gate flips the assertion to False
  ok    bite 5: the prose route fires in the corpus and NO edge is drawn from it — measured, refused, counted
  ok    bite 6: an icon-bearing snippet with no component is declared in unresolved and drops no pair silently
  ok    bite 7: a ruled-in .svg missing from the manifest gets NO node, is named as B1, and its ruledBy edge is declared not invented
  ok    bite 8: logo nodes parse lockup/theme/colourMode from the filename, refuse a malformed stem, and usesLogo comes from src=
  ok    bite 9: defaultFor fires on exactly the stems s230-D2 names, carries the stem's own theme, and invents no theme: node
  ok    bite 10: a component s230-D2's own clause names but that binds no logo enters as a declared null quoting the ruling
  ok    bite 18: the residue is anchored on s230-D2's own clause: a SECOND slug that is merely a substring of the ruling's English produces NO null
  ok    bite 11: --icons-only drops iconGroup+inGroup, --no-logos drops every logo node and edge, --no-usesicon drops only the byte-match
  ok    bite 12: with the allowlist OPEN, --land still REFUSES for the RIGHT reason at each gate — no id, malformed, not in _rulings.json, a live ruling not in RATIFIES — and writes no file
  ok    bite 13: all six edge types are declared NEW and no seventh type is emitted
  ok    bite 14: themedBy is declined: zero token edges, the fillMode split reported, tokens.icon handed over
  ok    bite 15: --dry-run writes its three JSONs outside the corpus and leaves the corpus byte-identical
  ok    bite 16: the explorer payload is measured in bytes from the serialised nodes+edges and the chip ships OFF
  ok    bite 17: --land through the REAL allowlist writes exactly the two node files, NAMES the ruling, drops the PROPOSED text, and leaves every input byte-identical
SELFTEST PASS
rc=0

$ python3 notes/_lanes/277/icons-propose/_mutate.py
BASELINE red=[] crashed=False — PASS
  M16   the s230-D2 residue is quietly completed instead of declared                                                      -> RED 10,18
  M26   the residue goes back to the substring-over-English test (A3: a second substring slug inherits the rail's reason) -> RED 10,18
  M18   the RATIFIES allowlist is bypassed — any real ruling opens the door                                               -> RED 12,17
  M19   --land accepts any ratified string at all                                                                         -> RED 12
  M20   the landed files keep the dry run's PROPOSED / NOT RATIFIED text                                                  -> RED 17
ALL MUTANTS CAUGHT
   (26 mutants, 0 survivors; the 21 unchanged rows are in the run's own output, each RED on its own bites)

$ python3 notes/_lanes/277/icons-propose/gen_kg_icons.py --dry-run <scratch>
DRY RUN — 666 icon records · 10 groups · 12 logos  ->  688 nodes · 1299 edges
  nodes: {'iconGroup': 10, 'icon': 666, 'logo': 12}
  edges: {'inGroup': 666, 'activeVariantOf': 234, 'usesIcon': 371, 'usesLogo': 18, 'defaultFor': 2, 'ruledBy': 8}
  edge targets resolved: {'inGroup': 666, 'activeVariantOf': 232, 'usesIcon': 371, 'usesLogo': 18, 'ruledBy': 8}
  status: {'inGroup': 'NEW', 'activeVariantOf': 'NEW', 'usesIcon': 'NEW', 'usesLogo': 'NEW', 'defaultFor': 'NEW', 'ruledBy': 'NEW'}
  byte-match: {'library_keys': 758, 'snippet_files': 137, 'inline_path_occurrences': 592, 'unmatched_paths': 102, 'svg_without_path': 835} -> 371 pairs / 105 components / 81 icons (585 of 666 icons unused)
  declared nulls (unresolved): 32
  payload 356,431 B against explorer 2,893,289 B = +12.32%
  chip: assets default OFF
  wrote <scratch>
  NOT LANDED — this is a dry run. Three node kinds and six edge types are closed-vocabulary changes (#75); RATIFIES is ('s277-D4', 's277-D5', 's277-D6', 's277-D7'), so --land accepts those ids and refuses every other id there is.

$ python3 notes/_lanes/277/icons-propose/gen_kg_icons.py --land --ratified s277-D4
LANDED — ratified s277-D4 · ['_icon_nodes.json', '_logo_nodes.json']

$ python3 knowledge/_validate_kg.py
== _validate_kg.py — KG edge parse-gate (s131-D2 / s133-D1 / s135-D4) ==
metas checked: 139
ref:null + $note (declared, awaiting Dave's-eye migration): 90
resolutions consumed (s135-D4, KG-REVIEW-VERDICTS-2026-08-08-s135-v1.json): 82 ruled verdicts asserted present (MERGE 5 / PROMOTE 52 / ATTACH 25)

_validate_kg.py: OK — every ref parses+resolves, every null carries a note, every meta has provenance, edges match schema, gen_kg_edges.py is idempotent-clean, and the s135-D4 resolutions input was consumed.
rc=0
```

## 5. Counts, re-read from the LANDED files

```
nodes 688   {'icon': 666, 'iconGroup': 10, 'logo': 12}
edges 1299  {'inGroup': 666, 'activeVariantOf': 234, 'usesIcon': 371, 'usesLogo': 18, 'defaultFor': 2, 'ruledBy': 8}
themedBy 0 · defaultActive 0 · null-target edges 4 (2 defaultFor + 2 orphan activeVariantOf)
declared nulls (unresolved) 32
ratified s277-D4 (both files) · $description carries RATIFIED, not PROPOSED
```

Independent resolution check over the two landed files against the live stores: **0 unresolvable refs**
(every `s`/`t` is either a node in the file, a `component:` meta stem, or a `ruling:` id), and every
`t: null` edge carries a `$note`.

## 6. Step 3 — the byte-diff of the dry run

`_icon_nodes.json` and `_logo_nodes.json` from a fresh `--dry-run` into scratch are **byte-identical** to the
committed proposal copies (`cmp` silent on both). A3 and A4 changed ZERO bytes in the node files, which is
the expected shape: the residue lives in `report["unresolved"]`, which is `dry-run.json` only, and A4 touched
a `.diff`, not the generator.

`dry-run.json` differs in exactly four places, all named:

1. `corpus` — this session's mount path vs the proposal session's. Environmental.
2. `rulings_available` — `593` → `604`. The tree gained 11 rulings since `5520d43`. Not mine.
3. the `app-shell-nav-rail` unresolved entry — **A3**: `why` drops the hardcoded "(56px rail head, no lockup
   fits …)" and now reads "s230-D2 names this component in its own clause as deliberately NOT rebound — a
   ruling-shaped residue that stays Dave's. The gap is DECLARED, never quietly completed"; `note` gains the
   ruling's own sentence, quoted: `s230-D2 says "App-shell-nav-rail deliberately NOT rebound (56px rail head,
   no lockup fits - a ruling-shaped residue that stays Dave's)."`
4. `ratifies` — `[]` → `["s277-D4","s277-D5","s277-D6","s277-D7"]`. **The door.**

Nothing else in the report moved: same 688/1,299, same 32, same 371/105/81, same 758/592/102/835, same
356,431 B payload.

## 7. Step 5 — the grammar, +3 kinds BY ADDITION

`knowledge/_validate_kg.py` did not know the three kinds (it carried ten). Added, never rewritten:

* `REF_RE` — the ten alternatives are untouched; `|icon|iconGroup|logo` is appended as a second regex line.
* `NODE_KINDS` — `"icon", "iconGroup", "logo"` appended after `"ux"`.
* two new store constants `ICON_MANIFEST` / `LOGO_DIR`, added after `UX_NODES`, with the s277 comment.
* two new resolvers `icon_ids()` (returns the 666 icons and the 10 group ids) and `logo_ids()` (the 12
  stems), added after `ux_ids()`.
* three new entries in the `resolvers` dict, after `"ux"`.

No existing kind, resolver or store changed shape. Measured after: `icon ids 666 · group ids 10 · logo ids
12`, `icon:menu-search` resolves **False** (blocker B1, deliberate — the manifest is the home and is one
asset stale), validator rc 0.

## 8. What the chip lane needs (NOT this lane — nothing in the explorer was touched)

* **The two files.** `knowledge/_icon_nodes.json` and `knowledge/_logo_nodes.json`, each
  `{$description, generated_by, family, edge_types, ratified, nodes[], edges[]}` — the same shape
  `_rule_nodes.json` / `_ux_principle_nodes.json` have, so `rule_nodes()`'s reader pattern in
  `_build_kg_explorer.py` transfers unchanged (`json.load` → `d.get('nodes', [])`, `d.get('edges', [])`,
  and a missing file returns `[], []`).
* **Node shape.** `{id, type, label, fam: "assets", …}`. `type` is one of `icon` / `iconGroup` / `logo`.
  icons carry `name, slug, file, active, fillMode, fills, group` (+ `$derived` where the #264 repair wrote
  one); iconGroups carry `groupKey, count`; logos carry `file, lockup, theme, colourMode`.
* **Edge shape.** `{s, t, type, fam: "assets"}` + extras: `via` on `usesIcon`/`usesLogo`, `theme` + `ruling`
  on `defaultFor`, `$note` on every `t: null`. Six names: `inGroup` 666 · `activeVariantOf` 234 (232 drawn,
  2 orphan nulls) · `usesIcon` 371 · `usesLogo` 18 · `defaultFor` 2 (both `t: null`) · `ruledBy` 8.
  Sources outside the family: `component:<slug>` (usesIcon/usesLogo) and `ruling:<id>` (ruledBy target) —
  both already node ids in the base graph, so the family hangs off it rather than floating.
* **The family key: `assets`, and it is FREE.** `RULE_FAM`'s note at line 113 warns that `rules` was taken
  by the base wiring chip, so I checked the same way rather than assuming: the live `notes/_KG-EXPLORER.html`
  carries exactly four `"fam":` values — `governance` (5,348), `guidelines` (1,262), `guidelinerules`
  (1,034), `uxprinciples` (282). No `assets`, and `grep assets knowledge/_build_kg_explorer.py` is empty.
  The generator already stamps `fam: "assets"` on every node and edge.
* **The chip ships OFF** (s274-D11 / #275 precedent, asserted by bite 16), and the layout column: the
  existing families sit at `cx` −1.0 / 1.0 / 2.2 / −2.2 (line 425), so the assets family needs a fifth `cx`
  of its own.
* **Size:** 356,431 B of serialised nodes+edges against a 2,893,289 B explorer — **+12.32%**.

## 9. Declared — what I did not do, and its size

* **`s277-D6`'s literal clause, under one of its two readings.** D6's `ruled` says "the 15 bases carry NO
  `activeVariantOf` edge and each of the 31 is a declared null". Read as *no edge is SOURCED AT a base* —
  i.e. no `defaultActive`, nobody invents a twin — the landed files enact it exactly: 0 `defaultActive`,
  and the 15 bases are 15 declared-null entries naming all 31 actives by slug. Read as *the 31 actives lose
  their `activeVariantOf → base` edges*, they do not: those 31 edges are drawn, inside the 234. I landed the
  first reading because the brief's own count assert pins it (`1,299 edges (666/234/371/18/2/8)`, `32
  declared nulls`) and the second reading contradicts it. **Size of the alternative: −31 edges (1,299 →
  1,268) and +31 declared nulls (32 → 63).** One line of `build()`. It is Dave's or the conductor's to say;
  I did not take it silently.
* **`_simulate_validator.py` can no longer apply its own diff.** Its `_validate_kg.py` anchors are now
  satisfied in the live tree, so step 1 stops at `ANCHOR MISS applying REF_RE/NODE_KINDS: found 0 of 1` —
  the anchor guard working, not a defect. I added six lines to its docstring saying so and changed no code.
  The `meta.schema.json` arm of the diff remains UNAPPLIED and unproposed for land: no meta carries a
  `usesIcon` / `usesLogo` list, and the landed edges live in the node files.
* **The explorer chip.** Not this lane. `knowledge/_build_kg_explorer.py` and `notes/_KG-EXPLORER.html` were
  READ and not written; `git status` proves it.
* **`notes/_dream/_GRADE-DECISIONS.jsonl`** was dirty before I started and is left unstaged.

## 10. `git diff --numstat`, re-read from the SHIPPED sha

Re-read after the commit with `git diff --numstat <sha>^ <sha>` and reported in the lane's reply — a table
inside this file cannot contain the sha of the commit that contains this file. The staged set is exactly:
`knowledge/_validate_kg.py`, `knowledge/_icon_nodes.json` (new), `knowledge/_logo_nodes.json` (new),
`notes/_lanes/277/icons-propose/gen_kg_icons.py`, `notes/_lanes/277/icons-propose/_mutate.py`,
`notes/_lanes/277/icons-propose/_simulate_validator.py`, `notes/_lanes/277/icons-propose/meta.schema.diff`,
`notes/_lanes/279/icons-land/BRIEF.md` (new), `notes/_lanes/279/icons-land/REPORT.md` (new),
`notes/_subreports/2026-09-16-279-IL-icons-land.md` (new).
