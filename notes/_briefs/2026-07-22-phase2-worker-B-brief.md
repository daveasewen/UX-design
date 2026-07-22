# Phase-2 Worker B brief — FEEDBACK & DATA lane (Alert family unblocked + surfaces)

*Cut by the review-pass session, 2026-07-22 (date from `date`), from `_BUILDOUT-STRATEGY-2026-07-21.md`
Phase 2 + the itinerary. You are a WORKER per `knowledge/_RUNBOOK-parallel-conductor.md`: create only
NEW files, NO git, NO writes to `GOOD-MORNING.md`/`_LIVE-STATE.md`/`_FUTURE-STATE.md`/shared registries.
Receipt at the end (path below). Model: Fable. Your lane is fenced from Worker A's by construction —
you share NO source files with them.*

## Your worklist (ordered; build down it until budget says stop — the cut line goes in your receipt)

| # | Component (itinerary row) | Notes |
|---|---|---|
| 1 | **Alert / inline callout** (68, P1) | UNBLOCKED by R-D20 — the full `rag/{error,warning,information,success}` + `-tint` sets are ruled. Bind them; re-decide NOTHING. Mine `snippets/Notifications` for shape only (it is a LEGACY REFERENCE — do not convert it, §A-AUTH). |
| 2 | **Toast / snackbar** (69, P1) | Transient sibling of 1 — same RAG bindings, distinct chrome. |
| 3 | **Banner** (73, P2) | Page-level persistent third of the family — build while the patterns are warm. |
| 4 | **Skeleton loader** (72, P1) | Perceived-performance placeholder. NOT the loader atom (that's queued to §C·3b) — no spinners here; shimmer/blocks only, motion respects reduced-motion. |
| 5 | **Drawer / side sheet** (70, P1) | Mine `snippets/Modals` (scrim, focus trap, close affordances). Its buttons = button-family membership (partials protocol below). |
| 6 | **Popover** (71, P1) | Rich anchored content — distinct from `snippets/Tooltip`; survey it first. |
| 7 | **Modal — true modals/lightboxes** (63, P1) | EXTENDS `snippets/Modals` — but do NOT edit that file (fence). New variants land as a NEW snippet (e.g. `Modal-lightbox.reference.html`); propose the eventual fold in your receipt. |
| 8 | **Empty state** (54, P1) | No-data / first-run. Illustration = real assets only; if none exists, text-led layout + icon-gap proposal. |
| 9 | **Stat / metric card** (52, P1) | Promote the existing util — grep reviews/fitness-tests for it; mine `snippets/Amount-display` + `Cards`. |
| 10 | **Amount / currency display + money format** (89, P1) | The formatting PRIMITIVE — document the format rules in the snippet; Worker A's amount-input consumes them later. |
| 11 | **Account selector / masked account chip** (90, P1) | Promote from `snippets/Account-card`; masked-number convention from tranches. |

*(Deliberately NOT in wave 1: Data grid (51) + Charts kit (53) — big enough to be their own lanes;
Brand mark (86) — needs the official asset from Dave first, icon-source rule.)*

## Per-component loop (definition of done — every item, no exceptions)

1. **CONSULT then survey:** `python3 knowledge/_consult.py "<component>"` · grep `snippets/`,
   `_proforma/` (tranches ARE Mono — near-canonical, ruling 3), `reviews/` for prior art. Extend,
   never restart. Pattern proofs: `snippets/Button.reference.html` (atom shape),
   `snippets/Icon-button.reference.html` (newest gated atom), `snippets/Cards.reference.html` (surface).
2. **Build the reference snippet** — NEW file `knowledge/snippets/<Name>.reference.html` (check the
   basename is unused in BOTH snippets/ and _proforma/ — basename-keyed gates). Requirements:
   - **Theme-blind:** bind semantic roles via `#token-manifest` + local vars in both
     `[data-theme="light"]` and `"dark"` blocks. NEVER `color/mono/*` direct (ADR-0014), never hexes.
   - **Radius = role tokens** (`border-radius/control|surface|indicator`; 50%/999px idioms literal).
   - **Type = composites only** (`.t-cm-*` — never raw font shorthand; blast-radius gate on type.css).
   - **Grid 4px · sentence case · weights 100/300/400/500/700 (no 600) · white type red-only
     (type26-013) · real icons only · AA floor + state-contrast (active > hover, never colour-alone).**
   - **Full variant/state spread** in the doc (the showroom pane shows it live).
3. **Partials protocol (ADR-0013 — never re-type a sub-atom).** Sub-buttons/pressables: NO local press
   physics CSS (the ratchet census must not grow). Place an EMPTY marker pair on your control selector:
   `/* ===== AUTO-PARTIAL press-physics START (button-family) ===== */` + `END` pair, declare
   `--phys-size` (your control's px), add manifest binds — and put the exact `$members` registry JSON
   line in your RECEIPT. The conductor registers + injects (registry is conductor-only). If
   `gen_component_partials --check` objects to your unregistered markers, comment them
   `<!-- PROPOSED-PARTIAL … -->` and say so in the receipt.
4. **Regenerate + verify:** `python3 knowledge/_build_all.py` → **must exit green** before the next
   component. (Generated surfaces are deterministic; the conductor's final serial build is
   authoritative.) Your new page auto-appears in showroom (category 'More' until the conductor maps
   it — propose the category in your receipt, don't edit `gen_showroom.py`).
5. **Blocked/ambiguous → receipt, don't improvise canon.** Live Dave rulings → receipt VERBATIM.

## Do NOT

Edit `component-types.json` · `_validate_radius.py` · `gen_showroom.py` · any existing snippet
(incl. `Modals`, `Notifications`, `Tooltip`, `Account-card` — mine them, never modify) · tokens
(propose via receipt — promotion is Dave's) · mint a loader atom · touch git or the handoff files.

## Receipt (mandatory, last act)

`notes/_receipts/2026-07-22-phase2-worker-B-feedback.md` — components landed + cut line ·
per-component role/judgment calls · registry `$members` JSON proposals · MIGRATED_SNIPPETS basenames ·
showroom category proposals · icon gaps · open questions · proposed §C lines · NO commits made.
