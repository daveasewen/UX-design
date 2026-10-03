---
name: ADS-generate-from-canon
description: Compose a screen or component from the Apollo design system's knowledge graph — ask the graph which parts answer each question the screen must answer, which rulings govern them and which rules they obey, then build from those parts' own reviewed markup, tokens, type composites and layout rails. Never invents a component, and never traces a template. Flags anything the system is missing instead of improvising. Use when you want on-brand, accessible UI drafted by construction. Outputs React (preferred) or plain HTML/CSS. Use this whenever the thing being asked for IS a piece of UI, however casually it is put — “build me a dashboard”, “build a screen”, “make a page”, “design a settings page”, “create a form”, “mock up a view”, “add a card to this screen”, “put a table on that page”, “can you lay this out”.
---

# Generate from canon — compose, never trace

Draft UI **strictly from the design system**, and **compose it** from the system's parts. Two
failures are ruled out here, and they are opposites:

- **Inventing** — quietly making up a component, variant or colour. If it isn't in the system,
  this skill flags it rather than making it up.
- **Tracing** — copying a finished template page and editing it down. A template in this pack is
  a **worked example** the gates were proved on. It is never the starting point of your page.

What sits between them is the job: the knowledge graph says which part is right for each question
the screen must answer, which of Dave's rulings govern it, and which rules it obeys. You choose from
that, you copy each chosen part's own markup, and you arrange the parts on canon's layout grammar.

**Strict about the interface, ambitious about the build** (`s258-D2`). The tokens, classes,
components and layout rails are the boundary — the JavaScript is not. Assume everything on the page
should *work*: rich mock data, live filters, real state. Writing code is an avenue to innovation
here, not a violation. When the system is genuinely missing a *component*, use
`ADS-draft-a-new-pattern`.

## Where things live

The graph first, then the four files for the parts it names.

| question | where |
|---|---|
| **Which parts, and under what law?** | `knowledge/_compose_slice.py` — the **reader** (`s277-D10`, `s278-D1`, shipped by `s279-D1`). One run gives the **seed**: the components for each role the brief needs, the rulings that govern them (`governs`), the rules and principles they obey (`obeys`), what they must not sit beside (`mustNot`), their token groups, their assets, and what it could not resolve (`unresolved`). Its **ASK** door answers one of twelve questions live, in under 1K tokens. |
| **What is the Constitution?** | `knowledge/_rulings.json` — every ruling, by id, with Dave's words. The reader reads it live; you cite ids from it. |
| **What exists?** | `showroom/index.json` — every component and foundation, with `slug`, `name`, `aliases`, `blurb`, `level` (element / pattern / block / shell / template), `status`, `related`, `page`. |
| **What does it look like?** | `showroom/<slug>.html` — the live page, every variant and state. `showroom/_thumbs/<slug>.png` for a glance. |
| **What is its contract?** | `knowledge/components/<slug>.meta.json` — `purpose`, `provides` (its role), `answers`, `shape`, `when` (when it is the right part), `priority`, `props`, `variants`, `relationships`, `edges` (`yieldsTo`, `mustNotNeighbour`, `groupsWith`, `obeys`, `governedBy`), `accessibility`, `antiPatterns`, `behaviour`. |
| **What is the real markup?** | `knowledge/snippets/<Slug>.reference.html` — the reviewed, gated source of **one component**. Copy from here. Never re-draw a component from the picture. |

⚠ **Filenames are the index `slug`, but the capitalisation isn't consistent** between the two
folders — `summary` has `knowledge/components/summary.meta.json` and
`knowledge/snippets/Summary.reference.html`; `cta-lockup` has
`knowledge/snippets/CTA-lockup.reference.html`. Match the slug **case-insensitively** (glob
it) rather than guessing the case. The seed's `components[].meta` and `components[].snippet`
fields give you both paths already resolved.

