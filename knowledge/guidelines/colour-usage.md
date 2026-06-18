# Colour — application guidance

> Source: create.hsbc brandhub (authenticated) — `foundations-and-identity/colour.html` (2025 standard). Captured 2026-06-18 for RAG. Summarised, not verbatim. **⚠️ A 2026 refreshed colour standard exists** at `foundations-and-identity/brand-refresh/colour.html` — reconcile when doing the brand-refresh pass. This file is *application* guidance; raw token values live in `tokens/colour.json` + `semantic-colour.json`.

## Why colour

Colour creates brand awareness, recall, visual balance and consistency across all media. The palettes act as the **"visual glue"** that delivers consistency and familiarity.

## Key takeaways (application rules)

1. **White and black are the base; HSBC red is applied *tactically*** — to draw the user's attention to key elements. (Matches the token rule: brand red is an accent, never a page background; and the "tactically red" creative-direction principle.)
2. **Always check contrast** when combining/layering colours (text or icons on a background) — correct colour contrast is required.
3. **Use the correct palette for the use case** — e.g. the illustration palette only for illustrations; the data-vis palette only for data. Don't cross-use palettes.

## Palette types

- **Brand palette** — Core + Complementary Red + Complementary Grey.
- **Illustration + Complementary Illustration palettes** — for creating illustrations.
- **Data Visualisation palette** — for graphical representation of data only.
- **RAG palette** — red / amber / green (+ an additional blue), based on the traffic-light system, for communicating **status or severity in UX journeys**.

### Brand palette breakdown
- **Core palette** — the most recognisable, distinctive colours; used for **all** communications.
- **Complementary Red palette** — supports Core; adds depth across owned channels.
- **Complementary Grey palette** — supports all palettes; adds depth and clarity.

### Illustration
- **Illustration palette** — chosen to create harmonious compositions with the brand colours.
- **Complementary Illustration palette** — depicts a **diverse range of skin and hair tones**.

### Data visualisation & RAG
- **Data Visualisation palette** — used **only** for graphical data representations.
- **RAG palette** — red/amber/green + blue; status/severity in journeys.

## Business-segment colour

Segments carry their own colour guidance: **Ultra/High Net Worth (Global Private Banking)**, **Mass Affluent**, **Asset Management**, **Life**.

## How this maps to the token store

- **RAG palette** → `rag/*` tokens (error/warning/success/information + tints + `rag/neutral`). Confirms the Status indicator / Notifications usage. (Token gap: missing `rag/neutral-tint` — see `_DESIGN-SYSTEM-GAPS.md` P4.)
- **Data Visualisation palette** → `data-vis/*` tokens.
- **Core / Complementary Red / Grey** → the brand primitives in `colour.json`; "tactically red" reinforces the `color/primary` accent-only rule and the primitive-leak flag (P5).
- **"Correct palette for use case"** → governance rationale for keeping palettes as distinct token groups.

## Sub-pages (create.hsbc, deeper — pull on demand)
- Brand colours — `foundations-and-identity/colour/brand-colours.html`
- Illustration colours — `foundations-and-identity/colour/illustration.html`
- Data visualisation colours — `foundations-and-identity/colour/data-visualisation.html`
- **2026 refreshed colour standard** — `foundations-and-identity/brand-refresh/colour.html`
- Downloadable palette files (RGB + CMYK) — `assets/collections/hsbc_brand_colourpalettes.html`
