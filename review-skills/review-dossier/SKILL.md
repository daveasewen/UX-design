---
name: review-dossier
description: Produce a Swiss-styled, navigable HTML review dossier from a document or a set of findings — with plain-language tooltips on every acronym or piece of jargon, and two reading levels (Technical, the default, and Standard, a plain-language version for capable non-technical reviewers). Use to make any review easy to share and easy to read for both builders and stakeholders.
---

# Review dossier

Turns a review — of a document, a design, a decision, a set of findings — into a
**Swiss-styled, navigable HTML dossier** that anyone can read. Two design goals:
**least friction to share** (one self-contained file, opens in a browser) and
**readable at two levels** (a full technical view and a simplified guided view).

Build from `dossier-template.html` in this folder (copy it, fill the content).
Style follows the `swiss-design-system` skill.

## The two things that make it work

**1. Tooltips on every acronym / piece of jargon.** Wrap any term a reader might
not know so they can hover *or* keyboard-focus it to see a plain definition:

```html
<span class="term" tabindex="0" data-def="Web Content Accessibility Guidelines, level AA — the accessibility standard we build to.">WCAG AA</span>
```

Do this for **every** acronym, technical term, or internal name — no exceptions.
The definition must itself be plain (no jargon inside the tooltip).

**2. Two reading levels — write BOTH for every finding.** Each block has a
`.tech` version and a `.std` version; the toggle top-right swaps them, so nothing
is lost — the reader chooses their level.

- **Technical** (default) — full detail, precise terms, for builders.
- **Standard** — a **plain-language** version for a **capable non-technical
  reviewer/stakeholder** (someone who *uses* the outputs, not a developer). Assume
  the reader is fluent with the web, spreadsheets and everyday software — just **not
  AI-native** and not steeped in design-system internals. Write **for an adult**:
  - **Reading level ~16.** Normal adult prose — full sentences, ordinary vocabulary.
    Not simplified, not choppy, not one-idea-per-line. Precise, just not jargon-laden.
  - **Explain only what's genuinely specialist** — AI, accessibility, and
    design-system terms. Don't explain general digital literacy (what a button, a
    screen or a spreadsheet is); that's patronising. Trust the reader's competence.
  - **Complete, not dumbed down** — say every finding in full; drop the internal
    shorthand and hex codes, keep the substance and the "what to do".
  - **Orient, don't hand-hold** — a brief header note (`.guide`) on how the page is
    laid out and that specialist terms are underlined for a definition, then let them
    read. No step-by-step "take it one point at a time" walkthrough.
  - Any specialist term still gets a `.term` tooltip; the Standard prose just avoids
    reaching for jargon it doesn't need in the first place.

## Procedure
1. Take the input (a doc to review, or a list of findings + severities).
2. Copy `dossier-template.html`. Set the header (subject, date, context).
3. For each finding: a heading, a **severity chip** (red = needs fixing · amber =
   have a look · green = fine), then **both** a `.tech` and a `.std` paragraph.
4. Wrap every acronym/jargon term with the `.term` tooltip.
5. Keep it one self-contained HTML file (inline CSS/JS) so it shares with no setup.

## Output
One self-contained `*.html` dossier. Default view = Technical; the reader can flip
to Standard top-right.

## Notes
- The **Standard** view is the whole point of low-friction sharing — write it as
  carefully as the technical one; it is *not* an afterthought.
- Render and look at both modes before sharing (every real defect to date was
  visual). A future option: a **diff mode** for reviewing changes between versions.

*Experimental.*
