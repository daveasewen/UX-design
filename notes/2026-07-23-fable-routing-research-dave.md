# Routing for Fable 5 — Skills, Context, Rules, Evals, Gates & Memento
*Research notes for Dave · 23 July 2026 · Verified against Anthropic primary docs where noted*
*(Filed verbatim 2026-07-23 by the chart-revisit-1 wrap session — Dave's paste, provenance: his own
research; links NOT followed in-session. Source material for the routing side-quest brief:
`notes/_briefs/2026-07-23-routing-sidequest-brief.md`.)*

## TL;DR
Yes, routing should be different for Fable — but mostly by **subtraction and configuration, not by forking content**. The documented risk with Fable 5 is not under-scaffolding, it's *inherited scar tissue*: instructions, workarounds and prescriptive steps written to compensate for older models actively degrade it. Anthropic says this outright:
> "Skills developed for prior models are often too prescriptive for Claude Fable 5 and can degrade output quality." — [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)
So the useful mental model is **three layers**:
| Layer | Contents | Route per model? |
|---|---|---|
| **Invariant** | Gates, hooks, eval acceptance criteria, memento *format* | Never. These are your trust boundary and regression detector — they must not depend on which model is running. |
| **Knowledge** | Skills, runbooks, rules/CLAUDE.md | One source of truth, written outcome-first. If you condition anything, condition the *prescriptive appendix*: older models load it, Fable doesn't. |
| **Adapter** | Effort, timeouts, verbosity nudge, autonomy framing, max_tokens, cost ceilings, task-routing thresholds | Yes — this is the legitimate per-model routing surface, and it's config, not prose. |
---
## What's actually different about Fable 5 (primary-source verified)
From the [model overview](https://platform.claude.com/docs/en/about-claude/models/overview), [migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide), [Fable 5 prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) and [announcement](https://www.anthropic.com/news/claude-fable-5-mythos-5):
- **Adaptive thinking is always on** and cannot be disabled. `thinking: {type: "disabled"}` and `budget_tokens` error out. Depth is controlled via the `effort` parameter instead. Raw chain-of-thought is never returned.
- **Effort recalibration:** "Start at high for most tasks, including workloads that ran at xhigh on Claude Opus 4.8… Lower effort settings on claude-fable-5 still perform well and often exceed xhigh performance on prior models."
- **More literal instruction following**, and steerable with brief instructions: "you can steer most behaviors with a brief instruction rather than enumerating each behavior by name."
- **Longer turns, more autonomy:** single requests can run many minutes; autonomous runs for hours. It "dispatches parallel subagents more readily than prior models" — harnesses should go async rather than block.
- **Memory affinity:** "Claude Fable 5 performs particularly well when it can record lessons from previous runs and reference them." The announcement claims persistent memory improved its performance ~3× more than it improved Opus 4.8.
- **Safety classifiers with fallback:** some requests return `stop_reason: "refusal"` (HTTP 200) and can fall back to another model; refused-before-output requests aren't billed.
- **API removals:** assistant prefill and non-default temperature/top_p/top_k are gone.
- **Reasoning-extraction refusals:** prompts/skills that tell the model to echo or transcribe its internal reasoning as output can trigger a refusal category. Cull these.
- **Same:** 1M context, 128k output, Messages API shape, tool-use patterns, prompt caching (min cacheable prefix now 512 tokens).
- **Cost:** $10/$50 per M in/out vs $5/$25 for Opus 4.8. One third-party guide ([Verdent](https://www.verdent.ai/guides/claude-fable-5-vs-opus-4-8-coding), citing Endor Labs) additionally reports ~30% higher token counts from a newer tokenizer and elevated refusal rates on security-adjacent coding — treat as practitioner report, not official.
---
## Component by component
### Model routing for tasks — keep it, sharpen the threshold
Route by **difficulty and horizon, not category**. Fable's lead grows with task length and complexity ("the longer and more complex the task, the larger Fable 5's lead"), so it earns its 2× price on long-horizon, capability-bound work: migrations, multi-hour autonomous runs, cross-file refactors, hard planning. Keep Opus 4.8 / Sonnet 5 as the default for routine, high-volume, well-fed-back work. Two extra routing inputs that didn't exist before:
1. **Effort routing is now a second axis.** Fable at `medium` may beat Opus at `xhigh` — so "route up" sometimes means *same model, more effort* and sometimes *Fable, less effort*. Cheapest adequate (model × effort) pair wins.
2. **Fallback-aware routing.** Security-adjacent work reportedly hits Fable's classifiers more often; if a task class shows elevated refusal/fallback in your logs, route it to Opus directly rather than paying Fable prices for fallback results.
### Skills — one source, prune for Fable, appendix for older models
Skills are model-blind at the platform level: no `model` frontmatter, no conditional loading, no way for a skill to ask what model it's on. So any model-conditioning is yours to build (per-model skill sets selected by your router at session setup). Before building that, do the cheaper thing:
- Rewrite skills **outcome-first**: goal, constraints, verification criteria. That version works on every model.
- Move step-by-step procedural crutches ("do X, then re-check Y, then re-read the file…") into a clearly-marked **runbook appendix**. Fable-class sessions skip it; older models get it. The [Masset piece](https://www.getmasset.com/resources/blog/fable-skills) runs this inversion deliberately — encoding Fable's working discipline (verify before claiming done, root-cause before fixing, minimal diffs) as prescriptive skills *for Opus*, precisely because Fable doesn't need them.
- Cull from all skills anything that asks the model to narrate/echo its reasoning (refusal risk on Fable) and stacked emphasis (ALL-CAPS, "IMPORTANT", triple repetition) — literal-following models overshoot on these.
- Fork a skill per model **only when evals prove** a specific model fails without the crutch.
### Rules / CLAUDE.md / context — model-agnostic, and shorter than you think
Keep one rules file, under ~200 lines (official guidance: longer files reduce adherence). The Fable-specific work is a **deletion pass**: progress-update workarounds ("summarize every 3 tool calls"), verbosity legislation, re-verification rituals, defensive repetition. The migration guide's checklist is mostly removals. If you need tight output, one brief line ("Provide concise, focused responses. Skip non-essential context.") replaces a paragraph of behavior enumeration.
### Runbooks — restructure for long turns and parallelism
For Fable: state the outcome, constraints, and *verification criteria*; permit parallel subagent dispatch; include explicit autonomy framing for unattended runs ("the user is not watching; proceed on reversible actions that follow from the request"); add scope constraints at high effort ("minimal diff, no unrequested refactoring") since that's the documented overshoot mode. Prefer fresh-context verifier subagents over "self-critique" steps. The step-enumerated version of the same runbook stays available as the older-model appendix.
### Evals — same suite everywhere, plus Fable-specific probes
Official docs are silent on cross-model eval strategy, so: run **one acceptance suite across all models** (that's your regression detector and the only honest basis for routing decisions), with per-model baselines. Add Fable-specific probes for its distinct failure modes: literal-instruction overshoot, unrequested refactoring at high effort, refusal/fallback rate by task class, and timeout behavior on long thinking turns. Re-baseline the effort ladder — your Opus-era "xhigh for hard things" rule is stale by Anthropic's own guidance.
### Gates & hooks — identical everywhere, by design
Hooks are deterministic and work the same on every model; that's the point. Do **not** relax gates for Fable because it "checks its own work" — gates exist so quality doesn't depend on model goodwill, and they're what makes model swaps safe. Legitimate per-model *harness* config here: timeout/heartbeat budgets (Fable's long thinking turns have caused per-instance timeouts in at least one practitioner's harness) and mid-run progress surfacing for long autonomous runs.
### Memento — format stays neutral; contents get an upgrade
Keep the handoff format model-neutral — that's the whole value of the system, and cross-model handoffs argue for *more* standardization, not per-model formats. But Fable changes what's worth putting in it:
1. **Lessons, not just state.** Fable benefits disproportionately from recorded lessons from previous runs — add/emphasize a "lessons learned / what didn't work" section, not just state + next steps.
2. **Evidence-pointered claims.** Adopt the documented discipline: every "done" claim in a handoff carries a pointer to the evidence (test run, command output, diff). Protects any successor model from inheriting unverified claims.
3. **Re-grounding style.** Write handoffs as re-groundings, not thread continuations: outcome first, complete sentences, no working shorthand — this is Anthropic's explicit guidance for Fable's long async work and it's good hygiene everywhere.
4. **Record model + effort used** (and any pending run state), so routing decisions are auditable against outcomes.
5. **Don't surface context-budget anxiety** in handoff/resume prompts — documented to cause premature wrap-up. Say "ample context remains" rather than quoting numbers.
6. **Route at the handoff seam.** Switching models mid-session invalidates the entire prompt cache; a fresh session on a new model pays no such penalty. Your memento handoffs are therefore exactly the right place for model routing to happen — decide the model when you open the next session, not mid-flight.
---
## Anti-patterns
- **Forking skills per model as the first move.** Prune first; fork only on eval evidence. Every fork is a sync liability.
- **Porting the old emphasis style.** Repetition and ALL-CAPS written for weaker models cause overshoot on literal followers.
- **Asking for reasoning in output.** Triggers the reasoning-extraction refusal category on Fable.
- **Weakening gates "because the model is smarter."** Gates are model-independent or they're not gates.
- **Mid-session `/model` switches.** Full cache invalidation; switch at task boundaries via handoff instead.
- **Routing everything to Fable.** 2× price (plus reported tokenizer overhead); the practitioner consensus matches Anthropic's own tiering — hybrid, with Fable reserved for work that's actually capability-bound. "The biggest reliability gains usually come from the workflow, not the model upgrade."
---
## Sources
**Official (primary, verified by direct fetch):**
[Model overview](https://platform.claude.com/docs/en/about-claude/models/overview) · [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide) · [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) · [Introducing Fable 5 & Mythos 5](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) · [Anthropic announcement](https://www.anthropic.com/news/claude-fable-5-mythos-5) · [Skills](https://code.claude.com/docs/en/skills) · [CLAUDE.md memory](https://code.claude.com/docs/en/memory) · [Hooks](https://code.claude.com/docs/en/hooks-guide) · [Model config](https://code.claude.com/docs/en/model-config) · [Subagents](https://code.claude.com/docs/en/sub-agents) · [Prompt caching](https://code.claude.com/docs/en/prompt-caching) · [Tool Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool) · [Eval development](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)
**Practitioner (secondary — attributed, not independently verified):**
[Verdent: Fable 5 vs Opus 4.8 for coding agents](https://www.verdent.ai/guides/claude-fable-5-vs-opus-4-8-coding) · [Masset: Fable Skills — teaching Opus to act like Fable](https://www.getmasset.com/resources/blog/fable-skills) · [TrueFoundry comparison](https://www.truefoundry.com/blog/claude-fable-5-vs-opus-4-8-benchmarks-pricing-when-to-use-each) · [AlphaSignal: How to actually prompt Fable 5](https://alphasignalai.substack.com/p/how-to-actually-prompt-claude-fable)
