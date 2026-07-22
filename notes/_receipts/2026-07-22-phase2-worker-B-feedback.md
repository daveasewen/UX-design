# Worker B receipt — Phase-2 wave 1, FEEDBACK & DATA lane

*2026-07-22, 16:11 BST (date from `date`). Fable worker per `_RUNBOOK-parallel-conductor.md` +
brief `notes/_briefs/2026-07-22-phase2-worker-B-brief.md`. NO commits made. NO shared files
edited (registry, gates, gen_showroom, existing snippets, tokens, handoff files all untouched).
All work = NEW files listed below + this receipt.*

## Components landed — 10/11, NO cut line (the 11th was already built)

| # | Component | Files (all NEW) | Gates |
|---|---|---|---|
| 1 | Alert | `snippets/Alert.reference.html` + `components/alert.meta.json` | ✅ |
| 2 | Toast | `snippets/Toast.reference.html` + `components/toast.meta.json` | ✅ |
| 3 | Banner | `snippets/Banner.reference.html` + `components/banner.meta.json` | ✅ |
| 4 | Skeleton loader | `snippets/Skeleton-loader.reference.html` + `components/skeleton-loader.meta.json` | ✅ |
| 5 | Drawer | `snippets/Drawer.reference.html` + `components/drawer.meta.json` | ✅ |
| 6 | Popover | `snippets/Popover.reference.html` + `components/popover.meta.json` | ✅ |
| 7 | Modal lightbox | `snippets/Modal-lightbox.reference.html` + `components/modal-lightbox.meta.json` | ✅ |
| 8 | Empty state | `snippets/Empty-state.reference.html` + `components/empty-state.meta.json` | ✅ |
| 9 | Stat card | `snippets/Stat-card.reference.html` + `components/stat-card.meta.json` | ✅ |
| 10 | Amount / money format | **NOT BUILT — already exists.** `snippets/Amount-display.reference.html` IS itinerary row 89 (its header cites the row; figure-4/5/6 composites + copy-025 + U+2212 all documented there). Building again would duplicate. Status = reference CANDIDATE awaiting Dave's vouch on figure-4/5/6. | n/a |
| 11 | Account selector + masked chip | `snippets/Account-selector.reference.html` + `components/account-selector.meta.json` | ✅ |

**Verification:** final `_build_all.py` **exit 0, 51/51 steps, 54 snippets / 54 metas** (16:10 BST;
includes Worker A's landed files). Per-component I ran the targeted gates (snippet · a11y · grid ·
icons · coverage · blast-radius · partials ratchet) after each build; two full-build reds mid-lane
were **attributable entirely to Worker A's in-flight files** (Form-layout 26px padding + metas
landing after snippets — the shared-live-tree race class; resolved by A before my final build).
Census **32 → 32** (this lane added ZERO press-shaped rules). Blast radius clean (24 selectors, no
escapes). **Render-verify OWED** as project-wide (headless-shell refusal) — verification stood on
gates; Dave reviews live HTML in the showroom.

## Registry $members proposals (conductor-only file; exact JSON per member)

All five files carry an EMPTY `AUTO-PARTIAL press-physics START/END (button-family)` pair,
`--phys-size` in `:root`… actually in the theme-var pattern of each file (see per-file notes), and
manifest binds `--press-travel`/`--press-darken` → `component-type/button-family/press-{travel,darken}`
(validated green). `--check` did NOT object to the unregistered markers (stray markers inert —
confirmed live). Colour-only interim states everywhere (active > hover). Proposed entries:

```json
"Alert":          { "selector": ".alert .x" },
"Toast":          { "selector": ".toast .x, .toast .act" },
"Banner":         { "selector": ".banner .x, .banner .actions .abtn" },
"Drawer":         { "selector": ".drawer-placeholder — see note", "$note": "real selectors: .dbtn, .sheet .close" },
"Popover":        { "selector": ".pop .x" },
"Modal lightbox": { "selector": ".lb-ctl" }
```

Corrected per-file selector map (conductor to normalise into the registry's one-selector-per-member
shape — if multi-selector members aren't supported, register the FIRST and I'll split markers on
the injection pass):

