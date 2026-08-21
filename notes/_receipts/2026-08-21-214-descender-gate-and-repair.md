# #214 — descender-clip: the specificity leg (G1) + the 18-selector repair

**Opus build sub, session #214.** Builds on this morning's READ-ONLY audit,
`notes/_receipts/2026-08-21-214-descender-cascade-audit.md`, which is this receipt's spec.

**No commits. No rulings.** `_rulings.json`, `_state.json`, GM/LS and the chain were not touched.

---

## 0 — AUTHORISATION

Dave, in chat today, on the audit's §5 recommendation (G1 + the 18-selector repair, including the
**gated** `Sidebar-nav.reference.html`, which ds-005's fence otherwise guards):

> **"This sounds great. lets get these done"**

That nod covers **both halves**: the gate leg and the repair. The audit had flagged
`Sidebar-nav.reference.html` as needing Dave's nod specifically ("⛔ `Sidebar-nav.reference.html` is
a **gated** component — its repair needs Dave's nod, not a lane's", audit §5). It has it, and it is
repaired below.

---

## 1 — HALF 1: THE SPECIFICITY LEG

`knowledge/_validate_descender_clip.py`, new leg beside the existing one. Existing leg untouched.

### What was wrong with the gate

Leg 1 builds a set of authored selector **strings** and asks only "does a rule bearing this exact
string declare `text-box-edge:text text` somewhere in the file". It has no model of specificity,
source order, or the cascade. So a file could carry the ds-005 override, never apply it, and pass.
That is what all 43 review components did.

### The arithmetic the leg now resolves

Every reference snippet carries its own private copy of the global leading-trim rule:

```
:is(button,a,label,span,…,input[type=text],input[type=search],…):not(:has(svg))
    { text-box-trim:trim-both; text-box-edge:cap alphabetic; }
```

* `:is()` takes the specificity of its **most specific argument** — `input[type=text]` = **(0,1,1)**
* `:not(:has(svg))` takes `:has(svg)` takes `svg` = **(0,0,1)**
* total = **(0,1,2)**

A bare single-class override `.sn-label{text-box-edge:text text;}` is **(0,1,0)**. It loses. The
label keeps `cap alphabetic` and clips every descender against its own `overflow:hidden`.

> **⚠ ONE CORRECTION TO THE AUDIT, and it changes no verdict.** The audit measured the trim rule at
> **(0,1,1)**; the correct figure is **(0,1,2)** — its resolver did not carry the `svg` inside
> `:not(:has(svg))`. Every one of the 18 verdicts is identical under both figures (both beat
> (0,1,0); both lose to (0,2,0)). Recorded because a resolver that is quietly wrong by one type
> selector is a thing a later session must not inherit. `canon.css:6645` states (0,1,2) — the canon
> comment was right and the audit's resolver was the drifted copy.

### The rule the leg enforces

> Every `text-box-edge:text text` override must **out-specify** (or tie and follow) every
> `text-box-edge:cap alphabetic` trim rule that could match the same subject element.

Scoped deliberately to `text-box-edge:text text`. Leg 1's other accepted override,
`overflow:visible`, works by removing the clipping box rather than the trimmed edge, so it is not
subject to this comparison and is not flagged.

### What was built (all in `knowledge/_validate_descender_clip.py`)

