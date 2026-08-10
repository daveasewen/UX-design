# #146 — two-thirds of a shape, the gate that resolves addresses, and the runner that died quietly

provenance: #146 · 2026-08-10
status: observed

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST delta #146 · ledger: `knowledge/_rulings.json` § `s146-D1` ·
banner: `GOOD-MORNING.md` ★ LATEST #146. This dossier holds the WHY and HOW; the terse records hold
the WHAT.*

## The arc

#145 handed over "three findings, one shape" as a carry-forward premise and residual ① as "build the
binds-resolve gate." The session's first move was to check the premise before building on it — and the
verdict was **⅔, not 3/3**. The `$type` fall-through in `gen_canon_tokens.py` and the binds-no-resolver
gap ARE one shape: a correspondence between two artefacts held by nothing, with silent fall-through on
a non-match. But the T3 self-confirming subject check is a DIFFERENT shape — a reference derived from
its own write, vacuous by construction, needing an independent reference (remedy already prescribed in
memory). Lumping the three would have produced a conflated fix — the exact class
[[conflated-fix-guarantees-recurrence]] names. The premise check changed the build's scope before a
line was written.

## Finding ① was already closed

The font-family regression (#145's finding ⑥) was fixed AND gated pre-session, in the post-wrap commit
`7649faa`: the `string|fontFamily` type match, `$webStack` read, and a raise on non-match. The survey
did not re-do it; it verified the receipt and moved on.

## The shape, live in the survey

The two-artefact-silent-fall-through shape was then hunted across the generator corpus and found live
in four places:

- `gen_snippet_tokens.py` ~221 — `if not mm: continue`: a manifest non-match silently drops a snippet
  from canon sync.
- `gen_theme_cascade.py` ~261 — the same `continue`, dropping from the theme projection.
- `gen_snippet_tokens.py` ~236 — writer-path `except KeyError: continue`, LOUD in the checker (~185)
  but silent in the writer: the same condition, two severities depending on which path runs.
- `gen_snippet_tokens.py` ~227 — the `.cn-<slug>` regex: rename a component and the replacement never
  fires, silently.

Counter-example inside the house: `gen_component_partials.py` fails LOUD on the same class — the
standard exists; these sites predate it. The writer-path KeyError and the regex are generator-code
decisions and were left for Dave/the conductor — declared, not smoothed.

## The gate

`knowledge/_validate_binds_resolve.py` landed as the one-gate remedy Dave licensed ("do it please",
`s146-D1`): manifest presence 75/75 absolute; all 956 manifest vars resolve via
`gen_snippet_tokens.resolve` — ONE router, not a re-implementation; 102 `binds` addresses (41
distinct) exist across the declared stores including the `icon-scale.json` + `opacity.json` routes —
6 addresses no prior instrument could see. Proofs: 5 selftest bites AND two real-corpus mutation
drives (a renamed rung → red; a renamed manifest id → red; both restored byte-identical,
`cmp`-verified). The drives are what make the green a measurement rather than an assertion
[[green-tests-cannot-see-scope]].

⚠ **Readback still owed:** "do it" was read as ratifying the one-gate design. Dave may strike that
reading — the scope of `s146-D1` is his, and the readback is named in the residual.

## The layered orphan

Wiring the gate exposed that `_build_all.py` had been ABORTING at `check_routes()` since #139: four
#139 STEPS entries (KG edge gate + selftest, fork-ban + selftest) had no ROUTE_ROWS row. So the
wiring gate INSIDE the dead runner never ran — which is why it never caught the two #141 orphans
(`_validate_binds_ratchet.py`, `_validate_dtcg.py`). An orphan-detector orphaned by its own runner:
[[instrument-without-a-consumer]], two layers deep. Repaired: routes 110 green, wiring 35/35, both
#141 orphans wired and PASS (ratchet floor 33/75 metas; dtcg 0 fail / 61 deferrals). The full
110-step runner has still never been driven end-to-end in-sandbox (no `--range/--resume`; the ~45s
call wall) — a declared residual, not a claim.

## The KG red was real, and the probe bit the investigator

The KG gate's red was REAL staleness, not flake — and diagnosing it produced this session's own
instance of the class under investigation: the probe `gen_kg_edges.py --corpus X` silently IGNORED
the unknown flag and regenerated the LIVE tree. The resulting 25 modified metas were verified
parse-equal to HEAD (slots/`$kg` position only, generator-owned) and committed in `a2afd5a`.
Hash-seed nondeterminism was ruled out across 5 seeds. The lesson is the session's thesis restated:
an interface that silently accepts a non-match will eventually do it to the person hunting the class.

## Resolved state

`s146-D1` appended to `knowledge/_rulings.json` (105→106, priors parse-equal). Gate live and wired;
runner un-dead; mid-session commit `a2afd5a` carries the enactment. Open: the readback on
`s146-D1`'s scope · the two generator-code decisions (writer-path KeyError, `.cn-` regex) ·
`check_freshness`'s tempfile default on the 85%-full root fs (ENOSPC-suspect, UNPROVEN) · the full
runner drive · MEMORY.md index compaction (hook fired, 19.5KB).
