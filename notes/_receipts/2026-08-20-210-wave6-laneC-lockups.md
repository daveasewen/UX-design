# Receipt — #210 Wave 6 · Lane C · Lock-ups I (Sonnet)

**Lane:** C (Sonnet) · **Session:** #210 · **Date:** 2026-08-20
**Brief:** `notes/_briefs/2026-08-20-210-wave6-layer2-p3-fanout-brief-v1.md` (THE JOB, Lane C)
**Members:** itinerary row 116 (Section-heading-lockup) · row 117 (Card-header-lockup) ·
row 118 (Hero-variants) · row 119 (Stats-band-lockup)

> ⛔ **NOTHING IN THIS RECEIPT IS A RULING.** All four lock-ups are PROPOSED, not ruled. No
> registry, `MIGRATED_SNIPPETS`, `CATEGORIES`, spine, canon.css, `_rulings.json` or git operation
> was touched — the serial set is the conductor's. This lane created NEW FILES ONLY, plus this
> receipt and its store row.

---

## 0 · THE JOB, RESTATED

Layer-2 rows 116/117/118/119 carry `derived: NO-ARTEFACT-CLASS` (116/117/119) or an EXISTING
gated Hero the itinerary names for extension (118). Per the wave brief's artefact-class
convention, each ships as `knowledge/snippets/<Name>.reference.html` +
`knowledge/components/<name>.meta.json` with `"$layer": "2 Lock-up"`. **THE CARDINAL RULE:
COMPOSE, NEVER RE-DRAW.** Every visible atom in all four files traces to an existing
gated/proposed `knowledge/snippets/*.reference.html` source, borrowed verbatim and diff-proven
below.

---

## 1 · FILE LIST — eight new files, plus this receipt

| # | path | bytes |
|---|---|---|
| 1 | `knowledge/snippets/Section-heading-lockup.reference.html` | 13,817 |
| 2 | `knowledge/components/section-heading-lockup.meta.json` | 5,342 |
| 3 | `knowledge/snippets/Card-header-lockup.reference.html` | 19,459 |
| 4 | `knowledge/components/card-header-lockup.meta.json` | 5,675 |
| 5 | `knowledge/snippets/Hero-variants.reference.html` | 18,258 |
| 6 | `knowledge/components/hero-variants.meta.json` | 5,688 |
| 7 | `knowledge/snippets/Stats-band-lockup.reference.html` | 20,926 |
| 8 | `knowledge/components/stats-band-lockup.meta.json` | 5,470 |
| 9 | `notes/_receipts/2026-08-20-210-wave6-laneC-lockups.md` | this file |

**No existing file was edited.** Renders used during the build live OUTSIDE the repo
(`NON-REPO: the session outputs mount, w6c_renders/*.png` — 24 PNGs, light+dark × 3 widths × 4
files) per `s191-D2` home-or-declare; they are working artefacts, not deliverables. The probe
script that produced them (`_w6c_probe.py`) was scratch in the repo root and is not a deliverable
either — safe to delete.

---

## 2 · COMPOSITION — what was borrowed, from where

**Section-heading-lockup.reference.html** (row 116) composes, verbatim: Layout-utilities
.reference.html PROPOSED (`.l-row`/`.l-stack`, the ENTIRE responsive story — no new CSS needed
for the collapse), Eyebrow.reference.html GATED (`.eyebrow`), Cards.reference.html GATED
(`a.arrow`), Badge.reference.html GATED (`.badge.standalone`), Button.reference.html GATED
(tertiary/quaternary tiers only). Three arrangements: **A** bare label (the Template-dashboard
`<h2 class="tpl-section-head t-cm-section-label">` shape), **B** label + trailing arrow-link,
**C** eyebrow + heading + count badge + two-button action group.

