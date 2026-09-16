# A2V — VERIFY — the KG audit's figures re-driven, the judgement judged
#277 · 2026-09-16 · lane A2V (Fable) · verifies A2 (`e958e6d`) + A3 (`3ca6301`) + the page `REVIEW-kg-audit-2026-09-16-v1.html` · graph pinned at `bedf383` (`git diff bedf383 HEAD -- knowledge/` is empty; tree dirty only in `notes/_REHEARSAL-LOG.jsonl` and `notes/_dream/_GRADE-DECISIONS.jsonl`, declared) · READ-ONLY; the only writes are this folder · every figure re-derived by `_verify_figures.py` (imports `_build_kg_explorer.extract()`/`extract_extra()` only; `main()` never called; no `gen_kg_edges.py`, no `_build_all.py`) → `verify-figures.json`; token counts by tiktoken `cl100k_base` in the same shell.

## Counts

**Figures: 22 GREEN · 9 AMBER · 3 RED.** Judgement (six decisions): D-1 AMBER (survives split, not as one letter) · D-2 AMBER · D-3 GREEN (carries the RED figure) · D-4 GREEN · D-5 AMBER · D-6 GREEN. Sources: 7 of 8 spot-checked hold, 1 AMBER.

**Verdict: PRESENT WITH THESE 5 FIXES** (listed at the end; two are one-line number corrections, three are card rewrites).

---

## Part 1 — the figures, re-driven

Every number the page carries, with the command that re-derived it. "page" = the decision cards, hero stats and Parts A–E of the HTML; "audit" = `A2-AUDIT.md`.

