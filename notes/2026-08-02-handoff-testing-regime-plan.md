# The handoff testing regime — a plan, for ruling

provenance: local_d88890e5-8ac4-4fa4-8447-31fedf412293 · 2026-08-02
status: ruled · notes/_MEMENTO-DECISIONS.md

> **RULED #77 (Dave, explicit option-select): R1–R4 all adopted as recommended.** Ledger entry
> § ★ #77. ⚠ **R3 correction, found at ledger read-back:** the commit-vs-wrap dichotomy in this
> plan was FALSE — #74-D1 already runs `_capture_gate.py --wrap` from `_git_commit.sh` (the
> WARN/`--wrap` mode split). Enactment shape: `roll_claim_check` lives INSIDE `wrap_checks()`;
> the existing #74-D1 consumer delivers it at the commit seam. No new wiring, single home.

*Dave's ask at #76, verbatim: "can I have a rigorous testing regime planed for the whole handoff
system plan in the next session, it keep breaking." This is that plan. Nothing here is built;
every mechanism below is FLOATED and priced, and four of them need his ruling before a line of
code. Authored #77 (Fable).*

---

## The plan in one page

The handoff system has broken at least seven times in seven sessions, and every fix so far has
been a discipline rule that the next instance outlived. The pattern under all of them is the
same: **the handoff is testimony about the session, written by the session, before the session
ends** — and nothing re-reads it afterwards. A claim authored before the last state change can
be falsified by that change, and in this system the wrap gate itself is a thing that changes
state (it blocks, and the block forces rolls).

So the regime is not "more checks" scattered about. It is one principle applied at five seams:

**Generate testimony where possible; where it must be authored, re-grade it at the seam where
it becomes durable — the commit — and re-enact every historical breakage as a fixture that must
go RED.**

The five test layers, one per observed failure seam:

1. **T1 — Generate the residual.** The banner's roll-residual line stops being authored prose.
   A new `_roll_state.py` measures the actual roll state and emits the line; the banner carries
   the generated line, never a narration. Kills the forward-claim class (#73, #75, #76) at source.
2. **T2 — The roll-claim check, wired at the COMMIT seam.** `_capture_gate.py::roll_claim_check`
   compares any banner roll-claim against the T1 measurement, BLOCKING — and it runs from
   `_git_commit.sh`, beside the existing `_gen_chain.py --check`, because commit is where a false
   claim becomes durable. The wrap gate runs *before* the last state changes; the commit script
   runs after all of them.
3. **T3 — Single-source the commit message.** The headline of the commit message is GENERATED
   from the ★ LATEST banner, so a finding can no longer live only in the msgfile. Kills the
   "Dave had to ask whether it was in the handoff" class (#72, #76) by construction rather than
   by checking.
4. **T4 — The regression corpus.** Every named historical breakage becomes a selftest fixture
   that must go RED when re-enacted, with a green control beside it. Growth contract: **a future
   breakage may not be closed without its fixture landing in the same commit.**
5. **T5 — Audit the gate's own red arms.** A BLOCKING check without a mutation fixture is an
   assertion. One audit pass: list all ~12 wrap checks, confirm each selftest has a red arm,
   build the missing ones. (Count is a floor, not a measurement — the audit produces the number.)

**The acceptance criterion for the whole regime (T0):** re-enact each of the five named
breakages against the finished machinery; each must go RED, and the green control must stay
green. If any re-enactment passes, that layer is an assertion, not a test.

**Declared non-catches — what this regime will NOT do:** it cannot fire inside a session that
never runs the wrap at all (#70/#71 — the next session's title check catches it one session
late, and that stays the only net); it cannot verify the *honesty* of a fill figure, only its
form; it cannot check reasons ("budget was why") — only STATE claims become checkable; and it
does not touch the **stale-copy seam** (GM header PROSE teaching a retired unit, the #58 band
case) — that class is prose, not roll-state, and its existing remedy is the right one: checkable
claims move to `_assertions.json` where `_validate_assertions.py` re-tests them every build.
Extending that register is orthogonal maintenance, not a sixth layer.

**What I need from Dave — four rulings, then it's delegable:** R1 adopt the generated residual ·
R2 generate the commit-message headline vs merely refuse a divergent one · R3 wire the claim
check at the commit seam vs the wrap gate · R4 adopt the no-closure-without-fixture growth
contract. My recommendation on each is below, with one control each.

**Price, whole regime:** ~300–380 added lines across `_roll_state.py` (new, ~80),
`_capture_gate.py` (~120 + fixtures), `_git_commit.sh` (~40), selftest corpus (~100). Build is
delegable under RULED #57 — no ruling is produced by the build itself, and every piece is
mutation-testable. The rulings and the fixture *semantics* (what each historical state was) stay
in-window.

---

## The evidence base

<details>
<summary><strong>The failure inventory — seven instances, five seams (sources named)</strong></summary>

| # | What happened | Seam | Was it gated? |
|---|---|---|---|
| #70/#71 | Never wrapped; the chain certified the wrong session — `--check` said FRESH *and was right* | **Skipped wrap** | No. Title-vs-LATEST check (`_gen_chain.py`, #72 (f)) now catches it ONE SESSION LATE |
| #72 | Findings lived only in the commit message + stratum; Dave had to ask | **Reach-the-chain** | No — nothing reads the msgfile |
| #73 | Declared gap authored mid-wrap, drifted before close | **Forward claim** | No — "declare LAST" was a discipline rule |
| #75 | Banner said "2f NOT run" while the wrap gate had BLOCKED and forced 2f; `_GAUGE-LOG.md` carries `#### 2026-08-01 #74` | **Forward claim** | No — nothing compares banner vs artefact |
| #76 boot | Paid for #75's false residual at boot; 4th banner-before-seam instance | **Forward claim** | No |
| #76 wrap | Gate caught 4 authored-testimony errors discipline missed; findings again only in msgfile + stratum until Dave asked | **Forward claim ×3 + reach-the-chain** | Form checks caught the 3; the reach failure is ungated |
| #58 | A bare comma crashed the whole gate — traceback instead of a verdict on 39 checks | **Gate robustness** | Fixed for that parser; no systematic rule |

Sources: `handoff-testing-regime-owed-77` (memory, quoting Dave), `_CHAIN.md` #76 banner + delta,
`_RUNBOOK-capture-ritual.md` (ds-022 history), `_capture_gate.py` PREFLIGHT_FIXTURES comments
(#58/#73/#74 already pinned — the house precedent T4 extends).

</details>

<details>
<summary><strong>The premise, verified against the call graph #77 (not recalled)</strong></summary>

- **Banner-before-gate:** runbook step 2 writes the banner; `wrap_checks()` (`_capture_gate.py:2360`)
  runs at close; `gauge_log_continuity` is BLOCKING and *forces* a 2f roll when N−1's block is
  missing — i.e. the gate changes what the session did, after the banner said what it did.
- **Nothing re-reads the banner's roll-claims:** `grep -n roll_claim _capture_gate.py` → no
  matches; `ls knowledge/_roll_state.py` → "No such file or directory". The wrap checks grade the
  banner for FORM (pre-flight stamp, title cap, budgets) — never content-vs-artefact.
- **The commit message is read by nothing:** the gate's only git call is
  `git status --porcelain` (wrap_checks, ~line 2445); `_git_commit.sh:11` takes a freehand
  msgfile.
- **The commit script is the true last act:** `_git_commit.sh` already runs
  `_gen_chain.py --check` before staging and refuses on non-zero — the exact precedent T2 rides.
- **The chain carries only** GM header + ★ LATEST banner + LS ⏱ LATEST delta
  (`chain_parts`, used by both the gate and the generator — one slicer). Stratum and msgfile are
  structurally outside it, which is why "write it down" ≠ "write it where the next session reads."

</details>

---

## The five layers, in full

### T1 — Generate the residual (`_roll_state.py`, new)

**Seam it closes:** forward claims about the rolls (#73, #75, #76). **The mechanism:** a
measurer, not a narrator — per [[measuring-tool-must-not-guess]] it observes and publishes:
GM banner-block count · LS delta-block count · GM stratum-block count · newest
`notes/_GAUGE-LOG.md` session key · newest `_GM-ARCHIVE.md` / `_LIVE-STATE-ARCHIVE.md` batch
keys. Output is ONE canonical line, e.g.:

```
> **residual (GENERATED #77):** 2c OK (banners 2/2) · 2d OK (deltas 3/3) · 2f OK (strata 1, log #76) — _roll_state.py · 2026-08-02
```

The banner carries this generated line. An authored residual sentence becomes illegal in the
same motion (T2 enforces). UNKNOWN is never defaulted: if a surface can't be parsed, the tool
emits `UNPARSEABLE — <which file, which anchor>` and the wrap fails loud and named — a crash is
not a fail, and neither is a guess.

**Mutation acceptance:** run against a tree where `_GAUGE-LOG.md`'s newest key is #74 while a
hand-authored banner line claims "2f NOT run" → T2 goes RED quoting both. Green control: the
generated line against the same tree passes.

**Why generation and not a better rule:** "declare LAST" already failed — #73 proved even a
declared-last gap drifts, because the wrap gate afterwards can still change state. A generated
claim cannot lag the artefact it is generated from, provided it is generated at the seam (T2's
wiring). This is [[translate-prose-into-machinery]] applied to the record itself.

### T2 — `roll_claim_check`, BLOCKING, wired at the commit seam

**Seam it closes:** the durability seam. Any line in the ★ LATEST banner matching the residual
vocabulary (the canonical form above, plus the authored forms it retires — scoped to EXACT
quoted forms per [[gate-must-quote-what-it-forbids]]; unknown forms FAIL loud, never enumerated
into silence) is re-derived via `_roll_state.py` and compared. Contradiction = FAIL quoting both
lines.

**The wiring is the decision that matters (R3):** `_git_commit.sh` gains one call beside its
existing `_gen_chain.py --check`. Rationale: [[check-after-its-own-remedy]] — gate the seam
where the defect becomes durable. The wrap gate runs before the last state changes (it *causes*
some of them); the commit script runs after all of them, every time, and already refuses on a
red check. Post-wrap addenda (runbook 5b) re-commit, so they re-run it — the addendum path is
covered for free.

### T3 — Single-source the commit message

**Seam it closes:** reach-the-chain (#72, #76 — "are these latest observations in the hand
off?"). **The mechanism (R2, primary form):** `_git_commit.sh` generates the msgfile headline
from the ★ LATEST banner's headline line — the banner becomes the single source, and a finding
that exists only in the commit message becomes *unwritable* rather than detectable. Body may
still carry mechanics (hashes, file lists). Fallback form if Dave prefers authored messages: the
script REFUSES a msgfile whose ⚠/⛔/★★-marked lines have no counterpart in banner or delta —
weaker, because grep-matching findings across prose is the fuzzy edge where this class was born.

**Declared limit:** T3 covers the msgfile. The *stratum* half of #72's defect is already
structurally handled — strata roll to `_GAUGE-LOG.md` under 2f and the EXIT CHECK requires
lessons to reach a standing home before rolling; T4 pins that with a fixture rather than adding
a second mechanism.

### T4 — The regression corpus (`selftest_handoff_history`)

**Seam it closes:** recurrence itself. The house pattern exists — PREFLIGHT_FIXTURES already pin
#58's crash-shape, #73's legal-refusal forms, #74's retired %-stamp — but it grew ad hoc, one
bite at a time. T4 makes it systematic: one fixture per inventory row above, each documenting
(session #, the state re-enacted, expected verdict), each run as a MUTATION before being written
down, each with a green control beside it ([[attribute-the-diff]]).

**The growth contract (R4):** from ratification, a handoff breakage may not be recorded as
closed unless its re-enactment fixture lands in the same commit. This is the gate inside the
growth loop — the corpus grows exactly as fast as the failure history, no faster.

### T5 — Red-arm audit of the existing gate

**Seam it closes:** the green-that-cannot-fail. The wrap runs ~12 checks; most have selftests;
whether EVERY blocking check has a fixture that makes it go red is **UNPROVEN — a priced TODO,
~half a session, delegable**. The audit's output is a table (check · tier · red arm present
Y/N), then fixtures for the gaps. No new mechanism — this is maintenance the regime formalises,
on the [[instrument-without-a-consumer]] principle: a gate that cannot be made to fail has never
been tested, only shipped.

---

## The four rulings (R1–R4), recommendation first

**R1 — Adopt the generated residual.** *Recommend YES.* For: it is the only shape that survives
#73's lesson (even declared-last drifts); precedent is the AUTO-MARKUP generator, mutation-tested
at birth. Against: one more generator to maintain; the banner loses a place where honest prose
nuance lived ("2c skipped because X") — nuance moves to the stratum, which is its home anyway.
Control: if generation proves too rigid, T2 alone (authored line, checked at commit) is the
fallback and R1 can be reversed by deleting one file — additive, like `_gen_chain.py`.

**R2 — Commit headline GENERATED (vs refusal-only).** *Recommend GENERATED.* For: makes the
defect unwritable instead of detectable; refusal-matching across freehand prose is fuzzy and
will false-positive. Against: commit messages become less expressive at the headline. Control:
body stays freehand; one session's trial, revert = one script edit.

**R3 — Wire at the commit seam.** *Recommend YES.* For: it is provably after every state change;
the precedent (`--check`) already lives there and blocked correctly at #75. Against: a check
outside the gate splits the gate's inventory across two files. Control: the check's *body* lives
in `_capture_gate.py` (single home); `_git_commit.sh` only invokes it — same split `--check`
already uses.

**R4 — No closure without a fixture.** *Recommend YES.* For: it is the only layer that addresses
"it KEEPS breaking" rather than "it broke". Against: adds friction to every future repair.
Control: the fixture requirement is itself checkable in review (the commit either carries a
fixture or it doesn't) — no new gate needed at birth; gate it later if discipline fails, which
is the house escalation path.

---

## Sequencing and price

| Step | What | Price (est) | Who |
|---|---|---|---|
| 0 | Dave rules R1–R4 | one review | Dave |
| 1 | `_roll_state.py` + its selftest (T1) | ~80 lines | sub |
| 2 | `roll_claim_check` + commit wiring (T2, T3) | ~160 lines | sub |
| 3 | Regression corpus (T4) | ~100 lines, semantics ratified in-window | sub builds, conductor ratifies |
| 4 | Red-arm audit (T5) | ~half a session | sub |
| 5 | T0 acceptance run — all five re-enactments RED, controls green | one run | conductor, receipts to Dave |

Estimates are planning estimates, not measurements — they flip no decision; the T0 acceptance
run is the measurement that matters.

---

## Phase 2 — the periphery (Dave's #77 mid-flight ask; inventory DONE, plan owed #78)

*Dave, verbatim: "after I want to test/analyse all the peripheral mechanisms too, the graphs,
eval, hooks, the state manager, all the supporting mechanisms too, anything that touches it."
Evidence base: `notes/2026-08-02-handoff-periphery-inventory.md` (measured, 15 named probes,
blind spots declared). T0 for phase 1 PASSED before this section was written.*

Priorities, by measured exposure — for ruling at #78, not ruled:

- **P0 — LIVE RED, INHERITED, DECLARED NOT DIAGNOSED:** `_gm_usage.py --selftest` (build step 11)
  fails two REAL-REPO arms at HEAD — control-run via `git archive HEAD` into a clean tree, so
  #77's diff is attributed CLEAN. The arms pin live repo state (`{LS:DEAD, LS:SPINOFFS,
  LS:TARGETS}` ⊆ never-cited set · "The remedy is UNRULED" in the report), which a legitimate
  #76 roll could flip with no code change — premise-ages-faster-than-rule, but whether it's an
  aged pin or a tracker regression is UNMEASURED. ⚠ CI on the next push will show this red;
  it is not #77's regime. First job at #78.

- **P1 — `_git_commit.sh` gets a test harness.** No selftest, no runner, and since #74-D1 + #77
  it is the seam every other check is delivered through. Fixture-repo tests: lock dance ·
  WARN/`--wrap` split · T3 headline (both parse paths) · stale-msgfile trap · `--check` refusal.
- **P2 — the spine's ungated writer.** `_build_live_state.py` writes `_LIVE-STATE.md` in place,
  advisory, no selftest. Selftest is buildable now; whether it GATES is Dave's ruling
  (derivation governance — engine never derives-and-promotes).
- **P3 — the `_build_all.py` label misroute** (substring matching sent a consult-index failure
  to the dark-surface remedy). Exact step IDs, unknown label fails loud.
- **P4 — orphan selftests wired:** `_validate_assertions`, `_build_decision_graph`
  (+ `_roll_state`, wired at #77 already). A selftest not in STEPS is a gate that does not run.
- **P5 — `_gauge_tokens.py` selftest** pinning the ruled budget triple (160K/200K/256K) and the
  cache behaviour — the constants every wrap is graded against are currently unbitten.
- **P6 — graphs:** `_build_decision_graph` red arms; `_GRAPH-REPORT.md` has no reader — find it
  a consumer or retire it (instrument ships WITH its reader).
- **P7 — drift check or boundary declaration** for the two `memento-package/` machinery copies.
- **Declared out of scope for machinery:** prose mechanisms (runbooks, GM, `dreamer.md`) — a
  ritual step has no exit code; Desktop-side git hooks (invisible to this clone); the dead
  `outputs/_wrap60_*` one-offs (flag for `_to_delete/`).
