# BRIEF — Visual progress dashboard ("mission control")
**Ruled by Dave 2026-08-12 (#164, verbatim: "this is a priority after the side quest, it will really help me"). Build session: 2026-08-13 (tomorrow), AFTER Dave's sidequest lane. Nothing built yet.**

## Dave's two design rulings (his words, #164)
1. **Component library = Mono** — build from the existing gated Mono snippets/tokens ("using mono as the component library").
2. **Aesthetic = the `swiss-design-system` skill** — invoke that skill for layout/typographic discipline.

## What it is
A generated HTML page — same law as the showroom: **built from the stores, never hand-edited, regenerated as a build step, so it cannot rot.** It exists because Dave is a human, not an LLM: it is HIS orientation instrument.

Sources (all machine-readable, all already exist):
- `knowledge/_state.py` / `_state.json` — open work, owners, close conditions, the 19 unconditioned debt set
- `knowledge/_rulings.json` — rulings count + the provenance-gap set (15 open at authoring)
- `_CHAIN.md` / `_LIVE-STATE.md` — session position
- `_FUTURE-STATE.md` — the future-state lane
- live gate runs — a gates-health strip (run, never asserted)

Panels sketched (#164, not ruled in detail — Dave rules layout by eye):
- Dave's-plate vs my-plate backlog columns
- Gates-health strip (per-gate pass/warn/fail, measured at generation)
- Progress-toward-atomic counts (e.g. 114/114 binds, rulings gated, debt ratchets falling)
- Future-state lane

## Constraints (standing law, applies here)
- Dave: dyslexic (exec-summary first, big type, prose not walls of bullets) · astigmatic — **red/yellow are problem hues, blue/green stable; never encode meaning in hue alone, label everything**
- Generated-never-inherited; if wrong, fix the store and regenerate
- Verify by render (`knowledge/_RUNBOOK-render-verify.md`); present live HTML for Dave's eye
- Candidate use: the agenda screen for the 2026-08-14 (Friday) housekeeping session — every nipped thread visibly moves a number

## v2 lane (Dave, #165, 2026-08-13 — "we'll keep working on it in the future")
1. **Interactive dashboard** — dig deeper + manipulate: drill into a card/count to its source lines; filter/sort/regroup live. (Generated page stays the law; interactivity is client-side over the same generated data.)
2. **Schema question, Dave's to rule:** `_state.json` has no `status`/`lane`/`phase`/`priority`. Claude's recommendation #165: add **`priority` only** (not derivable, Dave's judgment); do NOT add `status` (derivable from `state`×`condition` — a stored copy of a derivable fact is the rot class). `lane` admissible only if a grouping the real fields can't express shows up. Any added field lands with a presence gate on new items.

## Conductor note for the build session
Re-verify premises at boot (this brief ages): the 15 provenance fails, the state counts, HEAD. Check whether `gen_showroom.py` idioms (theme slots, one-bar harness) are worth reusing vs a simpler standalone generator, e.g. `knowledge/gen_dashboard.py` + `dashboard/index.html`.
