# Nio dashboard → Apollo Console — v2 change table

**Artefact:** `knowledge/_fitness-test/nio-dash-console-v2.canon.html`
**Generator:** `knowledge/_render/gen_nio_dash_v2.py` (re-run it; never hand-edit the HTML)
**Probe:** `knowledge/_render/verify_nio_dash_v2.py` (`--stage a` · `--stage b` · `--stage shots`)
**Predecessor:** `nio-dash-console-v1.canon.html` — **BYTE-UNTOUCHED.** v1's own composition
mapping (`nio-dash-console-v1.mapping.md`) still governs; **nothing in it is superseded except
where a row below says so.**
**Status:** ⬛ fitness test. NOT gated as canon, NOTHING RULED, awaiting Dave's eye.

v2 is v1 plus **six requested changes and two defects found while making them.** No component was
re-drawn, no colour value was authored, no `font-size` or `font-weight` was declared, and no
`.c-*`/`.cn-*` class was redefined. Both gates PASS.

---

## ① Light grey page background — and why v1 did not have one

**What Dave asked for:** a light grey page behind the white cards.

**What was actually wrong — and it is not what it looks like.** v1 declared
`body{ margin:0; background:var(--surface-hover); color:var(--text) }` and **that rule was never
parsed at all.** v1's harness header comment wrote its exclusion list with literal asterisks —
`no .c-<star>/.cn-<star>` — and `<star>` followed by `/` **is a CSS comment terminator.** The
comment closed early, the parser hit garbage, and it **discarded the very next rule**, which was
the `body{ }` rule.

Measured, first-hand, on v1 in Chromium:

| reading | v1 | v2 |
|---|---|---|
| rules the page `<style>` actually parses to | **45, with no `body` rule in the list** | 46, `body` present |
| `body` background, Console light | `rgb(255,255,255)` — same as a card | `rgb(240,240,240)` |
| `body` `margin-top` | **`8px`** — the browser default | `0px` |

So v1 has *two* dead declarations, and the second one is visible: **v1 still carries the
browser's default 8px body margin.** A specificity fix would have been a false fix on a true
symptom. This is the same species as **ds-039's second form**, which
`canon/gen_canon_components.py` already guards against **at the emitter** for `canon.css` — but a
composed screen writes its own `<style>` block and **no gate parses it.** Logged (see
`_DS-IMPROVEMENTS.md`).

**How v2 paints the page.** canon.css paints with `.canon{ background: var(--page) }`. v2 does not
out-specify that rule; it **re-points canon's own `--page` variable on `<body>`**. Every `.cn-*`
scope re-declares `--page` from `--background-default`, so nothing inside a component is
disturbed — proved by asserting the donut's inter-arc `stroke="var(--page)"` still resolves to
`--background-default` in both modes.

**⚠ THE GREY IS PER-MODE, AND THAT IS A TOKEN DEFECT, NOT A PREFERENCE.** Under Console there is
**no single surface token that is grey-and-distinct-from-card in both modes.** Measured:

| mode | token | resolves to | card (`--surface-raised`) | verdict |
|---|---|---|---|---|
| light | `--surface-subtle` | **`#F0F0F0`** | `#FFFFFF` | **distinct ✓ — v2 uses this** |
| light | `--surface-hover` / `--surface-raised-hover` | `#F0F0F0` | `#FFFFFF` | distinct, but semantically a *hover* token |
| light | `--background-default` | `#FFFFFF` | `#FFFFFF` | **identical ✗** |
| dark | `--surface-subtle` | `#1F1F1F` | `#1F1F1F` | **identical ✗** |
| dark | `--background-default` | **`#1A1A1A`** | `#1F1F1F` | **distinct ✓ — v2 uses this** |

v2 therefore selects `--surface-subtle` in light and `--background-default` in dark. **Zero values
are minted** — both are existing tokens read verbatim. This is the same defect the bento
exploration surfaced from the other side (`surface/raised ≡ background/default` in light), seen
now in dark as well: **the library has no "page behind raised surfaces" token that keeps its
meaning across light and dark.** Which token a page should paint with is Dave's.

