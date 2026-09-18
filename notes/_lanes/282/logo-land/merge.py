#!/usr/bin/env python3
"""s282-D5 step 2 — build knowledge/guidelines/logos.md as THE ONE LOGO GUIDELINE.

Moves, BYTE-FOR-BYTE: logo26-001..007 out of brand-refresh-assets.md's `## Logos (2026)`
section, and va25-015/016/017 out of visual-assets.md's `## Logos (2025 page …)` section.
Every {#id}, every destiny tag and every `(s282-D1, Dave …)` clause survives the move
unchanged — asserted by byte comparison before writing. va25-014 is NOT moved (the print
clear space; not named by the ruling). Leaves a one-line pointer where each block was.
"""
import re, sys, pathlib, hashlib

ROOT = pathlib.Path("/sessions/tender-hopeful-allen/mnt/UX-design/knowledge/guidelines")
BRA, VIS, LOG = ROOT/"brand-refresh-assets.md", ROOT/"visual-assets.md", ROOT/"logos.md"

def bullets(txt, header_rx):
    """Return (header_line, start, end, [(id, block_text)]) for the section."""
    m = re.search(header_rx, txt, re.M)
    assert m, header_rx
    sec_start = m.end()
    n = re.search(r"^## ", txt[sec_start:], re.M)
    sec_end = sec_start + n.start()
    body = txt[sec_start:sec_end]
    blocks = []
    idxs = [b.start() for b in re.finditer(r"^- ", body, re.M)] + [len(body)]
    for a, b in zip(idxs, idxs[1:]):
        blk = body[a:b]
        ids = re.findall(r"\{#([a-z0-9-]+)\}", blk)
        blocks.append((ids[0] if ids else None, blk))
    return m.group(0), sec_start, sec_end, body, blocks

bra = BRA.read_text(encoding="utf-8")
vis = VIS.read_text(encoding="utf-8")
log = LOG.read_text(encoding="utf-8")

bh, bs, be, bbody, bblocks = bullets(bra, r"^## Logos \(2026\)$")
vh, vs_, ve, vbody, vblocks = bullets(vis, r"^## Logos \(2025 page[^\n]*$")

move_bra = [(i, t) for i, t in bblocks if i and i.startswith("logo26-")]
move_vis = [(i, t) for i, t in vblocks if i in ("va25-015", "va25-016", "va25-017")]
keep_vis = [(i, t) for i, t in vblocks if i not in ("va25-015", "va25-016", "va25-017")]

assert [i for i, _ in move_bra] == [f"logo26-{n:03d}" for n in range(1, 8)], move_bra
assert [i for i, _ in move_vis] == ["va25-015", "va25-016", "va25-017"], move_vis
assert [i for i, _ in keep_vis] == ["va25-014"], keep_vis
assert "".join(t for _, t in bblocks).strip() == bbody.strip(), "brand-refresh section is not all bullets"

BRA_MOVED = "".join(t for _, t in move_bra).rstrip("\n")
VIS_MOVED = "".join(t for _, t in move_vis).rstrip("\n")
VIS_KEPT  = "".join(t for _, t in keep_vis).rstrip("\n")

