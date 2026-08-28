# The verifier probe registry (`W-45`, ruled `s204-D1` item 2)

**One scripted probe per historically-found defect class, a `caught:` ledger that IS the
promotion evidence, and a promotion rule that emits candidates but never promotes.**
Built #206. Home of the live facts about the registry; the programme scope lives in
`notes/_briefs/2026-08-19-204-mechanisation-programme-v1.md` § Item 2 and is not restated here
(ADR-0017 write-once: one home, addresses elsewhere).

## What is here

| file | what it is |
|---|---|
| `manifest.jsonl` | the registry. One row per probe: class · script · environment · **blind spots** · `caught` ledger. Schema in `_registry.py`'s docstring. |
| `_registry.py` | manifest schema + LOUD loader (unknown key = parse failure) + the runner. |
| `_promote.py` | the twice-caught rule as code. Emits candidature text; **writes nothing**. |
| `probe_meta_schema.py` | P-1 · component metas vs `meta.schema.json` (#204 C-8). |
| `probe_dup_ids.py` | P-2 · duplicate `id` + unresolved IDREF in review pages (#204 NEW-1). |
| `probe_dangling_var_pixel.py` | P-3 · dangling var → silent black, **from pixels** (#184 `s184-D3`). |
| `probe_premise_store.py` | P-4 · premise-vs-store diff (#203 lane H, #204 G-c). |
| `probe_stale_figure.py` | P-5 · carried figure vs live measurement (#173, #203). |
| `probe_input_trim_enactment.py` | P-6 · **canary**: the day a browser enacts `text-box-trim` inside form controls (#209 baseline). Its green is an INVERSION — findings=0 means nothing has changed. |
| `probe_container_self_query.py` | P-7 · a `@container` rule aimed at its own container — the rule can never fire (#210 ×3). |
| `probe_dangling_var_text.py` | P-8 · `var(--x)` with `--x` declared nowhere reachable, from TEXT (#184, #210). The sandbox tier of P-3's class. |

## How to run it

```bash
python3 knowledge/_probe_registry/_registry.py --list        # the manifest as a table
python3 knowledge/_probe_registry/_registry.py --run         # drive every probe (rc=1 on findings)
python3 knowledge/_probe_registry/_registry.py --selftests    # every probe's plant-then-detect
python3 knowledge/_probe_registry/_promote.py                # twice-caught candidates
```

P-3 needs a browser. Stage it per `knowledge/_RUNBOOK-render-verify.md`, then:

```bash
export PYTHONPATH=/var/tmp/pylibs PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-s197 \
       LD_LIBRARY_PATH=/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu TMPDIR=/var/tmp
```
Without it P-3 **REFUSES BY NAME and exits 77 COULD-NOT-ASK** (`knowledge/_could_not_ask.py`,
the #193 convention: exit 77 + a first line beginning `COULD-NOT-ASK:` carrying its own reason)
— it never reports a pass it did not measure, and ⛔ #208 a consumer can now tell that refusal
from the `1` a MEASURED finding returns. `_registry.py --run` prints refusals in their own
block and excludes them from its exit code (the `_build_survey.py` posture); a refused probe
does not fail the run and does not pass it.
Skip it deliberately with `--skip-env sandbox-render`; the skip is printed, never silent.

## Declared boundaries

- **NOT wired into `_build_all.py` or CI.** `s204-D1` forbids that until the registry has been
  driven in ≥ 1 real wave. Promotion of any probe to a gate is **Dave's** (derivation
  governance) — `_promote.py` proposes, and its selftest proves it leaves
  `_DS-IMPROVEMENTS.md` untouched.
- **A green registry run proves THE PROBES RAN, not that the tree is clean.** Every row carries
  a `blind` field for exactly this reason, and the runner prints that sentence on every run.
- **Environment split (#173):** P-1/P-2/P-4/P-5/P-7/P-8 are pure python and run anywhere python
  does. P-3 and P-6 are `sandbox-render` and are **UNPROVEN IN CI** — `s204-D1` item 5 owns the
  CI pixel leg.
- **⛔ NO FINDINGS COUNT IS TYPED IN THIS FILE, AND THAT IS THE #221 REPAIR.** Until #221 this
  bullet read *"P-7 and P-8 are NOT green on the current tree, and that is deliberate (#210) …
  P-7 6 findings + 3 WARN, P-8 58 findings in 9 files."* **Both probes were repaired at #211**
  — P-7 at `knowledge/snippets/Layout-utilities.reference.html:244`, P-8 at its generator cause
  (`knowledge/gen_token_ramp.py:28`, *"HTML COMMENTS ARE NOT CSS, AND THIS GENERATOR NOW KNOWS
  THAT"*) — and **nobody told the registry**. Driven on the default globs at #220 and again at
  #221 both read `findings=0`, so this file asserted **64 standing findings that do not exist**,
  for nine sessions. Anyone briefing off it carried a false premise.
  That is exactly the class **P-5** exists to catch — a stale carried figure — sitting in P-5's
  own registry, outside P-5's population. [[conclusions-are-debt-s129-d5]]
  **The fix is not a corrected number, it is no number.** A findings count is a property of a
  MOMENT, so its ONE home is a probe RUN and this document carries the ADDRESS (ADR-0017):

  ```
  python3 knowledge/_probe_registry/_registry.py --run --survey    # every probe, rc=0 always
  python3 knowledge/_probe_registry/_registry.py --run --probe P-7 # one probe, rc=1 on findings
  ```

  The last reading taken that way — **#221, 2026-08-27**, quoted from the runner's own summary,
  not retyped from a report — was `P-1 0 · P-2 0 · P-4 52 · P-5 0 · P-7 0 · P-8 0`, with **P-3
  and P-6 COULD-NOT-ASK** (playwright not importable in that sandbox; a refusal, not a pass).
  ⚠ Read that as a DATED RECEIPT, never as the current state: if you need today's number, run
  the command. Repair of any standing finding, and promotion of any probe to a blocking gate,
  remains **Dave's**.

## Adding a probe

1. Write `probe_<class>.py` here with `--check` and `--selftest`. `--check` must print a last
   line `PROBE <id> — findings=<n>`; the runner parses that.
2. The selftest must **DRIVE the probe on a planted artefact**, both directions (plant → fires;
   clean → silent), plus any control that keeps a known false-positive shape closed.
   [[mutation-tests-the-clause-not-the-feature]]: asserting on the probe's own clause is the
   #104 failure repeated.
3. Add a `manifest.jsonl` row with its receipts. `python3 _registry.py --selftest` fails if the
   manifest does not parse or a receipt pointer is dead.
4. Plant nothing inside the repo: the sandbox cannot unlink under the repo mount. Copy out to
   `$TMPDIR` (P-3 rewrites relative links to `file://` for exactly this).

---

## READY-TO-PASTE — verifier-PM brief paragraph (the consumer at birth)

> **Run the registry, then hunt free.** Start with
> `python3 knowledge/_probe_registry/_registry.py --run` (add
> `--skip-env sandbox-render` only if you cannot stage Chromium per
> `knowledge/_RUNBOOK-render-verify.md`, and say so in your report — a skipped probe is a
> declared gap, never a pass). Paste the run summary table into your challenge table and open a
> challenge row for every finding, with the probe id as its evidence token. **Then hunt free,
> and budget real time for it: the registry only covers classes somebody already found, so by
> construction it CANNOT find a new one.** Every probe publishes a `blind` field — read them,
> and treat them as your hunting ground rather than your excuse. A green registry run means the
> probes ran; it does not mean the tree is clean, and a verifier who reports "registry green"
> as a verdict has narrowed the hunt to yesterday's defects. If your free hunt finds a class the
> registry missed, that is the wave's most valuable output: add a `caught:` ledger entry (
> `provenance: "live-run"`) and, if a probe for it does not exist, price one — a class found
> twice is a candidate gate under `_promote.py`, and promotion is Dave's.
