# Receipt — #210 Wave 6 · Lane D · P3 Lock-ups II (Sonnet)

**Lane:** D (Sonnet) · **Session:** #210 · **Date:** 2026-08-20
**Brief:** `notes/_briefs/2026-08-20-210-wave6-layer2-p3-fanout-brief-v1.md` (THE JOB, Lane D)
**Members:** itinerary row 121 (Footer-doormat-lockup) · row 122 (CTA-lockup) · row 123 (Feature-grid-lockup)

> ⛔ **NOTHING IN THIS RECEIPT IS A RULING.** All three lock-ups are PROPOSED, not ruled. No
> registry, `MIGRATED_SNIPPETS`, `CATEGORIES`, spine, canon.css, `_rulings.json` or git operation
> was touched — the serial set is the conductor's. This lane created NEW FILES ONLY, plus this
> receipt and its store row.

---

## 0 · THE JOB, RESTATED

Wave-6 itinerary rows 121/122/123 carry `derived: NO-ARTEFACT-CLASS` — no shell/template/lock-up
artefact class exists in the store for any of them. Per the wave convention (carried from wave 5),
each ships as `knowledge/snippets/<Name>.reference.html` + `knowledge/components/<name>.meta.json`
with `"$layer": "2 Lock-up"`. **THE CARDINAL RULE: COMPOSE, NEVER RE-DRAW.** Every visible atom in
all three files traces to an existing gated/proposed `knowledge/snippets/*.reference.html` source
or a canon type composite, borrowed verbatim and diff-proven below.

Row 121 (Footer-doormat-lockup) is a special case: the itinerary describes it as "Footer composed
into the full mega-footer arrangement" — Footer.reference.html already implements a doormat form
100%, so this lock-up composes THE WHOLE of it verbatim (not a partial atom), wrapped in a page
context stub so the doormat is seen as end-of-document matter rather than an isolated demo. See §2.

---

## 1 · FILE LIST — six new files, plus this receipt

| # | path | bytes |
|---|---|---|
| 1 | `knowledge/snippets/Footer-doormat-lockup.reference.html` | 13,487 |
| 2 | `knowledge/components/footer-doormat-lockup.meta.json` | 4,865 |
| 3 | `knowledge/snippets/CTA-lockup.reference.html` | 12,753 |
| 4 | `knowledge/components/cta-lockup.meta.json` | 5,294 |
| 5 | `knowledge/snippets/Feature-grid-lockup.reference.html` | 17,062 |
| 6 | `knowledge/components/feature-grid-lockup.meta.json` | 5,444 |
| 7 | `notes/_receipts/2026-08-20-210-wave6-laneD-lockups.md` | this file |

**No existing file was edited.** Renders live OUTSIDE the repo (`NON-REPO: the session outputs
folder, w6d_renders/*.png` — 18 PNGs, light+dark × 3 widths × 3 files) per `s191-D2` home-or-declare;
working artefacts, not deliverables.

---

## 2 · COMPOSITION — what was borrowed, from where, and what was arrangement-only

**Footer-doormat-lockup.reference.html** (row 121) composes, verbatim, **100% of the visible
surface**: `Footer.reference.html`'s doormat form — `.ft`/`.ft-inner`/`.ft-brand`/`.ft-mat`/
`.ft-group`/`.ft-legal`, `a.lnk`, `a.arrow`, the back-to-top glyph — class-for-class identical to
the source, because this lock-up IS that arrangement, not a partial reuse. Footer's `slim` form is
out of scope (the brief names "the full mega-footer arrangement" specifically). The only NEW class
is `.fdl-*`, a page-context wrapper (`.fdl-page`/`.fdl-content`) that puts a content stub above the
footer — demo chrome, deletable without changing the component. **Footer's placeholder `href="#"`s
are carried unchanged, per the brief's DO-NOT-RULE — not repaired.**

**CTA-lockup.reference.html** (row 122) composes, verbatim: `Button.reference.html`'s `.btn` +
`.primary`/`.secondary` tiers + press-physics partial (the action pair). Heading/support text ride
canon composites (`t-ed-heading-3`, `t-ed-body`) in markup — never a raw declaration. Two
arrangement variants: **A** centred (full-bleed marketing band) · **B** split (title left, actions
right, for a narrower in-page band). Copy is plain and informational per the brief's mono
discipline / no-invented-urgency-copy instruction: "Open an account online" / "See how Apollo can
work for your business" — no countdown, no exclamation mark, no manufactured scarcity.

