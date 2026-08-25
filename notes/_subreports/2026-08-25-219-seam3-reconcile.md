# #219 seam 3 — reconcile: two concurrent lanes merged, lane 6's gate wired ADVISORY

**Sub:** Opus, #219 seam-3 reconcile. **Base:** `04655de` (clean). **Committed:** nothing — the tree is
prepared, the conductor commits.
**Brief:** `notes/_briefs/2026-08-25-219-crank-divvy.md` · lane reports
`notes/_subreports/2026-08-25-219-lane5-unconsumed-mints.md`, `…-lane6-gates-backlog.md`.

COUNTS: 11 tree paths reconciled · 0 UNCLAIMED · 0 dropped · 5/5 concurrent store rows intact · 1 row
minted (`W-180`, this report) · 1 mechanical addition (4 STEPS/ROUTE_ROWS lines + 2 comment blocks) ·
8 verdicts driven · regen serial SKIPPED-BY-DECLARATION · 4 items returned upward · subs 0

---

## 1 · The reconcile — every path, owned

Nine dirty paths at entry; two more added by this seat (`_CHAIN.md` at step 4, and this report).
**Nothing is unclaimed, nothing was
silently included or dropped.** The two lanes' own manifests partition the tree exactly — lane 5 claims
7 paths, lane 6 claims 3, they overlap on `_state.json` and `_graph-mark-observations.jsonl`, and the
union is the whole dirty set.

| path | status | owner | evidence the ownership is real |
|---|---|---|---|
| `knowledge/_build_all.py` | M | **lane 5 + THIS RECONCILE** | `git diff --stat` = 16 insertions at entry, all lane 5's two hunks (steps 100/101 + their ROUTE_ROWS). **Lane 6 did not touch it** — the diff carries no third hunk. My authorized addition sits on top, +18 more. |
| `knowledge/_graph-mark-observations.jsonl` | M | **BOTH (shared, append-only)** | `--numstat` = `47 0` — 47 added, **0 removed**, so no lane could have clobbered the other. Query split parsed from the JSON: 17 `memento-package verbatim set re-sync authorization` (**lane 6's** item-A probe) + 12 `tabs inactive token consumer` + 18 `color neutral raise elevation supercharge` (**lane 5's** two probes) = 47. **This matches lane 5's declaration of "30 mine, the other 17 another lane's" exactly.** |
| `knowledge/_state.json` | M | **BOTH** | +65/−0. Five ids added, no line removed — see §2. |
| `knowledge/_gate_minted_consumption.py` | ?? | lane 5 | inline provenance "built #219 lane 5"; lane 6 explicitly disclaims it |
| `knowledge/_validate_hidden_display.py` | ?? | lane 6 | lane 6 claims it; lane 5 explicitly flags it as "NOT MINE" |
| `notes/_subreports/2026-08-25-219-lane5-unconsumed-mints.md` | ?? | lane 5 | its own filed report |
| `notes/_subreports/2026-08-25-219-lane6-gates-backlog.md` | ?? | lane 6 | its own filed report; lane 5 flags it as not-mine |
| `notes/_subreports/assets/2026-08-25-219-lane5-unconsumed-mints/` | ?? | lane 5 | 3 files: `unconsumed-mints.png`, `verify.py`, `sweep.py` — the evidence dir its report names |
| `reviews/UNCONSUMED-MINTS-2026-08-25-v1.html` | ?? | lane 5 | the PROPOSED decision surface, rowed as `W-99zk` |
| `_CHAIN.md` | M | **THIS RECONCILE** | regenerated at step 4 — §5 |
| `notes/_subreports/2026-08-25-219-seam3-reconcile.md` | ?? | **THIS RECONCILE** | this report; rowed `W-180` (§5) |

**UNCLAIMED: 0.** Both lanes' cross-disclaimers agree with each other and with the diffs; there is no
path either lane failed to account for.

## 2 · The five concurrent store rows — 5/5 intact

Both lanes minted into `_state.json` at the same time. **All five survived; the concurrent writes did
not lose a row.** Verified by id, not by claim:

```
W-178   knowledge/_validate_hidden_display.py                        (lane 6, owner claude)
W-179   notes/_subreports/…-lane6-gates-backlog.md                   (lane 6, owner dave)
W-99zj  knowledge/_gate_minted_consumption.py                        (lane 5, owner dave)
W-99zk  reviews/UNCONSUMED-MINTS-2026-08-25-v1.html                  (lane 5, owner dave)
W-99zl  notes/_subreports/…-lane5-unconsumed-mints.md                (lane 5, owner dave)
```

