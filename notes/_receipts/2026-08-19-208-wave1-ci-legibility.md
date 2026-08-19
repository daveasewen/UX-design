# Session #208 — WAVE 1 receipt: make CI legible

status: observed
provenance: session #208, 2026-08-19, Opus work sub (lane: WAVE 1 — make CI legible), conductor Fable

Claim table (machine-linted): `notes/_claims/208-wave1-claims.jsonl`
Check-in mid-lane: `python3 knowledge/_checkin.py` → FILL 103,361 real · room to stop line 47,568 · boot 57,050.

⛔ ALL FOUR ITEMS' PREMISES WERE VERIFIED FIRST-HAND BEFORE ANY FIX. Two of the four briefed
premises were STALE and are corrected below — the stale halves are the ones a reader acts on,
so they are stated before the repairs.

---

## PATHS MODIFIED (complete list)

| path | what |
|---|---|
| `knowledge/_governs.py` | matcher narrowed (`matches`, new `names_a_directory`), 6 new selftest bites, ⬛-declaration block |
| `knowledge/_git_commit.sh` | `prefix_count` + `--selftest` (10 bites); door-level reused-msgfile gate; mention-map freshness gate (two halves); T3 renders to a separate file instead of mutating the msgfile; post-commit exactly-one-prefix assert |
| `.github/workflows/gates.yml` | third correction block (#208) + new step running `bash knowledge/_git_commit.sh --selftest` |
| `notes/_receipts/2026-08-19-208-wave1-ci-legibility.md` | this receipt (new) |
| `notes/_claims/208-wave1-claims.jsonl` | claim table for the evidence linter (new) |
| `knowledge/_CAPTURE-GATE.md` | ⚠ NOT hand-edited — REGENERATED as a side effect of running `python3 knowledge/_capture_gate.py` (bare) to verify the build-mode gate still passes. Derived audit output; the diff is a date + scope refresh (2026-08-17 → 2026-08-19, 151 → 161 files in scope). Declared so the reconcile does not meet it as anonymous dirt. |
| `notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl` | ⚠ instrumentation appends written by `_capture_gate.py` / `_checkin.py` while verifying — the W-22 declared class, not edits |

⚠ **OTHER-LANE DIRT, UNTOUCHED BY THIS LANE, listed so the conductor's reconcile can name it:**
`knowledge/_build_all.py` (+119/−1), `knowledge/_gate_doc_rows.py` (+73/−7),
`knowledge/_state.json` (+13), `knowledge/_ASSERTIONS.md`, `knowledge/_assertions.json`,
`_LIVE-STATE.md` (+1). None of these was read or written by this lane; they were already dirty
in the shared tree. Probe: `git diff --numstat -- knowledge/_build_all.py`.

NOT modified, and deliberately so: `knowledge/_rulings.json` (only `_inscribe_ruling.py` may write
it), `knowledge/_build_all.py`, `knowledge/_build_graph_mention_map.py` (no defect found in it),
`knowledge/_capture_gate.py` (its red had an external cause), any generated file.
`knowledge/_graph-mention-map.json` was mutated and regenerated during a drive and is
BYTE-IDENTICAL to its pre-drive state (`cmp` quoted below) — it is not a modified path.

---

## ITEM 3 (done first — it is the cause of item 2) — `_governs.py` too-loose matcher

**Premise, verified — and the briefed step number is WRONG.** The brief calls this "[14]".
Step 14 of `_build_all.STEPS` is the gauge-tokens selftest; `_governs.py` has NO step of its own
and reaches CI through `[12]`/`[13]` (`_capture_gate.py`). Step numbers in `_build_all.STEPS` are
POSITIONAL and have drifted since the gates.yml prose was written (that prose calls the chain
check `[109]`; it is `[112]` today). Probe:
`python3 -c "import ast; …ast.parse(open('knowledge/_build_all.py').read())…"` → `13 ('capture/provenance selftest (Memento §4.1)', '_capture_gate.py', ['--selftest'])`, `14 ('gauge-tokens selftest …', '_gauge_tokens.py', ['--selftest'])`, `110 ('graph mention map determinism check (#115 step 0)', …)` — total 124.

**The failure, quoted from a first-hand run** (`python3 knowledge/_governs.py --selftest`, rc=1):

```
  FAIL _governs: an unrelated path matched a ruling — the matcher is too loose to carry information
```

**The cause, isolated on real data.** `surface({"knowledge/_totally_unrelated_xyzzy.py"})` returned
`['s202-D3']`, whose `governs` is the bare token `["knowledge"]`. The matcher's third arm was

```python
if "/" not in gn and gn in t.replace("/", " ").split():
```

— a bare entry matched ANY PATH SEGMENT of the target, so one ruling governed every file under
`knowledge/`, the selftest's own negative control included.

**What changed.** `knowledge/_governs.py`:
- `matches()` — the path-segment arm REMOVED; a bare entry is now a file name or a symbol only.
  An entry that names a real directory matches nothing (`names_a_directory()`, new).
- ⛔ **No subtree scope was invented in its place**, and that is a decision with a reason, not an
  omission: `opacity-primitives-4pct` ("Opacity primitives run in 4% steps") carries
  `governs: ["knowledge/"]`, today a no-op, and reading a trailing slash as "everything under
  here" would have WIDENED a live ruling to the whole tree. Narrowing a mis-scoped entry to
  nothing and saying so is honest; widening one silently is [[gate-glob-scope-rule]] with the
  sign flipped.
- `selftest()` — 6 new bites (3a) on SYNTHETIC rulings so they bite whatever the corpus holds:
  bare-directory must MISS, `knowledge/` must MISS, basename must HIT, bare symbol must HIT,
  near-miss `_capture_gate.py` vs `_capture_gate_helpers.py` must MISS.
- `selftest()` — 3b, the ⬛ DECLARATION: every `governs` entry naming a real directory is PRINTED
  by name on every run, with its remedy. **Reach actually lost: exactly one entry** — `s202-D3` →
  `knowledge` (the only bare-token directory; the other 32 contain a `/` and never matched a file
  path before #208 either, so they are a pre-existing under-specification, counted in one line,
  not shouted 32 times).

**Driven, both directions:**

| direction | command | result |
|---|---|---|
| fires (mutation control) | pre-#208 `matches` monkey-patched back in, `selftest()` re-run | **2 failures**: the negative control AND the new 3a bare-directory bite |
| stays silent | `python3 knowledge/_governs.py --selftest` | **rc=0** — "all bites green" |
| real HIT | `surface({"knowledge/_capture_gate.py"})` | `['ds-021','ds-021-C','ds-023','gauge-band','gauge-refusal','derivation-governance']` |
| real HIT (symbol) | `surface({"measure_tokens"})` | `['ds-021','ds-021-D1-82']` |
| real MISS | `surface({"knowledge/_totally_unrelated_xyzzy.py"})` | `[]` |
| real MISS | `surface({"knowledge/tokens/nope-not-real.json"})` | `[]` |
| consumers unbroken | `python3 knowledge/_capture_gate.py` · `python3 knowledge/_inscribe_ruling.py --selftest` | rc=0 · rc=0 |

**⬛ PRICED TODO, NOT RULED HERE (Dave's).** `s202-D3` now governs no file. Its text is about
open-question provenance — a PROCESS, not a directory — so re-scoping it is a judgment, not a
repair. Remedy when ruled: rewrite that entry through `_inscribe_ruling.py` (the only legal
writer) naming the files/symbols it governs. The declaration prints on every selftest run until
then, so it cannot go quiet. Same question, lower stakes, for the 32 slashed directory entries.

---

## ITEM 2 — `[13]` capture/provenance gate: red in CI, green locally

**Premise, verified — and the briefed premise was STALE in BOTH halves.**
`python3 knowledge/_capture_gate.py --selftest` on this tree BEFORE any fix → **rc=1**, and its
only red was the `_governs` arm above:

```
  ❌ selftest: trigger index: `_governs.py` selftest is RED — 1 failure(s) …
  ❌ selftest: trigger index: `_governs.py` selftest — _governs: an unrelated path matched a ruling …
```

So it was red LOCALLY too, and its cause was mechanical — not the "Dave-owned residual" the #193
gates.yml note calls it, and not a #173 environment gate. The #173 half of `[13]` had ALREADY
been fixed at #194 (the `git check-ignore`-keyed COULD-NOT-ASK on gitignored `outputs/…`
evidence pointers); nothing was left to build there.

**Reproduced in the CI shape**, the #194 method — a bare clone, one variable:
`git clone --no-hardlinks -q . /var/tmp/ciclone` (then a second copy with HEAD's `_governs.py`
restored, as the baseline).

| environment | `_governs.py --selftest` | `_capture_gate.py --selftest` |
|---|---|---|
| working tree, BEFORE | rc=1 | rc=1 |
| bare clone, HEAD (baseline) | rc=1 | **rc=1 — the real CI red** |
| working tree, AFTER | rc=0 | **rc=0** |
| bare clone + the fix | rc=77 | **rc=77 — COULD-NOT-ASK** |

The 77 in the clone is the legal refusal form (`_could_not_ask.py`), which `_build_survey.py`
prints in full and excludes from its exit code — pass-with-declaration, not failure. Its reason
names its unreachable inputs: 3 evidence pointers on ds-034/ds-035 at gitignored
`outputs/_FINDING-…` / `_PARTITION-…` paths. A real red still outranks a refusal (the baseline
row above IS that proof: with a genuine failure present the same gate returned 1, not 77).

**What changed for `[13]`: nothing in `_capture_gate.py`.** Its red had an external cause and the
fix belongs where the cause is. Recorded in `.github/workflows/gates.yml` as the third correction
block, because the file's #193/#194 prose asserts `[13]` is Dave-owned and that claim is what a
reader consults when the gate is red.

---

## ITEM 1 — `[110]` mention-map re-stale CLASS (3rd recurrence)

**Premise, verified — and half of it was stale at read time.** `[110]` is
`python3 knowledge/_build_graph_mention_map.py --check`, and on this tree it is **rc=0**
("current (101 of 101 node(s) mentioned)"). The map is fresh RIGHT NOW; the class is that it
does not stay fresh, and nothing at the commit seam ever asked.

**What "stale" means to the gate** (read from the source, not inferred): `--check` rebuilds the
map from `_decision-graph.json` + `_memento-index.json` and does a **byte compare** against
`knowledge/_graph-mention-map.json`; any difference → exit 1. So CI can only go red on `[110]` in
the SURVEY step, which asks the COMMITTED tree BEFORE any regeneration — the later "Knowledge
build" step regenerates the map and cannot rescue that read. That makes the commit seam the exact
place where the question has to be asked.

**OWNED REGIONS OF THE GENERATOR, WRITTEN DOWN BEFORE IT WAS RUN**
([[do-not-rule-list-cannot-fence-a-generator]]): `_build_graph_mention_map.py` writes **exactly
one path** — `knowledge/_graph-mention-map.json`, whole-file overwrite (`OUT_PATH`). Probe:
`grep -n '"w"\|os.remove\|shutil\|unlink\|subprocess' knowledge/_build_graph_mention_map.py` →
two hits only, `140:` (a selftest tempfile) and `176:` (`OUT_PATH`). It READS
`_decision-graph.json` and `_memento-index.json` and writes neither. That single-owner property
is why regenerating it at the commit seam is safe, and it is NOT a licence for any other
generator at that seam.

**What changed** — `knowledge/_git_commit.sh`, two halves, both BEFORE the commit:
1. **Freshness gate** (after the showroom gate, before T3): `--check`; if stale, regenerate
   targeted, re-check that the regeneration TOOK (a still-stale map is nondeterminism, refused
   separately and named as such), then **REFUSE** with the path to add to the caller's
   `--reconciled` list. It regenerates but never stages: `git add -A` is retired (P5, ruled
   2026-08-02) and the chain check's own comment at this seam forbids staging "a file this
   session never showed you". Declared-gap hatch `MENTION_MAP_ACK=` mirrors its two neighbours.
2. **Regenerated-but-not-staged assert** (after staging, before commit): if the map differs from
   HEAD and is not staged, refuse. This is the hole the three targeted repairs kept falling
   through — regenerate locally, commit without naming the path, and CI's survey reads the OLD
   blob against the NEW corpus while `--check` is green on the author's machine.

**Driven, both directions.** The shell clauses ran end-to-end in a scratch git repo with the
REAL `_git_commit.sh` and its NEIGHBOUR gates shimmed to forced exit codes (the shim posture the
file itself uses for the wrap-gate consumer), plus the real generator on real repo data:

| arm | command | rc / result |
|---|---|---|
| real data, clean | `python3 knowledge/_build_graph_mention_map.py --check` | rc=0 "current (101 of 101)" |
| real data, mutated map (one planted hit) | same | **rc=1 "STALE — regenerate"** |
| real data, targeted regeneration | `python3 knowledge/_build_graph_mention_map.py` | rc=0, "101 of 101 node(s) mentioned, 1099 record hit(s)" |
| real data, after regen | `--check` | rc=0; `cmp` vs the pre-drive copy → **byte-identical, no residue** |
| gate: stale → regenerate + refuse | shim, `STUB_MAP_STALE=1` | **rc=1**, "REGENERATED just now … It is NOT staged", 0 paths staged |
| gate: still stale after regen | shim, stub pinned stale | **rc=1**, "STILL stale after a targeted regeneration … nondeterminism" |
| gate: declared hatch | shim, `MENTION_MAP_ACK="stub drive"` | "mention-map gate: DECLARED GAP — stub drive", run continues |
| gate: fresh | shim, default | "mention map fresh (… --check passed)" |
| 2nd half: dirty + unnamed | shim, map hand-edited, path NOT given | **rc=1**, "differs from HEAD and is NOT staged" |
| 2nd half: dirty + named | shim, map appended to the path list | **rc=0**, commit landed |

---

## ITEM 4 — msgfile-prefix gate (class count 8)

**Premise, verified — and the briefed "gate never built" is WRONG.** A gate DOES exist, at
`knowledge/_git_commit.sh` inside T3's non-wrap branch (#170):
`if re.match(r"after #\d+ \d{4}-\d{2}-\d{2} — ", first):` … and the post-commit subject-identity
assert against `$GEN_SUBJ` exists too (#171). **Three real holes remained**, and they are what
was built here:

1. **Shape.** The #170 regex sees only `after #N <date> — `. A WRAP msgfile's line 1 is
   `#N <date> — …`; feeding one into a non-wrap run walked straight past the gate and produced
   `after #208 … — #207 … — x`.
2. **Branch.** The wrap branch never asked at all — and it takes the body from line 2 onward, so
   a reused wrap msgfile silently DROPPED its first line.
3. **Mutate-before-refuse.** The briefed sentence "T3 … mutates the file even on REFUSALS" is
   true, but not of T3's OWN refusals (those precede its write). It is true of the FIVE refusals
   AFTER T3: lock survived · no paths named · nothing staged · empty commit refused · a git
   error. Every one left the caller holding a msgfile that had already grown a prefix; the caller
   fixed the named problem, re-ran the same file, and stacked. That is the actual mechanism.

**What changed** — `knowledge/_git_commit.sh`:
- `prefix_count()` — ONE implementation of "how many T3 prefixes are in this string", counting
  BOTH legal shapes, with three consumers (the door gate, the post-commit assert, `--selftest`).
- **Door gate**: line 1 of the msgfile is checked BEFORE any other gate and long before any
  write, so the answer does not depend on which branch T3 will take. The #170 in-branch check is
  LEFT IN PLACE unchanged — two gates on one class is not duplication when the inner one is the
  one proven to bite.
- **T3 no longer writes to the caller's msgfile.** It renders to `"$MSGFILE".t3-rendered` and the
  commit is `-F "$RENDERED"`. The msgfile is READ-ONLY input for the whole run, so a refusal costs
  nothing and a retry is safe — this kills hole 3 at the root rather than gating its symptom.
- **Post-commit exactly-one-prefix assert** on `git log -1 --format=%s`. The #171 identity assert
  cannot see this class (a doubled subject is a FAITHFUL copy of what T3 built), so the class gets
  its own check on the artefact a reader actually meets. Post-commit by design: that is where a
  wrong subject turns durable and where `--amend` is still available.
- **`--selftest`** — read-only (no staging, no commit, no push, no writes), wired into
  `.github/workflows/gates.yml` so it has a consumer [[instrument-without-a-consumer]].

**Driven, both directions** (`bash knowledge/_git_commit.sh --selftest` → rc=0, "10 bites: 5 fire,
5 stay silent"), plus end-to-end arms in the scratch repo with real commits:

| arm | result |
|---|---|
| fresh msgfile + named path | **rc=0**, subject `after #208 2026-08-19 — wave1: make CI legible`, "carries exactly ONE T3 prefix" |
| msgfile AFTER that run | **line 1 unchanged** (`wave1: make CI legible`) — the no-mutation property; the render file carries the prefix |
| the SAME msgfile re-run | **rc=0** and still exactly one prefix — reuse is now harmless, because nothing was mutated |
| msgfile written by the PRE-#208 script (`after #207 2026-08-18 — …`) | **rc=1**, REUSED-MSGFILE GATE, "this msgfile has not been modified" |
| WRAP-shaped prefix (`#207 2026-08-18 — …`) — the shape #170 MISSED | **rc=1**, same gate |
| control: same line with a HYPHEN not an em-dash | passes the door ("carries no T3 prefix") |
| post-commit assert BITES: `--wrap` whose GM banner summary itself carries a prefix | **rc=1**, "SUBJECT PREFIX COUNT = 2 (must be exactly 1)", subject `#208 2026-08-19 — after #207 2026-08-18 — carried summary` |
| control: ordinary banner | **rc=0**, "exactly ONE T3 prefix" |

---

## RESIDUALS — declared, not fixed

1. **`s202-D3` governs nothing** until its `governs` entry is re-scoped through
   `_inscribe_ruling.py`. ⬛ Dave's. Printed on every `_governs --selftest` run.
2. **32 slashed directory `governs` entries** (`knowledge/tokens`, `knowledge/snippets/`, …)
   govern no file — and did not before #208 either. Unchanged, declared in one line. ⬛ Dave's.
3. **`[13]` in CI is a REFUSAL (77), not a pass.** Honest and legible, but it stays non-zero
   until the 3 gitignored `outputs/…` evidence pointers on ds-034/ds-035 are re-homed
   (`s191-D2` HOME-OR-DECLARE). ⬛ Dave's — they are evidence, not machinery.
4. **`knowledge/_tests/test_gates.py` is RED and it is NOT my lane** — 27 tests, 1 failure:
   `FAIL a11y gate bites on sub-24 target floor — exit=0, marker 'MISSING: 2.5.8'`. Confirmed
   PRE-EXISTING by running it in the untouched baseline clone: same single failure. So the "Gate
   self-tests" CI step is red for that reason, independent of everything here.
5. **`_governs.py` has no STEPS entry of its own.** It reaches CI only through `[12]`/`[13]`.
   Giving it one needs BOTH a `_build_all.STEPS` entry AND a `ROUTE_ROWS` row (a STEPS entry
   without a route row aborts every full build above step 1 — the #119/#164 class), and I do not
   own `_build_all.py`. NOT DONE, priced: 2 lines, conductor's call. It already has a consumer,
   so this is legibility, not coverage.
6. **`dashboard/index.html` bakes live `_governs` output** and will render differently once
   regenerated (s202-D3 no longer surfaces against `knowledge/` files). `gen_dashboard.py --check`
   is COULD-NOT-ASK (77) here for the pre-existing #193 reason, so this was not asked first-hand.
   Regenerating the dashboard is not in my owned set.
7. **`_validate_evidence.py` can never sample `bash knowledge/_git_commit.sh --selftest`** — its
   safety allowlist refuses any command containing the string `commit` ("arbitrary effect, no
   allowlist can vouch for it"), so that row is a DECLARED REFUSAL, not a pass, in every run of
   the linter. The command is genuinely read-only; the refusal is the linter being honest about
   what it cannot vouch for. Its real consumer is the new gates.yml step, which does run it.
   `python3 knowledge/_validate_evidence.py notes/_claims/208-wave1-claims.jsonl` → rc=0,
   "EVIDENCE GATE PASS … 2 declared refusal(s)".
8. **The mention-map gate costs one re-run** when it fires (regenerate → refuse → re-run with the
   path named). Deliberate: auto-staging is ruled out. If Dave prefers auto-staging for this one
   provably single-owner derived file, that is a ruling, not a repair.

---

## CONSEQUENCES / PITFALLS (mandatory)

- **The commit seam grew a gate that CAN refuse a legitimate commit.** If the mention map is
  stale, the conductor's first commit attempt will refuse and print the path to add. That is one
  extra round trip per affected commit, by design. `MENTION_MAP_ACK="<real reason>"` is the
  declared-gap hatch (declared passes, silent fails).
- **The msgfile door gate will refuse any msgfile written by the PRE-#208 script**, because those
  files really do carry a prefix on line 1. Expected, loud, with the remedy printed. Fresh printf
  per invocation, as the runbook already says.
- **`"$MSGFILE".t3-rendered` files now appear beside every msgfile.** They are derived and
  disposable, live in the session-owned `outputs/` dir, and are never staged. If a caller puts
  msgfiles somewhere tracked, those render files become untracked dirt at the next reconcile —
  keep msgfiles in `outputs/`, which the runbook already requires.
- **T3's headline is now in the render file, not the msgfile.** Anything that read the msgfile
  back after a run to learn the subject will now read the AUTHOR's line instead. Nothing in the
  repo does this (`MSG_HEAD` was already diagnostic-only since #171), but a habit might.
- **The `_governs` narrowing means fewer rulings surface at the capture gate.** Exactly one entry
  lost reach and it is declared by name every run — but a session that relied on `s202-D3`
  appearing whenever it touched `knowledge/**` will no longer be reminded. That is the honest
  trade for a matcher that carries information, and the remedy is a data fix, not a matcher fix.
- **Step numbers in this receipt are POSITIONAL and will drift.** `[110]` etc. are indices into
  `_build_all.STEPS`; the gates.yml prose already carries two generations of stale ones. Re-derive
  with the `ast` probe quoted under item 3 before trusting any bracket number.
- **Nothing here was committed, staged, pushed or checked out in the real repo.** Every commit
  drive ran in `/var/tmp/shim` (a scratch `git init` repo) and every CI reproduction in
  `/var/tmp/ciclone*` (throwaway clones). The one `git checkout` in this lane was inside a
  throwaway clone, to build the baseline.
