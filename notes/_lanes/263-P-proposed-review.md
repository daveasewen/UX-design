# #263 lane P — the eleven proposed defaults, review page

**Built:** `notes/_PROPOSED-263.html` (50,906 bytes). Generator, kept as a lane fragment:
`notes/_lanes/263-P-build.py` — the page is regenerable, not hand-edited.

⛔ **NOTHING WAS RULED BY THIS LANE.** Every ruling row ships empty; no default is
pre-selected, and the export block reads `(nothing ruled yet)` until Dave touches it.

## What the page is

Swiss / International, single column, `--max:760px`, system font stack, 8px scale
(`--s1…--s6`), hairline `1px solid var(--rule)` separators, no shadows, no radius.
Self-contained: no CDN, no `<link>`, no external font, no `url()` and no `@import`
anywhere in the file. Light/dark by `prefers-color-scheme` only.

- **TWO-RED LAW (s151-D1)** honoured: `--accent:#DA1A00` on `:root`, `--accent:#F6604C`
  under `prefers-color-scheme:dark`. Accent paints the eyebrow, the field labels (`.k`),
  the pull-quote's left border, the selected ruling button's 3px underline, the focused
  note field's rule and the live tally numeral — **never body text**.
- **`knowledge/canon/type.css` is BAKED IN VERBATIM** at the top of the `<style>`, per the
  LABEL CROP PATTERN (review pages inline type.css rather than link it). The component crop
  rule **exists in type.css and is named in a comment above the baked block**:
  `text-box: trim-both cap alphabetic;` on the control/label list (`.btn`, `.chip`,
  `.seg button`, `.tabbar .tabbar__item`, `nav.main a`, …) at `type.css:150–164`, with the
  `@supports not (text-box-trim: trim-both)` fallback pair
  `.t-cm-slot::before` / `.btn::before` and `.t-cm-slot::after` / `.btn::after`
  (`type.css:165–170`) using `calc((0.5 - 0.65 + …)*-1em)` against `--cap` / `--desc`.
- **Structure:** masthead (`Eleven proposed defaults — #263 · rule each`, standfirst, four
  counts: 11 proposed · 0 ruled at #261 · 7 lanes · n ruled here) → sticky bar (live tally,
  "Dave's decision only" toggle, Export rulings, Clear all) → eleven cards `P-01`…`P-11`,
  each with a mono id, title, lane, the verbatim recommendation as a bordered pull-quote,
  the reason given, **current default** (mono path + what the code actually does),
  **alternative**, and a ruling row (Accept / Reject / Later + a one-line note field) →
  export `<pre>` → footer.
- **JS (vanilla, 3,435 bytes):** selection + note persist to `localStorage` key
  `apollo-proposed-263`, every read and write inside `try/catch`; live tally "n of 11 ruled"
  in two places; clicking the selected button again unsets it. **Export rulings** renders,
  in a `<pre>` with no download, one line per ruled item in card order:
  `s263-Dn · P-xx · ACCEPT|REJECT|LATER · <title> · note: …` (an em-dash when the note is
  empty), then a `NOT RULED (n): P-xx …` line so the wrap can see what is still open.
- **"Dave's decision only"** hides `.cbody` on every card — id, title and the ruling row
  remain.
- 44px minimum on every ruling button and the note field; at ≤760px the button group goes
  full width and splits three ways. `overflow-x:hidden` on `body`, `overflow-wrap:anywhere`
  on paths — nothing horizontal-scrolls.

## Per-item source pointers

