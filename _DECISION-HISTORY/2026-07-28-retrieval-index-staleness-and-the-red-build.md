# The retrieval door was quoting a superseded record — and the build had been red for two sessions

provenance: local_10b04a7a-7b78-41db-8835-fefa9e8b712e · 2026-07-28
status: observed

*Session #32 (Opus solo, Dave live). Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA 2026-07-28 #32.
Ledger: `knowledge/_DS-IMPROVEMENTS.md` ds-024. Commit `b62d4c6`.*

## Why this session existed at all

Dave opened it by refusing the question I had asked. I had priced #31's ruled enact job, found it
exceeded the ceiling that same session had ruled, and offered him four ways to resolve the
arithmetic. He answered none of them:

> *"don't worry about the panel. we need to fix this GM is too big the wrap up is to big. we tried
> using JIT and offloading it doesn't seem to be working, is teh serch working. and when was teh
> last time a flush was done?"*

That is the finding behind the finding. I had spent the opener doing careful arithmetic **inside** a
frame — how do we fit a job under a ceiling — while the frame itself was the problem. His three
questions were each answerable by measurement, and none of them had been asked for eleven sessions.

## Finding 1 — the growth contract worked, then quietly stopped working

Measured from git, thirty commits of `GOOD-MORNING.md` and `_LIVE-STATE.md` rendered through
tiktoken cl100k_base rather than estimated:

