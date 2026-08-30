# s227 lane 1 — the grill-me skill, and the two canon radius gaps fixed at cause

**COUNTS: built 3 · repaired 2 · ruling-shaped 6 · UNPROVEN 3**

Sub: Opus build sub, session #227, lane 1. Conductor: Fable seat.
⛔ No rulings, no store rows, no W-rows, no commits. Everything ruling-shaped is a `Q:` for Dave.

---

## Files touched

**Built (3)**

- `apollo-spider/skills/grill-me/SKILL.md` — new skill, designer-facing.
- `apollo-spider/skills/grill-me/brief-template.md` — the brief shape, blank + one filled example.
- `apollo-spider/skills/generate-from-canon/SKILL.md` — **addition only**, +10 lines, 0 deletions:
  a `0. Brief first.` step ahead of the existing step 1. No existing step was rewritten.

**Repaired at source (15 snippets + 2 regenerated artifacts)**

| file | change |
|---|---|
| `knowledge/snippets/Chart-{bar,boxplot,bullet,butterfly-h,butterfly-v,candlestick,combo,donut,histogram,line,pie,scatter,stacked-area}.reference.html` (13) | `.dv-tbl-toggle,.dv-vt` base rule gains `border-radius:var(--border-radius-control)` |
| `knowledge/snippets/Chart-{line,combo}.reference.html` (2, same files) | `.dv-toggle-seg` gains `border-radius:var(--seg-rad-xs)`, `.dv-toggle-seg .ind` gains `border-radius:var(--seg-thumb-xs)`; two new manifest binds + two harness declarations |
| `knowledge/snippets/{Search-field,Filter-toolbar-bar}.reference.html` (2) | base `.search` rule gains `border-radius:var(--border-radius-control)`; Search-field also gains the manifest bind + harness declaration it was missing |
| `knowledge/canon/canon.css` | **regenerated**, not hand-edited |
| `showroom/*.html` (15) | **regenerated**, not hand-edited |

---

## The emitter, found before anything was edited

`knowledge/canon/canon.css` is a built artifact between `AUTO-COMPONENTS` markers
(lines 1220–20027). Its emitter is `knowledge/canon/gen_canon_components.py`, and its
**source of truth is `knowledge/snippets/*.reference.html`** — the generator carries every
snippet rule verbatim, scoped `:where(.cn-<slug>)`. A hand-edit inside those markers
evaporates at the next build. So every repair below was made in the snippet and the
artifact regenerated.

Ran, in this order, nothing else, and **never `_build_all.py`**:

```
python3 knowledge/canon/gen_canon_components.py            → generated 135 components
python3 knowledge/canon/gen_canon_components.py --check     → OK — 135 components in sync
python3 knowledge/gen_showroom.py                           → 135 page(s), 15 written, 0 orphans
python3 knowledge/gen_showroom.py --check                   → OK — 135 page(s) + index in sync
```

`gen_showroom.py` is the **second** consumer of the same snippets; leaving it stale would
have been a red CI on the same edit. Its 15 rewritten pages are exactly the 15 snippets
touched — nothing else moved.

### One trap the generator set, and how it was avoided

`gen_canon_components.py` treats a var **declared in the snippet harness but absent from
its `token-manifest`** as a local literal and copies its value into canon
(`.cn-search-field{--border-radius-control:0}`). Search-field had **no** radius bind at
all, so adding only the harness `0` would have **hard-frozen search at square in every
theme** — the exact defect, one layer deeper. The manifest entry
`"--border-radius-control": "border-radius/control"` is what makes the generator skip the
literal and let the global token through (`tokenvar(token) == v → continue`). Both were
added together. Verified: `.cn-search-field{…}` contains **zero** `--border-radius-control`
declarations.

---

## B5 — the search field bound no radius

**Was:** `.search` in `.cn-search-field` and `.cn-filter-toolbar-bar` carried no
`border-radius` in any scope, while `.trigger` and `.tag` **on the same toolbar row** bind
`border-radius/control`. In console that is an 8px dropdown and 8px chips beside a square
search box.

