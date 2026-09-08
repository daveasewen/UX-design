# #260 lane A — DRIVEN RECEIPTS BECOME THE GATE (`s260-D3`) · subreport

**The red is discharged by measurement, not by weakening the rule.** `Chart-donut.reference.html`'s
spider canvas is drawn at runtime by `dvRender()`, so dv-004 had nothing to read and failed safe.
It now grades through a COMMITTED Playwright receipt: **2.109px** of real separation, measured off
the drawn path in **all 8 theme × mode combinations**, tied to the sha256 of every file the test
page loads. The static route is untouched for every chart that still carries its marks.

Ruling enacted verbatim (`knowledge/_rulings.json` entry 406, Dave, 2026-09-08):

> "DRIVEN RECEIPTS BECOME THE GATE FOR ENGINE-DRAWN CHARTS. Where a dataviz rule reads static
> geometry (dv-004 and its siblings) and the chart is drawn at runtime by
> `knowledge/canon/dv-render.js`, `_validate_dataviz` accepts a COMMITTED driven receipt (a
> Playwright measurement recorded from `knowledge/_tests/chart-engine/`) as the evidence for that
> rule — the gate is 'static OR driven', never skipped. Option (b), an engine-emitted self-report
> marker trusted by the static gate, is REFUSED."

Option (b) was not built. Nothing in the receipt is a claim the engine makes about itself: every
number is a measurement a browser made of the geometry it drew.

---

## 1 · `knowledge/_drive_chart_engine.py` — the committed driver

Runs Chromium **151.0.7922.34** headless via Playwright, `goto("file://…")` (never `set_content`),
over all six `knowledge/_tests/chart-engine/*.html` × 4 themes (mono, legacy, console, supercharge)
× 2 modes (light, dark) = **48 page loads**. Writes `knowledge/_tests/chart-engine/_receipts.json`
(sorted keys, `indent=1`, floats rounded to 3dp — the diff is readable).

**What it records, per page:** `sources` (sha256 of the test page AND of every local file it loads —
each `<script src>` and `<link href>` resolved on disk, 8 files for `donut.html`), `driven` ISO
timestamp, `chromium` version, and per combo: pageerror count + texts, console-error count + texts,
per-`figure.dv` dtype / mark count / table-row count / dv-004 px, and the filter result.

**How dv-004 is measured — from the DRAWN path, never from `data-a1`/`data-a2`.** Each mark is
sampled with `getPointAtLength` (1600 samples); the centre and outer radius come from the union
bounding box of the drawn marks. The reference radius is the ring's **inner edge** (the narrow one,
`r = ri`, measured at **59.95** for the donut) or, for a pie which has no inner edge, the same
`0.35·ro` the type partial itself uses (measured **35.02**). Candidate pairs are taken over ALL
pairs of segments (so adjacency and the wrap-around pair need no special case — the minimum is the
answer), then **refined by band-constrained coordinate descent** on the two arc-length parameters.
The refinement matters: coarse sampling alone read 2.113px and drifted in the third decimal; refined,
the figure is **identical to 3dp across all 8 combos and across separate runs**. A rect stack is
measured as the gap between adjacent `getBBox()` rects within a column (no engine page draws one
yet — the code path is there for the first that does).

`--check` re-hashes the recorded sources and prints FRESH/STALE per page, plus MISSING for a test
page with no receipt at all. `--help` (argparse, so `_validate_help_gate` is satisfied) opens by
naming the consumer — this instrument is not a zombie: `_validate_dataviz.py` reads its output.

### Measured, `mono/light` (identical in the other seven combos)

| page | pageerrors / console errors | figures | dv-004 |
|---|---|---|---|
| `bar.html` | 0 / 0 | `fig-bar` bar 9 marks · `fig-column` column 9 · `fig-grouped` grouped-column 24 | n/a (not a gapless surface) |
| `combo.html` | 0 / 0 | `fig-combo` combo 13 · `fig-shared` combo 25 | n/a |
| `donut.html` | 0 / 0 | `fig-donut` donut 5 · `fig-pie` pie 5 | **2.109px** / **2.108px** |
| `line.html` | 0 / 0 | `fig-line` line 1 · `fig-multi` multiline 3 | n/a |
| `sparkline.html` | 0 / 0 | four spark figures, 2+2+2+4 marks | n/a |
| `stacked-area.html` | 0 / 0 | `fig-stack` stacked-area 3 | n/a |

**Zero pageerrors and zero console errors in 48/48 combinations**, on load and after a re-render.

### Filter (rule 14), driven per combo

