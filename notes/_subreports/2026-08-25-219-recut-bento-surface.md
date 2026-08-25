# #219 lane 3 — the bento decision surface, RE-CUT to post-#218 state

**Filed under `s218-D7`.** Full report; chat got a stub.
**Base:** `d178313` (clean at start for the paths this lane owns).
**Brief:** `notes/_briefs/2026-08-25-219-crank-divvy.md` — DO-NOT-RULE observed: no `_rulings.json`
write, no constant/threshold, nothing closed on Dave's rows, every ambiguity landed as an open
control or as a RULING-SHAPED QUESTION below.

**COUNTS:** findings 8 · ruling-shaped 8 · UNPROVEN 4 · pages emitted 3 · ledger rows 12
(6 RULED · 3 PARTIAL · 3 OPEN) · live controls on the pages 5 · caption blocks measured 1,080 ·
render states driven 24 (3 pages × 8) · store rows minted 2 (`W-172`, `W-173`)

---

## What was emitted

| page | generator | struck | live controls |
|---|---|---|---|
| `reviews/BENTO-CANON-2026-08-25-v4.html` | `knowledge/_render/gen_bento_canon_217.py` | 5 | 2 (Q2, Q3) |
| `reviews/BENTO-CANON-2026-08-25-v5.html` | `knowledge/_render/gen_bento_roles_217.py` | 6 | 1 (Q6) |
| `reviews/GALLERY-COMPARE-2026-08-25-v2.html` | `knowledge/_render/gen_gallery_compare_217.py` | 7 | 4 (Q3, Q6, Q11, Q12) |

**The #217 pages are untouched on disk** — `BENTO-CANON-2026-08-23-v2.html`, `-v3.html` and
`GALLERY-COMPARE-2026-08-23-v1.html` all still exist and still probe against their own bytes.

**New file:** `knowledge/_render/_bento_recut_219.py` — the ONE home for the ledger (ADR-0017,
write-once). All three generators render it; nothing is stated twice. It has its own `--selftest`
(5 bites), one of which **refuses to render a RULED question as a live control** — the laundering
defect is now a gate, not a habit.

⚠ **Naming call, mine, and the conductor may re-cut it.** The brief named `BENTO-CANON-…-v4.html`
once but listed two generators that both write into the `BENTO-CANON` series. I gave the canon
demo **v4** (successor to v2) and the roles demo **v5** (successor to v3), so the series stays
monotonic and neither overwrites. Both carry `2026-08-25`.

---

## The ruled-vs-open table

Every `clause` is a **verbatim** slice of the named ruling's `says` field in
`knowledge/_rulings.json`, read at source. The pages render this same table from the same module.

