# #264 — wrap brief (cut by the Fable conductor at 214,299 real FILL, 2026-09-09 20:30)

**Session:** `Apollo - #264: the stat card arrow seat, /goal and the sidebar chart glyph` · 2026-09-09, one evening (19:26 → 20:30), conductor **Fable**, no subs until this wrap sub (Opus). **No date split.**

## What happened, in order
1. **Stat card arrow seat — NOT open, my error.** Dave: "I thought this was ruled". The P-01 card he ACCEPTed at #263 says verbatim "Stat card moves with it, always." ⇒ `s263-D1` already covers `Stat-card.reference.html` (its `governs` names it). The #263 wrap re-opened a closed item and the #264 opener repeated it. **STRIKE the carry**; no ruling owed.
2. **Sidebar glyph — the "hand-baked" carry was FALSE.** All 12 `<symbol>`s in `Sidebar-nav.reference.html` are byte-identical to `assets/icons/` files (path-data match). The defect was PAIRING: Spending rested on `data-chart` and went current on `insight-active` (a bulb); Transfers rested on `balance-transfer` (no twin exists) and went current on `transfer-active`. Review page `notes/_REVIEW-264-sidebar-glyph.html` (generator `notes/_lanes/264-glyph-build.py`), driven in Chromium.
3. **`s264-D1`** Dave "Spending A" → `data-chart`/`data-chart-active`. **`s264-D2`** Dave "Transfer D" → `transfer`/`transfer-active`. Commit `9bfacb9`.
4. Dave "1. okay fix them 2. do it": four app-shell/palette snippets (`App-shell-side-nav`, `-nav-rail`, `-multi-column`, `Command-palette`) `balance-transfer`→`transfer` at rest; **TWIN ARM** added to `knowledge/_validate_icons.py` (every `.ic-line`/`.ic-fill` pair resolved to library slugs; fill must be line's `-active` / `-active-badge`; MIS-TWINNED is BLOCKING; line with no twin in library = reported not failed); bite-test `twin` (`mut_mistwinned_icon`) registered in `knowledge/_tests/test_gates.py` and driven RED→GREEN in-process (one 93 MB copy). Found a THIRD case: Tab-bar Insights row had `insight` in BOTH slots → `ic-insight-a` = `insight-active` added (`s262-D3`). Commit `3d7def7`.
5. **Experiment (Dave: "go, lets see whatcha got")**: `-active` glyph derived from line glyph by Skia path ops — S = silhouette (contours filled+unioned), B = S − erode(S,1.25), I = L − B, A1 = S − I, A2 = S − silhouette(I). Calibrated on 10 human pairs (7 within tolerance; card/alert/insight are designer EDITS no rule recovers; settings needs A2). 13 orphans on `notes/_REVIEW-264-active-glyphs.html` (`264-active-gen.py`, `264-active-page.py`). Commit `3722f26`.
6. **`s264-D3`** Dave graded: 8 A1 ACCEPT (cheque, finances, document-report, newspaper, device-mobile, online-banking, presentation, add-circle) → ENTERED THE LIBRARY as `<slug>-active.svg` with `$derived` annotation in `icons.manifest.json` (textual insertion; `$counts` + `$total` 658→666; icon gate 750→758 glyphs, still 5 Legend UNKNOWN pre-existing). 5 "neither" with his reasons verbatim in the ruling (balance-transfer, tax, workspace, digital-statements, global-money) = ONE CLASS: two-body icons with overlap exclusion. Commit `c7247c2`.
7. **Second pass** (Dave: "have another go"): `264-active-gen2.py` — silhouette = holes of the EXTERIOR of (L ∪ grow(frontSil, gap 1.0)); fronts = rings whose sealing GAINS area (>3px², raster-counted at 16× for classification only); open bodies morphologically closed. balance-transfer, tax, workspace, digital-statements now fill; **global-money is ONE connected ink piece** (arrows touch meridians) — no second body to find, still rejected. Page `notes/_REVIEW-264-active-glyphs-2.html`. Commit `5e97c90`. Dave: "no time for this now, but we can return to it another time because we are getting somewhere" → four stay UNGRADED, nothing more in library; `s264-D3` evidence AMENDED with that sentence (`--amend-evidence`).
8. Dave: "wrap".

## Rulings this session
`s264-D1`, `s264-D2`, `s264-D3` — rulings store 436 → 439 (`_inscribe_ruling.py`, reconstruction proof passed each time). All `by` Dave, `date` 2026-09-09.

## Commits (5, all local, 0 pushed — PUSH IS PART OF THIS WRAP)
`9bfacb9` · `3d7def7` · `3722f26` · `c7247c2` · `5e97c90` (+ the amend is uncommitted — commit it in the wrap).

## Carries → #265 (POINTER + count in the banner, list in `_CARRIES.md` per s225-D2)
- **`/goal` bite-test** — ruled item 1 at the opener ("do it"), NOT STARTED; first item of #265.
- **global-money** active glyph — one connected component; drawing, not deriving.
- **Four ungraded** on `_REVIEW-264-active-glyphs-2.html` (balance-transfer, tax, workspace, digital-statements) — Dave grades when we return.
- `test_gates.py` FULL suite still unrun on this disk (only `icon` + `twin` cases driven in-process).
- Pre-existing reds unchanged: 5 Legend UNKNOWN icons; footer schema reds; `_build_integrity.py`.
- STRUCK: "Stat card arrow seat" (ruled at s263-D1 via P-01's text) · "sidebar chart glyph hand-baked" (false — was mis-twinned, fixed s264-D1/D2).
- Ruling-shaped, Dave's, NOT ruled: whether a gate report should be refused at commit when its tree ≠ HEAD (#263 carry) · #241 midnight-wrap question (age 22).

## Gauge (measured, `_checkin.py` at 20:29)
FILL **214,299 real** (peak, 96 turns) — OVER the `s260-D2` delegated stop line 180,000 and the 200K working ceiling ⇒ this wrap is DELEGATED. Boot **69,955 real** measured at the opener (tiktoken installed at opener — NO hole this session; 45 under the 70,000 ceiling; the standing breach is #255's 70,127). Throughput 612,089 cl100k-estimate. Subs: this wrap sub only.

## Declared skips (declare-last, each with size)
No `_build_all.py` · `_validate_screen.py` not run · full `test_gates.py` not run (disk 89%, 93 MB/copy) · `notes/_PROPOSED-263.html` still never driven · `_CARRIES.md` never read whole (10.6 MB) · no retrieval query · no recall plant · Artifact publish not attempted (refused in Cowork at #263; file is the surface).

## Sandbox notes for the ledger
Chromium per `chromium-in-sandbox-recipe` (playwright + `libXdamage.so.1`, no root) — full `chromium-1234` build DELETED to save disk, headless shell kept. Skia (`skia-python`) needed `libEGL`/`libGL`/`libglvnd`/`libGLX`/`libOpenGL` extracted the same way into `~/.local/lib`. A stale `.git/index.lock` (19:25) blocked the first commit; the mount refused deletion until the folder's delete permission was granted; lock MOVED to `~/orphan-locks/`, not deleted.

## DO-NOT-RULE (the sub does not decide these)
Anything in "Ruling-shaped, Dave's" above · whether derived glyphs are release-blocking · whether the four ungraded enter the library · grade of any glyph.
