# #292 — the release went green and the brain was ruled three more times by his eye

provenance: 292 · 2026-09-21
status: observed

*The WHY and HOW of #292. The WHAT is in `GOOD-MORNING.md`'s ★ LATEST banner and `_LIVE-STATE.md`'s
⏱ LATEST DELTA; his words verbatim are `notes/_lanes/292/DAVE-RULINGS-2026-09-21.md`; the filed
wrap report is `notes/_subreports/2026-09-21-292-W-wrap.md`. Both-way links: this dossier is named
from the ⏱ LATEST DELTA and from the `Last refreshed` stamp.*

⛔ **NO RULING WAS INSCRIBED. `knowledge/_rulings.json` stays at 622** — verified at the wrap seat
by `json.load` over the `rulings` list with no `s292-` id present. He did not say *"inscribe"*, so
everything below that looks like a decision is a **QUESTION PUT** (`s271-D4`), never a state of the
world.

---

## 1. A four-session red died, and the cause was in a file nobody was looking at

The release job had been red at CI step 12 since #288 — four sessions, declared each time as
inherited and each time correctly, because a wrap may not repair an inherited gate fail. #291's
handoff made the re-drive its owed item 6 and said the remedy in one command.

The interesting part is not that lane C ran the command. It is **what the command found**.

`knowledge/_drive_chart_engine.py --check` compares stored receipt hashes against the current
content of what those receipts were measured on. Thirteen of them were stale. The change that
staled them was **`knowledge/canon/canon.css` moving at commit `71b3363c`, after #288** — nothing
to do with charts at all. And when the receipts were re-taken, **not one measurement changed**. The
red was not reporting a defect in the drawn output; it was reporting that the *evidence* was
attached to a file that had moved underneath it.

That is the finding worth keeping, and it generalises past this instance:

> **The freshness check has no runner.** `--check` is in neither `_build_all.STEPS` nor any CI
> step. The first thing in the whole system that said the receipts were stale was the **release
> job** — the last gate before a cut, four sessions after the edit that caused it.

⬛ **Whether `--check` becomes a step, and blocking or advisory, is Dave's.** It is put, not
proposed-and-enacted, because wiring a new blocking arm is exactly the kind of thing that must not
arrive as a side effect of a repair lane.

A second thing rode with the re-drive and is named rather than bundled into the first: the
measuring browser moved **Chromium 151 → 153**, a major version bump. The receipt records the
version; **no gate reads it**. So a re-drive on a different browser major can land silently while
that receipt is evidence for a BLOCKING `dv-004` verdict. Also his.

**Verified at the wrap seat rather than taken from the brief, and the verification produced a
correction:** the brief named the strike's receipt as *"`bc7f3b79` + CI 35588407818"*. Run
`35588407818` has `head_sha` **`6751fdeb`** — the compose-audit carry commit that followed — and
**no CI run exists on `bc7f3b79` at all**. Both facts are published: `bc7f3b79` is the commit that
carries the fix, `6751fdeb` is the sha CI first proved it green on. Neither was rewritten.

---

## 2. Three more passes on one drawing, two of them rejections — and the geometry explains why

Dave ruled the brain by eye three times today, on top of #289's six. The arc is worth recording
because the *rejections* carried more information than the acceptance.

**Lane B** read his ask — *"can we have the starting angle of the the same as the books and the
cogs"* — as "match the numeric rest angle" and moved `YAW0 10 → 35`, `PIT0 8 → 20`. The lane's own
report flagged the residual defect honestly: at `+35` the brain's plate is the **mirror image** of
the books' and the gearbox's. His verdict: ***"The angles in this preview aren't right, the cogs
and books were fine as they were."*** **REJECTED**, and the books and gearbox were never touched.

**Lane B2** took his corrected ask — *"lets angle the tray on the brain to be the same as the cogs,
with the back of the brain angled towards us"* — and flipped the SIGN rather than the magnitude:
`YAW0 +35 → −35`, with `AOV 12 → 33` chosen not by eye but to put the plate at `2.34 : 1` in plan
against the gearbox's `2.35 : 1`. It offered a `−50` alternate beside it. His verdict: ***"two up
alt is better but we need to orientate the brain so its inline with the tray as it was before, but
this is the right angle."*** **The shipped frame was passed over for its own alternate**, with a
defect named.

