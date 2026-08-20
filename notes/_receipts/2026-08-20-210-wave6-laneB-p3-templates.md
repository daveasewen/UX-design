# Receipt — #210 WAVE 6 · Lane B · the five P3 TEMPLATES

**Lane:** B (Opus) · **Session:** #210 · **Date:** 2026-08-20
**Brief:** `notes/_briefs/2026-08-20-210-wave6-layer2-p3-fanout-brief-v1.md` (THE JOB, LANE B)
**Members:** row 108 settings · row 110 empty · row 111 error (404 / 500) · row 113 report ·
row 114 confirmation. All five are class `layer-2`, derived `NO-ARTEFACT-CLASS`.

> ⛔ **NOTHING IN THIS RECEIPT IS A RULING.** Every domain, fintech and structural semantic below is
> PROPOSED and is Dave's (`s182-D2`, the Kpi-tile precedent). No `CATEGORIES` entry, no
> `MIGRATED_SNIPPETS` entry, no `component-types.json` membership, no `canon.css` block, no
> `gen_showroom.py` run, no `gen_kg_edges.py` run, no `_rulings.json` line and no git operation was
> performed. This lane created **NEW FILES ONLY** and edited **no existing file**.

---

## 0 · THE HEADLINE — SIX DEFECTS, EVERY GATE GREEN OVER ALL SIX, AND ONE OF THEM WAS INVISIBLE

| # | defect | where it lives | gates over it | status |
|---|---|---|---|---|
| 1 | **The type ratchet CLIPPED EVERY FIELD'S DESCENDERS** — 9px cut, measured, and visible in a 4× crop | this lane, inherited from the ratchet | all green, incl. the **descender gate** | **FIXED** (ds-005 two-class, re-measured) |
| 2 | **`--muted` DANGLED and nothing could ever have shown it** — Confirmation's message colour, undeclared | this lane ×2 files | all green | **FIXED** + probe written |
| 3 | **Two fixed-canvas charts side by side made BOTH charts scroll at full desktop width** | this lane | all green | **FIXED** (arithmetic, not taste) |
| 4 | **A byte-lifted chart CONTRADICTED ITS OWN TABLE** — six household categories over five settlement routes | this lane · **and still live in `Template-dashboard`** | all green | **FIXED** here · **parent REPORTED, not patched** |
| 5 | **The crushed-shrinkable-child class, THIRD sighting** — explanation column crushed to 151px by a Segmented control | this lane | all green | **FIXED** (container query on a HOST, mutation-controlled) |
| 6 | **`status-icons/error-solid.svg` is an EMPTY FILE** — an `<svg>` with no path in it | ⛔ **the icon library** | icon gate green (nothing references it) | **REPORTED, not repaired** |

**And the one that says the most.** Defect 2 is the [[dangling-dataviz-var-renders-silent-black]]
class arriving by a route that class has never taken. `Confirmation`'s `.confirm__msg` reads
`color:var(--muted)`; the first draft of two templates never declared `--muted`. A `var()` that
resolves to nothing makes the declaration **invalid at computed-value time**, so `color` falls back
to **inherit** — and `--muted` is `text/secondary`, which in Mono is the **same hex** as
`text/default`. **The page rendered pixel-identically. No screenshot, no contrast check, no eye and
no gate could ever have found it.** Only a probe that asks the browser *"is every var this page
reads actually resolved?"* can see a dangle whose fallback happens to be correct — and the next one
might not be.

★ **The general point for Layer 2, stated once:** a template inherits a **var contract** from every
component it composes, and **nothing in this repo checks that it carried them all.** Wave 5 found
that with a visible black chart. This lane found it with **nothing visible at all.**

---

## 1 · FILE LIST — ten new files, plus this receipt

| # | path | bytes |
|---|---|---|
| 1 | `knowledge/snippets/Template-settings.reference.html` | 58,688 |
| 2 | `knowledge/components/template-settings.meta.json` | 12,810 |
| 3 | `knowledge/snippets/Template-empty.reference.html` | 31,327 |
| 4 | `knowledge/components/template-empty.meta.json` | 10,077 |
| 5 | `knowledge/snippets/Template-error.reference.html` | 23,428 |
| 6 | `knowledge/components/template-error.meta.json` | 9,789 |
| 7 | `knowledge/snippets/Template-report.reference.html` | 75,174 |
| 8 | `knowledge/components/template-report.meta.json` | 11,583 |
| 9 | `knowledge/snippets/Template-confirmation.reference.html` | 31,823 |
| 10 | `knowledge/components/template-confirmation.meta.json` | 10,977 |
| 11 | `notes/_receipts/2026-08-20-210-wave6-laneB-p3-templates.md` | this file |

**No existing file was edited.** No `intent` field was authored (`W-58` parked). Renders and build
scripts live OUTSIDE the repo — **`(NON-REPO: the session outputs folder, `wave6-laneB/` — 30
full-page PNGs (5 pages × light+dark × 1400/820/420), two 4× crops, and `measure.json`)`** per
`s191-D2` home-or-declare. The build helpers `/var/tmp/b6/{common,t_*,metas,drive,mutate,shots,
diffproof}.py` are scratch and do not survive the session; **every probe in the claim table is
written out in full so it can be re-run without them**, and the diff-proof script is reproduced
whole in §6.

★ **How the borrowing was done, because it changes what the claims mean.** Every borrowed CSS
region was **sliced out of its source file at build time by string index**, never retyped. A
byte-diff against the source is therefore guaranteed **by construction**, not by care. The only
transformations applied to a slice were (a) `defont()`, which strips raw font declarations and
records every drop, and (b) four **declared var-name renames** (§5). That is the whole mechanism.

---

## 2 · CLAIM TABLE — every claim carries a probeable token (`s182-D1`)

Run from the repo root.

