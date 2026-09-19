# #288 lane P — the composition probe: what Apollo produces when it CANNOT trace

`COUNTS: decisions 39 · gaps 10 · findings 6 · UNPROVEN 2`

**Sheet:** `notes/_lanes/288/P/probe-sheet.html`
**Artefact:** `notes/_lanes/288/P/composed-dashboard.html`
**Decisions:** `notes/_lanes/288/P/DECISIONS.md`
**Reads receipt:** `notes/_lanes/288/P/READS.log`
**Renders:** `notes/_lanes/288/P/render/` (composed-1440-mono.png, traced-1440.png, two measured JSONs)

---

## Why this lane exists

Dave, verbatim, today, on seeing the dashboard-bento template:

> "there is a definitely a problem here, 2 actually, the template is a bit wonky and it's
> basically copied by the AI, what is the point of building the KG if the agent just traces
> an existing file, its very safe but 1. its of average quality anyway... its okay but not
> great 2. what was the point of building the system if it just traces from existing
> examples??? the results with VS co-pilot are pretty much identical to this, this isn't
> Apollo its a dot-to-dot book"

The probe answers one question: what does a one-shot produce when the template is
unreachable and it must compose from the design system's atoms and the graph's rules?

---

## 1. The prompt, and where it came from

**The frozen demo prompt could not be recovered.** Searched, in order:
`python3 knowledge/_memento_search.py "cold-start acceptance W-304"` (and `--all`), which
returned `notes/_briefs/2026-08-31-229-cold-start-acceptance-brief.md`; that brief, the
#230 demo-day brief and the #258 demo-fence brief; a repo-wide grep for
`"Chief AI Officer"`, `"AI programmes in flight"` and `"operations dashboard for a bank"`.
Every brief DESCRIBES the test — #229 § "The test, sketched": *"Cold seat: fresh session,
v1.0.4 pack only. Prompt: a dashboard ask phrased the way a designer would ask it — NOT
phrased to steer toward the contract"* — and none of them carries the prompt's text.

So the lane brief's fallback was used, and this is said out loud on the sheet:

> "Build an operations dashboard for a bank's Chief AI Officer: AI programmes in flight,
> their spend against budget, efficiency gains realised, risk and compliance exceptions, and
> what needs a decision this week. Desktop first, 1440 wide."

⚠ **UNPROVEN-1:** the traced template was built at an earlier session against its OWN brief
(a business-banking account overview). **The two pages answer different briefs.** The
comparison is therefore about HOW each was made, not about which answers a shared ask
better. That limit is printed on the sheet.

## 2. The method

Acted as the one-shot builder `designer-skills-v1` describes, following
`README.md` and `generate-from-canon/SKILL.md`:

1. **Rules first.** Queried `knowledge/_rulings.json` (622 rulings; 80 matched
   dashboard/bento/hierarchy/mainSpacing/subSpacing/s219-D1/s217-D2/s248-D4) and read the
   full `says` of s219-D1, s217-D2, s217-D3, s248-D4, s249-D2/D3/D5, s247-D3/D4, s251-D1,
   s272-D1. Extracted the DP-01…29 principle statements from
   `reviews/DASHBOARD-PRINCIPLES-2026-09-05-v1.html` (tag-stripped regex; statements only).
   Ran `knowledge/_render/role_defaults_219.py --table` and read
   `knowledge/_render/_bento_edit_rails.json`.
2. **Theme mechanism read from canon, not assumed.** `canon.css` BASE block says apply
   `.canon` (+ optional `data-theme`) on the root; `gen_theme_cascade.py` says
   *"resolve(role, mode, theme): theme override wins; else base (Mono)"*;
   `tokens/themes/_themes.json` says *"Mono = base, no block emitted"*. So **Mono is the
   ABSENCE of `data-apollo-theme`**. The page carries `class="canon" data-theme="light"`
   and nothing else.
3. **Composed** from the component snippets, binding every visual value to a token, and
   wrote each decision down as it was taken with the rule it rests on.
4. **Rendered, measured, and let the measurements force further decisions** (§ H of
   DECISIONS.md — five of them).
5. **Gated**, then re-minted the provenance receipt and re-gated.

**The composed page uses 11 canon components** (`.cn-*` scopes, measured from the DOM):
`cn-button · cn-card-header-lockup · cn-chart-bar · cn-chart-line · cn-kpi-tile ·
cn-legend · cn-list-items · cn-page-header-lockup · cn-status-indicator · cn-table ·
cn-tags`. Charts are driven by `window.dvRender(fig, spec)` — the library owns the
arithmetic, the page owns the data.

