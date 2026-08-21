#!/usr/bin/env python3
"""
gen_review_213_wave_components.py — builds reviews/REVIEW-213-wave-components-four-theme-v1.html

⛔ PROPOSED, NOT RULED. This generator writes a REVIEW SURFACE, nothing else. It mints no token,
edits no canon, touches no store file. Written 2026-08-21, session #213, LANE R.

WHY IT EXISTS
  43 components landed in waves 3-6 (#209 wave 3, #210 waves 4/5/6). Every one ships
  PROPOSED-NOT-RULED and its store row is parked awaiting Dave's eye (W-63, W-71..W-74 open;
  W-75..W-84 parked). No four-theme review surface covered them — the newest four-theme pages in
  reviews/ were REVIEW-203-*. Dave cannot rule 43 components from receipts.

THE SPECIMEN RULE — [[specimen-starts-from-reference]] (#202)
  ⛔ NOTHING on this page is re-drawn. Every specimen is an <iframe> pointing at the component's
  OWN generated showroom page (showroom/<slug>.html), which itself srcdoc-mounts the gated
  reference snippet. Not one byte of component markup is copied into the review page. The review
  page owns only chrome: the theme broadcast, the question prose, and the decision controls.

HOW THE THEME BROADCAST WORKS (read gen_showroom.py:309-315 before changing it)
  Each showroom page ends with:
      window.addEventListener('hashchange', initFromHash);
  and initFromHash reads  #theme=<attr>&m=<light|dark>&w=<px>  and re-applies
  html[data-apollo-theme] + body[data-theme] to the srcdoc frame, plus the width slider.
  So the review page re-themes a specimen by assigning a new FRAGMENT to iframe.src — a
  same-document fragment navigation, no reload, no cross-origin script access. That is the whole
  mechanism; it is why this page needs no copy of the theme cascade.

REGENERATE
  python3 knowledge/_render/gen_review_213_wave_components.py
"""

import html
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "reviews", "REVIEW-213-wave-components-four-theme-v1.html")

THEMES = [("mono", "Apollo Mono"), ("legacy", "Legacy"),
          ("console", "Console"), ("supercharge", "Supercharge")]

# ---------------------------------------------------------------------------
# CROSS-CUTTING QUESTIONS — one ruling each, many components show the symptom.
# Prose condensed from the lane receipts named in `src`.
# ---------------------------------------------------------------------------
CROSS = {
    "w3": dict(
        label="Wave 3 — questions that span the nine",
        src="notes/_receipts/2026-08-20-209-wave3-lane{A,B,C}-*.md",
        items=[
            "The coloured money seats (success-ink / error-ink) are MONO ONLY and were deliberately left unbound. Every figure in all nine components is monochrome. Binding them on a ledger would have been ruling on your behalf.",
            "“Failed” and “At limit” sit on the WARNING seat, not the error seat. That is declared restraint, not a considered ruling — the error seat touches the two-red law.",
            "No component paints a delta, an arrow or a series. There is no trend anywhere in this wave, by construction.",
            "Is the <symbol>/<use> + fill=“currentColor” pattern the idiom every future icon-bearing snippet should copy, or should the library inline <path fill=“currentColor”> with no symbol indirection?",
            "No recurring-payment glyph exists in the library — four reload glyphs, none of which means “this payment repeats”. An _ICON-GAPS entry may be owed.",
        ]),
    "w4": dict(
        label="Wave 4 — questions that span the heavy seven",
        src="notes/_receipts/2026-08-20-210-wave4-lane{A,B,C}-*.md",
        items=[
            "The descender-clip gate accepts an override that loses on specificity, so Sidebar-nav is clipped today under a green gate. The class fix is a gate that reads the COMPUTED edge, not the authored string. Neither was done — both are priced TODOs.",
            "The accessibility and hit-area role vocabularies are missing four roles, so four of this wave's components are partly invisible to their own gates.",
            "Date-picker's today+selected ring is invisible. Found by looking, unrepaired, and the file is gated so the lane could not touch it.",
            "Type-composite debt grew 1097 → 1099 (+2) on the shared baseline line — in direct tension with the shrink-only ratchet. Flagged rather than silently accepted or worked around.",
        ]),
    "shell": dict(
        label="App shells — questions that span all seven",
        src="notes/_receipts/2026-08-20-210-wave5-laneA-app-shells.md · 2026-08-20-210-wave6-laneA-p3-shells.md",
        items=[
            "THE BREAKPOINT SCALE, and it is the biggest one. Wave 5's three shells carry three different pairs — 900/600, 1040/720, 1200/840. Wave 6's four deliberately reuse 900/600 rather than adding a fourth. layout.json has no breakpoint scale. Reusing an unruled number is not the same as having one.",
            "THE BRAND MARK. Twelve official SVGs exist, nothing binds them, zero of 108 snippets reference them. A component, or a direct embed? Until you answer, every shell carries a text wordmark stand-in.",
            "Does a shell belong in knowledge/snippets/ at all? The evidence for is that every existing gate then watches it for free — and it bit twice, catching a real off-grid value and a real schema violation. The evidence against is that the showroom, the knowledge graph and component-types.json all assume components.",
            "Should the schema gain a real layer property and a shell category value, instead of the $layer annotation these carry today? And $layer still has no consumer — nothing reads it.",
            "The placeholder convention: static aria-hidden furniture for a frame, the real announcing loader only where something genuinely loads. Confirm or overturn, once, for all of them.",
            "Should scroll-margin-top become a library-wide rule? Every sticky region in the repo has the same defect latent in it and nothing gates it.",
            "display:contents on the phone band's lists is accepted with a declared assistive-tech risk and NO screen-reader test. Worth a real device.",
            "All domain prose is placeholder — pane names, destination names, group names, the statement block. None is a semantic a lane may mint.",
        ]),
    "tpl": dict(
        label="Templates — questions that span all eleven",
        src="notes/_receipts/2026-08-20-210-wave5-lane{B,C}-*.md · 2026-08-20-210-wave6-laneB-p3-templates.md",
        items=[
            "Is the Layer-2 artefact class right? Each of these ships as snippets/<Name>.reference.html + components/<slug>.meta.json so every existing gate watches it for free. That is a PROPOSED convention stated once in a brief. If a template is not a “component” it may want its own home — and then it is born ungated.",
            "meta.schema.json has no seat for COMPOSITION. relationships is a closed shape with no edge for “the components this organism is assembled from” — the defining relationship of a template. It is carried as $composes so it is greppable but does not pretend to be a graph edge. Eleven files now depend on this.",
            "Should a template ship any JavaScript at all? Ten of the eleven ship none. Consequence, stated plainly: the search boxes, chips, switches, radios and sort headers LOOK LIVE AND ARE NOT.",
            "Where does a shell end and a template begin? These are the content region and assume they sit inside a <main>. “A shell wraps a template” is PROPOSED, adjudicated nowhere.",
            "Six type-composite weight deltas: every borrowed rule lost its raw font declaration, so errored inputs no longer go to weight 500, Selection-controls' labels drop 500 → 400, Summary's value row loses its 500. One root cause, not eight — the canon ramp has no 16/500 input or label composite. Widen the ramp, or accept that Layer-2 carries lighter emphasis than the Layer-1 it composes.",
            "Three inherited target-size shortfalls, MEASURED and not silently fixed: Breadcrumbs' links are ~39 × 10.1px (the leading-trim cap box IS the link box), View-options' segments are 40px, Data-grid's clear and chip-dismiss are 24 × 24. All three are the source components' shipped geometry — a lane must not quietly enlarge a gated component's target.",
            "Every status vocabulary is PROPOSED. Completed / Pending / Failed / Reversed · Awaiting approval · Reconciled / Two exceptions / Awaiting value date · Awaiting a second approver · Two changes not yet saved.",
            "No monetary figure on any template is coloured — the mono-only seats carried deliberately across a whole page rather than a single row.",
            "The page title steps 32 → 28. Headers' display h1 is a raw font:400 32px/1.1; copying it would grow the shrink-only type debt. 32px is on the ramp but as a single-line COMPONENT composite, and a page title wraps — so it goes to the editorial 28/36. The step down is visible.",
        ]),
    "lockup": dict(
        label="Lock-ups — the question that spans all nine",
        src="notes/_receipts/2026-08-20-210-wave5-laneD-lockups.md · 2026-08-20-210-wave6-lane{C,D}-lockups.md",
        items=[
            "Should each lock-up's arrangements be ONE flexible organism with an arrangement prop, or split into named files? All nine are drawn as one organism each with 3–4 arrangements side by side, so you can see the options together. If you want any split, the split is mechanical — each arrangement block is already self-contained.",
        ]),
}

# ---------------------------------------------------------------------------
# THE 43. Derivation is in the receipt; every row was probed for snippet + meta
# + showroom page before it was written here.
# ---------------------------------------------------------------------------
C = lambda wave, name, slug, kind, row, receipt, cross, qs: dict(
    wave=wave, name=name, slug=slug, kind=kind, row=row, receipt=receipt,
    cross=cross, qs=qs)

