# A1 — MEASURE — the KG audit, every number with the command that produced it
#277 · 2026-09-16 · lane A1 (Opus, mechanical) · brief `notes/_lanes/277/kg-audit/BRIEF.md` · **pinned sha `bedf383`**

**No judgement in this file.** Where the conductor's table is corrected, the correction is a measurement, not an opinion. Lane A2 (Fable) judges.

## Declaration — the working tree was DIRTY
`git status --porcelain` at measurement time:

```
 M notes/_REHEARSAL-LOG.jsonl
 M notes/_dream/_GRADE-DECISIONS.jsonl
 M notes/_lanes/277/DAVE-RULINGS-2026-09-16.md
?? notes/_lanes/277/icons-propose/
?? notes/_lanes/277/kg-audit/
```

`HEAD` = `bedf3838a481d7524dbf34847857d5b22e7d7482` = the pinned `bedf383`. **Nothing under `knowledge/` was dirty** — the three modified files are all under `notes/`, and `notes/_lanes/277/icons-propose/` is the parallel lane. The graph is read entirely from `knowledge/`, so every figure below IS the figure at `bedf383`. `git stash` was not used.

**Not run, as the brief requires:** `gen_kg_edges.py` · `_build_all.py` · `_build_kg_explorer.main()`. Only `extract()` and `extract_extra()` were imported; `notes/_KG-EXPLORER.html` is untouched.

**Gate:** `python3 knowledge/_validate_kg.py` → **OK** (exit 0; 139 metas checked; it independently confirms the 90 base `ref:null` edges counted in item 2).

## Totals
| | value |
|---|---|
| nodes | **3,897** |
| node kinds | **20** |
| edges (non-null target) | **6,616** |
| edges with a `None` target | **105** |
| edges, total carried | **6,721** |
| edge types | **51** |
| base graph (`extract()`) | 1,050 nodes · 1,642 edges |
| additive families (`extract_extra()`) | 2,847 nodes · 5,079 edges |

Command: `extract()` + `extract_extra()` (see `$commands` in the JSON). The conductor's headline — 3,897 nodes · 6,616 edges after dropping 105 · 51 edge types — **reproduces to the digit**.

---
## 1 — The per-kind table (corrected + extended)

**Verdict on the conductor's table: REPRODUCED EXACTLY.** All six columns match on every row the conductor numbered. The one correction is completeness — the conductor collapsed five kinds into a single un-numbered row (`guideline 13 · role 12 · principle 4 · standard 1 · policy 1`); those five are measured here. New columns: degree histogram, median and max degree.

| kind | nodes | deg 0 | deg ≤1 | intra-kind edges | cross-kind edge-ends | cross/node | median deg | max deg | 0 | 1 | 2 | 3–5 | 6–20 | >20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| evidence | 886 | 0 | 818 | 0 | 1243 | 1.4 | 1.0 | 92 | 0 | 818 | 28 | 21 | 15 | 4 |
| artefact | 618 | 0 | 417 | 0 | 1728 | 2.8 | 1.0 | 55 | 0 | 417 | 75 | 50 | 67 | 9 |
| ruling | 593 | 0 | 0 | 288 | 2977 | 5.02 | 5 | 27 | 0 | 0 | 17 | 307 | 265 | 4 |
| rule | 470 | 0 | 305 | 0 | 788 | 1.68 | 1.0 | 51 | 0 | 305 | 101 | 59 | 4 | 1 |
| pattern | 380 | 0 | 341 | 0 | 421 | 1.11 | 1.0 | 3 | 0 | 341 | 37 | 2 | 0 | 0 |
| context | 222 | 0 | 176 | 0 | 367 | 1.65 | 1.0 | 19 | 0 | 176 | 25 | 12 | 9 | 0 |
| ux | 145 | 99 | 109 | 22 | 65 | 0.45 | 0 | 6 | 99 | 10 | 24 | 10 | 2 | 0 |
| component | 137 | 0 | 0 | 269 | 2404 | 17.55 | 19 | 61 | 0 | 0 | 0 | 0 | 85 | 52 |
| snippet | 137 | 0 | 87 | 0 | 187 | 1.36 | 1 | 2 | 0 | 87 | 50 | 0 | 0 | 0 |
| session | 92 | 0 | 47 | 0 | 199 | 2.16 | 1.0 | 7 | 0 | 47 | 16 | 25 | 4 | 0 |
| axe | 64 | 0 | 60 | 0 | 68 | 1.06 | 1.0 | 2 | 0 | 60 | 4 | 0 | 0 | 0 |
| sc | 55 | 0 | 0 | 0 | 1116 | 20.29 | 7 | 111 | 0 | 0 | 0 | 21 | 19 | 15 |
| polarity | 30 | 0 | 5 | 0 | 74 | 2.47 | 2.0 | 5 | 0 | 5 | 12 | 13 | 0 | 0 |
| shape | 23 | 0 | 20 | 0 | 26 | 1.13 | 1 | 2 | 0 | 20 | 3 | 0 | 0 | 0 |
| intent | 14 | 0 | 8 | 0 | 28 | 2.0 | 1.0 | 6 | 0 | 8 | 2 | 3 | 1 | 0 |
| guideline | 13 | 0 | 0 | 0 | 110 | 8.46 | 8 | 20 | 0 | 0 | 2 | 2 | 9 | 0 |
| role | 12 | 0 | 0 | 0 | 108 | 9.0 | 8.0 | 27 | 0 | 0 | 0 | 3 | 8 | 1 |
| principle | 4 | 0 | 0 | 0 | 55 | 13.75 | 15.5 | 21 | 0 | 0 | 0 | 1 | 2 | 1 |
| standard | 1 | 0 | 0 | 0 | 55 | 55.0 | 55 | 55 | 0 | 0 | 0 | 0 | 0 | 1 |
| policy | 1 | 0 | 0 | 0 | 55 | 55.0 | 55 | 55 | 0 | 0 | 0 | 0 | 0 | 1 |

