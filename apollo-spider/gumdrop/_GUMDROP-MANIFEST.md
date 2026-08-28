provenance: #219 lane N3 · 2026-08-26 · rulings `s219-D5` (Q1, Q4) · `s219-D8` (naming)

# Gumdrop cold-start manifest — what is here, where it came from, and what it owes

This folder is the **record half** of Memento — Gumdrop: the two stores, the machinery that writes
them, the starter chain, and the two runbooks rewritten for VS Code + Copilot. The **chain half**
(`_gen_chain.py`, retrieval, the graph edges, the gauge shim) is the older cut and lives in
`machinery/` beside this file in the baked pack.

⚠ **In the repo these files live at `apollo-spider/gumdrop/`. In the pack they land at
`memento-package/`.** The move is done by the release generator's seed map
(`knowledge/_release/_gen_pack_manifest.py`, `SEED_PREFIXES`), not by hand, and `--check` verifies
the pack through the same mapping so the stager and the checker cannot disagree about the layout.

## Why they land THERE and not somewhere tidier

Every piece of Memento machinery resolves its own homes from **where the file sits**, and the
placement is therefore a measurement, not a preference:

| module | resolves | which means it must sit |
|---|---|---|
| `machinery/_gen_chain.py` | writes `_CHAIN.md` into its own grandparent | chain root = `memento-package/` |
| `_state.py` | reads `_state.json` from its OWN dir; resolves `home` against the parent | one level above `machinery/` |
| `_inscribe_ruling.py` | reads `_rulings.json` from its OWN dir | one level above `machinery/` |
| `_governs.py` | resolves an evidence PATH against its own grandparent | one level above `machinery/` |

Put the record machinery in `machinery/` and the parent becomes `memento-package/`, so a designer's
ruling citing a real file (`knowledge/tokens/…`, `showroom/…`) is refused as *path does not exist* —
the resolver would be looking inside the wrong directory. Measured both ways before this was fixed.

## The copies

Copies only, in the memento-package tradition: no Apollo file MOVES here, and nothing here is a
divergent fork. Sizes measured at copy time (`wc -cl`); source commit is the last touch at copy time.

| file | source | src commit | bytes / lines | verbatim? |
|---|---|---|---|---|
| `_helpgate.py` | `knowledge/_helpgate.py` | `416e1a6` | 9,215 / 189 | yes |
| `_governs.py` | `knowledge/_governs.py` | `5882813` | 45,994 / 762 | yes |
| `_inscribe_ruling.py` | `knowledge/_inscribe_ruling.py` | `f773cc2` + #219 N3 | 49,611 / 908 | yes |
| `_state.py` | `knowledge/_state.py` | `1b08f68` + #219 N3 | 50,851 / 921 | yes |

⚠ **`f773cc2` and `1b08f68` are pre-#219 commits.** Both files carry uncommitted #219 N3 changes at
the time this manifest was written; the copies are byte-identical to the working tree, and the row
above should be re-stamped with the landing commit at the seam.

### The #219 N3 changes to the two writers, and why they are at cause

Both were found by driving the shipped machinery against the EMPTY stores this release ships. Both
are fixes in Apollo's own file, then re-copied — never a patch applied only to the copy, which is
how the two halves silently diverge.

1. **`_inscribe_ruling.compose()` could not write into an empty store.** It spliced after the last
   `}` in the file's head, and an empty `"rulings": []` has none — `ValueError`. So the one
   sanctioned writer was the one thing that could not write a project's *first* ruling, and the
   empty store this release ships was illegal on arrival. The insertion point is now derived from
   the array's own `[`, structurally, in both arms. ⚠ The old line was latently wrong even when it
   worked: `rindex` searched the whole head, so any file whose pre-`rulings` keys contained an
   object would have had the entry spliced OUTSIDE the array.
2. **`_inscribe_ruling` and `_state` selftest fixtures addressed Apollo repo paths.** Run from a
   shipped pack they reported the *environment* as a store defect. The fixtures are now derived
   from the module's own location, and the arms that genuinely need Apollo's files declare
   `UNMEASURED` rather than failing — declared, never silently skipped, and never a pass.

## The stores

`_state.json` and `_rulings.json` ship **empty and well-formed**. Both were driven against the
shipped machinery before release:

| check | verdict |
|---|---|
| `_state.py` bare, against the empty store | exit 0, zero counts |
| `_state.py --selftest` inside the pack | 57 bites, all green |
| `_inscribe_ruling.py --dry-run`, first entry | accepted, reconstruction proof passed |
| `_inscribe_ruling.py --write`, first entry | inscribed, 0 → 1 rulings, all other bytes identical |
| `_inscribe_ruling.py --selftest` inside the pack | runs; 3 arms declared UNMEASURED (see above) |

## The vendored encoder (`s222-D2`, #222) — the one thing here that is not a copy of Apollo

`_encoder-cache/9b5ad71b2ce5302211f9c61530b329a4922fc6a4` (1,681,126 bytes, sha256
`223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7`) is `tiktoken`'s own MIT
encoding data for `cl100k_base`, mirrored from
`https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken`. It is not an Apollo
file and has no `knowledge/` original, so it is not in the copies table above — it is a vendored
third-party artefact, and `_encoder-cache/README.md` beside it carries its provenance and licence.

**Why it is here.** Dave, #222, off the first live Copilot-bridge session, where the chain
inscription refused because that host was unreachable: *"I need this to work out of the box for
the designers."* With the data inside the pack, token measurement needs no download, no reachable
host and no environment variable.

**One helper, one home.** `machinery/_encoder_home.py` is the only place that path is written
down. It resolves `_encoder-cache/` by walking up from its own file, then does
`os.environ.setdefault("TIKTOKEN_CACHE_DIR", …)` — `setdefault`, so a designer's own value wins.
`machinery/_capture_gate.py` (both packed copies of the shim, at different depths) calls it once
at import; the plugin mirror is NOT given a second copy of the helper — it finds this one, which
is the point of `setdefault` and of a resolver that searches rather than assumes.

**The refusal is untouched.** If the vendored file is missing or the wrong size, the helper says
so on stderr, loud and naming the exact path, and `_gen_chain.py` then refuses to write a chain on
an estimate exactly as it always has. Nothing here makes a failure quieter; it makes the real
measurement reachable. Check the whole path with
`python3 memento-package/machinery/_encoder_home.py --check`.

## What is deliberately NOT here

- **A record of any kind.** No chain content, no rulings, no tasks. Every adopting project grows
  its own.
- **`GOOD-MORNING.md` / `_LIVE-STATE.md`.** They are written by the project's FIRST wrap, and
  `_gen_chain.py` refuses cleanly until they exist — a refusal the package's README already
  documents as expected rather than a fault.
- **The capture gate.** Apollo's enforcing wrap script checks things specific to Apollo's own repo
  layout, and would fail here for reasons no adopting project could fix. The capture runbook says
  so and names the honest substitute.
- **Real token measurement.** No API-key machinery, no session-log reader. Copilot exposes no token
  count to itself, so the gauge runbook declares the gap and teaches the estimate tier instead of
  shipping an instrument that returns a confident wrong number.

## Owed

1. Re-stamp the source-commit column once #219's changes land.
2. There is **no delta gate over these four copies.** `_validate_package_delta.py` covers
   `memento-package/` only, and by design does not glob `apollo-spider/`. The copies can drift
   from `knowledge/` silently — which is exactly the defect that gate was built to end after a
   package copy fell 54 lines behind undetected. Extending its allowlist and its glob to this
   folder is the obvious next move and is priced, not done: it widens a gate's scope, which is a
   decision rather than a chore.
