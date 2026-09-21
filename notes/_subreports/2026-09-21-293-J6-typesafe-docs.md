# 293 · J6 — the whole TypeSafe documentation, read and mapped to Apollo

**Page: `notes/_lanes/293/J6/typesafe-field-guide.html`.** Analysis only. No live call was
made by this lane, no git command was run, and no file outside `notes/_lanes/293/J6/` and
`notes/_subreports/` was created or modified. Nothing on the page is phrased as done,
started or scheduled; every recommendation is after Friday 25 September and only if ruled.

**Headline:** the standing proposal's cost conclusion survives, its request arithmetic does
not. J5 priced A, B and C assuming twenty questions ride in every request — carried over
from J4, which put twenty Memento candidates into one shared `state`. TypeSafe's own
`cookbooks/classifying_rag_passages.md` says the opposite in one line: *"Nothing batches
passages into one request, because each question is about one pair."* Recomputed
one-state-per-request, costs fall and request counts rise roughly 8.6×.

---

## 1. Pages read — 59, all fetched clean, zero failures

Fetched as `.md` with `curl -sL` against `https://docs.typesafe.ai/<path>.md`, sourced from
`llms.txt`. **All 59 returned HTTP 200.** Total 1,095,218 bytes. No page failed to fetch,
no page returned an empty or truncated body, no retry was needed.

The ~50 JavaScript API-reference class/interface/type-alias pages were excluded by brief;
`sdk/javascript.md` was skimmed as instructed. `llms.txt` itself is counted as the index,
not as one of the 59.

### Conceptual and reference (13)
`llms.txt` · `introduction.md` · `introduction/quickstart.md` · `concepts/system-one.md` ·
`concepts/state.md` · `concepts/how-to-build-with-system-one.md` · `concepts/use-case-map.md` ·
`introduction/machine-learning-primer.md` · `confidence.md` · `models.md` · `api.md` ·
`agent-skill.md` · `legal.md` · `model-jaggedness/jev-1.13.md`

### Primitives (5)
`primitives.md` · `primitives/choice.md` · `primitives/score.md` · `primitives/noul.md` ·
`primitives/advanced.md`

### Patterns (5)
`patterns.md` · `patterns/fan-out.md` · `patterns/confidence-routing.md` ·
`patterns/composite-scoring.md` · `patterns/intent-routing.md`

### Demos (2)
`demos.md` · `demos/smart-home.md`

### Cookbooks (18)
`cookbooks/consistency_noul_cookbook.md` · `cookbooks/consistency_choice_cookbook.md` ·
`cookbooks/parallel_questions.md` · `cookbooks/rerank_typesafe.md` ·
`cookbooks/semantic_find.md` · `cookbooks/autoformat.md` · `cookbooks/function_calling.md` ·
`cookbooks/skill_suggestion.md` · `cookbooks/entity_alignment.md` ·
`cookbooks/classifying_rag_passages.md` · `cookbooks/citation_check.md` ·
`cookbooks/llm_guardrails.md` · `cookbooks/sde_cascade.md` ·
`cookbooks/date_extraction_cookbook.md` ·
`cookbooks/pre_parsed_value_extraction_cookbook.md` ·
`cookbooks/hierarchical_classification.md` ·
`cookbooks/autoresearch_feature_discovery.md` ·
`cookbooks/classification_using_confidence.md`

### SDK — Python (11)
`sdk.md` · `sdk/python.md` · `sdk/python/usage.md` · `sdk/python/changelog.md` ·
`sdk/python/api.md` · `sdk/python/api/clients/async.md` · `sdk/python/api/clients/sync.md` ·
`sdk/python/api/types/questions.md` · `sdk/python/api/types/responses.md` ·
`sdk/python/api/retries.md` · `sdk/python/api/types/common.md` ·
`sdk/python/api/exceptions.md` · `sdk/python/api/constants.md`

### SDK — JavaScript, skimmed only (3)
`sdk/javascript.md` · `sdk/javascript/changelog.md` · `sdk/javascript/api.md`

**Pages that failed to fetch: none.**

---

## 2. Facts verified vs declared

Everything in this section is **declared** — published by TypeSafe, not measured by this
lane or any other. The column that matters is whether it *confirms*, *corrects* or *adds
to* what Apollo already held.

