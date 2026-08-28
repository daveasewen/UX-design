# `#223` — the browser-gate THIRD STATE (playwright imports, browsers absent)

session: `#223` · 2026-08-28
window: Fable conductor, build lane
sub index: `browser-third-state`
brief: (inline brief in the spawn message — no `notes/_briefs/` file for this lane)
tokens: `UNMEASURED — a sub cannot read its own message.usage`; effort band M, ~15K job-window
budget, spend reported in the stub from the conductor's own accounting.

## VERDICT

DONE for the two gates the brief named. Both `knowledge/_validate_state_contrast.py` and
`knowledge/_validate_descender_computed.py` now answer the third state — playwright IMPORTS,
its browser binaries are NOT installed — with the ruled `COULD-NOT-ASK:` legal form at exit 77
instead of a raw traceback at rc=1. Reproduced first, fixed, re-driven, and mutation-proved in
both directions on all three affected entry paths (bare run ×2, `--selftest` ×1). The exact
consequence the brief named is now DRIVEN, not argued: `classify()` from
`knowledge/_release/_gen_pack_manifest.py`, called on the REAL captured runs, returns
`REPO-BOUND` before the fix and `RUNNABLE` after it.

Three things the conductor must not miss. **(1)** The committed probe of record
(`knowledge/_release/_pack_gate_probe.json`, commit `789f4331`) ALREADY carries these two gates
as `REPO-BOUND` with the browsers-missing signature — the defect has already bitten the pack's
recorded probe, so this is a live drop from the ship list, not a hypothetical. **(2)** A THIRD
gate has the identical defect: `_validate_hit_area.py --all` still crashes raw at rc=1 in this
state and classifies `REPO-BOUND` — the brief's DO-NOT-RULE list reserves its membership for
Dave, so it was measured and left untouched. **(3)** `classify()` has NO `rc == 77` arm, so the
fixed gates now land in `RUNNABLE` by the fall-through "a verdict is a run" branch — the ship
list is restored, but a REFUSAL is being recorded as a verdict FAIL. New classification
vocabulary is Dave's; it is a ruling-shaped question below.

COUNTS: findings `7` · ruling-shaped `3` · UNPROVEN `3`

## ⚠ ENVIRONMENT CHANGED — READ BEFORE RE-RUNNING ANY BROWSER GATE

This lane installed `playwright` 1.62.0 into the sandbox (`pip install playwright
--break-system-packages`) and deliberately did NOT install browser binaries — that absence IS
the third state under test. The sandbox is therefore left in the third state. Every browser gate
in `knowledge/` now meets browsers-missing rather than the older module-missing state, which
changes what they print. To restore the clean box:

```
pip uninstall -y playwright --break-system-packages
```

Left installed on purpose so the conductor can replay the proofs below.

## What was done

Two files edited, nothing else. No commit, no `git add`, no `git checkout`, no browser binaries
installed, no memory hook written.

- `knowledge/_validate_descender_computed.py` — `launch()` now wraps its single
  `p.chromium.launch(...)` and routes any failure to a new `_browser_unreachable(e)` helper,
  which returns the pre-existing `DescenderUnreachable`. `__main__` already converts that class
  to `cna.refuse(...)` → 77, so the new state reaches the door #221 built rather than a new one.
- `knowledge/_validate_state_contrast.py` — new `LAUNCH_ARGS` constant plus `_launch_chromium(p)`
  as the ONE home (ADR-0017 write-once) for starting this gate's browser. Both launch sites now
  go through it: the bare audit run (was an unguarded launch → raw traceback at rc=1) and
  `_measure_fixtures()` in the selftest, including the s152-D1 mutation control's second launch
  (was a local `except Exception -> StateContrastSelftestError`, i.e. rc=**2**, this file's
  ARGUMENT-error code — an environment fact wearing the vocabulary of a mistyped flag).

Message register copies #221's enacted shape: the refusal names what is absent, names the
remedy `playwright install chromium`, and carries the not-a-skip caveat pointing at the `render`
job of `.github/workflows/gates.yml` where the proof of record lives (state-contrast's caveat is
appended by its existing `__main__` handler; descender's is inside the message because its
`__main__` handler appends none).

## Findings

**F1 — the defect, reproduced (both gates).** After `pip install playwright
--break-system-packages` with no `playwright install`:

