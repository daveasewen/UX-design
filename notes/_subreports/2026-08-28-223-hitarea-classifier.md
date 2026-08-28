# `#223` — `_validate_hit_area.py` third state + the classifier's EXIT-77 arm (s223-D5 ①②)

session: `#223` · 2026-08-28
window: Fable conductor, build lane (Opus sub)
sub index: `hitarea-classifier`
brief: inline in the spawn message — no `notes/_briefs/` file for this lane
tokens: `UNMEASURED — a sub cannot read its own message.usage`; effort band M, ~12K job-window.

## VERDICT

DONE, both clauses of `s223-D5`, both mutation-proved.

**① The classifier learned the exit-77 arm.** `classify()` in
`knowledge/_release/_gen_pack_manifest.py` now files a `COULD-NOT-ASK` refusal as **NEEDS-DEP**,
naming the remedy the refusal itself printed. Driven on the REAL runs of all three browser gates
in this sandbox's third state: all three file `NEEDS-DEP`. Controls hold — a genuine raw crash at
rc=1 still files `REPO-BOUND`, a clean pass and a clean measured FAIL still file `RUNNABLE`.

**② `_validate_hit_area.py` got the same third-state repair** as the two gates the earlier sub
fixed: a launch failure is now `COULD-NOT-ASK … ` at exit **77**, not a raw traceback at rc=1.
All three measuring entry paths (`--all`, `--selftest`, explicit file) drive to 77; the
no-input-files argument refusal correctly still exits 2.

Generator selftest: **198 bites, 0 fail** (was 195 at v1.0.2 — I ADDED three bites for the new
arm, no fixture was changed and none regressed).

⚠ ONE PREMISE CORRECTION, and it matters for how the refusal reads: this sandbox is NOT in the
"no binaries at all" state for *this* gate. `_validate_hit_area._shell_path()` also globs
`/var/tmp/pw-browsers*`, and a **stale chromium from `#220` is still sitting there** — a real
314 MB binary that cannot start because `libXdamage.so.1` is absent from this box. So hit-area's
pre-existing "no headless_shell found" guard never fired; the defect actually repaired is
**browser PRESENT but unstartable**, which the other two gates never met. Both states now refuse
honestly, and the refusal says which one it is with the right remedy for each (see F3).

COUNTS: findings `7` · ruling-shaped `2` · UNPROVEN/COULD-NOT-RUN `3`

## What was done

Two files edited. No commit, no `git add`, no `git checkout`, no browser binaries installed, no
memory hook written, `knowledge/_rulings.json` NOT touched. The two already-repaired gates were
not edited (they were only RUN, to classify their real output).

- `knowledge/_validate_hit_area.py` — new `_harness_unavailable(e)` helper; the single
  `p.chromium.launch(...)` call in `measure()` is now wrapped and routes any launch failure
  through it. It returns the file's existing `RuntimeError("HIT-AREA: HARNESS UNAVAILABLE — …")`,
  so the refusal leaves by the door `#209` already built in `__main__` rather than a new one —
  exactly descender's shape. Three comment/docstring lines updated for truth (the exit contract,
  `measure()`'s "exit 2" line, and the `__main__` comment that used to promise a present-but-broken
  browser stays rc=2 — it does not any more, and now says so).
- `knowledge/_release/_gen_pack_manifest.py` — `REFUSAL_EXIT = 77` + `REFUSAL_REMEDY` constants
  beside `MODNOTFOUND`; `_refusal_dep(blob)` helper; the `rc == REFUSAL_EXIT` arm in `classify()`;
  the module docstring's verdict legend amended; three new `--selftest` bites.

⚠ `_gen_pack_manifest.py` also carries OTHER `#223` subs' edits in the working tree (the version
bump / ratify re-key). `git diff --stat` on it reads 103 changed lines; mine are the four hunks
listed above only.

## Findings

**F1 — the crash, reproduced (`--all`, before the fix).**