| Fact | Value | Status against Apollo's record |
| --- | --- | --- |
| Price | $42/Btok, **$0.042/Mtok input; output tokens free** | **Confirms** J4/J5's $0.042 figure, and adds that output is free — so `usage.input_tokens` alone is a complete bill |
| Usage fields | `usage.input_tokens`, `usage.output_tokens`, both required on the wire, both *nullable* in the SDK schema | **Confirms J4's "the API reports no cost field"** — there is none. J3 already read `usage` live (4,023 in / 177 out) |
| Context | 64k tokens/request total; 32k for `state` + longest question | **New.** Nothing in Apollo held this |
| Rate limits | 250,000 tok/s; 1,200 req/min; 429 on either; warned as changing without notice | **New.** Supports J5's risk 2 ("the limits move") with the vendor's own wording |
| Model aliases | `jev-latest` → `jev-1.13.0`; `jev-preview` → `jev-1.13.0`, no preview build now | **Confirms** the adapter's default |
| Versioned ids | **"Versioned IDs such as `jev-1.13.0` are accepted by the `model` field whether or not they appear in the list."** | **CORRECTS J5's risk 2**, which states "the version in the docs' sample responses is not one you may send." Pinning is available, and `models.md` recommends it where thresholds are tuned to a version |
| Retry defaults | `max_retries=2`, `backoff_initial=0.5`, `backoff_max=5.0`, `backoff_jitter=0.25`, `respect_retry_after=True`, connection + timeout errors retried, overall `timeout=30.0` | **New.** `_jev.py` does not retry by design; this is what "matching the SDK" would mean |
| Retryable statuses | `{408, 429} ∪ range(500,600)` — so **529 is retried** without being named | **New** |
| Per-op timeout | `DEFAULT_TIMEOUT = 10.0` s | **New** |
| Error statuses documented | 401, 422, 429, 529 on `api.md`; SDK adds 400, 403, 404 exception types | **Confirms** lane J2's measured-vs-declared note: a missing key returned **403** live, not the documented 401. The SDK's exception list does carry a 403 type the HTTP page omits |
| Env vars | `TYPESAFE_API_KEY`, `TYPESAFE_BASE_URL`, `TYPESAFE_DEFAULT_MODEL`, `TYPESAFE_LOG_LEVEL`; base URL default `https://api.typesafe.ai`; model default `jev-latest` | **New.** `_jev.py` uses `TYPESAFE_MODEL`, not the SDK's `TYPESAFE_DEFAULT_MODEL` — a naming divergence worth knowing if the SDK is ever swapped in |
| Question limits | Choice ≤ **255 options** (declared reliable to ~240); Score 2–**10** levels; instructions and all criteria accept string \| object \| array | **New, and load-bearing** — this is what makes the semantic_find shape available to Memento |
| Legal / retention | DPA, MCA, Privacy Policy, all off-docs at typesafe.ai; **not trained on customer requests or responses**; **ZDR is enterprise-only**, by request to privacy@typesafe.ai | **New.** Matters the moment client material is sent |
| Logging hazard | At `debug` the Python SDK logs request and response **bodies**; secret headers redacted, **bodies explicitly not** | **New.** Inert while `_jev.py` is stdlib; live the day the SDK lands |
| Language | English primary; other languages handled but less accurately | **New**, not currently relevant |

### The one figure this lane could NOT verify

**The "declared 70–500 ms latency band" does not appear anywhere in the current
documentation.** It is the figure J2, J3, J4 and J5 all measure against — J5's risk 1 is
built on "19 of 19 calls exceeded the declared band."

Searched: `models.md`, `api.md`, every conceptual page, every pattern, every cookbook, the
whole Python SDK reference. `models.md` publishes price, rate limits, context and input
types, and **no latency figure at all**. The only latency number anywhere on the site is a
cookbook's own measured mean round trip of **114 ms** for a Choice
(`cookbooks/consistency_choice_cookbook.md`), on TypeSafe's hardware, not a published
service band.

It may come from the console, from a page since edited, or from lane J's original research
(`notes/_subreports/2026-09-21-293-J-jev-research.md`, not re-read by this lane). **Recorded
as unverified, not as wrong.** The sentence wants re-sourcing before it is shown to anyone.

---

## 3. The recomputation, with its working

Baselines carried in, **measured** by J4: 364.7 input tokens per candidate-question at a
600-char cap; 7,293 input tokens per 20-question request; 920.0 ms per request; 46 ms per
question. Price **declared**: $0.042/1M input, output free.

Derived per-request token estimates (character count ÷ 4, plus question blocks):

- **A**, one request per record: ~150 (600-char body) + ~280 (14-label Choice criteria) +
  ~100 (4-level Score) + ~100 wrapper ≈ **650 tokens**.
- **B** providesRole, one request per meta: ~300 (meta text) + ~250 (12-role Choice) + ~80
  (3-level Score) + ~80 (evidence Nouls) + ~100 wrapper ≈ **810 tokens**.
