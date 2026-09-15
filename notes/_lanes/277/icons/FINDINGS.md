# LANE IX — FINDINGS — icons (666) then logos (12): the measured shape

#277 · 2026-09-15 · prep for `s269-D1` STEP 4 · READ-ONLY, nothing landed, no review page, no decisions taken.

Every figure below was re-run in this lane. The command sits beside the number. Nothing is quoted
from `A-inventory.json` as a measurement — `A-inventory.json` is only the **baseline** I am checking.

Working directory for every command: repo root. The commands that read `knowledge/` internals were
run from `knowledge/` and say so.

---

## 1. The corrected inventory — every A-inventory figure re-run

`A-inventory.json` was generated **2026-09-14** (lane 269-A). Re-measured **2026-09-15**.

### 1a. `assets — icons`

| A-inventory claim | re-measured | delta |
|---|---|---|
| `records_in_source` 666 | **666** | unchanged |
| `records_in_graph` 0 | **0** | unchanged |
| Miscellaneous 24 | **24** | unchanged |
| Social 7 | **7** | unchanged |
| Touch 10 | **10** | unchanged |
| Informative 131 | **131** | unchanged |
| Volume and audio 16 | **16** | unchanged |
| Media 104 | **104** | unchanged |
| Arrows and chevrons 24 | **24** | unchanged |
| Products and services 208 | **208** | unchanged |
| Global controls 122 | **122** | unchanged |
| Status Icons 20 | **20** | unchanged |
| `find knowledge/assets/icons -type f \| wc -l` → 677 | **677** | unchanged (composition confirmed below) |
| "86 metas mention icons in prose" | **86** | unchanged |
| "17 rulings mention icons" | **17** | unchanged (now of 590 rulings, was 578) |

Commands:

```
python3 -c "import json;m=json.load(open('knowledge/assets/icons/icons.manifest.json'));print(m['\$total'],m['\$counts'])"
  -> 666 {'Miscellaneous': 24, 'Social': 7, 'Touch': 10, 'Informative': 131, 'Volume and audio': 16,
          'Media': 104, 'Arrows and chevrons': 24, 'Products and services': 208,
          'Global controls': 122, 'Status Icons': 20}

find knowledge/assets/icons -type f | wc -l               -> 677
find knowledge/assets/icons -type f -name '*.svg' | wc -l -> 667
grep -ril 'icon' knowledge/components/*.meta.json | wc -l -> 86
grep -ril 'logo' knowledge/components/*.meta.json | wc -l -> 9
python3 -c "...\bicons?\b over ruled+says of _rulings.json..."  -> 17 of 590
```

The 677 breaks down as **667 SVG + 10 non-SVG** (`icons.manifest.json`, `_README.md`,
`_export-icons.py`, `dynamic-weight/{dynamic-icons.js,icon-weight-decisions.json,README.md,
playground.html,RUNBOOK-icon-conversion.md}`, and **two `.DS_Store` files** —
`assets/icons/.DS_Store` and `assets/icons/status-icons/.DS_Store`). The total is unchanged from
A-inventory but its parenthetical did not name the `dynamic-weight` JS/HTML/RUNBOOK, and `.DS_Store`
is noise any node builder must exclude explicitly.

**Manifest ↔ disk reconciliation (new — A-inventory never did it).** Every one of the 666 manifested
`file` paths resolves on disk; **zero** manifest entries are missing. Exactly **one** SVG on disk is
NOT in the manifest: **`menu-search.svg`**. That is not a stray — it is the glyph `s212-D9` ruled
("Library asset: knowledge/assets/icons/menu-search.svg"), dated 2026-08-21, while the manifest's
`$generated` is **2026-06-17**. **The manifest is two months stale by exactly one ruled asset.**
Slugs are unique across all 666 (no collisions), so `slug` is a safe node id.

```
# run from knowledge/ : walk assets/icons for *.svg, set-diff against manifest `file` values
on disk NOT in manifest: ['menu-search.svg']
in manifest NOT on disk: []
unique slugs: 666   duplicate slugs: []
```

