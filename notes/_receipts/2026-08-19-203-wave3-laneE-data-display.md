# Receipt — #203 Wave 3, Lane E · data display (Empty state · Stat card · Data grid)

*Worker receipt per the parallel-conductor checklist, written 2026-08-19 against HEAD `ec2336d`.*
*⛔ Nothing here is a ruling. No commit, no push, no `git checkout/restore/stash`. `knowledge/_rulings.json` untouched.*
*Gauge at close — `_checkin.py`: FILL **108,667 real** · boot **56,488 real** · peak 108,667 across 18 turns ·
throughput 117,646 real · room to the advisory stop line (150,929) **42,262**.*

---

## Headline for the conductor, before anything else

**The brief's premise is stale, and not only for this lane. All three of Lane E's components already
exist, gated, and have existed for weeks. So do the other fifteen across lanes A–F.** The itinerary
they were drawn from is dated **2026-07-14** and has not been reconciled since. Nothing in this lane
was built as a new component, because building one would have meant overwriting a gated artefact —
which the fence forbids and which would have been a deletion, not a delivery.

What this lane produced instead: the **four-theme review surfaces that did not exist**, and a
**conformance audit of the three live components against #203's ruled rules**, which turned up two
measured defects and one gate that is red at HEAD.

## Step 0 — the premise, verified first-hand

