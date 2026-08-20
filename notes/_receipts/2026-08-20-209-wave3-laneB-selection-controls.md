# Receipt — Wave 3 Lane B (selection controls), #209

Brief: `notes/_briefs/2026-08-20-209-wave3-fanout-brief-v1.md`. Worker lane, NEW FILES ONLY —
no edits to existing files, no git, no registry/spine touches. This receipt is the one
document the conductor asked for; everything below is this lane's own record, not a ruling.

## 1 · File list

| file | role |
|---|---|
| `knowledge/snippets/Range-slider.reference.html` | new snippet |
| `knowledge/components/range-slider.meta.json` | new meta |
| `knowledge/snippets/Rating.reference.html` | new snippet |
| `knowledge/components/rating.meta.json` | new meta |
| `knowledge/snippets/Transfer-list.reference.html` | new snippet |
| `knowledge/components/transfer-list.meta.json` | new meta |
| `notes/_receipts/2026-08-20-209-wave3-laneB-selection-controls.md` | this receipt |

All three snippets carry the CURRENT leading-trim CANARY block, copied verbatim from
`knowledge/snippets/Command-palette.reference.html:36` (byte-identical selector text), link
`../canon/type.css`, and declare zero raw `font-family`/`font-size`/`font-weight` — every text
element carries a `.t-cm-*` composite class directly (the Command-palette pattern: `.t-cm-label`,
`.t-cm-caption`, `.t-cm-input`, `.t-cm-figure-5/6`, `.t-cm-legal`), because `canon/type.css`'s own
bespoke-class matching (`.chip`, `.status`, …) is a shared file this lane cannot edit. No `intent`
field was authored anywhere. No token was minted — every `#token-manifest` var maps to an existing
address; each meta's own `tokens.$note` says so explicitly. No `binds` array in any of the three
metas uses the dotted `rag.*` grammar because none of the three components bind a RAG/status
address at all — so the #209 dotted-vs-slash lesson doesn't have a live test case here, and I'm
naming that absence rather than silently taking credit for having applied it.

## 2 · Claim table (probeable tokens)

| # | claim | probe |
|---|---|---|
| C-1 | Range-slider accretes from the gated Slider — track-fill gradient technique, thumb geometry, focus-ring treatment, "value as text" answer are copied, not re-drawn | `diff <(grep -oE 'width:20px; height:20px|border-radius:50%|::-webkit-slider-thumb' knowledge/snippets/Slider.reference.html) <(grep -oE 'width:20px; height:20px|border-radius:50%|::-webkit-slider-thumb' knowledge/snippets/Range-slider.reference.html)` → same three idioms present in both files |
| C-2 | Range-slider's only authored (non-copied) mechanism is the two-handle clamp + z-index handoff | `grep -n "no single-handle precedent" knowledge/snippets/Range-slider.reference.html knowledge/components/range-slider.meta.json` → both files name it explicitly |
| C-3 | Range-slider driven: keyboard ArrowLeft×4 on the high handle decrements it and the low handle stays clamped | Playwright drive (see §3) — printed `after 4x ArrowLeft on hi handle: displayed hi = £600 \| lo.value= 200 hi.value= 600` |
| C-4 | Rating's checkbox/radio idiom is Selection-controls' native radiogroup, copied, not a custom keydown handler | `grep -c "addEventListener('keydown'" knowledge/snippets/Rating.reference.html` → `0` (Selection-controls' chip radiogroup has a keydown handler; Rating's plain radios do not, by design) |
| C-5 | Rating's star glyph is the real library asset, not invented | `diff <(grep -A1 'M9 4.24501' knowledge/assets/icons/global-controls/favourite-star.svg) <(grep -A1 'M9 4.24501' knowledge/snippets/Rating.reference.html)` → the path data is byte-identical |
| C-6 | Rating driven: clicking the 5-star label checks the input and updates the live-region text | Playwright drive (see §3) — printed `value text after clicking 5-star label: 5 out of 5 \| #r1-5 checked: True` |
| C-7 | Transfer-list's checkbox (including the indeterminate "select all" header) is Selection-controls' checkbox, copied verbatim | `grep -c "stroke-dasharray:22; stroke-dashoffset:22" knowledge/snippets/Selection-controls.reference.html knowledge/snippets/Transfer-list.reference.html` → present in both, identical value |
| C-8 | Transfer-list driven end-to-end: check two rows, move them, counts/status/header-state all update correctly | Playwright drive (see §3) — printed `sel_count: 3 items`, `avail_count: 2 items`, `sel_status: 2 items moved to Selected`, `sel_items: ['Joint account', 'Sterling current account', 'USD holding account']`, then select-all on the remaining 2 rows → `checked_count: 2 header checked: True` |
| C-9 | All three metas conform to `meta.schema.json` | `python3 -c "import json,jsonschema; [jsonschema.validate(json.load(open(f'knowledge/components/{s}.meta.json')), json.load(open('knowledge/components/meta.schema.json'))) for s in ['range-slider','rating','transfer-list']]"` → no exception raised |
| C-10 | The repo-wide meta-schema probe (P-1) sees the three new metas and reports zero findings | `python3 knowledge/_probe_registry/probe_meta_schema.py --check` → `P-1 meta-schema sweep: 98 meta(s) checked · 0 finding(s) · 1 exempt failure(s) (EXAMPLE-button.meta.json)` — 98 includes the 95 pre-existing + this lane's 3 |
| C-11 | All four theme legs (mono light/dark × the two colour vars actually varying) render without error and font-load asserts true | Playwright render, 6 screenshots total (2 per snippet, light+dark), `document.fonts.check('16px HSBC_MtUnivers_Latin')` → `True` on every call |

