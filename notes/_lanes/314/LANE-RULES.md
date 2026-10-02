# #314 — rules every lane carries (conductor, Fri 2026-10-02 ~12:10 BST)

Apollo is Dave's governed design-system engine. The repo is the record. Dave rules from plain prose and pictures, never ID codes. Session #314 opened Fri 2026-10-02; HEAD at the opener is `8d8e91dad1ddf20803e2b0b1fd148f0bed36b9f2` (CI GREEN). Dave's opener ask: use Fable well this week. His "go for it" (12:06) approved three Fable jobs (twelve templates rebuilt as valid elements; the cold-run verdict; a whole-library audit against his rulings) and Opus for the rest, borders first.

## Where you work
- CLOUD = this container. A depth-1 clone of origin at `8d8e91da` is at `/home/claude/apollo`. Never edit `/home/claude/apollo` itself. Make your own worktree: `git -C /home/claude/apollo worktree add --detach /home/claude/w-<lane> 8d8e91da`.
- SEAT = Dave's Mac, through `mcp__remote-devices__device_bash` only (repo at `$HOME/mnt/Projects--UX-design`, never `UX-design--UX-design`). At most TWO lanes on the seat at once, one of them the single committer. Cloud lanes do NOT touch the seat unless their brief says they may (read-only renders only, and only if the brief allows).
- A CLOUD LANE NEVER COMMITS, never writes to the seat, never regenerates shared outputs (canon.css, `_rulings.json`, `_state.json`, chart receipts, `_RULINGS.html`, KG titles, the memento index), never runs the build survey. It hands back a PATCH: `git -C /home/claude/w-<lane> add -N <new files>; git -C /home/claude/w-<lane> diff --binary 8d8e91da > /home/claude/patches/<lane>.patch`. Source edits only (snippets, metas, generators, notes); the committer runs the regen serial. Never hand back whole copies of shared files.
- If your work genuinely needs a regenerated output to be checked, say which generator and what you expect; the committer runs it.

## Honesty rules
- Dave's words are QUOTED, never paraphrased. His #313 exports: `notes/_lanes/313/DAVE-RULINGS-2026-10-01-*.md`, chat lines `notes/_lanes/313/DAVE-WORDS-2026-10-01-chat-lines.md`. The rulings store is `knowledge/_rulings.json` (946, newest s313-D81). Open rows are in `knowledge/_state.json` (`python3 knowledge/_state.py`).
- Check a page's or brief's word against the tree before repeating it. A grep that finds nothing is not proof of absence; a grep that matches is not proof of presence.
- Never invent a ruling or a close condition for Dave's open work. Where his answer leaves something open, write it as his open question in plain words.
- When a brief lists examples, his word does not spread past what he named without saying so: if you find more surfaces than he named, list them and say which you changed and why.
- Do not read or write claude.ai Project memory.
- Never run `git status` at the seat (it locks). In the cloud worktree it is fine.

## Hand-back
- Write your report INSIDE your patch at `notes/_subreports/2026-10-02-314-<lane>.md` (what changed, file by file; what you checked and how; what is left; Dave's open questions in plain words; a `CITES:` line with the ruling ids you obeyed; a `MODEL:` line naming the model you actually ran on, if you can tell).
- Your final message to the conductor is SHORT (under 250 words): what the patch holds (path, files, line counts), what you checked, failures stated flat, open questions for Dave in plain words, and exactly what the committer must run after applying (generators, renders).

## WAVE 2 (from 15:50 BST) — base sha changed
- HEAD is now `3c717370` (pushed, CI GREEN). The cloud clone `/home/claude/apollo` is checked out at `3c717370`. Wave-2 lanes cut their worktree and their patch against `3c717370`, never `8d8e91da`: `git -C /home/claude/apollo worktree add --detach /home/claude/w-<lane> 3c717370` and `git -C /home/claude/w-<lane> diff --binary 3c717370 > /home/claude/patches/<lane>.patch`.
- Dave's 14:55 answers to the #314 review page are verbatim at `/mnt/user-data/outputs/314/DAVE-RULINGS-2026-10-02-1455-borders-switch-templates.md` (also at the seat `notes/_lanes/314/DAVE-RULINGS-2026-10-02-1455-borders-switch-templates.md`). Quote them; never paraphrase. They are not yet inscribed in `_rulings.json` (the committer does that at the end); cite them as "Dave 14:55, call N".
- Renders that open a menu or field do it by CLICK (pointer), never by focus + key, so no keyboard focus ring shows unless the render is about keyboard focus (Dave 14:55, call 1: "we never have a focus state unless the user is using keybord controls").
