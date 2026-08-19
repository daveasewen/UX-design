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
- **Environment split (#173):** P-1/P-2/P-4/P-5 are pure python and run anywhere python does.
  P-3 is `sandbox-render` and is **UNPROVEN IN CI** — `s204-D1` item 5 owns the CI pixel leg.

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
