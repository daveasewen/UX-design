# s227 · Dashboard regen diff — what the pipeline should have done

**COUNTS: findings 25 · generation-defects 3 · canon-gaps 14 · dave-improvements 8 · UNPROVEN 4**

Sub: Opus build sub, session #227. Conductor: Fable seat.
Artefacts produced (the only three files created):

- `dashboards/international-banking-dashboard.regen-v1.html` (45,621 bytes)
- `reviews/DASHBOARD-REGEN-COMPARE-2026-08-30-v1.html`
- this report

⛔ No rulings. Everything ruling-shaped below is a **question for Dave**, marked `Q:`.

---

## 0. Method, and the one premise correction

**Order of work, so the diff measures something.** Dave's file was read ONCE for its body
structure (markup + content only). The intent spec in §1 was written from that reading. His
`<head>` — the harness CSS, the `data-apollo-theme` attribute, every style decision — was
**not opened until §3**, after the regen was finished and gated. The regen was built only from
the spec, `apollo-spider/skills/generate-from-canon/SKILL.md`, `showroom/index.json`, the
`knowledge/components/*.meta.json` contracts, the `knowledge/snippets/*.reference.html` markup
and `knowledge/_render/_bento_edit_rails.json`.

**Premise correction, measured.** The brief says his file "carries ONE border-radius declaration
total." It carries **two**, and they are a pair:

```
.cn-chart-line .dv-toggle-seg{border-radius:var(--border-radius-segmented-container-xs);overflow:hidden}
.cn-chart-line .dv-toggle-seg .ind{border-radius:var(--border-radius-segmented-thumb-xs)}
```

That does not weaken the symptom — it sharpens it. Both declarations exist to repair **one**
canon omission (B6), and the fact that a hand-polished page needed exactly two radius patches and
no others is the finding, not the count.

**The theme, which turns out to be the hinge.** His `<html>` carries
`data-apollo-theme="console"`. The regen shipped **mono**, because SKILL.md rule 5 calls mono
"the baseline" and nothing in the Procedure ever asks. In mono every radius token resolves to `0`:

```
canon.css:542-554   --border-radius-default: 0;  --border-radius-control: …default;
                    --border-radius-surface: …default;  --border-radius-container: …default;
                    --border-radius-segmented-{container,thumb}-{xs,s,m,l}: 0;
```

So a mono build **cannot see** any of the radius defects below. They only become visible in
console (A2).

---

## 1. The intent spec (written before re-opening his file)

WHAT, never HOW. No styles, radii, spacing or colours.

**Page identity.** A corporate international-banking treasury dashboard. Single page,
self-contained, light + dark with a user-facing theme switch. Fictional HSBC brand mark.

**Sections, in order**

1. **Global navigation (masthead)** — brand logo linking to page top; primary nav of 4
   (Overview *(current)* / Payments / Liquidity / Trade); an actions cluster with a search
   trigger and an account-menu trigger; the account menu holds "Switch to dark theme" and
   "Secure session"; a search bar revealed by the search trigger, placeholdered
   "Search international payments", whose value is mirrored with the in-page payments search
   (one query, two entry points).
2. **Page header lockup** — eyebrow "Corporate international banking"; h1 "Global treasury
   overview"; meta "Consolidated position · 28 August 2026 · GBP equivalent"; one tertiary
   action "Export CSV", exporting the currently filtered rows.
3. **Stats band, 4 tiles** — label / big figure / delta:

   | label | figure | delta | trend |
   |---|---|---|---|
   | Available cash | £18,420,000 | +4.8% up · vs July | up |
   | Payments in flight | £2,760,000 | 18 payments · across 7 markets | none |
   | Net FX exposure | £642k | −8.1% · vs July | down |
   | Approvals | 6 | £1.24m · oldest 42 min | none |

   Layout intent: the two money tiles wider than the two count tiles (2 / 2 / 1 / 1 of six
   columns), one row.
4. **Liquidity + snapshot band, 2 tiles** —
   (a) a **line chart** (4 cols × 2 rows), "Six-month net cash flow", with a Monthly /
   Year-to-date view switch, independent "Target line" and "Last year" toggles, a
   "Copy data (CSV)" action and a "View as table" disclosure carrying the full table.
   Data (£m): Mar 1.4 · Apr 1.7 · May 2.1 · Jun 1.9 · Jul 2.5 · Aug 3.1. Last year:
   1.2 · 1.4 · 1.8 · 1.6 · 2.2 · 2.7. Year to date: 1.4 · 3.1 · 5.2 · 7.1 · 9.6 · 12.7.
   Target £2m a month.
   (b) a **treasury snapshot** (2 cols × 2 rows) — heading over a key/value list: Operating
   countries 14 · Active currencies 9 · Largest exposure USD £4.82m · Next funding cut-off
   Singapore · 48 min · Facilities available £12.6m.
