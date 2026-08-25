# #218 crank — CHARTS lane handoff receipt (Window 2, worker)

Session: `Apollo - #218w2: charts crank lane` · 2026-08-24 · Fable worker + 1 Opus build sub.
Divvy: `notes/_briefs/2026-08-24-218-crank-divvy.md` § Window 2 — lane-2-apollo-charts, §C·1 strands (a)–(d).
⛔ NO commits, NO rulings, NO memory writes from this window. Tree changes left in place for the conductor.
Gauge: boot 67,152 · FILL at receipt-cut 164,619 real (stop 190,000, seam CLEAR ×3: opener · post-survey · pre-receipt) · `subs 150043 tokens (n=1)` (QUOTA, not window FILL).

## What this window changed (region: chart snippets · showroom · dv-* verifies · _proforma)

**ONE build: DV-D16 wording ② ENACTED on Chart-bar's stacked-column figure. CSS-only, zero JS bytes.**

- Files: `knowledge/snippets/Chart-bar.reference.html` (+52/−13) · NEW `knowledge/_render/verify_dv_d16_render.py` · NOTHING else. Built by an Opus sub; replayed in-window by this seat (static verify GREEN · `b-value` red arm RED by name · `gen_component_partials.py --check` OK · `_validate_behaviour.py` OK, byte budgets identical).
- Mechanism: per-rect inline custom properties (`--b1`/`--b2`/`--self`) derived by script from the file's own y/height attributes (DV-D14 ENACTED geometry, never data values); shared `--grow-dur:760ms` timeline via 3 `@property` numbers animated `ease-in`/`linear`/`ease-out`; stacked rects cancel `dvGrowY` and compose translateY(cumulative animated below-height) · scaleY(self). The float rides the *cumulative animated* height — consequence: dv-004's 2px boundaries hold **at every frame**, not just at rest (the naive per-own-curve variant was built, measured opening 8.6–30.5px mid-flight, and discarded).
- Proof: static parse (12 rects/4 columns, count-guard ≥3, every `--b` re-derived and matched) · render on Chromium 151 (curves read back to 3 dp at t=0.10/0.50; contiguity 2.0±0.6px on 8 boundaries × 6 frames; all 4 columns concurrent — the discriminator against reversed wording ①; reduced-motion and JS-off both rest at full height, driven not asserted) · `_verify_dv_stacked_enactment.py` ALL PASS (2px min gap, key contrast 4.61:1, snippet+showroom, 1180+760, real cut) · 9 mutation arms all RED by name.
- UNPROVEN, declared: Chromium-only (`@property` is load-bearing; degradation path to final-frame is reasoned, not driven — price: one browser-matrix run) · the new verify skips the font farm (the stacked-enactment proof covers it).
- Evidence for Dave's eye: `notes/_receipts/2026-08-24-crank-charts-dvd16-mid-t042.png` (mid-flight, contiguous) · `…-dvd16-end.png`.

## Ruling-shaped questions → Dave (via conductor; nothing decided here)

1. **Easing vocabulary:** built with the literal CSS keywords `ease-in`/`ease-out` per the ruled words. If Dave meant house-tuned beziers (the file's `cubic-bezier(.22,.61,.36,1)` family), it's a two-token edit.
2. **On-chart letter keys don't ride the float.** Measured: at HEAD 8/12 keys already sat outside their segment at t=0.42; after the float 12/12 mid-flight (end state 12/12 inside, unchanged). Cheapest CSS-only mitigation if wanted: delay stacked keys' `dvFade` by `var(--grow-dur)`. Motion/feel call — NOT enacted.
3. **DV-D16b "every stacked surface" vs Chart-stacked-area:** stacked-area animates by FADE (bands→line→markers), not growth. Does forward-binding convert it to concurrent growth? Visual-design call beyond the two measured deltas; per the mock-the-readings rule this wants 2–3 renders side by side before any build.
4. **ds-012(b) gutter-relative plot area — NOT built, fence-shaped twice over:** the ledger marks it fenced pending a control-attributed diff, and its decision surface belongs in `reviews/` (outside this window's region). Priced plan: control-first render pair (pre/post, both widths, colours diffed as colours) via extending `verify_dv_j2_render.py` as the ledger prescribes; narrow-width floor is Dave's eye; must not share a commit with sibling ds-012.

## Findings (state corrections + fenced items, owed to conductor)

- **⚠ Stale-queue class, 4th recurrence on §C·1:** strand (b) says "~26 itinerary gaps"; the measured `reviews/ITINERARY-STATUS-2026-08-21-v3.json` says **78 Gap + 7 Partial** of 124 rows. The queue figure predates the v2/v3 itinerary widening.
- **⚠ `_validate_behaviour.py` prints "of 32 KB" (lines 144, 216) while the cap is Dave's re-dialled `PAGE_BYTES = 34*1024` (#96).** Current: 34,611 of 34,816 = **205 B page headroom**. The PASS is legitimate; the print string is stale and reads like an unearned green. Gate file = Window C's region — two-string fix, theirs.
- **⚠ DVD "SCOPE MEASURED" paragraph is wrong on one word:** stacked segments were NOT "all at once" — they carried a 45ms/rect `animation-delay` stagger (0→495ms). Now inert (rects run no animation), attributes left in place: removing them is an emission-contract change beyond the ruled deltas. **The generator should stop emitting `animation-delay` on stacked rects** — generator is fenced from this window.
- **⚠ Strand (a) is CLOSED-shaped:** chart-text instrument fixes LANDED #66 (trusted corpus figure 30, triage DAVE'S, still waiting) · ds-020 enacted #69 · DV-J2b folded #67, overtaken by s182-D2. Nothing in (a) was buildable that isn't already Dave-owed triage.
- **Strand (c) templates+shells:** deliberately NOT started — ADR-shaped, "best AFTER the ruling batch" premise unchanged; 28 of the wave-3 Gap rows are its Layer-2 subject matter, so sequencing it before wave-3 Layer-2 briefs still looks right.
- **Strand (d) enact window:** surveyed; every live candidate is token/registry/gate territory (fenced) or Dave-owed (radius tuner v2). No chart-snippet-shaped enactable found beyond DV-D16 ② (built).
- **#185 class:** `knowledge/_render/verify_dv_d16_render.py` has no `_state.json` store row — store is fenced; row owed at reconcile.
- **Shared-tree observation:** Window 3's edits (Sidebar-nav, Command-palette, Navigations, Pagination, Video-player, Payment-card-visual + showroom pages, `?? …crank-behaviour.md`, 3 `verify_behaviour_218w3_*.py`) were visible in this tree throughout. Untouched by this window; regions held disjoint.

## Wave-3 lane-brief draft (strand (b), paper only — conductor's to adopt)

From the measured v3 (78 Gap): **lane α — Inputs & forms P1** (8: form layout+validation · date · date-range · time · number/currency · file upload · OTP · textarea — one family idiom, heavy a11y surface) · **lane β — Feedback & status P1** (5: alert · toast · drawer · popover · skeleton — overlay/announce idioms shared) · **lane γ — Data display P1** (4: data grid · stat/metric card · empty state · charts-kit gap row is a register artefact, verify before briefing) + Partial repairs (Modal/Dialog P1 · Account selector P1). ⛔ Navigation family (5 gaps incl. sidebar/nav-rail + command palette) COLLIDES with Window 3's live lane — do not brief in parallel; sequence after their reconcile. Layer-2 (shells 7 · templates 11 · lock-ups 10) → hold for strand (c)'s ADR. Serial set unchanged (registry · MIGRATED_SNIPPETS · CATEGORIES · spine · ONE conductor commit).
