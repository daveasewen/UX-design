# `#241`-`E` — the ritual diet, APPLIED: seven items built, and one of them was already done

session: `#241` · 2026-09-02
window: lane E (delegated build lane under the #241 conductor)
sub index: `E`
brief: chat brief from the #241 conductor — "apply the RECOMMENDED DEFAULT PACKAGE of
`notes/_subreports/2026-09-02-241-lane-D-ritual-diet.md` § PART 4" (D1 + D2 + D3 + D4 + S1 + S5 +
S7). No `notes/_briefs/` file was minted for this lane — DECLARED GAP, not an omission I can
repair from here.
tokens: `UNMEASURED — no message.usage at a sub's own seat; UNOBSERVABLE and DECLARED, never
estimated`

## VERDICT

**All seven items are applied and none is blocked.** Six behave exactly as the package described.
**The seventh, D1, was already done** — and that matters more than the code I wrote for it. Lane D
priced D1 at "**≥22,400 tk/session**, the single most expensive thing the process layer does", on
a measurement of `cg.run(mode="wrap")` (its own probe, its line 102). The check-in does not call
that. It calls `_cg.run(rehearse=True)`, whose print has been terse since before HEAD: **3 lines,
171 tape, MEASURED here on the captured stdout.** The 7,534-tape figure is real, but it belongs to
`--wrap`, which is **S7's** subject — so the package's headline saving was **counted once and
attributed twice**. The honest total for the package as built is **≈4,100 tape per session at the
conservative floor**, not ~27,300. What D1 was genuinely missing — warn NAMES when the warn set
moves — did not exist and now does.