- **Alert** → `.alert .x` (--phys-size:24; declared in both theme blocks alongside travel/darken)
- **Toast** → `.toast .x` + `.toast .act` (--phys-size:44)
- **Banner** → `.banner .x` + `.banner .actions .abtn` (--phys-size:120)
- **Drawer** → `.dbtn` + `.sheet .close` (--phys-size:120; close is 44 — flag if per-selector size is wanted; see open Q3)
- **Popover** → `.pop .x` (--phys-size:24)
- **Modal lightbox** → `.lb-ctl` (--phys-size:44 — Icon-button geometry)
- Empty state → `.ebtn` (--phys-size:120)
- Stat card, Skeleton, Account-selector → NO markers (passive / form-control; see open Q4)

## MIGRATED_SNIPPETS basenames (radius-gate strict list, conductor-only)

All eight bind role tokens exclusively (control/surface/indicator; 50% idiom literal in
Skeleton's avatar bone) — safe to go strict:
`Alert.reference.html` · `Toast.reference.html` · `Banner.reference.html` ·
`Skeleton-loader.reference.html` · `Drawer.reference.html` · `Popover.reference.html` ·
`Modal-lightbox.reference.html` · `Empty-state.reference.html` · `Stat-card.reference.html` ·
`Account-selector.reference.html`

## Showroom category proposals (CATEGORIES is conductor-only)

- **Feedback**: Alert · Toast · Banner · Skeleton loader · Empty state (+ existing Loading-indicator, Notifications[legacy], Status-indicator if the conductor wants the family together)
- **Overlays**: Drawer · Popover · Modal lightbox (+ existing Modals, Tooltip)
- **Data display**: Stat card (+ existing Amount-display, Table, Summary)
- **Forms**: Account-selector (Worker A's lane owns the rest of the category)

## Judgment calls (per component, with the retrieval they stand on)

1. **Alert** — R-D20 bindings verbatim, nothing re-decided. Light roundel marks: error=tint
   knockout (4.71) · warning=near-black (R-D3, 5.76) · success/info=WHITE (5.0/5.03 — their tint
   knockouts fail the 4.5 mark leg at 4.11/3.85). Dark = white-shape/black-mark (the 2026-07-02
   dark roundel ruling, literals like the Legacy reference's enactment). The warning shape-vs-tint
   pair (2.44) is deliberately UNDECLARED — amber exempt by R-D3/R-D6 A′ (noted in manifest $note;
   the declared-pairs-only blind spot is documented, not hidden).
2. **Toast** — NO error variant (Legacy snackbar precedent: errors persist → Alert). Dark glyphs
   stay COLOURED on the elevated neutral ground (the white-shape ruling targets TINTED grounds) —
   **flagged for Dave, see Q1**. Timer pauses on hover/focus (2.2.1).
3. **Banner** — solid R-D20 `-background` fills (Mono precedent: Button is-success). Inks bind the
   most specific ruled role each: error=rag/text/on-dark (the ONE white-type surface, red-only,
   type26-013, 6.02) · warning/info=rag/text/on-light · success=text/on-success (B-D6). Actions XOR
   dismiss (Legacy family shape rule kept). Fill-vs-page undeclared (a page surface is not an indicator).
4. **Skeleton** — one token pair (tertiary/background/hover on page); bones aria-hidden, ONE
   region-level status announcement; reduced-motion kills shimmer AND gradient; no spinners (loader
   atom stays queued §C·3b — not minted).
5. **Drawer** — Modals mechanics mined verbatim (file untouched); `.dbtn` namespaced because `.btn`
   is type.css-bound (blast-radius escape otherwise) — same reason Account-selector's chip is
   `.acchip` not `.chip`. Type via composite markup classes throughout (T-D14 pattern — zero
   type.css edits by this lane).
6. **Popover** — non-modal dialog semantics (no aria-modal, no trap; focus-out closes); Tooltip's
   space-aware placement mechanics shared; the Tooltip/Popover boundary written into both meta
   purposes ("act inside it → Popover").
7. **Modal lightbox** — controls + caption on SURFACE TILES, never bare on scrim (contrast
   token-clean; avoids white-on-scrim type). No prev/next wrap (position stays truthful). Fold
   proposal: **Q2**.
8. **Empty state** — text-led (NO spot-illustration set exists → icon gap below); glyph decorative
   0.4 ink; one action max; no live region (state, not event).
9. **Stat card** — R-D5 retrieval: deltas red/green ONLY; the ARROW wears the colour (3:1 labelled-
   glyph floor, R-D6 A′); delta TEXT stays ink because dark rag/error (3.66) fails 4.5 as text.
   Value = Amount-display primitive verbatim. Promoted from the sme-payments `.flow` improvisations.
10. **Account-selector** — masked convention promoted from Account-card (`···4821` + aria-label
    "ending 4821"); Dropdown field chrome + mode-aware menu elevation; NO press physics (form
    control, not button-family → Q4).

## Icon gaps (for `_ICON-GAPS.md`)

- **Spot-illustration / empty-state set** — no illustration-scale assets exist anywhere in
  `assets/icons/`; Empty-state ships text-led with 48px informative glyphs as anchors. A dedicated
  set (empty inbox, no results, first-run) is the proper fix.
- (No other gaps — every glyph used is a byte-matched library asset: status-icons ×4, close,
  task, search, chevron-left/right/down, arrow-up/down.)

## Open questions for Dave / conductor

- **Q1 (Toast dark glyphs):** the white-shape dark roundel ruling was made on TINTED grounds; Toast
  keeps coloured shapes on the ELEVATED NEUTRAL ground (all ≥3.55 dark). Confirm or extend the
  ruling to elevated surfaces.
- **Q2 (modal family fold):** Modal-lightbox extends Modals as a separate snippet (fence). Propose
  eventual fold into one modal-family snippet (dialog + lightbox variants) OR keep split with a
  shared-mechanics partial once a "dialog-mechanics" registry group exists. Dave's shape call.
- **Q3 (per-selector --phys-size):** Drawer carries buttons (120) AND a close (44) in one file; the
  var is file-scoped in the current pattern. Registering both selectors under one member means one
  size wins unless the close gets a local override (`.sheet .close{--phys-size:44}` — legal, it's
  LOCAL geometry). Conductor to pick the idiom; I left the file-level var at 120.
- **Q4 (field family):** Account-selector (and Worker A's whole lane) = form controls with no press
  physics. Does a `field-family` component-type group accrete next (hover/active border mechanics
  are visibly duplicated across Dropdown/Input-fields/Search-field — observed duplication, ruling 3)?
- **Q5 (Amount-display vouch):** row 89 is DONE but rides on figure-4/5/6 composites still marked
  "PREPARED, awaiting Dave's vouch" — the vouch would flip Amount-display candidate→canon and
  harden Stat-card's value type.
- **Q6 (linked stat card):** tappable/linked Stat-card variant (whole-tile link) deliberately not
  improvised; needs the press/link posture question answered first.
- **Observation (dedup pass):** Tranche-1/2 carry earlier empty-state/toast/callout sketches; the
  queued pro-forma dedup pass (ruling 3) should reconcile them toward these canon snippets.

## Proposed §C lines (conductor merges)

- Feedback & data lane (worker B): **10 components landed gated** (Alert/Toast/Banner/Skeleton/
  Drawer/Popover/Lightbox/Empty-state/Stat-card/Account-selector; row 89 was already built as
  Amount-display). Registry $members + MIGRATED_SNIPPETS + categories proposed in the receipt;
  6 open questions (Toast dark glyphs · modal fold · phys-size idiom · field family · figure vouch ·
  linked stat card); 1 icon gap (spot-illustration set).

*NO commits made. Tree state at receipt time: my 21 new files (10 snippets + 10 metas + this
receipt) + generated surfaces (canon.css AUTO-THEMES + showroom + gate reports) regenerated by the
build — deterministic; conductor's serial build is authoritative.*
