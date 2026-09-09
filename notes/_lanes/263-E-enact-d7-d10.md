# Lane E — #263 — enact s263-D7 (dormant doormat) + s263-D10 (rulings-page wrap gate)

Both enactments landed. Nothing committed (conductor commits).

## Files changed

| File | What |
|---|---|
| `knowledge/components/footer.meta.json` | s263-D7 — `doormat` added to `variants[]` as a DORMANT variant carrying the whole #261 recipe; `$retired[0]` reduced to a one-line pointer. |
| `knowledge/_capture_gate.py` | s263-D10 — new `rulings_page_freshness_check(repo)`, called first inside `wrap_checks()` (lane wraps too), BLOCKING. Two stdlib imports added (`contextlib`, `io`). |
| `knowledge/_RUNBOOK-capture-ritual.md` | s263-D10 — new step **4d**, between 4c (scratch hygiene) and 5 (commit + push); step list in the header updated to `… 4, 4b, 4c, 4d, 5, 5b`. |

## diff summary

```
 knowledge/_RUNBOOK-capture-ritual.md  | 20 +++++++++++-
 knowledge/_capture_gate.py            | 59 +++++++++++++++++++++++++++++++++++
 knowledge/components/footer.meta.json | 20 ++++++++++--
 3 files changed, 95 insertions(+), 4 deletions(-)
```

Four further files are dirty as **side effects of running the validators/selftest**, not as edits:
`knowledge/_INTEGRITY-REPORT.md`, `knowledge/_graph-mark-observations.jsonl`,
`notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl`. Conductor's call whether they
ride along; nothing in them was hand-written.

---

## TASK 1 — s263-D7

**Shape check first, as briefed.** `grep -n dormant knowledge/components/*.meta.json` → **zero hits**;
no meta in the repo expresses dormancy, so there was no existing shape to reuse.

⚠ **ONE DEVIATION FROM THE BRIEF, AND IT IS THE SCHEMA'S DOING.**
`knowledge/components/meta.schema.json` defines `variants[].items` with
`"additionalProperties": false` and `patternProperties: {"^\\$": {}}` — only `name`, `use`, and
`$`-prefixed keys are legal. A bare `"status"` / `"why"` / `"recipe"` therefore drives the meta
validator RED (measured, verbatim, before I changed it):

```
variants/3 :: 'recipe', 'status', 'why' do not match any of the regexes: '^\\$'
```

So the keys are `$status: "dormant"`, `$why`, `$recipe` — the same `$`-convention this very file
already uses for `$status` on every prop, and the convention `navigations.meta.json::$since` and
`dropdown.meta.json::$ruling` use for extra variant keys. **The semantics the ruling asked for are
intact; only the sigil changed, to avoid editing a shared schema outside the lane fence.** If Dave
wants `status` as a first-class machine-readable variant field, that is a `meta.schema.json` edit
and his to rule.

**What the variant says.** `$why` cites s263-D7 verbatim (`"park — keep the doormat as a dormant
variant of Footer so it stays one component"` → `"dormant variant"`), states what dormant means
(declared, recipe kept, not built, not in any snippet or showroom, not reachable from the live
variant enum), and names Dave's accepted cost. `use` says it is the marketing/servicing mega-footer,
parked by s263-D7, not shipped in any app footer, recipe below.

**Props fence honoured.** `props[0].values` is still `["default","sticky","minimal"]` — `doormat` is
NOT in the live enum. `groups[]` and `backToTop` are NOT in `props[]`; they are recorded inside
`$recipe.$dormantProps` with a ⛔ line forbidding restoration to the live list without a build
decision.

**`$retired[0]` is now the one-line pointer:**

```json
{
  "what": "variant / prop value: doormat (the mega-footer), and the props groups[] and backToTop that served it",
  "retiredAt": "#261",
  "rehomedAt": "#263",
  "reason": "retired #261 → re-homed as dormant variant s263-D7; the recipe now lives in variants[] under name `doormat`, status `dormant`."
}
```

**`$finding-*` references intact** — `$finding-44px-cost` and `$finding-type-debt-conflict` travel
verbatim inside `$recipe.preserved`, and the top-level `$finding-24px-floor`,
`$finding-opacity-is-not-hierarchy`, `$finding-type-debt-conflict` blocks were not touched.

### Receipts — TASK 1

JSON parses, four variants, live enum unchanged, live props unchanged:

```
PARSE OK 4 variants: ['default', 'sticky', 'minimal', 'doormat']
props variant enum: ['default', 'sticky', 'minimal']
live prop names: ['variant', 'environment', 'systemStatus', 'dataFreshness', 'locale', 'legalLinks', 'copyright']
retired[0] keys: ['what', 'retiredAt', 'rehomedAt', 'reason']
```

