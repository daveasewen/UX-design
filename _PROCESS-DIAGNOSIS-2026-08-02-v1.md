# What is actually failing — a broad diagnosis

**2026-08-02 · #85 opener · measured, not recalled · every number path-scoped and re-derived in-window**

---

## The short version

Nothing is broken. Nothing is lost. The design system is intact and the gates are green.

What has happened is narrower and stranger than "rot": **the project stopped working on Apollo
on 26 July and has been working on its own bookkeeping ever since.** Seven days, roughly two
hundred commits, and the component library has not moved by one component.

The knowledge graph did not fail. It is holding perfectly — for a subject we abandoned. Its last
entry is dated **24 July**, which is within a day or two of the date the work changed domain. It
contains one hundred design decisions and **zero** process decisions, because it has no node type
for one. So every ruling you have made since — the unit, the budget, the refusal, the chain cut,
the cross-instrument gate — lives outside it, in eight other places, none of which is authoritative.

That is where "we've lost the broad context" comes from. The context is not lost. It is **shredded
across eight stores with no join between them**, and the largest of those stores is the one we
re-read, re-price and re-attribute at both ends of every single session.

The circling is not a mood. It is measurable: *headroom* has been on your opener list for
**ten consecutive sessions**. The six unruled edge types, for **eight**.

---

## The mechanism, in one sentence

**Every defect we find produces a gate; every gate is an artefact that can itself rot; every
rotted gate is a new defect — and there is no rule anywhere in the system that says a thing is
finished.**

So the defect count cannot go down. It is monotonically non-decreasing *by construction*. And
the better the detection gets, the faster it climbs — a sharper microscope finds more, not less.
That is why the work feels like it is accelerating and arriving nowhere at the same time. It is.

Three structural faults hold that loop open.

### 1. No gate can fail on behalf of the product

Every check in the system checks the record: sizes, units, banners, strata, provenance, freshness.
Not one of them can go red because Apollo did not move. Seven days at 68 components is invisible
to the entire apparatus. The only surface that *can* fail is the meta-layer, and the meta-layer
can always fail, because it is prose about prose. So attention flows to the only place that
produces signal.

### 2. The record is the workspace, not a summary of it

`GOOD-MORNING.md`, `_LIVE-STATE.md` and `_CHAIN.md` are edited every session, so every session
must read them, price them, roll them, attribute its own growth in them, and re-measure them.
That is a fixed tax proportional to nothing useful. **43% of commits in the last week touched only
the record.** The read chain was *cut* at #33 to stop exactly this — it has grown **47% in the
five days since the cut**.

The token fixation is not a bad habit. It is the correct response to a real cost that the process
manufactures itself. You are not stuck on the token count; **the token count is stuck on you**,
because the record grows whether or not anything is built.

### 3. The graph was the one structure that could have absorbed this, and it was left behind

At the moment the domain changed, the right move was one new node type in `_decision-graph.json`.
Instead the decisions scattered — and at #81 a *second* index was built beside it (`_rulings.json`,
9 entries). That index already carries a false line: it still records the budget as
`working 200,000 (Dave's)`, the exact provenance error struck at source at #83. **The replacement
index rotted within two sessions of being built.** Not because anyone was careless — because a
second store of the same facts *always* does.

---

<details>
<summary><b>Evidence — every figure, with how it was obtained</b></summary>

### Product velocity (path-scoped `git ls-tree`, not a tree-wide grep)

| date | components | snippets |
|---|---|---|
| 2026-07-17 | 39 | 38 |
| 2026-07-21 | 41 | 40 |
| 2026-07-24 | 66 | 65 |
| 2026-07-26 | **68** | 67 |
| 2026-08-02 | **68** | 69 |

39 → 68 in nine days to 26 July. **68 → 68 in the seven days since**, +2 snippets.

> ⚠ A first pass reported 108 and it was wrong: the grep was tree-wide and matched
> `_retired/` and `archive/` copies of the same paths. Re-measured path-scoped and corrected
> before publication — [[unmatched-grep-is-not-an-absence]], the *matched-grep-is-not-a-presence*
> half. Noted because it matters that **the rules in this repo are correct**; the fault is not
> in the rules.

### Where the effort went (commits by area, 2026-07-26 → 2026-08-02)