```
$ cd knowledge && timeout 150 python3 _validate_descender_computed.py
  File ".../_validate_descender_computed.py", line 235, in launch
    return p.chromium.launch(executable_path=shell[0] if shell else None, headless=True,
playwright._impl._errors.Error: BrowserType.launch: Executable doesn't exist at
  /sessions/nice-dreamy-johnson/.cache/ms-playwright/chromium_headless_shell-1234/chrome-linux/headless_shell
╔════════════════════════════════════════════════════════════╗
║ Looks like Playwright was just installed or updated.       ║
...
RC=1
```

`_validate_state_contrast.py` bare: byte-identical shape, `RC=1`, same
`playwright._impl._errors.Error: BrowserType.launch: Executable doesn't exist at ...` tail.

**F2 — the fix, driven (three entry paths, all 77).**

```
$ timeout 150 python3 _validate_descender_computed.py
COULD-NOT-ASK: DESCENDER-COMPUTED: HARNESS UNAVAILABLE — playwright is installed but its BROWSER
BINARIES are not — the chromium executable it drives was never downloaded (Error:
BrowserType.launch: Executable doesn't exist at /sessions/nice-dreamy-johnson/.cache/ms-playwright/
chromium_headless_shell-1234/chrome-linux/headless_shell) — this gate measures rendered geometry
and cannot be answered without a browser. Install them with `playwright install chromium`. Inside
this design system's own CI the proof lives in the `render` job, which installs chromium and runs
this BLOCKING — nothing here is claimed green, and THIS IS NOT A SKIP: the question was unaskable
on this box.
RC_DESC=77

$ timeout 150 python3 _validate_state_contrast.py
COULD-NOT-ASK: _validate_state_contrast.py — playwright is installed but its BROWSER BINARIES are
not — the chromium executable it drives was never downloaded (Error: BrowserType.launch:
Executable doesn't exist at ...headless_shell) — this gate measures rendered pixels and cannot be
proven without a browser; install them with `playwright install chromium` ⇒ THIS IS NOT A SKIP:
these arms (including the s152-D1 mutation control) run BLOCKING in the `render` job of
.github/workflows/gates.yml, which installs chromium — that job is where this gate's proof of
record lives. Nothing here is claimed green; the question was unaskable on this box.
RC_SC_BARE=77

$ timeout 160 python3 _validate_state_contrast.py --selftest
  ok   arm_refusal_is_machine_readable_and_names_its_reason
  ok   arm_refusal_says_where_the_proof_lives
  ok   arm_refusal_is_scoped_to_the_missing_import
COULD-NOT-ASK: _validate_state_contrast.py — playwright is installed but its BROWSER BINARIES are
not — ... (as above)
RC_SC_SELFTEST=77
```

The three #193/#221 refusal arms still run and still pass in this state — the new refusal did not
widen into them.

**F3 — the reason must be ONE LINE, and the first cut was not.** `_could_not_ask.reason_in()`
(`knowledge/_could_not_ask.py:82`) returns *the first* marked line and nothing after it.
Playwright's launch error carries a multi-line ASCII-box banner ("<3 Playwright Team"), so the
first version of this fix produced a refusal whose reason was truncated mid-sentence in every
consumer's summary (`_build_survey.py`, `_probe_registry/_registry.py`, the pack runner) —
including state-contrast's NOT-A-SKIP tail. Both gates now take
`type(e).__name__` + the FIRST line of the message, whitespace-collapsed, capped at 240 chars.
Driven: the outputs in F2 are single lines. This was caught by re-reading the produced artefact,
not by reasoning about it [[enactment-register-adr-0016]].

**F4 — mutation proof, descender.** Restored the pre-fix raw-raise path
(`raise _browser_unreachable(e)` → `raise`), drove it, restored:

```
mutated
╚════════════════════════════════════════════════════════════╝
RC_MUTANT_DESC=1
COULD-NOT-ASK: DESCENDER-COMPUTED: HARNESS UNAVAILABLE — playwright is installed but its
RC_RESTORED_DESC=77
RESTORED-IDENTICAL          # diff -q against the pre-mutation backup
```

**F5 — mutation proof, state-contrast, BOTH paths.** Bare run, launch un-guarded:
`RC_MUTANT_SC_BARE=1`, `RESTORED-IDENTICAL`. Selftest, old local
`except Exception -> StateContrastSelftestError`: `RC_MUTANT_SC_SELFTEST=2`,
`RESTORED-IDENTICAL`. Both wrong vocabularies are therefore MEASURED, not asserted: rc=1 (the
code a real measured contrast/descender failure returns) and rc=2 (the code a mistyped flag
returns). Every mutation ran mutate→drive→restore inside a single bash call with a `trap … EXIT`
and a `diff -q` receipt, because nothing survives a tool-call boundary in this sandbox.

