# #218 build brief — Photography page: per-theme gallery settings + all 251, lazy-loaded

**Ruled by Dave in chat, #218 (2026-08-24).** He drove the gallery dials and pasted FOUR export
blocks — one per theme — saying *"can we have this as the settings for the photography section on
the library"*, then *"Can I have all the images we have on file, with a lazy loader"*, and
option-selected **mint all 251 at the ruled spec** with the ~50MB consequence named and accepted.
The verbatim exports are the receipt — store them untrimmed at
`notes/_receipts/2026-08-24-218-photography-theme-settings.md` (create it from this brief's
appendix; the JSON must land byte-exact).

## The settings (state blocks are authoritative)

⚠ **PARSED, NOT SMOOTHED:** the supercharge and mono exports carry `resolved.theme: "legacy"` —
they were exported from the legacy tab. Dave's prose labels + the `state` blocks are what he
means; the `resolved` blocks are that tab's readback and are receipts only. Say this in the
receipt file too.

Per theme, the Photography foundations page (`showroom/_foundations/photography.html`) renders
its gallery with:

| theme | spacing | keylines | mode | edge | rounding | pageBg | bentoBg | capBg |
|---|---|---|---|---|---|---|---|---|
| supercharge | **1** | off | bento | square | corners | white | white | transparent |
| console | 24 | off | bento | square | corners | white | white | transparent |
| legacy | 24 | off | bento | square | corners | white | white | transparent |
| mono | 24 | off | bento | square | corners | white | white | **darkest grey + white text** |

Mono captions: Dave's words *"But with the darkest grey for the captions and white for the
text."* — **PROPOSED shade: the ruled blackest `#1A1A1A` via the ink token** (never a raw hex if
a token/var carries it; fallback literal per the silent-black gate). His eye rules the shade on
the render; do not present alternatives, just build it and name it in the return.

Implementation: per-theme settings compiled at MINT TIME into the page (s200-D1 — concrete
values under theme scopes), through the ONE writer (`gen_foundations_217.py`) consuming
`gen_bento_matrix_217` / `gen_bento_roles_217` modules — never a second copy of the gallery
maths. Caption space stays the derived 86px. P2 legality: mono's dark-on-white caption is legal
and needs no exemption.

## All 251, lazy