| # | claim | probe — re-runnable, exactly as written | verdict |
|---|---|---|---|
| 1 | The leading-trim block is the CURRENT one, byte-identical to Command-palette line 36 (328 chars) in all five | `python3 -c "cp=open('knowledge/snippets/Command-palette.reference.html').read().split(chr(10))[35]; print(len(cp), all(cp in open('knowledge/snippets/Template-%s.reference.html'%n).read() for n in ('settings','empty','error','report','confirmation')))"` → **`328 True`** | ✅ |
| 2 | The AUTO-TOKENS alpha ramp is byte-identical to Meter's generated block in all five | `python3 -c "m=open('knowledge/snippets/Meter.reference.html').read(); b=m[m.index('/* ===== AUTO-TOKENS START'):m.index('AUTO-TOKENS END ===== */')+24]; print(all(b in open('knowledge/snippets/Template-%s.reference.html'%n).read() for n in ('settings','empty','error','report','confirmation')))"` → **`True`** | ✅ |
| 3 | The report's LINE chart is byte-identical to Chart-line's twelve-month specimen (minus the `dv-fit` class) | §6 part A → **`Template-report line-chart BYTE-identical to Chart-line : True`** | ✅ |
| 4 | The report's COLUMN chart is **geometry-identical** to Chart-bar's column specimen — every `x`, `y`, `width`, `height`, `data-fx`, `data-fw`, grid line and axis value — with only text nodes and the copy-bearing attributes changed | §6 part A, which neutralises `aria-label`/`data-tip` and every text node on **both** sides → **`column-chart GEOMETRY identical to Chart-bar : True`**. The label change is defect 4 and is argued in §3 | ✅ **and the delta is declared** |
| 5 | The confirmation's success roundel is byte-identical to Confirmation's, **which is byte-identical to the library asset** | §6 part A → **`success glyph BYTE-identical to Confirmation: True`** and **`Confirmation's glyph path is byte-identical to the library asset: True`** | ✅ |
| 6 | **540 borrowed selectors are declaration-identical to their source component's rule** for the same selector; 18 carry at least one declaration not in the source, and **every one of the 18 is named in §5** | §6 part B → **`TOTAL: 540 selector(s) proven declaration-identical, 18 carrying declarations not in the source`** (settings 167/5 · empty 83/2 · error 48/4 · report 170/3 · confirmation 72/4) | ✅ |
| 7 | **NO COLOUR IS INVENTED.** Every hex in every theme block appears in the theme block of some source component | §6 part C → settings **79 · 0 NOT FOUND**, empty **38 · 0**, error **36 · 0**, report **92 · 0**, confirmation **48 · 0** | ✅ |
| 8 | …and that check **CAN FAIL** | MUTATION CONTROL, driven: `sed -i 's/--muted:#1A1A1A;/--muted:#C0FFEE;/' knowledge/snippets/Template-error.reference.html` then re-run → **`36 hex declaration(s) · 1 NOT FOUND` · `INVENTED COLOUR: --muted:#C0FFEE`**; restored and re-run → **`0 NOT FOUND`** | ✅ **MUTATION-CONTROLLED** |
| 9 | 4px-grid gate clean on all five | `python3 knowledge/_validate_grid.py knowledge/snippets/Template-{settings,empty,error,report,confirmation}.reference.html` → *"GRID GATE PASS — all layout dimensions on the 4px grid (5 file(s))"* | ✅ |
| 10 | Type-composite gate clean on all five, and **the repo debt does not grow** | `python3 knowledge/_validate_type_composites.py <the five>` → *"TYPE GATE PASS — all component text bound to canon composites (5 file(s))"* · *"advisory — 0 raw font decl(s) in demo-chrome scope"*. Repo-wide: `python3 knowledge/_validate_type_composites.py` → *"TYPE GATE FAIL — **1097** violation(s) across 90/150 file(s). TYPE-001 ×31 · TYPE-002 ×1050 · TYPE-003 ×16"* — **the #203 measured baseline, EXACTLY UNCHANGED**. This lane's TYPE-002 contribution: **0** | ✅ |
| 11 | Snippet/token gate clean, whole repo | `python3 knowledge/_validate_snippets.py` → *"snippet gate: 135 snippet(s), 0 failure(s)"* | ✅ |
| 12 | a11y gate: zero failures with all five present | `python3 knowledge/_validate_a11y.py` → *"a11y gate: 135 snippet(s), 0 failure(s), 285 warning(s), 627 note(s) · 1272 controls + 239 marks measured · 131 mark(s) below 24"* (135/285 are WAVE-wide — Lanes A/C/D added files concurrently) | ✅ |
| 13 | Descender-clip gate passes | `python3 knowledge/_validate_descender_clip.py` → *"DESCENDER-CLIP GATE PASS — every truncating label is descender-safe (151 file(s))"* ⚠ **AND THAT PASS WAS THE DEFECT — see claim 20 and §3 D1.** | ✅ **but blind** |
| 14 | The five metas are schema-valid — **and P-1 caught a real error first** | `python3 knowledge/_probe_registry/probe_meta_schema.py --check` → *"P-1 meta-schema sweep: 132 meta(s) checked · 0 finding(s) · 1 exempt failure(s)"* · `PROBE P-1 — findings=0`. **Before the fix:** *"⛔ template-report.meta.json [stateModel] 'none' is not one of ['simple', 'full']"* ×4 files. A property that does not apply is **omitted**, never defaulted to a word the schema has never heard of | ✅ **after a real catch** |
| 15 | Duplicate-ID probe clean | `python3 knowledge/_probe_registry/probe_dup_ids.py --check` → `PROBE P-2 — findings=0` | ✅ |
| 16 | Icon gate: nothing invented in any of the five | `python3 knowledge/_validate_icons.py Template-<n>` for each → *"0 UNKNOWN"* ×5. `Template-settings` reports *"2 bespoke"*, which are the two checkbox ticks — **byte-copied from Selection-controls with its own `data-bespoke` reason string**, the mirror form lesson 4 permits. **And that too was a real catch:** the first draft hand-drew `d="M3 9.5 L7 13.5 L15 4.5"` and the gate returned **2 UNKNOWN** | ✅ **after a real catch** |
| 17 | ★ **Zero NEW context or pattern node-ids were minted by this lane** | `python3 -c "import json;ctx={x['id'] for x in json.load(open('knowledge/components/_nodes-context.json'))};pat={x['id'] for x in json.load(open('knowledge/components/_nodes-pattern.json'))};bad=[(s,e['ref']) for s in ['template-settings','template-empty','template-error','template-report','template-confirmation'] for k,p in (('usedInContext',ctx),('commonPattern',pat)) for e in json.load(open('knowledge/components/%s.meta.json'%s))['edges'][k] if e['ref'] not in p];print('UNRESOLVED:',bad)"` → **`UNRESOLVED: []`** | ✅ |
| 18 | **The real HSBC cut rendered — asserted with TWO CONTROLS, not `fonts.check()`** | headless Chromium, 40px `Handgloves 12345` canvas measurement, taken on every one of the five pages: `HSBC_MtUnivers_Latin` **346.88** · `"Univers Next HSBC"` **346.88** · `"Univers Next for HSBC"` **346.88** · `DejaVu Sans` **375.39** · nonexistent face **301.07**. Both aliases land on the target and NEITHER lands on either control | ✅ **DRIVEN** |
| 19 | **Zero horizontal page overflow, all five pages, both themes, all three widths** | driven at 1400 / 820 / 420 CSS px: `document.documentElement.scrollWidth - clientWidth` → **0** in all **30** runs | ✅ **DRIVEN** |
| 20 | **The responsive collapse is MEASURED, not asserted** (lesson 3) | driven `getComputedStyle(...).gridTemplateColumns` / `.flexDirection` at 1400 / 820 / 420 — full table in §4 | ✅ **DRIVEN** |
| 21 | **No dangling CSS var anywhere in the five files** — the #184 class, asked in the consumer's grammar | driven probe: collect every `var(--x)` named by a rule **that matches a live element**, report any no element resolves → **`dangling: []` in all 30 runs**. Ground truth beside it: `getComputedStyle(rect.dv-series).fill` → **`rgb(118, 102, 130)`** = `#766682` = `data/series/1`, in BOTH themes | ✅ **DRIVEN** |
| 22 | …and that probe **CAN FAIL**, and it reproduces the exact defect | MUTATION CONTROL, driven in-page on `Template-report`: inject `rect.dv-series{fill:var(--data-series-NOPE)}` → before **`{dangling: [], seriesFill: 'rgb(118, 102, 130)'}`**, after **`{dangling: ['--data-series-NOPE'], seriesFill: 'rgb(0, 0, 0)'}`** — dangling detected AND the silent black reproduced | ✅ **MUTATION-CONTROLLED** |
| 23 | The container-query collapse fires **because of the HOST**, not by luck | MUTATION CONTROL, driven at 820px on `Template-settings`: host present **`['426px'×6]`** → `containerType:'normal'` **`['358px 44px'×4, '238.984px 163.016px', '235.391px 166.609px']`** (the crush returns, exactly) → restored **`['426px'×6]`** | ✅ **MUTATION-CONTROLLED** |
| 24 | Chart-line's two HIDDEN baked views really would paint without `.dv-off` | MUTATION CONTROL, driven: `.dv-off{display:block !important}` → the ghost series and the target line go from `display:none` to `display:block` with live strokes `rgb(118,102,130)` and `rgb(49,49,49)` | ✅ **MUTATION-CONTROLLED** |
| 25 | **The sticky action bar hides nothing AT THE SCROLL END** (lesson 7) | driven: scroll `.demo-frame` to `scrollHeight`, then count live `.fl-box` / `.field` boxes intersecting the bar's band → **0 at 1400, 0 at 820, 0 at 420, both themes**, with `frameScrolls: true` in all six runs. ⚠ **The FIRST form of this probe read at the INITIAL scroll position and reported 1–2 overlaps** — which is not a defect, it is what a sticky bar is *for*. **The test that matters is at the scroll END** | ✅ **DRIVEN, after an instrument correction** |
| 26 | The report's six chart labels do not collide | driven `getBBox()` per label → **`overlaps: []`**, minimum inter-label gap **26.3px**. ⚠ The first replacement set (full trading names) gave **five overlapping pairs, worst 13.0px** — see §3 D4 | ✅ **DRIVEN, after a real catch** |
| 27 | Every field's descenders survive | driven `scrollHeight − clientHeight` per input, plus the computed `text-box-edge`: **`[[0,'text'],[0,'text'],[0,'text'],[0,'text']]`** on settings and **`[[0,'text']]`** on empty. Before the repair: **`9`px clipped with edge `cap alphabetic`** | ✅ **DRIVEN** |
| 28 | ⛔ **`_validate_binds_resolve.py` check D FAILS for all five — DECLARED, not hidden** | `python3 knowledge/_validate_binds_resolve.py` → naming *"Template-settings.reference.html: no `.cn-template-settings` block in canon.css — project_canon projection is silently OFF for this snippet"* and the same for `-empty`, `-error`, `-report`, `-confirmation` (plus sibling-lane files) | ⛔ **CONDUCTOR'S** |
| 29 | ⛔ **`_validate_kg.py` FAILS** — the node registries are stale because five metas are new | `python3 knowledge/_validate_kg.py` → *"`_nodes-pattern.json` DRIFTED … `_nodes-context.json` DRIFTED"*. `gen_kg_edges.py` must be re-run. ★ Made as cheap as possible: **zero new node-ids** (claim 17) | ⛔ **CONDUCTOR'S** |

