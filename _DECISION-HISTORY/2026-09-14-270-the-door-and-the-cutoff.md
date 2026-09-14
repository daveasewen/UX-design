# #270 — the door and the cut-off

provenance: 270 · 2026-09-14
status: observed

*Narrative dossier (capture-ritual step 1b). The WHAT lives in `knowledge/_rulings.json` (`s270-D1`),
`_LIVE-STATE.md`'s ⏱ LATEST DELTA and `GOOD-MORNING.md`'s ★ LATEST banner; this file holds the WHY and
HOW. Both-way links: spine → `_LIVE-STATE.md` § ⏱ LATEST DELTA 2026-09-14 (#270); ledger →
`knowledge/_rulings.json` § `s270-D1`; contract → `_HANDOFF-121-the-door-and-the-cutoff.md`.*

---

## Where the session started: one word, and it was yes to both

#269 ended with a question it deliberately refused to answer for Dave — the **compose-time door**, a
third door on the retrieval spine that takes a task in and returns a closed context slice. #269's wrap
carried it as ASKED, NOT ANSWERED, with no recommendation attached, because his last words on it had
been a question about heat rather than a yes.

He answered it at the #270 opener in eight words: *"cool, lets do both in teh oredr you prefer"*. Both
means the door **and** the roles/DESK lane that `s269-D1`'s accepted order had put first. The order was
the conductor's to choose and the reasoning is worth recording because it is not arbitrary: the door
slices by ROLE, and roles were not in the graph. Building the door first would have meant building it
against a data shape that lane 1 was about to change. So lane 1 went first, the door second, and the
research lane ran alongside both because both of them need the same missing thing — a `when` predicate
that says which provider to pick.

## The pattern the session repeated three times: generate, don't land

All three lanes came back with a generator, a proposal page and nothing written to canon. That was not
timidity. `s269-D1` through `s269-D6` had just settled the ENTITY vocabulary, and the #75 closed
vocabulary for EDGE types is Dave's; a lane that generates 115 edges and lands them has made his
decision for him by the time he reads about it.

So `knowledge/gen_kg_roles_desk.py` was built with its `--land` path **refusing to run without a
recorded ruling id**, and — this is the part that matters — the conductor MUTATION-TESTED that refusal
rather than asserting it. A guard that has never been driven against a mutant is documentation
[[mutation-tests-the-clause-not-the-feature]]. The dry run measured 115 edges / 45 nodes over 26 metas,
and `_validate_kg.py` was driven twice on scratch: GREEN with the schema diff applied, RED with 100
failures without it. The diff being load-bearing is therefore a measurement and not a claim.

The same lane surfaced a drift nobody was looking for: `knowledge/roles.json` carries 108 memberships,
but only 24 metas carry a `provides` field, and 4 roles have no provider in any meta at all. The `when`
predicate reproduces on 81 of 108. That was REPORTED and left alone — repairing a drift found while
building a generator is how two unrelated changes end up in one commit.

## The door, and the conductor publishing its own defect

Lane 2 built `knowledge/_compose_slice.py`: task in, closed context slice out, twelve bites of which two
were mutation tests. The slices measure roughly six times smaller than the metas they replace and
twenty-five times smaller than the library, which is the whole argument for the door in one number.

The interesting decision was what to put on the proposal page. The conductor's own drive of the door on
an approvals-queue task went wrong: it picks providers by **word-match**, so it chose `meter` and
`summary` for "status badges" and left `badge` and `table` sitting in `unresolved` as prose. The page
published that run rather than a cleaner one. The reason is [[art-director-reviews-lane-output-268]]'s
sibling — a proposal that shows only its best case is asking for a yes on evidence that has been
curated, and the defect is exactly the thing Dave's § C direction later addressed.

## The correction: the numbers were never in the building

Lane 3 went looking for the `when` predicates and came back having corrected the conductor. The
conductor had said the record-list `when`s did not exist. They do — they are in `knowledge/roles.json`
(table "default, read-mostly"; data-grid "sort/filter/select/edit-in-place"; list-items "≤3 fields,
tappable"). They are in the wrong home and no gate reads them, which is why they read as absent. That
is a different defect from the one that was claimed, and the honest form is to name both.

For selection controls the finding was harder and more useful: 27 of 27 carry `when: null`, and the
HSBC sources are silent **by construction, not by omission**. The Common Toolkit component specs —
Dropdown, Selection controls, Segmented control, Input fields — and the forms prose node `45226:149920`
have never been ingested. `knowledge/guidelines/forms.md:40` names the node and `_INGESTION-QUEUE.md`
still lists it as Queued. So the corpus could not have answered the question, and no amount of searching
it harder would have helped. Sixteen own sources plus forty-nine external ones later, the switch-vs-
checkbox boundary resolved cleanly on "effect is immediate", 5 of 5 systems agreeing — and the
single-select cut-off resolved on nothing at all.

## The cut-off: a number that came out of Dave's head, and what we did about that

Asked whether a dropdown is our default single-select or our last resort, Dave said *"If I remember
correctly we use dropdowns for 5 and above"*, and when it was put to him that the number was in no file
we hold, *"okay lets do it from my memory 5 is the cutoff"*.

The decision this session made — and it is a decision about the RECORD, not about dropdowns — was to
inscribe it as `s270-D1` while making its provenance impossible to lose. Three things carry that:

1. The `ruled` field states the reading (radio ≤ 4, dropdown ≥ 5, dropdown as DEFAULT rather than last
   resort) and **labels it as the conductor's reading**, not as Dave's words. His two sentences sit in
   `says`, verbatim. This is the distinction #269 built the quote gate to protect.
2. The `ruled` field also names every place that was checked and came back empty — guidelines,
   `roles.json`, both metas, the Memento index, `_rulings.json` — so a later reader cannot mistake a
   recollection for a citation.
3. `P-270-1` in `knowledge/_parked.json` fires on the `guidelines-ingest` event. If the Figma pages say
   something else, the Figma number wins and the ruling is corrected BY ADDITION, never re-dated.

The alternative — waiting for Figma access before recording anything — would have left the number in a
chat transcript, which is where facts go to die. The alternative on the other side — recording it as
canon — would have made a recollection indistinguishable from an ingested source. The tripwire is what
makes the middle position honest rather than merely comfortable.

## What was deliberately NOT ruled

Four edge types (`providesRole`, `answersIntent`, `hasDataShape`, `yieldsTo`) are sitting at the door of
the closed vocabulary with a proposal page asking Dave for one word. The door's step-1 switch,
advisory or blocking, is his. Whether the record-list `when`s move from `roles.json` onto the metas is
his. So is splitting `selection-controls`, the multi-select boundary, the combobox threshold, and every
#119 open, which stands exactly as #119 phrased it.

And his § C sentences — *"three compositions that are all defensible under the same rules"* and *"maybe
the logic is cast the net wider for the slice, the slice carries the scoring so if variations asked for
there is scope to substitute"* — are carried as a **DIRECTION, not a ruling**, with no `sNNN` minted for
them. That is a deliberate restraint: turning a design direction into a ruling id is how a conversation
becomes a constraint nobody agreed to.

## Resolved state, and what is still open

Resolved: the door exists and is measured; roles and DESK fields have a generator that refuses to land
unsupervised; the `when` gap has a cause (never ingested) rather than a mystery; the cut-off has a
number, a label on its provenance and a tripwire.

Open and Dave's: everything in `_HANDOFF-121-the-door-and-the-cutoff.md` § D, plus the three structural
reds this wrap carried rather than repaired — the sixth consecutive boot-ceiling breach, and the #243
and #264 boot double-counts, where #269's separation stands: #264's is a real restatement inside one
block, #243's is a mis-attribution that binds #255's figure to #243's name, which makes the #243 half a
gate defect rather than a record defect.
