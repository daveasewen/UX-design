# Typography — usage guidance

> Source: create.hsbc brandhub (authenticated). Captured 2026-06-18 for RAG. Summarised, not verbatim. **Two standards captured, labelled** (per Dave): the **2026 refresh** (`foundations-and-identity/brand-refresh/typography.html`) and the **2025 standard** (`foundations-and-identity/typography.html`). Raw type-scale tokens live in `tokens/typography.json`.

---

## 2026 refresh (current direction)

**Feel:** typography should be **elegant, meticulously crafted and understated** — quietly assuring, conveying sophisticated integrity.

**Typeface:** **Univers Next for HSBC** is the core typeface — a consistent, modern tone across digital and print. (Matches `typography/font-family/default` in the token store.)

### Key takeaways (rules)
1. **Only brand-approved fonts, weights and colours.**
2. **All text must be legible and pass 4.5:1 colour contrast.**
3. **Never use red typography** except within specific digital-toolkit use-cases.
4. **Lighter font weights only for creative headline treatments.**
5. **No uppercase, no italics — use sentence case.**

### Principles
- **Expressive headlines** — use type expressively for emphasis, pace and personality without losing clarity. Favour **lighter weights**; use bolder weights only for occasional emphasis. *Do* favour fewer words for creative headlines; *don't* obscure or break up a word so it's illegible.
- **Balanced bilingual** — creative often sets Latin + Chinese + Arabic to reflect the international footprint. Balance layout, hierarchy, spacing and line length for readability. *Do* aim for similar length in Latin and Chinese so layout feels balanced; *don't* combine two languages on the same line.
- **Clear type hierarchy** — structured use of scale, weight, spacing and placement to show what matters. Distinct headlines in a light-weight typeface; **limit weight levels to the minimum** needed. *Do* limit type-weight levels for clarity; *don't* use too many weights — aim for two main fonts plus a bold option.

### Usage contexts
- **Marketing & social** — clean typography, clear and consistent.
- **Digital** — a consistent typescale creates clear hierarchy across pages (headlines, subheads, body). Directly underpins the `font-1…7` scale.
- **Documents & presentations** — well-defined hierarchy aids readability across brochures, BTL and decks.

### Resources / deeper sub-pages
- Typography specification (min sizes, colours, leading, kerning) — `brand-refresh/typography/specification.html`
- Typefaces (fonts) — `brand-refresh/typography/typefaces.html`
- Creative headlines — `brand-refresh/typography/creative-headlines.html`
- HSBC font collection (downloads) — assets library

---

## 2025 standard

> `foundations-and-identity/typography.html` — "Typography creates consistent and effective communication." Still valid until further notice. (Captured at summary level; the operative rules above carry over — Univers Next for HSBC, sentence case, 4.5:1 contrast, light weights for headlines, restrained weight count. Pull the full 2025 page on demand if a specific 2025-only detail is needed.)

---

## How this maps to the system
- **Univers Next for HSBC + font-1…7 scale** → `tokens/typography.json` (7-step scale, weights, family).
- **Sentence case / no italics / no uppercase / 4.5:1 / red type forbidden** → editorial rules the UX-copy and component layers should enforce.
- **Light weights for headlines, minimal weight count** → matches the components' use of regular/light/medium weights (e.g. Hero font-1 regular, links font-5 medium/light).
