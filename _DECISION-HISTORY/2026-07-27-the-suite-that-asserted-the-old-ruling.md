# The suite that asserted the old ruling — DV-D17 enacted, and six green checks that had to go red first

provenance: apollo-sds-2026-07-27-7 · 2026-07-27
status: ruled · knowledge/_proforma/_DATAVIZ-DECISIONS.md § Batch 10 (DV-D17)

*Session #7, Monday 2026-07-27, Opus 5 solo self-conducting, effort MAX. The first ENACTMENT window
after three consecutive record-only ones. DV-D17 is built and proven at the DOM level; the render in
the licensed cut is deliberately OWED, flushed to a fresh window on Dave's ruling. Spine entry:
`_LIVE-STATE.md` ⏱ LATEST 2026-07-27 #7 · ledger: `knowledge/_proforma/_DATAVIZ-DECISIONS.md`
§ Batch 10, DV-D17 ENACTED block.*

---

## 0. The step that was a read, not a build — and it answered a question the ledger had left open

`GOOD-MORNING` §DO-FIRST opened with step 0: **does the donut actually sequence today?** DV-D16's ask
names the pie as its reference (*"same as the pie"*) and the ledger recorded, honestly, that nobody had
checked. It also said: answer it from the repo, do **not** ask Dave ([[feedback-verify-before-asking]]).

**It does sequence — and not in the way the phrase implies.** `sweepDonut()`
(`snippets/Chart-donut.reference.html:889–945`) runs **one timeline**: a single `dur = 850`, a single
`t0`, a single `requestAnimationFrame` loop, and **one sweeping angle** `angAt(t)` that crosses the
whole ring. Segments *appear* to hand off only because a single angle crosses them in order. The
velocity envelope is explicit in the code: accelerate through the first segment's arc (`ta`), cruise at
constant speed through the interior (`tc`), decelerate through the last segment's arc (`td`).

⇒ **That is already Dave's easing rule** — ease-in first, linear middle, ease-out last — implemented as
one continuous curve rather than as N per-segment timelines.

