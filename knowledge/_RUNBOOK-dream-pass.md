# Runbook — dream-pass CONDUCTOR (the "run dream pass" sequence)

*Single source for the conductor side of the Memento dream-pass lane, exactly as `dreamer.md`
is single source for the dreamer side (A-D3 discipline: task prompts, skills and dispatches say
"read + follow" — they never restate). Stood up 2026-07-26 (S-D4) after two proven passes,
because the conductor checklist lived only in chat prompts — the reconstruct-from-memory
failure this lane exists to hunt. Trigger phrases: "run dream pass", the weekly task
(`memento-dream-pass`, Sun 07:10), or any manual/unscheduled run.*

*Lane record: `_LIVE-STATE.md` §🔀 · rulings ledger: `notes/_MEMENTO-DECISIONS.md` ·
dreamer spec: `.claude/agents/dreamer.md`.*

## The sequence

1. **Title + framing.** Title the session `Dream-pass · <cadence> lane run (<date from date>)`.
   Lane framing: ignore `GOOD-MORNING.md`; run COLD from `_LIVE-STATE.md` §🔀 (the lane is ruled
   outside the GM queue and dogfoods its own cold-read thesis).
2. **Routing announce, unprompted, at start:** conductor on the session's own model; dreamer =
   **Opus, pinned, as subagent** (Mode-2 deliberate delegation, per the routing audit).
3. **READ FIRST, in order** (read-not-restate): `_LIVE-STATE.md` §🔀 → `notes/_MEMENTO-DECISIONS.md`
   → the **checked-clear lists** at the end of EVERY prior proposals file in `notes/_dream/` →
   `.claude/agents/dreamer.md`.
4. **Lock/state check** before spawning: `git status` clean (reconcile anything dirty — a dirty
   tree is a FLAG, not a blocker for the pass, but it must be named); locks cleared by `mv` into
   `_to_delete/` (the sandbox delete-guard regenerates `index.lock` on every git call — known,
   not a mystery); note the push state (`origin/master` vs HEAD).
