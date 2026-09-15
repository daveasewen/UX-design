# Lane RK — the 470 tagged rules into the knowledge graph (#274, s269-D1 item 2)

READ-ONLY on the corpus. Nothing landed. Four new edge types and one new node kind are proposed;
`_rulings.json` is untouched, no meta is touched, `_rules-index.json` is untouched.

Deliverables: `knowledge/gen_kg_rules.py` · `dry-run.json` · `REVIEW-rules-into-graph-2026-09-15-v1.html` ·
`_build_page.py` (the page's builder) · this report.

## 1. The central finding — existing vs new

| edge type | status | shape | count |
|---|---|---|---|
| `definedIn` | **NEW** | rule → `artefact:knowledge/guidelines/<file>.md` | 470 |
| `cites` | **NEW** | rule → `sc:<n.n.n>` | 51 (32 resolved / 19 declared null) |
| `enforcedBy` | **NEW** | rule → `artefact:<gate path>` | 63 |
| `flaggedBy` | **NEW** | `snippet:<file>` → rule | 50 |
| `appliesTo` | **EXISTS** | rule → component | 27 candidates, OFF by default |
| `hasDestiny` | NEW, not recommended | rule → `destiny:<VALUE>` | 470, behind `--destiny-edges` |

The node kind `rule:<id>` is NEW. The prefix is free — measured, not assumed.

TWO vocabularies, not one list: (1) `meta.schema.json` → `edges.properties`, 21 types that live ON a
component meta — rules are not components, so it does not apply and is NOT edited; (2) the explorer
families (`_build_kg_explorer.py:extract_extra`) — governs · evidencedBy · ruledIn · mentions · under ·
appliesTo · enClause · boundBy · checkedBy · verifiedBy + the authored ruling verbs. `appliesTo` is the
only one of my five already there (826 edges, `sc:` → component). `enforcedBy`'s nearest neighbour is
`verifiedBy` (sc → `artefact:<script>`) — same shape, different subject; reuse is live, see §7.

## 2. Every count and the command that produced it

```
python3 knowledge/gen_kg_rules.py --dry-run notes/_lanes/274/rules-kg/dry-run.json
→ 470 rules read · 521 nodes · 634 edges
  edges: {'definedIn': 470, 'cites': 51, 'enforcedBy': 63, 'flaggedBy': 50}
  nodes: {'rule': 470, 'artefact': 51}   unresolved: 23

python3 knowledge/gen_kg_rules.py --with-appliesto --destiny-edges --dry-run /tmp/opt.json
→ 525 nodes · 1131 edges  (+appliesTo 27, +hasDestiny 470, +4 destiny hubs)
```

Independent measurements (each run standalone before the generator was written):

- **470 rules · ADVISORY 321 / BLOCKING 59 / REVIEW 34 / TASTE 56 · 34 distinct `file` values · 0 missing .md**
  — `python3 -c "import json;d=json.load(open('knowledge/guidelines/_rules-index.json'));print(d['count'],d['byDestiny'],len({r['file'] for r in d['rules']}))"`
- **38 `sc:` nodes** — `knowledge/compliance/rules/*.json` parsed for `sc` (the `_build_kg_explorer.py:sc_rules` source).
- **SC citations: 40 rules cite, 51 citations, 40 distinct criteria, 32 resolve, 19 do not** (17 distinct
  unresolved: 1.2.3 1.2.4 1.3.3 1.4.2 1.4.5 1.4.8 2.4.13 2.5.1 2.5.2 2.5.3 3.1.1 3.1.2 3.1.4 3.2.2 3.2.4
  3.3.7 3.3.8). SC-parenthetical rule, so `4.5.1` (a contrast ratio) is not a citation.
- **Advisory signals: 131 total, 88 cite a rule id, in 59 files; 52 are snippet nodes, 7 are `*.canon.html`
  pages that are not.** 84 citations in snippet files → deduped to **50** `flaggedBy` edges; 4 on
  `canon-gallery.canon.html` → declared unresolved. (`grep -cE '^- \*\*' knowledge/_ADVISORY-SIGNALS.md`;
  `grep -oE '\(([a-z]{2,4}-[0-9]{3})\)' … | sort | uniq -c`) ⚠ only TWO distinct rules are ever cited
  (`nam-002` 86×, `avd-006` 2×): 50 edges, 50 snippets, 2 rules. On the page, not smoothed over.
- **Gates: 46 rules have ≥1 gate, 63 rule→gate pairs, 17 gate scripts** — from
  `knowledge/_instrument-fit.json` `rows[].gates`, which `_build_instrument_fit.py:harvest_gates` builds by
  requiring the gate file to NAME the rule id (no keyword inference). Freshness proved: `rows` ids and index
  ids are the same 470-element set, 0 either way.
- **appliesTo: 27 pairs / 24 rules / 14 components** by exact component-`name` match in the rule text. The
  sample carries visible false positives: `va25-013` (aspect ratios) matched "Avatar" and "Badge",
  `icon-015` matched "Confirmation". Good hits exist too (`copy-030` "Buttons:", `ctkl-001` "Links",
  `neuro-010` "Links and buttons"). This is why it is off by default.
- **Existing prefixes in the live graph** (`notes/_KG-EXPLORER.html`): pattern 382 · context 232 ·
  component 137 · snippet 137 · role 12 · intent 14 · shape 23 · ruling 565 · artefact 570 · evidence 860 ·
  session 92 · sc 38 · guideline 12 · principle 4 · standard 1 · policy 1 · axe 64. `rule:` is free.
- **4 of the 34 guideline docs already exist as `artefact:` nodes** (a ruling governs them) — `definedIn`
  adds 30 nodes, joins 4.

## 3. What the selftest bites (12 bites, all mutation-proven)

`python3 knowledge/gen_kg_rules.py --selftest` → SELFTEST PASS.

1. every index row becomes a `rule:` node carrying id/file/destiny/destinyFull/text
2. `definedIn` is one edge per rule; two docs for three rules (dedupe)
3. the SC parse takes the parenthetical — a ratio `4.5.1` and a bare `1.1.1` are NOT citations
4. an SC with no node is `t:null` + note, counted in `unresolved`, never invented
5. `enforcedBy` reads `_instrument-fit.json` and its ids are asserted to exist in the index
6. `flaggedBy` dedupes two signals to one edge, refuses a `.canon.html` page and a ghost rule id
7. `--land` REFUSES with no id, an absent id and a malformed id, and writes nothing
8. `--land` on a real ruling writes ONLY `_rule_nodes.json`, stamps the id, leaves inputs byte-identical
9. `appliesTo` is off by default and exact-name when on (`EXAMPLE-` metas excluded)
10. destiny is an attribute by default; `--destiny-edges` swaps it for edges + hubs
11. `--dry-run` writes its JSON outside the corpus and leaves the corpus byte-identical
12. `edge_status` marks `appliesTo` EXISTS and the other four NEW

Mutation proof — 13 mutants run, every one turned a bite RED (a bite that cannot fail is not a test):

```
M1  cites accepts any n.n.n                  -> RED 3,4     M8  destiny edges by default        -> RED 1,10
M2  cites invents the missing sc node        -> RED 4       M9  definedIn edge skipped          -> RED 2
M3  flaggedBy stops refusing canon pages     -> RED 6       M10 destinyFull dropped             -> RED 1
M4  flaggedBy drops the dedupe               -> RED 6       M11 enforcedBy ignores the gate map -> RED 5
M5  land accepts any ratified string         -> RED 7       M12 edge_status claims EXISTS       -> RED 12
M6  land also rewrites the rules index       -> RED 8       M13 dry-run leaks into the corpus   -> RED 11
M7  appliesTo on by default                  -> RED 9
```
## 4. Gates

- `python3 knowledge/gen_kg_rules.py --selftest` → **SELFTEST PASS** (12/12)
- `python3 knowledge/_validate_kg.py` → **OK** — "every ref parses+resolves, every null carries a note,
  every meta has provenance, edges match schema, gen_kg_edges.py is idempotent-clean, and the s135-D4
  resolutions input was consumed" (139 metas checked). It reads metas and the schema; this lane wrote
  neither, and the run proves it rather than asserting it.
- `git status --short` → only new files from this lane, plus three pre-existing modifications I did not
  make (`notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl`,
  `notes/_lanes/274/DAVE-RULINGS-2026-09-15.md`).
- Page driven in chromium (`source knowledge/_render/seat_env.sh`): 0 console errors, export produces the
  byte-compatible `{page, at, decisions:[{id, choice, note}]}`, localStorage round-trips, mobile 390px
  `scrollWidth == clientWidth`. Screenshots reviewed before presenting.

## 5. Quote gate

One sentence on the page is attributed to Dave. `python3 knowledge/_quote_gate.py "<sentence>"`:

```
"We will be adding more, for example I'm trying to get hold of our CX principles."
  ✅ 1 verbatim · 0 not in the record — _LIVE-STATE-ARCHIVE.md:36
```

Two more from the same source were checked and NOT used on the page (they are about personas/JTBD, which
this lane does not touch): `"I think your recommendations for the 6 look good"` ✅ verbatim;
`"I don't want to loose the idea."` ✅ verbatim.
## 6. What I did NOT do

- Did not land anything. `--land` exists, refuses without a recorded ruling id, and was only ever run
  against a synthetic corpus in the selftest.
- Did not edit `meta.schema.json`, any `*.meta.json`, `_rulings.json`, `_rules-index.json`,
  `_build_kg_explorer.py` or `gen_kg_edges.py`; did not run `gen_kg_edges.py` / `_build_all.py`; did not
  commit, stash, checkout or reset.
- Did not write the explorer READER for `_rule_nodes.json`. If RK-5(a) is ruled, wave-1 work is: land the
  file + ~12 lines in `_build_kg_explorer.py` + a chip. Until then a landed file is an instrument without a
  consumer — said on the page, in `--land`'s own output, and here.
- Did not widen `appliesTo`; did not re-derive the gate map independently of `_instrument-fit.json` (its
  freshness is asserted against the index instead, bite 5); did not touch `_parked.json`.

## 7. Ruling-shaped sentences — every one is a decision on the page, none made silently

1. **The node prefix is `rule:`** → RK-1. (Free, measured; `gr:` is the alternative.)
2. **Which edge types land in wave 1** → RK-2. (All four / `definedIn` only / two of four / all five.)
3. **Destiny is an attribute, not an edge** → RK-3.
4. **The 19 unresolvable SC citations are declared `ref:null`, not dropped and not blocking** → RK-4.
5. **The nodes live in a new `knowledge/_rule_nodes.json`, and the explorer reader lands in the same wave**
   → RK-5. (The alternative — build them inside `_build_kg_explorer.py` with no file — is option (c) and is
   defensible; I did not pick it silently.)
6. **`appliesTo` stays out of wave 1** → RK-6.

Two more are ruling-shaped but did NOT reach the page (≤6 decisions), recorded so they are not lost:
(i) **`enforcedBy` could reuse `verifiedBy` instead of minting a type** — same shape (sc → `artefact:<script>`),
different subject; a note on RK-2 can rule it. (ii) **`flaggedBy` runs snippet → rule**, the `checkedBy` /
`renderedBy` convention (the edge lives on the thing carrying the evidence); the inverse would read as "this
rule flags that snippet", which is the judge's claim, not the rule's.
