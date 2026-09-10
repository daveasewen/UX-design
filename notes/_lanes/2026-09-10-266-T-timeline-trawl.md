# #266 lane T — evolution timeline trawl (read-only)

```
provenance: 266 · 2026-09-10
status: observed
scope: research only — no repo file other than this one was written
```

Purpose: source material for Dave's 15–20 minute demo to **David Rice, HSBC Chief AI
Officer**. Everything below is drawn from the repo's own record and cited to a path.
Where a claim could not be sourced, it is marked NOT FOUND rather than filled in.

---

## 1. Sources inventoried — 24 primary, plus the ledgers

### Presentation-shaped (the three that already exist)

| Path | What it is |
|---|---|
| `reviews/PRESENTATION-2026-07-14-apollo-sponsor.html` | 12-slide sponsor briefing, July 2026. The original Apollo pitch: tension → idea → four parts → what's real → four modes → the ask. |
| `reviews/PRESENTATION-2026-07-14-apollo-sponsor.pptx` | Same deck, PowerPoint export. Also copied to repo root as `Apollo-sponsor-briefing.pptx`. |
| `reviews/PRESENTATION-2026-08-12-designer-community-v1.html` / `-v2.html` | 14-slide designer-community talk, Aug 2026. Adds Memento as a co-equal product; ends on "try the four-skill pack". v2 is the later cut. |
| `notes/_receipts/2026-08-12-tender-stoic-clarke-designer-community-deck.md` | Build receipt for that deck — records what was flagged as forward-leaning. |
| `notes/_DEMO-PREP-david-rice-hsbc.html` | The audience dossier for this demo. Who Rice is, what he is measured on, what to lead with and what to avoid. |
| `digital-experience-transformation/strategy/05_narrative-and-deck-outline.md` | A narrative spine for the org-change story (Delivery → Experience). |

### Vision / strategy documents

| Path | What it is |
|---|---|
| `notes/_VISION-contextual-dashboard_2026-06-29.md` | Horizon-3 note: the engine as a generic "trust layer for assembled UI"; run-time contextual dashboard as the second vehicle. Directly relevant to a bank exec. |
| `notes/_VISION-northstar-front-end_2026-07-02.html` | North-star front end. |
| `notes/_VISION-iteration-machine_2026-07-03.html` | The iteration-machine framing. |
| `README.md` | The current one-page definition of Apollo: canon / criteria / gates / runbooks. |
| `digital-experience-transformation/strategy/01_transformation-thesis.md` … `04_people-transition.md` | Four-part operating-model thesis: artifact factory → governed system, roles, phased roadmap, people transition. |
| `docs/decisions/ADR-0001` … `ADR-0017` | 17 architecture decision records — the load-bearing turns of the project. |
| `docs/research-dossier.md` | External research backing. |

### The record itself (ledgers, not documents)

| Path | Count / what it is |
|---|---|
| `_DECISION-HISTORY/` | **217 dated session dossiers** (65 in July, 120 in August, 32 in September) — one per working session, each the WHY behind that day. |
| `knowledge/_rulings.json` | **441 rulings**, dated 2026-07-28 → 2026-09-09 (6 in July, 294 in August, 141 in September). Rendered for reading at `notes/_RULINGS.html`. |
| `knowledge/_decision-graph.json` | **102 nodes / 172 edges** — the temporal decision graph (ADR-0007). |
| `notes/_MEMENTO-DECISIONS.md` | 269 headed sections — the Memento (memory system) decision ledger. |
| `knowledge/components/*.meta.json` | **138 component criteria files.** |
| `knowledge/snippets/*.reference.html` | **137 gated reference components.** |
| `knowledge/_validate_*.py` + `_gate_*.py` | **56 gate scripts.** |
| `knowledge/_RUNBOOK-*.md` | **17 runbooks** — the method written down for a cold-start agent. |
| `apollo-spider/dist/` | **9 released zips**, v1.0.0 (26 Aug) → v1.0.9 (9 Sep). |
| git history | **1,245 commits**, 2026-05-31 → 2026-09-09. 1 in May, 53 in June, 467 in July, 526 in August, 198 in September. |

### Cold-run / one-shot evidence

`reviews/COLDRUN-258-2026-09-08-v1.html` … `-v5.html`, plus
`notes/_subreports/2026-09-08-258-C5-cold-run-5.md` and
`_DECISION-HISTORY/2026-09-08-258-five-cold-runs-and-the-sentence-2a-forbade.md`.
Baseline arm: `notes/_subreports/2026-09-05-246-B-baseline.md` and `-O-opus-baseline.md`,
surfaced at `reviews/BASELINE-246-2026-09-05-v1.html`.

