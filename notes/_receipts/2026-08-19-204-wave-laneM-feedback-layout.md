# Receipt — #204 Lane M · Popconfirm · Footer · Grid / stack utilities

*Worker receipt, written 2026-08-19, for the BUILD-PM in the `s203-D2` PM-topology trial.*
*⛔ Nothing here is a ruling. No git command of any kind was run — no commit, no push, no `checkout/restore/stash`.*
*⛔ No generator was run, not one, not even `--check`. `_build_all.py` NOT run.*
*⛔ No existing file was edited. `knowledge/_rulings.json`, `component-types.json`, `_a11y_target.py`, `meta.schema.json`, `_validate_*.py`, `canon.css`, all `tokens/*.json`, `_DS-IMPROVEMENTS.md`, `_REVIEW-SIGNOFF.md`, `_state.py`, `gen_showroom.py`, the itinerary files, `GOOD-MORNING.md`, `_CHAIN.md`, `_LIVE-STATE.md` and the memory stores are all untouched. Nine NEW files, nothing overwritten.*

---

## Headline, before anything else

**All three rows were TRUE gaps and all three were built end to end.** No stale-premise wall.

**The lane's real yield is not the three components — it is five things the repo could not see, four of which are only visible because a component was actually built and driven.**

1. ⛔ **The token store has no destructive button seat at all.** No `button/danger/*`, `button/destructive/*`, `button/critical/*` anywhere. A destructive confirm is the canonical place a system reaches for one. Finding 1.
2. ⛔⛔ **In Apollo Legacy, the destructive glyph and the ordinary primary button are the same red — 1.03:1 apart — and the REVERSIBLE confirm looks more alarming than the destructive one.** Measured and shown, not described. Finding 2. **This is the biggest thing in the lane.**
3. ⛔ **`_validate_a11y.py` cannot express `role="alertdialog"`.** Its vocabulary carries `alert` and `dialog` and is missing their compound. The right role for a confirm-in-place therefore could not ship. Finding 3.
4. ⛔ **The snippet gate cannot resolve `tokens/spacing.json` at all** — so the one component whose entire subject is spacing is the one component that cannot bind its own values through the gate. Finding 4.
5. ★★ **"Copy the approved artefact verbatim" and "add ZERO to the shrink-only type ratchet" are in direct conflict** when the approved artefact is itself in debt. The gated `Links` atom's two `font-weight:500` declarations drove the type gate red on a specimen that copied them faithfully. Finding 5.

**And two vocabulary collisions of the `s202-D3` class, both found by building:** "footer" already means a container's action row (the gated **Action-bar** describes *itself* as *"A footer bar that pins a screen/flow's actions"*), and "grid" already means the Data-grid. Both are named in the artefacts and neither is resolved — renaming is Dave's.

---

## Step 0 — the premise table. Every claim, its probe, its verdict

⚠ **HEAD sha not quoted:** the lane brief forbids git commands outright. Declared gap, not a silent one.

| # | Claim | Probe run — command and result, verbatim | Verdict |
|---|---|---|---|
| 1 | Row 75 **Popconfirm** has no snippet or meta | `ls knowledge/snippets/ \| grep -iE "pop\|confirm\|foot\|grid\|stack\|layout\|util\|container\|column\|flex\|spac"` → `Chart-stacked-area · Confirmation · Data-grid · Form-layout · Popover` — **no Popconfirm**. Same grep over `ls knowledge/components/` → `chart-stacked-area · confirmation · data-grid · form-layout · popover` | ✅ **CONFIRMED** |
| 2 | …and no content match under any alias | `grep -ril "popconfirm" knowledge/snippets/ knowledge/components/` → **empty**. Same for `"confirm-in-place"` → **empty**; `"inline confirm"` → **empty** | ✅ **CONFIRMED** |
| 3 | Row 81 **Footer** has no snippet or meta | probe 1's grep — **no Footer** in either directory | ✅ **CONFIRMED** |
| 4 | …no doormat / mega-footer anywhere | `grep -ril "doormat" …` → **empty**; `grep -ril "mega-footer" …` → **empty** | ✅ **CONFIRMED** |
| 5 | ⚠ …but "footer" DOES appear in the corpus, 13 files | `grep -ril "footer" knowledge/snippets/ knowledge/components/` → `Drawer, Links, Data-grid, Action-bar, Command-palette` + 8 metas. Read every hit: `Drawer:16 "footer actions"` · `Data-grid:254 "footer — range read-out · rows-per-page · pagination"` · `Action-bar:8 "A footer bar that pins a screen/flow's actions"` · `Command-palette:107 "footer hint bar"` · `button.meta:127 "desktop dialog-footer convention"` | ✅ **ALL A DIFFERENT FOOTER** — the collision, see finding 6 |
| 6 | ★ `links.meta.json` already declares a Footer context | `links.meta.json:112 "Footer"` · `:215 "ref": "context:footer"` · `_nodes-context.json:339 "id": "context:footer", "label": "Footer"` | ✅ **the graph anticipated the component** |
| 7 | Row 82 **Grid / stack utilities** absent | probe 1's grep — no layout-utilities file. Content greps: `"grid utilit"` → empty · `"stack utilit"` → empty · `"layout-utilities"` → empty · `"layout util"` → empty · `"flexbox"` → empty · `"spacing scale"` → empty | ✅ **CONFIRMED** |
| 8 | ⚠ Row 82 is NOT row 51's Data-grid | Read `Data-grid.reference.html` — records, fields, `role="grid"`, sorting, selection, pagination footer. Nothing in it is a layout primitive | ✅ **the itinerary's warning is CORRECT** |
| 9 | **No ruling governs any of the three** | ⚠ **Direct grep of the store, not the index:** `grep -inE "popconfirm\|confirm-in-place\|inline confirm\|footer\|doormat\|mega.?footer\|grid utilit\|stack utilit\|layout util\|layout primitive\|utility class" knowledge/_rulings.json` → **2 hits, both unrelated**: line 143 (`_gen_chain.py` "the footer states the size of the file containing it") and line 207 (`_CHAIN.md` footer token stamp). **Neither is a component ruling.** | ✅ **NO RULING** |
| 10 | …and the search index agrees, for what it is worth | `_memento_search.py "Popconfirm"` → *"no matches"*. `"footer"` → 1 GM header + 4 ledger sections, none component. `"grid stack utilities"` / `"layout primitives"` → GM sections only | ✅ corroborating |
| 11 | ⚠ The retrieval index is STALE | Carried from the brief and consistent with probe 10's shape. **Every ruling claim above rests on the DIRECT grep of `_rulings.json` (probe 9) — the store itself, not the index** (`retrieval-default-hides-the-ruling`: store > chain) | ⚠ **declared** |
| 12 | Overlap: Popover / Confirmation / Cards / Data-grid / Eyebrow | All five READ IN FULL. Popover = informational non-modal with a close ×. Confirmation = end-of-flow success screen. Cards = the surface. Data-grid = the data table. Eyebrow = a kicker `<span>` above a heading, **no layout role, no overlap** | ✅ **no duplication** |
| 13 | The store has no destructive button seat | `grep -inE "danger\|destructive\|critical" knowledge/tokens/semantic-colour.json` → **NO OUTPUT**. Full seat list enumerated: primary · secondary · tertiary · quaternary only | ✅ **CONFIRMED ABSENT** — finding 1 |
| 14 | 13 snippets hand-roll the responsive-grid recipe | `grep -rn "repeat(auto-\(fill\|fit\), *minmax" knowledge/snippets/` → **13 files** (12 pre-existing + my Footer). Floors 180/240/300 · gaps `16px`/`20px`/`24px 32px`/`24px 16px` · max-widths 760/800/none · `auto-fill` ×11, `auto-fit` ×2 (Cards) | ✅ **MEASURED** — finding 7 |
| 15 | `target/min` is already bound by other snippets | `grep -rl "target/min" knowledge/snippets/ knowledge/components/` → 7 snippets + 4 metas (Combobox, Tags-input, Anchor-nav, Sidebar-nav, Command-palette, Multi-select, Segmented-control) | ✅ **not novel** — I bind it too, correcting nothing |