**The finding, stated precisely because the imprecise version is misleading:** *"same as the pie"* is
**true of the easing and false of the appearance** under DV-D16's in-force wording ②. The donut is
serial-*looking*; wording ② explicitly rejects that look for stacks (*"they all grow at the same
time… floating and growing, rather than growing and handing off"*). What genuinely carries over from
the donut to the stacks is the **architecture** (one shared timeline), the **easing envelope**, and the
**`prefers-reduced-motion` answer already baked at `:901–906`** — land on the final frame, never
animate. That is worth more than the appearance would have been.

## 1. The second finding re-priced DV-D16 downward, which is the rarer direction

Reading `Chart-bar.reference.html:121–128` to scope DV-D16: every stacked segment already runs
`scaleY(0) → 1` from `transform-origin: bottom`, **all at once**, on one `--grow: 760ms`, CSS-only per
DEF-003. **Concurrency already exists.** Two things are missing, and only two:

1. the upper segments do not **float** — each grows from its own fixed anchor, so the stack gaps
   mid-animation instead of staying contiguous;
2. all segments share one `cubic-bezier(.22,.61,.36,1)` — there are no per-segment curves.

Both are reachable in pure CSS (the cumulative height below each segment is static per chart, so it can
be a per-rect custom property emitted at generation time), so **no JS enters physics** and B-D7 /
DEF-003 hold. ⇒ DV-D16 re-priced from ~30% to ~19%. Recorded because a *downward* re-price is the one
nobody double-checks, and it should be re-verified before the build, not inherited from this note.

## 2. DV-D17 — the enactment, and the one call inside it that was mine

The fix is four lines in `canon/dv-legend.js`: when a blank swatch is checked while isolated,
`st.isolated = null; st.focus = null;` and the legend leaves isolate mode. All three of the ruling's
named bites are covered — restore to `visible[]` not all-on; Reset must not self-disable while the view
is still filtered; the release must be announced on the add path.

**⚠ MY CALL, NOT DAVE'S, AND UNRULED AT WRITE TIME.** The release also sets `st.visible[id] = true`, so
the clicked series is showing afterwards. The ruling's letter is *"restore to `visible[]`, not to
all-on"*, and the strictly literal reading restores `visible[]` **alone**. Both avoid the failure the
bite exists to prevent (releasing to all-on would silently make this gesture a second Reset). The
difference is felt only in one case: if a series was dimmed **before** isolating and is then the one
clicked, the literal reading leaves it dimmed — so the click that ended the mode appears to do nothing
to the thing that was clicked. I chose the reading that honours the gesture. **It is one line either
way and it is flagged for Dave in `§C` and in the ledger's ENACTED block, not quietly canonised.**

**Also removed, not merely left unreachable:** the old `st.isolated ? ' added'/' removed'` announcement
branch. Under DV-D17 the focus set is always a singleton, so the add path releases above it and the
remove path is refused by the floor guard. Leaving code that enacts a superseded model in canon is how
a later reader reconstructs the wrong behaviour from the source — the same class of hazard as a stale
rule reading ([[stale-reading-failure-mode]]).

## 3. The finding worth the session: **six green checks were asserting the superseded ruling**

Baseline before the fix: members suite **100/100**, donut exemplar **27/27**. After the fix: **85/100**
and **23/27**.

That red is not a regression. Six checks — members 20/21, donut 12/13/14/20 — encoded the *additive
focus set*, which is exactly the half of DV-D11 that DV-D17 supersedes. **A conformance suite is an
inscription of a ruling, and it goes stale the same way prose does.** Nothing in the repo connected
"DV-D17 is ruled" to "six assertions now state the opposite"; the only thing that surfaced it was
running the suite. Sibling of [[assertion-propagation-gap]] — the gate fires on a flip, so a check that
is *known-wrong-now* is never chased — and a candidate instance of it in a surface nobody had counted:
**the verification tooling itself.**

Each was **rewritten, not deleted**, with its old wording preserved verbatim in a comment beside it. A
suite that quietly changes what a numbered check means is how a reversal reads as agent drift — the
same reason B-D7 and DV-D16 both keep both beats in the ledger.

**Donut check 20 is the one to look at, because it names a consequence the ruling did not.** It read
*"+Savings → 1250 / 54%"*: under additive focus, checking a second series **grew** the centre readout.
Under DV-D17 that same click ends isolation, so the selection becomes the whole visible set and the
centre snaps back to `2320 / 100%`. **DV-D13 is intact** — the centre still follows the selection; the
selection is simply everything again. But it is a *felt* change to a component Dave signed off
separately, it was not named in the accepted-cost line, and it is now flagged for his eye.

## 4. Bite-the-bite, three ways — and the one it does not catch

Per the standing rule, every proof ships with a bite proving the proof can fail. Rather than mutate
canon to do it, both suites gained a `DVLEGEND` env override (the same idiom the files already use for
`JSDOM`), so a neutered copy can be pointed at from outside. Three copies, one per named bite:

| neutered source | members | donut |
|---|---|---|
| full revert to additive focus | 99/108 | 23/27 |
| release, but to **all-on** | 105/108 | **27/27** ⚠ |
| release, but **silently** | 104/108 | 26/27 |
| **control — real canon** | **108/108** | **27/27** |

**⚠ The donut suite cannot catch the all-on regression, and the table is published so nobody assumes it
can.** Its scenario begins from the all-visible state, where `visible[]` and all-on are indistinguishable.
Only the members suite detects it, because only it deliberately dims a spare series **before** isolating.
That asymmetry is the whole reason the "not all-on" check needed its own setup rather than riding on the
existing sequence.

## 5. The byte cap did its job, and the job it did was on me

First commit of the fix carried ~1.9KB of explanatory comment and pushed `dv-legend.js` to **17123
bytes against ADR-0015's 16384 cap**. The gate blocked the build. The comment was restating the
ruling's arc inside the source — which the file's own header forbids in as many words: *"The models are
inscribed in `_proforma/_DATAVIZ-DECISIONS.md` — this file ENACTS them and does not restate the arc."*
Trimmed to the invariant plus a pointer; **16330 bytes, 54 to spare.**

**That 54 bytes is the real finding.** The dataviz behaviour group is at **90% of its 32KB page budget**
and `dv-legend.js` is at **99.7% of its own 16KB cap**. The next behaviour change to this group does not
fit. Which makes §6 not housekeeping.

## 6. I read a gate's advice text as live state — and the correction is the better finding

**First write-up of this section, wrong, kept because the correction has to be as loud as the claim:**
`_check_legend_migration.py` → **exit 0, WAVE COMPLETE**, while `GOOD-MORNING`, `_LIVE-STATE` and memory
all still said *"combo + line remain"*. I concluded that exit 0 was **an unclaimed authorisation** to
delete `dv-behaviour.js`'s transitional block, and wrote it into the banner, the spine and DO-FIRST as
*"the relief valve"* for §5. It got as far as ritual step 3 before a memory file I hadn't yet read
contradicted it.

**What is actually true, verified three ways:**

- The record staleness is **real**. `ba336dc` migrated combo and line; GM, `_LIVE-STATE` and one memory
  hook all still described the pre-`ba336dc` world. That half stands.
- **The cleanup was already done, by that same commit.** `dv-behaviour.js:146` is a **tombstone
  comment** where the transitional block used to be; the file is **13,004 bytes**, matching the
  15,771 → 13,004 drop recorded at the time.
- **The gate prints that todo list unconditionally** — `_check_legend_migration.py:87–89`, three bare
  `print()` calls under the WAVE-COMPLETE branch. It is **static advice, not a worklist.**
- **`class="dv-legrow` stays in the members' `extraContracts` deliberately**, not by omission:
  promoting it to the universal contract **fails the build**, because sparkline and scatter sit in the
  dataviz *group* but carry no legend. **The group is broader than the capability.**

**The method finding, which is the part worth keeping:** the instrument said one true thing (exit 0)
directly beside one stale thing (its remediation list), and I took the whole output as current. Sibling
of [[gate-narrows-its-own-rule]] — there a gate encoded one mechanism *as* the rule; here a gate's prose
outlived the state it described. **A gate's exit code is evidence. A gate's advice text is prose, and
prose carries drift** ([[trust-the-spine-not-the-prose]]).

**And the corrected version of §5 is worse, not better:** there is **no cleanup left and no relief
valve.** `dv-legend.js` sits at **16330 / 16384** and the group at **90%**, and nothing cheap buys space
back. The known fix is on the board already and is **Dave's call rather than an enactment** —
**per-member behaviour opt-in in the registry**, a schema change, the same item `Chart-sparkline`'s
inert 15.6KB payload has been waiting on since 07-26. **Until that lands, the next behaviour change to
this group does not fit.**

## 7. What I got wrong, and what the author flags against his own work

- **I priced DV-D17 at 15% and it ran closer to 20**, entirely on the byte-cap detour — which was
  self-inflicted (§5), not a discovery. Recorded per the throttle's instruction to record every overrun
  so the 15% reserve can eventually be re-derived from something.
- **`108/108` and `27/27` are DOM assertions, not renders.** jsdom proves the state machine; it does not
  prove `.is-solo` stops painting in a real engine. **ds-018 is a live, open counter-example on this very
  component** — CSS correct as authored, wrong on screen. Anyone reading this dossier as "DV-D17 is
  done" is reading it wrong: it is **enacted, DOM-proven, render-OWED.**
- **The members suite is 108 checks, not the "54/54" the handoff and memory both carried.** It was 100
  before this session. A stale count in three places is small, but it is the same failure class as §6.
- **§1's downward re-price of DV-D16 is the claim I am least willing to vouch for.** It was read from
  source in a few minutes, it makes the next job look cheap, and a cheap-looking job is exactly what
  the throttle exists to be sceptical of. Re-derive it before building, do not inherit it.
- **§6 was WRONG when first written and shipped into three files before I caught it.** Worth naming
  plainly: I wrote a confident finding — *"an authorised cleanup is sitting unclaimed"* — into the
  banner, `_LIVE-STATE` and DO-FIRST on the strength of a gate's advice prose, without checking whether
  the work it described had already been done. **What stopped it was ritual step 3**, reading a memory
  file, i.e. luck of ordering rather than any gate. Had the session ended ten minutes earlier, the next
  window would have opened on a Polaroid instructing it to redo finished work. **This is the exact
  failure mode this project names as its worst — confident false inscription — committed by the agent
  that wrote the warning into the same file, in the same hour.**

## 8. Resolved state / still open

**Resolved:** DV-D17 enacted in canon and injected into all 5 registered consumers · both jsdom suites
extended, green, and proven able to fail three ways · build **60/60 GREEN exit 0** · step 0's question
answered with a finding · DV-D16's scope measured down to two concrete deltas.

**Open, and each has a standing home:** the **render-verify in the licensed cut** for DV-D17 (§C·4 —
pair it with ds-018's `getComputedStyle` diagnostic; same page, same harness, same two widths, one
spin-up instead of two) · the **`st.visible[id] = true` call** (§2 — Dave's to reverse, one line) · the
**centre-figure consequence** (§3 — his eye) · the **transitional-block deletion**, now authorised (§6)
· `dv-legend.js` at **99.7% of cap** (§5) · everything carried in from #4–#6 unchanged.
