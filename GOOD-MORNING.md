# Good morning, Dave ☕

*Session briefing — written end of 2026-07-05, session "From provenance to project-memory: the
decision-graph turn." Supersedes the 07-04 "Flexing engine / inference-ramp / review instrument"
brief. **Read this, then `_LIVE-STATE.md` (new — the live/dead/open ledger), then
`knowledge/README.md`.***

## The session in one line

Started tightening the register's provenance (§9a) and turned up a deeper bug — a cold start had
been reasoning from a *retired* artifact — which reframed the whole session into **fixing how the
project remembers itself**: a supersession discipline, a temporal decision-graph (ADR-0007), a
`_LIVE-STATE` spine that successive sessions inherit, and a guard so the graph can't launder
unaudited decisions as vetted.

## What landed

1. **§9a — provenance of "reads HSBC."** The register's vibe-terms were de-anchored (drifting to
   the model's priors). Decomposed into named sources — character → `brand-principles.md` (the
   six principles), the pointer §9 was missing — plus a per-band **Brand-source stop** column and
   **flag-where-silent** as an advisory behaviour. Record: `knowledge/_PROVENANCE-inference-levels_2026-07-04.md`.

2. **Two harness modes (§9a).** Your reframe: converge/ship = **mode B** advisory brand self-check
   (ADOPTED) · explore/noodle = **mode A** open human gestalt (OPEN). **Mode is a first-class
   harness dial**, mapping onto the flexing engine's floor/ceiling. Memory: `harness-two-modes`.

3. **Context-rot root cause found + fixed.** A cold start resurrected the retired looks-based
   register dial (`sme-payments-registers.html`) — root cause = **an unrecorded supersession
   edge**. Fixes: tombstone banner on the dead artifact; **supersession discipline** now
   non-negotiable in `AGENTS.md`; live-vs-dead state in memory.

4. **ADR-0007 — project memory as a temporal decision-graph, lightweight-first.** Desk research
   (Graphiti/Zep bitemporal `t_valid→t_invalid`; ADR-as-KG / OIDA supersession; OpenLineage
   lineage). Edges as front-matter → generated `_LIVE-STATE` → advisory staleness gate → Graphiti
   as the graduation path. Load-bearing lesson: *the graph is a view over well-recorded edges; the
   ruling-time edge discipline prevents rot, not the storage.*

5. **`_LIVE-STATE.md` — the state-retention spine.** Seeded live/dead/open ledger, wired into the
   cold-start sequence (**GOOD-MORNING → `_LIVE-STATE` → `knowledge/README`**). Interim/hand-kept
   until the generator exists.

6. **Anti-laundering guard (ADR-0007 §5) — your catch.** Validity ≠ provenance. Every node carries
   a validation state (`unaudited → vouched`) *separate* from lifecycle; the backlog seeds
   **`unaudited`**; promotion = **human audit only, never derived**; the staleness gate enforces
   consistency, never validity.

7. **Git mechanism ruled.** Claude commits in terminal + clears stale `.git/*.lock`; **Dave pushes
   via GitHub Desktop only** (terminal push hangs on creds). Supersedes the 07-02 terminal-only
   ruling. In `AGENTS.md` + memory `git-push-method`.

## On your desk

- **Push before you close** — `master` is **ahead 3** (`8dbfbc4`, `7e6f024`, `a6d6ce0`) via Desktop.
- **⚠️ The whole decision corpus is `unaudited`.** The KG now retains state, but nothing in it has
  been checked for *correctness*. That's the open risk you named.

## Queue next (fresh session)

1. **Decision-corpus correctness audit — THE priority.** The guard against baking bad decisions in.
   First task = **design the audit method** (batched, fresh-context, you as judge; reuse
   `_REVIEW-QUEUE` tiering + `_CONFIDENCE` states). Then run it in batches. Do NOT attempt in a
   loaded context.
2. **`_build_live_state.py` + staleness gate** — make the ledger self-generating (ADR-0007 MVP).
3. **Divergence probe** — still parked behind the *missing inference-era spread*; and the
   propagation gap (vision/ADR-0006/iteration-machine still speak looks vs §9 inference) is unresolved.
4. **D2 novel-screen test** — the #1 external unlock, still waiting on the colleague's brief.
5. Parallel: toolkit tranche 2 (Dropdowns) on a cheap model.

> Next-session opener: **"Title this chat: <pick one>."** Read GOOD-MORNING.md, then `_LIVE-STATE.md`,
> then `knowledge/README.md`. Everything today is committed; push the pending 3 via Desktop.

## The meter

This was the session the project got a spine for its *own* memory — the same recursion that made
the design system self-validating, now pointed at the project's decisions. The tell that it's
working: we caught the rot mid-session, turned it into governance (a discipline + a ledger), and
then caught the *next* trap before building it — that a graph launders unaudited decisions. The
real next move is a **conversation-light, judgment-heavy audit**, run fresh, in batches — not more
docs.
