# Receipt — #215 · the component library CHROME restyled to the Swiss / International Style

**Session** #215 · 2026-08-22 · Opus build sub under s204-D1 (PM topology), brief from the conductor
**Instruction** Dave, explicit: restyle the component-library page chrome to the Swiss design system.
**Contract** `.claude/skills/swiss-design-system/SKILL.md` (read first, followed as the design contract).
**Generator** `knowledge/_render/gen_library_214.py` — it owns `showroom/index.html`, `showroom/index.json`
and the kept-alive redirect stub `reviews/LIBRARY-2026-08-21-v2.html`.
**⚠ NOT COMMITTED by this sub — the conductor commits.** Dirty paths at hand-off are listed in §7.

---

## 1 · The two project substitutions — DECLARED

Both OVERRIDE the skill's example values. Both are standing law, not judgment:

| Skill's example | What this page ships | The law |
|---|---|---|
| accent `#DB0011` | **`#DA1A00`** | s151-D1, THE TWO-RED LAW — this is the red on white. The skill's `#DB0011` appears nowhere in the page; selftest bite 25 proves it. |
| `--black: #000000` | **`#1A1A1A`** | the ink rule (blackest-not-pure-black). No `#000000` anywhere in the chrome; same bite proves it. |

**Font.** The chrome already loaded the project grotesque, so per the brief the project face is kept and
the skill's fallback chain is appended:
`"Univers Next for HSBC", "Helvetica Neue", Helvetica, Arial, sans-serif` (one `--face` token, used by
every control — `font:inherit` alone was silently dropping the face inside `<button>` and `<input>`).
Driven: `document.fonts.check('16px "Univers Next for HSBC"')` → **true** in the rendered page.

**The skill's neutral ramp is taken verbatim** — grey-1 `#F3F3F3` … grey-8 `#333333`, with the
grey-4/grey-5 "decorative only" warning carried into the CSS as a comment beside each token.

---

## 2 · Before → after, band by band