5. **Payment activity band, one full-width tile (6 × 3)** — h2 + a live result count; a filter
   toolbar of search + Market dropdown + Currency dropdown + a direction segmented control
   (All / Credits / Debits) + a removable-chip row; a list of payment rows (initials avatar,
   counterparty, status pill, "date · market · reference", signed amount in the row's own
   currency); an empty state with a "Clear filters" action; a foot with a range readout and
   pagination. Page size 6.
6. **Data** — the 12 payments, verbatim, with the status→tone mapping
   Completed=success · Awaiting approval=warning · On hold=error · Processing=info.

**Behaviour intent.** Filter + search + direction narrow the list; chips reflect and remove
active filters; pagination follows the result count; every change announces to a polite live
region; CSV export of the filtered set; theme toggle flips light/dark.

**Component shopping list** (canon names, resolved via `showroom/index.json` in §2):
masthead · nav search bar · page header lockup · button (tertiary) · bento (dashboard role) ·
stat card · line chart · summary list · filter toolbar · search input · dropdown · segmented
control · filter chips · list items · status pill · avatar · pagination · empty state ·
live region.

---

## 2. The by-the-book build, and where the book ran out

Discovery searched `showroom/index.json` (143 entries) by alias and blurb. Every component
resolved except the bento. Contracts read from `knowledge/components/<slug>.meta.json`; markup
**copied** from `knowledge/snippets/<Slug>.reference.html` (case-insensitive glob, per the
skill's own filename warning); layout dials read from `knowledge/_render/_bento_edit_rails.json`.

Used, and what was copied from where:

| component | snippet copied | scope class |
|---|---|---|
| navigations | `Navigations.reference.html` | `.cn-navigations` |
| page-header-lockup | `Page-header-lockup.reference.html` | `.cn-page-header-lockup` |
| button (tertiary) | `Button.reference.html` | inside the lockup |
| foundation-bento | **no snippet exists** — assembled from `canon.css` (B1) | `.c-bento` |
| stat-card | `Stat-card.reference.html` | `.cn-stat-card` |
| chart-line | `Chart-line.reference.html` | `.cn-chart-line` |
| summary | `Summary.reference.html` | `.cn-summary` |
| filter-toolbar-bar | `Filter-toolbar-bar.reference.html` | `.cn-filter-toolbar-bar` |
| list-items | `List-items.reference.html` | `.cn-list-items` |
| pagination | `Pagination.reference.html` | `.cn-pagination` |
| empty-state | `Empty-state.reference.html` | `.cn-empty-state` |

Layout dials shipped as the rails' minted mono/dashboard defaults:
`mainSpacing 40 · subSpacing 4 · keylines off · pageBg grey · bentoBg transparent`
(`_bento_edit_rails.json` → `defaults.values.dashboard.mono`).

**The chart geometry is the one thing the pipeline gets completely right.** Re-derived
independently from `Chart-line.reference.html`'s own canvas grammar (`viewBox 0 0 580 260`,
`data-pl=46`, `data-pr=12`, baseline `y=230`, top `y=14`), the regen's series points came out
**byte-identical** to Dave's: `46,154.4 150.4,138.2 254.8,116.6 359.2,127.4 463.6,95 568,62.6`.
Whatever "a bit of work" meant, it was not the chart.

**The gate verdict, as it actually printed.** SKILL.md step 5, `knowledge/_validate_screen.py`:

```
## international-banking-dashboard.regen-v1.html
- compose: ✅
- icon-source: ✅ all paths library-matched
- a11y: ✅  (warn: DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum … ×12)
RESULT: PASS ✅

## international-banking-dashboard.canon.html
- compose: ✅
- icon-source: ✅ all paths library-matched
- a11y: ✅  (warn: DATA MARK `g.dv-marker` … ×12)
RESULT: PASS ✅
```

Same verdict, same warning, same count, on a hand-polished 38.8KB page and an unstyled 45.6KB
one. **The gate cannot see the difference.** (B12.)

---

## 3. The diff

### (a) GENERATION DEFECTS — canon has it, the by-the-book flow lost it

---

**A1 · The segmented control loses its radius binding, because the reference markup omits the
wrapper that carries it.**

Canon **has** the binding:

```
canon.css:14307  :where(.cn-segmented-control) .seg{--seg-rad:var(--seg-rad-s); …
                   border-radius:var(--seg-rad); …}
canon.css:14309  :where(.cn-segmented-control) .seg .ind{… border-radius:var(--seg-thumb); …}
```

