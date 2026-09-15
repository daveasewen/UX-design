# Lane RP — the 145 UX principles + the 30 polarities into the knowledge graph (#275, s269-D1 item 3)

READ-ONLY on the corpus. Nothing landed. Two new node kinds and seven new edge types are proposed;
`principles.json`, `polarities.json`, every generated brain artefact, `_rulings.json`, every meta and
`_build_kg_explorer.py` are untouched.

Deliverables: `knowledge/gen_kg_principles.py` · `dry-run.json` ·
`REVIEW-principles-into-graph-2026-09-15-v1.html` · `_build_page.py` (the builder) ·
`principles-kg-decisions-2026-09-15.json` (the page's copy) · `_mutate.py` (the mutation harness) ·
`_drive_page.py` (the page driver) · `screenshot.png` · this report.

## 1. The central finding — existing vs new

| edge type | status | shape | count |
|---|---|---|---|
| `tensionWith` | **NEW** | `ux:` → `ux:` | 22 (0 null) |
| `hasParty` | **NEW** | `polarity:` → `ux:` \| `ruling:` \| null | 68 (51 + 2 resolved / 15 declared null) |
| `touches` | **NEW** | `polarity:` → `ruling:` | 9 (0 null) |
| `resolvedBy` | **NEW** | `polarity:` → `ruling:` | 7 (0 null) |
| `challengedBy` | **NEW** | `polarity:` → `ruling:` | 4 (0 null) |
| `explainedBy` | **NEW** | `polarity:` → `ruling:` | 1 (0 null) |
| `inFamily` | NEW, not recommended | `ux:` → `family:<id>` | 145 + 32 hubs, behind `--family-edges` |
| `evidencedBy` | **EXISTS** | `ux:` → `evidence:<url>` | 145, behind `--evidence-edges`, **0 join a live node** |

Node kinds `ux:<id>` (145) and `polarity:<id>` (30) are both NEW. `ux:` is the prefix s269-D2 ruled and it
is MEASURED free, not assumed.

**TWO vocabularies again, and this time the second one is Dave's own data model.** (1) The explorer
families (`_build_kg_explorer.py`) carry 60 distinct type strings [RV re-measured 62, or 44 real edge types — the 'not one of my seven' finding holds either way] and not one of my seven —
`evidencedBy` is the single overlap, and it is the one I recommend leaving off. (2) `polarities.json`
already carries a typed link vocabulary that s238-D6 ruled — `explainedBy` / `touches` / `resolvedBy` /
`challengedBy` — so those four words are not the lane's invention; they are already the register's, and
the only question is whether they cross into the graph as four types or collapse into one (RP-2 c).

The difference from #274: **not one of the 111 edges is parsed out of prose.** Every one is read from a
field, or from a generated file with a declared derivation rule that this lane re-derived and checked.
`cites` at #274 was the weak one because it parsed rule text; there is no equivalent here — and the three
joins that *would* need prose are measured, reported, and deliberately not drawn (§3).

## 2. Every count and the command that produced it

```
python3 knowledge/gen_kg_principles.py --dry-run notes/_lanes/275/principles-kg/dry-run.json
→ 145 principles · 30 polarities · 175 nodes · 111 edges
  edges: {'tensionWith': 22, 'hasParty': 68, 'explainedBy': 1, 'touches': 9,
          'resolvedBy': 7, 'challengedBy': 4}
  nodes: {'ux': 145, 'polarity': 30}   unresolved: 27
  pairwise view fresh (re-derived from polarities.json): True

python3 knowledge/gen_kg_principles.py --family-edges --evidence-edges --dry-run /tmp/opt.json
→ 260 nodes · 401 edges  (+inFamily 145 / 32 hubs, +evidencedBy 145 / 53 evidence nodes)

python3 knowledge/gen_kg_principles.py --no-polarity-nodes --dry-run /tmp/nopn.json
→ 145 nodes · 22 edges · unresolved 33   (the measured cost of RP-3 option b)
```

Independent measurements, each run standalone before the generator existed:

- **145 principles · A 6 / B 28 / C 75 / D 9 / L 27 · 32 families · all twelve fields present on all 145** —
  `python3 -c "import json,collections;P=json.load(open('knowledge/brain/principles.json'))['principles'];
  print(len(P),collections.Counter(p['grade'] for p in P),len({p['family'] for p in P}))"`.
  (The conductor's BRIEF.md line 5 says 31 families — the #269 inventory carries no such figure (lane RV, VERIFY.md); the measured answer is **32**.)
- **Live node prefixes, 18 of them, counted off the explorer page itself** — `evidence 873 · artefact 610 ·
  ruling 578 · rule 470 · pattern 382 · context 232 · component 137 · snippet 137 · session 92 · axe 64 ·
  sc 38 · shape 23 · intent 14 · role 12 · guideline 12 · principle 4 · standard 1 · policy 1`.
  `re.findall(r'"id"\s*:\s*"([A-Za-z][\w-]*):', open('notes/_KG-EXPLORER.html').read())` → **`ux:` is free,
  `polarity:` is free.** `rule:` is now taken — RK landed at #274, which is the proof this door works.
- **Live edge-type vocabulary: 60 distinct strings, and `tensionWith` / `hasParty` / `explainedBy` /
  `touches` / `resolvedBy` / `challengedBy` / `inFamily` are all ABSENT.** `evidencedBy` is present, 1,228
  edges. Same regex over the `type` key.
- **22 polarity edges, and the derived view is FRESH** — re-derived from `polarities.json` by the rule
  printed inside `polarity-edges.json` (unordered pairs of parties on DIFFERENT sides whose refs both
  resolve to a register row); the two sets are identical, 22 = 22. This is proof, not a sha comparison.
- **30 polarities · 18 with a derived pair · 12 without · 68 parties · 21 typed links to 14 distinct
  rulings · 15 declared stubs · 2 ruling parties.** Every one of the 21 link refs and both ruling parties
  resolve against the 578 ruling ids in `_rulings.json` — **0 unresolved**. The only nulls in the whole
  proposal are the 15 stubs, and each carries its verbatim phrase.
- **Grade names are read, never retyped**: `GRADE_NAMES` at `knowledge/_validate_polarities.py:203` is the
  s237-D1 map, and the generator regexes it out. If the constant goes, the attribute goes (bite 15).
- **Payload: 123 KB for all twelve fields, 33 KB for the head-only alternative**, against an explorer page
  that is already 2.7 MB.

## 3. The three joins that exist in prose only — measured, and NOT drawn

1. **Principle → the standard it restates.** 20 rows sit in standards families (fam-wcag22 11 · fam-coga 6 ·
   fam-aria-apg 1 · fam-en301549 1 · fam-eaa 1). **No field in `principles.json` names an `sc:`,
   `principle:`, `guideline:`, `standard:` or `policy:` node** — all twelve fields checked; the `n.n.n`
   strings that do appear are DOIs and page numbers inside `evidence`, not criteria. 4 ids
   (`pr-wcag-perceivable` and its three siblings) contain the name of a live `principle:` node, which is a
   NAME MATCH — the thing s274-D12 refused for 27 rule→component candidates yesterday. Reported, not drawn.
   → RP-4.
2. **Component → the law it rests on (s269-D5).** `grep` over 137 non-EXAMPLE metas: **0** name a `pr-` id,
   **0** name any of the six A-grade laws verbatim (Fitts · Hick · Steering · KLM / Keystroke-Level ·
   speed-accuracy · graphical perception). Entirely authored work, and P-274-3 already parks the identical
   shape for rules. → RP-5.
3. **Principle → its evidence.** 134 of 145 rows carry a URL, 53 distinct. **0 match any of the 873 live
   `evidence:` nodes** — those are chat receipts and file paths, so reusing the word would make `evidence:`
   mean two different things (the #202 vocabulary-collision class). Off by default. → RP-2 (d).

## 4. What the selftest bites (15 bites, all mutation-proven)

`python3 knowledge/gen_kg_principles.py --selftest` → **SELFTEST PASS**.

1. every register row becomes a `ux:` node whose twelve fields equal the source row read back off disk
2. `tensionWith` is read from `polarity-edges.json`, and re-derivation (same-side pairs refused) agrees
3. the `tensionWith` edge carries the polarity id, the mediating variable and from/to kind
4. the typed links become four distinct edge types and a fifth, untyped, link is REFUSED (s238-D6)
5. a link to a ruling `_rulings.json` does not hold is `t:null` + note, counted, never invented
6. `hasParty` resolves to `ux:` and `ruling:`, and a declared stub is `t:null` carrying the phrase verbatim
7. a polarity with no derivable pair is declared in `unresolved` and still becomes a node
8. `--no-polarity-nodes` removes the nodes and every edge sourced at one, and declares the loss
9. family is an attribute by default, an edge only on demand; grade NEVER moves (s237-D1)
10. `--land` REFUSES with no id, an absent id and a malformed id, and writes no file
11. `--land` writes only the landed file, NAMES the ruling in `$description`, carries no "PROPOSED" or
    "NOT RATIFIED" text, and leaves every input byte-identical
12. `--dry-run` writes its JSON outside the corpus and leaves the corpus byte-identical
13. `edge_status` marks `evidencedBy` EXISTS and the other seven NEW
14. no edge targets `principle:` / `sc:` / `guideline:` / `standard:` / `policy:` — the WCAG join is not drawn
15. `gradeName` is read from the s237-D1 map and omitted when the constant is gone

Mutation proof — `python3 notes/_lanes/275/principles-kg/_mutate.py`, **18 mutants, every one caught**:

```
M1  statement truncated                 -> RED 1      M10 grade moved onto an edge        -> RED 9
M2  same-side pairs allowed             -> RED 2      M11 land accepts any string         -> RED 10,11
M3  tensionWith drops its attributes    -> RED 3      M12 landed file keeps PROPOSED text -> RED 11
M4  any link type accepted              -> RED 4      M13 land rewrites principles.json   -> RED 11
M5  unheld ruling invented as a node    -> RED 5      M14 dry-run leaks into the corpus   -> RED 12
M6  stub invented as a stub: node       -> RED 6      M15 edge_status claims EXISTS       -> RED 13
M7  edgeless polarity dropped silently  -> RED 7      M16 WCAG join drawn by name match   -> RED 2,3,8,14
M8  --no-polarity-nodes leaks its edges -> RED 8      M17 gradeName retyped in the gen    -> RED 15
M9  family edges on by default          -> RED 1,9    M18 ruling party resolved as ux:    -> RED 6
```

**Three mutants survived the first run and were real defects in the bites, not in the code.** M1 survived
because the fixture's statement was 30 characters and the mutant truncated at 40 — a bite that could not
fail. M2 survived because the fixture had no same-side pair, so ignoring the different-sides rule changed
nothing. M9 crashed rather than reporting, because bite 1 indexed an attribute the mutant removes. Fixed by
lengthening the fixture statements to 500 chars, adding `pl-03` (the 237-T finding 4 shape: two principles
on one side, which must derive NO edge), and reading the source row back off disk instead of comparing to a
literal. **A green selftest without the harness would have shipped three dead bites.**

## 5. Gates

- `python3 knowledge/gen_kg_principles.py --selftest` → **SELFTEST PASS** (15/15)
- `python3 notes/_lanes/275/principles-kg/_mutate.py` → **ALL MUTANTS CAUGHT** (18/18)
- `python3 knowledge/_validate_kg.py` → **OK** — 139 metas checked, "every ref parses+resolves, every null
  carries a note, every meta has provenance, edges match schema, `gen_kg_edges.py` is idempotent-clean".
  This lane wrote no meta, and the run proves it rather than asserting it.
- `python3 notes/_lanes/275/principles-kg/_drive_page.py` (after `source knowledge/_render/seat_env.sh`) →
  **DRIVE PASS**, 11 checks: font loaded (`HSBC_MtUnivers_Latin`) · 0 console messages of any kind ·
  descenders intact on the tight boxes (35 elements, worst clip 0.00px) · nothing crops its own content ·
  no `text-transform:uppercase` · no ALL-CAPS runs in visible prose (nam-002) · export is the RK shape ·
  localStorage round-trips a choice and a note across a reload · 390px has no horizontal scroll ·
  **and both themes**: accent `rgb(218,26,0)` on white / `rgb(246,96,76)` on dark, the two-red law
  (s151-D1), with the crop clauses re-run per theme.
- `_validate_compose.py` NOT run: it gates `canon/canon.css` composition and nothing this lane wrote is
  composed.
- `git status --short` → only new files from this lane, plus two pre-existing modifications I did not make
  (`notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl`). `knowledge/` tracked files:
  `git diff --stat -- knowledge/` is empty.

### The descender check needed fixing before it meant anything

The `_validate_demo_page.py` canvas clause applied naively to every selector reported a 19.55px clip on
`.okey` — an inline `<span>`, whose `clientHeight` is 0, so the number was an artefact. Widening it to
`lines = round(clientHeight / lineHeight)` then reported 5.3px on ordinary body paragraphs, because padding
and mixed inline font sizes break that assumption too. The clause is correct for what it was written for —
a single-line, unpadded, own-box element — so it is applied to exactly those eight selectors, and a second,
independent check covers everything else: no element whose overflow is not `visible` is overflowing.

**It did catch three real crops** at the display sizes, where Univers Next's font box (cap 0.723em +
descender 0.232em + internal leading) needs 1.166 / 1.213 / 1.212em: `h1` was at 1.08, `h2` at 1.2,
`.stat b` at 1.15. The Swiss system's 1.0–1.08 display range crops in this face, so the house descender
clause won and the CSS says why in a comment.

## 6. Quote gate

Two sentences on the page are attributed to Dave. `python3 knowledge/_quote_gate.py` returns **0 verbatim**
for both, because its index covers neither `notes/_lanes/` nor the `says` field of `_rulings.json` — the
known gap named in the #275 brief. Both were therefore verified by hand against the source file, and each
occurs **exactly once** in `knowledge/_rulings.json`:

- `"Evidence grade is a field on every principle node."` — in the `says` of **s237-D1**.
- `"my instinct is that adopting the hyper-relationship version might pay off in the future when we really
  make this KG more powerful"` — in the `says` of **s238-D1**.

A third, `"is the edges on edges such a daft idea ???"`, passed the gate ✅ verbatim (`_GM-ARCHIVE.md:604`)
and was NOT used: it is the question s238-D1 answers, and quoting the question back reads as a gotcha.

## 7. What I did NOT do — and one thing I did by mistake

- Did not land. But **I did run `--land --ratified s269-D2` against the live tree as a fourth refusal
  probe, and it landed** — s269-D2 is a recorded ruling, so the guard correctly let it through. It is my
  error, not the generator's: the guard checks that a ruling EXISTS, which is all #75 asks of it, and it
  cannot know that s269-D2 does not ratify *this* proposal. I deleted
  `knowledge/_ux_principle_nodes.json` immediately; `git status` shows it gone and no tracked file in
  `knowledge/` changed. **Recorded here rather than quietly cleaned up.** The lesson is one line: drive the
  refusal probes against the SELFTEST's synthetic corpus, never the live one — the selftest already does
  exactly this (bite 10) with a scratch tree.
- Did not edit `principles.json`, `polarities.json`, `polarity-edges.json`, `polarity-status.json`,
  `stubs.json`, `polarity.schema.json`, `_rulings.json`, `_validate_polarities.py`, `meta.schema.json`, any
  `*.meta.json`, `_rules-index.json` or `_build_kg_explorer.py`; did not run `gen_kg_edges.py`,
  `_build_all.py` or `_build_kg_explorer.py`; did not stash, checkout or reset.
- Did not write the explorer READER. If RP-6 (a) is ruled, wave-1 work is the landed file plus ~14 lines in
  `_build_kg_explorer.py` (section C is the template) and a chip. Until then a landed file is an instrument
  without a consumer — which the generator now says in its own output, **measured at run time by grepping
  the explorer for the filename**, not hard-coded. (`gen_kg_rules.py`'s equivalent line is stale: explorer
  v1.11 reads `_rule_nodes.json`. Not fixed here — it is not this lane's file.)
- Did not draw the three prose joins (§3); did not touch `_parked.json` (P-274-3 fired its advisory notice
  on every run and is quoted into RP-5).

## 8. Ruling-shaped sentences — every one is a decision on the page, none made silently

1. **What the `ux:` node carries** → RP-1. (The prefix itself is s269-D2 and is NOT re-asked; it is
   re-measured free and stated.)
2. **Which of the six edge types land in wave 1** → RP-2.
3. **The polarity is a node, not an edge attribute** → RP-3.
4. **The 20 standards-family principles land with no cross-link** → RP-4.
5. **The s269-D5 authoring rides with P-274-3 in one lane** → RP-5.
6. **The nodes live in `_ux_principle_nodes.json` and the reader lands in the same commit** → RP-6.

Three more are ruling-shaped but did NOT reach the page (≤ 6 decisions), recorded so they are not lost:

- **`grade` is an attribute, and this was never in question.** s237-D1 is Dave's own sentence — "Evidence
  grade is a field on every principle node" — so unlike RK-3, there is no decision here and none was
  manufactured. `--family-edges` moves `family` and never touches `grade` (bite 9, mutant M10).
- **The four typed links could be one `polarityLink` type** carrying `linkType`. It is RP-2 option (c)
  rather than its own decision, because the trade (three words of vocabulary against s238-D6's "the typed
  link IS the citation") is the same trade RP-2 already puts in front of him.
- **`hasParty` runs polarity → party**, following s238-D1's "the node is the home with N typed parties".
  The inverse (`partyOf`, party → polarity) would scatter the same fact across 51 principle nodes and two
  rulings, and the 15 stub parties would then have no source node at all.