- Mint web derivatives for ALL 251 manifest rows through `knowledge/_build_photo_manifest.py`
  at the RULED spec (1600px / ~300KB / sRGB / progressive JPEG — s217-D1's spec, unchanged).
  Originals are at `knowledge/assets/photography/` (present at this seat, 2.5G, gitignored).
  ⛔ **CHUNK THE MINT** — 251 images will not survive a single 45s call; process in ranges with
  a resumable loop, and verify the count at the end (`ls | wc -l` == 251 + the 3 portrait extras
  already there, or whatever the real disjoint set is — MEASURE, don't assume).
- Update the manifest rows' `derivative` fields through the generator (never hand-edit the
  JSON), regenerate `_PHOTOGRAPHY-MANIFEST.md`.
- Page: all 251 in the gallery bento, ruled emphasis rhythm + aspect spans + squaring ladder
  (gallery holes tolerated per s217-D3), `loading="lazy" decoding="async"` on every `<img>`,
  zero-JS lightbox kept. **6 rows have no `exif_description`** — their captions render the
  licence line only; declared on the page as absent, never faked.

## Fence (DO-NOT-RULE)

No `_rulings.json` writes. No change to s217-D1's ruling or derivative spec. No token/canon
edits. No edits to the matrix explorer, the grids pages, logos. No lane/worklist/GM/LS/memory
edits. No commit, no push. The INSTRUMENT-STRAY capture-gate behaviour on untracked derivatives
is a known wrap-seam issue — leave it to the conductor, do not "fix" the gate.

## Proof (bounded, s172-D3)

- Per theme ×2 modes: gutter resolves 1/24/24/24, zero keyline elements, caption ground+ink per
  the table (mono: #1A1A1A ground, white text, measured), page+bento grounds white.
- 251 tiles rendered; every `src` resolves to a file on disk; every img carries `loading="lazy"`;
  the derivative count on disk matches the manifest's derivative fields.
- Fonts against two controls; dangling sweep; thumbnails re-shot for the photography page.
- One mutation arm: the per-theme settings block stripped ⇒ settings assertions red by name
  (use `BM_MUTANT_DIR`, session-suffixed).
- Bounded: the full `_build_all.py` is known-blocked at this seat (step [13], pre-existing);
  run the affected gates as the grids build did.

## Pitfalls, replayed

Same as the grids brief (shared /var/tmp, 45s kill, goto not set_content, var fallbacks,
compiled literals, arm-must-run-red, thumbnails) PLUS: the mint is I/O heavy — run it in the
sandbox with progress printed per range so a killed call is resumable, and `df -h` first
(ENOSPC masquerades — runbook pothole; the repo mount has the space, /var/tmp may not).

## Appendix — Dave's four exports, verbatim receipts

(supercharge)
```json
{"$proposed": true, "not_ruled": "Everything beyond s217-D5's own words is PROPOSED, not ruled.", "ruling": "s217-D5", "type": "gallery", "state": {"spacing": "1", "keylines": "off", "mode": "bento", "edge": "square", "rounding": "corners", "pageBg": "white", "bentoBg": "white", "capBg": "transparent"}, "resolved": {"theme": "legacy", "mode": "light", "role": "gallery", "gutterPx": 1, "containerRadiusPx": 0, "tileRadiusPx": 0, "tileBorderPx": 0, "pageBackground": "rgb(255, 255, 255)", "bentoBackground": "rgb(255, 255, 255)", "captionBackground": "rgba(0, 0, 0, 0)", "captionSpacePx": 86}}
```
(console)
```json
{"$proposed": true, "not_ruled": "Everything beyond s217-D5's own words is PROPOSED, not ruled.", "ruling": "s217-D5", "type": "gallery", "state": {"spacing": "24", "keylines": "off", "mode": "bento", "edge": "square", "rounding": "corners", "pageBg": "white", "bentoBg": "white", "capBg": "transparent"}, "resolved": {"theme": "console", "mode": "light", "role": "gallery", "gutterPx": 24, "containerRadiusPx": 0, "tileRadiusPx": 0, "tileBorderPx": 0, "pageBackground": "rgb(255, 255, 255)", "bentoBackground": "rgb(255, 255, 255)", "captionBackground": "rgba(0, 0, 0, 0)", "captionSpacePx": 86}}
```
(legacy)
```json
{"$proposed": true, "not_ruled": "Everything beyond s217-D5's own words is PROPOSED, not ruled.", "ruling": "s217-D5", "type": "gallery", "state": {"spacing": "24", "keylines": "off", "mode": "bento", "edge": "square", "rounding": "corners", "pageBg": "white", "bentoBg": "white", "capBg": "transparent"}, "resolved": {"theme": "legacy", "mode": "light", "role": "gallery", "gutterPx": 24, "containerRadiusPx": 0, "tileRadiusPx": 0, "tileBorderPx": 0, "pageBackground": "rgb(255, 255, 255)", "bentoBackground": "rgb(255, 255, 255)", "captionBackground": "rgba(0, 0, 0, 0)", "captionSpacePx": 86}}
```
(mono — plus his caption rider, his words: "But with the darkest grey for the captions and white for the text.")
```json
{"$proposed": true, "not_ruled": "Everything beyond s217-D5's own words is PROPOSED, not ruled.", "ruling": "s217-D5", "type": "gallery", "state": {"spacing": "24", "keylines": "off", "mode": "bento", "edge": "square", "rounding": "corners", "pageBg": "white", "bentoBg": "white", "capBg": "transparent"}, "resolved": {"theme": "legacy", "mode": "light", "role": "gallery", "gutterPx": 24, "containerRadiusPx": 0, "tileRadiusPx": 0, "tileBorderPx": 0, "pageBackground": "rgb(255, 255, 255)", "bentoBackground": "rgb(255, 255, 255)", "captionBackground": "rgba(0, 0, 0, 0)", "captionSpacePx": 86}}
```

## Return

Files changed, derivative count + total MB measured, probe tails (green + arm red by name),
the mono caption shade named with its token, residuals priced, fence findings named not enacted.
