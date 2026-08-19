# #208 — VERIFIER WAVE (adversarial), the first REAL drive of W-44 + W-45

**Seat:** Opus adversarial verifier sub · session #208, conductor Fable · tree at `83977f5`
**Subject:** the three build-PM claim tables of #208 — `notes/_claims/208-wave{1,2,3}-claims.jsonl` (55 rows)
**Product:** `notes/_claims/208-verifier-challenges.jsonl` (60 rows) + this receipt
**Licensing question this run answers:** `s204-D1` holds W-44 and W-45 out of `_build_all.py` and CI *until driven in ≥1 real verifier wave*. This is that wave. The verdicts are below; the **ergonomics findings are the licence evidence** and they are not all comfortable.

---

## 1 · THE NUMBERS

`python3 knowledge/_join_claim_tables.py <all-208-claims> notes/_claims/208-verifier-challenges.jsonl` → rc=0

| | count |
|---|---|
| claim rows joined | **55** (wave1 16 · wave2 21 · wave3 18) |
| challenge rows | **60** |
| **CONFIRMED** | **51** |
| **CONTRADICTED** | **2** — `W2-20`, `W3-11` |
| **UNTESTED** | **2** — `W1-15`, `W2-21` (both structurally unfalsifiable — see NEW-5) |
| **NEW** | **5** |
| UNCHALLENGED | **0** — every claim row got a challenge row |
| surfaced by the join | 9 of 60; 51 collapsed to a count |

Evidence linter on my own table: `python3 knowledge/_validate_evidence.py notes/_claims/208-verifier-challenges.jsonl --seed 208` → **rc=0**, 58 of 60 rows mechanical, 0 lint failures, 0 rc mismatches. *(It failed with 8 lint failures on first write — that failure is finding 4 below and it is the most useful thing in this receipt.)*

### The two CONTRADICTED, in full

**`W2-20` — the patch WAS applied, in the very commit that landed the claim asserting it had not been.**
Wave 2 wrote: *"the exact patch is written in the receipt and NOT applied, the file being another sub's."* At HEAD there are **two** doc-row gate call sites in `knowledge/_git_commit.sh` — `:246` (pre-staging, the one wave 2 names) and `:568`, printing `— doc rows present for this commit's staged adds (_gate_doc_rows.py, post-staging)`. Provenance: `git show HEAD~2:knowledge/_git_commit.sh | grep -c 'post-staging'` → **0**; `git log -S 'post-staging' -- knowledge/_git_commit.sh` → **5882813**, the waves-1+2 commit. Wave 1 applied it in the same commit that shipped wave 2's claim that nobody had. The *diagnosis* (`:246` fires before staging at `:541`) reproduces exactly; the *status clause* does not.

**`W3-11` — `21 of 205` is not reachable under the row's own word "non-empty".**
Everything else in the row reproduces exactly: 76 items · `Counter({'claude': 47, 'dave': 29})` · `Counter({'open': 50, 'done': 24, 'parked': 1, 'blocked': 1})` · 22 open+dave · 19 UNCONDITIONED · 205 rulings. But *"rulings with a non-empty `open` field is 21 of 205"* measures three ways: truthy → **18**, key-present → **21**, non-empty-string → **2**. 21 is reachable only under KEY-PRESENT, which is the one reading the word *non-empty* excludes. Direction untouched; figure is 18. This is the #204 `D-7` class recurring — a figure whose stated rule does not regenerate it.

---

## 2 · WHAT I DROVE, NOT READ

Adversarial drives, all in scratch clones under `/sessions/relaxed-keen-euler/vfy/` (a full `--no-hardlinks` clone and a `--depth 1` clone). ⛔ Nothing was committed, staged, pushed or checked out in the real repo; ⛔ no real `_build_all.py` build was run at any point.

