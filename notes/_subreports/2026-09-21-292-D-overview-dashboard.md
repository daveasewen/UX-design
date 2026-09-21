# #292 lane D — the Overview dashboard is defined, and the first cold one-shot since 2 September has been run and measured

`COUNTS: definition regions 5 · pass conditions 9 · composition decisions 13 · gaps named 7 (1 new) · gates run 12 · measured figures 41 · ESTIMATE 0`

---

## WHAT LANDED

| Path | What it is |
|---|---|
| `notes/_lanes/292/D/overview-dashboard-definition.html` | **The definition.** One page: what an Overview dashboard is, who reads it, the five regions it must carry, what it is not, the components it composes from (every one named from the repo, with its path), the layout on the ruled bento grid, and **nine pass conditions for a one-shot** — four on composition-not-tracing, five on alignment/spacing/dimensions. Closes with five ruling-shaped questions. Nothing on it is ruled. |
| `notes/_lanes/292/D/overview-dashboard-oneshot-v1.html` | **The cold one-shot**, 522 lines. Composed, not traced. 13 numbered decisions written into the page's own comments, each carrying the ruling, principle or token it rests on; 7 gaps flagged in place rather than invented over. |
| `notes/_lanes/292/D/overview-dashboard-oneshot-v1.png` | Light \| dark side by side, 1440 wide, ×2 device pixel ratio. |
| `notes/_lanes/292/D/overview-dashboard-oneshot-v1-light.png` · `-dark.png` | The two full-page renders separately. |
| `notes/_lanes/292/D/measured.json` | Every number below, machine-written, both themes. |
| `notes/_lanes/292/D/shoot.py` | The render + measure harness. Re-runnable; see REPLAY-THESE. |
| `knowledge/_screen-gate/overview-dashboard-oneshot-v1.md` | ⚠ **Written by `_validate_screen.py`, not by me** — the gate writes its verdict into the tree. Same behaviour as #288 lane P's stray `composed-dashboard.md`. Named here so it is committed with the work or removed deliberately, never swept in silently. |
| `outputs/syslibs/usr/lib/aarch64-linux-gnu/libXdamage.so.1` | ⚠ **`dpkg -x`'d at this seat** per `chromium-in-sandbox-recipe` — the only missing system lib. On the mount, so it survives a VM rebuild. Untracked; the conductor decides whether it is committed or ignored. |

**COLD, and here is what that means precisely.** The dashboard template (`knowledge/components/template-dashboard-bento.meta.json`, `showroom/template-dashboard-bento.html`, the `:where(.cn-template-dashboard-bento)` block in canon.css) was **not opened at this seat**, and neither was **#288 lane P's composed page** — so this is not a re-trace of the previous probe either. What *was* read: `knowledge/canon/canon.css` (the bento block 1078–1202, the BASE block, the alias block, the `.cn-kpi-tile` / `.cn-table` / `.cn-cards` / `.cn-card-header-lockup` / `.cn-chart-bar` scopes), `knowledge/canon/type.css`, `dv-render.js` and `dv-behaviour.js` headers, `knowledge/tokens/layout.json`, `knowledge/_rulings.json` (full `says` for s217-D2, s217-D3, s219-D1, s245-D8, s247-D3, s247-D4, s249-D2, s249-D5, s251-D1), `knowledge/_render/role_defaults_219.py --table`, `knowledge/_render/_bento_edit_rails.json`, nine `knowledge/snippets/*.reference.html`, and `reviews/DASHBOARD-PRINCIPLES-2026-09-05-v1.html`. #288 lane P's **subreport and DECISIONS.md** were read — they are the lane record of what the *system* measured, and its ten gaps are the reason four of them did not have to be rediscovered by hand.

**The brief used** is #288's, verbatim, so the two cold runs are comparable: *"Build an operations dashboard for a bank's Chief AI Officer: AI programmes in flight, their spend against budget, efficiency gains realised, risk and compliance exceptions, and what needs a decision this week. Desktop first, 1440 wide."* ⚠ The frozen demo prompt was **not recoverable at #288 and was not searched for again here** — that gap stands.

---

## MEASURED

All figures are read from the **live DOM** at 1440×1000, ×2, headless Chromium 153, both themes, unless stated. The probe is `notes/_lanes/292/D/shoot.py`; the raw output is `measured.json`. Nothing below is estimated.

