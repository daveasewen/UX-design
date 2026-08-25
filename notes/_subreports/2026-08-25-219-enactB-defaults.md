# #219 lane B (enact) — the TWELVE SHIPPED DEFAULTS and the three gallery supersessions

**Lane:** enact-B, #219 afternoon wave. **Model:** Opus. **Scope:** the settings compilation and
the gallery surfaces — the library's Foundations generator, the photography page it writes, and
the two probes that drive it.
**Files this lane owns and touched:** `knowledge/_render/gen_foundations_217.py`,
`knowledge/_render/verify_photography_218.py`, `knowledge/_render/verify_foundations_217.py`,
`showroom/_foundations/photography.html`, `showroom/_foundations/logos.html` (one shared-CSS
comment), and TWO new artefacts: `knowledge/_render/role_defaults_219.py` and
`reviews/SQUARING-PORTRAIT-2026-08-25-v1.html`.
**Not touched:** `gen_bento_matrix_217.py` and `showroom/_foundations/bento.html` (lane A),
`gen_grids_218.py` and the four `grids-*.html` (see UNPROVEN ②), `knowledge/_rulings.json`,
`knowledge/tokens/layout.json`, canon, `GOOD-MORNING.md`, `_CHAIN.md`, `_LIVE-STATE.md`, constants
and bands, any Dave-owned row. No commit. No regen serial.

**COUNTS:** findings 12 · ruling-shaped 7 · UNPROVEN 5 · new gates 4 selftest bites + 1 browser
arm + 1 blocking contrast sweep · files changed 4 + 2 new · store rows minted 3 (W-99zo/zp/zq)

---

## 1 · The twelve are minted, and they have ONE home

`knowledge/_render/role_defaults_219.py` **parses** Dave's receipt
(`notes/_receipts/2026-08-25-219-role-defaults-exports.md`) at import time and exposes
`DEFAULTS[type][theme]` (his `state` blocks — the ruling) and `RESOLVED[type][theme]` (his
`resolved` blocks — the pixels he approved). **Not one of the twelve is re-typed anywhere**: a
default typed into Python is a second copy of a decision, and the copy is the one that goes stale
(ADR-0017 / [[write-once-principle-floated-192]]). The module imports **nothing of the render
stack**, deliberately — `gen_foundations_217` imports `gen_bento_matrix_217`, so a defaults table
living in either one is unreadable by the other without a cycle.

