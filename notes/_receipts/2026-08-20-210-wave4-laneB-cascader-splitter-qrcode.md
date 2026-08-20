# Receipt — #210 Wave 4 · Lane B · cascader · splitter · qr-code

**Lane:** B (Opus) · **Session:** #210 · **Date:** 2026-08-20
**Brief:** `notes/_briefs/2026-08-20-210-wave4-heavy7-fanout-brief-v1.md` (THE JOB, Lane B)
**Members:** cascader · splitter · qr-code
**Store row for this receipt:** `W-73`

> ⛔ **NOTHING IN THIS RECEIPT IS A RULING.** Every design call below is PROPOSED and is Dave's
> (the Kpi-tile precedent, `s182-D2`). No registry, `MIGRATED_SNIPPETS`, `CATEGORIES`, spine,
> `canon.css`, `_rulings.json` or git operation was touched. This lane created NEW FILES ONLY,
> plus the one `_state.json` doc-row the return contract requires.

---

## 0 · THE HEADLINE: THE QR FENCE HELD, AND IT PAID FOR ITSELF TWICE

The brief's hardest fence was qr-code: *a real encoding or a loud refusal — a plausible fake is
the worst outcome.* **No refusal was needed.** Two independent things were done, in this order:

1. **An ISO/IEC 18004 byte-mode encoder was written for this lane** (Reed–Solomon over GF(256),
   the four masking penalty rules, BCH(15,5) format information) and every matrix it emits is
   **decode-verified before the snippet is written** — the build script refuses to emit a symbol
   that does not read back as its own stated payload.
2. **The rendered artefact was then decoded again** — screenshots of what Chromium actually
   painted, fed back to OpenCV 5.0.0's `QRCodeDetector`. That is the assertion that matters:
   not "the matrix came out of an encoder" but "what is on the page scans."

And step 2 answered a design question that would otherwise have been settled by assertion:

> ⛔ **IN DARK MODE, THE THEME-FOLLOWING VARIANT DOES NOT DECODE.** Five of six sampled specimens
> decoded in dark; the inverted one returned an **empty string**. Invert those same pixels back
> to dark-on-light and the identical image decodes perfectly — so the content is intact and it is
> the **polarity** that defeats the reader. One decoder is not every decoder, and plenty of phone
> cameras read inverted symbols. But this is a real reader failing a real render, and it turns
> "should a QR code invert in dark mode?" from a taste question into a priced one. **Still Dave's.**

★ **The encoder was WRONG TWICE before it was right, and both bugs were caught by decoding, not
by reading the code.** The format-information copies were placed LSB-first where the standard
places one of them MSB-first. The matrix looked completely convincing at every stage. **A QR code
is the purest case of the #202 defect class there is: it is unreviewable by eye, so the only
honest verification is a decode.**

---

## 1 · FILE LIST — six new files, plus this receipt

| # | path | bytes |
|---|---|---|
| 1 | `knowledge/snippets/Cascader.reference.html` | 37,974 |
| 2 | `knowledge/components/cascader.meta.json` | 11,937 |
| 3 | `knowledge/snippets/Splitter.reference.html` | 25,292 |
| 4 | `knowledge/components/splitter.meta.json` | 11,266 |
| 5 | `knowledge/snippets/Qr-code.reference.html` | 40,093 |
| 6 | `knowledge/components/qr-code.meta.json` | 10,800 |
| 7 | `notes/_receipts/2026-08-20-210-wave4-laneB-cascader-splitter-qrcode.md` | this file |

**No existing file was hand-edited.** Working artefacts live OUTSIDE the repo
(`NON-REPO: the session outputs folder` — `qr_encoder.py`, `gen_qr_snippet.py`,
`qr_snippet_template.html`, `drive_cascader.py`, `drive_splitter.py`, `drive_qr.py`,
`laneB-renders/*.png`) per `s191-D2` home-or-declare. They are tools and evidence, not
deliverables. ⚠ `Qr-code.reference.html` is GENERATED from `qr_snippet_template.html` by
`gen_qr_snippet.py`; the generator is non-repo, so **the snippet is the artefact and the
generator is a working note** — if Dave wants the QR component to be regenerable in-repo, that
generator needs a home and a store row, and that is a decision (Q-QR-6 below).

