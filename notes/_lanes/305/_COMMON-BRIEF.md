# #305 — COMMON BRIEF (every lane reads this first)

provenance: 305 · 2026-09-27 · conductor Opus 5.5 in the CLOUD, linked to Dave's Mac. You work ON THE MOUNT via the
`mcp__remote-devices__device_bash` tool: `cd "$HOME/mnt/Projects--UX-design"` at the top of every call.

## What happened
Dave took the Tuesday sitting on Sunday 2026-09-27 (13:59–14:53 BST). His answers, VERBATIM, are
`notes/_lanes/305/DAVE-RULINGS-2026-09-27-sitting.md`. The page they answer is
`notes/_SITTING-304-tuesday-2026-09-29-v1.html` — each call's text there (its recommendation and "what a yes
unblocks") IS the spec for that call. Quote his words; never paraphrase them.

His standing rule, said in chat at 13:59 BST (verbatim):
> most of these I want to do both but we might need to test a bit after, I guess we can just have a review on some of these decisions in the future, they are not set in stone they are set in ink and can be crossed out in the future

⇒ a "yes" on a sitting call means INSCRIBE AND BUILD. Conductor's reading of the short answers (the conductor
put these to Dave in chat; build to them):
- call 5 "as recommended" = the CLIP-VISIBLE form. call 42 "b" = route B as recommended.
- call 45 = the name is **Launchpad** (not "Apollo Live"): lock-up = "Apollo" as eyebrow, "Launchpad" below.
- call 47 "yes" = the PoC starts in October, once calls 14–19 are in the tree. Friday note: the PoC is a SURPRISE.
- call 27 has NO decision (comment only: "I need to visuals for this") — NOT ruled; a visuals page is owed.
- call 41c "keep today's through the cut"; call 3 "advisory through the cut"; call 41b "40px, the tile's own".
- calls 6, 8, 29 carry comments = NEW open threads (Dave's), not rulings.

## Rules for every lane (all are standing; none is new)
1. SCOPE (s172-D3 a): "Use the minimum complexity that solves the current task. No abstractions for hypothetical
   future needs. No defensive code for scenarios that cannot occur here. Make the changes requested and those
   clearly necessary to them — nothing else." Verification is TARGETED at the seam your deliverable creates; one
   level deep. Report `machinery: N instrument / M feature`.
2. Dave's fence: "careful of externalities, I don't want to fix something only to break other constituent parts."
   No existing gate, law or check is removed, relaxed or skipped.
3. ⛔ NEVER run `git status`. Read-only git ONLY as `git --no-optional-locks …`. ⛔ NEVER commit, push, `git add`,
   `git reset`, `git checkout`, `git stash`. The conductor's commit seat does all git writes.
   ⛔ NEVER `git checkout` / revert a shared directory — revert only files you own, from your own backups.
4. ⛔ `device_bash` kills background jobs when the call returns (≈178 s wall). Run everything in the foreground;
   split long work into steps; keep intermediate files under your lane dir.
5. FILE OWNERSHIP: write only the files your brief assigns you, plus your lane dir `notes/_lanes/305/<LANE>/`.
   Before your first write, list the paths you will write in `notes/_lanes/305/<LANE>/OWNS.txt`. If you need a
   file outside your fence, STOP that item and say so in your report — another lane may own it.
   Whole-tree regenerators (`_build_all.py`, `_gen_chain.py`, `_render_rulings.py`, the regen serial) are the
   COMMIT SEAT's, not yours — unless your brief names one. ⛔ DO NOT RUN `_build_all.py`.
6. Canon's own figures: every figure on a built page comes from canon, never from a specimen being imitated.
7. Rendering: at the seat, ONE bash call:
   `export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh; python3 <driver>`
   with `executable_path=$RENDER_SHELL`; `goto("file://…")`, never `set_content()`. Runbook:
   `knowledge/_RUNBOOK-render-verify.md`.
8. `pip install tiktoken --break-system-packages` if a gate needs it and it is missing.
9. Rulings are written ONLY through `knowledge/_inscribe_ruling.py` (append / --set-status / --amend-evidence).
   Only lane A inscribes. Other lanes may use `--set-status <id> enacted --evidence-sha <sha>` ONLY when their brief
   says so (normally the commit seat stamps after the commit exists).
10. ⛔ No Project memory reads or writes. No artifact publishing (the conductor publishes).
11. REPORT: file `notes/_subreports/2026-09-27-305-<LANE>-<slug>.md` (provenance line `305 · 2026-09-27`,
    `status: observed`): what you did per call, every path written (the commit seat needs the exact list),
    what you measured and how, what you held back and why, what is Dave's. Your final message back to the
    conductor = that report's path + a ≤15-line summary + the exact changed-path list.
