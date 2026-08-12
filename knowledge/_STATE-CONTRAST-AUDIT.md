# State-contrast audit — rendered hover / pressed states (light + dark)
*Drives each interactive element's real hover/pressed states and measures computed foreground vs effective background. TEXT < 4.5 (large < 3.0) FAILS; svg ICONS < 3.0 WARN (many decorative). Disabled controls skipped (WCAG-exempt). Closes the declared-pairs blind spot (Dave, 2026-06-22).*

**0 text failure(s) across 75 snippet(s).**

**15 DECLARED HOLE(s) — un-hit-testable box(es), reported UNMEASURABLE by name (s129-D3).**

**0 CARRIER failure(s) — declarations that carry meaning by colour alone, plus declarations this gate could not READ (s151-D1).**

## Accordion — ✅ clean

## Account-card — ✅ clean

## Account-selector — ✅ clean

## Action-bar — ✅ clean

## Alert — 🟡 14 declared seat(s) · ⬛ 2 UNMEASURABLE box(es)
- ⬛ UNMEASURABLE (declared hole) — a "Review payment details" — not present in the hit stack at its own sample point (pointer-events:none, or an overlay above it takes the hit). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).
- ⬛ UNMEASURABLE (declared hole) — a "Update contact details" — not present in the hit stack at its own sample point (pointer-events:none, or an overlay above it takes the hit). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).
- 🟡 SEAT (declared, advisory) [light/base] div.alert.err "Payment failed. The paym" — carriers `symbol label` — the seat fill measures 1.31:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/base] div.alert.warn "Statement overdue. Your " — carriers `symbol label` — the seat fill measures 1.24:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/base] div.alert.ok "Payment sent. The transf" — carriers `symbol label` — the seat fill measures 1.2:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/base] div.alert.info "Planned maintenance. Som" — carriers `symbol label` — the seat fill measures 1.22:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/base] div.alert.err "Session expiring. Save y" — carriers `symbol label` — the seat fill measures 1.31:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/base] div.alert.info "A single-line informatio" — carriers `symbol label` — the seat fill measures 1.22:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/base] div.alert.warn "Verify your details. We " — carriers `symbol label` — the seat fill measures 1.24:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/base] div.alert.err "Payment failed. The paym" — carriers `symbol label` — the seat fill measures 1.76:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/base] div.alert.warn "Statement overdue. Your " — carriers `symbol label` — the seat fill measures 2.3:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/base] div.alert.ok "Payment sent. The transf" — carriers `symbol label` — the seat fill measures 2.2:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/base] div.alert.info "Planned maintenance. Som" — carriers `symbol label` — the seat fill measures 2:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/base] div.alert.err "Session expiring. Save y" — carriers `symbol label` — the seat fill measures 1.76:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/base] div.alert.info "A single-line informatio" — carriers `symbol label` — the seat fill measures 2:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/base] div.alert.warn "Verify your details. We " — carriers `symbol label` — the seat fill measures 2.3:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.

## Amount-display — ✅ clean

## Amount-input — 🟡 2 declared seat(s)
- 🟡 SEAT (declared, advisory) [light/base] div.ai-msg.is-ok "Within your available ba" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] div.ai-msg.is-ok "Within your available ba" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote

## Avatar — ✅ clean

## Badge — ✅ clean

## Banner — ⬛ 1 UNMEASURABLE box(es)
- ⬛ UNMEASURABLE (declared hole) — a "See affected services" — not present in the hit stack at its own sample point (pointer-events:none, or an overlay above it takes the hit). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).

## Breadcrumbs — ✅ clean

## Button — ✅ clean

## Cards — ✅ clean

## Chart-bar — ✅ clean

## Chart-boxplot — ✅ clean

## Chart-bullet — ✅ clean

## Chart-butterfly-h — ✅ clean

## Chart-butterfly-v — ✅ clean

## Chart-candlestick — ✅ clean

## Chart-combo — ✅ clean

## Chart-donut — ✅ clean

## Chart-histogram — ✅ clean

## Chart-line — ✅ clean

## Chart-pie — ✅ clean

## Chart-scatter — ✅ clean

## Chart-sparkline — ✅ clean

## Chart-stacked-area — ✅ clean

