# Component build-out strategy — 2026-07-21

*Authored this session (Opus, planning) as the execution seed for the fresh parallel build
sessions. Goal: finish the Apollo Mono component library and stand up the four-theme review harness,
then build the remaining ~50 gaps at pace — burning ~50% of the token budget before Thursday-night
renewal **without dropping quality**. Read this, then `_LIVE-STATE.md`. Supersedes the looser
"component-library-buildout-plan" memory for the next few sessions.*

---

## The bet in one line

Housekeeping first (a clean room + a real four-theme harness), **then** fan out. We do not build at
pace until the harness and gates can catch regressions — parallelising before the base is correct
multiplies errors, not output.

## Ground truth (surveyed 2026-07-21)

- **40 gated canon components** — `knowledge/snippets/*.reference.html` + generated `canon.css`
  (`.cn-*`). This is the real finalised core; it's already fairly consolidated.
- **12 interactive pro-forma tranches** — `knowledge/_proforma/*.html` (a separate pattern set).
- **`reviews/` = 171 entries — this is the mess**, not the canon.
- **Itinerary** = 124 rows (`reviews/ITINERARY-2026-07-14-apollo-component-library.*`), ~50+ gaps.
- **Theme layer is declared, not built.** `tokens/themes/_themes.json` names all four themes, but the
  Legacy override-set file it points to **does not exist**, and `canon.css` bakes only Mono + a
  `[data-theme]` light/dark mode. There is **no `[data-apollo-theme]` cascade** yet.
- **Shape is half-wired.** `border-radius` IS a token (`layout.json`, Mono default `0` = square), but
  components **hardcode `border-radius:0`** in `canon.css` (button, list-items, …). A theme override
  can't round corners until those hardcodes are rebound to the token.
- `_make_review` has **no theme/mode switcher** — the universal harness is new work.

## Dave's theme rulings (2026-07-21) — these APPLY the existing architecture; do NOT write a new ADR

> **The architecture is already ratified — reference it, don't duplicate it.** ADR-0011 (themes =
> override sets at the semantic tier; Mono base, Legacy populated, Console/Supercharge = declared
> nullable slots) and **ADR-0010 (nullable flex slots)** already cover all of this. ADR-0010
> explicitly names **per-theme (override set)** as a flex dimension and explicitly anticipates flex
> **beyond colour** ("the set of dimensions is defined by what the style-builder will flex"). So the
> rulings below are **slot-population — token-store edits under ADR-0010/0011 — not new decisions to
> inscribe.** Shape/radius is simply an added per-theme flex slot, exactly as ADR-0010 describes.

1. **Console + Supercharge inherit Mono's palette** (base), not Legacy. Ship as Mono-inheriting
   override sets, currently equal to Mono except where a divergence is ruled.
2. **DataViz + status/RAG colours are identical across Mono / Console / Supercharge.** Only Legacy
   differs there (teals, Legacy reds).
3. **Divergence axes — theme-overridable, NEVER hardcoded:** UI greys (neutral ramp), **shape /
   border-radius** (Console = rounded corners, a real divergence *now*), and a possible future
   **input error-condition colour** (drawn from Mono values but overridable per theme).
4. **"Assume nothing changes for now, but might in future."** The override sets exist with the
   divergence hooks live but currently equal to Mono — so a future palette/greys/radius change is a
   token edit, never a re-architecture.
5. **Toggle shows all four slots; Console/Supercharge render as Mono** (labelled), plus Console's
   rounded corners once shape is de-hardcoded.

6. **Declare `null` placeholder slots on Mono now for the dimensions we anticipate flexing** — the
   input error-condition colour especially — so a value can be added at any time (per-theme, or in
   Mono itself) without re-architecting. This is ADR-0010's declared-but-unset pattern applied to the
   base, gate-guarded (§3: no `null` under a live binding) so nothing renders an unset slot.

**Architectural consequence:** a theme override set spans **colour + neutral-ramp + shape(radius) +
anticipated-null slots** (e.g. input error), all token-bound. **All of this is already governed by
ADR-0011 + ADR-0010 — nothing new to inscribe.** The Phase-0 work is *declaring the slots* (radius
per-theme; Mono null placeholders) and *populating the override files* — token-store edits, not
architecture. No "corners" ADR; radius is one more flex slot under ADR-0010.

---

## Phase 0 — the clean room (SERIAL; Fable + Opus; get it right once)

Do **not** parallelise this. Everything downstream inherits it.

