# Brief — s176 step-colour controller for Dave (2026-08-14, v1)

Conductor: #176. You are ONE Opus build sub. Build a DECISION CONTROLLER — a single live HTML page Dave rules from by eye. Output: `reviews/STEP-COLOUR-CONTROLLER-2026-08-14-v1.html`. Version `-v1`; never overwrite an existing file (use -v2 etc.).

## The two decisions the page serves (do NOT rule either)

**D-A — step-tracker colour in Mono / Console / Supercharge.** s175-D1: discrete-step indicators (Progress-tracker, Stepper) MAY use colour; Legacy is DEFINITE (keeps #DB0011 via step/complete); Mono/Console/SC are UNDECIDED. Show, per undecided theme, both candidates side by side: (1) COLOUR — the current inherited step/complete resolution (SC #B92F1E|#CC4333; Mono/Console currently resolve to base — show what actually renders, resolved from canon.css, not assumed) and (2) INK — the theme's s176-D1 ink (Mono/Console #1A1A1A|#FFFFFF, SC #13110E|#F7F6F4). Legacy renders as the RULED reference row, clearly labelled.

**D-B — the Legacy bar ink fall-through.** In Legacy the Progress-bar fill renders the BASE ink #1A1A1A (no override, no rebind). s176-D1 says Legacy's blackest ink is #333333. Show the Legacy Progress-bar both ways (#1A1A1A vs #333333 fill), light+dark, with measured fill-on-track contrast for each. One line of neutral framing; no recommendation baked into layout order.

## Requirements (standing Dave rules — all firm)

- LIVE specimens: real markup from `knowledge/snippets/Progress-tracker.reference.html`, `Stepper.reference.html`, `Progress-bar.reference.html`, styled by the real `knowledge/canon/canon.css` (link or inline it). Not screenshots, not approximations.
- Full spread: all relevant themes × light AND dark, and the responsive collapse (the @container ≤520px bar-shape state of the tracker) shown for each candidate — it keeps the step treatment per s175-D1(c).
- Measured contrast per cell (3:1 non-text threshold for fill-on-track and step-marker-on-surface), computed and printed next to each specimen. Compute WCAG ratios yourself in the page or pre-compute; label PASS/FAIL plainly.
- DECISION CONTROL: per open choice (Mono, Console, SC, and D-B) a radio/segmented pick, with an EXPORT button producing a JSON blob of the picks (so a pick becomes a ruling in one message). No localStorage — in-memory only.
- Plain-prose labels, no ID codes as the decision surface. Dave is dyslexic: short labels, generous type, the decision question stated in one sentence per section.
- Grey tints/inks: if you must introduce ANY grey not in the store, surface it loudly in the page — never silently pick one.

## Render-verify

Follow `knowledge/_RUNBOOK-render-verify.md` (READ IT): goto("file://…"), canvas probe for fonts not fonts.check(), playwright lives in /var/tmp if sandbox ENOSPC, ⛔ set_content() is banned. Verify: page loads, both modes toggle, specimens visibly differ between candidates, contrast figures render. Screenshot at least one light and one dark crop and report what you saw.

## ⛔ DO NOT

- Rule anything, change any token, edit canon.css or any generator, touch _rulings.json/_state.json/wrap machinery, run _build_all.py.
- Trust hexes from this brief — resolve every rendered value against canon.css at HEAD and report the resolution chain.

## Pitfalls replayed

- A token NAME is not an ADDRESS — SC rebinds color/neutral onto color/warm; resolve, don't assume.
- Call boundary ~45s wall — chunk playwright runs.
- A page that "should" show a difference must be VERIFIED to show it — compare computed styles between candidate cells before claiming the spread is live.

## Report back

File path · resolution chains for every hex shown · contrast table · render-verify receipts (what you saw, both modes) · friction log · NOT DONE list.

Repo (bash): /sessions/upbeat-nifty-mayer/mnt/UX-design