The parse REFUSES, by name, if: the receipt is missing; any of the twelve is absent; a `### theme`
heading and its JSON `type` disagree; or a type's dial set differs from the grammar
(`dashboard` main+sub, `display`, `gallery`'s eight). The headings rule, not `resolved.theme` —
the #218 lesson, where two exports were taken in the legacy tab.

**Interop with lane A, verified after the fact:** their `_bento_edit_rails.json` looks for
`gen_foundations_217.ROLE_DEFAULTS` **by address** and now resolves it
(`"$resolved_from": "gen_foundations_217.ROLE_DEFAULTS"`), validating each of the twelve against
their option space. The two lanes landed on one table without coordinating — theirs owns the
OPTION SPACE, this one owns the DEFAULTS.

Validation is now **type-aware and covers all twelve** (`validate_all()`, selftest bite 23): every
dial word against `gen_bento_matrix_217`'s own option sets, keylines against
`keylines_for(type, theme)`, gallery P2/P3 legality, and spacing against the s219-D1(4) rails.
`control_gap()` reports any ruled stop no control can reach — **empty today**, because lane A
widened `SPACINGS` to the same six stops in the same wave. The two rails are asserted EQUAL at
mint time, so they cannot drift apart in silence.

## 2 · The three supersessions, enacted

**(1) MONO CAPTIONS GO LIGHT GREY — `s219-D2 (1)`.** `capBg: grey` is the dial's word for
**`--surface-subtle`**, and that is the token, not a literal. The identification is not a
guess: mono resolves it `rgb(240, 240, 240)`, which is exactly what Dave's own export measured
(selftest bite 25b pins the receipt's readback so the identification cannot drift off the colour he
saw). The #218 rider (`--surface-digital-black` ground, `--text-reverse` ink) is **retired** —
`MONO_CAPTION_RIDER = None`, kept as `RETIRED_MONO_RIDER` with his words on both sides so
`s218-D6 (1)` reads as superseded history rather than as a thing that never happened. Bite 25
flipped with it: it now asserts the grey token IS there and the two rider tokens are **nowhere** in
the compiled block.

**THE INK TOKEN, AND THE CHOICE IS DECLARED: `--text-secondary`.** Two candidates existed and they
resolve **identically** in both themes that ship a grey caption ground: mono and console inherit
canon's `:root` tier, where `--text-secondary` and `--text-default` are both `#1A1A1A`. Enacted
`--text-secondary` because it is the token `.px-cap` has always used (through the page's
`--ink-2`) and because it keeps caption ink ONE decision across four themes. The pair diverges only
in legacy (`#545454` vs `#333333`), whose caption ground is transparent — so the choice is
invisible in today's paint and would only ever surface if a legacy caption went grey. **Filed as
Q3.**

**(2) SQUARE IS THE GALLERY-ROLE DEFAULT — `s219-D2 (2)`.** All four exports say `edge: square`;
the pass runs and the report's `enacted_by` now names `s219-D2 (2)` rather than s218-D6(4)'s
this-wall-only scope. **What did NOT move, and is declared rather than assumed away:**
`knowledge/tokens/layout.json` still records `$roles.gallery.squaring: false`, so
`role_policy("gallery")` still answers EXEMPT. Flipping it is a canon regen — the ordered serial —
which this lane may not run. The role's answer is asked on every build and carried on the report
beside the enactment, and bite 29b was re-worded from "the override is this page's" to "the role
policy is UNCHANGED, pending". **Filed as Q1.**

**(3) CONSOLE GALLERY ROUNDING IS CAPSULE — `s219-D2 (3)`.** The capsule branch puts canon's
container radius on the TILE and squares the picture inside it. Measured live: console tile radius
**20px**, picture 0; the other three 0/0. Resolves s217-D5's open P3 by his own export.

**(4) KEYLINES AS EXPORTED — `s219-D2 (4)`.** ON in legacy gallery only. The compiled block now
carries **both constructions** (a new bite, 24b, asserts exactly one theme has the edge), and the
ON construction draws a `1px` `--border-subtle` edge on the opener with the tile ground still
unpainted — the export's own `tileBorderPx: 1`. The keyline INK is a build choice, filed as Q7.

**Live gutters, measured:** mono 40 · legacy 24 · console 40 · supercharge 1 px (bite 24).

## 3 · A consequence that is NOT cosmetic — `pageBg: transparent` on a whole page

Three of the four gallery defaults say `pageBg: transparent`. In the explorer that means "the
stage's ground shows through". **On this page the wall IS the page**, and a body that paints
nothing falls through to the **UA canvas — white, in every theme, in dark mode too.** So a
transparent page ground compiles to `--background-default` (`page_bg_decl`), which is the surface
beneath a page body and exactly what this page painted before any settings block existed. It stays
on the BODY, not `html`: canon declares the dark tier on `[data-theme="dark"]`, which is the body —
painting `html` would resolve the LIGHT token in dark mode, silently, in all four themes.

Enacted as the obvious reading, **named on the page as PROPOSED**, and the probe prints it as a
declared divergence from the receipt's `rgba(0, 0, 0, 0)` readback rather than skipping it.
**Filed as Q2.**

## 4 · Squaring, the re-spans, and the portrait evidence page

The pass re-spanned **4 tiles in the last 5**, crop cost **10** on its own ordinal scale, ladder
4/3/2/1, zero holes at every band (re-measured off the SHIPPED markup by the probe, not off the
generator's report):

| tile | before | after |
|---|---|---|
| 247 `stocksy-6629948-w1600.jpg` (1067×1600, portrait) | 1×2 | **3×1 — the flattened portrait** |
| 248 | 1×1 | 2×1 |
| 249 | 1×1 | 2×1 |
| 251 | 1×1 | 3×1 |

`reviews/SQUARING-PORTRAIT-2026-08-25-v1.html` renders tile 247 **before and after** side by side,
plus the last twelve tiles as a before/after wall with the re-spans marked. It is **PROPOSED and
rules nothing** — `s219-D2 (2)` expressly leaves the orphan/flattening refinement (the W-99zi third
bend) open, and the page says so in its own first sentence. Nothing is re-drawn: the stylesheet,
header, theme script and tile markup are copied out of the shipped page, with two edits declared on
the page itself (opener is a `div`, asset paths one level shallower).

## 5 · Probes, contrast, mutants

**Contrast sweep — BLOCKING now.** The caption's ink is measured against its **effective** ground
(its own, or the bento's, or the page's — whichever actually paints), and anything under WCAG AA
4.5:1 is a FAILURE, not a note. Eight states, all pass:

| state | caption ground | ink | ratio |
|---|---|---|---|
| mono/light | rgb(240,240,240) | rgb(26,26,26) | **15.27:1** |
| mono/dark | rgb(31,31,31) | rgb(255,255,255) | **16.48:1** |
| legacy/light | transparent → white | rgb(84,84,84) | **7.57:1** |
| legacy/dark | transparent → rgb(31,31,31) | rgb(155,155,155) | **5.93:1** |
| console/light | rgb(240,240,240) | rgb(26,26,26) | **15.27:1** |
| console/dark | rgb(31,31,31) | rgb(255,255,255) | **16.48:1** |
| supercharge/light | transparent → rgb(247,246,244) | rgb(19,17,14) | **17.45:1** |
| supercharge/dark | transparent → rgb(26,26,26) | rgb(247,246,244) | **16.11:1** |

Lowest reading **5.93:1** (legacy dark). Dark falls out of the tokens throughout; **no
dark-specific value was invented** anywhere.

**Green:**
- `gen_foundations_217 --selftest` — **39 bites**, including 4 new/flipped (6b radii set, 24
  gutters, 24b keyline split, 25 supersession, 25b receipt pixel, 29/29b squaring provenance).
- `role_defaults_219 --selftest` — the parse, the twelve, and s219-D1(5)/D2(1..4) hand-computed
  against the rulings' own sentences rather than read off the parse.
- `verify_photography_218 --static` — 251 tiles, 502 lazy images, zero holes off the shipped markup.
- `verify_photography_218 --themes …` — **all four themes × light/dark green**, every expectation
  now READ OFF THE RULED DIAL (see below).
- `verify_foundations_217 --page photography` — 8 states, no dangling property, theme reached the
  paint in all four.

**The probe was re-pointed, not weakened.** `verify_photography_218` asserted ONE shape for four
themes (white grounds, corners, keylines off, transparent captions bar the mono rider). Under
s219-D1/D2 the defaults DIFFER BY THEME, so that probe would have redded the ruling rather than the
page. Every expectation now comes from `foundations.GALLERY_SETTINGS[theme]` and from the TOKENS
resolved live in that state; the receipt's own literals are cross-checked in light mode, with the
transparent-page divergence declared rather than skipped.

**Mutation arms, both seen RED by name:**
- `--break-settings` (existing) → 10 `SETTINGS` failures across GUTTER · KEYLINES · CAPTION ·
  CAPTION GROUND · PAGE GROUND.
- **`--break-default` (new, this lane)** → the block ships INTACT with exactly one minted default
  wrong (mono `capBg` grey→white). Required red is the **`SETTINGS CAPTION`** bucket specifically,
  not "a settings assertion": 2 failures, `CAPTION GROUND` (dial says grey, resolved white) and
  `CAPTION` (Dave's export resolved rgb(240,240,240)). This is the arm that proves the probe tests
  the RULED DEFAULT and not merely that a settings block exists.

**Render-verified** (fifth stratum, `/var/tmp/chromelibs-s213e2`, tiktoken present): four
screenshots of the wall seen first-hand — mono/light (grey captions, dark ink), console/light
(capsule tiles), legacy/light (1px keylines, 24px gutter), mono/dark — plus both halves of the
evidence page. Shots left NON-REPO at `/var/tmp/shots-219eb-viewed/`.

## 6 · Findings

1. The twelve are parsed, not typed; one home, and lane A already consumes it by address.
2. `grey` = `--surface-subtle`, identified from Dave's own resolved pixel, not from a comment.
3. Console capsule enacted — tile radius 20px measured live, picture squared.
4. Keylines split by theme within one role; legacy carries the edge (the s135-D1 echo holds).
5. Gutters 40/24/40/1 live and per-theme.
6. `pageBg: transparent` on a whole page would have shipped a WHITE dark mode. Enacted as the
   document ground; PROPOSED and named.
7. Squaring re-spanned 4 tail tiles; the flattened portrait is tile 247, `stocksy-6629948`.
8. Eight contrast readings, minimum 5.93:1 — the sweep is now blocking and it passes.
9. ⚠ **The caption-ground dial is UNFALSIFIABLE in mono dark.** `--surface-raised` and
   `--surface-subtle` both resolve `#1F1F1F` there, so the minted-default mutant is invisible in
   dark mode and only reds in light. The arm is honest about it; the token pair is not.
10. `supercharge`'s `grey` resolves **warm** — `rgb(223, 222, 220)` vs `rgb(240, 240, 240)` in the
    other three (standing grey-tint rule: SURFACED, never auto-swapped).
11. ⚠ **Render-verify pothole, for the runbook:** `/var/tmp/fonts-218w3/` looks intact but every
    TTF in it is a symlink into a FOREIGN session's mount (`/sessions/happy-magical-davinci/…`),
    which does not resolve here. The font probe then reports "the HSBC face is not rendering",
    which reads as a page defect. `fc-match` named it in one call. Same species as the fifth
    stratum's hollow lib dir: **`ls -la` the farm, don't trust the directory listing.** A fresh
    farm was staged at `/var/tmp/fonts-219eb/` + `/var/tmp/fonts-219eb.conf`.

12. ⛔ **A SUPERSEDED RULING IS STILL BEING PUT TO DAVE AS CURRENT, on three review pages —
    NOT THIS LANE'S FILES, flagged for the conductor.** `knowledge/_render/_bento_recut_219.py` is
    the one home for the bento decision ledger, and it carries `s218-D6 (1)` as **RULED** plus a
    `mono_caption_css()` helper that paints `--surface-digital-black` / `--text-reverse` captions.
    Three generated pages consume it — `reviews/BENTO-CANON-2026-08-25-v4.html` (via
    `gen_bento_canon_217`), `-v5.html` (via `gen_bento_roles_217`) and
    `reviews/GALLERY-COMPARE-2026-08-25-v2.html` (via `gen_gallery_compare_217`). As of `s219-D2
    (1)` that ground is **retired on the gallery role**, so those three pages now show Dave the
    superseded ground beside a ledger that calls it settled law. This lane did not touch them: they
    are review surfaces owned by the re-cut/review-regen lane, and the ledger's own rule is that it
    is quoted from `_rulings.json`, not edited by a consumer. **The ledger needs a `s219-D2 (1)`
    supersession row and `mono_caption_css` needs re-pointing (or renaming to what it now is:
    frozen #218 history).** [[read-chain-is-where-staleness-is-free]].

## 7 · UNPROVEN

1. **Eight of the twelve defaults have no compiled consumer.** Dashboard and display are parsed,
   validated against the option space and exposed — but no surface this lane owns RENDERS them, so
   they are proven legal, not proven right ([[instrument-without-a-consumer]]). See Q4.
2. **The explorer and the four `grids-*` pages were NOT regenerated.** `--check` reports six pages
   out of sync (`bento.html`, `grids-*`, and `logos.html`); `logos.html` was mine (a shared-CSS
   comment) and IS regenerated. The other five are lane A's drift from their matrix edits, in their
   lane. **The conductor must not read that `--check` red as this lane's.**
3. Whether the token store's gallery role policy should follow the default (Q1) — untested,
   because the canon regen was not run.
4. **Responsive bands were driven at 1280×900 only.** The gutter moved from 24 to 40 in two themes
   and to 1 in supercharge; the canon container-query bands (1100/820/520) were not re-driven at
   narrow widths after that change.
5. No repo-wide CI sweep was run — the blocking contrast sweep here is the page probe's 8 states.

## 8 · RULING-SHAPED QUESTIONS (Dave's, not this lane's)

1. **Does the token store follow the default?** `s219-D2 (2)` makes square the gallery-role
   default; `layout/bento/$roles/gallery/squaring` is still `false`. Flipping it changes what EVERY
   gallery bento does when it carries no instance dial — including surfaces nobody has looked at
   today. Canon regen, ordered serial. **Or** the role stays ragged-tolerant and the default lives
   only in the settings table, which is what ships now.
2. **What does `pageBg: transparent` mean on a whole-page gallery?** Enacted: the document ground
   (`--background-default`). The alternative reading is `--surface-raised`. The dial cannot mean
   "paint nothing" on a page body without shipping a white dark mode.
3. **Caption ink token — `--text-secondary` (enacted) or `--text-default`?** Identical in mono and
   console today; diverges only if a legacy caption ever goes grey.
4. **Where do the dashboard and display defaults get CONSUMED?** Options: the four `grids-*` pages
   boot from `ROLE_DEFAULTS` for their type and theme (a live default preview, lane B's files), or
   the explorer's controller boots from them (lane A's `STATE` literal, currently one hard-coded
   default for all themes), or they stay a manifest until an editor exists.
5. **Mono dark's caption ground is undecidable** — `grey` and `white` both resolve `#1F1F1F`. Does
   the gallery caption want a dark-mode ground of its own (a dark-specific CHOICE, which would be
   PROPOSED — nothing was invented here), or is the collapse acceptable?
6. **Supercharge's warm grey** — `rgb(223, 222, 220)`. Surfaced under the standing grey-tint rule;
   not swapped, not proposed away.
7. **The gallery keyline's INK.** The export gives `tileBorderPx: 1` and no colour; enacted
   `--border-subtle` (the page's own `--line`). s218-D1's corner-keyline construction is a
   different thing and is dashboard-only — is `--border-subtle` the gallery keyline, or is that a
   dial of its own?

## 9 · REPLAY-THESE (for the conductor)

- `python3 knowledge/_render/role_defaults_219.py --selftest`
- `python3 knowledge/_render/role_defaults_219.py --table` — the twelve, as parsed
- `python3 knowledge/_render/gen_foundations_217.py --selftest` (39 bites, ~60s: the squaring pass
  costs ~55s of it)
- `python3 knowledge/_render/verify_photography_218.py --static`
- `python3 knowledge/_render/verify_photography_218.py --themes mono,legacy` and
  `--themes console,supercharge` (render-verify env staged; sandbox wall)
- `BM_MUTANT_DIR=/var/tmp/mut-<session> python3 knowledge/_render/gen_foundations_217.py
  --break-default` then `… verify_photography_218.py --default-mutation --themes mono,console`
- ⛔ **Conductor action, cross-lane:** finding 12 — `_bento_recut_219.py`'s ledger still states
  `s218-D6 (1)` as ruled and still paints the retired dark caption on three review pages. It is
  neither lane A's nor lane B's file.
- **Dave's eye owed on:** `reviews/SQUARING-PORTRAIT-2026-08-25-v1.html` (the flattened portrait),
  and the photography page in all four themes (the mono/console grey captions and the console
  capsule are new surfaces, not re-renders).
