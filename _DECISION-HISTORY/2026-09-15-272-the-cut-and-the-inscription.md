# #272 — THE CUT AND THE INSCRIPTION

provenance: 272 · 2026-09-15
status: observed

*The narrative dossier for chat #272 (`_RUNBOOK-capture-ritual.md` step 1b). The WHAT is in
`knowledge/_rulings.json` (`s272-D1`…`s272-D93`), in `_LIVE-STATE.md`'s ⏱ LATEST delta and on
`GOOD-MORNING.md`'s ★ LATEST banner; this file holds the WHY and the HOW. Both-way links:
spine → `_LIVE-STATE.md` § ⏱ LATEST DELTA #272 · ledger → `knowledge/_rulings.json` §
`s272-D1`…`s272-D93` · handoff → `_HANDOFF-123-the-cut-and-the-inscription.md` · his words →
`notes/_lanes/272/DAVE-RULINGS-2026-09-15.md`.*

---

## ⚠ THE DATE, FIRST, BECAUSE THE RECORD HAS TO SAY IT PLAINLY

**The session opened on the evening of 2026-09-14. Dave's answers, every commit and this ritual
are 2026-09-15.** That is a **WRAP DATE SPLIT, the fourth occurrence**, and it is handled in the
**#241 shape, BY ADDITION**: a fourth standing notice is written beside #241's, #248's and #261's,
and **nothing is re-dated**. The ritual stamps 2026-09-15 because that is what `date` returns at
the seat that ran it, and the gate's *"Last refreshed is not today"* arm must grade a true
statement. #241's ruling-shaped question — *what should a wrap that spans midnight stamp?* — is
still Dave's, now at **age 31**, and it has now been asked four times without being answered.

## THE ARC

#271 built a decision surface and ruled nothing on it: 115 rows of harvested criteria from
thirteen external design systems, wired into a page with per-row controls, notes and an Export
JSON. #272 is the session where that surface came back **full**, and the whole day is one motion —
**get his decisions out of a browser and into the store without a single sentence of ours being
mistaken for one of his.**

Four beats, in order, each one a commit.

### 1 · The opener asked two questions and got two answers (`42a3f4d`)

The first question was the **"256" clause** — #271 had carried it deliberately uninscribed
because a sentence that reads like permission is the most dangerous kind to inscribe from a wrap
seat. His answer set three figures at once, and it is now **`s272-D93`**: **180,000 is the
WORKING figure**, an overrun to **~220,000** is tolerated without alarm, **256,000** stays hard.

⛔ **The code constants were NOT touched.** `_gauge_tokens.STOP_LINE_TK` is still `180_000` and no
new arm was wired. That restraint is the point: he ruled the *posture*, not an *enactment*, and
turning a tolerance into a gate arm is a behavioural change a session may not make on an
inference. **Whether ~220 becomes a named arm, and at what tier, is the ONE question #273 opens
with.**

The second answer — *the sheet is in progress, he was going through the last 31* — set the shape
of the whole day: **wait for the export, build the machine that eats it while waiting.**

That machine is `knowledge/_cut_harvest_rulings.py`: export JSON in, proposed rulings + a
when-patch + a review page out, **12 selftest arms including a quote-gate mutation**, and
`--inscribe` that **refuses without `--ratified`**. Two findings came out of building it, and
both came from driving the real thing rather than reading it:

- **The export schema was derived from `exportObj()` and then CONFIRMED by driving the real page
  in chromium.** Reading the generator was not treated as knowing the artefact.
- **Row family is keyed by `data-sec`, NOT by id prefix** — lane-B ids are bare `B-nn`, so a
  prefix parse would have mis-filed a whole family silently.

And one defect in the v2 sheet was found and fixed **by addition**: a note typed **under 400 ms**
before a reload or close was **lost**, because the only flush was on a debounce. Flush now also
fires on `focusout` and `beforeunload`. ⚠ **That defect ran in the artefact he was actually typing
his decisions into.** It was caught before the export, not after — but the honest reading is that
a data-loss bug sat in a decision surface for a session and nothing tested for it.

### 2 · The cut, on the real export (`d1af846`)

His export came back **115/115 decided — 104 ratify · 3 option · 8 decline · 0 later** — and was
saved verbatim at `notes/_lanes/272/harvest-decisions-2026-09-14.json` before anything read it.
His **19 non-empty notes** were transcribed verbatim into `DAVE-RULINGS-2026-09-15.md`, which is
the single `says` source for the cut.

The cut produced **92 proposed rulings**, a **15-row when-patch**, **8 undecided** (the declines)
and a review page rendered at 1280 and read on sight.

**Two changes to the cutter were made here, both by addition, and both are the interesting part:**

- **"Ratify" on a CONTESTED row means the lane's recommendation becomes the `ruled` text.** A row
  where the harvest lanes disagreed is not made undecidable by a one-word ratification; the
  recommendation is what he ratified, and the ruling says so.
