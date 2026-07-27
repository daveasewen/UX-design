# 2026-07-27 — Supersession by addition: why GOOD-MORNING kept outgrowing its own trims

provenance: local_1ffa04b1-ec26-4dd2-ab19-8c1d8e94167d · 2026-07-27
status: observed
*Session: "GM compaction architecture" (Fable solo). Spine: `_LIVE-STATE.md` ⏱ LATEST 2026-07-27 #13.
Ledger: `notes/_MEMENTO-DECISIONS.md` § GM growth-contracts ruling (GM-D1…D9). Proposal:
`notes/_briefs/2026-07-27-gm-compaction-architecture-proposal-v1.md`.*

## The arc

**The brief arrived pre-measured** (an Opus fresh-window analysis: 81.8KB/840 lines, DO-FIRST 27%,
§C·5 Parked 110 lines, chain ~21% of a window) with a hypothesis: 2c/2d roll banners and deltas,
nothing rolls DO-FIRST or the queue. Dave's steer on top: *"there is a structural problem here I
think, not just a problem with the handoff doc."* He was right, twice over.

**Finding 1 — the numbers were already stale, and that WAS the evidence.** By measurement time GM
was 90.2KB/910 lines: +70 lines in about a day. Attribution: DO-FIRST +27, the §C tail +~43 —
**~97% of growth in exactly the two regions with no roll rule.** The growth-rate claim proved
itself between the brief being written and being executed.

**Finding 2 — the brief indicted the wrong organ in §C.** "Parked (110 lines)" is innocent: the
true Parked list is 3 stable lines. What grows beneath its heading is an unlabelled
**pre-flight/post-mortem/COMMIT-STATE stratum stack** — sessions #12/#8/#7/#6 all present, two
blocks hand-marked *"[SUPERSEDED — kept for the record]"*. The author felt the pressure to roll;
no rule licensed the move. Diagnosis before this read would have written a roll rule for the
wrong section.

**Finding 3 — the disease has a name: supersession by addition.** Move-discipline (rolls are
verbatim moves, never rewrites) without a WHEN rule means the only legal way to kill text is to
pile a "⛔ SUPERSEDED — stop reading the below" notice on top of it. DO-FIRST carried a #10
stratum, a 40-line #11 spec its own #12 header declared HISTORY, and #12 notices negating both —
dead text and its warning label both billing full price every cold read. The 2c/2d pattern
(cap + archive sibling + verbatim move + EXIT CHECK) was proven twice on banners and deltas;
it had simply never been extended to the other stratum-generators. Hence the architecture:
**every section declares a growth contract — content type · cap · roll target · retirement test —
gate-enforced; §A alone standing and uncapped.**

**Finding 4 — Dave's reframe fixed the gauge decision before it was written.** The draft intent
was "re-price bands against the ~24% cold-start floor." His push-back: the floor is *measured
against the current GM+LIVE-STATE, which this work shrinks*. So a snapshot constant in canon would
be falsified by its own enactment — the prose-drift class (gate advice text aging while the exit
code doesn't). GM-D9 therefore rules the **mechanism** (floor measured per session, bands on
remaining budget, band table inscribed once) and leaves the numbers to the gauge canon.

## Calls worth remembering

- **The retirement test that unlocked D2:** a supersession notice is a warning label — it may not
  outlive the thing it warns about, and must not die before it. Lifetime = target's lifetime, one
  batch, one move. And its corollary: **a tombstone that must live forever is evidence a gate is
  missing** (gate-don't-patch applied to the record itself).
- **Deviation, licensed:** the brief said Read four files (~42K tk — the failure under diagnosis);
  probes + targeted slices were used instead, flagged to Dave first. §A was located, never read in
  full, never touched.
- **Deliverable exception, ruled:** markdown + rule-by-number in chat instead of the standing
  review-HTML rule — textual options, nothing visual to specimen. A narrow exception, not precedent.

## Resolved / open

**Ruled:** GM-D1…D9, all as recommended (ledger). **Open:** enactment (brief in `notes/_briefs/`,
its own window, ~30–40%) · `_LIVE-STATE` 2d-tightening (deliberately separate ruling) · band
numbers (Dave's, in the gauge canon pass) · MEMORY.md compaction (pre-existing, still its own window).
