# #127 — the schematic, and the record that was wrong about its own defect

```
provenance: 127 · 2026-08-07
status: observed
```

**Spine entry:** `_LIVE-STATE.md` ⏱ LATEST DELTA #127 · **Ledger:** `notes/_MEMENTO-DECISIONS.md` § ★ #127 ·
**Banner:** `GOOD-MORNING.md` ★ LATEST #127 · **Artefact:** `reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html`
(register: `knowledge/_REVIEW-SIGNOFF.md`).
Both-way links per `_DECISION-HISTORY/README.md`.

---

## The shape of the session

OPUS conductor, Dave live, ONE window, three OPUS subs. The title lane — `Apollo - #127: the schematic v2`
— **landed**, which is worth saying plainly because it had been named at #125 and again at #126 and died
both times. The four things that came out of it were the schematic, the wiring that followed from it, the
`_governs.py` repair, and the two state-contrast fixes. The thing that did *not* come out of it was the
dream pass, and that is recorded as overdue rather than quietly dropped.

---

## ① The schematic: why GENERATED was the only acceptable form

v1 (`reviews/MEMENTO-SCHEMATIC-2026-07-26-v1.html`) was hand-authored and asserted *"27 blocking validators
in a 55-step build"*. It was true on 2026-07-26 and false by 2026-08-07 — disk held 30 and 98 — and nothing
in between noticed, **because nothing was asking**. A second hand-drawn diagram would have been the same
object with fresher numbers, i.e. a claim with a shorter fuse.

So `knowledge/_gen_schematic.py` reads the tree and emits the diagram: seven panels (the six subsystems —
chain · store · search · marks · gates · package — plus a self panel), 39 rows, every figure read off disk
at generation time, inline SVG, no CDN. Two decisions inside it are worth recording:

- **Build-step counts come from `_gen_chain._steps_in` — the function, not a copy of its logic.** `s125-D1`
  established one slicer; a schematic that re-implemented the AST read would have been a second slicer with
  the same name and a different answer, which is the `--pri-hover` finding in another medium
  ([[canon-pri-hover-fork-108]]).
- **Each panel computes its own "what re-checks this"** from `STEPS` × `ROUTE_ROWS`, and renders a red
  **NOTHING RE-CHECKS THIS** where the answer is none. This was not decoration. **The panel fired that
  warning about the schematic itself** until the wiring below landed — the artefact accused itself, in
  public, on Dave's screen.

**v1 was KEPT and TOMBSTONED, +29/−0.** Dave's #125 disposition, enacted verbatim. The stale figures were
deliberately not corrected: they are the worked example of the class, and a corrected v1 would destroy the
only evidence that the class is real.

## ② The wiring, and the fourth row

Dave's call at the opener took the build from **98 to 102 steps**: three schematic rows (build · `--check` ·
`--selftest`) and **one contrast-selftest row**. Three were quoted to him; **four were wired**. The fourth
was added under the file's own stated precedent — *"a selftest not in STEPS is a gate that does not run"* —
and was **declared in chat at the time, not buried in a diff**. It is recorded here in the same words
because a deviation that is only mentioned once is a deviation that will read as drift later.

## ★ ③ `s125-D1` demonstrated itself a third time, live

Wiring the rows moved the chain's published build figure **98 → 102** and the never-verified shortfall
**23 → 27**, with **nothing typed**. #125 ruled it, #126 enacted it, #127 changed the underlying tree and
the published record simply followed. Three consecutive sessions, one ruling, no re-stamp.

## ④ `_governs.py`: the repair that would have gone green pointing at the wrong thing

The standing record said (`_LIVE-STATE.md:457`) that `s121-D1` points at `knowledge/canon/canon.css:5548`
and that *"that line does not exist"*. **Both halves were false.**

- The ruling points at **bare `canon.css`**. The record had silently added the `knowledge/canon/` prefix —
  and that addition is what hid the actual defect, because a bare `canon.css` is **never resolvable from
  repo root**. The entry was therefore **born red at #121**; it did not rot into red.
- **Line 5548 exists.** Today it reads `--alpha-84: 0.84;`.

⚠ **A repair driven off that sentence would have re-pointed the ruling at line 5548 and gone GREEN pointing
at an unrelated token.** The construct the ruling actually cites — the RAG roundel policy — had drifted
**5548 → 6451**, 903 lines in five sessions.

The fix does not re-point anything. `knowledge/_governs.py` gained an anchor pointer form `<path>#<literal>`
(`is_anchor_pointer()`, `resolve_anchor()`, wired into `render()` and `selftest()`), **+135/−0, purely
additive**, with the **line number derived at read time and stored nowhere** — the `_steps_in` shape again.
`_rulings.json` moved ±2 lines and was **round-trip byte-verified before writing** ([[serializer-defaults-reformat-the-file]]).
Seven mutation bites, all red as designed, every restore sha256 byte-exact. `_governs --selftest`: **32 → 30**.

