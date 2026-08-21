# Routing currency check — 2026-08-21

*Desk research, session #212. Proposal-only: nothing here is enacted and nothing is ruled.*
*Subject: is the 2026-07-23 routing research (`notes/2026-07-23-fable-routing-research-dave.md`)
and the canon it produced (`MODEL-ROUTING.md`) still current against Anthropic's live docs,
four weeks on?*

**Verdict in one line: holds with 10 amendments — the architecture is intact, but the model
strings, the effort ladder and the classifier/fallback picture have all moved, and one canon
rule now sits in genuine tension with Anthropic's own Opus 5 guidance.**

---

## Method

- Every fetch below was performed on **2026-08-21**. Each claim row carries the URL as fetched
  that day. No claim in this report is sourced from training knowledge; where a page could not be
  fetched, that is stated as UNFETCHABLE rather than filled from memory.
- **Fetch route.** Nine pages fetched directly. One page — the migration guide — exceeded the
  fetch tool's size cap; it was retrieved instead by `curl` in the session's Linux workspace and
  stripped to text locally, then read in full. Same URL, same day, different transport. Declared
  here so the provenance is not silently uniform.
- **Not probed.** The three remaining practitioner links in the July doc (Masset, TrueFoundry,
  AlphaSignal) were not re-fetched; they carried no load-bearing claim in canon. Their status is
  therefore UNKNOWN, not CONFIRMED. The Verdent practitioner report *was* checked against official
  guidance because canon leans on one of its numbers — see row 14.
- **Architecture is out of scope.** The July doc's own thesis — the invariant / knowledge / adapter
  layering, and scar-tissue subtraction for Fable — is architecture, not a doc claim. Current
  guidance does not contradict it; the "Refactor existing prompts and skills" bullet in the live
  Fable prompting guide still says in as many words that skills written for prior models are often
  too prescriptive and can degrade output. The thesis stands untouched.

### Pages fetched, 2026-08-21

| # | Page | URL | Status |
|---|---|---|---|
| A | Prompting Claude Fable 5 | `platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5` | fetched |
| B | Introducing Claude Fable 5 and Claude Mythos 5 | `platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5` | fetched |
| C | Models overview | `platform.claude.com/docs/en/about-claude/models/overview` | fetched |
| D | Migration guide | `platform.claude.com/docs/en/about-claude/models/migration-guide` | fetched via curl (size cap) |
| E | Effort | `platform.claude.com/docs/en/build-with-claude/effort` | fetched — **new page since July** |
| F | Refusals and fallback | `platform.claude.com/docs/en/build-with-claude/refusals-and-fallback` | fetched — **new page since July** |
| G | Prompt caching | `platform.claude.com/docs/en/build-with-claude/prompt-caching` | fetched |
| H | Model deprecations | `platform.claude.com/docs/en/about-claude/model-deprecations` | fetched |
| I | Prompting Claude Opus 5 | `platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5` | fetched — **new page since July** |
| J | Introducing Claude Opus 5 (announcement, Jul 24 2026) | `anthropic.com/news/claude-opus-5` | fetched — **new since July** |
| K | Redeploying Fable 5 (Jun 30 2026, updated Jul 1) | `anthropic.com/news/redeploying-fable-5` | fetched — **not cited in July doc** |
| L | Improving Fable 5's biology safeguards (Aug 7 2026) | `anthropic.com/news/improving-fable-5-s-biology-safeguards` | fetched — **new since July** |
| M | Introducing Fable 5 & Mythos 5 (announcement) | `anthropic.com/news/claude-fable-5-mythos-5` | fetched |

---

## The claim table

Rows are numbered for reference. **CONFIRMED** = unchanged and re-verified today.
**CHANGED** = the guidance moved. **GONE** = the claim or page is no longer there.
**NEW** = guidance that did not exist when the July doc was written.

### Confirmed — no action

