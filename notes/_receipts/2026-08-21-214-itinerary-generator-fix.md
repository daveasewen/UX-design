# Receipt — #214: `gen_itinerary_status.py` Layer-2 defect FIXED (v2 → v3)

> Hand-run, not `gen_brief.py`-minted. Session #214 (Opus build sub under the conductor).
> Nothing here is a ruling. `reviews/ITINERARY-STATUS-2026-08-19-v1.*` and
> `reviews/ITINERARY-STATUS-2026-08-21-v2.*` are UNTOUCHED (write-once, ADR-0017 / `s192-D1`);
> this run writes a NEW dated pair beside them: `reviews/ITINERARY-STATUS-2026-08-21-v3.json` +
> `.html`. Files edited: `knowledge/gen_itinerary_status.py` and this receipt. Nothing else.

## 1 · The defect

Named in `notes/_receipts/2026-08-21-213-laneI-itinerary-v2.md`, and re-verified against today's
tree before building on it (`[[premise-ages-faster-than-rule]]` — the receipt's own premise gets
the same treatment it gave the itinerary).

`resolve()` carried:

```python
    if str(row["layer"]).strip().startswith("2"):
        return [], "layer-2", {"class": "layer-2", "why": LAYER2_NOTE}
```

…and `LAYER2_NOTE` asserted, in hand-typed prose written at #203:

> "No artefact class for these exists in the store yet — not a snippet, not a meta, not a
> showroom page."

Every Layer-2 row (97–124, 28 rows) therefore short-circuited to `NO-ARTEFACT-CLASS` **without a
single probe**. `_with_drift()` compounded it with a second hand-carried clause —
`elif rec["class"] == "layer-2": drift = "AGREES" if itinerary_status == "Gap" else "REVIEW"` —
so the class could only ever agree with the frozen column.

**The premise is measurably false.** Re-listed today, first-hand, not taken from the #213 receipt:

```
$ ls knowledge/snippets/ | grep -iE 'shell|template|lockup'   → 25 files
   App-shell-{top-nav,side-nav,multi-column,split,focused,doormat,nav-rail}.reference.html   (7)
   {CTA,Card-header,Feature-grid,Footer-doormat,Page-header,Section-heading,Stats-band}-lockup… (7)
   Template-{dashboard,list-index,detail,create-edit,settings,wizard,empty,error,auth,report,
             confirmation}.reference.html                                                     (11)
$ ls knowledge/snippets/ | grep -iE 'hero|filter|toolbar'
   Hero-variants.reference.html · Filter-toolbar-bar.reference.html   (the other 2 Layer-2 rows)
```

27 Layer-2 artefacts, each with a matching `knowledge/components/<slug>.meta.json` and a matching
`showroom/<slug>.html` (both directory listings run and quoted above). ⚠ The #213 receipt says
"20 … snippets"; the correct count is **25** for shell/template/lock-up and **27** including
`hero-variants` + `filter-toolbar-bar`. Its arithmetic was low; its finding was right.

Consequence, exactly as #213 described it: no per-row Layer-2 status could ever move, and the
whole class leaked out as `$orphan_snippets` growing 1 → 28. A hand-carried premise living inside
the instrument built to catch hand-carried premises.

## 2 · The fix shape

**(a) Probe, don't presume.** Layer-2 rows now take the SAME five probes as every other row
(snippet · meta · showroom · radius-ratchet membership · `.cn-` canon rule count). Resolution is a
new MECHANICAL ladder, `resolve_layer2()`, whose rung is recorded per row as `basis`. No mapping
was hand-invented; `ROW_MAP` gained **zero** new entries.

