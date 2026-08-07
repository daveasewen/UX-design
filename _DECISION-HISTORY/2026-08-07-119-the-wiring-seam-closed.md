# #119 — The wiring seam closed, and the build that had not run since #116

provenance: local_857be5fa (cowork session, Fable conductor, low effort) · 2026-08-07
status: observed

## The arc

#118 handed over one spec'd gate and one open ruling. Dave took both at the opener via
option-set: **(b) shrink-only ratchet** for the type gate (`s119-D1`), and the lane plan as
briefed — 3 Sonnet subs on bucket B, Fable conductor lean. His stated quota shape governed the
routing: ~14%/day all-models, ~7%/day Fable — Sonnet subs spend the former and spare the latter,
which inverts the usual delegation caution ([[delegation-cost-inversion-110]]: name which budget
binds; this session he named it).

## Finding 1 — the wiring gate worked on its first real drive, and what it caught was upstream

`_validate_wiring.py` (30 on disk · 28 wired · 2 exempt-by-name) went green with 4 mutation
bites. But WIRING it into `_build_all.py` required route rows — and running the build to prove
the wiring revealed **the build had been aborting at `check_routes` since #116**: the a11y
selftest step was registered with no route row. Registered-but-unroutable is the same class as
built-but-unwired, one seam further down. Nothing caught it for three sessions because the wrap
gate does not run the build (documented at 2g's WHY) and nobody ran it by hand.

## Finding 2 — three more pre-existing reds were stacked behind the abort

With the route rows added, the build advanced and found, in order: `_governs.py` selftest red
(string `evidence` iterated char-by-char producing 2,282 phantom fails · 21 rulings born without
`status` · `commit <sha>` pointers with no legal form, reported as rot — the
[[honest-refusal-needs-a-legal-form]] shape, fixed by teaching the checker `git cat-file`
verification rather than mangling the record; clause mutation-tested with a fake sha). Then the
commit-seam harness red on fixture drift (`SESSION_N` demanded since #116, fixtures never
updated) — **declared, not chased**; the build still aborts at step 14 and more reds may sit
behind it. That end-to-end green is #120's first job.

## Finding 3 — a sub report contained a false claim, and replay caught it

Sub B (ds-025) reported "no SKILL.md anywhere on disk" — it searched the wrong mount. Replay
also surfaced the real state: P1 is *"awaiting Dave's confirm to open"* (`_DS-IMPROVEMENTS.md:1748`),
so item 10 was mis-filed as agent work in the #118 bucket sort — exactly the risk the sort itself
declared (9 of 17 sorted unprobed). Sub A's headline (CTRL regex retired at `2a231f9`) and Sub C's
(noise-floor trio isolated; its cited basis sessions were never recorded) both verified on replay.

## Dave's opens created or advanced this session

P1 confirm-to-open (asked, unanswered) · G4 ratify of the enacted §C OFFLOAD (216→162 by
addition, 10 blocks homed verbatim in `_GM-ARCHIVE.md` § ⬛ OFFLOADED #119) · recorder-constants
refresh (isolation now done for him).

## Still open

Commit-seam fixtures · build end-to-end · repair-or-retire `_validate_screen.py` /
`_validate_state_contrast.py` · item 13 stale-queue close at `_DS-IMPROVEMENTS.md:676` ·
stale-mount seam (gate or retire).

Ledger: `knowledge/_rulings.json` `s119-D1` · spine: `_LIVE-STATE.md` ⏱ #119 · banner: GM ★ LATEST #119.