## 3 · What was driven

Environment reachable and used exactly as specified: `PYTHONPATH=/var/tmp/pylibs-s201
LD_LIBRARY_PATH=/var/tmp/chromelibs-s201/root/usr/lib/aarch64-linux-gnu
PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-s197`, executable resolved from
`/var/tmp/pw-browsers-s197/chromium_headless_shell-*/chrome-linux/headless_shell`, launch args
`--no-sandbox --disable-dev-shm-usage --disable-gpu`.

- **Rendered, light + dark, all three** (screenshots read back and visually inspected, not just
  produced): Range-slider, Rating, Transfer-list. `document.fonts.check` asserted true on all 6.
- **A real bug was caught by rendering, not by reading the source**: the star glyph (Rating) and
  all four chevron glyphs (Transfer-list) were first authored as `<symbol>`/`<use>` references
  with no `fill` attribute on the inner `<path>`, relying on a `svg path` CSS descendant selector
  to colour them. The first render showed every glyph solid black in BOTH themes — a `<use>`
  instance's shadow-tree content does not match an ordinary light-DOM descendant selector from
  outside it (only genuinely inherited properties like `color`/`currentColor` cross that
  boundary). Fixed by adding `fill="currentColor"` on every `<path>` inside every `<symbol>` and
  switching every CSS rule from setting `fill` to setting `color` on the referencing `<svg>`. This
  is the load-bearing reason "driven, not just rendered" mattered here: a static read of the
  markup would have looked correct (the CSS var names, the theme forking, the selector nesting
  were all superficially right) and the defect would only show up as pixels.
- **A second bug, same render pass**: Transfer-list's panel-header checkboxes (`#avail-all`,
  `#sel-all`) sat outside the `.row` wrapper the hidden-input CSS rule was scoped to
  (`.row input[type=checkbox]`), so the native (unstyled) checkbox rendered doubled up next to the
  custom glyph. Fixed by widening the rule to `.panel input[type=checkbox]`. Caught by the same
  screenshot, not by re-reading the CSS.
