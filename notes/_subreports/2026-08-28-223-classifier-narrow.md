# `#223` — narrowing the EXIT-77 classifier arm (`s223-D6`)

session: `#223` · 2026-08-28
window: Fable conductor, build lane (Opus sub)
sub index: `classifier-narrow`
brief: inline in the spawn message — no `notes/_briefs/` file for this lane
predecessor: `notes/_subreports/2026-08-28-223-hitarea-classifier.md` (the arm this lane narrows)
tokens: `UNMEASURED — a sub cannot read its own message.usage`; effort band S, ~8K job-window.

## VERDICT

DONE. The exit-77 arm now routes every refusal through **the structural repo-resource test the
file already owned** before it may grant `NEEDS-DEP`. No keyword blocklist was invented: the
narrowing calls the SAME code the pre-existing REPO-BOUND fence calls, factored into one helper
so the two can never drift.

Measured on the four REAL refusals in this sandbox:

| gate | before | after |
|---|---|---|
| `_validate_evidence.py` | NEEDS-DEP *(wrong)* | **REPO-BOUND** ✅ |
| `_validate_state_contrast.py` | NEEDS-DEP | **NEEDS-DEP** ✅ |
| `_validate_hit_area.py` | NEEDS-DEP | **NEEDS-DEP** ✅ |
| `_validate_descender_computed.py` | NEEDS-DEP | **NEEDS-DEP** ✅ |

Controls hold: a raw crash at rc=1 is still REPO-BOUND, a clean pass and a clean measured FAIL are
still RUNNABLE.

Generator selftest: **203 bites** (198 → 203, five ADDED, no fixture edited). **1 fail, and it is
NOT mine** — `questions/Q6-premise-evidence-is-repo-bound` reads the WORKING-TREE
`_pack_gate_probe.json`, which another `#223` lane regenerated at `5efd667` *before* this
narrowing existed. It is red identically with and without my change (proved in F5), and the
conductor's regeneration at the landing sha is what clears it. See **⚠ THE ONE RED** below.

Roster: the narrowed arm dry-projects the gates group at **58 files** — the ruled `s223-D6`
figure — derived from the probe json's own import closure, not tuned to it (F6).

COUNTS: findings `7` · ruling-shaped `2` · UNPROVEN/COULD-NOT-RUN `3`

## What was done

**ONE file edited:** `knowledge/_release/_gen_pack_manifest.py`. No commit, no `git add`, no
`git checkout`. `knowledge/_rulings.json` NOT touched. `_pack_gate_probe.json`,
`_pack_manifest.json` and the gates themselves NOT touched.

Three changes, eight hunks:

1. **`_unshipped_subject(blob, shipped)`** — new helper, immediately above `_refusal_dep`. It is
   the pre-existing SUBJECT TEST loop (`MISSING_LINE` → `PATHISH` → `not in shipped`) lifted
   verbatim out of `classify()` and given a name. It returns the offending path or `None`.
2. **The exit-77 arm** now asks that question first:

   ```python
   if rc == REFUSAL_EXIT:
       unshipped = _unshipped_subject(blob, shipped)
       if unshipped:
           return "REPO-BOUND", "refuses for %s, a repo resource the pack does not ship — not " \
                                "a dependency the designer can install" % _tail(unshipped)
       return "NEEDS-DEP", _refusal_dep(blob)
   ```

3. **The old subject test collapsed onto the helper** (7 lines → 2), so there is exactly one
   implementation. The module docstring's verdict legend amended for both `NEEDS-DEP` and
   `REPO-BOUND`. Five new `--selftest` bites.

**★ THE MECHANISM IS STRUCTURAL, NOT TEXTUAL.** The brief permitted a weaker fallback (match on
the presence of an `install` remedy) and said to declare it if used. **It was not needed and was
not used.** The classifier reads what the refusal *names* — a repo path in a missing-language
clause that the pack does not carry — which is the ruling's own wording made mechanical. A future
gate refusing for some other unshipped repo path classifies correctly without being listed
anywhere [[gate-inside-the-growth-loop]].

