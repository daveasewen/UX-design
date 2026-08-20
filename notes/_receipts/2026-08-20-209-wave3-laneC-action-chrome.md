<!-- LANE RECEIPT · owner=human/agent · Wave 3, Lane C (action chrome), session #209 -->
# Wave-3 Lane C receipt — action chrome (split-button · fab · back-to-top)

Brief: `notes/_briefs/2026-08-20-209-wave3-fanout-brief-v1.md`. Worker lane, NEW FILES ONLY —
no registry/CATEGORIES/spine/component-types.json edits, no git operations, no `_rulings.json`.
The conductor reconciles, runs the serial set, gates, and lands one commit.

## 1 · File list

| file | role |
|---|---|
| `knowledge/snippets/Split-button.reference.html` | new snippet, itinerary row 6, slug `split-button` |
| `knowledge/components/split-button.meta.json` | new meta |
| `knowledge/snippets/Fab.reference.html` | new snippet, itinerary row 7, slug `fab` |
| `knowledge/components/fab.meta.json` | new meta |
| `knowledge/snippets/Back-to-top.reference.html` | new snippet, itinerary row 38, slug `back-to-top` |
| `knowledge/components/back-to-top.meta.json` | new meta |
| `notes/_receipts/2026-08-20-209-wave3-laneC-action-chrome.md` | this receipt |

All three itinerary rows were re-probed at #209 (`reviews/ITINERARY-STATUS-2026-08-19-v1.json`)
before building — n=6 Split button (P3, "Nice-to-have", basis=map, drift AGREES, all five
artefact probes negative), n=7 FAB (P3, "Mobile floating action", basis=absent, drift AGREES,
all five probes negative), n=38 Back-to-top (P3, "Long-page utility", basis=absent, drift
AGREES, all five probes negative). No pre-existing artefact was overwritten.

## 2 · Claim table (probeable token per claim, s182-D1)

| # | claim | probe | result |
|---|---|---|---|
| 1 | Leading-trim block is byte-identical to Command-palette line 36 | `grep -F "$(sed -n '36p' knowledge/snippets/Command-palette.reference.html)" knowledge/snippets/{Split-button,Fab,Back-to-top}.reference.html` | MATCH, all 3 |
| 2 | Zero raw `font-family`/`font-size` declarations (composites only) | `grep -nE "font-family\s*:|font-size\s*:" <file> \| grep -v -- "--"` | 0 hits, all 3 |
| 3 | `.t-cm-*`/`.t-ed-*` composites present | `grep -c "t-cm-\|t-ed-" <file>` | 19 / 6 / 7 |
| 4 | No `intent` field anywhere (W-58 parking honoured) | `grep -c '"intent"' <snippet> <meta>` | 0, all 6 files |
| 5 | Token-manifest addresses parse and use the SLASH grammar the store's own validator resolves (`button/primary/background/default`, not dotted) | `python3 knowledge/_validate_snippets.py <files>` | 0 findings on all 3 files, final run |
| 6 | 4px-grid gate (DEF-005) | `python3 knowledge/_validate_grid.py <files>` | `GRID GATE PASS — all layout dimensions on the 4px grid (3 file(s))` |
| 7 | a11y gate (target size, motion, ARIA vocabulary) | `python3 knowledge/_validate_a11y.py <files>` | `0 failure(s)` (repo-wide count including these 3, before/after fix: 2→0) |
| 8 | Type-composite gate | `python3 knowledge/_validate_type_composites.py <files>` | `TYPE GATE PASS` |
| 9 | Meta schema validity | `python3 -c "import json,jsonschema; jsonschema.validate(json.load(open(f)), json.load(open('knowledge/components/meta.schema.json')))"` for all 3 metas | VALID, all 3 |
| 10 | Render, both themes, headless Chromium, no console/page errors | `PYTHONPATH=/var/tmp/pylibs-s201 LD_LIBRARY_PATH=/var/tmp/chromelibs-s201/root/usr/lib/aarch64-linux-gnu PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-s197` + headless_shell, `data-theme` set to light/dark, `page.screenshot(full_page=True)` | 6/6 screenshots captured, `console_errors=[]` every run (light+dark x 3 components; split-button re-rendered twice after fixes, still clean) |

