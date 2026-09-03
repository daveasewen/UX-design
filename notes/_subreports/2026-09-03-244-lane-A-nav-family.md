# `#244`-`lane-A` — the navigation/menu family was already built; the lane measured it instead of duplicating it

session: `#244` · 2026-09-03
window: lane A (§C·1 strand (b), "Wave 3 fan-out (component library)" — navigation/menu family)
sub index: `lane-A`
brief: relayed in-window by the conductor (no `notes/_briefs/` file was cut for this lane —
declared, not assumed)
tokens: `UNMEASURED` — a lane sub cannot read the conductor's `message.usage`, and this seat had
no `_gauge_tokens.py` reading of its own window.

## VERDICT

**The lane built ZERO of its four, on purpose, and the reason is a recurrence the repo has already
named four times.** Every navigation/menu member the brief lists as a build candidate —
top-nav/app-bar, side-nav, tabs, menu/dropdown, breadcrumb — **already exists in the store today,
gated, with real behaviour.** I probed **16** nav-family members live against all five register
signals (snippet · meta · showroom · radius ratchet · canon `.cn-` rules) at 2026-09-03 and every
one carries snippet + meta + showroom page + 49–156 canon rules, with 7–199 lines of authored JS.
Building four of them would have handed the conductor four duplicates of gated canonical artefacts.

The brief's "~26 remain" figure is the **fifth recurrence of the frozen-column class**. It does not
come from any live measurement: `reviews/ITINERARY-STATUS-2026-08-25-v4.json` measures **GAP 1**
across 124 rows (row 86, "Brand mark / logo", derived ASSET-ONLY — not a nav component), plus one
Layer-2 GAP at row 124. The frozen 2026-07-14 cell says **78 Gap**. The "~26" agrees with neither;
it is a third, older figure carried in the §C·1 strand-(b) sentence itself
(`knowledge/_memento-index.json`, strand (b): *"~26 itinerary gaps remain"*). ⚠ **The #218 fix
worked at the register and did not reach the queue line** — see finding 2, which is the real news
of this lane.

So the lane converted its budget into the measurement the family actually needs — *quality, not
existence* — and returns eight findings, five ruling-shaped questions, and nine exact registry
lines the conductor is owed.

COUNTS: findings `8` · ruling-shaped `5` · UNPROVEN `4`

## What was done

**BUILD region — REFUSED, with the finding returned in its place.** No
`knowledge/snippets/*.reference.html` and no `knowledge/components/*.meta.json` was written. Zero
files created or modified anywhere in the repo except this report.

**Serial set — untouched, as fenced.** No registry, no `MIGRATED_SNIPPETS`, no `CATEGORIES`, no
spine, no `_build_all.py`, no git. No edits to `GOOD-MORNING.md`, `_LIVE-STATE.md`, `_CHAIN.md`,
`_CARRIES.md`, `knowledge/_rulings.json`, `knowledge/tokens/*`, or MEMORY. No ruling taken.

**Measurement region — DONE.** Gates driven this session, live:

| gate | result |
|---|---|
| `knowledge/_validate_snippets.py` | **136 snippets, 0 failures** — BEFORE and AFTER identical, because this lane wrote no snippet |
| `knowledge/_validate_radius.py` | 0 strict fails · 0 advisory pending · 4 physical corner longhands DECLARED ADVISORY (#221) |
| `knowledge/_validate_dark_surfaces.py` | 0 flat-white failures · 9 annotated exceptions |
| `knowledge/_validate_polarities.py --check` | GREEN — five refusals asked, none fired; three generated files content-fresh |
| `knowledge/_validate_no_hardcode.py` | PASS over **11 tranche files** — ⚠ nav snippets are OUT of this gate's scope (finding 6) |
| `knowledge/_validate_type_composites.py` | **FAIL — 1091 violations across 90/151 files** store-wide; **34 of them are in this family** (finding 4) |
| `knowledge/_validate_state_contrast.py` | **COULD-NOT-ASK** — playwright installed, chromium binaries absent on this box. ⛔ NOT a skip: these arms run BLOCKING in the `render` job of `.github/workflows/gates.yml`; that job is the proof of record. Nothing here is claimed green. |

## Findings

**1 · All 16 nav-family members are GATED in the store, probed live 2026-09-03.**
Probe: filesystem + an *imported* `_validate_radius.MIGRATED_SNIPPETS` + `knowledge/canon/canon.css`
text (1,903,149 B) + 145 showroom files. Never read out of the register — that would be a tautology.

| row | member | snippet B | js ln | meta | showroom | ratchet | canon `.cn-` |
|---|---|---|---|---|---|---|---|
| 28 | Tabs | 15,187 | 89 | ✓ | ✓ | ✓ | 71 |
| 29 | Tab-bar | 16,899 | 41 | ✓ | ✓ | **✗** | 65 |
| 30 | Breadcrumbs | 5,611 | 7 | ✓ | ✓ | **✗** | 49 |
| 31 | Pagination | 9,283 | 75 | ✓ | ✓ | **✗** | 55 |
| 32 | Nav / Menu (`Navigations`) | 25,619 | 125 | ✓ | ✓ | **✗** | 78 |
| 33 | Dropdown menu | 13,416 | 45 | ✓ | ✓ | ✓ | 65 |
| 34 | Stepper (interactive) | 28,963 | 126 | ✓ | ✓ | ✓ | 119 |
| 35 | Command palette | 34,594 | 199 | ✓ | ✓ | ✓ | 82 |
| 36 | Sidebar / nav rail | 29,312 | 95 | ✓ | ✓ | ✓ | 90 |
| 37 | Anchor / scrollspy | 17,723 | 61 | ✓ | ✓ | ✓ | 66 |
| 38 | Back-to-top | 11,876 | 49 | ✓ | ✓ | ✓ | 65 |
| 97 | App shell — top nav | 52,224 | 103 | ✓ | ✓ | **✗** | 143 |
| 98 | App shell — side nav | 61,168 | 118 | ✓ | ✓ | **✗** | 156 |
| 102 | App shell — doormat | 53,229 | 111 | ✓ | ✓ | **✗** | 142 |
| 103 | App shell — nav rail | 57,338 | 99 | ✓ | ✓ | **✗** | 130 |
| 115 | Lock-up — page header | 27,997 | 99 | ✓ | ✓ | **✗** | 111 |

The register's whole `Navigation` category is **11 rows, all 11 `derived: GATED`**. There is no
navigation gap to fill.

**2 · ⚠ THE FROZEN-COLUMN CLASS RECURRED A FIFTH TIME, AND IT RECURRED *THROUGH* ITS OWN FIX.**
This is the finding of the lane. `#218` diagnosed the class and enacted R1 option (a) at the
writer: the register field was renamed `itinerary_status` → **`itinerary_status_2026_07_14_FROZEN`**
and given a `$columns` block reading *"⛔ NOT A WORKLIST: counting 'Gap' here counts a photograph of
July, not the store."* **That fix holds — and the queue line never read the register.** §C·1
strand (b) carries its own hard-coded prose number (*"~26 itinerary gaps remain"*), which matches
neither the frozen 78 nor the measured 1. The rename fixed the file a brief would open; it could
not fix a number already transcribed into the queue sentence six weeks earlier.

Mechanically: the #218 remedy gated the **register**, but the defect lives in the **queue**, and
nothing reads one against the other. This is [[instrument-without-a-consumer]] in its exact shape —
a rename cannot fail, and a comment cannot fail. Prior recurrences: #196 (chart wave-2 divvy read as
open), #199 (`data/axis`+`data/grid` "to mint" — already enacted 2026-07-23), #203 (six-lane wave
briefed off it, 18 of 18 "P1 gaps" already gated), #218 (wave-3 divvy, "78 Gap"). This lane is
**five**. See ruling-shaped question 1.

**3 · The nav family splits cleanly on build era, and the split is visible in every quality signal.**
Probe: `_validate_type_composites.py` output filtered to family filenames.

| cohort | members | type violations |
|---|---|---|
| **P0 six + Stepper** (oldest) | Tabs, Tab-bar, Breadcrumbs, Pagination, Navigations, Dropdown, Stepper | **34** |
| **later nine** | Command-palette, Sidebar-nav, Anchor-nav, Back-to-top, the four App-shells, Page-header-lockup | **0** |

