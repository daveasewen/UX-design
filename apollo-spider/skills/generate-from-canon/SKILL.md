---
name: ADS-generate-from-canon
description: Build a screen or component using only the Apollo design system — its 135 reviewed components, its tokens, its type composites and its layout rails — never inventing new ones. Flags anything the system is missing instead of improvising. Use when you want on-brand, accessible UI drafted by construction. Outputs React (preferred) or plain HTML/CSS. Use this whenever the thing being asked for IS a piece of UI, however casually it is put — “build me a dashboard”, “build a screen”, “make a page”, “design a settings page”, “create a form”, “mock up a view”, “add a card to this screen”, “put a table on that page”, “can you lay this out”.
---

# Generate from canon

Draft UI **strictly from the design system**. The one job here is to stop the common
failure of AI design work — quietly *inventing* components, variants or colours. If it
isn't in the system, this skill flags it rather than making it up.

**Strict about the interface, ambitious about the build** (`s258-D2`). The tokens, classes,
components and layout rails are the boundary — the JavaScript is not. Assume everything on
the page should *work*: rich mock data, live filters, real state. Writing code is an avenue
to innovation here, not a violation. When the system is genuinely missing a *component*,
use `ADS-draft-a-new-pattern`.

## Where things live

Four files answer almost every question. Go to them in this order.

| question | file |
|---|---|
| **What exists?** | `showroom/index.json` — 143 entries: 135 components + 8 foundations. Each carries `slug`, `name`, `aliases`, a one-line `blurb`, `level` (element / pattern / block / shell / template), `usage` group, `status` (stable / beta / deprecated), `related`, and its `page`. Search this by aliases and blurb, not by guessing a name. |
| **What does it look like?** | `showroom/<slug>.html` — the live page, every variant and state. `showroom/_thumbs/<slug>.png` for a glance. |
| **What is its contract?** | `knowledge/components/<slug>.meta.json` — `purpose`, `props` (with the token each prop `binds` to), `variants`, `tokens`, `relationships`, `accessibility`, `antiPatterns`, `provenance`. |
| **What is the real markup?** | `knowledge/snippets/<Slug>.reference.html` — the reviewed, gated source. Copy from here. Never re-draw a component from the picture. |

⚠ **Filenames are the index `slug`, but the capitalisation isn't consistent** between the
two folders — `summary` has `components/summary.meta.json` and
`snippets/Summary.reference.html`; `cta-lockup` has `snippets/CTA-lockup.reference.html`.
Match the slug **case-insensitively** (glob it) rather than guessing the case. Every one
of the 135 resolves that way.

Everything else: `knowledge/canon/canon.css` (all tokens, aliases, utilities and all 135
components), `knowledge/canon/type.css` (the type composites),
`knowledge/assets/icons/` (659 glyphs + `icons.manifest.json`),
`knowledge/guidelines/` (59 briefing notes; `_rules-index.json` indexes 470 rules from
them, each tagged BLOCKING / ADVISORY / REVIEW / TASTE),
`showroom/_foundations/` (grids, bento, logos, photography).

## Rules (non-negotiable)

1. **Only what exists.** Every component and variant comes from `showroom/index.json` /
   `knowledge/components/`. Missing what you need? Put it on a **Gaps** list and stop —
   never improvise a component or a variant.
2. **Copy the snippet, don't re-draw it.** Take markup and classes from
   `knowledge/snippets/<Slug>.reference.html`. Hand-rolling a component from its
   screenshot invents defects that the gates then catch as yours.
   ⛔ **Never copy inside a fence** (`s258-D3`). Markup, CSS or script between
   `<!-- ===== APOLLO-DEMO <what> START (showroom harness — never copy) ===== -->` and its
   matching `<!-- ===== APOLLO-DEMO <what> END ===== -->` — and the CSS/JS-comment form
   `/* ===== APOLLO-DEMO <what> START … ===== */` … `/* ===== APOLLO-DEMO <what> END ===== */` —
   is **showroom harness, not the component**: width dials, state switchers, demo labels,
   `demo-*` wrapper classes and the script that drives them. Copy what is OUTSIDE the fences
   and nothing inside them; the component still renders with every fenced span deleted, which
   is exactly what the fence guarantees. A generated page that carries an `APOLLO-DEMO` marker
   is refused by the receipt gate as `FAIL:DEMO-CHROME-COPIED`.
