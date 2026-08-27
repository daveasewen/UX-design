# #220 — the lift, the default, and the day we drove our own machinery

```
provenance: 220 · 2026-08-27
status: observed
```

*Narrative dossier (ritual step 1b). The WHAT lives in `knowledge/_rulings.json` § `s220-D1` ·
`s220-D2` · `s220-D3`, the sixteen filed reports under `notes/_subreports/2026-08-27-220-*.md`,
and `GOOD-MORNING.md`'s ★ LATEST banner. This file holds the WHY and HOW — the arc, the dead
ends, the corrections. Both-way links: spine entry = `_LIVE-STATE.md` ⏱ LATEST DELTA #220;
ledger = `knowledge/_rulings.json` § `s220-D1`…`s220-D3`.*

*Written by the delegated Opus wrap sub from the conductor's brief
(`notes/_briefs/2026-08-27-220-wrap-brief.md`), the filed reports, the store, the tree and
`git log` — never from the chat transcript, which this seat cannot read. Every figure below was
copied off a file or measured here; none was retyped from the brief.*

---

## 1 · The day opened on a parked lane and an unenacted correction

#219 shipped a release and, in doing so, **parked the bento lane by Dave's own word** and left a
correction of his RECORDED but NOT ENACTED — *"its ether cohesive capsule or rounded full image
if there is no background colour on the caption"*, homed at
`notes/_receipts/2026-08-25-219-role-defaults-exports.md` § PARKED CORRECTION. The #219 banner
named that as the first thing #220 owed him. It is the thing #220 started with.

The method was the one that has now been ruled into the memory hooks: **mock the readings before
building.** An ambiguous visual ruling gets two or three readings rendered side by side and Dave
points. `reviews/CORRECTION-READINGS-2026-08-27-v1.html` put three readings of his correction on
one page (report `notes/_subreports/2026-08-27-220-readings-capsule.md`, *findings 9 ·
ruling-shaped 6 · UNPROVEN 3*). **Two of the three readings were rejected**, and the reason is
worth keeping: readings A and B were *removals* — they proposed taking a treatment out of the
grammar. Dave's answer was **"these 4 are all 'legal'"**. He did not want a smaller vocabulary.
He wanted a different **default**.

That distinction is the whole of `s220-D2`, and it is the second time in three sessions that the
`s219-D1` default-vs-option split has done real work: a role setting is a DEFAULT plus an
edit-pass OPTION SET, so a complaint about what you *see first* is a complaint about the default,
not a case for deleting an option.

## 2 · The lift: a value pick that turned into a rule

His complaint was narrower than it first read — *"the console chord looks good except the caption
in dark mode is too dark in capsule mode"*. **Dark MODE. Caption grounds. Capsule.** The ladder
page (`reviews/CAPTION-DARK-LADDER-2026-08-27-v1.html`, report
`notes/_subreports/2026-08-27-220-caption-dark-ladder.md`, *findings 11 · ruling-shaped 6 ·
UNPROVEN 4*) drew the rungs and he picked one: *"So i prefer gb(48,48,48) . #303030 for caption
background in dark mode, but there isn't a token for it, is there a primitive thats close in the
neutral ramp"*.

**The question inside his question is the finding.** He did not ask for `#303030`; he asked
whether the ramp already answers. It does — `color/neutral/5` `#313131`, one grey point off,
ΔL* ~0.4. And once the answer was a primitive rather than a hex, he extended it himself: *"yes
the other themes need an appropriate lift too, align with the neutral primitives please."*

So `s220-D1` is **not a colour**. It is **alignment by LIFT, not by HEX**: each theme's dark
caption ground lifts off *that theme's* dark page by the console calibration (neutral/5 over
`#1A1A1A`, ΔL* ~11), taken from *that theme's own* primitive ramp. Enacted dark-only at
`CAPTION_GROUND_MINTS`: mono `#313131`, legacy `#313131`, console `#313131` (all neutral/5),
supercharge `#312C26` (warm/5, ΔL* +9.08).