| Claim inherited from the brief | Verified? | Evidence |
|---|---|---|
| HEAD is unstated in the brief | HEAD is `ec2336d` (#202 wrap) | `git log --oneline -1` |
| Empty state (row 54) is a **Gap** | ❌ **FALSE** | `ls knowledge/snippets/` → `Empty-state.reference.html`, 168 lines, `#token-manifest` present |
| Stat / metric card (row 52) is a **Gap** — *"only a util today"* | ❌ **FALSE** | `Stat-card.reference.html`, 164 lines, gated |
| Data grid (row 51) is a **Gap** | ❌ **FALSE** | `Data-grid.reference.html`, **734 lines**, gated |
| All three absent from the radius ratchet | ❌ **FALSE** | `_validate_radius.py` `MIGRATED_SNIPPETS` — Empty-state + Stat-card at "Phase-2 wave 1", Data-grid at "Phase-2 wave 2" |
| Data grid needs sort + select + pagination composed on Table | ❌ **already built** | `aria-sort` cycle `_:593-596`, row checkboxes `_:340`, `<nav class="dgpg">` + rows-per-page `_:380-386`, filter chips `_:614` |
| Inline edit is OUT of scope, a PROPOSED cut | ❌ **already IN and working** | `_:387` — *"`Enter` … opens the reference cell for editing (`F2` also edits; `Esc` cancels)"* |
| Stat card `spark` slot is a known candidate | ✅ TRUE, and still **not built** | no `spark` in the snippet or meta; `Chart-sparkline` exists as its own gated component |
| `.meta.json` absent for all three | ❌ **FALSE** | `empty-state.meta.json`, `stat-card.meta.json`, `data-grid.meta.json` all present |
| Type-composite debt is **1,101** | ⚠ **STALE** — it is **1,097** | `_validate_type_composites.py` summary line, run today |

**The staleness is lane-wide, not mine alone.** Every component named in brief §9 already exists as a
gated snippet: `Form-layout` `Textarea` `Alert` `Date-picker` `Date-range-picker` `Time-picker`
`Amount-input` `Amount-display` `Secure-entry` `Toast` `Drawer` `Popover` `Empty-state` `Stat-card`
`Data-grid` `Skeleton-loader` `File-upload` `Stepper` — 18 of 18, verified by one `ls`. The itinerary's
`Status = Gap` column is the stale artefact. **Recommend the conductor reconcile the itinerary before
any further wave is briefed off it**, and check whether the other five lanes hit the same wall.

## Deliverables

| File | State |
|---|---|
| `reviews/REVIEW-203-empty-state-four-themes-v1.html` | **NEW** — 4 themes × light/dark, 8 panes, responsive |
| `reviews/REVIEW-203-stat-card-four-themes-v1.html` | **NEW** — 4 themes × light/dark, 8 panes, responsive |
| `reviews/REVIEW-203-data-grid-four-themes-v1.html` | **NEW** — 8 **live, independent** grid instances + a layout controller |
| `notes/_receipts/2026-08-19-203-wave3-laneE-data-display.md` | **NEW** — this file |

No snippet, meta, token, generator or shared file was created or edited. The three components' review
surfaces had **never existed** — `ls reviews/ | grep -iE 'empty|stat-card|data-grid'` returned nothing
before this lane.

Every pane is the **real snippet markup** rendered through the generated `canon.css` and the real
`[data-apollo-theme]` cascade — copied out of the approved artefact, never re-drawn
(`specimen-starts-from-reference`). The extractor is a throwaway at `/var/tmp/s203e/`, outside the repo,
per the #174 precedent; it is not an instrument the repo carries.

**The grid's eight panes are `srcdoc` iframes, and that is deliberate, not a fudge.** The grid carries a
real demo script bound to document-level ids; eight copies in one document would fight over them. Each
pane is its own document with a `<base>`, the same `type.css` + `canon.css`, and the theme attributes on
its root — identical cascade, isolated ids. Verified: **8/8 frames rendered 8 tbody rows each**, auto-height
784px, **0 page errors**. Sort, select, filter, paginate and `F2`-edit all work in every pane, so Dave can
compare two themes mid-interaction.

## Gates — every rc reported, baseline measured before anything was written

| Gate | At HEAD (baseline) | After this lane | Verdict |
|---|---|---|---|
| `_validate_snippets.py` | **rc=1**, 76 snippets, **18 failures** | rc=1, 76, 18 — **unchanged** | ⚠ **red at HEAD, not mine** — see below |
| `_validate_a11y.py` | **rc=0**, 76 snippets, 0 failures, 179 warnings | rc=0, unchanged | ✅ |
| `_validate_type_composites.py` | **rc=1**, **1,097** violations across 90/91 files | 1,097 — **unchanged** | ✅ ratchet held; I added 0 |
| `_validate_state_contrast.py` | **NOT RUN — declared, see residuals** | — | ⚠ left to the conductor |
| `_validate_radius.py` | not run (no snippet touched) | — | ⚠ left to the conductor |

⛔ `_build_all.py` NOT run. ⛔ No generator that rewrites shared outputs was run — not even `--check`,
because five sibling lanes are live and I had nothing to check into them. **Gates left to the conductor,
by name: `_validate_state_contrast.py`, `_validate_radius.py`, `_validate_coverage.py`, `_validate_icons.py`,
`gen_showroom --check`, `gen_canon_components --check`, `gen_theme_cascade --check`.** A declared gap
passes; this is the declaration.

### ⚠ `_validate_snippets.py` is RED AT HEAD and it is not this lane's doing

18 failures across **nine** snippets, all the same defect, all `--pri-hover`:

> `❌ Empty-state.reference.html: DRIFT --pri-hover (light) = #626262 but button/primary/background/hover = #636363`
> `❌ Empty-state.reference.html: DRIFT --pri-hover (dark) = #B7B7B7 but button/primary/background/hover = #B2B2B2`

Same two lines for `Action-bar` · `Button` · `Confirmation` · `Drawer` · `Form-layout` · `Icon-button` ·
`Modals` · `Stepper`. **Eight of the nine are outside Lane E; three are inside other live lanes right now
(`Drawer` = Lane D, `Form-layout` = Lane A, `Stepper` = Lane F).** The store moved under `s198-D1`/`s199`
when `--pri-hover` was minted and renamed, and these nine snippets kept the pre-mint values. This is the
`alias-repoint can strip a theme's override silently` class, showing up as an un-repointed literal.

**I did not fix it**, though it is a two-value edit per file: the fence is NEW files only, and a
cross-lane fix touching three other subs' components while they are mid-flight is exactly how #202 lost
work. **Proposed for the conductor at reconcile**, as one change: `#626262`→`#636363` (light),
`#B7B7B7`→`#B2B2B2` (dark) in `Empty-state.reference.html:62` and `:66`, and the equivalent lines in the
other eight. That single change should take the snippet gate from rc=1 to rc=0.

## Conformance audit against §5's ruled rules — driven, not assumed

Measured in a real browser (`goto("file://…")`, never `set_content()`), all four themes, both modes.

| Ruled rule | Finding |
|---|---|
| Four themes, light + dark | ✅ all three render in 8/8 panes, no theme falls back |
| Square corners by default | ✅ radius 0 in mono/legacy/supercharge; **20px in Console** — that is `s199-D3`'s console radii working as ruled, not a breach |
| Type composites, no raw font-size | ✅ my files add 0 to the debt. The three components' own residual debt is **demo-chrome only** (`h2{font-size:14px}` on the specimen page's section headings) plus `font-family:var(--font)` on `body` — the review pages hide those `h2`s entirely |
| 44px min-hit-area (no gate enforces it) | ⚠ **two findings, below** |
| Two-red law `s151-D1` + green mirror `s155-D1` | ❌ **one measured breach, below** |
| Mono error ink camp `s149-D1`/`s194-D1` | ✅ not engaged — none of the three paints text on an error fill |
| Real ARIA, `:focus-visible` | ✅ present and driven; grid announces via `role="status"`, roving-cell focus works in all 8 panes |
| Colour never the only carrier | ✅ stat-card deltas declare `data-carries="symbol label"` — arrow **and** the word "up"/"down"; grid selection = tint **+** 4px inset bar **+** checked box |