**And then the honest part.** The gate reports only `fs[0]`, so *"one rotten pointer"* was never one entry.
**Thirty remain**, in three classes: **B (18)** — `s122-D1…D5`, `s123-D1…D4`, `s124-D1`, missing `evidence`
or `status`, where filling the field **means asserting what Dave ruled**; **C (12)** — `s125-D1/D2/D3`,
where `evidence` was used as a prose field; and **11 further entries still on the old `<path>:<int>` form,
green and unverifiable and currently invisible.** ★ A form that cannot fail is not a passing form. All
recorded, none fixed.

## ⑤ The contrast fixes, and what made the boundary provable

Two defects were carried in from #125, both scoped out of `s125-D3` on purpose so its mutation test proved
one clause and not a bundle.

- **`effBg` was not "ancestors only" — the MODEL was wrong.** It modelled the paint stack as the ancestor
  chain, **when painting is a z-ordered geometry of boxes**. Ancestors are a subset of that geometry, so the
  code was blind *by construction* to an absolutely-positioned sibling. It now composites the browser's own
  hit stack (`elementsFromPoint`, paint order, src-over). Naming the class this way matters: "walk siblings
  too" would have been a patch that fails again on the next geometry it did not anticipate.
- **`out[3]` was a derived summary written into a positional slot the loop above owns.** Now an insert. The
  eaten `Accordion` heading is back and the zero-snippet `IndexError` is a named refusal.

**The boundary is the finding, not the fix. TEXT failures 46 → 14: exactly the 32 named false failures
removed (Segmented-control ×12 · Charts ×16 · View-options ×4), ZERO added, and all four REAL failures
survive with identical ratios** — Banner `.abtn:active` 4.09:1 ×4, Selection-controls 3.95:1 ×6 + 3.66:1 ×2,
Tabs dark 1.00:1 ×2. Nothing was waived and no threshold moved. **A second instrument sharing no code
confirmed it**: screenshot pixels read 21.0:1 where the gate had said 1:1.

Eight mutation bites, one clause each, byte-exact restore after every one — including **M5, the boundary
guard: a "fix" that stops failing by ceasing to report goes RED.** That bite exists because the cheapest way
to make this gate green is to make it measure less.

⚠ **The sub's first implementation was wrong twice and measurement caught both**: ignoring element `opacity`
invented 12 failures, and refusing un-hit-testable boxes turned 60 measured records into holes. **Both were
visible only because it captured the whole corpus instead of trusting the headline** ([[green-tests-cannot-see-scope]]).
Fifteen un-hit-testable boxes remain; the build declares them. **Whether declaring or refusing is right is
Dave's call, and it was left open.**

## ⑥ The claim that went false a third time — and the refusal to re-stamp it

`_build_all.py`'s state-contrast comment had already been hand-corrected once at #125, for going false
inside its own session. At #127 it went false again. **And a third instance sat beside it**: the gate's
`ROUTE_ROWS` remedy string still carried the `s125-D3` parse caveat, which had been *fixed at #125* — #127
measured **0 parse refusals across all 75 snippets**, before and after.

The comment was corrected. **The remedy was deliberately not corrected**, and that is a decision, not an
omission: the standing rule is *stale twice ⇒ GENERATE, don't re-stamp*, and a third hand-correction is
precisely the move `s125-D1` exists to forbid. It is left in place **as evidence**, with the generate-vs-
re-stamp question raised to Dave.

## ⑦ What we got wrong: a reserve on a reserve

The opener treated **150,929 as the ceiling and then subtracted the wrap again**, reporting ~30K of job room
against a real **79,012**. Dave caught it: *"150,929 is the line at which it is recommended you start the
wrap, not the limit."* 200,000 is working, 256,000 is the hard stop, and 150,929 is **derived** as
`wall − wrap`.

★ The defect is named in `_gauge_tokens.py`'s own comments **eleven lines above the constant that was
quoted**. The guard existed; it was not read. ⚠ And it was not cosmetic — **it materially affected a
decision**: Dave chose to delegate the schematic against an understated budget. The delegation succeeded;
the stated reason did not, so the pick was **declared re-openable rather than settled**. The arithmetic is
now inscribed at `knowledge/_RUNBOOK-context-gauge.md` § The Red trigger: **`job room = stop line − CURRENT
FILL`; the wrap is already inside the stop line; never subtract it twice.** No constant was moved.

## ⑧ The dream pass

Dave raised it mid-session. **A sub's report alone cost more FILL than remained before the wrap-open line**,
so it was rolled to #128 as the first item rather than started and abandoned. It is recorded as **overdue**,
not queued: it is the only thing on the #128 list he asked for out loud and did not get.

---

## Resolved state

**Closed:** the schematic (v2 generated, v1 tombstoned) · both `_validate_state_contrast.py` defects · the
audit's "stale by 37" · the `s121-D1` pointer, structurally.

**Open, and named:** the 30 remaining pointer entries (class B is Dave's ruling text; class C is mechanical
but rewrites ruling records; 11 legacy pointers are invisible) · declare-vs-refuse on the 15 un-hit-testable
boxes · the four REAL contrast failures · generate-vs-re-stamp for the `_build_all.py` comment and remedy ·
⛔/★-vs-ASCII in generated artefacts · the boot-floor re-base, now a **sixth** below-floor reading · the
dream pass.

**Nothing in this session's wrap ruled anything**, and no `s127-D*` id was minted: minting a ruling id is a
ruling act, and it is Dave's.