```
$ cd knowledge && timeout 150 python3 _validate_hit_area.py --all
  - [pid=20][err] /var/tmp/pw-browsers-220/chromium_headless_shell-1234/chrome-linux/headless_shell:
    error while loading shared libraries: libXdamage.so.1: cannot open shared object file:
    No such file or directory
  - [pid=20] <process did exit: exitCode=127, signal=null>
playwright._impl._errors.TargetClosedError: BrowserType.launch: Target page, context or browser
  has been closed
RC_ALL=1
```

rc=1 is the code `--strict` returns for a REAL measured hit-area breach — an environment fact
wearing the vocabulary of a design defect. `TargetClosedError` is not a `RuntimeError`, so the
`#209` handler in `__main__` never saw it.

**F2 — why the pre-existing guard did not catch it.** `_shell_path()` (line ~287) searches
`PLAYWRIGHT_BROWSERS_PATH`, then `/var/tmp/pw-browsers*`, then `~/.cache/ms-playwright`. Measured:

```
/var/tmp/pw-browsers-220/chromium_headless_shell-1234/chrome-linux/headless_shell   (314181896 bytes, Aug 27)
~/.cache/ms-playwright                                                              (does not exist)
```

The `#220` leftover satisfies the guard, so the gate proceeded to a launch that could never
succeed. `_validate_descender_computed.py` does NOT glob `/var/tmp/pw-browsers*`, which is why it
met the cleaner "Executable doesn't exist" state. Same class, two different faces
[[premise-ages-faster-than-rule]].

**F3 — the fix, driven, all entry paths.**

```
$ timeout 150 python3 _validate_hit_area.py --all
COULD-NOT-ASK: HIT-AREA: HARNESS UNAVAILABLE — playwright is installed and a chromium binary was
found, but it would not START on this box (TargetClosedError: BrowserType.launch: Target page,
context or browser has been closed | /var/tmp/pw-browsers-220/chromium_headless_shell-1234/
chrome-linux/headless_shell: error while loading shared libraries: libXdamage.so.1: cannot open
shared object file: ). The binary is on disk; what failed is starting it — `playwright install
--with-deps chromium` re-installs it together with the system libraries it needs. This gate
measures rendered hit-target geometry and cannot be answered without a browser. Inside this design
system's own CI the proof lives in the `render` job of .github/workflows/gates.yml, which installs
chromium and runs this BLOCKING — nothing here is claimed green, and THIS IS NOT A SKIP: the
question was unaskable on this box.
RC_ALL=77

RC_SELFTEST=77      # python3 _validate_hit_area.py --selftest  (same line)
RC_ONEFILE=77       # python3 _validate_hit_area.py snippets/Button.reference.html
RC_BARE=2           # ✖ HIT-AREA: no input files. Pass paths or --all.  ← unchanged, correct
```

Two deliberate departures from a straight copy of descender's message, both because the state here
is different and a refusal is only honest if the reader can ACT on it:

1. the FIRST line of a playwright launch error names the API call, not the cause. The cause is the
   call log's first `[err]` line. `_harness_unavailable` collapses **both** onto one line joined
   by ` | `, capped at 240 chars — F3 of the earlier sub-report proved the reason must be ONE LINE
   or `_could_not_ask.reason_in()` truncates it in every consumer's summary. Verified, not argued:
   `cna.reason_in(out)` on the real output returns `REASON_LINES= 1` and its tail is the full
   `…the question was unaskable on this box.` — nothing lost.
2. the remedy is conditional. `playwright install chromium` is the WRONG instruction when the
   binary is already on disk; that branch says `playwright install --with-deps chromium` instead,
   and the "binaries were never downloaded" branch keeps descender's wording.

**F4 — the no-binary branch still refuses too (direct function drive).** `_shell_path()` was
monkeypatched to `None` to simulate the literally-empty box, then `measure()` called:

```
NO-BINARY BRANCH -> HIT-AREA: HARNESS UNAVAILABLE — no chromium headless_shell found under
PLAYWRIGHT_BROWSERS_PATH / /var/tmp/pw-browsers* …
routes to 77? True
```

