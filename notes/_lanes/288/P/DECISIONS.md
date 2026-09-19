# 288/P — DECISIONS made while composing, each with the rule or token it rests on

Lane P of #288. The template was fenced; every structural and content decision below was
taken from the brief + the graph's rules + the component snippets, and written down as it
was made. "designer's call" = nothing in the system governs it.

THE PROMPT USED (the frozen demo prompt was NOT recoverable — see the report):
"Build an operations dashboard for a bank's Chief AI Officer: AI programmes in flight,
their spend against budget, efficiency gains realised, risk and compliance exceptions, and
what needs a decision this week. Desktop first, 1440 wide."

---

## A. The shell

**A1 — Theme mechanism: `class="canon" data-theme="light"` on `<html>`, and NO
`data-apollo-theme` attribute.**
Rests on: `knowledge/canon/canon.css` BASE block ("apply `.canon` (and optionally
`data-theme`) on the root element") + `knowledge/canon/gen_theme_cascade.py` docstring
("resolve(role, mode, theme): theme override wins; else base (Mono)") +
`knowledge/tokens/themes/` holds override files for console/legacy/supercharge only.
Mono is the BASE, so Mono is the ABSENCE of the theme attribute. Read from canon itself,
not assumed.

**A2 — Both stylesheets linked: `canon.css` and `type.css`.**
Rests on: measured — `t-cm-figure-4` etc. are DEFINED only in `knowledge/canon/type.css`;
canon.css contains no `@import` (grep: 0). Linking canon.css alone would leave every type
composite unresolved.

**A3 — Page background = grey.**
Rests on: `role_defaults_219.py --table` → `dashboard mono … pageBg=grey` (s219-D1(3)).
⚠ GAP (see G1): there is no semantic page-grey role in the store.

**A4 — Page header is `Page-header-lockup` arrangement A (eyebrow + title + right actions),
not an invented header.**
Rests on: `knowledge/snippets/Page-header-lockup.reference.html` tier A markup.

## B. The wall structure

**B1 — One outer wall, `.c-bento[data-bento-role="dashboard"]`, whose tiles are themselves
bentos (a bento-of-bentos).**
Rests on: s217-D3 — "DASHBOARD (sectioned app, bento-of-bentos): the theme radius sits on
each inner bento's CONTAINER (the s217-D2 model), tiles inside at 1px spacing"; and
canon.css `.c-bento[data-bento-role="dashboard"]:has(> .c-bento__grid > .c-bento)` — "a
dashboard whose tiles are themselves bentos IS the outer wall".

**B2 — Outer wall gutter 40px (mainSpacing), inner wall gutters 4px (subSpacing).**
Rests on: s219-D1(5) — "the dashboard grammar carries the two-dial spacing split
mainSpacing/subSpacing per the exports (main 24/40/40/24, sub 4/4/4/2 in
legacy/mono/console/supercharge order)" — Mono = main 40 / sub 4; confirmed by
`role_defaults_219.py --table` (`dashboard mono mainSpacing=40 · subSpacing=4`).
Both values are on the ruled stop set {1,2,4,16,24,40} (`_bento_edit_rails.json` →
`rail.spacing_stops`, s219-D1(4)).

**B3 — Instance dials written as `.c-bento.wall-x{…}`, never as a bare class.**
Rests on: canon.css ROLES comment — "SPECIFICITY: these rules are (0,2,0). A per-instance
dial written as a bare class is (0,1,0) and the role would beat it — declare instance dials
as `.c-bento.my-wall{…}`."

**B4 — Keylines OFF, tile grounds come from the CARD COMPONENT inside each tile, not from
the tile.**
Rests on: `role_defaults_219.py --table` → `keylines=off · bentoBg=transparent`; and
canon.css gives `.c-bento__tile` no background at all. So a tile is a SLOT and the surface
is the component's (`.cn-card-header-lockup .card{background:var(--surface)}`,
`.cn-kpi-tile .kpi-tile`). This is the grammar, not a workaround.

**B5 — Outer wall: 6 columns, dense packing, 320px row unit — all defaults, untouched.**
Rests on: s217-D2 — "ALL other parameters shared across the four themes — 6 columns, outer
padding 0, row unit 320px, dense packing on … responsive bands 1100px→3 / 820px→2 /
520px→1". Mono/supercharge gutter 0px is the BASE value that B2's instance dial overrides.

## C. Hierarchy — what the operator sees first