| area | commits | share |
|---|---|---|
| RECORD (GM / LS / CHAIN / notes / dossiers) | 720 | 43.2% |
| INSTRUMENT (gates, gauges, runbooks, index) | 432 | 25.9% |
| **PRODUCT (components, css, showroom, reviews)** | **338** | **20.3%** |
| other | 175 | 10.5% |

Two days in that window ran at **4.2%** and **4.4%** product.

### The knowledge graph

`knowledge/_decision-graph.json` — 100 nodes · 165 edges · **0 findings** · newest internal
date **2026-07-24** · zero session references.

Node namespaces: `ADR-` (19) · `R-D` (30) · `DV-D` (20) · `T-D` (15) · `B-D` (7) · `DEF-` (3) ·
`TYPE:` (3) · 2 misc. **All design-domain. No process-domain node type exists.**

Substring probe over the whole graph:

```
ds-021      False     preflight   False     chain       False
ds-023      False     capture     False     memento     False
ds-025      False     headroom    False     instrument  False
```

### The eight parallel decision stores

`_decision-graph.json` (frozen 24 Jul) · `_rulings.json` (9 entries, #81) ·
`notes/_MEMENTO-DECISIONS.md` · `_DECISION-HISTORY/` (29 dossiers) ·
`knowledge/_ENACTMENT-REGISTER.md` · `_LIVE-STATE.md` · `GOOD-MORNING.md` · `MEMORY.md`.

Each needs its own freshness gate. None is authoritative. Every ruling must be written to
several and can rot in any.

### The circling, counted

Items appearing on *"DAVE'S AT THE #N OPENER"* across #74–#85:

| item | sessions | count |
|---|---|---|
| headroom | 76,77,78,79,80,81,82,83,84,85 | **10** |
| the six `_decision-graph.json` edge types | 74,75,80,81,82,83,84,85 | **8** |
| `_measure_tokenizer.py` 0 consumers | 83,84,85 | 3 |
| §C over its warn cap | 83,84,85 | 3 |

**95 item-slots across 12 sessions; 84 distinct.** The list does not turn over. It accretes.

### The chain that was cut

| date | `_CHAIN.md` |
|---|---|
| 2026-07-29 (at the #33 cut) | 16,750 B |
| 2026-07-31 | 20,752 B |
| 2026-08-02 | **24,608 B** |

**+47% in five days.** Its ★ LATEST banner is now largely arithmetic about its own size.

### The rotted replacement index (verbatim)

```json
"id": "gauge-band",
"says": "... amber 160,000 · working 200,000 (Dave's) · hard 256,000 (sourced)..."
```

Live corrected form, in `_CHAIN.md` this morning:

```
amber 160,000 (PICKED) · working 200,000 (SOURCED)
```

`#83` struck *(Dave's)* at source because you had corrected it yourself in code at `#58b`.
`_rulings.json` was built at `#81` and never learned.

</details>

---

## What I would do, and why it is safe

**Safety first, because you asked for it and it is a factual matter, not reassurance:** you can
stop all of this today at zero risk. The product is whole, the gates pass, 68 components stand,
and the record is *over*-preserved rather than under. Nothing that has rotted is load-bearing on
Apollo. What has rotted is bookkeeping about bookkeeping.

Three moves, in order.

**1 — Freeze the instrument.** Not delete, not audit, not one more gate. A declared change
freeze: no new gates, no new indexes, no re-measurement work, for a fixed number of sessions.
This is the only experiment that can actually settle the question, because we have never once
run without them. If Apollo moves and nothing breaks, the instrument was already sufficient and
the last week is the proof. If something breaks, we learn precisely which gate we needed — which
is currently unknowable.

**2 — Give the product a gate that can go red.** One check, one number: *components/snippets
added this session*. Zero for N consecutive sessions **fails**. It is the only kind of check the
system does not have, and its absence is why attention drains to the meta-layer. It costs about
twenty lines.

**3 — Collapse eight stores to two.** One graph — extend `_decision-graph.json` with a `process`
node type, which is the same shape it already has, and backfill the nine rulings — and one
chronological ledger. Everything else becomes generated or archived. This also discharges the
edge-types item that has been open for eight sessions, because it becomes the same job.

The one thing I would **not** do is fix the cross-instrument claim check first. It is good work
and it is correctly reasoned. It is also the ninety-first turn of the loop.
