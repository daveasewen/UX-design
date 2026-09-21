# #293 lane DA — dream-pass enactment audit, passes 6–13 (plus pass 5)

session: `#293` · 2026-09-21 · lane `DA` (dream audit)
brief: dispatched in-chat by the #293 conductor, off Dave's *"we should probably look at the latest
dream pass, in fact some previous ones may not have been enacted."*
scope: READ-ONLY on git. No commit, no staging, no `.git/index.lock` touched. Two files written.
tokens: UNMEASURED — `_checkin.py` deliberately NOT run: it appends to `notes/_REHEARSAL-LOG.jsonl`
and `notes/_dream/_GRADE-DECISIONS.jsonl`, both counted datasets, and an audit sub must not move the
population it is auditing (the pass-6-P2 class, and the #226 digest sub's own precedent).

## WHAT WAS DONE

1. **Established the pass numbering from primary sources, and the brief was off by one.** The brief
   asserted `2026-08-08` = pass 6. Each proposals file states its own number in its first line:
   `2026-08-09-proposals.md` opens *"# Dream pass 6 — floated proposals"*, corroborated by
   `_DECISION-HISTORY/2026-08-09-137-dream-pass-6-triage.md` (*"Dream pass 6 fired on its scheduled
   Sunday 07:10 slot and committed `0219075`"*). `2026-08-08-proposals.md` calls itself *"Fifth
   pass"* in its own standfirst. **Published mapping:** 08-08 = 5 · 08-09 = 6 · 08-15 = 7 · 08-16 = 8
   · 08-23 = 9 · 08-30 = 10 · 09-06 = 11 · 09-13 = 12 · 09-20 = 13. Passes 6–13 are therefore the
   eight files 08-09 → 09-20, **39 proposals**. Pass 5's three are audited as an appendix because the
   brief named the file.
2. **Enumerated every `### P<n>` in all nine files** by grep, not by reading whole files.
3. **Searched for a ruling on each**, in four places: all **622** records in `knowledge/_rulings.json`
   (extracted by python — id/ruled/date/says[:260]/status[:200] only, never whole records);
   `notes/_MEMENTO-DECISIONS.md` (6,106 lines, grep only); every `notes/_lanes/*/DAVE-RULINGS-*.md`;
   and `_DECISION-HISTORY/*dream*`.
4. **Read the three prior enactment records** named in the brief: the #137 pass-6 triage, the #256
   DREAM-ENACT sub-report, the #226 pass-10 digest sub-report (the digest HTML itself was not
   re-read — the sub-report restates its content and the HTML is 45.8 KB).
5. **Probed the repo for each proposal's defect**, one probe apiece: `git log -S` on the relevant
   file for enactment shas, and a direct read/grep/run of the current artefact for liveness.
6. **Wrote two files**, nothing else. Tree otherwise untouched.

## FINDINGS

**1. Twenty-two of the thirty-nine are ruled and enacted with a commit behind them.** Passes 6, 7, 8,
11 and 12 were disposed of in full, usually within 24–48 hours of the pass firing. Pass 12 is the
best-served in the set: four proposals, four separate verbatim words from Dave at #271, all four
enacted the next day (`f4ad826f`, `b8024dec`).

**2. Exactly one item is RULED AND NOT ENACTED — pass 6 P1.** Dave firmed it at #186 on a full
read-back (*"Firm — ratify all"*, `s186-D2`), in a deliberately minimal shape: a re-checker that
counts the 21 frozen `#119 sweep` status strings at wrap, **no bulk rewrite**, because a bulk rewrite
manufactures the CLAIMED class ADR-0016 forbids. It was never built. Grep of `_capture_gate.py` and
`_governs.py` for any such arm returns nothing, and the count in the store today is still exactly 21.
36 days.

**3. Pass 9 has NO DISPOSITION RULING AT ALL.** Six proposals, and nothing in any of the four ruling
surfaces answers the pass as a pass. Three are dead by other events; three are still live. This is
the single largest gap the audit found and it was not previously recorded anywhere.

**4. Pass 13 is entirely unruled and every one of its seven defects is present today.** It fired on
schedule 2026-09-20 (`dcf17ade`, *"7 proposals floated, 0 ruled (scheduled fire; Dave absent)"*) and
three consecutive wrap briefs — #290, #291, #292 — record it as still unruled.

**5. The memory-grade (B3) question is the longest-carried class in the record: four passes, seven
proposals, and the instrument is now dead.** Pass 8 P4/P5 set the return dates (cost half after one
cycle, staleness half after five). Pass 9 P3/P4 said the cost half was due that morning with the
numbers ready. Pass 11 P1/P2 rebuilt the population. Pass 13 P1 found the grader has been blocked
since the #278 store move. Probe: `python3 knowledge/_gardener.py --refresh --dry-run` →
`⛔ GARDENER BLOCKED … expected /sessions/.../.auto-memory/MEMORY.md … REFUSING TO GUESS`. **Neither
return has ever been made** — one cycle elapsed 2026-08-23, five cycles elapsed 2026-09-20.

**6. Pass 11's two enacted gardener arms are now inert, and nothing declared it.** `population_delta()`
and `_HOOK_LINK_RE` were both landed with mutation proofs at `44c80619` and both are unreachable
today for the same reason as finding 5. The enactment record is correct; the world moved under it.

**7. `_checkin.py` has no staleness fence on the grades sidecar, and it is poisoning the dataset the
B3 review is owed.** The sidecar reads `refreshed_at 2026-09-13T07:11:34` over 52 hooks in a store
that no longer exists. `_checkin.py:1259–1300` prints whatever it finds and logs a row to
`_GRADE-DECISIONS.jsonl` regardless. The last three rows in that file are **byte-identical**:
`{"kind":"alert","lines":3,"chars":492,"tokens":153,…,"refreshed_at":"2026-09-13T07:11:34"}`. This is
pass 13 P1, confirmed three ways.

**8. `s276-D6`'s own removal condition has fallen due and nothing acted on it.** Dave's ruling:
*"it comes OFF at the next dream pass if the tripwire never fired."* The next dream pass was pass 13.
Nothing has ever run the guard, so the tripwire could not have fired. `python3
knowledge/_validate_wiring.py` reports **2 failures**, both orphans: `_validate_demo_page.py` and
`_validate_lane_ownership.py`. This is pass 13 P6, and it is the one still-live item that already
carries Dave's word — it needs enacting, not ruling.

**9. Pass 10's three unruled findings were digested onto a review page for Dave at #226 and then
never raised again.** All three probe live. P1 re-measured this morning with the gate's own three
regexes over all 363 filed reports: `COUNTS:` parses in 173 (48%), `REPLAY-THESE:` in 136 (37%),
the `RULING-SHAPED QUESTIONS` heading in 169 (47%). P2's `WRAP_COMMIT_SUBJECT_RE` at
`_capture_gate.py:5694` is byte-unchanged. P3 has **drifted**: `build_verdict_line()` now returns
*"75 of 144 steps green (#62, `18c7789`) — 69 steps have NEVER been in a green verdict"* — the
denominator moved with the codebase, the stale 75 did not. ⚠ `s125-D1`'s `watch` field forbids the
obvious fix by name: *"A future session 'helpfully' correcting 75 to 98 by hand would enact the
alternative Dave rejected, under cover of tidiness."*

**10. Pass 13 P5 has got worse in the one day since it floated.** The pass said three consecutive
suspensions; the #292 wrap (`GOOD-MORNING.md:487`) records a **seventh**: index at 44,909 B against a
49,152 B cap, `MEMORY-ARCHIVE.md` at 48,990 B with **162 B of headroom**. It was raised at #285, #286,
#287 and #288 and routed to "the dream pass" each time.

**11. Pass 9 P1 is the largest single counter in the record.** The pre-flight half of the
price-vs-actual dataset said `⛔ NOT CAPTURED` for 27 consecutive sessions when the pass floated it;
today `notes/_GAUGE-LOG.md` carries the same refusal from **#199 through #291 — 93 consecutive
sessions**, 185 occurrences in the file. The stated reason (*"a sub cannot measure the CONDUCTOR's
window"*) was already falsified by the `s214-D5` hand-over field when the pass said so, and the
#290/#291 entries now say outright that the conductor's gauge WAS read and simply not captured to a
file.

**12. Three pass-9 items are honestly overtaken rather than neglected.** P2 and P5 are both memory-
store claims and the store left the repo at #278 — the only copy of `git-push-method.md` in the tree
is the July snapshot under `_retired/`, and this seat cannot reach the live store. P6's specific
complaint is resolved: `s217-D1` is in `knowledge/_rulings.json` today. Its *general* complaint — a
wrap-time bare dirty count that never names what is in it — was never addressed by any ruling.

**13. Pass 5's three are all closed**, two enacted (#128, the first session in 52 to enact what the
lane dreamed) and one overtaken by `s225-D2`'s move of the carry list into the generated `_CARRIES.md`.

## RULING-SHAPED QUESTIONS

1. **Pass 6 P1 is ruled and unbuilt at 36 days.** Build the re-checker as ruled, or retire the ruling?
   It is the only RULED-NOT-ENACTED item in the audit and the smallest of the outstanding builds.
2. **Pass 13 P6 needs no ruling — it needs enacting.** `s276-D6` already says the guard comes off at
   the next dream pass if the tripwire never fired, and that condition is met. Delete
   `_validate_lane_ownership.py`, or exempt it by name with a reason and a date. The second orphan,
   `_validate_demo_page.py`, needs the same call and has no ruling behind it either way.
3. **Pass 9 was never put to Dave at all.** Its three live items (P1 pre-flight capture, P3 the
   staleness constant, P4 the overdue cost-half return) are 29 days old. Does pass 9 get a
   disposition sitting, or is it folded into the B3 review?
4. **The B3 return-with-numbers is owed on both halves and the instrument is dead.** Does the grader
   get re-pointed at the store's new home first (pass 13 P1 + pass 11's inert arms), or does the
   review go ahead on the data that exists?
