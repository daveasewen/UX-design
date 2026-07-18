# Register spread, restyle saga + seaworthiness (2026-07-05)

> STANDING: decision-history file — provenance record, never edited after landing.
> **Relocated VERBATIM from `_LIVE-STATE.md` (lines 566–590, 734–736, 852–869, 904–1033) on 2026-07-18**, per the ruled
> consolidation (`reviews/CONSOLIDATION-AUDIT-2026-07-18.html`). Spine summary: `_LIVE-STATE.md` → OPEN §9 + DEAD.
> **RESURRECT (Dave, 2026-07-18): YES — likely feeds the Creative and Explore modes of Apollo Create.** The experiments here are evaluation material for tuning the machine once the factory has all its parts. Related: `knowledge/_fitness-test/register-spread-2026-07-05*/`, memory `generation-mechanism-ideas`.

---

- **✅ Worked spread — DONE 2026-07-05, TWO instances (Sonnet + Opus re-run).** First
  retrieve/extend/invent spread under the §9 inference definition: SME Payments screen, three bands
  generated in isolated parallel passes. **Sonnet pass:** cardinal curbs held with zero violations;
  foundational curbs diverged monotonically with the register, as predicted. **Dave reviewed the
  actual HTML and found two real gaps**, not just polish: (a) sober used the never-reviewed
  `.c-stat-grid` utility instead of the gate-reviewed `.cn-account-card` for the same data —
  the brief said "retrieve" but had no rule ranking canon artifacts by rigour; (b) expressive
  wasn't bold enough despite nominal MAX-inference licence. Dave also asked whether a
  build→review→correct loop exists (**it didn't**) and proposed testing Opus. **Fixes made same
  session:** (1) `_TEST-BRIEF-v2-sme-payments.md` §2 now states an explicit, mechanical **canon
  rigour tier** — `.cn-*` (gate-reviewed, generated from snippets) always preferred over `.c-*`
  (hand-authored, never reviewed) when one fits; (2) re-ran the full spread on **Opus**. **Opus
  re-run result:** all three bands now retrieve `.cn-account-card`; sober dropped to **zero**
  `.c-*` fallback usage (from relying on it for its centrepiece); expressive reads as a
  substantially bigger compositional swing (needs Dave's eyeball, not just structural grep) — same
  cardinal-curb floor held throughout with zero violations. **Bonus finding:** two independent Opus
  passes caught a real ambiguity in the contract's own §3 wording (conflated "sum of all 5 rows"
  with "scheduled total") that neither Sonnet pass flagged — fixed in the contract. Full writeups:
  `knowledge/_fitness-test/register-spread-2026-07-05/_PROBE-and-selfcheck.md` (Sonnet pass) +
  `register-spread-2026-07-05-opus/_COMPARISON-sonnet-vs-opus.md` (the re-run + comparison).
  Memory: `register-inference-ramp`, `spread-review-gaps-2026-07-05`. **Still not "proven"** — one
  screen, two passes changing two variables at once (rigour-tier rule + model), no rendered visual
  check, and Dave hasn't yet confirmed the Opus expressive band actually reads more exciting. A
  designed build→review→correct loop remains unbuilt (Opus self-corrected mid-pass on one bug, but
  that's not the same as a designed loop).

---

- **Divergence probe — first real run done 2026-07-05** (structural/grep-based, not the full
  novelty-scoring tooling named in §9). See the writeup above. The formal tooling (threshold
  calibration, automated novelty count) is still named-not-built.

---

- **✅ Seaworthiness plan — DONE 2026-07-05 → `notes/_SEAWORTHINESS-PLAN_2026-07-05.md`.** Curated,
  dependency-aware sequence (not a flat backlog): hull patches (ingestion Phase 0 + capture ritual) →
  **big-rock #1 Ingestion Phase 1** (Sutherland token migration, confirmed unblocked) → **§9 worked
  spread in parallel** → **big-rock #2 PM-KG MVP** (staleness gate) → finish/unify (Phase 2→3→4, with
  the §4 language-strip inside Phase 3). Waiting/parked (D2, toolkit t2, harness-modes, TOV spin-off,
  ADR-0004 ops) kept off the critical path. Capture ritual/gate spec decided in the doc (ritual now,
  gate script alongside PM-KG MVP).
- **✅ Phase 0 (ingestion tracking hygiene) — CLOSED 2026-07-05.** The "39 metas vs 38 in the
  compliance graph" drift flagged in the prior session's KG spot-check was a **false alarm**: 39
  files exist in `components/`, but one (`EXAMPLE-button.meta.json`) is the authoring template,
  correctly excluded by `_build_compliance_kg.py`. Real component count is 38, matching the graph
  exactly. Rebuilt the KG to confirm — `git diff` on `compliance/graph-index.json` and `compliance/rules/`
  was **empty**; the graph was already current. Fixed a latent bug while here: `generated` was a
  hardcoded literal (`"2026-06-18"`) rather than today's date — a miniature of the exact
  "tracking rots silently" failure this plan exists to prevent; now stamps dynamically
  (`datetime.date.today()`). The `_DESIGN-SYSTEM-GAPS.md` correction banner + `_INGESTION-ASSESSMENT_2026-07-05.md`
  as single entry point both confirmed standing. Phase 0 fully closed; Phase 1 (Sutherland token
  migration) is next and is real, unblocked work — unlike this drift.

---

## The superseded gravity-fix target + the restyle saga (self-labelled historical)

- **🔴 SUPERSEDED BY OPEN QUESTION BELOW (2026-07-05, end of session) — Dave's verdict landed,
  and it's not the "converges once gravity-fixed" outcome this target-state assumed.** See the new
  OPEN entry "What does the §9 spread actually reveal?" — this target-state's own diagnosis (craft
  gap → sourced external references → re-run) is no longer the live framing; kept below for the
  historical trail only.
