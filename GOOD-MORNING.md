# Good morning, Dave ☕

*Session briefing — written end of 2026-07-05, session "§9 worked spread — SME Payments register
run + Opus re-test." Third execution session of the seaworthiness sequence. **Read this, then
`_LIVE-STATE.md`, then `knowledge/_fitness-test/register-spread-2026-07-05-opus/_COMPARISON-sonnet-vs-opus.md`.***

## The session in one line

Ran the first §9 worked spread, you reviewed the actual HTML and found two real gaps (not just
polish), I fixed one concretely and re-ran the whole spread on Opus to test the other — both moved
in the right direction, verified against the files themselves, not agent self-reports.

## What landed this session

- **First spread (Sonnet).** Isolated 3-band generation on SME Payments. Cardinal curbs held, but
  **you caught two real problems on eyeball review**: sober used a plain, never-reviewed canon
  utility instead of the purpose-built, gate-reviewed `.cn-account-card` for the same data; and
  expressive wasn't bold enough. You also asked whether a build→review→correct loop exists (it
  doesn't) and floated testing Opus.
- **Root-caused finding 1 precisely.** Canon.css already encodes a real rigour hierarchy through
  naming alone — `.cn-*` = auto-generated from gate-reviewed reference snippets; `.c-*` = a
  hand-authored, never-reviewed utility layer. The brief never said "prefer the reviewed one." Fixed:
  `_TEST-BRIEF-v2-sme-payments.md` §2 now states this as a mechanical rule, not an adjective.
- **Re-ran the full 3-band spread on Opus** (your call: "full 3-band spread, Opus"), same fixed
  contract, same isolation discipline (cold passes, no visibility into siblings or the earlier
  Sonnet run). **Verified against the files:** all three bands now retrieve `.cn-account-card`;
  sober dropped to **zero** never-reviewed-utility usage (from relying on it before). Expressive
  reads as a much bigger swing in its own report ("the reckoning wall" — full-bleed bands, 76px
  hero figure, red slab as deliberate centre of gravity) — **this needs your eyeball, not my grep.**
  Cardinal curbs held with zero violations on both models throughout.
- **Bonus catch:** two independent Opus passes flagged the same real ambiguity in the contract's
  §3 wording (it conflated "sum of all 5 rows" with "scheduled total") — neither Sonnet pass caught
  it. Fixed in the contract.
- **Full writeups:** `register-spread-2026-07-05/_PROBE-and-selfcheck.md` (first pass) +
  `register-spread-2026-07-05-opus/_COMPARISON-sonnet-vs-opus.md` (the re-run + comparison table).
  `_LIVE-STATE.md` + memory (`register-inference-ramp`, new `spread-review-gaps-2026-07-05`) both
  updated with the honest verdict: **promising, still not proven** — one screen, two variables
  changed at once this round, no rendered visual check yet.

## On your desk

- **Please open both sets of HTML files** — `register-spread-2026-07-05/` (Sonnet) and
  `register-spread-2026-07-05-opus/` (Opus), especially the two `expressive.html` files
  side-by-side. That's the actual test of "is Opus better for this kind of judgment work" — I can't
  see it, only describe what the files claim.
- Everything committed this session, ready to push via GitHub Desktop.

## Queue next (fresh session, or continue now)

1. **Your verdict on the Opus comparison** decides a lot: if Opus genuinely reads better here,
   that's the first real evidence (not just an a priori assumption) for reserving Opus for
   judgment-heavy generation per `model-selection-by-phase`.
2. **A designed build→review→correct loop is still an open question** — worth its own test once
   the model question settles, separate from just picking a better model.
3. Ingestion Phase 1 (Sutherland migration) still queued whenever you want to bank it — deferred
   again this session, not cancelled.
4. Off critical path unless you say: D2 novel-screen (waiting on colleague), toolkit tranche 2,
   harness-modes exploration, TOV spin-off, ADR-0004 ops follow-ups.

> Next-session opener: **"Title this chat: <pick one>."** Read GOOD-MORNING → `_LIVE-STATE.md` →
> the comparison writeup if continuing the §9 thread; → `_SEAWORTHINESS-PLAN_2026-07-05.md` if
> starting Phase 1.
