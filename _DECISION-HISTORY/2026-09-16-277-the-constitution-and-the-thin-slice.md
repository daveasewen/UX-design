# 2026-09-16 · #277 — the Constitution and the thin slice

provenance: 277 · 2026-09-16
status: observed

*Spine entry: `_LIVE-STATE.md` § ⏱ LATEST DELTA (#277) · banner: `GOOD-MORNING.md` § ★ LATEST (#277) ·
ledger: `knowledge/_rulings.json` §§ `s277-D1`…`s277-D13` · handoff: `_HANDOFF-128-the-constitution-and-the-thin-slice.md` ·
carry set: `_CARRIES.md` § `## residual → #278` · filed report: `notes/_subreports/2026-09-16-277-W-wrap.md` ·
his words, verbatim: `notes/_lanes/277/DAVE-RULINGS-2026-09-16.md`.*

⚠ **DATE SPLIT.** The session opened on the evening of **2026-09-15** and six commits carry that date;
the three exports, the thirteen rulings, the enactment and the ritual are **2026-09-16**, seventeen
commits. Nothing was re-dated. This file is dated from `date` at the hour it was written.

---

## 1. Why the day looked the way it did — a budget, and a suspicion

Two sentences of Dave's set the shape before any work began. The first was a budget: *"we have a lot of
tokens to use up"*, then *"I recommend yoy smash the subs and use a lot of fable judgement"*, and later,
mid-land, *"we have 2 days to use 60% of our tokens for the week, we need to rip through this work"*.
The second was a **suspicion about the graph**: *"we have a lot of new nodes with very little edges
connecting them some are pretty much orphaned or at least only local to their node type. I have a feeling
that because this has grown and evolved over time there might be a case for a full audit of the whole
thing to study it's structure and efficiency."*

The why matters more than the what here. A budget instruction and a structural suspicion pull in the same
direction — **spend tokens on judgement, not on typing** — and that is what produced nineteen lane seats
and ≈3.4M sub-tokens in one day. It is also what produced the session's only structural red: **FILL
reached 296,464 real and breached the 256,000 hard wall for the first time in the project's history.**
The breach is DECLARED and not excused, and the honest reading is that it was *bought*, not *suffered*:
his own instruction was the cause, the work is on disk, and what is missing is a rule about what a
session should DO at the wall. No gauge arm fires above 220,000. That gap is now item ⑫ of the carry set.

## 2. The correction that changed the method — Opus judgement, distrusted by its own author

The pivot of the day was not a ruling. It was this: *"okey you've been on opus for a while by mistake,
I'm not sure I trust its judgement, I've switched to fable, can you check its work please"*, and then
*"Fable can be used liberally when judgement is crucial"*.

What followed is the finding worth keeping. The conductor's Fable check of the Opus wave (`bf9978c`)
found **2 of 29 `$why` sentences carried a false mechanism** — sentences three separate Opus seats had
read and passed. Lane FV (`7102f9d`) read the 87 `$why` by inference and returned **6 RED of 87**. Lane
RIV (`edd33fc`) took the icons proposal to 19 GREEN / 4 AMBER / 1 RED. Lane A2V (`3a37bcd`) took the KG
audit page to 22 / 9 / 3.

**Every Opus author lane shipped a page that passed its own driver and needed a Fable seat to fail it —
five of five.** The dead end that taught the most was the verification shape itself: a verifier reading
*the proposal against the report* kept coming back green, because both documents were written by the same
seat from the same belief. Only the verifier reading *against the live file* found anything. Lane RIF
demonstrated the strongest version of it: rather than reword RI-3's recommendation, it **built a sheet of
46 live glyphs and looked at them**, and looking moved the recommendation from (a) to (c) before Dave ever
saw the page. ⇒ **Fable check + Fable verify against the live file is now the shape, on his word.**

## 3. The charts — the only three of thirteen that are in the tree

His export came back **a / a / b** with no notes, and the read-back drew *"go"*. `s277-D1` lands the 29
authored citations with two sentences replaced; `s277-D2` gives `chart-donut` the pie file (11 rules on
the donut, `dv-pie-003` donut-only); `s277-D3` takes the 19 family-level rules as a per-component authored
subset of 47 family edges with `dv-013` off `chart-bar`. `bedf383` enacted all three insert-only: 87
`obeys` edges, corpus 81 → 168, explorer v1.14.

**The residue is small and it is real:** `dv-013`'s exclusion from `chart-bar` rests on his *silence* —
the export carried no note on it — and the `parts ≤ 5` / `Maximum 6` contradiction inside
`chart-pie.meta.json` was never raised with him at all. Both are recorded as carries rather than treated
as settled, because a thing nobody asked about is not a thing anybody decided.

## 4. The icons — where the defect turned out not to be ours

The icons export came back **a / a / c / a** with two notes, and the **c** is the interesting one. RI-3
had recommended a default `activeVariantOf` for the fifteen bases carrying more than one `-active`
sibling. Dave refused it: *"I need to review this manually, many are wrong in two ways, they are not the
active variants and they are obviously labeled wrong and should have an in-active version."*

He was right, and the reason is upstream of the graph entirely. `_export-icons.py:113-118` is a
**slug-collision counter**: 31 actives across 15 bases share ONE Figma name, so the trailing `-2` / `-3`
records *enumeration order*, not variant identity. The bare `-active` is therefore not the base's twin —
on at least six of the fifteen it is a different drawing altogether (`dentist-active` is a price tag,
`renew-active` a stack of lines, `user-staff-active` a droplet+bolt).

The correction that matters for the record: **the session's first framing blamed the graph proposal, and
the second located the defect in the exporter.** `_validate_icons.py`'s twin-arm assumption is
consequently **known-unsafe on those fifteen and was shipped unchanged** — declared, not repaired, because
repairing it before his review would be guessing at the answers his review exists to give. `P-277-3`.

## 5. The audit — his instinct, measured

Three Fable lanes and a Fable verify put numbers on the suspicion in §1, and the numbers say he was right:
**3,897 nodes / 6,616 edges / 51 types**; **137 independent components** (1 giant · 36 islands · 99
orphans, every orphan a `ux:` node); **12 edge types with no consumer at all, 47% of every edge in the
graph**; **363 rule→scope edges absent**; and the headline — **6 of 12 canonical designer questions
answered, only 4 of 12 reachable AT BUILD TIME**, because nothing on the compose path reads the graph.

Two corrections inside the audit are worth preserving, because both were *ours*:

- the explorer's *"islands 2 · orphans 0"* is a **SCOPE defect**, not a healthy graph: islands are computed
  at `main():534-539` over the 1,050-node base graph, **before** `extract_extra()` appends 2,847 nodes at
  `:549`. The instrument was measuring a third of the thing it claimed to describe.
- *"730K tokens of metas"*, quoted for months, is `_compose_slice.py`'s **stale docstring**. The measurement
  is **414,755**. A number that nothing re-measures drifts, and this one had drifted by 76%.

And one that stands **uncorrected on purpose**: `A2-AUDIT.md`'s *"316 of 470 rules with no scope"* is an
edge count, not a rule count (the measure is **363**). Lane A2F corrected the *page* and deliberately left
the committed file and `e958e6d`'s commit message standing as wrong, rather than editing history. The
correction by addition is owed and is item ⑩ of the carry set.

## 6. The name, and the thing that is owed

He answered all six audit decisions **(a)** and typed one word into the free-text box: ***"record:
Constitution"***. That word is `s277-D8`: **one graph, three views by force, and the ruling record is THE
CONSTITUTION.** With it came `s277-D9` (scope per guideline file, 34 rows, instead of `obeys` × 137),
`s277-D10` (**`_compose_slice.py` wired as step 1** under a named contract), `s277-D11` (twelve reading
verbs over 51 storage types, no storage merge), `s277-D12` (tokens at group+tier — `s269-D3` honoured,
never 932 leaves) and `s277-D13` (ASK first of the five shortlisted augmentations).

Then he asked the question that the wave does not answer: *"is this slice persistent in the session? …
what if there are relevant nodes what if there are new instructions, hsould the graph act as an on-demand
RAG also"*. The conductor's read-back answer — **the thin slice is a step-1 seed, not session state; ASK
is called mid-session and reads the Constitution live** — was **written INTO `s277-D13` as its open
question rather than ruled**, which is the right call and worth naming as a method: *an answer given
during a read-back is the conductor's, not Dave's, until he says it back.* One word at #278's opener.

## 7. The resolved state, and what is still open

**Resolved:** thirteen rulings, `_rulings.json` 590 → 603, 205 insertions and zero deletions across three
commits. The charts are ruled **and enacted**. The KG has been audited end to end and the ruling record
has a name.

**Open, and most of it is his:** ten of the thirteen rulings are **law and not in the tree** — the icons
land is #278's first lane and the Constitution wave needs five lanes in a named order. `P-277-3` (the
fifteen bases), `P-277-4` (the logo review), `P-277-5` (npm distribution and the Angular/React emitters)
are parked with proven tripwires. The `s277-D13` clause, the pie cap, `dv-013` by silence, the precedence
ladder and derived scope (on the page, marked UNRATIFIED, counter-argued four ways) are unruled. And the
structural reds are inherited and unrepairable from a wrap seat: six blocking gate refusals that are all
another session's testimony in an append-only file, `_validate_roles_resolve.py` FAIL(6),
`_validate_lane_ownership.py --selftest` 2/3, 108 stale showroom pages for the fifth consecutive wrap, and
**twenty-four local commits waiting on a push that is his hand alone.**
