# #311 lane R — inscribe s311-D3..D9 and revise wave 2 around them

COUNTS: rulings inscribed 7 (s311-D3..s311-D9, store 851 → 858, commit 2fbc8184) · plan page 1 (verified 1440/390, side scroll 0, 6 of 6 calls in Copy as text) · briefs new 3 (J, L, N) · briefs amended 8 (A–H, REVISED header by addition) · WAVE-2-START.md revised by addition · jobs dropped 1 (C2) · lanes deferred to Friday 14 · lanes today 11 (9 Fable, 2 Opus)

Thu 2026-10-01, 11:15–12:00 BST, Fable, the only lane on the seat.

## Job 1 — inscribe
Dave's 11:10 export saved verbatim at `notes/_lanes/311/DAVE-RULINGS-2026-10-01-1110-apollo-for-other-libraries.md` (his chat line after it quoted there too). Seven entries at `notes/_lanes/311/s311-D{3..9}.entry.json`, modelled on `s311-D1.entry.json`; each `--dry-run` passed the reconstruction proof, then `--write`. `gen_kg_titles.py --write` (858 rulings titled, 0 untitled) and `_render_rulings.py` (858 rulings, 169 sessions) re-run. The commit gate regenerated the Memento schematic once; re-run with it appended. Commit `2fbc8184`.

| id | ruled |
|---|---|
| s311-D3 | the snippet is a fixture generated from the spec (reverses ADR-0013 ruling 4, cohort by cohort in phase 2, behind a round-trip gate) |
| s311-D4 | the neutral spec lives in the meta: anatomy, states, emits, bindings |
| s311-D5 | second runtime: Lit custom elements, React and Angular wrappers generated |
| s311-D6 | light DOM, styled by canon.css |
| s311-D7 | S2: an adapter manifest per client library; Apollo governs, theirs renders; unmapped list required |
| s311-D8 | tokens to DTCG 2025.10 now, one generator, extras under $extensions |
| s311-D9 | phases 0, 1 and the S2 schema now; 2 after call 1; 3 and 4 later |

## Job 2 — revise
Page: `notes/_PLAN-311-revised-wave-2-2026-10-01-v1.html` (shell from the Thursday burn plan, localStorage key `plan-311-revised-wave-2-v1`). Verified at the seat with `notes/_lanes/311/R/verify_plan.py`: 1440 side 0, 390 side 0, six calls, Copy as text returns every call; shots under `notes/_lanes/311/R/shots/`. Briefs: `notes/_lanes/312/{J,L,N}/BRIEF.md` new; `{A..H}/BRIEF.md` each with a REVISED section at the top (old text kept); `notes/_lanes/312/WAVE-2-START.md` with a REVISED section above the old § 1–6.

What the rulings changed in the plan: C2 dropped (the renderer is emitter E1, s311-D9); the meta/schema ownership moves from C0→D4 to L (today) → D4 (Friday); B's reworks kept as the fixture's truth, not superseded; C1 kept as emitter E5; three new jobs J (phase 0), L (phase 1, cohort one, review page for Dave), N (S2 schema + Sutherland manifest). The seat rule from the X review is applied: AC + F are the two seat lanes; nine Fable lanes in the cloud on a GitHub clone after a noon push. Fuel: ~6.2M sub tokens, ~10.5% all-models (ending ~93%), ~22.5% Fable (ending ~80%); stop lines 95/90.

## Found, not fixed
- The fuel reading at noon (83% / 58%) is an estimate from the 08:04 panel plus five Fable lanes since; the conductor should read the panel before launching.
- The cloud clones need wave 1 pushed first: nothing from overnight has been pushed (WAVE-2-START § 1). The plan puts the push at 12:00; without it every cloud lane starts from a stale tree.
- J's "one generator" has three readers (`gen_canon_tokens`, `gen_snippet_tokens`, `gen_theme_cascade`); the proposal priced it as one. The brief carries the risk and the fallback (base tokens today, theme resolver owed).
- `knowledge/_tmp/` (E's replay inputs) is not in the GitHub clone; E-replay stages it from the seat.
- 357 dirty paths on the mount from earlier sessions were not staged (explicit-path staging); the list is in the commit transcript.

## Ruling-shaped questions
The five calls on the plan page: the day's shape; cohort one's fifteen parts; deletion in the repo folder for the session; phase 2's start (Saturday run recommended); the first adapter library (Sutherland recommended). Silence by 12:30 takes each recommendation.
