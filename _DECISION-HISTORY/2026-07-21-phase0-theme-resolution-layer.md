# 2026-07-21 — Build-out Phase 0: the theme-resolution layer, the radius flex slot, and the showroom

*Session: "Apollo build-out Phase 0" (FABLE, conductor; Dave's parallel worker ran designer-skills-v2
separately). Executed `_BUILDOUT-STRATEGY-2026-07-21.md` Phase 0 in one pass: theme override sets →
`[data-apollo-theme]` cascade → radius de-hardcode + gate → universal harness → showroom → exit gate.
Build 38/38 → **42/42** (four steps added). Spine entry: `_LIVE-STATE.md` 2026-07-21 late delta.
Ledger/ADR: no new ADR — everything here is slot-population + generation under ADR-0011 + ADR-0010,
exactly as the strategy doc instructed.*

## Finding 1 — the projected-literal problem decides the cascade's shape

The obvious theme layer (override the canonical `--token-path` vars at root) is INSUFFICIENT here:
canon.css component blocks carry per-mode **literals** (projected by `gen_snippet_tokens
project_canon` for anti-drift), so no root-level var re-bind can reach `.cn-button{--pri-default:#1A1A1A}`.
The cascade therefore emits TWO tiers, both generated: root canonical vars (for alias/spine consumers)
+ **per-component re-projections driven by each snippet's own `#token-manifest`** — for every manifest
var whose token path a theme overrides:
`[data-apollo-theme="legacy"] .cn-button{--pri-default:#DB0011}` (+ the `[theme][data-theme="dark"]`
combo). Specificity proof in the generator docstring: theme-light (0,2,0)+later beats base; theme-dark
(0,3,0) beats mode-dark (0,2,0); **both modes always emitted** so a theme-light value can never leak
into dark. The manifests were built for anti-drift; they turned out to be exactly the join the theme
layer needed — the components stay theme-blind, the cascade knows every binding.

## Finding 2 — order-dependence bug, caught the same hour it was born

