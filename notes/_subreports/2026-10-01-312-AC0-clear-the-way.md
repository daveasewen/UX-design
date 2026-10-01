# #312 lane AC0 — clear the way (Opus seat lane, the single committer)

COUNTS: rulings inscribed 7 (s312-D1..D7, store 858 → 865) · stamped enacted 3 (D1, D2 at 07b1eb01; D5 at inscription, by the 12:52 grant) · commits 2 (07b1eb01, f8eedc96) · push 97c7793a..f8eedc96 (carries d3be2c22) · index build 4.1 s at the seat, NO shrink · _CHAIN.md 8,305 → 6,199 cl100k (warn 7,700) · CI run 36862352553 GREEN: release ✅, gates ✅, render ✅

Thu 2026-10-01, ~12:55–13:45 BST, Opus 5.5, Dave's seat. Authority: Dave 12:35 "yes to both, I want our plan to run smoothly" (`notes/_lanes/311/DAVE-WORDS-2026-10-01-1235-index-and-chain.md`) and 12:51 "cool fix anything that might get in our way now." (`notes/_lanes/312/DAVE-RULINGS-2026-10-01-1251-wave-2-calls.md`, committed in 07b1eb01).

## 1 — Inscribed (lane R's method at 2fbc8184)
Entries at `notes/_lanes/312/AC0/s312-D{1..7}.entry.json`; each `--dry-run` passed the reconstruction proof, then `--write`; `gen_kg_titles.py --write` (865 titled, 0 untitled) and `_render_rulings.py` (865 rulings, 170 sessions) re-run and committed with them.

| id | ruled | status |
|---|---|---|
| s312-D1 | the memento index is built, never committed; opener + CI build; determinism = two fresh builds; shrink only if too slow; no LFS | enacted at 07b1eb01 (stamped in f8eedc96) |
| s312-D2 | the eleven older WRAP DATE SPLIT header lines go to the archive, one counting line stays | enacted at 07b1eb01 (stamped in f8eedc96) |
| s312-D3 | day's shape: his rulings and pictures today; A, B, C3, C4, D, G Friday | ruled |
| s312-D4 | cohort one = the five M2 sampled + ten interactive neighbours | ruled |
| s312-D5 | deletion allowed in the repo folder for the session; his comment quoted | enacted at inscription — the 12:52 grant; no sha exists for a grant (adds 1 to the s295-D2 ADVISORY count, honestly) |
| s312-D6 | phase 2 Saturday as a weekend run after he rules cohort one's trees Friday; "lets see where we get to, it maybe we'll get here earlier :)" | ruled |
| s312-D7 | Sutherland React from the four existing bindings, theme export when J lands; his Copilot-brief comment quoted | ruled — the brief for the agent on his work machine is OWED |

His D7 comment spans two lines in the export; `says` marks the break with " / ", `ruled` joins them with a space.