| # | The question the #217 pages asked | State | Receipt | The clause that closed it | Residue still open |
|---|---|---|---|---|---|
| **Q1** | May tile spans be adjusted at mint time at all — does the squaring pass exist? | **RULED** | `s217-D3` | *"SQUARING PASS RATIFIED for dashboard and brochureware roles (Dave: 'is very cool', with gallery exempted in the same breath)."* | — |
| **Q2** | May only the TAIL of a wall move, or the whole wall? | **OPEN** | — | *(nothing reaches it)* | All of it. The shipped pass moves the last few tiles (`tail_cap=6`) — an implementation choice standing in for a decision. |
| **Q3** | What may a photograph be re-cropped into when a wall is squared? | **PARTIAL** | `s218-D6 (4)` | *"the squaring pass runs on the photography page's gallery wall and last-row photos may re-span to close holes."* | Ruled for **one page's wall** and **last-row** photographs only. No bound anywhere else, and no rule against flattening a portrait. |
| **Q4** | Does the gallery keep its keylines, drop them, or get both as a dial? | **RULED** | `s217-D5` | *"GALLERY: same three spacings; keylines on/off; caption background colour on/off"* — plus `s218-D3` recording the photography page's own answer (**off**, all four themes). | — |
| **Q5** | Span grid with orphan tolerance, or justified rows with a widow switch? | **RULED** | `s217-D5` | *"mode is 'Justified rows' OR 'Gallery bento', the bento mode carrying a sub-option ragged or square bottom (this turns s217-D3's gallery squaring exemption into a per-instance choice)"* — **both, as a per-instance dial**; `s218-D3` sets the photography instance to **bento**. | — |
| **Q6** | Ragged or square bottom edge on a gallery wall? | **PARTIAL** | `s217-D5` (dial) + `s218-D6 (4)` (one instance) | *"the bento mode carrying a sub-option ragged or square bottom"* | Whether the **gallery ROLE's default** flips. `s218-D6 (4)` scopes itself: *"the GALLERY ROLE's s217-D3 exemption elsewhere is untouched until he says wider."* |
| **Q7** | What ground and ink does a mono caption take? | **RULED** | `s218-D6 (1)` | *"The mono caption ground is RATIFIED at the proposed shade: #1A1A1A via --surface-digital-black with --text-reverse white ink - 'Yes - that's the one'. The s218-D3 PROPOSED marker on the shade is discharged."* | — |
| **Q8** | How much space does a gallery caption get? | **RULED** | `s217-D3` | *"GALLERY ADDITIONS: more generous caption space (ruled)"* — derived to **86px** in `layout/bento/caption-space`. | — |
| **Q9** | Where does the corner radius sit when every tile is keylined? | **PARTIAL** | `s218-D1` | *"each tile must have it's own keyline, but the radii should only apply to the 4 corners of each sub bento … Scope option-selected by Dave the same sitting: DASHBOARD ONLY for now - brochureware/gallery keep their s217-D3 radius behaviour until he extends it."* | Extension to brochureware / gallery. |
| **Q10** | May a keyline run down the middle of the spacing? | **RULED** | `s217-D8` | *"the keyline goes tight around each module (tile) - a 1px border on the tile box at every spacing stop - never a line centred in the gutter. … The centred-gutter 'treatment C' construction is retired for dashboards."* | — |
| **Q11** | Do justified rows RE-PACK as the container narrows, or keep mint-time membership? | **OPEN** | — | `s217-D5` rules the mode into existence and says **nothing** about re-packing. | All of it. |
| **Q12** | Do justified rows carry an emphasis rhythm at all? | **OPEN** | — | v1 named it in a table as *"a separate question if you go this way"*. It stayed separate. | All of it. |

**⬛ UNPROVEN, and not waiting on Dave:** whether candidate B **nests**. B is a flex column, not a
grid; nobody has measured it. Carried forward from v1, marked on the page as unproven rather than
open.

---

## What was baked in

- **The 86px caption block.** Consumed from `layout/bento/caption-space` via
  `--layout-bento-caption-space` — **the token, never the literal**. The fallback literal and the
  three-line clamp are both **minted at build time** from `caption_space()` (`s200-D1`), so the
  page cannot become a second source for a ruled number. On v5 and the compare page canon's own
  `[data-bento-role="gallery"] .c-bento__caption` rule supplies it; on v4 (whose walls carry no
  role — it is the `s217-D2` defaults demo, and giving them one would change what it demonstrates)
  the token is read directly.
- **The mono caption ground, `s218-D6 (1)`.** `--surface-digital-black` / `--text-reverse`,
  mono only, both modes, on all three pages. The construction is **copied from
  `gen_foundations_217.settings_css`'s ratified rider**, not re-derived
  ([[specimen-starts-from-reference]]).
- **`edge:square`, `s218-D6 (4)`, SCOPED AS THE RULING SCOPES ITSELF.** The compare page gains a
  **new A4 wall** — the same 4-column dial as A2, with the squaring pass run — labelled as the
  Foundations photography page's *instance*. A1/A2/A3/A5 stay **ragged**, and a selftest bite
  (`7k`) fails if any of them is squared, because squaring them would enact a widening of the
  gallery ROLE that nobody ruled.
