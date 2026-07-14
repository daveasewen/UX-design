# §9 session findings — "rules or architecture?" (2026-07-07)

*Dedicated session on the §9-spread verdict ("confused, not converged"). Every finding recorded
below with evidence + source. Companion artifacts: `_KNOWLEDGE-USAGE-TRACE.html` (interactive
dossier), `_trace_knowledge_usage.py` + `_build_trace_dossier.py` (the tools),
`_KNOWLEDGE-USAGE-ENTITIES.json` (data). Memory: [[register-inference-ramp]],
[[knowledge-usage-trace-tool]], [[library-composition-tier-gap]], [[ds-knowledge-graph-revisit]].*

## Executive summary

1. The governed engine is **provenance-perfect yet flat**; the unconstrained diagnostic is
   **invention-heavy yet better-composed**. So the ceiling is **not** rule-*adherence*.
2. **Layout is the crux, and the KB does not govern it** — there is no page-template tier; the
   charter says composition is "always inferred."
3. **Root cause named:** the invention rule is "retrieve/derive from what exists," but the library
   **stops at organism** — 38 components, zero templates/shells. So page composition has nothing to
   retrieve. Thin library at the composition tier ⇒ underwhelming layouts, by rule.
4. Three live hypotheses now on record (rule-crafting quality · architecture ceiling · **rules/
   library too thin at source**), converging on the library-tier gap as the shared cause.
5. Open decision: **build the ~200–300 catalog upfront** (`_COMPONENT-LIBRARY-TARGET.md`) vs
   **compound Layer 2 via cluster-promotion** (ADR-0006). Not resolved.

---

## F1 · Knowledge-graph scope: only the canon core is graphed

The live graph (`_build_xref_index.py`, joining `components/` metas + `tokens/_blast-radius.json` +
`compliance/graph-index.json`) covers **component / token / compliance** only. Guidelines are
attached via a **hand-typed `GLOBAL`+`TOPICAL` map inside the script** — pointed-*at*, not
graphed-*through*. Snippets, assets, the register, `_sources/`, TOV/copy corpus and ADRs are **not
nodes**. Confirms the still-open whole-corpus-KG diagnosis.
*Source: `knowledge/_build_xref_index.py`, `knowledge/_GRAPH-REPORT.md`. → [[ds-knowledge-graph-revisit]].*

## F2 · The knowledge-usage trace tool (built + to reuse)

Built two scripts that reconstruct **retrieved-vs-invented** from any generated artifact (no
self-report needed — sidesteps the unreliable-manifest problem seen 07-05):
- `_trace_knowledge_usage.py` — measurement; posture per screen (PURE-RETRIEVAL / HYBRID /
  INVENTED); reuses `_validate_icons.py` byte-match + resolves `var(--x)` against canon.
- `_build_trace_dossier.py` — Swiss interactive dossier: canvas force-directed **knowledge-graph
  intro** (Structure / Blast-radius / Retrieval-overlay), provenance bar-charts, layout section,
  **entity explorer** (filter, target+note, export worklist, localStorage), **rule-adherence
  layer**, and an **accordion** that reads full guideline + WCAG text in-tool.

Dave: "this is a great tool, note that we should reuse." *→ [[knowledge-usage-trace-tool]].*

## F3 · Provenance result — the ceiling is NOT rule-adherence

Traced all 3 lineages (11 files):

| Lineage | Posture | Live hex (invented colour) | canon components | Invented local vars |
|---|---|--:|--:|--:|
| governed-Sonnet | PURE-RETRIEVAL ×3, HYBRID ×1 | 0 | 19 | 2 |
| governed-Opus | PURE-RETRIEVAL ×4 | 0 | 26 | 0 |
| diagnostic (unconstrained) | INVENTED ×2, HYBRID ×1 | 56 | 1 | 219 |

Governed lineages are provenance-perfect (0 invented colours, ~200 canon token refs) yet are the
screens Dave judged flat. The rules are already **saturated** at the governed end — so tightening
their application cannot be the lever. 35% of all entities invented, all in the diagnostic lineage.
*Source: `_KNOWLEDGE-USAGE-TRACE.md`, `_KNOWLEDGE-USAGE-ENTITIES.json`.*

## F4 · Layout is the crux — and the KB does not govern it

The KB governs the **measure**: 12-column grid, ~1280px max width, gutters, breakpoints, spacing
tokens (`web-foundations.md` §Responsive grid, `tokens/layout.json`, `--layout-web-columns`,
`--breakpoint-*`, `--gap-*`). But it governs **no page template**: charter line 34 —
*"Composition — layout, grid, page templates (the canon has no template layer — this is always
inferred)."* Confirmed: **zero** `.cn-page/.cn-grid/.cn-layout` class. Even layout-*spacing* tokens
are ~0-retrieved — governed screens hand-author spacing in raw px (canon-space refs ≈ 0 across the
spread). So the flatness cannot come from retrieving a bad layout; **no layout is retrieved.**
*Source: `_FIXED-FLEX-CHARTER.md` §3/§9, `knowledge/guidelines/web-foundations.md`, `_KNOWLEDGE-USAGE-ENTITIES.json` layout blocks.*

