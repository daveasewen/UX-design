# Memento dream pass — proposals, 2026-07-28

provenance: local_68fe4195-5a0e-4adb-b308-6b30c789ee90 · 2026-07-28
status: floated

*Third pass. Cold Opus dreamer, Shape A (Cowork), per `.claude/agents/dreamer.md`. **Proposes only** —
nothing here self-promotes; promotion is Dave's alone (derivation-governance). Ranked by prevalence,
highest first. The do-not-re-float list supplied with the dispatch (every RULED ledger row + both
prior passes' checked-clear items) was honoured; nothing below re-opens ruled ground.*

*Three of the six proposals sit on the hunt lines Dave added to the spec three hours before this pass
(#21, `notes/_MEMENTO-DECISIONS.md` § DREAMER HUNT LIST +3): P1 is price-vs-actual drift, P2 and P3 are
the claimed-ENACTED-vs-RUN class. The lane-order hunt found nothing — see Method.*

---

### P1 — The price-vs-actual dataset cannot falsify a price: its "closed" column is a self-reported estimate written by the same agent that set the price, and in the one session where the divergence is large the record says "on plan" while the session told Dave it closed at the RED edge

- EVIDENCE:
  - **The material case, session #18 (2026-07-27, Opus solo, M-set enactment).** The record says
    **52%** in three places: `notes/_GAUGE-LOG.md:114` — *"Closed 🟡 ~52% ESTIMATE, reserve untouched"* ·
    `_GM-ARCHIVE.md:50` — *"Context gauge at authoring: 🟡 ~52% (ESTIMATE)"* · `_GM-ARCHIVE.md:61`
    (the #18 banner headline) — *"🟡 ~52% at wrap"*. The session's own closing message to Dave, sent
    **after** the commit it reports (`e53afc4`), says: *"**Gauge at close: 🟡 ~62%, RED edge (estimate)**
    — reserve untouched"* (transcript `local_9ecbcf40-1760-4a5a-9703-f8d2a34c8de9`, final wrap message).
    **52 is also exactly the pre-flight arithmetic** — `_GAUGE-LOG.md:108`, *"fill 24% + job 20% +
    wrap 8% = 52% AMBER"*. So the block reads as a perfect landing (no overrun recorded) for a window
    the author described in chat as ten points higher and at the RED edge.
  - **The pattern, smaller.** #15: log `:76` *"Closed 🟡 ~55% ESTIMATE"* vs transcript
    (`local_e79e89ee`) *"Closed 🟡 ~57%"*. #17: log `:101` *"Closed 🟡 ~60% ESTIMATE"* vs transcript
    (`local_1564cbbc`) *"closed honestly: 🟡 ~61%"*. #20: log `:123` *"Closed 🟡 ~55–58% ESTIMATE"* vs
    transcript (`local_13f9ebbd`) *"Closed 🟡 ~58–60%"*. Matches: #16 (log `:89` ~63% = transcript
    ~63%) and #12 (log `:47` ~72% RED = transcript *"Stamped 🔴 RED ~72%"*).
  - **The dataset also has an unexplained hole.** `notes/_GAUGE-LOG.md` runs #6 · #7 · #8 · #12 · #13 ·
    #15 · #16 · #17 · #18 · #20. **#14 is absent and unflagged** — the window that enacted GM-D5(a)'s
    own step 2f (`113eefc`), so 2f was in force for it. #19's absence *is* flagged (`:119`, *"⚠ #19
    wrote no stratum"*); #14's is not.
  - Every closed band since #15 carries the word **ESTIMATE** in the record itself, so the "actual"
    half of price-vs-actual is not a measurement at all.
- PREVALENCE: 4 of 6 sessions where both numbers exist diverge (#15, #17, #18, #20); 3 are within
  rounding, 1 is 10 points and inverts the entry's meaning. 10 blocks in the log, 2 sessions missing
  (1 flagged, 1 not). Dataset checked in full (`notes/_GAUGE-LOG.md`, 126 lines).
- PROPOSED: two reversible lines, both in `knowledge/_RUNBOOK-capture-ritual.md` step 2f, plus one
  append to `notes/_GAUGE-LOG.md`. (a) **The closed band is written to the record FIRST and the chat
  message quotes it** — one number, one source; today the chat re-estimates and nothing reconciles
  the two. (b) **A missing stratum is logged as a hole**, the way #19's was, so the dataset's gaps are
  visible to the next reader rather than silent. (c) **Append** (never rewrite — the #19 116-tk
  precedent) a correction line to the #18 block recording both figures and that they cannot be
  adjudicated. ⚠ **This is deliberately NOT a re-float of pass-1 P6** (rebuild the gauge's measuring
  half), which Dave parked to its own session in `_FUTURE-STATE.md`; it does not ask for a better
  instrument, only that the record stop containing two different answers with no note that it does.
- status: floated

---

### P2 — The enactment register publishes a project-wide verdict ("4 of 81 rulings (5%) are PROVEN") over a corpus that harvests 4 ledgers out of at least 6, and the two bodies it cannot see are the Memento governance set and the ds-* defect ledger

- EVIDENCE:
  - `knowledge/_build_enactment_register.py:34–37` — `LEDGERS` is exactly four files:
    `_proforma/_DATAVIZ-DECISIONS.md` · `_RAG-DECISIONS.md` · `_TYPE-DECISIONS.md` ·
    `_BUTTON-DECISIONS.md`; `:40` — `RULING_RE` matches only `DV-D|R-D|T-D|B-D` + digits, so no other
    ID shape can be counted even if a file were added.
  - `docs/decisions/ADR-0016-enactment-proof-register.md:43` states the scope as *"one row per ruling
    harvested from **every ledger** (`_DATAVIZ-`, `_RAG-`, `_TYPE-`, `_BUTTON-DECISIONS.md`)"* — the
    universal claim and its four-item enumeration are in the same sentence. This is the
    [[gate-glob-scope-rule]] shape, in an ADR rather than a gate.
  - `knowledge/_ENACTMENT-REGISTER.md:11–17` prints **TOTAL 81** and *"**4 of 81 rulings (5%) are
    PROVEN.** That number is the finding"*. Grepped the generated file for `GM-D`, `M-SET`, `MEMENTO`,
    `` `M<n> ``, `A-D<n>`, `S-D<n>` — **zero matches.**
  - Outside the denominator: `notes/_MEMENTO-DECISIONS.md` carries ~50 individually-keyed rulings
    (D1–D6 · A-D1–A-D4 · P1–P8 · S-D1–S-D4 · V2-P1–V2-P5 · GM-D1–GM-D9 + D7-am · M1–M12) and
    `knowledge/_DS-IMPROVEMENTS.md` carries 19 `ds-*` entries, several of which are rulings not
    defects (`:817` ds-018 RULED A2·B2·C2; `:291` ds-012 RULED gutter-relative).
  - Not covered by the ADR's own roadmap: P2 of ADR-0016 is about turning CLAIMED into PROVEN
    (`:66`, `:102`) and P3 about advisory→blocking rollout (`:75`). Corpus **width** is named nowhere.
- PREVALENCE: 1 generated register · 4 of ≥6 ruling ledgers harvested · ~69 keyed rulings outside the
  81-row denominator. Checked: the register, its builder, ADR-0016, and both excluded ledgers.
- PROPOSED: smallest reversible step is **not** to widen the harvest (that is a design call about what
  "enactment" means for a process ruling, and it is Dave's). It is one generated line at the top of
  `knowledge/_ENACTMENT-REGISTER.md`: **name the ledgers harvested and the ruling bodies deliberately
  excluded**, so the 5% is read as "5% of the pillar ledgers", not "5% of the project" — the
  [[measuring-tool-must-not-guess]] rule applied to the register's own denominator. Widening
  `LEDGERS`/`RULING_RE` is then a separate, ruled decision with a measured before-and-after.
- status: floated

---

### P3 — M9's advisory gate had its promotion condition declared MET at #18, in writing, in the repo — and three wraps later it is still advisory, with no line anywhere live tracking the promotion

- EVIDENCE:
  - `_GM-ARCHIVE.md:93–94` (Batch 2026-07-27 #18, verbatim in the record): *"**Advisory promotes to
    blocking once this has been seen working — this is the seeing.**"* The same batch records the
    proxy catching a real miss on its first live run (`:87–89`, *"the check fired at this very wrap
    and it was RIGHT"*).
  - `knowledge/_capture_gate.py:580` — `retirement_receipts()` docstring still reads *"M9(a),
    **ADVISORY**"*; `:587` *"Advisory first, per the brief — **promote to blocking only once it has
    been seen working**"*; `:624` the finding still emits as `warns.append(f"retirement receipts
    (ADVISORY): …")`. The trigger fired; the tier did not move.
  - Nothing live tracks it. Grepped `GOOD-MORNING.md` + `_LIVE-STATE.md` for `M9` — **zero hits**.
    GM tracks the two *other* advisory promotions on the board: `:435` M10's trigger (with a
    `[born #18 · guards · until]` tag) and `:55` ds-018's C2 `--strict` promotion, whose own text
    says *"an advisory gate never promoted is documentation — this one has its trigger, use it"*.
    M9 is the one with a **fired** trigger and no home.
  - Brief `notes/_briefs/2026-07-27-memento-hardening-brief.md:79–80` set the condition
    (*"Promote to blocking only after it's seen working once"*) — so the loop was opened deliberately
    and closed nowhere.
- PREVALENCE: 3 wraps since the trigger fired (#19 · #20 · #21), 0 mentions in either spine file;
  2 of 3 comparable advisory gates are tracked, this one is not.
- PROPOSED: **Do not auto-promote** — the proxy's own docstring names its limit (`:582–585`: it cannot
  see whether a retirement was *due*, only whether text vanished), so blocking could fire on a
  correct wrap. Smallest step: one `[born · guards · until]` line beside GM `:435`'s M10 trigger
  recording that **M9's condition is already satisfied and the promotion is Dave's call**, with the
  known false-positive risk stated. That converts a silently-expired trigger into a decision he can
  make in one word.
- status: floated

---

### P4 — The dream-pass lane's own status block in the cold-start spine ends with a completeness claim ("owed list now … only") that is two days stale, and it is four stacked status paragraphs where the ledger already holds all four

- EVIDENCE:
  - `_LIVE-STATE.md:14–19` (§🔀 SPIN-OFF LANE) is one entry line plus **four** paragraphs each opening
    *"**Status (2026-07-26 …)**"* — `:16` later session · `:17` Shape A session · `:18` ruling session ·
    `:19` weekly-run session. All four carry the same date; only the last is current.
  - `:19` closes: *"**Lane's owed list now: D6 (Dave, before Shape C) + `-v2`'s own §7 leftovers
    only.**"* The word *only* is now false in two ways, both ruled after that line was written:
    **M11** — the supervised `memento-dream-pass` fire, a lane item, owed by Dave before Sun 08-02
    (ruled #17, 2026-07-27; carried in `GOOD-MORNING.md:422–423` and `notes/_MEMENTO-DECISIONS.md`
    § M-SET) — and the **dreamer hunt-list change** ruled #21, 2026-07-28
    (`notes/_MEMENTO-DECISIONS.md:322–327`). Neither appears in §🔀.
  - Everything in the four paragraphs is already in the lane's tattoo: `notes/_MEMENTO-DECISIONS.md`
    rows D1–D5, A-D1–A-D4, P1–P8, S-D1–S-D4, V2-P1–V2-P5 — read and matched paragraph by paragraph.
    This is the duplicate-register shape GM-D4 deleted §B for, surviving in the sibling file.
  - It sits in the region that matters: `GOOD-MORNING.md:435–437` — trimming `_LIVE-STATE`'s
    **standing body** (12,694 tk) is what arms M10's block. ⚠ Its token cost is **UNMEASURED** here —
    no tokenizer in this pass's toolset, and [[measure-dont-convert-units]] forbids a chars/4 guess.
- PREVALENCE: 1 region · 4 stacked paragraphs, 3 superseded · 1 false completeness claim · 2 ruled
  lane items missing. The region is read on every cold start (`_LIVE-STATE.md` is the chain).
- PROPOSED: two steps, both reversible, both cheap. (a) **Correct the stale line first** — strike
  *"only"* and name M11 + the hunt-list change, or point at the ledger instead of restating a list.
  (b) **Then**, and only if Dave's open LS-trim-vs-defer question (GM `:435`, open since #19) resolves
  toward trim: roll the three superseded status paragraphs verbatim to `_LIVE-STATE-ARCHIVE.md` via
  `knowledge/_gm_move.py` and leave one current-state line + a ledger pointer. (a) is a correction and
  needs no ruling; (b) is a compaction and waits on his.
- status: floated

---

### P5 — Four orphaned lines sit near the top of the cold-start spine: the tail of a superseded "Last refreshed" paragraph whose head was overwritten, making a dated claim that contradicts the line directly above it

- EVIDENCE: `_LIVE-STATE.md:45–49`, verbatim:
  ```
  45  *Last refreshed: 2026-07-28 ~09:30 BST (session #21, "M5 mover lands", Fable solo). Previous: 2026-07-28 #20 · 2026-07-28 #19 (older chain → `_LIVE-STATE-ARCHIVE.md`).*
  46  1104 → ~450 lines per the classification Dave ruled via markup (11 pins) on
  47  `reviews/CONSOLIDATION-AUDIT-2026-07-18.html`. Nothing deleted: ~580 lines relocated verbatim to
  48  `_DECISION-HISTORY/`, duplicates reduced to pointers, two entries removed on their own recorded
  49  instructions. Prior refresh: T-D12 ruling, commit `9fb1381`.*
  ```
  Line 46 has no subject and no opening `*`; line 49 closes an italic span that line 45 already closed.
  The fragment is the tail of a 2026-07-18 refresh note — its head ("*Last refreshed: 2026-07-18 …
  Consolidated…*") has been replaced in place by successive wraps while the body was never carried
  with it. The result is a live, undated assertion (*"Prior refresh: T-D12 ruling, commit `9fb1381`"*)
  that flatly contradicts line 45's *"Previous: #20 · #19"* — one paragraph apart, in the file the
  project calls the cold-start spine.
  - Grepped the whole repo for `1104 → ~450` and `Prior refresh: T-D12`: **only these two lines**, so
    the text was never archived anywhere — it is a residue, not a copy.
  - Mechanism is the file's own diagnosis: a header rewritten in place while its body survives is
    supersession-by-addition, the disease GM-D1…D9 gated in `GOOD-MORNING.md` and nowhere else.
- PREVALENCE: 1 instance, 4 lines, unique in the repo — but in the file every cold session reads
  second, above the LIVE section.
- PROPOSED: one edit via `knowledge/_gm_move.py` (this is precisely its 2d surface): move lines 46–49
  verbatim to `_LIVE-STATE-ARCHIVE.md` under the 2026-07-18 consolidation, leaving line 45 intact.
  Nothing is deleted, the T-D12/`9fb1381` provenance survives, and the spine stops carrying a
  contradiction. Optional follow-on, Dave's call: whether a wrap-gate check for *unclosed emphasis /
  orphaned paragraph* in the two spine files is worth the false-positive cost.
- status: floated

---

### P6 — A ruling Dave made and an agent enacted AFTER the wrap gate ran never reached the session's own record; the ★ LATEST banner is contracted to be that record (thin, but the mechanism is live and just ran twice)

- EVIDENCE:
  - #21 (`local_5f9cda5a`): the wrap completes and commits (`d927b95`), **then** Dave asks about hunt
    pointers, rules *"all three are probaly good. No?"*, and the agent edits
    `.claude/agents/dreamer.md` + the ledger and commits again (`a5ca45d`) — the whole exchange sits
    after the capture ritual, so build, wrap gate and STAND-002 never saw those edits.
  - The ruling is inscribed correctly in the tattoos (`notes/_MEMENTO-DECISIONS.md:322–327`,
    § DREAMER HUNT LIST +3, Dave's verbatim + `status: ruled`) — but grepping `GOOD-MORNING.md` and
    `_LIVE-STATE.md` case-insensitively for `dreamer|hunt list|dream-pass|dream pass` returns **no
    hit inside the #21 banner or the #21 delta** (only `GOOD-MORNING.md:375` and `:423`, both
    pre-existing lines about other things). GM-D7-am's read-chain contract calls the ★ LATEST banner
    *"the session record — GM-D4"* (`GOOD-MORNING.md:120`), and #21's ruling is not in it.
  - The mechanism ran twice in a row. #20 (`local_13f9ebbd`) has the same post-wrap shape — wrap
    commit `ded0238`, then Dave's *"less lets not forget this, thats the whole point"*, then
    `beea4a4` — **but that one was propagated**: it reached `_LIVE-STATE.md:27` and the GM §C·1 lane-1
    line. So the difference between the two is discipline, not design, which is what makes it a class.
- PREVALENCE: 2 of the last 2 sessions produced a post-wrap ruling; 1 of 2 propagated to the spine
  files. Thin on count, deliberately marked so; the mechanism is unguarded either way.
- PROPOSED: one line in `knowledge/_RUNBOOK-capture-ritual.md` — **a ruling that lands after the wrap
  gets an explicit addendum beat**: append to the ★ LATEST banner (or write a one-line "post-wrap
  addendum" under it), re-run the wrap gate, then commit. That is the smallest thing that makes the
  banner true again. ⚠ Do **not** promote the spec/ledger to Polaroid duty — A-D3 rightly keeps
  `dreamer.md` the single source; the gap is that the session record does not say the source changed.
- status: floated

---

## Method

**Read.** `MEMORY.md` index (hooks only) → `GOOD-MORNING.md` in full (479 lines: star-LATEST #21 +
PRIOR #20, DO-FIRST, §A, §C, #21 strata) → `_LIVE-STATE.md` (heads, §🔀, LATEST/PRIOR deltas, refresh
block) → `notes/_MEMENTO-DECISIONS.md` in full (328 lines, every ruled row) → `notes/_GAUGE-LOG.md`
in full → both prior proposals files (headings only, to avoid re-floating).

**Transcripts.** 10 of the last ~20 Cowork sessions read at turn level via `list_sessions` →
`read_transcript`: `local_5f9cda5a` (#21) · `local_13f9ebbd` (#20) · `local_a29fe155` (#19 conductor) ·
`local_d86f26f2` (#19 Fable worker) · `local_9ecbcf40` (#18) · `local_1564cbbc` (#17) ·
`local_90b8db6d` (#16) · `local_e79e89ee` (#15) · `local_f59c13c8` (#12) · `local_1ffa04b1` (the
GM-compaction architecture window). **Skipped, with reason:** the ds-018 / ds-019 / DV-D17 arc
(`local_62a6211c`, `local_f0986bd9`, `local_68267253`, `local_ba406592`, `local_9229ff74`,
`local_6e4afcb3`), the gauge-throttle window (`local_dcee92a2`), the instrument-fit window
(`local_cbfd919e`) and `local_ae78d674` / `local_e0773ea6` — every one of them is either on the
supplied do-not-re-float list, on a prior pass's checked-clear list, or predates
`notes/_GAUGE-LOG.md`'s first block, so nothing in them was comparable. Their repo consequences were
checked directly instead (register, gate, ds ledger, spine files), which is the higher-fidelity path.

**Fidelity ceiling, and where it bit.** Transcripts are turn-level: tool calls appear as bare names,
with no arguments and no results. Every checkable claim above was therefore verified against repo
state, and the only claims sourced *from* a transcript are the agents' own words to Dave — which is
exactly what P1 and P6 are about, so the ceiling is load-bearing rather than incidental there.

**Where the ceiling stopped a hunt.** This pass has Read/Grep/Glob/Write and no shell or git, so
**file modification dates and commit history were unavailable**. That blunted the new lane-order hunt:
I could not date any chart-surface edit. What I could check, I did — the #20 and #21 commit-state
stratums enumerate every file touched (`_GM-ARCHIVE.md:32`, `GOOD-MORNING.md:478`), and the only
lane-2 surface in either is `knowledge/_proforma/_DATAVIZ-DECISIONS.md`, touched at #20 for the ruled
breadcrumb. **On that evidence lane order has held since the #20 ruling** — recorded as a checked
observation, not a proof; a pass with git can settle it in one command.

**Checked clear this pass** (so the next dreamer does not re-open them): `_CAPTURE-GATE.md` is current
and green, dated 2026-07-28, 22 files in scope · M5's mover selftest is genuinely wired as a build
step (`knowledge/_build_all.py:57`), so the `[63/63]` claim has a mechanism behind it ·
`knowledge/_type-sweep-2026-07-27.json` and `knowledge/_render/verify_dv_d17_render.py` both exist,
so the DO-FIRST lines citing them are not stale pointers · M10's advisory tier is correctly still
advisory (chain 30,306 tk, threshold 28,000 — trigger has not fired) · the four stacked "Status"
paragraphs in `_LIVE-STATE.md` §🔀 are duplicated in the ledger, which is what makes P4 a compaction
rather than a deletion risk.
