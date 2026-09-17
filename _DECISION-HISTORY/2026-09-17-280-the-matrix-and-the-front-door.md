# #280 — the layout matrix, and the explorer becomes the front door

provenance: 280 · 2026-09-17
status: observed

*Session #280, opened 2026-09-16 in the evening and wrapped 2026-09-17. Conductor **Fable 5.1**,
**eight Opus lane seats**, delegated wrap (this dossier written at the wrap seat). Spine entry:
`_LIVE-STATE.md` ⏱ LATEST DELTA #280. Ledger: `knowledge/_rulings.json` § `s280-D1`, § `s280-D2`.
Handoff: `_HANDOFF-131-the-matrix-and-the-front-door.md`. His words verbatim:
`notes/_lanes/280/DAVE-RULINGS-2026-09-17.md`. The eight filed reports are
`notes/_subreports/2026-09-1{6,7}-280-*.md`.*

*This file holds the WHY and HOW. The WHAT — the two rulings and their pins — is in the ledger and
the spine, and is not restated here.*

---

## 1. The session started inside somebody else's refusal, and the first decision was not to argue

#279 ended with Dave looking at explorer 1.16 and saying *"this does not look like 3 layers, just
relabelling and grouping them isn't what I expected tbh."* The #279 wrap recorded, correctly, that
nobody had done anything wrong: `s277-D8` as inscribed said *storage untouched; chips and family
labels change*, and the lanes had built exactly that letter. So the gap was not a defect to repair,
it was **an expectation that had never been elicited**.

The temptation at that point is to reason about what he meant. #280 did not. The instruction the
#279 wrap left — *"#280's FIRST move is a page carrying ONE concrete option, not a description of
one"* — was followed literally: lane LY built the option and shipped it as a page with **one
question at the bottom and a switch that defaults to the old behaviour** (`b212ca2`, explorer 1.17,
canvas md5 identical at page defaults).

**The why:** a page that changes nothing until he answers costs one lane and forecloses nothing. A
ruling written from an inference costs a session and forecloses everything.

## 2. His answer was a better question, and the second decision was to draw rather than argue again

He did not answer the question that was asked. He wrote: *"I actually like the strata, maybe we just
have multiple views, could the strata possibly be 3d too?"*

That is three propositions in one sentence — strata is good, multiple views may be the answer, and
3D may be available — and none of them is a decision. **The dead end that was not taken:** reading
that as approval of strata and building strata-3D. It would have been defensible and it would have
been a guess.

Instead lane LS drew **four** shapes for the same three views — strata, shells, floors, orbits —
every picture rendered **from the real node data** (4,562 nodes, 7,528 relations, the page's own
predicate over the live KG, with each caption stating its own sample) and put them on one page with
one question. Drawing four costs more than arguing for one; it is also the only way to find out that
the answer is none of them.

## 3. The answer was none of them, and that is what made the matrix

His export at 20:30Z chose `other`, kept all four, and wrote: *"Okay I want all of these plus the
original view, in 2d and 3d for all of them. just keep force as the default"*.

**That sentence is not a fifth sketch. It is a matrix** — three layouts × two dimensions, six cells,
one switch — and the finding that made `s280-D1` cheap to write is that **the four sketches map onto
it without remainder**: FLOORS *is* strata-3D and ORBITS *is* shells-2D. Nothing he asked for was
missing and nothing had to be invented to fill a hole. Lane LM inscribed the ruling **first** and
then built it in three commits (`b5df9c9`, `eddf87a`, `c3805ec`), with `?layout=` and `?dim=` so any
cell can be photographed without the page ever being clicked, and a contact sheet putting all six in
front of his eye at once.

**What was declared out rather than quietly dropped:** the shells-3D cutaway, and equal plate/ring
sizes per layer. Both are build decisions taken inside a lane, and both are written down as such —
they are not rulings and they are not defects.

## 4. The explorer's second thread: he kept following his own sentence further than the question

Lane EX3 went in to fix two irritations on 1.18 and found a third thing. The legend *"jumps from the
side to the bottom when you interact with it"* — and it did: since 1.16 the page recomputed the
legend's home on **every redraw**, so a family chip that widened the graph threw the legend across
the page while his hand was still on the chip. The fix is small (choose once at open, remember the
choice) but the measurement underneath it is the keeper: **1.18's rule "every non-force layout takes
the bottom strip" put the legend in the WORSE place in 4 of 6 cells** — a default derived from one
cell and applied to six. His word on the fix: *"good"*.

Then he answered EX3's new INSPECT modal with something much larger than a bug report:

> *"I want to see any artifact that exists here, including a render of the actual component snippet,
> this is such a good mental model that it becomes a great explorer for the entire system"*
> ... *"no i want to inspect the edge or indeed the actual file, a component for example"*