| | Before (#214/#215 v2 chrome) | After (Swiss) |
|---|---|---|
| Ground | `--page:#FAFAFA`, off-white everywhere | white page; grey-1 only where a band is *contained* |
| Header | 10px padding, 16px h1, ad-hoc grey `#808080` | the skill's nav bar: 56px, white, 1px hairline bottom, wordmark at head3/500, controls right, all labels caption2 uppercase 0.12em |
| Buttons | boxed `.btn` with a 1px grey border on white | **ghost**: no fill, no box, 1px ink bottom rule, caption2/500 uppercase 0.06em |
| Segmented | 1px ink box, active = ink fill | kept (already Swiss), retracked to 0.06em uppercase and put on the 8px grid |
| Tabs | 12px, active = **ink** underline | Swiss nav: caption1/500 uppercase 0.06em, grey-7 → ink on hover, **active = 2px ACCENT underline** (the one structural accent moment) |
| Chips / pills | `border-radius:999px` | **square** — no radius anywhere (skill: radius softens edges that should be resolved) |
| Tree | 12–13px mixed, grey `#808080` metadata | group heads caption2/500 uppercase 0.12em ink; rows caption1 ink; all secondary text grey-7 |
| Gallery | ONE grid: an intro `<div>` plus 135 bordered cards, 16px gaps | **three bands with different structures**, each closed by a full-width 1px hairline rule: (1) full-width opener — label pattern + head2 + a 4-up **stat display** (43px numerals at weight 200, caption2 labels); (2) a **3fr / 1fr divider / 4fr proposition split** carrying three notes with **decorative index numerals 01–03 in grey-4**; (3) the **feature grid**: grey-1 ground, white cells, **1px grey-2 gaps**, no borders, no radius, no shadow, hover = 1px ink outline |
| Section openers | none | **the label pattern** — 20px accent dash + uppercase caption2 eyebrow — on every main-column band |
| Spacing | 5/6/9/10/11/12/14/18/20/24px, ad hoc | the skill's 8px system, `--s1`…`--s7`, used throughout |
| Shadows / radius | none / pills | **none / none** — proven by selftest 24 and driven check CC |
| Focus | `#305A85` blue outline | one treatment: 2px ink outline, 2px offset (17.40:1) |

**Accent budget.** The skill's ceiling is 2–3 accent moments in one scan. Shipped: the label pattern on
main-column bands + the active tab underline. Everything else that *could* have taken accent was given
ink or grey deliberately — the ghost buttons' bottom rule (skill suggests accent) is **ink**, the tree's
current-item left border is **ink**, and the sidebar/pane sub-headings use a **grey `.sublabel` variant**
of the label pattern (grey-3 dash, grey-7 eyebrow) so the sidebar never spends accent. Bite 27 proves the
accent fills **nothing but the 1px label dash** — never a surface, never a background.

---

## 3 · Scope fence — what did NOT change

- **Not one byte of specimen markup or CSS.** Every pane is still an `<iframe>` at the component's own
  generated showroom page (selftest bite 2 counts exactly one iframe in the page).
- **The `#chrome=0` embed contract** and the **theme/dark/width fragment broadcast** are untouched —
  driven green for all four themes (checks V, W, X, Y×4).
- Type/Usage tabs, status facet, alias search + `/` + cmd-K, thumbnails, related strips, `index.json`,
  the redirect stub, recently-opened, deep links: all unchanged in behaviour.
- **Dark mode — the path taken, and why.** The header's Light/Dark switch is a **pane broadcast**: it
  re-themes the iframe by URL fragment and has never applied to the chrome. It still doesn't. Swiss
  chrome is white-ground by design and the brief permits keeping it light in both modes, so that is what
  ships — which means **the dark-ground arm of the two-red law is never reached**: `#F6604C` is not used
  and no 3:1-on-dark check is owed. Recorded in the CSS header comment so a later reader cannot mistake
  the absence for an oversight.
- One behavioural line changed, and it is a bug fix, not a restyle: `buildGallery()` now appends cards to
  `#cardgrid` (the grid) rather than `#gallery` (the scroller), and `#galleryempty` is generated markup
  rather than a JS-built node. `#gallery` is still the scroll container the drive script scrolls.

---

## 4 · WCAG — every text/ground pair in the chrome, MEASURED not intended

Driven in the rendered page: walk every element with a text child (iframe excluded), read computed
colour, walk ancestors for the effective background, compute the WCAG 2.1 ratio, and pick the threshold
from the element's own computed size and weight. Pressed-chip, current-row and open-pane states were
exercised first so their colours are in the sample.

| Ink | Ground | px | wt | ratio | needs | where |
|---|---|---:|---:|---:|---:|---|
| `#B7B7B7` grey-4 | `#FFFFFF` | 34 | 200 | **2.01** | 3.0 | `01/02/03` decorative index numerals — **exempt, see below** |
| `#767676` grey-6 | `#FFFFFF` | 12 | 500 | 4.54 | 4.5 | disabled ghost button label (also the search placeholder) |
| `#DA1A00` accent | `#F3F3F3` grey-1 | 12 | 500 | 4.58 | 4.5 | "ALL COMPONENTS" label on the grid band |
| `#DA1A00` accent | `#FFFFFF` | 12 | 500 | 5.09 | 4.5 | "THE LIBRARY" / "HOW IT WORKS" labels |
| `#545454` grey-7 | `#F3F3F3` grey-1 | 12 | 500 | 6.82 | 4.5 | tier word on the current tree row |
| `#545454` grey-7 | `#FFFFFF` | 12–16 | 400–500 | 7.57 | 4.5 | control labels, counts, hints, blurbs, tab (inactive), clear button |
| `#1A1A1A` ink | `#F3F3F3` grey-1 | 14 | 500 | 15.68 | 4.5 | current tree row |
| `#FFFFFF` | `#1A1A1A` ink | 12 | 400–500 | 17.40 | 4.5 | pressed chip, pressed segment |
| `#1A1A1A` ink | `#FFFFFF` | 12–43 | 200–700 | 17.40 | 3.0–4.5 | everything else — headings, body, stats, card names, tree rows, code |

**One sub-AA value, and it is the skill's own exemption:** the decorative index numerals `01 / 02 / 03`
in grey-4 at 2.01:1. They carry no information — each sits directly above a head3 heading in ink that
says the same thing ordinally — and the skill names grey-4/grey-5 "decorative only", with the brief
explicitly authorising "decorative large index numerals grey-4/5 (decorative exemption)". **⬛ OPEN TO
DAVE:** if he wants zero sub-AA values on the page at all, one token swap (`grey-4` → `grey-6`) closes it
and costs the numerals their recessiveness.

Two colours the walker cannot sample because they are state-only, checked against the same table by
token: `::placeholder` grey-6 on white = 4.54 (pass) and `.chip[aria-pressed] .n` white at 75% opacity on
ink ≈ 9:1 (pass). **grey-6 is banned on grey-1 grounds in this chrome** (4.09:1, a fail) — every band
with a grey-1 ground uses grey-7, and the ban is written beside the token in the CSS.

---

## 5 · Verification — every gate run, with the driven red

| Gate | Result |
|---|---|
| `python3 knowledge/_render/gen_library_214.py` | 135 components, index + index.json + stub written |
| `--selftest` | **27/27 bites green** (23 before, +4 Swiss) |
| `--check` | in sync |
| `python3 knowledge/gen_showroom.py --check` | OK — 135 pages + index in sync |
| `python3 knowledge/_render/drive_library_215.py` | **33/33 green** (30 before, +3 Swiss) |
| render-verify | 4 PNGs seen at 1500 / 1180 / 760 px, project face confirmed loaded |

**Four new selftest bites, each carrying a probeable token (s182-D1):**
- **24** no `border-radius` other than 0 and no `box-shadow` anywhere in the shipped chrome CSS.
- **25** the two-red law + the ink rule: the only red-family hex in the CSS is `#DA1A00`; `#000000`
  absent; the skill's `#DB0011` absent.
- **26** the label pattern is drawn (accent dash pseudo-element + uppercase eyebrow, ≥3 instances).
- **27** the accent fills nothing but `.label::before` — never a surface.

**Three new driven checks** (computed styles in the browser, not source text): **BB** active tab
border-bottom is `rgb(218, 26, 0)`; **CC** nothing among cards/chips/pills/buttons/segments/search/grid/
header/nav computes a radius or a shadow; **DD** the label's `::before` is a 20px accent dash and the
label is uppercase accent.

**TWO ASSERTIONS CHANGED, both styling-coupled, neither weakened.** Drive checks **A** and **M** read
`#rc` with `inner_text`, which returns *rendered* text; the result line is now a Swiss caption with
`text-transform:uppercase`, so the same string arrives as `135 OF 135 SHOWN`. Both now compare
`.lower()` — the exact count string is still asserted character for character. This was **observed as a
red before it was fixed** (28/30), i.e. the drive caught the restyle rather than sleeping through it.

**DRIVEN RED — the mutation tests the CLAUSE, not the feature.** In the generated
`showroom/index.html`, `--accent:#DA1A00` was replaced with the skill's example `#DB0011` — precisely the
substitution the two-red law forbids — and the drive re-run:

```
❌ BB · active tab is underlined in the accent #DA1A00 (two-red law s151-D1)
❌ DD · the label pattern draws a 20px accent dash before an uppercase eyebrow
DRIVE: 31/33 green
```

Regenerated afterwards and `diff` reports the file **byte-identical to its pre-mutation state**.

**One defect found and fixed by looking at the render, which no gate would have caught.** At 1500px the
header wrapped to a second row, and because `body` is a flex column the header — a flex item with the
default `flex-shrink:1` and `min-height:56px` — stayed 56px tall while its second row laid out at y=70,
painting the **Open** button on top of the sidebar's search field. `flex:0 0 auto` plus a tighter header
gap fixes it; the reason is written into the CSS beside the declaration. Re-measured: no header child
overflows its box at 1500 / 1180 / 760px.

---

## 6 · CONSEQUENCES / PITFALLS (mandatory)

1. **No gate parses the chrome's *layout*.** Bites 24–27 and checks BB/CC/DD read colours, radii and the
   label pattern. Nothing asserts band order, hairline rules between bands, or the 8px grid — a future
   edit can put three identical grids in a row, or compress a band below `--s5`, and every gate stays
   green. Same class as [[no-gate-parses-the-artefact]]; a "Swiss structure" bite is **priced, not built**.
2. **The accent budget is a judgment no gate holds.** Bite 27 stops the accent becoming a *fill*; nothing
   counts accent *instances*. Adding one more `.label` to the sidebar would push a single scan to four
   accent moments and no test would object.
3. **`inner_text` reads rendered text — every uppercase caption is a latent assertion break.** A/M were
   caught because they compare a whole string. Any future check that reads a Swiss caption must
   case-fold, or it will go red for a styling reason and be misread as a functional break.
4. **The card grid's 1px gaps ARE the grey-2 ground showing through.** Setting a background on
   `.cardgrid`, or a border on `.card`, silently destroys the hairline structure without failing anything.
5. **The chrome is light in both modes by design.** If Dave later rules the chrome must follow the dark
   toggle, `#DA1A00` must be re-checked on the dark ground *before* it is used there — the two-red law's
   else-arm (`#F6604C`) exists for exactly that and is currently unreached and untested here.
6. **Stale thumbnails still unguarded** (inherited, W-103): nothing re-shoots a thumbnail when its
   component changes, so a Swiss card can carry a stale photograph and every gate stays green.
7. **The receipt's contrast table is a MOMENT, not a property** (s129-D5). It was measured against the
   page generated 2026-08-22; any token edit re-opens it. The measuring script is not committed — it is
   reproduced in §4's method description, and a permanent contrast leg in `--selftest` is **priced, not
   built**.

---

## 7 · Hand-off

**Dirty paths (this sub changed these; the conductor commits):**
```
knowledge/_render/gen_library_214.py      the Swiss chrome + 4 new bites + the stat figures
knowledge/_render/drive_library_215.py    +3 driven Swiss checks, A/M case-folded
showroom/index.html                       regenerated
reviews/LIBRARY-2026-08-21-v2.html        regenerated (the redirect stub, restyled to match)
```
`showroom/index.json` is unchanged — the restyle touched no data, which is itself a check on the fence.

**Renders seen** (session outputs, non-repo): `s215-swiss-library-top.png`, `-grid.png`, `-mid.png`,
`-narrow.png` — 1500 / 1180 / 760px.

**⬛ OPEN TO DAVE**
1. The grey-4 decorative index numerals at 2.01:1 — keep the skill's decorative exemption, or trade
   recessiveness for a page with zero sub-AA values?
2. The header still carries "135 COMPONENTS" while the opening band's stat display says `135 / Components`
   in 43px. Deliberate (header = persistent state, band = the page's opening statement), but it is one
   fact in two places and Dave's eye rules whether that reads as rhythm or repetition.

**Nothing here is a ruling.** No `_rulings.json` write; no constants, thresholds or rulings introduced.
