provenance: #65 Fable conductor · 2026-07-31 · delta audit: `notes/_briefs/2026-07-31-package-delta-audit-DRAFT.md`

# Machinery manifest — every copy, its source, and what it still owes

**Rule (spec):** copies only, every copy delta-audited; no Apollo file MOVES here; no coupling in
either direction. These are **VERBATIM copies** — Apollo names (`GOOD-MORNING.md`,
`_LIVE-STATE.md`, `knowledge/` paths) are still inside them, on purpose. Generalisation is a
build step, not a copy step; a half-renamed copy would be neither auditable nor runnable.

## The copies (sizes MEASURED at copy time, `wc -cl`; source commit = last touch, `git log -1`)

| file | source | src commit | bytes / lines | verbatim? |
|---|---|---|---|---|
| `_gen_chain.py` | `knowledge/_gen_chain.py` | `514f4bd` 2026-08-02 | 25,616 / 445 | yes — **RE-SYNCED #79** |
| `_memento_search.py` | `knowledge/_memento_search.py` | `59148f3` 2026-07-28 | 8,158 / 202 | yes |
| `_search_core.py` | `knowledge/_search_core.py` | `59148f3` 2026-07-28 | 11,869 / 255 | yes |
| `_consult-lexicon.json` | `knowledge/_consult-lexicon.json` | `dbb0ef7` 2026-07-18 | 3,361 / 93 | yes |

## What is deliberately NOT copied

- **`_CHAIN.md` / `GOOD-MORNING.md` / `_LIVE-STATE.md`** — Apollo *content*, not mechanism.
  The package ships the generator; each adopting project grows its own chain.
- **`knowledge/_memento-index.json`** — generated, Apollo content; adopters regenerate.
- **`knowledge/_capture_gate.py`** — Apollo-laced (~2.5K lines of project-specific rules).
  NOT needed whole: `_gen_chain.py` imports four functions —
  `chain_parts` · `measure_tokens` · `measurement_degraded` · `read_chain_tk`
  (probe: `grep -oE 'cg\.[a-z_]+' | sort -u`, 2026-07-31).
  ★ **CORRECTED at the v0.1 build: "exactly four" was a grep of DIRECT calls and missed a
  transitive dependency** — `chain_parts` also needs the `GM_VOCAB`/`LS_VOCAB` tuples from
  `knowledge/_gm_usage.py` (833 lines, otherwise untouched). The build sub caught it and
  ported the two tuples as data into the shim. A dependency list from one grep is a list of
  MATCHES, not of SOURCES. ✅ **Shim SHIPPED as `machinery/_capture_gate.py`** (same module
  name, so the verbatim import resolves unchanged) — debt item 1 CLOSED #65.
- **Capture ritual + record-guarding gates** — the de-coupling job is real and unscoped;
  named as the next machinery wave, not smuggled in tonight.

## Generalisation debt (the port's build list, in order)

1. Four-function gauge shim (above) — smallest, unblocks `_gen_chain.py` standalone.
2. Configurable source-file names (`GOOD-MORNING.md`/`_LIVE-STATE.md` → package config) —
   the boot rule's "chain exists?" check must not assume Apollo's filenames.
3. Index bootstrap for a fresh project (the no-chain arm of the ratified boot rule).
4. Capture-ritual extraction (unscoped — do not start without pricing).
