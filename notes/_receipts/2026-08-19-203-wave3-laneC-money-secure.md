# Receipt — #203 Wave 3, Lane C · money & secure

*Worker receipt per the parallel-conductor checklist and `_BRIEF-wave3-foundations-2026-08-19-v1.md`.*
*Written 2026-08-19 against HEAD `ec2336d`. Opus work sub.*
*⛔ **Nothing here is a ruling.** No commit, no push, no `git checkout/restore/stash`.*
*`knowledge/_rulings.json`, `knowledge/tokens/*`, `MEMORY.md`, `_DS-IMPROVEMENTS.md` untouched.*

**Context gauge at close:** not stamped — `_checkin.py` writes to the shared
`notes/_REHEARSAL-LOG.jsonl`, and five sibling lanes are live in the same tree this session. Declined
rather than add an unattributable append to a shared rolling file. Declared, not silent. Rough self-read:
one long lane, ~25 tool calls, no chunking failures, no call-boundary kills.

---

## ⚠ Step 0 — THE LANE C PREMISE IS FALSE. All three components already exist.

The brief's §3 asks me to verify "the claimed absence of your components". They are **not absent.**

| Claim inherited from the brief | Verified? | Evidence (probe named) |
|---|---|---|
| HEAD is current | ✅ `ec2336d` (#202 wrap) | `git log --oneline -1` |
| Amount/currency display (row 89) is a **P1 Gap** | ❌ **FALSE** | `ls knowledge/snippets/` → `Amount-display.reference.html` (152 ln) |
| Number/currency input (row 17) is a **P1 Gap** | ❌ **FALSE** | `Amount-input.reference.html` (306 ln) |
| OTP/PIN secure entry (row 19) is a **P1 Gap** | ❌ **FALSE** | `Secure-entry.reference.html` (361 ln) |
| …and they are only half-through the route | ❌ **FALSE** | metas + `.cn-amount-display` / `.cn-amount-input` / `.cn-secure-entry` in `canon.css` + `showroom/<slug>.html` all present |

All three were **built, gated and generated on 2026-07-22** (Phase-2 wave 1, worker A). Both snippets say
so in their own header comments and cite their itinerary rows verbatim — `Secure-entry` line 9:
*"itinerary row 19 (P1)"*; `Amount-input` line 9: *"itinerary row 17 (P1), banking-critical"*.

**The defect is the itinerary, not the components.** `reviews/ITINERARY-2026-07-14-apollo-component-library.xlsx`
is dated **2026-07-14** and still marks rows 17/19/89 `Gap`. It is **stale by five weeks**, and the brief
inherited the staleness. This is `[[premise-ages-faster-than-rule]]` and the #194 carried-COUNT defect in
one: *a carried status is the same class of claim as a carried count, and ages the same way.*

⛔ **I did not correct the itinerary.** It is a shared reviews artefact outside my NEW-files-only fence,
and component status is promotion-adjacent — the DO-NOT-RULE list names "component promotion of any kind".
**Dave's.** Flagged to the conductor below.

**Consequence, stated plainly:** Lane C had no build work. Rebuilding three gated components as
`-v2` files would have been three invented defects for nothing — exactly `[[specimen-starts-from-reference]]`,
the #202 failure. So the lane was re-pointed at what was genuinely missing and genuinely in-fence: the
**four-theme review surfaces**, which no one had ever made for the fintech trio, plus a real audit of the
three against the Wave-3 §5 rule set (which post-dates their 2026-07-22 build).

---

## Deliverables — 3 NEW files, all inside the §4 fence

| File | State |
|---|---|
| `reviews/REVIEW-203-amount-display-four-themes-v1.html` | NEW — 4 themes × light/dark, 42,703 B |
| `reviews/REVIEW-203-amount-input-four-themes-v1.html` | NEW — 4 themes × light/dark, 39,670 B |
| `reviews/REVIEW-203-secure-entry-four-themes-v1.html` | NEW — 4 themes × light/dark, 51,292 B |

No snippet, meta, token, generator or shared doc was created or edited. `git status --short -- knowledge/`
attribution is below under residuals.

**Specimens are COPIED, never re-drawn** (`[[specimen-starts-from-reference]]`). The component markup in
all 24 panes is the gated snippet body, byte-verbatim, rendered through the generated `canon.css` — the same
grammar as `reviews/REVIEW-174-progress-bar-four-themes-v1.html`. Exactly **three** transforms, each declared:
1. the `<svg>` sprite is hoisted **once** per page (8 copies = 8× duplicate `<symbol>` ids);
2. every id defined in the specimen body is **suffixed per pane**, with `for` / `aria-labelledby` /
   `aria-describedby` / `href="#…"` references rewritten to match (8 panes = 8× duplicate ids otherwise);
3. `<p class="note">` explanatory prose dropped — identical in all 8 panes; the page carries one copy.

**Behaviour `<script>` blocks are NOT carried.** The review surface is a four-theme *visual* compare;
live drive stays in the gated snippet and the showroom. Declared, not silent.

Builder script: `/var/tmp/s203c.py` (throwaway, outside the repo — **0 instrument**, not a thing the repo carries).

---

## Findings — four, every one PROPOSED, none ruled

### 1 · ⛔ `gen_canon_components.py` silently drops dark-mode component rules — 33 rules, 19 of 76 snippets

**The strongest finding of the lane, and a screenshot caught it after every gate went green.**

In the dark panes the error roundel renders **red**. The gated snippet rules it **white shape + black mark**
("policy dark"), and rules the dark error border to go full red. Neither reaches `canon.css`.

Cause, quoted from `knowledge/canon/gen_canon_components.py:76`:

```python
if first in (":root",) or first.startswith("[data-theme"): return True
```

Correct for the harness var blocks (`[data-theme="light"]{--page:#FFF}`); **wrong** for a component rule
that merely happens to be dark-scoped (`[data-theme="dark"] .se-msg .ic{color:#FFFFFF}`). The very next
function, `prefix_selector`, already carries commented machinery for keeping a leading root-ancestor at the
front and scoping the descendant after it — **the drop test fires first, so that machinery never sees these
rules.** The capability exists; the ordering defeats it.

**Blast radius, measured** (`re` over every snippet's `<style>`, counting `[data-theme=…] <descendant>` rules):

```
SNIPPETS with dropped dark/light DESCENDANT rules: 19 of 76
TOTAL rules silently absent from canon.css: 33
  4 Notifications · 3 Form-layout · 3 Input-fields · 2 Amount-input · 2 Date-picker ·
  2 Date-range-picker · 2 Secure-entry · 2 Stepper · 2 Textarea · 2 Time-picker · 4 charts …
```

Lane C's own four: Secure-entry dark error border + white roundel; Amount-input dark error border + white roundel.

⚠ **This touches Lanes A, B and F directly** — Form-layout, Input-fields, Textarea, the date/time pickers
and Stepper are all on the list. Conductor should relay before those lanes' work is reconciled.

**PROPOSED #203 → `_DS-IMPROVEMENTS.md`** (conductor merges; ⛔ I may not edit it):
- **(a)** discriminate the drop — no descendant = var block, drop; has a descendant = scope it via the
  machinery already present;
- **(b)** a gate that **parses the generated partial in its own grammar** and diffs it against its source
  snippet. This is `[[no-gate-parses-the-artefact]]` verbatim: no gate compares a snippet to the partial
  generated *from* it, so 33 rules can vanish with all six gates green.

⛔ Not fixed here — shared generator, explicitly fenced. Dave's / the conductor's.

### 2 · Amount-input: the standard money field is **39px** tall — 5px under the ruled 44px minimum

Measured in a real browser at two widths, not read off CSS:

| surface | @1180px | @480px | 44px min |
|---|---|---|---|
| `.ai-box` standard | 380 × **39** | 457 × **39** | ❌ **FAIL, −5px** |
| `.ai-box.ai-display` | 380 × 75 | 457 × 75 | ✅ |

This is the field a customer taps to enter money on a phone. It has carried this since 2026-07-22 because
**no gate enforces the 44px minimum** — the brief says so itself (§5: *"token exists at base tier; no gate
enforces it"*). Enforced by hand here, as instructed, and it fails.

**PROPOSED:** padding `8px 16px` → `11px 16px` (45px, clears) or `10px 16px` (43px, does not). The choice
changes the field's proportion against its label, so it is a **look** decision, not a maths one. **Dave's.**

### 3 · Secure-entry: OTP cell drops to **42px** wide below 480px — 2px under the minimum

| surface | @1180px | @480px | 44px min |
|---|---|---|---|
| `.se-cell` | 50 × 58 | **42** × 50 | ❌ **FAIL, −2px on width** |
| `.se-btn` (Resend) | 139 × 44 | 139 × 44 | ✅ |

⚠ **Correction against my own first reading.** From the CSS (`canon.css:8249`, `Secure-entry:185`) I first
wrote "40px, 4px under". The **rendered** box is **42px** (40px content + 1px border each side), so it is
**2px** under, not 4px. A number read off a stylesheet is not a measurement — corrected in the review page
before it reached Dave. `[[measure-dont-convert-units]]`.

The narrowest breakpoint is exactly where a one-handed thumb enters an OTP.
**PROPOSED:** narrow cell → `44×48` content (46×50 rendered); clears the minimum and still fits six cells
plus the separator at 320px. **Dave's.**

### 4 · The two-red/green **ink** pair is ruled MONO ONLY, and nothing enforces it

`.cn-amount-display` binds `--success-ink: var(--rag-success-ink)`. Parsed out of `canon.css`:

| token | definitions | where |
|---|---|---|
| `--rag-success-ink` | **2** | `:root` `#137F3C` · `[data-theme="dark"]` `#66CC8D` |
| `--rag-error-ink` | **2** | `:root` `#DA1A00` · `[data-theme="dark"]` `#F6604C` |
| `--rag-success` | **8** | base ×2 + legacy `#00847F` · console/supercharge `#5DAC7B`, each ×2 |
| `--rag-error` | **8** | base ×2 + legacy `#A8000B` · console/supercharge `#B92F1E`, each ×2 |

The asymmetry is **correct** — `s151-D1` rules the ink pair MONO ONLY. But the cascade has no mechanism to
*enforce* mono-only, so the mono green renders unchanged in all four themes. **Driven, not inferred**, with a
control built in:

```
THEME         MODE   positive-seat colour   pane background
mono          light  rgb(19,127,60)         rgb(255,255,255)
legacy        light  rgb(19,127,60)         rgb(255,255,255)
console       light  rgb(19,127,60)         rgb(255,255,255)
supercharge   light  rgb(19,127,60)         rgb(247,246,244)   <- ground DID change
supercharge   dark   rgb(102,204,141)       rgb(19,17,14)      <- ground DID change
```

**The control is the Supercharge page ground.** It changes (`#F7F6F4` / `#13110E`), proving the theme
cascade is live on the page — so the unchanged ink is a real token gap, not a broken review harness. Under
Legacy the mono `#137F3C` sits beside a theme whose own success colour is the teal `#00847F`.

**It is a class, not one component:** `--rag-*-ink` has **four** consumers in `canon.css` —
`--success-ink` (this atom), `--error-atom`, and the sparkline `--spark-up` / `--spark-down` — none fenced.

**PROPOSED:** a fence, so a mono-only ink resolves to something theme-legal outside mono.
⛔ **NOT proposed:** re-legging `rag/*-ink` per theme — that would reopen `s151-D1`, and the two-red law is
on the untouchable list. **Dave's, and only Dave's.**

---

## Gates — every rc reported, attribution proved

⚠ **Scope, declared honestly first:** the brief says *"filtered to your own files"*. My files are
`reviews/*.html`, and **no gate's glob reaches `reviews/`** — `_validate_type_composites.py:245-246` globs
`knowledge/snippets/*.html` + `knowledge/_proforma/*.html` only. So my three files contribute **0 by scope,
not by cleanliness** (`[[gate-glob-scope-rule]]`). I therefore ran the gates whole-population, to attribute
the tree's state rather than to grade myself, and hand-checked my own files separately.

| Gate | rc | Reading |
|---|---|---|
| `_validate_snippets.py` | **1** | 18 ❌, **all `--pri-hover` DRIFT** in Modals/Stepper etc. **PRE-EXISTING, none mine** — `grep -i 'amount\|secure' ` over the output is **empty**. This is the #198/#199 `--pri-hover` workstream, red at HEAD. |
| `_validate_a11y.py` | **0** | 76 snippets, **0 failures**, 179 warnings, 145 notes. Clean. |
| `_validate_type_composites.py` | **1** | **1097** violations across 90/91 files (TYPE-001 ×31 · TYPE-002 ×1050 · TYPE-003 ×16). Ratchet is shrink-only and **held**. |
| `_validate_state_contrast.py` | — | **NOT RUN — declared gap.** Exceeds the call cap on 76 snippets (#174 hit the same wall) and a filtered run *overwrites* the tracked audit artefact. Left to the conductor / a longer runner. |
| `_validate_radius.py` | — | **Not run** — `MIGRATED_SNIPPETS` is on the ⛔ shared-file list and I added no snippet. |
| `gen_* --check` | — | **Not run.** No generated output should change: I added no snippet or meta. Expect my `reviews/` files to be absent from generated indexes — **that is the fence working.** |
| `_build_all.py` | — | ⛔ **NOT RUN**, per §4. |

⚠ **The type-gate debt reads 1097, not the 1,101 carried in memory.** Shrink-only is satisfied (1097 < 1101),
but the standing figure is **4 stale**. Same class as the itinerary above and #194's standing-44: *a carried
count is a claim, and it ages.* Conductor may want to re-stamp it.

**Pre-existing type debt in Lane C's own snippets** (quoted from the gate, **not mine, not fixed**):
`Amount-display` — `TYPE-003 font: 13px (off-ramp) [.stateLabel]`. **13px is off the sanctioned
12/14/16/20/32/40/52 scale**, the same species as the 11px #202 caught. Plus TYPE-002 raw declarations in
`h2.sec` / `p.note` / `.gallery .cap` across all three, which **do** survive into `canon.css`
(`.cn-amount-input h2.sec{font:500 16px/1.3 …}` etc.). Surfaced, not swapped.

**My own files:** hand-probed for raw type — **0 raw `font-size` / `font:` declarations** in my page CSS;
all review chrome sits on `.t-cm-*` / `.t-ed-*` composites. Verified by regex over each page's `<head>`.

---

## Render proof — `goto("file://…")`, never `set_content()`

**Font asserted with controls, never `fonts.check()`** (canvas width, 40px `Handgloves 12345`):

| probe | width | reading |
|---|---|---|
| `HSBC_MtUnivers_Latin` | **347** | the real cut |
| `"Univers Next HSBC"` (type.css `--uf`) | **347** | alias lands |
| `"Univers Next for HSBC"` (snippet `--font`) | **347** | alias lands |
| `DejaVu Sans` — control | 375 | genuinely different face |
| nonexistent face — control | 301 | default fallback |

Matches the runbook's recorded table exactly. Both aliases on target, both controls differ ⇒ no silent fallback.

- Rendered and **seen** at **1180px** and **480px/700px** — `[[feedback-review-live-variant-spread]]`.
- Crops read (smallest crop carrying the verdict, per the runbook's price-the-instrument note): Legacy pair,
  Supercharge OTP pair, Console pair. The Legacy/Console crops are what make finding 4 visible to the eye;
  the Supercharge OTP crop is what exposed finding 1.
- Responsive proved numerically: `.grid` computes to a **single 668px column at 700px** (stacks, not squeezes).
- Structure proved by parsing each output in its own grammar: **4 themes × 8 panes × 8 `.cn-` scopes, 0
  duplicate ids, 0 dangling `for`/`aria-labelledby`/`aria-describedby`/`href="#"` references** — on all three.
- Tree asserted clean: **0** `.uuid` fontconfig strays in the TTF dir (symlink-farm recipe, `#138`).

**A first render was rejected by eye and rebuilt.** Stacked state labels crowded the specimens above them —
leading-trim is ON, so a vertical stack needs an explicit tokenised gap (gated-component runbook, vertical
rhythm). Fixed in *my* chrome (`margin:24px 0 8px`), regenerated, re-shot, re-read.

---

## Residuals — declared, not glossed

- ⚠ **Running the gates modified three tracked shared files**: `knowledge/_REVIEW-SIGNOFF.md`,
  `knowledge/_SNIPPET-AUDIT.md`, `knowledge/_graph-mark-observations.jsonl`. These are **gate side-effect
  artefacts** — `_validate_snippets` / `_validate_a11y` write them on every run (#174 hit this identically).
  **I did not author them and I did not restore them:** `git checkout/restore` is ⛔ banned by §4 and is
  precisely how #202's sub destroyed uncommitted work. ⚠ **Five sibling lanes are live in this tree and are
  also running gates**, so I *cannot* attribute these diffs to myself alone and will not claim to.
  **Conductor: reconcile these three paths deliberately at merge — do not blind `git add -A`.**
- **No context-gauge stamp** — reasoning above; the instrument writes to a shared rolling file mid-parallel-run.
- **`_validate_state_contrast.py` unrun** over the population — priced TODO, owed to CI or a longer runner.
- **Behaviour not carried into the review pages** — deliberate, declared above. If Dave wants to *drive* OTP
  auto-advance across four themes, that is a v2 and it needs per-pane script scoping.
- **The itinerary is still wrong.** Rows 17/19/89 still say `Gap`. Untouched by design.
- ⬛ **UNPROVEN BY SCOPE:** I did not verify whether the other 15 `REVIEW-203-*` files now in `reviews/`
  (other lanes') collide with mine. Filenames are slug-unique, so collision is unlikely, not proven.

## For the conductor to merge

1. **`_DS-IMPROVEMENTS.md`** — finding 1, both halves (discriminate the drop; a partial-vs-snippet parse gate).
   ⚠ **Relay to Lanes A / B / F before reconcile** — their components are on the 33-rule list.
2. **`_DS-IMPROVEMENTS.md`** — finding 4, the unfenced mono-only ink class (4 consumers).
3. **A 44px hit-area gate** — findings 2 and 3 are both invisible to every existing gate. Two shipped gated
   components are under the minimum; there will be more.
4. **Itinerary rows 17 / 19 / 89** — `Gap` → built-2026-07-22. **Dave's call**, flagged not made.
5. **Re-stamp the type-composite debt** — memory carries 1,101; the gate measures **1097**.
6. **No CATEGORIES entry needed** — I added no component.

## Decisions needed from Dave

| # | Decision | Default if he says nothing |
|---|---|---|
| 1 | Amount-input box padding — `11px 16px` (45px, clears 44) vs `10px 16px` (43px, does not) | stays 39px, under the minimum |
| 2 | Secure-entry narrow cell → `44×48`? | stays 42px at ≤480px |
| 3 | Fence the mono-only `rag/*-ink` seat, or accept the mono green in all four themes? | mono green keeps leaking into Legacy/Console/SC |
| 4 | Fix `gen_canon_components`' drop test, and gate snippet-vs-partial? | 33 rules stay silently absent |
| 5 | Correct the itinerary's stale `Gap` rows (promotion-adjacent — DO-NOT-RULE) | itinerary keeps mis-briefing future waves |
| 6 | `Amount-display`'s off-ramp `13px .stateLabel` | stays off-scale |

## Friction log

1. **The brief's premise was false for this whole lane**, and only step 0 caught it. Had I trusted it,
   I would have re-drawn three good components as `-v2` — #202's exact failure, at 3× scale. **Step 0 is the
   single highest-value instruction in that brief.**
2. **A carried STATUS ages exactly like a carried COUNT.** The itinerary (5 weeks stale) and the memory hook's
   "1,101" (4 stale) are the same defect wearing different clothes.
3. **The screenshot beat the gates.** Six gates green; a crop of the Supercharge dark pane exposed 33 missing
   rules. `[[green-tests-cannot-see-scope]]`, one more time.
4. **My own CSS reading was wrong by 2px** and the render corrected it before it reached Dave. Read boxes,
   don't read stylesheets.
5. **The gates mutate the tree.** Running a read-shaped instrument dirtied three tracked files — with six
   lanes live, that is a reconcile hazard nobody priced in the brief.
6. **`/var/tmp` farms all survived** (`pw-browsers-s197`, `chromelibs`, `pylibs-s203e`) — the render recipe
   needed no download. Runbook worked verbatim; ~2 calls to first pixel.
