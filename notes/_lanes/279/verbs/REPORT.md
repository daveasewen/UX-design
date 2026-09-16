# LANE VB — REPORT — the twelve verbs: `_kg_verbs.json`, a reading map over the storage edge types, read by the slice and ASK
#279 · 2026-09-16 · enacting `s277-D11` (context `s277-D8` edge-force, `s277-D10` the slice contract, `s274-D11` reader-in-the-same-commit) · lane VB (Fable 5.1) · judgement lane: every verb is a claim about what an edge type MEANS, rested on the type's own definition and the audit's sentence

**The one line.** The storage vocabulary measures **58 edge types today** (the audit's 51 + the seven assets-family types of s277-D4 — measured, not typed). `knowledge/_kg_verbs.json` reads **36 of them through the audit's twelve verbs** (two types, `obeys` and `governs`, split by a declared discriminator) and carries **22 as `unread`** with a note each — the audit's ten machinery types, six the audit named nowhere (the five polarity types + `triggeredBy`), and six assets types that landed after the list. Storage untouched: no type renamed, merged or retired; none of s267-D3 / s270-D2 / s274-D8 / s275-D2 touched. The consumer is in the same commit: every `governs` / `obeys` / `mustNot` row of the seed carries `verb` + `verbVia`, every ASK answer carries `readsAs` and a `verb` per edge row, `--verbs` prints the map with live counts. Reader coverage of s277-D10's 3,110 consumer-less edges: **walked 2,351 of 3,136 today (75%; was 2,152 = 69% before this lane — `ruledIn`'s 199 are the gain)**, named with a verb 2,301 (73%). Selftest 62 → 75 bites (13 added), 0 failed on the committed blob; 79/79 in the working tree with lane PK's four PACK bites; `_validate_kg.py` rc 0.

## 1. The denominator — measured

`python3 -c "import sys;sys.path.insert(0,'knowledge');import _build_kg_explorer as B;bn,be=B.extract();xn,xe,rep=B.extract_extra(bn,be);import collections;print(collections.Counter(e['type'] for e in be+xe))"` → **58 types · 8,087 edges · 135 declared nulls**. Cross-checks: `meta.schema.json` `edges` has 21 typed keys (+2 `$` contract strings), all 21 minted; `_validate_kg.py` knows the same 23; the five node files' `edge_types` blocks (rules 4 + appliesTo · ux 6 · icons 7 · logos 8 · ruling edges 10) all appear in the extract; the slice's own `load_live()` mints 51 of the 58 (it does not mint `boundBy checkedBy enClause mentions ruledIn under verifiedBy` — `ruledIn` it now does, see §4). The seven not in the audit's 51: `activeVariantOf defaultActive defaultFor inGroup ruledBy usesIcon usesLogo` (s277-D4, landed the same day as the audit, after A1's census).

## 2. The twelve — what the audit said, and what each type's own definition says

The audit's sentence (A2 §4, verbatim in the map's `$audit.verbList`) is **exactly twelve** verbs and every verb has at least one live type — nothing padded, nothing dropped. The ruling's own parenthetical names *chooses*: that is s277-D8's SYSTEM-view posture (the agent chooses among what exists), not a thirteenth verb; the `is`-force verbs are what it chooses over.

| verb | force | edges | reads (live count) |
|---|---|---|---|
| `is-a` | is | 20 | `family` 12 · `partial` 6 · `reuses` 2 |
| `contains` | is | 191 | `containedBy` 88 · `hasPart` 22 · `composedOf` 5 · `consumes` 70 · `drivesConsumer` 5 · `delegatesTo` 1 |
| `sits-with` | should | 8 | `groupsWith` 8 |
| `must-not-sit-with` | must | 70 | `mustNotNeighbour` 70 |
| `yields-to` | should | 45 | `yieldsTo` 45 |
| `renders-as` | is | 137 | `renderedBy` 137 |
| `lives-in` | is | 788 | `usedInContext` 367 · `commonPattern` 421 |
| `provides-answers` | is | 162 | `providesRole` 108 · `answersIntent` 28 · `hasDataShape` 26 |
| `must` | must | 1,139 | `appliesTo` 826 · `obeys` 18 · `governs` 295 |
| `should` | should | 136 | `obeys` 136 |
| `rests-on` | should | 36 | `obeys` 14 · `tensionWith` 22 |
| `decided` | is | 2,765 | `governs` 1218 · `governedBy` 38 · `ruledBy` 8 · `evidencedBy` 1254 · `ruledIn` 199 · `bounds` 1 · `confirms` 5 · `corrects` 1 · `enacts` 6 · `extends` 16 · `narrows` 2 · `refines` 4 · `retires` 1 · `supersedes` 3 · `supersedesClause` 9 |