**Not one premise came back FALSE.** No pivot was needed.

---

## Deliverables — 9 NEW files, nothing overwritten, nothing edited

| File | State | Bytes |
|---|---|---|
| `knowledge/snippets/Popconfirm.reference.html` | **NEW** — PROPOSED specimen | 26,924 |
| `knowledge/snippets/Footer.reference.html` | **NEW** — PROPOSED specimen | 20,475 |
| `knowledge/snippets/Layout-utilities.reference.html` | **NEW** — PROPOSED specimen | 25,462 |
| `knowledge/components/popconfirm.meta.json` | **NEW** — schema-validated | 14,870 |
| `knowledge/components/footer.meta.json` | **NEW** — schema-validated | 13,570 |
| `knowledge/components/layout-utilities.meta.json` | **NEW** — schema-validated | 19,291 |
| `reviews/REVIEW-204-popconfirm-four-themes-v1.html` | **NEW** — 8 panes | 67,016 |
| `reviews/REVIEW-204-footer-four-themes-v1.html` | **NEW** — 8 panes | 48,395 |
| `reviews/REVIEW-204-layout-utilities-four-themes-v1.html` | **NEW** — 8 panes | 60,609 |
| `notes/_receipts/2026-08-19-204-wave-laneM-feedback-layout.md` | **NEW** — this file | — |

**Sources copied verbatim, named so a reviewer can diff them** (`specimen-starts-from-reference`):
`Popover` (bubble surface, elevation border, functional shadow, the 45°-rotated tail square and its per-side border suppression, and the whole dismiss/return-focus behaviour) · `Confirmation` (the `.btn` / `.primary` / `.ghost` pair, 96px min-width, control radius, brightness press) · `Links` (`a.lnk` underline-never-colour, combined hover/pressed, inset focus underline, `aria-current` treatment; `a.arrow` and its em-scaled tip) · `Stat-card`/`Kpi-tile` (the `auto-fill minmax(240px,1fr)` grid, then parameterised) · `Cards` (the demo block surface recipe). Icons byte-matched: `status-icons/warning-line.svg`, `global-controls/delete.svg`, `arrows-and-chevrons/arrow-up.svg`. **No parent file was touched.**

**Metas validated against `meta.schema.json` with `jsonschema`** — all three **PASS**. Three schema violations were caught and fixed on the way; two of them are findings (10, 11).

---

## Gates — every rc verbatim

| Gate | rc | Output line, verbatim | Verdict |
|---|---|---|---|
| `_validate_snippets.py` (repo-wide) | **0** | `snippet gate: 91 snippet(s), 0 failure(s)` | ✅ my three contribute 0 |
| `_validate_a11y.py` (repo-wide) | **0** | `a11y gate: 91 snippet(s), 0 failure(s), 186 warning(s), 218 note(s) · 566 controls + 203 marks measured · 107 mark(s) below 24` | ✅ |
| `_validate_type_composites.py` — my 3 files | **0** | `TYPE GATE PASS — all component text bound to canon composites (3 file(s)).` | ✅ |
| `_validate_type_composites.py` — repo-wide | 1 | `TYPE GATE FAIL — 1097 violation(s) across 90/106 file(s).  TYPE-001 ×31 · TYPE-002 ×1050 · TYPE-003 ×16` | ✅ **ratchet HELD — I added 0.** 1,097 is Lane E/K's measured #203 baseline, unchanged. `grep -c -E "Popconfirm\|Footer\.reference\|Layout-utilities"` over the failure list → **0** |
| `jsonschema` vs `meta.schema.json` | — | `popconfirm SCHEMA PASS · footer SCHEMA PASS · layout-utilities SCHEMA PASS` | ✅ |
| `_validate_state_contrast.py` | **NOT RUN — DECLARED** | a filtered run overwrites the tracked `_STATE-CONTRAST-AUDIT.md`; the lane holds no shared-file licence | ⚠ **owed to the BUILD-PM** |
| `_validate_radius.py` | **NOT RUN — DECLARED** | `MIGRATED_SNIPPETS` is a ⛔ shared registry | ⚠ conductor's |