**Card-header-lockup.reference.html** (row 117) composes, verbatim: Cards.reference.html GATED
(`.card` surface + action-card body padding, `.qbtn`), Icon-button.reference.html GATED
(quaternary tier, 44×44, as the overflow trigger), Status-indicator.reference.html GATED (tint
chip form B). The overflow panel reuses Dropdown.reference.html's GATED `.menu`/`.opt`/`.sep`
positioning CSS byte-for-byte, with **one declared ARIA deviation**: Dropdown's panel is a
`role="listbox"` VALUE picker; this lock-up's panel is a `role="menu"` ACTIONS panel
(`role="menuitem"` buttons, no `aria-selected`) — visual CSS unchanged, only the semantic layer
differs, stated in the file's own header. Three arrangements: **A** title+meta only, **B**
title+meta+two inline `.qbtn` actions, **C** title+meta+status chip+overflow menu.

**Hero-variants.reference.html** (row 118) composes/extends the GATED Hero baseline (`.hero`/
`h1`/`.intro`/`.cta-row`/`.cta`/`.arrow`) plus Layout-utilities' `.l-split`-style grid (own
`.hv-media`/`.hv-frame`, container-query collapse), Stat-card.reference.html GATED
(`.stat-card`/`.amt`/`.delta`), Button.reference.html GATED (primary+tertiary tiers). Four
arrangements: **A** baseline (Hero reproduced verbatim), **B** media (two-column split, text kept
OFF the image — Hero's own flagged scrim question is NOT answered here), **C** stat-led (CTA row
replaced by a 3-tile Stat-card board), **D** CTA-led (single `.cta` promoted to a primary+
tertiary Button pair).

**Stats-band-lockup.reference.html** (row 119) composes, verbatim, per the brief's own
do-not-rule instruction ("compose Cards/Stat-card/Kpi-tile — no new molecules"): Layout-utilities
`.l-grid`, Stat-card.reference.html GATED, Kpi-tile.reference.html PROPOSED #203 (full markup
including sparklines), Cards.reference.html GATED (`a.arrow`). Three arrangements: **A** heading
+ 3-tile Stat-card board (the Template-dashboard shape), **B** heading + 4-tile Kpi-tile board
with sparklines, **C** heading + trailing "View all" + 4-tile Stat-card board (auto-fill
collapse proven at a narrow width).

The ONLY new CSS in any of the four files is arrangement-only flex/grid wrapping (`.ch-*` header
row, `.hv-*` media split, `.sb-head` framing row) — zero new visual vocabulary, matching the
Meter/Page-header-lockup precedent.

**Declared deviations from byte-for-byte verbatim, all stated in the files' own banners:**
1. Card-header-lockup's overflow menu: `role="menu"`/`role="menuitem"` replaces Dropdown's
   `role="listbox"`/`role="option"` (an ACTIONS panel is not a VALUE picker) — CSS unchanged.
2. Hero-variants' h1/.intro/.arrow: Hero's own raw `font:`/`font-weight` shorthand (a bespoke
   fluid `clamp()` size with no fixed canon-ramp equivalent) is NOT reproduced verbatim — see §4.

---

## 3 · CLAIM TABLE — every claim carries a probeable token (`s182-D1`)

