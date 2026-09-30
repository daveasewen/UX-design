# Lane P — #311 — THE THURSDAY BURN PLAN: chunky multi-agent jobs for Thu 2026-10-01, from the whole backlog and the future-state notes

Conductor: #311, Opus 5.5, cloud seat linked to Dave's Mac. You are a Fable planning lane. You READ and PLAN; you build nothing except one plan page. You do NOT push.

## His ask, verbatim (chat, Wed 2026-09-30 21:30 BST)
"We have a lot of tokens to burn tomorrow, I want a plan with some chunky multi agent jobs, you can use fable as much as you like. take a look at the whole backlog and anything from notes and future state to see if we can string together a set of tasks that need lots of fuel."
His usage panel at 21:30: this week (all models) 64% used; Fable this week 24% used; both reset Thursday 23:00. So tomorrow roughly 36% of the weekly all-models budget and 76% of the Fable budget are use-it-or-lose-it by 23:00 Thursday.

## Survey (breadth first; cite a path or id for every item — never invent backlog)
1. The store: `python3 knowledge/_state.py` (548 live: 274 his, 274 mine) — group, don't list.
2. `_CARRIES.md` § residual → #311 (`python3 knowledge/_memento_search.py --fetch carries:residual-311`), and the OWED lists of `_HANDOFF-150`…`_HANDOFF-161` (plus #311's own finds: `notes/_subreports/2026-09-30-311-A-*.md`, `-311-B-*.md` found-not-fixed).
3. The queue and worklist: `gm:C1` strands, `gm:C2` ruling batch, `gm:C4` enact-queue, `gm:DOFIRST` (via `_memento_search.py --fetch`).
4. Future state in notes/ and reviews/: the roadmap (`notes/_PLAN-304-roadmap-and-weekend-runs-2026-09-26-v1.html`), Apollo-MCP proposal v2 (`notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html`) and its ruling (route B at #305), the KG gaps proposal (#269), research pages (#308), parked ideas and anything marked future/later/parked/idea (Jev/TypeSafe, permutation matrix, Apollo Assembly/Studio modes, Launchpad/Gen-UI, notice board for seats, the designer pack re-cut `s309-D4`, container types W-308iw, photography assets mapping, the live radius tuner, dream pass). Use `_memento_search.py` with the record's own vocabulary before concluding something is absent.
5. MODEL-ROUTING.md at repo root for which model does what.
You may fan out to Fable or Opus sub-agents for the reading. Do NOT read or write claude.ai Project memory.

## What makes a job fit for tomorrow
- Big: many parallel lanes, hours of fuel, Fable where judgment/design/research pays, Opus for builds, Sonnet for throughput sweeps.
- Mostly unattended: Dave may be at client work; name the ONE moment each job needs his word, and prefer jobs whose only Dave-moment is a review page at the end.
- Real: advances ruled work or future state he has asked for; no make-work, no re-deriving settled rulings, no reopening what he closed.
- Safe at the seat: one Mac seat. Root disk is 9.6G with ~3.7G free; a /tmp repo clone is ~1.3G, so at most two pre-push clones at once, and lanes must clear their own clones. Renders run at the seat (`ensure_env.sh`). Lanes that only read/write text or research can run from the cloud workspace. Commits only via `knowledge/_git_commit.sh`; lanes never push; the conductor pushes with a CI read-back. The conductor's window stops at 300,000, so the conductor must stay thin — lanes carry the fuel.
- Collision-free: jobs running at once must not touch the same files (canon.css, _rulings.json, _state.json are single-writer — say who owns each).

## The page
`notes/_PLAN-311-thursday-burn-2026-10-01-v1.html`, the review-page shell (copy `notes/_REVIEW-311-B-icons-and-supercharge-page-2026-09-30-v1.html`: styles, back link `../index.html`, Copy-as-text bar; NEW localStorage key). Plain prose first, machinery in Technical folds, dave-voice (answer first, short landmarked chunks, one idea per chunk).
- 01 The day on one screen: a small timeline of waves (morning launch, midday, evening) with which jobs run in parallel and rough fuel per job (Fable vs other), and a total against 76% Fable / 36% all-models. Say plainly these are estimates, and how you estimated (e.g. #310/#311 lanes: ~300-650k sub tokens each).
- 02 The jobs, 5 to 8 of them, ranked. Each: what it is in one line, why now (cite the backlog/notes source), lanes × model, what Dave gets back, his one moment, risk. Each is a call: "Run it tomorrow" / "Not tomorrow" (comment).
- 03 What I left out and why (short).
- 04 One call: the running order, with your recommendation first marked "(the recommendation)".
Pictures only if they earn it (inline SVG timeline is fine). Verify at 1440 and 390: no side scroll, Copy as text returns every call. Commit with `SESSION_N=311 bash knowledge/_git_commit.sh --reconciled --quiet <fresh msgfile, line 1 WITHOUT a "#311 date —" prefix> <paths>` (re-run with the Memento schematic appended if it regenerates it), msgfile ending `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` and `Claude-Session: https://claude.ai/code/session_016YhJYsAg5HUtsmKLoZMtxZ`; never `git status`; `python3 knowledge/_wrap_commit.py unlock --tag 311-P` after gate runs; no `rm` in the mount; no push. Also write each job's draft lane brief to `notes/_lanes/312/<job-letter>/BRIEF.md` so tomorrow's conductor can launch on his yes without re-reading the backlog.

## Seat mechanics
Everything via `mcp__remote-devices__device_bash` at `$HOME/mnt/Projects--UX-design`, `timeout_ms` ≤178000.

## Hand back
Plain prose, short: the jobs in rank order (one line each with lanes × model and fuel), the page path, the commit sha, and anything you found that Dave should know before he sleeps.
