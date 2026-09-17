# #282 lane LR — the logo review (P-277-4)

**Verdict: the review is on one page and two of the twelve files are broken.** `masterbrand-identifier-dark-colour.svg` and `masterbrand-identifier-dark-mono.svg` do not contain an identifier. They are the plain masterbrand, re-exported into a canvas more than twice as wide as the ink in them. The conductor's byte-size smell was right about those two and wrong about the hexagons: the 619-byte pair is one drawing exported twice, which for a colour hexagon is correct, not defective. Everything below was measured today; nothing under `knowledge/` was touched.

Page: `notes/_lanes/282/logo-review/LOGO-REVIEW-2026-09-17.html` (169,336 bytes, 36 inlined SVGs, 12 radio groups / 36 radios, 0 console errors).
Evidence: `notes/_lanes/282/logo-review/artwork.json`, `bindings.json`, `verify-1280.png`, `verify-390.png`.

## The defects, file by file

**1 · `masterbrand-identifier-dark-colour.svg` — BLOCKING.** 2,584 bytes, `viewBox="0 0 795 85"`, 9 paths, fills `#DB0011, none, white`. Ink stops at x=314.2 — **39.5% of its own canvas**. The light twin carries a 5,020-character identifier path filled `#333333` that reaches x=777; this file has **no `#333333` path at all**. Diffed against `masterbrand-dark-colour.svg` (2,584 bytes) the two files differ by exactly one `viewBox` line and one rounding digit (`236.374` vs `236.375`). It is the masterbrand with a wider box. Bound to a component it would render the masterbrand at 40% scale with 60% empty space beside it.

**2 · `masterbrand-identifier-dark-mono.svg` — BLOCKING.** Same finding: 2,493 bytes, `viewBox="0 0 795 85"`, 8 paths, fill `white` only, ink stops at x=313.9. Against `masterbrand-dark-mono.svg` (2,496 bytes) the diff is one `viewBox` line and three float-rounding digits. No identifier path.

**3 · `masterbrand-identifier-light-mono.svg` — ADVISORY.** A "mono" file with two inks: the masterbrand paths are `#000000`, the identifier path is `#333333`. Either Global Brand Design tints identifiers — in which case the tint is a rule the corpus does not carry — or the mono export did not flatten. va25-016 forbids recolouring a logo, which makes the unwritten second ink the sharper reading.

**4 · `hexagon-dark-colour.svg` / `hexagon-light-colour.svg` — HOUSEKEEPING, not a defect.** 619 bytes each, 5 paths each, identical geometry and fills, differing in a single float literal (`9.15527e-05` vs `8.58307e-05`). This is expected: the colour hexagon has no ground-dependent ink (red chevrons, white infill) so light and dark genuinely are the same artwork. Two Figma nodes, one asset, two graph nodes. Nothing to re-export; the only question is whether the library keeps two.

Dark ≠ light everywhere else: the masterbrand pairs differ correctly (wordmark `black` on light, `white` on dark), and `hexagon-light-mono` is black where `hexagon-dark-mono` is white. The exporter is not systematically broken: it broke on exactly the two files whose identifier ink is white.

## The bindings

12 nodes · 31 edges · 19 `usesLogo` edges = **18 distinct component→lockup pairs plus one declared null**. 9 components bind a logo; **4 lockups are bound, 8 are bound by nothing** (all four hexagons, all four identifier variants). `governedBy` is declared-null for 10 of 12, as ratified under s277-D4.

Every bound component reaches for the plain masterbrand: `masterbrand-light-colour` (8 components) and `masterbrand-dark-colour` (8) in the app shells, navigations and the bento dashboard; `masterbrand-light-mono` (1) and `masterbrand-dark-mono` (1) in `template-auth`. The live grep over `knowledge/components/**` and `knowledge/snippets/**` agrees with the node file — 14 files carry an `assets/logos/<name>.svg` src, and two more (`app-shell-doormat.meta.json`, `app-shell-focused.meta.json`) mention the directory in prose about the #230 ruling, which is why a `grep -l` says 16. `app-shell-nav-rail` is the declared null, and s230-D2 is the reason: "56px rail head, no lockup fits".

**Rules that name a logo: 27** by a text grep of `_rules-index.json` (`logo`, `lockup`, `lock-up`, `hexagon`, `masthead`, `wordmark`) — the brief expected ≥6 and the honest number is larger because hexagon/masthead rules live in colour, motion, typography and the toolkit files. The governing set is smaller: **11 rules sit in the two logo sections** (`logo26-001..007` in brand-refresh-assets.md, `va25-014..017` in visual-assets.md), and only 6 of those 11 contain a logo word in their own text — `logo26-002..006` carry the subject in their heading. Both counts are on the page so neither can be quoted alone. `logos.md` contributes **0 rules**, as the #277 page said of that file.

## The six questions, and what I recommend

