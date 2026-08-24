# Sub brief — logos into the library (#217, Opus build sub)

**Dave's lane, his words (#216):** *"sort out the logos and photography and get them into the library"*. This sub owns the LOGOS half.

## Context (verified this session)
- `knowledge/assets/logos/` — 12 brand SVGs + `_export-logos.py` (read it first: it is the existing machinery and may already encode naming/variant intent). Variants: hexagon / masterbrand / masterbrand-identifier × light/dark × colour/mono.
- The crescent is an **Apollo-only** brand mark — if you encounter it, that constraint is standing; surface, never widen.

## Scope (your regions)
1. **SURVEY FIRST** — `s215-D5`: library v2 REPLACED `showroom/index.html`. Grep for the live library structure and how existing asset/foundation sections are presented before authoring anything. Copy an approved page as the starting reference, never re-draw [[specimen-starts-from-reference]].
2. **Mint a Logos library section/page**: all 12 variants presented on correct grounds (dark variants on dark, light on light — never a dark logo floated on white to "show" it), colour + mono side by side, filenames visible, usage notes limited to what existing canon/ADRs already say. Test PER THEME — four themes is the requirement, and light+dark both.
3. **Type + colour discipline**: `.t-cm-*`/`.t-ed-*` composites are FIRM; two-red law and the mono error-ink camp are settled — do not restyle anything to taste.
4. **Render-proof**: read `knowledge/_RUNBOOK-render-verify.md` before rendering (fresh sandbox — chromium libs likely absent; re-extract recipe is stratum four). `set_content()` BANNED; `goto("file://…")` only. Chunk anything near 45s wall.
5. **Rows**: sign-off row in `knowledge/_REVIEW-SIGNOFF.md` (AWAITING Dave), store row for each new document at creation, DS defects to `knowledge/_DS-IMPROVEMENTS.md` by addition.
6. If minting touches any canon generator: the regen serial set is ORDERED — run the WHOLE serial per wave, ramp first, index last. Prefer NOT touching generators at all; a standalone library page is the expected shape.

## DO-NOT-RULE (hard fence)
- `knowledge/_rulings.json` READ-ONLY.
- No logo usage POLICY authoring (clearspace rules, minimum sizes, co-branding) — present what exists; policy is Dave's.
- No renaming or editing the SVGs themselves; no new derived logo variants.
- No token, theme, gauge, threshold, lane, or worklist edits.
- Do NOT commit or push; do NOT git-checkout/reset.

## Pitfalls to carry (mandatory replay, Dave #165)
- (a) SVGs may carry hardcoded fills that fight theme grounds — MEASURE (grep the fills) and report; do not "fix" them, that is a policy call.
- (b) A page that passes in one theme proves one theme — the four-theme spread is the deliverable, screenshots per theme.
- (c) Dangling var class: any `--*` you reference must resolve in ALL themes — an undefined var renders silent black and no gate catches it.
- (d) Version, don't overwrite: `-vN`; sandbox cannot rm (use mv).

## Report back (replayed in-window)
Paths built · per-theme render evidence · hardcoded-fill findings · rows added · residuals declared · what a failed probe would invalidate · token spend.