**C1 — Reading order: (1) attention strip, (2) headline metric row, (3) the dominant
evidence tile, (4) the decision panel, (5) the three evidence tiles.**
Rests on: DP-01 ("a dashboard's first level shows what is read every visit; everything else
is one deliberate step away") + DP-24 ("size and position carry importance").

**C2 — An ATTENTION STRIP above the wall whose chips anchor-link to the needs-attention
panel.**
Rests on: s251-D1, Dave verbatim — "the thing is I like the strip, its very important, this
is a good pattern, but it need the coordinate with the needs attention pattern. So the user
sees the strip and it orientates them to pay attention towards the detail" / "the user might
even click on teh chip and it anchor links to the needs attention panel". Built exactly
that way: `<a href="#needs-attention">` on each chip.
Chips are `Status-indicator`'s `.chip` (tint chip, "square, fully AA").

**C3 — Headline row = 5 metrics in ONE row, not a 2×2 board.**
Rests on: DP-06 ("headline metrics sit in one row across the top of the wall … a 2×2 board
is a choice for two metrics, not a default for four") + DP-07 ("between three and six
metrics") + s249-D2, Dave verbatim: "The headline row should simply be whatever the data
dictates, 5 is even okay in this case".

**C4 — The headline wall is given `--bento-columns:5` so five tiles fill it exactly.**
Rests on: s249-D5, Dave verbatim — "No ragged layouts" — five tiles in a 6-column grid
leaves an orphan cell; and `knowledge/tokens/layout.json` → `bento.columns.$note`:
"Per-instance overridable via `--bento-columns` (that is how a nested bento carries its own
parameter set)". The per-instance override is sanctioned by the token itself.

**C5 — Metric order, left to right: Programmes in flight · Spend against budget ·
Efficiency gains realised · Risk & compliance exceptions · Decisions awaiting you.**
Rests on: DP-07 — "the first is the one the role checks first, and order runs left to right
by how often it is read, not by size of number". Designer's call on WHICH is first: for an
operator (not a platform owner) the portfolio count is the daily glance. The brief's own
clause order is followed thereafter.

**C6 — Each headline metric carries value + signed delta against a NAMED period + a
sparkline.**
Rests on: DP-08 — "value, signed delta against a named period, and a trend shape; the shape
is a sparkline (length and position), never a gauge or ring." Built with `Kpi-tile`'s own
`.kpi-spark` / `svg.spark-inline` markup, points authored as the snippet authors them.

**C7 — ONE dominant tile: the programme portfolio table, `data-c="4" data-r="2"`. No other
tile is 4 wide.**
Rests on: DP-14 — "One tile per wall is dominant — the widest span, holding the evidence the
role came for — and no other tile matches its width."
Designer's call on WHICH: the portfolio table is the only element that answers three of the
brief's five clauses at once (programmes in flight, spend against budget, gains realised).

**C8 — Row 2 splits 4 + 2, deliberately unevenly.**
Rests on: DP-15 — "Widths are importance-weighted from the ruled span set — 6 · 4 · 3 · 2
… and a row below the lead row does not split evenly when it holds two tiles."

**C9 — Row 3 holds THREE tiles at 2 + 2 + 2.** (SUPERSEDED by C14 after the first render.)
Rests on: DP-15's even-split clause is scoped to a row "when it holds two tiles"; three
equal tiles are not caught by it, and 2+2+2 = 6 closes the row with no orphan cell (DP-16:
"the wall closes with no orphan cell"; s249-D5 "No ragged layouts").

**C10 — The needs-attention panel is a STANDING region, `data-c="2" data-r="2"`, with the
item's one primary action in place.**
Rests on: DP-10 ("an overview carries a standing 'needs attention' region: items the role
must act on, each with its status, its due, and its count against the total") + DP-11
("each attention item offers its one primary action in place … at most six actions").
Four items shipped, count stated as "4 of 11 open items".

**C11 — s247-D3's question answered: the status tiles are NOT hidden in the other cards.**
Rests on: s247-D3, Dave verbatim — "I certain that if they are the only statuses displays
they shouldn't be hidden in the other cards, that assuming they are teh most important
things the user should notice." The exception statuses appear (a) in the strip, (b) as a
headline metric, (c) as their own tile — never only inside the portfolio table.

**C12 — Stats are laid out as a ROW, not a grid.**
Rests on: s247-D4, Dave verbatim — "6 is better in this instant, but the better question is
row or grid, row for sure, teh stats look terrible in t eh grid layout and they waste so
much space when its not needed".

## D. Signal and colour

**D1 — The page is mostly UNHUED. Hue is spent only on the two things that are wrong.**
Rests on: DP-19 ("the dark-cockpit default: a dashboard with nothing wrong shows no hue …
Sky and foliage are unlit") + DP-27 ("Quiet is a designed state … no green tick and no
celebratory colour"). The three healthy metrics carry a `flat`/neutral delta with no ink
colour; only the exception count and the overdue decision carry red/amber.

**D2 — No green on the "efficiency gains realised" metric even though it is up.**
Rests on: DP-19 + s249-D3, Dave verbatim — "I think you are suggesting the green is
overwhelming and hiding the important signal which would be amber and red. is this right."

**D3 — Polarity is declared per metric, not inferred from the arrow.**
Rests on: DP-22 — "Colour follows meaning, not arithmetic: every metric declares which
direction is good … A falling cost, exposure or overdue count is fruit, not blood."
Exceptions RISING is blood (`.kpi-delta up` but negative polarity), so the canon
`up`/`down` classes are NOT used as the colour carrier there.
⚠ See G2 — canon has no polarity attribute; this had to be done by tile choice.

**D4 — Status is carried by dot + label, never hue alone.**
Rests on: `Status-indicator`'s own markup (`data-carries="label"`, `.dot` + text) and
DP-21 ("one channel per tier"). Also the standing in-house reason: Dave is astigmatic and
red is a problem hue (canon.css finding at the Sidebar-nav indicator).

**D5 — No entry motion, no load choreography.**
Rests on: DP-23 — "Motion is the rarest signal … never spent on load or entry
choreography on a monitoring page." The `dv-animate` class the chart snippets ship with is
therefore NOT used on this page.

## E. Charts

**E1 — Charts are driven by `window.dvRender(figureEl, spec)`, not hand-authored geometry.**
Rests on: `knowledge/canon/dv-render.js` header — "It REPLACES rule 18 of
`ADS-generate-from-canon` (the interim 'author the geometry yourself' recipe): the library
owns the arithmetic, the author owns the data."

**E2 — Spend against budget is a COLUMN chart, not a gauge or ring.**
Rests on: DP-08 ("never a gauge or ring") + NN/g rationale quoted there (length and 2D
position are preattentive, area and angle are not).

**E3 — Efficiency gains realised is a LINE chart (a run over months), spend is a COLUMN
chart (categorical by programme).**
Designer's call, inside the canon type registry (`dv-render-line.js`, `dv-render-bar.js`).

**E4 — Each chart ships a real `<table class="dv-table">` spine.**
Rests on: dv-render.js — "the `<table>` spine is not optional … JS off ⇒ the table is the
answer" (dv-005). The engine rewrites it; the markup ships one anyway.

**E5 — The exceptions tile is a TABLE, not a chart.**
Rests on: DP-08's shape rule is for headline metrics; seven exceptions with owner, age and
severity is a list of facts, not a distribution. Designer's call.

## F. Reveal / filters

**F1 — The filter bar ships COLLAPSED, as a chip row with a count and a clear-all.**
Rests on: DP-02 ("filter controls on an overview are dismissible and ship in the state the
designer decided; the collapsed form is the default unless the brief says otherwise") +
DP-03 ("a collapsed filter shows its count and its applied values as dismissible chips; a
clear-all sits beside them when two or more are applied"). Built from `Tags`' own
`.filterbar` / dismissible `.tag` + `.x` markup.

**F2 — The filter sits WITH the wall it filters, not in the page title zone.**
Rests on: DP-28 — "the action lives on the wrong surface. Both pages put a filter toolbar
in the page's title zone that acts on nothing there".

**F3 — Each chart tile carries "View as table" in its own header, in place.**
Rests on: DP-04 — "Detail is revealed in place where it answers the tile's own question
(expand, view-as-table, popover)".

## G. GAPS — what the system could not supply (flagged, not invented)

**G1 — `pageBg=grey` has no semantic token.** The dashboard/mono role default says the page
ground is grey (s219-D1(3), `role_defaults_219.py --table`), but the alias block in
canon.css offers only `--page: var(--background-default)` (#FFFFFF) and
`--surface-hover: var(--tertiary-background-hover)` (#F3F3F3). Bound to
`--tertiary-background-hover` as the nearest intent and flagged here. The system wants a
`background/secondary` (or `background/app-canvas`) role.

**G2 — No polarity attribute on Kpi-tile.** DP-22 requires every metric to declare which
direction is good, but `Kpi-tile`'s carrier is `data-trend="up|down|flat"` — arithmetic, not
meaning. DP-25 proposes `data-signal`, and it is one of the OPEN questions (Q8–Q16) at
s246, not ruled. Composed against the canon that exists (`data-trend`), with the polarity
expressed only in the copy ("+3 open, worse than last week").

**G3 — The 320px row unit fights DP-06.** `layout.bento.row-unit = 320px` is "MINTED s217-D2
— shared" with NO per-instance clause in its `$note` (unlike `columns`), and nested bentos
floor at `minmax(var(--bento-row-unit),auto)`. So the headline metric row cannot be made
compact, and DP-06's stated purpose — "compact, so the first chart starts above the fold" —
is unreachable at 1440 without an authoring act. NOT overridden; flagged.

**G4 — No "needs attention" component.** DP-10 requires a standing attention region and
there is no `Needs-attention` or `Attention-list` snippet; the closest canon pieces are
`List-items`, `Status-indicator` and `Button`. Composed from those three inside a
`Card-header-lockup` card rather than inventing a component — but the system is missing the
organism DP-10 names.

**G5 — No dashboard shell.** The `App-shell-*` snippets exist, but a dashboard whose page
chrome is a header lock-up + a bento wall has no shell that says so. Left as a plain page
container; a shell was not invented.

**G6 — No attention-strip component.** s251-D1 rules the strip as "a good pattern" and it
has no snippet; built from `Status-indicator` chips wrapped in a landmark, and flagged.

---

## H. Decisions forced by what the RENDER measured (taken after the first render, same method)

**C13 — A group of ONE is a plain tile, not a nested bento.**
Rests on: measured, this lane. A nested bento narrower than 1100px trips canon's compiled
band `@container bento (max-width:1100px){ .c-bento__grid{--bento-cols-now:3} }`, which
re-declares the column count on the GRID and so overrides the instance's own
`--bento-columns`. The dominant tile's wall (896px) and the decision panel's wall (448px)
both silently became 3-column. Both are now plain `.c-bento__tile`s. See G8.

**C14 — Row 3 is a 3-column wall two rows deep, with the exceptions list in its own
full-height column and the two charts stacked beside it.**
Rests on: DP-18 — "A tile is sized to its content's floor and never stretched to a
neighbour's height; a taller neighbour is answered by a second tile in the column, not by
empty ground." Measured first: the exceptions list (694px) stretched the charts' row to
791px inside a wall canon fixes at 320px, and `.c-bento{overflow:hidden}` clipped it
silently. Giving the list its own `data-r="2"` column answers the taller neighbour the way
DP-18 says to.

**C15 — The chart canvas is pinned to the 320px rung (`max-height` on `.dv-chart-area`).**
Rests on: `dv-behaviour.js` fitHeight's own comment — "the box must FOLLOW the viewBox
(height:auto released) … a CSS-pinned box would SCALE: keep the bake". Without the pin the
chart fills whatever slack `slackBelow()` finds and the fill feeds back into the row height.

**C16 — `List-items`' own `--row-h`/`--row-pad` density dials are set to 64px/10px.**
Rests on: those are the values `List-items`' own density control ships (measured in the
snippet source). A component dial, not an invented value.

**C17 — A Legend (DV-D11 markup) names the A/B keys the chart engine bakes.**
Rests on: measured — `dvRender` labels grouped series `A`/`B` on the marks and nothing on
the page said what A and B were. The `Legend` snippet's `.dv-leg`/`.dv-legrow` markup is
used verbatim, statically (progressive enhancement: the baked markup reads with JS off).

## G (continued) — GAPS found by measuring, not by reading

**G7 — canon's documented instance-dial recipe is under-specified.** canon.css tells the
author: "declare instance dials as `.c-bento.my-wall{…}`" because the role rules "are
(0,2,0)". But the rule that restores the outer gutter for a bento-of-bentos is
`.c-bento[data-bento-role="dashboard"]:has(> .c-bento__grid > .c-bento)`, whose `:has()`
argument lifts it to (0,4,0). MEASURED: `.c-bento.wall-ops{--bento-gutter:40px}` had NO
effect — the wall rendered at 0px gutter, i.e. the Mono base value, not the ruled
mainSpacing of 40. The dial only lands when it repeats the `:has()`. So the one ruled
dashboard dial (s219-D1(5)) cannot be set the way canon documents.

**G8 — a nested bento cannot carry its own column count below 1100px.** `layout.json`
says columns are "Per-instance overridable via `--bento-columns` (that is how a nested bento
carries its own parameter set)", and s217-D2 makes nesting canon behaviour. But the
compiled bands re-declare `--bento-cols-now` on `.c-bento__grid` at ≤1100 / ≤820 / ≤520,
and the bands answer the WALL, not the window. MEASURED: a 1-column inner wall 896px wide
rendered as 3 columns. Any inner wall of a 1440-wide dashboard is below 1100 unless it
spans the full six columns — so the per-instance column dial is only reachable for
full-width inner walls.

**G9 — no gate in the tree reads the composition of a page that LINKS canon.css.**
`_validate_composition.py` reads "column counts and band clamps from its own @container
blocks" — i.e. the artefact must restate the grammar inline. Verdict on this page,
verbatim: `UNPROVEN: the artefact declares neither a base column count nor any @container
band; C9 cannot read its grammar`. The orphan-cell arithmetic that DP-16 and s249-D5 rest
on therefore cannot be checked on a linked page at all.

**G10 — `_validate_compose.py` ignores a path argument.** It scans a fixed set of
`*.canon.html` screens; passing this page's path produced a `RESULT: PASS ✅` about seven
OTHER screens. Its pass is not evidence about this page. (`_validate_screen.py` DOES take a
path and did gate this page.)
