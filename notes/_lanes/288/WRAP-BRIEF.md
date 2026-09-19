# #288 wrap brief — cut by the conductor (Fable 5.1) at the stop line, 2026-09-19

provenance: 288 · 2026-09-19
status: brief (every figure here is DECLARED; the wrap seat re-measures and publishes both readings where they differ)

## The session in one line

Wave 1 (four Opus lanes) landed the strand map, the four-theme gutter sheet, the s219-D3 generation arm and the template quality review; then Dave challenged the premise on seeing the template ("this isn't Apollo its a dot-to-dot book"), a fifth lane ran the composition probe with the template fenced off, and he ruled by eye that it composes — "at least it's diverged from the template" — and named the defect class: sloppiness = alignment, spacing and dimensions.

## Dave's words

ALL in `notes/_lanes/288/DAVE-RULINGS-2026-09-19.md` — quote, never paraphrase. Conductor's readings are marked as the conductor's in that file; keep them marked.

## Lanes — all `Agent`, depth 1, model opus, NONE in seat

| lane | job | report | row | sub tokens (declared from the harness) |
|---|---|---|---|---|
| M | strand map page `notes/_STRAND-MAP-2026-09-19.html` | `notes/_subreports/2026-09-19-288-M-strand-map.md` | W-288m | 162,304 |
| B | four-theme gutter sheet `notes/_lanes/288/B/four-themes.html` (read-only; read HEAD via `git show`) | `…-288-B-bento-renders.md` | W-288b | 177,908 |
| A | s219-D3 arm: new `knowledge/canon/gen_bento_role_vars.py`, canon.css regenerated, snippet literals → vars, meta `$awaitingDave` 3→5 by addition | `…-288-A-s219-d3-arm.md` | W-288a | 174,021 |
| T | template quality review `notes/_lanes/288/T/template-quality-review.html`, 6-question decision pack | `…-288-T-template-quality.md` | W-288t | 190,369 |
| P | composition probe `notes/_lanes/288/P/{probe-sheet.html,composed-dashboard.html,DECISIONS.md,READS.log}` — 39 reads, 0 fenced | `…-288-P-composition-probe.md` | W-288p | 299,493 |

Declared subs total 1,004,095 (n=5), the harness's per-agent figure. Publish `_checkin.read_fill` alongside — two definitions, both published (the #287 form).

## Gauge, declared

Conductor transcript `f0d5834b-1313-45d3-9961-2f10be3c3817.jsonl`. Seam at the wrap call: FILL 180,585 real / 27 turns, 585 past the 180,000 stop line, tolerated to 220,000. Boot 74,174 real, n=3 on the Browser-blocked setup (#286 73,832 · #287 74,120 · #288 74,174) — still over the 70,000 ceiling, SHRINK-ONLY, not a re-base. Six inherited structural gate fails at the open (#243 form, 14th wrap). One day, no date split expected — read `date` at the seat.

## Declared by lanes, to carry forward verbatim

- Lane A ran `git stash push` (no entry created, tree verified intact) — a git write against the standing rule, declared by the lane.
- `knowledge/_render/seat_env.sh:44` globs a path playwright 1.63 no longer ships; lane B symlinked around it, lane T could not render. One-line fix owed; not done.
- Lane P: `_validate_screen.py` wrote a stray `knowledge/_screen-gate/composed-dashboard.md` — moved by the conductor to `_to_delete/288-P-stray/` (mv, not rm). `_COMPOSE-AUDIT.md` restored to HEAD by the lane.
- Discrepancy published, not reconciled: `$awaitingDave` count — handoff #138 says 4, lanes M and T read 3 at HEAD, lane A's additions make it 5.
- The frozen demo prompt is NOT recoverable from the record (lane P searched memento + briefs + repo); the probe used a fallback brief — the two probe pages answer different briefs.
- Inherited uncommitted at open: `notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl`, `notes/_lanes/287/DAVE-RULINGS-2026-09-19.md` (+6 lines appended after #287's commit — the wrong-order class, third session).

## Ruling-shaped, NOT inscribed (rulings stay 622 unless his word says "inscribe" — it did not)

1. Apollo composes, not traces — his verdict by eye on the probe sheet. What the one-shot generates FROM (the #230 "zero invented markup" pass condition rewards tracing).
2. The sloppiness class: alignment, spacing, dimensions. He writes the test brief himself ("I'll create a test brief for these tests") — owed by Dave.
3. The outer gutter: token 0/24/24/0 vs role default 40/24/40/24 (lanes A, B). Not ruled. The arm delivers from the rails manifest (40/24/40/24). Inner gutter has three answers (canon 1px, subSpacing 4/4/4/2, template 4). Supercharge's 0 is inherited, never decided.
4. Specificity root cause (lane P, measured): `.c-bento.wall-ops{--bento-gutter}` (0,2,0) loses to `.c-bento[data-bento-role="dashboard"]:has(…)` (0,4,0) — canon's own instance-dial recipe silently loses for the dashboard role.
5. Which Friday the 25th is — small internal demo or Rice. Not established.
6. The deck's new structure — his, not yet given. Wave 2 blocked on it.
7. Swiss design skill as an Apollo taste guarantee — PARKED by his word, "don't let me forget this" (memory `swiss-skill-as-apollo-taste-guarantee-288.md`).
8. Lane T's six-question decision pack (inline-style rule with 87 raw values re-measured, template status and index.json's fixed status list, the three `$awaitingDave`, a max-width ruling) — unanswered.
9. Showroom re-sync after the arm (showroom still shows the pinned 40/4); dashboard freshness check; the deck's stale graph figures (2,837 on slide vs 4,820 today); the one-shot's quality dark since 2026-09-02.
10. Everything on `_HANDOFF-130`…`-138` not closed today. Strike NOTHING without a receipt. Nothing closed today that I can receipt except: the s219-D3 arm is BUILT (lane A, gates green, four-theme proof) — the "never built" clause of #138 move 2 is discharged; the ruling on Mono's value is not.

## Ritual

Run `knowledge/_RUNBOOK-capture-ritual.md` in full, every step in order, as #287's W2 did (`notes/_subreports/2026-09-19-287-W2-wrap.md` is the model). Handoff `_HANDOFF-139-<slug>.md` outranks `_CHAIN.md` and does not replace #130–#138. Commit via `SESSION_N=288 knowledge/_git_commit.sh` (a lane, `mv` never `rm` for locks — `_to_delete/_stale_locks/`); push; CI read polled to completion, verdict verbatim. Memory hook written FIRST at `notes/_lanes/288/WRAP-MEMORY-HOOK.md` then placed; MEMORY-ARCHIVE is at 48,990 of 49,152 B — declare, never truncate. Next title via `python3 knowledge/_gen_titles.py --session 288`. Never run gen_kg_rules.py, land_rests_on.py, gen_kg_icons.py or `_build_all.py`. 2g last.
