# Receipt — #204 Lane 1 · CI repair (BUILD-PM, Opus)

*Written by the BUILD-PM under the `s203-D2` PM-topology trial, 2026-08-19.*
*⛔ No commit, no push, no `git checkout/restore/stash`. `knowledge/_rulings.json` NOT written (`git status --porcelain knowledge/_rulings.json` → empty).*
*⛔ `_build_all.py` NEVER run — the ~49s single-process hazard was not approached. Every regeneration below is targeted and individually timed.*

---

## Headline

**The brief named 4 CI steps. They are 4 steps but only 3 root causes, and the brief's working
hypothesis is half right.**

| CI step | Root cause | Regeneration debt from #203? | Now |
|---|---|---|---|
| `[3]` `_build_blast_radius.py --check` | stale generated artefacts | ✅ **YES** — hypothesis CONFIRMED | ✅ **rc=0** |
| `[110]` `_build_graph_mention_map.py --check` | stale generated artefact | ✅ **YES** — hypothesis CONFIRMED | ✅ **rc=0** |
| `[114]` `_gen_chain.py --selftest` | the chain/GM **compression ratio** crossed a threshold | ❌ **NO** — hypothesis FALSE | ⬛ **rc=1, STOPPED — decision named below** |
| `[13]` `_capture_gate.py --selftest` | **TWO** causes: it embeds `[114]`, **AND** an independent `_governs.py` failure the brief never named | ❌ **NO** — hypothesis FALSE | ⬛ **rc=1, STOPPED — decision named below** |

**All four reproduced locally first** (`rc=1` each, measured with a real exit code, not a piped
`tail`), so **none of them is the #173 "gate that cannot pass in one environment" class.**
The first probe I ran reported `rc=0` for all four because the exit code came from `tail`, not
from the gate — corrected with `$?` on an unpiped run before anything was concluded.

---

## Step 0 — premise table

| # | Claim (from the brief) | Probe run | Verdict |
|---|---|---|---|
| 1 | CI head is `3a88777` | `git log --oneline -5` → `3a88777 after #203 … s203-D2 PM-topology trial ruled for #204` | ✅ CONFIRMED |
| 2 | `[3]` fails: "2 file(s) out of sync with a fresh compute()" | ran it, `rc=1`, message verbatim names `tokens/_blast-radius.json` (43097 vs 49347 bytes) and `_GRAPH-REPORT.md` line 5 (**76** components on disk vs **85** fresh) | ✅ CONFIRMED |
| 3 | `[13]` fails, exit 1 | `rc=1` | ✅ CONFIRMED — **but the failure set is larger than the brief states (see finding 2)** |
| 4 | `[110]` fails, exit 1 | `rc=1`, "STALE — regenerate" | ✅ CONFIRMED |
| 5 | `[114]` fails: "materially smaller … (21,237 vs 51,204 tape, <40%)" | `rc=1`; the quoted figures are the **capture-gate fixture tree's**, not the live tree's — live is **34,250 vs 81,637** | ✅ CONFIRMED as a failure, ⚠ **figures re-measured; do not quote the brief's numbers** |
| 6 | Hypothesis: regeneration debt from #203's nine new components | the `_GRAPH-REPORT.md` diff (76→85 components) is exactly the nine | ✅ CONFIRMED **for `[3]`/`[110]` only** — FALSE for `[13]`/`[114]` |
| 7 | ⛔ `_build_all.py` is ~49s single-process | not tested — **the hazard was respected, not measured.** Targeted regeneration was sufficient | ⚪ UNTESTED by design |

---

## `[3]` and `[110]` — REPAIRED

```
python3 knowledge/tokens/_build_blast_radius.py     rc=0  (7s)  tokens=1033 referenced=119 components=91
python3 knowledge/_build_graph_mention_map.py       rc=0  (0s)  101 of 101 node(s) mentioned, 1090 record hit(s)
python3 knowledge/tokens/_build_blast_radius.py --check      rc=0  ✓ PASS (content, not mtime)
python3 knowledge/_build_graph_mention_map.py --check        rc=0  current (101 of 101)
```

Component count moved **85 → 91** across the regeneration: #203's nine plus **this session's six**.
Both artefacts are now fresh against a tree that includes the #204 wave, so the repair is not a
revert to a pre-wave state — it is forward.

