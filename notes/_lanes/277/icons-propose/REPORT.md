# LANE RI — REPORT — icons (666) then logos (12) into the graph: PROPOSED, nothing landed

#277 · 2026-09-16 · `s269-D1` STEP 4 · built from lane IX's FINDINGS.md (`ca294b4`)
**Nothing under `knowledge/` was written.** Every write is under `notes/_lanes/277/icons-propose/`.

---

## 1. What shipped

| file | what it is |
|---|---|
| `gen_kg_icons.py` | the generator. `--dry-run` (default) · `--icons-only` · `--no-logos` · `--no-usesicon` · `--prose-count` · `--selftest` · `--land --ratified <id>` (refuses, §5) |
| `_icon_nodes.json` · `_logo_nodes.json` · `dry-run.json` | the dry run's output, written into this lane dir |
| `_mutate.py` | 25 mutants against the generator |
| `meta.schema.diff` | the grammar ADDITION, proposed and **not applied** |
| `_simulate_validator.py` | applies that diff to a scratch tree and runs the real validator |
| `_build_page.py` · `_page-copy.json` · `REVIEW-icons-2026-09-16-v1.html` | the review page |
| `_drive_page.py` · 8 × `ri-*.png` | the driver and its screenshots |

---

## 2. Nodes and edges — measured, per kind and per type

**Nodes — 688.**

| kind | count | resolver / store |
|---|---|---|
| `icon:<slug>` | **666** | `assets/icons/icons.manifest.json` — 666 records, 0 duplicate slugs |
| `iconGroup:<slug>` | **10** | the same manifest's `groups` keys |
| `logo:<stem>` | **12** | `assets/logos/*.svg` — there is no logo manifest, the filenames are the manifest |

**Edges — 1,299 across six types, all structural.**

| type | direction | the join | edges | target resolves | declared null |
|---|---|---|---|---|---|
| `inGroup` | icon → iconGroup | the manifest key the record sits under | **666** | 666 | 0 |
| `activeVariantOf` | icon → icon | slug `-active(-N)$` + base in the manifest | **234** | 232 | **2** |
| `usesIcon` | component → icon | byte-match of `<path d>`, via `renderedBy` | **371** | 371 | 0 |
| `usesLogo` | component → logo | `src=` at an `assets/logos/` path | **18** | 18 | 0 |
| `defaultFor` | logo → *(null)* | the filename stem inside `s230-D2` | **2** | 0 | **2** |
| `ruledBy` | icon → ruling | a ruling `governs` entry naming the `.svg` | **8** | 8 | 0 (+1 declared, §3) |

`usesIcon` is 371 pairs across **105 components** and **81 of the 666 icons** — 585 icons
are used by nothing. `usesLogo` is 18 across **9 components** and **4 of the 12** lockups.

Against the live graph, measured by importing `_build_kg_explorer.extract()` /
`extract_extra()` in memory (`main()` never called; `notes/_KG-EXPLORER.html` byte- and
mtime-unchanged at 2,893,289 B / 08:50):

```
live graph today : 3,897 nodes / 6,721 edges
this family      :   688 nodes / 1,299 edges   =  +17.7% nodes · +19.3% edges
payload          : 356,431 B serialised as _build_kg_explorer.py serialises
                   against 2,893,289 B  =  +12.32%
chip             : `assets`, fifth additive family, proposed DEFAULT OFF (the `ux` precedent)
```

**Delta from IX, declared.** IX measured +9.4% (271,461 B) for option C. Mine is larger
because my nodes carry `name`, `file`, `fills` and the `$derived` sentence, and my
`usesIcon`/`usesLogo` edges carry a `via` string naming the join. Stripping those
provenance fields gives **239,565 B = +8.28%**, which brackets IX's figure. The provenance
is worth its bytes and the number is reported with it in, not out.

Three other IX figures moved, each for a named reason:
* **explorer 2,889,309 → 2,893,289 B** and **graph 3,893/6,622 → 3,897/6,721** — lane LL
  landed 87 `obeys` edges (`bedf383`) between IX's run and mine.
