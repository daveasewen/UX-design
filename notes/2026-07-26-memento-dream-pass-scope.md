# Memento — scope: §4.1 provenance+status, §4.2 dream pass, verified against tooling and the five docs

**Date:** 2026-07-26 (from `date`, 15:52 BST)
**Session:** Fable solo. Follow-on to `2026-07-26-memento-dreaming-convergence-and-buildable.md` (the record).
**Status:** SCOPE for Dave to rule on. Nothing here is ruled. Decision points marked ⚖.
**Context gauge at authoring:** 🟡 Amber ~40–45% (in-head estimate, ±15%).

**Verification performed first (the record was authored at Amber ~58%):**
- The record's §3 paragraph citations were re-checked against `lamish-context-engineering-transcript.md`.
  **All hold.** The "¶" numbers are line numbers of the transcript file; every cited claim is at its
  cited line (125, 127, 83/135, 139–145, 171, 65–71, 39–67, 169, 153, 165, 115–117, 211, 215, 217–223).
  The three inferred-not-confirmed catches also verify: no mention of weights/training anywhere in the
  talk; no model class specified for the dreamer; the Q&A holds exactly three questions, none on weight
  space. "Mukta" appears nowhere; the moderator says "Lamis" once, the transcript otherwise "Lamish".
  ⇒ The record's §2 and §4 can be trusted as written.
- The convergence note was NOT re-attached this session, so the owed `-v2` revision is deferred (§5).

---

## 1. What the five docs actually offer for §4.2 (read cold this session, in full or in load-bearing part)

### 1.1 Sub-agents — direct match to the orchestrator + fleet pattern (transcript ¶165–167)

- A custom subagent is a markdown file with YAML frontmatter (`.claude/agents/<name>.md`): `name`,
  `description`, `tools`/`disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`,
  `memory`, `background`, `isolation`, `effort`. A **`dreamer` agent definition is therefore a
  checked-in, versioned artifact** — the steering spec the record's open question 3 wanted a home for.
- **Fleet mechanics exist:** subagents run in the background by default, up to 20 concurrent /
  200 per session; nesting via `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`. An orchestrator session can
  fan a reader per transcript and collect summaries — exactly ¶165–167.
- **`memory: project`** gives a subagent its own persistent directory
  (`.claude/agent-memory/<name>/`) that survives across conversations and is *shareable via git*.
  The dreamer can accumulate its own cross-run knowledge without touching the main store.
- Subagents skip the main conversation's auto-memory and (except Explore/Plan) load CLAUDE.md.
  A fresh-context dreamer reading transcripts cold — the record's §4.2 bias argument — is the
  *default behaviour*, not something to engineer.
- Cowork parity: the Agent tool in Cowork sessions already accepts `subagent_type` and
  `isolation: "worktree"` — the fleet primitive exists on both surfaces.

### 1.2 Dynamic workflows — the strongest match for the dream pass as a *repeatable job*

- A workflow is a JavaScript script (Claude-written, human-readable, reusable) that orchestrates
  dozens–hundreds of subagents in phases; intermediate results live in script variables, not context.
  `agent()` accepts a **JSON `schema`** for structured findings; `pipeline(list, fn)` runs one agent
  per item. ⇒ *evidence + prevalence stats* (¶169) are a natural output shape, not a bolt-on.
- Workflows can have agents **adversarially verify each other's findings** before reporting —
  upstream ships the same instinct as §4.3 (score the dream before trusting it).
- Saveable as a slash command (`.claude/workflows/` in-repo, versioned); resumable; background.
- Constraint: Claude Code v2.1.154+, paid plans; **not verified available in Cowork** (known parity
  gap, memory `product-feedback-cowork-parity`). The dream-as-workflow is a Claude Code build.

### 1.3 Agent view / background sessions — the scheduling substrate

- `claude --agent dreamer --bg "<prompt>"` dispatches a defined agent as a supervised background
  session; `claude agents --json` lists sessions scriptably; transcripts survive process restarts.
- Cowork has scheduled tasks natively (cron-style) — the actual "nightly" mechanism available today.
  Record's open question 2 (cadence) becomes a config value, not a design problem.

### 1.4 Worktrees — YES: proposal-not-commit isolation, for repo-side writes

- `isolation: worktree` on a subagent gives it an isolated checkout branched from the default
  branch; Bash is **fenced to the worktree** (redirect-to-main-checkout commands fail); auto-cleanup
  if unchanged; a worktree with changes persists for review.
- ⇒ The dream's *repo-side* proposals can be **a branch, not a proposal file**: dreamer edits its
  worktree, `_build_all.py` runs inside the worktree (§4.3 — gates score the dream *before* it even
  reaches Dave), Dave reviews the diff, merge = accept. Git-native accept/reject (¶171), zero new
  plumbing, and the record's "hash-before-write / deliberately not building" call stands — branches
  make compare-and-swap moot for this use.