| id | item | lane | source |
|----|------|------|--------|
| P-01 | delta glyph ink seat | K | `notes/_subreports/2026-09-08-261-K-kpi-tile.md:102–104`; code `knowledge/snippets/Kpi-tile.reference.html:60–80,151–152` |
| P-02 | group row by type, not split | G | `…-261-G-grid-header.md:56–58`; code `knowledge/snippets/Data-grid.reference.html:129,138,211` |
| P-03 | disabled column muted by alpha | G | `…-261-G-grid-header.md:59–60`; code `knowledge/snippets/Data-grid.reference.html:249` |
| P-04 | adopt `data-apollo-filter-*` | F | `notes/_lanes/261-F-filter-toolbar-review.html:153–155`; `…-261-F-filter-toolbar.md:10–16`; code `knowledge/snippets/Filter-toolbar-bar.reference.html:433`, `knowledge/components/filter-toolbar-bar.meta.json:119–123` |
| P-05 | the 1400px collapse | F | `…-261-F-filter-toolbar.md:29–32` (and `:79` for the measured control heights) |
| P-06 | keep the Tab-bar name | N | `…-261-N-nav.md:93–98` |
| P-07 | retire the doormat | Ft | `…-261-Ft-footer.md:82–83`; code `knowledge/components/footer.meta.json:100–103` |
| P-08 | 44px legend seat | L | `…-261-L-legend.md:47–50` and `:86–88` |
| P-09 | `data-dv-controls` contract-only | L | `…-261-L-legend.md:52–57` and `:90–92` |
| P-10 | `--check` as a wrap gate | R | `…-261-R-rulings-page.md`, "Open questions for Dave" item 1, with the driven RED/control receipts immediately above it |
| P-11 | retire the source-text aria arm | D3 | `…-261-D3-driver-scope.md:95–99`, evidence at `:20` and `:28–30` |

Carry text for the set: `_LIVE-STATE.md:102` and
`_DECISION-HISTORY/2026-09-09-261-six-components-and-a-false-premise.md:136–143`.

## Items with THIN sources — flagged on the card itself, not smoothed over

1. **P-04 `data-apollo-filter-*`** — the F subreport documents the contract (`edges.$contract`
   in the meta) but carries **no "ruling-shaped" ask for it**. The wording quoted on the card
   is the lane's own review-page spec table, not a recommendation sentence. The item is on the
   eleven-list; its recommendation is not in the report. Stated on the card.
2. **P-05 the 1400px collapse** — sourced from a **build note, not an ask**. The report states
   1400 as what was built; it lists no alternative and no recommendation sentence. Stated on
   the card; the alternative offered there is inferred from the footer lane's comparable
   1440→1600 move, and is labelled as such.
3. **P-01 the delta glyph ink seat** — ⚠ **overlaps an answer he may already have given.** The
   K3 review carries his verbatim *"We need to use the dark versions of the colours on the
   arrows"*, and `Kpi-tile.reference.html:64` declares the two-seat question **CLOSED** on it —
   but no `s261-D*` entry states the seat (`s261-D4`'s `says` is the layout / arrow / end-dot
   answer), so the ledger does not carry it. The card says exactly this and asks him to
   confirm or correct rather than assuming either way.

Everything else quotes a "ruling-shaped" / "wants Dave's word" / "open questions" item
verbatim from its lane report.

## Verification receipts (verbatim, this sandbox)

    $ grep -c "cdn\|https://fonts\|<link" notes/_PROPOSED-263.html
    0

    $ grep -n "@import\|url(" notes/_PROPOSED-263.html
    (no output)

    $ grep -c '<article class="card"' notes/_PROPOSED-263.html
    11

    $ grep -o 'data-pid="P-[0-9]*"' notes/_PROPOSED-263.html | sort -u
    data-pid="P-01" … data-pid="P-11"        (11 distinct)

    $ wc -c < notes/_PROPOSED-263.html
    50906

    $ python3 - (html.parser, stack-balance + count)
    parse: mismatched=0 unclosed=[] articles=11 unique_ids=17

    $ node --check <extracted inline script>          # /usr/bin/node present
    returncode=0  stdout=''  stderr=''                (script 3,435 bytes)

**Not verified.** No browser was driven — the workspace has no usable Chromium for this lane
and the pane refuses `file://`. The 375px no-horizontal-scroll claim, the print rules, the
dark-mode plate and the localStorage round-trip are argued from the CSS/JS, **not driven**.
Do not treat those as green until a lane with playwright deps screenshots 375/768/1200 ×
light/dark and asserts `h-overflow=0px`.

**Not done.** Nothing committed, nothing staged (per the lane fence). `notes/_lanes/263-P-build.py`
is written but not registered anywhere. The **Stat card arrow seat** — the twelfth open item that
`_CARRIES.md` `→ #263` says "belongs on the same page as item ①" — is **NOT on this page**: the
brief named eleven and eleven is what was built.