### A · The wall — alignment, spacing, dimensions

| Reading | Light | Dark | Ruled value | Verdict |
|---|---|---|---|---|
| Outer wall computed `column-gap` / `row-gap` | **40px / 40px** | 40px / 40px | mainSpacing 40, mono (s219-D1(5)) | ✅ |
| Inner wall computed `column-gap` / `row-gap` | **4px / 4px** | 4px / 4px | subSpacing 4, mono (s219-D1(5)) | ✅ |
| Outer wall columns (`grid-template-columns` count) | **6** | 6 | 6 (s217-D2) | ✅ |
| Outer wall `grid-auto-rows` | **320px** | 320px | 320px (s217-D2) | ✅ |
| Inner wall `grid-auto-rows` | **minmax(320px, auto)** | same | the FLOOR model (s245-D8, "Okay it's 2") | ✅ |
| Inner wall `--bento-cols-now` | **5** | 5 | per-instance override sanctioned by `layout/bento/columns.$note` | ✅ |
| Outer wall `overflow` / `padding` | hidden / 0px | same | canon | ✅ |
| Bento spacing dials authored in the page | **4px, 40px** | — | stop set {1,2,4,16,24,40} (s219-D1(4)) | ✅ 2 of 2 on a stop |
| All other spacing authored in the page | 8px, 12px, 16px, 40px | — | component idiom (canon itself uses 8 and 12) | ⚠ see note |
| Off-grid layout dimensions (`_validate_grid.py`) | **0** | — | 4px grid | ✅ after one repair |

⚠ **The stop-set condition needed narrowing, and it was narrowed before it was scored, not after.** The first draft of pass condition P6 said *every* authored spacing value must be on the stop set. Measured, the page authors 8px and 12px inside its own list rows — values canon itself uses throughout. The stop set is scoped by its own source (`_bento_edit_rails.json` → `rail.spacing_stops`, "the edit pass picks among stops") to the **bento edit-pass vocabulary**, so P6 now reads on the dials and the two numbers are reported separately. Both are in the definition; neither is hidden.

