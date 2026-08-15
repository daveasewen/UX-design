# Brief — s176 step-tracker success-system enactment, FOR DAVE'S EYE (2026-08-14, v1)

Conductor: #176. ONE Opus build sub. Dave has given a WORKING ruling (firm in intent, to be ratified by eye — nothing is inscribed yet). Build it, prove it, render it for review. Do not commit.

## Dave's words (verbatim, this session)

"I think we should exactly the same system that we use for the success roundels on all, they can just inherit then wholesale. Except Legacy, it uses the red in light mode and white in dark." — and on the Legacy bar ink question + the s175 supersession: "both are true, lets see it first."

## What to enact (working, uncommitted)

1. **`step/complete` aliases the success-roundel system.** In the base store, `step/complete` → `$alias` `rag/success` (the roundel fill rung; verify which rung the roundel policy actually binds — `--success` resolves via `--rag-success` → `rag/success-glyph` in base; match the ROUNDEL's chain exactly, don't guess). Result per theme (VERIFY by resolution, report chains): Mono #66CC8D mode-invariant · Console/SC #5DAC7B mode-invariant · Legacy would inherit teal #00847F — which is why (2) exists.
2. **Legacy exception:** `step/complete` override = **#A8000B light / #FFFFFF dark** (the Legacy ERROR status red — Dave first said "the red", then corrected via "warning red" to, verbatim, "Legacy error, sorry my mistake". NOT brand #DB0011, NOT amber #FFBB33). This supersedes the s175-D1 #DB0011-both-modes shipped values — preserve the old values + provenance in the $note by addition (Dave: "both are true", supersession by his word). Do not delete the s175-D1 note text.
3. **Marks knock to page:** completed-step check glyphs follow the roundel policy (`--mark: var(--page)` shape=colour mark-knocks-to-page), replacing any white-fixed mark. Apply to Progress-tracker + Stepper, including the collapsed-bar responsive state.
4. **Legacy bar ink fall-through:** Legacy declares an explicit `progress/complete` override = **#333333 light / #FFFFFF dark** (s176-D1 Legacy ink; dark unchanged from base white). DECLARE it with a $note naming the fall-through class — a theme meaning a value must declare it.
5. Rebind/regenerate through generators only (gen_theme_cascade, gen_canon_tokens, gen_canon_components, gen_showroom as needed). ⚠ `--step-complete` currently paints NOTHING in Mono/Console (no :root definition) and the flattened per-theme literals outrank the token — fix the WIRING so the token is actually consumed at the address that paints (this was measured by the previous sub; its finding is in `_BRIEF-s176-step-colour-controller-2026-08-14-v1.md`'s output page if you need detail).

## Prove it

- Contrast, measured, every cell: step fill on page + fill on track + mark on fill, all four themes × light/dark, wide + collapsed. Flag any <3:1 non-text plainly — REPORT, never block or "fix" with a value change.
- Selftest: extend gen_theme_cascade selftest to assert the NEW values (values not absences), mutation-tested (break each, see red, restore, see green). The existing legacy/SC step clauses assert the OLD reds — retarget them (subject moved), preserving provenance in comments.
- Gates rc=0 before/after, rc captured directly: snippet · a11y · radius --strict · coverage · icon · all five --check generators · theme-cascade --selftest. Ratchet stays ≤1101. No _build_all.py.

## Render for Dave's eye

`reviews/STEP-SUCCESS-SYSTEM-2026-08-14-v1.html` — live specimens (real snippets + regenerated canon.css), all four themes × light/dark, Progress-tracker + Stepper + collapsed bar + the Legacy Progress-bar (#333333 light) alongside. BEFORE/AFTER pairs per cell (before = HEAD canon.css via git show, after = working tree). Contrast printed per cell. Plain prose labels, no ID codes. Render-verify per `knowledge/_RUNBOOK-render-verify.md` (goto file://, canvas font probe, /var/tmp, session-suffixed scratch names — /var/tmp collides across sessions).

## ⛔ DO NOT

Commit · touch `_rulings.json`/`_state.json`/MEMORY/wrap machinery · run _build_all.py · rule anything beyond enacting the above as WORKING · change any success/RAG value itself · touch s151-D1/s149-D1 surfaces · reformat files (byte-minimal diffs; JSON round-trip clean outside edits) · touch `step/incomplete` values (wiring only if needed to paint).

## Pitfalls replayed

Token NAME ≠ ADDRESS (SC warm rebind; the flattening) · rc through a pipe = the pipe's · green that can't fail = assertion (hence mutations) · ~45s call wall, chunk · a filtered state-contrast run rewrites the whole tracked audit — if you run it filtered, restore byte-identical · gen_showroom payloads stale silently when snippets change — regenerate and --check.

## Report back

Files touched + hunk attribution per generator region · resolution chains · contrast table · mutation receipts · gate rc table before/after · render receipts (what you SAW, both modes) · friction log · NOT DONE / NOT RULED list.

Repo (bash): /sessions/upbeat-nifty-mayer/mnt/UX-design