## 3. Reads log summary

`notes/_lanes/288/P/READS.log`, 39 entries, in order, each with its reason.
**Fenced files read: none.**

| Directory | Reads |
|---|---|
| `knowledge/snippets/` | 12 |
| `knowledge/canon/` | 8 |
| `knowledge/tokens/` | 3 |
| `knowledge/_render/` | 3 |
| `notes/_briefs/` | 3 |
| `knowledge/` (root files: `_rulings.json`, `_memento_search.py`, gates) | 3 |
| `designer-skills-v1/` | 3 |
| `reviews/` | 1 |
| `_DECISION-HISTORY/` | 1 |
| `knowledge/_screen-gate/` (the gate's own output on my page, read back) | 1 |

## 4. Decisions count

**49 numbered entries** in `DECISIONS.md`: **39 design decisions**, each carrying the
ruling, DP principle or token it rests on (or marked "designer's call"), and **10 gaps**
the system could not supply. Five of the 39 were forced by the render, not by reading
(§ H), and one (C9) is marked SUPERSEDED by a later one, in place.

The rules that did the most work: **s219-D1** (mainSpacing 40 / subSpacing 4 for Mono, the
{1,2,4,16,24,40} stop set), **s217-D2/D3** (bento-of-bentos, 6 columns, radius on the
container, nesting is canon), **s249-D2** ("5 is even okay in this case" — the headline
row), **s249-D5** ("No ragged layouts"), **s251-D1** (the strip that anchor-links to the
needs-attention panel — built literally as he described it), **s247-D3/D4**, **DP-01, 02,
03, 04, 06, 07, 08, 10, 11, 14, 15, 16, 18, 19, 21, 22, 23, 24, 27, 28**.

## 5. Gate verdicts, verbatim

**`_validate_screen.py notes/_lanes/288/P/composed-dashboard.html`** — this gate takes a
path and did run on this page. Its written verdict, from
`knowledge/_screen-gate/composed-dashboard.md`:

```
- verdict: PASS ✅
- receipt: ✅ 0 region(s) re-hashed and matched
  UNPROVEN:retrievalSet — null (rC Q4, the retrieval-set membership marker, is OPEN and was
  not invented here); a ruled membership marker carried in the receipt would prove which
  retrieval set the page was built from
- compose: ✅
- composition: UNPROVEN: C9 bands
- icon-source: ✅ all paths library-matched
- a11y: ✅
```

(Its index step then refused: `⛔ SCREEN-GATE INDEX REFUSED — a generated index may not be
built from state a clone cannot see. untracked subject: _screen-gate/composed-dashboard.md`.)

**`_validate_composition.py notes/_lanes/288/P/composed-dashboard.html`**:

```
  UNPROVEN: the artefact declares neither a base column count nor any @container band; C9
  cannot read its grammar
  UNPROVEN: C9 bands
_validate_composition: UNPROVEN  (notes/_lanes/288/P/composed-dashboard.html) - C9 reds 0
[BLOCKING] · C1 0 · C7 0 · C8 0 · C4 0 [advisory] · unproven 1
```

**`_validate_compose.py <path>`** printed `RESULT: PASS ✅` — **but not about this page.**
It ignores the path argument and scans a fixed set of seven `*.canon.html` screens. Recorded
so the PASS is never read as evidence about the probe.

**`check-against-design-system` (the pack's own skill, guidance, applied by hand to its own
six-step procedure).** Its verdict, verbatim as this lane produced it:

```
0 blockers · 4 warnings · PASS — no invented components, no invented variants, no invented
tokens, no raw hex; four warnings, all of them gaps in the system rather than drift in the
page.
```

The four warnings, each with the specific fix the skill's output format demands:
1. *warning · hard-coded value* — `--bento-gutter:40px` / `4px` on the wall instance dials.
   Fix: none available — s219-D1(4) rules the stop set as literal px values and the store
   emits no bento-spacing token to bind to. **Kept literal, on the ruled stops.**
2. *warning · hard-coded value* — `.wall-evidence .dv-chart-area{max-height:216px}`,
   `--bento-row-unit`'s 320px rung answered by hand. Fix: a `layout/bento/row-unit` per-role
   dial would remove it; none exists (see G3).
3. *warning · invented-token risk* — `--page` rebound to `var(--tertiary-background-hover)`
   because the dashboard/mono role default says `pageBg=grey` and no semantic page-grey role
   exists. Fix: add a `background/secondary` (or `background/app-canvas`) role to the store
   (G1).
4. *warning · missing-state* — the composed page ships default/hover/focus/pressed for every
   control it uses (they come with the components) but no loading, error or empty state for
   the attention region, because no component defines that organism (G4).

**Gates that could NOT run on a standalone page outside the tree**, each because it
discovers its own corpus and takes no path: `_validate_dataviz.py`
(`knowledge/_proforma/*.html`), `_validate_binds_resolve.py` and the standalone
`_validate_a11y.py` (`knowledge/snippets/*.reference.html`). The a11y and icon-source checks
DID run on this page, inside `_validate_screen.py`.

## 6. The measured table (both pages, live DOM, 1440px wall, Mono light)

| Measure | A · traced | B · composed |
|---|---|---|
| Wall width × document height | 1440 × 1197 | 1440 × 2016 |
| `.c-bento` instances | 4 | 3 |
| Top-level tiles in the dashboard wall | 3 | 4 |
| Total `.c-bento__tile` | 10 | 12 |
| Computed outer gutter (column-gap / row-gap) | 40px / 40px | 40px / 40px |
| **Distinct canon components, by `.cn-*` class in the DOM** | **0** | **11** |
| Heading levels present | h1 ×1, h3 ×3 (no h2) | h1 ×1, h2 ×6 |
| `<svg>` | 17 | 16 |
| `<table>` | 0 | 3 |
| Theme carriers on the root | `data-theme="light"` + `data-apollo-theme="mono"` (inert — canon emits no mono block) | `class="canon"` + `data-theme="light"` |
| Custom properties referenced in the page's own source | 82 | 23 |
| …resolving to nothing **on the root element** | 73 of 82 | 3 of 23 (`--baseline`, `--data-axis`, `--data-grid`) |
| Uncaught page errors at load | 0 | 0 |

⚠ **UNPROVEN-2:** the "resolves to nothing on the root" row is a SCOPE MAP, not a defect
count. A property legitimately declared on a component (`--bento-gutter` on `.c-bento`,
`--data-grid` inside a chart scope) is empty at the root by design. It shows how much of
each page's vocabulary is component-scoped rather than page-scoped; it does not show broken
bindings, and it was not re-measured per element.

The traced page was rendered **by URL only** — `goto(file://…showroom/template-dashboard-bento.html)`,
screenshot, DOM counts. Its source was never opened, grepped or diffed.

## 7. Findings

**F1 — the single sharpest measured difference: the traced page uses ZERO canon component
scopes.** Not one `.cn-*` class in its DOM. Its markup and CSS are its own; it participates
in the bento grammar (4 `.c-bento`, correct 40px gutter) but in none of the component
library. The composed page uses 11. Whatever else the two pages are, they are built out of
different materials.

**F2 — the one ruled dashboard dial cannot be set the way canon documents it (G7).**
canon.css instructs: *"declare instance dials as `.c-bento.my-wall{…}`"* because the role
rules "are (0,2,0)". But the rule that restores the outer gutter for a bento-of-bentos is
`.c-bento[data-bento-role="dashboard"]:has(> .c-bento__grid > .c-bento)`, which `:has()`
lifts to (0,4,0). **MEASURED:** a bare `.c-bento.wall-ops{--bento-gutter:40px}` had no
effect and the wall rendered at the Mono base 0px — not s219-D1(5)'s mainSpacing of 40. The
dial only lands when it repeats the `:has()`. A builder following canon's own instruction
silently loses the ruled spacing.

**F3 — a nested bento cannot carry its own column count below 1100px (G8).**
`layout.json` says columns are *"per-instance overridable via `--bento-columns` — that is
how a nested bento carries its own parameter set"*, and s217-D2 makes nesting canon.
But the compiled bands re-declare `--bento-cols-now` **on the grid** at ≤1100 / ≤820 / ≤520,
and they answer the WALL, not the window. **MEASURED:** a 1-column inner wall 896px wide
rendered as 3 columns; the dominant tile's card came out 296px instead of 896px. On a
1440-wide dashboard every inner wall is under 1100 unless it spans all six columns — so the
per-instance column dial is only reachable for full-width inner walls, and the promise in
the token's own `$note` is not generally true.

**F4 — the 320px row unit fights DP-06 (G3).** `layout.bento.row-unit` is "MINTED s217-D2 —
shared" with no per-instance clause in its `$note` (unlike `columns`), and nested bentos
floor at `minmax(var(--bento-row-unit),auto)`. So the headline metric row cannot be made
compact, and DP-06's stated purpose — *"compact, so the first chart starts above the
fold"* — is unreachable at 1440 without an authoring act. Not overridden; flagged.

**F5 — DP-18 is enforced by nothing, and canon clips silently when it is broken.** The first
composition put the exceptions list beside two charts; the list (694px) stretched the row to
791px inside a wall canon fixes at 320px, and `.c-bento{overflow:hidden}` swallowed the
overflow without a symptom in the DOM or the console. The fix was DP-18's own prescription
(give the taller neighbour its own column span). Nothing in the tree would have caught it —
`_validate_composition.py` returned UNPROVEN on this page (F6) and the render showed a
clipped page with `pageErrors: []`.

**F6 — no gate in the tree reads the composition of a page that LINKS canon.css (G9).**
`_validate_composition.py` reads *"column counts and band clamps from its own @container
blocks"* — the artefact must restate the grammar inline. The orphan-cell arithmetic that
DP-16 and s249-D5 ("No ragged layouts") rest on therefore cannot be checked on a linked
page at all. Every composed screen in the tree is self-contained; this is the first one that
links canon, and it fell straight through.

## 8. Gaps the system could not supply (the skill's own "Gaps" list)

G1 no semantic page-grey token for the ruled `pageBg=grey` · G2 no polarity carrier on
Kpi-tile (`data-trend` is arithmetic; DP-22 wants meaning; DP-25's `data-signal` is an OPEN
question) · G3 the 320px rung vs DP-06 · G4 no "needs attention" organism (DP-10) · G5 no
dashboard shell · G6 no attention-strip component (s251-D1 calls the strip "a good pattern")
· G7 the under-specified instance-dial recipe · G8 the nested-bento column dial · G9 no
composition gate for a linked page · G10 `_validate_compose.py` ignores its path argument.

## 9. Anything fenced I touched

**None.** `knowledge/snippets/Template-dashboard-bento.reference.html`,
`showroom/template-dashboard-bento.html`,
`knowledge/components/template-dashboard-bento.meta.json` and every prior dashboard artefact
were never opened, read, grepped, `grep -l`'d or diffed. `showroom/template-dashboard-bento.html`
was rendered by URL and measured through the DOM only. All `Template-*.reference.html`
snippets were avoided as a class, not just the bento one.

**Two repo writes outside my lane directory, both by gates I ran, both declared:**
- `knowledge/_COMPOSE-AUDIT.md` was rewritten by `_validate_compose.py`. **Restored to HEAD**
  (`git show HEAD:… > …`); `git status` is clean for it. Its only diff was `defs 1019 →
  1021`, which reflects another lane's canon.css changes, not mine.
- `knowledge/_screen-gate/composed-dashboard.md` was **created** by `_validate_screen.py`
  and I **could not remove it** — `rm` returns `Operation not permitted` at this seat. It is
  untracked (`?? knowledge/_screen-gate/composed-dashboard.md`) and is the gate's verdict on
  my page, quoted in § 5. **The conductor should delete it, or the lane's artefact should be
  moved before the gate is re-run.** No commits, no stashes, no other git writes.

## 10. What could not be established

1. **The frozen demo prompt's text.** Not recoverable from memento, the four briefs or a
   repo-wide grep. The fallback was used and is named on the sheet and in § 1.
2. **A same-brief comparison.** The two pages answer different asks (§ 1, UNPROVEN-1).
3. **Whether the composed page's wall is orphan-free by the graph's own arithmetic.**
   `_validate_composition.py` returned UNPROVEN (F6). The layout was reasoned to DP-16 and
   s249-D5 by hand and the render agrees by eye, but no machine confirmed it.
4. **The traced page's component provenance beyond class names.** Measuring it further would
   have meant reading it.
5. **Dark mode, and the other three themes.** Rendered in Mono light only, as briefed.
6. **Responsive bands.** Rendered at 1440 only. G8 was measured at 1440; the 820/520 bands
   were not exercised.
7. **The render seat.** `outputs/_render-env-229` does not exist at this seat (no
   `pw-browsers`, no `pylibs`), so `seat_env.sh` could not be sourced. Its logic was
   reproduced by hand: playwright installed via pip, Chrome for Testing 153.0.8010.12
   fetched by curl (playwright's own downloader failed TLS —
   `UNABLE_TO_GET_ISSUER_CERT_LOCALLY`), one missing lib (`libXdamage.so.1`) extracted from
   a deb, the fonts.conf + font farm generated per-seat (10/10 HSBC faces resolving, 404
   total). **`seat_env.sh` was NOT edited**; the line-44 glob was symlinked around
   (`chrome-headless-shell` → `headless_shell` inside
   `~/.cache/ms-playwright/chromium_headless_shell-1243/chrome-linux/`).