### Top-10 hubs by kind

**evidence** — `evidence:notes/_REVIEW-when-harvest-whole-library-2026-09-14-v2.html` 92 · `evidence:notes/_MEMENTO-DECISIONS.md` 41 · `evidence:notes/_lanes/271/harvest/A/DECISION-TABLE.json` 28 · `evidence:notes/_lanes/271/harvest/B/DECISION-TABLE.json` 21 · `evidence:notes/_lanes/271/harvest/C/DECISION-TABLE.json` 12 · `evidence:GOOD-MORNING.md` 11 · `evidence:notes/_PROPOSED-263.html export block, pasted by Dave in chat #263 2026-09-09; sources per card in notes/_lanes/263-P-proposed-review.md` 11 · `evidence:chat #261 - session opened 2026-09-08 evening and ran into 2026-09-09 (WRAP DATE SPLIT, the #241/#248 shape); the hour of the ruling was not recorded at this seat, so the date carried is the session's COMMIT date, never a claim about the hour` 9 · `evidence:commit d57a1e9 (the #261 wave; the ritual commit adds this entry)` 9 · `evidence:notes/_MEMENTO-DECISIONS.md#I'll go with all your recommendations` 7
**artefact** — `artefact:knowledge/guidelines/copywriting.md` 55 · `artefact:knowledge/guidelines/tone-of-voice.md` 40 · `artefact:knowledge/_capture_gate.py` 31 · `artefact:knowledge/_release/_gen_pack_manifest.py` 27 · `artefact:knowledge/guidelines/neurodiversity.md` 26 · `artefact:knowledge/guidelines/typography-standards-2026.md` 24 · `artefact:knowledge/guidelines/common-toolkit-tags-chips.md` 23 · `artefact:notes/_REVIEW-when-harvest-whole-library-2026-09-14-v2.html` 21 · `artefact:knowledge/guidelines/colour-standards-2026.md` 21 · `artefact:knowledge/_gauge_tokens.py` 20
**ruling** — `ruling:s151-D1` 27 · `ruling:s149-D1` 22 · `ruling:s175-D1` 22 · `ruling:ds-032` 21 · `ruling:s178-D1` 20 · `ruling:ds-021-D1-82` 19 · `ruling:ds-021` 18 · `ruling:s158-D4` 18 · `ruling:s176-D2` 18 · `ruling:s194-D1` 18
**rule** — `rule:nam-002` 51 · `rule:dv-004` 8 · `rule:dv-016` 6 · `rule:dv-017` 6 · `rule:aid-009` 6 · `rule:dv-005` 5 · `rule:dv-009` 5 · `rule:dv-014` 5 · `rule:avd-006` 5 · `rule:type26-019` 5
**pattern** — `pattern:account-overview` 3 · `pattern:spend-by-category` 3 · `pattern:add-a-payee` 2 · `pattern:back-to-navigation` 2 · `pattern:budget-composition` 2 · `pattern:business-banking-landing` 2 · `pattern:card-grid` 2 · `pattern:card-spending-cap` 2 · `pattern:caught-up-inbox` 2 · `pattern:daily-transfer-allowance` 2
**context** — `context:dashboards` 19 · `context:form` 15 · `context:dialog` 11 · `context:reports` 11 · `context:toolbar` 10 · `context:filter-bar` 8 · `context:nothing-this-is-the-outermost-frame` 7 · `context:app-shell-side-nav` 6 · `context:app-shell-top-nav` 6 · `context:list` 5
**ux** — `ux:pr-fitts` 6 · `ux:pr-hick` 6 · `ux:pr-response-limits` 5 · `ux:pr-speed-accuracy` 4 · `ux:pr-dsa25` 4 · `ux:pr-goal-gradient` 4 · `ux:pr-idp-offer-choice` 4 · `ux:pr-nng-minimalist` 4 · `ux:pr-nng-visibility` 4 · `ux:pr-teslers-law` 4
**component** — `component:button` 61 · `component:chart-bar` 59 · `component:chart-line` 51 · `component:template-dashboard-bento` 49 · `component:chart-pie` 46 · `component:links` 45 · `component:navigations` 41 · `component:notifications` 39 · `component:icon-button` 37 · `component:list-items` 36
**snippet** — `snippet:Chart-candlestick.reference.html` 2 · `snippet:Amount-input.reference.html` 2 · `snippet:App-shell-doormat.reference.html` 2 · `snippet:App-shell-focused.reference.html` 2 · `snippet:App-shell-multi-column.reference.html` 2 · `snippet:App-shell-nav-rail.reference.html` 2 · `snippet:App-shell-side-nav.reference.html` 2 · `snippet:App-shell-split.reference.html` 2 · `snippet:App-shell-top-nav.reference.html` 2 · `snippet:Avatar-group.reference.html` 2
**session** — `session:114` 7 · `session:76` 7 · `session:130` 6 · `session:165` 6 · `session:111` 5 · `session:116` 5 · `session:122` 5 · `session:129` 5 · `session:168` 5 · `session:201` 5
**axe** — `axe:input-image-alt` 2 · `axe:aria-hidden-body` 2 · `axe:area-alt` 2 · `axe:link-name` 2 · `axe:aria-meter-name` 1 · `axe:aria-progressbar-name` 1 · `axe:image-alt` 1 · `axe:object-alt` 1 · `axe:role-img-alt` 1 · `axe:svg-img-alt` 1
**sc** — `sc:4.1.2` 111 · `sc:1.3.1` 105 · `sc:1.4.1` 95 · `sc:1.4.11` 70 · `sc:2.5.8` 68 · `sc:2.1.1` 64 · `sc:2.4.7` 64 · `sc:1.4.3` 49 · `sc:4.1.3` 39 · `sc:2.4.3` 38
**polarity** — `polarity:pl-15` 5 · `polarity:pl-07` 4 · `polarity:pl-14` 4 · `polarity:pl-16` 4 · `polarity:pl-19` 4 · `polarity:pl-01` 3 · `polarity:pl-02` 3 · `polarity:pl-03` 3 · `polarity:pl-08` 3 · `polarity:pl-11` 3
**shape** — `shape:categories × two-series-mirrored` 2 · `shape:no-data × control` 2 · `shape:parts-of-whole` 2 · `shape:categories × five-number-summary` 1 · `shape:rows × measure-target-bands` 1 · `shape:periods × ohlc` 1 · `shape:bins × frequency` 1 · `shape:points × two-measures` 1 · `shape:no-data × page-regions` 1 · `shape:ancestor-path × links` 1
**intent** — `intent:change-over-time` 6 · `intent:comparison` 4 · `intent:composition` 3 · `intent:one-number` 3 · `intent:distribution` 2 · `intent:what-is-this` 2 · `intent:relationship` 1 · `intent:what-holds-the-page` 1 · `intent:where-am-i` 1 · `intent:what-can-i-do` 1
**guideline** — `guideline:1.4` 20 · `guideline:2.4` 20 · `guideline:2.5` 12 · `guideline:3.3` 10 · `guideline:1.2` 8 · `guideline:1.3` 8 · `guideline:3.2` 8 · `guideline:3.1` 6 · `guideline:4.1` 6 · `guideline:2.1` 4
**role** — `role:input` 27 · `role:chart-panel` 12 · `role:feedback` 11 · `role:arrangement` 8 · `role:action` 8 · `role:wayfinding` 8 · `role:record-list` 8 · `role:page-frame` 7 · `role:overlay` 7 · `role:headline-metric` 4
**principle** — `principle:operable` 21 · `principle:perceivable` 19 · `principle:understandable` 12 · `principle:robust` 3
**standard** — `standard:en-301-549` 55
**policy** — `policy:hsbc-digital-accessibility-framework` 55

