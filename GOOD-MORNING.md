# Good morning, Dave ☕

*Session briefing — written end of 2026-07-05, session "Seaworthiness planning — sequencing the
half-finished threads." Supersedes the earlier 07-05 "Tier A batch 3" brief.
**Read this, then `_LIVE-STATE.md`, then `_SEAWORTHINESS-PLAN_2026-07-05.md`.***

## The session in one line

Pulled every OPEN / TARGET thread into **one curated, dependency-aware sequence** to get the ship
seaworthy — not a flat backlog. **The plan is set, committed, and pushed.** No building happened;
this was the sequencing session you asked for.

## The sequence (this is the plan now)

Full doc: **`_SEAWORTHINESS-PLAN_2026-07-05.md`.** In order:

1. **Hull patches — cheap, first.** Finish ingestion **Phase 0** (correction banner already in
   `_DESIGN-SYSTEM-GAPS.md`; rebuild the compliance KG to resync 39-vs-38) + **stand up the capture
   ritual** (spec in the plan).
2. **Big rock #1 — Ingestion Phase 1** (Sutherland token migration, **confirmed unblocked**): import
   modes → rebind the 147 depricates → re-verify zero refs → delete; close P1/P3/P4. Tabs first.
3. **Prove-the-core, in PARALLEL — §9 worked spread**: one screen, retrieve/extend/invent + the
   divergence probe. Independent of ingestion; validates the flexing-engine thesis.
4. **Big rock #2 — PM-KG MVP**: `_build_live_state.py` + the staleness gate (emits FUTURE/TARGET,
   flags blockers-cleared-but-still-"blocked"). Build the **capture-gate script** alongside it — same
   front-matter machinery.
5. **Finish + unify** — Phase 2 (guidelines tail; toolkit t2 on cheap model) → Phase 3 (overlay/index
   KG = ADR-0003 "done right", **§4 language-strip lives inside it**) → Phase 4 (wire coverage into
   the state machine — needs #4).

**Off the critical path (don't pick up unless you say):** D2 novel-screen (waiting on colleague) ·
toolkit tranche 2 (cheap model) · harness-modes exploration (after §9) · TOV digital-editorial
spin-off + §4b content audit · ADR-0004 ops follow-ups (EAA/EN 301 549 recheck; align
`design:accessibility-review` skill to 2.2 AA).

## What landed this session

- **KG re-verified on disk** (your "double-check first" call — it paid off). Assessment holds on
  every count (462 rules · 31/31/38 compliance · 147 depricates · Sutherland exports present). Two
  live drifts found: **Phase 0 already partly done**; **compliance KG stale by one** (39 metas vs 38
  in the 2026-06-18 graph) — a miniature of the "tracking rots silently" failure, cheap to fix.
- **The plan doc** `_SEAWORTHINESS-PLAN_2026-07-05.md` (dependency-aware sequence + next-steps +
  capture-ritual/gate spec + spin-off decision parked).
- **Capture ritual/gate decided** — ritual (refresh `_LIVE-STATE` → `GOOD-MORNING` → memory →
  supersession → commit) stands up now; the enforcing `_capture_gate.py` builds alongside the PM-KG MVP.
- **`_LIVE-STATE` OPEN entry** for the seaworthiness plan flipped ✅ DONE, pointing to the doc.

## On your desk

- **All pushed.** Commit `c0f9bd5` (seaworthiness plan + `_LIVE-STATE` pointer). Stale `.git` locks
  cleared. Nothing pending.
- Your first big-rock decision this session: **Ingestion Phase 1 leads** (my recommendation, your
  "follow your advice") — the finish-don't-add move, fully unblocked.

## Queue next (fresh session)

1. **Start the sequence: hull patches.** Finish Phase 0 (rebuild compliance KG) + stand up the
   capture ritual. Cheap, clears the deck. *Or* jump straight to Ingestion Phase 1 if you'd rather
   bank the big win first — Phase 0 is now light enough to fold in.
2. **Then Ingestion Phase 1** as its own focused session — the token migration.
3. **§9 worked spread** available to run in parallel whenever you want the divergent track.

> Next-session opener: **"Title this chat: <pick one>."** Read GOOD-MORNING → `_LIVE-STATE` →
> `_SEAWORTHINESS-PLAN_2026-07-05.md`. Everything is committed and pushed.
