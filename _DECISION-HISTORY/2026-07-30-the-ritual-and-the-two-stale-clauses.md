# #58 — the ritual, the strata ruling, and two clauses that were teaching retired canon

```
provenance: 383e10dd-42d4-4e5e-8ef1-0dd5ddbeb367 · 2026-07-30
status: ruled — ledger `notes/_MEMENTO-DECISIONS.md` § ★ #58 (D1 strata exemption, Dave in-session;
        D2 behind-pace still unconfirmed; D3 % path forked to him; D4 chain-check UNPROVEN)
```

*2026-07-30 (Thu), Opus conductor + Sonnet subagent. Dave live at the opener, then away.
Step 1b dossier — the WHY and HOW. State lines are in `GOOD-MORNING.md`'s ★ LATEST banner and
`_LIVE-STATE.md`'s ⏱ LATEST delta, same commit (`ef265cb`).*

---

## The shape of the window

#57 ended at a bedtime stop line with the wrap gate red and a handoff that was unusually honest
about its own limits: it had **corrected its own instruction after a read-only probe**, and it said
so in the banner. That correction is the reason this session went cleanly — it named the one
ordering (2f first) that would have filed #56's stratum under a three-sessions-stale batch key with
a green receipt.

It also got one thing wrong inside the same sentence: it instructed minting `## Batch 2026-07-31
#58`. `date` said **2026-07-30**. ★ **A correct instruction is not correct in all its parts**, and
the part that was wrong was the part no gate can see — the gate checks the FORM of a batch key,
never its truth.

## What actually happened, in order

**The boot probe cost the most and produced the least.** `_gen_chain.py --check` exited **1** on the
first call of the session with a **clean tree** — the exact signature of #57's finding, the one
whose remedy had just been wired into the commit seam. Regenerating produced a **byte-identical
file** (`diff` zero lines, `git status` clean), and the check then exited **0** three times running
on that same file. So either `check()` is nondeterministic or the first reading was a cold-mount
artefact. **I could not tell which, and I stopped rather than build a diagnosis on one unreproduced
observation.** It is logged as UNPROVEN in §C·4, not dressed up as a finding — and it matters,
because that check is BLOCKING inside `_git_commit.sh`: a flaky RED blocks every commit and a flaky
GREEN defeats the fix it was built to deliver.

