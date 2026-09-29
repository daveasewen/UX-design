COUNTS: pages regenerated to scratch 8 / identical 2 (grids-12col, photography) / differing 6 (5 by one line: the supercharge caption fallback; 1 logos 12 -> 8) / other differences 0 / causes 2 / rulings cited 4 (s220-D1, s308-D1, s282-D4, s227-D8a context) / renders 9 PNG (7 embedded) + 2 page renders / review page 1 / files written in the repo: this report, the page, notes/_lanes/308/D/* / commits 0 / git writes 0

# #308 lane D — the foundations drift: diagnosed, shown, not fixed

provenance: 308 · 2026-09-29 · lane D (Opus 5.5), at Dave's seat on the mount through device_bash · read-only git only (log, show; `git status` was avoided after it tried to take index.lock) · no regeneration over the committed pages · no Project memory
status: observed. Every figure was printed by the generator, a selftest, a gate or the browser at the seat.

Dave, 14:44 BST: "lets look at the foundations drift after :)"

## The answer

Two differences. The pages are right on the colour and the generator is right on the logos.

| difference | pages | right side | cause |
|---|---|---|---|
| `--bm-cap-dark-darkgrey` fallback for supercharge: `var(--color-neutral-5,#312C26)` becomes `…#313131` | bento, bento-rails, grids-dashboard, grids-display, grids-gallery | **committed** | generator's colour reader broke at #288 |
| logos 12 -> 8 (and "12 variants/files" -> 8 in prose, plus a new "4 expected file(s) missing" line) | logos | **regenerated, nearly** | s282-D4 scrapped the identifier lockup at #282; the page was last written at #245 |

grids-12col and photography are byte-identical. There are no other differences.

## 1 · The supercharge caption: the generator broke

- The value comes from `gen_bento_matrix_217.CAPTION_GROUND_MINTS`, through `resolve_token()`, `theme_tokens()` and `_css_block()`. `_css_block` uses `re.search`, so it returns the FIRST block that matches `^\[data-apollo-theme="<t>"\]\s*\{`.
- canon.css now has two supercharge blocks, at lines 22135 (AUTO-BENTO-ROLE-VARS, two gutter vars) and 26442 (AUTO-THEMES, holding `--color-neutral-5: #312C26`). Console has blocks at 22131 and 24788. The first block of each was introduced by **71b3363c** (#288 capture, 2026-09-19, `gen_bento_role_vars.py`, no ruling inscribed that session).
- **Common/legacy is blind too, and has been for longer.** Since **53303b0f** (#228, 2026-08-31, the s227-D8(a) `common` alias), the legacy theme block opens `[data-apollo-theme="legacy"],\n[data-apollo-theme="common"]{`, and the anchored regex matches no legacy block at all (1 match before 53303b0f, 0 after). Measured: `theme_tokens("legacy")["--badge-background"]` is `var(--rag-error)`, Mono's value, while canon gives legacy `#DB0011`. #305 W2 wrote that legacy was "spared". That is wrong: legacy parses nothing.
- **Rulings.** s220-D1 (2026-08-27): dark caption lift by neutral primitive, supercharge warm/5 `#312C26`. s308-D1 (today, by click): "Close it: the four lifts are right". The committed pages (5ae4d32c, #245, 2026-09-03) predate #288, so they carry the ruled value.
- **Visible?** Not today. Supercharge dark with the darkgrey caption computes rgb(49,44,38) on both pages with canon loaded, and the two 2x PNGs are byte-identical. With canon.css blocked, committed paints `#312C26` and regenerated paints `#313131`. It is the fence regressing, not the picture.
- **Proof there is no other cause.** I replaced `theme_tokens` in memory with a reader that merges every top-level rule whose comma-separated selector list contains the exact theme selector, in the order root, dark, theme, theme dark. Supercharge dark neutral-5 then gives `#312C26`, and **7 of 8 pages regenerate byte-identical**. logos.html is the only one that differs. Driver: `~/scratch308D/regen_fixed.py` (seat scratch, not in the repo).
- **Prior sighting.** `notes/_subreports/2026-09-27-305-W2-remaining.md` §1 item 1 named the first-match fault while holding the rails file. No `_state.json` row carries the fix.
- **Blast radius of the fix.** The same reader feeds `_bento_edit_rails.json` (W2's held drift), `gen_mono_gallery_221.py`, `verify_bento_matrix_217.py` and `_gate_fallback_drift_221.py`. Fixing it will move the rails file. W2's item 2 (the nav family as a tile group) is separate and stays Dave's.

## 2 · The logos: the page is stale

- **da9f824e** (#282, 2026-09-18), s282-D4, Dave: "scrap the identifier versions". The set is 2 lockups x colour/mono x light/dark = 8. The four `masterbrand-identifier-*.svg` files were removed from the tracked tree and moved to `_to_delete/`. The commit itself said "Showroom gap inherited, declared."
- The committed logos.html draws 12 tiles, and **4 are broken images**: 4 failed requests, naturalWidth 0.
- The regenerated page draws 8 with no broken images. But `gen_foundations_217.py` still has `masterbrand-identifier` in `LOGO_ORDER` and `LOGO_LOCKUP` (lines 738–745), so it prints "4 expected file(s) missing from disk". It also keeps the "two ON-DARK identifier exports carry no identifier label" finding (ds-045, around line 1854), which s282-D4 made moot, and its docstring still says "the 12 exported HSBC marks".
- Fix: drop the lockup, the finding and the "12". Then regenerate logos.html.

## 3 · Why nothing caught it (the class)

- `gen_foundations_217.py --check` exists and says **OUT OF SYNC** on 6 pages today (~60 s). It is not in `_build_all.py` and not in `.github/workflows/gates.yml`. The last lane I can find that ran it is #245 L5.
- `gen_bento_matrix_217.py --selftest` has **9 red bites today**. C0 ("the static token resolver AGREES WITH THE BROWSER") would have gone red at #288. C4d, C4g, C4i and C4k (the caption lift) and 12 (fallbacks equal canon's answer) are red for the same cause. R6d and R6e are the rails/nav-family drift W2 held. The selftest is unwired.
- `_gate_fallback_drift_221.py` is advisory by its own header and unwired. It uses the same broken reader, so it reports `var(--color-neutral-5,#312C26)` as DRIFTED, which flags the ruled value as wrong. Its other 12 reds (`--border-subtle #D7D8D6`, `--text-secondary #545454`) are legacy's own values, which the reader cannot see, so they are likely false reds. I did not re-run it on the fixed reader.
- The class is instrument-without-a-consumer and unwired-validators: all three instruments would have caught this, and none of them runs.

## The page

`notes/_REVIEW-308-foundations-drift-2026-09-29-v1.html`: answer first, one section per difference with the picture pairs, the class section, then three calls with recommendations plus a note field. It has a decision bar with "Copy as text" headed "Session 308 · foundations drift · answers", localStorage in try/catch, and the rv-back link right after `<body>`. Rendered at 1440 and 390 (`notes/_lanes/308/D/D-page-1440.png`, `D-page-390.png`): scrollWidth equals clientWidth at both widths, 0 page errors, 0 failed requests, 7 of 7 images loaded, and a chip click counted "1 of 4 answered". Checked by eye.

Calls:
1. Fix the generator's colour reader so it reproduces the committed pages (recommended) · accept the grey · leave it.
2. Take the identifier lockup out of the generator, then regenerate logos.html with 8 (recommended) · regenerate as it stands · leave the 12.
3. Wire `gen_foundations_217 --check` and `gen_bento_matrix_217 --selftest` into the build, blocking, after 1 and 2 land (recommended) · advisory · not now. The fallback gate stays advisory until it has been re-run on the fixed reader.

Order if all three are taken: reader, then logos list, then regenerate logos.html (the only page that then changes), then wire.

## Files

- `notes/_REVIEW-308-foundations-drift-2026-09-29-v1.html`
- `notes/_lanes/308/D/D-caption-committed-canon.png`, `D-caption-regen-canon.png`, `D-caption-committed-nocanon.png`, `D-caption-regen-nocanon.png`
- `notes/_lanes/308/D/D-logos-committed.png`, `D-logos-regen.png`, `D-logos-regen-notes.png`
- `notes/_lanes/308/D/D-render-log.json` (computed colours, broken-image lists), `render_D.py` (driver)
- `notes/_lanes/308/D/D-page-1440.png`, `D-page-390.png` (page checks, not embedded)

Not done, by the brief: no regeneration of committed pages, no generator edit, no commit. Scratch lives at the seat's `~/scratch308D/` (outside the repo). `/dev/shm` does not persist between device_bash calls at this seat, so the scratch tree went under $HOME instead.

---

# Round 2 — BUILD: Dave took all three calls (17:01 BST)

COUNTS (round 2): rulings 3 inscribed (s308-D31..D33, store 820 → 823), 3 stamped (D31 enacted at c78cdb14, D32 enacted at a35e2474, D33 enacted in part at a95444a3) / row W-308d3 closed / commits 4 (c78cdb14, a35e2474, a95444a3, and the report commit) / pages regenerated 1 (logos.html) / selftest reds 9 → 2 (both HELD for Dave) / build steps 166 → 167 / pushed no

His words: `notes/_lanes/308/DAVE-RULINGS-2026-09-29-1708-drift-and-edges.md` § Foundations drift, committed in c78cdb14. There are three clicks, one per recommendation.

## 1 · The colour reader (s308-D31), c78cdb14

- `gen_bento_matrix_217.theme_tokens()` now merges EVERY top-level canon.css rule whose comma-separated selector list names the theme. It walks the tiers root → `[data-theme="dark"]` → theme → theme dark (both the `][` and the descendant forms), in source order within each tier. Comments are blanked and @-rule bodies are skipped whole, so a `@media` value cannot leak in. `_css_block` stays, used as the mutant in the new bite.
- Proof: all 8 pages regenerated in memory. 7 are byte-identical to HEAD, and logos.html is the only one that differs (call 2). Supercharge dark neutral/5 is `#312C26`, and legacy's badge is `#DB0011` (it had been reading mono's alias since #228).
- New selftest bites: **C0m** uses a planted sheet with a gutter block ahead of the colour block, a two-line `legacy, common` list, an `@media` block that must not leak, and a comment containing a brace. The retired first-match reader runs beside it as the mutant and must read `#313131` and `None`. **C0n** checks the live canon. I also ran an in-memory mutation with the first-match reader swapped back in: C0m and C0n both go red.
- **The grouping dial follows s308-D19.** Lane E (6bb91a0b) moved kpi-tile's and stat-card's `groupsWith` self-lines into `count: {min: 2, per: "group"}`. `grouping_dial()` now reads a `per: "group"` count as a same-kind group, so the fact keeps one home (s234-D4) and the dial follows it.
- **Fallback-drift gate (advisory).** It borrows the fixed resolver, so `#312C26` is canon's answer again (bites 7 and 7b). The fix exposed canon's global `--ink` (the `:root, [data-theme=…]` alias block), which put six `var(--ink,#1A1A1A)` consumers falsely red. A page-local alias now shadows canon's same-named token, as it does in the browser in scope. It is read from the file's own declaration, else from the shared preamble across the glob (bites 8, 8b, 8c mutant). Selftest: 16 bites. Run: 13 drifted → **0 drifted, 1 local-drift**: `gen_grids_218.py var(--surface-2,#F3F3F3)` against the preamble's `#F0F0F0`. That is a real #221 leftover, reported and not fixed, because fixing it changes the grids pages' fallback bytes.

## 2 · The logos (s308-D32), a35e2474

- `LOGO_ORDER = ["hexagon", "masterbrand"]` with the s282-D4 note. The identifier `LOGO_LOCKUP` row, the moot ds-045 finding block, "Three lockups" and the "12"/"twelve" prose are gone. Selftest bite 10 is re-based to 4 light + 4 dark tiles. Bite 12 now asserts that ds-045 and every `masterbrand-identifier` file are OFF the page, with 8 rows. `--selftest` passes 46 bites; `--check` reports 8 pages in sync.
- **Render at the seat** (mono light and supercharge dark, full page): `notes/_lanes/308/D/D2-logos-mono-light.png` and `notes/_lanes/308/D/D2-logos-supercharge-dark.png`. Both show 8 tiles, 0 broken images, 0 failed requests and 0 page errors. There is no "missing from disk" line, no ds-045, and no horizontal scroll. I checked both by eye: the grounds are pinned per tile and the chrome follows the theme.
- `gen_library_214 --check` OK and `gen_showroom --check` OK (lane L's picker guard included).

## 3 · Wiring (s308-D33), a95444a3, enacted in part

- **Wired BLOCKING**: STEPS label "foundations pages sync — the eight showroom/_foundations/ pages equal their generation (BLOCKING, s308-D33, wired #308)" → `_render/gen_foundations_217.py --check`, appended last, with its GATE route row in the same edit. `check_routes()` resolves 167 labels. The step is green at HEAD and takes about 60 s. CI runs `_build_all.py`, and the 251 photography derivatives are tracked, so the check can run there.
- **HELD, not wired: `gen_bento_matrix_217.py --selftest`.** 9 reds → 2 reds, and both remaining reds are the same cause:
  - **R6e**: the grouping dial now also derives `navigations + sidebar-nav + tab-bar`. navigations has been in the template's `$composes` since #231, and its `groupsWith` edges to sidebar-nav and tab-bar were **declared by the #261 nav lane** ("SAME-ANSWER", "MODULE level (s245-D7 Q7(a))"). No ruling names them.
  - **R6d**: the rails file on disk is not this generation. With the reader and count fixes, a fresh `--rails` differs from `_bento_edit_rails.json` in the nav group **only** (measured with a sorted-key JSON diff).
  - **Why stop here**: including the nav family as a dashboard tile group, or excluding module-level same-answer families from the dial, is a choice between s245-D7's derivation and the #261 family edges. #305 W2 put the same question to Dave ("a question, not a regen"). I did not regenerate the rails file and did not re-base the bite. Wiring the selftest blocking now would turn every build red, so it is wired when he answers. The `_build_all.py` comment and s308-D33's status both say so.

## Record

- `_inscribe_ruling.py` dry run, then write, for s308-D31, D32 and D33. The reconstruction proof passed each time. Receipt: `notes/_lanes/308/D/inscribe.write.txt`. Entries: `notes/_lanes/308/D/entries/`.
- W-308d3 closed with `_wrap_rows.py` (`notes/_lanes/308/D/rows.json`). `closed_by` names the three rulings.
- `--set-status`: D31 `enacted` at c78cdb14, D32 `enacted` at a35e2474, and D33 `enacted in part …` at a95444a3, with the hold written into the status.

## Verification before the last commit

- Sweep `outputs/308/sweep.py` over steps 1–166: the only reds were [11] (seat-only), [13] and [127] (timeouts) and [163] and [164] (advisory), all of them known. I ran step 167 directly, because the sweep's 40 s timeout is shorter than the check: `gen_foundations_217 --check` OK, 8 pages.
- `gen_kg_sources --check` OK. `_wrap_regen --checks-only --session 308`: fresh, apart from `_gen_titles` (it refuses until the wrap, as expected) and `_render_rulings`, which I regenerated for this commit.
- `canon.css` and `notes/_BUILD-VERDICT-LOG.jsonl` are byte-identical to HEAD throughout. I never ran `git status` and did not push.
