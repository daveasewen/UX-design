# Receipt — #210 WAVE 5 · Lane B · the three page TEMPLATES

**Lane:** B (Opus) · **Session:** #210 · **Date:** 2026-08-20
**Brief:** `notes/_briefs/2026-08-20-210-wave5-layer2-p2-fanout-brief-v1.md` (THE JOB, LANE B)
**Members:** Template — dashboard (itinerary row 104, P2) · Template — list / index (row 105, P2) ·
Template — detail (row 106, P2). All three are class `layer-2`, derived `NO-ARTEFACT-CLASS`.

> ⛔ **NOTHING IN THIS RECEIPT IS A RULING.** Every fintech, domain and structural semantic below is
> PROPOSED and is Dave's (the Kpi-tile precedent, `s182-D2`). No registry, `MIGRATED_SNIPPETS`,
> `CATEGORIES`, `component-types.json`, `canon.css`, `gen_showroom.py`, `_rulings.json` or git
> operation was touched. This lane created **NEW FILES ONLY** and edited **no existing file** — and
> that matters more than usual here, because the lane found three defects in GATED components and
> repaired none of them at source.

---

## 0 · THE HEADLINE: FIVE DEFECTS, FOUR OF THEM IN GATED COMPONENTS, ALL FOUND BY DRIVING

Every gate was green over every one of these before a browser was opened. The two that matter most
are the same shape as [[dangling-dataviz-var-renders-silent-black]] and [[no-gate-parses-the-artefact]]:
**a gate that reads the SOURCE TEXT cannot see what the browser does with it.**

| # | defect | where it lives | gates over it | status |
|---|---|---|---|---|
| 1 | **`.l-split` never collapses** — `container-type` on an element does not make that element queryable | ⛔ **GATED `Layout-utilities`** | all green | worked around here · **parent REPORTED, not patched** |
| 2 | **Chart bars painted solid BLACK in both themes** — a dangling `--data-series-1` | this lane's own composition | all green | **FIXED** + a mutation-controlled probe written |
| 3 | **ds-005 live: `text-box-edge:text text` LOSES the cascade**, clipping 3.88px of every descender | ⛔ **GATED `Timeline` + `Document-row`** | descender gate GREEN | two-class form applied here · **parents REPORTED, not patched** |
| 4 | **Row titles crushed to 47px by their own chips** — the #209 Lane A finding repeating | this lane's own composition | all green | **FIXED** with #209's own repair |
| 5 | **Namespacing a borrowed rule changed its weight** and un-centred `.dg-empty` | this lane's own composition | all green | **FIXED** |

**And the one that says the most about Layer 2:** defect 2 is a class this repo has already met and
already priced — but it arrived here by a NEW ROUTE. A template inherits a **var contract** from
every component it composes, and **nothing checks that it carried them all.** The h-bar chart
specimen was swapped for the column specimen mid-build; the theme block still carried the h-bar's
`--data-series-3` and not the column's `--data-series-1`; `fill:var(--undefined)` falls back to the
SVG initial value, **black**, in silence. Composition multiplies this risk by the number of
components composed.

---

## 1 · FILE LIST — six new files, plus this receipt

| # | path | bytes |
|---|---|---|
| 1 | `knowledge/snippets/Template-dashboard.reference.html` | 75,072 |
| 2 | `knowledge/components/template-dashboard.meta.json` | 15,786 |
| 3 | `knowledge/snippets/Template-list-index.reference.html` | 66,264 |
| 4 | `knowledge/components/template-list-index.meta.json` | 15,981 |
| 5 | `knowledge/snippets/Template-detail.reference.html` | 46,650 |
| 6 | `knowledge/components/template-detail.meta.json` | 16,044 |
| 7 | `notes/_receipts/2026-08-20-210-wave5-laneB-templates.md` | this file |

**No existing file was edited.** No `intent` field was authored (W-58 parked). Renders and probe
scripts live OUTSIDE the repo — **`(NON-REPO: the session outputs folder, `wave5-laneB/` — 18 PNGs
(3 pages × 2 themes × 3 widths), `drive.py`, and `Template-*.json` measurement dumps)`** per
`s191-D2` home-or-declare. They are working artefacts, not deliverables. The three build helpers
`/var/tmp/lb/{inject,diffproof,ds005}.py` are scratch and do not survive the session; **every probe
in the claim table below is written out in full so it can be re-run without them.**

---

## 2 · CLAIM TABLE — every claim carries a probeable token (`s182-D1`)

