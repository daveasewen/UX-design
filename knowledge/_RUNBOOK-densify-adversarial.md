# Runbook — adversarial densification (lossless context-file compression)

*Stood up 2026-07-19 (Dave: "maybe an adversarial set of agents might sharpen things up" +
"many a mickle macks a muckle" — 10–12%/file across the whole corpus adds up). Sibling to
`_RUNBOOK-context-gauge.md`: the gauge lowers WHEN we hit the ceiling; this lowers the resident
BASELINE so every session starts lighter. Method proven on the `MEMORY.md` index — the adversary
caught 3 real meaning-losses the densifier had introduced.*

---

## The problem it solves

We want files loaded every session (MEMORY.md, GOOD-MORNING.md, _LIVE-STATE.md, runbooks,
guidelines, dossiers) to cost fewer tokens **without losing valuable context**. A single agent
densifying-and-hoping silently drifts meaning ("grows *as byproduct of*" → "grows *via*" changes the
claim). The fix: pit two agents against each other so the fidelity check is active, not trusted.

## The loop (out-of-band — subagents, so churn stays out of the main window)

1. **Snapshot first** — copy the target file to a dated trail (`_retired/<name>-snapshot-YYYY-MM-DD`
   for repo files; a sibling `*-ARCHIVE`/snapshot for memory-store files). Non-destructive is the
   rule; the snapshot is the backtrack. (Repo files also have git as a trail; memory-store files do
   NOT — they need an explicit copy.)
2. **Densifier** (Sonnet/Haiku): rewrite as tight as possible, ZERO information loss. Hard rules:
   preserve every link/filename, identifier (R-D*, T-D*, ADR-*, hex, counts, dates), proper noun,
   distinctive recall-keyword, and status/polarity word (RULE/OPEN/CLOSED/RULED/PARKED/✅/⛔).
   Cut only filler, hedges, redundant restatement; swap phrases for the one precise word that carries
   them; use → · ≠ = symbols. Same information, fewer words — never summarize away nuance.
3. **Adversary/auditor** (Sonnet, ideally a different instance): given ORIGINAL + DENSIFIED, hunt
   every dropped fact, weakened word, and MISREAD risk — special attention to `+`/`·` that blur a
   list boundary or fuse two items. Output LOSSES · DISTORTIONS · VERDICT (PASS / PASS-WITH-FIXES /
   FAIL) · WORTH-IT judgement.
4. **Reconcile** (main agent): apply the adversary's fixes, then write the file. If FAIL, loop 2.

## When it's worth it — the prose-heaviness rule

Payoff scales with how much filler a file carries:

- **Already-terse files (indexes, token tables): DON'T reword — PRUNE.** On `MEMORY.md` the reword
  saved only ~10–12%, all from stripping articles, and *introduced* 3 meaning-losses: a bad trade.
  The real lever there was relocating historical/closed entries to a not-auto-loaded archive.
- **Prose-heavy files (runbooks, GOOD-MORNING §A, dossiers, guidelines): DO densify.** More filler to
  cut, fewer load-bearing single tokens, so the same 10–12% is both safer and higher-yield — and it
  compounds across the corpus (the "muckle"). Densify to *precise prose*, not bullet-shorthand, so a
  dossier's reasoning arc and narrative voice survive (density ≠ summarization; see
  `feedback-adversarial-densify`).

## Guardrails

- **Never touch link text / filenames** — they're recall targets and cross-refs.
- **Two operations, don't conflate:** densification = same info, fewer words (safe everywhere);
  summarization = dropping steps/dead-ends (forbidden in dossiers, the why lives there).
- **The adversary is the gate.** No densified file lands without a PASS or applied PASS-WITH-FIXES.

## Entry points

`_RUNBOOK-context-gauge.md` (the WHEN sibling) · `_RUNBOOK-capture-ritual.md` · memory
`feedback-adversarial-densify` · `spin-off-candidates` (generalise as a reusable "lossless-compress
with fidelity gate" tool).
