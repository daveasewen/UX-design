# #223 — the release day: five undecided plan items became eight rulings and a reproducible zip

provenance: 34fc1aea-f1d0-421b-aa40-8da929f080ca · 2026-08-28
status: observed

*Spine entry: `GOOD-MORNING.md` ★ LATEST #223 · `_LIVE-STATE.md` ⏱ LATEST delta #223.
Ledger: `knowledge/_rulings.json` § `s223-D1` … `s223-D8` — every id READ from the store at this
wrap, never retyped from a brief. Commits: `5efd667` · `004ddc9` · `6afab15` · `14af4d7` ·
`bff12fe` · `e33ea1b` · `a91b7e0` · `36abde7`, all eight pushed, subjects read back from
`git log`. Filed reports: `notes/_subreports/2026-08-28-223-browser-gate-third-state.md` ·
`…-223-delta-arm2-repair.md` · `…-223-hitarea-classifier.md` · `…-223-version-ratify.md` ·
`…-223-classifier-narrow.md` · `…-223-bake-v102.md` · `…-223-d8-enact-and-bake.md`.
Artefact: `apollo-spider/dist/Apollo-Spider-v1.0.2.zip`.*

---

## The arc in one line

#222 ended holding a plan with **nothing in it decided**. #223 put all five decisions to Dave in
one sitting, sent seven subs at the enactments, and baked — and the two most consequential
rulings of the day (`s223-D6`, `s223-D8`) **did not exist when the day was planned**. Both were
born because a sub stopped and reported instead of finishing.

## Finding 1 — a plan's value is that it makes the decisions *nameable*, not that it decides them

The #222 deliverable was deliberately a plan and not a bake. That looked, at the time, like a day
that had not landed anything. What it actually bought was that #223's opener could be a **single
decision surface with five items on it**, each with its own evidence quoted, rather than five
separate negotiations interleaved with five separate enactments.

Dave answered all five in one exchange. Four of the five answers were the recommendation; **one
was not** — `s223-D4`, the blind delta-gate arm. The conductor had priced repair at ~20K and
**recommended parking it**. Dave ruled repair, before the bake. That is worth recording precisely
because the record would otherwise show a smooth day: the conductor's judgement was overruled on
the one item where the cost was real, and the repair then **disproved its own brief** — the shim
was assumed to differ from source by one declared optional import, and five of twelve ported names
differed. Parking it would have shipped a gate that was BELIEVED rather than a gate that BITES
[[instrument-without-a-consumer]].

## Finding 2 — the ratification hole was the day's quiet one, and it is the one that generalises

`RATIFY_ID` was pinned to a single hard-coded id — `s219-D10`, Dave's word for **v1.0.0** — so
every future manifest read `RATIFIED` and `--release` would have waved any bake through without
ever asking him. Nobody had noticed because the machine's output was *correct-looking*: a manifest
that says RATIFIED, on a cut nobody ratified.

`s223-D3` re-keys the check **per cut**. The consequence is mechanical rather than ceremonial: at
the bake, v1.0.2 sat at `PROPOSED` and the gate refused, and it kept refusing until `s223-D7`
existed in the store. **v1.0.2 is the first cut ever to pass through that gate.** The general
form is the standing one — an unenforced convention is not a convention, it is a preference — and
this instance is unusually clean because the *enforcement* is what made Dave's word load-bearing.

## Finding 3 — the fence held, and that is why there are eight rulings and not six

The bake sub's brief carried an explicit fence: *if the released zip's sha differs from the
dry-run sha, STOP and report — do not rationalize.* It reached that fence, and it reached it the
cheap way: by measuring the release's sha with a consequence-free `--dry-run` **before** writing
anything into `dist/`, rather than discovering it afterwards.

The mismatch was real, mechanically necessary and fully explainable — ratifying flips a `status`
string inside the packed `_MANIFEST.json`, whose sha256 is stamped into `PROVENANCE.json` and
`README.md`, so **the act of recording Dave's word was the act that moved the bytes**. Explaining
it is exactly what the fence forbade treating as permission. The sub committed nothing.