# ---------------------------------------------------------------- new logos.md
NEW = f"""---
title: Logos — the one logo guideline
source: MERGED under s282-D5 (Dave 2026-09-18, his own export of the #282 logo review) from
  TWO sources — (1) HSBC Common Toolkit (MCP) "Gaps and edits" branch, Foundations › Logos
  page (node 29:1009), captured 2026-06-17, the 2025-era sticker sheet this file already
  was; (2) the logo section of `brand-refresh-assets.md` (create.hsbc → Foundations and
  identity → Brand identity refresh, `brand-refresh/logos.html`, captured 2026-07-02),
  whose `logo26-001..007` bullets moved here byte-for-byte, together with `va25-015`,
  `va25-016` and `va25-017` from the 2025 Logos section of `visual-assets.md`.
type: foundation-guidance
captured: 2026-06-17
merged: 2026-09-18
precedence: |
  APOLLO'S DECISIONS OVERRIDE THE REFRESH WHERE THEY DIFFER — Dave, 2026-09-18: "our
  decisions here over-ride the refresh". Where a rule below carries an Apollo ruling id
  (s282-D3, s282-D4, s282-D5) and a moved brand bullet says otherwise, the Apollo rule
  governs. Each moved block is labelled with its vintage (2026 refresh / 2025 page) so the
  boundary bra26-003 protects is kept inside this file instead of across two files.
related_assets: knowledge/assets/logos/ (8 logo SVG variants, 12 before s282-D4 — EXPORTED 2026-06-17, vector; see _export-logos.py)
external_ref: https://create.hsbc/foundations-and-identity/Logos.html
note: |
  This is the SINGLE logo guideline (s282-D5, q5 (a) "Merge into one logo guideline").
  Photography and Creative Hexagons stay in `brand-refresh-assets.md`; `va25-014` (the
  PRINT clear space and the 105×20px minimum) stays in `visual-assets.md` — it is the print
  rule and this ruling did not name it. No design tokens.
---

# Logos

The one logo guideline: the artwork set, the Apollo decisions that govern it, and the brand
rules — 2026 refresh and 2025 page — that were moved here under `s282-D5`. Where the brand
standard and an Apollo decision differ, the Apollo decision governs (see `precedence`).

## Logo set

Two logo lockups (the *Masterbrand with identifier* lockup was SCRAPPED — s282-D4, Dave
2026-09-18: its four files moved to `_to_delete/logos-identifier-282/`, its nodes removed
from the graph), each available in **Colour** and **Monotone**, and in **On Light** and **On
Dark** treatments (the On-Dark artwork is the light/reverse version for dark surfaces):

1. **Hexagon** — the HSBC hexagon mark alone.
2. **Masterbrand** — hexagon + "HSBC" wordmark.
3. ~~Masterbrand with identifier~~ — SCRAPPED (s282-D4). The identifier lockup was an
   "Example identifier" placeholder; two of its four exports were the plain masterbrand on a
   wider canvas (#282 logo review, exporter defect). Dave's export answered q6 (b), "Retire
   the four identifier variants until a real identifier exists", and his forward note — the
   material may one day return as an AI-readable "Ask create" assistant — is FILED as a
   carry (W-282ll), not enacted.

That's **8 variants** (2 lockups × {{Colour, Monotone}} × {{On Light, On Dark}}) — was 12
before s282-D4. The `hexagon-dark-colour` / `hexagon-light-colour` pair is ONE drawing
exported twice (619 bytes each, diff = 1 float literal) and BOTH FILES AND BOTH NODES ARE
KEPT — s282-D5, q1 (a) "Keep both files and both nodes"; no alias, no `activeVariantOf`.

## Size — the Apollo scale (s282-D3)

Logo size is measured by **HEIGHT**, on five steps:

| step | height |
| --- | --- |
| x-small | 24px |
| small | 28px |
| medium | 32px |
| large | 36px |
| x-large | 40px |

The height is the artwork's **RAW pixel height, not a viewBox scaled to it** — Dave: "no
view boxes, just the raw height" · "and width obviously". Width follows the lockup's own
ratio and is never the measure. Whether any lockup may render UNDER x-small is NOT ruled.

## Apollo rules (s282-D5, 2026-09-18 — his own export)

- **The masthead logo is the FULL-COLOUR Masterbrand on BOTH grounds, in ALL FOUR
  THEMES** — `masterbrand-light-colour` on light, `masterbrand-dark-colour` on dark, in
  Apollo Legacy, Apollo Mono, Apollo Console and Apollo Supercharge alike. A monochrome
  theme does not make a monochrome masthead: mono is not the masthead lockup in any theme.
  `va25-015` says a Masterbrand appears in ALL digital mastheads; this names WHICH VARIANT.
  Dave answered "Full colour both grounds — masterbrand-light-colour on light,
  masterbrand-dark-colour on dark" on all four theme rows of his own export.
  (s282-D5, Dave 2026-09-18) [BLOCKING — masthead variant check; the Header/masthead
  component inherits it alongside va25-015's behaviour contract] {{#logo26-008}}
- **Digital clear space is a FLOOR, not the print rule: vertical clear space ≥ 0.25 × logo
  height, snapped UP to the 4px grid.** At the five `s282-D3` steps that is 24 → 8 · 28 → 8
  · 32 → 8 · 36 → 12 · 40 → 12 px. It is a floor, not a value: anything at or above it that
  itself sits on the 4px grid is legal. Dave's words: "The logo dimension based clear space
  is really for print, we have a rule of thumb for digital is half of this dimension, but it
  isn't a rule, maybe we have it set as a floor of 0.25 snap-up to the 4px grid, so at 24
  height we have 8px as the floor fer the vertical clearspace, as long as it snaps to 4px
  above that I'm comfortable". ⚠ HIS NOTE SAYS **VERTICAL**. **HORIZONTAL clear space is NOT
  STATED AND IS NOT RULED** — it is carried open (W-282ll), never completed by symmetry. The
  logo-dimension clear space (`va25-014`, 1× hexagon height on all sides, `visual-assets.md`)
  remains the PRINT rule and is untouched. (s282-D5, Dave 2026-09-18) [BLOCKING — vertical
  digital clear space only; the horizontal axis has no rule to check against] {{#logo26-009}}
- **The hexagon alone may be used on the nav-rail head, the app tile and the favicon** —
  each conditional on Create Direct approval AND "HSBC" in view (`va25-016`'s two conditions
  stand, unrelaxed) — **and in responsive layouts at the smaller sizes, tablet-portrait and
  mobile, where the Masterbrand does not fit.** Dave's words: "The pure logomark can also be
  used in responsive layouts when we get to smaller sizes, tablet-portrait and mobile". This
  answers `s230-D2`'s declared residue — "App-shell-nav-rail deliberately NOT rebound (56px
  rail head, no lockup fits)": a lockup now fits, and it is the hexagon.
  (s282-D5, Dave 2026-09-18) [ADVISORY — every use is gated on a human approval (Create
  Direct) that this repo cannot check, so it advises rather than blocks] {{#logo26-010}}

## Logos (2026 refresh — moved here from `brand-refresh-assets.md` by s282-D5)

{BRA_MOVED}

## Logos (2025 page — moved here from `visual-assets.md` by s282-D5; refresh-contaminated, see visual-assets F1)

{VIS_MOVED}

## Exported assets

SVGs exported to `knowledge/assets/logos/<lockup>-<light|dark>-<colour|mono>.svg` via
`_export-logos.py` (Figma `file_content:read` token). All 12 (now 8) came through as
**vector** (hexagon in `#DB0011`/white; masterbrand wordmark and identifier as vector paths)
— no embedded raster.

> Per the icons sourcing rule, treat these exports as **internal prototype assets**; for
> production/dev handoff, source official logo artwork from create.hsbc / the UI Centre.

## Cross-references

`brand-refresh-assets.md` (Photography + Creative Hexagons stay there; its Logos section
moved here) · `visual-assets.md` (`va25-014`, the PRINT clear space and minimum size, stays
there) · `web-foundations.md` (webf-008 dark-logo receipt ↔ logo26-003) ·
`_PAYMENTS-JOURNEY-GAPS.md` (logo26-001 lands with Headers) · `icons.md` (icon-003, app
tiles as a separate branding application) · `hexagon-masks.md` / `imagery.md` (2025-era
record) · `knowledge/_logo_nodes.json` (the 8 logo nodes this file governs).
"""

