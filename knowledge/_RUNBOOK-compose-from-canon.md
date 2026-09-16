# Runbook — compose a screen from canon (the composition layer)

**Problem this solves** (proven in the payments-journey + SME walks): canon snippets were
standalone reference HTML. Assembling a screen meant hand-re-coding each component, which
drifted — the list-item title/sub stacking bug came back, and the button lost its calibrated
scale-physics (`scale(1.02/.97)` instead of canon's `1.04/.95`). There was no shared token +
component layer to compose from.

**The fix:** one importable stylesheet — `knowledge/canon/canon.css` — that every screen
*and* every snippet consumes. Composition becomes objective **selection + layout**; a composed
screen cannot silently drift because it has no component CSS of its own.

---

## What's in `canon/canon.css` (4 layers, top → bottom)

1. **AUTO-GENERATED TOKENS** — `:root` + `[data-theme="dark"]`, 343 vars + 116 dark overrides.
   Generated from `knowledge/tokens/*.json` by `gen_canon_tokens.py`; names trace 1:1 to token
   paths (`primary/background/hover` → `--primary-background-hover`). **Never hand-edit between
   the AUTO markers** — re-run the generator. This is the anti-drift spine.
2. **SEMANTIC ALIASES** — short ergonomic roles → semantic tokens (`--surface` →
   `var(--tertiary-background-default)`, `--focus` → `var(--focus-ring)`, …). This is the layer
   each snippet used to re-invent by hand; it lives **once** here now. Add an alias rather than
   re-deriving a colour in a component.
3. **BASE + LAYOUT UTILITIES** — `.canon` root, `.c-stack-*`, `.c-row`, `.c-grid`, `.c-screen`
   phone frame, plus the gap-report missing patterns: `.c-actionbar` (sticky), `.c-summary`
   (key/value), `.c-stat-grid`, `.c-account-card`, bottom `.c-tabbar`, `.c-choice-row`.
4. **AUTO-GENERATED COMPONENTS** — all 32, **generated from the reviewed snippets** by
   `canon/gen_canon_components.py`. Each component is carried **verbatim** (every rule, state,
   reduced-motion block AND every decision comment — handled a11y findings, contrast reasoning,
   non-colour press signals, `driftAllow` reasons), with its theme colours rewritten to token
   refs and its CSS scoped under `.cn-<component>` (e.g. `.cn-button`, `.cn-list-items`). A header
   comment per component carries its Aria contract, atom reuses, and known findings. The snippets
   are the source of truth (they are the final reviewed components); **never hand-edit between the
   AUTO-COMPONENTS markers** — edit the snippet and regenerate, so review decisions can't be lost.

## Compose a screen

1. Root element gets `class="canon"`, and **two** attributes on it (or `<body>`): the theme,
   `data-apollo-theme="common|console|supercharge"`, and the mode, `data-theme="light|dark"`.
   They are different dials — canon selects on both. `data-theme` cannot carry a theme, so a
   root with `data-theme` alone is a **mono** build (mono is the attribute-less baseline; every
   radius token is `0` there). `legacy` is the older key for `common` and still resolves
   (`s227-D8`), but new work emits `common`.
2. `<link rel="stylesheet" href="../canon/canon.css">`.
3. Drop in each component as **its scope class + the snippet's own markup**, e.g.
   `<div class="cn-button"><button class="btn primary full">…</button></div>` or
   `<div class="cn-list-items"><ul class="list"><li><button class="row">…</button></li></ul></div>`.
   Use the `.c-*` utilities + gap patterns for layout (`.c-stack-*`, `.c-actionbar`, `.c-summary`,
   `.c-account-card`, `.c-tabbar`, `.c-choice-row`). **The screen's own `<style>` is harness only —
   no `#hex`, no `.c-*`/`.cn-*` redefinitions.**
   ⛔ **Never copy a fenced `APOLLO-DEMO` span** (`s258-D3`). Snippets carry showroom harness —
   width dials, state switchers, demo labels, `demo-*` wrappers and the script driving them —
   fenced in the same marker family as the injection markers, so all three grammars read alike:

   | marker | who writes it | what it means |
   |---|---|---|
   | `<!-- ===== AUTO-TOKENS / AUTO-PARTIAL <name> / AUTO-BEHAVIOUR <name> / AUTO-MARKUP <name> / AUTO-BENTO START … ===== -->` (CSS/JS comment form inside `<style>`/`<script>`) | the generators (`gen_component_partials.py`, `gen_token_ramp.py`, `gen_canon_bento.py`) | **injected**: regenerated in place, never hand-edited |
   | `<!-- ===== APOLLO-SPLICE <region> START (source=<path> kind=<markup\|style>) ===== -->` | `gen_provenance_receipt.py` | **spliced**: the region's bytes are hashed into the page's provenance receipt |
   | `<!-- ===== APOLLO-DEMO <what> START (showroom harness — never copy) ===== -->` (and `/* ===== APOLLO-DEMO <what> START … ===== */` in CSS/JS) | the snippet author | **showroom-only**: delete every fenced span and the component still renders |

   `APOLLO-DEMO` spans stay in the snippet and never reach a composed screen: a page carrying
   the marker is red as `FAIL:DEMO-CHROME-COPIED` (`_validate_receipt.py`, step 3b).
   Demo-only *vars the component itself reads* are NOT fenced — the component rule keeps a real
   default (`.dg{max-width:var(--dg-max,760px)}`) and the harness sets that var from inside the
   fence, so the dial is harness and the default is the component's.
4. Worked example: `_fitness-test/payments-journey.canon.html` — same journey as the drifted
   `payments-journey.html`, but its hand-written CSS dropped from **117 lines → ~20** (harness
   only), 0 rogue hex, every component the gated original.

## Two inscribed lessons (from the 2026-07-05 restyle saga — history:
`_DECISION-HISTORY/2026-07-05-register-spread-and-restyle.md`; inscribed 2026-07-18 by ruling)