`project_canon`'s regex carries an OPTIONAL `[data-theme]` prefix, so it also matches the bare
`.cn-<slug>{` inside my new AUTO-THEMES selectors — a `gen_snippet_tokens` re-run **stomped Legacy red
back to Mono ink** inside the theme block. The cascade's `--check` caught it on the first
order-flipped run (the gate earned its keep the day it was wired). Fix = a **fence in the projector**
(everything from the AUTO-THEMES marker is the cascade generator's output; never touch), not a "run
them in the right order" convention — order-dependence documented is still order-dependence.

## Finding 3 — the projection had no gate, and the corpus proved why it needed one

First `gen_snippet_tokens` run this session projected **100 snippet/tranche values + 4 canon
literals** that had silently drifted: Tranches T1–T9 still carried the pre-R-D20 Legacy error reds
(`#A8000B/#DB0011` + old tints), canon's `.cn-button` still pre-B-D secondary/success values. Root
cause: the projector runs manually and NOTHING in the build verified sync — the snippet gate covers
snippets only, and tranches/canon literals had no check at all. All corrected values are
already-ruled ones (R-D20, B-D, R-D18) — this is enforcement catching up, not new decisions.
**Closed permanently:** `gen_snippet_tokens --check` is now build step "token projection sync"
(blocking). Committed separately for attribution (catch-up ≠ Phase-0 authoring).

## Finding 4 — Legacy is reconstructible from the eviction records alone

Every Legacy override value came from the corpus, none invented: the R-D18/R-D20 token `$note`s name
the evicted teal/tint/amber/navy pairs verbatim ("was #E5F2F2 / #001615"…), R-D16's note literally
instructs "Legacy retains the dimmer #545454/#9B9B9B as its own theme override", the registry
`ownsHexes` carries the reds, and the Legacy-era `primary/*` roles still hold the CTA red family.
20 paths authored with per-line provenance; the **exit gate caught the 21st** — Button binds
`rag/success-background` (an R-D14 Mono invention), which stayed green under Legacy until the teal
was added as its Legacy surface. **Open for Dave:** `text/on-success` kept BLACK under Legacy
(6.06:1 AA-pass); historically Legacy was white-on-teal (3.47:1, AA-fail) — flipping it would
inscribe a recorded a11y regression into the Legacy set, so it stays a ruling, not a default.

## Finding 5 — radius mechanics: spine var direct, no local shadow

De-hardcode = `border-radius:var(--border-radius-default)` in canon bodies (37 declarations; 50%
circles + 999px pills stay literal — the pill idiom is *deliberately* round in every theme, distinct
from the flex slot). Canon components deliberately do NOT declare a local radius var (a `.cn-x`-scoped
declaration would shadow the root theme override); standalone snippets DO declare it in their theme
blocks via manifest (`border-radius/default`), which required extending both `resolve()` functions
(projector + snippet gate) to route layout-namespace paths to `layout.json`. Button is the migrated
proof; the other 21 files are enumerated in `_RADIUS-GATE.md` as the Phase-1 ratchet (strict-on-
migrated, advisory census on the rest — the gate-glob-scope rule applied).

## Finding 6 — the harness needed `hashchange`, and the render loop found it

First exit-gate render: all four theme URLs produced Mono frames. Same-document fragment navigation
(`#theme=legacy` after load) fires no re-init without a `hashchange` listener — exactly the
index→page navigation path a user takes. Fixed in the template; the in-sandbox Playwright loop
(recipe: memory `sandbox-html-rendering`, headless shell + real HSBC TTFs) then verified attribute
propagation into both srcdoc iframes per theme, and the four renders were eyeballed: Legacy red
CTA + teal Done, Mono ink, Console rounded (8px, palette unchanged). **Supercharge = Mono proven by
pixel-diff (bbox None), not by eye.**

## Rulings recorded this session (in-chat, Dave)

- **Legacy corner radius = square, same as Mono** (`apollo-legacy.overrides.json` border-radius/default
  0, noted). The strategy doc's open confirmation is resolved.
- **Console = rounded NOW; the 8px value is my PROVISIONAL proposal**, flagged in the override `$note`
  for ruling on the harness — one token edit to change.
- Phase 0 run serially, me solo-conducting (per strategy; Dave confirmed at session open).

## Resolved state

Theme layer LIVE (4 themes, one attribute, components theme-blind) · shape = live flex slot ·
harness + showroom generated for all 40 (each page: 4 themes × light/dark panes × width slider ×
live variant spread; categorised index carries theme into pages) · four new build steps (projection
sync · cascade sync · radius gate · showroom sync), all blocking, all selftested/bite-tested ·
build **42/42**. Still open → §C of `GOOD-MORNING.md` (Console px ruling · Legacy on-success ·
21-file radius migration · tranches fold-or-stay · Mono null-slot store entry once the ADR-0010 §3
gate exists).

---

## ADDENDUM — same evening (after Dave's push + review): the radius becomes a TIER

*Appended explicitly per the archive rules (dated, not a silent edit). Dave, on the pushed result:
"the 8px can't be universal, the radii will be different on cards and buttons for instance, remember
flexibility is key, also remember that ultimately we will build a theme generator from this, maximum
flexibility."*

**Finding 7 — one flex slot per dimension is the wrong grain; the grain is the ROLE.** Enacted
immediately so Phase 1 migrates 21 files once, not twice: `layout.json` border-radius grew semantic
roles — `default` (the theme's base) + `control` / `surface` / `indicator`, each `$alias`-falling-back
to default (taxonomy = agent-PROVISIONAL, three roles by current canon evidence, extend by evidence
not speculation). `gen_canon_tokens` now emits modeless alias CHAINS
(`--border-radius-control: var(--border-radius-default)`), and `gen_theme_cascade` gained **generic
alias-aware resolution** — the true `resolve(role, mode, theme)` ADR-0011 promised: a theme
overriding the base cascades into every role that follows it; a role override wins. (Generic across
stores, so colour alias chains propagate too — Legacy's ink now correctly reaches roles that alias
`text/default`, e.g. icons.) Canon rebound by role (final census: 21 control / 8 surface /
8 indicator; three hand-corrections over the classifier — `.close`, `.overflow__trigger`,
`.overflow__item` are buttons, not surfaces; `.cn-tabs .indicator` left as control, worker may
refine). **Cards migrated as the second proof**; Console demo = default 8 + surface 12 (both
provisional) — **render-verified: Console cards 12px against buttons 8px, Dave's own example, live.**
The theme-generator horizon is inscribed in `_FUTURE-STATE.md` (style-builder entry, widened): themes
are data, the builder edits override sets, role-granular slots are its dials.