### 1b. The `active` flag pairing — A-inventory did not measure this; here it is

`active` is a **boolean on every one of the 666 records** (100% key coverage). It is **exactly**
predicted by the slug: `active == True` ⟺ the slug matches `-active(-\d+)?$`, on all 666 records,
**zero mismatches either way**.

| measure | value |
|---|---|
| records with `active: true` | **234** |
| slugs ending `-active` (no numeric suffix) | 218 |
| slugs matching `-active(-N)?$` | **234** (the extra 16 are `-active-2` / `-active-3`) |
| active records whose base slug exists in the manifest | **232** → 232 resolvable `activeVariantOf` edges |
| orphan `-active` (base slug absent) | **2** — `circle-active`, `menu-more-verticle-active` |
| base icons (non-active) | **432** |
| base icons with ≥1 active variant | **216** |
| base icons with **no** active variant | **216** |
| bases carrying >1 active variant | 15 (`dentist` ×3; `alert`, `electricity`, `laboratory`, `voice`, `renew`, `reward`, `user-staff`, `e-coupon`, `jade-lifestyle`, `contact-chat-ai`, `financial-health-check`, `traditional-chinese-medicine`, `employee-banking-solution`, `withdraw-overpayment` ×2 each) |
| cross-group twins (base and variant in different groups) | **0** |

**The manifest agrees with what #264 shipped.** Eight records carry a `$derived` key — the only
non-standard key anywhere in the 666 — and each names the repair verbatim:

```
device-mobile-active · document-report-active · newspaper-active · online-banking-active ·
presentation-active (Media) · cheque-active · finances-active (Products and services) ·
add-circle-active (Global controls)
  $derived: "#264 2026-09-09 — geometry from <base>.svg by notes/_lanes/264-active-gen.py (A1),
             graded A1 by Dave; not a Figma export"
```

`s264-D3` `governs` those same eight `.svg` paths. Manifest and ruling agree; nothing is orphaned by
the #264 repair.

⚠ **`-active-2` / `-active-3` is a ruling-shaped residue, not a measurement.** Sixteen records mean a
base can have two or three "active" glyphs and nothing in the corpus says which is *the* active twin.
`_validate_icons.py`'s twin arm assumes the single form (`x` → `x-active`). An `activeVariantOf` edge
can be drawn for all 232 without resolving this; a `defaultActive` edge cannot. **This is Dave's, and
it is one of the four decisions in §5.**

### 1c. `fillMode` and the theming claim

| measure | value |
|---|---|
| `fillMode == "currentColor"` | **613** |
| `fillMode == "baked"` | **53** |
| distinct hex values across all `fills` arrays | **6** |
| `#333333` | 648 occurrences |
| `#DB0011` 36 · `#00847F` 7 · `#A8000B` 5 · `#305A85` 1 · `#FFBB33` 1 | |
| every `currentColor` record's `fills` length | **1**, always (613/613) |
| `baked` records' `fills` length | 2 ×35, 1 ×15, 0 ×3 |

**The `fills` array does not join to a token, and A-inventory's `themedBy` candidate rests on a join
that does not exist.** `semantic-colour.json` carries exactly **8** `icon/*` leaves (of 393 total):

```
icon/default/light         = #1A1A1A      icon/default/dark         = #FFFFFF
icon/default-reverse/light = #FFFFFF      icon/default-reverse/dark = #FFFFFF
icon/disabled/light        = #E1E1E1      icon/disabled/dark        = #808080
icon/on-inverse/light      = #FFFFFF      icon/on-inverse/dark      = #333333
```

`#333333` — the value 648 of the 666 records carry — matches **`icon/on-inverse/dark` only**, and
that is a coincidence of the Figma export's grey, not a binding. `icon/default/light` is `#1A1A1A`.
The `fills` array records **what the artwork was before the rewrite**, not what the icon inherits. A
`currentColor` icon inherits whatever the *consuming context* sets; the relation is icon → *any*
`icon/*` token, identically for all 613. **`icon→token (themedBy)` is contentless at the icon
level** — see §3, rank 7.