---

## 3 · THE SIX DEFECTS, IN FULL — every one found by LOOKING or by MEASURING, none by a gate

### D1 ⛔⛔ THE TYPE RATCHET CLIPPED EVERY DESCENDER IN EVERY FIELD, AND THE DESCENDER GATE PASSED IT

`Form-layout` writes `.fl-box input{font:400 16px/24px var(--font)}`. That is a raw font
declaration, the repo's type debt is **shrink-only**, so the ratchet says drop it and bind
`.t-cm-input` in markup. `.t-cm-input` is **16px at `line-height:1`**. An `<input>` clips to its own
box, and the canon leading-trim `:is()` list **includes `input[type=text]`, `input[type=email]` and
`input[type=tel]`** — so every field on the settings page was trimmed to `cap alphabetic` and then
cut.

| probe, all driven at #210 | result |
|---|---|
| `#st-email` as first shipped (value `a.whitfield@meridiansupplies.co.uk`) | `clientHeight` **21** · `scrollHeight` **30** ⇒ **9px CLIPPED**, computed edge `cap alphabetic` |
| the source `Form-layout`'s own input, raw font intact | box **24px**, nothing clipped |
| a 4× crop of the field, LOOKED AT | the two `p`s of "supplies" **cut flat** |
| **TWO-CLASS** `.fl-box input.t-cm-input{text-box-edge:text text}` | `scrollHeight` **21** = `clientHeight` **21** ⇒ **0px clipped**, computed edge **`text`** |
| `text-box-trim:none` (alternative, not taken) | also 0px, but it discards the trim rather than re-basing it |
| inline `text-box-edge:text text !important` on the ELEMENT | **21px, unchanged** — the element-level test measures the input's own box and cannot see the line box, so it reads as a null result. ⚠ **An instrument that returns "no change" is not the same as a fix that does nothing** |

★ **The mechanism, and why a single class could never have worked.** The canon trim rule is
`:is(button,a,label,span,…,input[type=text],…):not(:has(svg))`. `:is()` takes the **highest**
specificity among its arguments, and that list contains **attribute selectors**, which are
class-level. The whole `:is()` weighs `0-1-1`; `:not(:has(svg))` adds an element for `0-1-2`. A
single class is `0-1-0`. **`.fl-box input.t-cm-input` weighs `0-2-1`.** That is ds-005, exactly as
the brief's lesson 2 states it, and the computed-edge read-back is the proof the declaration **won**
— not merely that it was written.

⛔ **`_validate_descender_clip.py` passes all of it**, on all 151 files, because it is a **textual**
check over truncating labels: it greps for the string on a truncating selector and never asks the
browser whether anything was cut. **It has no concept of an `<input>` at all.** That is
[[no-gate-parses-the-artefact]] in a new place.

