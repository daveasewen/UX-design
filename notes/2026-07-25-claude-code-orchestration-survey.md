# Survey — upstream orchestration features vs our harness (2026-07-25)

*Recorded 2026-07-25 (legend-v5.3 session, Fable) at Dave's ask after reviewing an X thread + the six
Claude Code docs pages. Ruling status: NOTES ONLY — Dave asked "architectural change or notes for a
follow-up?"; agreed answer = notes + queue entry, no architecture change now. OBSERVED = docs read
this session; INFERRED = the mapping onto our practice (mine).*

## What was surveyed (OBSERVED)

Trigger: X thread by @0xCodez, "Graph Engineering with Claude" (x.com/0xCodez/status/2079165300625330317)
— promotional but factually accurate. Verified against the official docs (code.claude.com/docs/en/):
`agents` · `sub-agents` · `agent-view` · `agent-teams` · `workflows` · `worktrees`.

Feature facts that checked out:

- **Dynamic workflows** (v2.1.154+, paid plans; CLI + Desktop app): Claude writes a JavaScript
  orchestration script; runtime executes it in the background. Primitives: `agent()` (one subagent,
  optional JSON `schema` → validated output, per-node `model`), `parallel()` (barrier fan-out; failed
  thunk → null), `pipeline()` (no barrier, streams items). Script holds the plan; Claude's context
  holds only the final answer. Caps: 16 concurrent / 1,000 agents per run. **No mid-run user input**
  — docs: "for sign-off between stages, run each stage as its own workflow." Saved runs →
  `.claude/workflows/` (project, git-shared) or `~/.claude/workflows/`; run as `/<name>`; can ship in
  plugins. Triggers: ask in words, keyword `ultracode`, or `/effort ultracode` (auto-workflow per
  task). Bundled: `/deep-research` (scope → parallel search → fetch → adversarial 3-vote verify →
  cited synthesis).