Judgements that needed making, each written into the map as `$definition` / `$note`:

- **`obeys` is split three ways, and the split is the edge's own definition.** `meta.schema.json` `edges.obeys` reads *"the rules this component obeys and the laws it rests on, in ONE list"* (s276-D3) — so `obeys → ux:` IS rests-on by the edge's definition, and the audit's *should* (destiny ADVISORY/REVIEW/TASTE) vs *must* (BLOCKING) reads the rule's own authored force field, which the edge transmits. The branch never reads the VIEW a node sits in — s277-D8's *"force is the edge's not the node's"* holds: the 14 obeys→ux edges stand as obligations at `should`, not demoted to *may* because ux: nodes sit in EXPLANATION.
- **`governs` is split by target kind, not by a derived scope.** The audit wrote *"design-scoped governs"*; s277-D8 says the derived per-ruling scope is UNRATIFIED. The map reads the edge's own resolved target — `governs[] → component:` (the entry names a meta path or its renderedBy snippet) is `must`; `governs[] → artefact:` is `decided`. This is what the slice already did (blocking:true on every governs row); the verb names it.
- **`decided` has ten ruling→ruling types, not eleven.** `_ruling_edges.json` holds ten authored types; A1's eleventh ruling→ruling type is `mentions`, the unratified regex proposal the same audit sentence calls machinery. A proposal is not a decision — `mentions` is unread.
- **`ruledBy` (8, assets) is read as `decided` on this lane's judgement**, flagged as such in the map: its definition is "ruled in by sNNN-DN", the assets' `governedBy`. The other six assets types are not forced (§3).
- **No verb carries `may`.** The two descriptive candidates (`lives-in`, `is-a`) are generated from the metas' own prose about where the component IS used and what it IS; reading them as permission would be inference. `sits-with` is `should` because groupsWith is the RULED grouping (s245-D7, s234-D4), not a description. `yields-to` is `should` (the meta's own `when` says so).
- **"the future restsOn"** the audit named is not a type today and is not listed — a phantom would fail the bite.

## 3. `unread` — 22 types, a null carried with its reason

