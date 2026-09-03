# `#244`-`lane-B` — the live radius / corner tuner

session: `#244` · 2026-09-03
window: lane B (parallel with lane A nav/menu family, lane C debt sweep)
sub index: `lane-B`
brief: in-chat lane brief from the #244 conductor (no `notes/_briefs/` file was written for it)
tokens: `UNMEASURED` — a lane sub cannot read its own `message.usage`; the conductor holds the
figure for this lane.

## VERDICT

DONE. `reviews/RADIUS-TUNER-2026-09-03-v1.html` (94,445 bytes, single file, inline CSS+JS,
`knowledge/canon/type.css` inlined verbatim, zero external references — grepped) is a live
decision surface for the whole shape tier: **13 radius tokens on dials**, **8 component families
as faithful specimens**, **4 themes × light + dark shown side by side at all times**, a
token→value readout table, a ruling-shaped export, and a reset-to-store control. Render-proof
passed with **0 fails across 136 computed-radius assertions** (17 specimens × 2 modes × 4 themes)
plus **2 mutation arms** that prove role isolation and the concentric law, driven through
`goto("file://…")` in the seat-env Chromium — never `set_content`. **No token was changed, no
generator run, no git, no shared-state file touched.** The page rules nothing: every candidate is
printed beside its store value and every drift is flagged in red.

COUNTS: findings `4` · ruling-shaped `3` · UNPROVEN `2`

## What was done

**Read first (as briefed).** `notes/_receipts/2026-07-21-worker-A-radius-phase1.md` and
`-worker-B-radius-phase1.md` (the Phase-1 migration and the control/surface/indicator role
census); `knowledge/_rulings.json` grepped for radius/corner — 21 hits, the load-bearing ones
being s199-D3, s200-D1/D2/D3/D4, s201-D1/D5, s202-D1/D2, s217-D2/D3, s227-D4/D7, s229-D2/D3;
`knowledge/tokens/layout.json` `border-radius` family and all three theme override sets;
`knowledge/canon/canon.css` AUTO-THEMES for the generated per-component cascade;
`reviews/CONTRAST-CONTROLLER-2026-08-08-v3.html` for the house shape of a live controller.

**Built.** `reviews/RADIUS-TUNER-2026-09-03-v1.html`.

*Tokens covered — all 13 in the family, none omitted:*

| tier | tokens | dial |
|---|---|---|
| base | `border-radius/default` | slider 0–32 |
| roles | `control` · `surface` · `indicator` · `container` | slider 0–32 each, **plus an alias checkbox** — the ADR-0010 mechanism itself, not a tuner convenience. A role that aliases follows `default` and its slider greys out; unlink it to dial independently. Console is the only theme that has unlinked any, and the page shows that state on load. |
| segmented | `segmented-container/{xs,s,m,l}` | slider 0–24 each |
| segmented | `segmented-thumb/{xs,s,m,l}` | derived by default: `max(container − padding, 0)`, one switch for all four scales (s227-D7 widened concentric to all four); unswitch to type each thumb. Padding (2/2/2/4) is shown **read-only** — it is a spacing token and this page does not tune spacing. |

The four minted Console thumbs (4/6/8/8) are *exactly* what the concentric law yields from the
minted tracks (6/8/10/12), so the derive switch reproduces the store rather than replacing it —
verified in the probe, not assumed.

*Specimens embedded — 8 families, lifted from the snippet corpus with their real class structure,
local var namespaces and per-theme canon projections:*

| specimen | source snippet | radius tier exercised |
|---|---|---|
| Button (4 tiers + disabled) | `knowledge/snippets/Button.reference.html` | control |
| Input fields (boxed default / error / disabled + underline) | `Input-fields.reference.html` | control |
| Tags / chips (static, link, 2 dismissible) | `Tags.reference.html` | control |
| Status indicator (4 tint chips, 4 table cells, sim button) | `Status-indicator.reference.html` | **indicator** + control |
| Cards (action, linkcard, selectable) | `Cards.reference.html` | surface |
| Banner (all four RAG) | `Banner.reference.html` | surface |
| Modal dialog (+ its two buttons and close) | `Modals.reference.html` | surface **and** control in one specimen |
| Segmented control (xs/s/m/l, live thumb) | `Segmented-control.reference.html` | segmented-container + segmented-thumb |
| Container shell (sub-bento, 6 tiles) | schematic — declared, see Findings 4 | container |

Colour fidelity is not approximated: the per-theme blocks are **pasted verbatim from canon.css
AUTO-THEMES** for exactly these components, light block then dark block, in canon's own order, so
Legacy's `#DB0011` CTA, Supercharge's warm ramp and Console's shared RAG map all render true.

