# Accessibility Audit: Gated reference snippets (all 31)
**Standard:** WCAG 2.1 AA (+ 2.5.8 from 2.2, + 2.3.3 advisory) | **Date:** 2026-06-20 | **Method:** static analysis across every `snippets/*.reference.html`

## Summary
Contrast (1.4.3 / 1.4.11) and name/role/value (4.1.2) are already **continuously enforced** by the
existing `_validate_snippets.py` gate (token-resolved contrast pairs + `requiredAria`), so this pass
focused on the criteria those gates don't cover: motion sensitivity, target size, focus, and live regions.

**Issues found:** 30 · **Critical:** 0 · **Major:** 28 (reduced-motion) · **Minor:** 2 (target size)
**All 30 fixed this pass.** A new build gate (`_validate_a11y.py`) now prevents regression.

### Findings

#### Operable
| # | Issue | WCAG | Severity | Resolution |
|---|-------|------|----------|------------|
| 1 | 28 of 31 snippets animate (transition/transform) with **no `prefers-reduced-motion` escape hatch** | 2.3.3 Animation from Interactions | 🟡 Major ×28 | Added a reduced-motion block to all 28 (only Countdown-timer, Loading-indicator, Tabs already had one). Invisible to users who haven't requested reduced motion. |
| 2 | Tags **dismiss button** is 16×16px — below the 24px minimum target | 2.5.8 Target Size (Min) | 🟢 Minor | Added an invisible `::before` overlay expanding the hit area to 24×24. Visible glyph unchanged. |
| 3 | Tooltip **help trigger** is 22×22px — below 24px | 2.5.8 Target Size (Min) | 🟢 Minor | Same `::before` hit-area expander to 24×24. Visible glyph unchanged. |

#### Perceivable — 1.4.1 Use of Color (audited 2026-06-20, all PASS)
| Component | Colour-only risk? | Second cue present |
|---|---|---|
| Status indicator | dot colour | ✅ text label beside every dot (`aria-hidden` dot + visible text) |
| Notifications | severity colour | ✅ distinct icon *shape* (triangle/circle-tick/circle-i) + heading text + `role=alert`/`status` |
| Input fields | error/success colour | ✅ alert/tick icon + help text + `aria-invalid` |
| Links (inline) | link colour | ✅ `text-decoration:underline` (non-colour cue); focus cue is an inset bar, not colour |
| Arrow / back links | — | ✅ directional chevron icon carries meaning |

No fixes needed. Rule written into `guidelines/digital-accessibility-standards.md` to prevent regression
(no naked status dots; pair colour with icon-shape + text; keep links underlined). Note: `rag/warning`
(#FFBB33, ~1.6:1) is only safe *because* it never stands alone — a lone warning dot would fail 1.4.1 **and** 1.4.11.

#### Operable — 2.1.1 Keyboard / 2.4.3 Focus Order (audited 2026-06-20, all PASS)
| Component | Mechanism | Keys verified |
|---|---|---|
| Dropdown | explicit JS (combobox/listbox) | Esc, ↑/↓, Enter/Space, focus moves to selected option + returns to trigger |
| Modals | explicit JS | Esc closes, `focus()` return to trigger |
| Tabs | explicit JS (roving tabindex) | ←/→, Home, End, Tab, Esc |
| Accordion | **native `<button>`** + aria-expanded/controls | Enter/Space fire `click` natively — no custom keydown needed (correct) |
| Reorder | **native `<button>`** move-up/down (2.5.7 drag alternative) + drag handle | Enter/Space on the move buttons; arrow-key reordering not required given explicit controls |
| Selection controls, Pagination, View options, Search, Quick actions, Links, Tags | native `<input>` / `<button>` / `<a>` | native key handling — intentionally not re-implemented |

No defects. Custom keydown logic exists only where the pattern is non-native (combobox, roving tabs, modal Esc);
everything else leans on native semantics, which is the conformant choice. **Not gated** — a static keyboard
gate would false-positive on native-semantics components (Accordion/Reorder above), so this stays an audit, not a check.
Focus-trap completeness + AT announce order remain in the human/AT queue (V3).

#### Passed (verified, no action)
| Criterion | Result |
|---|---|
| 2.4.7 Visible focus | All interactive snippets carry `:focus-visible` (0 missing). |
| 2.5.8 target size — other controls | Modals close 32, Reorder handle 32 / move 30, Search clear 24, Video controls 32 — all ≥24. |
| 1.4.3 / 1.4.11 contrast | Enforced per-snippet by the snippet gate (resolved token pairs, light+dark). |
| 4.1.2 name/role/value | Enforced per-snippet by `requiredAria`. |
| Auto-playing media (2.2.2 / 1.4.2) | Video player has **no** `autoplay`; controls present. |
| Live regions | Countdown-timer, Loading-indicator, Notifications expose status/live semantics. |

### What's now enforced (verification = enforcement)
`_validate_a11y.py` is wired into `_build_all.py` (step 10/11):
- **FAIL (gating):** any snippet that animates without `prefers-reduced-motion`.
- **WARN (reported):** interactive control < 24×24px with no `::before/::after` hit-area expander.
Bite-tested: stripping the reduced-motion block from one snippet turns the gate red; restoring it green.

### Limits of a static pass (still wants a human)
Static analysis catches ~30% of WCAG issues. The following still need manual / AT testing and are
**not** claimed as passed here:
- Real screen-reader announcement order (VoiceOver / NVDA) — especially Dropdown listbox, Modal focus trap, Tabs.
- Actual keyboard focus **order** and focus-return after Modal/Dropdown close (logic present; not AT-verified).
- 200% zoom / reflow (1.4.10) and text-spacing (1.4.12).
- The 4 baseline organisms (Navigations, Headers, Hero, Video player) — see `_VISUAL-CHECK-QUEUE.md`.

### Priority for the human pass
1. **Modal + Dropdown** keyboard/SR behaviour (focus trap, return, listbox semantics) — highest user impact.
2. **Tabs** roving-tabindex + arrow-key model under a screen reader.
3. Reflow/zoom on the organisms.