### ❌ Finding 1 — the stat-card delta arrows are bound to the FILL seat, not the ink seat

`stat-card.meta`'s manifest binds `--up` → `rag/success` and `--down` → `rag/error`. Those are the
**fill** family. The store says so itself, verbatim, in `semantic-colour.json`:

> *"`rag.error` is the FILL family (banner/roundel background) — a different seat."*
> *"`rag/error-ink` is the CANONICAL rung for coloured monetary TEXT … `s151-D1`'s two-red law is
> background-keyed `#DA1A00`-on-white / `#F6604C`-else."*

And `s151-D1` itself, quoted in `palettes/rag/mono.json`:

> *"dark red ink (the `s145-D1` `rag/error-ink` light leg `#DA1A00`) on WHITE — **text AND atoms alike**"*

The delta arrow is an atom, and in the light panes it sits on a white card. Measured today with the
repo's own `_contrast_utils.contrast_ratio`:

| Pair | Ratio | |
|---|---|---|
| `#F6604C` (as built) on `#FFFFFF` | **3.140:1** | scrapes the 3:1 non-text floor |
| `#DA1A00` (`rag/error-ink` light, ruled) on `#FFFFFF` | **5.090:1** | |
| `#66CC8D` (as built) on `#FFFFFF` | **1.980:1** | ❌ **fails 3:1 outright** |
| `#137F3C` (`rag/success-ink` light, ruled) on `#FFFFFF` | **5.090:1** | |
| `#F6604C` on `#1F1F1F` (mono dark card) | 5.260:1 | ✅ dark legs already correct |
| `#66CC8D` on `#1F1F1F` | 8.310:1 | ✅ |

**Only the light legs are wrong, and only the arrow.** The fix would be a two-token rebind
(`rag/error`→`rag/error-ink`, `rag/success`→`rag/success-ink`). **I have not touched it** — rebinding a
ruled colour seat is Dave's, the arrow-only treatment may have been a deliberate choice, and it is a
`surface, never swap` item. It is on the review page with the numbers, for his eye.

