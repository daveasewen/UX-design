# 2026-07-22 — The theming clean-room: ADR-0014, the neutral DNA tier, and the warm ramp

*Session: "Apollo theming clean-room [FABLE solo]" (2026-07-22, morning→midday BST). Spine entry:
`_LIVE-STATE.md` 2026-07-22 delta. Records: `docs/decisions/ADR-0014-per-theme-neutral-primitives-state-snap.md`,
`_proforma/_RAG-DECISIONS.md` R-D25. Review sheet: `reviews/SC-DARK-MODE-2026-07-22-v1.html`. This dossier
holds the WHY and HOW; the ledgers hold the what.*

## The arc

**1. The survey corrected the handoff before any design.** GOOD-MORNING said the tabs ruling was
"NOT yet inscribed" and rulings 2+3 still owed — but the ledger already carried **R-D23 AND R-D24**
(the morning Opus commit `06d3378` landed them in the same commit as the handoff that denied it).
Only ruling 3 (pro-forma fold-or-keep) was actually owed. Lesson repeated: the handoff is a
Polaroid; the ledger is the tattoo — read the ledger. The survey also found the cascade
**selftest stale-RED** (still asserting "Supercharge must be EMPTY", pre-R-D22) — it never ran in
the build, only `--check` did. Selftests that don't run, rot: they are now build steps (42→45).

**2. The Figma pull was archaeology, not API.** The brief's node range was right but the swatches
are raw VECTORS (no bound variables — `get_variable_defs` = `{}`; page metadata overflowed the
transport). The route that worked: the MCP asset URL for each vector returns the **SVG source with
the fill inline** — 15 fetches, grep the path fill, done. Self-verification was strong: monotonic
luminance along the row, warm cast peaking mid-low exactly as Dave described, and **step 2 =
`#13110E` = the ink he'd already quoted** — the brief's ink was a ramp step before we knew the ramp.
Two stumbles worth recording: I first treated swatch 1 as "a black illustration vector" (it was
step 1 of the ramp), and I grepped the SVG root's `fill="none"` before the path's.

**3. The design move was recognising the house pattern.** Per-theme neutral ramps could have been
~40 explicit override paths per theme (drift-by-omission waiting to happen). Instead: **one new
alias hop** — `color/neutral/1–15` between semantics and scales — exactly the radius alias-chain
move (Dave 2026-07-21) and ADR-0013's component→type-group hop. The cascade generator needed ZERO
resolution changes; the existing alias fixed-point propagated the 15-line warm binding into 109
effective override paths. When the third instance of a pattern appears this cheaply, the
architecture is telling you it was already there.

**4. The anchor discovery — index-identity is not the binding.** First render of the SC block put
ink at `warm/4 #25211C` (by index) while Dave had ruled `#13110E` (= `warm/2`). The insight this
forced: **neutral indices are SEMANTIC POSITIONS** — `neutral/4` means "the anchor: ink ≡
digital-black ≡ action fill", and each theme decides which of ITS steps plays that role. The warm
ramp packs dark, so SC's anchor is its step 2. One override line (`neutral/4 → warm/2`) moved ink,
dark page and primary fill coherently. Generalisation recorded in the ADR: themes bind by index by
default and REMAP where their ramp's shape demands it.

**5. Whites needed a classification, not a sweep.** Three spellings of white were live
(`color/white`, `color/grey/white`, flat values). The split that held: **substrate** whites (page,
ink-dark, reverse text, raised surfaces) ride `neutral/15` — warm off-white under SC; **absolute**
whites (labels ON status colours, dataviz, badge numerals) stay pure — type26-013 and the
dataviz-identical rule pin them. Four judgment calls (`text/on-action`, `text/on-inverse`,
`icon/on-inverse`, `border/action-strong`) were deliberately NOT auto-flipped — they're on Dave's
sheet, per the grey-tint-check instinct: surface, never auto-swap.

**6. Invariance was proven three ways before any render.** (a) a 179-leaf pre/post resolution
snapshot inside the transform script; (b) the projector reporting **0 value changes across 1248
bindings**; (c) the token-tier gate's cache-vs-alias arithmetic. The Playwright render pass then
FAILED environmentally (headless-shell download refused in this sandbox) — render-verify is OWED,
but it was the fourth check, not the first. Dave reviews the live HTML anyway (house rule).

**7. The graph seed had been rotting for three sessions.** `--verify` (run by hand, it's advisory
in-build) found **25 inscribed-not-in-seed edges** — R-D22's, ADR-0013's, R-D23/24's: every
session since the inscription pass had written headers/Edges lines without feeding the seed. The
assertion-propagation gap, structural: nothing fires when the seed drifts quiet. Reconciled under
the E2 rule (ratified source wins): +29 with R-D25's, one malformed `scope()` pseudo-edge
normalised at source (qualifier, not edge type), one duplicate traced to the parser re-extracting
"R-D24" from a parenthetical in my own ADR header — reworded the header rather than special-case
the parser. End state: **seed 122 = inscribed 122 = matched 122, zero mismatch.** Open question
queued: should `--verify` mismatch become blocking now that the corpus is clean?

## What I got wrong

- Dispatched the swatch fetch as PNG (PIL) before looking at the bytes — it was SVG all along.
- Asserted "Legacy dark ink = OPEN, don't guess" in the reflect-back; the override already
  carried `#FFFFFF` with a note. Verify-before-asking applies to my own flags too.
- The ADR header's prose parenthetical created a phantom graph edge — inscription prose is
  parser-visible; write headers knowing they are read by machines as well as people.

## Resolved state

ADR-0014 accepted + BUILT same session (Dave's 7-point in-chat ruling, by number). Build green
**45/45** with three new steps. Supercharge renders warm end-to-end (109 paths, 100 component
projections). R-D23 + R-D24 enacted in tokens/utils. Seed reconciled. **Open:** SC dark values +
raises + 4 held whites await Dave on the sheet; render-verify owed; ADR-0013 clean-room unblocked and next.
**Post-script (same session):** ruling 3 turned out RULED — the morning Opus session's wrap commit
`5459a4b` landed 14 SECONDS into this session (my "phantom dirt" reading of the 10:13 status was
wrong: those four dirty files were its uncommitted wrap, not stale mtimes). Race reconciled: my edits
all post-dated its commit, nothing lost either direction; receipt in
`notes/_receipts/2026-07-22-theming-cleanroom-race-note.md`. Two sessions writing shared state
without a declared conductor resolved by TIMING, not by the model — the receipt names the lesson.