Everything else: `knowledge/canon/canon.css` (all tokens, aliases, utilities and components — what
you LINK, not what you read), `knowledge/canon/type.css` (the type composites),
`knowledge/assets/icons/` (glyphs + `icons.manifest.json`), `knowledge/guidelines/` (the briefing
notes; `_rules-index.json` indexes their rules, each tagged BLOCKING / ADVISORY / REVIEW / TASTE),
`knowledge/_render/_bento_edit_rails.json` (the layout dials), `showroom/_foundations/` (grids,
bento, logos, photography).

## Rules (non-negotiable)

1. **Only what exists.** Every component and variant comes from the seed, `showroom/index.json` or
   `knowledge/components/`. Missing what you need? Put it on a **Gaps** list and stop — never
   improvise a component or a variant.
1a. **Compose, never trace.** Every part of the page is chosen for a question the screen must
    answer (procedure step 2), not inherited from a page that already exists. A template —
    anything at `level: template` in `showroom/index.json`, including
    `Template-dashboard-bento.reference.html` and `Template-dashboard.reference.html` — is a
    **fenced example** (meta `fence: "example"`). Dave, 14:55 2026-10-02, verbatim: "the page
    templates are only example or inspiration in the library for designers. automated build need
    to ignore these, I don't want builds to trace pages." So a build does not open a template at
    all — not its snippet, not its meta: the compose door never offers one (the seed cannot name
    it), and `knowledge/_validate_example_fence.py` refuses a built page that wears a template's
    scope or shares its body. Choose every module yourself from the parts the graph answers with.
    A page whose structure is a template's with the words changed has traced it, however it was
    produced.
2. **Copy the component's snippet, don't re-draw it.** Once the graph has chosen a component, take
   its markup and classes from its own `knowledge/snippets/<Slug>.reference.html`, whole. Hand-
   rolling a component from its screenshot invents defects that the gates then catch as yours
   (`s230-D1` beat 3: component markup from `knowledge/snippets/`, zero invented markup — at the
   level of the **component**, never of the page).
   ⛔ **Never copy inside a fence** (`s258-D3`). Markup, CSS or script between
   `<!-- ===== APOLLO-DEMO <what> START (showroom harness — never copy) ===== -->` and its matching
   `<!-- ===== APOLLO-DEMO <what> END ===== -->` — and the CSS/JS-comment form
   `/* ===== APOLLO-DEMO <what> START … ===== */` … `/* ===== APOLLO-DEMO <what> END ===== */` — is
   **showroom harness, not the component**: width dials, state switchers, demo labels, `demo-*`
   wrapper classes and the script that drives them. Copy what is OUTSIDE the fences and nothing
   inside them; the component still renders with every fenced span deleted, which is exactly what
   the fence guarantees. A generated page that carries an `APOLLO-DEMO` marker is refused by the
   receipt gate as `FAIL:DEMO-CHROME-COPIED`.
2a. **You write the JavaScript** (`s258-D1` — the old "author no JS" rule is REMOVED). Copy a
    snippet's own `<script>` (or its `AUTO-BEHAVIOUR` block) **verbatim where it fits** — the bytes
    are the key and a verbatim copy is still the cheapest correct answer — but you are expected to
    write the wiring the snippets cannot know about, and you may extend a component's script.
    Extend it and the gate says `NOTE:AUTHORED-JS`, not FAIL; delete a declared script entirely and
    it still says `FAIL:BEHAVIOUR-NOT-LOADED`. Where a component declares an ADDRESS in its meta
    (`behaviour.script`), carry that address into the page's receipt and into the
    `#behaviour-manifest` block beside `#token-manifest` — it names the source you started from, not
    a promise you left it untouched. `fallback` says what the component does with JavaScript off;
    if it is null, say so in the Gaps list rather than inventing one.
    ⛔ Rule 2's fence applies to scripts too: a `<script>` fenced as `APOLLO-DEMO` is the showroom's
    dial-and-switcher harness, never the component's behaviour — never copy it, and never carry it
    as the declared `behaviour.script` bytes.
