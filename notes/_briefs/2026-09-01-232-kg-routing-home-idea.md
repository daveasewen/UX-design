# Banked — Dave's #232 idea: routing logic belongs in the KG, not the skill

provenance: 232 · 2026-09-01 · banked in chat mid-morning, demo day · row W-333 (minted AT CREATION)
status: FLOATED, Dave's — nothing ruled. Reflected back in chat #232; his confirm pending.

## Dave's words, verbatim

> "I want to note something before I forget, would it be better if this sort of mechanism
> for dashboards etc was part of the KG whether explicitly like the skill or implicitly,
> surely the KG is the brain and some of this could be offloaded from the skill to the, I
> would think that this is the natural home for this logic."

Context: said immediately after #232 found `generate-from-canon/SKILL.md` carries zero
routing (no mention of bento/template/dashboard) — the mechanical cause of the cold build
not going bento-first.

## Reading (conductor's, declared — not his ruling)

The proposal: template/dashboard ROUTING (brief-shape → template family, bento-first,
splice-never-redraw) should be homed in the knowledge dir — the pack's brain — rather than
in skill prose. Either explicitly (a machine-readable routing manifest the skill reads
generically) or implicitly (derived from the snippet corpus itself).

This rhymes with two standing idioms: `s200-D1` mint-time derivation (content minted into
artefacts, never live-derived by prose), and the #231 detector's own design (no baked
family list — everything derived from `knowledge/snippets/*` at run time, so it cannot rot
when a snippet lands). A routing manifest derived or gated against the snippet corpus
closes the class that caused today's finding: a template landed and no prose knew.

## Consequences to price before any build (replayed, per the rule)

- The KG piece must SHIP — a routing row that stays repo-side reproduces the gap.
- It needs a gate: every `Template-*` snippet family must carry a routing row, or the
  forgotten-document class recurs inside the pack.
- Skill-vs-KG split is a RELEASE-SURFACE decision (packs are releases, machine-enforced)
  — v1.0.6-shaped, not today's repair.
- Feeds W-329 (Factory north-star): where routing lives is part of where the paraphrase
  seam sits.

## Pairing (tactical vs permanent)

Tactical (today, #232 repair lane): an explicit routing step in SKILL.md so the demo pack
routes dashboards bento-first. Permanent (owner: Dave rules the shape; conductor briefs
the build): the KG-homed routing this note banks. The tactical step is written knowing it
will be superseded — it is the patch half of an RCA'd pair, and it is DECLARED as such.
