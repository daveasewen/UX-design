#!/usr/bin/env python3
"""#281 lane RO — build the 59 restsOn PROPOSALS and Dave's review page.

INSCRIBE + PROPOSE only. Nothing here lands an edge, touches the builder, the
explorer or knowledge/_kg_verbs.json. The output is two files under
notes/_lanes/281/rests-on/:

    proposals.json                the machine record, one entry per BLOCKING rule
    RESTS-ON-2026-09-17.html      the page Dave reads and exports

Run:  python3 notes/_lanes/281/rests-on/gen_rests_on.py

Every proposal is GROUNDED: the clause quoted from the rule's own `text` and the
clause quoted from the principle's own `statement` are asserted to be literal
substrings of the stored node before anything is written. A typo in a quote is a
build failure, not a silent misquote.
"""
import html
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[4]
OUT = REPO / "notes" / "_lanes" / "281" / "rests-on"
RULES = REPO / "knowledge" / "_rule_nodes.json"
UX = REPO / "knowledge" / "_ux_principle_nodes.json"
DATE = "2026-09-17"
PAGE = "RESTS-ON-2026-09-17"

# ---------------------------------------------------------------- the proposals
# ruleId -> {rq: clause quoted from the rule, opts: [(uxId, pq, why)], null: why,
#            rec: 'a' | 'c'}   (rec 'a' = the first option; rec 'c' = convention)
P = {
# --- accessibility-content-authoring.md -------------------------------------
"aca-003": dict(rec="a", rq="first thing a speech-output user hears",
 null="The title could be called a naming convention, but the rule states a perceptual consequence, so a principle is the honest home.",
 opts=[("pr-information-scent", "the strongest cue that the target lies that way",
        "A page title is the first and often only cue a speech-output user has that they have arrived in the right place, which is exactly the foraging cue the principle describes."),
       ("pr-coga-2", "Help users find what they need",
        "Read as a findability rule rather than a perception one, a unique title is what lets someone locate the page again among a dozen open frames.")]),

"aca-004": dict(rec="a", rq="link text uniquely describes the target",
 null="Link wording is sometimes treated as a house style matter, but the rule gives a functional test — uniqueness in context — so it is not style alone.",
 opts=[("pr-information-scent", "People choose navigation paths the way animals forage",
        "A link is chosen on its text alone when the text is read out of context, so text that does not describe the target removes the only scent the person had."),
       ("pr-coga-2", "Help users find what they need",
        "Six identical “Info” links are six identical answers to “where do I go”, which is the finding problem stated plainly.")]),

# --- accessibility-interaction-design.md ------------------------------------
"aid-009": dict(rec="a", rq="44×44",
 null="The 44 and the 24 are statutory numbers, not house convention, so a declared null would hide their source.",
 opts=[("pr-fitts", "shrinks with target size",
        "The whole rule is a size floor, and the law says in numbers why a floor exists at all: acquisition time rises as the target shrinks."),
       ("pr-wcag-2-5-5", "Pointer targets are at least 44 by 44 CSS pixels",
        "Read as an obligation rather than an explanation, the rule is 2.5.5 adopted as the HSBC default with 2.5.8's 24 as the named exception.")]),

# --- accessibility-visual-design.md -----------------------------------------
"avd-006": dict(rec="a", rq="alt describes PURPOSE",
 null="Alt text is a statutory requirement, not a convention, so convention would be the wrong answer here.",
 opts=[("pr-wcag-perceivable", "must be presentable in ways users can perceive",
        "An image with no text alternative is information that one population simply cannot receive, which is the perceivable principle in its plainest form."),
       ("pr-norman-signifier", "the perceivable cue that tells someone where and how to act",
        "The rule's sharper half — actionable images describe the ACTION, not the picture — is a signifier rule: the alt has to say where and how to act, not what the thing looks like.")]),

# --- app-foundations.md ------------------------------------------------------
"appf-002": dict(rec="a", rq="test that the layout adapts to ALL accessibility font sizes",
 null="The rule names an iOS API, which could read as platform convention, but honouring a user's own setting is a principle, not a habit.",
 opts=[("pr-idp-give-control", "Do not override or remove the user's control of their view",
        "Dynamic Type is the user's own declaration of what they can read, and a layout that breaks at the largest sizes takes that control back."),
       ("pr-tog-readability", "readable by people with less than perfect sight, which is most people over forty",
        "Read as a legibility rule, the largest accessibility sizes exist for the sight the principle says most adults eventually have.")]),

# --- brand-refresh-assets.md -------------------------------------------------
"logo26-001": dict(rec="c", rq="An HSBC logo appears at least once",
 null="Brand presence. Nothing in the register explains why a mark must appear; it is an identity requirement the business sets and no graded principle predicts.",
 opts=[]),

"photo26-002": dict(rec="c", rq="no Generative AI, mixed media or CGI-rendered elements in imagery",
 null="Provenance and trust governance, not perception. The ban says where an image may come from, which is a sourcing rule; no graded principle in the register speaks to image provenance.",
 opts=[]),

# --- colour-standards-2026.md ------------------------------------------------
"col26-004": dict(rec="a", rq="prolonged exposure causes visual fatigue and reduces legibility",
 null="The rule gives its own reason in the clause, so convention would be discarding a stated one.",
 opts=[("pr-tog-readability", "Text must be readable by people with less than perfect sight",
        "The rule's own reason is legibility over time, and the principle is the register's statement that legibility is a design obligation rather than a preference."),
       ("pr-wcag-1-4-3", "Text must meet a minimum contrast ratio against its background",
        "Read as a contrast rule, red is the background most likely to fail 4.5:1 against the text colours the brand allows.")]),

"col26-008": dict(rec="a", rq="illustrations, data visualisations, status-driven interfaces (RAG, risk, gain/loss) only",
 null="A palette scope could be pure convention, but the scope is chosen so that a supporting colour keeps one meaning, which is a usability reason.",
 opts=[("pr-nng-consistency", "wonder whether different words or actions mean the same thing",
        "Confining the supporting palette to status and chart contexts is what stops the same green meaning “good” in one place and “decoration” in another."),
       ("pr-gestalt-similarity", "Elements sharing shape, colour or size are read as belonging to the same set",
        "If the supporting colours appear outside those contexts, everything wearing them reads as one set when it is not.")]),

"col26-009": dict(rec="a", rq="Don't use the supporting palette as text",
 null="The rule is a contrast consequence, not a taste call, so a null would lose the reason.",
 opts=[("pr-wcag-1-4-3", "Text must meet a minimum contrast ratio against its background",
        "The supporting palette was built for fills and indicators, and its mid-tones cannot reach the text contrast floor on the brand's backgrounds."),
       ("pr-nng-consistency", "wonder whether different words or actions mean the same thing",
        "Kept out of text, a supporting colour keeps its one job as a status fill.")]),

"col26-011": dict(rec="a", rq="every colour used must meet ≥3:1 against its background",
 null="This is a statutory threshold quoted directly; convention would be wrong.",
 opts=[("pr-wcag-1-4-11", "graphical objects need at least 3:1 contrast against adjacent colours",
        "The rule is 1.4.11 applied to chart marks: a bar or a line is a graphical object carrying information, so the 3:1 floor is the statutory one."),
       ("pr-wcag-perceivable", "must be presentable in ways users can perceive",
        "Read one level up, a chart colour nobody can separate from the page is information that was never delivered.")]),

"col26-012": dict(rec="a", rq="Don't combine HSBC Red with the supporting palette in data visualisations",
 null="Could be read as brand hygiene, but red already carries a reserved meaning in this system, so the reason is functional.",
 opts=[("pr-nng-consistency", "wonder whether different words or actions mean the same thing",
        "Red means call to action and, in RAG, means alert; used as an ordinary chart category alongside the supporting palette it stops meaning either."),
       ("pr-von-restorff", "An item that differs from its neighbours is remembered better",
        "Red is the strongest attention cue the palette has, and spending it on an arbitrary category spends the salience that the alert case needs.")]),

"col26-015": dict(rec="a", rq="Don't introduce colours outside the palettes",
 null="A closed palette is partly identity, and if the panel reads it that way the null is legal — the note would be “brand asset list”.",
 opts=[("pr-nng-consistency", "wonder whether different words or actions mean the same thing",
        "In this system colour is load-bearing — red is action, the supporting palette is status — so an off-palette colour is a signal with no agreed meaning."),
       ("pr-idp-be-consistent", "Use familiar conventions and apply them consistently across the service",
        "Read more simply, a closed palette is the mechanism that makes the service look and behave like one service.")]),

"col26-016": dict(rec="a", rq="red text is reserved for call to actions",
 null="The rule states a reservation, and a reservation exists to protect a signal, which is a principle.",
 opts=[("pr-von-restorff", "An item that differs from its neighbours is remembered better than the items it sits among",
        "Reserving red for calls to action is how the one red thing on the page stays the thing people notice; spend red on body copy and the effect is gone."),
       ("pr-nng-consistency", "wonder whether different words or actions mean the same thing",
        "If red sometimes means “click me” and sometimes means nothing, the reader has to check each time.")]),

"col26-017": dict(rec="a", rq="never light-on-light or dark-on-dark",
 null="A luminance-polarity rule restates a statutory floor, so convention would hide its source.",
 opts=[("pr-wcag-1-4-3", "Text must meet a minimum contrast ratio against its background",
        "Opposing luminance is the precondition for any contrast ratio at all: same-polarity pairs cannot reach the floor whatever the hue."),
       ("pr-gestalt-figure-ground", "ambiguity here is disorienting",
        "Read perceptually, same-polarity pairs leave the eye unable to decide which layer is the object and which is the ground.")]),

"col26-018": dict(rec="a", rq="text 4.5:1 · graphic elements (icons, chart indicators) 3:1",
 null="Two statutory thresholds quoted verbatim; a null would be false.",
 opts=[("pr-wcag-1-4-3", "Text must meet a minimum contrast ratio against its background",
        "The rule's first threshold is 1.4.3 exactly — RAG labels are text and take the 4.5:1 floor."),
       ("pr-wcag-1-4-11", "graphical objects need at least 3:1 contrast against adjacent colours",
        "The rule's second threshold is 1.4.11 exactly — a RAG dot or chart indicator is a graphical object at 3:1.")]),

# --- data-visualisation-bar-charts.md ---------------------------------------
"dv-bar-007": dict(rec="a", rq="Don't put negative values on a horizontal bar chart",
 null="A chart-form rule could be convention, but the reason is a measured perceptual one.",
 opts=[("pr-graphical-perception", "People judge position on a common scale far more accurately",
        "Vertical bars put positive and negative on one common scale through zero, so the sign is read as position; horizontal bars make the reader judge direction instead."),
       ("pr-jakobs-law", "they expect yours to work like those",
        "Read as an expectation rule, up-is-more and down-is-less is what every other chart the reader has seen has taught them.")]),

"dv-bar-009": dict(rec="a", rq="must include a zero baseline",
 null="The zero baseline is the single most measured rule in chart perception; convention would be a false answer.",
 opts=[("pr-graphical-perception", "People judge position on a common scale far more accurately than angle, area or colour saturation",
        "A bar encodes its value as length from zero, so removing the zero baseline leaves the accurate encoding — position on a common scale — measuring something other than the value.")]),

# --- data-visualisation-line-charts.md --------------------------------------
"dv-line-011": dict(rec="a", rq="Never gratuitous curves for aesthetics — they distort the data",
 null="The rule states the distortion in its own clause, so it does not rest on convention.",
 opts=[("pr-graphical-perception", "People judge position on a common scale far more accurately",
        "The reader takes position on the line as the value, so a spline between two points asserts positions that were never measured."),
       ("pr-gestalt-continuity", "Elements on a line or curve are read as related and as continuing in that direction",
        "A curve is read as a continuing trend, which is the specific false claim a smoothed line makes between samples.")]),

# --- data-visualisation-pie-charts.md ---------------------------------------
"dv-pie-009": dict(rec="a", rq="Maximum 6 slices",
 null="The exact number 6 is a house choice, but the reason for having a ceiling is measured.",
 opts=[("pr-graphical-perception", "far more accurately than angle, area or colour saturation",
        "A pie already uses the least accurate encodings the principle names, and every extra slice shrinks the angles being compared, so a ceiling is damage control."),
       ("pr-working-memory-4", "Working memory holds about four chunks, not seven",
        "Read as a load rule, a legend of seven or more categories is more than the reader can hold while looking at the wedges.")]),

"dv-pie-010": dict(rec="a", rq="always include value indicators",
 null="The summing requirement is arithmetic honesty; the label requirement has a perceptual reason, so neither is convention.",
 opts=[("pr-graphical-perception", "far more accurately than angle, area or colour saturation",
        "Printing the number beside the wedge replaces the angle judgment the principle says is inaccurate with a reading, which is accurate."),
       ("pr-mental-model", "mismatches with it produce errors",
        "A pie asserts that the parts are the whole; slices that do not sum to the total contradict the model the form itself created.")]),

# --- data-visualisation.md ---------------------------------------------------
"dv-004": dict(rec="a", rq="don't rely on colour to separate values",
 null="“Not colour alone” is statutory; the 2px figure is the house's implementation of it.",
 opts=[("pr-wcag-perceivable", "Information and interface components must be presentable in ways users can perceive",
        "A reader who cannot separate two hues gets no boundary at all unless a second, non-colour cue carries it, which is what the 2px gap is."),
       ("pr-gestalt-common-region", "the boundary outranks proximity",
        "The gap is a boundary, and the principle says a boundary is read before and above anything else, including colour.")]),

"dv-009": dict(rec="a", rq="No 3D styles, no gradient fills",
 null="A style ban that has a measured reason is not convention.",
 opts=[("pr-graphical-perception", "far more accurately than angle, area or colour saturation",
        "A 3D extrusion adds area and a gradient adds saturation — the two encodings the principle names as least accurate — on top of the length that was carrying the value."),
       ("pr-nng-minimalist", "Every extra element on a screen competes with the elements that matter",
        "Read as a noise rule, bevels and gradients are ink that carries no data and competes with the ink that does.")]),

"dv-016": dict(rec="a", rq="black-or-grey on light, white-or-grey on dark, ≥3:1",
 null="The 3:1 is quoted from WCAG in the rule itself; convention would be wrong.",
 opts=[("pr-wcag-1-4-3", "Text must meet a minimum contrast ratio against its background",
        "Titles and axis labels are text, so the rule is the text-contrast obligation applied to the furniture of a chart rather than to its body copy."),
       ("pr-wcag-1-4-11", "graphical objects need at least 3:1 contrast against adjacent colours",
        "Axis and grid lines are graphical objects, and 3:1 is the floor the rule quotes, so half of it is 1.4.11 rather than 1.4.3.")]),

"dv-017": dict(rec="a", rq="Only palette colours in charts",
 null="If the panel reads the palette as a brand asset list rather than a meaning system, the null is legal.",
 opts=[("pr-idp-be-consistent", "Use familiar conventions and apply them consistently across the service",
        "A fixed chart palette is what lets a reader carry the meaning of a colour from one chart to the next without relearning it."),
       ("pr-nng-consistency", "wonder whether different words or actions mean the same thing",
        "An off-palette colour in a chart is a category the reader has to decode from scratch.")]),

# --- icons.md ----------------------------------------------------------------
"icon-002": dict(rec="a", rq="Don't use illustrations as icons",
 null="The two forms are separate brand assets, so a convention reading is defensible — but the rule protects a functional signal.",
 opts=[("pr-norman-signifier", "the perceivable cue that tells someone where and how to act",
        "An icon is a signifier of an available action; an illustration is a picture, and putting one in the action slot removes the cue that says “you can act here”."),
       ("pr-gestalt-similarity", "Elements sharing shape, colour or size are read as belonging to the same set",
        "Icons are recognised as a set by their shared weight and construction, and an illustration dropped among them is read as a different kind of thing.")]),

"icon-005": dict(rec="a", rq="minimum 44×44px target area",
 null="A measured size floor with a statutory twin; convention would be false.",
 opts=[("pr-fitts", "shrinks with target size",
        "A 16px glyph is not a 16px target, and the law is why the touchable area rather than the drawn area is what the rule constrains."),
       ("pr-wcag-2-5-5", "Pointer targets are at least 44 by 44 CSS pixels",
        "Read as an obligation, 44×44 is 2.5.5 verbatim.")]),

"icon-006": dict(rec="a", rq="Minimum 16px, maximum 48px",
 null="The 2px increments and the 48px ceiling are house construction rules with no principle behind them; only the 16px floor has a perceptual reason.",
 opts=[("pr-tog-readability", "readable by people with less than perfect sight, which is most people over forty",
        "The floor exists because an icon's strokes stop resolving at small sizes for exactly the sight the principle describes; the ceiling and the increments are construction."),
       ("pr-gestalt-similarity", "Elements sharing shape, colour or size are read as belonging to the same set",
        "Read as a set rule, the size band and the 2px step are what keep a row of icons reading as one family.")]),

"icon-011": dict(rec="a", rq="Icons require 4.5:1 contrast in all instances",
 null="A stricter-than-statutory threshold is still a threshold with a source.",
 opts=[("pr-wcag-1-4-3", "Text must meet a minimum contrast ratio against its background",
        "The rule says “like text” in its own words: the house takes the 4.5:1 text floor for icons rather than the 3:1 graphical one."),
       ("pr-wcag-1-4-11", "graphical objects need at least 3:1 contrast against adjacent colours",
        "The statutory floor for an icon is 3:1, so read against the obligation the house rule is deliberately stricter than the law requires.")]),

"icon-012": dict(rec="a", rq="icon with label → `alt=\"\"` (null); icon without label → `alt` = icon name",
 null="Both halves have reasons, so neither is convention.",
 opts=[("pr-wcag-perceivable", "Information and interface components must be presentable in ways users can perceive",
        "The second half is the obligation exactly: an unlabelled icon carries meaning nobody using speech output can perceive unless it is named."),
       ("pr-nng-minimalist", "Every extra element on a screen competes with the elements that matter",
        "The first half is the mirror of that: naming an icon that already sits beside its label makes the screen reader say everything twice.")]),

"icon-013": dict(rec="a", rq="never colour alone for status — supporting information required",
 null="“Never colour alone” is statutory, not house habit.",
 opts=[("pr-wcag-perceivable", "Information and interface components must be presentable in ways users can perceive",
        "Status carried by hue alone is invisible to a large population, so the rule requires a second channel — a shape, a word — to carry the same fact."),
       ("pr-wcag-1-4-11", "graphical objects need at least 3:1 contrast against adjacent colours",
        "The rule's other half is the contrast obligation, applied against the background the icon actually lands on rather than the one it was designed against.")]),

# --- illustration-standards.md -----------------------------------------------
"ill-010": dict(rec="a", rq="Don't use typography within illustrations",
 null="Could be read as an asset-production convention; the accessibility consequence is the stronger reason.",
 opts=[("pr-wcag-perceivable", "Information and interface components must be presentable in ways users can perceive",
        "Words baked into an image cannot be resized, restyled, translated or read aloud, so the text is only available to people who can see it as drawn."),
       ("pr-idp-comparable-experience", "an equivalent way to accomplish the task, not a degraded alternative",
        "Read as an equity rule, text-in-image leaves some readers with an alt-text summary where others get the words themselves.")]),

# --- motion-standards.md ------------------------------------------------------
"mot-005": dict(rec="a", rq="Any motion over 5 seconds needs play and pause",
 null="The five seconds is the statutory figure, so the rule has a source and not a habit.",
 opts=[("pr-idp-give-control", "Do not override or remove the user's control of their view, including motion and zoom",
        "Motion nobody can stop is the interface deciding what the reader looks at, and the principle names motion specifically as control the reader keeps."),
       ("pr-wcag-operable", "Interface components and navigation must be operable",
        "Read as an obligation, unstoppable movement makes the content around it unusable for people it distracts or sickens.")]),

# --- naming.md -----------------------------------------------------------------
"nam-001": dict(rec="c", rq="HSBC should not appear in the possessive form",
 null="Brand naming convention, stated as such in the source. It is a house style rule about the word HSBC, and no graded principle predicts or explains it.",
 opts=[]),

# --- neurodiversity.md ----------------------------------------------------------
"neuro-026": dict(rec="a", rq="content must remain comprehensible with all images and icons removed",
 null="The rule states a comprehension test, which is a principle's kind of claim.",
 opts=[("pr-coga-1", "Help users understand what things are and how to use them",
        "The rule is that test made concrete: strip the pictures and the words must still say what each thing is and how to use it."),
       ("pr-coga-3", "Use clear and understandable content",
        "Read as a content rule, an icon that carries meaning alone is content that is only clear to the people who already know the icon.")]),

# --- pictograms.md ---------------------------------------------------------------
"pict-001": dict(rec="a", rq="Every pictogram carries a label or copy that underpins its meaning — no exceptions",
 null="The no-exceptions clause is a house decision, but the reason for it is a comprehension one.",
 opts=[("pr-coga-1", "Help users understand what things are and how to use them",
        "A pictogram is an invented sign with no universal meaning, so the label is the only thing that tells the reader what it stands for."),
       ("pr-norman-signifier", "the perceivable cue that tells someone where and how to act",
        "Read as a signifier rule, an unlabelled pictogram is a cue whose referent the designer knows and the reader has to guess.")]),

"pict-007": dict(rec="a", rq="causes contrast issues with the primary form",
 null="The rule gives the contrast reason in its own clause.",
 opts=[("pr-wcag-1-4-11", "graphical objects need at least 3:1 contrast against adjacent colours",
        "The rule names the failure it is preventing: on red, the pictogram's primary form cannot hold the 3:1 a graphical object owes its background."),
       ("pr-von-restorff", "An item that differs from its neighbours is remembered better",
        "The rule's other stated reason is interference with the red accent, which only works as an attention cue while it is the exception on the page.")]),

"pict-008": dict(rec="a", rq="≥3:1 contrast against the background in all placements",
 null="A statutory threshold quoted directly.",
 opts=[("pr-wcag-1-4-11", "graphical objects need at least 3:1 contrast against adjacent colours",
        "A pictogram is a graphical object carrying meaning, so 3:1 against whatever it actually sits on — including photography — is the statutory floor."),
       ("pr-wcag-perceivable", "Information and interface components must be presentable in ways users can perceive",
        "The rule's alt-text clause is the same obligation on the other channel: the meaning must also arrive without the picture.")]),

"pict-009": dict(rec="a", rq="elevation is functional-only (an object moving over another)",
 null="A shadow ban could be pure style, but the rule states a functional meaning for elevation, which is a signifier claim.",
 opts=[("pr-norman-signifier", "the perceivable cue that tells someone where and how to act",
        "A shadow tells the reader this thing is above and separate from what it covers; on a pictogram, which never moves over anything, it says something untrue."),
       ("pr-gestalt-figure-ground", "ambiguity here is disorienting",
        "Read perceptually, decorative shadows put layers into a scene that has none, which is exactly the figure-ground ambiguity the principle warns about.")]),

"pict-010": dict(rec="c", rq="Below 60px, use an icon instead",
 null="House construction figures. The 60px floor does have a perceptual reason — a pictogram's line detail stops resolving — but the register holds no acuity or minimum-legible-detail principle to rest it on, and 192px and the 2px interval are pure system construction.",
 opts=[("pr-tog-readability", "readable by people with less than perfect sight, which is most people over forty",
        "The nearest graded fit: the floor exists so the detail survives for readers whose sight the principle describes, though the principle is about text, not marks.")]),

"pict-011": dict(rec="a", rq="Never squash, stretch, skew or distort",
 null="Aspect-ratio locking is often pure asset convention, and if the panel reads it that way the null is legal.",
 opts=[("pr-gestalt-similarity", "Elements sharing shape, colour or size are read as belonging to the same set",
        "A pictogram is recognised by its shape, so a stretched one stops reading as a member of the set the reader has already learned."),
       ("pr-idp-be-consistent", "Use familiar conventions and apply them consistently across the service",
        "Read as a system rule, a locked ratio is what makes the same mark the same mark everywhere it appears.")]),

# --- tone-of-voice.md ------------------------------------------------------------
"tov-038": dict(rec="a", rq="'select', never 'click'; never describe UI visually",
 null="Word choice is house style, but this rule states a functional test — it must work on every device — so it is not style alone.",
 opts=[("pr-nng-match-real-world", "Use the words and concepts of the user's world",
        "“Click” is the designer's world; a reader on a phone or a screen reader has no click, so the instruction describes an action they cannot take."),
       ("pr-govuk-understand-context", "Design for the real context: the device, the place, the pressure people are under",
        "Read as a context rule, the same sentence has to survive a desktop, a phone, a tablet and speech output, which is what device-agnostic wording buys.")]),

# --- typography-standards-2026.md -------------------------------------------------
"type26-002": dict(rec="c", rq="Only use brand-approved fonts, weights and colours",
 null="Brand and licensing. The approved list is an asset and rights decision; an unapproved typeface is not less usable, it is not ours to use. Consistency is a side effect, not the reason.",
 opts=[("pr-idp-be-consistent", "Use familiar conventions and apply them consistently across the service",
        "The nearest graded fit if the panel reads the approved list as a consistency mechanism rather than a rights one.")]),

"type26-003": dict(rec="a", rq="All text legible and ≥4.5:1 contrast",
 null="A statutory threshold quoted verbatim.",
 opts=[("pr-wcag-1-4-3", "Text must meet a minimum contrast ratio against its background",
        "The rule is 1.4.3 restated at brand level, with the same number."),
       ("pr-tog-readability", "readable by people with less than perfect sight, which is most people over forty",
        "The rule's first word — legible — is broader than the ratio, and the principle is what that broader half rests on.")]),

"type26-004": dict(rec="a", rq="Never use red typography except within specific digital toolkit use-cases",
 null="A reservation exists to protect a signal, so the rule has a reason.",
 opts=[("pr-von-restorff", "An item that differs from its neighbours is remembered better than the items it sits among",
        "Red type works as a call-to-action cue only while it is rare, and the exception scope is what keeps it rare."),
       ("pr-nng-consistency", "wonder whether different words or actions mean the same thing",
        "Toolkit-defined rather than designer-judged exceptions are what stop red from meaning different things on different screens.")]),

"type26-005": dict(rec="a", rq="We don't use uppercase or italics lettering — use sentence case",
 null="The sister rule type26-019 states the legibility reason, so this one is not bare convention.",
 opts=[("pr-tog-readability", "readable by people with less than perfect sight, which is most people over forty",
        "Uppercase removes the word shapes readers use to recognise words without reading them, and italics thin the strokes; both cost most for the sight the principle names."),
       ("pr-coga-3", "Use clear and understandable content",
        "Read as a content rule, sentence case is the casing people read fastest and the one dyslexia guidance asks for.")]),

"type26-012": dict(rec="a", rq="12pt minimum, print AND digital",
 null="Minimum type sizes have a perceptual reason even though the exact points are house-set.",
 opts=[("pr-tog-readability", "readable by people with less than perfect sight, which is most people over forty",
        "Every clause in the rule is a floor below which strokes stop resolving — including the Ultra Light ban, which is a floor on stroke weight rather than size."),
       ("pr-govuk-understand-context", "Design for the real context: the device, the place, the pressure people are under",
        "Read as a context rule, the separate Chinese and Arabic floors exist because the same point size does not deliver the same legible detail in every script.")]),

"type26-013": dict(rec="a", rq="NO other colours for typography, ever",
 null="A colour restriction that exists to guarantee contrast is not convention.",
 opts=[("pr-wcag-1-4-3", "Text must meet a minimum contrast ratio against its background",
        "Restricting type to the two luminance extremes is how the brand guarantees the contrast floor without measuring every pairing."),
       ("pr-gestalt-figure-ground", "ambiguity here is disorienting",
        "The photography clause is the figure-ground case: over an image, only black or white reliably separates the word from the scene behind it.")]),

"type26-014": dict(rec="a", rq="3:1 large AA · 4.5:1 small AA · 7:1 AAA",
 null="Three statutory thresholds quoted verbatim.",
 opts=[("pr-wcag-1-4-3", "Text must meet a minimum contrast ratio against its background",
        "The three numbers are 1.4.3's large-text, small-text and enhanced levels exactly, applied to the hardest background there is.")]),

"type26-019": dict(rec="a", rq="harder to read, reduces word shapes, dyslexia/low-vision cost",
 null="The rule carries its own evidence clause, so a null would discard a stated reason.",
 opts=[("pr-tog-readability", "readable by people with less than perfect sight, which is most people over forty",
        "The rule names its own reason — word shapes, dyslexia, low vision — and the principle is the register's statement that those readers set the floor."),
       ("pr-coga-3", "Use clear and understandable content",
        "Read as a content rule, casing is part of whether the words are understandable at speed.")]),

"type26-020": dict(rec="a", rq="Never justified (rivers); avoid hyphenation",
 null="Alignment is often taste, and the panel could legally call this one convention.",
 opts=[("pr-gestalt-continuity", "Elements on a line or curve are read as related and as continuing in that direction",
        "A hard left edge is the line the eye returns to at every line break, and justification breaks it by opening rivers of white that the eye reads as a competing vertical."),
       ("pr-tog-readability", "readable by people with less than perfect sight, which is most people over forty",
        "Read as a legibility rule, uneven word spacing and broken words cost most for the readers already working hardest.")]),

# --- typography-usage.md -----------------------------------------------------------
"type25-003": dict(rec="a", rq="red only for text links (CTAs)",
 null="Same reservation as col26-016 and type26-004; it protects a signal.",
 opts=[("pr-von-restorff", "An item that differs from its neighbours is remembered better than the items it sits among",
        "The link is supposed to be the thing that stands out from the paragraph, and it can only do that while nothing else in the paragraph is red."),
       ("pr-nng-consistency", "wonder whether different words or actions mean the same thing",
        "One meaning for red text — this is a link — is what saves the reader from testing each red word.")]),

"type25-007": dict(rec="a", rq="harder to read, especially for people with dyslexia",
 null="The licensing half is convention, but the rule also states a legibility reason, so the honest answer keeps the principle.",
 opts=[("pr-tog-readability", "readable by people with less than perfect sight, which is most people over forty",
        "The rule gives the reason itself: slanted, lighter strokes cost the readers who are already working hardest. The licensing half is a separate, conventional reason."),
       ("pr-coga-3", "Use clear and understandable content",
        "Read as a content rule, italics are a styling device that carries emphasis at a comprehension cost for some readers.")]),

"type25-008": dict(rec="a", rq="underline = links only",
 null="An emphasis palette could be house style, but the underline clause protects a learned signal.",
 opts=[("pr-nng-consistency", "wonder whether different words or actions mean the same thing",
        "If underline sometimes means link and sometimes means emphasis, every underlined word becomes a question the reader has to test."),
       ("pr-norman-signifier", "the perceivable cue that tells someone where and how to act",
        "Read as a signifier rule, underline is the web's oldest cue for “this is actionable”, and spending it on emphasis makes the cue lie.")]),

"type25-020": dict(rec="c", rq="STRAIGHT TO BLOCKING",
 null="Not a design rule. This entry records a gate decision — three checks promoted past the advisory step and enacted in _validate_snippets.py — so what it rests on is the three rules it enforces (type25-003, type25-007, type25-008), each of which carries its own proposal on this page, and the ruling that promoted them. A principle here would be a category error.",
 opts=[]),

# --- web-foundations.md --------------------------------------------------------------
"webf-011": dict(rec="a", rq="0 = base content (body, imagery, cards, buttons — NEVER elevated)",
 null="A four-level taxonomy is a system construction, and the panel could legally call the numbering convention.",
 opts=[("pr-gestalt-figure-ground", "People separate a scene into a foreground object and a background, and ambiguity here is disorienting",
        "The taxonomy is a declared depth order, and its whole job is to stop two things claiming the same layer, which is the ambiguity the principle says disorients."),
       ("pr-mental-model", "People act on a compressed internal model of how the system works",
        "Read as a model rule, four named levels are a depth model simple enough for a reader to hold and predict.")]),

"webf-013": dict(rec="a", rq="No purely aesthetic shadows (inner or outer) — elevation is functional",
 null="The rule states the functional meaning in its own clause.",
 opts=[("pr-norman-signifier", "the perceivable cue that tells someone where and how to act",
        "Elevation is a cue that says this thing is over that thing and can move; used decoratively it is a cue with nothing behind it."),
       ("pr-gestalt-figure-ground", "ambiguity here is disorienting",
        "Read perceptually, shadows on things that are not raised invent layers and leave the reader unsure what is on top.")]),

"webf-018": dict(rec="c", rq="Base unit 4px",
 null="A chosen modulus. Four is divisible, halves cleanly and matches the platforms' own grids, but no graded principle predicts four rather than five or eight — the value of a base unit is that it is agreed, which is the definition of a convention.",
 opts=[]),

"webf-027": dict(rec="a", rq="padding/margins follow the system (e.g. 16px gutters → 16px card side-padding)",
 null="The 4px modulus itself is convention — webf-018 says so — but this rule is about what the spacing does, which is a principle.",
 opts=[("pr-gestalt-proximity", "Elements placed close together are seen as one group before anything else about them is processed",
        "Spacing is the grouping signal, and a shared scale is what makes the same gap mean the same degree of belonging in every layout."),
       ("pr-idp-be-consistent", "Use familiar conventions and apply them consistently across the service",
        "Read as a system rule, tying padding to the grid's own gutters is what keeps one service from looking like six.")]),
}

