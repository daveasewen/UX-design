# Phase-2 Worker A brief — FORMS & ENTRY lane (the biggest single gap)

*Cut by the review-pass session, 2026-07-22 (date from `date`), from `_BUILDOUT-STRATEGY-2026-07-21.md`
Phase 2 + the itinerary. You are a WORKER per `knowledge/_RUNBOOK-parallel-conductor.md`: create only
NEW files, NO git, NO writes to `GOOD-MORNING.md`/`_LIVE-STATE.md`/`_FUTURE-STATE.md`/shared registries.
Receipt at the end (path below). Model: Fable. Your lane is fenced from Worker B's by construction —
you share NO source files with them.*

## Your worklist (ordered; build down it until budget says stop — the cut line goes in your receipt)

| # | Component (itinerary row) | Notes |
|---|---|---|
| 1 | **Form layout + validation** (13, P1) | Field groups, inline + form-level errors. THE biggest gap. Mine `snippets/Input-fields` + tranche form patterns first. Error colour = `rag/error*` set (R-D20); input-error flex slot is a DECLARED null (ADR-0010) — bind the semantic role, don't mint values. |
| 2 | **Number / currency (amount) input** (17, P1) | Banking-critical. Mine `snippets/Amount-display` for the money-format conventions. |
| 3 | **Textarea** (20, P1) | Smallest item — pattern-match Input-fields exactly. |
| 4 | **OTP / PIN / secure entry** (19, P1) | Mine `_proforma/Tranche-9` (secure entry) — it exists, survey it BEFORE building. |
| 5 | **Date picker** (14, P1) | Core banking input. |
| 6 | **Date-range picker** (15, P1) | Extends 5 — build after it, share its structure. |
| 7 | **Time picker** (16, P1) | Payments scheduling. |
| 8 | **File upload / dropzone** (18, P1) | Document journeys. Icons: sprite + manifest ONLY (icon gate) — a missing glyph goes in `_ICON-GAPS.md` proposal via receipt, never invented. |
| 9 | **Stepper (interactive)** (34, P1) | Progress-tracker is display-only; this DRIVES flows. Consume Progress-tracker's reworked dots↔line visuals; Back/Next buttons = button-family membership (see partials protocol). |

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

Edit `component-types.json` · `_validate_radius.py` · `gen_showroom.py` · any existing snippet ·
tokens (propose via receipt — promotion is Dave's) · mint a loader atom (queued to the button-states
finesse pass, §C·3b) · touch git or the handoff files.

## Receipt (mandatory, last act)

`notes/_receipts/2026-07-22-phase2-worker-A-forms.md` — components landed + cut line · per-component
role/judgment calls · registry `$members` JSON proposals · MIGRATED_SNIPPETS basenames · showroom
category proposals · icon gaps · open questions · proposed §C lines · NO commits made.
