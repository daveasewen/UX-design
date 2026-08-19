# Receipt — #203 Wave 3, Lane B · date & time (Date picker · Date-range picker · Time picker)

*Worker receipt per the parallel-conductor checklist and `_BRIEF-wave3-foundations-2026-08-19-v1.md`.*
*⛔ Nothing here is a ruling. No commit, no push, no `git checkout/restore/stash`. `knowledge/_rulings.json` untouched.*

**Gauge at close** — `_checkin.py`: FILL **108,667 real** · boot **56,488** · peak 108,667 over 18 turns ·
room to the advisory stop line 150,929 = **42,262**. Throughput 117,646 real (gauge.count, ONE call —
not comparable to FILL).

---

## ⛔ THE HEADLINE: THIS LANE'S PREMISE WAS FALSE, AND SO WAS EVERY OTHER LANE'S

The brief asked Lane B to build three P1 **gaps** end-to-end. **All three already existed as gated
components and had done since 2026-07-22.** So did the other fifteen. This is the single most
important thing in this receipt and it belongs to the conductor, not to me.

### Step 0 — the premise, verified first-hand before building

| Claim inherited from the brief | Verified? | Evidence (probe named) |
|---|---|---|
| HEAD is unstated; I must read it | HEAD = **`ec2336d`** (#202 wrap) | `git log --oneline -1` |
| My three components are absent | **FALSE — all three present** | `ls knowledge/snippets/` → `Date-picker.reference.html` (530 lines), `Date-range-picker.reference.html` (565), `Time-picker.reference.html` (396) |
| They are un-gated / not through the route | **FALSE — fully gated** | all three in `MIGRATED_SNIPPETS`, `knowledge/_validate_radius.py:85–89`; metas exist (`date-picker.meta.json` 7,858 B, `date-range-picker` 7,210 B, `time-picker` 6,945 B); showroom pages exist (`showroom/date-picker.html` etc.); canon.css carries 74 / 79 / 57 `.cn-<slug>` rules |
| The itinerary carries them as P1 gaps | **TRUE, and the itinerary is STALE** | `ITINERARY-2026-07-14…xlsx` rows 14/15/16 all read `Status = Gap`. The file is dated **2026-07-14**; the components were built **2026-07-22** (Phase-2 wave 2, per the snippet header provenance). The Status column has never been updated as waves landed. |
| Type-composite debt is 1,101 | **STALE — measured 1,097** | `_validate_type_composites.py`, rc=1, "1097 violation(s) across 90/91 file(s)" |

**Wave-wide, measured, not inferred.** I tested all eighteen components named across lanes A–F for
presence at HEAD:

```
for n in Form-layout Textarea Alert Date-picker Date-range-picker Time-picker Amount-input \
         Amount-display Secure-entry Toast Drawer Popover Empty-state Stat-card Data-grid \
         Skeleton-loader File-upload Stepper; do git cat-file -e HEAD:knowledge/snippets/$n.reference.html; done
⇒ PRE-EXISTING = 18   ABSENT = 0   of 18
```

**Every single component in Wave 3 already existed.** The `?? reviews/REVIEW-203-*` entries in
`git status` show the other five lanes reached the same wall independently.

### What I did instead of building duplicates

Building a second `Date-picker.reference.html` was impossible inside the fence (NEW files, *unique
names*) and wrong outside it — it would have violated write-once (ADR-0017), [[specimen-starts-from-reference]]
("specimens COPY the approved artefact, never re-draw") and, if I had overwritten, #202's exact
destruction. I did not edit a single existing file.

The genuinely-owed, in-fence work is what the components have *never* had: **a four-theme side-by-side
review surface for Dave's eye**. The showroom offers only a one-theme-at-a-time iframe switcher; per
[[feedback-review-live-variant-spread]] Dave rules on a full live spread. That is what I built, plus
a conformance audit against the rules that were ruled *after* these components were built.

---

## Deliverables

| File | State |
|---|---|
| `reviews/REVIEW-203-date-picker-four-themes-v1.html` | NEW — 4 themes × light/dark + 360px responsive strip |
| `reviews/REVIEW-203-date-range-picker-four-themes-v1.html` | NEW — same, with the 6–14 July range demo |
| `reviews/REVIEW-203-time-picker-four-themes-v1.html` | NEW — same, listbox rather than calendar |
| `notes/_receipts/2026-08-19-203-wave3-laneB-date-time.md` | NEW — this receipt |

**Nothing else was created, edited or deleted.** No generator that rewrites shared outputs was run;
`_build_all.py` was not run.

**Provenance of the review pages — they are copies, not re-draws.** Each page extracts the specimen
markup from the gated snippet's own `<body>` (sprite, live field, states gallery, static panel),
strips only the snippet's demo prose (`<h2 class="sec">`, `<p class="note">`), and renders it through
the generated `canon.css` via `.cn-<slug>` + `data-apollo-theme` — the grammar of
`REVIEW-174-progress-bar-four-themes-v1.html`, copied. The calendar day cells are produced by a
**faithful Python port of the snippet's own `build(gridEl, y, m, {live:false})`** (same class strings,
same `aria-selected` / `aria-current` / `is-empty` / `in-range` logic), not hand-drawn. IDs are
suffixed per pane so eight copies do not collide; sprite refs (`#ic-*`) stay global.

