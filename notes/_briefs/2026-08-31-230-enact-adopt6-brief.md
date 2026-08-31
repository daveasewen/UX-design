# Brief — #230 enact lane (Opus): the six adopt-today items, in the components, before the demo

provenance: 230 · 2026-08-31 · conductor Fable · row W-316
Dave's go given #230. Demo is 2026-09-01 (W-308). Goal + pass condition:
`notes/_briefs/2026-08-31-230-demo-day-brief.md` § ★ THE GOAL — read it FIRST, it outranks
everything, including this brief.

## The job

Enact the six adoptable-today items exactly as priced in
`notes/_subreports/2026-08-31-230-demo-triage.md` (T1–T6 sections are the contract; this
brief does not restate them). Order: **T4 (chart tooltip) FIRST** — it is the one
demo-visible defect (28 `.dv-tip` rules scoped `:where(.cn-chart-*)`, tip appended to
`document.body` at `dv-behaviour.js:104`; conductor-verified). Then T1 (SKILL.md step-3
contradiction — docs only), T5 (screen-gate clobber), T2, T6, T3 (widest blast radius, last;
if time or risk bites, T3 may be DECLARED-DEFERRED rather than rushed).

## Fences (Dave's, verbatim-derived — violating any of these is the failure)

- ⛔ **Re-derive every fix in canon. NEVER copy code from
  `dashboards/international-banking-dashboard.canon.html` or from
  `_to_delete/Apollo-Spider-v1.0.2/`** — Dave: the Sol example "wont be a good example of
  the html code". GPT's tooltip change is a FINDING about the right mechanism (re-parent
  into the active `cn-chart-*` host); write the canon implementation yourself.
- Full ordered regen serial after source changes: `gen_radius_derive · gen_snippet_tokens ·
  canon/gen_canon_tokens · canon/gen_canon_components · canon/gen_theme_cascade ·
  gen_showroom · gen_component_partials` — ramp first, index last, the WHOLE serial per wave.
- T4 needs an EYE on a render: tooltip visible, styled, correctly positioned on a composed
  chart page, console light+dark minimum. Render recipe: mount-side per
  `notes/_subreports/2026-08-31-229-eye-repairs.md` + Lane B's REPLAY-THESE
  (`notes/_subreports/2026-08-31-230-seg-snippets-eye.md` §6): rebuild fonts.conf + font
  symlinks PER SESSION (they are session-path bound and fail SILENTLY — run the three-way
  font probe); `full_page=True` drops synthetic :hover; `TMPDIR=/dev/shm`, same-call exports;
  `set_content()` banned; ~178s call wall.
- No new rulings needed by construction — if an item turns out to need a design word, STOP
  that item, mark it DECLARED-DEFERRED with the question, move on. Do not guess.

## DO-NOT-RULE

No `_rulings.json`, no W-row writes, no memory, **no git operations** (conductor commits),
no release/dist/`RATIFY_IDS`, no `_build_all.py` (sandbox-impossible; run only the serial +
per-gate checks the triage report names per item), no review-page edits.

## Report

`notes/_subreports/2026-08-31-230-enact-adopt6.md` — COUNTS: (enacted N of 6, deferred M,
files changed, serial runs, PNGs eyed), REPLAY-THESE:, RULING-SHAPED QUESTIONS (mandatory
even if none). Chat gets a STUB: counts line + per-item one-liner + any deferral named.

## Pitfalls — replayed

- A mint assert proves VALUES never CONSUMPTION — drive the real thing (hover, tooltip).
- An alias-repoint can strip a theme override silently; a dangling var renders SILENT BLACK.
- Gate the presence, not the drift; a fix that skips the serial is a patch (s229-D3).
- canon has no `[data-theme="light"]` block — theme pinning inside dark ancestors lies;
  stamp `[data-chrome]` per FOUR-VISUALS v2.