- **B** usesIcon audit, one request per edge: ~500 (snippet + path data) + ~80 + ~100 ≈
  **680 tokens**.
- **C**, one request per pair: ~500 (both ruling records) + ~150 (3-option Choice) + ~100
  wrapper ≈ **750 tokens**.

| Item | J5 as published | Recomputed one-state-per-request |
| --- | --- | --- |
| A — 2,282 records | 229 reqs · $0.070 · 3.5 min | **2,282 reqs · ~1.48M tok · $0.062 · 35 min serial / ~2 min at 1,200 rpm** |
| B — providesRole | 1,656 pairs · 83 reqs · $0.025 · 76 s | **138 reqs · ~112k tok · $0.005 · 127 s** |
| B — usesIcon audit | 371 pairs · 19 reqs · $0.006 · 18 s | **371 reqs · ~252k tok · $0.011 · 341 s** |
| C — 78 judged pairs | 4 reqs · $0.0012 · 4 s | **78 reqs · ~59k tok · $0.0025 · 72 s** |
| **Programme total** | **335 reqs · ~$0.102 · ~5.5 min** | **2,869 reqs · ~$0.081 · ~48 min serial / ~3 min at 1,200 rpm** |

Plus a new item that did not exist in J5: the **semantic_find shape** over J4's existing
fixture — 14 requests, ~350k tokens, **$0.015**, ~13 s. One Choice per query whose options
are up to ~240 candidate record ids at a 400-char window (~24k state tokens, inside the 32k
budget), plus one Noul asking whether the corpus holds an answer at all. It widens the
shortlist twelvefold, which is the only mechanism that can move J4's measured 4 / 14
absent-from-top-20.

**Honesty on the derivation:** these assume J4's measured per-question rate carries to a
one-state-per-request shape. It does not, exactly — a single-record request pays its
wrapper and criteria block once for one record instead of once for twenty, so the per-record
figure is more likely under-stated than over-stated. Every conclusion survives a doubling.

---

## 4. Token cost of this lane

**Not readable.** This lane made no API call to TypeSafe, so there is no `usage` object and
no receipt line. The 1,095,218 bytes of documentation were fetched over plain HTTPS with
`curl` and read locally. Nothing was appended to `knowledge/_jev-receipts.jsonl`, which
stands at the 19 lines J5 recorded.

---

## 5. Commands run

```
curl -sL https://docs.typesafe.ai/llms.txt            # index
grep -o 'https://docs.typesafe.ai/[^)]*\.md' llms.txt \
  | grep -v '/sdk/javascript/api/'                    # 59 urls, JS class pages excluded
while read u; do curl -sL -w '%{http_code}' -o "$n" "$u"; done   # 59 fetches, all 200
```

No network call touched `api.typesafe.ai`. `.env.local` was never read. No git command was
run.

---

## 6. Six decisions put to Dave, all after the 25th

1. Re-price the standing proposal before ruling on it — the request arithmetic is inverted.
2. Try the line-by-line-search shape over J4's fixture (14 reqs, ~$0.015) before Proposal A,
   or instead of it.
3. Switch B from a Noul with a fitted threshold to entity_alignment's three-level Score with
   none — 1,656 pairs collapse to 138 requests.
4. Use the 31 rows Dave already ratified as plain citations as the calibration set for C's
   confidence threshold.
5. Run the vendor's own self-consistency experiment on one Apollo rubric — the cheapest item
   anyone has proposed, and it de-risks the most expensive one.
6. Decide whether the Data Processing Agreement needs reading before any client material
   goes through this door. ZDR is enterprise-only and we do not have it.
---

## ⚙ THE THREE MACHINE-READ LINES — ADDED BY THE #294 WRAP AT STAGING, AND SAID SO