*Two-red law (`s151-D1`):* `--tn-red` is `#DA1A00` on the white chrome and is redeclared
`#F6604C` on every non-white ground — the dark panes and the Supercharge light pane
(`#F7F6F4`). Lines 568 / 621 / 623.

## Per-theme render evidence

Driver: `notes/_subreports/assets/2026-09-03-244-lane-B-radius-tuner/verify_radius_tuner.py`,
run in one bash call after `source knowledge/_render/seat_env.sh`
(`SEAT_ENV: OK seat=practical-laughing-clarke … faces=10/404 farm=10/10`). Page loaded with
`goto("file://…")`; `set_content` was never used. Playwright was absent from the sandbox and was
installed with `pip install playwright --break-system-packages`; the browser binary came from the
repo's durable `outputs/_render-env-229` per the render-verify runbook.

**Computed `borderTopLeftRadius`, 17 specimens × 2 modes × 4 themes = 136 assertions, all green.**
Per theme (light and dark identical, as the store says they should be):

| theme | button | input | tag | chip | card | banner | dialog | dlg btn | shell | seg xs/s/m/l | thumb xs/s/m/l |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Mono | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/0/0/0 | 0/0/0/0 |
| Legacy | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/0/0/0 | 0/0/0/0 |
| Console | 8 | 8 | 8 | 4 | 20 | 20 | 20 | 8 | 20 | 6/8/10/12 | 4/6/8/8 |
| Supercharge | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/0/0/0 | 0/0/0/0 |

Console errors across the whole run: **`[]`**. Readout table: 13 rows in every theme. The
segmented indicator has non-zero width in all eight panes (`indw` 55px) — a zero-width thumb
would make the concentric pair unjudgeable, so it is asserted rather than eyeballed.

**Mutation arm 1 — role isolation.** Mono, `border-radius/surface` driven to 18: card, banner and
dialog all read `18px` in both modes; the button stays `0px`. A surface dial that moved the button
would mean the specimens were sharing one var, which is the defect this arm exists to catch.

**Mutation arm 2 — the concentric law is live, per scale.** Console,
`segmented-container/m` driven 10 → 16: thumb `m` becomes `14px` in both modes
(`max(16 − 2, 0)`), while scale `l` stays 12/8. Both the law and the per-scale isolation are
proven by the same arm.

**Settled-colour probe** (a second pass with a 900 ms settle — the first pass caught the 160 ms
`background` transition mid-flight and read Legacy's CTA as `rgb(210,1,17)`; that was the
instrument, not the page). Settled: Legacy CTA `rgb(219,0,17)` = `#DB0011` both modes; Legacy
banner `#A8000B`; Console/Supercharge banner `#B92F1E`; Supercharge light ground
`rgb(247,246,244)` = `#F7F6F4` with CTA `#13110E`; Mono/Console CTA `#1A1A1A` light,
`#FAFAFA` dark. Type resolves to `"Univers Next HSBC"` in every pane (the real face, not a
fallback).

**Eyeballed:** four full-viewport PNGs (one per theme) plus two scrolled captures of the
segmented block and of the readout + ruling-shaped block, all in
`notes/_subreports/assets/2026-09-03-244-lane-B-radius-tuner/`. Read back by eye at #244; the
Console capture shows the 8/20/4/20 set and the concentric segmented pairs rendering correctly in
both modes.

## Findings

1. **The Console thumbs are already exactly concentric — the law reproduces the store, it does
   not replace it.** Probed, not assumed: `max(6−2,0)=4`, `max(8−2,0)=6`, `max(10−2,0)=8`,
   `max(12−4,0)=8`, matching `apollo-console.overrides.json` byte for byte. The tuner's derive
   switch therefore starts ON in every theme, computed from the store rather than hard-coded
   (`STATE` seeds with `SCALES.every(...)`).
2. **`border-radius/indicator` is aliased in Console, not overridden.** `apollo-console.overrides.json`
   carries no `indicator` entry; canon projects `4px` purely through the `default: 4` alias. The
   page shows this in the dial's sub-line (`store 4px (aliased) · following default`) because
   it changes what a ruling on it would mean — dialling indicator alone requires *unlinking* it,
   which is a new override, not an edit to an existing one.
3. **Legacy's square is an explicit ruling, Supercharge's is inheritance.** `apollo-legacy.overrides.json`
   sets `border-radius/default: 0` on purpose (Dave 2026-07-21, "Legacy = square, same as Mono");
   `apollo-supercharge.overrides.json` carries no radius entry at all. Identical on screen,
   different in what it would cost to change. Both notes are surfaced under the theme switcher.