⬛ **AND IT IS A CLASS, NOT AN INCIDENT.** Every template in wave 5 and wave 6 that drops
`Form-layout`'s raw font and binds `.t-cm-input` inherits this. `Template-create-edit`,
`Template-wizard` and `Template-auth` (#210 wave 5, lane C) all did exactly that. **This lane did not
open them** — they are not its files — but the conductor should assume the same 9px and measure.

### D2 ⛔⛔ `--muted` DANGLED IN TWO FILES AND **NOTHING VISIBLE COULD EVER HAVE SHOWN IT**

`Confirmation`'s `.confirm__msg` reads `color:var(--muted)`. The first drafts of `Template-error`
and `Template-confirmation` borrowed that rule and **never declared `--muted`**.

- A `var()` that resolves to nothing makes the declaration **invalid at computed-value time**.
- For an inherited property like `color`, invalid-at-computed-value-time means **inherit**.
- The inherited value here is `--text` = `text/default`.
- **`--muted` is `text/secondary`, and in Mono `text/secondary` is the SAME HEX as `text/default`** —
  `#1A1A1A` light, `#FFFFFF` dark.

**So the page rendered pixel-for-pixel identically.** No screenshot could show it. No contrast
check could show it. No eye could show it. The snippet gate could not show it, because the gate
only checks vars the manifest **declares** — and an undeclared var is invisible to it by
construction. **Only a probe that asks the live document "is every var you read resolved?" can see
this**, and it only sees it because it does not care whether the fallback happened to be right.

**Repair:** `--muted: text/secondary` declared in both theme blocks of both files, added to both
manifests with its contrast pair, and re-measured to `dangling: []` in all 12 runs.

⬛ **This strengthens the case for the var-resolution gate already priced in `_DS-IMPROVEMENTS.md`
in a way the earlier evidence could not.** Wave 5's catch was a **black chart** — a defect an eye
would eventually find. This one has **no visual signature at all in this theme**, and would acquire
one the moment a theme forks `text/secondary` away from `text/default`. **Console, Legacy and
Supercharge are exactly where that would happen, and they are the themes nobody has rendered.**

### D3 ⛔ TWO FIXED-CANVAS CHARTS SIDE BY SIDE MADE **BOTH** CHARTS SCROLL AT DESKTOP WIDTH

The obvious layout for a report is two chart panels side by side, and that is what this file was
built with. Then it was driven.

| probe, driven with the two-column draft in place | result |
|---|---|
| 1400px viewport — page container 1088px, each panel 528px | chart stage `clientWidth` **478** vs `scrollWidth` **580** ⇒ **`scrolls: true`, BOTH CHARTS** |
| 820px viewport (already one column) | `scrolls: false` |
| after the repair, 1400px | `scrolls: false` · 820px `scrolls: false` · 420px `580 / 338 → scrolls: true` (correct) |

**A desktop report whose every chart must be dragged sideways is a defect, and no gate can see it:**
GRID, TYPE, SNIPPETS, A11Y, DESCENDER and ICONS were all green over it, and it looks plausible in a
screenshot until you notice the axis is cut.

★ **The repair is arithmetic, not taste, and that matters for the record.** A chart's canvas is a
fixed **580px** (`.dv-chart-area{width:580px}`) because the fit is a runtime measurement the static
file does not host. Two panels therefore need `2 × (580 + 48 panel padding) + 32 gap = **1288px** of
container`. This page's own frame caps at `--l-max:1120px`. **Two-up is not a narrow-screen problem;
it is impossible at any width this page can reach.** Writing it as a container query with a 1288px
threshold would have been a rule that can never fire — [[instrument-without-a-consumer]] — so it was
not written. One chart per row.

### D4 ⛔ A BYTE-LIFTED CHART CONTRADICTED ITS OWN TABLE — **and the same contradiction is live in `Template-dashboard`**

Lifted verbatim for provenance, `Chart-bar`'s column specimen brought its **demo data** with it. The
report drew **"Spend by category — Groceries, Transport, Housing, Leisure, Utilities, Savings"**
directly above a table headed **"Receipts by route — Card acquiring, Faster Payments, Direct Debits,
Standing orders, International"**. Six household spending categories on a business settlement
report, arguing with the five routes underneath them.

**Every gate was green,** because a chart's category labels are ordinary text nodes and **nothing in
this repo knows they are supposed to mean the same thing as the table beside them.**

**The resolution, and its price, stated exactly.** The **geometry** stays byte-identical — every
`x`, `y`, `width`, `height`, `data-fx`, `data-fw`, every grid line and every axis value — so the
diff-proof still holds for everything that is a **drawing** decision (claim 4). What changed is the
six label **text nodes** and the accessible names that quote them, which are **domain content** and
were never Chart-bar's to own. The six bars are re-read as a *different cut* from the table (payers,
not routes) so the two are complementary rather than contradictory, and **the numbers are made to
add up**: 420 + 180 + 950 + 260 + 210 + 300 = **2,320 of the page's 3,800 receipts**.

⚠ **And the first replacement set was too long, which only a measurement showed.** Full trading
names ("Ashcombe Retail", "Riverside Trading") were tried first: `getBBox()` gave **five overlapping
label pairs, worst by 13.0px**, and at a glance the axis still looked like an axis. **A specimen's
label positions were generated for the source's own strings and do not move.** Names of comparable
length were substituted and the overlap re-measured to **zero, minimum gap 26.3px**.

⬛ **REPORTED, NOT EDITED, BECAUSE IT IS NOT THIS LANE'S FILE:** `Template-dashboard` (#210 wave 5,
lane B) byte-lifted **the same specimen** and still says *"Where the money went — Groceries,
Transport, Housing"* on a **business banking overview** page. That is the same defect, live, in a
file this lane must not touch.

### D5 ⛔ THE CRUSHED-SHRINKABLE-CHILD CLASS, **THIRD SIGHTING**

`1fr auto` is the honest description of "copy, then control", and it is safe while the control is a
44px switch. It is **not** safe when the control is a Segmented control, because a `.seg` is `auto`
and does not shrink.

| probe, driven at a 420px viewport, before the repair | result |
|---|---|
| the four switch rows | `270px 44px` — fine |
| the two segmented-control rows | **`150.984px 163.016px`** — the EXPLANATION column crushed to 151px while the control kept its full 163px |
| after the repair, 820px and 420px | **`426px` / `338px`** — one column, six rows |
| **MUTATION CONTROL** — `containerType:'normal'` on the host, re-read | **`238.984px 163.016px`** — the crush returns, exactly |

★ **n = 3, across three consecutive sessions and three different layouts:** #209 lane A on a payee
row ("the payee was being crushed by its own chips"), #210 wave-5 lane B on a `Document-row`, and
this. It is mechanically probeable — *"a row whose only flexible item is text, carrying more than
one non-shrinking sibling"* — and it is **named to the conductor as a twice-caught promotion
candidate (`W-45` / `W-48`)**. ⬛ Promotion vocabulary is still open (`W-51`); this names a
candidate, it does not promote one.

⚠ **The repair's container is a DEDICATED HOST**, never the queried element — an element is a query
container for its **descendants** and never for itself, the trap wave 5 caught twice and which is
invisible in a screenshot. Mutation-controlled above so the collapse is a measurement, not a claim.

### D6 ⛔ `status-icons/error-solid.svg` IS AN EMPTY FILE

```
$ cat knowledge/assets/icons/status-icons/error-solid.svg
<svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
</svg>
```

No path. Its siblings `success-solid.svg`, `warning-solid.svg` and `information-solid.svg` all carry
one. Nothing in the library references it, so the icon gate cannot notice — **an unused asset has no
observer.** Found by opening it while choosing a glyph for the error template. **Reported, not
repaired: `knowledge/assets/` is not this lane's.**

⚠ **Note what this is NOT.** It is not the reason `Template-error` binds no RAG roundel. That reason
is a design decision and it is stated on the file's own face (§3 below and the file header). Two
independent facts arrived at once, and conflating them would have laundered a taste into a
constraint.

---

## 4 · WHAT WAS DRIVEN, AND WHAT IT MEASURED

