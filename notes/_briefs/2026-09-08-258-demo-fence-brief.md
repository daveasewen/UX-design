# #258 demo-fence brief — enact s258-D3 across the snippets (lanes A/B/C) + skill and gate (lane G)

**Model: Opus 5 per lane. Conductor: Fable (#258).** Ruling: `knowledge/_rulings.json` id `s258-D3`. Premise: `notes/_subreports/2026-09-08-258-P-demo-chrome-probe.md` (READ IT FIRST — it has the per-slug table, the convention and the risks).

## THE CONVENTION (from the probe — do not invent another)
- Markup: `<!-- ===== APOLLO-DEMO <what> START (showroom harness — never copy) ===== -->` … `<!-- ===== APOLLO-DEMO <what> END ===== -->`, fenced in place.
- Chrome CSS → ONE fenced block `/* ===== APOLLO-DEMO css START … */ … /* ===== APOLLO-DEMO css END ===== */` placed after the AUTO-PARTIAL block. Never inside any `AUTO-*` span.
- Chrome JS → a separate fenced `<script>` at end of body, never inside `AUTO-BEHAVIOUR`.
- Vars the COMPONENT reads (`--demo-width` etc.) are NOT fenced: the component rule gets a real default (e.g. `.dg{width:var(--dg-max,760px)}` or a plain value), and the harness sets that var from INSIDE the fence. Keep `_render_links.py` / `_render_tags.py` / `_validate_compose.py:42`'s `--demo-width` runtime usage working — check them before renaming anything they set.
- ACCEPTANCE per file: (1) delete every fenced span programmatically → the component still renders (playwright, 1440, light + dark; compare bounding boxes of the component root before/after — must match within 1px except chrome-only regions); (2) `_validate_snippets.py` exit 0; (3) `gen_component_partials.py --check` exit 0; (4) the file with fences intact still shows the chrome in the showroom render (open via srcdoc as `showroom/` does, or render the raw file).

## LANES
- **A** slugs `Action-bar … Hero-variants` (20 files, 8 dangerous) · **B** `Image-block … Stats-band-lockup` (20, 8) · **C** `Status-indicator … Transfer-list` (21, 11). Your list = the probe table rows in your range with chrome present. Do the DANGEROUS ones first.
- **G** (skill + gate, no snippets): `apollo-spider/skills/generate-from-canon/SKILL.md` — end of rule 2 (before 2a): never copy inside an `APOLLO-DEMO` fence; one clause in 2a (scripts) and Procedure step 3. `knowledge/_validate_receipt.py` `check()` after REGION-UNRECEIPTED: `re.search(r'APOLLO-DEMO[^\n]*(START|END)', html)` ⇒ `FAIL:DEMO-CHROME-COPIED`; add a selftest arm (copied fence ⇒ FAIL; clean ⇒ PASS). Also `apollo-spider/skills/check-with-gates/SKILL.md` if it lists the FAIL codes. Add the convention to whatever doc lists `AUTO-*` / `APOLLO-SPLICE` marker grammar (grep for `APOLLO-SPLICE`). Run the selftest; quote exits.

## RULES
⛔ Touch only your lane's files. ⛔ No `git checkout`/`stash`, no `_build_all.py`, no commit/push, nothing written under `knowledge/_screen-gate/` (don't run `_validate_screen.py`). Rule nothing. Every claim carries a token. Playwright: `knowledge/_ROBUSTNESS-PORTABILITY.md` if fresh (`LD_LIBRARY_PATH=$HOME/.local/chromelibs PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1`).
Subreport: `notes/_subreports/2026-09-08-258-<lane>-demo-fence.md` — files, acceptance results per file, NOT done, tokens.
Return ≤12 lines: files fenced / skipped (why), acceptance pass count, any component that broke and what you did, tokens.
