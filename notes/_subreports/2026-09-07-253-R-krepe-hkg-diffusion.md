# `#253`-`R-krepe` — KREPE (masked discrete diffusion on hyper-relational KGs, ICML 2026) and its neighbours: Desirability · Feasibility · Viability for Apollo

session: `#253` research lane (filed 2026-09-07, ahead of the #253 opener) · 2026-09-07
window: research worker (Fable 5.1), fired by Dave outside the #253 A/B/C wave — see `_HANDOFF-252-lanes-cold.md`; this lane touches NO meta, NO schema, NO validator, so it cannot collide with lanes A/B/C
sub index: `R-krepe`
brief: chat-only — "research this and any other similar systems … analyse the Desirability, feasibility, and viability for our project: openreview.net/forum?id=lRZmoqiAPg"
tokens: `UNMEASURED — harness counter 15,000,000 → ≈14,947,000 ≈ 53K QUOTA over ~25 tool calls; one sonnet sub (103K) spent on a truncated HTML capture and is NOT the source of anything below — every figure comes from the arXiv PDF read at this seat`

## VERDICT

**KREPE is not a build candidate for Apollo, at any horizon; it IS a usable test design and a brief-writing correction, both free.** The paper (Lee, Kim, Whang, KAIST, ICML 2026, arXiv 2605.24064) trains a 12–16-layer transformer with masked discrete diffusion over a hyper-relational knowledge graph — facts of the shape `((h, r, t), {(k_i, v_i)})` — so it can fill *any* subset of a fact's components, including all of them ("fact generation"). It reports SOTA link prediction (WD50K All MRR 0.419 vs MAYPL 0.411) and 0.717–0.855 judged-valid facts from scratch vs ≤0.369 for the best LLM-prompted baseline (Table 4). **Desirability is real but narrow**: Apollo's `roles.json` providers are literally hyper-relational facts — `(slot, wants, role)` qualified by `{priority, when}` — and the 25-meta pass (lanes A/B) is hand-authoring exactly the "arbitrarily masked fact" KREPE completes. **Feasibility is nil at our scale**: KREPE learns from 166K–306K facts over 35K–48K entities; Apollo holds 109 provider facts, ≈1,231 typed meta edges and 12 roles. A diffusion model on that corpus memorises; it cannot generalise, and the paper's own ablation (v: swapping the objective ⇒ generation accuracy 0.038) shows how fragile the generative capacity is even at full scale. **Viability is blocked twice over**: the code is CC BY-NC-SA 4.0 (non-commercial; Apollo carries HSBC token stores), and Apollo's constitution is *retrieval, never recall* with Dave as the only one who rules — a trained generator proposing `provides`/`when` is a GENERATOR the do-not-rule list cannot fence ([[do-not-rule-list-cannot-fence-a-generator]]). What transfers is (a) the **masking evaluation** — mask a field on a meta, see whether Claude-with-retrieval recovers it: a calibration test the README already promises and nobody has designed; (b) the **joint-vs-sequential finding** — KREPE's iterative/Gibbs baselines (fill one component at a time with a SOTA discriminative model) score 0.20–0.45 against 0.51–0.86 for joint decoding, which argues lanes A/B should author the six fields *together* per meta, not field-by-field; (c) the **context-message ablation** (i: −0.17 generation accuracy without neighbour context) — the paper's version of the graph-engineering research's candidate #1, one-hop edge expansion at retrieval, which is still unbuilt.

COUNTS: findings 11 · ruling-shaped 3 · UNPROVEN 4

## What was done

1. OpenReview is Cloudflare-gated in every route this seat has (page, `api2` JSON 403 `ChallengeRequiredError`, built-in browser pane "Verification failed to load"); Dave supplied the title; the arXiv PDF (28 pp) was pulled and text-extracted with pdfplumber. The GitHub repo README was fetched whole.
2. Paper read for: task definitions, method (§4.1–4.4), Tables 1–6, 8, 9, 13, §6, licence, hardware.
3. Comparable-systems sweep by search + abstract fetch: MAYPL (ICML 2025), HDiff (EMNLP 2025 Findings), THOR (2026), DARK (2025), "One Pass for All" (2026), HYPER (2025). Abstract-level only for all but KREPE — see UNPROVEN.
4. Apollo grounding by script over the repo: 137 metas (keys counted), `roles.json` 12 roles / 109 provider facts / 0 `with` / 0 `not-with`, meta `edges` 1,231, `relationships` strings 967, decision graph 101 nodes / 168 edges, usage graph 108 / 641, 387 rulings, `chart-intents.json` 5 intents. Prior research `_RESEARCH-graph-engineering-2026-08-05-v3.html` re-read for its verdict and six candidates.

## Findings

### The paper, as read (F1–F5)

**F1 — what a "hyper-relational fact" is, and why the shape matters here.** ξ = ((h, r, t), Q) with Q a set of (qualifier-relation, qualifier-entity) pairs. Link prediction = one blank; *fact generation* (their new task, Def 3.3) = "generating a valid hyper-relational fact from an arbitrarily masked query, i.e., completing a partially observed fact or generating a fact from scratch". Three settings: Scratch (all masked), Targeted (one known), Arbitrary Masking.

**F2 — the method in one paragraph.** Contextual message passing: every fact is decomposed into role-tagged (relation, entity) pairs; a fact rep is the SUM of pair reps; the message to a pair is the fact rep MINUS that pair's own rep (so a component is predicted only from its context); entities/relations aggregate messages over all facts they sit in via multi-head attention. Shared init tokens for all entities and all relations (no per-entity ID). Decoding: masked components become learnable mask vectors, scored by dot product against every candidate in V or R. Training: masked discrete diffusion (Austin et al. 2021) with a *bi-level noising strategy* — mask components inside a fact AND stochastically sample which facts are observed (train_graph_ratio 0.7) — under an any-order autoregressive (AO-AR) loss. Inference: iterative decoding, re-scoring all masks each step, top-p replacement of a random subset, caching so cost is O(|ζ|² d² (L+|V|+|R|)).

**F3 — numbers.** Datasets (Table 9): WD50K 47,155 entities / 531 relations / 166,435 train facts; WikiPeople⁻ 34,825 / 178 / 294,439; WikiPeople 47,765 / 193 / 305,725. Link prediction (Table 1, All positions): WD50K MRR 0.419 (MAYPL 0.411); WikiPeople⁻ 0.522 (0.521); WikiPeople 0.491 (0.488). Relation prediction MRR 0.963–0.984. Fact generation accuracy, GPT-5.2 judge (Table 4): Scratch 0.717 / 0.855 / 0.777; Targeted 0.508 / 0.600 / 0.591; Arbitrary 0.604 / 0.649 / 0.621 — versus best non-KREPE per column 0.351 / 0.369 / 0.326 / 0.482 / 0.394 / 0.396 / 0.604 / 0.497 / 0.469. Judge validated: Pearson 0.997 vs three-LLM unanimous consensus, 0.987 vs three-human unanimous on a 10% subset (Table 6). Runtime (Table 13): 0.53–0.91 s/query at 50–1000 steps, batch 0.08 s/query; 16 layers d=128 on WD50K (RTX 3090), 12 layers d=256 on WikiPeople (RTX A6000), 1,750–2,000 epochs.

**F4 — the two ablations that matter for us.** (i) remove context messages: scratch-generation accuracy 0.717→0.552 (WD50K), 0.855→0.578 (WP⁻). (v) replace the AO-AR objective with plain link-prediction cross-entropy: link prediction unchanged (0.415 vs 0.419) but generation collapses to 0.038 / 0.002. The generative capacity is the objective, not the architecture.

**F5 — stated limits.** Transductive only; §6 names inductive (unseen entities/relations) as future work. Evaluation novelty is enforced by rejection sampling against the training set (10 tries, then scored wrong). Code CC BY-NC-SA 4.0. Python 3.11 / PyTorch 2.6 / CUDA 11.8. Verification harness needs an OpenAI key.

### The neighbours (F6)

**F6 — six similar systems, one line each, what each would mean here.**
- **MAYPL** (same lab, ICML 2025, "Structure Is All You Need") — structure-only HKG representation, the discriminative backbone KREPE is built on and beats by ~0.01 MRR. Same scale problem for us.
- **HDiff** (EMNLP 2025 Findings) — confidence-guided *continuous* denoising diffusion for HKG link prediction, aimed at noisy graphs (intra-fact inconsistency, cross-fact association noise). Nearest prior to KREPE; still one-blank.
- **THOR** (arXiv 2602.05424, 2026) — *inductive* HKG link prediction via relation and entity "foundation graphs" + transformer decoder; claims +20–66% over inductive baselines across 12 datasets. Only one of the six that could in principle be applied to a graph it was not trained on — which is the only regime Apollo's size allows. UNPROVEN whether it transfers to a non-Wikidata vocabulary.
- **DARK** (arXiv 2510.11462) — masked diffusion over plain KGs unifying deductive (answer a logical query) and abductive (generate the hypothesis) reasoning, with self-reflective denoising and RL exploration. Closest in *spirit* to "propose the rule that explains these facts", but plain triples, no qualifiers.
- **"One Pass for All"** (arXiv 2604.18344, 2026) — discrete diffusion for triple-*set* prediction (many triples at once). PDF fetched empty; abstract-level only.
- **HYPER** (arXiv 2506.12362, 2025) — "foundation model for inductive link prediction with knowledge hypergraphs". Not read; named for completeness.
Nothing in this family runs without a graph two to three orders of magnitude larger than Apollo's.

### DFV against Apollo (F7–F11)

**F7 — Desirability: the fit is structural and exact, the need is small.** `roles.json` already encodes hyper-relational facts: `(stat-card, provides, headline-metric)` with qualifiers `{priority: 60, when: "default — label · value · delta · period, no series"}`; `not-with` = `{slug, when}` is another qualifier pair. The 25-meta pass is manual arbitrary-masking completion: given the meta's `purpose` and `roles.json` membership, fill `provides · answers · shape · span · priority · when`. So the *task* KREPE names is the task the next session is doing. But the volume is 25 metas now and ≤137 ever; the value of automating it is one afternoon's Opus lanes. Desirability grade: **real, low**.

**F8 — Feasibility: no, by three orders of magnitude.** Training corpus at hand: 109 provider facts + ≈1,231 typed edges + 168 decision edges ≈ 1.5K facts over ≈400 entities (137 components, 12 roles, contexts, patterns, tokens). KREPE's smallest benchmark is 166K facts / 47K entities; its shared-initialisation trick (F2) exists precisely because per-entity parameters overfit *at that scale*. On 1.5K facts a 12-layer transformer memorises the train set and the rejection-sampling novelty rule in F5 would mark nearly every output wrong. The inductive route (THOR/HYPER) is the only one where our graph is the *inference* graph, not the training graph — UNPROVEN, and it would still hand back Wikidata-shaped priors about `headline-metric`. Feasibility grade: **not feasible as a trained model; unproven as an inductive borrow**.

**F9 — Viability: blocked by licence and by constitution.** CC BY-NC-SA on the code; Apollo's canon carries `_icon-scale-hsbc-general.json` / `_spacing-hsbc-general.json` — a commercial context; a clean-room reimplementation is a research project, not a lane. Deeper: Apollo's operating rule is *retrieval, never recall* (README) and *Claude authors / Dave vetoes* (s251-D15) with every ruling carrying a `by: Dave` line. A model that emits `provides: chart-panel, priority: 30` with a softmax score is a generator whose outputs are not addressable to a ruling — [[do-not-rule-list-cannot-fence-a-generator]] and [[instrument-without-a-consumer]] both apply: nothing in the gate suite could consume a probability, and `_validate_roles_resolve.py` (lane C) refuses unknown slugs loud and named, which is the opposite posture. Viability grade: **not viable**.

**F10 — what transfers for free: a test, not a system.** The README promises a "calibration re-run (a completed project, blind, compared with what shipped)". KREPE's *Arbitrary Masking* protocol is a ready-made design for it at meta granularity: take the 15 metas that already carry `intent`, mask it, ask a lane (with and without one-hop neighbours in the brief) to recover it, score exact-match against canon, and repeat for `provides` once A/B land. Two numbers fall out — recovery rate with context, recovery rate without — and the second is the paper's ablation (i) run on our corpus. Ruling-shaped: **R1** adopt the masked-recovery test as the calibration design for metas (Dave's call; nothing built here).

**F11 — what transfers as a brief correction: author jointly, not sequentially.** KREPE's weakest baselines are the ones Apollo's lanes most resemble: *Iterative Prediction* (fill missing components one at a time with the SOTA discriminative model) 0.20–0.45 and *Gibbs Sampling* 0.18–0.42, against joint decoding 0.51–0.86 (Table 4). Read across: a lane that decides `provides`, then `answers`, then `when` in sequence will produce less coherent metas than one told to draft all six as one object and then check each against the others (`when` must name the condition under which this `provides` beats its co-providers at this `priority`). Ruling-shaped: **R2** the A/B briefs say "author the six fields as one object per meta; the `when` predicate must reference the sibling providers' `when` in `roles.json`". Also from ablation (i): **R3** put each meta's `roles.json` siblings and its `edges.mustNotNeighbour` targets *in the brief* (one-hop expansion by hand) — the same move as candidate #1 in the graph-engineering research, still unbuilt on the retrieval path.

## Dave-shaped items (do not rule here)

- R1 — masked-recovery calibration test for metas (F10). Design only; no lane briefed.
- R2 — joint-authoring clause in the A/B briefs (F11). Cheap; could go into the #253 opener if Dave says so.
- R3 — one-hop neighbours pasted into A/B briefs (F11). Cheap.

## UNPROVEN

- U1 — that THOR (or HYPER) run inductively on Apollo's graph returns anything but Wikidata priors; not attempted, no GPU at this seat.
- U2 — the Apollo fact count (≈1.5K) is a script estimate over `roles.json` providers + meta `edges` lists + decision-graph edges; contexts/patterns/tokens were not deduplicated into an entity set.
- U3 — "One Pass for All" and HYPER are abstract-only; DARK, THOR abstract-only.
- U4 — KREPE's Table 5/6 figures are on WikiPeople⁻ only; the paper's LLM baselines used GPT-5.2 and Gemini 3.0 Pro as *generators* with MAYPL as the backbone where a model was needed — the "LLM loses to KREPE" headline is about LLMs prompted with ≤1,000 facts, not LLMs with retrieval over the graph, so it does NOT bear on Claude-with-retrieval in Apollo.

## Sources

- Paper: https://arxiv.org/abs/2605.24064 (PDF read: 28 pp) · code: https://github.com/bdi-lab/KREPE (CC BY-NC-SA 4.0) · OpenReview: https://openreview.net/forum?id=lRZmoqiAPg (gated at this seat)
- MAYPL: https://github.com/bdi-lab/MAYPL · https://openreview.net/forum?id=2tH2vexW1Z
- HDiff: https://aclanthology.org/2025.findings-emnlp.391/
- THOR: https://arxiv.org/abs/2602.05424 · DARK: https://arxiv.org/abs/2510.11462 · One Pass for All: https://arxiv.org/abs/2604.18344 · HYPER: https://arxiv.org/abs/2506.12362
- Apollo: `README.md`, `knowledge/roles.json`, `knowledge/components/*.meta.json`, `knowledge/_decision-graph.json`, `_RESEARCH-graph-engineering-2026-08-05-v3.html`, `_HANDOFF-252-lanes-cold.md`

provenance: 253-R · 2026-09-07
status: observed