- **Driven interactively with Playwright** (clicks/keyboard, not just a static screenshot),
  three short scripts, one per component — full output quoted in the claim table (C-3, C-6, C-8).
  Transfer-list was driven the hardest: checked two specific rows by clicking their `<label>`
  (`.check()`/`.click()` on the native input itself both fail — the input is `opacity:0;
  width:0; height:0`, so Playwright's actionability checks refuse it; clicking the `<label>` via
  `page.eval_on_selector(...".click()")` was the way through, and is itself evidence the hidden-
  input pattern is faithfully invisible/inert to a real automated actor, which is what the pattern
  is for), clicked "Move selected", and read back both panels' item lists, counts, the `role=
  "status"` text, and the header checkbox's `checked`/`indeterminate`/`disabled` triple after a
  follow-up "select all" click.
- **An accidental repo-write, caught and reverted in-window**: `python3
  knowledge/_validate_snippets.py --help` did not just print its docstring — the script fell
  through to a full gate run and wrote `knowledge/_SNIPPET-AUDIT.md` (a shared, generated,
  conductor-owned file). Caught within the same window via `git status`; by the time it was
  re-checked the file was clean again (no diff, no longer listed dirty) — most likely a
  concurrent lane's own write/regeneration passing through the same shared file, since three
  worker lanes are running in parallel against one working tree. No further repo-wide gate that
  writes a tracked file was run afterward by this lane; final `git status --short` before writing
  this receipt shows only this lane's own new untracked files, nothing modified. Flagged here
  because a wave-3 successor should NOT invoke `_validate_snippets.py`/`_validate_a11y.py`
  standalone from a worker lane at all — they write shared audit files that are the conductor's
  serial-set territory, and `--help` does not safely no-op.

## 4 · Every design question NAMED (never settled)

From `range-slider.meta.json` `$decisionsForDave`:
- Should crossing the low/high clamp boundary produce a message, or stay a silent clamp (as
  built)?
- Should Range-slider inherit Slider's tick-marker idiom (itself carrying a DEPRECATED-token
  finding) or stay bare, as built?
- Is £/GBP the right specimen currency, or should the canonical specimen be currency-neutral?

From `rating.meta.json` `$decisionsForDave`:
- Filled-star colour: mono ink (as built, because the store has no gold/amber seat and "no token
  minting" is on this wave's DO-NOT-RULE) or a new warm token?
- Whole-star-only input (as built) or half-star precision — which needs a fresh hit-target/
  keyboard design this pass did not attempt?
- The 32px (not 44px) per-star target: accepted for compact/inline placements, or does Rating
  need a distinct "roomy" 44px-target variant for a standalone rating page?

From `transfer-list.meta.json` `$decisionsForDave`:
- After a move, should focus follow the item into its new panel, jump to the panel heading, or
  stay on the move button (as built)?
- Is the 280px per-panel scroll cap a real ceiling or a placeholder that needs its own design
  (search/virtualise) at scale?
- Is drag-and-drop wanted alongside checkbox+button, or is checkbox+button the whole surface by
  design (as built — the itinerary note says only "move-between-lists")?

Two additional questions surfaced by the render pass itself, not pre-existing in the itinerary,
each recorded in its meta's `tokenValidation.$note`:
- Rating/Transfer-list: is the `<symbol>`/`<use>` + `fill="currentColor"` pattern (now fixed in
  both) the idiom every future icon-bearing snippet should copy, or should the library instead
  standardise on inlining `<path fill="currentColor">` directly with no `<symbol>` indirection?
  This lane picked the symbol form because Payment-card-visual's meta names "byte-matched via
  `<symbol>`" as its own precedent — but that component's icon (contactless) apparently never hit
  this bug, or the bug was never rendered against. Worth a cross-lane check.
- Should `_validate_snippets.py`/`_validate_a11y.py` gain a real `--help`/no-op path that doesn't
  fall through to a full run-and-write? (see §3, accidental write)

## 5 · What stays UNPROVEN

- **The conductor's full serial-set gates were NOT run by this lane** — deliberately, per THE JOB
  and the DO-NOT-RULE (registry/MIGRATED_SNIPPETS/CATEGORIES/spine/git are the conductor's). Only
  run: (a) `probe_meta_schema.py --check` (a registered read-only probe, safe) and (b) an in-memory
  `jsonschema.validate` against `meta.schema.json` for the three new metas. NOT run:
  `_validate_snippets.py` (token-fidelity/ARIA/contrast/all-caps/focus/typography/copy-lint —
  after the accidental-write incident this lane deliberately stopped invoking it),
  `_validate_a11y.py`, `_validate_radius.py` (MIGRATED_SNIPPETS registration is explicitly the
  conductor's), `_validate_icons.py`, `_validate_coverage.py`, `_validate_state_contrast.py`.
  Every `tokenValidation.result` field in all three metas says so explicitly ("PROPOSED … no gate
  has been run by this worker").
- **Four-theme (mono/legacy/console/supercharge) contrast was NOT independently measured.** Only
  the MONO light/dark pair declared in each `#token-manifest` was rendered and eyeballed. The
  Command-palette precedent found a real cross-theme failure this way (`$rebind` note in its
  meta) — the same class of finding could exist here and has not been looked for.
- **No showroom entry, no `.cn-*` canon.css scope, no CATEGORIES entry** — all conductor's,
  per the DO-NOT-RULE-APPEND.
- **Rating's read-only (aggregate) variant's clip-path fractional fill was visually checked at one
  value (4.3/5, 86% width) only** — not swept across the 0–100% range for rounding/pixel-snapping
  artefacts at odd fractions (e.g. exactly on a star boundary).
- **Transfer-list's responsive stack (below 480px, container query) was declared in the meta and
  authored in CSS but NOT rendered at that width this pass** — only the 1000px-viewport desktop
  layout was screenshotted and driven.
- **No cross-browser check** (Chromium headless-shell only, per the environment given).
- **Focus-visible outline on the move buttons and star labels was authored (`:focus-visible{
  outline:2px solid var(--focus)…}`) but not captured in a screenshot with an element actually
  focused** — the driven scripts used `.focus()`/click, not Tab-key traversal, so the VISUAL focus
  ring was never itself rendered and inspected, only the underlying DOM focus state was asserted.
