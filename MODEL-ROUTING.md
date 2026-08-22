# MODEL-ROUTING — which model for which work

> Operating reference: name a session's work, get its model. Consulted at session start
> (per the session-title ritual) and used as the **delegation rule** inside a session.
> Supersedes the `model-selection-by-phase` memory (now points here). Audited 2026-07-23 against
> the Fable-era routing research (sheet: `reviews/ROUTING-AUDIT-2026-07-23-v1.html`; all 13
> proposals ratified by Dave same session) — still Dave's to tune.
> *Last updated: 2026-08-21 #212 `s212-D12` (routing currency check against live Anthropic docs,
> four weeks on — P1–P7, P9, P10 applied: model strings pinned across all four tiers, the effort
> ladder corrected to five rungs, the classifier-routing destination corrected [Opus 5 also runs
> classifiers now], and the tokenizer-overhead figure corrected. P8 — the rule-5 verification
> conflict — RULED `s215-D3` 2026-08-22 at reading 2, rule 5 now model-conditional; was
> deliberately left open at #212, Dave's call, not a sub's). Prior: 2026-07-30 #48 (Default
> tier corrected `Opus 4.8` → `Opus 5` — open 20 (a), Dave's ruling; see the staleness note under
> the table). Prior: 2026-07-25 (budget-aware routing governor added — Dave's proposal, reflected
> back + confirmed "good call") · 2026-07-23 (routing-audit #6 + #12: Fable-era notes · Mode 2 →
> deliberate · mid-session-switch anti-pattern).*

## The tiers (Dave's real economy)

| Tier | Model | When | Notes |
|---|---|---|---|
| **Premium — rationed** | **Fable** | Big, high-stakes, hands-off jobs where a mistake across the whole scope is costly and you can't babysit it — "I need to trust this." | Most-trusted, but dear. Spend it where high-trust-*at-scale* actually pays; not the daily driver. `claude-fable-5` · $10/$50 per MTok · on Pro/Max/Team plans it draws on **usage credits**, not the standard weekly allowance (Anthropic, 1 Jul 2026). Rationing is a billing fact, not just a habit. *(added `s212-D12`, 2026-08-21, P1)* |
| **Default — complex** | **Opus 5 · high** | Judgment, architecture, sequencing, audits, critique, governance, ambiguous or irreversible calls, reviews. | The workhorse. Your default for anything that needs thinking. Exact API string `claude-opus-5`. *(added `s212-D12`, 2026-08-21, P2 — see the staleness note below, now independently confirmed)* |
| **Throughput — to a plan** | **Sonnet** | Execute a known runbook/spec: gates, metas, snippets, token rebinds, ingestion tranches, refactors to spec. | The judgment is already made; you need reliable execution. Saves Opus budget. Exact API string `claude-sonnet-5` · $2/$10 per MTok · 1M context · prompt-cache minimum **1,024 tokens** (not 512 — that's Opus/Fable/Mythos only). *(added `s212-D12`, 2026-08-21, P3)* |
| **Chore — mechanical** | **Haiku** | Doc-drift fixes, find/replace, formatting, renames, gate-count sweeps, index bumps. | No judgment involved — never pay more than you must. Exact API string `claude-haiku-4-5-20251001` · $1/$5 per MTok · 200k context · cache minimum 4,096 tokens · **no adaptive thinking, no `xhigh`, no `max`** — this tier behaves categorically differently from the other three. Watch date: tentative retirement not sooner than **15 October 2026**, roughly eight weeks out as of this writing. *(added `s212-D12`, 2026-08-21, P3)* |

*The Fable↔Opus and Sonnet↔Haiku boundaries are yours to calibrate from experience; the roles are the fixed part, not the exact model on each line.*

> ⚠ **STALENESS CORRECTED 2026-07-30 #48, on Dave's ruling — open 20 (a).** The Default tier read
> **"Opus 4.8 · high"** for an unknown number of sessions while sessions were in fact running
> `claude-opus-5`; **#47 announced its routing at the opener off that table**, which is the whole
> cost of the defect — a routing announcement is one of the first things Dave reads, and it was
> sourced from a stale cell. ★ **The mechanism, and it is the reusable part: a VERSION NUMBER in
> this table is a claim with an expiry date, and the sentence directly above is what let it sit** —
> "not the exact model on each line" reads as licence for the cell to be approximate, so nothing
> ever chased it. **The ROLES are canon here; the model strings are a snapshot.** ⇒ Treat a version
> number in this file the way the gate treats a size stamp: it is a measurable claim, and if you
> notice it is wrong, correct it at source rather than routing around it
> [[assertion-propagation-gap]]. **Unfixed in the same class: the two amber edges and the
> "Measured, adjustable." annotation — open 20 (b) and (c), both still Dave's.**
>
> **ADDED `s212-D12`, 2026-08-21 (P2) — the correction is now independently confirmed, not just
> ruled.** Claude Opus 5 was announced 24 July 2026, one day after the 2026-07-23 research was
> filed. The live models overview names it the recommended starting point: "If you're unsure which
> model to use, start with Claude Opus 5." Sources fetched 2026-08-21:
> `anthropic.com/news/claude-opus-5` and `platform.claude.com/docs/en/about-claude/models/overview`.
> A ruling that started as Dave's word now also has a receipt.

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
  **CORRECTED `s212-D12`, 2026-08-21 (P6) — the Cowork observation and the 2026-07-24 correction
  above are untouched, both are OBSERVED facts about this environment and no doc speaks to them;
  only the API half moves.** The ladder is now **five rungs**: `low · medium · high · xhigh · max`
  — `max` is new since July ("absolute maximum capability with no constraints on token spending").
  `high` is the API default and is identical to omitting the parameter. There is now a dedicated
  page, `build-with-claude/effort`, with per-model recommendations. **For Fable:** start `high`,
  `xhigh` for capability-sensitive work, step down to `medium`/`low` for routine. **For Opus 5:**
  start `high`, and — quoted, because it bears on the habit of carrying settings across model
  generations — "If you carried effort settings over from an earlier model, run a fresh effort
  sweep on your evals rather than reusing them." (Sources: `build-with-claude/effort`,
  migration-guide, both fetched 2026-08-21.)
