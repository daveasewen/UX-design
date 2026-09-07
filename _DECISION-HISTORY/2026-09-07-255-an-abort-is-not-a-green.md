# #255 — an abort is not a green: the session that paid the bento debt and found a gate that had been silent for six sessions

provenance: 255 · 2026-09-07
status: observed

*The WHY and HOW of 2026-09-07's second session (#255). The terse WHAT lives in `GOOD-MORNING.md`'s
★ LATEST banner, `_LIVE-STATE.md`'s ⏱ LATEST delta, `knowledge/_rulings.json` § `s255-D1` and the
five filed lane reports under `notes/_subreports/2026-09-07-255-*`. Both-way links at the foot.*

---

## 1. The session was named for a debt and the debt was the easy half

`#255` opened as *"pay the bento debt, collapse intent"* — a title the #254 wrap wrote from the one
thing its runner had surfaced: five reds in the bento template, none of them #254's, all of them
authored across #248–#251 and invisible until `canon.css` finally rebuilt from #251's DP-08 snippet.

Lane A paid all five, and the interesting part is *where*. Every repair was made **at the snippet
source** and reached `canon.css` by regeneration, never by hand: `gap: 6px` → `4px` twice (the second
purely by projection), the two `--layout-bento-*` properties declared, and the `--bento-cols-now`
token fork closed. V-A then proved `canon.css` a **fixed point of its own generators** — re-ran both
and compared shas — which is the only evidence that matters for a file nobody is allowed to edit.

**Why the fork was closed the way it was, and why it is a call rather than a fix.** The obvious route
was the `--bento-columns` dial. It does not work, and the reason is a property of the gate rather
than of the CSS: the fork gate scopes by the **last `.cn-*` class**, so routing a per-instance column
count through the dial simply *moves* the fork onto `--bento-columns`. A per-instance column count is
**inexpressible** inside a `.cn-*` projection under this gate. Lane A therefore wrote
`grid-template-columns` directly on `.tpl-group-lead`, geometry unchanged at four columns, and
recorded the choice as a **Claude call under `s251-D15`** with its one call site named. ⛔ If Dave
wants the dial route, what has to change is the gate's scope key, and that is his.

## 2. The thing that made the day was a red nobody could see

Lane B's brief was small: `_validate_composition.py --selftest` had been aborting at L378, and an
aborting selftest is not a green. It had been aborting since `0979a9b` — **#249** — because a KPI
anchor drifted `data-c` 3 → 1 at #249/#251 and the selftest's fixture no longer matched.

Repaired in the `s253-D2` form (fix the **reader**, never narrow the gate), **17/17 arms ran where
zero had run**. And the run came back **RED**: the flagship bento artefact had been failing C9 —
the composition gate — for **six sessions**, with nothing anywhere in the record saying so.

★ **This is the finding, and it generalises past this gate.** An abort and a pass look identical in
a log nobody reads closely: both are "the step did not complain". A red is loud; an abort is *quiet*,
and quiet is what lets it ride. Nothing in the repo sweeps for the class — no gate asks *"which
selftests exited without running their arms?"* — and `_validate_composition.py --selftest` is
**still not a `_build_all.py` STEPS entry**, which is L5's RSQ1, open since #245. So the runner would
not have caught it either. The cheap half of the remedy is the STEPS wiring; the expensive half is
the sweep, and both are Claude's to price.

## 3. Why the contradiction went to Dave instead of being resolved by a lane

The un-aborted gate did not just say RED, it said something a lane could not act on. C9's
divisibility leg wants the tile count to divide the column count; `s248-D1`'s **4+2 wall** puts four
tiles over two, and four does not divide six. Two ruled facts, mutually unsatisfiable under the
gate's current reading — surfaced as `W-481` and put to Dave rather than reconciled.

He answered **"1"** — one character — and `s255-D1` records what option 1 was: **teach the gate the
artefact's own ruled declarations.** A literal `repeat(4, …)` on a scoped grid is legal *because
`s247-D3`/`s251-D1` declare it* (rule 10a); full-bleed `grid-column: 1 / -1` per band is legal
*because `s248-D1` declares it* (rule 6b(i)). **The wall stands. The reader was lagging the rulings,
so the reader was repaired.** The alternative — re-rule the wall to 3+3 or 6 — was put and not taken.

Two things are worth noting about how that decision was put, because #254's standing instruction was
being tested for the first time: it was **led with the recommendation**, carried **one** item of
weight, and accepted in **one word**. Dave named himself the bottleneck at #254; the shape held.

Lane C's enactment then went green on the artefact for the first time since #249 — 22 arms, 0 failed,
with the mutants `10a`-deleted, `6b(i)`-deleted and `data-c` 4→5 all going RED and **nothing exempted
by name**, which is the difference between teaching a gate and disabling it.

⚠ **What `s255-D1` did NOT settle, and it is now live:** any scoped grid can be argued into legality
by pointing at a ruling, and nothing written says which scopes may do that and which must stay inside
the band model. Lane C raised it as a ruling-shaped question. It is a definition, not a build.