Per file: Tabs 8 (TYPE-001 ×1, TYPE-002 ×5, +2 elided) · Stepper 8 · Dropdown 7 (TYPE-001 ×1) ·
Breadcrumbs 5 (TYPE-001 ×1) · Navigations 3 · Pagination 2 · Tab-bar 1. **TYPE-001 = the file does
not pull `canon/type.css` at all** — true of Tabs, Breadcrumbs and Dropdown, three of the six P0
heads of the family. The family's real gap is *depth in its highest-priority, oldest members*, not
breadth.

**4 · Four-theme carriage is 7/16 in the snippet inline layer.**
Probe: literal scan for `supercharge` / `console` / `legacy` / `mono` in each snippet.

- **All four named themes present (7):** Command-palette, Sidebar-nav, Anchor-nav, and all four
  App-shells.
- **Partial (2):** Stepper (`legacy` + `mono`), Tabs (`mono` only).
- **None (7):** Tab-bar, Breadcrumbs, Pagination, Navigations, Dropdown, Back-to-top,
  Page-header-lockup.

All 16 carry the **light/dark two-mode** inline block (`[data-theme="light"]` / `[data-theme="dark"]`).
15 of 16 link `canon.css`; **`Tab-bar.reference.html` does not** — so its four-theme rendering has
neither an inline named-theme layer nor the canon projection to inherit one from. That is a single
concrete four-theme hole, not a family-wide one.

**5 · TWO-RED LAW: `#DA1A00` appears ZERO times in the family; `#F6604C` is declared inside
white-page blocks in three files.** Probe: scoped literal scan, resolving each hit to its enclosing
theme block.

| file | line | scope | declaration | page in that scope |
|---|---|---|---|---|
| Dropdown | 53 | `[data-theme="light"]` | `--error:#F6604C` | `--page:#FFFFFF` |
| Stepper | 102 | `[data-theme="light"]` | `--error:#F6604C` /* rag/error */ | white |
| Page-header-lockup | 99 | `[data-theme="light"]` | `--badge-surface:#F6604C` | white |
| Tabs | 58 | `:root` | `--badge-bg:#F6604C` | mode-invariant |

`s151-D1` is background-keyed and firm: **#DA1A00 on white — text AND atoms alike — #F6604C
everywhere else.** Two of these four resolve without a ruling and two do not:

- **Settled, no action.** Tabs `--badge-bg` and Page-header-lockup `--badge-surface` are the badge
  *fill*, explicitly ruled at `s149-D1(3)` and `s122-D2` (*"mono mark on #F6604C, 5.55:1"*,
  mode-invariant). `#F6604C` is the surface, not red-on-white ink. Correct as built.
- **Not settled.** Stepper's `--error` paints **atoms**: `inset 0 -4px 0 0 var(--error)` on
  `.st-group.is-error .st-box` over `background:var(--page)` (white in light), and
  `.st-msg .ic{color:var(--error)}` — a **glyph**. `s151-D1(3)` puts red on the atoms; on white that
  red should read `#DA1A00`. But `s194-D1(2)` says that in MONO, *"the glyphs in mono always the
  default dark ink in both dark and light mode"*. Two live rulings point at the same two lines.
  See ruling-shaped question 2.
- **Dead declaration, mechanical.** Dropdown declares `--error` in both theme blocks and
  **has zero `var(--error)` consumers in the file** (probe: `grep -n "var(--error"
  knowledge/snippets/Dropdown.reference.html` returns nothing). It is an unconsumed token
  declaration, so it is not currently a two-red-law violation of anything rendered — but it is the
  shape of one waiting for its first consumer.

**6 · The two-red atom fork is guarded in canon for exactly ONE component.**
`knowledge/canon/canon.css:2992` mints `--error-atom: var(--rag-error-ink)` with the comment at
:3049 spelling the background keying, and every consumer at :3050–3056 is scoped
`:where(.cn-selection-controls)`. Stepper's error atom is **snippet-local and unguarded** by that
mechanism. Related: `_validate_no_hardcode.py` passes over **11 tranche files only** — no nav
snippet is in its scope, so nothing mechanically holds the family to the two-red law. This is
[[no-gate-parses-the-artefact]].