1. **Theme-resolution layer.**
   - Author `tokens/themes/apollo-legacy.overrides.json` (teals, HSBC grey ramp, Legacy reds) and
     stub `apollo-console.overrides.json` / `apollo-supercharge.overrides.json` as **Mono-inheriting**
     (only Console's radius set differently; everything else null → falls back to Mono base).
   - Generate a `[data-apollo-theme="legacy|mono|console|supercharge"]` CSS cascade that sits **above**
     the `[data-theme=light|dark]` mode layer, re-binding the semantic aliases to the active theme's
     override set. `resolve(role, mode, theme)`: theme override wins, else Mono base. Components stay
     theme-blind.
   - **De-hardcode shape:** rebind hardcoded `border-radius:0` in `canon.css` to
     `var(--border-radius-default)` (leave genuine `50%` circles alone). Gate it so new hardcodes fail.
2. **Universal review harness.** One shell that loads any component with: **theme switch (4) × mode
   switch (light/dark) × responsive slider × full variant/state spread**, on both grounds. This is the
   whole-system-in-action review Dave wants. Extend `_review/_make_review.py`; the harness is itself a
   product feature (review-layer = product).
3. **The single clean folder — the "showroom" (RULED, Dave 2026-07-21).** A **generated, browsable
   library** assembled from the canon (snippets + canon.css + tokens stay the gated source). Shape:
   **one separate file per component** (self-contained, fully token-wired, theme+mode-switchable) **+
   one master `index.html` that displays them as a categorised library** (grouped by kind —
   inputs, navigation, feedback, data, etc.), each with the theme×mode toggle. `reviews/` demoted to
   scratch/archive. One folder, unpolluted, human-navigable. Generated from source so it can't rot.

**Exit gate for Phase 0:** one real component (e.g. Button) renders correctly across all 4 themes ×
light/dark in the harness, with Console visibly rounded, zero hardcoded radius, build green.

## Phase 1 — finalise the existing 40 (PARALLEL; Fable workers + gate/Opus verify)

Run every existing Mono component through the new harness. Per component: confirm full token-wiring
(colour + shape), gate-pass, clean render across theme×mode, fix gaps, sign off into the showroom.
Batch across the 2 workers; conductor reconciles + commits per `_RUNBOOK-parallel-conductor.md`.

**Exit gate for Phase 1:** all 40 signed off in the showroom, build green, theme-provenance +
legacy-leak gates clean, no hardcoded radius anywhere.

## Phase 2 — build at pace (PARALLEL; the ~50 gaps toward the 124 itinerary)

Only after Phases 0–1. Generate remaining components in parallel Fable batches; each lands
token-wired + gated + harness-ready. Conductor reconciles + commits. Prioritise the itinerary's base
gaps (templates/shells are the load-bearing gap — see `library-composition-tier-gap`).

---

## The Fable leverage model — burn ~50% in two days, quality intact

- **Parallelism is the burn lever, gates are the fence.** Conductor + **2 Fable workers** (Dave's
  ruling). Workers generate; the conductor is the single writer for the shared tree (commit +
  `GOOD-MORNING`/`_LIVE-STATE`); workers emit receipts to `notes/_receipts/`. Never blind
  `git add -A` with workers live.
- **Fable on judgment-dense work** (composition, variants, review authoring) where its quality earns
  the spend. **Sonnet** for mechanical throughput (sweeps, rebinds). **Opus + the 38 blocking gates +
  the review harness** are the quality backstop — nothing counts as done until it passes the build and
  renders clean in the harness.
- **"Within reason":** serialise Phase 0; parallelise only Phases 1–2. Two workers, not four — keeps
  one clean tree with manageable reconcile overhead.
- **Leverage the tokens (both senses):** the design-token architecture makes generation cheap to
  verify (components bind roles, not hexes), which is *why* we can safely spend LLM budget on parallel
  generation.

## Quality guarantees (the "without sacrificing quality" contract)

Every component, before it counts: passes `python3 knowledge/_build_all.py` (38 gates, non-zero on
any fail) · renders clean across 4 themes × light/dark in the harness · token-wired on colour AND
shape (no hardcodes) · an Opus verification pass vouches a batch before commit.

## Open confirmations for the execution session

- Showroom-vs-reorg for the clean folder (showroom assumed).
- Whether the 12 pro-forma tranches fold into the finalised set or stay as a pattern library.
- Legacy's own corner radius (Mono square, Console rounded — Legacy = ? likely rounded/HSBC).
