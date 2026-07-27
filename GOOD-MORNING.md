# Good morning, Dave ☕

> **RENAME THE WRAPPED CHAT →** `Apollo — the suite was asserting the OLD ruling: DV-D17 ENACTED and DOM-proven (108/108 + 27/27, three neutered controls), six green checks rewritten not deleted, the donut's "sequence" is ONE timeline so DV-D16 re-prices down, legend migration COMPLETE and nobody knew · 60/60 · render OWED · flushed at ~60%`
> **TITLE THE NEXT CHAT →** `Apollo — RENDER-PROVE DV-D17 and DIAGNOSE ds-018 in the SAME licensed-cut harness run (one spin-up, two widths, snippet + showroom pane), then decide the per-member behaviour opt-in — dv-legend.js has 54 bytes of headroom, the group is at 90%, and there is NO cleanup left to buy space back`
> *(Titles are LABELS — role comes from Dave's opener line. The wave = the parallel model: Opus conducts, workers per lane, DIVVY in §DO-FIRST. Gauge bands: Green<45 / Amber 45–60 / Red≥60.)*


> ## ★ LATEST — 2026-07-27 (Mon **afternoon #7**, OPUS solo self-conducting, effort MAX — ★ **DV-D17 ENACTED: the first BUILD window after three record-only ones** · ★ **SIX GREEN CHECKS WERE ASSERTING THE SUPERSEDED RULING — a conformance suite goes stale exactly like prose** · ★ **the donut's "sequence" is ONE TIMELINE ⇒ DV-D16 re-prices ~30%→~19%** · ★ **legend migration COMPLETE (exit 0) and the record didn't know** · build **60/60 GREEN** · render OWED · flushed at ~60%): **The suite was an inscription of the old ruling, and only running it said so.**
> - **★ DV-D17 ENACTED — four lines in `canon/dv-legend.js`, injected into all 5 registered consumers.** A blank swatch checked while isolated sets `st.isolated = null; st.focus = null` and leaves isolate mode, so no row keeps `.is-solo` while several series show. **All three named bites covered, each with its own failing control.** ⚠ **RENDER-VERIFY IN THE LICENSED CUT IS OWED, NOT DONE** — jsdom proves the state machine, **not** that `.is-solo` stops painting, and **ds-018 is a live counter-example on this same component.** Anyone reading "108/108" as *done* is reading it wrong: **enacted · DOM-proven · render-OWED.**
> - **★ THE FINDING: SIX GREEN CHECKS ENCODED THE RULING DV-D17 SUPERSEDES.** Baseline **100/100 + 27/27**; after the fix **85/100 + 23/27**. That red was not a regression — members 20/21 and donut 12/13/14/20 asserted the **additive focus set**, the half of DV-D11 that DV-D17 kills. **Nothing in the repo connected "DV-D17 is ruled" to "six assertions now say the opposite"; only RUNNING the suite surfaced it.** Sibling of [[assertion-propagation-gap]], in a surface nobody had counted — **the verification tooling itself.** All six **REWRITTEN, NOT DELETED**, old wording verbatim beside each, so a reversal can never read as agent drift.
> - **★ BITE-THE-BITE ×3, WITHOUT MUTATING CANON.** Both suites gained a **`DVLEGEND` env override** (their own `JSDOM` idiom), so neutered copies are pointed at from outside: full revert **99/108 + 23/27** · release-to-**all-on** **105/108** · release-**silently** **104/108 + 26/27** · control **108/108 + 27/27**. ⚠ **PUBLISHED LIMIT — the donut suite CANNOT catch the all-on regression** (27/27 under it): its scenario starts all-visible, where `visible[]` and all-on are indistinguishable. **Only the members suite dims a spare BEFORE isolating.** Not interchangeable proofs of bite (i).
> - **★ STEP 0 ANSWERED FROM THE REPO — and "same as the pie" is TRUE OF THE EASING, FALSE OF THE APPEARANCE.** `sweepDonut()` (`Chart-donut.reference.html:889–945`) = **ONE timeline**, one `t0`, one rAF loop, **one sweeping angle**; segments only *appear* to hand off because one angle crosses them in order. Its envelope (accelerate through seg 1's arc → cruise → decelerate through seg N's) **is already Dave's easing rule as one continuous curve**; `prefers-reduced-motion` baked at `:901–906`. ⇒ **Reuse the architecture, envelope and reduced-motion answer; do NOT cite the donut as a visual precedent for wording ②.**
> - **★ DV-D16 RE-PRICED DOWN, the direction nobody double-checks.** `Chart-bar.reference.html:121–128`: stacked segments **already** run `scaleY(0)→1` from `transform-origin:bottom`, **all at once**, one `--grow:760ms`, CSS-only. **Concurrency exists.** Two deltas left: **(a)** upper segments don't FLOAT (fixed anchors ⇒ the stack gaps mid-animation) · **(b)** one shared easing curve, no per-segment curves. Both pure-CSS (below-height is static per chart ⇒ a per-rect custom property) ⇒ **no JS in physics**, B-D7 / DEF-003 hold. ⚠ **RE-DERIVE BEFORE BUILDING — a cheap-looking job is exactly what the throttle exists to doubt.**
> - **★ CORRECTED IN-WINDOW — I READ A GATE'S ADVICE TEXT AS LIVE STATE, and caught it at ritual step 3.** `_check_legend_migration.py` **does** exit 0 (WAVE COMPLETE), and GM/`_LIVE-STATE` **were** stale — they said *"combo + line remain"* after commit **`ba336dc`** had already migrated them. **That much stands.** But the gate prints its *"Now: delete the TRANSITIONAL block…"* list **UNCONDITIONALLY** (`_check_legend_migration.py:87–89`), and **`ba336dc` had already done it**: `dv-behaviour.js:146` is a **tombstone comment** where the block used to be (15,771 → **13,004 B**), and `class="dv-legrow` stays in the members' `extraContracts` **deliberately** — promoting it to the universal contract **fails the build**, because sparkline and scatter are in the dataviz GROUP but carry no legend. ⇒ **THERE IS NO CLEANUP LEFT AND NO RELIEF VALVE.** A memory file held the correct state the whole time and I hadn't read it yet. **Sibling of [[gate-narrows-its-own-rule]]: a gate said one true thing (exit 0) beside one stale thing (its todo list), and I took both as current.**
> - **⚠ SO THE CEILING IS WORSE THAN THE FIRST WRITE-UP SAID, and that is the real finding.** `dv-legend.js` = **16330 / 16384 bytes, 54 to spare**; dataviz page budget **29334 / 32768 = 90%** (was 88% before this session's comments). **Nothing cheap buys space back.** The known real fix is already on the board and is **Dave's call, not an enactment**: **per-member behaviour opt-in in the registry** (a schema change — the same item `Chart-sparkline`'s inert 15.6KB payload has been waiting on since 07-26, §C·4). **The next behaviour change to this group does not fit until that lands.**
> - **⚠ TWO THINGS FOR DAVE'S EYE, NEITHER RULED.** **(1) An enactment call that is MINE:** release also sets `st.visible[id] = true` so the clicked series shows; the literal reading restores `visible[]` **alone**, and they differ only when a series dimmed *before* isolating is then the one clicked — literal leaves it dimmed, so the click that ended the mode does nothing to what was clicked. **One line either way.** **(2) A DV-D13 consequence the ruling never named:** isolate Housing (`950/41%`) then check a second series — that click now **releases**, so the centre returns to `2320/100%` instead of growing to `1250/54%`. **DV-D13 is intact**; the selection is simply everything again.
> - **⬛ FLUSHED BY DAVE at the fork — the throttle's FIRST use on a job MID-FLIGHT.** Priced: fill ~55% + render ~10% + wrap ~5% ⇒ **~70% RED**; flushing lands ~60%. ⚠ **Overrun recorded per the throttle's own instruction:** DV-D17 was priced at 15% and ran nearer 20, **entirely on the byte-cap detour — self-inflicted, not a discovery.**
>
> ## ★ PRIOR — 2026-07-27 (Mon **afternoon #6**, OPUS solo self-conducting, effort MAX — ★ **DAVE'S CHART FLAGS CAPTURED *THEN* RULED: DV-D16/17/18 + ds-018 NEW + ds-012 RULED — and NOTHING ENACTED, by his choice** · ★ **DV-D16a REVERSED IN-WINDOW: the read-back offered three shapes and the right answer was in none of them** · build **60/60 GREEN** · 🟡 AMBER, flushed): **He picked an option, then twenty minutes later described what he actually meant — and it rejected the option he had picked.**
> - **★ THE CAPTURE HAPPENED BEFORE THE CONVERSATION, and that was the point.** Dave: *"I want to make changes to the charts too, I've noticed a couple of missed decisions, please note this."* Per **ds-017** — which cost the start of session #5 — a placeholder went into the pillar ledger **at the moment of the ask**, marked `OBSERVED-BY-DAVE, contents UNSTATED` with an explicit *"do not guess which decisions he means"*, then filled in as **`_DATAVIZ-DECISIONS.md` § Batch 10**. It was superseded four minutes later, which makes it look wasted; **it is not — it is what makes the EXISTENCE of the gap survive a window that ends unexpectedly**, and windows do.
> - **★ DV-D16 — ⚠⚠ RULED, THEN REVERSED IN THE SAME WINDOW. BOTH WORDINGS KEPT.** ① *"segment by segment"*, serial hand-off — **selected from a read-back, SUPERSEDED, DO NOT BUILD.** ② **IN FORCE:** *"they all grow at the same time, so they are floating and growing, rather than growing and 'handing off' to the next."* **One shared timeline; upper segments FLOAT upward as the ones below grow; per-segment easing CURVES, not per-segment timelines** — bottom `ease-in`, top `ease-out`, middles `linear` (his original easing rule, unchanged, and the durable part). Scope = **every stacked surface**; **`prefers-reduced-motion` ships WITH the first enactment** (*"fine"*) — ⚠ *reduced ≠ shortened*.
> - **★ THE METHOD FINDING, and it is MINE, not Dave's: A READ-BACK CAN ONLY OFFER ANSWERS THE ASKER THOUGHT OF.** Three tidy, mutually-exclusive, plausibly-exhaustive options **read as a complete space and were not one** ⇒ **a selection from an incomplete option set is indistinguishable from a ruling.** The instrument still earned its keep — it produced the correction — but **it manufactures confidence in proportion to how well-formed the options look.** ⇒ **STANDING MITIGATION, inscribed: when reading back a MOTION or FEEL decision, describe the resulting SENSATION, not the mechanism.** *"The top blocks float as the bottom grows"* would have been recognised on sight; *"segment 2 starts when segment 1 lands"* was not. ⚠ Sibling of the clarify-and-reflect-back rule — **the reflect-back happened, correctly, and still under-determined the answer. Doing the ritual is not the same as the ritual working.**
> - **★ DV-D18 cap-at-6 + ★★ FLOATED "Other" must be EXPANDABLE** (*"through some mechanism we'll explore later"* — unscoped by instruction, `_FUTURE-STATE.md`). ⚠ **Load-bearing as a PAIR: a cap with no route to the detail is data loss dressed as legibility** — already the donut's live state under `dv-pie-009`. ⚠ **JUSTIFICATION SHIFT RECORDED rather than quietly re-argued:** the cap answered a *duration* problem under serial motion; concurrent motion **dissolved that problem** (one timeline ⇒ N is free). **The cap stands on Dave's word but now rests on LEGIBILITY alone** — re-test it on that basis, don't inherit the old rationale.
> - **★ DV-D17 release-isolation + ★ ds-018 NEW + ★ ds-012 RULED.** DV-D17 cause read from source (`dv-legend.js:114/119/129`), **three enactment bites named** incl. *Reset must not self-disable while still filtered* — **the same expression ds-018 lives in; do not conflate the two fixes.** ds-018: disabled Reset paints ink, i.e. its own hover value; CSS is **correct as authored**, so **two competing causes** (token set ink-ish vs token failing to resolve ⇒ `currentColor`) — **separate them by `getComputedStyle`, never by reading CSS**, and the second would be **instance FIVE** of the silent-lookup class. ds-012: Dave re-reported the h-bar clipping **cold**, then ruled **(b) gutter-relative** — *"(a) fixes an instance, (b) fixes the class."*
> - **⬛ NOTHING ENACTED, BY DAVE'S CHOICE — and this is the throttle's first real use.** Priced at the fork: fill ~43% + enactment ~30% + wrap ~5% ⇒ **~78% RED**; DV-D17 alone hit the 60% boundary. The fork went to him and **he chose FLUSH.** ⚠ **First time it stopped work that was going WELL** — which is the case it was built for, and the harder one.
>
> *(Compaction 2c — keep ★ LATEST + 1 PRIOR, roll the rest. Older banners (the 07-22→24 chart-wave + ADR arc, the 07-25 AM v4 + midday→PM v5 + PM Memento-efficiency + PM#2 memory/routing-governor banners, and the 07-27 #5 throttle banner) are in `_GM-ARCHIVE.md` (Batches 1–10), verbatim, newest-first; durable narrative in `_DECISION-HISTORY/` + `notes/`.)*

---

*Briefing — refreshed 2026-07-27 ~13:15 BST (date from `date`), session "the read-back offered the
wrong options — Dave's chart flags captured, ruled, and deliberately not built" (Opus 5 solo
self-conducting, effort MAX). §A = orientation · §B = session · §C = queue.*

## ⬛ DO THIS FIRST

> **✅ CLOSED, do not re-open.** ds-014 calls (a)(b)(c) — RULED, ENACTED, RENDER-PROVEN. **★ DV-D17 is
> ENACTED + DOM-PROVEN (session #7) — its CODE is done; only its RENDER is owed. Do not re-implement it.** The legend wave,
> ds-013, ADR-0016 P1/P3-advisory all stay closed. **Nothing here is owed twice.**
>
> **✅ ALSO CLOSED — "the gauge must be a THROTTLE" is RULED AND INSCRIBED** (`_RUNBOOK-context-gauge.md`
> § ★ Half 0b, session #5). ⚠ *This block previously carried it as an UNRULED proposal for a full session
> after it had been ruled — the exact **ds-017** failure, found here by re-reading rather than by any gate.
> If you are reading a "Proposal (UNRULED…)" in DO-FIRST, check the runbook before believing it.*
>
> **★★★ THIS WINDOW = ONE HARNESS RUN THAT PAYS FOR TWO JOBS, THEN A CLEANUP THAT IS ALREADY AUTHORISED.**
> **0. RENDER-PROVE DV-D17 *and* DIAGNOSE ds-018 IN THE SAME SPIN-UP.** Same component, same page, same
>    two widths, same licensed cut — doing them separately pays the harness cost twice for nothing.
>    Read `knowledge/_RUNBOOK-render-verify.md` first; do **not** reconstruct the pipeline.
>    **(a) DV-D17's owed proof:** assert `document.fonts.check(...)` FIRST, then confirm **no `.dv-legrow`
>    resolves the `.is-solo` treatment** (ink border + 6% ink fill) after isolate-then-check-on — in the
>    **snippet AND the showroom pane**, at both widths. ⚠ Showroom panes are `srcdoc` IFRAMES: query
>    `page.frames`, not the top document. ⚠ **jsdom already says 108/108 — that is the state machine, not
>    the paint.** The whole reason this is owed is that ds-018 is a live case of *DOM correct, screen wrong*
>    on this very component.
>    **(b) ds-018, unchanged from its own entry:** `getComputedStyle` on the **disabled** Reset, snippet and
>    showroom, two widths; read the resolved value of **both** `--border-disabled` and `border-color`.
>    ⚠ **Do NOT hard-code a grey; do NOT tighten `:hover`** (already `:not(:disabled)`). If the token fails
>    to resolve, this is **instance five** of the silent-lookup class and the fix belongs in the generator
>    + a gate, not in `canon.css`.
> **1. ⛔ NOT A JOB — READ THIS BEFORE YOU PLAN ANYTHING ELSE ON THE DATAVIZ GROUP.** An earlier draft of
>    this handoff told you to "take the authorised transitional-block deletion". **It is already done**
>    (`ba336dc`); `_check_legend_migration.py` prints that todo list unconditionally at `:87–89` and
>    `dv-behaviour.js:146` is the tombstone. **Do not go looking for it.**
>    What is REAL: **`dv-legend.js` = 16330 / 16384 bytes (54 to spare); dataviz page budget 90%.**
>    **There is no cleanup left to buy headroom**, so **the next behaviour change to this group does not
>    fit.** The known fix is **Dave's call, not an enactment**: **per-member behaviour opt-in in the
>    registry** (schema change — same item `Chart-sparkline`'s inert 15.6KB payload waits on, §C·4).
>    ⇒ **If your plan touches dv-legend.js or dv-behaviour.js, price the schema question FIRST or you
>    will hit the ADR-0015 gate mid-job, exactly as session #7 did.**
> **2. ds-012 — (b) gutter-relative plot area.** ⚠ `cb2` is a **REVIEWED artefact**: every `x`/`width`
>    moves, so **attribute the diff with a control** or a correct change reads as a regression. Needs a
>    **floor** so a long category can't eat the plot at narrow widths — that floor is Dave's eye.
> **3. DV-D16 — concurrent "floating" growth. ⚠ RE-PRICE IT YOURSELF FIRST.** Session #7 measured it down
>    from ~30% to ~19% (concurrency already exists; only *floating* + *per-segment curves* are missing —
>    `Chart-bar.reference.html:121–128`, full detail in the ledger). **That is a downward re-price, which is
>    the direction nobody double-checks — re-derive it, do not inherit it.** Build wording ②, not ①. Must
>    animate **DV-D14's ENACTED heights**. **`prefers-reduced-motion` ships with it** — and the donut's
>    baked answer at `Chart-donut.reference.html:901–906` is the model (land on the final frame; **reduced
>    ≠ shortened**).
> ⚠ **THE ACCEPTANCE TEST IS A RENDER IN THE LICENSED CUT**, both widths, snippet AND showroom pane,
> `document.fonts.check(...)` asserted first. A fallback-face render passes while broken — that is precisely
> how ds-012 survived review. **Every proof ships with a bite proving it can FAIL.**
> ★ **The `DVLEGEND` env override added in #7 is the cheap way to do that for anything touching the legend:**
> point either suite at a neutered copy instead of mutating canon. Worked example + the published limit
> (the donut suite cannot see an all-on regression) in the ledger's DV-D17 ENACTED block.
>
> **★★★ FOUR OF THE FIVE CALLS ARE RULED (Dave, 2026-07-27 #4). What's left is small and named.**
> ✅ **(1) instrument fit = its own generated register sitting ON TOP of ADR-0016** — BUILT.
> ✅ **(2) adoption-time vs sweep = COMPLEMENTARY** — *"You're right about 2 they are complimentary"*.
>    Held shape, **not yet built**: adoption-time forcing function + a sweep **narrowed to one job,
>    finding undeclared adoptions** (`_FUTURE-STATE.md` § **Exploration beat 2**).
> ✅ **(3) the 465-rule pass** — BUILT, RUN, WIRED advisory (steps 58+59). See ★ LATEST.
> ⬛ **(4) the consult's enforcement column — NOT RULED.** Dave: *"I lean fix, but this probably needs
>    a discussion."* **Have the discussion before touching it.** ⚠ Its `5/5 shown` denominator fix is
>    separable and trivial and was **NOT** done — it is in §C·4, do it regardless.
> ⬛ **(5) `CTRL` vocabulary sweep in `_validate_a11y.py` — RULED YES, NOT STARTED.** 1,869 selectors
>    skip today. The `dv-vocab` pattern (normalise once + **fail loud on unknown**, never enumerate)
>    applies directly and is already ratified. **This is the cheapest ruled work on the board.**
>
> **★★★ NEW AND UNRULED — `ds-016`, and it is the same class one level up.** 7 live gates cite rules
> the index cannot see (698 anchors declared · 465 indexed · **265 invisible**), including **`aid-009`**,
> the ruling `_validate_a11y.py` names 5×. Three candidate remedies in `_DS-IMPROVEMENTS.md`:
> **(a)** fail loud when a gate cites an unindexed rule · **(b)** tag the 7 · **(c)** both — which is
> exactly the adoption+sweep pair he just ruled complementary, applied to itself.
> ⚠ **Do NOT bulk-add destiny tags to clear the list** — a destiny tag is an enforcement decision and
> belongs to Dave (derivation governance). ⚠ **`aid-009` is RULED AND IN FORCE** — its absence from the
> index is a retrieval failure, not a lapsed ruling.
> **Also open:** **279 of 465 rules are UNTAGGED** by the new pass ⇒ **12 under-instrumented is a FLOOR,
> not an answer.** Whether to invest in the pattern table is Dave's call; the number is published so it
> is made on evidence.
>
> **★★★ IF HE RULES "GO" ON #3 — the method is now demonstrated THREE times.** ADR-0016 P2 exemplars:
> `knowledge/_sweep_type_enactment.py` (corpus sweep) · `knowledge/_verify_dv_stacked_enactment.py`
> (**the better model** — ruled value vs RENDERED value across snippet × showroom × two widths).
> ⚠ **Every proof ships with a bite proving the proof can FAIL.** Non-negotiable; it has caught a real
> defect **five sessions running.**
> **Register reads PROVEN 4 · CLAIMED 20 · UNPROVEN 54 of 78** *(re-read the generated file, do not trust
> this line — it moved twice today as rulings were harvested).* **Target CLAIMED first** — an UNPROVEN row
> is honest about being unchecked; a CLAIMED row lies.
>
> **★★ STILL OWED, unchanged and NOT superseded:**
> **(i) The showroom type sweep + the 49-pane eyeball** — `_sweep_type_enactment.py` ran once: **800
> composite-bound elements, 22 deviations in 27 panes**, pattern is **WEIGHT not size**
> (`knowledge/_type-sweep-2026-07-27.json`). ⚠ Needs `--allow-file-access-from-files` or it reads ZERO and
> reports a cheerful "0 deviations". **Fold into the register as a P2 proof, don't re-run as a one-off.**
> **(ii) §C·2's RULING BATCH (15 + 17–22)** — unmoved for days, gates §C·1(c). **Fable is the model.**
> **(iii) The hit-area rule + gate** — read `notes/_briefs/2026-07-25-hit-area-rule-and-gate-proposal.md`
> FIRST. ⚠ **This is no longer a backlog item: ds-015 proves it is the NAMED RECEIVER for an exemption
> that is already shipping in 7 components.** The diamond's counter-rotation is the live case — a
> markup-driven gate must understand transforms, and a static one cannot.
> **(iv) Radius/corner tuner (§C·1d)** — v1+v2 BUILT + render-verified; owed = TWEAKS + ruling the numbers
> with Dave ("return soon, don't let me forget"). **Do NOT rebuild from scratch.**
> **(v) `showroom/chart-bar.html` cb5 rendered but UNSEEN by Dave** — 2.0–2.6% segment understatement,
> ink→white key flip, and **series-3 sits at 4.61:1, 0.11 over AA** (constrains any re-tune of that hue).
> **(vi) ds-014 (d) — donut cluster alignment, PARKED on his ruling** (`.dv-donut-row` is `flex-start`;
> −114px at 600 → −534px at 1440). Logged not fixed, deliberately — rule it where he can see it live.
> *(Carried up by the 2c EXIT CHECK so banner compaction can't lose it.)*
>
> **MODEL + EFFORT (Dave ruled 2026-07-26, still current):** conductor = **Opus 5, effort MAX** ·
> mechanical lanes = **Sonnet** · **Fable reserved** for open-judgment (the ruling batch · the hit-area
> gate). P2 is **script-then-judge**: any model writes a proof; **every deviation it finds is Dave's call.**
>
> **★★★ THE GAUGE IS A THROTTLE NOW — this supersedes every earlier pre-flight paragraph. READ
> `_RUNBOOK-context-gauge.md` § ★ Half 0b BEFORE PRICING ANYTHING.** *(The three-term rule alone is
> NOT current guidance — it was inscribed and then failed to stop a +17 overrun the same day.)*
> **`fill + job + WRAP (~5%) = projected band`** *plus* **a RING-FENCED ~15% reserve you may not spend
> without asking.** **Every job is priced and debited** (the ~10% floor is gone), stated out loud when it
> could move the band. **Any unplanned finding ⇒ STOP, re-price, put the fork to Dave** — log-and-stop /
> narrow / chase knowingly. **Never economise on READING the band table** (a wrong band twice, costs a `grep`).
> **★ AND CHECK THE PACE, which sets the posture:** the weekly allowance is **PERISHABLE**
> *(status: `inferred` ~75%, from the plan panel — see the runbook's provenance note)*. **At 2026-07-27 it
> was 0.65× pro-rata, Fable 0.55×.** ⇒ **Behind pace = MORE WINDOWS, not longer ones**; hoarding wastes
> allowance exactly as Red does. **Ask Dave for the current panel reading — no gate can see it.**
>
> **★★★ NEW AND UNRULED — `ds-017`.** A FLOATED item that **supersedes a standing instruction** has no
> path into this file; the EXIT CHECK only carries §C·4 items *up*. It cost the start of session #5, and
> the mechanism that hid it is still live. 3 remedies in `_DS-IMPROVEMENTS.md`: **(a)** wrap-gate check
> **(b)** ritual clause **(c)** both. ⚠ **A FLOATED item is not authority** — make the contradiction
> visible, never auto-promote the newer text.
>
> **⚠ THE LESSON THIS SESSION EARNED: the recommendation went through the CONSULT first, unprompted, and
> that is the whole remedy from this morning's arc working.** Cheap, and it is what stopped a second wrong
> recommendation. *(Full arc: `_DECISION-HISTORY/2026-07-27-the-instrument-cannot-see-the-property.md`.)*
>
> *Standing: every handoff carries both names (top) + a DIVVY PLAN. Known potholes all still true: the
> installer's non-zero exit is HOST-VALIDATION not download refusal (**check the cache, proceed**) ·
> `/tmp` NOT writable (use the outputs mount) · FONTCONFIG two-alias block required · **render the SNIPPET
> for canon truth and the SHOWROOM PAGE for what Dave looks at**, and the showroom's panes are `srcdoc`
> IFRAMES — query `page.frames`, not the top document. **Assume your probe is wrong in the direction that
> reads as green** (four sessions running).*

*Read: **§A Orientation** (skip if you're in context) → **§B This session** → **§C Queue**.
Then `_LIVE-STATE.md` → the decision files it points to.*

---

# §A · ORIENTATION — the whole project in one page

> **Why this file is called GOOD-MORNING** *(Dave's framing — keep it, it explains the architecture)*
> **Memento.** Leonard has anterograde amnesia: every morning he reconstitutes himself from a record he
> built when he still remembered — Polaroids for working state, **tattoos for the facts he cannot afford
> to lose**. That is this project's operating model, not a metaphor for it. A session starts with no
> memory and rebuilds from artefacts.
>
> **The trust hierarchy is the tattoo/Polaroid distinction:** repo rules + runbooks + ledgers = tattoos
> (durable, survive any single rewrite) · `GOOD-MORNING` + `_LIVE-STATE` = Polaroids (working state,
> rewritten often) · the chat = gone by morning. **Never let a durable rule live only on a Polaroid.**
> *(Live example, 2026-07-22: this file said the tabs ruling was "NOT yet inscribed" — the ledger already
> carried R-D23 AND R-D24. The ledger was right. Read the ledger.)*
>
> **The real danger is not forgetting — it is confident false inscription.** Records carry provenance
> and confidence, not just content. Corrections get inscribed as loudly as the original claim. **Mark
> what was OBSERVED versus what was INFERRED.** The ritual stamps dates from `date`, never from belief.
> *(2026-07-22 afternoon instance: B-D7 was ruled in TWO beats — "shared 4%", reversed within the hour
> to pixel-true. BOTH are in the ledger, so the reversal can never read as agent drift.)*
>
> **The SECOND failure mode costs more: a stale READING of our own rules.** ⇒ **Before designing anything,
> CONSULT: `python3 knowledge/_consult.py "<what you're about to design>"`** (rules · rulings · assertions ·
> gates + where each bites). Runbook: `knowledge/_RUNBOOK-consult.md`. *(ds-009 CLOSED 2026-07-22: the
> corpus is now DISCOVERED — every `_proforma/_*-DECISIONS.md` indexes or the build fails.)*

> **STANDING SECTION — carry it into every handoff, from 2026-07-17 on.** At Dave's request:
> *"orientate a new starter — wider context helps."* New-starter style: assume the reader has no context.
> **Update it when the shape of the project changes, not every session — but never drop it, and never
> shorten it to a label.** *(Also step 2 of `_RUNBOOK-capture-ritual.md`; reachability-gated by
> `_validate_standing_instructions.py`.)*

## What Apollo is
A **governed design-system engine** for agentic UI generation. The bet: *generation is a commodity* — the value
is the layer around any generator. Two principles run through everything:
- **Retrieval, not recall.** Brand values are retrieved from token stores, so generated work can't drift off-brand.
  **Since ADR-0013 (built 2026-07-22) retrieval reaches RULES too:** organisms consume atoms' rule-blocks
  as generated partials — never re-type a sub-atom.
- **Verification = enforcement.** Judgment is encoded as **blocking gates**; "done" is withheld until they pass.
  If a rule isn't gated, assume it will be broken.

Tagline: **"lovable on rails."** Four phases: **Discover** → **Create** (what's being built now) → **Craft**
(the review-overlay docs ARE this) → **Dispatch**.

## ★ ONE token store · ONE baseline library · FOUR themes (R-D15 → ADR-0011 → ADR-0014 → ★ ADR-0013)
*Themes are **override sets at the semantic tier**; since ADR-0014 they carry **their own neutral primitive
ramps** through the **neutral DNA tier** (semantic roles alias `color/neutral/1–15`, never `color/mono/*`
directly; indices are SEMANTIC POSITIONS — SC remaps its anchor). **State mechanism is a THEME PROPERTY**
(registry `stateMechanism` + blocking snap gate). **★ Since ADR-0013, MOTION is a theme dial too (B-D7):**
`motion/press/{travel,darken}` — Mono carries the movement (pixel-true 2px), **Console inherits it**,
**Legacy + Supercharge zero it** (colour-only state feedback); tuning = a token edit, zero JS.
**Sibling pairs:** {Mono, Console} share neutrals/opacity/status/dataviz — Console FENCED (colour;
motion is inherited-not-fenced, flag if it should join); {Legacy, Supercharge} = structural siblings.*
The four themes (Dave's canonical order):
- **Apollo Legacy** — faithful reproduction of the existing HSBC system: brand red `#DB0011`, teals,
  `color/grey/*`. **AA-EXEMPT as-built (R-D24)**; explicit per-path overrides, no DNA tier, **no press movement**.
- **★ Apollo Mono** — the baseline we build NOW. "Very mono": colour ONLY in RAG status + dataviz.
  Neutral scale = `color/mono/1–15`; only red `#B92F1E` (status/RAG/dataviz). Carries the B-D7 press physics.
- **Apollo Console** — branded HSBC library. **LOCKED ≡ Mono** on neutrals/opacity/status/dataviz (fence);
  inherits Mono's motion; live divergence = rounded corners (radius overrides, values provisional).
- **Apollo Supercharge** — brand-uplift. **OWN warm ramp** `color/warm/1–15` (OBSERVED, Figma pull);
  states = COLOUR; **no press movement**; dark mode = provisional-agent, awaiting Dave.

## Where things live
```
knowledge/            THE ENGINE
  tokens/             DTCG token stores — the retrieval source
    colour.json       primitives: mono/1-15 · neutral/1-15 (DNA tier) · warm/1-15 (SC) · grey/* (Legacy)
    semantic-colour.json  roles alias color/neutral/* + rag/* + component tiers + $extensions.apollo.state
    motion.json       durations · easings · ★ press/{travel,darken} (B-D7 — the theme-dialable physics)
    themes/           the four override sets + _themes.json registry (stateMechanism · neutralRamp ·
                      siblingPairs · console fencedPaths · ★ Legacy/SC motion kills)
  ★ component-types.json  THE ADR-0013 REGISTRY — one file, both halves: component-type/<group>/<param>
                      tokens ($alias→semantic + cached $value) + $members (selector map) + $partials
                      (source atom · rootSelector · requires/matchValues/declarations · $manifestBinds)
  snippets/           64 gated reference components = CANON (40 + Phase-2's 24). Atoms carry
                      PARTIAL blocks; consumers carry generated AUTO-PARTIAL blocks (provenance-
                      commented, sync-gated). Multi-control members = :is() selector lists (wave-1
                      convention); mixed sizes = local --phys-size override
  ★ gen_component_partials.py  injects partials into consumers; --check = build gate; selftest 8 bites
  ★ _validate_partials.py      the re-implementation RATCHET (strict on members · census = accretion
                      worklist) → _PARTIALS-GATE.md
  canon/              canon.css (token spine · components · AUTO-THEMES cascade) + type.css (HAND-AUTHORED)
                      + generators (gen_canon_tokens · gen_theme_cascade · ★ gen_canon_components — now
                      IN the build: regenerate-always + determinism --check, ADR-0013 ruling 4)
  guidelines/         the rules, each {#id} + destiny tag; _rules-index.json (generated)
  _proforma/          Apollo Mono tranches T1–T9 + the decisions ledgers (near-canonical per ruling 3)
  _consult.py         "what governs X?" — RUN IT before designing (corpus now DISCOVERED, ds-009 closed)
  _validate_*.py      the gates — incl. _validate_state_snap.py (ADR-0014) + ★ _validate_partials.py
  gen_showroom.py     generates showroom/ — never hand-edit showroom
showroom/             THE LIBRARY, browsable: 64 harness pages + index w/ live count (#theme=… all four)
reviews/              review sheets — ★ AWAITING DAVE: SC-DARK-MODE-2026-07-22-v1(.REVIEW).html
notes/_receipts/      worker-receipt dir · notes/_briefs/ conductor briefs
_LIVE-STATE.md        LIVE / DEAD / OPEN / TARGETS — read second, always
_GM-ARCHIVE.md        rolled-off GOOD-MORNING banners (verbatim, newest-first) — compaction, step 2c
_FUTURE-STATE.md      side-quests, ideas, RESURRECTION candidates
_DECISION-HISTORY/    dated narrative — ★ 2026-07-22: the ADR-0014 arc AND the ADR-0013/B-D7 arc
```

## The one command that matters
```
python3 knowledge/_build_all.py     # ★ the blocking build — it prints its own [i/N] step count;
                                    #   exits non-zero on any failure (count not hardcoded here: it rots — P4, 2026-07-26)
```

## Rules that actually bite (core + this session's)
- **CONSULT before designing** — then **survey before build**. *(This session the survey found Icon-button's
  physics was a REVIEWED refinement, not drift — which became B-D7.)*
- **★ ADR-0013 (BUILT): never re-type a sub-atom.** A registered partial's rule may exist ONLY in the
  atom's PARTIAL block or a generated AUTO-PARTIAL block — the ratchet gate blocks members' local
  re-implementations; the census lists everyone else's (accrete from OBSERVED duplication, ruling 3).
  Joining a family = markers + required vars + manifest binds + registry entry, and the generator
  fails loud on any missing piece.
- **★ B-D7: press physics is pixel-true and theme-dialable.** Travel/darken are TOKENS
  (`motion/press/*` → group caches); `--phys-size` is LOCAL geometry (buttons 120, icon 44); Legacy/SC
  zero the dial. **No JS in physics — ever** (Dave's constraint; DEF-003 posture). Tuning = token edit.
- **ADR-0014: semantic neutrals alias `color/neutral/*`, NEVER `color/mono/*` directly** · whites are
  classified (substrate → `neutral/15`; absolute → `color/white`, pinned).
- **ADR-0014: opacity states must SNAP** (`_validate_state_snap.py`, blocking, 7 checks incl. the
  text-state AA floor — inactive ≠ disabled).
- **Selftests are BUILD STEPS** — every new gate ships one AND wires it (partials + ratchet did).
- **Resurrect-verbatim is NOT gate-exempt** — the 273d18c~1 stepper's 13px/3px hit the grid gate on
  re-entry; corrected 12px/4px. Old reviewed artefacts re-enter through the same door as new work.
- **Grey-tint standing check** · **type26-013 (BLOCKING): white type is red-only** · **R-D6 glyph
  contrast by ROLE** · **`LEGACY_THEME_EXEMPTIONS`** (R-D24 — EXEMPTED, never passed).
- **canon.css** — generated only between AUTO markers; type.css HAND-AUTHORED. *(The ruling-4 gap is
  CLOSED: snippet RULE-text now self-heals into canon every build.)*
- **Every selector appended to `canon/type.css` is GLOBAL** — register in `_type-bindings.json` or the
  blast-radius gate fails.
- **Icons: real assets only** · **4px grid** · **sentence case** · **square corners in Mono** (radius =
  ROLE tokens, per-theme) · **weights: 100/300/400/500/700 only, NO 600.**
- **Derivation governance** — the engine never derives-and-promotes. **Promotion is Dave's alone.**
  *(SC dark values agent-derived → AWAIT him; B-D7's enacted values are HIS ruling, verbatim-quoted.)*
- **Spine discipline** — state lines in `_LIVE-STATE`; narrative >10 lines → `_DECISION-HISTORY/`.
- **Inscription prose is PARSER-VISIBLE** — no node names in ADR-header parentheticals (phantom edges).

## Standing instructions for the agent
- **Announce the model/routing split at the START of every substantive task** (`MODEL-ROUTING.md`).
- **Surface the chat names at BOTH ends — the small reliable thing Dave leans on, and it gets dropped
  (Dave flagged 2026-07-25).** At session START, offer the last handoff's "TITLE THE NEXT CHAT" as a
  ready-to-paste **"Rename this chat: …"**; at WRAP, put BOTH names at the top of `GOOD-MORNING.md`
  (ritual step 4b). Claude cannot rename chats itself — a name left unsurfaced is a label lost.
- **Verify before asking** (read repo / run gates) — including your own flags. **Reflect back before
  recording** a ruling — and when a ruling REVERSES, inscribe both beats (B-D7 is the model).
- **Decision-heavy / material-referring choices ship as review HTML** (`knowledge/_review/_make_review.py`
  — NOT at knowledge/ root). Architecture calls = the ADR-0012/0013/0014 model: options + firm
  recommendations in-chat, Dave rules by number, inscribe same hour, **feed the graph seed same hour**.
- **Surface spin-off candidates**; register ideas in `_FUTURE-STATE.md`. **Run the capture ritual
  unasked**; **stamp dates from `date`**. **Memory accelerates; the repo is the record.**
- **Stamp the context-gauge reading on every handoff artefact** — creator in `GOOD-MORNING` commit-state,
  workers in their receipt header — as a SCRUTINY indicator on that artefact (Red-authored ⇒ next reader
  re-verifies before trusting; not a quality score). Canon: `_RUNBOOK-context-gauge.md` § authoring-time stamp.

## The other standing documents (REACHABILITY-GATED by `_validate_standing_instructions.py` STAND-002 — keep every one referenced here)
`_STANDARDS.md` (★ the standards hub) · `AGENTS.md` · `MODEL-ROUTING.md` · `_FUTURE-STATE.md` · `_DECISION-HISTORY/README.md` ·
`knowledge/_proforma/_PROFORMA-RULES.md` · `knowledge/_proforma/_TYPE-DECISIONS.md` (T-D1…T-D14) ·
`knowledge/_proforma/_RAG-DECISIONS.md` (R-D1…R-D25) ·
`knowledge/_STYLE-PROVENANCE.md` · `knowledge/_proforma/_DATAVIZ-DECISIONS.md` ·
`docs/decisions/ADR-0012-decision-graph-edge-convention.md` (seed `notes/_decision-graph-seed-2026-07-21.json` —
★ 124/124 zero mismatch after B-D7; feed it EVERY inscription, or `--verify` drifts silent) ·
`docs/decisions/ADR-0013-component-type-tier-composition.md` (★ BUILT 2026-07-22 — Consequences updated) ·
`docs/decisions/ADR-0014-per-theme-neutral-primitives-state-snap.md` ·
`knowledge/_proforma/_BUTTON-DECISIONS.md` (B-D1…★ **B-D7**; in the CONSULT corpus since ds-009 closed) ·
`docs/decisions/ADR-0009-state-styling-architecture.md` · `docs/decisions/ADR-0010-token-schema-nullable-flex-slots.md` · `docs/decisions/ADR-0011-four-theme-token-architecture.md` ·
`knowledge/_DS-IMPROVEMENTS.md` (ds-007 open · ds-008 ✅ · ds-009 ✅) · `knowledge/_ICON-GAPS.md` · `knowledge/_ASSERTIONS.md` +
`knowledge/_assertions.json` · `knowledge/guidelines/_rules-index.json` · ★ `knowledge/component-types.json` (the ADR-0013 registry) ·
`knowledge/_PARTIALS-GATE.md` (the ratchet report — census = Phase-2's accretion worklist). **Runbooks** indexed by `knowledge/_RUNBOOKS.md`.
*(This list was dropped in a rewrite once and STAND-002 red-flagged it — do not prune it.)*

## Parallel-session model (PROVEN 2026-07-21)
On "read good morning", role is picked (Worker / Conductor / Solo) — **from Dave's opener line ONLY;
titles are labels.** ONE conductor = single writer for shared state; workers emit receipts to
`notes/_receipts/`, no git. Conductor reconciles the shared tree before committing (never blind
`git add -A` with workers live). Every handoff carries a **DIVVY PLAN**. Workers can absorb live Dave
rulings mid-flight — receipt verbatim.

## Renders — REAL FONT, in-sandbox
**→ `knowledge/_RUNBOOK-render-verify.md` (stood up 2026-07-23, Dave's ask) — read it, don't
reconstruct.** Pipeline VERIFIED WORKING 2026-07-23: headless-shell download + libs + real-HSBC-cut
render all green (the 07-22 "download refused" reads as the installer's EXPECTED host-validation
exit — the runbook explains). Render-verify for ADR-0014 + ADR-0013 is now UNBLOCKED, still OWED
until actually run + seen. HTML is what Dave reviews; PNGs are agent self-verification only.

## How we work
- **Review loop:** every doc ships **clean source + REVIEW copy** (`knowledge/_review/_make_review.py <file>`).
- **Live tuners beat static versions past ~2 colour round-trips.** Sheets read canon.css LIVE, never retype.
- **Dave commits via GitHub Desktop.** Claude commits in-sandbox per `_RUNBOOK-git-commit.md` — run it,
  don't improvise. `unable to unlink … *.lock` warnings = the delete-guard, not failure; judge by HEAD.
- **Comms:** exec summary + numbered next steps first, detail below.

---

# §B · THIS SESSION

> ⚠ **STALE BELOW — do not read it as current (2026-07-27, later morning #3).** The three most recent
> sessions are summarised only in the ★ LATEST + ★ PRIOR banners at the top of this file, which are
> authoritative. This section still narrates the 07-26 lane ① window. **The narratives you actually
> want:** this session → `_DECISION-HISTORY/2026-07-27-the-instrument-cannot-see-the-property.md`
> (the KG exploration arc: the consult's two defects, Dave's two reframes, why held angle (1) would have
> missed `aid-009`, and the three-term pre-flight) · prior → `_DECISION-HISTORY/2026-07-27-the-gate-that-narrowed-its-own-rule.md`
> (the full arc: why the recommendation was wrong, the gate-narrowed-its-own-rule finding, the forked
> vocabulary, the third silent-fallback, and the probe repeating the wrong-document error) · rulings →
> `knowledge/_proforma/_DATAVIZ-DECISIONS.md` **DV-D14 + DV-D15** · defect record →
> `knowledge/_DS-IMPROVEMENTS.md` ds-014 (ENACTED block) · the register build →
> `docs/decisions/ADR-0016-enactment-proof-register.md`. Rewriting §B was again deliberately not
> attempted — the banner + DO-FIRST + the dossier carry the session, and a hot rewrite of a long
> narrative section is exactly what produced 07-26's three corrections.

> ⓘ Most recent = **legend wave lane ①** (2026-07-26 evening, Opus 5 solo self-conducting, effort MAX).
> The ★ LATEST banner is its summary; the narrative WHY/HOW — why the re-verify mattered more than the
> lane, the correction to my own correction on the grep, the two non-obvious calls the divvy didn't
> name — is `_DECISION-HISTORY/2026-07-26-legend-wave-lane-1-and-three-record-corrections.md`.
> **Evidence per claim** (`<source> · <date>`): build `_build_all.py` 55/55 GREEN · 2026-07-26 ·
> members `node knowledge/_verify_dv_legend_members.js` 54/54 · 2026-07-26 · exemplar
> `node knowledge/_verify_dv_legend.js` 27/27 · 2026-07-26 · migration state
> `python3 knowledge/_check_legend_migration.py` → donut ✅ bar ✅, combo + line remain · 2026-07-26 ·
> ds-010 closure = computed-fill read at 1180 + 760 in the licensed cut, font assert passed ·
> 2026-07-26 · ds-012 = per-label `getBBox()`, 6 of 6 clipped, worst 16.8px · 2026-07-26 ·
> byte figures = `knowledge/_BEHAVIOUR-GATE.md` + `wc -c` · 2026-07-26 · commit `aabe617`.
> **What I got wrong:** my first framing said a grep "cannot" discriminate the migration state —
> building the replacement disproved it (`data-series-toggle="` works today, on punctuation luck).
> Corrected in the script's docstring, the dv-behaviour comment, the dossier and the banner.
> The two older narratives below are retained for context.
>
> ⓘ (prior) the **bar-audit → CONDUCTOR window** (the
> narrative WHY lives in `_DECISION-HISTORY/2026-07-23-bar-audit-and-conductor-absorbs.md` — audit
> method, the contaminated-Q8-framing lesson, the base64-payload iframe borrow, the rulings arc,
> the two-lane reconcile incl. the `a2acc9e` mid-conduct note). Evidence per claim: audit sheet
> `reviews/BAR-CHART-AUDIT-2026-07-23-v1.REVIEW.html` (rendered 1400+840) · ledger DV-D08/09 +
> seed 76/130 (`f887efd`) · sidequest receipt + its commit (`db1ed1b`) · builds 51/51 at baseline
> AND post-inscription. The detailed narrative below is the **PRIOR Phase-2 waves** session,
> retained for context.

## (prior) 2026-07-22 evening — "Phase-2, BOTH waves: one conductor, five worker windows"

*The record lives in the receipts (5 worker + 2 conductor-reconcile, `notes/_receipts/2026-07-22-
phase2-*`) — no separate dossier; the receipts ARE the narrative, judgment calls included.*

- **✅ 24 components in one day** (W1: A-forms 4 + B-feedback 10 · W2: A-continuation 5 — **forms
  brief COMPLETE 9/9** — + C Data-grid + D Charts 4). Library 40→64, registry 4→18 members,
  radius 45-strict, **census 32→32 across everything**, 51/51 green at every reconcile. Firsts:
  calendar panel (Date-picker, composed from surveyed parts) · determinate progress bar
  (File-upload, ink-on-neutral) · Charts = the parked kit PROMOTED (provisional-agent, sign-off
  yours). Conventions minted: `:is()` multi-control members · local `--phys-size` on mixed sizes ·
  `proforma-promotion` provenance class · dataviz gate wired to chart snippets (new-surface rule).
- **✅ The protocol COMPOUNDS:** wave-1 absorb completed 7 lanes' contracts by hand (they fire only
  on registration — fails-loud proven); wave-2 workers READ that lesson and pre-landed contracts →
  both wave-2 absorbs injected clean first try. Fences held all day; A's wave-2 breach flag =
  misread of MY mid-wave absorb of C (resolved + inscribed in the wave-2 reconcile receipt —
  the name-every-path reflex worked, the inference didn't).
- **✅ Dave's in-flight asks handled by the hot-clause:** showroom header count SHIPPED (live 64) ·
  card thumbnails NOTED (`_FUTURE-STATE`, `#bare`-mode shape) · theme "outage" diagnosed as
  wrong-file + payload-is-base64 (pages were correct; Legacy's small delta on data components =
  architecture, not bug).
- **🐛 Wrong/caught:** Drawer close 44→36 (file beat receipt) · my pkill self-match (twice-class,
  receipted for the runbook) · one stale-cascade red per wave (my own serial edits, regen healed).
  **Owed:** render-verify (headless-shell, standing).

---

# §C · QUEUE

## 1. ★ NEXT STRANDS (pick one per window; role from the opener line)
**(a) ★ CHART-EXPANSION PROGRAMME — prove-one-then-wave (Dave ruled 2026-07-22, this session).**
**STEP 1 (next window, solo — DO THIS FIRST):** build the **scatter** exemplar END-TO-END — proforma
section in `_proforma/DataViz-interactive.html` (DV-D01) + promoted `snippets/Chart-scatter.reference.html`
(composites-only type, role-token radius, dataviz tokens, controls toolbar + legend + `<table>` spine) +
its `.meta` + registration (`MIGRATED_SNIPPETS` radius-strict · `CATEGORIES` "Charts") + regen
cascade+showroom → build green (dataviz gate globs `Chart-*` automatically). Hand to Dave to eyeball the
LOCK-UP before fanning out. **STEP 2 (wave) — DIVVY PLAN, the other 8 as fenced worker lanes** (NEW snippet
files + receipts only, no git): **lane 1** butterfly-h + butterfly-v + histogram (bar-family geometry) ·
**lane 2** box plot + bullet + candlestick (statistical/gauge; candlestick up/down = `data/delta/gain·loss`) ·
**lane 3** pie (donut-family, dv-pie-009 ≤6, D-Q2 labelling) + stacked area (line-family) + **promote**
grouped/stacked bars (D-Q3). Conductor = serial set (registry · MIGRATED_SNIPPETS · CATEGORIES · spine ·
ONE commit). **Heatmap NOT in scope — parked** (`_FUTURE-STATE` ★). Model: Sonnet/Fable workers, Opus conducts.
**(b) Wave 3 fan-out (component library)** — ~26 itinerary gaps remain (`reviews/ITINERARY-2026-07-14…`);
conductor surveys + cuts lane briefs (wave-1/2 = the pattern; candidates: navigation/menu family + P2 depth).
Serial set as always (registry · MIGRATED_SNIPPETS · CATEGORIES · spine · git = conductor only, ONE commit).
**(c) Templates+shells clean-room (Layer-2, the load-bearing gap)** — solo Fable ADR-style session.
Best AFTER the ruling batch: field-family, stepper-fold and delta-seam answers shape it.
**(d) Enact window (cheap)** — absorb §C·2 rulings as token/registry edits + §C·4; new candidates: mint
`data/axis`+`data/grid` (per ★ DV-D07 two-channel) · R-D9 ramp promotion · field-family group build if ruled ·
Stat-card `spark` slot · **★★ the live radius/corner tuner (Dave: return SOON).**
**(e) ★ ROUTING SIDE-QUEST — ✅ DONE + RATIFIED SAME DAY (2026-07-23 evening).** All 13 proposals
RATIFIED by Dave and #6–12 ENACTED in-session (his override): sheet
`reviews/ROUTING-AUDIT-2026-07-23-v1.REVIEW.html` · receipt
`notes/_receipts/2026-07-23-routing-sidequest-audit.md` (ruling verbatim). **#12 SUPERSEDES the
07-13 Mode-2 default-on** (delegation now DELIBERATE; MODEL-ROUTING tombstoned, memory hooks
updated). #13 = the calm-banner trial riding THIS handoff's top — Dave judges by eye. Residue in
§C·4: none owed beyond the trial verdict.

## 2. ★ DAVE: THE RULING BATCH — 15 REMAIN of 16 (D-Q3 = #14 RULED 2026-07-23, promote in the
wave; Q8/B2 also RESOLVED → DV-D08) + the ★ DATAVIZ SIGN-OFF (rule by number; all retro-propagate). **The sign-off first:** D promoted the PARKED kit verbatim into
Chart-bar/line/donut/sparkline — your review flips them provisional-agent→canon (open-014).
**★★ NEW 2026-07-27 (session #6) — DAVE'S THREE CHART FLAGS. CAPTURED, NOT ENACTED, EACH OWES A READ-BACK.**
*"I want to make changes to the charts too, I've noticed a couple of missed decisions, please note this."*
Filed the same minute — `knowledge/_proforma/_DATAVIZ-DECISIONS.md` **§ Batch 10** (verbatim quotes +
source-read current behaviour + the read-back questions) and `knowledge/_DS-IMPROVEMENTS.md` **§ ds-018** —
per **ds-017**, so none of it lives only in a chat that is gone by morning.
**23. ✅ DV-D16 RULED · stacked animates SEQUENTIALLY FROM THE BOTTOM, SEGMENT BY SEGMENT, on EVERY STACKED
SURFACE** — *"same as the pie, ease-in for the first, ease-out for the last, and linear for everything in
between."* ⚠ **"Every stacked surface" is TODAY A SET OF ONE** (measured: `stacked` ×12 in Chart-bar, ×0 in
combo/line; stacked area unbuilt) ⇒ **the ruling is FORWARD-BINDING — carry it into the chart-expansion brief
(§C·1a lane 3 + the D-Q3 promotion)** or the next wave ships stacked surfaces that don't animate.
⚠ Must animate **DV-D14's enacted heights**, not true heights. ⚠ **STILL OPEN:** does the donut actually
sequence today (**verify, don't ask**) · fixed per-segment duration vs fixed total (serial cost scales with N,
and stacks have no `dv-pie-009`-style ≤6 cap) · **`prefers-reduced-motion` is NOT optional — it ships with the
first enactment** (ADR-0004 / WCAG 2.2 AA).
**24. ✅ DV-D17 RULED · RELEASE ISOLATION ENTIRELY on the second check-on** — *"the isolated key item stays
active when I check others on."* Cause read from source: `dv-legend.js:114/119/129` keeps `st.isolated` pinned
while `st.focus` grows, so `.is-solo` survives. Fix = `st.isolated = null`. **Accepted cost: no 2-of-5
comparison by isolate-then-add.** ⚠ **Three bites the enactment must not break:** restore to `visible[]` not
all-on (`:129`) · Reset must not self-disable while still filtered (`:122` — *same expression as ds-018, do not
conflate*) · `dv-sr` must announce release on the add path (`:140` only fires on re-click).
**25. ds-018 · Reset's DISABLED state renders as the HOVER state** — *"reset disabled style is set at the
hover style."* Disabled Reset paints an ink border; **B-D4 says disabled is visible-but-recessive.** Rules are
correct as authored (`:hover` is already `:not(:disabled)`) ⇒ **HYPOTHESIS: `--border-disabled` fails to
resolve → invalid-at-computed-value-time → `currentColor` = ink.** That would be **instance five** of the
silent-lookup class. ⚠ **A token-value bug looks identical — eliminate it by `getComputedStyle`, snippet AND
showroom, two widths. Do NOT hard-code a grey.** Gate candidate: *no control's disabled treatment may resolve
to its hover treatment.*
⚠ **All three are Dave-owned and NONE is render-verified. Answer the read-backs before building.**

**New this wave, 8–16:**
8. **(A-Q5)** Calendar day-cells + Stepper done-dots carry NO press physics (judged selection
   targets / structural markers, the Tabs class) — confirm, or extend the family.
9. **(A-Q6)** File-upload built the library's FIRST determinate progress bar (ink-on-neutral,
   R-D22 spirit) — accretion candidate when a second consumer appears.
10. **(A-Q7)** Stepper consumes Progress-tracker's visuals by copy — fold to one snippet, or
    accrete a stepper-visuals partial at a third consumer?
11. **(A-Q8)** Date-range = restart-on-earlier-pick (inscribed as reference behaviour) — flag if
    the HSBC source says swap-endpoints.
12. **(D-Q1)** Line markers: Background fill (promoted default, theme-adaptive) vs White — the
    kit toggle never ruled.
13. **(D-Q2)** Donut labelling default: spider vs direct; letters-on-segments HELD (white letters
    on series fills — type26-013).
14. ~~**(D-Q3)** Promote the kit's grouped/stacked bars next wave?~~ **✅ RULED 2026-07-23 (audit
    B1): PROMOTE, wave bar lane** — ledger line under DV-D09's block; the Batch-1 #3
    grouped-LAYOUT open (reference images) is separate and stays open.
15. **(D-Q4)** Status-watch amber light-mode = 3.02:1 vs page — the R-D3 graphic floor with zero
    margin. Comfortable for charts, or lift?
16. **(D-Q5)** TWO delta conventions now live (charts `data/delta/gain·loss` vs Stat-card's R-D5
    rag arrows) — one canon convention, or a deliberate chart/card split?

**17–22 — RESTORED from the rolled 07-24 chart-wave banner (dream-pass v2 P1, ruled 2026-07-26):
the banner's compaction to `_GM-ARCHIVE.md:32` carried these out of live state; copied back
verbatim-in-substance. Same ruling mechanics as 8–16.**
17. **Q2 combo home** — new snippet vs Chart-bar variant.
18. ~~**Sweep hook / 16KB cap fork** — amend cap vs modularise.~~ **✅ RULED 2026-07-26: SPLIT *and* RE-SCOPE** — `dv-legend.js` is a second source; 16KB stays per-source (legibility) and a **32KB per-GROUP PAGE budget** was added so a split can't buy headroom. Inscribed **ADR-0015 § Amendment**; the sweep is no longer baked-static (DV-D12 runs).
19. **COMBO-LINE-INVERT R-B/R-C** — R-A casing DAVE-SEEN-PROVISIONAL.
20. **Chart-scatter Layer-2** — deferred, stays Layer-1 safe.
21. **Brush/range-select spec** — menu 8, designed not built.
22. **JS-off seg wart** — shared w/ Chart-line, atom-level fix.

## 2b. WAVE-1 RULINGS 1–7 (unchanged, rule with the above)
1. **Form-label weight** — the `.t-cm-label` composite renders 400; gated Input-fields labels are
   16/500. Rule 400 (Input-fields migrates later) or mint a 500 form-label composite (one type.css
   line + binding).
2. **`input-error` null slot** — the ADR-0010 slot you anticipated is NOT declared; all four form
   components bind semantic `rag/error` directly. Declare the null slot?
3. **Toast dark glyphs** — coloured shapes on the ELEVATED NEUTRAL ground (all ≥3.55); the
   white-shape dark ruling was made on TINTED grounds. Confirm or extend.
4. **Modal family fold** — Modal-lightbox extends Modals as a separate snippet; fold into one
   modal-family snippet later, or keep split + a dialog-mechanics partial when a group accretes?
5. **Figure vouch** — figure-4/5/6 composites still "PREPARED, awaiting vouch"; vouching flips
   Amount-display candidate→canon + hardens Stat-card's value type.
6. **★ Field-family accretion** (ADR-0013 ruling 3, cross-lane OBSERVED duplication — the
   wave's standout): field chrome (hover fill · focus black border + 4px stroke · error stroke)
   now consumed by copy across ≥7 files (Input-fields, Dropdown, Search-field + A's four +
   Account-selector). Accrete `field-family` as registry group #2 next wave?
7. **Showroom Overlays split** — B proposes Overlays (Drawer/Popover/Lightbox/Modals/Tooltip) +
   Data-display buckets; wave 1 filed into existing buckets. Re-bucket?
   *(Minor, flag-if-wrong: conductor decided the mixed-size idiom = local `--phys-size` override,
   inscribed in the registry; Secure-entry holds figure-3/24 in its 40px narrow cells (A-Q3);
   fl-summary ≈ Alert filed to the dedup pass (A-Q4); linked Stat-card variant awaits the
   press/link posture question (B-Q6).)*

## 3. ★ THE STANDING EYEBALL SET (NON-BLOCKING — your "foundations first" ruling; pin-comments
now live in every showroom pane, so it's async)
**(a) B-D7 motion:** Button/Modals presses calm down · Progress-tracker scale press + dots↔line
collapse through 520px · Icon-button identical · `#theme=legacy`/`#theme=supercharge` = colour-only.
**(b)** SC dark sheet `reviews/SC-DARK-MODE-2026-07-22-v1.REVIEW.html` + 4 held whites + Console
radius px + bigplay. **(c) NEW from Phase-2:** all 24 new components across 4 themes × light/dark — the Charts 4 double
as the dataviz sign-off (§C·2).

## 4. Enact-queue (cheap, post-rulings)
**★ NEW 2026-07-27 #7 — carried here by the 2c EXIT CHECK so compaction cannot lose them:**
**DV-D17's render-verify in the licensed cut** (OWED — pair with ds-018, §DO-FIRST 0) · **the
`st.visible[id] = true` enactment call** (the agent's, UNRULED — one line to reverse; `_REVIEW-SIGNOFF.md`) ·
**the DV-D13 centre-figure consequence** (Dave's eye, live; `_REVIEW-SIGNOFF.md`) · **the dataviz behaviour CEILING** — 54 bytes free in `dv-legend.js`, group at 90%, **no cleanup left**;
the fix is the per-member opt-in SCHEMA question, Dave's (§DO-FIRST 1) · **`_verify_dv_legend*.js` both take a `DVLEGEND` override now** — use it to bite anything
touching the legend instead of mutating canon · ⚠ **the members suite is 108 checks, not the "54/54" the
record carried for two sessions** — a stale count in three places, same class as the migration miss.
**★ NEW 2026-07-27 #6 — THE ENACTMENT REGISTER CANNOT SEE A RULING WRITTEN IN A BLOCKQUOTE.** Found at
commit time: `_build_enactment_register.py` harvested **DV-D16 and DV-D17** from § Batch 10 (both
UNPROVEN, correct) and **silently missed DV-D18**, which sits inside a `>` block. Register now reads
**4 of 80**; the true denominator is 81. ⚠ **Do NOT fix this by reformatting DV-D18** — that hides the
finding and leaves the next blockquoted ruling just as invisible. **The defect is the SILENCE**: the
harvester should report ruling-shaped lines it declined to index, the same *fail-loud-on-unknown* shape
already ratified for `dv-vocab` and proposed for ds-016. **Same class as ds-010 · ds-013 · ds-016 ·
ds-018** — and I authored it **one hour after logging ds-018 for the same shape**, which is the honest
measure of how invisible this failure mode is from the inside.
**★ NEW 2026-07-27 (from exploration beat 1) — carried here by the 2c EXIT CHECK so compaction can't lose them:**
**consult `5/5 shown` denominator** — trivial, separable from the enforcement-column question, do it regardless ·
**`CTRL` vocabulary sweep** in `_validate_a11y.py` (`dv-vocab` pattern, 1,869 selectors skip today) ·
**ds-014 (d) donut cluster alignment** — PARKED on Dave, logged not fixed (`.dv-donut-row` `flex-start`) ·
**ds-015's exemption warnings** are advisory by design — they become the hit-area gate's worklist when it lands.
**★ NEW 2026-07-26 (from lane ①) — carried up here by the 2c EXIT CHECK, so they survive banner compaction:**
**DV-D13 aria asymmetry** — the legend's `aria-label`s deliberately keep BOTH the value and percent forms
(a screen-reader user shouldn't lose data to a toggle they may never perceive). Flagged at inscription,
**confirm at the wave's a11y pass** · **`_check_legend_migration.py`** is the authorisation to delete the
transitional block (exit 0) — the old grep in the handoff could never fire · **ds-012** h-bar labels clipped
16.8px, Dave's call on fix shape (`_DS-IMPROVEMENTS.md`) · **the swatch-shape delta** on Chart-bar, reversible
on request (`_REVIEW-SIGNOFF.md`).
**★ NEW 2026-07-26 (from the cap-fork session):** wire **BOTH** verify suites — `_verify_dv_legend.js` (donut exemplar, 27/27) and `_verify_dv_legend_members.js` (members, 54/54) — as advisory build steps, or vendor their jsdom dependency (today: `npm i jsdom` into `/tmp`, unwired; two suites now, so the prize is bigger) · decide `Chart-sparkline`'s **inert 15.6KB payload** (needs per-member behaviour opt-in in the registry — schema change) · give the graph parser a convention for an **ADR-amendment node** (`--verify` shows 5 unmatched seed edges) · F1 Legacy icon/default white · F2 Legacy `rag/error-tint` · tag-atom radius reconcile · F5 Dropdown's
6 locals · designer-pack v2.1 re-bake · **DV-D09 enact** (h-bar → series-3; bar lane) · **pro-forma dedup pass (ruling 3 — now also carries wave-1's
fl-summary≈Alert + B's observation that Tranche-1/2 hold earlier empty-state/toast sketches)** ·
composite motion tokens (would retire the matchValues pin) · enact whatever §C·2/§C·3 rulings change ·
consider `--verify` blocking.

## 4b. ★ QUEUED: button-states finesse pass (Dave 2026-07-22, "not now — follow up") *(was §C·3b — the wave-1 briefs/receipts + prior deltas point here under that number)*
Full brief in `_FUTURE-STATE.md` §button-states-finesse. Headlines: **Legacy state-mechanism fidelity
question** (as-built may be OPACITY, we render colours — VERIFY against source, don't flip on
recollection; "Legacy shouldn't change" = the design is frozen, our reproduction of it can be
corrected) · **Mono+Console pressed = darker pressed fill** (ties to the open tertiary/quaternary
pressed-token gap; B-D7's softer darken makes this more visible) · **SC keeps the opacity option
open, probably won't change** · **loader ATOM for all loading states** (registry group candidate #2;
Button's `.spin` = first consumer). Theme posture, Dave: Legacy frozen; Mono/SC/Console all in
design development. Natural shape: one session = fidelity check + pressed-tint tuner (review HTML,
rule live) + loader accretion.

## 5. Parked (unchanged)
Legacy hex seeding + provenance-gate flip · Console/Supercharge chromatic palettes · T9 review ·
Sutherland field test · full-review backlog (`_REVIEW-SIGNOFF.md`) · `_FUTURE-STATE` items ·
spot-illustration/empty-state icon set (`_ICON-GAPS.md`, wave-1's only gap).

> **pre-flight:** fill 30% + job 15% + wrap 5% = 50% AMBER · reserve 15% ring-fenced
> *(Session #7, 2026-07-27. Closed 🟡 **~60% AMBER, at the boundary**. **Overrun +5, and it was
> SELF-INFLICTED, not a discovery:** the byte-cap detour (a comment block that restated the ruling's arc
> inside a file whose header forbids exactly that) cost the difference. **Recorded per the throttle's own
> instruction to log every overrun so the 15% can eventually be re-derived from something.** The fork
> fired correctly and mid-flight this time — priced at ~55% fill, the render would have landed ~70% RED,
> and Dave chose flush. ⚠ The three-term projection was accurate to within 5 points here; **that is n=1
> and does not vindicate it.**)*
>
> **COMMIT STATE (refreshed 2026-07-27 ~14:20 BST from `date`, the suite was asserting the old ruling).**
> ONE commit: `knowledge/canon/dv-legend.js` (**DV-D17 ENACTED** — release-on-add + the removed
> superseded announce branch; trimmed to 16330/16384 after the ADR-0015 gate blocked the first pass) ·
> `knowledge/_verify_dv_legend_members.js` + `knowledge/_verify_dv_legend.js` (**six checks rewritten,
> old wording kept verbatim beside each; 4 new DV-D17 checks; `DVLEGEND` env override on both**) ·
> the 5 injected chart snippets + `showroom/chart-*.html` (regenerated, never hand-edited) ·
> `knowledge/_proforma/_DATAVIZ-DECISIONS.md` (**DV-D17 ENACTED block** + **DV-D16 (1) ANSWERED** with
> the scope measure) · `_DECISION-HISTORY/2026-07-27-the-suite-that-asserted-the-old-ruling.md`
> (**NEW dossier**) · `_GM-ARCHIVE.md` (2c roll, Batch 10) · `_LIVE-STATE-ARCHIVE.md` (2d roll) ·
> `_LIVE-STATE.md` · `knowledge/_REVIEW-SIGNOFF.md` · this file.
> **Build 60/60 GREEN (exit 0) · members 108/108 · donut 27/27 · 3 neutered controls all RED on the
> right checks · STAND-002 PASS, 26 standing docs reachable.**
> **⚠ WHAT THE AUTHOR FLAGS AGAINST HIS OWN WORK:** **108/108 and 27/27 are DOM assertions, NOT renders**
> — reading them as "DV-D17 is done" is the single most likely misreading of this handoff, and ds-018 is
> a live counter-example on the same component · **the DV-D16 downward re-price makes the next job look
> cheap**, which is exactly when to re-derive rather than inherit · **the `st.visible[id] = true` line is
> my call, not Dave's, and is unruled** — it is flagged in three places precisely because a quiet
> enactment choice is indistinguishable from a ruling six sessions later · **the donut suite's inability
> to catch an all-on regression is published, not patched** — do not treat the two suites as
> interchangeable.
> Dave pushes via GitHub Desktop (whole stack, Desktop closed while Claude commits).
>
> **pre-flight:** fill 30% + job 20% + wrap 5% = 55% AMBER · reserve 15% ring-fenced
> *(Session #6, 2026-07-27. ⚠ **The job term was for a BUILD that Dave then cancelled** in favour of
> capture-plus-ruling; the capture ran instead and cost more than the build would have been allowed.
> Closed 🔴 **~62% RED**. **The overrun is RECORDED, per the throttle's own instruction to record every
> overrun so the 15% can be re-derived from something.** Two honest causes: three ruling rounds arrived
> mid-ritual, each cheap, none priced — **the ~10%-floor failure mode the runbook says is gone, recurring
> in a new costume** — and I did not surface the Amber→Red crossing; **Dave asked "getting warm btw"
> before I said it**, which is the one thing the band rule exists to prevent.)*
>
> **[SUPERSEDED — kept for the record] COMMIT STATE (refreshed 2026-07-27 ~13:15 BST from `date`, the read-back offered the wrong options).**
> ONE commit: `knowledge/_proforma/_DATAVIZ-DECISIONS.md` (**§ Batch 10 NEW** — DV-D16 with **both**
> wordings and the reversal record · DV-D17 + 3 enactment bites · DV-D18 + the justification-shift note ·
> the read-back method finding) · `knowledge/_DS-IMPROVEMENTS.md` (**ds-018 NEW** with two competing
> causes; **ds-012 RULED (b)** + 5 enactment conditions + **a wording correction Dave's pushback earned**) ·
> `_FUTURE-STATE.md` (**★★ FLOATED: expandable "Other" buckets**) ·
> `_DECISION-HISTORY/2026-07-27-the-read-back-offered-the-wrong-options.md` (**NEW dossier**) ·
> `_GM-ARCHIVE.md` (2c roll, **Batch 9**) · `_LIVE-STATE-ARCHIVE.md` (2d roll) · `_LIVE-STATE.md` · this file.
> **Build 60/60 GREEN (exit 0) · capture gate 14 in scope / 0 fail / 0 warn · STAND-002 PASS, 26 standing
> docs reachable.** **NOTHING WAS BUILT — this commit is entirely record.**
> **⚠ WHAT THE AUTHOR FLAGS AGAINST HIS OWN WORK:** the **DV-D16 reversal means my read-back options were
> wrong once already today** — treat wording ② as Dave's words, not as my reading of them, and **re-read
> the ledger quote rather than this banner** · **ds-018's "instance five" framing is a HYPOTHESIS I want to
> be true**, which is exactly when to demand the measurement · **ds-012's ruling was taken at ~57%** —
> the conditions attached to it were written hot and deserve a cold re-read before enactment.
>
> **[SUPERSEDED — kept for the record] COMMIT STATE (2026-07-27 ~12:40 BST, the gauge becomes a throttle).**
> ONE commit: `knowledge/_RUNBOOK-context-gauge.md` (**§ ★ Half 0b NEW** — the throttle, the third tier,
> the bank/fee model, 4 anti-false-fix clauses incl. the PROVEN-form/UNPROVEN-rule gap; Half 0 rewritten,
> the ~10% floor removed) · `knowledge/_capture_gate.py` (**pre-flight FORM check** + 7 bites + 2 green
> controls + wrap wiring + `--lane` skip) · `knowledge/_DS-IMPROVEMENTS.md` (**ds-017 NEW**) ·
> `_FUTURE-STATE.md` (floated → **RULED**, diagnosis kept verbatim) ·
> `_DECISION-HISTORY/2026-07-27-the-gauge-becomes-a-throttle.md` (**NEW dossier**, incl. §5 the author's
> concerns against his own work) · `_GM-ARCHIVE.md` (2c roll, Batch 8) · `_LIVE-STATE` (2d) · this file.
> **Build 60/60 GREEN (exit 0) · capture-gate selftest GREEN, all classes bite · bite-the-bite PASSED
> (neutered band check ⇒ selftest red) · pre-flight check verified end-to-end on this handoff.**
> **⚠ THREE THINGS THE AUTHOR FLAGS AGAINST HIS OWN WORK** *(Dave: "you are super clever, but agreeable")*:
> the **15% is provisional** (n=3, one unknown, keyed off one unusual event — re-derive after ~5 sessions,
> and RECORD each session's overrun so there is something to re-derive from) · **"unspent allowance is
> LOST" is `inferred` ~75%**, not observed (it sat in a canon table as fact for 20 minutes) · **"1.36×
> pro-rata" is a number that looks like a target** — spending allowance on low-value work is not a win.
> **Superseded (do not act on): `git rev-list` showed 2 unpushed commits at session start** — this makes 3.
>