**7 · The family's hex literals are the snippet fallback idiom, not hardcoding — measured, not
assumed.** 505 live hex literals across the 16 files (comments and CSS comments stripped), against
**805 `var(--…)` reads**. Every literal I resolved sits inside a `:root` / `[data-theme="light"]` /
`[data-theme="dark"]` custom-property *declaration* block — i.e. the standalone reference file's
own token layer, which is what lets it render without `canon.css`. **This is the established
pattern, and I am recording it as compliant so a later reader does not mistake the count for 505
defects.** The `#DB0011` runs (`--logo`, `--indicator`, identical in both light and dark blocks
across the four App-shells) are the legacy brand red carried by precedent, documented in
`Sidebar-nav.reference.html:272` — *"THE BAR IS BRAND RED BY PRECEDENT, NOT BY INVENTION"*.

**8 · `Tabs.meta.json` carries a WIRING ISSUE verdict that the snippet already fixed, unretracted
for 77 days.** `tokenValidation.date: "2026-06-18"`, `result: "WIRING ISSUE — values resolve, but
the component is NOT using its dedicated tabs/* semantic group … it will NOT pick up dark-mode
values"`, with a `shouldRewire` list naming `tabs/active`, `tabs/standard-border`,
`tabs/overflow-border`, `tabs/background`, `tabs/overflow-background`.
**`Tabs.reference.html:49–60` declares all five of those, in both the light and dark blocks.** The
remedy the manifest demands appears already enacted in the artefact; the manifest was never
re-statused. Tabs is the family's only non-PASS `tokenValidation.result`, and it is **stale prose,
not a live defect** — the same assertion-propagation class as finding 2, one layer down. ⚠ I did
not re-run the token-resolution probe that produced the 2026-06-18 verdict, so *"already enacted"*
is CLAIMED from a read-back of the declaration block, not measured. See UNPROVEN.

## Registry lines owed to the conductor

**No new registrations are owed — nothing was built.** What *is* owed is a pre-existing ratchet
gap this lane measured. `MIGRATED_SNIPPETS` in `knowledge/_validate_radius.py` holds **81** of the
store's **136** snippets. **9 of the 16 nav-family members are off it**, each of which the register
flags itself as `ADVISORY: not on the radius ratchet`:

```python
    "Tab-bar.reference.html",
    "Breadcrumbs.reference.html",
    "Pagination.reference.html",
    "Navigations.reference.html",
    "App-shell-top-nav.reference.html",
    "App-shell-side-nav.reference.html",
    "App-shell-doormat.reference.html",
    "App-shell-nav-rail.reference.html",
    "Page-header-lockup.reference.html",
```

⛔ **These are lines to CONSIDER, not lines to paste.** Adding a file to `MIGRATED_SNIPPETS` moves
it from advisory to **strict**, and this lane did **not** run the strict arm against these nine
files. The gate currently reports `0 strict fail(s)` over the 81 that *are* enrolled; whether these
nine pass strict is **UNPROVEN**. Enrolling them blind would convert a green gate red inside the
conductor's serial. Recommended sequence: run `_validate_radius.py` with the nine added in a
throwaway copy first, then enrol what passes.

Store-wide the same gap is **55 snippets off the ratchet of 136** — the nav family is a 9/55 slice
of a larger, pre-existing question that is not this lane's to answer.

## Declared skips, each with its size

1. **The four builds the brief asked for — top-nav/app-bar, side-nav, tabs, menu/dropdown,
   breadcrumb. SKIPPED, ~0 tokens spent on them.** Grounds: all five exist and are gated (finding
   1). Size if the conductor overrides and wants them anyway: **4 × ~25–50 KB snippet + meta**, and
   the product is four duplicates of gated artefacts entering the regen serial.
2. **Render-verify / four-theme × light-dark render matrix. SKIPPED — no browser on this box.**
   `_validate_state_contrast.py` returned COULD-NOT-ASK (chromium binaries absent). Price to prove:
   **16 components × 4 themes × 2 modes = 128 renders**, or the CI `render` job on next push,
   which is where that gate's proof of record already lives.
3. **`_build_all.py`. NOT RUN — fenced by the brief and by `_CHAIN.md`'s standing warning** that
   any partial run strands the tree in the documented mid-build intermediate.