`git diff --numstat -- knowledge/_state.json` = **`65 0`** — sixty-five lines added, **zero removed**.
A concurrent write that clobbered a rival row would show a deletion. There is none.

**Verdicts, quoted:**

```
python3 knowledge/_state.py --selftest
  _state selftest: 57 bites, all GREEN                                             rc=0

python3 knowledge/_gate_doc_rows.py
  doc-row gate: population 77 · of which staged-in-THIS-commit 0 · unrowed 0
  ✅ PASS — every in-scope document has a store row.                                rc=0
```

⚠ **The plain doc-row PASS is not yet evidence for these files** — lane 5 named this correctly: the
`staged-in-THIS-commit 0` leg is the #207 single-commit blindspot, and untracked files are invisible to
it. **So I drove the staged arm** rather than accept a green that could not see the subject
[[instrument-without-a-consumer]]. Staged into a **throwaway index** (`GIT_INDEX_FILE=/var/tmp/…`) so
the conductor's real index is untouched — confirmed by a `git status --porcelain` read-back afterwards,
which still shows the same six `??` entries:

```
staged adds seen: _gate_minted_consumption.py · _validate_hidden_display.py ·
                  both lane subreports · the 3 asset files · UNCONSUMED-MINTS-…-v1.html
doc-row gate: population 79 · of which staged-in-THIS-commit 5 · unrowed 0
✅ PASS — every in-scope document has a store row.                                  rc=0
```

**That is the real green:** population rises 77 → 79, the gate SEES 5 of the new documents, and
**unrowed is still 0.** Lane 5's blindspot caveat is now discharged.

Re-driven once more at exit, with this report and its `W-180` row also in the tree — **population 80,
staged-in-THIS-commit 6, unrowed 0, PASS** — and the real index verified still carrying nothing
(`git diff --cached --name-only` = 0 lines). **The conductor's index is untouched; only the throwaway
one ever saw a `git add`.**

## 3 · The one mechanical addition — lane 6's gate wired ADVISORY

Conductor-authorized, and it is the consistency lane 6 asked for in its own pitfalls section: two
near-identical advisory instruments landed in one crank, one wired and one not, and *"a later session
will read [that] as a judgment about the unwired one."*

`knowledge/_validate_hidden_display.py` is now wired into `_build_all.py` **exactly matching lane 5's
shape** for `_gate_minted_consumption.py` — a run step + a selftest step in `STEPS`, mirrored in
`ROUTE_ROWS` as **ADVISORY** and **ABORT** respectively, each carrying a comment block stating why the
posture is what it is. Placed immediately after lane 5's pair, so the four advisory class-checks sit
together. Its CLI shape is the same as its sibling's: `--selftest` supported, `main()` ends
`sys.exit(0)  # advisory: never blocks`.

**ADVISORY ONLY. No blocking wiring, no promotion.** Promotion is Dave's word (ADR-0005 §5), and both
lanes' comments say so in the file.

