# #309 lane E — the checks that weren't made: the work-around

COUNTS: gates made to run in full at the seat 2 of 2 (state-contrast 137 of 137 snippets, hit-area 137 of 137) · state-contrast merged audit byte-identical to CI's render-job artefact 1 of 1 (CI fonts) · gate CI paths changed 0 · chunked clone survey 167 of 167 steps asked: 155 pass · 0 FAIL · 3 ADVISORY-warn · 9 COULD-NOT-ASK · seat-only reds 0 · mount survey seat-only reds 3 ([11], [13], [127]) · lane C's miss re-driven 1 ([10] exit 1 on 528e8318) · pushed no

machinery: 0 instrument / 2 feature (state-contrast `--slice I/N OUT.json` + `--merge`; hit-area reads `$RENDER_SHELL` first)

Asked: the conductor, #309, on Dave's "I'm worried that the checks weren't made can we investigate, im sure we can find a work-around" (`notes/_lanes/309/DAVE-WORDS-2026-09-30-0707.md` item 3). Brief: `notes/_lanes/309/E/BRIEF.md`.

## The answer

Dave was right to worry, and the reason is one sentence: the survey counts any step whose arguments are not `--check`/`--selftest` as "mutating" and never asks it, so step [10] — the assertion gate that went red — is asked by nobody but `_build_all.py`, in CI, after the push. Neither CI's own survey step nor a seat survey asks it. The work-around that closes it is a throwaway clone of the committed tree on the VM's local disk, surveyed with `--include-mutating` in four chunks. It asks all 167 steps in about six minutes, cannot strand the real tree, and on the commit that went red it gives exactly CI's red.

## A1. The state-contrast gate

Why it failed at the seat: nothing was broken — the browser launches fine. One full run is serial: 137 snippets × two themes × every interactive element × hover and pressed. CI's render job took 13 min 2 s for it on 054aee4b (06:14:21 → 06:27:23). That never fits a 170 s call.