COMPONENTS = [
    # ---------------- WAVE 3 (#209) — nine fintech / selection / chrome ----------------
    C("wave 3", "Transaction row", "transaction-row", "Fintech row", "W-63",
      "2026-08-20-209-wave3-laneA-fintech-rows.md", ["w3"], [
        ("⛔ Should this component exist at all? This is the biggest one.",
         "#204 already ruled itinerary row 91 a DUPLICATE of the promoted List-items transaction row. The ledger form — the running-balance column — is the only part List-items does not hold. If the product's statement is a list, this file should be deleted and row 91 marked Duplicate. The live outcome is stated on the file's own face."),
        ("Two money columns, or one signed column?",
         "Both are drawn. Two columns carries the sign STRUCTURALLY — a second, non-colour channel a signed column does not have. One signed column is what a phone width wants."),
        ("What does a pending row show where the balance will be?",
         "Drawn as an em dash with an aria-label, because the balance does not exist until it settles. Nothing, or a projection, are the other readings."),
        ("Should a ledger line be openable — a receipt view?",
         "Drawn passive. Making it interactive re-opens the existence question above."),
      ]),
    C("wave 3", "Standing order / mandate row", "standing-order-mandate-row", "Fintech row", "W-63",
      "2026-08-20-209-wave3-laneA-fintech-rows.md", ["w3"], [
        ("Standing order versus Direct Debit — one component or two?",
         "They are legally and operationally different objects: a customer-controlled fixed instruction versus a payee pulling a variable amount under the Direct Debit Guarantee. The row says which one IN TEXT, in a chip, never by hue. Drawing them in one list does not settle it."),
        ("For a variable Direct Debit, which figure shows?",
         "Drawn: the LAST taken figure, with “Amount varies” in the rhythm line — rather than presenting a stale number as if it were the next one."),
        ("Should a CANCELLED mandate be dimmed at all?",
         "It is not dimmed here because the dimmed version WAS drawn, rendered, and could not be read. If you want dimming, it needs an ink that is legible."),
      ]),
    C("wave 3", "Limits meter", "limits-meter", "Fintech row", "W-63",
      "2026-08-20-209-wave3-laneA-fintech-rows.md", ["w3"], [
        ("⛔ Should this component exist at all?",
         "Progress-bar's own meta already names “savings goal / limits meter” as a common pattern, and the bar here is Progress-bar's, copied byte-for-byte. Three live outcomes: keep it, merge it into Runway-bar as a parameterised “allowance” mode, or delete it and use Progress-bar with a domain aria-valuetext."),
        ("Limits meter versus Runway bar — two components or one?",
         "Runway's maximum is MY OWN BALANCE and its horizon is a date I discover. A limit's maximum is a CAP SET BY THE BANK and its horizon is a repeating reset known in advance. Runway's ceiling is a fact about my money; a limit's ceiling is a rule about my permission. It was drawn to Runway-bar's own anatomy deliberately, so that if you merge them the two files already rhyme."),
        ("Does the meter fill with what is USED, or empty with what REMAINS?",
         "Drawn as USED, like every progress bar. REMAINING — a fuel gauge — is the other honest reading of the word “meter”, and is what “how much do I have left” actually asks."),
        ("The “Per payment” row is a bar that will never fill.",
         "It renders as an empty track reading “£0 of £10,000 used” and always will — a per-payment cap is a ceiling PER EVENT that never accumulates. Left drawn so you can see the oddity rather than read about it. Should it be a bar at all, or a plain stated rule?"),
        ("role=progressbar or role=meter?",
         "Inherited from Runway-bar at #204 and carried forward unchanged. The search was RE-RUN, not cited: zero of 91 pre-existing snippets use role=meter and the rulings store says nothing. If you rule “meter”, both components change together."),
      ]),
    C("wave 3", "Range slider", "range-slider", "Selection control", "W-63",
      "2026-08-20-209-wave3-laneB-selection-controls.md", ["w3"], [
        ("Should crossing the low/high clamp boundary produce a message, or stay a silent clamp?",
         "Built as a silent clamp."),
        ("Should Range-slider inherit Slider's tick-marker idiom, or stay bare?",
         "Built bare. Slider's tick idiom itself carries a deprecated-token finding."),
        ("Is £/GBP the right specimen currency, or should the canonical specimen be currency-neutral?",
         "Built in sterling."),
      ]),
    C("wave 3", "Rating", "rating", "Selection control", "W-63",
      "2026-08-20-209-wave3-laneB-selection-controls.md", ["w3"], [
        ("Filled-star colour — mono ink, or a new warm token?",
         "Built in mono ink, because the store has no gold/amber seat and “no token minting” was on the wave's do-not-rule list."),
        ("Whole stars only, or half-star precision?",
         "Built whole-star-only. Half-stars need a fresh hit-target and keyboard design this pass did not attempt."),
        ("The star target is 32px, not 44px.",
         "Accepted for compact and inline placements. Does Rating need a distinct “roomy” 44px-target variant for a standalone rating page?"),
      ]),
    C("wave 3", "Transfer list", "transfer-list", "Selection control", "W-63",
      "2026-08-20-209-wave3-laneB-selection-controls.md", ["w3"], [
        ("After a move, where does focus go?",
         "Built: it stays on the move button. Following the item into its new panel, or jumping to the panel heading, are the alternatives."),
        ("Is the 280px per-panel scroll cap a real ceiling, or a placeholder?",
         "At scale it needs its own design — search, or virtualisation — which this pass did not attempt."),
        ("Is drag-and-drop wanted alongside checkbox+button?",
         "Built as checkbox+button only, because the itinerary note says just “move-between-lists”."),
      ]),
    C("wave 3", "Split button", "split-button", "Action chrome", "W-63",
      "2026-08-20-209-wave3-laneC-action-chrome.md", ["w3"], [
        ("Should ArrowDown on the MAIN button also open the menu?",
         "Built so only the caret opens it. Opening from the main button is a common APG variant."),
        ("Should a menu item carry a leading icon?",
         "Not drawn."),
        ("Are secondary and quaternary split-button tiers legitimate, or is the control reserved for primary and tertiary emphasis only?",
         "Undecided; only the two emphasis tiers are drawn."),
        ("Is the primary-tier divider hairline visible enough?",
         "It is alpha 24% over the fill. Should it bind a stronger existing token?"),
      ]),
    C("wave 3", "FAB", "fab", "Action chrome", "W-63",
      "2026-08-20-209-wave3-laneC-action-chrome.md", ["w3"], [
        ("Should the FAB deviate from the angular corner rule and render circular?",
         "Most systems that ship a FAB render it circular. Built angular, in house discipline."),
        ("Should a 56px fab size and a 24px floating-chrome offset be minted as tokens?",
         "Or do 56 and 24 stand forever as house-standard raw constants?"),
        ("FAB versus Back-to-top — they collide.",
         "Both are fixed bottom-right. Which wins the corner, or do they stack?"),
        ("Is a non-primary-tier FAB ever legitimate?",
         "Only the primary tier is drawn."),
      ]),
    C("wave 3", "Back to top", "back-to-top", "Action chrome", "W-63",
      "2026-08-20-209-wave3-laneC-action-chrome.md", ["w3"], [
        ("The scroll-distance appearance threshold is entirely unspecified.",
         "The demo uses an arbitrary 200px scrollTop for illustration only — explicitly NOT a proposed default."),
        ("Should the control become focus-reachable below the threshold?",
         "So that keyboard users are never stuck with no way to reach it."),
        ("Should Back-to-top always defer to a FAB present on the same screen?",
         "The corner collision, from the other side."),
        ("Is SECONDARY the single canonical tier?",
         "Built at secondary only."),
      ]),

    # ---------------- WAVE 4 (#210) — the heavy seven ----------------
    C("wave 4", "Calendar", "calendar", "Heavy organism", "W-72",
      "2026-08-20-210-wave4-laneA-calendar-tree.md", ["w4"], [
        ("⛔ Should Date-picker's panel CONSUME this organism? This is the biggest one.",
         "There are now two month grids in the corpus with the same day-cell language and the same keyboard model. Three live outcomes, all real: merge them; keep both and accept the duplication; or delete Calendar and say the month grid only ever exists inside a field. This lane did not edit Date-picker — it is gated and promoted."),
        ("A <table>, or a div grid?",
         "Date-picker builds a div role=grid with display:contents rows. Calendar is a real table role=grid. The table earns its keep twice: a month has genuine two-dimensional relations, and a table-backed grid is static markup every gate can read where a JS-built grid is invisible to all of them — which is precisely how one defect stayed hidden. If you want one house form, this is the moment."),
        ("Should out-of-month days be SELECTABLE?",
         "Drawn: rendered, announced, readable, but not focusable and not clickable — arrows page the month at the edge instead. The other honest reading is that clicking 1 October should jump to October and select it. Also open: should adjacent months show at all, or follow Date-picker and hide?"),
        ("Is a bordered card the right surface for a standalone calendar?",
         "Drawn as a bordered card. Inside a form step it may want no box at all."),
        ("Range selection is NOT DRAWN, deliberately.",
         "Date-range-picker exists. Whether the standalone month should learn ranges — and whether that is one calendar or two side by side — is unasked here."),
        ("Should the selected day carry a weight bump?",
         "It does not, and the reason is mechanical: there is no 16px/500 tabular composite on the ramp. Date-picker gets its weight by a raw declaration, which is one of its nine type violations. Selected therefore carries TWO channels here where Date-picker has three. Either the ramp gains a rung or the calendar stays at two."),
        ("The disabled day is 1.31:1 in light and 4.41:1 in dark.",
         "That is Date-picker's ruled treatment in lock-step, and disabled content is exempt from the contrast minimum. But the asymmetry is stark, and in a min-date calendar it produces a perceptual inversion worth looking at — the out-of-month days of the NEIGHBOURING month read as more available than the disabled days of THIS month."),
        ("Day cells are 40px, not 44px.",
         "148 advisory hit-area findings, against Date-picker's 74 on the same gate the same day. Inherited, not introduced. A 44px cell makes a seven-column month about 340px wide minimum — and it moves both components together."),
      ]),
    C("wave 4", "Tree", "tree", "Heavy organism", "W-72",
      "2026-08-20-210-wave4-laneA-calendar-tree.md", ["w4"], [
        ("Does SELECTION share a mark with CURRENT LOCATION?",
         "Drawn MONO: a hover wash plus a 3px active bar plus aria-selected. Sidebar-nav uses the same bar shape in brand red for aria-current=page. “The node I selected” and “the page I am on” are different meanings. The mono choice asserts nothing — it was made so your ruling is not pre-empted."),
        ("Two twisty idioms now exist.",
         "Sidebar-nav rotates chevron-down 180°; Tree rotates chevron-right 90°, the near-universal disclosure triangle. Both are real library glyphs. One house idiom, or two?"),
        ("Multi-select with checkboxes is NOT DRAWN.",
         "It composes Selection-controls and it changes the ARIA contract — aria-multiselectable, aria-checked, tri-state parents. Left undrawn rather than half-drawn."),
        ("The skeleton bone on a tertiary surface measures 1.05:1 in dark.",
         "Against Skeleton-loader's own 1.11:1. No contrast rule applies to a decorative bone and no token was invented. Should the bone key off its own surface rather than off the page background?"),
        ("Is aria-disabled the right word for “view only”?",
         "The node is readable, announced, and not selectable. aria-disabled is the closest existing vocabulary but it is not exactly what is meant — the same vocabulary strain the switch/thumb ruling names."),
        ("The indent ladder's floor is level 5.",
         "Picked, not derived. Deeper nodes keep level 5's indent rather than marching right. Is 5 the number, and is 24px the step?"),
        ("Tree versus Cascader versus Sidebar-nav.",
         "All three walk a hierarchy. Not adjudicated — the sidebar-nav precedent, and that adjudication is yours. Cascader was built in the same wave by another lane."),
        ("Do the domain semantics survive?",
         "Entity → sub-entity → account, with a child count, a lazily loaded group and a view-only dormant entity. Every one of those is PROPOSED."),
      ]),
    C("wave 4", "Cascader", "cascader", "Heavy organism", "W-73",
      "2026-08-20-210-wave4-laneB-cascader-splitter-qrcode.md", ["w4"], [
        ("⛔ Do Tree and Cascader both exist? This is the structural one.",
         "A tree DISCLOSES a hierarchy in place and can hold many branches open; a cascader SELECTS one path and shows one branch per level. Same data, different jobs. Both were built in the same wave. The relationship is stated in both metas and adjudicated in neither. Live outcome: if they merge, one of the two files should not exist."),
        ("Which ARIA mapping?",
         "Two exist and only one is drawn. Drawn: a chain of listbox columns with roving tabindex and a polite whole-path readout — matching the layout the eye sees and the keys the user presses. Not drawn: one role=tree spanning all columns via aria-owns — matching the DATA, and what a user who thinks in hierarchies may expect. Neither is obviously right."),
        ("Is the trigger a combobox?",
         "Drawn as a plain button with aria-expanded, deliberately not role=combobox: a combobox promises one popup of one type and this popup is several listboxes. Claiming semantics we do not implement is the worse lie — but it is a call."),
        ("Leaf-only, or any node selectable?",
         "Drawn leaf-only. Any-node needs a second affordance — a commit control, or a modifier — so that OPENING and CHOOSING stay distinct, and that affordance is not drawn."),
        ("Which layout is the default, and at what width?",
         "Columns and stacked are both built and they are the same code; the automatic switch is a 420px container query. The number is picked, not derived."),
        ("The panel reserves an empty column slot.",
         "With fixed 220px columns, a two-column state leaves visible empty space to the right of the last column. The alternative is a panel that grows and shrinks as you drill — no dead space, but the panel's right edge moves. Drawn: reserve. It reads as “there is room for the next level”; it may read as a bug."),
        ("Should a passing cursor open a branch?",
         "Drawn: no — expansion is click, Enter or Right only. Hover-to-expand is pointer-only and leaves keyboard and touch with no equivalent."),
      ]),
    C("wave 4", "Splitter", "splitter", "Heavy organism", "W-73",
      "2026-08-20-210-wave4-laneB-cascader-splitter-qrcode.md", ["w4"], [
        ("⛔ Is aria-valuenow a percentage or pixels?",
         "Drawn as a percentage. Pixels are the other honest reading — they are what the user is dragging, and they would let the min and max carry the real fences. This changes what a screen-reader user hears on every keypress."),
        ("24px or 44px?",
         "The divider's pointer target is 24px while the drawn rule is 8px. The hit-area advisory names it four times. Raising it to 44px means a 44px-wide invisible grab band between two panes — the same inherited-restraint call the gated Tags chip makes. Flagged, never silently raised."),
        ("Does the resting seam need to clear 3:1?",
         "It measures 1.31:1 in light and is deliberately NOT declared as a contrast pair, because a resting seam is decoration and the control's perceptibility rests on the grip, the hover darkening, the cursor, the focus ring and the published value. Moving it to a form border would change EVERY seam in the library."),
        ("Does a collapsed pane keep an 8px band, or become a re-open affordance?",
         "Drawn: it keeps the 8px separator, so there is always a way back. A 24px “re-open” tab is the other answer."),
        ("Should a splitter collapse to a stacked layout below some width?",
         "At 480px the panes measure 215px and 160px — both fences honoured, both cramped. No collapse is drawn."),
        ("Is the orientation naming right?",
         "data-orientation=horizontal means panes side by side, divided by a VERTICAL bar — which is what aria-orientation then says. The trap is real and the file states the reading on its own face so it can be refused."),
      ]),
    C("wave 4", "QR code", "qr-code", "Heavy organism", "W-73",
      "2026-08-20-210-wave4-laneB-cascader-splitter-qrcode.md", ["w4"], [
        ("⛔ What does a QR code do in dark mode? The biggest one — and it is MEASURED.",
         "Fixed plate keeps a white plate in every theme and DECODED. Theme-following inverts and DID NOT DECODE, with the same pixels decoding perfectly once flipped back. Fixed plate is a bright square inside a dark surface. Theme-following is what a dark UI wants to look like. This is a product-risk decision as much as a visual one."),
        ("Which error-correction level?",
         "Level M throughout. L, Q and H are all legal and the choice trades symbol size against damage tolerance."),
        ("A centre logo or lockup?",
         "Not drawn. It would REQUIRE level H, and it touches the dv-lockup work. Named, not begun."),
        ("Which payment-QR standard, if any?",
         "The second specimen is a plain-text demonstration string and is deliberately NOT an EPC/SEPA payload. The snippet says so twice, on its own face. Which standard a real payment QR carries is a product question."),
        ("Are 4 / 8 / 12px the right module sizes?",
         "Small is drawn deliberately at the edge of what ordinary phone cameras resolve at reading distance. The ramp is picked, not derived."),
        ("Where does the QR generator live?",
         "The matrices were computed by a lane-local encoder that is NOT in the repo. As shipped the snippet is a static artefact, and changing the payload means re-running a tool nobody else has. Homing that generator in-repo is a real decision with a real cost."),
      ]),
    C("wave 4", "Carousel", "carousel", "Heavy organism", "W-71",
      "2026-08-20-210-wave4-laneC-carousel-imageblock.md", ["w4"], [
        ("Should an opt-in autoplay variant exist at all?",
         "Not built. Proposed default: no autoplay, ever, given the Pause/Stop/Hide requirement and the mixed record of autoplaying carousels. If you want one it needs a visible pause control and a paused-on-focus rule at minimum — none of that is drawn."),
        ("Standard versus peek/snap — one default and one variant, or two different components?",
         "Drawn as two variants of one component because they share the same dot and arrow control row and the same slide markup; only the viewport mechanics differ. If you read them as answering different questions — a “rotator” versus a “reveal strip” — they may deserve separate names."),
        ("The carousel arrow glyph is hand-drawn, not byte-matched.",
         "The library chevrons exist and were considered, but their path data is a filled multi-point chevron shaped for a different stroke weight than the simple 2px-stroke arrow drawn here. This is a DEVIATION from the wave's byte-match instruction for icons, and it is named rather than hidden. Swap to the library chevron, or keep the drawn stroke and decide whether it should become a new icon-library asset."),
        ("Dot size: an 8px dot with a 44px invisible target, or a visibly larger dot?",
         "Drawn small-with-invisible-target, borrowing Segmented-control's hit-area idiom. A visibly bigger dot reads heavier and competes with the slide content."),
        ("Does the live-region text need the slide's TITLE, or is “Slide N of M” enough?",
         "Drawn terse, to avoid double-announcing content a sighted user already sees change. A screen-reader user gets no title in the live region — only on the next Tab into the slide body."),
        ("Should the peek carousel's neighbour-peek width be a token?",
         "Left as a bare calc(). No spacing token currently names “the amount a carousel should peek by”."),
      ]),
    C("wave 4", "Image block", "image-block", "Heavy organism", "W-71",
      "2026-08-20-210-wave4-laneC-carousel-imageblock.md", ["w4"], [
        ("Is 16:9 / 4:3 / 1:1 / 3:4 the right set, or does the library want a named CROP vocabulary?",
         "Drawn as raw ratios, matching how aspect-ratio is actually authored in CSS. A named vocabulary — hero, card, avatar, portrait — would be a thin wrapper on top and is not built here."),
        ("Attribution is optional and independent of caption — is that the right pairing?",
         "Drawn independent. Three of four combinations are demonstrated; attribution-only-without-caption is NOT drawn, and whether it should even be legal is open. Should a bare photo credit ever appear floating alone?"),
      ]),

    # ---------------- WAVE 5 (#210) — Layer-2 P2: 3 shells + 6 templates + 2 lock-ups ----------------
    C("wave 5", "App shell · top nav", "app-shell-top-nav", "App shell", "W-78",
      "2026-08-20-210-wave5-laneA-app-shells.md", ["shell"], [
        ("Inline or stacked as the product's default top nav?",
         "Both are drawn. Nothing picks one."),
        ("The trail at phone width.",
         "Drawn: ancestors drop. An ellipsis disclosure, or a single “Back to <parent>” link, are the alternatives."),
        ("Should Breadcrumbs itself grow 44px targets?",
         "Its links measure 10.1px tall today — the leading-trim cap box IS the link box. The shell grew them; the gated parent still has none."),
      ]),
    C("wave 5", "App shell · side nav", "app-shell-side-nav", "App shell", "W-78",
      "2026-08-20-210-wave5-laneA-app-shells.md", ["shell"], [
        ("The three new rail rules — should they go back into the GATED PARENT?",
         "They arguably belong there. A worker lane could not touch a gated file to find out."),
        ("The Sidebar-nav / Navigations overlap, carried open from #203.",
         "This shell consumes both. Whatever you rule, the composition is unaffected."),
        ("The rail tooltip, carried open from #203.",
         "A rail item has no visible name."),
        ("The three-way collapse precedence.",
         "Drawn as: the query sets the default, the user's toggle overrides inside the band where both states are legal, the narrowest band wins outright. Confirm or overturn."),
      ]),
    C("wave 5", "App shell · multi-column", "app-shell-multi-column", "App shell", "W-78",
      "2026-08-20-210-wave5-laneA-app-shells.md", ["shell"], [
        ("⛔ THE SELECTED LIST ROW.",
         "List-items models no selected state at all. The row here is Sidebar-nav's nav link, borrowed for its three “you are here” carriers. Live outcomes: keep the borrow, give List-items a selected state, or make the list a role=listbox."),
        ("aria-current=true or aria-selected for a master-list row?",
         "Two different meanings, one drawn."),
        ("What does the detail pane show BEFORE a row is chosen?",
         "Drawn pre-selected, which quietly makes a choice for the user. Empty-state exists and is the alternative."),
        ("Does choosing a row change the URL?",
         "Drawn as a pane swap with no history entry, so the browser back button leaves the shell. On a phone that is very likely wrong."),
      ]),
    C("wave 5", "Template · dashboard", "template-dashboard", "Template", "W-77",
      "2026-08-20-210-wave5-laneB-templates.md", ["tpl"], [
        ("Four KPIs — and which four?",
         "Four is drawn because the auto-fill grid reflows 4 → 3 → 1 and that is the collapse worth proving. Which four figures a business overview leads with is a product decision."),
        ("Should Data-grid consume Pagination?",
         "Data-grid re-states the pager recipe internally; Pagination is a gated component. The list template consumes the COMPONENT, the dashboard uses Data-grid's own — so both are visible on the same day. A duplication, surfaced, not adjudicated."),
        ("The horizontal-bar chart cannot be used without its engine.",
         "Composed first, rejected by LOOKING: its left category labels clip to “oceries” / “nsport” / “ousing” because the fit is a runtime measurement. A static composition must choose a specimen that does not need the engine — worth knowing before anyone composes a chart into a shell."),
      ]),
    C("wave 5", "Template · list / index", "template-list-index", "Template", "W-77",
      "2026-08-20-210-wave5-laneB-templates.md", ["tpl"], [
        ("⛔ Table or list? This is the whole point of the page.",
         "The library holds both answers and they are not interchangeable: a table carries relations BETWEEN rows — sort order, page-scoped selection, a column you read downwards; a list carries one record and a tap target. BOTH ARE DRAWN, with the same filters, the same five records and the same pager, so the choice is made by eye. Whichever you pick, the other half of the file is deleted."),
        ("Which control is a filter facet?",
         "Drawn as native selects wearing Data-grid's own chrome. Dropdown, Multi-select, Combobox and Date-range-picker all exist and all carry popup behaviour; hosting one would fork it. The native select is an honest placeholder, not a recommendation."),
        ("“Failed” sits on the ERROR seat here.",
         "That is a step beyond wave 3's declared restraint, which put “failed” on WARNING. It is on error because on a payments index a failed payment is the thing you came to find. That is a judgement, it is visible, and it touches the two-red law's neighbourhood — so it is stated as a change of position, not slipped in."),
      ]),
    C("wave 5", "Template · detail", "template-detail", "Template", "W-77",
      "2026-08-20-210-wave5-laneB-templates.md", ["tpl"], [
        ("The four-part order — identity, facts, history, documents.",
         "And the decision to put documents in a RAIL rather than in a tab. Both PROPOSED."),
        ("Document titles ellipsize in a 280px rail.",
         "At full desktop width “Invoice INV-2026-0871” renders at 134px with an ellipsis, and the full string exists only in the download button's label. That is Document-row's designed truncation meeting a 280px rail. Should the rail be wider when it hosts document rows, or should a truncated link carry a title attribute?"),
        ("A status chip inside a stretched-link row swallows the click at its own coordinates.",
         "Hit-tested: the point at the centre of the “Remittance advice” row lands on the chip, because Document-row raises the chip above the row's click overlay. Inherited, minor, reported rather than patched."),
      ]),
    C("wave 5", "Template · create / edit", "template-create-edit", "Template", "W-76",
      "2026-08-20-210-wave5-laneC-form-templates.md", ["tpl"], [
        ("Is “unsaved changes” a WARNING?",
         "Drawn as ink on a hover wash with the WORD “Unsaved” carrying the meaning — deliberately not the warning seat, which touches the two-red law and was not this lane's to touch."),
        ("Should the template LOCK the account fields, as drawn?",
         "Drawn locked with the reason in help text — changing where money goes is a verified journey, not a field edit. That is a PRODUCT POLICY dressed as a layout decision."),
        ("Where does the guidance aside end and a help pattern begin?",
         "Drawn as read-only guidance in a definition list. Any control in there competes with the form for the same decision. Is an aside even the right home for this content?"),
        ("Two of the four review-row values are tabular and two are not.",
         "Amount and Date are tabular; To and Reference are not. Reasonable, unruled."),
        ("Does this page's app bar overlap the Page-header lock-up?",
         "Both were built in the same session, concurrently. The template borrows Headers' content-header verbatim; the other lane built Page-header-lockup. The relationship is stated PROPOSED and adjudicated nowhere — the sidebar-nav-versus-navigations shape, one layer up."),
      ]),
    C("wave 5", "Template · wizard", "template-wizard", "Template", "W-76",
      "2026-08-20-210-wave5-laneC-form-templates.md", ["tpl"], [
        ("⛔ Should this template exist at all? The biggest one.",
         "Stepper is already an interactive wizard. The receipt states exactly what the template adds, and states the live outcome: delete the pair and mark itinerary row 109 DUPLICATE against the stepper component."),
        ("The step visuals now live in THREE files.",
         "Progress-tracker → Stepper → this template. Stepper's own receipt already flagged the duplication at two and queued the fold-or-partial question. This lane made it three and is saying so. The auto-partial mechanism exists for exactly this."),
      ]),
    C("wave 5", "Template · auth", "template-auth", "Template", "W-76",
      "2026-08-20-210-wave5-laneC-form-templates.md", ["tpl"], [
        ("Does the library adopt the <img> idiom for brand assets?",
         "This is the first gated snippet with a src-bearing image. Inlining was rejected on a MEASUREMENT, not a taste: the icon gate byte-matches against the icons folder only, so an inlined logo lands as UNKNOWN — indistinguishable from an invented mark. Two live outcomes: adopt <img> for logos and possibly widen the icon gate to see a logos folder, or mint a logos sprite the way icons have one."),
        ("Should the auth brand column carry anything but the mark?",
         "It is deliberately quiet — the mark and one neutral line — because inventing brand imagery is fenced. At wide widths it is a large empty plate. Fill it, narrow it, or drop the split entirely?"),
        ("Should password requirements be a live tick/cross meter?",
         "Drawn as plain ink list items stated BEFORE the field and kept visible. A live meter needs a met / unmet / partially-met vocabulary this lane had no mandate to mint."),
      ]),
    C("wave 5", "Page-header lock-up", "page-header-lockup", "Lock-up", "W-75",
      "2026-08-20-210-wave5-laneD-lockups.md", ["lockup"], [
        ("Does a page header ever need a SECOND action beyond “primary plus one other”?",
         "Only two-button rows are drawn — all three arrangements show exactly two. A row with three or more actions would need its own overflow treatment, echoing Tabs' “More”, which nothing here builds."),
      ]),
    C("wave 5", "Filter toolbar bar", "filter-toolbar-bar", "Lock-up", "W-75",
      "2026-08-20-210-wave5-laneD-lockups.md", ["lockup"], [
        ("Is two filters the right default, or should it be N?",
         "Drawn with exactly two — Account and Date range. A filter count is named as a prop but only the two-filter case is drawn; a three-plus filter row's wrap behaviour at 680px is UNDRAWN."),
        ("Should the compact toolbar ever carry filter dropdowns, or is it search-plus-sort by definition?",
         "Drawn as search-plus-sort only, matching the itinerary row's own note implying a dense secondary bar. If a dense row needs a filter too, that composition is undrawn."),
        ("Should the applied-filter chip ROW carry a group role?",
         "Tags ships a plain label per dismiss button with no group role wrapping the row. Whether the row should carry role=group labelled “Applied filters” is undrawn and untouched — Tags' own accessibility section does not call for it either."),
        ("Is a per-instance aria-label the right accessible name for a toolbar-embedded segmented control?",
         "Drawn with the same per-instance pattern Segmented-control's own reference uses — no new pattern invented, but not validated against a toolbar's landmark structure."),
      ]),

    # ---------------- WAVE 6 (#210) — Layer-2 P3: 4 shells + 5 templates + 7 lock-ups ----------------
    C("wave 6", "App shell · split", "app-shell-split", "App shell", "W-83",
      "2026-08-20-210-wave6-laneA-p3-shells.md", ["shell"], [
        ("Should Splitter's separator grow to 44px?",
         "Its hit band is 24px on an inherited-restraint argument; every other control this repo ships is 44."),
        ("Should the --axis custom-property pattern go back into Splitter?",
         "It is strictly more general than reading the attribute once."),
      ]),
    C("wave 6", "App shell · focused", "app-shell-focused", "App shell", "W-83",
      "2026-08-20-210-wave6-laneA-p3-shells.md", ["shell"], [
        ("⛔ WHAT DOES THE ONE EXIT DO?",
         "The central question of this shell and deliberately unanswered. Does “Save and exit” save a draft? Does “Exit” on a half-finished payment discard it? Does it need a Popconfirm or a Modal? The library has both."),
        ("⛔ ONE PROGRESS STATEMENT PER SCREEN.",
         "This shell's band and Template-wizard's step rail both say where you are. Hosted together they say it twice, in two vocabularies. Drawn as: the shell owns the band, a hosted rail is decorative. This must be ruled ONCE for the library, not per file."),
        ("The brand in INK rather than red.",
         "Diverging from Navigations and from App-shell-top-nav. Confirm or overturn."),
      ]),
    C("wave 6", "App shell · doormat", "app-shell-doormat", "App shell", "W-83",
      "2026-08-20-210-wave6-laneA-p3-shells.md", ["shell"], [
        ("Is the masthead cap of FOUR the rule?",
         "The whole doormat shell rests on it, and the number is not measured from anything."),
        ("Is the doormat NAVIGATION or END MATTER?",
         "This shell says navigation — a stronger claim than Footer's own meta makes. If navigation, it arguably wants one <nav> around the whole mat."),
        ("This shell carries TWO thresholds from two different owners.",
         "900/600 are the shell's; 560 is Footer's. Neither is ruled, and they are now in the same file."),
      ]),
    C("wave 6", "App shell · nav rail", "app-shell-nav-rail", "App shell", "W-83",
      "2026-08-20-210-wave6-laneA-p3-shells.md", ["shell"], [
        ("⛔ THE TWO-CONTRACT FLYOUT RULE.",
         "A flyout that repeats a name is decorative and hidden; a flyout that offers destinations is a disclosure and announced. Same pixels, opposite markup. This is the shell's central proposal and it answers the #203 rail-tooltip question — which may not be the answer you want: a real Tooltip, or permanent micro-labels, or accepting that a rail is for experts, are all live alternatives."),
        ("⛔ THE PHONE BAR NEEDS A SHORT-NAME CONVENTION OR A CAP — and this is measured.",
         "Four short names fit a 390px bar with ZERO truncation. Five names including “Payments and transfers” truncate to 62px boxes and read as “Overv… Acco… Paym… Cards Spen…”. The library has no short-name convention. Options: mint one, cap at four with a “More” disclosure the way Tab-bar does, or make the phone form BE Tab-bar."),
        ("A 64px rail head is the hardest place in the library to put a brand mark.",
         "The unbound brand mark question, at its sharpest."),
      ]),
    C("wave 6", "Template · settings", "template-settings", "Template", "W-82",
      "2026-08-20-210-wave6-laneB-p3-templates.md", ["tpl"], [
        ("The section vocabulary, and what belongs on it.",
         "Your details / Notifications / Statements and documents / Security are all PROPOSED. So is locking the customer number with a reason in help text rather than hiding it, and choosing the INFORMATION seat (not warning) for the “two changes not yet saved” chip — deliberately not the warning seat, which touches the two-red law."),
        ("At 420px the action bar is no longer the last thing on the page.",
         "When the split collapses, the rail stacks BELOW the form, so “Save settings” sits above “On this page”. Measured: the sticky bar rests 457.8px above the frame bottom at scroll-end. Arguably correct — in-page navigation belongs near the top on a phone — and arguably wrong."),
      ]),
    C("wave 6", "Template · empty", "template-empty", "Template", "W-82",
      "2026-08-20-210-wave6-laneB-p3-templates.md", ["tpl"], [
        ("This page composes Empty-state and adds no question of its own.",
         "Its open questions are the cross-cutting Layer-2 ones above — chiefly the artefact class, the missing composition edge, and whether a template ships any JavaScript."),
      ]),
    C("wave 6", "Template · error", "template-error", "Template", "W-82",
      "2026-08-20-210-wave6-laneB-p3-templates.md", ["tpl"], [
        ("⛔ Should an error page carry a RAG colour at all — and is that even a template's question?",
         "Not one RAG token is bound anywhere in that file, and it is the single biggest judgement in the delivery. The reasoning is on the file's own face: a form error names a field the person can fix and the red carries that instruction — A 404 HAS NO FIELD. Painting a whole page with the error seat sits squarely in the two-red law's neighbourhood and the mono error-ink camp's. The anchor is a decorative 48px glyph at 40% alpha and the HEADING carries the meaning. Live outcome either way: if you rule that an error page takes the error seat, one line changes; if you rule it does not, this becomes the precedent for every error surface."),
        ("Should an error page offer a support route at all?",
         "The do-not-rule list was obeyed to the letter: no phone number, no chat link, no “contact us”, no promise anyone is looking, no service-status claim. A neutral reference code is shown and NOTHING is asserted about what it is for — which is arguably worse than showing nothing. That is a product decision."),
        ("This is the one template that assumes it may be served OUTSIDE the shell.",
         "So it carries its own minimal masthead, where the other ten assume they sit inside a main region."),
      ]),
    C("wave 6", "Template · report", "template-report", "Template", "W-82",
      "2026-08-20-210-wave6-laneB-p3-templates.md", ["tpl"], [
        ("⛔ Do reports need a NARROW chart specimen?",
         "The arithmetic says two 580px canvases cannot sit side by side in a 1120px page AT ANY WIDTH. A report that wants two charts abreast needs a second canvas width IN THE CHART COMPONENTS THEMSELVES. That is a dataviz decision and it is bigger than this template."),
        ("⛔ What does a template do about a byte-lifted chart's DEMO DATA?",
         "Borrow verbatim for provenance and the chart lies about the page; change the labels and the byte-diff weakens. This lane split the difference — geometry byte-identical, copy replaced, both stated. Is that the rule? And separately, Template-dashboard still ships the contradiction."),
        ("The five leading figures, the four provenance fields and the four footnotes.",
         "Which figures a settlement report leads with, and what a report must state about its own provenance, are product decisions dressed as layout."),
      ]),
    C("wave 6", "Template · confirmation", "template-confirmation", "Template", "W-82",
      "2026-08-20-210-wave6-laneB-p3-templates.md", ["tpl"], [
        ("⛔ Should a PENDING confirmation get a roundel of its own?",
         "Confirmation's 56px roundel is built for a TICK: its mark is a page cutout, and the entire dark policy — white shape, black mark — exists so that cutout stays legible. There is NO ruled roundel for “accepted but not finished”. Minting one would be a decision inside the RAG policy's own neighbourhood, so the pending variant takes no success device at all — a decorative glyph plus a status chip carrying the word."),
      ]),
    C("wave 6", "Section-heading lock-up", "section-heading-lockup", "Lock-up", "W-81",
      "2026-08-20-210-wave6-laneC-lockups.md", ["lockup"], [
        ("Is a bare <h2> always the right level, or does this lock-up need an explicit level prop?",
         "Drawn as h2 throughout. A section nested under another section — inside a split panel, say — may need h3 for correct heading order. Undrawn, left to the consuming page."),
      ]),
    C("wave 6", "Card-header lock-up", "card-header-lockup", "Lock-up", "W-81",
      "2026-08-20-210-wave6-laneC-lockups.md", ["lockup"], [
        ("Does the overflow-menu ARIA deviation need its own named pattern, or should Dropdown grow a “menu mode”?",
         "Drawn as a declared one-off deviation — role=menu where Dropdown uses role=listbox. If overflow menus recur elsewhere in the system, and they likely will on every card and every table row, a shared “Action-menu” atom might be the better long-term home rather than each consumer re-declaring the deviation. Not built here."),
      ]),
    C("wave 6", "Hero variants", "hero-variants", "Lock-up", "W-81",
      "2026-08-20-210-wave6-laneC-lockups.md", ["lockup"], [
        ("Should Hero itself gain a ramp-legal FLUID composite?",
         "The type-ratchet fix traded Hero's fluid clamp() scaling for a fixed composite size. That is a real, if small, visual change from Hero's own baseline. If fluid headline scaling matters, the right fix is a new canon composite — which is the design system owner's call, not this lock-up's."),
        ("Is “no text over the image” the right permanent answer?",
         "Variant B deliberately sidesteps Hero's own flagged scrim question rather than resolving it. If a scrim IS wanted, someone still owes a guaranteed-contrast treatment that is not derivable from tokens — Hero's own words."),
        ("Should the two-button pair ever also carry the arrow link, as a THIRD action?",
         "Deliberately not drawn. Undrawn territory."),
      ]),
    C("wave 6", "Stats-band lock-up", "stats-band-lockup", "Lock-up", "W-81",
      "2026-08-20-210-wave6-laneC-lockups.md", ["lockup"], [
        ("Does the KPI-tile board arrangement ship the inherited two-seat colour question, or wait for it?",
         "Carried unchanged from Kpi-tile's own header — the fill-seat versus ink-seat divergence is visible in this lock-up's own dark render, where the flat tile's spark renders white ink. Not resolved here; Stat-card and Kpi-tile must move together per Kpi-tile's own instruction."),
      ]),
    C("wave 6", "Footer doormat lock-up", "footer-doormat-lockup", "Lock-up", "W-80",
      "2026-08-20-210-wave6-laneD-lockups.md", ["lockup"], [
        ("Is this the right SHAPE for the row, or should the lock-up ADD content beyond Footer's own doormat?",
         "It composes Footer's doormat 100% verbatim, adding only a page-context stub. A real mega-footer sometimes carries more — a newsletter sign-up row, app-store badges, a language switcher, social icons. None of those atoms exist as gated components today, so nothing was invented to fill the gap. If your mental model of “the full mega-footer arrangement” includes them, this lock-up under-delivers on the row's own name."),
        ("The band sits on the subtle surface — is that right?",
         "Carried from Footer's own open question rather than resolved. The CTA lock-up asks the same question from the other side."),
      ]),
    C("wave 6", "CTA lock-up", "cta-lockup", "Lock-up", "W-80",
      "2026-08-20-210-wave6-laneD-lockups.md", ["lockup"], [
        ("Should a CTA band ever carry a SINGLE button instead of a pair?",
         "Both arrangements draw exactly a secondary-plus-primary pair. A band with one action — a plain “Get started” with no “Learn more” — is a common pattern this file does not draw."),
        ("Should a CTA band read as the same neutral family as a footer band?",
         "Both sit on the subtle surface. Whether a CTA band should instead be visually distinct — on the page background with only a rule to separate it — is unexamined here."),
        ("Should the split arrangement force left alignment?",
         "Between roughly 560 and 600px the title block and button pair wrap by ordinary flex flow, not by the container override, and that can read as similar to the centred variant when the heading is long. Acceptable incidental behaviour, or does it need an explicit mid-width rule?"),
      ]),
    C("wave 6", "Feature-grid lock-up", "feature-grid-lockup", "Lock-up", "W-80",
      "2026-08-20-210-wave6-laneD-lockups.md", ["lockup"], [
        ("Is omitting per-cell actions always right?",
         "Drawn deliberately WITHOUT a per-cell button, on the theory that the CTA lock-up carries the call to action and a feature grid states benefits. Some real marketing patterns do put a “Learn more” link on each card. If you want it, Cards' own arrow-link atom is the obvious source and the composition would be additive, not a rebuild."),
        ("The icon choices are illustrative, not semantic.",
         "Four plausible retail-banking benefit icons were picked because the itinerary named no specific benefits. The COPY paired with each — security, mobile, insights, global reach — is equally illustrative. Both are yours to replace against an actual feature set."),
      ]),
]

