# #274 — the line and the rules

provenance: 274 · 2026-09-15
status: observed

**Spine:** `_LIVE-STATE.md` § ⏱ LATEST DELTA — 2026-09-15 (#274) · `GOOD-MORNING.md` § ★ LATEST (#274)
**Ledger:** `knowledge/_rulings.json` §§ `s274-D1`…`s274-D12` · `notes/_RULINGS.html`
**His words, in order, verbatim:** `notes/_lanes/274/DAVE-RULINGS-2026-09-15.md`
**Brief:** `_HANDOFF-125-the-line-and-the-rules.md` (written by the conductor BEFORE this ritual)
**Wrap report:** `notes/_subreports/2026-09-15-274-W-wrap.md`

---

## The arc in one line

Two halves of one instruction: finish the question the graph could not answer, then feed the graph.

## 1. The four list-vs-card decisions were not answered — they were dissolved

`P-272-1` had been open since #272 parked it and #273 researched it. #273's finding was **negative**:
thirteen external design systems, and **not one** draws the list/card boundary on field count. That
left `LC-1`…`LC-4` on `notes/_PROPOSAL-list-vs-card-2026-09-15-v1.html` with a recommendation against
each and nothing ruled.

#274 did not re-put those four questions. Dave answered by describing a model nobody had proposed —
two levels, containers over rows — and the four page decisions then **fell out of the model** rather
than being picked off the page:

> *"we have intersecting components here, so we have a simple-list-row, structured-list-row
> card-list-row - (this is basically the same as simple-list-row i guess, so we may not need the
> differentiation ). then we have simple-list, structured, card-list (the containers). I think that
> both simple and structured have optional headers, in banking these data in a structured list are
> obvious and often don't need headings."*

The conductor read that back as containers-over-rows with the card-list row admitted to be the same
object as the simple-list row, and he corrected **exactly one clause**:

> *"I think that actions might be allowable in a simple list in actuality"*

That sentence is the whole of `s274-D1`. The recommendation on the page had been *surface plus
record-level actions*; his correction struck the actions test and left **surface alone** — a record
is a card when its container draws a bordered surface around each record, and anything unbordered is
a list row at any field count. Actions became a **row property**, legal in any container.

**The lesson worth keeping: the page was nearly right, and the sentence that fixed it was his.** A
lane that had been allowed to "resolve" LC-1 from its own research would have shipped the actions
clause, and it would have been wrong in a way no gate could see.

The headers split closed the same way — *"okay i think you are right on 'headers on card lists' lets
get this done"* ⇒ `s274-D5`: a list-level heading optional on all three containers, a per-card title
living on the row. `04c51c6` inscribed `s274-D1`…`s274-D5`; the store moved **566 → 571**.

## 2. The enactment went onto the meta, and the lane named its own words as its own

`58f56ef` (lane LCE, Opus, 121,000 real) gave `knowledge/components/list-items.meta.json` the three
`$level: container` variants, marked the six record rows `$level: row`, wrote the `when` predicate
carrying D1's surface clause and D4's comparison test at `priority 60`, amended `purpose` **by
addition**, and gave `account-card` a `$note` recording D3 while leaving it `$not-a-provider`. Every
span reconstruction-proven.

⚠ Two of the words on that meta are the **lane's**, not his: `bordered-per-record` (the surface value
`s274-D1` is expressed in) and `$level: "typeset"`. The lane declared them as its own, and the wrap
carries them forward as an open item rather than letting them settle in unremarked. **A lane's
vocabulary entering a ruled model in silence is how a lane rules by accident.**

Then `s274-D6`, which is one character — *"1"* — on who is the default provider of `record-list`:
**`list-items` is the default and table takes the comparison test**, a field that must be read *down
a column* across records. `3a752d1` replaced two `roles.json` `when` strings by span and retired
`"<= 3 fields per item"` as contradicted by his own `s274-D1`/`s274-D4`.

And immediately after it, a requirement rather than a ruling:

> *"note that in edit mode, when we build it, the user can be presented with the alternatives we have
> defined."*

