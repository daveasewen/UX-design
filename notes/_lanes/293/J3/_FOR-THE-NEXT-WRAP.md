# Lane J3 landed after the #293 wrap — pick this up

provenance: 293 (Jev side-quest seat, conductor Fable 5.1) · 2026-09-21

The #293 wrap (`fa735458`) committed lanes J and J2 — `knowledge/_jev.py`, `knowledge/_jev-receipts.jsonl`
(2 lines at that point), the J brief and both subreports. **Lane J3 finished afterwards and is UNTRACKED:**

- `notes/_lanes/293/J3/` — two fixtures, the exact question JSON as sent, `probe-results.md`, this file
- `notes/_subreports/2026-09-21-293-J3-jev-probe.md`
- `knowledge/_jev-receipts.jsonl` — now **5 lines** (3 appended by J3); the tracked copy has 2

Name them in the commit body; do not sweep silently. `.env.local` holds the key, is gitignored
(`.gitignore:71`), and must stay out.

## Dave's words on this thread, verbatim

> quick side quest can you do some research around integrating jev into our projects and how we might do it from cowork

> so would this be an integrating with jev or a way to improve what we have already? obviously it wouldn't work for anyone who doesn't have the api

> so i need the api, i have an invite so that shouldn't be a problem

> install *(the `typesafe-ai` skill — now in his account skills, MIT, vendored verbatim plus one Apollo line)*

> okay, ill be guided by you

## What J3 measured (n=3, one source document)

P (poster as shipped) Score 2.99 conf 0.99 · M (one badge removed) 2.92 / 0.92 · N (no badges) 1.66 / 0.34.
Noul "claims something unbuilt" 0.13 → 0.21 → 0.89. **P > M failed** — cause is `html_to_state`
feeding Jev the page's prose ("two are faded and badged") not its render. Latency 579–621 ms; all
five calls to date exceed TypeSafe's declared 70–500 ms.

## Ruling-shaped questions — QUESTIONS PUT, nothing inscribed

1. Track `knowledge/_jev-receipts.jsonl` in git (no secrets) — and under what rotation rule?
2. Jev is dev-time instrument only, never a blocking dependency (his stated concern: no API, no Apollo change). Confirm as a ruling?
3. Next experiment, agreed in chat as the guided path: Memento re-rank on a known-answer fixture (ds-021 / #80 / #81 misses). **Fixture queries must come from Dave or real transcripts** or the test grades itself.