---
## 2 — The 105 dangling edges

**Correction.** The conductor described the 105 as "mustNotNeighbour/yieldsTo, anaphoric when prose". That covers 53 of 105 (mustNotNeighbour 51 + yieldsTo 2). The real spread is EIGHT edge types over TWO kinds.

| source kind | edge type | n |
|---|---|---|
| component | `mustNotNeighbour` | 51 |
| component | `triggeredBy` | 22 |
| polarity | `hasParty` | 15 |
| component | `hasPart` | 8 |
| component | `groupsWith` | 4 |
| component | `yieldsTo` | 2 |
| component | `family` | 2 |
| component | `partial` | 1 |
| | **total** | **105** |

By family: base 90, uxprinciples 15. **All 105 carry a `$note`** — not one is a silent null.

### What the extractor does with them

- **base 90** — _build_kg_explorer.py:63-64 — `if not ref: edges.append({... "t": None ...}); continue`. The edge is KEPT with a None target and its $note.
- **ux 15** — _build_kg_explorer.py:366-367 — `if e.get("t") is None: link(e["s"], None, ...)` — s275-D2, a declared null carried, never dropped. (Same shape at :348-349 for the rule family, which currently emits 0.)
- **survives the filter** — _build_kg_explorer.py:374 — `edges = [e for e in edges if e["s"] in known and (e["t"] is None or e["t"] in known)]`; the `e["t"] is None or` clause is s274-D10, explicitly keeping nulls.
- **what the explorer does** — _build_kg_explorer.py:461 layout() builds its edge array from `if e["t"]` only, and :529 skips them for degree, and :536 live_edges requires `e["t"]`. So a dangling edge is CARRIED in the baked JSON, contributes NOTHING to degree, layout, islands or orphans, and is drawn by nothing. It is a note attached to a node, wearing an edge type.

The full list — source, type, note — is in `A1-measure.json` → `item2_dangling.edges` (105 entries).

---
## 3 — Islands and orphans, measured independently

