provenance: sub-produced (read-only audit agent) · 2026-07-31 · target = `notes/2026-07-25-claude-code-orchestration-survey.md`

# DRAFT — sub-produced, awaiting conductor replay + Dave's ratification

Delta audit of the 2026-07-25 orchestration survey (Dave's #62 caveat: BASE, never current
truth). Six sessions have moved (#57–#64/#65-opener) since the survey was committed. Method:
every numbered claim below is re-verified against the repo as it stands now — `git log`, file
reads, `grep`/`wc` counts — never against the survey's own prose or a banner.

## (a) Exec summary

**HOLDS 12 · MOVED 8 · DEAD 3 · UNVERIFIABLE 7** (of 30 numbered claims).

> ★ CORRECTED AT CONDUCTOR REPLAY (#65). The sub's original line here claimed
> **14 · 9 · 2 · 5** "tallied by eye — no script". Re-measured on this table with a named
> instrument (`awk` on the Verdict column, rule: **primary verdict = first token of the cell**)
> the table returns 12 · 8 · 3 · 7; total 30 both ways, split irreproducible under any single
> counting rule tried. Cause attributed, not just blamed: rows **6** and **27** carry compound
> verdicts and row **28** is "DEAD (the target half)" — a count over such cells is
> instrument-dependent unless the rule is declared. This is the #64 defect class (a recalled
> count wearing a measurement's clothes) caught live at replay. The per-row verdicts and quoted
> evidence were spot-checked and stand; only this summary arithmetic was soft.
> Compound rows flagged for reading: 6 (UNVERIFIABLE ext / HOLDS repo part) ·
> 27 (MOVED 1/5 · HOLDS 2/5 · UNVERIFIABLE 2/5) · 28 (DEAD, target half only).

Five deltas that matter most for the package build:

1. **The boot artefact changed under the survey's feet.** The survey (committed `dfdc857`,
   2026-07-26) and its sibling `notes/2026-07-23-harness-framework-spinoff.md` both describe the
   invariant layer as "GOOD-MORNING §A/§B/§C". `_CHAIN.md` + `knowledge/_gen_chain.py` did not
   exist until `bb47693`, 2026-07-29 — three days later. The package spec already has this right
   (chain + retrieval, not §A); the survey and its neighbour note do not. **Port the chain
   mechanism, not the §A description in either 07-2x note.**
2. **The strategic question the survey left "NOT ruled" has since been ruled and acted on.**
   `memento-package/_PACKAGE-SPEC.md` (born 2026-07-31, commit `cca7952`) is the harness-as-
   portable-layer idea, live, with Dave's boundary attached. The survey's own proposed reframe
   ("a layer on top of upstream orchestration") is superseded by an actual package birth, not
   still a floated idea.
3. **The delegation/multi-window model the survey called "Built-in version of the ratified
   model" has itself moved twice since**: #57 (`0ab37aa`, 2026-07-30, "rule delegation in") and
   #60 (`643aae3`, 2026-07-31, "delegation measured at 46:1... multi-window ruled with two use
   cases and a cap of 3"). The survey's mapping row is directionally right but names a model that
   has since been measured and re-ruled, not the one it pointed at.
4. **Constraint #2 (legend v5.x queued, no mid-stream swap) is dead.** Legend wave signed off
   `111ff49` (2026-07-26) and closed `ba336dc` (2026-07-27) — both inside the six sessions this
   audit covers. The constraint that made this "notes-only" is gone; it is not a reason to hold
   back the package build today.
5. **A "Feeds" pointer never landed.** The survey promises the harness-spinoff reframe would feed
   `notes/2026-07-23-harness-framework-spinoff.md`; `git log` on that file shows exactly one
   commit (`db1ed1b`, 2026-07-23) and no edit since — the reframe was never written there. If the
   package build wants that note's context, the reframe still needs porting by hand.

## (b) Per-claim table

Legend: **P** = provenance/session-metadata claim · **M** = mapping-table row · **C** =
constraint · **V** = vision-touch · **F** = feeds · **X** = external Claude-Code product-feature
claim (see scoping note below table).

| # | Claim (paraphrased, source line) | Verdict | Evidence |
|---|---|---|---|
| 1 (P) | Survey "Recorded 2026-07-25 (legend-v5.3 session, Fable)" | MOVED | Committed `dfdc857`, **2026-07-26 15:46:30 +0100** (`git log --follow` on the file) — the filename/date-stamp is off by a day from the actual commit; legend-v5.3 itself lands in `fb340bc` same window. Not load-bearing, but a dated claim that doesn't match `git log`. |
| 2 (P) | "Ruling status: NOTES ONLY... no architecture change now" | HOLDS | True as a historical record of what was decided that session — nothing in the repo retroactively changes what was ruled that day. |
| 3 (P) | Trigger = X thread by @0xCodez + six Claude Code docs pages, "verified against code.claude.com/docs" | UNVERIFIABLE | Probe would be a live fetch of code.claude.com docs pages to diff against 2026-07-25 content; out of this audit's repo-state scope (task rule 4: verify against git log/files, not external docs currency) and no vendored copy exists in-repo to diff against. Treated as a frozen historical observation, not re-checked. |
| 4 (X) | Dynamic workflows feature spec (v2.1.154+, `agent()`/`parallel()`/`pipeline()`, caps 16/1,000, `.claude/workflows/`) | UNVERIFIABLE | Same as #3 — external product-doc claim, no in-repo artefact to check against; scoped out. |
| 5 (X) | Agent teams (experimental flag, lead+teammates, no worktree isolation) | UNVERIFIABLE | Same as #3. |
| 6 (X) | Subagents: `memory:` scopes + `MEMORY.md` (200 lines/25KB preload), `isolation: worktree` | UNVERIFIABLE (external spec) / **HOLDS (repo-observable part)** | The `isolation: worktree` claim is independently checkable: this audit's own Agent tool schema (visible in this session) currently exposes `"isolation": {"enum": ["worktree", "remote"]}`. `worktree` still present — HOLDS. `remote` is new since the survey (see #21). |
| 7 (X) | Agent view / worktrees (`claude agents`, `.worktreeinclude`, `EnterWorktree`) | UNVERIFIABLE | External product-doc claim, scoped out per #3. |
| 8 (M) | Row: "Workflow script holds the plan" ↔ "DIVVY PLAN prose in handoffs" | HOLDS | MEMORY.md (current, loaded this session): "[Parallel-session conductor]... DIVVY PLAN per handoff" — the mechanism is still named and standing. |
| 9 (M) | Row: "Stage-per-workflow for sign-off" ↔ "Dave's sign-off gates between waves" | HOLDS | No repo artefact contradicts this; sign-off gates remain the operative pattern (e.g. legend wave sign-off closures `111ff49`/`ba336dc`, below). |
| 10 (M) | Row: "`TaskCompleted` exit-2 hook" ↔ "verification = enforcement" | HOLDS | `knowledge/_A11Y-AUDIT.md:74` heading "What's now enforced (verification = enforcement)"; `knowledge/_HANDOFF-component-review.md:42` "**Gates** (verification = enforcement):" — the exact phrase is still live in two files. |
| 11 (M) | Row: "Adversarial verify / judge panels" ↔ "adversary-auditor gate" | HOLDS | MEMORY.md current: "[Adversarial densify]... keep the adversary-auditor GATE" — standing, unretired. |
| 12 (M) | Row: "Per-node `model` routing" ↔ "MODEL-ROUTING.md" | MOVED | `MODEL-ROUTING.md` exists (root, 11,244 bytes, last touched 2026-07-30). Since the survey, commit `8d962b0` "Inscribe budget-aware routing governor" adds machinery on top of the file the survey pointed at — the mapping still holds, the target has grown a governor since. |
| 13 (M) | Row: "Subagent `memory:` + MEMORY.md" ↔ "tattoo architecture, per-role" | HOLDS | MEMORY.md current: "[Memento framing]... tattoos vs Polaroids" — the tattoo/Polaroid vocabulary is still the standing frame, referenced as recently as memory entry `memento-framing.md` (#62 content). |
| 14 (M) | Row: "Teams lead/teammates + task list" ↔ "conductor/worker + divvy... Built-in version of the ratified model" | MOVED | The "ratified model" the survey points at has itself moved twice post-survey: `0ab37aa` (2026-07-30, "rule delegation in") and `643aae3` (2026-07-31, "delegation measured at 46:1... multi-window ruled, cap of 3"). MEMORY.md current confirms: "[★★ Delegation inversion RULED #57]... subs BY DEFAULT... multi-window settled #60-D1 (cap 3, Claude offers/Dave vetoes)". The row's *shape* still holds; the specific ruling it names has been superseded by a later, measured one. |
| 15 (M) | Row: "Teammate file partitioning" ↔ "worktree-reconcile rule" | HOLDS | MEMORY.md current: "[Working-tree reconcile + breadcrumb]... shared dirty tree → reconcile every path" — standing. |
| 16 (M) | Row: "Subagent transcripts survive compaction" ↔ "context-gauge flush ritual" | MOVED | The exact phrase "flush ritual" appears only in this survey and once more in `notes/2026-07-29-context-degradation-research.md:283`, where it is listed as a **future/automated horizon**, not current practice: `"Server-side compaction (beta, 4.6+) — the flush ritual, automated — horizon"`. Current canon vocabulary (MEMORY.md, "[★★ Gauge = REAL tokens...]") is **"write findings home MID-window"**, not "flush ritual" — same underlying relief mechanism, different and more current naming. |
| 17 (C) | Constraint 1: "Cowork Agent tool has `isolation: worktree`" (parity gap logged as `product-feedback-cowork-parity`) | MOVED | `isolation: worktree` still present (confirmed on this session's own Agent tool schema) **and** the same schema now also offers `isolation: remote` ("launches the agent in a remote cloud environment") — a capability absent from the survey's observation. The parity-gap memory itself is still indexed: MEMORY.md current, "[Product feedback: Cowork↔Code parity]... Dave wants slash-commands in Cowork". |
| 18 (C) | Constraint 2: "Legend v5.x sign-off + hit-area gate + donut/bar/combo wave are queued — no mid-stream process swap" | DEAD | Premise killed by three commits inside the audited window: `85d31d3` (2026-07-25, hit-area 44 canon patch — same day, later than the survey's session) · `111ff49` (2026-07-26, "Legend v5.x SIGNED OFF") · `ba336dc` (2026-07-27, "Legend wave CLOSED (combo + line migrated)"). The constraint that justified "notes-only, no process swap" no longer exists. |
| 19 (C) | Constraint 3: "Teams = experimental + no teammate worktrees; workflows = no mid-run rulings" | UNVERIFIABLE (external) | Same scoping as #3–#7; this is a Claude-Code product fact, not a repo fact. The internal half of the sentence — "the chart exemplar's six refinements came from watch-and-intervene" — is independently corroborated verbatim in `_FUTURE-STATE.md:227` ("the chart exemplar's SIX refinements came this way"), so the *reasoning* this constraint rests on still holds even though the product-spec half is unverified here. |
| 20 (V) | Vision touch 1: "production line IS a workflow" (pipeline mental model → workflow script) | HOLDS (still unruled) | `grep` across all `.md` files for "production line IS a workflow" / "Dispatch delivery vehicle" returns only this survey — the idea has not been enacted or re-raised elsewhere. Status is unchanged from the survey's own framing: floated, not ruled. |
| 21 (V) | Vision touch 2: "Dispatch delivery vehicle... could ship as an Apollo plugin" | HOLDS (still unruled) | Same probe as #20 — no other file references this; ADR-0008 (`docs/decisions/ADR-0008-canonical-core-and-adapters.md`, confirmed present, **Status: accepted**, dated 2026-07-20) still exists as the pattern this idea would extend, unchanged. |
| 22 (V) | Vision touch 3: "Register = inference ramp (charter §9)... per-node model routing = inference-tiering as a platform primitive" | HOLDS | `knowledge/_FIXED-FLEX-CHARTER.md:124` — "## 9. Register = an inference ramp (ranked curbs) — ratified 2026-07-03 (Dave) (CHARTER.S9)" — the charter section this touch depends on is present and still ratified, predating and unaffected by the survey. |
| 23 (F) | Feeds 1: "`_FUTURE-STATE.md` → 'Parallel windows vs subagents' entry... a THIRD mechanism" | HOLDS | `_FUTURE-STATE.md:220` "## ★ Parallel windows vs subagents..." and `_FUTURE-STATE.md:243` "**UPDATE 2026-07-25 — a THIRD mechanism surveyed (notes-only, NOT ruled):**..." — the entry exists and explicitly cites the survey by filename. Confirmed present, unedited status since. |
| 24 (F) | Feeds 2: "the multi-thread GOOD-MORNING entry" | MOVED | The entry itself (`_FUTURE-STATE.md` §"Parallel windows vs subagents", referencing "the multi-thread problem above") still exists, but its target description — "GOOD-MORNING entry" — is stale in the same way as claim #1's central finding: GOOD-MORNING.md is no longer the boot-read surface; `_CHAIN.md` is (see exec summary #1). The pointer resolves to a file that has changed role since. |
| 25 (F) | Feeds 3: "`notes/2026-07-23-harness-framework-spinoff.md` (reframe above)" | DEAD | `git log --follow` on that file shows **exactly one commit**, `db1ed1b` (2026-07-23, the file's creation) — no edit since, so the "layer on top of upstream, not competitor" reframe promised by this survey was never written into it. `grep -n "productis\|layer on top\|upstream\|competitor"` against the file returns no matches. The feed was declared and never enacted. |
| 26 (F) | Feeds 4: memory `harness-framework-spinoff` | UNVERIFIABLE | This is a pointer into the external Claude memory store (`.../spaces/.../memory/*.md`), not a repo path; current MEMORY.md (loaded this session) does not list `harness-framework-spinoff` among its active entries, and it is not in the "Moved #64" archive line either — cannot confirm its live content or status from inside the repo. Named probe: would need direct read access to the memory-store path outside this session's mounted folder, which this audit does not have. |
| 27 (F) | Wikilink feeds: `[[pipeline-mental-model]]` · `[[apollo-canonical-core-adapters]]` · `[[register-inference-ramp]]` · `[[chat-to-kb-bot]]` · `[[kb-distillation-at-deploy]]` | MOVED (1 of 5) / HOLDS (2 of 5) / UNVERIFIABLE (2 of 5) | `register-inference-ramp` and `kb-distillation-at-deploy` both still appear live in `_FUTURE-STATE.md` (lines 634, 683) — HOLDS. `apollo-canonical-core-adapters` is explicitly named in MEMORY.md's current "Moved #64" archive line — MOVED to `MEMORY-ARCHIVE.md`, no longer top-level-loaded. `pipeline-mental-model` and `chat-to-kb-bot` are not found in any live repo file (only in the 2026-07-18 `_retired/` snapshot) and are not in MEMORY.md's active or archived list — UNVERIFIABLE from inside this repo (same probe/limitation as #26). |
| 28 (M/X) | "Harness design target" steer: Copilot adapter mapping `AGENTS.md ← GM §A standing orientation` | DEAD (the target half) | `AGENTS.md` exists at repo root (confirmed, 7,270 bytes) — the Copilot side of this mapping still stands. But the thing it's mapped *from*, "GM §A standing orientation" as the thing a cold session reads, is exactly the premise `_CHAIN.md` replaced (`bb47693`, 2026-07-29): `_CHAIN.md`'s own header says "⚠ Do NOT now open GOOD-MORNING.md to 'check' ... §A orientation is `gm:A` (a router with 11 children)... retrieval, never a reading list." The mapping needs re-pointing at the chain + retrieval shape, per the package spec's own framing. |
| 29 (P) | "the create-cowork-plugin skill exists" (implied via package spec, echoed context) | HOLDS | Confirmed directly: this session's own skill listing includes `cowork-plugin-management:create-cowork-plugin`. |
| 30 (V) | Overall strategic implication: "spin-off = a layer on top of upstream orchestration, not a competitor... NOT RULED" | MOVED | No longer an open question in the same sense — `memento-package/_PACKAGE-SPEC.md` (born `cca7952`, 2026-07-31) is Dave's actual ruling on packaging: a real folder, a real boundary, a real boot rule, ratification "owed at #65's opener." The survey's "NOT RULED" framing describes a state the repo has since moved past into "ratified with one item outstanding" (ledger, per `_CHAIN.md`'s ★ LATEST banner: "Ratification owed at the #65 opener"). |

## (c) What this means for the port

Given current state, the package build should copy/reference:

- **Boot mechanism:** `knowledge/_gen_chain.py` (generator) + `_CHAIN.md` (the generated
  artefact) + `knowledge/_memento_search.py` (retrieval) — **not** any GOOD-MORNING.md §A
  description carried over from the survey or from `notes/2026-07-23-harness-framework-spinoff.md`.
  Both those documents predate the chain by 3 days and describe a superseded boot shape (claim
  #1, #28).
- **Capture ritual + record-guarding gates:** already scoped correctly by
  `memento-package/_PACKAGE-SPEC.md` — no delta found here; the spec's own text matches current
  practice (verification=enforcement claim #10, adversary-auditor claim #11 both still standing).
- **Delegation/conductor-worker model:** if the package documents "how subagents get used," pull
  from the #57/#60 rulings (`0ab37aa`, `643aae3` — "subs BY DEFAULT," measured 46:1, multi-window
  cap 3), not from the survey's "Built-in version of the ratified model" row, which points at a
  since-superseded state (claim #14).
- **Do NOT re-import** the dead Legend-wave constraint (claim #18) as a reason to gate the
  package build — that blocker cleared 2026-07-26/27, inside the audited window.
- **Outstanding, not this audit's job to close:** the never-landed reframe feed into
  `notes/2026-07-23-harness-framework-spinoff.md` (claim #25) and the two memory-store pointers
  this audit could not resolve from inside the repo (`harness-framework-spinoff`,
  `pipeline-mental-model`, `chat-to-kb-bot` — claims #26–27). ★ **RESOLVED AT CONDUCTOR
  REPLAY (#65): all three exist as named files in the memory store** (probe: `Grep` over the
  store for the three slugs; each matched on its own `name:` frontmatter line). The pointers
  are live; the sub's UNVERIFIABLE stands as correct *for its repo-only scope*, discharged
  here by the layer that holds the store. The never-landed reframe feed (claim #25) remains
  genuinely outstanding.

## Scoping note on external (X) claims

Six sessions moving the repo does not move Anthropic's or GitHub's product documentation. Claims
about Claude Code feature specifics (dynamic workflows, agent teams, subagent memory internals,
agent view, Copilot's `AGENTS.md`/custom-agents shape, org push-distribution) are **historical
observations frozen at 2026-07-25**, not repo-state claims — this audit's mandate (task rule 4)
is to verify against `git log`/files, and there is no in-repo vendored copy of those docs to diff
against. They are marked UNVERIFIABLE-by-repo-scope above rather than assumed true or re-derived
from general knowledge. Where a claim had an independently repo-observable half (e.g. `isolation:
worktree` on the Agent tool, claim #6/#17), that half was checked and reported separately.
