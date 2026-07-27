# GM compaction ARCHITECTURE — proposal v1 (2026-07-27, Fable, session "GM compaction architecture")

provenance: local_1ffa04b1-ec26-4dd2-ab19-8c1d8e94167d · 2026-07-27
status: ruled — `notes/_MEMENTO-DECISIONS.md` § GM growth-contracts ruling (GM-D1…GM-D9)

**★ RULED 2026-07-27, same session — ALL NINE AS RECOMMENDED** (Dave, explicit option-select:
*"All nine, as recommended"*). D1(a) · D2 all four, term LATEST+2 · D3(a) · D4(a) · D5(a) · D6(a) ·
D7(a) · D8(a) · D9. **NOTHING ENACTED** — enactment brief:
`notes/_briefs/2026-07-27-gm-compaction-enactment-brief.md`. Original proposal text below, unedited.

**Status at authoring: PROPOSAL. Nothing here is enacted. Dave rules by number (GM-D1…GM-D9).**
Rulings → `notes/_MEMENTO-DECISIONS.md`. Enactment = a later window, runbook-first.

**Invariants honoured by every proposal below (non-negotiable, restated so no option can violate them):**
- **§A is untouched.** No cap, no roll, no rewrite. Update-on-shape-change only. The 07-18 incident and its reason stand (runbook :126–131).
- **Every roll obeys the 2c EXIT CHECK** — ⚠/⬛/AWAITING/OPEN-CALL/DEFERRED-TO-DAVE items may not move until they already live in a standing section. Dated homes don't count.
- **Rolls are verbatim MOVES, never rewrites.** The archive stays a convenience copy, never a tattoo.

---

## 1 · Diagnosis (measured this session; all numbers from probes, not the brief)

**The file, today:** 90,204 B · 910 lines (brief said 81.8 KB/840 — it grew **+70 lines in ~1 day**).
Spans: preamble+banners 1–37 · **DO-FIRST 38–292 (255 ln, 28%)** · §A 293–483 (191 ln, 21%) ·
§B 484–551 (68 ln) · **§C 552–910 (359 ln, 39%)**, of which ~146 ln is a stratum stack (below).
Markers: ⛔ 11 · ⚠ 62 · ⬛ 10 · SUPERSEDED 5 · date stamps 76 (entries ARE dated — retirement can key on them).

**Growth attribution — the hypothesis confirmed and sharpened:** of the +70 lines since the brief,
DO-FIRST +27 and the §C tail +~43 — **~97% of growth landed in the two regions with no roll rule.**
2c/2d verified as briefed: they govern **banners and deltas only** (runbook :95–124).

**Correction to the brief:** §C·5 "Parked" is NOT the growing organ — the true Parked list is
**3 lines** (:761–763) and stable. What grows below its heading is an unlabelled
**pre-flight / post-mortem / COMMIT-STATE stratum stack**: sessions #12, #8, #7, #6 all present,
two blocks already hand-marked *"[SUPERSEDED — kept for the record]"* — the author felt the
pressure to roll but no rule licensed the move.

**The structural defect, named (this is why one-off trims keep being needed):**

- **SD-1 · Partial roll coverage.** Roll rules exist only where bleeding was noticed (2c banners,
  2d deltas — both added AFTER their file broke a Read). Every other stratum-generator appends forever.
