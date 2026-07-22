# ADR-0014 — Per-theme neutral primitives: the neutral DNA tier + the opacity-snaps-to-ramp state test

**Date:** 2026-07-22 · **Status:** accepted (Dave, in-chat, by number: items 1–3 + 6–7 "cool", item 5 "lets lock this in, they should be the same", item 4 "just use this we can always change") · **Extends:** ADR-0011 (four-theme override sets), ADR-0010 (nullable flex slots) · **Refines:** ADR-0009 (state mechanism — the `{colour|opacity|both}` set gains the theme-parameterised snap test) · **Relates:** R-D22 (progress=structure) · R-D23 (tabs — enacted here) · R-D24 (Legacy AA carve-out — enacted here) · ADR-0004 (AA floor, untouched outside that carve-out) · ADR-0008 (adapters consume stored colour equivalents, unchanged)

## Context

R-D23 (tabs) surfaced that the four themes carry their **own neutral primitive ramps** — an
architecture change, not a slot fill: Mono `color/mono/1–15`, Legacy the HSBC brand grey scale
(+ its 6-step dark-mode set, already in `colour.json`), Supercharge its own warm/taupe ramp,
Console sharing Mono's. Dave's spine (2026-07-22): **one flexible root DNA** — *"at any point we
could engineer 3 to align completely to one we choose"* — with sibling pairs **{Mono, Console}**
(same neutrals, interaction-opacity values, status palette, dataviz) and **{Legacy, Supercharge}**
(structural siblings, different palettes). ADR-0011's registry had anticipated this
(`neutralRamp` field, declared `ui-greys/neutral-ramp` slots) but nothing made it load-bearing.

**The Supercharge ramp was OBSERVED, not designed here** — pulled from Figma "Digital Supercharge
0.5" (`DS3tkWgaM1OsJg9ZC7nVLK`, swatch vectors `1105:47322…47350`, 2026-07-22, SVG-fill
extraction; the swatches are raw fills — `get_variable_defs` = `{}`):

| step | hex | step | hex | step | hex |
|---|---|---|---|---|---|
| 1 | `#000000` | 6 | `#413934` | 11 | `#AA9B92` |
| 2 | `#13110E` ★ink | 7 | `#493F39` | 12 | `#CDC8C6` |
| 3 | `#1C1915` | 8 | `#524842` | 13 | `#DFDEDC` |
| 4 | `#25211C` | 9 | `#635750` | 14 | `#F0EFED` |
| 5 | `#312C26` | 10 | `#806E65` | 15 | `#F7F6F4` (warm off-white — NOT `#FFFFFF`) |

Monotonic dark→light; warm cast peaks mid-low; **step 2 = `#13110E` = the ink Dave had already
named** — the quote was a ramp step before we knew the ramp.

## Decision

