# #178 — the nickname split that cleared the fork gate, and the fold that minted a new item

provenance: 178 · 2026-08-15
status: ruled — `knowledge/_rulings.json` § `s178-D1`

*Both-way links: `_LIVE-STATE.md` ⏱ LATEST DELTA #178 · `GOOD-MORNING.md` ★ LATEST #178 · `knowledge/_rulings.json` § `s178-D1`.*

---

## Why this session existed at all

#177 opened on the token-fork ledger and never touched it. Dave's word at that wrap was
*"okey lets wrap and defer to the next session"*, so the item arrived here as the **top residual,
his, and explicitly deferred** — not as a stale premise to be re-derived but as a booked decision.
The forward title said so. That is the whole reason the session could open on the decision surface
instead of on an investigation: the deferral was recorded as a deferral.

His direction at the opener was equally explicit: *"the fork ledger (yours, top item), P1's liveness
check. we can use subs liberally, keep it in this window."* Two lanes, named, with a budget posture
attached. Three Opus subs were spent under it (fork survey · liveness · build), 219,291 tokens.

## Finding 1 — the four red forks were one ruling's own split wearing one name

The fork survey did the archaeology rather than the count. The gate `_validate_token_forks.py` was
RED with **4 `--complete` forks** against a 42-fork ledger, and the naive reading is "four themes
disagree about a colour". They do not. `s175-D1` drew the line between a **continuous quantity**
(the progress bar — ink only, all four themes) and **discrete steps** (tracker/stepper — may use
colour), and `s176-D2` then gave the step components the success-roundel system. The bar and the
tracker were therefore *ruled to differ* — and were both reaching for one component-local nickname,
`--complete`. The gate matches by NAME. It was reporting the split faithfully; the split was legal.

That reframing is what made the remedy obvious and made **DECLARE the wrong answer**: a declaration
in the ledger would have blanketed the name, so every future genuine misuse of `--complete` would
also read green. Unification narrows; declaration blankets. Dave took (a) **split the nickname**.

⛔ Option C — rule the 42-name baseline itself — was put on the surface *and explicitly not ruled*.
It is booked as its own lane, his, un-started. Recording that it was offered and declined is the
point; a session later reading "the ledger was cleared" must not infer the baseline was blessed.

## Finding 2 — the rename proof that reads false

The build sub renamed the token to `--step-fill` in `Progress-tracker.reference.html` (8
occurrences) and `Stepper.reference.html` (7), then regenerated `canon.css` **through
`gen_canon_components.py` + `gen_theme_cascade.py` directly** — never `_build_all.py`, never a hand
edit to generated CSS.

⚠ **The finding is about the PROOF, not the change.** The generator emits declarations
alphabetically, so renaming `--complete` → `--step-fill` *moves the line*. A byte-`cmp` of the
before/after `canon.css` — the reflex proof for "zero colour deltas" — therefore reports a large
diff for a change that moved no value at all. The honest instrument is a comparison at the
**declaration level**: parse the declarations, key them by name, and compare the value sets modulo
the rename. That is what was run, and it is what proved zero colour deltas. The class is old and
familiar — *the measurement's subject was not what the reader assumed* — but this is a new
instance and it is cheap to be bitten by, so it is written down here rather than left as a habit.

## Finding 3 — the gate cleared by unification, and the ledger file was never touched

`_validate_token_forks.py` went **RED (4 forks) → rc=0**, verified independently by the conductor.
Counts moved FORK **42 → 41** and names **797 → 798** — one fork resolved, one new name minted,
which is exactly the arithmetic signature of a split. ⛔ `knowledge/_TOKEN-FORK-LEDGER.json` is
**UNTOUCHED**: the red cleared because the collision stopped existing, not because anything was
declared away. Two sessions from now that distinction is the difference between "we fixed it" and
"we silenced it".

Scope was declared rather than assumed. Not renamed, deliberately: the designer-skills packs (they
are RELEASES, never auto-synced), the `_fitness-test` artefact, `sutherland-fixtures.json`, and all
historical record.

## Finding 4 — the fold, and why liveness had to be checked first

`s177-D1` deferred P1 with a condition attached: fold a carried item into a *fenced* residual list
and it inherits the fence's immortality. So the fold was gated on a liveness check of all four
carried items, and the check paid for itself — it split the four two ways:

- **LIVE, folded** — the commit-gate hatch (`git log -S SESSION_ACK` finds a single commit,
  `cfca623` at #89; the `elif` in `_git_commit.sh:133–140` is unreachable while `SESSION_N` is set)
  and the archive-move body-grep gate (the runbook's prose 2c scan predates #117 and has bitten;
  `_gm_move.py` still checks no banner BODIES). Both dated **from birth (#117)**, not from today —
  a fold must not reset an age, because the age is the part a cold reader cannot reconstruct.
- **DEAD, deleted with receipts** — the attribution re-probe (discharged by the `s129-D1`/`s171-D1`
  re-bases plus the `#112-D1` recorder) and the varied tally queries (retired by the `s124-D1`
  demote).

★ And the fold **MINTED** an item rather than only subtracting: `knowledge/_surface_recorder.py` +
`_surface-samples.json` hold **ONE sample (session 113)** in ~65 sessions. An instrument with no
consumer. Deleting the re-probe without minting this would have traded a zombie for a silent loss —
the ledger of open items would have shrunk while the actual debt stayed flat.

## Finding 5 — the counter contradiction, and why nothing was re-stamped

The bare session-count ordinals in `GOOD-MORNING.md` disagreed with each other. Resolved by reading
rather than by arithmetic: **SEVENTH and TWELFTH were both frozen snapshots**; the last value that
was ever real was **THIRTEENTH at #127**, and the item left the list at #128 without being closed.
⇒ the stale ordinals were **DELETED, not re-stamped** — "stale twice ⇒ generate, never re-stamp".
Re-stamping would have produced a fourth number with the same failure mode already built in.
`_CHAIN.md` was regenerated by the conductor and the copied-header grep came back clean.

`_LIVE-STATE.md`'s BOOT-RENT line was amended **BY ADDITION** (the re-probe is discharged); the
BOOT-RENT half of it was left untouched.

## What is resolved, and what is still open

**Resolved:** the `--complete` fork red (`s178-D1`(a), gate green, generator round-trip proven at
declaration level) · the P1 fold (`s178-D1`(b), liveness-gated, two folded, two deleted, one minted).

**Open, and named on the #178 banner's residual:** ⬛ the **42-name ledger baseline review** — its
own lane, Dave's, un-started, option C explicitly not ruled · the two folded items at [61] · the
minted surface-recorder consumer gap · and the alphabetical-emission proof finding above, which is
declared and unbuilt (no instrument was minted for it, per `s172-D3`).
