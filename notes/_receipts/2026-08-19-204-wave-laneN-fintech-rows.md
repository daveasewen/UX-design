# Receipt — #204 Lane N · fintech rows (Transaction / ledger row · Statement / document row)

*Worker receipt, written 2026-08-19, under the BUILD-PM in the `s203-D2` PM-topology trial.*
*⛔ Nothing here is a ruling. No git command of any kind was run — no commit, no push, no `checkout/restore/stash`.*
*⛔ No generator was run, not one, not even `--check`. `_build_all.py` not run.*
*⛔ No existing file was edited. `knowledge/_rulings.json`, `component-types.json`, all `tokens/*.json`, `canon.css`, `_DS-IMPROVEMENTS.md`, `_REVIEW-SIGNOFF.md`, `_validate_radius.py`, `gen_showroom.py`, `knowledge/_state.py`, the itinerary files, `GOOD-MORNING.md`, `_CHAIN.md`, `_LIVE-STATE.md` and the memory stores — all untouched. Three NEW files only.*

**Context gauge at close — `knowledge/_checkin.py`, run live:** MEASURED **136,525 real** (headline,
throughput) · **FILL 120,690 real** · boot 56,589 real · peak 120,690 across 28 turns.
⚠ **Declared, not glossed:** `_checkin.py` reads the *session* transcript, shared with sibling lanes and
the BUILD-PM. That figure is **session-wide, not this lane's isolated spend**; a sub's own window is not
separately instrumented and I am not converting it into a per-lane number (`measure-dont-convert-units`).
It also self-reports **STALE by 18 min**.

---

## Headline for the BUILD-PM, before anything else

### ★★★ The List-items overlap adjudication — the central question of this lane, answered

**Row 91 "Transaction / ledger row" IS A DUPLICATE. It is not a gap, and it is not a "composition of
gated parts" either — it is a BUILT, GATED, DAVE-PROMOTED COMPONENT that has existed since 2026-06-22.
I built no transaction row.** This is the Sidebar-nav-vs-Navigations class, and it is not a close call.

Three independent pieces of evidence, all verbatim from the repo:

1. `knowledge/components/list-items.meta.json`, `build.$status`:
   *"PROMOTED 2026-06-22 (Dave) — **TRANSACTION row** brought to the Tabs-bar standard. Gated reference:
   snippets/List-items.reference.html (replaces the earlier generic account-row reference). Build green."*
2. Same file, `build.scope`: *"**Transaction row only** (the ★ payments-journey row). The other types
   (account/badge/item/review/review-detail/bullets) stay documented in `variants`/`tokenValidation` but
   are not yet refined to standard."* — and `build.prototypeGrade`: *"9.0/9 (2026-06-22) — joined Tabs at
   full marks."*
3. `knowledge/snippets/List-items.reference.html`, its `<title>` element, verbatim:
   *"List items — **Transaction row** (reference implementation, gated)"*, with `build.anatomy`
   *"leading avatar + title/description + trailing detail (tag chip OR status badge) above a
   right-aligned amount. Figma node 1508:76284."*

The itinerary's own note for row 91 is *"Statement/ledger line item."* That is the anatomy above,
exactly. **The `drift = OVERSTATED` flag on this row is pointing the wrong way: the itinerary is not
claiming more than the store holds, it is claiming a GAP the store CLOSED two months ago.** The Status
column reading "Partial" is wrong in the other direction too — the store holds a 9.0/9 promoted build.

⚠ **The five artefact probes were all NEGATIVE and all five were RIGHT — and that is the lesson.**
There is no `transaction-row` snippet and no `transaction-row.meta.json`, because the row does not live
under its own slug; it lives as the promoted `type` of `list-items`. **A slug-shaped probe cannot see a
component that ships as a variant of another component.** Any derived-status instrument that probes by
slug will manufacture this same false gap for every variant-shipped row in the library. Flagged for the
BUILD-PM as a class, not a one-off.

★ **The one genuinely open thing row 91 leaves behind** (a finding, not a build): the gated transaction
row renders its amounts as raw text — `−1,234.00 HKD`, `+32,000.00 HKD` — **currency code AFTER the
value, with a space**. That is `amount-display.meta.json`'s own antiPattern #1 verbatim (*"Putting a
space between the currency symbol/code and the amount (copy-025 — a space risks the amount wrapping to
a different line)"*) and its `copy-025` rule requires the symbol/code BEFORE with no space. **The row
does not compose the Amount-display atom at all.** So the "gap" that `amount-display.meta.json` names
in its `relationships.livesInside` as *"Transaction / ledger row (gap)"* is **not** "no transaction row
exists" — it is **"the gated transaction row does not use me, and contradicts my copy rule."**
That is a real, small, high-value repair on a gated file, and it is the BUILD-PM's or Dave's, not mine.

### Row 92 "Statement / document row" IS a genuine gap — and it was built

Not because the itinerary says so, but because the difference from List-items is **structural and
demonstrable**, and I drove a browser to prove it. See "the structural assertion" below.

⚠ **And the honest converse is shipped alongside it.** The SINGLE-ACTION form of a document row *is*
structurally a List-items row. It is drawn in the specimen as **variant B** precisely so Dave can rule
by eye. **If he rules that the product needs only the single-action form, this component should not
exist and row 92 collapses into List-items exactly as row 91 did.** That is a live outcome, stated in
the snippet header, the meta and the review page — not a hedge.

---

## Step 0 — the premise table, verified first-hand

⚠ **HEAD sha not quoted: the lane brief forbids git commands outright.** Declared gap, not a silent one.