The saving is real but it sits elsewhere than advertised: **D2 (2,289 tape off every cold session's
first read, permanently) and S7 (1,413 tape off every wrap-gate run, of which 59 were logged on
2026-09-02 alone)** carry it between them. S1 and S5 buy no tokens today: S1 is a **cap on the next
banner** (it warns, correctly, against the #240 one and would FAIL a #241 one — both arms driven)
and S5 is a **correctness gate** that costs 135 tape a wrap to hold the boot band honest.

⚠ And the wrap gate's real elephant is now **none of the above**: its stdout is 15,955 tape, of
which the **trigger-index NOTE block is 10,294 — 65%**. Finding 7.

COUNTS: items applied `7` of 7 · files touched `5` · tests run `9` · measured savings total
`4,129 tape/session (floor)` · UNPROVEN `4`

COUNTS: findings `7` · ruling-shaped `3` · UNPROVEN `4`

## What was done

Region by region, in the brief's order. Every figure below is **tiktoken `cl100k_base` over the
exact captured stdout or the exact file**, taken with the repo's own encoder, and labelled where
it is anything else. `python3 knowledge/_gauge_tokens.py` was NOT used for the stdout figures:
its `count()` reaches a token-counting API for a REAL tier, and these are file/stdout objects
already denominated in cl100k by the gate itself — measuring them twice in two units would be the
conversion this project bans [[measure-dont-convert-units]]. The unit is stated on every number.

**Baselines were captured BEFORE any edit** (`/tmp` scratch, quoted inline here because scratch
does not survive the window):

    python3 knowledge/_checkin.py            → 58 lines · 1,579 tape
    python3 knowledge/_capture_gate.py --wrap → 268 lines · 16,222 tape

### D1 — the rehearsal prints its record, not the gate · `knowledge/_checkin.py` unchanged;
`knowledge/_capture_gate.py` ~5,530

**APPLIED, and its premise CORRECTED in the file.** The brief pointed at `_checkin.py:1174-1181`.
That call site already reads:

    if not args.no_rehearse:
        print("  REHEARSAL   wrap gate, early (same checks as --wrap; #92):")
        import _capture_gate as _cg
        _cg.run(rehearse=True)

and `run(rehearse=True)` has printed terse since before HEAD — structural fails in full, heals
truncated, then one summary line, under a comment that already says `TERSE BY DESIGN`. Probe:
`git show HEAD:knowledge/_capture_gate.py | grep -n "TERSE BY DESIGN"` → line 5284. **Measured on
the baseline stdout: 3 lines, 171 tape.** There was no 130-line dump to remove.

What was missing is the second half of D1's own clause — *"plus fail NAMES when fails > 0 or when
the warn count changes"*. Fail names already print (structural in full, heals at 100 chars). Warn
names did not: a warn could appear, change wording or vanish between two rehearsals and the only
trace was a count. Built:

- `_warn_sig(w)` — `(key8, full8)`. The KEY normalises digit-runs to `#` over the first 80 chars,
  so `git: 10 uncommitted path(s)` and `git: 4 uncommitted path(s)` are **one warn that changed**,
  not two warns. The second digest is over the full text, which is what makes CHANGED separable
  from UNCHANGED. Keying on the raw string would have marked every warn CHANGED every run and the
  delta would have saved nothing while claiming to.
- `_previous_rehearsal_record(repo)` — the last `notes/_REHEARSAL-LOG.jsonl` line carrying
  `warn_sigs`. **Returns None, never `{}`,** on any failure: an unreadable log must fall back to
  FULL output, never to a confident empty delta that hides every warn at once.
- `_warn_delta_lines(warns, prev)` — `(full, one-liner)`.
- the log record gains `warn_sigs` (~16 bytes per warn; the bodies are **not** logged — it is an
  index, not a copy) and `prev_rec` is read **before** the append, or the delta would compare a
  run against itself.

Live after-state, from `python3 knowledge/_checkin.py`:

    ⚠️  2 warn(s) NEW or CHANGED since the wrap-open record of 2026-09-02 — named here
        because a moved warn that prints only as a count is invisible:
        · NEW SINCE 2026-09-02 — LATEST BANNER CAP (`s241-D2`: 10 lines / 1,200 tape …
        · CHANGED SINCE 2026-09-02 — git: 14 uncommitted path(s) — commit before close
    rehearsal [wrap-gate, early]: 1 STRUCTURAL fail(s) … · 17 warn(s) (was 17 at the last
    logged run) (run --wrap for bodies) · logged → notes/_REHEARSAL-LOG.jsonl

**Measured saving: 0.** Measured COST: ~10 tape in steady state (the `(was N …)` clause), ~170
tape on a run where warns actually moved — buying visibility that did not exist at any price
before.

### D2 — the 461 bare ids leave the chain · `knowledge/_gen_chain.py:479-484` → one counted line

**APPLIED.** The two `out.append(... ids(...) ...)` calls are replaced by a single line that keeps
**every generated count** (461 · 376 live · 199 Dave's · 177 mine · 447 conditioned · 14
unconditioned), keeps the store-gate line, and keeps the `python3 knowledge/_state.py` pointer.
The now-callerless nested `ids()` helper went with them.

    BEFORE  _CHAIN.md  11,319 tape · 100 lines
    AFTER   _CHAIN.md   9,030 tape ·  98 lines      SAVED 2,289 tape, every cold session

Regenerated with the generator, not by hand (`python3 knowledge/_gen_chain.py`), and the footer's
self-referential size sentence **re-fixed-pointed**: it now reads *"9,030 tape (cl100k ESTIMATE) —
the unit is THE WHOLE FILE"*, converged **in 2 passes**, and the generator reports
`FILE 9,030 = slice 8,181 + wrapper 849`. `python3 knowledge/_gen_chain.py --check` →
**`✅ _CHAIN.md is FRESH — byte-matches the live chain`**. The pointer to the bodies is stated on
the line the ids left, not only in the footer — lane D's Consequence (d) says a reader who reaches
for `_state.json` whole pays ~147,000 tape against the 2,615 the dump cost.

### D3 — the 119-sweep expiry nag leaves the check-in · `knowledge/_checkin.py` ~1,342

**APPLIED, and scoped exactly as briefed.** `_recheck_119_sweep.py` is untouched,
`knowledge/_119-sweep-recheck.json` is untouched, and the consumer still **runs** on every
check-in. What no longer prints is the nag:

    119-SWEEP   ⛔ EXPIRED — 15 sessions old (limit 15); verdicts below are STALE — re-run;
                UNPROBEABLE 20 · WEAK-MATCH 1 (rechecked_at 2026-08-30T10:01:23+00:00)
      ⇒ re-run `python3 knowledge/_recheck_119_sweep.py` — an expired verdict is a
        CONCLUSION PAST ITS DATE (s129-D5), not a green.

**2 lines, 107 tape, on every check-in.** The block now prints **only** when the sidecar holds an
ACTIONABLE verdict — anything that is not `UNPROBEABLE` or `WEAK-MATCH` — or when its own probe
breaks (that arm is untouched and still loud). Today's sidecar is 20 UNPROBEABLE + 1 WEAK-MATCH, so
it is silent. Retiring the sweep itself is **Dave's** and was not taken.

### D4 — `knowledge/_measure_tokenizer.py` retired · file `git rm`'d, gate entry removed

**APPLIED. Importer probe first, as instructed:** `grep -rn "_measure_tokenizer" .` → **zero import
sites**. The surviving hits are prose (`_governs.py` ×3 quote it as the cautionary tale, four
`notes/` files record it) plus its name inside a ruling's file list in `knowledge/_rulings.json`.
None of those executes it. The file was 106 lines / 1,351 tape on disk.

The pin and the file had to move together: leave the pin and `unit_vocabulary_audit`'s second loop
FAILS the wrap (*"it no longer exists"*); leave the file and the gate WARNS about a zombie forever.
Both are done — the `MEASURERS["_measure_tokenizer.py"]` entry is replaced by the record of why it
went. **Measured: the `ds-021 (C) CALIBRATION` warn was 106 tape on every gate run** and is gone
from the after-state (17 warns before, 17 after: −1 calibration, +1 new banner cap).

⛔ `git rm` first failed with `Operation not permitted` (the mount's unlink wart). Cleared via
`mcp__cowork__allow_cowork_file_delete` per `_RUNBOOK-git-commit.md` step 4b, with the lock moved
aside — never deleted — per `[[git-lock-mv-not-rm]]`. **The deletion is STAGED, not committed** (`D`
in `git status`); nothing was committed or pushed by this lane.

### S1 — the ★ LATEST banner cap · `knowledge/_capture_gate.py` ~972 (constants) and ~2,340 (check)

**APPLIED as a NEW check, because the constants the brief pointed at do not bound this object.**
`check_budgets`'s M8 budget measures `file top → DO-FIRST` — header **+** ★ LATEST **+** ★ PRIOR
together — and its cap is DERIVED from `_GM-ARCHIVE.md` (median / p75, n=211), which is why
`BANNER_BUDGET_FALLBACK_TK = (6400, 7800)` is a fallback that is currently unreachable. **No
constant in it can bound one banner**: two lean banners and one obese one measure the same. That
pair is left untouched (its pin selftest still passes). Added instead:

    BANNER_LATEST_CAP_LINES = 10          # `s241-D2`
    BANNER_LATEST_CAP_TK = 1200           # `s241-D2`
    BANNER_LATEST_CAP_FROM_SESSION = 241  # `s241-D2` — effective-from, not retroactive

The check measures the ★ LATEST block alone (heading → next ★ PRIOR, bounded by DO-FIRST so it can
never run to EOF) and **quotes the cap in both messages**, as briefed. The effective-from key is
the same shape and the same reason as lane B's `BOOT_CEILING_FROM_SESSION`: banners are ratified
record, and #49 / #51 / #153 each shaved inscribed record to quiet a budget. **GOOD-MORNING.md was
not touched.** Live:

    WARN  LATEST BANNER CAP (`s241-D2`: 10 lines / 1,200 tape, and the ⏱ LATEST DELTA is the
    sole home for gauge / declared-skip / not-done detail): GOOD-MORNING.md's ★ LATEST banner
    is over by 13 substantive lines against a cap of 10 and 3,353 tape against a cap of 1,200.
    PRE-CAP RECORD (banner #240 < #241) — NOT a fail and NOT to be rewritten. …

**3,353 tape is lane D's own figure for the same region, reproduced independently here.** Both arms
were driven as mutations, not asserted (see Evidence): relabel that same banner `#241` and it
**FAILS**; shorten it and the check goes **silent**.

### S5 — one stratum, one first-turn figure · `knowledge/_capture_gate.py` ~4,020

**APPLIED as a class fix at the source.** Lane B's dedupe lives in `derived_boot_band()` — first
reading per ordinal wins. That is a **shield, not a repair**: the log still says two things about
one boot, and the next consumer to walk it without the dedupe inherits the whole defect. Built:

- `_parse_boot_rows(text)` — the same walk as `_parse_boot_samples`, with the provenance kept
  (`session · tk · stratum · lineno · line`). `_parse_boot_samples` now delegates to it, so there
  is **one implementation and two views**; a second walk would have been a second answer to the
  same question. Control: **105 readings parsed before the refactor and 105 after, 0 refused.**
- `boot_stratum_double_count_check(repo)`, wired **blocking** beside `boot_constant_drift_check`
  in `run()`. A session ordinal carrying more than one reading FAILS **by session number, with
  both lines and their line numbers quoted**.
- `BOOT_DOUBLE_COUNT_FROM_SESSION = 241`, and this one is not caution — it is measured. **18
  ordinals in the live log already carry more than one reading** (110, 113, 118, 127, 169, 173,
  174, 216–223, 225, 226, 239). A retroactive fail could never pass in this repo, and a gate that
  cannot pass is a gate that gets routed around [[gate-cannot-pass-in-one-environment]]. History
  prints as one NOTE with its count; the rule binds strata from #241 on.

Three arms driven: a #241 stratum stating it **once** → silent; the same stratum stating it
**twice** → FAILS naming `#241` and both lines; a **pre-rule** stratum stating it twice → does not
fail. Cost: **135 tape per wrap** (the pre-rule note). Saving: none — this one buys correctness.

### S7 — the wrap gate's warns print as a delta · `knowledge/_capture_gate.py` ~5,560

**APPLIED.** NEW or CHANGED warns print in full, prefixed `NEW SINCE <date>` / `CHANGED SINCE
<date>`; unchanged warns collapse to one line that **names every one of them** and says which
record it compared against. `--warns-full` restores the old print in one flag and is registered in
the argv contract (`CG_MODIFIERS`, `CG_USAGE`), so it cannot be silently absorbed.

    BEFORE  WARN block  17 items · 1,793 tape
    AFTER   WARN block   1 item  ·   380 tape       SAVED 1,413 tape per gate run

**59 `wrap-open` runs were logged on 2026-09-02** (lane D's count, from the same log).

⚠ **The whole-stdout figures do not show that saving cleanly, and the reason is named rather than
smoothed:** 16,222 → 15,955 tape, a net 267. The gap is arithmetic, not error — the trigger-index
NOTE grew 9,282 → 10,294 tape **because this lane's own working-tree diff is larger** (it surfaces
one ruling per touched file), and S5 added a 135-tape note. `16,222 − 1,413 + 1,012 + 135 = 15,956`
against a measured 15,955. **The attributable saving is the WARN block: 1,413 tape.**

## Findings

1. **D1's headline saving does not exist, and the figure behind it was counted twice.** Lane D's
   own probe (its line 102) is `cg.run(mode="wrap", report=None)` → 130 lines / 7,534 tape. The
   check-in calls `run(rehearse=True)`, a different print. Measured here on the captured baseline:
   the check-in's whole REHEARSAL block is **3 lines / 171 tape**. The 7,534 figure is `--wrap`'s
   and is already priced as **S7**. The package's ~27,300 floor should read **≈4,100**.
2. **The wrap gate is bigger than lane D measured, not smaller — 16,222 tape, not 7,534.** Probe:
   `python3 knowledge/_capture_gate.py --wrap` captured to a file, tiktoken cl100k. Lane D's own
   closing ⚠ predicted this: it measured before lane B's boot-band build landed in the same tree.
3. **`_CHAIN.md` was 11,319 tape and is 9,030** — lane D's 11,319 reproduced exactly, then cut by
   2,289. The four counts and the store pointer survive; `--check` says the file byte-matches.
4. **The ★ LATEST banner is 3,353 tape over 13 substantive lines** — lane D's figure, reproduced
   independently by `_latest_banner_region()` + `measure_tokens()`. The cap it now carries is
   **2.8× smaller than the object it governs**, which is the point and also the risk (Q1 below).
5. **18 session ordinals in `notes/_GAUGE-LOG.md` already double-count their boot.** Probe:
   `Counter(s for s, _ in _parse_boot_samples(log)[0])`. #240 declared ONE of them (#239). The
   other seventeen were never named anywhere. They are held harmless only by lane B's reader-side
   dedupe.
6. **`_capture_gate.py --selftest` has ONE failure and it is INHERITED, not caused here.**
   `M10: a 24-fat-line banner did not warn the chain`. Attributed by driving the arm against three
   modules in one process — HEAD's committed gate, the post-lane-B pre-lane-E gate, and the current
   one: **all three return `chain warn? False`.** It is the fixture-hardcoding class the M8 comment
   describes at :6942, biting the arm M8's own s212-D11 fix did not reach: `CHAIN_BUDGET_TK` was
   restamped to (7700, 10000) while this fixture stayed at 24 lines. Everything else passes.
7. **The wrap gate's real cost centre is now the NOTE block, and it is not in this package.**
   Of 15,955 tape of `--wrap` stdout, **NOTES are 15,469 (97%) and the trigger index alone is
   10,294 (65%)**. WARNs — the thing S7 was aimed at — were 1,793. The next cut is `_governs`'s
   render, not the warns.

## RULING-SHAPED QUESTIONS

1. **The cap number, now that it is enforced.** `s241-D2` as built is **10 lines / 1,200 tape**,
   which is lane D's option (a) and the conductor's brief. The #240 banner is 3,353 over 13 lines —
   so the first bound banner must lose **64% of its tokens**. Option (a) keep 10/1,200 and let the
   #241 wrap discover the fit; (b) 12 lines / 1,800 tape for one session, then ratchet;
   (c) advisory (WARN) for #241, blocking from #242. **Recommend (a)** — it is what you said apply
   to, and the effective-from key means nothing already written is at risk. But the number is
   yours, and the wrap that first meets it is the one that pays.
2. **Whether the cap should be able to see a DECLARED gap at all.** It cannot. A banner cut to 10
   lines by dropping its `NOT DONE` / `DECLARED` clauses passes this gate exactly as well as one
   cut by writing tighter, and no mechanical check can tell them apart (lane D, Consequence (c)).
   Option (a) leave it to the wrap author, with the warning text as the only guard — as built;
   (b) add a `DECLARED:`-shaped required field to the banner and fail its absence, which is lane
   D's S2 in miniature. **Recommend (a) now, (b) with S2** — bolting a field on alone would make
   the banner longer, not shorter.
3. **The 119 sweep itself.** D3 removed the nag, as briefed, and deliberately did NOT retire the
   sweep — that is lane D's Q3 and still open in your name. Option (a) retire it; (b) re-run once
   then retire; (c) leave it silent, as it now is. **No recommendation from this lane beyond lane
   D's own (a):** with the nag gone, (c) is now a stable state and the decision has stopped costing
   you anything per session.

## Consequences and pitfalls — MANDATORY (Dave #165)

**(a) Every cut here trades a loud surface for a quiet one, and one of them trades a real
guarantee.** Today a session cannot miss a warn, because all 17 print every run. After S7 an
unchanged warn prints its **name** but not its **body** — so a warn that was always there and
starts *mattering* will be a name in a list rather than a paragraph. Mitigated three ways and none
of them is complete: names always print, the count moving is called out by name (`⚠ THE SET MOVED:
17 warn(s) at that record, 14 now`), and `--warns-full` restores everything. **What is genuinely
lost: the chance that someone re-reads a familiar warn and notices it differently.**

**(b) The delta is only as honest as the record it diffs against.** If `notes/_REHEARSAL-LOG.jsonl`
is truncated, rewritten, or its last `warn_sigs` line is lost, the printer falls back to FULL
output — loud, never silent. But if a record is written by a run in a *different tree state* (a
lane with a different working diff), warns will read CHANGED for a reason that has nothing to do
with the gate. That is noise, not blindness, and it is the safe direction.

**(c) D3 can silently lose an expiry nobody is told about.** The 119 sweep's verdicts still expire;
nothing now says so at the opener. If a future re-run produces an ACTIONABLE verdict the line
returns on its own — but if the sidecar simply rots for another twenty sessions, **no surface
mentions it again**. That is the trade the package made, and it is why retiring the sweep properly
is still your open item rather than a closed one.

**(d) D4's one non-import consumer is real and will register.** `notes/_dream/_MEMORY-GRADES.json`
entry 40 grades a memory hook on *"all 6 paths named in the hook FILE resolve (first:
`knowledge/_measure_tokenizer.py`; probe: os.path.exists + repo basename index)"*. **That grade
will drop at the next dream pass.** It is a path-resolution grade, not an importer, so the cut
proceeded as briefed — but the hook wants re-pointing at the history that replaced it, and **no
agent may edit your memory store to make the consequence disappear.**

**(e) S1 enforces LENGTH and cannot enforce HONESTY.** See Q2. A cap met by deleting declarations
inverts the asymmetry — *"a declared gap passes, a silent one fails"* — that makes the whole record
trustworthy, and this gate would read green through it.

**(f) S5 is blocking at birth and its window is the whole log.** If a future gauge-log edit
attributes a reading to a #241+ ordinal that already has one — including by the *label-position*
path lane B built, not only inside a stratum — **the wrap will FAIL** until the log is fixed. That
is intended. It also means a wrap can now be blocked by a line written by a *previous* session,
which is a new class of blocker in this file.

**(g) `_CAPTURE-GATE.md` is stale until the next `--build`.** D4 removed the `MEASURERS` entry;
the committed build-mode report at `knowledge/_CAPTURE-GATE.md:7` still lists `ds-021 (C)
CALIBRATION — knowledge/_measure_tokenizer.py`. `_build_all.py` was NOT run by this lane (a partial
run strands the tree) and `--build` was not run on its own. **The next build fixes it; until then
that line names a file that is not there.**

**(h) The savings are in FILL, not in quota** [[budget-vs-quota-vocabulary]]. D2 buys back every
cold session's opening read; S7 and D4 buy back conductor window at every gate run; D3 buys back
the opener. None of them buys quota, so none of them makes a *delegated lane* cheaper — they make
the *conductor's own window* longer, which is the budget that bound #240.

**(i) Nothing was ruled, committed or pushed by this lane.** No ruling was inscribed —
`knowledge/_rulings.json` was not written by me (it carries lane B's uncommitted edit, which I did
not touch). `GOOD-MORNING.md`, `_LIVE-STATE.md`, `_CARRIES.md` and `notes/_GAUGE-LOG.md` were **not
edited**. Every new constant carries a comment naming `s241-D2` — the id is a POINTER TO A RULING
THE CONDUCTOR HAS YET TO INSCRIBE, and if it is inscribed under a different id, five comments and
nine message strings in `_capture_gate.py`, `_gen_chain.py` and `_checkin.py` name the wrong one.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN: S1's saving.** The cap binds the NEXT banner; today it produces a WARN and zero
  tokens of saving. The #240 banner is 3,353 tape against a 1,200 cap, so the *headroom* is 2,153
  tape read and roughly the same written — but **whether a #241 banner can carry its record inside
  1,200 tape is not established by anything I can run.** Price to prove: one wrap.
- **UNPROVEN: how many check-ins a session runs.** Lane D's 3–6 is a division over a date-keyed
  log, not a count, and I did not close it. My per-session floor multiplies D3 by 3. Price to
  prove: one `session` field in `_rehearsal_log_append` and one wrap to observe it — under 200
  tokens of code. I deliberately did NOT add it: `_current_session_no()` reads the ★ LATEST banner,
  which during #241 still says **#240**, so the field would have recorded the wrong number and
  looked right.
- **UNPROVEN: that S7's 1,413 tape actually leaves a conductor's context.** I measured the stdout
  the instrument produces. Whether a given session pipes, truncates or reads it whole is not
  observable from this seat [[unmatched-grep-is-not-an-absence]].
- **UNPROVEN: that no consumer outside this repo reads the 461-id block.** The probe is a grep over
  the repo (lane D's, re-quoted). A skill pack, a shipped `memento-package/`, or your own habit of
  reading the chain for an id are all outside it. Price to prove: `grep -rn "OPEN WORK" designer-
  skills-v*/ apollo-spider/ memento-package/` — not run here.
- **CLAIMED: that finding 6's selftest failure is inherited.** Not claimed — DRIVEN, against three
  module versions in one process. Stated here only because the phrasing "pre-existing" is usually
  a claim; this one has a probe (see Evidence).
- **NOT MEASURED, DELIBERATELY: this lane's own token spend.** No `message.usage` at a sub's seat.

## Evidence

No evidence directory: every figure quotes the command that produced it, and every command is
re-runnable from the repo root. The mutation drives, verbatim:

    # S1, both arms — the same over-cap banner, relabelled
    #   MUTATION (#241 banner, same size):  FAIL ✅  LATEST BANNER CAP (`s241-D2` …)
    #   CONTROL  (short #241 banner):       SILENT ✅
    # S5, three arms
    #   CONTROL   — #241 states it ONCE:   fails=0
    #   MUTATION  — #241 states it TWICE:  fails=1  "session #241 states a first-turn figure 2 times"
    #   MUTATION B— a PRE-RULE stratum twice: fails=0
    # D1/S7 warn delta, five arms + the key-stability clause
    #   control (identical set):        full=0  one=yes
    #   one warn CHANGED (figure moved): full=1 "CHANGED SINCE …"
    #   one warn NEW:                    full=1 "NEW SINCE …"
    #   one warn GONE:                   one-liner leads "⚠ THE SET MOVED: 3 → 2"
    #   no previous record:              full=3, no one-liner  (never a silent empty delta)
    #   key stable across a moved count: True | full digest differs: True
    # finding 6 attribution — one process, three module versions
    #   HEAD (committed) gate            · fat_banner=24 · chain warn? False
    #   PRE-LANE-E (post-lane-B) gate    · fat_banner=24 · chain warn? False
    #   POST-LANE-E gate                 · fat_banner=24 · chain warn? False

Tests run (9): `_capture_gate.py --selftest` (1 inherited failure, finding 6) · `_gen_chain.py
--selftest` (**✅ all bites pass**) · `_gen_chain.py --check` (**✅ FRESH, byte-match**) ·
`_checkin.py --selftest-block` (**✅ 8/8 arms**) · a full `_checkin.py` run (rc 0) · two full
`--wrap` runs · the three mutation suites above. `_build_all.py` was NOT run.

`git diff --stat` (whole tree — **`_RUNBOOK-context-gauge.md`, `_gauge_tokens.py`,
`_surface_recorder.py` and `_rulings.json` are lane B's uncommitted edits, not mine**):

     _CHAIN.md                           |   8 +-
     knowledge/_RUNBOOK-context-gauge.md |  40 ++
     knowledge/_capture_gate.py          | 705 ++++++++++++++++++++++++++++++------
     knowledge/_checkin.py               |  29 +-
     knowledge/_gauge_tokens.py          | 138 ++++++-
     knowledge/_gen_chain.py             |  23 +-
     knowledge/_rulings.json             |  16 +
     knowledge/_surface_recorder.py      |   6 +-
     notes/_REHEARSAL-LOG.jsonl          |   8 +
     notes/_dream/_GRADE-DECISIONS.jsonl |   4 +
     10 files changed, 830 insertions(+), 147 deletions(-)
    --- staged (D4, not committed) ---
     knowledge/_measure_tokenizer.py     | 106 ------------------------------

Lane E's own share of `_capture_gate.py`, diffed against the pre-lane-E tree: **+304 / −18**.
Files touched by this lane: `_CHAIN.md` (generated) · `knowledge/_capture_gate.py` ·
`knowledge/_checkin.py` · `knowledge/_gen_chain.py` · `knowledge/_measure_tokenizer.py` (deleted).
`notes/_REHEARSAL-LOG.jsonl` and `notes/_dream/_GRADE-DECISIONS.jsonl` grew by their instruments'
own appends, as they do on every run.

REPLAY-THESE: `notes/_subreports/2026-09-02-241-lane-D-ritual-diet.md` § PART 4 + § Consequences
(~2,400 tk — the package this lane applied, and the D1/S7 attribution error is in its PART 4 table
where the conductor will look) · `knowledge/_capture_gate.py` § the `s241-D2` constant block at
`BANNER_LATEST_CAP_*` (~600 tk — the cap Dave is asked to confirm in Q1, in its standing home)
