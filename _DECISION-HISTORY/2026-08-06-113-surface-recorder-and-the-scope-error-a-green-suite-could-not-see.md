# #113 — The conductor-surface recorder, and the scope error a green suite could not see

provenance: #113 · 2026-08-06
status: observed

## The arc

**1 · The ruling that had survived four sessions.** #112-D1 (Dave) was blunt: build the recorder
first, inside the attribution lane, never as a competing option — *"otherwise #112 measures one
number and #113 is blind again — that is the #109 defect a third time."* It had already failed three
ways. #109 measured the boot floor and did not write the samples down next to the constant. #110
measured a **sub's** injected surface and called it the conductor's. #111 named the remedy in its own
post-mortem and did not build it. #112 ruled it and spent the budget on a compaction overrun. Dave
opened #113 with the order, not a menu: *"lets get these done in order, lets go for it, forget apollo
work for now"* — recorder, then attribution, then harness (conditional), then housework, with the
Apollo design-system enact queue explicitly PARKED.

**2 · What got built, and why each refusal is in it.** `knowledge/_surface_recorder.py` plus its store
`knowledge/_surface-samples.json`. It records the conductor's own boot-surface decomposition in real
tokens; it **hashes** every component so an unchanged one is recognised next session rather than
re-measured; and it diffs consecutive sessions into **ATTRIBUTED vs UNATTRIBUTED delta** — which is
exactly the quantity Dave ruled unsafe at #111-D3 (*"The 9,308 drop has NOT been attributed to the
residual. It has been assumed to be."*). The asymmetry this repo already runs on is built in rather
than documented: a **SILENT** gap refuses, a **DECLARED** gap passes, and a figure carried forward
without a hash match is recorded **UNVERIFIED** — never silently promoted to measured. Receipts:
`python3 knowledge/_surface_recorder.py selftest` → ALL GREEN, 19 tests; six mutations, each killing a
distinct clause. M1 (drop the silent-gap refusal) kills T2 and **not** T3 — which is the point worth
keeping: detection and discharge are separate clauses, and a single mutation proving "the gap check
matters" would not have shown that. Declared honestly rather than smoothed: M4's `sed` matched **both**
`raise CaptureRefused(` sites, so that mutation was compound, not minimal.

**3 · Finding 1 — `MEMORY.md` is in the sandbox mount, and has been all along.** It sits at
`/sessions/<session>/mnt/.auto-memory/`, a **hidden** directory that every `ls` for ~113 sessions
missed. Three sessions had already measured it the expensive way — by READING it into context —
at **8,470** (#109), **9,178** (#111) and **7,996** (#112) real tokens of fill, for a number `bash`
produces at zero. The general form is worth more than the file: **anything on disk stages at zero
fill; reading it in order to measure it IS the fill.** Two adjacent facts were re-checked rather than
inherited: `CLAUDE.md` is still **not** in the mount (`find -iname`, zero hits — #110's finding holds),
and `AGENTS.md` **is**, at repo root.

**4 · Finding 2 — the recorder shipped with a scope error its own green suite could not see.**
`_CHAIN.md` is **ADDITIVE**: it lands at turn 2, on top of boot, not inside it. The first build netted
it **off** the boot total, which understated the residual by **11,345**. At the moment that code was
declared correct the suite was 19 tests green with five mutations killing five clauses. None of them
could fail, because **synthetic fixtures have no scope** — every fixture was internally consistent
with whichever sign the code used, so no test could express the defect. It was caught by driving the
thing on real data, which is the same lesson #104 paid for
(`mutation-tests-the-clause-not-the-feature`) arriving from a new direction: a mutation test proves
the clause you mutated is load-bearing, never that the feature is right. Fixed with an explicit
`ADDITIVE` set, a `boot_measured_tk` / `additive_tk` / `floor_tk` split, a new T11, and M6 confirming
the split is load-bearing.

**5 · The first real sample, and the three stale constants.** Boot first-turn **54,038 real** — the
fourth consecutive post-break low (62,462 · 55,733 · 55,025 · 54,038). `memory_md` **8,188** in-boot.
`chain_md` **11,345**, ADDITIVE. Floor **65,383**. **45,850 unattributed BY SUBTRACTION**, with five
components declared-not-measured (`deferred_tools`, `mcp_blocks`, `skill_catalog`, `agent_types`,
`system_prompt`), each carrying its prior figure and a price so the next session can stage them rather
than rediscover them. Against that, three published constants are measurably stale:
`BOOT_FIRSTTURN_TK` 65,400 → 54,038 (−11,362); the floor 75,899 → 65,383 (−10,516); and the
`_gauge_tokens.py` comment-block chain line 10,499 → 11,345 (**+846**). **None was changed.** #111-D2
stands — *"Don't fit a constant across a structural break"* — and the series is still descending, so
this is drift in progress, not a new plateau. The conductor's read, stated as a read and not a ruling:
don't re-base the first two; **the third is a different animal** — it is growth, not a break, and what
it actually means is that the **P4 `_CHAIN.md` trim target GREW.**

**6 · What held the line, and it was not restraint.** #111 blew the stop line by 5,223 and #112 blew
it by 10,680 the same way, with #111's post-mortem freshly read. The remedy inscribed after #112 was
narrow and mechanical: any lane priced above ~15K gets a check-in **inside** it, and an exceeded
estimate means STOP and re-price rather than finish the lane. #113 ran exactly one mid-lane check-in,
at **FILL 117,731** against the **150,929** stop line, and the re-price it forced is why attribution,
harness and housework were rolled instead of ridden. The line held. The finding is that the throttle
worked because it fired in the middle of the work, not at either end of it.

## Where it stands

- **CLOSED:** #112-D1. The recorder exists, is driven, is tested, and its store holds a real sample.
- **OPEN, Dave's:** all three constants above. Put to him, ruled by nobody.
- **OPEN, unanswered:** the figure **2,460** quoted in the housework framing has no source anywhere in
  the repo — nearest are 2,388 (UUID tool-name prefixes) and 2,646 (five departed MCP servers). Asked
  at #113, not answered. It must not be mapped onto either.
- **ROLLED to #114:** the attribution re-probe, staging `deferred_tools` first because it holds the
  2,388 real of UUID-prefix waste; harness/P2 only if attribution says there is something to pull (the
  named candidates measure 836 real, ≈1.1% of the floor — the live untested hypothesis is
  **duplication**, `computer-use` and `chrome` guidance each injected twice); the 19
  `_state.LEGACY_IDS` and DO-FIRST item 22; the P4 chain trim at its new size of 11,345; and the
  Apollo enact queue, parked by Dave rather than dropped.

Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #113 · Ledger: `notes/_MEMENTO-DECISIONS.md` § ★ #113 ·
Banner: `GOOD-MORNING.md` ★ LATEST #113 · Measurements: `notes/_GAUGE-LOG.md` (boot #113) and
`knowledge/_surface-samples.json`.