- **A NOTE-ABSENT `says` is written as `"ratify — NOTE-ABSENT; accepted by click: …"`.** ⛔ This is
  the clause that stops the whole exercise from becoming a forgery. **79 of the 92 rows carry no
  note at all** — he accepted them with a click. The cutter's first instinct was to REFUSE those
  rows for want of a quotable sentence. **Dave overrode that** (*the cut page, his word*), and the
  compromise is that a click is recorded **as a click**, never dressed up as a quote. ⚠ **A ruling
  whose `says` is a click is a weaker artefact than one whose `says` is a sentence, and the store
  now contains 79 of them; that difference is visible in the record because the `says` names it.**

### 3 · The inscription (`b46ea90`)

On his *"were good, inscribe"*: **`_rulings.json` 469 → 562**. Every entry went in through
`_inscribe_ruling.py --write` after **92/92 clean dry-runs**; `_governs.py --selftest` green.

Then the 15 unanimous `when` predicates onto the component metas — and **this is the day's near
miss**. ⛔ **The FIRST attempt reformatted 15 meta files.** That is the **#179 class**: a
`json.load` / `json.dump` round-trip that preserves meaning and destroys the file. It was
**reverted and redone by TEXTUAL SPAN** — 12 predicates inserted, 3 replaced on the charts,
**15 insertions / 3 deletions total**, with a parse-and-diff proof that **only `when` moved**.
`_validate_kg.py` OK.

*Why it matters beyond the diff:* the rule *"never `json.dump` a meta"* is written in three
places and was still nearly broken, by a seat that had read it. **The proof, not the rule, is what
caught it** — a parse-and-diff run before the commit, which is cheap and was not skipped.

Finally, the eight declines and the noted follow-ups became **`P-272-1`…`P-272-4`** in
`knowledge/_parked.json`, on his *"lets make sure we return"*:

| | sidequest | tripwire |
|---|---|---|
| **P-272-1** | LIST vs CARD — when does a list item with columns become a card, or a list-card hybrid | `list-items.meta.json`'s next commit |
| **P-272-2** | MODAL TAXONOMY — Lightbox / Dialogue / Modal / Feature launcher | `modals.meta.json`'s next commit |
| **P-272-3** | NAVIGATION STRATEGY — mega-menus, IA, tabs-are-not-navigation | `navigations.meta.json`'s next commit |
| **P-272-4** | the ten smaller opens (pie, bento, date-range picker, notifications, steps, …) | the next dream pass |

⛔ **A decline is a SIDEQUEST, not a ruling, and none of the eight was inscribed.** P-272-1 is the
one with the most rows behind it — four.

### 4 · The handoff, written before the wrap (`5df4ead`)

`_HANDOFF-123-the-cut-and-the-inscription.md`, written by the conductor at **FILL ≈175,000 real —
UNDER the 180,000 working line** — before delegating this ritual. That is the first handoff in
four sessions cut under the stop line rather than past it, and it is a direct consequence of
`s272-D93` being answered at the opener rather than at the wrap call.

## WHAT THIS SESSION GOT WRONG, OR NEARLY DID

1. **The 15-meta reformat** (above) — caught by a proof that was run, not by a gate.
2. **The v2 sheet's sub-400ms note loss** — a data-loss defect in the surface his decisions were
   being typed into, found late.
3. **The cutter's NOTE-ABSENT refusal was the RIGHT instinct and the WRONG answer.** Refusing 79
   rows would have thrown away decisions he had actually made. The repair was not to relax the
   rule but to make the record carry the difference. ★ **The general form: when a discipline would
   discard something true, change what the record SAYS, not what the discipline FORBIDS.**
4. **A stale `.git/index.lock` from 2026-09-14 22:51** blocked the first commit and needed the
   sandbox delete permission. Third occurrence of the class.

## WHAT IS STILL OPEN AND IS HIS

Written as **QUESTIONS PUT** (`s271-D4`), not as states of the world:

- **The ~220 tolerance ENACT** — does it become a named arm, and does it ever block? `s272-D93` is
  a ruling about posture and enacts nothing. **One word at #273's opener.**
- **The 8 declines** (B-10, B-20, B-22, R-A-09, R-A-10, R1, R11, R15) — parked, not ruled.
- **The four sidequest SHAPES** — the list-vs-card definition, the modal vocabulary, the nav
  strategy, and which of the ten smaller ones goes first.
- **`s271-D2` / `s271-D4` blocking tier**, the **three explorer hues**, the **`roles.json` drift
  (108 vs 24)**, **door v2**, the **Common Toolkit specs into `_INGESTION-QUEUE.md`**, all of
  handoff-121 § D's remainder and **every #119 open**, unchanged.

## THE ONE-LINE FINDING

**A click is a decision and a sentence is a quote, and the store now distinguishes them by
construction** — 13 rulings carrying his words, 79 carrying a named click, and not one sentence
of ours presented as his.