---

## 2. The timeline — 22 milestones

### Act I — a component library, built properly (June)

**1. 2026-05-31 — the harness scaffold.**
First commit: *"feat: planning + harness scaffold for Promenaut design workflow"* (git).
A bespoke pipeline runtime. This is the approach the project later abandons — worth
telling because the abandonment is the good decision.
Source: `git log --reverse`; the design is preserved at `archive/harness-v0.1/`.

**2. 2026-06-17 — the first real HSBC material lands.**
*"feat: ingest first HSBC component + foundation tokens from Figma"* — then a re-base on
the Figma variable export the same day. The project starts from the bank's own canon, not
from a generic design system.
Source: git, 2026-06-17.

**3. 2026-06-18 — the inventory is taken, in one week.**
Component metas for Links, Input fields, List items, Loading indicator, Modals,
Navigations, Notifications, Pagination, Progress tracker, Quick actions, Reorder, Search
field, Selection controls, Slider, Status indicator, Table, Tabs, Tags, Tooltip, Video
player, View options — plus brand and platform guidelines from create.hsbc, and WCAG 2.2
AA alignment on every component.
Source: git, 2026-06-18 (8 commits).

**4. 2026-06-18 — the derived-views layer: the library starts checking itself.**
*"Add derived-views layer: xref, review queue, integrity gate, dark-mode audit, query
harness"* — and *"Add token blast-radius index + generated graph health report"*. This is
the first appearance of the idea that the library is a queryable knowledge base, not a
folder of files.
Source: git, 2026-06-18.

**5. 2026-06-19 — verification becomes enforcement.**
*"feat: contrast audits now gate the build"* — the moment a check acquires the power to
withhold "done". Followed by a dark-mode reconciliation sweep: *"24 flat tokens fixed, 7
inversions documented"*.
Source: git, 2026-06-19.

**6. 2026-06-22 → 06-29 — the 9/9 promotions.**
Components are promoted to gated canon one at a time against a rubric: Cards, List-items,
Status-indicator, Table (*"prototype-grade 6.5 → 9.0/9"*), Button, Progress-tracker,
Selection-controls, Modals, Input-fields, Links, Tags, Notifications. Also
*"Icons: migrate 52 hand-drawn SVGs → library glyphs / verified-bespoke (0 unverified)"*.
Source: git, 2026-06-22 to 2026-06-29.

### Act II — the pivot: it was never a pipeline, it was a brain (July)

**7. 2026-07-02 — the knowledge-engine pivot (ADR-0005).**
*"feat: ratify the knowledge-engine pivot (ADR-0005) — archive harness, rewrite identity"*.
The bespoke runtime is archived. The product becomes **the governed layer around any
generator**, operated by whatever host agent is to hand.
Source: `docs/decisions/ADR-0005-ratify-knowledge-engine-pivot.md`; git 2026-07-02.
> README: *"Generation is a commodity — this repo is the layer around any generator."*
> (`README.md`)