- **Diagnose before attributing a failure to safety classifiers.** Our one logged "refusal"
  (Playwright, 07-22) was a misdiagnosis of an installer's expected exit
  (`_RUNBOOK-render-verify.md`). Fallback-aware routing (route classifier-prone task classes to
  Opus) only ever acts on DIAGNOSED refusals, not pattern-matched ones.
  **CORRECTED `s212-D12`, 2026-08-21 (P4) — the diagnose-first discipline above stands unchanged,
  it was right and it caught a real misdiagnosis; only the destination is wrong now.** Claude
  Opus 5 also ships safety classifiers: "Claude Fable 5 and Claude Opus 5 include safety
  classifiers that can decline a request" (refusals-and-fallback page, fetched 2026-08-21). "Route
  it to Opus" is no longer automatically a classifier-free destination — it depends which Opus.
  Anthropic's own default fallback target for Fable's `cyber` category is **Opus 4.8**, not Opus 5.
  A diagnosed classifier refusal on Fable routes **down a generation, not sideways**.
  **ADDED `s212-D12`, 2026-08-21 (P5) — name the category, don't pattern-match it.** The refusal
  categories are published and named: `cyber`, `bio`, `frontier_llm`, `reasoning_extraction`,
  `general_harms` — a refusal reports which one fired in `stop_details.category`. A named API
  category is a diagnosis; "felt security-adjacent" is a pattern-match, and canon's own rule is
  that a diagnosis must be diagnosed. **Freshness warning:** refusal *rates* move — Anthropic
  tightened the cyber classifier 1 July 2026 and explicitly accepted more false positives on
  "routine coding and debugging tasks," then relaxed biology 7 August 2026, cutting bio fallbacks
  by about 85%. A refusal-rate observation is stale within weeks; the category name is the durable
  part, the rate is not.
