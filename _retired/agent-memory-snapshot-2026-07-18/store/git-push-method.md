---
name: git-push-method
description: "RULED 2026-07-05 (supersedes 07-02 terminal-only): single-writer git — Claude commits in terminal (+ clears stale locks), Dave pushes via GitHub Desktop ONLY; never push from terminal (hangs on creds), never commit in Desktop. CLOUD-MODE lock fix added 2026-07-14."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 17c82c4a-c802-4eb0-9b9a-20dbf87fe656
---

**RULED 2026-07-05 (Dave) — CURRENT.** Push method for UX-design (and any mounted repo):

- **Single-writer, split by layer:** Claude makes ALL commits (terminal, local — no creds touched), with a paste-ready conventional summary + description. Dave does the PUSH, through **GitHub Desktop ONLY**.
- **The auth layer has exactly one tool: Desktop.** Terminal push HANGS for Dave (spinning wheels, no error = HTTPS credential-helper conflict from mixing tools; sandbox also has no GitHub creds / keychain unreachable). So the terminal never does the remote/auth op — commit is local, push is Desktop. One tool on the credential layer = no fight.
- **Keep Desktop CLOSED while Claude commits**, open it only to push after Claude says "committed + locks clear." (This neutralises the 07-02 concern that Desktop's background fetches race a commit.)
- **Never** push from terminal; **never** commit in Desktop.
- **Git identity** isn't set in fresh sandboxes — commit with `git -c user.name="Claude" -c user.email="claude@anthropic.com" commit …`.

**Stale-lock hygiene (Claude's job before handoff) — method depends on run mode:**
- The delete-guard blocks git from unlinking its own `.git/index.lock` / `HEAD.lock` / `objects/maintenance.lock` / `objects/tmp_obj_*`. `rm` fails "Operation not permitted".
- **On-computer / local Cowork:** call `mcp__cowork__allow_cowork_file_delete` then `rm` (proven 2026-07-05).
- **⚠️ CLOUD Cowork (device bridge, `device_bash`) — added 2026-07-14:** `allow_cowork_file_delete` is NOT available and `device_bash` cannot delete at all. Workaround that WORKS: `mv .git/index.lock .git/HEAD.lock .git/objects/maintenance.lock` into a `_to_delete/` folder at repo root, then commit. **Running git itself from `device_bash` also fails** — it recreates locks it can't clean up (`unlink … Operation not permitted`), so the commit never lands and HEAD is unchanged. So in cloud mode DON'T try to commit via `device_bash`; instead just clear the locks by `mv`, then have **Dave commit AND push in GitHub Desktop** (Desktop's own commit is also blocked until every `*.lock` is moved aside — check `find .git -name '*.lock'`, not just index.lock). Then Dave deletes the `_to_delete/` folder.
- **Best fix for repo work in cloud:** re-run the task "On your computer" (desktop app → Run this task picker) so the terminal has real unlink permissions and Claude can commit directly.

**⚠️ SUPERSEDES the 2026-07-02 ruling** ("terminal-only push; GitHub Desktop RETIRED"). Why reversed: (1) terminal push now hangs for Dave on credentials; (2) that 07-02 ruling itself found the lock conflicts were caused by the **sandbox delete-guard, NOT Desktop's fetches** — so the anti-Desktop rationale was already undercut. Desktop-for-push is safe given lock-clearing + closed-during-commit. Papercut for [[robustness-portability]]; this reversal is itself a case study for [[pm-knowledge-graph-direction]] (a superseded ruling, edge now recorded).
