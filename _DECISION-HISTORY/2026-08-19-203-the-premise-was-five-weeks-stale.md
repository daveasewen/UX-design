# #203 — the premise was five weeks stale, and the push stopped being Dave's

```
provenance: 203 · 2026-08-19
status: observed
```

*Narrative dossier per capture-ritual step 1b — the WHY and HOW, not the WHAT. The terse records
are elsewhere: the ruling in `knowledge/_rulings.json` (`s203-D1`), the session record on
`GOOD-MORNING.md`'s ★ LATEST banner, the state delta in `_LIVE-STATE.md`, the twelve worker
receipts in `notes/_receipts/2026-08-19-203-*.md`. Both-way links: this file is named on the
★ LATEST banner (item ⑭) and on the `_LIVE-STATE.md` ⏱ LATEST delta.*

---

## 1 · The session that was planned, and the session that happened

#203 opened as a component build-out. The plan was two waves of six Opus subs against the
"P1 Foundations gaps" in `reviews/ITINERARY-2026-07-14-apollo-component-library.xlsx` —
eighteen components in wave 3a, cut into six lanes by family (forms core, date & time, money &
secure, overlays, data display, flow & load).

The first wave came back and said, six times independently, that there was nothing to build.

All eighteen components already existed. They were gated, four-theme-cascaded, showroomed and
ruled into, and had been since **2026-07-22** — commit `60e4dc1`, "Phase-2 wave 1: 14 components
land", eight days after the spreadsheet the brief was cut from was written. The spreadsheet's
`Status` column was a **2026-07-14 snapshot that has never been reconciled as waves landed**.

The conductor briefed six lanes off that column **without probing a single row**.

## 2 · Why the wave did not become eighteen duplicate components

This is the part worth recording, because the outcome could easily have been catastrophic and
the reason it wasn't is mechanical rather than lucky.

The base brief carried a **mandatory step-0 premise table**: before building anything, each lane
had to write down every claim it had inherited, mark it verified or not, and name the probe.
Six lanes did that, and six lanes' first row came back `FALSE`. Lane A's receipt states it in
the plainest form:

> *"All three Lane A components already exist, gated, four-theme-cascaded, and ruled. They were
> not built here because they did not need building, and the fence forbids overwriting them."*

Lane A then widened the probe **because the failure looked structural rather than local** — the
right instinct, and the one that turned a lane finding into a wave finding: 19 of the 20 P1 "Gap"
rows already had gated reference snippets; only row 86 (Brand mark / logo) was genuinely absent.
Lanes B, D, E and F ran the same widening independently and agreed.

**Zero duplicate components were built. Nothing gated was overwritten.** Every lane pivoted
in-fence to work that genuinely had not been done: the **four-theme review surfaces**, which did
not exist for any of the eighteen, plus a conformance audit of each live component against
#203's ruled rules. Eighteen spreads, `reviews/REVIEW-203-*-four-themes-v1.html`, with an index.

The credit belongs to the step-0 table, not to the brief. Said plainly: **the wave-3a spend
(964,359 tokens across six subs) bought review surfaces and findings, not the components it was
briefed for.**

## 3 · The class, on its fourth surface

This is [[premise-ages-faster-than-rule]] again, and it is worth counting the recurrences because
the count is the argument:

- a carried COUNT went stale (#194 — the "standing 44" measured 4);
- a carried CI premise went stale (#202 — "CI's complete pass is expected to clear it"; CI
  surveys, it never regenerates);
- a carried token figure went stale (#203, quietly, inside the same session — the type-composite
  debt has been restated as **1,101** for several wraps and measures **1,097**);
- and now a **planning document's status column** went stale, five weeks deep, and was used to
  brief twelve sub-hours of work.

The shape is always the same: a fact that was true when written, in a document nothing re-checks,
quoted forward by a reader who has no reason to doubt it. The rule that catches it is not "be
careful"; it is **verify the PREMISE like repo state**, which is exactly what the step-0 table
mechanised, and which is why the damage stopped at wasted spend rather than at deleted work.

Lane H then built the class fix rather than the instance fix: `knowledge/gen_itinerary_status.py`
**derives** the Status column from the store instead of reading it, measures all 124 rows, and
**exits 1 rather than guess** on any row it cannot resolve. Its first run: 86 rows agree, **35
STALE**, 3 OVERSTATED, 0 UNRESOLVED. The true gap list collapses from "20 P1 gaps" to **23
Layer-1 rows total** — P1 is row 86 alone, an asset-only wrap job — plus Layer 2 as **one**
structural gap rather than 28 component gaps. The frozen 2026-07-14 files were deliberately left
untouched; whether the generated page now *retires* the spreadsheet is Dave's call, not a
worker's.

## 4 · Wave 3b, and what changes when you brief off probes

The second wave was cut differently: every lane's rows were verified absent **first-hand, by the
conductor, before the brief was written**. The difference in outcome is stark — where wave 3a
found 18 of 18 present, wave 3b found 9 of 9 absent, and built all nine end-to-end:
Command-palette, Sidebar-nav, Anchor-nav (lane I) · Combobox, Multi-select, Tags-input (lane J) ·
Kpi-tile, Timeline, Avatar-group (lane K). Library **76 → 85**.

Two details from that wave are worth keeping:

**Lane J's alternate-slug finding.** "Absent" is harder to prove than it looks. `Tags` existed
and was gated — but `grep -nE '<input|contenteditable' Tags.reference.html` returned **0 hits**:
it was the *display* half, and the input half existed under no slug. Likewise `dropdown.meta.json`
*declared* `multi-select (non-native)` and `filterable single-select` variants that had never
been built. A meta can document a component into existence on paper. The probe that settles it is
the markup, not the name.

**Lane K's refusal to close a floated row.** Row 55 (KPI/trend tile) is named by `s182-D2`, which
explicitly declines to rule it — Dave, quoted inside that ruling: *"might be a partially built
trend card with option, I haven't decided yet."* So lane K built it as a **drawn PROPOSED
proposal**, marked so in the snippet header, the meta and the review page. A floated component
with standing direction is not a gap a worker may close; the discipline held under a brief that
would have let it slide.

## 5 · The repair nobody was looking for

Lane C's conformance audit turned up a generator defect that no gate could see: the canon builder
was **silently discarding 33 CSS rules across 19 of 76 snippets**. The drop test in
`gen_canon_components.py` treated any selector whose first token started with `[data-theme` as a
root-level rule to be skipped — so every *descendant* rule under `[data-theme="dark"]` was thrown
away.

Lane G reproduced it independently, and did so **with the generator's own `walk()` rather than a
fresh regex** — the difference between measuring the thing and measuring your model of it. The
ancestor histogram came back `{'[data-theme="dark"]': 33}`: **no light-mode component rule was
ever dropped**, which meant light was a free control for the fix. The capability to carry a root
ancestor already existed in `prefix_selector`; it was the **ordering** that defeated it.

Repaired, mutation-tested across six arms (rc=0), regeneration verified, and put on a before/after
page for Dave's eye. The consequence worth stating out loud: **the mono error ink camp reaches
dark for the first time in 19 components**, and the nine new components' dark legs all ride on
this fix.

## 6 · The instrument that found the record disagreeing with itself

Lane L was briefed to build a consumer for the 44px hit-area token, on the strength of a line in
its brief: *"the token is minted at base tier; no gate reads it."*

That line was false, and the store said so. The lane's own receipt records the cost honestly:

> *"A hit-area gate already exists and is already wired into `_build_all.py`, and Dave has already
> ruled on it four times. I found this only after building — the store grep should have been step
> 0, not step 8."*

`knowledge/_a11y_target.py:60-63` has enforced 44 for controls since `s114-D5` / #116. Which
leaves the record **split three ways**: `s201-D2`'s reading, the `s114-D5`/`s114-D6` line, and a
standing memory hook, and they cannot all be right. **Reconciling it is Dave's store correction**,
and this wrap deliberately did not touch it — it is carried, struck-with-receipt, on the residual.

What lane L did build is still worth having: `knowledge/_validate_hit_area.py`, **advisory and
deliberately unwired**, which caught both known real breaches (Amount-input 39px, Secure-entry
40×48 — correcting Lane C's reported 42) and delivered `s116-D1`'s **owed** mark measurement:
332 of 510 mark-tier rows below 24. And it refuses honestly when it cannot run — re-driven from
the wrap seat in a cold sandbox, `--all` returns **rc=2, "HARNESS UNAVAILABLE — playwright not
importable … this is NOT a pass."** That refusal is the reason its figures are recorded as *lane
L's measurement under a staged harness* rather than re-asserted as if they were reproducible here.

## 7 · The push stopped being Dave's

Mid-session, unprompted by any question about it, Dave wrote:

> *"I'm comfortable with you having control over the push now, this human is a hinderance now."*

Reflected back before inscription, per the clarify-and-reflect discipline, and inscribed as
`s203-D1`. It **reverses a standing clause** of `knowledge/_RUNBOOK-git-commit.md` that had held
since the split was first written: push runs only on Dave's explicit word.

The part of the ruling that matters most is the part that is easiest to drop: **the CI read-back
is part of the ruling, not a courtesy.** A push whose CI verdict is never relayed recreates
exactly the blindness the delegation exists to end — for months the standing complaint was that
work sat unpushed and CI never saw it; a delegated push that lands silently would swap "CI never
ran" for "CI ran and nobody read it", which is worse, because it looks like progress.

He can reclaim the push by a word in chat. Reclaiming needs no inscription; the newest word wins.

⚠ One consequence, and it is live: this wrap **commits only**. The push and the CI read-back are
the **conductor's** act, and the nine new components, lane G's repair and every one of the 29
review surfaces have **never been seen by CI**.

## 8 · What is resolved, and what is still open

**Resolved:** the itinerary's status column is derived rather than typed · the canon dark-drop is
repaired and mutation-proven · nine genuinely-absent components are built and gated with all five
gates green · the hit-area advisory exists, bites, and refuses honestly · the push is delegated,
with its read-back obligation written into the ruling · two carried figures were corrected against
first-hand measurement (type debt 1,101 → 1,097; the `canon.css` hover-var claim → 0 hits).

**Still open, and all of it Dave's:** the ~50 PROPOSED items across twelve receipts, whose door is
`reviews/REVIEW-203-INDEX-2026-08-19-v1.html` · the two-red seam where Stat-card's arrows sit in
the fill seat at 1.98:1 and the new Kpi-tile inherits it (7 of 8 panes disagree; under `s151-D1`
they must move together) · whether the derived itinerary page retires the frozen `.xlsx` ·
promoting the hit-area gate (advisory → wired, and `MARK_TIER` warn → fail — `s114-D6` already
ruled 44 blocking for controls, and 428 control findings say what it said then: *"a remediation
lane, not a flag flip"*) · Sidebar-nav versus the existing Navigations component · the
three-way-split 44-enforcement record · and — the irony of the session — **the segmented-label
type-scale binding this session was NAMED for, which was never touched.**

**Named and unbuilt:** `--check` has no contract. Four of thirteen generators write
unconditionally on `--check`, and the base brief told six lanes the flag was read-only. That is a
priced candidate, not a build, and it is the next instance of the same class this whole session
was about: a claim about the tooling that nothing re-tests.
