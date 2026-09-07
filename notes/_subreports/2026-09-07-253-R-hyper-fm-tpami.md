# `#253`-`R-hyper-fm` — Hyper-FM, "Hypergraph Foundation Model" (TPAMI vol. 48 no. 4, Apr 2026, pp. 4063–4080): Desirability · Feasibility · Viability for Apollo

session: `#253` research lane (filed 2026-09-07, ahead of the #253 opener) · 2026-09-07
window: research worker (Fable 5.1), third paper in the side lane with `253-R-krepe-hkg-diffusion.md` and `253-R-hyper-inductive-hkg.md`; touches NO meta, schema, validator or `reviews/META-TAGS-*` (A/B/C-owned — `_HANDOFF-252-lanes-cold.md`)
sub index: `R-hyper-fm`
brief: chat-only — CSDL link + "Hypergraph Foundation Model, Apr. 2026, pp. 4063-4080, vol. 48, DOI 10.1109/TPAMI.2025.3647504"
tokens: `UNMEASURED — harness counter ≈14,999,700 → ≈14,991,000 ≈ 9K QUOTA over 6 tool calls; CSDL and IEEE Xplore unreachable at this seat (JS shell / no response); the arXiv preprint 2503.01203v2 (18 pp, TPAMI camera-ready layout) was text-extracted and read instead — UNPROVEN that v2 is byte-identical to the journal version`

## VERDICT

**Different animal from the other two, and the least applicable of the three.** Hyper-FM (Feng, Gao et al., Tsinghua) is not a knowledge-graph model at all: it is a *vertex-classification* foundation model for **text-attributed hypergraphs** — papers, movies, books, proteins — where every vertex carries a paragraph of text, hyperedges are co-authorship / co-citation / co-rating sets, and the task is to label vertices (3–40 classes) after pre-training on several other domains and **fine-tuning with labels on the target**. Its two contributions are engineering for that setting: a hierarchical neighbour-guided way to fold domain text into vertex features, and a "multi-hypergraph" that joins domains through clustered *bond vertices* so structure transfers without semantic bleed. Headline: ≈13.4% average gain over baselines across 11 curated TAHG datasets, and a "scaling law" finding that **domain diversity, not data volume, is what improves a hypergraph foundation model**. Nothing here predicts a relation, ranks a role, or completes a fact; nothing runs zero-shot; the smallest dataset that showed transfer (PPI-Text, 401 vertices) still needed labels to fine-tune. **Desirability for Apollo is close to zero as a system.** What survives is one finding to carry: *diversity of relational structure beats volume* — which reads directly onto Apollo's own question of whether canon gets stronger by adding more components (volume) or more *kinds* of edge and context (diversity), and lands on the side the graph-engineering research already took. The rest is a taxonomy correction for the receipts: "hypergraph foundation model" now names three unrelated things (Hyper-FM · HYPER · KREPE-class), and the next conductor should not let the shared word do any work.

COUNTS: findings 7 · ruling-shaped 1 · UNPROVEN 3

## What was done

1. CSDL page fetched — GTM shell only (client-rendered); `ieeexplore.ieee.org/document/11311689` returned nothing; DOI resolved by Dave's message. Search located the preprint: arXiv 2503.01203 (v2), same title and authors; PDF pulled and text-extracted (18 pp, TPAMI two-column layout, "IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE" running head).
2. Read: abstract, §I contributions, §II related work (which itself places HYPER and HGFM), §III–IV method, Table I dataset statistics, §V-E scaling law, §VI conclusion.
3. No code sought beyond the paper (no repository URL appears in the extracted text — see UNPROVEN U2).

## Findings

**F1 — what it is.** "Hyper-FM, the first Hypergraph Foundation Model for multi-domain knowledge extraction." Pre-train on a set of source-domain text-attributed hypergraphs `{(T_x, G_x)}` with self-supervised losses (feature masking à la HyperGCL; structure co-occurrence à la SS-HT); fine-tune θ* on the target `(T_tar, G_tar, Y_tar)` for **vertex classification** with an appended MLP head. Supervised at the target; no zero-shot regime is reported.

**F2 — the two mechanisms.** (i) *Hierarchical High-Order Neighbor Guided Vertex Knowledge Embedding*: a language model encodes each vertex's text, then a hierarchy of hypergraph neighbourhoods and a domain description are folded in, so vertices with identical text at different structural positions get different features, and different-dimension features across domains are aligned. (ii) *Hierarchical Multi-Hypergraph Guided Structural Knowledge Extraction*: each domain hypergraph is clustered (optimal cluster count ≈ number of classes — a heuristic they report), clusters are summarised as virtual vertices, and domains are joined via *bond vertices* so cross-domain message passing happens through summaries rather than raw concatenation ("directly connecting multi-domain datasets … impedes … resulting in a decline").

**F3 — the data.** Eleven text-attributed hypergraphs they built (Table I): Aminer-Text 8,226 V / 4,050 E; Cora-CA/CC-Text 2,708 V; Pubmed-CA/CC-Text 19,717 V; Arxiv-Text 22,886 V; Movielens-Text 18,479; IMDB-Text 34,619; GoodBook-Text 5,834; PPI-Text 401 V / 381 E; OGBN-Arxiv 169,343 V. Labels 3–40 classes. Text per vertex 43–588 tokens on average. Every vertex is a *document*; every hyperedge is a *set of documents that co-occur*.

**F4 — the results and the scaling claim.** ≈13.4% average improvement over baselines (classical GNN/HGNN, GCOPE-style multi-domain graph pre-training, LLM-on-graph methods LLaGA / GraphGPT are named as comparators). Transfer degrades with distribution gap: Aminer→Pubmed-CC −0.64%, Aminer→PPI −18.07% (their Fig. 1 motivation). §V-E: "the performance of foundation models does not necessarily improve with an increase in the volume of relational data … as the number of domains increases, the performance … continues to improve" — diversity of structure is the scaling axis.

**F5 — Desirability: near zero as a system.** Apollo's graph has ≈400 entities, 12 roles and typed edges whose *meaning* is the point (`provides`, `mustNotNeighbour`, `supersedes`). Hyper-FM ignores edge type (an incidence matrix H ∈ {0,1}^{|V|×|E|}), needs a paragraph of text per vertex (metas have `purpose` prose — that much exists), and answers "which of L classes is this vertex" — which for Apollo would be at best "which `category` (atom/molecule/…) is this component", already declared on all 137 metas. There is no missing-label problem for it to solve. Grade: **not wanted**.

**F6 — Feasibility: technically runnable, pointlessly.** Fine-tuning needs labelled target vertices; with 137 metas and a handful of classes it would be a toy. The pre-training corpus is theirs (11 TAHGs), not shipped as a checkpoint in the text read (U2). Grade: **feasible in the sense that anything is; no reason to**.

**F7 — Viability: n/a; one finding to carry.** No licence question arises because nothing would be adopted. The finding that *should* travel: when the roles/edges vocabulary is next extended (roles.json `$extension`: input sub-roles, media/identity, needs-attention — owed by ruling, #252), the value is in the new *kind* of edge, not in more members of an existing kind. That is the same lesson `_RESEARCH-graph-engineering-2026-08-05-v3.html` drew ("the edges do [tell you which ruling is live]; they are just not consulted"), now with an external empirical echo. Ruling-shaped: **R6** — none needed; note it on the carry line of the graph-engineering research if Dave wants an external citation for "diversity over volume".

## Taxonomy note for the next conductor

Three "hypergraph foundation" papers arrived this lane and share a word, not a task:
- **Hyper-FM** (TPAMI 2026) — vertex classification on text-attributed hypergraphs; supervised fine-tune; no relations. *Not for us.*
- **HYPER** (ICLR 2026) — zero-shot link prediction on knowledge hypergraphs with unseen relations; 2 MB MIT checkpoint. *Baseline for R1 only (R4/R5 in `R-hyper`).*
- **KREPE** (ICML 2026) — generative fact completion on hyper-relational KGs; needs 10⁵ facts; CC BY-NC-SA. *Test design + brief corrections only (R1–R3 in `R-krepe`).*
None is an author of canon; the constitution (retrieval never recall; Claude authors / Dave vetoes) holds against all three.

## UNPROVEN

- U1 — arXiv v2 ≡ TPAMI print; page/figure numbering not cross-checked against pp. 4063–4080.
- U2 — code/checkpoint availability: no repository URL in the extracted text; not searched further.
- U3 — the "≈13.4%" is the paper's own average across 11 datasets and baselines; per-dataset tables (II–V) were not transcribed.

## Sources

- TPAMI: https://doi.ieeecomputersociety.org/10.1109/TPAMI.2025.3647504 (unreachable at this seat) · preprint read: https://arxiv.org/abs/2503.01203
- Companions: `notes/_subreports/2026-09-07-253-R-krepe-hkg-diffusion.md`, `notes/_subreports/2026-09-07-253-R-hyper-inductive-hkg.md`
- Apollo: `knowledge/roles.json` (`$extension`), `_RESEARCH-graph-engineering-2026-08-05-v3.html`

provenance: 253-R
status: observed
