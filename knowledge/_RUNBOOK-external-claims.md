# Runbook — external claims (the three-questions gate)

*Adopted 2026-08-06 #115, candidate 3 of `_RESEARCH-graph-engineering-2026-08-05-v3.html`
§ "Worth taking" (Dave: "lets get these done now"). Source of the form: Turing Post FOD#159.
Advisory by convention, applied at writing time — a research or comparison doc that quotes an
external number without these answers carries a declared gap, not a silent one.*

## The rule

Before any external performance/accuracy/cost claim is written into a research doc, a brief,
or a ruling proposal, answer three questions **in the text, next to the claim**:

1. **What kind of thing is being measured?** (For graphs: which of the four types. Generally:
   name the mechanism, not the buzzword.)
2. **Improved compared with what?** The baseline, named. "18% better" with no baseline is
   an ASSERTED, never a DOCUMENTED.
3. **Where did the number come from?** The study, its setting, and how far that setting is
   from ours. A number from one narrow study is reported as that, never promoted into a law.

## Why this is a standing rule, not a graph rule

It is the measurement-honesty discipline already ruled for internal numbers
([[measure-dont-convert-units]] — a count is not a measurement; name the unit) extended to
numbers we did not measure. The -v3 research doc's fact-check table is the worked example:
all four viral claims failed at least one of the three questions.