| # | Claim (from the brief / the ITINERARY-STATUS JSON) | Probe run, quoted | Verdict |
|---|---|---|---|
| 1 | Row 91 `transaction-row`: all five artefact probes NEGATIVE | `ls knowledge/snippets/ \| grep -i <k>` and `ls knowledge/components/ \| grep -i <k>` for **k ∈ {transaction, ledger, statement, document, download, line-item, lineitem, entry, posting, receipt, invoice, attach, file}** → **empty for every key** except `entry`→`Secure-entry`, `file`→`File-upload` (both unrelated) | ✅ **CONFIRMED** — but see #3 |
| 2 | Row 92 `document-row`: all five artefact probes NEGATIVE | same sweep, same output | ✅ **CONFIRMED** |
| 3 | Row 91 status "Partial", `drift = OVERSTATED — itinerary claims more than the store holds` | `list-items.meta.json` `build.$status` = *"PROMOTED 2026-06-22 (Dave) — TRANSACTION row brought to the Tabs-bar standard"*; `build.scope` = *"Transaction row only"*; `build.prototypeGrade` = *"9.0/9"*; `List-items.reference.html` `<title>` = *"List items — Transaction row (reference implementation, gated)"* | ⛔ **FALSE — and false in the OPPOSITE DIRECTION.** Not "Partial" and not "overstated": the store holds a **complete, promoted, 9.0/9 gated build**. Row 91 is a **Duplicate**. **STOPPED on this component, per the brief.** |
| 4 | Row 92 status "Partial", same drift flag | Content grep below found no document/statement ROW component anywhere | ✅ the row is a genuine **Gap**; "Partial" is still not supported, but the direction is harmless |
| 5 | `list-items.meta.json` covers the tappable list-row family incl. "Transaction" | `purpose`, verbatim: *"Covers the tappable list-row family (Account, Badge, Item, Review, Review Detail, **Transaction**) plus typeset bullet/ordered/custom lists."* Plus `props.type.values` contains `"transaction"` and `variants` contains `{"name":"transaction","use":"Transaction row with tag or status detail…"}` | ✅ **CONFIRMED** |
| 6 | `amount-display.meta.json` names row 91's own gap verbatim | `relationships.livesInside` = `[… "List-items", **"Transaction / ledger row (gap)"**, "KPI / trend tile (gap)"]`; `edges.usedInContext` = `{"ref":"context:transaction-ledger-row-gap"}` | ✅ **CONFIRMED — and it means something different from what it looks like.** See the headline: the gap is that the gated row *doesn't use the atom*, not that no row exists. |
| 7 | CONTENT grep, not just filenames | `grep -ril "transaction\|ledger\|statement\|document row\|downloadable" knowledge/snippets/ knowledge/components/` → 50 files. Every hit inspected by name: **the only component-level ones are `List-items` (the transaction row itself), `list-items.meta.json`, `File-upload` (upload file rows), `amount-display.meta.json` (the gap note) and the two `_nodes-*.json` indexes.** No document/statement row component. | ✅ ran |
| 8 | Is any of this already RULED? — **direct grep of the store, not the index** | `python3 -c "json.load(open('knowledge/_rulings.json'))"` → **203 entries**. Regex `transaction\|ledger\|statement row\|document row\|line[- ]item\|debit\|credit` → **16 entries matched**, every one inspected in context. **ALL 16 use "ledger" in the RECORD-KEEPING sense** — a decisions ledger, `_TOKEN-FORK-LEDGER.json`, an exceptions ledger, "ledger entries", "the 42-name ledger baseline". **ZERO concern a transaction, statement or document COMPONENT.** | ✅ **UNRULED** — searched twice (`unrun-search-indistinguishable-from-absent-record`) |
| 9 | Retrieval index reliability | `_checkin.py` rehearsal, verbatim: *"⛔ STRUCTURAL retrieval index is STALE — it does not match GOOD-MORNING.md / `_LIVE-STATE.md` as they now stand, so `_memento_search.py` is serving a PREVIOUS session's record."* | ⚠ **CONFIRMED STALE.** Every ruling claim in this receipt rests on the **direct grep of `_rulings.json`**, the store itself (`retrieval-default-hides-the-ruling`: store > chain). |
| 10 | Reviews dir has no prior artefact for these rows | `ls reviews/ \| grep -iE "transaction\|ledger\|statement\|document"` → **rc 1, no output** | ✅ CONFIRMED |

---

## Deliverables — 3 new files, nothing overwritten, nothing else touched

| File | State |
|---|---|
| `knowledge/snippets/Document-row.reference.html` | **NEW** — PROPOSED specimen |
| `knowledge/components/document-row.meta.json` | **NEW** |
| `reviews/REVIEW-204-document-row-four-themes-v1.html` | **NEW** — 4 themes × light/dark, 8 panes |
| `notes/_receipts/2026-08-19-204-wave-laneN-fintech-rows.md` | **NEW** — this file |

**No `Transaction-row` / `transaction-row` artefact of any kind was created.** Row 91 was stopped at
step 0 and pivoted to measurement, exactly as the brief instructs for a false premise.

**Specimens COPY the approved artefact, never re-draw** (`specimen-starts-from-reference`). Sources
copied and left **untouched**:

| Source (gated) | What was copied |
|---|---|
| `List-items.reference.html` | row shell (`ul`/`li` borders, surface, divider), two-line body geometry, density tokens `--row-h`/`--row-pad`/`--label-gap`, the hover trick where the leading disc flips to the default surface, the Status-indicator form-B chip, the disabled-glyph treatment, the container-query reflow |
| `Status-indicator` (via List-items) | RAG tint chip form B — tint surface + dot + **neutral** label |
| `Icon-button.reference.html` | 44×44 hit area, 18px glyph, focus-ring form |
| `File-upload.reference.html` | the file-type glyph *approach*; glyphs themselves byte-matched from `knowledge/assets/icons/media/{document-e-statement,document-pdf,document}.svg` and `global-controls/download.svg` |
| `Amount-display.reference.html` + meta | **deliberately NOT used** — see "no money colour" below. Read in full; its ruled treatment is quoted, not extended. |
| `Kpi-tile.reference.html` (#203 PROPOSED) | the PROPOSED-specimen shape, the AUTO-TOKENS block, the zero-type-debt approach, the review-page `.cn-<slug>` mirror |

★ **One deliberate divergence from the parent, declared:** `List-items` still carries raw
`font:500 16px/1.35 var(--font)` declarations. **I copied its anatomy, not its type debt.**

---

## Gates — every rc VERBATIM

| Gate | rc | Output (last line, verbatim) |
|---|---|---|
| `_validate_snippets.py` (repo-wide, after build) | **rc=0** | `snippet gate: 86 snippet(s), 0 failure(s)` |
| `_validate_a11y.py` (repo-wide) | **rc=0** | `a11y gate: 86 snippet(s), 0 failure(s), 186 warning(s), 194 note(s) · 528 controls + 203 marks measured · 107 mark(s) below 24` |
| `_validate_type_composites.py` — **my file, filtered** | **rc=0** | `TYPE GATE PASS — all component text bound to canon composites (1 file(s)).` and `advisory — 0 raw font decl(s) in demo-chrome scope` |
| `_validate_type_composites.py` — repo-wide | **rc=1** | `TYPE GATE FAIL — 1097 violation(s) across 90/101 file(s).  TYPE-001 ×31 · TYPE-002 ×1050 · TYPE-003 ×16` |
| `_validate_snippets.py` (repo-wide, **mid-lane re-run**) | **rc=1** | `❌ Runway-bar.reference.html: ALL-CAPS text run "INK ON TRACK"` + `❌ … "NO RED WAS INVENTED"` |
| `_validate_snippets.py` (repo-wide, **at close, after all 4 fixes**) | **rc=0** | `snippet gate: 91 snippet(s), 0 failure(s)` |
| `_validate_a11y.py` (repo-wide, **at close**) | **rc=0** | `a11y gate: 91 snippet(s), 0 failure(s), 186 warning(s), 218 note(s) · 566 controls + 203 marks measured · 107 mark(s) below 24` |
| `_validate_type_composites.py` — my file, at close | **rc=0** | `TYPE GATE PASS — all component text bound to canon composites (1 file(s)).` |
| `_validate_type_composites.py` — repo-wide, at close | **rc=1** | `TYPE GATE FAIL — 1097 violation(s) across 90/106 file(s).` — **still 1,097; I added 0** |
| `_validate_state_contrast.py` | **NOT RUN — declared** | see residuals |

★ **THE RATCHET HELD: 1,097, unchanged. I added ZERO.** 1,097 is Lane K's measured #203 baseline and
the figure `MEMORY.md` records; it did not move. My file contributes **0** type violations.

⚠ **THE MID-LANE RED WAS NOT MINE, AND I ATTRIBUTED IT BY DIFFING, NOT BY TRUSTING THE FILTER**
(the brief's known-defect warning). Both failures name `Runway-bar.reference.html`, a **sibling lane's**
file; `grep -c "Document-row"` against the failure list returned **0**. It had cleared by my closing run
(rc back to 0 at 90 snippets), so a sibling repaired it in-window. **Stated as an observation with its
probe, not a claim about who fixed it.**

⚠ **Concurrency is visible and every count here is timestamped by the probe that produced it:** the
snippet count moved **86 → 90** during this lane as sibling lanes wrote, and the type gate's file count
moved **101 → 105**.

⚠ **The filtered runs of `_validate_snippets.py` / `_validate_a11y.py` are not actually filtered** — they
ignore the path argument and sweep the whole directory, exactly as the brief warned. I never relied on
them for attribution.

**Gates left to the BUILD-PM, by name:** `_validate_state_contrast.py`, `_validate_radius.py`,
`_validate_coverage.py`, `_validate_icons.py`, `_validate_dtcg.py`, `_validate_kg.py`,
`_build_integrity.py`, and every generator `--check`. A declared gap passes; this is the declaration.

---

## Render proof — driven in a real browser, not asserted

`goto("file://…")` throughout; **`set_content()` never used**. Chromium from the cached farm
`/var/tmp/pw-browsers-s197`; `playwright` from `/var/tmp/pylibs-s203e`; `LD_LIBRARY_PATH` →
`/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu`. Fontconfig **symlink farm** built fresh at
`/var/tmp/fonts-s204n` with the `<include>` present — ⚠ the surviving `/var/tmp/fonts-s203*` farms are
**dead**: their symlinks point at a *foreign session's* mount path (`/sessions/gallant-festive-hopper/…`)
which no longer resolves. Reusing one would have silently fallen back to a substitute face. I read the
runbook and built my own farm; **I did not write "cannot render" at any point.**

**Font asserted by CANVAS MEASUREMENT against three controls, never `fonts.check()`:**
target `"Univers Next for HSBC"` = **423** · alias `"Univers Next HSBC"` = **423** ·
`DejaVu Sans` = **459** · nonexistent face = **361** ⇒ both aliases land on the real HSBC cut, and the
probe demonstrably discriminates.

**Result: 8/8 panes, 0 page errors, at 1400px AND 480px, no document overflow, 0 clipped titles.**
All four themes fork correctly, read off the DOM:

| theme | mode | title colour | glyph radius | glyph box | title clip (client/scroll) |
|---|---|---|---|---|---|
| mono | light / dark | `#1A1A1A` / `#FFFFFF` | 0px | 36×36 | 21/21 |
| legacy | light / dark | `#333333` / `#FFFFFF` | 0px | 36×36 | 21/21 |
| console | light / dark | `#1A1A1A` / `#FFFFFF` | **4px** (the console indicator fork) | 36×36 | 21/21 |
| supercharge | light / dark | `#13110E` / `#F7F6F4` | 0px | 36×36 | 21/21 |

**44px min-hit-area — ENFORCED BY HAND AND PROVEN, since no gate reads the token.**
**88 interactive targets** measured across all eight panes. **Minimum dimension: 44. Under 44: ZERO.**
At **480px**: same 88 targets, minimum **44**, under-44 **zero**, overflow **false**, clipped titles **0**.
(The primary target is measured as the full row the stretched link covers — min-height 76px — because
that is the real hit area; the `<a>` element's own box would flatter the number.)

**Status-chip contrast, computed with the repo's own `knowledge/_contrast_utils.contrast_ratio`,
label-on-tint, all four themes × both modes:**

| theme | mode | label on info-tint | label on warning-tint |
|---|---|---|---|
| mono | light / dark | 14.32:1 / 9.44:1 | 14.09:1 / 8.21:1 |
| legacy | light / dark | 10.94:1 / 19.56:1 | 11.95:1 / 17.63:1 |
| console | light / dark | 12.67:1 / 9.17:1 | 13.14:1 / 8.00:1 |
| supercharge | light / dark | 14.41:1 / 15.27:1 | 15.26:1 / 12.45:1 |

**Minimum across all 16 pairs: 8.00:1**, against an AA-text floor of 4.5. And **every status carries its
WORD** ("New", "Action needed") as well as its hue — the dot is decorative and `aria-hidden`.

### ★ THE STRUCTURAL ASSERTION — the component's whole reason for existing, DRIVEN not argued

This is the claim the component rests on, so it was tested against the live DOM rather than asserted
(`mutation-tests-the-clause-not-the-feature` — drive the thing):

```
rowTag:                       "LI"            ← the row is PASSIVE, not a <button>
buttonNestedInsideLink:       false
buttonNestedInsideAnyButton:  false
linkNestedInsideAnything:     false           ← no nesting anywhere (4.1.1)
clickAtButtonCentreHits:      "dr-dl"         ← the DOWNLOAD BUTTON wins over the stretched link
clickOverRowBodyHits:         "dr-title …"    ← the stretched link still covers the row body
focusableTargetsInRow:        2               ← exactly two, as designed
tab order in the list:        [dr-title, dr-dl, dr-title, dr-dl, dr-title, dr-dl]
variantB element:             "A"  with 0 nested controls   ← variant B is genuinely single-action
```

**`elementFromPoint` at the button's centre resolves to `.dr-dl`, and at the row body to `.dr-title`.**
Two independent targets in one row, neither inside the other, correct tab order. That is the thing
List-items' all-row-is-a-button shape cannot express, demonstrated rather than claimed.

⚠ **One probe CRASHED and was fixed loudly, not glossed** (`a-crash-is-not-a-fail`): the first run of
this assertion threw `Cannot read properties of null (reading 'className')` because the row was below
the fold and `elementFromPoint` returned `null`. Fixed with `scrollIntoView` + a re-read of the rects,
and the null branch now returns the literal string `"NULL — OFFSCREEN, PROBE INVALID"` so a future
silent null can never read as a pass.

### ★★ FOUR DEFECTS THE GATES COULD NOT SEE — every one caught by looking or measuring, none by a gate

Every gate was green over both (`green-tests-cannot-see-scope`):

**1. ⛔ The review page's theme cascade was DEAD, and mono's warning chip rendered with NO TINT.**
My page-builder scoped the snippet's `[data-theme="light"|"dark"]` blocks into
`.cn-document-row[data-theme="light"]` — **which never matches on the review page, where `data-theme`
sits on the `.pane` ANCESTOR.** Measured symptom: mono's warning chip computed
`background-color: rgba(0, 0, 0, 0)` in both light and dark, while legacy/console/supercharge were fine
(they get their values from the `[data-apollo-theme]` cascade blocks, which mono has none of).
**This is the `dangling-dataviz-var-renders-silent-black` class in a new place: a var that resolves to
nothing renders as *nothing*, and no gate fires.** Fixed the correct way rather than patched: the page
now emits **one `.cn-document-row{}` block binding each var to its CANON TOKEN by name, derived
programmatically from the snippet's own `#token-manifest`** — which is what `gen_canon_components.py`
actually does and what `REVIEW-203-kpi-tile` shows. Re-measured: mono warning tint now `#F6E6C0` light /
`#614C1C` dark, all eight panes correct. **The snippet was always right; only the review surface was
wrong** — the same shape of defect Lane K hit at #203, in a different mechanism.

**2. ⛔ The disabled row's file glyph was COMPLETELY INVISIBLE in light mode.**
I had coloured it `--disabled-text`, which in light is **`#E1E1E1` on a `#E1E1E1` disabled surface** —
identical values, glyph gone. **No gate fires because disabled content is exempt from 1.4.3.** Corrected
to the parent List-items' own treatment (`--reverse`, white), restoring `--reverse` → `text/reverse` to
the manifest. Re-measured across all eight panes: `#FFFFFF` on `#E1E1E1` (mono/legacy/console light),
`#FFFFFF` on `#484848` (dark), `#F7F6F4` on `#CDC8C6`/`#413934` (supercharge).
⬛ **But the parent's own treatment is itself only 1.42:1 in light.** That is List-items' promoted,
Dave-approved behaviour and I did **not** change it — surfaced, never auto-swapped (`grey-tint-check`).
It is decision 8 below.

**3. ⛔ TWO MANIFEST VARS WERE SELF-REFERENTIAL AND RESOLVED TO NOTHING IN ALL EIGHT PANES — and the
page still LOOKED right.** This is the one I predicted as my highest-risk residual, so I went back and
measured **all 22 manifest vars × 8 panes = 176 combinations** instead of leaving it declared.
Result: **14 unresolved**. `--border-radius-indicator` and `--border-radius-surface` are vars whose
component name **is already the canon token name**, so my generated base block emitted
`--border-radius-indicator: var(--border-radius-indicator);` — **a self-reference, which is invalid at
computed-value time and resolves to empty.**
★ **It looked correct by accident.** An invalid `border-radius` falls back to the initial value `0`,
which happens to be the angular rule's answer in three of four themes — so a square corner rendered for
the right reason in mono/legacy/supercharge and for entirely the wrong reason everywhere. Fixed by
omitting self-references and letting them inherit from `canon.css`. **Re-measured: 0 unresolved out of
176.**

**4. ⛔ COPYING A SIBLING'S CASCADE SILENTLY DROPPED CONSOLE'S RULED 20px SURFACE RADIUS.**
My review page's per-theme cascade was copied from `canon.css`'s own `.cn-list-items` blocks. But
`.cn-list-items` **does not declare `--border-radius-surface`** (its shell is a plain bordered `ul`),
while **mine does**. And `canon.css` emits `--border-radius-surface: 20px` for console **per component
scope** — every component that declares the var gets it (the `s199-D3` console radii). Probe:
`grep` for console blocks declaring radius → `.cn-account-card`, `.cn-alert`, `.cn-cards`,
`.cn-avatar-group`, … **all 20px**. So the copy inherited a *neighbour's omission* and console's shell
measured **0px** where the generator would have given 20px.
⚠ **And the miss was double**: the shell rule had **no `border-radius` declaration at all**, so the var
was declared in the manifest and never consumed — the opposite defect, in the same place.
Both fixed; console shell now measures **20px**, glyph **4px**, all other themes square.
**Lesson: `specimen-starts-from-reference` is right, but a copied cascade carries the source's
ABSENCES as well as its values, and an absence is invisible.**

★ **Final verification after all four fixes, re-driven end to end:** 22 vars × 8 panes = **0
unresolved**; 8/8 panes; **0 page errors**; **88 targets, minimum 44, zero under 44** at **both** 1400px
and 480px; **0 clipped titles** at both; no overflow at either. Console glyph 4px / shell 20px; mono,
legacy and supercharge square. Gates re-run after the last edit: `_validate_snippets.py` **rc=0**
(`91 snippet(s), 0 failure(s)`), `_validate_a11y.py` **rc=0** (`91 snippet(s), 0 failure(s)`), type
filtered **rc=0**, type repo-wide **rc=1 at 1,097 — unchanged**.

### ⬛ The ONE visual departure from the parent, declared rather than buried

`List-items`' `ul.list` declares **no radius** and its manifest does not carry
`--border-radius-surface`, so its shell is square in **every** theme — including console, where every
neighbouring surface is 20px. Copying it faithfully would have left this shell square beside round
cards. **I bound the shell to `border-radius/surface` so it follows the THEME's rule rather than
inheriting a neighbour's omission**, with `overflow:hidden` so the end rows clip to the corner.
This is the only place I departed from the parent's literal CSS on a visual matter. It is flagged in
the snippet, the meta and this receipt. **If Dave prefers the square shell, delete two declarations and
drop the var from the manifest** — decision 10 below.
⚠ It also raises a question I am **not** ruling: **should `List-items`' own shell take console's 20px?**
Right now the two will look different in console. **Surfaced, not fixed** — `List-items` is gated.

Renders viewed by eye at `outputs/s204n-renders/` — **(NON-REPO: session outputs folder)**, `s191-D2`
marker. They are my verification, not review artefacts; the HTML is what Dave reviews.
The page-builder is a **throwaway at `/var/tmp/s204n/`, outside the repo** (the #174/Lane E/Lane K
precedent). It is **not** an instrument the repo carries. `machinery: 0 instrument / ~430 feature`.

---

## How Document-row differs from its nearest gated neighbours

### vs `List-items` (the transaction row) — THE STRUCTURAL DIFFERENCE

In List-items **the whole row IS a `<button>`** (`<li><button class="row" type="button">…`, verbatim).
That shape supports exactly **one action per row**. A downloadable document row has **two actions that
are not the same action**: (a) open/preview the document, (b) download the file. You cannot nest an
interactive control inside a `<button>` — invalid HTML (4.1.1), the inner control is unreachable by
keyboard in several ATs, and the outer accessible name absorbs the inner one. So the two-action row
**cannot** be added as a `type="document"` value on List-items' existing `type` enum without changing
List-items' own row **element** for every other variant — and List-items is gated, promoted and 9.0/9.

**When to choose which:** List-items when the row is a **money event** the reader may open. Document row
when the row is a **file** the reader may open or take away. *The tell: a document row has no amount, and
a transaction row has no file.*

**The one visual change from the parent, and its reason:** List-items' leading visual is the **round**
Avatar disc — the documented round exemption, which exists for **people**. A file is not a person, so
the leading slot here is the same 36px but **square** (`border-radius/indicator`), which console forks
to 4px through the cascade exactly as it does for List-items' own indicator atoms. **No exemption is
claimed and none is needed.**

### vs `File-upload` (gated, itinerary row 18)

Same anatomy, **opposite direction**. File-upload is **inbound**: files the user is giving the bank,
mid-transfer, with a progress bar, a size-validation error state and a **remove (×)** control; its rows
are ephemeral. Document row is **outbound**: files the bank has already issued — complete, persistent,
with a **download** control, no progress, no removal.
**The tell: a File-upload row can FAIL ("This file is over 10MB"). A document row cannot — it already
exists.** The file-type glyphs are byte-matched from the same library, which is deliberate reuse.

### ⛔ NO MONEY COLOUR WAS INVENTED — the trap the brief named, and how it was avoided

A ledger/statement row is exactly where a debit/credit +/− colour binding gets improvised into canon.
**This component carries no monetary value at all, so there was no seat to invent and none was
invented.** Where an amount is genuinely wanted on such a row, the answer is the **gated Amount-display
atom**, which already holds the approved treatment. Copied from `amount-display.meta.json`, **not
extended by a single value**: the value is monochrome with a **U+2212 MINUS** for negatives, and the only
coloured seats are `sign=positive` → `rag/success-ink` (`s155-D1`, `s158-D2`) and `sign=negative` →
`rag/error-ink` (`s158-D3`), background-keyed `#137F3C`-on-white / `#66CC8D`-else for green and the
`s151-D1` two-red law for red, **MONO ONLY**.
The only colour in this component is the **status chip**, which is the Status-indicator atom form B
copied verbatim from List-items, and **every status carries its word as well as its hue**.

---

## Findings

1. **★★★ Row 91 is a duplicate of a Dave-promoted build.** Full evidence in the headline. The itinerary
   should read **Duplicate**, not Gap/Partial. **Dave's call, not mine.**
2. **★★ A slug-shaped probe cannot see a component that ships as a VARIANT of another component.** All
   five probes for row 91 were negative and all five were *correct* — the transaction row has no slug of
   its own; it is `list-items` `type: "transaction"`. Any derived-status instrument that probes by slug
   will manufacture this same false gap for **every variant-shipped row in the library**. This is a
   **class**, and it is the mechanism behind row 91's mis-flagged drift.
3. **★ The gated transaction row contradicts `copy-025` and does not compose Amount-display.** It renders
   `−1,234.00 HKD` — currency code *after* the value, *with* a space — which is Amount-display's own
   antiPattern #1 verbatim. This is what `amount-display.meta.json`'s *"Transaction / ledger row (gap)"*
   pointer actually means. A real, small repair on a gated file; **not mine to make.**
4. **⛔ A review page can silently lose its whole theme cascade** (defect 1 above). Snippet-scoped theme
   blocks scoped naively become `.cn-x[data-theme=…]`, which never matches when `data-theme` is on an
   ancestor. Symptom is a **transparent** background, not an error. Gate candidate proposed below.
5. **⛔ Disabled content is exempt from 1.4.3, so a disabled element can render at 1.00:1 and every gate
   stays green** (defect 2 above). The parent List-items ships this at 1.42:1 today.
6. **⚠ Surviving `/var/tmp/fonts-s203*` farms are DEAD and fail SILENTLY.** Their symlinks point at a
   foreign session's mount (`/sessions/gallant-festive-hopper/…`). Reusing one substitutes a fallback
   face with no error. **A font farm must be rebuilt per session, and the canvas control probe is what
   catches it.** Worth a line in `_RUNBOOK-render-verify.md` — the runbook's cleanup note covers
   *undeletable* stale dirs but not *silently wrong* ones.
7. **⛔ A self-referential custom property resolves to EMPTY and can look correct by accident**
   (defect 3). `--x: var(--x)` is invalid at computed-value time; an invalid `border-radius` falls back
   to `0`, which is the angular rule's answer in three of four themes. **A right-looking pixel is not
   evidence of a resolved token.**
8. **⛔ A per-theme cascade copied from a sibling carries the sibling's ABSENCES** (defect 4), and an
   absence renders as a plausible default rather than an error. Console's ruled 20px surface radius was
   silently lost this way.
9. **⚠ Inherited, not invented:** `text/secondary` on `tertiary/background/hover` in dark measures
   3.34:1 (< 4.5). This is **List-items' own open `$darkFinding`**, which calls it **SYSTEMIC** across
   every interactive row with secondary text on a hover surface. `list-items.meta.json` remains its home;
   I did not invent around it.

---

## Decisions needed — Dave's, every one PROPOSED #204

1. **★ Should itinerary row 91 be marked DUPLICATE?** The transaction row is built, gated and promoted
   (2026-06-22, 9.0/9). Nothing to build. *(Store search that failed to settle it: direct grep of all
   203 entries of `_rulings.json` for `transaction|ledger|statement row|document row|line[- ]item|
   debit|credit` → 16 hits, **all 16** using "ledger" in the record-keeping sense, **zero** about a
   component. `s202-D3` satisfied.)*
2. **★ Should the Document row exist at all?** If the product only ever needs the single-action form
   (**variant B** on the review page), it should not — row 92 collapses into List-items too. Both forms
   are drawn so this can be ruled by eye.
3. **P1 — document-type vocabulary** (statement / certificate / tax / contract / generic). My wording,
   unratified. *(Same store search as 1; nothing found.)*
4. **P2 — statement periodisation.** Built as title *"June 2026 statement"* + meta *"1 Jun – 30 Jun
   2026"*. Alternative: title *"1–30 June 2026"*, no separate period. Also unruled: whether the
   **period** or the **issue date** is the one that shows. *(Same store search; nothing found.)*
5. **P3 — the download affordance's form.** Built as a trailing 44×44 icon-button with no visible label.
   Alternatives: a text link, a whole-row download, an overflow menu when several formats exist.
   ⚠ `s182-D2` is cited in the specimen as **precedent** for a label-less trailing affordance; it governs
   the **trend card**, not this component. Precedent, not authority.
6. **P4 — does a document row carry a status chip at all?** Shown for "New" and "Action needed".
   Equally arguable: documents have no status, only a date.
7. **P5 — file meta content and order** (`PDF · 1.2MB`). Whether size shows at all is a product call.
   **P6 — density default:** roomy (inherited from List-items) vs compact for long archives.
8. **The disabled-glyph contrast (finding 5).** The parent's treatment is 1.42:1 in light. Accept as
   deliberate (disabled is exempt), or raise it? **Whatever you decide, List-items and Document row must
   move together** — I copied the parent precisely so they can't drift apart.
9. **Finding 3 — the gated transaction row's amount format.** Repair it to `copy-025` and compose
   Amount-display, or leave it? It is a gated file; I touched nothing.
10. **★ The list shell's corner radius — my one visual departure from List-items.** I bound the shell to
    `border-radius/surface`, so in console it is 20px like every neighbouring surface; `List-items`'
    shell is square in every theme because it declares no radius at all. **Two questions, one eye:**
    is 20px right for this shell in console, and **should `List-items`' own shell move with it?**
    Right now the two rows will look different in console. Square is two deletions away.

**None of the above was resolved here. Nothing a sub writes is a ruling.**

---

## Proposals for the BUILD-PM to merge — exact text (I edited no shared file)

- **`_DS-IMPROVEMENTS.md`** — *"A review/showroom page can silently lose an entire theme cascade. Snippet
  `[data-theme=…]` blocks scoped naively become `.cn-<slug>[data-theme=…]`, which never matches when
  `data-theme` sits on an ancestor pane; the symptom is a TRANSPARENT background, not an error, and no
  gate fires. Reproduced at #204 (mono's warning chip computed `rgba(0,0,0,0)` while the other three
  themes were correct). Candidate gate: for every `.cn-<slug>` scope, assert that each var named in the
  source snippet's `#token-manifest` resolves to a non-empty computed value in all four themes × both
  modes. This is the same class as the dangling-dataviz-var defect (#184), on a different surface."*
- **`_DS-IMPROVEMENTS.md`** — *"No contrast gate can see a DISABLED element: disabled content is exempt
  from 1.4.3, so a disabled glyph may render at 1.00:1 (invisible) with every gate green. Proven at #204,
  where a disabled file glyph computed `#E1E1E1` on `#E1E1E1`. The gated List-items ships the same
  treatment at 1.42:1. Candidate: an ADVISORY (non-blocking) disabled-legibility report, since the SC
  genuinely exempts it and a blocking gate would be wrong."*
- **`_DS-IMPROVEMENTS.md`** — *"A generated `.cn-<slug>` scope can emit SELF-REFERENTIAL custom
  properties. Where a component's var name is already the canon token name (`--border-radius-indicator`,
  `--border-radius-surface`), a naive `--x: var(--x)` resolves to EMPTY at computed-value time. Proven at
  #204: two vars unresolved in all 8 panes, and it LOOKED correct because an invalid `border-radius`
  falls back to the initial value 0 — the angular rule's answer in three of four themes. Candidate gate:
  refuse to emit any declaration whose value is `var(<its own name>)`, and assert every manifest var
  resolves non-empty per theme × mode."*
- **`_DS-IMPROVEMENTS.md`** — *"A per-theme cascade COPIED from a sibling component carries that
  sibling's ABSENCES as well as its values, and an absence is invisible. Proven at #204: the cascade was
  copied from `.cn-list-items`, which does not declare `--border-radius-surface`; the copying component
  does. `canon.css` gives console 20px for that var in every scope that declares it (`s199-D3`), so the
  copy silently rendered a 0px shell where the generator would give 20px. When mirroring a scope, derive
  from the TARGET's manifest and fill every var the target declares, rather than diffing a neighbour."*
- **`_DS-IMPROVEMENTS.md`** — *"A slug-shaped artefact probe cannot see a component that ships as a
  VARIANT of another component. At #204, all five probes for itinerary row 91 (Transaction / ledger row)
  returned NEGATIVE and all five were correct — the row has no slug of its own; it is `list-items`
  `type: \"transaction\"`, promoted by Dave 2026-06-22 at 9.0/9. Any derived-status instrument that
  probes by slug will manufacture a false gap for every variant-shipped row in the library. A status
  probe must consult each meta's `props`/`variants` as well as the filesystem."*
- **`_RUNBOOK-render-verify.md`** — *"A surviving `/var/tmp/fonts-<session>` farm from a FOREIGN session
  is DEAD and fails SILENTLY: its symlinks point at that session's mount path, which no longer resolves,
  so fontconfig substitutes a fallback face with no error. Rebuild the farm per session. The canvas
  control probe (target vs alias vs DejaVu vs a nonexistent face) is what catches it — `fonts.check()`
  would not."*
- **`reviews/ITINERARY-*` row 91** — status should become **Duplicate**, pointing at
  `component:list-items` `type: "transaction"`. ⛔ **Not merged by me** — the itinerary files are fenced,
  and this is Dave's call per decision 1.
- **`reviews/ITINERARY-*` row 92** — genuinely **Gap**; now **PROPOSED**, pending decision 2.
- **`_validate_radius.py` `MIGRATED_SNIPPETS`** — `Document-row.reference.html` is absent from the radius
  ratchet (⛔ shared file). Console's 4px indicator fork was verified present in the render.
- **`CATEGORIES` / `gen_showroom.py` / `component-types.json` / `canon.css`** — slug `document-row` has no
  entry in any of them. **All four are promotion decisions and therefore Dave's, not merge chores** —
  flagged, not requested. **None should be added before Dave rules decision 2.**
- **No new token is wanted.** Every value this component uses already exists and is already ruled. Zero
  tokens proposed, zero colour seats invented.

---

## Friction log

- **The brief's central question had a sharper answer than "overlap".** Row 91 is not a duplicate *risk*
  — it is a duplicate of a **promoted** component. The meta's own `build.$status` settled it in one read.
  Had I trusted the itinerary's "Gap"/"Partial", I would have built a second transaction row alongside
  Dave's own 9.0/9 one. **`premise-ages-faster-than-rule` earned its keep: the derived snapshot's Status
  column was wrong for one of my two rows.**
- **`_memento_search.py` is serving a stale index** — `_checkin.py` says so itself. Every ruling claim
  here rests on a direct grep of `_rulings.json`.
- **The `/var/tmp/fonts-s203*` farms looked reusable and were not** (finding 6). Cost one call; caught by
  building my own rather than assuming, and the canvas control probe would have caught it regardless.
- **My own review-page builder introduced the defect that ate the theme cascade.** Caught only by
  measuring computed styles pane-by-pane. **A page-builder is an artefact that needs its own
  verification, not a transparent pipe** — the same lesson Lane K recorded at #203, arrived at
  independently through a different mechanism.
- **My first structural probe crashed on an off-screen `elementFromPoint`.** Fixed loudly; the null
  branch now returns a shouting sentinel so a future null cannot read as a pass.
- **Concurrency is visible**: snippet count 86 → 90 mid-lane; a sibling lane's `Runway-bar` failure
  appeared and cleared inside my window.

---

## Residuals — declared, not glossed

- **`_validate_state_contrast.py` NOT RUN.** A filtered run **overwrites the tracked
  `_STATE-CONTRAST-AUDIT.md`**, and the brief forbids it. **It is owed** — BUILD-PM or CI.
- **HEAD sha not captured** — the lane brief's ⛔ on git commands overrides the base brief's §3.
- **`Document-row` is absent from `canon.css`, the radius ratchet, the showroom and
  `component-types.json`.** All four are fenced shared surfaces. The review page's `.cn-document-row`
  scope is a **hand-mirror derived programmatically from the snippet's own `#token-manifest`** — faithful,
  but **not generator output**. That is the fence working, and it is declared, not silent.
- **⚠ The review page's per-theme cascade blocks are COPIED from `canon.css`'s own `.cn-list-items`
  blocks** (the same list-row family), with `--avatar` renamed to `--glyph-bg` and three vars this
  component does not declare (`--pressed`, `--tag-border`…) filtered out, **plus console's
  `--border-radius-surface: 20px` added by hand because `.cn-list-items` omits it and my component
  declares it** (defect 4). They are generator output for a *sibling*, adjusted — not output for this
  component. **When the BUILD-PM regenerates, the authoritative scope should replace the mirror**, and
  the result should be re-rendered. My base block binds canon tokens directly, so much of the cascade may
  prove redundant, but I have **not** proven that and do not claim it.
- **The 22-var × 8-pane resolution check is a MOMENT, not a standing guarantee** (`conclusions-are-debt`).
  It passed at close; nothing in the repo will re-run it. The proposed gate is the durable form.
- **Narrow-viewport reflow below 480px is unexamined** and not claimed. Verified at 1400 and 480 only.
- **The container-query reflow at 360px is written but NOT exercised** — no pane in the review page is
  narrow enough to trigger it. **Declared UNPROVEN.**
- **Row 91 produced no artefact at all**, by design. If the BUILD-PM expected a specimen for it, the
  answer is finding 1: there is nothing to specimen that Dave has not already approved.
- **Print styles, RTL and forced-colors mode are unexamined** for this component.
- `outputs/s204n-renders/` holds 3 PNGs — **(NON-REPO: session outputs folder)**, `s191-D2`.
- Throwaway builder at `/var/tmp/s204n/` — outside the repo, not carried, not an instrument.

---

## ⛔ CONSEQUENCES / PITFALLS — what a verifier should attack first (Dave #165)

**What I did NOT run:** `_build_all.py` and every generator (fenced). `_validate_state_contrast.py`
(would overwrite a tracked file). `_validate_radius.py`, `_validate_coverage.py`, `_validate_icons.py`,
`_validate_dtcg.py`, `_validate_kg.py`, `_build_integrity.py`. Any git command. Any write to
`_rulings.json`. I never rendered the **snippet** standalone — **only the review page** — so the
snippet's own `[data-theme]` blocks are gate-verified but **not eye-verified in a browser**.

**What a green gate here cannot see:**
- **Nothing in the library gates the 44px minimum.** My 88-target measurement is a **moment**, not a
  standing guarantee (`conclusions-are-debt`). A later edit can breach it with every gate green.
- **No gate parses the review page at all.** It is not in `snippets/`, so `_validate_snippets.py` and
  `_validate_a11y.py` never look at it. The theme-cascade defect I found lived precisely there, and only
  a hand-written computed-style probe caught it. **This is `no-gate-parses-the-artefact` (#122) alive in
  the review surface.**
- **No gate resolves a `binds`/manifest address against the colour spine** — `amount-display.meta.json`
  says so itself at #145: *"no validator resolves a meta 'binds' address against the colour spine …
  rename the rung and every gate stays green."* My manifest's 25 var→token addresses are **unchecked by
  any instrument** beyond `_validate_snippets.py`'s value comparison.
- **No gate sees disabled-element contrast** (finding 5).
- **The type gate passed my file but the repo-wide ratchet is still red at 1,097.** "The ratchet held" is
  a statement about a **delta**, not about health.

**What a verifier should attack FIRST, in order:**
1. **The duplicate ruling.** Re-read `list-items.meta.json` `build.$status`/`build.scope` and
   `List-items.reference.html`'s `<title>` yourself. If I am wrong about row 91, everything downstream —
   including "don't build it" — is wrong. *(I believe this is the strongest-evidenced claim in the
   receipt, which is exactly why it should be checked first.)*
2. **The structural claim that justifies the component existing.** Re-drive `elementFromPoint` over the
   download button. If the stretched link swallows the button on any theme or width, the component's
   whole rationale collapses and it should become a List-items variant.
3. **~~The theme cascade, per pane, per var.~~ — I CALLED THIS MY HIGHEST RISK, THEN WENT AND CLOSED IT,
   AND I WAS RIGHT THAT IT WAS HIDING SOMETHING.** All **22 manifest vars × 8 panes = 176 combinations**
   are now measured: **14 were unresolved** (defect 3) and are now **0**. A verifier should still re-run
   it — it is a *moment*, not a guarantee — but it is no longer an undeclared hole. **The general lesson
   is worth more than the fix: "I did not check X" is a residual that can often just be turned into a
   measurement, and when the residual is the one you would bet on, it usually should be.**
4. **The 360px container-query reflow**, which is written and never exercised.
5. **Whether variant B should have been built at all** — if Dave rules single-action, most of this
   component is scaffolding around a List-items row.

**The failure mode I would bet on:** not the snippet, but **the review page** — it is ungated, hand-built,
and already produced one silent defect that eight green gates could not see.
