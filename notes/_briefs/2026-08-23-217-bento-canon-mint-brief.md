# Sub brief — bento canon mint per `s217-D2` + nested demo (#217, Opus build sub)

**Ruling in force: `s217-D2`** — READ IT FROM `knowledge/_rulings.json` FIRST; it is the complete parameter spec (per-theme gutters, shared geometry, 820-band unification, nesting, container-not-tile radius, out-of-scope list). This brief does not restate numbers; the store is the truth.

## Scope
1. **SURVEY FIRST**: how canon structural components are authored — the token store + override-set architecture (ADR-0011 as amended by `s216-D1`: one store, per-theme override sets, mint step compiles concrete values; ADR-0014 DNA tier). Follow the Kpi-tile/border-radius-surface-slot precedent for how a themed geometry slot is wired. Grep before building; queue-vs-canon disagreement means the queue is the defect.
2. **Mint the bento grammar into canon**: a bento container + tile span grammar covering the four types' needs (presets, gallery incl. aspect-mapped photography spans, container-query full-scale, snap-designer output). Parameter surface = custom properties on the container with theme-minted defaults; **per-instance values may override** (that is how nesting gets different settings per level). Gutter is the ONLY per-theme divergence; radius consumes the theme token on the **container with overflow clipping — never tiles**.
3. **Nesting**: an inner bento as a tile of an outer must work with independent parameter sets. No JS.
4. **Demo page for Dave's eye**: the bento-of-bentos he described — three tight-gutter (1px) bentos inside a 40px-gutter outer, real photography + mixed cards, four themes × light/dark, console showing the container-radius treatment clearly.
5. **Re-point the Foundations pages** (`showroom/_foundations/*.html` via `gen_foundations_217.py`) from page-local bento styles to the canon grammar — the declared page-local styles should shrink to near zero.
6. **Regen serial is ORDERED** — canon edits regenerate wide; run the WHOLE serial per wave, ramp first, index LAST. Report `git diff --stat` blast radius; unexplained churn is a finding.
7. **Render-proof** per `knowledge/_RUNBOOK-render-verify.md` (read first; no `set_content`; chunk near 45s; fontconfig at the /var/tmp farm). Probes: per-theme gutter measured (0 vs 24), container radius measured in console (20px) and mono (0), nested demo gutters measured (1 and 40), dangling-var sweep all 8 states, band collapse at 1100/820/520.
8. **Rows**: store rows at creation, `_REVIEW-SIGNOFF.md` AWAITING, DS defects by addition. If token-store edits create derivation-governance questions, log to `_DS-IMPROVEMENTS.md` — promotion beyond `s217-D2`'s words is Dave's.

## DO-NOT-RULE (hard fence)
- Nothing beyond `s217-D2`'s words: no component radii (segmented-switch carve-out untouched), no surface/ink choices, no typography, no ds-044 canon fix, no logo/photo calls.
- `knowledge/_rulings.json` READ-ONLY. No gauge/lane/worklist edits. No commit/push, no git-checkout/reset.

## Pitfalls to carry (mandatory replay, Dave #165)
- (a) Aspect thresholds apply to the PHOTOGRAPHY bento only — card spans are authored; wiring thresholds onto cards would silently re-layout every card wall.
- (b) A theme override that never lands leaves the DNA default silently in force in that theme — measure the gutter in EVERY theme, don't infer from one.
- (c) Container radius without overflow clipping shows square tile corners poking through — probe the clip, not just the radius.
- (d) Rule only as wide as the gate's glob — new canon rules must sit inside the scopes existing gates actually parse (`gate-glob-scope-rule`); check what parses the artefact.
- (e) The #216 showcases stay as-built (AWAITING Dave) — do not retrofit them; the canon grammar is forward-facing.
- (f) Version don't overwrite (`-vN`); mv to `_to_delete/`, never rm.

## Report back (replayed in-window)
Canon diff + blast radius measured · paths · per-theme measured gutters/radii · nested-demo measurements · Foundations re-point delta · rows · residuals · what a failed probe would invalidate · token spend.