**Why no gate caught it.** The red pair *is* declared (`rag/error` on `tertiary/background/default`,
context `ui`) and passes at 3.14 ≥ 3. The **green pair is not declared at all** — it was moved out of the
manifest onto the rendering gate under `s151-D2`, with a comment in the snippet saying so. So the 1.98:1
green depends entirely on `_validate_state_contrast.py`, which **I could not run** (below). That is an
`instrument-without-a-consumer` shape worth the conductor's attention: the declared-absence mechanism is
correct, but the instrument it defers to has not run over this file in this session.

### ⚠ Finding 2 — 44px, enforced by hand as the brief instructs

Measured across all 8 panes:

- **Empty-state first-run button: exactly 44×44 in 8/8 panes** ✅
- **Empty-state "Clear the search" link: 18px tall in 8/8 panes** ⚠
- **Data-grid pagination controls and sort headers: 44px** ✅
- Data-grid row checkboxes: 22×22 — the Selection-controls intrinsic anatomy, consistent with the a11y
  gate's own "107 marks below 24" note; flagged as *inherited*, not a Lane E defect
- The grid's `Live / Loading / Empty` switch: 26px — **demo chrome, not the component**

The 18px link is the one to decide. No gate enforces 44px, so it has never gone red. Whether a recovery
link inside an empty state must be a 44px target, or whether inline links are legitimately exempt, is a
rule that does not exist yet — so I did not write one.

## Render proof

`goto("file://…")` throughout; `set_content()` never used. Chromium 151.0.7922.34, cached browser at
`/var/tmp/pw-browsers-s197`, fontconfig **symlink farm** at `/var/tmp/fonts-s203e` per the `#138` runbook
step — so fontconfig writes its `.uuid` markers into the farm, **not into the repo it scans**. Verified
after the fact rather than assumed: `find . \( -name '.uuid*' -o -name '*.LCK' \)` returns **7 files, all
dated 2026-08-08/09 and all already quarantined in `_to_delete/`** — the #136/#138 strays. **Zero are
mine.** Verified too that no shared file was touched: `find knowledge/{snippets,components,tokens,canon}
-newermt '2026-08-19' -type f` returns **nothing**. Tree stays clean for the conductor's commit.

Font asserted by **canvas measurement against two controls**, never `fonts.check()`:
target `"Univers Next for HSBC"` = **163** · alias `"Univers Next HSBC"` = **163** ·
`DejaVu Sans` = 176 · nonexistent face = 141 ⇒ the real HSBC cut, both aliases landing on it.

Driven and seen by eye at 1180px, 1400px, 1600px and 480px. `0` page errors on all three pages.
Responsive: all three collapse to a single column at 480px (`grid-template-columns` computed = `416px`).
Renders viewed at `outputs/s203e-renders/`.

## Decisions needed — Dave's, every one PROPOSED #203