## Confirmation — 🟡 2 declared seat(s)
- 🟡 SEAT (declared, advisory) [light/base] div.confirm "Payment sent
    £250.00" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] div.confirm "Payment sent
    £250.00" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote

## Countdown-timer — ✅ clean

## Data-grid — 2 icon warn(s) · 🟡 4 MARK SKIP(s) · ⬛ 1 UNMEASURABLE box(es)
- 🟡 icon [dark/hover] 1.27:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.27:1 (need 3.0) (decorative)
- 🟡 MARK SKIP (declared, s152-D1) [light/hover] svg — no descendant shape paints the fill this svg declares, so it is not a surface any mark sits on (declared fill: `rgb(0, 0, 0)`). The mark leg did NOT run on this shape, and this line is the receipt.
- 🟡 MARK SKIP (declared, s152-D1) [light/pressed] svg — no descendant shape paints the fill this svg declares, so it is not a surface any mark sits on (declared fill: `rgb(0, 0, 0)`). The mark leg did NOT run on this shape, and this line is the receipt.
- 🟡 MARK SKIP (declared, s152-D1) [dark/hover] svg — no descendant shape paints the fill this svg declares, so it is not a surface any mark sits on (declared fill: `rgb(0, 0, 0)`). The mark leg did NOT run on this shape, and this line is the receipt.
- 🟡 MARK SKIP (declared, s152-D1) [dark/pressed] svg — no descendant shape paints the fill this svg declares, so it is not a surface any mark sits on (declared fill: `rgb(0, 0, 0)`). The mark leg did NOT run on this shape, and this line is the receipt.
- ⬛ UNMEASURABLE (declared hole) — svg — no on-screen box at measurement time (zero-size, or entirely outside the viewport). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).

## Date-picker — 4 icon warn(s)
- 🟡 icon [dark/hover] 1.21:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.21:1 (need 3.0) (decorative)
- 🟡 icon [dark/hover] 1.34:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.34:1 (need 3.0) (decorative)

## Date-range-picker — 4 icon warn(s)
- 🟡 icon [dark/hover] 1.21:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.21:1 (need 3.0) (decorative)
- 🟡 icon [dark/hover] 1.34:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.34:1 (need 3.0) (decorative)

## Divider — ✅ clean

## Drawer — ✅ clean

## Dropdown — ✅ clean

## Empty-state — ✅ clean

## Eyebrow — ✅ clean

## File-upload — 🟡 2 declared seat(s) · 2 icon warn(s)
- 🟡 icon [dark/hover] 1.11:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.11:1 (need 3.0) (decorative)
- 🟡 SEAT (declared, advisory) [light/base] span.fstate "Uploaded" — carriers `symbol` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] span.fstate "Uploaded" — carriers `symbol` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote

## Form-layout — 🟡 4 declared seat(s) · 2 icon warn(s) · ⬛ 1 UNMEASURABLE box(es)
- 🟡 icon [dark/hover] 1.11:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.11:1 (need 3.0) (decorative)
- ⬛ UNMEASURABLE (declared hole) — span#f-name-tip.tipbody "Match the name on the re" — not present in the hit stack at its own sample point (pointer-events:none, or an overlay above it takes the hit). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).
- 🟡 SEAT (declared, advisory) [light/base] div#s-err-msg.fl-msg "Enter a valid sort code," — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [light/base] div.fl-msg.is-ok "Sort code recognised — H" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] div#s-err-msg.fl-msg "Enter a valid sort code," — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] div.fl-msg.is-ok "Sort code recognised — H" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote

## Headers — ✅ clean

## Hero — ✅ clean

## Icon-button — ⬛ 1 UNMEASURABLE box(es)
- ⬛ UNMEASURABLE (declared hole) — svg — not present in the hit stack at its own sample point (pointer-events:none, or an overlay above it takes the hit). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).

## Input-fields — 🟡 2 declared seat(s) · 4 icon warn(s) · ⬛ 1 UNMEASURABLE box(es)
- 🟡 icon [dark/hover] 1.21:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.21:1 (need 3.0) (decorative)
- 🟡 icon [dark/hover] 1.34:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.34:1 (need 3.0) (decorative)
- ⬛ UNMEASURABLE (declared hole) — span#b1tip.tip "Enter the amount you wan" — not present in the hit stack at its own sample point (pointer-events:none, or an overlay above it takes the hit). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).
- 🟡 SEAT (declared, advisory) [light/base] div.ufield.is-ok "Email address
      
   " — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] div.ufield.is-ok "Email address
      
   " — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote

## Links — ✅ clean

## List-items — 🟡 30 declared seat(s)
- 🟡 SEAT (declared, advisory) [light/base] span.status.warn "Pending" — carriers `label` — the seat fill measures 1.24:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/base] span.status.err "Declined" — carriers `label` — the seat fill measures 1.31:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/base] span.status.ok "Received" — carriers `label` — the seat fill measures 1.2:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/base] span.status.ok "Approved" — carriers `label` — the seat fill measures 1.2:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/base] span.status.ok "Approved" — carriers `label` — the seat fill measures 1.06:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/base] span.status.ok "Approved" — carriers `label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [light/hover] span.status.warn "Pending" — carriers `label` — the seat fill measures 1.08:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/pressed] span.status.warn "Pending" — carriers `label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [light/hover] span.status.err "Declined" — carriers `label` — the seat fill measures 1.15:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/pressed] span.status.err "Declined" — carriers `label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [light/hover] span.status.ok "Received" — carriers `label` — the seat fill measures 1.06:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/pressed] span.status.ok "Received" — carriers `label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [light/hover] span.status.ok "Approved" — carriers `label` — the seat fill measures 1.06:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/pressed] span.status.ok "Approved" — carriers `label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [light/hover] span.status.ok "Approved" — carriers `label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] span.status.warn "Pending" — carriers `label` — the seat fill measures 2.01:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/base] span.status.err "Declined" — carriers `label` — the seat fill measures 1.53:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/base] span.status.ok "Received" — carriers `label` — the seat fill measures 1.92:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/base] span.status.ok "Approved" — carriers `label` — the seat fill measures 1.92:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/base] span.status.ok "Approved" — carriers `label` — the seat fill measures 1.83:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/base] span.status.ok "Approved" — carriers `label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/hover] span.status.warn "Pending" — carriers `label` — the seat fill measures 1.92:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/pressed] span.status.warn "Pending" — carriers `label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/hover] span.status.err "Declined" — carriers `label` — the seat fill measures 1.46:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/pressed] span.status.err "Declined" — carriers `label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/hover] span.status.ok "Received" — carriers `label` — the seat fill measures 1.83:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/pressed] span.status.ok "Received" — carriers `label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/hover] span.status.ok "Approved" — carriers `label` — the seat fill measures 1.83:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/pressed] span.status.ok "Approved" — carriers `label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/hover] span.status.ok "Approved" — carriers `label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote

## Loading-indicator — ✅ clean

## Modal-lightbox — ✅ clean

## Modals — ✅ clean

## Navigations — ✅ clean

## Notifications — ✅ clean

## Pagination — ✅ clean

## Popover — ✅ clean

## Progress-tracker — ✅ clean

## Quick-actions — ✅ clean

## Reorder — ✅ clean

## Search-field — ✅ clean

## Secure-entry — 🟡 2 declared seat(s)
- 🟡 SEAT (declared, advisory) [light/base] div.se-msg.is-ok "Code verified." — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] div.se-msg.is-ok "Code verified." — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote

## Segmented-control — ✅ clean

## Selection-controls — 6 icon warn(s) · 🟡 4 MARK SKIP(s)
- 🟡 icon [light/hover] 1:1 (need 3.0)
- 🟡 icon [dark/hover] 1.21:1 (need 3.0)
- 🟡 icon [dark/pressed] 1.34:1 (need 3.0)
- 🟡 icon [dark/pressed] 1.21:1 (need 3.0)
- 🟡 icon [dark/hover] 1.34:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 2.3:1 (need 3.0) (decorative)
- 🟡 MARK SKIP (declared, s152-D1) [light/hover] svg — no descendant shape paints the fill this svg declares, so it is not a surface any mark sits on (declared fill: `rgb(0, 0, 0)`). The mark leg did NOT run on this shape, and this line is the receipt.
- 🟡 MARK SKIP (declared, s152-D1) [light/pressed] svg — no descendant shape paints the fill this svg declares, so it is not a surface any mark sits on (declared fill: `rgb(0, 0, 0)`). The mark leg did NOT run on this shape, and this line is the receipt.
- 🟡 MARK SKIP (declared, s152-D1) [dark/hover] svg — no descendant shape paints the fill this svg declares, so it is not a surface any mark sits on (declared fill: `rgb(0, 0, 0)`). The mark leg did NOT run on this shape, and this line is the receipt.
- 🟡 MARK SKIP (declared, s152-D1) [dark/pressed] svg — no descendant shape paints the fill this svg declares, so it is not a surface any mark sits on (declared fill: `rgb(0, 0, 0)`). The mark leg did NOT run on this shape, and this line is the receipt.

