# Template dashboard (bento) — a quality review

Session #288, lane T · 2026-09-19 · READ-ONLY (no generator, no gate, nothing in `knowledge/` touched).
Deliverable page: `notes/_lanes/288/T/template-quality-review.html`. Store row: `W-288t`.

Dave's framing: *"I'm not sure about the quality of the template we need to look at this too."* ·
*"I just need the one-shot design to not disappoint, however it is getting better all the time."*

⚠ The gutter delivery path (the s219-D3 generation arm / the 40-4 literal pin) is **in flight, lane A**
and is deliberately not reported here as a finding.

---

## Headline

**The drawn page is sound; the paperwork around it is not.** Zero invented markup, zero dangling vars,
zero raw `font:` declarations, zero hex outside the theme blocks, zero raw inline lengths. Every finding
below is in the metadata, the status derivation, or the delivery path — i.e. in exactly the layer a
one-shot machine reads.

---

## 1 · Structure and markup — the #230 pass condition

**PASS.** Every region is a declared byte-identical splice with a line range and a sha256 prefix in the
build report's borrow ledger. The file's own new CSS is nine relationship rules, declared as such, and
the count holds. Checks run:

| check | measured |
|---|---|
| dangling `var()` — the silent-black class | **0**. 82 names referenced, 125 declared. (The single miss, `--undefined`, is prose inside an HTML comment.) |
| raw `font:` / `font-size` / `font-weight` / `line-height` in `<style>` | **0** over lines 1–920 with comments stripped. Type arrives from `.t-cm-*` composites throughout. |
| hex outside the two theme blocks | **0**. All 98 hex occurrences sit in the light block (`:170–247`) or the dark block (`:251–300`), or in prose. |
| inline `style="…"` attributes | **9**, all safe: one `position:absolute` on the hidden sprite sheet (`:930`), one `opacity:.6` (`:1108`), six `animation-delay:Nms` on chart rects (`:1124–1129`). |

**Where the template's raw lengths actually are** — not inline, but in its own `<style>`: **129** raw
px/rem declarations, comments stripped, split by region:

| region | raw lengths |
|---|---|
| AUTO-TOKENS (`:123–150`) | 0 |
| AUTO-BENTO, generated (`:320–492`) | 6 |
| spliced component CSS (`:493–775`) | 78 |
| the instance dials (`:776–904`) | 22 |
| APOLLO-DEMO css (`:905–911`) | 5 |

The 22 in the dials include the two gutter literals (`:802`, `:804`) — **lane A's**, not reported here —
and the three rung floors `120/240/96` (`:824–826`), which are ruled.

---

## 2 · The inline-style census, re-run

**The exact command** (run at `/sessions/.../UX-design`):

```python
import re, glob
root='knowledge/snippets/'
pat=re.compile(r'style="([^"]*)"', re.S)          # multi-line aware
raw=re.compile(r'(?<![\w-])\d*\.?\d+(px|rem|em)\b')
tot=attrs=0
for f in sorted(glob.glob(root+'*.reference.html')):
    for m in pat.finditer(open(f, encoding='utf-8', errors='replace').read()):
        tot += 1
        for d in m.group(1).split(';'):
            if ':' not in d: continue
            p, v = d.split(':', 1)
            if p.strip().startswith('--'): continue          # custom props excluded
            if raw.search(v) and 'var(' not in v:
                attrs += 1; break
print(tot, attrs)      # -> 566 87
```

### The numbers

| population | `style="` attrs | attrs with a raw px/rem/em and no `var()` |
|---|---|---|
| `knowledge/snippets/*.reference.html` (137 files) | **566** | **87** |
| `knowledge/snippets/*.html` (139 — adds two `_REVIEW-66-*.html` scratch files) | 596 | 87 |
| `Template-dashboard-bento.reference.html` alone | **9** | **0** |

⬛ **Lane X's 596 is the folder sweep and includes two `_REVIEW-66-scatter-*` scratch files that are not
library components.** The reviewed-population figure is 566. Lane X's **88** and my **87** differ by one;
both are the same measurement to within a parse detail (six attributes span line breaks, so a per-line
grep and a multi-line regex disagree slightly). **87 remains the right actionable number to put to Dave.**

### Classification of the 91 raw declarations inside those 87 attributes

