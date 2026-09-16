# #279 — the wave lands, and the graph is not three layers

provenance: 279 · 2026-09-16
status: observed

*The WHY and HOW of #279. The WHAT lives in its terse homes: the ★ LATEST banner in `GOOD-MORNING.md`,
the ⏱ LATEST DELTA in `_LIVE-STATE.md`, `knowledge/_rulings.json` § `s279-D1`, the twelve filed
sub-reports under `notes/_subreports/2026-09-16-279-*`, and `git log`. Both-way links: spine entry =
`_LIVE-STATE.md` ⏱ LATEST DELTA #279 · ledger = `knowledge/_rulings.json` § `s279-D1` · handoff =
`_HANDOFF-130-the-wave-lands-and-the-graph-question.md`.*

---

## 1. The shape of the day, and why it is the session #277 ruled for

#277 produced thirteen rulings and enacted three of them. #278 enacted one more and did no graph work
at all — by design, because the cloud move had to be measured before anything was built on top of it.
That left `s277-D4`…`s277-D13` as **law with no tree**, which is the most expensive state this project
knows: a ruling that is ratified and unbuilt costs a carry line on every wrap and reads identically at
age one and age thirty.

#279 was the discharge. Ten lane commits, three Fable verify seats, twelve filed sub-reports, and
eleven of the thirteen rulings went in. The arc that matters is not the enactment — it is that the
enactment was correct and **Dave rejected the result anyway**, which is a different kind of finding and
the reason this dossier exists.

## 2. The method that repeated across every lane, and what it bought

Every lane ran BUILD → Fable VERIFY → FIX, and the verify seat found something real every time:

- **IL → IV → IL2.** The icons landed at `f641242` (688 nodes, 1,299 edges, 32 declared nulls, selftest
  18/18, 26/26 mutants caught). IV then found that **28 of the 32 declared nulls existed in no
  `knowledge/` file at all** — only the four `t:null` edges actually landed — which breaks `s277-D4`'s
  *carried, never dropped* and `s277-D7`'s *enter VISIBLY*. IL2 (`84658db`) landed them.
- **RD → RV.** The reader landed at `d6bd57b`. RV re-drove all eight contract fields from source and
  found the ratio re-typed: RD's report said **31.83×** where `measure.json` said **35.14**. It also
  found that RD's SKILL.md edit had turned the BLOCKING frozen-release gate (`s114-D4`) **RED** — a
  gate RD did not know it was standing on.
- **SC → RV → SC2.** Scope per guideline file landed at `9e7a158`. RV's F4 found the row-level facet
  union misrouting `photo26-002` onto `app-shell-top-nav`; SC2 (`e3facb4`) added per-rule `ruleFacets`
  overrides — **27 on 5 rows, 0 refused, 26 strictly narrower**.
- **EX → EV → EX2.** Explorer v1.15 (`2c6b640`) then v1.16 (`9b2e1b0`), EV grading the `designrulings`
  sub-chip **stretched** before Dave ever saw it.

**The finding: the verify seat is not overhead, it is the mechanism.** Five of the six build lanes
passed their own drivers and were still wrong in a way a second seat could see. That is the #277
pattern repeating with a larger sample, and it is now the shape of the day rather than a precaution.

## 3. The one ruling, and how it was reached

Dave was given two questions off the icons verify and answered both in one breath: *"1. I need to do
the manual review of the 31"* and *"2. you'll have to give me the plain prose of this"*. The second is
the interesting one. The pack question — should designer-skills-v2 ship the reader and the
Constitution, or should ASK stay repo-side only — had been put to him in the vocabulary of the machine,
and he refused to answer it in that vocabulary. Given the plain prose of the two options he answered in
four words: ***"i agree 'a' it is"***.

That is `s279-D1`: **the pack ships `_compose_slice.py` and `_rulings.json`, so ASK reads the
Constitution live in-pack.** It reverses a deliberate exclusion in `_gen_pack_manifest.py` by his word,
and it is a release under `P-269-1` — lane PK re-baked designer-skills-v2 to **v2.1**, 849 → 1,102
files, read closure **218 paths with 0 outside the pack**, ASK's twelve questions answered in-pack at
**5,053 tokens, max 755**, and a planted ruling (`s998-D9`) answered live from inside the pack while a
repo grep found nothing — which is the proof that "reads live" means what it says.

