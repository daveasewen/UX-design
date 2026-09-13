# HANDOFF #119 — #268 → #269 — THE DESIGNER PACK AND THE DECK

> ⚠ **This file is NEWER than `_CHAIN.md` and therefore OUTRANKS it.** Read it first, then the chain.
> ✅ **It should NOT trip `_session.py`'s R3 CHAIN OVERTAKEN, because #118's advice was taken at the
> cause:** the GM/LS roll and `_gen_chain.py` ran **before** this file was written, so the chain
> already names **#269**. If R3 fires anyway, **fix it at the cause — re-run the roll and the
> generator. Do not brute-force `--acknowledge` or `SESSION_ACK`; both hatches are DEAD** (tried once
> each at #117, both rejected) and making one real is still open, still nobody's decision.

---

## ⛔ READ THIS FIRST, IN THIS ORDER — AND VERIFY THE PREMISE BEFORE YOU TRUST ANY OF IT

1. **This file.** It outranks the chain.
2. **`_CHAIN.md`** — the whole contract. ⛔ **Do NOT open `GOOD-MORNING.md` "to check"**; the chain
   already carries the part of it a cold session needs.
3. **`_CARRIES.md` § `## residual → #269`** — **only when you need a body.** 420 items, 8 of them new.
   Retrieval key `carries:residual-269`. The count is probeable:
   ```bash
   PYTHONPATH=knowledge python3 -c "import _capture_gate as c;print(len(c._carry_items([l for l in open('_CARRIES.md') if '#269:**' in l][0])))"
   ```
4. **`notes/_RUN-OF-SHOW-david-rice-2026-09-10-v1.html`** and
   **`notes/_DEMO-SLIDES-apollo-2026-09-12-v7.html`** — the two live demo artefacts. ⚠ **Deck files
   v1–v6 are still in `notes/` as history. `-v7.html` is the live one.**

★★★ **A STALE MOUNT LOOKS LIKE A QUIET REPO** (#118's finding, and it still bites). Before acting:

```bash
cd /sessions/<your-session>/mnt/UX-design
git log --oneline -3
ls -la --time-style=full-iso _CHAIN.md GOOD-MORNING.md    # compare against git log's timestamp
grep -n "YOU ARE #" _CHAIN.md
```

If the newest commit is newer than `_CHAIN.md`'s mtime, **your mount is stale — stop and re-read.**

---

## ⛔⛔ DAVE'S — EIGHT THINGS, OPEN, VERBATIM. DO NOT RULE THEM.

**Nothing below was ruled at #268, and nothing below may be re-worded, merged, absorbed into a
recommendation, or re-put as a fresh option set.** A re-worded question is a new question.

**1. THE ASK — deck card 10 is still DRAFT.** The one sentence the whole demo is built to earn:

> *"One live project, sponsored — six weeks on the clock, K1–K5 measured against your own fifteen
> percent. If it doesn't beat your number, you've lost six weeks. If it does, you own the stack."*

It stands on `notes/_DEMO-SLIDES-apollo-2026-09-12-v7.html` card 10 as **DRAFT** and is ratified
nowhere. It binds to `s268-D8` (six weeks is **his estimate, spoken as one**) and to the K1–K5 slot
on the run-of-show; a change to either moves this sentence.

**2. TITLE EDGES — KEEP OR STRIKE.** The title card's fly-through draws faint edges between the
pinprick nodes. **A lane added them for density.** Dave's word for **v5** was *no edges*; **v6 and v7
have them and he has not ruled either way.** ⛔ A lane may not settle this by taste — it is a picture
he has already ruled on once.

**3. THE DATE v1.0.6 WENT TO THE DESIGNERS.** `knowledge/_received.json` records
`v1.0.6 → designers, date "unknown"`. The register's own words: *"`date` may be \"unknown\" when the
handover predates this register — that is a recorded gap, not a guess."* ⛔ **DO NOT INFER IT** from
a commit, a zip mtime or a chat date. Only Dave has the day.

**4. DREAM PASS 12 — FOUR PROPOSALS FLOATED, ZERO RULED.** The scheduled Sunday pass fired on time
(07:10, 2026-09-13, `feabd0e`). **A scheduled pass cannot rule and did not.** Bodies in
`notes/_dream/`. All four await his eye.

**5. THE PRE-BAKE REAL-PAGE DRIVE AS A STANDING RUNBOOK STEP.** `knowledge/_validate_demo_page.py`
was **built at #268** and is what ended three releases of 11/12 slippage. ⛔ **It exists as a GATE and
is NOT ruled as a STEP** — whether every future release must drive a real page pre-bake is his.

**6. FLY-THROUGH DIRECTION — 1→3 OR 3→1.** The title card flies the three KG islands in index order.
**Island 3 carries ~4% of the nodes across ~28% of the axis**, so the last ~6 seconds are sparse.
Reversing front-loads the density and ends in quiet. ⛔ **A measurement, not a proposal.**

**7. v1.0.13 HAND-OVER — WHEN, AND RECORD THE DATE.** v1.0.13 is cut, released, cold-run-9 green and
**UNRECEIVED**; under `s268-D4` it may still be re-cut at its own number *until it leaves the repo*.
⛔ **THE MOMENT IT IS HANDED OVER, A ROW GOES INTO `knowledge/_received.json` WITH THE DATE** — the
register's own ⛔ line: *"ADD A ROW THE MOMENT A PACK LEAVES THE REPO."*

**8. THE SIX-MONTH COMPARATOR — BOTH SIDES SEEN, UNCHANGED.** `s268-D8` has him saying it **as an
estimate**: *"lets say something like a 6 month project may become 6 weeks or even less if we use AI
in resaech and user testing"*. `notes/_DEMO-EVIDENCE-external-kpis-2026-09-11-v1.html` records that
**no published study supports a 77% cut.** ⛔ **Dave has seen both and has not moved. Both stand.**
No lane may soften the sentence to fit the evidence page, or harden the evidence page to fit the
sentence.

---

## WHAT #268 DID — THE NUMBERS, WITH THEIR PATHS

**Session #268 opened 2026-09-11 and wrapped 2026-09-13. 71 commits, `202fa30..d9943f6`, ALL PUSHED
before this wrap.** ⚠ **This is a MULTI-DAY SESSION, not a wrap date split** — every commit carries
its own true date; the ritual and its commit are both 2026-09-13; nothing was re-dated.

### ① Three releases, and only the third goes out

| Release | Ruling | Word | What it was | Outcome |
|---|---|---|---|---|
| **v1.0.11** | `s268-D1` | *"check and ratify"* | the regenerated canon.css v1.0.10 could not carry | cold run 7 green; ⛔ **gates 4/5 RED — the version sweep missed 3 literals**, so `--check` went red *after* the bake |
| **v1.0.12** | `s268-D2` | *"12"* | the sweep completed + the descender fix at cause | ✅ `--check` GREEN; ⛔ **cold run 8: 10/14 — the crop was still in the zip** |
| **v1.0.13** | `s268-D3` | *"okay do 13"* | the descender class **one level out**: 108 snippet copies of the leading-trim default made `:where()` | ✅ **cold run 9: 14/14 · `--check` GREEN · 10/10 gates** |

- **v1.0.13 zip** — `apollo-spider/dist/Apollo-Spider-v1.0.13.zip`, sha256
  `5d4df132b1f57f1764736d6bf46d3260bb7b7d0393a8317ea11c8f6b8bb282c6`, **21,202,835 bytes**, cut at
  `08e315d`. Frozen ledger re-seeded: **13 zips, `60604b8d109e`** (`df64895`).
- Reports: `notes/_subreports/2026-09-11-268-cold-run-{7,8,9}.md`.

### ② The gate that ended the slippage

**`knowledge/_validate_demo_page.py`** (`08e315d`) **drives the real dashboard page out of the STAGED
pack, before the bake.** Every existing release gate parses the manifest, the file list, the version
literals and the receipts; **not one opens the page a designer will open.** That is why a 5.50px crop
survived a green v1.0.12 and was found a full release cycle late.
**[[no-gate-parses-the-artefact]], seventh venue.** ⛔ It is a gate, not a ruled step — **Dave's #5**.

### ③ Eight rulings — `knowledge/_rulings.json` 445 → 453

`s268-D1` v1.0.11 ratified · `s268-D2` v1.0.12 · `s268-D3` v1.0.13 · **`s268-D4`** an UNRECEIVED
release may be re-cut at its own version, both shas declared · **`s268-D5`** *"mint all four"*, the
four edge-type seats · **`s268-D6`** *"both now"*, read back and confirmed **"yes both now plaease"** ·
**`s268-D7`** the six-month comparator dropped — ⛔ **`status: superseded`, `supersededBy: s268-D8`** ·
**`s268-D8`** plot point 04 carries predicted **and** measured, labelled differently.

⚠ **TWO THINGS THE COMMIT LOG STATES DIFFERENTLY FROM THE STORE, AND THE STORE IS RIGHT:**
- `a4f78ee`'s subject says *"s268-D3 inscribed: unreceived releases may be re-cut at version"*. **The
  inscription is `s268-D4`** — its own `conductor_note` says so: *"this ruling was asked for as
  s268-D3, which was already taken by the v1.0.13 ratification; it is inscribed at the next free
  id."* Two commits therefore claim "s268-D3 inscribed" (`66fadd1`, `a4f78ee`) and only the first is
  the D3 that exists.
- `s268-D4`'s **12 → 13 substitution is the conductor's, not Dave's** — declared in the ruling: his
  proposal named v1.0.12 as "the one that goes to the designers" because v1.0.13 did not exist when
  he said it. **The logic is his verbatim; only the number moved.**

### ④ The KG went green

- `s268-D5` seats `composedOf` / `delegatesTo` / `drivesConsumer` / `$contract` in
  `knowledge/components/meta.schema.json` (`cf23d3c`).
- `s268-D6` enacts **(a) and (c) together** (`03e519c`): `DECLARED_EDGE_TYPES` widened **off the
  schema**, and **the generator never wipes `edges` again** — per-edge refresh, in-place splice.
- ⛔ **The #265 fence on `gen_kg_edges.py` is LIFTED by that enactment and the generator was RUN FOR
  REAL** (`aa394ea`): 138 metas, 3 refreshed, authored edges intact.
- ✅ **`_validate_kg.py` rc 0** — it had been rc 1 with 5 FAILs since #265. **Re-run at this wrap
  seat, green.**
- Explorer regenerated at v1.10: **2,837 nodes / 4,902 edges, 0 orphans** (`2043811`).

### ⑤ Run-of-show + evidence

`notes/_RUN-OF-SHOW-david-rice-2026-09-10-v1.html` — `tr.beat`/`div.beat` selector collision fixed
(`011fb34`), slots in column 2, ■ glyph; **Risks 1, 2, 5 and 7 RETIRED on measurement**, Risk 3
closed on Dave's word. **Plot point 03** = his car-plant/gearbox metaphor **verbatim** + a
two-sentence spoken draft, no diagram (`2ec4a28`). **Plot point 04** reframed on `s268-D8` — 15%
(HSBC's own) / 47% (IBM Carbon) / the 6→6 hypothesis (`ae54cfd`). **Plot point 05** = K1–K5.
`notes/_DEMO-EVIDENCE-external-kpis-2026-09-11-v1.html` (`4b55163`) — **20 sourced rows**.

### ⑥ The deck

`notes/_DEMO-SLIDES-apollo-2026-09-12-v7.html`, ten cards, **v1 → v7.8** over two days.
designer-community-v3 chassis, Univers Next, scroll-snap. **Title** = fly-through of the three KG
islands, white pinprick nodes (cap 2.0/3.2px), faint edges, mouse-nudged τ 1.2 s, **return-to-path
removed** on *"too jerky"*. **Card 2** = the wipe — the same animation reversed out through a
difference blend, five chapters in Dave's words, run schedule removed on his word. **Card 3** = a
line-drawn 3D gearbox, hidden lines, mouse orbit, **metaphor line restored** after the gearbox lane
dropped it (`d9943f6`). **30 fps cap, DPR ≤1.5, stop on blur** — his *"this lane is a bit hot"*.

⚠ **THE IN-FILE VERSION STAMP READS v7.7, NOT v7.8.** The last commit (`d9943f6`) calls the state
**v7.8**; the highest `v7.x` string inside the file is **v7.7**. **Nothing was renamed to fix this at
the wrap** — a stamp is a measurement and re-dating it to match a commit subject is the T-D12
false-inscription shape. **#269 should decide which of the two is the name and make the other agree.**

### ⑦ Process — the durable lesson

**Dave twice told the conductor to review the lanes' output itself — *"you're the art director"*.**
Every lane after that got a **conductor screenshot review before it reached him**, and **two lanes
were sent back on the picture, not on a gate.** ★ **A gate tells you a lane ran; only looking tells
you what it made.** It is the same finding as ② in the human direction.

---

## GAUGE — AND IT IS A BREACH

- ⛔★★★ **FILL 335,209 real, peak across 209 turns** (first-hand, `knowledge/_checkin.py`) — past the
  `s260-D2` delegated **stop line of 180,000** and past the **200,000 working wall.** Not averaged,
  not softened.
- ⛔★★★ **BOOT 71,939 real — 1,939 over the 70,000 shrink-only literal, the FOURTH CONSECUTIVE
  BREACH:** #265 70,260 · #266 70,442 · #267 70,717 · **#268 71,939.** The literal does not move
  (`s240-D2`/`s241-D1`); the refusal is carried in the **#243 form**, twenty-second wrap running.
- ⛔ **NO `subs` LINE.** No per-lane `message.usage` was captured anywhere this session and no
  aggregate was supplied. An estimate in a measured field is a false inscription.
- ⛔ **`/sessions` IS 96.5% FULL — 337,752 KB free.** No live GC; dead-session scratch is undeletable;
  **at 100% no session boots** (#227, #228). Run `python3 knowledge/_gate_scratch_hygiene.py` early.

---

## WHAT THIS WRAP DID NOT DO — DECLARED, NOT HIDDEN

- ⛔ **Ritual step 1b — the NARRATIVE DOSSIER (`_DECISION-HISTORY/2026-09-13-268-*.md`) is OWED and
  NOT WRITTEN.** This wrap was briefed narrow (handoff + chain + commit + push). The session's
  reasoning arc is carried by the ⏱ delta and this file alone, and a cold reader should know that.
- ⛔ **Ritual step 3 — MEMORY.** This seat cannot write to the memory filesystem; **the `#268` hook is
  NOT authored.**
- ⛔ **`_build_all.py`** (single-process run is sandbox-impossible; CI delivers the verdict on push) ·
  **the render gates** (`_validate_screen.py`, `_validate_fit_physics.py` — chromium needs
  `PLAYWRIGHT_BROWSERS_PATH=/tmp/pw` and `/sessions` is 96.5% full) · **`knowledge/_tests/test_gates.py`**
  (copytrees ≈5 GB, ENOSPC).
- ⛔ **The §A byte-identity probe that #237…#267 ran at the `size:` line was NOT run here and its
  figure is NOT re-stamped.** An un-run probe's number is not carried forward as if it had been taken.
- ⚠ **The ★ LATEST banner measures 1,197 real — UNDER the `s241-D2` cap of 1,200 — but it is 11
  lines against the same ruling's 10-line clause, and that is REPORTED rather than met by deleting a
  bullet.** It was trimmed in seven measured passes from 1,334; **under the cap means shorter, never
  quieter** — no declared gap, measured figure or word of Dave's was dropped to fit.

### Gate state at close: **3 fail, 16 warn** — all three inherited

The wrap's FIRST gate run read **9 fail**. Six were this wrap's own and were fixed at cause: the
rulings page re-rendered (`_render_rulings.py`, `--check` FRESH) · the titles receipt re-generated
against **this** session's banner · the hand-copied chain figure **deleted** from the `size:` stamp
(RETIRED #45 — a hand copy of a generated number is only accurate on the day it is written) · the
banner brought under its cap · the `stop line <N>` probe made resolvable again (the delta said
*"stop line of 180,000"*; `CHAIN_STOP_RE` wants *"stop line 180,000"*) · the retrieval index rebuilt
**LAST**. The **three that remain are inherited and are carried in the #243 form, not routed around**:

1. `boot-drift CEILING BREACH` — 70,000 against #265 70,260 · #266 70,442 · #267 70,717. ⚠ **#268's
   own 71,939 is not in that list yet** — it reaches `notes/_GAUGE-LOG.md` at the NEXT wrap's 2f
   roll, so the gate's series will read **four** next time.
2. + 3. `boot double-count #243` and `#264` — artefacts of **rolled archived text**. ⛔ **The repair
   is not an edit: a rolled stratum is verbatim record (`s183-D1`).** ★ Ruling-shaped and still
   Dave's, unchanged since #267: **the check's SCOPE wants fixing, not the strata.**

- ✅ **RAN AND GREEN:** `_validate_kg.py` (rc 0) · `_gm_move.py` (5 ops, receipts printed after the
  writes) · `_roll_state.py` (**2c 2/2 · 2d 3/3 · 2f strata 1, log #267**) · `_gen_chain.py`
  (fixed point in 2 passes, `--check` FRESH) · `_gm_usage.py --check-line` (usage line well-formed) ·
  `_render_rulings.py --check` (FRESH) · `_gen_titles.py` (receipt written) ·
  `_build_memento_index.py` (**2,154 records, run LAST — `index_freshness_check` compares CONTENT,
  never mtime**).

---

## THE #269 EXECUTION ORDER

1. **Put the eight DAVE'S items to him — in their own words, as they stand above.** They are the
   session. Lead with **#1 (the ask)** and **#7 (when v1.0.13 goes out)**: everything else is cheap
   and those two have weight.
2. **Rehearse the run-of-show out loud.** #268 **filled** the page; **nobody performed it.** The
   carry's verb was REHEARSE and it is still owed — that is why the #268 lead is struck only
   **partially** in `_CARRIES.md`.
3. **Settle the deck's version name (v7.7 vs v7.8)** — one of them is wrong and it is mechanical.
4. **Write the owed dossier** if #269 has room: `_DECISION-HISTORY/2026-09-13-268-*.md`, the WHY and
   HOW of three releases and a same-day supersession.
5. **Author the #268 memory hook** — the surface that can write to memory is not this one.

---

## ⛔⛔ DO-NOT-RULE — CARRIED FROM #118, UNTOUCHED BY #268

`CONTROL_TIER_44` NOT flipped · `MARK_TIER` stays `warn` · `BOOT_FIRSTTURN_TK` NOT refreshed · the
boot floor NOT changed · `DOFIRST_INDEX_TK_MAX = 700` NOT raised · the three surface-recorder
constants NOT refreshed · **`G1`–`G17` all open** · graph-mark demotion NOT RULED · mono grey ramp
(*he said NOT NOW*) · SC dark (`G14`) · dv-lockup's 3 placeholder titles · `G8` retire-or-pin · the
type-gate tier (a)/(b) · **the SC-dig auto-switch families (the 0-neighbour RED)** · the **thirteen
#265 lane RSQs** · the **eight islands** · the **four PARKED glyphs and `global-money`** ·
**#241's midnight-wrap question, age 27.**

⛔ **Do NOT widen an error bar or edit a constant to fit a gate.** ⛔ **Do NOT raise a cap to make a
gate pass.** ⛔ **Bucket A items keep their EXACT original wording.**

---

## STATE AT HANDOFF

- ✅ **#268's own 71 commits are PUSHED** — `git log @{u}..HEAD` read **0** at the wrap seat,
  first-hand, before this wrap's commit.
- ✅ **The full 2c / 2d / 2f roll RAN:** #266's banner → `_GM-ARCHIVE.md` § Batch 2026-09-13 #268 ·
  #267's post-mortem → `notes/_GAUGE-LOG.md` (22 ln, appended at EOF) and its commit-state →
  `_GM-ARCHIVE.md` · #265's ⏱ delta and its 9,540-char `Previous:` segment → `_LIVE-STATE-ARCHIVE.md`
  § Rolled 2026-09-13 #268. **Verbatim moves, via `_gm_move.py`. Nothing was hand-rolled.**
- ✅ **`_CARRIES.md` § `residual → #269` written by ONE programmatic pass**
  (`notes/_lanes/268/W/carry269.py`): **560 age brackets bumped** (8 of them `NEW — 0` → `1`), one
  surgical edit asserted unique. **Probe 412 → 420.**
- ⚠ **Dream pass 12's residue was inspected and committed at this wrap**, not carried: the diff is
  the dreamer's own bookkeeping — grade counts (FRESH 33 · AGING 10 · STALE 2 · UNPROVABLE 7), a P4
  spot-check note, two rehearsal-log appends. **No rule, threshold or ruling is touched by any of
  it.** The dream-pass `Last refreshed` stamp was **demoted verbatim** into the `Previous:` chain
  rather than overwritten — it is a real refresh of that file and is not this wrap's.
- ⚠ **`.git/index.lock` is SANDBOX-CREATED** by ordinary read-only git here. Clear it through the
  delete-permission tool, **never `rm`**, and never `mv` it to `/tmp` (that fails on this mount).
