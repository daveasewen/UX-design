# MODEL-ROUTING — which model for which work

> Operating reference: name a session's work, get its model. Consulted at session start
> (per the session-title ritual) and used as the **delegation rule** inside a session.
> Supersedes the `model-selection-by-phase` memory (now points here). Unaudited — Dave's to tune.
> *Last updated: 2026-07-13.*

## The tiers (Dave's real economy)

| Tier | Model | When | Notes |
|---|---|---|---|
| **Premium — rationed** | **Fable** | Big, high-stakes, hands-off jobs where a mistake across the whole scope is costly and you can't babysit it — "I need to trust this." | Most-trusted, but dear. Spend it where high-trust-*at-scale* actually pays; not the daily driver. |
| **Default — complex** | **Opus 4.8 · high** | Judgment, architecture, sequencing, audits, critique, governance, ambiguous or irreversible calls, reviews. | The workhorse. Your default for anything that needs thinking. |
| **Throughput — to a plan** | **Sonnet** | Execute a known runbook/spec: gates, metas, snippets, token rebinds, ingestion tranches, refactors to spec. | The judgment is already made; you need reliable execution. Saves Opus budget. |
| **Chore — mechanical** | **Haiku** | Doc-drift fixes, find/replace, formatting, renames, gate-count sweeps, index bumps. | No judgment involved — never pay more than you must. |

*The Fable↔Opus and Sonnet↔Haiku boundaries are yours to calibrate from experience; the roles are the fixed part, not the exact model on each line.*

## The rules (matter more than the table)

1. **Default down, escalate up.** Start at the cheapest tier that fits; jump up the instant you hit a real judgment call. This *is* the meter ruling, made operational.
2. **Model never moves judgment.** Promotion to canon and "vouched" are Dave's, regardless of which model ran (`derivation-governance`). Cheap models draft; the human decides.
3. **Declare + record the model.** The handoff names the session's work — add the model. Record which model produced any generated artifact (the Sonnet-vs-Opus spread proved model is a real variable; the trace/audit want the provenance).
4. **In experiments, model is a variable.** When testing the engine (e.g. the calibration run), pick the model on purpose and change **one thing at a time** (the 2026-07-05 confound was model + rule changed together).
5. **Verify with a peer-or-stronger model.** Adversarial checks or critique of a strong model's output use equal-or-stronger — never audit Opus judgment with Haiku.
6. **Fresh context pairs with the "decide" tier.** Judgment/audit sessions run cold *and* on Opus.

## How it runs in practice (there is no auto-fork)

A chat runs on **one model**; it changes only when you deliberately `/model`. Nothing silently reclassifies the task and switches you (which, for cost control, is a feature). So this file is a **lookup, not a router** — three ways to use it, in increasing automation:

- **Mode 1 — session lookup (default, zero infra).** Name the work → this table → set the model. **Surface caveat (2026-07-13):** `/model` is a slash command in **Claude Code** only; in **Cowork** the `/` menu is a **file/skill picker**, so there's no `/model` — set the model via the app's model selector if surfaced, or lean on Modes 2 + 3. (Portable win: this file pays off more on a move to Code.)
- **Mode 2 — in-session delegation (the cost lever). ✅ DEFAULT-ON, mention each time (ruled Dave 2026-07-13).** Keep the session on your judgment model (Opus) and **delegate the chore/throughput sub-tasks down** to Haiku/Sonnet *subagents* — they do the grunt work and return into the same chat, no fork, no lost context. This is what stops a default-Opus session from paying premium rates to do a find-and-replace, and it needs **no manual switch** — which matters because Mode 1 is awkward in Cowork. The orchestrating agent follows this file as the delegation rule and says when it delegates.
- **Mode 3 — handoff pre-selects the next model.** `GOOD-MORNING.md` ends with "next session = <work> → <model>", so cold-start the choice is already made (you still action it via the selector).

**Biggest saving for Dave specifically:** you default to Opus for complex work, and manual switching is hard in Cowork — so **Modes 2 + 3 carry the weight**: Mode 2 (auto-delegate the donkey work off Opus) saves more than any clever switching, and reserving Fable for genuinely big high-trust jobs keeps the premium spent where it pays.

## Entry points
`AGENTS.md` (How to work → model routing) · the session-title / capture ritual · memory `model-selection-by-phase`.
