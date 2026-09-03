# #243 — the stub's first boot: the reading came in under, the six controls were ruled rather than patched, and the skills prune turned out to be a wall

```
provenance: 243 · 2026-09-03
status: observed
```

*Spine entry: `_LIVE-STATE.md` § `## ⏱ LATEST DELTA — 2026-09-03 … #243`. Ledger: `knowledge/_rulings.json`
§ `s243-D1`. Banner: `GOOD-MORNING.md` § ★ LATEST #243. Reports:
`notes/_subreports/2026-09-03-243-lane-Q-six-controls.md` (+ its Q2 ADDENDUM) ·
`notes/_subreports/2026-09-03-243-V3-six-controls-verifier.md` · `notes/_subreports/2026-09-03-243-wrap.md`.
Review surface: `_REVIEW-six-controls-reading-2026-09-03-v1.html`. Both-way: each of those files names this
dossier's session.*

*This is the WHY and the HOW. The WHAT — the ruling text, the arm counts, the boot figure — lives in the ledger,
the reports and the `#### 2026-09-03 #243` stratum, and is not restated here except where the reasoning needs it.
Written by the delegated wrap sub from the conductor's brief and the filed reports; every figure attributed to
the conductor's seat is his DECLARED figure, and the wrap did not re-derive it.*

---

## 1. The session opened on a measurement, and the measurement was the whole point

#242 had changed exactly one thing that a cold boot pays for — `MEMORY.md` became a progressive-disclosure
stub under `s242-D1` — and it changed it *after* its own first turn. So #243's opener was the first turn that
would ever carry the stub, and residual → #243 carry ② said what to do with it in advance: read the first-turn
`message.usage` figure before anything else loaded, put it beside #242's, and let nothing else vary.

That is what happened. The reading came in **3,575 real under** #242's. Lane F had predicted the stub alone
would buy about 2,150 — but lane F's number is **tape** (tiktoken cl100k) and the reading is **real** tokens,
and the two are not converted into each other in this repo by ruling. So the honest statement is not "the
stub over-delivered" but "the stub was the only thing we changed, the boot fell by more than the stub's own
measured size in a different unit, and the excess is unattributed." The A/B design worked; the attribution
question it opens is carried, not answered.

Why the reading is stated once. `s241-D2` S5 puts a session's boot figure in its stratum and nowhere else,
so that the read chain does not carry the same number three times. This dossier obeys that: the figure is in
`GOOD-MORNING.md` § `#### 2026-09-03 #243`, and this file says only what it meant.

## 2. The six controls: why they were left red until ruled, and then rewritten rather than widened

Lane F at #241 wrote seven green controls to prove the polarity receipt worked. Under #239's Q3 — *a node may
not name its own oracle* — six of them, written in the LITERAL shape, are correctly refused. Lane P at #242
showed that every one has a legal form under `s240-D3` (cite the ruling id that made the node, or retire rows
instead of deleting them) and asked Dave which of three things to do: (a) leave the literal shapes red and
make the legal forms the migration path, (b) widen Q3 so a node may cite an oracle it names, (c) rule the six
controls retired.

The conductor's judgment was to leave them red and put the question to Dave by eye rather than by prose:
`_REVIEW-six-controls-reading-2026-09-03-v1.html` shows the three receipts side by side and the three options
under them, in the two-red law's colours. A hosted publish was REFUSED — a first publish needs an approval
this session could not obtain — so it stayed a file at the repo root, where the ruling's `says` field now
names it. Dave's response was a question and then a word: *"So the recommendation is that we leave them red
until they are ruled, could we rule them now?"* — then "yes" to the conductor's wording. The wording became
`s243-D1`: *a card may not name its own witness; #239 Q3 stands unchanged;* the six are rewritten to their
legal form as permanent named green arms, each paired with its literal shape as a red arm, so the proof they
were written to give is kept and the refusal that caught them is kept too. Options (b) and (c) are rejected
in the ruling text. The four UNRULED escapes are out of scope by design — the ruling says so, and they stay
his.

Why (a) and not (b). Widening Q3 would have bought seven green lines at the price of the one clause that had
just proved it could catch a node inventing its own witness. The controls were never the product; the gate
was. Rewriting the controls to satisfy the gate, and keeping both shapes as arms, means the gate's selftest
now carries the exact attack that motivated the clause, permanently, with the refusal's name on it.

## 3. Build, verify, fix — the verifier in the same wave, a third time

Lane Q ported the six legal forms and five literal shapes into `_validate_polarities.py --selftest` as eleven
named arms: 137 → 148, 0 failures, `--check` green, brain files untouched. On its own report it would have
closed the item.

V3 was briefed in the SAME wave as Q, not after it — `s238`'s lesson, now applied three sessions running —
and it returned SATISFIED WITH FINDINGS. Two of the findings matter for how this repo tests things. **F2
(HIGH):** 235 LEGAL's "verbatim" phrase had been cut from the gate's *own* haystack rather than from the R1
file — the arm was green because it tested the code under test against itself; fabricate the haystack and it
stayed green. **F1 (MEDIUM):** the three `S-SOURCE` literals asserted only the family name of the refusal, so
removing the very clause `s243-D1` says stands left all three passing — the arms proved *that* the gate
refused, not *why*. F3 found a duplicate arm; F4 was framing; F5 was a correct non-catch.

Lane Q2 fixed all four in the same session, in the same file, and the interesting fix is the smallest one:
the arm frame gained an optional `must_detail` substring, so a red arm can pin the *clause* and not just the
family. That is a new mechanism in the test frame. It is small, it is mechanical, and it has no ruling behind
it — which is why the wrap carries it by name rather than letting it arrive as settled. After Q2: 150 arms,
0 failures, `--check` green, brain files byte-untouched, re-run first-hand by the conductor.

