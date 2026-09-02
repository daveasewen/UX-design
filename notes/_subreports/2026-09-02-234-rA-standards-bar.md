# `#234`-`rA` — the standards bar: what a hand-off-ready page must satisfy

session: `#234` · 2026-09-02
window: quality-bar research, strand rA
sub index: `rA`
brief: `notes/_briefs/2026-09-02-234-quality-bar-research-brief.md`
tokens: `UNMEASURED — a sub cannot read its own message.usage from its seat; no _checkin.py
reading exists for a sub window.`

## VERDICT

Both regions DONE. The repo grounding was read in full (contract, both skills, three meta files,
the #233 finding set) and the web research is sourced to specs and system documentation, never
marketing. The candidate rubric below is **34 criteria in eight bands**, each carrying the check
that would decide it and a tier — MACHINE (a script can decide it from the file), DRIVE (only a
rendered, driven browser can decide it), EYE (only Dave). The headline finding is a **scope
finding, not a gap finding**: Apollo already owns gates for a large share of the rubric, but on
the path an agent actually hands over, `_validate_screen.py <path>` runs **exactly three**
checks — compose, icon-source, a11y — and every other gate is bound to a fixed folder
(`knowledge/snippets/`, `knowledge/_fitness-test/`, `knowledge/_proforma/`) that an agent's page
is never in. Eleven accessibility ADVISORY checks that already exist — skip-link, `<html lang>`,
pinch-zoom, down-event activation, `aria-required`, `inputmode`/`autocomplete`, paste-blocking,
directional phrases, duplicate links, role-suffix names, all-caps names — cannot see a page at
`my-work/page.html`, because `_validate_advisory.py` globs two directories and takes no path.
Second finding: `_validate_behaviour.py` **already exists** and is NOT what the #233 diagnosis
means by a behaviour gate — it is an ADR-0015 performance contract on dataviz behaviour SOURCES,
so the v1.0.6 brief has a live name collision. Third: the resilience band that produced the #233
line-chart symptom (JS off, engine absent) is written down as an acceptance criterion by both
GOV.UK and USWDS and is checked by no Apollo gate at any scope.

COUNTS: findings `17` · ruling-shaped `4` · UNPROVEN `5`

## What was done

**Region 1 — repo grounding (read-only).**

- `apollo-spider/cold-start/DESIGN-CONTRACT.md` (31 lines, read in full)
- `apollo-spider/skills/generate-from-canon/SKILL.md` (178 lines, read in full)
- `apollo-spider/skills/check-with-gates/SKILL.md` (169 lines, read in full)
- `notes/_briefs/2026-09-01-233-delegated-wrap-brief.md` (120 lines, read in full)
- Three meta files: `knowledge/components/dropdown.meta.json` (read in full),
  `knowledge/components/chart-line.meta.json` (keys + `accessibility` + `behaviour`),
  `knowledge/components/template-dashboard-bento.meta.json` (keys + `accessibility` + `behaviour`)
- Gate inventory: `ls knowledge/_validate_*.py` → **43 scripts**; docstring head of each read via
  `ast.get_docstring`; scope globs read for `_validate_screen.py`, `_validate_advisory.py`,
  `_validate_a11y.py`, `_validate_compose.py`, `_validate_dataviz.py`, `_validate_behaviour.py`,
  `_validate_hit_area.py`, `_validate_snippets.py`
- Pack travel list read from `_to_delete/bake225/Apollo-Spider-v1.0.3/_MANIFEST.json`
  (`version v1.0.3`, `commit_date 2026-08-29`)
- ⛔ `GOOD-MORNING.md` NOT read, per the brief.
- No file in the repo was written except this report. No git operations were run.

**Region 2 — web research.** WCAG 2.2 Recommendation (`https://www.w3.org/TR/WCAG22/`) and the
AAA-filtered quickref, fetched and grepped; ARIA APG *Read Me First*; GOV.UK Frontend
*Test components using accessibility acceptance criteria*; IBM Carbon `docs/guides/accessibility.md`
(AVT1/2/3); USWDS *Documentation (developers)*. Atlassian, Polaris and Material were searched but
returned only third-party blog write-ups at the depth needed — **not quoted**, per the brief's
"quote the spec/doc page" pitfall. That is a declared gap, priced below.

## Findings

**1. WCAG 2.2 is the version to write the rubric against, and it is additive.**
Probe — `https://www.w3.org/TR/WCAG22/`, § New Features in WCAG 2.2: *"This additive approach
helps to make it clear that sites which conform to WCAG 2.2 also conform to WCAG 2.1. The
Accessibility Guidelines Working Group recommends that sites adopt WCAG 2.2 as their new
conformance target, even if formal obligations mention previous versions."* A 2.2 rubric costs
nothing over a 2.1 one.

**2. 4.1.1 Parsing is gone.** Probe — same document, contents entry: *"4.1.1 Parsing (Obsolete
and removed)"*. A rubric line "the HTML validates" is therefore a code-quality criterion, not a
WCAG one, and must not be filed under conformance.

