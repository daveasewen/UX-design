# 2026-07-21 (night) — Build-out strategy, ADR-0007 part 2, and the gauge fix

*Dossier (the why/how). Spine entry: `_LIVE-STATE.md` LATEST DELTA 2026-07-21 (night). Strategy:
`_BUILDOUT-STRATEGY-2026-07-21.md`. Session: OPUS solo / self-conductor, opened on "good morning".*

## Arc

Opened as a good-morning orientation off the inscription handoff. Dave brought three quick items
(ADR-0007 part 2, "what are the conflicts", the amber-gauge proposal) and then, mid-session, the real
subject arrived: a **strategy to finish the component library** while burning ~50% of the token budget
before Thursday-night renewal. The session became that strategy; the three openers were the warm-up.

## Finding 1 — the gauge "amber → 0.50" was recorded but never applied (drift)

`_LIVE-STATE` carried a HOUSEKEEPING line asserting the amber threshold had moved 0.45→0.50 on
2026-07-20. The engine (`_context_gauge.py`) still read `AMBER_AT = 0.45`. Classic
recorded-never-applied drift — the exact "confident false inscription" the project is built to catch.
Dave's live instruction ("move red to 60% too") turned out to be a partial memory: red was **already**
0.60 in the engine (the 70% he recalled was superseded earlier). So the real work was small and
honest: set amber to 0.50 for real, confirm red 0.60, fix the runbook prose (45–60 → 50–60), and
rewrite the false line to say what actually happened and when. **Lesson reinforced:** a threshold that
lives in prose *and* code must be checked in code — the prose lied for a day.

## Finding 2 — ADR-0007 part 2 was a small build sitting behind a now-cleared blocker

ADR-0007's part 2 (generate the `_LIVE-STATE` LIVE/DEAD blocks from the edge parse) had been deferred
since 2026-07-10 with a precise blocker: "needs the front-matter edge convention on ADRs first." That
convention (ADR-0012) landed and all 94 edges were inscribed the night before (`4a6f442`). So the
blocker was already gone — the build was just waiting for someone to notice.

Design choices that mattered:
- **Don't clobber the hand-authored spine.** `_LIVE-STATE` is an 80KB prose document. The generated
  block goes between `AUTO-DECISION-LIFECYCLE` markers (canon.css's AUTO-marker pattern), owning only
  decision-NODE lifecycle; the hand-authored artifact-tombstones and prose stay untouched.
- **Right tool boundary.** The graph generator already writes `_decision-graph.json`; the live-state
  builder *consumes* it. So `_build_all.py` was reordered (graph before live-state) and generation
  lives in `_build_live_state.py` — exactly where ADR-0007 §2 named it ("`_build_live_state.py` walking
  the edges").
- **Deterministic, or it rots differently.** No volatile date in the block, so a clean build produces
  no spurious diff — the same discipline that keeps canon.css quiet. Verified the block is an exact
  derived view of the graph state (55 LIVE / 6 AMENDED / 8 DEAD / 1 OPEN, zero drift).

## Finding 3 — the conflict gate is real but too young to block

All 8 registered tensions carry a resolution and the one divergence (DEF-006⇹DEF-005) is intentional,
so `--strict` passes clean. The temptation was to promote it to blocking "because rigour". Dave asked
the better question — "what's safest?" — and the honest answer was **keep it advisory**: the project's
own doctrine (ADR-0005 §5) is earns-blocking-by-bite-test, and both the gate and its parser are a day
old. Promoting now would enforce a bar the corpus already clears while risking a surprise red build
from a fresh-parser edge case. Recorded a concrete promotion criterion: promote once it's stayed silent
through work that *adds* decision edges (the RAG follow-ons) — that's the real false-positive proof.

## Finding 4 — the build-out strategy, and two corrections from Dave that sharpened it

Surveyed the ground truth first (survey-before-build): 40 gated canon components, 12 pro-forma
tranches, `reviews/` at 171 entries (the actual mess), and — the load-bearing discovery — the
**four-theme toggle isn't buildable as drawn**: `_themes.json` declares the themes but the Legacy
override file doesn't exist, `canon.css` bakes only Mono + light/dark, and `border-radius:0` is
**hardcoded** in components rather than bound to its token. So "toggle 4 themes" is real architecture
work, and Console's rounded corners are impossible until shape is de-hardcoded.

Two corrections from Dave reshaped the plan:
1. **"This architecture is already in an ADR — don't duplicate."** Right: ADR-0011 (themes as override
   sets) + **ADR-0010 (nullable flex slots, which explicitly names per-theme flex *beyond colour*)**
   already govern all of it. So today's theme rulings are **slot-population — token edits — not new
   architecture**. Shape/radius is one more flex slot under ADR-0010, not a new "corners" ADR. The
   strategy doc was rewritten to reference, not inscribe.
2. **"We talked about null values on some Mono tokens so we can add any time."** The ADR-0010
   declared-but-unset pattern applied to the *base*: declare `null` placeholder slots on Mono for the
   dimensions we anticipate flexing (the input error-condition colour), gate-guarded (§3: no null under
   a live binding), so a value can be added later without re-architecting.

Dave's rulings, settled: Console + Supercharge inherit Mono's palette; dataviz + status identical
across the three (only Legacy differs); per-theme flex on greys + radius + input-error, never
hardcoded; Console = rounded corners now; the clean folder is a **generated showroom — one file per
component + one master categorised-library `index.html`**, snippets/canon.css/tokens stay the gated
source, `reviews/` demoted to scratch.

The Fable model (the answer to "burn 50% without dropping quality"): **parallelism is the burn lever,
the 38 blocking gates + the review harness + an Opus verify pass are the fence.** Conductor + 2 Fable
workers. Serialise Phase 0 (the clean room — get the base right once); parallelise only Phases 1–2, so
we multiply output, not errors.

## Resolved state / still open

Landed: gauge aligned + drift fixed; ADR-0007 part 2 built + recorded (build green 38/38); conflict
gate ruled advisory + criterion recorded; strategy authored as the execution seed. **Open for the
fresh Phase-0 session:** whether the 12 pro-forma tranches fold into the finalised set or stay a
separate pattern category; Legacy's own corner radius; and executing Phase 0 itself (theme-resolution
layer + harness + showroom) with conductor + 2 Fable workers.
