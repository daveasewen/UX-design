# Session #208 — WAVE 3 receipt: the externality-bearing mechanical repairs

status: observed
provenance: session #208, 2026-08-19, Opus work sub (lane: WAVE 3 — externality-bearing repairs), conductor Fable

Claim table (machine-linted): `notes/_claims/208-wave3-claims.jsonl` — `python3 knowledge/_validate_evidence.py notes/_claims/208-wave3-claims.jsonl` → **rc=0**, 18 rows, 18 mechanical, 0 lint failures, 5 sampled rows re-run with matching rc.
Check-in mid-lane: `python3 knowledge/_checkin.py` → FILL 127,601 real · boot 57,050 · room to the advisory stop line 23,328.

⛔ ALL THREE ITEMS' PREMISES WERE VERIFIED FIRST-HAND BEFORE ANY FIX. One briefed figure had aged
(item 2, 204 → 205) and one briefed instruction turned out to have **no code to repair at all**
(item 2 again). Both are stated before the repairs, because they are what a reader acts on.

---

## PATHS MODIFIED (complete list)

| path | what |
|---|---|
| `reviews/REVIEW-174-progress-bar-four-themes-v1.html` | 3 duplicate ids suffixed per pane + their in-pane references (48/48 lines) |
| `reviews/REVIEW-203-avatar-group-four-themes-v1.html` | 1 duplicate id suffixed per pane + references (16/16) |
| `reviews/REVIEW-203-kpi-tile-four-themes-v1.html` | 3 duplicate SVG `<symbol>` ids suffixed per pane + their `use href="#…"` (72/72) |
| `reviews/REVIEW-203-timeline-four-themes-v1.html` | 3 duplicate heading ids suffixed per pane + their `aria-labelledby` (48/48) |
| `reviews/REVIEW-203-date-picker-four-themes-v1.html` | 9 dangling `aria-describedby` tokens pointed at the id already in their pane (9/9) |
| `reviews/REVIEW-203-date-range-picker-four-themes-v1.html` | 18 dangling `aria-describedby` tokens, same (18/18) |
| `reviews/REVIEW-203-time-picker-four-themes-v1.html` | 9 dangling `aria-describedby` tokens, same (9/9) |
| `knowledge/_probe_registry/probe_dangling_var_pixel.py` | P-3's two refusal paths now exit **77 COULD-NOT-ASK** instead of 1; docstring EXIT contract corrected |
| `knowledge/_probe_registry/_registry.py` | the CONSUMER half: `verdict()` (new, one predicate), a COULD-NOT-ASK block in `run()`, refusal-aware `selftests()`, 7 new selftest bites, usage block |
| `knowledge/_probe_registry/README.md` | the "exits 1" sentence corrected to the 77 convention |
| `notes/_receipts/2026-08-19-208-wave3-externality-repairs.md` | this receipt (new) |
| `notes/_claims/208-wave3-claims.jsonl` | claim table for the evidence linter (new) |

⚠ **Instrumentation appends, not edits** (the W-22 declared class): `notes/_REHEARSAL-LOG.jsonl`,
`notes/_dream/_GRADE-DECISIONS.jsonl` — written by `knowledge/_checkin.py` while measuring.

NOT modified, deliberately: `knowledge/_rulings.json` (only `_inscribe_ruling.py` may write it),
`knowledge/_state.json`, `knowledge/_probe_registry/manifest.jsonl` (its P-3 `blind` prose is now
one clause behind — declared as residual 3 below rather than edited, because the ledger is the
promotion evidence and W-45 owns its schema), `.github/workflows/gates.yml`,
`knowledge/_build_all.py`, any generated file. **No commit, no push, no checkout, no `git add`.**

---

## ITEM 1 — P-2's findings: the #204 anchor-ID class on the pre-#204 pages

