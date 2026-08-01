# 2026-08-01 — worker: Anthropic KG cookbook, scored against Apollo's decision graph

**Role:** worker (Dave's opener: *"you are a worker, I want you to do some research, leave receipts for the
conductor"*). **Nothing committed. Nothing in the repo modified except this file.**
**Source under study:** `https://platform.claude.com/cookbook/capabilities-knowledge-graph-guide`
(Anthropic, published 2026-03-23) + its standalone scorer + linked cookbooks.
**Depth:** deep (Dave's pick) · **chain:** booted on Dave's mid-turn instruction (`_CHAIN.md`, 4,737 tape).

> ⚠ **Off the #70 critical path.** `_CHAIN.md`'s ★ LATEST has #70 owing D3 lockup rework, D4 DV-D17
> collision, and the review-export defect. This receipt touches none of them. Read it when the KG lane
> is next opened, not before D3/D4.

---

## Verdict in one paragraph

The cookbook is a competent guide to a problem **Apollo does not have**, and its central technique is one
**ADR-0012 §7 already ruled against** for this corpus. That half is a clean no. But probing our own graph to
score it turned up four defects in `_decision-graph.json` that have nothing to do with the cookbook and
everything to do with us — including **a recorded supersession that marks nothing dead**, which is the exact
failure mode ADR-0007 was written to prevent. The research earned its keep sideways.

**The one transferable idea:** the cookbook enforces its entity vocabulary with a closed `Literal` enum that
the API guarantees. ADR-0012 §2 ruled a closed seven-type edge taxonomy and we implemented it as an open
string. Six unruled types and ten edges walked in unremarked.

---

## 1 · What the cookbook actually teaches

Four stages, each replacing a trained model with a prompt:

1. **Extraction** — one structured-output call per document (`client.messages.parse()` + Pydantic) emitting
   `entities[]` and `relations[]`. `Entity.type` is a closed `Literal["PERSON"|"ORGANIZATION"|"LOCATION"|
   "EVENT"|"ARTIFACT"]`; `Relation.predicate` is a free-text `str`. Runs on Haiku.
2. **Entity resolution** — Claude clusters surface forms per type into `canonical` + `aliases`, using the
   one-line descriptions from stage 1 as disambiguation context. Runs on Sonnet. Catches
   "Edwin Aldrin" → "Buzz Aldrin", which string similarity cannot.
3. **Assembly** — NetworkX `MultiDiGraph`; endpoints rewritten to canonical form.
4. **Query** — serialize an *n*-hop subgraph as triples, hand it back to Claude, get edge-cited answers.

Plus a P/R/F1 scorer against a hand-labelled gold set.

**Its own published quality numbers** (guide, Evaluation section) — worth reading before anyone gets excited:

| doc | precision | recall | F1 |
|---|---|---|---|
| Apollo 11 | 1.00 | **0.55** | 0.71 |
| Neil Armstrong | 1.00 | **0.38** | 0.55 |

Precision is perfect; **recall is 0.38–0.55**. On six short, clean Wikipedia summaries. The extractor misses
roughly half of what a human labelled. Our corpus is denser, more cross-referential and more jargon-laden
than Wikipedia prose, so that is a ceiling, not a floor.

**Failure modes the guide names itself** (credit where due — these are declared, not hidden):

- **Silent drop.** A raw name Claude omits from every cluster vanishes from the graph, because
  `alias_to_canonical` has no entry for it. Guide's own words: *"a production resolver should fall back to a
  single-element cluster for unmatched names so nothing is lost."*
- **Over-merge.** *"a specific mission like 'Gemini 12' may get folded into the broader 'Project Gemini'
  because the descriptions overlap."*
- **Relation scoring ignores predicate wording** — matched on `(source, target)` pairs only, so
  *"its relation recall is an upper bound."* Declared. By our standard, a declared gap passes.

### 1b · A defect in the cookbook's own feedback loop

The guide closes with: *"change the extraction prompt, rerun the scorer, watch the F1 move. That loop is what
turns a demo into a production system."*

**The scorer does not run the guide's prompt.** The notebook's `EXTRACTION_PROMPT` carries four guidelines;
`evaluation/eval_extraction.py`'s `PROMPT` carries two. Dropped: the *"write a one-sentence description"*
guideline and the *"predicates should be short verb phrases"* guideline. The `description` field is still
required by the Pydantic schema, so it gets filled unguided — and stage 2's resolution quality depends on
exactly those descriptions.

So editing the notebook prompt changes nothing the standalone scorer measures. Anyone tuning that way is
watching a number that cannot move in response to the thing they changed. **This is our own
`check-after-its-own-remedy` class, in someone else's repo.** Not a reason to distrust the guide's method —
but a reason to distrust its numbers as a tuning signal, and worth knowing before we borrow the harness.

---

## 2 · Scoring against Apollo's ruled position

Retrieved and quoted, not recalled: `docs/decisions/ADR-0012-decision-graph-edge-convention.md`,
`docs/decisions/ADR-0007-project-memory-decision-graph.md`, `knowledge/_decision-graph.json`,
`knowledge/_build_decision_graph.py`, `_LIVE-STATE.md`, `notes/_receipts/2026-07-21-worker-decision-graph-inscription.md`.

### ⛔ INVALIDATED for our decision corpus — the core technique is already ruled against

ADR-0012 §1: *"A node is any unit that **already carries a stable ID**"* — `R-D*`, `T-D*`, `B-D*`, `DV-D*`,
`ADR-*`. Our nodes are **authored, not discovered.** There is no extraction problem to solve.

ADR-0012 §7 is the decisive one, and it is a ruling, not a preference:

> *"The audit showed edge-authoring is **not** mechanical (scoped/claim-level supersession, deliberate
> divergence). The judgment half — reading the corpus and deciding the edges — was therefore done **in this
> Fable session**… What remains delegable: the mechanical **inscription** of seed edges… Conflicts remain
> **queued for Dave, never auto-resolved**."*

ADR-0007 §5 backs it with the anti-laundering guard: promotion to `vouched` is *"a **human correctness-audit
only, never derived**"*, because *"a wrong decision, once a clean node with a tidy edge, **looks vetted** —
the graph launders it."*

The cookbook's pipeline derives nodes **and** edges. Pointed at our ledgers it would do precisely what §7 and
§5 forbid. Three concrete collisions:

1. **Over-merge would destroy an authored ruling.** ADR-0012 §2 records `diverges-from` for DEF-006 vs
   DEF-005, quoting the original: *"a future reader will try to reconcile them. **Do not.**"* An LLM resolver
   clustering on description similarity does exactly the forbidden thing. The guide's own named over-merge
   failure ("Gemini 12" → "Project Gemini") is structurally identical.
2. **Our edge vocabulary is strictly more expressive than the cookbook's.** Free-text `predicate` cannot
   carry `scope=`, `claim=`, `resolution=`, `reason=`, `ref=`. It cannot express
   `supersedes(R-D10, claim=fills-mode-stable)` — kill one claim, leave the node live. That qualifier
   mechanism is *the part that took judgment*, and it is the part the cookbook has no slot for.
   Live qualifier usage: `scope` 31 · `claim` 14 · `resolution` 8 · `ref` 6 · `reason` 1.
3. **The cookbook's graph is atemporal.** Edges are `(source, predicate, target, source_doc)` — no validity
   window, no lifecycle, no status. ADR-0007 §1 is explicitly Graphiti's `t_valid`/`t_invalid` in markdown,
   and §4 names **Graphiti** as the graduation path. The cookbook's graduation path is Neo4j/Neptune/Postgres
   with no temporal model at all. It cannot represent supersession, which is our whole point.

### ○ ORTHOGONAL — right method, wrong corpus

The cookbook targets *thousands* of unstructured documents. Our decision graph is 83 nodes / 155 edges,
hand-authored. Wrong scale by three orders of magnitude.

But we **do** own a large unstructured prose corpus where facts genuinely hide: `_DECISION-HISTORY/`,
`notes/_briefs/`, `notes/_receipts/`, the GOOD-MORNING archives. ADR-0012's own Context names the symptom —
*"Rulings cross-reference in **prose**… so recall = keyword search and reconciliation = manual archaeology."*
That is the cookbook's actual problem statement, in our words, about a different corpus than the one we
graphed.

**If** this is ever pursued, the only shape consistent with §5/§7 is **candidate generation for human
ratification** — extraction proposes edges into a queue, Dave vouches, nothing self-inscribes. That keeps
derivation on the consistency side of the line and validity on the human side. **Not recommended now**: at
R≈0.4–0.55 the proposal queue would be half-empty and wholly untrusted, and Memento's `_memento_search.py`
already serves retrieval over that corpus at zero marginal cost. Flagging it as a shape, not a plan.

### ✅ CONFIRMS — genuine independent corroboration

ADR-0007's desk research concluded: *"the graph is just a queryable view over well-recorded edges. The
discipline of writing the edge at ruling-time is what actually prevents rot — not the storage engine."*

The cookbook, from the opposite direction, agrees: *"Everything runs in memory with no database… The
extraction and resolution code doesn't change — only the persistence layer does."* Both land on
*storage is the boring part*. ADR-0007's decision to stay lightweight-first is corroborated by a source
that had every commercial reason to reach for infrastructure.

---

## 3 · What probing our own graph turned up (the real payload)

Four findings, **one shared cause**. All verified by running probes, none inferred.

**Cause:** edge `type` is an open string, and every protective mechanism in
`knowledge/_build_decision_graph.py` is keyed to *closed-set membership*. An unknown type falls silently
outside all of them and is stored, counted, and displayed as if it were fine.

### F1 · Six edge types are in the live graph that ADR-0012 never ruled — 10 edges

ADR-0012 §2 rules **seven** types + `relates`. The live graph carries fourteen. Unruled:
`sibling` (1) · `carve-out` (1) · `enacted-by` (1) · `amends` (4) · `enables` (2) · `supersedes-mechanism` (1).

Grepped for an authoring record extending the taxonomy — **none exists.** These entered by ordinary good-faith
use, written straight into `Edges:` lines. That is the predictable outcome of ruling "small core, nuance in
qualifiers" and then not gating it: when the seven don't fit, a new type is the path of least resistance.

⚠ **This is an absence, never a regression** — the gate was never built to check edge type. ADR-0012 §6
specifies `--strict` bites on *"any `conflicts-with` lacking a resolution, any `resolution=open`, or a
`supersedes` target that can't be resolved"*. Type validation is not in scope and never was.

### F2 · ⛔ A recorded supersession that marks nothing dead

`knowledge/_proforma/_DATAVIZ-DECISIONS.md:247`:

```
Edges: refines(dv-004, scope=mechanism-neutral-separation) · supersedes-mechanism(dv-004-stroke-only)
```

`_build_decision_graph.py:287` computes death by literal string match:

```python
dead_hit = [e for e in inbound.get(nid, []) if e["type"] == "supersedes" and not e.get("claim")]
```

`supersedes-mechanism` ≠ `supersedes`. **The target is never marked DEAD.** And `:306` gates the orphan
check on `t in STRUCTURAL` — which excludes all six unruled types — so an edge pointing at a node that does
not exist raises nothing either. Confirmed: `dv-004-stroke-only` is **not** among the 83 nodes; `DV-D14`'s
state is `null` and it is absent from the LIVE/AMENDED/DEAD/OPEN rollup entirely. It has no home anywhere —
it appears only in that `Edges:` line and in generated output.

**The suppressor is the type, and nothing else — traced, not assumed.** `:306` carries two legitimate
exemptions past the STRUCTURAL test: `RULE_ID = ^[a-z]{2,6}\d{0,2}[a-z]?-\d{3}$` (rule-IDs are valid
non-node targets by design) and `FILEISH = [/.]` (file paths). I ran all five unruled-edge targets through
the real gate condition:

| type | target | structural | RULE_ID | FILEISH | orphan check |
|---|---|---|---|---|---|
| `refines` | `dv-004` | ✓ | ✓ | — | silent — **legitimately exempt** |
| `supersedes-mechanism` | `dv-004-stroke-only` | ✗ | ✗ | ✗ | **silent — type is the sole suppressor** |
| `sibling` | `button-sheet-v7, ADR-0009` | ✗ | ✗ | ✗ | silent — type is the sole suppressor |
| `carve-out` | ``ADR-0004, `_STANDARDS.md` §3`` | ✗ | ✗ | **✓** | silent — **two** independent suppressors |
| `enacted-by` | `ADR-0014` | ✗ | ✗ | ✗ | silent — type is the sole suppressor |

So: **had `supersedes-mechanism` been typed `supersedes`, the orphan check *would* have fired.** That is the
decisive test and it passes cleanly. ⚠ But note the `carve-out` row — its target contains a `.` from
`_STANDARDS.md`, so `FILEISH` exempts it *independently*. **A type-only fix leaves that one silent.** Any
remedy that stops at the type set will bank a green it has not earned.

**This is ADR-0007's founding failure, restored.** That ADR opens with a session that
*"wasted most of a sitting reasoning from a **retired artifact**… because nothing marked it dead"*, and names
the root cause: *"context staleness is an unrecorded supersession edge."* Here the edge **is** recorded — and
it is inert. Arguably worse than absent, because it looks discharged. Someone did the right thing and the
machinery ignored them silently.

### F3 · The grammar cannot express a multi-target edge, and fails silently when one is written

`knowledge/_proforma/_RAG-DECISIONS.md:53` and `:70`:

```
Edges: refines(R-D22) · sibling(button-sheet-v7, ADR-0009) · verified-by(contrast-gate)
Edges: carve-out(ADR-0004, `_STANDARDS.md` §3, scope=theme=legacy) · enacted-by(ADR-0014)
```

The parser locates qualifier boundaries by the known key set (`scope|claim|resolution|reason|ref`) — correct
per the 07-21 receipt — so everything before the first recognised key becomes **one target string**:
`"button-sheet-v7, ADR-0009"` and ``"ADR-0004, `_STANDARDS.md` §3"``. Neither matches any node. Neither type
is STRUCTURAL, so `:306` never fires. Silent again — same cause as F2.

### F4 · Two self-loops

`amends(ADR-0015) → ADR-0015`, twice, from `docs/decisions/ADR-0015-behaviour-partials-dataviz.md:98` and
`:154` — sub-rulings `ADR-0015-A1`/`-A2` amend their parent, but the parent's own line also amends itself.
Minor, but note the cookbook guards this explicitly at assembly: `if src and tgt and src != tgt:`. We don't.

### The remedy this points at — already ruled, just not applied here

`scope-blindness-gate-vocabulary` ruled the fix for this exact class: **normalise once + fail loud on
unknown, never enumerate.** Adding the six types to `STRUCTURAL` would fix the symptom and leave the class
untouched — the seventh unruled type would walk in tomorrow, just as silently.

⚠ **And a type-only fix is measurably insufficient**, per the F2 table: `carve-out`'s target is *also*
exempted by `FILEISH`, because a legitimate file reference (`_STANDARDS.md`) was written inside the target
slot of a malformed two-target edge. Promote every unruled type to STRUCTURAL and that edge stays silent.
**Whoever takes this must assert against the F2 table, not against a green build** — the build is already
green with all four of these in it.

The cookbook's contribution, and it is a real one, is the *mechanism*: `Literal[...]` makes the vocabulary a
closed set the schema layer guarantees. Our equivalent is a parse-time check that any type outside the ruled
set is a loud, named failure — the `_gm_usage.py` `UNMEASURED` precedent (#62) is the shape: a legal value
scoped to an exact form, biting in both directions.

⬛ **Not an agent's call:** whether the six types get promoted into the taxonomy (an ADR-0012 amendment) or
rewritten as qualifiers on the existing seven. That is a ruling. Both are defensible; `supersedes-mechanism`
in particular reads like it wants to be `supersedes(dv-004-stroke-only, claim=stroke-only-mechanism)`, which
would make it structural and mark the target dead — but that changes what is DEAD in `_LIVE-STATE.md`, so it
is Dave's, not mine.

---

## 4 · UNPROVEN — declared, not smuggled

- **I did not run the cookbook pipeline.** No API calls, no extraction, no measurement on our corpus. Every
  quality number above is Anthropic's published figure on *their* Wikipedia corpus. Our recall is **unmeasured**.
- **I did not read the three linked cookbooks in full.** Fetched contextual-embeddings (61.8KB, persisted to
  the tool-results cache, not read through); RAG and structured-JSON extraction not fetched. Basis for calling
  them adjacent: their published abstracts + the guide's own one-line characterisations. Contextual retrieval
  is a chunk-enrichment technique for vector search — it bears on Memento's retrieval layer, **not** on the
  authored decision graph. Treat that routing as reasoned, not verified.
- **F1's "no authoring record" rests on one grep** across `docs/decisions`, `knowledge/_proforma`, and the
  notes ledgers. A ruling recorded only in a session transcript, a brief, or GOOD-MORNING's retrieval surface
  would not have been caught. Probe run: `grep -rn "new edge type\|edge type\|taxonomy" --include="*.md"`.
  **An unmatched grep is not an absence.**
- **I did not run `_build_all.py`** — per the standing `_CHAIN.md` warning that a partial run strands the tree
  in the documented mid-build state. All probes were read-only against the committed
  `knowledge/_decision-graph.json`. So findings describe **the graph as last generated**, not necessarily as a
  fresh build would produce it.
- **The 155-edge count is not inflated.** I suspected the 07-21 double-count bug (which produced 157) had
  recurred. **Probe run, suspicion killed:** 0 exact-duplicate edges, 155 total, 155 unique. Recording the
  dead suspicion so nobody re-runs it.
- **The verification pass changed the receipt — recording what it caught.** My first draft attributed F2's
  silence entirely to `STRUCTURAL` membership. Re-reading `:306` at source showed two further exemptions
  (`RULE_ID`, `FILEISH`) that the draft never mentioned. Running all five targets through the real gate
  condition confirmed the headline (type *is* the sole suppressor for `dv-004-stroke-only`) but exposed a
  second independent suppressor on `carve-out` that a type-only remedy would not clear. **The finding
  survived; the proposed fix did not.** Noting it because the draft would have banked an unearned green.
- **Whether the KG lane is worth opening at all** is not established here and is not mine to decide.

---

## 5 · For the conductor — options, priced, not recommendations

Nothing below is started. Ordered by ratio of consequence to cost.

1. **Fix the class, not the six instances** — make an unknown edge type a loud named failure in
   `_build_decision_graph.py`, advisory first per ADR-0005 §5. Small (~1 focused session incl. bite-test).
   **Blocked on the ruling in §3** — the gate can't be written until it's known whether the six types are
   legal or to-be-rewritten.
2. **F2 in isolation** — `dv-004-stroke-only`'s status is currently unrepresented. Tiny to fix, but it changes
   `_LIVE-STATE.md`'s DEAD block, so it needs Dave. **Should not wait for item 1.**
3. **Recall probe on the seed** — nobody has asked what edges exist in the corpus that the *seed itself*
   missed. `--verify` diffs inline against seed, so it cannot detect an edge both lack. That is a check that
   cannot fail in the direction that matters. The cookbook's gold-set P/R method is a candidate here, and this
   is its **best** fit anywhere in Apollo — measuring graph *completeness*, not decision correctness. Medium
   (~1 session to build a gold set over one ledger). ⚠ It does **not** discharge ADR-0007 §5's
   correctness-audit; that is validity, this is consistency. Do not let them be conflated.
4. **KG-over-prose candidate generation** — parked shape, described in §2. **Not recommended now.**

---

## 6 · Method — what I actually ran

Chain booted (`_CHAIN.md`) on Dave's mid-turn instruction; `GOOD-MORNING.md` **not** opened. Guide + scorer
fetched via `web_fetch`. Canon read directly. Four probes run read-only in the sandbox against
`knowledge/_decision-graph.json` and `_build_decision_graph.py`: duplicate-edge check, unruled-type census,
DEAD-computation trace, taxonomy-extension grep. Every quoted line re-read at its source before being written
here. Receipt written once and verified against sources in a second pass.

**Not committed** — worker. Reconcile this path explicitly; do not blind `git add -A`.