| # | Claim as filed in July | Status today (2026-08-21) | Source |
|---|---|---|---|
| 1 | Adaptive thinking always on; `thinking: {type:"disabled"}` and `budget_tokens` error out; depth via `effort`; raw chain-of-thought never returned | CONFIRMED. "Adaptive thinking is the only thinking mode on `claude-fable-5` and `claude-mythos-5`… `thinking: {type: "disabled"}` returns an error." Raw CoT never returned; `thinking.display` is `"summarized"` or `"omitted"` (default) | B, D |
| 2 | More literal instruction following; steerable with a brief instruction | CONFIRMED verbatim: "you can steer most behaviors with a brief instruction rather than enumerating each behavior by name" | A |
| 3 | Longer turns; single requests run many minutes, autonomous runs for hours; go async rather than block | CONFIRMED verbatim, including "consider restructuring harnesses to check on runs asynchronously… rather than blocking" | A |
| 4 | "Dispatches parallel subagents more readily than prior models" | CONFIRMED verbatim | A |
| 5 | Memory affinity — "performs particularly well when it can record lessons from previous runs and reference them" | CONFIRMED verbatim, under a section now headed "Construct a memory system" | A |
| 6 | Announcement claim: persistent memory improved Fable ~3× more than Opus 4.8 | CONFIRMED. "giving it access to persistent file-based memory improved its performance three times more than for Opus 4.8; Fable also reached the game's final act three times more often" (Slay the Spire) | M |
| 7 | `stop_reason: "refusal"` returned as HTTP 200, not an error | CONFIRMED, and now documented on a dedicated page with the full response shape | B, F |
| 8 | Refused-before-output requests aren't billed | CONFIRMED: "You are not billed for a refusal that arrives before any output." Newly explicit: a **mid-stream** refusal bills input plus already-streamed output, and a refused request still counts against rate limits | F |
| 9 | API removals: assistant prefill, non-default temperature/top_p/top_k | CONFIRMED. "Prefilling the assistant message is not supported… returns a 400 error" | D |
| 10 | Reasoning-extraction refusals — cull prompts that ask the model to echo its reasoning | CONFIRMED and hardened: it is now a named category, `"reasoning_extraction"`, with the docs warning it causes "elevated fallbacks to Claude Opus 4.8" | A, F |
| 11 | Same: 1M context, 128k output, Messages API shape, tool-use patterns | CONFIRMED. "a 1M token context window by default, and up to 128k output tokens per request" | B, C, D |
| 12 | Prompt caching minimum cacheable prefix now 512 tokens | CONFIRMED, with a caveat worth carrying: 512 applies to **Opus 5, Fable 5 and Mythos 5 only**. Sonnet 5 is still 1,024 and Haiku 4.5 is 4,096 | D, G |
| 13 | Cost $10/$50 per M in/out for Fable | CONFIRMED exactly: "$10 USD per million input tokens and $50 USD per million output tokens" | B, C |
| 14 | Route by difficulty × horizon — Fable's lead grows with task length and complexity | CONFIRMED in substance. Today's wording: "particularly effective at end-to-end work that takes a person hours, days, or weeks… testing it only on simpler workloads tends to undersell its capability range" | A |
| 15 | Mid-session model switch invalidates the prompt cache | CONFIRMED, and now stated directly on the effort page for the analogous case — see row 24 | E |
| 16 | Fresh-context verifier subagents beat self-critique | CONFIRMED **for Fable**: "Separate, fresh-context verifier subagents tend to outperform self-critique." Note the direct conflict with Opus 5 guidance in row 26 | A |
| 17 | Don't surface context-budget counts — causes premature wrap-up | CONFIRMED, still headed "Rare cases of context-budget concern", still recommending the "You have ample context remaining" reassurance | A |
| 18 | Write handoffs as re-groundings, outcome first, complete sentences, no working shorthand | CONFIRMED — this is now a fuller section, "Readability when communicating with the user", with the re-grounding language intact | A |

### Changed

