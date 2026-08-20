# Receipt — #210 Wave 5 · Lane C · the form-class Layer-2 templates

**Lane:** C (Opus) · **Session:** #210 · **Date:** 2026-08-20
**Brief:** `notes/_briefs/2026-08-20-210-wave5-layer2-p2-fanout-brief-v1.md` (THE JOB, LANE C)
**Members:** row 107 create/edit form · row 109 multi-step wizard · row 112 auth (log on / register / OTP)

> ⛔ **NOTHING IN THIS RECEIPT IS A RULING.** The artefact class itself ("a Layer-2 row ships in
> the library's grammar: `snippets/<Name>.reference.html` + `components/<name>.meta.json`") is the
> brief's **PROPOSED** convention and is Dave's to re-home. Every domain and design call below is
> PROPOSED (`s182-D2`, the Kpi-tile precedent). **No registration of any kind was performed** — no
> `CATEGORIES`, no `MIGRATED_SNIPPETS`, no `component-types.json` membership, no `canon.css` block,
> no `_rulings.json` line, no `gen_kg_edges.py` run, no git operation. This lane created **new
> files only** and edited **no existing file**.

---

## 0 · THE HEADLINE — three findings that matter more than the three files

**(a) ⛔ THE AUTH TEMPLATE NEVER COLLAPSED, AND ONLY A MEASUREMENT CAUGHT IT.**
The first draft declared `container-type: inline-size` on `.auth` itself and then wrote
`@container (max-width:880px){ .auth{ grid-template-columns: 1fr } }`. **That rule can never fire:
an element is a query container for its DESCENDANTS, never for itself.** Measured
`getComputedStyle('.auth').gridTemplateColumns` at three viewports: **`565px 565px` at 1180 ·
`355px 355px` at 760 · `185px 185px` at 420** — the whole log-on form crushed into 185px on a
phone. **Every gate was green** (grid, type, a11y, descender, icons, snippets, meta-schema) and the
420px full-page screenshot looked plausible enough to accept. Repaired by moving the container to
an `.auth-shell` wrapper; re-measured **`565px 565px` / `710px` / `370px`**.
★ The sibling templates were never affected — their queried elements (`.tpl-cols`, `ol.steps`) are
*descendants* of `.tpl`. **A container query written against its own container is a dead rule with
no failing observer, and this repo has no gate that can see one.** Priced as a gate candidate in §7.

**(b) ⛔ THE BRIEF'S PROPOSED META KEY `"layer": "2 Template"` IS SCHEMA-ILLEGAL.**
`knowledge/components/meta.schema.json` is `additionalProperties: false` with
`patternProperties: {"^\\$": {}}`. A bare `layer` key therefore FAILS probe P-1. The legal form is
**`$layer`**, which is what all three metas carry. Verified the same way, the hard way: my first
`template-auth.meta.json` used a bare `brandMark` key and P-1 returned
*"'brandMark' does not match any of the regexes: '^\\$'"* — that is now `$brandMark`. **This is a
correction to the brief's own PROPOSED artefact-class convention**, not a rename I made quietly.

**(c) ★ ROW 109 MAY BE A DUPLICATE, AND I SAY SO ON THE FILE'S OWN FACE.**
`Stepper.reference.html` is **already** an interactive wizard — step panels, validation-gated Next,
back-navigation on completed dots, focus management, sr-live announcer. Row 109 is a missing PAGE,
not a missing mechanism. `Template-wizard` adds exactly four things over Stepper: page scale; REAL
form steps (Stepper's panels are demo prose that says so itself); a REVIEW step (Summary's `<dl>`
with per-row Change links — Stepper has none); and an END STATE (Confirmation — Stepper's last Next
writes a string to a live region and stops).
⬛ **LIVE OUTCOME, not a hedge:** if Dave rules a wizard template is just Stepper with content
poured in, **delete the pair and mark row 109 Duplicate against `component:stepper`.** Deleting
costs nothing — nothing points at it. That call is his. (This is the #209 Lane A shape, deliberately.)

---

## 1 · FILE LIST — six new files, plus this receipt

| # | path | bytes |
|---|---|---|
| 1 | `knowledge/snippets/Template-create-edit.reference.html` | 50,973 |
| 2 | `knowledge/components/template-create-edit.meta.json` | 11,610 |
| 3 | `knowledge/snippets/Template-wizard.reference.html` | 50,576 |
| 4 | `knowledge/components/template-wizard.meta.json` | 12,230 |
| 5 | `knowledge/snippets/Template-auth.reference.html` | 51,233 |
| 6 | `knowledge/components/template-auth.meta.json` | 14,165 |
| 7 | `notes/_receipts/2026-08-20-210-wave5-laneC-form-templates.md` | this file |

**No existing file was edited.** Renders live OUTSIDE the repo
(`(NON-REPO: the session outputs folder, laneC-renders/*.png` — 18 full-page PNGs, light + dark ×
3 widths × 3 members, plus 5 driven-state shots`)`) per `s191-D2` home-or-declare. They are working
artefacts, not deliverables. No `intent` field was authored (W-58 parked; none of these is a chart).

---

## 2 · CLAIM TABLE — every claim carries a probeable token (`s182-D1`)

Run from the repo root. Where a probe's FORM is load-bearing, the false form is printed beside it.

| # | claim | probe — re-runnable, exactly as written | verdict |
|---|---|---|---|
| 1 | The AUTO-TOKENS block is byte-identical to Form-layout's generated block in all three | `python3 -c "import re;s=open('knowledge/snippets/Form-layout.reference.html').read();i=s.index('/* ===== AUTO-TOKENS START');j=s.index('AUTO-TOKENS END ===== */',i)+24;b=s[i:j];print([b in open('knowledge/snippets/Template-%s.reference.html'%n).read() for n in ('create-edit','wizard','auth')])"` → **`[True, True, True]`**, 1,325 chars | ✅ |
| 2 | The leading-trim block is the CURRENT one, byte-identical to Command-palette line 36 | `python3 -c "cp=open('knowledge/snippets/Command-palette.reference.html').read().split(chr(10))[35];print(all(cp in open('knowledge/snippets/Template-%s.reference.html'%n).read() for n in ('create-edit','wizard','auth')))"` → **True**, 328 chars | ✅ |
| 3 | The AUTO-PARTIAL press-physics block is the injected form, not a re-typed one | the `/* INJECTED from Button.reference.html … gen_component_partials.py */` header block from Form-layout appears verbatim in all three → **True ×3** | ✅ |
| 4 | Borrowed `.fl-*` bodies are byte-identical, at-rules stripped so a media override cannot masquerade as a delta | create-edit **55 of 57** shared selectors byte-identical · wizard **27 of 28** · auth **42 of 45**. **Every delta is a removed RAW FONT declaration** (claim 9) except `.fl-actions{margin}` (the template owns its action-bar spacing) | ✅ |
| 5 | Borrowed `.se-*` code-cell bodies are byte-identical to Secure-entry | **23 of 23** shared selectors identical, zero deltas | ✅ |
| 6 | Borrowed `.confirm*` bodies are byte-identical to Confirmation | **5 of 5** identical (its `@media(max-width:480px)` override is out of scope for the template and is not carried) | ✅ |
| 7 | Borrowed `.content-header` bodies match Headers | **4 of 6** identical. Delta 1: `h1` loses `font:400 20px/1.2` (claim 9). Delta 2: `background:var(--hover)` → `var(--field-bg-hover)` — the **same token** (`form/background/hover`), rebound to the name this file already declares rather than duplicating the var | ✅ |
| 8 | The Confirmation success glyph is byte-matched, not re-drawn | the 163-char `d="M9 0C4.03…"` path from `Confirmation.reference.html` appears verbatim in `Template-wizard` → **True**; and `python3 knowledge/_validate_icons.py Template-wizard` → *"0 UNKNOWN, 0 bespoke"* | ✅ |
| 9 | ⚠ **THE ONE SYSTEMATIC DELTA:** every raw font declaration in every borrowed rule was dropped and the canon composite bound in MARKUP | `python3 knowledge/_validate_type_composites.py knowledge/snippets/Template-{create-edit,wizard,auth}.reference.html` → **TYPE GATE PASS** on each. Six weight/size consequences are named in §4 as OPEN QUESTIONS | ✅ **and it changes what you see** |
| 10 | Type-composite debt UNCHANGED — these three add ZERO | `python3 knowledge/_validate_type_composites.py` → *"1097 violation(s) across 90/134 file(s)"*, the #203 measured baseline, and `… \| grep -c "Template-create-edit\|Template-wizard\|Template-auth"` → **0** (my files are named zero times) | ✅ |
| 11 | 4px-grid gate clean | `python3 knowledge/_validate_grid.py` → *"GRID GATE PASS — all layout dimensions on the 4px grid (135 file(s))"* | ✅ |
| 12 | a11y gate: zero failures with all three present | `python3 knowledge/_validate_a11y.py` → *"a11y gate: 119 snippet(s), 0 failure(s), 249 warning(s)"* (119/249 are WAVE-wide — Lanes A/B/D added files concurrently; baseline before this wave was 108/221) | ✅ |
| 13 | Descender-clip gate clean | `python3 knowledge/_validate_descender_clip.py` → *"PASS — every truncating label is descender-safe (135 file(s))"* | ✅ |
| 14 | Snippet/token gate clean — and it CAUGHT me once | `python3 knowledge/_validate_snippets.py` → *"snippet gate: 119 snippet(s), 0 failure(s)"*. ⚠ It first FAILED on `Template-auth`: *"ALL-CAPS text run 'THE CODE IS NOT CHECKED AGAINST ANYTHING' — banned outside acronyms (type26-019)"*. My emphasis in body copy broke a house rule; rewritten in sentence case | ✅ **after a real catch** |
| 15 | The metas are schema-valid — and P-1 caught the `brandMark` key | `python3 knowledge/_probe_registry/probe_meta_schema.py --check` → *"117 meta(s) checked · 0 finding(s) · 1 exempt failure(s)"*. Before the fix: *"⛔ template-auth.meta.json [<root>] 'brandMark' does not match any of the regexes: '^\\$'"* | ✅ **after a real catch** |
| 16 | Icon gate: nothing invented in any of the three | `python3 knowledge/_validate_icons.py Template-create-edit` / `Template-wizard` / `Template-auth` → *"0 UNKNOWN, 0 bespoke"* each; and the corpus run's 17 UNKNOWN name **no Lane C file** (`… \| grep -iE "template-(auth\|wizard\|create)"` → no output) | ✅ |
| 17 | ⛔ **binds-resolve check D FAILS for all three — DECLARED, not hidden** | `python3 knowledge/_validate_binds_resolve.py` → *"no `.cn-template-auth` / `.cn-template-create-edit` / `.cn-template-wizard` block in canon.css — project_canon projection is silently OFF"*. **Five sibling-lane files are in the same state** (`Filter-toolbar-bar`, `Page-header-lockup`, `Template-dashboard`, `Template-detail`, `Template-list-index`) | ⛔ **CONDUCTOR'S** |
| 18 | ⛔ `_validate_kg.py` FAILS — new metas, stale generated node registries | `python3 knowledge/_validate_kg.py` → *"_nodes-pattern.json DRIFTED … _nodes-context.json DRIFTED"*. `gen_kg_edges.py` must be re-run. **Shared generated files — conductor's** | ⛔ **CONDUCTOR'S** |
| 19 | ★ **Zero NEW context or pattern node-ids were minted by this lane** | `python3 -c` over `_nodes-context.json` / `_nodes-pattern.json`: every `usedInContext` and `commonPattern` ref in all three metas resolves → **UNRESOLVED: []**. ⚠ My FIRST draft minted `context:payments`, `context:account-management`, `context:authentication`, `pattern:log-on`, `pattern:register`, `pattern:set-up-a-payment` … — **6 of 8 patterns and 3 of 4 contexts did not exist.** Replaced with the nearest existing node before writing | ✅ **after a real catch** |
| 20 | The official brand mark actually LOADS, one per theme, and is never re-drawn | headless Chromium: all six `<img>` report `naturalWidth > 0`; exactly **one visible per theme** (light in light, dark in dark); **160 × 43** CSS px; `alt="HSBC"`; **zero failed network requests**; and `grep -c crescent` → 3, **all three in PROSE stating the #86 fence** — no crescent asset is referenced anywhere | ✅ **DRIVEN** |
| 21 | ⚠ **PROBE FORM IS LOAD-BEARING (and my first one was FALSE):** no other gated snippet references an external image | `grep -l '<img' knowledge/snippets/*.reference.html` → **2 files** and is a **FALSE probe** — Image-block's hit is the string `<img alt="…">` inside its header COMMENT. Correct form: `grep -l '<img[^>]*src=' knowledge/snippets/*.reference.html` → **`Template-auth` only** (6 hits here, **0** in Image-block) | ✅ **corrected** |
| 22 | `autocomplete` is correct on every credential field (1.3.5) | headless Chromium, read off the live DOM: `[['lg-user','text','username'], ['lg-pass','password','current-password'], ['rg-name','text','name'], ['rg-email','email','email'], ['rg-pass','password','new-password'], ['Digit 1 of 6','text','one-time-code']]`. Every credential field also carries `autocapitalize=none autocorrect=off spellcheck=false` | ✅ **DRIVEN** |
| 23 | The wizard actually WALKS, end to end, in a real browser | headless Chromium: Next with nothing chosen **BLOCKED** (summary open, `aria-invalid="true"`, panel 1 still shown) → choosing a payee advanced and moved focus to *"How much, and when?"* → `abc` in Amount **BLOCKED** with *"Enter an amount, like 250.00."* → the review step populated **from the live fields** (`Jane Smith` / `£250.00` / `RENT-AUG` / `2026-08-21`) → a Change link returned to step 2 → the Next label became **"Confirm and send"** at the review step → the last step showed the Confirmation and **the wizard's own bar retired** (`#wiz-bar.hidden === true`) → 3 completed dots were **real `<button>`s** | ✅ **DRIVEN** |
| 24 | The responsive collapse is MEASURED, not eyeballed, at 3 widths | `.tpl-cols` computed `grid-template-columns`: **`714px 320px` → `646px` → `322px`** · `.fl-actions` flex-direction: **row → row → column-reverse** · wizard dots visible: **True → True → False** · `#wiz-bar .st-nav` direction: **row → row → column-reverse** · `.auth` columns: **`565px 565px` → `710px` → `370px`** · OTP cell box: **48×56 → 48×56 → 40×48**. Horizontal overflow at every width, both themes, all three files: **0** | ✅ **DRIVEN** |
| 25 | The real HSBC face rendered, asserted against two controls not a boolean | canvas 40px `Handgloves 12345`: `HSBC_MtUnivers_Latin` **346.88** · `"Univers Next HSBC"` **346.88** · `"Univers Next for HSBC"` **346.88** · `DejaVu Sans` (control) **375.39** · nonexistent face (control) **301.07**. Both aliases land on the target and on neither control | ✅ **DRIVEN** |
| 26 | The library has **no password field** — so one is composed, not drawn | `grep -l 'type="password"' knowledge/snippets/*.reference.html` → only `Secure-entry` (its masked PIN cells) and `Template-auth`. `Input-fields.reference.html` has none | ✅ **NAMED GAP** |
| 27 | The library has **no visibility / eye glyph** — so the reveal control is TEXT | `ls knowledge/assets/icons/*/ \| grep -iE "eye\|visib\|hide\|show\|reveal\|password"` → `masthead-hide.svg`, `masthead-show.svg` (read them: arrows-and-rules, a **masthead collapse** control) and `security-password.svg` (a keyboard-with-dots). **None means "reveal what I typed."** The toggle is a "Show"/"Hide" button with `aria-pressed` | ✅ **NAMED GAP** |
| 28 | The auth specimen contains no authentication logic | `grep -cE 'fetch\(\|XMLHttpRequest\|localStorage\|sessionStorage\|document\.cookie\|crypto\.' knowledge/snippets/Template-auth.reference.html` → **0**. The only comparisons in its script are `length > 0`, `/.+@.+\..+/`, `length >= 12` and `val().length === cells.length` — three format tests and a completeness test | ✅ |

---

## 3 · THREE DEFECTS FOUND BY DRIVING AND MEASURING — every gate green over all of them

This is the most useful section, and it is the #204/#209 lesson repeating a third time.

1. **⛔ THE AUTH TEMPLATE'S TWO PANELS NEVER COLLAPSED** — §0(a). Container-query-on-itself.
   MEASURED `185px 185px` at a 420px viewport. Repaired with an `.auth-shell` wrapper, re-measured.
   *Nothing but reading `getComputedStyle` at three widths could have caught it: the screenshot at
   420px shows two thin plausible columns, not an obvious break.*

2. **⛔ THE GUIDANCE ASIDE'S TERM AND DEFINITION COLLIDED.** Measured `dt` → `dd` gap: **0.0px**.
   `.t-cm-label` is `line-height:1` and `<dt>` sits inside the leading-trim `:is()` list, so the
   term's box collapses onto the definition's first line. **This is [[W-67]]** — the minimum-spacing
   class Dave floated at #210 for exactly this situation (text collisions where line-height trim is
   active). Repaired to **4px**, the smallest grid step that clears it, and re-measured: `4, 4, 4, 4, 4`.

3. **⛔ THE STICKY ACTION BAR PAINTED OVER ITS OWN LIVE FORM.** With two whole templates stacked on
   one reference page, `position:sticky; bottom:0` resolved against the **viewport**, not the
   template: bar **1594–1671** over a form running **1562–2027**, `overlapsForm = true`. Repaired by
   giving each specimen a scrolling `.demo-frame` — which is what a real page is — and re-measured:
   the bar is now **flush with each frame's bottom edge** (`|barBottom − frameBottom| < 1.5px`) and
   both frames scroll.

**And one defect avoided by measuring rather than trusting the canon idiom:** the wizard's review
rows first used the canon `::before` hit expander (aid-009). Measured: a **10.1px** control with a
**44px invisible expander** on a **36.6px** row pitch — adjacent expanders **overlapped by ~7px**.
The a11y gate passes that (it sees a 44px expander; it cannot see that two of them intersect). Given
a REAL 44px box instead, the rows grew to a 68–69px pitch with **25px clear** between controls, and
**15 of 15 hit-test points** (top+1, centre, bottom−1 on each of five controls) land on the intended
control. ⚠ Note the instrument correction inside that measurement: the first hit-test run reported 5
wrong hits, all on the two rows sitting **under the stuck action bar at the initial scroll position**
— an artefact of the viewport, not an overlap. Re-run with `scrollIntoView`, it is 0/15.

**And one FALSE defect I nearly wrote up:** the wizard's primary button measured
`color(srgb 0.371 0.371 0.371)` instead of `#1A1A1A`. That is exactly
`color-mix(in srgb, #1A1A1A 70%, #FFFFFF)` — **the hover state**, because Playwright leaves the
pointer parked where it last clicked. Every reading and screenshot in this receipt is taken after
`mouse.move(2,2)`. With the pointer parked: **`rgb(26, 26, 26)`**. *The document was right; the
instrument was standing on the button.*

---

## 4 · THE SYSTEMATIC DELTA — what binding composites cost, stated plainly

The brief holds two rules that pull against each other: **borrow verbatim** and **type-composite
debt 1,097 may not grow**. Copying the sources' raw `font:` declarations would have added ~20 new
TYPE-002 violations and failed the shrink-only ratchet. So **every borrowed rule kept its structure
and its token bindings, and lost its raw font declaration**; the type arrives from the canon
composite bound in markup. Form-layout's own header sets the precedent ("bound the composite,
awaiting a weight ruling"). **The six visible consequences, none of them smoothed over:**

| # | source rule | what the source renders | what these templates render | where it shows |
|---|---|---|---|---|
| a | `.fl-group.is-error .fl-box input{font-weight:500}` | errored / completed input text goes medium | **400 — the weight cue is gone** | every errored field |
| b | `.st .dot{font-weight:500}` | the step numeral is medium | **`.t-cm-figure-6`, 14/400** | the wizard's dots |
| c | `.st li.current .step-label{font-weight:500}` | the CURRENT step's name is medium | **400** — current is now shown by the ring + full opacity only | the wizard's dots |
| d | `.st .count{font-weight:500}` | "Step 3 of 4" is medium | **400** | the collapsed wizard head |
| e | `.summary__v{font:500 16px/1.4; tabular-nums}` | review VALUES are bolder than their keys | **`.t-cm-label` / `.t-cm-figure-5`, 400** — values no longer outweigh keys | the wizard's review step |
| f | `.content-header h1{font:400 20px/1.2}` | app-bar title 20/400 | **`.t-ed-heading-4`, 20/350** | every app bar |

★ **The single root cause: the canon ramp has no 400→500 pair a composite can express at 14px, 16px
or 20px for these roles.** There is `.t-cm-button` (16/500) and `.t-cm-ctl-12/14` (500), but no
16/500 **input**, no 14/500 **figure**, no 20/400 **heading**. ⬛ **Dave's call, and it is one call
not six: widen the ramp, or accept that Layer-2 templates carry lighter state emphasis than the
Layer-1 components they compose.** A third option exists and I did not take it — fork the raw
declarations into the templates and let the debt grow by ~20 — because the brief fenced it.

**Also declared:** `body{font-family:var(--font)}` is absent from all three (it is TYPE-002 in every
sibling snippet and part of the 1,097). The face arrives via `<body class="t-ed-body">`. `--font`
stays declared, because a custom-property definition is exempt and the token address should stay
readable in the file.

---

## 5 · `$decisionsForDave` — NAMED, NOT SETTLED

**All of these are Dave's. None is answered by construction.**

### Q1 — ⛔ Should `Template-wizard` exist at all? *(the biggest one)*
Stepper is already an interactive wizard. §0(c) states exactly what the template adds and states the
live outcome: delete the pair and mark row 109 **Duplicate** against `component:stepper`. **His.**

### Q2 — ⛔ Is `$layer` the right key, and is the artefact class right at all?
The brief's `"layer"` is schema-illegal (§0(b)); `$layer` is legal. But a `$`-key is an *annotation*
by the schema's own grammar — if Layer-2 membership is meant to be **queryable structure**, it wants
a real enum property and a schema amendment, not an annotation. **Not a worker's call.**

### Q3 — The six type-composite weight deltas — one ruling, six symptoms (§4).
Widen the ramp, or accept lighter state emphasis in Layer-2?

### Q4 — Does the library adopt the `<img>` idiom for brand assets?
`Template-auth` is the first gated snippet with a src-bearing `<img>` (claim 21). Inlining was
rejected on a measurement, not a taste: `_validate_icons.py` byte-matches against `assets/icons/`
only, so an inlined logo lands as **UNKNOWN** — indistinguishable from an invented mark. Two live
outcomes: **adopt `<img>` for logos** (and possibly widen the icon gate to see `assets/logos/`), or
**mint a logos sprite** the way icons have one.

### Q5 — Should the auth brand column carry anything but the mark?
It is deliberately quiet — the mark and one neutral line — because inventing brand imagery is
fenced. At wide widths it is a large empty plate. Fill it, narrow it, or drop the split entirely?

### Q6 — Is "unsaved changes" a WARNING?
Drawn as ink on a hover-wash with the word "Unsaved" carrying the meaning, **deliberately not the
warning seat** — that touches the two-red law (`s151-D1`) and is not this lane's to touch.

### Q7 — Should password requirements be a live tick/cross meter?
Drawn as plain ink list items stated **before** the field and kept visible. A live meter needs a
RAG vocabulary (met / unmet / partially met) this lane has no mandate to mint.

### Q8 — Should the create/edit template lock the account fields, as drawn?
Drawn LOCKED with the reason in help text — changing where money goes is a verified journey, not a
field edit. That is a **product policy** dressed as a layout decision, and it is his.

### Q9 — Where does the guidance aside end and a help pattern begin?
Drawn as read-only guidance in a `<dl>`. Any control in there competes with the form for the same
decision. Is an aside even the right home for this content?

### Q10 — Two of the four review-row values are `.t-cm-figure-5` (tabular) and two are `.t-cm-label`.
Amount and Date are tabular; To and Reference are not. Reasonable, unruled.

### Q11 — ⚠ The step visuals now live in THREE files.
Progress-tracker → Stepper → Template-wizard. Stepper's own receipt already flagged the duplication
at two and queued the fold-or-partial question. **This lane made it three and is saying so.** The
AUTO-PARTIAL mechanism (ADR-0013) exists for exactly this.

### Q12 — An `_ICON-GAPS.md` entry for the visibility glyph?
Claim 27. That file is the conductor's, not this lane's (the #209 Q14 precedent).

### Q13 — Does the create/edit app bar overlap Lane D's row-115 page-header lock-up?
Both were built this session, concurrently. The template borrows `Headers`' `.content-header`
verbatim; Lane D built `Page-header-lockup.reference.html` (it is in the check-D failure list). **The
relationship is stated PROPOSED and adjudicated nowhere** — the #203 sidebar-nav-vs-navigations
shape, one layer up.

### Q14 — Confirmation is a CANDIDATE, not gated.
`confirmation.meta.json` provenance says *"REVIEW: no Figma node yet"*. Borrowing it into a template
does not promote it, and this receipt must not be cited as evidence that it is settled.

---

## 6 · WHAT STAYS UNPROVEN

1. **Console, Legacy and Supercharge are UNPROVEN for all three templates.** `_validate_binds_resolve.py`
   check D FAILS (claim 17) — no `.cn-*` blocks exist, so theme-cascade projection is silently OFF.
   **Only the light and dark legs authored in each snippet have been seen.** [[four-themes-flexibility-is-the-requirement]]
   says test PER THEME; that test has not been run and I am not claiming it was.
2. **`_validate_state_contrast.py` NOT RUN** — a filtered run overwrites the tracked
   `_STATE-CONTRAST-AUDIT.md`, outside this lane's fence. Same declaration Lane P made at #204 and
   Lane A at #209. **Owed.** It is the gate that checks the non-colour carrier against real DOM,
   which is precisely where these three files' declared `contrastPairs` absences are supposed to land.
3. **One browser, one zoom.** Headless Chromium at 1180 / 760 / 420 CSS px. No second engine, no zoom
   pass, no 320px pass, no real touch device. The `s210-D3` claim that no molecule gets a new fixed
   width is proven by reading the CSS, not by a 320px render.
4. **No reduced-motion render.** The `prefers-reduced-motion` blocks are present and gate-checked
   statically; the Confirmation entrance was never rendered with the media feature forced on.
5. **Contrast ratios are CARRIED, not re-measured.** Every value in these files came in with a
   borrowed region and its source's declaration. Nothing was re-computed at #210.
6. **The `.demo-frame` fix is a REFERENCE-PAGE fix.** It proves the sticky bar sticks to a scrollport.
   It does not prove the template behaves correctly as a whole page inside a real app shell — that
   seam belongs to Lane A's shells and was not tested jointly.
7. **The `$layer` convention is used but has no consumer.** Nothing reads it. [[instrument-without-a-consumer]]:
   a field nothing queries is a claim, not a mechanism. Declared.
8. **Nothing here has been seen by Dave**, nothing is registered anywhere, and every one of the
   fourteen questions in §5 is open.

---

## 7 · HANDOFF TO THE CONDUCTOR — the serial set this lane could not touch

1. **`.cn-template-create-edit`, `.cn-template-wizard`, `.cn-template-auth` blocks in `canon/canon.css`**
   (clears 3 of the 8 check-D failures; the other 5 are Lanes B/D's).
2. **Re-run `gen_kg_edges.py`** (clears `_validate_kg.py`). ★ Made cheaper deliberately: this lane
   minted **zero** new context or pattern node-ids (claim 19).
3. **`component-types.json` · `CATEGORIES` · `gen_showroom.py` · `_validate_radius.MIGRATED_SNIPPETS`**
   registrations, if these three are to be kept.
4. **Store rows** for the three components and for this receipt — the #185 forgotten-document class.
   This lane minted **one** row for the receipt (§8); the three component rows are the conductor's
   call, because whether they exist is Q1/Q2.
5. ⚠ **A GATE CANDIDATE, PRICED, NOT BUILT — the dead container query (§0(a)).** The condition is
   mechanically checkable and needs no browser: *for every `@container` rule whose selector matches
   an element that itself declares `container-type`, and which has no other container ancestor, the
   rule cannot fire.* A CSS-text probe over `knowledge/snippets/*.reference.html` would have caught
   this one in milliseconds. Nothing in the repo looks for it today. It belongs in
   `_DS-IMPROVEMENTS.md` / the probe registry — **the conductor's, and Dave's to promote.**
6. **The brief's `"layer"` key needs correcting to `$layer`** wherever it is quoted, or the schema
   needs widening (Q2). Three sibling lanes were briefed with the same illegal key.
7. ⚠ **RUNNING THE GATES REWRITES TRACKED FILES, AND THAT IS DECLARED, NOT HIDDEN.** Measured with
   `git status --short` at the end of this lane, the tracked files carrying gate-authored changes are
   exactly four: `knowledge/_A11Y-GATE.md`, `knowledge/_SNIPPET-AUDIT.md`,
   `knowledge/_ICON-SOURCE-AUDIT.md`, `notes/_REHEARSAL-LOG.jsonl`. *(I first typed a fifth,
   `knowledge/_graph-mark-observations.jsonl`, carrying it forward from the #209 receipt — `git status`
   does not show it, so it is struck. A carried claim is still a claim.)* `knowledge/_state.json` is
   also modified: that one IS deliberate and is §8's row plus the sibling lanes'. **No lane edited any
   of these by hand**, and all four are shared with Lanes A, B and D, which ran the same gates —
   attribution is the wave's, not any one lane's. Two further modified paths
   (`notes/_dream/_GRADE-DECISIONS.jsonl`, `reviews/ITINERARY-STATUS-2026-08-19-v1.{json,html}`) were
   **already dirty when this lane opened** and are not the wave's.
   **Reconcile every path deliberately — never `git add -A`.**
8. **Rows 107 / 109 / 112 still read `Gap` in `reviews/ITINERARY-STATUS-2026-08-19-v1.json`.** The
   itinerary files are fenced; **not merged by this lane.**

---

## 8 · THE STORE ROW MINTED BY THIS LANE

**`W-76`** — *"#210 wave-5 lane C: three Layer-2 form templates BUILT PROPOSED-NOT-RULED (create/edit,
wizard, auth) - Daves eye owed, 14 named questions incl. two existence questions"*, owner `dave`,
state `open`, `closes_when` stated (Q1 / Q2 / Q3 named explicitly), homed at this receipt.
Written through `knowledge/_state.py add()`, which refuses an item with no close condition.

⚠ **Three sibling lanes were minting concurrently, so the id was DERIVED AT WRITE TIME, not reserved.**
`knowledge/_state.json` was re-read immediately before the write and the next free `W-` id taken from
the live file: **`W-75` had already been claimed by Lane D** (page-header + filter-toolbar lock-ups),
so this lane took **`W-76`**. Re-read after writing: exactly one `W-76`, and
`python3 knowledge/_state.py` reports *"items 97 · live 65 · conditioned 78 · UNCONDITIONED 19"* —
the frozen 19 unchanged, so this row added a CONDITIONED item and did not grow the declared debt.