- **Limit:** the worktree only covers the repo. The memory store lives outside it (see §3), so
  memory-side proposals need the proposal-file convention regardless.

### 1.5 Verdict on the record's §6 expectation

Sub-agents match the orchestrator+fleet pattern **directly**; worktrees give proposal-not-commit
isolation **for the repo**; workflows are a purpose-shaped substrate the record didn't anticipate.
The docs offer *more* than §4.2 assumed, not less. The thin part is elsewhere — §2.

## 2. VERIFIED — what the session-transcript tooling actually returns

Empirically checked this session, not assumed:

| Route | Reach | Fidelity | Verdict |
|---|---|---|---|
| Cowork `list_sessions` | **119 sessions**, titles + state + cwd | Titles are intact — the session-title convention is already functioning as a transcript index | Good |
| Cowork `read_transcript` | Any of the 119 | Rendered turns: user + assistant text in full; **tool calls as names only — no arguments, no results** | Semi-thin |
| Raw JSONL (this session's mount) | Own session only, in-sandbox | **Full fidelity**: `message` content incl. `tool_use` arguments, `toolUseResult`, timestamps, git branch | Full, narrow reach |
| Claude Code `~/.claude/projects/…/*.jsonl` (per docs, not locally verified) | All CC sessions + per-subagent transcripts (`subagents/agent-*.jsonl`) | Full JSONL | Full — but only covers CC-side work |

**Consequence for §4.2:** the talk's "read the tool calls, not just the turns" (¶153) is available at
full fidelity **only where raw JSONL is reachable**. A Cowork-hosted dream pass over the 119 sessions
reads *turn-level* patterns (what was said, what was claimed, which tools were named) but not tool
payloads. That is still enough for the highest-value patterns — repeated mistakes across sessions,
stale claims, ritual drift — because in this project the *receipts live in the repo*, not in tool
output. But it is a real ceiling, and it was right to verify before scoping.

## 3. Scope: §4.1 provenance + status (the DO-FIRST item)

### 3.1 A collision the record missed — surfaced, not papered over

The record names the gate `_validate_memory_provenance.py`, **blocking**. But the capture-ritual
runbook (step 3, ruled text) states: memory *"lives outside the repo: not in git, not pushed…
**invisible to the shell and to every gate**"* — and this session confirmed the sandbox mounts bear
that out. `_build_all.py` **cannot see the memory store**. The mirror that would have made it
visible was deleted BY RULING 2026-07-18 ("inscribed, not photocopied") and must not come back.

So §4.1 as written is unbuildable as a blocking gate *on memory files*. The honest split:

- **Repo surfaces** (`notes/`, `_DECISION-HISTORY/`, `GOOD-MORNING.md`) — gate-visible, blockable.
- **Memory files** — writable and checkable only by the session itself (file tools), i.e. ritual
  discipline + a checker the session *runs by hand*, same standing as today's pre-`_capture_gate.py`
  ritual. Not blockable at build time. Per the gate-glob-scope rule, the rule is only as wide as the
  gate's glob — claiming otherwise would be exactly the false inscription this programme exists to stop.

⚖ **D1 — where does the blocking gate bite?**
  (a) Repo-side only, honestly scoped (recommended: fields on notes/dossiers/GM claims, blocking;
      memory files carry the same fields by ritual, checked at wrap by the session, unenforced), or
  (b) also build the memory-side checker as a session-run script-of-record (repo-committed, run via
      file tools at ritual step 3, output pasted into the wrap) — more ceremony, closes the gap
      halfway, still not a gate.

### 3.2 Field spec (mechanical capture, never authored as prose)

Two fields, both surfaces:

```yaml
provenance: <session-id> · <YYYY-MM-DD>     # session id from the session's own path; date from `date`
status: observed | inferred | ruled | floated
```

- **Memory files**: two new keys under existing frontmatter `metadata:`. The session already knows
  both values mechanically (its id is in its filesystem path; date from `date` — never from belief,
  per the T-D12 incident).
- **Repo notes / dossiers**: same two lines in the existing header block. The record note already
  proto-carries them as prose ("Session:", "Status: … PROPOSED, not ruled") — this formalises what
  the best artifacts are already doing by hand.
- `ruled` is reserved: only writable when pointing at a ledger/ADR entry (promotion is Dave's alone —
  derivation-governance). The gate cross-checks that a `status: ruled` names its ledger.

⚖ **D2 — status vocabulary.** The record's §4.1 proposes four values, but its own §2 table needed a
fifth register: the two-hemispheres idea is *"standing hypothesis / essay"* — long-lived, Dave-owned,
not floated-and-forgotten, not ruled. Options: (a) add `standing` as a fifth value; (b) keep four and
mark the essay strand `floated` with longevity carried in prose. (a) is truer to the worked example
that motivated the whole field.

### 3.3 The gate: `_validate_provenance.py` (repo-side, blocking) + selftest

- **Glob:** `notes/*.md`, `_DECISION-HISTORY/*.md` (new files from a cutover date — no retro-fitting
  the corpus; assertion-propagation lesson: gate fires on flip, not on history).
- **FAIL:** missing `status:` on a new note/dossier · unknown status value · `status: ruled` with no
  ledger pointer · date ≠ a parseable date.
- **WARN:** provenance session-id that matches no known session title line (soft — titles rotate).
- **Selftest ships wired** (standing rule: selftests are build steps): feed it a fixture file per
  failure class, assert non-zero.
- Folds naturally into the already-specced `_capture_gate.py` (runbook § "The gate") — same
  front-matter machinery. ⚖ **D3:** build as one script (capture-gate finally exists, provenance
  checks inside it) or as a separate `_validate_provenance.py` beside it. One script is less
  plumbing; the runbook already owns the spec.

### 3.4 Which ritual step writes it

- **Step 3** (memory update): writes both fields on every new/changed memory file. One-line
  amendment to the runbook.
- **Step 1b/4** (dossier/note authoring): header carries both fields at write time.
- **Step 2** (GOOD-MORNING §B): "every landed claim names its evidence" — unchanged in spirit; the
  evidence line's format becomes `provenance:`-shaped so it can later be machine-read.

### 3.5 What it lets us DELETE (the leanness win, honestly sized)

- **Memory file bodies**: inline justification prose ("Why:" narratives restating session context)
  shrinks to the fact + a provenance pointer back to the session/dossier. The reasoning is
  retrievable, not re-inscribed. Estimated saving: the bulk of body text in `feedback`/`project`
  entries.
- **GOOD-MORNING**: §B evidence sentences compress to provenance-shaped lines; the 2c banner-roll
  precondition ("confirm durable content lives in its proper home") becomes checkable rather than
  eyeballed, which is what makes further banner trimming safe.
- **NOT deletable:** the status words in `MEMORY.md` index hooks. The hook is what's loaded at
  recall; status must survive *in the line that gets read* (trust-the-spine). The win is in bodies
  and GM prose, not the index. The record's "~90 hooks" framing slightly oversold this — corrected here.

### 3.6 Estimate

Unchanged from the record: ≈ one afternoon. Field spec + runbook amendments + gate-with-selftest +
cutover note. No corpus retrofit.

## 4. §4.2 re-scoped against what was found (build shape only — not started)

Two viable shapes, not one:

- **Shape A — Cowork-native (available today):** scheduled task (nightly/weekly) runs a session that
  reads `MEMORY.md` + `GOOD-MORNING.md` + `_LIVE-STATE.md` + last-N transcripts via `read_transcript`,
  emits `notes/_dream/YYYY-MM-DD-proposals.md` with evidence + prevalence per proposal. Turn-level
  fidelity only (§2 ceiling). Cheap, on-cadence, zero new infrastructure.
- **Shape B — Claude Code-native (fuller):** a `dreamer` agent definition (+ optionally a saved
  workflow) fanning readers over raw JSONLs, **worktree-isolated**, running `_build_all.py` in its
  worktree so proposals arrive pre-scored by the 53 gates (§4.3 fused in), delivered as a branch.
  Full ¶153 fidelity for CC-side sessions; needs Dave working CC-side for the transcripts to exist.

⚖ **D4 — sequence.** Recommended: §4.1 first (unchanged), then Shape A as the first dream pass
(prove the loop on cheap fidelity), then Shape B when the harness-spinoff work gives it a home.
§4.3 attaches to either shape; it is near-free only in Shape B (gates run in the worktree).

## 5. Deferred / owed

- **Convergence note `-v2`**: NOT done. The source note wasn't re-attached and revising it from the
  record's summary of it would be exactly the confident-false-inscription failure. **Re-attach
  `2026-07-26-convergence-anthropic-dreaming.md` and it's a one-sitting job** — the fix list is fully
  specified in the record (§2 registers, §3 three verb fixes, databases-Q&A subsection, §5/§6 reorder).
- **Git**: last session ran no git. Uncommitted at session start: the record note, the transcript,
  `notes/2026-07-25-claude-code-orchestration-survey.md`, modified `_FUTURE-STATE.md`. This note adds
  itself. One paste-ready commit prepared at wrap.

## 6. Decision points, gathered

| # | Question | Recommendation |
|---|---|---|
| D1 | Gate bite: repo-side only, or + session-run memory checker | (a) repo-side only, honest scope |
| D2 | Status vocab: 4 values or 5 (`standing`) | 5 — the worked example demanded it |
| D3 | One `_capture_gate.py` or separate `_validate_provenance.py` | One script |
| D4 | Sequence: 4.1 → Shape A → Shape B | As stated |

Dave rules; nothing above is recorded as ruled.