4. **Re-running `gen_itinerary_status.py` to refresh the 9-day-old register. SKIPPED —
   `reviews/` is outside this lane's region.** Price: one generator run. Mitigated: every store
   figure in this report was re-probed live at 2026-09-03 rather than read from the snapshot.
5. **Fixing the 34 type-composite violations in the P0 seven. SKIPPED — snippet edits were the
   *build* mandate this lane declined**, and editing seven gated files is a different job from the
   one briefed. Price: ~34 declaration rewrites plus a `canon/type.css` link in 3 files.

## RULING-SHAPED QUESTIONS

⛔ **Dave's word, unscoped. Nothing below is decided here.**

1. **The frozen-column class has now recurred five times, and the #218 fix did not stop the fifth
   — does the QUEUE get gated, or does the queue line get regenerated?** The rename worked on the
   register; §C·1 strand (b) still carries *"~26 itinerary gaps remain"*, a number matching no
   measurement anywhere. Priced options, none enacted: **(a)** the strand-(b) sentence stops
   carrying a literal count and carries the register *pointer* only, so the reader must open the
   measured column — ~10 minutes, one sentence, but it is a prose edit and prose edits are exactly
   what went stale five times; **(b)** the count in §C·1 becomes **generated** from
   `ITINERARY-STATUS-*.json`'s `derived` field at every `_gen_chain.py` run, so it cannot disagree
   with the store — ~1 lane-hour, and it fixes the class at the writer the way #218 fixed the
   register; **(c)** a gate that refuses any brief or queue line citing a Gap count that disagrees
   with `derived` — the strongest, but it needs the brief-parser #218 already priced at ~half a day
   and still does not exist. **Recommend (b)**: (a) is the patch that Dave's *"always real fixes
   never patches, they just get lost"* names, and (c) prices a parser to catch what (b) makes
   impossible to write.

2. **Stepper's error atom on white: `#DA1A00` per the two-red law, or default dark ink per the
   mono glyph rule?** Two live rulings reach the same two lines
   (`Stepper.reference.html:194,199`). `s151-D1(3)` puts the background-keyed red on atoms —
   #DA1A00 on white. `s194-D1(2)` says mono glyphs ride the default dark ink in both modes.
   Options: **(a)** the underline atom takes `#DA1A00` on white and the `.st-msg .ic` glyph takes
   default ink — splits the two by carrier, honouring both rulings, 2 line edits; **(b)** both take
   `#DA1A00` — two-red law reads wider than the mono glyph rider; **(c)** both take default ink —
   the glyph rule generalises to the error atom, and the family stops carrying red here at all.
   **Recommend (a)**, because it is the only option that contradicts neither ruling — but the
   carrier split is a *judgment about what an inset underline is*, and that is Dave's.

3. **Is wave-3's subject existence or QUALITY?** #218 lane α put this and it was never answered;
   this lane reaches it from a different family and the answer now governs whether §C·1 strand (b)
   has any work left in it at all. With every nav member gated, the only work this lane could find
   is depth: 34 type violations concentrated in the P0 six, three files not pulling `type.css`,
   9/16 off the radius ratchet, 7/16 without a four-theme inline layer. Options: **(a)** wave 3 is
   **closed** on existence and a new depth pass is cut as its own strand with its own name;
   **(b)** wave 3 is **re-scoped in place** to mean depth over the gated families; **(c)** wave 3
   stays as written and the lane briefs keep finding nothing to build. Not decided here.

4. **Do the 9 nav-family snippets get enrolled in `MIGRATED_SNIPPETS` (advisory → strict)?**
   The register flags each as advisory; enrolment is a one-way ratchet into a blocking gate whose
   pass this lane did not measure. Options: **(a)** enrol all 9 after a throwaway strict run,
   dropping any that fail — ~30 min; **(b)** enrol none, and rule the 55-off-ratchet store-wide gap
   as its own lane, since 9/55 is a slice not a family; **(c)** enrol the 4 App-shells only, which
   were built latest and are cleanest on every other signal. **Recommend (b)** — the gap is not
   navigation-shaped and fixing a slice of it hides the size of the rest.