Named as a monkeypatched drive, not a subprocess run: the `#220` leftover cannot be hidden from a
real invocation on this box without deleting it, which was out of scope.

**F5 — mutation proof, hit-area.** Restored the pre-fix bare launch, drove `--all`, restored.
Mutate → drive → restore inside ONE bash call with `trap … EXIT`, because nothing survives a
tool-call boundary here:

```
MUTATED (fix removed)
RC_MUTANT_ALL=1
playwright._impl._errors.TargetClosedError: BrowserType.launch: Target page, context or browser…
RC_RESTORED_ALL=77
RESTORED-IDENTICAL              # diff -q against the pre-mutation backup
```

**F6 — THE CLASSIFICATION, driven on the REAL runs of all three gates.** `classify()` loaded from
the working-tree `_gen_pack_manifest.py` and called on the actual `(rc, out, err)` of each gate,
`shipped=[]`:

```
== REAL RUNS, this sandbox's third state ==
_validate_hit_area.py              rc=77  -> NEEDS-DEP  | playwright install --with-deps chromium
_validate_state_contrast.py        rc=77  -> NEEDS-DEP  | playwright install chromium
_validate_descender_computed.py    rc=77  -> NEEDS-DEP  | playwright install chromium
```

All three file `NEEDS-DEP`, and each names its OWN remedy — the classifier reads it out of the
refusal's backticks, it does not guess [[feedback-measuring-tool-must-not-guess]]. Before this arm
all three fell through to `('RUNNABLE', 'ran, verdict FAIL (exit 77) — a verdict is a run')`.

Two consequences repaired at once: `NEEDS-DEP` ships (`ship_gates = runnable + needsdep`), and the
differential arm is gated on `verdict == "RUNNABLE" and rc != 0`, so a refusal can no longer be
printed to Dave as "a live red, not a packaging fence".

Placement is deliberate and commented in the file: the arm sits **below** `MODNOTFOUND`, so the
pre-existing `classify/caught-import` bite (a 77 refusal that names `playwright`) still returns the
precise module name rather than the remedy sentence.

**F7 — the controls, real runs, named exactly.**

```
CONTROL A (mutant, raw crash) rc=1 -> ('REPO-BOUND', 'crashed:   - [pid=20] <gracefully close end>')
CONTROL B (real pass)         rc=0 -> ('RUNNABLE', 'ran clean, verdict PASS')
CONTROL C (clean fail, harness) -> ('RUNNABLE', 'ran, verdict FAIL (exit 1) — a verdict is a run')
```

- **A** is a REAL run: `_validate_hit_area.py --all` with the fix mutated out (the same
  mutate→drive→restore call, `RESTORED-IDENTICAL`). A genuine crash is still REPO-BOUND — the
  77 arm did not widen into rc=1.
- **B** is a REAL run: `python3 _validate_screen.py` (bare), which exits 0 in this sandbox because
  its bare invocation never reaches a launch.
- **C** is a MINIMAL HARNESS, not a run: `classify(1, "FAIL: 3 components missing a binding", "", [])`
  — the existing `classify/clean-fail` fixture, called directly. Declared as such: no gate in this
  repo returns a clean measured red on this box right now, so I did not have a real one to quote.

**F8 — the generator's own selftest, and a mutation on the new arm.**

```
$ python3 knowledge/_release/_gen_pack_manifest.py --selftest
selftest: 198 bites, 0 fail(s)          RC=0

# with `if rc == REFUSAL_EXIT: return "NEEDS-DEP", _refusal_dep(blob)` deleted:
selftest: 198 bites, 2 fail(s)
  RED [classify/refusal-is-needs-dep] got 'RUNNABLE', wanted 'NEEDS-DEP' a refusal is not a verdict
  RED [classify/refusal-names-its-own-remedy] got 'ran, verdict FAIL (exit 77) — a verdict is a run',
      wanted 'playwright install --with-deps chromium'
RC_MUTANT=1
RESTORED-IDENTICAL
```

