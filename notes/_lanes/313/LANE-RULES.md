# #313 — rules every lane carries (conductor, Thu 2026-10-01 ~18:00 BST)

Apollo is Dave's governed design-system engine. The repo is the record. Dave rules from plain prose and pictures, never ID codes.

## Where you work
- SEAT = Dave's Mac, reached only through `mcp__remote-devices__device_bash` (repo at `$HOME/mnt/Projects--UX-design`). At most TWO lanes on the seat at once; one of them is the single committer. The seat takes one command at a time: never ask it for anything a cloud shell can do.
- CLOUD = this container. A depth-1 clone of origin at `e5e0f355` is at `/home/claude/apollo`. A cloud lane makes its OWN worktree copy (`cp -a /home/claude/apollo /home/claude/w-<lane>` or `git worktree`-free copy) and never edits `/home/claude/apollo` itself.
- A CLOUD LANE NEVER COMMITS, never writes to the seat, never regenerates shared outputs, never runs the survey on the mount. It hands back a PATCH: `git -C /home/claude/w-<lane> diff --binary e5e0f355 > /home/claude/patches/<lane>.patch` (plus new files via `git add -N` first so they appear in the diff). The committer applies it with `git apply --3way` and refuses on conflict. Never hand back whole copies of shared files — three times at #312 a whole-file hand-back put back lines other lanes had committed.

## Seat rules (knowledge/_RUNBOOK-parallel-conductor.md § THE SEAT)
- NEVER run `git status` (it locks). Read git with `git diff --quiet`, `git diff-index --quiet HEAD`, `git ls-files -m -o`, `git log`, `git rev-parse`.
- Commits only via `knowledge/_git_commit.sh`. Commit msgfile line 1 carries NO `#<n> date —` prefix; non-wrap commits need `SESSION_N=313`. A commit runs alone in its call under `timeout 165`, output to a log, then grep it; pass `timeout_ms` up to 178000 to device_bash (default is 120 s).
- Before each commit: check for `*.lock` under `.git` (outside `_stale-locks/`); if no git process runs (`pgrep -a git`), move it into `.git/_stale-locks/`. Deletion is granted in the repo folder for this session.
- After every gate run: `python3 knowledge/_wrap_commit.py unlock --tag 313-<lane>`.
- Never commit `knowledge/_state.json` whole from a non-committer lane: name rows.
- An inscription is not done until `python3 knowledge/gen_kg_titles.py --write` and `python3 knowledge/_render_rulings.py` run and commit with it.
- Scratch at the seat goes to `TMPDIR=/dev/shm` or `/tmp`; never under `$HOME` outside `mnt/` (seat home is 99% full).
- The pre-push survey runs in a `git clone --depth 1 file://$PWD /tmp/<x>` clone (alternates at the mount's objects, `.git/shallow` moved aside, per the Worker checklist step 5): committed tree FIRST without `--include-mutating`, then the mutating pass; restore `notes/_BUILD-VERDICT-LOG.jsonl` between ranged chunks; delete the clone after.
- "Service Unavailable: server draining" = wait a minute and resend the same call.
- Renders: one bash call — `export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh; python3 <driver>` with `executable_path=$RENDER_SHELL`.

## Honesty rules
- Dave's words are QUOTED, never paraphrased. His two exports tonight are at `notes/_lanes/313/DAVE-RULINGS-2026-10-01-1752-cohort-one-trees-complete.md` and `notes/_lanes/313/DAVE-RULINGS-2026-10-01-1749-pictures-you-are-owed.md` (also in the cloud at `/mnt/user-data/outputs/313/`).
- Check a plan page's word against the tree before repeating it (#312: "the four Sutherland bindings" were June TODO placeholders).
- Never invent a ruling or a close condition for Dave's open work. Where his answer leaves something open, file it as his open question.
- Do not read or write Project memory.

## Hand-back
- File your report at `notes/_subreports/2026-10-01-313-<lane>.md` (cloud lanes: write it inside your patch).
- Your final message to the conductor is SHORT (under 200 words): what landed / what the patch holds, shas if any, failures stated flat, open questions for Dave in plain words.
