# Reconciliation register — README.md (language review)

*Decision record for the 2026-07-04 process-doc language review (rollout #3 — completes the
cold-start trio: charter, AGENTS, README). Produced by `_REVIEW-DOSSIER-README_2026-07-04.html`,
decided by Dave, enacted 2026-07-04. **Rollback:** revert the enacting commit; the REVERT line
on each entry is the exact pre-change wording. **Status: ALL 5 ENACTED.***

Reviewer: Dave · 2026-07-04 · 5/5 decided (all Agree) · 0 added by reviewer

---

## README-R1 · Gates · build count · [STALE] · 2026-07-04
DECISION: Agree · ENACTED
REVERT (before): a 15-step build …
CHANGE  (after): an 18-step build …

## README-R2 · Status · build count · [STALE] · 2026-07-04
DECISION: Agree · ENACTED
REVERT (before): Engine built and green (15/15 build steps).
CHANGE  (after): Engine built and green (18/18 build steps).

## README-R3 · Operating model · taste call · [UNSOURCED] · 2026-07-04
DECISION: Agree · ENACTED
REVERT (before): one human taste call (~20 seconds)
CHANGE  (after): one human taste call (a brief human decision)
NOTE: same reword as AGENTS-A3; the figure also appears in the north-star mock — carry it there if that doc is ever revised.

## README-R4 · Data hygiene · two-machine rule · [CONTRADICTION, STALE] · 2026-07-04
DECISION: Agree · ENACTED
REVERT (before): Home machine: synthetic + public data. Agency machine: real assets. Raw Figma exports … see that ADR's open item on token-store provenance before adding any real asset here.
CHANGE  (after): Resolved (ADR-0005): agency machine with company access — the "home = synthetic only" premise was wrong; real brand values cleared to live here. Raw exports stay untracked; git history still holds earlier raw exports (purge deferred, accepted risk while private). Heading dropped "(two-machine rule)".
NOTE: propagation — the ADR-0005 close-out dissolved the two-machine rule; README had not caught up.

## README-R5 · Status · next milestone · [STALE] · 2026-07-04
DECISION: Agree · ENACTED
REVERT (before): Next milestone: the calibration proof — re-run a completed HSBC project from its original brief, blind …
CHANGE  (after): Next milestone: the first real test — a scoped novel-work screen with an external stakeholder; the calibration re-run stays as the rigour backstop.
