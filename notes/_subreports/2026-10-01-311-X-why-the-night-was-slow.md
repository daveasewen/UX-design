# #311 lane X (Fable) · why the night was slow · diagnosis, 2026-10-01

COUNTS: seat calls read `2182` (conductor + 30 lanes, 30 Sep 18:23 → 1 Oct 04:44 UTC) · cut by the wall `143` (128 at ≤100 s run time; wall 178.7–182 s in 142 of 143) · never ran `38` · cloud "server draining" `21` · `_git_commit.sh` runs `147`, landed `23`, cut mid-run `41`, "could not stage" `14` · seat test calls `7` (N=1, 2, 4), cut `0` · lock probe rows `20` + `3` control · stranded locks on record `948` (377 `_orphan-locks`, 561 `_to_delete/_stale_locks`, 10 `.git/_stale-locks`) · rulings inscribed `0` · product files touched `0` · push `no` · Project memory `no`.

Headline: both faults are proven. (1) The seat runs one command at a time and a call's 180 s clock starts when it joins the queue; twelve lanes meant about two minutes of queue before every command, so "cut at 4–100 s" is the remainder of the clock after waiting (run time + wait = 180 s in all 143 cut calls). (2) The mount refuses `unlink`, and git releases an unused lock by unlinking it, so every no-op git command strands a lock and every landed commit strands `HEAD.lock` + `objects/maintenance.lock`; this has been true since #263 (948 moved-aside locks), twelve lanes only made the collisions fatal.

Page: `notes/_REVIEW-311-X-why-the-night-was-slow-2026-10-01-v1.html` (four calls; recommendations first, marked). Data: `notes/_lanes/311/X/` — `calls.json` (every call: agent, start, end, wall, timeout asked, cut ms, error class, lanes in flight), `bins.json`, `by_concurrency.json`, `extract.py`, `seat-test.txt`, `lock-probe.txt`.

## Fault 1 — the cut calls · PROVEN

- Server wording, 38 results: "device_bash did not run: this call waited (behind another command for the same session, or for the workspace) until its time ran out. Nothing was executed."
- Arithmetic: cut calls report "timed out after N ms" with N from 1,080 to 178,000 while their wall time is 178.7–182 s; `timeout_ms` asked for (20,000–178,000 or none) made no difference. Wait = 180 − N.
- By lanes in flight: ≤3 lanes 539 calls, 1 cut (a genuine 178 s run), median 0.7 s · 4–9 lanes 267 calls, 12 cut, 8 never ran, median 71 s · 11–12 lanes 1,129 calls, 128 cut, 30 never ran, median 114 s. Control: #311 A/B and the #310 wrap seat alone or in pairs 18:24–20:55, 280 calls, 1 cut, median 0.8 s.
- Seat test 07:09–07:20 UTC (alone): N=1 ran 150 s; N=2 ran strictly in series, both full, the second 301 s after submission; N=4 × 40 s strictly serial, none cut. From one agent the client serialises and the clock starts at execution; from many agents the server queues and the clock starts at submission. N=8 not run (cannot reproduce the multi-agent queue from one agent; said so on the page).
- Cost: ~44 lane-hours in flight beyond the solo norm while ≥4 lanes called, against at most 6.5 h of actual seat execution. Commit runs need 81–165 s uncontended (median 87); H1 held the commit mutex 22:10–01:26 over nineteen attempts.
- Fix (the recommendation): cap the seat at two lanes at once, one of them the single committer; text lanes (8 of last night's 12) work in the cloud, moving files with `device_stage_files` / `device_commit_files`. Untested and owed to the conductor: whether those two tools share the bash queue; whether a second linked session gets its own slot.

## Fault 2 — the lock · PROVEN

- Probe on the mount (`outputs/311/X/lockrepo`): leaks — no-op `git add`, `git add --dry-run`, `git status`, `git update-index --refresh`, empty `git commit`, clean `git reset -q` (HEAD.lock + branch lock), `git stash`; every landed `git commit` leaves `HEAD.lock` + `objects/maintenance.lock`. Clean — `git diff --quiet`, `diff --cached`, `diff-index`, `ls-files`, `log`, `rev-parse`. `GIT_INDEX_FILE` outside the mount stops only `index.lock`. Same commands in `/tmp`: nothing. Full table in `lock-probe.txt`.
- `_git_commit.sh`: `clear_locks` (mv-aside) at five points and `grep -v 'unable to unlink'` on the commit line already acknowledge the fault; but line 981 bare-adds every named path (no-op when unchanged) and line 984 runs `git status --porcelain` (leaks); between `clear_locks` and `git add` another lane's lock is a fatal "File exists" — 14 "could not stage" overnight, 11 "Unable to create index.lock". The bridge note's `git reset -q` advice leaks two locks itself.
- Fix (the recommendation): `device_request_delete_permission` on the repo root at every opener (one click), so git's own unlink works; keep the mv-aside as the belt. Cost: `rm` inside the mount becomes possible for the session, permanent. Alternative on the page: a git wrapper (mv-aside around every call, no-op forms refused, lock-free reads). Rejected by measurement: `GIT_INDEX_FILE`.

## What else the night taught — seven runbook rules (on the page, section 04)

No Agent tool ⇒ worker, hand back · survey the committed tree without `--include-mutating` first ([118] rebuilt the memento index before [119] checked it; CI red on 69848bbe, fixed efd0e89f) · ≤2 lanes at the seat · the commit mutex is one empty directory with a 30-minute stale rule · never commit `_state.json` whole from a lane · lock-free git reads only · "server draining" = cloud restart, resend.

## Found, not fixed

1. `_git_commit.sh:984` `git status --porcelain` and `:981` bare `git add` are lock leaks inside the script that bans `git status`.
2. `objects/*/tmp_obj_*` turds accumulate on every add at the seat (harmless, unbounded).
3. The seat home `/sessions` is near full; `TMPDIR=/dev/shm` was needed for the render.

## Commit

See the handback for the sha. Paths: the page, `notes/_lanes/311/X/*`, this report. `SESSION_N=311 bash knowledge/_git_commit.sh --reconciled --quiet`.