- **Agent teams** (EXPERIMENTAL, off by default, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`): lead
  session + teammate sessions, shared task list with dependencies + file-lock claiming, inter-agent
  mailbox, plan-approval gate (lead approves teammate plans), hooks `TeammateIdle` / `TaskCreated` /
  `TaskCompleted` (exit 2 = block + feedback). **No worktree isolation for teammates** — docs advise
  partitioning files per teammate. No session resumption of in-process teammates.
- **Subagents**: `memory: user|project|local` gives a subagent a persistent directory +
  `MEMORY.md` index (first 200 lines / 25KB preloaded) that survives across conversations.
  Resumable via `SendMessage` (full transcript retained); transcripts survive main-conversation
  compaction; subagents auto-compact themselves. `isolation: worktree` per-agent.
- **Agent view** (`claude agents`, research preview): dispatch/monitor background sessions, each
  auto-worktree'd. **Worktrees**: `--worktree`, `.worktreeinclude` for gitignored env files, auto
  cleanup sweep, `EnterWorktree` tool.

## Mapping onto our practice (INFERRED)

| Upstream | Ours | Read |
|---|---|---|
| Workflow script holds the plan | DIVVY PLAN prose in handoffs | Their answer to "confident false inscription": the plan never re-derived, it's code, versioned, re-runnable |
| Stage-per-workflow for sign-off | Dave's sign-off gates between waves | Direct fit |
| `TaskCompleted` exit-2 hook | verification = enforcement | Same principle, as a hook |
| Adversarial verify / judge panels | adversary-auditor gate | Same pattern productised |
| Per-node `model` routing | MODEL-ROUTING.md | Same principle, per-node not per-session |
| Subagent `memory:` + MEMORY.md | tattoo architecture, per-role | A productised slice of Memento |
| Teams lead/teammates + task list | conductor/worker + divvy | Built-in version of the ratified model |
| Teammate file partitioning | worktree-reconcile rule | They landed on our rule |
| Subagent transcripts survive compaction | context-gauge flush ritual | Structural relief for the gauge |

## The one strategic implication (for Dave to rule, own session)

**The harness spin-off has been partially productised upstream.** Invariant + method layers overlap
with workflows/teams/subagent-memory. Residual differentiation = what upstream does NOT cover:
capture ritual · provenance/confidence marking (OBSERVED vs INFERRED) · the gauge · Dave-in-the-loop
rulings + review-overlay docs · the tattoo/Polaroid trust hierarchy ACROSS sessions (their memory is
per-agent, not per-project-with-provenance). Proposed reframe: spin-off = **a layer on top of
upstream orchestration, not a competitor**. NOT RULED.

## Harness design target (Dave's steer, same session — working assumption, NOT ruled)

Dave: could the harness be redesigned as a Claude Code project — or is this what coders do anyway?
And: "the first version of this will be GitHub Copilot in VS [Code] to be fair" (bank-approved
tooling reality for his team).

**Steer adopted for the follow-up session: runtime-agnostic core + thin adapters — ADR-0008's
canonical-core pattern applied to the harness itself.** The tattoos are already plain markdown +
Python in git, so the core ports anywhere; Claude Code is ONE adapter, not the home.

- **What coders already do (don't compete):** the file-layout layer is table stakes across runtimes
  in 2026 — Copilot supports `AGENTS.md` (root + nested), custom agents `.github/agents/*.agent.md`
  (persona/tools/handoffs), subagents + plan agent, prompt files, MCP; community pro-formas exist
  (github/awesome-copilot). Verified 2026-07-25 (github.blog changelog 2025-08-28; VS Code docs).
- **What they don't do (the differentiated half):** provenance marking (OBSERVED/INFERRED) · gauge ·
  capture ritual + date discipline · decision ledgers with WHY · supersession · review overlays for
  a NON-CODER principal (coder practice assumes the human reads diffs; ours assumes the human rules
  on rendered reviews). This is the half Dave's team needs.
- **Copilot adapter mapping:** `AGENTS.md` ← GM §A standing orientation · `.github/agents/` ← worker
  roles · prompt files ← runbook invocations · gates = scripts in terminal/CI (runtime-free).
  Claude-only features (subagent `memory:`, dynamic workflows, hooks) = the premium tier of the
  Claude adapter, not blockers.
- **Delivery (Dave asked: plugin equivalent? Verified 2026-07-25):** Copilot has NO plugin artefact /
  marketplace equivalent. Instead: **org-level push-distribution** — agents in `{org}/.github/` or
  `.github-private` `/agents` reach every org member automatically, no install, IT-governed. For a
  bank this beats a marketplace (curated, zero friction). Enterprise pattern in the wild: central
  agent-platform repo + Actions sync into `.github-private`. ⇒ Copilot adapter ships via the org
  repo; no hooks there, so enforcement = CI only (our gates already are scripts).

## Constraints that keep this notes-only today

1. Features are Claude Code-side; we work in Cowork (parity gap already logged —
   memory `product-feedback-cowork-parity`). Workflows do exist in the Desktop app; Cowork unmentioned.
   Partial parity observed in-session: Cowork Agent tool has `isolation: worktree`.
2. Legend v5.x sign-off + hit-area gate + donut/bar/combo wave are queued — no mid-stream process swap.
3. Teams = experimental + no teammate worktrees; workflows = no mid-run rulings (Dave's eye is
   load-bearing in our loop — the chart exemplar's six refinements came from watch-and-intervene).

## Vision-level touch (Dave's follow-up question, same session — INFERRED, not ruled)

Dave: "might it touch on the final Apollo project, the vision?" Yes — three touchpoints beyond
process, correcting this note's earlier "process-only" framing:

1. **The production line IS a workflow.** Pipeline mental model (scoping → generation → gates →
   prototype; criteria == gates) maps one-to-one onto a workflow script: per-component generation
   fan-out, gates as verifier nodes on edges, "done" withheld until green. The production line
   becomes a versioned, re-runnable artefact rather than a build runner + prose.
2. **Dispatch delivery vehicle.** Saved workflows ship in PLUGINS as `/commands` → gates-as-a-service,
   chat-to-KB bot, canonical-core + adapters (ADR-0008) could ship as an Apollo plugin
   (canon + skills + gates + `/apollo-generate`, `/apollo-audit`). Teams install the process, not adopt it.
3. **Register = inference ramp** (charter §9): per-node `model` routing = inference-tiering as a
   platform primitive — cheap models on floor/churn nodes, expensive on judgment nodes.

Net: strengthens the bet ("generation is a commodity; value = the layer around it") — upstream
shipping the orchestration substrate makes the layer MORE portable, not less necessary. Changes
nothing in the build queue; floor-first holds. Feeds: [[pipeline-mental-model]] ·
[[apollo-canonical-core-adapters]] · [[register-inference-ramp]] · [[chat-to-kb-bot]] ·
[[kb-distillation-at-deploy]].

## Feeds

- `_FUTURE-STATE.md` → "Parallel windows vs subagents" entry (this is new evidence for that open
  question — a THIRD mechanism) + the multi-thread GOOD-MORNING entry.
- `notes/2026-07-23-harness-framework-spinoff.md` (reframe above) · memory `harness-framework-spinoff`.
- Candidate trial when Dave wants one: run ONE bounded audit (e.g. a repo-wide gate sweep) as a
  dynamic workflow in Claude Code/Desktop and compare against the same job as a conductor divvy.
