# VALIDATE RECEIPT — the four edge types against `_validate_kg.py` (#270 lane 1)

**Method.** The live corpus was copied to `/sessions/jolly-serene-meitner/tmp/kg270/`, the generator
was landed **in the copy only**, and the gate was run against the copy. The gate file was **not
edited** — its module constants were passed as arguments or monkeypatched in the harness, which is
what the brief allows. The scratch tree was deleted afterwards (`rm -rf`, confirmed).
**Nothing in `knowledge/components/` was written.** `git status --porcelain` after every run shows
only `?? knowledge/gen_kg_roles_desk.py` and `?? notes/_lanes/270/`.

---

## Run 0 — baseline, live tree, unmodified

```
$ python3 knowledge/_validate_kg.py
== _validate_kg.py — KG edge parse-gate (s131-D2 / s133-D1 / s135-D4) ==
metas checked: 139
ref:null + $note (declared, awaiting Dave's-eye migration): 88
resolutions consumed (s135-D4, …): 82 ruled verdicts asserted present (MERGE 5 / PROMOTE 52 / ATTACH 25)
_validate_kg.py: OK
```
**GREEN.** 0.8s.

## Run 1 — landing the generator in the scratch copy

```
$ cp -r knowledge/components /sessions/.../tmp/kg270/components
$ python3 knowledge/gen_kg_roles_desk.py --corpus /sessions/.../tmp/kg270/components \
      --land --ratified s269-D10
LANDED — ratified s269-D10 · 26 metas written · 115 edges
  ({'providesRole': 24, 'answersIntent': 28, 'hasDataShape': 26, 'yieldsTo': 37})
$ diff -rq knowledge/components /sessions/.../tmp/kg270/components | wc -l
26
```
`s269-D10` is a **real, existing ruling id used as a scratch stand-in so the guard could be
exercised as written** — not a claim that s269-D10 ratifies anything. The live tree was never a
`--land` target. Sample diff (`stat-card.meta.json`) is pure addition: three new keys appended
inside the existing `edges` block, every prior edge byte-identical.

## Run 2 — the gate against the landed copy, **schema NOT diffed** (the control)

```
UNPATCHED — fails: 100 · metas: 138 · ref:null+$note: 88
  100 × "unknown edge-type key '<type>' (not in meta.schema.json edges.properties)"
```
**RED, as expected and as designed.** 100 = the per-meta key count (24 providesRole + 26
answersIntent + 26 hasDataShape + 24 yieldsTo keys across 26 metas). Check (d) rejects the key and
`continue`s, so the refs never even reach check (a). **This is the proof that the four types cannot
land without Dave's vocabulary change** — the fence is real and the gate enforces it.

## Run 3 — the gate against the landed copy, **with the proposed diff applied to the scratch schema**

Applied in the scratch copy only: the four edge-type keys (hunk 1 of `SCHEMA-DIFF.md`), the widened
`ref` pattern (hunk 2), and the `_validate_kg.py` resolver widening (hunk 3) supplied by
monkeypatching `REF_RE`, `NODE_KINDS` and `resolve_ref` — **the gate file on disk was not touched**.

```
PATCHED — fails: 0 · metas: 138 · ref:null + $note: 90
```
**GREEN.** Checks (a) (b) (c) (d) all clean. `ref:null + $note` rises 88 → **90**: exactly the two
anaphoric `yieldsTo` entries (Chart-boxplot "yields to it", Chart-bullet "yields to both"), each
carrying its prose note. No ref fails the grammar; every `role:` / `intent:` / `shape:` ref resolves
against its store.

## Run 4 — check (e), generator idempotence, on the landed corpus

`check_freshness()` copies from the module constant `HERE/"components"`, so running it under a
patched `V.COMPONENTS` compares a regeneration of the **live** corpus against the **landed** one and
reports 26 spurious drifts. That is a harness artefact, not a finding — it was diagnosed and redone
properly: the landed corpus was copied into a full scratch `knowledge/` tree (components, snippets,
`_proforma`, `gen_kg_edges.py`, `_helpgate.py`, and `reviews/KG-REVIEW-VERDICTS-…json`) and
`gen_kg_edges.py` was run there directly.

```
$ python3 gen_kg_edges.py   # rc=0, "pattern nodes: 380 / context nodes: 222 / 82 ruled rows compiled"
$ diff -rq <landed corpus> components | grep -c differ
0
```
**GREEN.** `gen_kg_edges.py` is idempotent-clean over the landed corpus: `merge_edges` (s268-D6 (c))
carries the four new types untouched. **No edit to `gen_kg_edges.py` is required.**

## Run 5 — check (f), resolutions consumed

```
(f) resolutions consumed — fails: 0 · counts: {'merge': 5, 'promote': 52, 'attach': 25}
```
**GREEN.** Unchanged from baseline — the four new types touch none of the ruled verdicts.

## Run 6 — the explorer, against the landed corpus

```
$ python3 -c "import _build_kg_explorer as B; n,e=B.extract(K='<scratch knowledge>')"
nodes 935  edges 1382
node types: pattern 380 · context 222 · component 137 · snippet 137 · shape 23 · intent 14 · ruling 14 · role 8
new edge types: providesRole 24 · answersIntent 28 · hasDataShape 26 · yieldsTo 37
```
**GREEN, with one cosmetic gap.** Base graph 890→**935** nodes (+45) and 1267→**1382** edges (+115).
`_build_kg_explorer.py` needs **no code change** — `extract()` types a node from its id prefix. But
`_kg_explorer.template.html` paints nodes from `--c-<type>` CSS vars and has none for `role`,
`intent` or `shape`, in any of its three theme blocks; the new nodes would render with an undefined
colour. Three vars, three places — hunk 4 of `SCHEMA-DIFF.md`. Not yet ruled, not yet applied.

## Run 7 — the generator's own selftest

```
$ python3 knowledge/gen_kg_roles_desk.py --selftest
  ok  bite 1: alpha derives providesRole/answersIntent/hasDataShape/yieldsTo
  ok  bite 2: `beats beta` produces no yieldsTo beyond the two yields targets
  ok  bite 3: off-vocabulary provides/answers/shape -> ref:null + $note
  ok  bite 4: `yields to it` -> ref:null + $note; gamma carries no new edges
  ok  bite 5: --land is by addition (renderedBy survives) and byte-idempotent
  ok  bite 6: --land REFUSES with no id, an absent id and a malformed id, and writes nothing
  ok  bite 7: no store file is written by a dry run or a land
  ok  bite 8: --dry-run writes its JSON and leaves every meta byte-identical
SELFTEST PASS
```
Bite 6 is the **mutation test**: three bad ratifications (absent, malformed, missing) each raise
`SystemExit` and the synthetic corpus is byte-identical before and after — the guard is driven, not
asserted.

---

## Verdict

The four edge types validate clean **only with the `SCHEMA-DIFF.md` hunks applied**, and the gate
goes hard red without them. That is the closed-vocabulary fence (#75) doing its job, and it is why
this lane stops here.
