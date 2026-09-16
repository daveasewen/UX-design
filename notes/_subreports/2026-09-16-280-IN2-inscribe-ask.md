# LANE IN2 — REPORT — five more twins landed, jade-lifestyle left open, the generator keeps his answers

#280 · 2026-09-16 · opus seat · his ASK export read WHOLE and followed over the conductor's reading.
Everything below was RUN, not recalled.

---

## For Dave — in plain words

**Five of your six answers are in the library, the sixth is still yours, and the machine that writes the
library now reads your answers instead of wiping them.**

You answered the six questions the page put to you. Five of them named a twin, so those five are now the
default drawing for their base, with your own words kept beside each one. The sixth — **jade-lifestyle** —
you left open, so nothing was written down: no default, no drawing on the mislabelled list. What you wrote
about it (*“jade-lifestyle-active-2 - think is the most likely the correct icon”*) sits on the empty slot in
your words, so the record carries your lean without anyone turning it into a decision.

**Landed (5):**

1. **electricity** — `electricity-active` is the twin; `electricity-active-2` (the smiley) is written down
   as its own icon that needs an inactive version drawn.
2. **employee-banking-solution** — `…-active-2` is the twin; `…-active` goes down as a **name** problem
   only: the right drawing under the wrong name, so nobody owes it an inactive.
3. **financial-health-check** — the same shape.
4. **reward** — the same shape.
5. **traditional-chinese-medicine** — `…-active` is the twin you named, and you said the pair is mislabelled
   while `…-active-2` is the correct icon. Both went down: the pair as a name problem, `…-active-2` as its
   own icon that needs an inactive drawn.

**Still yours (1):** jade-lifestyle.

**And the thing worth your word from last time is fixed.** The last report said that if anyone regenerated
the icon store your answers would be wiped. They would not any more: the generator now reads your two
export files — the sheet and the question page — and rebuilds your fourteen answers from them every time it
runs. If the store ever records an answer your exports do not, it refuses to write anything and says so,
because an answer changing under the record's feet is a question for you, not something to overwrite. A test
rebuilds the real library and proves all fourteen come back with your own words and none go missing.

**One number:** fourteen of the fifteen bases are now settled; one is open.

---

## 1. His export against the conductor's reading

`notes/_lanes/280/inscribe-active/DAVE-EXPORT-ask-2026-09-16.json` (2026-09-16T20:23:15.692Z), read whole.
Six answers, the same envelope as the #279 sheet plus the ASK page's own `choice` vocabulary.

| base | his `choice` | his `twin` | his `flags` | his note, verbatim |
|---|---|---|---|---|
| electricity | `note` | `electricity-active` | `electricity-active-2` | electricity-active-2 - mislabeled |
| employee-banking-solution | `name-only` | `…-active-2` | — | employee-banking-solution-active - mislabeled |
| financial-health-check | `name-only` | `…-active-2` | — | financial-health-check-active - mislabeled |
| jade-lifestyle | `open` | null | — | jade-lifestyle-active-2 - think is the most likely the correct icon |
| reward | `name-only` | `…-active-2` | — | reward-active - mislabeled |
| traditional-chinese-medicine | `tick` | `…-active` | `…-active-2` | correct twin, but mislabeled.<br>traditional-chinese-medicine-active-2 - this is teh correct icon |

**The JSON agrees with the conductor's reading on all six**, including the two shapes worth naming: rows 2–4
are NAME defects (`name-only`), not missing-inactives, and row 6 is both — the pair is a name defect and
`…-active-2` is its own icon. Nothing in the brief had to be overridden. Two smaller notes:

* The brief says the `ruled` ledger goes **19 → 24**. It does not: `ruled` was **9** and is now **14**,
  `unresolved` 10 → 5, and the two ledgers still sum to the **19** rows the file has always owned. The 19 in
  the brief is that sum, not the ledger.
* The close condition on `W-280in` expected a file called `DAVE-EXPORT-ask-active-2026-09-16.json`. His is
  `DAVE-EXPORT-ask-2026-09-16.json` — same page, same envelope, and the receipt on the closed row says so.

## 2. The edits to `knowledge/_icon_nodes.json` — textual spans, as lane IN did

`_inscribe2.py`, importing lane IN's own span helpers so the blocks it replaces are the blocks that file
wrote. No regenerate was run against the tree.

1. **Five `defaultActive` edges** — `"t": null` → `"t": "icon:<his twin>"`, `$note` untouched, `$ruled`
   added naming him, the twin, **his `choice`**, the export and its timestamp.
2. **Five rows leave `unresolved` for `ruled`** carrying `t`, the candidate list, `his_note` verbatim,
   `his_flags`, **`his_choice`** and the export path. `unresolved` 10 → 5, `ruled` 9 → 14.