**The dead-end that was not taken, and why it matters:** the same reversal for `apollo-spider` was
NOT fired. PK armed it **version-gated** (`READER_SHIPS_FROM = "v1.0.14"`, `READER_RULING =
"s279-D1"`) because v1.0.13's manifest is RATIFIED under `s268-D3`, its zip frozen, and two BLOCKING
arms pin the generator byte-for-byte — any emitted change at v1.0.13 turns both red. Cutting Spider is
Dave's word under `s219-D4(2)`. A lane that had "just shipped it" would have taken a ratified artefact
red to save one commit.

## 4. The correction the day delivered: enacting a ruling's letter is not enacting its intent

Dave looked at the explorer 1.16 screenshot — the graph a long horizontal smear beside four labelled
legend boxes — and wrote:

> *"BTW do we still have work to do on the graph... this does not look like 3 layers, just relabelling
> and grouping them isn't what I expected tbh."*

**Nobody did anything wrong, and that is the finding.** `s277-D8` as inscribed says *storage untouched;
chips and family labels change*. EX and EX2 built exactly that. EV verified exactly that — chip-off
identity proven node-for-node, edge-for-edge, position-for-position against 1.14. The ruling was
enacted to its letter and the letter was not the thing he wanted.

What he wants is a **LAYOUT**: three visibly separated layers on the stage, not three labels over one
force graph. That is not a smaller version of what was built; it is a different object.

⛔ **And it is NOT inscribed.** A wrap may record a question; it may never answer one. The option has
not been put to him, so what exists is a question, not a ruling — written as the question it is under
`s271-D4`. **#280's first move is a layout lane that renders ONE concrete option on a page for his eye,
not a description of one.**

The obstacle is already measured, which is the useful part: lane EX2 found the OFF-column band is
**5,700 world units** of empty slot between the base cluster (x ≤ 449) and the assets column
(x ≥ 6,172); runtime column packing is **~25 lines** — but it moves ghost positions, so chip-off canvas
stops being pixel-identical to 1.15 and the change needs its own lane with pixel proof.

## 5. The thing the day generated that no lane could close: four ruling-shaped questions

Each one is a place where a lane found that the next step is Dave's word rather than more code, and
each is carried as a QUESTION PUT rather than a state of the world:

1. **The `designrulings` sub-chip.** Its label reads **341**; at page defaults it governs **28** drawn
   edges, and **10 of the 341 can never draw**. `s277-D8` fixed DESIGN GOVERNANCE at three provenances,
   so lane SC's "inference by declared scope" chip would be a fourth — **a ruling before it is ~25
   lines of code.**
2. **A thirteenth verb.** `usesIcon` 371 and `usesLogo` 19 have a consumer (the slice's `assets` field,
   ASK Q12) and no verb. And `verbVia`: keep it for provenance at ~+1,500 tokens across 122 rows, or
   drop it. Lane VB declared both *"Dave's to ratify, not this lane's to pad"* — a lane refusing to
   pad a ruling is the behaviour the DO-NOT-RULE list exists to produce.
3. **The Spider v1.0.14 cut** (§3 above).
4. **The `va25-013` split.** SC2 landed 27 facet overrides and deliberately left this rule alone: its
   own text says *"icons/avatars 1:1 square"*, so it genuinely binds 111 icon-bearing components and an
   override stripping `icons` would contradict the quoted rule. **Narrowing it is a rule SPLIT in
   `visual-assets.md`, never an override** — the distinction between fixing a routing artefact and
   editing the law.

## 6. What is still open, in one line each

`s277-D12` (tokens at group+tier) **was never started** — no lane, no line in the tree; #280's third
move · his 15-base export is received and **unread by the record**, and where its flags and notes
disagree the **note is his sentence — ask, do not guess** · the four questions in §5 · the standing reds
(showroom 108 stale, resolver FAIL(6), lane-ownership 2/3), every one inherited and every one his or
another session's.

## 7. Resolved state

`knowledge/_rulings.json` **604 → 605** (`s279-D1`, span `18  0`, zero deletions, reconstruction proof
passed). Eleven of thirteen `s277` rulings are in the tree. The pack is at **v2.1** with the reader and
the Constitution inside it. `_CARRIES.md` § `residual → #280` holds **507 probeable items**, one carry
STRUCK with its `s183-D1`/`s188-D2` receipt because the day's own commits falsified it, and seven new
items that become countable next wrap. The graph question is open, and it is the first thing #280 does.