WAVE_META = {
    "wave 3": dict(session="#209", rows="W-63 (open, yours) · W-62 (the brief + receipts)",
                   blurb="Nine fintech rows, selection controls and action chrome. Two of the nine carry an EXISTENCE question — whether the component should exist at all."),
    "wave 4": dict(session="#210", rows="W-71 · W-72 · W-73 · W-74 (all open, yours)",
                   blurb="The heavy seven. Five defects were found in already-GATED components while building these, every one under a green gate chain."),
    "wave 5": dict(session="#210", rows="W-75 · W-76 · W-77 · W-78 · W-79 (all parked, yours)",
                   blurb="Layer-2, first pass: three app shells, six page templates, two lock-ups. The artefact-class convention itself is PROPOSED here."),
    "wave 6": dict(session="#210", rows="W-80 · W-81 · W-82 · W-83 · W-84 (all parked, yours)",
                   blurb="Layer-2, second pass: four more shells, five more templates, seven lock-ups. Six defects found by driving, every gate green over all six."),
}

E = html.escape


def build():
    waves = ["wave 3", "wave 4", "wave 5", "wave 6"]
    by_wave = {w: [c for c in COMPONENTS if c["wave"] == w] for w in waves}
    total = len(COMPONENTS)
    assert total == 43, "component count changed: %d" % total

    parts = []
    parts.append(HEAD)

    # ---- masthead -------------------------------------------------------
    parts.append('<header class="mast">')
    parts.append('<div class="mast-in">')
    parts.append('<p class="kicker">Review surface · session #213 · lane R</p>')
    parts.append('<h1>The 43 components you have not seen yet</h1>')
    parts.append(
        '<p class="lede">Everything built in waves 3, 4, 5 and 6 &mdash; nine fintech and control components '
        'from #209, the heavy seven from #210, and the twenty-seven Layer-2 shells, templates and lock-ups. '
        '<strong>Every one of them ships PROPOSED-NOT-RULED and is waiting on your eye.</strong> '
        'Each specimen below is the component’s own generated showroom page, live in this document &mdash; '
        'not a copy, not a redraw. Switch theme and mode at the top and every open specimen follows.</p>')
    parts.append(
        '<p class="lede"><strong>Nothing on this page is a ruling.</strong> The controls record what you say '
        'and give it back to you as text you can paste. They write nothing into the store.</p>')

    parts.append('<div class="counts">')
    for w in waves:
        parts.append('<a class="cnt" href="#%s"><strong>%d</strong><span>%s</span></a>'
                     % (w.replace(" ", "-"), len(by_wave[w]), E(w)))
    parts.append('<span class="cnt tot"><strong>%d</strong><span>in total</span></span>' % total)
    parts.append('</div>')
    parts.append('</div></header>')

    # ---- sticky control bar --------------------------------------------
    parts.append('<div class="bar" id="bar"><div class="bar-in">')
    parts.append('<span class="bl">Theme</span><span class="seg" id="segTheme">')
    for attr, label in THEMES:
        parts.append('<button type="button" data-theme="%s"%s>%s</button>'
                     % (attr, ' aria-pressed="true"' if attr == "mono" else ' aria-pressed="false"', E(label)))
    parts.append('</span>')
    parts.append('<span class="bl">Mode</span><span class="seg" id="segMode">'
                 '<button type="button" data-mode="light" aria-pressed="true">Light</button>'
                 '<button type="button" data-mode="dark" aria-pressed="false">Dark</button></span>')
    parts.append('<span class="bl">Width</span><span class="seg" id="segW">'
                 '<button type="button" data-w="390" aria-pressed="false">390</button>'
                 '<button type="button" data-w="768" aria-pressed="false">768</button>'
                 '<button type="button" data-w="1280" aria-pressed="false">1280</button>'
                 '<button type="button" data-w="full" aria-pressed="true">Full</button></span>')
    parts.append('<span class="bar-sp"></span>')
    parts.append('<button type="button" class="bbtn" id="openAll">Open all</button>')
    parts.append('<button type="button" class="bbtn" id="closeAll">Close all</button>')
    parts.append('<button type="button" class="bbtn prim" id="exportBtn">Export rulings <span class="pill" id="ruledN">0</span></button>')
    parts.append('</div></div>')

    parts.append('<main>')

    for w in waves:
        m = WAVE_META[w]
        parts.append('<section class="wave" id="%s">' % w.replace(" ", "-"))
        parts.append('<div class="wave-hd">')
        parts.append('<h2>%s <span class="wc">%d components</span></h2>' % (E(w.title()), len(by_wave[w])))
        parts.append('<p class="wsub">Built in session %s. Store rows: <span class="jk">%s</span></p>'
                     % (E(m["session"]), E(m["rows"])))
        parts.append('<p class="wblurb">%s</p>' % E(m["blurb"]))
        parts.append('</div>')

        # cross-cutting blocks that first apply in this wave
        shown = []
        for c in by_wave[w]:
            for k in c["cross"]:
                if k not in shown:
                    shown.append(k)
        for k in shown:
            first_wave = next(cc["wave"] for cc in COMPONENTS if k in cc["cross"])
            if first_wave != w:
                continue
            x = CROSS[k]
            parts.append('<details class="xcut"><summary><span class="xtag">Rule once</span> %s '
                         '<span class="xn">%d questions</span></summary><ol class="qs">' % (E(x["label"]), len(x["items"])))
            for it in x["items"]:
                parts.append('<li>%s</li>' % E(it))
            parts.append('</ol><p class="src jk">%s</p></details>' % E(x["src"]))

        for c in by_wave[w]:
            parts.append(card(c))
        parts.append('</section>')

    parts.append('</main>')

    # ---- export dialog --------------------------------------------------
    parts.append('''
<div class="ovl" id="ovl" hidden>
  <div class="sheet" role="dialog" aria-modal="true" aria-labelledby="shTitle">
    <h2 id="shTitle">Your rulings, as text</h2>
    <p class="shp">Copy this and paste it back into the session. Nothing here has been written anywhere.</p>
    <textarea id="exportTa" readonly rows="18" spellcheck="false"></textarea>
    <div class="shb">
      <button type="button" class="bbtn prim" id="copyBtn">Copy to clipboard</button>
      <button type="button" class="bbtn" id="closeSheet">Close</button>
    </div>
  </div>
</div>''')

    parts.append('<footer class="foot"><p>Generated by <code>knowledge/_render/gen_review_213_wave_components.py</code> '
                 '&mdash; 2026-08-21, session #213, lane R. Specimens are live iframes of <code>showroom/&lt;slug&gt;.html</code>; '
                 'no component markup is copied into this page. Receipt: '
                 '<code>notes/_receipts/2026-08-21-213-laneR-review-surface.md</code>.</p></footer>')

    parts.append(SCRIPT.replace("__DATA__", json.dumps(
        [dict(slug=c["slug"], name=c["name"], wave=c["wave"], row=c["row"]) for c in COMPONENTS])))
    parts.append("</body>\n</html>\n")
    return "\n".join(parts)


