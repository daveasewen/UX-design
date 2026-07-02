# Generative AI and our brand — governance (ingested)

*Source: create.hsbc → Processes and tools → `generative-ai-and-our-brand.html`, captured
2026-07-02 via Dave's authenticated session (login-walled; ADR-0005 provenance applies).
Engine-era format. This is GOVERNANCE, not visual rules — ingested out-of-tier because it
defines the regime any generative design tool (i.e. Promenaut) operates inside. Group AI
policies / Responsible AI / AI-lifecycle pages are staff-only Confluence — not reachable
from create.hsbc, noted as source boundary.*

## Scope

Applies to **any generative-AI use producing outputs related to brand foundations** — the
page enumerates: logo, photography, video, motion, Creative Hexagons, sonic branding,
**data visualisation**, illustration, typography (non-exhaustive). Outputs must align with
brand identity foundations. **Our engine's entire output class is in scope.**

## The seven principles (rules)

- **Approved tools only** — generative AI tools must pass the HSBC AI lifecycle review;
  third parties and agencies included (Supplier Code of Conduct). [process — for Promenaut
  this is an ADOPTION GATE: the tool itself needs lifecycle approval at a client]
  {#gai-001}
- **Brand protection, two checkpoints** — brand review ticket BEFORE the creative process
  starts (when brand foundations are in the output), then **Global Living Wall review and
  approval before publication**. [process] {#gai-002}
- **Quality assurance** — "outputs must meet HSBC's high visual standards — avoid using any
  content that appears synthetic or does not reflect our premium brand values". [TASTE at
  source, but this is precisely what the gate stack mechanises — see Findings] {#gai-003}
- **Contextual appropriateness** — real imagery for real-world topics (news, locations);
  gen-AI permitted for visionary concepts ("Smart Cities 2050") and for localising
  backgrounds/clothing in real photographs; **never to add or alter people**.
  [ADVISORY] {#gai-004}
- **No AI-generated people in marketing/storytelling**; no cloning of real HSBC personnel;
  critical exceptions escalate to the Living Wall. [ADVISORY] {#gai-005}
- **Motion avatars** — internal, functional content only (e.g. training), clearly marked
  AI-generated; never marketing, never replicating real personnel. [ADVISORY] {#gai-006}
- **Ethical standards** — data privacy, bias, accountability for outcomes (Responsible AI
  page, staff-only). Plus, from the permitted/prohibited table: **never edit, add or remove
  religious or political items.** [ADVISORY] {#gai-007}

## Permitted vs prohibited (source table)

Permitted: visionary concepts · localising backgrounds/clothing in real photos · internal
motion avatars (marked) · real photography for real-world topics · creative concept
development and inspiration (e.g. scamping initial ideas from briefs).
Prohibited: AI people in marketing · adding/altering people · cloning personnel ·
low-quality or synthetic-looking output · editing religious or political items.

## Process (3 steps)

1. Confirm tool approval (AI lifecycle; register use case if not) → brand-review case if
   in scope. 2. Define the purpose against brand standards. 3. Submit all creative work to
   the Global Living Wall before release.

## Findings — Promenaut positioning (the reason this page jumped the queue)

1. **The tool is in-scope, twice.** Promenaut is (a) itself a generative-AI tool needing
   lifecycle approval at any HSBC-like client, and (b) a producer of brand-foundation
   outputs (data-vis, typography, colour) whose outputs sit under Living Wall governance.
   Adoption planning must include both. [REVIEW — strategy input, Dave] {#gai-008}
2. **The gates are the answer to principle 3.** "Avoid synthetic-looking output; meet high
   visual standards" is stated as un-mechanised taste. The engine's pitch in one line:
   blocking gates + advisory signals + human taste call = principle 3, made executable and
   auditable — with the criteria contract as the "define the purpose" artifact (step 2) and
   the promotion/taste-call loop as a scaled-down Living Wall. The governance page
   VALIDATES the engine's architecture. [strategy note — feed
   `digital-experience-transformation/`]
3. **Concept-development carve-out.** "Support creative concept development and
   inspiration (eg scamping initial ideas from briefs)" is explicitly permitted — the
   T3-exploration tier maps onto it cleanly (divergent work ungated, convergent output
   governed). Charter alignment, for free.

## Cross-references

`_FIXED-FLEX-CHARTER.md` (T1/T2/T3 ↔ permitted-uses mapping) ·
`_RUNBOOK-criteria-contract.md` (the "define the purpose" artifact) ·
`digital-experience-transformation/` (strategy strand — finding 2 belongs there) ·
`_INGESTION-QUEUE.md` (Group AI policy pages are staff-only Confluence: out of reach).