⚠ **Declared:** the pages pin "today" to **22 July 2026** so the today-ring is visible in every pane.
The live snippet follows the real date. This is stated on each page, not just here.

---

## Gates — every rc, captured directly (not after a pipe)

⚠ The #174 friction repeated on my first reading: `rc=$?` after `| tail` reads `tail`'s status and
returned a false `0`. Re-measured with the exit code captured directly; the figures below are the
second, correct reading.

| Gate | Result at HEAD | My three files | Verdict |
|---|---|---|---|
| `_validate_snippets.py` | **rc=1** — 76 snippets, **18 failures** | **0 failures** — no Lane B row in the output | ✅ mine clean; the 18 are pre-existing |
| `_validate_a11y.py` | **rc=0** — 76 snippets, 0 failures, 179 warnings | **0 failures, 0 warnings attributable** | ✅ |
| `_validate_type_composites.py` | **rc=1** — 1,097 violations across 90/91 files | **9 violations each = 27** | ❌ **see below** |
| `_validate_radius.py` | not re-run (no radius binding touched) | — | declared gap |
| `_validate_state_contrast.py` | **not run** — exceeds the call cap on 76 snippets (#174 residual, unchanged) | — | **declared gap, conductor's** |

**All 18 snippet-gate failures are the same pre-existing defect and none are mine:**
`DRIFT --pri-hover (light) = #626262 but button/primary/background/hover = #636363` and
`(dark) = #B7B7B7 but … = #B2B2B2`, across Action-bar, Button, Confirmation, Drawer, Empty-state,
Form-layout, Icon-button, Modals, Stepper. This looks like the `--pri-hover` rename/mint from #198
(`s198-D1`/`s198-D2`) landing in the token store but not in the nine snippets — **CI is red at HEAD
independently of Wave 3.** Flagged for the conductor; not mine to fix.

⛔ **THE BRIEF'S "YOUR FILES MUST CONTRIBUTE 0" TEST CANNOT BE MET BY THIS LANE, AND THE REASON MATTERS.**
The brief assumed new files. My three components are *old* files, authored 2026-07-22, before the
composite ratchet bit. Each carries 9 raw font declarations — `font-family: var(--font)` on `body`,
`font: 500 16px/1.3 var(--font)` on `h2.sec`, `font: 400 14px/1.5` on `p.note`,
`font: 400 16px/24px` on the field input, plus `font-weight` on placeholder and completed states.
**27 violations total, all inside the standing 1,097 — the ratchet has not been broken, and I added
nothing.** Fixing them means editing gated snippets, which is outside this lane's fence. Queued as a
proposal below.

---

## Conformance audit — the three, measured against the rules ruled AFTER they were built

These components predate `s149-D1`, `s151-D1`, `s175-D1`/`s176-D1` and the composite ratchet. I
checked each rule in brief §5 rather than assuming.

| Rule | Finding |
|---|---|
| **Four themes** | ✅ All four resolve distinctly. Measured per pane: mono `#FFFFFF`/`#1A1A1A`, legacy text `#333333`, supercharge `#F7F6F4`/`#13110E`. |
| **Two-red law** (`s151-D1`, MONO only) | ✅ Not violated. All three carry `#F6604C` as `rag/error` and no `#DA1A00` — which matches the canon body (`Alert.reference.html` post-151 does the same; only 2 of 76 snippets carry `#DA1A00`, both non-error uses). Legacy/Supercharge carry their own `--error: #B92F1E`; the two-red law is mono-only, so this is expected, not drift. **I nearly recorded a false finding here and checked the population first.** |
| **Mono error ink camp** (`s149-D1`/`s194-D1`) | ✅ `--mark-error: #1A1A1A` on `#F6604C`; no white-on-error anywhere. Confirmed by eye in the render — the error triangle carries a dark mark, the message is ink. |
| **Type composites** | ❌ 27 violations, above. |
| **Square corners** | ✅ radius bound to `border-radius/control` and `border-radius/surface`; all three are in `MIGRATED_SNIPPETS`, i.e. strict. |
| **44px min-hit-area** | ✅ **enforced by hand, as the brief requires.** The 4 `.dp-nav`/`.dr-nav` controls are 44×44 with `--phys-size:44`; the tail button is 24×24 with a `::before` 36px extended target (deliberate — 44 would spill the 46px field box, documented in the snippet header). **Day cells measured 40×40 in the render — under 44, above the 24px gating floor**, so the a11y gate passes them as a WARN class. Calling that acceptable is a judgment I am not making; it is listed under Decisions needed. |
| **Ink ruled** (`s175-D1`/`s176-D1`) | ⚠ See the Supercharge finding below. |
| **`#token-manifest` with passing pairs** | ✅ present in all three; the snippet gate reads them and passes. ⚠ It resolves against the **mono base only** and cannot see the Legacy/Console/Supercharge legs — the #174 caveat, unchanged. |

---

## Three findings, with their evidence

**1 · The calendar grammar is duplicated by copy, not shared — and nothing stops it drifting.**
I diffed the grid/nav/day/panel/head rule bodies between `Date-picker` (`.dp-*`) and
`Date-range-picker` (`.dr-*`): **19 shared rule keys, 18 byte-identical, 1 differing — and the one
difference is a CSS comment** (`/* … Icon-button precedent — divides the pixel-true travel */` vs
`/* … Icon-button precedent */`). Geometry is identical: `repeat(7, 40px)`, `gap:4px`, 44×44 nav,
`box-shadow: inset 0 0 0 2px var(--border-active)` for today, ink-knockout selection.
`date-range-picker.meta.json` already declares `$consumes: "Date-picker (panel + grid + keyboard
model — change it there)"` — but that is prose. **No gate enforces it**, so the two can silently
diverge. The brief's Lane B mandate ("share one calendar-grid grammar") is therefore satisfied in
*substance* and unenforced in *mechanism*.

**Time picker is correctly excluded**: it is a listbox (Dropdown language — 44px options, tabular
figures, weight + tick selection), because time has no calendar. Its shared grammar with the other
two is the **field anatomy** (Input-fields box + tail button), which it already consumes. Confirmed
in the render: 0 day cells in every Time-picker pane, 35 in every Date-picker pane.

**2 · Supercharge dark: `--page` is mono `#1A1A1A` while the theme's own dark ink is `#13110E`.**
Measured in the render: the Supercharge-dark pane surface paints `rgb(19,17,14)` = `#13110E`, but the
component's knockout numeral paints `rgb(26,26,26)` = `#1A1A1A`, because
`canon.css:11742` sets `--page: #1A1A1A` in the Supercharge-dark block while `--text` *is* warm
(`#F7F6F4`). **This is not Lane B's and not new**: I counted the Supercharge-dark component blocks —
**76 of 76 set `--page: #1A1A1A`.** It is theme-wide. Before writing it up as an open question I
searched, per `s202-D3`: it is the **known G14 item, "SC dark still awaits Dave"**
(`_TRIAGE-TICKLIST-2026-08-02-v1.md:37`, `_CHAIN.md:100`, `_HANDOFF-117…:74`). So this is **new
measured evidence for an existing open item (n=76), not a new question.** Surfaced, never swapped
[[feedback-grey-tint-check]].

**3 · The calendar panel has a hard ~336px floor and no answer below it.**
Seven 40px cells + six 4px gaps + panel padding ≈ 336px, and none of it compresses. In the 360px
responsive strip the panel overflows its column. The snippet's own `@media (max-width:520px)` sets
`min-width:304px`, which does not solve it. On a 360px phone the calendar needs either smaller cells
or a full-screen presentation. **Neither is ruled.** Shown deliberately on each review page with a
note saying the clipping is the finding, not a page bug.

---

## Render proof

`goto("file://…")`, never `set_content()`. Symlink-farm fontconfig per `_RUNBOOK-render-verify.md`
§SYMLINK FARM (`/var/tmp/fonts-s203b`, cachedir outside the repo, `<include>` present).

**Font asserted with controls, not a boolean** — the runbook's exact probe, identical on all three
pages and at both widths:

| probe | measured | reading |
|---|---|---|
| `HSBC_MtUnivers_Latin` | **347** | the real cut |
| `"Univers Next HSBC"` (type.css `--uf`) | **347** | alias resolves |
| `"Univers Next for HSBC"` (snippet `--font`) | **347** | alias resolves |
| `DejaVu Sans` — control | 375 | genuinely different face |
| nonexistent face — control | 301 | default fallback |

**Numeric assertions across all 9 panes per page** (8 theme panes + 1 responsive), driven not eyeballed:
Date picker 35 day cells / 1 selected / 1 today / 0 in-range · Date-range picker 35 / **2 endpoints** /
1 today / **7 in-range** (7–13 July, i.e. strictly between 6 and 14) · Time picker 0 / 0 / 0 / 0.
Cells measured **40×40** in every theme. Selection inverts correctly per theme
(mono light `#1A1A1A` on white → mono dark white on `#1A1A1A`). **Duplicate element IDs: 0** on every page.

**Rendered at two widths** (1180 and 480) per the runbook — one width proves one layout.
**Overflow assert, all full-width panes: 0** on all three pages, after a fix (below). PNGs were
**read**, not merely produced: `s203b-crop-supercharge.png`, `s203b-fix-time-picker.png` in `outputs/`.

⚠ **The render caught a real defect in my own page that every numeric check had passed** — exactly
what renders are for. The first Date-range-picker build put the From/To pair row in a 260px gallery
column; it overflowed by 40px and the error message clipped mid-word. Found by reading the PNG,
fixed by stacking `.dr-row` inside review panes (which is what the component itself does below
520px), re-rendered, re-asserted 0 overflow. Two of my own scripts also crashed loud and named
(a `Time picker` vs `Time-picker` filename typo; a broken Python string literal in a patch) — both
mine, both fixed, neither a repo condition.

**Tree asserted clean:** `.uuid` strays in the TTF dir = **0**; `git status --short
--untracked-files=all -- knowledge/` = **3 lines**, none of them mine — see residuals.

---

## Decisions needed — PROPOSED #203, Dave's eye owed (⛔ none of this is ruled)

Each is marked `PROPOSED #203, Dave's eye owed` and surfaced on the relevant review page.

1. **The Wave-3 premise itself.** All 18 components exist. Is Wave 3 re-scoped from *build* to
   *audit-and-review*, or is there a quality bar these 2026-07-22 builds miss that the brief meant
   by "gap"? **This one is the conductor's to put to Dave before any lane builds anything.**
2. **The itinerary Status column.** 3 of 3 Lane B rows say `Gap` for components built four weeks
   ago. Propose the itinerary is regenerated from `knowledge/snippets/` rather than hand-maintained
   — a stale status column is what sent six Opus lanes at built work. Not fixed here (shared file).
3. **27 type-composite violations** across the three. Propose a follow-up lane rebinds all three onto
   `.t-cm-*`/`.t-ed-*`. Shrink-only ratchet means this can only help. Outside this lane's fence.
4. **Promote the calendar grid to a shared partial** so Date-picker and Date-range-picker cannot
   drift (18 of 19 rules byte-identical today). ⚠ This is **component promotion**, which is on the
   brief's DO-NOT-RULE list — raised as an observation with its measurement, nothing more.
5. **40×40 day cells vs the 44px default.** Above the 24px gating floor, below the HSBC 44. Accept as
   a calendar-specific exception, or grow the cells?
6. **The 336px calendar floor on a 360px phone** — smaller cells, or full-screen presentation?
7. **Day cells carry no press physics** (selection targets, not buttons). A #147-era decision that
   was receipt-flagged for review at the time and has never been ruled. Still open.
8. **`.dp-nav`/`.dr-nav` button-family `$members` registration** (ADR-0013) — still unmade, as the
   2026-07-22 receipt proposed.
9. **The in-range tint** uses `form/background/hover` and is subtle in dark. Worth Dave's eye in
   Legacy and Supercharge dark specifically — but note it is deliberately never the only channel
   (endpoints change weight, every cell carries `aria-selected`), which matters given red/yellow
   instability.

## Proposals for the conductor to merge

- **`_DS-IMPROVEMENTS.md`** (I did not edit it — shared file): the `--pri-hover` DRIFT across 9
  snippets, red at HEAD, apparently #198's mint not propagated to snippets.
- **`_DS-IMPROVEMENTS.md`**: G14 evidence — `--page: #1A1A1A` in **76 of 76** Supercharge-dark
  component blocks against a `#13110E` theme ink.
- **No `CATEGORIES` entries needed** — all three slugs are already in `gen_showroom.py`'s index
  (showroom pages exist).
- **No new tokens wanted.** I found nothing this lane needed that the store lacks.

## Friction log

1. **The brief's premise was false for every lane, and the brief itself told me to check it.** Step 0
   is the reason this receipt says something useful instead of producing a duplicate component. The
   two probes that did it were four seconds of `ls` and `git cat-file`.
2. **`rc=$?` after a pipe** — #174 logged this and I still did it once. It reads `tail`'s status. The
   friction is that the correct form is more awkward to type than the wrong one.
3. **`_validate_snippets.py` WRITES a shared tracked file** — `knowledge/_SNIPPET-AUDIT.md`
   (line 354, `open(…, "w")`). The brief instructs **all six lanes** to run this gate while
   forbidding shared-file edits. Six lanes clobbering one audit file is the #158 write-by-default
   class. **The fence and the instructions contradict each other here.** A `--check`/`--no-write`
   flag would resolve it.
4. **`_validate_state_contrast.py` still cannot run over the full population in-sandbox** — the #174
   residual, unchanged, and it silently overwrites the tracked audit when run filtered. I did not run
   it rather than risk the clobber with five other lanes live in the tree.
5. **`/var/tmp/pylibs-s203e` already existed** — another Wave-3 lane staged Playwright before me. I
   reused it read-only per the runbook and staged only my own font farm. Cheap, and worth the
   conductor knowing that lanes are sharing sandbox state.

## Residuals — declared, not glossed

- **`_validate_state_contrast.py` NOT RUN.** Declared gap, conductor's or CI's.
- **`_validate_radius.py` not re-run** — I bound no radius. Declared gap.
- **`knowledge/` shows 3 modified tracked files**: `_REVIEW-SIGNOFF.md`, `_SNIPPET-AUDIT.md`,
  `_graph-mark-observations.jsonl`. `_SNIPPET-AUDIT.md` is written by `_validate_snippets.py`, which
  the brief told me to run — **so my gate run may have touched it, and so may five other lanes'.**
  With six lanes live in one tree I **cannot attribute these with certainty** and will not pretend
  otherwise. The conductor should reconcile them explicitly rather than `git add -A`.
- **The other lanes' `REVIEW-203-*.html` files** were already untracked in the tree when I looked;
  they are not mine and I did not touch them.
- **`machinery: 0 instrument / ~330 feature`** — no gate, checker or harness was built. The three
  throwaway scripts (`/var/tmp/s203b/{mkreview,run,shoot,crop2,diag}.py`) live outside the repo and
  are not instruments the repo carries. If the conductor wants the four-theme review generator to
  become an instrument, that is a separate, priced decision.
