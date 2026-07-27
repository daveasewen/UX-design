# 2026-07-27 — Memento hardening: the M-set (session #17)

provenance: local_1564cbbc-76e2-4d02-86a7-70254a6f5af4 · 2026-07-27
status: ruled — `notes/_MEMENTO-DECISIONS.md` § ★ M-SET (+ M7 closure + routing amendment)

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST #17 · enactment: `notes/_briefs/2026-07-27-memento-hardening-brief.md`*

## The arc

**Opened as the §C·2 ruling batch; Dave reframed it inside ten minutes.** His words carried the whole
brief: *"we must get this memento system running as efficiently as possible"* · *"it has to be
robust… there may be problems with the process external to the GM too"* · *"I need to rest assured
that I have a reliable system I can share with others"* — then the diagnosis, sharper than my probe
plan: *"very tight context windows, tasks overrunning and not being caught, and lots of going round
in circles correcting work repeatedly… running in red just makes a godawful mess."* And a second
worry with a date on it: the dream pass fires unattended for the first time THIS Sunday.

**Method: verify current truth first, then classify the day's papercuts, then propose.** Gates and
instruments run cold (build 62/62 · wrap gate 0 FAIL 2 WARN · tiktoken missing AGAIN — the #16 wart
recurring on schedule); today's seven session records + the gauge log swept for failure CLASSES
rather than incidents; the dream-pass lane audited end-to-end (task prompt → runbook → dreamer spec).
The classification that shaped the set: each papercut is either **fixed mechanically** (gated),
**fixed by discipline only** (fragile — works until a tired session), or **unfixed**. The M-set is
everything in the second and third columns, ranked by distraction-cost.

**Live specimen, mid-session:** Dave, looking at the sign-off panes parked an hour earlier, asked why
a "faulty view-as-table pattern" solved on bar and donut was still showing. Grep receipts: the solved
`dv-tbl-toggle` button lives on bar ×5 / line ×2 / combo / donut ×2; sparkline (:148) and scatter
(:163, :230) still carry the old bare `<details>` idiom. Nothing gates cross-sibling pattern
consistency — a refinement adopted by four charts silently left two behind. That is "going round in
circles" caught in the wild, and it became M4 (port + ADR-0013 partial + ratchet).

## The three beats worth remembering

1. **The M7 read-back.** My own recommendation (hard cap on §A) crossed Dave's recorded verbatim from
   #14 — *"not even a guard banner"* — and the blanket "all of these seem good" would have inscribed
   the contradiction silently. Caught at inscription because the ledger was READ before being written
   to. Read back, I withdrew the block half myself: a §A block would FORCE the trim the §A invariant
   forbids — the STAND-004 two-gates-opposite-structures class, rebuilt by hand a day after we cleaned
   it up. Final shape (Dave: *"agreed"*): **WARN-only, growth-triggered** — silent at steady state so
   it cannot wallpaper, loud when §A grows unnamed, never blocks.
2. **Routing reversed on trust, recorded as both beats.** The ruled split sent enactment to Sonnet
   (mechanical lane, per canon). Dave, minutes later: *"be careful and precise I don't trust sonnet,
   it cant think on its feet"* → enactment window is **Opus solo, effort MAX**, no Sonnet subagents;
   the brief gained a STOP condition per item so nothing is improvised on canon.
3. **M1 applied to its own birth window.** RED=wrap-only was ruled mid-session; the AMBER crossing was
   announced at ~44% and the in-window list trimmed on the spot (M11/M12 edits moved to the brief).
   The rule's first enforcement was on the session that wrote it.

## What is deliberately NOT fixed

Fill remains self-report — no gate can see a context window; M1 converts running-on in Red from a
judgment call to a rule violation, which is the strongest available move, not a mechanical one. The
2e retirement tests stay semantic; M9 adds a mechanical PROXY (removed line ⇒ archive presence) and a
dreamer hunt, not enforcement. The dream pass's conductor model stays unpinned by design.

## Wrap findings of its own

The §A hash convention had to be RECOVERED mid-wrap: a wrong-shape probe hashed `\n# §A`→`\n# §C` and
read `70e61b93…`; the recorded `999b1e3d…` = lines `# §A` → line before `# §C`, joined + trailing
newline. `git diff HEAD` = 0 proved §A unchanged before any retry — measure, don't guess, applied to
our own guard. The convention is now pinned in the brief (items 5 and 11) for M5's mover. One script
abort total, nothing written — the all-or-nothing design working.

## End state

M1/M2 live in gauge canon · M3–M12 specified in the brief with STOP conditions · M7 closed WARN-only
growth-triggered · dream-pass verdict: governance watertight, blast radius = one floated file + one
local commit, promotion physically Dave's; residual = the never-fired scheduled path (Dave fires it
supervised before Sun 08-02) · §C·2's 15 rulings + dataviz sign-off parked, unchanged, still owed.
