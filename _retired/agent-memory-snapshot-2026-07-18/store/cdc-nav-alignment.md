---
name: cdc-nav-alignment
description: "2026-07-15: Tranche 7 nav tuned to match two CDC (HSBC) Figma frames Dave supplied — top-nav bar + content-heavy mega menu. Mono translation confirmed (red active indicator → ink underbar; comes back as red automatically in branded modes). Review frame widened to 1600px design width."
metadata:
  node_type: memory
  type: project
---

**Dave's target = the CDC HSBC nav frames** (file `CDC_Navigation_UI_Patterns`, key `wlvhMFXSoDAmehMjdbzRil`;
node `216:5182` = horizontal top-nav bar, `216:5505` = mega menu content-heavy). Dave: *"a mono version of both
is a good target, we're not far off tbf."* Decisions (AskUserQuestion): **tune T7 in place** (not standalone specs);
mobile mega stays **accordion** (NOT the frame's drill-in) — one mobile pattern to maintain. Mid-task Dave added:
**"we design for 1600px width, so a masthead can be wider"** → raised the review `.wrap`/slider to 1600.

**Real CDC tokens captured** (from `get_variable_defs`): text/ink `#333333`, active `#DB0011` (red underline), borders
`#d7d8d6`/`#b7b7b7`, fills `#f3f3f3`/`#fafafa`, type = Univers Next for HSBC, Body font-5 16/24 (light 350 / medium 500),
Heading-2 font-2 43/52, spacing padding-large 20 / responsive-medium 24 / web margin 40.

**Mono translation rule (confirmed, consistent with [[apollo-mono]]):** keep the exact structure, swap the **red active
underline → a 2px ink underbar** (`.navlink[aria-current="page"]` → `border-bottom-color:var(--ink)`). Because everything
is mode-governed, red returns automatically in Apollo UI / SC. Dave did not object to the ink assumption.

**Changes made to `Tranche-7-interactive.html` (all 4 gates green, render-verified vs the frames):**
- **Global header (Frame 1):** mobile layout now hamburger-left · logo-centred · person-right (flex `order` + `margin-inline:auto`
  in the `@container gheader (max-width:440px)` block). Desktop unchanged (exposed L1 + ink underbar).
- **Mega menu featured variant (Frame 2 content-heavy):** replaced the old single feature-card with a faithful CDC layout —
  a `.mm-masthead` (brand + person + hamburger, L1 hidden) revealing an exposed `.mm-l1row` (active ink underbar), four
  `.menugroup` L2 columns (`.mm-groups`), and a divided **`.mm-rail` "Journeys"** column (5 items, real sprite icons:
  i-home/i-document/i-location/i-calendar/i-tag — no invented glyphs). New tokens-only CSS; `@container megamenu` reflows the
  rail below at ≤720px.
- **Width:** `.wrap` max-width 920→1600, slider `max`/`value` 920→1600, JS "full" threshold 920→1600.

**Known small divergence (Dave's call pending):** `.menulink` L2 links carry a default underline (heavier than the clean CDC
frame) — left consistent with existing menu styling; offered to switch to underline-on-hover.

**Delivery note:** the aligned file was delivered in chat + written to disk, but the device-bridge write tools **dropped
mid-session** (get_device_info stayed up, commit/artifact/memory tools vanished from the registry) and GitHub Desktop threw
the **stale `.git/index.lock`** error again → cleared by `mv`-ing the lock into `_to_delete/git-locks-20260715b/` (bridge
blocks unlink). Persisted artifact could NOT be updated in place (no update_artifact tool; `create_artifact` refuses an
existing id) — the current version lives on disk + as the chat render; the old `apollo-tranche-7-navigation` artifact is one
version behind. This is the recurring flaky-cloud-bridge issue ([[product-feedback-cowork-parity]]). See [[nav-pattern-catalog]], [[proforma-programme]].
