# Operating model & role map — the Digital Experience team

*DRAFT v0.1 for review. How the team actually works, and how today's roles become tomorrow's.*

---

## Executive summary

The old operating model is an **artifact factory**: briefs in, hand-made screens and specs out, with designer-hours as the bottleneck and quality dependent on whoever did the work. The new model is a **governed experience system** in three layers — a **Machine** that does the production labour, a **Standards** layer of encoded human judgment that the machine enforces, and a **Human** layer that spends its scarce hours on experience, research and the judgment calls the machine hands up. The headline role change is from **producing artifacts** to **governing the system that produces them**, plus a decisive shift of human time toward research, criteria and curation. The team gets **smaller, more senior, and gains an engineering spine** it never had.

## The two operating models, side by side

**Old — artifact factory**
> Brief → designer manually produces screens/specs → slow, subjective manual review → handoff document → engineering rebuilds it → drift between design and build.
> *Bottleneck:* designer hours. *Value metric:* artifacts shipped. *Quality:* inconsistent, person-dependent. *Compliance:* checked by hand, late, partially.

**New — governed experience system**
> Brief → researched, **criteria-bound spec** (success written as executable checks) → **generation from gated canon** → **objective gates** auto-reject anything non-compliant → human makes the rare **taste call** on the survivors → composed prototype → handoff with no drift (the build uses the same certified parts).
> *Bottleneck:* judgment and criteria, not hands. *Value metric:* compliant outcomes and time-to-trustworthy-prototype. *Quality:* certified and consistent by construction. *Compliance:* enforced continuously, auditably.

## The three layers

1. **The Machine (automated execution).** Generation from the gated canon, the objective gates (accessibility, contrast, token-fidelity, state-completeness, and more), and composition of certified parts into screens and journeys. This layer absorbs the production labour that used to be the team's whole job.
2. **The Standards (encoded judgment).** The **canon** (certified, compliant components), the **criteria/specs** (what "good" means, as checks), and the **gates** (what blocks vs what merely advises). Built and maintained by humans; enforced by the Machine. This is where the team's expertise now *lives* — durably, not in one-off files.
3. **The Humans (scarce judgment + experience).** Experience strategy, research and discovery, curation of the canon, authoring of criteria, governance of the gates, and the small set of genuine taste calls. This is where the team's hours go.

The art of running the team is keeping the **tiering** honest: a few hard objective gates that block, many cheap advisory signals that annotate, and a *small* number of true human taste calls — so the system never degrades back into the slow, subjective review it replaced.

## Role map: from → to

| Today (Design Delivery) | Tomorrow (Digital Experience) | What changes |
|---|---|---|
| **Production / UI designer** — makes screens and specs to order | **Experience designer & criteria author** — defines intent and success criteria, curates canon, makes the taste calls | Stops drawing every screen; starts defining *what good is* and judging the machine's output. Fewer needed, more senior. |
| **Design-system / component designer** — maintains a library humans copy from | **Canon steward** — owns the *certified* component set; spends judgment once, enforced forever | Library becomes a governed, gated canon. Very high leverage: one good decision propagates everywhere and can't drift. |
| *(did not exist)* | **Design-system / experience engineer** *(new, pivotal)* — builds and maintains the harness, the gates, the code-binding, the generation pipeline | The new spine of the team. Industry-wide, "engineering participation in design systems keeps growing." This is the design↔code bridge. |
| **Researcher** — often first to be cut | **Experience researcher** — elevated to the front of the value chain | When building is cheap, knowing *what* to build and whether it worked is the scarce input. Research moves from optional to essential. |
| **UX writer / content designer** — writes copy per screen | **Content & tone governor** — encodes tone-of-voice as an enforceable check | Content quality becomes governed and consistent, not hand-written every time. |
| *(scattered / informal)* | **DesignOps / governance lead** *(new or elevated)* — owns the gate model, compliance bar (WCAG 2.2), tiering, auditability | In a regulated org this is a senior, central role: compliance-as-enforcement. |
| **BA / PO** — write requirements | **Input providers & gate participants** — acceptance criteria become executable checks | Already modelled this way in the Apollo. Their criteria feed the gates directly. |
| **Design manager** — manages artifact throughput | **Experience lead / orchestrator** — manages outcomes and the system | Manages the machine and the experience, not the volume of hand-made deliverables. |

## What the team STOPS doing
- Manual screen production at volume.
- Hand-built redlines, specs and handoff documents.
- Manual, late accessibility and consistency checking.
- Per-screen policing of brand and pattern compliance.
- Re-solving the same patterns over and over.

## What the team STARTS doing
- Authoring **criteria** (success as executable checks) up front.
- Curating and certifying the **canon**.
- Governing the **gates** and the compliance bar.
- Running **discovery and research** as the front of the value chain.
- Making the rare, high-value **taste calls**.
- Building and maintaining the **harness** (the engineering spine).
- Owning **experience outcomes and journeys**, end to end.

## Team shape
Smaller, more senior, T-shaped, with a genuine **engineering spine** it did not have before. The industry pattern is explicit: *fewer people + higher seniority + AI augmentation = the same or better output*, with design teams shrinking even as product complexity grows. The Digital Experience team is the deliberate, value-creating version of that pattern — not "the design team, but cheaper," but "the team that owns experience and the infrastructure that guarantees it."

## New metrics (replace "artifacts shipped")
- **Time-to-trustworthy-prototype** (brief → gate-passing, testable prototype).
- **Governed-quality rate** (share of shipped UI that is certified/compliant by construction).
- **Compliance findings caught pre-ship** vs escaped to production.
- **Reuse rate** of canon vs net-new hand-built work.
- **Experience outcomes** (research-validated; did it work for users), not output counts.