**One real repair, found by a gate and not by eye:** `_validate_grid.py` failed the page on `max-height: 238px` — *"not a 4px multiple"*. Corrected to 240px (and the chart's authored height from 234 to 236). The gate then passed. **That is a measurement doing work the eye did not do.**

### B · Geometry — every band closes, nothing is clipped

| Reading | Value |
|---|---|
| Top-level tiles × spans | 6 tiles: `c6 r1` · `c4 r2` · `c2 r2` · `c2 r2` · `c4 r1` · `c4 r1` |
| Per-row column sums, **counting row-spans on both rows** | rows 0–4 = **6, 6, 6, 6, 6** |
| **Orphan cells** | **0** (DP-16, s249-D5 "No ragged layouts") |
| Distinct left edges of top-level tiles | **3** — 40, 507, 973 |
| Distinct right edges | **3** — 467, 933, 1400 |
| Tile widths | 1360 (c6) · 893 (c4) · 427 (c2) |
| Tile heights | 320 (r1) · 680 (r2) — i.e. exactly 2×320 + one 40px gutter |
| KPI cards: distinct widths / heights / tops | **1 / 1 / 1** — 269px, 320px, y=282. Five cards, one row, no ragged edge. |
| **Clipped boxes** (overflow-y hidden|clip with content taller than the box, excluding inline runs and sr-only) | **0**, both themes |
| Document height × width | **1440 × 2082** |
| Uncaught page errors + console errors | **0**, both themes |

**Dead ground inside each tile** — the gap in px between the lowest painted content and the bottom of the surface it sits on. This is the "dimensions" reading, and it is the page's weakest number:

| Tile | Dead ground |
|---|---|
| Headline metrics wall (c6 r1) | **17px** |
| Programme portfolio (c4 r2) | **22px** |
| Needs attention (c2 r2) | **187px** |
| Open exceptions (c2 r2) | **153px** |
| Spend chart (c4 r1) | **13px** |
| Gains chart (c4 r1) | **23px** |

**The mechanism, measured, not guessed.** The outer wall's rows are `grid-auto-rows: 320px` — **fixed**. The `minmax(<unit>, auto)` floor that lets a row grow to its own content (s245-D8) is declared only on `.c-bento__tile.c-bento > .c-bento__grid`, i.e. on **nested** walls. So a top-level tile is 320 or 680px tall whatever it holds, and DP-18's *"a tile is sized to its content's floor and never stretched to a neighbour's height"* is **unreachable on the outer wall of a dashboard**. The two two-row panels are where the slack lands. Content was pushed up to the ceiling the rules allow — the portfolio table lists all eleven programmes because the headline metric says eleven, and the attention region carries six items because DP-11 caps it at six — and **340px of dead ground across two tiles is what remains after doing that.** It is not a composition mistake; it is the row unit.

### C · Materials — composed, not traced

| Reading | This page | #288 traced page | #288 composed page |
|---|---|---|---|
| Distinct canon component scopes (`.cn-*`) in the DOM | **12** | 0 | 11 |
| `.c-bento` instances | 2 | 4 | 3 |
| `.c-bento__tile` total | 11 | 10 | 12 |
| Outer gutter | 40px / 40px | 40px / 40px | 40px / 40px |
| Document height | 2082 | 1197 | 2016 |
| Custom properties the page's own CSS references | 4 | 82 | 23 |
| …unresolved | **0** | 73 of 82 | 3 of 23 |
| Raw hex in the page's own declarations | **0** | — | — |
| Theme carriers on the root | `class="canon"` + `data-theme` | `data-theme` + inert `data-apollo-theme="mono"` | `class="canon"` + `data-theme` |

The twelve components: `cn-button · cn-card-header-lockup · cn-cards · cn-chart-bar · cn-chart-line · cn-kpi-tile · cn-legend · cn-list-items · cn-page-header-lockup · cn-status-indicator · cn-table · cn-tags`. Charts are driven by `window.dvRender(figure, spec)` — **12 bar marks** on the grouped column and **36 elements** on the line, both from data, none hand-authored. Both figures ship a real `<table>` spine (dv-005). The `.dv-animate` entry class the snippets ship with is deliberately unused (DP-23).

### D · The two themes

| Reading | Light | Dark |
|---|---|---|
| Page ground (computed on `<html>`) | **rgb(240,240,240)** | **rgb(35,35,35)** |
| Card surface | rgb(255,255,255) | rgb(31,31,31) |
| Card border | rgb(225,225,225) | rgb(128,128,128) |
| Ground-to-surface separation | **15 levels** | **4 levels, and inverted** |

⛔ **In dark the ruled grey page ground is LIGHTER than the card that sits on it.** The card is the "raised" surface and it is four levels *darker* than its canvas. This is the direct consequence of gap G1 — there is no semantic grey-page role in the store, so `--page` was bound to `--surface-hover` (`--tertiary-background-hover`), whose dark value is 35 while `--tertiary-background-default` is 31. Ruling s219-D1 left **the dark page ground expressly open**; this is what the open question looks like on a rendered page.

⚠ **And the borrow does not land in dark by itself.** Measured: with only `--page` re-bound, a child element resolving `var(--page)` painted rgb(35,35,35) while `<html>` itself painted rgb(26,26,26) — `--background-default`, not the grey. `background:var(--page)` had to be **re-declared** on `.canon` in the page's own stylesheet for the ruled ground to appear at all. Reproduced in both directions at this seat. Cause not established from this seat; the reading is.

### E · Gates — what ran, what said what, and what could not see this page

| Gate | Verdict, verbatim where short |
|---|---|
| `_validate_screen.py <path>` | **`verdict: PASS ✅`** · receipt ✅ 0 regions re-hashed and matched · compose ✅ · composition UNPROVEN: C9 bands · icon-source ✅ all paths library-matched · a11y ✅ |
| …its index step | ⛔ `SCREEN-GATE INDEX REFUSED — a generated index may not be built from state a clone cannot see. untracked subject: _screen-gate/overview-dashboard-oneshot-v1.md` (identical refusal to #288) |
| `_validate_composition.py <path>` | `UNPROVEN: the artefact declares neither a base column count nor any @container band; C9 cannot read its grammar` · `C9 reds 0 [BLOCKING] · C1 0 · C7 0 · C8 0 · C4 0 [advisory] · unproven 1` |
| `_validate_grid.py <path>` | **FAIL** first (`off-grid: max-height: 238px — not a 4px multiple`), **`GRID GATE PASS`** after the repair |
| `_validate_compose.py <path>` | `RESULT: PASS ✅` — **but about 7 other screens.** It ignores the path argument. Recorded so the green is never read as evidence here (#288's G10, unchanged) |
| `_validate_dataviz.py <path>` | `✅ DataViz gate passed (15 chart surface file(s))` — **the 15 are `knowledge/snippets/Chart-*.reference.html`, not this page.** It discovers its own corpus |
| `_validate_a11y.py <path>` | `137 snippet(s), 0 failure(s)` — again its own corpus, not this page. The a11y check that DID read this page is the one inside `_validate_screen.py`: ✅ |
| `_validate_no_hardcode.py` · `_validate_radius.py` · `_validate_dark_surfaces.py` · `_validate_palette_tier.py` · `_gate_inline_style_parse.py` · `_validate_hidden_display.py` | All pass / advisory, **all on their own fixed corpora** — none of them read this page |
| `_validate_hit_area.py <path>` | ⛔ `COULD-NOT-ASK: HIT-AREA: HARNESS UNAVAILABLE — no chromium headless_shell found`. **Its executable globs cover `chrome-headless-shell-linux64/` and not the aarch64 layout this sandbox installs, `chrome-headless-shell-linux-arm64/`.** Chromium launched fine for every other measurement in this report from the same cache. **This is a gate that cannot see an arm64 seat, not a pass and not a fail.** |
| `_validate_fit_physics.py <path>` | Takes `--targets`, not a bare path; **not run** rather than run wrongly |

**So: of twelve gates invoked, exactly three read this artefact** — `_validate_screen.py` (PASS), `_validate_composition.py` (UNPROVEN) and `_validate_grid.py` (FAIL, then PASS). Everything else scans a corpus it discovers for itself.

⛔ **The orphan-cell arithmetic cannot be gated on this page and will not be until something changes.** `_validate_composition.py` reads column counts and band clamps from the artefact's **own inline `@container` blocks**; a page that *links* `canon.css` restates none of them, so C9 returns UNPROVEN. **The 0-orphan reading in section B is from the bespoke DOM probe in `shoot.py`, not from a gate.** This is #288's G9, one session older and unmoved — and it means the one rule Dave stated most plainly ("No ragged layouts") is the one rule no instrument in the tree can check on a composed page.

⛔ **The provenance receipt attests to nothing here, and the reason matters.** `gen_provenance_receipt.py --mint` produced `"regions": []`, because the receipt hashes **APOLLO-SPLICE regions** — bytes copied out of a snippet into a page. A page that was *composed* has no spliced regions to hash. The gate then reports `✅ 0 region(s) re-hashed and matched`, which is a true statement about nothing. **The receipt machinery proves tracing. It has no reading for composition.**

### F · New gap found by measuring

**G11 — `dv-behaviour.slackBelow()` measures the TILE, not the figure's own surface, and a dashboard chart always has one in between.** `figure.dv` ships no surface of its own (canon: `:where(.cn-chart-bar) figure.dv{margin:0; position:relative}`), so every chart on a bento wall sits inside a card. The fit pass then offers the canvas the card's padding as slack and grows into it. **Measured before the pin: the canvas overshot its box by 33px (grouped column) and 71px (line), and `overflow:hidden` on the bento swallowed both — no DOM symptom, no console warning, `pageErrors: []`.** Answered with fitHeight's own documented escape (a CSS pin makes the grow fail its 1px check and the engine keeps the authored height). #288's G3, G7 and G8 were all re-encountered and all held; G1, G2, G4 and G6 were designed around and flagged in the page.

---

## RULING-SHAPED QUESTIONS

Nine. None of them was decided here, and none of them can be.

1. **Do the draft dashboard principles become the standard?** DP-01…29 at `reviews/DASHBOARD-PRINCIPLES-2026-09-05-v1.html` are unruled and the page says so on its own face — yet the definition and every grade in it rest on them. Adopt as a set, adopt selectively, or leave advisory and let the definition stand alone.
2. **Are the five regions a requirement or a recommendation?** Is a page without an attention strip *not an Overview dashboard*, or merely unusual?
3. **The dark page ground.** Measured: the ruled grey canvas is four levels lighter than the card sitting on it, so figure and ground invert in dark. s219-D1 left this expressly open. Does the dashboard get a dark ground of its own, or does the card get a lighter surface?
4. **A semantic grey-page token.** `pageBg=grey` is ruled and no role in the store means it; today it borrows `--surface-hover`, and it had to be re-declared by hand to land at all. Mint `background/app-canvas`, or keep borrowing and write the borrow down?
5. **The 320px row unit against DP-18.** The outer wall's rows are fixed, so a tile cannot be sized to its content and 340px of dead ground across two panels is the arithmetic, not a mistake. Does the row unit gain a per-instance dial (it has none, unlike columns), or does the dead ground stand as the cost of a regular wall?
6. **Two missing components.** There is still no needs-attention organism (DP-10) and no attention-strip component (s251-D1 calls the strip "a good pattern"). Both are hand-composed on every dashboard. Mint them, or keep composing?
7. **Polarity on a KPI.** DP-22 wants every metric to declare which direction is *good*; canon's only carrier is `data-trend`, which is arithmetic. Here the one red on the page had to ride the tile's error note instead of its arrow. DP-25's `data-signal` is open and this page hit the gap head-on.
8. **The receipt, and what "provenance" means for a composed page.** The receipt hashes spliced regions and this page has none, so a green receipt is a true statement about nothing. Either composition gets a provenance form of its own, or a composed page is honestly receipt-less and the gate should say so louder.
9. **Whether nine conditions and a PASS is enough for the 25th** — or whether the bar is your eye and these are only the floor.

Two further things are yours but are not questions about the design: the **stray gate output** `knowledge/_screen-gate/overview-dashboard-oneshot-v1.md`, and the **`outputs/syslibs/` lib** — both are untracked writes this lane made and both are named above rather than swept in.

---

## REPLAY-THESE

```bash
cd <MOUNT>/UX-design

# 0 · chromium in the sandbox — ONE bash call, nothing survives a call boundary
pip install playwright --break-system-packages
export NODE_TLS_REJECT_UNAUTHORIZED=0 NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
export TMPDIR=/dev/shm
python3 -m playwright install chromium-headless-shell     # non-zero exit on host-requirements is EXPECTED
cd /dev/shm && apt-get download libxdamage1 && dpkg -x "$(ls libxdamage1*.deb)" <MOUNT>/UX-design/outputs/syslibs

# 1 · render both themes and measure  (re-export in EVERY call)
cd <MOUNT>/UX-design
export TMPDIR=/dev/shm
export LD_LIBRARY_PATH=<MOUNT>/UX-design/outputs/syslibs/usr/lib/aarch64-linux-gnu
python3 notes/_lanes/292/D/shoot.py          # → 3 PNGs + measured.json

# 2 · the three gates that actually read this page
P=notes/_lanes/292/D/overview-dashboard-oneshot-v1.html
python3 knowledge/_validate_grid.py        "$P"
python3 knowledge/_validate_composition.py "$P"
python3 knowledge/gen_provenance_receipt.py --mint "$P"
python3 knowledge/_validate_screen.py      "$P"
cat knowledge/_screen-gate/overview-dashboard-oneshot-v1.md

# 3 · the gates that DO NOT read it — run them to see for yourself
python3 knowledge/_validate_compose.py "$P"    # PASS, about seven other screens
python3 knowledge/_validate_dataviz.py "$P"    # PASS, about 15 snippet files
python3 knowledge/_validate_a11y.py    "$P"    # 137 snippets, not this page
export PLAYWRIGHT_BROWSERS_PATH=$HOME/.cache/ms-playwright
python3 knowledge/_validate_hit_area.py "$P"   # COULD-NOT-ASK on aarch64

# 4 · the rules the definition cites
python3 knowledge/_render/role_defaults_219.py --table
python3 -c "import json;d=json.load(open('knowledge/_rulings.json'));print(d)" | head -c 0   # use the repo's own query path
sed -n '1078,1202p' knowledge/canon/canon.css
```

---

*Lane D of #292. The definition is `notes/_lanes/292/D/overview-dashboard-definition.html`; the composition decisions are written into `overview-dashboard-oneshot-v1.html`'s own comments, thirteen of them, each with its citation. Nothing in this report is ruled and nothing in it was decided on Dave's behalf.*