3. **jade-lifestyle keeps its null** and gains two fields on the edge — `$open` (why nothing is drawn, in
   his own answer's terms) and `$his_note` (his words verbatim) — and the same two on its `unresolved` row.
   It is the one row in the file whose emptiness carries his voice.
4. **`edge_types.defaultActive`** and **`$description`** re-stated for 14/15 and for the generator change.
5. **Lane IN's nine now-false sentences repaired** (`--repair-stale`): each of its nine edges said
   *“gen_kg_icons.py still declares this edge a null, so a regenerate would drop his answer.”* That stopped
   being true in this lane, and a false sentence in the store is worse than none. Nine spans, nothing else
   on those edges touched, and a selftest bite asserts the claim is gone from the file.

`git diff --numstat`: `knowledge/_icon_nodes.json` +97 −54, `knowledge/_ICON-GAPS.md` +18 −1.

## 3. The defect list — his answer, not a reading of it

A second section in `knowledge/_ICON-GAPS.md`, immediately before the `-active` convention section, with a
**What is wrong with it** column the first section did not need, because his answers now distinguish two
defects. The rows are DERIVED from his note line by line: a line that calls something wrongly labelled and
NAMES a drawing is a defect on that drawing (own icon if he ticked it, name-only if he did not); the same
line naming no drawing is a defect on the pair the question was about — which is exactly how
`traditional-chinese-medicine` produces both of its rows without a single base name being typed into the
script. Six rows, his words verbatim (including his typo), plus a paragraph for jade-lifestyle that quotes
his lean and says nothing was written down from it. Lane IN's stale paragraph — *“6 rows of his review are
not on this list yet”* — was replaced by a pointer to the new section.

## 4. The generator — his exports are now an INPUT

**The fix to lane IN's finding F1.** `gen_kg_icons.py` no longer treats `defaultActive` as null-only:

* `DAVE_EXPORTS` names the two export files (the #279 sheet, the #280 ASK page). `dave_exports()` reads the
  ones that exist and sorts by each file's own `exportedAt`; `dave_answers()` merges them so a later export
  wins the base outright — **including when the later answer is `open`, which revokes the earlier twin
  rather than leaving it standing.**
* `dave_reads()` returns his twin or `None` **and the reason**. A sheet answer (`choice: "twin"`) is
  re-read with the same three regexes lane IN's classifier uses: a note that fights its own ticks is not
  his sentence and is never drawn. An ASK answer (`tick` / `note` / `name-only`) is a direct answer to that
  row's own contradiction, so it settles it by construction. `open`, a missing twin, or a twin that is not
  one of that base's drawings: nothing drawn, and the record says whose decision that was.
* `build()` draws the edge with a `$ruled` sentence and appends a `ruled` row; an answered-but-open base
  keeps its null and carries `$open` + `$his_note`; a base he has never seen keeps the plain B4 null.
* The payload gains `$ruled` + `ruled` (icon file only) and an `edge_types.defaultActive` line that counts
  what he has settled and names what he has not.
* `--land` gains a **cross-check**: if the file it is about to overwrite records a `ruled` answer this build
  does not reproduce, it REFUSES, names the rows, and writes nothing.

**Why the exports and not the `ruled` ledger — the choice the brief asked me to make and say.** Both carry
the same fourteen answers. The ledger, though, lives inside the very file `--land` overwrites: it survives a
regenerate only while a previous output happens to be on disk in the tree being regenerated. A run with
`--corpus` pointed elsewhere, a rebuild from a clean checkout, or a dry run into an empty directory would
find no ledger and silently drop his answers — which is the exact failure being fixed. The exports are
inputs under `notes/`, this script never writes them, and they are his own words at source. So the exports
are the authority and the ledger is a cross-check, which is what the `--land` refusal above is.

**Proved, not asserted — `--land` was NOT run for real.** Three new bites:

* **bite 20** — a mini corpus with mini exports, five arms: his clean answer is drawn and lands in `ruled`
  with his words; a later `open` REVOKES it and keeps his words on the null; a sheet row whose note fights
  its ticks is not drawn and the reason says so; a twin that is not one of the base's drawings is not drawn;
  an `open` answer with a twin left in the envelope is not drawn either, and the record calls it his choice.
* **bite 21** — `--land` twice into a mini corpus: the second write is **byte-identical** to the first, so a
  regenerate keeps his answer; then the landed ledger is edited to name a different twin and `--land`
  REFUSES, leaving the file exactly as it found it.
* **bite 22 — the live tree.** It rebuilds `knowledge/` from his two exports in memory (nothing written) and
  asserts all **14** answers come back with the same twin, the same `his_note` and the same `his_flags`, that
  the 15 `defaultActive` edges match the landed file target for target, that **none is dropped**, and that
  `jade-lifestyle` is still a null carrying his note. In an isolated copy of the file with no tree around it
  (the mutation harness) the bite asserts that absence explicitly instead of passing quietly.

Measured against the live tree by a dry run into scratch: `defaultActive` resolved **14**, declared nulls
32 → 18, `dave_defaultActive_open == {"jade-lifestyle": …}`.

## 5. Gates — every line run at this seat

```
$ python3 notes/_lanes/280/inscribe-active/_inscribe2.py --selftest     → 11 bites, SELFTEST PASS
$ python3 notes/_lanes/280/inscribe-active/_inscribe.py  --selftest     → 13 bites, SELFTEST PASS
$ python3 notes/_lanes/277/icons-propose/gen_kg_icons.py --selftest     → 22 bites, SELFTEST PASS
$ python3 notes/_lanes/277/icons-propose/_mutate.py <scratch>           → BASELINE PASS · ALL MUTANTS CAUGHT (32, 0 survivors)
$ python3 knowledge/_validate_kg.py                                     → OK, rc 0
```

`_inscribe2.py` carries one bite per base he settled (each asserting five things at once: his twin is the
default, the `activeVariantOf` edges stand, the null is retired, his words + his `choice` survive, and his
drawing is on the defect list in his words), one for the open row, and four on the file as a whole.

**Lane IN's selftest was repaired, not left to rot.** Its bite *“the 6 asked rows are untouched”* would be
a lie after this lane, so it is now scoped by his second export: the rows he settled must be **ruled**, the
rows he left open must still be byte-untouched nulls. Same for its ledger bite. It reads his ASK export
where it sits; without that file it behaves exactly as before.

**The new bites can go red.** Four mutants were added to `_mutate.py` and lane IN's `M5` re-anchored onto
the rewritten loop, all caught: M5 *a base he has NOT answered is drawn anyway* → bites 3, 13; M29 *his
exports are not read at all (the pre-IN2 generator)* → 20, 21, 22; M30 *the exports merge newest-first, so
the sheet overrides the answers he gave after it* → 20; M31 *`--land` stops cross-checking* → 21; M32 *a
sheet row whose note fights its ticks is drawn anyway* → 20. Bite 21's setup is wrapped so a mutant that
breaks it turns the bite red instead of killing the harness — the file's own rule.

## 6. Findings

**F1 — the landed file and a regenerate agree on every answer and differ in prose.** Compared field by
field after a dry run: the 14 `ruled` rows match on `t`, `his_note`, `his_flags`, `note` and `why`, and the
15 edges match target for target. Two cosmetic differences remain, and a future `--land` would tidy them:
the generator adds `$his_note` / `$his_flags` to a drawn edge and `his_choice` to its ledger row, while lane
IN's nine hand-written rows carry `flagged_as` instead; and the `$ruled` sentences are worded differently
(the landed ones name the lane that inscribed them, a regenerated one names the export it was read from).
No answer of Dave's is affected either way, which is what bite 22 asserts.

**F2 — `_validate_icons.py`'s twin arm is now wrong on 8 of 14, not 5 of 9.** Lane IN's F2 stands and grows:
its `active_names` arm assumes the bare `-active` is the twin, and on the fourteen settled bases the bare
form is NOT the twin on eight (contact-chat-ai, dentist, renew, user-staff, withdraw-overpayment,
employee-banking-solution, financial-health-check, reward). Not touched here.

**F3 — the explorer still does not draw `defaultActive`** (`ASSET_DRAWN` in `_build_kg_explorer.py`, lane
LY's file, untouched). Fourteen resolved defaults are now in the store and invisible on the graph. Lane IN
raised this at nine; it is a question for whoever owns the explorer, not this lane.

**F4 — jade-lifestyle is the only open row, and it has a lean, not a default.** His note names
`jade-lifestyle-active-2` as *“the most likely”*. That is one word short of an answer and it stays one: the
edge is null, the base is in `unresolved`, and his sentence rides along in `$his_note` so the next lane can
put a one-row question to him rather than a fifteen-row sheet.

## 7. What was not done, with size

* `--land` was not run for real, by the brief. The proof is bite 21 (a real `--land` twice into a mini
  corpus, in a temp dir) and bite 22 (an in-memory rebuild of the live tree). Zero risk carried.
* The ASK page driver (`_drive_ask.py`) was not re-run: the page is answered and the driver asserts an
  unanswered page's DOM. Small.
* No screenshots; nothing was rendered in this lane. `/sessions` is at 99% and all scratch is removed.
* `_LIVE-STATE.md` / `_CHAIN.md` banners are the wrap's, not a build lane's. Small.

## 8. Files

| path | what |
|---|---|
| `knowledge/_icon_nodes.json` | 5 defaults landed, jade's null given his words, ledgers 10/9 → 5/14, 9 stale sentences repaired (+97 −54) |
| `knowledge/_ICON-GAPS.md` | the second-pass defect list, his words verbatim, own-icon vs name-only (+18 −1) |
| `notes/_lanes/277/icons-propose/gen_kg_icons.py` | reads his two exports, draws only what he named, `--land` cross-check, bites 20–22 (+394 −14) |
| `notes/_lanes/277/icons-propose/_mutate.py` | M5 re-anchored, M29–M32 added (+20 −6) |
| `notes/_lanes/280/inscribe-active/_inscribe2.py` | the span edits, the defect derivation, the stale-sentence repair, the selftest |
| `notes/_lanes/280/inscribe-active/_inscribe.py` | its selftest scoped by his second export (+24 −6) |
| `notes/_lanes/280/inscribe-active/DAVE-EXPORT-ask-2026-09-16.json` | his export, as received |