## 3 · What was driven

- All three snippets opened in a real headless-Chromium render (light AND dark), via the
  session's own Playwright/headless_shell toolchain — not just read as text. Zero console or
  page-script errors on any of the 6 renders. Screenshots live only in the sandbox scratch
  (`/var/tmp/rv209/*.png`) — not committed anywhere; this is a NEW-FILES-ONLY lane and
  screenshots are not a deliverable.
- The repo's own gates were driven directly against the 3 new files (read-only invocations,
  no registry writes): `_validate_grid.py` (DEF-005), `_validate_a11y.py`, `_validate_snippets.py`
  (token/contrast resolution against the live store), `_validate_type_composites.py`, and a
  `meta.schema.json` jsonschema validation. All are GREEN on the final state.
- **A real defect was caught and fixed mid-build, not just declared**: `_validate_a11y.py`
  first flagged `Split-button`'s tertiary-tier caret divider (a `::before` pseudo-element
  hack) as an under-24px hit-expander attempt — 2 FAILs. Rebuilt the divider as a plain
  `border-left`/`border-right` pair (no pseudo-element), re-ran the gate: 0 failures. Re-ran
  the grid gate and re-rendered the snippet afterward to confirm nothing else regressed.
- **A second real defect was caught and fixed**: the brief's "dotted grammar (`rag.success`,
  never `rag/success`)" instruction was initially applied to the snippets' own
  `#token-manifest` `vars`/`contrastPairs` blocks. Running `_validate_snippets.py` against the
  drafts surfaced ~20 `token 'X' not found in store'` + `contrast pair … unresolved` failures
  per file — the store's own address grammar (and every existing precedent: Button, Dropdown,
  Icon-button, Payment-card-visual) is SLASH-separated (`button/primary/background/default`).
  Cross-checked `knowledge/_validate_binds_resolve.py` (`address.split(".")`) and the existing
  `icon-button.meta.json`/`fab.meta.json` `props[].binds` arrays: the DOTTED grammar is real
  and correct, but it is the address form for a meta's `props[].binds` field specifically, not
  the snippet-level token-manifest. All three snippets' manifests were converted back to slash
  grammar (script-driven, whole-block JSON rewrite, then hand-verified); the meta `binds`
  arrays (`fab.meta.json`, `back-to-top.meta.json`) correctly kept dots throughout and needed
  no change. `_validate_snippets.py` now reports 0 findings on all three files.
