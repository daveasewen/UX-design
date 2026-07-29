# Reading the usage series — and finding the job had outlived its reason

```
provenance: local_50165c15-d8e2-4038-b812-41f702fa1347 · 2026-07-29
status: observed
```

*Session #35 (Wed morning, Opus solo, Dave live). Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA
2026-07-29. Ruling ledger: `notes/_MEMENTO-DECISIONS.md` § #35. Banner: `GOOD-MORNING.md` ★ LATEST.*

---

## 1. The job, and why it was the right job for the wrong reason

#34 handed #35 one headline: **make the usage data bite.** The evidence it offered was specific —
`PRIOR` referenced-never-consumed 8/8, `C2b`/`C3`/`C4b`/`C5` unused five sessions running,
**~3,275 tape carried dead every window.**

The first thing this session did was read the record instead of the summary. Both halves of the
brief turned out to be wrong, in different ways, and the second one changed the whole shape of
the work.

**`PRIOR` was cited at #33.** Its sequence across eleven sessions of testimony is
`RRRRRRRRRCR` — nine references, one citation, one more reference. "Referenced-never-consumed
8/8" does not survive a count of the thing it describes.

**And "~3,275 tape carried dead every window" was a PRE-CUT number.** #33 had cut the read chain
to *header → ★ LATEST → the ⏱ LATEST delta*. Every section the brief named sits **outside** that
chain. Measured this session: the chain is **3,760 tape / ~5,900 bill**, and not one of those
sections is in it. The saving the job was chasing had been banked one session earlier —
**by the session that wrote the brief.**

★ **Nothing in the record was false. The number had simply stopped being about anything.** That is
a distinct failure from a wrong figure, and harder to catch: every word around it stayed true
while the quantity underneath quietly changed referent. The generalisation, written into the
GM header this wrap: **an instrument's READING ages faster than its RULE. Measure the premise,
not only the work.**

## 2. What the series actually showed

