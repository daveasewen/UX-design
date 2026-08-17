# #192 — write-once became foundational, and the harness went blind a second time

provenance: 192 · 2026-08-17
status: observed

*The WHY and HOW of session #192. The WHAT lives in `GOOD-MORNING.md`'s ★ LATEST banner, the
⏱ LATEST delta of `_LIVE-STATE.md`, `knowledge/_rulings.json` (`s192-D1`),
`docs/decisions/ADR-0017-write-once-live-facts.md`, and the five work commits
`b9c72c6` · `4d517cf` · `c1991e5` · `a171e3c` · `adcc364` — all pushed, remote verified at
`adcc364`. Both-way link: the banner and the delta name this file; this file names them.*

---

## 1. WRITE-ONCE went from a floated candidate to an ADR inside one session

The principle had been floating for a while: **live facts get ONE home plus addresses to it;
history is frozen where it happened.** It arrived this session as one of the reconnaissance
lane's parked candidates and was committed as a receipt at `b9c72c6` — deliberately *as-is*,
with nothing ruled by the commit, because a receipt that quietly decides something is the
laundering failure the record already knows about.

Dave then ruled it, in his own words: *"promote WRITE-ONCE to an ADR, but lets get this fixed
very soon, it's foundational"*. That sentence is the whole arc — the promotion **and** the
urgency, and the second half is the part a bare ledger line cannot carry. It is inscribed as
`s192-D1` (conductor's inscription via `knowledge/_inscribe_ruling.py`, rulings 178→179) and
homed at `docs/decisions/ADR-0017-write-once-live-facts.md`, commit `a171e3c`.

**Why an ADR and not a runbook clause.** The rule governs *where facts live*, which is a
property of the whole record, not of any one ritual. A runbook clause would have made it a wrap
habit; an ADR makes it a constraint that new work is held to immediately, which is what
"accrete-from-duplication" means in practice.

**The trap inside it, stated so it is not discovered later.** Rule 2 cuts both ways: an address
without a resolver is *worse* than a copy. A split that leaves a pointer nobody can follow has
not reduced duplication, it has converted a redundant fact into an unreachable one. That is
carried on the banner as a pitfall, not buried here.

## 2. The finding: the commit harness went blind a second time, one session after it was healed

At #191 the finding was that the commit harness had been blind since #188 — the doc-row gate
went into `_git_commit.sh` without a fixture stub, so every commit-path arm of
`_test_git_commit.py` was *crashing*, and the crash was being read as a result. #191 healed it:
26 arms green.

**And then #191's own ruling recreated it.** The `s191-D1` showroom sync gate was wired into the
same commit path, unstubbed, in the very session that fixed the class. At #192's open, all
**14** commit-path arms were crashing again.

★ The lesson is not "someone forgot a stub". It is that **healing an instance does nothing to the
class** — [[a-crash-is-not-a-fail]] names the failure mode, but nothing was *checking* for it, so
the next gate through the same seam reproduced it at the first opportunity. A green that comes
from a crash is indistinguishable, at the harness's own exit code, from a green that comes from
a test.

**So the fix was a gate, not a repair** (`c1991e5`): `knowledge/_gate_harness_stubs.py` detects
gate invocations in `_git_commit.sh` that the harness fixture never stubs. Three things about
how it was built are worth keeping:

- **Consumer-first.** The detector was written against the real, currently-broken tree, so its
  first run had something true to say. A detector built after the repair would have had no
  observed failure to bite on.
- **A store row at creation.** `W-33` was added through `_state.add()` in the same pass — the
  forgotten-document class ([[forgotten-document-class]]) says a document with no row is invisible
  to every carry, and a new gate is exactly the kind of thing that goes quiet.
- **Mutation-proven both directions.** Planting an unstubbed gate makes it refuse; removing the
  plant makes it pass. Harness went 26 → 30 arms, all green.

**What it does NOT yet prove, declared in the commit and carried forward:** the SUBJECT-MISMATCH
absence is not mutation-proven; the detector recognises the *literal* stub-writing form, so a
refactor of the fixture builder turns it false-RED; and a **stub-adequacy** rung — a stub that
nothing actually drives still passes — is proposed and unbuilt.

★ And the honest residual on top of all that: **the gate has never refused a real commit.** The
class has now recurred twice (doc-row #188, showroom #191). The gate is the right shape of fix,
and it is still an assertion until it bites live [[instrument-without-a-consumer]].

## 3. The titled item landed and moved nothing, and that is the report

The session opened on the sidecar schema bump for `rechecked_at_session` — v1 → v2, `4d517cf`.
Selftest green. **Verdicts unchanged: STILL-UNENACTED 1 · UNPROBEABLE 19 · WEAK-MATCH 1.**

There is a standing temptation to dress a no-op as a finding ("confirmed stable"). It is
recorded as what it is: a schema bump that moved no verdict. The value is that the field now
exists for the next recheck to write into; the value is *not* that anything was learned about
the twenty-one records.

## 4. The push, and the debt it created

Dave gave the word — *"psh"* — and the push ran through the ruled call form,
`bash knowledge/_git_commit.sh --push` (`s133-D2`: the only push path). Remote verified equal to
`adcc364`.

★ **The push is what turns one carry from hypothetical into live.** `s191-D3` made the dataviz
var-gate BLOCKING, and the first single-process chained build with it blocking runs *in CI, on
this push*. Until that run is read back, the full-chained-build proof does not exist — the gate
is proven standalone and in the route selftest, which is a measurement of the route, not of a
real chained pass. That read-back is priced at ~2K and is residual ① into #193.

## 5. How the session was staffed, and why the wrap is delegated

FABLE conductor + one Opus build sub (86,140 tokens, n=1, measured) + this delegated Opus wrap
sub. Boot 56,750 real, in band.

The wrap was delegated for **two independent reasons**, and they are worth separating because
past sessions have conflated them:

1. **FILL bound.** At the wrap-open decision the conductor relayed ~26,000 room to the 150,929
   advisory line — under the 42–49K wrap band, so the wrap could not be run in-window
   [[delegation-cost-inversion-110]].
2. **Fable was also the hot quota** — All 30% · Fable 38%, resetting Thursday 10:59PM, relayed
   by Dave. ⛔ The crank decision itself was **not** taken; the panel is a relay, not a ruling.

⚠ One measurement honesty note, because it will be read later as a number: **the FILL figure for
#192 is DERIVED.** What was relayed was ROOM (~26,000); ~125,000 is its arithmetic complement
against the advisory. A delegated wrap sub cannot measure the conductor's window, so the figure
is written as derived everywhere it appears — the banner, the stratum, the gauge log — rather
than being allowed to pass as an independent reading [[feedback-measuring-tool-must-not-guess]].

## 6. What this wrap deliberately did not touch

The ruling was Dave's and was inscribed by the conductor; `knowledge/_rulings.json` was not
opened by this wrap. Memory step 3 ran at the conductor's seat (the write-once hook flipped
floated→canon, plus its `MEMORY.md` index line) — a wrap sub cannot reach the store. Everything
marked DAVE'S, FLOATED or PARKED was left exactly as found: the ds-0NN chart-intent candidate's
scope and first consumer, the `_GRADE-DECISIONS.jsonl` exclude/commit/relocate policy, the
var-gate's glob width and ds-number, the three remaining `W-31` builder choices,
`STALE_AFTER_SESSIONS`, `BASELINE_DATE`, `CARRY_GATE_BLOCKING`, the trend card, the `#174`
adjudication, every colour value, and all `G`-items.

---

**Resolved state:** ADR-0017 exists and governs; the blind-harness class has a detector wired
consumer-first with a store row; the sidecar carries `rechecked_at_session`; everything is
pushed.

**Still open:** the CI read-back of the first blocking-var-gate chained build · the detector's
unproven trio (subject-mismatch absence, coupling fragility, stub adequacy) · the ds-0NN
candidate's reconciliation on its own terms, now governed by ADR-0017 · the
`_GRADE-DECISIONS.jsonl` policy, which is Dave's.
