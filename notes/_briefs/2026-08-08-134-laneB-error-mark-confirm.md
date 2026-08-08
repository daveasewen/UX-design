# Lane B — error-mark image confirm (owed since #130) — 2026-08-08

## Retrieval
`_memento_search.py --all "error mark image confirm"` found no direct hit; the owed item is
recorded in `notes/_MEMENTO-DECISIONS.md:5497-5499` (§ `s130-D4`/`D5`/`D6`, not-enacted):

> ⛔ NOT RULED — THE ERROR MARK. Dave sent an image that did not arrive. The conductor's
> provisional reading (*white shape, red glyph*, both legs 6.02) is recorded as provisional
> and awaits his confirm.

`s130-D4` also ruled `--rag-error-background #F6604C → #B92F1E` (colour-stability canon:
error red `#B92F1E`; legacy error `#A8000B`, untouched here).

## What "provisional 6.02" actually is
Contrast is symmetric, so white-vs-`#B92F1E` computes to **6.02:1** whichever way you read it
(shape-vs-page or mark-vs-shape) — confirmed by direct WCAG relative-luminance calculation,
no browser needed:
- `white` vs `#B92F1E` = **6.02:1**
- `#B92F1E` vs `white` = **6.02:1** (same pair, same number — that's why "both legs" landed
  on one figure)

**But that "white shape / red glyph" construction does not exist anywhere in the built
snippets.** What IS built and shipping today (`knowledge/snippets/Alert.reference.html`,
the only error-carrying roundel in the corpus) is the opposite pairing:
- **Light mode**: shape = `--err` (`#B92F1E`) on tint `#F1E0DC`, mark knocks OUT to the tint
  (red shape, pale-red glyph) — 4.71:1 shape-vs-tint, 4.71:1 mark-vs-shape (symmetric pair).
- **Dark mode**: shape = literal white, mark = literal black (structural roundel policy,
  Dave 2026-07-02 eve) — 21.00:1 both legs. Shape colour itself (`#CC4333` accent/border) vs
  the dark tint `#2C120D` is 3.68:1; vs page `#1A1A1A` is 3.66:1.

So the image Dave never sent was proposing a **third construction** (white shape, red glyph)
that has no home in the current Alert/Toast/Notifications roundel set. Nothing was built
against the provisional reading — correctly, since it was never ratified.

## Render attempt — BLOCKED, environmental, not a code finding
Followed `knowledge/_RUNBOOK-render-verify.md`: `/sessions` was 100% full (38M free) so staged
on `/var/tmp` per the runbook's shared-mount guidance. `pip install playwright` (and a bare
`pip download`) repeatably failed `OSError: [Errno 28] No space left on device` at a fixed
**38.8/47.4 MB** cutoff, twice, despite `df -h /` reporting 2.1G free and a 100MB `dd` test
writing cleanly. This is a new pothole (fixed-offset truncation, not a genuine disk-full
condition) — flagged, not diagnosed further; not promoted to the runbook on n=1. Old
scratch playwright installs from prior sessions (`pw-browsers-129`, `pwenv-s131`, etc., ~1GB)
were cleared from `/var/tmp` first and did not help.

**No PNG was produced this pass.** The numeric assertions above are computed directly
(WCAG relative-luminance formula, hand-verified against the known-ruled values in
`_consult-index.json` R-D1/R-D10, which already carry `6.02` for red/white independently) —
they are sound arithmetic, not a rendered proof.

## What's owed to Dave's eye
1. **The actual image he intended to send** — still never arrived; nothing this session
   changes that. The "white shape / red glyph" treatment remains provisional and unbuilt.
2. **A PNG confirm of the AS-BUILT Alert error roundel** (light: red shape/pale mark; dark:
   white shape/black mark) — could not be produced this pass due to the sandbox ENOSPC
   pothole above. Re-run when `/var/tmp` write behaviour is sane, or ask Dave whether the
   as-built treatment is what he wants confirmed instead of chasing the lost image.

## DO-NOT-RULE respected
No ruling, no commit, no chain/GM/state edits, no colour swap, nothing removed (only stale
`/var/tmp` scratch from prior sessions cleared, not repo files).
