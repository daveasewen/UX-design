# #286 lane G — the 256,000 wording fix, and the boot-cold finding

Lane G of Apollo #286. Two tasks: (A) enact Dave's #284 correction as a WORDING fix in the gauge
constants' provenance, and inventory every other place the repo calls 256,000 a hard wall;
(B) write the boot-cold finding file. **No constant moved. No band changed. Nothing committed.**

---

## TASK A — the `_gauge_tokens.py` 256,000 wording fix

### The finding, as the record states it

From `_HANDOFF-135-…md` (lines 95–105) and `_HANDOFF-136-…md` (lines 273–276), verbatim in
substance:

- Anthropic's help centre (*"How large is the context window on paid Claude plans?"*) gives
  **Fable 5.1 / Opus 5 in Cowork on a paid plan a 1M token context window**, with auto-compaction
  near the limit; tools and connectors are token-intensive.
- The conductor read that as a licence to re-base the stop line. ⛔ **Dave corrected him in the
  same turn: the 180,000 was gauged against the MESSY MIDDLE — a QUALITY line, not a wall line —
  and IT STANDS.** A FINDING, not a re-base.
- ⚠ What it changes is a **WORD**: 256,000 is called *hard* and is **not a wall for this model in
  Cowork**, so #277's, #281's and #282's "hard-line breaches" were **quality breaches, not crash
  risks**.

### What I changed — wording only

**`knowledge/_gauge_tokens.py`**

| where | change |
|---|---|
| provenance block above `BUDGET_HARD` (after the "performance gradient" line) | new `⛔★ WORDING CORRECTED #286` paragraph: 256,000 is a QUALITY/TOLERANCE line sourced when the window was 200K-class, NOT a context wall for Fable 5.1 / Opus 5 in Cowork (1M + auto-compaction); the quality line that binds is 180,000 (`STOP_LINE_TK`), gauged against the messy middle, and it STANDS; #277/#281/#282 were quality breaches; no constant moved and re-basing stays Dave's |
| `BUDGET_HARD = 256_000` inline comment | value untouched; comment now carries "⚠ NAME IS HISTORICAL: a QUALITY/TOLERANCE line … NOT a context wall … per Dave's #284 correction" |
| `main()` printed budget line | `hard 256,000` → `quality-max 256,000`, plus three printed lines stating the correction and naming 180,000 as the binding quality line |
| `assert_budget_clears_floor()` ordering message | `… < hard 256,000 must hold` → `… < quality-max 256,000 must hold` |

**`knowledge/_capture_gate.py`** (in-scope: `knowledge/*.py` printed strings/comments)

| line (post-edit) | change |
|---|---|
| ~141–143 | band recap comment: `hard 256,000` → `quality-max 256,000 — the figure formerly labelled "hard"…`, with the #284/#286 provenance |
| ~1377–1392 | `check_preflight_tokens` HARD-line fail: comment gains the #286 wording note; the printed fail now reads **"is past the QUALITY-MAX line (256,000; historically called the 'hard line')"** and adds *"It is a QUALITY line, not a context wall for this model (1M + auto-compaction)"*. **The fail itself, its trigger and the constant are unchanged.** |
| ~1396 | adjacent warn: "inside the hard line" → "inside the quality-max line" |
| ~4281–4285 | the `s244-D1` FILL-ceiling posture comment: note that "the wall" is the HISTORICAL name for 256,000 |
| ~6537–6540 | selftest fixture comment: "the HARD one" → "the QUALITY-MAX one", plus the #286 note. The fixture string and its `should_fail=True` are untouched. |
| ~6571–6578 | the pinned-triple failure message: `HARD is SOURCED (93% MRCR v2 at 256K)` → `BUDGET_HARD is SOURCED (93% MRCR v2 at 256K) and is a QUALITY-MAX line, NOT a context wall for this model (1M + auto-compaction — Dave's #284 correction, worded #286)`. The pin `(160_000, 200_000, 256_000)` is untouched. |

⛔ **`knowledge/_seam.py` NOT edited** — it is fenced by this session's standing constraints, even
though it is `knowledge/*.py` and prints the wall wording. Listed as owed below.

