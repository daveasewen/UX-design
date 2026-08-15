# #183 — the brackets were ages, and both queued checks landed

provenance: s183 · 2026-08-16
status: observed

*Session #183 (ran 2026-08-15; this wrap crossed midnight and every stamp is taken from `date`,
which read `Sun Aug 16 00:34 BST 2026`). FABLE conductor + TWO OPUS build subs + this OPUS wrap sub.
Dave away after ruling **"we can still crank"** + **"go for it"**, scoped to Claude's lane only.
⛔ **NO RULINGS** — `knowledge/_rulings.json` was not written and not opened for edit.*

Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #183 · banner: `GOOD-MORNING.md` ★ LATEST #183.

---

## 1. The date, first, because a date is the small thing a record gets confidently wrong

The wrap opened on 08-15 and finished after midnight. The ritual's step 1 is explicit — *"take the
date from running `date`, never from the session's own belief"* — and the T-D12 precedent it cites
is exactly this shape: a handoff that self-dated a day out while its commits said otherwise. So the
whole wrap is stamped **2026-08-16** and the discrepancy is written down rather than smoothed.

One consequence worth carrying: the first **scheduled** dream-pass fires **2026-08-16 07:10**, which
is now *later the same day*, and it is the event that opens `s182-D1`'s counting window. This wrap
did not touch the scheduler.

## 2. Build sub A: a lane whose correct output was nothing

The carried residual read *"THREE REAL DEFECTS, PRICED AND UNBUILT — `[50]` · `[55]` · `[118]`"*,
and the brackets had been read as identifiers for several sessions. They are **ages**.

The probe was a walk back through `_GM-ARCHIVE.md`: the same three items appear at birth as
`[45]`·`[50]`·`[113]` and step **+1 every session** — which is precisely what the 2c step's own
age-format rule mandates. Nothing was wrong with the notation; the reading was wrong, and the
reading had been carried forward as a fact.

That is the class *"premise ages faster than rule"*, with a twist: here the premise was not stale,
it was never true — a misparse of our own convention, propagated by copy-forward. The conductor
wrote the memory hook `banner-brackets-are-ages.md` in-window so it cannot recur.

Having dissolved the IDs, the sub priced each real item, and **all three turned out to be Dave
calls, not build work**:

1. **The `#168`/`#168-A` `canon.css` comment.** Premise expired: it was already deleted by the
   generator and committed at `76b024c` (#174). It is recoverable verbatim at
   `git show 76b024c^:knowledge/canon/canon.css`, lines 4123–4133 — but restoring it re-inserts
   superseded hexes. So the open question is not "restore the comment", it is **adjudicating the
   #174 deletion**, which is Dave's. Both `gen_canon_components.py --check` and
   `gen_theme_cascade.py --check` are rc=1 today.
2. **The `--status-*` fall-through.** By the record's own words this needs Dave's eye — and
   `_LIVE-STATE-ARCHIVE.md:112` records the edit as *already shipped at #174*. So what is open is
   his eye on a **shipped** change. Reading it as unbuilt work would have produced a second edit on
   top of the first.
3. **The `#158` help-gate preamble port to the 8 package copies.** Re-priced, and the old price was
   wrong: a verbatim port **breaks all eight** with `ModuleNotFoundError: _helpgate`, because
   `_helpgate` does not ship. The genuine close is a **release** change — ship `_helpgate.py`, add it
   to `KNOWN_FILES` at `_validate_package_delta.py:85-86`, update `_MACHINERY-MANIFEST.md`, rebuild
   dist. A package is a release, so that is Dave's word. `_validate_package_delta.py` measured rc=1,
   8 failures, 6 lines each at that point.

**Why this is a good outcome and not a wasted lane.** Three items that read as agent work were
returned to the one person who can dispose of them, each with the coordinates that make the disposal
cheap. The alternative — building against a misread premise — would have restored a superseded hex
block and broken eight package copies.

## 3. Build sub B: both queued checks, built and driven

### (i) The `[112]`/`[107]` read-chain gate

The defect, found at #173: `_gen_chain.py --check` reports **STALE** in CI for a reason that has
nothing to do with staleness — CI can only reach the `tape (cl100k ESTIMATE)` tier because the real
measurement path is gitignored, so it can never byte-match a chain stamped `real`. Worse, the
comment in `gates.yml` asserted the gate refuses on the estimate fallback. It did not.

The fix, +137 lines in `knowledge/_gen_chain.py`: a `stamped_tier()` helper and a **COULD-NOT-ASK
clause inside `check()`, placed BEFORE the byte compare**, exiting non-STALE whenever the reachable
tier differs from the stamped tier — and **naming both tiers**, so the output says what it could not
ask rather than merely that it declined. An unreadable stamp is COULD-NOT-ASK too. `write()` was
deliberately left untouched, so offline generation still works.

Two things about the tests are worth recording:

- **The mutation arms mutate the STAMP, not the fallback.** Forcing the fallback would exercise a
  path that is unreachable at the point where the defect actually lives — a mutation that proves a
  clause nobody executes. Mutating the stamp drives the real branch.
- **The remedy was quoted, not re-invented.** `notes/_receipts/2026-08-14-s173-ci-triage.md` already
  carried the price: *"(c) is the recommendation… ~8–12K"* and *"fetch-depth: 0… ~2K"*. Reusing the
  priced record keeps the estimate a measurement of the earlier analysis rather than a fresh guess.

`.github/workflows/gates.yml` gained +43: `fetch-depth: 0` on both checkouts (the second, independent
cause of the CI divergence — `git show <sha>:` cannot work at depth 1), and the lying comment
replaced with the mechanism written out.

Proof: HEAD's copy of the script says STALE; the new code says COULD-NOT-ASK; **same tree, same env**.
That control is what makes it an attributed diff rather than a hopeful one.

### (ii) The evidence-format enforcement check

`s177-D1` ruled *no evidence pointers into rolling files* and the rule had no machinery. It has some
now: `knowledge/_governs.py` +62 (`ROLLING_FILES` + `rolling_target()`, enumerating the ruling's own
three files) and `knowledge/_inscribe_ruling.py` +68 (refusal `R6`, 8 selftest arms).

It was driven on **real data** — `s171-D1`'s actual evidence string — which returned rc=3, refused;
the cured form was accepted; and `_rulings.json`'s md5 stayed `0f9490e7…` throughout, so nothing was
written while proving a writer.

**The deliberate omission.** It is **not** wired into `_governs --selftest`/render. Wiring it would
turn the **11 ratified `_governs` fails** red — a ratified record outranks a later audit — so the
check exists at the inscription boundary, where new writing happens, and leaves the historical
corpus alone. The selftest output was proven byte-identical to confirm the omission is real.

**And one hollow claim, declared.** `s177-D1` says the check was *"PRICED"*. There is no number
anywhere on the record. It was searched for, not found, and no number was invented to fill the gap.

## 4. What the conductor re-ran, and the pitfall it caught

The conductor did not replay the subs' banners; it re-ran the receipts itself, unpiped:
`_gen_chain.py --selftest` rc=0 (all bites) · `_gen_chain.py --check` rc=0 FRESH ·
`_inscribe_ruling.py --selftest` rc=0 (all arms) · `_rulings.json` md5
`0f9490e7bf6876bfef2fd11eed2cf506`, unchanged.

One live pitfall: a `/tmp` redirect failed *Permission denied*, which made a selftest read come back
rc=1. **That rc belonged to the redirect, not to the test.** Re-run clean. This is the `/tmp`-class
trap the commit runbook already names — a shared path, a write failure that does not stop the chain
— appearing in a third tool.

## 5. Resolved state, and what is still open

**Resolved:** both queued checks are built, driven and green locally. The three "defects" are
dissolved as a class and re-addressed as three Dave calls with coordinates.

**Open, and new this session:**

- The **survey bucket is not wired** — no exit-code protocol for could-not-ask exists, so `[107]`
  still lands in CI's survey FAIL column. Close ≈ 4–6K (a picked number) **plus a ruling on the
  protocol**, which is Dave's.
- **Real CI is unproven.** Both fixes are proven locally only. Price of proof: the next push plus a
  run read-back, ~2K. The push is Dave's word and was not taken.
- **`[113]` package delta grew 6 → 143 lines** on `_gen_chain.py`'s two package copies. Deliberate —
  a package is a release — and 2 of the 8 delta findings are now this session's own.

**Open, carried:** the scaling call at tuner v2 (Dave's eye, #184's natural opener, wording
unchanged), the MONO-ONLY rider vs `s182-D3` contradiction, the trend card (floated), the compaction
five questions, and the long residual tail on the #183 banner.

---

*Links: `_LIVE-STATE.md` ⏱ LATEST DELTA #183 · `GOOD-MORNING.md` ★ LATEST #183 ·
`notes/_receipts/2026-08-14-s173-ci-triage.md` (the priced remedy this session spent) ·
`knowledge/_rulings.json` § `s177-D1` (the rule (ii) enforces — read, not written).*