2a. **You write the JavaScript** (`s258-D1` — the old "author no JS" rule is REMOVED).
    Copy a snippet's own `<script>` (or its `AUTO-BEHAVIOUR` block) **verbatim where it fits** —
    the bytes are the key and a verbatim copy is still the cheapest correct answer — but you
    are expected to write the wiring the snippets cannot know about, and you may extend a
    component's script. Extend it and the gate says `NOTE:AUTHORED-JS`, not FAIL; delete a
    declared script entirely and it still says `FAIL:BEHAVIOUR-NOT-LOADED`. Where a component
    declares an ADDRESS in `knowledge/components/<slug>.meta.json` (`behaviour.script`), carry
    that address into the page's receipt and into the `#behaviour-manifest` block beside
    `#token-manifest` — it names the source you started from, not a promise you left it
    untouched. `fallback` says what the component does with JavaScript off; if it is null, say
    so in the Gaps list rather than inventing one. Creativity in the JS is wanted; the design
    system's tokens and classes are the boundary, not the script.
    ⛔ Rule 2's fence applies to scripts too: a `<script>` fenced as `APOLLO-DEMO` is the
    showroom's dial-and-switcher harness, never the component's behaviour — never copy it, and
    never carry it as the declared `behaviour.script` bytes.
3. **Bind every visual value to a token by intent** — never a raw hex or px. The names
   live in `knowledge/tokens/*.json` and resolve in `knowledge/canon/canon.css`
   (`primary/background/hover` → `var(--primary-background-hover)`). Spacing, radius and
   border width are tokens too, not just colour: a raw px freezes the thing in every
   theme.
4. **Type via composites.** Component text takes a class from `knowledge/canon/type.css`
   — `.t-cm-*` for component text (button, label, caption, input, figure-1…6,
   chart-label, ctl-12/14/16), `.t-ed-*` for editorial (display-1/2, heading-1…4, body,
   body-small, caption). 31 in all. Never a raw `font-size` / `font-weight` /
   `line-height`.
5. **Pick a theme and say which.** Four ship: **mono** (the baseline), **common**,
   **console**, **supercharge** — the same four names the cold-start `DESIGN-CONTRACT.md`
   asks about, so the pack says back the name the designer said. (`legacy` is the older
   key for **common** and still resolves — `s227-D8` made the alias additive — but new
   work emits `common`.) Set them on the root element:
   `class="canon" data-apollo-theme="common" data-theme="light"`. The theme registry is
   `knowledge/tokens/themes/_themes.json`, and it records which colours belong to which
   theme. A colour from another theme's set is a leak, not a choice.
6. **Colour is meaning, and the reds are keyed to their background.**
   - Coloured red or green **text** exists in exactly one place: monetary values, always
     next to a symbol (minus, plus, up/down arrow). Nowhere else.
   - Two reds, chosen by the background behind them, not by light/dark mode: the dark red
     `#DA1A00` on **white**, the light red `#F6604C` on **everything else** — dark mode
     and every non-white ground alike.
   - Error checkboxes and radios take the red on the **mark only**. The label keeps
     default ink.
   - In mono, text and glyphs on an error surface take the default dark ink, both modes.
     White-on-error does not exist.
   - Ink itself is a token, not a literal — it resolves per theme (and it is never pure
     black). Bind to it; don't type a hex.
7. **Layout comes from the rails, not from taste.** For bento, grids and the layout
   dials, read **one file**: `knowledge/_render/_bento_edit_rails.json`. It carries every
   dial, its legal option set, the per-theme default, which options may be combined
   (chords) and which exclude each other. Generation ships the defaults — you do not have
   to decide anything up front. If a layout question isn't answered there, it's a Gap.
   Spacing picks from the ruled stops `{1, 2, 4, 16, 24, 40}`, never a free value.