## Skeleton-loader — ✅ clean

## Slider — ✅ clean

## Stat-card — 🟡 8 declared seat(s)
- 🟡 SEAT (declared, advisory) [light/base] span.delta.up "+12.4% upvs February" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [light/base] span.delta.down "−3.1% downvs February" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [light/base] span.delta.up "+2 upthis month" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [light/base] span.delta.down "−1 downthis month" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] span.delta.up "+12.4% upvs February" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] span.delta.down "−3.1% downvs February" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] span.delta.up "+2 upthis month" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] span.delta.down "−1 downthis month" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote

## Status-indicator — 🟡 6 declared seat(s)
- 🟡 SEAT (declared, advisory) [light/base] div.stat.ok "Approved" — carriers `label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [light/base] div.stat.warn "Pending review" — carriers `label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [light/base] div.stat.inf "In progress" — carriers `label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] div.stat.ok "Approved" — carriers `label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] div.stat.warn "Pending review" — carriers `label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] div.stat.inf "In progress" — carriers `label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote

## Stepper — ✅ clean

## Summary — ✅ clean

## Tab-bar — 4 icon warn(s) · ⬛ 3 UNMEASURABLE box(es)
- 🟡 icon [light/hover] 1:1 (need 3.0) (decorative)
- 🟡 icon [light/pressed] 1:1 (need 3.0) (decorative)
- 🟡 icon [dark/hover] 1.3:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.3:1 (need 3.0) (decorative)
- ⬛ UNMEASURABLE (declared hole) — svg — not present in the hit stack at its own sample point (pointer-events:none, or an overlay above it takes the hit). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).
- ⬛ UNMEASURABLE (declared hole) — svg.ic-fill — not present in the hit stack at its own sample point (pointer-events:none, or an overlay above it takes the hit). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).
- ⬛ UNMEASURABLE (declared hole) — svg.ic-line — not present in the hit stack at its own sample point (pointer-events:none, or an overlay above it takes the hit). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).

## Table — ⬛ 5 UNMEASURABLE box(es)
- ⬛ UNMEASURABLE (declared hole) — th "Account number" — no on-screen box at measurement time (zero-size, or entirely outside the viewport). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).
- ⬛ UNMEASURABLE (declared hole) — th "Account" — no on-screen box at measurement time (zero-size, or entirely outside the viewport). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).
- ⬛ UNMEASURABLE (declared hole) — th "Sort code" — no on-screen box at measurement time (zero-size, or entirely outside the viewport). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).
- ⬛ UNMEASURABLE (declared hole) — th "Type" — no on-screen box at measurement time (zero-size, or entirely outside the viewport). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).
- ⬛ UNMEASURABLE (declared hole) — th.num "Available balance" — no on-screen box at measurement time (zero-size, or entirely outside the viewport). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).

## Tabs — ✅ clean

## Tags — ✅ clean

## Textarea — ✅ clean

## Time-picker — 2 icon warn(s)
- 🟡 icon [dark/hover] 1.21:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.21:1 (need 3.0) (decorative)