| # | claim | probe — re-runnable, exactly as written | verdict |
|---|---|---|---|
| 1 | The leading-trim block is the CURRENT one, byte-identical to Command-palette line 36 (328 chars) in all three | `python3 -c "cp=open('knowledge/snippets/Command-palette.reference.html').read().split(chr(10))[35]; print(len(cp), all(cp in open(f).read() for f in ['knowledge/snippets/Template-dashboard.reference.html','knowledge/snippets/Template-list-index.reference.html','knowledge/snippets/Template-detail.reference.html']))"` → **`328 True`** | ✅ |
| 2 | The AUTO-TOKENS alpha ramp is byte-identical to Meter's generated block in all three | `python3 -c "m=open('knowledge/snippets/Meter.reference.html').read().split(chr(10)); a=m.index([l for l in m if 'AUTO-TOKENS START' in l][0]); b=m.index([l for l in m if 'AUTO-TOKENS END' in l][0]); blk=chr(10).join(m[a:b+1]); print(all(blk in open(f).read() for f in ['knowledge/snippets/Template-dashboard.reference.html','knowledge/snippets/Template-list-index.reference.html','knowledge/snippets/Template-detail.reference.html']))"` → **`True`** | ✅ |
| 3 | The dashboard's chart SVG is byte-identical to Chart-bar's column specimen but for the `dv-fit` class and the two hidden sort views | `python3 -c "cb=open('knowledge/snippets/Chart-bar.reference.html').read().split(chr(10)); s0=[i for i,l in enumerate(cb) if 'Spend by category. Groceries 420' in l][0]; s1=[i for i,l in enumerate(cb) if i>s0 and l.strip()=='</g>'][0]; blk=chr(10).join(cb[s0:s1+1]).replace('class=\"dv-svg dv-fit\"','class=\"dv-svg\"'); print(blk in open('knowledge/snippets/Template-dashboard.reference.html').read())"` → **`True`** | ✅ |
| 4 | **339 borrowed selectors are declaration-identical to their source component's rule** for the same selector; 44 carry at least one declaration not in the source, and **every one of the 44 is named and explained in §5** | the full diff-proof script is reproduced in §6 of this receipt; run it and read the `MATCH` / `NEW` columns → **`TOTAL: 339 selector(s) proven declaration-identical, 44 carrying declarations not in the source`** | ✅ |
| 5 | **NO COLOUR IS INVENTED.** Every hex in all three theme blocks appears in the theme block of some source component | §6's part C, the theme-block UNION check → **dashboard `102 hex declaration(s) · 0 NOT FOUND`, list-index `82 · 0`, detail `62 · 0`** | ✅ |
| 6 | …and that check **CAN FAIL** — it is not an assertion | MUTATION CONTROL, driven: `sed -i 's/--rail:#E1E1E1;/--rail:#C0FFEE;/' knowledge/snippets/Template-detail.reference.html` then re-run → **`62 hex declaration(s) · 1 NOT FOUND` · `⛔ INVENTED COLOUR: --rail:#C0FFEE`**; restored from the backup and re-run → **`0 NOT FOUND`** | ✅ **MUTATION-CONTROLLED** |
| 7 | 4px-grid gate clean on all three | `python3 knowledge/_validate_grid.py knowledge/snippets/Template-dashboard.reference.html knowledge/snippets/Template-list-index.reference.html knowledge/snippets/Template-detail.reference.html` → *"GRID GATE PASS — all layout dimensions on the 4px grid (3 file(s))"* | ✅ |
| 8 | Type-composite gate clean on all three, and **the repo debt does not grow** | `python3 knowledge/_validate_type_composites.py <the three>` → *"TYPE GATE PASS — all component text bound to canon composites (3 file(s))"* · `advisory — 0 raw font decl(s) in demo-chrome scope`. Repo-wide: `python3 knowledge/_validate_type_composites.py` → *"TYPE GATE FAIL — **1097** violation(s) across 90/134 file(s). TYPE-001 ×31 · TYPE-002 ×1050 · TYPE-003 ×16"* — **the #203 measured baseline, UNCHANGED**. TYPE-002 contribution of this lane: **0**. | ✅ |
| 9 | Snippet/token gate clean, whole repo | `python3 knowledge/_validate_snippets.py` → *"snippet gate: 119 snippet(s), 0 failure(s)"* | ✅ |
| 10 | a11y gate: zero failures with all three present | `python3 knowledge/_validate_a11y.py` → *"a11y gate: 119 snippet(s), 0 failure(s), 249 warning(s), 439 note(s) · 998 controls + 209 marks measured · 107 mark(s) below 24"* | ✅ |
| 11 | Descender-clip gate passes | `python3 knowledge/_validate_descender_clip.py` → *"DESCENDER-CLIP GATE PASS — every truncating label is descender-safe (135 file(s))"* ⚠ **AND THAT PASS IS THE DEFECT — see claim 18.** | ✅ **but blind** |
| 12 | The three metas are schema-valid | `python3 knowledge/_probe_registry/probe_meta_schema.py --check` → *"P-1 meta-schema sweep: 120 meta(s) checked · 0 finding(s) · 1 exempt failure(s) (EXAMPLE-button.meta.json)"* · `PROBE P-1 — findings=0` | ✅ |
| 13 | Duplicate-ID probe clean | `python3 knowledge/_probe_registry/probe_dup_ids.py --check` → `PROBE P-2 — findings=0` | ✅ |
| 14 | **The real HSBC cut rendered — asserted with CONTROLS, not `fonts.check()`** | headless Chromium, 40px `Handgloves 12345` canvas measurement: `HSBC_MtUnivers_Latin` **346.88** · `"Univers Next HSBC"` **346.88** · `"Univers Next for HSBC"` **346.88** · `DejaVu Sans` **375.39** · nonexistent face **301.07**. Both aliases land on the target and NEITHER lands on the fallback — the assertion the runbook prescribes | ✅ **DRIVEN** |
| 15 | **Zero horizontal page overflow, all three pages, both themes, all three widths** | driven at 1400 / 820 / 420 CSS px: `document.documentElement.scrollWidth - clientWidth` → **0** in all **18** runs | ✅ **DRIVEN** |
| 16 | **The responsive collapse is real and was measured, not asserted** | driven `getComputedStyle(...).gridTemplateColumns` track counts. Dashboard KPI board: **4 → 3 → 1** tracks at 1400 / 820 / 420. Dashboard + detail split: **2 → 2 → 1**. Wide fixed-canvas regions scroll INSIDE themselves rather than the page: at 420 the chart stage reports `scrollWidth 580 / clientWidth 338 → scrolls true`, the grid `640 / 386 → scrolls true`; at 1400 both report `scrolls false` | ✅ **DRIVEN** |
| 17 | **No dangling CSS var anywhere in the three files** — the #184 class, asked in the consumer's grammar | driven probe: collect every `var(--x)` named in `document.styleSheets`, report any that no element in the document resolves → **`DANGLING []` in all 18 runs**; ground truth beside it, `getComputedStyle(rect.dv-series).fill` → **`rgb(118, 102, 130)`** = `#766682` = `data/series/1`, in BOTH themes | ✅ **DRIVEN** |
| 18 | …and that probe **CAN FAIL**, and it reproduces the exact defect | MUTATION CONTROL, driven in-page: inject `rect.dv-series{fill:var(--data-series-NOPE)}` → before `{dangling: [], fills: ['rgb(118, 102, 130)']}`, after **`{dangling: ['--data-series-NOPE'], fills: ['rgb(0, 0, 0)']}`** — dangling detected AND the silent black reproduced | ✅ **MUTATION-CONTROLLED** |
| 19 | ⛔ **`_validate_binds_resolve.py` check D FAILS for all three — DECLARED, not hidden** | `python3 knowledge/_validate_binds_resolve.py` → *"binds-resolve gate: 119 snippets (119 with manifests, 1765 vars) · 116 metas (116 binds addresses) · 108/119 canon blocks · 11 failure(s)"*, naming *"Template-dashboard.reference.html: no .cn-template-dashboard block in canon.css — project_canon projection is silently OFF for this snippet"* and the same for `-detail` and `-list-index` (+ 5 sibling-lane files) | ⛔ **CONDUCTOR'S** |
| 20 | ⛔ **`_validate_kg.py` FAILS — the new metas name contexts and patterns the node registry has never seen** | `python3 knowledge/_validate_kg.py` → *"_nodes-pattern.json DRIFTED … _nodes-context.json DRIFTED"*; and `python3 -c "import json;s=json.dumps(json.load(open('knowledge/components/_nodes-context.json')));print([c for c in ['business-banking-overview','account-overview-screens','payments-screens','payment-detail-screens','statement-archive'] if c not in s])"` → **all five absent** | ⛔ **CONDUCTOR'S** |

