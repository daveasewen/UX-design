# Receipt — shared-tree race, 2026-07-22 (theming clean-room × morning Opus wrap)

**What happened.** The Fable theming clean-room opened at ~10:13:03 and read `git status`: HEAD
`06d3378`, ahead 2, four dirty paths (`_STANDARDS.md`, `_PROFORMA-RULES.md`, `_RAG-DECISIONS.md`,
the theming brief). The morning Opus session — still open — committed those same paths as its wrap
**`5459a4b`** at **10:13:17**, fourteen seconds later. My follow-up `git diff` (empty, post-commit)
led me to misread the dirt as stale-mtime phantoms. The truth surfaced only at MY commit step, when
HEAD ≠ the hash I'd recorded.

**Why nothing was lost.** All clean-room edits post-dated `5459a4b`; the ledger text I read at
session start WAS the sibling's inscription (working tree = shared), so R-D25 was inserted on top of
R-D23/24 correctly, and the sibling's ruling-3 inscription (`_PROFORMA-RULES.md`) was never touched
by this session. Both-direction check run at reconcile: my tree carries their text + mine; their
commit carries nothing of mine. Graph verify re-run clean (122 = 122 = 122).

**Reconciliation applied.** GOOD-MORNING + `_LIVE-STATE` + the dossier corrected (ruling 3 = RULED,
fold-in as near-canonical + dedup pass queued; "batch survivor" claim retracted). This receipt is the
breadcrumb per `feedback-worktree-reconcile-trail`.

**The lesson.** Two sessions wrote shared state with no declared conductor; the collision resolved by
timing, not by the model. "Good morning" opened this session WITHOUT a role word while another window
was still live — the opener-line role check should include *"is any other window open?"* before a
solo session self-seats as its own conductor. Also: a dirty tree at session start is a SIBLING
HYPOTHESIS first and a filesystem quirk second — `git log` + receipts before concluding phantom.
