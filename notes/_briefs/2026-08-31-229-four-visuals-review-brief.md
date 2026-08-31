# Brief — #229 four-visuals review page (Opus build sub)

**Mission:** one live HTML review page for Dave's eye — the four #228 repairs that have never
been rendered as pixels. HTML is the deliverable Dave reviews; any PNG you render is your OWN
verification only.

**Output file (the ONLY page you create):** `reviews/FOUR-VISUALS-2026-08-31-v1.html`
**Your report:** `notes/_subreports/2026-08-31-229-four-visuals-review.md`
Those two paths are the ONLY regions you own. You touch nothing else — no regen scripts, no
canon, no snippets, no tokens, no git operations of any kind (the conductor commits and pushes).

## The four specimens — COPY the approved artefacts, never re-draw

Hand-rolling invents defects. Every specimen starts from the reference:

1. **L8 — the underline stays straight.** `knowledge/snippets/Search-field.reference.html`.
   Show the plain (underline) search and the `.boxed` variant side by side: border-radius now
   lives ONLY on `.search.boxed` (canon: `:where(.cn-search-field) .search.boxed{…}`). Dave
   overruled the Dropdown/Input-fields precedent on the eye — the page should let him see why
   (straight underline vs rounded box).
2. **s227-D7 — concentric thumbs at m and l.** `knowledge/snippets/Segmented-control.reference.html`.
   All four scales (xs/s/m/l), and PER THEME — flexibility IS the requirement: mono/legacy/
   supercharge thumbs are 0 at every scale; console gets `--border-radius-segmented-thumb-m: 8px`
   and `-l: 8px` (track − padding). Console at m and l is the thing Dave has never seen.
3. **The library icon on the FAB's face.** Load the REAL `knowledge/_render/apollo-fab.js` on
   the page — the icon is on the FAB face; don't excerpt the SVG by hand.
4. **The hot-corner reveal.** Same live FAB: `REVEAL_DEFAULT='hotcorner'` (was `always`) —
   the FAB stays hidden until the cursor enters the corner (`CORNER_DEFAULT` 72). The page
   must SAY this beside the specimen so Dave knows to move his mouse, and show which corner.

## Method

- Copy the page scaffold from `reviews/FAB-READINGS-2026-08-30-v1.html` — its chrome is lifted
  verbatim from canon primitives and it deliberately wears canon's short alias names so the
  live FAB inherits the page theme on `file://`. Reuse that pattern; invent nothing.
- Live controllers per Dave's standing rule: light/dark toggle + theme switcher
  (mono/legacy/console/supercharge) where a specimen varies by theme. Specimens ALIVE, full
  spread — never screenshots pasted in.
- Load the real `knowledge/canon/canon.css` where the scaffold pattern does; if it inlines
  instead, the inlined values must be lifted verbatim and say where from.

## Render-verify (your own eye, before handover)

From `knowledge/_RUNBOOK-render-verify.md` (SIXTH STRATUM — read that section before rendering):
all in the SAME bash call — `export PYTHONPATH=/var/tmp/pylibs`,
`export PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-220`,
`export LD_LIBRARY_PATH=<MOUNT>/outputs/syslibs/usr/lib/aarch64-linux-gnu`, `TMPDIR=/dev/shm`.
`launch()` must NOT pass `env=`. ⛔ `set_content()` is BANNED — use `goto("file://…")` (drops
type.css silently otherwise). Render light AND dark, and console-theme segmented at m/l. Look
at the PNGs. A render owed clears only when SEEN.

## Pitfalls — replayed, not assumed read

- **Nothing survives a tool-call boundary** (wall ~178s): exports, /dev/shm, env — all die
  between calls. Drive steps individually; one render = one self-contained call.
- **Everything mount-side.** `/var/tmp` is a trap (VM disk class, #227); the orphaned playwright
  dirs above are read-only survivors, use them but write nothing there.
- **Version, don't overwrite** — the `-v1` suffix is deliberate; a follow-up is `-v2`. The
  sandbox can't `rm` (use `mv` if needed).
- The FAB probes `--surface` at mount — if your scaffold drops the alias names, the FAB falls
  back to its hard pair and the theme toggle will LOOK broken when it isn't.
- The segmented m/l concentric values are minted in canon under
  `[data-apollo-theme="console"]` ONLY — if you see 8px on mono, something is wrong; stop and
  say so rather than "fixing" it.

## DO-NOT-RULE

No rulings read into or out of scope; no `_rulings.json` access; no W-row opened, closed,
re-worded or minted; no memory writes; no commits, no push; no regen scripts; no edits outside
your two owned paths. Anything ruling-shaped you find goes in the report as RULING-SHAPED,
undecided, for the conductor.

## Report shape

`notes/_subreports/2026-08-31-229-four-visuals-review.md`: what you built, what you rendered
and SAW (per specimen, light+dark), anything UNPROVEN declared plainly, RULING-SHAPED items,
REPLAY-THESE for the conductor, and the wrap-handover cost line (unobservables declared, never
estimated). Your final chat message is a STUB: path to the page, path to the report, one line
per specimen's seen-state.
