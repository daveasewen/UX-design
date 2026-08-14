# #172 — bounded verification, and the labels that were ratified on the page

provenance: 172 · 2026-08-14
status: ruled — `knowledge/_rulings.json` § `s172-D1`, `s172-D2`, `s172-D3`

*Written at the #172 wrap by a delegated OPUS wrap sub. Spine entry: `_LIVE-STATE.md` ⏱ LATEST
DELTA #172 · ledger: `knowledge/_rulings.json` entries 150–152 · banner: `GOOD-MORNING.md`
★ LATEST #172. ⚠ Every gauge figure and every Dave quotation in this dossier is **RELAYED by the
conductor** — a sub cannot measure the conductor's window or read its transcript, and nothing here
was estimated in to cover the gap.*

---

## Why the session existed at all

The goal was Dave's and it was not an engineering goal: **get back to creating components** at the
weekend or next week. Everything #172 did was clearing the path to that. The plan was written down
rather than carried in the conductor's head — `_PLAN-172-back-on-track-2026-08-14-v1.md` — with
three strands: enact the Memento changes from the borrowed-instruments brief, wire the tokens and
atomic system ready for component work, and label everything on the dashboard as Apollo vs Memento.

The opener measured a **fresh quota week** (session 12% · weekly 4% · Fable 6%). That reading is
what licensed the shape of the day: **delegation is cheap in QUOTA and expensive in nothing else
this week**, so the window — not the weekly budget — was the binding constraint, and the correct
move was to push work into subs and keep the conductor's window for decisions.

## Finding 1 — the plan block got built, and the honest part is what it does NOT do

B2 of the borrowed-instruments brief is a regenerated plan block at lane seams. It landed:
`--block` / `--verify-block` / `--selftest-block` in `knowledge/_checkin.py`, plus a paragraph in
`knowledge/_RUNBOOK-context-gauge.md`. Both mutation tests were **driven to rejection, rc=3, each
with a passing control**, and the selftest goes red when its own checker is sabotaged. By the
standard this repo uses, that is a verified enactment.

And then the residuals, which are the part worth keeping:

- **The block is wired into no seam.** Its consumer is the conductor, by hand. Mechanising it into
  `_capture_gate.py` is priced at 30–45 minutes and was not done. This is the
  [[instrument-without-a-consumer]] shape *declared at birth* rather than discovered three sessions
  later — which is the only version of it that is cheap.
- **`_lanes.json` has been stale since Jul 28**, so the DOING line renders `step UNKNOWN`. That is
  the block being honest, not the block being broken. Worth saying out loud, because a reader who
  sees `UNKNOWN` and assumes a bug will go and "fix" a correct output.
- **`BLOCK_MAX_AGE_S=900` is PICKED, not derived.** It is overridable and it is declared as a
  choice. A number that looks like a measurement and is not one is how a threshold acquires
  authority it never earned.
- **A block run inside a sub measures the SUB's transcript**, never the conductor's. Same class as
  every other gauge figure a sub cannot see.

## Finding 2 — the labels were ratified on the rendered page, not off a list

`s172-D1`(5) had put the 37 `project` labels to Dave as **defaults for his eye**, with two flagged
as genuinely ambiguous (W-14 and G12). The engineering came first: a stored `project` field on all
37 items, proven with a **byte-identical round-trip** and an **untouched-fields** check taken
*before* the write; a presence gate in `_state.py::check()`, routed and driven to named refusals
(rc=1) with a passing control, taking the selftest from 41 to 57 arms; the label and an
All/Apollo/Memento filter in `gen_dashboard.py`; and the page regenerated **through the generator
only**.

Then Dave looked at the page and ratified all 37, settling both ambiguities in one line:
***"I think memento is right, and your suggestions"*** — W-14 = memento, G12 = apollo. That is
`s172-D2`.

★ **The method point is the one to keep: the ratification happened against the artefact, not
against a proposal.** A list of 37 label assignments in chat is a different object from 37 labels
sitting on a rendered page next to the items they describe, and only the second one can be judged
by eye. It is the same lesson `s170-D3` taught about the audit — the reader matters — pointed at a
human reader instead of a machine one.

Residuals, declared: the label **CSS is unproven in a real render** (~10 minutes of playwright, not
run) — the labels are ruled, the *rendering* of them is not proven; `_migrate_state.py` still
refuses (rc=1, fail-loud, pre-existing) and its fix was gated on exactly the ratification that
landed today, so it is buildable next window; `gen_dashboard --selftest` is not routed in
`_build_all.py`, pre-existing.

## Finding 3 — the appetite for instruments became a ruled quantity, and the fence came with it

This is the one that outlasts the session.

The measurement that provoked it is embarrassing in the useful way: **the B2 sub wrote 474
instrument lines around a 6-line emitter**, and the state-gate selftest went **41 → 57 arms**. Set
against that, the week's *real* catches were three, and every one of them came from proving that
**one** seam could fail:

| the catch | what actually found it |
|---|---|
| the self-comparing subject assert (#171) | driving the existing check on a doctored commit |
| the degenerate title parse (#169) | running the parser over the historical corpus |
| the fixture that passed on its own mutant (#171) | mutating the thing the fixture claimed to test |

⇒ **breadth of verification did not produce a single one of them.** Depth on one seam produced all
three. That asymmetry is the entire argument.

Dave adopted the bounded-verification template — five clauses, body homed by ADDITION at
`knowledge/_RUNBOOK-parallel-conductor.md` § BOUNDED VERIFICATION:

**(a)** the anti-over-engineering scope block goes into sub briefs near-verbatim (minimum
complexity for the current task; no abstractions for hypotheticals; no defensive code for
impossible scenarios; only the changes requested or clearly necessary) · **(b)** verification is
**TARGETED** — prove the seam *this* deliverable creates, never "verify everything you touch" ·
**(c)** a **DEPTH CAP** of one: a new check is proven able to fail once, and no checker checks a
checker beyond that · **(d)** every sub report declares its **instrument-lines vs feature-lines**,
reported and never thresholded · **(e)** an **OBSERVED-FAILURE RULE** — a new test cites the
failure class it guards or the ruling it enforces, and a speculative check queues as a proposal
instead of being built in the same breath as the thing it would watch.

Source for (a): Anthropic's prompting best-practices guidance, §§ *Overthinking and excessive
thoroughness* · *Overeagerness* · *Avoid focusing on passing tests and hardcoding*, fetched
2026-08-14 through one fetch plus one Haiku distill sub.

### And the fence, which is Dave's and is not a caveat

His condition, verbatim: ***"careful of externalities, I don't want to fix something only to break
other constituent parts."***

⇒ the template governs **the appetite for NEW instrument-building in FUTURE sub briefs, and
nothing else. It retires nothing.** Every existing gate, law, runbook clause and ruling stands
exactly as ruled. No existing check may be removed, relaxed, skipped or narrowed by citing
`s172-D3`, and a brief that cites it to justify not running something is misusing it.

★ **Why the fence is the load-bearing half.** A rule that says "build less machinery" is one
misreading away from a rule that says "run fewer checks", and the two are opposites: this repo's
machinery exists *because* checks caught things. The fence names the direction the rule points —
at the next instrument, never at the standing ones — so that the misreading has no textual
foothold. It was stated in the same breath as the adoption, not added afterwards, which is why it
is in the ruling rather than in a note under it.

⚠ And there is a deliberate self-application: **`s172-D3` has no gate.** Gating brief *prose*
would be the exact over-instrumentation the template rules against — clause (e) applied to the
template itself. It is discipline, the same class as `s165-D1`, enforced by being read at
brief-authoring time.

## What this wrap did NOT do, and why each one was a decision

- **`_build_all.py` was not run and not touched.** Its `#166` labels are exact-match join keys.
  The carried lane *"verify the audit's downstream consumers"* therefore got no window time — but
  it is **re-pointed rather than aged**: today's push hands CI the single-process full-build
  verdict, so **CI is the consumer**, and reading that verdict back is #173's opener item.
- **Nothing on the DO-NOT-RULE list was ruled**: `tooltip.tip` · base red 30 · the B3 fork's
  return-with-numbers · the gardener's first run · `_lanes.json` content · priority / deadline /
  effort values · any residual's status beyond aging it +1 · the 19 unconditioned items · the
  G-series.
- **No new instrument was built in this wrap.** Ritual, inscription, commit, push. `s172-D3`
  applies to the wrap that inscribed it, and a wrap that celebrated a new ruling by building a
  gate for it would have broken the ruling in the act of recording it.
- **The component lane is deferred** to the next window; the scaffold sub brief is not written.
  The weekend is Dave's-eye day (aesthetic leg · `tooltip.tip` · base red 30), then the first new
  component through the scaffold.

## One repair made during inscription, declared

Three `evidence` strings — one on `s172-D1`, two on `s172-D3` — lacked the `chat #<n>` legal
pointer form, and `_governs.py` refused them by name. They were repaired **by ADDITION**: a legal
prefix prepended, not one original word removed. The trigger-index selftest went from 5 fails to 4.

The remaining two are **pre-existing anchor rot** (`s129-D1`'s `_gauge_tokens.py#BOOT_FIRSTTURN_TK
= 54_859`, `s171-D1`'s `notes/_GAUGE-LOG.md#boot-drift …`): both point at text that no longer
exists on disk. ⛔ Repointing them at whatever currently looks right is the #127 re-stamp and is
not a wrap's call — carried as a residual instead.

## Resolved state, and what is still open

**Resolved:** `s172-D1` (six-item batch) · `s172-D2` (37 labels ratified) · `s172-D3` (bounded
verification, homed) · B2 enacted and mutation-verified · the dashboard project field, gate, label
and filter shipped.

**Open, in the order the next window meets them:** read CI's full-build verdict back (the
re-pointed audit-consumer lane) · write the component scaffold sub brief · wire the B2 block into a
seam (30–45 min) · the unproven label CSS render (~10 min) · `_migrate_state.py`'s refusal, now
unblocked · `_lanes.json`, Dave's · and the weekend's eye work: the aesthetic leg, `tooltip.tip`,
base red 30.
