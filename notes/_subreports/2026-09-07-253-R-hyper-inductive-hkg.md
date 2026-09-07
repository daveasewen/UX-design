# `#253`-`R-hyper` — HYPER (foundation model for inductive link prediction on knowledge hypergraphs, ICLR 2026): Desirability · Feasibility · Viability for Apollo

session: `#253` research lane (filed 2026-09-07, ahead of the #253 opener) · 2026-09-07
window: research worker (Fable 5.1), second paper in the same side lane as `2026-09-07-253-R-krepe-hkg-diffusion.md`; touches NO meta, schema, validator or `reviews/META-TAGS-*` (lanes A/B/C own those — `_HANDOFF-252-lanes-cold.md`)
sub index: `R-hyper`
brief: chat-only — "what about this? leave receipts — HYPER: A Foundation Model for Inductive Link Prediction with Knowledge Hypergraphs"
tokens: `UNMEASURED — harness counter ≈14,999,000 → ≈14,990,000 ≈ 9K QUOTA over 4 tool calls; arXiv PDF (34 pp) text-extracted at this seat, repo README + LICENSE fetched raw`

## VERDICT

**HYPER is the paper that answers the KREPE report's U1, and the answer is: feasible as a one-afternoon probe, desirable only as a baseline, never as an author.** HYPER (Huang, Bronstein et al., Oxford; ICLR 2026; arXiv 2506.12362) is a *pre-trained* graph foundation model: one 2 MB checkpoint, MIT-licensed, that scores links **zero-shot on any knowledge hypergraph — unseen entities AND unseen relations** — because entity and relation embeddings are computed on the fly from structure (a relation graph of positional interactions + sinusoidal position encodings), never stored. That removes the two walls that killed KREPE for us: no training corpus is needed (Apollo's ≈1.5K facts become the *inference* graph) and the licence is clean. What it does NOT remove is the constitution: HYPER emits a ranking with a probability, and Apollo's gates consume addresses and rulings, not probabilities. Its zero-shot quality is modest — averaged MRR 0.285 / Hits@3 0.281 over 19 hypergraphs (Table 4), 0.13–0.46 per inductive dataset (Table 2) — and its facts are ordered n-ary tuples `r(u₁…u_k)`, not qualifier pairs, so `roles.json`'s `when` predicates (free text) have no seat in the model unless discretised. **The one use that fits Apollo is as the machine baseline for R1 (the masked-recovery calibration test proposed in the KREPE report): mask each `provides` fact, ask HYPER zero-shot to rank the 12 roles, and record the rank. If a lane with retrieval cannot beat a 2 MB structure-only checkpoint at recovering canon, the brief — not the model — is what is broken.** Ruling-shaped, not ruled.

COUNTS: findings 8 · ruling-shaped 2 · UNPROVEN 3

## What was done

1. arXiv PDF 2506.12362 (34 pp, "Published as a conference paper at ICLR 2026") pulled and text-extracted; read for abstract, §4 method, §5.1 setup, Tables 2/4/13, §6 conclusion + limitation, compute appendix.
2. `github.com/HxyScotthuang/HYPER` README and LICENSE fetched raw: MIT; PyTorch 2.1+ / PyG 2.4+ / optional Triton; checkpoints in `ckpts/` at 2 MB each; "no awkward binary reification"; multi-GPU optional.
3. No code run. No Apollo file written outside this report.

## Findings

**F1 — the claim.** "The first foundation model for inductive link prediction over knowledge hypergraphs with arbitrary arity, capable of generalizing to both unseen entities and unseen relations" (§6). Query shape: `q = (r, ũ, t)` — a relation, a tuple with one position blanked, the position index t. Evaluated on 16 newly built inductive datasets + 3 existing.

**F2 — the mechanism, in one paragraph.** (a) Build a *relation graph* G_rel whose nodes are relations and whose edges record observed positional interactions — "relation r₁ at position a shares an entity with relation r₂ at position b". (b) Encode each interacting position pair (a, b) with Enc_PI (sinusoidal wins: 0.285 vs 0.236 all-one, 0.213 random — Table 4). (c) Conditional message passing over G_rel yields relation embeddings; (d) message passing over the original hypergraph, conditioned on the query, yields entity scores. Nothing is looked up; everything is derived from the graph presented at inference. That is why unseen vocabularies work.

**F3 — numbers that bound the usefulness.** Table 2 (node-and-relation inductive, MRR): HYPER(3KG+2HG) zero-shot 0.132–0.455 across 16 splits; fine-tuned 0.158–0.456; end-to-end trained per-dataset 0.135–0.468. Supervised hypergraph baselines G-MPNN / HCNet collapse to 0.000–0.104 when relations are unseen. ULTRA (the binary-KG foundation model) on reified hypergraphs trails HYPER on 13/16 zero-shot columns. Averaged zero-shot over 19 hypergraphs: MRR 0.285, Hits@3 0.281.