⚠ **The filtered runs are not filtered.** Confirmed again this lane: `_validate_snippets.py <file>` and `_validate_a11y.py <file>` ignore the path argument and sweep the whole directory. **My contribution was attributed by diffing the failure list, never by trusting the filter.**
⚠ **Snippet count moved 87 → 89 → 91 mid-lane** as sibling lanes wrote. Every count here is timestamped by the probe that produced it.
**Gates left to the BUILD-PM, by name:** `_validate_state_contrast.py`, `_validate_radius.py`, `_validate_coverage.py`, `_validate_icons.py`, `_validate_dtcg.py`, `_build_integrity.py`, `_gate_doc_rows.py`, and every generator `--check`. A declared gap passes; this is the declaration.

---

## Render proof — driven, not asserted

`goto("file://…")` throughout. **`set_content()` never used.** Chromium from `/var/tmp/pw-browsers-s197`; `playwright` from `/var/tmp/pylibs-s203e`; `LD_LIBRARY_PATH` → `/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu`; `TMPDIR=/var/tmp`. Fontconfig **symlink farm** at `/var/tmp/fonts-s204m` with the `<include>` present, so markers land in the farm, not the repo. **The runbook worked verbatim, first try, no potholes hit.**

**Font asserted by CANVAS MEASUREMENT against three controls, never `fonts.check()`:**

| probe | measured |
|---|---|
| `"Univers Next for HSBC"` (snippet `--font` string) | **347** |
| `"Univers Next HSBC"` (type.css `--uf` alias) | **347** |
| `DejaVu Sans` — control | 375 |
| nonexistent face — control | 301 |