## ② 1600px content column

`.l-container` owns its own `--l-max` (canon default **1120px**). v2 **re-points that variable** on
the page shell rather than overriding the rule, so the component keeps owning its own centring
maths. The masthead and footer inners take the same measure from a harness class, so chrome stays
full-bleed while its content lines up with the column.

Measured: `--l-max` on `<main>` reads `1600px` and `<main>` **renders at 1600px** in an 1800px
viewport (a variable can be set and ignored; the rendered width is the proof). v1 reads `1120px`
through the same probe.

## ③ The Console-styling miss on inputs — root cause

**It is not a cascade-order, specificity or scope problem.** The search field IS inside
`.cn-search-field`, and `--border-radius-control` resolves to **8px on that very element.**
**The component's CSS simply never consumes it.** Measured under Console, v1:

| element | computed `border-radius` | `--border-radius-control` on it |
|---|---|---|
| `.cn-search-field .search.boxed` | **`0px`** | `8px` |
| `.cn-input-fields` boxed field | `8px` | `8px` |
| `.cn-dropdown .trigger` | `8px` | `8px` |
| `.cn-account-selector .as-trigger` | `8px` | `8px` |
| `.cn-amount-input .ai-box` | `8px` | `8px` |
| `.btn.primary` | `8px` | `8px` |

Search-field is the **only** boxed control on this screen that draws a 1px box and declares no
radius. Under Console (8px) it is the one square control in a family of rounded ones — which is
exactly what *"generic, not Console"* looks like. Under **mono** (radius 0) it looks correct, which
is why it survived review.

**THE CLASS.** A sweep of all 135 `.cn-*` scopes in `canon.css` finds **16 that declare no
`border-radius` at all**, and **seven of those nevertheless draw a full 1px box**:

`.cn-search-field` (`.search.boxed`) · `.cn-headers` (`.frame`) · `.cn-quick-actions` (`.qa`) ·
`.cn-reorder` (`ul.reorder`) · `.cn-view-options` (`.seg`) · `.cn-splitter` (`.demo-box`) ·
`.cn-pagination` (`.pg a`, transparent border).

Every one is invisible under mono and wrong under the other three themes.

**Where the real fix lives:** `knowledge/snippets/Search-field.reference.html`. `canon.css` is
GENERATED from the snippets by `canon/gen_canon_components.py`, so a `canon.css` edit would be
erased on the next regeneration. It is **not applied here**, for two stated reasons: it is a
gated-snippet change and un-ruled, and `canon.css` is shared — changing it would retroactively
restyle **v1**, the artefact Dave asked to keep as the comparison. Logged instead.

**What v2 does:** one page-level rule applied to the **class** of boxed search fields on this
screen (both instances and any added later), consuming the token the component forgot:
`.nio-shell .search.boxed{ border-radius: var(--border-radius-control) }`. It names no `.cn-*`
selector, so the compose gate's redefinition check stays satisfied. Verified: **every**
`.search.boxed` on v2 now equals `--border-radius-control` in both modes; v1 reads `0px` through
the same probe.

**⚙ What a compiled per-theme stylesheet would have prevented** (evidence for the ADR-0011 /
`s200-D1` proposal — this page does **not** build it). A compiler minting a Console sheet from the
override store would emit a concrete `border-radius: 8px` for every rule that draws a box, and the
absence of a radius declaration on a boxed control becomes a **missing output** — a thing the
compiler can be *asked about* ("which boxed controls got no radius under console?") and can refuse
to emit. Today the miss is a **non-event**: the token resolves correctly, nothing dangles, no gate
has anything to look at, and the only detector is a human noticing one square corner among six
rounded ones. **The defect is not a wrong value; it is an unconsumed value, and only a compiler
that enumerates consumers can see it.**

## ④ Light / dark switch

`data-theme` on `<html>` — the bento showcase mechanism — driven from a canon
`.cn-segmented-control`. Real `<button>`s, so Tab plus Enter/Space work natively. The sliding
indicator is re-placed through **canon's own** `dv-behaviour.js` `placeSegs()` (a resize event),
not re-implemented. Driven both ways in the probe: by clicking, and by focus + Enter.