### Selftests, run after the edit

| command | result |
|---|---|
| `python3 knowledge/_gauge_tokens.py --selftest` | ✅ **PASS**, exit 0 — "counting path exact on 5 fixtures; cache hit fidelity + content-hash keying + corrupt-file robustness all bite; degraded-measurement honesty holds; band/floor guard logic verified relative to the live constants" |
| `python3 knowledge/_gauge_tokens.py --help` | ✅ prints the docstring, exit 0 |
| `python3 knowledge/_gauge_tokens.py` (main) | ✅ prints the new `quality-max` budget line and the three-line correction note; boot 87,688 ± 4,195, ceiling ⛔ OVER (pre-existing) |
| `_capture_gate.selftest_preflight_tokens()` (the ONE authority for the budget triple) | ✅ **PASS — zero failures**, called directly |
| `python3 knowledge/_capture_gate.py --selftest` | **4 fail · 3 warn — ALL FOUR PRE-EXISTING AND UNRELATED**: every one is `_governs.py` RED on rulings `s282-D2/D3/D4/D5` evidence lacking a `chat #<n>`/`commit ` pointer. No token/budget arm failed. |
| `python3 knowledge/_checkin.py --selftest` | ⚠ **ambiguous option** — argparse: could match `--selftest-block`, `--selftest-compaction`, `--selftest-disk`. Not a defect I introduced; recorded as measured. |
| `python3 knowledge/_checkin.py --selftest-block` | ✅ **8/8 arms** as specified |
| `python3 knowledge/_checkin.py --selftest-compaction` | ✅ **5/5 arms** as specified |
| `python3 knowledge/_checkin.py --selftest-disk` | ✅ runs, prints the live disk reading |
| `python3 knowledge/_checkin.py --window 200000 --no-block` | ✅ **still runs, exit 0** — full report emitted (FILL 138,556 real · boot 73,832 · rehearsal 6 structural fails, all pre-existing boot-ceiling / boot-double-count arms) |

---

## THE 256,000 INVENTORY — every other place it is printed or documented

Repo-wide grep (`256,000|256000|256_000|256K`), then filtered to lines that also carry
*hard* or *wall*.

### ⛔ OWED — prose / ratified surfaces, NOT edited (amending them is Dave's word)

**58 locations across 10 live files.**

| file | count | lines |
|---|---|---|
| `knowledge/_RUNBOOK-context-gauge.md` | **7** | 53, 60, 85, 372, 390, 872, 926 |
| `notes/_MEMENTO-DECISIONS.md` | 10 | 2006, 2013, 2229, 3599, 3956, 5239, 5385, 5568, 5748, 5835 |
| `knowledge/_rulings.json` | 10 | 93, 1334, 2389, 4023, 4026, 4056, 6947, 7984, 9546, 10623 |
| `notes/_RULINGS.html` | 9 | 181, 1098, 2541, 3491, 6285, 6314, 6315, 8005, 9939 |
| `knowledge/_state.json` | 8 | 1801, 1802, 9642, 10321, 10409, 10430, 10470, 10550 |
| `_LIVE-STATE.md` | 7 | 14, 83, 111, 113, 127, 131, 939 |
| `GOOD-MORNING.md` | 3 | 17, 42, 475 |
| `_CHAIN.md` | 2 | 42, 81 |
| `dashboard/index.html` | 1 | 7189 |
| `knowledge/_standing.md` | 1 | 17 — ✅ **already correct**: *"180,000 FILL is the QUALITY line and stands; 256,000 is not a wall for this model in Cowork (Dave's correction, #284)"* |

★ The sharpest two, quoted so the owed edit can be judged without re-reading:

- `knowledge/_RUNBOOK-context-gauge.md:85` — *"⛔ **256,000 stays the UNQUALIFIED wall (`s214-D2`)**"*
- `knowledge/_RUNBOOK-context-gauge.md:926` — *"200,000 is WORKING, 256,000 is the absolute hard stop…"*

Both are `s214-D2`-era rulings text. The runbook is RATIFIED; re-wording a ruling's own statement
is not a lane's to do.