**Now:** bound on the **base** `.search` rule — not on `.search.boxed` — so the underline
and boxed variants take the same shape. Precedent for binding a control radius on an
underline-construction control is already canon in two places: `Dropdown.reference.html`
`.trigger` (`border:0; border-bottom:1px` **+** `border-radius:var(--border-radius-control)`)
and `Input-fields.reference.html` `.uctrl input` (same construction, same bind).

**Proof, in the regenerated artifact:**

```
:where(.cn-search-field) .search{…}         → border-radius:var(--border-radius-control)  ✓
:where(.cn-filter-toolbar-bar) .search{…}   → border-radius:var(--border-radius-control)  ✓
```

**Second, independent receipt** — the showroom page's own theme meter moved:

```
showroom/search-field.html:45  −  6 token(s) · Legacy re-binds 1
                               +  7 token(s) · Legacy re-binds 1
showroom/search-field.html:64  +  {"attr": "console", … "hits": 1, "note": "Apollo Console: 1 var(s) re-bound."}
```

Console now re-binds one var on the search field where it re-bound none. That is the
rounding, counted by the showroom generator rather than asserted by me.

## B6 — the chart toolbar's three square boxes

**Was:** `.dv-tbl-toggle` (Copy data CSV), `.dv-vt` (View as table) and `.dv-toggle-seg`
(Target line / Last year) bound no radius, in 13 chart snippets. Dave repaired
`.dv-toggle-seg` and its `.ind` **by hand, in his own page**, on 2026-08-30 — the two
border-radius declarations his dashboard carries. `.dv-tbl-toggle` and `.dv-vt` he did not
catch, and they stayed square beside his repaired pair.

**Now, at source:**

- `.dv-tbl-toggle,.dv-vt` → `border-radius:var(--border-radius-control)`, matching
  `.dv-legrow` in the **same** chart snippets, which already binds it.
- `.dv-toggle-seg` → `var(--seg-rad-xs)` = `border-radius/segmented-container/xs`;
  `.dv-toggle-seg .ind` → `var(--seg-thumb-xs)` = `border-radius/segmented-thumb/xs`.
  This is **Dave's own hand-patch, promoted to the source** — same two tokens, same scale.

**Proof, in the regenerated artifact** (parsed, not grepped by eye):

```
:where(.cn-<chart>) .dv-tbl-toggle, :where(.cn-<chart>) .dv-vt{…}
   13 base rules · 13 carry border-radius:var(--border-radius-control) · 0 without
:where(.cn-chart-line)  .dv-toggle-seg{… border-radius:var(--seg-rad-xs);}
:where(.cn-chart-combo) .dv-toggle-seg{… border-radius:var(--seg-rad-xs);}
:where(.cn-chart-line)  .dv-toggle-seg .ind{… border-radius:var(--seg-thumb-xs);}
:where(.cn-chart-combo) .dv-toggle-seg .ind{… border-radius:var(--seg-thumb-xs);}
.cn-chart-{line,combo}{--seg-rad-xs:var(--border-radius-segmented-container-xs);
                       --seg-thumb-xs:var(--border-radius-segmented-thumb-xs);}
```

**And the token values confirm the intended look:** in console
`--border-radius-segmented-container-xs: 6px` and `--border-radius-segmented-thumb-xs: 0`.
The toggle frame rounds to 6px, the floating fill inside stays square — which is exactly
what Dave's hand-patched page renders. The repair reproduces his page token-for-token,
rather than re-deciding it.

---

## Zero unintended diff

Every changed line in `canon.css`, enumerated and counted:

```
13 −    flex:none; transition:border-color var(--ease);}
13 +    flex:none; transition:border-color var(--ease); border-radius:var(--border-radius-control);}
 2 ± .dv-toggle-seg{…}  + border-radius:var(--seg-rad-xs);}
 2 ± .dv-toggle-seg .ind{…}  + border-radius:var(--seg-thumb-xs);}
 2 ± .search{…}  + border-radius:var(--border-radius-control);}
 2 + --seg-rad-xs / --seg-thumb-xs scope binds
 + the s227 decision comments (carried verbatim from the snippets, as the generator does)
```

