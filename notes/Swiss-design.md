---
name: swiss-design-system
description: Apply this Swiss / International Style design system when building HTML pages, brochure layouts, research documents, or other web deliverables that need disciplined typographic structure. Use it whenever the task is to build, restyle, or create a visual layout in this idiom — including full pages, single sections, or component restyling. Trigger even for partial tasks like "add a section" or "restyle this component" when the layout should follow a Swiss-style grid system.
version: 2.0
---

# Swiss Design System

A Swiss / International Style design system for brochure-ware, research documents, and structured web layouts. It is typography-led: weight, scale, and tracking carry the layout, with colour reduced to a single accent. The system is presented spec-first — every value below is concrete, but the palette and accent colour are intended to be swapped per project. Replace the accent and font stack with project values; the structural rules, spacing, layout patterns, and typographic discipline are the transferable core.

## How to use this file

Paste it into an LLM's context, or keep it open as a reference, when building any layout in this idiom. It is self-contained: the two reference layouts described below are explained in full prose, so you do not need any external files to apply them. Where a value is project-specific (the accent colour, the font), substitute your own and keep everything else.

## Reference layouts

The system is built around two layout archetypes. They are described here in full so they can be reconstructed from prose alone — there are no external files to open.

### Archetype A — Brochure hero layout

A single marketing or proposition page. Top to bottom:

1. **Sticky nav** — white, 1px bottom border, logo or wordmark left, links centre, a single call-to-action right.
2. **Hero** — opens with the label pattern (accent dash + uppercase eyebrow), then a large heading at title scale, then a 2×2 grid of statistics rendered as ultra-light large numerals with small caption labels beneath each.
3. **Proposition split** — a 3-column grid (heading | thin vertical divider | body) carrying the page's central statement.
4. **Feature strip** — a 4-column card grid on a light-grey background, 1px gaps between cells, each cell an index number, title, short description, and arrow; cells turn white on hover.
5. **Insight / quote** — a single extracted pull quote, set off above by a hairline rule.
6. **Footer.**

Every major section is separated from the next by a full-width 1px hairline rule, not merely a gap. The spatial signature is the alternation between full-width bands and split grids, which sets the reading pace.

### Archetype B — Research document profile

A long-form analytical profile of a single subject (e.g. a competitor, a product, a case). Top to bottom:

1. **Sticky nav with back-link** — same nav component, but the left side is a back-link plus the category context the profile sits within.
2. **Profile header** — a 2-column block: subject name and organisation left, tagline and metadata right.
3. **Diagram section** — a label aside paired with a framed diagram or schematic.
4. **Dimension sections** — repeated 1/3 : 2/3 splits. The left third holds a large decorative index numeral and the dimension label; the right two-thirds hold the analysis body. Each dimension is one section.
5. **Claim comparison section** — a full-width light-grey band, 1/3 : 2/3 split: left holds a label and a large verdict statement, right holds analysis plus a two-cell distinction grid (see layout patterns).
6. **Footer nav** — previous / next.

The signature here is the repeated 1/3 : 2/3 rhythm down the page, with the decorative index numerals giving the eye an anchor on each section.

When building new work, model the spatial logic of whichever archetype fits — not just the token values.

## Colour tokens

```css
/* Core */
--accent: #DB0011;   /* PROJECT ACCENT — swap per project. Used sparingly, accent only. */
--black:  #000000;
--white:  #FFFFFF;

/* Optional darker accent shades — accent use only */
--accent-2: #BA1110;
--accent-3: #730014;

/* Neutrals */
--grey-1: #F3F3F3;   /* backgrounds, contained sections */
--grey-2: #EDEDED;   /* borders, dividers */
--grey-3: #D7D8D6;   /* secondary borders, pull quote rules */
--grey-4: #B7B7B7;   /* decorative only — FAILS WCAG on white */
--grey-5: #9B9B9B;   /* decorative only — FAILS WCAG on white */
--grey-6: #767676;   /* minimum safe for text (4.48:1, AA passes) */
--grey-7: #545454;   /* safe for text */
--grey-8: #333333;   /* safe for text */
```