3. **Bind every visual value to a token by intent** — never a raw hex or px. The names live in
   `knowledge/tokens/*.json` and resolve in `knowledge/canon/canon.css`
   (`primary/background/hover` → `var(--primary-background-hover)`). Spacing, radius and border width
   are tokens too, not just colour: a raw px freezes the thing in every theme.
3a. **The page arranges parts; it never resizes them.** Your own `<style>` may place a part (which
    tile, which span, which order) and nothing else. No `font-size`, `height`, `min-height`,
    `padding`, `width`, `zoom` or `transform` on a `.cn-*` scope or anything inside one, and no
    redefinition of a `.c-*` or `.cn-*` class. A component that renders smaller or larger on your
    page than on its showroom page has been restyled — undo it. (This is rule 2 made checkable: a
    snippet copied whole renders at its own size.) The app shells are the one part with two ruled
    heights: 640px is their specimen frame, and a page that is the app takes the full-height form by
    adding `is-full` to `.sh` — choosing a form the part carries, not resizing it.
4. **Type via composites.** Component text takes a class from `knowledge/canon/type.css` —
   `.t-cm-*` for component text (button, label, caption, input, figure-1…6, chart-label,
   ctl-12/14/16), `.t-ed-*` for editorial (display-1/2, heading-1…4, body, body-small, caption).
   Never a raw `font-size` / `font-weight` / `line-height`.
5. **Pick a theme and say which.** Four ship: **mono** (the baseline), **common**, **console**,
   **supercharge** — the same four names the cold-start `DESIGN-CONTRACT.md` asks about. (`legacy`
   is the older key for **common** and still resolves — `s227-D8` made the alias additive — but new
   work emits `common`.) Set them on the root element:
   `class="canon" data-apollo-theme="common" data-theme="light"`. The theme registry is
   `knowledge/tokens/themes/_themes.json`, and it records which colours belong to which theme. A
   colour from another theme's set is a leak, not a choice.
6. **Colour is meaning, and the reds are keyed to their background** (`s151-D1`).
   - Coloured red or green **text** exists in exactly one place: monetary values, always next to a
     symbol (minus, plus, up/down arrow). Nowhere else.
   - Two reds, chosen by the background behind them, not by light/dark mode: the dark red `#DA1A00`
     on **white**, the light red `#F6604C` on **everything else** — dark mode and every non-white
     ground alike.
   - Error checkboxes and radios take the red on the **mark only**. The label keeps default ink.
   - In mono, text and glyphs on an error surface take the default dark ink, both modes
     (`s149-D1`). White-on-error does not exist.
   - Ink itself is a token, not a literal — it resolves per theme (and it is never pure black).
     Bind to it; don't type a hex.
7. **Layout comes from the rails, not from taste.** For bento, grids and the layout dials, read
   **one file**: `knowledge/_render/_bento_edit_rails.json`. It carries every dial, its legal option
   set, the per-theme default, which options may be combined (chords) and which exclude each other
   (`s219-D1`, `s219-D3`). Generation ships the defaults — you do not have to decide anything up
   front. If a layout question isn't answered there, it's a Gap. Spacing picks from the ruled stops
   `{1, 2, 4, 16, 24, 40}`, never a free value. No ragged layouts (`s249-D5`): parts that share a
   row share their top and bottom edges, and gutters are equal wherever the rails say they are.
