# Runbook — committing from the sandbox (lock workaround)

*Why this exists: the sandbox mount runs a **delete-guard** — git can create `.git/*.lock` and
`objects/tmp_obj_*` files but **cannot unlink them** (`rm` → "Operation not permitted", even as the
file's owner). So git commits fail with `Unable to create '.git/index.lock': File exists`, and any git
command leaves a fresh lock behind. `mv` IS permitted where `rm` is not — that's the whole trick.
Companion to memory `git-push-method`; git split = Claude commits, Dave pushes via GitHub Desktop.*

## The procedure

**Clear locks BEFORE staging as well as after — the sequence is clear · stage · clear · commit · clear.**
A lock left behind by the *previous* session blocks `git add` itself, so starting at "stage" only works
from an already-clean `.git`. (Corrected 2026-07-18 after step 1 failed on a 12-minute-old stale lock.)

0. **Clear any inherited lock first** (not `rm` — `mv`):
   ```
   cd <repo> && mkdir -p _to_delete/_stale_locks
   for L in $(find .git -name '*.lock'); do mv "$L" _to_delete/_stale_locks/; done
   find .git -name '*.lock'      # expect: none — if not, stop; do not stage
   ```
1. **Stage** (this may print `unable to unlink … tmp_obj_*` warnings — harmless, ignore):
   ```
   git add -A
   git diff --cached --name-only    # confirm the files actually staged
   ```
   > If this prints *"Another git process seems to be running … remove the file manually"*, a lock
   > survived step 0. Nothing staged. Re-run step 0 and try again — do **not** proceed.
2. **Move every lock aside again** (staging respawns `index.lock`):
   ```
   for L in $(find .git -name '*.lock'); do mv "$L" _to_delete/_stale_locks/; done
   find .git -name '*.lock'      # expect: none
   ```
3. **Commit** with identity set (fresh sandboxes have none). It prints `unable to unlink` warnings but
   **the commit still lands** — verify by the HEAD hash, not the warnings:
   ```
   git -c user.name="Claude" -c user.email="claude@anthropic.com" commit -F <msgfile>
   git log --oneline -1          # confirm the new hash is HEAD
   ```
4. **Clear the lock git just re-created**, as the *last* action (any git command, even `status`,
   respawns `index.lock`). Do NOT run another git command after this:
   ```
   for L in $(find .git -name '*.lock'); do mv "$L" _to_delete/_stale_locks/; done
   ```
5. **Hand off to Dave** — "committed at `<hash>`, locks clear, safe to push." Dave pushes via
   **GitHub Desktop only** (never terminal push — it hangs on credentials). If Desktop ever complains
   about a lock, Dave can delete `.git/index.lock` on his side (his machine has normal permissions).

## Gotchas
- **Judge success by HEAD, not warnings.** The `unable to unlink … tmp_obj_*` / `*.lock` lines are git
  failing to tidy its own scratch files; the commit object is written and HEAD advances regardless.
- **Never `rm` inside `.git`** from the sandbox — it fails and wastes a turn. Always `mv` aside.
- **A stale lock is not a live lock.** Before assuming GitHub Desktop is holding it, check: a **0-byte**
  `index.lock` whose mtime is ~the same instant as `.git/index` is the signature of a *completed* git
  operation that then failed to unlink its own lock — i.e. this delete-guard, not a live process.
  Moving that aside is safe. A lock Desktop genuinely holds is a different situation; keep Desktop
  closed during sandbox git work (memory `git-push-method`).
- **The warnings lie about failure, and `git status` lies about success.** Even a read-only
  `git status` respawns `index.lock`, so a clean-looking status run leaves the next `git add` blocked.
  That is why step 4 says the lock-clear must be the *last* git-touching action.
- **`_to_delete/` is gitignored** and the bridge can't empty it from the sandbox — Dave deletes it on
  his machine when convenient. Never commit `_to_delete/`.
- **Big/licensed binaries** (fonts, raw exports) must be gitignored before `git add -A` — check
  `git status --short` for anything under `knowledge/assets/fonts/` or `knowledge/tokens/_raw/`.
- If commits must be frequent/reliable, re-run the task **"On your computer"** (desktop app → Run
  this task) so the terminal has real unlink permissions and this dance isn't needed.

## Entry points
`git-push-method` (memory — the single-writer split + cloud/local variants) · `AGENTS.md` (git split) ·
`_RUNBOOK-capture-ritual.md` (step 5 calls this).
