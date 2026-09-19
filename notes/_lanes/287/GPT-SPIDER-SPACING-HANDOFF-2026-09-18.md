# Spacing and layout without vision — development-agent handoff

Date: 2026-09-18  
Audience: Apollo development-workspace agent and system owner  
Origin: Apollo Spider v1.0.13 test bed; HSBC CEO banking prototype  
Lane: On-canon investigation; recommendations below are not new design-system rulings  
Delivery: Standalone report only; no prototype, canon, token, generator, gate or instruction changes accompany it

## 1. Executive summary

**Replace “be careful with spacing” with explicit layout relationships and browser-measured evidence.** Token usage alone does not establish correct spacing: a legitimate token can resolve to an unexpected value, a higher-specificity rule can override it, and a valid component can be placed in an invalid composition.

The CEO prototype improved after measuring and correcting shared page insets, outer bento spacing and action-button separation. The user subsequently reported: “Visually these results are good, the instructions to be careful with spacing reaklly helped.” That is useful designer feedback, not evidence that the agent performed a visual review.

Two template-level issues remain: Supercharge's prescribed 2px inner gap renders as 4px, and the deliberately fixed four-column KPI group clips financial values at narrow widths. A separate information-architecture problem also remains: multiple destinations reuse the same reporting wall instead of supporting distinct tasks.

Recommended development sequence:

1. Prove the failure classes with a standalone, read-only runtime checker and small positive/negative fixtures.
2. Reconcile theme-default delivery, supported instance dials and deliberate responsive overrides in the actual development source tree.
3. Add relationship-based layout contracts and truthful coverage reporting to the existing gate architecture, initially with an explicit trial posture.
4. Test typography changes and stressed content, not just the default screen.
5. Require page-purpose/content decisions before selecting a page template.

**Boundary:** this workspace is a test bed, not the Apollo development workspace. Do not treat this report as permission to patch its shared system files, silence gates, rewrite generated outputs or commit the enclosing home-directory repository.

## 2. Evidence, authority and limits

### 2.1 Evidence inventory

All references below are relative to this test-bed workspace. The narrative and measured values are included here so the report remains useful when copied to the development workspace; links may need remapping there.