But both consumers re-declare `.seg` in their own scope **without** a radius, and both sit
EARLIER in the file, so whichever rule is last wins:

```
canon.css:8897   :where(.cn-chart-line) .seg{position:relative; display:inline-flex;
                   height:var(--control-h); box-sizing:border-box; padding:2px;
                   border:1px solid var(--line); background:transparent; vertical-align:top;}
canon.css:11424  :where(.cn-filter-toolbar-bar) .seg{position:relative; display:inline-flex;
                   padding:2px; border:1px solid var(--border); background:var(--surface);
                   vertical-align:top;}
```

Neither carries `border-radius`. And the reference markup a generator is told to copy has no
`.cn-segmented-control` wrapper:

- `Filter-toolbar-bar.reference.html` → `<div class="ftb-view"><div class="seg md" role="group" aria-label="View as">`
- `Chart-line.reference.html` → `<div class="seg sm" role="group" aria-label="Chart view — one of two scales">`

So the regen's two segmented controls are square in every theme. Dave's are not — he wrapped
both: `<div class="cn-segmented-control"><div class="seg sm">`. Because `:where()` contributes
zero specificity, all three `.seg` rules sit at (0,1,0) and the `.cn-segmented-control` block at
line 14307 wins on source order alone. **His double-wrap is load-bearing, and nothing in the
skill, the meta or the reference tells you to do it.**

`Q:` should the consumer scopes stop re-declaring `.seg` at all, or should the two references
carry the wrapper?

---

**A2 · The Procedure never asks which theme the screen is for, and mono hides every radius
decision.**

SKILL.md rule 5 says "Pick a theme and say which" and names mono "the baseline". The Procedure
(steps 1–5) never asks. No discovery artefact — `showroom/index.json`, any meta, the rails —
records a project default. The regen therefore shipped mono. Consequence, measured:

| token | mono | console |
|---|---|---|
| `--border-radius-control` | `0` | `8px` |
| `--border-radius-surface` | `0` | `20px` |
| `--border-radius-container` | `0` | `20px` |
| `--border-radius-segmented-container-xs` | `0` | `6px` |
| `--border-radius-segmented-thumb-xs` | `0` | `0` |

(`canon.css:542-554` for mono; `canon.css:22160-22175` for `[data-apollo-theme="console"]`.)

Every finding in B5, B6, B7 and A1 is **invisible** in a mono build. The pipeline can produce a
radius-blind page and pass its own gate without ever surfacing the question. This is the reason
Dave's session "took a bit of work" and a mono regen looks fine: he was working in the one theme
where the omissions show.

`Q:` should the theme be a required opening question in the Procedure, and should there be a
per-project default recorded somewhere a generator reads?

---

**A3 · The reviewed references contain inline styles and raw px, so copying them faithfully
breaks SKILL rule 3.**

`Filter-toolbar-bar.reference.html` carries five inline `style=` attributes, two of which are in
the markup a generator must copy:

```
style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);"   ×2  (the sr-only labels)
style="display:flex; flex-wrap:wrap;"                                                     (.ftb-chips .row)
```

Rule 3 says "never a raw hex or px … Spacing, radius and border width are tokens too". Rule 2
says copy the snippet. The two rules contradict each other on this file. The regen carried the
inline styles (faithful copy); Dave replaced them with a `.dashboard-live` harness class.
Canon has no `.sr-only` / visually-hidden utility of its own — `grep '^\.c-' canon.css` returns
`.c-actionbar .c-amount-in .c-amount-out .c-bento .c-choice-group .c-choice-row .c-eyebrow
.c-fill .c-grid .c-grid-auto .c-pad .c-row .c-row-between .c-screen .c-stack .c-stat-cell
.c-stat-grid .c-summary .c-tabbar` and nothing else.

`Q:` add a `.c-sr-only` utility and clean the two references?

---

### (b) CANON GAPS — the system genuinely lacks it

---

**B1 · There is no snippet and no meta for the bento — the one thing the whole page is built
out of.**

```
ls knowledge/snippets/ | grep -ci bento          → 0
ls knowledge/components/ | grep -ci foundation   → 0
```

`showroom/index.json` lists `foundation-bento`, `foundation-bento-rails` and
`foundation-grids-dashboard` as `level: foundation, status: beta`, each pointing at a
`showroom/_foundations/*.html` page. SKILL.md rule 2 — "Copy the snippet, don't re-draw it" — is
**unsatisfiable** for the bento. The regen's bento markup had to be assembled by reading
`canon.css` source (`.c-bento`, `.c-bento__grid`, `.c-bento__tile[data-c][data-r]`), which is
exactly the "hand-rolling invents defects" the rule exists to prevent.

