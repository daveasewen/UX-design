---
name: feedback-verify-before-asking
description: "RULE 2026-07-14: verify state from the live filesystem/gate before asking Dave a state-question; only ask when genuinely blocked by something unverifiable or irreversible"
type: feedback
---

**Rule (Dave, 2026-07-14, firm):** When a question can be answered by **reading the repo or running a
gate/build, do that** — do not put a state-question to the user. Only ask when genuinely **blocked by
something you cannot verify or cannot undo.**

**Why:** I hit stale reads. My early cloud snapshot went stale when the *other* session landed the fixed
tranches + `_PROFORMA-DEFECTS.md` + rules 10–13 to disk moments later. Working from the stale snapshot I
concluded the canon/fixes were "lost" and raised a whole recovery **AskUserQuestion** — whose premise was
already false. Dave: *"Ignore your own recovery question — its premise is out of date… verify from the
filesystem, don't ask the user… stop putting state-questions to the user."*

**How to apply:**
- Before asking "is X present / did Y land / which version is on disk", **re-check the live source**:
  `git status`, re-read the file, run the gate/build. Snapshots taken earlier in a session can be stale —
  re-pull if another session may have written.
- Reserve `AskUserQuestion` for genuine forks the code/filesystem can't settle (taste calls, irreversible
  choices, missing external inputs). A verifiable fact is never one of them.
- This complements [[feedback-clarify-reflect-back]] (don't over-read tone) and [[feedback-route-by-default]]
  (announce routing) — together: verify first, route by default, reflect tone back, ask only when truly stuck.
- Distinct from the recovery instinct: it's fine to be cautious about clobbering reviewed work, but resolve
  "what's actually on disk" by *looking*, then proceed with a stated assumption + an offered undo, not a question.