- ~~**🎯 Inference-gravity for the register ramp (expressive craft fix) — ⚠️ BLOCKS external
  review of the §9 spread until resolved (Dave, 2026-07-05).**~~
  - **Target:** the expressive band reads as genuinely exciting/award-calibre digital-product craft
    (motion, depth, interaction choreography) — not just "sober, but bigger" — while the cardinal
    curbs (brand colour retrieved not typed, type, square corners, a11y/safety floor) still hold
    with zero violations, same as the two spreads already run.
  - **Current vs target:** two isolated 3-band spreads run (Sonnet, then Opus) on the same SME
    Payments contract. Both closed the sober retrieval gap (finding 1 — now uses `.cn-account-card`
    via the canon-rigour-tier rule) but **neither closed the expressive excitement gap** — Dave
    judged both against `sme-payments-portfolio.html` (an older, ungoverned "craft piece" with
    hover-lift+shadow/spring easing, radial-gradient hero glow, count-up motion, backdrop-blur
    modal) and found the governed expressive bands still underwhelming by comparison.
  - **Diagnosed cause (this session, confirmed against the actual prompts):** every expressive
    prompt gave *permission* (curbs lifted) but never *direction* — no external creative reference,
    only internal/corporate source material (`canon.css`, `brand-principles.md`,
    `colour-usage.md`). Permission without a target to reach for makes the model recombine what it
    already has rather than invent something new. Full diagnosis: memory
    `spread-review-gaps-2026-07-05`; comparison data: `_COMPARISON-sonnet-vs-opus.md`.
  - **Blockers:** the design tension is resolved in principle — an explicit guardrail now exists
    (pattern only: composition/motion/interaction; never colour/type/logo, which stay retrieved
    from HSBC canon) — but **Dave's eyeball verdict on the actual result is still outstanding.**
  - **Path — steps 1–3 DONE same session, step 4 is next:**
    (1) ✅ defined the inspiration source + guardrail as an explicit "inference gravity" instruction
    (Linear/Stripe/Mercury/Ramp/award-calibre-fintech, each with a named pattern to extract —
    sourced via web search 2026-07-05, not recall); (2) ✅ added it to
    `_TEST-BRIEF-v2-sme-payments.md` §2's expressive bullet, alongside the corrected §3 wording
    (the scheduled/awaiting labelling ambiguity found during the Opus run); (3) ✅ re-ran **only**
    the expressive band on both models as `expressive-v2.html` in each spread folder — grep-verified
    (not just self-reported): motion/animation/transition mentions roughly doubled-to-tripled
    (Sonnet 4→23, Opus 2→15), `backdrop-filter`/blur depth technique appears for the first time in
    either run (0→5 Sonnet, 0→3 Opus), `prefers-reduced-motion` still present in both, zero
    `border-radius` violations, zero brand-colour leaks (every hex is inside a comment citing the
    `var()` it derives from), all figures verbatim including the corrected §3 wording. **(4) NEXT —
    Dave reviews via the updated `register-spread-2026-07-05-compare.html`** (now has an
    "Expressive (v2 — gravity fix)" button per model, plus a direct "Portfolio piece" reference
    button) **against `sme-payments-portfolio.html` specifically for motion/depth/interaction craft.
    This is the actual test — structural counts are a proxy, not the verdict.** (5) once Dave
    confirms, fold the mechanism into charter §9 as a named piece and only then is the §9 spread
    presentable outside this session. **Scope discipline held:** this stayed inside the existing
    "prove-the-core, §9 worked spread" parallel track from `notes/_SEAWORTHINESS-PLAN_2026-07-05.md` —
    did not touch hull patches (done) or reorder Ingestion Phase 1 (still queued, untouched).
  - **Additional diagnostic run, same session (Dave's idea): pure-inference ceiling probe.**
    Two cold Opus passes on the same data, zero brand governance at all (no canon, no curbs, no
    a11y mandate) — with vs without the named influences — to see the true ceiling and isolate
    where the governed version's gaps are. Finding: colour/type/radius gaps are expected (that's
    what the cardinal floor is *for*); the more useful signal is structural — the ungoverned runs
    reached for a genuine organising idea (e.g. "time as the spine") that the governed gravity-fix
    prompt didn't, suggesting the next iteration should ask for a point of view on the data's
    structure, not just borrowed craft patterns. Writeup:
    `register-spread-2026-07-05-diagnostic/_FINDINGS.md`.
  - **Also fixed same session:** a real CSS cascade bug in Opus's `expressive-v2.html` (an
    equal-specificity, later-in-source `.cover > *{position:relative}` rule was silently
    overriding the decorative glow div's `position:absolute`, dropping it into normal flow as a
    520px block and pushing all content down — the "huge black box" Dave flagged from a
    screenshot); and a real comparability bug — three of the ten spread artifacts (Sonnet
    `expressive-v2`, Opus `sober` v1, Opus `balanced` v1) were built as fixed mobile-phone-width
    layouts (390-560px, one with a bottom tab bar) while the rest were desktop-width (900-1240px).
    Normalised all three to a shared desktop container (960px) so the comparison viewer
    (`register-spread-2026-07-05-compare.html`, now also carries the two diagnostic files) is
    genuinely like-for-like. No content/data/curb changes in any of these fixes.
  - **✅ Restyled-ceiling build, same session (Dave: "if we style these using the HSBC
    primitives I'd be pretty happy").** Took `without-influences.html` (Dave's pick — the
    diagnostic piece with the stronger organising idea) and rebuilt its `:root` palette as a
    thin alias layer into canon tokens (accent/warn/info/ok/muted), replaced all three Google
    Fonts with the Univers ramp, squared every corner except the avatar exemption, and
    reinstated the cardinal safety/a11y floor the diagnostic had been told to skip (the
    £45,200 payroll approval was identical to the low-value row — now gated behind a
    confirmation dialog; added focus rings + reduced-motion handling). Kept every
    compositional/motion decision: the "Today's arc" day-timeline and the horizontal
    scheduled-payments timeline (flagged as candidates — no `.cn-*` equivalent exists for
    either). One disclosed deviation: outflow is no longer rendered in red (HSBC's dark-mode
    error token shares the same hex as the brand accent; kept red to the one accent/approval
    job, direction carried by an icon instead). File: `without-influences-hsbc.html`; wired
    into the comparison viewer. Dave confirmed via screenshot that the restyle's structure
    matches what he's judging against — visual verdict on the restyle itself still pending.
  - **✅ Bug found + fixed from that screenshot:** the hero balance number ("122,450") was
    rendering effectively invisible. Root cause was the exact trap canon.css documents at its
    own line 495-496 — my restyle's `:root{ --ink: var(--page); --panel: var(--surface);
    --paper: var(--text); ... }` alias block was a BARE `:root` selector, so every alias
    computed once against `<html>`'s own (light-theme) tokens and inherited that frozen light
    value down, instead of recomputing at `<body data-theme="dark">` the way canon's own
    tokens do. Fixed by matching canon's own selector pattern: `:root, [data-theme="dark"]{...}`.
    Same class of bug as the earlier Opus cascade fix — a real, generalisable lesson (declare
    theme-dependent aliases against the same selector list the tokens they wrap use, never bare
    `:root`). **Still open, not yet fixed or raised for a ruling:** the "Free buffer" gauge
    legend uses the same accent red as "current balance/live" and the approve button — one
    accent doing double duty (live-status AND good/free-status), which may read oddly against
    normal finance-UX convention (red = attention/negative). Flagged for Dave's eye, not
    silently changed.
  - **⚠️ Caught by Dave, not by me:** when asked directly "did you put the restyle through the
    gates or use your own inference?" — the honest answer was **inference, not gates**. No
    `_SCREEN-GATE.md` existed for this file, no validator run showed in the commit history, and
    the file wasn't even named `*.canon.html` (the default glob `_validate_screen.py` scans), so
    the pipeline would have been blind to it either way. Ran `_validate_screen.py` against it for
    real: **FAIL** on first pass — 2 hex refs (`#000`/`#FFF`, only inside explanatory CSS
    comments, reworded to "black"/"white") + 3 UNKNOWN icon paths (hand-drawn stroke arrows for
    inflow/outflow/net-movement direction, a genuine icon-source-rule violation). Fixed by
    swapping in the real library glyphs (`assets/icons/arrows-and-chevrons/arrow-up.svg` /
    `arrow-down.svg`). Re-ran: **PASS**. Lesson for next restyle: run the gate as the LAST step
    before presenting, not as an afterthought prompted by a direct question — a hand-built
    "canon-primitive" restyle is a claim the gate exists specifically to check, not something to
    self-certify.
  - **⚠️ Caught by Dave again, then verified with real numbers, not just fixed on faith:**
    Dave said "this would fail accessibility for a start" after seeing the balance figure fixed.
    Ran the `design:accessibility-review` skill + pulled canon's actual dark-theme hex values and
    computed real WCAG contrast ratios (not the shallow `_validate_screen.py` a11y check, which
    only covers reduced-motion + target-size and gave a false-confidence ✅ earlier — same shape
    of gap as the [[gate-blindspot-state-contrast]] lesson). Found genuine 1.4.3 failures, all in
    my OWN invented tint compositions (not canon's `.cn-*` patterns): rail "current balance" value
    (red text on panel) 3.23:1; gauge "free buffer" label (red text on red-tinted fill) 2.92:1 —
    worse, and even canon's real error-tint token only gets red text to 3.71:1, so red is
    structurally unfit as small/normal-text colour on any dark tint, only as a solid fill with
    reverse text (which is why the buttons pass at 5.2:1); "Scheduled" tag (info/blue text on a
    hand-mixed 12% tint) 3.67:1; scheduled-card date (info/blue on bare panel) 4.24:1, borderline-
    failing. Fixed: the two red instances now use `--paper` (white) text, keeping red as the
    accent/fill only; the two blue instances now sit on canon's REAL `--info-tint` token instead
    of a hand-mixed approximation — verified 4.92:1, passes. Also closed a real modal gap found in
    the same pass: the payroll confirmation dialog had Escape-to-close but no actual keyboard trap
    (Tab could reach the still-exposed-to-AT background) — added Tab-cycling inside the dialog and
    `aria-hidden` on the background wrap while open. Re-ran `_validate_screen.py`: **PASS**.
    **Pattern now twice-confirmed:** a hand-built "canon-primitive" restyle needs its OWN explicit
    verification pass (gate script AND a real contrast check) before presenting — passing the
    existing automated gate is necessary but not sufficient, because that gate doesn't check
    contrast on compositions that aren't `.cn-*` snippets.

