# Idea, not a lane — Jev as the build-time selector OVER the knowledge graph

provenance: 293, Jev side-quest worker seat (Fable 5.1) · 2026-09-21 · **NOT ENACTED, NOT SCHEDULED**

⛔ Dave's standing word for everything Jev: *"any analysis is fine but any changes with impact will
need to be made after the presentations and demos"* (Friday 25 Sep). This file is a note so the idea
survives the wrap. Nothing below is cut as a lane until he says so, after the 25th.

## His question, verbatim

> could i use jev at build time instead of the KG?

## The answer given in chat

**No as a replacement; yes as the thing that reads it.**

- Jev has no memory — each call sees only the state handed to it, accuracy falls as state grows
  (jaggedness mode 5, "large state full of irrelevant detail"), context is bounded at 64k
  (`docs.typesafe.ai/models`). Without the graph there is no closed option set to choose from,
  and Jev can only pick from options it is given.
- The graph is the record: every edge carries evidence and Dave's ratification, and can be
  explained. A Jev answer is a probability with no reason attached.
- A build step that needs an API key is the dependency he already ruled out
  (`areas/jev-integration`: dev-time instrument, never a dependency). The KG is also the demo's
  show-stopper on the 25th.

**What CAN be done at build time:** Jev as the selector over the graph. A brief comes in; code pulls
the candidate nodes (rules, tokens, roles, principles — the graph's neighbourhood for the brief); one
Choice asks which applies; confidence decides automatic vs "to Dave". This is the docs' intent-routing
pattern (`patterns/intent-routing`) and skill-suggestion cookbook (`cookbooks/skill_suggestion`):
one request ranks every candidate and asks whether any applies at all; a second reads the top three
properly and can reject all of them. It replaces lexical lookup and rule-of-thumb, not the graph.
The graph becomes what Jev reads; Jev becomes how the build reads it fast.

## His second question, verbatim

> so we currently pull a slice of the KG for a build, its wasteful otherwise I guess, could jev call
> the entire KG and maybe make decisions from broader context?

## The answer — two hops, with the token counts MEASURED at this seat (2026-09-21, cl100k)

**The whole graph does not fit; its skeleton does.**

| what | measured | against |
|---|---|---|
| 335 component `*.meta.json` bodies (excl. `_to_delete`) | **962,656 tokens**, mean 2,873 per meta | Jev context **64k** (declared, `docs.typesafe.ai/models`) — ~15× over |
| the same 335 as one line each — `id \| kind \| title[:60]` | **2,871 tokens** | fits with ~60k to spare |
| edges as triples (est. 3,605 edges × ~5 tokens) | ≈ 18k (ESTIMATE, not measured) | skeleton + edges still < 25k |
| `knowledge/_decision-graph.json` (102 nodes / 172 edges) | 11,844 tokens | fits whole |

So "call the entire KG" literally = fifteen requests of the wrong shape (jaggedness mode 5: accuracy
falls with irrelevant state). "Call the entire skeleton" = one request carrying the full topology,
which is broader context than any build slice today.

**Hop 1 — broad.** Skeleton in (every node id/kind/title + edge triples). One Choice over candidate
ids (cap **255 options per Choice** — partition by kind or layer as the graph grows) + one Noul "does
any node here apply to this brief". Jev picks the neighbourhood by judgment over the whole graph
instead of by lexical proximity. That is `cookbooks/semantic_find` (one Choice over ≤255 line ids).
**Hop 2 — deep.** Only the chosen nodes' full metas go in (a dozen ≈ 35k tokens); Jev makes the
actual decisions with full text. That is the cascade shape (`cookbooks/sde_cascade`). The waste he
named — pulling a slice blind — is what hop 1 removes.

Limits, flat: 255-option cap; Jev is literal so node titles must say what nodes ARE (mode 1); still a
selector — the graph stays the record and the build must run identically without a key.

## If it is ever cut as a lane (after the 25th, only if ruled)

1. Pick ONE real brief the build already handles (the demo's cold brief once it is named to the
   record — HANDOFF-143 owed item 4).
2. Measure what the current build selects for it (the baseline, from the build's own receipts).
3. Hop 1: skeleton in (all nodes one line each + edge triples, measured ≈ 3k + ~18k tokens); one
   Choice over ids (≤255, partition by kind) + one Noul "does any apply". Output = the neighbourhood
   with a probability per node. Compare it to the slice the build pulls today — that comparison is
   the finding.
4. Hop 2: the chosen nodes' full metas as state (never a description of them — J3 lesson); the
   build's actual decisions as Choices; confidence-gated ≥0.8 automatic, else to Dave.
5. Compare selections; publish agreement, disagreements, latency and `usage.input_tokens`.
   Both readings stand; nothing inscribed; the build is not changed.
6. Fallback is mandatory: no key ⇒ the build selects exactly as it does today.

## His third question, verbatim — order

> okay last question about order, so we can use jev to improve the the KG and then we might have it
> help with the decision making at run time of are these mutaually exclusive

## The answer — not exclusive; sequential, and the order matters

1. **Build time first — Jev improves the graph** (J5 proposals C then B: audit the 78 derived
   ruling→ruling edges, then propose edges for the zero families). Output is a ratification page;
   Dave rules; ratified edges are just edges. Offline, once, **no dependency left behind** —
   anyone without a key gets the improved graph.
2. **Run time second — Jev selects over the graph** (this file's two-hop shape). Hop 1 reads the
   skeleton, so selection quality is capped by graph completeness: run it before the families are
   filled and you measure Jev against a graph missing half its nodes and blame the model.
3. **The loop.** Every run-time selection Dave corrects ("Jev picked X, I wanted Y") is a candidate
   edge or a missing node — build-time signal. Run-time receipts feed the next build-time pass.

The split that keeps his standing rule safe: **build time MAY depend on Jev** (output is ratified,
static); **run time MAY NOT** (the build must select identically without a key). The part that needs
Jev is the part nobody else runs.

**Proposed order after the 25th, only if ruled: C (78 calls, cheapest proof) → B → J7.**

## Where the rest of the record is

`notes/_lanes/293/J/` research brief · `J3/` falsification probe · `J4/` re-rank (flat; recall is the
defect) · `J5/jev-recall-proposal.html` (A Memento door, B KG edges, C ruling-edge audit) ·
`J6/typesafe-field-guide.html` (59 docs pages → Apollo map; corrects the 70–500 ms "declared band"
— it is press, not docs — and disputes J2's "jev-1.13.0 not requestable"; both stand until measured).
Adapter `knowledge/_jev.py`; receipts `knowledge/_jev-receipts.jsonl` (19 live calls to date).