**F4 — cost.** Pre-training: 4 days on one H100 80 GB — *already done; the checkpoint ships*. Fine-tuning / end-to-end: "typically less than 3 hours". Inference on a ≈1.5K-edge graph is seconds on CPU (UNPROVEN, inferred from the O(|V|) rspmm kernel and the 2 MB model). Stated limitation (§6): positional interactions grow quadratically with arity — irrelevant at Apollo's arity ≤4.

**F5 — Desirability: as a baseline, yes; as an author, no.** The 25-meta pass authors `provides · answers · shape · span · priority · when` by lane, Dave vetoes (s251-D15). HYPER can rank candidates for ONE blank in ONE structured fact — `provides(component, ?)` or `provides(?, role)` — with MRR ≈0.3 on graphs it has never seen. That is exactly the shape of a *sanity baseline* for the R1 calibration test in `R-krepe` F10 and nothing more: it cannot write `when`, cannot propose a thirteenth role (the fence is Dave's, s252-D1), and a 0.3-MRR ranking is not a source anyone should author from. Desirability grade: **real as instrumentation; nil as generation**.

**F6 — Feasibility: yes, small.** Zero-shot needs only a conversion script: `roles.json` providers → `provides(component, role)`; meta `edges` → `livesInside(component, context)`, `mustNotNeighbour(c₁, c₂)`, `commonPattern(component, pattern)`, `renderedBy(component, snippet)`; decision-graph edges → their nine ADR-0012 types. Ordered n-ary tuples, arity 2–3. `priority` can ride as a bucketed third position (`provides(component, role, band)`); `when` cannot (free text, no entity identity) — it is dropped, which is fine for a baseline that measures structure only. MIT licence; PyG on CPU is installable in the sandbox; no GPU at this seat (UNPROVEN that Triton is optional at inference — the README says "optional", not verified). Feasibility grade: **one afternoon, one script, one run**.

**F7 — Viability: fine as an advisory instrument, and only if it has a consumer.** MIT is clean for HSBC-adjacent canon. The constitutional objection to KREPE (a generator the do-not-rule list cannot fence) applies here too *if* HYPER's output is ever written into a meta — so it must not be. The viable seat is `knowledge/_ADVISORY-SIGNALS.md`: a signal that says "this `provides` ranks 9th of 12 for its component under a structure-only prior — look again", consumed by a reviewer, never by a gate. Even that is an instrument without a consumer until someone names who reads it ([[instrument-without-a-consumer]]) — which is why the recommendation below is a one-off calibration run, not a standing signal. Viability grade: **viable once, as a measurement; not as a standing gate**.

**F8 — where it sits against the earlier graph-engineering research.** `_RESEARCH-graph-engineering-2026-08-05-v3.html` ruled "the graph is not on the retrieval path" and listed six cheap candidates, #1 being one-hop edge expansion. HYPER is orthogonal to all six: it is a scorer over the same edges, not a retrieval change. It neither competes with nor substitutes candidate #1; it could *measure* it — recovery rank with vs without the meta's neighbours in the inference graph is a direct read of how much one-hop context is worth on our corpus.

## Dave-shaped items (do not rule here)

- **R4 — run HYPER zero-shot as the machine baseline for R1.** Convert `roles.json` + meta `edges` to hyperedges, mask each of the 109 `provides` facts in turn, record the rank of the true role; report the MRR beside the lane's exact-match recovery rate. One probe lane, Opus, ≈15K conductor FILL by the #250 pricing; no repo write outside `notes/_subreports/` and an `outputs/` scratch dir.
- **R5 — never write a HYPER (or KREPE) output into a meta.** Rank ⇒ advisory ⇒ human eye. If Dave adopts the baseline, the ruling should say so in those words so a later lane cannot launder a rank into a `provides`.

## UNPROVEN

- U1 — that HYPER runs CPU-only at inference (README: Triton "optional"; not verified by running it).
- U2 — that a ≈1.5K-edge graph with 12 roles is inside HYPER's useful regime; the smallest inductive benchmarks in Tables 14–18 were not extracted and may be an order of magnitude larger.
- U3 — the conversion in F6 loses `when` and `priority` granularity; whether the baseline is meaningful without them is a judgment call for the R1 design.

## Sources

- Paper: https://arxiv.org/abs/2506.12362 (ICLR 2026; PDF read, 34 pp) · code + checkpoints: https://github.com/HxyScotthuang/HYPER (MIT)
- Companion report: `notes/_subreports/2026-09-07-253-R-krepe-hkg-diffusion.md` (F10 R1, U1)
- Apollo: `knowledge/roles.json`, `knowledge/components/*.meta.json` `edges`, `knowledge/_decision-graph.json`, `knowledge/_ADVISORY-SIGNALS.md`, `_RESEARCH-graph-engineering-2026-08-05-v3.html`

provenance: 253-R
status: observed
