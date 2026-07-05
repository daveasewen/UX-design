# _SEAWORTHINESS-PLAN — sequencing the half-finished threads, 2026-07-05

> **Provenance.** Written 2026-07-05, planning session "Seaworthiness planning — sequencing the
> half-finished threads." Not a build session. Inputs: `GOOD-MORNING.md`, `_LIVE-STATE.md`,
> `knowledge/_INGESTION-ASSESSMENT_2026-07-05.md`, verified live against the KG on disk (counts
> re-checked, not recalled). Deliverable = ONE dependency-aware sequence, not a flat backlog.
> Supersedes nothing; feeds `_LIVE-STATE` OPEN → "Seaworthiness plan".

---

## TL;DR — the sequence (read this)

The ship has **one structural leak** (ingestion never finished → gates §4, §4b, ADR-0003) and **one
failure MODE** (tracking rots silently → the stale Sutherland manifest). A suspected 39-vs-38
compliance-KG drift was checked this session and turned out to be a **false alarm** (EXAMPLE-button
template miscounted as a component) — see Phase 0 update below. Seaworthy = close the leak on a
phased plan **and** make the tracking un-rottable. Everything else is cargo — parallel or parked.

**Order (dependency-aware):**

1. **Hull patches — cheap, do first, protect everything.** Ingestion **Phase 0** (finish un-staling
   the manifest — mostly done) + install the **end-of-session capture ritual/gate** (§ below).
2. **Big rock #1 — Ingestion Phase 1 (Sutherland token migration).** Confirmed unblocked. Rebind +
   retire the 147 depricates, close P1/P3/P4. The convergent "finish, don't add" win.
3. **Prove-the-core track — runs in PARALLEL.** §9 first worked retrieve/extend/invent spread on one
   screen + divergence probe. Independent of ingestion; validates the whole engine thesis.
4. **Big rock #2 — PM-KG MVP (staleness gate).** `_build_live_state.py` + gate that flags targets
   whose blockers cleared but still read "blocked." Also unblocks Phase 4.
