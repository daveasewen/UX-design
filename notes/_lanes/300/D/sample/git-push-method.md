---
name: git-push-method
description: "RULED 2026-07-05 (supersedes 07-02 terminal-only): single-writer git — Claude commits in terminal (+ clears stale locks), Dave pushes via GitHub Desktop ONLY; never push from terminal (hangs on creds), never commit in Desktop. CLOUD-MODE lock fix added 2026-07-14."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 17c82c4a-c802-4eb0-9b9a-20dbf87fe656
  modified: 2026-08-31T07:15:22.152Z
sources: [cowork-import]
imported_at: 2026-09-16T03:16:01Z
---

**RULED 2026-07-05 (Dave) — CURRENT.** Push method for UX-design (and any mounted repo):

- **Single-writer, split by layer:** Claude makes ALL commits (terminal, local — no creds touched). Dave does the PUSH, through **GitHub Desktop ONLY**. *(The "paste-ready summary + description" beat that used to sit here is RETIRED — Dave #63, see [[workflow-commit-summaries]]: he reads the message in Desktop; nothing to paste.)*
- **The auth layer has exactly one tool: Desktop.** Terminal push HANGS for Dave (spinning wheels, no error = HTTPS credential-helper conflict from mixing tools; sandbox also has no GitHub creds / keychain unreachable). So the terminal never does the remote/auth op — commit is local, push is Desktop. One tool on the credential layer = no fight.
- **Keep Desktop CLOSED while Claude commits**, open it only to push after Claude says "committed + locks clear." (This neutralises the 07-02 concern that Desktop's background fetches race a commit.)
- **Never** push from terminal; **never** commit in Desktop.
- **Git identity** isn't set in fresh sandboxes — commit with `git -c user.name="Claude" -c user.email="claude@anthropic.com" commit …`.

**Stale-lock hygiene (Claude's job before handoff) — method depends on run mode:**
- The delete-guard blocks git from unlinking its own `.git/index.lock` / `HEAD.lock` / `objects/maintenance.lock` / `objects/tmp_obj_*`. `rm` fails "Operation not permitted".
- **On-computer / local Cowork:** call `mcp__cowork__allow_cowork_file_delete` then `rm` (proven 2026-07-05).
- **⚠️ CLOUD Cowork (device bridge, `device_bash`) — added 2026-07-14:** `allow_cowork_file_delete` is NOT available and `device_bash` cannot delete at all. Workaround that WORKS: `mv .git/index.lock .git/HEAD.lock .git/objects/maintenance.lock` into a `_to_delete/` folder at repo root, then commit. **Running git itself from `device_bash` also fails** — it recreates locks it can't clean up (`unlink … Operation not permitted`), so the commit never lands and HEAD is unchanged. So in cloud mode DON'T try to commit via `device_bash`; instead just clear the locks by `mv`, then have **Dave commit AND push in GitHub Desktop** (Desktop's own commit is also blocked until every `*.lock` is moved aside — check `find .git -name '*.lock'`, not just index.lock). Then Dave deletes the `_to_delete/` folder.
- **Best fix for repo work in cloud:** re-run the task "On your computer" (desktop app → Run this task picker) so the terminal has real unlink permissions and Claude can commit directly.

**⚠️ Stale-msgfile trap (bitten 2026-07-22):** `/tmp` persists across sessions and files there can be owned-unwritable later; a failed heredoc + `git commit -F /tmp/msg.txt` silently committed YESTERDAY'S message. Rules: unique msgfile name under a session-owned dir (outputs/), `head -1` before `-F`, read the message back after committing. Full gotcha inscribed in `knowledge/_RUNBOOK-git-commit.md`. Also observed same day: Dave pushed mid-session (Desktop open during my commit window) — amend-after-commit is only safe while unpushed; check ahead-count before amending.

## ✅ 2026-08-09 (#137) — `s137-D1`: THE PUSH GATE STOPPED DIRTYING ITS OWN TREE

**RULED by Dave and ENACTED same session.** Since `s133-D2` the `--push` path asserts a **clean tree**. But
`_capture_gate.py --wrap` and `_checkin.py` both append to `notes/_REHEARSAL-LOG.jsonl`, which is **tracked**
— so *verifying a commit after making it* dirtied the tree and refused the very push `s133-D2` exists to
allow. `_git_commit.sh` runs the gate at `:153/157` and stages at `:300–316`, so a run **inside** the script
is captured and **anything run after the commit is not**.

**The ruling:** the clean-tree assertion excludes **exactly one named file**, `notes/_REHEARSAL-LOG.jsonl`,
**written out in full so the exclusion cannot silently widen** — not a pattern, does not generalise to a
second file. Dave picked it over two alternatives (move the append ahead of the staging seam; stop tracking
the log). Enacted `knowledge/_git_commit.sh:43-44` (`PUSH_DIRT` + `git status --short -- . ':(exclude)…'`);
**the refusal now also PRINTS the dirty paths**, which it did not before.

★ **Driven three ways** on the artefact's own bytes: real dirt → rc=1 with the log absent from the list ·
log-only → rc=0 · log **+ one other file** → rc=1 (**exclusion proven NARROW**). ⚠ **NOT driven: the
end-to-end `--push`, because driving it means pushing** — UNPROVEN BY CHOICE until Dave's next push.

★★ **The general shape, and it hit TWICE in one session — treat it as a class:** *an instrument that writes
into the tree it measures.* The other instance was **fontconfig**, whose `.uuid` markers landed inside
`knowledge/assets/fonts/_desktop/TTF/` after #136's ENOSPC fix pointed `FONTCONFIG_FILE`'s `<dir>` at the
repo TTFs — same failure, different instrument, and it also trips this clean-tree gate. See
[[sandbox-html-rendering]]. ⛔ Dave on that one, verbatim: *"no patches or hacks solve it permanently please"*
— so **do not gitignore the strays**; the fix is to move the writes out of the tree.

## ⛔ 2026-08-10 (#145) — MSGFILE PREFIX CLASS, INSTANCE 5, AND A NEW CAUSE

**Do NOT author msgfile line 1 with a `#<n> <date> — ` prefix on a NON-WRAP commit.** T3 generates its own
`after #<n> <date> — ` headline and **prepends** it, so an authored prefix doubles:
`after #145 2026-08-10 — #145 2026-08-10 — post-wrap fix: …` (commit `3044f1b`). Prior instances (×4 by #141)
all came from **diagnostic re-runs** mutating the msgfile; this one came from **authoring**, so "fresh printf
per invocation" — which I did correctly — cannot prevent it. Two distinct causes, one symptom.

★★ **Why nothing caught it: the script's own check is self-confirming.** `_git_commit.sh` prints
*"subject asserted identical to msgfile line 1"* — but T3 **mutates line 1 first**, then compares the commit
subject to what it just wrote. It is structurally incapable of catching a doubled prefix. [[check-after-its-own-remedy]]
★ The one check that DOES work: `git log -1 --format='%s' | grep -o '#<n> <date> —' | wc -l` — expect **1**.

⚠ **Also learned:** T3 **REFUSES** a non-wrap commit without `SESSION_N` (`s130-D3`, GENERATE-NEVER-INHERIT) —
loud, named, nothing staged, and it prints the remedy. That refusal is working correctly; re-run as
`SESSION_N=<n> bash knowledge/_git_commit.sh --reconciled <FRESH msgfile> <paths…>`.

**Left unrewritten** per the [[subject-fold-gated-124]] no-rewrite precedent. The gate for this class is still
unbuilt — now instance 5.

## ⛔ 2026-08-10 (#147) — INSTANCE 6: A COPY OF A MUTATED MSGFILE IS NOT FRESH

Doubled `after #147 … — after #147 … —` prefix (commit `f853a91`, caught by the independent grep-count and
amended clean to `2ed0425` while unpushed). Cause: the FIRST invocation mutated the original msgfile in
place; every retry was `cp`'d FROM that original, inheriting the prefix, and T3 prepended again. **"Fresh
msgfile" means a fresh `printf` FROM SCRATCH — never a `cp` of any file the script has ever seen.** Also
learned: since #128 the script REFUSES without explicit paths or `--all-dirty` (`git add -A` retired) — that
refusal prints only the dirty list, easy to misread as a lock problem; read the script's refusal text, not
its tail. Class count now 6; gate still unbuilt.

## ⛔ 2026-08-11 (#154) — INSTANCE 7: A SCRIPT REFUSAL STILL MUTATES THE MSGFILE

TRIPLED prefix (`7e35923`, amended clean while unpushed, message read back). New shape: no `cp` involved —
the SAME msgfile was passed to three consecutive invocations, two of which REFUSED (chain-stale, then
no-paths). **A refusal is not a no-op: T3 mutates line 1 BEFORE the refusal point, so every retry against
the same file stacks another prefix.** The rule generalises: fresh `printf` per invocation INCLUDING
retries after refusals. Independent check caught it (`git log -1 --format=%s`, prefix count ≠ 1).
Class count now 7; gate still unbuilt.

## ⛔ 2026-08-12 (#162) — INSTANCE 8: THE #154 SHAPE, RE-BITTEN DESPITE THE MEMORY

Doubled prefix (`6e0ed57`, amended clean to a fresh msgfile while unpushed, pushed as `0fa5f8f`).
Same cause as instance 7: first invocation REFUSED (no paths / `--all-dirty` missing), retry reused
the SAME msgfile, which the refusal had already mutated. The hook one-liner said "FRESH printf per
invocation" and I read it as per-commit. **Per INVOCATION means including refused ones.**
Caught by reading the subject back after commit. Class count now 8; gate still unbuilt.

⚠ Also #162: `git status -sb` showed only `ahead 1` at commit time — #161's "wraps NOT pushed" note
was stale; the remote already had them. Check ahead-count, don't inherit the pushed/unpushed claim.

## ★★ 2026-08-19 (#203) — `s203-D1`: PUSH AUTHORITY DELEGATED TO THE CONDUCTOR'S SEAT

Dave, verbatim: *"I'm comfortable with you having control over the push now, this human is a
hinderance now."* Inscribed `s203-D1` (202 records). **The conductor commits at wrap AND pushes,
and owes Dave the CI read-back in chat after every push** — the read-back is part of the ruling.
★ **MEASURED AT FIRST USE (#203, same session): `timeout 15 git push origin master` → exit 0,
`150cca4..b492496`, ~1s.** The "terminal push hangs / sandbox has no creds" premise was STALE for
this environment — the hang was Dave's local credential-helper conflict, and the current sandbox
pushes fine. So the mechanism is simply **terminal push at the conductor's seat**; GitHub Desktop
is the fallback (via computer use), not the route. Verify with a bounded `timeout`, never an
unbounded push. Dave may reclaim by a word in chat; newest word wins.

## ★★ 2026-08-19 (#207) — `s207-D1`: PUSH AT THE CONDUCTOR'S JUDGMENT, THE ON-DAVE'S-WORD HALF RETIRED

Dave, verbatim, live mid-turn right after pushing `2f4dd6e` himself: *"btw, you are free to push
whanevr you like, im comfortable with that now."* Inscribed `s207-D1` (205 records); runbook step 5
corrected by addition same session. **What stands unchanged:** the ruled call form
`bash knowledge/_git_commit.sh --push` (master, ff-only, verified) and the CI read-back owed in chat
(`s203-D1`). Exercised twice at #207: `2f4dd6e..6759e5f` and `6759e5f..8c09888`, both verified.
★ CI read-back path when `gh` is absent and api.github.com returns empty (private repo, unauthed):
the Chrome MCP on github.com/…/actions works — run list via `a[href*="/actions/runs/"]`, verdicts
from the job page's ❌ lines. Read run 32283675400 that way: 48 pass · 2 FAIL (`[13]` standing red +
`[110]` mention-map re-stale, third recurrence).

★ Re-affirmed by Dave #225 (2026-08-30), verbatim: *"btw you are free to push as you like"* — same
licence, standing. Exercised #225: `cbe69e6..3c1582c` verified, CI read-back delivered in chat.

## ⛔ 2026-08-31 (#227) — TWO FALSE COMFORTS AT THE PUSH SEAM, SAME MORNING

1. **A range against a NONEXISTENT ref is empty and reads as "synced."** `git log origin/main..HEAD | wc -l`
   returned 0 — because `origin/main` does not exist (branch is **master**); 12 commits were still local
   and I told Dave "pushed." Rule: name the branch from `git branch --show-current` before ANY ahead-count;
   an empty range proves nothing until the ref is proven to exist.
2. **`--push`'s refusal tail looks like success when grepped.** The clean-tree refusal prints the
   instrumentation-declaration block LAST, so `tail`/`grep committed` shows benign-looking lines and no ✗.
   Read for the literal `✅ pushed and VERIFIED` line — it prints the remote==local sha; anything else is
   NOT a push. (Both caught same morning by the CI read-back finding 0 runs for HEAD — the read-back is
   the outer control that catches a false push, one more reason `s203-D1` makes it mandatory.)

**⚠️ SUPERSEDES the 2026-07-02 ruling** ("terminal-only push; GitHub Desktop RETIRED"). Why reversed: (1) terminal push now hangs for Dave on credentials; (2) that 07-02 ruling itself found the lock conflicts were caused by the **sandbox delete-guard, NOT Desktop's fetches** — so the anti-Desktop rationale was already undercut. Desktop-for-push is safe given lock-clearing + closed-during-commit. Papercut for [[robustness-portability]]; this reversal is itself a case study for [[pm-knowledge-graph-direction]] (a superseded ruling, edge now recorded).


