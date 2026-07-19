# Worker receipt — `gen_rules_index.py` truncation (queue #3/#4.1)

*Written 2026-07-19 17:02, updated 17:17. Worker session (role picked at "read good morning" → Worker).
Conductor is the live session **"Promote the RAG tokens + nail the status component"**.
I did NOT run git, and did NOT edit `_LIVE-STATE`/`GOOD-MORNING`/`_FUTURE-STATE`.*

## ⚠️ CONDUCTOR — read this: paths I touched (so your reconcile step accounts for them)

Dave authorised a scoped step-out of worker role to inscribe the parallel-session hardening. **These are
all disjoint files you were NOT editing — safe to include in your commit or leave; nothing of yours is
touched. None is git-run.** Full list:

- `knowledge/_RUNBOOK-git-commit.md` — new **step 0.5** (reconcile every dirty path before staging). ENACTED.
- `knowledge/_RUNBOOK-parallel-conductor.md` — worker step 4 (fixed receipt path), conductor **step 2.5**
  (reconcile), + a "nothing clashes by construction" guardrail. ENACTED.
- `notes/_receipts/` — NEW conventioned receipt dir; this file moved here (was `notes/_WORKER-RECEIPT-…`).
- Memory (outside the repo): `feedback-worktree-reconcile-trail` + its MEMORY.md index line — PENDING flag
  now cleared to INSCRIBED.

The rules-index fix itself (below) remains the six pre-existing dirty files — **not mine**, still just
needs your commit.

## Headline
**The bug is already fixed in the working tree — uncommitted.** Nothing more to code. I verified it's
correct and complete. **Action for the conductor: just include the already-dirty files in your commit.**

## What I found
The GOOD-MORNING queue listed the `gen_rules_index.py` truncation (silent mid-sentence data loss for 11+
rules) as still-to-chase. On inspection the fix is already present in the working tree but **not yet
committed** (`gen_rules_index.py` last *commit* is 2026-07-03 `0d63d27`; the fix comment is dated today):

```diff
-    return chunk[:500]
+    # No length cap: rule_text is already bounded to a single bullet/paragraph by
+    # the walk-back above. A fixed char cap silently truncated long rules mid-
+    # sentence in _RECONCILIATION.md and made their tails unsearchable in
+    # _consult.py (fixed 2026-07-19). Full text flows to both consumers.
+    return chunk
```

The 500-char cap was the entire cause. Removing it lets full rule text flow to both consumers
(`_rules-index.json` and, via it, `_consult.py`).

## Verification I ran (all pass)
- **All 11 flagged rules now end in complete sentences:** mot-007, neuro-041, neuro-042, pict-014,
  tov-016, type26-015, type26-026, type26-029, webf-017, ctkb-015, icon-015.
- **Old-cap fingerprint gone:** 0 rules of length exactly 500; 0 rules ≥498 chars ending without terminal
  punctuation. Total 465 rules (unchanged count).
- **Full text captured, not just cap-removed:** for webf-017 (981), mot-007 (849), type26-029 (670),
  icon-015 (2833), the index tail is present verbatim in the source `.md` — so the walk-back isn't
  clipping either. Longest rule icon-015 = 2833 chars confirms long rules flow fully.

## Dirty files (all consistent with the fix + a `_build_all.py` run)
```
 M knowledge/guidelines/gen_rules_index.py     ← the fix (cap removed)
 M knowledge/guidelines/_rules-index.json      ← regenerated, full text
 M knowledge/guidelines/_RECONCILIATION.md     ← regenerated, full text
 M knowledge/_consult-index.json               ← rebuilt (tails now searchable)
 M knowledge/_RUNBOOKS.md                       ← build artifact
 M knowledge/_LIVE-STATE-CHECK.md               ← build artifact
```

## Recommendation to the conductor
1. Commit these six files with the truncation fix. Suggested message:
   `fix: drop 500-char cap in gen_rules_index — full rule text to index + consult (11+ rules were truncated)`
2. Tick queue **#4.1** (and the §B "REAL BUG" note) as **DONE — verified, awaiting only your commit**.
3. Provenance worth inscribing: the cap removal is deliberate; the fix comment already explains why, so a
   cold session won't "restore" a cap for tidiness.

## Note / watch
I couldn't attribute *who* applied the fix (it predates my session in the working tree). If the live RAG
session is the one that made these edits as a side-effect of a build, no conflict — they're the same six
files and my verification stands. If someone else is mid-edit on the guidelines index, reconcile before
committing.

---

## PROPOSAL for the conductor to inscribe — a "reconcile the working tree" check in the git runbook

*Prompted by Dave, 2026-07-19: "should there be a check in the git runbook or something." Raised because
this very fix sat as unexplained dirt in the shared tree, relying on luck to be committed correctly.
Worker rule = propose here, conductor decides + inscribes.*

**The gap.** `_RUNBOOK-git-commit.md` step 1 is `git add -A` — a blunt sweep. It guards neither failure:
- **Under-inclusion:** a conductor who deviates to selective `git add <files>` silently leaves worker
  dirt behind.
- **Over-inclusion:** `git add -A` commits a worker's *half-finished* experiment or a broken build
  artifact just as readily as finished work. The runbook warns about binaries + `_to_delete/`, but has
  no "know why each dirty file exists" step.

With parallel sessions the working tree is **shared** — a worker's change (fix OR breakage) is already in
the conductor's tree whether it knows or not. Nothing currently forces the conductor to reconcile that.

**Proposed — `_RUNBOOK-git-commit.md`, new step 0.5 (before staging):**

> **0.5 Account for every dirty path before you stage.** Run `git status --short`. `git add -A` is a
> blunt sweep — it will commit a worker's half-finished experiment or a broken artifact as readily as
> your own work. Confirm you can name *why* each dirty file exists. Any path you can't account for →
> **stop** and read the sibling sessions (`session_info` → transcript/receipt) before committing. This
> matters most with parallel sessions live: the working tree is shared, so their changes are already in
> yours.

**Proposed — `_RUNBOOK-parallel-conductor.md`, conductor checklist, new step between 2 and 3:**

> **2.5 Reconcile the working tree.** `git status --short`; every dirty file is yours or a known
> worker's (confirmed via its receipt/transcript). **Never blind-`git add -A` with workers live** —
> account for each path first (cross-ref `_RUNBOOK-git-commit.md` step 0.5).

This exact six-file situation is the worked example: `git add -A` sweeps them in (good), but only this
receipt explains what they are — the check is what makes "sweep knowingly" the rule instead of the lucky
default.

**Hardening (Dave, "it needs to be durable"):** the trail must not depend on a guessed filename. Add a
**conventioned receipt path** so the reconcile step is a fixed `ls`, not a hunt:

> Worker receipts land in **`notes/_receipts/`** (date-prefixed). `_RUNBOOK-parallel-conductor.md` worker
> step 4 + conductor step 1 name that path; the reconcile check (0.5 / 2.5 above) says "any unaccounted
> dirty path → `ls notes/_receipts/` and read the sibling transcripts (`session_info`) before committing."

Once ratified, this receipt should move to `notes/_receipts/`. I left it at the top level for now so I
don't half-establish a convention unilaterally — that's a conductor/Dave call.

**Durability status of THIS proposal:** the canonical home is the two runbooks (pending conductor). To
stop the proposal itself getting lost before then, it's also pinned in the memory index
(`feedback-worktree-reconcile-trail`) — loaded into every session, so a cold conductor can't miss that an
inscription is owed.
