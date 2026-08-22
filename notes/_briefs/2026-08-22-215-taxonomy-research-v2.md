# Component-library taxonomy + finding mechanisms — web research

**Session:** #214 · **Date:** 2026-08-21 · **Author:** Opus research sub
**Question (Dave's, verbatim):** *"Type filters, atom, molecule, organism, lock-up, shell, template etc. or primitive, base, pattern, lock-up, shell, template. actually where is the consensus on this type of naming. And any other finding mechanism that might be appropriate."*
**Status:** research only. No ruling. Candidates below are presented evenly — the call is Dave's with the conductor.

---

## (a) The consensus picture, in plain prose

There is a consensus, and it is **not** Atomic Design.

Every major production system in 2026 has converged on roughly the same four-word spine: **Foundations → Tokens → Components → Patterns**, with **Templates / Blocks / Layouts** as an optional fifth tier when the system ships whole page starts. Atlassian's own nav is literally Foundations · Components · Patterns · Tools ([atlassian.design/design-system](https://atlassian.design/design-system)). GOV.UK is Styles · Components · Patterns ([design-system.service.gov.uk](https://design-system.service.gov.uk/)). Material 3 is Foundations · Styles · Components ([m3.material.io/foundations](https://m3.material.io/foundations), [/components](https://m3.material.io/components)). Carbon describes itself as "components, patterns, guidance, and code" ([carbondesignsystem.com](https://carbondesignsystem.com/all-about-carbon/what-is-carbon/)). Nobody argues about these words any more; they are boring, and that is the point.

**Where Atomic Design survives:** as a *mental model* for composition depth, and inside Figma file structures where designers still name pages "Atoms / Molecules / Organisms". Brad Frost himself has said the labels "have never been the point, and we don't really use them in our work. But they're still useful as a mental model" ([atomicdesign.bradfrost.com ch.2](https://atomicdesign.bradfrost.com/chapter-2/); quote circulated via [qt.io](https://www.qt.io/software-insights/atomic-design-systems-why-the-labels-dont-matter)). **Where it has been dropped:** as *public navigation*. Not one of the eight systems surveyed below uses atoms/molecules/organisms as a top-level menu. The standing criticisms are consistent — the atom/molecule boundary is unarguable in principle and unresolvable in practice; "organism" and "template" are where teams stall; and the vocabulary is chemistry-teacher jargon that a consumer of the library has to *learn* before they can find a button ([DEV, 2025 relevance review](https://dev.to/m_midas/atomic-design-and-its-relevance-in-frontend-in-2025-32e9); [Webstacks, misconceptions](https://www.webstacks.com/blog/4-misconceptions-of-atomic-design-and-how-to-get-around-them)).

**The headless/unstyled camp went a different way:** "primitives" is now a firm, widely-understood industry word meaning *behaviour + accessibility, no styling* — Radix Primitives is the canonical use ([Vercel comparison](https://vercel.com/i/shadcn-vs-radix); [WorkOS](https://workos.com/blog/what-is-the-difference-between-radix-and-shadcn-ui)). Note this is a **different sense** from "primitive = smallest visual atom". If the library uses "primitive" for Button and Badge, some engineers will read it as "unstyled behaviour layer". Worth knowing before choosing. Separately, shadcn/ui now routes every component under a **`base/`** namespace (`/docs/components/base/button`) ([ui.shadcn.com/docs](https://ui.shadcn.com/docs)) — so Dave's "base" has a live precedent too.

**On Dave's two odd words.** **"Lock-up"** is a real, precise, *brand/graphic-design* term — the fixed arrangement of two or more elements (logomark + logotype) treated as one unit ([Google Fonts glossary](https://fonts.google.com/knowledge/glossary/lockup); [Tufts brand](https://brand.tufts.edu/guidelines/lockups)). It has **no** established meaning as a UI-composition tier. The industry word for "several components fixed into a reusable arrangement" is **block** — shadcn ships Blocks (login, sidebar, dashboard) as a first-class category alongside Components ([ui.shadcn.com/blocks](https://ui.shadcn.com/blocks), [Feb 2026 changelog](https://ui.shadcn.com/docs/changelog/2026-02-blocks)) — or **pattern**, or **composition**. **"Shell"** is on much firmer ground: Carbon ships a component literally called **UI Shell** ([carbondesignsystem.com/components/UI-shell-header](https://carbondesignsystem.com/components/UI-shell-header/usage/)), "app shell" is standard PWA/layout architecture vocabulary, and other systems ship App Shell as a layout component. Shell is safe. Lock-up is a coinage — defensible and evocative for a *brand-adjacent* system, but it will need a one-line definition on the page.

**What nobody says:** nobody publishes "molecule" or "organism" as a filter. Nobody has a consensus word for the level *between* a single component and a page — that gap is exactly where "lock-up", "block", "pattern", "composition" and "recipe" all compete, and it is genuinely unsettled industry-wide. And critically: **no system relies on the taxonomy alone for findability.** Every one of them ships search first (see (c)) — the taxonomy is a *browsing aid*, not the retrieval mechanism.

---

## (b) What the major systems actually call their levels

| System | Top-level nav words | Smallest tier | Composed tier | Page/layout tier | Source |
|---|---|---|---|---|---|
| **Atomic Design** (Frost) | Atoms · Molecules · Organisms · Templates · Pages | Atom | Molecule / Organism | Template, Page | [atomicdesign.bradfrost.com](https://atomicdesign.bradfrost.com/chapter-2/) |
| **Material 3** (Google) | Foundations · Styles · Components | Styles (colour, type, shape) | Components | "Canonical layouts" under Foundations → Adaptive design | [m3.material.io](https://m3.material.io/), [/foundations](https://m3.material.io/foundations), [canonical layouts](https://m3.material.io/foundations/adaptive-design/canonical-layouts) |
| **IBM Carbon** | Elements · Components · Patterns · Guidelines | Elements (+ design tokens) | Components | **UI Shell**; Patterns | [what-is-carbon](https://carbondesignsystem.com/all-about-carbon/what-is-carbon/), [patterns overview](https://carbondesignsystem.com/patterns/overview/), [UI Shell](https://carbondesignsystem.com/components/UI-shell-header/usage/) |
| **Shopify Polaris** | (now a web-components framework, docs by *surface*: App Home, Admin, Checkout, Customer accounts, POS) | Tokens | Components | App surfaces | [shopify.dev/docs/api/polaris](https://shopify.dev/docs/api/polaris) — note polaris.shopify.com now redirects here |
| **Salesforce SLDS 2** | Components · Styling hooks · Design tokens (Blueprints legacy) | Design tokens / styling hooks | Base Lightning Components | Blueprints (legacy), page layouts | [lightningdesignsystem.com](https://www.lightningdesignsystem.com/), [SLDS1 vs SLDS2](https://developer.salesforce.com/docs/platform/lwc/guide/create-components-css-slds1-slds2.html) |
| **Atlassian** | Foundations · Components · Patterns · Tools · Rovo UI | Tokens (under Foundations) | Components | Patterns | [atlassian.design/design-system](https://atlassian.design/design-system), [/foundations](https://atlassian.design/foundations), [/patterns](https://atlassian.design/patterns) |
| **GOV.UK** | Styles · Components · Patterns | Styles | Components | Patterns → **Pages** sub-group (confirmation, question, interruption pages) | [design-system.service.gov.uk](https://design-system.service.gov.uk/), [/patterns](https://design-system.service.gov.uk/patterns/) |
| **Radix Primitives** | Primitives (Components · Utilities) | **Primitives** | — | — | [Vercel: shadcn vs Radix](https://vercel.com/i/shadcn-vs-radix) |
| **shadcn/ui** | Components (`base/`) · **Blocks** · Charts · Themes · Registry | Components under `base/` namespace | Components | **Blocks** (login, sidebar, dashboard) | [ui.shadcn.com/docs](https://ui.shadcn.com/docs), [/blocks](https://ui.shadcn.com/blocks) |

**Read-across:** *Components* appears in 9/9. *Patterns* in 5/9. *Foundations* or *Styles* in 5/9. *Tokens* in 6/9. *Atoms/molecules/organisms* in 1/9 — the originating methodology, and its author says he doesn't use the labels. *Shell* appears as a named artefact in Carbon. *Lock-up* appears in **zero** UI taxonomies; it appears in essentially every **brand** guideline.

---

## (c) Finding mechanisms — what real browsers actually ship

Ranked roughly by how universal they are.

1. **⌘K / fuzzy search, first-class and always-on.** The primary retrieval path in every modern library. Storybook's sidebar search is explicitly fuzzy — typos still resolve ([Storybook docs: browse stories](https://storybook.js.org/docs/get-started/browse-stories), [sidebar & URLs](https://storybook.js.org/docs/configure/user-interface/sidebar-and-urls)). The Component Gallery puts ⌘K in the header ([component.gallery](https://component.gallery/)). SLDS ships a documented Global Search pattern ([SLDS Global Search](https://www.lightningdesignsystem.com/2e1ef8501/p/727af5)). **Implication: taxonomy is browse, search is find.**
2. **Aliases / "also known as" synonyms.** The strongest single fix for the dropdown-vs-select problem. The Component Gallery's Select page literally reads *"Also known as: Dropdown, Select input"* and indexes 82 real-world examples under it, including entries actually named "Dropdown" in Carbon, eBay, SEB, Wise, USWDS ([component.gallery/components/select](https://component.gallery/components/select/)). Figma achieves the same by **keyword-stuffing component descriptions** — Figma's asset search reads the description field, so teams add a `keywords:` line ([Figma: add descriptions](https://help.figma.com/hc/en-us/articles/7938814091287-Add-descriptions-to-styles-components-and-variables); [Designary tip](https://blog.designary.com/p/make-design-system-components-in-figma-more-searchable)). Doc-search engines call this a synonym set ([Typesense synonyms](https://typesense.org/docs/30.2/api/synonyms.html), [Azure AI Search synonym maps](https://learn.microsoft.com/en-us/azure/search/search-synonyms)).
3. **Tag / facet filters layered over the tree.** Storybook Tags are exactly this: a flexible categorisation layer *on top of* the sidebar hierarchy, multi-select, filtering the sidebar to matching stories ([Storybook tags blog](https://storybook.js.org/blog/storybook-tags/), [tags docs](https://storybook.js.org/docs/writing-stories/tags)). The Component Gallery runs two independent facet groups — **Tech** (React, Web Components, Sass…) and **Features** (Code examples, Usage guidelines, Accessibility, Tone of voice, **Unmaintained**, **Accessibility issues**, Research) ([component.gallery/components/select](https://component.gallery/components/select/)). Note that *status* facets (unmaintained / has-a11y-issues) are doing real work there.
4. **Category tree / sidebar hierarchy.** Universal, but everywhere it is now a *secondary* affordance next to search. Storybook supports implicit (file-location) or explicit (`title` param) placement ([naming & hierarchy](https://storybook.js.org/docs/writing-stories/naming-components-and-hierarchy)).
5. **Status / release-phase filters.** Atlassian publishes formal **Release phases** as a nav item ([atlassian.design/release-phases](https://atlassian.design/release-phases)). GOV.UK publishes "upcoming components and patterns" and an explicit contribution/proposal state ([GOV.UK community](https://design-system.service.gov.uk/community/)). This is a *type filter that isn't a taxonomy level* — worth separating in the UI.
6. **Visual index / thumbnail grid.** The Component Gallery renders a screenshot for every single example, auto-generated by a Puppeteer script ([component.gallery/about](https://component.gallery/about)). For a library where Dave's eye is the instrument, this is the highest-value non-search mechanism on this list.
7. **"Related components" cross-links.** Component Gallery's Select page ends with *Related components → Dropdown menu, Combobox*, each with a one-line **disambiguation** ("it differs from a select in that it shows actions or navigation options and is not a form input") ([component.gallery/components/select](https://component.gallery/components/select/)). This is the "for this pattern use X" mechanism, and the disambiguation sentence is the part that earns its keep.
8. **Recency / usage-frequency ordering.** Storybook's component finder keeps a **"recently opened"** history for quick access ([Storybook component finder](https://medium.com/storybookjs/new-component-finder-and-sidebar-3f47bd915cc8)). Figma's asset panel surfaces recently-used. Nobody surveyed ships true *usage-frequency-across-the-org* ordering in public docs — that's an available differentiator.
9. **Sort controls.** Component Gallery offers sort-by design-system vs sort-by component-name — cheap, and useful when the same concept is named differently in different places.
10. **Name-distribution / disagreement view.** Component Gallery has a "Name distribution" chart showing how many systems call the thing Select vs Dropdown vs Picker. Niche, but it is the honest answer to "what is this called".
11. **Machine-readable index for agents.** shadcn ships `llms.txt`, a Registry with **Dynamic Search** and an **MCP server** ([ui.shadcn.com/docs](https://ui.shadcn.com/docs), [registry MCP](https://ui.shadcn.com/docs/registry/mcp)); Atlassian shipped a portable `DESIGN.md`; Supernova markets an AI-agent surface ([supernova.io/for-ai](https://www.supernova.io/for-ai)). In 2026 "who is finding the component" now includes an agent — a flat JSON index is a finding mechanism.

---

## (d) Candidate taxonomies for this library (~124 components)

Existing levels as given: tokens/primitives → controls → composed components → lock-ups → app-shells → templates.

### Candidate 1 — Atomic-flavoured (Dave's first list)
`Atom · Molecule · Organism · Lock-up · Shell · Template`

- **For:** matches the composition depth already in the library one-for-one; instantly legible to any designer who has used Figma libraries; the size gradient is self-explaining without reading definitions; "lock-up" and "shell" sit comfortably as the two brand/app-specific extensions on a familiar spine.
- **Against:** the atom/molecule boundary generates unresolvable arguments at scale (does a Field = label+input+hint count as molecule or organism?); no surveyed production system navigates this way; the author of the methodology says he doesn't use the labels; engineers consuming the library have to learn chemistry before they can find a button; mixing chemistry (atom/molecule/organism) with print (lock-up) with architecture (shell) is three metaphors in one row.

### Candidate 2 — Industry-plain (the actual consensus words)
`Foundations · Components · Patterns · Blocks · Shells · Templates`
*(or with tokens split out: `Tokens · Components · Patterns · Blocks · Shells · Templates`)*

- **For:** every word is one that Material, Carbon, Atlassian, GOV.UK or shadcn already publishes, so nothing needs teaching; "Blocks" is the live industry word for the lock-up tier ([shadcn Blocks](https://ui.shadcn.com/blocks)); "Shell" has a named precedent in Carbon UI Shell; portable — a new hire or an LLM guesses right first time.
- **Against:** it **collapses** the library's real internal distinction between a control (Button) and a composed component (DataTable) into one bucket of ~100 items, which is the exact thing that made a taxonomy necessary; "Patterns" in the consensus sense means *task solutions* (GOV.UK: "check answers", "confirm an email") not *mid-size assemblies*, so borrowing it for assemblies imports a false friend; loses "lock-up", which is a genuinely accurate word for what those artefacts are.

### Candidate 3 — Dave's second list, hybrid (plain-language, keeps the depth)
`Primitive · Base · Pattern · Lock-up · Shell · Template`

- **For:** preserves all six real levels without chemistry; "primitive" and "base" both have live 2026 precedent (Radix Primitives; shadcn's `base/` namespace); reads as engineering vocabulary rather than teaching-metaphor; "lock-up" keeps the brand precision that a brand-adjacent system arguably wants.
- **Against:** **"primitive" is a loaded word** — in the Radix/Base UI sense it means *unstyled behaviour layer*, not *smallest visual element*, so engineers may read the tier backwards; "base" and "primitive" adjacent to each other are near-synonyms in plain English and the boundary won't be self-evident; "pattern" here means assembly, colliding with GOV.UK/Atlassian's task-solution sense; "lock-up" still needs a definition line because zero UI systems use it that way.

### Cross-cutting note applying to all three
Whichever spine wins, the surveyed evidence says the *level* should be **one facet among several**, not the whole IA. The facets that earn their place independently of taxonomy: **status** (stable / beta / deprecated — cf. Atlassian Release phases), **theme coverage** (mono / legacy / console / supercharge), **aliases**, and **thumbnail-first browsing**. And search with a synonym table will resolve more lookups than any of the three word-sets above.

---

## Sources

[Atomic Design ch.2](https://atomicdesign.bradfrost.com/chapter-2/) · [Atomic design in 2025 (DEV)](https://dev.to/m_midas/atomic-design-and-its-relevance-in-frontend-in-2025-32e9) · [Why the labels don't matter (Qt)](https://www.qt.io/software-insights/atomic-design-systems-why-the-labels-dont-matter) · [4 misconceptions (Webstacks)](https://www.webstacks.com/blog/4-misconceptions-of-atomic-design-and-how-to-get-around-them) · [Material 3](https://m3.material.io/) · [M3 Foundations](https://m3.material.io/foundations) · [M3 canonical layouts](https://m3.material.io/foundations/adaptive-design/canonical-layouts) · [Carbon: what is Carbon](https://carbondesignsystem.com/all-about-carbon/what-is-carbon/) · [Carbon patterns](https://carbondesignsystem.com/patterns/overview/) · [Carbon UI Shell](https://carbondesignsystem.com/components/UI-shell-header/usage/) · [Polaris references](https://shopify.dev/docs/api/polaris) · [SLDS 2](https://www.lightningdesignsystem.com/) · [SLDS1 vs SLDS2](https://developer.salesforce.com/docs/platform/lwc/guide/create-components-css-slds1-slds2.html) · [SLDS Global Search](https://www.lightningdesignsystem.com/2e1ef8501/p/727af5) · [Atlassian design system](https://atlassian.design/design-system) · [Atlassian foundations](https://atlassian.design/foundations) · [Atlassian patterns](https://atlassian.design/patterns) · [Atlassian release phases](https://atlassian.design/release-phases) · [GOV.UK Design System](https://design-system.service.gov.uk/) · [GOV.UK patterns](https://design-system.service.gov.uk/patterns/) · [shadcn/ui docs](https://ui.shadcn.com/docs) · [shadcn Blocks](https://ui.shadcn.com/blocks) · [shadcn Blocks changelog Feb 2026](https://ui.shadcn.com/docs/changelog/2026-02-blocks) · [shadcn registry MCP](https://ui.shadcn.com/docs/registry/mcp) · [Radix vs shadcn (Vercel)](https://vercel.com/i/shadcn-vs-radix) · [Radix vs shadcn (WorkOS)](https://workos.com/blog/what-is-the-difference-between-radix-and-shadcn-ui) · [Component Gallery: Select](https://component.gallery/components/select/) · [Component Gallery: about](https://component.gallery/about) · [Storybook tags](https://storybook.js.org/blog/storybook-tags/) · [Storybook tags docs](https://storybook.js.org/docs/writing-stories/tags) · [Storybook browse stories](https://storybook.js.org/docs/get-started/browse-stories) · [Storybook sidebar & URLs](https://storybook.js.org/docs/configure/user-interface/sidebar-and-urls) · [Storybook naming & hierarchy](https://storybook.js.org/docs/writing-stories/naming-components-and-hierarchy) · [Storybook component finder](https://medium.com/storybookjs/new-component-finder-and-sidebar-3f47bd915cc8) · [Figma component descriptions](https://help.figma.com/hc/en-us/articles/7938814091287-Add-descriptions-to-styles-components-and-variables) · [Designary: searchable components](https://blog.designary.com/p/make-design-system-components-in-figma-more-searchable) · [Supernova for AI](https://www.supernova.io/for-ai) · [Typesense synonyms](https://typesense.org/docs/30.2/api/synonyms.html) · [Azure AI Search synonyms](https://learn.microsoft.com/en-us/azure/search/search-synonyms) · [Google Fonts: lockup](https://fonts.google.com/knowledge/glossary/lockup) · [Tufts brand: lockups](https://brand.tufts.edu/guidelines/lockups)

---
---

# ADDED #215 — five additions, ordered by Dave

**Session:** #215 · **Date:** 2026-08-22 · **Author:** Opus research sub
**Why:** Dave read v1, liked the Carbon material most, and ordered five additions. This file is **v1 copied forward, untouched, plus everything below**. Nothing above this line has been trimmed or edited — v1 remains at `notes/_briefs/2026-08-21-214-taxonomy-research-v1.md` if you want the original bytes.

**Framing note — Dave's taxonomy is now RULED (`s215-D4`), so §d above is HISTORY.** The ladder is:

> **Foundations · Tokens**, then **Primitives** *(if needed)* / **Element** / **Pattern** / **Block** / **Shell** / **Template**

and the library gets **two tabs: Usage and Type**. Everything below is written against that ruling, not against the three open candidates in §d.

---

## §1 · ADDED #215 — CARBON DEEP-DIVE

Dave asked for this one to be the richest, so it is. Everything here was fetched live on 2026-08-22 from `carbondesignsystem.com`; the site footer on every page read *"React Components version ^1.114.0 · Last updated 21 August 2026"*, so this is current, not archived.

### 1.1 The four-tab component page — and the fact that it is a *requirement*, not a layout

Every Carbon component page carries exactly four tabs, in this order:

> **Usage · Style · Code · Accessibility**

Observed first-hand on `/components/button/usage/` and `/components/UI-shell-header/usage/`, and visible in the screenshot at `assets-215-nav/nav-carbon.png` ([Carbon Button, Usage](https://carbondesignsystem.com/components/button/usage/); [Carbon UI shell header, Usage](https://carbondesignsystem.com/components/UI-shell-header/usage/)).

The load-bearing find is that this tab set is **written into Carbon's definition of done**, not merely into its page template. Carbon's Component checklist says, verbatim:

> *"All components and patterns require **usage, style, code, and accessibility** guidance published on a Carbon ecosystem website."*
> — [Carbon: Component checklist § Documentation](https://carbondesignsystem.com/contributing/component-checklist/)

The same page lists a **documentation template per tab**, each independently versioned:

| Tab | Template | Last updated (per Carbon) | What the tab answers |
|---|---|---|---|
| **Usage** | Single-variant template / multiple-variant template | Q1 2024 / 2021 | *when* to use it and *how it works* |
| **Style** | Single-variant / multiple-variant | Q3 2024 / Q3 2024 | *how it looks* — colour, typography, structure, size |
| **Code** | Code template | 2022 | how a developer implements it — snippets, dependencies, version changes |
| **Accessibility** | Accessibility template | 2023 | written by Carbon's a11y SMEs; the considerations baked in |

*Source for the whole table: [Carbon: Component checklist](https://carbondesignsystem.com/contributing/component-checklist/).*

**Why this matters to Apollo.** Dave's ruled library has *two* tabs (Usage, Type) and those are **navigation** tabs — they slice the 135-item list. Carbon's four are **page** tabs — they slice one component's documentation. These are different instruments and they compose rather than compete: Apollo could ship *Usage | Type* on the browser and *Usage | Style | Code | Accessibility* on each component page, and neither would collide with the other. Carbon is the proof that the second set is worth four tabs rather than one long scroll.

### 1.2 What sits *above* the tabs on a Carbon component page

Read in order down `/components/button/usage/`, the page furniture is:

1. **A one-sentence definition.** *"Buttons are used to initialize an action. Button labels express what action will occur when the user interacts with it."* One sentence, no preamble.
2. **A live demo** with its own **Theme selector** (White / Gray 10 / Gray 90 / Gray 100) and **Variant selector** — the demo is themed *in place*, exactly the mechanism `gen_library_214.py` already uses via fragment broadcast. Carbon then hands off: *"View the full demo on Storybook for additional information such as its version, controls, and API documentation."*
3. **An accessibility testing status block** — four named rows, each with a state:

   | Row | State shown on Button |
   |---|---|
   | Default state | Tested |
   | Advanced states | Tested |
   | Screen reader | Manually tested |
   | Keyboard navigation | Tested |

   with the caveat printed on the page: *"These tests appear only when the components are stable."* ([Carbon Button](https://carbondesignsystem.com/components/button/usage/)) — i.e. **the a11y block doubles as a maturity signal**. That is a status facet hiding inside a content block; see §3.
4. **A jump-list of the page's own sections** (Overview · Formatting · Content · Universal behaviors · …variants… · Modifiers · **Related** · **References** · Feedback).
5. **Related** — a plain list of cross-links (for Button: Button labels, Fixed button bars, Form pattern, Icons, Link component, Menu buttons, Modal component). Note it mixes *components*, *patterns* and *content guidance* in one list — Carbon does **not** partition "related" by tier.
6. **References** — external, academic, cited properly (Nielsen Norman, Interaction Design Foundation, and Wiedenbeck 1999 on icon learnability). Carbon cites literature on component pages. Nobody else surveyed does.

### 1.3 UI Shell — documented as ZONES, not as one component

This is the single most transferable thing Carbon does for Dave's **Shell** tier.

Carbon does not ship a component called "UI Shell". It ships **three** components that are documented as **zones of one shell**, and says so on the page:

> *"The UI shell is made up of three components — the header, the left panel, and the right panel. All three can be used independently, but the components were designed to work together."*
> — [Carbon: UI shell header, Usage](https://carbondesignsystem.com/components/UI-shell-header/usage/)

| Zone | Carbon's own definition |
|---|---|
| **Header** | *"The highest level of navigation. The header can be used on its own for simple products or be used to trigger the left and right panels."* |
| **Left panel** | *"An optional panel that is used for a product's navigation."* |
| **Right panel** | *"An optional panel that shows additional system-level actions or content associated with a system icon in the header."* |

Four further things are worth lifting whole:

- **The shell is defined by SCOPE, not by shape.** *"A shell is a collection of components shared by all products within a platform. It provides a common set of interaction patterns that persist between and across products."* That is a definition Apollo can borrow verbatim for its Shell tier, and it is the reason Shell is a *tier* and not just a big component: a shell is the thing that outlives the page.
- **There is a spatial grammar inside the header.** *"For each UI shell component, left-to-right translates to product-to-global."* Left edge = product-level; middle = system-level controls; right edge = most global (the switcher, spanning multiple products). Carbon then fixes an **exact icon order** — 1 Search (furthest left, so an expanding search field does not shove the others), 2 Other, 3 Help (4th from right), 4 Notifications (3rd from right), 5 Account (2nd from right), 6 Switcher (furthest right). This is a *lock-up rule in Dave's sense* published as component guidance.
- **The shell has TYPES, and they are compositional.** Carbon lists four: *Header base* (persistent site title, single-page UI), *Header with navigation*, *Header with actions*, *Header with sidenav*. Apollo's seven `app-shell-*` pages are the same idea already — see §2.
- **Responsive behaviour is a shell-level rule, not a component rule.** *"As a header scales down… header links and menus should collapse into a left-panel hamburger menu… If your UI includes a left panel, the header links should be added above the left panel items, pushing them down accordingly."* The rule spans two zones; it could not live on either component alone. That is the argument for a Shell tier having its own guidance surface.

**Read-across for Apollo.** Apollo files seven `app-shell-*` slugs at Shell, and separately files `sidebar-nav`, `navigations`, `footer` and `headers` elsewhere (see §2). Carbon's model says those four are **zones of the shell**, and it documents each as its own page while asserting the set. That is a live precedent for either answer — Dave can keep the zones as separate pages and still call them Shell, which is exactly what Carbon does.

### 1.4 The Elements tier, and where tokens meet components

Carbon's left navigation puts **Elements** as a top-level group, *above* Guidelines, Components and Patterns. Observed first-hand and captured at `assets-215-nav/nav-carbon-elements.png`. The full expanded group, in Carbon's own order:

> **Elements** → 2x Grid · Color · Icons · Pictograms · Motion · Spacing · Themes · Typography

(Confirmed twice: by the screenshot, and by the Spacing page's own prev/next footer reading *"Previous: Elements: Motion — Next: Spacing: Code"*, [Carbon Spacing](https://carbondesignsystem.com/elements/spacing/overview/).)

**Elements pages have their own tab set, and it is NOT the component set.** Colour carries four:

> **Overview · Usage · Tokens · Code** — [Carbon Color: Usage](https://carbondesignsystem.com/elements/color/usage/)

Spacing carries two: **Overview · Code** ([Carbon Spacing: Overview](https://carbondesignsystem.com/elements/spacing/overview/)). So Carbon does **not** force a uniform tab set on the Elements tier — the tab set is per-element, and **Tokens is a tab only where there is a token table to show**. That is a directly usable pattern: Apollo's Foundations · Tokens tier does not need a fixed four tabs.

#### How tokens meet components at the Elements tier — Carbon's answer, in detail

This is the mechanism Dave will care about, because Apollo has four themes and the same problem.

Carbon's colour Elements page is, in substance, a document about **how a token knows which component it is inside**. Two named mechanisms, both quoted from [Carbon Color: Usage](https://carbondesignsystem.com/elements/color/usage/):

| Token type | Carbon's definition | Who uses it |
|---|---|---|
| **Layering tokens** | *"Explicit layering tokens used to manually map the layering model onto components. They come in sets that pair with individual UI layers."* | designers, and any component that lives on exactly one layer |
| **Contextual tokens** | *"Abstract code tokens used to automatically map the layering model onto components depending on where it is used on the page."* | code only — *"Contextual tokens are only available in code and are not a part of the design assets."* |

- There are **four layers** in a theme — base, `layer-01`, `layer-02`, `layer-03` — and the layer sets are named by numeric suffix (`-00`, `-01`, `-02`, `-03`). A component that must sit on three layers needs **three built variants** under layering tokens, or **one variant** under contextual tokens wrapped in a `<Layer>` component (nestable to three levels).
- Not every token is layered: *"Some tokens groups, like `text` and `icon`, work across layers"* — because they already carry enough contrast that they need not change per layer. **This is the single sharpest idea on the page**: the token taxonomy splits into *layer-bound* and *layer-free* families, and the split is derived from contrast, not from taste.
- Fields nest one level deeper than their ground: *"a field placed on a `$layer-02` background will use `$field-03`."* Borders pair with their own number: `$field-03` pairs with `$border-strong-03`.
- **Inline theming** is the escape hatch: wrap a region in `<Theme theme="g100">` so the shell or a side panel runs a different theme from the page. Carbon's stated rule — *"Only use inline theming for major shifts in color, like high contrast moments"* — is a governance rule, not a technical one, and it is published beside the mechanism.

Two more Elements facts worth having on the record:

- **Spacing.** One scale, thirteen steps, each with a token, all multiples of 2/4/8 — `$spacing-01` = 2px through `$spacing-13` = 160px ([Carbon Spacing](https://carbondesignsystem.com/elements/spacing/overview/)). Carbon's own FAQ answers the two questions every team asks: *are increments outside the scale allowed?* — *"There are always exceptions to the rule, but deviating from the spacing scales should be avoided whenever possible."*; *are spacing tokens responsive?* — **no**, *"the tokens themselves do not change values based on the screen size,"* but jumping a step at a breakpoint is sanctioned.
- **Spacing ships a component.** The `Stack` component applies the spacing scale between items *"to not use margin and instead delegate the responsibility of positioning and layout to parent components."* So an Element (spacing) reaches the component tier through a named component. That is the cleanest single example of "where tokens meet components" on the whole site.

### 1.5 Carbon's grouping and nav — and what it says about Usage vs Type

The complete Carbon left nav, read off the live site (`assets-215-nav/nav-carbon-elements.png`), top to bottom:

> All about Carbon · What's happening — *(rule)* — Designing · Developing · Contributing · Migrating — *(rule)* — **Elements · Guidelines · Components · Patterns** · Community assets · Data visualization · Help — *(rule)* — GitHub ↗

Four observations that bear directly on Dave's two-tab split:

1. **The nav is grouped by AUDIENCE first, TAXONOMY second.** The top block is about the system; the second block is *Designing / Developing / Contributing / Migrating* — four **jobs**; only the third block is the taxonomy (Elements / Guidelines / Components / Patterns). Carbon's primary cut is "who are you and what are you doing", and the tier ladder is subordinate to it. **This is the Usage tab, avant la lettre.**
2. **Guidelines sits *between* Elements and Components** — i.e. between the token tier and the component tier — which is where cross-cutting rules (accessibility, content, layout) belong and where they would otherwise be homeless.
3. **Data visualization is hoisted out of Components entirely** into its own top-level group. Apollo has **fourteen `chart-*` slugs** filed as `organism` (§2). Carbon's answer to that exact pressure was *not* to find them a tier — it was to give them a **sibling of the taxonomy**. That is a live, named precedent for a chart carve-out, and it is a Type-tab question, not a Usage-tab question.
4. **Carbon has no "type filter" anywhere.** Within Components, the sidebar is one flat alphabetical list (Overview, Accordion, AI label, Breadcrumb, Button, Checkbox, Code snippet, Contained list, Content switcher, Data table, Date picker, Dropdown, File uploader, Form, Inline loading, …). No chips, no facets, no atoms/molecules. **Carbon relies on alphabetical + search, and puts everything that resembles a facet into the URL path instead** (`/elements/…`, `/components/…`, `/patterns/…`). For a 135-item library this is the honest warning: a flat alphabetical list at Carbon's scale works because the *names* are conventional. Apollo's names are not all conventional (§4), which is precisely why Apollo needs the alias layer and the Type tab that Carbon can do without.

**Direct bearing on Usage-vs-Type.** Carbon splits the same way Dave ruled, but on different axes and at a different altitude: Carbon's **job/audience** grouping ≈ Dave's **Usage** tab, and Carbon's **URL-path tier** (`/elements/`, `/components/`, `/patterns/`) ≈ Dave's **Type** tab. The two systems land in the same place from opposite directions, which is about as strong a corroboration as a taxonomy decision gets. The one thing Carbon does that Dave's ruling does not yet cover: Carbon **hoists an entire domain (data-vis) out of the ladder** rather than forcing it down a tier.

---

## §2 · ADDED #215 — MAPPING TABLE: all 135 components on Dave's ruled ladder

### 2.1 Derivation — how these numbers were produced, mechanically

**Where levels live — probed, not assumed.** `knowledge/_state.json` carries **zero** occurrences of `"level"`. `reviews/ITINERARY-STATUS-2026-08-21-v3.json` carries zero occurrences of `"level"`, `atom`, `molecule` or `organism`; what it *does* carry is a `$layer2_rows` block and a `$layer2_note` reading *"Layer 2 (shells · templates · lock-ups · variant matrices), MEASURED 2026-08-21: 28 rows"* — i.e. the itinerary knows about the **top three tiers as one group**, but holds no per-component level. So neither store is the source. Levels are **derived at build time** by `level_of(slug, meta)` in `knowledge/_render/gen_library_214.py` (lines 192–209), from `knowledge/components/<slug>.meta.json`:

```
$layer "2 Shell"    -> shell        $layer "2 Template" -> template
$layer "2 Lock-up"  -> lockup       else meta category in {atom, molecule, organism} -> that
no meta at all      -> slug-shape fallback (app-shell-* / template-* / *-lockup), else "unfiled"
```

**What was run** (2026-08-22, this sandbox): `gen_library_214.collect()` was imported and executed against the live repo. It returned **135 rows** — one per existing `showroom/*.html` page excluding `index.html` — and **zero unfiled**, i.e. every one of the 135 carries a real derived level. No row below is hand-tagged.

**The count.** The derived levels are `atom 18 · molecule 57 · organism 33 · lockup 9 · shell 7 · template 11`, which sum to 135 exactly.

**The map onto Dave's ruled words.** The store's six derived levels map one-for-one onto the ruled ladder, in ordinal order. Two readings are legal and the difference is one boundary:

| Store level | n | **Map A — Primitives NOT used** | **Map B — Primitives used** |
|---|---:|---|---|
| `atom` | 18 | **Element** | **Primitive** |
| `molecule` | 57 | **Element** | **Element** |
| `organism` | 33 | **Pattern** | **Pattern** |
| `lockup` | 9 | **Block** | **Block** |
| `shell` | 7 | **Shell** | **Shell** |
| `template` | 11 | **Template** | **Template** |

Under **Map A**: Element 75 · Pattern 33 · Block 9 · Shell 7 · Template 11.
Under **Map B**: Primitive 18 · Element 57 · Pattern 33 · Block 9 · Shell 7 · Template 11.

**The evidence on "Primitives (if needed)".** Map B is the better-balanced tree (no bucket over 57), and the `atom` set does contain items that read as pre-component: `layout-utilities`, `divider`, `eyebrow`. But it also contains `textarea` (js=16), `segmented-control` (js=15), `reorder` (js=24) and `amount-input` (js=32) — four behaving controls that nobody would call a primitive in the Radix sense flagged in §a above. **So `atom` is not a clean Primitive tier as it stands**; Map B would need those four to move up. Recommendation: **take Map A now**, and only introduce Primitives if a later pass re-derives `atom` into "no behaviour, no state" (a mechanical test already available — `js == 0`) versus the rest.

### 2.2 The table — all 135, by tier

#### **ELEMENT** (Map A) — 75 = `atom` 18 + `molecule` 57

*`atom` (18):* Amount display · Amount input · Avatar · Back to top · Badge · Button · Divider · Eyebrow · Fab · Icon button · Layout utilities · Loading indicator · Qr code · Reorder · Segmented control · Status indicator · Tags · Textarea

*`molecule` (57):* Accordion · Account card · Account selector · Action bar · Alert · Anchor nav · Avatar group · Banner · Breadcrumbs · Cards · Carousel · Cascader · Chart sparkline · Combobox · Countdown timer · Date picker · Document row · Dropdown · Empty state · Headers · Image block · Input fields · Kpi tile · Limits meter · Links · List items · Meter · Multi select · Notifications · Pagination · Payment card visual · Popconfirm · Popover · Progress bar · Progress tracker · Quick actions · Range slider · Rating · Runway bar · Search field · Secure entry · Selection controls · Skeleton loader · Slider · Split button · Splitter · Standing order mandate row · Stat card · Summary · Tab bar · Tabs · Tags input · Time picker · Toast · Tooltip · Transaction row · View options

#### **PATTERN** — 33 (`organism`)

Calendar · **Chart bar · Chart boxplot · Chart bullet · Chart butterfly h · Chart butterfly v · Chart candlestick · Chart combo · Chart donut · Chart histogram · Chart line · Chart pie · Chart scatter · Chart stacked area** *(14 charts, bolded — see PFD-3)* · Command palette · Confirmation · Data grid · Date range picker · Drawer · File upload · Footer · Form layout · Hero · Modal lightbox · Modals · Navigations · Sidebar nav · Stepper · Table · Timeline · Transfer list · Tree · Video player

#### **BLOCK** — 9 (`lockup`)

Card header lockup · Cta lockup · Feature grid lockup · **Filter toolbar bar** *(see PFD-5)* · Footer doormat lockup · Hero variants · Page header lockup · Section heading lockup · Stats band lockup

#### **SHELL** — 7 (`shell`)

App shell doormat · App shell focused · App shell multi column · App shell nav rail · App shell side nav · App shell split · App shell top nav

#### **TEMPLATE** — 11 (`template`)

Template auth · Template confirmation · Template create edit · Template dashboard · Template detail · Template empty · Template error · Template list index · Template report · Template settings · Template wizard

### 2.3 PROPOSED-FOR-DAVE — placements that are genuinely ambiguous

These are **not** forced into the table above; they sit where the mechanical derivation puts them, and each is flagged here so Dave can rule. Nothing below has been moved.

| # | Component(s) | Derived tier | The tension | Proposed |
|---|---|---|---|---|
| **PFD-1** | `layout-utilities` | Element (`atom`) | It is not a component; it is spacing/grid machinery. Carbon files exactly this under **Elements → 2x Grid / Spacing** ([Carbon nav](https://carbondesignsystem.com/elements/spacing/overview/)), i.e. one tier *below* the ladder. | Move to **Foundations · Tokens** |
| **PFD-2** | `navigations`, `sidebar-nav`, `headers`, `footer` | Pattern ×3 + Element ×1 | Carbon documents header / left panel / right panel as **zones of the UI Shell** (§1.3). These four are Apollo's zones, filed across two different tiers. | Either **Shell** (as zones) or a declared "Shell zones live at Pattern" rule. Dave's call — but they should not be split across tiers |
| **PFD-3** | the 14 `chart-*` slugs | Pattern | A bar chart is not a "task solution" in the GOV.UK/Atlassian sense of Pattern, and 14 of 33 Patterns being charts drowns the tier. Carbon hoisted **Data visualization** to a top-level sibling of the whole taxonomy (§1.5). | **Carve out** — a Data-vis group beside the ladder, not a rung inside it |
| **PFD-4** | `chart-sparkline` | Element (`molecule`) | The other 14 charts are Pattern; sparkline alone is Element. Whichever way PFD-3 goes, this one is inconsistent with its siblings. | Follow PFD-3 with the rest |
| **PFD-5** | `filter-toolbar-bar` | Block (`lockup`) | The other eight Blocks are brand/marketing lock-ups (hero, CTA, doormat, stats band). This one is a functional toolbar with 41 lines of JS. It is a lock-up by shape but a Pattern by job. | **Pattern**, or accept that Block is shape-defined not job-defined |
| **PFD-6** | `hero` vs `hero-variants` | Pattern vs Block | One concept, two pages, two tiers. | Merge, or name the distinction on both pages |
| **PFD-7** | `confirmation` vs `template-confirmation` | Pattern vs Template | Same word at two rungs — the exact collision v1 §a warned about between "assembly" and "task solution". | Rename one |
| **PFD-8** | `form-layout` | Pattern (`organism`) | It is a *layout*, not a component. Sits between Pattern and Template. | **Template**, or declare Pattern covers layouts |
| **PFD-9** | the domain rows — `transaction-row`, `standing-order-mandate-row`, `document-row`, `account-card`, `payment-card-visual`, `runway-bar`, `limits-meter` | Element (`molecule`) | These are **fixed arrangements of elements representing one domain entity** — which is Dave's own definition of a lock-up, and the brand-design sense v1 §a documented. All seven ship `js=0`: pure arrangement, no behaviour. | **Block** |
| **PFD-10** | the plural slugs — `cards`, `headers`, `links`, `list-items`, `modals`, `notifications`, `input-fields`, `selection-controls`, `navigations`, `tags` | Element ×8, Pattern ×2 | These ten are **collection pages** (many variants on one page), not single components. A tier is a property of a component; these are properties of a page. | Flag with a `variants` marker rather than re-tier — it is a Type-tab question |
| **PFD-11** | `command-palette` | Pattern (`organism`) | `js=0` — an organism that ships no behaviour. Also absent from the Component Gallery entirely (§4). | Keep at Pattern; flag the missing behaviour as a build residual |
| **PFD-12** | `qr-code`, `video-player`, `payment-card-visual` | Element / Pattern / Element | Display artefacts, not controls. No tier on the ladder is about "media". | No move proposed — recorded so the gap is visible |

**Count: 12 PROPOSED-FOR-DAVE rows covering 41 of the 135 components.** The remaining 94 place unambiguously.

---

## §3 · ADDED #215 — LIFECYCLE VOCABULARY: what the majors call maturity

### 3.1 The comparison table

| System | The stages it publishes, verbatim | Shape | Source |
|---|---|---|---|
| **IBM Carbon** | **Draft** *(Discovery — "partially complete, ready for validation")* · **Preview candidate** *(Discovery — "partially complete, with measurable results, stakeholders, and clear business value")* · **Preview** *(Delivery — "mostly complete, changes possible based on feedback, **available to use in production**")* · **Stable** *(Launch and scale — "complete across code, kit, docs, design, and ready for production use")* | 4 forward stages, **no deprecation stage published on this page**; stages are pinned to a named Product Development Lifecycle | [Component checklist](https://carbondesignsystem.com/contributing/component-checklist/) |
| **Atlassian** | **Early Access** *("new experimental feature… breaking changes in minor releases at `0.x`… we don't recommend using this unless you are part of an early access pilot group")* · **Beta** *("new and ready to use… supported and stable at versions `1.0`+")* · **General Availability** *("fully stable and ready to use")* — then **Intent to Deprecate (Caution)** · **Deprecated** | **3 release phases + 2 deprecation phases**, explicitly separated into two tables; each stage is tied to a **semver range** | [Release phases](https://atlassian.design/release-phases) |
| **USWDS** | Four phases, thirteen named states. Ph.1 Proposal: *Discussion started · Proposal in progress · Proposal open for comment · Proposal evaluation · Approved · Conditionally approved · Returned for revision · Will not pursue*. Ph.2 Development: *Assigned · In development*. Ph.3 Released: **Experimental · Stable · Use with caution**. Ph.4: **Deprecated · Retired** | The most granular by far; **pre-release states are public**, because contribution is the point | [Component lifecycle](https://designsystem.digital.gov/components/lifecycle/) |
| **GOV.UK** | **Alpha · Beta** *(private or public)* — shipped as the **Phase banner** component, with *Live* as the state at which the banner comes off: *"Services… must use the phase banner until they pass a live assessment."* | ⚠ **This is SERVICE maturity, not component maturity.** GOV.UK's own components do not carry a published per-component maturity badge; its process states live in the community/upcoming pages | [Phase banner](https://design-system.service.gov.uk/components/phase-banner/); [Components index](https://design-system.service.gov.uk/components/) |
| **Shopify Polaris** | **Alpha** *(new/experimental, available for testing, may lack full functionality)* · **Beta** · **Stable** · **Deprecated** *(removed in a future major; warnings in the component file with alternatives)* | 4 stages — and notably a component **can carry Alpha and Deprecated simultaneously**, which is a documented defect of overlaying two orthogonal facets on one badge | [Polaris: Deprecated components](https://polaris-react.shopify.com/components/deprecated); [Polaris web components now stable](https://shopify.dev/changelog/polaris-unified-web-components-are-now-stable) |
| **Carbon, second signal** | The a11y test block on every component page — *"These tests appear only when the components are **stable**"* | A maturity signal delivered as **the presence or absence of a content block**, not as a badge | [Carbon Button](https://carbondesignsystem.com/components/button/usage/) |

### 3.2 What the table actually shows

Four things, none of them obvious before the table existed:

1. **The word "stable" is universal; everything around it is not.** Carbon, USWDS and Polaris all use **Stable** as the terminal good state; Atlassian alone calls it **General Availability**. Nothing else is shared across all four.
2. **"Beta" and "Experimental" are the *same rung* under two names** — and the systems split evenly. Atlassian and Polaris say **Beta**; Carbon says **Preview**; USWDS says **Experimental**. All four definitions agree on the substance: *usable in production, will change more than a stable one.* Carbon: *"available to use in production."* USWDS: *"OK to use but will likely change more frequently than their stable counterparts."* Atlassian Beta: *"new and ready to use."*
3. **Everybody who publishes a bad state publishes TWO of them, not one.** Atlassian: Intent to Deprecate → Deprecated. USWDS: Use with caution → Deprecated → Retired. The two-step exists because *"this is going away eventually"* and *"stop using this now"* are different messages to a consumer, and a single **deprecated** badge cannot carry both.
4. **The most granular vocabulary belongs to the system that most wants contributions.** USWDS publishes eight pre-release states because each is an invitation (*"Contribute by: opening a new component discussion…"*). Carbon publishes four because the audience is consumers, not contributors. **Vocabulary size tracks audience, not system size.**

### 3.3 Recommendation for Apollo's three-word set

**The working assumption `stable / beta / deprecated` is CONFIRMED, with one amendment and one carve-out.**

*Confirmed:*
- **stable** — universal (Carbon, USWDS, Polaris). Take it as-is.
- **beta** — Atlassian's and Polaris's word for the rung Carbon calls Preview and USWDS calls Experimental. All four definitions match; **beta** is the one a reader guesses right without reading a definition, which is v1 §a's own test. Take it.
- **deprecated** — universal wherever a bad state is published (Atlassian, USWDS, Polaris). Take it.

*Amendment — the missing fourth word is the one that will actually bite.* Every surveyed system that publishes a deprecation stage publishes **two**, for the reason in §3.2 point 3. Apollo has 135 components and an active regeneration programme; the state *"this exists, it works, but do not build new things on it"* will arise, and under a three-word set it has nowhere to go — it will get filed as **deprecated** and consumers will stop using something that still works, or filed as **stable** and consumers will build on something that is going away. **Recommend a fourth word: `caution`** (USWDS's *"use with caution"*, shortened; Atlassian's *Intent to Deprecate* is the same rung but is two words and reads as a plan rather than a state). Dave ordered three words, so this is a recommendation to be accepted or rejected, not a substitution.

*Carve-out — do not overlay orthogonal facets on the maturity badge.* Polaris's documented collision (a component simultaneously **Alpha and Deprecated**, [issue #10783](https://github.com/Shopify/polaris/issues/10783)) is the cautionary case. Apollo already has a second axis that will be tempted onto the same badge — **theme coverage** (mono / legacy / console / supercharge). Keep them as two facets. v1 §c.5 said the same thing from the other direction: *"a type filter that isn't a taxonomy level — worth separating in the UI."*

*One mechanism worth stealing regardless of the word-set.* Carbon's a11y block — four named rows (Default state / Advanced states / Screen reader / Keyboard navigation), each with a state, **shown only when the component is stable**. That is maturity expressed as *evidence present or absent* rather than as a claim, and it is far harder to lie with than a badge. Apollo already computes `js > 0` mechanically per component in `gen_library_214.collect()`; the same shape would extend to a "what has been verified" block.

---

## §4 · ADDED #215 — NAME DISTRIBUTION for Apollo's ten most alias-heavy components

### 4.1 Derivation

`ALIASES` in `knowledge/_render/gen_library_214.py` (lines 108–179) holds **70 alias→slug entries** (counted by regex over the literal block, not by eye). `collect()` inverts it to a per-slug alias list; **70 alias attachments land on 46 distinct slugs**, and `residuals["dead_alias"]` is empty — every alias target is a real page.

**Selection rule, declared:** the ten are taken by *alias count descending, then slug alphabetical*. That rule is mechanical and reproducible; it is also what produces the three two-alias entries at the tail (`amount-display`, `avatar-group`, `badge`) rather than any of the other eleven slugs that also carry two.

Comparators throughout are [The Component Gallery](https://component.gallery/components/), read live 2026-08-22. Its "Also known as" line and example count per component are the direct analogue of Apollo's alias table, which is why v1 §c.2 ranked it as the model.

### 4.2 The ten

---

**1 · `dropdown` — "Dropdown" (Element) · 4 aliases: select, picker, menu, context menu**

The Component Gallery splits this into **two separate components**, and the split is the finding:

| Gallery entry | Examples | Also known as | Gallery's own disambiguation |
|---|---:|---|---|
| **Select** | 82 | Dropdown, Select input | *"A form input used for selecting a value…"* |
| **Dropdown menu** | 49 | Select menu | *"…it differs from a select in that it **shows actions or navigation options and is not a form input**."* |

Carbon calls the form input **Dropdown** (in its own component sidebar, observed live), which is exactly the collision the Gallery is warning about — the most-used name in the industry for the *form input* is the Gallery's name for the *other thing*. Apollo's four aliases straddle the split: `select`/`picker` point at the Gallery's **Select**; `menu`/`context menu` point at its **Dropdown menu**. **Apollo has one page where the industry has two concepts.**
*Sources: [Select](https://component.gallery/components/select/) · [Dropdown menu](https://component.gallery/components/dropdown-menu) · [Carbon components nav](https://carbondesignsystem.com/components/button/usage/)*

---

**2 · `selection-controls` — "Selection controls" (Element) · 4 aliases: checkbox, radio, switch, toggle**

Three separate Gallery components collapse into this one page — and they are three of the most-documented components in the industry:

| Gallery entry | Examples | Also known as |
|---|---:|---|
| **Radio button** | 85 | Radio, Radio group |
| **Checkbox** | 84 | *(none listed)* |
| **Toggle** | 60 | Switch, Lightswitch, Toggle button |

GOV.UK ships them as **Checkboxes** and **Radios** (plural, two pages, no toggle at all); USWDS as **Checkbox** and **Radio buttons**; Carbon as **Checkbox** and **Toggle**. **Nobody surveyed publishes a combined "selection controls" page.** The name is Apollo's own coinage — which makes the four aliases load-bearing rather than decorative. ⚠ Note the live hazard already on the record: [[vocabulary-collision-switch-202]] — "switch" means the thumb control to Dave, and it is an alias here.
*Sources: [Radio button](https://component.gallery/components/radio-button) · [Checkbox](https://component.gallery/components/checkbox) · [Toggle](https://component.gallery/components/toggle) · [GOV.UK components](https://design-system.service.gov.uk/components/) · [USWDS components](https://designsystem.digital.gov/components/lifecycle/)*

---

**3 · `command-palette` — "Command palette" (Pattern) · 3 aliases: cmd-k, omnibox, quick open**

**⚠ DECLARED GAP: the Component Gallery has no entry for this component at all** — verified against the full 60-entry index read live on 2026-08-22. It is not under Command palette, Search input, Modal or Navigation. So there is **no name distribution to report**, and that absence is itself the finding: this is a developer-tool convention (VS Code's *Quick Open*, Chrome's *omnibox*, the near-universal ⌘K binding) that the design-system world has not yet named. Apollo's three aliases are, on this evidence, doing more work than any other three in the table. Note also that this component ships `js=0` (PFD-11).
*Source: [Component Gallery index](https://component.gallery/components/) — absence verified by reading the complete list*

---

**4 · `drawer` — "Drawer" (Pattern) · 3 aliases: sheet, off-canvas, side panel**

Gallery entry: **Drawer**, 38 examples, *"Also known as: Tray, Flyout, Sheet"*, defined as *"A panel which slides out from the edge of the screen."* Apollo's `sheet` matches the Gallery's third alias exactly; `off-canvas` and `side panel` are additions the Gallery does not list. Carbon calls its version **UI shell right panel** — *"an optional panel that shows additional system-level actions or content"* — i.e. Carbon does not have a "drawer" at all; it has a shell zone (§1.3). **Six live names for one artefact: Drawer, Tray, Flyout, Sheet, Off-canvas, Side panel.**
*Sources: [Drawer](https://component.gallery/components/drawer) · [Carbon UI shell header](https://carbondesignsystem.com/components/UI-shell-header/usage/)*

---

**5 · `loading-indicator` — "Loading indicator" (Element) · 3 aliases: spinner, loader, throbber**

The richest distribution in the whole survey. Gallery entry **Spinner**, 66 examples, *"Also known as: Loader, Loading"*. The actual per-system names, read off the 66 examples:

| Name used | Systems |
|---|---|
| **Spinner** *(the plurality)* | Atlassian, Backpack, Base Web, Blueprint, Bootstrap, Chakra, Clarity, Crayons, Duet, Evergreen, Flowbite, Fluent UI, Forma 36, Geist, Gestalt, HeroUI, Instructure-UI, Lightning (SLDS), Momentum, Nord, Pajamas, Paste, PatternFly, **Polaris**, Porsche, Primer, Quasar, Red Hat, SEB, Shoelace, Stacks, Wanda, Web Awesome |
| **Loader** | Auro, Cauldron, Decathlon, Elisa, Jøkul, Morningstar, Nessie, Seeds, Seek, uStyle, West Midlands Network |
| **Loading** | **Carbon**, Coral, Elastic UI, Orbit |
| **Loading indicator** *(Apollo's own name)* | **Dell**, Sainsbury's |
| Progress-family | Chakra *"Progress Circle"*, Spectrum *"Progress circle"*, HeroUI *"Circular progress"*, Quasar *"Circular Progress"*, NewsKit *"Progress indicator"*, Ruter *"Progress Radial"* |
| One-offs | Ant Design *"Spin"* · Geist *"Loading dots"* · Thumbprint *"Loader dots"* · Pharos *"Loading spinner"* · Elisa *"LoadingSpinner"* · giffgaff *"Loading icon"* · Workday *"Loading Animation"* · Ruter *"Splash Animation"* · Carbon *"Inline loading"* (a second, separate Carbon component) |

**Apollo's chosen name — "Loading indicator" — is used by exactly two of 66.** The alias `spinner` is therefore not a convenience, it is the primary retrieval path. ⚠ `throbber` appears in **zero** of the 66; it is a historical browser term and worth keeping only as a cheap alias.
*Source: [Spinner](https://component.gallery/components/spinner/) — all names read from the 66 listed examples*

---

**6 · `secure-entry` — "Secure entry" (Element) · 3 aliases: password, otp, pin**

**⚠ DECLARED GAP: no Component Gallery entry.** Nothing for "secure entry", "password", "OTP" or "PIN" in the 60-entry index; the nearest is **Text input** (72 examples). But the concept *is* shipping in production systems under a different name: **GOV.UK ships "Password input"** as a named component ([GOV.UK components](https://design-system.service.gov.uk/components/)), and USWDS ships **Input mask** and **Validation** as the adjacent machinery ([USWDS components](https://designsystem.digital.gov/components/lifecycle/)). **So the concept is real and the Gallery has not caught up** — Apollo's `password` alias points at the one published name that exists.

---

**7 · `sidebar-nav` — "Sidebar nav" (Pattern) · 3 aliases: hamburger, side menu, nav drawer**

| System | What it calls this |
|---|---|
| Component Gallery | **Navigation** (62 examples), *"Also known as: Nav, Menu"* |
| IBM Carbon | **UI shell left panel** — *"an optional panel that is used for a product's navigation"* |
| USWDS | **Side navigation** |
| GOV.UK | **Service navigation** (a distinct, narrower thing) |
| shadcn/ui | **Sidebar** — shipped as a **Block**, not a component |

Note the tier disagreement is as wide as the name disagreement: the same artefact is a *component* (USWDS), a *shell zone* (Carbon), and a *block* (shadcn). This is PFD-2 restated from the outside.
*Sources: [Navigation](https://component.gallery/components/navigation) · [Carbon UI shell header](https://carbondesignsystem.com/components/UI-shell-header/usage/) · [USWDS](https://designsystem.digital.gov/components/side-navigation/) · [GOV.UK](https://design-system.service.gov.uk/components/service-navigation/) · [shadcn Blocks](https://ui.shadcn.com/blocks)*

---

**8 · `amount-display` — "Amount display" (Element) · 2 aliases: money, currency**

**⚠ DECLARED GAP: no Component Gallery entry, and no equivalent in Carbon, Material, Atlassian, GOV.UK or USWDS.** This is a **domain component** — banking-specific — and the industry has no name for it because the industry does not ship it. That is a legitimate finding rather than a hole: it means the two aliases carry the whole retrieval load, and it means this component's page cannot borrow anyone's guidance. Same class as `runway-bar`, `limits-meter`, `standing-order-mandate-row`, `payment-card-visual` (PFD-9).

---

**9 · `avatar-group` — "Avatar group" (Element) · 2 aliases: avatar stack, facepile**

The Gallery ships **Avatar** (38 examples) with **no aliases listed at all**, and has **no separate entry for the group**. So the *singular* is a settled name and the *plural* is not — a clean example of the v1 §a observation that the mid-level assembly is where naming breaks down. **`facepile` is worth keeping**: it is Facebook-origin, widely used in engineering conversation, and appears nowhere in published design-system documentation, so it is exactly the kind of term search must resolve and browsing never will.
*Source: [Avatar](https://component.gallery/components/avatar)*

---

**10 · `badge` — "Badge" (Element) · 2 aliases: pill, label**

The Gallery's **Badge** is its second-largest entry: **123 examples**, *"Also known as: Tag, Label, Chip"*. Apollo's two aliases (`pill`, `label`) partially overlap — `label` matches, `pill` does not appear.

**⚠ Live collision inside Apollo.** The Gallery lists **Tag** and **Chip** as aliases *of Badge*, but Apollo ships **`tags`** as a separate Element **and** **`tags-input`** as another, with `chips` aliased to `tags`. So Apollo has split into three pages what the Gallery treats as one concept with three names — the mirror image of the `dropdown` problem (§4.2 #1), where Apollo has one page for the industry's two. Also note the Gallery's separate **Label** entry (15 examples, *"Form label"*) means `label` is genuinely ambiguous between "badge" and "form label" — and Apollo aliases it to `badge`.
*Sources: [Badge](https://component.gallery/components/badge) · [Label](https://component.gallery/components/label) · [Component Gallery index](https://component.gallery/components/)*

### 4.3 Read-across from the ten

- **Three of ten have no industry entry at all** (`command-palette`, `secure-entry`, `amount-display`). For those, aliases are not a convenience — they are the only retrieval mechanism, because there is no consensus name to guess.
- **Two of ten are splits/merges against the industry**: `dropdown` merges two industry concepts; `selection-controls` merges three; `badge`/`tags`/`tags-input` splits one into three. These are the places where a consumer coming from another system will be most reliably wrong.
- **One of ten uses a name that 2 of 66 systems use** (`loading-indicator`). Renaming is *not* recommended — but it does mean the alias is doing the finding, which is precisely v1 §c.2's ranking of aliases above taxonomy.
- **Zero of ten** would be found faster by a level filter than by search. The Type tab is a browsing aid; the alias table is the retrieval mechanism.

---

## §5 · ADDED #215 — NAVIGATION SCREENSHOTS of the surveyed systems

### 5.1 Status: CAPTURED — with a declared method caveat

Real screenshots were taken. They are **not** mock-ups; each is a headless-Chromium render of the live site, captured 2026-08-22, viewport 1440×1000, with the cookie banner dismissed where one appeared.

| File | Page | HTTP | Page `<title>` as returned |
|---|---|---|---|
| `assets-215-nav/nav-carbon.png` | carbondesignsystem.com/components/button/usage/ | 200 | *Button – Carbon Design System* |
| `assets-215-nav/nav-carbon-elements.png` | carbondesignsystem.com/elements/color/usage/ | 200 | *Color – Carbon Design System* |
| `assets-215-nav/nav-material.png` | m3.material.io/components | 200 | *Components – Material Design 3* |
| `assets-215-nav/nav-atlassian.png` | atlassian.design/components | 200 | *Overview - Components - Atlassian Design* |
| `assets-215-nav/nav-govuk.png` | design-system.service.gov.uk/components/ | 200 | *Components – GOV.UK Design System* |
| `assets-215-nav/nav-shadcn.png` | ui.shadcn.com/docs/components/button | 200 | *Button - shadcn/ui* |

*(Files live at `notes/_briefs/assets-215-nav/`, beside this document. The `nav-carbon.png` render also carries a partially-dismissed IBM cookie panel across the bottom ~15% — the nav, the tab strip and the page head are all unobstructed.)*

**⚠ DECLARED — four environmental obstacles, and what was done about each.** A declared gap passes; a silent one fails.

1. **Playwright's own browser download failed on TLS.** `python3 -m playwright install chromium` failed **five times across three CDN hosts** (`cdn.playwright.dev`, `playwright.download.prss.microsoft.com`, and the fallback path) with `UNABLE_TO_GET_ISSUER_CERT_LOCALLY` — i.e. a TLS-intercepting proxy whose root is not in Node's bundled CA set. **This is the #125 "TLS-blocked" reading reproducing**, which `knowledge/_RUNBOOK-render-verify.md` records as adjudicated-in-favour-of-the-other-reading at #129. It is not adjudicated; it is environment-dependent, and today's environment is the blocked one.
2. **The fix, and it is new:** `export NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt` before the install. With that single variable the download succeeded on the first attempt and landed `chromium-1234`, `chromium_headless_shell-1234` and `ffmpeg-1011` in full. **This is a runbook-grade finding and should be added to `_RUNBOOK-render-verify.md` as a fourth stratum** — it converts the #125 contradiction from "two irreconcilable readings" into "one reading with a known cause and a one-line fix".
3. **Chromium then refused to launch** on a missing `libxdamage1`, with no root to install it. Resolved by pointing `LD_LIBRARY_PATH` at `/var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu`, a foreign-session artefact — the "`/var/tmp` is shared across sessions" fact the runbook records at #129, used constructively. ⚠ **This is a borrowed dependency and it may vanish**; anyone reproducing this should expect to re-source `libXdamage.so.1`.
4. **Chromium then rejected the proxy's certificate** (`ERR_CERT_AUTHORITY_INVALID` on every external host). Resolved with `ignore_https_errors=True` on the browser context. **Declared explicitly:** this skips validation of the sandbox proxy's own certificate. It does **not** route around any block — the proxy still sees and filters every request, every target was already reachable through the sanctioned web tools, and no `curl`/`requests` call was used to fetch any page content. All prose content in this document came from `web_fetch`/`WebSearch`; Chromium was used for pixels only.

### 5.2 Textual descriptions of each system's nav structure

These are written from the renders and from the fetched pages, and stand on their own if the PNGs are ever lost.

**IBM Carbon** — *left sidebar, persistent, full height; black global bar above it.* Three ruled blocks: (i) **All about Carbon · What's happening**; (ii) **Designing · Developing · Contributing · Migrating** — four *jobs*; (iii) **Elements · Guidelines · Components · Patterns · Community assets · Data visualization · Help**, then **GitHub ↗**. Every entry is a disclosure with a chevron. When **Components** is expanded it becomes a **flat alphabetical list** (Overview, Accordion, AI label, Breadcrumb, Button, Checkbox, Code snippet, Contained list, Content switcher, Data table, Date picker, Dropdown, File uploader, Form, Inline loading…) — **no sub-grouping, no facets, no chips**. The component's own **Usage · Style · Code · Accessibility** tabs sit in the black band directly under the page title, not in the sidebar. Expanding **Elements** yields eight children: 2x Grid · Color · Icons · Pictograms · Motion · Spacing · Themes · Typography. **Notable: the taxonomy is the third-priority block in the nav, under audience and under system-meta.**

**Material 3** — *icon rail on the far left, ~88px wide, vertical, icons above labels.* Entries: search glyph, then **Home · Get started · Develop · Foundations · Styles · Components · Blog**, with a pair of theme/density toggles pinned at the bottom. There is no visible component tree in the rail at all. The Components page instead opens as a **scrolling editorial page of grouped sections** (Buttons first), and states its own grouping in the intro: *"They can be organized into categories based on their purpose: **Action, containment, communication, navigation, selection, and text input**."* **This is a pure Usage grouping, published as prose rather than as a filter** — the closest thing in the survey to Dave's Usage tab.
*Source: [M3 Components](https://m3.material.io/components)*

**Atlassian** — *collapsible left sidebar plus a top bar.* Top-level, in order: **Get started · Foundations · Components · Rovo UI · Tools · Release phases · Contact us**, with **Search** and a **Theme** control in the header. The footer carries the fuller taxonomy: *What's new · Get started · Foundations · Components · **Patterns** · Tools · Release phases*. Two things stand out: **Release phases is a top-level nav item** — maturity is promoted to a peer of the taxonomy (§3) — and **Rovo UI** (their AI surface) has been given a peer slot beside Components, which is the 2026 version of what Carbon did with Data visualization.
*Source: [Release phases](https://atlassian.design/release-phases)*

**GOV.UK** — *horizontal top nav, six items, no sidebar on the index.* **Get started · Styles · Components · Patterns · Community · Accessibility**, with a "Search Design system" box and a Sitemap link above. Inside Components the page is a **single flat alphabetical list of 35 items**, printed **twice** — once as a "Pages in this section" list and once as the page body — and there is **no filtering UI whatsoever**. The intro states the composition model in one sentence rather than in a taxonomy: *"You can also use the individual components in different patterns and contexts."* A cookie banner occupies the top of the viewport until dismissed. **The smallest surveyed system by component count, and the only one that ships no finding mechanism at all beyond search.**
*Source: [GOV.UK components](https://design-system.service.gov.uk/components/)*

**shadcn/ui** — *left sidebar with two labelled sections; horizontal top nav above.* Top nav: **Home · Docs · Components · Blocks · Charts · Directory · Typeset · Create**, plus "Search documentation…", a GitHub star count, a theme toggle and a **+ New** button. The sidebar is split under two explicit headings: **Sections** (Introduction, Components, Installation, Theming, CLI, Typeset, Skills, Registry, Changelog •) and **Components** (Accordion, Alert, Alert Dialog, Aspect Ratio, Attachment, Avatar, Badge, Breadcrumb, Bubble, Button, Button Group, Calendar, Card…). A right-hand **"On This Page"** rail lists the component's own sections. Two features nothing else surveyed has: the component page carries an **implementation-switcher** (*Base UI | React Aria | Radix UI*) as tabs above the demo, and a **"Copy Page"** control with prev/next arrows — a machine-readable affordance aimed at agents (v1 §c.11). **Blocks and Charts are top-level peers of Components** — the live precedent for Dave's Block tier.
*Source: [shadcn/ui Button](https://ui.shadcn.com/docs/components/button)*

### 5.3 What the five navs say collectively about Usage vs Type

| System | Primary cut | Secondary cut | Any type/level filter? |
|---|---|---|---|
| Carbon | audience/job (Designing, Developing…) | tier via URL path (`/elements/`, `/components/`, `/patterns/`) | **no** |
| Material 3 | audience (Develop, Foundations, Styles) | **purpose** (action, containment, communication, navigation, selection, text input) — prose only | **no** |
| Atlassian | tier (Foundations, Components, Patterns) | **maturity** (Release phases, top-level) | **no** |
| GOV.UK | tier (Styles, Components, Patterns) | — | **no** |
| shadcn/ui | tier (Components, Blocks, Charts) | implementation (Base UI / React Aria / Radix) | **no** |

**Not one of the five ships a type or level filter.** All five encode tier in the *route*, and three of the five add a **second, non-tier axis** as a first-class nav item — purpose (Material), maturity (Atlassian), implementation (shadcn). That is the strongest available evidence for Dave's ruling: **two tabs is the right number, and the second axis should not be another taxonomy.** Apollo's Usage tab is the axis Material publishes as prose and nobody publishes as a control — which makes it a differentiator, not a catch-up.

---

## §6 · ADDED #215 — RECEIPT

**What this document is.** `notes/_briefs/2026-08-21-214-taxonomy-research-v1.md` copied forward byte-for-byte, plus §§1–6 above. v1 is untouched on disk. Versions, never overwrites ([[feedback-version-dont-overwrite]]).

**Store row.** `W-104` in `knowledge/_state.json`, home-anchored at the §2 heading of this document, minted as a textual-span insert (never a whole-file `json.dump`). Without a store row the document is invisible ([[forgotten-document-class]]).

**Sources.** 32 distinct external URLs cited across §§1–5, every one fetched live on 2026-08-22 through the sanctioned web tools. No claim in §§1–5 is carried from memory.

**Figures, and where each came from.**

| Figure | Derivation |
|---|---|
| 135 components | `gen_library_214.collect()` run against the live repo, this session — one row per `showroom/*.html` excluding `index.html` |
| atom 18 / molecule 57 / organism 33 / lockup 9 / shell 7 / template 11 | `Counter(r['level'] for r in rows)` on the same run; sums to 135; zero `unfiled` |
| 70 alias entries | regex count over the literal `ALIASES` block in `gen_library_214.py`, lines 108–179 |
| 70 attachments on 46 slugs | `alias_by_slug` inversion inside `collect()`; `residuals["dead_alias"] == []` |
| all Component Gallery example counts | read off [component.gallery/components/](https://component.gallery/components/) and the [Spinner](https://component.gallery/components/spinner/) page, 2026-08-22 |
| 12 PFD rows / 41 components affected | counted from §2.3 |

### CONSEQUENCES

1. **§2 is a MAP, not a RULING.** The 135 placements follow the *existing* mechanical derivation in `gen_library_214.py`. Dave ruled the *words* (`s215-D4`); he has not ruled the *boundaries*. If any PFD row is accepted, `level_of()` changes and the table changes with it — the table must be regenerated, never hand-patched.
2. **Map A vs Map B is a live fork.** The doc recommends Map A (no Primitives tier) on evidence, but the recommendation is reversible and the switch is one config array in `gen_library_214.py` (`LEVELS`). Whichever Dave takes, `LEVELS` and this table must be changed in the same motion or they fork.
3. **The fourth lifecycle word is a recommendation against Dave's stated three.** §3.3 confirms `stable / beta / deprecated` and then argues for `caution` as a fourth. That is a press on a stated position, offered with evidence ([[feedback-press-on-deferments]]); it is Dave's to reject.
4. **The screenshots depend on a borrowed library.** `libXdamage.so.1` came from `/var/tmp/chromelibs-s213e2`, a foreign session's artefact. The PNGs are permanent; the *ability to re-shoot them* is not.
5. **`NODE_EXTRA_CA_CERTS` is a runbook-grade finding and is NOT yet in the runbook.** §5.1 records it here. It should be added to `knowledge/_RUNBOOK-render-verify.md` as a fourth stratum — this document is not that runbook, and a finding recorded only in a brief is a finding that will be re-discovered ([[feedback-read-the-runbook]]).

### PITFALLS

- **⚠ Do not read §2.2 as a component inventory.** It is one row per *showroom page*. `template-list-index.html` ends in `index.html` and is excluded by basename equality, not by `endswith` — a trap `gen_library_214.py` already documents at selftest bite 8. Any re-derivation must preserve that.
- **⚠ The plural slugs are collection pages** (PFD-10). Counting `cards` as one component understates the artefact count and overstates the tier's tidiness. Any headline "Apollo has N components" figure is wrong in one direction or the other and should say which.
- **⚠ `chart-sparkline` is filed one tier below the other fourteen charts.** Any chart carve-out that greps `chart-*` will catch it; any carve-out that filters on `level == 'organism'` will silently miss it. Filter by slug prefix, not by level.
- **⚠ "Preview" ≠ "beta" in Carbon's sense of readiness.** Carbon's **Preview** is explicitly *"available to use in production"*. If Apollo's `beta` is read as "not for production", the word has been imported with the opposite meaning to its strongest precedent. Define it on the page.
- **⚠ `switch` is an alias on `selection-controls` and a ruled vocabulary collision** ([[vocabulary-collision-switch-202]]). Anything that surfaces aliases to Dave should expect "switch" to mean the thumb, not the component.
- **⚠ `ignore_https_errors=True` is in the screenshot script.** It is correct for this sandbox's TLS-interception proxy and wrong as a default. Do not copy the script forward without re-reading §5.1 point 4.
- **⚠ The Component Gallery is one source with one maintainer.** Its "also known as" lists and example counts are curated, not exhaustive; three of Apollo's ten most-aliased components are absent from it entirely (§4.3). Absence there is evidence of *no published consensus name*, not evidence that no system ships the thing.

---

## Sources ADDED #215

[Carbon: Button, Usage tab](https://carbondesignsystem.com/components/button/usage/) · [Carbon: UI shell header, Usage tab](https://carbondesignsystem.com/components/UI-shell-header/usage/) · [Carbon: Color, Usage tab](https://carbondesignsystem.com/elements/color/usage/) · [Carbon: Spacing, Overview tab](https://carbondesignsystem.com/elements/spacing/overview/) · [Carbon: Component checklist](https://carbondesignsystem.com/contributing/component-checklist/) · [Carbon: What is Carbon](https://carbondesignsystem.com/all-about-carbon/what-is-carbon/) · [Atlassian: Release phases](https://atlassian.design/release-phases) · [Atlassian: Components](https://atlassian.design/components) · [USWDS: Component lifecycle](https://designsystem.digital.gov/components/lifecycle/) · [USWDS: Side navigation](https://designsystem.digital.gov/components/side-navigation/) · [USWDS: Component status](https://designsystem.digital.gov/components/status/) · [GOV.UK: Components](https://design-system.service.gov.uk/components/) · [GOV.UK: Phase banner](https://design-system.service.gov.uk/components/phase-banner/) · [GOV.UK: Service navigation](https://design-system.service.gov.uk/components/service-navigation/) · [Material 3: Components](https://m3.material.io/components) · [shadcn/ui: Button](https://ui.shadcn.com/docs/components/button) · [shadcn/ui: Blocks](https://ui.shadcn.com/blocks) · [Polaris: Deprecated components](https://polaris-react.shopify.com/components/deprecated) · [Polaris: web components now stable](https://shopify.dev/changelog/polaris-unified-web-components-are-now-stable) · [Polaris issue #10783 — Alpha and Deprecated simultaneously](https://github.com/Shopify/polaris/issues/10783) · [Component Gallery: index of all components](https://component.gallery/components/) · [Component Gallery: Spinner](https://component.gallery/components/spinner/) · [Component Gallery: Select](https://component.gallery/components/select/) · [Component Gallery: Dropdown menu](https://component.gallery/components/dropdown-menu) · [Component Gallery: Drawer](https://component.gallery/components/drawer) · [Component Gallery: Toggle](https://component.gallery/components/toggle) · [Component Gallery: Radio button](https://component.gallery/components/radio-button) · [Component Gallery: Checkbox](https://component.gallery/components/checkbox) · [Component Gallery: Badge](https://component.gallery/components/badge) · [Component Gallery: Label](https://component.gallery/components/label) · [Component Gallery: Avatar](https://component.gallery/components/avatar) · [Component Gallery: Navigation](https://component.gallery/components/navigation)