---

## `[114]` — ⬛ STOPPED. Regeneration does not clear it, and the remaining levers are not mine.

Measured against the **live** tree after all regeneration was complete:

| quantity | tape | share of GM |
|---|---|---|
| `GOOD-MORNING.md` | **81,637** | 100% |
| generated chain, whole file | **34,250** | **41.95%** ❌ (threshold `< 40%`) |
| ↳ GM header + ★ LATEST, **carried verbatim** | 28,730 | 35.19% |
| ↳ `_LIVE-STATE` LATEST delta, **carried verbatim** | 2,938 | 3.60% |
| ↳ generated wrapper | 2,582 | 3.16% |

**The decisive number: the chain's MANDATORY verbatim content alone is 31,668 tape = 38.79% of GM.**
The bite's entire headroom is **1.21 percentage points**, and the wrapper — which carries the clauses
*other bites in the same selftest assert must be present* (the ds-021 unit naming, the "Do NOT now
open GOOD-MORNING.md" instruction, the exact-stamp fixed point) — costs **3.16 points on its own.**

⇒ **This bite is not satisfiable by anything `_gen_chain.py` can regenerate.** The generator's output
is defined as a verbatim copy of a section of `GOOD-MORNING.md`; its size is set by whoever writes
GM's ★ LATEST banner, not by the generator. The bite is nominally measuring the chain's compression
and is **actually measuring GM's wrap discipline**, while blaming the chain in its message.

Arithmetic on the three levers, so the decision is priced, not vague:

- move the `0.40` constant (`knowledge/_gen_chain.py:648`) — ⛔ **not mine; constants are Dave's.**
- shrink the chain by **1,596 tape** — that is **62% of the entire wrapper**, and would trade this bite against the sibling bites that require the wrapper's clauses.
- grow GM to **≥ 85,625 tape** (+3,988), or equivalently shrink GM's ★ LATEST by ~3,990 tape — ⛔ `GOOD-MORNING.md` is fenced from this seat, and it is a wrap-ritual act.

**Not touched. Not worked around. Recorded as UNPROVEN with the decision named**, per the brief.

⚠ `git status` confirms `GOOD-MORNING.md`, `_CHAIN.md` and `_LIVE-STATE.md` are **unmodified by this
wave** — so `[114]` was inherited from #203 exactly as CI reported, and this session neither caused
nor cleared it.

---

## `[13]` — ⬛ STOPPED, and the brief undercounted it

`_capture_gate.py --selftest` reports `capture gate [wrap]: 5 in scope · 4 fail · 2 warn`. Its three
`❌ selftest:` verdicts are:

```
❌ selftest: trigger index: `_governs.py` selftest is RED — 1 failure(s) … the consumer of
   _rulings.json is broken, so rulings stop surfacing and the #80 re-derivation becomes possible again
❌ selftest: trigger index: `_governs.py` selftest — _governs: an unrelated path matched a ruling
   — the matcher is too loose to carry information
❌ selftest: #70/#71 non-catch: _gen_chain.py --selftest is NOT green
```

The third is `[114]` re-reported. **The first two are an independent defect the brief does not
mention at all**, and it is the more serious of the two.

### The `_governs` defect, isolated to one line of data

`_governs.selftest()` arm 3 is a **negative control**: a fixed synthetic path
`knowledge/_totally_unrelated_xyzzy.py` must match **no** ruling, "if everything matches everything,
the index is decoration". It now matches:

```
RULING: s202-D3   governs = ['knowledge']
```

`s202-D3`'s `governs` list contains the bare token **`knowledge`** — the repo's own main directory.
The matcher cannot tell a bare *symbol* (arm 2's whole purpose — `measure_tokens`, `BAND_FLOOR`, …)
from a bare *directory name*, so `'knowledge'` matches every path in the repo, including the control.

**Sized, so it is a one-line class and not a vague worry:**

```
203 rulings · 77 bare-token governs entries · governs entries that are BARE DIRECTORY NAMES: [('s202-D3', 'knowledge')]
```

**Exactly one offender.** Every other bare token is a genuine symbol.

⚠ **This is not the #204 wave's doing** — `git status --porcelain knowledge/_rulings.json` is empty;
the file is at HEAD. It has been red since `s202-D3` was inscribed at #202.

### Why I stopped rather than fixed it

All three available fixes are out of fence:

1. **Edit `s202-D3`'s `governs` list** → ⛔ writing `knowledge/_rulings.json` is explicitly forbidden; only the conductor's `_inscribe_ruling.py` may.
2. **Tighten `_governs`'s matcher** so a bare directory name does not match → that **narrows what a RULED item governs.** `s202-D3` is Dave's, RULED, firm; re-scoping its reach is a ruling, not a repair (`gate-glob-scope-rule`: a rule is only as wide as its gate's glob — changing the glob changes the rule).
3. **Change the negative control's path** → laundering a red into a green.

**Recorded as UNPROVEN with the decision named.** The fix is one token in one ruling, and it belongs
to the conductor's inscription seat.

★ **The gate-class finding underneath it:** `_inscribe_ruling.py` is the *only* writer of
`_rulings.json`, and it accepted a `governs` entry that immediately turned the store's own consumer
selftest red — and stayed red across two sessions. **The writer does not run the reader's selftest.**
That is an `instrument-without-a-consumer` inversion: the consumer exists and runs, but nothing
gates the *write* against it.

---

## Regeneration NOT run, and why — declared, not silent

- `_build_memento_index.py` — `_capture_gate` reports the retrieval index STALE (the #32 defect). ⛔ **Wrap-ritual territory, and it is fed by `GOOD-MORNING.md`/`_LIVE-STATE.md`, both fenced from this seat.** Owed to the conductor at the wrap. ⚠ It also means `_memento_search.py` served a **previous session's record** to all three workers — every ruling claim in this wave rests on a **direct grep of `_rulings.json`** instead (`retrieval-default-hides-the-ruling`: store > chain).
- `gen_canon_components.py`, `gen_theme_cascade.py` — **these files do not exist** at the paths the #203 receipts name (`rc=2, No such file or directory`). The six new components are therefore **absent from `canon.css`**, and their review pages carry hand-mirrored `.cn-` scopes, not generator output. **Declared; the conductor owns the reconciliation.**
- `_build_integrity.py`, `gen_component_partials.py`, `gen_token_ramp.py` — not run. Declared gap.

---

## Files this lane touched

| Path | Change |
|---|---|
| `knowledge/tokens/_blast-radius.json` | **regenerated** (85→91 components) |
| `knowledge/_GRAPH-REPORT.md` | **regenerated** |
| `knowledge/_graph-mention-map.json` | **regenerated** |
| `knowledge/_validate_radius.py` | **edited** — 6 slugs into `MIGRATED_SNIPPETS` + a comment recording that all six measured **0 advisory hardcodes before** registration |
| `showroom/*.html` | **regenerated** — 7 written (6 new pages + `index.html`) |
| `knowledge/_REVIEW-SIGNOFF.md` | **appended** one #204 row (add, never trim) |
| `knowledge/_RADIUS-GATE.md`, `_SNIPPET-AUDIT.md`, `_A11Y-GATE.md`, `_ICON-SOURCE-AUDIT.md`, `_graph-mark-observations.jsonl` | gate side-effect outputs, rewritten by running the gates |

⛔ **`gen_showroom.CATEGORIES` deliberately NOT edited** — see the claim table, `M-4`.

---

## Consequences / pitfalls

- **The two stopped items are one commit away from being forgotten.** `[13]`/`[114]` will still be red in CI after this wave lands, and the wave's green gates say nothing about them.
- **`_governs` being red is not cosmetic.** Its own message says it: a broken `_rulings.json` consumer means *rulings stop surfacing*, which is the #80 re-derivation condition. Every session between #202 and now has been running with a degraded ruling-trigger index.
- **`[114]` will get worse, not better, at every wrap** that grows GM's ★ LATEST banner. 41.95% today; the gate fires above 40%. A post-wrap addendum of the kind #203 wrote is roughly what pushed it over.
- **The showroom regeneration published six PROPOSED components** into `showroom/` under the "More" bucket. That is the generator's own fallback, not a taxonomy choice — but it is visible, and Dave has not ruled any of them.
- **Not run:** `_validate_state_contrast.py` (a filtered run overwrites the tracked `_STATE-CONTRAST-AUDIT.md`), `_build_integrity.py`, `_build_all.py`, and the CI job itself. **Nothing here has been seen by CI.**
