# H1 — the library build-out, measured (#289, 2026-09-19)

*Every figure has a source line. REPO = what a file/commit says. INF = my reading.
Dave's framing: `notes/_lanes/289/DAVE-RULINGS-2026-09-19.md:96`.*

## 1 · The "~36 components" moment

- REPO — **32 real component metas** at `87a71e4f` (2026-06-18); 33 files, one is the
  `EXAMPLE-button` template. accordion · avatar · badge · breadcrumbs · button · cards ·
  countdown-timer · divider · dropdown · headers · hero · input-fields · links · list-items ·
  loading-indicator · modals · navigations · notifications · pagination · progress-tracker ·
  quick-actions · reorder · search-field · selection-controls · slider · status-indicator · table ·
  tabs · tags · tooltip · video-player · view-options.
  *`git ls-tree -r 87a71e4f --name-only knowledge/components`.*
- REPO — flat at 32 for **13 days** (2026-06-18 → 2026-07-01); no count change between `87a71e4f`
  and `52ba8578`.
- REPO — **38** at `52ba8578` (2026-07-01): +account-card, +5 gap-patterns (action-bar,
  confirmation, eyebrow, summary, tab-bar). *Tree diff of the two commits.*
- REPO — the repo's own label for that state: *"~38 — 32 reviewed + 5 gap-patterns + account-card"*.
  *`knowledge/_COMPONENT-LIBRARY-TARGET.md:13` (drafted 2026-07-01).*
- INF — "36" is not a literal repo figure. The two quotable numbers are **32 reviewed** and
  **38 total**. The story holds; the number does not.

## 2 · The growth curve (component metas, first commit at each new count)

| Date | Commit | Metas | Note (REPO) |
|---|---|--:|---|
| 2026-05-31 | `5a7772b0` | 1 | harness scaffold only |
| 2026-06-17 | `1fc1aab5` | 9 | first HSBC Figma ingest |
| 2026-06-18 | `87a71e4f` | 33 | the plateau — 32 real |
| 2026-07-01 | `52ba8578` | 39 | +gap-patterns → 38 real |
| 2026-07-20 | `8f3f07cb` | 41 | |
| 2026-07-22 | `16c8b84d` | 65 | build-out opens at pace |
| 2026-08-05 | `df44e510` | 76 | |
| 2026-08-19 | `973d3fa8` | 92 | wave 3 |
| 2026-08-20 | `4e50090c` | 136 | +44 in one day |
| 2026-09-09 | `108493b6` | 138 | HEAD count |

*`git log --reverse -- knowledge/components` + `git ls-tree -r <h> | grep -c meta.json`.*
- REPO — today: **138 metas / 137 components / 137 reference snippets**; `showroom/index.json`
  `$component_count: 137`, `$count: 145`, `$foundation_count: 8`.
- INF — 32 → 137 is **4.3×**; ~60% of the total landed 2026-08-19 → 08-31.

## 3 · "Initial results were underwhelming" — what was measured

- REPO 2026-06-19 — first fitness test (Tabs, KB-only vs unconstrained): KB-only measured
  **1.0:1 dark-mode contrast** (WCAG 1.4.3 + 1.4.11 fail), **no focus indicator defined**; verdict
  line: *"in Route B it is ~90% my invention."* *`knowledge/_FITNESS-TEST-tabs.md`.*
- REPO 2026-06-30 — SME-Payments portfolio run: three gaps where *"the canon was silent in exactly
  the places it had to invent"* — invented charcoals (`#0E1014…`), invented waterfall/runway bars
  (no chart components existed), re-invented easings. *`knowledge/_COMPONENT-GAPS.md:13-19`.*
- REPO 2026-07-05 — Dave's verdict: both governed expressive bands (Sonnet, Opus) *"still
  underwhelming"* vs the ungoverned portfolio piece, which itself needed a manual restyle fixing a
  theme-alias trap, **3 invented icons, 4 real WCAG contrast failures**.
  *`_DECISION-HISTORY/2026-07-05-register-spread-and-restyle.md:83`.*