---

## 3 · THE FIVE DEFECTS, IN FULL — every one found by LOOKING or by MEASURING, none by a gate

### D1 ⛔ `.l-split` NEVER COLLAPSES — and it never collapses in the GATED PARENT either

`Layout-utilities`' split primitive declares `container-type:inline-size` **on `.l-split` itself**
and then tries to collapse it with `@container (max-width:760px){ .l-split{...} }`. That rule can
never match. `container-type` makes an element a query container **for its descendants**; a
`@container` rule resolves against an element's nearest **ancestor** container, and an element is
never its own. The parent's demo caption says the split *"has already collapsed"*. It has not.

| probe, all driven at #210 | result |
|---|---|
| `Layout-utilities.reference.html` @ 1400px — the split inside its own 394px `.frame.narrow` | `grid-template-columns: **90px 280px**` — the rail keeps its full 280px, the content column is squeezed to **90px** |
| `Layout-utilities.reference.html` @ 420px — the top-level split | `**44px 280px**` — a forty-four-pixel content column |
| this dashboard @ 420px, BEFORE the fix | chart stage `clientWidth **26px**`; the analysis paragraph `clientWidth **26px**`. **Unreadable on a phone, with GRID, TYPE, SNIPPETS, A11Y and DESCENDER all green** |
| **MUTATION CONTROL** — set `container-type:inline-size` on the split's PARENT, re-read | `**394px**` — one column. **The rule is correct; its container was missing** |

**Repair here:** composition rule 12, `.tpl-split-host{container-type:inline-size}`, a wrapper around
the split. **`Layout-utilities` is gated and was NOT edited.** ⬛ The real repair is Dave's and is one
of two: give every split a host (what this template does), or move `container-type` off `.l-split`
onto a wrapper **inside the primitive**, so consumers cannot get it wrong. The second is better and
is a one-line change to a gated file, which is why it is not this lane's.

⚠ **The same class bites `Document-row`'s and `Timeline`'s own `@container` reflow rules**, which is
why both templates supply hosts (`.tpl-list-host`, `.tpl-split-host`).

### D2 ⛔ THE CHART BARS PAINTED SOLID BLACK, IN BOTH THEMES

Caught by looking at the dark render: every bar in "Where the money went" was black on the near-black
page, and black on white in light. Cause: the column specimen fills every rect with
`var(--data-series-1)`; the theme blocks carried only `--data-series-3`, a leftover from the h-bar
specimen it had replaced. **`fill:var(--undefined)` does not fall back to the previous value — it
falls back to the SVG initial value, BLACK, in silence.**