5. **Finish + unify.** Ingestion **Phase 2** (guidelines tail; toolkit tranche 2 on cheap model) →
   **Phase 3** (overlay/index KG = ADR-0003 "done right", **with the §4 language-strip done inside
   it**) → **Phase 4** (wire coverage into the state machine — needs #4).
6. **Parked / spun-off / waiting** — off the critical path (§ below).

---

## Next steps (numbered, act on these)

1. **Finish Phase 0 — ✅ CLOSED 2026-07-05.** Confirmed `_DESIGN-SYSTEM-GAPS.md` correction stands;
   confirmed `_INGESTION-ASSESSMENT_2026-07-05.md` is the single ingestion-state entry point.
   Rebuilt the compliance KG: **no drift** — 38 real components (`EXAMPLE-button.meta.json` is a
   template, correctly excluded) already matched 38 in the graph; `git diff` after rebuild was empty.
   Fixed a hardcoded `generated` date in `_build_compliance_kg.py` (was a literal, now stamps
   dynamically) so the graph can't silently go stale the same way the Sutherland manifest did.
2. **Stand up the capture ritual/gate** (spec below). One-time; protects every future session.
3. **Execute Ingestion Phase 1** — strict order: import modes → rebind every in-use depricate
   (`depricate-replacement-map.json`) → re-verify zero references → **then** delete. Tabs = proven
   first rebind. Own focused session.
4. **In parallel: §9 worked spread** — one screen, retrieve vs extend vs invent, then the divergence
   probe. Moves §9/§9a from "framing vouched" to "proven"; closes the vision's looks-language gap.
5. **Then PM-KG MVP** — build `_build_live_state.py` + staleness gate emitting FUTURE/TARGET states.
6. **Then Phase 2 → 3 → 4** in order. §4 language-strip lives inside Phase 3, not as a charter tweak.

---

## Why this order (the dependency logic)

- **Phase 0 + capture ritual are near-free and protect the rest** — they come first no matter what.
- **Phase 1 leads the big rocks** because it's the only big item that is *fully unblocked and pure
  finishing* (no new thread). It matches Dave's stated pain: too much half-finished, sequence don't
  add. Retiring 147 tokens + closing 3 gaps is the most visible debt paydown on the board.
- **§9 is the natural parallel track** — it has *no* dependency on ingestion (it runs on existing
  canon), and it's the load-bearing validation of the flexing-engine thesis. Runs alongside Phase 1.
- **PM-KG is big-rock #2, not #1** — building it first would be "more infra before finishing work,"
  the exact anti-pattern the audit flagged. But it comes soon: Phase 4 depends on it, and the live
  compliance-KG drift shows the failure it prevents is real, not hypothetical.
- **Phases 2→3→4 are strictly ordered** — can't build the overlay graph over entities not yet
  captured (Phase 2 before 3); can't wire coverage into a state machine that isn't built (PM-KG
  before Phase 4). **§4 language-strip is inside Phase 3** by Dave's ruling.

---

## KG verification (this session, against disk)

Assessment confirmed accurate. Guidelines **462 rules** (317 advisory / 54 blocking / 35 review /
56 taste — exact). Compliance KG **31 SC ↔ 31 rules ↔ 38 components**. Depricate set **147**.
Sutherland raw exports **present** (brand + semantic-color light/dark/Sutherland-light +
semantic-scale). One real finding, one false alarm: (a) Phase 0 already partly done — correction
banner in `_DESIGN-SYSTEM-GAPS.md`, now confirmed standing; (b) the suspected **"39 component metas
vs 38 in the compliance graph"** drift was **investigated and closed as a false alarm** — 39 files
exist in `components/`, one of them (`EXAMPLE-button.meta.json`) is the authoring template, already
excluded by the build script; real count is 38 = 38, confirmed by rebuild (`git diff` empty). Fixed
the build script's hardcoded `generated` date (was a literal, now dynamic) while here.

---

## The capture ritual / gate — the insurance policy (Dave's ask, decided here)

**Principle (from GOOD-MORNING):** don't archive all chats (rebuilds the haystack); the transcript is
a black-box last resort. Invest instead in a *reliable* end-of-session distillation — that's where the
risk is. Design = a fixed ritual + a light gate so capture can't be skipped or rot.

**The ritual (fixed end-of-session sequence — a runbook):**

1. Refresh `_LIVE-STATE.md` — LIVE / DEAD / OPEN / PLANNED-TARGET; bump "Last refreshed" to today.
2. Write/refresh `GOOD-MORNING.md` handoff (session-in-one-line + what landed + on-your-desk + queue).
3. Update/add memory files + the `MEMORY.md` pointer line.
4. Record new decision nodes with **supersession discipline** (tombstone artifact + log propagation
   gap in the same pass).
5. Commit in terminal with a paste-ready summary + description; clear stale `.git/*.lock`; **Dave
   pushes via GitHub Desktop only.**

**The gate (light, enforceable — a `_capture_gate.py`, spec only, build during PM-KG MVP):**

- FAIL if `_LIVE-STATE.md` "Last refreshed" ≠ today.
- FAIL if `GOOD-MORNING.md` date ≠ today.
- WARN on dangling `MEMORY.md` pointers (a `[[link]]` or index line with no matching file).
- WARN if uncommitted changes remain (nudge to commit before close).
- Green = the session is safely captured; the transcript never has to be the source of truth.

Cost: small. Payoff: the distillation that the whole cold-start spine depends on becomes a checklist,
not a hope. **Recommended: stand up the ritual now (free), build the gate script alongside the PM-KG
MVP** (same machinery — both parse front-matter + dates).

---

## Parked / spun-off / waiting — OFF the critical path

- **Harness modes + dials exploration** — research thread; start *after* the §9 spread gives it a real
  screen to bite on. "Find the use cases first." Inherits §9a (framing vouched, proven deferred).
- **TOV → digital-editorial spin-off** + §4b content audit — decouple from the interface engine;
  future thread. For interfaces, keep only the neutral guidance (labelling, language/locale, formality).
- **D2 novel-screen** — THE #1 unlock, but **waiting on a colleague's brief** — don't pick up until Dave says.
- **Toolkit tranche 2 (Dropdowns ×4)** — parallel **cheap-model** workstream; rides into Phase 2.
- **ADR-0004 ops follow-ups** — (a) re-verify EAA / EN 301 549 legal position; (b) align the
  installed `design:accessibility-review` skill from WCAG 2.1 AA to the project's 2.2-AA bar.

## Spin-off / generalisable candidates — surface + decide

Revisit here per Dave. **The state machine** (`_LIVE-STATE` + ADR-0007 temporal decision-graph +
decision-audit method) is Dave's **first named pick** — a portable "how a long-running agent project
retains state, records supersession, and audits its own decisions" kit. Others unruled: decision-audit
runbook + validation-state machine · fixed/flex charter as brand-true-generation governance · the
ingestion→overlay-KG method · review-dossier language-review instrument · the "cockroach doc" pattern.
**Decision to make (later, not now):** which of these earns its own thread vs stays local. Set the
goal first; don't force spin-offs (most stays local).

---

## Reflection

The audit's recurring finding was *foundations set ahead of completed work*. This plan is built to
break that pattern: the big-rock #1 is **finishing** (Phase 1), not new foundation; the two "infra"
items (PM-KG, §9) are sequenced as #2 and a parallel prove-track, not as pre-work. The one live drift
found this session (compliance KG 39-vs-38) is a small, encouraging proof that the failure mode is
real and cheap to catch — which is exactly what the capture gate institutionalises.

## Entry points

`_LIVE-STATE.md` (OPEN → Seaworthiness plan → **this doc**) · `knowledge/_INGESTION-ASSESSMENT_2026-07-05.md`
(the phased worklist this sequences) · `GOOD-MORNING.md` · `AGENTS.md` (method).
