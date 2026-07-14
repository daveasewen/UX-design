# Session briefing — Strategy, 2026-06-20
*Dense end-of-session record. Start here next strategy session.*

## Bottom line
Worked the strategy kickoff. **Decisions are locked, instruments + a demo are built, and the spec is reissued at v0.2.** The proof project is chosen (payments retrofit) and is now the critical path — it's blocked only on a colleague chat + stakeholder responses. Everything else has an unblocked path.

## Decisions locked
1. **Spine = spec/eval-first.** Success/failure criteria written as executable checks before design; criteria become the gates. Governs the *objective* half only; the subjective half is a human taste call.
2. **Intake = adaptive maturity router**, 3 lanes → one criteria contract: seed→brainstorm · half-formed→guided JTBD · well-specced→ingest+quiz. Don't boil the ocean; build ONE lane (guided JTBD) for the prototype, rest designed-but-deferred. Users are non-expert, so lanes must guide.
3. **Checks tiered:** few objective gates (block) · many advisory signals (annotate) · rare human taste calls.
4. **Generation = multi-solution:** N variants on meaningful axes → all through objective gates → LLM *filters* (kills broken), humans + users *pick*. (LLM-as-judge research confirms: unreliable on aesthetics.)
5. **Adopt spec-kit "constitution"** = root non-negotiables ≈ gated canon.
6. **Editor last, wrapped not built** — generation/editing is commodity (v0, Stitch, Figma Make, Lovable); moat is upstream. NB: bank doesn't have Figma Make (agency only; slow procurement) — so an in-house gated-generation capability is genuinely new.

## Proof project — payments journey (retrofit)
Run the real, contested, under-discovered payments journey *backwards* through the loop → reconstruct criteria + riskiest assumptions + skipped gates → "what would've bitten us after go-live" gap report. Real, observable ground truth, no fabricated research. Dave to talk to a colleague close to it (state unknown — "slow, lots of opinions, no discovery").

## Artifacts produced (all in repo)
- `_STRATEGY-framework-comparison.md` — deliverable (b); recommendation + per-framework artifact/handoff notes.
- `payments-retrofit-prep.md` — quick prep sheet for the colleague chat.
- `payments-interview-guide.md` — semi-structured depth guide (doubles as guided-JTBD lane prototype).
- `payments-stakeholder-questionnaire.md` — ~10q breadth survey, opinion-spread (doubles as ingestion-lane prototype).
- `knowledge/_demo/_SCOPE-gated-generation-demo.md` + `knowledge/_demo/gated-generation-demo.html` — thin demo: generate a screen, gates as visible hero, gated vs "vibes" toggle. Build verified green (EXIT 0); fully isolated in `_demo/`, touches no canon.
- `apollo-pipeline-spec_v0.2_2026-06-20.html` — reissued spec with diagrams. **v0.1 archived** at `archive/apollo-pipeline-spec_v0.1_2026-05-31.html`.

## Repo / process notes
- Two chats share ONE working tree on `master` — **do not branch** (it would switch the build chat's files). Isolate by directory.
- Demo lives in `knowledge/_demo/`, consumes canon read-only, reuses real gates as source of truth. Exploration tier — never gated as canon.
- Multi-solution loop is **strategy-owned to define**, build-owned to execute. Don't start it in the build chat cold.

## Blocked vs movable
- **Blocked:** Sutherland JSON (late June/early July) · interview + questionnaire responses.
- **Movable now:** polish the demo for a boss showing · prototype the ingestion lane · run a one-screen retrofit on any live screen Dave can supply.

## Deferred (parked, not dropped)
- (a) Minimum-viable-target spec — blocked on picking the proof scope (now have the project).
- (c) Harness screen/journey/project definitions-of-done — inputs now specified by the intake lanes; no longer cold.

## v1 prune commitment (Dave's instinct, made explicit)
At v1, each of: `knowledge/_demo/*`, the two intake instruments, deferred harness work → explicit **keep / promote / delete**. Artifact volume ≠ proof; the demo + instruments are validated only after the colleague chat and a live showing.

## Honest flag
High artifact output in one session — watch the productivity-bubble risk. The next real progress is a *conversation* (colleague) and a *showing* (boss), not more documents.

## Next session — first moves
1. Did the colleague chat happen? If yes → run the payments retrofit into a gap report.
2. If not → do an unblocked movable: polish demo for the boss, or prototype the ingestion lane.
3. Pointers: `_STRATEGY-framework-comparison.md`, `apollo-pipeline-spec_v0.2_2026-06-20.html`.
