# Accessibility & inclusive design

> Source: create.hsbc brandhub (authenticated) — `foundations-and-identity/accessibility.html` + `.../accessibility/Neurodiversity-Guidelines.html`. Captured 2026-06-18 for RAG. Summarised, not verbatim. The component metas cite the **"HSBC Accessibility Framework"** (dev standard) at `create.hsbc/Guidelines/Accessibility.html` — that's the WCAG-aligned engineering checklist; this page is the brand/inclusive-design layer.

## Ambition

HSBC's bold ambition: become the **most digitally accessible financial services provider in the world** — public websites, mobile apps and internal systems **accessible and usable by all** customers and staff. Delivering this consistently requires digital teams to have accessibility **knowledge, training, tools and motivation**.

> ~**1 billion people (15–20% of the world)** experience some form of disability.

## Two strands on the brandhub

1. **Neurodiversity guidelines** — how to design, code and create digital content for neurodiverse users (below).
2. **Communication guidance** — the **seven most common workplace scenarios** for accessible/inclusive comms (sub-page; pull on demand).

## Neurodiversity guidelines

**What:** support people whose neurocognitive abilities (learning, attention, sociability, mood) differ — treated as **natural variations**, not abnormalities. At least **1 in 10 working-age adults** is neurodivergent (many don't consider it a disability).

**Basis:** **40 distinct guidelines + success criteria across 14 sections**, grounded in **Hassell Inclusion research for the National Autistic Society (2019)** — the first neurodiversity guidelines built on solid empirical evidence. They **complement** existing accessibility standards. Designed to aid **autism, dyslexia, ADHD, and learning difficulties**.

**Guiding beliefs:** neurodiverse conditions can benefit an organisation; supporting all users is the right thing to do; **inclusive design benefits all users**.

### The 14 guideline areas (apply to digital design/build)
Communication styles · Page layout (clear, clutter-free) · Navigation (consistent, simple) · Colours (low-contrast schemes; let users customise) · Fonts (readable on screen) · Text (formatting for easier reading) · Use of language (clear, concise, audience reading age) · Non-textual information (visuals alongside text) · Images (easy to understand, add clarity) · Video content · Movement (moving/animated elements) · Help pages (digital + non-digital access) · Customisation (let users tailor the experience) · Re-learnability (communicate changes in advance) · User research.

> Design implications worth flagging: **let users customise colour** and **avoid forcing high contrast everywhere** (low-contrast option), **keep layouts clutter-free with simple consistent nav**, **be cautious with movement/animation** (cf. the time-based-indicator rule "not essential → don't animate" and `prefers-reduced-motion`), and **announce UI changes in advance** (re-learnability).

### Common neurodivergent conditions (designing for)
- **ADD / ADHD** — focus/distraction variability (sometimes hyper-focus); different stimulation needs.
- **Autism (ASC)** — incl. Asperger's, PDD-NOS; sensory inputs (noise, heat, light, touch) can be an issue.
- **Dyslexia** — reading/writing; also sequencing, info processing, working memory, phonological processing.
- **Dyspraxia (DCD)** — fine/gross motor (handwriting, manual tasks); sensory responses; organisation/working memory.
- **Dyscalculia** — affects mathematical functions.
- **Dysgraphia** — handwriting and fine-motor (spelling, finger sequencing; may affect typing).

## How this maps to the system

- This is the **why/inclusive-design layer**; the per-component `accessibility` blocks + `relatedSC` (WCAG SCs) are the **how**, and the **HSBC Accessibility Framework** (`Guidelines/Accessibility.html`) is the engineering checklist all new dev must pass (Brand Design Team review before release — per the Search field guide).
- Reinforces recurring component rules: visible focus, 44px targets, not colour-alone, captions/transcripts for video, pausable motion, 400% text + pinch-zoom (Search field), status announcements (aria-live).

## Sub-pages (create.hsbc, deeper — pull on demand)
- Communication guidance (7 scenarios) — under `foundations-and-identity/accessibility/`
- HSBC Accessibility Framework (dev/WCAG checklist) — `Guidelines/Accessibility.html`
- About-us Accessibility — `about-us/Accessibility.html`