# ---------------------------------------------------------------- load + ground
def load():
    rn = json.loads(RULES.read_text())
    ux = json.loads(UX.read_text())
    rules = {n["ruleId"]: n for n in rn["nodes"]
             if n["id"].startswith("rule:") and n.get("destiny") == "BLOCKING"}
    prin = {n["uxId"]: n for n in ux["nodes"] if n["id"].startswith("ux:")}
    return rules, prin


def build(rules, prin):
    errs = []
    if set(P) != set(rules):
        errs.append("proposal set != BLOCKING set: missing %s / extra %s"
                    % (sorted(set(rules) - set(P)), sorted(set(P) - set(rules))))
    out = []
    for rid in sorted(rules, key=lambda r: (rules[r]["file"], r)):
        rule, p = rules[rid], P[rid]
        if p["rq"] not in rule["text"]:
            errs.append("%s: rule quote not in text: %r" % (rid, p["rq"]))
        opts = []
        for i, (uid, pq, why) in enumerate(p["opts"]):
            n = prin.get(uid)
            if not n:
                errs.append("%s: no such principle %s" % (rid, uid))
                continue
            if pq not in n["statement"]:
                errs.append("%s/%s: principle quote not in statement: %r" % (rid, uid, pq))
            if not why.endswith("."):
                errs.append("%s/%s: why is not one full sentence" % (rid, uid))
            opts.append({
                "choice": "ab"[i], "uxId": uid, "grade": n["grade"],
                "gradeName": n.get("gradeName", ""), "statement": n["statement"],
                "originator": n.get("originator", ""),
                "scope_conditions": n.get("scope_conditions", ""),
                "principleClause": pq, "why": why,
                "recommended": (p["rec"] == "ab"[i]),
            })
        out.append({
            "ruleId": rid, "file": rule["file"], "ruleText": rule["text"],
            "ruleClause": p["rq"], "destiny": "BLOCKING",
            "options": opts, "null": {"why": p["null"], "recommended": p["rec"] == "c"},
            "recommend": p["rec"],
        })
    if errs:
        print("GROUNDING FAILED:\n  " + "\n  ".join(errs), file=sys.stderr)
        sys.exit(1)
    return out


