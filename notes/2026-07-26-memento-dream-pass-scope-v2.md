# Memento — dream-pass scope v2: THREE shapes (Cowork · Claude Code · VS Code+Copilot)

**Date:** 2026-07-26 (from `date`, ~16:10 BST)
**Session:** Fable solo, same session as v1.
**Status:** SCOPE for Dave to rule on. Nothing ruled. Supersedes **§4 and the D4 row only** of
`2026-07-26-memento-dream-pass-scope.md` (v1); v1's §1–§3 (docs read, tooling verification, §4.1
scope + D1–D3) stand unchanged — referenced, not duplicated.
**Trigger:** Dave, this session: three shapes to consider; Max plan = Claude Code available;
"one day I'll move to code probably"; **"I want a version for VS Studio with GitHub Copilot."**
**Context gauge at authoring:** 🟡 Amber ~55% (in-head estimate, ±15%).

**Why Shape C matters beyond the dream pass:** it is the first concrete test of the
harness-spinoff thesis (memory `harness-framework-spinoff`, Dave's 07-25 steer: runtime-agnostic
core + adapters, **Copilot/VS Code likely first adapter**). The memory store is repo markdown +
gates; if a Copilot agent can run a useful dream over it, the "core is runtime-agnostic" claim
stops being an assertion.

---

## 1. Shape C — VS Code + GitHub Copilot (verified against primary sources this session)

### 1.1 What exists, verified

