# #315 — rules every lane carries (conductor, Fri 2026-10-02 ~21:35 BST)

Apollo is Dave's governed design-system engine. The repo is the record. Dave rules from plain prose and pictures, never ID codes. Session #315 opened Fri 2026-10-02 21:27 BST; HEAD at the opener is `853d7f56` (CI GREEN, run 37055316112). Fable is paused this week: every lane runs on Opus 5.5. Dave's word for this session so far: *"go"* (21:29) to the plan in the opener: the templates' second-look page first, the whole-library audit and the cold runs G1–G3 + GV behind it.

## Where you work
- CLOUD = this container. A depth-1 clone of origin at `853d7f56` is at `/home/claude/apollo`. Never edit `/home/claude/apollo` itself. Make your own worktree: `git -C /home/claude/apollo worktree add --detach /home/claude/w-<lane> 853d7f56`.
- SEAT = Dave's Mac, through `mcp__remote-devices__device_bash` only (repo at `$HOME/mnt/Projects--UX-design`, never `UX-design--UX-design`). At most TWO lanes on the seat at once. `device_bash` defaults to a 120 s timeout; pass `timeout_ms` up to 178000. A lane touches the seat only where its brief says so.
- A CLOUD LANE NEVER COMMITS, never writes to the seat, never regenerates shared outputs (canon.css, `_rulings.json`, `_state.json`, chart receipts, `_RULINGS.html`, KG titles, the memento index), never runs the build survey. It hands back a PATCH: `git -C /home/claude/w-<lane> add -N <new files>; git -C /home/claude/w-<lane> diff --binary 853d7f56 > /home/claude/patches/<lane>.patch`. Source edits only; the committer runs the regen serial. Never hand back whole copies of shared files.
- Renders in the cloud: Chromium is at `/opt/pw-browsers` (Playwright finds it; never run `playwright install`). The repo's render runbook is `knowledge/_RUNBOOK-render-verify.md`. Renders that open a menu or field do it by CLICK, never by focus + key (Dave 14:55 2026-10-02, call 1: *"we never have a focus state unless the user is using keybord controls."*).

## Honesty rules
- Dave's words are QUOTED, never paraphrased. His #314 exports: `notes/_lanes/314/DAVE-RULINGS-2026-10-02-1455-borders-switch-templates.md`, chat lines `notes/_lanes/314/DAVE-WORDS-2026-10-02-chat-lines.md`. The rulings store is `knowledge/_rulings.json` (974, newest s314-D28). Open rows: `python3 knowledge/_state.py`.
- Check a page's or brief's word against the tree before repeating it. A grep that finds nothing is not proof of absence; a grep that matches is not proof of presence.
- Never invent a ruling or a close condition for Dave's open work. Where his answer leaves something open, write it as his open question in plain words. A recommendation is a recommendation, never a ruling.
- Do not read or write claude.ai Project memory.
- Never run `git status` at the seat (it locks). In the cloud worktree it is fine.
- Do not read `GOOD-MORNING.md` or `_LIVE-STATE.md` top to bottom; `python3 knowledge/_memento_search.py "<q>"` → `--fetch <id>` is retrieval.

## Hand-back
- Write your report INSIDE your patch at `notes/_subreports/2026-10-02-315-<lane>.md` (what changed, file by file; what you checked and how; what is left; Dave's open questions in plain words; a `CITES:` line with the ruling ids you obeyed; a `MODEL:` line naming the model you actually ran on).
- Your final message to the conductor is SHORT (under 250 words): what the patch holds (path, files), what you checked, failures stated flat, open questions for Dave in plain words, and exactly what the committer must run after applying.
- The user is not watching; proceed on reversible actions that follow from the brief; an end-of-turn promise is not a completion — do the work or flag the blocker.