**F6 — THE CLASSIFICATION, driven on the real runs.** `classify()` in
`knowledge/_release/_gen_pack_manifest.py` is a pure function of `(rc, out, err, shipped)`. Called
on the runs captured above:

```
== POST-FIX (working tree) ==
_validate_descender_computed.py rc= 77 -> ('RUNNABLE', 'ran, verdict FAIL (exit 77) — a verdict is a run')
_validate_state_contrast.py     rc= 77 -> ('RUNNABLE', 'ran, verdict FAIL (exit 77) — a verdict is a run')
== PRE-FIX (mutant: raw raise) ==
_validate_descender_computed.py rc= 1 -> ('REPO-BOUND', 'crashed: ╚═══…═╝')
_validate_state_contrast.py     rc= 1 -> ('REPO-BOUND', 'crashed: ╚═══…═╝')
```

`shipped=[]` was passed; that argument is read only by the path-error branch, which needs a
`Traceback` in the blob and is not reached on either side. The brief's consequence is repaired:
REPO-BOUND gates do not ship (`_gen_pack_manifest.py:1471-1478` — `runnable + needsdep` ship,
`repobound` is dropped), so before the fix these two left the ship list and after it they stay.
⛔ But the verdict reached is `RUNNABLE`, **not** `NEEDS-DEP`: `classify()` has no `rc == 77` arm,
and my refusal text does not trip `MODNOTFOUND` (no "No module named") or `MISSING_LINE`
(playwright says "doesn't exist", the regex asks for "does not exist"). It falls through to the
final `return "RUNNABLE", "ran, verdict FAIL (exit %d) — a verdict is a run"`. A refusal is being
recorded as a verdict FAIL, and — if `--probe` is given `full_stage` — the differential arm would
label these two "a live red, not a packaging fence" (`_gen_pack_manifest.py:829` region). See
RULING-SHAPED Q1.

**F7 — the committed probe of record already shows the bite, and a THIRD gate has it.**
`knowledge/_release/_pack_gate_probe.json` at commit `789f4331242ef7bca6d7bfd8d0f1765bafff6e4f`,
49 gates, `Counter({'RUNNABLE': 38, 'REPO-BOUND': 11})`:

```
_validate_descender_computed.py REPO-BOUND | exit 1 | crashed:   - [pid=257] <gracefully close end>
_validate_hit_area.py           REPO-BOUND | exit 1 | crashed:   - [pid=361] <gracefully close end>
_validate_screen.py             RUNNABLE   | exit 0 | ran clean, verdict PASS
_validate_state_contrast.py     REPO-BOUND | exit 1 | crashed: ╚═══…═╝
```

That probe was taken on a box in the third state. Driven here, in the third state:

- `_validate_hit_area.py` bare → `rc=2`, `✖ HIT-AREA: no input files. Pass paths or --all.` The
  probe's `ARGS_REFUSAL` arm re-invokes it with `--all`.
- `_validate_hit_area.py --all` → `rc=1`, raw traceback,
  `playwright._impl._errors.TargetClosedError: BrowserType.launch: Target page, context or browser
  has been closed`. `classify(1, <that output>, "", [])` →
  `('REPO-BOUND', 'crashed:   - [pid=18] <gracefully close end>')`. Same defect, same drop. NOT
  fixed here: the brief reserves its membership for Dave.
- `_validate_screen.py` bare → `rc=0`, `RESULT: PASS ✅` — it never reaches a launch on the bare
  invocation the probe uses, so it is unaffected on that path.
- Wider class: `grep -rn "chromium.launch" knowledge/ --include=*.py` returns ~50 sites. Only
  `_validate_*.py` files are probed as gates; of those, the launch sites are
  `_validate_state_contrast.py` (fixed), `_validate_descender_computed.py` (fixed),
  `_validate_hit_area.py:333` (SURFACED, untouched) and `_validate_screen.py:92` (unaffected on
  the probed invocation). The `_render/` and `_probe_registry/` families are outside the gate
  roster.

## RULING-SHAPED QUESTIONS