## ⑤ Donut legend — capsule vs list, live toggle, **neither recommended**

v1 needed two blocks side by side to reproduce the reference: `.dv-leg` (the interactive filter,
names only) **plus** a `.cn-summary` `dl` (the figures). v2 adds a **list** variant that merges
them: one list beside the donut, **swatch + letter + label + value** per row, plus a Total row.
The switch is live; **neither variant is defaulted as a recommendation.**

**⚙ It needed no behaviour-layer extension, and that is the finding.** `dv-legend.js` binds nothing
to a layout: every listener is delegated at document level and resolves by **class contract** —
`.dv-leg` host, `.dv-legrow[data-series]`, `.dv-leg-sw`, `.dv-leg-item`, `.dv-leg-reset`,
`.dv-leg-name` — with state parked on the host as `host.__dv`. A list-shaped legend that honours
that contract inherits hover-fade, ghost-toggle, the DV-D19 isolate latch, the "at least one must
stay" guard, Reset and the live region **for free**. The value cell sits **inside** `.dv-leg-item`,
after `.dv-leg-name`, so `nameOf()` reads exactly what it read before.

⇒ **COMPONENT-VARIANT CANDIDATE, not a new component:** dv-legend gains a **value column** and a
**list presentation**. Gap-logged; not added to the showroom. This is the DS question v1's mapping
row 19 already asked.

**Parity, proved not asserted.** Both legends were driven through the same two gestures and the
chart read back after each:

| gesture | capsule → series ghosted | list → series ghosted | donut centre |
|---|---|---|---|
| uncheck series 3's swatch | `3` | `3` | `12684` both |
| isolate series 1 by its label | `2,3,4,5,6` | `2,3,4,5,6` | `8500` both |

Plus a **mutation**: the same assertion run against a wrong series id goes red, so the parity check
can fail.

**⚠ Two honest limits, both declared and neither hidden:**
- dv-legend keeps **one state record per host**, so the two legends hold separate states. The
  variant switch therefore **resets the outgoing legend** (clicks its own Reset) before swapping —
  **selection does not carry across the switch.**
- dv-legend's hover path resolves a figure's legend with `figure.querySelector('.dv-leg')` — the
  **first** match. The inactive legend therefore has its `dv-leg` class removed while hidden, so
  exactly one legend is ever discoverable. Without that, hovering an arc would drive the wrong
  record. Asserted: exactly **1** `.dv-leg` in the donut figure at any time.

## ⑥ Chromeless account-list variant, live toggle against v1's card form

`.cn-list-items` draws its chrome in exactly three places. Chromeless switches off the first two
and **keeps the separator** — which is the brief. Measured:

| variant | `ul.list` background | `ul.list` border | `li + li` separator | `.tag` border | row `min-height` |
|---|---|---|---|---|---|
| **Card** (v1's form) | opaque | `1px` | `1px solid` | `1px` | `76px` |
| **Chromeless** | transparent | `0px` | **`1px solid` ✓** | `1px` | `76px` |
| **Chromeless, plain tags** | transparent | `0px` | **`1px solid` ✓** | `0px` | `76px` |

Because the tag outline is genuinely ambiguous as "chrome", **both readings are offered** rather
than one being picked. Row markup, hover, press, focus ring and geometry are untouched in every
variant (the rows are still focusable buttons — asserted). Transparency comes from the existing
`--surface-transparent` token, not an authored value.

⇒ **COMPONENT-VARIANT CANDIDATE for `.cn-list-items`: a `flush` form.** Gap-logged; not added to
the showroom.

---

## Two defects found while building v2 — both measured, neither invented

**A · Canon scope bleed: the page-shell scope carries chart geometry.**
`canon.css` line ~16124 declares `:where(.cn-template-dashboard) .dv-svg{ width:580px; height:260px }`
— component-specific chart geometry living in a **template** scope, and it comes **later** in the
file than `:where(.cn-chart-donut) .dv-svg`, which sets no width at all. So on **any**
dashboard-templated page the donut is forced to 580px wide although its own markup says
`width="300"`. In **v1** that makes the donut overflow its 426px column and become horizontally
**scrollable** (`.dv-stage` carries `overflow-x:auto`, which hides the symptom). v2 restores the
size the svg's own `width`/`height` attributes already declare — 300 × 260, read off the markup,
not invented. Logged.

**B · The series palette stops at 5, and the sixth category renders silent black.**
`--data-series-6`, `-7` and `-8` are **defined nowhere in canon.css** (0 occurrences; 1–5 are
defined). The Nio donut has **six** categories, so measured in both Console light and dark:

| series | `--sc` on the swatch | swatch background | arc `fill` |
|---|---|---|---|
| 1–5 | `#766682` … `#A37E94` | painted | painted |
| **6** | **empty** | **`rgba(0,0,0,0)` — invisible** | **`rgb(0,0,0)` — pure black, both modes** |

Present in v1 and **inherited unchanged by v2**, because the honest fix is a new palette step and
this page mints no colour. Asserted in the probe so the defect is a measurement in the record, not
an impression. Exactly the `dangling-dataviz-var-renders-silent-black` class. Logged.

---

## Verification

`_validate_compose.py` **PASS** (28 canon classes, 0 rogue hex, 0 redefines, all resolve, title
unique across 7 screens) · `_validate_screen.py` **PASS** (compose ✅ · icon-source ✅ all paths
library-matched · a11y ✅ with the same `s116-D1` dense-data-mark advisories v1 carries).

`verify_nio_dash_v2.py` — **three stages, 55 checks, all GREEN**:
- **stage a** — 30 checks. Font asserted against two controls (target **346.88** = `--uf` 346.88 ·
  DejaVu 375.39 · nonexistent 301.07). Var sweep over Console light **and** dark, **0 empty**.
  Page-grey, 1600px measure and the search radius proved in both modes. **Five positive controls on
  v1** — its page background is *not* distinct from a card, its `<style>` *has lost* its body rule,
  its body margin *is* 8px, its `.search.boxed` *is* 0px, its `--l-max` *is* 1120px. A test that
  cannot show v1 failing proves nothing about v2 passing.
- **stage b** — 25 checks. Theme switch driven by click **and** by keyboard; legend parity + the
  mutation; the list legend proved to sit **beside** the donut by rectangle geometry; all three
  list-chrome variants read back.
- **stage shots** — 9 screenshots.

**Render-verified in-sandbox, 9 shots taken and 6 LOOKED AT:** full page Console **light** and
**dark** at 1800, the donut in **list**-legend mode and in **capsule** mode, the account list
**chromeless** and **chromeless plain-tags**, the masthead at 1800 (the 1600 column visible against
the grey), and a **560px narrow** full page — single-column collapse, review bar wraps.

## ⚠ UNPROVEN, declared

- **No contrast ratio was computed** for v2 — not for the grey page against card ink, not for the
  list legend's value column, not for the chromeless list. The grey is a token read, not a
  measured pair.
- `_validate_screen.py --render` (the state-contrast arm) was **not re-run** on v2. v1's row
  already records that arm as reading RED for wrapper reasons that are a DS-defect candidate, not
  the screen's defect; v2 changes nothing in that area, but that is an argument, not a measurement.
- `_validate_a11y.py` still ignores a path argument, so its 0-failure figure is repo-wide and did
  **not** assess this file.
- Neither the descender-clip nor the type-composite gate reaches `knowledge/_fitness-test/` at all.
- **Only Console was tested.** v2 is a Console screen, but the search-radius defect is a
  four-theme defect and only Console was measured here.
- The **series-6 black arc** and the **donut centre re-render** (`13734`, no currency symbol, no
  thousands separator — v1's declared divergence 5) are **carried, not repaired.**
- The page is wired into **no build step and no CI job**. **Not committed, not pushed.**

⛔ **Nothing on this page is ruled, recommended or preferred.**
