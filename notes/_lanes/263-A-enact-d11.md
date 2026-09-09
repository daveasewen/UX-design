# #263 lane A — s263-D11 enacted: the source-text `requiredAria` arm is RETIRED

**Ruling.** `s263-D11` (Dave, #263, "P-11 ACCEPT"): *"`_validate_snippets.py`'s source-text
requiredAria arm is RETIRED; the DOM-driven arm in `_validate_dataviz.py` is the one gate for the
rule."* Governs `knowledge/_validate_snippets.py`, `knowledge/_validate_dataviz.py`.

**Done.** The arm is DELETED (no code path, no stub — nothing consumed its result shape). Its
bite-test in `_tests/test_gates.py` is deleted with it, because a bite-test for a retired arm is a
guaranteed RED. Four docs that claimed the arm exists are corrected. The driven arm needed no
wiring: `_validate_dataviz.py` is already `_build_all.py` STEPS line 395 (and its `--selftest` at
line 399).

## 1 — files changed

```
 knowledge/README.md                   |  2 +-
 knowledge/_A11Y-AUDIT.md              |  5 +++--
 knowledge/_RUNBOOK-gated-component.md |  7 +++++--
 knowledge/_tests/test_gates.py        | 23 +++++++----------------
 knowledge/_validate_snippets.py       | 28 +++++++++++++++++++---------
 5 files changed, 35 insertions(+), 30 deletions(-)
```

- `knowledge/_validate_snippets.py` — check §2 (the `requiredAria in html_sans_manifest` loop) is
  gone, replaced by an `s263-D11 RETIRED` comment block naming the fail-open evidence and the
  successor gate. Module docstring item 2 rewritten. **No other check touched** (the `mm` manifest
  match is still used at line 209 for `manifest`; `html_sans_manifest` had no other consumer).
- `knowledge/_tests/test_gates.py` — `mut_missing_aria()` and its `CASES` row
  (`"snippet gate bites on missing ARIA"`) removed, each replaced by a comment pointing at the
  probe that now carries the bite. CASES 30 → 29.
- `knowledge/README.md` line 87, `knowledge/_A11Y-AUDIT.md` (summary + the 4.1.2 row),
  `knowledge/_RUNBOOK-gated-component.md` step 6 — all three said the snippet gate checks ARIA.
  Corrected to name the driven arm. (`knowledge/_A11Y-GATE.md` never mentioned `requiredAria` —
  nothing to fix there. Root `README.md:14` says the *metas* declare required ARIA, which is still
  true; left alone.)

## 2 — who else consumes `requiredAria`

`grep -n requiredAria knowledge/*.py` after the change:

| file | role | status |
|---|---|---|
| `_validate_dataviz.py` | `required_aria_of()` + `driven_aria()` — grades declared strings against the RENDERED DOM off a driven receipt | **THE gate.** In `_build_all.py` STEPS line 395 already — no wiring change made or needed |
| `_drive_chart_engine.py` | records `aria.present` per figure per theme×mode; writes the receipt the above reads | unchanged |
| `_build_sutherland_fixtures.py` | copies `requiredAria` into the exported per-component contract | export only, no grading — unchanged |
| `_validate_snippets.py` | — | **no code path remains** (4 grep hits, all comment/docstring) |

## 3 — receipts, verbatim

**Snippet gate, before and after (identical — the retired arm had zero live findings):**

```
BEFORE: snippet gate: 137 snippet(s), 0 failure(s)      (exit 0)
AFTER : snippet gate: 137 snippet(s), 0 failure(s)      (exit 0)
```

**The delta the ruling asked for — same file, `role="img"` stripped from the MARKUP only
(manifest declaration left intact), HEAD's module vs. the changed one:**

```
BEFORE (HEAD)    : 1 error(s) on Chart-boxplot with role="img" stripped from the MARKUP; ARIA errors -> ['Chart-boxplot.reference.html: required ARIA missing: role="img"']
AFTER  (s263-D11): 0 error(s) on Chart-boxplot with role="img" stripped from the MARKUP; ARIA errors -> NONE
```

**The driven arm still BITES — `_validate_dataviz.driven_aria()` on Chart-boxplot, control vs. a
receipt with `role="img"` absent from the recorded DOM in one combo:**

```
declared: ['role="group"', 'aria-labelledby', 'role="img"', 'aria-label', 'aria-controls', 'role="region"']
CONTROL (fresh receipt, DOM as driven):
    ([], ['requiredAria [driven]: PASSED — all 6 declared string(s) present in the RENDERED DOM across 8 theme x mode combos.'])
MUTANT (role="img" stripped from the rendered DOM in combo console/dark):
    (['requiredAria [driven]: 1 of 6 declared ARIA string(s) are MISSING FROM THE RENDERED DOM in console/dark — role="img". They may still be present in the file as JS string literals; a gate that reads source text cannot tell.'])
```

**Self-test — `python3 knowledge/_tests/test_gates.py`:**

```
30 test(s), 1 failure(s)
skipped by design: state-contrast / screen --render (need a browser; see docstring)
  FAIL  control: pristine copy passes all 6 static gates — _validate_icons.py exit 1
```

The one FAIL is **not this lane's**: it is the icons control, and `_validate_icons.py` is RED on
the pristine repo for a pre-existing reason — `5 UNKNOWN, 102 bespoke, across 137 snippet(s)` /
`still UNKNOWN: 5 Legend`. Every ARIA-adjacent snippet-gate bite still PASSES.

## 4 — not done / obstacles, precisely

1. **D3's own probe could not be run here.** `knowledge/_tests/chart-engine/_probe_fail_open.py
   --expect red` dies at `ModuleNotFoundError: No module named 'playwright'` — this workspace has
   no browser. The driven RED was therefore driven the cheap way instead (§3, mutant receipt),
   which exercises the same clause in `driven_aria()`.
2. **Every driven receipt is STALE right now, repo-wide, and that is pre-existing.**
   `python3 knowledge/_validate_dataviz.py` → `❌ DataViz gate FAILED`, every row reading
   `the driven receipt for <chart> is STALE — knowledge/canon/type.css has changed since it was
   driven. Re-drive: python3 knowledge/_drive_chart_engine.py`. `knowledge/canon/type.css` last
   moved in commit `4cc4204` (#261 F2, today 10:58) — nothing to do with this lane, and the
   re-drive needs the browser this workspace does not have. Worth noting the practical effect:
   **the one gate for `requiredAria` is currently BLOCKING-on-stale, so the rule is not being
   graded until someone re-drives.** Flagging, not fixing — out of this lane's fence.
3. **Gate-run side effects left in the tree, uncommitted:** `_DATAVIZ-GATE.md`,
   `_ICON-SOURCE-AUDIT.md`, `_INTEGRITY-REPORT.md`, `_graph-mark-observations.jsonl`,
   `notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl` — reports the gates rewrite
   when run. Most were already dirty before this lane touched anything; `_DATAVIZ-GATE.md` now
   records the stale-RED state from my run. **Nothing committed** (per brief). Nobody else's files
   touched — `meta.schema.json` and `footer.meta.json` untouched, no stash/checkout/reset used.
