# `#238`-`B` — L2, the BEHAVIOUR ADDRESS (`s234-D5`): schema, migration proposal, generator, gate — built for Dave's eye before it populates

session: `#238` · 2026-09-02
window: lane B (L2 of the v1.0.6 brief) — one Fable sub, parallel to lanes A/C/…
sub index: `B`
brief: `notes/_briefs/2026-09-02-238-B-L2-behaviour-address-brief.md`
tokens: `UNMEASURED — no message.usage at a sub's seat`. Shape for the conductor's ledger: ~90 tool
calls; three whole-file reads (`_validate_receipt.py` 477 lines, `gen_component_partials.py` in three
slices ≈ 1,000 lines, the L1 report 389 lines); the 100 KB review page was GENERATED and probed, never
read back; 3 of 12 render PNGs viewed by eye; one 20 KB schema read in two slices; no archive re-read
(`_memento_search.py` not needed — every premise was in the brief's named files).

## VERDICT

**All five brief deliverables DONE; nothing populated; the gate bites on a real page and its own
mutants.** (1) The schema is a JSON-Schema fragment + a two-hunk diff against `meta.schema.json`,
by addition — all 136 live metas still validate, the 20 proposals validate, 15 planted defects go
red and 6 controls stay green. (2) The migration is a PROPOSAL file: 20 prose values → 20 typed
objects, every field carrying its basis — 12 fields settled by the prose (quoted), 54 by a probe on
the reviewed snippet, **14 UNPROVEN, all of them `fallback`** (what the component does with JS off:
no prose settles it), with a candidate reading kept OUTSIDE the proposal. ⛔ No meta was written.
(3) The review page `_REVIEW-L2-behaviour-address-2026-09-02-v1.html` (swiss, light+dark, 1440+390,
rendered and looked at) shows the 20 side by side, old → proposed, with L1's three questions and
five of this lane's, each with options and a recommendation, none ruled. (4) `gen_component_partials.py`
derives a `#behaviour-manifest` block beside `#token-manifest` from a TYPED meta (silent on prose,
refuses orphans and bad addresses); `_validate_receipt.py` reads the META address and checks the
page loads it, two-sided by construction; both driven on a `/dev/shm` fixture with the brief's
PRESENT / ABSENT / WRONG arms and nine more — 12/12 as expected; 35 gate self-test arms green, 10
gate mutants and 4 generator mutants caught. (5) Rule 2a is drafted below as a PROPOSED block.
**The live tree is untouched by any run**: 0 metas are typed, the generator pass emits nothing,
`--check` is green in 1.8 s, and the receipted dashboard's verdict changes only by notes plus one
honest UNPROVEN line.

**Two things the conductor must not skim.** (a) The address is never in the prose (the s234-D5
census holds: "addressing the script in none"), so `script` is settled by MEASUREMENT for the 14
interactive metas — a probe on the snippet, not a reading of the words — and the proposal says so on
every one; a prose-only rule would have left the whole migration UNPROVEN and useless. (b) A
`#script` address pointing at ANOTHER component's snippet would have passed the gate whenever that
other script was on the page (finding 6). It is refused as `BEHAVIOUR-ADDRESS-FOREIGN` on both sides;
that is a constraint I added to the proposed grammar and it is question 1 below, Dave's.

COUNTS: findings `13` · ruling-shaped `5` · UNPROVEN `5`

Brief's own counts line: **metas with behaviour 20 · migrated-proposed 20 · UNPROVEN 14 (fields, all
`fallback`, on 14 metas) · gate arms 35 (red 22/22, green 12/12, helper 1) + drive arms 12 (red 10/10,
green 2/2) + schema arms 21 (red 15/15, green 6/6) · L1 questions 3 (carried)**.

## What was done

**Region 1 — the schema.** `notes/_subreports/assets/2026-09-02-238-B-L2-behaviour-address/behaviour.schema.fragment.json`
(the `behaviourAddress` definition + the discriminated `behaviour` property) and `meta.schema.proposed.diff`
(two hunks, 85 changed lines, produced by `apply_schema.py` — text surgery on two anchors, refuses
if either is not found exactly once, `Draft7Validator.check_schema` before writing). The shape:

```
"behaviour": {
  "script":   null | "knowledge/<path>.js" | "knowledge/snippets/<Slug>.reference.html#script",
  "partial":  null | "<name registered under component-types.json $behaviour>",
  "events":   ["click", …],                 // OPTIONAL — rC Q3 is open, shape floated
  "fallback": "<what it does with JS off>" | null,   // null = NOT DECLARED (unproven), never "none"
  "$note":    <the pre-s234-D5 prose, verbatim>,
  "$unproven": ["fallback"]                 // only when a field is null for want of evidence
}
```

Discriminator = the `script` key: an object carrying it MUST validate as an address; anything else is
LEGACY prose, legal during migration, closed later by a ratchet gate — never by the schema (the
`s140-D1` "permit now, enforce by gate later" posture). `script: null` is a POSITIVE "no script";
`fallback: null` is "undeclared". Proved by `schema_arms.py` → `schema-arms.txt`: 136/136 live metas
pass the proposed schema, the 20 prose values take the legacy branch, 20/20 proposals pass, 15 planted
defects red (bare filename · node-id grammar · `#script:2` · a `.css` · `partial` missing/uppercase ·
`fallback` missing/empty · `events` string/duplicate/`Click Me` · an extra prose key · bad `$unproven`
· numeric `$note` · numeric `behaviour`), 6 controls green.

**Region 2 — the migration PROPOSAL.** `…/behaviour-migration.json` (72 KB), built by
`build_migration.py` — 20 items, each `{old, proposed, provenance{field:{basis, quote|probe,
candidate, what_would_prove}}, unproven, measured}`. Bases: `prose` 12 · `measured` 54 · `UNPROVEN` 14.
The 6 passive (account-card · action-bar · badge · confirmation · eyebrow · summary): `script: null`
by prose AND probe (0 executable scripts — they agree), `fallback` "identical — the component carries
no script". The 14 interactive: `script` = `…#script` by probe (each carries exactly ONE inline
executable `<script>`, 956–11,225 bytes), `events` measured from `addEventListener` names with the
page-level modality tracker excluded and prose quotes beside each corroborated event, `fallback: null`
+ `$unproven` + a candidate sentence in `provenance` only. `partial: null` for all 20 (0
AUTO-BEHAVIOUR markers). ⛔ `knowledge/components/*.meta.json`: untouched (probe: `fixture-build.txt`
line 5d — 20 fixture snippets differ from live, 0 live files written by this lane).

**Region 3 — the review page.** `_REVIEW-L2-behaviour-address-2026-09-02-v1.html` (100,932 bytes,
generated by `build_review.py` FROM the migration JSON + the drive summary, so it cannot disagree
with the files). Sections: answer · the shape (grammar (a) vs (b) side by side) · the 20 with a
filter controller (All / Passive 6 / Carry a script 14 / With an unproven field 14) · proof table
(12 drive arms) · L1's three questions · this lane's five · rule 2a · consequences (8 cards, owners).
Rendered per `_RUNBOOK-render-verify.md` seventh stratum (mount `syslibs`, `TMPDIR=/dev/shm`):
`scrollWidth == clientWidth` at 1440 and 390 in both themes after one fix (finding 12); PNGs in the
assets dir, three looked at by eye. Two-red law honoured (`#DA1A00` on white, `#F6604C` dark).

**Region 4 — generator + gate, on a fixture.**
- `knowledge/gen_component_partials.py` (1,003 → 1,255 lines): `behaviour_manifest_block`,
  `inject_behaviour_manifest` (anchor and existing block LOCATED LIVE via `live_match`, spliced on raw
  bytes), `behaviour_manifest_fails`, `run_behaviour_manifests` (wired at the end of `run()`), selftest
  arm 5i (ten sub-arms). Imports the address grammar from the gate (`import _validate_receipt as VR`)
  — the direction the mint already takes; nothing re-implemented.