**3. Six of the nine criteria new in 2.2 are at A or AA; Apollo's gates name exactly one.**
Probe — TR § New Features lists 2.4.11 Focus Not Obscured (Minimum) **AA**, 2.5.7 Dragging
Movements **AA**, 2.5.8 Target Size (Minimum) **AA**, 3.3.8 Accessible Authentication (Minimum)
**AA**, 3.2.6 Consistent Help **A**, 3.3.7 Redundant Entry **A**. Counter-probe —
`grep -ho "2\.5\.[0-9]\+\|2\.4\.[0-9]\+\|3\.[0-9]\.[0-9]\+" knowledge/_validate_*.py | sort | uniq -c`
returns `12 2.5.8 · 3 2.5.5 · 3 2.5.2 · 3 2.4.4 · 3 2.4.2 · 2 3.3.2 · 2 3.2.2 · 2 3.1.1 · 2 2.4.7
· 2 2.4.1`. **2.4.11, 2.5.7, 3.2.6, 3.3.7 and 3.3.8 appear in zero gate scripts.**

**4. Three AAA criteria are cheap here; one is not, and one is already half-enacted.**
- **2.4.10 Section Headings (AAA)** — *"Section headings are used to organize the content."*
  `template-dashboard-bento.meta.json` already declares `headingOrder`: *"One `<h1>` (the page
  title). Module titles are `<h2>`/`<h3>`."* The rubric line costs a parse, not a redesign.
- **2.5.5 Target Size (Enhanced, AAA)** — *"at least 44 by 44 CSS pixels"*. Apollo's house floor
  is already 44: `_validate_a11y.py` carries `CONTROL_TIER_44 = "warn"` with the comment
  `# -> "fail" enacts s114-D6 (ordered AFTER s114-D5)`. AAA on this criterion is **one flag flip
  behind a ruled sequence point**, not new work.
- **2.4.13 Focus Appearance (AAA)** and **2.4.12 Focus Not Obscured (Enhanced, AAA)** — both are
  DRIVE-tier (rendered focus geometry). Apollo already drives rendered state in
  `_validate_state_contrast.py`, so the machinery class exists.
- **1.4.6 Contrast (Enhanced, AAA)** — *"a contrast ratio of at least 7:1"*. This is **not**
  cheap: it collides with ruled colour law. UNPROVEN whether the two-red law's `#F6604C`-on-
  non-white pairs clear 7:1; almost certainly they do not. Do not put it in a rubric without
  measuring first.

**5. GOV.UK writes the resilience band down as an acceptance criterion — and it is the #233
line-chart symptom, verbatim.** Probe — `alphagov/govuk-frontend`,
`docs/contributing/test-components-using-accessibility-acceptance-criteria.md`: components should
work when *"JavaScript fails to load, but stylesheets load"*, *"stylesheets fail to load, but
JavaScript loads"*, *"both JavaScript and stylesheets fail to load"*, *"users enlarge the text"*,
*"users zoom to 400%"*, and when *"users change colours on websites"*. Counter-probe — the #233
brief's symptom (b): the line chart shipped *"no tooltips, not responsive = the JS-off fallback
named in `chart-line.meta.json:85`"*. Apollo has the fallback in the meta and no criterion
anywhere that asks whether it was reached.

