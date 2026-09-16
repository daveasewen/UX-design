# A2 — JUDGE — structure and layers of the knowledge graph, from the agent's seat
#277 · 2026-09-16 · lane A2 (Fable) · briefs `BRIEF.md` + `BRIEF-A2-A3.md` · reads `A1-MEASURE.md` / `A1-measure.json` (`13a4cf2`) · graph pinned at `bedf383` · READ-ONLY, nothing enacted, nothing under `knowledge/` written

**The test applied to every finding:** does it change what an autonomous design agent on rails would do in its 30-second decision, compared with a good HSBC designer who had the same context to hand? A gap that never changes a decision is low. A gap that leaves the agent guessing where the designer would have known is high.

**The headline, in one line.** The graph answers **6 of the 12 designer questions** (50%), half-answers 2, and cannot answer 4 — and at design time the agent reaches almost none of it, because no code path on the compose route reads the graph at all. The layers are the commit history wearing chips; the biggest single gap is that **50 of the 59 BLOCKING HSBC rules bind no component**, not because the edges are missing but because those rules bind a *facet* (colour, type, copy, icons), and the graph has no way to say so.

---

## §0 THE LAYERS — Dave's question, answered directly

### Plain prose

Dave asked three things: are five layers the right number; should they stay layered-and-conjoined (chips over one graph) or become one graph or fewer; and is his instinct right that *"all the accessibility nodes should be design governance nodes, and what we have as governance should be something like 'system constitution' or 'codex' or 'system management'"*.