5. **Pass 10's three unruled findings have been on a review page since #226.** They were digested
   precisely so they could be ruled by eye. Rule them, or retire them?
6. **Pass 13 P3:** the `size:` stamp calls its figure *"exact"*. Drop the word, or state the
   tolerance beside it? The #292 wrap iterated the figure to a fixed point and in the same sentence
   named two drifts it deliberately did not re-take the stamp for.
7. **Pass 13 P5 is a decision, not a repair.** Raise the archive cap or shard the archive — nothing
   else moves it, and truncating a verbatim move is not a move.
8. **Pass 6 P4's stamped expiry (~2026-11-06) is about six weeks out.** The token *scope* was left as
   Dave's security call and has never been proposed.
9. **Four sub-clauses were deliberately reserved and are not oversights** — pass 11 P1(b) and P4(a),
   pass 12 P2(b) and P4(b) — plus two picked-not-derived constants, `POPULATION_DELTA_THRESHOLD = 5`
   and `GRADE_AGING_DAYS = 30`, both explicitly Dave's at the B3 review.

COUNTS: proposals 39 (passes 6–13) · ruled+enacted 22 · ruled-not-enacted 1 · never-ruled-still-live 13 · overtaken 3 · pass-5 appendix 3 (2 enacted, 1 overtaken) · ruling-shaped 9 · probes run 24 · red 0