**1. The neutral DNA tier: `color/neutral/1–15` (+ `raise-1..3`).** A theme-agnostic 15-step
neutral index between the semantic tier and the neutral scales. Base binds `neutral/N →
color/mono/N` ($alias source + gated $value cache, house convention). All ~100 semantic aliases
on `color/mono/*` — plus the substrate whites (`color/white`, `color/grey/white`) and
`surface/digital-black` — rebind onto `neutral/*`. **Mono resolves identically by construction**
(verified three ways: a 179-leaf pre/post resolution snapshot, the projector reporting 0 value
changes across 1248 bindings, and the token-tier gate's cache-vs-alias check). A theme swaps its
entire neutral substrate by overriding `neutral/1–15` — one 15-line block; page, ink, surfaces,
borders, disabled greys follow by step index. This is the radius alias-chain move (Dave
2026-07-21) applied to the neutral axis, and the box-side sibling of ADR-0013's one-more-hop.

**2. Ramps are nature-named primitives; themes SELECT.** The warm ramp enters `colour.json` as
`color/warm/1–15` with full pull provenance (ADR-0011 tier 1: primitives belong to no theme).
Supercharge's override set binds `neutral/N → $alias color/warm/N` — the override-set loader
gained `$alias` support so the primitive stays the single source (retrieval-not-recall).

**3. Neutral indices are SEMANTIC POSITIONS — themes may remap, and the ink is the anchor.**
Index-identity is the default binding, but `neutral/4` *means* "the anchor: ink ≡ digital-black ≡
primary-action fill" (Mono seats all three on `mono/4`). Supercharge's anchor is **its step 2**
(`warm/2 #13110E`, Dave: "just use this we can always change") because the warm ramp packs dark —
index-identity would land the anchor a shade light (`warm/4` L≈33 vs `mono/4` L≈26). One override
line (`neutral/4 → warm/2`) moves ink, dark page and action fill coherently. `raise-1..3` (dark
elevation offsets) are CALCULATED for Supercharge (mono's +5/+9/+13 per-channel deltas applied to
`warm/4`) — provisional-agent, on the review sheet.

**4. The state mechanism is a THEME PROPERTY, and opacity must SNAP — gated.** Registry
`stateMechanism.default` per theme: **Mono + Console `opacity`** (shared values — sibling DNA) ·
**Supercharge `colour`** (a fade drags the hue off-ramp; opacity only by exception) · **Legacy
`explicit`** (as-built values, no operational fades — R-D23/R-D24 posture). Dave's test, now
enforcement (`_validate_state_snap.py`, **blocking**, selftest wired): a state token whose
mechanism includes opacity must store, per mode, an **exact step of the active theme's
`neutralRamp`**, and the operational flatten (`α·fades + (1−α)·over`) must sit within 8/255 luma
of that step — *engineered* to snap, calibrated on the two ruled consumers (button-sheet v7
hover; R-D23 tabs inactive `mono/7`/`mono/10`). The `$extensions.apollo.state` schema gains
`fades` + `over` (the flatten recipe, named explicitly). AA stays with the contrast audits
(ADR-0009 §4 unchanged). `snapPass` is parameterised by the active theme's ramp: a warm theme
snaps to warm steps — `neutralRamp` is now load-bearing, not documentation.

**5. Sibling pairs are inscribed and FENCED.** Registry `siblingPairs` records the spine.
Console: `neutralRamp = color/mono/1-15` (LOCKED — "they should be the same"), `fencedPaths`
(rag/, color/neutral|mono|warm/, dataviz, badge/, progress/, tabs/) enforced by the cascade
selftest — Console cannot diverge on the shared layers without a build failure. The older
"Console carries the broader new palette" note is its **chromatic layer on top, parked** — not a
conflict with the shared neutrals. Legacy does **not** ride the DNA tier: it is a reproduction
(R-D24), overridden explicitly per path, never re-derived.

**6. Selftests are WIRED into the build** (steps 42→45: cascade `--selftest`, snap gate, snap
`--selftest`). Found this session: the cascade selftest sat stale-RED for a day (it still
asserted "Supercharge empty", pre-R-D22) because `--selftest` only ran by hand — the
recorded-never-run class. The assertion now encodes the ruled facts (Legacy CTA red + as-built
tabs, Console rounds inside its fence, Supercharge warm binding + anchor + R-D22 path).

**Also enacted here:** R-D23 tokens (`tabs/active` = ink pair on `neutral/4`+`neutral/15`;
`tabs/badge/background` chained to `badge/background` — one badge source, Legacy's flat `#DB0011`
propagates; `tabs/inactive` = v7 two-token with the snap extension; Legacy overrides: red bar,
as-built ink inactive, no fade) and R-D24 (`LEGACY_THEME_EXEMPTIONS` + `legacy_exemption()` in
`_contrast_utils.py` — Legacy-theme pairs surface as **EXEMPTED (documented), never passes**).

## Consequences

- **Supercharge renders warm end-to-end** (no longer Mono-identical): page `#F7F6F4`, ink
  `#13110E`, 109 effective override paths, 100 component projections. The cascade grew 32→147
  paths with **zero generator re-architecture** — the alias fixed-point did the propagation.
- **The DNA claim is now mechanical:** re-aligning a theme to another = rebinding 15 neutral
  lines (+ anchor choice). The theme-generator horizon (`_FUTURE-STATE`) gains its substrate.
- **Adapters unchanged** (ADR-0008): every opacity state still stores its portable colour
  equivalent — now gate-guaranteed to be a real ramp step.
- **Open, deliberately:** (a) **Supercharge dark mode has NO Figma source** — the index-symmetric
  dark values + calculated raises ship provisional-agent on the review sheet
  (`reviews/SC-DARK-MODE-2026-07-22-v1.html`); "we can always change." (b) Four whites kept
  ABSOLUTE pending Dave: `text/on-action`, `text/on-inverse`, `icon/on-inverse`,
  `border/action-strong` (pure white even under warm themes — flip to `neutral/15` is one line
  each if ruled substrate). (c) Console's chromatic palette stays parked. (d) Legacy's dark-mode
  grey set (`color/grey/dark-mode/1–6`) remains available to its per-path overrides; no forced
  mapping. (e) The `input/error-condition` declared slots (ADR-0010) are untouched.