- **Theme-dependent alias blocks use the SAME selector list as the tokens they wrap — never a bare
  `:root`.** A bare `:root{ --ink: var(--page); }` computes once against `<html>`'s light values and
  inherits the frozen result under `[data-theme="dark"]`. Match canon's own pattern:
  `:root, [data-theme="dark"]{ … }`. This bug rendered a hero figure invisible and canon.css
  documents the trap at its own alias layer — check there before writing aliases.
- **A hand-built "canon-primitive" screen is a CLAIM the gate exists to check — run the gate as the
  LAST step before presenting, never when asked.** The restyle passed "on inference" until Dave asked
  directly; the real run then failed on hex refs + 3 unknown icon paths, and a follow-up contrast
  pass found four genuine 1.4.3 failures the shallow check missed. Gate + a real contrast check on
  any composition that is not a `.cn-*` snippet.

## Gate it — run the composed screen through the WHOLE pipeline, not a hand audit

```
python3 knowledge/_validate_screen.py --render        # all *.canon.html through every applicable gate
```
`_validate_screen.py` runs, on each composed screen, the SAME gates the snippets pass — so a
deviation fails the build instead of waiting for a human to spot it:
- **compose** (`_validate_compose`): 0 rogue hex, no `.c-*`/`.cn-*` redefinition, every class resolves,
  no native/`accent-color` control reinvention.
- **icon-source** (`_validate_icons`): every inline `<svg>` path must byte-match the `assets/icons`
  library (or be `data-bespoke`); shape-only icons flagged. (This is what caught the hand-drawn tab-bar
  icons after the radio + notification icon fixes.)
- **a11y** (`_validate_a11y`): reduced-motion present if it animates; target-size.
- **state-contrast** (`_validate_state_contrast`, `--render`): renders every screen × light/dark, drives
  real hover/pressed on each interactive element, checks computed contrast (the gate that closed the
  Cards 9/9 blind spot).
Writes `_SCREEN-GATE.md`. The token-level gates (`_validate_dark_surfaces`, `_validate_coverage`) run on
the token/meta layer upstream — canon inherits them, so they don't need re-running per screen.
`_validate_compose.py` alone still works for a quick structural-only check.

