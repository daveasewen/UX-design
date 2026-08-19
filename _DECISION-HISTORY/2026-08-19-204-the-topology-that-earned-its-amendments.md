# #204 — the topology that earned its own amendments

```
provenance: 204 · 2026-08-19
status: observed
```

*Narrative dossier per capture-ritual step 1b — the WHY and HOW, not the WHAT. The terse records
are elsewhere: the ruling in `knowledge/_rulings.json` (`s204-D1`), its ONE home in
`notes/_briefs/2026-08-19-204-mechanisation-programme-v1.md`, the session record on
`GOOD-MORNING.md`'s ★ LATEST banner, the state delta in `_LIVE-STATE.md`, and the receipts in
`notes/_receipts/2026-08-19-204-*.md`. Both-way links: this file is named on the ★ LATEST banner
(item ⑯) and on the `_LIVE-STATE.md` ⏱ LATEST delta.*

---

## 1 · What the session was licensed to do

`s203-D2` did not order a topology. It licensed a **trial** of one: a Fable conductor holding
judgment only, an Opus **build-PM** owning a build wave, an **adversarial verifier-PM** whose
whole job is to disbelieve the builder, and a return of numbers at the wrap so Dave could rule on
whether the shape is worth keeping. The distinction between *adoption* and *permanence* was set
before the first sub was seated, and it is why this session ends with a ruling and still leaves an
open question.

The forward brief carried the usual DO-NOT-RULE fence. What it could not carry — because nobody
had run the shape yet — was any prediction of where the shape would break.

## 2 · Four seats, and the failure each one produced

The trial ran with four seats, and the useful part is not that it worked. It is that **each of the
four amendments Dave attached to the adoption traces to a specific failure the trial itself
produced**, in the window, with a receipt.

**The build-PM (131,688 tk, 58 calls)** built six of the seven briefed P2 components — Popconfirm,
Footer, Layout-utilities, Document-row, Payment-card-visual, Runway-bar — plus a lane-1 CI repair,
and then **died of a connection loss at roughly minute 43, at the exact moment it was writing its
claim table**. The build survived on disk; the *account* of the build did not. That is the trial's
one lossy hop, and it is the whole argument for **amendment ①, the incremental claim table**: a
claim table written at the end is a claim table that can be lost entirely, and the work then has to
be re-derived by a second agent from artefacts rather than read from a record.

**The finisher (136,326 tk)** did exactly that re-derivation, from receipts, into
`notes/_receipts/2026-08-19-204-buildpm-claim-table.md`. Its own contribution to the amendment list
came from something else. Re-running the gates, it found that a `/var/tmp` redirect was serving **a
foreign session's stale gate output as this run's evidence** — two gates read RED off months-old
numbers. Re-run under `mktemp`, both were green. This is the same shape the repo has already been
bitten by twice: the stale-msgfile trap in `_RUNBOOK-git-commit.md`, and the stale-ops-file trap at
the capture runbook's step 2c. A shared `/tmp`-class path, a fixed name, and a read that *succeeds*
against the wrong file. The failure mode is not an error; it is a confident green measured on
somebody else's artefact.

**The adversarial verifier-PM (113,224 tk, 48 calls)** returned 34 CONFIRMED, 3 CONTRADICTED, 12
UNTESTED and 4 NEW findings, every one grounded in
`notes/_receipts/2026-08-19-204-verifier-challenge-table.md`. The single most valuable thing it did
was catch **itself**: it cited a search it had not run, claiming two hits where the real count was
thirty-five. It reported that. **Amendment ③, run-before-cite**, is that self-catch turned into a
rule. It also adjudicated the row-91 Transaction "gap" as a **false gap** — Transaction ships inside
List-items as `type:"transaction"` and was promoted by Dave on 2026-06-22 — which is the same
premise-ageing class #203 hit at scale.

What the verifier could **not** do is look at anything. No browser was driven this session, so the
visual conformance of all six new components is the builder's word and nothing more. **Amendment ④,
the verifier render lane**, exists because the verifier's teeth stop at the DOM it never rendered.

**The fix sub (100,182 tk)** closed all three contradictions — three metas schema-conformed against
a 92-meta sweep, duplicate ids repaired across three review pages, a missing `W-43` store row added
through the store's own writer — and appended its addendum to the claim table. That the repairs
happened *inside the same session as the challenge* is **amendment ②, the fix loop inside the
build-PM mandate**: a challenge table that leaves its contradictions for the next session is a
backlog generator.

## 3 · The number that actually answers Dave's question

The trial's return is five numbers, and they are on the banner because that is where he rules from.
The one that matters most is the third: **481,420 sub tokens across four subs**, against #203's
**2,170,761 across twelve**. The topology did roughly a fifth of #203's delegated spend and returned
six gated components, a challenge table with real contradictions, and four amendments that came
from observed failures rather than from imagination.

The honest counterweights are in the same list. The conductor's own window still ran past the
advisory stop line (~155K against 150,929), so the shape did not make the conductor cheap. The
harness has **no agent resume** — `SendMessage` is unavailable here — so the finisher and the fix
sub were cold starts, paying a boot each for continuity the design assumes is free. And the
lossy-hop tally is one, on a trial of four seats, which is a rate worth watching rather than
dismissing.

None of this settles permanence. `s204-D1` adopts; the `s203-D2` verdict is a separate act and it is
still Dave's.

## 4 · What this wrap got wrong

The wrap sub ran `python3 knowledge/_build_all.py --list`, believing `--list` was a listing flag for
the build's step table. It is not a flag. `_build_all.py` accepts the unknown argument and **builds
anyway**; the run went partial and died at the call boundary, writing 33 files — 31 compliance rule
JSONs, `knowledge/compliance/graph-index.json` and `knowledge/_ASSERTIONS.md`, 412 insertions
against 1,464 deletions. That is the documented mid-build-intermediate signature, exactly as
`_RUNBOOK-git-commit.md` records it.

The repair was the documented one: `git show HEAD:<path> > <path>` for all 33, after which the
working tree was re-counted back to its exact 50-path pre-error state. Nothing was lost.

The part worth inscribing is not the mistake, it is where the mistake came from. **The ban is
printed in `GOOD-MORNING.md`'s own header** — *"DO NOT RUN `_build_all.py` TO CHECK — ANY PARTIAL
run strands the tree"* — in the very file this ritual spends its whole time editing. It was read
past in order to answer a question a `grep` on `_build_all.py` would have answered in one call. The
class is small and general: **a command with a standing ban invites a "harmless" invocation, and
`_build_all.py` has no argv guard to make the harmless invocation actually harmless.** That absence
is carried as a residual rather than fixed here, because building a guard at a wrap is exactly the
scope creep a wrap is supposed to refuse.

## 5 · Where it leaves the record

Adopted, amended, and mechanised on order: `W-44` and `W-45` are builds Dave asked for, `W-46` is a
scope-only lane and must stay one. Thirty-five review surfaces now sit under his eye, twenty-nine
carried from #203 and six new. Two CI gates — `[13]` and `[114]` — are still red by measurement, and
`[114]`'s threshold is a picked constant that no ruling has ever settled, which is why it is carried
as his rather than tuned by a wrap.

The trial produced its amendments the only way amendments are worth having: by failing in public,
in a window where somebody was watching.