| Function | Job |
|---|---|
| `specificity(sel)` | Selectors-4 (a,b,c). `:is()`/`:not()`/`:has()`/`:matches()` take the most specific argument; `:where()` contributes zero; `:nth-child(… of S)` = one pseudo-class + most specific S; `*` free; single-colon `:before/:after/:first-line/:first-letter` counted as pseudo-elements |
| `_split_top(s, sep)` | comma-split at nesting depth 0 — **the bug that bit first**: `_selectors()` (leg 1's splitter) splits on *every* comma and shredded the `:is(a,b,c)` list into fragments, so the first run compared overrides against `input[type=text]` alone and returned a wrong 66. Named here because leg 1 still has that behaviour and it is only harmless because leg 1 does string equality |
| `_subject(sel)` | rightmost compound — the element the rule actually styles |
| `_tags` / `_top_classes` / `_could_match_same` | conservative disjointness. Returns False **only when the two provably cannot match the same element** (disjoint tag sets, or a trim class the override's subject cannot carry). An unprovable case is reported, not skipped — a silent skip is exactly leg 1's hole |
| `check_specificity(css, where)` | returns `(override, trim, ovr_spec, trim_spec, file)` for every cascade-dead override |

Failures are loud and named: file + **both** selectors + **both** specificities + the remedy.

### Birth proof — 18/18

Driven over the full `DEFAULT_TARGETS` (151 files) **before** any repair:

```
✗ CASCADE-DEAD descender override: `.sn-brand` (0,1,0) in knowledge/snippets/App-shell-multi-column.reference.html
✗ CASCADE-DEAD descender override: `.sn-label` (0,1,0) in knowledge/snippets/App-shell-multi-column.reference.html
✗ CASCADE-DEAD descender override: `.sn-brand` (0,1,0) in knowledge/snippets/App-shell-side-nav.reference.html
✗ CASCADE-DEAD descender override: `.sn-label` (0,1,0) in knowledge/snippets/App-shell-side-nav.reference.html
✗ CASCADE-DEAD descender override: `.dr-title` (0,1,0) in knowledge/snippets/Document-row.reference.html
✗ CASCADE-DEAD descender override: `.dr-meta`  (0,1,0) in knowledge/snippets/Document-row.reference.html
✗ CASCADE-DEAD descender override: `.sn-brand` (0,1,0) in knowledge/snippets/Sidebar-nav.reference.html
✗ CASCADE-DEAD descender override: `.sn-label` (0,1,0) in knowledge/snippets/Sidebar-nav.reference.html
✗ CASCADE-DEAD descender override: `.mr-payee` (0,1,0) in knowledge/snippets/Standing-order-mandate-row.reference.html
✗ CASCADE-DEAD descender override: `.mr-meta`  (0,1,0) in knowledge/snippets/Standing-order-mandate-row.reference.html
✗ CASCADE-DEAD descender override: `.tl-title` (0,1,0) in knowledge/snippets/Template-detail.reference.html
✗ CASCADE-DEAD descender override: `.dr-title` (0,1,0) in knowledge/snippets/Template-detail.reference.html
✗ CASCADE-DEAD descender override: `.dr-meta`  (0,1,0) in knowledge/snippets/Template-detail.reference.html
✗ CASCADE-DEAD descender override: `.dr-title` (0,1,0) in knowledge/snippets/Template-list-index.reference.html
✗ CASCADE-DEAD descender override: `.dr-meta`  (0,1,0) in knowledge/snippets/Template-list-index.reference.html
✗ CASCADE-DEAD descender override: `.tl-title` (0,1,0) in knowledge/snippets/Timeline.reference.html
✗ CASCADE-DEAD descender override: `.ldg-name` (0,1,0) in knowledge/snippets/Transaction-row.reference.html
✗ CASCADE-DEAD descender override: `.ldg-ref`  (0,1,0) in knowledge/snippets/Transaction-row.reference.html
```

**18 selectors, 9 snippets — byte-for-byte the audit's set.** Nothing more, nothing fewer, no file
outside the audit's nine.

---

## 2 — MUTATION PROOFS (both ways, on the REAL gate, on REAL files)

No fixture stub. Every run below drove `knowledge/_validate_descender_clip.py` itself against real
repo files, per [[mutation-tests-the-clause-not-the-feature]].

### 2a — SABOTAGE a green file → RED

```
$ cp knowledge/snippets/Timeline.reference.html /var/tmp/mut214/Timeline.sabotaged.html
mutation applied: `.tl-line .tl-title` -> `.tl-title` (the pre-repair form)

$ python3 knowledge/_validate_descender_clip.py /var/tmp/mut214/Timeline.sabotaged.html
  ✗ CASCADE-DEAD descender override: `.tl-title` (0,1,0) in .../Timeline.sabotaged.html
      LOSES to the leading-trim rule `:is(button,a,label,span,small,strong,b,th,td,dt,dd,li,figcaption,lege…` (0,1,2) in the same file.
      The declaration is present but never applies — the label still renders with
      `cap alphabetic` and clips its descenders. Promote it to a descendant form
      that out-specifies the trim (see knowledge/canon/canon.css:4714-4724).

DESCENDER-CLIP GATE FAIL (specificity leg) — 1 descender-safe override(s) are CASCADE-DEAD…

MUTATION-1 (sabotaged) RC=1  <- expect 1
DESCENDER-CLIP GATE PASS — every truncating label is descender-safe AND every descender-safe override wins its cascade (1 file(s)).
CONTROL (repaired) RC=0  <- expect 0
```

### 2b — FIX a dead one → GREEN (on the pre-repair file, straight out of git)

```
$ git show HEAD:knowledge/snippets/Document-row.reference.html > /var/tmp/mut214/Document-row.pre.html
205:  .dr-title{flex:1; min-width:0; color:var(--text); text-decoration:none;
207:  .dr-meta{flex:1; min-width:0; color:var(--muted); opacity:var(--alpha-72);

--- gate on the PRE-REPAIR file (expect RED, 2 dead) ---
  ✗ CASCADE-DEAD descender override: `.dr-title` (0,1,0) in .../Document-row.pre.html
  ✗ CASCADE-DEAD descender override: `.dr-meta` (0,1,0) in .../Document-row.pre.html
DESCENDER-CLIP GATE FAIL (specificity leg) — 2 descender-safe override(s) are CASCADE-DEAD…
RC=1 <- expect 1

fixed `.dr-title` -> `.dr-line .dr-title` ONLY; `.dr-meta` left dead
  ✗ CASCADE-DEAD descender override: `.dr-meta` (0,1,0) in .../Document-row.pre.html
DESCENDER-CLIP GATE FAIL (specificity leg) — 1 descender-safe override(s) are CASCADE-DEAD…

fixed `.dr-meta` -> `.dr-line .dr-meta`
DESCENDER-CLIP GATE PASS — every truncating label is descender-safe AND every descender-safe override wins its cascade (1 file(s)).
RC=0 <- expect 0
```

The half-way step matters: **2 → 1 → 0**. The count tracks the repair one selector at a time, so the
leg is counting real defects, not emitting a per-file verdict.

### 2c — BLINDNESS CONTROL: the OLD gate on the exact same file

First attempt crashed on `ModuleNotFoundError: No module named '_helpgate'` (the scratch copy sat
outside `knowledge/`). **A crash is not a fail** — re-run honestly from inside the tree:

```
$ cp /var/tmp/mut214/gate_old.py knowledge/_gate_old_214_tmp.py     # = git show HEAD:…
$ python3 knowledge/_gate_old_214_tmp.py /var/tmp/mut214/DR.pre2.html
DESCENDER-CLIP GATE PASS — every truncating label is descender-safe (1 file(s)).
OLD GATE (leg 1 only) RC=0 <- 0 means it is BLIND to the 2 dead overrides
```

The pre-#214 gate certifies as green the exact file the new leg fails with two named defects. That
is the class defect, reproduced on demand. Scratch copy deleted; `git status` confirms no residue.

### 2d — THE RATCHET IS DRIVEN TOO (a fence nobody crossed is not a fence)

```
allowance 47 (one below truth):
✗ SPECIFICITY RATCHET BROKEN — canon/canon.css: 48 cascade-dead override(s), allowance 47.
  You have ADDED 1. This number may only shrink…
RATCHET-DRIVE RC=1 <- expect 1

allowance 49 (one above truth):
↓ SPECIFICITY RATCHET CAN TIGHTEN — canon/canon.css: 48 cascade-dead override(s), allowance 49.
  Lower SPECIFICITY_RATCHET to 48…
SLACK-DRIVE RC=0 <- expect 0 + tighten notice
```

### 2e — selftest, both legs

```
selftest OK — flags un-overridden ellipsis labels; accepts text-text / overflow-visible / same-rule / comma-group overrides; ignores containers + sr-only.
selftest OK (specificity leg) — :is()/:not()/:has()/:where() resolved; cascade-dead single-class override caught where leg 1 is blind; two-class form accepted.
```

The specificity selftest includes the assertion `check(dead_case,"t") == []` — i.e. it **asserts leg
1's blindness in code**, so leg 1 can never quietly grow the ability and let leg 2 rot untested.

---

## 3 — HALF 2: THE 18 REPAIRS

Form: the two-class descendant selector canon itself was repaired with
(`canon.css:4713-4724` — `.cn-app-shell-multi-column .sn .sn-label, … {text-box-edge:text text;}`,
render-measured there at `clipBelow 0.00`). Ancestor chosen per file from the snippet's own markup,
verified present. **Selector text only — no declaration, value, markup or comment was changed.**

| # | Snippet | Line | Before | After |
|---|---|---|---|---|
| 1 | `Transaction-row.reference.html` | 232 | `.ldg-name` | `.ldg-desc .ldg-name` |
| 2 | `Transaction-row.reference.html` | 234 | `.ldg-ref` | `.ldg-desc .ldg-ref` |
| 3 | `Standing-order-mandate-row.reference.html` | 198 | `.mr-payee` | `.mr-line .mr-payee` |
| 4 | `Standing-order-mandate-row.reference.html` | 200 | `.mr-meta` | `.mr-line .mr-meta` |
| 5 | `App-shell-side-nav.reference.html` | 227 | `.sn-brand` | `.sn .sn-brand` |
| 6 | `App-shell-side-nav.reference.html` | 249 | `.sn-label` | `.sn .sn-label` |
| 7 | `App-shell-multi-column.reference.html` | 243 | `.sn-brand` | `.sn .sn-brand` |
| 8 | `App-shell-multi-column.reference.html` | 254 | `.sn-label` | `.sn .sn-label` |
| 9 | `Template-list-index.reference.html` | 378 | `.dr-title` | `.dr-line .dr-title` |
| 10 | `Template-list-index.reference.html` | 380 | `.dr-meta` | `.dr-line .dr-meta` |
| 11 | `Template-detail.reference.html` | 278 | `.tl-title` | `.tl-line .tl-title` |
| 12 | `Template-detail.reference.html` | 341 | `.dr-title` | `.dr-line .dr-title` |
| 13 | `Template-detail.reference.html` | 343 | `.dr-meta` | `.dr-line .dr-meta` |
| 14 | `Sidebar-nav.reference.html` ⛔gated | 64 | `.sn-brand` | `.sn .sn-brand` |
| 15 | `Sidebar-nav.reference.html` ⛔gated | 86 | `.sn-label` | `.sn .sn-label` |
| 16 | `Document-row.reference.html` | 205 | `.dr-title` | `.dr-line .dr-title` |
| 17 | `Document-row.reference.html` | 207 | `.dr-meta` | `.dr-line .dr-meta` |
| 18 | `Timeline.reference.html` | 142 | `.tl-title` | `.tl-line .tl-title` |

Each edit was matched on the **rule that actually carries the override** (`Transaction-row` has two
`.ldg-ref{` rules — the second is `display:none` inside a container query and was correctly left
alone by that guard), and each site was asserted unique before writing.

### ⚠ 3 FURTHER LINES CHANGED, AND WHY — a promotion can invert a LATER rule

Promoting a rule raises its specificity against **every** later single-class rule that touches the
same properties, not just the trim. I scanned for that before trusting the repair and found **four
real inversions**, all `flex` in responsive blocks, all of which the repair would have silently
broken:

| Snippet | Rule that would have been out-specified |
|---|---|
| `Standing-order-mandate-row` | `@container (max-width:360px){ .mr-payee{flex:1 1 100%;} }` |
| `Template-list-index` | `.dr-title, .dr-meta{flex:1 1 100%;}` (both) |
| `Document-row` | `.dr-title{flex:1 1 100%;}` |

Each was promoted to the same two-class form, restoring the original relative order:

```
.mr-payee{flex:1 1 100%;}              ->  .mr-line .mr-payee{flex:1 1 100%;}
.dr-title, .dr-meta{flex:1 1 100%;}    ->  .dr-line .dr-title, .dr-line .dr-meta{flex:1 1 100%;}
.dr-title{flex:1 1 100%;}              ->  .dr-line .dr-title{flex:1 1 100%;}
```

Re-scan after: **remaining collisions: 0.** This is 3 lines beyond "the override selectors only" and
is declared here rather than buried: without them the repair fixes descenders and breaks the
narrow-width reflow. `git diff -- knowledge/snippets/` is 21 changed lines total, every one a
selector.

---

## 4 — FULL GATE, GREEN, COLD

Second bash call, fresh process, no state carried:

```
$ python3 knowledge/_validate_descender_clip.py
selftest OK — flags un-overridden ellipsis labels; accepts text-text / overflow-visible / same-rule / comma-group overrides; ignores containers + sr-only.
selftest OK (specificity leg) — :is()/:not()/:has()/:where() resolved; cascade-dead single-class override caught where leg 1 is blind; two-class form accepted.

⚠ REPORT-ONLY TRANCHE HOLDING — canon/canon.css: 48 cascade-dead descender override(s), at the
  allowance. NOT a pass: these labels clip today. The absorb prefixer is the cause. ⛔ The repair is
  a cross-file class remedy on gated canon — Dave's call, not a lane's.
DESCENDER-CLIP GATE PASS — every truncating label is descender-safe AND every descender-safe override wins its cascade (151 file(s)).

COLD FULL-GATE RC=0
```

Leg 1 green over all 151. Leg 2 green over all 150 blocking files. Zero cascade-dead overrides
outside canon.css.

---

## 5 — ⚠ THE FINDING NOBODY ASKED FOR: canon.css HAS 48 OF ITS OWN, AND THE ABSORB PREFIXER IS WHY

Driving the leg surfaced a second, larger tranche the audit never measured, **including selectors
canon's own comments record as repaired and render-measured**.

The absorb step that copies a snippet into `canon.css` prefixes `.cn-<component>` onto both the trim
rule and the override — but the trim rule's `:is()` **arguments get prefixed too**:

```
snippet trim   :is(…, input[type=text], …):not(:has(svg))                        (0,1,2)
canon   trim   .cn-x :is(…, .cn-x input[type=text], …):not(:has(svg))            (0,3,2)   +2 classes
snippet ovr    .sn .sn-label                                                     (0,2,0)
canon   ovr    .cn-x .sn .sn-label                                               (0,3,0)   +1 class
```

**The trim gains one more class than the override does.** A repair that wins in the snippet loses in
canon. The prefixer is not specificity-preserving, and it inverts precisely the fix ds-005 exists to
protect. Examples from the run — every one of these is a rule a prior session believed it had fixed:

```
.cn-app-shell-multi-column .sn .sn-label   (0,3,0)  loses (0,3,2)     <- canon.css:4724, the "repaired" one
.cn-cascader .cs .cs-value                 (0,3,0)  loses (0,3,2)     <- canon.css:6652, "#210 … `text` after"
.cn-combobox .cb .cb-box input             (0,3,1)  loses (0,3,2)     <- canon.css:9322, "#211 lane R5 repairs it"
.cn-transaction-row .ldg-name              (0,2,0)  loses (0,2,2)
```

**⚠ UNPROVEN BY RENDER.** This is a static resolution, not a browser measurement. It is corroborated
by canon's own first-hand comments (which state the same `:is()` rule and the same (0,1,2) figure)
and my resolver reproduces the audit's snippet set exactly — but **G2, the `--computed` leg, is the
only thing that would prove it, and G2 is priced-not-built.** The prior "measured after: `text`"
readings were almost certainly taken against the **snippet**, where the two-class form does win.
Treat this section as a PRICED TODO, not a settled fact.

### What I did about it, and what I deliberately did NOT do

**NOT repaired.** 48 selectors, cross-file, on gated canon; the render proof is unbuilt; and
`canon.css:9316` already says in as many words that *"the cross-file ds-005 class remedy is Dave's
call, not a repair's"*. Blocking the build for a defect nobody has been authorised to fix would fail
CI for everyone.

**Instead: a shrink-only ratchet, not a waiver.** `SPECIFICITY_RATCHET` in the gate holds
`canon/canon.css: 48`. Every one of the 48 prints on every run. **49 turns the build RED** (driven,
§2d). **47 prints a tighten instruction** (driven). It cannot rot into a silent pass, and the number
can only ever go down. Leg 1 remains blocking everywhere with zero waivers, exactly as ds-005 was
closed.

---

## 6 — RESIDUALS, NAMED AND PRICED

| # | Residual | State |
|---|---|---|
| R1 | **G2 — `--computed` render leg.** The only thing that proves the FEATURE rather than the clause. Now also the only thing that can settle §5. | PRICED NOT BUILT — ~3 h · ~45 K, plus per-build render cost, real CI-environment risk |
| R2 | **G3 — trigger widening.** Leg 1 and leg 2 both fire only off `text-overflow:ellipsis`. A trimmed label clipped by a fixed-height or `overflow:hidden` ancestor with no ellipsis is invisible to both. | PRICED NOT BUILT — ~40 min · ~8 K, **report-only first**, expected to surface new debt |
| R3 | **canon.css: 48 cascade-dead overrides + the non-specificity-preserving absorb prefixer.** §5. Two candidate remedies: repair 48 selectors, or fix the prefixer so it stops inverting. The second is the class fix. | ⛔ **DAVE'S CALL.** Ratcheted at 48, unrepaired, render-unproven. Scoping pass owed before either can be priced |
| R4 | **`showroom/*.html` now lag the snippets.** They carry base64-encoded copies (`atob` payload), so all 9 repaired snippets have stale twins there, and `reviews/REVIEW-213-…` renders downstream of those. Regen owed via `knowledge/gen_showroom.py` — **which is itself modified in the working tree by another lane**, so I did not run it. | HANDOFF to the conductor |
| R5 | **Gate glob scope.** `DEFAULT_TARGETS` = `type.css`, `canon.css`, `snippets/*.html`, `_proforma/*.html` = 151 files. `showroom/`, `reviews/` and every other generated artefact are **outside both legs**. Per [[gate-glob-scope-rule]] this leg rules only as wide as that glob. | NAMED NOT FIXED |
| R6 | **`_validate_no_hardcode.py` covers 11 tranche files, not 135.** Carried forward unchanged from the audit §3. The audit's tokenisation verdict was its own measurement, not that gate's. | NAMED NOT FIXED (audit's finding, re-declared so it does not drop) |
| R7 | **ds-005 has no `_rulings.json` row** — it lives only in `_DS-IMPROVEMENTS.md` prose, so a retrieval-by-default query answers "never decided" ([[forgotten-document-class]]). Same now true of this receipt. | ⛔ store writes were out of scope for this sub — **conductor owes both rows** |
| R8 | **The audit's resolver was wrong by one type selector** ((0,1,1) vs (0,1,2), §1). Verdicts unaffected; recorded so the figure in the audit receipt is not copied forward. | CORRECTED HERE |

---

## 7 — WORKING TREE, RECONCILED

Mine, and only these:

```
M knowledge/_validate_descender_clip.py                       (+353 / the leg + ratchet + selftests)
M knowledge/snippets/App-shell-multi-column.reference.html    (2 selector lines)
M knowledge/snippets/App-shell-side-nav.reference.html        (2)
M knowledge/snippets/Document-row.reference.html              (3 — incl. 1 order-restore)
M knowledge/snippets/Sidebar-nav.reference.html               (2)
M knowledge/snippets/Standing-order-mandate-row.reference.html(3 — incl. 1 order-restore)
M knowledge/snippets/Template-detail.reference.html           (3)
M knowledge/snippets/Template-list-index.reference.html       (3 — incl. 1 order-restore)
M knowledge/snippets/Timeline.reference.html                  (1)
M knowledge/snippets/Transaction-row.reference.html           (2)
+ notes/_receipts/2026-08-21-214-descender-gate-and-repair.md (this file)
```

**⚠ NOT MINE — pre-existing in the working tree when I started, left untouched:**
`knowledge/gen_showroom.py`, all ~140 `showroom/*.html`, and the untracked
`knowledge/_render/gen_library_214.py` + `reviews/LIBRARY-2026-08-21-v2.html`. Another lane's.
The conductor must reconcile those separately — **do not `git add -A`.**

Scratch artefacts (`/var/tmp/mut214/*`, `knowledge/_gate_old_214_tmp.py`,
`knowledge/_ratchet_drive_tmp.py`) were created inside the sandbox and removed; `git status` is
clean of them.

---

*Opus build sub, session #214. No commits. No rulings. Both halves driven, not asserted.*
