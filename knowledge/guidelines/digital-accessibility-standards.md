# Digital accessibility standards (the HSBC framework)

> Source: create.hsbc — `platforms-and-channels/Accessibility_Standards.html`. Captured 2026-06-18 for RAG. Summarised, not verbatim. **This is the dev/engineering conformance standard the component metas cite as the "HSBC Accessibility Framework."** Pairs with `guidelines/accessibility.md` (the brand/inclusive-design + neurodiversity layer).

## The standard (definitive)

- **Minimum permitted level of accessibility = HSBC's digital accessibility framework, based on WCAG 2.2 AA.**
- **Governed by Group Digital Experience and Accessibility.**
- **Applies to ALL HSBC digital projects** — every HSBC digital experience must be accessible.

## Principles

- Digital accessibility = the extent to which a digital experience is **easily used by everyone, regardless of ability**.
- **Universal design:** practices that make an experience better for those with special needs make it better for everyone.
- **Build it in from the start** — accessibility must be planned and built in; retrofitting existing experiences is very costly.

## WCAG 2.2 AA — what this pins for our components

The toolkit moved from WCAG 2.1 to **2.2 AA**, adding success criteria. Several map directly to components already documented:

- **2.5.8 Target Size (Minimum) — 24×24px** (AA): backs the recurring "44px target" guidance (HSBC's 44px exceeds the 24px floor) on tabs, links, pagination, view-options, etc.
- **2.5.7 Dragging Movements** (AA): every drag operation needs a single-pointer alternative → directly the **Reorder** "keyboard/move-up-down alternative" rule, and Quick actions / List reorder.
- **2.4.11 Focus Not Obscured (Minimum)** (AA): focused elements must not be hidden by sticky headers/overlays → relevant to Masthead, Modals, sticky Tabs.
- **3.3.8 Accessible Authentication (Minimum)** (AA): no cognitive-function test for login → relevant to any auth flow.
- (Plus the carried-over 2.1 criteria the metas already cite: 1.4.1 Use of Color, 1.4.3/1.4.11 Contrast, 2.1.1 Keyboard, 2.4.7 Focus Visible, 4.1.2 Name/Role/Value, 4.1.3 Status Messages, 1.4.13 Content on Hover/Focus, etc.)

### Operational rule — 1.4.1 Use of Color (every state-bearing component)
Meaning must **never** be carried by colour alone. Every status/severity/selection signal needs a
**second, non-colour cue** — a text label, a distinct icon *shape*, or a typographic change.
Verified across the gated canon (audit 2026-06-20, all PASS):

- **Status indicator / RAG**: a coloured dot is only conformant **beside a text label** (the dot is `aria-hidden`,
  the text carries meaning). A **standalone status dot with no text is non-conformant** — it fails 1.4.1, and
  because `rag/warning` (#FFBB33) is only ~1.6:1 it also fails 1.4.11 as a lone graphic. Rule: no naked status dots.
- **Notifications / inline errors**: pair colour with a distinct icon *shape* (triangle = error/warning, circle-tick =
  success, circle-i = info) **and** heading/help text; set `aria-invalid` on errored inputs and `role=alert`/`status`.
  Error vs warning must differ by text, not just the triangle's colour.
- **Inline text links**: must carry a non-colour indicator — keep `text-decoration:underline` (with a focus cue that
  isn't colour-only). Links distinguished from body text by colour alone fail 1.4.1.

## Sub-pages (create.hsbc, deeper — pull on demand)
- **New standards** — who they're for and why they matter.
- **WCAG 2.1 → 2.2 changes** — the exact new success criteria added.
- **Legacy standards** — baseline for guiding creation/testing of websites.

## How this maps to the system

- This is the **conformance target** for the whole component graph: every `meta.json` `accessibility` block + `relatedSC` should be read as "must meet **WCAG 2.2 AA**," and new dev is reviewed by the Brand Design Team before release (per the Search field guide).
- Feeds the **compliance knowledge-graph** (rule → component → check → SC → clause): the SC anchors are WCAG 2.2 AA, governed by Group Digital Experience and Accessibility.
- Complements `accessibility.md` (inclusive design / neurodiversity — the "why and beyond-compliance" layer).