| # | figure on the page | re-derived | grade | command / note |
|---|---|---|---|---|
| F1 | 3,897 nodes · 6,616 edges · 51 types · 20 kinds · 105 declared nulls | 3,897 · 6,616 live · 51 · 20 · 105 | GREEN | `extract()+extract_extra()`, `t is None` split |
| F2 | 6 / 2 / 4 = 50% answer rate | the twelve per-question facts underneath re-checked (F3–F12); the scoring is judgement and is defensible | GREEN | see note under F12 |
| F3 | Q1 `governs` reaches 107 of 137 components | 107 / 30 not | GREEN | `{t for governs} ∩ component` |
| F4 | Q7 `answersIntent` 14/14 · `hasDataShape` 23/23 · `providesRole` 108/137 | 28 edges → 14/14 intents · 26 edges → 23/23 shapes · 108 comps | GREEN | |
| F5 | Q8 "19 resolved on **17** components + 51 nulls" | 19 live `mustNotNeighbour` on **15** components; 51 nulls | AMBER | `len({e.s for mustNotNeighbour live})` = 15. Page Part A and audit §1 say 17. Correct to 15. |
| F6 | Q11 `appliesTo` 134/137 | 134 | GREEN | |
| F7 | Q5 `date` 593/593 · `ruledIn` 199 · session-in-id 392 of 394 | 593 · 199 · 392/394 | GREEN | |
| F8 | Q3 rule→ux 0 of 470 · Q4 no `conflictsWith` | rule out-types = {definedIn 470, cites 51, enforcedBy 63}; no rule→ux, no conflictsWith in the 51 | GREEN | |
| F9 | **432 of 593** rulings govern only files · 99 components only · 62 both — "with the extractor's own gov_target() test" | by the extractor's own live `governs` targets: **435 system · 99 design · 59 both** | AMBER | A2's `is_comp()` counts any `*.reference.html` string as a component target; the extractor's `gov_target()` sends the glob `knowledge/snippets/*.reference.html` (s116-D3, s121-D1, s258-D3) to `artefact:`. Δ3 either way; "three-quarters / one quarter" holds (73% / 27% → 73% / 27%). Fix the attribution sentence or the number, not both. Part B's "the 161 design-scoped rulings" becomes 158 under the extractor's test. |
| F10 | **50 of 59** BLOCKING rules bind no component | 59 BLOCKING; 9 obeyed; **50** unbound by `obeys` | GREEN | `blocking − {t for obeys→rule}`. Note for D-2: 4 of the 50 reach a component in two typed hops (rule `cites` sc `appliesTo` component); 46 reach nothing by any path. The card's "bind nothing from the agent's seat" is true for direct binding; the 2-hop path is the one A3 refuses to *mint* from, but it exists as a path. |
| F11 | **316 of 470** rules have no scope (audit §2 table, §7 G1, commit message) vs **363 of 470** (page Part C/D) | 470 − 107 distinct rules obeyed = **363** | RED | 316 = 470 − 154 `obeys` *edges*, not distinct rules (chart-bar/pie/line/donut cite the same family rules). The page is right (363); `A2-AUDIT.md` §2, §7 G1 and the `e958e6d` commit message carry 316. Correct the audit and note the commit message is wrong. |
| F12 | 26 of 34 guideline files unreached by `obeys`; 350 rules in them; copy 55 · tone 40 · colour 34 · type 32 · icons 31 · neuro 26 | 8 reached / 26 not / 350 / 55 · 40 · 34 · 32 · 31 · 26 | GREEN | The *count* holds. The card's wording "8 of 34 — the files named after a component" is off by one: s276-D5 says exactly 7 files are named after a component; the 8th reached is `data-visualisation.md`, the family file s277-D3 attached. "bind a facet every component has" is a judgement, not a measurement — 52 of the 350 are accessibility rules and 51 of those cite an sc that `appliesTo` named components, i.e. they are not facet rules, they are already component-addressed by the compliance corpus. |
| F13 | 12 consumer-less types · **3,125** edges · 47% | the same 12 types over the **live** graph = **3,110** edges = 47.0% | AMBER | 3,125 counts `hasParty` at 68, which includes its 15 declared nulls; the 6,616 denominator excludes nulls. 3,110 of 6,616 (47.0%) or 3,125 of 6,721 (46.5%) — not 3,125 of 6,616. Percentage survives; the integer on the hero stat and D-3 lede does not. |
| F14 | `governs` 1,484 / `governedBy` 28 · `mentions` 240 · `cites` 51 | 1,484 / 28 · 240 · 51 | GREEN | |
| F15 | 55 sc · 52 accessibility rules · 20 standards-family principles · **0** cross-links | 55 · 52 · 20 (wcag22 11, coga 6, en301549 1, eaa 1, aria-apg 1) · 0 ux→sc/rule/guideline/principle | GREEN | 51 of the 52 accessibility rules `cites` an sc (the "0" is ux↔sc/rule only; the card says so). |
| F16 | ux orphans 99 of 145; A-grade `pr-klm`, `pr-steering` at 0; 30 polarities | 99 · klm 0, steering 0 · 30 | GREEN | degree over live edges; the only degree-0 kind is `ux` |
| F17 | 341 of 380 patterns, 176 of 222 contexts at degree 1 | 341 · 176 | GREEN | |
| F18 | tokens block in 135 of 137 metas · 316 distinct refs · 10 live token files · top groups text/rag/tertiary/form/border-radius/icon | 135 · 316 · 10 (colour, elevation, icon-scale, layout, motion, opacity, semantic-colour, spacing, typography, typography-composites) · same top-12, carrying 70% of 1,587 group-mentions | GREEN | "932 leaves" is the ruling's own number (s269-D3); today's live-file leaf count is 792 (`$value` walk over the 10 files; 932 was over all 21 files incl. `-pre-s141`). Not a page defect — the card quotes the ruling. |
| F19 | 29 metas without `provides` · 21 with `governedBy` · 127 without `obeys` · 10 with `obeys` | 29 · 21 · 127 · 10 | GREEN | |
| F20 | 5 meta edge types drawn by no chip | answersIntent, hasDataShape, obeys, providesRole, yieldsTo | GREEN | `FAMILY` map in the template vs schema `edges` keys |
| F21 | D-3: "read the metas — 137 files, **about 730K tokens**" | 138 files · **1.6 MB** · **414,755** cl100k tokens (137 non-EXAMPLE: 414,184) | RED | The 730K is `_compose_slice.py`'s docstring line 13 ("138 files, 3.0 MB, ~730K"), which is wrong on both bytes (`cat *.meta.json | wc -c` = 1,606,913) and tokens. A2's own `A2-measure.json` carries `library_tokens: 414184` and A3's table carries 414,755 — the page still prints 730K. Correct to "about 415K". The audit §6 and Part D G2 say the same 730K. |
| F22 | D-3: `_compose_slice.py` "self-measured 19,113 tokens against 111,468 for the metas it replaces" | re-run: 21,253 vs 114,745 for 31 metas (5.4×) on a dashboard task; 5,735 vs 14,703 for 4 metas (2.56×) on a bar-chart task; library 414,184 | AMBER | Task-dependent; A2's task string is not recorded anywhere (the number has no source outside A2's files). The ratio (≈5–6×) holds; the card should say "on a 31-meta task" and name the task, or print the range. |
| F23 | 10 live token files (D-5) | 10 | GREEN | |
| F24 | D-4: 13 component→component types · 11 ruling→ruling types · s267-D3 retyped 20 by hand | 13 · 11 (10 authored + `mentions`) · s267-D3 `ruled`: "20 are RETYPED" | GREEN | |
| F25 | D-3 lede: "nine of the twelve [consumer-less types] answer a designer's question directly" | evidencedBy (Q6), appliesTo (Q11), ruledIn (Q5), definedIn (Q2, weakly) — **four**; checkedBy/enforcedBy/flaggedBy/boundBy/enClause/verifiedBy/hasParty/tensionWith answer none of the twelve as written | AMBER | Audit §4 itself names four in its parenthetical. Say "four". |
| F26 | A3 today-cost table: `_rulings.json` 232,648 · metas 414,755 (median 2,576) · `canon.css` 588,102 · `tokens/**` 528,168 · compliance 27,009 · icons manifest 40,943 · photography manifest 66,529 · rules-index + ux 102,363 · explorer 953,148 · `_consult-index` 109,270 · whole graph 798,152 | 232,648 · 414,755 (2,574.5) · 588,102 · 528,168 · 27,009 · 40,943 · 66,529 · 49,450 + 52,913 · 953,148 · 109,270 · 798,152 (bytes 2,470,180 vs A3's 2,465,653 — serialiser whitespace) | GREEN | every file figure reproduces to the token |
| F27 | A3: "≈ 2.6M tokens today vs ≈ 2.1K slices" (D-6 lede: "instead of a 200K-token file read") | the per-question column sums to 2,603,214 ✓; the graph slices for Q1 average 242 tokens on the same five components (A3: 305 — label field) | AMBER | The 2.6M is a *sum of per-question costs* that counts `_rulings.json` three times (Q1, Q5, Q6) and the metas twice (Q2, Q7); the de-duplicated union of files is ≈1.5M. The "1,200 : 1" ratio becomes ≈700 : 1. Conclusion unchanged; the number should be labelled "summed per question, not de-duplicated". |
| F28 | A3: Q9 costs **595,242** tokens today | = meta 5,286 + `canon.css` 588,102 + `_GRAPH-REPORT.md` 1,854 ✓ arithmetically | AMBER | The premise is wrong: the meta's `tokens` block already *names* the tokens a component consumes (typed, 135 metas), and `tokens/_blast-radius.json` (20,049 tokens, exists, generated 2026-06-18 — stale) answers "what breaks". An honest today-cost for Q9 is ≈25K, not 595K. A3's ranking rule ("today-cost saved × questions touched") puts TOKENS at rank 4 partly on this number; with 25K it drops on cost-saved and stays on "no node kind". D-6(d)'s plain sentence "instead of a 595K-token read" carries it onto the page. |
| F29 | A3: "12 canonical questions ≈ 2,140 slice tokens" | order of magnitude reproduces (Q1 242 avg, 1-hop mean ≈1,550 on my five vs A3's 901 — A3 used a different five) | GREEN | |
| F30 | page: "Every integer read at build time from the two measurement files; none typed" | `_build_page.py` reads A1/A2 JSON; but 19,113 / 111,468 / 414,184 are typed into `_measure_a2.py` (`slice_tokens: 19113` literal), and `after_d2_d5_answered: 9` is a literal | AMBER | The receipts line overclaims: three integers are hand-typed into the measurement file, then "read". |
| F31 | D-2: "137 × 350 sentences" for the obeys route | 137 × 350 = 47,950 — but that is the all-to-all upper bound, not the authored cost; s277-D3 measured the real per-family authoring at 16 of 19 rules × 3 components with 3 exceptions | GREEN (arithmetic) | rhetorical; see D-2 below |
| F32 | D-1: "the five edge types no chip draws today" | 5 ✓ | GREEN | |
| F33 | D-6: A3's TOKENS "~950 nodes / ~3,000 edges" | live-file leaves 792; all-file leaves 932 (#269); `_blast-radius.json` `tokens_defined` 1,043 | GREEN as A3's estimate | it is a leaf-count by any reading — see the s269-D3 call |
| F34 | hero: "0 files under knowledge/ written" | `git status` shows nothing under `knowledge/` | GREEN | |

### The three REDs, in full
- **RED F11 — "316 of 470 rules have no scope."** `A2-AUDIT.md` §2 (rule row), §7 G1, and the `e958e6d` commit message ("rule 316 no scope"). Re-derived: 470 rules − 107 distinct rules with an `obeys` in-edge = **363**. 316 is 470 − 154, and 154 is the number of `obeys`→rule *edges* (the four chart metas cite the same `dv-*` family rules, so 154 edges reach 107 rules). The HTML page already prints 363 (Parts C and D). **Correction: 363 in the audit; the commit message stands as wrong and is noted here.**
- **RED F21 — "read the metas — 137 files, about 730K tokens"** (D-3 lede; audit §6; Part D G2). Re-derived with tiktoken cl100k over `knowledge/components/*.meta.json`: 138 files, 1,606,913 bytes, **414,755 tokens** (137 non-EXAMPLE: 414,184). The 730K is copied from `_compose_slice.py`'s docstring, which is stale on both bytes and tokens; A2's own `A2-measure.json` holds 414,184 and A3's table 414,755. **Correction: "about 415K tokens (1.6 MB)". The D-3 argument is unchanged — 415K still does not fit beside a design task.**
- **RED (judgement, D-1) — s274-D11 is cited for a clause it does not contain.** D-1(a) "Supersedes the 'behind its own chip' clauses of s274-D11 and s275-D6 by name"; D-1(c) "Loses what s274-D11 and s275-D6 wanted visible". The `ruled` text of **s274-D11** is: "THE RULE NODES LIVE IN knowledge/_rule_nodes.json AND THE EXPLORER READER LANDS IN THE SAME COMMIT — at no point does an unread file exist in the repo … An instrument without a consumer is refused." There is **no chip clause** in s274-D11; the phrase "behind its own chip" occurs only in **s275-D6**. What s274-D11 wants is a *reader*, not a chip — which is D-3's principle, not D-1's. **Correction: D-1 touches s275-D6 only; s274-D11 is the ruling D-3 enacts, and should be cited there.** (And a sub-chip is still "its own chip" — even s275-D6 arguably needs no superseding clause; say "refined", not "superseded".)

### The AMBERs, in full (with corrections)
- **F5** 17 → **15** components carry a resolved `mustNotNeighbour` (Part A Q8, audit §1).
- **F9** 432/62 → **435/59** under the extractor's own `gov_target()` (three rulings govern the snippet glob); keep 432 only if the sentence stops claiming the extractor's test. Part B "161 design-scoped" → 158 or 161 accordingly.
- **F12** "8 of 34 — the files named after a component" → "7 named after a component (s276-D5) + the data-visualisation family file (s277-D3)"; and the lede's "350 rules that bind a facet" should carve out the 52 accessibility rules, 51 of which already cite an sc that names components.
- **F13** 3,125 → **3,110** live edges (47.0%), or state the denominator as 6,721 incl. nulls.
- **F22** 19,113 / 111,468 → name the task and the meta count, or print the measured range (2.6×–5.4× on two tasks re-run this session).
- **F25** "nine of the twelve" → **four** (evidencedBy, appliesTo, ruledIn, definedIn).
- **F27** label A3's 2.6M as "summed per question; the de-duplicated read is ≈1.5M".
- **F28** Q9's 595K → ≈25K (meta + `_blast-radius.json`); D-6(d)'s plain sentence to match; A3's rank-4 TOKENS keeps its place on "no node kind", not on cost.
- **F30** the receipts line: three integers in `A2-measure.json` are literals, not measurements — say so or measure them.

---

## Part 2 — the judgement, judged

### D-1 — one graph, three views by force, the Codex, the Constitution

**The strongest case against D-1(a).**

1. **It is four decisions wearing one letter.** (i) three views by force instead of five by wave; (ii) the record is named *Codex*; (iii) every ruling gets a derived `scope`; (iv) "the dozen fences" are written once as a *Constitution* with a precedence ladder. Dave asked a question about three words; the card does not let him pick a word without also buying the view re-cut, the scope derivation and an unwritten document. Option (b) folds two of the three words into one line ("Codex (or system management)") so it is not exclusive with (a) either — (a) contains (b)'s rename. A one-letter answer to D-1 is not readable back as a decision on any one of the four.
2. **The "precedence ladder" is a new normative claim with no ruling behind it.** Part B states it as fact: "law, then ruling, then BLOCKING, then ADVISORY, then the principles". Nothing in `_rulings.json` orders a Dave ruling against a WCAG criterion or a BLOCKING HSBC rule; s277-D3 flagged one such conflict (dv-pie-009 vs `chart-pie.when`) and explicitly did *not* resolve it. A ladder that would decide it is the s274-D12 shape — a plausible structure presented as if it were the measured conclusion. "The dozen fences" are not enumerated (four are named); asking for a letter on "written once as the Constitution" is a blank cheque.
3. **"Force" leaks at the first ratified edge.** The Explanation layer is defined as "never an obligation"; but s276-D3 ratified `obeys` → `ux:` grade-A laws with a `$why`, and 14 such edges exist today (measured: `obeys_to_ux` = 14). The metas *obey* principles in the ratified vocabulary. So either the six A-grade laws are governance (and the layer is by *grade*, not by kind) or the `obeys→ux` edges are mislabelled. The card does not say which.
4. **The 432 "system management" reading over-counts.** Derived `scope` from `governs[]` targets classifies s269-D3 (token grain), s274-D12 (no regex rule→component), s275-D4 (no name-match joins), s270-D2 (the DESK vocabulary) as *system* rulings — they govern `.py`/`.json`/`.html` — although they are the rulings that shape the designer brain and that this very page argues from. "Three-quarters of it is how the system was built" treats a proxy as a fact. The number is real; the sentence is not.
5. **The evidence does not select the cure.** The measurements (a11y in three families, 0 cross-links, 432/593) show the layers are ingestion waves. Any re-cut fixes that — by topic (Dave's instinct), by force (A2's), by provenance. "By force" is a taxonomy preference argued well in prose, not derived from a measurement; the card should say so rather than "the cut that fixes it is by force".
6. **It changes nothing.** A2's own §0: "today, nothing, under any of them". A relabelling of an HTML explorer's chips is the lightest decision on the page and is carried as "the one with the most weight" — that framing belongs to D-3.

**Does it survive?** **Partly.** The core — one graph in storage (already true), views as labels, the WCAG corpus + rules + design rulings shown as one obligation layer, storage untouched — survives all six points: it is cheap, reversible, and the a11y-in-three-places symptom is real and measured. What does not survive as part of a single letter: the precedence ladder (must be marked *A2's proposal, Dave's to author*), the Constitution (name the fences or drop the word), the derived `scope` (say "proxy from governs[] targets; 435/99/59"), and the Codex naming (its own line — Dave asked for a word). Point 3 needs one sentence on the card: the six A-grade laws sit in governance by grade, or `obeys→ux` is renamed.

**Rulings D-1 names, checked against `ruled`:**
- s274-D11 — RED, see above: no chip clause; it is the "reader in the same commit / instrument without a consumer" ruling. Belongs to D-3.
- s275-D6 — says "behind its own chip"; a sub-chip under Design governance is still its own chip. "Refined", not "superseded". AMBER.
- s275-D4 — says the 20 standards-family principles land with no cross-link and "the joins are AUTHORED later in a named lane". D-1(a) claims to be that lane *and* claims "no node id, no edge type changes". Both cannot hold: the joins are new authored edges (Part D G3 prices "20 authored `restatesSC` links" — a new edge type, a vocabulary change under s269-D1/#75). AMBER — internal contradiction on the card; either D-1(a) touches the vocabulary or it is not the s275-D4 lane.
- s269-D2 — `ux:` prefix kept: correct as read.
- s274-D7/D8, s275-D1..D3, s270-D2, s276-D3, s277-D1..D3, s267-D3 — "untouched": correct as read, with the point-3 caveat on s276-D3's `obeys→ux`.

### D-2 — a `scope` per guideline file
Recommendation right in direction; the card under-declares its shape. D-2(a) derives rule→component applicability for 350 rules with no sentence per pair — a structural join keyed on a 34-row authored table. That is the s277-D3(a) shape ("all 19 on each — refused as the s274-D12 shape wearing a sentence") lifted to file grain, and s277-D3's own measurement is the precision evidence the card omits: two blind lanes found 3 of 19 family rules did **not** bind all three charts. At "universal" scope, tone-of-voice alone yields 40 × 137 = 5,480 derived bindings with the same expected exception rate. The card says "Consistent with s274-D12 (no inference)" — it is inference by scope, honest inference, and should be named as such with the "declared escape" made concrete (an `obeysNot` / exception row per file). (a) ⊇ (b), so the options are not exclusive; fine for a "which route" card. AMBER; recommendation stands with the shape declared.

### D-3 — wire the reader
Right, and the one decision that changes what the agent does. Carries the RED F21 (730K → 415K) and AMBER F13/F25. s274-D11 belongs here (see D-1). Options exclusive. GREEN on judgement.

### D-4 — the reading vocabulary
Right; storage untouched; no ruling touched; figures GREEN (F24). The 12 verbs are a proposal and are labelled as one. Options exclusive. GREEN.

### D-5 — tokens at tier grain — and the s269-D3 call
**s269-D3, `ruled`:** "TOKENS ENTER THE GRAPH AT TIER GRAIN - semantic versus primitive - and NEVER as 932 leaf nodes. The leaf-per-token shape was priced and rejected as a graph that cannot be read." It is a CONDUCTOR'S READING of Dave's "I think your recommendations for the 6 look good", and the #269 proposal's own words for the pick were: "Tokens: file, tier, or leaf? Tier (semantic vs primitive) is my pick — it answers the blast-radius question without 932 nodes." The proposal listed *file* (21 nodes) and *tier* as **different** options.

**Who is right.** **A2, on the question that matters.** A3's TOKENS is "≈ 950 nodes … at TIER grain (semantic / component-type / foundation), primitives as leaves" — 950 nodes is a leaf count under any reading (792 live-file leaves, 932 all-file, 1,043 in `_blast-radius.json`); calling each leaf's tier a "grain" does not change the node count. It is the shape s269-D3 refused and would need s269-D3 superseded by id, exactly as A2 says. **But A2 is not literally at tier grain either.** "The 10 live token files — or the dozen groups" is the proposal's *file* option (rejected in favour of tier) or a group grain. The reading the repo already practises is `_compose_slice.py`'s: "a slice names the token GROUP and its tier, never the leaves" — group + tier, ~128 groups. D-5(a) should say "group grain with its tier, as `_compose_slice.py` already reads it (≈128 groups, top 12 carrying 70% of references)", not "10 files", and should not say "consistent with s269-D3" without adding "the ruling's word is tier; group-with-tier is how the repo has operationalised it since #269". AMBER; recommendation stands.

### D-6 — which augmentation first
A2's line — ASK is D-3 by another name — is right; the two lanes converging on SHAPES = Part C is a real signal. The five options are a ranking, not exclusive alternatives, and the card says "first", so that is fine. The cross-card inconsistency (D-5(a) with D-6(d)) is flagged in the why; better to grey (d) out under D-5(a). F28's 595K rides onto the page in (d)'s plain sentence — fix with F28. GREEN on judgement.

### s274-D12 shape check across the six
Nothing on the page mints an edge from prose. The one item that is a plausible structure dressed as evidence is D-1's precedence ladder / Constitution (Part 2, D-1 point 2). D-2(a) is inference by declared scope — honest if labelled. D-1's "by force" is preference argued as conclusion.

---

## Part 3 — A3's 33 sources, 8 spot-checked this session
| # | fetched | holds? |
|---|---|---|
| S1 | arXiv API 2404.16130 | GREEN — title and "community summaries for all groups of closely related entities" present |
| S7 | arXiv 2501.13956 | GREEN — the fetch cache reports A3's own fetch ~29 min earlier in this sandbox; abstract page live |
| S14 | arXiv 2410.20724 | GREEN — SubgraphRAG; "directional structural distances" in abstract |
| S16 | W3C SHACL | GREEN — "a language for validating RDF graphs against a set of conditions", Rec. 20 July 2017 |
| S21 | designtokens.org/tr/drafts/format/ | GREEN — §3.8 "A design token's value can be a reference to another token. The same value can have multiple names or aliases"; `$extends` "syntactic sugar for JSON Schema's $ref"; draft dated 08 September 2026, latest published 2025.10 |
| S22 | W3C CG post 28 Oct 2025 | GREEN — "first stable version of the Design Tokens Specification (2025.10)" |
| S26 | arXiv 2604.11364 | GREEN — quoted abstract phrases verbatim (v2, 12 Jun 2026) |
| S28 | arXiv 2604.14572 | GREEN — Corpus2Skill; "hierarchical skill directory … progressively finer summaries" |
| S32 | arXiv 2608.02356 | GREEN — SkillTrace (v2, 4 Aug 2026) |
| S31 | github VoltAgent/awesome-ai-agent-papers | **AMBER** — the README contains neither "progressive disclosure" nor a "≈200-token top level"; A3 labels it "(search summary, 2026)". A URL that does not carry the claim is not a source; drop S31 or cite the Agent Skills doc that does. |

(Nine fetched; S31 counted as the one that fails.)

---

## Part 4 — the page, read as Dave
Renders cleanly at 1280 both themes and at 390 (screenshots opened; the stats grid and hero hold). Decisions sit above evidence; recommendation first on each. **D-1 is not clear enough for a one-letter answer**: the (a) paragraph is ~120 words carrying four commitments (views · Codex · scope · Constitution) and (b) bundles two of Dave's three words into one option. A reader who wants "three views, but call it case law and don't write a constitution yet" has no letter. **Rewrite D-1 as: (a) three views by force / (b) five by wave, relabelled / (c) none — storage untouched in all three — plus one line under it: "the name of the record: codex · case law · system management · constitution (one word)", and move the precedence ladder and the Constitution out of the options into the why, marked as A2's proposal for Dave to author.** The rest of the page reads at one letter each.

---

## Verdict — PRESENT WITH THESE 5 FIXES
1. **D-3 / §6 / G2:** 730K → **about 415K tokens (1.6 MB)** — RED F21.
2. **D-1:** remove s274-D11 from the "supersedes" and "loses what … wanted visible" sentences (it has no chip clause; cite it under D-3); change s275-D6 "supersedes" → "refines"; resolve the s275-D4 contradiction (either D-1(a) adds 20 authored edges with a new type, or it is not the named lane) — RED (judgement).
3. **D-1 rewrite** as one letter for the views + one word for the name; precedence ladder and Constitution moved to the why as proposals; one sentence on the 14 `obeys→ux` edges (Part 2 point 3); 432 → 435/59 or drop "the extractor's own test" — AMBER F9.
4. **Small integers:** Q8 17 → 15 components (F5); 3,125 → 3,110 or state the denominator (F13); "nine of the twelve" → four (F25); "8 files named after a component" → 7 + the family file (F12); A2-AUDIT.md 316 → 363 (F11, page already right).
5. **D-5 / D-6:** D-5(a) worded as group-with-tier per `_compose_slice.py`, with s269-D3's word "tier" quoted; D-6(d) and A3's Q9 row: 595K → ≈25K (meta + `_blast-radius.json`), and A3's 2.6M labelled "summed per question, ≈1.5M de-duplicated" (F27/F28); drop S31.

Nothing here reverses a recommendation. D-3 is the decision; D-1 is the one that needs the rewrite before Dave can answer it in a letter.

## Receipts
`_verify_figures.py` → `verify-figures.json` (this folder). tiktoken cl100k_base 0.14.0. `_compose_slice.build_slice()` called in-process for two tasks (prints nothing, writes nothing; `git status` unchanged under `knowledge/`). Rulings read from `knowledge/_rulings.json` `ruled`/`says` fields: s269-D1..D5, s269-D9, s270-D2, s273-D2, s274-D9..D12, s275-D4..D6, s276-D1, s276-D3, s276-D5, s277-D3, s267-D3. Web: the nine URLs above. Nothing under `knowledge/` written; `main()` not called.
