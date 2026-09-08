# 2026-09-08 · s258 lane 3 — the three scripted components get a typed `behaviour`

Subject: COLDRUN-258-2026-09-08-v1.html finding 2 — 21 of 136 metas carry a `behaviour`
key, and `data-grid` / `filter-toolbar-bar` / `sidebar-nav` carried NONE while shipping
17,603 / 5,420 / 3,918 bytes of working inline script. `_validate_receipt.py` step 4b
therefore checked nothing for the three components carrying the interactivity: it read
`meta:NONE` and printed UNPROVEN.

## What was done

Typed `behaviour` added to three metas, address form `#script` (each snippet carries ONE
inline executable `<script>` outside any AUTO-BEHAVIOUR markers — measured with
`VR.inline_scripts`, so the s245-D1 grammar's third form is the correct address; none of the
three consumes a registered partial, so `partial: null`):

| slug | script address | events | script bytes |
|---|---|---|---|
| data-grid | `knowledge/snippets/Data-grid.reference.html#script` | blur, change, click, dblclick, keydown | 17,603 |
| filter-toolbar-bar | `knowledge/snippets/Filter-toolbar-bar.reference.html#script` | click, keydown, resize, transitionend | 5,420 |
| sidebar-nav | `knowledge/snippets/Sidebar-nav.reference.html#script` | click, keydown | 3,918 |

`events` were EXTRACTED from each snippet's own script (`addEventListener('<name>'`), never
authored — s245-D4. `fallback` is prose, per component:

- **data-grid** — the honest one, and the sharp one: `<tbody id="tbody">` carries only a
  comment and every row is rendered by the script, so with JS off there is NO DATA AT ALL.
  Chrome (header, search field, rows-per-page select, authored footer range) still paints.
- **filter-toolbar-bar** — everything paints and every control focuses; what goes is the
  search clear, the dropdown open, the segmented indicator placement (script-driven, incl.
  on resize) and chip dismiss.
- **sidebar-nav** — every row is a native `<a>` and stays in the tab order; the authored
  `aria-current="page"` stands and both visual carriers follow it because they are bound to
  the attribute in CSS. What goes: moving the current, Space activation, the arrow walk, the
  group disclosure and the rail collapse.

The pre-existing prose in each snippet's script comments was NOT deleted: the substance
travels under `$note` (by-addition, ADR-0017), each with a `$unproven` line saying the prose
is derived from the script and its comments, not from a driven probe.

`#behaviour-manifest` blocks were injected into the three snippets by IMPORTING
`gen_component_partials.behaviour_manifest_block` / `inject_behaviour_manifest` and calling
them for these three slugs only — the generator's own bytes, not a hand copy (the block says
DO NOT hand-edit), and scoped so no other lane's snippet was touched. Status for all three:
`injected`. `python3 knowledge/gen_component_partials.py --check` → exit 0, "all AUTO-PARTIAL
blocks in sync, contracts hold", which is the idempotence proof.

No script was rewritten.

## Gates

Per-snippet, before and after (identical both sides — a reference snippet is not a composed
page):

| gate | before | after |
|---|---|---|
| `_validate_receipt.py <snippet>` | exit 1 · `FAIL:NO-RECEIPT` | exit 1 · `FAIL:NO-RECEIPT` |
| `_validate_screen.py <snippet>` | exit 1 · `⛔ SCREEN-GATE INDEX REFUSED` | exit 1 · same |

Both refusals are structural and pre-existing: a snippet carries no `#provenance-receipt`,
and the screen gate refuses to build its index while `knowledge/_screen-gate/` holds
untracked subjects.

META SCHEMA: all three validate against `knowledge/components/meta.schema.json`
(`jsonschema.validate`, the `behaviourAddress` branch — the `script` key is the
discriminator) — `SCHEMA OK` each.

THE CHECK IS NOW LIVE — the proof the snippet runs cannot give. Run against a composed page
that splices two of the three:

    python3 knowledge/_validate_receipt.py outputs/baseline-246/arm-B-sighted/dashboard.html

    FAIL:BEHAVIOUR-NOT-LOADED — `data-grid-symbols`: meta …/data-grid.meta.json declares
      script `knowledge/snippets/Data-grid.reference.html#script`, and the page does not
      load it — the page carries 6 inline executable script(s), none hashing to
      Data-grid#script[0] (17603 bytes)
    ✅ filter-toolbar-bar-symbols … behaviour …#script LOADED-EXTENDED (page script #3
      matches Filter-toolbar-bar#script[0] AFTER whitespace normalisation — the bytes moved;
      …) · NOTE:AUTHORED-JS (s258-D1)

Before this lane both regions reported `meta:NONE` and an UNPROVEN line. The page's overall
verdict does not move (it was already FAIL on `template-dashboard-bento`'s `dp08-anchor`
partial, another lane's subject), but the data-grid region goes from unmeasured to measured
and named — which is the whole point of finding 2.

## Still untyped and still scripted — LISTED, NOT FIXED

51 metas have no `behaviour` key while their snippet ships >1,000 bytes of inline script.
Top 20 by script bytes:

| slug | script bytes | | slug | script bytes |
|---|---|---|---|---|
| app-shell-split | 9,282 | | tags-input | 4,392 |
| video-player | 9,107 | | app-shell-side-nav | 4,124 |
| cascader | 7,540 | | tabs | 4,011 |
| template-wizard | 7,111 | | combobox | 3,866 |
| template-auth | 6,997 | | payment-card-visual | 3,624 |
| navigations | 6,388 | | timeline | 3,527 |
| splitter | 5,733 | | app-shell-doormat | 3,521 |
| template-create-edit | 5,168 | | app-shell-top-nav | 3,466 |
| multi-select | 4,842 | | page-header-lockup | 3,391 |
| standing-order-mandate-row | 4,650 | | transfer-list | 3,389 |

The remaining 31 run from `pagination` (3,297) down to `list-items` (1,164). Note that
several of these — the `app-shell-*` family and `tags` — are OTHER LANES' subjects this
session and were deliberately left alone.

## Undone

- Running `_validate_screen.py` WRITES `knowledge/_screen-gate/<name>.reference.md` for its
  subject. Three such files (Data-grid, Filter-toolbar-bar, Sidebar-nav) were created by the
  before-run and could not be removed — the sandbox refuses deletion under that path. They
  are untracked; someone with delete rights should clear them, and the lane brief's "write
  nothing under `knowledge/_screen-gate/`" is not satisfiable while that gate is the
  instrument named for the job.
- The 51-meta backlog above is untouched by ruling — it is a list, not a fix.
- `fallback` and `$note` prose is derived from the snippets' own scripts and comments; none
  of the three was DRIVEN with JS off, so the fallback claims are CLAIMED, not PROVEN. Each
  `$note` carries a `$unproven` line saying so.
