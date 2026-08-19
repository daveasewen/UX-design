# Receipt — #203 Wave 3b, Lane I · navigation depth (Command palette · Sidebar nav · Anchor nav)

*Worker receipt against `_BRIEF-wave3b-verified-work-2026-08-19-v1.md` (which extends
`_BRIEF-wave3-foundations-2026-08-19-v1.md`), FABLE conductor, 2026-08-19.*
*⛔ Nothing here is a ruling. No commit, no push, no git mutation of any kind. `knowledge/_rulings.json`
untouched. No generator was run — not even `--check` (Lane G owns that surface this wave).*

**Gauge at close** — `_checkin.py`, real Claude tokens: FILL **145,808 real** · boot **56,488**
(inside the ruled band) · peak 145,808 over 30 turns · room to the advisory stop line (150,929)
**5,121**. Throughput 199,375 (`gauge.count`, one call — a different object, never summed with FILL).

---

## 1 · Headline

**All three rows verified genuinely absent, and all three were built.** Wave 3a found 18 of 18
briefed "gaps" already existed; rows 35 / 36 / 37 are the opposite case. Three new gated snippets,
three metas, three four-theme review pages. Every gate that reads my files is green.

The lane also produced **two cross-theme measurements that a mono-only gate cannot see**, one of
which changed a file before it shipped.

## 2 · Step 0 — the premise, verified first-hand, every probe named