# ---------------------------------------------------------------- the page
CSS = """
:root{--accent:#DB0011;--black:#000;--white:#fff;--grey-1:#F3F3F3;--grey-2:#EDEDED;--grey-3:#D7D8D6;--grey-5:#9B9B9B;--grey-6:#767676;--grey-7:#545454;--grey-8:#333;--ok:#0B6E3A;
--s1:.5rem;--s2:1rem;--s3:1.5rem;--s4:2rem;--s5:3rem;--s6:4rem;--s7:6rem;--max:1200px;--gutter:2rem}
*{box-sizing:border-box}
body{margin:0;background:var(--white);color:var(--black);font:400 1rem/1.75 "Helvetica Neue",Helvetica,Arial,sans-serif}
.wrapper{max-width:var(--max);margin:0 auto;padding:0 var(--gutter)}
nav{position:sticky;top:0;z-index:9;background:var(--white);border-bottom:1px solid var(--grey-2)}
nav .wrapper{display:flex;align-items:center;justify-content:space-between;height:54px;gap:var(--s3)}
nav a,nav span{font-size:.875rem;letter-spacing:.05em;color:var(--grey-6);text-decoration:none}
nav .now{color:var(--black);font-weight:500}
nav .jump{display:flex;gap:var(--s3);overflow:hidden}
section{padding:var(--s7) 0;border-bottom:1px solid var(--grey-2)}
.label{font-size:.75rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);display:flex;align-items:center;gap:var(--s1);margin:0 0 var(--s3)}
.label::before{content:"";display:inline-block;width:20px;height:1px;background:var(--accent);flex:none}
h1{font-size:3.5625rem;line-height:1.05;font-weight:400;margin:0 0 var(--s4);max-width:22ch}
h2{font-size:2.125rem;line-height:1.15;font-weight:400;margin:0 0 var(--s4)}
h3{font-size:1.1875rem;line-height:1.35;font-weight:500;margin:0 0 var(--s3);max-width:60ch}
p{margin:0 0 var(--s3);max-width:72ch}
.lede{font-size:1.1875rem;line-height:1.7;max-width:60ch}
.meta{font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--grey-6);margin:0}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--s4);margin-top:var(--s6)}
.stats div b{display:block;font-size:2.6875rem;font-weight:200;line-height:1}
.stats div span{display:block;font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--grey-6);margin-top:var(--s2)}
.spread{margin-top:var(--s5);border-top:1px solid var(--black);max-width:72ch}
.spread div{display:grid;grid-template-columns:5rem 1fr auto;gap:var(--s3);padding:var(--s2) 0;border-bottom:1px solid var(--grey-2);font-size:.9375rem}
.spread b{font-weight:500}
.spread span{color:var(--grey-7)}
.grouphead{padding:var(--s6) 0 var(--s3);border-bottom:1px solid var(--black);margin-bottom:0}
.grouphead h2{margin:0 0 var(--s1);font-size:1.5rem}
.grouphead p{margin:0;font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--grey-6)}
.card{display:grid;grid-template-columns:1fr 2fr;gap:var(--s6);align-items:start;padding:var(--s5) 0;border-bottom:1px solid var(--grey-2)}
.card>div{min-width:0}
.opt>div{min-width:0}
code{overflow-wrap:anywhere}
h3,.plain,.sub,b{overflow-wrap:break-word}
.idx{font-size:3.5625rem;font-weight:100;line-height:.9;color:var(--grey-3);margin-bottom:var(--s2)}
.rid{font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--grey-6);margin:0 0 var(--s3)}
.restson{font-size:.875rem;color:var(--grey-7);border-top:1px solid var(--grey-2);padding-top:var(--s3);margin:0}
.restson span{display:block;font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--grey-6);margin-bottom:var(--s1)}
.plain{font-size:1.0625rem;line-height:1.7}
.said{border-left:2px solid var(--accent);padding-left:var(--s3);margin:0 0 var(--s3)}
.said span{display:block;font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--grey-6);margin-bottom:var(--s1)}
.gradechip{display:inline-block;font-size:.6875rem;letter-spacing:.12em;text-transform:uppercase;color:var(--grey-6);border:1px solid var(--grey-3);padding:2px 8px;margin-left:var(--s1)}
details.tech{margin:var(--s3) 0 0;font-size:.875rem;color:var(--grey-7);max-width:72ch}
details.tech summary{cursor:pointer;font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--grey-6);font-weight:500;padding:var(--s2) 0}
details.tech code{font:400 .8125rem/1.6 Menlo,monospace}
details.tech p{margin:0 0 var(--s2)}
.opts{margin-top:var(--s4);border-top:1px solid var(--black)}
.opt{display:grid;grid-template-columns:auto 1fr;gap:var(--s2) var(--s3);padding:var(--s3) 0;border-bottom:1px solid var(--grey-2);cursor:pointer;align-items:start}
.opt input{margin:6px 0 0;flex:none}
.opt b{font-weight:500;display:block}
.opt .tag{font-size:.6875rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ok);font-weight:500;margin-left:var(--s2)}
.opt .sub{font-size:.875rem;color:var(--grey-7);line-height:1.6;margin-top:var(--s1)}
.opt input[type=text]{width:100%;max-width:32rem;font:400 .9375rem/1.6 inherit;padding:var(--s1) 0;border:none;border-bottom:1px solid var(--grey-3);background:none;color:var(--black);margin-top:var(--s1)}
label.note{display:block;margin-top:var(--s3)}
label.note span{display:block;font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--grey-6);margin-bottom:var(--s1)}
label.note input{width:100%;max-width:46rem;font:400 .9375rem/1.6 inherit;padding:var(--s1) 0;border:none;border-bottom:1px solid var(--grey-3);background:none;color:var(--black)}
label.note input:focus,.opt input[type=text]:focus{outline:none;border-bottom-color:var(--accent)}
.grey{background:var(--grey-1)}
button{font:500 .875rem/1 inherit;letter-spacing:.06em;text-transform:uppercase;padding:14px 22px;border:none;background:var(--black);color:var(--white);cursor:pointer}
button.ghost{background:none;color:var(--black);border-bottom:1px solid var(--accent);padding:14px 0;margin-left:var(--s4)}
pre{background:var(--white);padding:var(--s3);overflow:auto;font:400 .8125rem/1.6 Menlo,monospace;max-height:26rem;border:1px solid var(--grey-2)}
#msg{font-size:.875rem;color:var(--grey-7);margin-left:var(--s3)}
#count{font-size:.875rem;color:var(--grey-7)}
footer{padding:var(--s6) 0;font-size:.75rem;letter-spacing:.06em;color:var(--grey-6)}
@media (max-width:900px){
 :root{--gutter:1rem}
 h1{font-size:2.125rem} h2{font-size:1.5rem}
 section{padding:var(--s5) 0}
 nav .jump{display:none}
 .stats{grid-template-columns:repeat(2,1fr);gap:var(--s3)}
 .card{grid-template-columns:1fr;gap:var(--s3)}
 .idx{font-size:2.6875rem;margin-bottom:var(--s1)}
 .spread div{grid-template-columns:3.5rem 1fr auto;gap:var(--s2)}
 button.ghost{margin-left:0;display:block;margin-top:var(--s2)}
 .opt input[type=text]{max-width:100%}
}
"""