| | explorer header | independent (full graph) |
|---|---|---|
| graph measured | 1,050 nodes / 1,552 edges | 3,897 nodes / 6,616 edges |
| connected components | 3 | **137** |
| islands (size > 1, excl. giant) | **2** | **37** |
| orphans (degree 0) | **0** | **99** |

Component size distribution (full graph): 3479×1 · 56×1 · 41×1 · 21×1 · 16×1 · 15×1 · 12×1 · 10×2 · 8×3 · 7×5 · 6×3 · 5×5 · 4×3 · 3×4 · 2×6 · 1×99

Giant component: **3,479 nodes** — evidence 843, ruling 571, artefact 561, pattern 380, rule 319, context 222, component 137, snippet 137, session 86, axe 64, sc 55, shape 23, ux 21, polarity 15, intent 14, guideline 13, role 12, principle 4, standard 1, policy 1

### The two islands the explorer DOES name (both real, both in the base graph)
- **size 8** — `pattern:dashboard-hero-with-headline-stats` · `pattern:landing-hero-with-primary-secondary-cta` · `pattern:marketing-banner-with-photo` · `context:dashboard-overview-page-tops` · `context:landing-pages` · `context:marketing-pages` · `component:hero-variants` · `snippet:Hero-variants.reference.html`
- **size 7** — `pattern:device-enrolment` · `pattern:log-on` · `pattern:register` · `pattern:step-up-verification` · `context:the-unauthenticated-app-entry-it-has-no-shell-above-it-by-definition` · `component:template-auth` · `snippet:Template-auth.reference.html`

### The 36 islands and 99 orphans it does not

| size | n | composition |
|---|---|---|
| 56 | 1 | rule 55, artefact 1 |
| 41 | 1 | rule 40, artefact 1 |
| 21 | 1 | rule 20, artefact 1 |
| 16 | 1 | evidence 9, artefact 4, ruling 3 |
| 15 | 1 | rule 14, artefact 1 |
| 12 | 1 | artefact 10, ruling 1, evidence 1 |
| 10 | 2 | evidence 8, artefact 6, ruling 5, session 1 |
| 8 | 3 | evidence 7, rule 7, artefact 6, ruling 3, session 1 |
| 7 | 5 | artefact 8, evidence 8, rule 6, ux 5, ruling 3, session 3, polarity 2 |
| 6 | 3 | artefact 5, evidence 4, ux 4, ruling 2, polarity 2, session 1 |
| 5 | 5 | artefact 7, ux 6, rule 4, polarity 4, ruling 2, evidence 2 |
| 4 | 3 | artefact 4, evidence 3, rule 3, ruling 2 |
| 3 | 4 | ux 6, polarity 3, ruling 1, artefact 1, evidence 1 |
| 2 | 6 | polarity 4, ux 4, artefact 2, rule 2 |

**Orphans: 99, every one a `ux:` node** ({'ux': 99}). Full id list in the JSON. No node of any other kind has degree 0.

### WHY the explorer prints `orphans 0`

**A DEFECT OF SCOPE, not of definition. The definition is sound; it is applied to the wrong graph.**

- **mechanism** — _build_kg_explorer.main() computes islands/orphans at lines 534-539 from `live_nodes`/`live_edges`, which derive from `nodes`/`edges` as they stand AFTER with_history() and BEFORE line 541 `xnodes, xedges, rep = extract_extra(...)`. The four additive families are appended to `nodes`/`edges` only at line 549 — eight lines too late. So the header measures the BASE component graph alone: 1,050 nodes / 1,552 live edges. That graph is genuinely 2 islands and 0 orphans (verified independently: no base node has degree 0).
- **scope miss** — 2,847 nodes (73.1%) and 5,079 edges (75.6%) are never offered to the component/orphan computation — governance, guidelines, guidelinerules and uxprinciples in their entirety.
- **consequence** — The header `islands 2 · orphans 0` is TRUE of the base graph and FALSE of the graph the page draws. Measured over everything: 137 components — 1 giant (3,479), 36 islands, 99 orphans. All 99 orphans are `ux:` nodes; all 99 sit in the uxprinciples family, which the computation cannot see.
- **second order** — place_extra() at :425-439 parks each family at a fixed offset regardless of connectivity, so a degree-0 ux: node is still DRAWN in the principle cloud rather than on the orphan arc that layout() reserves at :484-486. The page therefore has no visual tell either.
- **template line** — knowledge/_kg_explorer.template.html:364 renders `KG.orphans.length ? ... : "none"` — with an empty array the page prints the word "none".

---
## 4 — Edge-type census (51 types)

Consumer verdicts: **NO CONSUMER** 12 · **READ** 32 · **SCHEMA-ONLY** 7

