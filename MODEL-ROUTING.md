# MODEL-ROUTING — which model for which work

> Operating reference: name a session's work, get its model. Consulted at session start
> (per the session-title ritual) and used as the **delegation rule** inside a session.
> Supersedes the `model-selection-by-phase` memory (now points here). Audited 2026-07-23 against
> the Fable-era routing research (sheet: `reviews/ROUTING-AUDIT-2026-07-23-v1.html`; all 13
> proposals ratified by Dave same session) — still Dave's to tune.
> *Last updated: 2026-07-25 (budget-aware routing governor added — Dave's proposal, reflected back +
> confirmed "good call"). Prior: 2026-07-23 (routing-audit #6 + #12: Fable-era notes · Mode 2 → deliberate
> · mid-session-switch anti-pattern).*

## The tiers (Dave's real economy)

| Tier | Model | When | Notes |
|---|---|---|---|
| **Premium — rationed** | **Fable** | Big, high-stakes, hands-off jobs where a mistake across the whole scope is costly and you can't babysit it — "I need to trust this." | Most-trusted, but dear. Spend it where high-trust-*at-scale* actually pays; not the daily driver. |
| **Default — complex** | **Opus 4.8 · high** | Judgment, architecture, sequencing, audits, critique, governance, ambiguous or irreversible calls, reviews. | The workhorse. Your default for anything that needs thinking. |
| **Throughput — to a plan** | **Sonnet** | Execute a known runbook/spec: gates, metas, snippets, token rebinds, ingestion tranches, refactors to spec. | The judgment is already made; you need reliable execution. Saves Opus budget. |
| **Chore — mechanical** | **Haiku** | Doc-drift fixes, find/replace, formatting, renames, gate-count sweeps, index bumps. | No judgment involved — never pay more than you must. |

*The Fable↔Opus and Sonnet↔Haiku boundaries are yours to calibrate from experience; the roles are the fixed part, not the exact model on each line.*

## Fable-era notes

> **CORRECTION 2026-07-24 (Dave, OBSERVED in-session, via the chart-line worker receipt):** effort
> **IS manually selectable per session in Cowork** — this supersedes the routing-audit #8 line
> "no per-spawn effort control" for *sessions* (the Agent-tool spawn limitation stands). Divvy
> plans may name model **and effort** per lane; the knob is Dave's, set at window-open. (routing audit 2026-07-23, ratified #6)

- **Route by difficulty × horizon, not category.** Fable's lead grows with task length and
  complexity (VERIFIED, Fable prompting guide) — a long ambiguous multi-file job earns Fable; a
  hard-but-short judgment call is still Opus territory.
