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

## Guardrails (unchanged, non-negotiable)

Nothing self-promotes; promotion is Dave's alone, on reading the file. The proposals file is
the pass's ONLY repo output. Enactment of rulings is a separate act in the same or a later
session, each with its own receipts, ledger rows, and commit.

## Standing carries (don't re-open, just carry)

P6 gauge Half-2 rebuild (own session, parked `_FUTURE-STATE.md`) · D6 Dave's Copilot access
check before any Shape C build · convergence `-v2` §7 leftovers. Prune this list as items close.