- **Copilot cloud agent *automations*** (GitHub changelog, 2026-06-02): the cloud agent runs
  **on a schedule (hourly / daily / weekly) or on repo events**, per-repository, with a configured
  prompt, a **restricted tool list**, and a chosen model; it works in a GitHub Actions sandbox and
  delivers a **draft pull request**. Available on Copilot Pro/Pro+/Max/Business/Enterprise;
  **private/internal repos only** for now. Usage-billed to the automation's creator.
  ⇒ Cadence (record's open question 2) *and* proposal-not-commit (¶171) are **native platform
  features** on this shape: the dream is a nightly automation, the proposal is a draft PR.
- **Custom agents** (VS Code docs, updated 2026-05): `.agent.md` files — description, tools,
  model, handoffs, body-as-system-prompt — in `.github/agents/`, **or natively from
  `.claude/agents/` ("Claude format")**. Reusable across chat, background agents (Copilot CLI),
  and cloud agents. Subagents can run a custom agent (experimental).
  ⇒ **One dreamer definition can serve Shape B and Shape C from the same file.** The adapter
  cost for the agent definition itself is zero.
- **AGENTS.md** is respected across modern Copilot surfaces — the repo already carries one.
- **`copilot-setup-steps.yml`** configures the agent's Actions environment ⇒ `_build_all.py` can
  run *inside the dreamer's sandbox*; independently, ordinary Actions CI on the dream PR re-runs
  the gates as a required check. **Gates-score-the-dream (§4.3) becomes server-side and
  unskippable** on this shape — arguably its strongest expression: a dream that breaks the build
  arrives pre-flagged on its own PR.
- Adjacent, noted not load-bearing: Copilot CLI gained prompt *scheduling*; a Copilot SDK is GA;
  local/cloud sandboxes in preview.

### 1.2 Where Shape C is thin — and why that thinness is interesting

- **No transcripts.** Copilot cannot see Cowork or Claude Code session transcripts. Its dream
  inputs are the **repo record only**: `GOOD-MORNING.md`, `_LIVE-STATE.md`, `MEMORY`-mirrored
  inscriptions, notes, dossiers, ledgers, git history — plus GitHub-side artifacts (issues, PRs,
  its own session logs). ¶153 ("read the tool calls") is unavailable.
- But the capture ritual's own success criterion is: *"the transcript never has to be the source
  of truth — a cold-start agent can reconstruct full context from the repo alone."* A repo-only
  dream is therefore not a degraded dream; **it is an audit of the capture ritual itself.** If
  Shape C's dreamer finds contradictions, staleness, and drift from the inscribed record alone,
  the ritual is working *and* being exercised. If it can't find anything a transcript-reading
  dreamer finds trivially, that measures exactly what the ritual is failing to inscribe.
- **The Cowork memory store is invisible to Shape C** — same boundary as the gates (v1 §3.1).
  Consistent, not new damage: memory is the accelerator, the repo is the record, and all three
  shapes dream over the record. Only Shape A can *additionally* read the accelerator.
- **Requires the repo on GitHub as private/internal** with Copilot cloud agent enabled — worth a
  one-time check of Dave's plan/repo settings before building.

## 2. The three shapes, side by side

| | **A — Cowork-native** | **B — Claude Code-native** | **C — VS Code + Copilot** |
|---|---|---|---|
| Dreamer runs as | Scheduled Cowork task (session) | `dreamer` agent: `--bg` session or saved workflow | Cloud agent **automation** (nightly) |
| Inputs | Repo + memory store + **119 transcripts** (turn-level) | Repo + raw JSONL transcripts (full ¶153 fidelity, CC sessions only) | **Repo record only** + GitHub artifacts |
| Proposal form | `notes/_dream/…-proposals.md` file | Worktree branch, gates pre-run in worktree | **Draft PR**, gates re-run by CI |
| Accept/reject | Dave reads file | Dave reviews diff / merges | Dave reviews PR — native review UI, comments, request-changes |
| Fleet (¶165–167) | Agent tool subagents (available, modest) | Full: subagents / workflows | Cloud agent internal; VS Code subagents experimental |
| Evidence+prevalence (¶169) | Prompt discipline | Workflow `schema` — structured | Prompt discipline; PR description carries it |
| §4.3 gates scoring | Manual step after proposal | In-worktree, near-free | **CI-enforced on the PR — strongest** |
| Available | **Today, zero install** | Today (Max plan) — Dave not yet working there | Needs repo on GitHub + Copilot plan w/ cloud agent |
| What it proves | The loop is worth running | Full-fidelity dreaming; eventual home | **Portability thesis; capture-ritual audit; team-facing** |
| Cost model | Plan usage | Plan usage | Usage-billed per automation run |

**Shared core across all three (the runtime-agnostic part, unchanged by shape):**
§4.1 fields + gate · the memory store as repo markdown · the steering spec (one dreamer prompt,
maintained once — home candidate: `.claude/agents/dreamer.md`, which VS Code reads natively) ·
the proposal-review-inscribe loop with Dave as sole promoter (derivation-governance).

## 3. Decision points (v2 — replaces v1's D4 row; D1–D3 unchanged, see v1 §6)

| # | Question | Recommendation |
|---|---|---|
| D1–D3 | *(unchanged — v1 §6)* | as v1 |
| **D4′** | Sequence across three shapes | §4.1 first → **A** (prove the loop, cheapest, tonight-capable) → **C** (portability proof + ritual audit; also the shape your team could see) → **B** when you move to Code (full fidelity, eventual home). C before B *only because* C tests a thesis and B mostly awaits your migration — flips freely if you start working CC-side sooner. |
| **D5** | Dreamer definition home | `.claude/agents/dreamer.md` — single file readable by Claude Code AND VS Code; `.github/agents/` symlink/copy only if a non-VS-Code Copilot surface needs it. |
| **D6** | Shape C precondition check | Confirm: repo hosted on GitHub (private), Copilot plan tier, cloud agent/automations enabled. One-time, five minutes, before any C build. |

Dave rules; nothing above is recorded as ruled.

## 4. Sources (Shape C claims)

- GitHub changelog 2026-06-02 — [Schedule and automate tasks with Copilot cloud agent](https://github.blog/changelog/2026-06-02-schedule-and-automate-tasks-with-copilot-cloud-agent/) (fetched in full this session)
- VS Code docs — [Custom agents in VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-agents) (fetched; `.claude/agents` "Claude format" location confirmed verbatim)
- Corroborating (search-level, not independently verified): [Copilot coding agent GA discussion](https://github.com/orgs/community/discussions/159068) · [GitHub Docs — kick off a task with Copilot agents](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/kick-off-a-task) · [Copilot CLI scheduling changelog](https://github.blog/changelog/2026-06-02-copilot-cli-improved-ui-rubber-duck-prompt-scheduling-and-voice-input)
- Prior in-repo: `notes/2026-07-25-claude-code-orchestration-survey.md` (the layer-on-upstream reframe this note extends to a second upstream)