5. **Dispatch the dreamer** (one cold Opus subagent). The dispatch supplies ONLY: shape +
   transcript count (A-D2 default: last ~15) · provenance session-id + date-from-`date` ·
   the do-not-re-float list (every RULED row in the ledger + every checked-clear item) ·
   the versioning fact (if today's proposals file exists, output is `-vN`, never overwrite) ·
   "only repo output = the proposals file". Everything else comes from `dreamer.md`.
6. **Conductor spot-check, ≥3 receipts, INDEPENDENTLY re-run** (grep/read/measure yourself —
   never accept the dreamer's numbers as receipts for themselves). Chase every count that
   doesn't match exactly; twice on 2026-07-26 a claimed "0 hits" was really 1–2 benign hits
   that needed naming before accept. Also verify the dreamer's cleanup claim: `git diff HEAD`
   clean, only the proposals file new.
7. **Commit, mechanical rule:** only-the-proposals-file dirty → `bash knowledge/_git_commit.sh
   --reconciled <msgfile>` (msgfile unique, in the session's outputs dir). Anything ELSE dirty →
   leave it and flag it; never sweep it into the lane commit.
7b. **Conductor writes the lane's status to `_LIVE-STATE.md` — BETWEEN the commit and the gate.**
   *(Seam ①, ruled Dave 2026-08-08 #128.)* Append ONE dated line to `_LIVE-STATE.md` **§🔀 SPIN-OFF
   LANE — Memento dream-pass**, and refresh the file's **"Last refreshed" zone** (the header zone the
   wrap gate reads — first 40 lines; see `_capture_gate.py`'s `"Last refreshed"` check) to today.
   The line says, at minimum: **whether the pass was scheduled or manual · whether it was overdue and
   from where · how many proposals and their ids · what became of them (ruled / held / rolled) ·
   the commit ref.**
   ⚠ **Why this step exists, and why HERE:** the lane's own charter sentence is *"the weekly task
   dreams; Dave rules; sessions enact"* — but the lane wrote its output to `notes/_dream/` and its
   rulings to the ledger, and **§🔀 stopped being updated after 2026-07-26**, so live state could not
   see whether the lane had run, was overdue, or had produced anything. Five passes ran before anyone
   noticed. It sits between the commit and the gate because the commit is what makes the pass real
   and the gate is what checks the file is fresh — a status written before the commit describes an
   intention, and one written after the gate is a status the gate never saw.
8. **Gate:** `python3 knowledge/_capture_gate.py --wrap --lane` (S-D2/S-D3: GM-header check
   skipped-and-printed; stdout-only).
9. **Fixed report to Dave:** lane · routing · reads · lock/state · pass shape · proposals
   one-per-line with prevalence · spot-check score · guardrails · gate result · commit hash ·
   gauge stamp. Plain-language read-back available on request — rulings are recorded only after
   reflect-back (V2 precedent: "do it" rows enact; an unsure row HOLDS).

> **⚠ ABSENCE IS THE FAILURE SIGNAL (M11, 2026-07-27).** If a scheduled fire produces NO
> proposals file, that absence IS how this lane reports failure — there is nothing else to
> read. Go to the session transcript. **Nothing in the repo is at risk when a pass dies:**
> the pass's only output is the proposals file, it never pushes, and promotion is Dave's
> alone. A silent Sunday means the pass did not run or did not finish, never that it ran and
> found nothing — a pass that finds nothing still writes the file and says so.
>
> The CONDUCTOR model is deliberately unpinned (whatever the scheduled session runs as); the
> **dreamer subagent IS pinned to Opus** and that pin is load-bearing — it is the half that
> reads cold and must think on its feet.

## The B3 refresh arm — grades in a sidecar (RULED s179-D1, built #180)

Every pass runs `python3 knowledge/_gardener.py --refresh`. It re-derives one MECHANICAL probe
per `MEMORY.md` hook, re-runs it, and restamps `notes/_dream/_MEMORY-GRADES.json` — a SIDECAR,
never the index: boot cost stays zero and no boot-floor re-base is owed, which is exactly what
Dave ruled (B-then-review). Grades are `FRESH · AGING · STALE · UNPROVABLE`, and **the schema and
vocabulary are PROVISIONAL — Dave rules them at the B3 review** (brief §7). `UNPROVABLE` is a
first-class grade, not a gap: an entry with no re-runnable claim is never quietly called fresh.
The bounded mitigation is one block in the check-in output (`knowledge/_checkin.py`, the boot
chain-read seam): starred/blocked entries ONLY, STALE ones listed, the rest counted. **That
surface is NOT ruled permanent** — every printing logs a row with its cost, measured in real
tokens, to `notes/_dream/_GRADE-DECISIONS.jsonl` (first live drive #180: header + one alert line
= **105 real tokens**; the `⚠ SURFACE COST` instrument line that reports it is a further 70 and
disappears when the surface is ruled). The other half of the return-with-numbers is human and is
never inferred: when a grade actually changes what you retrieve, say so with
`--grade-decision <entry-id> --changed yes|no --note "..."`.
⛔ **EVERY PASS RECORDS AT LEAST ONE `--grade-decision` ROW for the grades it actually consulted,
INCLUDING A `--changed no` — a nil return is a datapoint and an absent return is not**
(`s183-D1`, dream pass 8 P4b). ⛔ **Never backfill or synthesise decision rows** — the human half is
worth exactly what it is, and inventing it manufactures the CLAIMED class ADR-0016 forbids.
★ **THE RETURN DATE, AMENDED (`s183-D1`, dream pass 8 P5 form (a)) — the DATE moves, the CONSTANT
does NOT:** the return-with-numbers reports **after the FIRST cycle on the COST half** (which has
data now) and **after FIVE cycles on the AGING half**, because `GRADE_AGING_DAYS = 30` cannot move
a single entry inside a 7-day window — one cycle of AGING evidence would be *no signal* read as
*no decay* [[unrun-search-indistinguishable-from-absent-record]]. ⛔ `GRADE_AGING_DAYS` is
UNTOUCHED and stays Dave's at the review; this amends the REVIEW PLAN only.
★ **The counting window is GENERATED, not noted:** `GRADE_WINDOW_OPEN` in `knowledge/_gardener.py`
carries the ruled instant (`2026-08-16T06:10:28Z`, the scheduled fire) and the sidecar's schema
block restates it; the `--refresh` receipt reports countable rows as `at >= window_open`.
After the cycle above, both figures
go back to Dave — the fork is a deferral with a return date. Failures are loud: a missing index,
a corrupt sidecar or an unknown probe kind BLOCKS; `--selftest-grades` is the mutation test.

## Guardrails (unchanged, non-negotiable)

Nothing self-promotes; promotion is Dave's alone, on reading the file. The proposals file is
the pass's ONLY repo output. Enactment of rulings is a separate act in the same or a later
session, each with its own receipts, ledger rows, and commit.

## Standing carries (don't re-open, just carry)

P6 gauge Half-2 rebuild (own session, parked `_FUTURE-STATE.md`) · D6 Dave's Copilot access
check before any Shape C build · convergence `-v2` §7 leftovers. Prune this list as items close.