* **`tokens.icon` 28 → 29 metas** — re-counted live.
* **prose route 1,736 → 1,947 pairs, 138/138 → 137/137 metas** — I skip `EXAMPLE-` (as the
  explorer does) and I test the whole serialised meta, not only its prose values. The
  finding is identical and stronger: it fires on **every** meta.

IX's headline byte-match figures reproduce exactly: **371 / 105 / 81**, and **STRUCT-ONLY
= 32**. My scan reads the 137 `*.reference.html` files (which are exactly the 137 snippet
nodes the graph holds); IX scanned 139 including a `_REVIEW-` scratch file and then
excluded it, landing on the same 371.

---

## 3. The declared nulls — 32, none filled by a guess

| type | n | why it cannot be drawn |
|---|---|---|
| `defaultActive` | **15** | a base carries two or three `-active` glyphs and nothing in the corpus says which is the twin — **B4**, decision RI-3 |
| `governedBy` | **10** | no rule source binds the lockup: **0** rules in `_rules-index.json` whose `file` is `logos.md`, **0** rulings naming a logo `.svg` in `governs` — **B3**, off-repo |
| `activeVariantOf` | **2** | orphan actives: `circle-active`, `menu-more-verticle-active` — the base slug is absent from the manifest |
| `defaultFor` | **2** | `s230-D2` names the two defaults but `theme:` is not a node kind and this lane proposes three, not four (§4) |
| `icon:` | **1** | `menu-search.svg` is on disk and ruled in by `s212-D9`, and is **not in the manifest** — **B1** |
| `usesLogo` | **1** | `app-shell-nav-rail` — `s230-D2` records it as deliberately NOT rebound; the gap is declared, never quietly completed |
| `ruledBy` | **1** | `s212-D9 governs knowledge/assets/icons/menu-search.svg` and there is no `icon:` node to source it from — B1 again |

All five classes the brief named are present and each fires from a structural test, not a
hand-written list. `ruledBy` is 9 candidates: **8 drawn, 1 declared.**

---

## 4. The four refusals

1. **No prose join.** `--prose-count` measures it: every manifest slug as a whole word
   against every meta fires on **137 of 137** metas and makes **1,947** pairs
   (`accessibility` ×137, `no` ×137, `card` ×68, `export` ×65, `error` ×64 …). There is no
   flag that draws it and no code path that can. `s274-D12`, `s276-D5`. The number that
   justifies the byte-match instead is **32**: that many components render a library glyph
   and never once say the word "icon" in their meta.
2. **`themedBy` declined.** 613 `currentColor` / 53 `baked`, against 8 `icon/*` token leaves
   the consuming context sets — 613 identical edges. Handed to the tokens gap with the
   `tokens.icon`-in-29-metas observation attached.