def card(c):
    qn = len(c["qs"])
    p = []
    p.append('<article class="cmp" id="c-%s" data-slug="%s">' % (c["slug"], c["slug"]))
    p.append('<div class="chd">')
    p.append('<div class="cnm"><h3>%s</h3><span class="kind">%s</span></div>' % (E(c["name"]), E(c["kind"])))
    p.append('<div class="cmeta jk">row %s &middot; <code>%s</code> &middot; <code>notes/_receipts/%s</code></div>'
             % (E(c["row"]), E("knowledge/snippets/%s" % snippet_name(c["slug"])), E(c["receipt"])))
    p.append('<div class="cst"><span class="badge prop">Proposed &mdash; not ruled</span>'
             '<span class="badge qn">%d open question%s</span>'
             '<span class="verdict" data-for="%s"></span></div>' % (qn, "" if qn == 1 else "s", c["slug"]))
    p.append('</div>')

    # questions
    p.append('<div class="cbody">')
    p.append('<div class="qcol"><h4>What is open, in plain words</h4><ol class="qs big">')
    for head, body in c["qs"]:
        p.append('<li><strong>%s</strong> %s</li>' % (E(head), E(body)))
    p.append('</ol>')
    if c["cross"]:
        labels = " &middot; ".join(E(CROSS[k]["label"]) for k in c["cross"])
        p.append('<p class="src">Also governed by the rule-once blocks above: %s</p>' % labels)
    p.append('</div>')

    # decision control
    p.append('<div class="dcol"><h4>Your ruling</h4>')
    p.append('<div class="opts" role="group" aria-label="Ruling for %s">' % E(c["name"]))
    for val, lab in (("promote", "Promote"), ("rework", "Rework"), ("delete", "Delete"), ("defer", "Defer")):
        p.append('<label class="opt"><input type="radio" name="r-%s" value="%s"><span>%s</span></label>'
                 % (c["slug"], val, lab))
    p.append('</div>')
    p.append('<textarea class="note" data-slug="%s" rows="4" placeholder="In your own words &mdash; what you want changed, or which of the questions above you are answering."></textarea>'
             % c["slug"])
    p.append('<button type="button" class="clr" data-slug="%s">Clear</button>' % c["slug"])
    p.append('</div>')
    p.append('</div>')

    # specimen
    p.append('<details class="spec"><summary><span class="sc">Show the live specimen</span>'
             '<span class="src jk">showroom/%s.html</span></summary>' % E(c["slug"]))
    p.append('<div class="fwrap"><iframe class="sf" data-base="../showroom/%s.html" title="%s specimen, live"'
             ' loading="lazy"></iframe></div>' % (E(c["slug"]), E(c["name"])))
    p.append('</details>')
    p.append('</article>')
    return "\n".join(p)


