# A11y gate — _validate_a11y.py

**101 snippet(s)** · **0 failure(s)** · **186 warning(s)** · **237 note(s)**

Measured MARKUP-DRIVEN (s114-D5, rebuilt #116): **609 control(s)** and **203 focusable data mark(s)** enumerated from the markup, sized through a subject-aware cascade with `var()` resolved. Engine + declared gaps: `knowledge/_a11y_target.py`.

Gating: reduced-motion (2.3.3) · unknown ARIA role · CONTROL target under the 24px floor (2.5.8, aid-009). Reported: CONTROL 24–43 vs the 44 HSBC default (axs-003; `s114-D6` promotes this to blocking, ordered after this rebuild) · DATA MARK under 24 (`s116-D1`) · UNMEASURED boxes.

Library bar (aqa-003, ruled 2026-07-03): the canon is LIBRARY-GRADE — guideline and recommendation tiers bind it, not just standards.

## Owed measurement — data marks below 24 (`s116-D1`, for Dave)

**107 focusable data mark(s) fall below the 24px dense-case minimum**, across 6 snippet(s):

- `Chart-bar` — 6
- `Chart-butterfly-h` — 12
- `Chart-butterfly-v` — 5
- `Chart-combo` — 12
- `Chart-line` — 60
- `Chart-stacked-area` — 12

NOT WAIVED and NOT REMEDIED here: `s116-D1` orders this measurement BEFORE the mark tier goes blocking. `MARK_TIER` in this file is the single switch.

## Accordion
- ⚪ note — `button.head` — UNMEASURED: one axis declared (autox56), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.head` — UNMEASURED: one axis declared (autox56), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Account-selector
- ⚪ note — `button#asTrigger.as-trigger` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.as-opt` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `li.as-opt` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `li.as-opt` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size

## Alert
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size

## Anchor-nav
- ⚪ note — `a` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Avatar-group
- ⚪ note — `button.avg-btn` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Banner
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size

## Breadcrumbs
- ⚪ note — `a.crumb` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.crumb` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.crumb` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.crumb` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.crumb` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.crumb` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size

## Cards
- ⚪ note — `a.linkcard` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.headline` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.arrow` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.arrow` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `div.card.opt` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `div.card.opt` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `div.card.opt` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size

## Chart-bar
- 🟡 warn — DATA MARK `rect.dv-series` — 219.2x20.2 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 94.0x20.2 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 495.9x20.2 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 135.7x20.2 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 109.6x20.2 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 156.6x20.2 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)

## Chart-butterfly-h
- 🟡 warn — DATA MARK `rect.dv-series` — 133.2x20.0 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 162.8x20.0 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 83.2x20.0 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 112.8x20.0 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 55.5x20.0 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 46.2x20.0 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 166.5x20.0 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 175.8x20.0 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 107.3x20.0 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 74.0x20.0 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 37.0x20.0 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 61.0x20.0 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)

## Chart-butterfly-v
- 🟡 warn — DATA MARK `rect.dv-series` — 48.7x16.2 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 48.7x21.6 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 48.7x23.4 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 48.7x18.9 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `rect.dv-series` — 48.7x17.1 — under the 24 dense-case minimum (rect w/h attrs) (s116-D1: marks carry the 24 floor, not the 44 target)

## Chart-combo
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- ⚪ note — `button.t-cm-chart-label` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size

