# Component interaction review — sign-off tracker

Durable record of the component-by-component interaction review (gallery frontier).
**Once a component is ✅ signed off, it is locked — we do not reopen it.**

## Method (per component)
1. Review the **HTML snippet** (`snippets/<Name>.reference.html`) live in a browser — check interactivity, responsiveness, visuals. (Source of truth; fully interactive; theme toggle + `@media` + reduced-motion built in.)
2. Dave points at issues → fix the **snippet** (never canon.css directly).
3. Regenerate: `python3 knowledge/canon/gen_canon_components.py` → render → `python3 knowledge/_validate_screen.py --render`.
4. Re-gate the gallery + journey. Green + Dave's eyes → **sign off**.

Issue types we're hunting: **missing interaction decisions** (motion / hover / pressed / focus / open-close), **incomplete / missing** (states, variants, dropped sub-parts), **finesse** (spacing, hierarchy, proportion, colour nuance).

**Review specimens show the component ALIVE + its full variant/state spread (Dave, 2026-07-19).** A review doc that features a component must present it as a *live, working* example and show *every variant and state it carries* — never one frozen instance. The spread is not invented: **read it from the component's meta** (`components/<name>.meta.json` — `props` / `variants` / sizes / documented states), then add theme (light+dark) and motion states (normal / active / reduced-motion). A pick (type size, colour, spacing) can only be judged across the component's real range. A variant that plainly exists but is absent from the meta is itself a finding. Then obey the standard review-doc rule: build clean in `reviews/`, inject the overlay with `_make_review.py`, present the `.REVIEW.html`.

**Template controls — every review carries a light/dark toggle + a responsive-width slider (Dave, 2026-07-19).** The spread shows the variants; the controls let Dave stress the component across theme and viewport. Durable target: bake both into `_review/_review-overlay.html` so every generated review inherits them (tracked in `_FUTURE-STATE`); until then add them to each doc's chrome by hand.

Legend: ⬜ pending · 🔧 in fix · ✅ signed off (locked)

---

## Tranche 1 — Buttons & actions (interactive triggers)
| Component | Status | Signed | Notes |
|---|---|---|---|
| Button | ✅ | 2026-06-29 | Good — promoted (incl. leading-trim) |
| Links | ✅ | 2026-06-29 | Signed off — active = label hover/pressed (underline). Filled-active icon DEFERRED (glyph missing) → _ICON-GAPS.md |
| Tags | ✅ | 2026-06-29 | Good — promoted |
| Quick-actions | ✅ | 2026-06-29 | Good — promoted (Button scale-physics motion added) |
| Badge | ✅ | 2026-06-29 | Good — promoted |
| Status-indicator | ✅ | 2026-06-29 | Good — promoted |

## Tranche 2 — Inputs & selection
| Component | Status | Signed | Notes |
|---|---|---|---|
| Input-fields | ✅ | 2026-06-29 | Good — promoted |
| Search-field | ✅ | 2026-06-29 | Promoted — Boxed + Underline; clear only when value present; native cross suppressed; icon centred |
| Selection-controls | ✅ | 2026-06-29 | Good — promoted |
| Slider | ✅ | 2026-06-29 | Good — promoted |
| View-options | ✅ | 2026-06-29 | Promoted — sliding active indicator; single container border |
| Dropdown | ✅ | 2026-06-29 | Promoted — Underline + Boxed (full-border) variants |

## Tranche 3 — Containers & data display
| Component | Status | Signed | Notes |
|---|---|---|---|
| Cards | ✅ | 2026-06-29 | Promoted — undecorated ghost actions at standard button size (h44/pad20) |
| Account-card | ⏸ defer | | DEFERRED (Dave) — needs more work, not a priority; revisit later |
| Table | ✅ | 2026-06-29 | Promoted — card-collapse left-aligns all data (label + value) |
| List-items | ✅ | 2026-06-29 | Promoted — two-line aligned row (title↔status, desc↔amount); density scales both sides; descenders safe |
| Divider | ✅ | 2026-06-29 | Promoted |
| Accordion | ✅ | 2026-06-29 | Good — promoted |

## Tranche 4 — Navigation & wayfinding
| Component | Status | Signed | Notes |
|---|---|---|---|
| Tabs | ✅ | 2026-06-29 | Good — promoted |
| Navigations | ✅ | 2026-06-29 | Promoted (fine for now; Dave to develop further later) |
| Breadcrumbs | ✅ | 2026-06-29 | Promoted — slash + library-chevron separator versions |
| Pagination | ✅ | 2026-06-29 | Promoted — Button press states (inverting fill + depress) added |
| Headers | ⏸ revisit | 2026-06-29 | Subtitle fixed (regular); DEFERRED — marked for revisit (full header set) |
| Reorder | ✅ | 2026-06-29 | Promoted — pointer drag works (+ keyboard moves). FUTURE: "portfolio-level interactions" pass invited by Dave |

## Tranche 5 — Feedback & overlays
| Component | Status | Signed | Notes |
|---|---|---|---|
| Notifications | ✅ | 2026-06-29 | Promoted — close × first-line aligned (22px) across all; --text-shift 7px optical centre; Global 3 variants (none/close/actions) + flush bottom-right actions; title/desc stack 8px; multi-link stack 10px |
| Modals | ✅ dialog | 2026-06-29 | Promoted AS DIALOG; GAP noted: add true modals + lightboxes (desktop+mobile) from Figma → _COMPONENT-GAPS.md |
| Tooltip | ✅ | 2026-06-29 | Promoted — icon-at-end-of-label canon rule + space-aware positioning |
| Progress-tracker | ✅ | 2026-06-29 | Promoted — reworked to Figma (inline label + continuous red fill) |
| Loading-indicator | ✅ | 2026-06-29 | Promoted (fine for now; Dave to tinker later) |
| Countdown-timer | ✅ | 2026-06-29 | Promoted — butt caps; number centred; animates only final 5s (no pause needed); subtitle regular |

## Tranche 6 — Identity & media
| Component | Status | Signed | Notes |
|---|---|---|---|
| Avatar | ✅ | 2026-06-29 | Good — promoted |
| Hero | ⏸ revisit | 2026-06-29 | Promoted (fine for now); Dave to develop further — marked for revisit |
| Video-player | ✅ | 2026-06-29 | Promoted — square play button + Button scale-physics |

---

## Queued after review — 5 gap-patterns → gated components
Follow the **account-card** template. Components: **summary, tab-bar, action-bar, eyebrow, confirmation/success**.

| Gap-pattern | Status | Signed | Notes |
|---|---|---|---|
| summary | ✅ | 2026-06-30 | Promoted — dl key/value + emphasised total row |
| tab-bar (bottom nav) | ✅ | 2026-06-30 | Promoted — A standard labelled bar + B segmented sliding-pill islands (interactive; View-options easing; full-width; inverting black/white selected; Menu in the exclusive group; Insights added). **ISLANDS marked for REVISIT (Dave)** |
| action-bar | ✅ | 2026-06-30 | Promoted — Back(tertiary,left)+Cancel+Confirm; reflow stacks primary-top/Back-bottom; reuses Button |
| eyebrow | ✅ | 2026-06-30 | Promoted — sentence case (house type rule); leading-trim kicker |
| confirmation/success | ✅ | 2026-06-30 | Promoted (finesse later) — success-solid pop + staggered rise; mobile vertical-centre; desktop variant logged in _COMPONENT-GAPS.md |