⚠ **One deliberate deviation from lane 6's prose, and why.** The step title says **`hidden-attr vs
author-display`**, not `[hidden]-vs-author-display`. The build banner prints
`=== [{i}/{len(STEPS)}] {label} — {rel} ===` (`_build_all.py:1206`), so a literal `[hidden]` in the
label puts a **second bracket pair on the banner line** — and CI reds are cited by bracketed step id
throughout both lane reports (`[120]`, `[18]`, `[40]`). Probed before choosing:
**no existing step title in `STEPS` contains a square bracket.** Keeping that property intact costs one
word; the literal `[hidden]{display:none}` form is carried in the comment block, where nothing parses
it [[banner-brackets-are-ages]].

**Verdict, quoted:**

```
python3 knowledge/_build_all.py --selftest
  selftest PASS — exact-ID failure routing over 132 steps; unknown never defaulted (#77)   rc=0
```

**130 → 132.** Both new rows resolve, no stale rows, no misroute (the #77 class — my titles carry
neither "surface" nor any other branch-matching word).

## 4 · The gates driven, and the serial NOT run

Both new instruments' selftests, driven individually per the sandbox call-boundary rule:

```
python3 knowledge/_validate_hidden_display.py --selftest
  ✅ _validate_hidden_display selftest: all bites pass          (16 bites)          rc=0

python3 knowledge/_gate_minted_consumption.py --selftest
  ✅ selftest PASS — the inventory can flag, can stop flagging, and both
     false-positive subtractions are mutation-proved (10 bites)                     rc=0
     [1] green control … declared=973 consumed=600 orphan=265
```

The hidden-display mutant arm re-named the real #218 instance as designed —
`Command-palette.reference.html: STATIC hidden-bearing <div> (class=cp-opt) at line 230 …`. **Minor
drift, non-material:** it reports the painting rule at **line 93**; lane 6's report quotes **line 92**.
`Command-palette.reference.html` is not in the dirty set and was not edited by anyone, so this is an
off-by-one between the report's prose and the live mutant output, not a moved file. The element line
(230) and the class agree exactly. Named so nobody reads it as a changed artefact.

```
python3 knowledge/_state.py --selftest        → 57 bites, all GREEN                 rc=0
python3 knowledge/_gate_doc_rows.py           → PASS, unrowed 0 (staged arm: 5 seen) rc=0
python3 knowledge/_validate_help_gate.py      → 7 reds, NONE from this crank        rc=1
```

**The help-gate red is pre-existing and is not this crank's** — all 7 are `#218` render-proofs
(`_render/verify_behaviour_218w3_{media,nav,overlay}`, `verify_phantom_surfaces_218`,
`verify_wave3_{alpha,beta,gamma}_218`). Probed both ways: `grep -c` for either new instrument in the
gate's output = **0**, and `grep -l "_helpgate"` names **both** new files. Lane 5 declared this and it
still holds after my wiring [[a-crash-is-not-a-fail]].

### ⛔ The ordered regen serial was NOT run — declared, with the probe

**No source feeding the serial changed.** This is a probe, not an assumption:

```
git status --porcelain -- knowledge/canon/ knowledge/snippets/ knowledge/tokens/ knowledge/*.css
  → EMPTY
git status --porcelain -- notes/_briefs/ notes/_dream/ notes/_MEMENTO-DECISIONS.md \
                          notes/_GAUGE-LOG.md knowledge/components/ knowledge/_RUNBOOK-*.md
  → EMPTY
```

The whole crank's output is **two instruments, one runner wiring, an append-only observation log, five
store rows, a review page and two reports.** No token store, no canon CSS, no snippet, no component
meta. `gen_theme_cascade` / `gen_canon_tokens` / `gen_snippet_tokens` / the ramp have nothing to
re-emit — lane 5 reached the same conclusion for its own half ("Nothing was regenerated… the regen
serial set was correctly not entered") and it holds for the merged tree.

**The memento index is included in that skip, and I checked it specifically** rather than assuming,
because two new documents landed. `_build_memento_index.py`'s corpus is `notes/_GAUGE-LOG.md`,
`notes/_MEMENTO-DECISIONS.md`, `notes/_briefs/*.md`, `notes/_dream/*.md`, the RUNBOOK set and
`knowledge/components/*.meta.json` — **`notes/_subreports/` is not in it.** The `#219` brief is already
committed (`d178313`). So the index corpus is byte-unchanged and the index is not stale.
**Serial skipped, by declaration, on that evidence.**

## 5 · `_gen_chain.py` — was stale, regenerated, included

```
python3 knowledge/_gen_chain.py --check
  ✗ _CHAIN.md is STALE — it does not match GOOD-MORNING.md / _LIVE-STATE.md as they
    now stand …                                                                     rc=1
```

Regenerated. **The diff is entirely generated figures moving, and I read every hunk before accepting
it** — nothing was reworded, no Dave row closed:

- **worklist counts:** `233 → 239` items · `154 → 160` live · Dave's `80 → 84` · mine `74 → 76` ·
  conditioned `219 → 225`. That is **exactly +6**: the five rows of §2 arriving in the chain (+4
  Dave-owned — `W-179`, `W-99zj/zk/zl`; +1 mine — `W-178`), **plus `W-180`, the row for THIS report.**
  I minted `W-180` before the final regenerate, because `notes/_subreports/*.md` **is** in the doc-row
  gate's population (§2 proved it: the gate saw both lane reports once staged), so an unrowed reconcile
  report would have turned `_gate_doc_rows` red in the conductor's own commit — the
  [[forgotten-document-class]] rule, #185. **Order mattered:** row first, chain second, or the chain
  ships one row short. It is `owner: claude`, rules nothing and closes nothing. **If the conductor
  would rather mint it themselves (s218-D7 reads the conductor as the minter), drop `W-180` and
  re-run `python3 knowledge/_gen_chain.py` — those two motions, in that order.**
- **build verdict:** `75 of 128 steps` → `75 of 132 steps`, `53` → `57` never-green. **Generated from
  `_build_all.py`'s AST at both ends** (`s125-D1`), so this is lane 5's +2 and my +2 being counted, not
  a typed number.
- the six new rows render into their owners' lists; file size `42,061 → 42,781` real and the paid-for
  fraction `47% → 48%`, both fixed-point outputs.

```
python3 knowledge/_gen_chain.py --check
  ✅ _CHAIN.md is FRESH — byte-matches the live chain · FILE 42,781 real
     = slice 29,974 + wrapper 12,807 · fixed point in 2 pass(es)                     rc=0
```

`GOOD-MORNING.md` and `_LIVE-STATE.md` were **read** by the generator and **not written** — confirmed
in §6.

## 6 · DO-NOT-TOUCH — verified by probe, not by claim

```
git status --porcelain -- knowledge/_rulings.json GOOD-MORNING.md _LIVE-STATE.md \
                          knowledge/_gauge_tokens.py
  → EMPTY
```

No ruling written, no constant/band/advisory/threshold/stop-line moved, no Dave-owned row closed or
reworded, no gate promoted, no memory write, no lane repoint.

### RETURNED, not fixed: the `s149-D1` stale status field

Lane 5's finding 7. **Left exactly as found — this is Dave's**, and `_rulings.json` is DO-NOT-TOUCH for
this seat too. Quoted verbatim from the store so the conductor need not re-derive it:

> `s149-D1` · `status`: *"RULED #149, **NOT ENACTED**. No value moved in any token or canon file.
> Enactment is #150 lane 1, priced: token amendments (mono banner + badge legs) + canon consumption
> (wash medium, mark inks, `.ovcount` re-point) + re-drive of `_validate_state_contrast.py` to restate
> the 20-fail headline."*

Lane 5 measured the `.ovcount` re-point **live** at `canon.css:2896` and `Tabs.reference.html:105-107`
with the `s149-D1` comment attached. So the record's own status field contradicts the artefact — the
[[conclusions-are-debt-s129-d5]] class, in the ruling store itself. **A correction is a
`_rulings.json` write and therefore Dave's.**

## 7 · What the conductor still owes upward

Neither lane's ruling-shaped work is discharged by this reconcile — it is only merged and made
commit-safe.

- **Lane 5's five questions** + `REPLAY-THESE`: `reviews/UNCONSUMED-MINTS-2026-08-25-v1.html` —
  **open it, do not read it** (Rows A and B are Dave's eye).
- **Lane 6's Q1** (memento-package mirror: `s114-D7` live-mirror vs `s193-D1`(b) authorized-once — two
  of Dave's own rulings pointing opposite ways, CI red `[120]` sitting between them), **Q2** (how a
  session that wrapped TWICE testifies — CI red `[18]`; touches `GOOD-MORNING.md`, which no lane may
  edit), **Q3** (the three CERTAIN `dv-empty-frame` findings + promotion).
- **The `s149-D1` status field**, above.
- ⚠ **Both CI reds `[120]` and `[18]` will still be red after this commit.** Lane 6 named this as a
  pitfall and it is worth carrying into the push read-back: their persistence is **not** a failure of
  either lane, and not a regression from this seam. Both remedies are ruling-shaped.

## 8 · UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN: `_build_all.py` end-to-end.** Unchanged from lane 5's declaration and now covering four
  advisory steps rather than two. The new steps were driven **individually** (rc 0 each) and the
  routing table proved over **132** steps, but they have **not** been observed executing inside the
  runner loop — `--range` refuses a pass that does not start at step 1, and a full single-process run
  does not fit a sandbox call. **CI delivers that verdict on push.**
- **UNPROVEN: that the wired advisory step stays advisory under a real build's error paths.** The route
  row says ADVISORY and the script ends `sys.exit(0)`, both read; no build has exercised the pair
  together.
- **CLAIMED (declared, not re-derived): both lanes' findings.** I verified their **manifests, diffs,
  store rows and verdicts** — not their research. Lane 5's 6-orphan disposition and lane 6's 3 CERTAIN
  corpus findings are taken as filed.
- **NON-REPO, declared per s191-D2:** the throwaway index `/var/tmp/probe_index_219` and
  `/var/tmp/hg.txt` (help-gate capture). Both are scratch; neither is an instrument, and the real
  index was verified untouched afterwards.

---

**Tree state at exit:** 11 paths dirty, 0 unclaimed, nothing staged, nothing committed, nothing pushed.
The conductor commits.