| Source | What it establishes |
| --- | --- |
| [Confirmed CEO brief](../briefs/2026-09-18-hsbc-ceo-international-banking-grill.md) | Supercharge, both modes, comfortable wide desktop, bento, simulated workflows and no-vision constraint |
| [Prototype composition](../screens/hsbc-ceo-banking.canon.html#L10-L35) | Local wrapper, spacing-token and layout-dial bindings |
| [Browser suite](../screens/hsbc-ceo-banking.test.cjs#L171-L198) | Actual geometry selectors, conditions and desktop assertions |
| [Saved browser results](../artifacts/hsbc-ceo/browser-checks.json) | Snapshot dated 2026-09-18T09:36:17.858Z; 31 passed, 0 failed; twelve width/mode measurements |
| [Generated bento rails](../knowledge/_render/_bento_edit_rails.json) | Legal dial options, per-theme defaults, generator ownership and permission levels |
| [Template metadata](../knowledge/components/template-dashboard-bento.meta.json) | Declared contracts, proposed status, specificity warning, responsive claims and open decisions |
| [Compiled template spacing](../knowledge/canon/canon.css#L18113-L18121) | 32px wrapper inset and template-scoped Mono 40px/4px gutter declarations |
| [Compiled lead layout](../knowledge/canon/canon.css#L18162-L18184) | Deliberate four-column override of the generic bento band machinery |
| [Editorial scale](../knowledge/canon/type.css#L8-L18) | Existing title-size composites; no new typography needed for requested increases |
| [Baseline gate log](../artifacts/hsbc-ceo/baseline-gates.log), [final gate log](../artifacts/hsbc-ceo/full-gates.log) | Both report 33 pass / 8 FAIL / 0 could-not-ask |
| [Screen gate record](../knowledge/_screen-gate/hsbc-ceo-banking.canon.md) | Screen-specific passes, failures and unproven claims |

No browser suite or gate was rerun for this report. Existing evidence was read and checked against current source. Do not interpret the report date as a new execution timestamp.

### 2.2 What is and is not approved

- **Confirmed user direction:** retain the successful spacing discipline; make the overview system-wide reporting plus task navigation; give destination pages distinct content; increase the main title and Accounts and balances title by two existing scale steps; keep this workspace a test bed; vision is disabled with no workaround.
- **Observed implementation:** fixes and remaining defects described in sections 3–5.
- **Recommendations, not rulings:** checker schema, new assertions, thresholds, responsive policy and integration plan below. Obtain system-owner decisions where they alter established rules.
- **Not performed:** agent visual review, screenshot interpretation or formal accessibility certification. An earlier screenshot is not validation evidence. Do not pursue an alternate vision service or Quick Look workaround.

## 3. Measured results and the changes that helped

### 3.1 Shared page alignment

**Before:** header, filters and records began at the viewport edge; the bento wall began 32px in. Reusing components had not given them a shared page frame.

**Local correction already made:** reuse the existing canonical page wrapper around the relevant regions and remove redundant nested framing. This aligned the header, filters, reporting wall and register rather than adding individual compensating margins.

**Evidence:** all four measured regions begin at x=32. At 1440px their right edges are 1408; at 1920px, 1888; at 1100px, 1068. The JSON records both edges. The automated alignment assertion currently checks rounded left edges only; right-edge equality was observable in the saved data, not a separate assertion.

**General lesson:** define one page-frame owner. Specify which regions share it, and which deliberately use full bleed. A component's valid internal padding does not establish its position relative to sibling sections.

### 3.2 Outer bento spacing and computed token resolution

**Before:** the copied template contributed Mono's 40px outer gap while the page selected Supercharge, whose dashboard default is 24px.

**Intermediate failure:** binding the outer dial to `--layout-bento-gutter` did not fix it; that variable resolved to 0 in the consuming scope. The reference to a legitimate token looked plausible in source but failed in the browser.

**Local correction already made:** the screen's `#portfolioWall` binds `--bento-gutter` to `--padding-fixed-xlarge`, which resolves to 24px in the tested context. Computed grid gap was verified in both modes.

**Important distinction:** this is a local composition fix, not the ideal universal API. Do not prescribe this ID selector or fixed token for every theme. Development should deliver the selected role/theme default through a supported, cascade-safe mechanism; a consumer should not have to outguess template specificity.

### 3.3 Action-button separation

**Before:** adjacent controls in some reset/share and export/action groups had no explicit separation.

**Local correction already made:** action wrappers use flex layout, wrapping and `gap: var(--padding-fixed-medium)`, resolving to 16px. The desktop suite asserts this computed gap.

**General lesson:** button anatomy and an arrangement of buttons are different contracts. HTML whitespace is not a spacing system. Check the group container and actual neighbouring bounds, not just each button's padding.

### 3.4 Readiness and dialog focus

An initial one-animation-frame focus callback could run before the canonical modal became visible. Early tests also read empty displayed text or tried to focus a hidden close button.

The application now waits for computed visibility before initial focus and avoids an old opening callback refocusing a newer dialog. Tests await visibility and rendering readiness. This is a behaviour/readiness fix, not a correction to visual appearance, but it is essential to trustworthy geometry and interaction evidence.

### 3.5 Final recorded geometry

The following outcomes were the same in light and dark mode. Viewport height was 1100px.

| Viewport width | Document width | Outer gap | Inner group gaps | Selected text/number clipping |
| --- | --- | --- | --- | --- |
| 1920px | 1920px | 24px | 4px | None detected |
| 1440px | 1440px | 24px | 4px | None detected |
| 1100px | 1100px | 24px | 4px | None detected |
| 820px | 820px | 24px | 4px | None detected; diagnostic coverage, not complete tablet approval |
| 520px | 520px | 24px | 4px | £758.4m needs 93px and −£32.6m needs 89px; each has 79px |
| 390px | 418px | 24px | 4px | All four KPI values clip; available width 47px, required widths 73–93px |

At desktop widths the suite also found no overlap between KPI tile rectangles and no footer overlap with the measured last-content region. This is not an all-elements collision audit.

## 4. Remaining system findings

### 4.1 Theme vocabulary is not fully delivered by the template

The generated role defaults specify:

| Theme | Dashboard main spacing | Dashboard sub-spacing |
| --- | --- | --- |
| Mono | 40px | 4px |
| Common, represented by `legacy` in this rails artifact | 24px | 4px |
| Console | 40px | 4px |
| Supercharge | 24px | 2px |

The inspected template scope embeds Mono's 40/4 pair. Metadata explicitly notes that other themes' defaults are addressed elsewhere rather than emitted there. This is more specific than “the agent chose the wrong gap”: the root theme and the template's shipped layout behaviour can disagree.

**Recommendation:** trace the development-side generation path from the authoritative role defaults through template projection to the consuming grid. Produce one supported implementation of that contract, and test all themes. Do not duplicate a defaults table in a new checker; read the authoritative data and independently test its projection into CSS.

### 4.2 The 2px inner dial is vocabulary, not a usable binding here

`subSpacing` legally includes 2. The rendered inner groups remain at 4px. No intent-correct consumer binding for selecting 2px was identified in this investigation. A token with a numerical value of 2px elsewhere is not automatically appropriate for content spacing.

**Recommendation:** decide how legal dial values are exposed and minted. If the system needs an additional semantic binding, use its existing authoring/governance process. Do not borrow a border-width or segmented-control padding token, add an arbitrary raw value in a page, or loosen a checker to accept 4px as the Supercharge default.

The legal bento stop set is `{1, 2, 4, 16, 24, 40}`. It applies to those bento dials, **not to every spatial value in every component**. The template's 32px page inset and its component-internal spacings must not be rejected simply because they are not bento stops.

### 4.3 Four columns are intentional, not a missing generic media query

The lead group's explicit `repeat(4, minmax(0, 1fr))` deliberately out-specifies bento's container bands. Source comments describe an earlier decision to avoid ragged packing at tested widths. Deleting it would change a deliberate layout policy, not merely repair a typo.

The template metadata also contains a broader banded-reflow description that does not adequately communicate this exception. The development agent should reconcile the current contract, exception and coverage rather than blindly relying on either description.

**Recommendation:** get a sanctioned small-container policy for lead KPIs. A four-to-two-to-one progression is a candidate, not a decision in this report. Preserve content legibility, source order and grouping; do not make the data fit by shrinking type, clipping money, scaling the whole page or hiding values.

Use the actual queried container width. The page frame consumes 64px, and nested groups have their own containers; a 1100px viewport is not a 1100px bento container. Test just below, at and just above each relevant container threshold.

### 4.4 Availability is not approval

The inspected template metadata still labels its status PROPOSED and includes unresolved governance questions, despite the template being distributed and directed for use by the composition skill. Development should reconcile this status with the supported consumer path. Do not silently promote it by writing a test that passes.

## 5. Why the current green browser result is insufficient

**31 pass / 0 fail means the executed assertions passed, not that the layout has no known defects.**

Current coverage limitations:

- Only widths at or above 1100px run blocking geometry assertions. Smaller-width findings are recorded but do not fail the suite.
- Inner 4px gaps are recorded, not asserted against the Supercharge 2px expectation.
- Geometry checks run on the overview in its default data state. Navigation and workflows are exercised separately, but not all their layouts are measured in every mode/width/state.
- Text overflow checks cover `h1`, `h2`, KPI amounts and buttons, using `scrollWidth > clientWidth + 2`. This does not comprehensively detect ancestor clipping, vertical clipping, line-clamp loss or inline-text collisions.
- Pairwise overlap is checked among KPI tiles, not all meaningful sibling regions.
- Left-edge assertions round coordinates. There is no explicit contract for logical end edges, nesting depth, cumulative inset or baseline relationships.
- A computed `gap` can be correct while `space-between`, margins, padding or child sizing creates an incorrect actual separation.
- There are no full stress fixtures for very long labels, substantially larger figures, text enlargement, validation-message growth or RTL content.

**Reporting recommendation:** separate assertion results, expected-but-unmeasured coverage and known violations. For example: “desktop contract assertions passed; two known responsive/spacing findings remain; visual review unavailable.” Do not aggregate an untested or knowingly failing requirement into an unqualified green summary.

The full pack's eight failing categories remain composition, grid, polarities, receipt, role resolution, screen, token forks and type blast radius. The CEO screen separately passes compose, icon-source and static accessibility checks, while receipt behaviour checks fail and several composition/provenance claims remain unproven. Three pack passes examined zero subjects. These findings must remain visible when a new layout checker is added.

## 6. Recommended standalone layout-contract checker

### 6.1 Responsibility and non-goals

Build a generic measurement runner with small composition adapters. The runner should read an application and its contract, exercise named states, measure them, and emit evidence. It should not rewrite application CSS or automatically repair layout.

Keep responsibilities distinct:

1. **System contract:** supported tokens, theme/role defaults, component anatomy and responsive rules.
2. **Composition contract:** which regions share an edge, which regions contain others, which content must remain visible and which overflow is intentional.
3. **Runtime evidence:** actual styles, bounds, state, loaded assets and measured values.
4. **Product judgement:** information priority, usefulness, balance and whether the page answers the right question.

Existing gates remain responsible for their existing questions. Reuse them rather than implementing a second token, provenance or icon system inside this checker.

### 6.2 Candidate contract records

This is a schema proposal, not a shipped manifest or new required format. Align it with existing schemas before adoption.

| Field | Purpose |
| --- | --- |
| Stable check ID | Identify a requirement across reports without depending on line numbers |
| Contract source | Link the rule, approved brief or component metadata that authorises the expectation |
| Page, region and locator | Identify the consumer; prefer stable semantic/test hooks over text-dependent selectors |
| Applicability | Theme, mode, density, container band, route and state |
| Relationship | Equal inline edge, contained by, sibling separation, non-overlap, no unintended overflow, or type-composite match |
| Expected value or source address | Resolve theme-specific expectations from their source rather than duplicating numbers |
| Measurement method | Computed property, border/content rectangle, text fragment or scroll extent |
| Tolerance | Declared by measurement type; never a global allowance that hides a meaningful gap mismatch |
| Expected overflow | None, wrapping, approved truncation or named scroll container |
| Required subject count | Prevent a broken locator or absent component being reported as a pass |
| Exception | Scoped reason, owner, evidence and review condition; no blanket ignore list |

For this reproduction, candidate requirements are: shared page-frame edges; outer and inner gaps matching selected role/theme; action-group separation; readable financial figures; footer after normal-flow content; deliberate, bounded table scrolling; dialog controls inside its usable area.

### 6.3 Measurement and false-positive controls

| Probe | Method | Essential qualification |
| --- | --- | --- |
| Shared edges | Compare `getBoundingClientRect()` values for declared peer regions | Compare the intended border/content edge; use logical start/end when supporting RTL; exclude documented full-bleed sections |
| Effective spacing | Read computed `rowGap`/`columnGap`, then measure adjacent same-row/column border-box separation | Account for wrapping, alignment, margins and padding; the nearest DOM sibling may not be the spatial neighbour |
| Containment | Compare child bounds with the declared ancestor's usable area | Distinguish border, padding and content boxes; intersect clipping ancestors, not just the immediate parent |
| Overflow | Check both scroll dimensions, document extent and declared scroll regions | Horizontal table scrolling can be valid while document-level horizontal overflow is not |
| Text fit | Combine scroll metrics with `Range.getClientRects()` and clipping-ancestor bounds | Text fragments are layout boxes, not painted glyph bounds; cap-height, descender and optical issues still require existing specialist checks or human review |
| Overlap | Compare declared sibling regions with expected co-visibility | Do not compare every element with every element: nested content, icons in buttons and intentional overlays overlap legitimately |
| Responsive packing | Measure actual container widths, grid tracks, item order and occupied rows | Do not hardcode every screen to four columns or make raggedness universally illegal without the component's contract |
| Typography | Check selected composite and computed size, line height and weight for the intended mode | Preserve semantic heading levels; a larger class does not justify changing heading order |
| Dialog/action reachability | Exercise long content and validation; check visible/reachable controls and focus behaviour | Scrolling may be intentional; geometry alone cannot establish focus-ring visibility or complete accessibility |

Tolerance should address subpixel browser rounding, not policy violations. A narrowly scoped geometric epsilon, for example up to 1 CSS pixel where justified, is a proposal to validate with fixtures. It must never turn a required 2px gap rendered as 4px into a pass. Device pixel ratio, browser engine and coordinate space should be recorded.

### 6.4 Readiness protocol

1. Load a deterministic dataset and named route/state in an isolated browser context.
2. Confirm required CSS and font assets loaded. Await `document.fonts.ready`, but also check the expected face/load outcome; “ready” does not prove that no fallback font was used.
3. Await the application state's readiness and relevant component visibility, including chart fit/resize work.
4. Require stable relevant bounds across a small declared number of animation frames, with a bounded timeout. Two frames were useful in this prototype but are not a universal asynchronous-readiness guarantee.
5. Record unavailable measurements or readiness failures explicitly. Do not retry until a random pass, sleep for an arbitrary duration, or treat a timeout as an empty successful population.
6. Use a reduced-motion lane for deterministic settled geometry and a normal-motion lane for transition-dependent behaviour. Do not disable the very behaviour being tested without declaring it.

No screenshots are necessary for these measurements. Their absence must remain visible in the result, not be disguised as visual approval.

### 6.5 Coverage matrix

Start with a small, explicit matrix; expand according to risk rather than generating an unbounded Cartesian product.

- **Theme:** all four system themes for reference/default-delivery fixtures; the selected theme for each application contract.
- **Mode and density:** light/dark and every density actually claimed by the consumer.
- **Dimensions:** representative desktop and small widths, relevant container breakpoints ±1px, constrained embedding inside a narrower host, and short-height dialogs.
- **Content:** long entity/account names, long headings, large and negative monetary values, zero, unavailable values, long references and non-breaking strings. Use realistic fixtures, not arbitrary truncation to pass.
- **State:** default, filtered, zero results, record detail, open menu/dialog, validation error, persisted state and loading/error states where the component implements them.
- **Text scaling:** test the applicable resizing/reflow requirements, including text enlargement and a narrow CSS viewport. Do not equate device-scale-factor changes with browser zoom, or claim a viewport-only test proves every zoom criterion.
- **Direction/language:** include RTL and expanded translations when supported or required; otherwise report them out of scope, not passed.

Prioritise default and worst-content cases across every supported band. Use targeted pairings for additional states, and publish what the chosen matrix does not cover.

### 6.6 Result model

Separate **outcome**, **severity** and **approval status**:

- Outcomes: PASS, FAIL, UNMEASURED, and justified NOT APPLICABLE.
- Severity: blocking or advisory according to an explicit, approved gate posture.
- Approval: independently report whether visual/product review exists and whether the underlying pattern is approved.

A required missing element is a structural failure, not a passing zero-subject check. An unavailable browser is unmeasured. A legitimately absent optional panel is not applicable only when the contract says so. Unknown expectations must not default to the rendered value.

Each finding should include expected/actual values, the subject and its container bounds, route/state/theme/mode/density, viewport and container size, relevant token values, measurement method, tolerance, source authority, runtime version and artifact timestamp/hash. Investigative cascade information can be attached where available; do not promise that `getComputedStyle()` alone identifies the winning selector.

Example finding, based on the saved data: “Supercharge dashboard inner gap: expected 2px from role defaults; observed 4px on the inner grids. Template-scoped rule requires investigation.”

Example finding, based on the saved data: “At viewport 520px, cash amount has 79px available but requires 93px; essential figure does not fit. Lead group still has four columns.”

## 7. Page architecture is a separate layout input

A geometry checker can approve seven neatly spaced versions of the wrong page. This prototype demonstrates that limitation: the renderer keeps the overview wall for most banking destinations, then changes the register below it. The user's objection is valid even when the browser checks pass.

**Confirmed direction:** the overview is a system-wide reporting bento and launcher. It should give status, significance and a meaningful next action. Destination pages should be task-led, not copies of that wall.

### 7.1 Proposed content allocation for the next prototype revision

| Destination | Primary content | Task it enables |
| --- | --- | --- |
| Overview | Financial resilience, risk outlook and decisions across the system; concise summaries and contextual links | Understand the position and choose the next task |
| Accounts | Balances by account/entity/currency, availability/restriction and selected-account transactions | Locate cash and investigate movement |
| Liquidity | Funding capacity, facility utilisation and maturity schedule | Assess headroom and request a drawdown |
| Payments | Approval queue, exceptions and payment history | Approve, reject, investigate or create a simulated payment |
| FX and markets | Currency exposure, hedged/unhedged amounts and relevant positions | Investigate exposure and request a quote |
| Risk | Breaches, utilisation, concentration and recorded responses | Prioritise exceptions and document mitigation |
| Trade | Instruments, expiries, required documents and requests | Resolve requirements or request finance |
| Reports | Library, reporting scope and generated briefings | Prepare a board pack or export |
| Messages / settings | Correspondence and request tracking / workspace preferences | Follow up with the service team / configure the workspace |

This allocation is a proposal, not an assertion that the prototype already implements distinct layouts or that every required pattern exists. Inventory canonical list, detail, report and settings templates before choosing their presentation. If none fits, surface the gap through the existing process instead of forcing the dashboard template or inventing a page-scale pattern.

Carry entity/region scope into task links, and expose the destination's active filters. Keep overview counts and linked queues definitionally consistent. Remove the full account register from the overview unless the designer explicitly asks for it; Accounts owns detailed account work.

Before composing each page, state its primary question, content, main task, supporting actions, states and overflow policy. Distinct content should determine layout, not cosmetic variety for its own sake.

### 7.2 Requested title changes — not yet applied

| Element | Current composite | Requested two-step increase |
| --- | --- | --- |
| Main page title | `t-ed-heading-2`, 28px / 36px line height | `t-ed-display-2`, 40px / 48px line height |
| Accounts and balances section title | `t-ed-heading-4`, 20px / 28px line height | `t-ed-heading-2`, 28px / 36px line height |

Retain semantic `h1` and `h2`. Use the existing composites rather than raw size/weight overrides. Test long titles, two-line wrapping, action clearance and surrounding vertical rhythm after applying the change. Do not apply a compensating negative margin or fixed header height to preserve the previous screenshot shape. The user named the Accounts and balances title; do not silently enlarge every section heading across all pages.

## 8. Development work packages and acceptance criteria

### WP1 — Establish a trustworthy reproduction and checker

**Priority:** first. **Scope:** standalone tooling and fixtures in the development workspace, with source ownership verified before any shared edit.

- Reproduce the known 4px versus 2px mismatch and the two narrow clipping cases.
- Add positive fixtures and deliberate failures for misaligned insets, zero/wrong gaps, doubled nesting, overflowing figures and missing subjects.
- Include legitimate wrapping, full bleed, scrolling tables and intentional overlays as non-failing counterexamples.
- Prove that the checker catches a token resolving to zero and a legal token losing through the cascade.
- Report known findings separately from passing assertions and fail coverage requirements when mandatory subjects are absent.
- **Acceptance:** each seeded defect is detected, counterexamples do not fail, results are stable across repeated runs, and the report makes no visual-review claim.

### WP2 — Deliver role/theme spacing coherently

**Priority:** high. **Scope:** authoritative defaults, supported dials and their development-side generators/projectors.

- Trace and fix the source path; do not hand-edit generated rails or compiled canon as the permanent repair.
- Define deterministic precedence between theme defaults, permitted instance choices and template layout rules.
- Exercise both nested and non-nested dashboard structures where supported; specificity is part of the contract.
- Check that approved non-default dial choices win without new ID-selector or `!important` workarounds.
- **Acceptance:** reference default fixtures render 40/4, 24/4, 40/4 and 24/2 for the respective themes in both modes, using the declared source of truth; unrelated components retain their own spacings.

### WP3 — Set and implement a supported lead-group reflow policy

**Priority:** high for reusable system support; the original application brief targeted wide desktop.

- Review the deliberate four-column rule with the system owner before replacing it.
- Establish a supported minimum container/content requirement and approved behaviour below it.
- Reconcile metadata, snippets, generated outputs and assertions so they describe the same policy.
- **Acceptance:** no essential KPI clipping or accidental document overflow in the agreed supported bands and stressed content; logical reading order remains intact; any intentional limitations are explicit. The original 520/390px failures must either be fixed under the approved policy or remain clearly out of the supported contract, never silently green.

### WP4 — Integrate with truthful gate posture

**Priority:** after fixture proof. **Scope:** existing gate/coverage architecture, not a parallel compliance system.

- Reuse relevant existing fit, grid, type, descender, hidden-display and composition checks after inspecting their actual populations.
- Start experimental heuristics as explicitly advisory where their precision is not established; promote only through the normal decision process.
- Keep exact contract violations distinct from uncertain heuristic signals.
- **Acceptance:** the combined report identifies tested population, missing coverage, genuine failures, baseline debt and review limits. Zero subjects cannot masquerade as verified application coverage.

### WP5 — Revise the prototype by page purpose

**Priority:** separate application lane; do not mix product restructuring with a spacing-engine change.

- Build a separate prototype revision if requested; preserve this reproduction and its evidence.
- Apply the two requested title increases and content allocation after checking suitable canonical templates.
- Replace generic repeated dashboards with task-appropriate content and retain contextual launcher links.
- **Acceptance:** overview summarises the whole system; each destination exposes its primary task immediately; counters agree with linked records; revised title/layout stress checks pass for the supported scope. Product review remains a distinct requirement.

## 9. Decisions needed from the system owner

1. What is the approved public mechanism for theme-aware dashboard defaults and instance dial selection?
2. What replaces or constrains the deliberate four-column lead rule below its proven width/content envelope?
3. Where should composition-level layout relationships live, without duplicating token or component facts?
4. Which checks are mature enough to block, and how are scope-limited exceptions reviewed?
5. What is the supported status of the distributed bento template, and how should consumers discover that status?

These are development decisions, not reasons to ask the designer to choose arbitrary padding values. Preserve defaults already ruled; ask only where the contract is genuinely unresolved.

## 10. Guardrails for the receiving agent

- Work in the actual development repository. Verify its root, tracked files and rollback strategy; do not rely on this test bed's enclosing home-directory Git repository.
- Before critical changes, state exact scope and reason, then create and verify the required dated rollback backup.
- Follow source ownership. Generated files declare their generators; fix authoritative inputs and regenerate through the supported sequence. Not every system file is generated: the typography file explicitly describes itself as hand-authored.
- Never conceal a defect with overflow hiding, smaller monetary text, an unrelated token, a broad selector, relaxed tolerances, an unused script or a weakened gate.
- Do not update golden expectations from the currently broken render. Expected values need an independent contract source.
- Do not turn “uniform spacing” into “every gap is the same.” Page frames, inter-group gaps, intra-group gaps and component-internal rhythm serve different purposes.
- Keep the existing pack and screen failures visible. Fixing layout does not resolve receipt, tracking or governance failures.
- No visual workaround. User feedback can be recorded as user feedback; runtime geometry can be recorded as runtime geometry. Neither should be relabelled as agent visual inspection.

## 11. Handoff completion and requested return evidence

This report is the only authored workspace change for this request. No implementation, title change, new checker, shared-system fix or new gate run is claimed. Existing prototype and Memento state files remain untouched by this reporting task.

The development agent should return:

1. The authoritative source path and confirmed cause for each defect class.
2. A minimal fix per class, with any required system-owner decisions clearly separated.
3. Passing positive fixtures and failing negative fixtures before the repair, followed by corrected runtime results.
4. Theme/band/content coverage with actual subject counts, explicit exclusions and known gaps.
5. Before/after expected and observed values, not only screenshots or a green total.
6. Generator/determinism results and the real full-gate outcome, including unchanged baseline debt.
7. A clear statement that visual review remains unavailable unless that environment and user direction genuinely change.

**Success is not “all pixels measured.” It is making recurring, mechanically detectable layout failures difficult to ship, while preserving an honest boundary around what the measurements cannot judge.**