| class | declarations | breaks a theme switch? |
|---|---|---|
| **layout** (margin 35 · gap 15 · width 15 · height 9 · max-width 6 · flex 4 · min-height 3 · padding 2 · misc 2) | **91** | No. A theme changes colour and radius; these are geometry. |
| **type** (6 × `font-size`) | **6** | **Yes** under a size-ramp/type-theme change. All six are specimen rows: `Links.reference.html:125-127`, `Tags.reference.html:93-95`. |
| **colour** | **0** | Nothing to break. |

**Conclusion: the inline-style population is not a theming risk.** It is a tidiness question. 33 of the 87
sit inside `APOLLO-DEMO … START/END` harness blocks or on demo-class elements ("showroom harness — never
copy"); 54 are in shipped component markup. The single most-repeated value is `margin-top:2.75rem`, a demo
section spacer, ×12.

### No gate covers it

`knowledge/_validate_no_hardcode.py` (DEF-004) **does** read `style=""` attributes — that hole was fixed at
#221 after #220-L1 planted three hardcodes and the gate exited 0. But:

- its population is `knowledge/_proforma/*.html` filtered to `id="icon-manifest"` — **11 files**
  (`_validate_no_hardcode.py:185`). `knowledge/snippets/` is **not in scope at all**;
- its axes are spacing · radius · border-width. `width` / `height` / `max-width` / `font-size` — most of
  the 87 — are **outside the stated scope** (`:35`, "geometry/dimensions … are a separate axis").

So widening the population would still miss most of the 87. That shapes decision-pack Q1.

### Top files by raw declarations

Filter-toolbar-bar 10 · Data-grid 6 · Layout-utilities 6 · Amount-display 5 · Template-detail 5 ·
Links 5 · App-shell-doormat 5 · Tags 4 · Chart-bar 12 **(all custom properties — `--b1`/`--b2` stacked-bar
offsets; excluded from the 87 by the custom-property rule, and legitimately so)**.

---

## 3 · Type, colour, spacing

- **Type: clean.** Zero raw font declarations. One *declared, visible, open* defect: the Summary value
  row's 500 weight is lost, because the splice dropped the source's two raw `font:` declarations and
  `.t-cm-label` carries no weight channel. The file names it and assigns it —
  `Template-dashboard-bento.reference.html:655-657`: *"the value row's 500 WEIGHT IS LOST. ⬛ DECLARED,
  VISIBLE, AND DAVE'S."* It is in the position rail, so it is on screen in any one-shot.
- **Colour: one declared drift, and it is the right call.** `surface/subtle` dark = `#1F1F1F`;
  `tertiary/background/default` dark = `#1F1F1F` — **byte-identical, 1.00:1** (verified in
  `knowledge/tokens/semantic-colour.json`). The ruled `pageBg: grey` would therefore paint wall and
  modules the same colour in dark with keylines off. The template ships `--wall-ground:#1A1A1A`
  (`:300`, `background/default`) as a manifest driftAllow with the reason at `:1376`. Light leg
  (`:247`, `#F0F0F0`) is on-token.
- **Dangling dataviz: none.** Both theme blocks declare `--data-series-1`, `--data-series-3`,
  `--data-axis`, `--axis-alpha`, `--data-grid`, `--grid-alpha` (`:204-205`, `:267-268`). The file's own
  `$foundByLooking[0]` records that the masthead's three vars were bound-and-never-declared in the first
  cut and that `gen_snippet_tokens.py` caught it, not an eye — the same class, caught pre-gate.

---

## 4 · Responsiveness — READ FROM CSS, NOT RENDERED

⛔ **UNPROVEN: no render.** No chromium, no playwright, no selenium at this seat;
`source knowledge/_render/seat_env.sh` → `SEAT_ENV: FAIL envdir absent`. Building the environment is not
the "cheap" the brief allowed. Everything below is a CSS read.

Geometry: `.tpl-bento-stack{padding:0 32px}` (`:798`), no max-width anywhere on the page chain. The wall is
its own container (`container-type:inline-size; container-name:bento`, `:347`). Canon bands rewrite
`--bento-cols-now` at container ≤1100 → 3, ≤820 → 2, ≤520 → 1 (`:405-417`). Wall tiles are 6 (lead) + 4
(evidence) + 2 (context) — `:1029`, `:1108`, `:1166`.

- **At 1920 window** → wall ≈ 1856 → above 1100 → **6 columns**. Masthead padding `0 32px` (`:717`)
  matches the wall's, so the vertical alignment holds. No cap: `.l-container{--l-max:1120px}` is
  **defined at `:509` and applied to no element in the body**. `.l-measure{max-width:64ch}` (`:522`) is
  used once, on `.tpl-display` (`:977`). Summary's own `max-width:420px` is **deliberately not copied**
  (`:657`, s210-D3 "the container dictates the width") — so at 1920 the rail's summary rows run to
  ~900px with key and value at opposite ends. **Predicted, never seen.**
- **At 1024 window** → wall ≈ 960 → the ≤1100 band → **3 columns**, plus rule 6b (`:843`): the context
  rail takes `grid-column:1/-1`, and its own container query `min-width:821px` (`:846` region) keeps its
  two `data-c="3"` cards side by side. This is s248-D1/D4 as approved.
- ⛔ **The 520 band is unmeasured for the headline row.** Rule 10a (`:882`)
  `.tpl-page .c-bento.tpl-group-lead > .c-bento__grid{grid-template-columns:repeat(4,minmax(0,1fr))}`
  deliberately **opts out of every band**. Its own comment (`:868`) records *"measured 4/4/4 at 1440 /
  1100 / 820"* — 520 is absent. At a 520 wall, four KPI tiles get ≈125px each minus gutters, which will
  not hold a formatted currency figure. Named as a risk, not a proven defect.

---

## 5 · Status — the meta says PROPOSED, the showroom says beta

**`showroom/index.json` cannot express "proposed" at all, and the template can never reach "stable".**
Both established from the generator, `knowledge/_render/gen_library_214.py`:

- `STATUSES` (`:258-262`) is a **fixed three-key list** — stable / beta / deprecated — ruled at s215-D5(2).
  `index.json`'s `$statuses` is a straight projection (`:1552`). There is no free-text field.
- `status_of()` (`:519-528`) is the ONE derivation: `deprecated` if the meta says so, else `stable` iff
  the slug is in the gated set **and** `PROPOSED_RE` (`:265`, matching `PROPOSED|NOT GATED|eye owed`)
  does **not** match the meta's `$status`, else `beta`. **So beta is the residual bucket, and a PROPOSED
  marker actively DEMOTES to beta.** The card is not contradicting the meta; beta is the generator's only
  way of saying what the meta says.
- ⛔ **The date trap.** `gated_slugs()` (`:507-517`) reads
  `reviews/ITINERARY-STATUS-2026-08-21-v3.json` — a frozen snapshot dated **2026-08-21**. The template was
  built **2026-08-31**. 134 slugs are GATED in that file; `template-dashboard-bento` is not one of them and
  **structurally never can be**. So even with a perfect status line the card stays beta. (By contrast
  `template-dashboard` IS gated and is beta only because of its own PROPOSED marker.) 26 of 145 rows are
  currently non-stable.
- `STATUS_OVERRIDES = {}` (`:257`) is the declared seat for Dave's rulings and is empty.
- Self-test bite 14 (`:1626-1628`) asserts every row's status is in `STATUSES`, so a fourth key is a
  generator change plus a ruling on the status set.

### ⛔ And the meta's status line is badly stale — four of its five claims are false

`template-dashboard-bento.meta.json:5` still reads *"PROPOSED #231 … ⛔ NOT GATED, NOT RULED, NOT
REGISTERED - absent from CATEGORIES, MIGRATED_SNIPPETS, component-types.json and _rulings.json. It IS
projected into canon.css and showroom/ because … gen_showroom.py glob[s] every snippet; that is the
serial's own behaviour, not a registration."* Measured today:

| claim | measured |
|---|---|
| absent from `_rulings.json` | **FALSE** — **32** rulings name it: s231-D2, s232-D3, s245-D6/D7/D8/D9, s246-D2…D6, s247-D2…D5, s248-D1…D4, s249-D1/D2/D5, s251-D1/D2/D10/D12/D14/D15, s252-D1, s255-D1, s268-D3, s272-D85. |
| absent from `component-types.json` | **FALSE** — registered as a `$partials` member at `component-types.json:472`, and the DP-08 entry at `:543` names it as the sole consumer scope. |
| NOT RULED | **FALSE** — s245-D9 sets its rung ladder by name; s248-D4 records *"W2 RHYTHM AS RENDERED IS APPROVED"*. |
| only globbed into canon | **FALSE in spirit** — 196 `.cn-template-dashboard-bento` selectors in `knowledge/canon/canon.css`. |
| NOT GATED | **TRUE** — but for the date reason in §5 above, not for merit. |

A cold builder opening the meta is told the thing they are about to copy is unapproved scaffolding.

---

## 6 · The `$awaitingDave` and `$tokenGaps` entries

⚠ **Correction to the brief: the meta carries THREE `$awaitingDave` entries, not four** (`:190-193`),
plus two `$tokenGaps` (`:195-196`).

| # | asks | what it would take to close |
|---|---|---|
| aD-1 | **The dark page ground.** s219-D1 rules `pageBg: grey`; its dark leg collides with the tile surface at 1.00:1, so the file ships `#1A1A1A` as a declared driftAllow. | Dave's eye on the three readings already rendered at `reviews/BENTO-SNIPPET-2026-08-31-v1.html`, and one word. Zero code either way if he ratifies what ships. |
| aD-2 | **May a snippet link `canon.css`?** 0 of 137 do, so this file carries a declared copy of the AUTO-BENTO block, which `gen_canon_components` then re-projects back into canon (+8KB). Nothing compares the copy to its source — **it will rot silently.** | Either a convention change (link canon — touches all 137), or build the byte-compare gate (already priced in the #231 report), or teach the projector to skip canon-owned selectors. The gate is the cheap half. |
| aD-3 | **Do the other three themes' dashboard defaults belong in a snippet?** Snippets are single-theme (mono) by convention; only mono's 40/4 is minted here. | Answered by lane A's s219-D3 generation arm if built — then the snippet needs no literal at all. Otherwise a convention ruling. |
| tG-1 | `layout/bento/columns` **cannot** be manifest-bound: `gen_snippet_tokens._unitless()` does not know the path, so `resolve()` returns the string `'6px'` and `repeat(6px,…)` is invalid CSS. MEASURED. | A **one-line** fix — add the path to `_unitless` — in a shared generator, so it is the build-PM's class fix, not a lane's. |
| tG-2 | `layout/bento/packing` cannot be bound either: s217-D4 stores `'row dense'` under `$extensions` rather than `$value`, so `resolve()` raises `KeyError`. | Nothing to fix — that is the **ruled** storage shape. Closing it means re-ruling where extension values live, or accepting the declared literal permanently. Recommend the latter. |

### ⛔ And the meta actively contradicts the shipped markup

`antiPatterns[3]` (`:135`): *"Do not invent a span. Only 6 and 3 are square at every compiled band …
A `data-c="2"` tile leaves one column empty at the 3-column band, and no gate sees it."*
`$bentoGrammar.spans` (`:187`): *"ONLY `data-c="6"` and `data-c="3"` … Every wall holds an even number
of 3s."*

The shipped wall is **6 / 4 / 2** (`:1029`, `:1108`, `:1166`) — legalised later by s248-D1's rule 6b
(`:843`) and approved by Dave at s248-D4. The meta was never amended. **A builder reading the contract
would "fix" the shipped wall back to 3+3 and unbuild Dave's own approval, with every gate green.** This
is the highest-ranked finding on the deliverable page.

---

## 7 · Against the one-shot goal

`notes/_briefs/2026-08-31-230-demo-day-brief.md` § THE GOAL, Dave verbatim: *"I Either expect it would
use the dashboard bento or it will ask if that is right."* Pass condition (3): *"copies component markup
from `knowledge/snippets/` with canon tokens — zero invented markup."*

On (3) the template **delivers completely** — it is the thing that made (3) possible, since the #230
rehearsal measured `grep -rl '\.c-bento' knowledge/snippets/` → 0 files.

Three ways it would still disappoint, ranked:

1. ⛔ **The builder may never reach it.** The shipped skill makes `_compose_slice.py` the mandatory step 1
   (*"Seed — ask the graph, do not read the library"*). I ran it:
   `python3 knowledge/_compose_slice.py "build a dashboard overview screen" --out /tmp/seed.json --explain`
   → **19 components, no template of any kind**. The only occurrence of "bento" in the entire seed is a
   phrase inside `app-shell-top-nav`'s `when` clause (*"the bento template composes it"*). Cause:
   `knowledge/roles.json` has **0** mentions of the template — it provides no role, so the reader cannot
   return it. ✓ **Mitigated by prose**: `apollo-spider/skills/generate-from-canon/SKILL.md:110-125` names
   the file explicitly and says *"splice the snippet, not re-draw the wall"*, and
   `apollo-spider/cold-start/DESIGN-CONTRACT.md:12` carries the ask-first line. So the shipped pack IS
   wired — but at line 119 of a long skill, after a step 1 that says the opposite.
   ⚠ The **stale zips** `designer-skills-v1/` and `designer-skills-v2/` have **zero** mentions of
   `template-dashboard-bento` or `showroom/index.json` in any `SKILL.md`. The brief's grep returns nothing
   because those packs predate the wiring; the live pack is `apollo-spider/skills/`.
2. ⛔ **If they reach it and read the contract, they may unbuild it** — §6's contradiction.
3. ⚠ **On a wide screen it will look unfinished** — §4's no-cap plus the stretched summary rows.

---

## 8 · Decision pack — six questions (full text on the HTML page)

1. **The inline-style rule.** 87 raw values, zero colour, six type, no gate covers the population.
   Options A ban all / B ban only the six type values / C ban in shipped component regions and exempt
   harness blocks / D no rule. **Rec: C** — the harness blocks already say "never copy", so the exemption
   is free to define and the rule aims at the markup builders actually lift.
2. **The template's status.** Options A add a fourth status word / B keep three, accept beta, fix the
   meta's stale line / C re-measure the gated set at today's date / D override to stable now.
   **Rec: B + C** — B costs no ruling and removes the contradiction; C repairs a date trap that pins
   every post-21-August component at beta forever, which is bigger than this template.
3. **aD-1, the dark page ground.** A ratify what ships / B keep the token and turn keylines on in dark /
   C derive a new dark token. **Rec: A** — it is what has shipped and been looked at for twenty sessions.
4. **aD-2, may a snippet link canon.css.** A link it / B keep the copy and build the byte-compare gate /
   C teach the projector to skip canon-owned selectors. **Rec: B** — buys the rot protection without
   reopening a convention 137 files rely on.
5. **aD-3, the other three themes' defaults.** A keep one theme / B write all four in / C no literal at
   all. **Rec: A** — C is what lane A's generation arm is for; B creates a second home for a generated fact.
6. **Does an overview dashboard have a maximum width?** A no cap / B cap at the existing 1120px container /
   C no cap on the wall, restore the cap on summary rows. **Rec: C** — filling a wide screen is right for a
   bento and wrong for a key-and-value list. Wants a render at 1920 first.

---

## What I could NOT establish

- ⛔ **Any render.** No browser at this seat; `seat_env.sh` reports its envdir absent. 1024 / 1920 / 520
  are CSS reads throughout and are labelled so on the page.
- ⛔ **Whether rule 10a's four-across headline actually holds at the 520 band.** The file records 1440 /
  1100 / 820 only.
- ⛔ **What the wide-screen summary rows look like.** Predicted from the dropped `max-width:420px`, never seen.
- ⚠ **The one-token gap between lane X's 88 and my 87** is a parse detail (six attributes span line
  breaks), not a disagreement about population. Either is fine to quote; I used 87.

## REPLAY-THESE

```
python3 /tmp/lt/c3.py                       # the census, source quoted in §2 above
python3 knowledge/_compose_slice.py "build a dashboard overview screen" --out /tmp/seed.json --explain
python3 -c "import json;d=json.load(open('reviews/ITINERARY-STATUS-2026-08-21-v3.json'));\
g=set();[g.update(r.get('slugs') or []) for r in d['rows'] if r.get('derived')=='GATED'];\
print('template-dashboard-bento' in g)"     # -> False
grep -c "template-dashboard-bento" knowledge/_rulings.json          # -> 16 lines / 32 rulings
grep -n "Template-dashboard-bento" knowledge/component-types.json   # -> 472, 543
```