## F5 · Rule-adherence layer — freer layout and rule-honouring pull OPPOSITE

Added WCAG + create.hsbc-principle probes to the trace (honoured / violated / not-detected).
Governed screens honour 5–7 rules with 0–2 violations. The diagnostic — the one with the **better
layout** — honours **1 and violates 6** (no focus styles, no aria/role, no reduced-motion,
non-square corners, canon not linked). So on these screens, **better layout arrived bundled with
wholesale rule-breaking.** That decouples "feels better" from "adherence," and is direct evidence
for the rules-design tension below.
*Source: `_build_trace_dossier.py` rule_probes(), `_KNOWLEDGE-USAGE-ENTITIES.json` summaries.*

## F6 · Root cause — the invention rule meets a library that stops at organism

**The rule (verbatim).** Charter §6 "generate-new mechanism": *"Retrieval-first — query the graph
for a component/token that fits before generating"* + *"Derive from fixed — a new value must be
derived from a brand primitive… not invented free-hand."* §9 sober band: *"retrieve and assemble
what exists; invent only if forced, then derive-from-canon."* Invention at the strict end is
therefore bounded to inferring/deriving from **existing** components + rules.

**The library.** The 38 components are **9 atoms · 23 molecules · 6 organisms — zero templates,
shells, or page-scaffolds** (largest unit = organism). So when composing a *page* at sober/balanced,
retrieval-first returns only parts; the composition tier has nothing to retrieve, so layout is
always inferred from thin ingredients. **Underwhelming layouts are structurally forced** there — a
library-completeness problem, not a tuning one. (Dave's recollection, verified correct.)

**Already costed.** `_COMPONENT-LIBRARY-TARGET.md`: base ~38 → ~75–85, plus Layer 2 of ~40–50
shells/templates/lock-ups → a *"200–300+ item catalog."* Its closing line is the same point:
*"the automation can only compose what exists, so the inventory is the prerequisite for the
machine."* Matches Dave's "~300 including templates and shells."
*Source: `_FIXED-FLEX-CHARTER.md` §6/§9, `_XREF-INDEX.json` (category counts), `_COMPONENT-LIBRARY-TARGET.md`. → [[library-composition-tier-gap]].*

## F7 · Open decision — build-upfront vs compound

`_COMPONENT-LIBRARY-TARGET.md` frames the ~300 catalog as a **program / prerequisite** (build it).
ADR-0006 point 4 pushes the other way — *"compounding canon, not completeness… chasing a complete
library is the alphabetical treadmill"* — answering with the **cluster promote-loop** (each novel
lock-up becomes gated canon the moment invented once). They agree the template/shell **tier must
exist** and currently doesn't; they differ on *how to fill it*. ADR-0006 also notes cluster-level
promotion is the **least-proven** part of the loop (tokens + motion promoted; never a whole
lock-up). **Unresolved — this is the real decision the session surfaced.**
*Source: `docs/decisions/ADR-0006-flexing-engine-product-shape.md` (pt 4), `_COMPONENT-LIBRARY-TARGET.md`.*

---

## Three hypotheses, reconciled

- **H1 — rule-crafting quality** (Dave's live guess, "just crafting the rules"): *weakened.*
  Governed lineages are already provenance-perfect; the rules aren't leaking.
- **H2 — architecture ceiling** (single governed pass vs generate-then-normalise two-pass):
  *still live.* The output Dave liked was HYBRID/derive-and-flag = the two-pass fingerprint
  ([[generation-mechanism-ideas]] Idea 2). No controlled 1-pass vs 2-pass run on one screen yet.
- **H3 — rules/library too thin at source** (Dave, this session): *strengthened, and refined.*
  Not that the rules are wrong, but that *"retrieve what exists"* is correct while **what exists
  stops at organism.** The layout gap (F4) and the library-tier gap (F6) are the same gap from two
  angles; it's also why the unconstrained diagnostic won on layout — it freely invented the missing
  tier.

## Next probes (named, not started)

- **Retrievable composition layer** — page archetypes / shells as graph nodes: the missing
  governance F4/F6 expose.
- **Composition-tier probe** in the trace tool — measure per screen whether any retrieved unit is
  above organism level (currently indistinguishable).
- **Controlled 1-pass vs 2-pass** run on one screen — the comparison nobody has run.
- **Resolve F7** — build-upfront vs cluster-compound — as a product-shape decision.
