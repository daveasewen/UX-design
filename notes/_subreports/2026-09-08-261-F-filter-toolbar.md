# #261 lane F — filter-toolbar-bar, design pass

Component: `knowledge/components/filter-toolbar-bar.meta.json` + `knowledge/snippets/Filter-toolbar-bar.reference.html`.
Dave's #3 nominated dashboard element. No reference existed for the new anatomy — designed by judgment,
PROPOSED, not ruled. Status quoted in the snippet's first comment, per the brief.

## What the pass changed

1. **It drives something.** Under `s258-D1` the bar now publishes an event + attribute contract and the
   demo consumer under it re-queries 24 seeded transactions (`s258-D2`: entities, accounts, channels,
   three currencies, statuses, ages, signed amounts) on every change. `apollo:filter-change` /
   `-clear` / `-export` out; `data-apollo-view` / `-density` written onto the consumer so a CSS-only
   consumer needs no script; `data-apollo-result-count` / `-total` / `-state` **read back**. The bar
   never sets its own state from the request it just made — that read-back leg is the point.
   Documented in the meta under `edges.$contract`, not in prose in the snippet.
2. **Anatomy.** Search · add-filter menu · date-range trigger · applied-filter chips with a `+N more`
   disclosure · results count · clear all · right-aligned export and density. Every one composed from a
   gated atom: Search-field, Dropdown, Segmented-control, Tags, and Links. ONE declared deviation —
   Links' `a.lnk` selector is widened to `:is(a.lnk,button.lnk)` because clear-all and retry are
   actions, not destinations (4.1.2); the paint is unmodified and a 24px centred `::before` grows the
   target, the same idiom Tags' own `.x` uses.
3. **Date range is a TRIGGER.** Presets resolve here; `Custom range…` hands off to `date-range-picker`
   (meta edge `delegatesTo`). Copying half of that component's calendar in would be the re-draw the
   Layer-2 cardinal rule forbids, so partial consumption was declined and the hand-off recorded.
4. **Five states** on one attribute, `data-ftb-state`, with per-node `data-when` membership: no-filters ·
   filtered · loading · empty · error. Loading holds the count's POSITION (skeleton, `role=status`,
   `aria-busy`) and leaves every control live — a filter you cannot change while it runs is a trap.
   Error shows an em-dash, never a stale number dressed as fresh.
5. **Two rows collapse to one** at a container width of 1400px; 680px gives the search its own row;
   400px stacks everything (375px verified, no horizontal scroll). All container queries, so the bar is
   legal in a bento tile (`s248-D3`). Sticky with an EARNED shadow — an IntersectionObserver sentinel,
   not a permanent drop shadow.

## Receipts (all run in this sandbox today)

```
_validate_snippets.py        137 snippet(s), 0 failure(s)
_validate_behaviour.py       Behaviour-contract gate OK — 14,145 code-only bytes of 16,384 per source
_validate_type_composites.py TYPE GATE PASS (1 file)
_validate_icons.py           0 UNKNOWN, 17 bespoke (the neutral selection tick), 750 library glyphs
_validate_grid.py            GRID GATE PASS (1 file)
_validate_coverage.py        137 meta(s) / 137 snippet(s), 0 failure(s)
_validate_a11y.py            137 snippet(s), 0 failure(s)
gen_showroom.py              137 page(s) -> showroom/ (filter-toolbar-bar.html regenerated)
DRIVEN (Chromium, seat_env.sh, real HSBC face — canvas probe 346.88 vs 301.07):
_validate_hit_area.py        1440/680/375px — 144 targets, 0 BREACH-FLOOR  -> notes/_lanes/261-F-HIT-AREA.md
_validate_state_contrast.py  0 carrier failure(s) (was 12 before the fix below)
4 themes x 2 modes shot      notes/_lanes/261-F-filter-toolbar-<theme>-<mode>.png
```

Review page: `notes/_lanes/261-F-filter-toolbar-review.html` — OLD (git HEAD) vs NEW side by side, live,
self-contained, with theme / mode / width controls. Builders: `261-F-shoot.py`, `261-F-build-review.py`.

## Three defects the DRIVEN pass caught that no static gate would have

1. **Chips shrunk to one letter.** With `flex:0 1 auto` and no floor the chip group was squeezed to
   ~10px by its neighbours and every chip clipped to a single character. Fixed with a 200px floor; the
   one-row collapse is now a consequence of both groups fitting at their floors, not a width claim.
2. **Three views painted at once.** `[hidden]` is specificity (0,1,0) and lost to `.ftb-msg{display:flex}`,
   `.demo-cards{display:grid}` and the `<table>` — the empty message, the error message and both views
   rendered together while `hidden` told AT they were gone. This is exactly the `#218 W3 F1` /
   `s218-D5` clause-3 class. The `[hidden]{display:none !important}` remedy is now in the file.
3. **`data-carries="symbol label"` on the amount cells was a false claim** — the minus sign is a LABEL,
   not a symbol, and `_validate_state_contrast.py` measured the absence at the browser (12 ❌). Changed
   to `data-carries="label"`. The error block keeps `symbol label`: it really has a triangle.

## Obstacles / notes for the conductor

- `gen_component_partials.py` **fails on another lane's file** (`Navigations.reference.html` carries a
  `#behaviour-manifest` with no typed behaviour in its meta), so it could not regenerate mine. I
  asserted equality between the snippet's `#behaviour-manifest` and the meta's `behaviour` block
  programmatically instead — script / partial / events / fallback all MATCH. `_validate_kg.py` is also
  red on `data-grid.meta.json`, another lane's in-flight file. Both outside this fence, absorbed.
- **Behaviour budget headroom is 86%** (14,145 / 16,384 code-only bytes in one source). Anything else
  added to this bar's script needs the source split or the demo consumer moved out.
