# #166 — The ratchet +1 was an inert link

provenance: local_e612890d-6eae-485b-980c-d85337ce3766 · 2026-08-13
status: ruled — `knowledge/_rulings.json` § `s166-D1`

*Session #166, Thursday 2026-08-13. FABLE conductor in-window, one OPUS wrap sub (this dossier).
Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #166 · banner: `GOOD-MORNING.md` ★ LATEST #166 ·
ledger: `knowledge/_rulings.json` § `s166-D1`. This file holds the WHY and HOW; the ledger holds
the WHAT.*

⚠ **CONSEQUENCES, REPLAYED UP FRONT (`s165-D1`, one session old and enacted here by construction):**
narrowing a gate's scope is a **reduction in coverage** and must be read as one. The consequences of
`s166-D1`, stated before its arc: **(1)** `.css` files are no longer checked for a `type.css` pull —
accepted, because the check was **impossible to satisfy legally** there; **(2)** the 1101 baseline now
describes a **slightly smaller universe**, so it is not comparable line-for-line with the pre-#166
figure, and this dossier is where that discontinuity is written down; **(3)** the **31 live TYPE-001
fails on HTML are untouched** — if that number ever drops to zero, check the *scope* before believing
the *improvement*; **(4)** the repair pattern *"a gate fires where it cannot be satisfied ⇒ narrow the
gate"* is **only safe when the impossibility is structural**, as it is here, and is a bad habit
anywhere else.

---

## 1. Why the +1 was worth hunting at all

`#165` closed with the type ratchet **breached: 1102 against a declared baseline of 1101**, and the
breach carried a specific insult — the ratchet is a debt that **may only shrink**. Dave deferred the
hunt at #165; it came back as residual ④, and #166 opened on it.

A one-row breach is the worst size of finding: too small to be obviously real, too small to be
obviously noise. That shape is what decided the method. **The first question was not "what is the new
row?" but "is the instrument the same instrument?"** — because a validator that has been edited since
the baseline was set produces a +1 without anything in the corpus having changed, and that answer
would have made the whole hunt a category error [[attribute-the-diff]].

## 2. The per-file inventory diff — and the instrument's acquittal

The measurement was a **per-file inventory diff**: the full 1101/1102-row inventory as it stands now,
against the inventory of the corpus **as it was at the #119 baseline morning**, both eras' content
read with `git show <sha>:<path>`.

Two things fell out of it at once:

- **Every file was byte-identical in verdict except one.** `knowledge/canon/canon.css` moved
  **279 → 280**. Nothing else moved at all.
- **Both eras' validators agreed verdict-for-verdict** on the shared corpus. ★ **The instrument is
  acquitted** — the +1 is a real content change.

This is the step that could have been skipped, and skipping it is how a session ends up "fixing" a
corpus to satisfy a drifted measurement. The acquittal cost one command and bought the right to treat
every later finding as being about the repository rather than about the ruler.

## 3. The single row, and the commit that minted it

The new row is a **TYPE-001** — *"does not pull canon/type.css"* — on `canon.css`.

`git log -S` on the dropped strings named the commit without ambiguity: **`49ef4cb`, session #122,
2026-08-07**, which removed **two inert `<link … type.css>` strings from a comment block** inside
`canon.css`. The #122 session was doing something else entirely; the strings looked like dead
documentation, because they *were* dead documentation.

⚠ **And the baseline's own date is what makes this readable:** **1101 was measured at #119, the same
morning as the era being compared.** The +1 was minted three sessions later.

## 4. Why nobody saw it for forty-two sessions

Because nothing ran.

`_build_all.py` **died before step 1 from #158** — and, on the ratchet's own evidence, the ratchet was
not being run across **#122 → #164** either. That was the #164 finding, and this is its consequence
landing in a second place: ★ **the debt did not grow unnoticed because a person ignored it; it grew
because its consumer was not executing** [[instrument-without-a-consumer]]. A gate that cannot run
cannot fail, and a ratchet that never runs is a number in a file.

## 5. The finding that outlives the fix: mention is not use

The interesting part is not the +1. It is **what the old pass was made of.**

A `.css` file **cannot** carry a `<link>` element. There is no legal way for `canon.css` to "pull
`canon/type.css`" in the sense TYPE-001 checks. So for the entire life of the check up to `49ef4cb`,
`canon.css` passed TYPE-001 **because of an inert string sitting in a comment** — a mention, not a use.

