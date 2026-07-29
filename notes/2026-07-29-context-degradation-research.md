# Context-window degradation — verification pass on Dave's paste, and what it does to the gauge

```
provenance: worker-context-degradation · 2026-07-29
status: floated
```

**Register: FLOATED — research + proposals. Nothing ruled, nothing enacted, no git.**
**Role: WORKER.** Receipt: `notes/_receipts/2026-07-29-context-degradation-worker.md`.
**Model:** Opus 5. **Stamp:** 2026-07-29 (sandbox `date`).
**Origin:** Dave pasted third-party research on context-window degradation, hallucination thresholds
and prompt caching, and asked for independent verification plus concrete proposals.

**Context gauge at authoring: ⛔ CANNOT BE STATED — and that is the headline finding, not a dodge.**
The gauge divides by `DEFAULT_WINDOW = 200_000`. Anthropic's published spec for the model running this
session (Opus 5) is **1M tokens, default, no beta header**. My tape is ~70–80K `cl100k` proxy tokens.
That is **~37% against 200K** (🟡 AMBER) or **~7.5% against 1M** (🟢 GREEN). Same session, two bands,
three bands apart. **I will not name a band off an unmeasured denominator** — see P1.

---

## §0 — Exec summary

1. **The paste is roughly half-sound.** Every *paper* it cites is real and I read them. Every
   *Claude-model-specific threshold* it states ("Opus 5 safe to 350K", "Fable 5 safe to 500K",
   "750K danger zone") is **unsupported** — sourced to YouTube, Medium, Instagram and vendor blogs,
   and contradicted in shape by the primary literature. Full verdict table in §2.
2. **★ THE FINDING — the band table's unit is wrong.** The published degradation literature measures
   in **absolute tokens** (32K / 128K / 200K). Apollo's throttle measures in **% of window**. The two
   are only interchangeable if the window is known, and Apollo's window is a **hardcoded guess that
   has never been measured** and is contradicted by Anthropic's own spec. This is
   [[measure-dont-convert-units]] firing on the instrument built to enforce it: *a count is not a
   measurement; name the unit.* The unit named is `%`, and `%` of *what* is unset.
3. **Three further verified defects in the gauge**, each independently under-reporting: wrong
   tokenizer (`cl100k` is OpenAI's, not Claude's), uncounted thinking tokens (kept-by-default on
   Opus 4.5+, stripped on Haiku — so a fill number means different things per model), and a
   `MODEL-ROUTING.md` default tier naming **Opus 4.8** while this session runs **Opus 5**.
4. **Five platform capabilities Apollo is not using**, all verified in docs today: the token-counting
   API (exact, ends the estimate era), context awareness on Sonnet 5 (a *free live meter*),
   task budgets (the throttle, server-side), server-side compaction (the flush, automated), and
   cache diagnostics.
5. **⛔ ONE FORK TO DAVE, and it is large.** If the window is 1M, the ruled refill arithmetic
   (*"a fresh window buys ~78%, not 100%"*) is a %-of-200K figure and the flush economy inverts.
   **Do not act on this note until P1 returns a number.** §5.

### Next steps, in order

| # | Do | Cost | Blocks |
|---|---|---|---|
| **P1** | **Measure the window.** One throwaway Sonnet 5 session, one tool call, quote the injected `<system_warning>`. | ~2 min, one session | everything below |
| **P2** | Re-express the band table in **absolute tokens**, `%` derived for display. | small edit, Dave's numbers | P1 |
| **P3** | Swap `tiktoken/cl100k` for Anthropic's token-counting API; until then re-label every number "cl100k **proxy**". | half a lane | — |
| **P4** | Give the gauge a **model** field; count thinking on Opus. | half a lane | P1 |
| **P5** | Refresh `MODEL-ROUTING.md` — Opus 4.8 → Opus 5, verified price table, Sonnet 5 price step 1 Sep 2026. | small | — |
| **P6** | Inscribe the corrected Fable-refusal mechanism **before** the folklore version lands anywhere. | small | — |
| **P7** | Correct the cache-invalidation notes: the mid-session rule is now *partly false* on Opus 5. | small | — |
| **P8** | ⛔ **Fork:** re-price the refill economy against the measured window. | Dave's call | P1 |

