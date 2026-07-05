# ADR-0006 — The product is a *flexing* engine: one governed core, dial-settings per work-type

**Date:** 2026-07-03 · **Status:** accepted (Dave) · **Extends:** ADR-0005

> **Amended 2026-07-05 (decision audit, Tier A batch 1).** The register dial was described here
> as "cool → warm → hot", which charter **§9** (ratified the same day) superseded — register is an
> *inference ramp* (retrieve/extend/invent), **not a look**. The looks-language below is corrected
> to the §9 framing; the spine of this ADR was vouched. This amended text re-enters as `unaudited`
> and is re-audited in a later batch. See `knowledge/_DECISION-AUDIT.md`.
>
> **Re-audited 2026-07-05 (Tier A batch 2) — `validation: vouched`.** The dial correction verified
> against charter §9 line-by-line: every register mention now reads retrieve/extend/invent + "not a
> look"; no "cool/warm/hot" survives; spine untouched. See `knowledge/_DECISION-AUDIT.md`.

## Context

ADR-0005 ratified "the knowledge engine is the product; orchestration is inherited."
Before committing further, Dave re-opened the deeper question: is a governed
*designer-in-a-box* engine actually better than a **multidisciplinary agent setup**
(the archived harness — orchestrator + typed spokes + seven discipline pipelines)?

The prior desk research was recovered, not re-run: `docs/research-dossier.md`
(2026-05-31) and `ADR-0001`. Its load-bearing findings already pointed at the engine —
"simpler loops win", "don't marry a heavyweight framework", "a workflow with bounded
steps, not a free-roaming agent", structure around portable AGENTS.md + Skills + MCP
(portable data, *inherited* runtime). The pivot executed the research's own hedges;
it did not contradict them.

**The reframe that resolves the question:** the two are not competing products; they
are different layers. Disciplines survive as **criteria packs / advisory checks**, not
agent pipelines (ADR-0005 §5). So the real fork is not *one generalist vs seven
specialists* — it is **own the generation (the labour) vs own the governance (the
standard).**

## Decision

**1. Engine-over-agents, reaffirmed** — for sequencing / low-regret reasons, not because
"one generalist beats seven specialists":

- **Necessary vs optional.** Whatever generates the work, its output still has to pass
  the gates. The engine is needed in *both* worlds; the orchestrator in only one.
- **Reversibility (the clincher).** Engine-first keeps the multi-agent option fully open
  — add specialist agents *on top of* the engine later, cheap. Orchestrator-first is
  expensive, commoditising, and still needs the engine. Engine-first dominates under
  uncertainty.
- **Market.** Orchestration is commoditising (agent SDKs, 30+ SDD frameworks); design-
  system **enforcement at generation time** is the unoccupied gap (2026-07-02 scan).
- **Empirical.** The harness got one dry-run and died; the engine got 53/54 commits, is
  verified green (18/18 build, 25 gate self-tests, cold-start reproducible), and
  generalised to a second system (GOV.UK, ADR-0005 / `second-system-govuk/_FINDINGS.md`).

**2. The product shape is a FLEXING engine** — one governed core, dials set per
work-type. The flex has (at least) four dials:

- **Discovery depth** — none / quiz / full ingestion+synthesis (the maturity router).
- **Creativity register** — the inference ramp: sober (retrieve) → balanced (extend) → expressive
  (invent); charter **§9**. This is the *level of inference* the engine is licensed to use, **not a
  look** (§9 superseded the earlier "cool/warm/hot" describe-the-output framing).
- **Unit of work** — component-cluster → screen → journey.
- **Library growth** — retrieve if it exists; else generate-inside-the-curbs → gate →
  promote (compounding canon).

**3. Two named modes anchor the flex** (they map onto the org's real, bimodal work):

- **FLOOR / churn / "vibe"** — low discovery, sober register, BA-instruction in →
  compliant screen out. This is *standards-compliant Figma Make* — **the wedge.** It
  attacks the real problem (variance in designer/research/requirement quality) by making
  the quality **floor** high: sub-standard work can't ship because the gates withhold
  "done". Provable **now** — it exercises the built, verified engine and needs least of
  the unbuilt upstream.
- **CEILING / novel / "analysis"** — full discovery, register spread, journey unit,
  iteration. Augments good designers on hard problems. Depends on the still-"named-not-
  built" upstream (north-star G1 ingestion, G5 heuristics/CX/content).
- **Same curbs at every setting.** The engine is what makes the flex *safe*.

**4. Library reframe — compounding canon, not completeness.** A finite library never
"cuts it" because the design labour is *inventing novel-to-us clusters/lock-ups*.
Chasing a complete library is the alphabetical treadmill the 07-02 review flagged. The
answer is the promote loop applied to **clusters**: each novel lock-up becomes permanent
gated canon the moment it is invented once — judgment-spent-once on **composition**.
Cluster-level promotion is the **least-proven** part of the loop (tokens and motion have
been promoted; never a whole lock-up) — proving it is worth more than N hand-built
components. Build the clusters a *real journey* needs, in the order it needs them
(extends review decision 3).

**5. Front-end vision — the iteration machine.** Dave's notebook sketch, realised at
`_VISION-iteration-machine_2026-07-03.html`. A **loop**, not a linear pipeline:
Input (chat + inject + analysis/vibe toggle) → Shape (quiz) → Result (register switch on a
canon screen — the §9 inference ramp: retrieve/extend/invent) → Refine (comments + quiz) → loop. Sits beside the
north-star mock (`_VISION-northstar-front-end_2026-07-02.html`) as the more user-facing
expression. The register spread = the §9 inference ramp (retrieve/extend/invent, not a look);
**enforcement present-but-quiet is the moat** vs commodity generators (v0 / Lovable / Figma Make).

## Honesty — status of the mock

The iteration-machine file is a **facade, not wired to the engine.** Screens are hand-
authored; the gate pills, the 2.7:1 contrast figure and the Repair action are simulated
in JS; the quiz does not compile a real contract. What is *real*: the palette is
**retrieved** from `tokens/colour.json` (#DB0011 et al.), and everything it fakes exists
and runs (gates green, the contrast validator computes real ratios, the contract format
exists at `runs/contract-001-sme-payments/contract.json`, the promote loop has shipped
three times). It **proves nothing** about the engine — it is an alignment / target
artifact only. The proof lives in the gate suite, GOV.UK, and the calibration project.
Structurally verified; **not** pixel-rendered (sandbox renderer absent).

## Consequences

- The single open critical-path item is **unchanged: review decision 2** — pick the one
  real project (the calibration proof), still gated on the colleague conversation. It is
  the arbiter of the floor/ceiling weakness: if the engine breaks on *coordination*, add
  discipline agents on top; if on *thin criteria*, keep going. Re-litigating architecture
  in the abstract is the analysis-trap — the proof settles it, not more desk research.
- **The floor/churn workflow is a candidate to reshape decision 2** — real stakeholder
  who isn't Dave, highest volume, worst quality, lands squarely on the engine's built
  strengths, and is the strongest leadership demo (measurable defect/throughput).
- No architecture re-litigation without new evidence.

## Related

`ADR-0005` · `ADR-0001` · `docs/research-dossier.md` · `REVIEW-2026-07-02-critical-regroup.html` ·
`_FIXED-FLEX-CHARTER.md` · `_VISION-northstar-front-end_2026-07-02.html` ·
`_VISION-iteration-machine_2026-07-03.html` · `second-system-govuk/_FINDINGS.md`
