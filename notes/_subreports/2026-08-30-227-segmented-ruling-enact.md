# s227 lane 6 — the segmented ruling, enacted at the mint

**COUNTS: changed 2 · derived 2 · repaired 7 · ruling-shaped 7 · UNPROVEN 3**

Sub: Opus build sub, session #227, lane 6. Conductor: Fable seat.
⛔ No rulings, no store rows, no W-rows, no commits, no promotion past advisory.
Everything ruling-shaped below is a `Q:` for Dave.

Review page for his eye: **`reviews/SEGMENTED-RULING-2026-08-30-v1.html`**
(64 specimens — 4 themes × light/dark × xs/s/m/l × before/after; every specimen is the
canon `.cn-segmented-control` atom under the built `canon.css`, nothing re-drawn.)

---

## Dave's four numbers, and where each one landed

| # | his words | enacted at | value |
|---|---|---|---|
| 1 | "xs is going to be 28 height" | `tokens/layout.json` `size/segmented-control/xs` **+** `themes/apollo-console.overrides.json` | 24 → **28px** |
| 2 | "medium 44 is going to have 2px padding not 4" | `tokens/spacing.json` `padding/segmented-control/m` **+** console overrides | 4 → **2px** |
| 3 | "small and extra large stay the same" | nothing touched at `s` / `l` heights or paddings | — |
| 4 | "the inner radii is just not right for console on the two small sizes … we had a way of calculating it" | `knowledge/gen_radius_derive.py` (the LAW), then minted | console thumb xs **0 → 4**, s **2 → 6** |

**Exactly 6 `$value` edits across the three token stores, and no others** — proven by
`git diff -- knowledge/tokens/ | grep '"\$value"'`, which returns those six lines and
nothing else. Everything else in the token diff is `$note` prose.

⚠ **"extra large"** — the minted scale has **no XL**. It is `xs / s / m / l` (s201-D1,
dimension-first). Read as **`l`**, and `l` was left completely untouched (48px, pad 4,
track 12, thumb 6). If he meant something else, only `l` needs revisiting.

⚠ **`s` looks like it moved and did not, in the sense he meant.** Scale `s` keeps its
height (36) and its padding (2) — "small stays the same". What moved at `s` is its
**console thumb radius** (2 → 6), because `s` is one of the "two small sizes" in his
*radius* sentence. Two different sentences, two different scopes, no contradiction.

---

## The derivation: what was actually wrong, and the input that was changed

Pitfall 2 was real and is now closed. The generator had a **tuned dial that overrode
concentric**:

```
knowledge/gen_radius_derive.py:~78   SEGMENTED_THUMB_DIAL = 6
                                     thumb = max(container_radius − 6, 0)
```