### Colour rules

**Accent — accent only. Never a background fill.** Use for:

- Section labels / eyebrows (the —— LABEL pattern)
- Active nav indicator (left border)
- Progress bar
- Comparison label
- A single underline emphasis moment (max one per page)
- The "ours" head in a distinction grid

**Black** — all body copy, headings, and UI text. The default for everything that communicates.

**Greys** — non-copy use only (borders, dividers, background fills, decorative large numbers, SVG diagram internals). Grey-6 is the minimum for any text that must appear (e.g. secondary nav links, footer legal). Prefer black.

**Dark backgrounds (black, grey-8)** — white text is permitted and required.

> Note on the example accent: #DB0011 is a strong red that passes AA on white at 5.08:1. If you substitute a different accent, re-check its contrast (see WCAG section) before using it for labels or any text.

## Typography

Font stack: `"Helvetica Neue", Helvetica, Arial, sans-serif`

Substitute the project's licensed grotesque if available, keeping the fallback chain, e.g. `"Univers Next", "Helvetica Neue", Helvetica, Arial, sans-serif`

### Type scale

| Token | px | rem |
|---|---|---|
| display | 96 | 6rem |
| title1 | 84 | 5.25rem |
| title2 | 57 | 3.5625rem |
| head1 | 43 | 2.6875rem |
| head2 | 34 | 2.125rem |
| head3 | 19 | 1.1875rem |
| body1 | 16 | 1rem |
| caption1 | 14 | 0.875rem |
| caption2 | 12 | 0.75rem |

### Weight scale (named)

thin (100) · light (300) · regular (400) · medium (500) · bold (700)

### Copy weight rule

All copy defaults to **regular (400)**. Do not use thin or light as a default body weight.

### Emphasis rule — DORMANT BY DEFAULT

Do not apply emphasis styling unless it is explicitly requested.

When emphasis IS requested, apply the weight pairing rule:

**≤ 24px** (body1, caption1, caption2, head3): pairs must be **two named weights apart**

- light (300) + medium (500)
- regular (400) + bold (700)

**> 24px** (head2, head1, title2, title1, display): pairs must be **one named weight apart**

- thin (100) + light (300)
- light (300) + regular (400)
- regular (400) + medium (500)
- medium (500) + bold (700)

The receding weight takes the grey-5/grey-6 colour; the emphasis weight is black. This pattern should only appear on display headings when requested — never in body copy.

### Letter spacing

- display / title1 / title2: 0em — do not tighten
- head1 / head2: 0em or -0.01em max
- head3: 0em
- Labels / eyebrows (caps): 0.12em–0.16em
- Body: 0em
- Nav / button: 0.04em–0.06em

### Line height

- Display / titles: 1.0–1.08
- Heads: 1.1–1.2
- Body: 1.7–1.8
- Captions: 1.5–1.6

## Spacing system (8px base)

```css
--s1: 0.5rem;   /*  8px */
--s2: 1rem;     /* 16px */
--s3: 1.5rem;   /* 24px */
--s4: 2rem;     /* 32px */
--s5: 3rem;     /* 48px */
--s6: 4rem;     /* 64px */
--s7: 6rem;     /* 96px */
--s8: 8rem;     /* 128px */

--max-width: 1200px;
--gutter: 2rem;
```

Section padding: major sections use `var(--s7)` top/bottom. Minor sections use `var(--s5)` or `var(--s6)`. Never compress below `var(--s5)` between major sections. White space is structural, not decorative.

## Layout patterns

### The label pattern

Opens every section. Accent dash + uppercase small-caps label.

```html
<p class="label">Section name</p>
```

```css
.label {
  font-size: var(--caption2);
  font-weight: 500;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent);
  display: flex;
  align-items: center;
  gap: var(--s1);
}
.label::before {
  content: '';
  display: inline-block;
  width: 20px;
  height: 1px;
  background: var(--accent);
}
```

### Left / right split (proposition)

3-col grid: heading | divider | body. Used for section-opening statements.

```css
.proposition {
  display: grid;
  grid-template-columns: 3fr 1fr 4fr;
  gap: var(--s6);
  align-items: start;
}
```