1. **The stale itinerary.** 18 of 18 Wave-3 components already exist. Reconcile the `Status` column, or
   re-brief the waves off something else? *(This one is really the conductor's to raise.)*
2. **Stat-card delta arrows — rebind to the ink seat?** Measured 1.98:1 green on white against a ruled
   5.09:1. Rebind, or ratify the fill seat as a deliberate exception for arrows?
3. **Stat-card `spark` slot.** Not built. `Chart-sparkline` already exists standalone, so this is a
   composition question: does the card grow a slot, or does a board place a sparkline beneath a card?
4. **Empty-state glyph opacity, per theme.** 0.4 ink is uniform across all four themes; it is visibly
   faintest in Console and Supercharge dark. Per-theme value, or drop the glyph and let the title carry it?
5. **Empty-state recovery link and the 44px rule.** 18px today. Exempt inline links, or size them up?
6. **Data-grid responsive divergence.** It scrolls horizontally under a sticky header where the passive
   `Table` collapses to cards. The recorded reason is sound (collapsing orphans the columnheader
   relationships an AT contract needs) and peers agree — but it is a visible inconsistency with Table and
   should be a decision, not a leftover.
7. **Data-grid inline edit.** The brief scoped it OUT as a proposed cut; it is already IN and working.
   Cutting it now would be a deletion, not a deferral.

None of the above was resolved here. Nothing a sub writes is a ruling.

## Proposals for the conductor to merge

- **`--pri-hover` drift, nine snippets** — the two-line fix above. Not a DS improvement; a straight
  re-point. Highest value of anything in this receipt: it should clear `_validate_snippets.py` to rc=0.
- **`_DS-IMPROVEMENTS.md`** (I did not edit it — it is on the ⛔ list): *"Stat-card binds `rag/error` /
  `rag/success` (fill seat) where `s151-D1`/`s155-D1` rule the `-ink` seat for atoms on white. Measured
  1.98:1 green on white. The green pair is undeclared by design under `s151-D2` and therefore only
  visible to `_validate_state_contrast.py` — verify that gate actually runs over `Stat-card`."*
- **`_DS-IMPROVEMENTS.md`**: *"No gate enforces the ruled 44px min-hit-area. Empty-state's recovery link
  measures 18px and has never gone red."*
- **Itinerary reconcile** — `Status = Gap` is false for all 18 Wave-3 rows.
- **CATEGORIES**: nothing owed. All three slugs are long-registered.
- **No new tokens are wanted.** Both values this lane would have asked for (`rag/error-ink`,
  `rag/success-ink`) already exist and are ruled. That is the point of finding 1.

## Friction log

- **The brief's biggest cost was its premise.** Roughly the first fifth of the window went on
  establishing that the components existed — and it was only cheap because step 0 is mandatory. Without
  it this lane would have overwritten three gated artefacts.
- **`_validate_snippets.py` red at HEAD** cost a control pass to attribute (grep the failing set, confirm
  8 of 9 are outside the lane, confirm the values against the store).
- **No `playwright` module in the sandbox**, but the runbook's cached browser (`/var/tmp/pw-browsers-s197`)
  and a peer lane's font farm were both present. `pip install --target /var/tmp/pylibs-s203e` + the
  runbook env landed it in one call. **Do not write "cannot render" without opening that runbook first.**
- **`/var/tmp` is shared across concurrent lanes.** Lane C's font farm was sitting there. I built my own
  symlinked farm rather than write markers into a live sibling's directory.
- **The grid's document-level ids** are the reason its review page differs in construction from the other
  two. Worth knowing before anyone tries to put it in a combined showroom page.
- **The 2-up pane layout clips the grid's Amount column** at ordinary desktop widths — the component's own
  ruled horizontal-scroll behaviour, doing exactly what it should, in a review frame too narrow for it.
  Rather than fake a wider grid, the page carries a **live layout controller** (`Side by side` /
  `Full width`) so Dave can switch. Verified: frame width 726px → **1502px** on toggle.

## Residuals — declared, not glossed

- **`_validate_state_contrast.py` was NOT run.** A filtered run *overwrites* the tracked
  `_STATE-CONTRAST-AUDIT.md` (the #174 receipt records exactly this, and restored it by hand). With five
  sibling lanes live and no shared-file edits permitted, restoring it was not a risk worth taking.
  **It is the gate that would confirm or clear finding 1's green leg. It is owed, and it belongs to the
  conductor or CI.**
- The stat-card review page at 480px overflows its column (802px computed) — the `.board` carries
  intrinsic minimums. It is single-column and legible; a true narrow-viewport reflow for stat-card boards
  is unexamined and is **not** claimed here.
- `outputs/s203e-renders/` holds six PNGs outside the repo (`s191-D2` NON-REPO marker:
  **NON-REPO: session outputs folder**). They are the agent's own verification, not review artefacts —
  HTML is what Dave reviews.
- `machinery: 0 instrument / ~250 feature` — no gate, checker or harness was built. The three throwaway
  scripts live at `/var/tmp/s203e/` outside the repo.