### 1d. `assets — logos`

| A-inventory claim | re-measured | delta |
|---|---|---|
| `records_in_source` 12 | **12** | unchanged |
| `records_in_graph` 0 | **0** | unchanged |
| `find knowledge/assets/logos -type f \| wc -l` → 13 | **13** | unchanged (12 SVG + `_export-logos.py`) |
| "9 of 138 metas mention logo in prose" | **9** | unchanged |
| the 3 × 2 × 2 grid | **confirmed, complete, regular** | unchanged |

```
ls knowledge/assets/logos/
_export-logos.py
hexagon-{dark,light}-{colour,mono}.svg                    (4)
masterbrand-{dark,light}-{colour,mono}.svg                (4)
masterbrand-identifier-{dark,light}-{colour,mono}.svg     (4)
```

All 12 cells of `{hexagon|masterbrand|masterbrand-identifier} × {light|dark} × {colour|mono}` are
present, none extra, filename pattern `<lockup>-<light|dark>-<colour|mono>.svg` with **no
exceptions** — so lockup / theme / colourMode are three parseable fields of the filename, not prose.
`knowledge/guidelines/logos.md` **exists** (27 lines) and states the same 12 in its own words
("That's **12 variants** (3 lockups × {Colour, Monotone} × {On Light, On Dark})"), with
`related_assets: knowledge/assets/logos/`. There is **no logos manifest** — the filenames are the
manifest.

**Rulings on logos: 2 of 590** (`\blogos?\b` over `ruled`+`says`). `s230-D2` is the load-bearing one.
**Zero rulings name a logo `.svg` path in `governs`** — `s230-D2` governs six *snippets*, not assets.

### 1e. Corpus figures the two families will land against

```
ls knowledge/components/*.meta.json | wc -l   -> 138   (137 component nodes; EXAMPLE- is skipped by the explorer)
python3 knowledge/_validate_kg.py             -> metas checked: 139  (138 + _proforma)
# run from knowledge/, via _build_kg_explorer.extract() / extract_extra() imported in memory
base:  1,003 nodes / 1,555 edges     extra: 2,890 nodes / 5,067 edges
TOTAL: 3,893 nodes / 6,622 edges
base node types: pattern 380 · context 222 · component 137 · snippet 137 · rule 60 · shape 23 ·
                 intent 14 · ruling 14 · role 12 · ux 4
ls -la notes/_KG-EXPLORER.html -> 2,889,309 B
```

No `icon:` or `logo:` node exists anywhere. (`_validate_kg.py`'s `REF_RE` admits ten kinds and
neither is one; the one grep that looks like a hit — `sidebar-nav.meta.json` — is the prose string
`item.icon:`, not a ref.)

---

## 2. Node kinds, costed

### 2a. Icons — three options

| option | nodes added | edges it can carry | explorer payload | grammar change |
|---|---|---|---|---|
| **A. `iconGroup` only (10)** | 10 | none worth drawing (10 hubs, nothing hangs off them) | negligible | +1 kind |
| **B. `icon` only (666)** | 666 | `activeVariantOf` 232, `usesIcon` 371, `ruledBy` 9 | ~+250 KB | +1 kind |
| **C. both (676)** | **676** | B **plus** `inGroup` 666 | **+271,461 B = +9.4%** | **+2 kinds** |

Measured payload for option C, serialised exactly as `_build_kg_explorer.py` serialises
(`json.dumps(..., separators=(',',':'))`, same node/edge dict shape it writes):

```
simulated icon-family payload bytes: 271,461   nodes 676   edges 1,269
current explorer bytes: 2,889,309             ->  +9.4%
```

Option C is what I would *propose* (not a decision): `iconGroup` is what makes 666 nodes navigable —
without it, **176 icon nodes have no edge at all** (measured: the 216 bases with no active variant
plus the 2 orphan actives, minus the 42 of those a component uses). With `inGroup` every icon has at
least one edge and the family has ten legible hubs.

