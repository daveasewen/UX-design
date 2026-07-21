# Receipt — Phase-1 Worker A: radius migration + theme-response audit
*2026-07-21 · Worker A (Fable) · per `notes/_briefs/2026-07-21-phase1-worker-A-brief.md` + conductor live-concurrency amendments. NO commits made (conductor commits). No git run. No writes to GOOD-MORNING / _LIVE-STATE / _FUTURE-STATE / MEMORY.*

## What landed

All 10 assigned files migrated onto the ADR-0010 radius role tokens. The 21-file ratchet is now **fully closed**: `_RADIUS-GATE.md` reports **0 strict fails, 0 advisory files** — 21 migrated snippets + canon, no hardcoded `border-radius` anywhere in scope. Full build **42/42 green** (run twice: after file 5, after file 10). Pattern per the Button/Cards proofs: local var in BOTH `[data-theme]` blocks (value 0 = projected Mono value), rules on `var(--border-radius-<role>)`, manifest binding `"border-radius/<role>"`, basename into `MIGRATED_SNIPPETS` in the same change. 50%/999px idioms left literal throughout.

## Per-element role choices (record of judgment calls)

| File | Element | Role |
|---|---|---|
| Input-fields | `.box` (boxed field) | control |
| Input-fields | `.uctrl input` (underline field) | control |
| Input-fields | `.help-btn` ((?) help button) | control |
| Input-fields | `.demo-controls button` | control |
| Selection-controls | `.box` (checkbox) | control |
| Selection-controls | `.chip` (chips, all 3 kinds) | control |
| Selection-controls | `.chip .x` (dismiss button) | control |
| Selection-controls | `.demo-controls button` | control |
| Selection-controls | radio (50% ×2), switch (999px), thumb (50%) | literal, round by design |
| Dropdown | `.trigger` (combobox) | control |
| Dropdown | `.menu` (floating listbox panel) | **surface** — elevated panel, same grain as Cards/Modals; trigger and panel deliberately diverge (Console: 8 vs 12) |
| Slider | `::-webkit-slider-runnable-track` | **indicator** — progress rail, not a box control |
| Slider | `::-moz-range-track` + `::-moz-range-progress` | indicator — these two had NO radius decl at all; added the var so the flex slot works in Gecko too (Mono value 0, zero visual change) |
| Slider | thumb (50% ×2) | literal |
| Icon-button (snippets/) | `.iconbtn` | control (lock-step with Button) |
| Icon-button (_proforma/) | `.iconbtn` | control — migrated in the SAME change (basename-keyed list) |
| Badge | `.badge` / `.dot` / `.standalone` | **no role bound** — 999px pill idiom, deliberately round in every theme; binding a role would have wrongly cornered badges in Console. Its 1 gate count was PROSE (see finding F0) |
| Tags | `.tag` | control — interactive in 2 of 3 variants; shape-kin to Selection-controls chips, kept in lock-step |
| Status-indicator | `.chip` (tint chip) | **indicator** — same atom as List-items `.status`, which Worker B bound to indicator (verified, matched) |
| Status-indicator | `.sim` (simulate button) | control |
| Status-indicator | `.dot` (50%) | literal |
| Progress-tracker | `.track` | indicator (same judgment as Slider) |
| Progress-tracker | `.nav button` (Back/Next) | control |
| Progress-tracker | `.demo-controls > button` | control |

Summary: 15 control bindings, 1 surface, 5 indicator (incl. the 2 added -moz rules), 1 no-bind (Badge pill), 8 literal idioms untouched.

## Authoritative MIGRATED_SNIPPETS additions (Worker A — for clobber repair)

Exactly these 9 basenames were added by me, in this order:
`Input-fields.reference.html` · `Selection-controls.reference.html` · `Dropdown.reference.html` · `Slider.reference.html` · `Icon-button.reference.html` · `Badge.reference.html` · `Tags.reference.html` · `Status-indicator.reference.html` · `Progress-tracker.reference.html`
(Read fresh before every edit; no collision with Worker B observed — their 10 + Button + Cards were all present at every read.)

## Theme-response findings — PROPOSALS ONLY, nothing enacted

