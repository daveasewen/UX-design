# _LIVE-STATE — what's true now (cold-start spine)

*The supersession ledger for the project: what's **LIVE**, what's **DEAD** (don't build on it),
what's **OPEN**. Read this second, after `GOOD-MORNING.md`, before `knowledge/README.md`.
Per **ADR-0007**. ⚠️ **INTERIM — hand-maintained** until `_build_live_state.py` generates it from
front-matter edges + tombstones. Refresh at end of every session alongside the handoff.*

*Last refreshed: 2026-07-05.*

> ⚠️ **AUDIT STATUS — everything below is RECORDED, not VALIDATED.** Provenance ≠ correctness.
> These entries capture *that* a decision was made and what it supersedes — **not** that it is
> right. Treat every node as **`unaudited`** until a human correctness-audit vouches it (ADR-0007).
> The ledger tells you what's live/dead; it does **not** endorse. Don't mistake a clean node for a
> vetted one.

---

## LIVE — current truth (in force)

- **Product = a *flexing* engine** — one governed core, dials per work-type; floor/churn ("vibe")
  vs ceiling/novel ("analysis"). `ADR-0006`.
- **Output modes = a first-class dial** (Dave, 2026-07-05): the engine must produce **two fidelity
  tiers** — (1) **"dumber" portable HTML-component prototypes** (library-agnostic, no build; the
  portability floor) and (2) **build-ready output from a prebuilt library**, with **Sutherland** (the
  HSBC React lib) the intended build target ("build directly using Sutherland"). **Portability =
  NOT married to Sutherland** — dumb-HTML mode, or ingest other libraries, or whatever strategy wins;
  Sutherland is *a* target, not *the* architecture. Note the two-way tie: our **dark-mode work feeds
  back INTO Sutherland** while Sutherland is also our **build target** (same artifact up- and
  downstream); the **Figma library IS Sutherland's working file.** Memories: `output-modes-portability`,
  `sutherland-figma-mapping`. Unaudited node (extends ADR-0006).
- **Register = an inference ramp** (NOT a look): sober = retrieve · balanced = extend ·
  expressive = invent. Charter `_FIXED-FLEX-CHARTER.md` **§9**.
- **§9a — provenance of "reads HSBC"**: brand-ness resolves to named sources (primitives→token
  store · composition→`canon/canon.css` · character→`brand-principles.md` · tone→§4b · red→
  `colour-usage.md`); flag-where-silent is an advisory generation behaviour; residual gestalt =
  human. Brand-source-stop column on the §9 band table. Record:
  `knowledge/_PROVENANCE-inference-levels_2026-07-04.md`.
- **Two harness modes** (§9a): converge/ship = **mode B** advisory brand self-check (ADOPTED) ·
  explore/noodle = **mode A** open human gestalt (OPEN). Mode = a first-class harness dial.
  Memory: `harness-two-modes`.
- **Project memory = temporal decision-graph pattern**, lightweight-first; **this file is the
  cold-start spine.** `ADR-0007`. Memory: `pm-knowledge-graph-direction`.
- **Supersession discipline** (non-negotiable, `AGENTS.md`): any ruling that kills something must
  tombstone the artifact + log the propagation gap in the same pass.
- **Git split** (`AGENTS.md` + memory `git-push-method`; no standalone ADR): Claude commits in terminal + clears
  stale `.git/*.lock`; **Dave pushes via GitHub Desktop only** (never terminal push, never Desktop
  commit, Desktop closed during commits).
- **Build**: `python3 knowledge/_build_all.py` — runs the full gate set (integrity · contrast ·
  snippet · icon-source · a11y · coverage · dark-surface · rules-index); green = internally
  consistent, dark-legible, surfaces not flat-white, snippets match canon. *(Doc-drift: older notes
  say "four gates" — it's ~8; fix on the Tier-B build-gate audit.)*
- **State machine records FUTURE/TARGET states too** (RULED 2026-07-05, Dave; extends `ADR-0007`):
  this ledger carries not just current truth + change history but **where we intend to be** — see the
  `## PLANNED / TARGET STATES` section below. A target = what · why · blockers · source. The
  staleness gate must flag a target whose blockers have cleared but whose status still reads
  "blocked" (the Sutherland failure). This ruling is itself an `unaudited` decision node (extends the
  vouched ADR-0007).

## SUPERSEDED / DEAD — do not build on

- `knowledge/_fitness-test/sme-payments-registers.html` — old **looks-based** register dial
  (surface/accent/motion knobs). → superseded-by charter §9 (2026-07-05). Tombstoned.
- Register-as-"described-look" (dark band / hero / gradient) — → superseded by §9 inference ramp
  (2026-07-03).
- Terminal-only push / "GitHub Desktop retired" (07-02 ruling) — → superseded by the git split
  (07-05).
- `knowledge/_NEXT-SESSION.md` — retired, → superseded by `GOOD-MORNING.md`.

## OPEN — propagation gaps + parked threads

- **⚠️ PROPAGATION GAP:** the product vision still speaks the OLD looks-language — `ADR-0006` +
  `_VISION-iteration-machine_2026-07-03.html` say "cool/warm/hot register switch" with surface-band
  moments (the mock even has a `border-radius:10px` cardinal violation). Reconcile with §9
  inference-def when next in that area.
- **No worked spread exists under the new inference definition yet** — the looks→inference shift
  landed in the charter only.
- **Divergence probe — PARKED** behind the missing inference-era spread. Build a real
  retrieve/extend/invent spread on one screen first; the probe then measures **inference
  separation** (tier/candidate count), not look-distance.
- **Named-not-built harness machinery** (§9/§9a): isolated generation · divergence probe · mode-B
  brand self-check · the mode dial.
- **PM-KG MVP** (`ADR-0007`): build `_build_live_state.py` + the staleness gate — own focused
  session.
- **✅ Decision-corpus correctness audit — TIER A CLEAN 2026-07-05 (ADR-0007 §5).** Method:
  `knowledge/_RUNBOOK-decision-audit.md`; ledger: `knowledge/_DECISION-AUDIT.md`. Batches 1–3 run in
  fresh sessions. Batch 1: **ADR-0005 vouch · ADR-0007 vouch · §9/§9a vouch(framing)+defer(proven) ·
  ADR-0006 amend · `derivation-governance` amend.** Batch 2: **ADR-0006 re-audit vouch ·
  `derivation-governance` re-audit split · ADR-0001 vouch · ADR-0002 vouch · ADR-0003 defer ·
  ADR-0004 vouch+rationale-amend.** Batch 3: **charter §4 amend+defer · charter §4b defer ·
  two-harness-modes defer(kept A) · supersession-discipline vouch;** triage **git-split → Tier B ·
  build-gate → Tier B (fast-follower).** **Every Tier A node now has a verdict — the milestone that
  retires the "everything is unaudited" risk for foundational nodes.** Standing OPEN follow-ups:
  §9 proof-obligation · ADR-0003 KG/ingestion · §4 language-strip · TOV content audit ·
  harness-modes exploration. **Next audit work: Tier B opportunistically (feedback/project memories,
  runbook rules) + Tier C by sample/on-touch — NOT the priority; per Dave the next session is the
  seaworthiness planning run.** Never run the audit in a loaded session.
  - **Operational follow-ups from ADR-0004 (07-05, not correctness faults):** (a) **verify current
    EAA / EN 301 549 legal position** (2026-05-31 legal facts are point-in-time); (b) the installed
    `design:accessibility-review` skill audits to **WCAG 2.1 AA** — align to the project's 2.2-AA
    bar; (c) `wcag_version` config param survives only in `archive/harness-v0.1/`, live engine
    hard-targets 2.2. Foundational driver now recorded in ADR-0004: HSBC aspiration = *most digitally
    accessible bank in the world* (bar leads, not complies; ratchets over time).
  - **⚠️ AUDIT-DEFERRED verification (charter §9/§9a) — DO NOT FORGET (Dave, 07-05).** The
    inference-ramp *framing* is vouched, but its *proven/safe* status is **deferred** pending: (a)
    the first worked retrieve/extend/invent spread on one screen, and (b) the divergence probe +
    isolated generation + mode-B self-check (all named-not-built). These are the same items in the
    "no worked spread" / "named-not-built harness machinery" bullets above — now carrying an
    explicit audit obligation, not just a build backlog. Re-audit §9/§9a's proven status once a
    spread exists.
  - **Re-audit obligation (two amended nodes).** ADR-0006 (register dial corrected to §9 inference
    ramp) and `derivation-governance` (staged multi-human promotion path) were **amended** in the
    audit; their amended text **re-enters `unaudited`** and must be re-audited in a later batch.
  - **OPEN thread — staged-promotion / extension-library process (from `derivation-governance`
    amend).** Define how inference-born ideas move: holding-pen/sandbox → colleague review →
    "extension library" (separate-but-connected canon) → general canon if broadly useful. Not yet
    worked out; connects to the ADR-0006 compounding-canon promote loop + `gap-pattern-build`.
    **Re-audited 07-05 (batch 2): direction VOUCHED, mechanism DEFERRED — kept OPEN not banked.**
    **FUTURE FEATURE (Dave, 07-05 — capture-only, build once the goal is set):** tiered access to
    canon commits — roles **design-system admin → domain admin → standard**; **sandbox open to
    everyone**, **commits tiered**; **extension libraries readable by all, edit privileges gated by
    domain + commit right**; general-canon promotion still needs the multi-human bar. Set the goal
    first, then the access model falls out of it.
- **⭐ NEW — Harness modes + dials exploration (from two-harness-modes defer, 07-05 batch 3).**
  Kept **Tier A** but **DEFERRED** — abstract/named-not-built, inherits §9a (framing vouched, proven
  deferred). **Dave's reflections to carry:** the harness must be **flexible to a degree** — the modes
  might be a **clean switch, or both** (a simple toggle *plus* an **advanced mode** to tune it); maybe
  even a **"let it rip" mode** (for fun); **finding the use cases is the important part**; approach =
  **research + iterate, start small, expand if needed**; the **dials themselves may need exploration,
  and that exploration may define the settings/toggle**. Own research thread — not the audit. Memory:
  `harness-two-modes`; ledger: `_DECISION-AUDIT.md`.
- **⭐ NEW — Tone-of-voice (TOV) = digital-editorial spin-off + future content audit (from §4b defer, 07-05 batch 3).**
  §4b deferred. Dave's framing: **TOV is genuinely useful for DIGITAL EDITORIAL** and is a **candidate
  spin-off thread** (its own home, separate from the interface engine). For **interfaces it is NOT a
  priority** — the exception is guidance for the **neutral decisions: labelling, language/locale,
  formality**. The wit-licence-per-band mapping can't be vouched without **auditing the actual TOV
  content** (tov-001…051) against the KG — a **possible future thread**, not this audit. Tagged on
  memory `tone-of-voice-ingest`. Ledger: `_DECISION-AUDIT.md` (§4b).
- **⭐ NEW — Charter §4 language-strip (HARD follow-up, from §4 amend+defer, 07-05 batch 3).**
  Audit ruled §4 **amend + defer**: the ramp is governed ONLY by cardinal + foundational curbs +
  inference levels + full compliance, all **retrieved from the KG** — §4's interpretive *language*
  (prose rulings on flatness/red/rounding) is recall-by-adjective (§9/§9a) and must be **stripped**,
  leaving the four curbs only as KG-sourced curb/level derivations. Dave flagged this as a **HARD
  follow-up**, not a quick edit — **do it inside the unified-KG/ingestion thread below, not as a
  standalone charter tweak.** Completeness of the derivations is **deferred** (unprovable until
  ingestion is finished). §4's amended text will re-enter `unaudited`. Ledger: `_DECISION-AUDIT.md`.
- **⭐ NEW — Unified DS knowledge-graph + ingestion, done right (from ADR-0003 defer, 07-05).**
  ADR-0003 was **deferred** (not vouched): Dave reopened the founding instinct that the *whole*
  design-system corpus (component specs, foundations, tokens, snippets, create.hsbc guidelines) is
  **one interlinked graph**. Today that interlink lives only inside the compliance graph. **Root
  cause: ingestion was never completed** (attempted, curtailed). This is a **separate, structured
  work thread with its own audit-grade method** — stated aim: do it correctly this time. Scope:
  map the entity/edge model across the full corpus; decide keep-hybrid / go-unified / **overlay-
  index layer** (leading hypothesis — link across existing stores, don't collapse into one monolith;
  extends `_blast-radius.json` / `graph-index.json`); connect to `graphify-tool` + ADR-0007 infra.
  Memory: `ds-knowledge-graph-revisit`. **Own focused session — not the audit.**
- **✅ Seaworthiness plan — DONE 2026-07-05 → `_SEAWORTHINESS-PLAN_2026-07-05.md`.** Curated,
  dependency-aware sequence (not a flat backlog): hull patches (ingestion Phase 0 + capture ritual) →
  **big-rock #1 Ingestion Phase 1** (Sutherland token migration, confirmed unblocked) → **§9 worked
  spread in parallel** → **big-rock #2 PM-KG MVP** (staleness gate) → finish/unify (Phase 2→3→4, with
  the §4 language-strip inside Phase 3). Waiting/parked (D2, toolkit t2, harness-modes, TOV spin-off,
  ADR-0004 ops) kept off the critical path. Capture ritual/gate spec decided in the doc (ritual now,
  gate script alongside PM-KG MVP).
- **✅ Phase 0 (ingestion tracking hygiene) — CLOSED 2026-07-05.** The "39 metas vs 38 in the
  compliance graph" drift flagged in the prior session's KG spot-check was a **false alarm**: 39
  files exist in `components/`, but one (`EXAMPLE-button.meta.json`) is the authoring template,
  correctly excluded by `_build_compliance_kg.py`. Real component count is 38, matching the graph
  exactly. Rebuilt the KG to confirm — `git diff` on `compliance/graph-index.json` and `compliance/rules/`
  was **empty**; the graph was already current. Fixed a latent bug while here: `generated` was a
  hardcoded literal (`"2026-06-18"`) rather than today's date — a miniature of the exact
  "tracking rots silently" failure this plan exists to prevent; now stamps dynamically
  (`datetime.date.today()`). The `_DESIGN-SYSTEM-GAPS.md` correction banner + `_INGESTION-ASSESSMENT_2026-07-05.md`
  as single entry point both confirmed standing. Phase 0 fully closed; Phase 1 (Sutherland token
  migration) is next and is real, unblocked work — unlike this drift.
- **D2 — novel-screen test — THE #1 unlock.** Waiting on a colleague's brief (their brief-v2 +
  own baseline + signed contract *before* generation). `_TEST-PLAN-novel-screen-proof.md`.
