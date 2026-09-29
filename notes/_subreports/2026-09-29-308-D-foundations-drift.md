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