| # | claim | probe — re-runnable, exactly as written | verdict |
|---|---|---|---|
| 1 | Every visible atom traces to a named gated/proposed source | manual diff: every non-arrangement CSS selector (`.eyebrow`,`a.arrow`,`.badge`,`.btn`,`.card`,`.qbtn`,`.iconbtn`,`.chip`,`.menu`/`.opt`,`.hero`,`.stat-card`,`.kpi-tile`,`.spark-inline`,`.l-row`/`.l-stack`/`.l-grid`) appears verbatim in its named source file — see §2 | ✅ |
| 2 | Meta schema conformance (P-1) | `python3 knowledge/_probe_registry/probe_meta_schema.py --check` → `127 meta(s) checked · 0 finding(s) · 1 exempt failure(s) (EXAMPLE-button.meta.json)` | ✅ |
| 3 | Every `$layer` key present (not bare `layer`) | `grep -n '"\$layer"' knowledge/components/{section-heading,card-header,hero-variants,stats-band}-lockup.meta.json` (renamed forms) → 4/4 hits, `"$layer": "2 Lock-up"` | ✅ |
| 4 | Snippet/token-manifest gate clean on all four | `python3 knowledge/_validate_snippets.py` → `snippet gate: 129 snippet(s), 0 failure(s)` | ✅ |
| 5 | Leading-trim block byte-identical to Command-palette line 36 | `python3 -c "cp=open('knowledge/snippets/Command-palette.reference.html').read().split(chr(10))[35]; print(all(cp in open(f).read() for f in [...4 files...]))"` → **True** | ✅ |
| 6 | No colour invented; two-red law + mono error ink camp untouched | `grep -nE '#[0-9A-Fa-f]{6,8}' <4 files> \| grep -vE '<the ~35 already-carried hexes>'` → **0 lines** | ✅ |
| 7 | Type ratchet: 0 new violations (debt may not grow) | `python3 knowledge/_validate_type_composites.py --ratchet` → **"TYPE RATCHET PASS — declared debt holds at 1097 (0 new)."** (first draft measured 1108, +11 — see §4) | ✅ |
| 8 | a11y gate clean with all four present | `python3 knowledge/_validate_a11y.py` → *"a11y gate: 129 snippet(s), 0 failure(s), …"* | ✅ |
| 9 | 4px-grid gate clean | `python3 knowledge/_validate_grid.py` → *"GRID GATE PASS … (145 file(s))."* | ✅ |
| 10 | Descender-clip gate passes | `python3 knowledge/_validate_descender_clip.py` → *"DESCENDER-CLIP GATE PASS … (145 file(s))."* | ✅ |
| 11 | Icon-source gate: rc=0 for all four (first draft had 1 UNKNOWN) | `python3 knowledge/_validate_icons.py` → *"0 UNKNOWN, 97 bespoke, across 129 snippet(s)"* (fixed — see §4) | ✅ |
| 12 | ⛔ binds-resolve check-D FAILS for all four — DECLARED, not hidden | `python3 knowledge/_validate_binds_resolve.py` → *"119/129 canon blocks · 10 failure(s)"*, naming all 4 of this lane's files + 6 sibling-lane files from the same wave — no `.cn-*-lockup`/`.cn-hero-variants` block exists in canon.css yet | ⛔ **CONDUCTOR'S** |
| 13 | Zero horizontal overflow at 3 widths × 2 themes × 4 files, driven | headless Chromium 151 (`chromium_headless_shell`, `--no-sandbox --disable-dev-shm-usage --disable-gpu`), widths 1400/700/340, both `data-theme`s (set on `<body>`, matching every source snippet's own convention): `document.body.scrollWidth - document.body.clientWidth` → **0 in all 24 combinations** | ✅ **DRIVEN** |
| 14 | The responsive collapses actually happen, not just "no overflow" | Section-heading: at 340px the action row + eyebrow drop below the heading (`.l-row` tops measured 527px vs 601px — two rows, not one). Card-header: `.ch` `flex-direction` measured `row` at 1400px, `column` at the 230px narrow frame. Hero-variants media: `.hv-media` `grid-template-columns` measured `308px` (single track) at 340px after the fix in §4. Stats-band: `.l-grid` `grid-template-columns` measured `260px` (single track) at the narrow frame. All measured via `getComputedStyle`, not asserted from a screenshot alone | ✅ **DRIVEN** |
| 15 | Card-header-lockup's overflow menu opens/closes and is keyboard-operable | driven: trigger click → `aria-expanded="true"`, `data-open="true"`; `Escape` → `aria-expanded="false"`, focus returns to trigger | ✅ **DRIVEN** |
| 16 | Fonts render in the licensed HSBC cut, all 24 renders | `document.fonts.check('16px HSBC_MtUnivers_Latin')` → **true** in all 24 combinations | ✅ |
| 17 | Dark theme actually renders dark (caught a probe-script bug, not a snippet defect) | first probe pass toggled `document.documentElement`'s `data-theme`, but every source snippet hardcodes `<body data-theme="light">` in markup — the attribute on `<body>` itself wins over an inherited custom-property value from `<html>`, so the FIRST dark screenshots were silently still light. Fixed the PROBE (toggle `document.body`, matching the repo's own convention) and re-ran; all 4 files' dark renders confirmed correct by eye (screenshots looked at) | ✅ **DRIVEN, defect was in the harness not the component** |