Headless Chromium (`chromium_headless_shell`, `--no-sandbox --disable-dev-shm-usage --disable-gpu`),
each file loaded with `goto("file://…")` per `_RUNBOOK-render-verify.md`, real HSBC cut asserted with
the three-way control probe (claim 18), `data-theme` toggled live, **30 full-page screenshots
(5 pages × light+dark × 1400/820/420) taken and LOOKED AT**, plus two 4× crops. Every reading taken
after `mouse.move(2,2)` — the #210 wave-5 lane C lesson: Playwright leaves the pointer where it last
clicked, and a hover state reads as a wrong colour.

**THE COLLAPSE, MEASURED (lesson 3) — computed values at 1400 / 820 / 420:**

| region | 1400 | 820 | 420 |
|---|---|---|---|
| settings `.l-split` | `776px 280px` | `476px 280px` | **`388px`** |
| settings `.fl-row` | `355px 355px` | `228px 228px` | **`338px`** |
| settings `.tpl-setting` | `658px 44px` | **`426px`** | **`338px`** |
| settings `.fl-actions` | `row` | `row` | **`column-reverse`** |
| report `.l-grid` (stats band) | `254 254 254 254` | `246.7 ×3` | **`388px`** |
| report `.tpl-report-meta` | `254 ×4` | `246.7 ×3` | **`182 182`** |
| error / confirmation `.confirm__actions` | `row` | `row` | **`column`** |

**Wide fixed-canvas regions scroll INSIDE themselves rather than the page:** at 1400 and 820 both
report chart stages read `scrolls: false`; at 420 both read `scrollWidth 580 / clientWidth 338 →
scrolls: true` and the table reads `640 / 336 → true`.

**Type, measured rather than assumed** (light-1400) — every composite in use resolved to its canon
ramp value in the real face: `t-cm-legal` 12/400 · `t-cm-caption` 14/400 · `t-cm-ctl-14` 14/500 ·
`t-cm-ctl-16` 16/400 · `t-ed-body-small` 14/400 · `t-cm-label` 16/400 · `t-cm-input` 16/400 ·
`t-cm-tooltip` 14/400 · `t-cm-figure-5` 16/400 · `t-cm-figure-6` 14/400 · `t-cm-section-label`
20/500 · `t-cm-figure-4` 32/400 · `t-ed-heading-4` 20/400 · `t-ed-body` 16/400 · `t-ed-heading-2`
**28/300** · `t-cm-chart-label` 12/500 · `t-cm-chart-value` 12/500 — all `"Univers Next HSBC"`.

**Effective hit targets, read off the page not assumed** (1400px): every Button **44px** tall
(159×44, 135×44, 121×44, 170×44, 220×44, 232×44, 234×44, 304×44, 197×44, 169×44, 198×44, 100×44,
116×44); every Selection-controls `<label>` **44px** tall (44×44 for the bare switches, 112–304×44
for text labels); every Data-grid sort header **44px** tall (237×44, 171×44, 188×44, 166×44,
268×44). Segment buttons **32px** (md) / **28px** (sm) visible, carrying Segmented-control's
invisible ≥44px `::before`. **Three inherited shortfalls, measured and NOT silently enlarged** —
see Q9.

---

## 5 · THE 18 SELECTORS CARRYING A DECLARATION NOT IN THE SOURCE — every one named

Claim 6's `NEW` rows, grouped. **None of them is a re-drawn atom.**

**(a) Theme blocks and `:root` — 10 selectors (2 per file).** A template's theme block is the
**union** of the theme blocks of the components it composes, so **no single source can contain all
of it**. That is why the honest claim is claim 7's per-value UNION check, which is
mutation-controlled: **0 of 293 hex declarations across the five files is absent from every source.**

**(b) Motion-name collisions resolved by RENAME — 3 declarations.** `--move:200ms cubic-bezier(.4,0,.2,1)`
(Segmented-control's own unnamed `--ease`, renamed because Selection-controls on the same page
declares `--ease` at 180ms and **two components disagreeing about what `--ease` means is the
collision class again**); `--phys-size:120` (Button's characteristic text-button size, hoisted to
`:root` because three borrowed ladders read it); `--draw-slow:2400ms cubic-bezier(.33,0,.3,1)`
(Chart-line's draw duration, which its specimen's `pathLength="2400"` depends on).

**(c) `--muted`, `--data-target`, `--target-alpha` — 5 declarations, and every one is a var contract
the borrowed markup reads.** `--muted` is D2. `--data-target` / `--target-alpha` are consumed **only
by Chart-line's two hidden baked views**, which a reader would never guess were needed — and which
paint over the chart if `.dv-off` is not carried with them (claim 24).

**(d) `.fl-tip::before` — 1 selector, 2 declarations.** Form-layout writes `var(--hit,44px)`; this
page already declares the **bound** name `--target-min` (`target/min`). **Same token, one name.**

**(e) Demo chrome — the rest (`.demo-h`, `.demo-note`).** Delete every one and all five pages still
work.

**THE FOUR DECLARED VAR-NAME RENAMES, in full**, because a rename inside a borrowed rule is exactly
the kind of thing that becomes invisible:

| source | its name | this page's name | why |
|---|---|---|---|
| Segmented-control | `--border` (`form/border/default`) | `--fborder` | this page already calls `border/subtle` `--border`, following Data-grid and Template-dashboard |
| Segmented-control | `--ease` (200ms) | `--move` | Selection-controls declares `--ease` at 180ms on the same page |
| Selection-controls | `--label` / `--label-disabled` | `--text` / `--text-disabled` | Form-layout already declares those names for the same two tokens |
| Form-layout | `var(--hit,44px)` | `var(--target-min)` | the bound name for `target/min`, already declared here |

★ **Every one is a VAR-NAME collision avoided, not a value changed.** Composing eight components
means eight vocabularies; where two sources name the same token differently, one name has to win.
§6 part B normalises exactly these four before comparing, which is why they do not inflate the
`NEW` count — and the normalisation is written into the script so a reader can see what was
forgiven.

---

## 6 · THE DIFF-PROOF SCRIPT, WRITTEN OUT SO IT CAN BE RE-RUN

Save as `diffproof.py` at the repo root and run `python3 diffproof.py` (add `-v` to print every
`NEW` row). It produced claims 1–8.

