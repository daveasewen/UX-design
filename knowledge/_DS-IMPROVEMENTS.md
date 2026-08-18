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
**FIXED + GATED 2026-07-22 (ADR-0013 session):** `strip_comments` now strips HTML `<!-- -->` before CSS
`/* */`; selftest gained the prose-trip bite case. The sibling `_validate_partials.py` gate shipped with
HTML-comment stripping from birth (its selftest case 6 cites this defect).
`strip_comments` removes CSS `/* */` only, not HTML `<!-- -->` — "border-radius:0" in a snippet's header
prose trips the census (Badge + Tags each carried one). Worker reworded the prose (doc fix); checker logic
untouched (was shared with a live parallel worker). **Fix:** strip HTML comments in `check_text` + extend
the selftest with a prose-trip case. Matters before Phase-2 fan-out (~50 new files will carry header prose).

## ds-009 — CONSULT corpus omits `_BUTTON-DECISIONS.md` (2026-07-21, architecture session)
**FIXED 2026-07-22 (ADR-0013 session), stronger than specced:** the corpus is now DISCOVERED —
`parse_rulings()` globs `_proforma/_*-DECISIONS.md` (no hardcoded list to forget), `RULING_ID_RE` is
generic (`[A-Z]{1,3}-D\d+`), and a ledger yielding ZERO records fails the build loudly (the completeness
assertion runs every build, not just on hand-run selftest). Verified live: B-D2/B-D4/B-D6 surface on a
consult query. The secondary cross-vocabulary gap (keyword→fuzzy retrieval) stays a `_FUTURE-STATE` path.
`_build_consult_index.py` indexes the TYPE/RAG/DATAVIZ ledgers + ADRs + guidelines + OPEN items, but
not `_proforma/_BUTTON-DECISIONS.md` — B-D1…B-D5 (Mono primary, disabled visibility, ADR-0009 wiring)
are unfindable via `_consult.py` (verified: a direct B-D1 query returns nothing). Any future ledger
addition repeats this silently. **Fix:** add the ledger to the corpus list + a selftest asserting every
`_proforma/_*-DECISIONS.md` on disk is indexed (catches the NEXT new ledger, not just this one).
Secondary (already a `_FUTURE-STATE` path): keyword retrieval misses cross-vocabulary queries —
"composition/organisms" doesn't reach ADR-0010/0011's "override sets/nullable slots"; fuzzy→rigorous.

## ds-010 — Chart-bar CSS `fill` override collapses ALL bars to series-1 (2026-07-24, legend-prototype render)
**✅ CLOSED 2026-07-26, legend-wave lane ① — fixed AND render-proven.** The offending line was deleted from
`Chart-bar.reference.html` (a comment now sits in its place explaining why a CSS `fill` must never return
there). Proof, at 1180px AND 760px in the licensed HSBC cut, reading `getComputedStyle(rect).fill` per
figure: cb1 single-series purple ✓ · **cb2 horizontal = `rgb(87,124,120)` series-3 teal — DV-D09 restored** ✓ ·
**cb3 status = 4 distinct, `rgb(185,47,30)` #B92F1E red · `rgb(197,137,0)` #C58900 amber · green · blue — the
R-D9 salience ramp restored** ✓ · cb4/cb5 three distinct series each ✓. Before the fix every one of these was
a single purple. *(Same render surfaced the sibling defect [[ds-012]] — the h-bar labels are clipped.)*

*Original entry follows.* **OPEN — surfaced to Dave 2026-07-24 (legend feel session); recommend folding the fix into the bar lane of
the chart wave.** Render-verify of the REAL `knowledge/snippets/Chart-bar.reference.html` (the render that
was standing-OWED and never actually run on these snippets) shows **every bar rendering `--data-series-1`
purple** — grouped column, stacked column, horizontal bar, AND the status chart. Confirmed at 1180px, light,
real HSBC font; screenshot in the session outputs (`REAL_bar.png`).

**Root cause:** `knowledge/snippets/Chart-bar.reference.html` line 102 —
`rect.dv-series{fill:var(--sc,var(--data-series-1));}`. A CSS `fill` property beats an element's
`fill="…"` **presentation attribute** (presentation attributes sit below author CSS in the cascade). Every
bar carries `fill="var(--data-series-N)"` (or `var(--status-breach)` etc.), but `--sc` is **never set on any
rect** (grep `--sc:` → 0 hits), so the rule resolves to the `var(--data-series-1)` fallback for ALL of them.
The `fill` attributes — and with them DV-D09 (horizontal default = series-3) and the R-D9 status salience
ramp (breach/watch/healthy/info) — are dead in render. The donut is UNAFFECTED (`path.dv-series` carries no
`fill` declaration, only `transition`/hover), which is why multi-series colour reads correctly there.

**Why no gate caught it:** `dv-016`/DataViz gate checks the DECLARED tokens + `contrastPairs` manifest
(data/series/1–5 vs background), not what the bars RESOLVE to after CSS overrides the attribute. Same shape
as the declared-pairs contrast blind spot (ds earlier) and [[gate-blindspot-state-contrast]] — checks-passed
≠ renders-right. Render-verify is the only thing that sees it; it had been OWED on every chart handoff.

**Fix (one line):** drop the `fill` declaration from `rect.dv-series` (keep the `transition` on
`rect.dv-series,polygon.dv-series` and the `:hover{filter}`), letting each bar's `fill=` attribute stand.
Verified in `reviews/LEGEND-ISOLATE-TOGGLE-PROTOTYPE-2026-07-24-v3.html` (workaround applied there so the
legend review renders the intended three-colour series). If a CSS-var fill channel is genuinely wanted for
theming, set `--sc` per rect via `style` at generation time instead of a blanket fallback rule.
**Gate follow-up:** the DataViz gate should resolve each `.dv-series` fill AFTER CSS (or forbid a blanket
`fill` on `.dv-series` that shadows the per-element attribute) so the next colour-collapse can't ship green.
Touches canon → Dave's call; the bar lane of the wave already opens this snippet.

## ds-011 — Three advisory a11y promotions carry trigger conditions that have never fired; the debt was invisible outside the generated report (2026-07-26, dream-pass v2 P3)
**OPEN — Dave ruled "log them" 2026-07-26 (dream-pass v2). Tracking entry only — the fixes are design
work at the named trigger events, not this entry.** `_ADVISORY-SIGNALS.md` has held **20 signals across
11 commits** (2026-07-22→25); three of them were wired 2026-07-03 with explicit written promotion
conditions (`_validate_advisory.py`, advisory-first per ADR-0005 §5), all still unmet:

- **G role-suffix (avd-006)** — condition: *"fix at the Cards revisit, then promote."* Still 2 signals
  (Cards + canon-gallery). **Trigger: the Cards revisit.**
- **H skip-link (acd-003, WCAG 2.4.1 — Level A)** — condition: *"all 5 composed screens signal at
  wiring — real gap, fix at the composition touch."* Still **5 of 5** — `_fitness-test/` screens
  untouched since the Apollo rename, so the trigger has never fired. Level A on every composed screen,
  against the ADR-0004 floor. **Trigger: any composition touch.**
- **N inputmode/autocomplete (acd-025, SC 1.3.5)** — condition: *"evidence banked for the Input-fields
  supercharge."* Still 8 signals (4 Input-fields + 4 gallery mirrors). **Trigger: the Input-fields
  supercharge.**

**Why it went invisible:** a condition whose trigger never fires is indistinguishable from a closed item
— the report is generated, green-adjacent, and nothing live pointed at it ([[assertion-propagation-gap]];
same family as [[gate-blindspot-state-contrast]]). This entry is the pointer. **When a trigger event is
scheduled (Cards revisit · composition touch · Input-fields supercharge), its brief carries the line
"clears advisory G/H/N" and the promotion happens per the wired condition.**

## ds-012 — Chart-bar's horizontal-bar category gutter is too narrow for the REAL HSBC cut; every label is clipped (2026-07-26, legend-wave lane ① render)
**OPEN — found the same way ds-010 was, one render later.** Rendering the real
`knowledge/snippets/Chart-bar.reference.html` at 1180px and 760px with the licensed HSBC face shows
**all six category labels on the horizontal-bar figure (`cb2`) cut off at the left edge**: "Groceries"
renders as "oceries", "Transport" as "nsport", "Housing" as "ousing", "Utilities" as "Jtilities".

**Root cause — measured, not eyeballed.** The labels sit at `x="38"` with `text-anchor="end"`, so they
grow LEFTWARD from a 38px gutter into a viewBox whose origin is 0. Measured `getBBox()` in-browser:

| label | width @12px, real cut | left edge | overflow |
|---|---|---|---|
| Groceries | 54.8 | −16.8 | **16.8px** |
| Transport | 55.0 | −16.4 | 16.4px |
| Housing | 48.2 | −10.2 | 10.2px |
| Savings | 45.3 | −7.3 | 7.3px |
| Utilities | 44.0 | −6.0 | 6.0px |
| Leisure | 42.0 | −3.8 | 3.8px |

Six of six clipped — the gutter is short by at least 17px for this data.

**Why it survived until now:** this is [[univers-measured-facts]] biting geometry. The HSBC cut is
LOOSER than Helvetica, so **a gutter baked against a narrower face fits, and the same gutter under the
licensed face does not.** The 38px was sized against something narrower than the real cut; the defect
was born there.