7a. **Dashboards are bento-first, or you ask.** The rails are the *dial vocabulary*; this
    is the *layout choice*, and it is not yours to make silently. When the request is a
    dashboard — an overview, a landing screen, a wall of panels — say this, in your own
    reply, before you build:

    > **dashboard bento — is that right?**

    Then go bento-first unless the designer says otherwise. **A skip is a yes**, exactly
    as in `ADS-grill-me`: a shrug never counts as a no, and you never wait for permission to
    proceed. Bento-first means you **splice the snippet**, not re-draw the wall: start
    from `knowledge/snippets/Template-dashboard-bento.reference.html` and edit it down to
    the brief. Rule 2 applies here like everywhere else — hand-rolling a bento wall from
    `showroom/_foundations/bento.html` or straight from canon invents defects. The
    snippet's own scope is `.cn-template-dashboard-bento` over `.c-bento` /
    `.c-bento__grid` / `.c-bento__tile`; the dashboard role's dials read from
    `_bento_edit_rails.json`, and `showroom/_foundations/bento.html` stays the worked
    example you read, not the thing you copy.
    ⚠ **If the request is not dashboard-shaped and no template snippet fits, ask.** Do
    not reach for a template that is merely close, and do not compose a template's worth
    of screen out of loose components without saying that is what you are doing.
    <!-- W-333 (banked, #232): this routing step lives here for now. Its permanent home —
         routing off the knowledge graph rather than off a skill rule — is Dave's to rule. -->
    ⚠ `Template-dashboard.reference.html` is `.l-grid`-based, not bento. It is a
    legitimate non-bento dashboard and it is **not** the answer to "build me a dashboard"
    unless the designer answered the question above with a no.
7b. **Grouping comes from the graph, not from the class name.** Whether two modules share
    a group is a fact stored ONCE, as an `edges.groupsWith` entry in the member's
    `knowledge/components/<slug>.meta.json` (the positive twin of `mustNotNeighbour`). The
    rails' `grouping` dial and this rule are DERIVED from it and never restate it. A group is
    members that answer ONE question the user came with — never "the KPIs, because they are
    KPIs"; its members are uniform in kind, carry one accessible name and one containment
    signal, and stay contiguous at every band. Read the edge before you draw a `<section>`;
    where the edge is `ref:null` the grouping is undecided and is a Gap, not a guess. HOW MANY
    groups a screen has, and what belongs in each, is the designer's product decision — never
    yours (template-dashboard-bento.meta.json:12). The snippet's group classes are ROLE words
    (`tpl-group-lead` / `-evidence` / `-context`), never content types; the composition gate
    (`_validate_composition.py`, step 1b of `_validate_screen.py`) reads span legality off the
    page and blocks an orphan cell.
8. **Icons are real assets only** — from `knowledge/assets/icons/`. Never draw a glyph.
   If a shape is genuinely custom, mark it `<svg data-bespoke="why">` so it reads as a
   decision rather than an invention.
8a. **The mark is the masterbrand, and it is already bound.** Mastheads carry
    `knowledge/assets/logos/masterbrand-light-colour.svg` on light chrome and
    `masterbrand-dark-colour.svg` on dark. This is the DEFAULT and it needs no question —
    the shell and navigation snippets bind both files already, so rule 2 (copy the
    snippet) gets it right on its own. **Ask only when the brief names a different
    brand**, and then stop and treat it as a Gap: never re-key the mark, never set a
    wordmark in type, never draw one. The other ten files in `knowledge/assets/logos/`
    (hexagon, masterbrand-identifier, and the mono treatments) are chosen deliberately or
    not at all — `showroom/_foundations/logos.html` shows the set.
9. **Honour `antiPatterns` and `relationships`** from each component's meta —
   `mustNotNeighbour` in particular.
10. **Cover the states**: default / hover / pressed / focus / disabled / loading / error /
    empty, as the component defines them.
11. **Sentence case** for headings and labels. No ALL-CAPS outside acronyms.
12. **Carry provenance** — note which component and which tokens each part came from.
13. **A DATA MODEL comes first.** Before any markup, write **one** in-page JS dataset —
    `const DATA = {…}` in a single `<script>` — and make every KPI, chart, grid, filter option
    and drawer read from it. No number is typed twice into the HTML. It is **rich and deep**
    and plausible for the domain (`s258-D2`): named entities with ids and relationships to each
    other, real currencies and units, a time series long enough to shape a chart, enough rows
    that paging and sorting mean something, a spread of statuses and dates. Thin data is why
    behaviours have nothing to act on. Derive KPIs from the rows — never hard-code a total that
    a filter would falsify.
14. **Every control does something visible.** Nothing on the page is decorative. Filters
    re-drive the grid **and** the KPIs **and** the charts (a filter that moves the grid but
    leaves a chart identical is a defect, not a shortcut). Nav switches the view. Sort sorts.
    Paging pages. Search searches. Drawers, modals, menus and tabs open, close and return
    focus. A CTA that opens nothing is a Gap, not a button. Wiring that reaches ACROSS
    components is yours to write — that is exactly what rule 2a now allows.
    **Wire by delegation.** Controls inside markup you RENDER from `DATA` (rule 13) do not
    exist when a per-element listener runs; attach one listener to a static ancestor and
    dispatch on `event.target.closest('[data-action]')`. Cold run 5: two KPI CTAs died on
    exactly this, while the same handler on static markup worked.
15. **State survives a reload.** Filters, nav/view, sort, page size and theme persist — URL
    query params (shareable, preferred) or `localStorage` — and are read back on load so the
    page comes up where it was left. Reflect state in the URL as the user changes it.
16. **Zero uncaught JS errors on load**, and none on any interaction you wired. Open the
    console before you claim it. A page that throws has not been built, only written.
17. **Every page shell carries a footer.** A screen ends in the shell's footer region —
    never a page that stops at the last card.

## Procedure

0. **Brief first.** Look for the newest `briefs/*-grill.md` in the project. If one
   exists, **read it and cite it** in the used/missing note — which brief, and which of
   its answers shaped the build (theme above all). If there is none, run the `ADS-grill-me`
   skill; if the designer would rather not, ask **one** question before you build —
   *which theme?* — because rule 5's four themes differ in corner shape as well as
   colour, and **mono makes every radius zero by design**, so a mono build is
   radius-blind: it cannot show you a shape decision you might have wanted. If the theme
   question is skipped too, **say which default you are using before you build** — mono,
   and square — and record it as a default, never as a choice. Never pick a theme
   silently.
1. **Find.** Search `showroom/index.json` for each thing the screen needs — by alias and
   blurb. Open the showroom page to confirm it's the right thing.
2. **Read the contract.** `knowledge/components/<slug>.meta.json` — variants, states,
   antiPatterns, relationships, and **`behaviour`** (s258 cold run 3: the script address,
   the events it emits/handles, and the open/selected contract it expects — e.g. a filter
   menu that opens on `data-open="true"`. Wiring a control without reading this is how
   three toolbar filters died).
2a. **Model the data** (rule 13). Write `DATA` before the markup: the entities the brief
   implies, their relationships, the time series, the currencies, enough rows to sort and
   page. List the behaviours it must support — which filter drives which panel — then build
   the markup to render it.
3. **Compose.** Link `knowledge/canon/canon.css` and `knowledge/canon/type.css`. **The
   `<html>` element** — not `<body>`, and never the same element that carries a `.cn-*`
   scope class — gets `class="canon"` plus **two** attributes — the theme and the mode
   (cold run 5: `data-theme` on `<body>` beside a `.cn-*` class killed the whole dark
   theme silently — canon's theme legs are DESCENDANT selectors and never matched): `data-apollo-theme="common|console|supercharge"` **and** `data-theme="light"` or
   `data-theme="dark"`. They are different dials and `canon.css` selects on both:
   `data-apollo-theme` carries the four themes, `data-theme` carries light/dark only.
   **The answer to step 0's theme question lands on `data-apollo-theme`.** `data-theme`
   has nowhere to put it, so a build that sets `data-theme` alone is a MONO build — and
   mono makes every radius token `0`. Mono is the attribute-less baseline: canon has no
   `data-apollo-theme="mono"` block, so mono is `data-theme` on its own (writing
   `data-apollo-theme="mono"` is legal and self-documenting — it simply selects nothing).
   Same contract as step 5 and as
   `knowledge/_RUNBOOK-compose-from-canon.md` § Compose a screen. (`data-mode` is a
   component-level attribute, not a theme one: in `canon.css` it appears only inside
   `.cn-template-auth`, swapping a light/dark logo mark. Do not put it on the root.) Drop each component in as
   its scope class + the snippet's own markup — `<div class="cn-button"><button class="btn
   primary">…</button></div>` — **and drop every `APOLLO-DEMO` fenced span on the way in**
   (rule 2): the fenced markup, CSS and script are the showroom harness, and the component
   renders without them. Use the `.c-*` layout utilities. **Your own `<style>` is
   harness only**: no hex, no redefining a `.c-*` or `.cn-*` class. If you're redefining a
   component locally, you've left canon.
   The long version of this is `knowledge/_RUNBOOK-compose-from-canon.md`.
4. **Gaps.** Anything the system can't supply → the Gaps list. Don't invent.
5. **Prove it.** Run the gates on what you built — see the `ADS-check-with-gates` skill.
   Composed screens have their own runner:
   `python3 knowledge/_validate_screen.py path/to/your-screen.html`.
   A draft you haven't gated is a claim, not a result.
   **Mint the receipt first** — `python3 knowledge/gen_provenance_receipt.py --mint path/to/your-screen.html`
   — then `python3 knowledge/_validate_receipt.py path/to/your-screen.html`. Without a
   receipt the gate stops at `FAIL:NO-RECEIPT` and never inspects the page; every later
   check (behaviour loaded, no demo chrome copied) only runs on a receipted page.
   **No eyes, no browser (a VS Code / Copilot session):** you cannot do step 6 or read a
   console. Say so in the Gaps list as one line — *"not driven: no browser in this session"* —
   list the controls you wired and what each should change, and stop. Do not claim a drive.
6. **Drive it.** Load the page, read the console (rule 16), then work every control (rule 14)
   and reload once to prove the state came back (rule 15). Report what you drove and what
   each control changed — untested wiring is a claim too.

## Output

- The code (React wiring the real components, or HTML/CSS on the canon classes).
- A short **used / missing** note: components and tokens drawn on, plus any Gaps.
- A **behaviour manifest**: for each control, what it drives, and where its state persists.
  Where you started from a snippet's script, name its address and say whether you carried it
  verbatim or extended it (`s258-D1` — extending is allowed and is reported, not hidden).
- The gate verdict from step 5 and the drive result from step 6, as they actually printed.

> With Figma Dev Mode + Code Connect available you can pull components and variables
> live; otherwise the files above are the source of truth.

*Experimental — feedback on what's missing is the point.*