**His instinct is right about the symptom and half right about the cure.** The five layers as built are not five kinds of knowledge. They are five *ingestion waves*: the base wiring (#266), the rulings (#266 v1.2), the WCAG corpus (#266 v1.2), the 470 HSBC rules (#274), the 145 UX principles (#275). Each got a chip because each landed in its own lane under its own ruling — the chips record how the graph was built, not how a designer thinks. The proof is accessibility itself: it is smeared across *three* of the five layers today — the 55 WCAG success criteria sit in "guidelines", the 52 rules from the eight `accessibility-*.md` files sit in "guideline rules", and 20 principles from the standards families (fam-wcag22, fam-coga, fam-en301549, fam-eaa, fam-aria-apg) sit in "UX principles" — with **zero edges between the three holdings** (s275-D4 declared exactly this and deferred the joins to a named lane). A designer does not think of WCAG, the HSBC accessibility guideline and the COGA principle as three subjects. They are one obligation with three provenances.

So the right cut is not by *topic* (accessibility) and not by *ingestion wave*. It is by **force** — what a node does to a design decision:

1. **The system** — what exists: components, snippets, patterns, contexts, roles, intents, shapes; tokens and assets when they land. The agent *chooses* from this layer.
2. **Design governance** — what a design must or should do: the WCAG criteria (external law), the 470 HSBC rules (internal standard, with destiny BLOCKING/ADVISORY/REVIEW/TASTE), and the *design-scoped* rulings (Dave's case law on components). Three provenances, one precedence ladder. The agent *obeys* this layer. Accessibility lives here entirely — that is the half of Dave's instinct that is right.
3. **Explanation** — why: the 145 graded UX principles and the 30 polarities, plus the evidence trail. Never an obligation; the agent *consults* this layer when two obligations pull against each other or when nothing governs.

And the ruling record — 593 rulings, 886 evidence nodes, 92 sessions, 618 artefacts — is not a layer of the designer brain at all. It is the **codex**: the system's own case law, with receipts. Measured: **432 of the 593 rulings govern only files, scripts and notes** (lanes, gates, releases — system management); **99 govern only components** (design case law); 62 govern both. So what is called "governance" today is 73% the record of how the system was built and 27% design precedent. Dave's instinct that "the categorisation might not be correct" is measured, not felt.

**On his three words.** *System constitution* names the wrong size of thing: a constitution is small, founding and rarely amended, and this record grows by ten rulings a session; the word fits the handful of fences everything else defers to (fence 3 of #261, the two-red law s151-D1, nam-002, "an instrument without a consumer is refused") — a precedence ladder of perhaps a dozen lines, which does not exist as a document today and should. *System management* names the 432 operational rulings well and the 161 design rulings badly; it is a *scope* on a ruling, not the name of the record. *Codex* fits the record: a bound, ordered collection of rulings that are cited by id, each with its evidence and its session, superseding and refining one another — which is exactly what `_ruling_edges.json` already draws. The one risk is the name collision with a well-known AI coding product; if that bothers Dave, "case law" says the same thing in plainer English. **Proposal: the record is the Codex; each ruling carries a `scope` (design | system | both) derived from what it governs; the design-scoped rulings appear inside the Design governance view; the dozen fences are written down once as the Constitution — the precedence ladder.**

**What the agent would do differently at design time under each organisation.** Honestly: *today, nothing*, under any of them — because the compose path does not read the graph (§6). The chips live in an HTML explorer that a human browses. The layer question only bites the moment a design-time reader exists (D-3), and then it bites hard: a reader over five ingestion families has to know four stores and 51 edge types to assemble "what must this component do"; a reader over three force layers asks one question — *give me the obligations for this component, in precedence order* — and gets WCAG first, then the design rulings, then BLOCKING rules, then ADVISORY, with the principles behind them on request. That is the 30-second answer. So the layer decision and the "wire the reader" decision are one decision wearing two names, and the page puts them side by side as D-1 and D-3.

**Layered-and-conjoined, or one graph?** One graph, one node-id grammar, one closed vocabulary — that is already true in storage and should stay true (every node lives in one `nodes` list; the `fam` field is a label). The layers are *views*. Three views by force, not five by wave; the provenance inside Design governance shown as sub-chips (standard · guideline · ruling) so nothing that s274-D11 and s275-D6 wanted visible becomes invisible.

### Technical prose

- **The five as built** (`knowledge/_build_kg_explorer.py` §A–§D; `knowledge/_kg_explorer.template.html:164-201`): base nodes carry no `fam`; the four additive families carry `fam ∈ {governance, guidelines, guidelinerules, uxprinciples}`; the template's `FAMILY` map assigns each *edge type* to one of eight chips (structure · usage · render · rules · governance · guidelines · guidelinerules · uxprinciples) and `famOn` opens with the four additive chips OFF (`:201`). Five edge types are in no chip at all — `obeys`, `providesRole`, `answersIntent`, `hasDataShape`, `yieldsTo` — so they are never drawn (the s276 declared gap, `VERSION` note at `:29`).
- **Accessibility across three families**, measured at `bedf383`: guidelines family — sc 55, guideline 13, principle 4, standard 1, policy 1, axe 64; guidelinerules family — rules with `file` in `accessibility-*.md` = 52 (client-side-dev 15, interaction-design 14, content-authoring 12, visual-design 7, IA 1, QA 1, framework 1, hub 1), of which 51 carry a `cites` edge to an sc: node (the only rules that do); uxprinciples family — `family ∈ {fam-wcag22 11, fam-coga 6, fam-en301549 1, fam-eaa 1, fam-aria-apg 1}` = 20 ux: nodes, 0 edges to any sc:/guideline:/principle: node (s275-D4).
- **Ruling scope**, measured over `knowledge/_rulings.json` `governs[]` with the extractor's own `gov_target()` test: component-only 99 · artefact-only 432 · mixed 62 · none 0. Artefact targets by kind: `.py` 301, `.json` 124, `.md` 112, `notes/` 96, `.html` 73, `tokens/` 63, `canon/` 41, `guidelines/` 18, other 358.
- **Session is recoverable for 392 of the 394 rulings with no `ruledIn` edge**: `SESSION_RX` (`:143`) reads only the `ruled` field, which holds `#N` for 199 rulings and the ruling *text* for the rest; but 558 of 593 ids are `sNNN-Dn`, so the session is in the id. `date` is present on 593/593.
- **Rulings a re-layering touches** (none undone; each superseded by a named clause if D-1(a) is taken): `s274-D11` and `s275-D6` ("behind its own chip" — the chip becomes a sub-chip of Design governance; the reader-in-the-same-commit clause is untouched); `s275-D4` (the 20 standards-family principles land with no cross-link, "AUTHORED later in a named lane" — D-1(a) *is* that named lane's brief, not a reversal); `s269-D2` (the `ux:` prefix — kept, no node id changes); `s274-D7`, `s274-D8`, `s275-D1..D3`, `s270-D2`, `s276-D3`, `s277-D1..D3` (node kinds and edge types — untouched; a view re-cut changes `fam` labels and the template's `FAMILY`/`FAMLABEL`/`famOn`, never a node id or an edge type); `s267-D3` (the explorer reads `_ruling_edges.json` — untouched).

### Recommendation
**One graph, three views by force (System · Design governance · Explanation), the ruling record named the Codex with a derived `scope` on every ruling, and the dozen fences written once as the Constitution — D-1(a).**

---

## §1 The 12 canonical questions — the headline

### Plain prose

These are the questions a designer asks mid-task, in the order they come up: what am I choosing from, what must it do, what did we decide last time, what goes with it, what goes wrong. Each is scored on whether the graph can answer it **by a path**, then on whether the agent could **reach that answer at design time today**. The two numbers are far apart, and the second is the one that matters for a hyper-designer.

**The graph answers 6 of 12** — governance of a component, the ruling's evidence and date, the intent and data-shape lookups, pattern and context, and the WCAG obligation. It **half-answers 2** — which components a rule binds (only for the 8 component-named files) and what a component must not sit next to (51 of the 70 statements have no component to point at). It **cannot answer 4** — the principle under a rule, the conflicts between rules, the tokens a component consumes, and the icon or logo it may use. Two of those four are already in flight (icons and logos, `5520d43`, waiting on a ruling; tokens, ruled at tier grain by s269-D3 and never built).

**At design time the agent reaches about 4 of 12**, because the compose path reads the metas and the pack does not ship the rulings, the rule nodes or the principle nodes (§6).

### Technical prose (A1 §7 seeds, judged)

| Q | the designer's question | graph verdict | path · coverage | design-time today | what closes it |
|---|---|---|---|---|---|
| Q1 | what governs this component? | **ANSWERED** | `governs` ruling→component, len 1, 107/137 (78%); the other 30 are true absences, not gaps | PARTIAL — only the 28 `governedBy` on 21 metas ship; the 295 `governs` live in `_rulings.json`, empty in the pack | D-3 |
| Q2 | which components does this rule bind? | **PARTIAL** | `obeys` inverse, 154 edges, 10 metas, 8 of 34 files; the 26 foundation files (copy 95, colour 34, type 32, icons/pictograms 31, neurodiversity 26 …) bind by *facet* and the graph cannot say so | NO | D-2 — a `scope` per guideline file (universal · facet · component) |
| Q3 | what principle underlies this rule, and its grade? | **UNANSWERABLE** | rule→ux 0/470; no edge type exists in either direction | NO | new authored type `restsOn` (rule → ux); start with the 59 BLOCKING rules against the six A-grade laws (s269-D5, s275-D5 extend) |
| Q4 | which rules conflict for this component? | **UNANSWERABLE** | needs component→rule (7.3%) *and* rule↔rule `conflictsWith`, which does not exist; the one known conflict (dv-pie-009 "maximum 6" vs `chart-pie.when` "≤ 5 parts") is prose in s277-D3 | NO | authored `conflictsWith` (rule ↔ rule | meta field), rare and Dave's |
| Q5 | what did Dave rule about this, and when? | **ANSWERED** | governs len 1 + `date` 593/593; `ruledIn` 199/593 but the session is in the id for 392 of the other 394 | NO — rulings do not ship | extractor reads the id (5 lines); D-3 |
| Q6 | what evidence supports that ruling? | **ANSWERED** | `evidencedBy` len 1, 593/593 | NO | D-3 |
| Q7 | which components answer this intent / data shape? | **ANSWERED** | `answersIntent` 14/14, `hasDataShape` 23/23 — chart scope only (26 metas); the rest is `providesRole` 108/137 + `roles.json` `when` | YES (roles.json ships) | 29 components without a role — the s273-D2 held sets |
| Q8 | what must this component not sit next to? | **PARTIAL** | `mustNotNeighbour` 19 resolved on 17 components + 51 declared nulls that are anti-pattern *statements* ("a raw `<select>` for the same choice"), not components | YES — the skill reads `relationships.mustNotNeighbour` prose, which is richer than the graph | keep the nulls (s270-D2/s274-D10 shape); the statement is the content |
| Q9 | what tokens does this component consume, and what breaks if I change one? | **UNANSWERABLE** | no `token:` kind; yet `tokens` is a typed block in 135/137 metas (316 distinct refs; 12 groups — `text/`, `rag/`, `tertiary/`, `form/`, `border-radius/`, `icon/` … — carry most of them; 10 live token files) and `tokens/_blast-radius.json` already computes reach | NO | D-5 — tokens at file/group grain, `bindsToken` structural |
| Q10 | which pattern / context is this used in? | **ANSWERED** | len 1, 100% / 99.3% — but 341 of 380 patterns and 176 of 222 contexts are named by exactly one component: labels, not compositions | YES (metas) | §2 — a pattern of one is a tag |
| Q11 | what is the accessible-name / WCAG obligation here? | **ANSWERED** | `appliesTo` 134/137 + the meta's `accessibility.relatedSC` typed block; the *obligation text* is on the sc: node and in `check.description` | YES (compliance ships) | — |
| Q12 | what icon / logo / photo may I use here? | **UNANSWERABLE** | no asset kind; lane RI proposes `usesIcon` 371 / `usesLogo` 18 (`5520d43`), photography ruled as manifest row (s269-D4) and unbuilt | PARTIAL (icons manifest ships, unlinked) | RI's ruling; then photography |

**Answer rate: 6 ANSWERED · 2 PARTIAL · 4 UNANSWERABLE = 50% (67% counting partial).** With RI landed and Q5 read from the id: 7 / 2 / 3. With D-2 and D-5: 9 / 1 / 2. Design-time reach today: Q7, Q8, Q10, Q11 = 4/12.

### Recommendation
**Treat 50% as the baseline and the design-time 4/12 as the number to move — D-2, D-3 and D-5 take the graph to 9/12 and the agent to the same figure.**

---

## §2 Per-kind intent — what each kind is FOR, and its minimum

### Plain prose

"Orphan" only means something against a stated minimum, and the minimum depends on what the node is for. A snippet with one edge is perfect: it is a leaf that renders one component. A rule with one edge is useless: it is defined in a file and binds nothing, so the agent can never apply it. The table says, per kind, what the node does in a designer's head, what the least connectivity is that lets it do that, and the measured gap. Three kinds fail their own purpose at scale: **rule** (316 of 470 have no scope at all), **pattern** (341 of 380 are one-component labels) and **ux** (99 of 145 touch nothing, including two of the six A-grade laws).

### Technical prose

| kind | n | what it is for | minimum | gap (measured) |
|---|---|---|---|---|
| component | 137 | the thing chosen | `renderedBy` 1 · `usedInContext` ≥1 · `providesRole` ≥1 · ≥1 obligation | 0 at deg 0; 29 without a role (s273-D2 held sets); 127 without an `obeys` |
| snippet | 137 | the render | 1 (`renderedBy`) | none — 87 at deg 1 is correct |
| pattern | 380 | a named composition of ≥2 components | ≥2 `commonPattern` in-edges, or steps | **341 at deg 1** — labels, not patterns |
| context | 222 | where a component lives | ≥2 in-edges | **176 at deg 1** |
| role / intent / shape | 12 / 14 / 23 | the DESK address (s270-D2) | ≥1 provider | none; 8 intents at deg 1 are single-provider, fine |
| ruling | 593 | a decision, cited by id | ≥1 `governs` + ≥1 `evidencedBy` + a session | 394 without `ruledIn` (392 recoverable from the id); no `scope` |
| evidence | 886 | the receipt | 1 | none by intent; but 886 ids are the evidence *string* — 4 near-duplicate chat citations sit as separate nodes |
| artefact | 618 | a governed file | 1 | none; note `artefact:knowledge/guidelines/*.md` is both a `governs` target and a `definedIn` target — the natural scope hub for D-2 |
| session | 92 | when | ≥1 | none |
| rule | 470 | an obligation the agent applies | `definedIn` 1 + **a scope** (component, facet or universal) | **316 with no scope; 50 of 59 BLOCKING bind nothing** |
| sc | 55 | the legal obligation | `under` + `appliesTo` ≥1 | none (all deg ≥3) |
| guideline / principle / standard / policy | 13/4/1/1 | the WCAG taxonomy | ≥1 | none |
| axe | 64 | the automatable check | 1 (`checkedBy`) | none by intent; no consumer reads it |
| ux | 145 | the explanation, graded | ≥1 (a rule or component resting on it, or a polarity) | **99 at deg 0**; A-grade `pr-klm`, `pr-steering` at 0; the 20 standards-family principles have 0 links to sc: |
| polarity | 30 | a tension between two principles | `hasParty` 2 | 5 at deg ≤1 — the 15 declared-stub parties (s275-D3 shape, correct) |

### Recommendation
**Adopt these minimums as the graph's stated intent; the gaps that change a design decision are rule (D-2), ux (Q3's `restsOn`) and pattern (decide whether a one-component pattern is a node or a tag — §7 G8).**

---

## §3 Silent structure — the 105 dangling edges and the explorer's false zero

### Plain prose

The 105 edges with no target are not silent: every one carries a sentence, and the rulings s270-D2, s274-D10 and s275-D2 say exactly this — an unresolvable target stays `ref: null` with a note, never invented, never dropped. Read one by one they are four different things wearing edge types. Fifty-one `mustNotNeighbour` nulls are **anti-pattern statements** ("a raw `<select>` for the same choice", "a second chart re-using data/series/1 for different data") — they name a *shape*, not a component, and the shape is the content; a designer would say the same sentence. Twenty-two `triggeredBy` nulls name **events** ("form submission", "session state") — a kind the graph does not have and does not need yet. Eight `hasPart` nulls name **sub-parts** of data-grid and hero that are not components. Fifteen `hasParty` nulls are the polarity **stubs** s275-D3 declared. Only the two `yieldsTo` nulls are true anaphora ("it", "both") and both are resolvable by a human reading the `when` sentence, not by a rule.

The explorer's `islands 2 · orphans 0` is a scope defect A1 has already dissected: the count is taken over the 1,050-node base before the four families are appended. It should be fixed and it is not a decision.

### Technical prose

Dangling by type (A1 §2): `mustNotNeighbour` 51 · `triggeredBy` 22 · `hasParty` 15 · `hasPart` 8 · `groupsWith` 4 · `yieldsTo` 2 · `family` 2 · `partial` 1. The two anaphoric `yieldsTo`: `component:Chart-boxplot` ("it when variables = 1 and the bin shape is the claim" — the sibling is `Chart-histogram`, named two clauses earlier in the same `when`) and `component:Chart-bullet` ("both when no target exists" — the two siblings are the bar and the KPI named in the sentence). Resolvable by an author in two minutes; not by a regex without re-creating s274-D12's false positive. Explorer defect: `_build_kg_explorer.py:534-539` vs `:549`; the fix is to compute after the append, and to let `place_extra()` (`:425-439`) route a degree-0 family node to the orphan arc (`:484-486`).

### Recommendation
**Keep all 105 as declared nulls (ruled shape); resolve the two anaphora by hand in the next meta touch; fix the explorer's scope in the next explorer touch — no decision needed.**

---

## §4 Edge-type efficiency — 51 types, 12 with no consumer

### Plain prose

Fifty-one edge types is not expensive for the agent, because the agent never sees them: the compose skill names three (`mustNotNeighbour`, `groupsWith`, `obeys`). It is expensive for the *system* — every type is a line in the validator, a colour in the explorer, a sentence in a skill that has not been written. The real finding is not synonyms. It is that **12 types carrying 3,125 edges — 47% of the graph — are read by nothing**, and 7 more are permitted by the schema and read by nothing. The reason is not that the types are wrong; it is that the reader they were built for — a design-time consult — does not exist. Retiring them would be retiring the answer to Q1, Q2, Q5, Q6 and Q11 because nobody has asked yet. The efficient move is the consumer, not the cull.

On synonyms, A1's endpoint evidence kills the conductor's suspected cluster (`governs`/`boundBy`/`enforcedBy`/`under`/`appliesTo` are six different signatures) and finds the real concentrations: 13 component→component types and 11 ruling→ruling types. Both were ratified deliberately (s267-D3 retyped 20 edges by hand into those 11). A storage merge would undo a ruling to save nothing the agent pays for. What the agent needs is a **reading vocabulary** — the dozen verbs it will ever be told — mapped onto the storage types, which touches no ruling.

### Technical prose

- **No consumer** (A1 §4): `evidencedBy` 1243 · `appliesTo` 826 · `definedIn` 470 · `ruledIn` 199 · `checkedBy` 68 · `hasParty` 68 · `enforcedBy` 63 · `boundBy` 55 · `enClause` 55 · `flaggedBy` 50 · `tensionWith` 22 · `verifiedBy` 6. Nine of the twelve answer a canonical question directly (Q1 via appliesTo/Q11, Q2, Q5, Q6). **Schema-only**: `obeys` 168, `providesRole` 108, `yieldsTo` 45, `answersIntent` 28, `hasDataShape` 26, `drivesConsumer` 5, `delegatesTo` 1 — and these five are also the ones the explorer's `FAMILY` map omits, so they are drawn by nothing either.
- **True inverse pair**: only `governs` (1,484) / `governedBy` (28). The 28 are the metas' own citations (21 metas); the 1,484 are the rulings' `governs[]`. Not a synonym — a two-ended authored join. Keep both; a reader should union them.
- **Reading vocabulary proposed** (agent-facing, 12 verbs, storage untouched): *is-a* (family/partial/reuses) · *contains* (containedBy/hasPart/composedOf/consumes/drivesConsumer/delegatesTo) · *sits-with* (groupsWith) · *must-not-sit-with* (mustNotNeighbour) · *yields-to* · *renders-as* (renderedBy) · *lives-in* (usedInContext/commonPattern) · *provides / answers* (providesRole/answersIntent/hasDataShape) · *must* (appliesTo, obeys→BLOCKING, design-scoped governs) · *should* (obeys→ADVISORY/REVIEW/TASTE) · *rests-on* (obeys→ux, tensionWith, the future restsOn) · *decided* (governs/governedBy/evidencedBy/ruledIn + the 11 ruling→ruling verbs). Everything else (definedIn, enforcedBy, flaggedBy, checkedBy, verifiedBy, boundBy, enClause, under, cites, mentions) is machinery the reader uses and the agent never names.
- **Rulings a storage merge would touch**: `s267-D3` (11 ruling→ruling types, ratified by hand), `s270-D2` (providesRole/answersIntent/hasDataShape/yieldsTo), `s274-D8` (definedIn/cites/enforcedBy/flaggedBy), `s275-D2` (six ux types), `s276-D3` (obeys). A reading map touches none.

### Recommendation
**No storage merge; publish the 12-verb reading vocabulary as the agent's contract and give the 12 consumer-less types their consumer (D-3, D-4).**

---

## §5 The prose tier — 291 edges

### Plain prose

Two edge types come from reading free text. `mentions` (240) is a regex over what a ruling *says*, drawn dashed, carrying a proposed verb that Dave has not ratified — exactly the advisory shape s267-D3 set, and it should stay that way. `cites` (51) is different in kind: the regex reads a citation the rule's *author wrote* — "(SC 1.4.3)" in the rule text — so it is a parsed citation, not an inference about meaning. It is drawn solid and A1 is right that it wears the same authority as a typed field; but the author did type it, in prose. The honest fix is to *say* what it is (join class "parsed citation") rather than to demote it. Nothing in the prose tier should be promoted to authored by a generator, and nothing should go.

### Technical prose

`mentions` 240 (`MENTION_RX` over `rulings[].says`, `_build_kg_explorer.py:252-291`; `proposedType` 10 verbs; suppressed where s267-D3 authored the pair). `cites` 51 (`gen_kg_rules.py` PAREN_RX/NUM_RX/INLINE_RX over `_rules-index.json` rule text; all 51 from the five `accessibility-*.md` files; 0 nulls since s276-D1..D4 ingested the 17 missing criteria). Against s274-D12 (no rule→component by regex) and s276-D5 (name-match tier not widened): neither type is a rule→component join, so neither is the refused shape; `cites` targets an sc: id the author wrote in full.

### Recommendation
**Keep both; tag `cites` "parsed citation" in the census and the explorer legend; never widen the regex tier (s274-D12, s276-D5 hold).**

---

## §6 Structure and efficiency overall — the graph from the agent's seat

### Plain prose

**Is a star around components the right shape?** For the 30-second decision, yes. The designer's questions all pass through the component — choose it, check what it must do, check what it sits with, render it. A star with the component at the centre (median degree 19, max 61) is the right lookup shape, and the two hubs beside it — `sc:` (median 7) and `role:` (median 8) — are the right entry points for "what must" and "what for".

What the star lacks is a **middle layer above the component for obligations**. Today an obligation reaches a component only by an edge *to that component*: `appliesTo` (WCAG names components in `applies_to`), `obeys` (a meta cites a rule with a sentence), `governs` (a ruling names a meta file). That works for the 8 guideline files named after a component. It cannot work for the other 26 files — copywriting, tone of voice, colour, typography, icons, motion, neurodiversity — because those rules bind a *facet* that every component has. A designer knows the tone-of-voice rules apply to every label on the screen; the graph would need 137 × 95 authored sentences to say so, and s277-D3 already priced that shape and refused it. The fix is not a family node (s277-D3 option c, correctly declined — nothing could carry it) and not a regex (s274-D12). It is one attribute on each of the 34 guideline files — its **scope**: universal, or a facet keyed to a token group the metas already name (`text/`, `icon/`, `rag/`, `border-radius/` …), or a component. Thirty-four rows, authored once, and applicability becomes a structural join through the `tokens` block that 135 metas already carry. That is D-2, and it is the single change that moves the most rules into the agent's reach.

Below the component, the graph also lacks **real composition**. 341 of 380 patterns are one component's label. The one place a real composition is recorded — the bento template's groups under s245-D7 — is carried as `groupsWith` notes. Persona and job-to-be-done nodes above patterns are parked (P-269-9) and rightly so; nothing can be relied on yet.

**What the graph looks like from the agent's seat today.** It does not look like a graph. The compose skill says "read the metas": 138 files, 3.0 MB, roughly 730K tokens if read whole; the pack ships the metas, `roles.json`, the 470-rule index and the WCAG rules, and ships `_rulings.json` *empty by design*. The rule nodes, principle nodes, ruling edges and the explorer do not ship. One tool already does the right thing — `knowledge/_compose_slice.py` turns a task sentence into roles → components → edges → BLOCKING rules → anti-neighbours → rulings at a measured 19K tokens against 111K for the 31 metas it replaces — and it is marked `PROPOSAL, ADVISORY, NOT WIRED`, with the wiring named as Dave's to rule. Until it is wired, every edge type in this audit is an instrument without a consumer, which is the exact thing s274-D11 refuses for a file. That is D-3.

**What is missing that a designer could consult** (the parked families, by P-id): the Common Toolkit Figma specs (P-273-1, access is the obstacle), tokens (s269-D3 ruled, P-269-7 tripwire, unbuilt — D-5), photography (s269-D4 ruled, unbuilt), fonts (no manifest at all — #269 family 9), personas/JTBD (P-269-9), content standards and lifecycle status (s269-D6 in scope, unbuilt), the temporal validity window (P-269-6). Copy tone is *not* missing: 95 rules in `copywriting.md` and `tone-of-voice.md` are in the graph — they are the rules D-2 makes reachable.

### Technical prose

Hubs: component median 19 / max 61 (`button` 61, `chart-bar` 59); sc median 7 / max 111 (`sc:4.1.2`); role median 8 / max 27 (`role:input`). Adjacency 28/400 filled; 12 kinds are pure sinks — correct for leaves (snippet, evidence, artefact, session, axe, intent, shape, role), wrong for `pattern` and `context` only if they are meant as compositions. Compose path: `apollo-spider/skills/generate-from-canon/SKILL.md` names `edges.groupsWith` (`:136`) and `mustNotNeighbour` (`:137, :161`); `check-against-design-system/SKILL.md:15` names `obeys`; `:130-131` records that routing off the graph "is Dave's to rule". `knowledge/_compose_slice.py` (VERSION 0.1, docstring `:12-24`) reads `roles.json`, `chart-intents.json`, `_rules-index.json`, the metas, `_rulings.json`, `_ruling_edges.json`, `_consult-lexicon.json`, `typography-composites.json`, `icons.manifest.json`; traverses `commonPattern`, `usedInContext`, `renderedBy`, `containedBy`, `hasPart`, `consumes`, `composedOf`, `family`, `groupsWith`, `mustNotNeighbour`, `governedBy`; self-measures 19,113 tokens vs 111,468 (5.83×) vs 414,184 for the whole library. It does not read `_rule_nodes.json` or `_ux_principle_nodes.json`. Pack (`apollo-spider/dist/Apollo-Spider-v1.0.13.zip`): ships metas, roles, compliance, `_rules-index.json`, `_graph_edges.py` without its inputs; does not ship `_consult.py`, `_rule_nodes.json`, `_ux_principle_nodes.json`, the live rulings.

### Recommendation
**Keep the star; add the scope layer above the component (D-2) and wire the one reader that exists (D-3); leave composition and personas parked under their P-ids.**

---

## §7 Ranked gap list — with cost

Each: what the designer would have known · what the agent guesses today · what closes it · join class · cost · rulings and P-ids touched. Ranked by how often it changes a 30-second decision.

| # | gap | designer knows | agent guesses | closes with | join | cost | touches |
|---|---|---|---|---|---|---|---|
| **G1** | **50 of 59 BLOCKING rules bind no component; 316 of 470 rules have no scope** | copy, colour, type and icon rules apply to every component that has text, colour, type, icons | reads the rule index flat, or nothing | a `scope` attribute per guideline file (34 rows): universal · facet:<token group> · component:<slug>; applicability derived through `metas.tokens` | authored once + structural | 34 rows · 1 reader (~40 lines) · 1 lane | s274-D9 (attribute not hub — consistent) · s274-D12, s276-D5 (obeys stays; no regex) · s277-D3 (option c not built — this carries what a family node would) · P-274-3 (enacted) |
| **G2** | **no design-time reader — 47% of edges have no consumer; the agent reads 730K tokens of metas** | what to look up, and in what order | reads files whole | wire `_compose_slice.py` as generate's step 1, reading by force layer | — | 1 lane to read rule/ux stores + pack cut | s274-D11 principle · pack manifest rulings (s269-D9 pins `_search_core`) · apollo-spider SKILL `:130` |
| **G3** | the layers are ingestion waves; accessibility sits in three with 0 links | one obligation, three provenances | n/a today (explorer only) | three views by force; `scope` on rulings; 20 authored `restatesSC` links for the standards-family principles | template + authored | 1 lane (template + 20 sentences) | s274-D11, s275-D6 (chip clauses superseded) · s275-D4 (the named lane) · s269-D2 kept |
| **G4** | **no token kind (Q9)** | which tokens a component consumes and the blast radius of a change | reads `tokens` block prose | `token:` at tier grain — the 10 live token files, or the ~12 groups that carry most references — + `bindsToken` from `metas.tokens`; reach from `_blast-radius.json` | structural | 10–20 nodes · ~1,000–1,500 edges · 1 lane | s269-D3 (tier grain — consistent) · P-269-7 |
| **G5** | **no asset kind (Q12)** | which icon, which lockup, on which theme | reads the manifest by hand | lane RI's 688 nodes / 1,299 edges (`5520d43`) | structural | ruled + one land lane | s269-D1 step 4 · RI-1..RI-4 (its own page) · s230-D2 |
| **G6** | rule → principle absent (Q3) | why the rule exists and how strong the evidence is | nothing | authored `restsOn` (rule → ux); 59 BLOCKING rules × six A-grade laws first | authored | ≤ 60 sentences · 1 lane | s269-D5, s275-D5 (extends the "both halves" lane) |
| **G7** | conflicts between rules absent (Q4) | the 5-vs-6 slice cap, and which wins | guesses, or copies the meta | authored `conflictsWith` + the precedence ladder (Constitution) | authored | rare; the known one first | s277-D3 (flagged, unresolved) |
| **G8** | 341 patterns / 176 contexts are one-component labels | a pattern is a composition | reads 380 names | decide: a pattern with <2 members is a tag attribute, or gets members | decision | 0 build | `_nodes-pattern.json` registration; no ruling |
| **G9** | 394 rulings lack a session edge; no `scope` on rulings | when, and whether it is a design ruling | n/a | read the session from the `sNNN-` id; derive `scope` from `governs[]` | structural | ~10 lines | none |
| **G10** | explorer reports `islands 2 · orphans 0` over the base graph only | — | — | compute after the append | fix | 8 lines | none |
| **G11** | 99 orphan principles incl. 2 A-grade laws | the law exists | n/a | G6 + s275-D5's component citations | authored | inside G6 | s275-D5 |
| **G12** | Figma specs, photography, fonts, personas/JTBD, content standard, lifecycle, temporal window | the spec, the photo, the persona | nothing | parked | — | — | P-273-1 · s269-D4 · P-269-9 · s269-D6 · P-269-6 |

---

## §8 The decisions page — six, recommendation first

`REVIEW-kg-audit-2026-09-16-v1.html`, decisions above evidence, export in the `charts-decisions-2026-09-15-v2.json` shape. One-liners:

- **D-1 — The layers.** (a) one graph, three views by force — System · Design governance · Explanation — the record named the Codex with a derived `scope`, the dozen fences written once as the Constitution; (b) keep the five ingestion chips, rename "governance" only; (c) one undifferentiated graph, no chips. **Recommend (a).**
- **D-2 — How the 470 rules reach components.** (a) a `scope` attribute per guideline file (34 rows), applicability derived through the token groups the metas already name, `obeys` kept for the specific and the escape; (b) continue the per-meta `obeys` route file by file; (c) a chart/family node (s277-D3 c). **Recommend (a).**
- **D-3 — Wire the design-time reader.** (a) `_compose_slice.py` becomes generate's step 1 at the next pack cut, reading the rule and principle stores by force layer; (b) keep read-the-metas and accept that 12 edge types are explorer-only; (c) retire the 12 consumer-less types. **Recommend (a).**
- **D-4 — The vocabulary.** (a) a 12-verb reading vocabulary for the agent over the 51 storage types, storage untouched, no ruling touched; (b) merge in storage (touches s267-D3, s270-D2, s274-D8, s275-D2); (c) leave. **Recommend (a).**
- **D-5 — Tokens enter the graph.** (a) tier grain now — the 10 live token files (or the ~12 heavy groups) as `token:` nodes and `bindsToken` from `metas.tokens`, the join key D-2 uses; (b) wait for the P-269-7 token-report tripwire; (c) leaf grain (refused s269-D3). **Recommend (a).**
- **D-6 — Which augmentation first.** Fed from lane A3's `A3-shortlist.json` (ASK · CLOSURE · SHAPES · TOKENS · NEIGHBOURS, `3ca6301`). A2's line on it: ASK is D-3 by another name — one lane, two verbs; SHAPES is §2 written into the validator; A3's TOKENS reaches D-5's gap at ~950 nodes, the leaf grain s269-D3 refused, so the two lanes agree on the need and disagree on the grain — D-5(a) keeps tier grain and takes A3's `aliasOf` onto the tier nodes; A3's shape would need s269-D3 superseded by id.

---

## §9 What I would refuse

The attractive fixes that are the s274-D12 shape — plausible edges manufactured by a machine and presented as knowledge:

1. **Rule → component by any text match** — the 27 regex candidates, name-in-prose, shingle overlap. s274-D12 and s276-D5 refused it; RI's icons lane measured the same route at 1,947 junk pairs. Still refused.
2. **Principle → sc by family name** (`fam-wcag22` → `principle:perceivable`). It is a name match; s275-D4 refused it. The 20 links are authored under D-1 or not at all.
3. **Token leaves as nodes** — 932 leaf nodes, s269-D3 refused; a graph that cannot be read.
4. **A family node without a carrier** — s277-D3 (c). D-2's scope attribute answers the need without a new kind.
5. **Promoting `mentions` to typed edges by verb proximity** — the regex proposes, Dave ratifies (s267-D3). 240 proposals stay dashed.
6. **Merging the 11 ruling→ruling verbs into one** — undoes 20 hand-retyped edges (s267-D3) to save nothing the agent pays for.
7. **Inferring a ruling's `scope` from its prose** — derive it from `governs[]` targets only (G9); a ruling that names no component is a system ruling until Dave says otherwise.
8. **Retiring the 12 consumer-less types to make the census look clean** — they are the answers to five of the twelve questions; the defect is the missing reader, not the edge.

---

## Receipts
- Sources read: `BRIEF.md`, `BRIEF-A2-A3.md`, `A1-MEASURE.md`, `A1-measure.json`, `notes/_lanes/277/DAVE-RULINGS-2026-09-16.md`, `knowledge/_rulings.json` (ids named above), `knowledge/_build_kg_explorer.py`, `knowledge/_kg_explorer.template.html:160-231`, `knowledge/_validate_kg.py:87-88`, `knowledge/components/meta.schema.json` (`edges` 23 keys), `knowledge/_rule_nodes.json`, `knowledge/_ux_principle_nodes.json`, `knowledge/guidelines/_rules-index.json`, `knowledge/_parked.json`, `notes/_STATE-MACHINE-TARGET.md §7`, `notes/_lanes/269/kg-gaps/A-inventory.json`, `notes/_lanes/277/icons-propose/REPORT.md`, `knowledge/_GRAPH-REPORT.md`, `knowledge/_compose_slice.py` (docstring), `apollo-spider/skills/*/SKILL.md`, `knowledge/_consult.py`.
- Measurements made by this lane (commands in `A2-measure.json`): ruling scope split 99/432/62; session-in-id 392/394; accessibility holdings 55/52/20 across three families; BLOCKING rules obeyed 9/59; rules by file (34 files); `obeys` by file and by meta; ux orphans by grade (C 60 · L 21 · B 14 · A 2 · D 2); metas with `tokens` 135, 316 distinct refs, 12 heavy groups, 10 live token files.
- Nothing under `knowledge/` written. No generator run. `_build_kg_explorer.main()` not called.