**6. GOV.UK also fixes the SHAPE of a criterion.** Probe — the same source set, quoted through
the Design System's own accessibility strategy: good acceptance criteria *describe an outcome
rather than the solution*, and the Design System's criteria are *"complementary to WCAG and do
not replace it."* Read against the brief's own pitfall ("a rule that sounds checkable but
isn't"), the tension is real: an outcome-shaped criterion is the one a gate can least often
decide. This is why the rubric below carries a tier per line rather than a pass/fail column.

**7. Carbon splits verification into THREE stages, not two.** Probe —
`carbon-design-system/carbon`, `docs/guides/accessibility.md`: *"Accessibility Verification
Testing (AVT) at IBM is broken up into three stages: **AVT1:** automated checks using tooling
like DAP · **AVT2:** manual checks that cannot be automated through tooling · **AVT3:** manual
checks to verify screen reader support."* Apollo's vocabulary has two tiers (gate / eye). Carbon
splits Apollo's "eye" into *driven-but-manual* and *screen-reader*. Reported, not recommended.

**8. Carbon's AVT2 keyboard list is six concrete, testable conditions.** Probe — same file:
*"All functionality should be available from a keyboard without exception"*; TAB / SHIFT+TAB /
ENTER-or-SPACE / Escape as the standardised keystrokes, with *"Any variance on these standardized
keystrokes should be outlined clearly to the user beforehand"*; a focused state on anything
focusable; no focus trap (*"you should be able to move focus away from that element with a
keyboard"*); tab order that *"makes sense"*; and *"Long or burdensome lists, links, or navigation
should provide a 'skip to main content' link."* Five of the six are MACHINE-decidable in weak
form; "makes sense" is EYE.

**9. Carbon publishes screen-magnifier rules that bear directly on the chart tooltip.** Probe —
same file: *"Tooltips, toasts and popups should be shown to the user adjacent to where they were
triggered"*; *"Tooltips or any word bubble type notifications ... should not depend on a mouse
hover"*; *"Don't obscure content on mouse hover."* `chart-line.meta.json` already answers the
second: *"Markers = focus stops (tabindex 0 + aria-label; popover shows on focus)"* — so the
canon component is compliant and the #233 output was not, because the engine never loaded.

**10. APG names the exact failure mode #233 hit, from the other side.** Probe —
`https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/`: *"Principle 1: A role is a promise …
Using a role without fulfilling the promise of that role is similar to making a 'Place Order'
button that abandons an order and empties the shopping cart."* #233 symptom (a) is an agent that
kept the promise's markup and rewrote the JS behind it (`Dropdown.reference.html:178`); the
generic form of the criterion is *role declared ⇒ the behaviour that role promises is present and
is the system's own*.

**11. USWDS states progressive enhancement as a product property, not a nice-to-have.** Probe —
`https://designsystem.digital.gov/documentation/developers/`: *"All users will have access to the
same critical information and basic experience regardless of their browser … If JavaScript fails
users will still get a robust HTML foundation and all the necessary content."* Same band as
finding 5, from a second independent system.

**12. USWDS's BEM rule is the mechanical shape of "variant, not invention".** Probe — same page,
CSS architecture: *"Modifier classes are additive — proper markup requires the base class *and*
the modifier class or classes."* Also *"Avoids hard-coded magic numbers"* and *"Set theme
settings with USWDS design tokens, not with values directly."* Apollo's `.c-*` / `.cn-*` scoping
has the same shape; the #233 bento symptom (c) — local `--bento-row-unit:460px` overrides and a
`cn-table` class pushed onto stat-cards — is exactly an additive-modifier rule being broken.
(Strand rC owns the contract question; this is noted here only because the *criterion* is a
standards-side one.)

**13. REPO COVERAGE — the hand-off path runs three checks.** Probe —
`knowledge/_validate_screen.py`, docstring lines 6–13 list `1. compose · 2. icon-source ·
3. a11y · 4. state-contrast (optional, --render)`, and line 87:
`files = args or sorted(glob.glob(os.path.join(HERE, "_fitness-test", "*.canon.html")))`. This is
the ONLY gate in the set that accepts a path — `check-with-gates/SKILL.md:68` calls it *"the main
road, and the one to reach for first."* Everything the rubric needs beyond hex / class-resolution
/ icon-provenance / reduced-motion / target-size is not asked on that road.

**14. REPO COVERAGE — eleven existing a11y checks cannot see an agent's page.** Probe —
`knowledge/_validate_advisory.py:229-230`:
`targets = sorted(glob.glob(os.path.join(ROOT, "snippets", "*.reference.html"))) + \
 sorted(glob.glob(os.path.join(ROOT, "_fitness-test", "*.canon.html")))`
and line 186 `screen = "_fitness-test" in path`. The checks stranded behind that glob are
skip-link (SC 2.4.1), `<html lang>` (3.1.1), pinch-zoom (1.4.10), no-activation-on-down-event
(2.5.2), no-submit-on-change (3.2.2), `aria-required` (3.3.2), `inputmode`/`autocomplete`
(1.3.5), no paste-blocking, directional phrases (1.3.3), adjacent duplicate links (2.4.4) and
role-suffix accessible names. The script takes `--root DIR` only, described in its own usage line
as existing *"for bite-tests"*. `check-with-gates/SKILL.md` lists no row for it at all. This is
the memory hook [[gate-glob-scope-rule]] firing on a11y: the rule is only as wide as its gate's
glob, and this glob is two folders wide.

**15. REPO COVERAGE — contrast on a composed page is DRIVE-only in practice.** Probe — static
contrast lives in `knowledge/_validate_snippets.py:256-258` (`need = 4.5 if ctx in ("text",
"icon") else 3.0`) and is driven off a declared `#token-manifest`, i.e. Route C, which
`check-with-gates/SKILL.md:87-93` explicitly tells a non-contributor **not** to use. On a
composed page the only contrast reading is `_validate_screen.py --render`, which needs playwright
and otherwise exits `77` COULD-NOT-ASK. So SC 1.4.3 / 1.4.11 on a hand-off page is, today,
normally *unasked* rather than passed.

**16. REPO — `_validate_behaviour.py` already exists and means something else.** Probe —
`knowledge/_validate_behaviour.py`, docstring: *"Behaviour-contract gate (ADR-0015) … checks every
behaviour SOURCE registered in `knowledge/component-types.json` (`$behaviour` blocks), plus its
member snippets"*, with `MAX_BYTES = 16 * 1024`, `PAGE_BYTES = 34 * 1024`, a banned-API list
(`setInterval`, `fetch`, `XMLHttpRequest`, `WebSocket`, `.style.transform`, `--hs`/`--ps`) and
`no external <script src>` on members resolved at line 129 as
`os.path.join(HERE, "snippets", m + ".reference.html")`. It is a **performance and DEF-003
boundary contract on the library's own JS**, and it never looks at a composed page. The #233
brief proposes *"a `_validate_behaviour.py` gate in check-with-gates"* — that name is taken, and
by a gate that already travels in the pack (`_MANIFEST.json`, v1.0.3).

**17. REPO — a chart pasted into a hand-off page is ungated as a chart.** Probe —
`knowledge/_validate_dataviz.py:532-533`: the population is `_proforma/*.html` files carrying the
`APOLLO-DATAVIZ` signature plus `snippets/Chart-*.reference.html`. Likewise
`_validate_hit_area.py:602` globs `SNIPPETS`. Neither is in `_validate_screen.py`'s chain. The
45KB dataviz gate — the deepest a11y instrument in the repo — cannot grade the artefact the
designer hands to a developer.

---

## THE CANDIDATE RUBRIC

34 criteria, eight bands. **Tier**: `M` = a script can decide it from the file as handed over ·
`D` = needs a driven render (browser) · `E` = eye only, name it and stop pretending. **Repo**
names the existing gate, or `—` for uncovered. `scope✗` means the gate exists but its glob does
not include the hand-off page (findings 13, 14, 17).

### Band A — semantics and structure

| # | criterion | source | check | tier | repo |
|---|---|---|---|---|---|
| A1 | Exactly one `<h1>`; heading levels descend without skipping | SC 1.3.1; bento meta `headingOrder` | parse heading tree | M | — |
| A2 | Section headings organise the content (no orphan `.t-cm-section-label` standing in for a heading) | SC 2.4.10 (AAA); bento meta: *"a TYPE class and never substitutes for a heading element"* | parse: type-class blocks with no heading sibling | M | — |
| A3 | One `<main>`, one `<header>`; each bento group a labelled region | SC 1.3.1; bento meta `landmarks` | parse landmarks + `aria-label` | M | — |
| A4 | `<html lang>` present and true | SC 3.1.1 | attribute present | M | `_validate_advisory` acd-007 **scope✗** |
| A5 | Semantic markup, not `<div>` soup | GOV.UK AAC: *"use semantic markup"* | ratio/heuristic + role census | M (weak) / E (strong) | — |
| A6 | Unique, non-empty `<title>` | SC 2.4.2 | parse | M | `_validate_compose` check 8 (canon.html scope) |
| A7 | Every image/icon has a text alternative or is `aria-hidden` | SC 1.1.1 | parse `<img>`/`<svg>` | M | — |
| A8 | Markup order matches reading order | GOV.UK AAC: *"contain markup in an order that makes sense to users"* | DOM order vs visual order | D (grid re-order detectable) / E | — |

### Band B — keyboard and focus

| # | criterion | source | check | tier | repo |
|---|---|---|---|---|---|
| B1 | Every interactive element is reachable and operable by keyboard | SC 2.1.1; Carbon AVT2 §1 | drive TAB through the page | D | — |
| B2 | Standard keystrokes: TAB / SHIFT+TAB / ENTER-or-SPACE / Escape; any variance documented | Carbon AVT2 §2 | drive; and static: role→expected-keys table | D + M | — |
| B3 | No focus trap | SC 2.1.2; Carbon AVT2 §4 | drive | D | — |
| B4 | Visible focus state on everything focusable | SC 2.4.7; Carbon AVT2 §3 | static `:focus-visible` rule present per control | M (weak) / D (real) | `_validate_snippets` (2.4.7, snippet scope) |
| B5 | Focus is never entirely hidden by author content | SC 2.4.11 **AA, new in 2.2** | drive: focused box vs sticky/overlay geometry | D | — |
| B6 | Tab order makes sense | Carbon AVT2 §5 | — | E | — |
| B7 | Skip-to-content link on a full page | SC 2.4.1; Carbon AVT2 §6 | parse | M | `_validate_advisory` acd-003 **scope✗** |
| B8 | A declared ARIA role carries the behaviour that role promises | APG *Read Me First*, Principle 1 | role→required states/keys/JS-present table | M (weak) / D (real) | — |
| B9 | No ARIA that cloaks true semantics (`role` on a list/table/link that hides it) | APG Principle 2 | parse role-vs-element pairs against a deny table | M | `_validate_a11y` CTRL vocabulary (unknown role fails loud) — snippet scope |

### Band C — colour and contrast

| # | criterion | source | check | tier | repo |
|---|---|---|---|---|---|
| C1 | Text ≥ 4.5:1, large text ≥ 3:1 | SC 1.4.3; GOV.UK AAC *"at least 4.5:1"* | computed fg vs effective bg | D (M if declared pairs) | `_validate_snippets:256-258` (Route C) · `_validate_state_contrast` (`--render`) **scope✗ on a hand-off path** |
| C2 | UI components and graphical objects ≥ 3:1 | SC 1.4.11 | same | D | `_validate_snippets`, `_validate_dataviz` (**scope✗**) |
| C3 | Contrast holds in hover / pressed / focus / disabled, both modes | SC 1.4.3 + 1.4.11 across states | drive real states | D | `_validate_state_contrast` (playwright; else `77`) |
| C4 | Colour is never the only carrier | SC 1.4.1; GOV.UK AAC *"not depend on colour alone"*; bento meta `colourIsNeverAlone` | parse: RAG chip carries its word; trend carries `data-trend` | M | `_validate_dataviz` (**scope✗**) |
| C5 | The page survives user-forced colours / high contrast | GOV.UK AAC *"users change colours on websites"* | render under forced-colors emulation | D | — |
| C6 | Text ≥ 7:1 | SC 1.4.6 **AAA** | computed | D | — — **collides with ruled colour law; see UNPROVEN** |

### Band D — targets and pointer

| # | criterion | source | check | tier | repo |
|---|---|---|---|---|---|
| D1 | Controls ≥ 24×24 CSS px or an equivalent/spacing exception | SC 2.5.8 **AA** | measured from markup | M | `_validate_a11y` FAIL tier (`_a11y_target.py`) ✅ |
| D2 | Controls ≥ 44×44 (house default) | SC 2.5.5 **AAA** = HSBC default | same measurement, higher floor | M | `_validate_a11y` `CONTROL_TIER_44 = "warn"`; `s114-D6` ruled blocking, ordered ✅ |
| D3 | Data marks ≥ 24 floor with a table fallback | `s116-D1` | same | M | `_validate_a11y` `MARK_TIER = "warn"` ✅ |
| D4 | Nothing requires a drag | SC 2.5.7 **AA, new in 2.2** | parse drag handlers, require a single-pointer path | M (weak) / D | — |
| D5 | No activation on down-event | SC 2.5.2 | parse | M | `_validate_advisory` acd-016 **scope✗** |
| D6 | Visible label text is contained in the accessible name | SC 2.5.3 | parse `aria-label` vs visible text | M | `_validate_advisory` avd-006 suffix half only, **scope✗** |

### Band E — motion and user preference

| # | criterion | source | check | tier | repo |
|---|---|---|---|---|---|
| E1 | Anything that animates carries `prefers-reduced-motion: reduce` | SC 2.3.3; ADR-0015 | parse | M | `_validate_a11y` FAIL tier ✅ (runs on a supplied path) |
| E2 | Motion is CSS+token governed, not JS-driven | DEF-003 / `s116-D1` | parse for `.style.transform`, scale writes | M | `_validate_css_governed`, `_validate_behaviour` (**scope✗** — library sources only) |
| E3 | Nothing flashes or blinks | GOV.UK AAC *"not move (for example, flash or blink)"*; SC 2.3.1 | parse keyframes for rapid opacity/visibility cycles | M (weak) | — |

### Band F — resilience (the #233 band)

| # | criterion | source | check | tier | repo |
|---|---|---|---|---|---|
| F1 | With JS off and CSS on, the page still carries all content and the fallback surface | GOV.UK AAC; USWDS *"a robust HTML foundation and all the necessary content"*; `chart-line.meta.json:85` | render twice, JS on / JS off, diff the accessible content | D | — |
| F2 | Any component with declared behaviour actually ships its own `<script>` (not an authored substitute) | #233 symptom (a); APG Principle 1 | byte-compare the page's script block against the snippet's | M | — |
| F3 | With CSS off, JS on — and with both off — content order still reads | GOV.UK AAC (two further criteria) | render/parse | D / M | — |
| F4 | Reflow at 320 CSS px equivalent without two-axis scrolling | SC 1.4.10 | drive at width | D | — |
| F5 | Zoom to 400% and text enlargement | GOV.UK AAC *"users zoom to 400%"*; SC 1.4.4 | drive | D | — |
| F6 | Pinch-zoom never disabled | SC 1.4.10 | parse viewport meta | M | `_validate_advisory` acd-010 **scope✗** |
| F7 | Container-query surfaces answer their container, not the window | bento meta `reflow` (*"Proven by DRIVING"*) | drive at two wall widths | D | — |

### Band G — system fidelity (Apollo's own bar, standards-adjacent)

| # | criterion | source | check | tier | repo |
|---|---|---|---|---|---|
| G1 | No raw hex; no raw px for spacing/radius/border | DEF-004; USWDS *"Avoids hard-coded magic numbers"* | parse | M | `_validate_compose` check 4 ✅ (via `_validate_screen`) · `_validate_no_hardcode` **scope✗** |
| G2 | No local redefinition of a `.c-*`/`.cn-*` class | `generate-from-canon` rule 3; USWDS additive-modifier rule | parse | M | `_validate_compose` check 5 ✅ |
| G3 | Every class used resolves in `canon.css` | — | parse | M | `_validate_compose` check 6 ✅ |
| G4 | Type via composites only, never raw font values | DEF-006 | parse | M | `_validate_type_composites` **scope✗** |
| G5 | Icons are library glyphs or marked `data-bespoke` | `generate-from-canon` rule 8 | byte-match paths | M | `_validate_icons` ✅ (via `_validate_screen`) |
| G6 | No cross-theme colour leak | `s227`/ADR-0011 | parse | M | `_validate_theme_provenance`, `_validate_legacy_leak` **scope✗** |
| G7 | Sentence case; no ALL-CAPS outside acronyms | house rule, dyslexia rationale | parse | M | `_validate_snippets` check 4 · `_validate_advisory` A/D **scope✗** |
| G8 | The two-red law holds for the ground each red sits on | `s151-D1` | resolve each red against its computed background | M (declared) / D (real) | — |

### Band H — hand-off completeness (the "ready to wire" band)

| # | criterion | source | check | tier | repo |
|---|---|---|---|---|---|
| H1 | Every state the component defines is present or explicitly out of scope | `generate-from-canon` rule 10 | meta `props`/`variants` vs page census | M | — |
| H2 | A used/missing note lists components, tokens and Gaps | `generate-from-canon` § Output | file present and parses | M | — |
| H3 | The gate verdict is quoted **with its population** and any `77` named | `check-with-gates`: *"passed (0 tranche file(s))` is a gate that graded nothing"* | parse the verdict block | M | — |
| H4 | Provenance: which snippet and which tokens each part came from | `generate-from-canon` rule 12 | receipt present, ids resolve | M | — (rC's region) |
| H5 | Real content, not lorem, where the brief said real | `DESIGN-CONTRACT.md` Q5 | — | E | — |
| H6 | The composition reads as one page, not a wall of parts | — | — | E | — (rB's region) |

**Rubric tally.** 34 criteria: **20 MACHINE**, **11 DRIVE**, **3 EYE** (A8 partly, B6, H5, H6 —
counted as 3 with A8 assigned to DRIVE-weak). Covered on the hand-off path *today*: **9**
(A6 partial, C1–C3 only with `--render`, D1–D3, E1, G1–G3, G5). Covered by a gate whose glob
excludes the hand-off page: **12**. Covered by nothing at any scope: **13**.

## RULING-SHAPED QUESTIONS

⛔ Per the brief, **no option below is recommended**. Each is priced; Dave rules.

1. **What is the rubric's conformance target line?** (a) WCAG 2.2 AA only — cheapest, matches
   both GOV.UK and IBM baselines; (b) AA plus the three cheap AAA (2.4.10, 2.5.5, 2.4.13) —
   2.5.5 is already one flag flip behind `s114-D6`, so the marginal cost is one sequence decision
   plus a focus-geometry measurement; (c) AA plus 1.4.6 (7:1) — **collides with `s151-D1`** and
   is not costable until the two-red pairs are measured.

2. **Does Apollo adopt a THREE-tier verification vocabulary?** Carbon's AVT1 / AVT2 / AVT3 splits
   what Apollo currently calls "eye" into *driven-but-manual* and *screen-reader*. Apollo has no
   name and no instrument for the screen-reader tier at all. Option (a) keep two tiers and mark
   11 rubric lines EYE; option (b) adopt three and accept that AVT3 has no instrument, so the
   third tier is honest DECLARED-UNASKED rather than silent.

3. **`_validate_behaviour.py` — the name is taken.** The #233 proposal and the existing
   ADR-0015 gate are two different contracts on the same filename. Option (a) the new gate takes
   a different name and the ADR-0015 one keeps its; (b) the existing gate widens to take a path
   and gains the composed-page clauses; (c) the new work goes into `_validate_screen.py`'s chain
   instead of a new script. This is a naming/ownership ruling, not a technical one.

4. **The scope class: does the rubric bind to the ARTEFACT or to the FOLDER?** Every gate except
   `_validate_screen.py` is folder-bound. Option (a) widen each gate's glob one at a time;
   (b) give `_validate_screen.py` more chained checks so the one path-taking road carries the
   rubric; (c) require the agent to place its page inside a gated folder. Each has a different
   failure mode and none of them is mine to pick.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** whether the `s151-D1` two-red pairs clear 1.4.6's 7:1 on any ground. No contrast
  arithmetic was run in this lane. Price to prove: one script over the ruled pairs using
  `knowledge/_contrast_utils.py`, ~2K tokens, no render needed.
- **UNPROVEN:** Atlassian, Shopify Polaris and Material handoff conventions. Searched; the
  results were third-party blog write-ups, and the brief bars quoting marketing-grade sources.
  Nothing about those three systems is asserted here. Price to prove: three doc-page fetches at
  ~6–10K tokens each — Polaris and Material pages are large and mostly nav chrome.
- **UNPROVEN:** the rubric's coverage tally (9 / 12 / 13) is derived from reading gate docstrings
  and globs, **not** from running any gate — the brief forbids running them. A gate may check
  more than its docstring says. Price to prove: one `run-gates.py` sweep on a real composed page,
  plus reading three gate bodies in full, ~15K tokens.
- **UNPROVEN:** whether the criteria marked M-weak (A5, B2-static, B8, D4, E3, G8) can be made to
  fire without an unacceptable false-positive rate. Every one of them is the shape the brief
  warns about — checkable-sounding. Price to prove: a bite-test population per check, one
  session's lane.
- **CLAIMED:** the pack travel list and the "36 gates that run away from Apollo's repo" figure
  come from `check-with-gates/SKILL.md:8` and the **v1.0.3** manifest at
  `_to_delete/bake225/`, not from the v1.0.5 pack Dave cold-tested (its proving zip is recorded
  as VANISHED in memory). Re-read costs a pack regeneration, not a file read.
- **CLAIMED:** `chart-line.meta.json:85` as the home of the JS-off fallback line, and
  `Dropdown.reference.html:178` as the snippet's script — both are quoted from the #233 brief,
  not re-read from those files at this seat. Re-read costs ~1K tokens.

## Evidence

No evidence files: every claim above quotes its probe inline — a repo path with a line number, or
a URL with the quoted sentence. The two large web fetches (WCAG 2.2 TR, WCAG 2.2 AAA quickref)
were held in session tool-result scratch and grepped there; they are public documents at stable
URLs, so nothing was copied into `assets/`.

## WHAT APPLIES TO A FACTORY

A factory generates pages, so its bar has to be a property of the *output*, not of the library.
Apollo's instruments are excellent and almost all of them are pointed at the library: the
snippets, the pro-forma tranche, the fitness-test screens. The one road that accepts an arbitrary
path runs three checks. That is the difference between a design system that grades itself and a
factory that grades what it ships.

Three things the mature systems do that a factory can copy. First, they write the criteria down
as *acceptance criteria on the artefact*, in the same repo, in prose a tester can hold — GOV.UK's
list is a page of plain sentences, not a schema. Second, they name the tier honestly: Carbon says
out loud which stage is automated and which is a human with a keyboard, so a green never implies
more than it measured. Third, they make resilience a criterion rather than a virtue — "JavaScript
fails to load, but stylesheets load" is a line on a checklist at both GOV.UK and USWDS, and it is
the exact failure the #233 cold test found.

The factory-specific twist: a page generated by an agent has no author to interview afterwards.
Everything a reviewer would have asked the designer has to arrive with the artefact — the states
covered, the gaps declared, the gate verdict with its population, the provenance of every part.
That is why Band H exists and why it is the band with no coverage at all.

REPLAY-THESE: `notes/_subreports/2026-09-02-234-rA-standards-bar.md` § THE CANDIDATE RUBRIC (~4,800 tk) · `knowledge/_validate_advisory.py` docstring lines 1-70 (~1,400 tk) · `knowledge/_validate_behaviour.py` docstring lines 1-25 (~500 tk) · GOV.UK AAC page, resilience + interactive-element sections (~900 tk)
