# #261 C — the #260 core requests, classified and the cheap ones LANDED

**⚠ PREMISE CORRECTED FIRST.** The lane brief says *seven* collated core requests. There are
**seven lane FRAGMENT FILES** in `notes/_lanes/260/`; `_CORE-REQUESTS-collated.md` de-duplicates
them into **ELEVEN** requests — **nine** against the core (`A1–A9`), one against a type partial
(`B1`), one against a gate (`C1`, already done by #260 I). All eleven are classified below.

## The table

| # | the request (quoted, ≤25 words) | class | outcome | why | receipt | commit |
|---|---|---|---|---|---|---|
| A1 | *"Let a type opt out of (or dial down) the cartesian furniture"* — `fn.furniture=false` / `fn.axis="none"`, F1 wants a third position `'axis'` | CHEAP | **LANDED** | 5 reporters, no ruling, default true ⇒ no shipped chart moves; 4 copies of `ctx.out.length=0` replaced | `notes/_lanes/261C-probe-a1.py` — default grid 5/tick 5, `"axis"` 0/5, `false` 0/0, marks 4 throughout | `c582678` |
| A2 | *"Scope the ZERO CLAMP to the types that own it"* — `fn.zeroBaseline !== false`, or clamp only where the engine is guessing | CHEAP | **LANDED** | dv-bar-009 IS a bar rule and `_validate_dataviz` already scopes to `BAR_FAMILY`; the core was broader than the ruled rule. Default true, **no type opts out today** | `261C-probe-a2.py` — same spec: clamped axis 0–150, `zeroBaseline:false` axis 90–110, default restored | `f84d691` |
| A3 | *"Let a series value be `null` and mean ABSENT"* — ragged data, ~60 code bytes across `validate`, `writeTable`, `autoLabel` | **DEFER** | deferred | the collated file names it *"spec-shaped as well as core-shaped"*: it changes the authored contract, and `writeTable` feeds two gates that read the table as data | — | — |
| A4 | *"The spec has no NUMERIC X"* — `categories` may be numbers, or the spec grows `x: […]`; the core then owns the x scale | **DEFER** | deferred | *"the big one"* — a second scale, a third `fn.axis` value and axis-2 furniture; far past 40 lines, and it re-shapes the ruled spec | — | — |
| A5 | *"`valueLabel` beside `categoryLabel`"* — the value axis has no name, the series name is doing two jobs | **DEFER** | deferred | not a lever: it adds FURNITURE nobody has placed. Where the label sits, how the plot pays for it, whether it rotates — design decisions, one reporter | — | — |
| A6 | *"A type cannot contribute to its own accessible name"* — `fn.label = fn(spec)` alongside `fn.axis`/`fn.domain`, or `ctx.setLabel(s)` | CHEAP | **LANDED** | 6 lines; the standing workaround MUTATES the caller's spec behind a private flag — *"nothing forbids and nothing sanctions"*. Authored `spec.label` still wins | `261C-probe-a6.py` — off: 48-phrase enumeration; `fn`: *"Sessions. 4 sessions, 90.41 to 108.52."*; authored wins | `c1b64c7` |
| A7 | *"A re-render never re-runs a type partial"* — re-call `draw(ctx)` past some width delta, or expose `dvRender.redraw(figure)` | CHEAP | **LANDED** | the second spelling is 8 lines and adds NO listener (ADR-0015 §4). The automatic width watcher is the half that was NOT taken | `261C-probe-a7.py` — partial runs: first 1 · after a resize **1** · after redraw **2**; un-rendered figure refuses | `0420197` |
| A8 | *"Furniture BEHIND a partial's own marks"* — one output buffer, pushed in order; an opting-out partial can only paint on top | **DEFER** | deferred | *"not needed today"* by its own reporter, and the fix re-orders the paint of EVERY chart in the group — every receipt would move for a 1px cosmetic | — | — |
| A9 | *"`fitOne` moves `g` not `circle`; `fitY` moves `circle` not `g`"* — one sentence in the core's grammar comment fixes it | CHEAP | **LANDED** | documentation only, and comments are FREE under the code-only unit (#250) — 0 bytes of budget | 27 receipts re-driven for the sha change; every measurement byte-identical | `7a6a1a1` |
| B1 | *"Emit radial path coordinates at TWO decimals"* in `dv-render-donut.js` — driven 2.109 → 2.194 | **DEFER** | deferred | not the core (out of this lane's fence), and ruling-shaped: the pie has no inner edge, so its 2.108 is judged at a **convention** (0.35·ro), not at the defect | — | — |
| C1 | `_validate_dataviz.ENGINE_TEST_PAGE` needs the new snippet→page mappings | n/a | **DONE at #260** | mapped by #260 I with a selftest bite; nothing owed | — | `1a1f516` |

## Bytes — and a finding about the budget

`dv-render.js` **9,309 → 9,779 code-only bytes** of 16,384 per source (+470, four changes).
**Chart-combo: 34,209 → 34,209 of 34,816 — UNMOVED, and it could not have moved.** `s260-D1`'s
`shared` list makes `_validate_behaviour` EXCLUDE the core from the member sum outright
(`w not in shared`), reporting it on its own line instead. So the 607 bytes of headroom the brief
priced were never at risk from engine work — engine growth is currently **free** against the page
budget as the gate measures it, though the browser still loads all of it. Ruling-shaped, recorded
here, not acted on.

## Gates, all green after the last commit

`_validate_dataviz.py` ✅ 15 chart surfaces · `_drive_chart_engine.py --check` ✅ **all 27 FRESH**
(Chromium 151.0.7922.34, arm64) · `_validate_behaviour.py` ✅ (Chart-combo 34,209 of 34,816) ·
`_validate_snippets.py` ✅ 137 snippets, 0 failures. Each landed request was re-driven and gated
in its own commit; the four mutation probes are committed beside them in `notes/_lanes/`.

## Obstacles, in the order met

1. **`gen_component_partials.py --check` cannot be green in this tree** — `Navigations.reference.html`
   carries a `#behaviour-manifest` block its meta does not type (the nav lane's, outside this fence).
   The generator also REWRITES `Sidebar-nav`/`Tab-bar`/`Navigations` on every run: restored with
   `git show HEAD:<path> > <path>` after each, and never staged.
2. **A full 27-page drive is ~178s and this sandbox caps a shell call near that**, with background
   processes killed at the end of the call. `--page` MERGES, so the drive splits into three calls
   (13 test pages, then the 14 snippets in two halves) and `--check` still reads all 27 FRESH.
   The probes need `LD_LIBRARY_PATH` set by hand; only the driver honours `APOLLO_PW_LD_LIBRARY_PATH`.
3. `showroom/chart-donut.html` and `chart-pie.html` were already dirty when this lane opened
   (an uncommitted regeneration from an earlier lane) — absorbed into C1, stated in its message.
