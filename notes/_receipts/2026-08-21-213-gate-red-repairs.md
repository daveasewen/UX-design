# Receipt — #213 GATE-RED repair lane (four attributable `_build_all.py` reds)

> ⛔ **DATED PERIOD RECORD, NOT A LIVE HOME.** Written 2026-08-21 by the #213 gate-red repair Opus sub.
> **Nothing in this file is a ruling.** Open choices below are PROPOSED-not-ruled and are Dave's.
> The store (`knowledge/_state.json`, `knowledge/_rulings.json`) stays the one live home.

| governance | value |
|---|---|
| lane | GATE-RED repair, #213 mine-side burn-down fan-out |
| brief | `notes/_briefs/2026-08-21-213-mine-burn-fanout-brief-v1.md` |
| lanes read first | E1 `…-laneE1-w99-ds018-enactment.md` · E2 `…-laneE2-w99a-rag-canon.md` · E3 `…-laneE3-w59-var-renames.md` · `…-template-family-repair.md` |
| git | **none run** (FENCE 1). All edits UNCOMMITTED. |
| shared state | **untouched** — no `_state.json`, `_rulings.json`, `_GOVERNING-RECORDS.md`, `_lanes.json`, `_TOKEN-FORK-LEDGER.json`, `_DS-IMPROVEMENTS.md`, `MEMORY.md`, `_CHAIN.md`. `knowledge/_type_ratchet.json` verified byte-unchanged (`baseline 1097`, `shrunk "1099 -> 1097 on 2026-08-17"`). |

---

## 0. HEADLINE

| # | red | rc before | rc after |
|---|---|---|---|
| 1 | 4px-grid gate (`_validate_grid.py`, DEF-005) | **1** — 12 off-grid | **0 — GRID GATE PASS, 151 file(s)** |
| 2 | type-composites ratchet (`--ratchet`, s119-D1) | **1** — 1105 > 1097, 8 NEW | **0 — holds at 1097, 0 new** |
| 3 | compose gate (`_validate_compose.py`) | **1** — `--uf`, `--undefined` | **0 — RESULT: PASS ✅** |
| 4 | fork-ban gate (`_validate_token_forks.py`) | **1** — 5 undeclared forks | **1 — 2 forks, both DECLARED RESIDUAL (§4)** |

Also cleared as collateral: **property-resolves gate C2** (`_validate_property_resolves.py`) — 2 failures I caused mid-repair, then fixed properly; now **0 failures / 147 files** (§3b).

