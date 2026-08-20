# Receipt — #210 Wave 4 · Lane A · calendar + tree

**Lane:** A (Opus) · **Session:** #210 · **Date:** 2026-08-20
**Brief:** `notes/_briefs/2026-08-20-210-wave4-heavy7-fanout-brief-v1.md` (THE JOB, Lane A)
**Members:** calendar (the standalone month grid) · tree (recursive disclosure)
**Precedent followed:** `notes/_receipts/2026-08-20-209-wave3-laneA-fintech-rows.md`

> ⛔ **NOTHING IN THIS RECEIPT IS A RULING.** Every design and domain semantic below is
> PROPOSED and is Dave's (the Kpi-tile precedent, `s182-D2`). No `CATEGORIES`,
> `MIGRATED_SNIPPETS`, `component-types.json`, `canon.css`, `_rulings.json`, `_ICON-GAPS.md`
> or git operation was touched. **NEW FILES ONLY**, plus the one store doc-row this receipt
> is required to mint. No existing file was edited — in particular **Date-picker,
> Sidebar-nav and `_a11y_target.py` were NOT touched**, and each of those carries a finding
> below that this lane deliberately did not repair.

---

## 0 · THE HEADLINE: FIVE DEFECTS, EVERY ONE OF THEM UNDER A GREEN GATE CHAIN

Three of the five are in **components that were already gated and promoted**, and were found
only because this lane drew the same anatomy in real markup and then drove it.

| # | defect | where | how it survived | repaired here? |
|---|---|---|---|---|
| 1 | **today + selected = an invisible ring** (measured **1.21:1** light, **1.00:1** dark) | this lane's draft AND **the gated Date-picker**, same class | no gate compares a box-shadow against the background it is painted on | ✅ in Calendar · ⛔ **Date-picker unrepaired — conductor's** |
| 2 | **every tree row label clipped its descenders** ("Northwind Holdings" → "Holdinas"), clientHeight **12** vs scrollHeight **18** | this lane's draft AND **the gated Sidebar-nav**, identical cause | `_validate_descender_clip.py` reads the DECLARATION, not the CASCADE — the `text-box-edge:text text` override **loses on specificity** | ✅ in Tree · ⛔ **Sidebar-nav unrepaired + a GATE finding — conductor's** |
| 3 | **the indent selector for loading/empty rows matched NOTHING** — measured `padding-left: 0px` where 56px was intended | this lane's draft | a selector that matches nothing is silent in every gate | ✅ |
| 4 | **the view-only node was a 2.52:1 ghost** (light; 3.79:1 dark) | this lane's draft | disabled-ish content is exempt from 1.4.3 | ✅ (a CATEGORY correction — see §5) |
| 5 | **`_a11y_target.py`'s role vocabulary is missing four roles** — `gridcell`, `rowgroup`, `tree`, `treeitem` | the shared gate | Date-picker's grid is built in **JavaScript**, and no static gate can read JavaScript-built markup | ⛔ **NOT this lane's — see §6** |

★ **The structural tell, and it is the reusable one:** *#2 is not a missing declaration, it is a
lost cascade.* The leading-trim block every snippet carries is
`:is(button,a,label,span,…,input[type=text],…):not(:has(svg))`. `:is()` takes the specificity of
its **most specific argument** — `input[type=text]` = (0,1,1) — and `:not(:has(svg))` adds
(0,0,1), so that rule lands at **(0,1,2) and beats any single class (0,1,0)**. Every component
that "overrides" it with a bare `.some-label{text-box-edge:text text}` is **not overriding it**.
The gate is green because the string is present. **The fix in this file is a selector, not a
property**, and the gate cannot tell the two apart.

---

## 1 · FILE LIST — four new files, plus this receipt

| # | path | bytes |
|---|---|---|
| 1 | `knowledge/snippets/Calendar.reference.html` | 37,939 |
| 2 | `knowledge/components/calendar.meta.json` | 11,010 |
| 3 | `knowledge/snippets/Tree.reference.html` | 36,417 |
| 4 | `knowledge/components/tree.meta.json` | 12,359 |
| 5 | `notes/_receipts/2026-08-20-210-wave4-laneA-calendar-tree.md` | this file |

*(Measured with `wc -c` after the last repair. If a later edit lands they drift — re-run `wc -c`
rather than quoting this table.)*

**No existing file was edited.** No `intent` field was authored on either meta (`W-58` parked;
neither is a chart). Working renders live OUTSIDE the repo
(**`NON-REPO`: the session outputs folder — `cal-{light,dark}.png`, `tree-{light,dark}.png`
plus three cropped 2-up composites**) per `s191-D2` home-or-declare. Drive scripts likewise
(**`NON-REPO`: `/var/tmp/210lA/*.py`**) — working artefacts, not deliverables.

---