**8. 2026-07-02 — the gates get gated, and the engine is proved on a second design system.**
Two commits the same day: *"feat: gate the gates — bite-test suite + CI; fix self-satisfying
ARIA check"* and *"feat: GOV.UK second-system run — engine generalises (decision #4 closed)"*.
The engine is pointed at GOV.UK and still works — the portability claim earns evidence on
day one of the pivot.
Source: git, 2026-07-02; `second-system-govuk/`.

**9. 2026-07-05 — project memory is designed (ADR-0007).**
*"feat(pm): ADR-0007 temporal decision-graph + _LIVE-STATE cold-start spine"*, then the
same week *"docs(adr-0007): add anti-laundering guard — validity ≠ provenance"*. The
project starts keeping a record that can prove its own honesty.
Source: `docs/decisions/ADR-0007-project-memory-decision-graph.md`; git 2026-07-05.

**10. 2026-07-14 — the sponsor briefing.**
The first public articulation of Apollo, in 12 slides. Its four parts (canon, gates,
runbooks, host agent) are still the shape of the system today.
Source: `reviews/PRESENTATION-2026-07-14-apollo-sponsor.html`.
> *"the machine does the build, and the designer does the craft."*
> *"Verification = enforcement."* (README)

**11. 2026-07-21 — the decision graph is built and inscribed.**
*"Build-out strategy + ADR-0007 part 2"*, the edge convention (ADR-0012), and the seed at
`notes/_decision-graph-seed-2026-07-21.json`. Design decisions become nodes with edges,
so the reason for a value can be traced, not remembered.
Source: git 2026-07-21; `knowledge/_decision-graph.json`.

**12. 2026-07-26 → 07-30 — Memento is born, and hardened.**
Four days: Shape A built and the first dream pass run (07-26), the capture gate made
blocking (07-26), the M-set of twelve hardening rulings (07-27), the modular search spine
(07-28), and then *"TWENTY-TWO RULINGS IN ONE PASS"* (07-30). Memory becomes a second
product with its own ledger.
Source: `notes/_MEMENTO-DECISIONS.md` (269 sections); git 2026-07-26 to 07-30.
> Deck framing: *"An AI wakes up every morning with no memory of yesterday."*
> (`reviews/PRESENTATION-2026-08-12-designer-community-v2.html`)

**13. 2026-07-28 — the rulings store opens.**
First entries dated 2026-07-28 (`ds-023`) and 2026-07-30 (`ds-021`). Every decision Dave
makes is inscribed with an id, a date and his own words — from 6 entries in July to 441 by
2026-09-09.
Source: `knowledge/_rulings.json`.

### Act III — a product with releases (August)

**14. 2026-08-12 — the designer-community talk and the four-skill pack.**
Memento and Apollo presented as two products from one methodology, ending on an
invitation: `generate-from-canon`, `check-against-design-system`, `usability-review`,
`draft-a-new-pattern`.
Source: `reviews/PRESENTATION-2026-08-12-designer-community-v2.html`;
`notes/_receipts/2026-08-12-tender-stoic-clarke-designer-community-deck.md`.

**15. 2026-08-12 — the gate that could not run.**
*"AND THE FINDING IS A GATE THAT COULD NOT RUN — `_build_all.py` DIED BEFORE STEP 1"*.
A good story about a governed system: the machinery caught its own builder.
Source: git 2026-08-12 (#164 dossier in `_DECISION-HISTORY/`).

**16. 2026-08-19 — the machinery catches its own builder, twice.**
Session dossiers `2026-08-19-205-the-machinery-caught-its-own-builder.md` and
`2026-08-19-206-the-registry-caught-the-tree-and-repaired-nothing.md`. Also
`2026-08-19-203-the-premise-was-five-weeks-stale.md` — a stale premise found by a probe.
Source: `_DECISION-HISTORY/`.

**17. 2026-08-26 — v1.0.0: Apollo-Spider ships, carrying Memento-Gumdrop.**
*"#219 THE BAKE — Apollo - Spider v1.0.0 carrying Memento - Gumdrop v1.0.0"*, with a
**frozen ledger** recording the release as BORN and a birth clause added. From here a
release is a signed, hash-recorded artefact, not a folder copy.
Source: git 2026-08-26; `apollo-spider/dist/Apollo-Spider-v1.0.0.zip`.

**18. 2026-08-27 → 08-31 — v1.0.1, v1.0.2, v1.0.3, v1.0.4.**
Four releases in five days.
Source: `apollo-spider/dist/`.

### Act IV — one prompt, one dashboard (September)

**19. 2026-09-05 (#246) — the focus narrows to one sentence, and the BEFORE is measured.**
Dave at the opener: the demo is ~2 weeks out and the focus is one thing. Two lanes run the
frozen prompt cold — Fable and Opus, as two model families — and score the output on four
axes: **rich / full / persistent / interactive**. Baseline: **2 / 2 / 0 / 2**. Nothing is
fixed; the point is to know the starting number.
Source: `_DECISION-HISTORY/2026-09-05-246-the-library-dictates.md`;
`reviews/BASELINE-246-2026-09-05-v1.html`.
> Dave: *"the focus is getting the dashboards one-shotable."*
> (`notes/_briefs/2026-09-05-246-lane-P-dashboard-principles-brief.md`)

**20. 2026-09-08 (#257) — the audience is corrected, on Dave's word.**
The record had inferred the demo audience was "Sutherland". It is not — Sutherland is
HSBC's React component library, the binding target. The mis-inscription is left visible in
the dossier rather than quietly edited.
Source: `notes/_DEMO-PREP-david-rice-hsbc.html`;
`_DECISION-HISTORY/2026-09-05-246-the-library-dictates.md` § 2 (the correction, by addition).
> Dave: *"where do you get the idea that this has anything to do with Sutherland? The demo
> is to David Rice at HSBC"*

**21. 2026-09-08 (#258) — five cold runs in one day: 2/2/0/2 → 3/3/3/2.**
Five blind runs of the frozen prompt, each verified by driving the page in a browser, each
one finding and fixing a real defect. The series in full:
**#246 2/2/0/2 → v1 3/2/0/2 → v2 3/2/3/3 → v3 3/2/3/2 → v4 3/2/3/3 → v5 3/3/3/2**, at
which *"BOTH gates PASS for the first time in the series"*.
Source: `_DECISION-HISTORY/2026-09-08-258-five-cold-runs-and-the-sentence-2a-forbade.md`;
`reviews/COLDRUN-258-2026-09-08-v1.html` … `-v5.html`.

**22. 2026-09-08 → 09-09 — the chart engine, v1.0.8, v1.0.9, and the tenth release gate.**
The chart engine lands (#259): *"dv-render core + six type partials … six snippets
re-pointed to draw from DATA … driven green in 4 themes × light/dark"*. v1.0.8 releases
*"9/9 gates green"* (#260, 8 Sep); v1.0.9 releases the next day (#262). Then #263 rules
eleven proposed defaults and adds a **tenth release gate** — a release now refuses over
stale receipts.
Source: git 2026-09-08/09; `apollo-spider/dist/`; `_DECISION-HISTORY/2026-09-09-263-*.md`.

---

## 3. KPI and benefit claims — what exists, quoted exactly

### Counts that are real and checkable today

| Claim | Figure | Source |
|---|---|---|
| Gated reference components | **137** | `ls knowledge/snippets/*.reference.html` |
| Component criteria files | **138** | `ls knowledge/components/*.meta.json` |
| Rulings inscribed | **441** (2026-07-28 → 2026-09-09) | `knowledge/_rulings.json` |
| Decision graph | **102 nodes, 172 edges** | `knowledge/_decision-graph.json` |
| Gate scripts | **56** | `knowledge/_validate_*.py` + `_gate_*.py` |
| Runbooks | **17** | `knowledge/_RUNBOOK-*.md` |
| ADRs | **17** | `docs/decisions/` |
| Session dossiers | **217** | `_DECISION-HISTORY/` |
| Releases | **9 zips, v1.0.0 → v1.0.9**, 26 Aug → 9 Sep | `apollo-spider/dist/` |
| Commits | **1,245**, 31 May → 9 Sep | git |
| Release gates | **9/9 green at v1.0.8**; a **tenth** added at #263 | git 2026-09-08 / 09-09 |
| Ship-set gates at v1.0.8 | *"the dataviz gate is back in the ship set (45 gates)"* | git 2026-09-08 |
| Build steps | *"an 18-step build … a11y, contrast, token fidelity, icon provenance, coverage and integrity are blocking"* | `README.md` |

### The one-shot score — the only measured before/after in the repo

Four axes, 0–3 each: **rich / full / persistent / interactive**.

> *"2/2/0/2 → v1 3/2/0/2 → v2 3/2/3/3 → v3 3/2/3/2 → v4 3/2/3/3 → v5 3/3/3/2"*
> — `_DECISION-HISTORY/2026-09-08-258-five-cold-runs-and-the-sentence-2a-forbade.md`

Persistence moved **0 → 3** on the strength of two rulings (`s258-D1`/`s258-D2`) in a
single day. This is the cleanest quantified improvement the project owns, and it is
verified by driving the page, not by inspecting the source.

### Deck claims (older — check before reusing)

From `reviews/PRESENTATION-2026-07-14-apollo-sponsor.html` (July, now understated):
- *"38 reviewed components"* · *"2.2 AA WCAG build target"* · *"Light + dark, gated, both themes"*
- *"The repetitive build collapses from hours to moments."*

From `reviews/PRESENTATION-2026-08-12-designer-community-v2.html`:
- *"38+ reviewed components, each one gated before it entered."*
- *"Four themes in the registry, all derived from one baseline."*

The 38 figure is stale — the library is now 137 gated components. Update it.

### External / industry claims (sourced, but not ours)

From `digital-experience-transformation/strategy/`:
- *"around 91% of designers now use AI, three in four use it daily"* (`01_transformation-thesis.md`)
- *"teams ship 40–60% faster"* (`05_narrative-and-deck-outline.md`)
- *"Reported ~10x feature throughput once a library is structured this way."* (`docs/research-dossier.md`)

Roadmap horizons (`03_phased-roadmap.md`): Prove (now → ~3 months) · Encode (≈0–6 months) ·
Shift (≈6–12 months) · Scale (≈12–18 months).
> *"never restructure ahead of proven capability."*

### ⚠ Two things Dave asked for that are NOT in the repo

1. **The car-plant / gearbox metaphor.** A full-text search across `notes/`,
   `_DECISION-HISTORY/`, `reviews/`, `docs/`, `digital-experience-transformation/` and
   `README.md` for *gearbox*, *car plant*, *every car*, *assembly line*, *production line*,
   *factory floor* returns **no such passage**. The nearest recorded analogues are:
   - *"The old operating model is an **artifact factory**: briefs in, hand-made screens and
     specs out, with designer-hours as the bottleneck"* — `02_operating-model-and-roles.md`
   - *"The production line IS a workflow"* — `notes/2026-07-25-claude-code-orchestration-survey.md`
     (a pipeline mental model, still unruled per `notes/_briefs/2026-07-31-package-delta-audit-DRAFT.md`)
   - *"The machine assembles what is known. The designer is freed for what is new"* — July deck

   The metaphor is Dave's spoken one. It should be written down for the demo, not
   retrofitted into the record.

2. **A "6 months → N weeks" time-compression claim.** No such claim exists anywhere in the
   repo. Every "six months" hit is unrelated prose or a UI chip label. **Do not invent one.**
   The defensible time story is the observable one: the library was inventoried in a week
   (17–18 June), nine releases shipped in fifteen days (26 Aug – 9 Sep), and the one-shot
   score moved two axes in a single day (8 Sep).

---

## 4. The five stories for a bank operations executive

Ordered by how they land with Rice, whose prep note says he *"will judge Apollo as an
operator, not a designer"* and to *"Lead with throughput"*
(`notes/_DEMO-PREP-david-rice-hsbc.html`).

**1. One prompt, one dashboard — with a number attached (the headline).**
The frozen prompt, run cold, five times in a day, scored on four axes: 2/2/0/2 → 3/3/3/2.
This is exactly his metric shape — a process simplified, a colleague equipped, and a
measurement to prove it. It is also the only claim in the project with a verified
before-and-after. Show the run, not the slide.
Sources: `reviews/COLDRUN-258-2026-09-08-v5.html`;
`_DECISION-HISTORY/2026-09-08-258-five-cold-runs-and-the-sentence-2a-forbade.md`.

**2. The gates refuse, and they refuse the people who built them.**
The story is not "we have checks". It is `_build_all.py` dying before step 1 and being
caught (#164); the registry catching the tree (#206); a release refusing to cut over stale
receipts (#263, the tenth gate); a "green" that was a false green being struck (#255,
*"an abort is not a green"*). In his language: **auditability and controlled scale**, made
mechanical. The prep note says governance here is a selling point, not a caveat.
Sources: `_DECISION-HISTORY/2026-08-19-205…`, `2026-09-07-255-an-abort-is-not-a-green.md`,
git 2026-09-09 (s263-D13).

**3. Every decision has an id, a date and a name on it — 441 of them.**
For a bank, the differentiator is not that the AI produced a screen. It is that you can ask
*why is this button that colour* and get a ruling id, the date, and the words the human
used. 441 rulings, a 102-node decision graph, 217 dated dossiers, and a rendered page a
non-engineer can read (`notes/_RULINGS.html`). This is provenance as infrastructure, and it
is the thing freeform GenUI structurally cannot offer.

**4. It generalises — proved on GOV.UK on the day of the pivot.**
Within hours of archiving the bespoke runtime, the engine was pointed at a completely
different design system and still worked (`second-system-govuk/`, 2026-07-02). This
pre-empts his platform question: **model-agnostic engine plus a skills pack; it runs where
the designer's tools run**, and it is not welded to one component library. Frame the
Sutherland binding the way the prep note says he will hear it — *"does the output land in
the real codebase without rework."*

**5. The run-time vehicle — a personalised dashboard where entitlement is a gate.**
The June vision note already worked out the second vehicle, and it is a banking argument,
not a design one: assemble a per-user landing surface from certified cards, where
*"entitlement becomes a verification check on card eligibility, not a nice-to-have"* — you
can only ever see what you are entitled to, provably. Use this as the "where it goes" close
if the ask is a platform slot rather than sponsorship.
Source: `notes/_VISION-contextual-dashboard_2026-06-29.md`.

### Honourable mention — the recovery stories

If he probes on rigour rather than speed, the strongest material is the project's record of
catching itself: the premise that was five weeks stale (#203), the two lanes that wiped
each other (#253), the demo audience the record got wrong and corrected in Dave's own words
rather than quietly editing (#257). A system that files its own mistakes with a date on
them is the most bank-legible thing in the repo.

### What to avoid

Per the prep note, verbatim: *"design-system vocabulary as the headline, token/typography
detail up front, and anything that reads as a pilot. He was hired to move past pilots."*