195 → 198 is three ADDED bites, not a changed fixture: `classify/refusal-is-needs-dep`,
`classify/refusal-names-its-own-remedy`, and `classify/refusal-arm-does-not-widen` (a measured red
at rc=1 must stay `RUNNABLE`). No existing bite was edited and none regressed
[[instrument-without-a-consumer]] — the arm has a consumer that fails when it is removed.

## RULING-SHAPED QUESTIONS

1. **The stale `/var/tmp/pw-browsers-220` chromium is a live trap for the NEXT probe run.** It is
   found by `_shell_path()` and cannot start. Any gate that globs `/var/tmp/pw-browsers*` will meet
   it, and (until this fix) crashed on it. The fix makes that honest, but the probe of record will
   now file hit-area `NEEDS-DEP` because of a leftover directory rather than a genuinely absent
   dependency. Delete it before the regen, or `playwright install --with-deps chromium` on the
   probe box? Not decided here — deleting files outside the repo was not in scope.
2. **`_validate_screen.py`'s browser path is still unmeasured in this state** (its BARE invocation,
   the one the probe uses, exits 0 without launching, so the probe verdict is unaffected). It holds
   the fourth `chromium.launch` in the gate roster. Extend the same repair to it in this commit —
   "fix the class, not the instance" applied one step further — or leave it, since the probe never
   reaches its launch? Surfaced, not decided.

## UNPROVEN / COULD-NOT-RUN (ADR-0016)

- **COULD-NOT-RUN: the end-to-end `--probe --commit <sha>`.** Driven and refused by design:
  `$ python3 knowledge/_release/_gen_pack_manifest.py --probe` → `REFUSED: --probe needs --commit
  <sha> (a probe of 'the tree' is a probe of nothing reproducible)`, `RC_PROBE=2`. Staging is
  `git archive <sha>`, so the probe can only see COMMITTED content and this lane may not commit.
  As the brief directed, the classification claims in F6/F7 were proved by calling `classify()`
  directly on the real captured runs — the same function the probe calls, on the same inputs.
  The conductor owes one `--probe --commit <sha>` after the commit. Price ~2K tk.
- **UNPROVEN: the GREEN path of `_validate_hit_area.py` on a box with a working browser.** No
  usable chromium exists here and installing one was out of scope. The launch call's arguments are
  byte-identical to what was there before (only a `try:` and the 4-line arg list re-wrapped around
  it) and `py_compile` is clean, but "unchanged by construction" is not a measurement
  [[planning-estimate-is-not-a-measurement]]. Price: the CI `render` job, or one
  `playwright install --with-deps chromium`.
- **UNPROVEN: what the new NEEDS-DEP reason looks like on Dave's release page.** The HTML renderer
  prints `"needs " + esc(v["why"])`, so hit-area would read *"needs playwright install --with-deps
  chromium"*. Read from the source at the `order = {...}` block, not from a rendered page. Price:
  one `--manifest` run at a commit.
- **Residual, declared:** the module docstring of `_validate_hit_area.py` still describes its
  harness section in `#209` terms elsewhere; only the exit-code contract line was corrected.
  Left as one line for a later pass rather than widening this lane.

## Evidence

No evidence files — every claim above quotes its probe inline. Mutation backups lived at
`/var/tmp/ha.bak`, `/var/tmp/ha2.bak`, `/var/tmp/gm.bak`, each consumed and verified by `diff -q`
inside the same bash call that created it.

⚠ ENVIRONMENT: unchanged by this lane. playwright 1.62.0 is still installed (the earlier sub
installed it), no browser binaries were added or removed, and `/var/tmp/pw-browsers-220` was left
in place — see RULING-SHAPED Q1.

REPLAY-THESE: `python3 knowledge/_release/_gen_pack_manifest.py --probe --commit <sha>` after the
commit — the one thing this lane could not prove end to end, and the roster number it reads is
Dave's (~2K tk) · RULING-SHAPED Q1, because the stale `/var/tmp` chromium decides whether the
regen files hit-area `NEEDS-DEP` for a real reason or a leftover one (~1K tk) · F8's bite count
195 → 198, so the conductor does not read it as a regression (~0.5K tk).
