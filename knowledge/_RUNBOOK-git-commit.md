# Runbook — committing from the sandbox (lock workaround)

*Why this exists: the sandbox mount runs a **delete-guard** — git can create `.git/*.lock` and
`objects/tmp_obj_*` files but **cannot unlink them** (`rm` → "Operation not permitted", even as the
file's owner). So git commits fail with `Unable to create '.git/index.lock': File exists`, and any git
command leaves a fresh lock behind. `mv` IS permitted where `rm` is not — that's the whole trick.
Companion to memory `git-push-method`; git split = Claude commits, Dave pushes via GitHub Desktop.*

## The procedure — RUN THE SCRIPT (2026-07-26, dream-pass P2, Dave ruled)

```
git status --short                                   # step 0.5 — account for EVERY dirty path first
bash knowledge/_git_commit.sh --reconciled <msgfile>  # clear · stage · clear · commit · clear
```

The script mechanises the whole sequence below, refuses to stage while any `.git/*.lock` exists,
refuses an empty/stale msgfile, verifies HEAD advanced AND the message matches, and clears locks as
its last action. It cannot do step 0.5's judgment — the `--reconciled` flag is your attestation that
every dirty path is accounted for (worktree-reconcile rule). WHY a script: 7 of 9 commit sessions (3 of 5 at ruling 2026-07-26; #36, #41, #56 and #109 since — the count is maintained because it is the evidence for this tool. ⚠ #109 hand-rolled the lock `mv` AND ran a control probe to re-derive the 0-byte/mtime diagnostic already written in Gotchas below, then found the script — Dave caught it with "there s a commit runbook". The memory hook, not the runbook, was the misfire: it carried "ask if GitHub Desktop is open" WITHOUT the diagnostic that answers it. Hook corrected #109)
reconstructed this sequence from memory under wrap heat and hit the lock failure first; a hot agent
can call one script (`feedback-gate-dont-patch`). Everything below is the reference the script
implements — read it when the script surprises you, don't re-derive it.

## The manual sequence (reference — the script implements this)

**Clear locks BEFORE staging as well as after — the sequence is clear · stage · clear · commit · clear.**
A lock left behind by the *previous* session blocks `git add` itself, so starting at "stage" only works
from an already-clean `.git`. (Corrected 2026-07-18 after step 1 failed on a 12-minute-old stale lock.)

0. **Clear any inherited lock first** (not `rm` — `mv`):
   ```
   cd <repo> && mkdir -p _to_delete/_stale_locks
   for L in $(find .git -name '*.lock'); do mv "$L" _to_delete/_stale_locks/; done
   find .git -name '*.lock'      # expect: none — if not, stop; do not stage
   ```
0.5. **Account for every dirty path BEFORE you stage** (added 2026-07-19). `git add -A` is a blunt
   sweep — it will commit a worker's half-finished experiment or a broken artifact as readily as your
   own work, and a *selective* add silently drops worker dirt. Neither failure is otherwise guarded.
   Reconcile first:
   ```
   git status --short            # every path below must be explained
   ```
   Confirm you can name WHY each dirty path exists (yours, or a known worker's). Any path you can't
   account for → **stop**: `ls notes/_receipts/` and read the sibling sessions
   (`mcp__session_info__list_sessions` → transcript) before committing. This matters most with parallel
   sessions live — the working tree is shared, so their changes are already in yours. Companion:
   `_RUNBOOK-parallel-conductor.md` conductor step 2.5.
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
   git log --oneline -1          # confirm the new hash is HEAD — and the MESSAGE is yours
   ```
   ⚠ **Write `<msgfile>` under a dir this session owns (outputs/), with a UNIQUE name, and `head -1`
   it before `-F`.** Never a fixed `/tmp` name — see the 2026-07-22 gotcha below.
4. **Clear the lock git just re-created**, as the *last* action (any git command, even `status`,
   respawns `index.lock`). Do NOT run another git command after this:
   ```
   for L in $(find .git -name '*.lock'); do mv "$L" _to_delete/_stale_locks/; done
   ```
4b. *(Optional sweep — dream-pass P8, 2026-07-26. ⛔ **CORRECTED #41 — this step used to route the job
   to Dave and that was wrong.**)* If `_to_delete/` is bulging, **the agent clears it — do NOT put it in
   the handoff.** `rm` fails `Operation not permitted` **until permission is granted**, and there is a
   tool for exactly that: **`mcp__cowork__allow_cowork_file_delete`**, whose own description says to call
   it *"whenever a delete operation (such as rm) fails with 'Operation not permitted', rather than
   telling the user it is impossible."* Then `rm -rf _to_delete/*` works. ⚠ **Keep the directory and
   re-`mkdir -p _to_delete/_stale_locks`** — the lock workaround writes there every commit.
   ★ **Why this correction exists:** #41 handed Dave a terminal command; he replied *"i dont know how to
   do this."* He pushes via GitHub Desktop by design and should never need a shell. **A step that routes
   agent-solvable work to the human is a defect in the step** — and this is the THIRD mechanism #41
   hand-rolled around in one window (`_git_commit.sh`, the chain file, this).
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
- **`_to_delete/` is gitignored.** ⛔ **CORRECTED #41 — the old text here read *"the bridge can't empty
  it from the sandbox — Dave deletes it on his machine"*, and that is FALSE:** the agent clears it after
  `mcp__cowork__allow_cowork_file_delete` grants the folder (see step 4b). **Never commit `_to_delete/`,
  and never hand the cleanup to Dave.** ⚠ The false claim survived because *"the sandbox cannot"* is TRUE
  of the default state and nobody re-tested it once a permission tool existed — [[assertion-propagation-gap]]:
  the gate fires on a FLIP, so a line that was true when written and quietly went stale is never chased.
- **Big/licensed binaries** (fonts, raw exports) must be gitignored before `git add -A` — check
  `git status --short` for anything under `knowledge/assets/fonts/` or `knowledge/tokens/_raw/`.
- **The stale-msgfile trap (bitten 2026-07-22).** `/tmp` persists across sessions and a file there can
  be OWNED-UNWRITABLE by a later session. Sequence that bit: heredoc to `/tmp/msg.txt` failed
  ("Permission denied") but the command chain continued, and `git commit -F /tmp/msg.txt` silently read
  **yesterday's message from the stale file** — 43 files inscribed under the previous session's text.
  Confident-false-inscription, in git. Caught same minute (`git log -1` showed the wrong headline);
  fixed by `--amend -F` from a fresh uniquely-named file under outputs/. Rules: unique msgfile name in
  a session-owned dir · `head -1` the file before `-F` · after committing, read the MESSAGE back, not
  just the hash. (Amend is safe only while the commit is unpushed — check `git status -sb` ahead-count
  first; if Desktop might be open, confirm the bad commit didn't just get pushed.)
- If commits must be frequent/reliable, re-run the task **"On your computer"** (desktop app → Run
  this task) so the terminal has real unlink permissions and this dance isn't needed.

## Entry points
`git-push-method` (memory — the single-writer split + cloud/local variants) · `AGENTS.md` (git split) ·
`_RUNBOOK-capture-ritual.md` (step 5 calls this).

---

## Reverting in the sandbox — and the trap in the bulk form (added 2026-07-19, T-D12)

`git checkout` FAILS here: it needs to unlink, and the `.git` mount blocks unlink. **Write-in-place
is the working revert:**

```bash
git show HEAD:<path> > <path>                                   # one file
for f in $(git diff --name-only); do git show HEAD:$f > $f; done  # everything — SEE WARNING
```

⚠️ **The bulk form reverts YOUR TOOLING TOO.** During T-D12 I used it to reset an experiment and it
silently took `apply_type_bind.py` — the script the experiment depended on — back to HEAD with it.
The next run then produced HEAD's behaviour while I read the output as the new behaviour. Cost:
two wasted render cycles before I noticed.

**Before any bulk revert, park work-in-progress tooling outside the repo:**
```bash
cp knowledge/apply_type_bind.py /tmp/apply_type_bind.py.patched   # park
for f in $(git diff --name-only); do git show HEAD:$f > $f; done  # revert
cp /tmp/apply_type_bind.py.patched knowledge/apply_type_bind.py   # restore the instrument
```
The general rule: **a revert is scoped to the EXPERIMENT, never to the instrument measuring it.**
If the instrument is itself uncommitted, `git diff --name-only` cannot tell them apart — you must.

## Sandbox wart — build kills at call boundaries (banked 2026-07-27 #15)

**Nothing survives a tool-call boundary in this sandbox** — `nohup` and `setsid` both get reaped
(tested #15). A `_build_all.py` killed mid-run freezes whatever step was writing: the signature is
**~33 stripped compliance JSONs + `_CAPTURE-GATE.md`** (#14's "34 files / 1,335 deleted lines" and
#15's 33/1,336 were the same event). **Run the build FOREGROUND, ONE call — it fits inside 45s.**
Restore stripped files with `git show HEAD:<path> > <path>` — the delete-guard blocks `git checkout`'s
unlink (`Operation not permitted`), and `git status` itself can strand `index.lock` if its call is
reaped (clear per step 0 above).