---

## 2 · CLAIM TABLE — every claim carries a probeable token (`s182-D1`)

| # | claim | probe — re-runnable, exactly as written | verdict |
|---|---|---|---|
| 1 | All three components were ABSENT before this lane | `ls knowledge/snippets/ \| grep -icE 'cascad\|qr'` → **0** at build; `ls knowledge/snippets/ \| grep -iE 'split'` → **only `Split-button.reference.html`**; `grep -rl 'role="separator"' knowledge/snippets/` → **0** | ✅ |
| 2 | ⚠ Split-button is a DIFFERENT component and was not touched | `git status --short knowledge/snippets/Split-button.reference.html` → **no output** (unmodified). ⚠ FALSE-PROBE WARNING: `grep -ril split knowledge/snippets/` returns both files and proves nothing — the name is the collision, so the probe must be on the FILE STATE, not the string | ✅ |
| 3 | The leading-trim block is the CURRENT one, byte-identical to `Command-palette.reference.html` line 36 | `python3 -c "cp=open('knowledge/snippets/Command-palette.reference.html').read().split(chr(10))[35]; print(all(cp in open(f).read() for f in ['knowledge/snippets/Cascader.reference.html','knowledge/snippets/Splitter.reference.html','knowledge/snippets/Qr-code.reference.html']))"` → **True** (328 chars, identical) | ✅ |
| 4 | 4px-grid gate clean, whole repo | `python3 knowledge/_validate_grid.py` → *"GRID GATE PASS — all layout dimensions on the 4px grid (124 file(s))."* | ✅ |
| 5 | Snippet/token gate clean, whole repo | `python3 knowledge/_validate_snippets.py` → *"snippet gate: 108 snippet(s), 0 failure(s)"* | ✅ |
| 6 | Descender-clip gate clean | `python3 knowledge/_validate_descender_clip.py` → *"DESCENDER-CLIP GATE PASS — every truncating label is descender-safe (124 file(s))."* | ✅ **but see claim 20 — this gate CANNOT see the cascade** |
| 7 | Type-composite debt: these three files add **ZERO** | `python3 knowledge/_validate_type_composites.py knowledge/snippets/Cascader.reference.html knowledge/snippets/Splitter.reference.html knowledge/snippets/Qr-code.reference.html` → *"TYPE GATE PASS — all component text bound to canon composites (3 file(s))."* | ✅ |
| 8 | The repo figure moved 1,097 → **1,099** and NEITHER is this lane's | `python3 knowledge/_validate_type_composites.py` → *"TYPE GATE FAIL — 1099 violation(s)"*; attributed: `python3 knowledge/_validate_type_composites.py knowledge/snippets/Carousel.reference.html` → **1 violation**, same for `Image-block.reference.html` → **1**. Lane C's two, named so they are not charged to the wave at large | ✅ **attributed** |
| 9 | The three metas are schema-valid | `python3 knowledge/_probe_registry/probe_meta_schema.py --check` → *"109 meta(s) checked · 0 finding(s) · 1 exempt failure(s)"* → *"PROBE P-1 — findings=0"* | ✅ |
| 10 | No duplicate ids introduced | `python3 knowledge/_probe_registry/probe_dup_ids.py --check` → *"PROBE P-2 — findings=0"* | ✅ |
| 11 | Every manifest var resolves; the ONLY failures are check-D canon blocks | `python3 knowledge/_validate_binds_resolve.py` → *"binds-resolve gate: 108 snippets (108 with manifests, 1417 vars) · 108 metas (116 binds addresses) · 101/108 canon blocks · 7 failure(s)"* — **0 var failures**; the 7 are `no .cn-<name> block in canon.css` for Calendar, Carousel, **Cascader**, Image-block, **Qr-code**, **Splitter**, Tree | ⛔ **CONDUCTOR'S** (3 of the 7 are this lane's) |
| 12 | a11y gate: the only failure in the repo is Lane A's, not this lane's | `python3 knowledge/_validate_a11y.py \| grep -c -iE 'cascader\|splitter\|qr-code'` → **0**; the single FAIL line names **`Tree`** (`unknown ARIA role(s) ['tree','treeitem']`) | ✅ |
| 13 | The icon audit no longer carries an UNKNOWN for this lane | `python3 knowledge/_validate_icons.py \| head -6` → *"15 UNKNOWN … still UNKNOWN: 11 Carousel · 4 Image-block"* — **Qr-code is gone** (it was 1 UNKNOWN until the sprite was marked `data-bespoke` with a statement that it is computed geometry, not a glyph) | ✅ |
| 14 | No glyph was drawn in Cascader — the chevron is copied byte-for-byte from gated Multi-select | `diff <(grep -o 'd="M17 4.15198[^"]*"' knowledge/snippets/Cascader.reference.html \| head -1) <(grep -o 'd="M17 4.15198[^"]*"' knowledge/snippets/Multi-select.reference.html \| head -1)` → **identical** | ✅ |
| 15 | ⚠ Splitter's grip IS bespoke, and the library really has no glyph for it | `ls knowledge/assets/icons/*/ \| grep -icE 'grip\|drag\|handle\|resize'` → **0**. It is three 4px `<rect>`s marked `data-bespoke` at its use site. An `_ICON-GAPS.md` entry may be owed — that file is the conductor's | ✅ **declared** |
| 16 | Every QR matrix is a REAL encoding, verified before the file was written | `cd <outputs> && python3 gen_qr_snippet.py` → *"decode-verified A: version 2, mask 6, 25 modules -> 'https://www.hsbc.co.uk/'"* · *"decode-verified B: version 3, mask 2, 29 modules -> 'Pay 250.00 GBP to Acme Ltd ref INV-2291'"*. The generator raises `SystemExit("REFUSED: …")` rather than write an unverified symbol | ✅ **DRIVEN** |
| 17 | And the RENDERED artefact decodes — in a browser, from pixels | headless Chromium element screenshots → OpenCV 5.0.0 `QRCodeDetector`. **LIGHT: 6 of 6** decoded to their stated payload (`265×264`, `133×132`, `397×397`, fixed-plate, theme-following, `297×297` v3). **DARK: 5 of 6** | ✅ **DRIVEN** |
| 18 | ⛔ The theme-following variant does NOT decode in dark, and the failure is polarity | same run: `dark → qr-follows-theme → decoded=''`; the same PNG bit-inverted → `'https://www.hsbc.co.uk/'` | ⛔ **MEASURED — Dave's** |
| 19 | The matrix is drawn as SVG `<rect>`s at true module coordinates, once each | in-page: `document.querySelectorAll('#qr-symbol-a rect').length` → **169**, `#qr-symbol-b rect` → **214**, `.qr use` → **9**. Horizontal runs are merged, so 169 rects paint the symbol's 25×25 grid plus its plate; nine specimens share two symbols, so no two specimens can drift apart | ✅ |
| 20 | ⛔ **THE ds-005 OVERRIDE NEEDS TWO CLASSES, AND SIX GATED SNIPPETS ARE CURRENTLY LOSING** | in-browser `getComputedStyle(el).textBoxEdge`: `Document-row .dr-title` → **`cap alphabetic`** · `.dr-meta` → **`cap alphabetic`** · `Sidebar-nav .sn-label` → **`cap alphabetic`** · `Timeline .tl-title` → **`cap alphabetic`** · `Transaction-row .ldg-name` → **`cap alphabetic`** · `Standing-order-mandate-row .mr-payee` → **`cap alphabetic`**. This lane's two, after raising the selector: **`text`**, **`text`** | ⛔ **CONDUCTOR'S — see §5** |
| 21 | Splitter: the keyboard step is exactly what the file declares | driven: **545 → 561 (+16) → 625 (+64 shift) → 609 (−16)** px, published `aria-valuenow` 50 → 51 → 57 → 56 | ✅ **DRIVEN** |
| 22 | Splitter: the POINTER and the KEYBOARD reach the SAME two fences | keyboard `Home` → **160px**; drag hard past the left edge → **160px**. Keyboard `End` → **930px** with the secondary at **160px**; drag hard past the right edge → **930px**, secondary **160px** | ✅ **DRIVEN** |
| 23 | Splitter: collapse is reversible and the separator survives it | `Enter` → `aria-valuenow=0`, primary **0px**, `data-collapsed="true"`, divider still **8px** wide; `Enter` again → **545px**, the pre-collapse size (`restore_equals_pre_collapse` → **true**) | ✅ **DRIVEN** |
| 24 | Splitter: the fixed variant is a separator WITHOUT a tab stop | driven: `{role:"separator", aria-disabled:"true", tabindex:null, cursor:"not-allowed"}`; a whole-page focusable sweep returns exactly **two** items: *"separator:Resize the Accounts pane"*, *"separator:Resize the Filters pane"* | ✅ **DRIVEN** |
| 25 | Splitter: the divider's drawn rule is 8px and its pointer target is 24px, both axes | driven: `--div` **8px**, `.sp-div` rect **8px** wide; `::before` **24px × 100%** horizontally and **100% × 24px** vertically. Independently confirmed by the hit-area advisory: `div.sp-div` **24 × 278** and **1098 × 24** | ✅ **DRIVEN** |
| 26 | ⚠ And that 24px is UNDER the 44px target — flagged, not hidden | `python3 knowledge/_validate_hit_area.py knowledge/snippets/{Cascader,Splitter,Qr-code}.reference.html` (playwright staged) → *"ADVISORY: 26 target(s) measured, 4 finding(s), 6 exempt"*, all four `Splitter … 24 × … UNDER −20px`. **Cascader: 22 targets, 0 findings** (`li#cs1-l0-o1` **220 × 44**) | ⚠ **ADVISORY — Dave's** |
| 27 | ⛔ Splitter had a real defect: a zero-width container destroyed the user's split | instrumented in-browser during a full-page capture: `win:resize (1,1,0)` → `aria-valuenow` **0** → restore → `aria-valuenow` **85**. A 50/50 split became 85/15 with nobody touching it. **FIXED** — the component now keeps the RATIO. Re-measured after the fix: 1180px viewport **50% / 545px**; narrow to 480px → still **50%**, now 215px (it used to become 63% / 270px) | ✅ **FOUND BY DRIVING, FIXED** |
| 28 | ⛔ Cascader had a real defect: a committed cascader re-opened EMPTY in the stacked layout | `showLevel(path.length)` with `path.length === cols.length` marked NO column current; in the container-query layout every column is `display:none`. **FIXED** with a clamp. Driven after: at a 380px container, `cq_cols_visible_at_open` → **1**, back row `display` → **flex**, label → *"Back to Region"* | ✅ **FOUND BY DRIVING, FIXED** |
| 29 | Cascader: the cascade actually cascades, and stale columns are cleared | driven: choose *United Kingdom* → column 2 = **["England","Scotland","Wales"]**, column 3 `hidden` **true**; choose *England* → column 3 = **["London","Bristol","Manchester","Leeds"]**, live region = *"Selected path: United Kingdom / England"*; then choose *France* → column 2 = **["Île-de-France","Auvergne-Rhône-Alpes"]** and column 3 `hidden` **true** again | ✅ **DRIVEN** |
| 30 | Cascader: the whole thing is operable from the keyboard alone | driven, no pointer: `Down` opens and lands in a column · `Right` enters a branch (focus moves to column **2**) · `Right` on a LEAF does nothing · `Left` returns to column **1** · `Enter` on a leaf commits **"France / Île-de-France / Paris"**, sets `aria-expanded="false"` and returns focus to **`cs1-field`** | ✅ **DRIVEN** |
| 31 | Cascader: one tab stop per column, and a disabled branch refuses | driven: options in column 0 with `tabIndex===0` → **1**; clicking the `aria-disabled` branch (*Singapore*) leaves the path string unchanged → **true** | ✅ **DRIVEN** |
| 32 | Cascader: 44px rows, and no horizontal overflow at either width | driven: column-0 option heights **[44, 44, 44, 44]**; `scrollWidth − clientWidth` → **0** at 1180px and **0** at 480px | ✅ **DRIVEN** |
| 33 | The real HSBC face rendered — asserted with controls, not a boolean | canvas width of `Handgloves 12345` at 40px, in all three drives: target `HSBC_MtUnivers_Latin` **347** · `"Univers Next HSBC"` **347** · `"Univers Next for HSBC"` **347** · control `DejaVu Sans` **375** · control (nonexistent face) **301**. Both aliases land on the target and on neither control | ✅ **DRIVEN** |
| 34 | No colour is invented, and the two-red law is untouched | `grep -cE 'rag/(error\|warning\|success\|information)' knowledge/snippets/{Cascader,Splitter,Qr-code}.reference.html` → **0 CSS declarations in all three** (Cascader's meta mentions rag only in prose about what it does NOT bind). `grep -c '#DA1A00\|#F6604C\|#137F3C\|#66CC8D' <the three files>` → **0** | ✅ |
| 35 | Width belongs to the container | `grep -n 'max-width' knowledge/snippets/Cascader.reference.html` → the only hits are `.demo-w` / `.demo-w.wide` / `.note`, every one inside a block commented `DEMO CHROME`; `grep -c 'max-width' knowledge/snippets/Splitter.reference.html` → **1**, the `.note` prose measure | ✅ |
| 36 | The tree is clean of fontconfig strays after every render | `ls -a knowledge/assets/fonts/_desktop/TTF/ \| grep -c '^\.uuid'` → **0**; the render used the `/var/tmp` symlink farm per the #138 runbook | ✅ |

---

## 3 · WHAT WAS DRIVEN — a real browser, light AND dark, all three

Headless Chromium (`chromium_headless_shell`, `--no-sandbox --disable-dev-shm-usage
--disable-gpu`), each snippet loaded from disk with `goto("file://…")`, the real HSBC cut via
the `/var/tmp` symlink farm (`_RUNBOOK-render-verify.md` § SYMLINK FARM, #138), `data-theme`
toggled live, full-page screenshots in **both modes for all three members** plus a **480px**
narrow pass — **nine PNGs, and they were looked at.**

**Four defects were found, three of them by LOOKING or DRIVING while every gate was green.**

1. **⛔ THE COMMITTED CASCADER'S DESCENDERS WERE CLIPPED — "United Kingdom / England / Bristol"
   rendered as "United Kinadom / Enaland / Bristol".** `_validate_descender_clip.py` was green,
   because the `text-box-edge:text text` declaration WAS there. It just lost the cascade: the
   #209 leading-trim block is `:is(button,a,label,span,…,input[type=text],…):not(:has(svg))`,
   whose specificity is **(0,1,2)** because of the attribute selectors inside `:is()`, and a
   single-class override is **(0,1,0)**. Measured, not reasoned: `.cs-value` computed
   `cap alphabetic` before the selector was raised to two classes and `text` after.
   ⇒ **This is a repo-wide class and six other gated snippets are losing today (claim 20).**
   *Repair here: two-class selectors. Repair there: the conductor's — see §5.*
2. **⛔ A COMMITTED CASCADER RE-OPENED EMPTY IN THE STACKED LAYOUT.** `showLevel(path.length)`
   was unclamped, so once a full path existed no column was marked current — invisible in the
   columns layout, and `display:none` on everything in the container-query one.
   *Repair: clamp to the last column.*
3. **⛔ THE CASCADER'S COLUMNS RE-DIVIDED A FIXED WIDTH AS THE USER DRILLED.** With `flex:1 1 0`
   the first column went 100% → 50% → 33% and the row under the cursor moved out from under it.
   *Repair: the panel grows rightwards on a fixed 220px column basis.*
4. **⛔ A ZERO-WIDTH CONTAINER DESTROYED THE SPLITTER'S SPLIT.** The resize handler re-derived the
   pane size from its CURRENT RENDERED WIDTH. A full-page capture momentarily sizes the viewport
   to 1×1; the handler ran against a 0px container, published 0%, and the restore left the
   divider pinned at maximum — 50/50 became 85/15 untouched. The 1×1 capture is a stand-in for
   every real case with that shape: a hidden tab panel, a `display:none` ancestor, a print
   stylesheet, a collapsed accordion.
   *Repair — a CATEGORY correction, not a guard:* **the ratio is what the user chose; the pixel
   is only how it happens to be drawn right now.** The component keeps the percentage and refuses
   to write a size while there is no room to write it into.

★ **The through-line in all four:** every gate in this repo reads the SOURCE. Three of these four
are only visible in the RENDERED RESULT — a cascade that loses, a layout that empties, a handler
that fires at a size no author ever writes down.

---

## 4 · `$decisionsForDave` — every open question named, none answered

**All of these are Dave's. None is answered by construction.**

### CASCADER

**Q-CS-1 — ⛔ Do Tree and Cascader both exist?** *(the structural one)*
A tree DISCLOSES a hierarchy in place and can hold many branches open; a cascader SELECTS one
path and shows one branch per level. Same data, different jobs. Lane A built Tree in this same
wave. **The relationship is STATED in both metas and adjudicated in neither** — the sidebar-nav
precedent. Live outcome: if they merge, one of the two files should not exist.

**Q-CS-2 — Which ARIA mapping?** Two exist and only one is drawn. **(a) DRAWN:** a chain of
`role="listbox"` columns with roving tabindex and a polite whole-path readout — matches the
layout the eye sees and the keys the user presses. **(b) NOT DRAWN:** one `role="tree"` spanning
all columns via `aria-owns` — matches the DATA, and is what a user who thinks in hierarchies may
expect. Neither is obviously right.

**Q-CS-3 — Is the trigger a combobox?** Drawn as a plain `<button aria-expanded aria-controls>`,
deliberately not `role="combobox"`: a combobox promises one popup of one type and this popup is
several listboxes. Claiming semantics we do not implement is the worse lie — but it is a call.

**Q-CS-4 — Leaf-only, or any-node selectable?** Drawn leaf-only. `any-node` needs a second
affordance (a commit control, or a modifier) so that *opening* and *choosing* stay distinct, and
that affordance is not drawn.

**Q-CS-5 — Which layout is the default, and at what width?** Columns and stacked are both built
and they are the same code; the automatic switch is a **420px container** query. The number is
picked, not derived.

**Q-CS-6 — The panel reserves an empty column slot.** With fixed 220px columns and
`min-width:100%`, a two-column state leaves visible empty space to the right of the last column.
The alternative is a panel that grows and shrinks as you drill — no dead space, but the panel's
right edge moves. **Drawn: reserve.** It reads as "there is room for the next level"; it may read as a bug.

**Q-CS-7 — Should a passing cursor open a branch?** Drawn: **no**, expansion is click/Enter/Right
only. Hover-to-expand is pointer-only and leaves keyboard and touch with no equivalent.

### SPLITTER

**Q-SP-1 — ⛔ Is `aria-valuenow` a percentage or pixels?** Drawn as a percentage. Pixels are the
other honest reading — they are what the user is dragging, and they would let
`aria-valuemin/max` carry the real fences. **This changes what a screen-reader user hears on
every keypress.**

**Q-SP-2 — ⚠ 24px or 44px?** The divider's pointer target is 24px (WCAG 2.5.8) while the drawn
rule is 8px. The hit-area advisory names it four times, `UNDER −20px`. Raising it to 44px means a
44px-wide invisible grab band between two panes. The same inherited-restraint call the gated Tags
chip makes for its dismiss button — **flagged, never silently raised.**

**Q-SP-3 — Does the resting seam need to clear 3:1?** `divider/border/section` measures
**1.31:1** in light. It is deliberately NOT declared as a contrast pair, because a resting seam
is decoration and the control's perceptibility rests on the grip, the hover darkening
(`#808080`, 3.54:1), the cursor, the focus ring and the published value. **Moving it to
`form/border/default` would change every seam in the library.**

**Q-SP-4 — Does a collapsed pane keep an 8px band, or become a re-open affordance?** Drawn: it
keeps the 8px separator, so there is always a way back. A 24px "re-open" tab is the other answer.

**Q-SP-5 — Should a splitter collapse to a stacked layout below some width?** At 480px the panes
measure 215px and 160px — both fences honoured, both cramped. No collapse is drawn.

**Q-SP-6 — Is the orientation naming right?** `data-orientation="horizontal"` means panes side by
side, divided by a VERTICAL bar — which is what `aria-orientation` then says. The trap is real
and the file states the reading on its own face so it can be refused.

### QR CODE

**Q-QR-1 — ⛔ What does a QR code do in dark mode?** *(the biggest one, and now MEASURED)* Fixed
plate keeps a white plate in every theme and **decoded**; theme-following inverts and **did not
decode**, with the same pixels decoding perfectly once flipped back. Fixed plate is a bright
square inside a dark surface. Theme-following is what a dark UI wants to look like. **This is a
product-risk decision as much as a visual one.**

**Q-QR-2 — Which error-correction level?** M throughout. L/Q/H are all legal and the choice
trades symbol size against damage tolerance.

**Q-QR-3 — A centre logo or lockup?** Not drawn. It would REQUIRE level H, and it touches the
`dv-lockup` work. Named, not begun.

**Q-QR-4 — ⚠ Which payment-QR standard, if any?** The second specimen is a **plain-text
demonstration string** and is deliberately NOT an EPC/SEPA payload. The snippet says so twice, on
its own face. Which standard a real payment QR carries is a product question.

**Q-QR-5 — Are 4 / 8 / 12px the right module sizes?** Small is drawn deliberately at the edge of
what ordinary phone cameras resolve at reading distance. The ramp is picked, not derived.

**Q-QR-6 — Where does the QR generator live?** The matrices are computed by a lane-local encoder
that is NOT in the repo. As shipped, the snippet is a static artefact and changing the payload
means re-running a tool nobody else has. Homing that generator in-repo is a real decision with a
real cost, and it was not this lane's to take.

---

## 5 · WHAT STAYS UNPROVEN — declared, not smoothed

1. **THE FOUR-THEME LEGS ARE UNPROVEN FOR ALL THREE COMPONENTS.** The snippet gate resolves
   against the MONO base only, and `_validate_binds_resolve.py` check D fails for all three
   (`.cn-cascader`, `.cn-splitter`, `.cn-qr-code` do not exist in `canon.css`), so theme cascade
   projection is silently OFF. **Only the light and dark legs authored in each file have been
   seen. Console, Legacy and Supercharge are UNPROVEN.** The QR fixed-plate variant is the one
   most likely to survive a theme unchanged because both its tokens are mode-invariant — **that
   is an argument, not a measurement.**
2. **THE DARK-MODE QR FINDING RESTS ON ONE DECODER.** OpenCV 5.0.0's `QRCodeDetector`, one
   version, one library. It is a real reader failing a real render — it is **not** a survey of
   scanners, and it is **not** evidence about any particular phone.
3. **NO PHYSICAL SCAN WAS PERFORMED.** Nothing here has been pointed at with a camera. The claim
   is "these pixels decode", not "this prints and scans at 12mm".
4. **`_validate_kg.py` WAS NOT RUN and will DRIFT.** The three new metas name pattern nodes the
   generated registries have never seen (`pattern:hierarchical-location-picker`,
   `pattern:list-and-detail`, `pattern:scan-to-pay`, and six more). `gen_kg_edges.py` must be
   re-run — a shared generated file, **conductor's**.
5. **`_validate_state_contrast.py` NOT RUN** — a filtered run overwrites the tracked
   `_STATE-CONTRAST-AUDIT.md`, outside this lane's fence. Same declaration Lane P made at #204
   and Lane A at #209. **Owed.**
6. **ONE BROWSER, ONE ZOOM, TWO WIDTHS.** Headless Chromium at 1180px and 480px, plus a 380px
   container-query pass. No second engine, no zoom pass, no touch pass. Pointer drag was driven
   with a synthetic mouse, never a finger.
7. **THE ENCODER COVERS VERSIONS 1–4 AT ECC M ONLY** and was tested on exactly two payloads. It
   is a working artefact, not a library. Its mask CHOICE also differs from `segno`'s for the same
   payload (both are valid symbols; the penalty scoring is not identical), and its padding uses
   `EC/11` where `segno` emits a leading `0x00` — **both decode, and neither difference was
   chased to the bottom.** Declared.
8. **THE HIT-AREA GATE IS ADVISORY AND NOT WIRED.** Its four Splitter findings are a signal, not
   a failure, and the gate says so about itself.
9. **NOTHING HERE HAS BEEN SEEN BY DAVE**, nothing is registered anywhere, and every one of the
   nineteen questions in §4 is open.

---

## 6 · HANDOFF TO THE CONDUCTOR — the serial set this lane could not touch

1. **`.cn-cascader`, `.cn-splitter`, `.cn-qr-code` blocks in `canon/canon.css`** (clears 3 of the
   7 check-D failures; the other 4 are Lanes A and C).
2. **Re-run `gen_kg_edges.py`** (clears the `_validate_kg.py` drift the three new metas create).
3. **`component-types.json` · `CATEGORIES` · `gen_showroom.py` ·
   `_validate_radius.MIGRATED_SNIPPETS`** registrations, if these three are kept.
4. **Store rows for the three new components.** This lane minted **only** `W-73`, the doc-row for
   this receipt, per the return contract.
5. ⛔ **THE ds-005 SPECIFICITY CLASS — the biggest thing in this receipt for the repo at large.**
   Six single-class overrides in five gated snippets are defeated by the #209 leading-trim block
   and are clipping descenders **today**: `Document-row .dr-title` / `.dr-meta`,
   `Sidebar-nav .sn-brand` / `.sn-label`, `Standing-order-mandate-row .mr-payee` / `.mr-meta`,
   `Timeline .tl-title`, `Transaction-row .ldg-name` / `.ldg-ref`. **And the gate cannot see it**
   — `_validate_descender_clip.py` reads the DECLARATION, not the cascade, so every one of them
   is green. Two repairs are available and they are different sizes: raise each override to two
   classes (nine edits, no blast radius), or lower the leading-trim block's specificity once
   (one edit, blast radius = every snippet). **Neither is this lane's to choose.** ⚠ Lane A hit
   the same class independently in `Tree.reference.html` this same wave — that is two lanes
   finding it in one session, which is the twice-caught shape the probe registry promotes on.
6. ⚠ **AN `_ICON-GAPS.md` ENTRY MAY BE OWED**: the library has no drag-grip / handle / resize
   glyph (`ls knowledge/assets/icons/*/ | grep -icE 'grip|drag|handle|resize'` → **0**). The
   Splitter's grip is three bespoke 4px rects, marked as such.
7. ⚠ **RUNNING THE GATES REWROTE TRACKED FILES, AND THAT IS DECLARED, NOT HIDDEN.**
   `git status --short` shows `knowledge/_A11Y-GATE.md`, `knowledge/_ICON-SOURCE-AUDIT.md`,
   `knowledge/_SNIPPET-AUDIT.md` modified as a SIDE EFFECT of the gate runs in this receipt.
   They are gate-authored outputs and they are **shared with Lanes A and C**, which ran the same
   gates, so attribution is the wave's and not any one lane's. **Reconcile deliberately — never
   `git add -A`.**
8. ⚠ **`knowledge/_state.json` SHOWS A 1,328/1,302 LINE CHURN** because `_state.save()`
   re-serialises the whole file. Three lanes minted a doc-row into it in the same window
   (`W-71` Lane C, `W-72` Lane A, `W-73` Lane B). **Check all three rows survived** before
   committing — a concurrent read-modify-write is exactly the shape that loses one silently.
9. **Consider whether the QR generator should be homed in-repo** (Q-QR-6). As shipped, changing a
   payload requires a tool that lives only in the session outputs folder.