- **`s218-D1` recorded, not re-drawn.** The corner-keyline construction is enacted in
  `gen_bento_matrix_217.py`, which owns it. v5's dashboard section states the ruling **and its
  DASHBOARD-ONLY scope**, so nothing below it reads as re-opening either half.

---

## The matrix explorer — checked, and deliberately UNTOUCHED

`showroom/_foundations/bento.html` is **unchanged** (`git status` on `showroom/` is empty).

**None of `s217-D5`'s five open points was discharged by a named ruling.** Checked at source
against every bento ruling that post-dates `s217-D5` — `s217-D6`, `s217-D7`, `s217-D8`, `s218-D1`,
`s218-D2`, `s218-D3`, `s218-D6`:

| point | verdict |
|---|---|
| **P1** tight+keylines-on = flush tiles with hairline separators | **NOT discharged by name.** ⚠ See ruling-shaped question 1 — `s217-D8` and `s218-D1` both legislate the 1px flush stop's construction and neither names P1. |
| **P2** caption judged against its immediate ground | Not discharged. `s218-D6 (1)` ratifies a *shade*, not the legality rule. |
| **P3** capsule requires caption background or keylines | Nothing reaches it. |
| **P4** stepped-down concentric radius at Display tight | `s217-D6` amended P4's **presentation** (stacked, not halved). The proposal itself stands. |
| **P5** grey/white/transparent palette across all three types | Not discharged. ⚠ See ruling-shaped question 2. |

⛔ **I did not strike P1 or P5 in the explorer.** Both are *adjacent* to a #218 ruling and neither
is *named* by one. Striking an adjacency is ruling, and this lane's DO-NOT-RULE forbids it.

---

## Photographs — 15/15, pinned by name

Every emitted page was checked against `gen_bento_roles_217.SPECIMEN_FILES` by basename:

| page | distinct basenames | verdict |
|---|---|---|
| `BENTO-CANON-2026-08-25-v4.html` | 15 | **MATCH**, zero missing |
| `BENTO-CANON-2026-08-25-v5.html` | 15 | **MATCH**, zero missing |
| `GALLERY-COMPARE-2026-08-25-v2.html` | 15 | **MATCH**, zero missing |

---

## Render-verify

Runbook staging per `knowledge/_RUNBOOK-render-verify.md`, **fifth stratum honoured**:
`/var/tmp/chromelibs` was confirmed **hollow** and `/var/tmp/chromelibs-s213e2` used instead,
verified with `ls` + `ldd` (`ldd | grep "not found"` printed nothing) rather than with a launch
attempt. `tiktoken` importable first. Fresh symlink font farm `/var/tmp/fonts-s219l3` with the
`<include>` present; cache outside the repo. `git status` on `knowledge/` shows **no `.uuid`
strays**.

**Font probe, all three pages, with two controls:** target 347 · alias_uf 347 · alias_font 347 ·
DejaVu 375 · nonexistent 301. Both aliases land on the target and on neither control.

| probe | verdict |
|---|---|
| `verify_bento_canon_217.py` (v4) | **ALL GREEN**, 8 states |
| `verify_bento_roles_217.py` (v5) | **ALL GREEN**, 8 states |
| `verify_gallery_compare_217.py` (compare v2) | **ALL GREEN**, 8 states |

### The 86px caption space, MEASURED — not authored

**v4**, new arm, **240 caption blocks across 8 states**, three readings per block because any two
of them can be right while the page is wrong:

- **rendered height** ≥ 86px — proves the block is not collapsed;
- **computed `min-height`** == 86px — proves the number came from the token, not from tall content;
- **resolved `--layout-bento-caption-space`** == 86px — proves the cascade delivered it rather
  than a fallback literal standing in.

**v5**: 360 blocks, existing arm, green. **Compare v2**: 600 blocks, existing arm, green.
**Total 1,080 caption blocks measured.**

### ⬛ MUTATION ARM, RED BY NAME — and the mutant is a real artefact

The pre-fix page **is** the mutant. The v4 probe was driven against
`reviews/BENTO-CANON-2026-08-23-v2.html` and went **RED by name in every state**:

```
⛔ supercharge/dark — caption min-height 0px, expected the ruled 86px (s217-D3, layout/bento/caption-space)
⛔ supercharge/dark — caption block RENDERS 38px, below the ruled 86px: authored and collapsed is not enacted
⛔ supercharge/dark — caption clamp '2', expected the DERIVED 3 line(s) — the space and the clamp have drifted apart
EXIT 1
```

**That measurement IS Dave's complaint, quantified: v2's caption block rendered 38px against the
ruled 86px — 48px, 56% of the block, missing.** A caption arm that had never been seen to fail
would not be a gate ([[instrument-without-a-consumer]]).

### The mono ground, both directions

`s218-D6 (1)` is asserted **positively in mono** (`rgb(26,26,26)` ground, `rgb(255,255,255)` ink,
both modes) and **negatively in the other three themes** — a non-mono caption taking the mono
ground fails by name. Asserting only mono would pass a page that painted every theme's captions
black; asserting only the others would pass a page where the rider never landed.

### `s218-D6 (4)` scope, measured

The compare probe reports A raggedness for **A#0, A#1, A#3 only** — wall **A#2, the squared
instance, measures zero holes** while the other three stay ragged in all eight states. The scope
sentence is enacted, not merely quoted.

### Downstream, nothing broken

`gen_bento_matrix_217 --selftest` **54 bites OK** · `gen_grids_218 --selftest` **16 bites OK** ·
`gen_foundations_217 --check` **7 pages in sync** · all three re-cut generators' own selftests
green (8 / 9 / 8 bites) · `_bento_recut_219 --selftest` 5 bites.

---

## Findings

1. ⚠ **THE BRIEF'S PREMISE IS OFF BY TWO RULINGS, AND IT MATTERS.** The brief says the pages
   "predate the #218 rulings `s218-D4`/`D5`/`D6` (twelve rulings by option-select)". Read at
   source, **`s218-D4` and `s218-D5` contain nothing about the bento** — D4 is phantom
   affordances / meter behaviour / wave-3 lanes / CI contrast / the palette chord; D5 is
   stacked-bar motion. The rulings that actually close these pages' questions are **`s217-D5`,
   `s217-D8`, `s218-D1`, `s218-D3` and `s218-D6`** — and two of those are `s217`, i.e. the pages
   were stale *within their own session's numbering*. Working from the brief's list alone would
   have struck nothing on the gallery-compare page, whose whole question is closed by `s217-D5`.
   ([[premise-ages-faster-than-rule]] — verified the premise like repo state.)
2. **Dave's caption complaint, quantified: 38px rendered against the ruled 86px.** v2's photo
   captions used neither the token nor canon's `.c-bento__caption` slot. Now measured, and the
   arm has been seen red.
3. ⛔ **THE RATIFIED SQUARING PASS FLATTENS A PORTRAIT — SEEN, ON THE PINNED SPECIMEN.** Running
   `s218-D6 (4)`'s pass on the 15-photograph set at 4 columns re-spans two tiles:
   `gettyimages-968890266-w1600.jpg` (landscape) 1×1 → 1×2, and **`stocksy-6629948-w1600.jpg`
   (portrait) 1×2 → 1×1**. The pass is cost-ordered to avoid exactly that and it still happened.
   The page names it tile by tile rather than reporting "2 tiles re-spanned", because the summary
   hides the only part that is a design consequence. **This is Q3 made visible instead of argued.**
4. ⛔ **TWO SELFTEST BITES WERE GATES PINNING SETTLED QUESTIONS OPEN.** `gen_bento_canon_217`
   bite 6b required the words *"not ruled"* in the squaring section; `gen_bento_roles_217` bite 6c
   required them in the trial section. Both rulings had landed. Each bite would have **failed the
   build if the page told Dave the truth** — an instrument enforcing the laundering defect. Both
   reversed: they now require the RECEIPT and forbid the phrase.