7a. **Dashboards are bento-first, or you ask** (`s230-D1` beat 2). The rails are the *dial
    vocabulary*; this is the *layout choice*, and it is not yours to make silently. When the
    request is a dashboard — an overview, a landing screen, a wall of panels — say this, in your own
    reply, before you build:

    > **dashboard bento — is that right?**

    Then go bento-first unless the designer says otherwise. **A skip is a yes**, exactly as in
    `ADS-grill-me`: a shrug never counts as a no, and you never wait for permission to proceed.
    **Bento-first means the page is laid out on canon's bento grammar — not that you start from
    the bento template.** Borrow the wall's *grammar*, never its *content*. The grammar is canon
    classes, defined in `knowledge/canon/canon.css` and described in
    `knowledge/components/template-dashboard-bento.meta.json` under `$bentoGrammar` (`s217-D2`
    bento-of-bentos, `s217-D3` the dashboard role):

    ```html
    <div class="cn-template-dashboard-bento">           <!-- the scope: carries the per-theme gutters -->
      <main class="tpl-page">
        <div class="c-bento tpl-wall" data-bento-role="dashboard" aria-label="…">
          <div class="c-bento__grid">
            <section class="c-bento__tile c-bento tpl-group tpl-group-lead" data-bento-role="dashboard"
                     data-c="…" aria-label="…">        <!-- one group = one question (rule 7b) -->
              <div class="c-bento__grid">
                <div class="c-bento__tile" data-c="…"> …one chosen component, whole… </div>
              </div>
            </section>
          </div>
        </div>
      </main>
    </div>
    ```

    Everything inside the tiles — which groups exist, which questions they answer, which component
    answers each, the headings and the data — comes from your brief and the graph (procedure step
    2), never from the template file. The gutters, radius and grounds come from the scope and the
    rails' defaults; you never set them yourself. Spans come from the rails; the composition gate
    (`knowledge/_validate_composition.py`) reads span legality off the page and blocks an orphan
    cell. `showroom/_foundations/bento.html` and `Template-dashboard-bento.reference.html` are the
    worked examples you may read; neither is the thing you copy.
    ⚠ **If the request is not dashboard-shaped and no single part fits, ask.** Do not reach for a
    template that is merely close, and do not compose a template's worth of screen without saying
    that is what you are doing.
    ⚠ `Template-dashboard.reference.html` is `.l-grid`-based, not bento. It is a legitimate
    non-bento *example* and it is **not** the answer to "build me a dashboard" unless the designer
    answered the question above with a no — and even then it is read for its grammar, not traced.
7b. **Grouping comes from the graph, not from the class name.** Whether two modules share a group
    is a fact stored ONCE, as an `edges.groupsWith` entry in the member's meta (`s245-D7`, the
    positive twin of `mustNotNeighbour`). A group is members that answer ONE question the user came
    with — never "the KPIs, because they are KPIs"; its members are uniform in kind, carry one
    accessible name and one containment signal, and stay contiguous at every band. Read the edge
    before you draw a `<section>`; where the edge is `ref:null` the grouping is undecided and is a
    Gap, not a guess. HOW MANY groups a screen has, and what belongs in each, is the designer's
    product decision — never yours. The group classes are ROLE words (`tpl-group-lead` /
    `-evidence` / `-context`), never content types.
8. **Icons are real assets only** — from `knowledge/assets/icons/`, or the seed's `assets` list.
   Never draw a glyph. If a shape is genuinely custom, mark it `<svg data-bespoke="why">` so it reads
   as a decision rather than an invention.
8a. **The mark is the masterbrand, and it is already bound.** Mastheads carry
    `knowledge/assets/logos/masterbrand-light-colour.svg` on light chrome and
    `knowledge/assets/logos/masterbrand-dark-colour.svg` on dark. This is the DEFAULT and it needs
    no question — the shell and navigation snippets bind both files already, so rule 2 gets it
    right on its own. **Ask only when the brief names a different brand**, and then stop and treat
    it as a Gap: never re-key the mark, never set a wordmark in type, never draw one. The other
    files in `knowledge/assets/logos/` are chosen deliberately or not at all —
    `showroom/_foundations/logos.html` shows the set.
9. **Honour the graph's prohibitions.** The seed's `mustNot` rows (and each meta's `antiPatterns`
   and `relationships`) are binding — a `ref:null` prohibition is still a prohibition. A part's
   `yieldsTo` edge means another part takes the case its `when` names; follow it.