This is [[dangling-dataviz-var-renders-silent-black]] (#184, mutation-proven, "13 gates blind")
reproduced at **composition** time. **The new thing it says:** a template inherits a var contract
from *every* component it composes, and nothing checks that it carried them all. Composition
multiplies the exposure by the number of components.

**Repair:** `--data-series-1:#766682` added to both theme blocks (Chart-bar's own value, byte-copied)
and bound to `data/series/1` in the manifest. **Plus a probe** (claims 17/18) that asks the question
in the browser's grammar and is mutation-controlled both ways.
⬛ The general repair — a **var-resolution gate that parses the artefact** — is already the priced
candidate in `_DS-IMPROVEMENTS.md`. This lane adds a second live catch to its evidence and **did not
build the gate.**

### D3 ⛔⛔ ds-005 IS LIVE IN TWO GATED COMPONENTS, AND THE DESCENDER GATE CANNOT SEE IT

The brief's own do-not-rule list says: *"ds-005 is LIVE (trim specificity beats single-class
overrides): if a lock-up needs an override, use the two-class form **and MEASURE the computed
edge**."* Measured, in a real browser, on the gated parents as well as here:

| probe | computed `text-box-edge` | label box height |
|---|---|---|
| as shipped — single-class `.tl-title{text-box-edge:text text}` | `cap alphabetic` | **10.13px** |
| natural height of the same string, untrimmed | — | 14.00px |
| inline `text-box-edge:text text !important` | `text` | **18.00px** |
| **two-class** `.tl-line .tl-title{text-box-edge:text text}` | `text` | **18.00px** |
| trim off entirely (upper-bound control) | `cap alphabetic` | 14.00px |

**3.88px of every `g`, `y`, `p`, `q` and `j` is clipped** by the truncating label's own
`overflow:hidden`. Identical numbers in `Timeline.reference.html` itself and in `Document-row`'s
`.dr-title` / `.dr-meta`. `CSS.supports('text-box-edge','text text')` → **`true`**, so the value is
not being rejected: **the declaration is losing a cascade fight.**

★ **THE MECHANISM, NAMED.** The canon trim rule is
`:is(button,a,label,span,…,input[type=text],…):not(:has(svg))`. `:is()` takes the **highest**
specificity among its arguments — and that list contains **attribute selectors**
(`input[type=text]`), which are class-level. So the whole `:is()` weighs `0-1-1`, `:not(:has(svg))`
adds an element, giving `0-1-2`. A single class is `0-1-0`. **The trim rule outweighs every
single-class override in the repo by construction, because of one attribute selector buried in a
fifty-item list.**

⛔ **And `_validate_descender_clip.py` passes all of it** — it PASSES `Timeline`, and it passes these
three templates — because it is a **textual** check: it greps for the string `text-box-edge: text
text` on a truncating selector and calls the label safe. **It never asks the browser whether the
declaration won.** That is the [[no-gate-parses-the-artefact]] shape exactly: the first gate must
parse in the **consumer's** grammar.

**Repair here:** the two-class form, in the two templates that carry truncating labels. Re-measured
after: box `18.00px`, computed edge `text`. **`Timeline` and `Document-row` are gated and were NOT
edited.**

### D4 ⛔ THE ROW TITLES WERE CRUSHED BY THEIR OWN CHIPS — the #209 finding, repeating

`Document-row`'s `.dr-line` is a **non-wrapping** flex row whose only shrinkable item is
`.dr-title`. These templates add a status chip and (in the list) an amount to the same line — content
the parent never had — and both are `flex:none`. **Measured at 420px before the fix: title elements
47–68px wide**, i.e. "Meridian Supplies Ltd" reduced to three letters and an ellipsis. In the detail
template's 280px rail the same crowding cut "Remittance advice" to **71px at full desktop width**.

★ **This is #209 Lane A's third finding verbatim** — *"THE PAYEE WAS BEING CRUSHED BY ITS OWN CHIPS"*
(`notes/_receipts/2026-08-20-209-wave3-laneA-fintech-rows.md` §3.3) — and it repeats because the
cause is **structural, not local**: adding a `flex:none` sibling to a non-wrapping flex row always
crushes the one shrinkable item. **The repair is that receipt's repair**, scoped by `:has()` so it
reaches only rows carrying the extra content; a plain Document-row row is left exactly as its parent
draws it.

⬛ **A candidate for the twice-caught promotion rule (W-45/W-48):** this is now n=2 in two consecutive
sessions, and it is mechanically probeable — *"a `flex-wrap:nowrap` row containing more than one
`flex:none` child and exactly one shrinkable text child"*. Naming it as a candidate; **promotion is
not this lane's.**

### D5 ⛔ NAMESPACING A BORROWED RULE CHANGED ITS WEIGHT

`Data-grid` declares `th,td{text-align:left}` (specificity `0-0-1`), which its own `.dg-empty`
(`0-1-0`) beats. This template **namespaced** the cell rule to `.dg th,.dg td` so a table elsewhere
on the page could not inherit it — and that raised it to `0-1-1`, which now **beats** `.dg-empty`.
The empty result's message and its recovery button rendered **flush left inside a centred panel**.

**Repair:** match the scope (`.dg td.dg-empty`), not `!important`. Measured after: `td` centre
**700.0px**, button centre **700.0px**.

★ **The lesson is a composition lesson, not a CSS one: namespacing a borrowed rule changes its
weight, so everything that used to beat it must be re-checked.** There is no gate for this.

---

## 4 · WHAT WAS DRIVEN

Headless Chromium (`chromium_headless_shell`, `--no-sandbox --disable-dev-shm-usage --disable-gpu`),
each file loaded with `goto("file://…")` per `_RUNBOOK-render-verify.md`, real HSBC cut asserted with
the three-way control probe (claim 14), **`data-theme` toggled live**, **18 full-page screenshots
(3 pages × light+dark × 1400/820/420) taken and LOOKED AT**, plus scripted measurement of: computed
grid tracks, page and per-region overflow, effective hit targets via `document.elementFromPoint`,
every type composite's computed size/weight/family, every clipped text node, every painted
foreground/background pair, chart and sparkline geometry, and CSS-var resolution.

**Type, measured rather than assumed** (light-1400, dashboard) — every composite in use resolved to
its canon ramp value in the real face: `t-cm-legal` 12/400 · `t-cm-caption` 14/400 · `t-cm-ctl-14`
14/500 · `t-cm-figure-6` 14/400 · `t-ed-body-small` 14/400 · `t-cm-label` 16/400 · `t-cm-input`
16/400 · `t-cm-figure-5` 16/400 · `t-cm-button` 16/500 · `t-ed-body` 16/400 · `t-cm-section-label`
20/500 · `t-cm-figure-4` 32/400 · `t-ed-heading-2` 28/300 · `t-cm-chart-label` 12/500 ·
`t-cm-chart-value` 12/500 — all `"Univers Next HSBC"`.

**Hit-tested, not assumed:** clicking the centre of a `.drow` lands on the row's stretched
`.dr-title` link, and the effective target is the **278×76** row box, not the 12px-tall `<a>`.
Buttons, tabs and pager cells hit-test to themselves at 44–48px.

---

## 5 · THE 44 SELECTORS THAT CARRY A DECLARATION NOT IN THE SOURCE — every one named

Claim 4's `NEW` rows, grouped. **None of them is a re-drawn atom.**

**(a) Same value, fewer indirections — 6 selectors.** `.btn{height:44px; padding:0 20px}` where
Button writes `height:var(--h); padding:0 var(--pad-x)` with `--h:44px; --pad-x:20px`.
`.btn.primary:hover` where Button writes `calc(var(--alpha-68) * 100%)` and this writes `68%`.
`.dgsearch:hover{background:var(--hover)}` where Data-grid uses a separate `--fhover` of the same
hex. `.seg{border:1px solid var(--fborder)}` where View-options calls the same hex `--border`.
`.summary__k` where Summary's `--muted` (text/secondary) is expressed as text/default at `alpha/60`,
the idiom Kpi-tile and Data-grid already use. `.pg [aria-current]{border-color:var(--currentbd)}`
where Pagination calls the same token `--current-bd`. ⬛ **Every one of these is a VAR-NAME collision
avoided.** Composing eight components means eight vocabularies; where two sources name the same token
differently, one name had to win.

**(b) `--move` / `--spring` / `--press` transitions re-pointed — 3 selectors.** `.seg`, `.seg .ind`,
`.seg button` and `:root` use `--move` where View-options declares its own unnamed `--ease` at the
same `220ms cubic-bezier(.4,0,.2,1)`. Renamed because the page already has a 140ms `--ease` from
Kpi-tile; **two components disagreeing about what `--ease` means is the collision class again.**

**(c) `s210-D3` width overrides — 3 selectors.** `.dg{width:100%}` (Data-grid ships
`var(--demo-width,760px)`), `.tl{width:100%}` (Timeline ships `var(--demo-width,460px)`), and
`body{padding:0}` (the sources are specimen sheets with `2.5rem` padding; a template is a page).
**Each is the container asserting width, which is what `s210-D3` licenses a template to do.**

**(d) The declared defect repairs — 5 selectors.** `.spark-inline .dv-base` (the `--grid-alpha`
collision rename, §7), `.tl-line{flex-wrap:wrap}` + `.tl-amount{margin-left:0}` inside the container
query (D4's class, pre-empted in the timeline), `.tablist{overflow-x:auto}` (Tabs' overflow is a
JS-driven "More" menu this page does not host — scrolling is the honest static answer), and
`.summary__row--total{border-top}` (Summary's total row has no rule; this page's total is the last
line of a payment and reads as a sum).

**(e) Theme blocks and `:root` — 9 selectors (3 per file).** A template's theme block is the **union**
of the theme blocks of the components it composes, so **no single source can contain all of it**.
That is why the honest claim is claim 5's per-value UNION check, which is mutation-controlled: **0 of
246 hex declarations across the three files is absent from every source.**

**(f) Genuinely new composition rules — 18 selectors.** Thirteen on the dashboard, nine on the
list-index, eight on the detail, minus overlaps. Each is a **relationship** — page frame, header
rule, actions to the far end, panel head rhythm, rail stack, container host, panel alignment,
selection bar, pager row — and none describes an atom's appearance. **If a rule ever describes what
an atom LOOKS like, something is being re-drawn.**

**(g) Demo chrome — the rest.** `.demo-bar`, `.demo-h`, `.demo-note`, `.sr-only`,
`.visually-hidden`. Delete every one and all three pages still work.

---

## 6 · THE DIFF-PROOF SCRIPT, WRITTEN OUT SO IT CAN BE RE-RUN

Save as `diffproof.py` at the repo root and run `python3 diffproof.py`. It produced claims 1–6.

```python
#!/usr/bin/env python3
"""Diff-proof every borrowed region of the three Lane-B templates against its SOURCE component.
BYTE = byte-identical to a named span of the source.  DECL = every CSS declaration in the
template's rule is present verbatim in the source's rule for the same selector."""
import re, io
R = ''   # repo root, with trailing slash
def txt(p): return io.open(R + p, encoding='utf-8').read()
FONT = re.compile(r'^(font|font-family|font-size|font-weight|line-height)\s*:', re.I)
def rules(css):
    out = {}
    for m in re.finditer(r'([^{}/]+)\{([^{}]*)\}', css):
        sel = ' '.join(m.group(1).split())
        out.setdefault(sel, []).extend(d.strip() for d in m.group(2).split(';') if d.strip())
    return out
def style_of(p): return '\n'.join(re.findall(r'<style>(.*?)</style>', txt(p), re.S))
def strip_comments(c): return re.sub(r'/\*.*?\*/', '', c, flags=re.S)
TARGETS = ['knowledge/snippets/Template-dashboard.reference.html',
           'knowledge/snippets/Template-list-index.reference.html',
           'knowledge/snippets/Template-detail.reference.html']
SOURCES = ['Layout-utilities','Kpi-tile','Stat-card','Summary','Data-grid','Pagination',
           'Document-row','Timeline','Tabs','Button','Breadcrumbs','View-options',
           'Status-indicator','Chart-bar','Headers','List-items']
src_rules = {s: rules(strip_comments(style_of('knowledge/snippets/%s.reference.html' % s))) for s in SOURCES}

print('=== A · BYTE-IDENTICAL REGIONS ===')
cp = txt('knowledge/snippets/Command-palette.reference.html').split('\n')[35]
meter = txt('knowledge/snippets/Meter.reference.html').split('\n')
i0 = next(i for i, l in enumerate(meter) if 'AUTO-TOKENS START' in l)
i1 = next(i for i, l in enumerate(meter) if 'AUTO-TOKENS END' in l)
auto = '\n'.join(meter[i0:i1 + 1])
cb = txt('knowledge/snippets/Chart-bar.reference.html').split('\n')
s0 = next(i for i, l in enumerate(cb) if 'Spend by category. Groceries 420' in l)
s1 = next(i for i, l in enumerate(cb) if i > s0 and l.strip() == '</g>')
chart = '\n'.join(cb[s0:s1 + 1]).replace('class="dv-svg dv-fit"', 'class="dv-svg"')
for t in TARGETS:
    s = txt(t)
    print('  %-52s trim(328ch)=%s  auto-tokens=%s  chart-svg=%s' % (t.split('/')[-1],
          cp in s, auto in s, 'n/a' if 'dv-svg' not in s else str(chart in s)))

print('\n=== B · DECLARATION-LEVEL PROOF, per borrowed selector ===')
tot_m = tot_x = 0
for t in TARGETS:
    tr = rules(strip_comments(style_of(t)))
    print('\n  --- %s ---' % t.split('/')[-1])
    for sel, decls in sorted(tr.items()):
        base = sel.replace('.dg ', '').replace('nav.tpl-crumbs', 'nav').replace('.tpl-crumbs ', '')
        # EXACT selector match only, then the de-namespaced form. A loose matcher (endswith)
        # produced false "NEW" rows by pairing `.btn:focus-visible` with a bare `:focus-visible`.
        hits = [(n, r) for n, rr in src_rules.items() for k, r in rr.items() if k == sel] \
            or [(n, r) for n, rr in src_rules.items() for k, r in rr.items() if k == base]
        if not hits: continue
        name, srcdecls = max(hits, key=lambda h: sum(1 for d in decls if d in h[1]))
        missing = [d for d in decls if d not in srcdecls]
        droppedfont = [d for d in srcdecls if d not in decls and FONT.match(d)]
        if not missing:
            tot_m += 1
            print('    MATCH  %-46s <- %s%s' % (sel[:46], name,
                  (' · DROPPED-FONT[%s]' % ', '.join(droppedfont)) if droppedfont else ''))
        else:
            tot_x += 1
            print('    NEW    %-46s <- %s · not-in-source: %s' % (sel[:46], name, '; '.join(missing)[:150]))
print('\n  TOTAL: %d selector(s) proven declaration-identical, %d carrying declarations not in the source'
      % (tot_m, tot_x))

print('\n=== C · THEME-BLOCK UNION PROOF ===')
HEX = re.compile(r'#[0-9A-Fa-f]{3,8}')
src_theme = {}
for s in SOURCES:
    for k, v in src_rules[s].items():
        if k.startswith('[data-theme') or k == ':root':
            key = (k.split(']')[0] + ']') if 'theme' in k else ':root'
            for d in v:
                m = HEX.search(d)
                if m: src_theme.setdefault(key, {}).setdefault(m.group(0).upper(), set()).add(s)
for t in TARGETS:
    tr = rules(strip_comments(style_of(t))); unknown = []; n = 0
    for k, v in tr.items():
        if not (k.startswith('[data-theme') or k == ':root'): continue
        for d in v:
            m = HEX.search(d)
            if not m: continue
            n += 1
            if not any(m.group(0).upper() in src_theme.get(kk, {}) for kk in src_theme):
                unknown.append(d)
    print('  %-52s %d hex declaration(s) · %d NOT FOUND in any source theme block'
          % (t.split('/')[-1], n, len(unknown)))
    for u in unknown: print('      ⛔ INVENTED COLOUR: %s' % u)
```

⚠ **The instrument's own blind spots, declared.** It compares CSS **text**, so it cannot see whether
a borrowed rule still WINS at runtime (D3 and D5 were both invisible to it). It matches by selector
STRING, so a renamed selector reads as new. It has no opinion about markup. **The browser drive is
not optional beside it — it is the half that catches what it cannot.**

---

## 7 · A SIXTH MEMBER FOR THE `W-59` LOCAL-VAR COLLISION LEDGER

`W-59` is open: *"rename the 5 ledgered local-var collisions to component-local names."* Composing
Kpi-tile and Chart-bar on one page surfaced a **sixth**, and the snippet gate caught it:

> `Kpi-tile`'s sparkline baseline reads `stroke-opacity:var(--grid-alpha)` where its own light block
> sets `--grid-alpha:.10`. `Chart-bar`'s `.dv-grid` reads **the same name** where its light block
> sets `1` (bound to `data/grid/alpha`). **Two components, one unbound local name, opposite values.**
> On one page, one of them silently wins.

Resolved here by giving the chart the **bound** name and renaming the spark's to
`--spark-base-alpha`, which is component-local and binds nothing. **Reported for `W-59`'s ledger;
`Kpi-tile` was not edited.**

★ **The general point for Layer 2:** a collision between two components' unbound local vars is
INVISIBLE until something composes them. **Templates are the first artefact class that composes
them, so templates are where this class becomes findable at all.**

---

## 8 · `$decisionsForDave` — NAMED, NOT SETTLED

**None of these is answered by construction. All are Dave's.**

**Q1 — ⛔ Is the Layer-2 artefact class right?** Every one of these ships as
`snippets/<Name>.reference.html` + `components/<slug>.meta.json`, because the one grammar keeps every
existing gate watching them for free. It is a PROPOSED convention stated once in the brief. If a
template is not a "component", it may want its own home — and then it is born ungated.

**Q2 — ⛔ `meta.schema.json` has no seat for COMPOSITION, and that is a real gap for Layer 2.**
`relationships` is a **closed** shape (`livesInside` · `mustNotNeighbour` · `commonPatterns` ·
`triggeredBy`). There is no edge for *"the components this organism is assembled from"* — which is
the **defining** relationship of a template. The list is carried as `$composes` so it is greppable
but does not pretend to be a graph edge. **Adding a `composes` edge type is a schema change.**

**Q3 — ⛔ The brief asks for a `layer` field; the schema forbids it.** Only `$`-prefixed additional
root keys are allowed, so the itinerary's layer value is carried as `$layer`. A first-class `layer`
field is a schema change.

**Q4 — ⛔ Table or list? (row 105, and the whole point of that page.)** The library holds both
answers and they are not interchangeable: a table carries relations BETWEEN rows (sort order,
page-scoped selection, a column you read downwards); a list carries one record and a tap target.
**Both are drawn, with the same filters, the same five records and the same pager, so the choice is
made by eye.** Whichever Dave picks, the other half of the file is deleted.

**Q5 — Should `Data-grid` consume `Pagination`?** Data-grid re-states the pager recipe internally as
`.pbtn`; `Pagination` is a gated component. The list template consumes the **component**; the
dashboard uses Data-grid's own, so both are visible on the same day. **A duplication, surfaced, not
adjudicated.**

**Q6 — Which control is a filter facet?** Drawn as native `<select>`s wearing Data-grid's own
`.dg-pp select` chrome. `Dropdown`, `Multi-select`, `Combobox` and `Date-range-picker` all exist and
all carry popup behaviour; hosting one would fork it. **The native select is an honest placeholder,
not a recommendation.**

**Q7 — ⛔ Should a template ship any JavaScript at all?** These three ship none. Consequence, stated
plainly: **the controls look live and are not.** The alternative is to import each source's engine,
which forks it. The third option — a template that `<iframe>`s or `<script src>`s its components —
is an architecture decision nobody has taken.

**Q8 — Where does a shell end and a template begin?** These are the CONTENT region of a page and
assume they sit inside a `<main>`. Rows 97/98/99 are the shells. **"A shell wraps a template" is
PROPOSED, not adjudicated** — and it interacts with the open `Sidebar-nav` vs `Navigations` overlap
(#203).

**Q9 — The page title steps 32 → 28.** `Headers`' `.display h1` is a raw `font:400 32px/1.1`.
Copying it would grow the TYPE-002 debt, which is shrink-only. 32px IS on the ramp
(`.t-cm-heading`) but that is a **single-line component** composite and a page title wraps, so the
deciding rule (wrapping ⇒ Editorial) sends it to `.t-ed-heading-2` at 28/36. **The step down is
visible and is Dave's.** The same trade appears on `Summary`'s value row (its raw `font-weight:500`
is not carried; emphasis moved to the total row via `.t-cm-ctl-16`) and on Pagination's and
Breadcrumbs' `[aria-current]` weight (carried by `.t-cm-ctl-16` / `.t-cm-ctl-14` in the markup).

**Q10 — ⛔ Three inherited target-size shortfalls, measured and NOT silently fixed.**
`Breadcrumbs`' `.crumb` links measure **39.4 × 10.1** — the leading-trim cap box IS the link box, so
a breadcrumb is a ten-pixel-tall target. `View-options`' `.seg` buttons are **40px** tall.
`Data-grid`'s `.dgs-clear` and `.fchip .x` are **24 × 24**. All three are the SOURCE components'
shipped geometry. ⚠ The a11y gate reports the first as *"UNMEASURED: no declared box
(layout-determined) and no hit-expander — this gate must not guess a size"*; **this lane measured it
in a browser.** Dave's to rule; a lane must not quietly enlarge a gated component's target.

**Q11 — Document titles ellipsize in a 280px rail.** At full desktop width, "Invoice INV-2026-0871"
renders at 134px with an ellipsis, and the full string exists only in the download button's
`aria-label`. That is `Document-row`'s designed truncation meeting `Layout-utilities`' 280px rail.
**Should the rail be wider when it hosts document rows, or should a truncated link carry a `title`?**

**Q12 — The KPI delta ARROW colour seat is still open, and is still not resolved here.**
`--up:#66CC8D` / `--down:#F6604C` are inherited verbatim from `Stat-card` via `Kpi-tile`, where the
file itself flags them as Dave's call at 1.980:1. **Carried, not touched.**

**Q13 — No monetary figure on any of the three pages is coloured.** `rag/success-ink` and
`rag/error-ink` are MONO ONLY (`s155-D1` / `s158-D2` / `s158-D3`). Binding them to money on a page
template would be ruling on Dave's behalf. **This is the #209 Lane A restraint, carried deliberately
across a whole page rather than a single row.**

**Q14 — Every status vocabulary is PROPOSED.** Completed / Pending / Failed / Reversed (grid);
Pending / Failed (list); Awaiting approval / Pending / Name matched / After approval (detail).
⛔ **"Failed" sits on the ERROR seat here**, which is a step beyond #209 Lane A's declared restraint
(that lane put "failed" on WARNING). It is on error because on a payments index a failed payment is
the thing you came to find. **That is a judgement, it is visible, and it touches the two-red law's
neighbourhood — so it is stated as a change of position, not slipped in.**

**Q15 — The detail page's four-part order** (identity → facts → history → documents) and the
decision to put documents in a **rail** rather than in a tab. Both PROPOSED.

**Q16 — Four KPIs, and which four.** Four is drawn because the auto-fill grid reflows 4 → 3 → 1 and
that is the collapse worth proving. Which four figures a business overview leads with is a product
decision.

**Q17 — ⛔ A status chip inside a stretched-link row swallows the click at its own coordinates.**
Hit-tested: `elementFromPoint` at the centre of the "Remittance advice" row lands on the chip's
`<span>`, because `Document-row` gives `.status` `position:relative; z-index:1` to raise it above the
`::after` overlay. Inherited, minor, **reported rather than patched.**

**Q18 — The h-bar chart cannot be used without its engine.** Composed first, rejected by looking:
its left category labels clip to "oceries" / "nsport" / "ousing" because `data-pl-fit` is a runtime
measurement. **A static composition must choose a specimen that does not need the engine** — worth
knowing before anyone composes a chart into a shell.

---

## 9 · WHAT STAYS UNPROVEN — declared, not smoothed

1. **⛔ CONSOLE, LEGACY AND SUPERCHARGE ARE UNPROVEN FOR ALL THREE.** `_validate_binds_resolve.py`
   check D fails: no `.cn-template-*` block exists in `canon/canon.css`, so theme-cascade projection
   is **silently OFF**. Only the light and dark legs authored in each snippet have been seen. Given
   [[four-themes-flexibility-is-the-requirement]], **this is the largest single gap in this
   delivery.** Projecting the blocks is the conductor's and is a precondition of any four-theme claim.
2. **`_validate_kg.py` FAILS.** The new metas name contexts and patterns the generated node
   registries have never seen (`business-banking-overview`, `account-overview-screens`,
   `payments-screens`, `payment-detail-screens`, `statement-archive` — all absent from
   `_nodes-context.json`). `gen_kg_edges.py` must be re-run. Shared generated files — **conductor's**.
3. **`_validate_state_contrast.py` NOT RUN** — a filtered run overwrites the tracked
   `_STATE-CONTRAST-AUDIT.md`, outside this lane's fence. Same declaration Lane P made at #204 and
   Lane A at #209. **Still owed.**
4. **No contrast ratio was RE-MEASURED.** Every colour pair on these pages is a pair a gated
   component already ships, and the a11y gate reports 0 failures over all 119 snippets — but this
   lane computed no ratios of its own. **Carried, not verified.**
5. **One browser, one zoom, one engine.** Headless Chromium at three viewport widths. No second
   engine, no zoom pass, no 200%-text pass, no forced-colours pass, no real screen-reader pass. The
   ARIA is authored and structurally checked; it has not been LISTENED to.
6. **The three pages are not interactive and have never been driven as a task.** Nothing sorts,
   filters, pages or switches tabs. Keyboard order was not walked end-to-end.
7. **The `:has()` repair for D4 is Chromium-measured only.** `:has()` is broadly supported but the
   fallback behaviour (no wrap) was not checked in an engine that lacks it.
8. **The Layer-2 artefact class has no gate of its own.** These files pass the COMPONENT gates
   because they are shaped like components. Nothing checks that a template composes rather than
   re-draws — **the diff-proof in §6 is a script in a receipt, not a gate**, and it dies with this
   session unless someone homes it.
9. **⛔ THE DEFECT IN `Layout-utilities` IS STILL THERE.** So is the one in `Timeline` and
   `Document-row`. Three gated components ship measured defects and this lane repaired **none** of
   them at source, by fence. Every consumer of `.l-split` written before or after today has the same
   non-collapsing split.
10. **Nothing here has been seen by Dave**, and nothing is registered anywhere. Every one of the
    eighteen questions in §8 is open.

---

## 10 · THE STORE DOC-ROW FOR THIS RECEIPT

Minted through the store's own writer (`knowledge/_state.py` `add()`, which refuses a row with no
close condition) at receipt creation, per the return contract and the #185 forgotten-document class.
**Exactly one row; the component rows and the wave row are the conductor's.**

| field | value |
|---|---|
| id | **`W-77`** |
| home | `notes/_receipts/2026-08-20-210-wave5-laneB-templates.md` |
| owner / state / opened | `dave` · `open` · `210` |

⚠ **CONCURRENCY HAZARD, DECLARED.** Lanes A, B, C and D all write `knowledge/_state.json` in the same
window; `_state.py` does read-modify-write with no lock. The next free id was **`W-77`** when this
lane read the store (`W-01`…`W-76` taken, with `W-75`/`W-76` already added by sibling lanes during
this session). This lane **re-read the store after writing and asserted its own row survived**, but
it cannot assert that nobody else's was lost. **The conductor must verify all four lane rows are
present before committing.**

---

## 11 · HANDOFF TO THE CONDUCTOR — the serial set this lane could not touch

1. **`.cn-template-dashboard`, `.cn-template-list-index`, `.cn-template-detail` blocks in
   `canon/canon.css`** — clears 3 of the 11 check-D failures and is the **precondition for any
   four-theme claim** (unproven item 1).
2. **Re-run `gen_kg_edges.py`** — clears `_validate_kg.py`.
3. `component-types.json` · `CATEGORIES` · `gen_showroom.py` ·
   `_validate_radius.MIGRATED_SNIPPETS` registrations, **if these three are to be kept**.
4. **Store rows for the three new artefacts** — the #185 forgotten-document class. This lane minted
   a row for the RECEIPT only.
5. ⬛ **Three defect reports against GATED components**, none repaired by this lane:
   **(a)** `Layout-utilities` — `.l-split`'s container query cannot fire (§3 D1, mutation-controlled);
   **(b)** `Timeline` — `.tl-title`'s descender override loses the cascade (§3 D3, measured);
   **(c)** `Document-row` — same, on `.dr-title` / `.dr-meta`.
   Each has a one-line repair and each needs Dave, because they are gated.
6. ⬛ **Two gate candidates, both priced by evidence in this receipt, neither built:**
   **(a)** a `--computed` leg for `_validate_descender_clip.py` — the textual check passes a label
   whose override loses ([[no-gate-parses-the-artefact]]);
   **(b)** the var-resolution gate already named in `_DS-IMPROVEMENTS.md` — this receipt is its
   **second** live catch, with a mutation control (claims 17/18).
7. ⬛ **A twice-caught promotion candidate for `W-45`/`W-48`:** the crushed-shrinkable-child class,
   n=2 across #209 and #210, mechanically probeable (§3 D4). **Promotion vocabulary is still open
   (`W-51`) — naming a candidate, not promoting one.**
8. ⬛ **A sixth member for `W-59`'s local-var collision ledger:** `--grid-alpha`, Kpi-tile vs
   Chart-bar, opposite values (§7).
9. ⚠ **`_ICON-GAPS.md`:** no gap found by this lane — every glyph used was byte-matched from
   `knowledge/assets/icons/` via a component that already carries it.
10. ⚠ **RUNNING THE GATES REWROTE TRACKED FILES — declared, not hidden.** `git status --short
    knowledge/` shows `knowledge/_A11Y-GATE.md`, `knowledge/_SNIPPET-AUDIT.md` and
    `knowledge/_ICON-SOURCE-AUDIT.md` modified as a **side effect** of the gate runs quoted above,
    plus `knowledge/_state.json` (the doc-row). **No lane edited the first three by hand**; they are
    gate-authored outputs and they are **shared with Lanes A, C and D**, which ran the same gates, so
    attribution is the wave's and not any one lane's. **Reconcile every path deliberately — never
    `git add -A`.**
11. ⚠ **Not this lane's, named so it is not misattributed:** at the time of writing, the snippet gate
    briefly reported one failure in `Template-auth.reference.html` (an ALL-CAPS run, type26-019).
    It was clear by the final run (`0 failure(s)`); recorded only so the wave's history is honest.
