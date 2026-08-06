# #115 — three graph-engineering candidates landed, and an observation window became an instrument

```
provenance: session-115 · 2026-08-06
status: observed
```

*Both-way links: spine `_LIVE-STATE.md` ⏱ #115 delta · ledger `notes/_MEMENTO-DECISIONS.md` § ★ #115 ·
brief `notes/_briefs/2026-08-06-graph-candidates-pricing-brief.md` · register `knowledge/_rulings.json`
`s115-D1`/`s115-D2` · commits `9b47152` · `6a16633` · `ce0cc7f`.*

---

## 1. The session was titled for one thing and Dave opened another

#115 was opened for **#114-D5's checker measurement redesign** and **#114-D2's citation gate**. The
opener instead put the `-v3` research candidates in front of him with their prices, and he ruled:
**"no lets get these done now"** — candidates **1**, **3**, and the **mark-half of 2**.

The why matters more than the pick. The titled lane is two builds that each end in a gate promotion,
and neither is blocked by anything. The graph candidates were blocked by a **join that did not exist**:
the decision graph's node ids and the retrieval corpus's record ids had never been reconciled. So the
deferral is not a preference between two queues, it is **unblocking before building** — and it is
Dave's, recorded as such so a later reader does not read the roll as a slip.

## 2. The measurement that re-priced the doc

The research doc sized candidate 1 as **Small**. The first thing the build sub did was measure the
overlap between node ids and record ids: **0 of 575**. There was no join to extend — one had to be
constructed. The candidate is **Medium**, and the doc's own estimate was wrong.

This is the [[measure-dont-convert-units]] shape applied to a plan rather than a number: an estimate
inside a delivered artefact is still an estimate, and the tree is the arbiter. It is also why the
pricing brief exists as a repo artefact rather than as a chat message.

## 3. Dave's catch: an observation window nobody can observe

Candidate 2 splits into **mark** (annotate a result that mentions a superseded node) and **demote**
(rank it lower). Only the mark half was built, on purpose: demotion changes ranking, and ranking should
not change on a hunch. The plan said *run marks for a while, then decide from what we see*.

Dave read that and asked:

> *"so I should be looking out for these manually?… do I have to write these down on a postit or something??"*

That is [[feedback-measuring-tool-must-not-guess]] pointed at a **human** instead of a script, and it
is the sharpest thing in the session. An observation window whose record is somebody's memory produces
a verdict with no provenance, and the verdict would then govern a ranking change. The remedy shipped
the same session (`ce0cc7f`):

- the doors append **one JSONL line per DISPLAYED (post-cap) marked result** to
  `knowledge/_graph-mark-observations.jsonl` — post-cap, because a mark on a result nobody saw is not
  an observation;
- **the reader ships with the writer** — `_graph_edges.py --tally` — so the instrument cannot decay
  into a store nothing re-reads [[instrument-without-a-consumer]];
- write failure prints **LOUD** and never raises into the door: a retrieval door must not be taken
  down by its own telemetry;
- **6 selftest bites**, and the selftests are **proven not to pollute the real log** — the store is the
  evidence for a future ruling, so a test that writes into it would corrupt the thing it protects.

The first real tally, taken immediately: **15 marked results, 4 carrying ⛔**, and `ls:LIFECYCLE` alone
accounts for **17 dead-node mentions** — which is the **predicted** noise class, because that section
is *about* supersessions. The prediction landing on the first tally is mild evidence the instrument is
measuring the right thing.

## 4. The semantic that must not drift

**⛔ on a result means the result MENTIONS a superseded node. It does not mean the result is dead.**
Inscribed in the brief and carried on a standing surface, because the observation window's whole
output is a count of these marks: a reader who mis-reads the symbol produces a confident false verdict
from a correct instrument.

## 5. Corrections and dead-ends, declared

- **Two steps, one commit.** The plan split candidates 1 and 3 into separate commits. The sandbox's
  delete-guard blocks the mv-aside that split needed, so they landed together and the **deviation was
  declared at the commit**. What the split was actually protecting — **mark vs demote separability** —
  is untouched.
- **The index went stale, and the machinery caught it.** The new brief and the new runbook are corpus
  members, so the retrieval index was one record short the moment they landed. The commit script's own
  rehearsal probe caught it; `6a16633` regenerated 575→**576**. The **+1 `notes/_REHEARSAL-LOG.jsonl`
  lines inside `9b47152` and `ce0cc7f` are that probe's records** — named here so nobody chases them
  as corruption later.
- **A pre-existing FAIL was found and left alone.** The memento known-answer test for
  `runbook:context-gauge` (slug *"…the-only-cop"*) fails at HEAD **before** this lane — verified by
  stash. It was **declared and deliberately not fixed**: repairing an unrelated known-answer test
  inside a build lane is how a lane's evidence stops being about the lane. The honest repair is a
  **re-pin off the rebuilt index**; it sits in GM §C·4 with **no owner**, which is the accurate state.
- **Retrieval worked, and that is worth saying because #114's headline was the opposite.** *"Have we
  enacted the -v3 recommendations?"* was answered from repo greps plus the ledger, and `_search_core.py`
  was verified to hold **no edge code** before anything was priced [[roll-pointer-is-not-an-absence]].

## 6. The throttle

One check-in, run **at the D5 seam**: **FILL 130,074 real** against the **150,929** stop line — runway
**20,855**. The next lane was priced above 15K, so the wrap was **opened rather than the lane ridden**.
No mid-lane blow. That is #97's mechanism working, and it is the third distinct session where the
recorded cause of holding the line is *stopping at a seam rather than finishing a lane*.

Sub quota: **build sub 122,030**, plus this delegated wrap sub, whose own figure is **not observable
from inside it**. **Dave gave no day-quota reading this session, so it is UNKNOWN** — and no earlier
reading was substituted for it.

## 7. Resolved state, and what is still open

**Resolved:** candidates 1 and 3 built, wired and committed · the mark half of candidate 2 built ·
the observation window instrumented with a shipped reader · the index and mention-map regenerated.

**Open:** **demotion is not ruled and not scheduled** — it waits on `--tally` evidence, and that is
Dave's ruling to make · the titled lane (**D5 checker redesign**, then **D6's 44-promote**, and the
**D2 citation gate**) rolls intact · the **attribution re-probe (#111-D3) has now rolled three
consecutive sessions** (#113 → #114 → #115), which is stated plainly rather than restated as *"next
session"* for a fourth time.