**This directly answers the brief's question: no, a bento dashboard-role exemplar you can copy
does not exist.** The prior finding holds and is now measured at the file level, not just the
rendered one.

---

**B2 · A dashboard-role bento TILE has no surface anywhere in canon.**

```
grep -c 'bm-tile\|bm-card\|bm-wall\|bm-inner' knowledge/canon/canon.css   → 0
```

The only rendered dashboard exemplar is `showroom/_foundations/grids-dashboard.html`, which
paints its tiles with **page-local** CSS:

```
showroom/_foundations/grids-dashboard.html:487
.bm-panel,.bm-card{padding:var(--sp-4,16px); gap:var(--sp-2,8px); justify-content:flex-end;}
```

`.bm-card`, `.bm-tile`, `.bm-wall`, `.bm-inner` exist in that one showroom page and nowhere in
canon. Canon's role block is explicit that this is deliberate:

```
canon.css:1166  .c-bento[data-bento-role="dashboard"]{
                  --bento-radius:var(--border-radius-container);
                  --bento-gutter:1px;
                  overflow:hidden; }
```

Radius on the container, 1px gutter, tiles square — a model that only reads if the tiles have a
ground and the gutter shows as a hairline between them. Canon supplies the gutter and withholds
the ground. Dave supplied it:

```
.dashboard-tile{padding:24px;background:var(--surface-raised);min-width:0;overflow:visible}
```

The regen has no tile surface at all. This is the single biggest visual difference between the
two files and it is not taste — it is an absent declaration.

---

**B3 · Dashboard rows are a fixed 320px and the rails expose no dial for it.**

```
canon.css:539   --layout-bento-row-unit: 320px;
canon.css:1092  grid-auto-rows:var(--bento-row-unit);   /* "⚠ FIXED rows" */
```

`_bento_edit_rails.json → types.dashboard.dials` = `["mainSpacing","subSpacing","keylines","bentoBg"]`.
No row unit. So a by-the-book stat band is **320px tall per row** and the regen ships it that
way. Dave overrode both:

```
.c-bento.dashboard-bento{… --bento-row-unit:minmax(148px,auto) …}
.c-bento.dashboard-stats-bento{--bento-row-unit:auto}
```

⚠ Canon's own comment at `canon.css:1090-1092` warns that intrinsic rows kill the span
vocabulary ("MEASURED #217, Foundations photography bento"), so this is **not** a silent flip.
`Q:` a `rowUnit` dial on the stops rail, or a different default for the dashboard role?

---

**B4 · The rails' dial names bind to nothing, and one of them contradicts canon.css.**

```
grep -c 'mainSpacing\|subSpacing\|bentoBg\|keylines' knowledge/canon/canon.css   → 0
```

`_bento_edit_rails.json` says `$permission_levels.generation`: *"ships the minted defaults only —
zero decisions up front, every generated instance lands on canon."* There is no class, attribute
or custom property in canon that a generator can write to ship them. SKILL rule 7 sends you to
"one file" for every layout dial; that file names dials the stylesheet has never heard of.

And they disagree. The mono dashboard default is `subSpacing: "4"`; `canon.css:1181` hardcodes
`--bento-gutter:1px` for the role. Dave used a third number, `2px`. Three sources, three values,
for one gap. `Q:` which is it?

---

**B5 · The search field binds no radius — in a toolbar where its two neighbours do.**

```
grep -c '\.search[^ ]*{[^}]*border-radius' knowledge/canon/canon.css   → 0
```

```
canon.css:3159   :where(.cn-search-field) .search.boxed{border:1px solid var(--border); padding:0 8px;}
canon.css:11382  :where(.cn-filter-toolbar-bar) .search.boxed{border:1px solid var(--border); padding:0 8px;}
```

No `border-radius` on `.search` in either scope, nor on the base `.search` rule. Meanwhile,
inside the **same** `.cn-filter-toolbar-bar` block:

```
canon.css:11397  … .dd .trigger{… border-radius:var(--border-radius-control); …}
canon.css:11439  … .tag{… border:1px solid var(--border); border-radius:var(--border-radius-control); …}
```

In console that is an 8px-rounded dropdown and 8px-rounded chips sitting beside a square search
box, on one row. **This is Dave's "search input squareness", and it is canon's, not the
generator's** — the pipeline reproduced it faithfully. Neither file fixes it; his page has it too.

---

**B6 · The chart toolbar has three bordered boxes with no radius; Dave patched one pair and the
other two are still square in his own file.**

