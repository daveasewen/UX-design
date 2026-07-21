# Design-system improvements register

Recommendations for improving the DESIGN SYSTEM itself — findings where our gates fail
not because the engine is wrong but because the published standard has a gap or error.

## Governance (RULED 2026-07-03, Dave)

Nothing is derived-and-promoted on the engine's derivation alone. Promotion into the
token store or canon requires **Dave's judgment, grounded in his knowledge of the design
system**. When a gate failure is essentially an error in the design system, the default
path is: **log the recommendation here, with supporting artifacts, and move on** — no
token or component change. Sometimes Dave will simply decide on the spot; logging is the
default when he doesn't. Derived candidate values recorded here are **evidence, not
canon** — they carry no authority until Dave promotes them.

Entry format: finding · evidence (receipts) · prepared-but-unpromoted candidates ·
blast radius if adopted · artifacts.

---

## ds-001 — dark UI blue: no published dark-legible blue exists (blue/400 leak)

**Status:** LOGGED 2026-07-03 (Dave: log and move on). Current value stands.

**Finding:** dark `focus/ring` + `rag/information` carry #4587A7 — illustration Blue 5
verbatim, never a published UI value (receipted against BOTH the legacy illustration page
and the current 2025 standard, col25-018). It fails 3:1 on #404040 (2.61) and #474747
(2.33), both real adjacencies (form borders; form/background/pressed, tabs hover, two tab
borders in dark). The published standard offers exactly ONE UI blue — RAG #305A85 =
blue/600 — and no dark ramp above it. **The design system has no legal dark-legible UI
blue.**

**Recommendation to the design system:** publish a dark-mode UI blue (a blue/400-class
primitive) derived from the RAG blue ramp. Prepared, unpromoted candidates (hue 210°/
sat 47%, charter §6 method): **#719ECC** (≥3:1 on every dark surface incl. #474747) ·
**#6293C6** (all but #474747 at 2.88; closer to current weight).

**Blast radius if adopted:** colour.json value + 24 snippet manifests (inspect, not
blind-sed) + notifications/tabs meta + canon.css regen + full gate sweep.

