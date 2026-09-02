# #235 — LANE L1: the RECEIPT and `_validate_receipt.py`

*Written 2026-09-02 by the Fable conductor. ONE Opus build sub. Report files at `notes/_subreports/2026-09-02-235-L1-receipt-gate.md` per `s218-D7`; chat gets a STUB. Parent brief: `notes/_briefs/2026-09-02-234-v106-brief.md` § L1.*

## WHAT IS RULED (Dave's — build against these, never re-open them)

| id | ruled |
|---|---|
| `s234-D6` | the rubric binds to the artefact through `_validate_screen.py <path>`; the page carries a provenance RECEIPT the gate PARSES first; folder globs are NOT widened |
| `s234-D5` | behaviour address = typed declaration in the meta + a generated snippet block (the `#token-manifest` precedent) — L2 builds the meta half; L1 only READS what is there today |
| `s235-D1` | the receipt is KEYED ON A CONTENT HASH of the spliced region, not filename or slug; filename/slug/pack version may ride along for the reader; the gate COMPARES on the hash; a receipt is valid against the pack version it was minted from |
| `s235-D2` | the new gate is `knowledge/_validate_receipt.py`; `_validate_screen.py` chains into it FIRST; `_validate_behaviour.py` stays what ADR-0015 made it |

Read them from `knowledge/_rulings.json` (grep the ids) — the table is a pointer, the store is the text.

## THE DELIVERABLE (all four, or say which is UNPROVEN and why)

1. **The receipt block spec + generator.** A `<script type="application/json" id="provenance-receipt">` block (mirror the `#token-manifest` shape — `knowledge/gen_component_partials.py:301` has the regex that proves the precedent) carrying, per spliced region: `snippet` (slug, for the reader) · `hash` (sha256 of the spliced region's bytes, THE KEY) · `variant`/`props` values used · `script` (the behaviour address as the meta declares it today, or `null`) · `pack` (version string) · `retrievalSet` (version, or `null` with a `$note` that rC Q4 is open). Generator: whichever module today injects `#token-manifest` into snippets gains the receipt injection BESIDE it, never inside it. **Hash the bytes the extractor actually splices** — the `#231` borrow-ledger precedent (`template-dashboard-bento.meta.json` `$cardinalRule`) is the shape to copy.
2. **`knowledge/_validate_receipt.py`.** Takes ONE path. Parses the receipt FIRST (no receipt ⇒ a NAMED refusal, exit nonzero, never a silent pass). Then, per region: re-hashes the region in the page and compares to `hash` (mismatch ⇒ INVENTION, named by slug + the first differing byte offset); confirms the behaviour address in `script` is loaded by the page (a `<script src>` or inline id match) or reports `NO-BEHAVIOUR-DECLARED` when the meta has none; reports the pack version. Output vocabulary: ADR-0016 — `PASS` / `FAIL:<reason>` / `UNPROVEN:<what would prove it>`. Fail LOUD and NAMED on a parse error (a crash is not a fail).
3. **The chain.** `_validate_screen.py <path>` calls `_validate_receipt` as step 0, before compose. Existing steps untouched. `check-with-gates/SKILL.md` gains ONE line naming the new step, beside the existing list, never re-wording it.
4. **DRIVEN on a real page.** Run the gate on `dashboards/international-banking-dashboard.regen-v1.html` (a #227 regen, no receipt today ⇒ expect the NAMED refusal) and on ONE page you regenerate WITH the receipt (generate, do not hand-write). Then a mutation: alter one byte inside a spliced region and show the gate names the slug. Quote the three outputs in the report.

## GROUND IN THE REPO FIRST (~15 min, before writing a line)

`knowledge/_validate_screen.py` whole · `knowledge/gen_component_partials.py` lines 1–60 + 290–320 · `knowledge/components/meta.schema.json` lines 60–77 and 185–198 (rC's REPLAY-THESE) · `knowledge/_validate_advisory.py` docstring lines 1–70 and `knowledge/_validate_behaviour.py` docstring lines 1–25 (rA's REPLAY-THESE) · `notes/_subreports/2026-09-02-234-rC-retrieval-contract.md` § findings on the receipt shape (Figma shader `version` = SHA + `{filename, bytes, uri}`) · `knowledge/_RUNBOOK-render-verify.md` only if you need a browser (you should not — this lane is parse + hash, no render). **Do NOT read `GOOD-MORNING.md`, `_CHAIN.md`, or any `_subreports` beyond rA/rC.** Say in the report that you READ the rA and rC REPLAY-THESE lines — `W-340` and `W-342` close on that sentence.

## DO NOT RULE

No ruling, no re-wording of `s234-D*`/`s235-D*`. Not yours: the `events` field shape (rC Q3) · the retrieval-set membership marker (rC Q4 — leave `null` + note) · the three-tier vocabulary (rA Q2) · the meta `behaviour` typed object (that is L2 — read the prose value that exists, do not promote it) · any widening of a folder glob · `_rulings.json` · `_state.json` · any `.meta.json` · `DESIGN-CONTRACT.md`. No git operations — the conductor commits. `knowledge/_tmp/` is not yours.

## FILING

Copy `notes/_subreports/_TEMPLATE.md`; `sub index` = `L1`; `brief:` = this file. Every claim carries its probe (path:line or the command + quoted output). ADR-0016 vocabulary throughout. Close with **REPLAY-THESE** (≤ 5 items with token prices) and a **PITFALLS SEEN** list. Chat stub: verdict · files touched (paths) · the three drive outputs in one line each · token spend · REPLAY-THESE.

## PITFALLS (consequences replayed, #165)

- **A gate that runs on nothing cannot fail** [[instrument-without-a-consumer]] — if `_validate_screen.py` does not actually call yours, the lane is not done. Show the call in the diff.
- **Green tests can't see scope** — the mutation must be on the REAL regenerated page, not a fixture you wrote.
- **Hash the SPLICED bytes, not the reference file** — hashing the reference makes every page pass; the key is the page's own region.
- **Sandbox call boundary ~178 s** — drive steps individually; nothing in `/tmp` survives. Evidence goes beside the report.
- **`tiktoken` first** if any instrument you call measures; otherwise a refusal masquerades as a red.
- **A crash is not a fail** — a malformed receipt yields a NAMED refusal, not a traceback.
- **Do not invent a receipt by hand** to make the drive pass — that is the exact defect the gate exists to catch.