```
canon.css:8865  :where(.cn-chart-line) .dv-tbl-toggle, :where(.cn-chart-line) .dv-vt{
                  position:relative; height:var(--control-h); box-sizing:border-box;
                  display:inline-flex; align-items:center; background:transparent;
                  border:1px solid var(--line); color:var(--ink); padding:0 8px; cursor:pointer;
                  flex:none; transition:border-color var(--ease);}
canon.css:8885  :where(.cn-chart-line) .dv-toggle-seg{position:relative; display:inline-flex;
                  height:var(--control-h); box-sizing:border-box; …}
```

None of `.dv-tbl-toggle`, `.dv-vt`, `.dv-toggle-seg` binds a radius. Dave's **two** border-radius
declarations repair `.dv-toggle-seg` and its `.ind` only. So in his console page, the chart
toolbar reads left-to-right as: rounded segmented switch (6px, via his `.cn-segmented-control`
wrapper) → rounded "Target line" (his patch) → rounded "Last year" (his patch) → **square**
"Copy data (CSV)" → **square** "View as table". A residual he did not catch. Same pattern lives
in `.cn-chart-combo` (`canon.css:8297`) and by inspection in chart-bar / chart-donut / chart-pie.

---

**B7 · The segmented-control's contract and its implementation disagree, and the live size
mapping declares itself PROPOSED, not ruled.**

`knowledge/components/segmented-control.meta.json` → `variants`:

```
label-square-md  (Default)  ·  sm  ·  lg  ·  icons
```

The **ruled** `xs / s / m / l` scale — minted heights 24 / 36 / 44 / 48, with its own
`--border-radius-segmented-{container,thumb}-{xs,s,m,l}` tokens — appears nowhere in the meta.
It is implemented in `canon.css:14330-14342` and in the reference. A generator reading the
contract, as SKILL step 2 instructs, picks from the **legacy** family and never learns the ruled
one exists. The regen used `.seg sm` and `.seg md`; so did Dave.

canon.css then says, in its own words:

```
canon.css:14345  ⚠ ORDINAL map (sm→xs · md→s · lg→m), PROPOSED not ruled — the nearest-HEIGHT
                 reading collapses md and lg onto the same scale (32→36 and 36→36), which is why
                 it was not taken silently. Both readings are drawn in
                 reviews/SEGMENTED-ADOPTION-2026-08-25-v1.html for Dave to point at.
canon.css:14351  :where(.cn-segmented-control) .seg.sm{--seg-rad:var(--seg-rad-xs); --seg-thumb:var(--seg-thumb-xs);}
canon.css:14352  :where(.cn-segmented-control) .seg.md{--seg-rad:var(--seg-rad-s);  --seg-thumb:var(--seg-thumb-s);}
```

**Dave's suspicion that "the -xs members are wrong" is measurable, and it is this.** In console:

| class | container radius | thumb radius |
|---|---|---|
| `.seg.sm` → xs | **6px** | **0px** |
| `.seg.md` → s | 8px | 2px |
| `.seg.lg` → m | 10px | 4px |

`.seg.sm` is the only step in the ladder whose thumb is square inside a rounded track — because
`--border-radius-segmented-thumb-xs` is `0` in console while its container is `6px`. The chart's
view switch is a `.seg.sm`. That is the pair he is looking at.

This is **not a generation defect and not something to fix here** — `reviews/SEGMENTED-ADOPTION-2026-08-25-v1.html`
exists and is waiting for his eye. `Q:` is the xs thumb `0` correct (a square thumb is the
intent), or should the ordinal map move `.seg.sm` onto `s`?

---

**B8 · The masthead logo slot is a text wordmark; canon has no image composition and no
light/dark mark swap.**

```
canon.css:1756   :where(.cn-navigations) .logo{font-weight:500; font-size:20px;
                   color:var(--logo); letter-spacing:-.01em;}
grep -c '\.logo img' knowledge/canon/canon.css   → 0
```