**That is a change of what the explorer is for**, which is why lane EX4 inscribed `s280-D2` before
building rather than treating it as a feature request. INSPECT now opens the **artefact, by kind** —
a component renders its snippet live, a rule opens its guideline scrolled to its own highlighted
row, a ruling opens its record, an icon is drawn at 48 and 16 px on both grounds — and anything with
no renderer yet still opens as the raw file **named by its type**, so *"nothing built for this yet"*
never looks like *"there is nothing here"*. Relations became doors too, with a trail.

**Two honest limits came out of it rather than being discovered later.** A `file://` page may not
read the file beside it, so the explorer is now **served** (`knowledge/_serve_explorer.py`) and the
page says so out loud when it is not. And **snippet scripts are stripped in the sandbox**, so a
script-driven component renders as its markup — declared, not hidden.

**The finding that would have been a false alarm:** 1.20's canvas md5 changed. It changed **by data,
not by picture** — `s280-D2`'s own five governance nodes moved the ghost hatch — and the lane proved
it with a 2×2 rather than asserting it. A pixel-identity claim that is allowed to fail loudly is
worth more than one that is quietly weakened.

## 5. The icons: the value was in what was NOT written

Dave's 15-base review came back at #279 and the standing instruction was explicit: *where flag and
note disagree the NOTE is his sentence — ask, do not guess.* Lane IN inscribed the **nine** rows
where tick, note and twin all said the same thing, and put the other **six** back to him as one
question each on a page. Lane IN2 read his answers and landed **five** more.

The sixth is the point. `jade-lifestyle` came back `choice: "open"`, `twin: null`, with the note
*"jade-lifestyle-active-2 - think is the most likely the correct icon"*. **Nothing was written into
the library for it** — no default, no entry on the mislabelled list — and his sentence sits on the
empty slot. The record carries his lean without anyone turning a lean into a decision.

The durable half is the generator: `gen_kg_icons.py` now **rebuilds the fourteen from his own
exports and refuses on disagreement** (22/22, mutants 32/32). Before that, a regeneration would have
wiped his answers. **A decision that only lives in the output is not inscribed; it is waiting to be
overwritten.**

## 6. The census: counting is not planning, and the lane refused to conflate them

On a screenshot of the pink UX cloud he asked *"do we have a plan to wire up the orphans etc?"*.
Lane OC answered **the counting half only**: **157 of 4,618 nodes have no line any chip can draw**,
four causes, ten sets, each set a radio on a page.

The two largest sets are the reason the halves had to be separated:

- **100 of the 145 UX principles are dark**, 99 with no edge of any kind in storage. This is **a
  switch left off, not a gap in the vocabulary** — the principle generator can already emit a
  principle's research family and the sources it was graded on, both behind flags since `s275-D2`.
  ⛔ But turning the first on **puts a family node on the stage**, a new kind of thing, and that is
  Dave's word and not a lane's.
- **94 base `rule:` dots** are not orphans at all. They light the moment the HSBC `rule:` chip goes
  on — a default, read as a defect.

His word on the census was *"cool"*. **His export has not arrived, and until it does the census is a
count and not a plan.** That is #281's first move.

## 7. What this session says about method

Four lanes and one export beat a guess, twice — once on the layout and once on the icons — and in
both cases the cheap move was to **show him something and let the answer be a surprise**. The
recurring shape, now with several samples behind it:

1. **Build ONE option that changes nothing until he answers**, not an argument for an option.
2. **When the answer is a new question, draw the alternatives** instead of reasoning about which he
   meant.
3. **Inscribe the ruling before building it**, so the build has something to be graded against.
4. **Write down what was NOT decided** — the open row, the deferred cutaway, the stripped scripts —
   in the same pass, because that is the part that evaporates.

## 8. Resolved, and still open

**Resolved:** the layout question (`s280-D1`) · what the explorer is for (`s280-D2`) · fourteen of
fifteen icon bases · the legend's home · the orphan count.

**Open, every one a question put and not a state of the world (`s271-D4`):** his **census export**
(ten radios, not received) · the **eye-check of the six cells** (the conductor expects Floors or
Orbits to go — an expectation, not a finding; no lane may thin a ruled matrix on it) ·
**`jade-lifestyle`** · the shells-3D cutaway and the sandbox's stripped scripts · **`s277-D12`
(tokens at group+tier), still never started** and bumped a second session · and the four questions
carried unchanged from `_HANDOFF-130`.

**Links back:** `_LIVE-STATE.md` ⏱ LATEST DELTA #280 · `GOOD-MORNING.md` ★ LATEST #280 ·
`knowledge/_rulings.json` § `s280-D1` / § `s280-D2` · `_CARRIES.md` § `residual → #281` ·
`notes/_subreports/2026-09-17-280-W-wrap.md`.
