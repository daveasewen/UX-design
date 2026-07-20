# _LIVE-STATE — what's true now (cold-start spine)

*The supersession ledger for the project: what's **LIVE**, what's **DEAD** (don't build on it), what's
**OPEN**, plus in-flight **TARGETS**. Read this second, after `GOOD-MORNING.md`, before
`knowledge/README.md`. Per **ADR-0007**. ⚠️ **INTERIM — hand-maintained** until `_build_live_state.py`
generates it from front-matter edges + tombstones. Refresh at end of every session alongside the
handoff — and **stamp the date from `date`, never from the session's own belief** (the T-D12 handoff
mis-dated itself a day forward; commit timestamps caught it).*

*Siblings: **`_FUTURE-STATE.md`** — side-quests, feature ideas, resurrection candidates (the forward
half of the state machine, Dave's ask 2026-07-18) · **`_DECISION-HISTORY/`** — dated per-thread
narrative, relocated verbatim (how we got here; see its README for the rules + RESURRECT tags).*

## ⏱ LATEST DELTA — 2026-07-20 (evening 3) — "Pre-flight for the Mono alignment sweep: record de-risked, worklist pinned, sweep handed to a fresh session"
- **Session opened good-morning; scoped the Mono alignment sweep but did NOT execute canon edits** (Dave: "be careful, I don't want to lose anything" + context discipline → spin a fresh session for the bulk). Baseline verified: tree clean, all pushed, **build green 37/37**.
- **★ INTEGRITY CHECK — nothing lost.** All 88 round-1→3 rulings are durably inscribed (21 clustered in `reviews/_style-consolidation-decisions-2026-07-20.json`; 20 singletons in `reviews/gen_style_consolidation_review.py` `SINGLETON_RULINGS`). Authoritative **align = 39** = 27 snippets + 1 `_review` (reconciled tab/stepper) + 11 `_proforma`.
- **★ RECORD DE-RISKED (only file changed this session): `knowledge/_STYLE-PROVENANCE.md` §backlog.** The pre-round-3 "backlog A (19 snippets)" list was STALE — it named Hero/Navigations/Progress-tracker/Tabs as align targets, but round 3 **archived** all four and kept **Notifications** as legacy-reference. Marked it superseded (struck-through, kept for audit) and wrote **§A-AUTH** — the authoritative 39-item align list + explicit DO-NOT-ALIGN (5 archived) + DO-NOT-CONVERT (Notifications) lists + per-item drift type (unblocked vs blocked). Build still green 37/37.
- **★ TRAPS a naive sweep would hit (now recorded in §A-AUTH):** (1) the stale list; (2) archived files still in the advisory gate's dir-wide scan (`MONO_DIRS`) — they leave scope via the later dedup pass, don't get Mono-edited; (3) Notifications' `#A8000B` is *correct* Legacy red — retag, never convert.
- **NEXT SESSION (Sonnet, cold start) — turnkey brief in `GOOD-MORNING.md` §C:** (a) **teal→green** on Masthead + Tranche-2…9 (`Tranche-1` has none): `#00847F` success → Mono `rag/success-glyph #4A9568` (dark ground), **preferably tokenise not hardcode**; ⚠️ **OPEN sub-decision** — the `#i-success` SVG is a filled circle with a WHITE tick; under type26-013 the tick likely → BLACK (cf. `on-success`=black) — rule before swapping the tick. (b) grey inks (`Avatar`,`Quick-actions`)→`color/mono/*` **via the grey-tint check** (surface numbers to Dave first). (c) regen `_review` copies (`_make_review.py`). **HELD for a tuner:** all red — bare `rag/error` (R-D17), `tabs/active` + `progress/complete` Mono values (R-D19). Then flip `_validate_theme_provenance.py` to blocking.


- **★ LIVE — the FOUR THEMES are now wired as an architecture, not just intent (ADR-0011).** `docs/decisions/ADR-0011-four-theme-token-architecture.md`: themes = **override sets at the semantic tier** (Mono = base · Legacy = populated override · Console + Supercharge = **declared nullable slots**, ADR-0010). Registry `tokens/themes/_themes.json` = single source of truth for which hex belongs to which theme. Mechanises R-D15. **Root cause found:** the token store had NO theme dimension — only light/dark modes — so Legacy red + Mono lived in the same flat roles (`primary/*`=#DB0011, `tabs/active`, `progress/complete`, bare `rag/error`). That is why "align to Mono" was "too loose" (Dave).
- **★ LIVE — RULING R-D19: red belongs to a THEME.** Legacy red `#DB0011`/`#A8000B` = Apollo **Legacy only** (CTA, tabs, progress, Legacy error). Apollo **Mono's only red = `#B92F1E`**, used **only** for status/RAG + dataviz (never action/nav). Any Legacy red in a Mono surface = **drift**. Source: Dave ("these reds are valid for legacy only, we have a new red for mono, only used for status and RAG"). Ledger `_proforma/_RAG-DECISIONS.md`.
- **★ LIVE — THE RECORD: `knowledge/_STYLE-PROVENANCE.md`** (Dave's ask — "clear record … don't miss this in future"). Classifies every artefact across `snippets`/`_proforma`/`_review`/`_fitness-test` by theme-era; scopes LIBRARY (align to Mono) vs `_fitness-test` (exploration = mine · research = preserve · **SME-payments journeys = ignore, test pages** per Dave). Machine mirror `reviews/_style-clusters.json`.
- **★ LIVE — VISUAL REVIEW SCREEN: `reviews/STYLE-CONSOLIDATION-REVIEW-2026-07-20-v2.html`** (Dave: "when there are duplicate patterns I need to compare visually" + "review screen … launch full screen … iframes too small"). Per-cluster picker; wrapping grid (no h-scroll); column/height/bg controls; **Open ↗** (full window) + **⤢** (fullscreen) per variant. Old exploration beside canon, theme-era + drift tags. (v1 COMPARE = first cut, superseded.)
- **★ LIVE — ADVISORY GATE `_validate_theme_provenance.py`** (wired into `_build_all.py`, build green **37/37**). Flags **hardcoded** foreign-theme hexes in Mono surfaces — the blind spot the token leak gate can't see. First run: **68 hardcoded Legacy hexes across 61 Mono files** → `_THEME-PROVENANCE-GATE.md`. Advisory now; **promote to blocking after the migration** (ADR-0011).
- **OPEN / BACKLOG (in `_STYLE-PROVENANCE.md` §backlog):** align 19 drifting snippets + 12 proforma tranches (Sonnet sweep, then regen `_review` copies); **rulings owed** for `tabs/active` + `progress/complete` Mono values (R-D19) before their Legacy red can be gate-seeded blocking; bare `rag/error` Mono red rebinds with error/warning/info (R-D17). History pointer: this delta + ADR-0011 + R-D19.

## ⏱ PRIOR DELTA — 2026-07-20 (~17:30 BST) — "Button rebind → Legacy-colour leak gate + RAG success green (R-D18) + Icon button"
- **★ LIVE — `Button` REBOUND onto the Mono `button/*` ladder** (commit `528e205`, build green 36/36): primary monochrome (no red); hover = operational **0.70 opacity** over the page (color-mix; stored colour-equiv kept, ADR-0009/B-D3); **B-D4 disabled-label fold across all four tiers** (`label/disabled` → `text/on-disabled`; siblings had drifted onto `text/disabled` `#E1E1E1` == ground = invisible). Success → R-D14 **green fill** + new per-mode `text/on-success` (black label, type26-013) — **B-D6**.
- **★ LIVE — Legacy-colour LEAKAGE GATE** (`knowledge/_validate_legacy_leak.py`, build-blocking, R-D17): no Mono surface may resolve to a Legacy-only colour (seeded with teal `#00847F`). Caught **7** leaking surfaces (incl. Reorder + Status-indicator). Root cause: `color/green/600` holds the teal; **all four bare `rag/*` roles are Legacy-drifted**.
- **★ LIVE — RAG success GREEN set COMPLETE (R-D18, Dave on a live tuner):** glyph dark `#4A9568`, tints `#DCEDE3`/`#12291D`, bare `rag/success` role rebased off teal → tracks the glyph. 7 components swept; **leak gate 0 waived / 0 leaks** — teal evicted from Mono. Tuner `reviews/RAG-SUCCESS-GREEN-2026-07-20-v1.html`.
- **★ LIVE — ADR-0010** (`docs/decisions/ADR-0010-token-schema-nullable-flex-slots.md`): explicit nullable placeholder slots for the dimensions we flex; `null` = declared-but-unset; "no null under a live binding" gate = companion to the leak gate. Pilot = the RAG green set. Staged.
- **★ LIVE — FIRST build-out component: Icon button GATED** (commit `8f3f07c`): on the Mono `button/*` ladder, real HSBC sprite glyphs, 4.5:1 (icon-015), 44px target, aria-label, visible disabled glyph. **38→39 gated? (40 snippets / 40 metas)**; **39 P1 gaps remain**.
- **OPEN:** bare `rag/error`/`warning`/`information` roles still Legacy-drifted (same fix pattern; needed before Alert/Banner/Toast). ADR-0010 null-gate + slot rollout staged. Primary-hover ≈ secondary parked. History: `_DECISION-HISTORY/2026-07-20-button-rebind-legacy-leak-gate.md`.

### ⏱ PRIOR DELTA — 2026-07-20 (evening) — "Mono primary-action token + ADR-0009 state-styling architecture (live-editor loop)"
- **★ LIVE — the OWED mono primary-action ruling is CLOSED (commit `b895c40`, build green 35/35).** `button/primary/*` minted, completing the button ladder: component → semantic (`surface/action-primary{,-hover,-pressed}`, `icon/on-inverse`, `text/on-disabled`) → `color/mono/*`. **Monochrome — NO red** (red is out of bounds for Mono, not merely Legacy-only; ruling B-D1). Settled values (Dave, dialed on the v7 live editor): default `#1A1A1A`/`#FAFAFA` · hover **opacity 0.70** operational + colour-equivalent `#626262`/`#B7B7B7` stored · pressed `#000000`/`#FFFFFF` · disabled fill `#E1E1E1`/`#484848`, label `#9D9D9D`/`#808080`. Ledger: **`knowledge/_proforma/_BUTTON-DECISIONS.md` (B-D1…B-D5)**.
- **★ LIVE — ADR-0009 state-styling architecture** (`docs/decisions/ADR-0009-state-styling-architecture.md`, extends R-D15/ADR-0004/0008): the **colour token is the universal per-state substrate** (per-theme override; a chromatic mode — red default/blue hover/green active — is just an override set); **opacity is an optional operational layer**; **render-mechanism is a per-state SET `{colour|opacity|both}`**, colour-alone first-class; **AA is invariant** across mechanism. Wired **non-breaking** via `$extensions.apollo.state` on the hover token; migrates to a first-class number/opacity token with the style-builder.
- **FIXED:** (a) **invisible disabled label** — `text/disabled` `#E1E1E1` equalled the disabled ground → minted **`text/on-disabled`** visible ghost, exempt-but-perceivable (B-D4; other button tiers likely share the defect — flagged). (b) **3 dark-mode border greys** off the Legacy primitive: `border/strong`, `form/border/{default,pressed}` dark alias `color/grey/dark-mode/200` → `color/mono/8`. **Legacy alias advisories now 1 (was 4)** — the remaining one is `primary/border/hover` dark = Legacy red, intentionally left.
- **PRINCIPLE (Dave):** **live-controls-in-reviews** — every review carries a *decision control per open choice*; Dave edits in place, not an AskUserQuestion round-trip. Codified in `_FUTURE-STATE.md` + memory `feedback-live-controller`; reference impl = the v7 editor (segmented selectors, mechanism switch, AA-clamped opacity dial, chromatic example, export block). **Style-builder interface** added to `_FUTURE-STATE` (the harness-side home of ADR-0009).
- **OPEN / DEFERRED (the thing to line up before building more components):** the **`button/*` snippet rebind** — until it runs, the *rendered* Mono button still shows **red primary** and hover isn't yet operationally opacity; batched with the secondary/tertiary/quaternary rebind (queue #4). Opacity → first-class number token with the style-builder. **T9 secure entry still awaits Dave review.** History: `_DECISION-HISTORY/2026-07-20-mono-primary-state-styling.md`.

## ⏱ Prior delta — 2026-07-20 (later) — "Canonical-core ADR + doc/memory housekeeping"
- **LIVE:** the canonical-core strategy now has its **formal anchor — `docs/decisions/ADR-0008-canonical-core-and-adapters.md`** (extends ADR-0002/0005/0006). Records: Apollo = canonical source (well-formed superset, not a mirror); quality is the vote-winner, never inherit a consumer's flaw (the decoupled `button/*` tier is the reference divergence); respect-but-don't-follow via an **automated adapter layer** (`sutherland-diffs.json` + hub-and-spoke `codeBindings`); operating principle **"diverge for quality, keep every divergence machine-mappable"**; designers run the full architecture. **★ the OWED ADR is now DRAFTED** — clears the 2026-07-20 open item.
- **HOUSEKEEPING done:** **GOOD-MORNING.md un-staled** (was two sessions behind — refreshed to current truth, §A + STAND-002 standing list intact) → the "GOOD-MORNING is STALE" flag below is now CLEARED. **Memory-index compaction run** (was flagged DUE ~20KB). No gated-code change; build stays green. Wrap commit = ADR-0008 + this file + GOOD-MORNING (+ memory files, outside the repo).
- **OPEN (unchanged, promoted to next-session frontier):** the Sutherland field test (ADR-0008 case #1) · `designer-skills-v1` revisit (no-Python assumption now overturned) · the mono primary-action token ruling. See GOOD-MORNING §C.

## ⏱ Prior delta — 2026-07-20 — "Button ladder → canonical 3-tier tokens; the Sutherland/canonical-core strategy locked"
- **LIVE:** Apollo Mono **button ladder** is now a proper 3-tier stack — `button/{secondary,tertiary,quaternary}` (component) → `surface/action*` · `text/on-action` · `border/action-strong` (semantic) → `color/mono/*` (primitive); the tier gate ENFORCES it; build green 35/35 (commit **`ded4900`**). Secondary = grey filled **per-mode** (L `#626262`/white label · D `#808080`/black label — a11y-verified, label flips by mode); tertiary = transparent + digi-black(L)/white(D) border+text; quaternary = undecorated text. **Red primary = Apollo Legacy only** (not created for Mono). The **overloaded legacy `secondary/tertiary/primary`** are UNTOUCHED (they carry checked-state/surface roles) — Mono buttons got their own decoupled tier.
- **★ STRATEGY LOCKED (Dave 2026-07-20) — Apollo = CANONICAL source; consumers via AUTOMATED ADAPTERS; quality over conformance.** Apollo is the smart DS replacing the Figma→code→docs triptych; must **serve/replace ANY codebase**. **Respect-but-don't-follow** Sutherland; map after the fact (seed: `tokens/_manifests/sutherland-diffs.json` + hub-and-spoke `codeBindings`). Operating principle: **diverge for quality, keep every divergence an automated transform.** Memory `apollo-canonical-core-adapters`. **✅ FORMAL ADR NOW DRAFTED → `docs/decisions/ADR-0008-canonical-core-and-adapters.md`** (see LATEST DELTA).
- **Designers have Python → no compromise:** Apollo runs as the **full architecture** on their machines. **Revisit `designer-skills-v1`** before it ships (currently no-Python guidance-only). Ground-truth plan: run Apollo in **VS Code + Copilot beside the real Sutherland repo** → build the real Apollo↔Sutherland map (also the first live-fire of the designer pack).
- **OPEN:** the button ladder greys/tiers go on the full-review backlog (`knowledge/_REVIEW-SIGNOFF.md`); legacy `secondary/tertiary` → `button/*` migration + snippet-button rebind = the eventual adapter/cleanup (worker flagged the snippet list in `notes/_receipts/2026-07-20-worker-button-3tier.md`).
- **HOUSEKEEPING:** amber gauge threshold moved **0.45 → 0.50** (`_context_gauge.py` + runbook). ✅ GOOD-MORNING refresh + memory-index compaction both DONE in the 2026-07-20 (later) session — see LATEST DELTA.

## ⏱ Prior delta — 2026-07-19 (evening) — "Tranche-9 secure entry + all tranches tokenised"
- **LIVE:** **Tranche-9 · Secure entry** BUILT + gated (build green 35/35) — `knowledge/_proforma/Tranche-9-interactive.html`. OTP/PIN (segmented, auto-advance, paste), password (**Show/Hide text** toggle + **mono** strength ramp + requirement checklist), memorable-word partial entry, re-auth card (+ device-agnostic biometric alt). Monochrome; the one hue = `rag/error` dot; carries a `#token-manifest`. **NOT yet Dave-reviewed.**
- **LIVE:** **T1–T8 TOKENISED** (Sonnet worker) — each now carries a `#token-manifest`; `gen_snippet_tokens.py` projects **all 9 tranches** (`Tranche-[1-9]`), closing the pre-R-D16 hardcode drift. Receipt: `notes/_receipts/2026-07-19-worker-tranche-tokenize.md`.
- **OPEN / RULING OWED (sharpened):** mono **primary-action** token gap. Worker VERIFIED that binding `--pri-lbl`→`text/reverse` gives **1.0:1 in dark** (primary ground inverts by mode; `text/reverse` is flat white). Interim across T1–T9: `--pri`→`text/default`; `--pri-h`/`--pri-lbl`/`--icon-rev` kept as safe **local literals** (flagged). Fix = mint `action/primary/{background,background-hover,label}` (+ an `icon/on-inverse`); `text/on-inverse` (#FFFFFF/#333333) is the ready label candidate — **Dave's call** (promotion is his).
- **NOTE (visible delta):** tokenisation made `--focus` resolve to the real **blue** focus-ring (`focus/ring` #305A85/#4587A7) across all tranches — was mono near-black in T6. Functional a11y token; flag if a mono focus ring is wanted.
- **OPEN (carried):** rest of the store still 2-tier → deferred migration; 4 legacy alias bugs (advisory in `_validate_token_tiers`).

*Prior delta (2026-07-19 PM, commits `dba719b`+`e69b75f`): R-D16 enacted (greys on `color/mono/*`, +2 a11y carve-outs — do NOT revert to nearest-step), snippets styled BY tokens, strict 3-tier token stack + dark-elevation exemplar — all LIVE below / in `_STANDARDS.md`.*

> **SPINE DISCIPLINE (ruled 2026-07-18, Fable consolidation session — supersedes the "1044 lines"
> banner):** state lines live here; **narrative longer than ~10 lines goes to `_DECISION-HISTORY/` at
> write time, in the same pass.** Split entries end `History: _DECISION-HISTORY/<file>`. Advisory
> tripwire ~500 lines. Edits to this file are reachability-relevant — run
> `python3 knowledge/_validate_standing_instructions.py` (STAND-002) after touching it.

*Last refreshed: **2026-07-20 ~21:29 BST — "Pre-flight for the Mono alignment sweep"** (solo / self-conductor): Verified NOTHING lost — all 88 round-1→3 rulings durable (decisions JSON + generator `SINGLETON_RULINGS`); reconciled the authoritative **align = 39**. De-risked the record: replaced the stale pre-round-3 "backlog A" in `_STYLE-PROVENANCE.md` with **§A-AUTH** (authoritative 39-item list + DO-NOT-ALIGN / DO-NOT-CONVERT). Scoped teal→green but **held ALL canon/token edits** for a fresh Sonnet session (Dave: "be careful, don't lose anything" + context discipline); found teal→green carries an OPEN sub-decision (the `#i-success` white tick → black under type26-013). No canon change; build green 37/37. Two procedure misses caught by Dave — improvised git instead of `_RUNBOOK-git-commit.md`, improvised the handoff instead of `_RUNBOOK-capture-ritual.md`; corrected, ran both by the book. Dossier `_DECISION-HISTORY/2026-07-20-preflight-mono-sweep.md`. Previous: **2026-07-20 ~18:35 BST — "Style consolidation → four-theme token architecture"** (solo / self-conductor): Found the semantic token store had **no theme dimension** (Legacy + Mono shared flat roles = the "too loose" root cause); ruled **R-D19** (red is themed — Legacy `#DB0011`/`#A8000B` vs Mono's only red `#B92F1E` for status/RAG/dataviz); wrote **ADR-0011** (themes = semantic-tier override sets; Console/Supercharge = nullable slots); built the **`_STYLE-PROVENANCE.md`** record + `_style-clusters.json`, the **v2 visual review screen** (+ overlay copy), and an **advisory theme-provenance gate** (68 hardcoded foreign hexes / 61 Mono files). Commit `a1b9fbb`, build green 37/37. Dossier `_DECISION-HISTORY/2026-07-20-style-consolidation-four-themes.md`. Previous: **2026-07-20 ~17:30 BST — "Button rebind → Legacy-colour leak gate + RAG success green (R-D18) + Icon button"** (solo / self-conductor): Rebound `Button` onto the Mono `button/*` ladder (red-free primary, 0.70 opacity hover, B-D4 disabled-label fold), success → R-D14 green + `text/on-success` (B-D6); built the **Legacy-colour leakage gate** (R-D17, caught 7 surfaces); ruled the **success green set** on a live tuner (R-D18) → 0 leaks; wrote **ADR-0010** (nullable flex slots); built **Icon button** (first build-out component, gated). Commits `528e205` + `8f3f07c`, green 36/36. Context hit Amber/Red → capture ritual run. Previous: **2026-07-20 — "Canonical-core ADR + doc/memory housekeeping"** (solo / self-conductor): Drafted **ADR-0008** (canonical-core + automated adapters — the formal anchor for the 2026-07-20 strategy lock); un-staled `GOOD-MORNING.md` (it was two sessions behind); compacted the memory index (moved 10 closed/historical entries to `MEMORY-ARCHIVE.md`, tightened hooks — under the 17.1KB limit). Housekeeping — no gated-code change, build green 35/35, STAND-002 reachable; committed `24d1331`, pushed. Previous: **2026-07-19 — "Apollo Mono: the money atom, digital-black as the new #000, and the grey ramp ruled onto semantics"** (conductor): Built the **Amount-display** P1 atom (money-format primitive, gated) with new figure rungs `.t-cm-figure-4/5/6` (32/16/14, tabular). **Digital black `#1A1A1A` ruled the new `#000`** (general) → swept all 38 components' dark grounds + `background/default` dark → `#1A1A1A` (COMMITTED, conductor). Surfaced all 79 semantic greys vs the `color/mono/*` ramp; Dave RULED **R-D16** — Mono text ink → `mono/4 #1A1A1A` (**supersedes col25-011** for Mono; Grey-8 = Legacy), **drop** secondary text grey, `#767676`→`mono/8`, tinted `#D7D8D6`→`mono/12`, mechanical maps approved — **RULED, enactment PENDING (Sonnet).** Fixed a **STAND-002 red build** (the prior GOOD-MORNING rewrite had dropped the standing-docs reachability list). Sheet `reviews/APOLLO-MONO-SEMANTIC-GREYS-2026-07-19-v1`; dossier `_DECISION-HISTORY/2026-07-19-amount-display-and-mono-greys.md`. Previous: **2026-07-19 — "RAG light fills: proving per-mode, and a tuner I could use for days"**: LIGHT-mode RAG fills LOCKED (R-D12…R-D14) — light green `#5DAC7B` / blue `#7DABCD` (H241), dark stays R-D10; red+amber mode-stable, green+blue **per-mode PROVEN** (exhaustive search: no single pair holds green›blue on both grounds). Rulings: R-D12 (NO lines, aesthetic + black-text states) · R-D13 (light locked, dark reopened-then-held) · R-D14 (full reconciled set). Reframe: fill contrast = **salience lever not a floor** (label carries meaning, R-D6 — I over-raised amber-washout, Dave corrected). Built: derivation `reviews/_rag_light_fills_calc.py`, sheets v1→v9-LOCKED, ★ **two-mode in-browser OKLCh tuner** (ramp-guard) = Apollo Labs / Layer-2 candidate. NEXT = token promotion (Sonnet, behind blast-radius gate). **CONDUCTOR-MERGED with a parallel session ("Context gauge + adversarial densify", committed `e7f8b87`):** context fuel-gauge `knowledge/_context_gauge.py` + `_RUNBOOK-context-gauge.md` (Red >70% fires the ritual); adversarial-densify method (`_RUNBOOK-densify-adversarial.md` — FINDING: rewording near-dead corpus-wide, DON'T corpus-densify, keep the adversary gate); memory index pruned → `MEMORY-ARCHIVE.md`; **★ BUG: `gen_rules_index.py` silently truncates 11+ `_RECONCILIATION.md` entries mid-sentence** (OPEN, see below); conductor pattern `notes/_PARALLEL-SESSIONS-conductor.md`. Previous: **2026-07-19 — "RAG colour: halation, the salience ramp & the astigmatism instrument"**: RAG DARK set LOCKED (R-D5…R-D11, dossier `_DECISION-HISTORY/2026-07-19-rag-colour-halation-ramp.md`) — breach `#B92F1E` white / watch `#F0B13A` / healthy `#43AD6F` / info `#5F92B9`, uniform Medium 500, red+amber carve-outs, green+blue ramp-tuned; halation bloom/dance MODEL built (`reviews/_rag_bloom_model.py`); the SALIENCE-RAMP reframe (status ≠ isoluminant); ⚠️ R-D11 correction = status FILLS are ground-relative → LIGHT-mode fills REOPENED; §1 manifestation decision sheet built; capture ritual gained **step 1b NARRATIVE DOSSIER**; Apollo Labs + whole-palette sweep + dual-observer principle + ~450 weight target registered in `_FUTURE-STATE`. Previous: **2026-07-19 (later) — "Small picks, and an edit-mode μX with legs"**: §1 `.num` RULED + enacted (T-D14 — `.t-cm-figure-3` 24/500 rung, countdown numeral bound via CLASS = first composite in markup, ASSERT-003 retired, build green 34 steps); §2 dv-017 visual built (`reviews/DV017-DELTA-VS-RAG-2026-07-19-v1`) awaiting Dave's wording confirm; μX in-context edit-mode prototype v1→v3 built + registered in `_FUTURE-STATE` (universal to all components · controls derived from meta · TIERED to the strict↔creative register, prompt-only at the creative extreme); review conventions inscribed (live variant/state spread + light/dark + responsive slider; versioning `-vN` not overwrite). Previous: **2026-07-19 late — "The button-label audit that became a gate": ds-005 GATED + CLOSED — new blocking descender-clip gate (`_validate_descender_clip.py`, build step 27/34); 7 truncating labels fixed with ZERO waivers; `.btn`/`.cta`/`.qbtn` audited CLEAN (null result); commit `3af1696`**. Previous: **2026-07-19 — "A gate for the blast radius"**: blast-radius gate built (closes open-001), h2 namespaced, specimen chrome harmonised, ds-005 logged, Tag atom (3 variants × 2 sizes) wired. Earlier: **2026-07-18 late** — R-D4 matting rungs ruled + first RAG role-token promotion. Earlier: **2026-07-18 Fable consolidation** — consolidated
1104 → ~450 lines per the classification Dave ruled via markup (11 pins) on
`reviews/CONSOLIDATION-AUDIT-2026-07-18.html`. Nothing deleted: ~580 lines relocated verbatim to
`_DECISION-HISTORY/`, duplicates reduced to pointers, two entries removed on their own recorded
instructions. Prior refresh: T-D12 ruling, commit `9fb1381`.*

## 🕓 OPEN — Latin Univers **WEBFONT**: waiting on brand (raised 2026-07-18, reframed same week)

> **DOWNGRADED from ⛔ BLOCKING to 🕓 WAITING.** Dave: *"the license will be renewed soon, it may well
> have been already, the webfont needed Ultralight added, I think this is only procedural, and low
> risk."* **The commercial judgement is his and recorded as made — do not re-litigate it.**

**Split the question in two. Only one half is about risk.**

**(1) LICENCE — procedural, pending, low-risk. Owner: BRAND, chased by Dave.** The renewal is in
flight; the delta is a *weight* (**Ultralight**) being added. Write **"renewal pending; Dave assesses
the gap as procedural and low-risk"** — never "we have no licence".

**(2) ASSETS — unchanged, and NOT a risk question.** Verified by inventory: **zero Latin
`.woff`/`.woff2` files exist in the repo** (five script packs present; Latin has none). A favourable
licence does not deliver files — shareable real-face material stays blocked until the pack physically
lands, because there is nothing to embed.

**✅ DISTRIBUTION — CLOSED, ruled "leave".** The four tracked files embedding base64 woff2 stay. No
`git rm --cached`, no BFG, no history rewrite. Repo is private (confirmed by Dave) and shared only to
HSBC employees — every recipient sits inside HSBC's own licence. Interim control retained:
`reviews/*CONTACT*.html` gitignored; share OUTSIDE HSBC as PDF only.

**WHAT CLEARS THIS:** (1) **files land** — `HSBC_MtUnivers_Latin-*.woff/.woff2` in
`knowledge/assets/fonts/` (this alone unblocks shareable material); (2) **brand confirms whether
Ultralight is in scope** — ⚠️ not a detail: the packs ship Th/Lt/Rg/Md/Bd ≡ 100/300/400/500/700, so
Ultralight is a **sixth weight below Thin → a change to the canon ramp → a TYPE RULING, not an asset
drop.** Expect it; don't discover it in a diff.

**Provenance corrections, kept loud (full record: `knowledge/_proforma/_TYPE-DECISIONS.md`
§ Blockers 1):** I struck this blocker as "false" and Dave caught it. And
`WebfontUserGuide-2024.pdf` is **generic Monotype guidance, not an entitlement record** — "we hold no
Latin webfont" rests on absence of files, not on any document.

## LIVE — current truth (in force)

### ⭐ TYPE and BOX are SEPARATE — T-D12, RULED + VERIFIED across 21 files (2026-07-18)
- **Two lists, two questions.** `.t-cm-<size>` = TYPE (family, size, weight, **`line-height:1`**) —
  **safe to bind anywhere.** `.t-cm-slot` = BOX (`display:inline-flex`, `align-items`, `min-height`,
  cap-trim) — **opt-in**, bound ONLY where the element already declares a flex display.
- **`--slot` carries the slot height on the type composite.** A custom property is inert unless read,
  so a type-only binding has no box consequence. That is what makes the two lists independent.
- **`line-height` is TYPE, not BOX** — Component tier *is* "single-line at line-height 1". This was
  not the question the queue asked and it is the one that decided the batch: with line-height in the
  box, type-only bindings silently DROPPED the `/1` the old shorthand carried.
- **Cap-trim reaches elements that lacked it, and the shift is ACCEPTED** — refusing it would leave
  two classes of button in canon.
- **The slot test stays conservative.** "Already declares flex" is the OBSERVED condition `.btn` met,
  not a theory. **Slotting anything else is a per-component decision with its own diff, never a
  mechanical sweep.** Widening it is a ruling.
- Evidence: 13/21 pixel-identical, 0 page-height changes, real HSBC Univers. Ledger:
  `_proforma/_TYPE-DECISIONS.md` **T-D12**; sheet `reviews/TYPE-BOX-SPLIT-2026-07-18.html`.
  Validation state: **unaudited**.
- **METHOD, reusable:** the `NO_SNAP=1` isolation control in `apply_type_bind.py` separated diffs the
  binding CAUSED from diffs T-D10 INTENDED. **A diff you cannot attribute is not evidence.** Reach for
  a control before reaching for a verdict.

### Type binding — RULED + PROVEN on one component (2026-07-18)
- **Mechanism = (d) selector-list extension, HAND-MAINTAINED.** A component binds by being appended
  to its composite's selector list in `canon/type.css`. Plain CSS: no generator, no build step, no
  markup change. `type-bindings.json` + orphan gate = an OPTIONAL later upgrade, **explicitly
  deferred — do not build**. Ledger: `_proforma/_TYPE-DECISIONS.md` T-D9.
- **`.t-cm` is variant D.** Cap-trim sits on the **ELEMENT**; the former required `.txt` child is
  **GONE**. `inline-flex` + `align-items:center` centres the cap box in a taller slot — an
  `inline-block` variant TOP-ALIGNS and is wrong. Observed in real HSBC Univers. Supersedes the
  07-17 composite.
- **⚠️ LOAD ORDER IS LOAD-BEARING.** `.t-cm-button` and `.btn` are both specificity 0-1-0 → source
  order decides. **`type.css` must load BEFORE component CSS.** Not yet gated.
- **Delivery = `<link>`, NOT inlining.** The portable unit is the PROJECT, not the file (Dave: *"the
  entire project must be portable… a package, pulled from a repo"*). The 49-file inline sweep was
  solving a problem that does not exist.
- **`type.css` is HAND-AUTHORED.** The "generated" header was false provenance; removed.
- **Bound so far: `.btn` (selector-list) + Countdown `.num` (CLASS).** **T-D14 (2026-07-19):** new rung
  `.t-cm-figure-3` (24px/500) added to the ramp; the countdown numeral is the **first composite bound in
  MARKUP** — via a class on the element, because bare `.num` can't go global (collides with `.cn-table td.num`).
  Zero-visual-change (500 = shipped value). **ASSERT-003 retired** (clears_when met). ⚠️ **The BULK binding
  mechanism for the remaining ~338 stays OPEN** — this was one collision-forced case, NOT a general ruling. Ledger: T-D14.
- **Unchanged from 07-17:** CSS cap-trim · 4px slot · slot min `ceil(cap + 2·descender)` snapped to
  4px · descender guard baked INTO the slot · stacks use `gap`, **never padding**.

### RAG — amber SOLVED, background/glyph split (2026-07-18)
- **Two tokens per hue: `background` (fills) + `glyph` (icons, arrows, text).** Red/green/blue hold
  the SAME value in both roles; **only amber diverges**. Ledger: `_proforma/_RAG-DECISIONS.md`.
- **`amber/background` = `#F0B13A`** — ink on it 9.16. **`amber/graphic` = `#C58900`** — 3.02 on
  white, 6.25 on `#111`; required by `{#dv-016}` (≥3:1 series fills, blocking).
- **Rule 1 — amber is always paired with black text. Rule 2 — amber is not a DIRECTIONAL delta
  colour**; it remains valid for status and tolerance.
- **White is the RAG text colour universally; dark-text variant DROPPED** (R-D1) — amber the sole
  exception, always was.
- **`#000000` retained in the KB as brand source of truth**; `#1A1A1A` = digital black for screens;
  `#1D1D1D` dropped; `#333333` canon, stays.
- **Incumbent RAG values NOT deleted** — retired into a future legacy theme. Tombstone, keep.
- **R-D4 (2026-07-18): matting rungs RULED — green + blue matted 15%** (`#2B7E4F` / `#306EC6`),
  red as-is, one level across both. **Role tokens PROMOTED** into `semantic-colour.json` as
  `rag/<hue>-background` + `rag/<hue>-glyph` (additive; incumbents untouched; zero components
  rebound yet — rebinding waits for the blast-radius gate). Green promoted **light-only**: the
  contrast gate refused the known-failing incumbent dark (3.37) — dark leaf lands with the
  dark-green ruling. Gate model gained `RULED_PAIR_EXCLUSIONS` (white text × amber fill is
  forbidden by rule 1, so the audit no longer tests it). Ledger: R-D4.
- **★ DARK SET LOCKED (2026-07-19, R-D5…R-D11).** Full arc: `_DECISION-HISTORY/2026-07-19-rag-colour-halation-ramp.md`.
  Dark-mode RAG (mode-stable for red/amber; per §note below for green/blue): **breach `#B92F1E` white ·
  watch `#F0B13A`/`#C58900` black · healthy `#43AD6F` black · info `#5F92B9` black** (cyan-shifted for
  astigmatic legibility). Weight uniform Medium 500. Marks icon/label-paired (never bare coloured text on
  dark). **Red = carve-out (deep+white, instability); amber = carve-out (lightness); green+blue = the
  isoluminant→RAMP-tuned pair.** Key rulings: R-D6 (halation = 3rd axis: bloom vs dance, thickness selects
  the mode; glyph-contrast-by-role) · R-D7 (red locked, weight polarity→uniform 500) · R-D9 (status colour
  is a SALIENCE RAMP, not isoluminant — loudness descends with severity) · R-D10 (set locked).
- **✅ LIGHT FILLS LOCKED (2026-07-19, R-D12…R-D14) — full set now reconciled.** R-D11 (fills are ground-relative)
  RESOLVED: **light green `#5DAC7B` · light blue `#7DABCD`** (H241, black text); dark stays R-D10 (`#43AD6F`/`#5F92B9`);
  red `#B92F1E`/white + amber `#F0B13A`/`#C58900` mode-stable. **NO lines** (R-D12 A, aesthetic); **black text on states**
  (R-D12 B). **Fill contrast = salience lever, NOT a floor** — the LABEL carries meaning (R-D6), so amber-soft-on-white is
  ruled fine (I over-raised it; Dave corrected). **★ Per-mode PROVEN, not asserted:** exhaustive search shows no single
  green/blue keeps green›blue on both grounds (loud=darker on white, lighter on dark). Reconciled table + arc: ledger
  R-D12…R-D14; sign-off `reviews/RAG-LIGHT-FILLS-2026-07-19-v9-LOCKED`; derivation `reviews/_rag_light_fills_calc.py`;
  ★ **two-mode in-browser TUNER** (v6→v7, OKLCh, ramp-guard) = Apollo Labs / Layer-2 controls candidate.
- **✅ FILLS PROMOTED (2026-07-19, this session).** R-D14 fills written to `semantic-colour.json` `*-background`
  + propagated to `canon.css`: light `#5DAC7B`/`#7DABCD`, dark `#43AD6F`/`#5F92B9`, breach `#B92F1E` now mode-stable,
  watch `#F0B13A`. `rag/text` polarity (white on breach, black on states — `type26-013`+R-D12 B) enacted via the
  **existing `RULED_PAIR_EXCLUSIONS`** (white×green/blue forbidden, like amber). Build green. **NOT rebound** — components
  render RAG as dots (glyphs, bind incumbents, R-D6 fine) + chips (tints); the `-background` fills await the §1
  manifestation pick. **Both amber rules still unenforced (gate owed).**
- **★ FOUR-THEME ARCHITECTURE — R-D15 (2026-07-19).** ONE token store + ONE baseline library, toggling **4 themes:
  Apollo Legacy · Mono · Console (UI) · Supercharge (SC)**. Components bind theme-agnostic roles; theme override sets
  supply the hex. **Apollo Legacy** alone carries the teals AND the HSBC brand `color/grey/100–800`. **The baseline we
  build now = Apollo Mono, "very mono": monochrome throughout, colour ONLY in RAG + data-vis.** Broader colour/theming
  build PARKED ("deal with colours later"). Ledger R-D15; memory `four-theme-architecture`.
- **★ Apollo Mono grey ramp = `color/mono/1…15`** (2026-07-19, R-D15). Dual-end brightness curve (γ=1.7, 15 stable
  index steps, black→white), packing resolution to both ends, thinning mid-greys; `#1A1A1A` = `mono/4`. Keys are index
  (theme-remappable); per-step brightness in the token `$description`. In `colour.json` + canon; build green. Tuner:
  `reviews/APOLLO-MONO-GREY-CURVE-2026-07-19-v2.html`. **Grey-tint standing check** (memory `feedback-grey-tint-check`):
  surface greys (`#333`=`grey/800`, `#767676`=`grey/600`) before changing — Dave usually rules black, but confirm.
- **★ Amount-display — P1 atom BUILT + gated (2026-07-19).** Money-format primitive: currency-before-no-space
  (copy-025), tabular figures, U+2212 sign, redacted privacy state. Snippet + `amount-display.meta.json` + review;
  monochrome (directional colour deferred to the colour workstream). Added figure rungs **`.t-cm-figure-4/5/6`**
  (32/16/14, all tabular) to `canon/type.css`; atom is fully composite-bound (no raw font). COMMITTED (conductor).
- **★ Digital black `#1A1A1A` = the new `#000`** (Dave 2026-07-19) — GENERAL, not just the reverse-text halation
  case. Swept all 38 components' dark grounds + `background/default` dark → `#1A1A1A` (shadows/overlays stay pure
  `#000`). COMMITTED. Expands [[neutral-blacks]]'s conditional framing; `#1A1A1A` = `mono/4`.
- **★ R-D16 — Mono semantic greys seated on `color/mono/*` — RULED, enactment PENDING.** Dave ruled on
  `reviews/APOLLO-MONO-SEMANTIC-GREYS-2026-07-19-v1`: text ink → `mono/4 #1A1A1A` (**★ SUPERSEDES `col25-011`**
  for Mono — Grey-8 stays Legacy) · **DROP** secondary text grey (hierarchy = weight/size, "very mono") ·
  `#767676`→`mono/8 #808080` · tinted `#D7D8D6`→`mono/12 #E1E1E1` · mechanical maps approved. **Enactment
  (Sonnet, queued):** write token values + sync the 38 component declarations + regen `canon.css` + re-gate;
  annotate `col25-011`/`colour-usage.md` with the Mono override. Ledger `_proforma/_RAG-DECISIONS.md` R-D16.

- **Project name = Apollo** (renamed from *Promenaut* repo-wide 2026-07-14; "Apollo" singular
  preferred, "Apollo SDS" acceptable). History: `_DECISION-HISTORY/2026-07-14-rename-and-restructure.md`.
- **Red rule = red is the PRIMARY-action accent, used ONCE per screen** (RULED Dave 2026-07-14) —
  **NOT destructive-only.** Destructive/error takes a distinct, non-red treatment. Supersedes the
  charter §4 register-tied ceiling → now universal. `BRAND-1` gate rewritten accordingly.
  **Propagation gap (OPEN):** historical fitness-test builds + proof-001 `_GATE2-REPORT.md` still
  state the old rule — regenerate if revived. Memory `apollo-rename-and-red-rule-2026-07-14`.
- **Designer pack = shipped-ready** (2026-07-14). `designer-skills-v1/` (4 skills + built KB,
  gitignored); handover artifact **`Apollo-designer-skills.zip`**. Delivery via VS Code + Copilot
  Agent Skills; no Python for v1. Intro ~the 20th; hands-on the 24th. **Untested:** live-fire on a
  designer's machine — top release risk.
- **Working model = land to the live repo as-you-go** (RULED 2026-07-14). Deliverables write straight
  to the connected repo; the `/tmp/ux` snapshot is stale — don't trust it. GitHub Desktop CLOSED
  during Claude commits. Memory `working-model-cloud-vs-device`.
- **Repo restructured for human-readability** (2026-07-14) — root = operating essentials; visual map
  `docs/repo-map.html`. History: `_DECISION-HISTORY/2026-07-14-rename-and-restructure.md`.

- **Component library = Apollo pro-forma programme, in flight.** ONE component skeleton, N modes —
  **Apollo mono** (monochrome base; *"pro-forma" = Apollo mono*) · **Apollo UI** (branded HSBC) ·
  **Apollo SC** (prior branded — "keep the ideas, don't copy the solutions"). **FOUNDATIONAL RULING
  (Dave 2026-07-15):** no hardcoded styling — everything tokenised, sibling libraries governed by
  MODES; enforced by DEF-003 (no JS motion) + DEF-004 (no raw px) in `_build_all.py`.
  **Tranches T1–T8 built + gated** in `knowledge/_proforma/` (interactive one-file-per-tranche);
  rules live in `_PROFORMA-RULES.md` (16 rules, incl. rule 16: every component ships Swiss dossier +
  KB model doc). Reviewable build list =
  `reviews/ITINERARY-2026-07-14-apollo-component-library.{html,xlsx}` (124 items; ~50 real base gaps;
  extend-not-restart). Memory [[proforma-programme]].
  History: `_DECISION-HISTORY/2026-07-15-proforma-tranche-arc.md`.
- **TYPE-TOKEN SYSTEM = PROMOTED TO CANON + grid enforced library-wide** (2026-07-17, Dave "crack
  on"): (1) primitives → `tokens/typography.json` + composites → `tokens/typography-composites.json`,
  `type.css` settled; (2) HSBC-general incumbent type+spacing parked as sibling sets — Apollo = the
  proposed HSBC standard, governed by modes; (3) **DEF-005** grid gate wired; (4) retrofit — 230
  off-grid snaps across canon.css + 38 snippets + 9 tranches; (5) vertical-stack rule drafted;
  (6) arrow asset RETIRED; (7) DEF-005 expanded to 50 files, all PASS. Rulings + WHY in
  `knowledge/_proforma/_TYPE-DECISIONS.md`.
  History: `_DECISION-HISTORY/2026-07-17-type-token-build.md`.
- **ATOMISE — build at the true atomic level, compose up** (RULED Dave 2026-07-14). Rolled-up
  patterns are a **debt**, not the model; build atoms → molecules → organisms per the `meta.schema`
  ladder. Known debt: decompose existing rolled-up molecules later. Applies to all new work.

- **Apollo product spine = "lovable on rails" · four phases** (Dave 2026-07-17; labels provisional,
  shape is the vision). **1 · Discover** (ingest/research; chat-to-KB bot likely here) ·
  **2 · Create** (being built now; four modes: **Strict** "Factory" · **Creative** · **Component
  Dev** · **Explore**) · **3 · Craft** (the review doc + comment overlay IS this phase) ·
  **4 · Dispatch** (hand to engineering; may fold away). **The four Create modes = TIERED LEVELS OF
  ADHERENCE** to the rails, guardrails progressively removed, per-tier sub-settings. **a11y (WCAG
  2.2 AA) IS the single non-removable floor** across every mode (per FOUNDATIONAL
  `accessibility-aspiration`) — "non-removable" = LOCKED, not HARDCODED: an **admin access layer**
  tunes every setting incl. the floor. **Apollo = the MOONSHOT** (name rationale). Memory
  `apollo-product-framing`. Unaudited — a framing, not a spec.
- **Product = a *flexing* engine** — one governed core, dials per work-type; floor/churn vs
  ceiling/novel. `ADR-0006`.
- **Output modes = a first-class dial** (Dave 2026-07-05): two fidelity tiers — portable dumb-HTML
  prototypes + build-ready from a prebuilt library, with **Sutherland** *a* target, not *the*
  architecture. Two-way tie: dark-mode work feeds INTO Sutherland; the Figma library IS Sutherland's
  working file. Memories `output-modes-portability`, `sutherland-figma-mapping`. Unaudited.
- **Register = an inference ramp** (NOT a look): sober = retrieve · balanced = extend · expressive =
  invent. Charter `_FIXED-FLEX-CHARTER.md` **§9**.
- **§9a — provenance of "reads HSBC"**: brand-ness resolves to named sources; flag-where-silent is
  advisory; residual gestalt = human. Record: `knowledge/_PROVENANCE-inference-levels_2026-07-04.md`.
- **Two harness modes** (§9a): converge/ship = mode B ADOPTED · explore/noodle = mode A OPEN. Memory
  `harness-two-modes`.
- **Project memory = temporal decision-graph pattern; this file is the cold-start spine.** `ADR-0007`.
- **Supersession discipline · git split · data hygiene** — canonical in `AGENTS.md` (tombstone +
  propagation log in the same pass; Claude commits in terminal, Dave pushes via GitHub Desktop only).
- **Build** — `python3 knowledge/_build_all.py` is the one command; the gate list lives in the script
  and in `GOOD-MORNING.md` §A. (This entry previously carried a third, drifted copy of the list.)
- **State machine records FUTURE/TARGET states too** (RULED 2026-07-05, extends ADR-0007): targets
  carry what · why · blockers · source; the staleness gate must flag a target whose blockers cleared.
  **Extended 2026-07-18:** the forward half now has its own home — **`_FUTURE-STATE.md`** (side-quests,
  ideas, resurrection candidates); in-flight TARGETS stay below. Unaudited node.

## SUPERSEDED / DEAD — do not build on

- `knowledge/_fitness-test/sme-payments-registers.html` — old looks-based register dial → superseded
  by charter §9 (2026-07-05). Tombstoned.
- Register-as-"described-look" — → superseded by §9 inference ramp (2026-07-03).
- Terminal-only push (07-02) — → superseded by the git split (07-05).
- `knowledge/_NEXT-SESSION.md` — retired → `GOOD-MORNING.md`.
- **`knowledge/_agent-memory/store/` — the memory mirror — DELETED 2026-07-18 (RULED Dave, via
  consolidation review pin 11).** It had become the third source of truth its own README forbids
  (115 stored vs 110 live, five ghosts, knowingly stale by three more). Final dated snapshot:
  **`_retired/agent-memory-snapshot-2026-07-18/`** (tombstone-bannered, non-authoritative, never
  refreshed). Capture-ritual step 3 amended: durable content is INSCRIBED properly (rules →
  guidelines/runbooks · checkable facts → assertions · rulings → ledgers), never photocopied.
  Propagation: runbook rewritten; snapshot README carries the tombstone; memory `capture-ritual`
  updated.
- **The "stale-reading pattern" spine note (07-18) — tombstoned 2026-07-18**, superseded by the
  **consult mechanism** (ruled via consolidation review pin 10): problem-domain index + pre-flight
  receipt, spec at `reviews/CONSOLIDATION-AUDIT-2026-07-18.html` §3, landing as
  `knowledge/_consult.py` + `_RUNBOOK-consult.md`. The bite-rule ("check the KB and the gates BEFORE
  designing") lives in `GOOD-MORNING.md` §A until the tool makes it mechanical.

## OPEN — propagation gaps + parked threads

### ✅ CLOSED (2026-07-19) — `gen_rules_index.py` truncation fixed
The `chunk[:500]` cap in `rule_text()` was cutting 11+ rules mid-sentence in `_RECONCILIATION.md` and making
their tails unsearchable in `_consult.py` (`icon-015` alone lost ~2300 chars). **Fix: cap removed** — the
walk-back already bounds `rule_text` to one bullet/paragraph, so full text now flows to both consumers.
Verified independently by the rules-index worker (465 rules intact, longest icon-015=2833, old-cap
fingerprint gone). Provenance comment in the generator so a cold session won't "restore" the cap. Receipt:
`notes/_receipts/2026-07-19-worker-rules-index-truncation.md`.

### ✅ CLOSED (2026-07-18) — the binding mechanism's BLAST RADIUS now has a gate
`_validate_type_blast_radius.py` (blocking, wired into `_build_all.py`) + registry
`canon/_type-bindings.json`. Bites on any UNREGISTERED / ESCAPED / UNWAIVED-BARE appended selector;
current debt registered + waived so it lands green. Full ruling + v1 limits: **T-D13** in
`_proforma/_TYPE-DECISIONS.md`. Residual DEBT to burn down (non-`/1` batch): namespace `h2` (25
files) then the scoped-element set — tracked there, not here.

### 🟠 OPEN — the non-`/1` batch, and why DEF-006 stays unwired
**61 non-`/1` font shorthands remain in `snippets/`**; the bulk of the remaining **690 TYPE-002** sit
in the pro-forma tranches, carrying line-heights 1.1–1.6 — binding REPLACES them with canon and
**things move**. Needs its own reviewed batch with T-D12's before/after pixel discipline.
**DEF-006 is 780 → 729 and stays UNWIRED until this lands** — wiring it earlier trains everyone to
ignore a red build.

### Awaiting Dave — small, no analysis needed
- ~~Matting rung for green + blue~~ — **RULED R-D4 (2026-07-18): both matted 15%** (`#2B7E4F` /
  `#306EC6`), red as-is; role tokens promoted (see LIVE → RAG). Rung came from a direct readback —
  the pin export named the hue, not the row (the overlay row-identity debt biting again).
- ~~**`{#dv-017}`(a) CONTRADICTION**~~ **RESOLVED R-D5 (2026-07-19): split the clause** — directional deltas
  red/green ONLY; RAG status a separate concern (R-D3). Enacted in `data-visualisation.md`.
- ~~**★ RAG light-mode FILLS — REOPENED (R-D11)**~~ **RESOLVED + LOCKED 2026-07-19 (R-D14).** Light green `#5DAC7B` /
  blue `#7DABCD` (H241), dark stays R-D10; per-mode proven. See LIVE → RAG. **Only open piece: the token promotion**
  (`rag/*` per-mode + rebind behind the blast-radius gate) — Sonnet-appropriate, deferred.
- **§1 RAG manifestation — OPEN.** Which forms are canon: Status-indicator dot+label (existing canon) · filled
  cell/badge · bar/edge; tags+pills EXCLUDED by canon (ctkt). Decision sheet built
  (`reviews/RAG-STATUS-MANIFESTATION-2026-07-19-v1`), awaiting Dave's canon pick (A / A+B / A+B+C). Then a
  Sonnet build: rebind Status-indicator to R-D10, spec cell/bar as gated components (cells need more vertical padding).
- ~~**`.tag` COLLISION**~~ **RESOLVED 2026-07-18.** Was three things under one name: the tag component
  (14px), a smaller reuse (12px), and a masthead descriptor `.h .tag`. Ruled (Dave): tag atom = 3
  variants (dismissible/bordered/plain) × 2 sizes (`.tag`/`.tag--sm`), `.tag--plain` for borderless;
  colour/RAG deferred. Masthead descriptor renamed `.h .tag` → `.h .subtitle` (specimen chrome, not a
  component). Live Tags descender clip fixed via ds-005. Specimen: `reviews/TAG-COMPONENT-2026-07-18`.
  **ds-005 now GATED + CLOSED (07-19):** `_validate_descender_clip.py` (step 27/34) forces
  `text-box-edge:text text` on every truncating label; the button follow-on audit found `.btn`/`.cta`/`.qbtn`
  CLEAN (they never truncate — null result), the real debt was 7 labels in Tranche-2/3/4/7/8 + Masthead
  `.dd-title`/`.navitem-tx`, all fixed zero-waivers. Removing an override now reds the build.
- ~~**`.num` at 24px**~~ **RULED T-D14 (2026-07-19):** added `.t-cm-figure-3` (24/500) to the ramp;
  countdown numeral bound via class; build green (34 steps). Multi-size 20/24/32 lands with countdown size variants.
- **Family A (reverse on near-black), 12 decls** — held at 500. Re-specimen on a FULL dark surface.

### Gates owed — rules that exist but do not bite
- **Amber rules 1 + 2** (R-D3) · **type.css load order** · **DEF-006** (see above) · dark-mode green
  `#1AA05C` 3.37 · dark-mode red/blue as TEXT glyphs on `#111` (3.97 / 4.15).

### ⚠️ METHOD DEBT — the review overlay loses row identity
Three sheets needed three different disambiguation routes; one (RAG-MATTING) is unresolvable. **The
overlay should capture which row a comment is pinned to.** A PRODUCT fix, not a process workaround —
registered against the review-layer-as-product thread (and `_FUTURE-STATE.md` feature ideas).

- **🔴 GAP (2026-07-17, measured) — the library does NOT use the canon type ramp.** Type was promoted
  and the *grid* retrofit ran, but components were never rebound: **0 of 50** files reference a
  `.t-cm-*`/`.t-ed-*` composite; raw font declarations remain everywhere (canon.css 113, T8 43, T1
  25, T6 23…). **THE TYPE RETROFIT (sibling to the grid retrofit) — NOT STARTED:** (1) components
  link/inline `type.css`; (2) rebind every text declaration — Component for single-line, Editorial
  for wrapping prose (the N1 caveat decides); (3) snap off-ramp sizes; (4) wire
  `_validate_type_composites.py` into the build (Dave: *"we need to hard wire this"*).
  ⚠️ `canon.css` is GENERATED from snippets between the AUTO markers — edit snippets and regenerate,
  never hand-retype. Scope ≈ the grid retrofit; needs a fresh session.
- **✅ Icon SOURCE canvas normalised to 18×18** (2026-07-17, ruled option A — fix the assets, we own
  the library). Library now **652 × 18×18** + 6 deliberate non-square utility marks; build green;
  renders identical. History: `_DECISION-HISTORY/2026-07-17-type-token-build.md`.
- **🔵 SCHEDULED (Dave 2026-07-17) — ICON SCALE onto the 4px grid** (step 0 above done). Icon render
  sizes were never snapped and DEF-005's square-exemption can't see them. Measured: ~56 usages
  on-grid, **~50 OFF** (18px ×20, 14px ×14, 22px ×7, 26/34/11/15/10 tail). **The work:**
  (1) sanctioned icon scale on 4px = **12/16/20/24/32/36/40/44** (36·40·44 added by Dave — 44 = WCAG
  target-size floor); rule the mapping per off-grid size **against renders, not on paper** (Dave's
  call — optical weight); (2) **tie icon box → the type grid-slot** (icon beside a label takes the
  SAME slot — the rule that makes the scale self-evident); (3) source-artwork caveat: the ~71
  non-square assets need a `preserveAspectRatio`/pad-to-square ruling; (4) gate it — narrow DEF-005's
  exemption or add `_validate_icon_scale.py`; (5) retrofit the ~50, re-render. NOT started.

- **🟢 RULE 16 (2026-07-16) — component documentation is part of "done":** Swiss dossier in
  `reviews/` + graph-connected KB model doc in `_proforma/` (typed `relations:`). FIRM going forward.
  Exemplar: the Masthead pair. **Backlog (Dave "we might have to go back"):** retrofit docs for
  T1–T7; stand up the Swiss component catalog ("nicer Storybook") as their shared home.
- **🟡 PARKED — round-one DataViz kit BUILT + reviewed, "good enough for now", NOT signed off**
  (RULED Dave 2026-07-16). Gate-first: `_validate_dataviz.py` (9 blocking + 5 advisory) wired; whole
  kit on `knowledge/_proforma/DataViz-interactive.html`; **nine review rounds enacted** — ledger
  `knowledge/_proforma/_DATAVIZ-DECISIONS.md` (read before touching charts). **REVISIT target, not
  DONE:** Dave will add Layer-2 interaction controls (filtering, chart titles…) and finish sign-off.
  Interactivity never render-checked in a browser by Dave — needs his in-browser pass. Staleness:
  flip to DONE only on his sign-off.
- **DataViz foundations — RATIFIED + PROMOTED (2026-07-16):** method dossier ratified (semantic SVG +
  tokens + CSS motion + hidden-table spine; canvas rejected); **V7 promoted into
  `semantic-colour.json`**: `data/series/1–5` (C, mode-stable) · `data/series-high-contrast/1–5` (A,
  per-chart rebind) · `data/delta/{gain,loss,neutral,warning}` (D2, value-split pairs); **`{#dv-019}`
  recorded** (scoped gain/loss exception + the vibrating-boundaries rule, thresholds 1.25 / 135° /
  0.5 adopted advisory — quantified because Dave OBSERVED the dance on a 146° pair); suggestion
  ranges stay `proposed` in `tokens/_proposals/dataviz-ranges.proposals.json`. **NEXT = round-one kit
  revisit** per the parked entry above. Dossier: `reviews/DATAVIZ-METHOD-2026-07-16.html`.
  History (the rev 1→3 arc): `_DECISION-HISTORY/2026-07-16-dataviz-v7-arc.md`. Presentation
  candidate: see `_FUTURE-STATE.md`.
- **🟢 Masthead — SHIPPED as an MLP** (review complete, Dave "done at last", 2026-07-16; MLP status
  ruled 2026-07-18). `knowledge/_proforma/Masthead-interactive.html`: one `.masthead`, 3 recipes
  (L1 exposed · L1 + mega · Trigger mega), drill-down drawer variant, all gates green. Supersedes the
  T7 `gheader` + `mm-masthead` demos. Two provisional glyphs (`i-brand-apollo` crescent,
  `i-menu-search`) await real assets — `knowledge/_ICON-GAPS.md`. Design revisit possible later.
  History (six review rounds): `_DECISION-HISTORY/2026-07-16-masthead-rounds.md`.
- **⚠️ PROPAGATION GAP (partially closed):** `ADR-0006` + `notes/_VISION-iteration-machine_2026-07-03.html`
  still speak the OLD looks-language ("cool/warm/hot register switch"; the mock has a
  `border-radius:10px` cardinal violation). `_TEST-BRIEF-v2` §2 was reconciled 07-05; the vision doc
  + ADR-0006 remain open — do when next in that area.

- **Worked spread — DONE 2026-07-05, two instances (Sonnet + Opus re-run).** First
  retrieve/extend/invent spread; cardinal curbs held; Dave found two real gaps, fixed same session
  (canon rigour tier `.cn-*` > `.c-*`; Opus re-run). Writeups in
  `knowledge/_fitness-test/register-spread-2026-07-05*/`. Still not "proven" — one screen.
  History: `_DECISION-HISTORY/2026-07-05-register-spread-and-restyle.md`.
- **🟠 GENERATION SHAPE — RULED (Dave, 2026-07-10): rule-tuning + inference tiering LEAD; the
  double-pass is a component, not the architecture.** The two-pass restyle was "not all that
  successful" — an interesting hypothesis, no more. Future state affirmed: **strict mode over a full
  component suite for the "factory"**. The trace tool (`knowledge/_trace_knowledge_usage.py`) showed
  governed output is already PURE-RETRIEVAL — tuning must change *what the rules ask for*, not
  adherence. **ROOT CAUSE of flat layouts: the library stops at organism — ZERO templates/shells** —
  the layout-governance gap and the library-tier gap are the SAME gap ([[library-composition-tier-gap]]).
  **OPEN DECISION F7:** build-upfront vs cluster-compound. **Working plan (agreed direction):**
  housecleaning → gap-analysis targets across three tiers (templates/shells = the load-bearing zero
  tier) → prove the loop on ONE cluster → build the template tier + compose gate → scale compounding.
  Full chain + all three hypotheses: `_DECISION-HISTORY/2026-07-07-s9-root-cause-and-ruling.md` +
  `knowledge/_FINDINGS-s9-session-2026-07-07.md`. Deep review:
  `reviews/REVIEW-2026-07-10-deep-analysis_rev2.html`. Memory [[ruling-generation-shape-2026-07-10]].
  **RESURRECT:** the experiment lineage is future evaluation material once the factory has all its
  parts (Dave, 2026-07-18) — registered in `_FUTURE-STATE.md`.
- **Named-not-built harness machinery** (§9/§9a): isolated generation · divergence probe (formal
  tooling) · mode-B brand self-check · the mode dial.
- **PM-KG MVP** (`ADR-0007`): `_build_live_state.py` + the staleness gate + `_capture_gate.py` — own
  focused session.
- **✅ Decision-corpus audit — TIER A CLEAN 2026-07-05** (ADR-0007 §5; method
  `_RUNBOOK-decision-audit.md`; ledger `_DECISION-AUDIT.md` — per-batch verdicts live there).
  Milestone: every Tier A node has a verdict — retires the "everything is unaudited" risk for
  foundational nodes. **Standing follow-ups:** §9 proof-obligation · ADR-0003 KG/ingestion · §4
  language-strip · TOV content audit · harness-modes exploration · re-audit the two amended nodes
  (ADR-0006, `derivation-governance` — amended text re-enters `unaudited`) · staged-promotion /
  extension-library process (direction VOUCHED, mechanism DEFERRED; tiered-access feature idea →
  `_FUTURE-STATE.md`). Next: Tier B opportunistically, Tier C by sample/on-touch. Never in a loaded
  session.
- **⭐ Harness modes + dials exploration** (from the 07-05 defer): flexible to a degree — clean
  switch or toggle + advanced mode, maybe "let it rip"; **finding the use cases is the important
  part**; research + iterate, start small. Own thread. Memory `harness-two-modes`.
- **⭐ TOV = digital-editorial spin-off + future content audit** (§4b defer): genuinely useful for
  DIGITAL EDITORIAL — candidate spin-off; for interfaces NOT a priority except neutral decisions
  (labelling, locale, formality). Memory `tone-of-voice-ingest`.
- **⭐ Charter §4 language-strip (HARD follow-up):** strip §4's interpretive prose
  (recall-by-adjective), leaving the four curbs as KG-sourced derivations — **do inside the
  unified-KG/ingestion thread, not standalone.** Amended text re-enters `unaudited`.
- **⭐ Unified DS knowledge-graph + ingestion, done right** (from ADR-0003 defer). The whole corpus is
  one interlinked graph; today that lives only in the compliance index. **Design direction (Dave,
  2026-07-10):** the compliance "KG" is an inverted index, fine for its job, wrong for the roadmap.
  When taken up: (1) **NOT GraphRAG** — overlay/property graph over existing stores, edge layer
  derived + regenerable, no monolith; (2) granularity = typed EDGES, not finer text (split only
  bundled rules — ACT atomic-vs-composite); (3) **import** the SC↔rule leg (ACT Rules Format 1.1 +
  axe-core metadata), hand-curate only component↔SC (our genuine novelty); (4) type edges
  `applies_to` vs `verified_by` — the queryable form of "enforced vs asserted"; (5) keep structural
  graph separate from advisory retrieval-over-prose. **Sequencing:** rides with the layout/library
  tier (R4) + Ingestion Phase 3 — not standalone infra. Cheap-now slice: type existing edges + import
  ACT. Memory `ds-knowledge-graph-revisit`. Unaudited.
- **Seaworthiness plan — DONE 2026-07-05** → `notes/_SEAWORTHINESS-PLAN_2026-07-05.md` (the
  dependency-aware sequence; partly overtaken by the pro-forma pivot). Phase 0 ingestion-tracking
  hygiene CLOSED same date. History: `_DECISION-HISTORY/2026-07-05-register-spread-and-restyle.md`.
- **D2 — novel-screen test — THE #1 unlock.** Waiting on a colleague's brief (their brief-v2 + own
  baseline + signed contract *before* generation). `notes/_TEST-PLAN-novel-screen-proof.md`.
- **Toolkit tranche 2** (Dropdowns ×4) — parallel cheap-model workstream. Memory
  `common-toolkit-survey`.

## PLANNED / TARGET STATES — in-flight targets (per the ADR-0007 extension)

*Intended end-states with a path. Ideas not yet in flight live in **`_FUTURE-STATE.md`**.*

- **🎯 Full consolidated review page (Apollo Mono baseline)** — Dave reviews the whole Mono baseline in **ONE
  big review page when the build-out is "done"**, not piecemeal (*"I just need to get this nailed"*, 2026-07-19).
  Running backlog + method: `knowledge/_REVIEW-SIGNOFF.md` top block. Covers T1–T9 as they render post-tokenise,
  the tokenise deltas (divider `#3A3A3A→#808080` · blue focus · near-white primary), and the open decisions
  (mono primary-action token · success mono-vs-teal · focus blue-vs-mono) + DataViz sign-off + T9 first review.
  Memory `full-review-pending`.

- **🎯 Gates-as-a-service → close the agentic loop** (Dave 2026-07-14). Expose Apollo's validators as
  callable tools (MCP) so a host agent runs them mid-task (generate → check → fix → re-check) — the
  verifier is the expensive, differentiated half, already built. Removes the per-designer Python
  blocker. *Honesty:* the repair loop is not built; gates verify DECLARED obligations only. Memory
  `agentic-loop-gates-as-service`. Unaudited.
- **🎯 Chat-to-the-KB bot** (Dave 2026-07-17). Conversational agent over the Apollo KB (canon ·
  criteria · rulings · decision graph) for designers/devs/stakeholders. Open: retrieval grounding +
  citations, scope, surface, guardrails. **The consult index (2026-07-18) is its seed — same index,
  read side built once, used twice.** Memory `chat-to-kb-bot`. Unaudited.
- **🎯 Ingestion "done right"** — full detail: `knowledge/_INGESTION-ASSESSMENT_2026-07-05.md`
  (cockroach doc). Target: every ingested entity addressable in one overlay graph; tokens
  Sutherland-canonical, 147 deprecates retired; completeness = edge coverage. Sutherland export is NO
  LONGER a blocker (arrived 06-17). Path: Phase 1 token migration → Phase 2 finish guidelines →
  Phase 3 overlay graph (= the 07-10 KG design direction above) → Phase 4 wire coverage into this
  machine.

## SPIN-OFF / GENERALISABLE CANDIDATES — surface, don't bury (Dave, 2026-07-05)

*Tools/methods that may generalise — treat like company spin-offs. Surface mid-chat; don't force it.
Memory `spin-off-candidates`. Sibling register for ideas/side-quests: `_FUTURE-STATE.md`.*

- **🌱 The state machine** (`_LIVE-STATE` + `_FUTURE-STATE` + `_DECISION-HISTORY` + decision-audit
  method) — **Dave's first named candidate.** A portable "how a long-running agent project retains
  state, records supersession, and audits its own decisions" kit.
- **🌱 The FONT AUDIT instrument** (2026-07-18, `reviews/gen_univers_dossier.py` + fontTools passes):
  answers "is this face tight or loose relative to its own stroke weight; is our commissioned cut
  actually stock?" with numbers. Settled in ten minutes a weeks-open question and relocated a defect
  to the foundry (ds-004). Unruled; embedded in a dossier generator, would need extracting.
- **🌱 REAL-FONT EMBEDDING for review sheets** (2026-07-18, `embed_fonts()` in
  `gen_tracking_contact_sheet.py`): base64 woff2 inlining so specimens render in the brand face
  anywhere. Retired the "judge on your screen" caveat. **Candidate to fold into `_make_review.py`.**
- Other candidates (unruled): decision-audit runbook · fixed/flex charter pattern ·
  ingestion→overlay-KG method · review-dossier language-review instrument ·
  verification=enforcement gate-tiering · the cockroach-doc pattern. Precedent:
  `digital-experience-transformation`, `graphify-tool`.

- **Capture ritual** — canonical at `knowledge/_RUNBOOK-capture-ritual.md`; run every session, no
  exceptions. The enforcing `_capture_gate.py` is deferred to the PM-KG MVP.
