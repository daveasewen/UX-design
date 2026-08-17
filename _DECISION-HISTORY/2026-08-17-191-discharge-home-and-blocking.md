# #191 — a discharge, a home rule, and a promotion to BLOCKING

provenance: 191 · 2026-08-17
status: observed

*The WHY and HOW of session #191. The WHAT lives in `GOOD-MORNING.md`'s ★ LATEST banner, the
⏱ LATEST delta of `_LIVE-STATE.md`, `knowledge/_rulings.json` (`s191-D1` · `s191-D2` · `s191-D3`)
and the four work commits `7c95f9c` · `165fe11` · `8a89b75` · `9eaed64`. Both-way link: the banner
and the delta name this file; this file names them.*

---

## 1. DV-J1 was not a build. It was a discharge.

The lane pointer said DV-J1 was NEXT. The first Opus build sub was briefed to build it and came back
with the opposite finding: the scope it named had already been closed twice — by **DV-J2 at #27** and
again by **`s182-D2`** — so building it would have been re-enacting a settled decision.

What was genuinely broken sat underneath: the **showroom was serving deleted markup, four rulings
stale**. Nothing pointed at it, because no carry existed for "the generated surface has drifted from
the rulings that govern it". `gen_showroom` regenerated five pages and the gates went green.

The interesting part is the disposal, not the fix. A row that was queued as a BUILD and turns out to
be a DISCHARGE has two halves — the scope that was already closed, and the residue that actually got
done — and closing it with one of those halves on the receipt would have made the record lie in
whichever direction the writer preferred. Dave ruled the shape himself: *"your recommendation is good:
call it landed, with a receipt naming both halves."* That sentence is the method, and it generalises:
**a discharge closes with both halves named.**

## 2. The harness had been blind for three sessions, and it looked green the whole time

While adding the four `declare_instrumentation_dirt` arms owed since #190, the sub found that
**every commit-path arm in `_test_git_commit.py` had been crashing since #188** — the doc-row gate
was wired into `_git_commit.sh` without a fixture stub, so the arms died inside the gate and the
crash was being read as a result.

This is [[a-crash-is-not-a-fail]] arriving in the one place it is most expensive: the instrument
that certifies the commit seam. Three sessions of green receipts were, in that region, assertions.
Healed, the suite runs **26 arms green**.

The remedy has a residual attached deliberately: the 14 previously-crashing arms are now
**green-by-stub** and their CONTENT has not been reviewed against today's `_git_commit.sh`. A stub
that lets an arm RUN is not a stub that makes it TEST, and saying so is cheaper than discovering it
at #195. Sub B proposed the durable form — a harness arm that greps `_git_commit.sh` for gate
invocations lacking fixture stubs — which is the blind-harness class gated rather than patched. It
is proposed, priced (~20 lines) and unbuilt.

## 3. Three rulings, and why each was a rule rather than a patch

**`s191-D1` — the showroom sync gate BLOCKS at the commit seam.** The #191 finding (stale generated
surface) had no detector. A gate placed anywhere but the commit seam would have let the stale surface
travel; placed there, it refuses. Driven both ways before it was trusted: a planted stale page was
REFUSED **with nothing staged**, which is the property that matters — a gate that refuses after
staging leaves a repair job behind.

**`s191-D2` — home-or-declare.** #189 left four `W-31` builder choices provisional, and flagged one
as needing *"a RULE, not a patch"*: three hooks name artefacts that live outside the repo and can
therefore never grade FRESH. The patch would have been an allowlist. The rule is that an artefact is
either **homed in-repo** or its **non-repo home is DECLARED and graded as such** — so `render.py` moved
to `knowledge/_render/render.py` (the runbook now copies it, never retypes it), and `_gardener.py`
learned an adjacent NON-REPO marker, mutation-armed at `g13`. The real-store refresh then flipped both
remaining STALE hooks FRESH **honestly** — store **FRESH 96 · AGING 4 · STALE 0 · UNPROVABLE 27** — which
is the test that separates a rule from a green-washing.

**`s191-D3` — the var-gate is a GATE.** #190 built the dataviz var-resolution gate and wired it
ADVISORY by a DECLARED choice, explicitly leaving severity to Dave. He gave it: *"okay these new
recommendations are good."* Promotion touched both route tables in `_build_all.py`, and the `#166`
labels moved **together** because they are join keys — the one part of that file that must never be
edited cosmetically. `check_routes` selftest green at 119.

## 4. The record clash, reconciled by annotation

`GOOD-MORNING.md` and `knowledge/_state.json` both carried *"DV-J2b FOLDED+ENACTED #67"*, an older and
different closure claim than `s182-D2`'s. #190 flagged it and refused to patch it — correctly: two
closure stories for one item is a record question. #191 resolved it the way the record's own rules
prescribe — **annotated OVERTAKEN, naming `s182-D2` as the operative closure, added and never
trimmed** [[feedback-header-wins-over-audit]]. The ratified text stays readable; the reader is told
which claim is operative. Erasing the older line would have been tidier and would have destroyed the
evidence that the project once believed something else.

## 5. What went wrong, honestly

- The lane pointer sent a build sub at a closed scope. The pointer was not verified before briefing
  [[roll-pointer-is-not-an-absence]] — the same shape as #190's stale NEXT pointer, one session later.
- One hash typo was inscribed into a ruling and had to be repaired **textually, pre-commit**. It was
  caught, declared, and did not travel; but a ruling writer that can accept an unverified sha is a
  gap nobody has priced.
- The wrap opened at FILL **167,166** — past the 150,929 advisory by 16,237. That is legal under
  `s190-D2` (the wall is 200,000) and was DECLARED rather than discovered, which is the whole point of
  the asymmetry: a declared gap passes, a silent one fails.

## 6. Resolved state, and what is still open

Resolved: DV-J1 (landed, both halves) · the two false-STALE hooks · the declare-dirt arms · the
119-sweep consumer · the DV-J2b record clash · the var-gate's severity.

Open, and on the #192 carry: the var-gate BLOCKING is unproven in a full chained build (the runner
refuses mid-range starts) · the glob width and ds-number are still PICKED [Dave's] · three `W-31`
builder choices remain [Dave's] · the sidecar schema bump for `rechecked_at_session` [Dave's] ·
`STALE_AFTER_SESSIONS = 15` [Dave's] · the 14 green-by-stub arms · the proposed blind-harness gate ·
the B3 return-with-numbers, which restarts on the new honest figures and is Dave's window to read.