- **Toolkit tranche 2** (Dropdowns ×4) — parallel cheap-model workstream. Memory:
  `common-toolkit-survey`.

## PLANNED / TARGET STATES — where we intend to be (for planning, per ADR-0007 extension)

*The forward-looking dimension of the state machine. Not current truth (that's LIVE) and not a flat
backlog (that's OPEN) — these are intended end-states with a path. Refresh alongside LIVE/DEAD/OPEN.*

- **🎯 Ingestion "done right".** Full detail + phased worklist: **`knowledge/_INGESTION-ASSESSMENT_2026-07-05.md`** (cockroach doc — cold-start-proof, evidence-cited).
  - **Target:** every ingested entity (guideline rule · token · component · snippet · success-
    criterion) addressable in **one interlinked graph or an overlay/index layer** across the existing
    stores; token store **Sutherland-canonical** with the **147 depricate tokens retired**;
    completeness measured as **edge coverage**, not pages processed.
  - **Current vs target:** 3 siloed stores + 1 narrow graph (WCAG↔component only); guidelines 462
    rules (Tier 1 done, Tier 2 tail + 21 legacy open); tokens half-migrated.
  - **Blockers:** **Sutherland export NO LONGER a blocker** (arrived 2026-06-17; the gaps manifest is
    STALE and still says "parked" — Phase 0 fix). Remaining work is ours, not a wait.
  - **Path:** Phase 0 un-stale tracking → Phase 1 execute Sutherland token migration (rebind 147
    depricates → verify → delete; close P1/P3/P4) → Phase 2 finish guidelines capture → Phase 3 build
    the overlay/index graph (ADR-0003 "done right", audit-grade) → Phase 4 wire ingestion coverage
    into this machine as a tracked target.

## SPIN-OFF / GENERALISABLE CANDIDATES — surface, don't bury (Dave, 2026-07-05)

*Tools/methods built here that may generalise to other projects — treat like company spin-offs.
Also the place to surface **whole new projects that emerge mid-chat**. Flag when something proves
reusable; don't force it (most stays local). Memory: `spin-off-candidates`. Revisit in seaworthiness.*

- **🌱 The state machine** (`_LIVE-STATE` + temporal decision-graph/`ADR-0007` + decision-audit
  method) — **Dave's first named candidate.** A portable "how a long-running agent project retains
  state, records supersession, and audits its own decisions" kit.
- Other candidates (unruled): decision-audit runbook + validation-state machine · the fixed/flex
  charter as a brand-true-generation governance pattern · the ingestion→overlay-KG method · the
  review-dossier language-review instrument · verification=enforcement / gate-tiering · the
  "cockroach doc" cold-start-proof pattern.
- Precedent (already ad hoc): `digital-experience-transformation`, `graphify-tool`. The ask is to
  make spin-off **intentional + surfaced**, not accidental.

- **✅ Capture ritual — STOOD UP 2026-07-05 → `knowledge/_RUNBOOK-capture-ritual.md`.** The five-step
  end-of-session sequence (refresh `_LIVE-STATE` → refresh `GOOD-MORNING` → update memory → record
  decision nodes with supersession discipline → commit+push) is now a runbook, not a hope. The
  enforcing `_capture_gate.py` is still deferred to the PM-KG MVP build (spec lives in the runbook);
  until then, the runbook itself **is** the gate — run it by hand every session.

## Entry points

`GOOD-MORNING.md` (latest handoff) → **this file** → `knowledge/README.md` (build) ·
`MEMORY.md` (memory index) · `AGENTS.md` (principles + method) ·
`knowledge/_RUNBOOK-capture-ritual.md` (end-of-session sequence, run every session).