| rung | rule | example |
|---|---|---|
| `layer-2-family` | family pattern (`app-shell-{d}` · `template-{d}` · `{d}-lockup`) + slugified descriptor HITS the store | `Template — settings` → `template-settings` |
| `layer-2-direct` | the full slugified descriptor is itself a **snippet** name (snippet-only: a bare word like `error` or `page` can collide with a canon-only `.cn-` scope, and a canon hit is not an artefact) | `Lock-up — hero variants` → `hero-variants` |
| `layer-2-tokens` | exactly ONE member of the row's family has a distinctive-token set that is a subset of the descriptor's, naive-singularised | `App shell — top / stacked nav` → `app-shell-top-nav` |
| `layer-2-ambiguous` | more than one member qualifies → **UNRESOLVED**. Never guesses. | — |
| `layer-2-absent` | nothing answers → fuzzy scan; plausible alias → UNRESOLVED, else GAP | row 124 → GAP |

`_l2_tokens()` deliberately does NOT apply `STOPWORDS`: `card` and `row` are stopwords for Layer-1
fuzzy matching but load-bearing in a lock-up name — filtering them makes `card-header` a subset of
every other `*-header` row and manufactures a false ambiguity.

The `_with_drift()` layer-2 special-case was deleted: those rows now take the ordinary rank
comparison, so their drift is visible instead of hard-coded to AGREES.

**(b) Regenerate the premise, don't patch it.** `LAYER2_NOTE` (the dead sentence) is **gone**.
In its place `layer2_note(records)` DERIVES the statement from what was just measured, and it is
emitted into the JSON (`$layer2_note`), the HTML (new section 5b + section 6) and stdout. This
run's generated text, verbatim:

> Layer 2 (shells · templates · lock-ups · variant matrices), MEASURED 2026-08-21: 28 rows, 27
> resolved to a store artefact by the mechanical Layer-2 ladder and probed like any other row
> (GAP 1, GATED 27); 1 GAP (row 124); 0 UNRESOLVED (none). Every verdict here is five probes deep
> — snippet · meta · showroom · radius ratchet · canon .cn- rules — not a class assertion.

New JSON keys: `$layer2_note`, `$layer2_rows` (per-row derived/basis/slug), `$measured`,
`$prior_snapshot`. `$session` is now the `SESSION` constant, not a literal `"#203 Wave 3b Lane H"`.

**(c) `STAMP` bumped** `2026-08-19-v1` → `2026-08-21-v3`, so the generator's own output path writes
the new dated pair and cannot overwrite a frozen snapshot. Nothing in the repo imports or invokes
this generator (`grep -rln gen_itinerary_status` → docs, receipts and itself only), so the bump
breaks no consumer.

## 3 · Selftest — repaired, and proved able to go RED

**Arm 2 repaired per the selftest's own doctrine.** It named six live fixture rows
(6, 7, 25, 26, 61, 93) expected to measure GAP; all six had become GATED, i.e. the fixtures moved
under the test — exactly what the arm's own comment warned would happen. Re-typing a fresh fixture
list only restarts that clock, so the arm is now **derived**: it hides a mapped row's artefact from
a scratch copy of the index (`_hidden()`) and requires GAP, whatever the live tree holds. Row 86's
ASSET-ONLY split verdict stays as the one live fixture — it is a structural fact about the logo
assets, not a build state.

**New arm 6, five sub-arms, each individually red-able:** 6a probes fire on a Layer-2 row and the
row carries its five probes · 6b store mutation (hide `template-dashboard`) collapses the routed
verdict · 6c clause mutation (`LAYER2_FAMILIES` emptied) proves the mapping is load-bearing ·
6d ambiguity refusal (plant `template-step` so row 109 has two equally-good family members) ·
6e the Layer-2 GAP path is reachable via a synthetic unanswerable row.

⚠ 6b asserts "no longer routed" rather than pinning GAP: with `template-dashboard` hidden, the
fuzzy rung still sees the rest of the `template-*` family as plausible aliases and returns
UNRESOLVED. That refusal is the instrument working; the arm tests the clause it owns.

### Transcript (verbatim, actually run)

```
$ python3 knowledge/gen_itinerary_status.py --selftest
SELFTEST OK — 6 arms: pass(6 rows) · fail(row 86 + derived gap mutation) · mutation-store · mutation-clause · fail-loud · layer-2(probe · store-mutation · mapping-mutation · ambiguity-refusal · gap-reachable)
rc=0

=== COLD RE-RUN ===
$ python3 knowledge/gen_itinerary_status.py --selftest
SELFTEST OK — 6 arms: pass(6 rows) · fail(row 86 + derived gap mutation) · mutation-store · mutation-clause · fail-loud · layer-2(probe · store-mutation · mapping-mutation · ambiguity-refusal · gap-reachable)
rc=0
```