s202-D2 (#202) had replaced the track padding with that flat 6 as the derivation input —
the file's own `$superseded` block records it: *"Console's concentric 4/6/6/8 became
0/2/4/6 in the same motion."* That is precisely the motion Dave means by "we had a way of
calculating it, thats why I dropped it."

**Why the flat dial fails, stated so nobody re-tunes it back by accident:** a flat
subtraction eats a small radius whole. Console xs is a 6px track — `6 − 6 = 0`, a
**square thumb inside a rounded track**. `s` is 8 — `8 − 6 = 2`, near-square. The bigger
scales survive it (10−6=4, 12−6=6) which is exactly why the defect only ever showed on the
two small sizes. Concentric subtracts the *padding* (2), so the inner corner stays parallel
to the outer one at every size.

**The INPUT was changed, not the numbers.** New declared knob, beside the dial:

```python
SEGMENTED_CONCENTRIC_SCALES = ("xs", "s")

def thumb_radius(container_r, padding=None, scale=None):
    if scale is not None and scale in SEGMENTED_CONCENTRIC_SCALES:
        if padding is None:
            refuse(...)                      # UNKNOWN is never defaulted
        return max(container_r - padding, 0) # CONCENTRIC — #227
    return max(container_r - SEGMENTED_THUMB_DIAL, 0)   # dial — s202-D2, m and l
```

The generator then **emitted** 4 and 6, and those emitted numbers were minted. The token
`$note` on each says so and names the emitting path, so a future hand-edit is legible as a
mistake:

```
border-radius/segmented-thumb/xs  $note: "… DERIVED, NOT TYPED … track 6 − padding 2 = thumb 4 …
   Emitted by knowledge/gen_radius_derive.py at themes/apollo-console/segmented/xs/thumb_radius
   — do NOT hand-type this number …"
```

Driven live:

```
xs concentric  track 6  - track padding 2 = thumb 4
s  concentric  track 8  - track padding 2 = thumb 6
m  tuned dial  track 10 - tuned dial     6 = thumb 4
l  tuned dial  track 12 - tuned dial     6 = thumb 6
```

Base themes (mono / legacy / supercharge) have a 0 track, and `max(0 − 2, 0) = 0` under the
new law just as `max(0 − 6, 0) = 0` did under the old one — **no square theme moves**.

---

## The class fix — `--assert-mint`, born ADVISORY, driven live

"I got fed up of it **continually wrong**" is the important half of the ruling, so the
question was *what let a wrong number survive*. The answer is a structural blind spot:

> **`--check` cannot see a wrong mint.** It recomputes the proposal **from the store**, so a
> hand-typed store value produces a self-consistent proposal and `--check` passes. Nothing
> anywhere compared **the mint** to **the derivation**.

New mode in `knowledge/gen_radius_derive.py`:

```
python3 knowledge/gen_radius_derive.py --assert-mint
```

It reads the store and asserts, per theme per scale,
`minted border-radius/segmented-thumb/<scale> == thumb_radius(track, padding, scale)`.
16 theme/scale pairs, all green. Sample output:

```
apollo-console  xs  concentric   track  6 - track padding 2 =  4   minted  4  [apollo-console override] OK
apollo-console  s   concentric   track  8 - track padding 2 =  6   minted  6  [apollo-console override] OK
apollo-console  m   tuned dial   track 10 - tuned dial    6 =  4   minted  4  [apollo-console override] OK
ASSERT-MINT OK — 16 theme/scale pair(s): every minted thumb equals its derived value.
```

**Mutation-proved, against the STORE not the artifact** (a planted proposal value would
only re-prove `--check`). The selftest writes a wrong thumb into
`apollo-console.overrides.json`, runs the assert, and restores:

```
planted [console xs thumb 4 -> 7 in the STORE] -> assert-mint rc=1 DETECTED
SELFTEST: #227 mint-assert proof ran (wrong thumb planted in the STORE, seen, restored).
SELFTEST OK — every planted defect was detected; refusals fired loud.
```

The existing selftest also had to be repaired: its "dial proof" asserted *"padding proven
inert"*, which the #227 law makes a **lie at xs/s**. It now proves **both branches
separately** — padding inert at the dial scales, padding **live** at the concentric scales,
the two branches proven to *disagree* (else the scope set would be doing nothing), and a
concentric call with a missing padding proven to **refuse** rather than default.

`--assert-mint` is **ADVISORY and unwired** — see `Q3`, which is the honest debt.

---

## A1 rider — the overrides that shadowed the atom's radius away

**Found wider than the brief named.** 13 snippets re-declare a bare `.seg{` rule. Sorted by
what the atom's minted tokens are actually *valid for*:

| group | files | disposition |
|---|---|---|
| **2px inset** — matches the minted `padding/segmented-control` at xs/s, so the minted thumb radii are geometrically correct | `Chart-bar`, `Chart-donut`, `Chart-line`, `Chart-pie`, `Filter-toolbar-bar`, `Template-settings` | **REPAIRED (6)** |
| **zero inset** — `.seg` has no padding and `.ind` sits at `top/left:0`; a thumb radius derived for a 2px inset is the *wrong number* here | `Table`, `Template-dashboard`, `Template-list-index`, `Template-report`, `View-options` | **left alone → `Q2`** |
| deliberate pill, different component | `Tab-bar` (`.seg` + `.seg__item`, `border-radius:999px`) | exempt → `Q5` |
| the atom itself | `Segmented-control` | source of truth |

The repair **copies the atom's own construction** rather than inventing one — scale-selected
locals, repointed by the size class:

```css
.seg{--seg-rad:var(--seg-rad-s); --seg-thumb:var(--seg-thumb-s); … border-radius:var(--seg-rad);}
.seg .ind{… border-radius:var(--seg-thumb);}
.seg.sm{--seg-rad:var(--seg-rad-xs); --seg-thumb:var(--seg-thumb-xs);}
.seg.md{--seg-rad:var(--seg-rad-s);  --seg-thumb:var(--seg-thumb-s);}
```

plus the matching `token-manifest` binds and both harness declarations per file.
**Lane 1's trap was avoided deliberately**: a var declared in the harness but absent from
the manifest is copied into canon as a frozen literal, so every bind and every harness
declaration was added together. Verified — `0` local `--seg-rad-s:0` literals leaked into
any `.cn-*` block.

---

## ⚠ Lane 1's repair was INERT in console until this lane ran

**`gen_theme_cascade.py --check` was RED at HEAD, before this lane touched anything.**
Commit `365db63` (#227 lane 1) ran `gen_canon_components.py` and `gen_showroom.py` but not
`gen_theme_cascade.py`, so the theme projections for its new manifest binds were never
written. The consequence is not cosmetic:

- `[data-apollo-theme="console"] .cn-chart-line{--seg-rad-xs; --seg-thumb-xs}` — **missing**,
  so Dave's own `.dv-toggle-seg` hand-patch, promoted to source at B6, resolved to the
  square base value. **Console chart toggles were still square.**
- `[data-apollo-theme="console"] .cn-search-field{--border-radius-control: 8px}` — **missing**,
  so the B5 search-field repair also **never reached console**.

Both are now live (`canon.css:22693-22694`, `canon.css:23249`). This is why
`showroom/chart-combo.html` moved in this lane's diff although its snippet was never edited.

---

## Every moved pixel, named

**Heights — one consumer, one instance.** Only `Segmented-control.reference.html` (and its
showroom page) uses the tier-1 size classes; `grep 'class="seg \(xs\|s\|m\|l\)"'` across
`knowledge/snippets/`, `showroom/`, `dashboard/`, `dashboards/` matches **that file only**.

- `.seg.xs` outer box **24 → 28px**, all four themes, light+dark. Its button is `height:100%`,
  so the inner button goes 18 → **22px** (28 − 2×2 padding − 2×1 border).
- **No chart-toolbar height moved.** The legacy `.seg.sm` ramp does **not** consume `--seg-h`,
  and the chart `.seg` carries its own `--control-h: 32px`. Pitfall 3 is clean.

**Track inset — one consumer, one instance.**

- `.seg.m` padding **4 → 2px**. Outer height stays **44px** (unmoved). The thumb grows: its
  `top/bottom/left` inset goes 4 → 2, so it is **4px taller** and sits 2px further left.
  The inner button goes 34 → **38px**.

**Console thumb radii — atom + the 6 repaired files.**

- `.seg.xs .ind` **0 → 4px**, `.seg.s .ind` **2 → 6px** (console only).
- via the ordinal map: `.seg.sm .ind` **0 → 4px** and `.seg.md .ind` **2 → 6px** in console.
- **mono / legacy / supercharge: 0 everywhere, before and after. Nothing moves.**

**A1 — radius appears where there was none, console only.**

- `.cn-chart-bar|-donut|-line|-pie .seg.sm`: track **0 → 6px**, thumb **0 → 4px**.
- `.cn-filter-toolbar-bar`, `.cn-template-settings`: `.sm` track 6 / thumb 4; `.md` track 8 / thumb 6.
- In the three square themes these all resolve to 0 → 0. **The entire A1 pixel move is console-only.**

---

## ⚠ The sm/xs "exact height match" is NOT one — units

The brief flagged that after xs→28, legacy `sm` (28 high) becomes an exact height match for
the proposed `sm→xs` ordinal map. **Measured, it does not.**

| | measurement | value |
|---|---|---|
| `.seg.xs` | **outer box** (`--seg-h-xs`, border-box) | **28px** |
| `.seg.sm` | **button** (`canon.css:14462 .seg.sm button{height:28px}`) | 28px |
| `.seg.sm` | **outer box** (28 + 2×`--seg-pad-s`(2) + 2×1px border) | **34px** |

So xs's *whole control* equals sm's *inner button* — a near-miss between two different
measurements, not an alignment. **6px apart** outer-to-outer. Recorded on the review page
in those words. The `PROPOSED` comment and the map itself were **not touched**.

---

## Files touched

**Mint (3)** — `knowledge/tokens/layout.json` · `knowledge/tokens/spacing.json` ·
`knowledge/tokens/themes/apollo-console.overrides.json`

**Machinery (1)** — `knowledge/gen_radius_derive.py` (concentric scope knob, per-scale law,
`thumb_inputs()` audit trail, `--assert-mint`, three new selftest arms, repaired dial proof)

**Snippets, A1 (6)** — `Chart-bar` · `Chart-donut` · `Chart-line` · `Chart-pie` ·
`Filter-toolbar-bar` · `Template-settings` `.reference.html`

**Regenerated, never hand-edited (11)** — `knowledge/_derive-radius-proposal.json` ·
`knowledge/canon/canon.css` · `knowledge/snippets/Segmented-control.reference.html`
(4 projected values) · `showroom/{segmented-control,chart-bar,chart-donut,chart-line,chart-pie,chart-combo,filter-toolbar-bar,template-settings}.html`

**New (1)** — `reviews/SEGMENTED-RULING-2026-08-30-v1.html`

Generators run, in this order, **never `_build_all.py`**:

```
gen_radius_derive.py            → WROTE _derive-radius-proposal.json (4 themes)
gen_snippet_tokens.py           → 4858 bindings, 4 value(s) projected
canon/gen_canon_tokens.py       → 577 root vars, 195 dark overrides
canon/gen_canon_components.py   → generated 135 components
canon/gen_theme_cascade.py      → 230 override path(s), 388 component projection(s)
gen_showroom.py                 → 135 page(s), 8 written, 0 orphans
```

## REPLAY-THESE

```
python3 knowledge/gen_radius_derive.py --check          # rc=0
python3 knowledge/gen_radius_derive.py --assert-mint    # rc=0  ← the new advisory
python3 knowledge/gen_radius_derive.py --selftest       # rc=0  ← incl. store-mutation arm
python3 knowledge/gen_snippet_tokens.py --check --quiet  # rc=0
python3 knowledge/canon/gen_canon_components.py --check  # rc=0
python3 knowledge/canon/gen_theme_cascade.py --check     # rc=0  (was RED at HEAD)
python3 knowledge/gen_showroom.py --check                # rc=0
python3 knowledge/_validate_snippets.py                  # rc=0, 135 snippets, 0 failures
python3 knowledge/gen_component_partials.py --check       # rc=0
```

**Ratchets: unmoved.** `_validate_type_composites.py` reports **1091** violations. Not
asserted — *measured on both trees*: stashed the whole lane, re-ran on clean HEAD, got
**1091**, restored. This lane moves the type debt by exactly **0**. Nothing typed was touched.

**No gate refused any of Dave's four numbers.** Pitfall 1 did not fire: no snap or ratchet
gate objected to 28.

---

## `Q:` for Dave — ruling-shaped, not settled

**`Q1:` Should concentric extend to m and l?** *(the one that matters)*
#227 moved two things that meet at `m`. Padding dropped to 2, and concentric came back at
xs/s only — so console `m` now reads track 10, padding 2, thumb 4, where concentric gives
**8**. `l` reads track 12, padding 4, thumb 6 vs concentric **8**. The dial now sits **4px
further from concentric at m** than it did before the padding moved. He said only the two
small sizes were wrong, so m and l were left alone. Extending is one constant —
`SEGMENTED_CONCENTRIC_SCALES = ("xs","s","m","l")` — and a re-mint. **The m and l cards in
the two Console rows of the review page are drawn for exactly this decision.**

**`Q2:` The five zero-inset `.seg` consumers.** `Table`, `Template-dashboard`,
`Template-list-index`, `Template-report`, `View-options` re-declare `.seg` with **no padding**
and `.ind` at `top/left:0`. They were deliberately **not** repaired: with a zero inset the
concentric thumb equals the **track** radius, and no token carries that value — binding
`--seg-thumb-s` there would ship a knowingly wrong number. Either they gain a 2px inset (and
become the same case as the six repaired), or a zero-inset thumb slot gets minted. His call.

**`Q3:` `gen_radius_derive.py` has NO consumer — none, and never had one.** Probe run:
`grep -rn "gen_radius_derive" --include=*.py --include=*.yml --include=*.sh --include=*.toml`
across the repo returns **only the file itself**. It is absent from `_build_all.py` and from
`.github/workflows/gates.yml`. So the defect had **two independent covers**: nothing ran the
derivation's checks, and `--check` structurally could not see a wrong mint anyway.
`--assert-mint` closes the second. The first is a one-line wiring, **not taken here** (that is
promotion, and `_build_all.py` is shared spine other lanes may be editing). Proposed rows:

```python
("radius derivation — proposal determinism (s200-D1)", "gen_radius_derive.py", ["--check"]),
("radius mint assert — minted thumb == derived (advisory, #227)", "gen_radius_derive.py", ["--assert-mint"]),
("radius derivation selftest (s200-D1/#227)", "gen_radius_derive.py", ["--selftest"]),
```

**`Q4:` The `sm→xs` ordinal map now has a wider blast radius.** It stays `PROPOSED` and was
not edited — but mirroring the atom's tier-2 ramp into 6 more snippets means 6 more files now
*depend* on that proposed reading. If he picks the nearest-height reading instead, those 6
files change with it. Both readings are still drawn in
`reviews/SEGMENTED-ADOPTION-2026-08-25-v1.html`.

**`Q5:` `Tab-bar` uses `.seg` for a different component.** `.seg` + `.seg__item`,
`border-radius:999px` — a pill tab bar, not the segmented atom, sharing the class name. Left
untouched. Worth renaming before the collision bites.

**`Q6:` `canon/gen_canon_tokens.py` has no `--check` and WRITES when given one.**
`gen_canon_tokens.py:341` tests only `if "--selftest" in sys.argv`; every other flag falls
through to the write path. Passing `--check` at baseline **rewrote `canon.css`** (harmlessly —
byte-identical, `git status` stayed clean, verified). This is the #158 write-by-default class
the help-gate exists for, in a generator the help-gate does not cover. Not fixed here — out of
this lane's ruling.

**`Q7:` The review page has no store row** (forgotten-document class, #185). Minting one is
the conductor's act, not this sub's.

---

## UNPROVEN (3)

1. **Every render.** No headless browser and no `pip` in the build VM (disk 100% full). All
   proofs here are **structural** — regenerated artifacts parsed and quoted, generator
   `--check` return codes, `git diff` counts. Nobody has *looked* at a rendered pixel.
2. **That 4 and 6 are right to Dave's eye.** The arithmetic is proven and the law is restored;
   whether console xs/s *look* right at those radii is his judgement, which is what the review
   page is for.
3. **That the six A1 files should follow the `sm→xs` ordinal map** — see `Q4`. The map is
   `PROPOSED`, so the radius each repaired toolbar now takes is proposed too.