1. **What verdict should a 77 / `COULD-NOT-ASK` gate get in the pack probe?** `classify()` has no
   `rc == 77` arm (F6). Options: (a) add an explicit refusal arm mapping 77 → `NEEDS-DEP` with
   the dependency named from the refusal's own words — honest, keeps the gate shipping, reuses
   existing vocabulary; (b) add a FOURTH verdict (e.g. `REFUSED`) — most accurate, but it is new
   classification vocabulary and every consumer of the verdict table would have to learn it; (c)
   leave the fall-through — the gate ships and the count holds, but the manifest calls a refusal
   a verdict FAIL and the differential arm may print "a live red". This is Dave's: the brief's
   DO-NOT-RULE names gate-classification vocabulary explicitly, and I may not edit
   `_gen_pack_manifest.py` in this lane. Recommend (a) if a recommendation is wanted — it needs
   no new noun.
2. **`_validate_hit_area.py` — same defect, membership reserved.** It crashes raw at rc=1 in the
   third state and classifies REPO-BOUND (F7). Extending the same `_launch_chromium`-shaped fix
   would put it back on the ship list. Its membership is Dave's per the brief. Question: fix the
   refusal path regardless of the membership question (the refusal is honest either way), or hold
   the file untouched until membership is ruled?
3. **The roster count.** The committed probe drops 3 browser gates as REPO-BOUND. With the two
   fixed here they return; `_validate_hit_area.py` does not. Whether the resulting number lands
   on Dave's ruled 55 (s219-D9) is not decidable from this lane and is his in any case — the
   brief's DO-NOT-RULE list says so. Surfaced, not decided.

## UNPROVEN / CLAIMED (ADR-0016)

- **COULD-NOT-RUN: `_gen_pack_manifest.py --probe` against the working tree.** Driven, and it
  refuses by design:
  `$ python3 knowledge/_release/_gen_pack_manifest.py --probe` →
  `REFUSED: --probe needs --commit <sha> (a probe of 'the tree' is a probe of nothing
  reproducible)`, `RC_PROBE_NOCOMMIT=2`. Staging is `git archive <sha>`
  (`_gen_pack_manifest.py:865`), so the probe can only ever see COMMITTED content and this lane
  is forbidden to commit. The classification claim in F6 was therefore proved by calling
  `classify()` directly on the real captured runs, which is the same function the probe uses on
  the same inputs — but the END-TO-END probe on a named commit is the conductor's to re-prove at
  the regen step. Price: one `--probe --commit <sha>` run after the fix is committed.
- **UNPROVEN: the green path is unchanged on a box WITH browser binaries.** No browsers exist
  here and installing them was forbidden, so the passing run of either gate was not driven. The
  launch arguments are byte-identical to what was there before (both state-contrast sites used
  the same four args, now the `LAUNCH_ARGS` constant; descender's `executable_path`/`headless`
  kwargs are untouched) and `py_compile` is clean on both files, but "unchanged by construction"
  is not a measurement. Price: the CI `render` job, or one local `playwright install chromium`.
- **UNPROVEN: `_validate_screen.py`'s browser path in the third state.** Its bare invocation —
  the one the probe uses — exits 0 without launching, so the probe verdict is unaffected; what
  its `--all`-equivalent path does with no binaries was not driven. Price: ~1 gate run.
- **CLAIMED (not re-read): that `RUNNABLE` and `NEEDS-DEP` both ship while `REPO-BOUND` does
  not.** Read from `_gen_pack_manifest.py:1471-1478` (`runnable`/`needsdep`/`repobound` lists and
  the helper closure that spans only the first two), not from a driven build. Re-read costs one
  `--manifest` run at a commit.
- **Residual, declared:** `_validate_state_contrast.py`'s module docstring (line 41-42) still
  says an unavailable browser is "a selftest FAILURE, never a silent skip". Since #193 it is a
  REFUSAL at 77 — neither pass, fail, nor skip. Left untouched (the brief scoped this lane to
  the third-state fix); one line for a later pass.

## Evidence

No evidence files: every claim above quotes its probe inline, and the brief's pitfall note about
scratch not surviving the window applies to `/var/tmp/*.bak` (mutation backups, already consumed
and verified by `diff -q`).

REPLAY-THESE: `python3 knowledge/_release/_gen_pack_manifest.py --probe --commit <sha>` after the
fix is committed — the ONE thing this lane could not prove end to end (~2K tk) · F6's
classification block, because the `RUNNABLE`-not-`NEEDS-DEP` fall-through decides whether Q1 must
reach Dave before the bake (~1K tk) · F7's `_validate_hit_area.py` measurement, because it is a
third gate still dropping off the ship list (~1K tk)
