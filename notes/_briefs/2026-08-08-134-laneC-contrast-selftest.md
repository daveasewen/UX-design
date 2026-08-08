# Lane C — `_validate_state_contrast --selftest` env-dependence (residual ⑥ from #133)

## Diagnosis
`knowledge/_validate_state_contrast.py` did `from playwright.sync_api import sync_playwright` at
module top, unguarded. On a box without the `playwright` module this raised a bare
`ModuleNotFoundError` at import time — Python traceback to stderr, process exits **rc=1**.

`main()`'s own contract makes rc=1 mean "a real measured failure" (`total or refused` truthy) and
reserves rc=2 for `StateContrastArgError` / `StateContrastReportError` / `StateContrastSelftestError`
— named, attributable failures (the file already has this exact class for "chromium would not
launch", `StateContrastSelftestError`, rc=2). The missing-module case bypassed that contract
entirely: it was an *unnamed* crash sharing rc=1 with a genuine contrast failure, so two different
environments running the identical `--selftest` command were indistinguishable by exit code alone
— on a box with `playwright` importable but no browser binary installed, it correctly raised
`StateContrastSelftestError` (rc=2, named); on a box without the module at all, it silently
degraded to an ImportError traceback (rc=1, unnamed). That is the env-dependence: same command,
same intent ("prove this gate can be run here"), two different failure shapes depending on what
happened to be `pip install`ed.

Verified directly: `python3 _validate_state_contrast.py --selftest` in this sandbox (no playwright
installed) → `ModuleNotFoundError` traceback, rc=1, confirmed before any fix.

## Fix
Wrapped the import in `try/except ModuleNotFoundError`, capturing the error message as a **plain
string** (not the exception object — `except … as _e` is scoped to the except block and Python 3
deletes `_e` on exit, so a closure referencing it directly raises `NameError` later; caught this in
testing and fixed by capturing `repr(_e)` into a module-level string before the block ends). On
failure, `sync_playwright` is rebound to a stub that raises `StateContrastSelftestError` naming the
missing module and the fix command, deferred to first actual use (inside `run()` and
`_measure_fixtures()`), not at import time — so a normal `import` of the file for e.g. `--help`
still works, but any path that needs a browser gets the same named, rc=2 failure whether the cause
is "module not installed" or "chromium binary not installed." No thresholds, colors, or scope
changed — single guard at the top of the file, same class of fix as the existing
`StateContrastArgError`/`StateContrastReportError`/`StateContrastSelftestError` triad.

## Proof (rc evidence)
```
$ python3 _validate_state_contrast.py --selftest        # before fix
ModuleNotFoundError: No module named 'playwright'         (bare traceback, rc=1)

$ python3 _validate_state_contrast.py --selftest        # after fix
...18 selftest arms run and pass (pure-logic arms don't need a browser)...
StateContrastSelftestError: the 'playwright' module is not installed
(ModuleNotFoundError("No module named 'playwright'")) — this gate cannot be
proven without it; run `pip install playwright && playwright install chromium`
rc=2

$ python3 _validate_state_contrast.py                   # non-selftest path, same env
StateContrastSelftestError: ... (identical message)       rc=2
```
Both call sites now agree: named, attributable, same rc class as every other refusal in this file.

### Mutation test
- Broke it: `s/raise StateContrastSelftestError(/raise RuntimeError(/` → `--selftest` now exits
  **rc=1** with a bare `RuntimeError` traceback (uncaught by `main()`'s except tuple) — proves the
  selftest's own failure mode is reachable, not an assertion that can't fail.
- Restored: `cp` back from a pre-mutation copy, `diff` confirmed **byte-identical**, re-ran
  `--selftest` → rc=2, named `StateContrastSelftestError`, all 18 non-browser arms still pass.

## Residual
Could not install `playwright` in this sandbox (`pip install` failed: `OSError(28, 'No space left
on device')`), so the 7 browser-driven arms (`arm_sibling_paint_is_seen` etc.) were not exercised
end-to-end here — only the 18 pure-logic arms ran, plus the import-guard itself (which is the part
in scope for this lane). The guard's own correctness was proven directly (mutation test above),
independent of whether a browser is ever available. Recommend a follow-up run of `--selftest` in
an environment with headless Chromium installed to confirm the browser-driven arms still pass
unchanged (they were not touched by this fix).