- `knowledge/_validate_receipt.py` (477 → 937 lines): `ROOT`, `ADDRESS_RE`, `inline_scripts` (comment-masked
  via `_htmlmask`, raw-sliced), `snippet_file`, `meta_path_for`, `load_meta`, `typed_behaviour`,
  `behaviour_state`, `registered_partials`, `resolve_address` (META side), `address_loaded` (PAGE side,
  sha256 byte-identity with a whitespace / near-copy hint), `foreign_script_address`,
  `behaviour_verdict`; `check()` calls it for every markup region and emits ONE
  `UNPROVEN:behaviour-address` line naming the regions whose meta is PROSE/NONE. New reasons:
  `BEHAVIOUR-ADDRESS-UNRESOLVABLE` · `BEHAVIOUR-ADDRESS-FOREIGN` · `BEHAVIOUR-ADDRESS-DISAGREES` ·
  `BEHAVIOUR-PARTIAL-UNREGISTERED` (+ `BEHAVIOUR-NOT-LOADED` re-used). Selftest arms J–Z2 (26 new)
  on a temporary knowledge tree. `_validate_screen.py` is NOT modified — its step 0 calls
  `receipt.check()` and inherits 4b (drive J/K prove it blocks through the chain).
- Fixture: `fixture_build.py` copies `knowledge/{*.py, snippets, components, tokens, canon}` to
  `/dev/shm/l2fix` (5 s; `/dev/shm` is per-call so every drive rebuilds), applies the schema and the
  20 proposals, validates 136/136, runs `--check` (20 out of sync) → write (20 injected) → `--check`
  (OK), then composes one page with L1's mint (Date-picker · Textarea · Stat-card) and splices the two
  inline scripts verbatim as `kind=script` regions (finding 7), re-minted.