**Lane B3** then produced the session's best piece of measurement, and it is a single sentence:

> **`a` is BOTH the brain's front-back axis AND the tray's long axis.** The tray is `box(u, a, b)`
> over the same `a` the trace runs along. So under **one camera** the two long axes are parallel by
> construction, at every yaw.

B2's alternate was not one camera. It drew the body at `−50` while holding the tray at `−35` — a
**15° rotation of the body about `b` relative to the tray** — and that relative rotation was the
entire defect Dave's eye reported. The fix was to put it back to zero **while leaving the body
exactly where the alternate had it**: the tray follows the body to `−50`, rather than the body
being dragged back to `−35` (which is pass eight, the frame he did not pick). **One constant,
`YAW0 −35 → −50`.** Screen residual `14.81° → 6.10°`, plan split `15.0° → 0°`.

Two methodological notes that make the arc trustworthy rather than merely confident:

- **51 candidate poses were rendered and measured**, and the metric was derived in closed form off
  the orthographic projection, with a pitch-88 plan render as an independent check.
- **Blob PCA of the body silhouette was tried as the alignment metric and DISCARDED**, because at
  every useful yaw the brain's elongation runs 1.0–1.3 and the principal axis is therefore noise.
  A discarded method named is worth more than a green number.

And the costs are on the record rather than buried: `eye·a` rose to `+0.72` (more back-turn than
pass eight's `+0.54`, which is what the alternate bought and what he kept) and body foreshortening
fell `0.842 → 0.694` — **the brain is 18% shorter on screen than at `−35`.** That is the price of
the frame he picked, and he picked it knowing what it looked like.

⬛ **What is open is the plate.** It no longer sits at the gearbox's literal `−35`, which was his own
earlier ask — because *"inline"* and *"the alternate's body angle"* cannot both hold with the plate
pinned; they are the same axis. The alternate that keeps the plate at `−35` exists
(`notes/_lanes/292/B3/alt-body-23-tray-35.png`, body `−23.43`, screen residual `0.01°`) and costs an
`11.6°` plan split and a second view matrix. **Which he wants is his, and nobody guessed.**

---

## 3. A definition written before a one-shot, and the one-shot run cold on purpose

Monday on the strand map was *"overview-dashboard definition and first cold one-shot"*, and today is
Monday. Lane D did both, in that order, and the order is the point: **the definition was written
first so the one-shot had something to be graded against that was not itself.**

The definition names five regions, every composing component **with its repo path**, the layout on
the ruled bento grid, and **nine pass conditions** — four on composition-not-tracing, five on the
defect class Dave himself named at #288 (*"its all about alignment spacing and dimensions"*).

**COLD means something precise here.** The dashboard template and #288 lane P's composed page were
**both deliberately unopened** at that seat. So the output is neither a re-trace of the template —
the thing Dave challenged at #288 with *"this isn't Apollo its a dot-to-dot book"* — nor a re-trace
of the previous probe. What it *did* read is enumerated in the lane report, which is the honest way
to make "cold" a checkable claim rather than an adjective.

The page carries **13 numbered composition decisions in its own comments**, each citing the ruling,
principle or token it rests on, and **7 gaps flagged in place rather than invented over**.

His answer was to defer: ***"We need time to go over the dashboard"*** — and to attach a standing
note for next time: ***"next time can we use the cold brief we will be doing the demo with rather
than the Ai platform one."*** ⛔ **Which brief that is has not been named to the record**, and the
frozen demo prompt was declared NOT RECOVERABLE at #288, so this note needs his pointer before a
lane can obey it. Saying that is better than a lane guessing.

Nine ruling-shaped questions are attached to the definition. The one under all the others: **the
draft dashboard principles DP-01…29 are unruled, the page says so on its own face, and the
definition and every grade in it rest on them.**

---

## 4. A poster from a picture, and a deck card proven by subtraction

He attached a hub-and-spoke "Intelligent Design System" diagram and asked for *"a version of this
diagram in our swiss style, anything that we dont have currently we can fade and badge with 'coming
soon'."* The image was **READ and NOT FILED**, on the #289 precedent.

Lane H's answer is **10 tiles HAVE / 2 COMING SOON**, with **ten repo paths cited on the poster's
own face** — one per "have". That is the load-bearing design choice: a map of a design system that
cannot point at the system is a diagram, and a map that can is a claim you can check.

The two faded tiles are not symmetric and the lane said so: **CX Principles** has a parked item in
`knowledge/_parked.json` pointing at it, so *"coming"* has footing; **User Research & Insights** has
nothing in the repo at all, and may be a genuine gap or something Apollo deliberately does not own.
⬛ **A badge asserts intent either way, and which it is, is his.**

Lane P4 then put it on the deck, and the interesting part is the *method of proof*:

- **The insertion is ONE contiguous 15,456-character block**, and the claim "v12 is untouched" is
  demonstrated by **subtraction**: strip the block and what remains is v12 exactly, byte for byte.
  That is a stronger statement than a diff read by eye.
- **Ids were not renumbered, and that was MEASURED FIRST rather than assumed.** The chassis
  navigates positionally off `deck.scrollTop / deck.clientHeight` with no hash router and no `#sN`
  lookup — so `s11` and `s12` keep their names and the new card takes `s10map`, deliberately
  outside the `s<N>` sequence so nothing matching `s11`/`s12` can collide.
- **It is inline markup and scoped CSS, not the PNG**, so it scales with the slide box and prints
  as type.

Re-measured at the wrap seat: **thirteen `<section class="slide">` blocks, every one id'd, `s10map`
eleventh of thirteen** — P4's declaration reproduces exactly.

His verdicts: ***"the design system map is good for now as a placeholder, we'll refine later. we can
slot it after slide 10"*** and ***"the slide is great for now."*** **Accepted as a placeholder,
which is not an inscription.**

⬛ **The counter came with it and is unresolved: thirteen cards, twelve of them reading `NN / 12`,
and the new one reading `10A / 12`.** Honest about being an insertion, and it disturbs nothing —
but a sweep to `NN / 13` is the obvious next move once the map stops being a placeholder, and
whether the id follows into the sequence is the second half.

---

## 5. The instrument was overridden once and then obeyed, for a second consecutive session

The seam check fired five times across the window. At **FILL 180,850 real / 18 turns** it read the
stop line as passed, and that was quoted to him in chat. **His answer was one more note** — the
brain inline with its tray — lane B3 ran, and the wrap came on ***"wrap when you're ready."***

⇒ **#283 and #290 stopped ON the instrument. #291 and #292 each overrode it exactly once with a
note and then obeyed.** That is the same shape twice, and **n=2 is an observation, not a pattern.**

⛔ **No rule is invented from it here, and the temptation to invent one is the reason this paragraph
exists.** It is evidence about `s283-D1`'s tolerance arm and nothing more: a *blocking* arm would
have refused a lane Dave asked for, both times, and whether that is what he wants is his alone.

One thing the second datapoint does add, and it cuts against alarm rather than for it: **the
override was cheap.** #291's cost 44,412 real and closed 8,714 past the 256,000 hard figure;
#292's cost 7,391 and closed with 200,000, 220,000 and 256,000 all clear. An overrideable
instrument produced a well-inside window this time. One reading is not a trend either.

---

## 6. Where this wrap's own honesty was tested

**(a) The 2d EXIT CHECK caught something real, and it was caught by probing rather than by
reading.** The #289 ⏱ delta was about to roll to the archive. Scanning it for ⚠/⬛ items surfaced
*"Dream pass 13's seven proposals are still unruled"* — and probing all 611 items of `_CARRIES.md`
§ `residual → #292` for *dream pass 13*, *dream 13*, *dream-13* and *seven proposals* returned
**none**, while dream pass **12** has a carry and pass **11** has two. **The seven had been living
on the #289, #290 and #291 ⏱ deltas — all three of them rolling surfaces — and would have left live
state the moment that block moved.** It is now carry ⑩ in § `residual → #293`, copied up **before**
the roll, which is the order the rule specifies and the reason the rule exists.

**(b) Nothing was struck that could not name where its correction is inscribed.** Three candidates
presented themselves and only one qualified:

- **The chart-engine re-drive** — struck in `_HANDOFF-143`'s owed list with its receipt. It has no
  numbered carry of its own in `_CARRIES.md` (probed, four hits, all of them other carries' prose),
  so `s183-D1` — which strikes a HEADLINE and never a clause — had nothing to touch there.
- **His slide-by-slide read** — **HALF, and NOT struck.** He has read the deck; his notes are not
  given. The change is minted as a new item instead.
- **Parts on slide 10** — he answered it: *"The cogs are fine for now."* ⛔ **Still not struck**,
  because `s188-D2` requires the retraction to name **where the correction is inscribed**, and
  nothing was inscribed. An explicitly provisional acceptance by eye has no inscription to point
  at. *"A strike that is wrong is worse than an item that is merely stale"* (`s271-D4`).

**(c) The banner cap stopped being a girth constraint and started shaping the record.** The ★ LATEST
banner was drafted over the `s241-D2` cap and shortened **six times**. Five of those were trims. The
sixth — the one that actually worked — was **merging two bullets into one**, so a session with ten
ruling-shaped carries is represented on the banner by five bullets. It closed at **1,198 / 1,200
tape on 9 of 10 lines: two tokens of headroom, the tightest reading this record carries.** That is
reported, not appealed — the cap is Dave's — but it is a different complaint from the one
`s214-D6` was written to answer. [[gate-inside-the-growth-loop]]

**(d) The `subs` disagreement is systematic, and saying so is more useful than saying it is small.**
Measured **1,257,555 (n=9)** against declared **1,263,895 (n=9)** — 0.50% apart. But **every one of
the nine measures BELOW its declaration, by between 329 and 1,120 tokens, never above.** A one-sided
residual on all nine is what a definitional gap looks like, not what measurement error looks like: a
sum of final-FILL readings is not a sum of cumulative tokens billed. Both figures stand and neither
is corrected into the other [[measure-dont-convert-units]].

**(e) The window identification was the strongest the `s214-D5` field has carried.** The hand-over
`delta` is only meaningful when both terms read the same window. Here they do, one turn apart, and
the window is identified by **six independent agreements** rather than one: every seam reading the
conductor declared — 145,281 / 5 · 164,001 / 8 · 173,669 / 13 · 176,438 / 16 · 180,850 / 18 ·
187,287 / 23 — reproduces at the wrap seat with **zero difference**, and the boot agrees to the
token at 74,170. `delta` = **954 real**, the smallest on record.

**(f) No eighth gate fail was born by the mandated 2f roll — and it was TESTED, not trusted.** The
gate's own `_parse_boot_samples` was run over the exact text the roll would append and returned
**one** row for #291. Post-roll the breach list still reads **seven**, because **#281 fell out of
the sliding window as #291 came in** — the same reading as #290's and #291's, now a **third**
occurrence, declared rather than left to be re-discovered a fourth time.

---

## What is resolved, and what is still open

**Resolved:** the release job is green end to end (first in five sessions); the brain rests inline
with its tray at the angle he picked; the Swiss design-system map exists and is on deck v13 as a
placeholder; the overview dashboard is defined and has a first cold one-shot; Parts on slide 10 is
the gearbox *"for now"*; the *"almost"* on the workers is answered — the finessing is to be done
**together**.

**Open, and every one of them his:** his v12/v13 notes, and the four D2 layout flags and the dark
robots slide they gate · lane B3's plate question · whether `AOV` widens past 33 · the two
hidden-line flaws lane B2 named · the deck's own brain, three passes behind the drawing file · the
counter on thirteen cards · the receipt-freshness runner, blocking or advisory · the Chromium-major
declaration · lane H's two faded tiles and the *"Data & Insights"* reading · lane D's nine · the
dashboard review and the next one-shot on the demo's own cold brief, **which has not been named** ·
dream pass 13's seven · proposal v3 · index sharding · the memory archive's 162 B · the 5b-versus-cap
conflict · the two-probe-shape question, now at its twenty-fourth session · **and the internal
Friday the 25th, FOUR days out.**
