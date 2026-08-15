# #179 — the desk cleared, and the writer it cost

```
provenance: 179 · 2026-08-15
status: ruled — `knowledge/_rulings.json` § `s179-D1`
```

*Spine entries: `GOOD-MORNING.md` ★ LATEST #179 · `_LIVE-STATE.md` ⏱ LATEST DELTA #179.
Ledger: `knowledge/_rulings.json` § `s179-D1` (160 rulings, last entry).
Brief: `_BRIEF-borrowed-instruments-2026-08-12-v2.md` §§3b/3c/3d/5/7.*

---

## Why this session existed

`⬛ THE BORROWED-INSTRUMENTS BRIEF'S FIVE DAVE-GATES` had been on the residual since #164 —
fourteen sessions of a carry that could not move because every one of its five open questions
needed Dave and none of them had been put to him as a decision rather than as a description.
The arc of #179 is therefore not "build the gardener"; it is **how five coupled gates were made
rulable in one sitting**, and what the enactment then cost.

## Finding 1 — the gates were coupled, and that is why they were put together

Dave's direction was explicit about the risk: *"lets get as much of the desk as possible, beware of
dependancies and externalities when briefing and judging, ill go with your recommenations."* The
externality clause is the operative half. A findings cap (N) that ignores the queue cap (Q) produces
a queue that fills faster than it drains; a cadence ruled without a review surface schedules work
that then has nowhere to land. Putting them one at a time would have produced four locally sensible
answers and one incoherent system.

What made the set rulable was the readback plus a two-part `AskUserQuestion` confirm — the four
mechanical gates as one confirm, the carve-out as its own, because the carve-out is not the same
KIND of decision as a cap. He confirmed all four and granted the carve-out **as worded**.

## Finding 2 — the cadence gate was answered by a probe, not by a preference

The honest position on "how often should the dream pass run" was that nobody knew what the binding
constraint was. So it was measured: a grep of `notes/_dream/*.md` for ruling references found **zero**
in the Jul-26, Jul-26-v2, Jul-28 and Aug-02 proposal files. Promotion had been happening only via
recent batch passes; older proposals were not being *rejected*, they were not being *reached*.

⇒ **review friction is the binding constraint, not generation cadence.** That is why the ruling
schedules a weekly Monday slot and then explicitly **withholds its enactment until the controller
exists**. Scheduling more generation into a blocked review queue would have made the measured
problem worse while looking like progress.

## Finding 3 — the Tier-1 carve-out, and why "narrow" is doing real work

This is the first exception to *promotion is Dave's alone*, a rule that has held for the whole
Memento programme. It was granted only because the exception can be stated in **machine conditions**
rather than in judgment: the claim is a pointer (not a measurement, ruling, or prose) · the old
target is provably absent · the new target is provably present · **the content hash matches**, so
the thing moved rather than changed. Any failed or ambiguous condition resolves *upward*, off the
auto path. Every repair goes to a register with before/after/probe/hash, and is git-reversible.

The fourth condition is the one that makes the other three safe. Without the hash, "old gone, new
present" is a guess about identity; with it, the repair is provably a re-address of the same bytes.

## Finding 4 — three defects, all found by DRIVING, none by a selftest

Each build sub was required to mutation-prove its work with failing controls. The interesting part
is that the three real defects of the session were found by **running the thing on real inputs**,
not by the tests:

- **B2:** a definition-time `repo=REPO` default-argument binding in `_checkin.py` — the classic
  bind-at-def-time trap. It only shows when the caller's repo differs from the module default.
- **B1:** a **resolution-root** defect that produced **14 false cards** on the gardener's first real
  pass. There were two legitimate resolution roots and the code assumed one. A tempdir fixture could
  not see it because a fixture has one root by construction. Fixed, with both roots documented in
  `resolve_pointer`'s docstring.
- **The controller:** nothing, but only because it was driven through a DOM stub — the PAUSED
  mutation, the honest-empty state and the fail-loud-on-missing-queue path were all *observed*,
  not reasoned about.

★ The generalisation is one already inscribed and re-earned here: **a green test cannot see the
scope its fixture excludes.** Drive the instrument on the real corpus before believing it.

## Finding 5 — the near-miss that became a permanent writer

The conductor's first attempt to inscribe `s179-D1` went through a JSON serializer and reformatted
**613 lines** of `_rulings.json`. It was caught before commit, reverted, and redone as a textual
insertion — which is exactly the documented remedy, and exactly what happened at #176 as well.

Dave's response is the reason this session produced a fourth artefact nobody planned:
*"does this need a permanent fix? I don't like patching things"*.

⇒ `knowledge/_inscribe_ruling.py` — **the only sanctioned writer of `_rulings.json`**. It validates
schema, reconstructs textually rather than re-serialising, parses the result, refuses duplicates,
and checks evidence legality by importing `_governs`. Its selftest includes a planted "harmless
tidy" writer, which it catches. A real dry-run against the live file came back clean with the md5
unchanged.

★ **The class fix was Dave's instinct, not the agent's.** The agent had already applied the correct
manual remedy twice and would have applied it a third time; he is the one who read two occurrences
as a class. That is the recurring shape of gate-don't-patch, and it is worth recording that the
human caught it.

## Finding 6 — what was deliberately NOT done

The Tier-1 **register file was not created**, because there were zero Tier-1 findings. An empty
register would have been an artefact asserting a state that did not exist. The **refresh arm of the
gardener is a declared inert stub**, because B3 is unbuilt and §7 fences it. The **controller writes
nothing** — it compiles taps into one paste-able message for Dave and is explicitly not a fifth
register. And `s179-D1`'s own two evidence legal-form fails were fixed, taking the `s179` count to
zero, while the **11 pre-existing `s175`/`s176`/`s178` fails were left untouched as ratified record**.

## Resolved state, and what is still open

**Resolved:** all five brief gates are ruled · B2 is wired and ran green live twice · the gardener
exists and has produced a real queue of 9 findings · the controller renders them for Dave · the
rulings file has a sanctioned writer.

**Open, and every item is Dave's or waits on him:** his eye on `_GARDENER-REVIEW.html` and the
disposition of the 9 cards · the `--apply-tier1` write path is **enacted, not verified**, and the
§3-fence-1 vs lane-brief wording question is unanswered · the brief-parser gate question is queued,
not decided · **B3 is unbuilt**, and with it the standing debt to return to Dave with numbers after
one full dream-pass cycle · the weekly Monday schedule is ruled but not scheduled.

★ The honest summary of the session: **the desk was cleared of decisions and refilled with
enactments.** That is the right trade, but it is a trade, and the residual says so.
