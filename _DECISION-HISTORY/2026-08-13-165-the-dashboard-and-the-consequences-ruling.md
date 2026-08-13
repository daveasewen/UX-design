# #165 — The dashboard got built, and the ruling that outlasts it is about consequences

```
provenance: 165 · 2026-08-13
status: ruled → knowledge/_rulings.json § s165-D1 … s165-D6
```

*Session #165, 2026-08-13 (Thu). Dave's 9am sidequest lane. Three OPUS build subs plus one
four-task sub, and this OPUS wrap sub. Dave live throughout. **SIX rulings, all his.***

Both-way links: `GOOD-MORNING.md` ★ LATEST #165 · `_LIVE-STATE.md` ⏱ LATEST DELTA #165 ·
`knowledge/_rulings.json` `s165-D1`…`s165-D6` · `_BRIEF-progress-dashboard-2026-08-13-v1.md` ·
`_PROPOSAL-links-backfill-2026-08-13-v1.md`.

---

## ① The ruling that will outlive the session it was made in — consequences are ALWAYS replayed

Dave, in his own words:

> *"we should always highlight potential consequences of our actions… replay them to me… in all
> the appropriate records and the state machine, and sub briefings"*

**Why it came up:** the session ran four subs, each of which made choices with downstream costs —
a routing verdict, a schema addition, a scoring model, a proposal — and each of those costs was
legible to the sub that made it and invisible to Dave until he asked. The pattern he named is not
"tell me what you did"; it is **tell me what this will cost me later, before I agree to it**.

**Why it is a standing instruction and not a gate.** No gate parses a sub brief, and no gate reads
a proposal. Writing "gated" beside this ruling would be a false inscription of exactly the kind
`[[gate-glob-scope-rule]]` exists to prevent. It is inscribed instead in three named places — the
records, `_state.json`, and every sub brief — and its enforcement is discipline, declared as such.
`s165-D1`.

**The honest residual:** this ruling is one session old and has been enacted precisely once — in
this dossier and this wrap's banner. Whether it survives contact with a hot window is unproven.

## ② Priorities: I generate, Dave overrules — and the mechanism matters more than the ruling

> *"I'm comfortable for you to generate priorities, I can always overrule them"*

The dead-end this avoids: a priority list that an agent authors **into a store** becomes a decision
nobody ruled, and it rots silently — the exact class `[[conclusions-are-debt-s129-d5]]` names. So the
ordering on the dashboard is a **score computed at generation time** from six weighted criteria whose
weights are **printed on the page**, labelled PROPOSAL on every surface, **never written back**, and
regenerated every build. It cannot rot into a decision because it does not persist.

Dave's override channel is an OPTIONAL `priority_override` integer on a `_state.json` item, validated
when present and displayed as "DAVE OVERRULED → n". ⛔ **No override value was authored by this
session, and none may be authored by any program.** `s165-D2`, `s165-D5`.

Where an input is missing, the item is still scored **and flagged LOW CONFIDENCE with the missing
inputs named** — the refusal to silently default an unknown (`[[feedback-measuring-tool-must-not-guess]]`).

## ③ Fail loud — a routing split was proposed, and Dave reversed it inside the session

The worklist store gate (`_state.py::check()`) and its selftest had existed **since #88 and run only
by hand** — an instrument with no consumer, the class `[[instrument-without-a-consumer]]`. Wiring them
was the fix. The wiring **declared a routing split**: selftest ABORT, store gate GATE, on the argument
that the gate's reds are *Dave's data* and a build he must fix before it completes is a gate making his
ruling for him.

**Dave reversed it: both arms ABORT.** The argument was wrong in its **premise**, not its principle —
the gate does **not** red on the 19 declared legacy items (declared debt passes by design), so the only
thing that can turn it red is a **NEW malformed item**: a schema violation an agent wrote, not a
decision Dave owes. And a GATE-routed red prints its remedy eighty steps from the end, where it is
read as weather. `s165-D3`, ENACTED and VERIFIED in-window.

★ **The generalisable form:** before routing a gate soft "because its reds belong to the human", check
whether the human's data can actually turn it red. Here it could not.

## ④ The dashboard — and the thing it measured that nobody had measured

`knowledge/gen_dashboard.py` + `dashboard/index.html`: exec summary · gates strip (MEASURED at
generation, never asserted) · stat cards · two plates · provenance panel · forward lane · kanban
(19/13/1/4) · scored priority with declared weights. Mono components, `swiss-design-system` aesthetic,
both Dave's calls from the #164 brief. Same law as the showroom: **built from the stores, never
hand-edited, regenerated as a build step, so it cannot rot.** Wired into `_build_all.py` this session
as step "dashboard sync", routed **GATE** in mirror of `gen_showroom.py --check`.

**What it found:** `links` coverage is **0 of 37** across the corpus. The dashboard reported it as a
flagged problem and repaired nothing — correctly; the dashboard REPORTS. Dave ruled the emptiness
**is** the defect (`s165-D4`). A backfill proposal was written with 6 of 37 candidates evidenced.
⛔ **No link was written to the store. Ratification is per-line and is Dave's, and it is OPEN.**

**Direction, his:** the interactive dashboard — *"dig deeper and manipulate"* — is a **v2 lane**,
future. v1 stays a report rather than smuggling interactivity in. `s165-D6`.

## ⑤ The findings — three of which contradict something the record believed

- **The tool-call wall is ~178s, not ~45s.** RE-MEASURED this session. The ~45s figure is what the
  chunking recipe in `_RUNBOOK-git-commit.md` § "build kills at call boundaries" was priced against.
  ★ **This is a premise ageing, not a rule ageing** (`[[premise-ages-faster-than-rule]]`).
- **The chunked full build COMPLETED in-sandbox for the first time** — and the verdict is a
  **LEDGER, 108/116 green, not a passed build.** Step 13 is a **declared skip** (Dave's 15 provenance
  fails) and step 69 is **UNMEASURED**. ⛔ **Calling this "the build passed" would be the false claim
  this record exists to prevent.**
- **The default `BUILD_ALL_STATE` path `/var/tmp/_build_all_state.json` is permanently poisoned
  in-sandbox** — the working recipe uses a session-suffixed path.
- **`LD_LIBRARY_PATH` must be `/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu`.** The short path
  **fakes a gate red**; the tell is `rc=2` with green arms, i.e. a crash wearing a failure's clothes
  (`[[a-crash-is-not-a-fail]]`).
- **`_state.json` bodies are truncated at 400 chars** — 7 of 37 items sit on the cap, so derivations
  are **under-read by construction**. Measured, not fixed.
- **The type ratchet is BREACHED: 1102 vs 1101.** ⛔ The +1 was **NOT hunted** — Dave deferred it.
  A debt that may only shrink has grown by one, and that is recorded rather than smoothed.

## ⑥ What is still open

`s165-D4`'s per-line link ratification · the 15 provenance fails on `s157-D1`…`s163-D1`
(**Dave's, targeted Friday**) · the ratchet +1 · priority / deadline / effort **values** (schema
approved, values his) · the v2 dashboard lane · the `#166` session-number discrepancy in
`_build_all.py`'s worklist comments (see the banner — declared, **not silently corrected**).
