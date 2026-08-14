# #170 — the msgfile was the mechanism, and the phantom was the instrument

provenance: 170 · 2026-08-14
status: observed

*The narrative dossier for session #170 (FABLE conductor + two OPUS build subs + one OPUS wrap sub,
Dave live). The WHAT lives in `knowledge/_rulings.json` (`s170-D1`…`s170-D4`), the ★ LATEST banner of
`GOOD-MORNING.md` and the ⏱ LATEST delta of `_LIVE-STATE.md`. This file holds the WHY and the HOW —
the corrections, the dead ends, and the two findings that were not on anybody's plan for the morning.*

Both-way links: `GOOD-MORNING.md` § ★ LATEST 2026-08-14 #170 · `_LIVE-STATE.md` § ⏱ LATEST DELTA #170 ·
`knowledge/_rulings.json` § `s170-D1` · `s170-D2` · `s170-D3` · `s170-D4`.

---

## 1. The twice-titled item was done first, and that is the whole story of `s170-D1`

`s165-D4` — per-line ratification of 37 link rows — had been the **titled item of #168 and of #169**
and had moved **zero rows in either**. Both sessions reported it faithfully at their wraps and then
did something else, because the titled item is what a session opens on and the first interesting
thing is what a session actually does.

#170 took it **first**, before anything else was opened. Six tier-A links ratified, 31 ratified
empty, **37/37, closed**. Nothing about the work was hard; what changed was the ordering.

★ **The lesson is about carries, not about links.** A carry that survives two headline slots is not
under-specified or blocked — it is being scheduled after the session's curiosity, and the only
repair available to a session is to spend the *first* tokens on it rather than the last.

## 2. Why the error-text rulings split into two (`s170-D2`, and the phantom behind it)

The three per-theme `rag/text/on-information` gating fails carried out of #169 were flagged there as
**LIKELY ARTEFACTS of the unapplied token-override leg — a recommendation, explicitly unconfirmed**.
#170 finished that measurement rather than acting on the recommendation.

Two different things were tangled in those numbers:

- **A real ink question.** console and supercharge were grading dark ink `#1A1A1A` on a palette-owned
  error ground at **2.89:1**. `s149-D1`'s dark-ink camp has always been scoped **MONO ONLY**, and
  `s131-D1` had already put legacy in the white camp. Dave ruled the obvious completion — white in
  console and supercharge too, **2.89 POOR → 6.02 OK in both** (`s170-D2`).
- **A phantom.** Alongside them sat a **1.0:1** pair, which is the signature of a value being graded
  against itself.

The 1.0:1 was **not in the data**. The audit was pairing **ink states against the wrong ground
state**; an ink state was being read against a ground that belonged to a different state, and in one
configuration that resolved to the same colour twice. Fixed (`s170-D3`), ink states pair with **their
own ground states**, and the phantom disappears — *because it never existed*.

★ **This is `no-gate-parses-the-artefact` in its most expensive form: the instrument's grammar
produced a defect-shaped number, and the natural repair — author a colour to make 1.0:1 go away —
would have "fixed" a reading rather than a surface.** It is the second consecutive session in which
the audit's *reader*, not the token data, turned out to be the defect (#169 found it had no theme
axis; #170 found its state pairing was wrong). Two findings, one class: **a measurement instrument
that has been extended faster than its own grammar.**

And the fix earned its keep immediately: with the phantom gone, a **real** gap was visible
underneath it — `button/primary/icon/default` in `apollo-legacy` at **2.42:1**. `s131-D1` had put the
legacy CTA **label** on white years of sessions ago; the **icon** had simply never been carried with
it. Dave ruled the mirror: **2.42 → 5.22 OK** (`s170-D4`).

⚠ **What was deliberately NOT done:** the base **red 30** (`rag/text/on-dark`, `#FFFFFF` on
`#F6604C`, **3.14:1**) was left exactly where it was. It remains the single base gating failure, and
adjudicating it was outside this session's brief.