**The supercharge value corrected an INVERSION** — its caption ground had been sitting *darker*
than its page. Nobody had asked for that fix; it fell out of stating the rule as a lift. A hex
list would have carried the inversion forward, because a hex list has no opinion about the ground
behind it. That is the argument for the rule form, and it is why the per-theme values are
**PROPOSED to his eye** while the rule is his and settled.

Enacted in two steps, deliberately: the rung first (`reviews/RUNG-ENACT-2026-08-27-v1.html`,
report `-rung-enact.md`, *8 files changed +394/−9, 40 verifier states driven*), then the
all-theme extension (`reviews/THEME-LIFT-2026-08-27-v1.html`, report `-theme-lift.md`, *11 files
+617/−142, matrix bites 100 → 103, 7 mutation arms with before/after MEASURED*). Both pages await
his eye.

## 3 · The default switch, and a discharge by ADDITION

`s220-D2` moved the **console gallery default** to chord two — **rounded-corner image +
transparent caption**, identical in light and dark — on his words *"if you are asking for a
default lets go with rounded corner image with transparent capsule"* and, over the pair, *"I guess
this would be the default for the two modes"*. It supersedes `s219-D2`(3)'s capsule default and
the console-gallery capsule+grey rows of his own `s219-D1`(3) tuner exports: **his word outranks
his own export**, which is the `s219-D2`(1) latest-wins pattern showing up for the second time.

⚠ **MONO IS EXPRESSLY OPEN.** The ruling set console. Mono's gallery default is still one word of
his, and this wrap did not put a value in that hole.

And the #219 parked correction was **discharged BY ADDITION, never by removal** — all four
caption treatments stay legal, the receipt cites `s220-D2`, and no option left the grammar. That
shape matters: a correction discharged by deleting the offending option would have quietly
narrowed the edit pass `s219-D1` had just widened.

## 4 · Two releases in one day, and what that broke

`Apollo - Spider v1.0.1` carrying `Memento - Gumdrop v1.0.1` was baked and pushed — zip
**18,992,272 B**, **1,646 entries**, sha256 `c8934ebd…`, re-measured off the artefact and not
retyped. Both cold-start breakers were fixed **at cause**; `knowledge/_gate_pack_imports.py` was
born **ADVISORY** and stays advisory.

The interesting failure was structural rather than technical. **A two-release day breaks any gate
that audits history against the live manifest** — the release-audit `--pack` arm compares frozen
old releases to the manifest that now speaks for a *newer* version, and on the first day the repo
ever shipped twice, it fired. It was re-scoped **at cause**: the manifest speaks for ONE version
(commit `b6f5ad0`). The class is worth naming because it is invisible until the second release
exists, and it will be invisible again for the next assumption that quietly encodes "one of these
per day".

`s220-D3` came out of the same bake by a different road. The v1.0.1 pack ships 30 Getty/EyeEm
**web derivatives**, and shipping them *distributes* licensed assets to Dave's designers — the
`s219-D5`(Q2) fonts ruling covered fonts only. Flagged explicitly, he answered *"images are in
licence, all good."* ⛔ **The reason there is a ruling entry at all is that the L5 audit found the
licence word homed only in a CODE COMMENT.** A chat sentence is not a home for a live
distribution fact (ADR-0017). The inscription is the home; the pack provenance may cite it.

## 5 · The audit wave: what the machinery does when you actually drive it

Six lanes, filed and cited by path. The wave's premise was the standing one — **a green test
cannot see its own scope** — and it paid.

- **L1 (gate fleet).** ⛔ **The `gates` job of `.github/workflows/gates.yml` has been RED AT ITS
  FIRST STEP since `aa26947`**, which means two sessions of the Knowledge build, 27 gate
  bite-tests, 19 advisory bite-tests, the commit-script selftest and the claim-table linter have
  **not run in CI at all**. Eight false greens established, four of them by *planted defect with
  a firing control beside each*: two BLOCKING gates blind to CSS logical properties, one blind to
  `style=""` entirely, `_validate_wiring.py` green only because its glob cannot see the
  `_gate_*.py` namespace, and five committed gate artefacts stale at HEAD with nothing comparing
  them. **The fleet's static leg has no HTML or CSS parser anywhere in it** — the #122 finding,
  still true.