```python
#!/usr/bin/env python3
"""Diff-proof every borrowed region of the five #210 wave-6 lane-B templates against its SOURCE.
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
TARGETS = ['knowledge/snippets/Template-settings.reference.html',
           'knowledge/snippets/Template-empty.reference.html',
           'knowledge/snippets/Template-error.reference.html',
           'knowledge/snippets/Template-report.reference.html',
           'knowledge/snippets/Template-confirmation.reference.html']
SOURCES = ['Layout-utilities','Form-layout','Selection-controls','Segmented-control','Empty-state',
           'Confirmation','Summary','Stat-card','Kpi-tile','Data-grid','Chart-bar','Chart-line',
           'Button','Breadcrumbs','Headers','View-options','Status-indicator','Document-row',
           'Template-dashboard']
src_rules = {s: rules(strip_comments(style_of('knowledge/snippets/%s.reference.html' % s))) for s in SOURCES}

print('=== A · BYTE-IDENTICAL REGIONS ===')
cp = txt('knowledge/snippets/Command-palette.reference.html').split('\n')[35]
m = txt('knowledge/snippets/Meter.reference.html')
auto = m[m.index('/* ===== AUTO-TOKENS START'):m.index('AUTO-TOKENS END ===== */') + 24]
cb = txt('knowledge/snippets/Chart-bar.reference.html').split('\n')
s0 = next(i for i, l in enumerate(cb) if 'Spend by category. Groceries 420' in l)
s1 = next(i for i, l in enumerate(cb) if i > s0 and l.strip() == '</g>')
col = '\n'.join(cb[s0:s1 + 1]).replace('class="dv-svg dv-fit"', 'class="dv-svg"')
# the column specimen's GEOMETRY only: category labels + accessible names are DOMAIN CONTENT and
# were deliberately re-written (see the receipt). Strip every text node and every copy-bearing
# attribute from BOTH sides and the remainder must be byte-identical.
def geom(s):
    s = re.sub(r'(aria-label|data-tip)="[^"]*"', r'\1=""', s)
    s = re.sub(r'>[^<>]+<', '><', s)
    return re.sub(r'^\s+', '', s, flags=re.M).strip()
cl = txt('knowledge/snippets/Chart-line.reference.html')
i = cl.index('aria-label="Balance over the y')
line = cl[cl.rindex('<svg class="dv-svg', 0, i):cl.index('</svg>', i) + 6].replace('class="dv-svg dv-fit"', 'class="dv-svg"')
conf = txt('knowledge/snippets/Confirmation.reference.html')
tick = conf[conf.index('<svg class="success"'):conf.index('</svg>', conf.index('<svg class="success"')) + 6]
for t in TARGETS:
    s = txt(t)
    print('  %-46s trim(%dch)=%-5s auto-tokens=%-5s' % (t.split('/')[-1], len(cp), cp in s, auto in s))
rep = txt('knowledge/snippets/Template-report.reference.html')
print('  Template-report  column-chart GEOMETRY identical to Chart-bar :', geom(col) in geom(rep))
print('  Template-report  line-chart   BYTE-identical to Chart-line    :', line in rep)
print('  Template-confirmation success glyph BYTE-identical to Confirmation:',
      tick in txt('knowledge/snippets/Template-confirmation.reference.html'))
print('  ...and Confirmation\'s glyph path is byte-identical to the library asset:',
      re.search(r'd="([^"]+)"', tick).group(1) in txt('knowledge/assets/icons/status-icons/success-solid.svg'))

print('\n=== B · DECLARATION-LEVEL PROOF, per borrowed selector ===')
tot_m = tot_x = 0
newrows = []
for t in TARGETS:
    tr = rules(strip_comments(style_of(t)))
    mm = xx = 0
    for sel, decls in sorted(tr.items()):
        base = (sel.replace('.dg ', '').replace('nav.tpl-crumbs', 'nav').replace('.tpl-crumbs ', '')
                   .replace('.empty .glyph', '.glyph').replace('.glyph', '.empty .glyph'))
        hits = [(n, r) for n, rr in src_rules.items() for k, r in rr.items() if k == sel] \
            or [(n, r) for n, rr in src_rules.items() for k, r in rr.items() if k == base]
        if not hits: continue
        name, srcdecls = max(hits, key=lambda h: sum(1 for d in decls if d in h[1]))
        # the four renames are DECLARED, not silent: same token, one name (see receipt section 5)
        norm = lambda d: (d.replace('var(--fborder)', 'var(--border)').replace('var(--move)', 'var(--ease)')
                           .replace('var(--text-disabled)', 'var(--label-disabled)')
                           .replace('var(--text)', 'var(--label)').replace('var(--target-min)', 'var(--hit)'))
        missing = [d for d in decls if d not in srcdecls and norm(d) not in srcdecls]
        if not missing: tot_m += 1; mm += 1
        else:
            tot_x += 1; xx += 1
            newrows.append('    NEW  %-40s <- %-20s not-in-source: %s' % (sel[:40], name, '; '.join(missing)[:110]))
    print('  %-46s MATCH %3d   NEW %3d' % (t.split('/')[-1], mm, xx))
print('\n  TOTAL: %d selector(s) proven declaration-identical, %d carrying declarations not in the source'
      % (tot_m, tot_x))
if '-v' in __import__('sys').argv:
    print('\n'.join(newrows))

print('\n=== C · THEME-BLOCK UNION PROOF (no colour is invented) ===')
HEX = re.compile(r'#[0-9A-Fa-f]{3,8}')
known = set()
for s in SOURCES:
    for k, v in src_rules[s].items():
        if k.startswith('[data-theme') or k == ':root':
            for d in v:
                mm2 = HEX.search(d)
                if mm2: known.add(mm2.group(0).upper())
for t in TARGETS:
    tr = rules(strip_comments(style_of(t))); unknown = []; n = 0
    for k, v in tr.items():
        if not (k.startswith('[data-theme') or k == ':root'): continue
        for d in v:
            mm2 = HEX.search(d)
            if not mm2: continue
            n += 1
            if mm2.group(0).upper() not in known: unknown.append(d)
    print('  %-46s %3d hex declaration(s) · %d NOT FOUND in any source theme block'
          % (t.split('/')[-1], n, len(unknown)))
    for u in unknown: print('      INVENTED COLOUR: %s' % u)
```

⚠ **The instrument's own blind spots, declared.** It compares CSS **text**, so it cannot see whether
a borrowed rule still WINS at runtime — **D1 was completely invisible to it**. It matches by
selector STRING, so a renamed selector reads as new (which is why the four declared renames are
normalised, and why that normalisation is written in the open). It has no opinion about markup,
which is why **D4 was invisible to it too**. **The browser drive is not optional beside it — it is
the half that catches what it cannot.**

---

## 7 · `$decisionsForDave` — NAMED, NOT SETTLED

**None of these is answered by construction. All are Dave's.**

**Q1 — ⛔ Should `Template-error` carry a RAG colour, and is that even a template's question?**
Not one `rag/*` token is bound anywhere in that file, and it is the single biggest judgement in this
delivery. The reasoning is on the file's own face: a form error names a field the person can fix and
the red carries that instruction; **a 404 has no field.** Painting a whole page with the error seat
sits squarely in the two-red law's neighbourhood (`s151-D1`) and the mono error-ink camp's
(`s149-D1`). The anchor is Empty-state's decorative 48px glyph at `alpha/40` and the **heading**
carries the meaning. **Live outcome either way:** if Dave rules that an error page takes the error
seat, one line changes; if he rules it does not, this becomes the precedent for every error surface.

**Q2 — ⛔ Should a PENDING confirmation get a roundel of its own?**
Confirmation's 56px roundel is built for a **tick**: its mark is a page-cutout, and the entire dark
policy (white shape, black mark, ruled by Dave 2026-07-02 eve) exists so that cutout stays legible.
**There is no ruled roundel for "accepted but not finished."** Minting one would be a decision
inside the RAG policy's own neighbourhood, so the pending variant takes no success device at all —
decorative glyph plus a Status-indicator chip carrying the word. **His.**

**Q3 — Should an error page offer a support route at all?**
The brief's do-not-rule list is obeyed to the letter: no phone number, no chat link, no "contact
us", no promise anyone is looking, no service-status claim. A neutral reference code is shown and
**nothing is asserted about what it is for**, which is arguably worse than showing nothing. That is
a product decision.

