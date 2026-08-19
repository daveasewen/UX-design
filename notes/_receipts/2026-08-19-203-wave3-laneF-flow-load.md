# Receipt — #203 Wave 3, Lane F · flow & load (Skeleton loader · File upload · Stepper)

*Worker receipt per `_BRIEF-wave3-foundations-2026-08-19-v1.md` and the parallel-conductor checklist.*
*Written 2026-08-19 against HEAD `ec2336d`.*
*⛔ Nothing here is a ruling. No commit, no push, no git state command of any kind.
`knowledge/_rulings.json` untouched. No shared file edited. No generator that rewrites shared
outputs was run. `_build_all.py` NOT run.*

**Gauge at close** — `knowledge/_checkin.py`, run first-hand: FILL **108,667 real**
(`message.usage`, last turn, a floor) · boot **56,488** · peak 108,667 over 18 turns ·
room to the advisory stop line 150,929 = **42,262**. Throughput 121,080 real (gauge.count, one
call — NOT comparable to FILL). Seam clear, integrity digest matched, no UNKNOWN.

---

## 0 · The headline, before anything else

**All three of Lane F's components already existed.** The brief sent me to build them from nothing
on the strength of the itinerary spreadsheet marking each one `Status = Gap`. That column is
**stale**. I verified it by hand before writing a line, and I did **not** rebuild anything —
rebuilding would have destroyed working, gated, ruled-into components (the #202 lesson, from the
other direction).

What I did instead is the work that genuinely had never been done, all of it inside the fence:
the **four-theme review surfaces** for Dave's eye, and the **`role="progressbar"` reconcile** the
brief named as Lane F's specific technical job — which turned out to be a real, measurable,
visible divergence.

## 1 · Step 0 — the premise, verified first-hand