⚠ **Explorer layout, not payload, is the real cost.** `place_extra()` lays each new family out on its
own and parks it beside the base graph; the largest family today is `rule` at 410 nodes and the whole
extra set is 2,890. 676 more nodes is **+17.4% on the whole graph's node count**. That is a *visual*
judgement Dave has to make on a screenshot, which is why §5's lane ships a driven screenshot before
it ships an opinion.

### 2b. Logos — one option

`logo` (12) — nodes added **12**, payload **~5 KB (+0.2%)**, one grammar kind. There is no
sub-taxonomy worth a second kind: lockup / theme / colourMode are **node properties parsed from the
filename**, not nodes. (A `lockup` kind would add 3 nodes and 12 edges to say what a field says.)

### 2c. `_validate_kg.py` — the grammar cost, mirroring #276

The #276 precedent (`577c82d`, read with `git show --numstat`) is the template, and it is small. Two
places:

```
knowledge/_validate_kg.py:87   REF_RE = re.compile(r"^(component|pattern|context|snippet|ruling|role|intent|shape|rule|ux):.+$")
knowledge/_validate_kg.py:88   NODE_KINDS = ("component","pattern","context","snippet","ruling","role","intent","shape","rule","ux")
```

Add `icon|iconGroup|logo` to both, plus a resolver store each — **by addition, exactly as #276 did
for `rule:`/`ux:`** — and against the file that IS their home (ADR-0017 write-once), never a second
registry:

* `icon:` resolves against `knowledge/assets/icons/icons.manifest.json` (666 slugs) — **plus
  `menu-search`, or the manifest is regenerated first; blocker B1.**
* `iconGroup:` resolves against the same manifest's `groups` keys (10).
* `logo:` resolves against `glob('knowledge/assets/logos/*.svg')` (12) — the filenames are the store.