**F0 (gate mechanics, OBSERVED).** `_validate_radius.py` `strip_comments` removes CSS `/* */` only, NOT HTML `<!-- -->` comments — prose like "border-radius:0" in a snippet header comment counts as a declaration. Badge's single "hardcode" and one of Tags' two were prose, not CSS. I reworded the prose (legitimate doc fix); the checker itself is shared with Worker B so I did not touch its logic. Proposal: strip HTML comments in `check_text` + extend the selftest.

**F1 (Legacy miss, OBSERVED in the generated cascade).** Legacy overrides `button/primary/label/default` but NOT `button/primary/icon/default`. Icon-button's glyph binds the icon path → under `[data-apollo-theme="legacy"]` the `.cn-icon-button` block flips `--pri-default` to #DB0011 but `--pri-glyph` is absent, so dark mode renders the Mono dark glyph **#333333 on the red #DB0011 fill** (~1.8:1, illegible). Same class as the Button success-background miss. Proposal: add `button/primary/icon/default` = #FFFFFF both modes to `apollo-legacy.overrides.json` (mirror of the label override). **Render-pass eyeball requested: Icon-button × legacy × dark.**

**F2 (Legacy miss, OBSERVED in the override set + cascade).** The Legacy set carries `rag/success-tint`, `rag/warning-tint`, `rag/information-tint` but **NOT `rag/error-tint`**. Status-indicator's error chip therefore keeps the Mono tint (#F1E0DC/#2C120D — a tint of Mono red #B92F1E) while its siblings go Legacy teal/amber/navy. Proposal: add `rag/error-tint` to the Legacy set from the R-D20 eviction record's pre-eviction pair (I did not invent values). **Render-pass eyeball requested: Status-indicator × legacy, both modes.**

**F3 (red drift, OBSERVED value + INFERRED intent).** `progress/complete` resolves **#DB0011 both modes in the Mono base** (snippet + store agree; snippet reworked 06-29, pre-R-D19/R-D20). Per R-D19 #DB0011 is Legacy's alone; Mono's only red is #B92F1E. Same pattern as the Cards `--accent` drift. Proposal for Dave: either rebase `progress/complete` (Mono red #B92F1E, or mono ink given B-D1 monochrome direction) with Legacy keeping #DB0011 via override, or inscribe an explicit exemption (the "red = primary-action accent once per screen" rule may be argued here). Not enacted.

**F4 (red drift, OBSERVED value + INFERRED intent).** Badge's `--surface` binds `primary/background/default` = **#DB0011 both modes in Mono** — a Mono surface resolving a Legacy-only colour (the R-D17-class condition; the leak gate evidently does not scope this path). Also binds the OLD bare ladder (`primary/*`, not `button/primary/*`), so the Legacy theme override (which targets `button/primary/*`) never reaches it — Badge is #DB0011 in all four themes by accident of path, not by ruling. Proposal: Dave rules Mono badge red (keep-as-brand-accent vs rebase); either way rebind onto a live path so themes can reach it. **Render-pass eyeball: Badge across all 4 themes** (it will currently look identical in all of them).