Nothing else. No other selector, no other token, no other component moved.
`git diff --numstat -- showroom/` = 15 files, 1–3 lines each, all of them mine.

## Gates driven (not assumed)

| gate | verdict |
|---|---|
| `gen_canon_components.py --check` | ✅ 135 components in sync |
| `gen_showroom.py --check` | ✅ 135 pages + index in sync |
| `gen_snippet_tokens.py --check` | ✅ 4814 binds, 0 values would change |
| `_validate_binds_resolve.py` | ✅ 135 snippets (2169 vars), 0 failures |
| `_validate_property_resolves.py` | ✅ 147 files, 0 failures |
| `_gate_dataviz_vars.py` | ✅ 767 refs across 4 themes, all resolve |
| `_validate_snippets.py` | ✅ 135 snippets, 0 failures |
| `_validate_radius.py` | ✅ exit 0 |
| `_validate_no_hardcode.py` | ✅ 11 tranche files |
| `_validate_descender_clip.py` | ✅ specificity ratchet at zero, 151 files |
| `_release/_gate_frozen_release.py --check` | ✅ 3 arms, no frozen surface moved |
| `_release/_gate_release_audit.py --check` | ❌ **RED — and red BEFORE this lane** (see below) |

**The release-audit red is not mine.** Probed properly rather than assumed: `git stash`,
re-run, `git stash pop`. The gate printed the **identical** fresh sha
`f580ed2097a99259` against `f1003d9e9a794db8` on disk, with and without this lane's
changes. `_pack_manifest.json` is pinned at commit `1e028a1` (#225) while HEAD is
`bc288a7` (#227) — the drift predates this lane and this lane does not widen it.

---

## Ruling-shaped — Dave's, not mine (6)

**`Q1:` Search radius on the BASE rule, or on `.boxed` only?**
I bound the base rule, so the underline search rounds too. Precedent says base (Dropdown's
`.trigger`, Input-fields' `.uctrl input` — both underline constructions, both bind control
radius). But a rounded *underline* field is a shape decision, not a bug fix.
**Proposed-not-ruled default.** If Dave wants only the boxed variant rounded, the change is
moving one declaration from `.search` to `.search.boxed` in two snippets and regenerating.

**`Q2:` I widened B6 from one chart to thirteen.** The diff report named `.cn-chart-line`
and noted the pattern "lives in chart-combo and by inspection in chart-bar / donut / pie".
It is in **13** chart snippets, identical text in all. Fixing only chart-line would have
made the line chart round and the other twelve square — a new inconsistency in place of an
old one. So the whole class was repaired. If Dave wants it narrower, the revert is scoped
per file.

**`Q3:` `.dv-toggle-seg` takes the segmented atom's shape pair, not `--border-radius-control`.**
Copied from Dave's own hand-patch. It means the toggle frame and the neighbouring
`Copy data` button take **different** radii in console (6px vs 8px) — visible, and
deliberate on his part in his own page. Confirming it here makes it canon.

**`Q4:` A1 is still open and still square.** The segmented control's own radius binding
(`canon.css:14307 .seg{border-radius:var(--seg-rad)}`) is still overridden to nothing by
`.cn-chart-line .seg` and `.cn-filter-toolbar-bar .seg`, which re-declare `.seg` without a
radius and sit earlier in the file. **Out of this lane** (A1, not B5/B6) — but the
consequence is that after this repair the chart toolbar reads: rounded segmented switch
only if the page adds its own `.cn-segmented-control` wrapper, rounded toggles, rounded
Copy/View — and a **square view switch** wherever that wrapper is absent. Worth a lane.

**`Q5:` `grill-me` is not in the pack manifest and is not versioned.** Per the brief,
nothing under `memento-package/`, `dist/`, any manifest, ledger or `RATIFY_IDS` was
touched. The manifest's `skills` group currently lists **5** files
(`apollo-spider/skills/*/SKILL.md`); the generator reads **git-tracked** paths, so
`grill-me/` is invisible to it until staged. Once staged, that group goes **5 → 7 files**
and the pack cut needs regenerating on Dave's release word.

**`Q6:` "Common" appears in designer-facing copy while the code key is still `legacy`.**
Per the brief the rename is a separate lane, so nothing was renamed. `grill-me/SKILL.md`
says **Common *(code key: `legacy`)***. If the rename lands, that parenthetical drops; if
it doesn't, the parenthetical is the only place the two names are reconciled for a
designer.

---

## UNPROVEN (3)

1. **No render.** No headless browser on this box. Every radius claim above is
   **structural** — the declaration is in the artifact, the token resolves per theme, the
   value is `6px`/`8px` in console and `0` in mono. Nobody has **looked** at a rounded
   search field or a rounded chart toolbar. A render pass in console light + dark is owed
   before this is called done.
2. **The showroom regen is proven by its own `--check` and by the search-field theme meter
   (`6 → 7 token(s)`, console re-binds 1), not pixel-compared.** 15 files, 1–3 lines each,
   all in scope — but a character-level diff of the base64 payloads was attempted and
   timed out on ~1MB single-line files, so the payload delta is inferred from the snippet
   delta, not read.
3. **`grill-me` has never been run.** It is written, not driven. Nobody has answered its
   six questions and watched a brief get written, and `generate-from-canon`'s new step 0
   has not been exercised against a real `briefs/*-grill.md`. First designer to use it is
   the first test. The skip semantics in particular — full skip, per-question skip, the
   announced mono default — are **prose, not behaviour**, until a session runs them.

---

## The grill-me skill, in one paragraph

Six questions, theme first, each with a one-line visual consequence
(**Mono = square, zero radius, deliberately**; **Console = the rounded one**;
**Common** *(code key `legacy`)*; **Supercharge** = warm neutrals, square). Then
light/dark/both · density and width · brand assets · real-or-placeholder data · a single
closing question folding accessibility commitments together with *anything the system must
not do* — six asks total, because designers skip walls of questions. A full skip
(*"skip the grill"*) and a per-question skip both exist; a skipped question is written into
the brief as `skipped`, and if the **theme** is skipped the skill **announces mono before
building** and records it as `skipped — proceeding with Mono (announced <date>)`, so a
default is on the record as a default and never as a choice. Answers land in
`briefs/<date>-<task>-grill.md`, one line per answer, all six present including the skipped
ones. `generate-from-canon` step 0 reads the newest brief and **cites** it in its
used/missing note; with no brief it asks the one theme question and explains why — because
mono makes every radius zero, so a mono build is radius-blind and cannot show you a shape
decision you might have wanted. That sentence is A2, written where the next designer will
hit it.

---

## REPLAY-THESE

1. **The emitter, not the artifact.** `canon.css` is generated from
   `knowledge/snippets/*.reference.html` by `knowledge/canon/gen_canon_components.py`.
   A radius fix typed into `canon.css` between the `AUTO-COMPONENTS` markers is gone at the
   next build. **Two** generators consume those snippets — `gen_canon_components.py` and
   `gen_showroom.py` — so a snippet edit that regenerates only one leaves the other red.
2. **A harness var without a manifest bind gets HARD-FROZEN into canon.** The generator
   copies a `[data-theme]`-declared var that is not in `token-manifest` as a **literal**.
   Declaring `--border-radius-control:0` in Search-field's harness *without* the manifest
   entry would have shipped `square` to every theme — the defect, one layer deeper, with
   every gate green. Add the two together, always.
3. **Dave's hand-patch is the ruling, promoted.** His page's two border-radius declarations
   named the exact tokens (`segmented-container-xs` + `segmented-thumb-xs`); the repair
   copied them rather than re-deriving a "better" pair. Console's values (6px container,
   0 thumb) confirm the copy reproduces his page.
4. **Probe a red before you own it.** The release-audit red looked like this lane's until
   `git stash` → re-run → `git stash pop` printed the identical fresh sha. It predates the
   lane. A gate that was already red is not evidence about your change.
5. **A skipped question must be written down.** The A2 defect was a silent default (mono,
   never asked, never announced). The cure is not "ask more" — it is "record the skip and
   announce the default". Six questions, all skippable, none silent.
