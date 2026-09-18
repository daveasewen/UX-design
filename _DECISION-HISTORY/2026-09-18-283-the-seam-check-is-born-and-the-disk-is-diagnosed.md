# #283 — the seam check is born and stops its own session; the disk is diagnosed

provenance: 283 · 2026-09-18
status: observed

*Both-way links: spine entry `_LIVE-STATE.md` § ⏱ LATEST DELTA — 2026-09-18 (**#283**) · ledger
`knowledge/_rulings.json` § `s283-D1` (`107aa44`) · handoff
`_HANDOFF-134-the-seam-check-is-born-and-the-disk-is-diagnosed.md` · his words
`notes/_lanes/283/DAVE-RULINGS-2026-09-18.md` · the wrap's own filed report
`notes/_subreports/2026-09-18-283-W-wrap.md`.*

⚠ **This is the WHY and HOW. The WHAT — the ruling, the spans, the figures — lives in the ledger and
the spine and is not re-inscribed here.** Lands whole, dated from `date`, never silently edited after.

---

## 1. The session opened with a promise, and the promise became a ruling in one exchange

#282 had closed **81,559 past the hard line with the gauge unread between the logo review landing and
the last ruling** — the third breach, and the first where the instrument was not consulted at all. The
conductor opened #283 by offering, unprompted, to read the gauge at every lane seam and say the number
in chat. Dave's answer was five words: *"can we do this in every session"*.

That is the whole arc of the ruling. What is worth recording is the **shape of the question he asked
back**: not *is the number right* but *is this a habit*. The same thing happened again ten minutes
later on scratch hygiene — the conductor offered to clear scratch before the masters lane, and he
answered *"good, maybe we make this a regular check- more mechanical"*.

⇒ **Two offers, two identical replies, one ruling.** `s283-D1` folds both into a single instrument
(`knowledge/_seam.py`) because they were answered with the same instinct: a thing worth doing once at
a seam is a thing worth doing at every seam, and a thing done by judgement is a thing that will be
skipped on the day it matters. **The dead end avoided here was building two scripts** — a gauge
reader and a scratch cleaner — which would have been two things to remember instead of one.

⚠ **It is ADVISORY, and that was deliberate.** The conductor did not arm it. `s271-D2` makes
`FILL_CEILING_BLOCKING` Dave's, and a session that arms its own stop line is grading its own homework;
`s283-D1` says so in its own text.

## 2. The instrument fired the same day it was born, and the correction it forced was to stop

At turn 43 the seam check read **210,476 real** and printed the verdict against the three lines. The
next thing on the plan was the per-size logo masters — 40 SVGs, the one lane specified well enough to
need no conversation, and the thing #283 was opened to do.

**The lane was not cut.** That sentence is the session's result.

⚠ **Recording it honestly means recording what it is NOT.** It is not proof the instrument works: n=1,
and a single obeyed advisory is a data point. It is not an answer to the standing question of what a
session should DO at the hard wall — that question is Dave's and is put for the fourth wrap running.
And the session still closed **6,084 outside the ≤220,000 tolerance**, so the check did not keep the
window clean; it kept the window **under 256,000**, which is the first time in four sessions.

★ **The thing worth carrying forward is the inversion.** For three sessions the failure mode had been
migrating away from the instrument — crossed under pressure (#277), read and overruled (#281), not
read at all (#282). #283 is the first counter-example, and it cost the session the work it was opened
to do. **That price is the evidence, not a complaint about it.**

## 3. The disk: a long-held belief was half wrong, and the half that was wrong was ours

Dave asked *"I thought we had fixed the VM problem before, can you check"*, and later, more pointedly,
*"we've been through this exact problem before and fixed it"*.

**He was right, and the record agreed with him**: the #227/#228 scratch fix held — `/var/tmp` was
empty and the hygiene gate had been doing its job every wrap. The dead end was assuming that because
the old cause was fixed, the new fill had the same cause.

It did not. **The repo itself was 9.3 GB on a 9.8 GB disk.** The breakdown is in the spine; what
belongs here is how it was found and what it says:

- **`.git` at 2.6 GB with a 63 KB pack** is not a git problem, it is a **symptom of the index-lock
  class this project has been carrying as a runbook line for months**: 28,991 loose objects never
  packed, and **745 `tmp_obj_` stubs** — the debris of interrupted writes under a mount that refuses
  `unlink`. The disk story and the git-lock story are the same story seen from a different end.
- **A 2.5 GB asset zip duplicating a 2.5 GB directory**, both gitignored, is the ordinary kind of rot
  that no gate looks for because no gate was ever pointed at bytes.

**Dave fixed it himself, on his own Mac, instructed step by step** — his own framing: *"you'll have to
instruct me im not a terminal ace pilot"*. Two Finder moves and one Terminal line. The measurement
after is in the spine: repo 4.3 GB, `.git` 576 MB, garbage 0, photography originals kept.

## 4. And then the disk did not release, which is the finding that matters

After a full application restart — VM `uptime` one minute — `/sessions` still read **9.1 G used, 136
MB free**, with the same 127 dead session directories present.

The diagnosis: **`/sessions` is a persistent ext4 volume, and every session AND every sub-lane leaves
a `drwxr-x--- nobody:nogroup` home behind it** — unreadable and unremovable from any session uid, with
no `sudo`. At ~38 MB each (pip installs, tokenizer caches) the 127 of them hold ~4.8 GB. Rebuilds
appear to trigger at 100%, not on a schedule.

⛔ **This is not fixable from inside the sandbox and not fixable from his Mac.** Writing that plainly
is the point of the section: three sessions of this project have now spent time on a disk problem
where **the only two available actions are to report it to Anthropic or to wait for a rebuild**. The
one thing that changed today is that the next rebuild is now worth ~5 GB of headroom instead of 500 MB,
because the repo shrank.

**The one lever inside was pulled** (`85aee08`): our own lanes' home residue is now cleaned at wrap.

## 5. A closed collision, and the claim that closed it a session early

#282 measured two runbook steps in direct collision: step 4c's `--clean` deleted `/tmp/gitshim`, which
step 5 depends on under this mount. `85aee08` put the shim on the gate's KEEP list, and **this wrap
verified it at 4c rather than taking the commit message's word for it** — the gate printed
`/tmp/gitshim  → KEPT (keep-list)`.

⛔ **But #282's filed report states the collision *"is now in `_CARRIES.md`"*, and a probe of
§ `residual → #283` at this seat finds no item mentioning `gitshim` or step 4c at all.**

★ **That is the lesson of the section, and it generalises:** the 2c EXIT CHECK tests PRESENCE for
items it can see, and an item that was never written is invisible to it. A wrap may state that it
homed something, and nothing checks that it did. The collision survived one wrap on a claim, and is
closed today only because the conductor happened to fix it from a different direction. It is minted as
a carry now, *after* it closed, so the record of the near-miss survives the fix.

## 6. What this session got wrong about itself

**The fill.** 226,084 real over 53 turns — 6,084 outside tolerance — in a session that cut no lanes and
ruled once. The conductor named the cause rather than leaving it to be inferred: **one
`git count-objects -vH` printed 745 `tmp_obj_` garbage lines, roughly 60K real, that should have been
piped through `grep`.** A diagnostic command run without a filter cost more than a quarter of the
window's overspend. ⚠ **That is a measurement, not a rule** — nobody ruled anything about piping, and
this dossier is not the place to invent one.

**The boot.** 80,871 real, n=1, **+10,077 on the floor and the eighth post-diet reading over the
70,000 ceiling.** It is not a re-base and the literal is not raised; cutting the boot is Dave's.

## 7. Resolved state, and what is still open

**Resolved:** `s283-D1` is ruled, built, selftested and enacted in two commits; the rulings page is
fresh in the ruling's own commit; the 4c/step-5 collision is closed and verified; the repo's own half
of the disk problem is fixed and measured.

**Still open, every one of them a question put and not a state of the world (`s271-D4`):** the 40
per-size logo masters (#284's first move, unstarted by ruling) · the third dial · the theory door and
the three postures · `col26-012` · **the disk's platform half, and whether the seam's "no render lane
over 90%" becomes blocking** · the boot ceiling's eighth reading · what a session does at the hard wall
· the four generators that would undo hand-authored state · the git-lock runbook line · the
instrumentation-append policy.

**Six inherited blocking gate fails stand, carried in the `#243` declared not-a-wrap form for the
ninth consecutive wrap.** They are another session's append-only testimony and a wrap may not repair
them.