def snippet_name(slug):
    # slugs are the lower-cased snippet stem; recover the file name for the join key
    special = {"qr-code": "Qr-code.reference.html", "cta-lockup": "CTA-lockup.reference.html",
               "fab": "Fab.reference.html"}
    if slug in special:
        return special[slug]
    return slug[0].upper() + slug[1:] + ".reference.html"


HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The 43 &mdash; wave 3&ndash;6 components, four themes, live (#213)</title>
<style>
  :root{
    --ink:#1A1A1A; --mid:#5F5F5F; --faint:#8C8C8C; --line:#E1E1E1; --line2:#F0F0F0;
    --paper:#FFFFFF; --ground:#F7F7F7; --red:#DA1A00; --amber:#B26B00;
    --bar-h:56px;
  }
  *{box-sizing:border-box;}
  html{scroll-behavior:smooth;}
  body{margin:0; background:var(--ground); color:var(--ink);
    font-family:"Univers Next for HSBC","Helvetica Neue",Helvetica,Arial,sans-serif;
    font-size:16px; line-height:1.5; -webkit-font-smoothing:antialiased;}
  h1,h2,h3,h4{margin:0; font-weight:400; letter-spacing:-0.01em;}
  code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:0.82em;}
  main{max-width:1240px; margin:0 auto; padding:0 24px 96px;}

  /* masthead */
  .mast{background:var(--paper); border-bottom:1px solid var(--line);}
  .mast-in{max-width:1240px; margin:0 auto; padding:48px 24px 32px;}
  .kicker{margin:0 0 12px; font-size:12px; letter-spacing:0.12em; text-transform:uppercase; color:var(--faint);}
  .mast h1{font-size:44px; line-height:1.08; max-width:26ch; margin:0 0 20px;}
  .lede{max-width:74ch; margin:0 0 12px; color:var(--mid); font-size:17px;}
  .lede strong{color:var(--ink);}
  .counts{display:flex; flex-wrap:wrap; gap:10px; margin-top:24px;}
  .cnt{display:flex; align-items:baseline; gap:8px; text-decoration:none; color:var(--ink);
    border:1px solid var(--line); padding:10px 16px; background:var(--paper);}
  .cnt:hover{border-color:var(--ink);}
  .cnt strong{font-size:26px; font-weight:300; line-height:1; letter-spacing:-1px;}
  .cnt span{font-size:12px; color:var(--mid); text-transform:uppercase; letter-spacing:0.08em;}
  .cnt.tot{background:var(--ink); color:#FFF;} .cnt.tot span{color:#CFCFCF;}

  /* sticky bar */
  .bar{position:sticky; top:0; z-index:40; background:var(--paper); border-bottom:1px solid var(--line);}
  .bar-in{max-width:1240px; margin:0 auto; padding:10px 24px; display:flex; align-items:center;
    gap:10px; flex-wrap:wrap; min-height:var(--bar-h);}
  .bl{font-size:11px; letter-spacing:0.1em; text-transform:uppercase; color:var(--faint);}
  .seg{display:inline-flex; border:1px solid var(--line);}
  .seg button{appearance:none; border:0; background:var(--paper); color:var(--mid);
    font:inherit; font-size:13px; padding:7px 12px; cursor:pointer; border-right:1px solid var(--line);}
  .seg button:last-child{border-right:0;}
  .seg button[aria-pressed="true"]{background:var(--ink); color:#FFF;}
  .seg button:focus-visible{outline:2px solid var(--red); outline-offset:-2px;}
  .bar-sp{flex:1 1 auto;}
  .bbtn{appearance:none; border:1px solid var(--ink); background:var(--paper); color:var(--ink);
    font:inherit; font-size:13px; padding:8px 14px; cursor:pointer;}
  .bbtn:hover{background:var(--ink); color:#FFF;}
  .bbtn.prim{background:var(--ink); color:#FFF;}
  .bbtn.prim:hover{background:#000;}
  .pill{display:inline-block; min-width:20px; text-align:center; background:#FFF; color:var(--ink);
    margin-left:6px; padding:0 5px; font-size:11px;}

  /* waves */
  .wave{padding-top:48px;}
  .wave-hd{border-top:2px solid var(--ink); padding-top:16px; margin-bottom:20px;}
  .wave-hd h2{font-size:30px;}
  .wc{font-size:13px; color:var(--faint); letter-spacing:0.06em; text-transform:uppercase; margin-left:10px;}
  .wsub{margin:8px 0 0; font-size:13px; color:var(--mid);}
  .wblurb{margin:6px 0 0; max-width:76ch; color:var(--mid);}
  .jk{color:var(--faint); font-size:12px;}

  /* rule-once blocks */
  .xcut{background:var(--paper); border:1px solid var(--line); border-left:3px solid var(--amber);
    margin:0 0 16px; padding:0 18px;}
  .xcut summary{cursor:pointer; padding:14px 0; font-size:16px; list-style:none;}
  .xcut summary::-webkit-details-marker{display:none;}
  .xcut summary::before{content:"\\25B8"; display:inline-block; width:1em; color:var(--faint);}
  .xcut[open] summary::before{transform:rotate(90deg);}
  .xtag{display:inline-block; background:var(--amber); color:#FFF; font-size:10px;
    letter-spacing:0.1em; text-transform:uppercase; padding:2px 7px; margin-right:8px; vertical-align:2px;}
  .xn{color:var(--faint); font-size:12px; margin-left:8px;}
  .qs{margin:0 0 14px; padding-left:22px;} .qs li{margin:0 0 10px; max-width:88ch;}
  .qs.big li{margin:0 0 14px;}
  .src{font-size:12px; color:var(--faint); margin:0 0 14px;}

  /* component card */
  .cmp{background:var(--paper); border:1px solid var(--line); margin:0 0 18px;}
  .chd{padding:18px 20px 14px; border-bottom:1px solid var(--line2);}
  .cnm{display:flex; align-items:baseline; gap:12px; flex-wrap:wrap;}
  .cnm h3{font-size:22px;}
  .kind{font-size:11px; letter-spacing:0.1em; text-transform:uppercase; color:var(--faint);}
  .cmeta{margin-top:6px;}
  .cst{margin-top:10px; display:flex; align-items:center; gap:8px; flex-wrap:wrap;}
  .badge{font-size:11px; letter-spacing:0.06em; text-transform:uppercase; padding:3px 8px; border:1px solid var(--line);}
  .badge.prop{border-color:var(--amber); color:var(--amber);}
  .badge.qn{color:var(--mid);}
  .verdict:empty{display:none;}
  .verdict{font-size:11px; letter-spacing:0.06em; text-transform:uppercase; padding:3px 8px;
    background:var(--ink); color:#FFF;}

  .cbody{display:grid; grid-template-columns:minmax(0,1.55fr) minmax(280px,1fr); gap:0;}
  @media (max-width:900px){ .cbody{grid-template-columns:1fr;} }
  .qcol{padding:18px 20px 4px; border-right:1px solid var(--line2);}
  @media (max-width:900px){ .qcol{border-right:0; border-bottom:1px solid var(--line2);} }
  .dcol{padding:18px 20px 20px; background:#FCFCFC;}
  h4{font-size:11px; letter-spacing:0.12em; text-transform:uppercase; color:var(--faint); margin:0 0 12px;}
  .opts{display:flex; flex-wrap:wrap; gap:6px; margin-bottom:12px;}
  .opt{display:inline-flex;}
  .opt input{position:absolute; opacity:0; width:0; height:0;}
  .opt span{display:inline-block; border:1px solid var(--line); padding:7px 13px; font-size:13px;
    cursor:pointer; color:var(--mid); background:var(--paper);}
  .opt input:checked + span{background:var(--ink); color:#FFF; border-color:var(--ink);}
  .opt input:focus-visible + span{outline:2px solid var(--red); outline-offset:2px;}
  .note{width:100%; font:inherit; font-size:14px; padding:10px; border:1px solid var(--line);
    background:var(--paper); color:var(--ink); resize:vertical;}
  .note:focus-visible{outline:2px solid var(--red); outline-offset:-2px;}
  .clr{appearance:none; border:0; background:none; color:var(--faint); font:inherit; font-size:12px;
    padding:8px 0 0; cursor:pointer; text-decoration:underline;}

  /* specimen */
  .spec{border-top:1px solid var(--line2);}
  .spec summary{cursor:pointer; padding:12px 20px; display:flex; align-items:baseline; gap:12px;
    list-style:none; background:#FAFAFA;}
  .spec summary::-webkit-details-marker{display:none;}
  .sc{font-size:13px; border-bottom:1px solid var(--ink);}
  .spec[open] .sc::after{content:" \\2014 open";}
  .fwrap{padding:0; background:#EFEFEF; overflow-x:auto;}
  .sf{display:block; width:100%; height:760px; border:0; background:#FFF; margin:0 auto;}

  /* export sheet */
  .ovl{position:fixed; inset:0; background:rgba(26,26,26,.55); z-index:80; display:flex;
    align-items:center; justify-content:center; padding:24px;}
  .ovl[hidden]{display:none;}
  .sheet{background:var(--paper); max-width:820px; width:100%; padding:24px; border:1px solid var(--ink);}
  .sheet h2{font-size:24px; margin-bottom:8px;}
  .shp{margin:0 0 14px; color:var(--mid); font-size:14px;}
  #exportTa{width:100%; font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:13px;
    padding:12px; border:1px solid var(--line); background:#FCFCFC; color:var(--ink); resize:vertical;}
  .shb{display:flex; gap:8px; margin-top:14px;}

  .foot{border-top:1px solid var(--line); background:var(--paper);}
  .foot p{max-width:1240px; margin:0 auto; padding:24px; font-size:12px; color:var(--faint);}

  @media (max-width:640px){
    .mast h1{font-size:32px;} .mast-in{padding:32px 20px 24px;} main{padding:0 16px 64px;}
    .sf{height:560px;}
  }
</style>
</head>
<body>'''

SCRIPT = '''
<script>
(function(){
  "use strict";
  var DATA = __DATA__;
  var KEY = "review213-rulings-v1";
  var state = {theme:"mono", mode:"light", w:"full"};
  var rulings = {};
  try { rulings = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch(e) { rulings = {}; }

  // ---- theme broadcast -------------------------------------------------
  // A showroom page listens for `hashchange` and re-reads #theme/&m/&w
  // (gen_showroom.py:309-315). Assigning a new FRAGMENT to iframe.src is a
  // same-document fragment navigation: no reload, no cross-origin access.
  function frag(){
    var p = ["theme=" + state.theme, "m=" + state.mode];
    // ALWAYS name the width. "full" maps to the showroom slider's own full
    // stop (1600), so a specimen whose inner slider carries stale state (seen
    // live #213: a 400px viewport surviving into a Full review) is RESET to
    // desktop rather than left wherever it last was.
    p.push("w=" + (state.w === "full" ? "1600" : state.w));
    return "#" + p.join("&");
  }
  var nonce = 0;
  function paint(f){
    var base = f.getAttribute("data-base");
    var want = base + frag();
    // If the wanted src equals the current one, an identical fragment fires no
    // `hashchange` and a stale INNER state (the inner slider, driven by hand)
    // survives an outer re-broadcast — proven live #213: Full over an inner
    // 400px stayed 400px. A nonce key makes every broadcast a real navigation;
    // the showroom's hash parser reads only theme/m/w and ignores it.
    if (f.getAttribute("src") === want) want += "&n=" + (++nonce);
    f.setAttribute("src", want);
    // outer width: the review page's own responsive check, independent of the
    // showroom's inner slider
    f.style.width = (state.w === "full") ? "100%" : (state.w + "px");
  }
  function paintAll(){
    document.querySelectorAll("iframe.sf").forEach(function(f){
      if (f.getAttribute("src")) paint(f);
    });
  }
  function mount(det){
    var f = det.querySelector("iframe.sf");
    if (f && !f.getAttribute("src")) paint(f);
  }

  function seg(id, key, attr){
    var el = document.getElementById(id);
    el.addEventListener("click", function(e){
      var b = e.target.closest("button"); if(!b) return;
      state[key] = b.getAttribute(attr);
      el.querySelectorAll("button").forEach(function(x){
        x.setAttribute("aria-pressed", String(x.getAttribute(attr) === state[key]));
      });
      paintAll();
    });
  }
  seg("segTheme","theme","data-theme");
  seg("segMode","mode","data-mode");
  seg("segW","w","data-w");

  document.querySelectorAll("details.spec").forEach(function(d){
    d.addEventListener("toggle", function(){ if (d.open) mount(d); });
  });
  document.getElementById("openAll").addEventListener("click", function(){
    document.querySelectorAll("details.spec").forEach(function(d){ d.open = true; mount(d); });
  });
  document.getElementById("closeAll").addEventListener("click", function(){
    document.querySelectorAll("details.spec").forEach(function(d){ d.open = false; });
  });

  // ---- decision controls ----------------------------------------------
  function save(){
    try { localStorage.setItem(KEY, JSON.stringify(rulings)); } catch(e) {}
    var n = 0;
    for (var k in rulings) { if (rulings[k] && (rulings[k].v || rulings[k].n)) n++; }
    document.getElementById("ruledN").textContent = String(n);
  }
  function badge(slug){
    var el = document.querySelector('.verdict[data-for="' + slug + '"]');
    if (!el) return;
    var r = rulings[slug];
    el.textContent = (r && r.v) ? r.v : "";
  }
  document.addEventListener("change", function(e){
    var t = e.target;
    if (t.type === "radio" && t.name.indexOf("r-") === 0){
      var slug = t.name.slice(2);
      rulings[slug] = rulings[slug] || {};
      rulings[slug].v = t.value;
      badge(slug); save();
    }
  });
  document.addEventListener("input", function(e){
    var t = e.target;
    if (t.classList && t.classList.contains("note")){
      var slug = t.getAttribute("data-slug");
      rulings[slug] = rulings[slug] || {};
      rulings[slug].n = t.value;
      save();
    }
  });
  document.addEventListener("click", function(e){
    var b = e.target.closest(".clr"); if(!b) return;
    var slug = b.getAttribute("data-slug");
    delete rulings[slug];
    document.querySelectorAll('input[name="r-' + slug + '"]').forEach(function(i){ i.checked = false; });
    var ta = document.querySelector('.note[data-slug="' + slug + '"]'); if (ta) ta.value = "";
    badge(slug); save();
  });

  // restore
  DATA.forEach(function(c){
    var r = rulings[c.slug]; if (!r) return;
    if (r.v){
      var i = document.querySelector('input[name="r-' + c.slug + '"][value="' + r.v + '"]');
      if (i) i.checked = true;
    }
    if (r.n){
      var ta = document.querySelector('.note[data-slug="' + c.slug + '"]');
      if (ta) ta.value = r.n;
    }
    badge(c.slug);
  });
  save();

  // ---- export ----------------------------------------------------------
  function exportText(){
    var lines = [];
    lines.push("RULINGS ON THE 43 WAVE 3-6 COMPONENTS - " + new Date().toISOString().slice(0,10));
    lines.push("(typed into REVIEW-213-wave-components-four-theme-v1.html; nothing was written to the store)");
    lines.push("");
    var waves = ["wave 3","wave 4","wave 5","wave 6"], any = false;
    waves.forEach(function(w){
      var rows = DATA.filter(function(c){ var r = rulings[c.slug]; return c.wave === w && r && (r.v || r.n); });
      if (!rows.length) return;
      any = true;
      lines.push("== " + w.toUpperCase() + " ==");
      rows.forEach(function(c){
        var r = rulings[c.slug];
        lines.push("- " + c.name + " [" + c.slug + ", row " + c.row + "]: " + ((r.v || "no verdict").toUpperCase()));
        if (r.n) lines.push("    " + r.n.replace(/\\n/g, "\\n    "));
      });
      lines.push("");
    });
    var undone = DATA.filter(function(c){ var r = rulings[c.slug]; return !(r && (r.v || r.n)); });
    if (undone.length){
      lines.push("== NOT YET RULED (" + undone.length + " of " + DATA.length + ") ==");
      lines.push(undone.map(function(c){ return c.slug; }).join(", "));
    }
    if (!any) lines.push("(nothing recorded yet)");
    return lines.join("\\n");
  }
  var ovl = document.getElementById("ovl");
  document.getElementById("exportBtn").addEventListener("click", function(){
    document.getElementById("exportTa").value = exportText();
    ovl.hidden = false;
    document.getElementById("exportTa").focus();
  });
  document.getElementById("closeSheet").addEventListener("click", function(){ ovl.hidden = true; });
  ovl.addEventListener("click", function(e){ if (e.target === ovl) ovl.hidden = true; });
  document.addEventListener("keydown", function(e){ if (e.key === "Escape") ovl.hidden = true; });
  document.getElementById("copyBtn").addEventListener("click", function(){
    var ta = document.getElementById("exportTa");
    ta.select();
    try { document.execCommand("copy"); this.textContent = "Copied";
      var b = this; setTimeout(function(){ b.textContent = "Copy to clipboard"; }, 1600); } catch(e) {}
  });
})();
</script>'''


if __name__ == "__main__":
    out = build()
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(out)
    print("wrote %s (%d bytes, %d components)" % (
        os.path.relpath(OUT, REPO), len(out.encode("utf-8")), len(COMPONENTS)))