V3 also left one item it would not decide: Q5's verbatim haystack joins each register row's fields with a
single space, so a phrase that straddles two fields passes as "verbatim". None of the fifteen real stubs
depend on that; only the tautological arm did, and Q2 fixed the arm without touching Q5. Tightening Q5 is a
change to a refusal's scope, so it is Dave's, and it is carried in his words.

## 4. The skills prune is not a task, it is a wall — and that changes the carry's state, not its wording

`s242-D2` ruled the plugin-roster skills pruned from the boot, Dave's panel action, sequenced after #243's
reading so the two variables could be separated. #243 did the sequencing and then went to enact it, and the
enactment turned out not to exist.

Dave showed all three panels. His Skills panel lists five; the Plugins panel shows every plugin disabled; the
Connectors panel shows two. The boot nonetheless ships `docx`, `pptx`, `xlsx`, `pdf`, `schedule`,
`setup-cowork`, `explain-usage`, `consolidate-memory`, `import-memory` and two `cowork-plugin-management`
skills. The mounted skills directory is read-only, has twelve entries, and mixes his skills with harness
built-ins. `gtb-brand` is in his panel and not in the boot. There is no toggle for any of the ten. Presence in
the boot proves *shipping*, not *enablement* — the same finding #242 made about the computer-use block, and
the same class the repo already names: a gate that cannot pass in one environment.

What this does to the carry is the part worth writing down. The carry said "ruled and NOT DONE, Dave's panel
action". That premise is now false — no panel does it — but the ruling is not retracted and the item is not
closed: it is ruled and unenactable here. So the carry is *corrected with a receipt* and *not struck*. Under
`s183-D1`/`s188-D2` a carry's wording changes only to record a correction, and the correction must name the
session that proved it and where it is inscribed; that is what the #244 line does, with the original text
kept verbatim after the receipt. The ruling itself is write-once and was not touched. Lane F's "~900 movable
tape" is recorded as not movable by us.

## 5. The cloud toggle: one variable, set up and deliberately not read

Mid-session Dave disabled the Claude-app setting "Cloud code execution and file creation", which the app
labels *Required for skills*, and left network egress on. Nothing observable changed in #243 — the Cowork
sandbox was already alive and kept its twelve mounted skills — so the effect is unknown, and #243 did not try
to measure it, because a mid-session reading would have been contaminated by everything already loaded.

#244's A/B is therefore that toggle alone: read the first-turn boot against #243's reading, and check whether
`dave-voice`, `swiss-design-system` and `dream-pass` still appear in the boot's skill list. If they vanish,
revert — the setting is labelled as the thing skills need, and a cheaper boot with no skills is not the
outcome anyone wants. Nothing else changes before that reading. Whether the toggle stays off afterwards is
Dave's.

## 6. The ceiling arm fires at this wrap, and the wrap could neither pass it nor should have

#242's stratum predicted this in so many words: its boot of 70,710 was 710 over the `s241-D1` ceiling of
70,000 on the ceiling's first morning, and because both boot checks read `notes/_GAUGE-LOG.md` only, the
breach would fire by name at #243's 2f roll, when the #242 stratum reaches that file.

It did. `boot_constant_drift_check` has two arms. ARM 2 (the derived band) has a legal declared form — the
`boot-drift DECLARED` line #242 wrote — because a band step is something a session can honestly state. ARM 1
(the ceiling) has none: the number is shrink-only by Dave's ruling, the gate's own text says the remedy is to
cut the boot and never to raise the literal, and it says raising it is not a price a wrap may pay to unblock
itself. The wrap agrees. About 89% of the boot is harness by #242's decomposition; the wrap cannot cut it, and
the literal is not the wrap's. So the wrap gate is red at this seat on a true statement about #242's morning,
the red is declared in the stratum with the gate's exact text, and the commit is made over it with the gap
named — which is what this repo does with a red it cannot honestly clear. The #243 reading is under the
ceiling and reaches the log at #244's roll, one wrap behind, exactly the lag the #242 wrap report named as its
RULING-SHAPED 2.

## 7. What the wrap did not do, and why each was declined rather than skipped

No push: the brief did not authorise one and runbook step 5 is Dave's GitHub Desktop, so the commit sits
local and says so. No memory write: step 3 is the conductor's and he did it. No `_build_all.py` and no
`--selftest` re-drive: fenced, and over the sandbox call wall. No CI read-back: four pushes are now owed at the
capped route and none was read here. `_lanes.json` was not repaired: it is the conductor's surface and the
stale step is carried. Nothing was ruled, re-worded, re-dated or re-stamped; no constant, band, ceiling,
floor, stop line or wall moved. Each of these is in the stratum's declared-skips line with a size, because
"skipped" reads as housekeeping and a size reads as what it is.

## Resolved state

`s243-D1` inscribed, store 335 → 336, read back. The six controls are permanent named arms in both shapes;
V3's four findings are fixed; the selftest is at 150/0 and the brain files never moved. The stub's first boot
is read and stated once. The skills prune is recorded as unenactable from any panel and its carry corrected
with a receipt. The cloud-toggle A/B is set up for #244 as the single variable. Open, and Dave's: the four
escapes, `BOOT_BAND_SIGMA`, diet S2/S3/S4/S6, the `SCHEMA-LOOSENED` word, V3's Q5 question, whether the toggle
stays off, `must_detail` as a frame mechanism, and what a ceiling arm should mean when it fires on a boot no
seat can cut.