FILE_TITLES = {
    "accessibility-content-authoring.md": "Accessibility — content authoring",
    "accessibility-interaction-design.md": "Accessibility — interaction design",
    "accessibility-visual-design.md": "Accessibility — visual design",
    "app-foundations.md": "App foundations",
    "brand-refresh-assets.md": "Brand refresh assets",
    "colour-standards-2026.md": "Colour standards 2026",
    "data-visualisation-bar-charts.md": "Data visualisation — bar charts",
    "data-visualisation-line-charts.md": "Data visualisation — line charts",
    "data-visualisation-pie-charts.md": "Data visualisation — pie charts",
    "data-visualisation.md": "Data visualisation",
    "icons.md": "Icons",
    "illustration-standards.md": "Illustration standards",
    "motion-standards.md": "Motion standards",
    "naming.md": "Naming",
    "neurodiversity.md": "Neurodiversity",
    "pictograms.md": "Pictograms",
    "tone-of-voice.md": "Tone of voice",
    "typography-standards-2026.md": "Typography standards 2026",
    "typography-usage.md": "Typography usage",
    "web-foundations.md": "Typography usage — web foundations",
}
FILE_TITLES["web-foundations.md"] = "Web foundations"

GRADE_WORDS = {
    "A": "grade A — replicated, a measured law",
    "B": "grade B — studied, a real effect with limits",
    "C": "grade C — practised, agreed guidance rather than measurement",
    "D": "grade D — doubted",
    "L": "grade L — an obligation in law or standard",
}


