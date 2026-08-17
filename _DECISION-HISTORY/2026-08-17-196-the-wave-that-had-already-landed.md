# #196 — the wave that had already landed, and the gate that will say so next time

provenance: 196 · 2026-08-17
status: observed

*Both-way links: spine `_LIVE-STATE.md` ⏱ LATEST DELTA #196 · handoff `GOOD-MORNING.md` ★ LATEST #196 ·
build receipt `notes/_briefs/2026-08-17-196-stale-queue-gate-brief.md` (store row `W-36`) ·
commit `e95ea60`. ⛔ **Nothing here is a ruling** — this session inscribed none.*

---

## 1. The session opened on work that did not exist

The plan at the opener was ordinary: fire the 8-chart wave named in `GOOD-MORNING.md` §C·1(a) STEP 2,
three sub lanes, conductor holding the serial set. The survey that precedes any wave went looking for
the lane inputs and found the outputs instead: **all eight charts had landed at `df44e51`, session
#95, twelve sessions earlier** — metas and reference snippets on disk, intent fields included from
`s195-D1`'s pass the session before.

The queue line had been stale the entire time. It is the **second** recurrence on that exact line;
#26 caught the first one, and the correction note #26 wrote is still sitting in the file a few words
above the claim that went stale again. That detail is the whole finding: **a correction inscribed
next to a claim does not keep the claim true.** A note is a Polaroid; nothing re-reads it.

What did NOT happen is the part worth recording. No sub was fired. The survey ran before the spend,
which is the only reason this session cost a gate instead of three lanes of duplicated work
[[feedback-survey-before-build]].

## 2. Dave asked for the class, not the patch

His words: *"we keep missing decisions already made"*, then *"I want a proper fix, thorough and
tested"*. That is a refusal of the obvious move (edit the line, close the session) in favour of the
expensive one (make the line unable to lie silently).

The shape that survived design was a **presence rule with an annotation grammar**, not a truth
oracle. A gate cannot know whether a queue item is done; it can insist that the item **says what it
claims and names something probeable**:

- `state=landed` requires a `receipt=` — a commit sha the gate can resolve.
- `state=partial` requires a `declared=` — prose stating what is done and what is not.
- `state=open` is legal on its own, but an item that names **no probeable artefact at all** must say
  so in a `declared=` clause. That is the honest-refusal legal form
  [[honest-refusal-needs-a-legal-form]]: without it, four of §C·1's strands — "wave 3 fan-out",
  "templates+shells clean-room" — would have had to lie to pass, and a gate that fails correct
  behaviour teaches sessions to fake annotations.
- **An unannotated item FAILS.** Gate the presence, not the drift [[gate-inside-the-growth-loop]].

The dead end considered and dropped: probing every item's artefact for freshness. It would have
needed a per-item semantics the queue has never had, and it would have been an instrument nothing
could drive.

## 3. What proves it, and what does not

The mutation arm is the part that makes this more than an assertion: **today's own miss was replayed
as the FAIL case** — STEP 2 restored to its pre-correction wording, the gate refusing and quoting
path and line. Then the corrected file, green. Both directions, on real data, plus 13 selftest bites
including three scope traps (annotations outside §C·1 must not be counted). The conductor re-ran the
drive and one mutation with his own eyes rather than reading the sub's receipt
[[mutation-tests-the-clause-not-the-feature]].

What is **not** proven, and is carried rather than smoothed:

- The **CI arm** is unrun. The route is green locally; the CI log is the arbiter and was never opened
  from the sandbox. One read-back of `e95ea60`'s run closes this — and it closes #195's carried
  CI-count item at the same time, because it is the same run.
- The grammar has **never met the roll machinery in anger**. It was verified that no script writes
  GM at all, so a roll cannot corrupt an annotation — but verified-by-absence is an argument, not a
  drive.
- The tier is **WARN**. A stale claim now warns at every commit and blocks nothing. The flip to
  BLOCKING is **Dave's**, explicitly deferred, and this session did not adjudicate it.
- The presence rule covers **§C·1 only**. Banners and memory hooks carry the identical class with no
  gate at all. Named, unpriced [[instrument-without-a-consumer]].

## 4. The two corrections that came out of the same class

Once the session was looking for stale claims it found two more, both cheap:

- **legend-centring was being carried as open** in a memory hook. It is closed — `#106-D1`, Option A.
  The hook was the defect, and it was corrected in-window.
- **`--pri-hover`'s remainder was mis-stated.** The real residue is the **stored colour equivalents**
  `#626262` / `#B7B7B7`, derived at the retired `0.70` rather than the live `--alpha-68`. That is a
  value question and therefore ⬛ **Dave's promotion, not a build.**

And one enactment, which is the same class read from the other end: **`ds-033`** had been sitting
STILL-UNENACTED in the 119-sweep sidecar since #187 — Dave's own `#108-D1` from long before. The
edit is one literal, `knowledge/canon/type.css:180`, dark background `#111` → `#1A1A1A`; the sweep
re-run flipped it to **LITERAL-GONE** and the unenacted column is now **0**. ⚠ Recorded because it
nearly went in wrong: the decision note called it "ink" and the ruled literal was the **background**.
The specimen title was the authority, not the note's prose.

## 5. The commit path bit twice, and neither bite was new

T3's reused-msgfile gate refused twice. Once correctly — T3 writes the session prefix back into the
msgfile, so a second `-F` on the same file is a stale read. Once because the conductor's own leading
`#196 2026-08-17 —` stamp collided with the same grammar: the runbook forbids exactly that stamp
(step 3, inscribed at #185 after a doubled subject), and the refusal was the runbook working. The
`--reconciled` explicit-paths requirement took a fourth attempt.

**Nothing was staged on any refusal**, which is the property that makes those bites cheap. The
subject-assert took its 23rd live drive at `e95ea60` and, again, did not fail.

## 6. Resolved state, and what is still open

Resolved: the queue line is correct **and** guarded; `ds-033` is enacted with a receipt; two carried
claims are corrected at their source.

Open, in Dave's seat: the **WARN → BLOCKING flip** · the `--pri-hover` stored-equivalents
re-derivation · the still-unexplained `2c2f481` push (⛔ the `e95ea60` push is **not** it — that one
is on the record as his word this session).

Open, in the conductor's: the **memory-index compaction**, still owed, unreachable from a delegated
wrap sub.

Open, unpriced: the **wider presence class** — banners and hooks. If this session's lesson is right,
that is where the next twelve-session miss is already sitting.