**Q4 — ⛔ Is the Layer-2 artefact class right, and is `$layer` the right key?**
Carried unchanged from wave 5 (Q1/Q2 there), because it has not moved: these ship as
`snippets/<Name>.reference.html` + `components/<slug>.meta.json` so every existing gate watches them
for free, and `layer` is schema-illegal so `$layer` is used. But a `$`-key is an **annotation** by
the schema's own grammar. If Layer-2 membership is meant to be **queryable structure**, it wants a
real enum property and a schema amendment. **Not a worker's call.** ⚠ And `$layer` still has **no
consumer** — nothing reads it ([[instrument-without-a-consumer]]).

**Q5 — ⛔ `meta.schema.json` still has no seat for COMPOSITION.**
`relationships` is a **closed** shape (`livesInside` · `mustNotNeighbour` · `commonPatterns` ·
`triggeredBy`). There is no edge for *"the components this organism is assembled from"* — the
**defining** relationship of a template. The list is carried as `$composes` so it is greppable but
does not pretend to be a graph edge. Wave 5 raised this; **five more files now depend on it.**

**Q6 — ⛔ Do reports need a NARROW chart specimen?**
D3's arithmetic says two 580px canvases cannot sit side by side in a 1120px page **at any width**.
A report that wants two charts abreast needs a second canvas width **in the chart components
themselves**. That is a dataviz decision and it is bigger than this template.

**Q7 — ⛔ What does a template do about a byte-lifted chart's DEMO DATA?**
D4 is a general problem: borrow verbatim for provenance and the chart lies about the page; change
the labels and the byte-diff weakens. This lane split the difference (geometry byte-identical, copy
replaced, both stated). **Is that the rule?** And separately: `Template-dashboard` still ships the
contradiction.

**Q8 — The six type-composite weight deltas are unchanged from wave 5, and now bite harder.**
Every borrowed rule lost its raw font declaration. The visible consequences here: errored/completed
inputs no longer go to weight 500; Selection-controls' labels drop from 500 to 400; Summary's value
row loses its 500. **And D1 shows the cost is not only weight** — dropping
`font:400 16px/24px` took the **line-height** with it and clipped every descender. ⬛ The root cause
is one call, not eight: **the canon ramp has no 16/500 INPUT or LABEL composite, and `.t-cm-input`
is `line-height:1`.** Widen the ramp, or accept that Layer-2 carries lighter emphasis than the
Layer-1 components it composes.

**Q9 — ⛔ Three inherited target-size shortfalls, measured and NOT silently fixed.**
`Breadcrumbs`' `.crumb` links measure **~39 × 10.1** (the leading-trim cap box **is** the link box).
`View-options`' `.seg` buttons are **40px** tall. `Data-grid`'s `.dgs-clear` and `.fchip .x` are
**24 × 24**. All three are the SOURCE components' shipped geometry. **A lane must not quietly
enlarge a gated component's target**, so all three are carried and reported. *(Same three wave-5
lane B reported; unchanged.)*

**Q10 — Should a template ship any JavaScript at all?**
Four of these five ship none, and the fifth ships only the segmented indicator's position (which
**must** be measured after layout, so it cannot be authored). Consequence, stated plainly: **the
search box, the chips, the switches, the radios and the sort headers look live and are not.** The
alternative is importing each source's engine, which forks it.

**Q11 — Where does a shell end and a template begin?**
These are the CONTENT region of a page and assume they sit inside a `<main>` — except
`Template-error`, which deliberately assumes it may be served **outside** the shell entirely and so
carries its own minimal masthead. **"A shell wraps a template" is PROPOSED, not adjudicated**, and
Lane A is building four more shells in this same window.

**Q12 — The settings page's section vocabulary, and what belongs on it.**
Your details / Notifications / Statements and documents / Security are PROPOSED. So is the decision
to lock the customer number with a reason in help text rather than hiding it, and the choice of
`rag/information` (not warning) for the "two changes not yet saved" chip — **deliberately not the
warning seat**, which touches the two-red law.

**Q13 — At 420px the settings action bar is no longer the last thing on the page.**
When `.l-split` collapses, the rail stacks **below** the form, so "Save settings" sits above "On
this page". MEASURED: the sticky bar rests 457.8px above the frame bottom at scroll-end. Arguably
correct (in-page navigation belongs near the top on a phone) and arguably wrong. **Unruled.**

**Q14 — Every status vocabulary is PROPOSED.** Reconciled / Two exceptions / Awaiting value date
(report); Awaiting a second approver (confirmation); Two changes not yet saved (settings).

**Q15 — The report's five leading figures, its four provenance fields and its four footnotes.**
Which figures a settlement report leads with, and what a report must state about its own
provenance, are product decisions dressed as layout.