### Zombie check — the new arms DRIVEN red (`/tmp/zz/red.py`, out-of-repo, imports the real module and calls the real `selftest()`)

```
=== RED-PROOF 1: restore the #214 Layer-2 shortcut (no probing) ===
SELFTEST FAIL — arm6a row 104 expected slug template-dashboard, got []
SELFTEST FAIL — arm6a row 104 expected GATED/BUILT, got GAP
SELFTEST FAIL — arm6a row 104 did not carry the five per-slug probes
SELFTEST FAIL — arm6b mutation: row 104 with template-dashboard hidden from all four indexes still reported GAP — the Layer-2 verdict is not measured
SELFTEST FAIL — arm6e: an unanswerable Layer-2 row expected GAP/layer-2-absent, got GAP/layer-2 — the Layer-2 gap path is unreachable
SELFTEST FAIL — arm6d refusal: row 109 with two equally-good family members (template-wizard, template-step) expected UNRESOLVED, got GAP — the instrument guessed
selftest rc = 1

=== RED-PROOF 2: drop the ambiguity REFUSAL (pick the first match) ===
SELFTEST FAIL — arm6d refusal: row 109 with two equally-good family members (template-wizard, template-step) expected UNRESOLVED, got PARTIAL — the instrument guessed
selftest rc = 1
```

Red-proof 1 reinstates the exact removed shortcut and the arms catch it. The test is not a zombie
[[mutation-tests-the-clause-not-the-feature]].

## 4 · v2 → v3 delta

```
$ python3 knowledge/gen_itinerary_status.py
wrote reviews/ITINERARY-STATUS-2026-08-21-v3.html (92555 B)
wrote reviews/ITINERARY-STATUS-2026-08-21-v3.json (195677 B)
rows 124 | GATED 121 | BUILT 0 | PARTIAL 0 | GAP 1 | ASSET-ONLY 1 | layer-2 rows 28
drift: {"AGREES": 40, "STALE — itinerary UNDERSTATES the store": 84}
TRUE gaps (Layer 1): 86
ORPHAN snippets (no itinerary row): meter
rc=0

$ python3 knowledge/gen_itinerary_status.py --check
ITINERARY-STATUS --check OK (124 rows)
rc=0
```

| measure | v2 | v3 | note |
|---|---|---|---|
| `$counts` GATED | 94 | **121** | +27 — the Layer-2 class, now measured |
| `$counts` NO-ARTEFACT-CLASS | 28 | **0** | the verdict class is gone; it only ever meant "not probed" |
| `$counts` GAP | 0 | **1** | row 124, honestly measured |
| `$counts` ASSET-SYSTEM / ASSET-ONLY | 1 / 1 | 1 / 1 | unchanged |
| `$orphan_snippets` | **28** | **1** (`meter`) | the entire finding of #213, closed |
| `$drift_counts` AGREES | 67 | **40** | −27 |
| `$drift_counts` STALE-understates | 57 | **84** | +27 — the frozen column calls 27 built Layer-2 rows "Gap" |
| `$true_gaps` | `[86]` | `[86]` | unchanged (Layer-1 scoped) |
| `$unresolved` | `[]` | `[]` | no row required a guess |
| `$radius_ratchet_advisory` | 26 | **53** | +27 — see finding below |
| rows whose `derived` moved | — | **28** | **all 28 are rows 97–124. Layer-1 movers: ZERO.** |

Per-row Layer-2 outcome (all 27 resolved rows measured **GATED** — snippet + meta + showroom +
canon `.cn-` scope all present):

