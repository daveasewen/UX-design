# Next session (FRESH CHAT) — fix composition: make canon importable

**Why a fresh chat:** the chat that produced this is long; all state is in the memory files. Start clean,
read `MEMORY.md` + [[payments-journey-proof]] + [[pipeline-mental-model]] first, then this note.

## The problem (proven, not theoretical)
Canon snippets are **standalone reference HTML documents, not importable parts.** Assembling a real
screen means **hand-re-coding each component** (re-deriving its CSS + tokens), which drifts from canon —
demonstrated twice:
- `_fitness-test/payments-journey.html` (consumer 3-screen flow) — reintroduced a list-item title/sub
  stacking bug; button lost its calibrated scale-physics.
- `_fitness-test/sme-payments.html` (SME business screen) — re-derived cards/lists/buttons by hand again.
There is **no shared token + component layer** to compose from. This is the "materials → Sutherland /
harness barely built" gap ([[pipeline-mental-model]]) made concrete: components are proven in isolation,
but the unit of value (the screen) can't be assembled without re-coding.

## Goal
A way to **assemble a screen FROM canon without hand re-implementation**, so a composed screen cannot
silently drift from the gated components/tokens.

## Options to weigh (decide first, don't just build)
1. **Shared CSS layer** — extract canon tokens + per-component classes into one importable stylesheet
   (`canon.css`) + small HTML partials; snippets become consumers of it too (so the gate still covers them).
   Lowest-tech, works today, pre-Make/pre-Sutherland.
2. **Web components** — wrap each canon component as a custom element reading canon tokens.
3. **Sutherland React swap** — the eventual "materials swap" (snippets → Sutherland components). Real
   target, but gated on the Sutherland repo / Code Connect work ([[code-binding-hub-spoke]]).
4. **Build-step partials** — generate importable partials from the gated snippets so there's one source.

## Constraints / must-holds
- Must stay **gate-faithful**: composed screens have to be covered by (or re-use) the existing gates
  (token fidelity, state-contrast, icon-source HARD gate, a11y). Don't create a path that dodges them.
- Don't automate taste; composition is selection + layout (objective) — consistent with the rules.
- Connects to the **contextual-dashboard** vehicle ([[vision-contextual-dashboard]]) and the journey
  tranche still to refine (Headers/Navigations/Avatar/Dropdown) + missing patterns (stat grid, summary
  list, account card, sticky action bar, ink/neutral primary button) from the gap report.

## Also queued (from this session)
- Build the SME full journey from `_fitness-test/_PROMPT-sme-journey.md` (3 screens, canon styling, red rule removed).
- Revisit [[dark-rag-token-gaps]] (success/warning don't darken; dedicated dark rag-SURFACE token).
- Refine the journey-critical component tranche to 9/9.
