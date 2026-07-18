---
name: presentation-delivery-2026-07-13
description: "Operative near-term plan (2026-07-13): two presentation horizons + the Copilot-skills DELIVERY decision + what's BUILT (designer-skills-v1 pack) + the review-tooling backlog to finesse before 20 Jul"
type: project
---
**TWO HORIZONS (Dave, 2026-07-13):**
1. **Designers** — a **Copilot skill pack** to experiment with. Intro ~**20–21 Jul**, hands-on release
   ~**24 Jul**. Heavily caveated. (Today = 13th; weekend 18–19 to build.) HARD deadline.
2. **Sponsor** — an exec/sponsor meeting to **introduce the idea** (narrative + demo), and set the
   follow-up date *in* that meeting. Narrative-led; deeper demo at the follow-up. Date TBD.

**DELIVERY DECISION — runs in the designers' existing VS Code + GitHub Copilot as Agent Skills**
(`SKILL.md` in `.claude/skills/`), NOT a bespoke tool. This IS the ADR-0002/0005 architecture
(portable skills+data operated by any host agent). Research confirmed (2026-07-13): Copilot's "Agent
Skills" are GA and it reads `.claude/skills/` natively (Claude-Skills-compatible) — so our skills are
largely drop-in. **Python gates can't run per-designer** (need Python installed + approval per run) →
v1 leads with generation/retrieval skills; the authoritative gates stay in **CI**; a shared **MCP
server** for gates = v2. (Simple explainer for others: skills = text anyone's Copilot reads instantly;
gates = programs needing Python installed, so they stay in the shared build for now.)

**BUILT 2026-07-13 → `designer-skills-v1/` in the repo (committed):**
- **4 skills** (reframed from the old harness skills into designer-facing Copilot skills, jargon
  stripped): `generate-from-canon` (strict build), `check-against-design-system` (drift check, in-editor
  guidance; authoritative gates = CI), `usability-review` (Nielsen), `draft-a-new-pattern` (NEW =
  the creative / co-creation mode; output = a candidate for human review, not auto-canon).
- **README** + **`build-designer-kb.sh`** — curates the lean designer KB from live `knowledge/`:
  **838 files / 4.6MB** (38 metas + schema, token stores, `canon.css`, 38 snippets, WCAG map, 658-icon
  library, **49 guidelines**; excludes the Python machinery, audit/working docs, 10 process/governance
  guideline docs). Run it from repo root to materialise `designer-skills-v1/knowledge/`. Full pack
  preview delivered as a zip.
- **Guidelines insight (important):** under-used in STRICT mode (trace showed the §9 tests hit only
  2 docs — brand-principles, colour-usage) but they are the **FUEL for the CREATIVE mode**
  (`draft-a-new-pattern`) — you can't invent an on-brand new component from existing components.
  **Test (rides on the release):** run `draft-a-new-pattern` with vs without the guidelines, trace it,
  see if consumed + if the pattern is better. Open test thread, not a ruling.

**REMAINING for the 24th:** confirm the exact skills folder path from one of the team's existing
skills (Teams message sent asking); a quick sanity-check that a skill actually fires. Then it's their
repo's `.claude/skills/` + `knowledge/` + `AGENTS.md`.

**NEXT (queued):** the **sponsor narrative** (reuses the review, the vision, the trace, and now a real
working pack to point at).

**BACKLOG — review-tooling additions (Dave, 2026-07-13, "time to finesse before the 20th"):**
1. **Package the `swiss-design-system` skill** into the pack (styling for dossiers/outputs; repo already
   has `Swiss-design.md`).
2. **Review-dossier skill/template** (reusable, as used before — cf. `_REVIEW-DOSSIER-*`,
   `_build_trace_dossier.py`, memory [[process-doc-language-review]]): Swiss-styled · **tooltips on
   every acronym/jargon term** · **two modes: 'standard' (simplified) + 'technical' (default)**.
   *Standard* = for a **non-technical human consumer/reviewer, NOT a builder** ("AI consumer" = consumer
   of the AI system) · **reading age 11–12** · simple-but-complete · carefully guided through the
   dossier · least-friction sharing. (⚠️ confirm this audience read with Dave before building — per
   [[feedback-clarify-reflect-back]].)
3. **Component-review skill/template** (as used before — cf. `gen_gallery.py`, [[review-preview-html]],
   [[component-review-program]]): produce + review components in **light AND dark mode, carefully
   labelled**, optional **diff mode** for iterative before/after changes.
   Build order rec: swiss (quick) → dossier skill → component-review skill; one at a time.

**Working reminder:** reflect interpretation back before recording as a ruling ([[feedback-clarify-reflect-back]]);
Dave's register = understatement. Long session 2026-07-13 — captured here as the resumable handoff.