- GM peaked at **26,323 tk** on 07-27, was cut to **12,780** by the growth-contract enactment (#16),
  and had climbed back to **15,347** within twenty-four hours. **+20%, ~+150 tk per wrap.**
- LS: **16,037 → 18,579** over the same window. **+16%.**

The contract is not broken. It caps the sections that **roll** — the banner stack, the delta stack,
the strata. It says nothing about the sections that **accrete**: DO-FIRST (2,474 tk) and §C·4
(1,435 tk) are where the +150 per wrap lands, and nothing measures them against a trend.

The shape worth remembering: **a cap on the parts that roll reads like a cap on the file.** It
isn't. Every session's wrap made the next session's floor worse, and every session's gate said green.

## Finding 2 — the usage instrumentation had been right for five sessions and nothing read it

`_GAUGE-LOG.md` carries a `section-usage` line per session (U/R/C self-report) and a code-measured
`section-sizes` line. Read across the eight recorded sessions:

- `PRIOR` — **referenced, never consumed, 8 of 8.**
- `C2b` · `C3` · `C4b` · `C5` — **unused five sessions running.**
- `C2` — unused three.

That is ~3,275 tk cl100k (~5,100 charged, ~2.5 points) carried dead in every window, with the
evidence sitting in the repo the whole time. **Exactly the ds-022 shape one layer over: an
instrument that emits a number no gate consumes.** #23 built the emitter and #24 promoted its
FORM check to blocking — but the form check asks "is the line well-shaped?", never "what does the
accumulated data say?".

## Finding 3 — the read-chain contract makes JIT structurally impossible

This is the one that answers Dave's "JIT isn't working". It was built. It works. It cannot help.

`_memento_search.py` is a working two-stage retrieval door over 255 records. But GM's own read-chain
contract (GM-D7-am) mandates: §A + LATEST banner + §C + `_LIVE-STATE.md` — **~33K tokens, eagerly,
before any question is asked.** Retrieval cannot save a token that the contract has already spent.
The spine is redundant *by design*, and no amount of improving it changes that.

§A is the clearest case: 4,208 tk, static, consumed every session because the contract says so. The
standing instruction says **never drop it** — and that was read, for eleven sessions, as *always
read it*. Those are different instructions. Keeping a section in the file and loading it into every
window are separable decisions, and nobody had separated them.

## Finding 4 — the one nobody was looking for

Dave asked "is the search working?" I ran it. It returned results, formatted correctly, ids resolving,
no errors — and `--fetch gm:LATEST` returned **#29's banner** while the file carried **#31's**.

The cause chain, each link verified against the repo rather than reasoned about:

1. The index regenerates inside `_build_all.py`. The **wrap** rewrites GM/LS *after* the session's
   last build. So retrieval is structurally one session behind — by construction, not by accident.
2. It could not regenerate at all. #30's ds-022 repair wrote `#### GAPS FOUND AT #30's AUDIT` into
   `_GAUGE-LOG.md`; `_build_memento_index.py` accepts only `#### YYYY-MM-DD #N` and refuses
   everything else by design (the ds-016 fail-loud contract). The step exited 1.
3. Therefore **`_build_all.py` had been RED at step 65/72 since `f2c083a`**, and **#30 and #31 both
   completed their wraps and committed over it** — because the wrap gate does not run the build.

The session that repaired one silent-record failure created another one layer down, and the layer
below it was unwatched. Three sessions of work — including the throttle rulings — were committed on
top of a red build by agents who each believed they had verified their state.

**And RETRIEVAL-FIRST is standing canon.** "Quote the record, never reconstruct" was pointing every
session at a door that returned a superseded record with full confidence. This is the
confident-false-inscription failure the whole Memento architecture exists to prevent, living inside
the mechanism built to prevent it.

## The fix, and why it is shaped this way

**The META form, not an exemption.** #30's block is a legitimate record — a finding *about* the file
rather than a session *in* it. The lazy fix is a special case for that heading. The fix taken
declares a second form (`#### META — <title>`) and leaves every other `####` refusing loud: the
dv-004 scope-blindness shape, normalise once and fail loud on unknown, never grow a list. META blocks
index under `gauge:meta:*` and terminate the session body above them; META-only files still refuse,
because a gauge log with findings and no sessions is broken rather than quiet.

**A content comparison, never mtime.** `index_freshness_check` rebuilds the records in-process and
byte-compares against disk. An mtime check was the obvious implementation and is wrong: mtimes reset
on any checkout, so it would read green on a reverted file — the DV-D17 shape, where a test that can
only see absence passes a full revert.

**Step 2g, ordered last.** The gate is what stops the rot, but the *ordering* is the actual fix:
rebuild the index after every GM/LS edit is final. This is the first ritual step that must run after
the banner is written, which is a genuinely new shape for the ritual.

## What the tests caught that I did not

Two of nine new bites failed on first run, and both were my errors, not the code's:

- **The near-miss bite.** I wrote `#### META-ish heading` as a fixture that *should* refuse. It
  didn't — my separator pattern was `[—–-]` with optional whitespace, so `META` + `-` + `ish heading`
  matched and was silently accepted as a meta block. I had read that regex twice and seen nothing.
  The fix requires whitespace around the separator. **Caught by a test disagreeing with me, not by
  reasoning about the pattern** — the fifth consecutive session where that sentence is the lesson.
- **The id bite.** I asserted the slug would be `gaps-found-at-30s-audit`; it is
  `gaps-found-at-30-s-audit` (the apostrophe separates). My expectation was wrong, the code was
  right, and the bite is now pinned to the measured value.

The freshness selftest's **first** bite is deliberately the positive one — a fresh index passes AND
reports FRESH. A failure-only suite survives a revert that deletes the whole comparison. The green
path is the load-bearing half of the pair, and that is the ds-019 lesson stated as construction
rather than as regret.

Then proven end-to-end on the live repo rather than on fixtures: edited a runbook the index covers →
gate went red with the correct message → ran 2g → gate went green.

## What I got wrong, and what stayed unfinished

- **I diagnosed one layer and reported it as the answer.** My opener told Dave the index was stale
  because the wrap rewrites files after the build. That was true and incomplete; the index also could
  not build, and the build was red. I found layers 2 and 3 only because I tried to *run* the fix
  rather than reason about it. A diagnosis that has not been executed is a hypothesis.
- **I priced the session against a ceiling and then exceeded it anyway.** Declared as a RESERVE SPEND
  on Dave's word rather than silently, but the honest reading is that #32 is the third consecutive
  session to blow its own projection — which is now three points in ds-023(c)'s overrun dataset.
- **Tasks 2 and 3 are not done.** Making the usage data bite, and cutting the eager read chain. Both
  are new build artefacts and both were refused at Amber by the rule against starting one there. The
  eager-read cut is the change that actually answers Dave's opening sentence, and it is still owed.

## The shape to carry forward

**A gate that does not run cannot fail, and a build that is never run at wrap is not enforcement.**
The programme's whole thesis is *verification = enforcement* — and its central verification step was
absent from the ritual that closes every session. Three sessions passed every check they ran while
the check that mattered was not among them.

The generalised form, and it is not about this bug: **each of these findings is an instrument whose
output nothing consumes.** ds-022 was the gauge log with no gate. Finding 2 is the usage line with no
gate. Finding 4 is the build with no wrap-time run. Building the instrument feels like closing the
gap, and it is only ever half.