`load_schema_edge_types()` already reads props/required **per edge type** from its own `items.$ref`
(the #276 change), so a new edge type carrying its own `$why`-style required field costs **one scoped
definition in `meta.schema.json`** and **zero** further work in `_validate_kg.py`.

Estimated land diff, by the #276 measure: `_validate_kg.py` ~+20/−4, `meta.schema.json` +30/−0,
`_build_kg_explorer.py` ~+15/−2 (one `--c-<kind>` and one `--f-assets` per theme block ×3, one
`FAMLABEL`, one `NEWFAM`, one `famOn:0`, one `EDGEFAM` line per edge type). **Estimate, declared as
an estimate — I did not write the patch.**

---

## 3. Edge kinds, ranked by defensibility

**Ranked by whether it can be authored, not by how many edges it makes.** "Structural" = read from a
field, a filename, or a byte-match. "Prose" = a regex over sentences → **REFUSED** (`s274-D12`,
`s276-D5`).

| # | edge | join | kind | count | verdict |
|---|---|---|---|---|---|
| 1 | `icon → iconGroup (inGroup)` | manifest `groups` key | **structural** | **666** (0 null) | **build** |
| 2 | `logo → theme (defaultFor)` | `s230-D2`, Dave verbatim | **authored, his words** | **2** | **build** |
| 3 | `icon → icon (activeVariantOf)` | slug `-active(-N)?$` + base in manifest | **structural** | **232** (2 declared orphans) | **build** |
| 4 | `component → icon (usesIcon)` | **byte-match of inline `<path d>` against the library** | **structural** | **371** across 105 components / 81 icons | **build** |
| 5 | `component → logo (usesLogo)` | `src="…/assets/logos/<file>.svg"` attribute | **structural** | **18** across 9 components / 4 logos | **build** |
| 6 | `icon → ruling (ruledBy)` | ruling `governs` entry ending `assets/icons/*.svg` | **structural** | **9** (2 rulings) | **build, trivially** |
| 7 | `icon → token (themedBy)` | `fillMode` + `fills` hex | **structural but contentless** | 613 × identical | **do not build** — §1c |
| 8 | `logo → guidelineDoc (governedBy)` | `logos.md` front-matter `related_assets` | structural but **1 target, 0 rules** | 12 → 1 | **do not build yet** — B3 |
| 9 | `component → icon` **from meta prose** | regex / slug-token over meta text | **PROSE** | **1,736** | ⛔ **REFUSED** |
| 10 | `logo → ruling` | ruling `governs` naming a logo `.svg` | structural | **0** | cannot be built — no such entry exists |

### Rank 4 is the crux, and the answer is YES — but not by the route A-inventory proposed

A-inventory proposed `icon→component (usedBy — 86 metas mention icons in prose)`. **That route is
refused, and I can put a number on why.** Testing every exact manifest slug as a whole token against
every meta's text:

```
metas containing >=1 exact manifest slug as a token : 138 of 138
total (meta, slug) prose pairs                      : 1,736
top matches: accessibility x138 · no x136 · export x64 · error x59 · collapse x52 ·
             user x52 · link x50 · card x50 · block x48 · script x43 · time x41 …
```

`accessibility` is an icon slug. So is `no`. So is `time`. The prose join fires on **every meta in the
corpus** and produces 1,736 pairs of which the overwhelming majority are the English language, not an
icon. **This is the exact route `s274-D12` and `s276-D5` refused, and it deserves refusing.**

**The defensible route already exists in the repo and nobody has read it as a join.**
`knowledge/_validate_icons.py` (the icon-source GATE, promoted from advisory 2026-06-24) *already*
builds a byte-match index of every library glyph's normalised `d=` path data and matches every inline
SVG path in every snippet against it. That is a **geometry byte-match**, not a regex. I re-derived it
independently here using the gate's own `norm()`/`DRE` rules:

```
# run from knowledge/
library distinct normalised path-d keys : 758
snippet .html files scanned             : 139
inline <path d=> occurrences            : 594   (unmatched 102; <svg> with no <path> 837 — sprite <use> refs)
snippets with >=1 library byte-match    : 106
distinct (snippet, icon) pairs          : 372
distinct icons used                     : 81
pairs unresolvable to a manifest slug   : 0
```

Snippets then resolve to components through the graph's **own** `snippet → component` mapping
(`_build_kg_explorer.extract()` yields 137 such edges; no new inference):

```
of the 106 icon-bearing snippets, 105 map to a component; 1 does not
  (the exception is _REVIEW-66-scatter-title-before.html, a review scratch file, not a component snippet)
component -> icon distinct pairs : 371  across 105 components / 81 distinct icons
```

Cross-check against the prose signal, which is where the value shows:

```
metas mentioning 'icon' in prose               : 86
components with a byte-matched glyph           : 105
prose-only (mentions icons, no matched glyph)  : 13
STRUCT-ONLY (uses a glyph, never says 'icon')  : 32
both                                           : 73
```

**32 components use a library glyph and never mention the word "icon" in their meta.** The prose
route would have missed every one of them, and would have invented 1,736 pairs instead. The
byte-match route finds all 105 and invents nothing.

**Declared limits of rank 4, honestly:**
1. It measures the **reference snippet**, not the component's contract. An icon a snippet happens to
   demonstrate is not necessarily an icon the component *requires*. Name the edge for what it
   measures — `usesIcon` (observed in the reference render) — never `requiresIcon`.
2. **81 of 666 icons are used; 585 are not.** The edge illuminates 12% of the family. That is the
   true finding, not a shortfall: the library is a catalogue and the system consumes a twelfth of it.
3. 102 inline paths byte-match nothing. `_validate_icons.py` classifies those as `bespoke` (declared
   `data-bespoke=`) or UNKNOWN; I did not re-classify them, and no edge is drawn for them.
4. The 837 `<svg>` elements with no `<path>` are sprite `<use href="#…">` references into a `<symbol>`
   defined in the same file; the symbol's own path is counted once, so the *pair set* is correct but
   per-use **frequency** is not measured, and no weight should be put on an edge.

### Rank 2 — `s230-D2` names exactly two of the twelve

Dave's words, read from `knowledge/_rulings.json` (`s230-D2`, 2026-08-31, by Dave — quoted from the
ruling record's `says` field, **not** via `_quote_gate.py`, whose index covers neither `notes/_lanes/`
nor `says`):