That is a demand on the composer's **edit mode** — show the resolver's runner-up providers — not a
decision about a mechanism, so it was **parked as `P-274-1`** with a tripwire on
`knowledge/_compose_slice.py` (`3b12185`) rather than inscribed. ⛔ The distinction is the discipline:
a requirement inscribed as a ruling is a false inscription with a good excuse.

## 3. The 470 guideline rules entered the graph — and the read-back is where the ambiguity died

`s269-D1` step 2. The shape was RK/RL, proven at #273: one **read-only** Opus lane builds the
generator with a dry-run, a selftest and a `--land --ratified` gate that refuses without a recorded
ruling id; it publishes a review page of **six** decisions; it **lands nothing**.

`0bfaf91` (lane RK, Opus, 203,000 real) did exactly that — `knowledge/gen_kg_rules.py`, selftest 12
bites, **13 mutants all caught**, dry-run 521 nodes / 634 edges / 23 declared nulls, nothing written.

His export came back **RK-1 a · RK-2 a · RK-3 null · RK-4 a · RK-5 a · RK-6 a**, and two of the six
were not plain accepts:

- **RK-3 came back `null` with a question**, not a deferral — *"I need to understand this better,
  which is the more durable/scalable solution, and if we have both will this cause unneeded
  complexity?"*
- **RK-4 and RK-6 came back `a` with a sequel attached** — *"Can we have A and then C, surly the
  compliance fix isn't egregious??"* and *"So A for now I guess and then D, is that correct?"*

The conductor read the **whole** set back in one message with those sequels written as staged
follow-ups, and his reply was one word: *"go"*. `f6c5da8` inscribed `s274-D7`…`s274-D12` — node kind
`rule:<id>`, four edge types (`definedIn`, `cites`, `enforcedBy`, `flaggedBy`) ratified into the
closed vocabulary, destiny as an **attribute** and not an edge, the 19 unresolved SC citations
**declared `ref:null` with a note** rather than dropped, store and reader landing in the **same
commit**, and rule → component staying out of wave 1 because the durable route runs the other way.
The store went **572 → 578**.

`00f3a87` (lane RL, Opus, 139,000 real) landed it: `knowledge/_rule_nodes.json` at **521 nodes / 634
edges / 19 declared nulls**, 470 of the nodes `rule:`, with the explorer at v1.11 reading it behind a
"Guideline rules" chip, driven in chromium with zero console errors and **screenshot-reviewed by the
conductor before it was presented** [[art-director-reviews-lane-output-268]]. `P-274-2` (the 19 SC
criteria into the compliance corpus) and `P-274-3` (metas cite rules) are parked as the sequels he
named.

**The method finding: a `null` with a sentence attached, and an `a` with a sentence attached, are the
same event — a redirection.** #273 learned the first half; #274 learned that the read-back, not the
re-ask, is where a sequel becomes a plan.

## 4. What was deliberately not done

The KG-gaps presentation stayed shut, on his own direction:

> *"this is just getting teh KG working harder we'll work on the demo/prez after we get this all
> sorted"*

Carried as **direction, not a ruling**, and deliberately given no `sNNN`.

## Resolved state, and what is still open

**Resolved:** the list/card line (surface alone) · the shapes (one meta, three containers) ·
`account-card` · the cardinality question (no number, the comparison test) · headers · the
`record-list` default · the rule-node kind, its four edge types, destiny, the SC nulls, the
land-with-reader rule and the direction of rule → component.

**Open, and every one of them a question put rather than a state of the world (`s271-D4`):** lane
LCE's three proposals and its two coined words · lane RL's chip word and the 99 of 634 edges that
draw only with two explorer layers on · `_rule_nodes.json`'s `$description` still reading *"PROPOSED
… NOT RATIFIED"* · the `example` key on the 13 new `when-fields` entries · the four near-dupe pairs ·
the six `data-grid` reds · `input` sub-roles · `P-272-2`…`P-272-4` · the 108 stale showroom pages ·
the boot ceiling and the #243 double-count · the push.

**Next (`_HANDOFF-125` § #275):** `s269-D1` step 3 — the 145 UX principles in the RK/RL shape — then
`s273-D2` authoring pass two, with `record-list` now unblocked and `input` still waiting.