| rows | basis | resolved to |
|---|---|---|
| 98, 99, 100, 101, 103, 104, 105, 106, 108, 110, 111, 112, 113, 114, 119, 121, 122, 123 | `layer-2-family` | the family-patterned slug |
| 97, 102, 107, 109, 115, 116, 117 | `layer-2-tokens` | `app-shell-top-nav`, `app-shell-doormat`, `template-create-edit`, `template-wizard`, `page-header-lockup`, `section-heading-lockup`, `card-header-lockup` |
| 118, 120 | `layer-2-direct` | `hero-variants`, `filter-toolbar-bar` |
| 124 | `layer-2-absent` | — (GAP) |

## 5 · UNRESOLVED / ambiguous rows

**None.** `$unresolved` is `[]`; no row hit `layer-2-ambiguous`. The ladder resolved 27 of 28
Layer-2 rows mechanically and did not need a hand-invented mapping for any of them.

**Row 124 — "Per-component variant matrices" — is a GAP, not an ambiguity.** No family prefix in
the row name, no store artefact answers to it, and the fuzzy scan is empty. That is honest: it is a
combinatorial promise ("every base × emphasis/size/state/density"), not a component. ⛔ It is a GAP
that does **not** appear in `$true_gaps`, because `$true_gaps` is deliberately Layer-1-scoped
(`class != "layer-2"`) — kept that way so v1/v2/v3 stay comparable. Whether row 124 should be
promoted into the TRUE-gap list, or is a row the itinerary should not carry at all, is a naming /
scope judgment: **Dave's, not mine.** Named here rather than decided.

## 6 · Findings and residuals

- **NEW FINDING — a whole artefact class is off the radius ratchet.** `$radius_ratchet_advisory`
  jumped 26 → 53: all 27 Layer-2 snippets are absent from
  `_validate_radius.MIGRATED_SNIPPETS`. This was invisible while the rows were never probed. It is
  an ADVISORY by design (migration state, not gating state) and is **not** fixed here — flagged for
  the conductor as the largest single block on the ratchet.
- **`--check` against v2 FAILS out-of-sync, and that is CORRECT.** Driven, not asserted: re-emitting
  through `_emit()` and diffing against the v2 files gives
  `reviews/ITINERARY-STATUS-2026-08-21-v2.html -> OUT OF SYNC` and
  `…v2.json -> OUT OF SYNC`. v2 is a frozen record of the *unfixed* instrument; v3 is the new truth.
  Nothing to "fix" [[green-tests-cannot-see-scope]].
- **status-indicator's 67 → 86 canon-rule jump (rows 47, 88) remains observed, not diagnosed.**
  Not chased, per brief. It persists unchanged in v3.
- **`notes/_REHEARSAL-LOG.jsonl` shows one appended line in `git status`.** It is a `"kind":
  "wrap-open"` check-in record written by `_capture_gate`, identical in shape to the three lines
  above it, and NOT written by this generator or by any edit of mine. Pre-existing session dirt,
  named so the conductor's commit reconcile does not attribute it here.
- **`$true_gaps` semantics unchanged on purpose** (see row 124 above) — a scope decision left open.
- Selftest arm 1 still names live rows (13, 17, 19, 52, 89, 63) expected GATED/BUILT. Those are
  ratchet-direction fixtures (they can only get *more* routed, never less), so they do not rot the
  way arm 2's GAP fixtures did — but they are hand-named and worth re-reading if any of those six
  is ever retired.

## 7 · Evidence pointers

- Generator (edited): `knowledge/gen_itinerary_status.py`
- v1 (untouched): `reviews/ITINERARY-STATUS-2026-08-19-v1.{json,html}`
- v2 (untouched): `reviews/ITINERARY-STATUS-2026-08-21-v2.{json,html}`
- v3 (this run): `reviews/ITINERARY-STATUS-2026-08-21-v3.{json,html}` — Layer 2 is section 5b of
  the HTML, with per-row `basis` and evidence
- Prior receipt: `notes/_receipts/2026-08-21-213-laneI-itinerary-v2.md`
- Red-proof driver: `/tmp/w`-class scratch, `/tmp/zz/red.py` (NON-REPO: sandbox `/tmp`, not committed)