def e(s):
    return html.escape(s, quote=True)


def page(props, prin):
    n = len(props)
    withp = [p for p in props if p["recommend"] != "c"]
    conv = [p for p in props if p["recommend"] == "c"]
    spread = {}
    carriers = {}
    for p in withp:
        rec = [o for o in p["options"] if o["recommended"]][0]
        spread[rec["grade"]] = spread.get(rec["grade"], 0) + 1
        carriers.setdefault(rec["uxId"], []).append(p["ruleId"])
    nradio = sum(len(p["options"]) + 2 for p in props)

    h = []
    a = h.append
    a('<!DOCTYPE html>\n<html lang="en"><head>')
    a('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">')
    a("<title>What each blocking rule rests on — fifty-nine proposals — #281</title>")
    a("<style>" + CSS + "</style></head><body>")

    groups = []
    for p in props:
        if not groups or groups[-1][0] != p["file"]:
            groups.append((p["file"], []))
        groups[-1][1].append(p)

    a('<nav><div class="wrapper"><span>#281 · rests on</span>'
      '<span class="now">59 blocking rules</span>'
      '<span class="jump"><a href="#top">Top</a><a href="#cards">The rules</a>'
      '<a href="#export">Export</a><span id="count"></span></span></div></nav>')

    # ---- header
    a('<section id="top"><div class="wrapper">')
    a('<p class="label">The proposals</p>')
    a("<h1>Fifty-nine rules, and what each one rests on.</h1>")
    a('<p class="lede">You said start with the fifty-nine blocking rules and bring a page. '
      "Here they are, one card each: the rule in its own words, the principle I think it rests on, "
      "one sentence of why, and the grade that principle carries. "
      "Nothing is drawn in the graph until this page comes back from you.</p>")
    a('<p class="plain">A card is not asking whether the rule is right. The rule is already blocking and stays blocking. '
      "It is asking what the rule's <em>reason</em> is — the thing a designer gets when they ask why the pie stops at six slices "
      "and today gets nothing. Where two reasons compete I have put both and marked the one I would take. "
      "Where nothing in the register honestly explains the rule, the card says so: "
      "<em>convention — no principle</em> is a real answer, not a gap, and %d of the fifty-nine get it.</p>" % len(conv))
    a('<p class="plain">Take all the recommendations at the bottom if you agree with the shape of it, '
      "then change the ones you do not, and send the file back. Where you pick something other than my recommendation "
      "the export records that you overruled me, so the record shows it.</p>")
    a('<div class="stats">')
    a("<div><b>%d</b><span>blocking rules</span></div>" % n)
    a("<div><b>%d</b><span>with a proposed principle</span></div>" % len(withp))
    a("<div><b>%d</b><span>convention — no principle</span></div>" % len(conv))
    a("<div><b>%d</b><span>offered a second reading</span></div>"
      % len([p for p in props if len(p["options"]) > 1]))
    a("</div>")
    a('<div class="spread">')
    for g in ["A", "B", "C", "L", "D"]:
        if spread.get(g):
            a("<div><b>%s</b><span>%s</span><span>%d rules</span></div>"
              % (g, e(GRADE_WORDS[g].split("—")[1].strip()), spread[g]))
    a("<div><b>—</b><span>convention, no principle named</span><span>%d rules</span></div>" % len(conv))
    a("</div>")
    top = sorted(carriers.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:5]
    a('<p class="meta" style="margin-top:2rem">Carrying the most rules: '
      + " · ".join("%s %d" % (e(prin[u]["statement"].rstrip(".").split(",")[0][:46]), len(r))
                        for u, r in top) + "</p>")
    a("</div></section>")

    # ---- cards
    a('<div id="cards"></div>')
    i = 0
    for fname, items in groups:
        a('<section><div class="wrapper">')
        a('<div class="grouphead"><h2>%s</h2><p>%s · %d blocking rule%s</p></div>'
          % (e(FILE_TITLES.get(fname, fname)), e(fname), len(items), "" if len(items) == 1 else "s"))
        for p in items:
            i += 1
            rid = p["ruleId"]
            rec = None
            for o in p["options"]:
                if o["recommended"]:
                    rec = o
            a('<div class="card" id="c-%s">' % e(rid))
            a("<div>")
            a('<div class="idx">%02d</div>' % i)
            a('<p class="rid">%s</p>' % e(rid))
            if rec:
                a('<p class="restson"><span>Rests on</span>%s<span class="gradechip">%s</span></p>'
                  % (e(rec["statement"]), e(GRADE_WORDS[rec["grade"]])))
            else:
                a('<p class="restson"><span>Rests on</span>Convention alone. '
                  "No principle in the register honestly explains this one.</p>")
            a("</div>")
            a("<div>")
            a('<h3>%s</h3>' % e(p["ruleText"]))
            if rec:
                a('<div class="said"><span>Why I think it rests there</span>'
                  '<p class="plain" style="margin:0">%s</p></div>' % e(rec["why"]))
            else:
                a('<div class="said"><span>Why there is no principle</span>'
                  '<p class="plain" style="margin:0">%s</p></div>' % e(p["null"]["why"]))
            # technical fold
            a('<details class="tech"><summary>Technical</summary>')
            a("<p><code>rule:%s</code> — <code>%s</code>, destiny BLOCKING. "
              "The clause of the rule that carries the link: “%s”.</p>"
              % (e(rid), e(p["file"]), e(p["ruleClause"])))
            for o in p["options"]:
                a("<p><code>restsOn → ux:%s</code> (grade %s, %s; %s). "
                  "The clause of the statement that carries the link: “%s”. "
                  "Scope: %s</p>"
                  % (e(o["uxId"]), e(o["grade"]), e(o["gradeName"]), e(o["originator"] or "—"),
                     e(o["principleClause"]), e(o["scope_conditions"] or "not recorded")))
            if not p["options"]:
                a("<p><code>restsOn → ref:null</code> with the note above — the declared-null shape of "
                  "<code>s275-D2</code> (RP-2 option a), a legal answer, never a dropped row.</p>")
            a("</details>")
            # options
            a('<div class="opts">')
            for o in p["options"]:
                tag = '<span class="tag">recommended</span>' if o["recommended"] else ""
                a('<label class="opt"><input type="radio" name="%s" value="%s"><div>'
                  '<b>%s<span class="gradechip">%s</span>%s</b>'
                  '<div class="sub">%s</div></div></label>'
                  % (e(rid), o["choice"], e(o["statement"]), e(GRADE_WORDS[o["grade"]]), tag, e(o["why"])))
            ctag = '<span class="tag">recommended</span>' if p["recommend"] == "c" else ""
            a('<label class="opt"><input type="radio" name="%s" value="c"><div>'
              '<b>Convention — no principle%s</b><div class="sub">%s</div></div></label>'
              % (e(rid), ctag, e(p["null"]["why"])))
            a('<label class="opt"><input type="radio" name="%s" value="d"><div>'
              '<b>Another principle — name it</b>'
              '<input type="text" id="other-%s" placeholder="the principle you would rest it on, in your words">'
              "</div></label>" % (e(rid), e(rid)))
            a("</div>")
            a('<label class="note"><span>Note</span>'
              '<input type="text" id="note-%s" placeholder="optional — your words, kept verbatim"></label>' % e(rid))
            a("</div></div>")
        a("</div></section>")

    # ---- export
    a('<section class="grey" id="export"><div class="wrapper">')
    a('<p class="label">Export</p>')
    a("<h2>Send the answers back</h2>")
    a("<p>One choice per rule. Nothing is inscribed in the graph until the file comes back — the ruling "
      "already says the lines land only on your export of this page. The export carries your pick and my "
      "recommendation side by side, so the record shows where you overruled me.</p>")
    a('<p><button id="takeall" type="button">Take all the recommendations</button>'
      '<button id="dl" class="ghost" type="button">Download the answers</button>'
      '<button id="cp" class="ghost" type="button">Copy to clipboard</button><span id="msg"></span></p>')
    a('<pre id="exp" hidden></pre>')
    a("</div></section>")
    a('<footer><div class="wrapper">#281 · notes/_lanes/281/rests-on/%s.html · '
      "proposed, not ruled · %d cards · %d radios</div></footer>" % (PAGE, n, nradio))

    ids = [p["ruleId"] for p in props]
    rec_map = {}
    ux_map = {}
    for p in props:
        rec_map[p["ruleId"]] = p["recommend"]
        ux_map[p["ruleId"]] = {o["choice"]: o["uxId"] for o in p["options"]}
    a("<script>")
    a('var PAGE=%s;' % json.dumps(PAGE))
    a("var IDS=%s;" % json.dumps(ids))
    a("var REC=%s;" % json.dumps(rec_map))
    a("var UX=%s;" % json.dumps(ux_map))
    a("""
function state(id){var r=document.querySelector('input[name="'+id+'"]:checked');
 var c=r?r.value:null;var n=document.getElementById('note-'+id);var o=document.getElementById('other-'+id);
 var ux=null;if(c&&UX[id]&&UX[id][c])ux=UX[id][c];else if(c==='d')ux=(o&&o.value.trim())||null;
 return {choice:c,uxId:ux,note:(n&&n.value)||"",recommended:REC[id],overruled:c!==null&&c!==REC[id]}}
function envelope(){var a={};IDS.forEach(function(id){a[id]=state(id)});
 return {exportedAt:new Date().toISOString(),page:PAGE,answers:a}}
function show(){var j=JSON.stringify(envelope(),null,2);var p=document.getElementById('exp');p.hidden=false;p.textContent=j;return j}
function tally(){var d=0;IDS.forEach(function(id){if(document.querySelector('input[name="'+id+'"]:checked'))d++});
 document.getElementById('count').textContent=d+'/'+IDS.length}
document.getElementById('takeall').onclick=function(){IDS.forEach(function(id){
 var el=document.querySelector('input[name="'+id+'"][value="'+REC[id]+'"]');if(el)el.checked=true});
 tally();show();document.getElementById('msg').textContent='all '+IDS.length+' set to the recommendation \\u2014 change any before you export'};
document.getElementById('dl').onclick=function(){var j=show();var a=document.createElement('a');
 a.href=URL.createObjectURL(new Blob([j],{type:'application/json'}));a.download=PAGE+'-export.json';a.click();
 document.getElementById('msg').textContent='downloaded'};
document.getElementById('cp').onclick=function(){var j=show();try{if(navigator.clipboard&&navigator.clipboard.writeText){
 var w=navigator.clipboard.writeText(j);if(w&&w["catch"])w["catch"](function(){})}}catch(e){}
 document.getElementById('msg').textContent='copied \\u2014 the JSON is below too'};
document.addEventListener('change',function(){tally();if(!document.getElementById('exp').hidden)show()});
document.addEventListener('input',function(){if(!document.getElementById('exp').hidden)show()});
tally();
""")
    a("</script>")
    a("</body></html>")
    return "\n".join(h), nradio, spread, carriers, conv


