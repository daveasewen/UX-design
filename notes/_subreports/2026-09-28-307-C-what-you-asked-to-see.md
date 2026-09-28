# #307 lane C — the review page for what Dave asked to see

Page: `notes/_REVIEW-307-what-you-asked-to-see-2026-09-28-v1.html` (86,367 B, sha256 `b70a4de9…74edd`). Started from a copy of `notes/_REVIEW-305-call-27-visuals-2026-09-27-v1.html`: its house CSS, the "All review pages" back link, the Your-decisions bar (Copy as text / Save as file / Clear) and the lightbox. Changed only what the content needed: option buttons per call (`data-options` / `data-rec`, the recommended one tagged), the export lists every call (its recommendation, the choice, "the recommendation" or "not the recommendation", his words, his comment), "Export rulings .md" was relabelled "Save as file" as on the #307 sitting page, and the drop folder is now 307. There are 14 calls and a whole-page note. Section 6 is a marked placeholder carrying `<!-- COLDRUN-SLOT -->` with no decision box, so the conductor can add one if the result needs it. Nothing inscribed, no git write, no memory, nothing published, no existing file edited.

## Per item: what was rendered, the recommendation, and what could not be shown

1. **Dark caption, four themes (W-307qi from W-208).** Rendered the "Capsule — Dark grey" card on `showroom/_foundations/bento-rails.html` (canon plus the generated CAPTION_GROUND_MINTS block) in every theme, dark and light, using the page's own switch (html theme, body mode). Measured: mono, legacy and console #313131 on #1A1A1A, ΔL* +11.06, white text 13.01:1; supercharge #312C26, ΔL* +9.08, 12.80:1. Light is unchanged. These match s220-D1's figures. **Recommendation: close it.** FINDING: the card carries its own `data-apollo-theme` (console-scoped). Left on under a dark body, a card-level theme attribute re-declares that theme's LIGHT page ground: supercharge measured #F7F6F4 behind the dark card. The driver takes the attribute off. The page is not affected today, because the card is console, but any card given a supercharge scope would show the fault.
2. **Tree mark and the ring (W-307qr from W-72).** Rendered from the Calendar, Date-picker, Tree and Sidebar-nav reference files, light and dark. The calendar cells are at 4×, and each is clipped with its own page ground around it (neighbouring cells hidden for the shot). The date picker is shown open on today (28/09/2026, typed in, then focus blurred and the panel asserted still open). The tree uses a black bar (white in dark) plus a grey ground. The navigation uses a red bar, #DB0011. **Recommendation 2a: keep the tree's mark black.** FINDING: the #211 repair (the ring drawn in the page colour) measures 17.40:1 against the fill, but the ring touches the page, so it cannot be seen as a ring. A today-and-chosen day looks like a chosen day 2px smaller all round. The "before" cell (black ring on black) and a **one-rule proposal** (`box-shadow: inset 0 0 0 3px var(--text), inset 0 0 0 5px var(--page)`) are rendered as mutations on the real part. The proposal is NOT canon. **Recommendation 2b: set the ring inside the square.**
3. **The other eight wave-3 parts (W-307qu from W-63).** Each reference snippet rendered at 960 wide, 2×, light and dark, trimmed to its content. The mandate row is cropped to its first specimen. Recommendations, one each:
   - Mandate row: rework as a list-items variant.
   - Limits meter: close, as it is already Meter (s210-D1/D5).
   - Range slider: rework as Slider's two-handle form.
   - Rating: delete.
   - Transfer list: rework, then promote.
   - Split button: promote.
   - FAB: rework, then promote.
   - Back to top: rework the reference page, then promote.

   Three faults were found by looking and are measured:
   - Rating's aggregate row puts the filled stars over the empty ones out of step (4× close-up).
   - Transfer list: the `ic-chev-rr` / `ic-chev-ll` symbols carry one path of the two-path library glyph, so "move all" looks like "move one" (4× close-up). Its select-all box also sits above its label.
   - Back to top: the demo frame's computed font is "Times New Roman", and a note shows a missing-glyph box.

   The FAB's "three stray body rules" is quoted from lane B's W-307qy and was not re-measured here.
