# LANE AR — REPORT — the 15-base active review sheet for Dave (P-277-3)
#279 · 2026-09-16 · instrument for the manual review under `s277-D6` · lane AR (Fable 5.1) · nothing under `knowledge/` touched; every figure on the page is derived at build time from `knowledge/_icon_nodes.json` and the SVGs it names.

**The one line.** `notes/_lanes/279/active-review/REVIEW-active-2026-09-16.html` — one row per base (15), the base and its 2–3 "active" candidates each drawn at 48px + 16px on a light chrome and a dark chrome side by side, one radio answer per base (`<slug>` is the twin · none of these · flag + per-candidate checkboxes + a note), progress in a sticky nav, answers in localStorage, **Export** writing `DAVE-EXPORT-active-2026-09-16.json`. Driven green (36/36 checks), then screenshotted in a never-driven fresh context, light + dark × 1280 + 390, and looked at.

## 1. What the page derives, and from where

| figure | value | derived from |
|---|---|---|
| bases | **15** | the `defaultActive` rows in `_icon_nodes.json`'s `unresolved` ledger (`source` = the base) |
| candidates | **31** | the `note` of each row (`<base>: <a>, <b>[, <c>]`), each cross-checked against an `activeVariantOf` edge to that base — the builder refuses otherwise |
| bases with two / three | 14 / 1 (`dentist`) | counted |
| glyphs on the sheet | 46 | 15 + 31, each inlined 4 times (2 sizes × 2 chromes) = 184 `<svg>` |
| by group | Informative 7 · Products and services 5 · Media 2 · Global controls 1 | node `group` |
| Figma name per base | one, e.g. "Alert Active" | node `name`; the builder refuses if a base's candidates carry more than one |
| fill mode | all `currentColor` | node `fillMode`; the builder refuses any SVG that does not paint with `currentColor` (the chrome panes could not invert it) |

The ruling's figures (15 / 31) are ASSERTED after derivation, never read in. Nothing is typed into the HTML that the build can compute.

## 2. The page

Swiss idiom: sticky nav (brand · "N of 15 decided" + 2px accent track · Export), hero with the label pattern + title + a 3fr/1fr/4fr proposition split + a 4-cell stat strip + a 3-column "how to answer" row, then 15 `section.base` rows on a 1fr/2fr split (index numeral + name + slug + "2 drawings exported as 'X Active'" + group/fill + live state left; candidate cards + the ask right), then the export section and a footer. Plain prose only in the body; the ruling id sits once in the footer.

Each glyph card is a **chrome pair**: a fixed white pane (`#333` ink) and a fixed `#111` pane (`#F2F2F2` ink), each showing the 48px and 16px renders, so the pair reads the same on a light and a dark page. The base card is captioned "the base — inactive"; candidates "candidate n of N". A chosen twin's card takes the accent border.

The ask per base: one radio per candidate ("`slug` is the active twin of `base`."), "None of these is the twin.", "Flag: a drawing here is its own icon and needs an inactive version drawn." with a checkbox per candidate under it (ticking a box selects the flag radio), and a note box. Progress counts a base as decided when its radio is set.

## 3. Export envelope

```
{ page: "REVIEW-active-2026-09-16",
  at:  "<ISO>", exportedAt: "<ISO>",          // same instant; `page`+`at` are the v2 page's keys, `exportedAt` the brief's
  answers: { <base-slug>: { choice: "twin"|"none"|"flag"|null,
                            twin:   <candidate slug>|null,
                            flags:  [<candidate slug>, ...],
                            note:   "" } ... all 15 bases ... } }
```

Mechanics copied from `_build_page_v2.py`: a Blob download + a `<pre>` on the page + Copy-to-clipboard + Clear-all with confirm; localStorage key `apollo.review.active.2026-09-16`, stored as `{answers, at}`. Undecided bases export with `choice: null`, so a partial review is still a valid file. A sample from the driver is at `_driver-export.json` (alert → twin `alert-active` + note; contact-chat-ai → none; dentist → flag `dentist-active`, `dentist-active-2`).

Deviation from the brief, said: the brief's envelope was `{exportedAt, page, answers}` and the v2 page's is `{page, at, decisions}`; this page emits `page`, `at` AND `exportedAt` so whichever key the inscribe tooling reads is there.

## 4. Gates

- `_build_review.py`: 15 bases / 31 candidates asserted after derivation · every SVG on disk · every SVG paints with `currentColor` · one Figma name per base · every candidate has an `activeVariantOf` edge to its base · `node --check` on the extracted inline script (temp file) → OK.
- `_drive_review.py` (Chromium via `knowledge/_render/seat_env.sh`, the seat's own headless shell — `/tmp/pw` holds shell build 1243 and the seat's playwright wants 1234, so the seat env was used; nothing downloaded): **36 checks, 0 failures** — no ruling id in body copy; 15 rows / 31 cards / 184 svg / 0 duplicate DOM ids; 61 radios (31 + 2×15), 31 checkboxes; virgin first load; progress 0 → 3 of 15; flag checkbox selects the flag radio; chosen card marked; download named `DAVE-EXPORT-active-2026-09-16.json`; envelope keys and per-base shape; the three driven answers exact; 12 undecided as null; localStorage round-trip across reload; no page errors; no horizontal overflow at 1280 and 390 in both themes; every fresh screenshot context virgin before its PNG.
- No repo file outside `notes/_lanes/279/active-review/` changed (the two dirty instrumentation logs are not this lane's and are not staged).

## 5. Screenshots — looked at, not just taken

`shots/ar-{1280,390}-{light,dark}.png` (full page), `ar-1280-*-top.png` (first viewport), `ar-*-row01.png` (the alert row). All from a fresh context with cleared storage. Palette-quantised (64 colours) to keep 2.0 MB on a disk at 99 %.

Seen and fixed by eye: at 390 the nav wrapped to three lines (brand / progress / button, ~150px of sticky chrome) — brand now hides under 640px and the nav stays one line. Seen and left: the one three-candidate row (dentist) wraps its fourth card to a second line at 1280 — legible, and the alternative (narrower cards) would crowd the 48+16 pair.

What the sheet already shows on row 01: `alert-active-2` is a bell with a plus — the second defect the ruling names, on the first row.

## 6. Not done, with size

- No "decided" state screenshot ships (the brief asked for never-driven PNGs only); the driven state is proven by the checks and `_driver-export.json`. Small.
- One answer per base, per brief. A row like dentist could in principle want a twin AND a flag on a third drawing; the note box carries that until Dave says the form should. Small — a form change if he wants it.
- No inscribe step: this lane ships the instrument; the reading of Dave's export into rulings is the next lane's.
