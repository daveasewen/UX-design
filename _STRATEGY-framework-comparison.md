# Promenaut — Framework comparison + recommendation
*Deliverable (b) from the strategy kickoff. Written 2026-06-20 by Claude + Dave.*
*Sketch-level by design — enough to make decisions, not big-design-up-front.*

---

## Summary (read this first)
**Recommendation: use spec/eval-first as the spine, and treat the other frameworks as *intake patterns* that feed it — not as competitors.** They operate at different layers, so "pick one" is a false choice. Spec/eval-first is the only one that is natively a *contract* (criteria as executable checks), which is exactly Promenaut's "verification = enforcement" principle moved upstream. The others are better at the *fuzzy front* (finding the right problem, surfacing risk) where spec/eval-first is weak.

**The honest risk with spec/eval-first:** it assumes you already know enough to write criteria. For a genuinely new problem you don't — and writing criteria too early just locks in your first guess. That's the gap the other frameworks fill. So the spine needs a divergent front-end bolted on, or it becomes premature precision.

**One sharp finding for the editor decision:** the generation/editor space is now crowded and commoditised (v0, Google Stitch (ex-Galileo), Figma Make, Lovable). Confirms the brief — do not build this. Wrap one. Your IP is upstream of where these tools start.

## Decisions LOCKED (2026-06-20)
1. **Spec/eval-first = the spine. YES.** Caveat from Dave: intake is **multi-modal / adaptive to project maturity**, not one fixed flow — a *maturity router*:
   - Seed idea → **brainstorm** (divergent) first.
   - Half-formed → **guided JTBD / assumption mapping**.
   - Well-specced → mostly **ingestion + a short quiz** to fill gaps.
   - All lanes converge on the same criteria/spec contract that feeds the gates. Several tools eventually; **don't boil the ocean** — see #2.
2. **Front-end for the prototype: entry-level / guided JTBD to start.** Hard user constraint: teams are **non-expert** in these methods (some agile + six-sigma; some continuous-discovery interviews; POs are DT-aware; designers are tactical practitioners on short sprints, not framework experts). So the tool must *guide*, not assume skill. **Build ONE lane (guided JTBD) for the prototype; router + other lanes designed-but-deferred.**
3. **Steal spec-kit's "constitution" pattern. YES.** Maps ~1:1 onto the gated canon.

---

## The comparison (compact)

| Framework | What it's good at | Where it's weak | Maps to Promenaut as… | Artifact it hands downstream → tier |
|---|---|---|---|---|
| **Spec/eval-first** (spec-kit, eval-driven dev) | Turning intent into *executable criteria before building*; criteria = gates | Assumes the problem is already understood; premature if used too early | **The spine** — criteria contract = your gates | `spec.md` + executable evals → **screen/journey tier** definition-of-done |
| **Double Diamond** | Clean mental model: diverge→converge twice; the Define gate *is* a criteria contract | High-level; doesn't tell you *how* to do any phase | Framing wrapper; `brainstorm`=Discover, `grill-me`=Define | Problem statement + success criteria → feeds the spec |
| **JTBD + assumption mapping** | Extracts jobs, contexts, **riskiest assumptions**; assumptions→testable criteria | Not a full process; needs a host framework | **Intake engine** for the divergent front | Job statements + ranked risky assumptions → become criteria/evals |
| **GV Design Sprint** | Time-boxed; "Sketch" = natural home for multi-solution gen; "Test" consumes variants | Designed for co-located humans/5 days; needs heavy adaptation for async-agent | Cadence model for the generation→test loop | N sketched variants + test signal → **variant-selection** step |
| **Lean UX / Continuous discovery (Torres)** | Keeps criteria honest against real users; opportunity-solution tree | Ongoing practice, not a project pipeline | Feedback loop that *refreshes* criteria over time | Validated/invalidated assumptions → updates the spec |