4. **"Five parts not built" (W-307qw from W-151).** The premise of the card is wrong, and the page says so. `notes/_receipts/2026-08-25-wave3-alpha.md` built zero of EIGHT because all eight already existed. Its "five" were five decisions. Shown: the eight form parts as thumbnails (reference files, 1×), and the five questions with where each stands now:
   - Q1: never answered.
   - Q2: the logo, s282-D3.
   - Q3: the column renamed `itinerary_status_2026_07_14_FROZEN` (v4 register, commit 941c92d7).
   - Q4: File-upload aria-invalid fixed in 941c92d7; measured 1 at rest tonight.
   - Q5: lanes β and γ stopped (their receipts).

   **Recommendation: close it.**
5. **The third red and the 29 forks (W-229).** Rendered the error state of `showroom/input-fields.html` and `showroom/notifications.html` in four themes, light and dark, by clicking the pages' own buttons. Measured the reds painted:
   - Mono field: #F6604C in both modes.
   - Mono message box: #A8000B.
   - Legacy: #A8000B.
   - Console and supercharge: #B92F1E.

   So the third red shows on one mono page. Also for Dave's eye: the mono field on white paints the light red, where s151-D1 puts the dark red on white. Forks: `knowledge/_validate_token_forks.py --strict --json` was re-run into this lane's folder, with the ledger md5 unchanged either side. #221's rule was re-applied by `classify_forks.py`, giving A 24 and A2 6. These are #221's 29 plus a "common" twin of legacy's `--ink`. All are still UNRULED-BASELINE except `--panel`, declared at s215. The four declared at s305-D41 (`--status-positive/negative/neutral`, `--cell-py`) are NOT among the 29. **Recommendations: 5a, fold the third red into mono's error red (legacy keeps its own); 5b, hand the 29 to Claude and bring back only real colour choices.**
6. **Fresh-session dashboard run:** placeholder only, `<!-- COLDRUN-SLOT -->` at line 458.

## Verify receipts (`notes/_lanes/307/C/verify/verify-receipt.json`, driver `verify_page.py`)

- 1440 light, 390 light, 1440 dark: 66 of 66 images load (naturalWidth > 0). The 67th `img` is the lightbox's, which has no src until it is opened. No console errors, no failed requests, no sideways scroll (scrollWidth equals viewport), no element past the right edge.
- Copy as text, with the clipboard stubbed by an init script: every recommended button was clicked and two notes were typed. The copied text is 10,495 characters and carries all 14 call titles (0 missing), 14 "Chose" lines all marked "the recommendation", both notes, and "15 of 15 answered". Saved at `verify/copied-text-1440.md`.
- Looked at by eye, section by section, at 1440 light and dark and at 390. Fixed along the way:
  - The chips had been uppercased by the overlay CSS.
  - `.shot` widths were overriding the real-size width attributes.
  - The four-across grids had shrunk real parts, so they are now two-across.
  - A class clash (`.pair`) broke the fork table.
  - The transfer-list close-up was cropped too loose.
  - The date picker's focus outline covered the ring.
  - At 390 the table column was too narrow.

  No descender clipping was seen in any shot. The tree label measured 21 of 21px.

## Unproven or declared

- The ring proposal is one rule rendered as a mutation, and nothing puts it in canon.
- The FAB repair is taken from lane B's row text.
- "Mono can pick the chord from tonight" rests on lane B's W-99zr → W-307qh reading.
- The legacy-owns-#A8000B reading rests on canon's Notifications comment ("legitimate Legacy hexes").

## Paths written (all new)

- `notes/_REVIEW-307-what-you-asked-to-see-2026-09-28-v1.html`
- `notes/_subreports/2026-09-28-307-C-what-you-asked-to-see.md`
- `notes/_lanes/307/C/`:
  - `_lib.py`, `shots_1_captions.py`, `shots_2_tree_ring.py`, `shots_3_wave3.py`, `shots_4_formparts.py`, `shots_5_reds.py`, `classify_forks.py`, `build_page.py`, `verify_page.py`, `_sheet.py`
  - `forks-strict-now.json`
  - `shots/` (PNGs and measure JSONs)
  - `verify/` (section screenshots, receipt, copied text)
- Scratch, left because deletion is off at this seat: `notes/_lanes/307/C/_r305-stripped.html`, `_check/` (contact sheets, `v/`, `v2/`, `v3/`, `old-verify/`, `verify_page.py.bak`). None of it is referenced by the page, and it can be dropped.
