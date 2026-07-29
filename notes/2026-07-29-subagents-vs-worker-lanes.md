# Sub-agents vs worker lanes — the distinction this project has never drawn

```
provenance: local_50165c15-d8e2-4038-b812-41f702fa1347 · 2026-07-29
status: floated
```

**Register: FLOATED — nothing ruled, nothing enacted.** Path per **ds-017**: this note + one
`_FUTURE-STATE.md` entry, same commit, **no GM/§C edit** — §C is over its warn cap and this is
unruled. ⚠ **Written by #35 AFTER its wrap, while #36 was already open**, so it deliberately
touches no file #36 is likely to be authoring. **It therefore has no standing home and will not be
read unless someone gives it one** — the dated-home problem, declared rather than hidden.

**Origin:** Dave, 2026-07-29, after #35's wrap: *"we never had the chat about sub-agents."*

---

## 1. The two things both called "sub-agents", and only one is modelled

| | **worker lane** | **in-session sub-agent** |
|---|---|---|
| what it is | a separate session/window running a briefed slice | an agent spawned inside the current window |
| context | its own, and it keeps it | its own, and it is **discarded** |
| what comes back | files + a commit + a receipt | **a message** |
| project support | `_lanes.json` · `_RUNBOOK-parallel-conductor.md` · `lane_routing_check` BLOCKING · conductor-commits rule · DIVVY PLAN in the handoff | **none — no lane entry, no receipt convention, no routing rule, nothing in the capture ritual** |
| proven | yes (2026-07-21; #33 ran one Sonnet lane with a receipt) | never tried here |

*(Left column from the record + memory; verify the exact filenames before relying on them.)*

**The whole point of the distinction:** a worker lane hands back **artefacts you can verify**.
A sub-agent hands back **prose you cannot.** Everything else in this repo is checked against a real
run, a commit hash or a file — and #29→#35 is a seven-session streak of *a claim about repo state is
verified against `git log`, never against a banner*. **A sub-agent's report is structurally a
banner.** That is not a reason to refuse them; it is the design constraint any adoption has to meet.

## 2. Why it is nevertheless interesting, and it comes straight out of #35

#35 spent six rounds trimming its own handoff to clear a size gate — work that consumed the very
window whose quality it was protecting. In the doctrine already inscribed in
`notes/2026-07-28-memento-jit-context-research.md` — **context receives conclusions, not working** —
that is textbook: the trimming *working* did not need to be in this context, only its *conclusion*
(a number and a diff).

So the shape worth exploring is narrow and specific: **a sub-agent is a way to buy a context window
without buying a session.** Same weekly allowance, fresh 200k, conclusion returned.

## 3. The measured floor, from today

#35 offered a Sonnet worker lane at the opener and never opened one. Retrospectively:

- a lane costs **a brief + a receipt + a reconcile** ≈ **4–6 points** of the conductor's window
  before it saves anything;
- #35's whole build was ~12 points.

⇒ **Below roughly 15 points of mechanical work, delegation loses.** ⚠ **This is one observation,
not a constant** — exactly the n=1 the throttle programme keeps being burned by (`TAPE_TO_BILL` is
still PROVISIONAL at n=2). Do not let this number into a table as a fact.

## 4. The three questions, none of which #35 can answer

1. **What is the receipt?** A sub-agent reporting *"done, 3,431 tape"* is a banner. Candidate
   answer: a sub-agent may only be trusted for work whose **output is a file or a run** the parent
   then verifies itself — i.e. it may do the *working*, never the *judging*. That is a strong
   constraint and probably the right one.
2. **What is the threshold, and whose number is it?** Dave's, from measurement — same posture as
   `DEFER_STREAK`, which is sitting AGENT-PROPOSED right now precisely so a number nobody ruled
   cannot read as a ruling.
3. **How does it interact with PACE?** Sub-agents burn **allowance** faster than they burn
   **window**. At the 2026-07-29 reading (all models 69% consumed vs ~71% elapsed = on pace;
   **Fable 82% = ahead**) that trade is not free. Behind pace it is nearly free. **The pace check
   in `_RUNBOOK-context-gauge.md` § THE THIRD TIER already decides this** — it just has never been
   applied to a delegation decision.

## 5. ⚠ The failure mode to watch, named in advance

This is the exact shape of thing that produces **an instrument with no consumer** (ds-024) or
**a door with no granularity** (#33): satisfying to build, plausible-sounding, and unmeasured.
**The honest prerequisite is already queued: MEASURE THE BOOT.** If ~17 points of every window is
fixed overhead, that single number decides whether spawning a fresh context is cheap or ruinous —
and no session in this project has ever measured it.

⇒ **Recommendation: do not rule sub-agents until the boot is measured.** The measurement is the
input; everything above is speculation without it.

**Links:** `notes/2026-07-28-memento-jit-context-research.md` (same doctrine, applied to tools) ·
`_DECISION-HISTORY/2026-07-29-reading-the-usage-series.md` § 6 (the trimming that motivated this) ·
`knowledge/_RUNBOOK-context-gauge.md` § ★★ THE THIRD TIER (pace) ·
`_RUNBOOK-parallel-conductor.md` (the modelled half).