The divider column contains a 1px left border element, minimum height 120px.

### Left / right split (dimension)

1/3 : 2/3 split. Label + large decorative index left, body content right. Used for analysis sections in research documents.

```css
.dimension .wrap {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: var(--s6);
  align-items: start;
}
```

### Feature / card grid

4-column grid on grey-1 background with 1px grey-2 gaps between cells. Each cell: index label (accent), title, description, arrow. Hover: cell background transitions to white.

### Stat display

Large numerals at head1 scale, weight 200 (ultra-light). Grouped in a 2×2 grid. Stat labels in caption2, grey-5 — a decorative context, so the WCAG exception applies.

### Pull quote

Extracted from adjacent body text. Sits below the body column. Border-top grey-2, padding-top. Font at head3 scale, weight regular. Colour: black.

### Distinction grid

Two-cell comparison. 1px grey-3 gap between cells on white background. Left cell: the alternative (grey label). Right cell: the preferred option (accent label). Used in comparison sections.

### Comparison section

Full-width grey-1 background section. 1/3 : 2/3 split. Left: label + large verdict statement. Right: analysis body + distinction grid.

## Components

### Nav bar

Fixed/sticky. White background. 1px grey-2 border-bottom. Height: 52–56px. Contents: logo/back-link left, links centre, CTA right. Nav links: caption1, grey-6 minimum, hover to black. Active state: accent underline or accent left border.

### Progress bar

2px. Accent. Position fixed top. `transform-origin: left`, `scaleX` driven by scroll position.

### Section rule

Full-width 1px grey-2 horizontal divider. Used between major sections. Never substitute a gap for a rule — both serve different structural purposes.

### Buttons

- **Primary:** black fill, white text, caption1, weight 500, 0.06em tracking, uppercase, 14px height padding. Hover: grey-8.
- **Ghost:** black text, accent bottom border 1px, no fill. Hover: colour holds, border darkens.

## Aesthetic directives

**Swiss International Style. Every element earns its position.** The grid is the argument, not decoration.

**White space is load-bearing.** Do not compress section padding to fit more content. If content doesn't fit, reduce content.

**No decorative borders, shadows, or radius.** Borders communicate structure. Shadows imply elevation that doesn't exist. Radius softens edges that should be resolved. Exception: SVG diagram internals may use `rx` for readability.

**The accent is a single moment per page.** Scan a layout — if you see the accent in more than 2–3 places, remove one. The label pattern, one structural rule (progress bar, active nav), and one content accent is the ceiling.

**Typography carries the layout.** Weight, scale, and tracking do the work that colour and decoration do in lesser systems. Trust the type.

**Left/right rhythm creates pace.** Alternate between full-width and split layouts to create a reading rhythm. Never use the same grid structure for three consecutive sections.

## WCAG compliance

Minimum contrast ratios (WCAG 2.1 AA):

- Normal text (<18px regular or <14px bold): 4.5:1
- Large text (≥18px regular or ≥14px bold): 3:1
- UI components / decorative: 3:1

Safe text colours on white: black (21:1), grey-8 (12.6:1), grey-7 (7.4:1), grey-6 (4.48:1 — minimum).

Unsafe for text on white: grey-5 (2.85:1), grey-4 (1.95:1), grey-3 and lighter.

Example accent on white: #DB0011 is 5.08:1 — passes AA for normal text, safe for labels. If you swap the accent, re-check this before using it for any text.

White on black: 21:1. White on grey-7: 4.48:1 minimum — check at use size.

When in doubt: use black. The rule is simple.

## Output types

### Brochure HTML page

Model on Archetype A. Include: sticky nav, hero section with label + heading + stats, proposition split, feature strip (grey-1), insight/quote section, footer. All sections separated by 1px grey-2 rules.

### Research document profile

Model on Archetype B. Include: sticky nav with back-link + category context, profile header (2-col: name/org left, tagline + meta right), diagram section (label aside + frame), dimension sections (1/3 : 2/3 with index numbers), comparison section (grey-1 background), footer nav (prev/next).