- **`_governs.py` near-misses, 15 hand-built pairs** — bare-dir/slashed-dir/basename/symbol/reverse-suffix/prefix-glued/empty. All behave as designed. Own mutation control (hand-typed pre-#208 `matches()`) → 2 failures; restored → 0.
- **Seven adversarial msgfiles through the real door gate** in a scratch clone. Four correctly refused, two correctly passed (unreachable shapes — T3 emits `date +%F` and `— ` literally), **one false positive** → NEW-2.
- **Five real commits landed in the full clone** (`4387b7a`, `f6211a7`, `cdba859`, `68ce12b`, …), driving `W1-10` (five arms), `W1-13`, `W1-14`.
- **`W1-14` made to BITE by mutation on a real commit** — patched T3's headline to carry an inherited prefix; the commit landed as `after #208 2026-08-19 — after #207 2026-08-18 — verifier doubled-subject drive` and the assert exited 1 with `SUBJECT PREFIX COUNT = 2`. Control (mutation reverted) → rc=0. The memory hook says this assert "has never been seen to fail" — **it has now, on demand, both directions.**
- **Doc-row staged arm, plant-and-detect on a real git index** — `git add`ed an unrowed brief, ran the HEAD~2 gate and the HEAD gate against the *same* index: old → rc=0 `✅ PASS` while shipping it; new → rc=1, named.
- **Eight plausible-but-unknown argv tokens** into `_build_all.py` — all rc=2, all refusal path, all returning before `check_routes()`.
- **`W3-5`/`W3-6` masking re-run with MY OWN masker** (11 IDREF attrs + `id=` + `href="#…"`), plus two controls the lane did not run: visible-text length unchanged on all seven files, and a masker mutation control proving it does not eat content. I also ran the lane's own `/var/tmp/diffverify.py` — it survives in this sandbox and returns rc=0.
- **`W3-1` re-driven against the pre-repair blobs** — `git checkout 83977f5~1 -- reviews/` then P-2 → rc=1, `46 finding(s)`, 10 DUPLICATE-ID + 36 UNRESOLVED-IDREF, 45 files. Every figure reproduces.

---

## 3 · ERGONOMICS FINDINGS — the licence evidence

These are the points where the instruments fought me. Ordered by how much they would matter once W-44/W-45 are in CI.

### 1. ⛔ THE EVIDENCE SAMPLER COMPARES EXIT CODES, NOT OBSERVATIONS — and it certified two rows whose evidence I had just proved false

`python3 knowledge/_validate_evidence.py notes/_claims/208-wave2-claims.jsonl --seed 208` → rc=0, `✅ EVIDENCE GATE PASS`, including:

```
✅ RAN W2-12 — git show HEAD:knowledge/_build_all.py → rc=0 (matches declared)
✅ RAN W2-7  — git show HEAD:knowledge/_assertions.json → rc=0 (matches declared)
```

Both commands exit 0. Both now print the **post-fix** file — the opposite of what those rows assert. `git show`, `grep -c`, `find`, `ls`, `sed -n` all return 0 for *any* content. So for read-style evidence — which is most of a claim table — the sampler proves **runnability, not reproduction**, and its green is close to vacuous.

**This is the one thing I would fix before wiring W-44 into CI.** The row needs an optional `expect` field (a substring of stdout, or a count) so the sampler can compare an *observation*. Without it, `EVIDENCE GATE PASS` on a claim table means "the commands still parse".

### 2. ⛔ `git show HEAD:` IS A MOVING POINTER — the act of committing a claim table invalidates its own evidence

Three wave-2 rows (`W2-7`, `W2-12`, `W2-16`) cite `git show HEAD:<path>` to establish a *pre-fix* state. That was true when written. The conductor then committed, and every one of those pointers now resolves to the fixed file. All three substances are CONFIRMED — at `HEAD~2`, which is `8c09888`. Finding 1 is why this went unnoticed: the linter ran all three and passed them.

**Remedy:** claim tables must cite an immutable ref (a SHA), never `HEAD` / `HEAD~n`. This is the `read-chain-is-where-staleness-is-free` class applied to claim evidence, and it is a one-line rule the linter could enforce: reject `HEAD` in a `git show` evidence token.

### 3. ⛔ THE LINTER HAS NO LEGAL FORM FOR AN ABSENCE — confirmed independently, twice, in my own writing (`W3-18` is right)

`knowledge/_validate_evidence.py:16-17` — *"A PATH token that does NOT EXIST is a HARD FAIL"* — with no ABSENT/EXPECTED-MISSING escape. Every row of mine whose finding *is* an absence (`W3-9`, `W3-17`, `NEW-4`) had to be written as a `grep … → rc=1, no output` **figure** rather than naming the path that is missing. And `W3-6` — an honest row saying *"the lane's exact bite is not re-runnable; I re-established the property with an independent instrument"* — was a HARD FAIL for carrying no probeable token, until I attached a token pointing at my own scratch script.

The linter is satisfied by **hiding the subject**. That is `honest-refusal-needs-a-legal-form` inside the W-44 instrument itself, and it now has three independent instances.

### 4. ⛔ A VERIFIER'S PATHS LIVE IN SCRATCH CLONES, AND THE RULED `s191-D2` MARKER IS NOT HONOURED

My first write of the challenge table failed the linter with **8 lint failures, 6 of them dead pointers** — all naming files that exist in my scratch clone but not in the mount. That is the verifier's *normal* working material: an adversarial seat plants files in throwaway trees by design.

I tested the ruled escape. `s191-D2` says a non-repo home is declared `(NON-REPO: <where>)`. Driving `_validate_evidence.paths_in()`:

| evidence form | `paths_in` sees |
|---|---|
| `` `notes/_vfy.txt` `` | `['notes/_vfy.txt']` → HARD FAIL |
| `` `notes/_vfy.txt` (NON-REPO: /…/vfy/full) `` | `['notes/_vfy.txt']` → **still HARD FAIL** |
| `` `notes/_vfy.txt…` `` (trailing ellipsis) | `[]` → passes |
| `` `/sessions/…/vfy/full/notes/_vfy.txt` `` | `[]` → passes |

Only two forms pass: an absolute clone path, or a **trailing-ellipsis hack**. I used absolute paths (honest — that is where the files really are), but note what the ellipsis form is: a way to launder a dead pointer past the gate by typing one character. **`_validate_evidence.py` should honour `(NON-REPO: …)`** — it is already the ruled vocabulary, and it makes the honest statement legal instead of the hack.

### 5. ⛔ `0 · lane discipline` ROWS ARE UNFALSIFIABLE THE MOMENT THE WRAP COMMITS

`W1-15` and `W2-21` both assert a property of the **working tree** (`git status --short` shows only the lane's paths / no staged entries). `git status --short` on the mount today is **empty** — the conductor committed. A verifier arriving after the wrap can neither confirm nor refute them, and both landed as UNTESTED for that reason alone.

In a topology where the conductor commits before the verifier runs, this section is structurally post-hoc-unverifiable. Either the verifier runs **before** the commit, or the row must carry a **pre-commit transcript** as its evidence rather than a command to re-run. (Correctly, both rows were tagged `CLAIMED`/`PROVEN` in a way that exempts them from the linter — the schema is not lying, the *seat ordering* is.)

### 6. `rc` IS ONE SCALAR ON A ROW THAT MAY CITE SEVERAL COMMANDS

`W1-13` cites three commands with three different exit codes. The sampler drew the third, compared it to the row's single `rc`, and reported `⛔ RC MISMATCH`. I removed the `rc` — the only legal move — which *loses information*. The schema needs either per-command rc, or an explicit convention that `rc` binds to the **first** command token (which is what `sample()` actually does when it picks — but the drawn command is not always the first).

### 7. THE JOIN IS 1:1 AND A WAVE IS N:1

`_join_claim_tables.py` refuses three claim files: `✖ REFUSED: need exactly <claims.jsonl> <challenges.jsonl>` rc=2. A three-PM wave forces the conductor to `cat` the tables into a temp file first — and the generated `## Sources` header then cites **that temp path** as the provenance of the join, which is a write-once/ADR-0017 wound in a GENERATED file. Accepting `N` claim files (as `_validate_evidence.py` already does) removes both problems.

### 8. THE PROBE-RUN FORM IS REFUSED AS SIDE-EFFECTING WHEN IT IS NOT

Linting wave 3: `⛔ REFUSED [SIDE-EFFECTS] W3-1 — python3 knowledge/_probe_registry/_registry.py --run --probe P-2 — a bare python3 REWRITES its tracked audit output`. `--run --probe` is a **read-only probe drive**; the classifier keys on the absence of `--check`/`--selftest`/`--dry-run` and cannot see it. Under `--strict-sample` this would be an rc=1. `classify()` should learn `--run` for registry probes, or the registry should accept `--check --probe P-N`.

### 9. `/var/tmp` WAS AT 92% AND MY FIRST CLONE DIED ENOSPC

`git clone` into `/var/tmp` → `fatal: … No space left on device`. `df -h /` → 9.6G, 824M free; prior waves left `/var/tmp/ciclone` and `/var/tmp/ciclone_base` at **929M each**. I moved to `/sessions/relaxed-keen-euler/vfy/` (7.8G free) where a full clone is only 47M. A verifier seat needs scratch space as a stated prerequisite, and waves should clean their clones.

---

## 4 · THE FIVE NEW FINDINGS (detail in the JSONL)

- **NEW-1** — the sampler compares exit codes, not observations (finding 1 above).
- **NEW-2** — ⛔ **the #208 door gate has no legal form for an honest subject that quotes a prior one.** `prefix_count` uses `re.findall` (unanchored) where the #170 gate it widens uses `re.match` at `:487` (anchored). A *fresh* subject containing a prefix-shaped string mid-line is refused, and there is **no ACK hatch** — `grep -n 'MSGFILE_ACK\|REUSE_ACK\|ALLOW_PREFIX'` → no match — unlike its two neighbours `SESSION_ACK` and `MENTION_MAP_ACK`. The selftest's near-miss for this shape (`'fixes the class #205 found'`) carries no date, so it never exercises the case. ⬛ Anchoring it, or adding a hatch, is another sub's gate and is not mine to change.
- **NEW-3** — a gate whose verdict depends on **clone depth**, and a **mutation proof that `fetch-depth: 0` in `gates.yml` is load-bearing**. In a `--depth 1` clone, `_gate_doc_rows.py --check` → rc=1 (false finding: every file dates to the single commit) and `_capture_gate.py --selftest` → rc=1 (`s198-D2` points at commit `5b77cce`, absent from a shallow clone) where the full clone returns 77. ✅ CI is already safe: `gates.yml:167` and `:208` both set `fetch-depth: 0` and the header at `:138` names this as the second independent #173 cause. **Recorded so that line is never trimmed as redundant.**
- **NEW-4** — a probe that expected to contradict and did not. `_governs.matches()` compares a lowercased `governs` entry against a **raw** target; `matches({'governs':['BOOT_FIRSTTURN_TK']}, {'BOOT_FIRSTTURN_TK'})` → False, and **223** non-anchor governs entries carry an uppercase character. It holds only because all three call sites normalise (`_capture_gate.py:4273`, `:5522`, `_governs.py:745`). The selftest's symbol bite uses `measure_tokens` — already lowercase — so nothing would notice a fourth caller that forgot. A one-line `t = _norm(t)` inside `matches()` makes the invariant local instead of conventional. ⬛ Not mine to apply.
- **NEW-5** — finding 5 above, as a row.

---

## 5 · RESIDUALS AND DECLARED STOPS

- **`W1-14`'s exact route was not reproduced.** I made the class bite through a different door (mutating T3's headline) rather than driving a full `--wrap` with a planted GOOD-MORNING banner. The `--wrap` path runs the spine writer and capture gate and is not safe or cheap from this seat. The assert itself is proven, on a real landed commit, both directions.
- **`W3-14`'s black-pixel arm is UNTESTABLE-FROM-THIS-SEAT** — Playwright is not importable here (`probe_dangling_var_pixel.py --check` → rc=77). The empty-population arm is confirmed.
- **`W3-2`'s per-pane `n==1` assertion is UNTESTABLE-FROM-THIS-SEAT** — it lived in an ephemeral repair script. Its *prediction* is confirmed (0 DUPLICATE-ID after; every changed byte inside an id/IDREF/fragment value; 220 insertions / 220 deletions, equal-line on all seven files).
- **The commit path is unreachable from a bare clone** until `knowledge/.token-cache.json` is copied in — `_gen_chain.py --check` returns COULD-NOT-ASK first (#173, both sources gitignored). I copied it into my scratch clone. Anyone re-running `W1-10`/`W1-13`/`W1-14` from a clone needs that step, and it is in none of the wave-1 evidence.
- **Verdict vocabulary collision, declared.** My brief asked for `CONFIRMED / REFUTED / UNTESTABLE-FROM-THIS-SEAT`. The ruled #204 shape — and the only vocabulary `_join_claim_tables.py` classifies — is `CONFIRMED / CONTRADICTED / UNTESTED / NEW`. I used the **ruled** vocabulary so the join works, and put "UNTESTABLE-FROM-THIS-SEAT" in `note`. Worth settling in words so the next brief and the instrument agree.
- **`_checkin.py` from a sub seat reads the CONDUCTOR'S log, not mine.** `python3 knowledge/_checkin.py` → `FILL 139,680 real · room to stop line 11,249 · throughput 190,393 · boot 57,050`. That is the conductor's window and it is worth his attention; it says nothing about a sub's. A sub cannot measure its own fill with this instrument — declared, not guessed.

## 6 · PATHS CHANGED BY THIS LANE

| path | what |
|---|---|
| `notes/_claims/208-verifier-challenges.jsonl` | NEW — 60 challenge rows, #204 schema |
| `notes/_receipts/2026-08-19-208-verifier-wave.md` | NEW — this receipt |

Plus two **declared instrumentation appends** (W-22), written by my own `_checkin.py` run and not by any edit of mine:

| path | writer |
|---|---|
| `notes/_REHEARSAL-LOG.jsonl` | `_checkin.py` (rehearsal row) — EXCLUDED from the push gate by `s137-D1` |
| `notes/_dream/_GRADE-DECISIONS.jsonl` | `_checkin.py` B3 grade alerts — NOT excluded; its policy is ⬛ Dave's, unruled |

Full `git status --short` at hand-off: those two `M` lines and the two `??` lines above — nothing else. Every drive that needed a mutable tree ran in `/sessions/relaxed-keen-euler/vfy/{full,scratch}`; nothing in the repo was staged, committed, pushed or checked out.

⚠ **Neither new file is in a gate's scope.** `_gate_doc_rows.py:48` scopes to `notes/_briefs` / `_BRIEF-*`, and P-4's glob is `notes/_briefs/*.md` — so `notes/_claims/` and `notes/_receipts/` are invisible to both, and `python3 knowledge/_gate_doc_rows.py --check` → rc=0 `unrowed 0` says nothing about them. Whether `notes/_claims/` earns a store row is already an open question on the #207 banner (⬛ Dave's); this run adds a second file to it and does not rule it.