## Chart-line
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its rect child (rect w/h attrs)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its rect child (rect w/h attrs)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its rect child (rect w/h attrs)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its rect child (rect w/h attrs)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its rect child (rect w/h attrs)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its rect child (rect w/h attrs)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its rect child (rect w/h attrs)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its rect child (rect w/h attrs)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its rect child (rect w/h attrs)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its rect child (rect w/h attrs)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its rect child (rect w/h attrs)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 11.0x11.0 — under the 24 dense-case minimum (<g> wrapper measured from its rect child (rect w/h attrs)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 13.0x13.0 — under the 24 dense-case minimum (<g> wrapper measured from its polygon child (polygon bbox)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 13.0x13.0 — under the 24 dense-case minimum (<g> wrapper measured from its polygon child (polygon bbox)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 13.0x13.0 — under the 24 dense-case minimum (<g> wrapper measured from its polygon child (polygon bbox)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 13.0x13.0 — under the 24 dense-case minimum (<g> wrapper measured from its polygon child (polygon bbox)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 13.0x13.0 — under the 24 dense-case minimum (<g> wrapper measured from its polygon child (polygon bbox)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 13.0x13.0 — under the 24 dense-case minimum (<g> wrapper measured from its polygon child (polygon bbox)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 13.0x13.0 — under the 24 dense-case minimum (<g> wrapper measured from its polygon child (polygon bbox)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 13.0x13.0 — under the 24 dense-case minimum (<g> wrapper measured from its polygon child (polygon bbox)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 13.0x13.0 — under the 24 dense-case minimum (<g> wrapper measured from its polygon child (polygon bbox)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 13.0x13.0 — under the 24 dense-case minimum (<g> wrapper measured from its polygon child (polygon bbox)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 13.0x13.0 — under the 24 dense-case minimum (<g> wrapper measured from its polygon child (polygon bbox)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 13.0x13.0 — under the 24 dense-case minimum (<g> wrapper measured from its polygon child (polygon bbox)) (s116-D1: marks carry the 24 floor, not the 44 target)
- ⚪ note — `button.t-cm-chart-label` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `button.t-cm-chart-label` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size

## Chart-pie
- ⚪ note — DATA MARK `path.dv-marker.dv-pie-seg.dv-series` — UNMEASURED: path with a free-form `d` — bbox not statically derived
- ⚪ note — DATA MARK `path.dv-marker.dv-pie-seg.dv-series` — UNMEASURED: path with a free-form `d` — bbox not statically derived
- ⚪ note — DATA MARK `path.dv-marker.dv-pie-seg.dv-series` — UNMEASURED: path with a free-form `d` — bbox not statically derived
- ⚪ note — DATA MARK `path.dv-marker.dv-pie-seg.dv-series` — UNMEASURED: path with a free-form `d` — bbox not statically derived
- ⚪ note — DATA MARK `path.dv-marker.dv-pie-seg.dv-series` — UNMEASURED: path with a free-form `d` — bbox not statically derived
- ⚪ note — DATA MARK `path.dv-marker.dv-pie-seg.dv-series` — UNMEASURED: path with a free-form `d` — bbox not statically derived
- ⚪ note — DATA MARK `path.dv-marker.dv-pie-seg.dv-series` — UNMEASURED: path with a free-form `d` — bbox not statically derived
- ⚪ note — DATA MARK `path.dv-marker.dv-pie-seg.dv-series` — UNMEASURED: path with a free-form `d` — bbox not statically derived
- ⚪ note — DATA MARK `path.dv-marker.dv-pie-seg.dv-series` — UNMEASURED: path with a free-form `d` — bbox not statically derived
- ⚪ note — DATA MARK `path.dv-marker.dv-pie-seg.dv-series` — UNMEASURED: path with a free-form `d` — bbox not statically derived

## Chart-sparkline
- ⚪ note — DATA MARK `polyline.dv-series` — UNMEASURED: polyline (trend line): its target is stroke width x hit band, which is a render-axis fact
- ⚪ note — DATA MARK `polyline.dv-series` — UNMEASURED: polyline (trend line): its target is stroke width x hit band, which is a render-axis fact
- ⚪ note — DATA MARK `polyline.dv-series` — UNMEASURED: polyline (trend line): its target is stroke width x hit band, which is a render-axis fact

## Chart-stacked-area
- 🟡 warn — DATA MARK `g.dv-marker` — 8.4x8.4 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 8.4x8.4 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 8.4x8.4 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 8.4x8.4 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 8.4x8.4 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 8.4x8.4 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 8.4x8.4 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 8.4x8.4 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 8.4x8.4 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 8.4x8.4 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 8.4x8.4 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)
- 🟡 warn — DATA MARK `g.dv-marker` — 8.4x8.4 — under the 24 dense-case minimum (<g> wrapper measured from its circle child (circle diameter 2r)) (s116-D1: marks carry the 24 floor, not the 44 target)

## Combobox
- ⚪ note — `li#cb1-o1.cb-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li#cb1-o2.cb-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li#cb1-o3.cb-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li#cb1-o4.cb-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li#cb1-o5.cb-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li#cb1-o6.cb-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li#cb1-o7.cb-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li#cb2-o1.cb-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li#cb2-o2.cb-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li#cb2-o3.cb-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li#cb2-o4.cb-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Command-palette
- ⚪ note — `div#cp1-o1.cp-opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `div#cp1-o2.cp-opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `div#cp1-o3.cp-opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `div#cp1-o4.cp-opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `div#cp1-o5.cp-opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `div#cp2-o1.cp-opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Data-grid
- 🟡 warn — `button.dgs-clear` — 24x24 is under the 44 default (aid-009)
- ⚪ note — `button` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `button` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `button` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `button.full.sort.t-cm-button` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.full.sort.t-cm-button` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.full.sort.t-cm-button` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.full.sort.t-cm-button` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.full.sort.t-cm-button` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Date-picker
- 🟡 warn — `button#dp-open.tail-btn` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button.tail-btn` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button.tail-btn` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button.tail-btn` — ::before hit-expander 36x36 — under the 44 default

## Date-range-picker
- 🟡 warn — `button#dr-open-from.tail-btn` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button#dr-open-to.tail-btn` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button.tail-btn` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button.tail-btn` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button.tail-btn` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button.tail-btn` — ::before hit-expander 36x36 — under the 44 default

## Document-row
- ⚪ note — `a.dr-title.t-cm-label` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.dr-title.t-cm-label` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.dr-title.t-cm-label` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.dr-title.t-cm-label` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.drow-b` — UNMEASURED: one axis declared (autox76), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.drow-b` — UNMEASURED: one axis declared (autox76), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Drawer
- ⚪ note — `button#open` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size

## Dropdown
- ⚪ note — `button#ddTrigger1.trigger` — UNMEASURED: one axis declared (autox52), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button#ddTrigger2.trigger` — UNMEASURED: one axis declared (autox52), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Empty-state
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size

## File-upload
- 🟡 warn — `button.fu-remove` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button.fu-remove` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button.fu-remove` — ::before hit-expander 36x36 — under the 44 default

## Footer
- ⚪ note — `a.arrow` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-ed-body-small` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-ed-body-small` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-ed-body-small` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-ed-body-small` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-ed-body-small` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-ed-body-small` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-ed-body-small` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-ed-body-small` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-ed-body-small` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-ed-body-small` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-ed-body-small` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-ed-body-small` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.em.lnk.t-ed-body-small` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-ed-body-small` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-ed-body-small` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-ed-body-small` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-cm-legal` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-cm-legal` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-cm-legal` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-cm-legal` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-cm-legal` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-cm-legal` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.lnk.t-cm-legal` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Headers
- 🟡 warn — `button` — 40x40 is under the 44 default (aid-009)
- 🟡 warn — `button` — 40x40 is under the 44 default (aid-009)

## Hero
- ⚪ note — `button.cta` — UNMEASURED: one axis declared (autox48), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.arrow` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size

## Input-fields
- 🟡 warn — `button.tail-btn` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button.tail-btn` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button.tail-btn` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button.tail-btn` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button.tail-btn` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button.tail-btn` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button.tail-btn` — ::before hit-expander 36x36 — under the 44 default

## Links
- ⚪ note — `a.lnk` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.lnk` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.lnk` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.arrow` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.arrow.back` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.icon-lnk` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.icon-lnk` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.lnk` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.lnk` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.lnk` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.lnk` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.lnk` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.arrow.back` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.arrow.back` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a.arrow.back` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size

## List-items
- ⚪ note — `button.row` — UNMEASURED: one axis declared (autox76), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.row` — UNMEASURED: one axis declared (autox76), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.row` — UNMEASURED: one axis declared (autox76), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.row` — UNMEASURED: one axis declared (autox76), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.row` — UNMEASURED: one axis declared (autox76), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.is-hover.row` — UNMEASURED: one axis declared (autox76), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.is-pressed.row` — UNMEASURED: one axis declared (autox76), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.row` — UNMEASURED: one axis declared (autox76), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.row` — UNMEASURED: one axis declared (autox76), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Modal-lightbox
- ⚪ note — `button#open` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size

## Modals
- 🟡 warn — `button#close.close` — 36x36 is under the 44 default (aid-009)
- ⚪ note — `button#open` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size

## Multi-select
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default
- ⚪ note — `li#ms1-o1.ms-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li#ms1-o2.ms-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li#ms1-o3.ms-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li#ms1-o4.ms-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li#ms1-o5.ms-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li#ms2-o1.ms-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li#ms2-o2.ms-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li#ms2-o3.ms-opt.t-cm-label` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Navigations
- ⚪ note — `a` — UNMEASURED: one axis declared (autox64), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a` — UNMEASURED: one axis declared (autox64), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a` — UNMEASURED: one axis declared (autox64), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a` — UNMEASURED: one axis declared (autox64), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Notifications
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size

## Popover
- ⚪ note — `button.pop-trigger` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `button.pop-trigger` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `a` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `button.pop-trigger` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size

## Progress-tracker
- ⚪ note — `button#back` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button#next` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size (a @media-conditioned size exists and is NOT measured)

## Quick-actions
- ⚪ note — `button.qa` — UNMEASURED: one axis declared (autox88), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.qa` — UNMEASURED: one axis declared (autox88), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.qa` — UNMEASURED: one axis declared (autox88), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.qa` — UNMEASURED: one axis declared (autox88), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Reorder
- 🟡 warn — `button.handle` — 32x32 is under the 44 default (aid-009)
- 🟡 warn — `button` — 30x30 is under the 44 default (aid-009)
- 🟡 warn — `button` — 30x30 is under the 44 default (aid-009)
- 🟡 warn — `button.handle` — 32x32 is under the 44 default (aid-009)
- 🟡 warn — `button` — 30x30 is under the 44 default (aid-009)
- 🟡 warn — `button` — 30x30 is under the 44 default (aid-009)
- 🟡 warn — `button.handle` — 32x32 is under the 44 default (aid-009)
- 🟡 warn — `button` — 30x30 is under the 44 default (aid-009)
- 🟡 warn — `button` — 30x30 is under the 44 default (aid-009)

## Search-field
- 🟡 warn — `button.clear` — 24x24 is under the 44 default (aid-009)
- 🟡 warn — `button.clear` — 24x24 is under the 44 default (aid-009)

## Selection-controls
- 🟡 warn — `button.chip` — autox32 — the declared axis is under the 44 default (aid-009); the other axis is layout-determined
- 🟡 warn — `button.chip` — autox32 — the declared axis is under the 44 default (aid-009); the other axis is layout-determined
- 🟡 warn — `button.chip` — autox32 — the declared axis is under the 44 default (aid-009); the other axis is layout-determined
- 🟡 warn — `button.chip` — autox32 — the declared axis is under the 44 default (aid-009); the other axis is layout-determined
- 🟡 warn — `button.chip` — autox32 — the declared axis is under the 44 default (aid-009); the other axis is layout-determined
- 🟡 warn — `button.chip` — autox32 — the declared axis is under the 44 default (aid-009); the other axis is layout-determined
- 🟡 warn — `button.chip` — autox32 — the declared axis is under the 44 default (aid-009); the other axis is layout-determined
- 🟡 warn — `button.chip` — autox32 — the declared axis is under the 44 default (aid-009); the other axis is layout-determined
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default

## Sidebar-nav
- ⚪ note — `a.sn-link` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.sn-link` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.sn-link` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.sn-group-toggle` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.sn-link` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.sn-link` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.sn-link` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.sn-link` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Skeleton-loader
- ⚪ note — `button#resolveDemo` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size

## Split-button
- ⚪ note — `button.sb-main.t-cm-button` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.sb-item.t-cm-button` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.sb-item.t-cm-button` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.sb-item.t-cm-button` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.sb-main.t-cm-button` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.sb-item.t-cm-button` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.sb-item.t-cm-button` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.sb-item.t-cm-button` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.sb-main.t-cm-button` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.sb-item.t-cm-button` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.sb-item.t-cm-button` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.is-disabled.sb-main.t-cm-button` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Standing-order-mandate-row
- ⚪ note — `a.mr-payee.t-cm-label` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.mr-payee.t-cm-label` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.mr-payee.t-cm-label` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.mr-payee.t-cm-label` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.mr-payee.t-cm-label` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.mr-payee.t-cm-label` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.mr-payee.t-cm-label` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size (a @media-conditioned size exists and is NOT measured)

## Status-indicator
- ⚪ note — `button#sim.sim` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size

## Tab-bar
- ⚪ note — `a.is-active.tabbar__item` — UNMEASURED: one axis declared (autox56), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.tabbar__item` — UNMEASURED: one axis declared (autox56), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.tabbar__item` — UNMEASURED: one axis declared (autox56), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.tabbar__item` — UNMEASURED: one axis declared (autox56), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.seg__item` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.seg__item` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.seg__item` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `a.seg__item` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size (a @media-conditioned size exists and is NOT measured)

## Table
- ⚪ note — `button` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `button` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `button` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size

## Tabs
- ⚪ note — `button#t1.tab` — UNMEASURED: one axis declared (autox48), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button#t2.tab` — UNMEASURED: one axis declared (autox48), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button#t3.tab` — UNMEASURED: one axis declared (autox48), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button#t4.tab` — UNMEASURED: one axis declared (autox48), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button#t5.tab` — UNMEASURED: one axis declared (autox48), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button#t6.tab` — UNMEASURED: one axis declared (autox48), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button#ovTrigger.overflow__trigger` — UNMEASURED: one axis declared (autox48), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Tags-input
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default

## Tags
- 🟡 warn — `a.link.tag` — autox34.4 — the declared axis is under the 44 default (aid-009); the other axis is layout-determined
- 🟡 warn — `a.link.tag` — autox34.4 — the declared axis is under the 44 default (aid-009); the other axis is layout-determined
- 🟡 warn — `a.link.tag` — autox34.4 — the declared axis is under the 44 default (aid-009); the other axis is layout-determined
- 🟡 warn — `a.link.tag` — autox34.4 — the declared axis is under the 44 default (aid-009); the other axis is layout-determined
- 🟡 warn — `a.link.tag` — autox34.4 — the declared axis is under the 44 default (aid-009); the other axis is layout-determined
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default
- 🟡 warn — `button.x` — ::before hit-expander 24x24 — under the 44 default

## Time-picker
- 🟡 warn — `button#tp-open.tail-btn` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button.tail-btn` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button.tail-btn` — ::before hit-expander 36x36 — under the 44 default
- 🟡 warn — `button.tail-btn` — ::before hit-expander 36x36 — under the 44 default
- ⚪ note — `li.t-cm-figure-5.tp-opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.t-cm-figure-5.tp-opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.t-cm-figure-5.tp-opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `li.t-cm-figure-5.tp-opt` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Timeline
- ⚪ note — `button.t-cm-button.tl-more` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Toast
- ⚪ note — `button#spawnOk` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `button#spawnInfo` — UNMEASURED: no declared box (layout-determined) and no hit-expander — this gate must not guess a size
- ⚪ note — `button.act.t-cm-button.t-cm-slot` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)
- ⚪ note — `button.act.t-cm-button.t-cm-slot` — UNMEASURED: one axis declared (autox44), the other layout-determined (a @media-conditioned size exists and is NOT measured)

## Tooltip
- 🟡 warn — `button.trigger` — ::before hit-expander 24x24 — under the 44 default
- 🟡 warn — `button.trigger` — ::before hit-expander 24x24 — under the 44 default
- 🟡 warn — `button.trigger` — ::before hit-expander 24x24 — under the 44 default

## Video-player
- 🟡 warn — `button` — 32x32 is under the 44 default (aid-009)
- 🟡 warn — `button` — 32x32 is under the 44 default (aid-009)
- 🟡 warn — `button` — 32x32 is under the 44 default (aid-009)

## View-options
- 🟡 warn — `button` — autox40 — the declared axis is under the 44 default (aid-009); the other axis is layout-determined
- 🟡 warn — `button` — autox40 — the declared axis is under the 44 default (aid-009); the other axis is layout-determined