- **Fable is now a spawnable subagent target** in Cowork's Agent tool (OBSERVED 2026-07-23) —
  rule 5's peer-or-stronger verification can be satisfied with a fresh-context Fable subagent
  when the session itself runs on Fable.
- **ADDED `s212-D12`, 2026-08-21 (P10) — the ~30% tokenizer-overhead figure that shadowed Fable's
  price tag is corrected, and the practitioner claim behind it is demoted.** The 2026-07-23
  research carried a practitioner report (Verdent, not official) of ~30% higher token counts on
  Fable from a newer tokenizer. The official migration guide **contradicts this as a Fable-vs-Opus-
  4.8 delta**: "Token counts are roughly unchanged because the models use the same tokenizer." The
  ~30% figure is real, but it is the delta versus models **before Opus 4.7** — a cost already paid
  generations ago, not one Fable adds. **Fable's true premium over Opus 4.8 is 2× per token and
  nothing more; over Opus 5, also 2×.** No inflated tokenizer surcharge belongs in any Fable-vs-
  Opus cost comparison. (Source: migration-guide, fetched via curl 2026-08-21, size-cap route.)

## The rules (matter more than the table)

1. **Default down, escalate up.** Start at the cheapest tier that fits; jump up the instant you hit a real judgment call. This *is* the meter ruling, made operational.
2. **Model never moves judgment.** Promotion to canon and "vouched" are Dave's, regardless of which model ran (`derivation-governance`). Cheap models draft; the human decides.
3. **Declare + record the model.** The handoff names the session's work — add the model. Record which model produced any generated artifact (the Sonnet-vs-Opus spread proved model is a real variable; the trace/audit want the provenance).
4. **In experiments, model is a variable.** When testing the engine (e.g. the calibration run), pick the model on purpose and change **one thing at a time** (the 2026-07-05 confound was model + rule changed together).
5. **Verify with a peer-or-stronger model — MODEL-CONDITIONAL since `s215-D3` (P8 ruled, 2026-08-22).** Adversarial checks or critique of a strong model's output use equal-or-stronger — never audit Opus judgment with Haiku. **Scope ruled at reading 2:** the adversarial verifier (a *different seat* auditing the work) STAYS for Fable-run and high-stakes work; routine "re-check your own work" self-verification scaffolding COMES OFF Opus 5 sub briefs, per Anthropic's own Opus 5 guidance ("do not use subagents to verify or double-check your own work") — adversarial audit and self-verification are different acts, and only the second is redundant on Opus 5.
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
  **ADDED `s212-D12`, 2026-08-21 (P9) — the ruling stands, and the live docs now corroborate it
  from the Default tier's own model, not just Cowork economics.** The doc evidence cuts both ways
  by model: the Fable guide pushes the other way ("Use subagents frequently… prefer asynchronous
  communication between orchestrator and subagents over blocking"), but the Opus 5 guide pushes
  Dave's way — "Delegate to a subagent only for large tasks that are genuinely independent and
  parallelizable… Do not delegate work you can finish yourself in a handful of tool calls… keep
  spawn counts low" (fetched 2026-08-21). Since Dave's Default tier is Opus 5, this is
  model-appropriate as well as environment-specific — worth saying so, since the ruling previously
  read as purely a Cowork-cost artifact.
- **Mode 3 — handoff pre-selects the next model.** `GOOD-MORNING.md` ends with "next session = <work> → <model>", so cold-start the choice is already made (you still action it via the selector). **Anti-pattern (inscribed 2026-07-23, audit #6c; broadened `s212-D12`, 2026-08-21, P7): never switch model or effort mid-session** — it invalidates the whole prompt cache (REPORTED, migration-guide era, for the model half; now also officially documented for effort — "Because effort shapes the rendered prompt, changing it between requests does not preserve cached prefixes from earlier turns; if you rely on prompt caching across a long session, pick an effort level at the start and keep it constant," `build-with-claude/effort`, fetched 2026-08-21) and Cowork can't do it anyway; the handoff seam IS the routing point for both model and effort now.

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
