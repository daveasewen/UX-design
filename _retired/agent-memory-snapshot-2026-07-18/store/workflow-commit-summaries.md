---
name: workflow-commit-summaries
description: "When user says they're committing, automatically provide git push summary and description"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d5fd4177-9969-4ce3-b8dd-dd9a7c2f2afe
---

**Rule:** When Dave says "I'll commit" or similar, provide a concise git commit summary + description before he does the push. Display as plain unformatted text in a simple panel (show_widget).

**HARD CONSTRAINT (seen 2026-06-24):** the sandbox CANNOT write the mounted repo's `.git` — `git add` leaves a `.git/index.lock` it then can't unlink ("Operation not permitted"), and `git commit` fails. So Claude cannot commit on Dave's behalf; ALWAYS hand him a paste-ready command (incl. `rm -f .git/index.lock` first, since a stale lock may linger) + the message. Staging via `git add` partially works but leaves the lock — prefer giving him a self-contained `git add … && git commit -F` block.

**Why:** Saves time; ensures consistent, clear commit messages; keeps the work narrative accurate for future reference. Panel format makes it easy to copy.

**How to apply:** At the moment he says he's committing, generate:
- **Summary** (1 line, <50 chars): what changed
- **Description** (2-3 lines): why it changed, what it enables

Display in show_widget as simple monospace text block (no styling, no interactive elements). Format:
```
Summary text here

Description text here
```