`Navigations.reference.html` ships `<span class="logo" aria-label="HSBC">HSBC</span>`. The regen
copied it and therefore reads the word "HSBC" in the masthead. The real marks exist —
`knowledge/assets/logos/hexagon-{light,dark}-{colour,mono}.svg` plus the masterbrand set — and
`foundation-logos` is in the index, but nothing composes them into the masthead and canon's only
light/dark mark swap lives inside `.cn-template-auth` (per SKILL.md's own note on `data-mode`).
Dave wrote the composition himself:

```
.cn-navigations .dashboard-logo{display:inline-flex;align-items:center;justify-content:center;width:56px;min-width:56px}
.cn-navigations .dashboard-logo img{display:block;width:42px;height:auto}
```

⚠ And his `<img src="…hexagon-light-colour.svg">` is **pinned to the light mark** — it does not
swap in dark mode. The gap bit him too. This is the brief's "nav/logo composition" item.

---

**B9 · There is no page-width container.**

`.c-screen` (`canon.css:982`) is `width:390px` — a mobile frame. No desktop page container
exists among the `.c-*` utilities. Both files invented one in harness: Dave
`padding:0 24px 24px` on a flex stack, the regen `max-width:1280px; margin-inline:auto`.
`page_rail` in the rails names the page *ground* (`page` / `white` / `grey`) but not the page
*measure*, and binds neither.

---

**B10 · `.c-summary` hardcodes a raw font, in breach of SKILL rule 4, and is invisible to
discovery.**

```
canon.css:999   .c-summary__k{ color:var(--muted); font:400 16px/1.4 var(--font); }
canon.css:1000  .c-summary__v{ color:var(--text); font:500 16px/1.4 var(--font); … }
```

Raw `font-size` / `font-weight` / `line-height`, not a `.t-cm-*` composite — inside canon itself.
Two things are called "summary": the `summary` **component** (`.cn-summary .summary__*`, the one
in `showroom/index.json`, the one the regen used) and this **utility**, which is in no index and
which the compose runbook explicitly recommends ("Use the `.c-*` utilities … `.c-summary`").
Dave used the utility. A generator following the index uses the component; a generator following
the runbook uses the type-unsafe one.

---

**B11 · Nothing says how to get an icon into a self-contained page.**

SKILL rule 8: "Icons are real assets only — from `knowledge/assets/icons/`." 659 SVG files on
disk. Neither the skill nor `_RUNBOOK-compose-from-canon.md` says whether to inline a `<symbol>`
sprite, reference by path, or use `<img>`. Both files independently improvised the same answer
(an inline sprite of `<symbol>`s with `<use href="#…">`), which suggests the convention is real
and simply unwritten.

---

**B12 · The composed-screen gate cannot tell the two files apart.**

`knowledge/_validate_screen.py` returns `PASS ✅` with an identical three-line body and an
identical 12× `dv-marker` warning on both. It checks compose-legality, icon provenance and a11y.
It has no check for: whether a bento tile has a ground, whether a bordered control binds a radius
token, whether a fixed row unit swallows its content, or whether the page renders at all. **A
green gate here is not evidence of a usable screen** — which is the whole reason Dave had to do
the work by hand.

---

**B13 · The runbook and the skill disagree on the theme contract, and the runbook is wrong.**

`knowledge/_RUNBOOK-compose-from-canon.md` § Compose a screen: *"Root element gets
`class="canon"`; theme via `data-theme="light|dark"` on it (or `<body>`)."* SKILL.md step 3 quotes
it as *"That is the whole contract."* But:

```
grep -c 'data-apollo-theme' knowledge/canon/canon.css   → 1187
grep -c 'data-apollo-theme' knowledge/canon/type.css    →    0
```

1,187 rules in canon.css select on `data-apollo-theme`. Mono is the attribute-less default
(`grep -o 'data-apollo-theme="[a-z]*"'` returns console 360 · legacy 413 · supercharge 414 · mono
**0**), so a generator that follows the runbook literally ships mono forever and never discovers
the other three themes exist. SKILL rule 5 gets it right; step 3 then defers to a runbook that
contradicts rule 5.

---

**B14 · Running the skill's own step 5 silently clobbers a tracked report file.**

`knowledge/_validate_screen.py` does not only print — it **rewrites**
`knowledge/_SCREEN-GATE.md` with the results of the current invocation only. Before this
session that file held seven subjects:

```
## canon-gallery.canon.html · nio-dash-console-v1 · nio-dash-console-v2 · payments-journey
## sme-payments-desktop · sme-payments-swiss · sme-payments
```

After two runs it held two — mine. `git diff --stat` read
`knowledge/_SCREEN-GATE.md | 28 ++------------------------` (3 insertions, 26 deletions).
**I restored it** (`git checkout -- knowledge/_SCREEN-GATE.md`; verified back to seven subjects)
and the gate verdicts are quoted verbatim in §2 instead, so nothing is lost.

But this is a real trap: SKILL.md step 5 tells every user of the skill to run this command
("A draft you haven't gated is a claim, not a result"), and doing so destroys the standing record
for every other screen. It is also a write-once / ADR-0017 violation in miniature — one file
holding live facts for seven subjects, rewritten wholesale by any one of them.

`Q:` should the gate append per-subject (or write `knowledge/_screen-gate/<subject>.md`) rather
than replacing the whole file?

⚠ Also declared: `notes/_REHEARSAL-LOG.jsonl` shows one added line (`"kind": "wrap-open"`,
`"date": "2026-08-30"`). That is **not mine** — nothing I ran writes jsonl — but it is in the
working tree, so the conductor should reconcile it rather than assume it is clean.

---

### (c) DAVE IMPROVEMENTS — his polish, priced as back-ports

His whole harness is 29 declarations. Every one of them is either a gap above or plumbing.
Priced by what a back-port actually costs.

| # | his declaration | what it repairs | price |
|---|---|---|---|
| **C1** | `.dashboard-tile{padding:24px;background:var(--surface-raised);min-width:0;overflow:visible}` | B2 — the missing dashboard tile ground | **Medium.** One canon rule (`.c-bento[data-bento-role="dashboard"] > .c-bento__grid > .c-bento__tile`), one rails `tileSurface` dial + its default, and a regression pass over gallery/display roles which deliberately have no tile ground. Changes every existing dashboard bento. |
| **C2** | `--bento-row-unit:minmax(148px,auto)` / `auto` | B3 — 320px fixed rows | **Small in code, heavy in governance.** `canon.css:1090` warns intrinsic rows destroy the span vocabulary. Needs a `rowUnit` dial on the stops rail rather than a silent default change. Dave's eye owed. |
| **C3** | `--bento-gutter:2px` on the wall | B4 — the three-way disagreement (rails 4 · canon 1px · Dave 2px) | **Nil in code.** One number to rule. Cheapest item here and it unblocks the rails/canon reconciliation. |
| **C4** | `.dashboard-stat-tile .stat-card{padding:24px;border:none}` + `.dashboard-tile .cn-list-items ul.list{border:none}` | the double-border: a component that owns a border, inside a tile that now owns a ground | **Medium.** A `flush` / `bare` variant on stat-card and list-items — 2 metas, 2 snippets, 2 canon blocks, plus the variant naming question. Falls out of C1: the moment tiles have a ground, every bordered component inside one needs this. |
| **C5** | `.cn-chart-line .dv-toggle-seg{border-radius:var(--border-radius-segmented-container-xs)}` + `.ind{…thumb-xs}` | B6 — chart toolbar corners | **Small but wide.** 2 declarations × the chart scopes that share the block (chart-line, chart-combo, and by inspection bar/donut/pie), **plus** the two he missed (`.dv-vt`, `.dv-tbl-toggle`). Gate-glob-scope rule applies: rule only as wide as the glob. |
| **C6** | `.cn-navigations .dashboard-logo img{width:42px}` (+ the 56px slot) | B8 — masthead logo composition | **Small-medium.** A `.logo img` rule in canon plus a Navigations snippet update is small; the light/dark mark swap is the real work and has no precedent outside `.cn-template-auth`. Note his own version does **not** swap. |
| **C7** | `.dashboard-root{background:var(--surface-subtle)}` | B4 — the rails' `pageBg: grey` default, enacted by hand | **Small.** One page-level utility (`.c-page-grey` or an attribute) so `page_rail` has somewhere to land. |
| **C8** | `@media(max-width:520px){.cn-navigations .main{display:none} …}` | the masthead has no responsive collapse | **Medium.** Hiding the nav is a stopgap, not the fix — a real collapse (menu button + flyout) is a Navigations component change, and the component already has the flyout machinery. |

**The inversion worth noticing.** Two components the by-the-book flow got *right* and the
hand-polish dropped: the regen uses `.cn-empty-state` (`Empty-state.reference.html`, "no results"
tier) and `.cn-summary` (the component); Dave hand-rolled `.transaction-empty` (`padding:40px 24px;
text-align:center; border:1px solid var(--divider-border-section); background:var(--surface-raised)`)
and used the `.c-summary` **utility** with its raw font (B10). Under SKILL step 3 —
"no redefining a `.c-*`/`.cn-*` class … if you're redefining a component locally, you've left
canon" — three of his rules (`.cn-chart-line .dv-toggle-seg`, `.dashboard-tile .cn-list-items
ul.list`, `.c-bento.dashboard-bento`) are formally out of canon. Which is the point: **canon
could not express what he needed, so he left it.** The regen stayed inside canon and is unusable.

---

## 4. UNPROVEN, declared

- **U1 · Nothing here has been rendered.** No headless browser in the sandbox — `which chromium
  chromium-browser google-chrome` returns empty, `import playwright` → `ModuleNotFoundError`, and
  pip is dead on a full disk. Every claim above is read from CSS source, token values and
  selector order. They are quoted with file and line so they are re-checkable, but **no pixel in
  either file has been measured.** The one thing that would settle "how much worse does the regen
  actually look" is a screenshot pair, and it does not exist.
- **U2 · The compare page's synchronised theme control is untested.** It sets `data-theme` and
  `data-apollo-theme` on both iframes' documents, which `file://` normally refuses as
  cross-origin. The page detects the refusal and reveals a fallback banner with a
  `python3 -m http.server` recipe — **the detection path is also untested.** If Dave opens it from
  the filesystem and the banner does not appear but the buttons do nothing, that is this.
- **U3 · Only the gate SKILL step 5 names was run.** `knowledge/_validate_screen.py`, on both
  files. The wider `check-with-gates` suite was not run; the individual gates (radius, type,
  contrast, dataviz) were not driven on either file.
- **U4 · B7 is a measurement, not a verdict.** I measured that `.seg.sm` in console is a 6px track
  around a 0px thumb and that canon.css calls the mapping "PROPOSED not ruled". Whether that is
  wrong is Dave's call, and `reviews/SEGMENTED-ADOPTION-2026-08-25-v1.html` is already the place
  he was meant to make it.

---

## 5. REPLAY-THESE

Run from the repo root. Each one re-derives a claim above.

```bash
# B1 — no bento snippet, no foundation meta (expect 0 / 0)
ls knowledge/snippets/ | grep -ci bento
ls knowledge/components/ | grep -ci foundation

# B2 — the dashboard tile surface is showroom-local, not canon (expect 0, then line 487)
grep -c 'bm-tile\|bm-card\|bm-wall\|bm-inner' knowledge/canon/canon.css
grep -n 'bm-card' showroom/_foundations/grids-dashboard.html | head -1

# B4 — the rails' dial names bind to nothing (expect 0)
grep -c 'mainSpacing\|subSpacing\|bentoBg\|keylines' knowledge/canon/canon.css
python3 -c "import json;print(json.load(open('knowledge/_render/_bento_edit_rails.json'))['defaults']['values']['dashboard']['mono'])"
sed -n '1178,1186p' knowledge/canon/canon.css        # canon's hardcoded 1px

# B5 — no radius on .search anywhere (expect 0), neighbours have one
grep -c '\.search[^ ]*{[^}]*border-radius' knowledge/canon/canon.css
sed -n '11382p;11397p;11439p' knowledge/canon/canon.css

# B6 / A1 — chart + toolbar .seg and dv-* boxes carry no radius
sed -n '8865,8866p;8885,8886p;8897,8898p;11424p' knowledge/canon/canon.css
sed -n '14307,14309p;14351,14353p' knowledge/canon/canon.css   # where the binding does live

# B7 — the contract omits the ruled scale; the map declares itself PROPOSED
python3 -c "import json;print(json.load(open('knowledge/components/segmented-control.meta.json'))['variants'])"
sed -n '14343,14352p' knowledge/canon/canon.css
sed -n '22166,22174p' knowledge/canon/canon.css      # console's xs container 6px / thumb 0

# B8 — masthead logo is text only (expect 0 for .logo img)
grep -c '\.logo img' knowledge/canon/canon.css
sed -n '1756p' knowledge/canon/canon.css
grep -o '<span class="logo"[^<]*<' knowledge/snippets/Navigations.reference.html

# B13 — the runbook contradicts the skill (expect 1187 / 0 / mono absent)
grep -c 'data-apollo-theme' knowledge/canon/canon.css
grep -c 'data-apollo-theme' knowledge/canon/type.css
grep -o 'data-apollo-theme="[a-z]*"' knowledge/canon/canon.css | sort | uniq -c

# B12 — the gate cannot tell them apart (expect two identical PASS blocks)
# ⚠ B14: each run REWRITES knowledge/_SCREEN-GATE.md. Restore it afterwards:
#        git checkout -- knowledge/_SCREEN-GATE.md
python3 knowledge/_validate_screen.py dashboards/international-banking-dashboard.canon.html
python3 knowledge/_validate_screen.py dashboards/international-banking-dashboard.regen-v1.html
git checkout -- knowledge/_SCREEN-GATE.md

# B14 — the clobber, before restoring (expect ~26 deletions on a file you did not edit)
git diff --stat -- knowledge/_SCREEN-GATE.md

# §0 — Dave's harness, rule by rule (expect 29 declarations, 2 border-radius)
sed -n '/<style>/,/<\/style>/p' dashboards/international-banking-dashboard.canon.html \
  | grep -o '[^}]*{[^}]*}' | sed 's/{/  ==>  /;s/}//' | nl
```

**And the one that needs his eye, not a shell:**
open `reviews/DASHBOARD-REGEN-COMPARE-2026-08-30-v1.html`, switch Theme to **Console**, and look
at the chart toolbar and the payments search row. If the theme buttons do nothing, that is U2 —
serve the repo over HTTP first.