4. **The `container` role has no lifted specimen in the snippet corpus** — its live consumer is
   the bento layer in `canon.css` (`--bento-radius: var(--border-radius-container)`), not a
   `knowledge/snippets/*.reference.html` file. It is drawn here as a schematic sub-bento (6 tiles,
   1px gutter, radius on the container per s217-D2) and declared as such on the page. The
   s218-D8 corner-keyline construction is **not** modelled.

## RULING-SHAPED QUESTIONS

⛔ Nothing below is ruled. The page itself carries a RULING-SHAPED block that prints the dial
state verbatim and **unscoped** — it names no theme binding, no mint-vs-inherit, no enactment.

1. **The whole point of the surface: the numbers themselves.** The dials open on the store, so
   the export currently reads `NO CANDIDATE VALUES — every dial sits on its store value`. Dave
   moves a slider, the export names the drifted tokens, and *that* text is the candidate.
   Option (a) rule per token off the export; option (b) rule the Console set as one block, the
   way s199-D3 did. No recommendation — this is the decision the page exists to hold.
2. **Does `border-radius/indicator` want to leave the alias?** Console's `4px` today is
   `default`'s value arriving through the alias (Finding 2). Option (a) leave it aliased —
   indicator and default move together for ever; option (b) unlink it now at `4` so it can be
   dialled later without a structural change. Costs differ: (b) writes a new override entry into
   `apollo-console.overrides.json` for zero visual change today.
3. **Do the three square themes want a `container` entry at all?** s200-D3 wrote nothing for
   mono/legacy/supercharge deliberately. If Dave ever dials one of them off zero, the alias
   carries `default` into every role at once — the tuner shows exactly that coupling when you
   drag `default` in Mono. Option (a) leave the coupling (one dial, whole theme); option (b) mint
   explicit role entries so a square theme can round one tier only.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** that the tuner's specimens are pixel-equivalent to the same components rendered
  from `canon.css` itself. The CSS here is lifted from the snippets and the AUTO-THEMES
  projections rather than served from the 1.9 MB `canon.css` — inlining that file would have made
  the page ~2 MB and, at that size, slower to open than to reason about. Price to prove: one
  pixel-diff matrix, showroom page vs tuner pane, 8 components × 4 themes × 2 modes = 64
  comparisons, ≈ one render lane.
- **UNPROVEN:** behaviour on a narrow viewport. Every probe ran at 1600×1200/1400. The chrome
  carries two breakpoints (`1080px` rail stacks, `900px` panes stack) but they were not rendered.
  Price to prove: two more screenshots (390 and 820) in an existing driver run, ≈ 2 minutes.
- **CLAIMED:** the ruling identifiers cited on the page and in this report (s199-D3, s200-D1…D4,
  s201-D1/D5, s202-D1/D2, s217-D2/D3, s227-D4/D7) are read from `knowledge/_rulings.json` `says`
  fields and from the `$note` text in the token files. The `$note` text is itself a claim by a
  prior session — I re-read the **values** first-hand and they agree; I did not re-derive the
  ruling history behind them.

**Declared residue:** an EMPTY directory `outputs/_tmp-244B/` remains. Its four PNGs were moved
into the assets folder above; the sandbox mount refuses `rmdir` on it
(`Operation not permitted`). `outputs/` is gitignored; the residue is a zero-byte directory, not
content.

**Not done, by instruction:** no token value changed · no git · no `_build_all.py` · no edits to
`GOOD-MORNING.md`, `_LIVE-STATE.md`, `_CHAIN.md`, `_CARRIES.md`, `knowledge/_rulings.json`,
`knowledge/tokens/*` or MEMORY · no ruling inscribed. Verified by inspection: the only files this
lane created are the review page, this report, and the six files under its assets folder.

## Evidence

`notes/_subreports/assets/2026-09-03-244-lane-B-radius-tuner/`

- `verify_radius_tuner.py` — the render-proof driver, re-runnable; prints the full probe JSON and
  a `=== FAILS:` line. Reading on 2026-09-03: **0**.
- `mono.png` · `legacy.png` · `console.png` · `supercharge.png` — full viewport at 1600×1400,
  each theme, light and dark panes side by side. Proves the four-theme switch and the colour
  cascade, and shows Console's rounded set against three square themes.
- `console-seg.png` — scrolled to the segmented block and the container shell: the concentric
  pairs at all four scales, both modes.
- `console-readout.png` — the 13-row readout table and the head of the RULING-SHAPED export.