The dataset was never the problem. Eleven sessions (#23–#34, **#26 absent**) had faithfully
recorded `section-usage` testimony, one line per wrap, form-checked every time. **Nothing had
ever read them as a series.** `section_usage_probe` validates the current line and stops; the
accumulated lines sat in `notes/_GAUGE-LOG.md` being correct and unread.

ds-024's class exactly — *an instrument shipped without its reader* — and the instrument's own
docstring names the consumer it never got: *"the dataset that answers LS-trim-vs-defer"*. The
waiting had no end because no code was ever going to look.

Read as a series, it says: **twelve sections have never once been cited in eleven sessions.**
Not four. Eight of those are also unread six-or-more sessions running:

| id | sequence (oldest → newest) | unread streak |
|---|---|---|
| `GM:C3` `GM:C4b` `GM:C5` | `RRRUUUUUUUU` | 8 |
| `GM:C2b` | `RRRRUUUUUUU` | 7 |
| `LS:DEAD` `LS:LIFECYCLE` `LS:SPINOFFS` `LS:TARGETS` | `RRRURUUUUUU` | 6 |

**3,431 tape** in total — carried, rolled by the mover, walked by the gates. Not window cost.
**Record cost**, which is real and is a different currency. The two must never be quoted as
each other.

## 3. The reader, and the one guard that mattered

`_gm_usage.py` gained `usage_history` · `usage_streaks` · `deferral_candidates` ·
`history_report` · `--history`; `_capture_gate.py` gained `usage_history_probe`, **ADVISORY at
birth with its promotion trigger written into the code** — the ds-021/022/023 lesson, where three
ruled picks sat unenacted for three sessions because nothing in the codebase held them.

Design decisions worth keeping:

- **It refuses rather than skips.** A line that opens as testimony and fails to parse is a
  refusal. A reader that silently drops what it cannot understand reports a cleaner history than
  the record contains.
- **Identical duplicates collapse; disagreeing duplicates REFUSE.** A session's stratum lives in
  `GOOD-MORNING.md` until the next wrap rolls it, so the same session legitimately appears twice.
  If the two copies disagree, one is false and this reader cannot know which.
- **★ UNKNOWN stops a streak; it never extends one.** An id absent from an older line (a section
  registered later) is `?`, and `?` breaks the run. The opposite convention would let the reader
  **manufacture the evidence it is looking for** — a count is not a measurement.

Two of these were mutation-tested rather than assumed: flipping `?` to count as unread, and
accepting disagreeing duplicates, both turn the suite red.

## 4. Dave's ruling

Read back to him with the premise correction first, because his stated goal — *"getting the
front-loaded context as efficient as possible to expand the context window"* — is **not** what
this list buys. It buys record cost. He ruled anyway, on the record-cost case:

1. **OFFLOAD seven** to the archives. Verified, not assumed: a real `_memento_search.py` query
   returns archive-only content with a fetchable id, so **the archives are in the retrieval
   corpus and offload is lossless**. `GM:C2b` is ratified rulings ⇒ offload, **never** trim.
2. **`LS:LIFECYCLE` DE-MATERIALISE, not offload.** Verified: `_build_live_state.py` generates it
   between `AUTO-DECISION-LIFECYCLE` markers from `_decision-graph.json`. It is a materialised
   view of code-held truth — the one place his *"code rather than prose"* instinct applies
   literally.
3. **The DEFERRED REGISTER is the condition, not a nicety.** `C3`/`C4b`/`C5` are the *queue*.
   For a queue, *never cited* is ambiguous between **not needed** and **invisible**, and the
   reader cannot tell those apart. Offloading queue items without a register optimises the
   record by quietly discarding decided work — the failure this project exists to prevent,
   dressed as tidying.
4. **Per-subsection usage testimony DECLINED.** The door it would measure is no longer paid
   eagerly; recorded in writing so it stops resurfacing as an open question.

## 5. What went wrong, and one thing that went right by accident

Five corrections, **none found by re-reading code** — the ninth consecutive session.

- **I asserted `LS:LIFECYCLE` was generated before verifying it**, then a heading-string grep came
  back empty and I nearly reported the opposite. The claim was right and my first evidence was
  not; the defect is identical in both directions.
- **I reached for `mv` to `/tmp`** to clear a mutation-test file — cross-device, refused — when
  the repo's own `_to_delete/` convention already existed and I had not looked. *Survey before
  build*, applied to housekeeping.
- ★★ **My own new probe refused this session's banner.** It detected testimony by the substring
  `section-usage`, so a blockquoted line *mentioning* it read as a malformed record. Same class
  as #33's bite matching a phrase two messages happened to share. Fixed to match the
  `**section-usage #<N>` opening — nothing loosened, only aimed. **A defect shipped and caught
  inside a single window, by the instrument it was pointed at.**
- **`_gm_move.py`'s module docstring** claimed `roll_2f` takes *"deliberately no anchor
  argument"* for **both** destinations. The code has carried `archive_at` since #34, exactly as
  #34's banner describes. Prose staler than its own code; caught only because I read the
  implementation instead of the docstring.
- ★★ **The wrap gate's `"Last refreshed" is not today` check reads only the first 40 lines of
  `_LIVE-STATE.md` — where that line does not live.** It has been passing on **dates inside the
  LANES section**. On #34 it could not have failed even with a completely stale stamp. The line
  was moved into the zone this wrap so the check tests the thing it is named after. *A gate
  passing for a reason unrelated to its name is indistinguishable from a gate working, until
  the day the unrelated reason stops holding.*

## 6. The wrap that forced the enactment

The session priced 42% and closed at ~50% — its own stop line, `60 − the 10-point wrap` — and
**dropped the enactment at the door**, second consecutive session the ceiling has done that.

Then the wrap gate blocked on `GOOD-MORNING.md` compactable, and the block could not be met.
**Six rounds of trimming, each yielding less than the one before**, ending 54 tape short while
the handoff got progressively thinner. #34 had already declared the cap *structurally* at its
limit; #35 is the proof — **every trim came out of the current session's own record, because
that is the only prose a session is licensed to cut.**

So the four GM offloads Dave had ruled an hour earlier were enacted at the wrap: `C2b` `C3`
`C4b` `C5` moved verbatim to `_GM-ARCHIVE.md`, retired from `GM_VOCAB`, and registered in §C·4.
Compactable fell from 12,054 tape to **11,353** and the block cleared.

⚠ **The honest reading of that sequence:** the cap was not satisfied by discipline, it was
satisfied by removing content — and the only reason that was safe is that Dave had already ruled
it, the archive is retrievable, and the register records what left. **A size cap that can only be
met by the newest session cutting its own record is a cap charging the wrong party.** #36 inherits
the LS half of the ruling, which is the remaining relief.

## 7. Resolved / still open

**Resolved:** the reader exists and is wired · the candidate list is reproducible
(`_gm_usage.py --history`) · four GM sections offloaded, registered, retrievable · per-subsection
testimony declined in writing · three prose-vs-code defects fixed.

**Open, Dave's:** the LS offloads (`DEAD` `SPINOFFS` `TARGETS`) + `LS:LIFECYCLE` de-materialised,
with their register rows — **#36's first job** · ★ **the boot has never been measured by any
session in this project**: ~17 of #35's ~20-point floor is harness + memory index + system
prompt, and **every pre-flight number in this repo rests on an estimate of it** · the M10 numbers
and the disarmed 28,000 trigger, a third session untouched · the `{17}`-literal siblings, unswept.

**Links:** spine `_LIVE-STATE.md` ⏱ 2026-07-29 · ledger `notes/_MEMENTO-DECISIONS.md` § #35 ·
gauge `notes/_GAUGE-LOG.md` #35 · register `GOOD-MORNING.md` §C·4 ⬛ DEFERRED REGISTER.