The fix: `--slice I/N OUT.json` sweeps every Nth snippet from the I-th and writes raw results only (no audit, not a verdict); `--merge OUT1.json …` refuses unless the slices cover every snippet exactly once, then goes through the same render, audit write and exit code as a full run. The default path is untouched: bare run and `--selftest` go through `parse_args` exactly as before (the selftest's `parse_args` arms still hold), so CI cannot see the change.

Cost at the seat: 8 slices, 4 in parallel per call (the seat has 4 cores): 140 s + 119 s ≈ 4.3 min.

The proof:
1. With the seat's fontconfig off (`unset FONTCONFIG_FILE`, so fallback fonts as in CI), the merged `_STATE-CONTRAST-AUDIT.md` is **byte-identical** to the audit CI's render job uploaded for 528e8318 (run 36637115402) — and CI's 054aee4b artefact (run 36677095831) is byte-identical to that one; no snippet or canon file differs between the two commits.
2. With the seat's real HSBC fonts, the verdict is the same (0 text failures across 137 snippets, 0 carrier failures, exit 0) but 79 declared holes, not 78: Alert's "Update contact details" link is not in the hit stack when laid out in HSBC. Driven on Alert alone: 2 holes with seat fonts, 1 without. A font fact, not a slicing fact.
3. Refusals driven: merge missing slice 8 → exit 2 naming the 17 absent snippets; slice 1 given twice → exit 2 naming Accordion. `--selftest` 62 arms OK at the seat in 6 s; `--bogus` still refused by name.

## A2. The hit-area gate

Why it failed at the seat: `_shell_path()` globs `chromium_headless_shell-*/chrome-linux/headless_shell`. The seat's playwright build (1243, arm64) lays the shell out as `chrome-headless-shell-linux-arm64/chrome-headless-shell`, so no glob matched and the gate refused 77 with the browser on disk.

The fix: `$RENDER_SHELL` first, when set and a file (`seat_env.sh` exports it only after asserting it resolves). CI never sets it. Driven with it unset: still 77 with the old words.

`--all` at the seat takes ~171 s, one call cannot hold it, so it runs as two halves of the sorted file list (positional paths, no new flag): 86 s + 85 s. Result: 3,357 targets measured, 1,046 findings, 1,084 exempt, over 137 snippets. ADVISORY, exit 0.

Two things found, not changed:
- The gate's own words say CI's `render` job "runs this BLOCKING". It does not — `gates.yml` never names it. Its only CI run is `_build_all.py` step [68] in the `gates` job, which has no playwright, so in CI it has refused 77 on every run.
- The committed `knowledge/_HIT-AREA-ADVISORY.md` is from 2026-08-19 (bd372c54) and covers 77 snippets; today's sweep covers 137.
- Also not changed: the committed `knowledge/_STATE-CONTRAST-AUDIT.md` at HEAD is a 3-snippet partial ("0 text failure(s) across 3 snippet(s)"; last touched ce2018da). CI regenerates it and does not commit it. Left alone — `_build_all.state_contrast_caveat()` reads it, and changing what it says is outside this lane.

## B. The whole blocking verdict before a push

Measured two ways, on HEAD 054aee4b.

**On the mount (the survey as lanes run it today, `--no-record`, `--timeout 60`, seat env sourced):** 87 of 167 steps asked, 80 never asked (called "mutating" — [10] among them). Four calls: 1:45 (not timed, under 165 s), 46:110 58 s, 111:140 137 s, 141:167 96 s. Reds, all seat-only:
- [11] `_validate_assertions.py --selftest` — the mount arm (`root=mount must reach outside the repo`); CI passes it. Already known (_HANDOFF-159).
- [13] `_capture_gate.py --selftest` — over 160 s at the seat. At the seat the gitignored inputs exist, so every arm runs; CI refuses 77 in seconds because 4 arms cannot read them.
- [127] `_gen_chain.py --selftest` — over 60 s on the mount; passes in CI.
Plus [163] advisory (itinerary register out of sync), which CI also shows.

**In a throwaway clone (the work-around):** `git clone -q --shared --no-checkout <mount> /tmp/e309/wt && git checkout -q HEAD` — 23 s, 1.3 GB on the VM's local disk (2.5 GB free; `/tmp` persists between calls, `/dev/shm` does not; `$HOME`'s disk is 99% full). No seat env, so it mirrors CI's `gates` job. `--include-mutating --no-record --timeout 60`, `--resume` from the second chunk on:
- chunks as run: 1:30 151 s · 31:55 15 s · 56:110 22 s · 111:167 160 s = 5.8 min. Two were near the wall, so per-step times were taken: steps 2–4 cost ~95 s, [13] 34 s, [16] 11 s, [30] 18 s, [132]–[134] 33 s, [140] 18 s, [143]–[146] 43 s. Balanced chunks: **1:12 (~97 s) · 13:55 (~80 s) · 56:140 (~95 s) · 141:167 (~95 s)**.
- result: 155 pass · 0 FAIL · 3 ADVISORY-warn ([140], [150], [163]) · 9 COULD-NOT-ASK ([10], [13], [61], [68], [73], [74], [142], [153], [154]) — the same refusal families CI shows. **Zero seat-only reds.**
- CI's steps after the build, in the clone: `_tests/test_gates.py` 14 s (32 tests, 0 failures; needs `TMPDIR=/tmp/e309/tmp`, the default TMPDIR disk is full), `_tests/test_advisory.py` 1 s, `_git_commit.sh --selftest` 0 s, `_validate_evidence.py notes/_claims` 16 s.
- **It catches lane C's miss:** clone checked out at 528e8318, `--include-mutating --range 10:10` → `❌ [10] assertion veracity gate — exit 1`, the exact red CI gave.
- Caveat: the regeneration leaves 42 derived files differing from what is committed (ASSERT-007 shows ⊘ in a clone, staleness lines, list ordering), so the clone's diff is noise and is not a "forgot the regen" detector. The survey verdict is the signal.

Why this is safe: `_build_all.py` is never run; nothing in the real tree is written; the survey's own `git status` runs in the clone on local disk, not on the mount.

## C. The routine to recommend (draft — the conductor's and Dave's call where it goes)

Suggested home: the Worker checklist in `knowledge/_RUNBOOK-parallel-conductor.md`, with one line in the build brief template pointing at it.

> **Before the conductor pushes a lane's work, the lane surveys its own commit in a clone.** Commit through `_git_commit.sh` as usual, then, one call each: (1) `rm -rf /tmp/pp && git clone -q --shared --no-checkout "$PWD" /tmp/pp && git -C /tmp/pp checkout -q HEAD` (about 25 s); (2)–(5) in `/tmp/pp`, `python3 -u knowledge/_build_survey.py --include-mutating --no-record --timeout 60 --range 1:12`, then `13:55`, `56:140`, `141:167`, adding `--resume` from the second on (about 90 s each). Any ❌ or ⏱ is a red CI will also give — fix it, commit, and survey again; ⊘ and ⚠ match CI and do not block. (6) Still in the clone, `TMPDIR=/tmp/pp-tmp python3 knowledge/_tests/test_gates.py` and `python3 knowledge/_validate_evidence.py notes/_claims` (about 30 s). If the lane touched a snippet or `canon.css`, also run the state-contrast sweep at the seat in two calls, four slices at a time — `--slice 1/8 … 4/8`, then `5/8 … 8/8`, then `--merge` — and restore `_STATE-CONTRAST-AUDIT.md` from HEAD afterwards unless the audit is meant to change (about 4.5 min). Whole routine: about 7 minutes and six calls, about 12 minutes and eight with the sweep. Delete `/tmp/pp` when done. Do not run the survey on the mount for this: it never asks the writer gates, and three of its selftests go red there for seat reasons.

## Commits

This report and the two gate changes: see the commit that carries this file. Nothing pushed.