⚠ **WORDING CORRECTED 2026-07-27 (session #6), because the original misled Dave — and would have
misled the next reader the same way.** The entry read *"invisible in any render that falls back"*,
which he reasonably took as a claim about **his** environment: *"I have Universe installed so it
shouldn't use helvetica surely."* **He is right, and the clipping is the proof.** Univers is the
*looser* face — a Helvetica fallback would render these labels NARROWER and most of them would fit.
**Seeing the clipping is positive evidence the licensed cut is loading correctly**, on his machine and
in the measurement above. ⇒ **The fallback caution is about (i) how the 38px came to be baked and
(ii) MY verification renders**, where the sandbox can silently substitute — which is why the runbook
asserts `document.fonts.check('16px HSBC_MtUnivers_Latin')` before shooting. **It was never a claim
about Dave's browser.** *(Filed as a wording defect in its own right: a caution aimed at the render
harness, written where it reads as a diagnosis of the user's setup.)*

**NOT fixed in lane ①, deliberately.** Widening the gutter re-bakes every `x`/`width` on the h-bar
figure — a geometry change to a reviewed artefact, not a legend migration. Two candidate shapes, for
Dave: (a) widen the gutter to a fixed value that fits the longest label at the real cut (~60px), or
(b) make the plot area gutter-relative so long categories can't clip at any width. **Recommend folding
into the same beat as ds-010's sibling checks, with a render as the acceptance test — and adding a
"no `text.dv-label` has `getBBox().x < 0`" assertion to the dataviz gate so geometry clipping becomes
gated rather than eyeballed.** *(The gate would have to run in a browser — today it cannot; log as the
reason the assertion is a recommendation and not a patch.)*

### ★ RULED 2026-07-27 (session #6) — **(b) GUTTER-RELATIVE PLOT AREA**

**Dave re-reported the defect cold**, from a screenshot of the same figure, without reference to this
entry — *"we have cropping of the labels on the horiz-bars"* — and then ruled the fix shape:
**(b), the plot area is computed from the widest label, not a fixed number.**

**Why (b) and not the cheaper (a), in his own terms and worth keeping:** a fixed ~60px gutter fixes
*this data in this face*. **The clipping is driven by two things neither of which is a design
property** — how long the category names happen to be, and how loose the rendered face happens to be
([[univers-measured-facts]]: the HSBC cut is looser than Helvetica, which is the whole reason this
survived review). ⇒ **(a) fixes an instance; (b) fixes the class.**

**⚠ RULED ≠ ENACTED. Not built — the window was flushed before any build.** What the enactment owes:

1. **Compute, don't guess.** The widest label's width is only knowable *after* layout in the real
   face. A build-time constant re-introduces (a) wearing (b)'s clothes.
2. **⚠ RE-BAKING RISK — this touches a REVIEWED artefact.** Every `x`/`width` on `cb2` moves.
   **Attribute the diff** ([[attribute-the-diff]]): render a control before and after, or a correct
   change will be indistinguishable from a regression, which has nearly reverted good work twice.
3. **⚠ DO NOT let the plot area collapse.** Making the gutter grow with the label means the bars
   shrink; at narrow widths a long category can eat the plot. Needs a floor, and the floor needs
   Dave's eye — it is a legibility trade, not a formula.
4. **The acceptance test is a RENDER in the licensed cut**, both widths, snippet AND showroom pane,
   with `document.fonts.check(...)` asserted first. A fallback-face render will pass while broken.
5. **Ship the gate with it:** *no `text.dv-label` has `getBBox().x < 0`*. ⚠ It needs a browser, so it
   belongs with the render-proof family (`_verify_dv_*`), **not** in the static dataviz gate — putting
   it in a static gate is exactly the instrument-fit error the 07-27 pass measured (a STATIC check for
   a RENDERED property), and it would report a cheerful pass.

**Found by:** Dave, by eye, twice — 2026-07-26 render and again 2026-07-27 cold. ⚠ **The second report
is itself the signal: a logged, measured, correctly-parked defect was hit again by the user before the
queue reached it.** Parking is not free; it spends Dave's attention on something we already knew.

## ds-013 — `srcdoc` re-based every showroom payload's relative URL, so type.css 404'd in ALL 49 panes that link it (2026-07-27, Dave's report → render)
**✅ FIXED + GATED SAME SESSION.** Dave, cold: *"the labeling on the donut and bars, they are all too
big apart from the reset button, we had an independent scale for labels that seems to have been
lost"* — an exact description of the DV-D08 chart text ladder (12/500) not applying.

**Root cause — the srcdoc base-URL trap.** `gen_showroom.py` embeds the reference snippet VERBATIM and
hands it to the pane iframe as `srcdoc`. A srcdoc document has no URL of its own; per spec it inherits
the **parent's** base URL — `showroom/<Component>.html`. So the snippet's own
`<link rel="stylesheet" href="../canon/type.css">`, correct from `knowledge/snippets/`, re-resolved to
`<repo>/canon/type.css` — **a path that does not exist**. Every `.t-cm-*` composite AND every
selector-list binding in type.css was inert in every showroom pane. A 404 stylesheet throws nothing:
the failure presents as "the type looks a bit off".

**Measured, not eyeballed** (computed styles, licensed HSBC cut, `showroom/Chart-donut.html` +
`Chart-bar.html`, both panes):

| element | before | after | canon |
|---|---|---|---|
| `.dv-leg-item` (label) | 16px / 400 | **12px / 500** | 12/500 |
| `.dv-leg-name` | 16px / 400 | **12px / 500** | 12/500 |
| `.dv-key` (letter key) | 16px / 400 | **12px / 700** | 12/700 |
| `.dv-leg-reset` | 12px / 400 | **12px / 500** | 12/500 |
| `.t-cm-chart-label` rule | NOT FOUND | **12px / 500** | — |
| `type.css` cssRules | BLOCKED / absent | **57** | — |

Reset was the only correct label in the pane **because its snippet CSS hard-codes `font-size:12px`** —
the one member not depending on the composite. That is exactly the asymmetry Dave reported.

**Longstanding, not a lane-① regression — OBSERVED.** Rendering the PRE-migration snippet
(`git show 7401daf~1`) under the same unreachable-type.css condition gives `.dv-legbtn` = **13.333px /
400** — the `<button>` UA default. The DV-D11 migration added `.dv-leg-item{font:inherit}`, which
swapped that UA default for the inherited **16px** body size. So the outage predates the wave; the
migration made it 2.7px worse and cost the key its 700 weight, which is what pushed it over Dave's
threshold. **Blast radius: 49 of 67 snippets link type.css — every one of them has been rendering
uncomposed type in the showroom.**

**Fix + GATE (`knowledge/gen_showroom.py`).** `rebase_payload_urls()` re-points each payload's relative
URLs so they resolve from `showroom/` (`../canon/type.css` → `../knowledge/canon/type.css`), and — the
half that matters — **a rebased URL whose target does not exist FAILS THE BUILD.** The condition is
gated, not the instance. Selftest `--selftest` (6 bites) wired as a build step; build **56/56 GREEN**.

⚠ **ANTI-FALSE-FIX, recorded because it is the obvious "simplification":** do NOT replace this with an
injected `<base href="…">`. A `<base>` also re-bases **fragment-only** URLs, which would break every
inline icon-sprite reference (`<use href="#ic-*">`) in the library — trading a type outage for an icon
outage. Bite 2 pins that.

**Two residues, logged not fixed.** (a) `reviews/BINDING-MECHANISM-2026-07-18*.html` carries the same
dead `../canon/type.css` — a historical review artefact, left as filed (do not rewrite ratified docs);
(b) **49 showroom panes now render canon type for the first time** — a library-wide visual change that
no one has eyeballed. Registered in `_REVIEW-SIGNOFF.md`.

**The standing pattern, now THREE times:** ds-010, ds-012 and ds-013 were all found by rendering the
real artefact in the real cut, and **none is reachable by any static gate we had.** ds-013 differs in
one way that matters — it was found by *Dave's eye*, not ours. The gate it produced is the first of the
three to make the class of failure build-blocking.

## ds-014 — DAVE'S FLAGS, 2026-07-27: "we are losing decisions" — the stacked graph + 3 cardinal a11y rules
**OPEN. RECORDED VERBATIM AND IMMEDIATELY, because the complaint is precisely that things like this
evaporate.** Dave, mid-session, three messages:

> *"okay we are loosing decisions, this is getting frustrating"*
> *"theres more the stacked graph, has lost decisions made days ago"*
> *"its even lost 3 cardinal Ally rules"*

**NOT YET DIAGNOSED — and deliberately not guessed at.** The specific stacked-bar decisions and the
three accessibility rules he means are HIS observations; writing my guess here would be exactly the
confident-false-inscription failure the project is built to avoid. **Next session's FIRST job: get
the three named, then diff the stacked figure (`cb5`, `Chart-bar.reference.html`) against
`_DATAVIZ-DECISIONS.md` + the a11y rule set, decision by decision, and report what is actually
missing rather than what is plausibly missing.**

**What IS measured already (2026-07-27, post-ds-013 sweep — the first systematic pass):**
`_render-env/sweep.py` walks every showroom pane, reads each `.t-cm-*`/`.t-ed-*` composite's DECLARED
size+weight out of `type.css`, and asserts the computed value on every element carrying that class.
**800 composite-bound elements checked · 22 deviations across 27 panes.** The pattern is **WEIGHT, not
size** — `t-cm-caption`/`t-cm-label`/`t-cm-figure-5/6` computing **500 where the composite declares
400**, and `t-ed-heading-4` computing **400 where it declares 300**. Worst pane: **stepper (3)**. Also
touched: amount-input · date-picker · date-range-picker · drawer · empty-state. (The panes reporting
"type.css did not load" are the snippets that never linked it — count consistent with 67−49=18, but
CONFIRM rather than assume.)

**THE STRUCTURAL POINT, which is Dave's actual complaint.** ds-013 was the same shape: **DV-D08's
12/500 chart ladder was ruled, inscribed, gated-green, and silently not in force for weeks.** Rulings
in this project do not get reversed — they quietly stop applying, and the only detector is Dave's eye.
Gates prove the corpus is SELF-CONSISTENT. **Nothing proves a RULING IS LIVE in the artefact Dave
looks at.** That is a missing gate class, not a missing fix:
- the sweep above is the first instance of one — it compares a **ruled value** to a **rendered value**;
- `_ASSERTIONS.md` already holds the machinery for "this claim, this evidence" but is not wired to
  ledger rulings, and per [[assertion-propagation-gap]] it only fires on FLIP;
- **candidate: every `DV-D*`/`R-D*`/`B-D*`/`T-D*` ruling carries either an executable enactment proof
  or an explicit NOT-GATEABLE marker, and the build reports the unproven ones as a standing debt
  register.** Recommend, do not enact — this is an architecture call and Dave's to make.

**★ ds-014 UPDATE — Dave NAMED two of them (2026-07-27, same session, verbatim):**

> *"spacing between segments and contrast on the alpha labels"*

So the stacked figure (`cb5`, `Chart-bar.reference.html`) has lost, in his eye: **(1) the spacing
between stacked segments** and **(2) the contrast treatment on the alpha labels** (the A/B/C letter
keys — "legend alphas" in DV-D07's language, emphasis channel 700). ⚠ **CORRECTED same session — Dave: *"the 3 was a misstype"*. There is NO third unnamed rule.**
The earlier line here asked the next session to chase one; it would have gone looking for something
that does not exist. The accessibility complaint IS the alpha-label contrast, named above.

**Leads for the next session, marked as LEADS not findings:**
- **DV-D07** already rules that where a theme sets alpha < 1, **dv-016 / DV-D03 contrast must compute
  from the COMPOSITE (colour × alpha × ground), never the stored hex alone.** If the enactment
  computes on the hex, letters can pass a gate and fail on screen — the same silent-wrongness shape
  as ds-013.
- Segment spacing: the ledger's stacked entries found so far are ANIMATION order (Batch 3 #2, Batch 4
  #4, #3 easing), **not** a spacing/separation rule — so the spacing decision is likely inscribed in
  the **bar audit** (`reviews/BAR-CHART-AUDIT-2026-07-23-v1.REVIEW.html`) or the DV-D08/09 block.
  **Find where it was ruled before judging whether it was lost.**
- ⚠ **A first probe of `cb5` returned ZERO segment rects** — the figure/selector assumption in
  `_render-env/stack.py` is wrong (grouping by `x` attribute; the stack may use `<g transform>` or
  non-`rect` marks). **That is a broken probe, NOT evidence that the segments are missing.** Fix the
  probe before reading anything into it. Written down because a "0 rects" line in a log is exactly
  the kind of thing that gets quoted later as a finding.

**Authoring gauge: 🔴 RED ~90% — this entry is a CAPTURE, not a diagnosis. Everything above the
"LEADS" line is Dave's words; everything below is unverified.**

**★ ds-014 UPDATE 2 — a fourth flag (2026-07-27, verbatim):**

> *"teh donuts have lost the centreing responsive behaviour"*

**Dave's running list, as given, in his words:** label scale on donut + bars *(FIXED — ds-013)* ·
stacked **segment spacing** · stacked **alpha-label contrast** · donut **centring responsive behaviour**. *(A "3 cardinal a11y rules" phrasing in the original
messages was a typo, corrected by Dave same session — there is no third item.)*

**★ THE HYPOTHESIS THAT SHOULD BE TESTED FIRST — and it is cheap.** Every one of these was seen in
the SHOWROOM, and until this morning **the showroom could not load `type.css` at all** (ds-013).
Layout that depends on text metrics measures differently when the type is 16px/400 instead of the
ruled 12px/500 — **a donut whose centre figure is sized and centred against its own text is exactly
that kind of layout**, and so is anything reflowing on a container/element width that text
contributes to. ⇒ **Some of this list may be showroom artefact rather than lost canon; some may be
real regression that the broken type was masking. Do not assume either.**

**THE TEST, one pass, mechanical:** render each affected component **standalone**
(`knowledge/snippets/<X>.reference.html`, where `../canon/type.css` has ALWAYS resolved) and
**side-by-side with its showroom pane**, and diff the measured geometry. Anything that differs is a
showroom/base-URL artefact; anything wrong in BOTH is a genuinely lost decision, and only those go to
the ledger diff. **This separates the two causes in one run and stops us chasing five things that may
share one cause.** ⚠ Note the showroom panes were only regenerated correctly at commit `ba336dc` —
anything Dave looked at before that was, for type purposes, a different document.

**★ CORRECTION (Dave, same session): *"the 3 was a misstype"* — there is no third cardinal a11y
rule and nothing is owed on it. The list is FOUR items, one of them already fixed. Struck here as
loudly as it was raised, because a phantom item on a debt register is worse than no register: it
sends the next session hunting, and an agent that hunts long enough will FIND something and inscribe
it. (This is the [[memento-framing]] failure mode in miniature — the danger is not forgetting, it is
confident false inscription.)**

**★ ds-014 UPDATE 3 — the structural fix is RULED, not proposed (Dave, 2026-07-27):**

> *"is this in the next session, we nee to fix it"*

**⇒ The enactment-proof register is a BUILD, scheduled next session, phased P1 register → P2 proofs
for the four flagged items → P3 wire advisory-then-blocking.** Full shape in `GOOD-MORNING` §DO-FIRST.
Candidate **ADR-0016**, to be written in the same session as P1 (same-hour inscription rule) and fed
to the graph seed. Reflected back to Dave in-session for correction before the next window opens.

---

**★ ds-014 DISCHARGED — the discriminator RAN, 2026-07-27 (Mon morning session).** Every item below
is MEASURED by render, licensed cut, at 1180 **and** 760, **snippet beside showroom pane** — the one
pass that separates a lost decision from a ds-013 base-URL artefact. Probe + raw JSON:
`_render-env` recipe in `_RUNBOOK-render-verify.md`; results quoted here are OBSERVED, not inferred.

| # | Dave's flag | verdict | measured |
|---|---|---|---|
| 1 | label scale, donut + bars | **ARTEFACT — already fixed** | ds-013 (`srcdoc` killed `type.css`); keys now 12px/700, `.t-cm-figure-3` 24px/500 in the licensed face |
| 2 | stacked **segment spacing** | **★ LOST DECISION** | gap **0.0–0.1px** on all 4 columns × 3 boundaries, `stroke:none`. **dv-004 is BLOCKING and requires ≥2px.** Identical snippet vs showroom |
| 3 | stacked **alpha-label contrast** | **★ LOST DECISION** | keys render **`#1A1A1A` (`--ink`)**, not the `var(--page)` their markup declares — `text.dv-barkey{fill:var(--ink)}` (snippet L127 / canon.css L3434) overrides the SVG presentation attribute. Contrast **3.31 / 3.46 / 3.78:1** at 12px/700; AA floor 4.5:1. White measures ≈5:1 and passes. Identical snippet vs showroom |
| 4 | donut **centring**, responsive | **ARTEFACT — does not reproduce** | centre value **dx +0.00 / dy −2.00** (optical), ring offset **0.00** in canvas — identical snippet vs showroom at both widths |

**★ WHY #2 SHIPPED GREEN — the root cause, and it is bigger than one chart.** `_validate_dataviz.py`
guards dv-004 with `if dtype in ("donut","pie","stacked")`. The figure declares
`data-dv-type="stacked-column"`. **The gate never looked.** The register's scope-blindness audit
generalised it the same hour: `stacked-column`, `grouped-column` and `scatter` appear **zero** times
in the gate ⇒ **dv-004, dv-bar-009 and dv-line-011 are all inert on those three chart types.**

**⬛ OPEN, and they are DAVE'S CALLS (derivation governance — measured, not fixed):**
- **(a)** dv-004 on stacked columns: 2px surface-coloured stroke (the donut's mechanism) or a
  geometry gap? Either changes the chart's look; both make the currently-green build FAIL until done.
- **(b)** alpha keys back to `var(--page)` white per the D-Q2 ledger line, or re-rule the ledger to
  ink and accept 3.3:1? (type26-013 "white type is red-only" is the tension the ledger already noted.)
- **(c)** widening the gate's dtype vocabulary is mechanical, but it turns (a) into a build failure —
  so it lands *with* (a)'s answer, not before it.
- **(d)** NEW, un-ruled, not on Dave's list: `.dv-donut-row` is `flex-start`, so the ring+legend
  cluster pins left and whitespace grows with viewport (**−114px at 600 → −534px at 1440** from
  figure centre). No ruling covers donut cluster alignment. Flagged only.

---

**★★ ds-014 CALLS (a)+(b) RULED AND ENACTED — 2026-07-27, later morning. Proven by RENDER, not by gate.**

**Dave ruled (a) = GEOMETRY, against my recommendation, and he was right on the evidence.** I had
recommended the donut's 2px surface-coloured stroke. He pushed back — *"I prefer the geometry the
border will obscure gridlines, may I know why you recommend borders?"* — and he was correct:
**`cb5` carries 5 full-width `.dv-grid` lines behind the columns; the donut carries none.** An SVG
stroke straddles its path, so a 2px page-coloured stroke puts 1px OUTSIDE each rect and would paint
over every gridline down both sides of all 4 columns. ⇒ **A surface-coloured stroke only simulates
separation when the thing behind it IS the surface.** The donut precedent does not transfer to a
gridded plot. *(My recommendation was precedent-transfer without checking the ground — recorded as
the error it was.)*

**★ THE RULE HAD BEEN NARROWED BY ITS OWN GATE — the generalisable finding.** dv-004's text is
mechanism-NEUTRAL: *"minimum 2px separation between colour blocks."* `_validate_dataviz.py`
implemented it as *"must carry a surface-coloured stroke >=2px"*. **So a chart satisfying dv-004
with real geometry would have FAILED the gate**, and the only "compliant" answer available to an
agent reading the gate was the wrong one for this chart. Dave caught it from the KG —
*"the gap is only 2px minimum, this is in the dataviz specifications in the KG"* — which is the
seed of the forcing-function idea now held in `_FUTURE-STATE.md`.

**ENACTED, geometry variant A (both ends pinned):** baseline stays `y=230` and each stack top stays
at its true total, so every column still reads correctly against the gridlines; the 4px (2 boundaries
× 2px) comes out of segment heights, proportionally. Cost, stated at ruling time and accepted:
segments understate by **2.0–2.6%**, worst on the shortest column.

**ENACTED (b): `data/text/on-series` MINTED** (Dave's promotion) → `color/grey/white`, pinned in BOTH
modes, modelled on `rag/text/on-dark`. **Deliberately no alpha channel** — DV-D07 requires contrast to
compute from the composite, so an alpha slot here would be a route to a key that passes on the hex and
fails on screen. The blanket `text.dv-barkey{fill:var(--ink)}` is now split by ground: ink for cb4's
keys on page air, `--data-text-on-series` for cb5's keys on fills, with an anti-false-fix comment.

**★ MEASURED, licensed cut, snippet AND showroom pane, 1180 AND 760 — all four agree:**

| assertion | ruled | rendered | verdict |
|---|---|---|---|
| dv-004 separation | ≥2px | **2.00px** across all 8 boundaries, every context | ✅ |
| alpha key A on `rgb(118,102,130)` | ≥4.5:1 | **5.26:1** | ✅ |
| alpha key B on `rgb(164,92,58)` | ≥4.5:1 | **5.04:1** | ✅ |
| alpha key C on `rgb(87,124,120)` | ≥4.5:1 | **4.61:1** | ✅ ⚠ |

⚠ **The handoff predicted "white measures ≈5:1". MEASURED worst case is 4.61:1** — series-3, margin
**0.11 over AA**. Recorded as measured, per the 07-26 Correction-2 rule. **Series-3 cannot be lightened
without breaking this**, and nothing but the new proof would catch it.

**★ A THIRD INSTANCE OF THE SILENT-FALLBACK CLASS, caught by the probe and not by any gate.** With the
token minted, generated into `canon.css`, and the whole build green, **the keys still rendered BLACK
(3.99:1)**. Cause: the snippet is standalone-previewable and carries a LOCAL MIRROR of the token list
in its own `[data-theme]` blocks — and it did not declare `--data-text-on-series`. **`fill:var(--undefined)`
does not fall back to the previous value; it falls back to the SVG initial value, black, in silence.**
Same shape as ds-010 (author CSS beat the `fill=` attribute) and ds-013 (404 stylesheet): *the failure
mode of this file's whole history is a lookup that misses and reports nothing.*

**★ GATE WORK — condition gated, not instance patched:**
1. **`dv-vocab` (NEW, BLOCKING)** — any `data-dv-type` the gate has never heard of now FAILS the build,
   naming the rules that would have skipped it. The corpus had forked unnoticed: **both `stacked` and
   `stacked-column`, both `grouped` and `grouped-column`**, plus `scatter`. Enumerating the three known
   synonyms would only have postponed the next miss.
2. **`DTYPE_CANON`** normalises synonyms once, at read time, instead of at five separate branches.
3. **dv-004 now accepts EITHER** a ≥2px surface stroke **or** ≥2px of measured geometry
   (`_rect_stack_gap`), matching the rule's own wording. Unmeasurable geometry still demands the
   stroke — it fails SAFE.
4. **9 new bites**, including one that reproduces the exact ds-014 figure and one proving `dv-vocab`
   fires. **Selftest WIRED into the build** (step added): it existed and ran only by hand, which is
   precisely why nothing ever proved dv-004 could fail.
5. **`knowledge/_verify_dv_stacked_enactment.py` (NEW)** — the ADR-0016 **P2 proof** for both rulings:
   reads the ruled value, asserts the RENDERED value in the licensed cut across snippet × showroom ×
   two widths. It caught the black-keys defect above, which every gate had passed.
   ⚠ **It also committed the wrong-document error itself** — first pass queried only the top document
   and reported "no stacked-column figure" for the showroom, whose panes are `srcdoc` iframes. Third
   session running that a probe made the class of error it was written to detect. **Assume yours will.**

**(c) DISCHARGED** — the vocabulary widening landed *with* (a), as required. **(d) PARKED on Dave's
ruling** (2026-07-27): log only, rule it in a session where he can see it live. Not fixed, deliberately.

---

## ds-015 — `aid-009`'s hit-area check EXEMPTS every component that adopts the hit-area mechanism; 7 of 67 snippets are actually measured (2026-07-27, Dave: "maybe we are checking the wrong thing")

**Found by Dave, from the KG-forcing-function exploration** — he read the `icon-005`/`aid-009` exhibit and
said: *"so the 44px rule is negated by the hit area mechanism, maybe we are checking the wrong thing."*
He was right, and the mechanism is worse than mis-measurement: **adopting the correct mechanism is what
removes a component from the check.**

**The line (`knowledge/_validate_a11y.py`), quoted verbatim — its own comment is candid:**
```python
# an explicit hit-area expander for THIS selector exempts both tiers
# (static CSS can't size the expander; the render axis owns that check)
if re.search(re.escape(sel) + r'\s*::(before|after)', s):
    continue
```
It does not measure the expander. It **skips**, and defers to "the render axis" — which is the hit-area
gate still marked *PENDING DAVE SIGN-OFF* in `notes/_briefs/2026-07-25-hit-area-rule-and-gate-proposal.md`.
**The handoff has no receiver.**

**MEASURED (2026-07-27, corpus scan reproducing the gate's own `CTRL`/`DECOR` regexes):**

| | count |
|---|---|
| snippets | 67 |
| selectors SKIPPED — not matched by the `CTRL` regex | **1,869** |
| control selectors eligible (explicit px `width`+`height`) | 14 |
| — EXEMPTED by a `::before` expander (check skipped) | **7** |
| — **actually measured** | **7** |

**Gate verdict today: 67 snippets · 0 failures · 6 warnings · exit 0.** 64 of 67 snippets use `::before`.
**The library's hit-area compliance rests on 7 measured selectors.**

**THE DIAMOND — three independent blindnesses on one element, and the defect it hides is already PROVEN.**
`Chart-line.reference.html`: `.dv-leg-sw.sw-diamond` is `width:8px;height:8px;transform:rotate(45deg)`,
its target on `.dv-leg-sw::before{min-width:var(--hit,44px)}`.
1. **Scope** — `.dv-leg-sw` does not match `CTRL` (`button|a\.|\.x|\.close|\.clear|\.trigger|\.handle|\.page|\.step`).
   Never in scope. **Same hand-maintained-vocabulary class as the `dtype in ("donut","pie","stacked")` fork
   that produced ds-014** — and `dv-vocab` closed that one for dataviz only. **`CTRL` is UNSWEPT.**
2. **Parse** — the expander is `min-width:var(--hit,44px)`; the gate's regex reads literal `(\d+)px`.
   **It cannot parse a token.**
3. **Exemption** — `::before` present → `continue`.

> **✅ CLOSED BY ADDITION (2026-08-07, #122):** blindness 1 is RETIRED — the hand-maintained `CTRL` regex
> was replaced in the #115 markup rebuild (`2a231f9`) by ARIA-role classification in `_validate_a11y.py`
> that **fails loud on unknown roles** ("CTRL vocabulary: unknown ARIA role(s) … cannot classify"),
> verified #119. This queue line was the stale record. Blindnesses 2 (token parse) and 3 (`::before`
> exemption) and the transform-consequence class remain open, owed to the render-axis hit-area gate below.
⚠ **And the actual defect is a TRANSFORM consequence** (the `rotate(45deg)` rotated the 44px target onto
its corner). **No static box measurement can see that in principle**, not merely in this implementation.
It was caught by `elementFromPoint` probes at render, by hand, during the legend wave — and that snippet's
own comment records that *"the divvy did not name it."*

**⚠ SEVERITY IS UNKNOWN AND THAT IS THE POINT.** This record proves the check is blind, **NOT** that the
components are non-compliant. Most probably pass. **Nothing has measured them**, and per
[[gate-blindspot-state-contrast]] "0 failures" from a blind check is worse than no check.

**INTERIM FIX APPLIED (2026-07-27, Dave assented — reversible, one line, NO rule change):** the silent
`continue` now emits a **warning** naming the exemption, so exemptions are visible and countable instead
of invisible. **The exemption still stands** — this does not fail any build and does not pre-empt his
rulings.

**OWED — Dave's, all open:** the real fix is the render-axis hit-area gate (DO-FIRST item iii), which
**stops being a backlog item: it is the named receiver for an exemption already shipping.** Framing +
trigger-shape questions are held in `_FUTURE-STATE.md` § *forcing the KG into the decision loop*,
Exploration beat 1 — including **Dave's cascade point**: *"the hit mechanism should have triggered
something that cascaded this elsewhere."*

---

## ds-016 — Seven live gates cite rules the index cannot see: 698 anchors declared, 465 indexed, 265 invisible (2026-07-27, found by a bite failing on its first run)

**Status: LOGGED, not fixed.** Deliberately — the remedy is call (4)'s discussion, which Dave has
NOT ruled (*"I lean fix, but this probably needs a discussion"*).

**MEASURED** (`knowledge/_build_instrument_fit.py`, regenerates every build):

| | count |
|---|---:|
| rule anchors `{#id}` declared in `guidelines/*.md` | **698** |
| held in `guidelines/_rules-index.json` (destiny-tagged) | **465** |
| declared but NOT indexed (no enforcement-destiny tag) | **265** |
| of those, **cited by a live gate as its authority** | **7** |

The seven: `aca-003` (`_validate_compose.py`) · `aca-004` (`_validate_advisory.py`,
`_validate_snippets.py`) · **`aid-009`** (`_validate_a11y.py`) · `aid-020` (`_validate_advisory.py`) ·
`avd-006` (`_validate_advisory.py`, `_validate_snippets.py`) · `axs-003` (`_validate_a11y.py`) ·
`nam-001` (`_validate_advisory.py`, `_validate_snippets.py`).

**Why it matters, and why it was found by accident.** `aid-009` is Dave's hit-area ruling of
2026-07-03 and the founding case of **ds-015**. `_validate_a11y.py` names it five times as the rule
it enforces. Its anchor line ends `Bite-tested (test_gates target24)] {#aid-009}` — **the destiny
tag was never written**, so the rule a BLOCKING gate enforces cannot be retrieved by `_consult.py`,
the enactment register, or anything else that reads the index. It surfaced only because a bite
asserting the ds-015 ground truth returned `None`.

**The mirror image sits in the same family:** `icon-005` — **BLOCKING**, *"Functional icons need a
minimum 44×44px target area"* — IS indexed and **no gate names it at all**. So the 44×44 rule that
exists has no check, and the check that exists cites a rule nothing can look up.

⇒ **ds-015 INVERTED.** There the gate could not see the component; here the index cannot see the
rule. Same signature as the silent-lookup class already proven three times (ds-010 · ds-013 · the
DV-D15 local token mirror): **the markup is correct, the lookup fails, and nothing reports it.**

### ⚠ ANTI-FALSE-FIX

1. **The 265 are excluded BY DESIGN, not by bug** — `gen_rules_index.py` says so in its docstring:
   the index holds enforcement-destiny-tagged rules. **Do not "fix" the generator to swallow all
   698.** That would flood the index with prose anchors and break every count that depends on it.
2. **The defect is the SILENCE, not the exclusion** — nothing reported that seven live gates depend
   on rules inside the excluded set. Any fix must make that condition *loud*, not make it disappear.
3. **Do not bulk-add destiny tags to clear the list.** A destiny tag is an enforcement decision
   (BLOCKING / ADVISORY / REVIEW) and belongs to Dave — derivation governance. Tagging 265 anchors
   to quieten a report would be the largest unpromoted derivation in the project's history.
4. **`aid-009` in particular is RULED and IN FORCE** — its absence from the index is a retrieval
   failure, NOT evidence the ruling lapsed. Do not treat the gate as unauthorised.

### Candidate remedies (none ruled — for the call-(4) discussion)

- **(a) Fail loud, adoption-time.** A gate citing a rule ID absent from the index errors at build.
  Cheap, structural, mirrors the ratified `dv-vocab` fix (*normalise once, fail loud on unknown,
  never enumerate*). Catches the next one for free; says nothing about the existing 7.
- **(b) Tag the 7.** Smallest possible change, restores retrievability for exactly the rules a gate
  already enforces. Each tag is a Dave decision.
- **(c) Both** — (b) clears today's debt, (a) stops tomorrow's. This is the adoption-time/sweep pair
  Dave ruled complementary the same session, applied to itself.

**Detected by:** `knowledge/_build_instrument_fit.py` § dangling citations (bites 1c + 1d).
**Narrative:** `_DECISION-HISTORY/2026-07-27-the-index-cannot-see-the-rule.md`.

## ds-017 — A FLOATED item that supersedes a standing instruction has no path into the handoff (2026-07-27)

**Status: LOGGED at the moment it bit, then partially closed by the ruling it was blocking.**

**What happened.** At the 2026-07-27 #4 wrap Dave said *"the pre-flighting needs work, we cant keep
hitting red, its a waste of effort."* The diagnosis was filed correctly — `_FUTURE-STATE.md`
★★ FLOATED, marked UNRULED, with its own sequencing note: *"~10 minutes at the FRONT of the next
window; it does not displace ds-016 / the `CTRL` sweep, it precedes them."*

**The next session did not find it.** `GOOD-MORNING.md` § DO THIS FIRST carried a pre-flight paragraph
— restating the **three-term rule**, i.e. **the very rule the same session's wrap had concluded did not
work**. The correction lived only in `_FUTURE-STATE.md`, which nothing in the read-order requires. The
agent read the handoff, ranked ds-016 as the session's task, and was wrong; **Dave had to say
"should be the pre-flight work" twice before the right file was opened.**

⇒ **Same signature as the silent-lookup class** (ds-010 · ds-013 · ds-015 · ds-016): the record was
correct and complete, the retrieval path did not reach it, and nothing reported the gap. Here the extra
turn of the screw is that **the stale instruction was still being handed forward as live guidance** —
a Polaroid carrying a superseded posture, which is the *confident false inscription* failure the whole
GOOD-MORNING architecture exists to prevent (§A).

### Why the existing mechanism missed it

The ritual's **2c/2d EXIT CHECK** (ruled 2026-07-26, dream-pass V2-P1) carries §C·4 items up so banner
compaction cannot lose them. It has **no clause for the inverse case**: an item filed in
`_FUTURE-STATE.md` that **supersedes or contradicts a standing instruction already in the handoff**.
Compaction was never the problem — **the item was never in the handoff to begin with.**

### ⚠ ANTI-FALSE-FIX

1. **Do not "fix" this by copying `_FUTURE-STATE` into the handoff.** It is 63KB of deliberately-parked
   material; the handoff's value is that it is short. The defect is the missing *link*, not missing bulk.
2. **Do not add "read `_FUTURE-STATE` too" to the read-order** and call it closed. That is a discipline
   instruction, not a mechanism — the same category error as the pre-flight rule itself, which was
   inscribed as prose and then failed to stop the thing it described.
3. **A FLOATED item is not authority.** Anything that supersedes a standing instruction still needs
   Dave's ruling before the handoff presents it as live. The fix is to make the *contradiction visible*,
   not to auto-promote the newer text.

### Candidate remedies (UNRULED — Dave's call)

- **(a) Wrap-gate check:** a `_FUTURE-STATE.md` entry marked ★★ FLOATED whose body names a standing
  document must be echoed as a one-line pointer in `GOOD-MORNING.md` § DO THIS FIRST, or the wrap fails.
  Mechanical, mirrors the ratified *fail-loud-on-unknown* pattern.
- **(b) Ritual clause:** extend the 2c/2d EXIT CHECK with the inverse direction — before writing the
  handoff, list FLOATED items that touch a standing instruction and carry each up or explicitly decline.
- **(c) Both** — (b) catches this week's, (a) stops the next one silently recurring. Same
  adoption-plus-sweep pair Dave ruled complementary on 2026-07-27.

**Found by:** Dave, twice, in the first ten minutes of session #5 (*"read the 'do first' … it should have
a new task"* → *"should be teh pre-flight work, is that correct?"*). **No gate saw it.**
**Canon it was hiding:** `_RUNBOOK-context-gauge.md` § ★ Half 0b · `_FUTURE-STATE.md` § the throttle.

---

## ds-018 — Legend Reset renders its DISABLED state as the HOVER state (2026-07-27, Dave by eye)

> **★ #121 (2026-08-07) — RULED `s121-D1` + ENACTED: C2 0-of-114, PROMOTED `--strict`.** A1 generator-inject (`gen_token_ramp.py`, 4th injection type) · B1″ per-status mark map (values PROVISIONAL — Dave's combination pass owed) · C1 measured `--phys-size` (Alert 24 · Popover 24 · Empty-state 120 provisional-from-receipt). Projector's missing `alpha/` route (since #99) fixed same pass. Cases: `notes/_ds-018-C2-cases.md` · dossier: `_DECISION-HISTORY/2026-08-07-121-ds018-token-schema-ruling.md`.


> ### ✅✅ ENACTED + BUILD-GREEN 2026-07-27 (session #12). **A2 · B2 · C2 are all in. Do not re-enact.**
> **Build `62/62` GREEN, exit 0** (58→62: C2 + its selftest added two steps, and two generators re-ran).
> **⚠ NOT RENDER-PROVEN.** Deferred by Dave's ruling this session — the env was cold and the proof was
> priced against a window already at Amber. **The render-proof is the one thing still owed on ds-018**,
> and it is owed against `_RUNBOOK-render-verify.md` (licensed cut asserted inside each measured frame,
> transitions settled, colours compared as colours, **cells read not flattened text** — #11's probe wart).
>
> **WHAT LANDED, file by file:**
> - **A2 · the tier.** Minted `data/control/label-disabled` in `tokens/semantic-colour.json` as a
>   sibling of `data/axis` / `data/grid` — light `#9D9D9D` (`color/neutral/9`), dark `#808080`
>   (`color/neutral/8`). Declared as `--data-control-label-disabled` on the light AND dark spine blocks
>   of **Chart-bar · Chart-combo · Chart-donut · Chart-line** (the four with legends; scatter and
>   sparkline have none), and mapped in each `#token-manifest`.
>   ⚠ **In the SNIPPET SPINES, not `canon.css`** — chart snippets link `type.css` only and inline their
>   own spine, so `canon.css` is not in this cascade (#11's finding, and it held).
>   ⚠ **CORRECTION TO #11's INSTRUCTION:** the handoff said to land this "in the GENERATOR, never a
>   canon.css hand-patch". **There is no generator for the CSS spine** — `gen_component_partials.py`
>   injects only the JS behaviour blocks between `AUTO-BEHAVIOUR` markers. The spine is hand-authored
>   per snippet, so this was four hand-edits, applied by one anchored script with per-file assertions.
> - **B2 · the channel.** `.dv-leg-reset:disabled` now reads
>   `border-color:var(--line); color:var(--data-control-label-disabled);`
>   ⚠ The border is bound **directly to `--line`**, not to a new border token — that IS B2: the disabled
>   border *is* the enabled-resting border. **The ruled+accepted cost stands: at rest the two are
>   identical and the label carries the whole distinction. Do not "fix" this back into a border
>   difference without asking.**
> - **THE VALUE — reuse, not derivation.** `#9D9D9D`/`#808080` is B-D4's SETTLED pair adopted verbatim.
>   Dave 2026-07-27, asked for the most efficient path: *"just do it"* — taken against an explicit
>   statement that (a) the alternative was a fresh value judgement, (b) a token value is a **one-line
>   reversible edit, not architecture**, and (c) proposing it was me proposing a value, vetoable in a word.
>   ⚠ **CAVEAT RECORDED AT MINT, not discovered later:** B-D4 dialled that pair against the **disabled
>   fill `#E1E1E1`**; here it sits on the **chart ground** (the legend row has no background,
>   `Chart-bar.reference.html:203`), so the same hex reads at a different ratio than the one judged.
>   **Re-dial on sight is expected and cheap.**
> - **`--muted` (the sibling defect, found this session).** `.dv-leg-sw[aria-checked="false"]` referenced
>   `--muted`, used in **4 of 6** chart snippets and declared in **none** (and not in `type.css`; it is in
>   `canon.css:748`, which is not in this cascade). Dave, on the v2 doc: *"muted looks fine to me"* ⇒
>   ruled as **no visual change**. Enacted as `--data-control-swatch-off:currentColor` — **a no-op BY
>   CONSTRUCTION, not by measurement**: it resolves to precisely what the failed lookup was already
>   falling back to, so it cannot shift a pixel, and it converts an accident into a named, tunable dial.
> - **C2 · the gate.** `knowledge/_validate_property_resolves.py`, wired at build steps 52–53.
>
> ### ⚠ C2 SHIPS **ADVISORY**, DELIBERATELY, AND THE REASON MATTERS MORE THAN THE GATE
> C2 is RULED BLOCKING. It runs advisory because **it found 10 pre-existing failures on its first run**,
> and going blocking today would have required clearing them **now** — which means inventing values.
> **Value promotion is Dave's alone.** The other exit, narrowing the glob to charts, is
> `gate-narrows-its-own-rule` in its purest form: a gate whose glob is smaller than its rule silently
> redefines the rule as whatever it happens to check. **So the rule stays wide, the findings are
> published, and nothing is faked green. Promotion is a one-line edit** (`["--strict"]` on the build step)
> **the moment the worklist is empty.** ⚠ An advisory gate that is never promoted has quietly become
> documentation — this one has a named trigger, use it.
>
> ### ★★★ THE GATE FOUND THREE MORE INSTANCES ON ITS FIRST RUN — the worklist, all Dave's
> **This is the finding of the session, and it is bigger than ds-018.** Five instances of the
> silent-lookup class had been found across five sessions, every one **by eye or by accident**. The
> first automated pass found three more in seconds. **⇒ The class was never rare; it was invisible.**
> 1. **`--border-radius-default` — instance six. FIXED THIS SESSION.** Consumed by `.dv-legrow` in all
>    four chart snippets, declared in **no snippet in the library**. Fell to initial = `0`, which is
>    *correct in Mono by accident* (square corners) and would have gone **silently wrong in Console**,
>    whose live divergence is rounded corners. ⇒ **A silent lookup can hide indefinitely behind a theme
>    whose value happens to match the initial.** Fixed by consuming the **role** token
>    `--border-radius-control` (a legend row is a control, not a surface — a tier correction, and my
>    call: the minimal fix was to declare the base, which would have bypassed the role tier) and
>    declaring it on both spine blocks + the manifest. **Value 0 in Mono ⇒ no visual change today.**
> 2. **`--phys-size` — instance seven. NOT FIXED, needs values.** Referenced 2× each in **Alert ·
>    Empty-state · Popover**, declared in none. This is **B-D7's press-physics local geometry** (buttons
>    120, icon 44 — Dave's ruled numbers) ⇒ **the press physics may be silently dead in three
>    components**, on a RULED behaviour. ⚠ **Unverified by render** — the inference is from resolution
>    rules, not observation. **Measure before believing it, then Dave sets the three numbers.**
> 3. **`--mark` — instance eight. NOT FIXED, needs a value.** Referenced across **7 pro-forma files**
>    (Masthead-interactive 7×, Tranche-2/3/4/5 1× each, Tranche-7 7×, Tranche-8 7×), declared in none.
>    It fills icon marks inside `<symbol>` ⇒ **falls to the SVG initial value, BLACK, in silence** —
>    *the exact failure `Chart-bar`'s own spine comment documents for `--data-text-on-series`*, which
>    was caught at 3.99:1 by a render probe. Same shape, same corpus, uncaught until now.
>
> ### ⛔ RECORD CORRECTION — the "B-D4 vs canon collision" DOES NOT EXIST
> The handoff carried, in **three** places (GOOD-MORNING DO-FIRST, `_LIVE-STATE` LATEST DELTA, §C·4),
> that *"B-D4 ruled `#808080` while canon ships `#9D9D9D` — two ledgered numbers that disagree"*.
> **They do not disagree.** B-D4's *prose* says `#808080` "both modes"; **B-D4's own
> `Values — SETTLED (Dave, 2026-07-20, dialled on the v7 live editor)` block gives the light/dark PAIR
> `#9D9D9D` m9 / `#808080` m8**, which `canon.css:351`/`:648` and `semantic-colour.json:1636` both
> implement. Three sources agree; the fourth is loose prose in the same document, read against half the
> ruling. ⇒ **`trust-the-spine-not-the-prose`, and it cost part of a window.** Nothing to reconcile.
>
> **Evidence:** `python3 knowledge/_build_all.py` **62/62 GREEN exit 0** · 2026-07-27 ·
> `_validate_property_resolves.py --selftest` **green control + 4 bites + a bite-the-bite, all PASS**
> · 2026-07-27 · `--muted` / `--border-radius-default` / `--phys-size` / `--mark` censuses by `grep -c`
> over `knowledge/snippets/*.reference.html` + `knowledge/_proforma/*.html` · 2026-07-27 ·
> decision doc `reviews/DS-018-VALUE-2026-07-27-v2.html` (+ `.REVIEW.html` overlay), **self-measuring:
> it leaves the three properties undeclared so the reader's browser resolves them.**
> **⚠ WHAT THE AUTHOR FLAGS AGAINST HIS OWN WORK:** the three new instances are **static-resolution
> reasoning, not renders** — instance six is safe to believe (initial `0` matches Mono), but
> **`--phys-size` and `--mark` should be render-confirmed before anyone acts on them**; the `--mark`→black
> claim in particular is the kind of tidy explanation this project has been burned by (ds-019). And the
> value `#9D9D9D` is **mine to propose and Dave's to keep** — it entered on "just do it", which is
> assent to a plan, not a dialled number.

> ### ★★★ RULED BY DAVE 2026-07-27 (session #11) — the remedy is settled. **A2 · B2 · C2.**
> **Ruled from** `reviews/DS-018-DISABLED-STATE-2026-07-27-v1.html` (live specimens, three decision
> controls, contrast computed at render time). Dave, verbatim: *"I've gone with your recommendations
> but we should probably wrap up and do it in the next window."* The doc's marked recommendations were
> A2 / B2 / C2, so that is what "my recommendations" resolves to. **Recorded as RULED; enactment is
> deliberately NOT started — his instruction, and the gauge was Red.**
>
> - **CALL A — the tier fix ⇒ A2: MINT DATAVIZ-TIER EQUIVALENTS.** New `--data-control-*` properties
>   declared on chart scopes, siblings of the `--data-axis` / `--data-grid` / `--data-series-*` family
>   that already lives there. **Not chosen:** declaring the form tokens on chart scopes (imports the
>   form ladder wholesale); promoting to `:root` (see the finding below — it is already the state of
>   `--text-disabled`, and it is a source of defect, not a fix).
> - **CALL B — the channel ⇒ B2: LABEL-LED.** The disabled label drops to a recessive step; the
>   disabled border returns to `--line`, i.e. matching enabled-resting. **Accepted cost, stated in the
>   doc and ruled with it: at rest, enabled and disabled borders become identical and the label carries
>   the whole distinction.** **Not chosen:** border-led (structurally unavailable — see THE SQUEEZE);
>   both (would change an enabled state Dave has not complained about).
> - **CALL C — the gate ⇒ C2: THE WIDE ONE.** *A declaration referencing a custom property that
>   resolves nowhere in its own scope is a build failure, not a silent fallback* — the
>   `fail-loud-on-unknown` shape already ratified for `dv-vocab`. **Not chosen:** the narrow
>   *disabled≠hover* gate (encodes one mechanism as the rule — the failure shape logged twice);
>   the affordance gate C3; the C2+C3 pair. ⚠ **C3 was NOT rejected on merit — it was not selected.**
>   It stays a live candidate in §C·4, because it catches a resolved-but-wrong ladder that C2 cannot see.
>
> ⛔ **STILL UNRULED, AND MUST NOT BE INFERRED FROM THE ABOVE — THE RECESSIVE VALUE ITSELF.**
> The doc offered `#9D9D9D` (canon's `--text-on-disabled` today), `#808080` (B-D4's ruled value),
> `#B5B5B5` and `#6B6B6B` **explicitly as candidates and explicitly NOT as a recommendation**, under
> derivation governance: promotion of a value is Dave's alone. `#9D9D9D` was merely the page's
> pre-selected preview. **Enactment must put the value to him, not read it off this entry.**
> **The light/dark pairing is equally unruled** — candidates were shown paired at the same lightness
> step so the ladder could be judged, which is not the same as a ruling that they pair.
>
> ### ★★ THE SQUEEZE — the finding that produced CALL B, and it was not in the record before #11.
> The remedy the record implied was *"make the disabled border recessive"*. Measured, that is
> **structurally impossible**: the Reset's **enabled resting** border is `var(--line)` `#E1E1E1` at
> **1.31:1** against the page, while the disabled border currently resolves to ink at **17.40:1** —
> **the dead control carries 13.3× the contrast of the live one.** Any disabled border quieter than
> enabled is below the perceptible floor; any border equal to it erases the distinction. **There is no
> third value, so the border channel cannot carry this state at all.** The label channel can: enabled
> label is ink at maximum contrast, leaving a wide recessive-but-visible band — which is precisely the
> band **B-D4** already ruled acceptable ("faint but visible by choice"). ⇒ **The remedy is label-led,
> and the tier question is downstream of the channel question, not the other way round.**
>
> ### ★★ THREE CORRECTIONS TO THE RECORD, verified from source 2026-07-27 #11.
> 1. **`--text-disabled` IS declared on `:root` — the record said it was not.** `canon.css:350` =
>    **`#E1E1E1`**, dark twin `#808080` at `:647`. ⇒ **"Promote to `:root`" is not an untried option;
>    it is already the label token's state, and `#E1E1E1` is exactly the value B-D4 minted
>    `text/on-disabled` to escape.** The prior entry's *"zero `:root`"* was true of
>    `--border-disabled` only and was over-generalised to both.
> 2. **`--border-disabled` census CONFIRMED unchanged:** 29 declarations, ten `.cn-*` form scopes +
>    their SC/dark twins, **zero chart scopes, zero `:root`**.
> 3. **Chart snippets are not in `canon.css`'s cascade at all.** `Chart-bar.reference.html:51–52`
>    links **only** `type.css`, then inlines its own spine. ⇒ **A `:root` fix would reach a real app
>    page and leave the snippet — the thing every render-proof measures — still broken.** This is why
>    A2's declarations must land on the chart scope in the generator, not in a `:root` block.
> 4. ⚠ **VALUE DRIFT, FLAGGED NOT CORRECTED:** B-D4 ruled `text/on-disabled` = `#808080`; canon ships
>    **`--text-on-disabled: #9D9D9D`** (`canon.css:351`) per the later B-D6 four-tier fold. Both are in
>    the ledgers, so this is not drift-in-the-dark — but the two numbers disagree and **the
>    reconciliation is Dave's**, and it collides directly with the unruled recessive value above.
>
> **Evidence:** review doc `reviews/DS-018-DISABLED-STATE-2026-07-27-v1.html` (+ `.REVIEW.html`
> overlay copy) · 2026-07-27 · render-proof `knowledge/_render/verify_ds018_review.py` **30 checks ·
> 0 failures at 1180 and 760**, licensed HSBC cut asserted inside each measured frame, transitions
> killed before every computed read, colours parsed and compared **as colours** · 2026-07-27 ·
> **`--bite` red** (declaring the two properties on a copy resolves the lookup and turns STEP 1 red —
> the probe is not blind) · 2026-07-27 · token census by AST-ish scope walk over `canon/canon.css` ·
> 2026-07-27.
> ⚠ **PROBE WART, banked:** the first run reported the enabled ratio as `11.31:1`. **The doc was
> right (1.31:1); the probe was wrong** — a `\d+\.\d+` regex over the table's *flattened* textContent
> straddled the adjacent `#E1E1E1` cell. **Read cells, never flattened text.** Same family as every
> other instrument defect this week: present, correct-looking, not measuring what it claimed.

> ### ✅✅ RE-VERIFIED 2026-07-27 (session #10) — ds-018 **STANDS**, on a clean instrument.
> **WHY A RE-CHECK WAS OWED:** ds-018 and the later-**withdrawn** ds-019 were measured in one session
> by one probe. When that probe was discredited, ds-018 was left resting on its reputation. *"Should
> not be affected" is not "is not affected"* — and a defect entry surviving on a discredited
> instrument is the confident-false-inscription this project treats as the primary risk.
> **RE-MEASURED** with `knowledge/_render/recheck_ds018.py` — licensed cut asserted, transitions
> settled, **pointer parked** (`hovered` OBSERVED as a field, so the hover rule cannot be mistaken for
> the finding), **4 contexts** (2 Reset instances × 1180/760). **All four identical, and unchanged:**
> **`--border-disabled` → `''`** · **`--text-disabled` → `''`** · **`border-color` → `rgb(26,26,26)`
> = `--ink`** · `color` → `rgb(26,26,26)`. **The timing defect did not reach it.** The census evidence
> (29 declarations, ten FORM scopes, **zero** chart scopes) was always independent of any render and
> is untouched.
>
> **★ AND THE SYMPTOM IS SHARPER THAN "DISABLED LOOKS LIKE HOVER" — THE TWO STATES ARE INVERTED.**
> Measured across the real gesture sequence on one Reset (settled, unhovered, session #10):
>
> | legend state | Reset `:disabled` | `border-top-color` |
> |---|---|---|
> | baseline (all series shown) | **true** | **`rgb(26,26,26)` = `--ink`** |
> | isolated (Reset is live and useful) | false | `rgb(225,225,225)` = `--line` |
> | released (all shown again) | **true** | **`rgb(26,26,26)`** |
>
> ⇒ **The DISABLED Reset is the most prominent control in the legend, and the ENABLED one is the
> faintest.** B-D4 requires disabled to be *visible-but-recessive*; this is not merely a wrong colour,
> it is **an inversion of affordance** — the control shouts loudest exactly when it cannot be used.
> ⚠ **This does not change the CAUSE** (still the lookup, still instance five) **and it does not
> change who rules the fix** — but it raises the stakes on the fix shape, and it is a second, cheaper
> gate candidate in its own right: *a disabled control may not out-contrast its own enabled state.*
> **Evidence:** `knowledge/_render/recheck_ds018.py` + the three-state read · 2026-07-27 session #10.
> **STILL OWED, UNCHANGED — Dave's ruling on the FIX SHAPE** (tier fix + which gate); `--text-disabled`
> fails in the same breath and must be fixed with it. **RE-VERIFIED ≠ FIXED.**
>
> ### ⬛ DAVE'S STEER, 2026-07-27 evening #10 — CAPTURED, NOT ENACTED. Direction only; the tier fix and the gate are still unruled.
> Verbatim, two beats: *"there should be a disabled state for reset"* → then, sharpening it himself:
> *"or, the reset disabled state should look like a disabled state not the hover state."*
> **What this settles:** the remedy is to **make the disabled state real and recessive**. It is NOT
> *"delete the disabled styling"*, and it is NOT *"stop disabling the button"* — both were live readings
> before he sharpened it, and both are now dead. A disabled state for Reset is **already declared**
> (`.dv-leg-reset:disabled{border-color:var(--border-disabled); color:var(--text-disabled)}`) — it has
> simply never been **delivered**, because neither token resolves on a chart scope. ⇒ **The job is to
> make the existing declaration resolve to a recessive value, not to design a new state.**
> **What this does NOT settle, and must not be read as settling:** (a) the **tier** fix — declare the
> form tokens on chart scopes vs mint dataviz-tier equivalents vs promote to `:root`; (b) **which gate**
> — now three candidates (*disabled ≠ hover* · *fail loud on a property that resolves nowhere in its own
> scope* · **new #10:** *a disabled control may not out-contrast its own enabled state*).
> ⚠ **AND A TRAP FOR WHOEVER TAKES THIS — the naive tier answer imports a value B-D4 already rejected.**
> The form tier's `--text-disabled` runs as faint as `#E1E1E1`, while **B-D4 ruled disabled labels to
> `#808080`** — *"faint-but-visible by choice"* — minted precisely because a fainter value was invisible
> to sighted users. **Declaring the form tokens on chart scopes would therefore risk re-creating B-D4's
> original defect on charts.** That pushes toward minting dataviz-tier equivalents, **but it is Dave's
> call and this is an argument, not a ruling.** ⚠ **UNVERIFIED:** which theme/scope the `#E1E1E1` row
> belongs to was NOT checked (window ran out at ~79%) — **confirm it before quoting it as evidence.**

**Status: CONFIRMED (2026-07-27 #8) · RE-VERIFIED on a clean instrument (2026-07-27 #10) · NOT FIXED.
The fix shape is Dave's. Original hypothesis wording kept below, verbatim, for the arc.**

**What Dave saw**, verbatim: *"reset disabled style is set at the hover style."* Screenshot: a legend
row with all three series showing — `A Current`, `B Savings`, `C Investments` all in the plain resting
treatment — and **`Reset` carrying a heavy ink border**. With every series visible and nothing
isolated, Reset is `disabled` by construction (`canon/dv-legend.js:122` —
`st.reset.disabled = (count(st, st.visible) === st.ids.length && !st.isolated)`), so the ink border is
being painted **on the disabled control**.

**Why that is wrong, by rule not by taste.** The declared cascade (`canon.css`, replicated per chart
family at `:3531–3539` bar, `:3696–3704` combo, `:3901–3908` donut) is:

```
.dv-leg-reset            border:1px solid var(--line)              /* resting  */
.dv-leg-reset:hover:not(:disabled)  border-color:var(--ink)        /* hover    */
.dv-leg-reset:disabled   border-color:var(--border-disabled)       /* disabled */
                         color:var(--text-disabled)
```

The rules are **correct as authored** — `:hover` is even properly fenced with `:not(:disabled)`, so
this is not a specificity fight. Yet disabled renders at ink, which is the hover value. And **B-D4
requires disabled to be VISIBLE but recessive** (`_proforma/_BUTTON-DECISIONS.md`; the neighbouring
comment says so in words — *"default DISABLED (token colours, still VISIBLE)"*). Ink is neither.

### ⚠ HYPOTHESIS — stated as a hypothesis, to be PROVEN or KILLED by render, never assumed

If **`--border-disabled` does not resolve in the context being viewed**, `border-color:var(--border-disabled)`
becomes **invalid at computed-value time**, and `border-color` falls back to its inherited/initial
value — `currentColor` — which on this surface is **ink**. **A failed token lookup would therefore
produce exactly the hover appearance, in silence.**

That is the repo's signature defect class, and this would be **instance five**: ds-010 (author CSS beat
`fill=`) · ds-013 (404 stylesheet re-based by `srcdoc`) · the 07-27 black chart keys (local mirror
missing the new var) · ds-016 (index cannot see the rule) · **this**. In every one the markup is
CORRECT, the lookup misses, and **nothing reports it** — see [[silent-lookup-failure-class]].

⚠ **Competing explanation that must be eliminated first:** `--border-disabled` may resolve perfectly
well and simply be *set to an ink-ish value* in the theme in view. That is a token-value bug, not a
lookup bug, and it has a completely different fix. **Do not choose between them by reading CSS** —
`getComputedStyle` on the disabled Reset, in the snippet AND the showroom pane, at two widths, per
`_RUNBOOK-render-verify.md`. Read the *resolved* value of both `--border-disabled` and `border-color`.

### ⚠ ANTI-FALSE-FIX

1. **Do not hard-code a grey on `:disabled`.** That silences the symptom and, if the cause is a failed
   lookup, leaves every other consumer of `--border-disabled` broken and invisible.
2. **Do not "fix" it by tightening the `:hover` selector.** `:not(:disabled)` is already there; a
   change that makes the symptom go away without explaining the ink value has not found the defect.
3. **Fix it in `canon.css`'s generator, not in `canon.css`** — the block is replicated per chart family
   (bar · combo · donut, and line/scatter/sparkline should be checked), so a hand-patch fixes one of N.
   ⇒ If the cause is real, this is a **GATE candidate**, not a patch: *no interactive control may resolve
   its disabled treatment to the same computed value as its hover treatment* — cheap, mechanical, and it
   would have caught this the day it landed. See [[feedback-gate-dont-patch]].

**Found by:** Dave, by eye, from a screenshot — **no gate saw it**, and the declared-pairs contrast
check cannot: both values are legal colours, the defect is that they are the SAME one.
**Related:** DV-D17 (same legend, same session) · B-D4 disabled-but-visible · `dv-016`/`icon-011`,
the two BLOCKING contrast rules the 07-27 instrument-fit pass flagged as having STATIC gates for a
COMPOSITED property — this is that gap, arriving as a real defect.

### ✅ CONFIRMED 2026-07-27 (session #8) — RENDER-MEASURED. It is the LOOKUP. Instance FIVE.

**The hypothesis is PROVEN and the competing explanation is ELIMINATED — by measurement, not by
reading CSS**, exactly as this entry demanded. `getComputedStyle` on the **disabled** Reset, licensed
HSBC cut, `document.fonts.check('16px HSBC_MtUnivers_Latin')` asserted true first, **four contexts:
snippet AND showroom pane (the pane read through `page.frames`, not the top document), at 1180 and
760**. All four returned identical values:

```
--border-disabled   →  ""              ← DOES NOT RESOLVE (empty string)
--text-disabled     →  ""              ← DOES NOT RESOLVE
--ink               →  #1A1A1A         ← resolves fine, so this is not a broken context
border-color        →  rgb(26, 26, 26) ← = #1A1A1A = ink   ⇒ IDENTICAL to :hover
color               →  rgb(26, 26, 26)
```

⇒ `border-color:var(--border-disabled)` is **invalid at computed-value time** → `border-color` takes
its initial value `currentColor`; `color:var(--text-disabled)` is likewise IACVT → `color` is an
inherited property so it becomes `inherit` → ink. **Both roads end at ink, which is the hover value.**

**The competing token-value explanation is dead, and the reason is stronger than the measurement.**
`--border-disabled` is not *set to an ink-ish value* — it is **not set at all, anywhere a chart can
see it**. Source census (`canon/canon.css`, every declaration, by enclosing selector):

- **29 declarations**, on `.cn-input-fields` · `.cn-dropdown` · `.cn-amount-input` · `.cn-date-picker` ·
  `.cn-date-range-picker` · `.cn-file-upload` · `.cn-form-layout` · `.cn-secure-entry` · `.cn-textarea` ·
  `.cn-time-picker` (+ their `[data-apollo-theme="supercharge"]` / dark twins).
- **ZERO on any chart scope. ZERO on `:root`.** `awk` over the file for a declaring selector matching
  `chart|:root|html|body|*` returns nothing.
- The four chart snippets that *use* it declare it **0 times**: `Chart-bar` · `Chart-combo` ·
  `Chart-donut` · `Chart-line` each show `decl=0 use=1` for **both** `--border-disabled` and
  `--text-disabled`. (`Chart-scatter` and `Chart-sparkline` neither use nor declare — they carry no legend.)

**So the defect is a FORM-TIER token consumed from a DATAVIZ-TIER scope.** The `.dv-leg-reset` rule
block was written against a variable that only exists inside form components. It has never resolved on
a chart, in any theme, at any width, since the day it landed — and every gate stayed green throughout.

**Scope of the fix — wider than the symptom Dave reported.** `--text-disabled` fails in the same
breath and is currently masked (inherit happens to land on ink, which *reads* plausible), so a fix
that only addresses `border-color` leaves a second silent lookup in place. Both belong to the
generator, per ANTI-FALSE-FIX 3 — the block is replicated per chart family, so a hand-patch to
`canon.css` fixes one of four and is overwritten on the next regen.

⚠ **GATE, not patch** — the candidate this entry already names is now evidenced twice over:
*no interactive control may resolve its disabled treatment to the same computed value as its hover
treatment.* Add the sibling that would have caught it a layer earlier and cheaper: **a declaration
referencing a custom property that resolves nowhere in its own scope is a build failure, not a
silent fallback** — the *fail-loud-on-unknown* shape already ratified for `dv-vocab` and proposed
for ds-016. ⚠ Neither gate is built; **this is CONFIRMED, not FIXED.**

**Evidence:** `outputs/_render-env/probe.py` + `probe-result.json` · 2026-07-27 · four contexts, font
assert passed in all four · declaration census by `awk` over `canon/canon.css` and `grep -c` over
`snippets/Chart-*.reference.html` · 2026-07-27. Narrative + the false-green it produced:
`_DECISION-HISTORY/2026-07-27-the-treatment-that-never-painted.md`.

---

## ds-019 — ⛔ **WITHDRAWN WITH CAUSE 2026-07-27 (session #9): NOT A DEFECT. It was a MEASUREMENT ARTEFACT — the probe read a computed value in the same task as the class change, i.e. at t=0 of a 160ms transition.** The treatment paints correctly and always did.

> ## ⛔ WITHDRAWAL — read this before the original entry below
>
> **Status: WITHDRAWN. There is no overriding rule. `.dv-legrow.is-solo` paints exactly as authored.**
> **Both beats are kept verbatim** (the original claim is below, unedited) so that a reversal can
> never read as agent drift — per the Memento discipline in `GOOD-MORNING.md` §A.
>
> **What was actually wrong: the instrument, not the CSS.** `.dv-legrow` carries
> `transition: border-color var(--ease), background var(--ease)` = **0.16s**. A computed value read in
> the **same task** as `classList.add('is-solo')` is the **pre-transition** value. Measured time series,
> canon snippet, `.is-solo` applied directly:
>
> | when | `border-top-color` | `background-color` |
> |---|---|---|
> | before add | `rgb(225,225,225)` (`--line`) | `rgba(0, 0, 0, 0)` |
> | **t=0, same task** | **`rgb(225,225,225)`** | **`oklab(0 0 0 / 0)`** ← *the pair the original entry records as proof* |
> | t≈50ms | `rgb(145,145,145)` | `oklab(0.217785 … / 0.0241082)` |
> | **t≈150ms +** | **`rgb(26,26,26)` = `--ink`** ✓ | **`color(srgb 0.101961 … / 0.06)` = 6% ink** ✓ |
>
> **The cascade was never in question.** CDP `CSS.getMatchedStylesForNode` on the node:
> `.dv-legrow.is-solo` **(0,2,0) at cascade index 4**, beating `.dv-legrow` **(0,1,0) at index 3**.
> No `!important`, no inline style, no `attributesStyle`, no keyframes, no `:is()`/`:where()` rule, no
> `#cb4-legend li` rule. **The winning rule that "does not contain the string `dv-legrow`" does not
> exist** — the census that found only four such selectors was correct, and its conclusion was sound;
> the premise it was answering was false.
>
> **Confirmed in six contexts**, all correct: snippet @1180 and @760 · showroom light pane @1180 and
> @760 · showroom **dark** pane @1180 and @760 (theme-tracks properly — `--ink` `#FFFFFF`, 6% white).
>
> ⚠ **`oklab(0 0 0 / 0)` IS THE SIGNATURE OF AN IN-FLIGHT INTERPOLATION, not of a failed declaration.**
> Chromium interpolates `background-color` toward a `color-mix()` result in oklab. Reading it as *"fully
> transparent, therefore the declaration did not win"* is the whole of the error.
>
> **★ AND THE HARDEST PART TO SWALLOW: the predecessor probe's positive control WAS WORKING.** It
> observed `oklab(0 0 0 / 0)` differing from `rgba(0, 0, 0, 0)` and passed — because those genuinely
> are different states (**transitioning-transparent vs static-transparent**). Session #8 diagnosed its
> own control as a string-comparison defect and dismissed the signal. **The string comparison was
> indeed a bad method — and on that reading it was accidentally right.** ⇒ *When a control fires
> unexpectedly, exhaust "it detected something real" before concluding it is broken.*
>
> **Consequences, all recorded 2026-07-27 #9:**
> 1. **DV-D17's render-proof is UNBLOCKED.** It was blocked only by this entry's premise. It is
>    dischargeable — the proof must settle the transition before reading (see 3).
> 2. **Dave's logged question is ANSWERED:** *"if it never painted, what did the DV-D17 screenshot
>    show?"* — it showed the treatment, because the treatment paints. **Screenshot right, probe wrong,
>    for two sessions.** No silent regression, no unprobed context.
> 3. **Structural remedy shipped, not just a note:** `knowledge/_render/cdp_matched_styles.py`
>    (`--settle off` by default) injects `transition:none !important` *before* the class change, so a
>    mid-transition read is impossible; `--settle none` exists solely to reproduce this artefact on
>    demand. Pothole banked in `_RUNBOOK-render-verify.md`.
> 4. **ds-018 is NOT withdrawn and NOT re-verified.** Same instrument, same session — but it measured a
>    **resting** disabled control, not a post-class-change state, so this timing defect should not reach
>    it, and its structural census (29 declarations, ten form scopes, **zero** chart scopes) is an
>    independent line of evidence. ⚠ **"Should not" is not "does not" — a cheap re-check is OWED.**
>
> **The class it actually belongs to.** It is still a sibling of [[silent-lookup-failure-class]], but one
> level further out: **the instrument was present, correct-looking, and not measuring what it claimed** —
> the same shape as #7's stale conformance suite and [[gate-narrows-its-own-rule]]. The difference is
> that this time the false reading was **inscribed as a defect in the corpus** and began directing work.
> ⇒ **`GOOD-MORNING.md` §A is right: the real danger is confident false inscription, not forgetting.**
> This entry is the worked example, and it survived one full session as canon.
>
> **Evidence** · `knowledge/_render/cdp_matched_styles.py` (CDP matched-styles enumeration, cascade
> order, specificity, `!important`, inline + attributes + keyframes) · time series + six-context
> confirmation, licensed cut not staged **deliberately** — cascade resolution is font-independent and
> this measures neither geometry nor paint · bite: `.is-solo` deleted from a copy reproduces the
> original numbers exactly, canon untouched · 2026-07-27.

---

### ⬇ ORIGINAL ENTRY, KEPT VERBATIM — the claim as written 2026-07-27 #8. **It is WRONG.** Retained because a withdrawn claim that vanishes is indistinguishable from drift.

## ~~ds-019 — `.dv-legrow.is-solo` MATCHES, its variables RESOLVE, and it still does not paint: the isolate treatment has never been visible, and DV-D17's render-proof is therefore VACUOUS (2026-07-27, found by a positive control that nearly passed)~~

**~~Status: OBSERVED + MEASURED, cause NOT yet named. Nothing fixed.~~** → **WITHDRAWN, see above.**
**Found by:** the positive control inside DV-D17's own render-proof — the check written to stop that
proof from passing vacuously. It nearly failed to. *(It did not fail. It worked, and was overruled.)*

### What was measured

Licensed HSBC cut, `document.fonts.check` asserted first, snippet `Chart-bar.reference.html`,
legend `#cb4-legend`, `.is-solo` applied **directly** (no gestures, so no behaviour code is involved):

```
element matches '.dv-legrow.is-solo'  →  TRUE
  rule declares: border-color: var(--ink); background: color-mix(in srgb, var(--ink) 6%, transparent)
--ink   on the row  →  #1A1A1A     ← resolves
--line  on the row  →  #E1E1E1     ← resolves
computed border-color →  rgb(225, 225, 225)   ← --line. The .is-solo declaration DID NOT WIN.
computed background   →  oklab(0 0 0 / 0)     ← FULLY TRANSPARENT, not 6% ink
CONTROL: the identical mix written literally on a sibling <div> in the SAME subtree
         →  color(srgb 0.101961 0.101961 0.101961 / 0.06)   ← the mix itself is fine
```

Reproduced at 1180 and 760, snippet and showroom pane (pane read via `page.frames`).

**So: a rule that matches, whose custom properties resolve, whose colour function is valid in the same
subtree, is nonetheless overridden on BOTH its declarations.** The rule census run against the element
enumerated only selectors whose text contains `dv-legrow` — four of them, none of which can beat
`.dv-legrow.is-solo` (0,2,0). ⇒ **The winning rule does not contain the string `dv-legrow`** — candidates
not yet checked: a `:is()`/`:where()` list, a descendant selector via `.dv-leg > li` or `#cb4-legend li`,
an `!important`, or an inline/animated value. **Naming it is the whole of the next step; do not guess it.**

### Why this outranks its own symptom

**DV-D17's owed render-proof is unattainable as specified, and would have read GREEN forever.** The
acceptance test in the handoff is *"confirm no `.dv-legrow` resolves the `.is-solo` treatment (ink
border + 6% ink fill) after isolate-then-check-on"*. **No row resolves that treatment at any time** —
before isolating, during isolation, or after release. The assertion is true, permanently, for a reason
that has nothing to do with DV-D17, and it would have stayed true through a complete revert of the fix.

⇒ **DV-D17 remains ENACTED and DOM-PROVEN (108/108 + 27/27, three neutered controls) and its RENDER
PROOF IS STILL OWED** — it cannot be discharged until the treatment paints. ⚠ **Do not mark it
render-verified on the strength of a green run of the probe as currently written.**

### The class

Sibling of [[silent-lookup-failure-class]] one level up. There the *lookup* misses while the markup is
correct; here the **lookup succeeds, the selector matches, and the paint is still absent** — and again
**nothing reports it**. It also joins ds-018 as the second case today of a dataviz rule that has never
had visible effect, both green in every gate since the day they landed. Related: [[gate-blindspot-state-contrast]]
(declared-pairs checking cannot see a computed-value outcome) · [[feedback-measuring-tool-must-not-guess]].

### ⚠ ANTI-FALSE-FIX

1. **Do not raise specificity or add `!important` to `.is-solo`.** That would make the symptom go away
   without naming what is beating it — and whatever that is presumably beats other rules too.
2. **Do not "fix" it in `canon.css`.** Same reasoning as ds-018 ANTI-FALSE-FIX 3: the block is
   replicated per chart family and regenerated.
3. **Do not treat "DV-D17's probe went green" as evidence of anything** until the positive control
   demonstrably fails on a reverted `dv-legend.js`. It currently cannot.

### ⚠ The probe's own near-miss, recorded because it is the transferable lesson

The first run printed **24 checks · 0 failures**. It was a **false green**. The positive control
compared computed strings, and the solo background serialises as `oklab(0 0 0 / 0)` where the baseline
serialises as `rgba(0, 0, 0, 0)` — **textually different, visually identical (both fully transparent)**
— so the control "saw a difference" and passed. It was caught **by eye, reading the JSON, not by the
check.** ⇒ **Comparing computed colour values requires comparing them as COLOURS (parse to
r/g/b/a), never as strings**, and a control that can pass on a serialisation difference is not a
control. This happened inside the probe written specifically to honour *"assume your probe is wrong in
the direction that reads as green"* — which is the honest measure of how hard that rule is to obey.

**Evidence:** `outputs/_render-env/probe.py` · `outputs/_render-env/diag.py` · `probe-result.json` ·
2026-07-27 · four contexts, font assert passed in all four.
Narrative: `_DECISION-HISTORY/2026-07-27-the-treatment-that-never-painted.md`.

---

## ds-020 — Chart-scatter is the only cartesian chart still drawing axis + grid the pre-DV-D07 way (2026-07-28, session #27, measured)

**Status: ✅ ENACTED #69 (2026-08-01) — the axis/grid migration, with its control.** All five runbook
steps run: roles declared both modes (light `#626262`/`#E1E1E1`, dark `#9D9D9D`/`#484848`, alphas → 1) ·
`.dv-grid`/`line.dv-axis` + all 16 inline grid strokes, 4 axis strokes, 20 axis/label text fills rebound ·
scatter's `extraContract` gained `vars` + `manifestBinds` (contract gate bit on the missing
`#token-manifest` binds, then green) · pre/post control rendered FIRST, both modes, diffed as colours
(pre: ink@.10/.16 → post: exact role values; grid/axis element counts unchanged 16/4, so only the two
channels moved; PNGs + JSON in the #69 session outputs) · narrow-width floor: **Dave's eye still OWED**
— `_REVIEW-SIGNOFF.md` row added #69. ⚠ **The DV-D02-A waiver STAYS, part-discharged**: its clears-when
named TWO conditions under one label — the colour idiom (done) and the `data-fx` fit hooks (6 vs bar's
175, re-measured #69, never scoped into ds-020). Waiver text updated by addition; remaining clears-when
is fit-hook adoption. *(Prior status kept below for the record.)*

**Status as written #27: OPEN. FENCED BY RULING, not by oversight** — Dave ruled it out of DV-J2's scatter half in
plain language ("just the interaction"), *on the attribution argument*, so this entry exists to stop
a deliberate deferral decaying into a forgotten one. It is a **numbered item, not a queue line**
(the assertion-propagation class: §C·1(a)'s STEP-1 sat stale six days and cost the start of #26).

**What was measured** (`Chart-scatter.reference.html` vs `Chart-bar` / `Chart-line`, 2026-07-28):

| | scatter (today) | canon since DV-D07 |
|---|---|---|
| grid stroke | `stroke="var(--ink)"` | `stroke="var(--data-grid)"` |
| grid alpha | `--grid-alpha:.10` light / `.16` dark | `--grid-alpha:1` (colour carries it) |
| axis colour | `var(--baseline)` + `--axis-alpha:.6` | `--data-axis:#626262` light / `#9D9D9D` dark, alpha 1 |
| registry contract | no axis/grid vars | `vars` + `manifestBinds` → `data/axis/*`, `data/grid/*` |

DV-D07 is the **two-channel** ruling (colour and alpha are separate channels; it supersedes the
promotion-time "ink at alpha" idiom). Line, bar and combo carry axis+grid; donut carries axis only
(radial, no gridlines); sparkline is axis-free. **Scatter is the one cartesian member left on the
old idiom** — and since it now sits in the dataviz `$members` map (DV-J2), it is visibly the odd
one out in a group whose other cartesian members all bind the roles.

**Why it was fenced, in Dave's terms:** enacting it moves *every gridline and axis pixel in the
file*, in both modes, in the same commit as the interaction work. A correct change would then be
indistinguishable from a regression by eye — the standing "attribute the diff" rule (a diff you
cannot attribute is not evidence; the `NO_SNAP=1` control in the T-D12 arc is the method).

**What enacting it looks like** (do NOT start it without the control):
1. declare `--data-axis` / `--data-grid` in both theme blocks, alphas → 1;
2. rebind `.dv-grid` and `line.dv-axis` strokes to the role vars;
3. add `vars` + `manifestBinds` to scatter's `extraContract` in `component-types.json`
   (`data/axis/color`, `data/axis/alpha`, `data/grid/color`, `data/grid/alpha`) — the contract gate
   then enforces it;
4. **render the control FIRST**: same widths, pre- and post-, both modes, diffed as colours not
   strings — `knowledge/_render/verify_dv_j2_render.py` is the nearest harness to extend;
5. the narrow-width floor is Dave's eye (the ds-012(b) precedent).

**Sibling, same shape:** ds-012(b) gutter-relative plot area, fenced for the same attribution
reason. If both are ever enacted, they must not share a commit.

**★ A SECOND FINDING, recorded because it is evidence for a promotion already on the board.** While
porting the canon toolbar CSS into scatter I referenced `var(--shadow)` in `.dv-tablepanel` and
`.dv-tip` without declaring it — scatter had never needed it. **The ds-018 C2 gate
(`_validate_property_resolves.py`) caught it in the same build**, correctly, with the right message:
the declaration is invalid at computed-value time and `box-shadow` silently takes its initial value.
Fixed by declaring `--shadow` / `--pop-border` in both theme blocks (matching Chart-bar) and binding
`--shadow → elevation/functional` in the token manifest. **C2 is still ADVISORY** — the promotion to
blocking is DO-FIRST item 1 and is gated on Dave's four values. Had it been blocking, this would have
been a red build instead of a line in an advisory census I had to go looking for; had I not gone
looking, scatter would have shipped a shadowless popover that renders *almost* right. That is the
argument for promotion, and it now has a live instance behind it rather than only a rationale.

---

## ds-021 — The GM growth contracts are denominated in a unit the window does not charge in (2026-07-28, session #30, measured)

*(SUPERSEDED in part — the status block below is a dated historical record: the unit live when written. "Caps bind on `bill`" was superseded by #54/#56 (the unit is REAL Claude tokens, #82-D1); the text is NOT re-denominated, per #82-D1's own rule. Declaration added s163-D1 — this was the #84 audit's named true positive in this file.)*

**★ Status: ENACTED #34 (2026-07-28). Units NAMED by Dave: `tape` (what tiktoken cl100k counts) /
`bill` (what the window charges) — "the tape is not the bill". Caps bind on `bill`, restated at their
current real value and NOT tightened. Three homes edited together: `_RUNBOOK-context-gauge.md`
§ ★ THE UNITS · `_capture_gate.py` (TAPE_TO_BILL + bill_of + fmt_units + ratio_status, pinned) · the
`size:` stamp format (legacy `tk` still parses but WARNS; promotion trigger recorded in-code).
Bites: `selftest_units` — 4 classes, bite-the-bite verified. ⚠ RATIO STILL PROVISIONAL at n=2; the
gate forks to Dave at n≥4.**

*(Original status, kept: OPEN, UNRULED. This is Dave's call — the thresholds are his)* (`_RUNBOOK-context-gauge.md`
§ ★ THE FLOOR IS MEASURED: *"the numbers are Dave's and are re-dialled only by him, here"*).

**What was measured.** Both chain files, two ways, same session:

| | `tiktoken cl100k_base` (what the gate measures) | actually charged on read | ratio |
|---|---|---|---|
| `GOOD-MORNING.md` | 16,107 tk | **25,355 tk** | 1.57× |
| `_LIVE-STATE.md` | 18,818 tk | **29,103 tk** | 1.55× |
| chain floor | 34,925 = 17.5% | **54,458 = 27.2%** | — |

**Why it matters.** Every cap in the 2c–2f growth contracts, and every floor figure in every stratum,
is stated in cl100k tokens. The window is not charged in cl100k tokens. So:

- **GM compactable warn 8,000 / block 12,000 are really ~12,600 / ~18,800 charged.**
- At audit time GM measured **11,899 — 99.2% of block** — while the file actually costs ~18,700.
- The reported floors (#27 16.1% · #28 17.0% · #29 17.2%) understate true fill by **~10 points**.

~2,100 tk of the gap is line-number prefixes, which are a *real* cost — the chain is read through the
Read tool, so the prefix is charged every time. The remaining ~17,400 is tokenizer difference: this
corpus's ★ ⚠ ⛔ · — load prices differently under the two encoders.

**The class.** Same as `measure-dont-convert-units` and #28's *a count is not a measurement*: a proxy
was measured carefully and then reported as the quantity itself. The runbook already warns
*"Measure, never convert by rule of thumb"* about **bytes→tokens** — and then converts
**cl100k-tokens→charged-tokens** at 1.0 without saying so. ⚠️ **The gate is not wrong; it is precise in
the wrong unit**, which is why five sessions of careful measurement never caught it.

**What #30 did NOT do.** Re-dial anything. A falsified constant is UNSET and forked, not replaced by
the finder's own number (derivation governance). The 1.55–1.57× ratio is **observed on two files in one
session** — it is not established as a corpus constant, and a third measurement could move it.

**Remedies, Dave's pick — none started:**
**(a)** Keep cl100k as the measured unit, re-dial the caps to their charged equivalents (one edit,
thresholds stay his). **(b)** Measure and report BOTH numbers in the stamp and the gate output, and
let the caps bind on the charged one. **(c)** Rule the ratio a corpus constant only after it is
measured on a third and fourth file — the honest option, and the slowest.
⚠️ Whichever wins, the fix must reach `_RUNBOOK-context-gauge.md` § THE FLOOR IS MEASURED, the
`_capture_gate.py` cap constants, and the stamp format together — three homes, one unit.

**★ RULED (2026-07-28 19:13 BST, #31 — Dave: "whatever you recommend"; recommendation adopted on his
word, VETOABLE, provenance = delegated pick, not his own derivation):** **(b), with (c) folded in as
standing practice.** Every stamp and gate output reports BOTH numbers with the unit NAMED; **caps bind
on the charged figure**. The caps are RESTATED at their current real value, not silently tightened:
warn ≈ **12.6K charged** / block ≈ **18.8K charged** (≡ today's 8K/12K cl100k at the provisional
×1.57). The ratio stays PROVISIONAL — each wrap logs one cl100k↔charged pair (the Read-tool count vs
tiktoken, free at every chain read) into `notes/_GAUGE-LOG.md` until n≥4 files, then the constant is
put to Dave. Three homes still owed together: runbook § THE FLOOR IS MEASURED · `_capture_gate.py`
caps · the stamp format.
[born #30 · ruled #31 (delegated) · guards: this entry · until: the three homes are edited + ratio firmed at n≥4]

---

## ds-022 — Step 2f's stratum split is discipline with no receipt: nothing reads `_GAUGE-LOG.md` (2026-07-28, session #30, measured)

**★ Status: ENACTED #34 (2026-07-28) as ruled — (c) guarded by (a).** `_gm_move.py` gains the
`roll_2f` op: both halves or neither, both destinations APPENDED at true EOF (no anchor argument
exists, because the anchor is what produced #27's prepend), duplicate + out-of-order + unkeyed
blocks all refused. `_capture_gate.py::gauge_log_continuity` is BLOCKING at birth: a wrap fails
unless N−1 has a block or an explicit `HOLE #<N> — <why>`. Runbook step 2f rewritten to run the op.
Bites: 6 in the mover (incl. the append-order bite that would have caught #27), 4 in the gate.
★ **CLOSED BY DAVE, #34 — a THIRD state, `ABSENT`.** #9/#10/#11/#19 had no block and no note.
`HOLE #<N>` is a POSITIVE claim (*"that session wrote no stratum"*) and writing four would have made the log
read complete **at the price of four invented facts** — confident false inscription, committed to tidy a
file. **`ABSENT #<N>` is a claim about the RECORD, not the session:** no block found, cause UNKNOWN. The
four are now countable as unknowns and **the dataset accounts for every session 6→33 with zero gaps**.
⚠ The gate **WARNS** on `ABSENT` rather than passing it — a silent one would become a free skip for step 2f,
i.e. `HOLE` with the honesty removed. After #34 there should never be a new `ABSENT`.

*(Original status, kept: OPEN, UNRULED. Repair done at #30's wrap; the mechanism is untouched.)*

**The rule** (capture ritual step 2f): at each wrap the older stratum splits — **post-mortems →
`notes/_GAUGE-LOG.md`** (append-only, chronological, one block per session) · **commit-states →
`_GM-ARCHIVE.md`**. The log exists so the throttle programme is not reasoning from n=1.

**What was observed** (`grep '^#### ' notes/_GAUGE-LOG.md`, 2026-07-28):

- blocks present: **#6 #7 #8 · #12–#18 · #20–#25 · #27**
- **#26, #28, #29 never arrived** — their strata rolled WHOLE into `_GM-ARCHIVE.md` instead of splitting
- **#9 #10 #11 #19 absent with no HOLE line**, so the file cannot say whether a stratum ever existed
  (#14 is the counter-example: its absence was flagged, so #14 is countable)
- **#27's block sits at line 7, above the #6→#25 run** — prepended by #28's wrap, against this file's
  own declared APPEND-ONLY · chronological contract

**#29 is the expensive loss.** It is the only 🔴 RED session on the board and the only one with a
measured overrun cause. Its closed band lived on a Polaroid (`GOOD-MORNING.md`) and never reached the
tattoo. Dream-pass-3 **P1(a)** rules *record-FIRST-then-quote — one number, one source*; #29 quoted a
number it had not recorded, which is the #18 failure the rule was written to prevent, one ruling later.

**Why it kept happening: no gate can see it.** `grep -n 'GAUGE-LOG' knowledge/*.py` returns four hits,
**all comments or docstrings — zero checks.** The wrap gate verifies §C lines, compactable size, chain
size, banner region, retirement receipts, section-usage FORM, consult-receipts FORM, lane-routing and
pre-flight FORM. It does not verify that the post-mortem it just displaced landed anywhere.
**This is the gate-don't-patch trigger:** three wraps in a row got the same step wrong, which is the
definition of a condition that should be gated rather than remembered.

**Remedies, Dave's pick — none started:**
**(a)** A wrap check: the session number in GM's stratum must be N, and N−1 must have a block in
`_GAUGE-LOG.md` — FAIL otherwise. Cheap, catches exactly this. **(b)** Same check, plus assert the
file's own contract (chronological, one block per session, no duplicate keys). **(c)** Fold the roll
into `_gm_move.py` so it cannot be done by hand at all — the M5 argument, applied one step further.
⚠️ **(a) needs a HOLE escape hatch** or it will block a wrap whose predecessor legitimately wrote no
stratum — the P1(b) line must satisfy the check, or the gate will teach sessions to fake blocks.

**★ RULED (2026-07-28 19:13 BST, #31 — Dave: "whatever you recommend"; recommendation adopted on his
word, VETOABLE, provenance = delegated pick):** **(c) guarded by (a).** The 2f roll folds into
`_gm_move.py` so the split cannot be done by hand (the M5 argument); the wrap gate gains the N−1
check — a wrap FAILS unless session N−1 has a block **or an explicit HOLE line** in
`notes/_GAUGE-LOG.md`. (b)'s contract asserts (chronological · one block per session · no duplicate
keys) ride along only if cheap at build time — not required for the ruling to be enacted.
[born #30 · ruled #31 (delegated) · guards: this entry + the GAPS block in `notes/_GAUGE-LOG.md` · until: mover fold + N−1 check land]

---

## ds-023 — The reserve is being read as additive headroom, which the canon forbids by name (2026-07-28, session #30, Dave by eye)

**★★ SUPERSEDED IN SHAPE #37 (2026-07-29) — THIS IS A BAND, NOT A CEILING. Dave re-stated it at
#36 and #37 enacted it.** `45–60` is the PREFERRED BAND for the FULL price (front-load + context GM
+ job + wrap); `60` is the line and is LIVABLE; `61–63` is tolerable when RARE and MARKED. **45 was
never a ceiling** — the `>= 45 -> FAIL` below was picked by a *delegated agent* at #31, never ruled
by Dave, and it was failing the very zone it existed to steer sessions into. `PREFLIGHT_CEILING` is
gone; `BAND_FLOOR` / `HARD_STOP` / `MARKED_MAX` are pinned to `(45, 60, 63)`. Whole arc:
`GOOD-MORNING.md` § ★ LATEST #36 · `_LIVE-STATE.md` § ⏱ LATEST DELTA #37 ·
`_DECISION-HISTORY/2026-07-29-the-ceiling-was-never-a-ceiling.md`.

⬛ **OPEN AND DAVE'S — the ONLY part of ds-023 still unruled: what happens ABOVE 63.** He ruled the
band and the marked tolerance and nothing beyond. #37 deliberately **kept the pre-#36 escape-hatch
shape** there (marked → WARN, unmarked → FAIL) rather than inventing a harder stop, and the gate
*says* `UNRULED` in the message. A pinned assertion in `selftest_preflight` fails if a later session
quietly fills that silence — **because filling exactly this kind of silence is how `>= 45 -> FAIL`
got in.** ⚠ Do not resolve this by reasoning; it needs his words.

*(Everything below is the #30→#34 record, kept verbatim. It is the evidence that only the
ENFORCEMENT ever moved — the underlying reserve arithmetic was never in dispute.)*

**★ Status: ENACTED #34 (2026-07-28), Dave confirming — "this is making me suffer unduly".**
`_capture_gate.py::check_preflight` now enforces the CEILING (`fill + job + wrap ≤ 45`, FAIL) with the
canonical escape `RESERVE SPEND — forked to Dave` (WARN + receipt), and publishes the in-flight stop
line `60 − the priced wrap` on BOTH the passing and the over-ceiling path — it moves with the wrap
price and is bitten for it. Runbook § ds-023 documents the marker where the rule is, not only in the
regex. Bites: 3 fixtures + 5 assertions; ceiling/stop pinned at (45, 60).
★ **BOTH RESIDUALS CLOSED BY DAVE, #34, same window.** (1) **The one-point slack is gone: `< 45`, not
`≤ 45` — 45 itself now FAILS**, because 45 is AMBER and the rule is "project to finish GREEN". #34 shipped
the literal `≤` and forked the contradiction rather than picking the stricter reading unasked; Dave ruled
it. Boundary bitten (44 pass · 45 fail · 46 fail), and the fixture that read *"at the ceiling exactly —
allowed"* was **FLIPPED to FAIL rather than deleted**, so the change stays legible. (2) **The marker stays
STRICT**, cost accepted and named: #33's stamp was correct behaviour in different words and this gate fails
it, but loosening to any prose containing "forked to Dave" would let the receipt be produced by accident —
**and a receipt that can be produced by accident is not a receipt.** Mitigation: the literal is documented
in the RULE (`_RUNBOOK-context-gauge.md`), not only in the regex.

*(Original status, kept: OPEN. The SHAPE is already ruled — what is missing is a CEILING and a check.
The ceiling number is Dave's.)*

**Dave's words, #30:** *"I think that calibration of the headroom is wrong… I think it's calculating
60+15 headroom is okay and it definitely isn't, 60 should be a hard stop."*

**He is right, and `_RUNBOOK-context-gauge.md` already agrees with him — three times, verbatim:**

> The RESERVE … is **not** a fourth addend: adding it to the projection is exactly the **thermometer**
> — it reported how hot the session was and never once told it to stop.

> **RULED (a) — the reserve is RING-FENCED, not additive. ~15%.**

> ANTI-FALSE-FIX 2. **The reserve is a LINE, not an allowance.** `fill + job + wrap + 15%` is not a
> budget to run to; crossing the line is a **question put to Dave.**

⇒ **This is not a calibration gap. It is an enforcement gap** — the third of this session's three, and
the same shape as ds-021 and ds-022: the rule exists, is correct, is ratified, and nothing checks it.

**The arithmetic the rule implies, and the reason nobody was doing it.** If RED (≥60%) is a hard stop
and the ~15% reserve is ring-fenced *inside* it, the ceiling on any pre-flight is:

```
fill + job + wrap  ≤  45%          (= the GREEN ceiling, unchanged)
```

**i.e. a job must be projected to finish GREEN.** The reserve is what makes AMBER a *fork* zone rather
than a working zone. ⚠️ **This falls out of Dave's own ratified numbers — it is NOT a new threshold and
was NOT self-promoted.** The 45% is written here as the derivation, not as the rule; **the ceiling is
his to confirm or re-dial** (derivation governance, and the band numbers are explicitly his alone).

**The evidence — two consecutive sessions, both passing every gate:**

| | stamped pre-flight | vs 45% ceiling | closed |
|---|---|---|---|
| **#29** | `fill 17 + job 25 + wrap 8 = 50% AMBER-projected` | **over at the opener** | 🔴 68–72% |
| **#30** | `fill 27 + job 15 + wrap 10 = 52% AMBER-projected` | **over at the opener** | 🟡 est. |

- **#29 then built a new instrument from an AMBER projection**, which the Amber rule forbids in terms
  (*"DO NOT START A NEW BUILD ARTEFACT AT AMBER"*). It closed 68–72%: it did not merely spend the
  reserve, **it exceeded it**.
- ⚠️ **Compose ds-021 with this and #29 gets worse.** Its fill was not 17% — measured in the unit the
  window actually charges, it was **~27%**. The true pre-flight was **27 + 25 + 8 = 60% before a single
  tool call**, plus 15% ring-fenced. **There was no session there**, and no instrument in the programme
  could see it: the floor was measured in the wrong unit (ds-021) and the projection was never compared
  to a ceiling (this entry).
- **#30 committed the identical error in the session that found it** — stamped 52%, proceeded, and the
  wrap gate passed it. Recorded here rather than regretted, per the ds-018/#28 discipline.

**Why every existing mechanism missed it.** The band table describes *fill*. The reserve rule describes
*a line*. `_capture_gate.py` checks the stamp's **three terms, its arithmetic, and that the stated band
matches the table** — and it does bite: it caught #30's own first stamp for calling 27% AMBER when the
table says GREEN. **But no check compares the projection to a permissible maximum.** So a stamp can be
arithmetically perfect, correctly banded, gate-green, and describe a session the canon forbids.

**Remedies — Dave's pick, none started:**
**(a)** One wrap/pre-flight check: `fill + job + wrap` ≤ ceiling, else FAIL unless the stamp carries an
explicit `RESERVE SPEND — forked to Dave` marker. Cheap; reuses the existing stamp parser.
**(b)** (a) plus a **stop rule at 60%**: no new build artefact, no new file, wrap only — making RED
mechanical rather than advisory (M1 already says this for wraps; it is not enforced).
**(c)** Re-dial the reserve instead of the ceiling — the runbook itself flags 15% as **provisional,
"sized from n=3 with one value unknown"**, and asks to re-derive after ~5 more recorded overruns.
⚠️ **ds-022 blocks (c):** re-deriving needs the overrun dataset, and `notes/_GAUGE-LOG.md` is missing
#26/#28/#29 — including #29, the **only RED session and the largest overrun on the board**. **Fix
ds-022 first or (c) is being computed on a corpus with its most informative point deleted.**

**★ RULED IN PART (2026-07-28 19:13 BST, #31, Dave, plain language — verbatim):** *"the wrap should be
done before we hit that mark thats when thing go wrong"* → *"so we should never run hot, the wrap
should try and stay below 60, does that answer the question, we need to a handle on this."*
**Read-back (reflected in-chat, confirmed by the second beat):** 60 is where the wrap must have
**FINISHED**, not where it starts — starting the ritual at 60 is what spends the reserve (#28/#29's
recorded failure). ⇒ the in-flight **stop-and-wrap trigger = 60 − the priced wrap** (~50–52 at the
current 8–10-point wraps; moves with the wrap price, is not its own constant). "Never run hot" is the
standing posture. The pre-flight ceiling stays the derivation above (fill + job + wrap ≤ 45,
projected-GREEN) — **still his to confirm or re-dial, not yet confirmed in terms.**
**★ ENFORCEMENT PICKED (2026-07-28 19:13 BST, #31 — Dave: "whatever you recommend"; adopted on his
word, VETOABLE, provenance = delegated pick): (b) + (a)'s pre-flight check.** Mechanical stop at
**60 − the priced wrap** (wrap-only beyond it; RED stays wrap-only per M1) · pre-flight check
`fill + job + wrap ≤ 45` with the explicit `RESERVE SPEND — forked to Dave` escape marker. **The 45
is CONFIRMED by the same delegation** — flagged as adopted-on-recommendation, not his own derivation;
re-dial remains his at any time. **(c) stays blocked by ds-022** until the log holds ~5 recorded
overruns, then the 15% reserve is re-derived and put to him.
[born #30 · ruled-in-part #31 · enforcement picked #31 (delegated) · guards: this entry + the GM header · until: the checks land in `_capture_gate.py`]

## ds-024 — The wrap gate does not run the build, so a RED build survives any number of wraps (2026-07-28, session #32, measured)

**Status: ENACTED IN PART — the specific hole is closed and gated. The GENERAL question is
OPEN and Dave's.**

**Measured at #32's opener.** `_memento_search.py --fetch gm:LATEST` returned **#29's banner**
while `GOOD-MORNING.md` carried **#31's**. Three links, each verified against the repo (`git log`,
a real run of the builder, a real run of `_build_all.py`) rather than reasoned about:

1. The index regenerates inside `_build_all.py`; the **wrap** rewrites GM/LS *afterwards*. Retrieval
   is one session behind **by construction**.
2. It could not regenerate at all: #30's ds-022 repair wrote `#### GAPS FOUND AT #30's AUDIT`, and
   `_build_memento_index.py` refuses any `#### ` that is not `#### YYYY-MM-DD #N` (the ds-016
   fail-loud contract, working exactly as designed). The step exited 1.
3. ⇒ **`_build_all.py` was RED at step 65/72 from `f2c083a` onward, and #30 and #31 BOTH wrapped and
   committed over it** — because the wrap gate does not run the build.

⚠️ **The session that fixed one silent-record failure opened another one layer down.** ds-022 was
"nothing reads `_GAUGE-LOG.md`"; its repair broke the index; nothing was watching *that*. Three
sessions of work — including the ds-021/022/023 throttle rulings — were committed on a red build by
agents who each believed they had verified their state. **And RETRIEVAL-FIRST is standing canon**, so
the door was pointing every session at a superseded record with full confidence: the
confident-false-inscription class, inside the mechanism built to prevent it.

**✅ ENACTED #32 (commit `b62d4c6`), and deliberately narrow:**
- `_build_memento_index.py` — a SECOND declared gauge-log form, `#### META — <title>`; every other
  `#### ` still refuses. Declared, not enumerated (dv-004 shape). 5 bites.
- `_capture_gate.py::index_freshness_check` — **BLOCKING at birth.** Rebuilds in-process, byte-compares
  against disk. **Content, never mtime** — an mtime check reads green on a reverted file (DV-D17
  shape). 4 bites, the FIRST of which is the positive one (fresh passes AND says FRESH), because a
  failure-only suite survives a revert that deletes the comparison.
- `_RUNBOOK-capture-ritual.md` **step 2g** — rebuild the index LAST, after every GM/LS edit is final.
  The ordering is the fix; the gate is what stops it rotting.
- Proven end-to-end on the live repo, not fixtures: runbook edit → gate RED → 2g → gate GREEN.

**⬛ OPEN — Dave's, and the general form is the point:**
**(a)** Should the wrap gate **run `_build_all.py`** (or a fast subset) rather than trusting that some
earlier call in the session did? ⚠️ Price it honestly: the build takes most of a 45s call, and a wrap
gate that costs a call every time will get worked around — which is how we got here. A `--since-HEAD`
subset may be the real answer.
**(b)** Or: a cheap **build-freshness stamp** — `_build_all.py` records its exit + HEAD, the wrap gate
refuses to close if the last recorded green build predates the session's first commit. Cheaper than (a),
catches the same class, does not catch a build that was never run at all.
**(c)** Neither — declare that a red build is the session's own discipline. ⚠️ That is the status quo,
and the status quo produced two sessions of commits over a red build.

**★ THE CLASS, and it is bigger than this entry.** #32 found three instruments this session whose
output **nothing consumes**, and they are the same defect wearing different clothes:
- **ds-022** — `_GAUGE-LOG.md` measurements, no gate reads them.
- **the section-usage lines** — `PRIOR` referenced-never-consumed **8 of 8** sessions; `C2b`/`C3`/`C4b`/`C5`
  unused **five sessions running**; ~3,275 tk cl100k carried dead every window. The #23 emitter and the
  #24 FORM check both exist; neither asks what the accumulated data *says*. **UNBUILT — #33's.**
- **this entry** — the build runs, and the wrap never asks whether it passed.

⇒ **Building the instrument feels like closing the gap, and it is only ever half.** Proposed standing
rule, Dave's to accept: **an instrument ships with its consumer, or it ships as ADVISORY with a named
trigger and a dated review** — never as a measurement with no reader. *(Sibling of gate-don't-patch,
and of the ADR-0016 CLAIMED-vs-UNPROVEN distinction: an unread instrument is UNPROVEN wearing green.)*

**⬛ ALSO OPEN, same session, NOT started (both refused at Amber as new build artefacts):**
- **The eager read chain (GM-D7-am) is why JIT cannot work.** The contract mandates §A + LATEST + §C +
  whole `_LIVE-STATE.md` — **~33K tk before any question is asked.** `_memento_search.py` is a working
  two-stage door over 255 records and **cannot save a token the contract has already spent.** §A alone
  is 4,208 tk, static, loaded every window. ⚠️ The standing instruction says **never drop §A** — read for
  eleven sessions as *always read it*. **Those are separable decisions and nobody had separated them.**
  Dave ruled the cut GO at #32 ("lets do it your way"); it is UNBUILT. **#33's first job.**
- **Growth: the contract caps what ROLLS, not what ACCRETES.** Measured over 30 commits: GM 26,323 →
  **12,780** at the #16 enactment → **15,347** twenty-four hours later (**+20%, ~+150 tk/wrap**); LS
  16,037 → 18,579 (**+16%**). DO-FIRST (2,474) and §C·4 (1,435) carry it. A cap on the rolling sections
  **reads like** a cap on the file and is not one.

**⚠ WART FOUND WHILE WRAPPING #32 (small, real, unfixed).** `_gm_usage.validate_stratum()` selects the
line to validate with `if "section-usage" in ln and ln.lstrip().startswith(">")` and validates
**`usage[0]`** — a **substring match**, the ds-018 silent-lookup class. #32's own stratum LESSON line
mentioned *"the section-usage lines"* in prose and was therefore picked up and reported MALFORMED,
while the real, well-formed usage line two lines below was never examined. **The failure reads exactly
like a genuine false inscription**, which is the worst possible disguise for a lookup bug. Worked
around by rewording the prose; the selector should anchor on the line-START form (`^>\s*\*\*section-usage`)
like every other anchor in this programme. One line, plus a bite that puts the phrase in neighbouring
prose and proves the real line is still the one validated. **#33, cheap.**

## ds-025 — Every load-bearing number in the throttle is one no session can observe from inside itself (2026-07-29, session #37, measured)

**Status: OPEN. The measurement is done and is not in dispute; the REMEDY is a ruling and is Dave's
alone, because it changes what the agent is allowed to assert.**

**Three numbers hold up the whole gauge, and not one of them is observable from inside the window
that depends on it:**

1. **THE BOOT (front-load).** Never measured by any session in 36. Carried as *"~17 of a ~20-pt
   floor"*. Measured at #37, the DISK-RESIDENT half alone: **17,810 tape / ~27,961 bill / ~14.0 pts**
   — `MEMORY.md` 4,517 · reconstructed `available_skills` (37 SKILL.md) 5,684 · GM lines 1–120 6,253 ·
   LS delta 1,356. The harness half (system prompt, tool schemas, MCP instruction blocks) is **not on
   disk and not reachable from the sandbox** — the session transcript is outside every mount. ⇒ the
   real boot is almost certainly well above the inherited ~17, and **every pre-flight in this repo
   has been priced on the low figure.**

   ⛔⛔ **PART-FALSIFIED #52 (2026-07-30) — THE SENTENCE ABOVE IS WRONG AND THIS IS THE CORRECTION AT
   SOURCE.** *"The session transcript is outside every mount"* is FALSE: the live transcript sits at
   `.claude/projects/<project>/<sessionId>.jsonl` and **IS readable from the sandbox**. It can be
   measured with `tiktoken` there and never loaded into the window, so **the reading is free.**
   Confirmed as the live session by matching `sessionId`, timestamps and content probes.
   **MEASURED #52, `cl100k`: conversation half 613,386 tape** (`user`/tool-results 426,344 ·
   `assistant` 168,587 · `attachment` 18,455; meta records excluded). ⚠ **A cumulative log is not a
   fill reading** — that figure is THROUGHPUT, and it assumes no compaction/eviction, which is
   DECLARED not verified. ⚠ **SCOPE, and it matters: only the CONVERSATION half is now observable.
   The boot half — system prompt, tool schemas, MCP instruction blocks — has NO record type in that
   file, so THIS ITEM'S HEADLINE CLAIM STANDS: the boot is still unmeasured after 36 sessions.**
   ⇒ **`ds-025` is NOT closed; item 1 is narrowed.** ★ Found because Dave used the check-in
   mechanism he ruled the same hour (*"how hot are we now?"*) — **an instrument's first run
   disconfirmed the premise it was built on.** → `notes/_MEMENTO-DECISIONS.md` § ★★ #52.

   ⛔⛔ **RE-SCOPED #109 (2026-08-06), RULED #109-D3 — THE HEADLINE CLAIM ABOVE ("the boot is still
   unmeasured after 36 sessions") IS NOW FALSE AND THIS IS THE CORRECTION AT SOURCE.** The harness
   half IS observable — not from disk, but directly via `message.usage` at first turn, which was
   available the whole time and simply not used as the boot instrument. **Measured, n=5 (#103 65,023
   · #104 64,765 · #105 67,370 · #107 65,046 · #109 64,778): first turn 65,400 ± 1,400 real.** Plus
   `_CHAIN.md` (10,499 real), which lands ADDITIVELY at turn 2, not inside the boot figure — the prior
   `boot = disk + harness` shape summed two different conversation MOMENTS as though they were two
   halves of one thing, a second defect independent of the stale `20,000` constant it was carrying.
   **Corrected floor: 75,899, published as 30,499 — under-reported by 45,400.** Enacted in
   `knowledge/_gauge_tokens.py` (`BOOT_FIRSTTURN_TK`/`BOOT_FIRSTTURN_ERR`, replacing
   `BOOT_HARNESS_EST`/`_ERR`); Dave approved the RE-SCOPE below, not yet the code line-by-line
   (ENACTED + UNRATIFIED). ⇒ **item 1 NARROWS AGAIN, not closes:** the boot TOTAL is measured and
   that half is done; item 1 now means the DECOMPOSITION of the 65,400 first-turn figure only —
   `MEMORY.md` 8,470 is split out and measured (#109), **56,308 remains unattributed** (system prompt
   + tool schemas + deferred-tool list + MCP server instructions + CLAUDE.md — bounded and named, not
   yet split). Closes when the 56,308 splits, not before. Four-phase plan (split · cut unauthenticated
   MCP boot rent · gate the ceiling · the smaller `_CHAIN.md` trim) priced for #110, governed by
   `ds-036` (#109-D4, verbatim: *"no patches no sticking plasters"*), awaiting Dave's confirm to open.
   Full arc: `_DECISION-HISTORY/2026-08-06-109-boot-floor-measured.md`. → `notes/_MEMENTO-DECISIONS.md`
   § ★ #109.
2. **`bill`.** ds-021(c) requires one `tape`/`bill` pair per wrap and sends the constant to Dave at
   **n≥4**. Measured at #37: `notes/_GAUGE-LOG.md` has **never contained a single pair** (`grep -i
   bill` → 0 hits, all sessions). `TAPE_TO_BILL = 1.57` is still the original **n=2** from #30. The
   reason is not laziness — **`bill` is what the WINDOW CHARGES, and a session cannot read its own
   meter.** The instrument was asked for a number it structurally cannot produce.
3. **`fill`.** `_capture_gate.py` says so itself, in its own header: *"It CANNOT check whether the
   fill figure is honest… it has no access to the token tally, and a guessed number wearing a gate's
   authority is the failure this programme exists to stop."* Correct — and it means the first term of
   every pre-flight stamp is an agent's estimate.

★ **THE SHAPE.** This is [[measuring-tool-must-not-guess]] at programme scale: **a number the
instrument cannot observe will be supplied by estimate forever, and estimates do not announce
themselves as estimates once they are written into a stamp.** Dave's #36 band makes it sharper, not
softer — the band is denominated in the FULL price, so the unmeasured boot sits *inside* the ruled
quantity. The band is only as honest as its floor.

**PROPOSED, HIS TO RULE (three options, deliberately not chosen here):**
- **(a) Dave-supplied inputs.** `fill` and `bill` become pasted observations like the **pace panel**
  already is — he can read the meter, the agent cannot. Worked precedent: he pasted the panel at #37
  and it priced the session honestly in one line.
- **(b) REFUSE rather than estimate.** #36 raised this for the size checks (the gate silently
  degrades to `bytes/3.53` without `tiktoken` and **under-reports by 414 tape**, i.e. fails UNSAFE).
  Generalised: an unobservable term is `UNKNOWN`, and `UNKNOWN` blocks rather than defaults.
- **(c) Publish the split.** Keep estimating, but every stamp states which terms are MEASURED and
  which are ESTIMATED, so the boot's status can never again be invisible for 36 sessions.

⚠ **Do NOT let an agent pick between these.** ds-023 is the cautionary case in this very file: a
delegated agent chose an enforcement Dave never ruled and it stood for six sessions.

**Cheap first step regardless of the ruling:** the boot's disk-resident half is now measurable in one
script (~15 lines, `tiktoken` + the mounted paths) and should be re-measured per session rather than
inherited — it is *"a variable this programme shrinks"* (GM-D9), and nobody has ever watched it move.

## ds-026 — dv-lockup could carry a dedicated INSIGHT slot (2026-08-01, session #69, FLOATED — Dave's)

**Register: FLOATED, not ruled, not scoped.** While ruling the three #68 lockup placeholder titles,
Dave: *"I quite like adding in the insight somewhere, lets note as a refinement for later."*

Context: the house title register is already insight-led sentence case ("Housing takes two fifths of
the month's spend"), so today the title carries the insight implicitly. The floated refinement is a
possible *dedicated* insight slot in the dv-lockup — distinct from the title — so a chart could pair
a neutral title with an explicit insight line (or similar; the shape is undecided).

Mechanics if it ever scopes: AUTO-MARKUP already supports per-figure instance data via
`data-lockup-*` attributes (#68), so a `data-lockup-insight` + optional markup partial is the
natural grain — but that is an observation about the machinery, not a proposal Dave has seen.
Promotion is Dave's, per derivation governance.

---

**★ #86 (2026-08-02, triage-bankruptcy — inscribed #87): DS-018's recessive value is now a STANDING
GOVERNING RECORD (G11).** Dave accepted the close condition via the ratified review export
(`reviews/TRIAGE-BANKRUPTCY-2026-08-02-v1.html`, 19/19): **closes when Dave picks the recessive
value** — four candidates incl. `#9D9D9D`, still explicitly NOT a recommendation, per the
⛔ STILL-UNRULED block above (unchanged by this entry). Register: `knowledge/_GOVERNING-RECORDS.md`
G11 · ledger: `notes/_MEMENTO-DECISIONS.md` § ★ #86-D1.

## 2026-08-05 #99 — opacity primitives enactment: two registered follow-ons (agent's, not rulings)

1. **`--pri-hover` stored colour-equivalents are now derived at a retired strength.** #99-D1 migrated
   the primary-hover mix from 0.70 (ADR-0009/B-D3) to `--alpha-68`; the STORED chromatic equivalents
   (`#626262`/`#B7B7B7`, `button/primary/background/hover`, bound in manifests for colour-only
   consumers) were derived at 0.70 and are NOT re-derived here — a re-derivation is a measurement on
   the rendered mix (light ≈ `#636363`, MEASURED #99 render: srgb 0.389333 = 99.28), not an
   arithmetic conversion, and touching a stored token is Dave's promotion. Registered, declared in
   the Button snippet header comment.
2. **The literal-opacity corpus is far wider than the five migrated sites.** Sweep MEASURED #99:
   125 literal `opacity:.N` declarations across 49 snippet files (`grep -rE 'opacity:\s*\.'`,
   var()-bound and 0/1 excluded) — chart state classes (`.is-faded:.24`, `.is-ghost:.12`), harness
   chrome (`h2 .6` in ~40 files), `.45`/`.75`/`.7` strays. The #99 enactment scoped to the five
   sites in the ratified review table; the wider sweep is FORKED to Dave (sweep-now vs
   per-component-as-opened), not silently widened.

**★ #102 (2026-08-05): the #99 literal-opacity corpus fork is CLOSED — Dave ruled SWEEP-NOW (#102-D1,
ds-028).** 182 occurrences / 131 lines / 50 files migrated to the `--alpha-*` ladder in one pass,
non-ladder values rounded DOWN per #99-D3; residual ③ (Input-fields `p.note` .75→72) swept under the
same ruling. Residual ① (`--pri-hover` stored equivalents at 0.70) remains OPEN — Dave's promotion.
Evidence: ledger § ★ #102 · snippet gate 75/0 · showroom `--check` OK.

---

## ds-037 — The rules index cannot tell an ENFORCED rule from a BLOCKING-DERIVABLE CANDIDATE (2026-08-06, session #114, measured — agent's finding, NOT a ruling)

**Status:** LOGGED #114, per this register's own 2026-07-03 governance section (*log the
recommendation here, with supporting artifacts, and move on*). ⛔ **Nothing here is promoted, and no
tier is changed** — enforcement tiers are Dave's alone.

**Finding (the SECOND index defect, surfaced by the ds-016 dossier — the first is ds-016 itself).**
The rules-index extraction regex reads only the literal alternation `[BLOCKING|ADVISORY|TASTE|REVIEW`.
That vocabulary has no term for a rule that is *derivable as blocking* but *not enforced by any live
gate* — so both collapse into the same `BLOCKING` bucket. **Measured: 51 of the index's `BLOCKING`
entries are BLOCKING-DERIVABLE CANDIDATES, not enforced rules.**

**Why it matters, and it is the ds-016 failure one level up.** ds-016's headline — *7 live gates cite
rules the index cannot see* — is about rules MISSING from the index. This is the mirror image:
**rules PRESENT in the index under a status the index cannot actually justify.** A count of "blocking
rules" taken off this index is therefore an over-count of enforcement by up to 51, and every
downstream instrument-fit number inherits it [[measure-dont-convert-units]]. ★ The general form: **a
vocabulary with no word for a state cannot report that state — it reports the nearest word it has,
confidently** [[scope-blindness-gate-vocabulary]] [[honest-refusal-needs-a-legal-form]].

**Evidence:** the ds-016 dossier work of #114 (remedy (b) enactment, `0678f7f`); the regex itself in
the rules-index builder; `knowledge/guidelines/_rules-index.json`.

**Prepared-but-unpromoted candidate remedy (evidence, not canon):** widen the status vocabulary by
one term — e.g. `BLOCKING-DERIVABLE` — and make the extractor **FAIL LOUD on an unregistered status
word** rather than bucketing it, the dv-vocab pattern already used by `_gm_usage.py`. ⚠ **This would
re-price ds-016's published figures**, which is exactly why it is logged rather than done: the
numbers Dave has already been shown were derived under the old vocabulary.

**Blast radius if adopted:** `knowledge/guidelines/_rules-index.json` · the rules-index builder ·
`knowledge/_instrument-fit.json` / `_INSTRUMENT-FIT.md` · every published "N blocking rules" count,
including the ones in ds-016's own entry.

---

## ds-038 — Legacy dark RAG values in the theme overrides drifted from the token store; RULED + CLOSED same session (2026-08-07, #122, s122-D1)

**Found:** Dave's eye against the mark-map controller v4 KG fixtures. `apollo-legacy.overrides.json` minted per-mode
dark values — error `#DB0011`, information `#4587A7` — with `$notes` citing "registry ownsHexes". The token store
(`semantic-color/dark.tokens.json`, the spine) holds NO dark variance: `rag/error #A8000B`, `rag/information #305A85`,
identical to light. The KG standard ({#col25-017}) names one value per role, no per-mode fork.

**Ruled (s122-D1, Dave verbatim):** *"there are no dark mode changes they stay the same in both modes, keep them the
same as light mode. the white progress bar is fine."*

**Enacted #122:** 5 override paths flattened (error / error-glyph / error-background → #A8000B; information /
information-glyph → #305A85), old values retired into the `$notes`; `gen_theme_cascade.py` regenerated (159 paths,
204 projections); legacy-leak 0 · property-resolves 0-of-87 · theme-provenance 37 pre-existing at HEAD (attributed).

**Declared scope residual:** per-mode TINT pairs (`*-tint`) were NOT put to Dave and remain as-built; the ds-001/ds-002
receipts that motivated the old dark values stand as history, not authority.

---

## ds-039 — `canon.css` was HALF DEAD since #99: a documentation comment injected HTML into it and the CSS parser dropped 2,067 rules (2026-08-07, session #122, measured — agent's finding, NOT a ruling)

**Status:** FOUND + FIXED #122. The defect is closed at its cause; the entry is the record, and the
generalisable half is the last paragraph.

**What was wrong.** `gen_canon_components.py` harvests `<style>` blocks out of the reference snippets.
Its harvest regex was lazy and comment-blind, so a `<style>` **merely MENTIONED inside a documentation
comment** in `Chart-butterfly-h.reference.html` was harvested as if it were real CSS. What landed in
`knowledge/canon/canon.css` at ~line 4580 was therefore **markup** — a `<link>` tag plus a comment tail —
and a CSS parser, on hitting `<`, discards everything after it.

**Measured:** `tinycss2` parsed **1,252 rules** before the fix and **3,319** after ⇒ **2,067 rules were
dead**, including **all four theme blocks**. Post-fix parse: **0 errors.** The file had been in this state
since **#99 (`ba02920`)** — twenty-three sessions.

**How it was found, and this is the part worth keeping.** Not by a gate. Dave's eye: *"legacy hasn't
picked up the colours."* The mark-map controller's v4 KG fixtures then made the mismatch **attributable**
rather than merely visible, and a `tinycss2` parse — the first time anything in this repo had parsed
`canon.css` **as CSS** — located it. **19+ green gates stood over this file and not one of them parses
it**; they measured its CONTENT, never its PARSEABILITY.

**Fixed:** HTML comments are stripped BEFORE harvest, and `gen_one()` carries a **HARVEST-NOT-CSS refusal
clause** that fails loud and named rather than injecting markup. Mutation-tested: a literal `<` planted in
a harvested style BITES.

**★ The class.** A green that cannot fail is an assertion — and a gate suite that never applies the
target format's own parser to the target file is exactly that shape. The owed visual confirm caught what
the numeric gates could not [[mutation-tests-the-clause-not-the-feature]].

**Evidence:** `knowledge/canon/gen_canon_components.py` (comment-strip + refusal clause, lines ~143–151) ·
`knowledge/canon/canon.css` (regenerated, parses clean) · `_DECISION-HISTORY/2026-08-07-mark-map-pass-and-the-half-dead-canon.md`.

---

## ds-0NN (QUEUED PROPOSAL, #174) — progress fill-on-track misses 3:1 in Legacy dark and Supercharge dark

**Status:** OBSERVED + MEASURED at #174, **NOT FIXED**. This is a token-level condition and promotion is
Dave's — nothing was changed. Raised while building `Progress-bar` (the first component through the
scaffold route, `s173-D1`).

**What was measured.** `progress/complete` on `progress/incomplete` — the pair that tells a reader how far
along a bar is — across all four themes, light and dark, against the generated `canon/canon.css`:

| theme | light | dark |
|---|---|---|
| Mono | 15.27:1 ✅ | 9.15:1 ✅ |
| Console | 15.27:1 ✅ | 9.15:1 ✅ |
| Legacy | 4.58:1 ✅ | **1.75:1 ❌** |
| Supercharge | 4.48:1 ✅ | **2.38:1 ❌** |

Threshold is 3:1 (non-text, WCAG 1.4.11). Both failures are the **red fill on the dark grey track**:
Legacy `#DB0011` on `#484848`, Supercharge `#CC4333` on `#413934`.

**Scope — this is PRE-EXISTING, not new.** The same pair sits under the existing `Progress-tracker` bar
and under the improvised bars in `File-upload` and `Stepper`. `Progress-bar` did not introduce it; it is
the first component to have measured it across four themes.

**How it is carried meanwhile (not a fix, a mitigation).** `Progress-bar` never declares this pair as a
gated `contrastPair`, and every specimen renders a **numeric value in text** (17.4:1) plus
`aria-valuetext`, so completion never rests on the fill/track boundary alone (1.4.1).

**★ Why no gate caught it.** `_validate_snippets.py` `resolve()` reads `tokens/semantic-colour.json` — the
**Mono base only**. It cannot see the Legacy or Supercharge leg of any declared pair. Declaring this pair
would therefore have produced a **green that cannot fail in the two themes where it is false**. The
four-theme figures above had to be computed outside the gate, by hand.

**Options for Dave (none taken):** (a) lighten the Legacy/Supercharge dark track; (b) darken/lighten the
dark fills; (c) accept it and rely on the numeric carrier under `s151-D1`'s meaning-carrier vocabulary,
which is what the component does today. **Dave rules.**

**Evidence:** `knowledge/components/progress-bar.meta.json` (`tokenValidation.$finding`) ·
`reviews/REVIEW-174-progress-bar-four-themes-v1.html` (all eight panes, live) ·
`knowledge/snippets/Progress-bar.reference.html` (`knownFindings`).

## ds-0NN (QUEUED BUILD CANDIDATE, #184) — a dangling dataviz `var()` renders SILENT BLACK and zero of thirteen gates catch it

*(2026-08-16, session #184, MEASURED by an Opus build sub during the `s184-D3` mutation drive — **an agent's finding, NOT a ruling**. Registered here per derivation governance: a DS error goes to this ledger, and a build candidate is priced here rather than smuggled into a banner.)*

**The observation, driven not reasoned.** A `rect` carrying `fill="var(--status-breach)"` **with no declaration
of `--status-breach` anywhere** — the exact shape left behind by a half-finished rename — paints **black** and
is reported as a pass by **every gate we own**. The mutation was introduced deliberately, the full local gate
chain was run, and **thirteen of thirteen came back clean**. Black is a plausible-looking chart colour, so the
defect has **no visible signature to a reader who was not looking for it**.

**Root cause, named:** `_validate_property_resolves` does not parse a snippet's `fill=` presentation attributes
against **that snippet's own theme blocks**. It resolves declared custom properties; it never asks whether a
property a snippet USES is one the snippet DECLARES. The two halves of the question live in the same file and
nothing joins them.

**Why it matters more than one rename.** `s184-D3` renamed `breach/watch/healthy/info` →
`negative/monitor/positive/neutral` across `canon.css`, `Chart-bar.reference.html` and
`sutherland-fixtures.json` — equal +/− on every file, render-proven byte-identical. **That rename was safe
because a human counted the sites, not because a gate could have caught a miss.** The next rename, in a hurry,
has no such guarantee. Same class as ds-039: **no gate parses the artefact in the consumer's grammar**
[[no-gate-parses-the-artefact]].

**The candidate, priced honestly:** a **chart var-resolution gate** — parse every `fill="var(--X)"` /
`stroke="var(--X)"` in each dataviz snippet, resolve `--X` against that snippet's own declarations plus canon,
and FAIL LOUD on an unresolvable name. Estimate **PICKED, not derived** — this is a planning estimate and is
labelled as one [[planning-estimate-is-not-a-measurement]]. ⛔ **Not built, not scheduled, and it needs no
ruling** — it is a gate candidate, not a value. Whether it is worth the money is the next session's call.

**✅ BUILT #190 (2026-08-16, Opus build sub) — appended, nothing above rewritten.**
`knowledge/_gate_dataviz_vars.py`. It parses colour-bearing SVG **presentation attributes**
(`fill` · `stroke` · `stop-color` · `flood-color` · `lighting-color` · `color`) — the surface C2
structurally cannot see, because C2 reads `<style>`/`style=""` — and resolves each `var(--x)` per
theme (mono · legacy · console · supercharge), following alias chains, against the file's own CSS,
its `<link>`ed stylesheets and `canon/canon.css` (base block + that theme's `[data-apollo-theme]`
block). Unresolvable-in-every-theme ⇒ exit 1, quoted `file:line` + the literal attribute.
Glob, stated so widening is a visible edit: `knowledge/snippets/*.reference.html` ·
`knowledge/snippets/DataViz-interactive.html` · `knowledge/_proforma/*.html`.
**Real-surface measurement, 2026-08-16:** 15 files carry colour presentation attributes,
**688 references, 0 dead, 0 partial-theme** — the #184 instance class has no survivors in the glob
today. Selftest = 8 arms (green control on the real Chart-bar · plant-undeclared · declared control ·
broken alias chain · console-only partial · `var(--x, fallback)` safe · empty population errors ·
missing `canon.css` errors), all PASS. Wired **ADVISORY** in `_build_all.py` (steps 93–94, route
rows added, 119/119 label join verified). ⬛ **PICKED, NOT RULED — Dave's:** (a) making it BLOCKING,
(b) the partial-theme tier warning rather than biting, (c) the attribute list.

**⚠ Related, and deliberately left open:** `knowledge/_DS-IMPROVEMENTS.md:249` still names the OLD vocabulary
in prose. It is a **period reference describing the #122 defect as it was found**, not a consumer, and
rewriting it would falsify a dated record. Dave was shown it at #184 and **did not rule**; it stands.

## ds-0NN (PARKED CANDIDATE, #192, 2026-08-17) — builder-decision data is CARRIED but PROSE-SHAPED: a chart's analytical intent (and its kin) cannot be looked up, only inferred

**Status:** PARKED by Dave, 2026-08-17 (#192): *"park this as a priced candidate … leave receipts
for another lane to reconcile."* No meta change, no gate, no generator change made.

**Finding (measured, #192).** Surveyed all **77** `knowledge/components/*.meta.json`. The decision
data a builder needs largely EXISTS — `purpose` (77/77), `antiPatterns` (77/77), `relationships`
with `livesInside`/`mustNotNeighbour`/`commonPatterns` (77/77) and `triggeredBy` (26), `variants[].use`
(66) — but it is prose-shaped. Concrete instance (Dave's example): no field says a butterfly chart
answers COMPARISON while a candlestick answers CHANGE-OVER-TIME; the fact is in `purpose` prose across
the 7 Chart metas, so "which chart for this dataset?" is inference, not lookup. You cannot ask
machinery *"list every chart whose job is comparison"*. Same shape recurs beyond intent: sibling
redirects ("use Alert instead") live inside `antiPatterns` strings, not as a structured pointer;
charts carry no data-shape field (series count / relationship arity).

**Research receipts (#192, web, 2026-08-17):**
- The intent vocabulary is SETTLED in the field — comparison · change-over-time · distribution ·
  relationship · composition. Adopt, never invent. FT Visual Vocabulary is the practitioner canon
  (9-category superset): https://data.europa.eu/apps/data-visualisation-guide/choosing-charts-the-message
  · academic convergence: https://pmc.ncbi.nlm.nih.gov/articles/PMC7861272/
- Machine consumption of such fields exists but only in full recommender engines — Draco (UW,
  constraints + learned weights, https://idl.uw.edu/draco, paper
  https://idl.cs.washington.edu/files/2019-Draco-InfoVis.pdf) and TaskVis
  (https://shenleixian.github.io/pdf/TaskVis_EuroVis.pdf). Different weight class; not our shape.
- Practitioner design systems (IBM Carbon https://carbondesignsystem.com/data-visualization/chart-types/,
  FT) ship this as human guidance pages, NOT metadata fields. A structured field would be ahead of
  the field — engineered, but with no borrowed convention beyond the vocabulary itself.

**The candidate, priced (planning estimates, PICKED not derived [[planning-estimate-is-not-a-measurement]]):**
1. **`intent` + `notFor`** on the 7 Chart metas, fixed 5-word vocabulary above — ~10 lines/file,
   S-band. Converts chart choice from inference to lookup.
2. **Structured sibling redirect** — e.g. `insteadUse: {"error toast": "Alert"}` alongside the
   antiPatterns prose — vocabulary = existing component names, checkable against the meta set. M-band
   across 77 files IF widened beyond charts; charts+status family alone is S-band.
3. **NO gate, NO generator change** until a consumer exists — [[instrument-without-a-consumer]] +
   ADR-0013 ruling 3 (accrete from observed duplication, never speculation). Natural first consumer:
   a builder brief or the review layer; if an agent ever picks charts, the vocabulary check is built
   WITH that agent, not before.

**Blast radius if adopted:** 7 Chart metas (candidate 1) / up to 77 metas (candidate 2); zero token,
zero snippet, zero canon change. Gates unaffected until a consumer lands.

**Pitfall, replayed:** a field nobody reads is dormant-claim debt ([[conclusions-are-debt-s129-d5]]).
Mitigation: the 5-word vocabulary is stable (decades old in the field), so it ages slowly — unlike
binds addresses. The reconciling lane should decide consumer-first vs field-first, then move.

**Reconciliation owed by another lane (Dave's instruction):** pick candidate scope (1 only / 1+2),
name the first consumer, then land field + consumer together or re-park with a dated reason.

**ARCHITECTURE RECOMMENDATION (recorded #192 at Dave's instruction — FLOATED, not ruled):**
the intent vocabulary must live as a KG ENTITY with metas carrying ADDRESSES into it — never
inline strings, never data inside the generator. The pattern to copy is the alias hop
(`_STANDARDS.md` §1: component var → type-group → semantic role → value; one entity, many
references). Concretely: the 5 intents live ONCE (section in `component-types.json` or a small
`intent` store beside it, each carrying definition + notFor + FT provenance); `Chart-*.meta.json`
carries `intent: "comparison"` as an address; `insteadUse` values are addresses to component metas.
The generator gains only RESOLUTION — unknown intent refuses, dangling `insteadUse` refuses.
**Binding rule: entity and first resolver land TOGETHER, or the addresses are prose with extra
syntax** — an unresolved address is the #145 binds gap (looks checked, is not), which is worse
than a copy.

**GENERALISATION (recorded #192 at Dave's instruction — FLOATED, candidate-ADR shaped, Dave's to
promote): the WRITE-ONCE principle — live facts get ONE home and addresses; history gets copies,
dated and frozen.** The system's worst recurring defects are violations of it and its best fixes
are already applications of it. Receipts, by instance:

*Violations (the defect classes):*
- #41 — read-chain instruction lived inside the 433-line file it governed; five sessions paid full
  price while calling the chain CUT (→ `knowledge/_gen_chain.py`, WHY block).
- #145 (this file's alert case) — meta `binds` addresses that nothing resolves; four gates mention
  binds, none reads `semantic-colour.json` (`components/alert.meta.json`, status-prop `$status`).
- #167 — `_state.json` home pointers rot as GOOD-MORNING rolls (home-pointer-rot class).
- #185 — B3 figures quoted into prose went WRONG-TEXT; copies of live numbers staled silently.
- ds-037 — the rules index cannot tell an ENFORCED rule from a CANDIDATE (entity-registry gap).

*Applications (the fixes that already enact it):*
- `knowledge/_gen_chain.py` — chain GENERATED from one source (GM header + ★ LATEST banner).
- `knowledge/_gen_lanes.py` — one implementation; `_capture_gate.py::lane_routing_check` IMPORTS
  it, "never a second copy" (mover≠gate lesson, #20).
- canon.css regenerated from snippets (`canon/gen_canon_components.py`) — snippets are the single
  source of truth; review decisions cannot diverge (#s pre-33 loss class, closed).
- s177-D1 — "no evidence pointers into rolling files": an address is only safe pointing at a
  non-moving home.
- #182 NEW-HOOK CONVENTION — mechanical claims carry their probeable token: the address travels,
  not the copy.
- s188-D1 — the grader reads the hook FILE, not a restatement.
- token spine + alias hop itself — Apollo's colour/type system is already write-once end to end.

*Candidate next instances (unpriced, for the reconciling lane or a future ADR):*
- meta `$status`/`$note` fields quoting ruling prose at length → address into `_rulings.json`
  + local one-liner.
- MEMORY.md hooks restating memory-file content → hook-as-address (s188-D1 direction).

*Hard limits (both already ruled in this repo):* (1) address-without-resolver is the binds gap —
worse than a copy; (2) dated PERIOD RECORDS are exempt — rewriting them falsifies history (#184
ruling on this file's line 249; header-wins-over-audit). Write-once governs LIVE facts only.

---

## ds-0NN (FLOATED CANDIDATE, #194, 2026-08-17) — audit verdicts are BOOLEAN; a graded defect rating with an automated report is the shape Dave floated

**Status:** FLOATED by Dave, 2026-08-17 (#194). **NOT ruled — promotion is Dave's alone.** Nothing
built beyond the narrow WARN tier s194-D1 *did* rule (see below); this entry is the record of the
larger idea, not a licence to build it.

**Dave's words (#194, verbatim):** *"a future development may be a graded rating of defects rather
than a boolean one, with an automated report, Apollo must serve new design systems as well as the
ones we are creating, so its a system development tool and the decisions can be passed to the
designer."*

**Finding (the gap the words name).** Every contrast/a11y gate in `knowledge/` speaks a two-value
verdict: it passes, or it fails the build. The only escape hatches are per-instance and hand-listed
— `CONTRAST_ALLOWLIST` (disabled states), `LEGACY_THEME_EXEMPTIONS` (R-D24), `RULED_PAIR_EXCLUSIONS`
(pairings a ruling forbids). Each is binary again: fully counted, or fully removed. A real a11y
review does not work that way — it grades (blocker / major / minor / advisory) and hands the
judgement to the designer. Dave's #194 case was exactly this: mono white-on-error is a genuine
measurement (3.14:1) about a state a ruling abolished — not a build-stopper, not a non-event.

**What was ALREADY ruled and built at #194 (the floor this candidate sits on, do not re-open):**
s194-D1 gave `_build_surface_contrast_audit.py` a THREE-word severity vocabulary — `pass` / `minor`
/ `gating` — with `minor` reachable ONLY through the named, theme-scoped pairs in
`_contrast_utils.MINOR_PAIRS`. One row is minor today. That is a ruled carve-out, deliberately
conservative; it is NOT the graded system described here.

**The candidate (unpriced, deliberately — pricing it invites building it):**
1. A shared severity vocabulary across the audit family (surface, indicator, icon-delta, compose),
   not one reader — today each gate owns its own verdict words.
2. Grading rules that are DERIVED rather than hand-listed: distance below threshold, whether the
   pairing is reachable in a live component, whether a ruling covers it.
3. An automated report addressed to a DESIGNER, not to CI: the decisions surfaced for a human to
   take, which is the "passed to the designer" half of Dave's sentence and the half no current
   artefact does.
4. The portability requirement Dave named: this must work for a design system Apollo did not
   author, so grading may not depend on Apollo's own token names or ruling IDs.

**Blast radius if adopted:** every contrast gate's exit-code semantics, `_TEXT-CONTRAST-AUDIT.json`
consumers, the dashboard's red counts, and the review layer. Large — which is why it is floated.

**Pitfalls, replayed (Dave #165):**
- **A grading system is a way to stop failing.** Every downgrade path is a route by which a real
  defect becomes a warning nobody reads. Any promotion must ship with the mutation proof that a
  genuine failure still turns the build RED (the s194-D1 arms A7b/A7c are the pattern).
- **A vocabulary with no consumer is dormant-claim debt** ([[instrument-without-a-consumer]],
  [[conclusions-are-debt-s129-d5]]). Grades that no report and no reader acts on are decoration.
- **Derived grades are a generator.** [[do-not-rule-list-cannot-fence-a-generator]] — if grading
  rules are derived, they will re-grade rows nobody asked about; the regions it owns must be named
  BEFORE it runs.
- **Portability is the hard half.** A rule keyed to `rag/*` or to `s1NN-D1` ids does not travel to
  a foreign design system; the abstraction has to be over MEASUREMENTS, not over Apollo's names.

**Reconciliation owed:** Dave's alone. Promote, re-scope, or park with a dated reason — nothing
here may be enacted on the engine's own judgement (Governance, this file).

## ds-0NN (QUEUED BUILD CANDIDATE, #201, 2026-08-18) — `size/segmented-control/min-hit-area` (44) has no consumer gate; a 36px target ships clean

The token is minted (`s200-D4`) and its semantics are ruled (`s201-D2` hit zone; `s201-D3` hit box
= max(44, visual height) — natural above the floor). But no gate reads it: a segmented control
rendered at 36px with no expanded interactive target passes every existing validator
([[instrument-without-a-consumer]] — declared as pitfall (c) at #200, still true after #201).

**Shape of the gate:** parse rendered specimens/snippets in the consumer's grammar
([[no-gate-parses-the-artefact]]) — assert that any element carrying the segmented-control role
with visual height < 44 presents an interactive box (::after or padded target) ≥ 44px computed.
The `SEGMENTED-SCALE-SPECIMEN-2026-08-18-v1.html` ::after geometry (verified 8/8 at #201) is the
reference implementation. Must ship with a mutation proof: remove the ::after and the gate goes RED
(the s194-D1 arms pattern, this file's Governance note).

**Priced, not built** — queued at #201 for a component-work window. Enactment call is Dave's.
