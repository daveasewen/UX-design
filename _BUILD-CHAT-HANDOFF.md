# Promenaut — Build chat hand-off
*Seed doc for a fresh chat to continue the hands-on KB / gated-component work **in parallel** with the
strategy chat (`_STRATEGY-KICKOFF.md`). Paste this in and say "continue the build chat."*
*Written 2026-06-20. Current state is green and stable — safe to pick up cold.*

---

## Read me first — scope boundary (the two chats must not collide)
There are two chats running in parallel on the **same repo** (`knowledge/`):
- **Strategy chat** (`_STRATEGY-KICKOFF.md`) — owns product vision, the **harness/pipeline redesign**, the
  **check-tier architecture** (blocking vs advisory), and anything that re-shapes how the pipeline fits together.
- **THIS chat (build/tactical)** — owns convergent, gate-verifiable canon work *inside the current architecture*.

**Rule for this chat:** do **not** restructure the pipeline, re-tier the gates, or design new check
*architecture* — that's the strategy chat's call. You may *prototype an advisory-only (non-blocking) check*
if useful, but don't make it a hard gate or build a tier system. When in doubt, it's convergent canon work here;
anything that changes the *shape* of the system belongs to strategy. Commit small; flag anything cross-cutting.

## Current state (verified green 2026-06-20)
- **32/32 real components gated** — `knowledge/snippets/*.reference.html`, each token-faithful (light+dark), build-verified. (`EXAMPLE-button` is a template, not a component.)
- **Build:** `cd knowledge && python3 _build_all.py` → 12 steps, **6 gates**, EXIT 0. The gates (all bite-tested):
  1. text/icon contrast · 2. indicator/accent contrast · 3. dark-surface flatness (`_validate_dark_surfaces.py`) ·
  4. snippet token-fidelity (`_validate_snippets.py`) · 5. a11y (`_validate_a11y.py` — reduced-motion required when animating = hard fail; sub-24px targets reported) ·
  6. coverage (`_validate_coverage.py` — every meta has a name-matched snippet) · + integrity lint + schema (32/32).
- **Gate philosophy:** gates exit non-zero to *withhold "done"* (verification = enforcement). Keep new definition-of-done **executable**, not prose.

## Repo map (so you can navigate cold)
- `knowledge/snippets/*.reference.html` — the gated canon. Each carries an embedded `#token-manifest` JSON (`vars` = CSS var→token path, `contrastPairs` = passing pairs only, `requiredAria`).
- `knowledge/components/*.meta.json` — per-component metadata (props, tokens, accessibility, `tokenValidation`, `$finding`).
- `knowledge/tokens/*.json` — token store (`semantic-colour.json`, `colour.json`, `motion.json`, `layout.json`).
- `knowledge/guidelines/*.md` — the authored standards (brand-principles, focus-indicators, digital-accessibility-standards, etc.).
- `knowledge/_build_all.py` — the build/gate runner. `knowledge/_validate_*.py` — the gates.
- `knowledge/_fitness-test/*` — **exploration tier (NEVER gated)**: motion showcases, A/B explorations.
- Reports/indices: `_FINDINGS-INDEX.md` (the map of everything), `_A11Y-AUDIT.md`, `_DESIGN-SYSTEM-AUDIT.md`, `_VISUAL-CHECK-QUEUE.md`.
- Runbooks (the method, written down): `_RUNBOOK-gated-component.md`, `_RUNBOOK-reconcile-dark-tokens.md`.

## Invariants (do not violate)
- Colours are **resolved semantic tokens**, never invented hexes (exception: a flagged `review`-tagged proposal, kept local + annotated, e.g. `text/secondary`, `focus/ring`).
- The build must end **green** before you call anything done.
- **Two-tier canon:** gate canon (`snippets/*.reference.html`); **never gate exploration** (`_fitness-test/`).
- Angular brand rule: square corners (`border-radius:0`); only Badge + Avatar are round exemptions.
- A new snippet needs a `prefers-reduced-motion` block if it animates, and a meta whose `name` matches its manifest `component`.

## Done today (so you don't redo it)
`text/secondary` token added + adopted (List items, Cards); focus ring token-tracked in 5 snippets; full WCAG
static pass (reduced-motion ×28, 24px hit targets on Tags/Tooltip) + the a11y gate; 1.4.1 use-of-colour audit
(all pass) + rule in guidelines; **Table built** (closed coverage to 32/32); keyboard audit (all pass); coverage
gate; design-system consistency audit. Details in `_FINDINGS-INDEX.md §5/§6`.

## Open work — by lane

### A) Safe autonomous / convergent (crack on without Dave)
- **Sutherland fixture index — ✅ DONE 2026-06-20.** `_build_sutherland_fixtures.py` (build step 4) emits
  `tokens/_manifests/sutherland-fixtures.json` + `_SUTHERLAND-FIXTURES.md` — the per-component acceptance
  contract (token bindings + ARIA + contrast pairs + props). Regenerated each build. Extend it when Sutherland JSON arrives.
- **(Optional) advisory-only states-completeness probe** — a *non-blocking* report on which snippets demonstrate
  empty/loading/error/overflow states. Keep it advisory; do NOT gate it (tiering is strategy-owned).
- **NOTE:** the `tooltip/*` "reconcile" is NOT a safe silent task — it hides a deprecate-vs-adopt decision
  (adopting changes appearance). Re-filed to lane C / `_FINDINGS-INDEX.md §6`. Don't touch `tooltip/*` without Dave.

### B) Needs Dave's eyes — `_VISUAL-CHECK-QUEUE.md` (don't guess these)
- V1 `text/secondary` values · V2 the 4 baseline organisms (Navigations, Headers, Hero, Video) · V3 screen-reader/keyboard AT pass · V4 zoom/reflow · V5 Table sort + small-screen reflow strategy.

### C) Needs a decision — `_FINDINGS-INDEX.md §6`
- `focus/ring` sign-off · inverting-label canon · `rag/warning` standalone-dot rule (already documented) · the token-hygiene confirms above.

### D) Parked / strategy-owned (leave for the strategy chat)
- Motion promotion (`_PROMOTION-QUEUE.md`) — partly visual, partly strategy; coordinate before promoting.
- Figma dark write-back (needs Dave's go-ahead) · the upstream discovery/PRD phase · Code Connect · the harness redesign.

## Suggested first task for this chat
The clean autonomous wins (Sutherland fixtures) are **done**. Remaining build work mostly needs Dave's eyes
(lane B) or a decision (lane C), so the honest first move is to **ask Dave which lane-B/C item to unblock**, or
do the optional advisory **states-completeness probe** (lane A) if you want a self-contained convergent task.
Keep the build green; present a diff for review when done.

## Working conventions (Dave)
- Concise, direct; minimal formatting. When committing, hand over a paste-ready git summary + description.
- Use the visual-check queue for anything needing his eyes — never silently make a taste call.
- Pointers: `knowledge/_NEXT-SESSION.md` is the broader start-here; this doc is the build-chat-specific cut.
