# #199 — the snap was the answer, and the queue went stale a third time

```
provenance: 199 · 2026-08-18
status: observed
```

*The narrative dossier for session #199 (capture-ritual step 1b). The WHAT lives in
`GOOD-MORNING.md`'s ★ LATEST banner, `_LIVE-STATE.md`'s ⏱ LATEST delta, and
`knowledge/_rulings.json` § `s199-D1` / `s199-D2`. This file holds the WHY and HOW.
Written by the DELEGATED wrap sub; every sha here is read back from `git log`, never from
the brief this sub was given.*

Both-way links: `GOOD-MORNING.md` ★ LATEST #199 · `_LIVE-STATE.md` ⏱ LATEST DELTA #199 ·
`knowledge/_rulings.json` (`s199-D1`, `s199-D2`) · commits `dcc16de` · `a2d330e`.

---

## 1. The open question was not a gap — it was a preference

#198 fenced Supercharge's hover with scope-preserving overrides (`warm/7`, `warm/10`) and wrote
the fence up honestly: **pixel-identical today, but it is a SNAP, not a 0.68 derivation, and the
derivation question is Dave's.** That framing carried an implicit theory — that a snap is an
unfinished derivation, and that finishing it is owed work sitting on a queue.

Dave's ruling dissolved the theory rather than answering the question inside it:

> *"no derivation, supercharge works with specific colour values"*

`s199-D1` is therefore a **settlement, not a deferral**. The #198 overrides are the answer. The
important consequence for the record is what must NOT happen next: nobody should re-open this as
"the warm derivation is still owed", because the residual it came from is consumed, not carried.
That is why the #199 banner marks it **SETTLED, not deferred** in the same clause that consumes it.

The general shape is one this project keeps meeting from different sides: a per-theme system's
*flexibility is the requirement*, so a theme choosing literal values over a derivation is the
system working, not the system incomplete [[four-themes-flexibility-is-the-requirement]].

## 2. The rename had to be one act, not a sequence

`s199-D2` renamed `color/mono/hover-1|hover-2` to `hover-light`|`hover-dark`. Read as a naming
change it is trivial. Read as a token-graph change it is the #198 near-miss waiting to happen
again: the primitives are mirrored into `neutral/*`, aliased by semantic entries, and **overridden
by Supercharge**. Re-point the alias first and the override's target no longer exists — the theme
silently falls back to the mono greys, and no gate renders a pixel to notice.

So the rename moved primitives, mirrors, aliases and the Supercharge overrides **together, in one
commit** (`dcc16de`), and the mint-notes were **annotated** rather than rewritten — the notes are a
record of when and why the primitives were minted, and falsifying them to match a later name would
destroy the provenance the rename is supposed to preserve.

Dave picked option **B** off `reviews/HOVER-NAMES-2026-08-18-v1.html`. The page is the mechanism,
not decoration: an eye-ruled naming choice made from a rendered comparison is a different act from
a name proposed in prose and nodded through.

## 3. The third recurrence, and why the gate could not have caught it

The session's second commit (`a2d330e`) was meant to be small: flip the stale-queue gate's route
label to `(BLOCKING,#198)` and correct a selftest docstring that said 6 bites while the test ran 13.
Both landed. The route label is a **join key**, so it moved in *both* `_build_all.py` tables at once
and the join was verified 2/2 — a label edited in one table only is the defect that instrument was
built to prevent.

The finding came from the other lane. An Opus worker was sent to enact §C·1(d)'s DV-D07 mint
candidate — `data/axis` and `data/grid`. It found the work **already done on 2026-07-23**:
`knowledge/tokens/semantic-colour.json:2035–2075`, with receipts at
`notes/_receipts/2026-07-23-chart-line-exemplar-worker.md:43` and
`notes/_receipts/2026-07-24-wave-lane1-bar-scatter.md:28`.

This is the **third** occurrence of the class — #26 first, #196 second, #199 third — and #196 built
a gate for exactly this (`knowledge/_validate_queue_fresh.py`, flipped BLOCKING at #198). The gate
was live. The gate passed. And the gate was **right to pass**, which is the uncomfortable part: the
item carries a `declared=` tail, and the grammar does not measure declared-no-artefact items. There
was nothing on disk for it to contradict.

The lesson is not "the gate failed". It is that **"the gate is green" and "the queue is fresh" are
two different claims**, and #198's record — reasonably — read the first as evidence for the second.
A gate's glob is the exact width of its authority [[gate-glob-scope-rule]]; a class fix that leaves
a whole item shape outside the grammar has closed most of the class, not the class.

The candidate remedy — teaching the grammar to reach `declared=` items — is **priced and not built**,
and this wrap deliberately rules nothing about it. Naming a fence is not crossing it.

## 4. What was not proven, again

#198 recorded that the gate's **detection** across a §C·1-moving roll had never been observed —
survival had, detection had not. This wrap could have closed half of it and did not: the 2c/2d/2f
rolls ran *before* the probe, so only a POST-roll run exists (PASS, 7 items, blocking tier, rc=0).
Reconstructing a pre-roll reading afterwards would have been an invented measurement, so the missing
half is declared rather than filled. Survival: twice proven. Detection: still zero.

## 5. The tuner that returned

The same worker built `reviews/RADIUS-CORNER-TUNER-2026-08-18-v1.html` standalone — border-radius
tokens read live from `knowledge/tokens/layout.json`, container and data-mark sliders explicitly
flagged **PROPOSED** so a slider cannot pass itself off as a ruling, and an export that **preserves
the `$alias` cascade** instead of flattening it (a flattening export would silently convert a
theming decision into thirty literal values).

It surfaced one thing worth the banner: **Supercharge carries no border-radius override at all** —
it inherits the mono base. That is disk truth, not inference, and it is surfaced rather than ruled.

Dave had said "return SOON" about this tuner. It returned. What it does not yet have is his eye,
and neither does `reviews/GROUPB-HOVER-EYE-2026-08-18-v1.html`. Both are the #200 opener.

## 6. Resolved state, and what is still open

**Resolved:** `s199-D1` (Supercharge's snap is the settled state) · `s199-D2` (the rename, enacted
end to end) · the route label in both tables · the selftest docstring · the DV-D07 phantom, struck
by addition with its receipts named · memory step 3, run at the conductor's seat.

**Still open, and named on the residual → #200:** Dave's eye on the radius/corner tuner and on the
Group B hover page · the icon-button's 70% hardcode against the family's 0.68 · detection across a
moving roll · the stale baked artefacts, now wider than #198 recorded them because `canon.css` still
carries the pre-rename `--color-*-hover-1|2` names · the `declared=` blind spot as a priced
candidate · wave-3 brief-cutting, deferred for budget.