## 2 · PREMISE, RE-PROBED IN-LANE (the brief's premise is not evidence)

| probe, exactly as run | result |
|---|---|
| `ls knowledge/snippets/ \| grep -icE "^(Calendar\|Tree)\."` | **0** |
| `ls knowledge/components/ \| grep -icE "^(calendar\|tree)\."` | **0** |
| `grep -rli 'role="tree"' knowledge/snippets/` | **no output** (0 files) |
| `grep -rl 'role="gridcell"' knowledge/snippets/` | **no output before this lane** — Calendar's first draft was the corpus's FIRST static `role="gridcell"`, which is exactly why it surfaced finding 5 |

---

## 3 · CLAIM TABLE — every claim carries a re-runnable probe (`s182-D1`)

Run from the repo root. Browser claims were driven in headless Chromium
(`chromium_headless_shell`, `--no-sandbox --disable-dev-shm-usage --disable-gpu`,
`goto file://…`, 1180px viewport) with the real HSBC cut asserted against two controls.

| # | claim | probe — re-runnable, exactly as written | verdict |
|---|---|---|---|
| 1 | The HSBC cut rendered; the render is not a silent fallback | canvas width of `40px 'Handgloves 12345'`: `HSBC_MtUnivers_Latin` **346.88** · `"Univers Next HSBC"` **346.88** · `"Univers Next for HSBC"` **346.88** · control `DejaVu Sans` **375.39** · control nonexistent face **301.07**. Both aliases hit the target AND differ from both controls (`_RUNBOOK-render-verify.md` § ASSERT WITH A CONTROL) | ✅ **DRIVEN** |
| 2 | ⛔ **today+selected is an invisible ring, and the test CAN fail** — a MUTATION test, not an assertion | in-page: read `boxShadow` + `backgroundColor` of `#cell-today-selected`, then inject `.cal-day.is-today[aria-selected="true"]{box-shadow:inset 0 0 0 2px var(--border-active)!important}` and re-read. **REPAIRED 17.40:1 (light) / 17.40:1 (dark)** · **MUTATED `rgb(0,0,0)` on `rgb(26,26,26)` = 1.21:1 (light)**, **`rgb(255,255,255)` on `rgb(255,255,255)` = 1.00:1 (dark)** | ✅ **DRIVEN + MUTATED** |
| 3 | Calendar's ARIA grid roles are NATIVE — not written, and not merely assumed | CDP `Accessibility.getFullAXTree` over `Calendar.reference.html` → **grid 4 · row 20 · columnheader 21 · gridcell 119 · rowgroup 5 · caption 4**, with `grep -c 'role="gridcell"\|role="rowgroup"' knowledge/snippets/Calendar.reference.html` → **0** | ✅ **DRIVEN** |
| 4 | Out-of-month days are READABLE recessive ink, not the disabled ghost | in-page composited contrast of `.cal-day.is-outside`: **rgb(118,118,118) on rgb(255,255,255) = 4.54:1** light · **rgb(163,163,163) on rgb(26,26,26) = 6.90:1** dark. Both clear 4.5:1 | ✅ **DRIVEN** |
| 5 | The disabled-day ink is Date-picker's, in lock-step, and it is thin — DECLARED, not smoothed | same probe on `button.cal-day:disabled`: **rgb(225,225,225) on rgb(255,255,255) = 1.31:1** light · **rgb(128,128,128) on rgb(26,26,26) = 4.41:1** dark. Exempt from 1.4.3 (disabled), but the light/dark asymmetry is real — **Q7** | ✅ **DRIVEN + OPEN** |
| 6 | Calendar's keyboard model works, driven not asserted | headless: focus the roving stop → `ArrowRight` **20 Aug → 21 Aug** · `ArrowDown` **→ 28 Aug** · `Home` **→ 24 Aug** · `End` **→ 30 Aug** · `PageDown` title **August 2026 → September 2026** · `Shift+PageDown` **→ September 2027** · `Enter` → live region reads *"Selected: 30 September 2027."* · `aria-selected="true"` count **1** · tab stops in the grid **1 before and 1 after** | ✅ **DRIVEN** |
| 7 | Width is the container's | `.cal` declares no width/max-width (`grep -nE '\.cal\{' -A3 knowledge/snippets/Calendar.reference.html`); measured day cell **42.0 × 40** at the 360px seat and **31.7 × 40** at the 288px seat, from the same markup | ✅ **DRIVEN** |
| 8 | ⛔ **Tree row labels were clipping descenders, and the repair is a SELECTOR** | in-page on `#live-tree .tr-label`: **BEFORE clientHeight 12 / scrollHeight 18, computed `text-box-edge: cap alphabetic`** (the authored `text-box-edge:text text` LOST) → **AFTER `.tr-row > .tr-label` (0,2,0): clientHeight 21 == scrollHeight 21, computed edge `text`**, `text-overflow` still `ellipsis`, row height unchanged **44px** | ✅ **DRIVEN** |
| 9 | ⛔ **Sidebar-nav carries the same clip today, and the gate is green over it** | same probe on `Sidebar-nav.reference.html` `.sn-label`: **clientHeight 12 / scrollHeight 18, edge `cap alphabetic`** — and `python3 knowledge/_validate_descender_clip.py` → *"DESCENDER-CLIP GATE PASS — every truncating label is descender-safe (124 file(s))"* | ⛔ **CONDUCTOR'S — a live defect AND a gate finding** |
| 10 | ⛔ **The loading/empty indent selectors matched nothing** | BEFORE: every `.tr-empty` / `.tr-loading` measured `padding-left: 0px` (four rows). AFTER changing `[data-level="2"] > .tr-empty` to `.tr-empty[data-level="2"]`: **56px on all four**. `data-level` sits ON the row, so a child combinator can never match | ✅ **DRIVEN** |
| 11 | ⛔ **The view-only node was unreadable, and the repair is a CATEGORY correction** | BEFORE (`--alpha-40`): **rgb(163,163,163) on rgb(255,255,255) = 2.52:1** light, **rgb(121,121,121) on rgb(31,31,31) = 3.79:1** dark. AFTER (full ink, no hover, the words "View only" in a `.tr-meta`): **17.40:1** light / **16.48:1** dark | ✅ **DRIVEN** |
| 12 | The indent ladder is exactly what it claims, on the 4px grid | measured `padding-left` per level: **8 · 32 · 56 · 80 · 104px**; measured label left edges **517 · 541 · 565 · 589 · 613** — five steps of **exactly 24px**; `aria-level` **1 · 2 · 3 · 4 · 5**; row height **44px** at every level | ✅ **DRIVEN** |
| 13 | ONE tab stop for the whole tree | `document.querySelectorAll('#live-tree [role=treeitem][tabindex="0"]').length` → **1**, against **8** treeitems; still **1** after a full keyboard walk and a selection | ✅ **DRIVEN** |
| 14 | The tree keyboard model works, driven | `ArrowDown` → *Northwind UK Ltd* · `ArrowRight` sets `aria-expanded="true"` · second `ArrowRight` → *Current account · 40-12-09 87654321* · `ArrowLeft` → back to the parent · second `ArrowLeft` sets `aria-expanded="false"` · `End` → *Unassigned accounts* · `Home` → *Northwind Holdings* · typing **k** → *Kestrel Associates* · `Enter` → `aria-selected` count **1**, live region *"Selected: Kestrel Associates."* | ✅ **DRIVEN** |
| 15 | Lazy loading is REAL, not drawn | click the Treasury twisty → during: `aria-busy="true"`, **2** bones, **0** treeitems; after 1.2s: `aria-busy` **absent**, **0** bones, **3** treeitems with labels `['Notice deposit · 40-12-09 90001122', 'FX settlement · 40-12-09 90001123', 'Money market · 40-12-09 90001124']` | ✅ **DRIVEN** |
| 16 | The twisty clears 2.5.8 without being a second control | measured `.tr-twisty` **24 × 24** inside a row measured **44px** tall ⇒ pointer area **24 × 44**; `grep -c '<button' knowledge/snippets/Tree.reference.html` → **0** (there is no button anywhere in the component) | ✅ **DRIVEN** |
| 17 | The tree's mono selection bar reads, both themes | measured `box-shadow` on the selected row: **`rgb(0,0,0) 3px 0 0 0 inset`** on `rgb(240,240,240)` = **18.43:1** light · **`rgb(255,255,255)`** on its surface = **15.72:1** dark | ✅ **DRIVEN** |
| 18 | Every icon is byte-matched from the library, none drawn | `for f in chevron-left chevron-right chevron-double-left chevron-double-right; do diff <(grep -o 'd="[^"]*"' knowledge/assets/icons/arrows-and-chevrons/$f.svg) <(grep -o 'd="[^"]*"' knowledge/snippets/Calendar.reference.html \| sort -u \| grep -F -f <(grep -o 'd="[^"]*"' knowledge/assets/icons/arrows-and-chevrons/$f.svg)); done` → no diff for all four; same for `media/document.svg` in Tree. Corroborated by `python3 knowledge/_validate_icons.py` → **neither Calendar nor Tree appears in the UNKNOWN list** (the 16 UNKNOWN are Carousel ×11 and Image-block ×4 plus one other, all Lane C) | ✅ |
| 19 | ⚠ **NO folder / hierarchy glyph exists** — an absence, named | `ls knowledge/assets/icons/*/ \| grep -iE "folder\|hierarch\|org\|structure\|node\|group"` → **`structured-notes.svg`, `structured-notes-active.svg`** only, which mean a financial product, not a container | ✅ **and it is a GAP** |
| 20 | The leading-trim block is the CURRENT one, byte-identical to `Command-palette.reference.html` line 36 | `python3 -c "cp=open('knowledge/snippets/Command-palette.reference.html').read().split(chr(10))[35]; print(all(cp in open(f).read() for f in ['knowledge/snippets/Calendar.reference.html','knowledge/snippets/Tree.reference.html']))"` → **True** | ✅ |
| 21 | Type-composite debt: **this lane adds ZERO**, and the +2 is attributed not assumed | `python3 knowledge/_validate_type_composites.py knowledge/snippets/{Calendar,Tree}.reference.html` → **"TYPE GATE PASS … (2 file(s))"**. Tree-wide moved 1097 → **1099**; per-file sweep of all seven wave-4 members shows **Carousel ×1 and Image-block ×1 (Lane C)**; Calendar, Tree, Cascader, Splitter and Qr-code all PASS | ✅ **and the +2 is Lane C's** |
| 22 | ⛔ **Hit-area is ADVISORY and Calendar inherits Date-picker's 40px day cell** | `python3 knowledge/_validate_hit_area.py knowledge/snippets/Calendar.reference.html` → **"ADVISORY: 168 target(s) measured, 148 finding(s), 44 exempt"** (day cells 31.7–42 × 40, UNDER by 2–12.3px). **CONTROL, same gate, same day:** `Date-picker.reference.html` → **"ADVISORY: 82 target(s) measured, 74 finding(s), 104 exempt"**. Same class, inherited in lock-step, not introduced — **Q8** | ✅ **DRIVEN + OPEN** |
| 23 | ⚠ **The hit-area gate measured only 2 targets in Tree, and that is the vocabulary gap again** | `python3 knowledge/_validate_hit_area.py knowledge/snippets/Tree.reference.html` → **"ADVISORY: 2 target(s) measured, 0 finding(s), 0 exempt"** — it cannot see 8 treeitems because `treeitem` is not in its control set. **A green here means NOTHING**; the 44px rows are measured by claim 16 instead | ⛔ **DECLARED — a green that cannot fail** |
| 24 | Zero horizontal overflow, both files | `document.documentElement.scrollWidth - clientWidth` → **0** for both at 1180px; and the 280px ladder panel measured `clientWidth 278 == scrollWidth 278` with the deepest label ellipsing (clientWidth 122 < scrollWidth 140) **inside** the panel (label right 735 < panel right 752) | ✅ **DRIVEN** |
| 25 | ⚠ **A FALSE READ OF MY OWN, corrected by measuring** | I read the 280px ladder specimen off a screenshot as "overflowing its panel". Claim 24's numbers say it does not — the crop was 620px wide and cut the panel, and the label was ellipsing exactly as designed. **Recorded because the eye was wrong and the instrument was right, which is the rarer direction** | ⚠ **withdrawn** |
| 26 | ⚠ **The skeleton bone loses contrast on a TERTIARY surface** — measured, not repaired | bone vs its own surface: **Tree light 1.14:1 / dark 1.05:1**; **CONTROL `Skeleton-loader.reference.html`: light 1.14:1 / dark 1.11:1**. The bone token assumes `background/default` (#1A1A1A); on `tertiary/background/default` (#1F1F1F) it loses a further ~5% of an already-thin separation. No SC applies to a decorative bone — **Q12** | ✅ **DRIVEN + OPEN** |

---

## 4 · GATE OUTPUTS — VERBATIM

```
--- python3 knowledge/_validate_grid.py
GRID GATE PASS — all layout dimensions on the 4px grid (124 file(s)).
--- python3 knowledge/_validate_snippets.py
snippet gate: 108 snippet(s), 0 failure(s)
--- python3 knowledge/_validate_a11y.py
a11y gate: 108 snippet(s), 1 failure(s), 221 warning(s), 252 note(s) · 673 controls + 203 marks measured · 107 mark(s) below 24
  FAIL Tree: CTRL vocabulary: unknown ARIA role(s) ['tree', 'treeitem'] — this gate cannot classify them as interactive or structural, so it cannot tell whether the elements carrying them are in scope for 2.5.8. Add each to INTERACTIVE_ROLES or NON_INTERACTIVE_ROLES in _a11y_target.py before shipping (dv-vocab shape: fail loud, never let an unknown default to skip).
--- python3 knowledge/_validate_descender_clip.py
DESCENDER-CLIP GATE PASS — every truncating label is descender-safe (124 file(s)).
--- python3 knowledge/_validate_type_composites.py            (whole tree)
TYPE GATE FAIL — 1099 violation(s) across 92/123 file(s).  TYPE-001 ×31 · TYPE-002 ×1052 · TYPE-003 ×16
--- python3 knowledge/_validate_type_composites.py knowledge/snippets/Calendar.reference.html knowledge/snippets/Tree.reference.html
TYPE GATE PASS — all component text bound to canon composites (2 file(s)).
--- python3 knowledge/_probe_registry/probe_meta_schema.py --check
P-1 meta-schema sweep: 109 meta(s) checked · 0 finding(s) · 1 exempt failure(s) (EXAMPLE-button.meta.json)
PROBE P-1 — findings=0
--- python3 knowledge/_probe_registry/probe_dup_ids.py --check
P-2 duplicate-ID/IDREF scan: 50 file(s) over ['reviews/REVIEW-*.html'] · 0 finding(s) · 56 WARN-tier fragment miss(es)
PROBE P-2 — findings=0
--- python3 knowledge/_validate_binds_resolve.py
binds-resolve gate: 108 snippets (108 with manifests, 1417 vars) · 108 metas (116 binds addresses) · 101/108 canon blocks · 7 failure(s)
  ⛔ Calendar.reference.html: no .cn-calendar block in canon.css — project_canon projection is silently OFF for this snippet (renamed component file, or block never authored)
  ⛔ Tree.reference.html: no .cn-tree block in canon.css — project_canon projection is silently OFF for this snippet (renamed component file, or block never authored)
--- python3 knowledge/_validate_icons.py
16 UNKNOWN, 77 bespoke, across 108 snippet(s); 746 library glyphs.
--- python3 knowledge/_validate_hit_area.py knowledge/snippets/Calendar.reference.html
ADVISORY: 168 target(s) measured, 148 finding(s), 44 exempt.
--- python3 knowledge/_validate_hit_area.py knowledge/snippets/Tree.reference.html
ADVISORY: 2 target(s) measured, 0 finding(s), 0 exempt.
--- python3 knowledge/_validate_hit_area.py knowledge/snippets/Date-picker.reference.html      (CONTROL)
ADVISORY: 82 target(s) measured, 74 finding(s), 104 exempt.
```

**Read the numbers, not a mood.** The **binds-resolve check-D failures are EXPECTED** for
unregistered snippets — 0 var failures, 7 canon-block failures of which **2 are this lane's**
(the other 5 are Lanes B and C). The **a11y failure is the ONE declared refusal** in §6. The
tree-wide type figure moved **+2, and both are Lane C's** (claim 21).

⚠ **RUNNING THE GATES REWRITES TRACKED FILES, AND THAT IS DECLARED — AND MEASURED, NOT GUESSED.**
`git status --short -- knowledge/ notes/` at the end of this lane shows exactly four modified
tracked paths and nothing else:

```
 M knowledge/_A11Y-GATE.md
 M knowledge/_ICON-SOURCE-AUDIT.md
 M knowledge/_SNIPPET-AUDIT.md
 M knowledge/_state.json
```

The first three are **gate-authored outputs** (`_validate_a11y.py`, `_validate_icons.py`,
`_validate_snippets.py` write them as a side effect); the fourth is **this receipt's doc-row**
(§10). **No lane edited any of them by hand**, and Lanes B and C ran the same gates, so
attribution for the first three is the WAVE'S, not any one lane's — same class Lane A declared at
#209. Everything else in the tree is `??` untracked: the seven wave-4 snippets, their metas, the
brief and the lane receipts. **The conductor must reconcile these paths deliberately — never
`git add -A`.**

---

## 5 · WHAT WAS DRIVEN, AND WHAT LOOKING FOUND THAT MEASURING DID NOT

Headless Chromium, each file loaded from disk, `data-theme` toggled live, **full-page
screenshots taken in BOTH modes for both members and LOOKED AT**, plus scripted measurement of
computed styles, composited contrast, hit boxes, the CDP accessibility tree, keyboard walks and
a real asynchronous load. Screenshots re-taken and re-read after every repair.

**Defects 2, 3 and 4 in §0 were found BY LOOKING at a screenshot, not by any measurement**, and
every gate was green over all three:

1. **The descender clip** announced itself as *"Northwind Holdinas"* and *"Treasurv services"* in
   the render. Only then was it measured (claim 8) — and only then did the **Sidebar-nav control**
   get run, which is how a live defect in a gated, promoted component surfaced (claim 9).
2. **The un-indented bones** were visible as skeleton rows flush against the panel edge at the
   wrong depth. Measuring confirmed `padding-left: 0px` on all four rows (claim 10).
3. **The view-only ghost** is the **#209 cancelled-mandate class recurring inside one session**,
   and the repair is the same shape it was then: ⛔ **a view-only node is not disabled content, it
   is content you may READ but not ACT on.** Dimming it to 2.52:1 removes the only thing it is
   for. It now keeps full ink, loses its hover affordance, and says **"View only" in TEXT** — a
   second, non-colour channel, exactly as the cancelled mandate got a "Cancelled" chip.

And one correction in the other direction: **claim 25** — I read an overflow off a screenshot that
the measurement then refuted. Recorded rather than quietly dropped.

---

## 6 · THE ONE REFUSAL: `_a11y_target.py`'s ROLE VOCABULARY

**`Tree.reference.html` fails `_validate_a11y.py` and it is DECLARED, not hidden.** The gate says,
verbatim: *"unknown ARIA role(s) ['tree', 'treeitem'] … Add each to INTERACTIVE_ROLES or
NON_INTERACTIVE_ROLES in `_a11y_target.py` before shipping."*

**Probed, not assumed:** `grep -c "gridcell" knowledge/_a11y_target.py` → **0**;
`grep -c "rowgroup"` → **0**; `tree` and `treeitem` likewise appear in neither set
(`_a11y_target.py:70` INTERACTIVE_ROLES, `:74` NON_INTERACTIVE_ROLES).

**Why the two members were handled differently, and why that is a principle and not a dodge:**

- **Calendar CAN drop its explicit roles**, because `<table role="grid">` makes HTML-AAM map
  `<td>`→`gridcell` and `<thead>`/`<tbody>`→`rowgroup` natively. Removing them is the *first rule
  of ARIA*, not a workaround — and the computed tree was then **read out of Chromium** to prove
  the semantics survived (claim 3). Calendar is green.
- **Tree CANNOT.** No native HTML element maps to `treeitem`. A tree without `role="tree"` is not
  a tree. The roles must stay, so the gate must fail.

**Extending a shared gate's vocabulary is a RULING, and the fence for this lane is NEW FILES
ONLY.** So the classification is handed over rather than taken. **The recommendation, with its
reasoning, for the conductor or Dave:**

| role | proposed set | reasoning |
|---|---|---|
| `treeitem` | **INTERACTIVE_ROLES** | it is the focusable, selectable, activatable element — the same shape as `option`, which is already in that set |
| `tree` | **NON_INTERACTIVE_ROLES** | a container, the same shape as `listbox`, already in that set |
| `gridcell` | **NON_INTERACTIVE_ROLES** | a structural cell, exactly like `cell`, already in that set |
| `rowgroup` | **NON_INTERACTIVE_ROLES** | structural, exactly like `row`, already in that set |

⛔ **And a warning about what a green would mean if that classification landed:** the hit-area
gate's control set has the same gap (**claim 23** — it measured **2** targets in a file with **8**
treeitems and reported 0 findings). Classifying `treeitem` as interactive is what makes that gate
able to fail on a tree at all. **Until then a green from it on any tree is a green that cannot
fail** [[instrument-without-a-consumer]]. The 2.5.8 question is answered in this receipt by
measurement instead: rows **44px**, twisty pointer area **24 × 44** (claim 16).

---

## 7 · `$decisionsForDave` — EVERY OPEN QUESTION NAMED, NONE ANSWERED

### CALENDAR

**Q1 — ⛔ Should Date-picker's panel CONSUME this organism? *(the biggest one)***
There are now two month grids in the corpus with the same day-cell language and the same keyboard
model. The proposal on the file's face is that Date-picker's panel becomes a Calendar in a
popover. **Live outcomes, all three real:** merge them; keep both and accept the duplication; or
delete Calendar and say the month grid only ever exists inside a field. This lane did not edit
Date-picker — it is gated and promoted.

**Q2 — `<table>` or a div grid?**
Date-picker builds `<div role="grid">` with `display:contents` rows. Calendar is a real
`<table role="grid">`. The table earns its keep twice: a month has genuine two-dimensional
relations, and **a table-backed grid is static markup every gate can read, where a JS-built grid
is invisible to all of them** — which is precisely how finding 5 stayed hidden. If Dave wants one
house form, this is the moment.

**Q3 — Should out-of-month days be SELECTABLE?**
Drawn: rendered, announced, readable (4.54:1 / 6.90:1) but **not focusable and not clickable**;
arrows page the month at the edge instead. The other honest reading is that clicking 1 October
should jump to October and select it. Also open: should `showAdjacentMonths` default true at all,
or follow Date-picker and hide them?

**Q4 — Is `border/subtle` the right surface rule for a standalone calendar?**
Drawn as a bordered card. In a form step it may want no box at all.

**Q5 — Range selection.**
**NOT DRAWN, deliberately.** Date-range-picker exists; whether the standalone month should learn
ranges (and whether that is one calendar or two side by side) is unasked here.

**Q6 — Should the selected day carry a weight bump?**
It does not, and the reason is mechanical: **there is no 16px/500 tabular composite on the ramp**
(`.t-cm-figure-5` is 16/400; `.t-cm-ctl-14` is 14/500). Date-picker gets its `font-weight:500` by
a raw declaration, which is one of its 9 TYPE-002 violations. Selected therefore carries **two**
channels here (knockout + `aria-selected`) where Date-picker has three. **Either the ramp gains a
rung or the calendar stays at two — both are Dave's.**

**Q7 — The disabled day is 1.31:1 in light and 4.41:1 in dark.**
That is Date-picker's ruled treatment, in lock-step, and disabled content is exempt from 1.4.3.
But the asymmetry is stark, and in a min-date calendar it produces a **perceptual inversion worth
looking at**: the out-of-month days of the NEIGHBOURING month (4.54:1) read as more available than
the disabled days of THIS month (1.31:1). Visible in `cal-light.png`, top rows.

**Q8 — Day cells are 40px, not 44px.** 148 advisory hit-area findings, against Date-picker's 74 on
the same gate the same day (claim 22). Inherited, not introduced. A 44px cell makes a 7-column
month ~340px wide minimum. **Dave's, and it moves both components together.**

### TREE

**Q9 — Does SELECTION share a mark with CURRENT LOCATION?**
Drawn **mono**: `tertiary/background/hover` + a 3px `form/border/active` bar + `aria-selected`.
Sidebar-nav uses the same bar shape in `primary/border/default` (**#DB0011**) for
`aria-current="page"`. "The node I selected" and "the page I am on" are different meanings. The
mono choice asserts nothing — it was made so that Dave's ruling is not pre-empted.

**Q10 — Two twisty idioms now exist.** Sidebar-nav rotates `chevron-down.svg` **180°**; Tree
rotates `chevron-right.svg` **90°** (the near-universal disclosure triangle). Both are real
library glyphs. One house idiom, or two?

**Q11 — Multi-select with checkboxes.** **NOT DRAWN.** It composes Selection-controls and it
changes the aria contract (`aria-multiselectable`, `aria-checked`, tri-state parents). Left
undrawn rather than half-drawn.

**Q12 — The skeleton bone on a tertiary surface.** Measured **1.05:1** in dark against
Skeleton-loader's own **1.11:1** (claim 26). No SC applies to a decorative bone, and no token was
invented. Should the bone key off its own surface rather than off `background/default`?

**Q13 — Is `aria-disabled` the right word for "view only"?** The node is readable, announced,
and not selectable. `aria-disabled` is the closest existing vocabulary but it is not exactly what
is meant — the same vocabulary strain `s202-D3` names.

**Q14 — The indent ladder's floor is level 5.** Picked, not derived. Deeper nodes keep level 5's
indent rather than marching right. Is 5 the number, and is 24px the step?

**Q15 — Tree vs Cascader vs Sidebar-nav.** All three walk a hierarchy. **Not adjudicated** (the
sidebar-nav precedent — that adjudication is Dave's). Cascader was built in the same wave by Lane B.

**Q16 — Do the domain semantics survive?** Entity → sub-entity → account, with a child count, a
lazily loaded group and a view-only dormant entity. **Every one of those is PROPOSED.**

### CROSS-CUTTING, AND THESE ARE THE MOST VALUABLE

**Q17 — ⛔ The descender-clip gate accepts an override that loses on specificity.**
Claims 8 and 9. `_validate_descender_clip.py` reads the declaration; the cascade decides.
**Sidebar-nav is clipped today, under a green gate.** The class fix is a gate that reads the
COMPUTED edge, not the authored string — [[no-gate-parses-the-artefact]] — and a sweep of every
snippet that "overrides" the leading-trim block with a single-class selector. **Neither was done
here; both are priced TODOs.**

**Q18 — ⛔ The a11y and hit-area role vocabularies are missing four roles.** §6.

**Q19 — ⛔ Date-picker's today+selected ring is invisible.** Claim 2. Unrepaired, gated.

---

## 8 · WHAT STAYS UNPROVEN — DECLARED, NOT SMOOTHED

1. **Four-theme rendering is UNPROVEN.** `_validate_binds_resolve.py` check D fails for both
   (`.cn-calendar` / `.cn-tree` absent from `canon.css`), so theme projection is silently OFF.
   **Only the light and dark legs authored in each snippet have been seen. Console, Legacy and
   Supercharge are UNSEEN for both members.**
2. **`_validate_kg.py` NOT RUN.** Both metas name patterns
   (`payment-date`, `appointment-slot`, `statement-period`, `account-hierarchy`,
   `category-picker`, `org-structure`) the generated node registries have probably never seen.
   `gen_kg_edges.py` is a shared generated artefact — **conductor's**. Two `tree.meta.json` edges
   carry **`ref: null` with prose**, deliberately, rather than invent a node id.
3. **`_validate_state_contrast.py` NOT RUN** — a filtered run overwrites the tracked
   `_STATE-CONTRAST-AUDIT.md`, outside this lane's fence. Same declaration Lanes P (#204) and A
   (#209) made. **Owed.**
4. **`_validate_radius.py`, `_validate_partials.py`, `_validate_compose.py`,
   `_validate_no_hardcode.py` and the full `_build_all.py` were NOT run.** Named so the absence is
   visible; several depend on registration this lane deliberately did not take.
5. **ONE browser, ONE engine, TWO widths, ONE zoom.** Headless Chromium at 1180px with 280/288/360/400/520px
   containers. No second engine, no zoom pass, no real 480px viewport pass, **no touch device**.
   The 40px day cell and the 44px tree row have never been touched by a finger.
6. **No screen reader was ever run.** Every accessibility claim here is a claim about the DOM,
   the computed accessibility tree and computed styles. `aria-level`/`setsize`/`posinset`,
   `aria-busy`, the roving tabindex and the live regions are **asserted structurally and
   announced by nobody.**
7. **The lazy-load timing is a 900ms `setTimeout`,** not a network. Nothing here proves the
   loading state behaves under a slow or failed fetch — **there is no ERROR state on the tree at
   all**, and that is a gap, not an omission.
8. **The type-composite debt figure quoted (1097 → 1099) is a whole-tree number measured while
   two other lanes were writing into the same tree.** It is attributed per-file in claim 21, but
   the tree was moving under all three lanes and a re-run will differ.
9. **Nothing here has been seen by Dave**, and nothing is registered anywhere. Every one of the
   nineteen questions above is open.

---

## 9 · HANDOFF TO THE CONDUCTOR — the serial set this lane could not touch

1. `.cn-calendar` and `.cn-tree` blocks in `canon/canon.css` (clears 2 of the 7 check-D failures;
   the other 5 are Lanes B and C).
2. Re-run `gen_kg_edges.py`, then `_validate_kg.py`.
3. `component-types.json` (incl. the `$members` entry for `.cal-nav` — button-family candidates
   with empty AUTO-PARTIAL markers and `--phys-size:44` already in place) · `CATEGORIES` ·
   `gen_showroom.py` · `_validate_radius.MIGRATED_SNIPPETS` registrations, **if these are kept**.
4. **Store rows for `calendar` and `tree` as components** — the #185 forgotten-document class.
   This receipt's own doc-row is minted (§10); the component rows and the wave row are the
   conductor's.
5. ⛔ **`_a11y_target.py` role vocabulary** — four roles, classification proposed in §6. **A
   ruling, not a patch.**
6. ⛔ **`_validate_descender_clip.py` reads the declaration, not the cascade** (Q17), and
   **Sidebar-nav is clipped today under its green** (claim 9). Two separate repairs: the gate,
   and a sweep of every single-class override in the corpus.
7. ⛔ **Date-picker's today+selected ring** (claim 2, Q19). One CSS rule; a gated file.
8. An `_ICON-GAPS.md` entry for the **absent folder/hierarchy glyph** (claim 19) — that file is
   the conductor's.
9. ⚠ **Gate side-effect writes** — `_A11Y-GATE.md`, `_SNIPPET-AUDIT.md`, `_HIT-AREA.md`,
   `_graph-mark-observations.jsonl`, `_REHEARSAL-LOG.jsonl`: **wave-level, not lane-level**.
   Reconcile each path deliberately; **never `git add -A`.**
10. ⚠ **CONCURRENCY HAZARD, DECLARED.** Lanes A, B and C all wrote `knowledge/_state.json`
    doc-rows in the same window (Lane C's row is `W-71`). `_state.py` does read-modify-write with
    no lock. This lane re-read the store after writing and asserted its own row survived (§10),
    **but it cannot assert that nobody else's was lost.** The conductor should verify all three
    lane rows are present before committing.

---

## 10 · THE STORE DOC-ROW FOR THIS RECEIPT

Minted through the store's own writer (`knowledge/_state.py` `add()`, which refuses a row with no
close condition) at receipt creation, per the brief's return contract and the #185
forgotten-document class. **Exactly one row; the component rows and the wave row are the
conductor's.**

| field | value |
|---|---|
| id | **`W-72`** |
| home | `notes/_receipts/2026-08-20-210-wave4-laneA-calendar-tree.md` |
| owner / state / opened | `dave` · `open` · `210` |
| condition | `stated` (`add()` refuses a row without one) |

**Verified after writing, in a separate read:** `W-72` is present, **Lane C's `W-71` survived the
same window**, the store holds 93 items, and `_state.check()` returns `ok=True` with zero fails.
`python3 knowledge/_gate_doc_rows.py --check` → *"population 25 … unrowed 0 · ✅ PASS"*.
⚠ Lane B had not written its row at the time of that read, so **this receipt cannot say Lane B's
row survived** — only that A's and C's did.

⛔ Note on scope: `_gate_doc_rows.py`'s population is `notes/_briefs/*` and `_BRIEF-*` only, so a
receipt is **outside** what that gate can check. The row is minted because the class demands it,
not because a gate would have caught its absence — which is exactly the #185 shape.
