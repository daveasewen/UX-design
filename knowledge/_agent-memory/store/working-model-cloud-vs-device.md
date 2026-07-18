# Working model — cloud session vs the live project (RULED 2026-07-14, Dave)

**The rule:** every file Claude produces lands in Dave's live project on disk **as it is made**,
via the desktop bridge (`device_commit_files`) — NOT built in cloud scratch and "delivered" into the
chat for later. Delivering a file into the conversation (SendUserFile) is NOT the same as putting it
in the project; a download card does not write to disk.

**Why this exists:** on 2026-07-14 a whole session of work (dossier tone fix, component-review skill,
Apollo sponsor deck, built designer KB) had piled up only in the cloud container's `/tmp` and in a
stale `/tmp/ux` snapshot — none of it in the real repo. Dave: "these docs are being created on the
cloud, I need them in the project… dude, lets not do that again."

**How to work from now:**
- The live repo is the connected folder `/Users/daviewen/Documents/Claude/Projects/UX-design`
  (parent, has `.git`), mounted for `device_bash` at `mnt/Projects--UX-design/`. The nested
  `UX-design/UX-design` is the empty decoy — ignore it.
- `/tmp/ux` in the cloud is a STALE tar snapshot from an earlier session — do not treat it as truth.
  Work against the live repo via the bridge: stage → edit in cloud if needed → `device_commit_files`
  back, or write new files straight to disk. Land as you go.
- The cloud workspace is only for intermediate/render/build steps (screenshots, KB generation, etc.).
- Generated artifacts (e.g. `designer-skills-v1/knowledge/`, 839 files) can be regenerated on Dave's
  machine with `device_bash` running the build script locally (no network needed) rather than pushing
  hundreds of files through the bridge.

**Git:** the working tree had a large uncommitted pile (not just one session) + a stale
`.git/index.lock` that blocks commits. `device_bash` cannot delete (mv the lock into `_to_delete/`
instead). Commit model in the cloud era is still Dave's call — old rule "Claude commits in a terminal
that shares the repo" is broken because cloud Bash can't see the live repo; `device_bash` can.