## Why spec/eval-first is the spine (and the real critique)
The strongest argument is structural, not fashion: every other framework *ends* at "here's the problem and roughly what good looks like." Spec/eval-first *starts* there and makes "what good looks like" **machine-checkable**. Your whole project thesis is that enforcement beats review. Spec/eval-first is that thesis applied to discovery — the criteria you write *are* the gates the variants must pass. Nothing else gives you that continuity from intake → generation → checks for free.

Two things to keep honest:
- **It is not a discovery method.** spec-kit and eval-driven dev both assume someone already decided what to build. If you adopt the spine without a divergent front-end, you'll write crisp criteria for the wrong problem — fast, confident, wrong. This is why #2 above is a real decision, not a formality.
- **"Evals before design" is cheap for behaviour, expensive for aesthetics.** Eval-driven dev works because code output is verifiable. Half of design output is taste, which is *not*. So the spine governs the **objective** half (states, a11y, tokens, content rules) and explicitly hands the **subjective** half to the human taste-call. Don't let the spec/eval framing tempt you into writing "evals" for beauty — that's the LLM-as-judge trap (below).

## spec-kit's "constitution" — worth stealing
spec-kit puts a `constitution.md` at the root: the project's non-negotiable principles that *every* later phase references. That is structurally identical to your **gated canon** — the rules every variant must obey. Adopting the pattern gives you a clean place to declare the hard objective gates once, and have discovery/generation/checks all reference the same source. Low cost, good fit.

spec-kit's four phases (Specify → Plan → Tasks → Implement) are a coding workflow, so don't copy them literally — but the *shape* (each phase emits a markdown artifact that is the next phase's input) is exactly the harness contract you still need to define for the screen/journey/project tiers.

## LLM-as-judge — the research backs your pushback #2
The literature is consistent and unflattering for the aesthetic case: LLM judges are **confidently wrong**, **probabilistically unstable** (same input, different score), carry **position/verbosity bias**, and are **weakest in exactly the domains needing nuanced judgement** — visual quality among them. This is hard evidence for "automate around the taste call, never the taste call itself." Use LLM judging only to **filter** (kill objectively broken variants) and **annotate** (advisory signals), never to **rank/pick**. Picking stays human + user testing.

## Prior-art reality check (editor decision)
The text→UI generation space is now commodity: **v0** (React/shadcn code), **Google Stitch** (ex-Galileo — free, multi-framework export), **Figma Make** (design-system-aware, in-canvas edits), **Lovable** (MVPs). They all do generation + editing well and cheaply. Building a bespoke editor or generator would be spending your scarcest effort on the *least* differentiated part of the stack. Confirms the brief: editor last, and likely a wrapped existing canvas. Your moat is the gated discovery→criteria→enforcement loop that sits *upstream* of where these tools begin.

## Artifact/handoff notes (seed for the deferred harness task)
The harness contract needs, per tier, {input → definition-of-done → output}. From the above, the framework layer pins down the upper tiers' *inputs*:
- **Project tier** in: brief + ingested research → out: constitution + ranked risky assumptions.
- **Journey tier** in: assumptions + JTBD → out: `spec.md` with success/failure criteria (the evals).
- **Screen tier** in: spec criteria → out: N gated variants (objective gates pass) + advisory annotations.
- **Component tier**: already defined (gated snippet + 6 gates) — unchanged.
- The **token tier** sits below component, already covered by the token work.

This is the bridge: discovery doesn't just "inform" the build, it *emits the criteria artifact* that becomes the screen/journey definition-of-done. That's what makes the harness tiers composable rather than vague.

## Deferred (parked per Dave)
- **(a) Minimum-viable-target spec** — blocked on picking the one real HSBC proof project.
- **(c) Harness tier-contract** — blocked on this doc; seeded by the artifact/handoff notes above.

---
*Sources: GitHub spec-kit (github.github.com/spec-kit), GitHub blog on spec-driven development, OpenAI/Anthropic/Hamel Husain on eval-driven dev, Braintrust & arXiv judge-reliability work on LLM-as-judge, 2026 AI-design-tool comparisons (v0 / Google Stitch / Figma Make / Lovable).*
