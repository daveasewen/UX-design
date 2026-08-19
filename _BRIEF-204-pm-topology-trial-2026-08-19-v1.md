# Brief — the #204 PM-topology trial (ruled by Dave at #203, post-wrap)

*Cut at #203 by the FABLE conductor after Dave ruled the trial in chat. This file exists so the
topology survives the session boundary — #204's conductor reads it from the chain's queue, not
from a chat it never saw. Ruling: `s203-D2` (trial, not permanence — permanence is Dave's after
the numbers come back).*

## Dave's words (verbatim, #203 chat, 2026-08-19)

> "I like using Fable as the 'boss' and Opus as 'teams' it seems to get good results, but could
> we focus Fble on only judgment and Opus for everything else, maybe even sub-orchestration.
> Fable as the decision maker and deep thinker, Opus as PM and also Opus for team members, do
> you think that would work?" … "Lets try it out, the lossy part is interesting could we have
> two PMs, maybe specialists, or adversarial or just to compare notes, is there a strategy here
> that makes the reports, efficient, coherent and complete"

## The topology under trial at #204

- **FABLE (conductor seat): judgment only.** Rules, reads review surfaces, answers Dave, takes
  seams. Does NOT absorb raw worker reports, does NOT run reconcile mechanics.
- **OPUS BUILD-PM (one sub): orchestration.** Fires and manages the Opus worker subs, absorbs
  their receipts, runs the conductor's serial set mechanics (registries, regeneration, gate
  suite) EXCEPT inscription and anything on a DO-NOT-RULE list, and merges everything into ONE
  structured digest for Fable: a **claim table** — one row per claim, each with its evidence
  pointer (gate rc, file path, commit) and a PROVEN / MEASURED / CLAIMED / UNPROVEN tag.
- **OPUS VERIFIER-PM (one sub, adversarial): completeness and truth.** Builds nothing. Reads
  the same receipts AND the tree first-hand; its whole job is to probe the build-PM's claim
  table against the store and the repo: re-run sampled gates, grep the quoted rulings, verify
  premises (the #203 itinerary lesson, generalised). Output: a **challenge table keyed to the
  same claim IDs** — CONFIRMED / CONTRADICTED (with its own evidence) / UNTESTED (with the
  probe it would take). It is REWARDED for finding grounded contradictions, not for agreement.
- **Fable receives the JOIN** of the two tables — small, schema'd, and every disagreement is
  visible as a row, never smoothed into prose. Ruling-adjacent items reach Fable as QUOTED
  store hits, never paraphrase (`s202-D3` binds across both hops).
- **Preload sub: DECLINED, measured** — boot is ~56K of which the chain read is only ~10K;
  not worth a lossy hop. **Delegated wrap: KEPT** (proven #202, #203).
- Both PMs and all workers carry the standing fences: DO-NOT-RULE lists, git-checkout ban,
  NEW-files-only for workers, fresh-printf msgfile, step-0 premise tables.

## Why adversarial rather than twin-cooperative (the research, briefly)

Hierarchical summarisation between agent layers is known-lossy and uncalibrated; the mitigations
that hold up are structured merge over prose, and grounded critique. Debate/critic setups beat
redundant peers specifically when critiques must cite explicit facts and the judge rewards
verifiable reasoning — which is exactly this repo's existing evidence culture. Two cooperative
PMs comparing notes share blind spots and double the merge burden; a builder/skeptic split makes
the second PM's spend buy contradictions, which are the only thing Fable's seat actually needs.
Anthropic's own orchestrator-subagent research system (lead agent + parallel subagents)
outperformed single-agent by ~90% on research evals — with the noted cost that multi-agent burns
tokens fast, so the PANEL IS READ AT THE OPENER before sizing the wave, every time.

## What the trial must MEASURE (return to Dave with numbers)

1. Fable FILL end-to-end (vs #203's 70K→178K mid-session growth as the baseline).
2. Fable quota delta for the session (panel read at opener AND close).
3. Total sub spend (n= every sub, both PMs included) — the quota price of the layer.
4. Defect rate at the seam: how many CONTRADICTED rows the verifier-PM lands, and how many
   survive Fable's read (a zero-contradiction session means the verifier was toothless, not
   that the build was perfect — say so).
5. Anything a PM digest LOST that Fable later needed (the lossy-hop tally, honest).

⛔ The trial rules nothing permanent. Dave rules keep/kill/adjust on the numbers.

---

## ADDENDUM (#204, by addition): the trial RAN, the shape is ADOPTED with four amendments

Ruled `s204-D1` (Dave, #204). The four amendments (incremental claim table · fix loop inside
the build-PM's mandate · run-before-cite · verifier render lane) and the five-item
mechanisation programme are homed at `notes/_briefs/2026-08-19-204-mechanisation-programme-v1.md`
— ONE home, this is a pointer (ADR-0017). Trial numbers to Dave at the #204 wrap; the
topology's PERMANENCE verdict remains his on those numbers per `s203-D2`.
