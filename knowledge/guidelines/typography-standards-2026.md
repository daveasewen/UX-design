# Typography (2026) — brand guidance (ingested)

*Source: create.hsbc → Foundations → Brand refresh → Typography
(`brand-refresh/typography.html`), captured 2026-07-02 via Dave's authenticated session
(login-walled; ADR-0005 provenance applies). Engine-era format. 2026 refresh standard —
2025 standards remain usable "until further notice" (parallel-valid, same pattern as colour).
Subpages NOT yet ingested (queued): `typography/typefaces.html`,
`typography/creative-headlines.html`, and the typography **specification** page (minimum
sizes, colours, leading, kerning — the component-relevant numbers live there).*

## Typefaces

**Univers Next for HSBC** is the core typeface (digital + print), visually matched with
**MYing Hei** (Chinese) and **Univers Next Arabic** — one multilingual system. A complete
brand font collection is downloadable on the site (licensed — not fetched; the sandbox
renders with fallbacks regardless, see `_ROBUSTNESS-PORTABILITY.md`).

- ⚠ **Token-store delta:** `tokens/typography.json` carries **Univers** as the primitive —
  the refresh names **Univers Next for HSBC**. Blast radius: the type primitive, every
  snippet's font stack, Sutherland fixtures. Parallel-validity means no forced migration
  yet, but new-work-targets-refresh implies the token store needs a 2026 mode or a
  documented stay-on-2025 decision. Dave's call. [REVIEW] {#type26-001}

## Key takeaways (rules)

- **Only use brand-approved fonts, weights and colours.** [BLOCKING-derivable — font-family
  whitelist; colour side already gated] {#type26-002}
- **All text legible and ≥4.5:1 contrast.** [BLOCKING-derivable — existing text-contrast
  gate, already enforced] {#type26-003}
- **Never use red typography except within specific digital toolkit use-cases.** Sharpens
  the col26 red-text rule: the exception scope is toolkit-defined (e.g. CTA links), not
  designer judgment. [BLOCKING-derivable — red-text check with toolkit-exception allowlist]
  {#type26-004}
- **"We don't use uppercase or italics lettering — use sentence case."** ⚑ This makes the
  house sentence-case rule (and the G5 all-caps advisory check) **source-backed at brand
  level** — and extends it: *italics are also out*. Informs the open all-caps scope ruling
  on Dave's desk: the source is brand-wide, favouring canon-wide over brief-scoped.
  [BLOCKING-derivable — the advisory all-caps rule has its promotion evidence; italics
  check is new] {#type26-005}
- Only use lighter font weights for creative headline treatments; favour lighter weights
  generally, bolder weights only for occasional emphasis (a word, a subheading).
  [ADVISORY-derivable — weight-usage distribution] {#type26-006}

## Principles

- **Expressive headlines** — emphasis, pace, personality without losing clarity; fewer
  words; never obscure or break a word into illegibility. [TASTE — matches refresh
  cheat-sheet; fenced to composition experiments per `_BRAND-REFRESH-DIRECTION.md`]
  {#type26-007}
- **Balanced bilingual** — Latin/Chinese/Arabic given comparable prominence, unified not
  "translated"; balance layout, hierarchy, spacing, line length. [TASTE — no bilingual
  content in the canon yet; becomes contract-relevant for multilingual briefs] {#type26-008}
- **Clear type hierarchy** — scale/weight/spacing/placement signal reading order; limit
  weight levels to the minimum; **max two main fonts with a bold option**.
  [ADVISORY-derivable — countable font/weight census per view] {#type26-009}

## Usage contexts ([TASTE], register/contract framing)

Marketing/social: clean, scannable, mobile-legible. Digital: hierarchy reduces cognitive
load, journeys feel calmer. Documents/presentations: size/weight/spacing differences turn
dense content into a navigable path.

## Cross-references

`typography-usage.md` (legacy pre-engine distillation — superseded in part by this file;
upgrade pending the spec-page ingestion) · `colour-standards-2026.md` (red-text family,
col26-004/005) · `_ADVISORY-SIGNALS.md` + `_validate_advisory.py` (all-caps rule → now has
brand-level promotion evidence) · `tokens/typography.json` (Univers → Univers Next delta) ·
`_BRAND-REFRESH-DIRECTION.md` (expressive headlines, fenced).
