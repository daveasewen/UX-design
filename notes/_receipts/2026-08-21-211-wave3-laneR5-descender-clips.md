# #211 findings-repair wave 3 — LANE R5 receipt: three input descender-clip repairs, same shape as R3

**Brief:** conductor's wave-3 lane brief (chat-issued); playbook `notes/_receipts/2026-08-21-211-wave1-laneR3-a11y-repairs.md`
(lane R3, repair (c), Form-layout) — the exact same defect class, reused verbatim.
**Repo HEAD at lane open and close:** `652d432` (`after #211 2026-08-21 — the [45] canon layer repaired…`)
**— NO COMMIT MADE.**
**Files touched — three, all inside the fence:** `knowledge/snippets/Multi-select.reference.html` ·
`knowledge/snippets/Tags-input.reference.html` · `knowledge/snippets/Combobox.reference.html`.
**Diffstat:** `3 files changed, 24 insertions(+), 0 deletions(-)` — 8 lines each (comment + one rule),
byte-identical shape to R3's Form-layout repair.
No gate threshold, constant or count was moved. No token was minted, swapped, lightened or invented.
No `git commit`, no `git checkout`, no `_build_all.py`. `_validate_partials.py` and `_validate_radius.py`
were **not run at all** (R3's own trap, § 4d of the playbook — avoided by not invoking either).

**Render environment** (`knowledge/_RUNBOOK-render-verify.md`, symlink farm #138) — **reused R3's staged
environment on `/var/tmp`, unchanged, nothing re-downloaded:**
`PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-s197` · `PYTHONPATH=/var/tmp/pylibs` ·
`FONTCONFIG_FILE=/var/tmp/fonts-s211R3.conf` (farm `/var/tmp/fonts-s211R3`, `<include>` present) ·
`TMPDIR=/var/tmp` · `LD_LIBRARY_PATH=/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu` (needed this
lane — the first launch failed `libXdamage.so.1: cannot open shared object file` until this was set;
R3's own receipt does not carry it explicitly but the fix is the standard #138/#161 lib set).
**Tree assertion:** `ls -a knowledge/assets/fonts/_desktop/TTF | grep -c '^\.uuid'` → **0** — no
font-cache stray entered the tree (see `git status --short` verbatim at § 5).

**Instrument reused verbatim, not reinvented:** R3's own working script survived on disk at
`/sessions/loving-dreamy-wright/mnt/outputs/_r3_pixel_descender.py` and was read, then copied
byte-for-byte into `/var/tmp/_r5_pixel_descender.py` with one addition — `REPO` reads from env var
`R5_REPO` so the same instrument can be pointed at a staged HEAD tree or the live repo, instead of
being hand-retyped. Same probe string (`pygmy jonquil`), same 4× device-scale ink-row analysis, same
mutation (`text-box-trim:none`), same ink-mask threshold (`d > 60`).

---

## 1 · THE THREE REPAIRS, IN ONE TABLE

| # | file | selector fixed | BEFORE (measured, HEAD) | AFTER (measured, repaired) | how proven |
|---|---|---|---|---|---|
| (a) | `Multi-select.reference.html` | `#ms1-input` (4 inputs share the rule) | box **32px**, `cap alphabetic`, ink **47** dev-px @4×, bottom row **148px** (flat cut), mutation control grows ink by **3.25 CSS px** | box **32px** (unchanged), `text`, ink **60**, bottom row **36px** (tapered), mutation control now moves ink by **0.00 px** | `_r5_pixel_descender.py` against `git show HEAD:` (staged symlink tree) vs the repaired working file |
| (b) | `Tags-input.reference.html` | `#ti1-input` | box **32px**, `cap alphabetic`, ink **47**, bottom row **147px**, mutation grows ink by **3.25 CSS px** | box **32px** (unchanged), `text`, ink **60**, bottom row **36px**, mutation moves ink by **0.00 px** | same instrument, same two runs |
| (c) | `Combobox.reference.html` | `#cb1-input` | box **21px**, `cap alphabetic`, ink **47**, bottom row **148px**, mutation grows ink by **3.25 CSS px** ⚠ *(brief cited 2.75 — see § 4 discrepancy note)* | box **21px** (unchanged), `text`, ink **60**, bottom row **36px**, mutation moves ink by **0.00 px** | same instrument, same two runs |

**In every case, AFTER is byte-identical to the `text-box-trim:none` ground truth** (ink 60 / bottom-row
36 / mutation delta 0.00) — the same outcome R3 recorded for Form-layout and Date-picker.

---

## 2 · THE REPAIR SHAPE — identical to R3's, per file

Each file's `.<prefix>-box input` rule was `0-1-1` and lost to the #209 trim block's `0-1-2`
(`:is()` takes its highest arg — `input[type=text]` = `0-1-1` — plus `svg` inside `:not(:has())` =
`0-0-1`). Each file already wraps its box in a class-bearing ancestor (`.ms`, `.ti`, `.cb`), and each
file **already used the two-class idiom** for its own state rules before this lane touched it:

| file | pre-existing two-class precedent (grep on the HEAD copy) | new rule | new specificity |
|---|---|---|---|
| Multi-select | `.ms.is-error .ms-box` — 2 hits | `.ms .ms-box input{text-box-edge:text text;}` | `0-2-1` |
| Tags-input | `.ti.is-error .ti-box` — 2 hits | `.ti .ti-box input{text-box-edge:text text;}` | `0-2-1` |
| Combobox | `.cb.is-completed .cb-box input` — 1 hit (an even closer precedent: same three-part shape, just scoped to one state) | `.cb .cb-box input{text-box-edge:text text;}` | `0-2-1` |

**Ancestor coverage is universal in every file** (every `.<prefix>-box` sits inside a `.<prefix>`
element, so the fix reaches every state, not just the live specimen):

| file | `.<prefix>` count | `.<prefix>-box` count |
|---|---|---|
| Multi-select | 4 (`ms`, `ms is-disabled`, `ms is-error`, `ms summary`) | 4 |
| Tags-input | 5 (`ti`×2, `ti is-disabled`, `ti is-error`×2) | 5 |
| Combobox | 5 (`cb`, `cb underline`, `cb is-completed`, `cb is-disabled`, `cb is-error`) | 5 |

Nothing in the `#209` leading-trim `:is(...)` block moved. The ds-005 cross-file class remedy stays
Dave's, exactly as R3's playbook required — this lane applied three more instances of the same local,
per-file override, nothing more.

---

## 3 · CLAIM TABLE — every mechanical claim carries its probeable token (`s182-D1`)

Probe staged at `/var/tmp/_r5_pixel_descender.py` (NON-REPO: session outputs mount, `s191-D2` marker —
a lane instrument, not a library artefact; re-runnable with `R5_REPO=<root>` + the env block above).
HEAD comparison tree staged at `/var/tmp/r5head/` — a symlink farm mirroring `knowledge/*` except
`knowledge/snippets/{Multi-select,Tags-input,Combobox}.reference.html`, which are `git show HEAD:`
byte copies (verified 0 occurrences of the repair string before, matching the working tree's 1
occurrence each — § 5).

| # | claim | probeable token | verdict |
|---|---|---|---|
| 1 | Each defect reproduces exactly as R3's §4c table recorded box height and computed edge | `R5_REPO=/var/tmp/r5head python3 /var/tmp/_r5_pixel_descender.py '[["Multi-select.reference.html","#ms1-input"],["Tags-input.reference.html","#ti1-input"],["Combobox.reference.html","#cb1-input"]]'` → `boxH 32/32/21`, `edge "cap alphabetic"` all three | ✅ **DRIVEN** |
| 2 | Each defect is a rendered CUT, not a computed-style opinion — mutation-proven | same run: `text-box-trim:none` mutation grows ink by **3.25 / 3.25 / 3.25 CSS px** (13 dev-px / 4×) on all three | ✅ **MUTATION-PROVEN** |
| 3 | Each repair restores the glyphs EXACTLY to the untrimmed truth | `R5_REPO=<real repo>` run on the repaired working tree: **inkH 60, bottomRowInk 36** on all three — identical to R3's Form-layout `text-box-trim:none` control figures — and the mutation now moves ink by **0.00 px** on all three | ✅ **DRIVEN + CONTROLLED** |
| 4 | Each repair is a SPECIFICITY fix, and the declaration is proven to have WON | computed `text-box-edge` read back off the live element: `cap alphabetic` → `text`, all three | ✅ **DRIVEN** |
| 5 | Each repair uses the idiom the file ALREADY uses, and its ancestor is universal | grep counts § 2: precedent idiom present (2/2/1 hits) before this lane touched the file; ancestor:box coverage is 4:4, 5:5, 5:5 | ✅ |
| 6 | The repair changes ONLY the ds-005 input leg — the trim block itself is untouched | `diff` on all three files shows only the 8-line insertion (comment + one rule) between the existing `input{...}` rule and its `::placeholder` neighbour; `grep -c ':is(button,a,label'` unchanged at 1 per file, byte-identical to HEAD | ✅ **CONTROLLED** |
| 7 | ⛔ The type ratchet did NOT move — the shrink-only debt is untouched | `python3 knowledge/_validate_type_composites.py` on the three repaired files → `TYPE GATE PASS … (3 file(s))`. Same gate on the `git show HEAD:` copies staged at `/var/tmp/r5head/` → `TYPE GATE PASS … (3 file(s))`. Identical verdict, pre-existing and post-repair | ✅ **CONTROLLED** |
| 8 | Box heights did not move | `boxH` read back by the same probe: **32/32/21 both before and after** — the repair changes only what edge the glyph is measured against, never the box | ✅ **DRIVEN** |
| 9 | The gates that cover these files are green after the repairs | `_validate_descender_clip.py` → `PASS … (151 file(s))` rc 0 (same population count R3 recorded) · `_validate_snippets.py` → `135 snippet(s), 0 failure(s)` rc 0 (same count R3 recorded) · `_validate_a11y.py` → `0 failure(s)` rc 0 · `_validate_css_governed.py` rc 0 · `_validate_behaviour.py` rc 0 · `_validate_no_hardcode.py` rc 0 — all run WITHOUT file arguments (build mode), per the playbook's named trap | ✅ |
| 10 | No font-cache stray entered the tree | `ls -a knowledge/assets/fonts/_desktop/TTF \| grep -c '^\.uuid'` → **0** | ✅ |
| 11 | `_validate_partials.py` / `_validate_radius.py` were never run, so their tracked census files cannot have been narrowed by this lane | not invoked at all this lane; `git status --short` (§ 5) shows neither `_PARTIALS-GATE.md` nor `_RADIUS-GATE.md` dirty | ✅ **AVOIDED, NOT JUST REVERTED** |
| 12 | ⛔ `knowledge/gen_component_partials.py` is dirty but NOT this lane's | `git diff knowledge/gen_component_partials.py` header reads `# ------------------------------------------------------------------ comment mask (#211 lane R6)` — a sibling lane's own attribution, in its own diff, never touched by an Edit call in this lane | ⬛ **NOT THIS LANE'S** |

---

## 4 · ⚠ ONE FIGURE IN THE BRIEF DID NOT REPRODUCE — DECLARED, NOT SMOOTHED

The brief's own table (from R3's §4c) records Combobox at **2.75 CSS px** cut. This lane's
independent re-run of R3's own `_pixel_descender.py` shape, same probe string, same 4× scale, same
threshold, against the same HEAD bytes, measured **3.25 CSS px** — identical to Multi-select and
Tags-input, not 0.5 px less. Two candidate explanations, neither confirmed:

1. R3's §4c table may have been produced by a **different** one of R3's four probe scripts (its own
   receipt names `_r3_probe_inputs.py` and `_r3_probe_inputs2.py` as siblings alongside
   `_r3_pixel_descender.py` — the survivors on disk — and the glyph-bounds "twin span" method in
   `_r3_probe_inputs2.py` measures sub-CSS-pixel via `getBoundingClientRect()`, not a 4×-scaled ink
   mask quantised to 0.25 CSS px steps, so it can land on a different fractional value for the same
   underlying cut).
2. A genuine one-device-pixel difference in how Chromium anti-aliases the descender of this specific
   font/box-height combination at the ink-mask threshold used (`d > 60`), which would show up as a
   ±0.25 CSS px wobble at the boundary.

**This lane does not adjudicate between them.** What is DRIVEN, twice, independently, is that
Combobox's `#cb1-input` **was cut** before the repair and **is not cut** after it, matching R3's
qualitative finding exactly; only the precise magnitude of the prior cut is in question, and by at
most half a CSS pixel. Reported as a priced TODO, not resolved by picking the more convenient number.

---

## 5 · `git status --short` — VERBATIM, at lane close

```
 M knowledge/gen_component_partials.py
 M knowledge/snippets/Combobox.reference.html
 M knowledge/snippets/Multi-select.reference.html
 M knowledge/snippets/Tags-input.reference.html
```

Every path attributed, none swept:

| path | whose | why it is dirty |
|---|---|---|
| `knowledge/snippets/Multi-select.reference.html` | **R5 — mine** | the `.ms .ms-box input{text-box-edge:text text;}` repair + its comment |
| `knowledge/snippets/Tags-input.reference.html` | **R5 — mine** | the `.ti .ti-box input{text-box-edge:text text;}` repair + its comment |
| `knowledge/snippets/Combobox.reference.html` | **R5 — mine** | the `.cb .cb-box input{text-box-edge:text text;}` repair + its comment |
| `knowledge/gen_component_partials.py` | **sibling — lane R6** | its own diff header self-attributes `#211 lane R6`; never opened or edited by this lane (claim 12) |

No gate side effect to declare: `_validate_partials.py` and `_validate_radius.py` were never invoked,
so `_PARTIALS-GATE.md` / `_RADIUS-GATE.md` are not in the status above and needed no revert.

---

## 6 · WHAT IS DRIVEN AND WHAT STAYS UNPROVEN

**DRIVEN** — all three repairs, mutation-proven before (ink grows under `trim:none`) and controlled
after (ink no longer moves), computed `text-box-edge` read back off the live element, box heights and
the type ratchet confirmed unchanged, all six cross-cutting gates green in build mode.

**UNPROVEN, declared, each one a priced TODO — same shape R3 declared, extended to these three files:**

1. ⬛ **Only mono was rendered.** All three files hardcode `[data-theme]` blocks like Form-layout;
   nobody has looked at Multi-select, Tags-input or Combobox in legacy, console or supercharge for
   this repair. The token consumed (`text-box-edge` is a layout property, not a themed colour) makes
   a per-theme divergence unlikely, but it was not rendered.
2. ⬛ **Only the first live specimen per file was driven** (`#ms1-input`, `#ti1-input`, `#cb1-input`).
   Ancestor-coverage math (§ 2) proves the CSS rule reaches all 4/5/5 instances per file; the disabled,
   error and completed-state inputs were not individually screenshotted.
3. ⬛ **No screen reader was run.** This is a purely visual/layout repair; nothing here touches ARIA,
   focus order or announced text, and R3's a11y gate figure (`0 failure(s)`) is unchanged, but that is
   a mechanical proof, not a heard one.
4. ⬛ **The Combobox 2.75-vs-3.25 discrepancy (§ 4) is not resolved**, only declared with two named
   candidate causes.
5. ⬛ **The 3.25/2.75 px figures are cuts on THIS face at 16px**, exactly as R3 declared for
   Form-layout — not a constant, a measurement of one font/size/box combination.
6. ⬛ `_validate_hit_area.py` and `_validate_state_contrast.py` were **not run** this lane (out of
   scope for a `text-box-edge` repair that touches no geometry and no colour) — carried forward as
   R3 carried them, not re-declared as new gaps.

---

## 7 · DO-NOT-RULE ITEMS THIS LANE BRUSHED — returned PRICED, none settled

1. **ds-005 class choice (trim-block specificity vs single-class override) — DAVE'S, untouched.**
   This lane applied three MORE instances of the same local, per-file two-class override R3 used,
   using each file's OWN existing idiom (§ 2). It did not touch the `:is(…)` trim block, did not
   lower its specificity, and did not choose a cross-file remedy. **Five gated snippets now carry
   the input leg fix (Date-picker, Form-layout from R3; Multi-select, Tags-input, Combobox from this
   lane) — R3's §4c table is now fully closed, all three of its "live" rows repaired.** The cross-file
   decision is exactly as open as it was at mint.
2. **ANY new tint, hue or grey — DAVE'S.** None proposed, none touched. This repair is
   `text-box-edge` only; no colour, mark or red was approached.
3. **ANY gate threshold, constant or count — DAVE'S.** None moved. The descender gate, the type
   ratchet, the a11y gate and every other gate run this lane are byte-identical in configuration to
   what R3 ran; only the input files changed.
4. **The 34 proposed organisms + the REVIEW-210/211 pages** were not opened.
5. **P-6 / P-7 / P-8 promotion or park** — not this lane's; not touched, not run.

---

## 8 · CONSEQUENCES AND PITFALLS — mandatory (Dave #165)

**What could recur, and where.**

1. **The ds-005 class recurs in every NEW text-bearing `<input>` composed against a tight box.**
   R3 named the predicate from data: an input is cut when the trim is enacted (`cap alphabetic`) AND
   its box is tight (≤ ~32px). This lane's three repairs close the last three snippets R3 had
   measured live at mint — but nothing GATES the class. A sixth snippet built tomorrow with a ≤32px
   input box will clip identically and silently, because (per R3's § 3) the descender gate's
   population never contains an `<input>` at all. **That instrument gap is still open**; this lane
   fixed instances, not the blindness that let them recur three more times.
2. **This repair is a LOCAL override, not a systemic one — by design, per the fence.** If a future
   snippet copies `.ms-box`/`.ti-box`/`.cb-box`'s markup without also copying the two-class ancestor
   wrap, the fix does not travel with the copy. The comment left in each file says so inline, exactly
   as R3's did.
3. **The Combobox figure discrepancy (§ 4) could recur as a false confidence signal** if a future lane
   quotes a magnitude from a brief without re-measuring. This lane re-measured and found a different
   number for the SAME underlying defect on the SAME bytes — the qualitative finding held, the
   quantitative one did not reproduce exactly. Future magnitude citations from this receipt should be
   re-run, not retyped.
4. **What this lane's repairs do NOT do.** They add no gate, promote no probe, retire no finding and
   settle nothing that was Dave's. Three files moved by 24 lines total. The wider question — the
   ds-005 cross-file remedy, and the descender gate's blindness to `<input>` entirely — is returned
   open and priced, not closed by implication, exactly as R3 left it.

---

## 9 · SUB SPEND

Lane R5 ran as a single sub in one window, doing the work directly (reading the playbook, applying
three CSS edits, reusing and re-running R3's surviving instrument, running six build-mode gates).
**No sub-delegation from this lane: subs 0 tokens (n=0).** The conductor should count this lane as
**n=1**.