**F5 (manifest-dodging locals, OBSERVED).** Dropdown declares 6 vars its manifest does NOT bind: `--field-bg`, `--border-disabled`, `--item-hover`, `--item-pressed`, `--text-disabled`, `--text-reverse`. Values include Legacy-era greys (#D7D8D6 = Legacy grey-3, #767676 = Legacy grey-5, #F3F3F3, #212121, #474747) that differ from the live Mono roles (e.g. item hover #F3F3F3 vs form/background/hover #F0F0F0). No theme can re-reach them and the projector cannot validate them. Proposal: bind onto live roles (form/border/disabled, text/disabled, form/background/hover|pressed — or mint menu-item roles); values would visibly change, so promotion + render check are Dave's. (Minor: `--error` is manifested but unused by any Dropdown rule.)

**F6 (policy hexes outside the manifest, OBSERVED, low risk).** Input-fields carries two hardcoded `#FFFFFF` (dark-mode RAG roundel shapes, lines `[data-theme="dark"] .err-msg .ic` / `.uic`) per the roundel policy. White works on all four themes' dark grounds, but they are invisible to the cascade; note for whenever the roundel policy gets tokenised.

**F7 (expected non-response, OBSERVED, no action).** `_proforma/Icon-button` binds the Legacy-era bare ladder (`primary/*` etc.), which no theme overrides — it renders perma-Legacy-red in every theme including Mono. Known tranche condition; fold-or-keep already queued for Dave (§C). Radius now flexes correctly even there.

**Positive checks (working as designed):** Legacy `text/default`/`text/secondary` correctly re-ink Input-fields, Tags, Selection-controls, Progress-tracker (title dims via text/secondary); Legacy rag/error reaches Input-fields' error stroke + Selection-controls' error state; Console projections exist for all 20 radius-bearing components (verified in AUTO-THEMES: control/indicator→8, surface→12; Dropdown renders trigger 8 vs menu 12); Badge correctly has NO Console projection (pill). Legacy stays square via `border-radius/default: 0`.

## Open questions

1. Tags = control was my call (interactive-dominant, chip lock-step); a static keyword tag as indicator is arguable — flag if Dave wants the split at variant level.
2. `.cn-tabs .indicator` was left "as control, worker may refine" in the census — Tabs is Worker B's file; not touched.
3. F3/F4 need a Dave ruling before anyone enacts (red is a brand question, not a wiring one).

## Files touched (complete list)

- `knowledge/snippets/Input-fields.reference.html`
- `knowledge/snippets/Selection-controls.reference.html`
- `knowledge/snippets/Dropdown.reference.html`
- `knowledge/snippets/Slider.reference.html`
- `knowledge/snippets/Icon-button.reference.html`
- `knowledge/_proforma/Icon-button.reference.html`
- `knowledge/snippets/Badge.reference.html` (prose de-trip only; no binding — pill)
- `knowledge/snippets/Tags.reference.html`
- `knowledge/snippets/Status-indicator.reference.html`
- `knowledge/snippets/Progress-tracker.reference.html`
- `knowledge/_validate_radius.py` (MIGRATED_SNIPPETS: +9 basenames listed above, nothing else)
- Generated (via generators, never hand-edited): `knowledge/_RADIUS-GATE.md`, `knowledge/canon/canon.css` AUTO-THEMES block, `showroom/*` pages, snippet-token artefacts

## Proposed §C lines (for the conductor)

- Radius ratchet CLOSED (21/21, gate reports 0+0) — Phase-1 radius migration complete; showroom re-rendered.
- Legacy override set: 2 concrete misses to add (button/primary/icon/default; rag/error-tint from the R-D20 eviction record) — F1/F2, render-verify then Dave promotes.
- Red-drift rulings for Dave: progress/complete + Badge surface both resolve #DB0011 in Mono (F3/F4).
- Dropdown manifest gap (6 unbound locals incl. Legacy-era greys) — F5, needs promotion decision.
- Gate nicety: _validate_radius should strip HTML comments (F0).

## Build state at handoff

`python3 knowledge/_build_all.py` → **42/42 green** (final run after file 10). `_validate_radius.py` → 0 strict / 0 advisory. Generators in sync (snippet-tokens, theme-cascade 28 paths/60 projections, showroom 40 pages). No foreign-file failures encountered at any point; no waits/retries needed. **No commits made.**

## ADDENDUM 2026-07-21 (same evening) — F3 + F4 ENACTED on Dave's ruling

**Dave, in-chat (verbatim, both for the ledger):** *"resolve this to the newer red status color"* (on F3/F4), then the why: *"mono is named mono for the very reason it only uses colour with intent, rag, status and dataviz only"*, then, on the dark-badge contrast question: *"is there a red value for glyphs that carry meaning like arrows etc, can you hunt it out, we need to check if it has enough contrast with black text."*

**What changed (3 source files + regen):**
1. `tokens/semantic-colour.json` `progress/complete`: #DB0011 flat → **#B92F1E light / #CC4333 dark**, `$alias` → `rag/error-glyph` (per-mode strength pair; bar = bare on-ground indicator; flat #B92F1E is 2.89:1 on #1A1A1A, under the 3.0 floor). Supersedes the 2026-06-20 "brand red" note.
2. `tokens/themes/apollo-legacy.overrides.json`: + `progress/complete` (#DB0011 both — evicted base values) · + `rag/error-background` (#A8000B/#DB0011, tracks bare role; zero consumers today after the Badge re-seat below — kept, forward-correct for Alert/Banner/Toast, per the file's Phase-1 extension charter).
3. `snippets/Badge.reference.html`: `--surface` → **bare `rag/error`** (per-mode #B92F1E/#CC4333), numeral stays WHITE; manifest + both contrastPairs + prose updated. First seat was `rag/error-background` (mode-stable) — its dark edge failed the audit at 2.89:1; **the hunt answered it**: the meaning-glyph red (`rag/error-glyph`, also dataviz `delta/loss` arrows) passes everything per-mode. **Black-text check (Dave's ask): black FAILS both reds — 3.49 on #B92F1E, 4.42 on #CC4333 (ink #1A1A1A: 3.66). White passes both: 6.02 / 4.75.** Breach-is-white survives on arithmetic. *(Correction, inscribed loudly: I mid-session claimed white-on-#CC4333 ≈4.0 fails — wrong; the stored 3.97 was glyph-as-text on the old #111 ground. Actual white-on-#CC4333 = 4.75.)*

**Verification (OBSERVED):** full `_build_all.py` **42/42 green, 0 ❌** (log: `.git/worker-a-build.log`); snippet gate 40/0; cascade 30 paths/60 projections in sync; Legacy projections confirmed in canon.css (`.cn-badge --surface:#A8000B` · `.cn-progress-tracker --complete:#DB0011`); radius gate still 0/0; leak gate 0. Showroom badge + progress-tracker pages regenerated.

**For the conductor to inscribe (RAG ledger candidate, quotes above):** progress/complete + Badge seated on the Mono status red — closes the OWED `progress/complete` Mono ruling (R-D19 line in _LIVE-STATE §3). `tabs/active` remains the last unruled red (archived consumer, unchanged). F1/F2/F5 remain un-enacted proposals.

**Process note (self-caught):** two `_build_all.py` runs briefly overlapped mid-enactment (my backgrounding error, then a pkill that matched its own shell — exit 143); tree verified intact afterwards (git diff --stat sane, manifests parse) and every generator re-run clean before the final green build. No worker/conductor collision at any point.

## ADDENDUM 2 — ruling sheet built at Dave's ask (pending his eye)

Dave flagged the projector line (`--muted` → `text/secondary` → #1A1A1A/#FFFFFF) and asked to see it to rule. That resolution = R-D16's Mono collapse rendering live. Built **`reviews/MONO-SECONDARY-INK-2026-07-21-v1.html`** — live controller: keep-collapse (as-ruled) vs mono-ramp dim vs custom pair; real Progress-tracker specimen + hierarchy strip, light/dark panes, Legacy's ruled dim (#545454/#9B9B9B) alongside, live WCAG readouts, ledger-ready export. **No ruling yet — nothing changed in the store; R-D16 stands until Dave rules on the sheet.** If re-seated: text/secondary token edit + R-D16 AMENDED edge + 11 consumers re-project (conductor inscribes).

## ADDENDUM 3 — three harness rulings ENACTED + two findings (Dave live on the showroom)

**Ruling A (sheet export, pasted by Dave verbatim):** "text/secondary (Mono): KEEP the R-D16 collapse — single ink #1A1A1A/#FFFFFF; de-emphasis stays weight+size. No token change. R-D16 stands unamended." → RECORDED ONLY, nothing changed. R-D16 reconfirmed on the live sheet 2026-07-21.

**Ruling B (progress-tracker, verbatim):** "i think this is the right behavior and in mono and console it should be black. the colours in legacy and supercharge are fine." → ENACTED: `progress/complete` → ink pair #1A1A1A/#FFFFFF ($alias mono/4 + grey/white, mirrors text/default; literal black is invisible on the dark page — interpretation stated to Dave before enacting). Console inherits Mono (no override needed). Legacy keeps #DB0011 (override, already present). **Supercharge gains its FIRST override** — `progress/complete` #B92F1E/#CC4333 (the pair on screen at ruling time); its file's "deliberately EMPTY" description superseded for this one path. Trail in the token $note: #DB0011 drift → status red (early evening) → ink (this ruling). Progress is STRUCTURE, not status.

**Ruling C (badge, verbatim):** "the colours are fine apart from Legacy, it should be the legacy primary red on both light and dark." → ENACTED: minted component token **`badge/background`** (Mono: $alias bare rag/error → per-mode #B92F1E/#CC4333; same component-tier override pattern as button/primary/*). Badge manifest + pairs rebound. Legacy overrides badge/background = **flat #DB0011 both modes** (brand-primary, deliberately NOT the Legacy error pair — the slot exists so badge ≠ error per theme). Known fidelity condition noted in the override $note: white numeral on #DB0011 ≈ 4.02:1 — queued with the text/on-success Legacy-fidelity-vs-AA family. NB: this is the first live instance of the queued component-type flex tier's problem class, solved within current architecture via the button/* precedent.

**Verification (OBSERVED):** build **42/42 green, 0 ❌** (`.git/worker-a-build2.log`); cascade 32 paths / 61 projections; canon.css confirmed: supercharge `.cn-progress-tracker --complete:#B92F1E` (+#CC4333 dark block) · legacy `.cn-badge --surface:#DB0011` BOTH mode blocks · PT snippet re-projected `--complete:#1A1A1A/#FFFFFF`. Showroom regenerated (40 pages).

**Finding — scale interaction (Dave: "there is an established interaction for buttons based on scaling"):** located + status: promoted 2026-06-22 ("Refined scale-physics — grow toward cursor on hover + press"), factors tokenised as LOCAL vars 2026-07-15 (`--btn-grow:1.04 / --btn-press:0.95`), carried by the Button-family atoms (2 files), explicitly "pending the interaction-motion token rollout". NOT in the token store → not theme-flexable yet → flex-slot candidate for the queued component-type/type-group architecture session (same shape radius had pre-Phase-0).

**Finding — "are we using the atoms to build these patterns?" (Dave):** honest audit: **value-level retrieval YES** (tokens, type composites via T-D9/T-D12, radius roles — organisms bind the same roles the atoms bind); **rule-level atom retrieval NO** — organisms re-implement sub-buttons locally. Proof by interaction drift: the Button atom presses with scale 0.95; Progress-tracker's Back/Next press with `translateY(1px)` (line 59); Modals declares its own `.btn` recipe. The established scale interaction doesn't propagate because nothing retrieves the atom's RULES. This is the recorded composition-tier gap made concrete + measurable — sharpened by Dave to: retrieval must reach INSIDE organisms, not just above them. **Strategic flag for the conductor / Phase 2: building the ~50 itinerary gaps on the current pattern duplicates sub-atoms ~50×; the atom-retrieval mechanism (generated partials / component machine) should land BEFORE the fan-out.**

**Queue proposals (§C candidates):** (1) responsive stepper collapse (roundels→bar, Tranche-1; canon dots at `273d18c~1`) — Dave: "i think this is the right behavior"; fold into canon Progress-tracker when composition mechanism lands? (2) interaction-motion tokens into the type-tier session. (3) Legacy AA-fidelity pair now has TWO members (on-success white-on-teal · badge white-on-#DB0011) — rule together. (4) Composition/atom-retrieval mechanism priority vs Phase-2 fan-out — strategy call, conductor + Dave.

## Provenance (session `local_e06e4e3f`, appended on role change)

Executed by a **Fable subagent** directed by session `local_e06e4e3f` (Dave approved the spawn; his stand-down-to-Worker-A instruction crossed it in flight — the subagent had already completed the brief). On stand-down the session **verified (OBSERVED)**: `_RADIUS-GATE.md` reads 21 migrated / 0 advisory · HEAD unchanged at `6e900b8` (no commits) · GOOD-MORNING / _LIVE-STATE / _FUTURE-STATE untouched per `git status` · all 21 basenames present in `MIGRATED_SNIPPETS`. Full-build 42/42 is the subagent's run, not independently re-run (avoiding generator collision with the live Worker B session). Conductor may re-run at reconcile.