> `use this as teh default logo "masterbrand-light-colour"` and
> `use this for dark mode masterbrand-dark-colour`

So the two named are **`masterbrand-light-colour`** (light chrome) and **`masterbrand-dark-colour`**
(dark chrome). That is `logo → theme (defaultFor)`, 2 edges, his word, nothing inferred.

**The remaining ten are bound by nothing.** Measured, not assumed:

* `masterbrand-{light,dark}-mono` — used, but **only** by `template-auth`, and no ruling says why.
* `masterbrand-identifier-*` (4) and `hexagon-*` (4) — **zero references anywhere in the corpus**.
  `grep -rhoE '(src|href)="[^"]*assets/logos/[^"]*"' knowledge/snippets/` returns only the four
  masterbrand files. Eight of twelve logos are unbound in exactly the sense `s230-D2` was written to
  fix.
* `knowledge/guidelines/logos.md` explicitly **declines** to bind them: *"the detailed logo standard …
  lives on create.hsbc"*, *"No design tokens."* The doc is a sticker sheet, not a rule source.

The measured `component → logo (usesLogo)` set, all 18 from `src=` attributes:

```
app-shell-doormat          masterbrand-{light,dark}-colour
app-shell-focused          masterbrand-{light,dark}-colour
app-shell-multi-column     masterbrand-{light,dark}-colour
app-shell-side-nav         masterbrand-{light,dark}-colour
app-shell-split            masterbrand-{light,dark}-colour
app-shell-top-nav          masterbrand-{light,dark}-colour
navigations                masterbrand-{light,dark}-colour
template-dashboard-bento   masterbrand-{light,dark}-colour
template-auth              masterbrand-{light,dark}-mono        <-- the only mono consumer
```

The **prose set and the structural set differ**, again in the useful direction: the 9 metas that say
"logo" include `payment-card-visual` and `qr-code` (which reference no logo file) and **miss**
`app-shell-split` and `template-dashboard-bento` (which do). Structural wins here too.