- **L2 (generator fleet).** 35 of 36 driven; 21 reproduce byte-for-byte; 7 drift in four classes.
  `gen_dashboard.py --check`, a **BLOCKING** build gate, has **no reachable FAIL path** — it can
  return 0 or 77 and never 1 — and the dashboard it guards *is* stale (#219 / 194 items against a
  store now holding 299). And a **case-sensitivity class**: `gen_library_214.py` is byte-identical
  on macOS and silently degrades on Linux, which is what CI runs — 7 components degraded where
  nobody looks.
- **L3 (token & canon health).** The good news is real: **silent black is 0 across every live
  population**, and the `s220-D1` mint resolves 8/8 per theme × mode with values matching the
  ruled table exactly. The bad news is a shape we keep meeting: `_validate_token_forks.py` exits
  **0** at baseline and **1** on 98 forks under its own `--strict` flag — same tree, same run,
  opposite verdict, and **only the permissive mode is wired**. Plus 16 drifted fallback
  cause-sites across 5 sibling generators, and a probe README asserting 64 findings that no
  longer exist.
- **L4 (designer first hour).** The pack was extracted from the shipped zip and driven as a
  designer would. **"Green on day one" holds** — 35 pass / 0 FAIL in 7s on a virgin pack, both
  gate routes work, both mutation arms fire. But **`tiktoken` is documented as optional and the
  wrap step hard-refuses without it**, so a designer on a clean machine finishes the guided
  session, gets a red, and is greeted next morning as if the pack had never been used. The whole
  first session evaporates. Three more blockers beside it.
- **L5 (the sitting).** `reviews/SITTING-220-2026-08-27-v1.html` — **122 calls, 97 open, 25
  CANDIDATE-closed, and nothing closed.** Every candidate is a struck card carrying the clause or
  probe that answers it, **probed in the tree today** rather than inherited from the report that
  proposed it — which is how three turned out to be answered by an *enactment* rather than a
  ruling, and one by the code-comment licence sentence that became `s220-D3`.
- **L6 (efficiency).** 140/140 build steps timed, 12 trims priced, none taken. `git gc` recovers
  ~744 MB — **Dave's machine only**, because of the sandbox `tmp_obj` kill class. ⚠ And L6
  **declared its own fence breach**: `_capture_gate.py --selftest` ran twice against the brief's
  ban. Measured consequence: **no tracked file moved, twice**. Reported as a premise to re-check
  upward, *not* as a licence to drop the fence — which is the right disposal, and the re-check is
  priced and not run.

## 6 · The correction this session owes itself

⛔ **The ARMED ~190,000 stop line was crossed mid-bake without an at-crossing declaration.** The
conductor declared it **late**, when Dave asked *"how hot"*. The 200,000 working line and the
256,000 wall were crossed too. The platform window is ~15M and nothing broke — and that is
precisely why the miss is worth writing down rather than smoothing: **a silent crossing is a
failed declaration even when the environment makes it safe.** The declaration is the instrument;
the safety is a property of the day.

It is also, again, **evidence FOR the pending `s208-D1` re-base and never a licence for it.** Boot
came in at **69,565 real** — the **TENTH consecutive** out-of-band reading against a band of
55,595–57,903. Ten. No constant, band, advisory, stop line or wall was moved at this wrap, and the
re-base stays Dave's, with the boot-REDUCTION option that his own rider requires priced beside it.

## 7 · What is still open

Mono's gallery default — one word of his. The THEME-LIFT / DEFAULT-SWITCH / RUNG proof pages
await his eye. The 97 sitting calls stay open. **CI is red at the first `gates` step and his
read-back queue is still blocked at his GitHub sign-in**, which means the audit wave's own
evidence about CI is CLAIMED via a local bare-clone proxy rather than read back from a run. Every
repair the six lanes priced is a **next-session lane**, by this wrap's own fence: nothing found
today was fixed today, and that was the deal the wave was run under.