## Findings

**F1 — the four refusals, measured, verbatim.** Captured from real processes; the browser gates
from the repo (`--all`, the invocation the probe reaches via the ARGS_REFUSAL arm), the evidence
linter from a staged copy of `knowledge/` under `/var/tmp/stg223` with **no `notes/`** — the
packed condition.

```
COULD-NOT-ASK: the evidence linter — no claim table was named and the conventional home
notes/_claims does not exist here — there are no evidence rows to lint (notes/ is out of the
release ship list, so this is the expected reading in a packed or a fresh project). Name a
<rows.jsonl> or a directory of them to ask this gate anything.                       rc=77

COULD-NOT-ASK: _validate_state_contrast.py — playwright is installed but its BROWSER BINARIES
are not — the chromium executable it drives was never downloaded (Error: BrowserType.launch:
Executable doesn't exist at …/chromium_headless_shell-1234/chrome-linux/headless_shell) — …
install them with `playwright install chromium` ⇒ THIS IS NOT A SKIP …                rc=77

COULD-NOT-ASK: HIT-AREA: HARNESS UNAVAILABLE — playwright is installed and a chromium binary was
found, but it would not START on this box (… libXdamage.so.1: cannot open shared object file: ).
… `playwright install --with-deps chromium` re-installs it together with the system libraries it
needs. … the proof lives in the `render` job of .github/workflows/gates.yml …        rc=77

COULD-NOT-ASK: DESCENDER-COMPUTED: HARNESS UNAVAILABLE — playwright is installed but its BROWSER
BINARIES are not … Install them with `playwright install chromium`. …                rc=77
```

**F2 — the discriminator, read off those four texts.** Only the evidence refusal carries a
missing-language clause naming a path the pack does not ship:

| refusal | missing-language clause | `PATHISH` hit on that line | verdict |
|---|---|---|---|
| evidence | `does not exist` ✓ | `notes/_claims` | REPO-BOUND |
| state-contrast | *(none — `doesn't exist` is not in `MISSING_LINE`, and the path is `/…/.cache/ms-playwright/…`)* | — | NEEDS-DEP |
| hit-area | `no such file or directory` ✓ | **none** — the paths it names are `/var/tmp/pw-browsers-220/…` and `.github/workflows/gates.yml`, neither of which `PATHISH` recognises as a repo resource | NEEDS-DEP |
| descender | *(none)* | — | NEEDS-DEP |

Hit-area is the interesting one and it is why a keyword blocklist would have been the wrong
instrument: its refusal **does** contain missing-language, and the test still says NEEDS-DEP
because what the sentence names is a *browser*, not a repo path. That case is now a selftest bite
(`classify/refusal-installable-still-needs-dep`) precisely so the narrowing cannot widen on prose.

**F3 — BASELINE, before the narrow.** `classify()` loaded from the working-tree generator and
called on the real captured `(rc, out, err)` — the same function the probe calls, on the same
inputs.

```
== BASELINE classify(), shipped=[] ==
_validate_evidence.py              rc=77  -> NEEDS-DEP  | something this box does not have — see the refusal
_validate_state_contrast.py        rc=77  -> NEEDS-DEP  | playwright install chromium
_validate_hit_area.py              rc=77  -> NEEDS-DEP  | playwright install --with-deps chromium
_validate_descender_computed.py    rc=77  -> NEEDS-DEP  | playwright install chromium
```

⚠ Note the evidence linter's `why` even before the narrow: *"something this box does not have —
see the refusal"*. `_refusal_dep` found no backticked `install` command to quote, because there is
none — the refusal was never about anything installable. The classifier was already telling us it
could not name a remedy; the arm shipped the gate anyway.