## 2 — The index (s312-D1)
- `git rm --cached knowledge/_memento-index.json`; `.gitignore` gains it with the ruling. History NOT rewritten, no LFS. The local copy stays on disk (53 MB) as a cache.
- `_build_memento_index.py --check`: builds twice in-process, compares sha256 of the two renders; a stale or absent local copy is REPORTED, not failed. Measured: 4.1 s, ~785 MB peak RSS.
- Opener: `knowledge/_render/ensure_env.sh` step 5 builds it; the OK line ends `index=built(<n> records,<ms>ms)` so the opener's `tail -1` shows it. Measured at the seat: `index=built(2376 records,4140ms)`, whole script 4.4 s. A refusal names itself on the OK line and does not fail the render env; `APOLLO_SKIP_INDEX=1` skips it. Fast enough — the shrink fallback was NOT taken.
- CI: `.github/workflows/gates.yml` gains "Build the Memento index" before the survey (the survey's `_gen_chain --check`, mention-map and schematic checks read it). Release and render jobs do not read it (release audit / frozen gate / pack / CI template / projections / build-script selftest all green in a clone without the file).
- `_wrap_regen.py`: the index step stays in the serial (later steps read it) but names no output to stage (git refuses an ignored path). `_capture_gate.index_freshness_check` keeps refusing a stale local copy at the wrap; its message now says built, never staged.
- Proven after a fresh build: `_memento_search.py "wrap date split"` and `--fetch gm-archive:header-lines-moved-2026-10-01-312-the-eleven-older-wrap-date` both answer.
- Not changed (carry): the packaged copies in `memento-package/` and `apollo-spider/gumdrop/` (their own index story); `_RUNBOOK-capture-ritual.md` step 2g prose still says to stage the index — the tools no longer do; the runbook line is owed a correction.

## 3 — The chain (s312-D2)
`_gm_move.py --ops notes/_lanes/312/AC0/chain-move-ops.json`: 11 lines moved VERBATIM to `_GM-ARCHIVE.md` under a new top section `## Header lines moved 2026-10-01 #312 — the eleven older WRAP DATE SPLIT lines (s312-D2)` — deliberately NOT a `## Batch … #312` heading, because `_wrap_ops.py` refuses an existing `## Batch <date> #312` when #312 wraps. One counting line now leads the header (it starts `> ⚠ **WRAP DATE SPLIT`, sits before #311's line, so `_wrap_ops` still inserts after #311's). `_gen_chain.py`: **6,199 cl100k** (was 8,305; warn 7,700, fail 10,000), 19,792 bytes. ⚠ `_gen_chain.py` needs `TIKTOKEN_CACHE_DIR=apollo-spider/gumdrop/_encoder-cache` when `TMPDIR=/dev/shm` (the default cache dir moves with TMPDIR and is empty).

## 4 — The commit script
`knowledge/_git_commit.sh`: the `git status --porcelain` count (old line 984) → `git ls-files -m -o --exclude-standard | wc -l`; `--all-dirty` and both refusal listings → `ls-files -m -o`; staging runs `git add` ONLY on a named path that changed (tracked and `git diff --quiet` says different, or untracked and not ignored) and prints `unchanged (not staged, no git add run)` otherwise. `clear_locks` mv-aside belt kept. `--selftest` 32 bites OK (seat and clone). Left alone: `git status --short` at lines 151 and 238 (`--declare-dirt` / push dirt) — their output feeds a parser of that exact format; a later pass can move them.

## 5 — The runbook
`knowledge/_RUNBOOK-parallel-conductor.md` § "THE SEAT — seven rules from the night of #311, and two facts measured at #312": the seven rules verbatim in substance, his 12:51 line as authority, the stage/commit-shares-the-queue fact (11:53 UTC) and the 99%-full seat home disk (use /dev/shm or /tmp; depth-1 clone for the pre-push survey).

## 6 — Commit, pre-push, push, CI
- 07b1eb01 (28 paths, incl. the index deletion; the commit gate regenerated the mention map once — re-run with it and the schematic named) · f8eedc96 (status stamps; 3 paths). Both first-class `_git_commit.sh` commits, SESSION_N=312.
- Pre-push on `git clone --depth 1 file://$PWD /tmp/ac0c` + the new CI step (index built). ⚠ A depth-1 clone FAILS the history-reading arms (`_governs` commit pointers, `_gen_chain`'s `git show 18c7789`), which are artefacts, not defects; fixed at zero disk by pointing the clone's `objects/info/alternates` at the mount's `.git/objects` and moving `.git/shallow` aside — full history visible, nothing copied. Worth adopting in the runbook.
  - Survey, committed tree, NO `--include-mutating` (ranges 1:60, 61:120, 121:170): **81 pass · 0 FAIL · 2 advisory (163, 164) · 4 could-not-ask** — the #311 baseline exactly.
  - Writer gates `--include-mutating` (1:40, 41:85, 86:125, 126:170): **154 pass · 0 FAIL · 4 advisory (140, 150, 163, 164) · 9 could-not-ask** — the #311 baseline exactly.
  - test_gates rc 0 · test_advisory 19 cases bite · commit-script selftest 32 OK · evidence gate PASS · release job's six commands rc 0.
  - Clone deleted after; /tmp back to 3.6 GB free.
- Push 12:31:34 UTC: `97c7793a..f8eedc96`, plain `git push origin master` after fast-forward check; `git ls-remote` = f8eedc96. No GitHub size warning.
- CI run 36862352553 on f8eedc96: **release ✅ (12:32:45Z) · gates ✅ (12:37:37Z)** · **render ✅ (12:46:23Z)** — `_ci_readback.py` VERDICT: GREEN, every run completed and passed.

## Found, not fixed
- `_GM-ARCHIVE.md` and `_LIVE-STATE-ARCHIVE.md` carry duplicate `## ` headings (the index warns on every build, 6 ids); pre-existing.
- `.git/objects` holds 2.42 GB of LOOSE objects (≈ the old index committed ~40 times) + 89 tmp_obj turds; a `git gc` would reclaim most of it — Dave's call, not done.
- `_capture_gate` / runbook step 2g prose: "stage the index" — the message is fixed in the gate; the runbook text is owed.
- The s312-D7 brief for the Copilot agent on his work machine is owed (lane N or the conductor).

## Files
`.gitignore` · `.github/workflows/gates.yml` · `knowledge/_build_memento_index.py` · `knowledge/_render/ensure_env.sh` · `knowledge/_capture_gate.py` · `knowledge/_wrap_regen.py` · `knowledge/_git_commit.sh` · `knowledge/_RUNBOOK-parallel-conductor.md` · `GOOD-MORNING.md` · `_GM-ARCHIVE.md` · `_CHAIN.md` · `knowledge/_rulings.json` · `knowledge/_node_titles.json` · `notes/_RULINGS.html` · `notes/_lanes/312/AC0/` · this report (UNCOMMITTED — for the next commit wave).
