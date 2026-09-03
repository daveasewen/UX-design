# #242 lane P brief — BUILD `W-387`: the polarity receipt (`s240-D3`), V2 is gated on it

**Model: Opus. Conductor: Fable (#242). Dated period record (ADR-0017) — the store is the live home.**

## THE RULING YOU ENACT (verbatim from `knowledge/_rulings.json` `s240-D3`, Dave's, 2026-09-02)

> A POLARITY'S RECEIPT MAY POINT AT AN R1 ROW OR AT A RULING ID — the quote rule stands (every polarity traces to something Dave ruled) but the anchor widens: a node born after R1 carries a seed receipt naming the `knowledge/_rulings.json` id that created it; a retired node keeps its row and carries `retiredBy` naming the ruling that retired it, and drops out of everything generated from the KG. The receipt is one pointer per node. This is the legal form for a NEW or RETIRED polarity that lane F (#239) found missing; the six false-red controls become legal under it and V2 may run.

Governs: `knowledge/brain/schema/polarity.schema.json` · `knowledge/_validate_polarities.py` · `knowledge/brain/polarities.json`.

## CLOSE CONDITION (`W-387`, verbatim)

> the schema and `_validate_polarities.py` accept a `$seed` receipt and a `retiredBy` node with mutation arms proving both refusals, the `SCHEMA_SHA256` pin moves in the same commit, lane F's six FALSE-RED green controls drive green, and V2 has run against the built gate

You own everything up to "V2 has run" — V2 is a separate verifier lane the conductor fires on your report.

## START FROM REFERENCE — read these FIRST, in this order

1. `notes/_subreports/2026-09-02-239-F-polarity-fix.md` — the fix-by-class lane; its ruling-shaped 4 is where the missing legal form was found. Its `green-controls-recut.txt` and `escaped-now-caught.txt` (paths inside the report) are the six false-red controls you must turn green.
2. `notes/_subreports/2026-09-02-238-V-polarity-verifier.md` — V's harness (the doors, the attack list, `escaped-repro.txt`). V2 will be driven from V's harness, so your arms must be legible to it.
3. `knowledge/_validate_polarities.py` — 2,362 lines. `SCHEMA_SHA256` at :175, checked at :389; the five refusal floors near :48 (Q2). Read the selftest before adding arms (125 arms at #239).
4. `knowledge/brain/schema/polarity.schema.json` + the gate's `--selftest` and `--check` modes.

## THE BUILD

- Schema: a receipt is ONE pointer per node — either an R1 register row (today's form, unchanged) OR a ruling id. Add `$seed` (ruling id that created the node) as the legal receipt for a node born after R1. Add `retiredBy` (ruling id) — a retired node KEEPS its row.
- Gate: accept both; REFUSE by name (a) a `$seed`/`retiredBy` that names an id absent from `knowledge/_rulings.json`, (b) a node with two receipts (one pointer, not two), (c) a retired node that still appears in anything under `knowledge/brain/_generated/` — find the generator and make retired nodes drop out of it. Each refusal gets a mutation arm: green control + break arm RED BY NAME, driven both ways.
- `SCHEMA_SHA256` moves in the same change as the schema. It is a pin, not a decoration — if you touch the schema and not the pin, the gate must go red, and your report must show that it did (that is one of your mutation arms).
- `polarities.json`: byte-UNTOUCHED unless the six false-red controls require a data edit — if so, STOP and put it in the report as ruling-shaped; do not edit data rows on your own judgment (#239 closed 44 escapes without touching a data row; keep that discipline).
- Re-drive lane F's six false-red green controls: they must drive GREEN under the built gate. Re-drive V's `escaped-repro.txt`: ESCAPED must not RISE above 4 (the 4 UNRULED stay Dave's — `W-374`).

## FENCE (consequences replayed — every one of these has bitten before)

- ⛔ NO rulings. `_inscribe_ruling.py` is the only writer of `_rulings.json` and only on Dave's word. Anything ruling-shaped (e.g. "should a retired node's quote be kept?") goes in the report's ruling-shaped list, undecided.
- ⛔ NO edits to `_state.json`, `_lanes.json`, `GOOD-MORNING.md`, `_LIVE-STATE.md`, `_CARRIES.md`, memory, any prior report/brief/asset. The conductor mints store rows.
- ⛔ NO commit, NO push. Leave the working tree with your changes staged-or-unstaged and LIST every path in the report.
- ⛔ NO `_build_all.py` (a partial run strands the tree). Run only `_validate_polarities.py` modes and your own arms.
- ⛔ Sandbox call kill ~178 s wall, ~45 s soft: split long selftests; `pip install tiktoken --break-system-packages` only if a tool refuses.
- ⛔ Vocabulary: `s237-D1` names grades Replicated · Studied · Practised · Debunked · Obligation; "measured" is the gauge's word — do not reuse it in schema field names.
- Do not "fix" the 4 UNRULED escapes (241/301 register receipt · 243 same-ref resolvedBy+challengedBy · 245 links receipt). They are rulings, not bugs.

## REPORT — file it, chat is a stub

`notes/_subreports/2026-09-03-242-lane-P-polarity-receipt.md`, the `_TEMPLATE.md` shape (COUNTS line: files / tests / findings / ruling-shaped / UNPROVEN). Include: every path changed; the old and new `SCHEMA_SHA256`; each mutation arm with its command and its red-by-name line; the six controls' before/after; V's `escaped-repro.txt` count before/after; anything UNPROVEN, declared, never smoothed. Final chat message = report path + the COUNTS line + one sentence on whether `W-387` closes short of V2.
