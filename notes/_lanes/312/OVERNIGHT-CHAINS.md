# The overnight run — three chain conductors under the #311 conductor (Wed 2026-09-30 22:05 BST → Thu 2026-10-01)

Dave, verbatim, 22:05 BST: "cool lets do it. lets get the lanes running over night" — his yes to `notes/_PLAN-311-thursday-burn-2026-10-01-v1.html` (the proposed order stands; no job was declined).
The #311 conductor's challenge, accepted by that yes: one conductor cannot read 48 lane reports, so three chain conductors each run their jobs and hand back one short report.

## Session numbering
This runs INSIDE session #311, overnight. Wherever a job brief says #312 or `SESSION_N=312`, read #311 / `SESSION_N=311`. Keep the brief paths `notes/_lanes/312/<job>/`. Report stems use the day the lane writes them (`2026-10-01-311-<job><n>-...`).

## The chains (run in parallel; jobs inside a chain in this order)
- CHAIN 1 — jobs A, then B, then G. Owns `knowledge/canon/canon.css`, the chart receipts, the snippet sources, `notes/_lanes/312/A|B|G`. Job A's commit seat (AC) commits for A and B, as the brief says. G builds its candidate at this chain's last clean HEAD (the survey green in the clone), not a pushed sha.
- CHAIN 2 — job C, then job D. Owns the metas and `meta.schema.json`, `apollo-launchpad/`, the edge register files, `notes/_lanes/312/C|D`. C's schema lane runs first; D's consumers lane only after C's schema commit.
- CHAIN 3 — jobs E, F and H, in parallel inside the chain. Owns `knowledge/_wrap_*.py` (E), its review page (F, renders read-only against canon), and H's cloud-only research page.

## Shared files: ONE SEAT-WIDE LOCK
`knowledge/_rulings.json`, `knowledge/_state.json`, every generated file the commit script regenerates (`_CHAIN.md`, `_node_titles.json`, `notes/_RULINGS.html`, the Memento schematic) and git itself are shared by all three chains. Any write to the store, any `_inscribe_ruling.py` run, and EVERY `_git_commit.sh` run happens inside the lock:
`until mkdir /tmp/apollo-commit.lock 2>/dev/null; do sleep 15; done` … work … `rmdir /tmp/apollo-commit.lock`
If a call would outlast 178 s, take the lock in one call, do the work in the next, release it in a third; never leave it held when a lane hands back. A lock older than 30 minutes (`stat`) is stale: say so in the report, then remove it.
A chain that needs a file another chain owns does not edit it; it names the need under `## Found, not fixed`.

## Pre-push clones: ONE AT A TIME
The seat's root disk has about 3.7G free; a /tmp clone is about 1.3G. Take `mkdir /tmp/apollo-prepush.lock` before cloning, and remove your OWN clone with `rm -rf /tmp/<your clone>` as soon as the survey is read, then `rmdir` the lock. That `rm` is allowed because it is outside the mount; `rm` inside the mount stays banned. Never write big files into the seat home (`/sessions` is 99% full).

## Hard rules (every lane)
Everything else in each job brief's § Hard rules stands: `mcp__remote-devices__device_bash` at `$HOME/mnt/Projects--UX-design`, `timeout_ms` ≤178000; renders via `ensure_env.sh` + `seat_env.sh`, `executable_path=$RENDER_SHELL`, `goto("file://…")`; commits only via `SESSION_N=311 bash knowledge/_git_commit.sh --reconciled --quiet <fresh msgfile, no "#311 date —" prefix> <paths>` (re-run with the Memento schematic appended if it regenerates it), msgfile ending `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` and `Claude-Session: https://claude.ai/code/session_016YhJYsAg5HUtsmKLoZMtxZ`; never `git status`; `python3 knowledge/_wrap_commit.py unlock --tag 311-<job>` after gate runs; an inscription is not done until `gen_kg_titles.py --write` and `_render_rulings.py` run and commit with it; NO PUSH (the #311 conductor pushes after a survey on the combined HEAD); no claude.ai Project memory. No new ruling is inscribed without Dave's words: build what is ruled, put what needs him on a review page.

## Hand back (chain conductor → #311 conductor)
At most 300 words: per job, what was built (rulings stamped enacted, rows closed), the commit shas, the survey verdict on the chain's last commit, the review page path(s) for Dave, and found-not-fixed. Every lane files its own report at `notes/_subreports/`; the chain conductor files one chain report at `notes/_subreports/2026-10-01-311-chain<n>.md`.

---

## ADDENDUM 22:20 BST — the chains could not launch; WAVE 1 IS LAUNCHED FLAT BY THE #311 CONDUCTOR

The three chain conductors had no Agent tool (a sub-agent cannot spawn lanes); their reports are `notes/_subreports/2026-10-01-311-chain{1,2,3}.md`. So the #311 conductor launches lanes directly, in waves. Everything above stands, amended here:

1. **Wave 1 tonight (12 lanes):** A1 · A7 · B5 · C0 · CS · D1–D3 (one Opus lane, in that order) · E0 · F1 · F2 · H1 · H2. The rest (A2–A6, B1–B4, B6, B7, BV, C1–C4, CV, D4, D5, DV, E1–E3, EV, F3–F5, G, H3, AV) is wave 2+, launched later on these lanes' commits.
2. **Every lane is its own committer tonight** (there is no AC seat in wave 1): commit only your own named paths, inside the seat-wide commit lock. Rows into `knowledge/_state.json` and any `_inscribe_ruling.py --set-status` also only inside the lock.
3. **canon.css is regenerated by A1 ONLY tonight.** Any other lane whose change would need a canon regen stops before the regen and reports. **The metas and `meta.schema.json` are C0's ONLY tonight.** The edge register files are the D1–D3 lane's only.
4. **No per-lane full pre-push survey tonight** (one clone at a time would serialise twelve lanes for hours). Each lane runs, at the seat, the gates its own change touches plus `test_gates`, and names them in its report. The full survey runs ONCE on the combined HEAD before the #311 conductor pushes.
5. A lane whose input is not yet committed (another lane's work) stops and says so — it never builds on another lane's uncommitted files.
6. Hand back to the #311 conductor in AT MOST 100 words: built (ids), commit shas, gates run, report path, the one thing that needs Dave. Everything else goes in your filed report.
