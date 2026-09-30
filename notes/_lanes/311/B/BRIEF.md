# Lane B — #311 — build s311-D1 (dark icons follow the ink) and s311-D2 (Supercharge dark page and section warm/4), then a short look page

Conductor: #311, Opus 5.5, cloud seat linked to Dave's Mac. You are an Opus 5.5 build lane. You build, measure, render, and hand back ONE short look page. You do NOT push.

## Read first
- Dave's export, verbatim: `notes/_lanes/311/DAVE-RULINGS-2026-09-30-2030-soft-white-and-tab-strip-built.md`. The two rulings: `notes/_lanes/311/s311-D1.entry.json`, `notes/_lanes/311/s311-D2.entry.json` (inscribed at `84bd8c93`). Quote; never paraphrase.
- Lane A's report and drivers (reuse them): `notes/_subreports/2026-09-30-311-A-soft-white-and-tab-strip.md`, `notes/_lanes/311/A/`. Page shell to copy (NEW localStorage key and path): `notes/_REVIEW-311-A-soft-white-and-tab-strip-2026-09-30-v1.html`.

## Job 1 — s311-D1, the icons follow the ink
In dark, wherever s310-D7 softened text to #E1E1E1 (Mono, Console, Common), icons drawn in pure white follow it (the header search glass, for one); Supercharge's follow its #F7F6F4. Build at the token source + generator, never by hand in canon.css; regenerate in the ordered serial. Scope is icons that were pure white as ink; do NOT move icons that carry a status or brand colour. Count pure-white icon elements on the banking demo in dark before and after (target 0 in the three themes). Lane A's found-not-fixed list names other things bound to the text ink (QR modules, rating star, etc.) — leave those as they are.

## Job 2 — s311-D2, Supercharge's dark page and section take warm/4 #25211C
Fix at the source: the theme cascade generator locks `background/default` after its light half (lane A's report names the function); Supercharge dark page and `surface/section` → warm/4 #25211C, tile stays #13110E. Update the digital-black token's stale note lane A named. Check nothing else in Mono/Console/Common/Legacy moves (diff canon.css per theme and state it). Measure tile-vs-page and tile-vs-section contrast.

## Job 3 — the look page
`notes/_REVIEW-311-B-icons-and-supercharge-page-2026-09-30-v1.html`. 01 The icons: banking demo top, dark, Console, before/after, plus one 4x crop of the header icons next to text; one line for Mono and Common. 02 Supercharge's dark page: a real Supercharge dark page with tiles on the page ground and on a section background, before/after (built, not scratch). Each section one call, "Does it stand?" — Yes, it stands / Change it (comment). Plain prose first, machinery in a Technical fold. Pictures inline `<img>` only, under `notes/_lanes/311/B/img/`, ≤10 pictures. Verify at 1440 and 390: no broken images, no side scroll, Copy as text returns every call.

## Checks, report
- Do NOT stamp s311-D1/D2 enacted — the conductor does it after Dave looks.
- Pre-push check (s309-D7, Worker checklist step 5 of `knowledge/_RUNBOOK-parallel-conductor.md`) on your commits in a /tmp clone: four chunks with `--include-mutating`, tests, evidence; the state-contrast sweep in slices (you touch canon); chart receipts via `outputs/310/A/drive_wrap.py` if canon changed. Steps 68 and 73 time out in the survey at this seat; run them on their own as lane A did. Fix any ❌ you caused.
- Report at `notes/_subreports/2026-09-30-311-B-icons-and-supercharge-page.md` (COUNTS line first).

## Seat mechanics (hard rules — `notes/_lanes/310/A/BRIEF.md` § Seat mechanics; read it)
Everything via `mcp__remote-devices__device_bash` at `$HOME/mnt/Projects--UX-design`, `timeout_ms` ≤178000; renders `export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh`, `executable_path=os.environ["RENDER_SHELL"]`, `goto("file://…")`; Supercharge's dark block out-specifies a plain `[data-theme="dark"]` override. Commits only `SESSION_N=311 bash knowledge/_git_commit.sh --reconciled --quiet <fresh msgfile, line 1 WITHOUT a "#311 date —" prefix> <paths>` (if it regenerates the Memento schematic, re-run with that path appended), msgfile ending `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` and `Claude-Session: https://claude.ai/code/session_016YhJYsAg5HUtsmKLoZMtxZ`; never `git status`; `python3 knowledge/_wrap_commit.py unlock --tag 311-B` after every gate run; no `rm`; no push; no Project memory. Budget ~75 minutes.

## Hand back
Plain prose, short: what is on the page, the counts, the commits, the pre-push verdict, the page path, found-not-fixed.
