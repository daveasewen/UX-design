# `#241`-`B` — the boot band DERIVED, the ceiling TYPED, and the parser defect fixed as a class

session: `#241` · 2026-09-02
window: lane B (build lane, `W-386`)
sub index: `B`
brief: chat brief from the conductor (job: build `W-386`); source ruling brief
`notes/_briefs/2026-09-02-240-boot-band-derive-brief.md` (`W-384`)
tokens: `UNMEASURED — no message.usage at a sub's seat`

## VERDICT

**DONE**, all five regions of the brief, with one deliberate exception named below. `s240-D1`,
`s240-D2` and `s241-D1` are ENACTED: `BOOT_FIRSTTURN_TK` / `BOOT_FIRSTTURN_ERR` are **deleted**
from `knowledge/_gauge_tokens.py`, the band is now computed at check time by
`derived_boot_band()`, and `BOOT_CEILING_TK = 70_000` is the one typed number left. The
`boot-drift` check in `knowledge/_capture_gate.py` grades the newest reading against the derived
band AND against the ceiling, fails the ceiling BY NAME, and carries a re-pointed DECLARED legal
form that stays backward-tolerant of the ~37 ratified pre-`s240-D1` lines already in the gauge
log. The #240 parser finding is fixed as a CLASS (ordinal attribution, not a one-line patch) and
the fix is measured, not asserted. **The one exception:** `W-386` is left **OPEN** in
`knowledge/_state.json` — `_state.py` exposes no close verb and `s218-D7` puts store-row minting
at the conductor's seat; the exact close payload is handed over in Findings 9.

COUNTS: files touched `4` · tests run `7` · findings `9` · UNPROVEN `2`

*(ruling-shaped `1`)*

```
 knowledge/_RUNBOOK-context-gauge.md |  40 ++++
 knowledge/_capture_gate.py          | 387 +++++++++++++++++++++++++++---------
 knowledge/_gauge_tokens.py          | 138 +++++++++++--
 knowledge/_surface_recorder.py      |   6 +-
 4 files changed, 460 insertions(+), 111 deletions(-)
```

## What was done

**Region 1 — `knowledge/_gauge_tokens.py`.**
- `BOOT_FIRSTTURN_TK = 56_749` and `BOOT_FIRSTTURN_ERR = 1_154` are **removed**, not commented
  out. `hasattr(_gauge_tokens, "BOOT_FIRSTTURN_TK")` reads `False`. The four historic re-base
  comment blocks above them (`s129-D1`, `s171-D1`, `s208-D1`) are left untrimmed as history.
- New `derived_boot_band(samples=None, n=BOOT_BAND_WINDOW, repo=REPO)` returns
  `(mean, spread, samples, sessions)` or `None`. Passing `samples` is the live path; leaving it
  `None` lazily imports `_capture_gate._parse_boot_samples` (lazy on purpose — `_capture_gate`
  imports `_gauge_tokens`, so a module-level import either way is a cycle).
- New constants: `BOOT_BAND_WINDOW = 7`, `BOOT_BAND_SIGMA = 2.0`, `BOOT_CEILING_TK = 70_000`,
  each with provenance naming `s240-D1` / `s240-D2` / `s241-D1` and the 69,092 reading.
- `measure_boot()` no longer publishes a constant: its `firstturn` / `firstturn_err` terms are
  the derived band, and when the band cannot be derived it falls back to `BOOT_CEILING_TK`
  **labelled as an upper bound, never as a measurement**. Two new keys, `band` and `ceiling`.
- `main()` prints the ceiling line with an `⛔ OVER` / `✅ under` marker.

**Region 2 — `knowledge/_capture_gate.py`.**
- `BOOT_DRIFT_WINDOW = 6` **deleted** — the window is `s240-D1`'s and is read from
  `_gauge_tokens.BOOT_BAND_WINDOW` at check time (a second copy here is the copy-chain class).
- `_parse_boot_samples()` — the CLASS fix (Finding 1).
- `boot_constant_drift_check()` rewritten into two arms: the CEILING (per reading, by name) and
  the DERIVED BAND (newest reading vs mean, red past `BOOT_BAND_SIGMA × spread`).