Meta validator = `knowledge/_build_integrity.py` (step 1 SCHEMA: *"every components/\*.meta.json
validates against meta.schema.json"*). Footer's schema errors AFTER the change:

```
edges :: Additional properties are not allowed ('composes' was unexpected)
provenance/source :: 'redesign' is not one of ['figma', 'code', 'both', 'gap-report', 'proforma-promotion']
variant keys: ['name', '$status', '$why', 'use', '$recipe']
```

⚠ **Those two errors are PRE-EXISTING #261 debt, not mine** — `edges.composes` and
`provenance.source: "redesign"` were both red before this lane touched the file, and neither is
under s263-D7. The variants error I would have introduced is **gone**. `_build_integrity.py` itself
still reports its repo-wide `FAIL — 17 errors, 25 warnings` (Data grid, Filter-toolbar-bar, Footer,
…) — that number is unchanged by this lane.

Related validators run for completeness: `_validate_coverage.py` → `137 meta(s) / 137 snippet(s),
0 failure(s)`; `_validate_intent_resolve.py` → `RESULT: PASS`. `_validate_kg.py` and
`_validate_roles_resolve.py` are red on pre-existing rows (legend patterns, data-grid `with` slugs,
Footer's `composes` edge and unresolved `pattern:` refs) — none introduced here.

---

## TASK 2 — s263-D10

**(a) Runbook step 4d — LANDED.** Placed between 4c and 5, in the neighbours' voice (dated +
attributed opener, fenced commands, the *why*, the ⚠ trap, the gate's own home named). It cites
s263-D10 with Dave's words, says a STALE result is RED and blocks the wrap, points at the #32
retrieval-index precedent in 2g, and warns that `--check` alone is not the step — the rebuild is.
The header step list now reads `(1, 1b, 2, 2c, 2d, 2e, 2f, 2g, 3, 4, 4b, 4c, 4d, 5, 5b)`.

**(b) Wrap probe — LANDED, but NOT as a subprocess gate, because there is no such list.**
`_capture_gate.py --wrap` does **not** shell out to gate scripts: `wrap_checks()` is a sequence of
**in-process** check functions, and `index_freshness_check` states the reason in its own docstring —
*"rebuilds the records IN-PROCESS (no subprocess: the sandbox call-boundary lesson)"*. So the new
check follows that pattern exactly: it **imports `_render_rulings` and calls the renderer's own
`check()`**, capturing its FRESH/STALE line. One implementation of the freshness rule; the gate
cannot drift from the command Dave runs.

Wiring, minimal:
- new `rulings_page_freshness_check(repo)` immediately above `wrap_checks`;
- three lines at the top of `wrap_checks()` — **before** the lane branch, so it bites on LANE wraps
  too (`_rulings.json` is repo-wide; any seat can inscribe and stale the page);
- appends to `fails`, not `warns` — **BLOCKING at birth by Dave's word**, with no tier constant to
  dial on an agent's judgement (deliberately unlike `REGEN_SERIAL_BLOCKING` and friends);
- skips OUT LOUD on a tree with no `knowledge/_rulings.json` (fixture trees), in the house phrasing
  *"NOT a pass"*;
- `import contextlib` and `import io` added, each commented `s263-D10`.

### Receipts — TASK 2, verbatim

**RED arm** — one byte mutated in a *copy* of `_rulings.json` on a scratch path
(`"ruled"` → `"rUled"`, offset 1545), driven through `--src`/`--out`. The real files were never
touched:

```
mutated byte at offset 1545
--- --check with mutated --src against the real --out
STALE _RULINGS.html embeds a0c5b24ca0a6069896bccc884aa8a08bb58b14b34127a2f7711ab7fe6523f3ec but _rulings.json is now bd5107c41fcef1c4b18645fe3af16411327f0a4b5d88aa77c082cb5dd64db4ba
exit=1
```

**GREEN arm** — the real check, untouched files:

```
=== B. the real check
FRESH _RULINGS.html matches _rulings.json sha256 a0c5b24ca0a6069896bccc884aa8a08bb58b14b34127a2f7711ab7fe6523f3ec
exit=0
```

**THE GATE ITSELF DRIVEN** (mutation tests the CLAUSE, not the feature — the new function called on
a stale scratch tree and on the real repo, in one process):

```
=== C. the WRAP GATE itself, driven on a scratch tree (stale) ===
STALE tree -> FAILS: 1 NOTES: 0
    s263-D10 RULINGS PAGE STALE — STALE _RULINGS.html embeds a0c5b24ca0a6069896bccc884aa8a08bb58b14b34127a2f7711ab7fe6523f3ec but _rulings.json is now bd5107c41fcef1c4b18645fe3af16411327f0a4b5d88aa77c082cb5dd64db4ba. Run `py
REAL repo -> FAILS: 0 NOTES: 1
    s263-D10 RULINGS PAGE: FRESH _RULINGS.html matches _rulings.json sha256 a0c5b24ca0a6069896bccc884aa8a08bb58b14b34127a2f7711ab7fe6523f3ec
```

**Gate selftest still green** with the new check in the chain, and the fixture-tree SKIP path prints
honestly rather than passing silently:

```
  ▫️  s263-D10 RULINGS PAGE check SKIPPED — no `knowledge/_rulings.json` under /sessions/.../tmptv0959nz, so this is not a state tree. NOT a pass.
capture gate [wrap]: 5 in scope · 4 fail · 4 warn
  ✅ capture-gate selftest: all failure classes bite; green control passes
exit=0
```

Scratch trees under `/sessions/practical-nice-davinci/tmp/263E*` were removed after the drive.

---

## Not done / for the conductor

1. **No commit.** Conductor's.
2. **`status` vs `$status` on the dormant variant** — schema-forced, described above. If a
   machine-readable `status` field on variants is wanted, `meta.schema.json` must gain it; that file
   is shared and outside this lane's fence.
3. **Footer's two PRE-EXISTING schema reds** (`edges.composes`, `provenance.source: "redesign"`)
   are untouched and still red. Not s263-D7's scope; flagged so nobody reads them as this lane's.
4. **`_capture_gate.py` has no bite-test arm for the new check.** The selftest exercises it through
   the wrap fixture (SKIP path) and I drove both arms by hand above, but there is no registered
   failure-class arm the way older checks have. Cheap to add if the conductor wants the gate's own
   regime honoured fully; it is the only structural gap I know of in this enactment.
5. **Four generator-output files dirtied by running the validators** — listed under diff summary.