## Toast — 🟡 10 declared seat(s)
- 🟡 SEAT (declared, advisory) [light/base] div.toast.ok "Payment sent." — carriers `symbol label` — the seat fill measures 1:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/base] div.toast.info "Draft saved automaticall" — carriers `symbol label` — the seat fill measures 1:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/base] div.toast.warn "Connection is unstable." — carriers `symbol label` — the seat fill measures 1:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/base] div.toast.ok "Message archived.Undo" — carriers `symbol label` — the seat fill measures 1:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [light/base] div.toast.info "New version available.Re" — carriers `symbol label` — the seat fill measures 1:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/base] div.toast.ok "Payment sent." — carriers `symbol label` — the seat fill measures 1.15:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/base] div.toast.info "Draft saved automaticall" — carriers `symbol label` — the seat fill measures 1.15:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/base] div.toast.warn "Connection is unstable." — carriers `symbol label` — the seat fill measures 1.15:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/base] div.toast.ok "Message archived.Undo" — carriers `symbol label` — the seat fill measures 1.15:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.
- 🟡 SEAT (declared, advisory) [dark/base] div.toast.info "New version available.Re" — carriers `symbol label` — the seat fill measures 1.15:1 against what is painted beneath it. ADVISORY, never a failure: under s151-D1 the status fill's own background contrast is SECONDARY because the symbol and label carry the meaning. The measurement is reported, not a prescription — this gate does not say what the value should be.

## Tooltip — 🟡 4 MARK SKIP(s)
- 🟡 MARK SKIP (declared, s152-D1) [light/hover] svg — the svg has no painted fill at all (fill is absent or none), so there is no shape for a mark to sit on (declared fill: `none`). The mark leg did NOT run on this shape, and this line is the receipt.
- 🟡 MARK SKIP (declared, s152-D1) [light/pressed] svg — the svg has no painted fill at all (fill is absent or none), so there is no shape for a mark to sit on (declared fill: `none`). The mark leg did NOT run on this shape, and this line is the receipt.
- 🟡 MARK SKIP (declared, s152-D1) [dark/hover] svg — the svg has no painted fill at all (fill is absent or none), so there is no shape for a mark to sit on (declared fill: `none`). The mark leg did NOT run on this shape, and this line is the receipt.
- 🟡 MARK SKIP (declared, s152-D1) [dark/pressed] svg — the svg has no painted fill at all (fill is absent or none), so there is no shape for a mark to sit on (declared fill: `none`). The mark leg did NOT run on this shape, and this line is the receipt.

## Video-player — 2 icon warn(s)
- 🟡 icon [light/hover] 1:1 (need 3.0) (decorative)
- 🟡 icon [light/pressed] 1:1 (need 3.0) (decorative)

## View-options — ✅ clean

---
**⬛ 15 DECLARED HOLE(s) — UNMEASURABLE, `s129-D3` (Dave, #129).** Each box above is not hit-testable — it has no on-screen geometry, or it opts out of hit testing (`pointer-events:none`), or something over it takes the hit — so the paint stack beneath it CANNOT BE OBSERVED. Every one is listed BY NAME with its measured reason. The pre-2026-08-07 ancestor-only walk still runs over them, so no failure is waived and no threshold moved; but an overlapping sibling would still be missed, and those readings may NOT be quoted as hit-stack measurements. ⛔ Dave ruled DECLARE, not REFUSE: refusing them would have turned ~60 measured records into nothing, and publishing the fallback number as if it were the real one is the invented-number class this gate exists to kill. The count above is RE-READ off this artefact and asserted equal to the number of ⬛ lines on every write — a hole that goes quiet is a failed write, not a clean run.

---
**s151-D1 — THE MEANING-CARRIER VOCABULARY (Dave, #151).** The rule this gate enforces, quoted: "colour alone must not carry meaning" — NOT "every surface must clear 4.5". A composition may declare `data-carries="symbol label"` on the element that seats meaning on a status colour; legal carriers are `symbol`, `label`, `colour`. Three clauses: (a) REDUNDANCY — a declaration naming no carrier other than colour, or a declared seat containing neither a symbol nor a label, is a HARD FAIL reading "state carries meaning by colour alone"; (b) CARRIER LEGIBILITY — the symbol and label keep their normal thresholds (text 4.5, icon 3.0) against THEIR backgrounds and still ❌ if they miss; (c) SEAT DEMOTION — the declared seat's own fill reading is ADVISORY 🟡, never ❌. ⛔ Clause (c) applies ONLY where a valid declaration exists: an UNDECLARED seat behaves exactly as it did before this change, because nothing may pass by silence. An unreadable declaration — empty, or naming a word outside the legal set, or claiming a symbol/label the DOM does not contain — is a NAMED failure, never a default. The count above is RE-READ off this artefact and asserted equal to the carrier lines in the body on every write.