| page | unticked | marks | table rows |
|---|---|---|---|
| `bar.html` | Groceries | 42 → 40 | 26 → 24 |
| `combo.html` | Jan | 38 → 35 | 24 → 22 |
| `donut.html` | Housing | 10 → 8 | 10 → 8 |
| `line.html` | Jan | 4 → 4 | 24 → 22 |
| `stacked-area.html` | Q1 24 | 3 → 3 | 10 → 9 |
| `sparkline.html` | — | 10 → 10 | 48 → 48 |

Recorded honestly rather than smoothed: `line.html` and `stacked-area.html` filter **categories**,
so a line/area chart keeps one mark per series and only the table rows move — the receipt carries
`moved_marks:false, moved_rows:true` and the note names the category unticked. `sparkline.html` has
a `#filter` fieldset with **no checkbox** at all, so the driver records `driven:false` with the
reason in the note instead of inventing a result. See §5, item 2.

---

## 2 · `knowledge/_validate_dataviz.py` — the gate reads the receipt

In the dv-004 branch and nowhere else. A chart takes the driven route only when it is
**ENGINE-DRAWN**: no `.dv-series` mark inside the figure's markup AND the file drives the engine
(`dvRender(` or a `dv-render` load). Everything else keeps the static path byte-for-byte —
the stroke mechanism and the `_rect_stack_gap` geometry mechanism are unchanged.

`ENGINE_TEST_PAGE` maps snippet basename → test page explicitly (7 entries), because a mapping you
can read is a mapping a reviewer can falsify.

**The route is never a skip.** Every one of these is BLOCKING and names its remedy
(`python3 knowledge/_drive_chart_engine.py`):

1. no `_receipts.json` at all;
2. the snippet is not in `ENGINE_TEST_PAGE`;
3. the mapped page has no receipt;
4. any recorded source hash no longer matches the bytes on disk — **the message names the stale
   file**;
5. fewer than the recorded themes × modes combinations;
6. no figure of this dtype measured in some combo;
7. any measured figure `< 2.0px` — **the message quotes the combo and the px**.

On a pass it says so, in the gate report, with the number and the route:

```
- ⚠ donut#cd1 — dv-004: PASSED by driven receipt — donut.html/fig-donut measured 2.109px
  (worst of 8 measurements across 8 theme x mode combos, rule >=2.0px),
  driven 2026-09-08T18:01:19Z on Chromium 151.0.7922.34.
  Source: knowledge/_tests/chart-engine/_receipts.json
```

Both the pass and the fail text carry the words **"driven receipt"** and the px, so a reader can
see which route graded the chart without opening the source.

---

## 3 · Selftest bites (`_validate_dataviz.py --selftest`)

The repo uses `--selftest` for this validator (`knowledge/_tests/test_gates.py` does not exercise
`_validate_dataviz` at all — grep for "dataviz" there returns nothing), so the bites went there.
Six new cases, each on a throwaway tree — the bite-test touches no repo file:

| bite | result |
|---|---|
| fresh + all 8 combos ≥2px **PASSES** and says "driven receipt" + "2.109px" | ok |
| ONE combo at **1.9px** is BLOCKING, quoting `console/dark` and `1.900px` | ok |
| **STALE** source hash is BLOCKING, names `dv-render-donut.js` and the drive command | ok |
| **NO receipt at all** is BLOCKING (never a skip) | ok |
| an **UNMAPPED** engine snippet is BLOCKING | ok |
| **CONTROL** — a static donut with a ≥2px stroke still passes the STATIC route, and no "driven receipt" text appears | ok |

All 34 selftest cases green.

---

## 4 · MUTATION TEST — the thing was driven, not asserted

`knowledge/canon/dv-render-donut.js` line 89, the one line that sets the dv-004 angular cut:

```
-    var gap = ctx.GAP / (ri || ro * 0.35) / RAD;
+    var gap = 1.6   / (ri || ro * 0.35) / RAD;
```

| step | result |
|---|---|
| mutate, gate WITHOUT re-driving | RED — `dv-004: the driven receipt for donut.html is STALE — knowledge/canon/dv-render-donut.js has changed since it was driven.` `--check` reports `[STALE] donut.html` and names the same file. |
| re-drive with the mutation in place | receipt records **1.600px** (`fig-donut`) and **1.553px** (`fig-pie`), identical in all 8 combos, still 0 pageerrors |
| gate | **RED** — `dv-004: driven receipt FAILS — donut.html/fig-donut measured 1.600px of separation in combo console/dark (rule is >=2.0px).` |
| `git checkout -- knowledge/canon/dv-render-donut.js` | md5 back to `b4ee7268efde0d7e02a2c757569db0d9`, **byte-identical to the pre-mutation file** |
| re-drive | **2.109px / 2.108px**, the same numbers as before the mutation — the measurement is deterministic |
| gate | **GREEN** |

The mutation discriminates in **two** places, not one: the freshness leg fired before the drive, the
threshold leg fired after it. A receipt that could be left stale would have been a rubber stamp.

---

