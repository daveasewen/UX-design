# Cutting the eager read chain — GM-D7-am retired, and what a door has to be before it counts

provenance: 2026-07-28-33 · 2026-07-28
status: ruled — `GOOD-MORNING.md` § read-chain contract; ledger `knowledge/_DS-IMPROVEMENTS.md` ds-024 (the class); banner ★ LATEST #33

**Spine entry:** `_LIVE-STATE.md` § ⏱ LATEST DELTA #33 · **Worker receipt:**
`notes/_receipts/2026-07-28-a-subdivision-worker.md` · **Brief:**
`notes/_briefs/2026-07-28-a-subdivision-worker-brief.md` · **Predecessor arc:**
`_DECISION-HISTORY/2026-07-28-retrieval-index-staleness-and-the-red-build.md` (#32).

---

## Why this session existed

#32 measured something uncomfortable. The Memento retrieval door worked — 255 records, two-stage
refs → `--fetch` — and it was saving nothing, because the read-chain contract (GM-D7-am) told every
session to read §A, the ★ LATEST banner, §C and all of `_LIVE-STATE.md` *before any question was
asked*. **A door cannot save a token the contract has already spent.** Dave ruled the cut GO
(*"lets do it your way"*), ordered it first, and #33 was that job.

The sharpest thing in #32's finding was not the number. It was this: for eleven sessions,
**"never drop §A" had been read as "always read §A."** Those are two separable decisions. §A is
standing, uncapped, never to be trimmed or shortened to a label — all true, all ruled, and none of
it implies loading 4,208 tokens into every window whether or not anything wants them. Nobody had
separated them because nobody had needed to state them separately.

The irony arrived immediately: to discover that #33's job was to cut the eager read, this session
read `GOOD-MORNING.md` in full — 15,920 tk cl100k / ~24,676 charged — when the header and the
★ LATEST banner alone (~2,500) carried the answer. That is a data point for the ruling, collected by
accident, in the first two minutes.

## Finding 1 — the cut is worth more than it was priced at

Measured before touching anything, in both units (ds-021 discipline — name the unit on every number):

| | cl100k | charged (×1.55) | % of a 200K window |
|---|---|---|---|
| old chain — GM + `_LIVE-STATE` whole | 34,094 | 52,846 | **26.4 pts** |
| new chain — header + ★ LATEST + LS latest delta | **3,410** | 5,286 | **2.6 pts** |
| saving | 30,684 (**90.0%**) | 47,560 | 23.8 pts |

#32's banner had estimated "~3.5K". It was right — worth recording, because the standing rule is to
verify claims against a real run rather than a banner, and this is the case where the banner held.

## Finding 2 — the ruled cut had a hole in it, and it was the one that mattered

The ruling said §A becomes "retrieval-on-demand." Measuring the door showed `--fetch gm:A` returning
**the entire section, 4,208 tk, all or nothing.** §C was already granular (`gm:C1`…`gm:C5`,
84–1,435 tk each) and needed nothing.

So the cut *as ruled* would have moved §A from **paid every window** to **paid in full on the first
§A-shaped question** — "where does X live", "what are the four themes", "what's the build command".
Those are the commonest questions there are. The saving would have been real only for sessions that
asked §A nothing.

**A coarse door is not retrieval.** This is a sibling of the class ds-024 named: an instrument that
technically exists, reports, and delivers nothing to anybody. Here the door technically existed and
resolved the id, and a session paying it would have felt like it was doing retrieval while paying
the eager price.

Forked to Dave, who ruled a divvy: conductor takes the contract and the gate, a worker lane takes
the subdivision.

## Finding 3 — what the worker did, and the judgment call inside it

The lane (Sonnet, fenced to `_gm_usage.py` + `_build_memento_index.py`, no git) delivered 11
subsection records plus a **router** at the legacy `gm:A`.

| path | cost | vs 4,208 before |
|---|---|---|
| "what's the build command" → `gm:A:CMD` | 66 tk | −98% |
| "what are the four themes" → `gm:A:THEMES` | 494 tk | −88% |
| "where does X live" → `gm:A:WHERE` | 754 tk | −82% |
| legacy id → router → child (worst case) | 1,136 tk | −73% |

Children sum **exactly** to the old whole — nothing lost, nothing duplicated.

The backward-compatibility choice was the real judgment. Keeping `gm:A` as full text alongside the
children satisfies "the id still answers" while leaving **the expensive path as the one a searcher
naturally takes** — `gm:A` is the memorable id and it ranks on §A-shaped queries. That re-opens the
hole while looking closed. Deleting it is a retrieval regression, and retrieval regressions cost #32
two sessions. A router is the only shape that answers the question a coarse id can honestly answer —
*which part?* — at ~9% of the payload's price.

A second decision deserves recording: **`GM_A_SUBVOCAB` was kept separate from `GM_VOCAB`.** Adding
11 ids to `GM_VOCAB` would have pulled them into the section-usage testimony contract, which is
`BLOCKING` and demands a line inside `GOOD-MORNING.md` — a file the lane was fenced out of. Retrieval
granularity and testimony granularity are different questions at different costs; conflating them
makes the cheap change pay the expensive one's price. **The consequence is now live and open: the
door is finer than the instrument that measures its use.** `A:R` cannot distinguish "read the build
command" from "read the whole orientation", so the 82–98% saving is invisible to the usage dataset.
That is #34's call, and the ids are already minted.

## Finding 4 — re-pointing an instrument is not re-dialling it, and the difference is governance

M10 measured "the chain" as GM + `_LIVE-STATE` whole. After the cut that is not the chain; it is the
**retrieval surface**. Re-pointing it was enactment. But three things had to be handled deliberately:

**(a) The corpus must still be published.** The cut *deferred* 34K tokens; it did not delete them. A
report showing only the chain would let a 90% cheaper cold start read as a 90% smaller record. The
D7 amendment had already made this argument once about §A ("an exclusion that also hides the total
would understate exactly the cost the measured floor exists to make honest") — the same principle,
one level up.

**(b) The old promotion trigger had to be disarmed, not satisfied.** It said: arm the block once a
wrap measures the chain under 28,000. Re-pointing satisfies that instantly — 3,487 < 28,000 — but
**by redefinition, not by achievement**, and arming a 28,000 block against a 3,487-token chain builds
precisely what ds-024 named: an instrument that can never fire. Disarmed, with the reasoning in the
constant block, and the decision handed to Dave.

**(c) The pin fired, and was right to.** `_capture_gate.py` pins ruled values so a convenience
re-dial has to be a deliberate act. Changing `CHAIN_BUDGET_TK` tripped it. The correct response was
not to update the pin quietly to make the build green — it was to make the pin record **both** the
old ruled numbers and the re-point, marked agent-derived and advisory. Derivation governance: the
engine never derives-and-promotes.

## Finding 5 — three corrections, none of them found by reading the code

This is the seventh consecutive session where the corrections came from a measurement disagreeing
with the author rather than from re-reading the implementation.

1. **Over-coupling.** The first `read_chain_tk` called `split_sections` with the full `unknown_check`
   and refused the whole measurement if any unrelated marker (`C4b`, `STRATA`) was missing. A chain
   that cannot be measured because `C4b` moved is over-coupled — and worse, it routed *every* fixture
   down the UNMEASURED path, where no warn-bite can fail. Found by a bite, not by inspection.
2. **A bite that matched a shared phrase.** The corpus warn's own explanatory prose contains the
   words "read chain". A fat-§A fixture therefore "warned the chain" when the chain had measured
   60 tk. **A bite matching a phrase two different messages share is not a bite.** Both messages now
   lead with a unique `M10` tag.
3. **My own brief was wrong.** It quoted §A as 15,869 B, taken from `--fetch` *output*. The worker
   measured the *record* at 15,817 and flagged the 52-byte disagreement rather than chasing it. The
   52 bytes are the fetch wrapper header. The worker's inference (concurrent prose edits) was wrong;
   its instinct — flag a disagreement between two instruments, do not reconcile it by assumption —
   was exactly right, and the error originated with me.

The positive-bite discipline from #32 paid off directly: reverting `read_chain_tk` to return `None`
in-process was caught **only** by the positive bite. Every failure-only bite passed happily on the
broken version, because an unmeasured chain never warns. The worker independently ran the same proof
on its own suite — four bites red on revert, and the compatibility guard correctly staying green.

## Finding 6 — the EXIT CHECK earned its place, again

Before rolling #31's banner, the 2c EXIT CHECK requires that every ⚠/⬛/AWAITING item in it already
live in a standing section. Grepping §C·4 and DO-FIRST returned **zero** for `ds-021`, `ds-022`,
`ds-023` and `veto`. Those are three ruled-but-unenacted throttle decisions plus Dave's open veto
window, and they existed **only** in the banner about to roll and the banner rolling next. Copied up
first, with `T-D15-for-charts` and M12.

Without the check, three ruled decisions would have begun leaving live state exactly as six of seven
numbered deferrals did on 07-24.

A smaller observation from the same pass: the mover reported §C at 161 lines against **warn 150 /
block 225** and proceeded — *"warn ≠ block"*. Meanwhile GM prose asserts "§C IS AT CAP — an addition
must DISPLACE." **The prose is stricter than its own gate.** That is a documented class, and the
remedy is to measure a cap before paying it rather than performing a displacement the gate never
asked for.

## Resolved state

- Read chain **cut and gated**: 3,487 tk cl100k, contract inscribed in `GOOD-MORNING.md`, runbook
  step 2 amended in the same pass that made its old wording wrong.
- `gm:A` **subdivided**: 11 records + router; worst-case §A question −73%, best case −98%.
- M10 **re-pointed**, corpus published beside the chain, old trigger **disarmed** with reasoning.
- Build **72/72, exit 0**. Capture-gate selftests green, positive bites proven load-bearing.

## Still open

- **The M10 numbers** (chain warn 4,500 / block-candidate 6,000; corpus warn 36,000) — agent-derived,
  advisory, Dave's to rule — and **whether the 28,000 trigger stays disarmed.**
- **Should section-usage testimony follow the door to per-subsection?** The door is now finer than
  the instrument. #34's.
- **#31's three delegated picks** — ds-021 (b), ds-022 (c)+(a), ds-023 — a third session unenacted;
  until they land the gate measures cl100k and every band is directional. Veto window still open.
- **The `{17}`-literal class:** a selftest reporting a pass-count it does not compute. The instance
  was fixed in passing; **siblings were not swept for.** Same family as ds-024.
- **Fourth consecutive projection overrun.** #33's was declared to Dave and ruled a spend before it
  happened, rather than discovered in the post-mortem. That is the bar, not an excuse — the ceiling
  has still never once held, and that is now a four-point dataset for ds-023 (c).