| # | Claim as filed in July | What it says today | Source |
|---|---|---|---|
| 19 | **Effort recalibration.** July quoted: *"Start at high for most tasks, including workloads that ran at xhigh on Claude Opus 4.8… Lower effort settings on claude-fable-5 still perform well and often exceed xhigh performance on prior models."* | The second sentence survives verbatim. The first has been **replaced by a full ladder**: "Use `high` as the default for most tasks, with `xhigh` for the most capability-sensitive workloads and `medium` or `low` for routine work." The section is now headed **"Consider all effort levels"** — the emphasis has moved from *start high* to *use the whole range*. The old sentence survives only in the migration-guide checklist | A, D, E |
| 20 | **Effort has three or four levels** (implied by the July doc, which discusses medium/high/xhigh) | There are **five**: `low`, `medium`, `high`, `xhigh`, `max`. `max` = "Absolute maximum capability with no constraints on token spending". `high` is the API default and "produces exactly the same behavior as omitting the `effort` parameter entirely" | E |
| 21 | **Fallback-aware routing: route classifier-prone task classes to Opus** | Materially changed. **Claude Opus 5 also ships safety classifiers.** The refusals page opens: "Claude Fable 5 **and Claude Opus 5** include safety classifiers that can decline a request." Opus 5's own cyber-category refusals fall back to Opus 4.8. So "route it to Opus" is no longer automatically a classifier-free destination — it depends which Opus | F, D |
| 22 | **Classifiers fire on "security-adjacent" work** (July doc's loose phrasing, sourced partly from Verdent) | Now a published, named set of five categories: `"cyber"`, `"bio"`, `"frontier_llm"`, `"reasoning_extraction"`, `"general_harms"` — each with the note that benign work in the domain can also trigger it. The Fable prompting guide names the three primary domains as offensive cybersecurity, biology/life sciences, and extraction of summarized thinking | A, F |
| 23 | **Verdent practitioner report: ~30% higher token counts from a newer tokenizer** (filed as practitioner-report, not official) | **Officially contradicted as a Fable-vs-Opus-4.8 delta.** The migration guide: "Token counts are roughly unchanged because the models use the same tokenizer." The ~30% figure *is* official — but it is the delta versus models **before Opus 4.7**: "Compared with models before Claude Opus 4.7, the same content can tokenize to roughly 30% more tokens." Dave already paid the 4.7 tokenizer once. Moving Opus 4.8 → Fable 5 costs no token inflation, only the 2× per-token price | D |
| 24 | **Anti-pattern: never switch model mid-session (cache invalidation)** | Still true, and now **broader than model**. Changing the **effort** value between requests also invalidates the cached prefix: "Because effort shapes the rendered prompt, changing it between requests does not preserve cached prefixes from earlier turns; if you rely on prompt caching across a long session, pick an effort level at the start and keep it constant" | E |

### New

| # | Guidance that did not exist in July | Source |
|---|---|---|
| 25 | **Claude Opus 5 exists.** Announced **24 July 2026** — one day after Dave filed the research. `claude-opus-5`, $5/$25 per MTok, 1M context, 128k output, adaptive thinking, knowledge cutoff May 2026. The models overview now opens: "If you're unsure which model to use, start with **Claude Opus 5**… For workloads that need the highest available capability, use Claude Fable 5." The announcement positions it as "close to the frontier intelligence of Claude Fable 5 at half the price" and "the new default model on Claude Max, and the strongest model on Claude Pro" | C, J |
| 26 | **Opus 5 over-verifies, and the docs say to stop telling it to verify.** "Claude Opus 5 verifies its own work without being told to. If your prompt contains explicit verification instructions ('include a final verification step for any non-trivial task,' **'use a subagent to verify'**), remove them… The same applies to legacy harness scaffolding that adds separate verification steps." Its sample delegation instruction includes: "**do not use subagents to verify or double-check your own work**". This runs against canon rule 5 and against row 16's Fable guidance — see P8 | I, D |
| 27 | **Opus 5 delegates more readily, and the docs say to cap it.** "Delegation pays off on genuinely independent, sizeable tracks of work, but it multiplies cost and time when applied to small tasks… give explicit guidance on which scenarios warrant delegation, or set deterministic caps." Named caps for Claude Code / Agent SDK: `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`, `max_budget_usd` (require Claude Code 2.1.217+) | I |
| 28 | **Opus 5 responses run longer, and effort will not shorten them.** "Effort controls thinking volume, not visible response length: on Claude Opus 5, changing effort does not reliably shorten responses, so prompt for length instead" | E, I |
| 29 | **Opus 5 breaking change: thinking cannot be disabled at `xhigh` or `max`** — those requests return 400, validated per request | D, E |
| 30 | **Server-side fallback is now a product.** `fallbacks: "default"` on the Claude API (beta header `server-side-fallback-2026-07-01`) retries a declined request on Anthropic's recommended model for that refusal category; or name up to three models yourself. SDK middleware (`BetaRefusalFallbackMiddleware`) does the same client-side on any platform. **Fallback credit** refunds the prompt-cache cost of switching so you don't pay it twice | B, F |
| 31 | **Fable 5 was suspended and redeployed.** US export controls applied 12 June 2026 forced suspension of Fable 5 and Mythos 5 for all users; controls lifted 30 June; access restored **1 July 2026**. Anthropic shipped an improved cyber classifier in response to an Amazon-reported bypass, and states plainly: "The new classifier also comes at the cost of **flagging benign requests more often during routine coding and debugging tasks**." This is the official confirmation of the false-positive pressure the July doc could only cite Verdent for | K |
| 32 | **Biology safeguards relaxed, 7 August 2026.** "we're making updates to Claude Fable 5's biology safeguards in a way that substantially reduces false positives… this update reduced biology-related fallbacks by about **85%** across our product surfaces." Refusal rates are a moving target, four weeks stale by default | L |
| 33 | **Fable on subscription plans runs on usage credits.** For Pro, Max, Team and select Enterprise plans, Fable 5 was included for up to 50% of weekly usage limits through **7 July 2026**, "after which it will be available via usage credits". This is the actual mechanism behind Dave's "Premium — rationed" tier | K |
| 34 | **Three new Fable prompting sections with direct Memento relevance:** "Ground progress claims during long runs" (audit each claim against a tool result from this session; in Anthropic's testing this "nearly eliminated fabricated status reports"), "State the boundaries" (report findings and stop; don't fix until asked), and "Create a send-to-user tool" (surface verbatim content mid-turn without ending it) | A |
| 35 | **`max` effort available on Fable 5, Mythos 5, Opus 5, Opus 4.8, Mythos Preview, Opus 4.7, Opus 4.6, Sonnet 5, Sonnet 4.6.** `xhigh` on Fable 5, Mythos 5, Opus 5, Opus 4.8, Opus 4.7, Sonnet 5 — note **Haiku 4.5 supports neither, and has no adaptive thinking at all** | C, E |
| 36 | **Retirement dates now published for every tier model.** `claude-fable-5` not sooner than 9 Jun 2027 · `claude-opus-5` not sooner than 24 Jul 2027 · `claude-sonnet-5` not sooner than 30 Jun 2027 · `claude-haiku-4-5-20251001` **not sooner than 15 Oct 2026**. All four are Active with no deprecation filed | H |
| 37 | **Fable 5 and Mythos 5 are Covered Models** — 30-day data retention, not available under zero data retention. Opus 5 has no such restriction | B, D |

### Gone

| # | July claim | What replaced it |
|---|---|---|
| 38 | The July doc's "Sources" list points at a **Skills** page, **CLAUDE.md memory**, **Hooks**, **Model config**, **Subagents**, **Prompt caching** and **Tool Search Tool** under `code.claude.com` and `platform.claude.com` | Not re-fetched this pass — they carried no numeric claim in canon. Status **UNKNOWN**, not GONE. Flagged only so nobody reads this table as a clean bill of health for them |
| 39 | Nothing in the July research doc is GONE from the live docs. Every claim it filed still has a live home | — |

---

## Numbered amendment proposals

These are proposals. Nothing below has been applied. Dave rules by number.

---

**P1 — Fable tier: pin the model string and name the ration mechanism.**

*Where:* `MODEL-ROUTING.md`, the tiers table, **Premium — rationed** row, Notes cell.

Current: "Most-trusted, but dear. Spend it where high-trust-*at-scale* actually pays; not the daily driver."

Proposed addition to that cell: `claude-fable-5` · $10/$50 per MTok · on Pro/Max/Team plans it draws on **usage credits**, not the standard weekly allowance (Anthropic, 1 Jul 2026). Rationing is a billing fact, not just a habit.

*Why:* row 33. The tier is called "rationed" and now there is an official mechanism with that name. Naming it makes the tier auditable rather than a feeling.

---

**P2 — Default tier: give the corrected cell a citation and a date.**

*Where:* `MODEL-ROUTING.md`, tiers table, **Default — complex** row, Model cell; and the staleness note below the table.

Current: `Opus 5 · high` — corrected 2026-07-30 on Dave's ruling, with no external source named.

Proposed: keep the cell, add `claude-opus-5` as the exact API string, and add to the staleness note that the correction is now **independently confirmed**: Opus 5 was announced 24 July 2026 (one day after the research was filed), and the live models overview names it the recommended starting point. Cite `anthropic.com/news/claude-opus-5` and the models overview, both fetched 2026-08-21.

*Why:* rows 25 and 36. The #48 defect was a version number with no provenance. It now has provenance; attaching it converts a ruling into a receipt.

---

**P3 — Throughput and Chore tiers: pin their strings too, and set a watch date on Haiku.**

*Where:* `MODEL-ROUTING.md`, tiers table, **Throughput** and **Chore** rows.

Proposed: Throughput → `claude-sonnet-5` ($2/$10, 1M context, cache minimum 1,024 tokens — *not* 512). Chore → `claude-haiku-4-5-20251001` ($1/$5, 200k context, **no adaptive thinking, no `xhigh`, no `max`**, cache minimum 4,096 tokens), with a watch note: tentative retirement **not sooner than 15 October 2026**, roughly eight weeks out.

*Why:* rows 12, 35, 36. Two of the four tiers currently carry a bare family name. The Haiku line is the one with an actual clock on it, and the "no adaptive thinking" fact means the Chore tier behaves categorically differently from the other three — worth one clause in the Notes cell.

---

**P4 — Rewrite the fallback-aware routing bullet: Opus is no longer classifier-free.**

*Where:* `MODEL-ROUTING.md`, **Fable-era notes**, the bullet beginning "Diagnose before attributing a failure to safety classifiers", specifically its last sentence: *"Fallback-aware routing (route classifier-prone task classes to Opus) only ever acts on DIAGNOSED refusals, not pattern-matched ones."*

Proposed replacement: keep the diagnose-first discipline in full — it was right and it caught a real misdiagnosis. Amend only the destination: **Opus 5 also runs safety classifiers** (refusals page, fetched 2026-08-21), and Anthropic's own default fallback target for Fable's cyber category is **Opus 4.8**, not Opus 5. So a diagnosed classifier refusal routes *down a generation*, not sideways.

*Why:* row 21. This is the single most load-bearing change in the report: canon currently names a destination that no longer has the property it was chosen for.

---

**P5 — Replace "security-adjacent" with the five published refusal categories.**

*Where:* `MODEL-ROUTING.md`, Fable-era notes, same bullet as P4; and by extension the July doc's loose phrasing.

Proposed: name the categories as published — `cyber`, `bio`, `frontier_llm`, `reasoning_extraction`, `general_harms` — and record that a refusal reports which one fired in `stop_details.category`. Add the freshness warning: refusal *rates* move. Anthropic tightened the cyber classifier on 1 July 2026 and explicitly accepted more false positives on "routine coding and debugging tasks", then on 7 August 2026 relaxed biology, cutting bio fallbacks by about 85%. A refusal-rate observation is stale within weeks.

*Why:* rows 22, 31, 32. Canon's own rule is that a diagnosis must be diagnosed — a named category from the API is a diagnosis; "felt security-adjacent" is a pattern-match.

---

**P6 — The effort axis is a five-rung ladder, and it has an official page now.**

*Where:* `MODEL-ROUTING.md`, Fable-era notes, the bullet beginning "**Effort is a real second axis at the API but NOT controllable in Cowork**".

Proposed: keep the Cowork observation and the 2026-07-24 correction above it untouched — both are OBSERVED facts about Dave's environment and no doc speaks to them. Amend only the API half: the ladder is `low · medium · high · xhigh · max`; `high` is the default and is identical to omitting the parameter; there is now a dedicated page (`build-with-claude/effort`) with per-model recommendations. For Fable: start `high`, `xhigh` for capability-sensitive work, step down to `medium`/`low` for routine. For Opus 5: start `high`, and — quoted, because it bears on Dave's calibration habit — "If you carried effort settings over from an earlier model, run a fresh effort sweep on your evals rather than reusing them."

*Why:* rows 19, 20, 35. Canon's effort line predates the existence of both `max` and the page that documents it.

---

**P7 — Broaden the mid-session anti-pattern from model to model-and-effort.**

*Where:* `MODEL-ROUTING.md`, "How it runs in practice", **Mode 3**, the anti-pattern sentence "never switch model mid-session".

Proposed: extend to "never switch model **or effort** mid-session". Official wording now available: "Because effort shapes the rendered prompt, changing it between requests does not preserve cached prefixes from earlier turns; if you rely on prompt caching across a long session, pick an effort level at the start and keep it constant."

*Why:* row 24. Canon notes the model half was REPORTED, migration-guide era. Both halves are now documented, and the effort half is new information — the handoff seam is the right place to set effort as well.

---

**P8 — The verification conflict. This one needs Dave, not a footnote.**

*Where:* `MODEL-ROUTING.md`, **rule 5** ("Verify with a peer-or-stronger model") and **rule 6**, and the July doc's runbook advice "Prefer fresh-context verifier subagents over 'self-critique' steps".

The two live Anthropic pages now disagree, by model:

- **Fable 5 guide:** "Separate, fresh-context verifier subagents tend to outperform self-critique."
- **Opus 5 guide:** "Claude Opus 5 verifies its own work without being told to. If your prompt contains explicit verification instructions ('include a final verification step for any non-trivial task,' 'use a subagent to verify'), remove them: instructions like these cause over-verification on Claude Opus 5, and removing them reduces wasted tokens with no loss in quality. **The same applies to legacy harness scaffolding that adds separate verification steps.**" Its own sample delegation prompt says "do not use subagents to verify or double-check your own work."

Dave's default tier is Opus 5. Canon rule 5 is a standing instruction to verify with a peer-or-stronger model, and the parallel-conductor machinery is exactly the "legacy harness scaffolding that adds separate verification steps" the Opus 5 page names.

*Proposed, and deliberately framed as a question rather than an edit:* three readings, all defensible, none mine to pick —

1. **Rule 5 is a trust boundary, not a prompt.** It is invariant-layer, like the gates: it exists so quality doesn't depend on model goodwill. Anthropic is optimising tokens; Dave is buying independence. Keep rule 5 verbatim, add a note that the cost is now documented and accepted on purpose.
2. **Rule 5 is model-conditional.** Keep the adversarial verifier for Fable-run and high-stakes work; drop routine self-check scaffolding on Opus 5 sessions, where the model does it unprompted. This is the adapter-layer reading and matches the July doc's own three-layer thesis.
3. **Rule 5 stays, the scaffolding thins.** Keep peer-or-stronger adversarial *audit* (a different act from self-verification), but strip the "re-check your own work" instructions that duplicate what Opus 5 already does.

*Why it can't be auto-applied:* rule 5 is ratified canon and this is precisely the class of change that a sub must not make. It is flagged, priced and left open.

---

**P9 — Mode 2 delegation: the doc evidence now cuts both ways, and Dave's ruling survives both.**

*Where:* `MODEL-ROUTING.md`, "How it runs in practice", **Mode 2 — in-session delegation: DELIBERATE, not default**.

Proposed: leave the ruling standing and add one line of current evidence, because the Mode 2 note currently rests only on Cowork's own economics and the reader has no idea the docs say anything at all:

- The Fable guide pushes the other way: "Use subagents frequently… prefer asynchronous communication between orchestrator and subagents over blocking."
- The Opus 5 guide pushes Dave's way: "Delegate to a subagent only for large tasks that are genuinely independent and parallelizable… Do not delegate work you can finish yourself in a handful of tool calls… keep spawn counts low."

Since Dave's default tier is Opus 5, the Opus 5 guidance independently corroborates the 2026-07-23 supersession. Worth saying so — the ruling currently reads as environment-specific when it is in fact also model-appropriate.

*Why:* rows 4 and 27, plus the delegation-cost-inversion memory. This strengthens an existing ruling rather than reopening it.

---

**P10 — Correct the tokenizer-overhead line, and demote the practitioner claim that produced it.**

*Where:* the July research doc's cost bullet and its anti-pattern "Routing everything to Fable… 2× price (plus reported tokenizer overhead)". Canon inherits the framing rather than the number, so the edit is small — but the number is wrong in a direction that matters.

Proposed: record that the official migration guide contradicts the Verdent practitioner report on this point. Moving Opus 4.8 → Fable 5, "token counts are roughly unchanged because the models use the same tokenizer." The ~30% figure is real but is the delta versus models **before Opus 4.7** — a cost Dave already absorbed generations ago. **Fable's true premium over Opus 4.8 is 2× per token and nothing more; over Opus 5, also 2×.**

*Why:* row 23. The July doc did the right thing labelling it practitioner-report. The audit is now available and the practitioner was wrong; leaving the inflated figure in makes Fable look ~30% dearer than it is, which biases every close routing call away from it.

---

## Verdict

The July research holds. Its architecture — invariant, knowledge, adapter — is untouched by anything Anthropic has published since, and the live Fable prompting guide still says in as many words that skills written for prior models are too prescriptive and degrade output, which was the thesis. Eighteen of the claims re-verified clean today, including every load-bearing number Dave asked to be checked: 1M context, 128k output, $10/$50, the 512-token cache minimum, the ~3× memory result, and the unbilled pre-output refusal. Nothing is GONE. But four weeks bought three real movements, and they cluster in the adapter layer, which is exactly where the July doc predicted the churn would be. **Claude Opus 5 shipped the day after the research was filed** — it is now Anthropic's recommended default, it is Dave's Default tier, and it comes with its own prompting page that neither document has ever read. **The effort axis grew a fifth rung and a dedicated page**, and the "start at high" advice canon quotes has been restaged as "consider all effort levels". **And the classifier picture inverted the one piece of routing advice that named a destination**: "route classifier-prone work to Opus" was written when Opus meant classifier-free, and Opus 5 now runs classifiers of its own, with Anthropic's default fallback pointing back at Opus 4.8. Set against that, one genuine conflict is left open rather than resolved — Anthropic now tells Opus 5 users to delete the verification scaffolding that canon rule 5 requires, and choosing between a token bill and an independence guarantee is Dave's call, not a sub's. **Holds with 10 amendments, of which P4 and P8 are the two that change behaviour rather than text.**

*All fetches 2026-08-21. Proposal-only: nothing enacted, nothing ruled.*