## 4. Why the conductor declined the re-cut with permission in hand

`_gate_release_audit.py --pack` prints **PASS**: `Apollo-Spider-v1.0.6.zip` matches the manifest at
`f6a834064ba3`. So the carry that has said *"the v1.0.6 zip is still missing"* since **#245** — and
that was repeated on the #254 banner and in the `→ #255` carry set — is **false**, and it is retracted
in this wrap rather than dropped. ★ The zip was one command away from being probed for ten sessions.

What *is* open is the **re-cut**, and `--drift` prices it: HEAD is 30 commits past the manifest. Dave's
word at the end of the session was *"run if you have the bandwidth"* — a conditional yes. The
conductor read the condition literally, measured the bandwidth (FILL 144,466 at the brief cut, against
a 150,929 advisory with a whole wrap still to pay for), found it absent, and **declared the decision
rather than taking it**. ★ That is the right reading of a conditional permission: the condition is a
measurement, and a re-cut squeezed into the last 6,000 tokens of a window is exactly the class of act
that produces an artefact nobody can vouch for. Today is nonetheless the first day HEAD is gate-clean
for a cut, which is why it leads the `→ #256` carry set.

## 5. The correction the conductor made about itself

Mid-session the conductor said it was *"still well under the advisory"* at what was in fact ≈130,000
real — a mis-pricing of roughly 70K, caught and corrected in chat.

★ The mechanism is worth naming because it is structural, not careless. **Lane reports fill the
conductor even when the lanes are short**: every stub, path, count and verdict comes back into his
window, while the lane's own spend goes to QUOTA and never appears in his FILL. So the seat that
*feels* idle — delegating, not writing — is precisely the seat that is filling fastest, and the
intuition points the wrong way by construction. ⇒ a temperature claim is a **measurement**
(`knowledge/_checkin.py`), never a feeling. The check-in is already ruled mandatory at the opener and
at every seam; what this session adds is the reason the rule feels unnecessary right up until it is.

## 6. The sixth breach, called one session in advance and prevented by nobody

#254's stratum recorded five consecutive boot readings under the 70,000 ceiling — 69,293 · 69,321 ·
69,526 · 69,664 · 69,797 — noted that they were **monotonically rising**, and wrote that this is
*"exactly the shape that precedes a sixth breach"*. It was reported and acted on by nobody, because
nothing in the repo fails on a rising-but-under series.

#255's boot reads **70,127** — 127 over, the first over-ceiling reading since #248. The `--wrap` commit form is refused for the ninth
consecutive wrap and the ceiling literal was **not** moved. ⚠ The arm itself, quoted rather than
paraphrased, names only **#248 70,974** at the wrap seat — #247 has slid out of the band window and
70,127 does not reach `notes/_GAUGE-LOG.md` until the #256 wrap's 2f roll, so this is a breach
measured today that the gate will name tomorrow: `s240-D2`/`s241-D1` make it shrink-only, the ruled remedy is to cut
the boot, and raising it is Dave's word alone.

★ **The general form: a trend that breaches nothing breaches no gate either.** A prediction written
into a stratum is a prediction with no owner in the wave that follows it — the same defect #254's own
ruling-shaped question named about `s254-D2`'s dated `intent` collapse. What to cut, and whether to
cut, are both his.

## 7. What is resolved and what is still open

**Resolved.** The five bento reds (`202ae6f`). The aborting selftest (`4c57bdb`). C9 against the
flagship artefact (`b4adf44`, `s255-D1`). The v1.0.6-zip absence, retracted on a first-hand probe.

**Open, and Dave's.** The v1.0.6 **re-cut** at a gate-clean HEAD. The `intent` collapse (dated ≈09-19,
`s254-D2` item 4 — two homes still hold one fact on 15 metas). **R1**. Lane S's **Q2–Q6**. Which
scopes may write a literal `repeat(n)`. The **boot ceiling**, now breached. The six §14 authoring
calls and the three role extensions. `META-TAGS-CALLS-CONTEXT`, still unread and never rendered.
The three `s251-D15` calls above, each open to his veto.

**Open, and Claude's to price.** The abort-class sweep and the `--selftest` STEPS wiring.
`gen_canon_components.py`'s habit of parsing custom-property syntax out of **prose comments** and
projecting it into `canon.css` as a real declaration — caught in the diff by lane A, nothing shipped,
no gate sees it.

---

**Links.** Spine: `_LIVE-STATE.md` § ⏱ LATEST DELTA #255 · `GOOD-MORNING.md` § ★ LATEST #255 ·
`GOOD-MORNING.md` § `#### 2026-09-07 #255`. Ledger: `knowledge/_rulings.json` § `s255-D1` (entry 393).
Reports: `notes/_subreports/2026-09-07-255-BUILD-A.md` · `-BUILD-B.md` · `-BUILD-C.md` · `-V-A.md` ·
`-V-C.md` · `-wrap.md`. Carries: `_CARRIES.md` § `## residual → #256`. Commits: `202ae6f` ·
`4c57bdb` · `b4adf44`.