5. **Three probes carried their own copy of the page filename.** `verify_bento_canon_217`,
   `verify_bento_roles_217` and `verify_gallery_compare_217` each hard-coded the `2026-08-23`
   path. Under version-don't-overwrite that is a probe that goes on measuring the stale file and
   reports green about a document nobody is looking at. All three now `from <generator> import
   OUT as PAGE` — one source for the name. Fixed at cause, not patched
   ([[feedback-gate-dont-patch]]).
6. **No `s217-D5` P1–P5 point was discharged; the explorer is untouched.** Two adjacencies found
   and *not* acted on — see ruling-shaped 1 and 2.
7. ⚠ **FOREIGN WORKING-TREE CHANGES ARE PRESENT AND ARE NOT THIS LANE'S.** At filing,
   `git status` also shows `knowledge/_proforma/DataViz-interactive.html`,
   `knowledge/_render/verify_dv_d16_render.py`, `knowledge/_review/_gen_dataviz_charts.py`,
   `knowledge/snippets/Chart-bar.reference.html` and the untracked
   `knowledge/_render/apply_dv_d16_region_219.py` — the DV-D16 lane. **This lane touched none of
   them.** Named here so the reconcile does not attribute them, and does not blind-`git add -A`.
8. **`gen_grids_218.py --check` is not a flag.** The module writes nothing (`gen_foundations_217`
   is the ONE writer) and its help gate says so; `--selftest` is the driveable arm. Minor, but a
   `--check` in a runbook or a wrap script would read as a silent pass.

### Store rows

`W-172` — the re-cut itself, **owner Dave**, linked to `W-119` / `W-124` / `W-125`, closing on his
eye plus his answer to the five live controls. `W-173` — this report, owner Claude, closing when
the conductor cites it **by path** in the session receipt. Existence + close condition only;
neither touches a row of his.

⚠ **One self-correction worth a line, because it is a class.** The rows were first written with a
raw `json.dump(..., indent=1)`, which **reformatted the entire store** — a 3,314-line diff for two
new rows. Reverted and re-minted through `_state.save()`, the store's own writer (`indent=2`):
**+32 lines, nothing else moved.** A store has ONE writer and its serialisation is part of it;
a hand-rolled dump passes every content check and still produces an unreviewable diff.

### This lane's own paths (for the reconcile)

```
M  knowledge/_render/gen_bento_canon_217.py
M  knowledge/_render/gen_bento_roles_217.py
M  knowledge/_render/gen_gallery_compare_217.py
M  knowledge/_render/verify_bento_canon_217.py
M  knowledge/_render/verify_bento_roles_217.py
M  knowledge/_render/verify_gallery_compare_217.py
M  knowledge/_state.json                    (W-172, W-173 — seam grammar, +32 lines only)
?? knowledge/_render/_bento_recut_219.py
?? reviews/BENTO-CANON-2026-08-25-v4.html
?? reviews/BENTO-CANON-2026-08-25-v5.html
?? reviews/GALLERY-COMPARE-2026-08-25-v2.html
?? notes/_subreports/2026-08-25-219-recut-bento-surface.md
M  notes/_REHEARSAL-LOG.jsonl               (one appended line — `--rehearse`, below)
```

