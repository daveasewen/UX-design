# #218 build brief — Foundations "Grids" group: four pages, controls kept

**Ruled by Dave in chat, #218 (2026-08-24), his words:** *"I think I'd like this added to the
library under foundations, we should have a section called grids with subsections – the 12 col
grid and these 3 types, I'd like to keep the controls so the designer can use them."* Structure
option-selected by Dave: **four separate pages under a Grids group** (not one page with sections).
Scope rider, same sitting: the #218 corner-keyline rule is **dashboard-only** for now.

## The deliverable

Foundations tier gains a **Grids group** of four generated pages:

1. `showroom/_foundations/grids-12col.html` — **The 12-column grid.** Renders the RULED tokens
   `layout/web` + `layout/app` (12 columns; margins/gutters per scale-1/2/3; breakpoint doc
   preserved in the store's $description). Live column overlay built on canon's own `.l-cols` /
   `.l-span-*` utilities — never a re-drawn grid. A scale/viewport switch is a VIEW control;
   nothing on this page tunes a token.
2. `grids-display.html` · 3. `grids-gallery.html` · 4. `grids-dashboard.html` — one page per
   bento type, each carrying **that type's full working controls** exactly as the matrix explorer
   ships them (spacing, keylines where legal per theme, backgrounds, gallery mode + rounding
   dials, dashboard sub-spacing snapping slider, export). The dashboard page carries the #218
   corner-keyline construction (per-band minted corner rules).

**ONE DATA PATH / ONE MATHS:** all bento content, spans, packing and corner rules come from
`knowledge/_render/gen_bento_matrix_217.py`'s modules (`read_photos` path via
`gen_bento_roles_217`, `pack_rows` via `gen_gallery_compare_217`, `corner_rules`,
`square_nested_wall`) — never a second copy. All four pages are written through
`knowledge/_render/gen_foundations_217.py` (ONE writer, ONE shell).

**Library wiring:** `gen_library_214.py` FOUNDATIONS gains minimal GROUP support — a `group:
"Grids"` field and grouped rendering in the tier nav + `showroom/index.html` + `index.json` +
one thumbnail per new page via the ruled thumbs generator. Keep the mechanism as small as the
need: a group label over four entries, not a general nesting system (the library IA v2 word-set
is still Dave's open ruling, W-99zg — do not pre-empt it).

## What stays untouched

- `showroom/_foundations/bento.html` (the matrix explorer) — LIVE decision surface for
  s217-D5 P1–P5 (row W-126). **The PROPOSED controls and proposal notes stay ONLY there**; the
  new type pages carry ruled behaviour + working dials, no PROPOSED surface.
- Photography and Logos entries — unchanged.

## DO-NOT-RULE (fence)

No `knowledge/_rulings.json` writes. No token mints, no `canon.css` / `gen_canon_bento.py`
edits. No closing, moving or restating of s217-D5's five open points. No edits to the explorer
page or its generator's PROPOSED surfaces (**consuming its modules is in scope; changing them is
not** — if a module needs a change to be consumable, STOP and return the finding). No lane,
worklist, GM/LS or memory edits. No commit, no push. Regions owned: `gen_foundations_217.py`,
`gen_library_214.py` (FOUNDATIONS + nav render only), new page bodies, new/extended verify
scripts, `showroom/index.*`, `showroom/_thumbs/` for the new pages.

## Proof (bounded, s172-D3 — targeted, depth 1)

- Each new page driven in all 8 theme×mode states: renders, controls drive, fonts asserted
  against two controls, zero dangling properties over the canon property sweep.
- Dashboard page: corner assertions from rendered positions (the #218 clause), gutters empty
  above 1px, 1px handover.
- 12-col page: overlay column count == the token's 12 at desktop; margins/gutters read back off
  the live document against the STORE values, never typed.
- Library: nav group renders, four entries present, index.json round-trips, thumbnails exist.
- One mutation arm on the new surface: nav grouping stripped ⇒ the group assertion goes red by
  name. Reuse `BM_MUTANT_DIR` for any mutant artefacts.

## Pitfalls, replayed (Dave #165 — mandatory reading)

- **/var/tmp is SHARED across sessions**: foreign artefacts are unwritable and STALE. Session
  paths: fonts `/var/tmp/fonts-s218.conf` (+ `/var/tmp/fonts-s218/` symlinks into THIS mount),
  mutants via `BM_MUTANT_DIR`. A stale mutant silently proves yesterday's clause (#218 measured).
- **45s call kill**: chunk browser drives; nothing survives a tool-call boundary.
- **`set_content()` is BANNED in render-proofs** — `goto("file://…")` only.
- **Foreign `var()` needs a literal fallback** — the page selftest's silent-black gate bites.
- **Band literals are COMPILED, not var()-read** — @container cannot read a custom property.
- **A probe proves the clause it was written for** — new assertions must be seen RED on a
  mutant before they count (drive the arm, don't just write it).
- **Thumbnails predate their pages if not re-shot** (#217 residual class).
- Render env recipe that works at this seat: `PYTHONPATH=/var/tmp/pylibs`
  `PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-215`
  `LD_LIBRARY_PATH=/var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu`
  `FONTCONFIG_FILE=/var/tmp/fonts-s218.conf` `TMPDIR=/var/tmp`.

## Return

Files changed (path list), probe output tails (green + the arm red by name), residuals PRICED
not smoothed, and any finding that wanted to cross the fence — named, not enacted.