---

## 4 · TWO FIXES FOUND BY RUNNING THE GATES/BROWSER, NOT BY INSPECTION

**Fix 1 — type ratchet, first draft measured 1108 (+11), FAILED.** Composing an atom into a new
file duplicates whatever raw (non-composite) font declarations that atom's own file still
carries, exactly as the wave-5 lane D receipt found. Fixed the same way:
1. `body{font-family:var(--font)}` was deleted from all four files (the Kpi-tile precedent: once
   every text element carries a `.t-cm-*`/`.t-ed-*` composite, `body` needs no font declaration
   at all).
2. `a.arrow{font-weight:500}` (Section-heading, Stats-band) and `.hero .arrow{font-weight:500}`
   (Hero-variants) were deleted; `.t-cm-button` was added to each arrow-link's `.lbl` span.
3. `.card p.desc{font:400 14px/1.43 var(--font)}` and `.ch-titles h3{font-weight:500}`
   (Card-header) were deleted — the markup already carried `.t-ed-body-small`/`.t-cm-ctl-16`
   redundantly; the raw CSS was simply dead weight duplicating what the composite already does.
4. Hero-variants' h1/.intro/.arrow carry Hero's OWN bespoke fluid `clamp()` size with no fixed
   canon-ramp equivalent — reproducing it verbatim would be a genuinely NEW occurrence (Hero's own
   copy already counts once inside the 1097 baseline). Fixed with the wave-5 technique: the raw
   declaration was deleted and the CLOSEST fixed composite was added to the markup instead
   (`.t-ed-display-2` 40/48/300 for h1, `.t-ed-heading-4` 20/28/300 for `.intro`, `.t-cm-button`
   16/500 for the arrow-link label). **DECLARED VISUAL DEVIATION**: the headline no longer scales
   fluidly between Hero's 32-52px range — Dave's call on whether Hero itself should eventually
   gain a ramp-legal fluid composite (§6 Q4).

After the fix: **0 new violations, ratchet PASS, debt holds at 1097.**

**Fix 2 — icon-source gate, first draft had 1 UNKNOWN.** Card-header-lockup's overflow trigger
glyph was hand-drawn (a three-dot kebab) rather than byte-matched. Found a real library glyph at
`knowledge/assets/icons/global-controls/menu-more-horizontal.svg` and byte-matched it in; icon
gate now `0 UNKNOWN, 97 bespoke, across 129 snippet(s)`.

**Fix 3 (not a gate — caught by DRIVING the browser, WAVE-5 LESSON 3 exactly as warned) —
Hero-variants' media split silently never collapsed.** `container-type:inline-size` was declared
on `.hv-media` itself, and the `@container` rule targeting `.hv-media`'s own
`grid-template-columns` queried `.hv-media`'s nearest ANCESTOR container — which does not exist —
so the rule never fired (only the DESCENDANT rule, `.hv-media .img{order:-1}`, correctly queried
against the container `.hv-media` establishes and DID fire). This produced a visually plausible
but WRONG render: the image reordered to the left, but the grid stayed two-column, causing a
6-14px scroll overflow at 340px that a screenshot alone would not explain. Measured directly
(`getComputedStyle(.hv-media).gridTemplateColumns` returned `"142px 142px"` — two tracks — even
though `order:-1` had visibly applied). **Fix**: moved `container-type:inline-size` onto a new
wrapper `.hv-frame`, so `.hv-media` (now a proper descendant of the container) can legally be
queried. Re-measured: `gridTemplateColumns` → `"308px"` (one track) at 340px, overflow → 0. This
is the exact trap WAVE-5 LESSON 3 names, caught here by measuring computed style rather than
trusting a screenshot or an assertion.