3. **No `theme:` kind.** The two `defaultFor` edges ship with `t: null`, the theme as an
   edge property and Dave's line as the note. Inventing `theme:light` to make an arrow land
   is what fence 3 (#261) exists to stop.
4. **No manifest write.** B1 is declared, not fixed — fixing it is a write under
   `knowledge/`, and this lane writes nothing there.

---

## 5. Gates

```
$ python3 notes/_lanes/277/icons-propose/gen_kg_icons.py --selftest
  17 bites, all ok   SELFTEST PASS
  1 fields verbatim + the group key · 2 active<->slug 0 mismatches + inGroup total
  3 twins drawn, orphan declared, B4 declared, no defaultActive
  4 the gate's own norm(), whitespace-insensitive, and a DRIFTED gate flips it False
  5 the prose route fires and NO edge is drawn from it
  6 an icon-bearing snippet with no component is declared, not dropped
  7 a ruled-in unmanifested .svg gets no node and its ruledBy is declared
  8 logo fields parsed from the filename, a malformed stem refused
  9 defaultFor fires on exactly the named stems, invents no theme: node
 10 the s230-D2 residue is declared
 11 the three option flags each remove exactly their own thing
 12 --land refuses for the RIGHT reason at each of four gates
 13 all six types NEW, no seventh emitted
 14 themedBy declined in fact and in the report
 15 --dry-run leaves the corpus byte-identical
 16 the payload is measured, the chip is OFF
 17 --land with an OPEN allowlist writes two files, names the ruling, drops PROPOSED

$ python3 notes/_lanes/277/icons-propose/_mutate.py
  BASELINE red=[] crashed=False — PASS
  25 mutants · ALL MUTANTS CAUGHT · 0 survivors

$ python3 knowledge/_validate_kg.py            # the LIVE tree, which I did not touch
  metas checked: 139 · ref:null + $note: 90 · 82 ruled verdicts consumed
  _validate_kg.py: OK       rc = 0

$ python3 notes/_lanes/277/icons-propose/_simulate_validator.py   # scratch tree
  baseline rc=0 · diff applied by anchored span (3 of 3 in _validate_kg.py,
  definitions 6->7 and edges.properties 23->26 in meta.schema.json)
  389 real entries planted across 105 scratch metas
  PASS 1 : metas checked 139 · _validate_kg.py OK · rc = 0
  PASS 2 : N1 icon:menu-search CAUGHT · N2 icon:not-a-real-icon CAUGHT ·
           N3 logo:hexagon CAUGHT · N4 usesIcon with no $source CAUGHT · restored rc=0
  RESULT  baseline rc=0 · simulated rc=0 · negatives ALL CAUGHT

$ source knowledge/_render/seat_env.sh && python3 .../_drive_page.py
  22 checks, all ok   DRIVE PASS
```

With 389 new entries across 105 metas the freshness arm still reports `gen_kg_edges.py is
idempotent-clean` — `s268-D6(c)` carries a declared edge type it has no prose source for,
so `usesIcon` and `usesLogo` survive a regeneration untouched. No change to
`gen_kg_edges.py` is needed and none is proposed. (I did not run it; the validator does,
inside its own scratch copy, as it does on every live run.)

**Two mutation findings, both fixed rather than reported as survivors.** The first pass left
seven survivors. Three were the harness scoring a bite that RAISED as "did not even run" —
every bite's condition is now a callable and an exception is a FAIL, not a crash. Four were
real: the gate-drift assertion could not say no (bite 4 now drifts the gate and checks it
flips); `defaultFor` matching a lockup WORD passed unnoticed (the mini corpus now carries
`mark-light-mono`, whose lockup is named and whose stem is not); the door's `ruling_exists`
arm was unreachable behind the allowlist (bite 12 now asserts each of the four refusals by
its own message); and the whole of `land()` was unreachable code (bite 17 opens the
allowlist inside the test, lands, and restores it).

**The `--land` door is shut and can be shown to be shut.** `RATIFIES = ()`. A ratifying id
must be well-formed, recorded in `_rulings.json`, **and** listed in `RATIFIES`. Bite 12 runs
`--land` against every live ruling id in the test corpus and each is refused by name. No
`s277-D*` id ratifies this proposal.

---

## 6. The page

`notes/_lanes/277/icons-propose/REVIEW-icons-2026-09-16-v1.html` — 36,352 B, 4 decisions,
46 measured figures, **no integer typed into the HTML**. Decisions sit at 13% of the
document height and the first radio at 17%; every evidence section is behind them and says
it is evidence. One lead figure per card, one Recommended per card, attribution inside each
card. Three flagged findings that are deliberately NOT decisions: B1 (a build step),
`themedBy` (declined and handed over), `defaultFor`'s missing target.

Screenshots — driven in chromium via `knowledge/_render/seat_env.sh`, both themes, 1280 and
390, and **looked at**:

```
ri-light-1280.png  ri-dark-1280.png             full page, 1280
ri-decisions-light.png  ri-decisions-dark.png   the four cards
ri-RI3-light.png  ri-RI3-dark.png               RI-3 and RI-4 in full
ri-390-light.png  ri-390-dark.png               full page, 390 (13,979px tall)
```

**Two defects the driver passed and my eye caught.** On `ri-decisions-light.png`, the copy
file's `` `inGroup` `` shipped to the page as literal backticks — `md()` had no backtick
rule. On `ri-RI3-dark.png`, `_validate_icons.py` rendered as *validateicons.py* in italics,
because CP's builder carries an `_..._` italic rule that ate the underscores in every
filename starting with one. Both fixed in `_build_page.py` and re-driven. A driver that goes
22-for-22 on a page with a mangled filename in its recommendation is exactly the #268
finding, again.

---

## 7. The four decisions, as one-liners

* **RI-1 — recommend (a):** all three kinds, **688 nodes**. Without the 10 `iconGroup` hubs,
  **170 icons carry no edge at all**; with them every one of the 666 has one and the family
  has ten legible entrances. +17.7% on node count is a look, not an argument, and the
  screenshots are there to judge it on.
* **RI-2 — recommend (a):** draw `usesIcon` from the byte-match, **371 edges across 105
  components and 81 icons**, with the four limits attached. The settling number is **32**
  components that render a glyph and never say "icon" — the prose route misses all of them
  and invents 1,947 pairs instead.
* **RI-3 — recommend (a):** the bare `-active` is the default by rule, the **16**
  `-active-2`/`-active-3` records enter as declared variants. `_validate_icons.py`'s twin arm
  already assumes it, and **all 15** multi-variant bases have a bare `-active`, so it
  resolves every one. It is a small ruling, not a measurement, and (b) costs nothing because
  the 232 twins are drawn either way.
* **RI-4 — recommend (a):** all **12** logos enter, the **10** unbound ones visibly so, each
  carrying a declared `governedBy` null. 0 rules in `logos.md`, 0 rulings naming a logo file
  — eight lockups bound by nothing is the condition `s230-D2` was written to fix, and the
  graph should show it rather than hide it.

---

## 8. Not run, fenced by the brief

`gen_kg_edges.py` · `_build_all.py` · `git stash` · `_build_kg_explorer.main()` · any write
under `knowledge/`. `_build_kg_explorer.py` was imported as a module and `extract()` /
`extract_extra()` called in memory for the live node and edge counts; nothing was written and
`notes/_KG-EXPLORER.html` is byte-unchanged. `_quote_gate.py` not run — its index covers
neither `notes/_lanes/` nor `says`, as #274/#275/#276 each found; Dave's `s230-D2` line on the
page is quoted directly from the `says` field of `knowledge/_rulings.json` and the field is
named beside it in the citation.

`_simulate_validator.py` copies only what `_validate_kg.py` reads — a whole-tree `copytree`
dies on this seat's 97%-full disk at `assets/photography/`. The snippets and `_proforma` are
copied whole because the validator's freshness arm re-runs `gen_kg_edges.py` and that reads
their bodies; the logo `.svg`s are recreated as empty files because nothing reads a logo
body. That substitution is declared in the script's own docstring.

---

## 9. `--numstat`, re-read from the shipped sha

```
$ git show --numstat --format= HEAD     # re-read FROM the shipped commit
   19    0  BRIEF.md                             (the conductor's, committed with the lane)
  NNN    0  REPORT.md        <- this file; its own count moves as this section fills
  424    0  REVIEW-icons-2026-09-16-v1.html
  586    0  _build_page.py
  355    0  _drive_page.py
18168    0  _icon_nodes.json
  281    0  _logo_nodes.json
  210    0  _mutate.py
   57    0  _page-copy.json
  293    0  _simulate_validator.py
  379    0  dry-run.json
 1117    0  gen_kg_icons.py
  211    0  meta.schema.diff
    -    -  ri-390-dark.png · ri-390-light.png · ri-RI3-dark.png · ri-RI3-light.png ·
            ri-dark-1280.png · ri-decisions-dark.png · ri-decisions-light.png · ri-light-1280.png
```

**21 files, ~22,350 insertions, 0 deletions, every path under
`notes/_lanes/277/icons-propose/`.** INSERT-ONLY: the lane deleted nothing and modified
nothing, here or anywhere. `git status` after the commit shows only the three sibling-lane
files that were already dirty when the lane opened (`notes/_REHEARSAL-LOG.jsonl`,
`notes/_dream/_GRADE-DECISIONS.jsonl`, `notes/_lanes/277/DAVE-RULINGS-2026-09-16.md`) and
`notes/_lanes/277/kg-audit/BRIEF.md`, which is the parallel audit lane's. None of them is
mine and none was touched.

The sha is not written into the file on purpose: this section is filled in by amending the
commit, and an amend changes the sha, so a sha typed here would name a commit that no longer
exists. `git show --numstat --format= HEAD` on the shipped commit is the re-read, and every
figure above except this file's own line count is byte-stable across the amend.
