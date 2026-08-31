# Sub-report — #231 lane W-326: the dashboard-bento snippet

**Brief:** `notes/_briefs/2026-08-31-231-bento-snippet-brief.md` · **Row:** W-326 · **Model:** Opus (sub)
**Decision surface for Dave:** `reviews/BENTO-SNIPPET-2026-08-31-v1.html` (light + dark, four themes,
four responsive bands, two AWAITING-DAVE reading sets).

---

## COUNTS — every figure below was copied off a probe, none typed from belief

| what | figure | probe |
|---|---|---|
| snippet built | 1166 lines / 79,685 bytes | `grep -c ''` · `wc -c` |
| meta built | 18,549 bytes, schema-valid | `jsonschema.Draft7Validator` → `schema errors: 0` |
| review page | 315,752 bytes | `wc -c` |
| showroom page (generated) | 156,796 bytes | `gen_showroom.py` wrote 1 page |
| `canon.css` delta | **+764 / −0 lines** | `git diff --numstat` |
| byte-identical splice runs | **21** | extractor ledger, §BORROW LEDGER |
| `.c-bento` class uses in markup | 15 | `grep -o 'class="[^"]*c-bento'` |
| bento walls (`data-bento-role="dashboard"`) | 4 (1 outer + 3 inner) | markup count |
| masterbrand `<img>` pair | 2 | `grep -o '<img[^>]*masterbrand'` |
| raw type declarations | **0** (3 hits, all inside comments) | `grep -n 'font-weight'` etc. |
| off-ramp control heights added | **0** | see §FINDING 3 |
| glyphs, matched / bespoke / UNKNOWN | 7 / 0 / **0** | `_ICON-SOURCE-AUDIT.md` row 118 |
| orphan rows across every rendered group | **0 of 57 groups** | driven in-browser, §PROOF 2 |
| dataviz + component vars resolving, both modes | **16 / 16** | driven readback, §PROOF 3 |
| tiles painting a keyline anywhere | **0 of 170** | driven readback, §PROOF 4 |
| regen serial steps run | 7 of 7, then 5 `--check` determinism passes | §GATES |
| gates run | 13 | §GATES |
| gates red | **0** — 1 UNASKABLE (playwright-dependent, CI's arm) | §GATES |
| render calls | 3 (font probe green on the first) | §RENDER |

---

## 1 · WHAT WAS BUILT

`knowledge/snippets/Template-dashboard-bento.reference.html` — a Layer-2 template whose layout is
canon's `.c-bento` structural component rather than a Layout-utilities grid.

**Why the file exists, mechanically.** s230-D1 beat 3 measured PARTIAL at the #230 rehearsal for one
reason: `grep -rl '\.c-bento' knowledge/snippets/` returned **0 files**. The cold-start instruction
"copy component markup from `knowledge/snippets/`" had nothing to point at for a bento dashboard, so a
cold builder could only paraphrase the grammar out of `canon.css`. That grep now returns this file.

**The structure** is a bento-of-bentos (s217-D2/D3): one outer `data-bento-role="dashboard"` wall whose
three tiles are themselves dashboard bentos —

* **group 1** "This month" — four Kpi-tile modules, `data-c="3"` each
* **group 2** "Spending analysis" — the Chart-bar column specimen, `data-c="6"`
* **group 3** "Position" — a Summary of balances + a needs-attention list, `data-c="6"` each

Canon detects the outer wall **structurally** (`:has(> .c-bento__grid > .c-bento)`) and hands it the
open gutter while the inner walls stay tight. There is no second role name and nothing to switch on.

Accompanying files: `knowledge/components/template-dashboard-bento.meta.json` (required — the coverage
gate red'd on an orphan snippet until it existed) and the generated `showroom/template-dashboard-bento.html`.

**Status: PROPOSED, not registered.** Absent from CATEGORIES, MIGRATED_SNIPPETS, `component-types.json`
and `_rulings.json` — the Template-dashboard (#210) precedent, deliberately. It IS in `canon.css` and
`showroom/` because `gen_canon_components.py` and `gen_showroom.py` glob every snippet; that is the
serial's own behaviour, not a registration act, and it is declared in the meta's `$status`.

---

## 2 · BORROW LEDGER — 21 byte-identical splice runs

Cut by an extractor, sha256-stamped by the extractor, never re-typed. `TD` =
`knowledge/snippets/Template-dashboard.reference.html`; `ATN` = `App-shell-top-nav.reference.html`.

```
BENTO_CSS       knowledge/canon/canon.css   L1048-1218  10404 chars  sha256:23971d861f0d
AUTO_TOKENS     TD  L99-128     859   c8586d8a271f     LEADING_TRIM   TD  L129-130    329   25f7c44b46f5
THEME_BLOCKS    TD  L131-234    7451  d5a9cf2fd184     LAYOUT_PRIMS   TD  L235-308    5726  ec7f573a956a
HEADER_CSS      TD  L309-353    3698  041d1d092e00     KPI_CSS        TD  L400-462    4816  6ad6494543cc
CHART_CSS       TD  L463-485    1666  273e19019f31     TPL_R2         TD  L562-563    204   52a1e8aa4b38
TPL_R5          TD  L565        126   e059ad0ece1c     TPL_R10        TD  L570-571    257   7fea64a0befa
MASTHEAD_CSS    ATN L196-227    2370  45bc5be3c25d     HEADER_MARKUP_A TD L620-640    1325  72e9f9782bf6
HEADER_MARKUP_B TD  L647-649    189   7ed2a03e8fb1     KPI_A          TD  L661-673    1275  eb22295bf64a
KPI_B           TD  L675-686    1090  c9efd4f8477a     KPI_C          TD  L688-699    992   51076b5734b0
KPI_D           TD  L701-712    1004  b9e1d90842db     CHART_FIG      TD  L725-760    4816  eb25f77d4c51
BALANCES        TD  L769-777    803   5d2297adb365     ATTENTION      TD  L781-798    1219  4ffbb8edd1f4
```

**The only edit to any spliced markup run** is the tile re-classing: the first tag of each module gains
`c-bento__tile ` at the head of its class list and a `data-c`/`data-r` pair. Nothing else moved.

⚠ **I did NOT splice from `dashboards/international-banking-dashboard.canon.html`.** It is the one file
in the tree that already builds a bento dashboard, and it was tempting. The #230 enact brief forbids it
in as many words — *"NEVER copy code from `dashboards/international-banking-dashboard.canon.html`"* —
because Dave's own word on the Sol example is that it "wont be a good example of the html code". Flagged
here because the next lane that greps for a bento dashboard will find it first.

---

## 3 · WHAT IS RULED HERE, READ NOT REMEMBERED

Every value below was read off `knowledge/_render/role_defaults_219.py --table` or out of
`knowledge/_rulings.json`, not recalled.

| dial | ruling | value in the file |
|---|---|---|
| role | s217-D3 | `dashboard` — theme radius on each inner bento's CONTAINER, tiles square |
| main spacing (outer wall) | s219-D1 | **40px** — mono's shipped default |
| sub spacing (inner walls) | s219-D1(5) | **4px** — mono's shipped default |
| keylines | s219-D2(4) | **off** — the ruled default on every dashboard, every theme |
| keyline construction if ever on | s217-D8 + s218-D1 | **addressed, not copied** — §FINDING 2 |
| pageBg / bentoBg | s219-D1 | grey / transparent — light leg bound; **dark leg open**, §AWAITING DAVE 1 |
| masthead mark | s230-D2 | `masterbrand-light-colour` / `masterbrand-dark-colour`, `<img data-mode>` pair |
| radius model | s217-D2 | container radius + `overflow:hidden` clip, spliced from canon |
| type | type-composite mandate | 0 raw type literals; TYPE-002 contribution 0 |
| control sizes | 28/36/44/48 ramp | every control on the ramp; §FINDING 3 |

**The two-red law (s151-D1) holds, measured in the browser:** `--spark-down` resolves `#DA1A00` on the
white leg and `#F6604C` on the dark leg; `--spark-up` mirrors at `#137F3C` / `#66CC8D`. No red or green
is bound to a monetary figure anywhere — the only RAG on the page is a Status-indicator chip and it
always carries its word.

---

## 4 · THE SQUARING PASS IS MINT-TIME, AND A STATIC SNIPPET CANNOT RUN IT

s217-D3/D7 ratify a squaring pass that eliminates orphans. It is a **mint-time rewrite of `data-c`/`data-r`**
(`gen_canon_bento.square_wall()` / `square_nested_wall()`), so a hand-authored static snippet has no way
to run it. Rather than ship a wall that orphans at some band, the spans are chosen from the one set that
needs no pass at all:

* canon compiles the bands to **6 → 3 → 2 → 1** columns at 1100 / 820 / 520 container px, and **clamps**
  any `data-c` above the live column count;
* therefore `data-c="6"` is a full row at every band, and `data-c="3"` is a half row at six columns and a
  full row at three, two and one;
* every wall in the file uses **only 6 and 3**, and every wall holds an even number of 3s.

Orphans are impossible by construction. **PROOF 2** below drives it rather than arguing it.

---

## 5 · PROVEN BY DRIVING (not by reading the source back)

Rendered from `reviews/BENTO-SNIPPET-2026-08-31-v1.html` through `canon.css`'s projected block, so the
theme cascade is canon's own and not this lane's hand.

**PROOF 1 — the four responsive bands are real.** Four frames, wall widths measured in-browser:

```
wall 1174px → 6 columns (inner 6)   wall 934px → 3 columns (inner 3)
wall  654px → 2 columns (inner 2)   wall 374px → 1 column  (inner 1)
```

**PROOF 2 — zero orphans.** For every group, in every frame, in every theme: sum of tile widths +
gaps compared against the grid width. `groups: 57, orphanGroups: 0`. Page horizontal overflow: `0`.

**PROOF 3 — no dangling var, and the bars are not black.** Sixteen custom properties read back off the
live scope in both modes, all resolving:

```
              light      dark              light      dark
--data-series-1 #766682  #766682   --data-grid  #E1E1E1  #484848
--data-series-3 #577C78  #577C78   --data-axis  #626262  #9D9D9D
--baseline      #1A1A1A  #FFFFFF   --grid-alpha 1        1
--spark-up      #137F3C  #66CC8D   --axis-alpha 1        1
--spark-down    #DA1A00  #F6604C   --spark-flat #1A1A1A  #FFFFFF
--spark-base-alpha .10   .16       --wall-ground #F0F0F0 #1A1A1A
--surface       #FFFFFF  #1F1F1F   --rule       #E1E1E1  #808080
--indicator     #DB0011  #DB0011   --pressed    #CECECE  #484848
```

and the decisive one, read off the painted element rather than the stylesheet:
`firstBarFill = rgb(118, 102, 130)` in **both** modes — `#766682`, not black.
[[dangling-dataviz-var-renders-silent-black]] does not reproduce here.

**PROOF 4 — s217-D8 is honoured by absence, and the absence is asserted.** Keylines are off by ruling,
so nothing may paint a line in any gutter: **0 of 170 rendered tiles carry a top or left border**.

**PROOF 5 — the four themes differ where canon says they should.** Measured per theme, light:

| theme | outer gap | inner gap | `--border-radius-container` | inner group radius | overflow |
|---|---|---|---|---|---|
| mono | 40px | 4px | 0 | 0px | hidden |
| legacy | 40px | 4px | 0 | 0px | hidden |
| **console** | 40px | 4px | **20px** | **20px** | hidden |
| supercharge | 40px | 4px | 0 | 0px | hidden |

The s217-D2 model — radius on the container, clip on the container — is visible in console and resolves
to the same square picture in the other three. **SEEN**: all four themes, light and dark, in
`outputs/_render-231/03-themes.png`.

**PROOF 6 — the brand mark loads.** `masterbrand-light-colour.svg` and `masterbrand-dark-colour.svg`
both report `naturalWidth 315 / naturalHeight 85` — they are fetched, not broken references, and the
mode pair hides exactly one. **SEEN** in `01-alive.png`: the official mark, never text.

---

## 6 · AWAITING DAVE — rendered as readings, not decided

### AWAITING DAVE 1 — the dark page ground (§5 of the review page, three readings)

s219-D1 rules the dashboard page ground as **grey**. In light that is `surface/subtle` = `#F0F0F0`
under white modules and it works. **In dark the same token resolves to `#1F1F1F`, which is
byte-identical to `tertiary/background/default` — the module surface.** Ground and module become one
colour at 1.00:1, the 4px gutters vanish, and the wall stops reading as a bento. s219-D3(4) leaves the
dark page-ground derivation **expressly open** ("dark equivalents to be derived from tokens").

Three readings rendered side by side, same wall, only the ground moving — measured grounds
`rgb(31,31,31)` / `rgb(26,26,26)` / `rgb(49,49,49)` against a module surface of `rgb(31,31,31)`:

* **A** `#1F1F1F` — the ruled token taken literally. Modules vanish.
* **B** `#1A1A1A` — one rung darker. **This is what the file ships**, as a manifest `driftAllow` whose
  `$reason` carries the whole argument. It is the *shape* of s220-D1's "alignment by lift" applied to a
  ground s220-D1 does not govern. **Not a ruling.**
* **C** `#313131` — `color/neutral/5`, the exact grey s220-D1 put under the console caption in dark.
  Ground lighter than modules; the inverse of B.

One word closes it and the closing is a one-line change.

### AWAITING DAVE 2 — a module's own radius inside a rounded group (§6, two readings)

s217-D2 says tiles stay square inside the clipped container, and canon enacts that by writing **no**
tile radius at all — deliberately; canon's own comment says a literal `border-radius:0` would trip the
radius gate (ADR-0010) and would square off the very inner containers whose radius IS the dashboard role.

But a bento tile here is a **component**, and Kpi-tile carries `border-radius:var(--border-radius-surface)`
of its own. Mono/legacy/supercharge resolve that to 0 and the question never appears. **Console resolves
it to 20px** (measured: shipped `20px` vs squared `0px` in the two readings). Canon never ruled the case
because canon's tiles have no radius to rule on. Reading A (component keeps its radius, zero new CSS) is
what ships; reading B (modules squared) is rendered on the review page only. **If B is right the fix
belongs in canon's dashboard-role block, not in this snippet — which makes it a canon change.**

### AWAITING DAVE 3 — may a snippet link `canon.css`?

**Zero of 137 snippets do.** ⚠ The loose probe `grep -l 'canon/canon.css' knowledge/snippets/*.reference.html`
returns **110** and is a **FALSE probe** — every snippet carries that string inside its AUTO-TOKENS
provenance comment. The true probe `grep -l 'href="../canon/canon.css"' …` returns **0**. The whole shape
of this file turned on that distinction.

Consequence: a snippet using a canon **structural** component must carry a **copy** of the generated
block. This file carries a declared copy of the AUTO-BENTO block — and `gen_canon_components.py` then
re-projects that copy back into `canon.css` under `.cn-template-dashboard-bento`. Measured: the projected
block is **46,295 bytes** against Template-dashboard's 38,376 — roughly **+8 KB of duplicated bento rules
inside canon.css**, and it will scale linearly with every future bento snippet. Nothing compares the copy
to canon today, so it will rot silently. Both remedies are convention changes and both are Dave's:
(a) let snippets link `canon.css`, or (b) teach the projector to skip canon-owned selectors. §PRICED below.

### AWAITING DAVE 4 — should a bento snippet carry all four themes' spacing defaults?

s219-D1 gives each theme its own dashboard pair — mono 40/4, legacy 24/4, console 40/4, supercharge 24/2.
Snippets are mono-authored by convention, so only mono's pair is minted here and the other three are
**addressed** at `role_defaults_219.py` rather than typed into a second home. PROOF 5 shows the
consequence: the four themes differ in radius but not in spacing. Declared, not hidden.

---

## 7 · FINDINGS — things that were true before I arrived

**FINDING 1 — three masthead vars were bound and never declared, and the PROJECTOR caught it, not the eye.**
The first cut spliced ATN's masthead CSS and bound `--rule` / `--pressed` / `--indicator` in the manifest
but declared none of them in the theme blocks. `gen_snippet_tokens.py` refused with three named warnings.
Undeclared, `border-bottom:1px solid var(--rule)` resolves to `currentColor` and `color:var(--indicator)`
to nothing — the silent-black class one store over. Fixed before any gate ran. **The instrument works.**

**FINDING 2 — the keylines-ON construction cannot be honestly copied into a static snippet.**
s218-D1's corner assignment is minted **per responsive band** from the browser's own dense placement by
`gen_bento_matrix_217.corner_rules()`. Hand-copying the ~36 resulting selectors into a snippet would be a
**third home** for a generated fact (ADR-0017). Keylines are OFF by ruling so the file is correct as it
stands, and the ON construction is ADDRESSED in the header rather than duplicated. If a cold builder must
be able to switch keylines on from the snippet alone, that wants a generator, not a copy.

**FINDING 3 — `View-options.reference.html` still writes `height:40px`, and 13 snippets carry the literal.**
Template-dashboard's page-header lock-up ends with a `.seg` period switcher spliced from View-options,
whose `.seg button` is `height:40px` — off the 28/36/44/48 ramp, one of the three #230 eye-lane findings.
Measured at head: `grep -ln 'height:40px' knowledge/snippets/*.reference.html` → **13 files**, View-options
among them; **`Segmented-control.reference.html` — the component s229 actually ruled — is NOT among them.**
The brief says do not import another, so the header lock-up is spliced as **two** byte-identical runs with
the switcher's 44 CSS lines and 6 markup lines left out. Nothing was edited at source: View-options'
literal is the build-PM's to retire. **If a period switcher is wanted here, splice Segmented-control.**
The demo bar's own button is 36px, not the 32px Template-dashboard draws — same reason, declared in the file.

**FINDING 4 — two bento parameters cannot be manifest-bound today.**
* `layout/bento/columns` → `gen_snippet_tokens.resolve()` returns the **string `"6px"`**, because
  `_unitless()` does not know the path. `grid-template-columns:repeat(6px, …)` is invalid CSS. MEASURED.
* `layout/bento/packing` → **KeyError**: s217-D4 stores `"row dense"` under `$extensions`, not `$value`.
  That is the ruled storage shape, not a defect.

Both are declared as literals in the file with the reason attached. §PRICED below.

**FINDING 5 — `.tpl-link` was missing and only the EYE caught it.** The first cut omitted
Template-dashboard's composition rules 2, 3, 5, 10 and 11, and the "View all" link in the needs-attention
module fell back to the user agent's default blue — **invisible on the dark ground, with all 13 gates
green over it.** Found by looking at the render, fixed by splicing the five rules byte-identically.
[[green-tests-cannot-see-scope]], again, in the smallest possible form.

---

## 8 · GATES — every last line quoted, none paraphrased

**The whole ordered regen serial, ramp first, index last, re-run in full after every source change
(three times in total — after the first build, after the manifest repair, after the `.tpl-*` repair):**

```
1 gen_radius_derive          WROTE _derive-radius-proposal.json (4 themes) — PROPOSAL ONLY, nothing minted.
2 gen_snippet_tokens         5015 manifest bindings across 136 snippets + 9 tranches; 0 value(s) projected
3 canon/gen_canon_tokens     TOTAL: 577 root vars, 195 dark overrides
4 canon/gen_canon_components generated 136 components -> .cn-<scope>
5 canon/gen_theme_cascade    wrote AUTO-THEMES block — 230 override path(s), 392 component projection(s)
6 gen_showroom               136 page(s) -> showroom/ (1 written, 0 orphan(s) pruned)
7 gen_component_partials     0 consumer block(s) injected/refreshed (all in sync)
```

⚠ `_build_all.py` was **not** run (chain warning, per the brief). The index step is `gen_showroom`'s;
`knowledge/_render/gen_library_214.py` owns `showroom/index.html` and was **deliberately not run** — this
snippet has no component-store entry, so wiring it into the library index would be a registration act and
is not this lane's. `showroom/index.html` is unchanged (confirmed in `git status`).

**Determinism `--check` passes, all green:**
```
gen_canon_components --check OK — 136 components in sync.
gen_theme_cascade --check OK — 230 override path(s), 392 component projection(s) in sync.
gen_showroom --check OK — 136 page(s) + index in sync.
gen_component_partials --check OK — all AUTO-PARTIAL blocks in sync, contracts hold.
gen_snippet_tokens --check: 0 value(s) would change; 0 canon.css literal(s) would change.
```

**Gates:**
```
✅ snippet gate          : 136 snippet(s), 0 failure(s)
✅ coverage gate         : 136 meta(s) / 136 snippet(s), 0 failure(s)
✅ icon-source gate      : 0 UNKNOWN, 97 bespoke, across 136 snippet(s); 750 library glyphs
✅ radius gate           : 0 strict fail(s), 0 advisory file(s) pending migration
✅ a11y gate             : 136 snippet(s), 0 failure(s), 287 warning(s), 671 note(s)
✅ DTCG gate             : PASS — 0 failure(s), 61 declared deferral(s)
✅ binds-resolve gate    : 136 snippets · 136/136 canon blocks · 0 failure(s)
✅ descender-clip gate   : PASS (152 file(s))
✅ dataviz gate          : PASS (15 chart surface file(s))
✅ dark-surface gate     : 0 flat-white failure(s), 9 annotated exception(s)
✅ no-hardcode gate      : PASS (11 tranche file(s))
✅ TYPE gate, this file  : PASS — all component text bound to canon composites (1 file(s))
✅ GRID gate, this file  : PASS — all layout dimensions on the 4px grid (1 file(s))
✅ meta schema           : jsonschema Draft7 — 0 errors
⚠ state-contrast gate    : COULD-NOT-ASK — playwright not importable on the default interpreter.
                           This is NOT a skip: it runs BLOCKING in the `render` job of gates.yml,
                           which installs chromium. That job is where its proof of record lives.
⚠ hit-area gate          : COULD-NOT-ASK, same cause, same standing.
```

**The repo-wide type ratchet.** `TYPE GATE FAIL — 1091 violation(s) across 90/151 file(s)` is the
standing repo state, not this lane's. **This file's own contribution is 0** (per-file run PASS above), so
the debt cannot have grown from here. ⛔ **UNPROVEN, declared:** I did not run the ratchet's own
baseline comparison arm, so "the ratchet did not move" is an inference from the per-file pass, not a
measurement. `--ratchet` dumps ~538 KB and was abandoned rather than paged through.

---

## 9 · RENDER — how it was proven, and the font

Recipe per `knowledge/_RUNBOOK-render-verify.md` plus `notes/_subreports/2026-08-31-230-seg-snippets-eye.md` §6.

* `outputs/_render-env-229/` **survived on the mount** — `pylibs`, `pw-browsers`, `chromelibs` all worked
  verbatim, saving the install. ✅ Replay note 1 of #230 holds a third time.
* Its `fonts.conf` and every font symlink pointed at `/sessions/determined-affectionate-euler/…` — **dangling**.
  Rebuilt for this session at `outputs/_render-env-231/` (10 symlinks + conf + cachedir), ~1 call.
* `ldd` probe before trusting the lib dir: **NO MISSING LIBS**.
* **The three-way font probe, run before believing any pixel:**
  `{"hsbc": 740.61, "arial": 711.72, "nonexistent": 641.72}` — three distinct widths ⇒
  **REAL HSBC CUT RESOLVING.**
* All exports in the same bash call as the render; `TMPDIR=/dev/shm`; no `set_content()`; no `env=` on
  `launch()`. 3 render calls, all well inside the ~178 s wall. `pageerrors: []`, console errors `0`.

Shots at `outputs/_render-231/`: `01-alive` · `02-bands` · `03-themes` · `04-dark-readings` ·
`05-full` · `06-tileradius` · `facts.json`. **01, 03, 04 and 06 were opened and looked at.**

---

## 10 · PRICED, NOT BUILT (gate-don't-patch)

1. **A byte-compare gate for the AUTO-BENTO copy.** ~30 lines: extract this file's AUTO-BENTO region and
   `canon.css`'s, assert byte-equality, fail loud with both sha256s. Cheap, and it converts a silent rot
   into a red build. It becomes unnecessary if Dave rules that snippets may link `canon.css`.
2. **The `_unitless()` one-liner** for `layout/bento/columns` (FINDING 4). One line in a **shared**
   generator; the class fix (which other count-shaped token paths are mis-formatted as px?) is the
   build-PM's, not a worker lane's. Not applied.
3. **A projector skip-list for canon-owned selectors** (`.c-bento*`) in `gen_canon_components.py`, if
   Dave prefers (b) over (a) in AWAITING DAVE 3. Larger, and it changes canon output — a canon change.
4. **The View-options `height:40px` retirement** (FINDING 3). 13 files carry the literal. Not touched.

---

## 11 · UNPROVEN — declared, not hidden

* **The type ratchet's own comparison arm** — see §8.
* **state-contrast and hit-area** — unaskable on this box; CI's `render` job is their home.
* **Real keyboard/AT behaviour** — nothing was driven with a screen reader. The a11y gate's 0 failures is
  a static measurement.
* **The four themes' SPACING** — only mono's ruled pair is minted (AWAITING DAVE 4). Console/legacy/
  supercharge were rendered with mono's 40/4, which is what the file says; their own ruled pairs are
  UNRENDERED here.
* **Print, reduced-motion and forced-colors** — not driven.
* **The 46,295-byte canon projection** was measured but its downstream effect on page weight across the
  showroom was not.

---

## 12 · REPLAY-THESE — 8

1. **★ `grep -l 'canon/canon.css' knowledge/snippets/*.reference.html` is a FALSE probe.** It returns 110
   of 137 and every hit is the AUTO-TOKENS provenance comment. The true probe is
   `grep -l 'href="../canon/canon.css"'` → **0**. I nearly built the file on the 110 reading.
   [[unmatched-grep-is-not-an-absence]] has a mirror: **a MATCHED grep is not a presence either.**
2. **★ The persisted render env survives but its FONT LEG is session-path bound and fails silently.**
   Third session running: `pylibs` / `pw-browsers` / `chromelibs` all reusable verbatim; `fonts.conf` and
   every symlink dangling. Rebuild the font farm per session and **run the three-way font probe before
   believing any type on any shot** — #230's replay note 1, held again.
3. **★ `gen_canon_components.py` and `gen_showroom.py` GLOB every snippet — there is no registry gate.**
   Dropping a file into `knowledge/snippets/` silently adds a `.cn-<slug>` block to `canon.css` and a
   showroom page. Measured cost for this file: **+764 canon.css lines / 46,295 bytes**. Price the canon
   growth *before* writing a snippet that carries structural CSS, not after.
4. **★ The coverage gate red's on an orphan snippet within one run.** A new snippet needs
   `knowledge/components/<slug>.meta.json` in the same breath, and the meta schema requires
   `accessibility.relatedSC` and `tokenValidation.{date,against,result}` — copy an existing meta's shape
   or `jsonschema` will find them for you.
5. **★ A bento instance dial written as a bare class LOSES SILENTLY.** Canon's bento-of-bentos carve-out
   is `:has(> .c-bento__grid > .c-bento)` and `:has()` takes its most specific argument, so that rule
   weighs **(0,4,0)**. `.tpl-wall{--bento-gutter:40px}` is (0,1,0) and canon wins — at one spacing, in one
   theme, with every gate green. Do the specificity arithmetic, and write it down next to the rule.
6. **★ Spans 6 and 3 are the only orphan-free static set.** The squaring pass is mint-time and no static
   snippet can run it. Because canon clamps `data-c` above the live column count, only `6` (full row
   always) and `3` (half at six, full at three/two/one) survive every band. An even number of 3s per wall.
   Any other span needs the generator.
7. **★ A gate suite of 13 greens did not see a default-blue link on a dark ground.** `.tpl-link` was
   missing; the eye caught it in the first render. Look at the picture before believing the gates.
8. **The projector is a gate.** `gen_snippet_tokens.py` named three undeclared masthead vars before any
   validator ran. Run the serial early and read its WARNINGS, not just its exit code.

---

## 13 · RSQ — RULING-SHAPED QUESTIONS, all Dave's, none touched

| # | question | where it is rendered | cost of getting it wrong |
|---|---|---|---|
| R1 | The **dark page ground** for a dashboard bento: A `#1F1F1F` (the ruled token, modules vanish) / **B `#1A1A1A` (shipped, provisional)** / C `#313131`. s219-D3(4) left it expressly open. | review §5, three readings | every dark bento dashboard reads wrong or right on this one value |
| R2 | **Does "tiles stay square" (s217-D2) reach a module that is a component with its own surface radius?** Console shows 20px modules inside a 20px group. | review §6, two readings | affects every console bento that holds a real component |
| R3 | **May a snippet link `canon.css`?** Today 0 of 137 do, so structural canon must be COPIED — and re-projected back into canon at ~+8 KB a snippet. | §AWAITING DAVE 3 | canon.css grows linearly with bento snippets; the copy rots silently |
| R4 | **Should a bento snippet carry all four themes' spacing defaults**, or address `role_defaults_219.py`? | §AWAITING DAVE 4 | three of four themes ship mono's spacing in any copied snippet |
| R5 | **Should this file carry the keylines-ON construction inline?** Its corner rules are minted per band; copying makes a third home. | §FINDING 2 | a cold builder cannot turn keylines on from the snippet alone |
| R6 | **Should `Template-dashboard-bento` be registered** (CATEGORIES / MIGRATED_SNIPPETS / component-types / library index), or stay PROPOSED like Template-dashboard? | §1 | an unregistered snippet is invisible to the library index |
| R7 | **The View-options `height:40px` retirement** across 13 snippets, and whether `.seg` consumers should be repointed at the s229-ruled Segmented-control. | §FINDING 3 | the off-ramp literal keeps propagating by splice |
| R8 | Whether the **priced AUTO-BENTO byte-compare gate** (§10.1) should be built, or made moot by R3. | §10 | silent divergence between canon and its copy |

---

## 14 · FILES WRITTEN — nothing else

**New (mine):**
```
knowledge/snippets/Template-dashboard-bento.reference.html      79,685 bytes
knowledge/components/template-dashboard-bento.meta.json         18,549 bytes
reviews/BENTO-SNIPPET-2026-08-31-v1.html                       315,752 bytes
showroom/template-dashboard-bento.html                         156,796 bytes  (generated by the serial)
outputs/_render-env-231/{fonts.conf, fonts/*10 symlinks, fccache/}            (render env, this session)
outputs/_render-231/{01..06}.png + facts.json                                 (render evidence)
notes/_subreports/2026-08-31-231-bento-snippet.md               this file
```

**Modified, all by the regen serial and its audit writers:**
```
knowledge/canon/canon.css              +764 / −0   (the .cn-template-dashboard-bento projection)
knowledge/_A11Y-GATE.md · _COVERAGE-GATE.md · _ICON-SOURCE-AUDIT.md · _SNIPPET-AUDIT.md   (gate reports)
knowledge/_derive-radius-proposal.json  $generatedAt timestamp only
```

⛔ **NOT touched, per the DO-NOT-RULE list:** `knowledge/_rulings.json` · `knowledge/_state.json`
(it was already dirty when this lane opened — another lane's) · no commits · no push · no release
machinery · no roster/version moves · no pack/dist/manifest · `showroom/index.html` · no other snippet.
`knowledge/_detect_retrieval.py`, `notes/_briefs/2026-08-31-231-detector-brief.md`,
`notes/_subreports/2026-08-31-231-detector.md` and `reviews/DETECTOR-READINGS-2026-08-31-v1.html`
appear in `git status` and are **another lane's**, not mine.

---

## 15 · COST

21 splice runs, 3 builds of the snippet, 3 render calls, 7-step serial run 3× in full, 13 gates.
⛔ Token spend **not instrumented** for this lane — I did not run `_checkin.py` (it measures the
conductor's window, not a sub's) and will not report a figure I did not measure.