## 3. The finding: twelve instances of a "discipline problem" were a write-back

The doubled-commit-subject class had **twelve recorded instances** and a remedy that read like
hygiene: *use a fresh `printf` msgfile every invocation, never `cp`*. It had been inscribed, gated
nowhere, and repeated.

This session produced instance thirteen — and the shape of it gave the mechanism away. The conductor
reused **one msgfile across three invocations** and the prefix came out **tripled**, not doubled.
A linear stack of prefixes, one per invocation, is not what a careless copy looks like; it is what a
**write-back** looks like.

And that is what it is. **`SESSION_N` mode GENERATES the `after #N <date> — ` prefix and writes it
INTO the msgfile.** The file that is the script's *input* is mutated by the script's *output*, so any
reinvocation reads a file that already carries a prefix and prepends another.

★ **Twelve instances were treated as a user failing because the remedy was stated in terms of the
user's behaviour.** Nobody had asked what would have to be true for the prefix to appear twice; the
answer was reachable at any point by reading the script.

Once named, the gate is trivial: `knowledge/_git_commit.sh` now **refuses any msgfile whose first
line already carries the prefix**. It was **driven to that named refusal first-hand, with nothing
staged**, rather than asserted — an unrun gate cannot fail, and a gate nobody has tried to cross is a
claim, not a fence.

⇒ **the class is closed at the seam unless the gate is evaded.** ⚠ And it is one session old: a
gate's real test is the wrap that tries to cross it *by accident*, which has not happened yet.

## 4. The second finding is about the channel, and Dave ruled it mid-session

The session opened putting decisions to Dave the way recent sessions had: **ID codes and buttons** —
a controller with row identifiers, pick-one affordances, a compact decision surface.

He stopped it, verbatim: ***"codes and buttons don't work for this particular human"***.

⇒ **decisions are put to him in PLAIN PROSE + VISUALS.** The id-level controller was **replaced
mid-session** by a prose-and-swatch walkthrough with structured plain-language choices, and
★ **all four of the session's rulings came through that replacement channel.** The ruling was not
merely recorded and honoured later; it was the instrument the remainder of the session ran on, which
is the strongest available evidence that it was the right call.

⬛ **His float is kept floated:** *"we'll have to write some empathy rules for you at some point."*
Recorded as **floated, Dave's** — not ruled, not scheduled, and ⛔ not to be enacted as if it were
[[memento-three-registers]].

★ **Why this belongs in a dossier and not only in a memory hook:** the decision surface is an
interface, and this session is the measurement that says the compact-code interface was optimising
for the wrong reader. A ledger line records the preference; only the narrative records that the
preference changed the session's own machinery in flight.

## 5. What is resolved, and what is open

**Resolved:** `s165-D4` closed 37/37 · per-theme error text OK in all themes (per-theme gating fails
**3 → 0**) · the 1.0:1 phantom gone at source · the legacy icon at 5.22 OK · the T3 prefix class
gated at the seam · both commits (`a21e357`, `832ccfa`) pushed on Dave's explicit word, remote
verified equal to local.

**Open, carried:** base **red 30** at 3.14:1, unadjudicated · the **empathy-rules** item, floated and
Dave's · four stale `rag/*-glyph` rows in `knowledge/_INDICATOR-CONTRAST-AUDIT.{md,json}`,
pre-existing and untouched · `_build_all.py` **not run**, so the audit's downstream consumers are
**unverified** rather than green · the T3 gate **unproven in anger**.

**Declared gaps, not estimates:** this wrap sub was relayed **no boot figure and no fill figure**, and
a sub cannot measure the conductor's window ⇒ the **effort rung is uncomputable** and is left
unwritten rather than banded by feel. Sub spend: **`subs 174079 tokens (n=2)`** — this wrap sub's own
spend excluded and unmeasured. Dave's quota panel was answered **loosely** (*"it refreshed last
night, we have loads of budget"*); the three numbers were not given and are **recorded as absent,
never defaulted**.