---

## §1 — What was actually verified (OBSERVED, fetched 2026-07-29)

All four Anthropic pages fetched in full today; both arXiv papers located and their abstracts read.

### 1a. Context windows — [platform doc](https://platform.claude.com/docs/en/build-with-claude/context-windows)

- **1M-token context window** on Opus 5, Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 5, Sonnet 4.6, Fable 5,
  Mythos 5, Mythos Preview. *"For every model with a 1M-token context window, 1M is the default: you
  don't need a beta header."* Sonnet 4.5 and others: 200K.
- Anthropic **uses the term "context rot" in its own docs**: *"As token count grows, accuracy and
  recall degrade… This makes curating what's in context just as important as how much space is
  available."* The phenomenon is vendor-acknowledged. The *thresholds* are not vendor-published.
- **★ Context awareness.** Sonnet 5, Sonnet 4.6, Sonnet 4.5, Haiku 4.5 receive API-injected tags:
  `<budget:token_budget>…</budget:token_budget>` in the system prompt, and after **every tool call**
  `<system_warning>Token usage: 35000/200000; 165000 remaining</system_warning>`.
  **"Claude Opus 4.7 and later Opus models, Claude Fable 5, and Claude Mythos 5 don't receive these
  injected tags."**
  ⇒ *Confirmed by direct observation this session: I am Opus 5 and no such tag is present in my
  context.* This is why the gauge is a hand-estimate — **and it is a solved problem on Sonnet.**
- **★ Thinking blocks are KEPT by default** on Opus 4.5+ and Sonnet 4.6+, Fable 5, Mythos 5, and
  *"count toward the context window like any other input tokens."* On earlier Opus/Sonnet and **all
  Haiku models** they are automatically stripped.
- Everything counts: system prompt, every message, tool results, images, documents, **tool
  definitions**, and the model's own thinking.
- Companion levers: **server-side compaction** (beta, 4.6+), **context editing** (tool-result
  clearing, thinking-block clearing), **token counting API**, **task budgets** (beta — an explicit
  budget you hand to Opus 4.7+/Fable 5/Mythos 5, which *do not* get the injected tags).

### 1b. Prompt caching — [platform doc](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

Verified pricing multipliers: **5-min cache write ×1.25 · 1-hour cache write ×2 · cache read ×0.1.**
Verified per-MTok table (today):

| Model | Input | 5m write | 1h write | Cache hit | Output |
|---|---|---|---|---|---|
| Fable 5 | $10 | $12.50 | $20 | $1 | $50 |
| **Opus 5** | **$5** | $6.25 | $10 | $0.50 | **$25** |
| Opus 4.8 / 4.7 / 4.6 / 4.5 | $5 | $6.25 | $10 | $0.50 | $25 |
| Sonnet 5 *(to 31 Aug 2026)* | **$2** | $2.50 | $4 | $0.20 | **$10** |
| Sonnet 5 *(from 1 Sep 2026)* | **$3** | $3.75 | $6 | $0.30 | **$15** |
| Haiku 4.5 | $1 | $1.25 | $2 | $0.10 | $5 |

Other verified mechanics that bear on Apollo:

- 5-minute TTL is **refreshed for free on every hit** — the paste's "rolling timer" claim is correct.
- **Minimum cacheable prompt: 512 tokens on Opus 5 / Fable 5 / Mythos 5** — down from 4,096 on
  Opus 4.5/4.6. Small prefixes are now cacheable that previously were not.
- **Lookback window is 20 blocks.** A growing conversation that adds ≥20 blocks between breakpoints
  silently stops hitting cache. Relevant to long agentic sessions.
- **★ Changing `effort` always invalidates message blocks** — and Dave's Cowork effort knob is
  exactly that control. Changing effort mid-session is a cache flush.
