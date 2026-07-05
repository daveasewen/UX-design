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
- **Build**: `python3 knowledge/_build_all.py` — four gates green = internally consistent, dark-
  legible, surfaces not flat-white, snippets match canon.

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
- **Decision-corpus correctness audit — Tier A BATCH 1 RUN 2026-07-05 (ADR-0007 §5).** Method:
  `knowledge/_RUNBOOK-decision-audit.md`; ledger: `knowledge/_DECISION-AUDIT.md`. Batch 1 verdicts:
  **ADR-0005 vouch · ADR-0007 vouch · charter §9/§9a vouch(framing)+defer(proven/safe) ·
  ADR-0006 amend · `derivation-governance` amend.** Audit obligations now OPEN (see below).
  **Next: Tier A batch 2** (ADR-0001–0004, charter §4/§4b) in a fresh session; then Tier B/C.
  Never run in a loaded session.
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
- **D2 — novel-screen test — THE #1 unlock.** Waiting on a colleague's brief (their brief-v2 +
  own baseline + signed contract *before* generation). `_TEST-PLAN-novel-screen-proof.md`.
- **Toolkit tranche 2** (Dropdowns ×4) — parallel cheap-model workstream. Memory:
  `common-toolkit-survey`.

## Entry points

`GOOD-MORNING.md` (latest handoff) → **this file** → `knowledge/README.md` (build) ·
`MEMORY.md` (memory index) · `AGENTS.md` (principles + method).