**The EXIT CHECK found nothing missing, which is itself the result.** Every ⚠/⬛/AWAITING item in the
two rolling banners (#55, #56) already had a standing home in §C·4 — the 1b dossier, the archive
CONTENT-probe, ds-021's three homes, the chain-over-warn declaration, the MEMORY.md non-measurement.
**One did not: §C·4 still described the delegation inversion as "FLOATED BY DAVE #56, UNRULED, HIS"
after he ruled it in at #57.** Corrected at source rather than rolled — a wrong status must not
outlive its own correction, and when the queue and canon disagree, the queue is the defect.

**The archive had a hole shaped like a presence.** `_GM-ARCHIVE.md` carried **190 lines of banners
under no batch heading at all**. Minting `## Batch 2026-07-30 #58` at the top and rolling into it —
the obvious move — would have silently annexed every orphan into #58's batch. ★ This is
[[unmatched-grep-is-not-an-absence]] read backwards: **a matched, present, plausible-looking region
is not an accounted-for one.** Marked at the boundary as `⛔ UNBATCHED REGION — provenance
UNDETERMINED`: an `ABSENT`, not a `HOLE`, and explicitly not re-keyed, because the answer is by
CONTENT and that probe is still owed.

## Dave's ruling, and why the shape of it matters

The strata gate could not go green: `STRATA_MAX_BLOCKS = 1` against a floor of **three permanently
unrollable blocks plus the current one**. I put three options to him and did not pick. He ruled:

> *"Exempt #40/#41/#42 by name and keep the cap at 1 for live strata… They're unrollable for a
> recorded reason, so that's a known permanent condition. **Name it, don't bury it in a threshold.**
> … Not raising the cap to 4 — that's a cap at its own floor with no headroom, and #57 skipped 2f
> the night before, which would have taken it straight to 5. And the exemption is a named list of
> three, not a licence to accumulate: if a fourth unrollable block ever turns up, fail loud and come
> back to me."*

He also supplied the precedent himself — `SECTION_EXEMPT`, in the same function, where §A is exempt
by ruling and *"measured and reported, never charged."*

★ **This is the second remedy for a cap set at its own floor, and it is different from the first.**
#53's answer was **derive the cap** from the population it governs. #58's answer is **name the
exceptions** when the floor is a *closed list of known permanent conditions*. Raising the number to
meet the floor is neither — it launders a known defect into a threshold where the next reader cannot
see it. The two remedies are now both on the record, with the test for choosing between them.

## The two stale clauses, and the general lesson

The `GOOD-MORNING.md` header still said the `(45, 60, 63)` percentage band was *"LIVE IN CODE —
price against it"*, six sessions after #56 replaced it with real tokens, and still carried *"behind
pace means MORE WINDOWS"* after Dave contradicted it at #57.

★★ **The header is the one region no roll rule reaches.** 2c/2d/2e/2f all govern regions that change
every session; the header changes rarely, so nothing ever comes back to it. And it is the region
`_gen_chain.py` copies verbatim into `_CHAIN.md` — **read first, at full price, by the reader least
equipped to doubt it.**

⚠ **Both were measured before being called stale.** `BAND_FLOOR/HARD_STOP/MARKED_MAX` are still
defined, `check_preflight` still implements the % path, the selftest at `:2543` still pins the
triple — but the live wrap emits **no band line**, because dispatch keys on the stamp form and the
current stamps are in tokens. ⇒ **DORMANT, not wrong. The PROSE was the defect.** Retiring the code
path is forked to Dave: deleting a pinned ruling of his is not an agent's move.

## The crash

Writing #58's own pre-flight stamp tripped a latent defect and it is the sharpest thing here.
`ABS_TERM_RE`'s number group was `([\d,]+)` — which matches a **bare comma**. My banner mentioned a
term in prose before stating it (*"…no band was written before the job, and that is a LAPSE…"*), the
`job` pattern matched the comma, `_n(",")` raised a bare `ValueError`, and **the entire 39-check
wrap died with a traceback instead of a verdict**.

★★ **A crash is not a fail.** A failing check reports and the run continues. A crashing one reports
nothing about *any* check, and the session cannot distinguish a broken gate from a clean one — the
gate had been green minutes earlier. Fixed by requiring a leading digit (which repairs the
USE-vs-MENTION half for free: `search` walks past a mention with no number after it), plus a
fail-loud named `_n`, plus a fixture of the mention-then-state shape, mutation-tested both arms.
⚠ **Residual declared and NOT fixed:** a mention *followed by a number* would still win. **Scope is
what saves USE vs MENTION; syntax cannot.**

## Delegation, second data point

Per Dave's #57 ruling the strata build went to a Sonnet subagent — no ruling produced, and a gate
plus a mutation test could check it. It came back honest: it flagged that its own first mutation
test *proved nothing* (3 exempt − 1 removed = 2 live, still under a cap of 1) and that it had run
`_gm_move.py --selftest` outside its stated scope. **I replayed the load-bearing claims anyway** —
gate before/after, selftest, both mutation arms — which is the standing rule, and the reason it is
standing is that verification remains the unmeasured half of the fan-out economics.

## What was not done, and why

**No Apollo build-out.** Dave's plan was ritual first, then Apollo with the rest of the window; he
then went to bed. Unsupervised build work would have minted decisions he has to rule while asleep —
progress of the wrong kind, and the opposite of his own test. Declared, not slipped.

**No 1b dossier for #55 or #57.** This file is #58's. The other two remain owed, and the debt is now
compounding rather than merely persisting — which is the argument for paying it before it is three
sessions of reconstruction instead of one.