★ **A gate satisfied by a MENTION is not a gate** [[gate-must-quote-what-it-forbids]]. The pass was
never evidence of anything; the failure is what finally made the emptiness visible. This inverts the
usual reading of a breach: the +1 is not a regression, it is **the moment a false green stopped being
told**.

## 6. The dead end that was declined

The cheapest repair available was to **restore the two strings**. It would have taken one edit, the
ratchet would have read 1101 within a minute, and every receipt would have been green.

It was declined and offered to Dave as option (2) with that property named: **it restores a fake
pass.** Option (3) — raise the baseline to 1102 — was worse in a quieter way: it converts a
structural impossibility into **permanent declared debt** that no future session can ever pay off,
because there is no work that would pay it.

## 7. The ruling, and the shape of the choice

Three options were put to Dave with the trade-off of each stated:

1. **Scope TYPE-001 to `.html`/`.htm`** (recommended)
2. Restore the inert string
3. Raise the baseline to 1102

Dave picked (1): ***"go for it."***

`s166-D1` therefore says: **TYPE-001 fires only on HTML files.** CSS files stay fully gated by
**TYPE-002/TYPE-003**, which are the checks that *can* be satisfied there. The **1101 baseline stands
unraised** — the whole point of the ruling is that no debt was actually incurred.

## 8. Enactment, and why the selftest asserts both directions

`knowledge/_validate_type_composites.py` gained a **commented scope clause citing `s166`**, and the
selftest gained **two** cases, deliberately:

- TYPE-001 **fires** on a `nolink.html` fixture — the gate still bites where it can be satisfied.
- TYPE-001 **does NOT fire** on a `nolink.css` fixture — the new clause is real.
- `raw.css` **still fails TYPE-002** — the control proving the narrowing did not quietly un-gate CSS.

★ A one-direction test here would have proved only that the file still parses. **The clause, not the
feature, is what needed the mutation** [[mutation-tests-the-clause-not-the-feature]].

**Receipts, re-driven at the wrap rather than relayed:** `--selftest` **rc=0** · `--ratchet` **rc=0**,
*"declared debt holds at 1101 (0 new)"* · `--inventory` **1101 rows** (1102 lines including the CSV
header — the unit is stated because the raw line count is precisely the number that looked like a
breach) · **TYPE-001 ×31 still live on HTML** · `knowledge/_type_ratchet.json` **baseline untouched**.

## 9. The stash mishap — recorded because the lesson is cheap and the loss was not zero

While measuring the two eras, the session used a **stash sequence** to hold and restore working state.
**`stash@{N}` indices reshuffle after every `git stash drop`**, and a drop-by-index step took the wrong
entry with it: the boot check-in's `rehearse` log line (`kind:"rehearse"`, `warns:14`) was lost.

The tree was **reconciled to `674880f` and verified clean**, and a later check-in appended a fresh
rehearse line, so **no repo content was lost** — but the honest form is that a measurement dance
destroyed a measurement record.

★ **The remedy is to stop dancing.** For reading a file as of another commit, `git show <sha>:<path>`
is a plain read with no stack, no indices, and nothing to reshuffle. The later measurements in this
very session used it. The lesson is inscribed in `knowledge/_RUNBOOK-capture-ritual.md` § 2c, beside
its sibling — the stale-ops-file trap #165 caused — because both are the same class: **a shared,
positionally-addressed resource consumed by a step that reads success from a green receipt.**

## 10. Resolved state, and what is still open

**Resolved:** the ratchet +1 is **attributed, ruled and closed**; #165's residual ④ is **consumed**;
the ratchet reads **PASS at 1101** with the baseline unchanged.

**Open, and none of it is this session's:** the **15 provenance fails** on `s157-D1`…`s163-D1`
(Dave's, target Friday 2026-08-14) · `s165-D4`'s **per-line link ratification** · the
**priority/deadline/effort values** · the **`_state.json` 400-char body truncation** (7 of 37 items on
the cap) · the **`#166` label strings in `_build_all.py`**, declared at #165 ⑫ and **deliberately not
edited — they are exact-match join keys** · the `_REVIEW-SIGNOFF.md` queue · the dashboard **v2** lane.

**Links:** ledger `knowledge/_rulings.json` § `s166-D1` · spine `_LIVE-STATE.md` ⏱ LATEST DELTA #166 ·
banner `GOOD-MORNING.md` ★ LATEST #166 · instrument `knowledge/_validate_type_composites.py` ·
predecessor finding `_DECISION-HISTORY/2026-08-12-164-the-gate-that-could-not-run.md`.