**Feature-grid-lockup.reference.html** (row 123) composes, verbatim: `Cards.reference.html`'s
`.card` base + the Action-card icon/title/body geometry, **with the `.actions` button row
deliberately omitted** (a feature-grid cell states a benefit, it does not carry its own per-cell
CTA — that is CTA-lockup's job). Title/body ride `t-cm-button` (16/500, exact match to Cards' own
raw `h3` declaration) and `t-ed-body-small` (14/400, exact match to Cards' own raw `p`
declaration). Four icons, byte-matched (see §3 claim 5): `security-secure`
(global-controls), `device-mobile` (media), `data-chart` (products-and-services), `world-trader`
(products-and-services). Three arrangement variants: **A** 2-up · **B** 3-up · **C** 4-up.

The ONLY new CSS in any of the three files is the `.fdl-*`/`.ctal-*`/`.fgl-*` arrangement layer
(flex/grid containers, container queries) — the Meter organism precedent (ruled #210): an
organism's own rules are arrangement only, zero new visual vocabulary. **s210-D3 discipline is
carried through**: none of `.fdl-*`/`.ctal-*`/`.fgl-*` declares a width; `.demo-*` classes are demo
chrome only, deletable without changing the component.

---

## 3 · CLAIM TABLE — every claim carries a probeable token (`s182-D1`)

| # | claim | probe — re-runnable, exactly as written | verdict |
|---|---|---|---|
| 1 | All visible atoms are gated/proposed sources or canon composites, not re-drawn | manual diff: every non-`.fdl-*`/`.ctal-*`/`.fgl-*`/`.demo-*` CSS selector name (`.ft`,`a.lnk`,`.btn`,`.card`) appears verbatim in its named source file — see §2 | ✅ |
| 2 | Footer-doormat-lockup's placeholder hrefs are carried, not repaired | `grep -c 'href="#"' knowledge/snippets/Footer-doormat-lockup.reference.html` → **12** (identical count/positions to Footer.reference.html's own doormat form) | ✅ |
| 3 | The leading-trim block is the CURRENT one, byte-identical to Command-palette line 36 | `python3 -c "cp=open('knowledge/snippets/Command-palette.reference.html').read().split(chr(10))[35]; print(all(cp in open(f).read() for f in ['knowledge/snippets/CTA-lockup.reference.html','knowledge/snippets/Feature-grid-lockup.reference.html','knowledge/snippets/Footer-doormat-lockup.reference.html']))"` → **True** | ✅ |
| 4 | No colour invented; two-red law + mono error ink camp untouched | `grep -nE '#[0-9A-Fa-f]{6}' knowledge/snippets/{CTA-lockup,Feature-grid-lockup,Footer-doormat-lockup}.reference.html \| grep -vE '#F0F0F0\|#FFFFFF\|#1A1A1A\|#1F1F1F\|#808080\|#E1E1E1\|#305A85\|#4587A7\|#636363\|#000000\|#484848\|#313131\|#9D9D9D\|#626262\|#9D9D9D\|#B2B2B2\|#333333\|#B7B7B7'` → **0 lines** (every hex is a value already carried by the borrowed atom's own manifest) | ✅ |
| 5 | Feature-grid-lockup's 4 icons are byte-matched from the library, not invented (lesson 4) | `python3 knowledge/_validate_icons.py` → `_ICON-SOURCE-AUDIT.md` row 53: **"Feature-grid-lockup \| 4 \| 4 \| 0 \| 0 \| yes \| ✅ verified"** (4 library, 0 bespoke, 0 unknown); Footer-doormat-lockup row 56: **"1 \| 1 \| 0 \| 0 \| yes \| ✅ verified"**; CTA-lockup row 19: **"0 \| 0 \| 0 \| 0 \| — \| no inline svg paths"** | ✅ |
| 6 | Type-composite ratchet: 0 new violations from these 3 files (DO-NOT-RULE) | `python3 knowledge/_validate_type_composites.py 2>&1 \| grep -E "CTA-lockup\|Feature-grid-lockup\|Footer-doormat-lockup"` → **0 lines**. Repo-wide: `--ratchet` reports **FAIL, 5 new**, but every one of the 5 is attributed to `Card-header-lockup.reference.html`/`Section-heading-lockup.reference.html` (Lane C's files, concurrent lane) — declared, not mine | ✅ (mine) / ⛔ **NOT MINE, DECLARED** |
| 7 | Snippet/token gate: 0 findings for these 3 files | `python3 knowledge/_validate_snippets.py 2>&1 \| grep -E "CTA-lockup\|Feature-grid-lockup\|Footer-doormat-lockup"` → **0 lines**. Repo-wide: 6 failures, all `Card-header-lockup`/`Hero-variants` (Lane C's files) | ✅ (mine) / ⛔ **NOT MINE, DECLARED** |
| 8 | a11y gate: 0 failures with all 3 present | `python3 knowledge/_validate_a11y.py` → *"a11y gate: 126 snippet(s), 0 failure(s), …"* | ✅ |
| 9 | 4px-grid gate clean | `python3 knowledge/_validate_grid.py` → *"GRID GATE PASS … (142 file(s))."* | ✅ |
| 10 | Descender-clip gate passes | `python3 knowledge/_validate_descender_clip.py` → *"DESCENDER-CLIP GATE PASS … (142 file(s))."* | ✅ |
| 11 | All 3 metas are schema-valid | `python3 knowledge/_probe_registry/probe_meta_schema.py --check` → *"126 meta(s) checked · 0 finding(s)"* (1 pre-existing exempt failure, `EXAMPLE-button.meta.json`, unrelated) | ✅ |
| 12 | ⛔ binds-resolve check-D FAILS for all 3 — DECLARED, not hidden | `python3 knowledge/_validate_binds_resolve.py` → *"119/125 canon blocks · 6 failure(s)"*, naming `CTA-lockup`, `Feature-grid-lockup`, `Footer-doormat-lockup` (+3 sibling-lane files) — no `.cn-*` block exists in canon.css yet | ⛔ **CONDUCTOR'S** |
| 13 | Zero horizontal overflow at 3 widths × 2 themes × 3 files, driven | headless Chromium (`chromium_headless_shell`, `--no-sandbox --disable-dev-shm-usage --disable-gpu`), widths 1400/700/340, both `data-theme`s: `document.documentElement.scrollWidth - clientWidth` → **0 in all 18 combinations, AFTER a fix — see §4** | ✅ **DRIVEN** |
| 14 | The responsive collapse actually happens, not just "no overflow" | at 340px: Feature-grid-lockup's up-2/up-3/up-4 grids all collapse to 1 column (measured, §4); Footer-doormat-lockup's mat collapses to 1 column and the legal bar stacks (Footer's own untouched rule); CTA-lockup's split arrangement flex-wraps to a stacked, full-width button pair — all **screenshotted and looked at**, see §5 | ✅ **DRIVEN** |
| 15 | Footer-doormat-lockup: content stub never overlaps the footer (lesson 7's non-sticky analogue) | driven: `.fdl-content.getBoundingClientRect().bottom` vs `.ft.getBoundingClientRect().top` at 1400/700/340px → **gap = 0 at every width** (adjacent, never negative) | ✅ **DRIVEN**, numeric |
| 16 | Hit-area advisory: 0 findings across all interactive targets in the 3 files | `python3 knowledge/_validate_hit_area.py knowledge/snippets/{CTA-lockup,Feature-grid-lockup,Footer-doormat-lockup}.reference.html` → *"42 target(s) measured, 0 finding(s), 8 exempt"* (CTA-lockup 2×4 button targets pass at both 1180/480; Footer-doormat-lockup 2×17 link targets pass, worst `a.arrow` 94.9×44; Feature-grid-lockup has no interactive candidate — display-only cells, correctly reported as such rather than silently vanishing) | ✅ **DRIVEN** |
| 17 | Font alias resolves in the render (not a stock fallback) | `document.fonts.check('16px HSBC_MtUnivers_Latin')` → **true**, all 18 combinations | ✅ |

---

## 4 · THE SPECIFICITY-TRAP DEFECT — found by DRIVING the browser, not by inspection

**First driven pass measured 21px horizontal overflow at 340px width, both themes, on
Feature-grid-lockup's up-2 and up-3 tiers only** (up-4 happened to pass by coincidence — see
below). The collapse rule read correctly on inspection:

```css
@container (max-width: 480px){
  .fgl-grid{grid-template-columns:1fr;}
}
```

but never fired for `.fgl-grid.up-2` or `.fgl-grid.up-3`, because **`.fgl-grid.up-2` (specificity
0-2-0) always beats a bare `.fgl-grid` (0-1-0) inside the `@container` block, regardless of source
order** — the same CLASS of trap wave-5 lesson 2 names for `:is()` weight in the trim block, in a
new outfit (a container-query override losing to a variant modifier class rather than to `:is()`).
`up-4`'s own 200px auto-fit floor happened to land on one column at 218px container width anyway,
which is exactly why the bug did NOT show there and would have been easy to miss on a single-tier
spot check. **Fix**: match the specificity explicitly —

```css
@container (max-width: 480px){
  .fgl-grid.up-2, .fgl-grid.up-3, .fgl-grid.up-4{grid-template-columns:1fr;}
}
```

Re-driven after the fix: **0 overflow across all 18 (file × theme × width) combinations** (§3 claim
13). The banner comment in the file now names this defect explicitly so a future reader does not
reintroduce it silently.

---

## 5 · WHAT WAS DRIVEN — a real browser, light AND dark, 3 widths, all 3 files

Headless Chromium (`chromium_headless_shell`, `--no-sandbox --disable-dev-shm-usage
--disable-gpu`; system libs reused from `/var/tmp/chromelibs*` per `_RUNBOOK-render-verify.md` §4,
no root; font farm reused from `/var/tmp/fonts-210w6B.conf`, same session's shared mount). Widths
**1400 / 700 / 340**, both `data-theme`s, all 3 files — **18 full-page screenshots taken and looked
at** (home: `NON-REPO: session outputs, w6d_renders/*.png`). Zero horizontal overflow measured in
all 18 (after the §4 fix). Interactions driven/measured: Feature-grid-lockup's grid collapse (§4),
Footer-doormat-lockup's content/footer non-overlap (§3 claim 15), the hit-area sweep (§3 claim 16).
Neither CTA-lockup nor Feature-grid-lockup nor Footer-doormat-lockup carries any JS of its own — all
three are static compositions (Button/Footer's own atoms are likewise static; Footer has no JS,
Button's press-physics is pure CSS per its own file) — so there is no additional scripted
interaction to drive beyond what §3/§4 already cover.

---

## 6 · EVERY OPEN DESIGN QUESTION — NAMED, NOT SETTLED

**All of these are Dave's.**

### Q1 — Is "Footer-doormat-lockup" the right shape for row 121, or should the lock-up ADD content beyond Footer's own doormat?
This lock-up composes Footer's doormat 100% verbatim, adding only a page-context stub. A real
mega-footer sometimes carries more (a newsletter sign-up row, app-store badges, a language
switcher, social icons) than Footer's own 4-column-mat-plus-legal-bar shape. None of those atoms
exist as gated components today, so nothing was invented to fill the gap — but if Dave's mental
model of "the full mega-footer arrangement" includes them, this lock-up under-delivers on the
itinerary row's own name. UNDRAWN, named rather than guessed at.

### Q2 — Should CTA-lockup ever carry a single button instead of a pair?
Both arrangements draw exactly a secondary+primary pair. A CTA band with a single action (e.g. a
simple "Get started" with no secondary "Learn more") is a common pattern this file does not draw —
`actions` is named as a 1-2 slot in the meta but only the 2-button case is in the reference.

### Q3 — Feature-grid-lockup's omission of per-cell actions — is that always right?
Drawn deliberately WITHOUT a per-cell button (see §2), on the theory that CTA-lockup is the
component that carries a call to action and a feature grid states benefits. Some real marketing
patterns do put a "Learn more" link on each card. Undrawn; if Dave wants it, Cards' own `a.arrow`
atom is the obvious source (Media card already uses it) and the composition would be additive, not
a rebuild.

### Q4 — Feature-grid-lockup's icon choices are illustrative, not semantic
`security-secure` / `device-mobile` / `data-chart` / `world-trader` were picked as plausible retail-
banking benefit icons, not because the itinerary named specific benefits. The COPY paired with each
(security / mobile / insights / global reach) is equally illustrative. Both are Dave's to replace
per an actual feature set.

### Q5 — CTA-lockup's `--band` colour — same question Footer's own `$decisionsForDave` 3 asks about `--surface`
Both bands sit on `surface/subtle`. Whether a CTA band should read as the SAME neutral family as a
footer band, or should be visually distinct (e.g. sit on `background/default` with only a rule to
separate it), is unexamined here — carried from Footer's own open question rather than resolved.

### Q6 — Should the split CTA arrangement force `text-align:left`, or is the natural flex-wrap centring (observed at intermediate widths, §5) the intended behaviour?
At container widths between roughly 560px and ~600px, the split arrangement's title block and
button pair don't fit on one row and wrap via ordinary flexbox flow (not the explicit `@container`
override, which only fires under 560px) — visually this can read as similar to the centred variant
when the heading text is long enough to span most of the band width. Whether that's acceptable
incidental behaviour or needs an explicit mid-width rule is UNDRAWN.

---

## 7 · WHAT STAYS UNPROVEN

1. **The canon-block projection.** `_validate_binds_resolve.py` check D FAILS for all 3
   (`.cn-cta-lockup`, `.cn-feature-grid-lockup`, `.cn-footer-doormat-lockup` do not exist in
   `canon.css`) — 6 failures total in that gate run, shared with 3 sibling-lane files from the same
   wave. Until the conductor projects those blocks, **Console, Legacy and Supercharge are UNPROVEN
   for all 3 lock-ups** — only the light/dark legs authored in each snippet have been seen.
2. **`_validate_kg.py`** was not re-run this lane (no new context/pattern names were introduced
   beyond what the consumed atoms already carry, so no new node is expected, but this was not
   independently re-measured) — same declared gap as the wave-5 Lane D precedent.
3. **Only 3 widths were driven** (1400/700/340), and only ONE browser engine (headless Chromium),
   matching the #209/#210-wave-5 Lane D precedent's own declared limit.
4. **Nothing here has been seen by Dave**, and nothing is registered anywhere (no
   `MIGRATED_SNIPPETS`, `CATEGORIES`, `component-types.json`, `gen_showroom.py`,
   `gen_kg_edges.py` entry, `canon.css` block, or `_rulings.json` row).
5. **CTA-lockup's copy and Feature-grid-lockup's icon/copy pairings are illustrative** (§6 Q4),
   not derived from a named feature set or brand copy deck — Dave's to replace.

---

## 8 · BLAST RADIUS (lesson 6) — declared: NONE

No shared file (`canon/canon.css`, `canon/type.css`, `component-types.json`, or any other snippet)
was edited by this lane. All three deliverables are new, self-contained HTML documents; the classes
they use that also appear in canon/type.css's composite selector lists (`.btn`, `.badge` is NOT
used here, `t-cm-button`, `t-ed-body-small`, etc.) are CONSUMED via the markup-class route, not
extended by editing type.css's own selector lists. There is therefore no global-selector reach to
declare, unlike wave-5 Lane D's `.badge`/`.seg` finding — this lane's compositions happen not to
touch a selector list that needed widening.

---

## 9 · HANDOFF TO THE CONDUCTOR

1. `.cn-footer-doormat-lockup`, `.cn-cta-lockup`, `.cn-feature-grid-lockup` blocks in
   `canon/canon.css` (clears 3 of the wave's 6 check-D failures, shared with the other lanes' 3).
2. Re-run `gen_kg_edges.py` if these three are kept (residual §7.2).
3. `component-types.json` · `CATEGORIES` · `gen_showroom.py` · `_validate_radius.MIGRATED_SNIPPETS`
   registrations, if kept.
4. **Q1 (biggest structural question)**: does "the full mega-footer arrangement" mean Footer's
   doormat as-is, or does it imply additional content (newsletter, app badges, language switcher,
   social icons) that no gated atom currently supplies?
5. This receipt's own store row (`W-80`, added at creation per the #185 forgotten-document
   class — see the wrap chain).
