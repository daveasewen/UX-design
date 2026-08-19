# W-45 — verifier probe registry + promotion rule: BUILT and DRIVEN (#206)

*Opus build-PM lane, brief `notes/_briefs/2026-08-19-206-w45-buildpm-brief.md`, ruled scope
`notes/_briefs/2026-08-19-204-mechanisation-programme-v1.md` § Item 2 (`s204-D1`).
**Nothing in this receipt is a ruling.** Promotion of any probe to a `_build_all.py` gate is
Dave's under derivation governance; the three live findings below are REPORTED, NOT REPAIRED —
every one of them sits outside this lane's owned regions. Claim table (joinable form):
`notes/_claims/206-w45-claims.jsonl`, 20 rows, `_validate_evidence.py` rc=0.*

## A · What was built

`knowledge/_probe_registry/` — a directory, a manifest, five probes, a runner, a promotion tool
and a README that carries the ready-to-paste verifier-brief paragraph.

| file | role |
|---|---|
| `manifest.jsonl` | the registry: class · script · environment · **blind spots** · `caught` ledger |
| `_registry.py` | manifest schema + LOUD loader (unknown key = parse failure) + runner |
| `_promote.py` | the twice-caught rule as code; emits candidature text, **writes nothing** |
| `probe_meta_schema.py` | P-1 · metas vs `meta.schema.json` (#204 C-8) |
| `probe_dup_ids.py` | P-2 · duplicate `id` + unresolved IDREF (#204 NEW-1) |
| `probe_dangling_var_pixel.py` | P-3 · dangling var → silent black, **from pixels** (#184 `s184-D3`) |
| `probe_premise_store.py` | P-4 · premise-vs-store diff (#203 lane H, #204 G-c) |
| `probe_stale_figure.py` | P-5 · carried figure vs live measurement (#173, #203) |

## B · Selftests — plant-then-detect, both directions, DRIVEN on real artefacts

```
python3 knowledge/_probe_registry/_registry.py --selftests
SELFTEST rc TABLE
  P-1    rc=0    probe_meta_schema.py
  P-2    rc=0    probe_dup_ids.py
  P-3    rc=0    probe_dangling_var_pixel.py
  P-4    rc=0    probe_premise_store.py
  P-5    rc=0    probe_stale_figure.py
```
Plus `_registry.py --selftest` rc=0 (11 manifest plant arms + duplicate-id + removal-green +
live-manifest) and `_promote.py --selftest` rc=0.

**Every arm DRIVES the probe on a planted artefact** — a real meta (`stateModel: "interactive"`
+ a non-`$` annotation key, the #204 C-8 shapes), a real review page (a duplicated real id + a
dangling `aria-labelledby`), a real chart snippet (a real `fill="var(--x)"` renamed to a
nonexistent property), a real brief against the real store, a real living document with a
figure four off the live measurement. **No arm asserts on a probe's clause**
([[mutation-tests-the-clause-not-the-feature]] — that is the #104 failure this lane was told to
avoid, and avoiding it is why the selftests cost more than the probes).

Controls that exist because a green without them proves nothing:
- **P-2 tier control** — a planted `href="#missing"` must be REPORTED as WARN and must NOT
  become a finding, so #204's declared placeholder-link residual is never re-litigated.
- **P-3 fallback control** — `var(--nonexistent, #DA1A00)` must NOT fire. That is the #204
  verifier's own false positive, rebuilt as a fence.
- **P-3 pixel control** — the same page unplanted must report zero black suspects, so the black
  reading is attributable to the plant.
- **P-4 controls** — a `closes_when` line quoting "CLOSED" must not read as a state assertion;
  a pre-`BASELINE_DATE` brief must stay exempt (the frozen legacy set `_gate_doc_rows.py` uses).
- **P-5 precision control** — the six false positives this probe produced on its FIRST real
  drive (delta prose in `GOOD-MORNING.md`) are now a control arm.

## C · The real-tree drive — what the registry actually found

```
python3 knowledge/_probe_registry/_registry.py --run          → rc=1
REGISTRY RUN SUMMARY (5 probe(s))
id     env             rc    findings  class
P-1    sandbox         0     0         meta vs meta.schema.json drift
P-2    sandbox         1     46        duplicate id + unresolved IDREF in review pages
P-3    sandbox-render  0     0         dangling var renders silent black (dataviz)
P-4    sandbox         1     2         premise vs store disagreement (stale carried state)
P-5    sandbox         1     1         stale carried figure vs live measurement
```

### ⛔ P-2 — 46 findings, 7 files: the #204 duplicate-id class SURVIVED on the #203-era pages
10 DUPLICATE-ID · 36 UNRESOLVED-IDREF, over 45 `reviews/REVIEW-*.html`:

| file | findings |
|---|---|
| `reviews/REVIEW-203-date-range-picker-four-themes-v1.html` | 18 |
| `reviews/REVIEW-203-date-picker-four-themes-v1.html` | 9 |
| `reviews/REVIEW-203-time-picker-four-themes-v1.html` | 9 |
| `reviews/REVIEW-174-progress-bar-four-themes-v1.html` | 3 |
| `reviews/REVIEW-203-kpi-tile-four-themes-v1.html` | 3 (`kpi-down`/`kpi-table`/`kpi-up`, 8× each) |
| `reviews/REVIEW-203-timeline-four-themes-v1.html` | 3 (`tl1-h`/`tl2-h`/`tl3-h`, 8× each) |
| `reviews/REVIEW-203-avatar-group-four-themes-v1.html` | 1 |

The #204 repair fixed the **six #204 pages**. The identical defect — one id set repeated across
eight theme panes, `aria-labelledby` resolving to the first pane — is still live on seven
earlier pages, and `aria-describedby="f-time-help"` in the time-picker page resolves to **no id
at all**, 8×. ⛔ **Not repaired here:** `reviews/` is outside this lane's owned regions.

### ⛔ P-5 — 1 finding: `knowledge/README.md:13` carries `(38 metas)`; live count is **92**
The #173 stale-inventory shape, still on disk, in a LIVING document. Not repaired (outside
owned regions).

### ⛔ P-4 — 2 findings, one of which is this lane's own brief
`notes/_briefs/2026-08-19-206-w45-buildpm-brief.md` has **no store row**. `_gate_doc_rows.py`
reports `population 16 · unrowed 0` **because the brief is untracked** — the gate's rc=0 is
VACUOUS, exactly the #204 G-c finding, one wave later. It will flip rc=1 the moment the brief is
`git add`ed. The second is `notes/_briefs/2026-08-16-memento-closeout-plan.md`.
⛔ Not repaired: the brief is the conductor's document. **The repair is one `_state.add()` row
before the brief is committed.**

### ✅ P-1 — 0 findings (92 metas checked; `EXAMPLE-button.meta.json` printed as a DECLARED exemption)
### ✅ P-3 — 0 findings across 14 chart snippets, **14 positive controls sampled, 0 unsampled**
A green here is only worth something because the control leg proves the sampler was alive on
every page. Measured, not assumed.

### One more measurement, offered rather than acted on
`knowledge/snippets/DataViz-interactive.html` **does not exist**, yet `_gate_dataviz_vars.py`
names it in its declared GLOB. An unmatched pattern in a live gate's scope
([[unmatched-grep-is-not-an-absence]]). Outside owned regions; reported.

## D · The ledger and the promotion rule

```
python3 knowledge/_probe_registry/_promote.py                 → rc=0
TWICE-CAUGHT ASSESSMENT (threshold=2 distinct session(s), EXACT kind only)
id    candidate sessions         class                                      basis
P-1   no        204              meta vs meta.schema.json drift             HISTORICAL-ONLY
P-2   YES       204,206          duplicate id + unresolved IDREF in review  MIXED
P-3   no        184              dangling var renders silent black (dataviz HISTORICAL-ONLY
P-4   YES       203,204,206      premise vs store disagreement (stale carri MIXED
P-5   YES       173,203,206      stale carried figure vs live measurement   MIXED
```

**Seed provenance, stated plainly.** Every seeded entry is `historical-mined` — the class was
caught by a person or an agent BEFORE the probe existed, and this lane mined the receipt. The
only `live-run` entries are the three catches above, from this drive. Both count toward "twice",
because the ruled evidence IS the ledger — but every candidature prints its **basis**
(`HISTORICAL-ONLY` / `MIXED` / `LIVE`), so a retrospective pair can never travel as two live
catches. One session that caught a class three times (#203 caught the 1,101 figure in lanes C, E
and F) counts **once**: the rule is about independent occasions.

**Two probes are deliberately NOT candidates**, and that is a finding rather than a gap:
- **P-1** — the #204 catch and the #204 repair are the same occasion.
- **P-3** — its only `exact` evidence is #184. The #204 lane-P entry is `kind: species` (a
  `--x: var(--x)` CYCLE, not an absent declaration) **and** the #204 verifier CONTRADICTED it as
  a shipped defect (zero occurrences on disk). Counting it strictly would have manufactured a
  candidate out of a contradicted receipt.

The three candidature blocks are on stdout, ready to paste. ⛔ **`_DS-IMPROVEMENTS.md` was NOT
written** — proven by an mtime arm inside `_promote.py --selftest`. Promotion is Dave's.

## E · Schema choices — PROPOSED, not ruled (with the alternatives rejected)

1. **`caught` is a LIST INSIDE the probe row**, not a separate ledger file.
   *Rejected:* a `caught.jsonl` joined on probe id — a second file to keep in step, and W-44's
   whole lesson is that two documents needing a human join is the defect.
2. **`provenance: historical-mined | live-run`** on each entry.
   *Rejected:* omitting it (the brief's priced consequence — a mined receipt would read as a
   live catch); *also rejected:* excluding mined entries from the count, which would have made
   the ruled seeding pointless.
3. **`kind: exact | species`**, EXACT-only by default, `--include-species` widens and says so.
   *Rejected:* one flat class list (species creep silently inflates the count); *also rejected:*
   dropping species entries (the #204 lane-P cycle is real knowledge and belongs in the ledger).
4. **`environment: sandbox | sandbox-render | unknown`**, and `unknown` is never defaulted.
   *Rejected:* a boolean `needs_browser` — it cannot express "we have not established this".
5. **`blind` is REQUIRED**, not optional prose.
   *Rejected:* leaving blind spots to the docstring, where the runner cannot print them and a
   candidature cannot carry them.
6. **Free-text `note` on both the probe row and each ledger entry** (the schema-too-tight price).
7. **`klass` not `class`** — a JSON key named `class` reads as a Python keyword at every call
   site. Cosmetic, recorded because it is the kind of choice that gets silently "corrected".

## F · The priced gaps this lane knows about and did NOT fix

- **P-5's precision fence is a heuristic, not a parser.** `HISTORY_MARKERS` + `TOTALISING_RE`
  keep delta prose out; a carried total phrased outside those shapes is invisible. Closing it
  properly means parsing the sentence, which is a different instrument.
- **P-5 cannot reach where the 1,101 actually lived** — a MEMORY HOOK, outside the repo. The
  probe closes the repo-document half of the class and says so.
- **P-3 is UNPROVEN IN CI** (#173). It ran in the sandbox reusing a foreign session's Chromium
  at `/var/tmp/pw-browsers-s197`. `s204-D1` item 5 owns the CI pixel leg.
- **P-3's pixel leg is corroboration, not the detector.** 17 of 61 planted elements carried no
  exact-`rgb(0,0,0)` pixel (small antialiased glyphs). The cascade leg names them all.
- **P-2's glob is `reviews/REVIEW-*.html` only.** Showroom and snippet surfaces are unscanned.
- **P-1 depends on `jsonschema`** being importable; absent, it REFUSES by name (rc=1), never
  passes.
- **`_validate_evidence.py` refuses three of five sampled rows** as SIDE-EFFECTS because their
  head verb is a bare `python3 knowledge/…`. `_registry.py --run`, `_promote.py` and the probes
  write nothing (the mtime arm proves one of them). The linter's heuristic is right in general
  and wrong here — a note for the W-44 owner, not a change this lane may make.

## G · Consequences, replayed (Dave #165)

- **Registry probes rot like all instruments.** The selftests are the fence, and every arm
  drives the probe on a planted artefact rather than asserting its clause.
- **A manifest schema too tight forces prose into chat** — `note` is free text at both levels.
- **Seeded entries are HISTORICAL evidence, not fresh catches** — provenance is carried into
  every candidature's basis line.
- **A green registry run proves the probes ran, not that the tree is clean.** The runner prints
  that sentence every run, every probe publishes a `blind` field, and the verifier-brief
  paragraph in `README.md` keeps free hunting explicitly mandatory.
- **A registry the verifier trusts too much narrows the hunt** — which is why the brief text
  says the registry *cannot by construction* find a class nobody has found yet.