Still red, **NOT MINE, NOT TOUCHED**: radius gate (4 strict fails — Dave's, `W-90` snap-or-waive) · pro-forma universal gate (§5).

---

## 1. RED 1 — the 4px-grid gate

**PROBE.** `python3 knowledge/_validate_grid.py` → 12 `✗ off-grid`, six in
`knowledge/snippets/Status-indicator.reference.html` and the same six re-reported from
`knowledge/canon/canon.css` (the generator's projection of the same rules — one source defect
counted twice).

**MECHANISM.** Lane E2's new G17-B/G17-C blocks (`…laneE2…md:44` — *"G17-B `.cell` + `.statustable`
and G17-C `.sbar` blocks"*) carry six off-grid layout values. Quoted from the file before the fix:

```
:85  .statustable th{… padding:6px 12px; …}
:87  .cell{… padding:4px 10px; …}
:96  .sbar{… gap:10px; padding:10px 14px; margin:6px 0; …}
```

**FIX** (source snippet, never canon.css by hand — ds-018 recurrence class):

| site | was | now | why this value |
|---|---|---|---|
| `.statustable th` | `padding:6px 12px` | `padding:8px 12px` | matches `.statustable td`'s existing `8px 12px` — the row rhythm the table already uses |
| `.cell` | `padding:4px 12px`* | `padding:4px 12px` | *was `4px 10px`; 12px matches the table cell's own 12px inline padding. `min-width:84px` + `text-align:center` unchanged, so the chip's visual size is governed by min-width, not the pad |
| `.sbar` | `gap:10px; padding:10px 14px; margin:6px 0` | `gap:12px; padding:12px 16px; margin:8px 0` | copies the file's own `.live{gap:16px; padding:12px 16px}` / `.stat{gap:12px}` rhythm rather than inventing one |

**PROOF IT CAN FAIL** (mutant DRIVEN, not asserted):
re-planted `padding:6px 12px` on `.statustable th` → `rc=1`,
`✗ off-grid: padding: 6px (knowledge/snippets/Status-indicator.reference.html) — not a 4px multiple`;
restored → `rc=0`. The plant was asserted present before the run (no plant-that-didn't-plant, #209).

**rc after:** `python3 knowledge/_validate_grid.py` → **0**, `GRID GATE PASS — all layout dimensions on the 4px grid (151 file(s))`.

---

## 2. RED 2 — the type-composites ratchet

**PROBE.** `--ratchet` → `TYPE RATCHET FAIL — 1105 violation(s) > declared debt 1097. 8 NEW violation(s)`.

**⛔ THE BRIEF'S ATTRIBUTION WAS WRONG, AND THE MECHANISM IS NAMED.**
The brief named `Chart-bullet.reference.html` and `Chart-candlestick.reference.html`. **They are not
the cause.** Probes:

| probe | result |
|---|---|
| `_validate_type_composites.py knowledge/snippets/Chart-bullet.reference.html` | `TYPE GATE FAIL — 5 violation(s)`; `Chart-candlestick` also 5; `Chart-bar` / `Chart-line` / `Chart-scatter` **6 each** | 
| were they outside the glob before? | **No.** `DEFAULT_TARGETS` globs `knowledge/snippets/*.html` — no allowlist. Both files are referenced from `notes/_briefs/2026-08-05-chart-wave2-lane2-statistical.md` (2026-08-05), i.e. long inside the 2026-08-17 baseline measurement |
| was the debt mis-keyed? | **No.** The ratchet stores a single integer, not a per-file key (`_type_ratchet.json` → `{"baseline": 1097, "unit": "violations (count), … summary line"}`) — there is nothing to mis-key |
| why do they appear in the output at all? | the gate prints every violation; `_build_all.py` shows the **tail** of that list. The two chart files are simply the alphabetically-late snippets in a 1,105-line report. They are **pre-existing declared debt** |

**THE ACTUAL MECHANISM — Lane E2 again, same two blocks.**
`--inventory` on the only file with today's mtime that carries new font declarations:

```
TYPE-002,knowledge/snippets/Status-indicator.reference.html,.statustable th,font-weight,600
TYPE-003,knowledge/snippets/Status-indicator.reference.html,.statustable th,font-weight,600 (off-ramp weight)
TYPE-002,knowledge/snippets/Status-indicator.reference.html,.sbar,font,400 15px/1.35 var(--font)
TYPE-003,knowledge/snippets/Status-indicator.reference.html,.sbar,font,15px (off-ramp)
```

…and the identical four projected into canon.css as `.cn-status-indicator .statustable th` /
`.cn-status-indicator .sbar`. **4 in the snippet × 2 (snippet + canon projection) = exactly the 8 NEW.**
Confirmed by arithmetic after the fix: the count landed on **1097 exactly, 0 new** — an 8-violation
delta with nothing else moved.

**FIX — bind the mandated composites; the debt figure was NOT raised.** Worked to the file's own
existing convention (`.chip`, `.sim` already carry `/* type: … (bound in canon/type.css - T-D9/T-D12) */`
and no raw font decl, with the class on the markup):

- `.statustable th` — raw `font-weight:600` **removed**; markup `<th scope="col">` ×3 now carry
  `class="t-cm-ctl-14"` (Component composite, 14px/500 — single-line `white-space:nowrap` header,
  the mini control ramp T-D15 step for dense tables). 600 was also off the canon ramp
  (`weights [250,300,350,400,500,700]`); 500 is on it.
- `.sbar` — raw `font:400 15px/1.35 var(--font)` **removed**; the inner `<span>` ×5 now carry
  `class="t-ed-body"` (**Editorial**, 16px/24px/400). THE DECIDING RULE applied: the bar's label
  wraps, so it must be Editorial, not Component (the N1 caveat). 15px was off the ramp; 16px is on it.

**PROOF IT CAN FAIL:** re-planted `font-weight:600` on `.statustable th` → the file-scoped gate goes
`TYPE-002 ×3` → `TYPE-002 ×4 · TYPE-003 ×1` (5 violations, `rc=1`); restored → back to 3.
Note the file-scoped gate returns `rc=1` either way — `Status-indicator` still carries **3
pre-existing** debt violations (`body`, `.stat`, `.live .now`), which are inside the 1097 and were
deliberately left alone. **The gate whose verdict changed is the ratchet**, and its bite is the
1097/1099 boundary.

**rc after:** `--ratchet` → **0**, `TYPE RATCHET PASS — declared debt holds at 1097 (0 new). This is
DEBT, not a pass of the underlying gate.` `_type_ratchet.json` **not written** (the gate only writes
when the count *falls* below baseline; it landed exactly on it).

---

## 3. RED 3 — the compose gate (`--uf`, `--undefined`)

### 3a. `--undefined` — a GATE defect, not a canon defect. Fixed in the gate, mutation-proven both ways.

**PROBE.** The only occurrence in canon.css is **line 17549, inside a `/* … */` comment**:

```
     carried them all: `fill:var(--undefined)` does not fall back to the previous value, it falls
     back to the SVG initial value, BLACK, in silence [[dangling-dataviz-var-renders-silent-black]].
```

— prose projected verbatim from `knowledge/snippets/Template-report.reference.html:87`. The same
sentence lives in `Template-dashboard.reference.html:170` and `Chart-bar.reference.html:100`.

**MECHANISM.** `_validate_compose.py:check_canon()` extracted refs from the **raw bytes**:
`refs = set(re.findall(r'var\((--[\w-]+)', css))` — no comment stripping. The gate was reddening on
a **sentence warning about dangling vars**. It is not a generator emitting a literal fallback (the
brief's hypothesis, re-probed and **falsified**: `grep -rn -- "--undefined" knowledge/*.py knowledge/canon/*.py`
returns nothing; the string exists only in snippet prose).

**FIX — in the gate, the class fix.** Added `strip_css_comments()` and applied it to the def/ref
extraction only. Rationale inscribed at the site: *parse in the consumer's grammar* — the browser
never sees comment text, so a `var(--x)` in prose is not a reference **and** a `--x:` in prose is not
a definition. The change is strictly more accurate in **both** directions.

**PROOF IT CAN FAIL — two arms, both DRIVEN against canon.css, restored byte-identical:**

| arm | plant | result |
|---|---|---|
| **A — detectable-when-present** | a REAL dangling `outline-color:var(--truly-dangling)` in live CSS | `rc=1`, `❌ canon.css: 1 unresolved var(): ['--truly-dangling']` — the gate still catches the thing it exists to catch |
| **B — the fixed case** | `/* prose: fill:var(--another-undefined-in-prose) */` in a comment | `rc=0`, `RESULT: PASS ✅` — no longer fires on prose |

Brace-count exposure measured, not assumed: raw `7785/7785`, comment-stripped `7715/7715` — both
balanced, so the brace check was left reading raw bytes and no verdict moved. **Declared residual:**
`check_screen()`'s rogue-hex scan reads `<style>` including comments — same class, not in this lane's
named edits, **PROPOSED** below.

### 3b. `--uf` — a real dangling var, and my first fix was wrong. Both states recorded.

**PROBE.** `var(--uf)` in canon.css:6179 / :10673, from
`CTA-lockup.reference.html:100` and `Feature-grid-lockup.reference.html:100`:
`.demo-note{font:400 12px/1.3 var(--uf); …}`. `--uf` is defined **only** in
`knowledge/canon/type.css:6` (`:root{--uf:"Univers Next HSBC",…}`) — a real file, not a typo, but
one that canon.css does not contain. Sibling snippets carry the byte-identical line with
`var(--font)`: `Page-header-lockup.reference.html:127`, `Filter-toolbar-bar.reference.html:92`.

**FIRST FIX, AND WHY IT WAS INSUFFICIENT — declared, not hidden.** I changed `--uf` → `--font` in
both snippets. Compose went green; then `_build_all` step 121-ish surfaced a **new** red I had
caused: `_validate_property_resolves.py` (C2, ds-018) → *"`--font` referenced 1× with no fallback and
declared nowhere this file can reach"* in exactly those two files. The two contexts genuinely
disagree: standalone, the snippet links type.css so `--uf` resolves and `--font` does not; inside
canon.css the reverse. A one-sided fix could only ever move the red.

**PROPER FIX.** Both snippets' own `:root{}` now declare `--font`, **byte-identical to
`Page-header-lockup.reference.html:68`** — the shape 87 of 135 snippets already use. Verified
non-projecting before applying: `grep` finds **zero** `.cn-*{--font:…}` in canon.css, so the
generator does not project a component-scoped `--font` and the addition cannot create a `--font`
fork. Re-measured after regen: fork gate `names 923`, no `--font` fork.

**rc after:** `_validate_compose.py` → **0**, `RESULT: PASS ✅` · `_validate_property_resolves.py` →
`147 file(s), 0 failure(s)` (was 2).

---

## 4. RED 4 — the fork-ban gate: 3 of 5 retired, **2 DECLARED RESIDUAL, both PROPOSED to Dave**

**PROBE** (re-run, not inherited — the gate that E3 found crashing at exit 2 now parses, so the
Template-family repair lane's orphan-brace fix landed):

```
FORK --l-min    mono  .cn-layout-utilities .l-grid (240px)      vs .cn-template-report .tpl-stats (200px)
FORK --min-pri  mono  .cn-app-shell-split .sp (240px)           vs .cn-splitter .sp (160px)
FORK --min-sec  mono  .cn-app-shell-split .sp (240px)           vs .cn-splitter .sp (160px)
FORK --move     mono  .cn-tabs (220ms …)                        vs .cn-template-settings (200ms …)
FORK --panel    supercharge/dark  .cn-app-shell-multi-column (#2A2621) vs .cn-app-shell-nav-rail (#1A1A1A)
GATE RED: 5 fork(s) not in the ledger
```

— the same five E3's `§5b` lists. E3's class fix (component-local rename in the **snippet source**)
applied where the collision is genuinely a name accident.

### 4a. FIXED — 3 fork records, 3 renames

| snippet | rename | sites | why it is a name accident |
|---|---|---|---|
| `Splitter.reference.html` | `--min-pri` → **`--spl-min-pri`** | 3 | two unrelated components each declare their own pane fence; App-shell-split's 240px is documented as *"SYMMETRIC … Coequal panes, coequal fences"*, Splitter's 160px is its own. No manifest binding on either name (`grep '"--min-pri"'` → nothing), so no semantic moved |
| `Splitter.reference.html` | `--min-sec` → **`--spl-min-sec`** | 3 | same |
| `Template-settings.reference.html` | `--move` → **`--tset-move`** | 6 | Template-settings' own header already says it renamed `--ease`→`--move` *"BOTH are var-NAME collisions with other components on this page"* — it collided again with Tabs' 220ms. Six other consumers of `--move` (Tabs, Page-header-lockup, Template-detail/-dashboard/-list-index/-report) are all 220ms and UNIFORM |

Renames used the whole-token regex `(?<![-\w])--NAME(?![-\w])` over the whole file, so CSS
declaration, prose comment and the snippets' JS (`num('--min-pri')` / `num('--min-sec')`) moved
together. Residual old names in the edited files: **grep exit 1 — zero**.
`var(--min-pri|--min-sec)` in canon.css: **zero**. `var(--move)` survivors in canon.css: 8, all in
the 220ms uniform set.

**PROOF IT CAN FAIL:** with `--spl-min-pri` reverted to `--min-pri` **in canon.css** (the file the
gate actually reads), `GATE RED: 2` → `GATE RED: 3` with `FORK --min-pri theme=mono` back; restored
byte-identical → `GATE RED: 2`. The plant asserted the rename had reached canon.css first
(`1 site`), so this is a driven bite, not a self-comparison.

### 4b. ⛔ `--l-min` — **NOT a fork. Renaming it would SILENTLY BREAK the page.** Left red.

The gate is comparing a **documented parameter** against the consumer that sets it. Evidence, quoted:

- `Layout-utilities.reference.html:209` — `.l-grid{ display:grid; --l-min:240px; grid-template-columns:repeat(auto-fill, minmax(min(var(--l-min), 100%), 1fr)); }`
- `Template-report.reference.html:414` — `.tpl-stats{ --l-min:200px; }  /* 12 · the stats band's min track */`
- `Template-report.reference.html:536` — **`<div class="l-grid tpl-stats" data-gap="l">`**
- `knowledge/tokens/_manifests/sutherland-fixtures.json:5130` `$note` — *"`.l-grid`'s track floor, **set by the consumer**."*

`.l-grid` and `.tpl-stats` are **the same element**. `--l-min` is the l-grid partial's public
parameter and `.tpl-stats` overrides it at a narrower scope, exactly as designed. A component-local
rename would leave `var(--l-min)` reading the 240px default and the stats band would silently widen
— a behaviour change with no gate to catch it. (`Template-dashboard.reference.html:536`
`.tpl-kpis{--l-min:240px}` does the same thing at the same value, which is why it never forked.)

**PROPOSED, NOT RULED — Dave's:** the fork-ban gate does not model **parameterised partials**
(ADR-0013 territory). Either (a) the gate learns to exempt a var that a registered partial declares
as its own parameter, or (b) `--l-min` gets a ledger entry. I did **neither**:
`_TOKEN-FORK-LEDGER.json`'s `$purpose` says *"Baseline of forks MEASURED at #139"* with
`$measured = 2026-08-09 s139` and `$do_not = No script may add to this file automatically` — adding
today's forks would corrupt a dated measurement, and the ledger is shared state this lane may not edit.

### 4c. ⛔ `--panel` — a real value question, **exactly the carve-out the brief named.** Left red.

Not a name accident: the two components bind `--panel` to **different semantics**, in their own
manifests:

- `App-shell-multi-column.reference.html:538` — `"--panel": "tertiary/background/default"`
- `App-shell-nav-rail.reference.html:708` — `"--panel": "background/default"`

The two semantics happen to coincide in every theme/mode **except supercharge/dark**, where they
resolve `#2A2621` vs `#1A1A1A` — which is why one fork record, not eight. That asymmetry is itself
the finding: the divergence is invisible until one theme's dark ramp separates the two tiers.

**No value picked, no rename applied** (a rename would freeze the divergence and read as an answer).
**PROPOSED, in Dave's terms:** *"Should the nav rail's panel sit on the same tertiary tier as the
multi-column shell's panel, or is a nav rail deliberately darker than a content panel in supercharge
dark?"* Whichever way it goes, the loser is a one-line binding change; if the answer is *"both are
right"*, the ledger entry is then Dave's to sanction.

**rc after:** `_validate_token_forks.py` → **1**, `GATE RED: 2 fork(s) not in the ledger` — 5 → 2,
both remaining declared above.

---

## 5. WHAT ELSE IS RED — measured, none of it mine, none of it touched

| gate | state | owner |
|---|---|---|
| radius gate | 4 strict fails | **Dave's — `W-90` snap-or-waive.** Not touched, per brief |
| pro-forma universal gate | `[FAIL] _proforma/Masthead-interactive.html — INVENTED icon(s) not asset-backed and not flagged provisional: ['i-menu-search']` | not in this lane's four reds; file mtime 13:37 today, predates this lane. **Flagged for the conductor**, unrepaired |
| fork-ban | 2, both §4b/§4c | Dave's |

`_build_all.py` was run as instructed (`--range 1-120`, then `--resume 121`) — that is how the
property-resolves red of §3b and the pro-forma red above were found; steps 1–128 ran contiguous.

---

## 6. GREEN AFTER, TARGETED (s172-D3 bounded verification — depth cap 1)

| check | result |
|---|---|
| `_validate_grid.py` | **rc 0** — `GRID GATE PASS … (151 file(s))` |
| `_validate_grid.py --selftest` | rc 0 |
| `_validate_type_composites.py --ratchet` | **rc 0** — `holds at 1097 (0 new)` |
| `_validate_type_composites.py --selftest` | rc 0 |
| `_validate_compose.py` | **rc 0** — `RESULT: PASS ✅` |
| `_validate_token_forks.py` | **rc 1** — 2 declared residuals (§4b, §4c) |
| `_validate_property_resolves.py` | `147 file(s), 0 failure(s)` (was 2 mid-repair) |
| `_validate_snippets.py` | `135 snippet(s), 0 failure(s)` |
| `_validate_binds_resolve.py` | `135 snippets … 135/135 canon blocks · 0 failure(s)` |
| `gen_canon_components.py --check` | `OK — 135 components in sync` |
| `gen_snippet_tokens.py --check` | `OK — snippets + tranches + canon.css in sync with tokens` |
| `gen_theme_cascade.py --check` | `OK — 228 override path(s), 386 component projection(s) in sync` |
| `_type_ratchet.json` | baseline `1097`, `shrunk "1099 -> 1097 on 2026-08-17"` — **unwritten** |

---

## 7. E2's CONTRAST + RENDER PROOF, RE-DRIVEN ON THE CHANGED CELLS

Harness `/var/tmp/s213gate/probe.py` — the G17-B and G17-C fragments lifted from the repaired
snippet, mounted under `.cn-status-indicator` against the regenerated `canon/canon.css` +
`canon/type.css`, Chromium headless (Playwright; env per `_RUNBOOK-render-verify.md`, reusing
`/var/tmp/pw-browsers-s213e2` + `/var/tmp/fonts-s213e2.conf`; `LD_LIBRARY_PATH` corrected to
`/var/tmp/chromelibs-s213e2/…` — the runbook's `/var/tmp/chromelibs` is empty this session and
launch dies on `libXdamage.so.1`, worth a runbook line). Transitions and animations disabled before
reading (the settle requirement). **FOUR themes × light + dark.**

**G17-B cell ink contrast — byte-identical to E2's receipt line 208, i.e. my repairs moved no colour:**

```
theme/mode         .cell ink CR (ok, warn, err, inf)     .sbar label CR
mono/light         10.59  7.99  5.55  7.04               15.27
mono/dark          10.59  7.99  5.55  7.04               16.48
legacy/light        4.56 10.28  7.87  7.17               11.09
legacy/dark         4.56 10.28  7.87  7.17               16.48
console/light       7.65  6.95  6.02  4.61               15.27
console/dark        7.65  6.95  6.02  4.61               16.48
supercharge/light   7.65  7.53  6.02  4.99               14.02
supercharge/dark    7.65  7.53  6.02  4.99               13.91
```

Every `.sbar` label ≥ **11.09:1**. Computed geometry, live DOM (mono/light shown, all 8 checked):
`.statustable th` → `font-size 14px, font-weight 500, padding 8px/12px`;
`.sbar` → `gap 12px, padding 12px/16px, margin-top 8px, border-left-width 4px`;
`.sbar` label → `16px / 24px / 400`. **Assertions: off-grid 0 · off-ramp 0 · transparent-or-black
fallback 0, across all 8 theme/mode dumps.**

**The render probe CAN FAIL — DRIVEN, #184 class:** one mutant carrying both a geometry break
(`gap:12px`→`10px`) and a dangling var (`--fill:var(--ok-bg-DANGLING)`) fired
`('.sbar','gap','10px','off-grid')` and `('.cell','background-color','rgba(0, 0, 0, 0)','SILENT-BLACK/transparent')`
in **every** theme/mode; canon.css restored byte-identical afterwards. The zero above is a
measurement, not a self-comparison.

---

## 8. FILES CHANGED (all UNCOMMITTED)

| file | change |
|---|---|
| `knowledge/snippets/Status-indicator.reference.html` | grid snaps ×3 rules; raw `font-weight:600` + `font:400 15px/1.35` removed; `t-cm-ctl-14` on 3 `<th>`, `t-ed-body` on 5 `.sbar` labels |
| `knowledge/snippets/CTA-lockup.reference.html` | `var(--uf)`→`var(--font)`; `--font` declared in `:root{}` |
| `knowledge/snippets/Feature-grid-lockup.reference.html` | same pair |
| `knowledge/snippets/Splitter.reference.html` | `--min-pri`→`--spl-min-pri`, `--min-sec`→`--spl-min-sec` (CSS + comments + JS) |
| `knowledge/snippets/Template-settings.reference.html` | `--move`→`--tset-move` (6 sites) |
| `knowledge/_validate_compose.py` | `strip_css_comments()` + applied to canon def/ref extraction |
| `knowledge/canon/canon.css` · `knowledge/showroom/*` · snippet token blocks | **regenerated**, not hand-edited |

## 9. SERIAL SET — RUN HERE (the brief instructed it), ORDERED (#210)

Run in order after the last source edit, all rc 0:
`gen_token_ramp.py` (147 in sync) → `canon/gen_canon_components.py` (135 components) →
`gen_snippet_tokens.py` (4730 bindings, 0 projected) → `canon/gen_theme_cascade.py` (in sync) →
`gen_showroom.py` (135 pages + index).
**Not run — the conductor's:** registry · MIGRATED_SNIPPETS · CATEGORIES · spine · git · dashboard.
No snippet was added or removed and no category moved, so none of those should change; the dashboard
may need a regen because gate results moved.

## 10. OPEN CHOICES — PROPOSED, NOT RULED

1. **`--panel` (§4c)** — nav rail vs multi-column panel tier in supercharge dark. Dave's.
2. **`--l-min` (§4b)** — the fork gate cannot see a parameterised partial. Exempt-in-gate, or ledger
   the fork? Dave's. (This is a `_DS-IMPROVEMENTS.md` candidate; candidature is Dave's, so nothing
   was written there.)
3. **`_validate_compose.py:check_screen()`** reads `<style>` including comments for its rogue-hex
   scan — the same class as §3a, unfixed because it is outside this lane's named edits.
4. **`.demo-note` is demo-chrome and is being projected into canon.css** (`canon.css:6179`, `:10673`).
   `_validate_type_composites.py`'s `CHROME_SEL` treats `.demo*` as never-ships scaffolding, yet the
   component generator ships it. Not repaired here; it is the reason the `--uf` dangle existed at all.
5. **`_RUNBOOK-render-verify.md`** names `/var/tmp/chromelibs` for `LD_LIBRARY_PATH`; that directory
   is empty this session and Chromium dies on `libXdamage.so.1`. The working path today was
   `/var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu`. A runbook line, not a ruling.
6. **The brief's own attribution** (Chart-bullet / Chart-candlestick for the type ratchet) was
   falsified in §2. Worth noting for how the next fan-out brief reads a truncated gate report.

---

*Evidence artefacts (NON-REPO: sandbox `/var/tmp/s213gate/`, this session only — regenerate from §7):*
`probe.py` · `frag.html` · `out.json` · `ba1.log` / `ba2.log` (the two `_build_all` chunks).
