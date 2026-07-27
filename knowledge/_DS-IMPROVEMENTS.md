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
LOOSER than Helvetica, so a gutter sized against a fallback face fits and the same gutter against the
licensed face does not. It is invisible in any render that falls back — which is precisely why the
runbook asserts `document.fonts.check('16px HSBC_MtUnivers_Latin')` before shooting.

**NOT fixed in lane ①, deliberately.** Widening the gutter re-bakes every `x`/`width` on the h-bar
figure — a geometry change to a reviewed artefact, not a legend migration. Two candidate shapes, for
Dave: (a) widen the gutter to a fixed value that fits the longest label at the real cut (~60px), or
(b) make the plot area gutter-relative so long categories can't clip at any width. **Recommend folding
into the same beat as ds-010's sibling checks, with a render as the acceptance test — and adding a
"no `text.dv-label` has `getBBox().x < 0`" assertion to the dataviz gate so geometry clipping becomes
gated rather than eyeballed.** *(The gate would have to run in a browser — today it cannot; log as the
reason the assertion is a recommendation and not a patch.)*

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