**Artifacts:** `_fitness-test/blue400-review.html` (live, switchable, in-situ) ·
`guidelines/colour-usage.md` {#col25-018} (ladder + matrix) ·
`guidelines/illustration-standards.md` §Findings (provenance receipt) ·
`_STATE-CONTRAST-AUDIT.md`.

## ds-002 — dark error text: #DB0011 on #000000 = 4.02:1 at rest

**Status:** LOGGED 2026-07-03 (Dave: log and move on). Current value stands.

**Finding:** rag/error does darken (light #A8000B → dark #DB0011 = color/primary), but
not far enough for TEXT: 4.02:1 on the dark page, 3.71:1 on the error tint, 3.23:1 on
#1D1D1D — all under the 4.5:1 text floor, at rest, wherever dark error text appears
(found on Selection-controls error label + message via the corrected state-contrast
sweep, 2026-07-03). No published red sits above #DB0011, so the standard offers no legal
dark-legible error text. As a GRAPHIC (border, mark, roundel) #DB0011 clears 3:1 — the
gap is text-only.

**Recommendation to the design system:** publish a dark-mode error-text red, or rule the
white-text-with-red-mark pattern (kin to the 2026-07-02 dark roundel policy) for dark
error text. Prepared, unpromoted candidates (hue 355°/sat 100%, charter §6 method):
**#FF3D4C** (≥4.5 on page/tint/surface/form-hover) · #FF3343 · #FF4D5A (also ≥3:1 as a
graphic on #404040).

**Blast radius if adopted:** snippets whose dark theme block carries `--error` for text
+ rag/error token note; graphics keep #DB0011 either way.

**Artifacts:** `_fitness-test/blue400-review.html` §4 (at-rest 4-up + ladder) ·
`_STATE-CONTRAST-AUDIT.md` (Selection-controls, dark) · `tokens/colour.json` (red ramp:
nothing above #DB0011).

**Gate note:** until the standard moves, the state-contrast sweep will keep reporting
the 2 Selection-controls dark text fails — they are this entry's signature, not a
regression. Treat "36/38 clean + ds-002 signature" as the known-good sweep state.

---

## ds-003 — demo-chrome type is not bound to the canon ramp (deferred, not exempt)

**Status:** OPEN — deliberate deferral, Dave ruling 2026-07-18. Logged so it is a known
debt rather than a silent gate exemption.

**Finding:** `_validate_type_composites.py` (DEF-006) gates **component scope only**. The
reference pages carry a second population of text — `.demo-controls` toggle buttons and
harness furniture used to demo component states — which the gate counts but does not
block: **78 raw font declarations** across the 38 snippets, dominated by 13px on
`.demo-controls` and `.demo-controls button`. This scaffolding never reaches a product
screen, so binding it to composites buys nothing at ship time.

**Why it is logged and not just exempted:** the exemption is a **selector-name
convention** (`CHROME_SEL` in the gate). Nothing stops a real component from being named
`.demo-*` and hiding behind it. The exemption is therefore a soft edge on an otherwise
blocking gate, and worth revisiting rather than forgetting.

**Recommendation:** when the reference-page harness is next touched, bind the chrome to
the ramp too and delete `CHROME_SEL` — the gate then has no selector-based carve-out at
all. Until then, treat "component scope green + 78 chrome advisory" as the known-good
state, the same way ds-002 has a signature.

**Blast radius if adopted:** 78 declarations across 38 snippet files; no product surface
changes; no canon.css regeneration needed (chrome is not promoted into canon).

**Artifacts:** `_validate_type_composites.py` (`CHROME_SEL`, advisory line in `run()`) ·
`reviews/TYPE-RETROFIT-2026-07-18.html` §4.

---

## ds-004 — `Fo` unkerned in Univers Regular. **UPSTREAM — do NOT raise with HSBC brand.**

*Logged 2026-07-18. Measured, not inferred.*

**What:** the pair `Fo` carries **zero kerning in Regular (400) only**. Every other weight in the
family kerns it −25 to −30 units. Visible as a slightly loose `Fo` in body-weight text.

**Why it is logged as upstream, with the evidence:** Dave supplied stock **Univers Next Pro**
mid-session, which made a direct comparison possible for the first time. The gap is present in
**stock Univers Next Pro Regular at the identical zero**. It is a Linotype/Monotype omission that
HSBC's commissioned cut inherited — **not something HSBC introduced, and not something they can
fix**. Raising it with brand would waste their time and ours.

**Supporting measurement (same comparison, worth keeping):** HSBC's cut is horizontally
**identical** to stock — sidebearings (LSB *and* RSB) across 75 glyphs × 6 weights, advance widths
across 82 glyphs × 6 weights, and **60/60 exact kerning matches** on ten problem pairs. The single
differing glyph in the entire Latin set is the **ampersand**, deliberately redrawn for HSBC.
Full detail: `_proforma/_TYPE-DECISIONS.md` § T-D3.

**Recommendation:** accept. A single unkerned pair at body weight is below the threshold at which
a manual `letter-spacing` patch would do more harm than good, and patching one pair by hand is
exactly the kind of untracked local override the TYPE-002 retrofit exists to remove. **Log and
move on** — the standing rule for DS defects.

**Blast radius if ever addressed:** none available to us. Would require a re-cut from the foundry.

**Artifacts:** `reviews/UNIVERS-DOSSIER-2026-07-18.html` §3 + §5 · `reviews/gen_univers_dossier.py`.

---

## ds-005 — descender clip on trimmed labels inside icon+label controls. **KEEP — cross-component.**

**Status:** LOGGED 2026-07-18 (Dave: *"a finding we have to keep… it applies to buttons"*). Confirmed
live in the gated Tags component; fix proven on the Tag specimen in real Chromium.
**GATED + CLOSED 2026-07-19** — Dave: *"do it right — use your suggestion"* (gate, don't blanket the CSS)
and *"I don't want other sessions viewing it as a bug and trying to fix it"*. `_validate_descender_clip.py`
is now a blocking build step (27/34): every truncating label (`text-overflow:ellipsis`) must carry
`text-box-edge:text text` (or `overflow:visible`). Day-one-green with ZERO waivers — the full current debt
(7 truncating labels across Tranche-2/3/4/7/8, plus Masthead `.dd-title`/`.navitem-tx`; List-items + canon
were already safe) was fixed, not waived. Removing any override now turns the build red and points back
here — so a cold session cannot "fix" the override away without the gate stopping it.

**Finding.** The canon leading-trim strategy applies `text-box-trim:trim-both; text-box-edge:cap alphabetic`
to label elements. `cap alphabetic` trims the box to cap-height…baseline — which is *exactly* what makes a
label optically centre against an adjacent **icon** (the ✕ in a tag, an icon in a button). BUT when that
same label also carries `overflow:hidden` (for ellipsis), the descender sits **below** the alphabetic
baseline — outside the trimmed box — and is **clipped**. The gated **Tags** component shows this today:
"Savings" renders "Savin*q*s". `leading-trim-label-decision` gotcha 2 named the clip but prescribed
`text-box-edge:text text`; that keeps the glyph box (no clip) but **re-introduces the misalignment** —
`text text` centres the full ascent→descent box, so cap-height text no longer centres on the icon. The two
documented options are therefore **mutually exclusive for the icon+label case**: `cap alphabetic` =
aligned-but-clips; `text text` = unclipped-but-misaligned.

**Resolution (proven, real Chromium).** For **icon+label controls**, keep `cap alphabetic` (icon alignment)
and **don't clip at the label** — set the label `overflow:visible` and let the descender sit in the
control's own vertical slack (a 14px tag in a 30px chip has ~8px); the control's own `overflow:hidden`
still bounds genuine over-length. Trade-off: no per-label ellipsis (fine for short atoms; a control needing
true ellipsis **and** an icon **and** descenders at once needs horizontal-only clipping, which CSS doesn't
do cleanly today — revisit if it arises).

**Decision tree — trimmed truncating labels:**
- Stacked text, NO adjacent icon (List-items `.title/.desc`) → `text-box-edge:text text` (keeps ellipsis, no clip; alignment N/A). *Already applied.*
- Icon+label control (tag, button, CTA, chip) → `cap alphabetic` + label `overflow:visible` into the control's slack. *New.*
- Icon+label control that ALSO TRUNCATES (ellipsis label — nav rows, dropdown titles) → `text-box-edge:text text`. *Added 2026-07-19.* The `overflow:visible` fix above kills the ellipsis, so it's wrong for a truncating label. `text text` keeps `overflow:hidden` (ellipsis survives) AND stops the descender clip (the box now spans the full glyph, so the baseline no longer cuts g/y/p). Cost: the icon-alignment half — `text text` centres the taller box, so cap-height text sits a hair differently against the icon; **acceptable at nav-row scale (44px)**, same trade List-items already took. This resolves the "ellipsis + icon + descenders" trilemma flagged as unsolved above: it is soluble via `text text` when alignment can flex; only unsolved if pixel-perfect icon alignment AND ellipsis AND descenders are all non-negotiable at once.

**Button audit outcome (2026-07-19).** `.btn`/`.cta`/`.qbtn` labels audited (the ds-005 recommendation-3): **CLEAN — null result.** Canonical buttons centre their labels with no `overflow:hidden`, so they carry neither the clip nor the truncation. The live truncating icon+label label was instead in the **Masthead** — `.dd-title` (mobile drawer header): render-confirmed clipping ("Savings"→"Savin*q*s") on the exact selectors, and after the fix `getComputedStyle` reads `text-box-edge:text` + `overflow:hidden` (ellipsis kept). `.navitem-tx` (side-nav row) carries the same CSS condition but is **defined-but-unused in this demo file** (nav labels here render as `.menulink`, which don't truncate — clean); it was fixed defensively so the atom is correct wherever the side-nav variant is instantiated. Build green, 33 steps.

**Blast radius.** Icon+label pairing is pervasive — **24** snippet/tranche files pair an icon with a label
under the global trim. Only those that **truncate** a label (`overflow:hidden` on the label) clip today;
the confirmed live case is **Tags**. **Buttons/CTAs with truncating labels are the next-most-likely** —
audit `.btn/.cta/.qbtn` labels for `overflow:hidden` + descenders. The *alignment* half is already correct
everywhere via `cap alphabetic`; only the *clip* half is the defect.

**Recommendation:** (1) bake the decision tree into the leading-trim canon guidance (extends gotcha 2);
(2) fix Tags at Tag-atom wiring time; (3) audit button labels. **Gate candidate:** render-time check that no
descender is cut inside a trimmed+clipped label (cheap static approximation: trimmed label with
`overflow:hidden` and no `overflow:visible`/`text text` override).

**Artifacts:** `reviews/TAG-COMPONENT-2026-07-18.html` (specimen + fix) · the 5-way alignment comparison
(`outputs/tag-align-test`) · memory `leading-trim-label-decision` (gotcha 2, extended here).

## ds-006 — `_make_review.py` drops snippet review copies INTO the gated `snippets/` dir (2026-07-19)
`_make_review.py` co-locates the review copy next to its source. For a **snippet** source
(`snippets/<X>.reference.html`) the copy lands as `snippets/<X>.reference.REVIEW.html` — inside a dir the
**grid + blast-radius gates scan** (they glob `snippets/*.html`; only the snippet gate uses `*.reference.html`).
The overlay's own chrome (5px/14px padding, extra `.stateLabel`) then reds the build. **Workaround used:** move
the copy to `knowledge/_review/` (no gate scans there), as done for `Amount-display`. **Proper fix:** teach
`out_path()` to send snippet sources to `_review/` too (like `_proforma/` sources), OR have the grid +
blast-radius globs exclude `*.REVIEW.html`. Low effort; do next time `_make_review` is touched.

## ds-007 — R-D17 leak gate misses snippet-RESOLVED Legacy values (2026-07-21, Phase-1 worker B finding 6)
Three Mono surfaces (Action-bar/Modals/Confirmation mirrors + Links arrow + Tabs active) resolved base
`#DB0011` via still-bound pre-ladder roles (`primary/background/default`, `tabs/active`) and the leak gate
stayed green — its scope evidently covers hardcoded hexes/override sets, not what a snippet's bound role
RESOLVES to in the Mono base. Same shape as the declared-pairs contrast blind spot (gates check what's
declared, not what renders). The mirrors were rebound same evening (Dave ruled, worker-B addendum), so the
live instances are gone; the GAP remains for future bindings. **Fix candidate:** extend
`_validate_legacy_leak.py` to resolve every manifest-bound role per snippet against the Mono base and flag
`LEGACY_ONLY_HEXES` resolutions. Do when the ~50-gap fan-out starts (Phase 2) — new components multiply the
exposure.

## ds-008 — `_validate_radius.py` counts prose in HTML comments as declarations (2026-07-21, Phase-1 worker A F0)
`strip_comments` removes CSS `/* */` only, not HTML `<!-- -->` — "border-radius:0" in a snippet's header
prose trips the census (Badge + Tags each carried one). Worker reworded the prose (doc fix); checker logic
untouched (was shared with a live parallel worker). **Fix:** strip HTML comments in `check_text` + extend
the selftest with a prose-trip case. Matters before Phase-2 fan-out (~50 new files will carry header prose).