- **★ On Opus 5 / Opus 4.8 / Fable 5 / Mythos 5 you can append a mid-conversation `{"role":"system"}`
  message without invalidating system or message caches.** *Not* available on Sonnet 5.
- **Pre-warming** with `max_tokens: 0` is now a first-class feature.

### 1c. Refusals and fallback — [platform doc](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback)

The paste's most dangerous passage, because it welds a **true detail** to a **false mechanism**.

**True:** Fable 5 has safety classifiers that can decline; a decline is an HTTP 200 with
`stop_reason: "refusal"`; and there is a real Fable-5 → Opus-4.8 fallback path
(`fallbacks=[{"model": "claude-opus-4-8"}]`, beta `server-side-fallback-2026-06-01`).

**False, or unsupported:**

- It is **opt-in**. You pass `fallbacks` + the beta header, or install SDK middleware. **Nothing
  silently "routes the session down."** In Cowork, Dave has no such parameter.
- It is triggered by **request content**, not context length. The four categories are `cyber`,
  `bio`, `frontier_llm`, `reasoning_extraction`. **None of them is "cluttered context."**
- The paste's *"overwhelming the context window with complex, cluttered text can trigger false
  positives"* appears **nowhere** in the documentation. It is invented mechanism.
- Corollary worth keeping: `reasoning_extraction` fires when a request *"asks the model to reproduce
  its internal reasoning in the response text."* That is a real, nameable category — and it is the
  one Apollo could plausibly trip, given how much of this programme is about making reasoning legible.

⇒ **`MODEL-ROUTING.md` already inoculates against exactly this paragraph:** *"Diagnose before
attributing a failure to safety classifiers. Our one logged 'refusal' (Playwright, 07-22) was a
misdiagnosis of an installer's expected exit."* The canon was right before the paste arrived. Good.

### 1d. The primary literature