- `BOOT_DRIFT_DECL_RE` / `BOOT_DRIFT_LEGAL_FORM` re-pointed at the derived band; the old regex
  is kept verbatim as `BOOT_DRIFT_LEGACY_RE` + `_parse_legacy_boot_declarations()` so ratified
  lines are read as HISTORY and never re-stamped.
- `selftest_boot_delta_parse()` gained four arms: ordinal attribution, per-session dedupe, band
  red-on-step / green-on-drift in both directions, and ceiling-breach-by-name.

**Region 3 — drive the thing.** Before/after and mutation runs, Findings 2, 5, 6, 7.

**Region 4 — `knowledge/_RUNBOOK-context-gauge.md`.** A dated `#### ✅ 2026-09-02 (#241)`
paragraph ADDED at the end of § "★ THE FLOOR IS MEASURED, NEVER ASSUMED (GM-D9)". Nothing above
it was rewritten; GM-D9's two rules are byte-untouched.

**Region 5 — `knowledge/_state.json`.** NOT written. See Finding 9.

⛔ **NOT TOUCHED, as fenced:** `GOOD-MORNING.md`, `_CHAIN.md`, `_LIVE-STATE.md`, `_CARRIES.md`,
`notes/_GAUGE-LOG.md` (`git status --porcelain notes/_GAUGE-LOG.md` returns empty), and
`knowledge/_rulings.json` (this lane inscribed NOTHING; the diff on that file is the conductor's).
`_build_all.py` was NOT run.

## Findings

1. **The #240 parser finding is NOT a duplicate-line problem — it is ORDINAL MIS-ATTRIBUTION,
   and the dedupe was already there.** `_parse_boot_samples` took `re.search(r"#(\d+)", line)` —
   the first `#N` ANYWHERE in the line. #239's `PREMISES WERE CHECKED` line restates its own boot
   (75,619) and cites `#238` in a later clause, so that reading was filed under **238**,
   overwriting #238's real 75,336 and putting #239's one reading into the window twice. Probed
   before the fix: `sorted(by_session.items())[-10:]` ended `… (237, 76915), (238, 75619),
   (239, 75619)`. The same class hit **eleven** `Context gauge at authoring:` lines, which
   restate their own session's boot and cite `` `#56-D1` `` (the UNIT ruling) — all eleven were
   filed under session **56**, each clobbering the last.
2. **The fix, and its measured blast radius.** The ordinal now comes from LABEL POSITION (a `#N`
   inside the line's opening `BOOT_LABEL_ORD_MAXCOL = 60` characters AND before the boot figure)
   or, failing that, from the enclosing `#### <date> #N` stratum (`BOOT_STRATUM_RE`). Measured on
   the live log, not asserted: **105 readings parsed before and after, 0 gained, 0 lost, 14
   re-attributed** — the #239 line, the eleven `Context gauge` restatements, one #125 line and
   one unlabelled `**pre-flight:**` that had been sitting in the `-1` bucket. The live window
   changes by exactly one member: **#238 gets its own 75,336 back.**
3. **The spread is the SAMPLE STANDARD DEVIATION (n−1), not the half-range of `s129-D1`/
   `s171-D1`/`s208-D1` — and that is forced, not preferred.** `s240-D1` records the figure Dave
   was shown before ruling: **75,672 ± 641** over #234–#240. Readings 75,206 · 75,294 · 75,198 ·
   76,915 · 75,336 · 75,619 · **76,138** (#240's, read off `GOOD-MORNING.md:478`) give mean
   75,672.28 ✓ and `statistics.stdev` **640.7 → 641** ✓. The half-range method would have said
   **1,243**. The statistic must be the one on which the ruling was taken.
4. **The RED LINE had to be 2× the spread, and the multiplier was MEASURED.** `s240-D1` has two
   clauses and at 1σ the second is false. Driven: a linear ramp of `d`/session over n=7 puts the
   newest reading 3d from the mean against a 2.16d spread = **1.39σ ⇒ RED at 1σ for any slope**,
   which reinstates the exact re-base treadmill the ruling ends. A one-session step of size `S`
   off a flat series is **2.27σ ⇒ RED at 2σ for any step size**. So `BOOT_BAND_SIGMA = 2.0`
   satisfies both clauses and 1.0 satisfies one. This was not designed in — the first
   implementation used 1σ and the new selftest arm caught it, verbatim: *"boot-drift band
   (`s240-D1`, slow drift): expected GREEN, got fails=['… the newest boot reading (#547, 69,600)
   sits +600 from the band …']"*. ⚠ **The band is still REPORTED as `mean ± spread`** — Dave's
   641 — with the red line stated separately and never folded into it.
5. **BEFORE (HEAD, run against the live gauge log in an isolated symlink tree):**
   `boot-drift: constant 56,749 ±1,154 vs recent mean 75,642 (n=6, last 6 sessions of 83 parsed)
   — delta +18892` · 0 fails, passing ONLY on the `#240` DECLARED line, with sample list
   `75,206 · 75,294 · 75,198 · 76,915 · 75,619 · 75,619` — the duplicate visible in the gate's
   own output.
6. **AFTER (live tree):**
   `boot-drift: DERIVED band 75,994 ±1,219 (`s240-D1`, n=7 sessions #233–#239: 78,392 · 75,206 ·
   75,294 · 75,198 · 76,915 · 75,336 · 75,619) · newest #239 75,619 · delta -375 · red beyond
   ±2,438 (2× the spread) · ceiling 70,000 (`s241-D1`, shrink-only)` · **0 fails**. #238's 75,336
   is back; no duplicate.
7. **The mutation tests bite, and the ceiling fails BY NAME.** Scratch copy of the log
   (`/dev/shm`, never the repo) plus one fabricated `#### 2026-09-02 #241 … boot 71,000 real`:
   - `boot-drift CEILING BREACH: `_gauge_tokens.BOOT_CEILING_TK` = 70,000 and 1 post-diet
     reading(s) EXCEED it — #241 71,000. ⛔ `s240-D2`/`s241-D1` make this number SHRINK-ONLY …`
   - and the band arm independently: `… sits -3938 … past the 2× red line of ±3,679 … STEP
     CHANGE … ⛔ AND IT IS UNDECLARED.`
   The mutant was removed; `git status --porcelain notes/_GAUGE-LOG.md` returns empty.
   A second fixture drove the full #111-D1 loop with a realistic 69,092 post-diet reading:
   undeclared ⇒ 1 FAIL; the generated legal-form line
   `> **boot-drift DECLARED #241 (2026-09-02):** newest 69092 · derived band 74666 ±2532 (n=7,
   #234–#241) · delta -5573 · ceiling 70000 · DERIVED at check time per `s240-D1`.`
   appended ⇒ **0 fails, DISCHARGED**.
8. **Tests run — 7, all green, all named.** `_gauge_tokens.py --selftest` (rc=0);
   `_capture_gate.selftest_boot_delta_parse` (0 failures, now including the four new arms);
   `selftest_preflight_tokens`, `selftest_gauge_refusal_seam`, `selftest_bare_token`,
   `selftest_gauge_continuity`, `selftest_preflight` (0 each); `SELFTEST_REFUSALS` empty.
   `python3 -m py_compile` clean on all three modules; `import _checkin, _surface_recorder,
   _gauge_tokens` OK. ⛔ **The full `python3 knowledge/_capture_gate.py --selftest` was NOT run
   to completion** — it exceeds the sandbox call wall (>120 s, and a backgrounded run does not
   survive the call boundary). The six affected selftest functions were driven individually
   instead; that is the honest scope, and the remaining 26 arms are UNPROVEN by this lane.
9. **No dangling `BOOT_FIRSTTURN` name is left in CODE.** `grep -rn "BOOT_FIRSTTURN"
   --include=*.py` now returns only `_to_delete/_mutants/` (dead) — the live reference in
   `knowledge/_surface_recorder.py:212`'s `floor_note` string was re-pointed at
   `derived_boot_band()` / `BOOT_CEILING_TK`. Remaining hits are PROSE ABOUT HISTORY in `notes/`,
   `_DECISION-HISTORY/`, `_GM-ARCHIVE.md`, `knowledge/_DS-IMPROVEMENTS.md`, and in the record
   files `knowledge/_rulings.json`, `knowledge/_state.json`, `knowledge/_surface-samples.json`
   (historic `floor_note` values) — ratified record, deliberately not rewritten.

## RULING-SHAPED QUESTIONS

1. **`BOOT_BAND_SIGMA = 2.0` — the red line's multiplier.** `s240-D1` says "beyond the spread"
   without fixing a multiplier, and Finding 4 proves 1× cannot satisfy the ruling's own
   slow-drift clause. Options: **(a)** keep 2.0 — a linear ramp is green at any slope, a
   one-session step is red at any size, both selftested; **(b)** 1.5 — tighter, still passes a
   ramp (1.39σ) but with almost no margin, so ordinary noise on a ramp would go red; **(c)** put
   it back to 1.0 and accept a red-and-declare every wrap. **Recommend (a)**, because it is the
   only value shown to satisfy both halves of what Dave ruled. This is reported, not inscribed —
   no ruling was written by this lane.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** the other 26 arms of `python3 knowledge/_capture_gate.py --selftest`, and the
  gate's `--wrap` / `--build` paths end to end. Price to prove: one run that exceeds the ~178 s
  sandbox call wall — it needs a seat that can hold a long call, not more tokens.
- **UNPROVEN:** the **shrink-only** property of `BOOT_CEILING_TK` is enforced by REVIEW and by
  `git log -p` on that line, not in process — the previous value is not in the file, so there is
  nothing cheap for the code to compare against. Stated in the constant's own comment rather than
  pretended. Price to prove mechanically: a ratchet sidecar (the `_type_ratchet.json` shape),
  roughly one small lane.
- **CLAIMED:** #240's boot reading of **76,138**, used only to reproduce Dave's `± 641` in
  Finding 3, is read from `GOOD-MORNING.md:478` — it is not yet in `notes/_GAUGE-LOG.md` (it
  enters at this wrap's 2f roll).

## ⚠ CONSEQUENCES THE CONDUCTOR MUST PRICE

1. **The #241 wrap will go RED on `boot-drift` and will need a DECLARED line in the NEW form.**
   When #241's own boot (69,092) rolls into the gauge log it is a genuine step change off the
   pre-diet plateau — the gate is working, not broken. The line to write is the one in Finding 7,
   with the figures **copied from the gate's own failure text at that seat**, never from here:
   `> **boot-drift DECLARED #<N> (<YYYY-MM-DD>):** newest <R> · derived band <M> ±<S> (n=<n>,
   #<first>–#<last>) · delta <+/-D> · ceiling <C> · DERIVED at check time per `s240-D1`; NOT a
   re-base and no constant was edited.`
2. **`W-386` is still OPEN and its close is the conductor's act.** `knowledge/_state.py` has no
   close verb (`grep -n "argparse\|add_argument" knowledge/_state.py` → only a `--selftest`
   branch), and `s218-D7` puts store-row minting at the conductor's seat. Proposed payload:
   `state: "done"`, `closed_by: "#241 2026-09-02 - lane B: s240-D1/s240-D2/s241-D1 enacted in
   knowledge/_gauge_tokens.py (BOOT_FIRSTTURN_TK/_ERR deleted, derived_boot_band(),
   BOOT_CEILING_TK = 70_000) and knowledge/_capture_gate.py (boot-drift graded against the
   derived band + the ceiling, selftested red-on-step / green-on-drift / ceiling-by-name);
   report notes/_subreports/2026-09-02-241-lane-B-boot-band.md"`.
3. **The CLI now prints `⛔ OVER` beside the ceiling** (`python3 knowledge/_gauge_tokens.py`),
   because the derived mean is still the pre-diet 75,994. That is a DISPLAY reading of a real
   condition, not a gate failure — the gate does not grade pre-#241 readings against a post-diet
   ceiling (`BOOT_CEILING_FROM_SESSION = 241`, named in a note, never silently skipped). It will
   stop showing OVER once post-diet readings fill the window.
4. **`s208-D1`'s rider still binds and is NOT discharged by this lane:** a band that moves with
   the measurement is measurement honesty, never target acceptance. The boot-reduction work
   stays open.

## Evidence

No evidence files: every claim above quotes the command or the gate output that produced it, and
both mutation fixtures were built in `/dev/shm` and removed (`s218-D7` forbids scratch as
evidence, so nothing is claimed from them beyond the output pasted inline).

REPLAY-THESE: `knowledge/_gauge_tokens.py` lines ~178–265, the new band block (~1,800 tk) ·
`knowledge/_capture_gate.py::boot_constant_drift_check` + `_parse_boot_samples` (~3,000 tk)