**Premise, verified, and it held EXACTLY.** `python3 knowledge/_probe_registry/_registry.py --run
--probe P-2` → **rc=1**, `P-2 duplicate-ID/IDREF scan: 45 file(s) over ['reviews/REVIEW-*.html'] ·
46 finding(s) · 56 WARN-tier fragment miss(es)`. The 46 are **10 DUPLICATE-ID + 36
UNRESOLVED-IDREF across exactly 7 files**, as briefed. (The 56 WARN-tier fragment misses are the
#204-declared placeholder demo links; the probe does not count them and neither did this lane.)

**Two shapes, not one — and this matters, because they take opposite repairs:**

1. **DUPLICATE-ID (4 files, 10 ids).** Each page repeats one id set once per theme pane. Verified
   before touching anything: every offending id occurs **exactly once per pane** and every
   reference to it lives **inside the same pane** — so no reference crosses a pane and a per-pane
   suffix is a total repair. The suffix copies the #204 FIX-2 convention `--<theme>-<mode>`
   (probe: `reviews/REVIEW-204-popconfirm-four-themes-v1.html` carries `pc-delete--mono-light`).
2. **UNRESOLVED-IDREF (3 files, 36 tokens).** One shape only: an `aria-describedby` whose FIRST
   token was never given the suffix its target already carries. `…time-picker…:69` read
   `aria-describedby="f-time-help f-time-msg-mono-light"` while the help paragraph on line 66 is
   `id="f-time-help-mono-light"`. **The repair points the token at the id that already exists** —
   no id invented, no element added, no attribute removed. (These three files carry a NINTH
   `narrow · light` pane; the suffix was resolved from the ids present in each pane, never from
   the pane caption, so the ninth pane repaired itself correctly.)

**⛔ THE HARD FENCE, AND HOW IT WAS PROVEN — not asserted.** These are review surfaces awaiting
Dave's untriaged eye. The proof is stronger than a diff read: every `id` value, every IDREF
attribute value and every `href="#…"` fragment in BOTH the HEAD blob and the repaired file was
replaced with a single placeholder, and the two masked texts compared byte-for-byte.

| file | masked-identical to HEAD | numstat |
|---|---|---|
| REVIEW-174-progress-bar-four-themes-v1.html | **True** | 48 / 48 |
| REVIEW-203-avatar-group-four-themes-v1.html | **True** | 16 / 16 |
| REVIEW-203-kpi-tile-four-themes-v1.html | **True** | 72 / 72 |
| REVIEW-203-timeline-four-themes-v1.html | **True** | 48 / 48 |
| REVIEW-203-date-picker-four-themes-v1.html | **True** | 9 / 9 |
| REVIEW-203-date-range-picker-four-themes-v1.html | **True** | 18 / 18 |
| REVIEW-203-time-picker-four-themes-v1.html | **True** | 9 / 9 |

Equal added/removed counts on every file: **no line was added or removed anywhere**. Masked
identity means no text, no class, no style, no attribute other than those three kinds changed.

**And the fence check BITES** ([[mutation-tests-the-clause-not-the-feature]] — the check must be
able to fail): changing ONE word in the timeline page (`Transaction history` → `Transaction
HISTORY`) flipped that row to `masked-identical=False` and the verifier to **rc=1**; restoring the
file returned it to **rc=0**.

**A rename cannot move a pixel here, and that was measured too:** not one of the seven files
carries a CSS `#id` selector or a `getElementById`/`querySelector` lookup for any renamed id
(`grep -c getElementById reviews/REVIEW-203-kpi-tile-four-themes-v1.html` → 0). The only readers
of these ids are the accessibility tree and the SVG `<use>` references, both of which the repair
rewrote in step.

**After:** `python3 knowledge/_probe_registry/probe_dup_ids.py --check` → **rc=0**, `45 file(s) …
0 finding(s)`. All seven repaired files report `DUP=0 unresolved_idref=0`. Whole-registry run:
**rc=0**.

---

## ITEM 2 — the `s204-D1` non-filter: ⛔ STOPPED, IT IS DAVE'S. There is nothing mechanical here.

**Premise re-measured, and the figure has AGED (direction unchanged):** the brief and the #207
proposal say *204 of 204*; today it is **205 of 205** rulings carrying `by: Dave`
(`grep -c '"by": "Dave"' knowledge/_rulings.json` → 205; `grep -c '"id":'` → 205).

**The diagnosis asked for — WHY it matches everything — is not "wrong field" or "wrong
predicate". It is that THERE IS NO PREDICATE.**

- `grep -rn 'get("by")' --include=*.py knowledge/` → **rc=1**. Nothing in the repo selects rulings
  on `by`. The single reader of that field anywhere is a **Counter** at
  `knowledge/_gen_schematic.py:394`.
- The brief generator the filter was specified for **is not built** (`ls` of it in `knowledge/`
  → rc=2). W-46 was scope-only and HELD at #207.
- ⇒ The "filter" exists **only as prose**, in `s204-D1` item 4 and the programme brief. It has
  never run. This is [[instrument-without-a-consumer]] read backwards: a *specification* nobody
  has crossed yet, and the crossing is where it would have failed.

**The mechanism, so the repair is not mis-aimed:** `by` is a **constant, not a discriminator**.
`knowledge/_inscribe_ruling.py:62` lists it in `KEYS` and `:108` requires it non-empty, but no
allowed-value set constrains it and every ruling ever inscribed carries `Dave`. Any predicate
reading it selects the whole store, by construction. **Every ruling genuinely is tagged** — the
third of the three hypotheses in my brief.

**⛔ THEREFORE THE REPAIR IS NOT MECHANICAL AND I STOPPED.** Making that field discriminate needs
either retro-tagging 205 rulings or rewriting `s204-D1`'s item-4 text. Both are Dave's, both are
explicitly out of this lane. Options, priced, so the decision is one reading:

| option | what it costs | what it buys | what it breaks |
|---|---|---|---|
| **A · re-source the list** — drop `by` and read `knowledge/_state.json` `state=open AND owner=dave`, **+ a human-appended lane block** | 0 today (the generator is unbuilt); ~1 lane when it is | a list that actually selects: **22 of 76** items | nothing — `by` keeps its (non-)meaning; a correction to `s204-D1` item-4 wording, which is why it is Dave's |
| **B · re-source from rulings** — rulings with a non-empty `open` field | same | **21 of 205** | ties DO-NOT-RULE to a field with no writer discipline |
| **C · retro-tag the store** — add a real owner/authority field to 205 rulings | a bulk rewrite of `_rulings.json` through `_inscribe_ruling.py`, the only legal writer | a genuine filter | ⛔ 205 history rows rewritten; ADR-0017 says history is frozen. **Not recommended.** |
| **D · leave it, and say so** | 0 | honesty | the phrase "rulings tagged Dave's" stays in a ruling while meaning "all rulings" |

⚠ **The #207 brief's replacement figures HAVE ALSO AGED — re-measured here, do not carry the old
ones:** state items `open` + `owner=dave` = **22 of 76** (brief: 21 of 73); rulings with a
non-empty `open` field = **21 of 205** (brief: 21 of 204); `condition: UNCONDITIONED` = **19**
(unchanged). Store totals today: 76 items, owner `{claude: 47, dave: 29}`, state `{open: 50,
done: 24, parked: 1, blocked: 1}`.

This is Q2.1 of the #207 proposals, still open, now with fresher numbers and a sharper diagnosis:
**it is not a broken filter, it is an unbuilt one specified against a constant.**

---

## ITEM 3 — P-3's refusal gets a legal form (rc=77 COULD-NOT-ASK)

**Premise, verified first-hand.** Before this lane both of P-3's refusal paths — `check()` and
`selftest()` — printed `NOT-IN-THIS-ENVIRONMENT: …` and returned **1**. A CI consumer reads that
as a measured red. The probe's own docstring said "REFUSES by name and exits 1", so the defect was
specified, not accidental.

**The convention was COPIED, not re-invented** ([[reference-dont-duplicate-adr]]): read from
`knowledge/_could_not_ask.py` (EXIT 77 + a first line beginning `COULD-NOT-ASK:` carrying the
gate's own reason), from `.github/workflows/gates.yml:24` ("THREE VERDICTS, NOT TWO") and from
`knowledge/_build_survey.py:236-250`, which prints refusals in their own block and **excludes them
from its exit code**. The refusal is keyed on the **unreachable input** (playwright /
headless_shell), never on "am I in CI" — the `_could_not_ask.py` prohibition, which
[[gate-cannot-pass-in-one-environment]] is the reason for.

**What changed:**
- `knowledge/_probe_registry/probe_dangling_var_pixel.py:231` — `check()`'s refusal is now
  `cna.refuse("P-3 dangling-var PIXEL test", refusal)`.
- `…:272` — `selftest()`'s refusal, same.
- docstring EXIT contract rewritten: `0 clean · 1 findings (a MEASURED failure) · 77
  COULD-NOT-ASK`.

**⛔ AND THE CONSUMER WAS TAUGHT — otherwise this repair would have been a costume.** The
registry runner bucketed on `rc != 0`, so it would have counted the new 77 as a red and the
convention would have bought nothing ([[instrument-without-a-consumer]]).
`knowledge/_probe_registry/_registry.py:215` now holds **one** predicate, `verdict(rc, findings)`
→ `PASS | FAIL | REFUSED | SKIP`, used by `run()`; refusals print in their own block
(`…:280`) in the probe's own words and are excluded from the run's exit code, the
`_build_survey.py` posture. `selftests()` reports a refused selftest as `77(COULD-NOT-ASK)` rather
than folding it into `rc_total`.

**Driven, both directions, on real data:**

| arm | command | rc |
|---|---|---|
| refusal, `--check` (no playwright in this sandbox) | `python3 knowledge/_probe_registry/probe_dangling_var_pixel.py --check` | **77**, first line `COULD-NOT-ASK: P-3 dangling-var PIXEL test — NOT-IN-THIS-ENVIRONMENT: playwright is not importable…` |
| refusal, `--selftest` | same script `--selftest` | **77**, marked line + "never a pass, and distinguishable from the rc=1 a real red returns" |
| **a real failure still bites** — empty population | `… --check --glob 'knowledge/snippets/NOPE-*.html'` | **1**, "THE GLOB MATCHED NOTHING — an empty population is not a pass" |
| **a real failure still bites** — findings path, real 14-page glob, `drive()` returning a measured pure-black suspect | in-process drive of `check()` | **1**, "14 page(s) rendered … 1 suspect(s), 1 of them painting PURE BLACK" |
| consumer, full registry | `python3 knowledge/_probe_registry/_registry.py --run` | **0** — P-1/P-2/P-4/P-5 pass, P-3 shown `REFUSED` in a ⛔ COULD-NOT-ASK block with its own reason |
| consumer, selftests | `… --selftests` | **0**, table shows `P-3 rc=77(COULD-NOT-ASK)` |
| consumer bites | `… --selftest` | **0**, 7 new verdict bites green |
| consumer bites FIRE | `verdict()` monkeypatched back to the pre-#208 two-verdict rule | **1** — exactly the two refusal bites fail: "VERDICT WRONG: 77 + no findings is a REFUSAL, never a red" |

**Reach, stated honestly:** the registry is **not wired into `_build_all.py` or CI** (`s204-D1`
forbids it until the registry has run in ≥1 real wave). So this repair changes **no CI verdict
today**. It removes the trap that would fire the day `s204-D1` item 5 wires the pixel leg in —
and `knowledge/_build_all.py:1131` already reads `rc == 77` as the third verdict, so the receiving
end is ready.

---

## RESIDUALS — declared, not fixed

1. **⬛ ITEM 2 IS DAVE'S AND IS NOT DONE.** Four options priced above. Nothing was changed in
   `_rulings.json` or any ruling text. Until it is decided, `s204-D1` item 4 specifies a filter
   that would select every ruling in the store — harmless only because the tool that would read
   it does not exist.
2. **The 56 WARN-tier fragment misses remain** (`#doc-jun`, `#dl-may`, …). Inherited #204
   judgment: a placeholder-demo-link design question, not this class. Untouched, by design.
3. **`manifest.jsonl`'s P-3 `blind` prose is one clause behind** — it says the CI leg is UNPROVEN
   (still true) but predates the 77 form. NOT edited: the manifest ledger is W-45's promotion
   evidence and its schema is not this lane's. ⬛ One-line update for whoever owns W-45 next.
4. **The evidence linter has no legal form for an ABSENCE** — a genuinely new finding, hit while
   writing this table. `knowledge/_validate_evidence.py` HARD-FAILS a row that names a path which
   does not exist, *including a row whose entire claim is that the path does not exist*. The row
   only lints once its subject is described in prose instead of named — i.e. the linter is
   satisfied by hiding the thing. That is [[honest-refusal-needs-a-legal-form]] inside the W-44
   instrument itself. ⬛ Priced TODO for W-44's owner: an `absent:` token shape that the linter
   verifies by checking the path is NOT there. Row W3-18.
5. **No store row was added for this receipt or its claim table.** Checked, not assumed:
   `grep -c "208-wave1\|208-wave2" knowledge/_state.json` → **0**, so waves 1 and 2 set the
   precedent and `python3 knowledge/_gate_doc_rows.py` is **rc=0** with `unrowed 0` (population
   21, receipts are outside its PICKED scope). ⬛ Left to the conductor rather than taken: the
   store is shared and a parallel lane may be writing it. If the #185 forgotten-document rule is
   meant to reach receipts, that is a scope widening for the gate, not a hand-edit here.
6. **P-3 remains UNPROVEN in this environment** — no playwright, so its actual detection was not
   re-driven this lane. The refusal is now honest about exactly that. `s204-D1` item 5 owns it.

---

## CONSEQUENCES AND PITFALLS (REPLAYED)

- ⛔ **[[no-gate-parses-the-artefact]]** — P-2 is the gate that parses these pages in the
  consumer's grammar; nothing else in the chain sees them. It stays the only witness that the
  repair holds, so **re-run it after any future edit to a review page**, not just after this one.
- ⛔ **[[green-tests-cannot-see-scope]]** — P-2 reporting 0 proves the ids resolve, NOT that any
  reference points at the RIGHT element (the probe's own `blind` field says so: presence only).
  A per-pane suffix could in principle point a pane at its own wrong element and P-2 would stay
  green. Countered here by the masked-identity proof plus the one-id-per-pane assertion, not by
  the green.
- ⛔ **[[mutation-tests-the-clause-not-the-feature]]** — both the fence check and the consumer's
  verdict bites were mutated until they went red, then restored. A check nobody has seen fail is
  a check nobody has seen.
- ⛔ **[[instrument-without-a-consumer]]** — the whole point of item 3's second half. A refusal
  code with an untaught consumer is a costume; the taught consumer is `_registry.verdict()`.
- ⛔ **[[premise-ages-faster-than-rule]]** — item 2's 204 was already 205, and the #207 brief's
  replacement figures had all moved. **Re-measure before quoting any of them.**
- ⛔ **[[gate-glob-scope-rule]]** — P-2 rules only over `reviews/REVIEW-*.html`. Duplicate ids in
  showroom pages, snippets or `outputs/` are invisible to it and were not looked at here.
- ⛔ **A green registry run proves the probes RAN, not that the tree is clean** — and with P-3
  refusing, one of the five did not even run. The COULD-NOT-ASK block exists so that fact cannot
  be read off as a pass.
- ⚠ **The review pages are still awaiting Dave's untriaged eye.** Nothing in this lane is a
  review verdict, a restyle, or a copy edit; the fence proof above is the receipt for that.