**Doc-row gate driven:** `knowledge/_capture_gate.py --rehearse` → **0 STRUCTURAL fail(s)**,
0 heals-at-wrap, 18 warns. `s218-D7` widened the gate's glob to the sub-report path, so this run is
the proof that the two new documents and this report all carry their store rows (the
forgotten-document class, #185). ⚠ `--rehearse` appends one line to `notes/_REHEARSAL-LOG.jsonl`;
that is the only unintended path this lane touched and it is named here rather than left for the
reconcile to wonder about.

---

## RULING-SHAPED QUESTIONS

⛔ Nothing below was decided by this lane. Items 3–7 are live controls **on the pages**, each
carrying its owner and the ruling an answer would mint; 1, 2 and 8 are for the conductor.

1. **Is `s217-D5`'s P1 discharged?** P1 proposed *"tight+keylines ON = flush tiles with inset
   hairlines (1px cannot hold a gap and a line)"*. `s217-D8` then ruled the keyline construction
   *"a 1px border on the tile box at every spacing stop"* with the conductor's enactment detail
   preserving *"the rounded group border + flush hairline construction"* at the 1px stop; `s218-D1`
   says *"The 1px flush stop is unchanged"* and Dave signed the live explorer off — *"Yay it works.
   very happy with this."* **Neither ruling names P1**, and both are scoped to the DASHBOARD while
   P1 sits on Display. A sign-off on a render is not a ruling on a proposal. **Left open, explorer
   untouched.** Dave's to close, or the conductor's to raise.
2. **Does `s217-D5`'s ruled background palette gain a fourth ground?** `s218-D6 (1)` puts
   `#1A1A1A` into service as a caption ground, and the #218 receipt says in as many words that the
   explorer's grey / white / transparent palette *"cannot say"* a dark ground, so the rider is
   *"an ADDITION to the ruled vocabulary rather than a selection from it."* P5 proposed that one
   palette serve all three types. **Is the dark ground now part of the palette, or a
   photography-page exception?** Not acted on.
3. **Q2 — may only the tail of a wall move, or the whole wall?** Live on v4. Answering mints a
   ruling on the squaring pass's mutation scope.
4. **Q3 — what may a photograph be re-cropped into?** Live on v4 and the compare page, with
   finding 3 rendered beside it. Answering mints a bound on the crop a squaring pass may pay,
   applying to every wall rather than to one page.
5. **Q6 — does the gallery ROLE's edge default flip from ragged to square?** Live on v5 and the
   compare page. Answering mints an amendment to `s217-D3`'s exemption. ⛔ `s218-D6 (4)` set one
   *instance* and explicitly did not widen it; this is the widening.
6. **Q11 — do justified rows re-pack, or shorten?** Live on the compare page. Answering mints a
   ruling on justified-row responsiveness.
7. **Q12 — do justified rows carry an emphasis rhythm?** Live on the compare page.
8. **Is v4/v5 the right series cut?** Two generators write into the `BENTO-CANON` series; I gave
   the canon demo v4 and the roles demo v5. A filename, not a design decision — but it is mine and
   the conductor may re-cut it before the commit.

---

## UNPROVEN — declared, not implied

1. **Candidate B's nesting.** Untested at #217, untested now. Marked on the page as unproven
   rather than open, because nobody is waiting on a decision — somebody is owing a measurement.
2. **No PNG was read.** Every claim above is a computed-style or geometry assertion driven in the
   live document across 24 states. The pages have **not been looked at by an eye**, mine or
   Dave's. The mono caption ground in particular is asserted as `rgb(26,26,26)` on
   `rgb(255,255,255)` ink; whether it *reads* well against each theme's photography is his call
   and is unasked here.
3. **The full `_build_all.py` suite was not run** (brief: regen only what these generators own;
   and it exceeds the sandbox call cap). Driven instead: the four bento selftests, the three
   render probes, `gen_foundations_217 --check`, `gen_grids_218 --selftest`. **Bounded
   verification, `s172-D3`.**
4. **The `-NOSQUARE` / `-WRONGROLE` / `-BROKEN` mutation arms of the three probes were not
   re-driven against the successors.** They were green at #217 against the predecessor pages and
   nothing in this re-cut touched the mechanisms they exercise, but that is an inference, not a
   measurement. The one mutation arm that WAS driven is the new caption arm (finding 2), which is
   the clause this lane added.

---

## Not done, on purpose

- **No commit, no push.** Working-tree changes + this report, per the brief.
- **No `_rulings.json` write.** No constant, threshold, band or advisory touched.
- **No row of Dave's closed or reworded** — `W-119` / `W-124` / `W-125` / `W-126` stand exactly as
  they are; the new store row **links** to them and closes on his eye.
- **No full regen serial.** Only the three generators this lane owns were re-run.