*Method:* A type is READ if its quoted string literal appears in _validate_kg.py, _consult*, a designer-skills-v2 skill, system-manager/, another knowledge/*.py tool, or the explorer template JS. Files that MINT the type (the generators, the landed JSON, the source metas/rule/compliance/brain data) do not count as consumers. Some TOOL hits are English-word collisions inside quoted strings (`under`, `extends`, `bounds`, `family`, `partial`, `touches`) — the file lists are recorded per type so A2 can discount them; this measurement does not judge.

| type | n | dangling | src kind(s) → tgt kind(s) | minted by | from | join class | consumer |
|---|---|---|---|---|---|---|---|
| `answersIntent` | 28 |  | component→intent:28 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | STRUCTURAL 28 | SCHEMA-ONLY |
| `appliesTo` | 826 |  | sc→component:826 | `extract_extra() §B · sc_rules()` | compliance/rules/*.json → applies_to[] ↔ meta.name | STRUCTURAL 826 | NO CONSUMER |
| `boundBy` | 55 |  | sc→policy:55 | `extract_extra() §B · sc_rules()` | compliance/rules/*.json → sources.internal_policy_ref | STRUCTURAL 55 | NO CONSUMER |
| `bounds` | 1 |  | ruling→ruling:1 | `extract_extra() §A2 · ruling_edges()` | knowledge/_ruling_edges.json → edges[] | AUTHORED 1 | READ |
| `challengedBy` | 4 |  | polarity→ruling:4 | `extract_extra() §D ← gen_kg_principles.py` | brain/polarities.json → links[].type/.ref | STRUCTURAL 4 | READ |
| `checkedBy` | 68 |  | sc→axe:68 | `extract_extra() §B · sc_rules()` | compliance/rules/*.json → external_automatable_refs[].rule_id | STRUCTURAL 68 | NO CONSUMER |
| `cites` | 51 |  | rule→sc:51 | `extract_extra() §C ← gen_kg_rules.py` | rows[].rule TEXT → PAREN_RX/NUM_RX/INLINE_RX | PROSE 51 | READ |
| `commonPattern` | 421 |  | component→pattern:421 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | STRUCTURAL 421 | READ |
| `composedOf` | 5 |  | component→component:5 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | STRUCTURAL 5 | READ |
| `confirms` | 5 |  | ruling→ruling:5 | `extract_extra() §A2 · ruling_edges()` | knowledge/_ruling_edges.json → edges[] | AUTHORED 5 | READ |
| `consumes` | 70 |  | component→component:70 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | STRUCTURAL 70 | READ |
| `containedBy` | 88 |  | component→component:88 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | STRUCTURAL 88 | READ |
| `corrects` | 1 |  | ruling→ruling:1 | `extract_extra() §A2 · ruling_edges()` | knowledge/_ruling_edges.json → edges[] | AUTHORED 1 | READ |
| `definedIn` | 470 |  | rule→artefact:470 | `extract_extra() §C ← gen_kg_rules.py` | guidelines/_rules-index.json → rows[].file (filename join) | STRUCTURAL 470 | NO CONSUMER |
| `delegatesTo` | 1 |  | component→component:1 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | STRUCTURAL 1 | SCHEMA-ONLY |
| `drivesConsumer` | 5 |  | component→component:5 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | STRUCTURAL 5 | SCHEMA-ONLY |
| `enClause` | 55 |  | sc→standard:55 | `extract_extra() §B · sc_rules()` | compliance/rules/*.json → sources.en301549_clause | STRUCTURAL 55 | NO CONSUMER |
| `enacts` | 6 |  | ruling→ruling:6 | `extract_extra() §A2 · ruling_edges()` | knowledge/_ruling_edges.json → edges[] | AUTHORED 6 | READ |
| `enforcedBy` | 63 |  | rule→artefact:63 | `extract_extra() §C ← gen_kg_rules.py` | guidelines/_rules-index.json → rows[].gates[] | STRUCTURAL 63 | NO CONSUMER |
| `evidencedBy` | 1243 |  | ruling→evidence:1243 | `extract_extra() §A` | knowledge/_rulings.json → rulings[].evidence[] | STRUCTURAL 1243 | NO CONSUMER |
| `explainedBy` | 1 |  | polarity→ruling:1 | `extract_extra() §D ← gen_kg_principles.py` | brain/polarities.json → links[].type/.ref | STRUCTURAL 1 | READ |
| `extends` | 16 |  | ruling→ruling:16 | `extract_extra() §A2 · ruling_edges()` | knowledge/_ruling_edges.json → edges[] | AUTHORED 16 | READ |
| `family` | 12 | 2 | component→component:10 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | AUTHORED 2/STRUCTURAL 10 | READ |
| `flaggedBy` | 50 |  | snippet→rule:50 | `extract_extra() §C ← gen_kg_rules.py` | knowledge/_ADVISORY-SIGNALS.md → (file, rule id, line) | STRUCTURAL 50 | NO CONSUMER |
| `governedBy` | 28 |  | component→ruling:28 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | STRUCTURAL 28 | READ |
| `governs` | 1484 |  | ruling→artefact:1189, ruling→component:295 | `extract_extra() §A · gov_target()` | knowledge/_rulings.json → rulings[].governs[] | STRUCTURAL 1484 | READ |
| `groupsWith` | 8 | 4 | component→component:4 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | AUTHORED 4/STRUCTURAL 4 | READ |
| `hasDataShape` | 26 |  | component→shape:26 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | STRUCTURAL 26 | SCHEMA-ONLY |
| `hasPart` | 22 | 8 | component→component:14 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | AUTHORED 8/STRUCTURAL 14 | READ |
| `hasParty` | 68 | 15 | polarity→ux:51, polarity→ruling:2 | `extract_extra() §D ← gen_kg_principles.py` | brain/polarities.json → parties[].ref/.role | AUTHORED 15/STRUCTURAL 53 | NO CONSUMER |
| `mentions` | 240 |  | ruling→ruling:240 | `extract_extra() §mentions · MENTION_RX` | knowledge/_rulings.json → rulings[].says (free text) | PROSE 240 | READ |
| `mustNotNeighbour` | 70 | 51 | component→component:19 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | AUTHORED 51/STRUCTURAL 19 | READ |
| `narrows` | 2 |  | ruling→ruling:2 | `extract_extra() §A2 · ruling_edges()` | knowledge/_ruling_edges.json → edges[] | AUTHORED 2 | READ |
| `obeys` | 168 |  | component→rule:154, component→ux:14 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | STRUCTURAL 168 | SCHEMA-ONLY |
| `partial` | 6 | 1 | component→component:5 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | AUTHORED 1/STRUCTURAL 5 | READ |
| `providesRole` | 108 |  | component→role:108 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | STRUCTURAL 108 | SCHEMA-ONLY |
| `refines` | 4 |  | ruling→ruling:4 | `extract_extra() §A2 · ruling_edges()` | knowledge/_ruling_edges.json → edges[] | AUTHORED 4 | READ |
| `renderedBy` | 137 |  | component→snippet:137 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | STRUCTURAL 137 | READ |
| `resolvedBy` | 7 |  | polarity→ruling:7 | `extract_extra() §D ← gen_kg_principles.py` | brain/polarities.json → links[].type/.ref | STRUCTURAL 7 | READ |
| `retires` | 1 |  | ruling→ruling:1 | `extract_extra() §A2 · ruling_edges()` | knowledge/_ruling_edges.json → edges[] | AUTHORED 1 | READ |
| `reuses` | 2 |  | component→component:2 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | STRUCTURAL 2 | READ |
| `ruledIn` | 199 |  | ruling→session:199 | `extract_extra() §A · SESSION_RX` | knowledge/_rulings.json → rulings[].ruled | STRUCTURAL 199 | NO CONSUMER |
| `supersedes` | 3 |  | ruling→ruling:3 | `extract_extra() §A2 · ruling_edges()` | knowledge/_ruling_edges.json → edges[] | AUTHORED 3 | READ |
| `supersedesClause` | 9 |  | ruling→ruling:9 | `extract_extra() §A2 · ruling_edges()` | knowledge/_ruling_edges.json → edges[] | AUTHORED 9 | READ |
| `tensionWith` | 22 |  | ux→ux:22 | `extract_extra() §D ← gen_kg_principles.py` | brain/polarity-edges.json → from/to | STRUCTURAL 22 | NO CONSUMER |
| `touches` | 9 |  | polarity→ruling:9 | `extract_extra() §D ← gen_kg_principles.py` | brain/polarities.json → links[].type/.ref | STRUCTURAL 9 | READ |
| `triggeredBy` | 25 | 22 | component→component:3 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | AUTHORED 22/STRUCTURAL 3 | READ |
| `under` | 110 |  | sc→guideline:55, guideline→principle:55 | `extract_extra() §B · sc_rules()` | compliance/rules/*.json → sc (id split) | STRUCTURAL 110 | READ |
| `usedInContext` | 367 |  | component→context:367 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | STRUCTURAL 367 | READ |
| `verifiedBy` | 6 |  | sc→artefact:6 | `extract_extra() §B · sc_rules()` | compliance/graph-index.json → verification.by_sc[].script | STRUCTURAL 6 | NO CONSUMER |
| `yieldsTo` | 45 | 2 | component→component:43 | `extract()` | knowledge/components/*.meta.json → edges.<type>[].ref | AUTHORED 2/STRUCTURAL 43 | SCHEMA-ONLY |

### Types with NO CONSUMER (12 types, 3,125 edges)

Nothing outside the minting path names these strings — not the validator, not `_consult*`, not a skill, not `system-manager/`, not the explorer JS.

| type | edges |
|---|---|
| `evidencedBy` | 1243 |
| `appliesTo` | 826 |
| `definedIn` | 470 |
| `ruledIn` | 199 |
| `checkedBy` | 68 |
| `hasParty` | 68 |
| `enforcedBy` | 63 |
| `boundBy` | 55 |
| `enClause` | 55 |
| `flaggedBy` | 50 |
| `tensionWith` | 22 |
| `verifiedBy` | 6 |

### SCHEMA-ONLY (7 types, 381 edges)

Named only by `knowledge/components/meta.schema.json` — the schema permits them; no code reads them.

| type | edges |
|---|---|
| `obeys` | 168 |
| `providesRole` | 108 |
| `yieldsTo` | 45 |
| `answersIntent` | 28 |
| `hasDataShape` | 26 |
| `drivesConsumer` | 5 |
| `delegatesTo` | 1 |

### Synonym candidates — types sharing an endpoint-kind signature

| endpoint kinds | types | n types | edges |
|---|---|---|---|
| component/component | `containedBy`, `consumes`, `yieldsTo`, `mustNotNeighbour`, `hasPart`, `family`, `partial`, `composedOf`, `drivesConsumer`, `groupsWith`, `triggeredBy`, `reuses`, `delegatesTo` | 13 | 269 |
| ruling/ruling | `mentions`, `extends`, `supersedesClause`, `enacts`, `confirms`, `refines`, `supersedes`, `narrows`, `corrects`, `bounds`, `retires` | 11 | 288 |
| polarity/ruling | `touches`, `resolvedBy`, `challengedBy`, `explainedBy` | 4 | 21 |
| artefact/rule | `definedIn`, `enforcedBy` | 2 | 533 |

The conductor's suspected cluster `governs`/`governedBy`/`boundBy`/`enforcedBy`/`under`/`appliesTo` is **NOT** one cluster by endpoints: `governs` is ruling→artefact/component, `governedBy` component→ruling (the inverse, 28 vs 1,484), `boundBy` sc→policy, `enforcedBy` rule→artefact, `under` sc→guideline and guideline→principle, `appliesTo` sc→component. Six different endpoint signatures. The real concentrations are the 13-type `component→component` and 11-type `ruling→ruling` clusters above.

---
## 5 — Join class per edge

- **STRUCTURAL** — the target was resolved from a typed `ref`/id/path field or a filename — no human sentence was needed for the JOIN.
- **AUTHORED** — a human wrote the edge itself as a judgement (knowledge/_ruling_edges.json, ratified s267-D3), or wrote a sentence with no resolvable target at all (the 105 dangling notes).
- **PROSE** — the target was found by a regex over free text — `mentions` (MENTION_RX over rulings[].says) and `cites` (PAREN_RX/NUM_RX/INLINE_RX over the rule TEXT in guidelines/_rules-index.json).

| class | edges (all 6,721) | edges (6,616 live) |
|---|---|---|
| STRUCTURAL | 6,277 | 6,277 |
| AUTHORED | 153 | 48 |
| PROSE | 291 | 291 |

**The prose tier is 291 edges — 4.4% of live edges**: `mentions` 240 + `cites` 51. `mentions` is drawn dashed and carries an unratified `proposedType`; `cites` is minted as a hard rule->sc edge with no dashing and no proposal, i.e. a regex result presented with the same authority as a typed field.

**AUTHORED is 153**: 48 ratified ruling→ruling judgements (`_ruling_edges.json`, s267-D3) + the 105 dangling notes, which are a human sentence and nothing else.

### Per type (only types that are not purely STRUCTURAL)

| type | STRUCTURAL | AUTHORED | PROSE |
|---|---|---|---|
| `bounds` |  | 1 |  |
| `cites` |  |  | 51 |
| `confirms` |  | 5 |  |
| `corrects` |  | 1 |  |
| `enacts` |  | 6 |  |
| `extends` |  | 16 |  |
| `family` | 10 | 2 |  |
| `groupsWith` | 4 | 4 |  |
| `hasPart` | 14 | 8 |  |
| `hasParty` | 53 | 15 |  |
| `mentions` |  |  | 240 |
| `mustNotNeighbour` | 19 | 51 |  |
| `narrows` |  | 2 |  |
| `partial` | 5 | 1 |  |
| `refines` |  | 4 |  |
| `retires` |  | 1 |  |
| `supersedes` |  | 3 |  |
| `supersedesClause` |  | 9 |  |
| `triggeredBy` | 3 | 22 |  |
| `yieldsTo` | 43 | 2 |  |

### Authored-sentence carriage (a separate cut — 2,971 edges carry a human `$note`/`$why`)

| type | edges carrying a note |
|---|---|
| `governs` | 1484 |
| `usedInContext` | 366 |
| `mentions` | 240 |
| `ruledIn` | 199 |
| `containedBy` | 88 |
| `consumes` | 70 |
| `mustNotNeighbour` | 70 |
| `checkedBy` | 68 |
| `hasParty` | 68 |
| `boundBy` | 55 |
| `enClause` | 55 |
| `flaggedBy` | 50 |
| `triggeredBy` | 25 |
| `hasPart` | 22 |
| `extends` | 16 |
| `family` | 12 |
| `supersedesClause` | 9 |
| `touches` | 9 |
| `groupsWith` | 8 |
| `resolvedBy` | 7 |
| `enacts` | 6 |
| `partial` | 6 |
| `verifiedBy` | 6 |
| `composedOf` | 5 |
| `confirms` | 5 |
| `challengedBy` | 4 |
| `refines` | 4 |
| `supersedes` | 3 |
| `narrows` | 2 |
| `reuses` | 2 |
| `yieldsTo` | 2 |
| `bounds` | 1 |
| `corrects` | 1 |
| `delegatesTo` | 1 |
| `explainedBy` | 1 |
| `retires` | 1 |

---
## 6 — Kind × kind adjacency (20×20, directed)

| src ↓ / tgt → | evidence | artefact | ruling | rule | pattern | context | ux | component | snippet | session | axe | sc | polarity | shape | intent | guideline | role | principle | standard | policy |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **evidence** | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · |
| **artefact** | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · |
| **ruling** | 1243 | 1189 | 288 | · | · | · | · | 295 | · | 199 | · | · | · | · | · | · | · | · | · | · |
| **rule** | · | 533 | · | · | · | · | · | · | · | · | · | 51 | · | · | · | · | · | · | · | · |
| **pattern** | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · |
| **context** | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · |
| **ux** | · | · | · | · | · | · | 22 | · | · | · | · | · | · | · | · | · | · | · | · | · |
| **component** | · | · | 28 | 154 | 421 | 367 | 14 | 269 | 137 | · | · | · | · | 26 | 28 | · | 108 | · | · | · |
| **snippet** | · | · | · | 50 | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · |
| **session** | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · |
| **axe** | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · |
| **sc** | · | 6 | · | · | · | · | · | 826 | · | · | 68 | · | · | · | · | 55 | · | · | 55 | 55 |
| **polarity** | · | · | 23 | · | · | · | 51 | · | · | · | · | · | · | · | · | · | · | · | · | · |
| **shape** | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · |
| **intent** | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · |
| **guideline** | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | 55 | · | · |
| **role** | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · |
| **principle** | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · |
| **standard** | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · |
| **policy** | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · |

**28 of 400 cells are filled (7.0%); 372 are empty.** 27 of 210 undirected kind-pairs are connected at all.

**Pure sinks — 12 of the 20 kinds emit no edge at all:** `artefact`, `axe`, `context`, `evidence`, `intent`, `pattern`, `policy`, `principle`, `role`, `session`, `shape`, `standard`.

**Only 8 kinds are edge sources:** `component`, `guideline`, `polarity`, `rule`, `ruling`, `sc`, `snippet`, `ux`.

---
## 7 — Reachability seeds for A2 §1

*Method:* Undirected BFS (max depth 8) from 10 evenly-spaced start nodes (sorted by id) of the start kind to the NEAREST node of the target kind — ANY edge type. Plus, separately, whether the edge type the question actually names exists on that node, and corpus-wide coverage of that typed edge over ALL nodes of the start kind. A1 states path existence and length; it does NOT score the question — that is A2 §1.

| Q | question | start → target | ANY path (10 samples) | median len | the named edge type(s) | direct, 10 samples | **corpus coverage of that typed edge** |
|---|---|---|---|---|---|---|---|
| Q1 | what governs this component? | component → ruling | 10/10 | 1 | `governedBy`, `governs` | 7/10 | 107 / 137 = **78.1%** |
| Q2 | which components does this rule bind? | rule → component | 7/10 | 2 | `appliesTo`, `obeys` | 2/10 | 107 / 470 = **22.8%** |
| Q3 | what principle underlies this rule (and its grade)? | rule → ux | 7/10 | 4 | `obeys`, `tensionWith` | 0/10 | 0 / 470 = **0.0%** |
| Q4 | which rules conflict for this component? | component → rule | 10/10 | 2 | `obeys` | 0/10 | 10 / 137 = **7.3%** |
| Q5 | what did Dave rule about this and when? | component → session | 10/10 | 4 | `ruledIn` | 0/10 | 0 / 137 = **0.0%** |
| Q6 | what evidence supports that ruling? | ruling → evidence | 10/10 | 1 | `evidencedBy` | 10/10 | 593 / 593 = **100.0%** |
| Q7a | which components answer this intent? | intent → component | 10/10 | 1 | `answersIntent` | 10/10 | 14 / 14 = **100.0%** |
| Q7b | which components answer this data shape? | shape → component | 10/10 | 1 | `hasDataShape` | 10/10 | 23 / 23 = **100.0%** |
| Q8 | what must this component not sit next to? | component → component | 10/10 | 1 | `mustNotNeighbour` | 0/10 | 17 / 137 = **12.4%** |
| Q9 | what tokens does this component consume / what breaks? | component → **token** | **KIND ABSENT — 0/10** | — | `consumes` | 0/10 | **no `token:` node kind in the graph** |
| Q10a | which pattern is this component used in? | component → pattern | 10/10 | 1 | `commonPattern` | 10/10 | 137 / 137 = **100.0%** |
| Q10b | which context is this component used in? | component → context | 10/10 | 1 | `usedInContext` | 10/10 | 136 / 137 = **99.3%** |
| Q11 | what is the accessible-name / WCAG obligation here? | component → sc | 10/10 | 1 | `appliesTo`, `obeys` | 10/10 | 134 / 137 = **97.8%** |
| Q12 | what icon/logo/photo may I use here? | component → **asset** | **KIND ABSENT — 0/10** | — | — none exists — | 0/10 | **no `asset:` node kind in the graph** |

Per-start-node paths (the actual edge sequence for every sample) are in `A1-measure.json` → `item7_reachability_seeds.questions[].samples[].path`.

Notes on reading this table, mechanical only:
- **ANY path** is the loosest possible test — undirected, any edge type, up to 8 hops. A 10/10 with median length 4 is not the same answer as a 10/10 with median length 1.
- **Corpus coverage** is the honest number for A2: Q4 `obeys` reaches 10 of 137 components (7.3%) because only 10 metas carry `edges.obeys` at `bedf383` (s277-D1..D3 landed 4 chart metas; 168 obeys edges over 10 metas).
- Q5 `ruledIn` is ruling→session, never component→session, so its component coverage is 0 by construction; the ANY path exists at length 4 (component → ruling → session).
- Q9 and Q12 have **no target node kind at all**: there is no `token:` node and no `asset:`/`icon:`/`photo:` node anywhere in the 20 kinds.

