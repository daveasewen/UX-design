# #246 lane P brief — RESEARCH + DRAFT: dashboard composition principles (progressive reveal · density · execute-on-page · bento rhythm)

**Model: Fable. Conductor: Fable (#246). Dated period record (ADR-0017). Read-only against canon/knowledge — MOVES NOTHING in the library, RULES NOTHING. Output is a DRAFT for Dave's eye.**

## WHY (Dave, 2026-09-05, verbatim — these are the seeds, not the rules)

> "both chose the 2x2 lock-up for the stats a designer wouldn't do this, they would make it vertically dense by having them in a row, also filters would probably be dismissible for the same reason, then the designer simply decides on the default state. maybe we need guidance on progressive reveal strategies, there are many we should research the subject so we have principles and rules around this."
> "When I think of a dashboard I think of something more complex on an overview, with the options to execute on this page, I also think that a summary/feedback on actions tasks and statuses are always important."
> "the bento construction could be more interesting, this is too regular, a mixture of odd numbered and non-symmetrical layouts create rhythm in layouts, strict grids are boring as hell, this is why i love the display bentos so much, and mixing 6-4-3-2 three columns and making them irregular widths based on importance is another way of creating hierarchy."
> "the focus is getting the dashboards one-shotable."

Baseline evidence (what the machine did without these principles): `reviews/BASELINE-246-2026-09-05-v1.html` and `outputs/baseline-246/arm-*/render-1440-light.png` — read them; cite the specific defect each principle would have prevented.

## WHAT EXISTS (read before writing — do not duplicate, extend)
- `knowledge/guidelines/` — 59 notes; `knowledge/guidelines/_rules-index.json` — 470 rules tagged BLOCKING / ADVISORY / REVIEW / TASTE. Grep for: progressive disclosure, density, dashboard, bento, hierarchy, filters, default state, rhythm. Quote existing rule ids you build on.
- The bento foundations: `showroom/foundation-bento*.html`, `showroom/foundation-grids-dashboard.html`, `showroom/foundation-grids-display.html`, `knowledge/_render/_bento_edit_rails.json` (the edit-pass rails), `knowledge/components/template-dashboard-bento.meta.json`. Dave loves the DISPLAY bentos — look at why.
- Rulings that touch this: `grep -n -i "bento\|density\|dashboard" knowledge/_rulings.json` — anything Dave already ruled is settled; cite by id, do not re-open.

## RESEARCH (web — WebSearch/web_fetch; cite every source with URL; primary sources over blogs)
Four topics, bounded to what a dashboard needs:
1. **Progressive disclosure / progressive reveal strategies** — the taxonomy (staged, contextual, on-demand, drill-down, dismissible controls, expand-in-place, overview→detail, defaults-then-controls). Nielsen Norman, Tidwell (Designing Interfaces), Few (Information Dashboard Design), Cooper (About Face), and the major design systems' dashboard/filter guidance (Carbon, Atlassian, Polaris, Material, GOV.UK, Fluent, SAP Fiori overview pages). What each says about WHEN to hide, WHAT the default state is, and WHO decides.
2. **Density and stat rows** — why a KPI row beats a 2×2 above the fold; Few's "overview at a glance"; guidance on the number of KPIs, their order, and the delta/spark treatment.
3. **Execute-on-page + feedback** — dashboards that carry actions (approve, release, retry) and a status/feedback surface (tasks, exceptions, "needs attention"); SAP Fiori Overview Page / Work Zone, Atlassian, Salesforce Lightning home, banking treasury portals (public material only). What patterns recur.
4. **Bento rhythm and hierarchy** — asymmetry, odd counts, importance-weighted widths (6-4-3-2 on a 12/6 grid), editorial grid theory (Müller-Brockmann, Hochuli), Apple's bento marketing pages as the popular reference, and any measured guidance on "regular grid = boring". Find the principles that make irregular layouts read as ORDERED not messy (alignment to a common baseline, a single dominant module, repetition with one break, span ratios).

## DELIVERABLE — ONE page, swiss-design-system idiom, for Dave's ruling
`reviews/DASHBOARD-PRINCIPLES-2026-09-05-v1.html` (skill: `swiss-design-system`). Structure, in this order:
1. **The four seeds** (Dave's words, verbatim) each paired with the baseline defect it names (render crop or the file/line).
2. **Research digest** — per topic, ≤ 8 findings, each ONE sentence + source URL. No essay.
3. **DRAFT PRINCIPLES** — numbered `DP-01…`, each in the `_rules-index.json` shape: statement · rationale (one line, sourced) · proposed tag (BLOCKING / ADVISORY / REVIEW / TASTE — PROPOSED, never ruled) · which component/meta/rail it would bind to · the baseline defect it prevents. Aim 12–20, not 50. Group: reveal · density · execute+feedback · bento rhythm.
4. **What it would take to ENACT** — for each group, the ONE source it lands at (guideline note, a meta field, a bento rail, the skill text, a validator arm) and a rough size. Additive only.
5. **Ruling-shaped questions for Dave** — numbered, unanswered. Include: which tags; whether "designer decides the default state" becomes a brief question in grill-me; whether importance-weighted spans need a new bento dial; whether the "needs attention / tasks" surface is a new component or a composition.

Plus `notes/_subreports/2026-09-05-246-P-principles.md` — what was done, sources count, declared gaps, tokens.

## RULES
- ⛔ No edits under `knowledge/`, `showroom/`, `apollo-spider/`. No commit, no push. No ruling.
- Every principle cites a source or Dave's words; a principle with neither is TASTE and says so.
- Copyright: paraphrase; ≤ 1 short quote per source.
- Return: the review path, the subreport path, principle count by group, top 3 findings in one line each, the RSQ list.
