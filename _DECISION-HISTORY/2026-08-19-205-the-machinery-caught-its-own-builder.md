# #205 — the machinery caught its own builder's source

provenance: 205 · 2026-08-19
status: observed

*Spine entry: `_LIVE-STATE.md` § ⏱ LATEST DELTA (**#205**) · banner: `GOOD-MORNING.md` § ★ LATEST (**#205**).
⛔ **ZERO rulings were inscribed this session** — there is no ledger line to link to, and that absence is
the first thing this dossier records. `knowledge/_rulings.json` is byte-untouched.*

---

## 0. What this session was, in one line

#204 ordered `W-44` and `W-45` as builds and `W-46` as a scope-only lane. #205 cleared the CI debt
#204 left behind, re-based an assertion that had correctly refused to let a build finish, built `W-44`,
and then **drove `W-44` against #204's own claim tables** — where it disagreed with the count #204 had
typed about itself.

---

## 1. The CI arc — and why "six fails" was not the same shape as "one fail"

#204's head ran **RED with six fails**: `[3]` `[13]` `[40]` `[45]` `[50]` `[110]`. The declared
expectation carried into #205 was **`[13]` only**. The gap is not carelessness; it is the composition of
the failure being invisible from the outside:

- **five of the six were the stale-bake class.** #204 built six new components and never got a complete
  build pass, so five downstream artefacts were baked from a pre-#204 corpus.
- **`[3]` and `[110]` were re-staled by #204's own wrap edits** landing in the same commit — the
  regen-last-before-commit class, where the wrap's own writes invalidate artefacts the wrap already
  regenerated.

**The method miss, recorded because it is the reusable part:** #205's opener **re-derived the six-fail
composition from CI** rather than reading it off the `pm-topology-adopted-204` memory hook, where #204's
seat had already put it. Root cause was not the hook's body but **its index line, which was too thin to
advertise what it held**. The conductor fattened the index line the same session. ⚠ That edit is
**NON-REPO** (`s191-D2` home-or-declare) and unreachable from the wrap sub's seat, so it is recorded here
as **the conductor's**, not claimed by the wrap.

**The repair.** A Sonnet chore sub (110,219 tk) regenerated the five generators **targeted** — see §2 for
why targeted and not wholesale — and committed `f71202e`. The conductor pushed. CI on `df2c9eb`
(run **32253533450**) returned **SURVEY 49 pass · 1 FAIL, `[13]` only**: the predicted best honest state.

⚠ **`[13]` is `_governs.py`'s too-loose matcher.** It is standing red, untouched, and nobody has priced
its fix. "1 fail" reads as "nearly green" and that reading is the trap.

⚠ **And the class is not closed.** CI **surveys; it never regenerates.** The five gates are green only
because the artefacts were regenerated *locally* and pushed. The next generator change re-stales them by
exactly the same route.

---

## 2. ASSERT-009 — an assertion that stopped a build, and was right to

The chore sub's first move was a full `_build_all.py` run. It **ABORTED at the veracity gate**, on
ASSERT-009's count having drifted. That abort is the reason the regeneration became targeted, and it is
worth saying plainly: **the assertion did its job.** A gate that refuses a build on a drifted fact is the
design working, not an obstacle.

Dave's word was *"do it"* — a chat authorisation, **not inscribed as a ruling**.

**Re-measured first-hand, not inherited:** **92 dir metas · 96 entries**. The old *"77 repo-wide"* framing
is **RETIRED**, and the retirement matters more than the number: **repo-wide is now 176**, which is a
*different population*, so 77 → 92 is not a delta on the same quantity. Calling it one would have been a
unit error dressed as a measurement [[measure-dont-convert-units]].

**Four-doc correction pass, BY ADDITION, nothing trimmed:**

- `knowledge/_assertions.json` — n=92 plus provenance
- `_LIVE-STATE.md` § OPEN #131 note, and the guard 76 → 92
- `notes/_MEMENTO-DECISIONS.md` — addendum line
- `_DECISION-HISTORY/2026-08-08-131-…` — addendum

`python3 knowledge/_validate_assertions.py` → **rc=0, "8 claim(s) still true"**. Receipt:
`notes/_receipts/2026-08-19-205-assert009-rebase.md`. Commit `87dfcc4`.

⛔ **Declared NOT fixed, and the declaration is the point:**

- `asserted_in` still names `GOOD-MORNING.md`, but **GM no longer carries the figure** — it rolled. This
  is the home-pointer-rot class: the pointer survives the roll and quietly stops resolving.
- **ASSERT-001 is past its 30-day recheck window** (webfonts). Unrelated to this session, untouched, and
  named here so it is countable rather than invisible.

⬛ **The remedy question (a)/(b)/(c) is UNCHANGED and DAVE'S.** Nothing in this session narrowed it.

---

## 3. Reading #204's dossier back — two defects, corrected by addendum

Dave asked for the #204 dossier to be checked. It was read against the record rather than against itself:
figures, ruling and receipts all check out. **Two defects were found and corrected by an in-file
addendum; nothing was trimmed** [[feedback-header-wins-over-audit]].

**(a)** Its §5 said *"`[13]` and `[114]` still red"*. That was **stale at the moment it was written** —
`[114]` went green during #204's own wrap, and the real red set was the six at §1. A wrap describing its
own CI state is describing a moving target, and this is what that costs.

**(b)** Its claimed back-link from `_LIVE-STATE.md` **does not exist** (`grep` → 0 matches). The
both-way-links rule was asserted, not enacted. Left to the next spine-writer pass and **declared** —
because a back-link written into a dossier by a wrap sub is a different act from a spine edit, and
pretending otherwise would put a false claim in the file that just corrected one.

---

## 4. `W-44` — four instruments, and what each exists to refuse

Built by an Opus build-PM (172,271 tk), commit `541ffcc`. All selftests **rc=0**, plant-then-detect proven
in **both** directions — a planted defect is caught, and a clean corpus is not falsely accused
[[mutation-tests-the-clause-not-the-feature]].

- **`knowledge/_claimtable.py`** — the schema plus a **loud** loader. A malformed row fails named, never
  silently coerced [[a-crash-is-not-a-fail]].
- **`_join_claim_tables.py`** — surfaces **disagreement / untested / fence / unchallenged only**;
  CONFIRMED collapses to a count. A **suppression selftest arm** proves a hidden row surfaces, which is
  the one property a join that hides things must be able to demonstrate.
- **`_validate_evidence.py`** — the `s182-D1` linter (every mechanical claim carries its probeable token)
  plus a seeded sampler that actually *runs* sampled evidence.
- **`_gen_claim_table_md.py`** — the md is generated **from** the jsonl, per ADR-0017's write-once
  principle: one home for the live facts, addresses everywhere else.

Canonical table: `notes/_claims/205-w44-claims.jsonl` (**24 rows**), with its md receipt generated from it
— the tool dogfooded on its own build.

⛔ **NOT wired into `_build_all.py` and NOT wired into CI.** That is `s204-D1`'s condition, not an
oversight: **not until it has been driven in ≥1 real wave.**

---

## 5. Driving it on #204's real tables — three findings

Derived JSONL copies were made under `notes/_claims/`; **the originals are byte-unchanged.**

### (i) #204's typed count is not reproducible from #204's own rows

#204 reported **"34 CONFIRMED / 12 UNTESTED"**. Re-derived mechanically from the rows it was reporting on,
the figure **under a stated rule** is **46/11**. CONTRADICTED **3** and NEW **4** reproduce exactly.

This is the typed-count-lies class, caught by the machinery built for it — and the machinery caught it in
its *own author's* source material, one session after that source was written.

⛔ **46/11 IS NOT "THE CORRECTED FIGURE".** It is *"the reproducible figure under a stated rule"*. Quoting
it as "#204's real numbers" would swap one typed count for another and throw away the only thing that
makes it better: the rule. The builder's **one** judgment override (C-7 → UNTESTED) is **declared in
code**, not folded into the total.

### (ii) Three claims were never challenged at all

**C-5, F-7 and F-8** received **no challenge row**, and **the verifier's own omissions list misses them**.
An inner join cannot report a row that has no partner — the blindness is structural, not clerical. The
new **UNCHALLENGED class** is the fix, and this is its first real sighting.

### (iii) The evidence linter on #204's tables: rc=1, five failures

One dead pointer written twice, plus three rows with **no probeable token** — the exact `s182-D1` clause.

---

## 6. The dead-ends, because they are the honest half

The fix loop (`s204-D1` amendment ②) ran **four times in-lane, all four on the builder's own defects**:

1. a converter **glob-stripping bug**
2. a **linter false-positive class**
3. a **sampler stdin hang** — first **misreported as an environment gap**, which is the more interesting
   error: a hang is easier to blame on the sandbox than on the code
4. **two dead pointers in its own claim table** — the linter found them in the file the linter's author
   had just written

**Lossy hops this session: 0** (compare #204's one). **No browser was driven and nothing visual was
built** — so nothing here is an assertion about appearance.

---

## 7. What is open, and stays open

⬛ **Five PROPOSED schema choices stand as defaults, each recorded with its rejected alternative** —
`notes/_claims/205-w44-claims.jsonl` rows **W44-16 … W44-20**:

1. NEW as a stored **and** derived cross-check
2. kind-aware id uniqueness
3. a `fence` field that surfaces at **any** verdict
4. the UNCHALLENGED class
5. unknown-fields-fail, **with an evidence exemption for CLAIMED / UNPROVEN / UNTESTED rows**

The conductor's recommendation, relayed to Dave: take them as **one batch**, and let the test be the next
real PM wave; **the exemption boundary (5) is flagged as the most-likely-wrong**. ⬛ **All five remain
Dave's. Nothing here is ruled.**

⛔ **The priced gap, the builder's own and honest:** the evidence sampler **refuses every bare
`python3 knowledge/_validate_*.py` command** — `[SIDE-EFFECTS — they rewrite tracked audits]` — so its
coverage of **gate** evidence is **structurally near-zero** until those gates grow a `--check` form. A
green linter run says nothing about the gates it declined to execute.

⛔ **Also UNPROVEN:** no PM has yet written the JSONL **from scratch**. Its ergonomics are untested —
which is precisely `s204-D1`'s *"driven in ≥1 real wave"* condition, still unmet.

⬛ **Still Dave's, untouched by this session:** the ASSERT-009 remedy (a)/(b)/(c) · whether
`notes/_claims/` earns its own store row · the `[13]` / `_governs.py` matcher fix · the 0.40
chain-selftest constant · the `_GRADE-DECISIONS.jsonl` commit/exclude policy · the `s203-D2` permanence
verdict (**adoption ≠ permanence**) · the **35-surface review queue**, on which nothing was ruled ·
G8/G14 and every standing ⬛ in the record.

---

## 8. Housekeeping, recorded rather than smoothed

- The **rehearsal gate** caught a **stale retrieval index** mid-session, after the `_LIVE-STATE.md` edit —
  the #32 class, which is exactly what that gate exists for. Rebuilt and committed cheaply at `69e6c3c`.
- A `python3` invocation with an **empty argument substitution sat on stdin to a timeout** at the
  conductor's seat. No damage; verified by `git status`. Written down instead of tidied away, because a
  tidied-away wart is a wart nobody can count.

---

## 9. Gauge

⚠ **The conductor's figures, first-hand at the conductor's seat, relayed — not this wrap sub's.**

boot **57,004 real** (in band per `knowledge/_gauge_tokens.py`) · **FILL at the wrap-brief cut ~156,000
real — PAST the ADVISORY stop line 150,929**, UNDER the **200,000** working line, the **256,000** wall
BINDING · **subs 282,490 tokens (n=2, MEASURED: 110,219 + 172,271)** · **effort band `L`** — job window
= FILL − boot ≈ **99,000 real**, graded against edges **45,000 / 75,000** re-derived first-hand from
`gen_dashboard.effort_anchors()` (n=26) rather than quoted from `s168-D2`'s own 45K/85K text. The edge
moving with the corpus is the derivation working, not drift.

⛔ **This wrap sub's own spend is EXCLUDED and unknowable from its seat — declared, never estimated.**

**QUOTA at the opener, Dave's panel verbatim:** *"All models Resets Thu 10:59 PM 58% used · Fable Resets
Thu 10:59 PM 68% used"* (deltas vs #204's opener: **All +4 / Fable +2**). ⬛ **The close panel is OWED** —
the conductor asks Dave in chat; it is not invented here.

⚠ **FILL closed past the advisory stop line for a fourth consecutive session.** That is a trend, not an
incident, and the wrap term keeps being bought out of the working-line margin.

---

## 10. Commits

`f71202e` · `df2c9eb` · `87dfcc4` · `541ffcc` · `69e6c3c` · `cbbc8e1` — all pushed, remote verified at
`cbbc8e1`. The tree was **clean at wrap-open**, so the wrap commit carries the ritual's own edits and
nothing else.

---

*Both-way links: spine → `_LIVE-STATE.md` § ⏱ LATEST DELTA (#205); banner → `GOOD-MORNING.md` § ★ LATEST
(#205). ⚠ Per §3(b), the corresponding back-link INTO `_LIVE-STATE.md` for the #204 dossier is still
missing and is declared open — this dossier does not silently repeat that claim about itself.*