**Q16 — An `_ICON-GAPS.md` entry for the empty `error-solid.svg`?** D6. That file is the
conductor's, not this lane's (the #209 Q14 precedent).

---

## 8 · BLAST RADIUS — the global selectors this lane extended (lesson 6)

**Do NOT run `--update`; the conductor re-seeds.** This lane extended the reach of the following
`canon/type.css` selectors by using their class names in five new files:

| selector | what it now also matches |
|---|---|
| `.btn` | every action on all five pages (settings 2, empty 3, error 4, report 2, confirmation 4) |
| `.seg button` and `.seg.sm/.md/.lg button` | settings (2 controls) and report (1 control) |
| `.status` | settings (1 chip), report (5 chips), confirmation (1 chip) |
| `.chip` | **not used** — declared so its absence is not mistaken for an omission |

⚠ **One deliberate departure, declared rather than avoided:** `Empty-state` namespaces its action
button `.ebtn` **precisely so the `.btn` classname's type.css blast radius does not escape**.
`Template-empty` uses `.btn` anyway, because the page around it already carries Button atoms and two
button families on one page is the collision class this wave keeps finding. **That is a considered
trade against a gated component's own stated intent, and it is the conductor's to accept or reject.**

---

## 9 · WHAT STAYS UNPROVEN — declared, not smoothed

1. **⛔ CONSOLE, LEGACY AND SUPERCHARGE ARE UNPROVEN FOR ALL FIVE.** `_validate_binds_resolve.py`
   check D fails: no `.cn-template-*` block exists in `canon/canon.css`, so theme-cascade projection
   is **silently OFF**. Only the light and dark legs authored in each snippet have been seen. Given
   [[four-themes-flexibility-is-the-requirement]], **this is the largest single gap in this
   delivery** — and D2 makes it sharper, because `--muted` dangling was invisible *only because*
   Mono collapses `text/secondary` onto `text/default`. **A theme that forks them would have shown
   it.** Projecting the blocks is the conductor's and is a precondition of any four-theme claim.
2. **`_validate_kg.py` FAILS.** Five new metas; `gen_kg_edges.py` must be re-run. Shared generated
   files — **conductor's**. ★ Made as cheap as possible: **zero** new node-ids (claim 17).
3. **`_validate_state_contrast.py` NOT RUN** — a filtered run overwrites the tracked
   `_STATE-CONTRAST-AUDIT.md`, outside this lane's fence. Same declaration Lane P made at #204, Lane
   A at #209 and Lane B/C at #210 wave 5. **Still owed** — and it is precisely the gate that checks
   the non-colour carrier against real DOM, which is where these files' `data-carries` attributes
   are supposed to land.
4. **No contrast ratio was RE-MEASURED.** Every colour pair is one a gated component already ships
   and the a11y gate reports 0 failures over all 135 snippets, but this lane computed no ratios of
   its own. **Carried, not verified.**
5. **One browser, one zoom, one engine.** Headless Chromium at three viewport widths. No second
   engine, no zoom pass, no 200%-text pass, no forced-colours pass, no 320px pass, no real
   screen-reader pass. The ARIA is authored and structurally checked; **it has not been LISTENED to.**
6. **No reduced-motion render.** The `prefers-reduced-motion` blocks are present and gate-checked
   statically; Confirmation's entrance was never rendered with the media feature forced on.
7. **The pages are not interactive and have never been driven as a task.** Nothing sorts, filters,
   pages, saves or switches. Keyboard order was not walked end-to-end.
8. **The `svh` unit is Chromium-measured only.** `min(52svh, 420px)` and `min(64svh, 520px)` were
   read in one engine; the mobile-chrome behaviour `svh` exists for was never exercised.
9. **The Layer-2 artefact class still has no gate of its own.** These files pass the COMPONENT gates
   because they are shaped like components. **Nothing checks that a template composes rather than
   re-draws** — the diff-proof in §6 is a script in a receipt, not a gate, and it dies with this
   session unless someone homes it. *(Wave 5 said this. It is still true, and there are now eleven
   templates.)*
10. **⛔ D1's CLASS IS ALMOST CERTAINLY LIVE IN THREE WAVE-5 FILES.** `Template-create-edit`,
    `Template-wizard` and `Template-auth` all dropped `Form-layout`'s raw font and bound
    `.t-cm-input`. **This lane did not open them and does not claim they are broken** — it claims
    the condition that broke this one is present in them, and that a measurement is owed.
11. **D4's contradiction is live in `Template-dashboard`, unmeasured beyond reading its markup.**
12. **Nothing here has been seen by Dave**, nothing is registered anywhere, and every one of the
    sixteen questions in §7 is open.

---

## 10 · THE STORE DOC-ROW FOR THIS RECEIPT

Minted through the store's own writer (`knowledge/_state.py` `add()`, which refuses a row with no
close condition) at receipt creation, per the return contract and the #185 forgotten-document class.
**Exactly one row; the component rows and the wave row are the conductor's.**

| field | value |
|---|---|
| id | **`W-82`** |
| home | `notes/_receipts/2026-08-20-210-wave6-laneB-p3-templates.md` |
| owner / state / opened | `dave` · `open` · `210` |

⚠ **CONCURRENCY HAZARD, DECLARED.** Lanes A, B, C and D all write `knowledge/_state.json` in the
same window; `_state.py` does read-modify-write with no lock. The next free id was **`W-82`** when
this lane re-read the store immediately before writing (`W-01`…`W-81` taken, with `W-80`/`W-81`
already added by sibling lanes during this session). This lane **re-read the store after writing and
asserted its own row survived**, but it cannot assert that nobody else's was lost. **The conductor
must verify all four lane rows are present before committing.**

---

## 11 · HANDOFF TO THE CONDUCTOR — the serial set this lane could not touch

1. **`.cn-template-settings`, `.cn-template-empty`, `.cn-template-error`, `.cn-template-report`,
   `.cn-template-confirmation` blocks in `canon/canon.css`** — clears 5 check-D failures and is the
   **precondition for any four-theme claim** (unproven item 1).
2. **Re-run `gen_kg_edges.py`** — clears `_validate_kg.py`. Zero new node-ids to absorb.
3. `component-types.json` · `CATEGORIES` · `gen_showroom.py` · `_validate_radius.MIGRATED_SNIPPETS`
   registrations, **if these five are to be kept** (Q4).
4. **Store rows for the five new artefacts** — the #185 forgotten-document class. This lane minted a
   row for the RECEIPT only.
5. ⬛ **A MEASUREMENT OWED AGAINST THREE WAVE-5 FILES.** D1's condition (raw
   `font:400 16px/24px` dropped, `.t-cm-input` bound, `<input>` clips, trim `:is()` includes
   `input[type=…]`) is present in `Template-create-edit`, `Template-wizard` and `Template-auth`.
   The probe is two lines: `scrollHeight - clientHeight` per input, plus the computed
   `text-box-edge`. **Not this lane's files.**
6. ⬛ **A DEFECT REPORT AGAINST `Template-dashboard`** (D4): its byte-lifted chart says "Where the
   money went — Groceries, Transport, Housing" on a business banking overview page.
7. ⬛ **A LIBRARY REPORT: `knowledge/assets/icons/status-icons/error-solid.svg` IS EMPTY** (D6). An
   `_ICON-GAPS.md` entry is the conductor's call (Q16).
8. ⬛ **THREE GATE CANDIDATES, priced by evidence in this receipt, none built:**
   **(a)** the **var-resolution gate** already named in `_DS-IMPROVEMENTS.md` — this receipt is its
   **third** live catch and the **first where the defect had no visual signature at all** (D2), which
   is a strictly stronger argument than either predecessor;
   **(b)** a `--computed` leg for `_validate_descender_clip.py`, which today has **no concept of an
   `<input>`** and passed a 9px clip on 151 files (D1);
   **(c)** an **artefact-vs-artefact consistency** check — a chart and a table on one page that claim
   to describe the same thing (D4). This one is genuinely hard and may not be worth building; it is
   named so the cost is visible rather than assumed away.
9. ⬛ **A twice-caught promotion candidate for `W-45`/`W-48`:** the crushed-shrinkable-child class,
   now **n=3** across #209 and #210, mechanically probeable (D5). **Promotion vocabulary is still
   open (`W-51`) — naming a candidate, not promoting one.**
10. ⚠ **BLAST RADIUS, DECLARED, DO NOT `--update`:** §8.
11. ⚠ **RUNNING THE GATES REWROTE TRACKED FILES — declared, not hidden.** `git status --short
    knowledge/` shows `knowledge/_A11Y-GATE.md`, `knowledge/_SNIPPET-AUDIT.md`,
    `knowledge/_ICON-SOURCE-AUDIT.md` and `knowledge/_COMPOSE-AUDIT.md` modified as a **side effect**
    of the gate runs quoted above, plus `knowledge/_state.json` (the doc-row) and
    `notes/_REHEARSAL-LOG.jsonl`. **No lane edited any of these by hand**; they are gate-authored
    outputs **shared with Lanes A, C and D**, which ran the same gates, so attribution is the wave's
    and not any one lane's. **Reconcile every path deliberately — never `git add -A`.**
12. ⚠ **Not this lane's, named so it is not misattributed:** at the time of writing, `git status`
    also shows a large set of untracked sibling-lane files (`App-shell-*`, `*-lockup.*`,
    `Hero-variants.*`). Recorded only so the wave's history is honest.