Both aliases land on the target and neither lands on the nonexistent-face number — the real HSBC cut, and the probe demonstrably discriminates. *(These are the runbook's own working-config numbers, reproduced.)*

**Results — 3 snippets × 2 modes × 2 widths, and 3 review pages × 2 widths. 0 page errors throughout.**

| artefact | panes | interactive targets | **under 44px** | doc overflow @1400 / @480 |
|---|---|---|---|---|
| `Popconfirm.reference.html` (light + dark) | — | 12 | **0** | false / false |
| `Footer.reference.html` (light + dark) | — | 24 | **0** | false / false |
| `Layout-utilities.reference.html` (light + dark) | — | **0 by design — nothing to press** | 0 | false / false |
| `REVIEW-204-popconfirm` | **8/8** | 96 | **0** | false / false |
| `REVIEW-204-footer` | **8/8** | 192 | **0** | false / false |
| `REVIEW-204-layout-utilities` | **8/8** | 0 | 0 | false / false |

**44px minimum — enforced BY HAND and PROVEN, since no gate reads the token for hit area. 324 measured targets, zero under 44.**

**All four themes fork correctly, read off the DOM in the browser** (`--text` / `--surface` / `--border-radius-control` / primary-button fill / confirm-button height, per pane):

| theme | mode | `--text` | `--surface` | control radius | primary fill | btn height |
|---|---|---|---|---|---|---|
| mono | light | `#1A1A1A` | `#FFFFFF` | `0` | `rgb(26,26,26)` | 44 |
| mono | dark | `#FFFFFF` | `#1A1A1A` | `0` | `rgb(250,250,250)` | 44 |
| legacy | light | **`#333333`** | `#FFFFFF` | `0` | **`rgb(219,0,17)`** | 44 |
| legacy | dark | `#FFFFFF` | `#1A1A1A` | `0` | **`rgb(219,0,17)`** | 44 |
| console | light | `#1A1A1A` | `#FFFFFF` | **`8px`** | `rgb(26,26,26)` | 44 |
| console | dark | `#FFFFFF` | `#1A1A1A` | **`8px`** | `rgb(250,250,250)` | 44 |
| supercharge | light | **`#13110E`** | **`#F7F6F4`** | `0` | `rgb(19,17,14)` | 44 |
| supercharge | dark | **`#F7F6F4`** | `#1A1A1A` | `0` | `rgb(240,239,237)` | 44 |

Renders viewed by eye at `outputs/s204m-renders/` — **(NON-REPO: session outputs folder)**, `s191-D2` marker. HTML is what Dave reviews; PNGs are my verification.
Repo pollution check after the fact: `ls -a knowledge/assets/fonts/_desktop/TTF/ | grep -c '^\.uuid'` → **0**; `find . \( -name '.uuid*' -o -name '*.LCK' -o -name '*.cache-*' \) -not -path './_to_delete/*'` → **empty**.

### ★ Four defects the gates could not see, caught only by looking

Every one of these passed **all three gates green** before and after. This is `green-tests-cannot-see-scope`, four times in one lane.

1. ⛔⛔ **The review-page builder emitted SELF-REFERENCING custom properties, and they fail silently.** Where a snippet's var name already IS canon.css's own name for that token (`--target-min` ← `target/min`, `--border-radius-surface` ← `border-radius/surface`), the builder wrote `--target-min: var(--target-min);` — a guaranteed-invalid-at-computed-value-time declaration. The property resolves to the **empty string**, and every consumer collapses. **Measured symptom: 96 of 96 targets rendering at 16–32px instead of 44, and the console theme's radius reading `""` instead of `8px`.** No gate can see this: the snippet is correct, the review page is not generator output, and nothing parses either for var self-reference. Caught by *measuring in the browser*, not by looking — the page still looked broadly plausible. Fixed by inheriting such vars from canon.css instead of re-binding them, and the fix is commented in place.
2. **Descenders clipped in the payee row** (`text-box-edge: cap alphabetic` + `overflow:hidden` cut the tail of the *p* in "Meridian Supplies"). **The identical defect Lane K hit at #203, in a different component, from the same cause** — the leading-trim `:is()` rule meets a clipping container. Re-measured after the fix: `clientHeight == scrollHeight == 18`, `text-box-edge: text`. ⇒ **This is now n=2 and it is a CLASS, not an incident** — proposed as a gate candidate below.
3. **The confirm button cropped its own label.** Confirmation's atom writes `height:44px`, which is right for its one-word labels; a Popconfirm's confirm label *repeats the verb* ("Delete standing order") and wraps to two lines inside a fixed 44px box. Copying the parent verbatim was the defect. Changed to `min-height` + vertical padding — the ruled floor is kept and the divergence from the parent is declared in the file.
4. **The open bubbles covered the demo notes beneath them.** Absolutely-positioned overlays over too-short spacer wrappers. Fixed, and then **asserted numerically** rather than eyeballed: a bounding-box intersection probe of every `.pc.is-open` against every `.demo-h`/`.demo-note` → **`OVERLAPS: none`**.

The builder is a **throwaway at `/var/tmp/s204m/`, outside the repo** (the #174 / Lane E / Lane K precedent). It is **not** an instrument the repo carries. `machinery: 0 instrument / ~200 feature`.

---

## The components — how each differs from its nearest gated neighbour

### Row 75 — Popconfirm

**A Popover ANSWERS; a Popconfirm ASKS.** It borrows Popover's chrome byte-for-byte and refuses its close ×, because here **dismissal IS the cancel** and a × beside a Cancel button offers one outcome under two labels. *The tell: if dismissing the thing has no consequence, it is a Popover.*
It is **not a Modal** — no scrim, no trap, and the row being changed stays visible behind it. That is what "confirm in place" means, and it is the itinerary's own wording.
It is **not Confirmation** — that reports an outcome *after*; this asks *before*. Opposite ends of one event, sharing only the button pair.
Three specimens: default (reversible), destructive (glyph in the error ink), and an icon trigger inside a list row. Two open by default so every review pane shows the thing open; two closed and driveable.

### Row 81 — Footer

**Links owns the ATOM; Footer is the REGION.** Links even ships `.related`, which its own source calls *"the footer / utility pattern"*. *The tell: strip the landmark and the group headings from a Footer and what is left is a `.related` list, and it should be one.*
Four named `<nav>` groups rather than one anonymous list of forty links. Two forms: doormat and slim.
**vs Action-bar** — the collision, finding 6. Action-bar pins the ACTIONS of a flow and belongs to the task; Footer is the end of the DOCUMENT and belongs to the site. They can sit on one screen.
**vs Headers** — a header carries wayfinding a reader is about to use; a footer carries what they went looking for and what the regulator requires.

### Row 82 — Grid / stack utilities

**Not the Data-grid.** *The tell: a Data-grid's columns MEAN something — they are fields. A layout grid's columns mean NOTHING — they are space.*
Seven primitives: container · stack · row · grid · twelve-column · split · measure. They paint nothing, size no type, carry no role.
**vs Cards** — Cards owns the surface and hand-rolls a grid to sit several side by side. *A Card without a grid is still a Card; a grid without anything in it is nothing at all.*
**vs Form-layout** — layout WITH semantics, versus layout with none.
The `.l-split` specimen appears twice with identical markup and the second copy has already collapsed inside a 420px frame on a 1400px screen — **the case that decides container-query vs viewport-query, shown rather than argued.**

---

## Findings

### ⛔⛔ Finding 1 — the token store has no destructive button seat

`grep -inE "danger|destructive|critical" knowledge/tokens/semantic-colour.json` → **no output**. Every button seat is primary / secondary / tertiary / quaternary. A destructive confirm is the canonical place a design system reaches for a danger button and **this system does not have one.**
The specimen **invents none.** The destructive variant carries its weight three ways that already exist: the warning glyph in `rag/error-ink` (s151-D1's own values, MONO ONLY), the **verb** in the confirm label ("Delete standing order", never "OK"), and the question. Measured on the bubble surface with the repo's own `_contrast_utils.contrast_ratio`: **5.090 light, 5.550 dark**, both clear of the 3:1 non-text floor in all four themes (supercharge light is the tightest at 4.710 on `#F7F6F4`).
⛔ **Whether a destructive seat should exist is Dave's.** It touches `s151-D1` (two-red law) and `s149-D1` (mono error ink camp), both FIRM, and neither is touched here: nothing in this component paints text on an error fill, so the ink camp does not arise.

### ⛔⛔ Finding 2 — in Apollo Legacy the danger red and the primary red are the same red, and the reversible confirm looks more alarming than the destructive one

**This is the finding of the lane, and it is only visible because the thing was built and driven.**

`rag/error-ink` is **theme-invariant** — measured off the DOM, the destructive glyph computes to `rgb(218,26,0)` = **`#DA1A00`** in light and `rgb(246,96,76)` = **`#F6604C`** in dark, **identically in all four themes**. Meanwhile `button/primary/background/default` **forks per theme**, and in Legacy it is HSBC red **`#DB0011`** in *both* modes.

⇒ In Apollo Legacy, the destructive bubble puts a **`#DA1A00`** warning glyph beside a **`#DB0011`** primary button. **Contrast ratio between the two reds: `1.03:1`.** They are, to the eye, the same colour, carrying two different meanings — *"danger, read this"* and *"this is the primary action"* — eight centimetres apart in the same bubble.

**And it is worse than a clash.** In Legacy the *ordinary, reversible* "Remove payee" confirm also gets a large red primary button, while the *destructive* one gets the same red button plus a small red glyph. **The reversible action reads as more alarming than the irreversible one.** Look at `outputs/s204m-renders/crop-popconfirm-legacy.png` — both panes, side by side.

⛔ **NOT RESOLVED, and not resolvable by a worker.** Rebinding a ruled colour seat is Dave's; `surface, never swap` binds. It is a cousin of Lane K's #203 arrow-seat finding — *a theme-invariant RAG ink meeting a theme-forking brand colour* — and the two should be answered together, not separately. Dave is astigmatic and red is a problem hue, which is exactly why this is being surfaced rather than absorbed.

### ⛔ Finding 3 — `_validate_a11y.py` cannot express `role="alertdialog"`, so the right role could not ship

Built with `role="alertdialog"` first. The gate went **red**, verbatim:
> `FAIL Popconfirm: CTRL vocabulary: unknown ARIA role(s) ['alertdialog'] — this gate cannot classify them as interactive or structural, so it cannot tell whether the elements carrying them are in scope for 2.5.8. Add each to INTERACTIVE_ROLES or NON_INTERACTIVE_ROLES in _a11y_target.py before shipping (dv-vocab shape: fail loud, never let an unknown default to skip).`

**The gate's behaviour is correct — it fails loud rather than defaulting to skip, which is exactly right.** The vocabulary is the problem: `_a11y_target.py:74–81` `NON_INTERACTIVE_ROLES` already contains **both** `"alert"` and `"dialog"` and is simply missing their compound.
`_a11y_target.py` is a shared gate outside this lane's fence and **was NOT edited**. The snippet fell back to `role="dialog"` (the gated Popover's own role) so the tree stays green. ⚠ **A green a11y gate on this file is measuring `dialog`, not endorsing it** — that sentence is written into the snippet header, the meta and the review page so nobody downstream reads the green as a verdict on the role. One-line merge proposed below.

### ⛔ Finding 4 — the snippet gate cannot resolve the spacing scale, and the layout primitive is where that bites

`_validate_snippets.resolve()` loads `semantic-colour`, `layout`, `motion`, `opacity` and `component-types` **only**. `tokens/spacing.json` is not in its namespace list. So declaring `--l-gap-s: gap/fixed/content/small` in a manifest fails with *"token not found in store"*.
**The one component whose entire subject is spacing is the one component that cannot bind its own values through the gate.** The gap ramp (`gap/fixed/content/{2,4,8,12}`, `gap/fixed/subsection/{24,32,40,48}`, `gap/fixed/section/{48…120}`, `padding/fixed/{12,16,20,24}`) is therefore written as literals, each carrying its token path in a comment, and the manifest declares only what the gate can actually check. **Not patched here.**

★ **A second, sharper half that is NOT a repo defect and cannot be fixed:** `@media` and `@container` conditions **cannot consume custom properties at all** — a CSS language fact. So `breakpoint/s|ms|m` can never be bound in any snippet, ever. Those values are literal with token paths in comments, and are **deliberately NOT declared** in the manifest, because declaring a var the component does not consume would be a green assertion about nothing.

⚠ **And a third, quieter one:** `layout/web/columns` = `12` **cannot** be bound either, because `resolve()` sends every `layout/*` path through `px_number`, so it resolves to the string `"12px"` — a manifest binding would demand that literal in the CSS. The track count is written `repeat(12, …)` with the token path in a comment.

### ★★ Finding 5 — "copy the approved artefact" and "add zero to the ratchet" are in direct conflict

The gated `Links` atom writes `font-weight:500` **twice** in its own CSS — on `a.arrow` and on `a.lnk[aria-current="page"]`. Those are exactly the raw declarations `TYPE-002` counts, and Links carries that debt today.
**Copying them verbatim, as the specimen law requires, drove `_validate_type_composites.py` RED on my file — measured, 2 violations.** The two laws collided head-on.
Resolved by taking the emphasis through canon/type.css's own `.t-ed-body-small .em` modifier applied in the **markup** (the T-D14 markup-class route): identical rendered weight, zero added debt. **Links itself was NOT edited** — it is a gated shared artefact and its two declarations are the BUILD-PM's to retire.
⚠ **This will recur every time a specimen copies from a parent that is in the 1,097.** 90 of 106 files carry debt, so the odds are high. Worth a line in the specimen law: *copy the artefact, but take type through the composite even where the parent does not.*

### ★★ Finding 6 — two vocabulary collisions, both the `s202-D3` class, both found by building

- **"footer"** already means a container's action row. The gated **Action-bar** describes *itself*, verbatim, as *"A footer bar that pins a screen/flow's actions"*. Drawer, Modals, Data-grid and Command-palette all use the word the same way. A site Footer and an Action-bar can appear on one screen and are not variants.
- **"grid"** already means the Data-grid. The itinerary's own warning is correct and the slug/prefix (`layout-utilities` / `.l-`) avoids claiming the word — but **avoiding a word is not the same as deciding one.**

⛔ **Neither is renamed.** `s202-D3`'s lesson is that a collision left unnamed produces a rejected build with every assertion green; both are named in the snippet header, the meta and the review page.
★ **A third collision was avoided by NOT building something.** The classic name for the "side by side until they run out of room, then stacked" primitive is a **switcher** — and `s202-D3` rules "switch" to mean the THUMB of a toggle. The primitive is **deliberately not built** and the omission is declared rather than silently renamed on my own authority.

### ★ Finding 7 — the responsive-grid recipe is hand-rolled in 13 snippets and they disagree behaviourally

`grep -rn "repeat(auto-\(fill\|fit\), *minmax" knowledge/snippets/` → **13 files**.
- **floors:** 180px · 240px (Stat-card, Kpi-tile) · 300px (ten files)
- **gaps:** `16px` · `20px` (Cards ×2) · `24px 32px` (nine form-family files) · `24px 16px`
- **max-widths:** 760px (form family) · 800px (Stat-card, Kpi-tile) · none (Cards)
- **keyword:** `auto-fill` ×11 vs **`auto-fit` ×2 (Cards)** — ⚠ **a real behavioural difference, not a stylistic one.** `auto-fit` collapses empty tracks and stretches the survivors; `auto-fill` keeps them. **Two snippets behave differently from the other eleven and nothing in the repo records that as a decision.**

Also observed: several of the hand-rolled copies use a bare `minmax(300px, 1fr)` with no `min(…, 100%)` wrapper, which **forces a horizontal scrollbar in a container narrower than 300px.** My `.l-grid` wraps it. That is a latent reflow bug in gated files; **not fixed here** (13 shared artefacts), reported.
⛔ **Nothing is reconciled.** Picking one floor, one gap and one keyword is a ruling.

### ⚠ Finding 8 — the 44px minimum has a visible design cost, and someone should decide to pay it

Every footer link here is a ≥44px target at **every** width, not only when stacked. The gated `Links` `.related` pattern grows targets only at ≤420px. Deciding it once makes a four-column doormat **measurably taller** than the compact typographic ideal a footer usually reaches for. That is a design trade, not a technicality, and it is shown in every pane. Dave's.

### ⚠ Finding 9 — `_validate_a11y.py` reports 107 marks below 24 and 186 warnings repo-wide, and none of them block

Recorded as an observation with its probe, not a claim about ownership. If a mark-size floor is ever ruled, that number is the standing debt it would inherit.

### ⚠ Finding 10 — `meta.schema.json`'s `category` enum has no rung for a layout primitive

`layout-utilities.meta.json` was written with `"category": "primitive"` and the schema rejected it, verbatim: `'primitive' is not one of ['atom','molecule','organism','template','page']`. The enum is the atomic-design ladder, and a layout primitive is **not a thing on the page at all** — it is the space between things. Shipped as `"atom"` (the nearest legal rung) with the divergence declared in a `$categoryNote`. `meta.schema.json` is a shared file and was **NOT edited**.

### ⚠ Finding 11 — `meta.schema.json`'s `stateModel` enum has no rung for "stateless"

Same shape. `stateModel` accepts only `simple` and `full`. A layout primitive has **no** default/hover/focus/pressed state because there is nothing to press; a Popconfirm's real model is *open/closed with return-focus*, which is neither. Both shipped at the nearest legal value with a `$stateModelNote`. **Two enum gaps found by one lane writing three metas** suggests the schema's vocabulary has not been exercised outside the component ladder.

---

## Decisions needed — Dave's, every one PROPOSED #204

Grouped so they can be answered in one sitting. **Nothing below was resolved here. Nothing a sub writes is a ruling.**

**The red one, first:**
1. **The Legacy two-red collision (finding 2).** The destructive glyph (`#DA1A00`, theme-invariant) and the Legacy primary button (`#DB0011`, theme-forking) are `1.03:1` apart in the same bubble, and the reversible confirm reads as more alarming than the destructive one. Rebind, re-tone the destructive treatment, or accept? **This and Lane K's #203 arrow-seat finding are the same species and should move together.**
2. **Should a destructive button seat exist at all (finding 1)?** The store has none. The specimen works without one. Adding one touches `s151-D1` and `s149-D1`, both FIRM.

**Popconfirm:**
3. **Which actions may use a confirm-in-place?** Fintech semantics are yours. Right for removing a payee; probably wrong for sending money. Where is the line, and should the meta state it as a hard rule rather than guidance?
4. **Does a destructive confirm trap focus?** This inherits Popover's non-modal reading — no trap, leaving closes. The other reading is that a decision the page is waiting on should hold focus until it is made.
5. **`alertdialog` or `dialog` (finding 3)?** The gate cannot currently express the former.
6. **Placement:** reuse Popover's space-aware placer (one mechanism, two components) or keep the simpler anchored form?
7. **Cancel left of confirm**, and **is "Popconfirm" the name**?

**Footer:**
8. **The name (finding 6).** "Footer" already means a container's action row, and Action-bar uses the word about itself.
9. **The 44px trade (finding 8).** Accept the extra height everywhere, or grow targets only when stacked as `Links` does?
10. **The band colour.** The footer sits on `surface/subtle` — in Mono light that is `#F0F0F0` on a `#FFFFFF` page, a very quiet distinction. Band, or let the section rule carry the whole separation?
11. **Two forms or two components?** Doormat and slim share a landmark, a legal row and a link atom, and nothing else.
12. **What belongs in the legal bar.** Regulatory, varies by market, not mine to fix.
13. **Back-to-top on by default?**

**Layout utilities:**
14. **The name (finding 6).** `.l-` avoids claiming "grid"; avoidance is not a decision.
15. **One floor, one gap, one keyword (finding 7).** This is what turns a specimen into a primitive.
16. **Should the thirteen migrate?** If they do, thirteen gated snippets change and each needs re-gating. If they do not, this is documentation rather than machinery.
17. **The gap ramp's shape** — seven steps drawn from two token ramps that *meet* at 48px. Seven, or fewer?
18. **Container queries or viewport queries, as a system rule.** The `.l-split` specimen is the case that decides it.
19. **The missing "switcher"** — wanted, and under what name?
20. **Is 64ch the measure?** It already appears by hand in several snippets.

---

## Proposals for the BUILD-PM to merge — exact text, no shared file edited

**`knowledge/_a11y_target.py` — one line, finding 3.** In `NON_INTERACTIVE_ROLES` (currently lines 74–81), add `"alertdialog"` beside the `"alert"` and `"dialog"` it already contains:
```python
NON_INTERACTIVE_ROLES = {
    "alert", "alertdialog", "dialog", "grid", "group", "img", "list", "listbox", "listitem",
```
Then `Popconfirm.reference.html` may take `role="alertdialog"` (4 occurrences of `role="dialog"`), and the `requiredAria` entry `"role=\"dialog\""` becomes `"role=\"alertdialog\""`. ⛔ **The role is still Dave's call (decision 5) — this merge only makes it EXPRESSIBLE.**

**`_DS-IMPROVEMENTS.md`** — *"`_validate_snippets.resolve()` cannot reach `tokens/spacing.json`: it loads semantic-colour, layout, motion, opacity and component-types only. A component cannot bind its gap or padding through its manifest, so the whole spacing ramp is invisible to the drift gate. Proven at #204 by the layout-primitive component, whose entire subject is spacing. Candidate fix: add a `spacing.json` branch to `resolve()` alongside the existing `layout/` branch, returning a CSS length."*

**`_DS-IMPROVEMENTS.md`** — *"A custom property bound to ITSELF (`--target-min: var(--target-min)`) is guaranteed-invalid-at-computed-value-time: it resolves to the empty string and every consumer collapses, silently. Reproduced at #204 in a review-page builder, where it took 96 ruled 44px targets down to 16–32px with all three gates green. Any generator or builder that maps a manifest var to a canon custom property must skip the case where the two names are equal and inherit instead. `gen_canon_components.py` should be checked for the same shape."*

**`_DS-IMPROVEMENTS.md`** — *"`text-box-edge: cap alphabetic` (the leading-trim rule inlined in every snippet) CLIPS DESCENDERS inside any container with `overflow:hidden`. Hit at #203 (Lane K, Timeline titles) and independently again at #204 (Lane M, Popconfirm payee rows) — n=2, so it is a class, not an incident. Candidate gate: flag any rule combining `overflow:hidden` with a text element inheriting the trim rule and no `text-box-edge:text` override."*

**`_DS-IMPROVEMENTS.md`** — *"The specimen law ('copy the approved artefact verbatim') and the shrink-only type ratchet ('add zero') CONFLICT when the parent carries TYPE-002 debt. Proven at #204: copying `Links`'s two `font-weight:500` declarations faithfully drove the type gate red on a new file. 90 of 106 files carry debt, so this will recur. Amend the specimen law: copy the artefact, but take type through the composite even where the parent does not."*

**`_DS-IMPROVEMENTS.md`** — reinforcing Lane K and Lane E: *"`_validate_snippets.py <file>` and `_validate_a11y.py <file>` still ignore the path argument and sweep the whole snippets directory (re-confirmed #204). Either honour the filter or drop the argument."*

**`_DS-IMPROVEMENTS.md`** — *"Several gated snippets write `minmax(300px, 1fr)` with no `min(…, 100%)` wrapper, which forces a horizontal scrollbar in any container narrower than 300px (SC 1.4.10). Enumerated #204: Time-picker, Form-layout, File-upload, Secure-entry, Textarea, Date-range-picker, Amount-input, Input-fields, Date-picker, Cards. Not fixed at #204 — thirteen shared artefacts."*

**`knowledge/components/meta.schema.json` — findings 10 and 11, TWO enum gaps.** `category` has no rung for a LAYOUT PRIMITIVE (shipped as `atom` with a `$categoryNote`); `stateModel` has no rung for STATELESS or for open/closed-with-return-focus (shipped at the nearest legal value with a `$stateModelNote`). ⛔ **Both are vocabulary decisions, so they are Dave's, not a merge chore** — flagged, not requested.

**`component-types.json`** — none of the three is registered, so none takes an `AUTO-BEHAVIOUR` or press-physics partial. **Popconfirm's pressables therefore carry colour-only states — the same declared state the gated Popover shipped in.** Registration is a promotion decision and therefore Dave's. Flagged, not requested.

**`gen_canon_components.py` / `canon.css`** — the three components are absent from `canon.css`. The review pages hand-mirror the `.cn-<slug>` scope, and ★ **unlike the #203 pages they bind to canon.css's OWN custom properties (`var(--text-default)`) rather than re-typing resolved per-theme values**, so the four-theme cascade is canon.css's and cannot drift from it. Once the BUILD-PM regenerates, the authoritative scopes should replace the mirrors.

**`_validate_radius.py` `MIGRATED_SNIPPETS`** — three new snippets absent from the radius ratchet (⛔ shared file). Console's 8px control radius was verified present in the render.

**`CATEGORIES` / `gen_showroom.py`** — three new slugs (`popconfirm`, `footer`, `layout-utilities`) have no showroom entry. ⛔ shared file; **and none should be added before Dave rules the two naming questions.**

**`_gate_doc_rows.py` / the doc-row store** — three new snippets, three new metas and three new review pages exist with no store row. Per the `forgotten-document-class` rule (#185), new docs get a store row at creation. **The store is a shared surface and Lane M holds no licence** — declared and handed over, and the BUILD-PM should run the doc-row gate before committing.

**Itinerary rows 75, 81, 82** — all three genuinely `Gap`; the Status column is **correct** for these three. Same signal Lane K gave: the rot is not uniform, so a derived status must probe per row.

**No new token is wanted.** Every value used already exists and is already ruled. Two are *proposed* and both are Dave's: a destructive button seat (finding 1) and whatever finding 2's resolution needs.

---

## Friction log

- **The runbook worked verbatim, first try.** No ENOSPC, no missing lib, no font fallback. `/var/tmp` farms from #197 and #203 were reusable read-only exactly as the runbook says. **This is the first render pass in several sessions that hit no pothole at all** — worth recording, because the runbook's value is invisible when it works.
- **My own builder introduced the single worst defect in the lane** (self-referencing custom properties), and it was **invisible to every gate and nearly invisible to the eye** — the page looked plausible with 44px targets rendering at 18px. It was caught by *measuring*, not by looking. A page-builder is an artefact that needs its own verification, not a transparent pipe. Third lane running to learn this.
- **Three schema violations, three enum gaps.** Writing metas that describe things the schema's vocabulary was not built for surfaced two real gaps in one sitting. Cheap, and only possible because the schema is actually validated rather than assumed.
- **The two-red finding required BUILDING the thing.** No amount of reading `_rulings.json` would have produced it: it needs a destructive component, in Legacy, in a browser, with both reds on screen at once. `mutation-tests-the-clause-not-the-feature` — drive the thing.
- **A gate that fails loud on unknown vocabulary is worth its inconvenience.** `_validate_a11y.py` cost me a round-trip and a design compromise, and it was **right** — it refused to silently skip a role it could not classify. Recording the cost so it is not mistaken for a complaint.
- **Concurrency is visible:** snippet count moved 87 → 89 → 91 mid-lane, and `reviews/` gained sibling lanes' `REVIEW-204-*` files while I worked.

---

## Residuals — declared, not glossed

- **`_validate_state_contrast.py` NOT run.** A filtered run overwrites the tracked `_STATE-CONTRAST-AUDIT.md`; the lane holds no shared-file licence. **It is the gate that would adjudicate finding 2's rendering leg, and it is owed** — BUILD-PM or CI.
- **HEAD sha not captured** — the lane brief's ⛔ on git commands overrides the base brief's §3.
- **The three components are absent from `canon.css`, the radius ratchet, the showroom, `component-types.json` and the doc-row store.** All five are shared surfaces. The review pages' `.cn-` scopes are hand-mirrors — faithful to each manifest and cascade-correct, but **not generator output.** That is the fence working, declared not silent.
- **Popconfirm's space-aware placement is NOT built.** Popover owns that mechanism; this anchors in flow so the open state renders statically. A production Popconfirm should reuse Popover's placer. **Declared in the snippet, the meta and the review page.**
- **Popconfirm's confirm and cancel buttons both simply close.** What a real product would then DO is composition-level, and inventing it would be canon by improvisation. The buttons are real, focusable affordances with no destination — declared, not hidden.
- **Below 480px is unexamined and is not claimed.** Verified at 1400 and 480 only.
- **`_validate_dataviz.py` not run** — no dataviz geometry exists in any of the three files.
- **The 13 hand-rolled grid recipes were NOT migrated and the missing `min()` wrappers were NOT fixed.** Thirteen shared artefacts; reported, not touched.
- **The `Links` atom's two `font-weight:500` declarations were NOT retired.** Gated shared artefact; the divergence is declared in my file instead.
- **`outputs/s204m-renders/` holds 15 PNGs** — **(NON-REPO: session outputs folder)**, `s191-D2` marker.
- **Throwaway builder at `/var/tmp/s204m/`** — outside the repo, not carried, not an instrument.

---

## ⛔ CONSEQUENCES / PITFALLS — what a verifier should attack first (Dave #165)

**What I did NOT run:** `_validate_state_contrast.py` · `_validate_radius.py` · `_validate_coverage.py` · `_validate_icons.py` · `_validate_dtcg.py` · `_build_integrity.py` · `_gate_doc_rows.py` · `_validate_dataviz.py` · every generator, including `--check` · `_build_all.py` · any git command. **A declared gap passes; this is the declaration.**

**What a green gate here CANNOT see:**
1. **That `role="dialog"` is the wrong role.** The a11y gate is green because it is measuring `dialog`. It has no opinion about whether that is right, and finding 3 is the reason the green is not a verdict.
2. **The self-referencing-var class.** No gate parses a review page at all, and none parses a snippet for var self-reference. A `--x: var(--x)` anywhere in the tree is currently undetectable and silently collapses everything downstream of it. **Attack this first** — check `gen_canon_components.py` for the same shape, because it does exactly this mapping for every gated component.
3. **Hit area.** No gate reads `target/min` for target SIZE. All 324 measurements in this receipt are hand-driven and would vanish the moment someone edits a padding value. The `_validate_snippets` binding proves the *token value* has not drifted; it proves nothing about geometry.
4. **The two-red collision (finding 2).** Every declared contrast pair passes. The collision is between two values that each pass independently and that no manifest declares as a *pair* — because they are not foreground and background, they are two neighbours. **No gate in this repo compares adjacent meanings.**
5. **Descender clipping.** Passed all gates in two lanes running.
6. **Whether the components are the right components at all.** Naming, scope and the permitted action class are Dave's and no gate has an opinion.

**Where I would attack this work if I were verifying it:**
- **Re-drive the review pages and re-measure every target.** The self-referencing-var bug proves the pages can look right and measure wrong. Do not trust my numbers — re-run them.
- **Open `crop-popconfirm-legacy.png` and decide whether finding 2 is real** before touching anything else. If it is, it is bigger than this lane.
- **Test the Popconfirm's dismissal by keyboard**, not by reading the script. Esc, Tab out, Shift+Tab back, and the toggle path. I drove the geometry; I did **not** drive the focus sequence with a real keyboard, and that is an honest gap.
- **Check the `@container` queries actually fire.** Footer's 560px and `.l-split`'s 760px collapses were verified visually and by layout measurement at two widths, not by a boundary sweep. A container query that never matches looks identical to one that matches everywhere until you hit the boundary.
- **Confirm the metas' `$`-annotations survive whatever consumes them.** I validated against the schema; I did not run whatever *reads* these files.
- **Assume the itinerary rows are right and my greps are wrong** before assuming the reverse. Probes 1–8 are filename and content greps, and `unmatched-grep-is-not-an-absence` cuts both ways: I named every probe and quoted every result so they can be re-run, which is the only defence I have.

---

**Context gauge at close — `knowledge/_checkin.py`, run live:** MEASURED **136,525 real** (headline, throughput) · **FILL 120,690 real** · boot 56,589 real · peak 120,690 over 28 turns · room to the advisory stop line (150,929) 30,239 · `✅ SEAM CLEAR`.
⚠ **Declared, not glossed:** `_checkin.py` reads the *session* transcript, which this wave shares with the BUILD-PM and sibling lanes. **That figure is session-wide, not this lane's isolated spend** — a sub's own window is not separately instrumented, and I am not converting it into a per-lane number (`measure-dont-convert-units`).