# byte-for-byte proof BEFORE writing
for rid, blk in move_bra + move_vis:
    assert blk.rstrip("\n") in NEW, rid
    assert f"{{#{rid}}}" in NEW, rid

# ------------------------------------------------------------- source surgery
PTR_BRA = ("*The 2026 Logos section moved to `logos.md` under `s282-D5` (Dave 2026-09-18, "
           "\"our decisions here over-ride the refresh\") — `logo26-001`…`logo26-007` live "
           "there, byte-for-byte, with the new Apollo logo rules. Photography and Creative "
           "Hexagons stay here.*\n")
PTR_VIS = ("*`va25-015` (masthead contract), `va25-016` (never-rules) and `va25-017` "
           "(variant selection on photographic backgrounds) moved to `logos.md` under "
           "`s282-D5` (Dave 2026-09-18). `va25-014` stays here: it is the PRINT clear space "
           "and minimum size, and the ruling did not name it.*\n")

bra_new = bra[:bs] + "\n\n" + PTR_BRA + "\n" + bra[be:]
vis_new = vis[:vs_] + "\n\n" + PTR_VIS + "\n" + VIS_KEPT + "\n\n" + vis[ve:]

LOG.write_text(NEW, encoding="utf-8")
BRA.write_text(bra_new, encoding="utf-8")
VIS.write_text(vis_new, encoding="utf-8")
print("moved from brand-refresh-assets.md:", [i for i, _ in move_bra])
print("moved from visual-assets.md:", [i for i, _ in move_vis])
print("kept in visual-assets.md:", [i for i, _ in keep_vis])
print("logos.md bytes:", len(NEW))