10. **Cover the states**: default / hover / pressed / focus / disabled / loading / error / empty, as
    the component defines them.
11. **Sentence case** for headings and labels. No ALL-CAPS outside acronyms.
12. **Carry provenance** — note which component, which tokens, which rulings and which `when`
    clause each part came from (the decision table, step 2).
13. **A DATA MODEL comes first.** Before any markup, write **one** in-page JS dataset —
    `const DATA = {…}` in a single `<script>` — and make every KPI, chart, grid, filter option and
    drawer read from it. No number is typed twice into the HTML. It is **rich and deep** and
    plausible for the domain (`s258-D2`): named entities with ids and relationships to each other,
    real currencies and units, a time series long enough to shape a chart, enough rows that paging
    and sorting mean something, a spread of statuses and dates. Derive KPIs from the rows — never
    hard-code a total that a filter would falsify.
14. **Every control does something visible.** Nothing on the page is decorative. Filters re-drive
    the grid **and** the KPIs **and** the charts (a filter that moves the grid but leaves a chart
    identical is a defect, not a shortcut). Nav switches the view. Sort sorts. Paging pages. Search
    searches. Drawers, modals, menus and tabs open, close and return focus. A CTA that opens nothing
    is a Gap, not a button. Wiring that reaches ACROSS components is yours to write (rule 2a).
    **Wire by delegation.** Controls inside markup you RENDER from `DATA` do not exist when a
    per-element listener runs; attach one listener to a static ancestor and dispatch on
    `event.target.closest('[data-action]')`.
15. **State survives a reload.** Filters, nav/view, sort, page size and theme persist — URL query
    params (shareable, preferred) or `localStorage` — and are read back on load so the page comes up
    where it was left. Reflect state in the URL as the user changes it.
16. **Zero uncaught JS errors on load**, and none on any interaction you wired. Open the console
    before you claim it. A page that throws has not been built, only written.
17. **Every page shell carries a footer.** A screen ends in the shell's footer region — never a page
    that stops at the last card.
18. **Charts are drawn by the library's engine, from `DATA`** (`s249-D4`). Every registered chart
    snippet carries the engine in its `AUTO-BEHAVIOUR` block — `knowledge/canon/dv-render.js` plus
    its type partial — and exposes `window.dvRender(figureEl, spec)`: the library owns the
    arithmetic, you own the data. Copy the chart's snippet whole (rule 2), keep its `<table>` spine,
    and call `dvRender(figure, spec)` with a spec built from `DATA` —
    `{ type, categories, series:[{name, values}], format?, unit?, caption? }` (the full contract is
    the header of `knowledge/canon/dv-render.js`). **Re-render on every filter change** (rule 14) by
    calling `dvRender` again with the new spec.
    **Traps.** (a) The `.dv-*` chrome in `canon.css` is namespaced under the chart's scope class
    (`:where(.cn-chart-bar)` and siblings); drop that wrapper and the svg takes no size, bars never
    animate, the tip is unstyled. (b) Theme attrs go on `<html>`, never on the element carrying a
    `.cn-*` scope (step 5). (c) Marks you render don't exist when a per-element listener runs —
    delegate (rule 14). (d) Hand-authored SVG geometry is the last resort, only for a chart type the
    engine does not register; then the marks carry fractional x (`data-fx`, `data-fw`, …) so
    `knowledge/canon/dv-behaviour.js` can fit them, every re-render ends with
    `dispatchEvent(new Event('resize'))` (the only re-fit hook dv-behaviour exposes), and the
    manifest names your renderer under `authored`.

## Procedure