- Drives: `drive_arms.py` → `drive-A…I-*.txt` + `drive-arms-summary.json` (12/12 as expected), plus
  `drive-J/K` (the chain, green then blocking), `drive-L` (the chain's default 7-screen population on
  the fixture: 7 × `UNPROVEN:NO-RECEIPT`, `PASS`), `drive-0` (the LIVE receipted dashboard, read-only:
  same 12 greens, notes added, +1 UNPROVEN), `drive-M` (L1's `mutate.py` still reds at offset 184).
- Mutants: `selftest-validate-receipt-mutants.txt` (10 gate mutants, every one turns the selftest
  red; control green) · `selftest-gen-component-partials-mutants.txt` (4 generator mutants, same).

**Region 5 — rule 2a, PROPOSED text (not written into the pack; v1.0.5 HELD, no bump):**

```
2a. **Copy the script address with the markup; author no JS.** Every snippet whose
    component carries behaviour declares its ADDRESS in `knowledge/components/<slug>.meta.json`
    (`behaviour.script`) and carries the same address in a `#behaviour-manifest` block beside
    `#token-manifest`. Take the snippet's own `<script>` (or its `AUTO-BEHAVIOUR` block)
    verbatim — the bytes are the key — and carry the address into the page's receipt. Never
    write a handler yourself, never paraphrase the script, never point at another component's
    script: shared behaviour is a registered partial. `fallback` says what the component does
    with JavaScript off; if it is null, say so in the Gaps list rather than inventing one.
    `_validate_receipt.py` reads the meta and checks the page loads what it names.
```

### FILES TOUCHED (for the reconcile)

| path | state |
|---|---|
| `knowledge/_validate_receipt.py` | MODIFIED — docstring 4b + the META-address section + `check()` call site + arms J–Z2 |
| `knowledge/gen_component_partials.py` | MODIFIED — docstring + behaviour-manifest section + `run()` wiring + selftest 5i |
| `_REVIEW-L2-behaviour-address-2026-09-02-v1.html` | NEW — generated |
| `notes/_subreports/2026-09-02-238-B-L2-behaviour-address.md` + `assets/…/` (46 files) | NEW — this report + evidence, scripts, renders |

⛔ Not touched: every `knowledge/components/*.meta.json` and `meta.schema.json` (proposal only) ·
`apollo-spider/` (read only) · `_validate_screen.py`, `gen_provenance_receipt.py` (L1's files —
findings 7/8 name what they need) · `_SCREEN-GATE.md` / `_screen-gate/` (the chain was driven on
the fixture, so no live record was rewritten) · the store, the spine, memory. No git.

## Findings

**1 — THE POPULATION IS 20 = 15 OBJECTS + 5 STRINGS; "THREE JSON TYPES" IS THE SCHEMA'S ALLOWANCE,
NOT THE DATA.** Probe: `Counter` over `knowledge/components/*.meta.json` → `{'dict': 15, 'str': 5}`;
`meta.schema.json:197` allows `object|array|string`. No array exists. (s234-D5's "three JSON types"
reads the schema.)

**2 — "136/136 SNIPPETS CARRY `<script>`" COUNTS THE JSON MANIFEST.** Probe over all 136: executable
inline scripts (no `src`, type absent/`text/javascript`/`module`) — 91 carry one, 8 carry two, 1
carries three (the charts: AUTO-BEHAVIOUR payloads), **36 carry none**; `<script src>` 0/136;
`#token-manifest` 136/136 and **all in `<body>`**. So a `script` address exists for 100 snippets, and
`null` is the honest value for 36.

**3 — THE ADDRESS IS NEVER IN THE PROSE AND ALWAYS IN THE SNIPPET, AND THEY NEVER DISAGREE.** For the
20: 14 snippets carry exactly one inline executable script (956–11,225 bytes), 6 carry none — and the
6 are exactly the ones whose prose says "passive / no states". 0 conflicts. Hence `script` is
`measured` on 14 and `prose`+`measured` on 6, and no meta needed a guess.

**4 — THE DERIVED BLOCK LANDS BETWEEN THE MANIFEST AND THE SCRIPT IT NAMES.** `#token-manifest` sits in
`<body>` immediately before the inline `<script>` in every snippet (Date-picker: manifest @24,122 <
behaviour-manifest @26,812 < script @27,324 — `fixture-build.txt` 5e). An agent copying the body
copies the address with the script. The block carries only the four address fields plus `component`
and a `$generated` provenance — no prose, no clock (idempotent; selftest 5i (ii)/(iii)).

**5 — THE 14 DATAVIZ METAS HAVE NO `behaviour` KEY WHILE THEIR SNIPPETS CARRY 1–3 REGISTRY PARTIALS.**
Probe: 14 snippets with AUTO-BEHAVIOUR markers, all `meta:NONE`; Chart-donut carries `dv-behaviour ·
dv-donut-sweep · dv-legend`, 8 others carry two. The brief's `partial: <id|null>` is singular and
cannot hold them. Not in this lane's 20; a second, MECHANICAL migration (registry → meta) once the
shape is ruled — question 2.

**6 — A FOREIGN `#script` WAS A HOLE, AND IS CLOSED.** With the grammar as first cut, a meta pointing
at Textarea's script passed on any page that carried Textarea. Refused now as
`BEHAVIOUR-ADDRESS-FOREIGN` in the gate (arm Y, drive D) and in the generator (5i (vi-b), drive D2);
the own stem in another case is NOT foreign (arm Y2 — the SKILL's case-insensitive rule). Shared
behaviour is a registered partial. This is a constraint on the proposed grammar → question 1.

**7 — THE L1 MINT HAS NO `kind: script`.** `gen_provenance_receipt.py --compose` splices `markup`,
`style` and AUTO-BEHAVIOUR `behaviour` regions; a snippet's plain inline `<script>` — the form 100/136
carry — cannot be spliced or receipted by it. The fixture spliced the element by hand between
`APOLLO-SPLICE … kind=script` markers and `--mint` receipted it fine (the mint reads `kind` off the
marker). Price: one more `kind` in `compose()` + one selftest arm, ~1K tokens; L1's file.

**8 — THE MINT'S `$scriptNote` AND `behaviour_address()` WILL BE FALSE THE DAY A META IS TYPED.** They
say "meta `behaviour` is untyped prose (meta.schema.json:197)". The mint should resolve `script`
through `VR.typed_behaviour` / `VR.resolve_address` (it already imports `VR`), ~500 tokens; until
then the receipt's `script` stays `null` for the 14 and the gate's meta side does the work (drive A
shows LOADED with `receipt script null` — no false red, because DISAGREES fires only when both are
non-null and differ).

**9 — THE `keydown / mousedown / touchstart` TRIO IS A PAGE-LEVEL HARNESS, NOT THE COMPONENT'S
EVENTS.** 11 of the 14 scripted snippets open with the same three window-level listeners writing
`document.documentElement.dataset.modality` (the focus-visible heuristic). Excluded from `events` by
that exact signature (window-level, no element listener of that name, `dataset.modality` present);
without the exclusion those 11 would each list all three (anchor-nav, command-palette and tab-bar carry no tracker). Anchor-nav has no listeners at all — its
scrollspy is an `IntersectionObserver`, recorded under `observers`, not `events`.

**10 — ONE SNIPPET STATES ITS OWN NO-JS ANSWER.** `Anchor-nav.reference.html`, first line of the
script: *"The authored aria-current in the markup is the no-JS answer; this only ever moves it."* A
measured hint for a `fallback`, the only one of 14; still UNPROVEN as a field because the rule for
`fallback` is "prose or a JS-off render settles it", and this is neither.

**11 — L1 QUESTION 2 REPRODUCES ON THIS FIXTURE.** `_validate_screen.py dashboards/l2-fixture.html`
→ `receipt: ✅ 8 region(s)` then `compose: ❌ 98 hex colour(s) in <style>` (drive J). Composable or
provable, not both — unchanged, and now measured twice.

**12 — THE REVIEW PAGE OVERFLOWED BY 67 px AT 390 ON ONE TOKEN.** `scrollWidth` 457 vs 390; the
element was a `<dd>` holding `arrows/Home/End/PageUp/PageDown(+Shift=year)/Enter/Escape,` (no break
opportunity). Fixed with `overflow-wrap:anywhere` on the prose; re-measured 390 == 390 in both themes.
Named because the T review's own note says a table was the last culprit — this time it was prose.

**13 — THE SCHEMA'S DISCRIMINATOR HAS A QUIET SIDE.** A typed object with `script` deleted is read as
LEGACY prose and stays green against the schema (schema arm, expected). The generator emits nothing
for it and the gate reports it UNPROVEN, so nothing false is asserted — but it is not red either. It
closes when the legacy branch is retired (question 3).

## RULING-SHAPED QUESTIONS

⛔ The three L1 questions are CARRIED, not re-put — they stand in the review page with the same
options and recommendations L1 gave (1: recommend advisory now, blocking by regeneration; 2:
recommend the composer projects theme values; 3: recommend keeping the dashboard rows). This lane's:

1. **The address grammar and its constraints.** (a) path + fragment — `knowledge/<path>.js` |
   `knowledge/snippets/<Slug>.reference.html#script`, one grammar with the receipt and the registry,
   `#script` = the component's OWN snippet's inline script(s) (finding 6); (b) node-id —
   `snippet:<file>#script`, the KG edge grammar, but a file address has no prefix and the receipt
   already uses paths. **Recommend (a)**, including the FOREIGN refusal.
2. **`partial`: one name or a list?** (a) singular now, widen later; (b) `string | string[] | null`
   today, by addition (the 20 are unaffected — all null); (c) rename `partials: []`. Measured need:
   9 of the 14 dataviz members carry 2–3. **Recommend (b)**; the dataviz migration is then ~2K tokens
   and mechanical.
3. **When does a PROSE `behaviour` start blocking?** Today: one UNPROVEN line, never red. **Recommend:
   block a meta whose `behaviour` key is still prose on the day the 20 are written** (0 would go red
   then; one flag, ~300 tokens); metas with NO `behaviour` key stay UNPROVEN until rC Q3 and the
   dataviz migration settle what "none" means. (The schema's legacy branch retires on the same word.)
4. **`events` — wanted at all (rC Q3, still Dave's)?** Proposal: optional, measured never authored,
   floated. **Recommend keep, optional**; a generator can mint it from the snippet.
5. **The 14 candidate `fallback` readings — accept, reject, or render?** **Recommend the render**
   (a JS-off pass over the 14 snippets, rA's resilience criterion, ~3K tokens); promoting them on my
   reading alone is the brief's pitfall 2.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN: the 14 `fallback` values.** Nothing in the prose says what any interactive component does
  with JS off. Candidates are in `provenance` only. Price: a JS-off render of 14 snippets (~3K tokens
  with the runbook recipe already standing at this seat), or Dave's word per row.
- **UNPROVEN: the composed fixture page renders.** It is a gate fixture (spliced CSS from three
  snippets); never opened in a browser. Price: one render pass, ~1K tokens. Do not put it in front of
  Dave as a design.
- **UNPROVEN: the regen serial with the 20 applied.** `--check` → write → `--check` was driven on the
  fixture only; `_build_all.py` is forbidden to a sub and was not run, so the ORDERED serial (#210) with
  20 typed metas is unproven end to end. Price: the conductor's serial at apply time, ramp first,
  index last.
- **UNPROVEN: `_tests/test_gates.py`.** Not run — L1's ENOSPC precedent (`copytree` of
  `knowledge/assets`, 5.2 GB) and the same disk. What IS established: both touched modules pass their
  own `--selftest`, `gen_component_partials.py --check` is green on the live tree, and
  `_validate_screen.py` runs its full default population green on the fixture (drive L). Price: one
  CI run.
- **UNPROVEN: the `events` field's semantics.** rC Q3 is open; the values are measured listener names
  and nothing more is claimed of them.
- **CLAIMED — none.** Every figure above is from a probe in this window: the counts from
  `behaviour-migration.json` / `schema-arms.txt` / `drive-arms-summary.json` / the two selftest
  transcripts; the L1 figures quoted (7/7, offset 184, 191 hex) were RE-DRIVEN today (drives L, M, J —
  98 hex on the fixture, 191 on the dashboard was not re-run and is L1's number).

## PITFALLS (consequences replayed, Dave #165)

| # | what could go wrong | owner |
|---|---|---|
| 1 | A `#script` address rots when a snippet gains a second inline script: the resolved set grows and a page carrying one goes red with a named hint | snippet author; the generator's `--check` catches the drift |
| 2 | A re-indented copy of a script is RED by design (bytes are the key, s235-D1) — reads as friction to an agent that tidies | Dave (the key), not a bug |
| 3 | The L1 mint cannot splice a plain inline `<script>` — composed pages cannot carry the 14 receipted until `kind: script` lands | next L1-file lane, ~1K tk |
| 4 | The mint's `$scriptNote` becomes false for 20 snippets the day the metas are typed | next L1-file lane, ~500 tk |
| 5 | `partial` singular vs 2–3 per dataviz member — typing Chart-donut is impossible without question 2 | Dave |
| 6 | Applying the 20 puts 20 snippets out of sync until the generator runs — whole serial per wave, never `_build_all.py` from a sub | conductor at apply time |
| 7 | Candidate readings look like values; a copy-paste from the red-ruled box into a meta is the "likeliest reading" defect | whoever applies |
| 8 | Only receipted pages reach step 4b — until L1 Q1 flips, the population under this gate is one fixture and one dashboard; a gate that is not a consumer of every commit is not a gate | Dave (blocking date) |
| 9 | The generator now imports the gate at module level; a pack that ships the generator without `_validate_receipt.py` (or `_htmlmask.py`) breaks at import — same dependency shape the mint already has | pack manifest (`_gen_pack_manifest.py`) at the 1.0.6 cut |
| 10 | `snippet_file()` / `meta_path_for()` scan a directory per region — fine at 12 regions, worth a cache at 100 | whoever meets it; ~200 tk |

## Evidence

`notes/_subreports/assets/2026-09-02-238-B-L2-behaviour-address/`

| file | proves |
|---|---|
| `behaviour.schema.fragment.json` · `meta.schema.proposed.json` · `meta.schema.proposed.diff` · `apply_schema.py` | deliverable 1 — the fragment, the applied copy, the two-hunk diff, the refusing applier |
| `schema_arms.py` → `schema-arms.txt` | 136/136 live + 20/20 proposals pass; 15 red / 6 green arms |
| `build_migration.py` → `behaviour-migration.json` | deliverable 2 — the 20, with basis, quote/probe, candidates OUTSIDE `proposed` |
| `build_review.py` → `_REVIEW-…-v1.html` (repo root) · `render-{light,dark}-{1440,390}-*.png` (12) | deliverable 3; overflow measured 0 at both widths, both themes |
| `fixture_build.py` → `fixture-build.txt` | the fixture: schema applied, 20 typed, 136/136 valid, 20 out-of-sync → 20 injected → OK, block BESIDE the manifest, page composed + re-minted |
| `drive_arms.py` → `drive-A…I-*.txt`, `drive-arms-summary.json` | the brief's PRESENT / ABSENT / WRONG arms + 9 more, 12/12; each transcript carries command, output, rc, expectation, verdict |
| `drive-J-chain-validate-screen.txt` · `drive-K-chain-absent-blocks.txt` · `drive-L-chain-default-population-on-fixture.txt` | the chained entry inherits 4b (green, then blocking); the 7-screen default population still PASS |
| `drive-0-live-regen-v2-unchanged.txt` · `drive-M-l1-mutate-still-bites.txt` | the live dashboard: same 12 greens + notes + 1 UNPROVEN; L1's one-byte mutation still reds at offset 184 |
| `selftest-validate-receipt.txt` (35 arms) · `selftest-validate-receipt-mutants.txt` (10 mutants) | the gate's arms, and that each arm can fail |
| `selftest-gen-component-partials.txt` · `selftest-gen-component-partials-mutants.txt` (4 mutants) | the generator's arm 5i, and that it can fail |

**I READ the L1 REPLAY-THESE line** (`notes/_subreports/2026-09-02-235-L1-receipt-gate.md`): the
gate docstring lines 2–113 (the shape, the hashed-bytes definition, the exit codes — 4b is written in
that register and under that heading), finding 7 + question 1 (the ratchet — copied as the posture
for PROSE metas), `drive-3-one-byte-mutation.txt` (re-driven as drive M), the pack-cut UNPROVEN (still
open; a typed address does not change it), and `_validate_screen.py` 24–35 / 54–74 (why 4b needed no
change there). Also read: rC findings 11–12 and questions 2/3/5 (the CEM `events` shape, the Code
Connect `<script>` idiom, rule 2a beside rule 2); `s237-D10` (frozen mechanical suite AFTER L2 lands —
the drive arms are the shape of that suite); `_validate_behaviour.py` lines 1–25 (no external
`<script src>` on members — why `address_loaded` accepts inline first).

REPLAY-THESE: `_REVIEW-L2-behaviour-address-2026-09-02-v1.html` §§ 02 "The shape" and 06 "This lane's questions" (~1,800 tk) · finding 6 + drive-D above, the FOREIGN hole and its closure (~400 tk) · `behaviour-migration.json` items `date-picker` and `badge` — one scripted, one passive, to see a full provenance block (~900 tk) · finding 7/8, the two L1-mint residuals that bite before any page can carry the 14 (~350 tk) · `knowledge/_validate_receipt.py` docstring lines 82–113 (4b, the two-sided check) (~600 tk)
