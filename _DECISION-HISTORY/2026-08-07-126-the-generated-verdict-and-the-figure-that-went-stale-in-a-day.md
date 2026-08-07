# #126 — the generated verdict, and the figure that went stale in a day

```
provenance: 126 · 2026-08-07
status: observed
```

**Spine entry:** `_LIVE-STATE.md` ⏱ LATEST DELTA #126 · **Ledger:** `notes/_MEMENTO-DECISIONS.md` § ★ #126 ·
**Rulings:** `knowledge/_rulings.json` (`s125-D1` — RULED #125, ENACTED #126) ·
**Banner:** `GOOD-MORNING.md` ★ LATEST #126.
Both-way links per `_DECISION-HISTORY/README.md`.

---

## 0. What this session was, and the half of it that did not happen

The title Dave confirmed at the opener, by explicit option-select (*"Title lane as written"*), was
**`Apollo - #126: enact s125-D1, then draw the schematic`**. Two named halves. **One landed.**

`s125-D1` is enacted. **The schematic was not built.** The window ran out and the wrap was delegated at
FILL 135,735 against the 150,929 stop line — roll, not ride — and the schematic was never started, for
exactly that reason.

That is the second consecutive session titled partly for the schematic that did not build it. #125 was
redirected away from it at its opener; #126 priced it behind the enactment and never reached it. The
honest reading is **not** a motivation problem: **the schematic has never been given a window of its
own.** It has twice been the second item on a two-item lane, and the second item on a two-item lane is
the item that pays for the first one's overrun.

The title is a **LABEL**, not a deliverable claim. It is written down here first because a cold reader
who finds a confident title and no artefact spends real tokens looking for the artefact.

---

## 1. The ruling, and why the obvious enactment would have been wrong

`s125-D1`, ruled by Dave at #125: the chain banner's build-step count **stops being a typed number and
becomes a generated figure** — `_gen_chain.py` reads `len(STEPS)` out of `_build_all.py`'s AST at
generation time. He chose this **explicitly over a third re-stamp**. The count had already been
re-stamped 72→75 once and classified *"Perishable reading"*; the class then recurred on the very line
that named it.

The obvious enactment is one line: read the live count, substitute it. **It would have published a
sentence nobody has ever measured.**

The banner's standing text was *"ALL 75 STEPS ASKED AND GREEN (#62)"*. Substituting only the live count
turns that into ***"ALL 98 STEPS ASKED AND GREEN (#62)"***. But `#62`'s green verdict was taken against a
tree that had **75** steps in it. The other 23 were never in that run. The sentence would have been
manufactured — **by the very fix whose purpose is to stop manufactured claims.**

This is the dead-end worth recording, because it is not obvious from the ruling's text. A ruling that
says *"generate the number"* does not say *"and check that the sentence around the number is still true
once you do."* The generator inherits the sentence.

### The decision: two numbers, and a computed gap

So **both ends are measured**:

- the **working tree** — `_steps_in()` parses `_build_all.py`'s AST → **98** steps, 98 distinct labels;
- the **commit behind the green claim** — `git show 18c7789:knowledge/_build_all.py`, same parser →
  **75** steps, 75 distinct labels;
- and the **shortfall is computed**: **23**.

The chain now reads: *"⛔ BUILD VERDICT: 75 of 98 steps green (#62, `18c7789`) — 23 steps have NEVER
been in a green verdict. Both counts GENERATED from `_build_all.py`'s AST at each end; the shortfall is
computed (`s125-D1`)."*

The 1:1 agreement between step count and distinct labels **at both ends** is what licenses calling them
the same object measured twice, rather than two different things that happen to be countable.

### `VERDICT_SHA` is typed, and that is deliberate

`VERDICT_SHA = "18c7789"` is a hand-typed constant, in an enactment whose entire point is removing
hand-typed constants. The distinction is the one that matters: **it names a fixed historical event.** A
commit sha for a past verdict cannot go stale the way a COUNT does — the past does not acquire new build
steps. Everything *derived* from it is measured. If the sha ever becomes unreachable, the mutation
battery proves the code **declares the coverage unmeasured** rather than quietly publishing the live
count alone.

---

## 2. Where the splice lives, and why it is not where the ruling says

The ruling names `_gen_chain.py`. **The AST reader is there, as ruled. The splice is not** — it is a
20-line, purely additive, zero-deletion block in `_capture_gate.chain_parts()`.

The reason is a mechanism, not a preference. `chain_parts()` is **the one slicer**:

- `read_chain_tk` measures **exactly what `chain_parts` returns**;
- `_gen_chain` writes **exactly what `chain_parts` returns**.

Text injected downstream of the slicer would therefore be **written but not measured** — the chain file
would carry bytes the size stamp had never seen. That is the #41 second-consumer drift, and
`chain_parts` was extracted specifically to make it impossible. `dofirst_index` is composed inside the
slicer for the identical reason.

**This is an implementation reconciliation, not a re-ruling**, and it is flagged as visible to Dave in
the banner, in the delta, in `§ OPEN` and in the ruling record. The substance Dave ruled — the figure is
read from the AST, never typed — is intact. Only the seam at which the rendered line enters the chain
moved, and it moved *toward* the measurement rather than away from it.

The general form is worth keeping: **an instruction can be right while its stated cause is wrong for the
current code**; verify the reason against the call graph before obeying the letter.

---

## 3. The finding: the premise demonstrated itself inside one day

#125's probe measured `len(STEPS)` = **97**.
#126's enactment measured **98**.

The difference is `s125-D2` — #125's *other* ruling, which un-exempted `_validate_state_contrast.py` and
wired it into `_build_all.py`. It added a build step **between the probe and the enactment**.

**The figure went stale again in under twenty-four hours, inside the session pair that existed to stop
it going stale.** No process failed here; nobody was careless. The number is simply attached to a thing
that changes whenever the project works properly. That is the whole argument for a generator over a
fresher value, and it argued itself.

★ This is the sharpest evidence #126 produced, and it is evidence for a ruling that was already made.

---

## 4. The second finding: 23 steps have never been inside any green verdict

This one is **new**, and it is a finding rather than a restatement.

While the figure was a single typed number, the gap was **unstatable**. You cannot notice that a verdict
under-covers the tree if the verdict and the tree are the same number by construction. Measuring both
ends produced the statement as a by-product:

**23 of the 98 build steps have never been asked inside a green single-process build.**

⚠ It says nothing about whether those 23 pass. It says the published verdict has never covered them. A
full single-process `_build_all.py` run is sandbox-impossible (~49s against the ~45s call kill), so
closing it belongs to CI. It is standing at `_LIVE-STATE.md` § OPEN, **not ruled, not scheduled, not
waived.**

---

## 5. What re-checks this?

`s125-D1` exists because a claim went stale with nothing watching it. An enactment that answers the
ruling but leaves the same hole open would be a fix in the same shape as the defect.

**Five permanent bites were wired into `_gen_chain.selftest()`**, which is already a registered build
step. The load-bearing one **re-derives `len(STEPS)` from disk at test time and asserts that the chain
publishes that number.** It cannot be satisfied by a constant, because it computes the expectation from
the same source the code reads and compares two independently obtained values.

The mutation battery — **12 bites, 0 fail** — proves the clauses individually:

| mutation | required behaviour | observed |
|---|---|---|
| add a step to `STEPS` | published figure moves 98→99, gap 23→24 | ✅ |
| rename `STEPS` | **refuse BY NAME**, publish NO count | ✅ |
| make `STEPS` non-literal | refuse | ✅ |
| unreachable `VERDICT_SHA` | declare the **coverage** unmeasured, keep the live count | ✅ |
| duplicate a label | **surface it**, never count it as growth | ✅ |

`_build_all.py` was restored **byte-exact (sha256 verified)** after every mutation — the mutation harness
must not be the thing that changes the object it measures.

★ Note the shape of the fourth row. A failure of the historical half degrades the output to *"the live
count, coverage unmeasured"* — it does **not** fall back to publishing the live count as if it were
covered. **A declared gap passes; a silent one fails.**


### And then the bites bit this wrap

The marker-leak bite went **red during #126's own wrap.** The banner and delta text above, as first
written, *mentioned* the marker literally while describing the enactment — and both are chain-resident, so
the raw marker appeared twice in `_CHAIN.md`.

A **mention** inside chain-resident text is indistinguishable, to a cold reader, from a **failed
substitution**. That is precisely the state the bite forbids.

The gate was right and the prose was the defect. **The prose was rewritten; the bite was not touched, not
scoped, not exempted.** A green selftest can never supply this: an instrument driven on real data,
failing, on the day it was built. The 12-bite battery proved the clauses — this proved the feature.

---

## 6. Home by addition, then cut

`GOOD-MORNING.md` line 10 carried a 371-character typed segment: *"⛔ **BUILD VERDICT: "ALL 75 STEPS
ASKED AND GREEN (#62)" … RULED #125, NOT ENACTED**…"*. It is now the 17-character marker
`{{BUILD_VERDICT}}`.

The order was: home first, cut second. Its narrative was already at `_LIVE-STATE.md` § OPEN and
`notes/_MEMENTO-DECISIONS.md` § ★ #125 **before** the segment was removed, and the full reasoning now
lives as comments in `_gen_chain.py` — beside the code, where the next person to touch the generator will
be standing.

---

## 7. What we got wrong, and what we found and did not fix

**The `_capture_gate.py --selftest` red is not this session's.** `_governs.py` fails because the ruling
`s121-D1` points at `knowledge/canon/canon.css:5548`, and that line does not exist.

The temptation on finding a red during your own enactment is to assume you caused it. The temptation
after that is to fix it. **Both were declined**, and the attribution was *checked* rather than assumed:
`_governs.py` and `canon.css` are untouched in `git status`, and #126's `_capture_gate.py` diff is 20
lines with **0 deletions**, entirely gated behind `if "{{BUILD_VERDICT}}" in gm_part`.

★ It is the same class as #125's three, in a **fourth medium**: prose · a comment · a return value ·
and now **a pointer**. A claim that was true when written, went false, and has nothing that re-checks it.

⛔ Recorded standing at `_LIVE-STATE.md` § OPEN and **not fixed**. A wrap that repairs whatever it
happens to trip over is a wrap that ruled its own scope.

**Also found, also not fixed:** the DO-FIRST pointer *"The build does NOT fit one ≤45s call — MEASURED
#62: ~49s for all 75 steps"* carries the same stale 75. It is honest as a dated #62 measurement, and its
conclusion is *more* true at 98 steps than at 75, so it misleads in the safe direction — but it is the
same class, and hand-correcting a historical measurement is the act `s125-D1` forbids. Recorded, left.

**A working-tree reconcile, declared:** `knowledge/_rulings.json` arrived at this wrap with a 2,310-line
diff for **one** semantic change — the file had been re-serialised at `indent=2` with a trailing newline
where the committed form is `indent=1` with none. A control proved the point before anything was touched:
`json.dumps(HEAD_parse, indent=1, ensure_ascii=False)` reproduces the committed bytes **exactly**
(sha256 match). Re-serialising the working copy the same way collapsed the diff to **10 lines**, and a
parsed old-vs-new comparison confirms `s125-D1` is the only entry that differs. Formatting churn that
buries the one real change is not cosmetic — it is a diff nobody can audit.

---

## 8. Gauge

**Boot 53,997 real** (`message.usage`, first turn) — the **fifth** datapoint below the published 75,899
floor, and consistent with the post-break n=3 mean of 54,859.

⛔ **Recorded, not re-based. The re-base is Dave's and remains untaken.** Five readings disagreeing with a
published constant are evidence, not authority.

FILL check-ins **74,120 → 135,735** against the stop line **150,929**. The wrap was **delegated at
135,735** — roll, not ride. Conversation-half throughput at the seam: **175,569 real**.

⚠ **Dave's quota panel was asked for at the opener and not given.** It is recorded as **UNKNOWN**. No
figure was estimated in its place: an instrument that guesses when it cannot measure is the defect this
whole session was spent removing from a different instrument.

---

## 9. Resolved state, and what is still open

**Resolved:** `s125-D1` is enacted, mutation-proven, and permanently re-checked by a build step.

**Open, carried to #127:** the schematic v2 (Dave's #125 pick, **rolled twice**) · `effBg` sibling
blindness · `out[3]` overwrite + the stale audit + the `IndexError` + the missing `--selftest` ·
**the render-runbook contradiction, owed at #126 and NOT DONE** · the 4 real contrast failures (Dave's) ·
the new `_governs.py` red · the 23 uncovered build steps · and the carried set, on its **thirteenth** roll.

**Nothing was ruled at this wrap.** No value changed, no gate, threshold or fence was edited — including
`G4`, whose §C 164-vs-150 warn was printed and proceeded past. Warn ≠ block; the cap was not moved.
