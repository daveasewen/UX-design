# #206 — the registry caught the tree, and repaired nothing

provenance: 206 · 2026-08-19
status: observed

*Session #206. FABLE conductor + 1 OPUS work sub (the `W-45` build-PM) + this OPUS delegated wrap sub.
⛔ **ZERO RULINGS INSCRIBED** — `knowledge/_rulings.json` is byte-untouched.
Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #206 · banner: `GOOD-MORNING.md` ★ LATEST #206 ·
receipt: `notes/_receipts/2026-08-19-206-w45-registry-drive.md` · claim table:
`notes/_claims/206-w45-claims.jsonl` · store rows `W-48`/`W-49`/`W-50` in `knowledge/_state.json`.*

---

## 0. Why this session existed

`s204-D1` ordered three lanes in sequence: `W-44` (the claim table), `W-45` (the probe registry),
`W-46` (a scope-only lane). #205 built `W-44` and left `W-45` sitting on the residual as *"the next
ordered build"*. Dave's opening word at #206 was two syllables — **"go for it"** — and that is the
entire authorisation this session ran on. Nothing else was ruled, and nothing else should be read
back into it.

The forward premise was simple and turned out to be the interesting part: **`W-45` is an instrument
whose whole purpose is to re-run defects the project has already found once, so that the second
occurrence is caught by a script rather than by a session's memory.** Building it means writing five
probes. *Driving* it means pointing them at the corpus that produced them. Those are not the same
act, and only the second one can surprise you.

## 1. What was built, and the one shape decision inside it

`knowledge/_probe_registry/` — five probes, one runner, one promotion tool:

| probe | class |
|---|---|
| `P-1` | meta-schema conformance |
| `P-2` | duplicate id / unresolved IDREF (the #204 class) |
| `P-3` | dangling dataviz var → silent-black pixel |
| `P-4` | premise-vs-store (a brief asserting state the store contradicts) |
| `P-5` | stale typed figure vs a live count |

The registry itself is `manifest.jsonl`. **The `caught` ledger is a FIELD on each manifest row, not
a separate file** — this wrap re-read `knowledge/_probe_registry/README.md` first-hand to check that,
because the build brief's phrasing (*"manifest + caught ledger"*) reads naturally as two artefacts and
a wrap that repeated it would have inscribed a file that does not exist. Small, and exactly the class
[[enactment-register-adr-0016]] exists to catch: **re-read the generated thing; never quote the
description of it.**

Two typed dimensions on every `caught` entry carry the honesty:

- **provenance** — `historical-mined` (this probe would have caught a defect we already know about)
  versus `live-run` (this probe caught something on a real tree, today).
- **kind** — `exact` (the same defect) versus `species` (the same class, a different instance).

Those two fields are the whole reason the promotion output later reads as weak evidence rather than
strong. Without them, three candidates would have looked like three proven wins.

`_promote.py` implements the twice-caught rule and **writes nothing**. Its no-write property is
proven by an **mtime selftest arm** against `_DS-IMPROVEMENTS.md` rather than asserted in a docstring —
which is the difference between a claim and a test [[mutation-tests-the-clause-not-the-feature]].

## 2. The finding: an instrument built from the corpus found three live defects in it

The first real-tree drive returned **three live catches**, and the session repaired **none** of them:

1. **`P-2` → 46 findings** — 10 `DUPLICATE-ID` and 36 `UNRESOLVED-IDREF` across **7 review files**.
   This is the #204 class, still alive in pages authored before #204 fixed it. The class was fixed
   forward and never swept backward, and nothing existed to notice that until now.
2. **`P-5` → `knowledge/README.md:13`** still types **"(38 metas)"** against a live **92**. That is
   the same population ASSERT-009 was re-based to at #205 — the assertion was corrected in
   `_assertions.json` and the prose that repeats it was not, which is the home-pointer-rot class
   arriving from the other direction.
3. **`P-4` → unrowed briefs.** And the first one it found was **this session's own brief**. The
   conductor repaired that before staging (row `W-50`, commit `d07e85c`);
   `notes/_briefs/2026-08-16-memento-closeout-plan.md` remains unrowed.

**The decision that matters here is the one that was NOT taken.** All three findings sit outside the
regions this session owned. Repairing them would have been cheap — a regenerate, a number, a store
row — and it would also have been a build sub silently editing three files nobody asked it to touch.
`W-49`'s `closes_when` carries repair-or-park, and **that call is Dave's**. The precedent this session
is deliberately setting: *a probe reports; a ruling repairs.* [[do-not-rule-list-cannot-fence-a-generator]]

## 3. Promotion: three candidates, and why "twice caught" was not enough on its own

`_promote.py` emitted **three twice-caught candidates** — `P-2` (#204 + #206), `P-4` (#203 / #204 /
#206), `P-5` (#173 / #203 / #206) — and **all three are MIXED basis**: historical-mined evidence plus
one live run. `P-1` and `P-3` were correctly not candidates.

The temptation, written down because it was real, was to report "three probes have earned promotion".
They have not. Mixed basis is the **weakest** form the twice-caught rule admits: one of the two
occurrences was mined from a record that already knew the answer, which is closer to a fixture than to
a catch. Saying so costs a sentence and preserves the difference between an instrument that has been
tested and one that has been demonstrated [[green-tests-cannot-see-scope]].

Promotion is Dave's under derivation governance, so all three stayed as candidature text on stdout.

## 4. The dead-end, and why the refusal is the right outcome

`P-3` — the dangling-var pixel probe — is the only probe that needs a browser, and it reports **three
different states in three environments**:

- **rc=0** selftest in the build sub's environment, where Playwright was staged;
- **rc=1, `NOT-IN-THIS-ENVIRONMENT`, loud and named**, in the conductor's fresh shell;
- **unproven** in CI, which has never seen it.

The refusal is the design working [[honest-refusal-needs-a-legal-form]]. But it would be a mistake to
file that as a pass. A probe that refuses in two of three environments has a **structural** gap, not an
environmental one, and it is the same shape as `s173`'s gate-that-cannot-pass-in-one-environment
[[gate-cannot-pass-in-one-environment]]. It is written on the residual as unproven rather than as
green-with-a-caveat, because those two readings behave differently in six sessions' time.

## 5. The correction that arrived exactly on schedule

#205's wrap wrote a pitfall (d): *"CI's 49/1 is a survey, not a regeneration — the next generator
change re-stales them identically."*

At #206 the next generator change happened. The new `W-45` documents landed, the graph mention map
went stale, and CI ran **RED with `[110]` + `[13]`** on both `d07e85c` and `49ba965`. The pitfall was
not a hedge; it was a forecast, and it came true within one session.

It was repaired the cheap way — a **targeted** regeneration, pushed at `5a716a6`, giving run
**32270152513** a gates job of **49 pass · 1 fail, `[13]` only**, read out of the log rather than off
the badge. And it will happen again on the next generator change, because CI still surveys and never
regenerates. **That is the finding: a pitfall that recurs on schedule is not a warning any more, it is
an unbuilt gate.**

Two smaller things from the same beat, recorded rather than tidied:

- the conductor's **check-in at the lane seam** caught a stale retrieval index right after the `W-45`
  docs landed — the #32 class — and it was rebuilt and committed for almost nothing at `49ba965`.
  The check-in-INSIDE-the-lane rule has now paid for itself in two consecutive sessions
  [[checkin-at-the-ends-cannot-catch-the-lane]].
- the **render job's verdict on `5a716a6` is DECLARED UNREAD**: SUCCESS on the earlier run
  **32269020332**, `in_progress` at the conductor's last read on **32270152513**. A wrap does not
  invent a verdict it did not see [[feedback-measuring-tool-must-not-guess]].

## 6. The gauge, and the number that did not move

For the first time in five sessions the wrap was handed over **under the advisory stop line**: FILL at
the wrap-brief cut **128,711 real** against **150,929**, with **22,218** of room. Boot **57,133**, job
window ≈ **71,600**, effort band **`M`** against edges 45,000 / 75,000 re-derived first-hand from
`gen_dashboard.effort_anchors()` (n=26) rather than inherited from the brief. The sub cost
**242,418 tokens** — quota, not fill.

And then the number that did **not** move. Dave's quota panel read **identically at the opener and at
the close**: *"All models Resets Thu 10:59 PM 60% used · Fable Resets Thu 10:59 PM 71% used"* — an
intra-session delta of **0/0** across one full Opus lane. Against #205's close (58/68) that is All +2 /
Fable +3. The honest reading is that the panel **lags**, and it is recorded verbatim rather than
smoothed into a trend.

This matters because of Dave's closing sentence — *"we still have loads of token spend so we should
crank that next one"* — which is a pacing decision taken against an instrument that did not respond to
a full lane of work. The instruction stands; the **basis** for it is flagged.

## 7. Resolved state, and what is still open

**Resolved:** `W-45` is built, selftested, receipted, claim-tabled (25 rows,
`_validate_evidence.py` rc=0 with three declared sampler refusals), store-rowed, committed and pushed.
The registry has been driven once on a real tree and it worked.

**Open, and every one of them is Dave's or unbuilt:**

- **repair-or-park** on the three live catches;
- **promotion** of the three mixed-basis candidates;
- the five `W-44` schema choices, and ASSERT-009's (a)/(b)/(c), both untouched since #205;
- **`[13]`** — `_governs.py`'s too-loose matcher, standing red, still unpriced, now named in three
  consecutive sessions;
- and the structural one: **`W-44` and `W-45` are both unwired**, by `s204-D1`, until the first real
  verifier wave. Two instruments now wait on **one** consumer event, which is not additive risk — an
  instrument with no consumer cannot fail, and now there are two of them
  [[instrument-without-a-consumer]].

`W-46` is next, and it is **scope-only**: items 3/4/5, output is three scoped proposals returning to
Dave. Scope-only still means scope-only.

---

*Both-way links: `_LIVE-STATE.md` ⏱ LATEST DELTA #206 · `GOOD-MORNING.md` ★ LATEST #206 ·
`notes/_receipts/2026-08-19-206-w45-registry-drive.md` · `notes/_claims/206-w45-claims.jsonl` ·
`knowledge/_probe_registry/README.md`.*