- **Effort is a real second axis at the API but NOT controllable in Cowork** (OBSERVED 2026-07-23):
  no top-level effort knob; it exists only in agent-definition frontmatter. Record effort where
  known (handoff/receipt header slot, #8); don't build routing logic on the missing knob. This
  section pays off on a move to Code.
- **Diagnose before attributing a failure to safety classifiers.** Our one logged "refusal"
  (Playwright, 07-22) was a misdiagnosis of an installer's expected exit
  (`_RUNBOOK-render-verify.md`). Fallback-aware routing (route classifier-prone task classes to
  Opus) only ever acts on DIAGNOSED refusals, not pattern-matched ones.
- **Fable is now a spawnable subagent target** in Cowork's Agent tool (OBSERVED 2026-07-23) —
  rule 5's peer-or-stronger verification can be satisfied with a fresh-context Fable subagent
  when the session itself runs on Fable.

## The rules (matter more than the table)

1. **Default down, escalate up.** Start at the cheapest tier that fits; jump up the instant you hit a real judgment call. This *is* the meter ruling, made operational.
2. **Model never moves judgment.** Promotion to canon and "vouched" are Dave's, regardless of which model ran (`derivation-governance`). Cheap models draft; the human decides.
3. **Declare + record the model.** The handoff names the session's work — add the model. Record which model produced any generated artifact (the Sonnet-vs-Opus spread proved model is a real variable; the trace/audit want the provenance).
4. **In experiments, model is a variable.** When testing the engine (e.g. the calibration run), pick the model on purpose and change **one thing at a time** (the 2026-07-05 confound was model + rule changed together).
5. **Verify with a peer-or-stronger model.** Adversarial checks or critique of a strong model's output use equal-or-stronger — never audit Opus judgment with Haiku.
6. **Fresh context pairs with the "decide" tier.** Judgment/audit sessions run cold *and* on Opus.

## Budget-aware routing governor (added 2026-07-25, Dave's proposal)

A **two-sided** control layered on top of rule 1 — spend the least tier that fits, **and** don't let the
weekly allowance go unused. The lever is **pace**, not gut feel.

- **Pace = spend-so-far ÷ even-pace**, where even-pace ≈ **14.3%/day** of the weekly allowance (100% ÷ 7).
  A read >1.0 = ahead of budget for the day-of-week; <1.0 = behind.
- **Under pace (surplus)** → bias **up** a tier where a call is genuinely close, and **pull deferred
  quality work forward** — the backlog that always slips when budget is tight: render-verify, the standing
  eyeball set, Fable adversarial audits, memory/GM compactions. Surplus is meant to be *spent on quality*,
  not banked to expiry.
- **Over pace / late in the week** → bias **down**; protect the reserve so the week finishes clean. Step
  down at the **handoff seam**, never mid-session (that invalidates the cache — see Mode 3).
- ⚠ **No live usage meter in this environment — Dave supplies the number** (same reason the context gauge
  is a hand-estimate). The governor only runs when a real % is in hand; absent that, fall back to plain
  rule 1 (default down, escalate up).

*It nudges the boundary, it doesn't rewrite the roles:* a hard judgment call is still Opus even under
pace; a mechanical chore is still Haiku even with surplus. The governor decides which way to lean when a
call is close, and which deferred quality work to greenlight.

## How it runs in practice (there is no auto-fork)

A chat runs on **one model**; it changes only when you deliberately `/model`. Nothing silently reclassifies the task and switches you (which, for cost control, is a feature). So this file is a **lookup, not a router** — three ways to use it, in increasing automation:

- **Mode 1 — session lookup (default, zero infra).** Name the work → this table → set the model. **Surface caveat (2026-07-13):** `/model` is a slash command in **Claude Code** only; in **Cowork** the `/` menu is a **file/skill picker**, so there's no `/model` — set the model via the app's model selector if surfaced, or lean on Modes 2 + 3. (Portable win: this file pays off more on a move to Code.)
- **Mode 2 — in-session delegation: DELIBERATE, not default (re-ruled Dave 2026-07-23, routing
  audit #12 — ⚠️ SUPERSEDES the 2026-07-13 "default-on" ruling).** The Cowork environment
  now names agent spawning the *expensive* path (each spawn cold-starts and re-derives context) —
  the 07-13 economics inverted. Delegate down to a subagent only when: the **divvy plan says so**,
  **Dave asks**, or a subagent is the only way to keep the main window clean (e.g. the out-of-band
  gauge read). Throughput's real carrier is the **parallel worker-chat model with divvy plans**
  (`_RUNBOOK-parallel-conductor.md`) — proven at scale 07-19 → 07-22. Say so when you delegate,
  as before.
- **Mode 3 — handoff pre-selects the next model.** `GOOD-MORNING.md` ends with "next session = <work> → <model>", so cold-start the choice is already made (you still action it via the selector). **Anti-pattern (inscribed 2026-07-23, audit #6c): never switch model mid-session** — it invalidates the whole prompt cache (REPORTED, migration-guide era) and Cowork can't do it anyway; the handoff seam IS the routing point.

**Biggest saving for Dave specifically (re-weighted 2026-07-23):** manual switching is hard in Cowork, so **Mode 3 + the parallel worker-chat model carry the weight** — route at the handoff seam, run throughput lanes on cheap models per the divvy plan, and reserve Fable for genuinely big high-trust jobs. Mode 2 subagents are the exception tool, not the standing lever (see the supersession note above).

## Worked pattern — scope once (expensive brain), run at scale (trusted hands)

The highest-leverage shape for a **big repetitive job** (e.g. verifying all 27 unverified `verified_by`
edges): **Opus writes the brief + spec** — which items qualify, how each check works, the pass bar, the
output format, the edge cases — and then **one model rattles through the whole batch against that spec**.
**The spec is the hinge:** it converts an exploratory judgment problem into a hands-off execution one.

- **Who runs the batch is set by STAKES, not size.** High-stakes-at-scale — a mistake across the whole
  scope is costly and you won't review each item — → **Fable**, one confident sweep. Mechanical and
  cheaply re-checkable — e.g. a build gate re-tests every wired check, so a slip is caught anyway — →
  **Sonnet**. Reach for Fable when the spec is subtle and you want to trust the entire pass; Sonnet when
  the safety net already exists.
- **The guardrails still hold** (rules 2 + 5): the executor never self-promotes its output — **Opus or
  Dave vouches it** — and any adversarial check uses a peer-or-stronger model, never a weaker one.
- **Mnemonic:** *expensive brain scopes it once, trusted hands run the scope* — Opus writes **a mini
  brief for the brief** (Dave's phrase): the spec IS a brief, produced by the pricey model, that the
  batch model then executes against.

*Recorded 2026-07-19 (Dave, from the compliance-edges routing discussion).*

## Entry points
`AGENTS.md` (How to work → model routing) · the session-title / capture ritual · memory `model-selection-by-phase`.
