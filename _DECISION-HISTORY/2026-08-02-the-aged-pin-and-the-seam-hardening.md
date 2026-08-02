# The aged pin and the seam hardening — session #78, 2026-08-02

```
provenance: local_a32bb000-4b3f-42be-911e-1fb3046f367b · 2026-08-02
status: observed
```

*Rulings this narrative rests on: `notes/_MEMENTO-DECISIONS.md` § ★ #78 (#78-D1…D3). Spine entry:
`_LIVE-STATE.md` ⏱ LATEST DELTA #78. Commits: `c9b74f5` · `219986b` · `f73b9ec` + the wrap.*

## Finding 1 — the step-11 red was the reader working, and the diagnosis took three probes

The chain handed #78 a red declared "aged pin vs regression UNMEASURED". The arc: (1) reproduce —
`_gm_usage.py --selftest` at HEAD, exit taken off the process (the #77 confession about `$?` after a
pipe was live in memory), two arms named, a FAIL not a crash; (2) read the arms' source — both hinged
on one candidate list, so two reds collapsed into one suspected cause before any history was pulled;
(3) measure — `--history` showed a C at #74 for all three pinned sections, and `_GAUGE-LOG.md:739`
carried #74's ratified testimony verbatim. No code had regressed; a fixture had pinned a LIVE fact
("these sections have never been cited") that #74's fix-block sweep made false honestly. The code
itself documented the class one comment below — LS:LIFECYCLE was excluded from the pin for exactly
this reason — and the pin outlived its premise anyway. **The general lesson, now also in the ledger:
pin deltas, not states.** The replacement arms assert `ever_consumed` (monotonic — testimony only
accumulates) and a structural XOR; the original intents moved to a synthetic corpus where the
candidate exists by construction. Mutation evidence both ways: the fixture's in-block control flips
both greens with one citation; the delta arm goes red in a re-enacted pre-#74 world (row #74 struck).

## Finding 2 — one named misroute hid six siblings

The periphery inventory named ONE routing defect (consult-index failure reported as dark-surface).
Sub B, told to replace the mechanism rather than patch the instance, measured the whole cascade:
SEVEN misroutes, including two "(advisory)"-labelled steps that silently GATED the build because a
substring matched earlier in the cascade, and one purpose-written remedy that was dead code because
a competing substring always won. The dead-ends: none — but the near-miss worth recording is that a
one-line fix to the named instance would have left six standing and READ AS COMPLETE. The fix-the-
class instinct (Dave's standing "best practice over convenience") is what surfaced them: exact-ID
rows + a boot-time table check + loud refusal on unknown IDs makes the class unwritable, and the
selftest's mutation control (drop one route, watch the check name the victim) keeps the green
falsifiable.

## Finding 3 — T3's first mid-session firing exposed a shape its ruling never saw

#77 ruled the commit headline generated from the banner (single source, kills found-only-in-the-
commit-message). Nobody had yet committed MID-session under it. #78's P0 fix commit came out
stamped with #77's headline — truthful about the banner, false about the commit — because the
banner rolls at wrap. Two commits in `git log` now claimed to be #77's regime work; only the bodies
were honest. Ruled the same hour (#78-D3): non-wrap headlines carry `after #N`. The receipt is
self-demonstrating: the build commit that shipped the prefix wears it. The meta-lesson repeats #77's:
**the first live run of a mechanism is a probe, and the seam teaches fastest when you actually
route work through it.**

## Finding 4 — replay discipline caught two of my own instrument errors

(1) My zero-override grep matched two PROSE lines mentioning `.dv-leg` inside a comment — the same
matched-grep-is-not-a-presence class the memory carries; quoted, discharged. (2) My first render
replay silently read the light posed strip twice: the dark-pane scope selector missed and fell back
to `document`, and the identical numbers were the tell. Both were confessed in-flight and re-run
correctly (the dark pane independently verified: `--ink` → `#FFFFFF`, 6% white tint). Worth keeping:
**identical readings across supposedly different scopes are a probe defect until proven otherwise.**
Also operational: the render browser lives at `outputs/_render-env/` (headless shell + extracted
libs via `LD_LIBRARY_PATH=…/chromelibs/root/usr/lib/aarch64-linux-gnu`) — `playwright install
--with-deps` fails on sudo in this sandbox; plain reuse of the sub's env works.

## Resolved state

P0 green (60 bites) · phase-2 P1–P4 built and consumed at the commit seam · DV-D19 specimen v2 on
real canon awaiting Dave's two pins · CI's next push expected green through step 11 and delivering
the first real-build verdict on the routing table.

## Still open

P5–P7 (unruled, priced) · the specimen pins (swatch-at-rest · fade attribution) · legend headroom
(78 B group free) · DO-FIRST 16's pair (unregistered-source gate · bar-motion half) · Sub A's
msgfile blank-line fold (declared, unruled) · `_build_survey.py` docstring's stale line numbers.