0. **Brief first.** Look for the newest `briefs/*-grill.md` in the project. If one exists, **read
   it and cite it** in the used/missing note — which brief, and which of its answers shaped the
   build (theme above all). If there is none, run the `ADS-grill-me` skill; if the designer would
   rather not, ask **one** question before you build — *which theme?* — because rule 5's four themes
   differ in corner shape as well as colour, and **mono makes every radius zero by design**. If the
   theme question is skipped too, **say which default you are using before you build** — mono, and
   square — and record it as a default, never as a choice. Never pick a theme silently. If the
   request is a dashboard, rule 7a's question goes in this same reply.
1. **Seed — ask the graph, do not read the library** (`s277-D10`, `s278-D1`). Run the reader once
   on the brief and work from the slice it returns:
   ```
   python3 knowledge/_compose_slice.py "<the brief, in one or two sentences>" --out seed.json --explain
   ```
   Read `components` (one winner per role plus alternates, each with its `when`, `snippet`, `meta`
   and `why`), `governs` (the rulings over those parts, BLOCKING), `obeys` (the rules and principles
   they obey, BLOCKING first), `mustNot`, `tokens`, `assets` and `unresolved`. A field that is
   `null` says why in `$nulls`. **Treat `unresolved` as your work list, not noise:** a role the
   reader could not fill (a chart asked for with no stated intent is the usual one) is resolved by a
   second, typed run for that panel —
   ```
   python3 knowledge/_compose_slice.py "<one panel's question>" --intent change-over-time --shape "time-series × 1–5-series" --out seed-panel-2.json
   ```
   (`--roles`, `--intent`, `--shape`, `--components`, `--budget` are the typed inputs;
   `python3 knowledge/_compose_slice.py --help` lists them). Over a token budget the seed reduces
   by declared steps and says so in `sized`; it never truncates silently.
   **Ask on demand.** When a later question needs a node the seed excluded — or a ruling inscribed
   after it — use the ASK door, which reads the Constitution live:
   ```
   python3 knowledge/_compose_slice.py --ask "what governs component:data-grid?" --seed seed.json
   python3 knowledge/_compose_slice.py --ask "which components answer change-over-time?"
   python3 knowledge/_compose_slice.py --ask "what must component:drawer not sit next to?"
   ```
   The twelve questions are governs · binds · principle · conflicts · ruled · evidence · answers ·
   avoid · tokens · usedIn · wcag · assets. A refusal names its first obstacle; do not work around
   it.
   **Fallback, declared, not default:** only if `knowledge/_compose_slice.py` is not in the pack you
   were given, read the metas of the parts `showroom/index.json` names for each role — and write
   `step 1: metas-read fallback (no reader in pack)` in the used / missing note.