## 5 · Ruling-shaped, found but NOT decided — Dave's, named

1. **The drawn gap is 2.109px, not the 2.2px the engine intends — `n1()` rounding eats ~0.09px.**
   `dv-render.js` sets `GAP = 2.2`, and `dv-render-donut.js` cuts each slice by `GAP/ri` radians, so
   the *intended* separation is 2.200px at the inner edge. The emitted path coordinates are rounded
   to **one decimal** by `n1()`, and the geometry that actually reaches the screen measures
   **2.109px**. The rule is ≥2px, so the margin is **0.108px** — real, but thinner than anyone has
   been told. #259's subreport reports 2.199px because it computed from the `data-a1`/`data-a2`
   attributes (the ideal), not from the drawn `d` (the truth). ⚠ **Dave's call, not mine:** whether
   `GAP` should be raised (2.4 would restore a comfortable margin), whether `n1` should emit two
   decimals on radial paths, or whether 0.108px of headroom is simply accepted and recorded.
2. **`sparkline.html` has a `#filter` fieldset with nothing in it to drive.** The receipt records
   `driven:false` and the reason, rather than a false green. Whether that page owes a real filter
   control (rule 14 says a filter re-renders; a sparkline may legitimately have none) is a question
   about the TEST PAGE's obligations, not about this gate. Not decided here.
3. **The driven route currently covers dv-004 only.** The ruling says "dv-004 **and its siblings**".
   The other blocking rules that read geometry or resolved colour on an engine-drawn chart
   (dv-016 rendered contrast, dv-017 palette-only fills, dv-009 flat fills, dv-line-011 straight
   lines) are today evaluated against markup that, on an emptied canvas, contains nothing — so they
   pass **vacuously**, silently. That is the same defect class one rule over. The receipt already
   carries the mark counts that would anchor them. ⚠ Extending the driven route to those rules is a
   scope decision — flagged, not taken.
4. **`Chart-bar`, `Chart-line`, `Chart-combo`, `Chart-sparkline`, `Chart-stacked-area` are mapped
   but not yet exercised**, because none of their dtypes is in dv-004's gapless set. The mapping is
   committed so that the day one of them is emptied, the gate finds a receipt instead of a hole.

## 6 · What I could NOT do — first obstacle, named

**`knowledge/_tests/test_gates.py` cannot run in this sandbox, for a reason that predates this
lane.** It `copytree`s the whole of `knowledge/` (**5.3 GB**, font binaries included) into a temp
dir; the session volume has **1.7 GB** free, so the control copy dies with `[Errno 28] No space
left on device` before a single validator runs. This is environmental and is not caused by anything
in this lane — it is [[gate-cannot-pass-in-one-environment]]. The five gates in the lane brief all
run and are green.

**`_validate_help_gate.py` is RED on one file, and it is not mine:**
`knowledge/_tmp/wrap258/carry259.py` has no help gate. `_drive_chart_engine.py` is clean (argparse
owns `--help`). Left alone — it is a wrap artefact from #258/#259, not this lane's to move.

## 7 · Gate results

| gate | result |
|---|---|
| `python3 knowledge/_validate_dataviz.py` | ✅ 15 chart surface files, 0 blocking (was 1 blocking on `Chart-donut`) |
| `python3 knowledge/_validate_dataviz.py --selftest` | ✅ 34 bites, 6 of them new |
| `python3 knowledge/_validate_behaviour.py` | ✅ |
| `python3 knowledge/gen_component_partials.py --check` | ✅ all AUTO-PARTIAL blocks in sync |
| `python3 knowledge/canon/gen_canon_components.py --check` | ✅ 136 components in sync |
| `python3 knowledge/_drive_chart_engine.py --check` | ✅ all 6 receipts FRESH |

`_build_all.py`, `gen_showroom.py` and `_validate_screen.py` were NOT run, per the lane brief.
`GOOD-MORNING.md`, `_LIVE-STATE.md`, `_CARRIES.md`, `_rulings.json` and the memory files were not
touched. The only `git checkout` in this lane is the single mutation restore recorded in §4.

## 8 · Reproducing the drive

Playwright had to be installed fresh (`pip install playwright --break-system-packages`), and
`python3 -m playwright install chromium` fails on this sandbox with
`UNABLE_TO_GET_ISSUER_CERT_LOCALLY` until `NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt`
is exported. The libXdamage obstacle from #259 is unchanged and resolved the same way:
`apt-get download` the runtime `.deb`s, `dpkg-deb -x` them into `/tmp/pwlibs/root`, export
`LD_LIBRARY_PATH`. The driver honours `APOLLO_PW_LD_LIBRARY_PATH` so the prefix can be set once in
the environment rather than remembered at each call. All of this is written into the script's
`--help`, so the next session does not have to find this file to re-drive.
