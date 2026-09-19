# Spider spacing handoff — claims tested against the development workspace

Session #287, lane X · 2026-09-19 · READ-ONLY (no generator, no gate, no repo file changed but this one)

Source under test: `notes/_lanes/287/GPT-SPIDER-SPACING-HANDOFF-2026-09-18.md` (Apollo Spider
v1.0.13 test bed, HSBC CEO banking prototype, GPT agent, no vision).

Dave's framing: *"don't take it on face value, use your judgment, but what it did worked."*
That is the posture taken here. The browser-measured work is not re-litigated; only the report's
**factual claims about our system** are tested, against this tree, at file:line.

No gate was run. No generator was run. Nothing in `knowledge/` was touched.

---

## Headline

The report's *measurements* hold up and its *mechanism claims* are largely right, but it
mis-frames two of them. Twice it reads a **ruled value as a defect**:

- `--layout-bento-gutter: 0` is not a token that "failed" — it is the **ruled** value of
  `layout/bento/gutter` for mono and supercharge (s217-D2, Dave's own tuner exports).
- The template's 40/4 pin is not sloppiness — it is the snippet convention (single-theme, mono)
  declared in the meta's own `$awaitingDave`.

The real system finding, which the report circles but never names, is sharper than either:
**the bento gutter TOKEN and the dashboard ROLE DEFAULT disagree, per theme, by ruling.**

| theme | `layout/bento/gutter` (s217-D2) | dashboard `mainSpacing` (s219-D1(5)) | agree? |
| --- | --- | --- | --- |
| mono | 0 | 40 | ✗ |
| legacy / common | 24 | 24 | ✓ |
| console | 24 | 40 | ✗ |
| supercharge | 0 | 24 | ✗ |

Three of four themes disagree with themselves. Both numbers are ruled, on different days, in
different vocabularies, and nothing in the tree reconciles them. That is the actual §9-Q1 gap.

---

## 1. "The template scope embeds Mono's 40/4 regardless of theme; other themes' defaults are 'addressed elsewhere'." — **VERIFIED**

The pin, in compiled canon:

- `knowledge/canon/canon.css:18119`
  `:where(.cn-template-dashboard-bento) .tpl-page .c-bento.tpl-wall[data-bento-role="dashboard"]:has(> .c-bento__grid > .c-bento){--bento-gutter:40px; --bento-row-unit:auto;}`
- `knowledge/canon/canon.css:18121`
  `:where(.cn-template-dashboard-bento) .tpl-page .c-bento.tpl-group[data-bento-role="dashboard"]{--bento-gutter:4px;}`

Both are **literals**, not theme-conditioned, and the source comment at `canon.css:18117` says so
in as many words: *"MAIN SPACING 40px — mono's s219-D1 default, read off role_defaults_219.py
--table."* The same pair is in the authoring source at
`knowledge/snippets/Template-dashboard-bento.reference.html:802` and `:804`.

The "addressed elsewhere" wording is near-verbatim, in the meta's own hand —
`knowledge/components/template-dashboard-bento.meta.json`, `$awaitingDave[2]`:

> "WHETHER THE OTHER THREE THEMES' DASHBOARD DEFAULTS BELONG IN A SNIPPET. Snippets are
> single-theme by convention (mono); s219-D1's dashboard mainSpacing/subSpacing differ per theme
> (40/4 mono, 24/4 legacy, 40/4 console, 24/2 supercharge). Only mono's pair is minted here; the
> other three are ADDRESSED at role_defaults_219.py rather than typed into a second home."

The per-theme table the report quotes is correct against
`knowledge/_render/_bento_edit_rails.json` → `defaults.values.dashboard`:
mono 40/4, legacy 24/4, console 40/4, supercharge 24/2. The rails file resolves those from
`gen_foundations_217.ROLE_DEFAULTS` and declares itself GENERATED.

### Is there a supported cascade path that delivers the SELECTED theme's default?

**No — not to a consumer composing a screen.** Three findings:

1. **The role default never becomes CSS.** `_bento_edit_rails.json` is a *vocabulary* file. Its
   own header says: *"No editor is built or proposed here. This is the vocabulary such an editor
   would read"* (`$groundwork_only`). s219-D3 makes generation/editing/authoring three permission
   levels on that one manifest — but the generation arm is not built. Nothing projects
   `dashboard.supercharge.mainSpacing = 24` into a selector.

2. **What IS in canon is the theme TOKEN, not the role default.** `--layout-bento-gutter` is
   declared 24px under `[data-apollo-theme="legacy"], [data-apollo-theme="common"]`
   (`canon.css:22009`) and `[data-apollo-theme="console"]` (`canon.css:24611`), plus
   template-scoped repeats at `:24071`, `:24099`, `:25914`, `:25934`. Supercharge's block
   (`canon.css:26250`ff, 420 selectors) declares **no** `--layout-bento-gutter` at all. Mono is
   the `:root` base. Both therefore inherit `:root{--layout-bento-gutter: 0}` at
   `canon.css:537` — which is correct per s217-D2, and is *not* the role default.

3. **Even where the theme value exists, the template out-specifies it.** `canon.css:18119` is
   (0,4,0)+`:has()`; the theme declarations reach `--bento-gutter` only through
   `.c-bento[data-bento-role="dashboard"]:has(> .c-bento__grid > .c-bento)` at `canon.css:1199`,
   which is weaker. So a console page carrying `.cn-template-dashboard-bento` gets 40px from the
   template, coincidentally right, and a legacy page gets 40px, wrong — the theme's own 24px
   loses silently. The template's own meta already names this specificity trap in `antiPatterns`:
   *"canon's bento-of-bentos carve-out weighs (0,4,0) … Declare instance dials at (0,4,0) or above."*

**Verdict: the report is right, and the cause is deeper than it says.** There is no delivery path
because the generation arm of s219-D3 was never built; the rails file is groundwork that has sat
un-consumed since #219.

---

## 2. "`--layout-bento-gutter` resolves to 0 in the consuming scope." — **VERIFIED, but mis-framed**

Definition: `knowledge/canon/canon.css:537` — `--layout-bento-gutter: 0;` inside `:root`, in the
`/* ---- Layout (layout.json) ---- */` block.

Consumption: `canon.css:1082` (`.c-bento` re-declares `--bento-gutter: var(--layout-bento-gutter)`,
commented *"THE ONLY per-theme divergence"*), then `canon.css:1106` `gap:var(--bento-gutter)`.

For the tested page — Supercharge — the value **is** 0, because supercharge has no override
anywhere in canon. The snippet itself hard-declares it in both its theme blocks:
`Template-dashboard-bento.reference.html:235` and `:288` —
`--layout-bento-gutter:0; --layout-bento-outer-padding:0; …` (mono's value, per the snippet's
single-theme convention).

**Where the report goes wrong.** It calls this *"a legitimate token [that] resolved to 0"* and
treats it as a cascade accident — *"the reference to a legitimate token looked plausible in source
but failed in the browser."* It did not fail. `knowledge/tokens/layout.json:114` states the design
intent outright:

> "GUTTER IS THE ONLY PER-THEME DIVERGENCE — supercharge + mono 0px (this base), legacy + console
> 24px (their override sets)."

Ratified at s217-D2 from Dave's four tuner exports: *"supercharge and mono gutter 0px; legacy and
console gutter 24px."* Zero is the answer to the question `layout/bento/gutter` asks. The agent
bound the **wrong question's token** — it wanted the *dashboard role's* mainSpacing, and reached
for the *bento grammar's* gutter. Those are two ruled facts that happen to share a name-shape.

The local repair (`#portfolioWall` → `--padding-fixed-xlarge`) lands on 24px by arithmetic
coincidence, not by contract, and the report says so honestly ("not the ideal universal API"). It
is right to say so. It is also an ID selector, (1,0,0), which beats the template pin — legal under
the meta's antiPattern (which forbids *bare class* dials and *inline* dials, not ID selectors) but
exactly the "outguess template specificity" the report itself objects to.

---

## 3. "Supercharge's 2px inner gap has no intent-correct consumer binding — rendered inner groups stay 4px." — **VERIFIED**

- `2` is legal vocabulary: it is in the ruled stop set `{1, 2, 4, 16, 24, 40}`
  (`_bento_edit_rails.json` → `rail.spacing_stops`, `dials.subSpacing.options`, ruled by
  s219-D1(4)), and supercharge's dashboard `subSpacing` is `"2"` in `defaults.values.dashboard`.
- It reaches no CSS. `grep -rn 'bento-gutter:\s*2px' knowledge/canon knowledge/_render knowledge/snippets`
  → **zero hits**. The only sub-spacing declaration that ships is the 4px literal at
  `canon.css:18121`.
- The nearest 2px token is `--gap-fixed-content-xxsmall: 2px` (`canon.css:503`), declared at
  `:root` only, with no theme leg. It is a **content** gap, not bento vocabulary — borrowing it
  is precisely the "a token with a numerical value of 2px elsewhere is not automatically
  appropriate" move the report warns against, and I agree it should not be taken.
- The other 2px values in canon (`--padding-segmented-control-*`, `--border-width-medium`,
  `--focus-ring-width/offset`) are all worse candidates for the same reason.

So: legal dial value, no minting path, no binding. The report is correct and its recommendation —
mint through the existing authoring/governance process rather than borrow — matches s219-D3's own
"authoring is the only mode that widens the rails."

---

## 4. "The lead KPI group's `repeat(4, minmax(0,1fr))` is a deliberate override with a source comment." — **VERIFIED**

Found, twice:

- `knowledge/canon/canon.css:18184` —
  `:where(.cn-template-dashboard-bento) .tpl-page .c-bento.tpl-group-lead > .c-bento__grid{grid-template-columns:repeat(4,minmax(0,1fr));}`
- authoring source: `knowledge/snippets/Template-dashboard-bento.reference.html:869`

The comment is not a note, it is twenty lines of receipt, `canon.css:18164–18183`. It carries:

- the **ruling**: s251-D1/D2 at #251, and s247-D3 (the two status tiles leave the row);
- the **measurement**: *"the lead group is FOUR at every band — measured 4/4/4 at 1440 / 1100 /
  820, light and dark, maxWdiff 0, no void (#251 probe P1)"*;
- the **intent**, verbatim: *"It out-specifies canon's band clamps deliberately: four tiles never
  have to divide three because the band never reaches the row, which is what keeps s249-D5 (no
  ragged layouts) true here."* (s249-D5 is Dave verbatim at #249: *"No ragged layouts"*.)
- a **rejected alternative with its own measurement** (`canon.css:18174`ff, "10a", #255):
  writing the count onto `--bento-cols-now` or `--bento-columns` was tried and refused because
  `_validate_token_forks.py` would read it as a token fork — *"measured both ways at #255."*

The report's read is right and its caution is right: deleting this rule changes a ruled policy
(s249-D5) and would re-open a token-fork question that was already measured shut.

One correction to the report's framing. It says the metadata's *"broader banded-reflow
description does not adequately communicate this exception."* It does communicate it — in the
wrong place. `meta.json` → `variants[1] "banded"` describes the generic 6/3/2/1 bands and closes
with *"That is canon's compiled behaviour, not a variant this file declares"* — but the four-column
lead exception is recorded only in the CSS comment, not in the meta. So the defect is that the
**meta is silent**, not that it is misleading. That distinction matters for the repair: the fix is
an addition to the meta, not a rewrite of the variant prose.

---

## 5. "Metadata still says status PROPOSED with open governance questions while the composition skill directs its use." — **VERIFIED, and worse than stated**

**The meta.** `knowledge/components/template-dashboard-bento.meta.json`, `$status`:

> "PROPOSED #231 (2026-08-31), lane W-326 … ⛔ NOT GATED, NOT RULED, NOT REGISTERED - absent from
> CATEGORIES, MIGRATED_SNIPPETS, component-types.json and _rulings.json. It IS projected into
> canon.css and showroom/ because gen_canon_components.py and gen_showroom.py glob every snippet;
> that is the serial's own behaviour, not a registration. Dave's eye is owed."

Confirmed: `grep -n "template-dashboard-bento" knowledge/component-types.json` → **0 hits**. The
meta also carries four `$awaitingDave` entries and two `$tokenGaps`, unresolved.

**The skill.** `apollo-spider/skills/generate-from-canon/SKILL.md:115–130` routes to it as the
default for any dashboard request:

> "**dashboard bento — is that right?** … Then go bento-first unless the designer says otherwise.
> **A skip is a yes** … Bento-first means you **splice the snippet** … start from
> `knowledge/snippets/Template-dashboard-bento.reference.html`"

"A skip is a yes" makes it the **silent default**. The skill states no status at all.

**The part the report missed, and it sharpens §9-Q5.** The status surface the skill actually tells
builders to search is `showroom/index.json` (SKILL.md:24 — *"143 entries … Search this by aliases
and blurb"*). That file says:

> `{'slug': 'template-dashboard-bento', 'name': 'Template dashboard bento', 'level': 'template', 'status': 'beta'}`

So the system ships **two statuses for one artefact**: `PROPOSED / NOT REGISTERED` in the meta,
`beta` in the index a builder is told to consult. The index entry exists only because
`gen_showroom.py` globs every snippet — the meta predicted exactly this ("that is the serial's own
behaviour, not a registration") and was right. A consumer following the skill's own instructions
cannot discover that the template is unratified.

That is not a documentation nit. It is the mechanical answer to §9-Q5: *consumers discover status
from `showroom/index.json`, and `showroom/index.json` cannot express "proposed".*

---

## 6. "33 pass / 8 FAIL: composition, grid, polarities, receipt, role resolution, screen, token forks, type blast radius; three passes examined zero subjects." — **PARTLY — the arithmetic is exact; the attribution is mostly Spider-side debt**

All eight gate names exist here as real, wired validators:

| report name | file |
| --- | --- |
| composition | `knowledge/_validate_composition.py` |
| grid | `knowledge/_validate_grid.py` |
| polarities | `knowledge/_validate_polarities.py` |
| receipt | `knowledge/_validate_receipt.py` |
| role resolution | `knowledge/_validate_roles_resolve.py` |
| screen | `knowledge/_validate_screen.py` |
| token forks | `knowledge/_validate_token_forks.py` |
| type blast radius | `knowledge/_validate_type_blast_radius.py` |

**The 41 is exact.** Reading `_MANIFEST.json` out of `apollo-spider/dist/Apollo-Spider-v1.0.13.zip`
(extracted to scratch; the repo copy untouched): 55 verdicts, of which **41 RUNNABLE**, 10
REPO-BOUND, 4 NEEDS-DEP. 33 + 8 = 41. The report's total is the pack's runnable set exactly, so
the log it quotes is real and complete.

(Note the skill text at `apollo-spider/skills/check-with-gates/SKILL.md:8` says "36 gates". That is
stale against v1.0.13's manifest of 41. Minor, but the skill's own closing line — *"Read the gate
list from the runner, never from here"* — is the reason it is only minor.)

**Attribution.** Splitting the eight by what population they read:

*Screen-scoped — these three ARE the new screen's:*
- `_validate_receipt.py` — "the PROVENANCE RECEIPT gate (s235-D2). The first thing
  `_validate_screen.py <path>` does with a composed page." Takes the screen path.
- `_validate_screen.py` — "Composed-screen pipeline runner … Runs, on each composed screen."
- `_validate_composition.py` — "driven against a REAL bento artefact (never the library)",
  step 1b of the screen gate.

The report already concedes these: *"receipt behaviour checks fail and several
composition/provenance claims remain unproven."* Consistent, and they are the agent's to answer.

*Repo-population — these five are pre-existing pack debt, not caused by a fresh screen:*
- `_validate_polarities.py` — "the ONLY sanctioned writer for the polarity home" (s238-D7); it
  grades the polarity declaration and the commit seam, neither of which a designer's screen touches.
- `_validate_token_forks.py` — grades same-scope forks across the shipped token store (s136-D1 D).
- `_validate_type_blast_radius.py` — "guards `knowledge/canon/type.css`", a shipped file.
- `_validate_roles_resolve.py` — the 25-meta address-resolve pass (s251-D12), grades metas.
- `_validate_grid.py` — the 4px-grid gate over *tranche* files; whether it is the screen's depends
  on where the file was put (SKILL.md:80 explains the tranche routing).

So the honest split is roughly **3 screen-caused, 4 pack-baseline, 1 (grid) depends on placement.**
The pack's own runner supports exactly this reading: `ci-template/run-gates.py` ships
`--baseline` / `--write-baseline` for precisely this, and the skill says it in plain words at
SKILL.md:36 — *"a gate that was green and is now red is yours; a gate that was red before you
arrived is not."* The GPT agent ran no baseline, so it could not separate the two, and it reported
the aggregate. It was right to keep the aggregate visible; it should have baselined.

**"Three passes examined zero subjects" is a designed feature, not a bug.** `run-gates.py:274`
emits *"⚠ %d of those green(s) graded a population of ZERO — they have nothing to look at"* and
SKILL.md:97 says *"`passed (0 tranche file(s))` is a gate that graded nothing and exited green."*
The report's insistence that this stays visible is already our rule. Nothing to fix; the WP4
acceptance criterion ("zero subjects cannot masquerade as verified coverage") is **already met** by
the runner and should not be rebuilt.

---

## 7. Inline-style census

Dave: *"we still seem to be writing a lot of inline styles BTW, which would be good to avoid."*
He is right that the volume is large. He is mostly wrong about where it comes from — the shipped
library is not the problem; the **test-bed and review artefacts** are.

### Totals — `style="` occurrences

| bucket | files | `style="` |
| --- | --- | --- |
| **(a)** `knowledge/snippets/*.html` | 139 (107 with ≥1) | **596** |
| **(b)** `knowledge/components/*.html` | **0 files exist** (metas only) | **0** |
| **(c)** showroom pages `showroom/*.html` | 138 | **0** |
| (c2) `showroom/_foundations/*.html` | — | 35 |
| **(d)** generated screens `knowledge/_render/**/*.html` | **0 files** | **0** |
| `knowledge/_proforma/*.html` | — | 261 |
| `knowledge/_fitness-test/**` (composed screens live here) | — | **1,398** |
| `notes/**` | — | 805 |
| `dashboards/` + `dashboard/` | — | 98 |
| `knowledge/_demo` | — | 5 |

Two results worth stating plainly:

- **The showroom is clean.** 138 pages, zero inline styles — they embed via `<iframe>`. Whatever
  is wrong, the public-facing surface is not it.
- **There is no `screens/` directory and no HTML under `knowledge/_render/`.** Composed screens
  live in `knowledge/_fitness-test/`, and that is where the mass is: 1,398, more than twice the
  snippet library.

### Top 10 files by count

| n | file |
| --- | --- |
| 449 | `knowledge/_fitness-test/canon-gallery.canon.html` |
| 449 | `notes/_lanes/261M/attic/_m3probe/canon-gallery.canon.html` (attic copy of the above) |
| 202 | `knowledge/_fitness-test/nio-dash-console-v2.canon.html` |
| 195 | `knowledge/_fitness-test/nio-dash-console-v1.canon.html` |
| 191 | `knowledge/_review/DataViz-interactive-REVIEW.html` |
| 188 | `knowledge/_proforma/DataViz-interactive.html` |
| 60 | `notes/_lanes/281/rests-on/RESTS-ON-2026-09-17.html` |
| 60 | `knowledge/snippets/Template-report.reference.html` |
| 59 | `knowledge/_fitness-test/blue400-review.html` |
| 54 | `knowledge/_fitness-test/v7-series-assignment-AB.html` |

Seven of ten are fitness-test / review / proforma / notes artefacts. The highest-count *shipped
snippet* is 60, and `Template-dashboard-bento.reference.html` itself carries **9**.

### Classification — all 590 inline styles in `knowledge/snippets/`

Not a 30-sample; the whole population was classified, which is cheap and more honest:

| kind | n | share | example |
| --- | --- | --- | --- |
| **B — data-driven value** | 216 | 37% | `style="width:62%"` (meter/bar length), `style="animation-delay:90ms"` (stagger index) |
| **A — layout-dial / custom-property binding** | 93 | 16% | `style="--sc:var(--data-series-1)"` (74 of these are the dataviz series channel) |
| **E — harness / sprite / sr-only** | 81 | 14% | `style="position:absolute"` on the 0×0 SVG sprite (74); `clip:rect(0,0,0,0)` sr-only (5) |
| **D — presentational colour** | 78 | 13% | `style="fill:var(--mark)"` (68, token-bound, on SVG paths) |
| **C — one-off override a class should own** | 85 | 14% | `margin-top:2.75rem` (12), `display:flex; gap:12px` (5), `margin:0` (10), `opacity:.6` (9) |
| F — other | 37 | 6% | |

**Dominant kind is data-driven (B) at 37%**, and that is the *legitimate* category — a bar's length
is content, not style, and it cannot live in a stylesheet. Add A (token bindings) and D
(token-bound fills) and **62% of the population is defensible**.

**The 14% in category C is the real debt.** Concretely: **88 of 590 inline styles carry a raw
px/rem with no `var()`** — `margin-top:2.75rem` (12×), `display:flex; gap:12px` (5×),
`gap:40px` / `gap:32px`, `flex:1 1 160px`, `width:120px`, `margin:0 0 16px`, `max-width:368px`.
Those are hardcodes in the least overridable place in CSS, and every one of them is a mode-override
that cannot happen. **That number — 88 — is the census's actionable answer**, not the 596.

### Which generator or skill emits them

30 `.py` files under `knowledge/` construct a `style=` string. By volume:

| file | `style="` | what it emits |
| --- | --- | --- |
| `knowledge/_render/gen_nio_dash_v2.py` | 25 | dashboard fixture chrome |
| `knowledge/_render/gen_nio_dash.py` | 23 | same, v1 |
| `knowledge/_validate_state_contrast.py` | 22 | probe markup (gate-internal, not shipped) |
| `knowledge/_review/_gen_dataviz_charts.py` | 17 | review-page charts |
| `knowledge/_gate_inline_style_parse.py` | 17 | its own selftest fixtures |
| `knowledge/_build_trace_dossier.py` | 10 | dossier HTML |
| `knowledge/_validate_no_hardcode.py` | 8 | selftest fixtures |
| `knowledge/gen_gallery.py` | 1 | `gen_gallery.py:68` — the `<svg … style="position:absolute">` sprite block, which alone accounts for the 74 `position:absolute` hits in the snippet corpus |
| `knowledge/gen_dashboard.py` | 1 | `gen_dashboard.py:1309` — `<div class="board" style="max-width:none">` |

Most of the count in that column is **gate selftest fixtures and probe markup**, which never ship.
The two that reach shipped artefacts are `gen_gallery.py:68` (one line, 74 occurrences, harmless —
a 0×0 hidden sprite) and `gen_dashboard.py:1309` (a genuine one-off override).

**The bento generators are the counter-example, and they are emphatic.** Four of them refuse inline
dials in their own source comments:

- `knowledge/_render/gen_bento_roles_217.py:396` — *"INSTANCE PARAMETER SETS — declared rules, never a `style=""` attribute"*
- `knowledge/_render/gen_bento_canon_217.py:334` — same line
- `knowledge/_render/gen_bento_matrix_217.py:288`, `:1804`, `:1886`, `:2028` — *"one declared rule per stop — never a `style=""` attribute"*; *"an inline custom property … would render nothing"*
- `knowledge/_render/gen_foundations_217.py:985` — *"The dials are declared as RULES, never a `style=""` attribute"*

And `template-dashboard-bento.meta.json` → `antiPatterns`:

> "Do not set `--bento-gutter` with a `style=""` attribute. An inline custom property is invisible
> to every instrument that reads the stylesheet against the document (canon says so in as many
> words)."

**Measured compliance: `grep -rho 'style="--bento[^"]*"' --include=*.html .` → zero hits across the
whole repo.** The rule is stated in five places and obeyed everywhere. So the *layout-dial* class
of inline style — the one that would actually hurt — does not exist here.

### Is there an existing gate or ruling?

**Gate: yes, two, and one is advisory.**

- `knowledge/_gate_inline_style_parse.py` — *"⬛ ADVISORY AT BIRTH (#221). The FIRST parser in the
  static leg."* Runs `html.parser` over `style=""` attributes, narrowly, on
  `knowledge/_proforma/*.html`. It exits 0 unless `--strict`, and its own docstring says *"nothing
  in this repo passes `--strict`."* Promotion is explicitly Dave's.
- `knowledge/_validate_no_hardcode.py` — **blocking**, and it reads `style=""` attributes since
  #221 (`_validate_no_hardcode.py:72` — `re.findall(r'style="([^"]*)"', html)`). Its docstring
  records the hole being closed: *"L1's finding 12 planted `<div style="padding:13px;…">` … and the
  BLOCKING DEF-004 gate exited 0 — because `_validate_no_hardcode.styles()` read `<style>` blocks
  and nothing else."*

  ⚠ But its population is **pro-formas**, not snippets. That is why the 88 raw-value inline styles
  in `knowledge/snippets/` are not red today: they are outside the gate's window, not inside it and
  forgiven. Widening DEF-004's population to the snippet corpus is the single highest-value,
  lowest-cost move this census suggests — and it is a scope change, so it is Dave's.

**Ruling: no.** `grep -in "inline" knowledge/_rulings.json` returns 15 hits, none about inline
styles (they are "inline notifications", "inline comments", "the wrap runs inline"). `grep 'style='`
returns **0**. Across 622 rulings there is **no ruling on inline styles at all** — only the
generator-comment convention above and the template's antiPattern. The convention is strong,
consistent and obeyed; it has simply never been inscribed.

---

## 8. §9 decisions — already ruled vs. genuinely open

### Already ruled (in whole or in part) — 3 of 5

**Q1 — theme-aware dashboard defaults and instance dial selection.** The **vocabulary and
governance are fully ruled**; only the delivery is missing.
- s217-D2 rules the per-theme gutter token (supercharge + mono 0, legacy + console 24).
- s219-D1(3)(4)(5) rules the twelve exports as shipped defaults, the stop set
  `{1,2,4,16,24,40}`, and the dashboard two-dial split (main 24/40/40/24, sub 4/4/4/2).
- s219-D3(1) rules the three permission levels; s219-D3(2) rules options-come-in-chords with a
  validator that refuses illegal combinations.
- **Open:** nothing *builds* the generation arm. `_bento_edit_rails.json` says so itself
  (`$groundwork_only`). **And the two ruled numbers contradict each other in 3 of 4 themes** (see
  Headline). That contradiction is genuinely unresolved and is the thing to put to Dave — not
  "what should the mechanism be", but "which of these two ruled numbers governs a dashboard
  wall's outer gutter, and does the other one need re-ruling?"

**Q2 — what constrains the four-column lead rule.** **Ruled, and the report under-credits it.**
s249-D5 ("No ragged layouts", Dave verbatim) is the constraint; s251-D1/D2 and s247-D3 authorise
the rule; s217-D2 rules the bands (1100→3, 820→2, 520→1). The #251 probe measured 4/4/4 at
1440/1100/820. **Genuinely open:** only the sub-820 envelope — the 520px and 390px clipping the
report measured sits below every band the ruling tested. That is a narrow question ("what happens
to a four-up KPI lead below 820 container px?"), not the open-ended policy review §9 implies.

**Q4 — which checks block, and how exceptions are reviewed.** **Ruled in substance.** The posture
already exists: `_gate_inline_style_parse.py` is ADVISORY-at-birth with promotion named as Dave's;
`run-gates.py --baseline` separates new failures from debt; SKILL.md:36 states the
yours/not-yours rule; SKILL.md:133 requires exceptions to be *"an explicit, documented exception
marker"*. A new checker should adopt this, not invent a second posture. **Open:** only whether the
specific new layout checks are mature enough — a per-check judgement, not a missing policy.

### Genuinely open — 2 of 5

**Q3 — where composition-level layout relationships live.** **Open, and there is a named schema
gap waiting for it.** `template-dashboard-bento.meta.json` → `$composesNote`:

> "`relationships` is a CLOSED shape in meta.schema.json (livesInside · mustNotNeighbour ·
> commonPatterns · triggeredBy) and has no seat for 'the components this organism is assembled
> from'. ⬛ THAT IS A REAL GAP FOR LAYER 2 … composition is the defining edge of a template, and
> the graph cannot currently express it. … Adding a `composes` edge type is a schema change and is
> Dave's."

s245-D7 added `groupsWith` to the schema for *grouping*; the *containment/edge-sharing*
relationships the report's checker needs have no home. The 12-entry `$composes` array is carried
as a `$`-prefixed escape hatch precisely because it cannot be a real edge. **This is the decision
with the most existing groundwork and the clearest shape.**

**Q5 — supported status of the distributed bento template, and consumer discovery.** **Open, and
the report understates it.** The meta says PROPOSED / NOT REGISTERED, `component-types.json` has no
entry, `_rulings.json` has 14 mentions but none that ratifies it — and `showroom/index.json`, the
one surface the skill tells builders to search, says `beta`. Two decisions are needed, not one:
1. the template's actual status (Dave's eye, owed since #231, plus four `$awaitingDave` items
   including the dark page ground at 1.00:1 contrast);
2. whether `showroom/index.json` gains a status value that can say "proposed" — because today the
   generator globs every snippet into the index and stamps it `beta` regardless.

### One decision §9 does not list, and should

**The `layout/bento/gutter` ÷ `dashboard.mainSpacing` contradiction.** s217-D2 and s219-D1(5) are
both ruled, both from Dave's own tuner exports, and they disagree for mono (0 vs 40), console
(24 vs 40) and supercharge (0 vs 24). Any implementation of Q1 must first be told which one wins.
Building the generation arm without answering this would harden the contradiction into code.

---

## What could not be checked

- **Every runtime claim.** No browser was available in this lane and none was used. Computed
  values, the 24px/4px measurements, the clipping widths at 520/390px, the dialog focus timing and
  the shared x=32 page frame are all taken as reported. Only their *source-side explanations* were
  tested.
- **The gate log itself.** No gate and no generator was run (instructed, and correct). The 33/8
  split is verified as *arithmetically consistent with v1.0.13's 41 RUNNABLE gates*; whether those
  specific eight are the ones that fail, and what they say, is unverified here.
- **The test-bed artefacts.** `screens/hsbc-ceo-banking.canon.html`, `.test.cjs`,
  `artifacts/hsbc-ceo/*.json|log` and `knowledge/_screen-gate/hsbc-ceo-banking.canon.md` are on
  Dave's work machine, not in this tree. All §2.1 evidence rows pointing at them are untested.
- **`role_defaults_219.py --table`.** Not executed (it is a generator). Its values were read
  instead from `_bento_edit_rails.json`, which declares itself generated from
  `gen_foundations_217.ROLE_DEFAULTS` and is asserted by selftest to equal a fresh generation.
- **The 3 zero-subject passes.** The runner's zero-population warning exists and was read at
  `run-gates.py:274`; *which* three gates graded zero on that run cannot be known without the log.

---

## Bottom line

The GPT agent was careful, honest about its limits, and correct on the facts it could reach from
inside a test bed. Its five §9 questions are worth answering — but **three are already ruled and
need implementing rather than deciding**, and the two that are genuinely open (Q3 composition edges,
Q5 template status) both have groundwork already laid and named in our own metadata.

The report's one real analytical miss is the same miss twice: it read `0` and `40/4` as defects,
when both are ruled values. Correcting that framing turns a vague "reconcile theme-default
delivery" into a single answerable question — *which ruled number governs the outer gutter of a
dashboard wall?* — and that question, not a new checker, is the unblocking decision.

On inline styles: the volume is real but the shipped library is largely fine (62% defensible, and
zero inline layout-dials repo-wide against a rule stated in five places). The actionable debt is
**88 raw-value inline styles in the snippet corpus that DEF-004 does not currently look at**, and
the fix is a population widening, not a new gate.