**F4 — AFTER the narrow, same real runs, `shipped={knowledge/canon/canon.css,
knowledge/tokens/colour.json}`.**

```
== AFTER THE NARROW — classify() on the REAL captured runs ==
_validate_evidence.py (staged, bare)          rc=77 -> REPO-BOUND | refuses for notes/_claims, a repo resource the pack does not ship — not a dependency the design…
_validate_state_contrast.py (staged, bare)    rc=77 -> NEEDS-DEP  | playwright install chromium
_validate_hit_area.py (repo, --all)           rc=77 -> NEEDS-DEP  | playwright install --with-deps chromium
_validate_descender_computed.py (repo, --all) rc=77 -> NEEDS-DEP  | playwright install chromium

== CONTROLS, same call ==
raw crash rc=1            -> REPO-BOUND | crashed: playwright._impl._errors.TargetClosedError: BrowserType.launch: Target page, context o…
clean pass rc=0           -> RUNNABLE   | ran clean, verdict PASS
clean measured fail rc=1  -> RUNNABLE   | ran, verdict FAIL (exit 1) — a verdict is a run
```

All four obligations of proof-step 2 met. The exclusion is honest in `why`: *"refuses for
notes/_claims, a repo resource the pack does not ship — not a dependency the designer can
install"* — it names the resource, and it says why it is not a dependency.

**F5 — MUTATION PROOF, and the pre-existing red isolated.** Mutate → drive → restore inside ONE
bash call with a `trap … EXIT`, because nothing survives a tool-call boundary here. The mutation
deletes only the four narrowing lines from the 77 arm.

```
MUTATED (narrowing removed)
selftest: 203 bites, 3 fail(s)
  RED [classify/refusal-for-repo-resource-is-repo-bound] got 'NEEDS-DEP', wanted 'REPO-BOUND' no `install` command can hand a designer the repo's notes/_claims
  RED [classify/refusal-repo-resource-named-in-why] got False, wanted True
  RED [questions/Q6-premise-evidence-is-repo-bound] got 'NEEDS-DEP', wanted 'REPO-BOUND' Q6 says the evidence linter dropped out as REPO-BOUND — the probe must agree

RESTORED-IDENTICAL                      # diff -q against the pre-mutation backup
selftest: 203 bites, 1 fail(s)
  RED [questions/Q6-premise-evidence-is-repo-bound] got 'NEEDS-DEP', wanted 'REPO-BOUND' …
```

TWO bites go red when the narrowing is deleted and green when it is restored — the arm has a
consumer that fails without it [[instrument-without-a-consumer]]. The third red is present in
BOTH states, which is the proof that it is not mine.

**⚠ THE ONE RED, named.** `questions/Q6-premise-evidence-is-repo-bound` (a pre-existing bite, in
`HEAD` — `git show HEAD:… | grep -c` returns `1`) asserts that the card copy and the PROBE JSON
agree about the evidence linter:

```python
_pg = {g["gate"]: g["verdict"] for g in json.load(open(_pp))["gates"]}
… _pg.get("_validate_evidence.py"), "REPO-BOUND",
  "Q6 says the evidence linter dropped out as REPO-BOUND — the probe must agree"
```

It reads a stored artefact, never `classify()`. The working tree's `_pack_gate_probe.json` was
regenerated at `5efd667` **by the un-narrowed arm** and still says:

```
probe json (working tree, regenerated at 5efd667 BEFORE the narrow):
   _validate_evidence.py              NEEDS-DEP
   _validate_hit_area.py              NEEDS-DEP
   _validate_state_contrast.py        NEEDS-DEP
   _validate_descender_computed.py    NEEDS-DEP
   verdict tally: {'RUNNABLE': 38, 'REPO-BOUND': 7, 'NEEDS-DEP': 4}
```