| Claim inherited from the brief | Verified? | Evidence (probe named) |
|---|---|---|
| HEAD is unstated in brief | HEAD = `ec2336d` (#202 wrap) | `git log --oneline -1` |
| Skeleton loader (row 72) is a P1 **Gap** | **FALSE** | `ls knowledge/snippets/` → `Skeleton-loader.reference.html` (158 lines, has `#token-manifest`) + `knowledge/components/skeleton-loader.meta.json`. Last touched `0fb104a` (#121). |
| File upload (row 18) is a P1 **Gap** | **FALSE** | `File-upload.reference.html` (441 lines) + meta. The meta's own `purpose` reads *"Itinerary row 18 (P1); built Phase-2 wave 2 (worker A continuation)."* Last touched `f091769` (#151). |
| Stepper interactive (row 34) is a P1 **Gap** | **FALSE** | `Stepper.reference.html` (463 lines) + meta. `purpose` reads *"Itinerary row 34 (P1); built Phase-2 wave 2 (worker A continuation)."* Last touched `2d2ff44` (#178). |
| Itinerary carries "20 P1 gaps" | **22 P1 rows**, all but two marked `Gap`/`Partial` | parsed `reviews/ITINERARY-2026-07-14-apollo-component-library.xlsx` sheet `Itinerary` with openpyxl; 22 rows at `Priority == P1` |
| Type-composite debt is **1,101** | **STALE — measures 1,097** | `python3 knowledge/_validate_type_composites.py` → `TYPE GATE FAIL — 1097 violation(s) across 90/91 file(s)` |
| Stepper: "Progress-tracker is display-only and GATED — copy its grammar, add interaction" | ✅ TRUE, and **already done** | `stepper.meta.json` `purpose` + variants describe exactly this; `Progress-tracker.meta.json` is `interactive:false` |
| File-upload improvises `role="progressbar"` (#174) | ✅ TRUE, quoted | `File-upload.reference.html:291` and `:404` |

**A stale spreadsheet column is a premise, and premises age faster than rules**
[[premise-ages-faster-than-rule]]. The carried count (1,101 → 1,097) is the same defect in
miniature — a COUNT is not a MEASUREMENT.

⚠ **This almost certainly affects other lanes.** A whole-itinerary sweep of the 22 P1 rows found
snippet + meta already present for rows 14, 15, 16, 18, 20, 34, 51, 54, 68, 69, 70, 71, 72, 90 —
and rows 17, 19, 52, 89 also exist under different slugs (`amount-input`, `secure-entry`,
`stat-card`, `amount-display`), which my first slug match missed and I am declaring rather than
asserting either way. **Genuinely absent** on the same probe: rows 13 (form layout — though
`form-layout.meta.json` exists), 53, 63, 86. The conductor should re-price Wave 3 on this.

## 2 · The reconcile — Lane F's actual technical job, done and measured

The brief: *"File-upload snippet already improvises `role="progressbar"` (#174 finding) —
reconcile with gated Progress-bar."*

**Gated `Progress-bar` contract** (`requiredAria` in its manifest): `role="progressbar"` ·
`aria-valuenow` · `aria-valuemin` · `aria-valuemax` · **`aria-valuetext`** · `aria-labelledby`.
Tokens: track `progress/incomplete`, fill `progress/complete`, radius `border-radius/indicator`.

### 2a · Stepper — already reconciled. No action.

`Stepper.reference.html:165–166` binds `--incomplete: progress/incomplete` and
`--step-fill: step/complete`, binds `var(--border-radius-indicator)`, and `:262–263` carries
`aria-valuetext="Step 1 of 4"`. It matches `Progress-tracker`'s grammar. **The Stepper is the
well-behaved one.** Its one divergence from Progress-bar — `aria-valuemin="1"`/`aria-valuemax="4"`
counting *steps* rather than 0–100 *percent* — I judge correct and am recording as a **deliberate
documented divergence**, PROPOSED, not resolved (see §5).

### 2b · File-upload — genuinely diverges. Three counts, all measured.

`.fu-bar` at `File-upload.reference.html:182–183`:
```
.fu-bar{height:4px; background:var(--field-bg-hover); ...}     /* form/background/hover */
.fu-bar b{... background:var(--text); ...}                     /* text/default */
```

**1 · Token bindings are wrong even where the pixels agree.** Fill is bound to `text/default`, not
`progress/complete`. Resolved from generated `canon.css` across all four themes × both modes, the
two **coincide in all eight legs today** — so nothing looks wrong. But `progress/complete` has
already *moved once* (`s175-D1` sent the reds to `step/complete`), and File-upload would not have
followed. Latent, not live. Stated as latent deliberately — a matched value is not a proof of
correctness.

**2 · The track diverges live, in all four dark modes.** Resolved from `canon.css`, then
**confirmed in the browser** by reading `getComputedStyle` off the rendered review page (values
below are the browser's, not my arithmetic):

| Theme / mode | Gated track | File-upload track | fill-on-track (gated → FU) |
|---|---|---|---|
| Mono light | `#F0F0F0` | `#F0F0F0` | 15.27 → 15.27 |
| **Mono dark** | `#484848` | **`#232323`** | 9.15 → 15.72 |
| Legacy light | `#F0F0F0` | `#F0F0F0` | 11.09 → 11.09 |
| **Legacy dark** | `#484848` | **`#232323`** | 9.15 → 15.72 |
| Console light | `#F0F0F0` | `#F0F0F0` | 15.27 → 15.27 |
| **Console dark** | `#484848` | **`#232323`** | 9.15 → 15.72 |
| Supercharge light | `#DFDEDC` | `#DFDEDC` | 14.02 → 14.02 |
| **Supercharge dark** | `#413934` | **`#2E2A25`** | 10.46 → 13.19 |

**3 · And it compounds into something a user would actually feel.** Fill-on-track *improves*, so a
naive read says "harmless". The number that matters is **track vs the page it sits on** — that is
what tells you how much is *left*:

| | gated Progress bar | File-upload bar |
|---|---|---|
| Mono / Legacy / Console dark | **1.90:1** | **1.11:1** |
| Supercharge dark | **1.67:1** | **1.32:1** |

At 1.11:1 the track is effectively invisible: you see the fill, you cannot see where it *ends*.
Neither clears 3:1, and the gated bar is fine with that **because it always prints a number beside
itself and always carries `aria-valuetext`**. The File-upload bar does **neither** — no visible
percentage, and `aria-valuetext` is absent from the markup *and* from its manifest `requiredAria`
(which lists `role`/`aria-valuenow`/`aria-live`/`aria-describedby`, omitting even the `valuemin`
and `valuemax` the markup does carry). So on a dark-mode upload row the bar is the sole carrier of
progress and it is the weakest of the three possible carriers. **That compounding is the finding —
not the token mismatch on its own.**

⛔ Not fixed. Fixing means editing `File-upload.reference.html`, which is outside the NEW-files-only
fence, and the remedy is a design call, not a bug fix (see §5).

## 3 · Deliverables

| File | State |
|---|---|
| `reviews/REVIEW-203-skeleton-loader-four-themes-v1.html` | NEW — 8 theme panes + 2 narrow + live frame |
| `reviews/REVIEW-203-file-upload-four-themes-v1.html` | NEW — same, plus the measured reconcile table + swatches |
| `reviews/REVIEW-203-stepper-four-themes-v1.html` | NEW — same, two flow states per pane |
| `notes/_receipts/2026-08-19-203-wave3-laneF-flow-load.md` | NEW — this file |

Built by copying the approved `REVIEW-174-progress-bar-four-themes-v1.html` grammar
[[specimen-starts-from-reference]]: snippet body inlined into `.cn-<slug>` under
`[data-apollo-theme]` × `[data-theme]`, rendered through the generated `canon.css`. No snippet, meta,
token, generator or shared file was touched. Generator lived at `/var/tmp/s203F/mkreview.py` —
outside the repo, throwaway, not an instrument the repo carries.

## 4 · Gates — every rc reported

Baseline measured before I created anything; since I created only `reviews/*` and one receipt,
baseline and after are identical by construction, and that is the point.

| Gate | Baseline (HEAD `ec2336d`) | After | Verdict |
|---|---|---|---|
| `_validate_snippets.py` | **rc=1** · 76 snippets, **18 failures** | rc=1 · 18 failures | ⚠ **RED AT HEAD, pre-existing** — see §4a |
| `_validate_a11y.py` | rc=0 · 76 snippets, 0 failures, 179 warnings | rc=0, unchanged | ✅ |
| `_validate_type_composites.py` | **rc=1** · **1,097** across 90/91 files | rc=1 · 1,097 | ✅ ratchet held; my new files contribute **0** (`reviews/` is not in the gate's scope — declared, not assumed: `grep -c 'reviews/'` on the gate output = 0) |
| `_validate_state_contrast.py` | not run | not run | ⬛ **DECLARED GAP** — exceeded the call cap on the full 76-snippet population at #174 and I did not re-attempt it; it also writes a shared audit `.md`, which is outside my fence |
| `_validate_radius.py` | not run | not run | ⬛ **DECLARED GAP** — it writes shared `_RADIUS-GATE.md`; and my files add no snippet, so `MIGRATED_SNIPPETS` needs no entry |
| `gen_showroom --check` etc. | not run | not run | ⬛ **DECLARED GAP**, left to the conductor's single reconcile |

⛔ `_build_all.py` NOT run. ⛔ No generator that rewrites shared outputs was run.

### 4a · `_validate_snippets.py` is RED at HEAD — 18 failures, one defect, nine files, no owner

**This is not Lane F's doing and it is not Lane F's to fix**, but every lane will hit it and a lane
reporting "snippet gate green" is reporting something that cannot be true. All 18 are the identical
defect:

```
❌ <file>: DRIFT --pri-hover (light) = #626262 but button/primary/background/hover = #636363
❌ <file>: DRIFT --pri-hover (dark)  = #B7B7B7 but button/primary/background/hover = #B2B2B2
```

Nine files: `Action-bar` · `Button` · `Confirmation` · **`Drawer`** (Lane D) · **`Empty-state`**
(Lane E) · **`Form-layout`** (Lane A) · `Icon-button` · `Modals` · **`Stepper`** (Lane F).

This is the `--pri-hover` mint from #198 (`s198-D1`/`s198-D2`) and the #199 rename landing in the
token store without these nine snippets following it — the *"alias-repoint can strip a theme's
override silently"* hazard, arriving from the other direction. It is one value per file, it spans
four lanes, and it belongs to the conductor. Visually it is a few units on a button hover.

## 5 · Decisions needed — Dave's, every one PROPOSED

Per `s202-D3` each is carried with its store search — **run, and quoted, not asserted**. Probes:
`python3 knowledge/_memento_search.py` on `"pri-hover"`, `"file upload progress bar"`,
`"progressbar valuetext"`, `"skeleton contrast pairs"`; plus a direct parse of
`knowledge/_rulings.json` for `pri-hover` · `progressbar` · `valuetext` · `fu-bar` · `skeleton`.

What the store returned:

- **`--pri-hover` is RULED and the drift is a consequence, not a new question.** `s198-D1` — *"THE
  STORED --pri-hover COLOUR-EQUIVALENTS RE-DERIVE AT THE LIVE ALPHA 0.68"* — and `s198-D2` — *"THE
  TWO RE-DERIVED --pri-hover VALUES GET MINTED PRIMITIVES"* (#198, Dave). The nine snippets carry
  the **pre-mint** values. Sharper still: **`ds-032` (#106, Dave) already warned about exactly this
  shape** — *"--alpha-68 is APPROVED for --pri-hover, but the ruling is scoped to the BUTTON ATOM,
  not to eight per-component [copies]"*. Nine per-component copies is what then drifted. So §4a is
  not a new finding so much as the predicted cost arriving. **Not mine to rule; do not re-put it to
  Dave as an open question** [[dont-launder-a-premise-into-a-ruling]].
- **`valuetext` → 0 hits. `fu-bar` → 0 hits.** No ruling governs the File-upload bar's bindings or
  its ARIA contract, so item 1 below is genuinely open.
- **`progressbar` → 1 hit, `s173-D1`** (#173, Dave) — the ruling that made Progress-bar the first
  component through the scaffold route, determinate only. It does **not** speak to step-counting
  vs percent, so item 2 is genuinely open.
- ⚠ **Scope of the probe, honestly:** these were default-depth searches, not `--all`.
  [[retrieval-default-hides-the-ruling]] says the default can hide a ruling, so treat "genuinely
  open" above as *not-found-at-default-depth*, not as proven-absent.

1. **The File-upload bar — rebind, or rule the divergence correct?** Proposed remedy: bind
   `.fu-bar` to `progress/incomplete` + `progress/complete` + `border-radius/indicator`, add
   `aria-valuetext`, add a visible percentage. **The counter-argument is real:** an upload row is
   field furniture, and the lighter `form/background/hover` track may be the *right* reading inside
   a form. A progress bar in a field may simply not be the same object as a progress bar on a page.
   Design call. Dave's. Nothing changed.
2. **Stepper's step-counting `progressbar`** (`aria-valuemin="1"`/`valuemax="4"`) vs Progress-bar's
   percent 0–100. I judge it correct — it matches Progress-tracker, and "Step 2 of 4" is what a
   screen reader should say in a flow. PROPOSED as a **deliberate, documented divergence** rather
   than an inconsistency to iron out.
3. **Skeleton-loader declares zero `contrastPairs`.** Defensible under 1.4.11 (bones are
   `aria-hidden` decorative placeholders), but it means **no gate can ever fail on the bone
   colour** — a green that cannot fail [[gate-inside-the-growth-loop]]. Dave's eye on the
   Supercharge and Legacy dark panes: are the bones still readable as *structure*?
4. **Stepper's completed-step fill reads RED in Legacy.** `step/complete` aliases `rag/success`
   (the #176 roundel chain) and Legacy overrides it to the primary red. Ruled inheritance, not a
   mistake — but red-for-done deserves a look, and red is a problem hue for Dave
   [[colour-stability-red-yellow-problem]]. Visible in the Legacy panes of the Stepper review page.
5. **Wave 3's premise.** Lane F's three rows were not gaps. The conductor should re-price the wave
   before more lanes spend on rebuilds. Not mine to rule.

## 6 · Proposals for the conductor to merge

- ⛔ **Do not let me or any lane edit these** — listed for the conductor's single reconcile:
  - **`knowledge/_DS-IMPROVEMENTS.md`**: the `--pri-hover` nine-file drift (§4a) as one gated
    class, not nine tickets. Candidate gate: the snippet gate already *catches* it — what is
    missing is anything that makes a token mint **fan out** to its consuming snippets. That is the
    `no-gate-parses-the-artefact` shape: the mint had no consumer.
  - **`knowledge/_DS-IMPROVEMENTS.md`**: `Skeleton-loader.reference.html` fails `TYPE-001` — it
    **does not pull `canon/type.css`** (the only one of my three; `File-upload` and `Stepper` both
    do). One-line fix, outside my fence. Its headings visibly render in the browser serif default.
  - **`knowledge/_DS-IMPROVEMENTS.md`**: the File-upload progress-bar reconcile (§2b), queued
    behind Dave's decision #1 — do not enact it as a tidy-up.
- **Itinerary**: `reviews/ITINERARY-...xlsx` `Status` column is stale for at least rows 14–16, 18,
  20, 34, 51, 54, 68–72, 90. Correcting it is a shared-file edit and is **not** mine.
- **No new tokens proposed.** No `CATEGORIES` entry needed — I added no component.

## 7 · Friction log

- **The brief's central premise was false for my entire lane.** Step 0 caught it in the first two
  probes. Had I trusted the brief I would have written three duplicate components over three
  working ones. The receipt-with-a-premise-table discipline from #174 is what earned this.
- **A static review pane cannot review the Stepper — and no gate can tell you that.** The Stepper's
  dots are drawn by script: `<ol class="steps" id="st-steps">` is **empty in the file**. My first
  render produced eight panes with no dots at all and I only caught it *by eye*, exactly as
  [[green-tests-cannot-see-scope]] predicts. Fixed by driving the real snippet in Chromium and
  inlining the **post-JS DOM** at two flow states, so Dave sees done + current + upcoming together.
- **Driving the component surfaced a second fact for free:** clicking Next twice only advanced one
  step (`aria-valuenow` = 2). That is the validation gate working, not a bug — the amount field is
  required. Worth knowing that the Stepper's headline feature is live and correct.
- **I shipped invalid CSS to myself and the render caught it.** The page template used `{{ }}`
  brace-escapes intended for `str.format()` but was consumed by `str.replace()`, so every emitted
  rule read `body{{...}}`. Result: no pane borders, no two-column grid, panes full-bleed. Nothing
  errored; it simply looked wrong. **A crash is not a fail, and neither is silence.**
- **`--demo-width` defaults to 520px, which is exactly the `@container (max-width:520px)` collapse
  threshold** — so every "wide" pane would have shown the *collapsed* form and Dave would never
  have seen the dots grammar the brief asked me to inspect. Forced to 760px wide / 420px narrow.
- A third layout defect (grid columns auto-expanding on a 760px specimen, clipping the dark pane)
  was caught the same way. Three separate defects in my own deliverable, all invisible to gates,
  all caught by looking. Final state asserted numerically: 10 panes each, 10/10 bordered,
  **0 clipped**, no page overflow, **0 duplicate ids**, 80 dots / 180 bones / 10 bars rendered.

## 8 · Render proof

`goto("file://…")` throughout; `set_content()` never used. Symlink-farm fontconfig per
`_RUNBOOK-render-verify.md` §SYMLINK FARM, with the `<include>` present.

Font asserted with **controls, not a boolean** — 40px `Handgloves 12345`, canvas measurement,
identical on all three pages:

| probe | reading |
|---|---|
| `HSBC_MtUnivers_Latin` | **347** |
| `"Univers Next HSBC"` (type.css alias) | **347** |
| `"Univers Next for HSBC"` (snippet alias) | **347** |
| `DejaVu Sans` — control | 375 |
| nonexistent face — control | 301 |

Both aliases land on the target and on neither control ⇒ the real HSBC cut, no silent fallback.
Tree asserted after every render run: `ls -a knowledge/assets/fonts/_desktop/TTF/ | grep -c '^\.uuid'`
→ **0**; `git status --short --untracked-files=all` shows only new `reviews/REVIEW-203-*` files and
receipts (mine and other lanes'), no strays of mine.

Seen by eye, not merely asserted: Mono and Legacy Stepper sections (dots, ring, check, and the
Legacy red), the narrow collapse at 420px, and the File-upload Mono light/dark section (dropzone,
drag-over, disabled, and the three row states).

## 9 · Residuals — declared, not glossed

- `_validate_state_contrast.py` and `_validate_radius.py` **not run** (§4). Both write shared
  audit files; the first also exceeded the call cap on the full population at #174. Owed to the
  conductor or a longer runner.
- **The 44px min-hit-area rule was not enforceable by me.** No gate covers it, and the interactive
  targets live in `File-upload` and `Stepper` — existing files I may not edit. I did *observe*
  that `File-upload`'s remove control is a **24px** button (`fu-remove`, and the a11y gate reports
  107 marks below 24 across the corpus). **UNPROVEN whether its padded hit box reaches 44px** — I
  did not measure the box, so I am not claiming either way. Priced TODO, not a finding.
- The `reviews/` directory is **not** in the type gate's scope. My pages therefore contribute 0 to
  the 1,097 by exclusion rather than by virtue. Declared so nobody reads it as a green.
- The live-behaviour `<iframe>` on each review page shows the real snippet, which hard-codes the
  **Mono** values in its own `<style>`. It is therefore **Mono-only by construction** — the four
  themes are only visible via the static `.cn-*` panes. Said on the page itself, not just here.
- `/var/tmp/s203F/` (generator, render scripts, PNGs) and
  `mnt/outputs/s203F-renders/` (crops read back for the eye check) are **outside the repo** and
  are not repo artefacts [[non-repo-home-or-declare]] — `(NON-REPO: sandbox /var/tmp and the
  session outputs mount)`.
- `knowledge/_REVIEW-SIGNOFF.md`, `knowledge/_graph-mark-observations.jsonl`,
  `notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl` show as modified in
  `git status`. **Not mine** — present before I started; my `_checkin.py` run appends to the
  rehearsal log by design. Flagged so the conductor does not attribute them to Lane F.

`machinery: 0 instrument / 0 feature` — no gate, checker or harness was built, and no component
code was added. The three review surfaces are Dave's decision surface, which is the deliverable
[[review-layer-product-feature]].