- **SD-2 · Supersession-by-addition.** Under move-discipline with no WHEN rule, the only legal way to
  kill text is to pile a notice on top of it. DO-FIRST now carries a #10 stratum, a #11 stratum
  (40 lines of spec its own #12 header declares HISTORY), and #12 notices negating both. Dead text
  and its warning label both bill full price every cold read.
- **SD-3 · No lifecycle metadata.** Nothing records what a notice guards or when it lapses, so no
  gate CAN retire anything; everything retires by hand, i.e. never.
- **SD-4 · Standing content bleeds into session sections.** Throttle canon, model routing, potholes,
  read-order — all inscribed elsewhere (`_RUNBOOK-context-gauge.md` Half 0b etc.) yet restated in
  DO-FIRST. Recall creeping back into the file whose whole design is retrieval.
- **SD-5 · The read-chain is a selective instruction pretending to be complete.** GM :288 says
  *"Then `_LIVE-STATE.md` → the decision files it points to"*; LIVE-STATE cites **112 asset paths**
  (~312K tk for the resolvable subset per the Opus measure — 1.5× a window). Unreadable by construction,
  and nowhere does the file say so.
- **SD-6 · No budgets, no gate.** Behaviour JS has ADR-0015 byte budgets with a blocking gate; the
  most-read file in the repo has neither. `_capture_gate.py` (built 07-26) is the natural anchor.
- **SD-7 · Gauge floor priced at 0.** The band table (GM :5) ignores the ~22–24% cold-start chain.
  Dave's refinement, agreed this session: the floor is a *variable this work shrinks* — so fix the
  **mechanism** (measured floor, bands on remaining budget), never a snapshot constant.

**Precedent that the cure works:** 2c's first run cut GM 35%; 2d's first run cut LIVE-STATE
205 KB→62 KB *after it too exceeded a single Read*. This proposal extends a **twice-proven pattern**
(cap + archive sibling + verbatim move + EXIT CHECK) to the sections still uncovered.

**Minor defect, fold into enactment:** `_GM-ARCHIVE.md` batch serials collided (two "Batch 11",
two "Batch 6" — parallel sessions minting serials independently). Batch key should be
`<date> <session#>`, not a serial.

---

## 2 · The architecture in one line

**Every GM section declares a growth contract — (what it may contain · cap · roll target ·
retirement test) — enforced at wrap by the capture gate; §A alone is standing and uncapped.**

---

## 3 · Decisions for ruling

### GM-D1 — DO-FIRST gets a typed-content contract + roll rule (new runbook step 2e)
DO-FIRST may contain ONLY: **(i)** the current worklist, **(ii)** live supersession notices whose
target text is still visible on a live surface, **(iii)** closure tombstones within their D2 term,
**(iv)** one-line POINTERS to standing canon — never restated bodies (kills SD-4).
At each wrap, strata older than **LATEST + 1 session** roll verbatim to `_GM-ARCHIVE.md`, EXIT CHECK first.
- **(a)** Contract + **cap 120 lines** (warn), 180 (block). A compliant DO-FIRST today ≈ 60–80 ln.
- **(b)** Contract, no cap — trust the typed-content rule alone.
- **(c)** Cap only, no typed-content rule.
**REC: (a).** The cap catches what the type rule misses and vice versa; both are one gate check.

### GM-D2 — The retirement test, per notice type (the "⛔ when does it stop earning its place?" answer)
- **Supersession notice** (*"X is DONE, stop planning it"*): lives **exactly as long as the text it
  negates remains on a live surface** (GM or `_LIVE-STATE.md`, archives excluded). When the dead
  stratum rolls, the notice rolls **with it, in the same batch — they are one move**. A warning label
  may not outlive the thing it warns about, and must not die before it.
- **Closure tombstone** (*"✅ CLOSED, do not reopen"*): term = **LATEST + 2 sessions** (mirrors 2d).
  To persist beyond term it must name a **structural guard** — a gate that enforces the closure, or
  a ledger closed-register line. After term it rolls; §C keeps one aggregate line
  (*"recently closed: ds-014 · ds-019 · …"*). **A tombstone that must live forever is evidence a gate
  is missing** — gate-don't-patch, applied to the record itself.
- **Record correction** (*"the collision DOES NOT EXIST"*): same test as supersession notices, plus
  the correction must be struck through **at the source of the wrong claim** before the notice may roll.
- **Perishable readings** (pace/panel, quota): **replaced at next wrap, never stacked.** Already dated.
**REC: adopt all four.** Options if you want a different tombstone term: **(a)** LATEST+2 *(rec)* ·
**(b)** LATEST+1 (aggressive) · **(c)** LATEST+3.

### GM-D3 — Lifecycle tags make D1/D2 mechanical (new entries only)
Every NEW notice/tombstone carries one machine-readable suffix:
`[born #12 · guards: <target> · until: <condition|session>]`. The capture gate lists retirement-due
items at each wrap — retirement becomes a checklist, not a memory feat.
- **(a)** Full tag on new entries; existing entries are NEVER retro-tagged (verbatim discipline) —
  they retire via one supervised audit pass at first enactment.
- **(b)** Born-session only (cheaper, gate can't check `guards:`).
- **(c)** No tags — hand-audit every wrap.
**REC: (a).**

### GM-D4 — §B is merged into the banner (runbook step-2 amendment)
Practice has already voted: §B's own STALE notice (:486) declares the banners authoritative, and the
★ LATEST banner already carries what the runbook demands of §B (evidence-per-claim, model/effort,
gauge stamp). §B today = a stale warning + three "retained for context" strata (07-26, 07-23, 07-22).
- **(a)** DELETE §B. Banner spec formally absorbs §B's requirements (evidence lines,
  provenance-shaped). Existing §B strata roll verbatim to `_GM-ARCHIVE.md`, EXIT CHECK first.
  GM structure becomes **banner (=session) · §A · §C**.
- **(b)** Keep §B as LATEST-session-only with a 2c-style roll (banner = summary, §B = evidence detail).
- **(c)** Status quo + a roll rule for the "retained for context" tail only.
**REC: (a).** −68 lines and a duplicate register; nothing is lost that the banner + dossiers don't hold.
This amends the runbook's ratified required-structure — flagged as such; it changes only on your ruling.

### GM-D5 — The stratum stack gets a roll rule (new runbook step 2f) + a home
GM keeps **LATEST pre-flight/post-mortem + LATEST commit-state only** (the handoff's freshness and
trust stamp). All prior strata roll at wrap.
- **(a)** Post-mortems → NEW **`notes/_GAUGE-LOG.md`** (append-only, one block per session);
  commit-states → `_GM-ARCHIVE.md`. The gauge log turns the throttle programme's "n=1 again" into a
  countable dataset — pre-flight vs closed band, overrun causes. *(rec)*
- **(b)** Everything → `_GM-ARCHIVE.md` (uniform, no new file).
**REC: (a).** The post-mortems are measurements, not narrative; a log makes them queryable.
EXIT CHECK applies — e.g. #12's "fork rule failed mid-enactment" lesson must be inscribed in the
gauge runbook before its stratum rolls. Batch key fix (`<date> <session#>`) rides along.

### GM-D6 — §C active-queue contract
§C·1–4 items = **pointer + state + owner**, no method bodies (method lives in briefs/ledgers — the
hit-area item already does this right). Parked stays as-is (3 lines, correct). Cap for §C excluding
the D5 stack: **(a) 150 lines** *(rec)* · **(b) 200 lines** · **(c) no cap**.
Today's §C minus the stack ≈ 210 ln — one pruning pass needed, mostly §C·2 inline ruling texts that
already live in the review docs. Every trim = verbatim move to archive, EXIT CHECK first.

### GM-D7 — The read-chain contract becomes explicit and budgeted
Replace GM :288's open-ended chain with an honest contract, stamped in the file:
*"This file ≤ N. Chain = GM + `_LIVE-STATE.md` ≤ M (~12% of a window). Everything cited beyond the
chain is RETRIEVAL (`_consult.py`, grep a section), never a reading list."*
Both files carry their own size stamp at wrap (gate-checked) so drift is visible, not discovered.
- **(a)** Chain target **≤ ~24K tk (~12%)**: GM ≤ 8K, LIVE-STATE ≤ 16K. *(rec as target)*
- **(b)** ≤ ~30K tk (~15%) — looser, no LIVE-STATE follow-up ruling needed.
Note: LIVE-STATE is 68 KB today; meeting (a) likely needs a separate 2d-tightening ruling
(LATEST+2 → LATEST+1?). **Deliberately NOT proposed here** — separate patient, separate ruling.

### GM-D8 — Budgets wired into the capture gate
`_capture_gate.py` gains per-section line counts + the D7 size stamps: **warn at cap, BLOCK at
cap+50%**, failure message names the runbook step and nothing else (advice prose kept minimal —
exit code is the evidence, prose goes stale). **Splitting never buys headroom** (ADR-0015 phrase):
moving content to a new un-governed file fails the gate unless that file declares its own contract.
- **(a)** Warn+block as above *(rec)* · **(b)** advisory only *(⚠ an advisory gate never promoted
  quietly becomes documentation — GM's own words, :59)*.

### GM-D9 — Gauge floor + bands: mechanism, not snapshot (your reframe, ratified)
- Floor = **measured at session start** (fill announced after the mandated reads).
- Bands defined on **remaining budget**, inscribed ONCE in `_RUNBOOK-context-gauge.md`; GM :5's
  inline band table becomes a pointer (trust the spine — two copies of a band table WILL drift).
- Post-compaction floor target: harness ~15–20% (not ours to shrink) + chain ≤12% (D7) + memory
  ~2.6% ⇒ **~30–35%**, vs ~42–46% today. The ~24% chain-floor becomes the "before" evidence.
- Band NUMBERS are yours and are ruled in the gauge canon, not here. This decision fixes only the mechanism.
**REC: adopt.**

---

## 4 · What it buys (estimate, all moves verbatim — zero content loss)

§B −68 · dead DO-FIRST strata ≈ −100 · stack tail ≈ −120 (LATEST kept) · §C prune ≈ −60
⇒ **GM ~910 → ~450–500 lines ≈ 12–13K tk**, single-Read again, with §A untouched at full length.
Chain ~22.6% → **~13–14%** before any LIVE-STATE ruling. Growth thereafter is bounded by contract,
not by the next emergency.

## 5 · Enactment plan (post-ruling; fresh window; Opus conducts, Sonnet lanes; NOT this session)

1. Amend `_RUNBOOK-capture-ritual.md`: steps 2e/2f, §B spec change (per D4), archive batch key.
2. Wire D8 into `_capture_gate.py` (+ bites: over-budget fixture must go red).
3. One supervised compaction pass under the new rules — verbatim moves, EXIT-CHECK receipts per batch,
   §A untouched, one commit, paste-ready summary. The D3 audit pass rides along.
Price: ~30–40% of one window. Rulings inscribed in `notes/_MEMENTO-DECISIONS.md` first.