- A third, smaller correction: `Split-button`'s `--item-hover` was initially mapped to
  `form/background/hover` in the manifest, which produced a `DRIFT` finding (`_validate_snippets.py`
  compares the CSS value against the store's resolved value for the claimed address — `#F3F3F3`/`#212121`
  vs the store's `#F0F0F0`/`#232323`). The hex values were copied byte-for-byte from
  `Dropdown.reference.html`'s own `.opt:hover`, which itself does NOT manifest `--item-hover`
  against the store (checked directly — Dropdown's own `#token-manifest` has no such entry).
  Rather than force a semantic address the copied value does not actually match, the entry was
  removed from the manifest and the `$note` documents the inherited-undocumented value and the
  DRIFT that caught it, so the gap is visible rather than silently mis-mapped.

## 4 · Design/fintech questions NAMED (never settled — every one lives verbatim in its meta's `$decisionsForDave`)

- **Split button** — should ArrowDown on the MAIN button also open the menu (a common APG
  variant), or only the caret (as built)? Should a menu item carry a leading icon? Are
  secondary/quaternary split-button tiers legitimate, or is the control reserved for
  primary/tertiary emphasis only? Is the primary-tier divider hairline (alpha.24 over the
  fill) visible enough, or should it bind a stronger existing token?
- **FAB** — should the FAB deviate from the angular corner rule and render circular (the way
  most systems that ship a FAB do)? Should a `fab/size` (56px) and a floating-chrome offset
  (24px) token be minted, or do 56/24 stand forever as house-standard raw constants? FAB vs
  Back-to-top collision — both are fixed bottom-right; which wins the corner, or do they
  stack? Is a non-primary-tier FAB ever legitimate?
- **Back-to-top** — the scroll-distance appearance threshold is entirely unspecified (the demo
  uses an arbitrary 200px `scrollTop` for illustration only, explicitly NOT a proposed
  default). Should the control become focus-reachable/visible on programmatic focus even below
  the threshold, so keyboard users are never stuck? Should Back-to-top always defer to a FAB
  present on the same screen? Is SECONDARY the single canonical tier?

None of these were defaulted, resolved, or silently picked — each is a NAMED open question in
the component's own meta, per the brief's return-contract item 4.

## 4b · Fence note for the conductor — gate write-by-default class

`_validate_a11y.py` and `_validate_snippets.py`, run against this lane's 3 files for
verification, do NOT scope their writes to the files passed as arguments — both scan every
snippet in `knowledge/snippets/` regardless and rewrite `knowledge/_A11Y-GATE.md` /
`knowledge/_SNIPPET-AUDIT.md` as a side effect (the repo's own known "write-by-default gate"
class, `_helpgate.py`'s `#158` note). That run also touched `knowledge/_graph-mark-observations.jsonl`
and `notes/_REHEARSAL-LOG.jsonl`. Because the brief fences this lane to NEW FILES ONLY / never
edit an existing file, all four were reverted to `HEAD` via `git show HEAD:<path> > <path>`
(the mount's own working-revert method — `git checkout` is unusable here) immediately after
verification, before writing this receipt. `git status --short` is clean of anything but new
files as of this receipt. Flagging for the conductor because Lane A/B's own gate runs (their
untracked deliverables are visible alongside mine in this shared checkout) will trip the same
class — the SAME four files will need the same treatment, or a single deliberate regenerate
pass, before the conductor's serial gate run and single commit.

## 5 · What stays UNPROVEN

- **No pixel-diff or human eye-check was performed on the 6 screenshots.** The render-verify
  claim (item 10 above) proves the DOM loaded, the theme attribute applied, and the page
  executed without script errors in a real browser — it does NOT prove correct visual
  layout, contrast, or spacing by inspection. That is Dave's-eye / reviewer's job, named here
  rather than silently assumed.
- **Contrast ratios were NOT independently re-measured** (no `_contrast_utils.contrast_ratio`
  pass was run against the DOM, unlike Payment-card-visual's #204 build, which measured its
  chip-dot pairs by hand). The `contrastPairs` declared in each manifest are inherited/copied
  claims from Button/Dropdown/Icon-button's own gated pairs, not independently re-measured
  in this session.
- **`_validate_state_contrast.py`, `_validate_radius.py`, `_validate_icons.py`,
  `_validate_coverage.py`, and every `--check` generator are NOT run by this lane** — they are
  the conductor's serial set per the brief. Not registered in `component-types.json`, not in
  `_validate_radius.MIGRATED_SNIPPETS`, no `.cn-*` scope exists in `canon.css` for any of the
  three — all declared, not silently assumed done.
- **Back-to-top's live scroll-threshold demo was NOT driven interactively by an automated
  probe** (no scripted `scrollTop` simulation + re-screenshot of the appear/disappear
  transition) — only the static hidden/visible specimen rows and the DOM-load render were
  verified. The scroll-listener JS is present and was exercised by hand-reading the code, not
  by a scripted interaction test.
- **Split-button's keyboard wiring (Arrow/Enter/Escape/click-away) was NOT driven by a
  scripted keyboard-interaction test** — only code-read and the static "open" specimen row
  were used to verify the flyout renders correctly; the JS event wiring itself was not
  exercised end-to-end in the browser.
- **FAB's 56px target and 24px offset, and Back-to-top's 24px offset, are DECLARED raw
  constants, not store tokens** — flagged in-file and in the meta as open to Dave, not
  resolved by this lane (no token was minted, per the DO-NOT-RULE list).