---

## 5 · WHAT WAS DRIVEN — a real browser, light AND dark, 3 widths, all four files

Headless Chromium 151 (`chromium_headless_shell`, `--no-sandbox --disable-dev-shm-usage
--disable-gpu`; system libs from `~/.local/chromelibs` + `/var/tmp/chromelibs`, no root; fonts
installed from `knowledge/assets/fonts/_desktop/TTF` with the two-string fontconfig alias per
`_RUNBOOK-render-verify.md` §5). Widths **1400 / 700 / 340**, both `data-theme`s (toggled on
`<body>`), all four files — **24 full-page screenshots taken and looked at** (home: `NON-REPO:
session outputs mount, w6c_renders/*.png`). Zero horizontal overflow measured in all 24
combinations (§3 claim 13). Collapses measured via `getComputedStyle`, not just screenshotted
(§3 claim 14). Card-header-lockup's overflow menu driven open/closed with keyboard (§3 claim 15).
Dark-theme renders visually confirmed correct AFTER fixing the harness bug in §3 claim 17 — the
component files themselves never had the defect, the first probe script did.

---

## 6 · EVERY OPEN DESIGN QUESTION — NAMED, NOT SETTLED

**All of these are Dave's.**

### Q1 — Should each lock-up's arrangements be one flexible organism (an `arrangement` prop) or split into named files?
All four are drawn as ONE organism each with 3-4 arrangement variants side by side, on the
Page-header-lockup precedent. If Dave wants any split, the split is mechanical — each arrangement
block is already self-contained in its own `<section>`/`<div>`.

### Q2 — Section-heading-lockup: is a bare `<h2>` always the right level, or does this lock-up need an explicit `level` prop?
Drawn as `<h2>` throughout; a section nested under another section (e.g. inside a `.tpl-split`
panel) may need `<h3>` for correct heading order — undrawn, left to the consuming page.

### Q3 — Card-header-lockup: does the overflow-menu ARIA deviation (role="menu" vs Dropdown's role="listbox") need its own named pattern, or should Dropdown itself grow a "menu mode"?
Drawn as a declared one-off deviation (§2). If overflow-menus recur elsewhere in the system
(they likely will — every card, every table row), a shared "Action-menu" atom might be the
better long-term home rather than each consumer re-declaring the deviation. Not built here.

### Q4 — Hero-variants: should Hero itself gain a ramp-legal FLUID composite (a `clamp()`-based `.t-ed-display` tier), rather than this lock-up substituting a fixed size?
The fix in §4 (Fix 1, item 4) trades Hero's fluid scaling for a fixed composite size to satisfy
the type ratchet. That is a real, if small, visual change from Hero's own baseline. If fluid
headline scaling matters, the right fix is a new canon composite, which is Dave's / the design
system owner's call, not this lock-up's.

### Q5 — Hero-variants B (media): is "no text over the image" the right permanent answer, or is the scrim treatment Hero's header flags actually wanted?
Deliberately NOT answered here (§2) — this variant sidesteps Hero's own flagged question rather
than resolving it. If a scrim IS wanted, someone still owes a guaranteed-contrast treatment that
is not derivable from tokens (Hero's own words).

### Q6 — Stats-band-lockup: does arrangement B (Kpi-tile board) ship the inherited two-seat colour question, or does this lock-up need to wait for that to resolve first?
Carried unchanged from Kpi-tile.reference.html's own header (§2) — the fill-seat/ink-seat
divergence is visible in this lock-up's own renders (confirmed in the dark-1400 screenshot: the
"Approvals waiting" flat tile's spark renders white ink, matching `s182-D3`'s dark rule). Not
resolved here; Stat-card and Kpi-tile "must move together" per Kpi-tile's own instruction.