`app-shell-nav-rail` is deliberately absent — `s230-D2` records it as *"deliberately NOT rebound
(56px rail head, no lockup fits — a ruling-shaped residue that stays Dave's)"*. Any lane that draws
this family must leave that gap as a **declared null with a `$note`**, never quietly complete it.

### Rank 6 — the two rulings that already name an asset

```
s212-D9 -> menu-search                         (governs knowledge/assets/icons/menu-search.svg)
s264-D3 -> add-circle-active · cheque-active · device-mobile-active · document-report-active ·
           finances-active · newspaper-active · online-banking-active · presentation-active
```

9 edges, free, from a `governs` field. **But `menu-search` is not in the manifest** (§1a), so this
edge and blocker B1 are the same problem wearing two hats.

---

## 4. The blockers — what must exist first, and whose it is

**B1 — the icon manifest is one asset stale. OURS (a lane, not Dave).**
`icons.manifest.json` `$generated: 2026-06-17`; `menu-search.svg` was ruled in on 2026-08-21 by
`s212-D9`, is on disk, and is not manifested. If `icon:` resolves against the manifest, the graph
cannot hold the one icon Dave personally approved. Fix before any land: re-run `_export-icons.py`
(or add the record **by textual span**, never a re-dump — the #179/#275 class), then re-check `$total`
666 → 667 and the group count it lands in. **This is a build step, not a decision.** Nothing else in
the family is stale: 0 manifest entries are missing from disk.

**B2 — token nodes do not exist, and `themedBy` needs them. NOT OURS AND NOT NEXT.**
Zero `token:` nodes in the graph (§1e). Even if they existed, §1c shows the per-icon join is
contentless — 613 identical edges. The real relation is **component → `icon/*` token**, and that one
already has a structural home: `tokens.icon` is a **real key in 28 of 138 metas**, carrying values
like `"icon/default"`. That is a `component → token` edge waiting for a token family, and it belongs
to the **tokens** gap (932 records, A-inventory), not to this one. **Recommendation: this family's
proposal explicitly declines `themedBy` and hands the 28-meta `tokens.icon` observation to the tokens
lane.**

**B3 — there is no logo rule source. NOT OURS (it is create.hsbc's).**
`_rules-index.json` holds 470 rules; `file == 'logos.md'` → **0**. `file == 'icons.md'` → **17**
(`icon-001`…`icon-017`). So `icon → rule (governedBy)` has a clean filename join — the same shape
`s276-D3` used, "filename join, never a regex" — and **`logo → rule` has nothing to join to.**
`logos.md` itself says the standard lives off-repo. `brand-refresh-assets.md` carries `logo26-001`
(*BLOCKING*: an HSBC logo appears at least once on every communication) — **one** rule, about
*presence*, not about which of the twelve. Two of the 17 `icons.md` rules are directly load-bearing
and should be surfaced, not buried: `icon-010` (*"use the active version to differentiate default vs
selected"* — the `activeVariantOf` edge stated as a rule) and `icon-014` (*"Do not export SVGs from
the HSBC Icon Library file … Download the SVGs from the UI Centre"* — which our own exporter does;
already flagged in `logos.md` as "internal prototype assets").

**B4 — the `-active-2/-3` ambiguity. DAVE'S.** §1b. Blocks `defaultActive` only; does not block
`activeVariantOf`.

**B5 — no fonts manifest (A-inventory's fonts family, 111). NOT A BLOCKER HERE.** Named in the brief;
it touches neither icons nor logos. Left where it is.

**Not a blocker, but on the record:** two untracked files appeared at the repo root at 21:33 during
this wave — `artefact` (0 B) and `rule?` (49 B, containing `--- does any edge type point component-
or role-`). They are not mine, they look like a shell redirect accident from a sibling lane
(`> rule?` / `> artefact`), and I have **not** touched them — read-only outside my lane. Someone
should sweep them before the wrap commit.

---

## 5. A proposed two-lane plan — DRAFT for the conductor, <= 4 decisions

Mirrors the RK/RL shape steps 2 (#274) and 3 (#275) used: **propose lane → verifier in the same wave
→ land lane on one word.**

### Lane RI (propose) — read-only, nothing lands

1. Write `knowledge/gen_kg_icons.py` — `--dry-run` / `--land --ratified <id>`, mirroring
   `gen_kg_rules.py` and `gen_kg_principles.py`. Emits `_icon_nodes.json` (676 nodes) +
   `_logo_nodes.json` (12), and the six buildable edge types from §3 ranks 1–6.
2. **Do B1 first, as a build step:** reconcile `menu-search` into the manifest by textual span and
   re-report `$total`.
3. Re-derive the rank-4 byte-match **inside the generator** from `_validate_icons.py`'s own
   `norm()`/`DRE` rules — never a second copy of the geometry index, never a regex. Declare the four
   limits from §3 in the file's docstring.
4. Selftest with mutation bites, >=12, each proven both ways: a bogus slug drives it red; a renamed
   required key drives it red; a prose-derived pair is rejected by construction.
5. Build the review page, drive it in chromium, and **review the screenshots by eye** before
   presenting (the #268 art-director rule). Ship a chip-on and a chip-off screenshot so Dave can judge
   +17.4% node count visually, not arithmetically.
6. Verifier lane RV in the same wave, recounting every figure independently.

### The review page asks Dave exactly four things — drafted as one-liners

> **RI-1 · Do the icons enter the graph as 666 `icon:` nodes plus 10 `iconGroup:` hubs, as the 666
> alone, or as the 10 groups alone?**
> *(a) both, 676 · (b) icons only · (c) groups only · (d) not yet*

> **RI-2 · The `component → icon` edge is a geometry byte-match against the library (371 edges, 105
> components, 81 of 666 icons); the prose route produces 1,736 pairs and is refused. Draw it?**
> *(a) draw it as `usesIcon` · (b) draw it, different name · (c) don't draw it*

> **RI-3 · Fifteen icons have two or three `-active` variants (`dentist-active`, `-active-2`,
> `-active-3`). `activeVariantOf` draws all 232 regardless. Does one become the default active twin,
> or does that stay open?**
> *(a) stays open, draw the 232 · (b) I'll pick the defaults · (c) bare `-active` is the default by rule*

> **RI-4 · `s230-D2` binds two of the twelve logos. The other ten — four `masterbrand-identifier`,
> four `hexagon`, two `masterbrand-*-mono` — are referenced by nothing except `template-auth` (mono).
> Do they enter as unbound nodes, or wait?**
> *(a) all 12 enter, 10 unbound and visibly so · (b) only the 4 masterbrand that ship · (c) logos wait*

**Not asked, deliberately:** `themedBy` (B2 — declined by the lane, handed to the tokens gap),
`logo → guidelineDoc` (B3 — one target, zero rules, nothing to say), and the `app-shell-nav-rail` gap
(already ruling-shaped residue inside `s230-D2`; it enters as a **declared null with a `$note`**,
which is a build rule, not a question).

### Lane RL3 (land) — on one word

`gen_kg_icons.py --land --ratified <the ratifying id>` · `_validate_kg.py` grammar +3 kinds **by
addition** (§2c) · `meta.schema.json` scoped definitions +N/−0 · explorer `v1.13 → v1.14`, fifth
additive family `assets`, chip **OFF by default** (the #275 precedent) · regen · chromium drive ·
`--numstat` receipt · `notes/_lanes/<n>/…/LAND-REPORT.md`.

---

## 6. Gauge at close, and every gate line I ran

```
$ python3 knowledge/_validate_kg.py
metas checked: 139
ref:null + $note (declared, awaiting Dave's-eye migration): 90
resolutions consumed (s135-D4, KG-REVIEW-VERDICTS-2026-08-08-s135-v1.json): 82 ruled verdicts
  asserted present (MERGE 5 / PROMOTE 52 / ATTACH 25)
_validate_kg.py: OK — every ref parses+resolves, every null carries a note, every meta has
  provenance, edges match schema, gen_kg_edges.py is idempotent-clean, and the s135-D4
  resolutions input was consumed.
rc = 0                                    OK (I changed nothing it reads)

$ git status --porcelain
 M notes/_REHEARSAL-LOG.jsonl            <- NOT MINE (sibling lane in this wave)
 M notes/_dream/_GRADE-DECISIONS.jsonl   <- NOT MINE (sibling lane in this wave)
?? artefact                              <- NOT MINE, stray, untouched (§4)
?? notes/_lanes/277/                     <- mine + two sibling lanes
?? rule?                                 <- NOT MINE, stray, untouched (§4)
                                          my only write is notes/_lanes/277/icons/FINDINGS.md

$ python3 knowledge/_checkin.py           (run at the seam)
  SEAM CLEAR — provenance complete, integrity digest matches, every field re-derives, no UNKNOWN.
  GRADES: 2 STALE hooks (retrieval-default-hides-the-ruling, tape-unit-is-not-real-tokens) —
          both INHERITED, both name an absent `_measure_tokenizer.py`, neither touched here.
  DREAM: newest = pass 12 (2026-09-13), enact commit exists (c455bc0).

$ python3 knowledge/_gauge_tokens.py
  budget  amber 160,000 · working 200,000 (Dave #56) · hard 256,000
  boot    91,137 +/- 1,300   [ceiling 70,000 — OVER; inherited, not this lane's]
  first turn 80,814 +/- 1,300   => room for job + wrap ~108,863
```

**Did NOT run** (fenced by the brief): `gen_kg_edges.py` · `_build_all.py` · `git stash` · anything
that writes under `knowledge/`. `_build_kg_explorer.py` was **imported as a module** and its
`extract()` / `extract_extra()` called in memory to count nodes; `main()` was never called, nothing
was written, and `notes/_KG-EXPLORER.html` is byte-unchanged (mtime still Sep 15 20:30).

**Not run, and why:** `_quote_gate.py` — its index covers neither `notes/_lanes/` nor `says` (#274,
#275 and #276 all found this). Dave's two `s230-D2` sentences in §3 are quoted directly from
`knowledge/_rulings.json` and the field is named beside them.