2. **Decide each part — the decision table, before any markup.** List the questions the screen must
   answer (from the brief; for a dashboard, the designer's questions, rule 7b). For each question
   write one row: **question → role → the component chosen → the `when` clause that is true for
   your data → the rulings from `governs` that bind it.** Choose by the graph, in this order:
   (a) a provider whose `when` is **false** for your data is out; (b) among the rest, the one whose
   `when` claims the most things true of your data; (c) a tie goes to the higher `priority`; (d) a
   `yieldsTo` edge or a "yields to …" sentence in the `when` prose hands the case to the named part
   when its condition holds. Where no part's `when` fits, it is a Gap, not a guess. The table goes
   in the used / missing note; it is how a reviewer sees that the page was composed.
3. **Read the contract** of each chosen part: its meta's variants, states, `antiPatterns`,
   `relationships`, `edges`, and **`behaviour`** (the script address, the events it emits and
   handles, and the open/selected contract it expects — e.g. a filter menu that opens on
   `data-open="true"`). Open its showroom page to confirm it is the right thing.
4. **Model the data** (rule 13). Write `DATA` before the markup: the entities the brief implies,
   their relationships, the time series, the currencies, enough rows to sort and page. List the
   behaviours it must support — which filter drives which panel — then build the markup to render
   it.
5. **Compose.** Link `knowledge/canon/canon.css` and `knowledge/canon/type.css`, and load
   `knowledge/canon/click-or-tab.js` **once**, as a `<script src>` in the head — the one shared script
   that tells a click from a Tab, so canon's focus ring shows for the keyboard only (`s315-D26`); a
   part that carries its own copy runs once beside it. **The `<html>`
   element** — not `<body>`, and never the same element that carries a `.cn-*` scope class — gets
   `class="canon"` plus **two** attributes — the theme and the mode: `data-apollo-theme="common|console|supercharge"`
   **and** `data-theme="light"` or `data-theme="dark"`. They are different dials and `canon.css`
   selects on both. **The answer to step 0's theme question lands on `data-apollo-theme`.** A build
   that sets `data-theme` alone is a MONO build — mono is the attribute-less baseline (writing
   `data-apollo-theme="mono"` is legal and self-documenting — it simply selects nothing).
   (`data-mode` is a component-level attribute, not a theme one: in `canon.css` it appears only
   inside `.cn-template-auth`, swapping a light/dark logo mark. Do not put it on the root.) Then, in
   this order: the **shell** from its own snippet (masthead, navigation, footer — copied whole, rule
   17); the **layout** on canon's grammar (rule 7a for a dashboard, the `.c-*` / `.l-*` layout
   utilities otherwise); and each **part** from the decision table as its scope class + its
   snippet's own markup — `<div class="cn-button"><button class="btn primary">…</button></div>` —
   **dropping every `APOLLO-DEMO` fenced span on the way in** (rule 2). **Your own `<style>` is
   placement only** (rule 3a): no hex, no sizes, no redefining a `.c-*` or `.cn-*` class. If you're
   restyling a component locally, you've left canon.
   The long version of this is `knowledge/_RUNBOOK-compose-from-canon.md`.
6. **Gaps.** Anything the system can't supply → the Gaps list. Don't invent.
7. **Prove it.** Run the gates on what you built — see the `ADS-check-with-gates` skill. Composed
   screens have their own runner:
   `python3 knowledge/_validate_screen.py path/to/your-screen.html`.
   A draft you haven't gated is a claim, not a result.
   **Mint the receipt first** — `python3 knowledge/gen_provenance_receipt.py --mint path/to/your-screen.html`
   — then `python3 knowledge/_validate_receipt.py path/to/your-screen.html`. Without a receipt the
   gate stops at `FAIL:NO-RECEIPT` and never inspects the page; every later check (behaviour loaded,
   no demo chrome copied) only runs on a receipted page.
   **No eyes, no browser (a VS Code / Copilot session):** you cannot do step 8 or read a console. Say
   so in the Gaps list as one line — *"not driven: no browser in this session"* — list the controls
   you wired and what each should change, and stop. Do not claim a drive.
8. **Drive it, and measure it.** Load the page, read the console (rule 16), then work every control
   (rule 14) and reload once to prove the state came back (rule 15). Then read the geometry from the
   DOM, not from a screenshot: parts in one row share top and bottom edges; the gutters between
   rows equal the gutters within them; a control bar is as wide as the thing it controls; no tile
   holds dead space below its content; each part's rendered height matches the same part on its
   showroom page (rules 3a, 7). Report what you drove, what each control changed, and each geometry
   reading — untested wiring and unmeasured layout are claims too.

## Output

- The code (React wiring the real components, or HTML/CSS on the canon classes).
- A short **used / missing** note: the seed command(s) you ran, the **decision table** from step 2,
  the components, tokens and rulings drawn on, and any Gaps.
- A **behaviour manifest**: for each control, what it drives, and where its state persists. Where
  you started from a snippet's script, name its address and say whether you carried it verbatim or
  extended it (`s258-D1` — extending is allowed and is reported, not hidden).
- The gate verdict from step 7 and the drive and geometry result from step 8, as they actually
  printed.

> With Figma Dev Mode + Code Connect available you can pull components and variables live;
> otherwise the files above are the source of truth.

*Experimental — feedback on what's missing is the point.*