REPLAY-THESE:
```
# pass numbering + proposal census
for f in 2026-08-08 2026-08-09 2026-08-15 2026-08-16 2026-08-23 2026-08-30 2026-09-06 2026-09-13 2026-09-20; do
  head -1 notes/_dream/$f-proposals.md; grep -n "^### P" notes/_dream/$f-proposals.md; done

# rulings store: dream-related records, id/ruled/date/says[:260]/status[:200] only
python3 -c "
import json,re
d=json.load(open('knowledge/_rulings.json')); r=d['rulings']
for i,v in enumerate(r):
    if re.search(r'dream', json.dumps(v), re.I):
        print(i,v.get('id'),v.get('ruled'),v.get('date'),str(v.get('says'))[:260])
        print('  STATUS:',str(v.get('status'))[:200])"

grep -n -i "dream" notes/_MEMENTO-DECISIONS.md
grep -rn -i "dream" notes/_lanes/*/DAVE-RULINGS-*.md
grep -rln -i "dream" _DECISION-HISTORY/

# enactment receipts
git log --oneline -S"exclude)notes/_REHEARSAL-LOG.jsonl" -- knowledge/_git_commit.sh   # p6 P2  -> 08852b26
git log --oneline -S"boot reads:" -- knowledge/_RUNBOOK-parallel-conductor.md          # p7 P2  -> affb76fa
git log --oneline -S"STANDING CARRY LINE DISSOLVED" -- GOOD-MORNING.md                 # p7 P1  -> 2d2ff44c
git log --oneline -S"GRADE_WINDOW_OPEN" -- knowledge/_gardener.py                      # p8 P4a -> eaaee375
git log --oneline -S"s225-D1" -- knowledge/_release/_gen_pack_manifest.py              # p10 P4 -> ddc7821d
git log --oneline -S"population_delta" -- knowledge/_gardener.py                       # p11 P1a-> 44c80619
git log --oneline -S"_HOOK_LINK_RE" -- knowledge/_gardener.py                          # p11 P2 -> 44c80619
git log --oneline -S"_untracked_subjects" -- knowledge/_validate_screen.py             # p11 P4b-> 44c80619
git log --oneline -S"STOP_LINE_TK" -- knowledge/_gauge_tokens.py                       # p12 P1 -> f4ad826f
git log --oneline -S"FILL_CEILING" -- knowledge/_capture_gate.py                       # p12 P2a-> f4ad826f
git log --oneline -S"hook_open_items_recheck" -- knowledge/_capture_gate.py            # p12 P4a-> b8024dec
git log --oneline -S"2026-11-06" -- notes/_MEMENTO-DECISIONS.md                        # p6 P4  -> 5199b111
git log --oneline -1 dcf17ade                                                          # pass 13 commit

# liveness probes
grep -c "enactment state NOT asserted here (UNPROVEN by this sweep)" knowledge/_rulings.json   # p6 P1  -> 21
grep -rn "frozen\|119 sweep" knowledge/_capture_gate.py knowledge/_governs.py                  # p6 P1  -> no arm
grep -n "REHEARSAL-LOG" knowledge/_git_commit.sh                                               # p6 P2  -> :174
sed -n '98,112p' knowledge/_RUNBOOK-git-commit.md                                              # p6 P3  -> corrected inline
grep -n "all-dirty" knowledge/_git_commit.sh                                                   # p6 P5  -> kept
grep -n "boot reads" knowledge/_RUNBOOK-parallel-conductor.md                                  # p7 P2  -> :106
grep -c "NOT CAPTURED" notes/_GAUGE-LOG.md; grep -n "NOT CAPTURED" notes/_GAUGE-LOG.md | tail  # p9 P1  -> 185, #199..#291
grep -n "GRADE_AGING_DAYS" knowledge/_gardener.py                                              # p9 P3  -> :145, =30 provisional
python3 -c "
import re,glob,os
C=re.compile(r'^COUNTS:\s*(\S.*)$',re.M); R=re.compile(r'^REPLAY-THESE:\s*(\S.*)$',re.M)
Q=re.compile(r'^#{1,6}\s*RULING-SHAPED QUESTIONS\s*$',re.M)
fs=[f for f in glob.glob('notes/_subreports/*.md') if '_TEMPLATE' not in f]
n=c=r=q=0
for f in fs:
    t=open(f).read(); n+=1; c+=bool(C.search(t)); r+=bool(R.search(t)); q+=bool(Q.search(t))
print(n,c,r,q)"                                                                                # p10 P1 -> 363/173/136/169
grep -n "WRAP_COMMIT_SUBJECT_RE" knowledge/_capture_gate.py                                    # p10 P2 -> :5694 unchanged
cd knowledge && python3 -c "import _gen_chain as g; print(g.build_verdict_line()[:200])"       # p10 P3 -> "75 of 144 … 69"
python3 knowledge/_gardener.py --refresh --dry-run                                             # p11/p13 P1 -> GARDENER BLOCKED
python3 -c "
import json; d=json.load(open('notes/_dream/_MEMORY-GRADES.json'))
print(d.get('refreshed_at'))"                                                                  # p13 P1 -> 2026-09-13T07:11:34
sed -n '1255,1300p' knowledge/_checkin.py                                                      # p13 P1 -> no staleness fence
tail -3 notes/_dream/_GRADE-DECISIONS.jsonl                                                    # p13 P1 -> 3 identical rows
grep -rn "8,470" _CHAIN.md GOOD-MORNING.md                                                     # p13 P2 -> 4 sites
grep -n "size:" GOOD-MORNING.md | head -1                                                      # p13 P3 -> :15 "36,009 exact"
grep -n "ID_RE" knowledge/_state.py                                                            # p13 P4 -> :117 [a-z]{0,2}
grep -n "SUSPENDED FOR A SEVENTH" GOOD-MORNING.md                                              # p13 P5 -> :487, 162 B headroom
python3 knowledge/_validate_wiring.py                                                          # p13 P6 -> 2 ORPHANs
grep -rn "_near_dupes" --include=*.py --include=*.sh --include=*.yml knowledge/ .github/       # p13 P7 -> comment only
grep -n "add -A" knowledge/_git_commit.sh                                                      # p5 P3  -> :24 RETIRED
```

## FILES WRITTEN

- `notes/_lanes/293/DA/dream-enactment-audit.html` — the audit page: headline counts, a still-live
  leaderboard ordered by passes ridden, the verified pass-number mapping, and one table per pass
  (P# · plain-words subject · status + receipt · still-live probe · smallest enactment step), plus a
  pass-5 appendix and a riders section for the four deliberately-reserved sub-clauses.
  Swiss design system, accent `#DB0011`, hairline section rules, 1/3:2/3 dimension splits.
- `notes/_subreports/2026-09-21-293-DA-dream-enactment-audit.md` — this file.

Nothing else was written, staged or committed. `knowledge/_rulings.json`, `GOOD-MORNING.md`,
`_CARRIES.md`, `_LIVE-STATE.md` and `dist/` were not touched, no generator and no `_build_all.py` was
run, and the only git operations were read-only `log`.