So the red is the OLD probe disagreeing with the card, and this lane may not regenerate the probe
(brief: the conductor's step). **The bite going green is the conductor's read-back that the
regeneration at the landing sha actually took the narrowing.** It is a free, already-wired
acceptance check — do not skip it.

**F6 — the roster, DRY-REASONED, not tuned.** The gates group ships `runnable + needsdep` plus a
helper closure computed only from RUNNABLE/NEEDS-DEP gates' `local_imports`. Flipping the evidence
linter's verdict in the stored probe and recomputing that set:

```
manifest gates group as generated at 5efd667 (UN-narrowed): files = 60 counts = {'empty_population': 4, 'needs_dep': 4, 'repo_bound': 7, 'runnable': 38}
simulated gates+helpers, un-narrowed : 51
simulated gates+helpers, NARROWED    : 49
leaves the ship list                 : ['knowledge/_claimtable.py', 'knowledge/_validate_evidence.py']
PROJECTION for the gates group       : 58
RULED figure (s223-D6)               : 58
MATCH: True
```

The companion drops out **structurally**, not by name: `_claimtable.py` reaches the pack only via
`helper_closure`, and the only other importers are `_gen_claim_table_md.py` and
`_join_claim_tables.py`, neither of which is a probed gate (`in probe list? False` for both).
Nothing in this lane was tuned toward 58 — the classifier was written from the ruling's wording,
and 58 fell out of the arithmetic afterwards.

**F7 — nothing else in the file changed.**

```
$ git diff --stat -- knowledge/_release/_gen_pack_manifest.py
 knowledge/_release/_gen_pack_manifest.py | 83 ++++++++++++++++++++++++++++----
 1 file changed, 73 insertions(+), 10 deletions(-)

$ git diff -U0 -- knowledge/_release/_gen_pack_manifest.py | grep "^@@"
@@ -32 +32,3 @@      docstring legend, NEEDS-DEP
@@ -34 +36,2 @@      docstring legend, REPO-BOUND
@@ -687,0 +691,18 @@  _unshipped_subject helper
@@ -717,0 +739,10 @@  s223-D6 comment
@@ -718,0 +750,4 @@   the narrowing itself
@@ -738,7 +773 @@     old subject test collapsed onto the helper
@@ -747 +776 @@       …its `why` line
@@ -2358,0 +2388,34 @@ five new selftest bites

$ python3 -m py_compile knowledge/_release/_gen_pack_manifest.py
py_compile: clean
```

All eight hunks are mine — the predecessor lane's edits to this file landed in `5efd667`.

⚠ The full working tree also shows `_pack_gate_probe.json`, `_pack_manifest.json` and
`_rulings.json` modified. **None of the three is mine** — the two json artefacts are the
`5efd667`-era regeneration by another lane, and `_rulings.json` is the conductor's inscription.
Declared so the conductor's reconcile does not misattribute them
[[feedback-worktree-reconcile-trail]].

## REPLAY-THESE

```bash
cd <repo>

# 1. the five new bites, and the mutation that reddens two of them
python3 knowledge/_release/_gen_pack_manifest.py --selftest

# 2. the real refusals this lane classified (browser gates; the third state of this box)
cd knowledge && python3 _validate_hit_area.py --all; echo rc=$?
python3 _validate_descender_computed.py --all; echo rc=$?

# 3. the evidence linter's PACKED refusal — needs a stage with no notes/
rm -rf /var/tmp/stg223 && mkdir -p /var/tmp/stg223/knowledge \
  && cp <repo>/knowledge/*.py /var/tmp/stg223/knowledge/
cd /var/tmp/stg223 && PYTHONPATH=/var/tmp/stg223/knowledge \
  python3 knowledge/_validate_evidence.py; echo rc=$?     # 77, names notes/_claims

# 4. ⛔ THE CONDUCTOR'S READ-BACK, after regeneration at the landing sha:
python3 knowledge/_release/_gen_pack_manifest.py --selftest   # must be 203 bites, 0 fail
#   → questions/Q6-premise-evidence-is-repo-bound green means the regen took the narrowing
#   → the gates group must read 58 files
```

## RULING-SHAPED QUESTIONS

1. **`MISSING_LINE` does not match `doesn't exist`, only `does not exist`.** Measured in F2 —
   state-contrast's refusal says *"Executable doesn't exist at …"* and the phrase is invisible to
   the test. Today that is harmless (the path it names is not repo-ish, so the verdict is right
   either way) but it is right by luck, not by construction. Widen `MISSING_LINE` to catch the
   contraction — accepting that it also widens the pre-existing REPO-BOUND fence for every clean
   FAIL — or leave the regex alone and record the gap? Surfaced, not decided: widening a shared
   test touches an arm this lane was not sent to change.
2. **`PATHISH` is a closed list of repo top-level directories** (`knowledge|showroom|reviews|
   notes|runs|memento-package|designer-skills-v[12]|projects|archive`). The narrowing inherits it,
   so a future gate refusing for a repo resource under a directory not on that list would be
   granted NEEDS-DEP and ship. That is the same closed-list exposure the REPO-BOUND fence already
   carries, now load-bearing in one more place. Gate the list against the repo's actual top-level
   directories (a bite that fails when a new one appears), or accept it? Not decided here.

## UNPROVEN / COULD-NOT-RUN (ADR-0016)

- **COULD-NOT-RUN: the end-to-end `--probe --commit <sha>` and the regenerated manifest.** Driven
  and refused by design — staging is `git archive <sha>`, so the probe sees only COMMITTED content
  and this lane may not commit. Every classification claim above was proved by calling
  `classify()` directly on real captured runs, the same function on the same inputs. **The
  conductor owes one `--probe --commit <landing-sha>` + `--manifest`**, after which
  `questions/Q6-premise-evidence-is-repo-bound` must go green and the gates group must read 58.
  Price ~2K tk.
- **UNPROVEN: the 58 is a PROJECTION, not a regeneration.** F6 recomputes `ship_gates ∪
  helper_closure` from the stored probe json with one verdict flipped; it does not re-run
  `blob_sizes`, `gate_data` or `ci_template`, which are functions of the commit. Those three
  contribute the same paths in both branches of the flip, so the DELTA (−2) is sound while the
  ABSOLUTE 58 rests on the stored `files = 60`. If the landing sha differs from `5efd667` in the
  gates group for any other reason, 58 moves and that is a real finding, not a defect in this arm
  [[planning-estimate-is-not-a-measurement]].
- **UNPROVEN: the narrowed `why` string as Dave will read it on the release page.** The HTML
  renderer prints REPO-BOUND reasons under the excluded-gates list; the evidence linter would read
  *"refuses for notes/\_claims, a repo resource the pack does not ship — not a dependency the
  designer can install"*. Read from the source at the `order = {...}` block, not from a rendered
  page. Price: one `--manifest` run at a commit.
- **Declared residual, staging fidelity:** the `/var/tmp/stg223` stage used in F1/F3/F4 is a flat
  copy of `knowledge/*.py` (plus `knowledge/canon/`), NOT a `git archive` of the pack's exact path
  set. It reproduces the CONDITION that matters — no `notes/` — and the refusal TEXT is what the
  classifier reads, but it is not byte-identical to the probe's stage. Named as a stand-in, not
  claimed as the probe [[a-crash-is-not-a-fail]].

## Evidence

No evidence files. Every claim above quotes its probe inline. The mutation backup lived at
`/var/tmp/gm223.bak`, consumed and verified by `diff -q` inside the same bash call that created
it (`RESTORED-IDENTICAL`), with a `trap … EXIT` as a second restore in case the call died mid-way.
Captured runs at `/var/tmp/runs223.json`, `/var/tmp/_validate_hit_area.py.{out,err}`,
`/var/tmp/_validate_descender_computed.py.{out,err}` — sandbox-local, they do not survive.