| Source | Real? | What it actually says |
|---|---|---|
| [Chroma, *Context Rot*](https://research.trychroma.com/context-rot) (Hong, Troynikov, Huber, Jul 2025) | ✅ | 18 frontier models (GPT-4.1, Claude 4, Gemini 2.5, Qwen3). **Every one degrades as input grows**, non-uniformly, well before the documented limit. Evaluated on LongMemEval. |
| [arXiv 2509.21361 — *Maximum Effective Context Window*](https://arxiv.org/abs/2509.21361) (Paulsen, Sep 2025, rev. Apr 2026) | ✅ | MECW ≪ MCW and **shifts by problem type**. *"Some top-of-the-line models failed with as little as 100 tokens in context, with most experiencing severe degradation in accuracy by 1000 tokens."* **Far more pessimistic than the paste's "20–30% rule", and stated in absolute tokens, not percentages.** |
| [arXiv 2603.08274 — *How Much Do LLMs Hallucinate in Document Q&A?*](https://arxiv.org/abs/2603.08274) (Mar 2026) | ✅ | 172-billion-token study. Fabrication **1.19% best-case at 32K**, ~**triples at 128K**, **>10% for all models at 200K**. ⚠ **35 open-weight models — no Claude, no GPT.** The paste presented it as covering "top-tier models"; it does not. |
| "Lost in the middle" U-curve | ✅ (well-established) | Real, long-replicated finding; the paste's "15–20 percentage points" is a plausible restatement but is not attributed to a primary source in the paste. |

---

## §2 — Verdict table on the paste, claim by claim

| Claim in the paste | Verdict | Note |
|---|---|---|
| Opus 5 and Fable 5 have 1M-token windows | ✅ **VERIFIED** | Platform doc, today. |
| Context rot is real and pre-limit | ✅ **VERIFIED** | Anthropic's own doc + Chroma. |
| Cache read = 0.1× base; Fable read $1/MTok | ✅ **VERIFIED** | Pricing table matches exactly. |
| 5-min TTL refreshes free on hit; 1h TTL costs more | ✅ **VERIFIED** | 1h write is **×2**, ~$20/MTok on Fable. |
| Cache is prefix-exact; reordering/whitespace breaks it | ✅ **VERIFIED** | Plus: 20-block lookback, `effort`/`thinking`/images/`tool_choice` all invalidate. |
| Put instructions last (recency) | ✅ **plausible, weakly sourced** | Consistent with the U-curve; the paste cites a Reddit thread for it. |
| XML tagging + document IDs help retrieval | ✅ **consistent with Anthropic guidance** | Fine as craft advice. |
| "20–30% rule" — degrade past a *fraction* of window | ⚠️ **MIS-STATED** | The MECW paper it cites gives **absolute** token failures (100–1,000 tk), not fractions. The fraction framing is the paste's own. |
| Fabrication 5–7% moderate, >10% at 200K | ⚠️ **TRUE BUT MIS-SCOPED** | Real numbers — for **35 open-weight models**. Not measured on Claude. |
| **Opus 5: "safe 0–350K", "degradation ~400K", "750K danger zone"** | ❌ **UNSUPPORTED** | No primary source exists. Cited to YouTube, Medium, bleap.finance. |
| **Fable 5: "safe 0–500K", "degrades past 600K"** | ❌ **UNSUPPORTED** | Same. Cited to Instagram, OpenRouter, vendor blogs. |
| **Fable 5 "routes the session down to Opus 4.8" under context pressure** | ❌ **FALSE MECHANISM** | Fallback is real but **opt-in, per-request, content-triggered — never context-triggered, never silent.** §1c. |
| **"Hallucinated constraints / false refusals" from cluttered context** | ❌ **INVENTED** | Not in any doc. This is the class `MODEL-ROUTING` rule already forbids acting on. |
| "Opus 5 features Thinking on by default" | ⚠️ **PARTLY** | Adaptive thinking is real; the framing and the "verification loops" gloss are not vendor claims. |

**Pattern worth naming:** the paste is most confident exactly where it is least sourced. Its verifiable
half (caching mechanics, window sizes) is sourced to `platform.claude.com`; its load-bearing half
(model-specific safe ranges) is sourced to content marketing. **That inversion is the tell**, and it is
the same shape as [[silent-lookup-failure-class]] — fluent output over an unverified lookup.

---

## §3 — What this does to Apollo's instruments

### ★ P1 — MEASURE THE WINDOW. Nothing else in this note is safe until this returns.

`knowledge/_context_gauge.py` line 34: `DEFAULT_WINDOW = 200_000`, comment *"Measured, adjustable."*
**It is not measured.** It is the Sonnet-4.5-era default, and it has been the denominator under every
band Apollo has ever quoted — including the band table Dave ratified.

**The test, and it is cheap:**

> Open one throwaway **Sonnet 5** Cowork session. Make any single tool call. Ask it to quote verbatim
> the `<system_warning>` line it received. The API injects `Token usage: X/Y; Z remaining` — **Y is
> the true window for this environment.**

This works because Sonnet 5 *does* receive context-awareness tags and Opus 5 *does not*. It costs one
short Sonnet session (cheapest tier that fits, per routing rule 1). If Cowork's Sonnet 5 reports
`Y = 1000000`, the gauge is 5× wrong and every historical band is inflated. If it reports `Y = 200000`,
the gauge is vindicated and this whole section closes with a receipt.

⚠️ **Caveat, stated rather than hidden:** Sonnet 5's window is not *necessarily* Opus 5's window in the
same harness. The test measures Sonnet's; treat Opus's as INFERRED-from-it until a second method
confirms. **UNKNOWN is never defaulted** ([[feedback-measuring-tool-must-not-guess]]).

### ★ P2 — Re-express the band table in absolute tokens

Every degradation number in the literature is absolute (32K, 128K, 200K, "by 1,000 tokens"). Apollo's
band is relative. A relative band **cannot be checked against the evidence** and **silently re-scales
when the window changes** — which is exactly the failure P1 is chasing.

Proposal: bands become **token lines**, with `%` as a derived display column:

```
🟢 GREEN   tape < G tk        (display: <45% of measured window)
🟡 AMBER   G ≤ tape < R tk
🔴 RED     tape ≥ R tk
```

`G` and `R` are Dave's to set, and setting them is a real ruling, not a restatement — **but they can
now be argued from evidence** rather than from feel. **The numbers stay Dave's; only the unit changes.**

### P3 — `cl100k` is the wrong tokenizer, and ds-021 names the wrong unit

`_context_gauge.py` uses `tiktoken.get_encoding("cl100k_base")`. **That is OpenAI's GPT-3.5/4
tokenizer.** It is not Claude's. Every `tape` figure in every stamp, banner and receipt in this repo is
a *GPT-token proxy for a Claude-token quantity* — the textbook [[measure-dont-convert-units]] error, and
it has been sitting inside the instrument that teaches the lesson.

Two moves, either acceptable:

- **(a) Exact:** call Anthropic's [token counting API](https://platform.claude.com/docs/en/build-with-claude/token-counting)
  (`/v1/messages/count_tokens`) — returns the real count for a given model. Needs network + a key from
  the gauge's out-of-band lane, which already runs outside the main window.
- **(b) Honest-cheap:** keep `cl100k`, but **rename the unit everywhere** from `tape` to
  `tape(cl100k-proxy)` and stop implying it is a Claude-token measurement. Costs nothing, lies less.

⚠️ **(b) does not fix the arithmetic, only the claim.** Do not register (b) as closing the defect.

### P4 — The gauge has no model field, and thinking makes that fatal

Verified today: thinking blocks are **kept** on Opus 4.5+/Sonnet 4.6+/Fable 5 and **count as input
tokens**; they are **stripped** on earlier Opus/Sonnet and **all Haiku**.

⇒ **The same tape number means different fills on different models**, and the gap grows with every
turn. Worse: the gauge's out-of-band reader is *a Haiku subagent reading a transcript dump* — Haiku is
the one tier where thinking never accumulates, so the reader's intuition is systematically wrong about
the window it is measuring. Whether `session_info.read_transcript` even emits thinking blocks is
**UNTESTED** — worth one grep before P4 is scoped.

**Proposal:** `_context_gauge.py` takes `--model`, and the thinking-retention behaviour is a per-model
constant in the script, not an assumption.

### P5 — `MODEL-ROUTING.md` is stale in its default tier

The table names **"Opus 4.8 · high"** as *Default — complex*. **This session is `claude-opus-5`.**
Also now verifiable: Opus 5 costs **$5/$25** per MTok, i.e. **one third** of the Opus 4.1 rate the
routing economy was originally felt against; Fable 5 is **$10/$50**, exactly 2× Opus 5 in both
directions; and **Sonnet 5 steps from $2/$10 to $3/$15 on 1 September 2026** — five weeks out, and a
direct input to the budget-aware routing governor.

### P6 — Inscribe the corrected refusal mechanism now

Not because it is urgent, but because **the folklore version is more memorable than the true one**, and
the paste is now in the session record where a future window may retrieve it. One paragraph in the
Fable-era notes, quoting §1c. This is the [[assertion-propagation-gap]] pattern: a doc known-wrong-now
is never chased unless something writes the correction down.

### P7 — Two cache-invalidation lines in `MODEL-ROUTING.md` need splitting

The anti-pattern *"never switch model mid-session — it invalidates the whole prompt cache"* is
**VERIFIED and stands.** But two adjacent facts are now different from what the file implies:

- **Newly true:** on Opus 5 / 4.8 / Fable 5 / Mythos 5, a mid-conversation `{"role":"system"}` message
  **does not** invalidate system or message caches. A mid-session ruling is no longer necessarily a
  cache flush. *(Not exposed as a Cowork knob — this is a Code/API-era win, like the rest of the file.)*
- **Newly relevant:** changing **`effort`** always invalidates message blocks. Dave's Cowork effort
  knob is a cache-killer, and the file currently records effort as a free per-session dial.

---

## §4 — Platform capabilities Apollo is not using (all verified today)

| Capability | What it would replace | Where |
|---|---|---|
| **Token counting API** | the `cl100k` estimate | P3 |
| **Context awareness (Sonnet 5)** | the hand-estimated fill, entirely | P1 — *free live meter* |
| **Task budgets (beta)** | the throttle, but server-side, on Opus 4.7+/Fable 5 | horizon |
| **Server-side compaction (beta, 4.6+)** | the flush ritual, automated | horizon |
| **Context editing** (tool-result / thinking-block clearing) | manual spine-flush | horizon |
| **Cache diagnostics (beta)** | guessing why a cache missed | horizon |
| **Prompt-caching floor now 512 tk on Opus 5** | "too small to cache" assumptions | now |

⚠️ Everything marked *horizon* is **API-only**. Per the 2026-07-21 observation already in memory,
these are not Cowork knobs. They pay off on a move to Code — same conclusion `MODEL-ROUTING.md`
already reaches for `/model`. **No action; recorded so the next window does not re-derive it.**

---

## §5 — ⛔ THE FORK TO DAVE

**The refill arithmetic is denominated in the unmeasured window.**

Ruled and load-bearing: *"a fresh session reached ~22% fill … before doing any work ⇒ a fresh window
buys ~78%, not 100%"*, and on that arithmetic rests **RULED (c) — a new session is a refill, not a
penalty**, plus the fork option (b) *flush and hand to a fresh window*.

That ~22% is `~44K tape ÷ 200K`. **If the window is 1M, the cold floor is ~4–5%, not ~22%** — a fresh
window would buy ~95%, the "transaction fee" that makes flushing feel expensive largely evaporates,
and **flushing becomes cheaper than Apollo currently prices it, not dearer.** The JIT programme in
`notes/2026-07-28-memento-jit-context-research.md` is costed against the same denominator: its headline
*"~5–6 points of every window back"* is 5–6 points **of 200K**, i.e. ~1 point of 1M.

**This does not mean the JIT work is wrong** — thinning the chain is right on context-rot grounds
regardless of window size, because rot is absolute-token-driven. **It means the *justification* changes
from budget economics to accuracy economics**, and a programme argued on the wrong axis gets prioritised
wrongly. [[premise-ages-faster-than-rule]]: the premise here is a number nobody has checked since it was
written.

**Three ways forward. Dave's call, and I am not choosing by starting:**

- **(a) Measure first, judge nothing.** Run P1. One Sonnet session. Everything above waits.
- **(b) Measure and re-price in the same window.** P1, then re-run the cold-floor measurement and
  restate the refill arithmetic with the real denominator. Bigger job — this is a re-price of ruled
  process, not a fix.
- **(c) Rule that the band stays relative regardless.** Defensible! A % band is a *throttle on the
  session*, not a *model-accuracy prediction*, and Dave may want it to stay a discipline instrument.
  But then §3's P2 becomes a **deliberate** choice to hold two units apart, inscribed as such —
  not an unexamined inheritance.

---

## §6 — Risks in this note itself

1. **I could not measure the window from inside this session.** Opus 5 receives no context-awareness
   tags — verified in the doc and by direct observation. Everything in §5 is therefore **conditional**,
   and I have tried to keep every "if" visible rather than collapsing to the dramatic branch.
2. **Absence of evidence is doing real work in §2.** "No primary source exists" for the Opus-5/Fable-5
   thresholds means *I searched and found none* — vendor-published per-model degradation curves would
   be unusual to publish, so their absence is expected, not damning. What is damning is **stating them
   to five significant figures anyway.**
3. **The 2603.08274 numbers are open-weight-model numbers.** I have not found an equivalent study on
   Claude 5-family models and should not be read as having done so.
4. **This note is FLOATED.** Nothing here is ruled. P1 is a measurement, not a change; P2–P8 are
   proposals with named costs. **No file outside `notes/` was touched and no commit was made.**
