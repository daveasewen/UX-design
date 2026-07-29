# Worker receipt — context-degradation verification pass — 2026-07-29

```
provenance: worker-context-degradation · 2026-07-29
status: observed
```

**Lane:** `worker-context-degradation` · **Role: WORKER.** No git — a conductor reconciles and commits.
**Brief:** none. Dave's opener, verbatim: *"I had some very brief research on context windows and how
they work: … I want you to do some of your own research, I want some concrete proposals from this,
you are a worker so leave receipts."*
**Model:** Opus 5 (`claude-opus-5`, per session env). **Stamp:** 2026-07-29.
**Output:** `notes/2026-07-29-context-degradation-research.md` (FLOATED).

**Context gauge at authoring: ⛔ NOT STATED — deliberately, and it is the finding.**
Tape ≈ 70–80K **cl100k-proxy** tokens (own estimate, unmeasured, ±20%). Against the gauge's
`DEFAULT_WINDOW = 200_000` that is ~37% → 🟡 AMBER. Against Anthropic's published 1M window for
Opus 5 that is ~7.5% → 🟢 GREEN. **Three bands apart on the same session.** Per
`knowledge/_RUNBOOK-context-gauge.md` § *"THE FLOOR IS MEASURED, NEVER ASSUMED"* and
[[feedback-measuring-tool-must-not-guess]] (*UNKNOWN never defaulted*), I am declining to name a band
rather than picking one. **This is not the gauge failing to be read — it is the gauge's denominator
being unset.** See P1 in the note.

---

## What was actually done

| Step | Method | Result |
|---|---|---|
| Repo survey | `ls`, `find`, `grep` on `UX-design/` | Found `knowledge/_context_gauge.py`, `knowledge/_RUNBOOK-context-gauge.md`, `MODEL-ROUTING.md`, and **yesterday's** `notes/2026-07-28-memento-jit-context-research.md` |
| Band table | `grep` on the runbook — **read, not recalled** | 🟢 >55% left / 🟡 40–55% / 🔴 <40% left; pre-flight ceiling `fill+job+wrap < 45` |
| Gauge source | `cat knowledge/_context_gauge.py` | `DEFAULT_WINDOW = 200_000`, `DEFAULT_BASELINE = 35_000`, `tiktoken cl100k_base`, `AMBER_AT=0.50 / RED_AT=0.60` |
| Anthropic docs | **`web_fetch`, full page, 3 pages** | context-windows · prompt-caching · refusals-and-fallback |
| Papers | `WebSearch`, abstracts + search summaries only | 2509.21361 · 2603.08274 · Chroma context-rot |

**Fetched in full (highest-confidence tier — these are primary, current, vendor-published):**

- <https://platform.claude.com/docs/en/build-with-claude/context-windows>
- <https://platform.claude.com/docs/en/build-with-claude/prompt-caching>
- <https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback>

**Located via search, abstract-level only (⚠ NOT full-text read — do not quote beyond the abstract):**

- <https://arxiv.org/abs/2509.21361> — MECW, Paulsen, Sep 2025 rev. Apr 2026
- <https://arxiv.org/abs/2603.08274> — Document Q&A hallucination, 172B-token study, Mar 2026
- <https://research.trychroma.com/context-rot> — Hong/Troynikov/Huber, Jul 2025

**Deliberately NOT used as evidence:** every source in Dave's paste that is a YouTube video, Medium
post, Instagram link, Reddit thread, or vendor content-marketing blog. They are cited in the note only
as *the provenance of the unsupported claims*, never as support for anything.

---

## OBSERVED vs INFERRED — the split, stated explicitly

**OBSERVED** (quoted from a page I fetched today, or from a file I read today):

- 1M window on Opus 5 / Opus 4.8–4.6 / Sonnet 5 / Sonnet 4.6 / Fable 5 / Mythos 5; default, no beta header.
- Context-awareness tags go to **Sonnet 5, Sonnet 4.6, Sonnet 4.5, Haiku 4.5**; *"Claude Opus 4.7 and
  later Opus models, Claude Fable 5, and Claude Mythos 5 don't receive these injected tags."*
- Thinking blocks **kept** on Opus 4.5+/Sonnet 4.6+/Fable 5/Mythos 5 and counted as input tokens;
  **stripped** on earlier Opus/Sonnet and **all Haiku**.
- Cache multipliers ×1.25 / ×2 / ×0.1; the full per-model price table (reproduced in the note §1b).
- Min cacheable prompt **512 tk** on Opus 5 / Fable 5 / Mythos 5; 20-block lookback; `effort` change
  invalidates message blocks; mid-conversation `{"role":"system"}` does **not** invalidate on
  Opus 5 / 4.8 / Fable 5 / Mythos 5 (but does on Sonnet 5).
- Refusal = HTTP 200 + `stop_reason: "refusal"`; categories `cyber` / `bio` / `frontier_llm` /
  `reasoning_extraction`; fallback is **opt-in** via `fallbacks` + `server-side-fallback-2026-06-01`
  or SDK middleware.
- `MODEL-ROUTING.md` names **"Opus 4.8 · high"** as the default tier; session env reports
  **`claude-opus-5`**.
- **Direct self-observation:** no `<system_warning>Token usage: …>` or `<budget:token_budget>` tag is
  present anywhere in this session's context. Consistent with the doc's statement about Opus models.

**INFERRED** (reasoning, flagged as such in the note):

- That Cowork's window for this session is 1M. **NOT OBSERVED.** The doc states the *API* default for
  the model; the harness may configure otherwise. This is precisely what P1 tests, and the note says so.
- That the ~22% cold floor would become ~4–5% at 1M. Arithmetic on an unverified premise.
- That `session_info.read_transcript` may omit thinking blocks. **UNTESTED** — named as untested.

**NOT DONE, and worth saying:**

- I did **not** run `_context_gauge.py`, run the capture gate, or run `_build_all.py`. This lane wrote
  two files under `notes/` and touched nothing else.
- I did **not** edit `knowledge/_context_gauge.py`, `_RUNBOOK-context-gauge.md`, or `MODEL-ROUTING.md`.
  All three are named as needing changes; **none is this lane's to make** — P2/P5 move Dave's ratified
  numbers and P3 changes the unit under every historical stamp.
- I did **not** read the arXiv papers in full. Abstract-level confidence only, stamped as such.

---

## ⛔ Fork handed up, not resolved

**The gauge's denominator has never been measured, and Apollo's ruled refill economics are denominated
in it.** Full statement in the note §5, with three named options (measure-only / measure-and-re-price /
rule the band deliberately relative). **I did not choose by starting.** Per
[[feedback-clarify-reflect-back]] the reading above should be confirmed or corrected before anything
in P2–P8 is scoped.

**Cheapest next action, if Dave wants one thing:** P1 — one throwaway **Sonnet 5** session, one tool
call, quote the injected `<system_warning>` line. It returns the true window in about two minutes and
it gates everything else in the note.

## Reconcile note for the conductor

- Two new files, both under `notes/`, both carry `provenance:` + `status:` in a fenced block at the top
  (the field the gate parses — the failure mode `2026-07-28-memento-jit-research-worker` hit).
- Register: research note = `floated`; this receipt = `observed`.
- Per ds-017 an unruled note takes **note + one `_FUTURE-STATE.md` entry, same commit** — the
  `_FUTURE-STATE.md` entry is **NOT written**; it needs the conductor's judgement on where P1 sits
  relative to the JIT programme already logged there, and §C is at cap.
- No GM / `_LIVE-STATE` edit. Nothing ruled.