On the way it found a second thing nobody was looking for: `apollo-spider/FIRST-SESSION.md:51`
still sent a v1.0.2 designer into an `Apollo-Spider-v1.0.1` directory — **step one of the very
Copilot first-session that is this cut's acceptance test**, caught only by an advisory gate and
not declared on the go/no-go page Dave had looked at.

Both findings came back ruling-shaped. Both became `s223-D8`: the literal fixed **inside** the cut
with his bake word carrying to the new sha, and the ratification stamp **moved outside the zip**.
The packed manifest now ships status-free and ratification lives repo-side only, so a released zip
byte-matches its dry-run twin again — proven at the bake with a **forced-PROPOSED control**, which
is the part that makes it a measurement rather than a claim.

## Finding 4 — a number that moves twice in one session is a symptom, not a value to pick

The roster went 55 → 56 (found at #222) → 60 (after `s223-D5`'s exit-77 arm) → **58 (ruled,
`s223-D6`)**. The middle move is the interesting one: teaching the classifier that an honest
`COULD-NOT-ASK` refusal means NEEDS-DEP swept two gates into the ship list that refuse for a
**repo** resource — `notes/_claims` — which no designer machine will ever hold. The remedy was not
a tuned number but a structural narrowing: `_unshipped_subject()`, shared with the pre-existing
REPO-BOUND fence, so NEEDS-DEP means *a dependency the designer can install*. **58 is derived by
that predicate, not chosen to land on 58.**

The dead-end worth recording: the first instinct was to read the drift as a regression in the
gates. It was not. It was the ship list correctly reflecting a classifier that had just learned a
new state and had no way to tell two kinds of missing thing apart.

## Finding 5 — a ledger seed that would have looked like compliance

`s223-D2`'s letter asked for the ledger re-seeded in the same commit as the version bump. The
version sub drove `--seed`, **measured what it produced**, and found a false row: version `v1.0.2`
over a surface holding no v1.0.2 zip, which additionally makes the laundering arm go red at the
bake. It restored the ledger byte-identical to HEAD and returned the deviation as a ruling-shaped
question rather than committing a true-looking falsehood. `s223-D5`(3) then ruled the general
form — **the ledger seeds at the bake, not at the bump** — and the seed landed at `a91b7e0`.

## Finding 6 — the one red that is not ours

The CI read-back was finally done, in Dave's own Chrome, and it did not find the failure everyone
expected. **No job has run since #442.** Every run since #443 is a three-second instant death
carrying GitHub's own words: *“recent account payments have failed or your spending limit needs to
be increased.”* Eight commits pushed at #223, **zero CI verdicts**, and the carried claim that the
read-back was *blocked at the browser* is now struck with its receipt.

This is worth the paragraph because the shape recurs: a queue was owed for weeks, the blocker was
assumed to be the last known blocker, and the actual blocker was one screen away and of a
completely different kind [[premise-ages-faster-than-rule]].

## What is resolved, and what is still open

**Resolved.** All five #222 plan decisions (`s223-D1`…`D4`, `s223-D7`) · the roster count
(`s223-D6`, 58 for this cut) · the ratification no-op (`s223-D3`) · the blind delta arm
(`s223-D4`) · the version-literal class and the stamp-inside-the-zip defect (`s223-D8`) · and the
bake itself: `apollo-spider/dist/Apollo-Spider-v1.0.2.zip`, 19,850,657 B, sha256
`3a7fe297140862b7…`, ledger row seeded `v1.0.2`, frozen-release gate 3 arms PASS, `--check` GREEN.

**Open, and Dave's.** His fifteen minutes in Copilot on the v1.0.2 pack — still the only real
proof, and now unblocked · the CI billing remedy, and with it every owed verdict · three
`Memento — Gumdrop v1.0.0` literals shipped unruled · whether the delta arm's body audit widens to
`measurement_tier` / chain (b) · and the un-parking of `W-217`, the bento sitting, the mutation-arm
call and the mono dark chord, now that `s222-D3`(2)'s *until baked* condition has been met.
Nothing here un-parked any of them.