## Regenerate canon (the two generators — canon.css is generated, not hand-kept)

```
python3 canon/gen_canon_tokens.py        # tokens/*.json      -> AUTO-GENERATED TOKENS block
python3 canon/gen_canon_components.py     # snippets/*.html    -> AUTO-COMPONENTS block
python3 _validate_compose.py              # gate
```
Both rewrite only their AUTO block; the hand-authored aliases / utilities / gap patterns in
between are preserved. Idempotent.

## Add / change a component

Edit the **snippet** (`snippets/<Name>.reference.html`) — it's the reviewed source of truth and
stays covered by `_validate_snippets.py` (token-fidelity + a11y) and `_validate_icons.py`. Then
run `gen_canon_components.py`. Never hand-edit the component inside canon.css. New patterns that
aren't a snippet yet (account card, summary, stat grid…) live in the hand-authored
JOURNEY/SCREEN PATTERNS block as `.c-*`.

---

## Known follow-ups (deliberately not done this session)

- **Icon-source gate on composed screens** — `payments-journey.canon.html` uses inline SVG paths
  (like the original fitness-test). To bring composed screens under `_validate_icons.py`, wire the
  `assets/icons/` sprite (`<symbol>` + `<use>`) instead of inline paths.
- **Dark RAG token gaps** (`[[dark-rag-token-gaps]]`) — canon faithfully mirrors them
  (`--rag-information` dark = `#4587A7`, the illustration-blue leak that fails contrast). Fix
  belongs in `tokens/semantic-colour.json`, then re-run the generators.
- **Promote gap patterns to snippets** — the `.c-*` JOURNEY/SCREEN patterns aren't gated yet; once
  reviewed, give each a snippet so it generates into the `.cn-*` layer like the rest.

---

## Step 1 is the reader — the thin-slice SEED and the ASK door (`s277-D10` · `s277-D13` · `s278-D1`, #279)

**What changed.** Step 1 of generate-from-canon no longer reads the library. It runs
`knowledge/_compose_slice.py` once and works from the SEED it returns; the consumer is
`designer-skills-v2/generate-from-canon/SKILL.md` § Procedure step 1 (landed in the same commit —
`s274-D11`). Reading the 137 metas + `canon/canon.css` is the DECLARED FALLBACK for a pack that
does not carry the reader, never the default.

```
python3 knowledge/_compose_slice.py "<request>" --out seed.json --explain      # the seed, once
python3 knowledge/_compose_slice.py "<request>" --roles page-frame,record-list --intent comparison \
        --components button,table --shape "parts-of-whole" --budget 20000       # typed inputs
python3 knowledge/_compose_slice.py --ask "what governs component:button?" --seed seed.json   # on demand
python3 knowledge/_compose_slice.py --measure                                   # the claim, re-measured
python3 knowledge/_compose_slice.py --selftest                                  # 43 named bites
```

**The contract (in).** `task` sentence, and/or the typed inputs: `intent` (a `chart-intents.json`
word), `shape` (a meta `shape` string), `roles` (`roles.json` keys), `components` (an optional
explicit set, forced in), `budget` (cl100k tokens for the seed).

**The contract (out) — eight fields, every one content or `null` + a note in `$nulls`:**

