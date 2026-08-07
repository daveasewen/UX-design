# Component interaction review — sign-off tracker

Durable record of the component-by-component interaction review (gallery frontier).
**Once a component is ✅ signed off, it is locked — we do not reopen it.**

---

## ⬛ PENDING — FULL CONSOLIDATED REVIEW (Apollo Mono baseline) — added 2026-07-19
Dave will run **one big review page** over the whole Mono baseline **when the build-out is "done"** — *"I just
need to get this nailed"* (2026-07-19). **Do NOT drip-review the tranches piecemeal — accumulate everything into
that single pass.** Running list of what it must cover:
- **Tranches T1–T9 as they render NOW (post-tokenisation).** The per-component sign-offs below are dated
  2026-06-29/30 and **predate the Mono ramp + R-D16 + the tokenise sweep** — they do not cover current values.
- **Tokenise deltas to eyeball (2026-07-19):** dark divider lightened + more prominent (`--line2` `#3A3A3A → #808080`);
  focus ring now **blue** (`focus/ring` #305A85/#4587A7), was mono near-black; primary button dark slightly brighter
  near-white (`#F2F2F2 → #FFFFFF`).
- **Open decisions to close in-review:** mono **primary-action** token (mint `action/primary/*` + `icon/on-inverse`,
  or adopt `text/on-inverse`); **success/verified kept MONO** (ink check) vs teal; **blue-vs-mono focus ring**.
- **Also owed:** DataViz sign-off (parked "good enough"); **Tranche-9 first review**; Masthead/Hero/Headers revisits
  already flagged below.
- **★ NEW 2026-07-27 (#7) — TWO FELT CONSEQUENCES OF DV-D17, NEITHER RULED, BOTH NEED DAVE'S EYE LIVE.**
  Surfaces: `showroom/chart-donut.html`, `chart-bar.html`, `chart-combo.html`, `chart-line.html`.
  **(a) An enactment call that is the agent's, not Dave's.** Release-on-add also sets `st.visible[id] = true`,
  so the series you clicked is showing afterwards. The strictly literal reading of DV-D17 bite (i) restores
  `visible[]` **alone** — both avoid the all-on failure, and they diverge only when a series dimmed *before*
  isolating is then the one clicked: literal leaves it dimmed, so the click that ended the mode does nothing
  visible to the thing clicked. **One line either way.**
  **(b) A DV-D13 consequence the ruling never named.** Isolate Housing (`950 / 41%`), then check a second
  series: that click now **releases**, so the donut's centre returns to `2320 / 100%` instead of growing to
  `1250 / 54%`. DV-D13 is intact — the centre still follows the SELECTION; the selection is simply everything
  again. **Judge it live, not from this description.**
  ⚠ **Both are DOM-proven only** (`_verify_dv_legend*.js`, 108/108 + 27/27) — **the render in the licensed cut
  is OWED** and is `GOOD-MORNING` §DO-FIRST item 0(a) for the next window.
- **★ NEW 2026-07-27 — THE WHOLE SHOWROOM CHANGED TYPE, and nobody has looked at it yet (ds-013).** Dave
  reported the chart legend labels rendering too big; the cause was `srcdoc` re-basing every payload's
  relative URL, so **`canon/type.css` 404'd in all 49 panes that link it** and every `.t-cm-*` composite
  and selector binding in it was inert. Fixed + gated in `gen_showroom.py` (build 56/56). ⚠ **Consequence
  to eyeball: 49 showroom panes are now rendering CANON type for the first time.** Measured on the charts
  (labels 16px/400 → 12px/500, keys → 12px/700); everywhere else the delta is unmeasured. Anything that
  looked acceptable at browser defaults may have moved. **This wants a deliberate sweep — it is the
  cheapest moment to catch type regressions across the library, and it is not a chart question.**
- **★ NEW 2026-07-27 (later morning #2) — Chart-bar `cb5` STACKED COLUMN re-geometried + alpha keys
  re-coloured; Dave has not seen it rendered.** Pane: `showroom/chart-bar.html` (also
  `knowledge/snippets/Chart-bar.reference.html` standalone). Both changes are DV-D14/DV-D15 enactments
  and both are **measured green** (`knowledge/_verify_dv_stacked_enactment.py`: 2.00px separation on all
  8 boundaries; keys white at 5.26 / 5.04 / **4.61:1**), but the *look* is his call:
  **(i)** segments now understate by **2.0–2.6%** to buy the gap — accepted at ruling time, never seen;
  **(ii)** the keys flipped ink → white, which changes the chart's whole texture at a glance;
  **(iii)** ⚠ **series-3's 4.61:1 leaves 0.11 of margin over AA** — flagged because it constrains any
  future re-tune of that hue, and he should know the ceiling is that close before he approves the look.
- **Video-player re-themed — ★ FAST FOLLOWER, do NOT hold for the consolidated pass (Dave 2026-07-21
  end-of-session: "fine-ish for now, lets make it a fast follower"):** primary action
  now the B-D1 ladder ink (red = Legacy-only via override); `--muted` bound to `text/secondary` — a **deliberate
  darkening** #767676/#9a9a9a → #1A1A1A/#FFFFFF (Dave: *"resolve to the near black... we can review later"*);
  focus ring → `focus/ring` (was rogue #4d9fff); scrim/controls tokenised (`overlay/version2` / `text/reverse`).
  **Eyeball in-review:** the darkened caption/timestamp weight; **the bigplay ON-SCRIM treatment — ENACTED
  same evening** (Dave: "yes but let me eyeball") — light-mode ink fill measured **1.2:1** vs the video (fail;
  the old red was itself 2.7:1) → play button now joins the on-video control family: reverse fill BOTH modes
  (14–19:1) + #333333 glyph (12.6:1, driftAllow'd), themed accent stays on the scrub. **Applies in ALL themes —
  Legacy's play button is white now too (its scrub stays red) — confirm at eyeball.** Also review the scrub
  played-bar contrast against its track (pre-existing, all themes). Worker-B receipt 2026-07-21 has probe values.
- **✅ Legend isolate/toggle v5.x — SIGNED OFF (Dave 2026-07-26, "good done, love this" on v5.5) — LOCKED.**
  `reviews/LEGEND-ISOLATE-TOGGLE-PROTOTYPE-2026-07-24-v5.5.html` = the reference implementation; v5.1–v5.4
  retained as the decision arc. **INSCRIBED same session: DV-D11** (legend model: dual gesture · two fade
  levels full/ghost-12% · additive isolate · hover live in both modes + 24% peek) · **DV-D12** (trapezoidal
  sweep easing keyed to segment spans) · **DV-D13** (typed tooltip + centre figure follows selection) in
  `_DATAVIZ-DECISIONS.md`; seed fed (81 nodes / 138 edges); build 55/55 GREEN. Enactment = the
  donut+bar+combo wave bakes DV-D11/12/13 into `dv-behaviour.js`. Residual asks riding the wave: the
  aria-both-forms asymmetry (DV-D13 ⚠) + the seed-uncheck edge (DV-D11 open edge).
- **Radius/corner tuner v1+v2 (added 2026-07-26, P4):** `reviews/RADIUS-CORNER-TUNER-2026-07-24-v1/-v2.html` — the ★★ "return SOON" item; owed = tweaks + numbers, then per-theme ruling. *(Served to Dave again #66 — no verdict yet.)*
- **Molecules pack — RULED #66, ENACTS PENDING (added 2026-08-01 #66):** `reviews/MOLECULES-KEYFILTER-LOCKUP-2026-08-01-v2.html` — D1 A2 permanent-strict · D2 sparkline sheds · D3 scatter connects · D4 dv-lockup shape approved (ledger § ★ #66-D6). Not awaiting signoff — awaiting the #67 enact wave; stays here until the four enacts land so the ruled-but-unenacted state has a durable home. ⚠ Doc predates the two-register + export-pair runbook laws it triggered; regenerate per `_RUNBOOK-review-doc.md` only if re-presented.
- **Data-marks-exempt hit-area rule + a11y gate rebuild (added 2026-07-26, P4):** `notes/_briefs/2026-07-25-hit-area-rule-and-gate-proposal.md` — sign-off inscribes the rule + green-lights the markup-driven gate rebuild (44 blocking for controls, marks exempt).
- **⬛ Donut legend ENACTED — awaiting Dave's eye (added 2026-07-26, legend-wave session):**
  `showroom/chart-donut.html` (and `knowledge/snippets/Chart-donut.reference.html`) — the first member
  running the real DV-D11/12/13 model out of `canon/dv-legend.js`. Verified numerically **27/27**
  (`knowledge/_verify_dv_legend.js`, real source against the real snippet, incl. 950/41% and 1250/54%);
  ✅ **Render-verify CLEARED 2026-07-26 (lane ①)** — the standing owed note is discharged: Playwright was
  staged per `_RUNBOOK-render-verify.md` and the donut shot at 1180px + 760px in the licensed HSBC cut
  (font assert passed). Both figures, the legend rows, the Reset and the centre figure all read correctly.
  ⚠ **Two deltas from the signed-off v5.5 need your eye, both forced by gates:** row padding 5px/9px →
  **4px/8px** (DEF-005 4px grid) and `border-radius:2px` → `var(--border-radius-default)` (radius gate).
  Resurrect-verbatim is not gate-exempt — same door the 273d18c~1 stepper came through.
- **⬛ Chart-bar legend ENACTED + ds-010 CLOSED — awaiting Dave's eye (added 2026-07-26, legend-wave lane ①):**
  `showroom/chart-bar.html` — wave member 2, and the first member carrying **TWO legends on one page**
  (cb4 grouped · cb5 stacked). Verified **54/54** (`knowledge/_verify_dv_legend_members.js` — DV-D11
  conformance per legend, plus 8 new cross-talk checks proving one legend cannot move the other's marks
  or write to its live region) and **render-verified at 1180px + 760px in the licensed HSBC cut**.
  ⚠ **ONE DELIBERATE VISUAL DELTA needs your eye:** the shaped swatches are gone — `.sw-circle` /
  `.sw-square` / `.sw-diamond` are now plain 12px squares, as on the donut. Reasoning: bar's marks are
  rects, so no marker shapes exist for the swatches to encode; bar's real non-colour channel is the
  on-chart LETTER key (A/B/C). A diamond swatch promised a diamond mark that was never there.
  **Chart-line's markers genuinely ARE circle/square/diamond** — it keeps shape modifiers in lane ③,
  so the two members will differ on purpose. Say the word and I'll put bar's shapes back.
  ✅ Also visible here: **ds-010 closed** — every figure now renders its true colours (h-bar teal per
  DV-D09, the full R-D9 status ramp red/amber/green/blue), where before all four were series-1 purple.
  ⬛ And the same render surfaced **ds-012**: all six h-bar category labels are clipped at the left
  (worst 16.8px) — a 38px gutter sized against a fallback face, not the real cut. Logged, NOT fixed.
- **Five chart showroom panes (added 2026-07-26, P4):** `showroom/chart-{bar,line,donut,combo,sparkline}.html` — the DataViz sign-off = Dave eyeballs the 5 panes → canon flips provisional-agent→canon (open-014). Same object as the "DataViz sign-off" line above — pane paths pinned here so the eyeball has its list.
- **Eight wave-2 chart panes (added 2026-08-05, #95):** `showroom/chart-{butterfly-h,butterfly-v,histogram,boxplot,bullet,candlestick,pie,stacked-area}.html` — ✅ render-verified #96 all 8 PROVEN (receipt `notes/_receipts/2026-08-05-96-render-verify-wave2.md`; stacked-area's missing `dv-fit-on` overrides fixed #96 then re-verified) — Dave's eyeball still OWED; metas carry the #96 resolution note. Per-lane flags for Dave are listed in `_proforma/_DATAVIZ-DECISIONS.md` § ★ #95 (bullet proportions + grey tints · candlestick dv-011 · histogram static key · stacked-area alpha dial + fit gap · pie sweep data-ri).

Method + template controls (live variant/state spread from meta · light/dark toggle · responsive slider · comment
overlay) per the **Method** section. Pointer in `_LIVE-STATE.md` PLANNED/TARGET; memory `full-review-pending`.

## Method (per component)
1. Review the **HTML snippet** (`snippets/<Name>.reference.html`) live in a browser — check interactivity, responsiveness, visuals. (Source of truth; fully interactive; theme toggle + `@media` + reduced-motion built in.)
2. Dave points at issues → fix the **snippet** (never canon.css directly).
3. Regenerate: `python3 knowledge/canon/gen_canon_components.py` → render → `python3 knowledge/_validate_screen.py --render`.
4. Re-gate the gallery + journey. Green + Dave's eyes → **sign off**.

Issue types we're hunting: **missing interaction decisions** (motion / hover / pressed / focus / open-close), **incomplete / missing** (states, variants, dropped sub-parts), **finesse** (spacing, hierarchy, proportion, colour nuance).

**Review specimens show the component ALIVE + its full variant/state spread (Dave, 2026-07-19).** A review doc that features a component must present it as a *live, working* example and show *every variant and state it carries* — never one frozen instance. The spread is not invented: **read it from the component's meta** (`components/<name>.meta.json` — `props` / `variants` / sizes / documented states), then add theme (light+dark) and motion states (normal / active / reduced-motion). A pick (type size, colour, spacing) can only be judged across the component's real range. A variant that plainly exists but is absent from the meta is itself a finding. Then obey the standard review-doc rule: build clean in `reviews/`, inject the overlay with `_make_review.py`, present the `.REVIEW.html`.

**Template controls — every review carries a light/dark toggle + a responsive-width slider (Dave, 2026-07-19).** The spread shows the variants; the controls let Dave stress the component across theme and viewport. Durable target: bake both into `_review/_review-overlay.html` so every generated review inherits them (tracked in `_FUTURE-STATE`); until then add them to each doc's chrome by hand.

Legend: ⬜ pending · 🔧 in fix · ✅ signed off (locked)

---

## Tranche 1 — Buttons & actions (interactive triggers)
| Component | Status | Signed | Notes |
|---|---|---|---|
| Button | ✅ | 2026-06-29 | Good — promoted (incl. leading-trim) |
| Links | ✅ | 2026-06-29 | Signed off — active = label hover/pressed (underline). Filled-active icon DEFERRED (glyph missing) → _ICON-GAPS.md |
| Tags | ✅ | 2026-06-29 | Good — promoted |
| Quick-actions | ✅ | 2026-06-29 | Good — promoted (Button scale-physics motion added) |
| Badge | ✅ | 2026-06-29 | Good — promoted |
| Status-indicator | ✅ | 2026-06-29 | Good — promoted |

## Tranche 2 — Inputs & selection
| Component | Status | Signed | Notes |
|---|---|---|---|
| Input-fields | ✅ | 2026-06-29 | Good — promoted |
| Search-field | ✅ | 2026-06-29 | Promoted — Boxed + Underline; clear only when value present; native cross suppressed; icon centred |
| Selection-controls | ✅ | 2026-06-29 | Good — promoted |
| Slider | ✅ | 2026-06-29 | Good — promoted |
| View-options | ✅ | 2026-06-29 | Promoted — sliding active indicator; single container border |
| Dropdown | ✅ | 2026-06-29 | Promoted — Underline + Boxed (full-border) variants |

## Tranche 3 — Containers & data display
| Component | Status | Signed | Notes |
|---|---|---|---|
| Cards | ✅ | 2026-06-29 | Promoted — undecorated ghost actions at standard button size (h44/pad20) |
| Account-card | ⏸ defer | | DEFERRED (Dave) — needs more work, not a priority; revisit later |
| Table | ✅ | 2026-06-29 | Promoted — card-collapse left-aligns all data (label + value) |
| List-items | ✅ | 2026-06-29 | Promoted — two-line aligned row (title↔status, desc↔amount); density scales both sides; descenders safe |
| Divider | ✅ | 2026-06-29 | Promoted |
| Accordion | ✅ | 2026-06-29 | Good — promoted |

## Tranche 4 — Navigation & wayfinding
| Component | Status | Signed | Notes |
|---|---|---|---|
| Tabs | ✅ | 2026-06-29 | Good — promoted |
| Navigations | ✅ | 2026-06-29 | Promoted (fine for now; Dave to develop further later) |
| Breadcrumbs | ✅ | 2026-06-29 | Promoted — slash + library-chevron separator versions |
| Pagination | ✅ | 2026-06-29 | Promoted — Button press states (inverting fill + depress) added |
| Headers | ⏸ revisit | 2026-06-29 | Subtitle fixed (regular); DEFERRED — marked for revisit (full header set) |
| Reorder | ✅ | 2026-06-29 | Promoted — pointer drag works (+ keyboard moves). FUTURE: "portfolio-level interactions" pass invited by Dave |

## Tranche 5 — Feedback & overlays
| Component | Status | Signed | Notes |
|---|---|---|---|
| Notifications | ✅ | 2026-06-29 | Promoted — close × first-line aligned (22px) across all; --text-shift 7px optical centre; Global 3 variants (none/close/actions) + flush bottom-right actions; title/desc stack 8px; multi-link stack 10px |
| Modals | ✅ dialog | 2026-06-29 | Promoted AS DIALOG; GAP noted: add true modals + lightboxes (desktop+mobile) from Figma → _COMPONENT-GAPS.md |
| Tooltip | ✅ | 2026-06-29 | Promoted — icon-at-end-of-label canon rule + space-aware positioning |
| Progress-tracker | ✅ | 2026-06-29 | Promoted — reworked to Figma (inline label + continuous red fill) |
| Loading-indicator | ✅ | 2026-06-29 | Promoted (fine for now; Dave to tinker later) |
| Countdown-timer | ✅ | 2026-06-29 | Promoted — butt caps; number centred; animates only final 5s (no pause needed); subtitle regular |

## Tranche 6 — Identity & media
| Component | Status | Signed | Notes |
|---|---|---|---|
| Avatar | ✅ | 2026-06-29 | Good — promoted |
| Hero | ⏸ revisit | 2026-06-29 | Promoted (fine for now); Dave to develop further — marked for revisit |
| Video-player | ✅ | 2026-06-29 | Promoted — square play button + Button scale-physics |

---

## Queued after review — 5 gap-patterns → gated components
Follow the **account-card** template. Components: **summary, tab-bar, action-bar, eyebrow, confirmation/success**.

| Gap-pattern | Status | Signed | Notes |
|---|---|---|---|
| summary | ✅ | 2026-06-30 | Promoted — dl key/value + emphasised total row |
| tab-bar (bottom nav) | ✅ | 2026-06-30 | Promoted — A standard labelled bar + B segmented sliding-pill islands (interactive; View-options easing; full-width; inverting black/white selected; Menu in the exclusive group; Insights added). **ISLANDS marked for REVISIT (Dave)** |
| action-bar | ✅ | 2026-06-30 | Promoted — Back(tertiary,left)+Cancel+Confirm; reflow stacks primary-top/Back-bottom; reuses Button |
| eyebrow | ✅ | 2026-06-30 | Promoted — sentence case (house type rule); leading-trim kicker |
| confirmation/success | ✅ | 2026-06-30 | Promoted (finesse later) — success-solid pop + staggered rise; mobile vertical-centre; desktop variant logged in _COMPONENT-GAPS.md |

---

## Awaiting Dave — running list (dream-pass v2 P4, ruled 2026-07-26)

| Artefact | Raised | State |
|---|---|---|
| `reviews/DS-018-DISABLED-STATE-2026-07-27-v1.REVIEW.html` | 2026-07-27 #11 | **A2·B2·C2 RULED same session.** ⛔ **The RECESSIVE VALUE remains UNRULED** — the doc's four candidates (`#9D9D9D` canon today · `#808080` B-D4 · `#B5B5B5` · `#6B6B6B`) were offered as candidates, **never as a recommendation**, per derivation governance. Light/dark pairing also unruled. **Enactment must put the value to him.** ⚠ Collides with the flagged drift: B-D4 ruled `#808080`, canon ships `#9D9D9D` (`canon.css:351`). |
| `notes/2026-07-31-what-memento-is-onepager-v1.md` | 2026-07-31 #63 | **Approved in draft same session** (Dave: "really encapsulates the idea"). Awaiting his VOICE pass + a release-home decision (where it publishes). |
| `notes/_bite-matrix-gm-move-DRAFT.md` | 2026-07-31 #63 | DRAFT, replay done — **count reconciliation owed** (4 unverdicted rows) before ratification. |
| `notes/_bite-matrix-chain-and-index.md` | 2026-07-31 #63 | DRAFT, conductor-built, mutations quoted — awaiting ratification. |
| `notes/_bite-matrix-capture-gate-PHASE1-DRAFT.md` | 2026-07-31 #63 | DRAFT phase 1 (no mutations by design) — phase 2 = the 30 UNCOVERED rows, queued #64. |
| `notes/_briefs/2026-08-01-dv-lockup-scope-brief.md` | 2026-08-01 #67 | dv-lockup scope. ✅ BUILT #68 (`2a3f6ee`) — per-chart-block + name confirmed at the #68 opener; premise correction inscribed in the brief. |
| `knowledge/snippets/Chart-donut.reference.html` (cd2 title) + `Chart-scatter.reference.html` (both titles) | 2026-08-01 #68 | ✅ **RULED #69 (Dave, in-session):** cd2 → "Housing dominates the month's spend" (edited via `data-lockup-title`, regenerated, sync green) · cs1 "Savings rise with monthly income" + cs2 "Savings rise with income across every segment" RATIFIED as-written (placeholder wording adopted as Dave's copy, no file change). ⚠ Text-only change; pages not re-rendered — geometry untouched. |
| `reviews/2026-08-01-72-D3-scatter-responsive-v1.html` (D3 scatter width-behaviour) | 2026-08-01 #72 | ⬛ **AWAITING DAVE — D3 deliberately UNRULED at #72** (he asked to SEE it again): width scrubber over both surfaces, fixed 1180/600/420 spread, mutation table. Registered at the #74 EXIT CHECK — the row was owed by #72's own wrap and lived only on rolling banners. |
| `knowledge/canon/dv-legend.js` + 5 chart snippets (★ DV-D18 additive isolate) | 2026-08-01 #70 | ⬛ **AWAITING DAVE — review pair NOT built, deferred by his own budget ruling at the #70 wrap** (~140K of a 200K line; a review build landed ~205K — declared and forked, not spent silently). **#71 opens by building it.** DV-D18 is gate-proven (108/108, both mutants red) but **NOT eye-proven**. Also still owed: **D3 lockup rework detail, Dave's — asked at the #70 opener, not given.** |
| ⛔ **Review-overlay export defect — ROOT-CAUSED AND FIXED #70** | 2026-08-01 #70 | ✅ **The radios were NEVER WIRED, in ANY review doc — an absence, not a #66 regression.** `_review-overlay.html`'s `buildPrompt()` built from `comments[]` only; zero radio reads. #66's fix repaired comment-pin export under a sentence claiming to repair *picks* — two problems conflated under one sentence, so #69's recurrence was inevitable. **Fixed:** `scanPicks()` (unruled groups declared "(not ruled)", never omitted) + `isDecisionControl()` exempting choice controls from the review-mode `preventDefault()`. ⚠ **UNPROVEN — Dave has not used it yet; #71's doc is its first real test.** |
| `knowledge/snippets/Chart-scatter.reference.html` (ds-020 axis/grid migration) | 2026-08-01 #69 | ✅ **RULED #69 (Dave, screenshots — review-doc export FAILED him, see defect row below):** D1 axis/grid colours APPROVED · D2 title-left/toggle-right APPROVED · **D3 legend lockup NEEDS REWORK** (keys-left/Reset-right + 520px wrap-centre placeholder rejected as built — no detail given yet, get it at the #70 opener) · **D4 swatch-during-isolate → DISCUSS LIVE next session** (DV-D17 vs Dave's "additive" wording — collision unresolved, DV-D17 stands until ruled) · D5 AGREED: fit hooks + four-theme wiring (incl. Mono/Console switcher in review controls — asked twice #69) = next session line. Review pair: `reviews/CHART-SCATTER-DS020-LOCKUP-2026-08-01-v1(.REVIEW).html`. |
| Review-overlay export path (`_make_review.py` pair) | 2026-08-01 #69 | ⛔ **DEFECT, RECURRED from #66: Dave ruled via screenshots AGAIN — "the radio buttons do nothing", no way to transfer picks.** The overlay was present (probed in-context) but the export was not usable/discoverable at the moment of ruling. The #66 hard lesson said the pair is mandatory; the pair EXISTED and still failed the person. Diagnose at #70: export discoverability (button placement/labelling) vs radios-outside-overlay-scope (doc's own radios may not be captured by the overlay's export). Until fixed, every review doc must state IN THE DOC how picks reach Claude. |
| `reviews/DV-D19-MODE-LATCH-PROTOTYPE-2026-08-02-v1.html` (DV-D19 mode latch, A/B against DV-D18) | 2026-08-02 #76 | ⚠ **BEHAVIOUR SIGNED OFF, ARTEFACT REJECTED.** Dave: *"DV-D19 is correct, but obviously it isn't styled correctly as this is a prototype."* The ruling is CLOSED — enacted in `canon/dv-legend.js`, mutation-proven by check 24 (112/116 under the old predicate, 116/116 restored). ⛔ The SPECIMEN is defective and it is my defect: it invented an `.is-solo` treatment instead of canon's (`canon.css:3508` — ink border + 6% ink tint, 12px swatch, 44px hit). **Repair = rebuild against real `canon.css` + real snippet markup, NOT a restyle of the approximation. OWED #77.** ✅ **REPAIR DELIVERED #78 — superseded by the v2 row below.** |
| `reviews/DV-D19-MODE-LATCH-2026-08-02-v2(.REVIEW).html` (DV-D19 on REAL canon — the #76 repair) | 2026-08-02 #78 | ⬛ **AWAITING DAVE — two pins.** Composed from linked canon.css + verbatim snippet figure + the #76-D1 behaviour trio; zero component-selector overrides (replayed); `.is-solo` = resolved `--ink` + 6% tint EXACT both themes (`canon.css:3508`); release path real-clicked both panes; verifier control 116/116. **Open pins, presented as OPEN in-doc:** (1) swatch-at-rest (narrow reading badged "shipped today", Dave's #75 wording quoted) · (2) ✅ **the fade — CLOSED #78 post-wrap** (Dave: *"the fade levels are good btw"* → ladder read back → *"— is correct"*; PRESERVE not ADD, closure in `_DATAVIZ-DECISIONS.md`). Committed `f73b9ec`; **ONE pin remains: swatch-at-rest.** ✅ **FULLY SIGNED OFF #79 (2026-08-02) — the last pin is CLOSED.** Swatch-at-rest put to Dave at the opener with both doc options verbatim + a fresh source probe of what the wide reading would actually cost (`visible[]` freezes at first click; the Reset guard `dv-legend.js:147` breaks in both halves; 14 legend-bearing surfaces). He ruled **NARROW** in his own words: *"DV-D19 — the mode latch, shown on real canon prototype is perfect as it is."* Read back as sensation before inscribing. **No code change — shipped behaviour ratified.** Closure in `_DATAVIZ-DECISIONS.md` (by addition, nothing trimmed). |
| `notes/2026-08-02-the-tokenizer-unit-five-whys.md` (the `ds-021` three-homes ENACTMENT — a decision brief, not an HTML review) | 2026-08-02 #80 | ⬛ **AWAITING DAVE — FOUR SHAPES, none pre-selected. ⚠ THE UNIT IS NOT ON THE TABLE: he RULED it at #54** (*"ONE unit — real Claude tokens; `cl100k` … never a unit a cap is stated in"*), declaring it NOT ENACTED that window — and it is still unenacted 26 sessions on. ⛔ **Read the note's CORRECTION BLOCK first:** the ratio was #53's measurement (×1.559, `knowledge/_measure_tokenizer.py`), not #80's; #80 re-derived it and nearly filed it as new. #80 re-measured `_CHAIN.md` 5,761 → **9,079** and `GOOD-MORNING.md` 27,171 → **42,435** ⇒ every tape-vs-budget comparison is dimensionally invalid. **New at #80:** the ROOT CAUSE — `measurement_degraded()` is present, wired, pinned and **blind** (the vocabulary has no word for REAL) ⇒ the remaining work is a CODE change, not the "write-up" §C·4 claimed. Shapes: **(A)** make the unit a TYPE (`Tokens(n, unit)`, refuses cross-unit compare) · **(B)** ONE measuring authority (delete two of three paths) · **(C)** a CROSS-INSTRUMENT gate — cheapest, and the only one that catches the NEXT occurrence · **(D)** calibrate and keep `cl100k` — **named for completeness and argued against** (a conversion where a measurement is available; ratio not constant, ×1.79 prose vs ×1.56 here). ⚠ **Deliberately NOT shipped:** whichever lands, the re-measurement touches the GM `size:` stamps, `ds-025`'s floor and the amber line. Ledger: `notes/_MEMENTO-DECISIONS.md` § ★ #80. |
| `showroom/index.html` (side tree nav #97 → ONE-BAR #98) | 2026-08-05 #98 | ⬛ **AWAITING DAVE, narrowed:** #97 flag ① CLOSED (#97-D1/#98 — viewbar + index theme seg REMOVED, one bar per page, bites 6–6e) · sources pure canon (#98-D1, receipt `notes/_receipts/2026-08-05-98-one-bar-chrome.md`). Still his eye: **bullet flex-height · Confirmation Replay disabled** (motion is display-toggle, not `dv-animate` — migrate idiom? canon behaviour change) · #97 flag ② 700px tree→intro gap, cosmetic. ✅ **BOTH RULED #103:** Replay = second detection idiom, snippet untouched (ds-029, enacted + mutation-tested) · bullet flex-height SUPERSEDED by ds-030 (all charts fully horizontally responsive; donut/pie = fluid container + fixed circle, render-proven). Remaining his eye: legend-variant centring (group vs svg-alone) · #97 flag ②. ✅ candlestick hollow/filled RULED #100 (ds-027: solid two-state, table = a11y fallback; spread `reviews/CANDLESTICK-FOURSTATE-2026-08-05-v1.html`) — **enactment owed #101**. ✅ **#97 flag ② CLOSED #104** — `.shell{align-content:start}` at ≤760px, `gen_showroom.py:338` (1 line) + regen; gap `intro.top−tree.bottom` 700px 322.5px→24px, 375px 259px→24px (24px = `.intro`'s own padding), 1180px byte-identical (zero regression); `--check OK — 75 in sync` · `--selftest OK — 11 bites`. ⛔ **CORRECTED AT SOURCE #104 — the ds-029 "enacted + mutation-tested" claim above covered the DETECTION clause only.** Driving the real page found Replay restarted only 3 of 4 Confirmation elements — `svg.success` never restarted (`void el.offsetWidth` is undefined on SVGElement, HTMLElement-only per CSSOM View, so the `none→prev` toggle never flushed). Fixed: `void el.getBoundingClientRect()`, `gen_showroom.py:285` + regen; all four elements now restart (proof: `460,finished→0,running→460,finished` etc.); mutation-tested both directions (reverted ⇒ reproduces the exact defect; restored ⇒ all four pass). Gates re-run green. **Lesson:** a mutation test proves the clause you mutated is load-bearing, not that the feature works — full arc `_DECISION-HISTORY/2026-08-05-104-unit-error-and-the-defective-enactment.md`. Legend-variant centring now MEASURED not decided → see the dedicated row below. |
| `reviews/OPACITY-PRIMITIVES-2026-08-05-v1(.REVIEW).html` (the 4% ladder spread, #96-D2/#98-D3) | 2026-08-05 #99 | ✅ **RULED IN FULL #99 — D1 full ladder · D2 `--alpha-04…96` · D3 migrate-all ties-DOWN · D4 REVERSED by #99-D1 (charts SOLID, state-changes-only licence).** Enacted + render-proven same window (ledger § ★ #99, ruling ds-026). ⬛ **ONE FORK REMAINS FOR DAVE: the wider literal-opacity corpus — 125 declarations / 49 snippet files (MEASURED #99, `_DS-IMPROVEMENTS.md` § #99) — sweep-now vs per-component-as-opened.** ⬛ **RESIDUAL ① `--pri-hover` — MEASURED, NOT PROMOTED → see the dedicated row below (#104).** |
| `reviews/LEGEND-CENTRING-SPREAD-2026-08-05-v1.html` (donut/pie legend-variant centring, Option A vs B) | 2026-08-05 #104 · **RULED #106** | ✅ **RULED #106-D1 (Dave, ds-031): OPTION A — KEEP AS-IS.** The 109px offset is ACCEPTED; Option B not taken. Original measurement retained below. ⬛ **AWAITING DAVE'S EYE — MEASURED, NOT DECIDED.** Option A (current, `.dv-donut-row{justify-content:center}`): ring **−109px off true container centre**, CONSTANT at 1180px and 760px — offset = (legend 190 + gap 28)/2 = 109 exactly, legend-footprint-driven not proportional. Option B (not enacted): a hidden `.dv-leg-spacer{min-width:190px}` mirroring the legend ⇒ **0px** offset. Light+dark, both widths, screenshotted. Nothing enacted pending his pick. |
| `reviews/PRI-HOVER-MEASUREMENT-2026-08-05-v1.md` + `.html` (`--pri-hover` opacity-derivation, #99 residual ①) | 2026-08-05 #104 · **RULED #106** | ✅ **RULED #106-D2 (Dave, ds-032): `--alpha-68` APPROVED — but SCOPED TO THE BUTTON ATOM, not 8 per-component edits.** NOT ENACTED: Dave ruled blast radius measured first (58 declarations / 10 of 77 files; 8-sites vs 9-files delta UNRECONCILED → #107). Original measurement retained below. ⬛ **AWAITING DAVE'S WORD — a promotion, not a pick (derivation governance).** All 8 candidate colours are pure neutral grey — no problem-hue hit. Group A (Icon-button/Empty-state/Form-layout/Stepper, live `color-mix(…70%…)`): swap to `--alpha-68` is a quantified delta — L `#5F5F5F→#636363` (+4/255), D `#B7B7B7→#B2B2B2` (−5/255); label contrast 6.39→6.01:1 (L), 6.3→5.96:1 (D), both clear 4.5:1. Group B (Modals/Action-bar/Confirmation/Drawer, flat `var(--pri-hover)`): exact if ramp-snap kept (re-snapping at 68% lands on the SAME stored steps, 0px change). Legacy `#BA1110` + Supercharge overrides: NOT promotable, never opacity-derived. Sub's recommendation (NOT a decision): swap Group A, leave Group B's stored hex, correct Group B's `$note` derivation number. |

| `_RESEARCH-graph-engineering-2026-08-05-v1.html` + `-v2.html` + `-v3.html` (graph-engineering audit, Swiss) | 2026-08-05 #105 · **-v3 DELIVERED #107** | ✅ **-v3 DELIVERED #107, pays #105-D1** — `_RESEARCH-graph-engineering-2026-08-05-v3.html`, Dave verbatim *"I want it to be honest."* Six honesty defects fixed; worst: the closing band self-labelled "the honest read" still carried the pre-correction four-type framing. Also reconciled a 7-vs-9 edge-type contradiction against `_build_decision_graph.py:38–53` + ADR-0012's dated amendment (nine is current, the 7→9 change now dated explicitly). Responsive gap declared in v2 CLOSED by numeric assertion. ⬛ **AWAITING DAVE'S READ.** ⛔ **CORRECTED #108: "v3 untracked, not yet staged" was STALE the moment it was written — `git log` shows v3 WAS staged and committed in #107's own wrap (`90c1d9d`).** |
| `reviews/TYPE-CSS-180-SPECIMEN-2026-08-06-v1.html` (`type.css:180` dark-mode specificity, #106-D3 deferred pending a specimen) | 2026-08-06 #107 · **RULED #108** | ✅ **RULED #108-D1 (Dave, by eye, `ds-033`): ink = `#1A1A1A`, not `#111111`.** Measured: delta +9 on R,G,B identically — achromatic, so the red/amber instability caveat does NOT apply; contrast vs white body text 18.88:1 (`#111`) vs 17.40:1 (`#1A1A1A`), both AAA — this was preference, not a contrast question. ⬛ **NOT YET ENACTED** — the literal at `type.css:180` still reads `#111`; #109's job. ⚠ **Record correction (from #107):** `type.css:180` really is `[data-theme="dark"]{background:#111;color:#fff;}` at 0-1-0, but there is no literal `body{background:var(--page)}` line INSIDE `type.css` — that 0-0-1 pattern lives in each consuming snippet's local stylesheet (e.g. `Account-card.reference.html:32`). **Bonus finding:** the same line 180 also overrides `color:#fff` over each snippet's `color:var(--text)` — invisible today because both resolve white, same literal-over-token pattern. |
| `outputs/_PARTITION-button-primary-2026-08-06-v1.md` (button/primary scope partition, enacts #107-D1 "partition first") | 2026-08-06 #107 · **#108-D2 EXTENDS #108** | ⬛ **STILL AWAITING DAVE'S FINAL SCOPE RULING.** #108-D2 (Dave): measure the other 35 colliding token names BEFORE ruling scope — only 5 of 40 were value-checked; extends #107-D1 one level deeper. Inscribed `ds-034`. ⚠ **The sweep's SPEC CHANGED this session (see the new finding row below): test value agreement PER THEME, not globally** — a global sweep would manufacture ~35 false findings, because themes are EXPECTED to diverge on the same token name (`ds-035`, Dave's four-theme standing constraint). #109's first job, per-theme. Groups from #107: **A** full button ladder (4 files: Button, Form-layout, Icon-button, Stepper) · **B** simple CTA, default+hover only (5: Action-bar, Confirmation, Drawer, Empty-state, Modals) · **C** brand scope, NOT a button case (1: Hero) · **D** secondary only (1: File-upload). ⚠ Lives in the gitignored `outputs/` folder — not a git-tracked path; Dave reads it locally. |
| `outputs/_FINDING-canon-pri-hover-brand-mono-fork-2026-08-06-v1.md` (`--pri-hover`/`--sec-hover` cross-theme "fork", measured + self-corrected) | 2026-08-06 #108 | ✅ **CLOSED, INFORMATIONAL — not a pending decision.** Measured live in `canon.css`: `--pri-hover` = `#BA1110` at `:root` vs `#626262`/`#B7B7B7` under `.cn-button`/`.cn-modals`; `--sec-hover` resolves to three different upstream tokens across three components. The MEASUREMENT stands; the DEFECT conclusion the doc first reached does not, once Dave's four-theme requirement (`ds-035`) is applied — the fork is almost certainly the theme layer working, not debt. ★ Governs `ds-034`'s sweep spec (PER THEME, not global). ⚠ Lives in the gitignored `outputs/` folder; Dave reads it locally. |
| `notes/_briefs/2026-08-06-graph-candidates-pricing-brief.md` (graph-engineering candidates 1–4, priced; the `-v3` research doc's enactment) | 2026-08-06 #115 | ⬛ **AWAITING DAVE — ONE ITEM, AND IT IS ITEM 4 (DEMOTE).** Items 1, 3 and the **mark-half of 2** were RULED and ENACTED this session (#115-D1/#115-D2, `9b47152` · `6a16633` · `ce0cc7f`). ⛔ **Item 4, DEMOTION, is NOT ruled and NOT scheduled** — it is decided on **`python3 knowledge/_graph_edges.py --tally`** (save-vs-noise evidence from `knowledge/_graph-mark-observations.jsonl`), never on recollection; the observation window was instrumented precisely so this ruling has provenance (Dave's catch: *"do I have to write these down on a postit or something??"*). First tally: 15 marked results, 4 with ⛔, `ls:LIFECYCLE` the predicted noise class (17 dead-node mentions — a section ABOUT supersessions). ★ **Read the mark correctly before ruling: ⛔ means the result MENTIONS a superseded node, NOT that the result is dead.** ⚠ Re-priced in-flight: node-id↔record overlap measured **0/575**, so candidate 1's *"Small"* in the research doc is **Medium**. |
| `_TRIAGE-118-bucket-sort-v1.md` (the decision-backlog bucket sort, run on Dave's *"Show me the bucket sort before you act"*; **floated, nothing enacted**) | 2026-08-07 #118 | ⬛ **AWAITING DAVE — ONE ITEM AND ONE ITEM ONLY: the type-composite gate's TIER, (a) BLOCKING now vs (b) SHRINK-ONLY RATCHET at 1,101.** Claude recommends **(b)** and names the risk against its own recommendation — *a baseline at today's count has exactly the shape of "a cap raised to clear its own gate."* ⛔ The other 16 rows need nothing from him: 8 were taken back as mis-escalated, 1 is stale, bucket D is Claude's entirely. ⚠ 9 of the 17 were sorted on nature, UNPROBED — declared. Verbatim home: `GOOD-MORNING.md` §C·2. |
| `reviews/outputs/mark-map-controller-v6.html` (the #122 mark-map pass — three lanes) | 2026-08-07 #122 | ⬛ **AWAITING DAVE'S EYE — the RULINGS are closed, the RENDER is not.** `s122-D2`…`s122-D5` were taken by eye off v5; v6 is the post-enactment state: **mono editable** · **console+SC** with a live `console == supercharge` assert · **legacy display-only**, asserting fills against {#col25-017} AND marks against `s122-D5`. ⚠ **NOT DRIVEN VISUALLY — nobody has eyeballed rendered marks on the new fills.** ⚠ Six parked consequences ride with it (legacy warn/info backgrounds unruled · `ownsHexes` stale · SC badge shift · legacy success leg 4.56 · `*-tint` unruled · the visual confirm itself) — standing home `_LIVE-STATE.md` § OPEN. ⚠ Lives in the gitignored `reviews/outputs/` folder; Dave opens it locally. |