⚠ **Lane J6 filed this report before `s294-D2` existed** (ruled, inscribed and enacted later the
same day, #294), so it carried none of the three lines `s218-D7` requires and the `s294-D2` arm —
which reads the STAGED set only — would have refused the commit that carries it. The **#294 wrap**
added them rather than exempting the file, on lane C2's own precedent from that session. ⛔ **No
sentence of this lane's was altered, deleted or renumbered, and every figure below is the #294
wrap's count of THIS report's own text, derived and shown:**

**findings 20** = **59 pages fetched as `.md`, ALL HTTP 200, 1,095,218 bytes, zero failures and zero
retries** · ★ **the standing proposal's cost conclusion survives and its REQUEST ARITHMETIC DOES NOT
— `cookbooks/classifying_rag_passages.md` says in one line that nothing batches passages into one
request, so request counts rise roughly 8.6×** · price **CONFIRMED at $0.042 / 1M input and output
tokens FREE**, so `usage.input_tokens` alone is a complete bill · `usage` carries no cost field,
**confirming J4** · context **64k per request, 32k for `state` + longest question — NEW to Apollo** ·
rate limits **250,000 tok/s · 1,200 req/min**, warned as changing without notice — NEW, and it
supports J5's risk 2 in the vendor's own wording · model aliases `jev-latest` → `jev-1.13.0`,
**confirming the adapter's default** · ★ **versioned ids ARE accepted whether or not they appear in
the list, which CORRECTS J5's risk 2** · retry defaults (`max_retries=2`, `backoff_initial=0.5`,
`backoff_max=5.0`, `backoff_jitter=0.25`, `respect_retry_after=True`, `timeout=30.0`) — NEW, and
what *"matching the SDK"* would mean for a `_jev.py` that does not retry by design · retryable
statuses `{408, 429} ∪ range(500,600)`, **so 529 is retried without being named** · per-op
`DEFAULT_TIMEOUT = 10.0 s` · documented error statuses 401/422/429/529 plus the SDK's 400/403/404
types, **confirming lane J2's measured-vs-declared note that a missing key returned 403 live, not
the documented 401** · env vars, and the divergence that matters — **`_jev.py` uses `TYPESAFE_MODEL`,
the SDK `TYPESAFE_DEFAULT_MODEL`** · question limits **Choice ≤ 255 options (reliable to ~240) and
Score 2–10 levels**, which is what makes the `semantic_find` shape available to Memento · legal and
retention, **not trained on customer requests or responses, and ZDR is ENTERPRISE-ONLY** · the
logging hazard — **at `debug` the Python SDK logs request and response BODIES; headers are redacted,
bodies explicitly are not** · English primary · the recomputed programme at **2,869 requests /
~$0.081 / ~48 min serial or ~3 min at 1,200 rpm**, against J5's published 335 / ~$0.102 / ~5.5 min ·
the **`semantic_find` shape as a NEW item that did not exist in J5** (14 requests, ~350k tokens,
$0.015, ~13 s; it widens the shortlist twelvefold, the only mechanism that can move J4's measured
4 / 14) · and **this lane's own token cost is NOT READABLE — no API call, so no `usage` object and no
receipt line; `knowledge/_jev-receipts.jsonl` stands at the 19 lines J5 recorded.**

## RULING-SHAPED QUESTIONS

**ruling-shaped 6** = the lane's own § 6 *"Six decisions put to Dave, all after the 25th"*, as it
numbered them: **(1)** re-price the standing proposal before ruling on it, the request arithmetic
being inverted; **(2)** try the line-by-line-search shape over J4's fixture (14 reqs, ~$0.015)
before Proposal A, or instead of it; **(3)** switch B from a Noul with a fitted threshold to
`entity_alignment`'s three-level Score with none — 1,656 pairs collapse to 138 requests; **(4)** use
the **31 rows Dave already ratified as plain citations** as the calibration set for C's confidence
threshold; **(5)** run the vendor's own self-consistency experiment on one Apollo rubric — *"the
cheapest item anyone has proposed, and it de-risks the most expensive one"*; **(6)** decide whether
the Data Processing Agreement needs reading before any client material goes through this door.

**UNPROVEN 1** ⛔★★ **and it is the sharpest thing in the report: the *"declared 70–500 ms latency
band"* DOES NOT APPEAR ANYWHERE IN THE CURRENT DOCUMENTATION** — searched across `models.md`,
`api.md`, every conceptual page, every pattern, every cookbook and the whole Python SDK reference.
**It is the figure J2, J3, J4 and J5 all measure against, and J5's risk 1 is built on it**
(*"19 of 19 calls exceeded the declared band"*). The only latency number on the site is a cookbook's
own measured **114 ms** mean round trip for a Choice, on TypeSafe's hardware, which is not a
published service band. ⚠ **RECORDED AS UNVERIFIED, NOT AS WRONG** — it may come from the console,
from a page since edited, or from lane J's original research, which this lane did not re-read.
**The sentence wants re-sourcing before it is shown to anyone.**

COUNTS: findings 20 · ruling-shaped 6 · UNPROVEN 1

REPLAY-THESE: `curl -sL https://docs.typesafe.ai/llms.txt` · `grep -o 'https://docs.typesafe.ai/[^)]*\.md' llms.txt | grep -v '/sdk/javascript/api/'` (59 urls, JS class pages excluded) · `while read u; do curl -sL -w '%{http_code}' -o "$n" "$u"; done` (59 fetches, all 200) · `grep -ri "70-500\|70–500\|latency" <the 59 fetched pages>` (the band is absent; the only figure is the Choice cookbook's measured 114 ms)