| field | what it carries | read from |
|---|---|---|
| `components` | one winner per role + capped alternates; `why`, `when`, `snippet`, edges, `score` | `components/*.meta.json`, `roles.json` providers + `providesRole` edges, `chart-intents.json` |
| `governs` | the rulings over those components — Dave's law | `edges.governedBy` + `_rulings.json` `governs[]` (meta path or renderedBy snippet), read LIVE |
| `obeys` | rules + UX principles in three classes, BLOCKING first: **authored** (`edges.obeys`, with the meta's `$why`) · **derived** (a typed hop the meta did not author: `flaggedBy` via its snippet, a rule id cited in prose) · **routed** (a BLOCKING rule whose file the vocabulary routes) | `edges.obeys`, `_rule_nodes.json`, `guidelines/_rules-index.json` |
| `mustNot` | `mustNotNeighbour` from edges AND prose, plus `not-with` — the `ref:null` rows are carried with their `$note` (51 of 70 today) | the metas |
| `tokens` | the token GROUP and its tier (semantic / component-type / foundation / primitive / composite), ≤4 members, an honest count — never the leaves | the metas' `tokens` blocks against `tokens/*.json`; `typography-composites.json` as tier `composite` |
| `assets` | every `usesIcon` / `usesLogo` edge from a chosen component, plus its declared-null asset edges | `_icon_nodes.json` + `_logo_nodes.json` (`s277-D4..D7`) |
| `unresolved` | everything not resolved, each `ref:null` + `$note` + `why` — incl. the photo limit (no node kind) | — |
| `sized` | cl100k tokens (a LABELLED estimator, `ds-021`) whole and per field, vs the metas it replaces and the library; `budget`, `within_budget`, `reductions` | tiktoken |

Over `budget` the seed REDUCES by declared steps (drop alternates → drop routed obeys), each recorded
in `sized.reductions`; if still over it refuses (`SliceRefused`, exit 3) — never a silent truncation.

**ASK — the on-demand half.** The seed is composed once and is NOT session state (`s278-D1`). When
the next prompt needs a node the seed excluded, or a ruling inscribed after the seed, ASK reads the
Constitution LIVE (`_rulings.json` + the metas' edges + the ratified node files are re-read on every
call) and returns the answering slice for one of the 12 canonical questions in ≤1,000 cl100k tokens,
or refuses loudly naming the count. The verbs: `governs` · `binds` · `principle` · `conflicts` ·
`ruled` · `evidence` · `answers` · `avoid` · `tokens` · `usedIn` · `wcag` · `assets`. Name the node
as `kind:id` (`component:button`, `rule:ctkb-003`, `ruling:s277-D10`, `sc:1.4.3`,
`intent:comparison`) or by its meta name. Three answers carry a declared limit because the graph has
no such edge: `principle` (no rule→ux edge), `conflicts` (no rule→rule conflict type; the 2-hop
`tensionWith` between obeyed principles is walked and is empty on today's tree), `tokens` (no
`token:` node kind — blast radius comes from `tokens/_blast-radius.json`, a derived index). ASK never
mutates the seed (selftest proves it byte-for-byte) and never touches `_rulings.json`.

**Gate it.** `python3 knowledge/_compose_slice.py --selftest` (43 bites: every out field present;
nulls carry notes; ASK ≤1K on all 12; ASK sees a ruling planted AFTER the seed in a scratch copy of
`_rulings.json`, never the live file; seed unchanged by ASK; budget refusal; the live reader agrees
with `_build_kg_explorer.extract()`+`extract_extra()` on shared edge-type counts), then
`python3 knowledge/_validate_kg.py` on the live tree.

**Measured, not asserted (2026-09-16, `--measure`, the dashboard task).** Seed 28,621 tokens
against 111,468 for the 31 metas it names (3.9×) and against 1,005,758 for what step 1 read before
the wiring — every meta 414,184 + `canon.css` 588,102 + `type.css` 3,472 (31.8×). The `s277-D10`
figure (19,117 / 5.8×) was the PROPOSAL's field set; the contract's `governs` (38 live rulings, not
3) and `assets` (31 rows, not 0) are the difference, and are content the old slice did not carry.

**Correction, by addition (#279 lane SC2, 2026-09-16, RV F2).** The "31.8×" in the paragraph above
was re-typed, not measured: `notes/_lanes/279/reader/measure.json` line 22 says
`"ratio_vs_step1_before_wiring": 35.14` (1,005,758 / 28,621). The live figure today, after lane SC's
routed-by-scope rows and lane SC2's per-rule facet override: seed 31,372 vs 111,468 (3.55×) and vs
1,005,758 (32.06×) — `python3 knowledge/_compose_slice.py --measure`. The paragraph stands as
written; this note is the record of the slip.
