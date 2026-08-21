# #211 findings-repair wave 1 — LANE R3 receipt: three component repairs, ruled tokens only

**Brief:** `notes/_briefs/2026-08-21-211-findings-repair-wave1-v1.md` § LANE R3
**Repo HEAD at lane open and close:** `fc6b35d` — **NO COMMIT MADE** (conductor's serial, per the fence).
**Files touched — three, all inside the fence:** `knowledge/snippets/Date-picker.reference.html` ·
`knowledge/snippets/Drawer.reference.html` · `knowledge/snippets/Form-layout.reference.html`.
**Diffstat:** `3 files changed, 38 insertions(+), 3 deletions(-)`.
No gate threshold, constant or count was moved. No token was minted, swapped, lightened or invented.
No `git commit`, no `git checkout`, no `_build_all.py`. The 34 proposed organisms and the REVIEW-210
pages were not opened.

**Render environment** (`knowledge/_RUNBOOK-render-verify.md`, symlink farm #138):
`PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-s197` · `PYTHONPATH=/var/tmp/pylibs` ·
`FONTCONFIG_FILE=/var/tmp/fonts-s211R3.conf` (farm `/var/tmp/fonts-s211R3`, cachedir
`/var/tmp/fccache-s211R3`, `<include>` present) · `TMPDIR=/var/tmp`.
**Font assertion is a CONTROL, not a boolean** (canvas widths of `Handgloves 12345` @40px):
`HSBC_MtUnivers_Latin` **347** · `"Univers Next HSBC"` **347** · `"Univers Next for HSBC"` **347** ·
`DejaVu Sans` **375** · nonexistent face **301**. Both aliases land on the target and on neither
control ⇒ the real HSBC cut rendered, no silent fallback.
**Tree assertion:** `ls -a knowledge/assets/fonts/_desktop/TTF | grep -c '^\.uuid'` → **0**; no
font-cache stray entered the tree (see `git status --short` verbatim at § 6).

---

## 1 · THE THREE REPAIRS, IN ONE TABLE

| # | defect | BEFORE (measured) | AFTER (measured) | how proven |
|---|---|---|---|---|
| **(a)** | Date-picker `today + selected` ring invisible | ring `rgb(0,0,0)` on cell `rgb(26,26,26)` = **1.21:1** light · ring `rgb(255,255,255)` on `rgb(255,255,255)` = **1.00:1** dark | ring `rgb(255,255,255)` on `rgb(26,26,26)` = **17.40:1** light · ring `rgb(26,26,26)` on `rgb(255,255,255)` = **17.40:1** dark | driven through the real user path (open → click today → reopen), computed `boxShadow` + `backgroundColor` read off the live cell, ratio computed from the RGB; both themes; regression controls on the three neighbouring states; 8× crop looked at |
| **(b)** | modal drawer: two-frame visibility + inert-before-focus | **3 consecutive frames** with `activeElement = BODY` **while `page.inert === true`** and the sheet still `visibility:hidden` (`t0-postclick · rAF1 · rAF2`, sheet visible only at `rAF3`, focus only at `rAF4`) — all four arms | **0 such frames.** Focus stays on the trigger through the settle, then lands in the sheet at `rAF2`, the exact frame the sheet computes `visible`; inert set in that same frame — all four arms | frame-by-frame `getComputedStyle(sheet).visibility` + `document.activeElement` + `page.inert`, at light/dark × 1180/420; **mutation control:** a 200 ms main-thread stall on the same click |
| **(c)** | `<input>` descender clip the descender gate cannot see | **3.25 CSS px of every descender cut flat**: ink height **47** device px @4×, bottom ink row **148 px wide** (a flat cut), computed `text-box-edge: cap alphabetic`; at 6× "pygmy jonquil" renders **"pvamv ionauil"** | **0.00 px cut**: ink height **60** device px, bottom ink row **36 px** (tapered glyph tips) — *byte-identical to the no-trim control* — computed `text-box-edge: text`; at 6× it renders **"pygmy jonquil"** | rendered glyph bounds from an element screenshot at 4×/6×, ink-mask row profile; **mutation control** in both directions; two crops read by eye |

---

## 2 · CLAIM TABLE — every mechanical claim carries its probeable token (`s182-D1`)

Probe scripts are staged at `/sessions/loving-dreamy-wright/mnt/outputs/_r3_*.py` (NON-REPO:
session outputs mount, `s191-D2` marker — they are lane instruments, not library artefacts;
each is re-runnable with the env block above).

| # | claim | probeable token | verdict |
|---|---|---|---|
| 1 | The (a) defect reproduces EXACTLY as #210 wave-4 lane A claim 2 recorded it | `python3 _r3_probe_dp.py` on `git show HEAD:knowledge/snippets/Date-picker.reference.html` → `light … ringVsBg 1.21`, `dark … ringVsBg 1.0` | ✅ **DRIVEN** |
| 2 | The (a) repair reaches contrast in both themes | same probe, repaired file → `light ring [255,255,255] bg [26,26,26] ratio 17.4` · `dark ring [26,26,26] bg [255,255,255] ratio 17.4` | ✅ **DRIVEN** |
| 3 | The (a) repair uses an EXISTING ruled token already consumed by that very selector | the rule is `box-shadow:inset 0 0 0 2px var(--page)`; `--page` is bound to `background/default` in this file's own `token-manifest`, and `.dp-day[aria-selected="true"]` already sets `color:var(--page)`. `grep -c '"--page": "background/default"' knowledge/snippets/Date-picker.reference.html` → **1** | ✅ **NO NEW TOKEN** |
| 4 | …and that pair is already a DECLARED contrast pair of this component | `token-manifest.contrastPairs` contains `{ "fg": "background/default", "bg": "text/default", "context": "text" }` — it was there before this lane | ✅ |
| 5 | The (a) repair holds in ALL FOUR THEMES, light and dark | `background/default` vs `text/default` resolved from `knowledge/tokens/semantic-colour.json` + the three `knowledge/tokens/themes/*.overrides.json`: **mono 17.4/17.4 · legacy 17.4/17.4 · console 17.4/17.4 · supercharge 17.4/17.4** | ✅ **TOKEN-LAYER PROVEN** · ⬛ see § 5 for what this does NOT prove |
| 6 | The (a) repair changes ONLY the intersection — three regression controls | driven on the live grid: **today-not-selected** ring unchanged (`--border-active`: 21.0:1 light, 17.4:1 dark) · **selected-not-today** unchanged (knockout, `boxShadow:none`, ink 17.4:1) · **plain day** unchanged (`boxShadow:none`) | ✅ **CONTROLLED** |
| 7 | The (b) defect is a real window, not a theory | frame log, all four arms: `t0-postclick:hidden/BODY/inert=true \| rAF1:hidden/BODY/inert=true \| rAF2:hidden/BODY/inert=true \| rAF3:visible/BODY \| rAF4:visible/close` | ✅ **DRIVEN** |
| 8 | ★★ …and the test CAN FAIL — the defect is REPRODUCED, not inferred | `python3 _r3_drawer_mutation.py` against HEAD: a 200 ms main-thread stall registered on the same click ⇒ **`motion=no-preference stall=200ms → NO - focus stranded on BODY`** and **`motion=reduce stall=200ms → NO`**. The drawer opens, is inert, and has **no keyboard entry point** | ✅ **MUTATION-PROVEN** |
| 9 | The (b) repair survives that same mutation | same probe, repaired file: **all four arms `KEYBOARD_ENTRY_POINT: YES`**, `active: close`, `activeInSheet: true`, `sheetVisibility: visible`, `pageInert: true` | ✅ **MUTATION-CONTROLLED** |
| 10 | The (b) repair removes the stranded-focus window entirely | frame log after, all four arms: `t0-postclick:hidden/open/inert=false \| rAF1:hidden/open/inert=false \| rAF2:visible/close/inert=true` — **no frame has focus on BODY, and inert is never set before focus is inside** | ✅ **DRIVEN** |
| 11 | The (b) repair does not disturb tab order, the trap, Esc, or focus return | real `keyboard.press('Tab')` ×6 from the landed focus → `['act','cancel','close','act','cancel','close']` (DOM order, wraps) · `tabbableOutside: 0` while open · Escape → `active: open`, `tabbableOutside: 4`, `sheetOpen: false` — identical before and after, all four arms | ✅ **CONTROLLED** |
| 12 | The (c) defect is a rendered CUT, not a computed-style opinion | `python3 _r3_pixel_descender.py` on `#f-name` @4×: ink rows `top 29 / bottom 75`, **inkH 47**, **bottomRowInk 148** (a flat, full-width cut). Mutation `text-box-trim:none` → `bottom 88`, **inkH 60**, **bottomRowInk 36** (tapered tips) ⇒ **3.25 CSS px was being cut** | ✅ **MUTATION-PROVEN** |
| 13 | …and a human can see it | 6× crops read in-session: `r3-BEFORE-input-crop.png` renders **"pvamv ionauil"**, `r3-AFTER-input-crop.png` renders **"pygmy jonquil"** | ✅ **LOOKED AT** |
| 14 | The (c) repair restores the glyphs EXACTLY to the untrimmed truth | repaired file: **inkH 60, bottomRowInk 36** — identical to the `text-box-trim:none` control — and the `trim:none` mutation now moves the ink by **0.00 px**, i.e. the probe that could fail no longer can | ✅ **DRIVEN + CONTROLLED** |
| 15 | The (c) repair is a SPECIFICITY fix, and the declaration is proven to have WON | computed `text-box-edge` read back off the live element: **`cap alphabetic` → `text`**. The rule is `.fl-group .fl-box input` = **0-2-1** against the #209 trim block's **0-1-2** (`:is()` takes its highest arg `input[type=text]` = 0-1-1, plus `svg` inside `:not(:has())`) | ✅ **DRIVEN** |
| 16 | The (c) repair uses the idiom the file ALREADY uses, and its ancestor is universal | `git show HEAD:knowledge/snippets/Form-layout.reference.html \| grep -c '\.fl-group[.a-z-]* \.fl-box input'` → **2** (`.fl-group.is-completed .fl-box input` and `.fl-group.is-error .fl-box input` — both predate this lane). Ancestor coverage: `class="fl-box"` : `class="fl-group…"` = **10 : 10**, so `.fl-group` wraps every field — the selector is universal, not lucky | ✅ |
| 17 | ⛔ **The type ratchet did NOT move** — the shrink-only debt is untouched | `python3 knowledge/_validate_type_composites.py` on the three files → `TYPE GATE FAIL — 21 violation(s) … TYPE-002 ×21`. **Same gate, same day, on `git show HEAD:` copies staged at `/var/tmp/r3head/` → `21 violation(s) … TYPE-002 ×21`.** Identical: pre-existing, not introduced | ✅ **CONTROLLED** |
| 18 | The gates that cover these files are green after the repairs | `_validate_descender_clip.py` (build mode) → `PASS … (151 file(s))` rc 0 · `_validate_snippets.py` → `135 snippet(s), 0 failure(s)` rc 0 · `_validate_a11y.py` → `0 failure(s)` rc 0 · `_validate_css_governed.py` rc 0 · `_validate_behaviour.py` rc 0 · `_validate_no_hardcode.py` rc 0 | ✅ |
| 19 | P-7 did not move (wave 1 does not touch it) | `python3 knowledge/_probe_registry/probe_container_self_query.py --check` → `PROBE P-7 — findings=6` · premise table at mint: **6** | ✅ **UNCHANGED** |
| 20 | ⛔ **P-8 is lane R1's; this lane did not run it and reports no delta for it** | declared, not measured | ⬛ **NOT THIS LANE'S** |

---

## 3 · (c) — WHY THE GATE MISSED IT, NAMED EXACTLY

Three separate blindnesses, in the order they bite. This is the section the brief asks for, and
the third one is a **NEW finding this lane did not go looking for**.

**(i) The gate's population never contains an `<input>`.** `knowledge/_validate_descender_clip.py`
triggers on one signal — `ELLIPSIS = re.compile(r"text-overflow\s*:\s*ellipsis")` — and its own
docstring says so: *"`text-overflow:ellipsis` is the high-precision signal for 'visible truncating
text label'."* An `<input>` never declares `text-overflow:ellipsis`; it clips because it is a form
control with its own single-line inner editor whose overflow the UA owns. So the rule that cuts the
glyphs is **not in the set the gate examines at all**. #210 wave-6 lane B wrote it as *"it has no
concept of an `<input>` at all"*; this is the mechanism behind that sentence.

**(ii) Even inside its population, the verdict is a STRING MATCH, never a rendered measurement.**
`_norm()` collapses whitespace and compares selector text; `OVR_TEXTBOX` greps for
`text-box-edge:text text` **on the same selector**. It cannot resolve a cascade, so an override
that loses on specificity still reads as present — the ds-005 label class, caught three times
across #210 waves 4/5/6. Not the cause here, but the same family:
[[no-gate-parses-the-artefact]].

**(iii) ⛔⛔ NEW — P-6, the probe named for exactly this, is measuring the wrong organ, and its
green is FALSE ON ITS OWN FIXTURE.** `knowledge/_probe_registry/probe_input_trim_enactment.py` is
the canary for "did the browser start enacting `text-box-trim` inside form controls". Run today, on
the same engine, in the same session:

```
P-6 text-box-trim enactment canary · threshold: shrink >= 1.00 CSS px AND >= 5%
  CONTROL <span>        32.00 →  11.56 px (Δ 20.44, 63.9%) computed='trim-both'
  SUBJECT <input    >   32.00 →  32.00 px (Δ  0.00,  0.0%) computed='trim-both'  INERT (the reviewed state)
  SUBJECT <textarea >   32.00 →  32.00 px (Δ  0.00,  0.0%) computed='trim-both'  INERT (the reviewed state)
  ✅ still inert — the state Dave reviewed at #209 and ruled KEEP on. The authored vocabulary
     changes nothing a user can see, today, in this engine.
PROBE P-6 — findings=0
```

I rebuilt P-6's fixture shape and **measured the ink instead of the box**:

| fixture | box height | ink height @4× | bottom ink row | verdict |
|---|---|---|---|---|
| **P-6's own shape** — `line-height:2` (32px) + trim `cap alphabetic` | **32.00 px, Δ 0.00** | **47** | **148 px — flat cut** | ⛔ **the glyphs ARE being cut, in P-6's own fixture** |
| library shape — `line-height:24px` + trim `cap alphabetic` | 24.00 px, Δ 0.00 | 47 | 148 px — flat cut | ⛔ cut |
| library shape + this lane's repair — `text-box-edge:text text` | 24.00 px | **60** | **36 px — tapered** | ✅ |
| control — `line-height:24px`, **no trim at all** | 24.00 px | **60** | **36 px — tapered** | ✅ ground truth |

**An `<input>` does not shrink its box when it is trimmed. It keeps its box and cuts the ink.**
P-6's threshold (`SHRINK_PX` / `SHRINK_FRAC` on box height) is therefore structurally incapable of
seeing the enactment it exists to catch — its sentence *"the authored vocabulary changes nothing a
user can see, today, in this engine"* is **contradicted by its own fixture, at 4×, in the same
minute**. The claim *"Zero input boxes changed height"* is TRUE; the conclusion drawn from it is
not. That is [[green-tests-cannot-see-scope]] and
[[mutation-tests-the-clause-not-the-feature]] in one instrument.

⛔ **NOTHING WAS DONE ABOUT IT.** P-6 is lane R4's file this wave, and a repair may not dial a gate
threshold (`s208-D1` rider, and the wave-1 DO-NOT-RULE append). It is PRICED at § 4 and returned.

---

## 4 · PRICED, NOT WIRED — the gate extension, and everything this lane brushed that is DAVE'S

### 4a · The gate extension (PRICED — deliberately NOT BUILT)

| option | what it is | cost | reach | risk |
|---|---|---|---|---|
| **A — ink leg on P-6** *(recommended)* | keep P-6's fixture and threshold **exactly as they are**; ADD a second, independently-named verdict that measures **rendered ink** (element screenshot, ink-row profile, compared against a `text-box-trim:none` twin) beside the box-height verdict. Nothing existing is relaxed, narrowed or re-tuned. | ~60 lines + numpy/PIL, already staged in-sandbox; the working instrument is `_r3_pixel_descender.py` | catches the whole class the day it enacts, on any engine | ⚠ needs the pixel leg, i.e. `environment: sandbox-render` — a **DECLARED GAP** in a plain shell, exactly like P-3 |
| **B — `--computed` leg on `_validate_descender_clip.py`** | the leg #210 wave-5 lane B and wave-6 lane B both priced: read the *computed* `text-box-edge` in a browser rather than grepping the declaration | larger; needs a render harness on 151 files | fixes blindness (ii) for labels | ⚠ does **not** fix blindness (i) — an `<input>` is still not in the population, because it has no `text-overflow:ellipsis` to trigger on |
| **C — widen the trigger to `input`** | add `<input>`s to the descender gate's population unconditionally | small | would have flagged these | ⛔ **would fire on every input in the library** including the 46–47 px ones that are NOT cut (§ 4c) — a gate with false positives is a gate people learn to ignore |

⬛ **Note for whoever builds A:** neither `scrollHeight − clientHeight` nor computed `text-box-edge`
alone is a sound predicate, and I have the counter-examples. `scrollHeight−clientHeight` reads
**3** on a *repaired, uncut* input (`24/27`) and **0** on an uncut one — it does not discriminate.
`text-box-edge: cap alphabetic` is present on Data-grid, Command-palette and Search-field inputs
that are **not cut at all**. **Only a rendered-ink comparison separates the cases.** Any cheaper
predicate will ship a false green or a false red; that is the whole lesson of this lane.

### 4b · DO-NOT-RULE items this lane brushed — returned PRICED, none settled

1. **ds-005 class choice (trim-block specificity vs single-class override) — DAVE'S, untouched.**
   This lane applied the **local, per-file two-class override** in two named files, which is what
   every #210 lane did and is a repair. It did **not** touch the `:is(…)` trim block, did not lower
   its specificity, and did not choose the cross-file remedy. The cross-file decision is exactly as
   open as it was at mint — and § 4c below is the number it should be decided against.
2. **P-6 / P-7 / P-8 promotion or park — DAVE'S.** Nothing was promoted. P-6's finding above is a
   **repair-or-park candidate**, not a promotion, and it is the second independent catch of the
   "the instrument measures the wrong organ" shape this wave.
3. **ANY new tint, hue or grey — DAVE'S.** None proposed. Repair (a) reuses `--page`, a token this
   component already declares, already binds and already lists as a contrast pair. The two-red law
   (`#DA1A00`-on-white / `#F6604C`-else) and the mono error ink camp (`#1A1A1A` on `#F6604C`) were
   not approached: nothing in these three repairs touches a red, a green or a mark.
4. **ANY gate threshold, constant or count — DAVE'S.** None moved. P-6's `SHRINK_PX` /
   `SHRINK_FRAC` are byte-identical; the descender gate is byte-identical; the type ratchet's 21
   TYPE-002 violations on these files are identical to HEAD (claim 17).
5. **The 34 proposed organisms + the REVIEW-210 pages** were not opened.

### 4c · ⛔ THREE MORE GATED SNIPPETS ARE CUTTING DESCENDERS TODAY — REPORTED, NOT TOUCHED

Same instrument, same session, same threshold, measured by ink with the repair applied as the
mutation control. **All three are outside this lane's fence.**

| snippet | input | box | computed edge | cut TODAY |
|---|---|---|---|---|
| `Multi-select.reference.html` | `#ms1-input` (×4 in file) | 32 px | `cap alphabetic` | **3.25 CSS px** |
| `Tags-input.reference.html` | `input` | 32 px | `cap alphabetic` | **3.25 CSS px** |
| `Combobox.reference.html` | `input` | 21 px | `cap alphabetic` | **2.75 CSS px** |
| — *repaired by this lane* — | | | | |
| `Form-layout.reference.html` | `#f-name` (10 inputs) | 24 px | **`text`** | **0.00** |
| `Date-picker.reference.html` | `#f-date` (4 inputs) | 24 px | **`text`** | **0.00** |
| — *measured CLEAN, no action needed* — | | | | |
| `Data-grid` `#dgSearch` · `Command-palette` `input` · `Search-field` `input` | | 46–47 px | `cap alphabetic` | **0.00** — the box is tall enough that the re-based line still fits |

**The predicate, from the data:** an input is cut when the trim is enacted (`cap alphabetic`) **and**
its box is tight (≤ ~32 px). At 46–47 px nothing is lost. That is why a blanket "flag every input"
gate (option C) would be wrong, and it is the number the ds-005 class decision should be priced
against: **five gated snippets in the library carry the input leg; two are now repaired, three are
live.**

### 4d · ⛔ A TRAP FOR THE NEXT AGENT, FOUND THE HARD WAY

Running `_validate_partials.py` or `_validate_radius.py` **with explicit file arguments** rewrites
their tracked census files (`knowledge/_PARTIALS-GATE.md`, `knowledge/_RADIUS-GATE.md`) with a
census narrowed to those files — `_RADIUS-GATE.md` flipped from *"✅ STRICT surfaces clean"* to
*"❌ STRICT failures (4)"* purely as an artefact of the narrowed run, not because anything broke.
This lane caused both, noticed both, and **reverted both with `git show HEAD:<path> > <path>`** (the
working revert on this mount; `git checkout` is banned by the fence and cannot restore here anyway).
Verified gone in the verbatim status at § 6. **These two gates are build-mode-only in practice — do
not hand them a file list.**

---

## 5 · WHAT IS DRIVEN AND WHAT STAYS UNPROVEN

**DRIVEN** — all three repairs, both themes where the file has themes, with a mutation control on
(b) and (c) and regression controls on (a); the real HSBC face asserted against two controls; two
crops read by eye.

**UNPROVEN, declared, each one a priced TODO:**

1. ⬛ **The four themes were proven at the TOKEN layer, not by rendering four themed specimens.**
   `Date-picker.reference.html` hardcodes its own `[data-theme="light"]/["dark"]` hex block — it is a
   mono-only artefact and does not consume the theme cascade, so a per-theme render is not reachable
   from the snippet. Claim 5 resolves `background/default` and `text/default` out of
   `semantic-colour.json` + the three `themes/*.overrides.json` and gets **17.40:1 in all eight
   theme×mode combinations**. That proves the TOKEN PAIR, not a rendered console/supercharge
   date-picker. **Nobody has looked at this component in legacy, console or supercharge.**
2. ⬛ **No screen reader was run.** Focus, inertness and tab order were measured programmatically
   (claims 7–11). Nothing was heard. `aria-current="date"` still carries the today semantics, and it
   was left exactly as it was.
3. ⬛ **The (b) repair was driven at 1180 and 420, light and dark, and under
   `prefers-reduced-motion: reduce`. It was NOT driven on a real touch device, nor with a screen
   reader's virtual cursor**, and the `@media (max-width:480px)` `.sheet{width:100%}` arm was
   exercised only at 420.
4. ⬛ **`_validate_hit_area.py` returned `77 COULD-NOT-ASK`** in the gate pass at claim 18 (it
   resolves playwright from its own env and did not see the staged `PYTHONPATH`). That is a third
   verdict, not a pass — **the hit-area question was not asked of these three files.** Date-picker's
   day cells were already an OPEN advisory from #210 (`74 finding(s)`), and this lane did not change
   any geometry, so nothing is expected to have moved. Unverified.
5. ⬛ **`_validate_state_contrast.py` refused** — `rc=2 StateContrastArgError: no snippet matches …
   refusing to write an empty audit`. An honest refusal (it wants snippet NAMES, not paths). The
   state-contrast audit for these files was **not re-run**, and the (a) ring is a `box-shadow`, which
   that gate does not read anyway (#210 wave-4 lane A: *"no gate compares a box-shadow against the
   background it is painted on"* — **still true, and this lane did not fix it**).
6. ⬛ **The 3.25 px figure is the cut on this face at 16 px.** It is a measurement of
   `HSBC_MtUnivers_Latin` at `font-size:16px`, not a constant. A different size or face gives a
   different number.

---

## 6 · `git status --short` — VERBATIM, at lane close

```
 M knowledge/_119-sweep-recheck.json
 M knowledge/_probe_registry/probe_dangling_var_pixel.py
 M knowledge/_probe_registry/probe_input_trim_enactment.py
 M knowledge/gen_token_ramp.py
 M knowledge/snippets/Button.reference.html
 M knowledge/snippets/Chart-butterfly-h.reference.html
 M knowledge/snippets/Date-picker.reference.html
 M knowledge/snippets/Drawer.reference.html
 M knowledge/snippets/Form-layout.reference.html
 M knowledge/snippets/Template-dashboard.reference.html
 M knowledge/snippets/Template-detail.reference.html
 M knowledge/snippets/Template-list-index.reference.html
 M notes/_REHEARSAL-LOG.jsonl
 M notes/_dream/_GRADE-DECISIONS.jsonl
?? notes/_briefs/2026-08-21-211-findings-repair-wave1-v1.md
?? notes/_receipts/2026-08-21-211-wave1-laneR1-token-ramp.md
?? notes/_receipts/2026-08-21-211-wave1-laneR3-a11y-repairs.md
?? notes/_receipts/2026-08-21-211-wave1-laneR4-probe-hygiene.md
```

Every path attributed, none swept:

| path | whose | why it is dirty |
|---|---|---|
| `knowledge/snippets/Date-picker.reference.html` | **R3 — mine** | repair (a) + the in-fence input leg of (c) |
| `knowledge/snippets/Drawer.reference.html` | **R3 — mine** | repair (b) |
| `knowledge/snippets/Form-layout.reference.html` | **R3 — mine** | repair (c) |
| `knowledge/gen_token_ramp.py` · `snippets/Button` · `Chart-butterfly-h` · `Template-dashboard` · `Template-detail` · `Template-list-index` | **LANE R1** | the `gen_token_ramp` comment defect + its regenerated AUTO-TOKENS regions |
| `knowledge/_probe_registry/probe_dangling_var_pixel.py` · `probe_input_trim_enactment.py` | **LANE R4** | P-3 / P-6 crash-to-refusal. ⚠ P-6 is the probe § 3 (iii) reports on — **R3 read it and ran it, and changed NOTHING in it** |
| `knowledge/_119-sweep-recheck.json` · `notes/_REHEARSAL-LOG.jsonl` · `notes/_dream/_GRADE-DECISIONS.jsonl` | **pre-existing at mint** | dirty in the brief's own environment block (`dirty paths: 3`) before any lane ran |
| `notes/_briefs/2026-08-21-211-…-v1.md` | conductor | the brief itself |
| `notes/_receipts/…laneR1-…` · `…laneR4-…` | R1 / R4 | sibling receipts |
| `notes/_receipts/2026-08-21-211-wave1-laneR3-a11y-repairs.md` | **R3 — mine** | this file |

⚠ **Gate side effects, DECLARED and REVERTED, not swept:** `knowledge/_PARTIALS-GATE.md` and
`knowledge/_RADIUS-GATE.md` were rewritten by this lane's gate runs and restored to HEAD bytes —
see § 4d. They are correctly absent from the status above.
⚠ **No `.uuid` font stray entered the tree** (asserted in the header).

---

## 7 · CONSEQUENCES AND PITFALLS — mandatory (Dave #165)

**What could recur, and where.**

1. **The (b) class recurs in EVERY dialog anyone composes.** Show → two frames → focus → inert is
   four steps that must be in that order, and getting it wrong produces a defect that is invisible on
   a fast, idle machine — this file's own BEFORE state passed a naive "does focus land?" check on
   three of four arms and only failed under a 200 ms stall. **A dialog that is only tested unstalled
   is not tested.** The repair carries its reasoning inline in the file so the next composer inherits
   it, but nothing gates it: **no probe in the registry asks "does this dialog have a keyboard entry
   point under load?"** The #210 wave-5 lane A shells and wave-6 lane A shells have the correct order;
   `Modals.reference.html` and `Modal-lightbox.reference.html` were **NOT examined by this lane**
   (out of fence) and are the obvious next place to look.
2. **The (c) class is live in three more gated snippets right now** (§ 4c). This repair fixes two
   files. It does not fix Multi-select, Tags-input or Combobox, and it does not fix whatever the
   templates inherited — #210 wave-6 lane B's own note says `Template-create-edit`, `Template-wizard`
   and `Template-auth` all dropped Form-layout's raw font and bound `.t-cm-input`, and those are in
   Dave's eye queue and were correctly not opened.
3. **The (a) class is unguarded.** There is still **no gate that compares a `box-shadow` against the
   background it is painted on** — the sentence #210 wrote is still true after this repair. Any
   future state that layers a ring over a knockout can reproduce 1.21:1 silently. Repair (a) fixes
   one intersection in one component; the CLASS is open.
4. **The instrument lesson, twice in one lane.** #210 recorded `Form-layout`'s own input as *"box
   24px, nothing clipped"* using `clientHeight`; it was cutting 3.25 px. P-6 records `<input>` as
   *"INERT … changes nothing a user can see"* using box height; its own fixture is cutting. **Both
   are true measurements of the wrong quantity.** Where a defect is about what is PAINTED, the
   instrument must read PAINT — [[no-gate-parses-the-artefact]],
   [[mutation-tests-the-clause-not-the-feature]].
5. **What this lane's repairs do NOT do.** They add no gate, promote no probe, retire no finding and
   settle nothing that was Dave's. Three files moved by 38 lines. Every wider question — the ds-005
   cross-file remedy, P-6's repair-or-park, the box-shadow-vs-background gate, the three live
   snippets — is returned open and priced, not closed by implication.

---

## 8 · SUB SPEND

Lane R3 ran as a single Opus sub in one window. **Approximately 165,000 tokens** of job window
consumed (context at hand-back ≈ 202K of a 1M-token seat, of which the conductor's brief + the #210
material read in at open is the bulk). No sub-delegation from this lane: **subs 0 tokens (n=0)**.
The conductor should count this lane as **n=1**.
