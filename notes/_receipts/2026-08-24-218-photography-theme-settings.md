# Receipt — #218, Dave's four gallery exports for the Photography page (2026-08-24)

**What this is.** Dave drove the `s217-D5` bento matrix explorer's **Gallery** dials in each of the
four themes and pasted the exported state, saying *"can we have this as the settings for the
photography section on the library"*. He then asked for *"all the images we have on file, with a
lazy loader"* and option-selected **mint all 251 at the ruled `s217-D1` spec**, with the ~50 MB
consequence named and accepted (measured after the mint: **251 derivatives, 42.1 MB**).

**Why it is stored verbatim.** The blocks below are the RECEIPT. They are untrimmed and
byte-exact; nothing here is a summary, and the page's stylesheet is compiled from the `state`
blocks rather than from any prose about them.

---

## ⚠ PARSED, NOT SMOOTHED — two `resolved.theme` labels are known-wrong

The **supercharge** and **mono** exports both carry `"theme": "legacy"` inside their `resolved`
block. They were exported **from the legacy tab**: `resolved` is that tab's own live readback of
the document, not a statement about which theme the settings are for.

- **Authoritative:** Dave's prose label for each block, plus the `state` block inside it.
- **Receipt only:** the `resolved` block. It records what one tab measured at the moment of
  export and is kept because a receipt that has been tidied is no longer a receipt.

The four `resolved` blocks are also all `"mode": "light"`. They say nothing about dark mode, and
nothing in this build claims they do.

---

## The settings, read out of the `state` blocks

| theme | spacing | keylines | mode | edge | rounding | pageBg | bentoBg | capBg |
|---|---|---|---|---|---|---|---|---|
| supercharge | **1** | off | bento | square | corners | white | white | transparent |
| console | 24 | off | bento | square | corners | white | white | transparent |
| legacy | 24 | off | bento | square | corners | white | white | transparent |
| mono | 24 | off | bento | square | corners | white | white | **transparent + the rider below** |

**The mono caption rider, Dave's words verbatim:** *"But with the darkest grey for the captions
and white for the text."* This sits **on top of** the mono export, whose `capBg` state word is
`transparent`. The two do not disagree: the explorer's background palette is lightest-grey /
white / transparent (`gen_bento_matrix_217.BACKGROUNDS`) and **none of the three is a dark
ground**, so the rider is an **addition** to the ruled vocabulary rather than a selection from it.
Enacted as `--surface-digital-black` (#1A1A1A in mono, both modes) with `--text-reverse` (#FFFFFF)
ink — tokens, not raw hexes, and mode-stable because a ground ruled by eye must not invert when
the mode flips. **Dave's eye rules the shade on the render.**

**`edge: square` is RECORDED AND NOT ENACTED.** All four exports carry it; the photography wall is
`role=gallery`, and `s217-D3` exempts a gallery from the squaring pass (orphans are acceptable
there — the wall ships with 1 hole at 4 columns, ruled acceptable). Enacting the dial would
overturn that ruling, which was outside this build's fence. The page states both facts and
`gen_foundations_217.py --selftest` bite 29 holds them together.

**"White" is a dial word, not a hex.** `pageBg`/`bentoBg` `white` is the explorer's name for
`--surface-raised`, which resolves to `rgb(255,255,255)` in light mode and to the theme's raised
dark surface in dark mode. The `resolved` blocks below were all taken in light mode.

---

## Appendix — the four exports, verbatim

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

---

## Where these settings are enacted, and what proves it

| surface | what it holds |
|---|---|
| `knowledge/_render/gen_foundations_217.py` | `GALLERY_SETTINGS` + `MONO_CAPTION_RIDER` — the `state` blocks, compiled to per-theme CSS at mint time (`s200-D1`) by `settings_css()`. Every dial word is validated against `gen_bento_matrix_217`'s own ruled option sets before a rule is written. |
| `showroom/_foundations/photography.html` | the compiled block, between the `/* @gallery-settings:start */` and `:end` markers. |
| `knowledge/_render/gen_foundations_217.py --selftest` | bites 6b, 23, 24, 25, 29. |
| `knowledge/_render/verify_photography_218.py` | the settings resolved LIVE, four themes × two modes, off `getComputedStyle` — never off the declaration. |
| `gen_foundations_217.py --break-settings` | the mutation arm: the settings block stripped, so the live assertions can be SEEN to go red by name. |
