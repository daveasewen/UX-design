# Good morning, Dave ☕

*Session briefing — written end of 2026-07-05, session "Decision audit — Tier A batch 2."
Supersedes the earlier 07-05 "Decision audit — Tier A batch 1" brief.
**Read this, then `_LIVE-STATE.md`, then `knowledge/README.md`.***

## The session in one line

Ran ADR-0007 §5 correctness audit **Tier A batch 2** — six nodes, fresh context, Dave adjudicating
each. Cleared the two amended-node re-audits and the remaining foundational ADRs. Tier A is now
**11/~20 audited**; every ADR (0001–0007) has a verdict.

## What landed

Six verdicts (recorded two ways per runbook §5 — ledger line in `knowledge/_DECISION-AUDIT.md`
+ state in `_LIVE-STATE`):

1. **ADR-0006 re-audit** (register dial) — **vouch.** Verified line-by-line against charter §9;
   no "cool/warm/hot" survives; spine untouched.
2. **`derivation-governance` re-audit** — **split: core vouch + mechanism defer.** Multi-human/
   staged *direction* is sound; the specific holding-pen→extension-library machinery is named-not-
   built → deferred. **Dave's future-feature captured:** tiered canon-commit access (design-system
   admin → domain admin → standard; sandbox open to all, commits tiered, extension libraries
   read-all / edit-by-domain).
3. **ADR-0001** (own our orchestration) — **vouch.** Portability/own-the-invariant principle is the
   backbone of 0002/0005/0006. (Noted: the named `harness/orchestrator.md` is archived; Dave
   vouched the principle as-written.)
4. **ADR-0002** (open standards) — **vouch.** The three-standard spine (AGENTS.md + Skills + MCP)
   is exactly how the project runs; the founding leg that survived and strengthened.
5. **ADR-0003** (knowledge-rep per stage) — **defer.** Dave reopened the scope: the *whole* DS
   corpus may be one interlinked graph. **Root cause = ingestion was never completed.** Spun off as
   a separate, audit-grade work thread (see below). Not vouched.
6. **ADR-0004** (WCAG 2.2 AA bar) — **vouch + rationale-amend.** Added the **foundational driver the
   ADR omitted**: HSBC's aspiration to be *the most digitally accessible bank in the world* — the
   bar leads, doesn't merely comply; 2.2 AA is the floor of that aspiration, not its ceiling.

**The batch's real finding:** the pattern is holding from batch 1 — no *bad* decisions, but
foundations set defensively or scoped ahead of completed work. ADR-0003's defer named the biggest
one: the KG ambition wasn't disproven, ingestion just never finished.

## On your desk

- **Committed, not pushed** — `5435b99` ("Decision audit — Tier A batch 2"). Stale `.git` locks
  cleared. **Push via GitHub Desktop.**
- **Two new work threads captured** (both in `_LIVE-STATE` OPEN, memories written):
  - **Unified DS KG + ingestion, done right** — `ds-knowledge-graph-revisit`. Own session, its own
    audit-grade method; leading hypothesis = overlay/index layer, not a monolith.
  - **Seaworthiness plan** — state + goals analysis → one prioritised sequence. Deferred *after*
    batch 3 (Dave chose to finish Tier A first).
- **New foundational memory:** `accessibility-aspiration` (most-accessible-bank; bar leads, ratchets).

## Queue next (fresh session) — FOCUS: finish Tier A

1. **Tier A batch 3 — decision audit (THE task).** **Charter §4 (ratified curbs) + §4b (tone/
   temperature)**, plus any `_LIVE-STATE` LIVE entry not yet covered by an ADR/§9 (triage: two
   harness modes, supersession discipline, git split, build gate — some may drop to Tier B). Same
   protocol: fresh context, dossier + devil's-advocate + recommendation per node, Dave adjudicates,
   record at ruling-time. Runbook: `knowledge/_RUNBOOK-decision-audit.md`; ledger:
   `knowledge/_DECISION-AUDIT.md`. **This closes Tier A** ("KG stops laundering its load-bearing
   claims"). **Never run in a loaded session.**
2. **Then: seaworthiness planning session** — the state+goals curation Dave asked for.
3. Standing/parallel: DS-KG + ingestion thread · PM-KG MVP · D2 novel-screen (waiting on colleague)
   · toolkit tranche 2 (cheap model).

Two small operational follow-ups parked from ADR-0004 (not audit nodes): verify current EAA /
EN 301 549 legal position; align the `design:accessibility-review` skill (audits to 2.1 AA) to the
2.2 bar.

> Next-session opener: **"Title this chat: <pick one>."** Read GOOD-MORNING.md → `_LIVE-STATE.md`
> → `knowledge/README.md`. Everything is committed; push `5435b99` via Desktop.

## The meter

Batch 2 did the job batch 1 designed: fresh context, a written case *against* each node, and honest
outcomes — including one **defer** that surfaced the real root cause (incomplete ingestion) rather
than papering it, and one **rationale-amend** that put the actual foundational reason (the
accessibility aspiration) back into ADR-0004. Two nodes to go and Tier A is clean.
