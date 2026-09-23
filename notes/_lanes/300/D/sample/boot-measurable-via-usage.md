---
name: boot-measurable-via-usage
description: "★★★ BOOT AND FILL ARE DIRECTLY MEASURABLE in real tokens via message.usage — proven 07-31; current constant lives in _gauge_tokens.py (s171-D1), never in this hook"
metadata: 
  node_type: memory
  type: project
  provenance: local_cfa295ea-b60e-46f9-9918-13bcccab96c6 · 2026-08-02
  status: observed
  originSessionId: 7a750225-872a-4082-8720-a37313692f24
  modified: 2026-08-15T07:53:56.001Z
sources: [cowork-import]
imported_at: 2026-09-16T03:13:39Z
---

**THE ROUTE.** Every `assistant` record in the session transcript carries `message.usage`.
`input_tokens + cache_creation_input_tokens + cache_read_input_tokens` = Anthropic's own
real-tokenizer count of what was actually sent for that call. ⇒ **FIRST assistant turn = BOOT.
LAST assistant turn = LIVE FILL.** Real tokens — no cl100k proxy, no `×1.559` conversion, directly
comparable to the ruled 160K/200K/256K bands. Proven in
`notes/_briefs/2026-07-31-compaction-and-fill-research.md`; re-run live 2026-08-02.

★★ **"COWORK BOOT IS UNMEASURABLE FROM INSIDE" IS FALSE.** That sentence rode every pre-flight
stratum from #63 on. **Five readings: 61,582 (#58b) · 61,775 (RULED #60-D3) · 61,812 (#59) ·
61,582 (brief) · 61,854 (measured live from inside a Cowork window, 2026-08-02) — spread 272
across two harnesses.** #68/#69's `boot 10,000 est` was not conservative, it was **out by 6×**,
and both published totals on it (`168,000 of 200,000 — AMBER` is **219,775** on the ruled constant).

⛔ **PROVEN ≠ ENACTED, and this is the live gap.** Probes, named, all empty:
`grep "usage\|input_tokens\|cache_read" knowledge/_checkin.py` → **0** — *the instrument already
opens the file holding the answer and never reads the field* · `grep -rln
"total_input_tokens\|cache_read_input_tokens" knowledge/*.py` → **0, nowhere in code** · no ledger
row, runbook line or ADR cited the brief. **Four sessions after the proof got WORSE, not better**
(#68/#69 substituted a guess, #72–#75 gave up with `⛔ NOT CAPTURED`). The brief's own §357 ends
*"Dave should rule which claim he needs"* — **that question never reached him.**

⬛ **DAVE'S, STILL UNRULED: which claim is `ds-025` item 1 about?** The **TOTAL** is measured and
closeable. The **harness-only decomposition** (system prompt vs tool schemas vs `MEMORY.md`,
isolated) stays unobservable — `usage` gives the call's sum, not a breakdown; it needs a second
data point to subtract. Two different claims, one code.

⚠ **NEVER compare this to `_checkin.py`'s figure.** That reads cl100k **THROUGHPUT, cumulative** —
a different object, over-counting real tokens by ~1.28×. See [[measure-dont-convert-units]].

Ledger: `notes/_MEMENTO-DECISIONS.md` § ★★ DREAM PASS 4 (2026-08-02) + its correction.
Related: [[gauge-absolute-tokens-ruled]] · [[tape-unit-is-not-real-tokens]] ·
[[feedback-context-gauge]] · [[premise-ages-faster-than-rule]] · [[instrument-without-a-consumer]]


