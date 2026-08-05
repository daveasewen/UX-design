# #98 — ONE bar, pure canon: how the purge changed sides

provenance: local_72856636-93aa-4b17-8dd7-ed9e929ea328 · 2026-08-05
status: observed

**Spine links:** ledger `notes/_MEMENTO-DECISIONS.md` § ★ #98 · receipt
`notes/_receipts/2026-08-05-98-one-bar-chrome.md` · register `knowledge/_REVIEW-SIGNOFF.md`.

## The arc

**1 · The opener settled #97's forks fast, except (c).** Dave ruled (a) one pane and (b) keep
Replay in one line each. On (c) — generator-strip vs source edits — he said *survey first*,
with generator-side as the stated lean ("snippets stay canonical"). The lean was mine as much
as his, carried from #97's ledger line.

**2 · The survey killed the lean's premise.** The controls were uniform (76/77 identical
`.demo-controls` blocks — good for any method), but the wiring was not: every file binds the
toggle with an UNGUARDED `getElementById('themeToggle').addEventListener`. A generator-side
DOM strip would throw inside the pane and kill everything after it in the same script block —
including the Replay wiring that ruling (b) required kept. So the "safe, one-writer" option
was the JS-hazardous one; the evidence pack said strip-with-stubs, CSS-hide, or sources.

**3 · Dave flipped the frame rather than picking a workaround.** Offered strip-with-stubs as
the recommendation, he answered with intent, not mechanism: *"I want these snippets to be
clean."* A clarifying pass (he asked for the implications in plain terms) surfaced the real
question — does anyone ever open a snippet file directly? His answer — the library is his
sole interface now — dissolved the one argument for keeping controls in source. **#98-D1:
sources clean.** The lesson: the survey's job wasn't to choose between the two named options;
it was to expose the hazard that made a THIRD option (remove the hazard class entirely) the
cheap one.

**4 · Replay changed homes twice and ended simpler.** #97 read it "per-pane?"; the opener
kept it per-pane; the final ruling put it IN the bar, disabled where inapplicable. That
demanded a generic mechanism (generator-injected? no — bar-side `contentDocument` re-toggle
of `.dv-animate`/`figure.dv`), which works for 13 of 14 former replay carriers.
**Dead-end, declared:** Confirmation's motion is a display-toggle idiom, not `dv-animate`,
so its Replay is disabled — migrating it is a canon behaviour change, registered for Dave.

**5 · Mechanics.** Strip delegated to a Sonnet sub (75 files, −931/+171; entangled files
hand-edited, real state controls kept; one incident — a bracket-depth bug caught by its own
verification grep, full restore from HEAD, redo). Conductor re-ran every verification before
building on it. Generator: one bar, one pane, index viewbar gone; +5 selftest bites pinning
the ruling on the templates. Render-proof: 44 asserts × 2 widths, HSBC face true, console
errors [] — the empty console IS the proof the strip left no orphaned JS. Mid-window, Dave's
screenshot removed the index theme seg too (#98-D2) — the one-bar rule eating its second
duplicate the same day it landed.

## Resolved / open

Resolved: #97-D1 enacted end-to-end; flag ① closed; sources pure canon; 4% opacity steps
ruled (#98-D3). Open: opacity spread build (#99) · candle/bullet eyeballs · Confirmation
replay idiom · 700px cosmetic gap.
