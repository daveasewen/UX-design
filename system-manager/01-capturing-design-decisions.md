# 01 — Capturing design decisions

**Status:** draft for review · **Date:** 2026-06-22 · **Author:** Dave + Claude
**Subject:** As the design system matures and feeds several projects, how are
decisions made, captured, and executed?

---

## 0. Your proposal, stated fairly

> A formalised decision meeting over Zoom with multiple actors. The AI summary of
> that meeting is the *ingest* — not the record: a model processes it into
> proposed changes (context, design changes, new components), a human signs those
> off, and only then do they enter the system, with notifications to the relevant
> actors. In short: **a group of humans decide → the meeting is auto-captured as
> raw input → a model drafts the changes → a human signs off → the system updates.**

The instinct is sound. Humans hold the decision; capture is automated; humans
stay in the loop on the way in and the way out. That matches this project's core
philosophy — *"HITL gates are designed components, not fallbacks"* and *memory is
"committed only via the configured update policy — never silently."* So we're
not arguing about direction. We're arguing about where it breaks.

This document does three things: (1) shows what you **already have** so we don't
rebuild it, (2) stress-tests the flow — one part already aligned, six places to
tighten — and (3) proposes a **model that keeps your instinct**. Prior art is in §4.

---

## 1. You already have most of a decision spine — don't rebuild it

Before designing anything new, note that the repo already contains four of the
pieces this needs. The job is mostly to *connect and extend*, not invent.

| Existing piece | Where | What it already does for decisions |
|---|---|---|
| **ADRs** | `docs/decisions/ADR-*.md` | Append-only, one-decision-per-file record with context/decision/rationale/consequence. This *is* a decision log. |
| **Promotion queue** | `knowledge/_PROMOTION-QUEUE.md` | The explicit "blessed by Dave → enters canon" path. A decision-execution mechanism, already human-gated. |
| **canon / memory / `taste.md` split** | `archive/harness-v0.1/harness/state/`, `…/hitl.md` (archived — see ADR-0005) | Authoritative facts vs learned preferences vs human judgment. Defines *who may write what*. |
| **Component graph + xref index** | `knowledge/components/*.meta.json`, `knowledge/_XREF-INDEX.json` | The dependency map — i.e. the blast-radius engine for "what does this change break?" |

The gap is not "we have no way to record decisions." The gap is: the existing
records are about *the harness* (ADRs) and *single component promotions*
(the queue). There is no record type for a **cross-cutting design decision made
by a group that affects several downstream projects** — which is exactly what you
described. That's the thing to build.

---

## 2. Stress-testing the flow: what holds, what to tighten

### 2.1 We're aligned here: the AI drafts, a human signs off
Worth stating up front because it's the load-bearing principle — and it's already
in your design. The Zoom summary is *ingest*, not the record: a model turns it into
proposed changes, and a named human signs those off before anything enters the
system. Keep it exactly that way. It matters because an AI summary captures
*discussion*, not *decisions*, and can be wrong even with retrieval grounding; in a
regulated context (your HSBC surface) the gap between an auto-transcript and the
signed record is itself a governance risk (§4). Your own `memory.md` states the same
rule for the learning store — never commit silently. The six points below are where
the flow genuinely needs tightening.

### 2.2 The flow conflates the *decision* with its *execution*
"AI summary → context changes, design changes, new components → approved" mixes
two different objects:

- **The decision** ("we will adopt a 4px base grid", "tabs replace segmented
  controls for ≤5 options") — made once, rarely, by people with decision rights.
- **The execution** (the token edit, the new component, the doc rewrite, the
  migration in each consuming product) — many changes, over time, each needing a
  *craft* check, not a re-vote on the decision.

If you collapse them, one of two bad things happens: either every code change
re-litigates the decision, or a single approval rubber-stamps downstream changes
nobody has actually seen yet. Your repo already separates these (ADR = decision;
promotion/PR = execution). Keep them separate by design.

### 2.3 "Approved by a system manager" is a single point of failure
One manager approving everything is the model Nathan Curtis calls the *overlord* —
and "overlords don't scale" (§4). The moment the system feeds several projects,
that person is the bottleneck and the bus-factor. You need a **governance model**
decision *first*: centralised, federated, or hybrid. (Recommendation in §3.)

### 2.4 "Notify everyone to approve the executions" → approval fatigue
If every actor must approve every execution, you get rubber-stamping and
resentment, and the gate stops meaning anything. Most actors don't need to
*approve* — they need to be *informed* ("a breaking change to `Input` lands in
v3, here's the migration window"). Mixing "approve" and "inform" into one
notification is how governance processes die. You need explicit **decision rights**
(who decides / who is consulted / who is merely informed — a RACI-style split).

### 2.5 No impact analysis / blast radius
"The design system feeds several projects" is the whole reason this is hard, yet
the flow has no step that asks *"what does this decision break, and for whom?"*
before it's ratified. A change to one component can ripple across N products. You
already hold the dependency data (`_XREF-INDEX.json`, component meta) — a decision
record should carry a computed impact assessment and a **semver class**
(patch / minor / breaking). Breaking changes need a deprecation window and a
migration note, not a Slack ping.

### 2.6 Provenance isn't audit-grade
In a regulated context you need to reconstruct, later: who was in the room, what
options were considered, why this one won, what it superseded. An AI summary alone
gives none of that reliably. ADR practice already gives you the shape: append-only,
*supersede don't edit*, link related records (§4). The decision record must carry
participants, date, options-rejected, rationale, impact, and supersedes/superseded-by.

### 2.7 Over-formalising, and the "pipeline OR separate app" ambiguity
Two traps here. First, **not every decision deserves a Zoom summit** — over-ceremony
makes people route around the process. Tier it: a maintainer can make and log a
reversible ("two-way door") call solo; only significant or hard-to-reverse
("one-way door") decisions trigger the formal meeting. Second, your "(or a separate
design-system manager)" aside hides a real fork: **don't build a bespoke app first.**
The "system manager" should start as a *role + a thin Git-based process* using the
machinery you already have. Automation/UI comes later, only if the process proves
it's needed. This is your own "deliberate simplicity" principle.

---

## 3. A model that keeps your instinct

### 3.1 The unit of capture: a Design Decision Record (DDR)
Extend the ADR pattern you already use into a sibling record type for *design
system* decisions. It lives in Git (the source of truth), append-only, one
decision per file — `system-manager/decisions/DDR-NNNN-*.md`. The meeting produces
a *draft* DDR (AI-assisted from the transcript); a named human owner edits and
ratifies the final text. The decision is the file, not the summary.

A DDR carries: title · status · date · **deciders / consulted / informed** ·
context · options considered (incl. rejected) · the decision · **impact &
blast-radius** · **semver class** · rationale · `supersedes` / `superseded-by`.

### 3.2 The lifecycle (six stages, mapped to what exists)

```
 PROPOSE → DISCUSS → RATIFY → EXECUTE → COMMUNICATE → REVIEW
   │         │         │         │           │           │
 anyone   the mtg;   owner +   federated:  deciders   does it
 opens a  AI drafts  deciders  consuming   approved;  stick?
 stub     the DDR    sign the  teams ship  consumers  escalations
 (tiered) (= input)  DDR text  via gates   *informed* feed taste.md
                     +impact   (craft/a11y +migration  → supersede
                     +semver   /taste)     window      if not
```

| Stage | What happens | Reuses |
|---|---|---|
| **Propose** | Anyone opens a DDR stub. Trigger is *tiered* by reversibility/blast-radius — small reversible calls skip the meeting and are just logged. | new `decisions/` |
| **Discuss** | The Zoom meeting. AI captures transcript + drafts the DDR. This is **input**, never the record. | AI assist |
| **Ratify** | The decision owner + named deciders approve the DDR text. Impact assessment (from the xref graph) and semver class are attached here. | `_XREF-INDEX`, component meta |
| **Execute** | Consuming teams/maintainers implement via PRs/promotions — each passing the *existing* craft / a11y / taste gates. The DDR links to them. | promotion queue, HITL gates, contracts |
| **Communicate** | Deciders' approval is recorded; consumers are **informed** (changelog + migration window for breaking changes). Not asked to re-approve. | versioning/changelog |
| **Review** | If a decision keeps getting re-opened or keeps causing escalations, that pattern feeds `taste.md` and the DDR is superseded. | `taste.md`, memory |

### 3.3 Governance: centralised *ratification* + federated *execution*
Given it feeds several projects, the hybrid model fits best (§4): a small core
holds **decision rights and ratification** (high-leverage, low-volume); consuming
teams hold **execution** (high-volume, gated by automated craft checks, not by the
core's manual approval). This dissolves the bottleneck in 2.3 and the approval
fatigue in 2.4 simultaneously.

### 3.4 Decision rights, explicitly
Every DDR names its deciders (accountable, must approve), consulted (input
sought), and informed (told, not asked). "Notify the relevant actors to approve"
becomes: **deciders ratify; everyone else is informed.** Approval is scarce and
therefore means something.

### 3.5 The AI's role: assistive, never authoritative
The AI may: draft the DDR from the transcript, compute blast-radius from the xref
graph, classify the semver impact, draft the migration note, and route
notifications. The AI may **not**: ratify a decision, write canon silently, or be
the record. Every place the AI touches the system of record, a human owns the
commit — consistent with the harness today.

---

## 4. Prior art — others have attempted versions of this

**Decision records as a practice.** ADRs are the established pattern for capturing
"architecturally significant" decisions: one decision per file, append-only, and
crucially *supersede-don't-edit* so history is preserved. Guidance also warns to
keep the deciding group small (<10) and to only record hard-to-reverse decisions —
both directly relevant to your tiering and decision-rights questions. ([adr.github.io](https://adr.github.io/), [Microsoft](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record), [AWS](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/), [Martin Fowler](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html))

**Design-system governance models.** Nathan Curtis's centralised / federated /
hybrid framing is the canonical reference, including the warning that "overlords
don't scale" and the case for a dedicated core plus embedded contributors with a
defined contribution process. This is the literature behind §3.3. ([EightShapes — team models](https://medium.com/eightshapes-llc/team-models-for-scaling-a-design-system-2cf9d03be6a0), [Defining Contributions](https://medium.com/eightshapes-llc/defining-design-system-contributions-eb48e00e8898), [The Fallacy of Federated Design Systems](https://medium.com/@nathanacurtis/the-fallacy-of-federated-design-systems-23b9a9a05542))

**Communicating change downstream.** The execution/communicate half maps to
established versioning practice: semantic versioning, library-vs-component
versioning, gradual deprecation with end-of-life dates, and changelogs generated
from conventional commits. Tokens act as "a contract: change the contract and
every downstream consumer updates" — which is exactly why a *breaking* DDR needs a
migration window, not a notification. ([EightShapes — Versioning](https://medium.com/eightshapes-llc/versioning-design-systems-48cceb5ace4d), [SemVer](https://semver.org/), [Supernova — versioning examples](https://www.supernova.io/blog/8-examples-of-versioning-in-leading-design-systems), [Single source of truth](https://designsystems.surf/guides/single-source-of-truth))

**AI meeting tools as a governance risk.** The legal/governance literature is
explicit that AI meeting transcripts and summaries create new risks: discrepancies
between an AI transcript and the formal minutes can be used against you, and
AI outputs flowing into decision pipelines "without structured review" escalate
fast — the recommended mitigation is exactly approval gates + human-in-the-loop
validation. This is the evidence behind problem 2.1. ([White & Case](https://www.whitecase.com/insight-alert/when-every-word-recorded-ai-meeting-tools-and-new-governance-risks), [Thomson Reuters](https://www.thomsonreuters.com/en/insights/articles/accuracy-in-ai))

**Net read:** nobody has a turnkey "meeting → auto-ingested design system" product
that's trustworthy, and the serious sources all converge on the same correction —
keep the decision record human-authored, keep the deciding group small, separate
deciding from executing, and version/communicate change deliberately. Your
instinct is mainstream; the AI-summary-as-record shortcut is the part the field
warns against.

---

## 5. Open questions for you (these are yours to decide)

1. **Governance model** — confirm hybrid (centralised ratification + federated
   execution), or do you want a different split?
2. **Where DDRs live** — extend `docs/decisions/` (one log for everything) or keep
   a separate `system-manager/decisions/` for design-system decisions? (I lean
   separate: different audience, different cadence.)
3. **Who are the deciders** — for a typical cross-cutting decision, name the roles
   that must approve vs. are consulted vs. informed.
4. **Trigger tiers** — what's the line between "log it solo" and "convene the
   meeting"? (Suggest: reversibility × number of consuming projects affected.)

## 6. Suggested next step
If the model in §3 is roughly right, the cheapest proof is a **DDR template +
one real worked example** (take an actual recent design-system decision and run it
through the six stages on paper). That tests the process with zero tooling before
we commit to building anything. I can draft both in `decisions/` on your word.

---

### Sources
- ADRs: https://adr.github.io/ · https://martinfowler.com/bliki/ArchitectureDecisionRecord.html · https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record · https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/
- Governance: https://medium.com/eightshapes-llc/team-models-for-scaling-a-design-system-2cf9d03be6a0 · https://medium.com/eightshapes-llc/defining-design-system-contributions-eb48e00e8898 · https://medium.com/@nathanacurtis/the-fallacy-of-federated-design-systems-23b9a9a05542
- Versioning & propagation: https://medium.com/eightshapes-llc/versioning-design-systems-48cceb5ace4d · https://semver.org/ · https://www.supernova.io/blog/8-examples-of-versioning-in-leading-design-systems · https://designsystems.surf/guides/single-source-of-truth
- AI-meeting governance risk: https://www.whitecase.com/insight-alert/when-every-word-recorded-ai-meeting-tools-and-new-governance-risks · https://www.thomsonreuters.com/en/insights/articles/accuracy-in-ai