| type | edges | nulls | why no verb of the twelve honestly covers it |
|---|---|---|---|
| `definedIn` | 470 | 0 | machinery the reader uses and the agent never names (the audit's own sentence, A2 §4): rule → the guideline .md that defines it — a file join the slice uses to name `file |
| `enforcedBy` | 63 | 0 | machinery the reader uses and the agent never names (the audit's own sentence, A2 §4): rule → the gate script that enforces it — provenance of enforcement, not a reading  |
| `flaggedBy` | 50 | 0 | machinery the reader uses and the agent never names (the audit's own sentence, A2 §4): snippet → rule — an advisory-signal join the slice walks to reach the `derived` obe |
| `checkedBy` | 68 | 0 | machinery the reader uses and the agent never names (the audit's own sentence, A2 §4): sc → axe rule id — the automatable check behind a criterion |
| `verifiedBy` | 6 | 0 | machinery the reader uses and the agent never names (the audit's own sentence, A2 §4): sc → verification script — the same, for scripts |
| `boundBy` | 55 | 0 | machinery the reader uses and the agent never names (the audit's own sentence, A2 §4): sc → the HSBC accessibility policy — provenance of the criterion |
| `enClause` | 55 | 0 | machinery the reader uses and the agent never names (the audit's own sentence, A2 §4): sc → the EN 301 549 clause — provenance of the criterion |
| `under` | 110 | 0 | machinery the reader uses and the agent never names (the audit's own sentence, A2 §4): sc → guideline → principle — WCAG's own hierarchy, structure of the standard |
| `cites` | 51 | 0 | machinery the reader uses and the agent never names (the audit's own sentence, A2 §4): rule → sc: — a PARSED citation the rule's author wrote in prose (A2 §5); ASK Q11 wa |
| `mentions` | 241 | 0 | machinery the reader uses and the agent never names (the audit's own sentence, A2 §4): ruling → ruling by regex over `says` — an UNRATIFIED proposal drawn dashed (s267-D3 |
| `hasParty` | 68 | 15 | polarity → ux: | ruling — the two sides of a polarity (s275-D2). The audit's twelve name no polarity verb; `rests-on` reads the tension between the sides (tensionWith), a |
| `touches` | 9 | 0 | polarity → ruling — one of s238-D6's four typed links (s275-D2). Not named by the audit's twelve; a ruling that TOUCHES a polarity has not decided it, so `decided` would  |
| `resolvedBy` | 7 | 0 | polarity → ruling — s238-D6 typed link: the ruling resolves the trade-off. Close to `decided` in meaning, but the audit's sentence names neither it nor any polarity→rulin |
| `challengedBy` | 4 | 0 | polarity → ruling — s238-D6 typed link: the ruling challenges the trade-off. Not named by the twelve; not a decision about the polarity. Not forced. |
| `explainedBy` | 1 | 0 | polarity → ruling — s238-D6 typed link: the ruling explains the trade-off. Not named by the twelve. Not forced. |
| `triggeredBy` | 25 | 22 | component → component, 22 of 25 declared null — 'prose, awaiting Dave's-eye' in the schema; the audit's sentence names it in NEITHER list (not a contains/lives-in type, n |
| `usesIcon` | 371 | 0 | component → icon: — landed AFTER the audit's list (assets family, s277-D4..D7). Read by the slice's `assets` field and ASK Q12 (so it HAS a consumer) but no verb of the t |
| `usesLogo` | 19 | 1 | component → logo: — as usesIcon: read by `assets` / ASK Q12, no verb of the twelve; not padded. |
| `inGroup` | 666 | 0 | icon: → iconGroup: — the icon library's own grouping (s277-D4); structure of the assets family, not a reading for a design. |
| `activeVariantOf` | 234 | 2 | icon:-active → icon: base — the variant relation inside the library (s277-D4); `is-a` reads kinship between COMPONENTS and stretching it to glyph variants would be forcin |
| `defaultActive` | 15 | 15 | icon: → null ONLY — declared-null, never drawn, never resolved (s277-D4: no default ruled); a null carried, not a reading. |
| `defaultFor` | 2 | 2 | logo: → null ONLY — s230-D2 names the default lockup per theme but theme: is not a node kind; carried as a declared null with the theme on the edge. Not a reading. |

The polarity five and `triggeredBy` are the honest gap: the audit's sentence names them in **neither** list. `resolvedBy` is close to `decided` in meaning, but reading one of the four s238-D6 links in and leaving three out is a judgement Dave has not seen; it waits with its siblings. The assets edges HAVE a consumer (the slice's `assets` field, ASK Q12) but no verb — a thirteenth verb (*uses*) is Dave's to ratify, not this lane's to pad.

## 4. The consumer — `_compose_slice.py` 1.0 → 1.1 (verb code paths only)

- `load_graph` reads `_kg_verbs.json` as `g["verbs"]`; `verb_index()` / `verb_of(g, type, t)` resolve the map and the two splits per edge — an unknown type, an unknown target kind, a rule id not in the index or a missing map is `unread` with a note, never a crash, never a guess.
- Seed rows: `governs_for` → `verb` must/decided by whether a ruling's `governs[]` names the component or only the meta cites it; `obeys_for` → must/should/rests-on by the target (rows reached with **no storage edge** — derived / routed / routed-by-scope — take the verb their destiny selects and `verbVia` says *"by destiny — no storage edge (routed-by-scope)"*: the verb names the force, the class names the provenance, neither passed off as the other); `must_not_for` → must-not-sit-with, prose and not-with homes saying "no storage edge". `explain()` and `to_html()` show the verb column.
- ASK: `_e()` puts `verb` on every edge row; the result carries `readsAs` {edge type → verb} for the types the question walks; Q5 rows carry `verb` and `session`; Q6 carries `session`. **`ruledIn` is now minted in `load_live()`** (the explorer's own SESSION_RX join, `"#81-D1" → session:81`; 199 of 604 rulings carry a leading #N — the rest have no session edge, not invented) and read as `decided` — the one consumer-less type this lane gives an actual walk.
- `--verbs` prints the map with live counts from the explorer's own extract (falls back to the live reader and says so); `--verbs --coverage` adds §6's measure.
- **Cost, measured:** the worked seed 31,372 → 34,211 cl100k tokens (+2,839, +9%; ratio vs its metas 3.55× → 3.26×) for `verb` + `verbVia` on 122 rows. `verbVia` was shortened once (from ~30 to ~8 tokens a row); dropping it would save ~1,500 more at the price of the provenance sentence.

## 5. Bites — 13 added, 75/75 committed (79/79 with PK's four in the tree)

39 planted edge type (`plantedVerbZZ` on a scratch meta) lands in `unseen` with a note, `verb_of` says unread, no crash · 40 live meta untouched · 69 exactly twelve verbs · 70 forces from the closed set · 71 partition: 58 types = 36 read + 22 unread + 0 unseen, split types' branches equal exactly the verbs listing them, no type in both `reads` and `unread` · 72 every `reads` / `unread` entry is live (count > 0) · 73 every `$source` a substring of its file (12 verbs + 2 ruling fragments) · 74 all 122 seed rows carry a verb + verbVia · 75 obeys rows split by destiny (BLOCKING ⇔ must; ux ⇔ rests-on) · 76 governs rows must vs decided · 77 ASK carries `readsAs` + per-row verb · 78 `ruledIn` read (Q5/Q6 `session`) · 79 unknown kind / missing rule / no map → unread.

## 6. Reader coverage — s277-D10's figure re-measured

`python3 knowledge/_compose_slice.py --verbs --coverage`. D10's 3,110 = A1's 3,125 less the 15 `hasParty` nulls; today the 12 types carry 3,136 (evidencedBy +11). Method = A1 §4's own (a quoted literal in the consumer's CODE — this file below the docstring and above the bites; the D10 list itself excluded).

| type | edges | walked by the slice / ASK | verb |
|---|---|---|---|
| `evidencedBy` | 1,254 | yes | `decided` |
| `appliesTo` | 826 | yes | `must` |
| `definedIn` | 470 | no | `unread` |
| `ruledIn` | 199 | yes | `decided` |
| `checkedBy` | 68 | no | `unread` |
| `hasParty` | 68 | no | `unread` |
| `enforcedBy` | 63 | no | `unread` |
| `boundBy` | 55 | no | `unread` |
| `enClause` | 55 | no | `unread` |
| `flaggedBy` | 50 | yes | `unread` |
| `tensionWith` | 22 | yes | `rests-on` |
| `verifiedBy` | 6 | no | `unread` |

**Walked 2,351 / 3,136 = 75%** (before this lane 2,152 = 69%: evidencedBy Q6 · appliesTo Q11 + load_live · flaggedBy derived-obeys · tensionWith Q4; this lane adds `ruledIn` 199). **Named with a verb 2,301 = 73%.** The 785 walked-by-nothing edges are the map's `unread` machinery (`definedIn` 470 the largest — the slice reads the rule's `file` field, not the edge) and the polarity `hasParty` 68; none is retired.

## 7. Coordination — lane PK, and one thing PK's manifest must know

PK's hunks (`OPENED` + `_load`/`_read` recording, the four PACK bites, 64 lines) were in the working tree throughout and PK's commit had not landed after 30 minutes of polling `git log -1 -- knowledge/_compose_slice.py` (PK's last file touch 17:13, poll ended 17:40). Rather than sweep PK's hunks into this commit or wait indefinitely, **this lane staged a blob of HEAD + its own hunks only** (`git hash-object -w` + `git update-index --cacheinfo`, the `git add -p` the commit script has no form for) and named every other path through `_git_commit.sh`; the working tree keeps both lanes' hunks, so PK's later `git add` of the file commits exactly PK's 64 lines on top. Verified: `diff` of the staged blob against the tree is 64 lines, all PK's; the blob alone passes `--selftest` 75/75. This lane touched only the verb paths and the scratch-copy file list (`VERBS_FILE` added so the scratch reader has the map). Because PK's `_load` records every opened path, **`knowledge/_kg_verbs.json` is a new opened file** — PK's working-tree `_gen_pack_manifest.py` already names it (line 522) and PACK bites 65–68 pass with it present.

## 8. For the explorer lane (not touched here)

A legend reading needs: `reads` + `$splits` resolved per edge by target kind / destiny; `reverse` to draw the arrow the reading way (containedBy, governedBy, ruledBy); `unread` to label machinery as such; a force ramp must | should | is (no `may` today). The `$notes[6]` entry in the map says the same.

## 9. Ruling-shaped, for Dave (not decided here)
1. A thirteenth verb for the assets edges (`usesIcon` 371 / `usesLogo` 19) — *uses*? — or leave them read by `assets` without a verb.
2. Whether `resolvedBy` / `challengedBy` / `explainedBy` / `touches` / `hasParty` get a verb (the audit named none) — one *decided* for `resolvedBy` alone would split s238-D6's four.
3. `verbVia` on seed rows: keep (provenance, +~1,500 tokens) or drop to `verb` only.