### Q7 — Should Hero-variants D's two-button pair ever also carry the arrow-link (a THIRD action)?
Deliberately not drawn (§2, the file's own demo-note) — undrawn territory.

---

## 7 · WHAT STAYS UNPROVEN

1. **The canon-block projection.** `_validate_binds_resolve.py` check D FAILS for all four
   (`.cn-section-heading-lockup`, `.cn-card-header-lockup`, `.cn-hero-variants`,
   `.cn-stats-band-lockup` do not exist in `canon.css`) — 10 failures total in that gate run,
   shared with 6 sibling-lane files from the same wave. Until the conductor projects those
   blocks, **Console, Legacy and Supercharge are UNPROVEN for all four** — only the light/dark
   legs authored in each snippet have been seen.
2. **`_validate_kg.py`** freshness FAILS for the four new metas + the two `_nodes-*.json`
   aggregate files (expected — `gen_kg_edges.py` was NOT run per the brief's "Do NOT run --update
   yourselves" instruction; this is the conductor's re-seed, same residual class as wave-5 lane D).
3. **Only 3 widths were driven** (1400/700/340), and only ONE browser engine (headless
   Chromium 151), matching the wave-5 precedent's own declared limit.
4. **Hit-area gate (`_validate_hit_area.py --all`)** was not independently re-run this lane;
   Card-header-lockup's overflow trigger (44×44, Icon-button's own hit area, unmodified) and the
   status chip (passive, no hit area) were not separately measured beyond the browser drive in §5.
5. **Nothing here has been seen by Dave**, and nothing is registered anywhere (no
   `MIGRATED_SNIPPETS`, `CATEGORIES`, `component-types.json`, `gen_showroom.py`,
   `gen_kg_edges.py` entry, `canon.css` block, or `_rulings.json` row).
6. **The type-ratchet fix's visual deviations** (Hero-variants' fixed-size headline in place of
   the fluid clamp) have not been shown to Dave as a before/after comparison — only described
   here in prose (§4, §6 Q4).

---

## 8 · BLAST RADIUS — selectors this lane extended (WAVE-5 LESSON 6)

None of the four files extends a GLOBAL selector's reach (`.badge`, `.seg`, `.chip`, etc. are all
scoped inside each file's own `<style>` block, matching every other snippet's self-contained
convention — no shared stylesheet edited). The gate escape named in §3 claim 12
(binds-resolve check D) is the only cross-file consequence, and it is the conductor's re-seed,
not a blast-radius extension.

---

## 9 · HANDOFF TO THE CONDUCTOR

1. `.cn-section-heading-lockup`, `.cn-card-header-lockup`, `.cn-hero-variants`,
   `.cn-stats-band-lockup` blocks in `canon/canon.css` (clears 4 of the wave's 10 check-D
   failures).
2. Re-run `gen_kg_edges.py` if these four are kept (residual §7.2).
3. `component-types.json` · `CATEGORIES` · `gen_showroom.py` · `_validate_radius.MIGRATED_SNIPPETS`
   registrations, if kept.
4. **Q4 (Hero-variants type fix)**: does the type-ratchet fix's fixed-size headline stand, or
   does Hero need a fluid canon composite first? Affects whether Hero-variants A should also be
   re-typed to match, or whether the fix should be reverted once a fluid composite exists.
5. **Q3 (Card-header-lockup's ARIA deviation)**: worth a shared Action-menu atom, or does the
   declared one-off deviation stand?
6. This receipt's own store row (added at creation per the #185 forgotten-document class — see
   the wrap chain).
7. Delete `_w6c_probe.py` from the repo root (scratch, not a deliverable) if it survived to
   commit time.