5. **`intent` is absent from all 16 nav metas and present in 15 of 137 store-wide — 14 of those 15
   are charts. Is `intent` a chart-only manifest field, or a general one the whole store owes?**
   The wave-2 exemplar this lane was told to copy (`Chart-butterfly-h.meta.json`) carries it; no
   nav meta does. Options: **(a)** chart-only by design — say so in `meta.schema.json` and the
   question closes permanently, ~15 min; **(b)** general and owed — 122 metas need it, which is a
   programme, not a lane; **(c)** general but only for interactive components — a middle scope that
   needs its own boundary ruled. Recommend nothing: this is a schema question and I have no basis
   to prefer a scope.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN — the family's rendered four-theme correctness.** No render was driven this session.
  `_validate_state_contrast.py` was COULD-NOT-ASK (no chromium binaries). Every four-theme figure
  in finding 4 is a claim about **file text** — which named themes appear in which snippet — never
  about pixels. Price to prove: 128 renders (16 × 4 themes × 2 modes), or read back the CI `render`
  job on next push.
- **UNPROVEN — whether the 9 ratchet-missing files pass `_validate_radius.py` STRICT.** The gate's
  reported `0 strict fail(s)` covers the 81 enrolled files only. Price: one throwaway run with the
  nine added, ~5 minutes.
- **UNPROVEN — that the 34 type-composite violations are the *whole* family debt.** The gate elides
  after the first six per file ("+N more"); I reconstructed the elided counts from its own summary
  lines, so the per-file totals are the gate's arithmetic, not a line-by-line enumeration.
- **CLAIMED — that `Tabs.meta.json`'s WIRING ISSUE is already remedied in the snippet** (finding 8).
  Basis: `Tabs.reference.html:49–60` declares all five `tabs/*` custom properties the manifest's
  `shouldRewire` list names, in both theme blocks. I did **not** re-run the 2026-06-18 token
  resolution that produced the verdict, so this is a read-back of a declaration block, not a
  measurement of resolution. Price to prove: re-run the token-resolution probe against Tabs, ~2K.
- **CLAIMED — the register figures** (`GAP 1`, `$true_gaps [86]`, `$drift_counts`,
  `itinerary_status_2026_07_14_FROZEN: Gap 78`) are read from
  `reviews/ITINERARY-STATUS-2026-08-25-v4.json`, measured **2026-08-25**, 9 days old. The **store**
  figures in finding 1 were re-probed live 2026-09-03 and do not depend on it.
- **DECLARED — no `_state.json` store rows** for this report; the store is fenced from this seat.
  Rows owed at the conductor's wrap (the `#185` forgotten-document class, same declaration the
  #218 lanes made).

## Tree state left for the conductor (reconcile every path)

- **New (untracked), MINE — exactly one path:** `notes/_subreports/2026-09-03-244-lane-A-nav-family.md`.
- **Modified: NONE by this lane.** `git status` at 16:12 shows 6 modified paths — `_LIVE-STATE.md`,
  `knowledge/_capture_gate.py`, `knowledge/_graph-mark-observations.jsonl`, `knowledge/_lanes.json`,
  `notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl` — **all with mtimes 15:36–16:00,
  before this lane's first gate run, and none in this lane's region.** Pre-existing dirt, declared so
  it is not attributed here. Every gate this lane drove is read-only or was called in a
  refuse-to-write mode (`_validate_polarities.py --check`).
- **Also untracked, NOT MINE:** `knowledge/_memory_cap_check.py` ·
  `notes/_subreports/2026-09-03-244-lane-C-debt-sweep.md` (lane C).

## Evidence

No `notes/_subreports/assets/2026-09-03-244-lane-A-nav-family/` directory was created — this lane
produced no artefact files. Every figure above is reproducible from the repo in one command; the
probes are named inline at each finding. The three that carry the verdict:

- `python3 knowledge/_validate_snippets.py` → `snippet gate: 136 snippet(s), 0 failure(s)`
- `python3 knowledge/_validate_type_composites.py` → `TYPE GATE FAIL — 1091 violation(s) across
  90/151 file(s). TYPE-001 ×29 · TYPE-002 ×1046 · TYPE-003 ×16`
- `python3 -c "import json; d=json.load(open('reviews/ITINERARY-STATUS-2026-08-25-v4.json')); print(d['\$counts'], d['\$true_gaps'])"`
  → `{'GATED': 121, 'ASSET-SYSTEM': 1, 'ASSET-ONLY': 1, 'GAP': 1} [86]`