### ⛔ OWED — code, but FENCED by this session's standing constraints

`knowledge/_seam.py` — **4 locations**, all the "HARD LINE" verdict:

- line 5 (docstring: *"#277 crossed the 256,000 hard line under pressure"*)
- line 32 (docstring verdict table: `BUDGET_HARD 256,000 → past it: "HARD LINE BREACHED"`)
- line 65 (printed: `⛔⛔ HARD LINE BREACHED (+N over 256,000)`)
- line 173 (the verdict tuple `(G.BUDGET_HARD, "HARD LINE BREACHED")`)

⇒ This is the one remaining **printed** wall wording in live code. It is a wording-only change of
the same shape as the ones above, and it wants whichever lane owns `_seam.py`.

### ▫️ HISTORICAL RECORD — listed, deliberately NOT owed

Amending these would be rewriting the record of what past sessions declared at the time:
`notes/_GAUGE-LOG.md` (64 hits), `_CARRIES.md` (62 wall-lines), `knowledge/_memento-index.json`
(244 — index of the above), `_GM-ARCHIVE.md` (65), `_LIVE-STATE-ARCHIVE.md` (62),
`_DECISION-HISTORY/*` (~22 files, 1–4 each), `notes/_briefs/*`, `notes/_subreports/*`,
`notes/_lanes/2xx/W/*` wrap artefacts, `outputs/_wrap*`, `knowledge/_tmp/wrap*`.

`_HANDOFF-135…md:103` and `_HANDOFF-136…md:275` already state the correction correctly.

`knowledge/_recall_probe.py:6` names the *"200,000–256,000 CONDITIONAL BAND"* — a band name, not a
wall claim. **No edit needed**; noted so a later sweep does not re-open it.

---

## TASK B — the boot-cold finding file

Written: **`notes/_lanes/286/BOOT-COLD-2026-09-18.md`**.

It states, as a reading and not a verdict (n=1 against n=1): **#286 boot 73,832 real** vs **#285
80,863 real**, delta **−7,031**; the ONE variable changed (the built-in Browser connector's 17
`mcp__Claude_Browser__*` tools set to BLOCKED at #285), with skills, computer-use and the three
remaining connectors held constant; what would make it a verdict (a second cold boot on the same
setup); and the next candidate lever (the next-largest connector's tool descriptions) declared
**UNMEASURED** — `_checkin.py` reports boot as one figure and its decomposition is `ds-025` item 1,
so no per-tool-description size was available and none is guessed.

⚠ Honest residual carried in that file: the last seven post-diet readings span 72,110–83,636 — a
spread of 11,526, **wider than the −7,031 delta** — so the direction is consistent with the lever
working and the magnitude is not established.

**Ceiling:** 73,832 is **3,832 over `BOOT_CEILING_TK` 70,000** — the breach continues (11th
post-diet reading over it) and `s240-D2`/`s241-D1` keep the literal **shrink-only**.

## ⛔ THE WRAP MUST LOG 73,832 **ONCE**

Read first-hand from `_checkin.py`'s live output this session — the rule it quotes is:

> `s241-D2`: ONCE, in the `post-mortem #N:` line

and the structural arm fires today on #243 (5 statements), #264, #272, #273, #274 (2 each), with
the stated harm: *"One reading counted twice displaces a real session from the derived band's
window."*

⇒ **The #286 wrap writes 73,832 exactly once, in the `post-mortem #286:` line of
`notes/_GAUGE-LOG.md`.** This lane did not append to that file, and
`notes/_lanes/286/BOOT-COLD-2026-09-18.md` is deliberately outside it.

---

## FILES TOUCHED

- `knowledge/_gauge_tokens.py` — wording only (4 sites)
- `knowledge/_capture_gate.py` — wording only (6 sites)
- `notes/_lanes/286/BOOT-COLD-2026-09-18.md` — new
- `notes/_subreports/2026-09-18-286-G-gauge-wording-and-boot-cold.md` — this file

Nothing committed or pushed. No constant, band, stop line or ceiling moved. `_standing.md`,
`_seam.py`, `_git_commit.sh`, `_logo_nodes.json` and `_state.json` untouched.