- **Q1 (4 groups, one per defective file) — fix `clean()` in `_export-logos.py`, then re-export from Figma.** The cause is probably ours: `clean()`'s background-stripping regex matches any wide white path, and the identifier path begins at x=404 (see UNPROVEN). Re-exporting without the fix may reproduce the same file. For the two-tone light mono, a plain re-export. For the hexagon pair I recommend keeping both files and both nodes and writing the duplication down.
- **Q2 (4 groups, one per theme: Legacy, Mono, Console, Supercharge) — full colour on both grounds in all four.** That is logo26-003 read straight and what 8 of the 9 binding components already do. **Ruling-shaped:** Apollo Mono is "very mono — colour ONLY in RAG status and dataviz" and the masterbrand is red. My reading is that the theme's colour discipline governs UI, not a placed brand asset. That reading is an inference, not a ruling, and it is on the page as such.
- **Q3 clear space and minimum size — author from create.hsbc, your authenticated fetch.** Measured: the brand-refresh source snapshot (11,836 bytes) returns **zero** matches for *clear*, *minimum* or *NNmm*, so the brief's condition for proposing a number is not met. The corpus does carry numbers, once, in the 2025 page — va25-014: "clear space = 1× hexagon height on all sides; minimum size = 7mm hexagon height / 105×20px / 26×7mm; positioning = top-left or bottom-left, inset 1× hexagon from edges" (ADVISORY). Promoting those into a `logo26-*` rule is offered as option (b), and choosing between a 2025 number in force and a 2026 number you have to fetch is **ruling-shaped**: bra26-003's vintage discipline points one way, having any enforceable minimum at all points the other.
- **Q4 hexagon alone — permit it on the nav-rail head, app tile and favicon, each conditional on Create Direct approval and "HSBC" in view.** va25-016 names those examples; `app-shell-nav-rail` is the only real candidate in the library and is the one component s230-D2 deliberately left unbound. It would also give the four hexagon files their first consumer. **Ruling-shaped:** Create Direct approval is a per-use external gate that a component contract cannot hold.
- **Q5 guideline shape — `logos.md` becomes a pointer.** It keeps what only it has (which Figma node produced which file, and that all 12 are vector) and stops being a rival standard with 0 rules in it. A full merge would destroy the vintage boundary bra26-003 protects.
- **Q6 the eight unreferenced lockups — keep as library, the declared null stands.** logo26-002 says use the original, which means the original has to be present, and Q4 may give the hexagons a consumer this week. The counter-case is on the page: the two dark identifiers are wrong precisely because nothing renders them.

## COUNTS

lockups 12 · files measured 12 · exporter defects 3 (2 blocking, 1 advisory) + 1 housekeeping duplicate pair · lockups bound 4 · unbound 8 · components binding a logo 9 · distinct component→lockup pairs 18 (+1 declared null) · rules naming a logo term 27 · rules in the two logo sections 11 · themes 4 · questions 6 · radio groups 12 · radios 36 · SVGs inlined 36 · console errors 0 · page 169,336 bytes.

## ruling-shaped

1. **The masthead lockup in Apollo Mono** — a monochrome theme and a red masterbrand. I recommended colour; the reasoning is an inference about what "very mono" governs.
2. **Whether s230-D2's default was library-wide or Legacy-only** — the graph carries it as two `defaultFor` edges with `theme` as an edge property and `t: null`. Q2 asks per theme rather than assuming.
3. **The clear-space and minimum-size number** — 2025's va25-014 in force now, or a 2026 number only Dave can fetch. Not mine.
4. **Hexagon-alone permission** — the rule requires an external per-use approval; whether a component contract may assume it is Dave's.
5. **Whether the `#333333` identifier tint is intended** — cannot be settled without the Figma node or create.hsbc.
6. **Writing the `_state.json` row** — the brief says edit nothing under `knowledge/` and also says add the row via `_state.add()`. I read the first as scoping to assets, guidelines, node files and rulings, and added the row. Flagging the tension rather than deciding it silently.

## UNPROVEN

- **That the exporter is the cause.** The mechanism is measured, the event is not. `clean()` in `_export-logos.py` strips `<path d="M-?\d{3,}…" fill="white"/>`, a rule written to remove Figma's white background path. The identifier path is `<path d="M404.468 59V24.296…">` — it starts at x=404, so it matches the `\d{3,}` arm, and it survives in the light files only because it is filled `#333333` rather than white. On a dark export the identifier is white. **Not reproduced**: confirming it needs a `FIGMA_TOKEN` and a re-export, which this lane does not do. The alternative — a broken Figma node (2384:92925 / 2384:92910) — is not excluded, and the same re-export distinguishes them.
- **Whether create.hsbc's 2026 page carries a clear-space or minimum-size number at all.** Only the local snapshot was searched; the live page is login-walled.
- **The render fidelity of any lockup below its ruled minimum.** The page renders at 105px and 32px; nobody has checked legibility on a real device.
- **`va25-014`'s "105×20px"** is quoted as stored. The masterbrand viewBox is 315×85 (3.7:1), so 105×20 (5.25:1) is not this lockup's aspect ratio. The number may describe a different lockup or predate this artwork. Not resolved here.

## REPLAY-THESE

1. `sha256sum knowledge/assets/logos/*.svg` — 12 shas, recorded in `artwork.json` and printed under every rendering on the page.
2. `diff <(fold -w100 knowledge/assets/logos/masterbrand-dark-colour.svg) <(fold -w100 knowledge/assets/logos/masterbrand-identifier-dark-colour.svg)` — two lines out: the viewBox, and one digit.
3. `grep -c '#333333' knowledge/assets/logos/masterbrand-identifier-*.svg` — 1 in each light file, 0 in each dark file.
4. `grep -ioE 'clear|minimum|[0-9] ?mm' knowledge/guidelines/_sources/brand-refresh-assets/all-pages.txt` — no output. The refresh source carries no number.
5. `python3 /tmp/lr/bind.py` re-derives `bindings.json` from `_logo_nodes.json` + a live grep + `_rules-index.json`; the node file and the grep agree or a row is wrong.
6. The verification run: 36 SVGs, 36 radios, 12 groups, 0 external refs, `Take all the recommendations` → 12 checked, export round-trips with the note preserved, no horizontal scroll at 1280 or 390, console `[]`.
