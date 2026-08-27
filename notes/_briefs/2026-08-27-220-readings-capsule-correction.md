# #220 sub brief — the capsule-chord correction READINGS page (build, NO enactment)

**Model: Opus. Budget: sub spend is QUOTA and today quota is use-it-or-lose-it — be thorough, never frugal. FILL discipline inside your own window still applies.**

## Mission
Dave rejected one card on `showroom/_foundations/bento-rails.html` — "Capsule — White" — with:
> "almost right, this would never exist. its ether cohesive capsule or rounded full image if there is no background colour on the caption."

(Receipt: `notes/_receipts/2026-08-25-219-role-defaults-exports.md` § PARKED CORRECTION.)

His sentence supports THREE distinct enactments. Per the ruled practice (an ambiguous VISUAL ruling is rendered as readings side by side; he points; we never build the likeliest), build **`reviews/CORRECTION-READINGS-2026-08-27-v1.html`** showing all three readings LIVE, console theme, light AND dark, each rendered from COPIED artefact markup — never re-drawn.

## The three readings (defined by the conductor — do not invent a fourth, do not drop one)
- **READING A — White leaves the capsule ramp (the receipt's own reading, unconditional).** The console-gallery capsule chord's caption grounds become grey · darkgrey only. A white/ground-less caption is served by chord two (rounded full image + transparent caption). Show: the surviving capsule cards, and "where white captions went" — the chord-two form.
- **READING B — White is fenced, not removed (conditional exclusion).** White stays on the ramp; a widened X1-class exclusion refuses capsule+white only when the ground beneath (pageBg/bentoBg) is itself white/page. Show: white capsule ON a grey page ground (legal under B, gone under A), and the white-on-white pairing rendered as REFUSED by the validator.
- **READING C — Ground-less captions re-form the tile (structural).** When capBg is none/transparent, the tile must take one of exactly two forms: cohesive capsule (caption clipped inside the one capsule with the image) or rounded full image (image rounded, caption bare beneath). Show: both legal forms plus the current broken form (half-capsule image + invisible caption strip) labelled as the thing he said would never exist.

## Method — copy, never re-draw
1. Read `knowledge/_RUNBOOK-render-verify.md` FIRST (read the runbook, not the hook). Sandbox note: nothing survives a tool-call boundary; drive render steps individually; `goto("file://…")`, never `set_content()`.
2. COPY the `.br-card` / `.bm-stage` markup and its CSS from `showroom/_foundations/bento-rails.html` (the approved artefact). The `git checkout` route is BANNED; read the live file. Reuse its real photograph tiles.
3. Page top: the BEFORE — the rejected card rendered live — with Dave's words verbatim beside it.
4. Labels in PLAIN PROSE (Dave rules by eye and words; ruling IDs only as small-print provenance). One line on the page: mono's access to the dark-caption chord is EXPRESSLY OPEN (s219-D3(3)/X6) and is NOT decided by this page.
5. Page footer: name the enactment site so the enact wave is priced — `knowledge/_render/gen_bento_matrix_217.py --rails` (the manifest is GENERATED; a hand edit of `_bento_edit_rails.json` is a RED) + `gen_foundations_217.py`.
6. Colour law: two-red law and mono error ink camp are UNTOUCHED. Type composites `.t-cm-*`/`.t-ed-*` only.

## DO-NOT-RULE / DO-NOT-TOUCH
- NO enactment: do not edit `_bento_edit_rails.json`, any generator, any showroom page, `knowledge/_rulings.json` (only `_inscribe_ruling.py` ever writes it, and not you), `knowledge/_state.json`, memory, git (no add/commit/push — conductor commits).
- Regions you own: `reviews/CORRECTION-READINGS-2026-08-27-v1.html` + your filed report. Nothing else. You run NO generator that writes outside these (name any generator you run and the regions it owns BEFORE running it; `_capture_gate.py --selftest` writes `knowledge/_CAPTURE-GATE.md` — do not run it).
- Version-don't-overwrite: `-v1` filename; sandbox cannot rm (use mv).

## Pitfalls / consequences (mandatory, Dave #165)
- A hand-rolled specimen invents defects — copying the artefact is the whole method.
- A readings page that renders only the likeliest reading re-creates the defect this page exists to prevent.
- Fonts: canvas probe, not `fonts.check()`; ENOSPC → `/var/tmp`.
- If a reading cannot be rendered honestly, say UNPROVEN in the report — never fake a specimen.

## Report
FILE the full report at `notes/_subreports/2026-08-27-220-readings-capsule.md` with a `COUNTS:` line, a `RULING-SHAPED QUESTIONS` section (questions are Dave's, never your rulings) and a `REPLAY-THESE` section. Chat gets a STUB (≤6 lines): deliverable path, counts, red flags.