| Claim inherited from the brief | Verified? | Probe run, and what it returned |
|---|---|---|
| HEAD is at #202 | ✅ TRUE — `ec2336d` | `git log --oneline -1` (read-only) |
| Row 35 **Command palette / global search** absent | ✅ **TRUE** | `ls knowledge/snippets/` (76 files, no match) · `ls knowledge/components/` (no match) · `grep -ril` over both dirs for `command palette` · `command-palette` · `commandpalette` · `cmd+k` · `palette` — the only `palette` hits are chart colour palettes (`Notifications`, `Chart-scatter`, `Chart-stacked-area`, `stepper.meta`) |
| Row 36 **Sidebar / nav rail** absent | ✅ **TRUE** | same `ls` ×2 · `grep -ril sidebar` → **one hit, `stat-card.meta.json`, unrelated prose** · `grep -ril` for `nav rail` · `navrail` · `nav-rail` → **zero** |
| Row 36 "may collide with gated Nav/Menu" (brief's own flag) | ⚠ **PARTIAL — see §3** | `Navigations.reference.html` read in full: **64 lines, one `<header>`, a horizontal masthead**. Its meta claims a family it does not render. |
| Row 37 **Anchor / scrollspy** absent as an ARTEFACT | ✅ **TRUE** | `grep -ril scrollspy` · `scroll-spy` → **zero** · `grep -ril "anchor nav"` → **two hits, both METAS** (`navigations.meta.json`, `_nodes-pattern.json`), **zero snippets** |
| Row 37 absent as a CLAIM | ❌ **FALSE — see §3** | `navigations.meta.json` declares a variant `anchors` ("brand-red underline indicator") and a pattern `in-page-anchor-nav`. The claim exists; the markup does not. |
| Itinerary row numbers/labels | ✅ TRUE, quoted | xlsx parsed directly: `B36 Command palette / global search · P2 · 2 Depth · "Power-user search"`; `B37 Sidebar / nav rail · P2 · "Desktop app frame nav"`; `B38 Anchor / scrollspy · P3 · "In-page section nav"` (sheet rows 36–38 = itinerary #35–37) |
| Type-composite debt is 1,101 | ⚠ **STALE** — measured **1,097** today, across 90 of 97 files | `_validate_type_composites.py`, rc=1. Same correction Lane D filed. |
| `_validate_snippets` red at HEAD (18 `--pri-hover` DRIFT, per Lane D) | ⚠ **NO LONGER TRUE in the working tree** — measured **rc=0, 0 failures** at my first run | ran before I wrote anything. The re-sync Lane D proposed appears to have landed in-tree. Declared because a carried figure is not a measurement. |

## 3 · The one collision the brief asked me to check, and what it actually is

The brief flagged that row 36 "may collide with gated Nav/Menu — check and say". It does, but not
where the brief expected, and the same seam catches row 37 harder:

- **`Navigations.reference.html` is 64 lines and renders exactly one thing: a horizontal web
  masthead.** Logo, four links, two icon buttons, one `aria-current` underline. That is all.
- **`navigations.meta.json` claims a four-member family** — `masthead`, `anchors`,
  `nav-bar-bottom`, `nav-bar-top` — with token bindings, audited Figma node ids and accessibility
  notes for all four. The artefact contains none of the last three. The meta's own `$finding`
  admits it: *"BASELINE flagged for review: a web masthead only."*
- ⇒ **Row 36 does not collide** with any built artefact: nothing in Apollo is a persistent vertical
  column, and nothing collapses. The masthead is page *chrome*; a sidebar is an application *frame*.
- ⇒ **Row 37 collides with a CLAIM, not a component.** The `anchors` variant has been described in
  a meta since 2026-06-20 and never built. `Anchor-nav.reference.html` makes it real and keeps the
  brand-red underline indicator the meta describes rather than inventing a new one.

**PROPOSED #203, Dave's eye owed** (component promotion is on the DO-NOT-RULE list, so both are
surfaced, not resolved):
1. Does **Sidebar nav** stand alone, or become a `type` of Navigations?
2. Should **`navigations.meta.json`** now point at Anchor-nav, or stop claiming a variant it does
   not render? *(I did not edit it — shared file, fenced.)*
3. Does the gated masthead's **`flyout="search"`** become a placement of **Command palette**?

This is a new instance of a known class: **a meta can claim a variant the artefact never had, and
nothing gates the gap.** Related to [[no-gate-parses-the-artefact]] — a coverage gate counts
meta-to-snippet *pairs*, so a meta that over-claims inside a pair it satisfies is invisible.

## 4 · Deliverables

| File | State |
|---|---|
| `knowledge/snippets/Command-palette.reference.html` | NEW — gated |
| `knowledge/snippets/Sidebar-nav.reference.html` | NEW — gated |
| `knowledge/snippets/Anchor-nav.reference.html` | NEW — gated, real scrollspy |
| `knowledge/components/command-palette.meta.json` | NEW — schema-valid, 0 errors |
| `knowledge/components/sidebar-nav.meta.json` | NEW — schema-valid, 0 errors |
| `knowledge/components/anchor-nav.meta.json` | NEW — schema-valid, 0 errors |
| `reviews/REVIEW-203-command-palette-four-themes-v1.html` | NEW — 8 panes |
| `reviews/REVIEW-203-sidebar-nav-four-themes-v1.html` | NEW — 8 panes |
| `reviews/REVIEW-203-anchor-nav-four-themes-v1.html` | NEW — 8 panes |
| `notes/_receipts/2026-08-19-203-wave3b-laneI-navigation-depth.md` | NEW — this file |

**Nothing else in the repo was written or modified.** No shared file, no token, no generator output,
no `MIGRATED_SNIPPETS` entry, no `CATEGORIES` entry (proposals in §8).

Every review pane is the **real gated snippet markup**, extracted by the builder with a fail-loud
content assertion (`must_contain` per file — the build raises `BUILD FAIL` if the literals move) and
rendered through the real generated `canon.css`. Never re-drawn, never hand-copied
([[specimen-starts-from-reference]]; #202's three hand-rolled pages are why). Builder at
`/var/tmp/s203i/build.py`, outside the repo, per the #174 precedent — not an instrument the repo
carries.

## 5 · Gates — every rc, every gap declared

Baseline measured **before** anything was written. ⚠ Exit codes captured directly, never through a
pipe (#174's void first reading).

| Gate | Baseline at open | After | Verdict |
|---|---|---|---|
| `_validate_snippets.py` | rc=0 · 76 snippets, 0 fail | **rc=0 · 85, 0 fail** | ✅ (other lanes added 6 more) |
| `_validate_a11y.py` | rc=0 · 76, 0 fail | **rc=0 · 85, 0 fail** | ✅ my three add 0 failures |
| `_validate_icons.py` (filtered, ×3) | — | **rc=0 · 0 UNKNOWN, 0 bespoke** | ✅ every glyph byte-matches the library |
| `_validate_type_composites.py` (filtered, ×3) | 1,097 across 90/97 | **PASS, 3 files, 0 violations** | ✅ **my three contribute 0** |
| `_validate_coverage.py` | 76/76 | **rc=0 · 85 meta / 85 snippet, 0 fail** | ✅ |
| `_validate_radius.py` | — | **rc=0 · 0 strict fail** | ✅ |
| `meta.schema.json` (jsonschema Draft7) | — | **0 errors × 3** | ✅ |
| `_validate_state_contrast.py` | — | **NOT RUN** | ⛔ declared — see below |
| every generator, incl. `--check` | — | **NOT RUN, deliberately** | ⛔ Lane G owns the surface this wave |

⚠ **Side effect declared, as the addendum permits:** the filtered gate runs rewrote
`knowledge/_SNIPPET-AUDIT.md`, `_A11Y-AUDIT.md`, `_ICON-SOURCE-AUDIT.md`, `_RADIUS-GATE.md`,
`_COVERAGE-AUDIT.md`. Those are generated audit artefacts, not hand-authored state.

⛔ **`_validate_state_contrast.py` NOT RUN, and I tried to cross the fence before saying so.** Lane D
already grepped it: line 1317 is an unconditional write of the shared `_STATE-CONTRAST-AUDIT.md`
with no suppression flag. I did not re-prove that; I inherited it and say so. Owed to the conductor
or CI. [[instrument-without-a-consumer]].

⛔ **`_build_all.py` NOT run.** ⛔ **`MIGRATED_SNIPPETS` NOT edited** — so `_validate_radius.py`
treats my three as advisory, not strict-from-birth. #174 added its entry; this wave's fence forbids
it. **PROPOSED for the conductor:** add `Command-palette` / `Sidebar-nav` / `Anchor-nav` to
`_validate_radius.py::MIGRATED_SNIPPETS` at reconcile. All three are radius-0-by-token already, so
the promotion should be free.

## 6 · The two findings a mono-only gate cannot see

Measured against the **real generated `canon.css`**, resolving `[data-apollo-theme]` overrides and
`var()` chains — the four-theme legs the snippet gate is blind to (it reads
`tokens/semantic-colour.json`, the mono base only, and says so).

### 6·1 — A four-theme measurement changed a file before it shipped

`Command-palette`'s first draft bound the query field's `focus-within` bottom stroke to
`form/border/default`. **The snippet gate passed it: 3.95:1 light / 4.17:1 dark.** Against
`canon.css`:

| `form/border/default` on the raised surface | mono | legacy | console | supercharge |
|---|---|---|---|---|
| light | 3.95 | 3.95 | 3.95 | 8.22 |
| **dark** | 4.17 | 4.17 | 4.17 | **1.69 ❌** |

`#524842` on `#2A2621` — under the 3:1 non-text floor, on **the field's only visible focus
affordance**. Rebound to `form/border/active` (ink: 21.00 / 19.44 light, 16.48 / 13.91 dark — passes
in all eight legs). The gate would never have caught it.

⇒ **`#524842` is the same value #203 Lane D measured at 1.96:1** as the Supercharge-dark elevation
hairline. One theme-level seam, found twice, from two directions, by two lanes that did not talk.
Corroboration, not duplication.

### 6·2 — The brand-red "you are here" bar fails 3:1 in Supercharge dark

Both nav components mark current location with `primary/border/default` (`#DB0011`), copied from
`Navigations.reference.html:27` — the one gated navigation artefact. Measured:

| `#DB0011` on… | mono | legacy | console | supercharge |
|---|---|---|---|---|
| raised surface, light | 5.22 | 5.22 | 5.22 | 4.84 |
| raised surface, **dark** | 3.16 | 3.16 | 3.16 | **2.88 ❌** |
| hover surface (a current row), light | 4.58 | 4.58 | 4.58 | 3.89 |
| hover surface, **dark** | 3.01 | 3.01 | 3.01 | **2.73 ❌** |
| page, dark (the horizontal bar's ground) | 3.33 | 3.33 | 3.33 | 3.33 ✅ |

**Not declared as a gated `contrastPair`** — it would be a green that cannot fail in the one theme
where it is false (the #174 precedent, verbatim shape). Both components therefore carry current
location on **three** carriers, of which colour is third: `aria-current` for AT, a bar whose
**presence or absence is a shape difference**, and a surface change. Dave is astigmatic and red is a
problem hue [[colour-stability-red-yellow-problem]] — this was designed for that from the start, and
the measurement then justified it rather than the other way round.

**PROPOSED #203, Dave's:** Supercharge dark needs its own current-location value, or the pattern
needs a non-red mark in that theme. Note the three passing themes clear 3:1 by 0.01–0.16 — this is a
thin seam everywhere, not only in Supercharge.

### 6·3 — A pair the gate refused, correctly

`Anchor-nav`'s first draft declared `divider/border/section` on the page as a 3:1 pair. **The
snippet gate failed the file at 1.31:1** (`#E1E1E1` on `#FFFFFF`). Not a defect: a section divider
between blocks of prose is decorative, not a boundary you must perceive to operate the component
(1.4.11 governs meaning-bearing boundaries). The declaration was removed and the reasoning written
into the manifest — because afterwards, an *undeclared* pair and an *unmeasured* one look identical
[[unrun-search-is-not-an-absence]].

## 7 · Render proof — driven, not asserted

`goto("file://…")`, **never `set_content()`**. Fonts installed per `_RUNBOOK-render-verify.md` §5
(both alias `<match>` blocks) — the first shoot measured **301 / 301 / 375 / 301** (target / alias /
DejaVu / nonexistent) = a **silent fallback**; after `fc-cache` it measures **347 / 347 / 375 / 301**
⇒ the real HSBC cut, both aliases landing on it, neither falling back. Canvas measurement against
two controls, not `fonts.check()`. Rendered at **1180 and 480**. PNGs were **read**, not merely
produced — Sidebar-nav mono-light, Command-palette supercharge-dark, Anchor-nav mono-light.

Measured in the DOM across all 8 panes per page:

- **Hit areas: 0 of 240 interactive targets under 44px** (48 palette + 128 sidebar + 64 anchor).
  Enforced by hand — no gate reads `target/min`, which is Lane L's job this wave.
- **`aria-current` count: 16 per nav page** = exactly 2 per pane, 8 panes. Never two on one nav.
- **The four themes are really arriving.** Supercharge dark panel resolves `rgb(42,38,33)` vs mono
  dark `rgb(31,31,31)`; Supercharge light page `rgb(247,246,244)`. **Console renders
  `border-radius: 20px`** on the palette surface — that is **`s199-D3`, Dave's own ruling**, arriving
  correctly through `canon.css` from a file that declares `border-radius/surface`. Checked the store
  before calling it a drift [[retrieval-default-hides-the-ruling]]; Lane D was caught by the same
  thing and I inherited the correction rather than re-discovering it.
- Two layout defects were caught **by eye, not by any gate**, and fixed: the palette's result list
  clipped an option mid-row (stage 400→460px) and the sidebar clipped its last group (frame
  440→540px). A third was caught by the type gate's own deciding rule — a *wrapping* sentence in the
  empty state carried `.t-cm-caption` (Component) and now carries `.t-ed-caption` (Editorial).

## 8 · Proposals for the conductor to merge (⛔ all shared files, none touched)

1. **`_validate_radius.py::MIGRATED_SNIPPETS`** += `Command-palette.reference.html`,
   `Sidebar-nav.reference.html`, `Anchor-nav.reference.html` — strict from birth, all three are
   radius-by-token already.
2. **`gen_showroom.py::CATEGORIES`** += `command-palette` → *Navigation*, `sidebar-nav` →
   *Navigation*, `anchor-nav` → *Navigation*. ⚠ Not blocking: `gen_showroom.py:483` is
   `CAT_OF.get(slug, "More")`, so an unlisted slug lands in **More** rather than vanishing (the #174
   correction). Cosmetic, but they belong with `navigations` / `breadcrumbs` / `tabs`.
3. **`knowledge/_DS-IMPROVEMENTS.md`**: Supercharge's `#524842` is simultaneously
   `form/border/default`, `elevation/border` and `divider/border/*`, and lands at 1.69–1.96:1 on
   every dark surface it is asked to separate. Two lanes measured it independently this session.
4. **`knowledge/_DS-IMPROVEMENTS.md`**: `primary/border/default` as a current-location indicator is
   under 3:1 in Supercharge dark and within 0.01 of the floor in the other three (§6·2).
5. **Carried-figure correction**: type-composite debt is **1,097**, not the 1,101 in the standing
   memory hook — same correction Lane D filed, measured independently here.
6. **Class finding for the itinerary/meta work (Lane H's neighbourhood):** a meta can claim a
   variant its artefact never had, and no gate sees it, because coverage counts *pairs*.
   `navigations.meta.json` has claimed `anchors` since 2026-06-20. A cheap candidate gate: assert
   every `variants[].name` is reachable in the rendered snippet.
7. **No token proposals.** I minted nothing and wished for nothing; every value resolved from the
   store.

## 9 · Decisions needed — Dave's, none of them mine

1. **Sidebar nav: stand alone, or a `type` of Navigations?** (component promotion)
2. **Should `navigations.meta.json` point at Anchor-nav**, or stop claiming an `anchors` variant it
   does not render?
3. **Does the masthead `flyout="search"` become a placement of Command palette**, or do the two get
   a stated reason to differ?
4. **Supercharge dark's current-location red** (§6·2) — accept, re-value, or use a non-red mark
   there.
5. **The palette's active-option ink vs the navs' brand red.** I split them deliberately: red = "you
   are here", ink = "the cursor is here". Never ruled.
6. **The keyboard chord.** The palette footer shows `Ctrl` `K`. Platform pairing (Ctrl / Command) and
   whether the product claims that chord at all are unruled.
7. **What an empty query shows** — recents, a default set, or nothing. Scoped out, not answered.
8. **Rail items need a visible name on hover.** Composing the gated Tooltip is the obvious answer; I
   did not build it, because inventing a composition rule is not a worker's call.
9. **The sub-desktop placement of Sidebar nav** — almost certainly the gated Drawer, but that is a
   placement ruling.
10. **`Anchor-nav`'s scrollspy tie-break** (first intersecting section in document order,
    `rootMargin -56px / -55%`) — a judgement call with no canon behind it.

## 10 · Residuals and friction — declared, not glossed

- **`_validate_state_contrast.py` unrun** (§5) — inherited Lane D's proof of why, did not re-prove.
- **`MIGRATED_SNIPPETS` / `CATEGORIES` unedited** — fenced; §8 items 1–2 are owed at reconcile.
- **No generator ran, so the showroom has no page for these three yet.** `gen_showroom.py --check`
  would report them missing — that is the fence working, and Lane G's regeneration will close it.
  ⚠ Declared rather than run: the addendum forbids even `--check` this wave.
- **The four-theme measurement is a CSS-text resolver, not a browser.** It parses `canon.css`
  `:root` / `[data-theme="dark"]` / `[data-apollo-theme=…]` blocks and dereferences `var()` chains.
  It **failed loud** on its first run (`PARSE FAIL — selector matched nothing`, a missing `re.M`)
  rather than returning empty tables — [[a-crash-is-not-a-fail]]. The *rendered* corroboration is
  independent: `getComputedStyle` across 24 panes agreed with the resolver on every surface value it
  reported.
- **The font farm was NOT present at session open** and the first shoot silently fell back to a
  stock face (301 = the nonexistent-face control). Caught by the two-control canvas measurement, not
  by `fonts.check()`. Anyone re-shooting in this sandbox must run `_RUNBOOK-render-verify.md` §5
  first.
- **`/var/tmp` farms re-used, not rebuilt** — `pw-browsers-s197`, `pylibs-s203e`, `chromelibs`.
  Disk healthy (`/` 72%, `/sessions` 16%); no ENOSPC, n=0.
- **Six PNGs written to `outputs/s203i/`** (outside the repo, the only path both the sandbox and the
  file tools can reach). Nothing was written to `/var/tmp` that the repo carries.
- **Nothing was deleted, moved, or git-touched.** The only git command run in this lane was
  `git log --oneline -1`.

**Machinery price** — `0 instrument / ~1,050 feature`. No gate, checker or harness was built. The
three throwaway scripts (`/var/tmp/s203i/{measure,build,shoot,panes}.py`) live outside the repo and
are not instruments the repo carries. ⚠ The four-theme resolver in `measure.py` is a **candidate**
instrument — it does something no gate does — but promoting it is a scope call, not mine.