- REPO 2026-07-07 — the hardest number: governed lineages **provenance-perfect and still flat**
  (governed-Opus: PURE-RETRIEVAL ×4, 0 invented colours, 26 canon components, 0 invented vars) vs
  the unconstrained diagnostic at **56 invented hexes, 1 canon component, 219 invented local vars**
  — which read better. 35% of all entities invented, all in the diagnostic lineage.
  *`knowledge/_FINDINGS-s9-session-2026-07-07.md` F3; data `knowledge/_KNOWLEDGE-USAGE-ENTITIES.json`.*
- REPO — root cause, same day: *"the invention rule is 'retrieve/derive from what exists', but the
  library stops at organism — 38 components, zero templates/shells… Thin library at the composition
  tier ⇒ underwhelming layouts, by rule."* (38 = 9 atoms · 23 molecules · 6 organisms · 0 templates.)
  *Same file, `:14-18`, `:91`.*
- INF — this is the measured form of "it can't be automated without the inventory": rule-adherence
  was already saturated, so inventory was the only lever left.

## 4 · Re-creating / inventing where the gaps were

- REPO — engine-side, measured: **13 of 40 snippets carried a local button recipe; 7 copied
  Button's scale-press; 4 pressed with `translateY` (drifted physics)**; Selection-controls carried
  both in one file. *"Copies drift — that is the whole case, observed."*
  *`_DECISION-HISTORY/2026-07-21-composition-architecture-call.md` §2.*
- REPO — human-designer side, in HSBC's own Figma library: the ruled source of truth is the
  designers' **"Gaps and edits" branch `Cgbtrmfp15ruNFkIAClpkI`** (2026-07-03, "prior use was ad
  hoc"); logged deltas include **td-009, two exact-duplicate Standard Tag frames** and **td-014, a
  page flagging its own divergence**. *`knowledge/_COMMON-TOOLKIT-SURVEY.md:5, :108, :120`.*
- REPO — the rationale, stated: *"when a part is missing, the model invents (the cold-B run
  fabricated account numbers + status chips to fill a table it needed)… Coverage removes the reason
  to invent."* *`knowledge/_COMPONENT-LIBRARY-TARGET.md:23`; same run at
  `knowledge/_TEST-BRIEF-v2-sme-payments.md:150`.*
- REPO — then planned, not drifted: 2026-07-21 ground truth *"40 gated canon components · itinerary
  124 rows · ~50+ gaps"*, housekeeping-then-fan-out. *`_BUILDOUT-STRATEGY-2026-07-21.md`.*
- REPO — closed out 2026-08-25: **124 itinerary rows → GATED 121, GAP 1**; the frozen hand-typed
  column understates the store on 84 of 124 rows.
  *`reviews/ITINERARY-STATUS-2026-08-25-v4.json` (`$counts`, `$drift_counts`).*

## 5 · Not established (looked, did not find)

- **A literal "36"** as a component count anywhere in the repo — see §1.
- **A dated one-shot / cold-run scorecard with a score or grade.** cold-A/cold-B is referenced
  (`_COMPONENT-LIBRARY-TARGET.md:23`, `knowledge/guidelines/accessibility-content-authoring.md:28`)
  but no scored card survives.
- **`_REVIEW-B3-grades-2026-08-15-v1.html` is NOT library evidence** — it grades 122 *memory hooks*
  (FRESH 12 · AGING 1 · STALE 0 · UNPROVABLE 109). Do not cite it in this strand.
- **A gate fail-count time series** across the build-out — gates exist per artefact
  (`knowledge/_*-GATE.md`), no dated pass/fail trend found.
- **A person-level record** of a named designer re-creating a named component; evidence is
  library-level only.
- **A before/after re-measure of the same brief at 32 vs 137 components** — the §9 experiment chain
  was parked ("we pivoted to the factory"), so the payoff is argued, not measured.
  *`_DECISION-HISTORY/2026-07-07-s9-root-cause-and-ruling.md` header.*