def main():
    rules, prin = load()
    props = build(rules, prin)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "proposals.json").write_text(json.dumps({
        "$what": "#281 lane RO — PROPOSED restsOn links, one per BLOCKING rule. "
                 "Proposals only: nothing here is an edge, and nothing lands until Dave's export "
                 "of RESTS-ON-2026-09-17.html comes back (s281-D3).",
        "ruling": "s281-D3",
        "date": DATE,
        "page": "notes/_lanes/281/rests-on/%s.html" % PAGE,
        "generated_by": "notes/_lanes/281/rests-on/gen_rests_on.py",
        "counts": {
            "rules": len(props),
            "withPrinciple": len([p for p in props if p["recommend"] != "c"]),
            "convention": len([p for p in props if p["recommend"] == "c"]),
            "withAlternative": len([p for p in props if len(p["options"]) > 1]),
        },
        "proposals": props,
    }, indent=1, ensure_ascii=False) + "\n")
    doc, nradio, spread, carriers, conv = page(props, prin)
    (OUT / ("%s.html" % PAGE)).write_text(doc)
    print("cards %d  radios %d  convention %d  spread %s"
          % (len(props), nradio, len(conv), spread))
    for u, r in sorted(carriers.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:8]:
        print("   %-28s %2d  %s" % (u, len(r), " ".join(r)))
    print("   convention:", " ".join(p["ruleId"] for p in conv))


if __name__ == "__main__":
    main()
