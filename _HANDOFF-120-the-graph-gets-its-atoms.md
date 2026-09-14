# HANDOFF #120 — #269 → #270 — THE GRAPH GETS ITS ATOMS

> ⚠ **This file is NEWER than `_CHAIN.md` and therefore OUTRANKS it.** Read it first, then the chain.
> Written by the #269 conductor (Fable) at FILL 374,074 real — BEFORE the ritual ran, so that nothing
> in it depends on a delegated wrap remembering it. Dave's word at the seam: *"be carful I don't want
> any context lost or any mistakes in the next lane, 374,074 is quite a bust, this makes me nervous,
> typically this is where things get squirrely."* Every claim below is a receipt you can probe.

---

## ⛔ READ THIS FIRST, IN THIS ORDER

1. **This file.**
2. **`_CHAIN.md`** — the whole contract. Do NOT open `GOOD-MORNING.md` "to check".
3. **`_PROPOSAL-kg-entity-and-edge-gaps-2026-09-14-v1.html`** — the page #270 builds from. Its six
   decisions are ACCEPTED (below). Its lane evidence: `notes/_lanes/269/kg-gaps/{A-inventory,
   B-component-edges,C-external,V-verify}.json`.
4. **`python3 knowledge/_parked.py --check`** — nine parked items with tripwires. Never re-ask them.
5. **`_CARRIES.md § residual → #270`** only when you need a body.

★★★ **STALE MOUNT CHECK before acting:** `git log --oneline -3` vs `ls -la --time-style=full-iso
_CHAIN.md` — if the newest commit is newer than the chain, your mount is stale; stop and re-read.

---

## ⛔⛔ DAVE'S — HIS WORDS, VERBATIM. THE WRAP INSCRIBES; NOBODY RE-WORDS.

**A. The six KG-gap recommendations are ACCEPTED** (2026-09-14): *"I think your recommendations for
the 6 look good, personas and JTBD is interesting but we don't have any we can rely on, could we
create placeholders, or create our own on the back of some research? I don't want to loose the idea.
We will be adding more, for example I'm trying to get hold of our CX principles."* — full text in
`notes/_lanes/269/kg-gaps/DAVE-RULINGS-2026-09-14.md`. Read as:

1. GO on the recommended order 1–5: roles + DESK fields → 470 tagged rules → 145 principles + 22
   polarity edges → icons then logos → setIn / behaviourFrom / capturedFrom / acceptsCapability.
2. UX-principle prefix = `ux:` (`principle:` and `guideline:` are WCAG's — measured, `A-inventory.json`).
3. Tokens enter at TIER grain (semantic vs primitive), never 932 leaves.
4. Photography node = the MANIFEST ROW (original + derivative as attributes).
5. Metas cite principles: the six A-grade laws first.
6. New entity kinds now: content standard + lifecycle status. Persona/JTBD NOT dropped → `P-269-9`.

**B. Spelling in a quote** (2026-09-13): *"obviously this should be corrected, I have very dyslexic
fingers as well as my very bad spelling brain"* — `_quote_gate.py` treats a corrected spelling as
his words; a changed word or digit still misses.

**C. The audience phrase** (2026-09-13): *"an operator not a platform owner" is the original phrase I
think* — restored in the run-of-show and demo-prep (`6fd65b4`).

**D. The n-gram build** (2026-09-13): *"as long as it's safe and you test the usual dependancies and
externalities lets go for it"* + *"we are well behind pace so you can be really thorough and use
fable level judgment liberally"* — the doors were built under that word.

**E. Tripwires** (2026-09-13): *"store them for future sake, can they be triggered, or can we have a
hook so they don't get missed at the appropriate time"* and (09-14) *"okay we need this recorded
with tripwires"* — `knowledge/_parked.json` + `_parked.py` exist under that word.

**F. Still open from #119, untouched by #269 — DO NOT RULE:** the ask (deck card 10 DRAFT) · title
edges keep/strike · the date v1.0.6 went to designers · dream pass 12's four proposals · pre-bake
real-page drive as a STEP · fly-through direction · v1.0.13 hand-over date · the six-month comparator.
The meeting has slipped: *"the meeting is probably not going to happen this week"*; Dave is thinking
about the presentation *"offline with a pen and paper"*.

**G. The compose-time door — ASKED, NOT ANSWERED.** I proposed a third door on the retrieval spine:
task in → closed context slice out (components providing the roles, BLOCKING rules first, type
composites, icons, tokens, anti-neighbours, the ruling behind each), the generate skill's step 1
becoming "ask the graph" instead of "read the metas", and the gates checking the page against the
same slice. His last words on it were the heat question, not a yes. **#270 asks for the one word
before drafting it.**

---

## WHAT #269 DID — RECEIPTS

**Session #269 opened 2026-09-13 (Sun) and wrapped 2026-09-14 (Mon). MULTI-DAY. 9 commits
`f02fe4c..33b709d` + the wrap. Pushed to `814344e` on his word ("okay push"); `a8ff567` and `33b709d`
were NOT pushed at write time — the push is his word.**

### ① n-gram research → three read-only ADVISORY doors (Sun)
- `_RESEARCH-ngram-lookups-2026-09-13-v1.html` — six uses measured on the live index.
- `knowledge/_quote_gate.py "<phrase>"` / `--file <page>` — verbatim lookup over the Memento index;
  FOUND with id·file:line, or nearest phrase + longest common run + did-you-mean; spelling-corrected
  = his words (B). 14 bites. Day-one catches: run-of-show "research"≠"resaech", "designer"≠"platform
  owner" (both ruled, B/C).
- `knowledge/_near_dupes.py` — 8-word shingle Jaccard; 22 pairs ≥0.5; ONE EXACT DUPLICATE
  `_GM-ARCHIVE.md:4940` = `:6133` (dream-pass candidate, `P-269-4`).
- `knowledge/_ngram.py` — library, 11 bites. `_RUNBOOK-consult.md` § n-gram doors appended.
- ⛔ `_search_core.py` / `_memento_search.py` are PINNED byte-identical to the memento-package by
  `_validate_package_delta.py` — any ranking change is a RELEASE (`P-269-1/2`). Pack untouched.

### ② PARKED WITH A TRIPWIRE (Sun/Mon)
- `knowledge/_parked.json` (9 rows, P-269-1..9) + `knowledge/_parked.py` (`--check` / `--due <event>`
  / `--list` / `--selftest` 10 bites). Events: release-cut · kg-edge-gen · dream-pass · memento-cut ·
  token-report · guidelines-ingest. Hooks (print-only, try/except, never a verdict):
  `_release/_gate_release_audit.py --check`, `gen_kg_edges.py` main, `_validate_package_delta.py`
  main, `tokens/_build_blast_radius.py` main, `_RUNBOOK-dream-pass.md` step 7b.
- Driven: a v1.0.14 manifest fires 3. `P-269-8`'s `at_commit` pinned to `45a62c3` so its own fix
  doesn't trip it.
- Graph-engineering table (research 2026-08-05 v2) audited: 1 done (#115) · 2 mark done, DEMOTE
  RETIRED `s124-D1` · 3 done (`_RUNBOOK-external-claims.md`) · 4 → `P-269-6` · 5 type-half done,
  token-half → `P-269-7` · 6 → `P-269-8`. `_STATE-MACHINE-TARGET.md` §9 generator ⬜ → PARTIAL.

### ③ KG gaps proposal (Mon) — 4 Opus lanes, ~510K sub tokens, ALL READ-ONLY
- Graph today: 890 nodes / 1,267 edges (16 types) + governance & WCAG families 1,941 / 3,605.
- 13 families at ZERO: tokens 932 · icons 666 · tagged rules 470 (`_rules-index.json`, consumed by
  `_build_consult_index.py:53` + `_build_instrument_fit.py:60` — NOT orphaned) · untagged docs 25/381
  headings · principles 145 · polarities 30 · logos 12 · photos 251 (KG-NOTE stale: says 12
  derivatives, folder has 251) · fonts 111 (NO manifest) · roles 12 (81/108 `when`) · DESK fields ·
  synonyms 69 · personas 0.
- 12 candidate edge types (closed vocabulary #75 — proposals only). conformsTo = near-dup of
  appliesTo (826/834). usesIcon 19 (lane said 4).
- Verifier: 65 counts, 53 exact, 12 corrected on the page; 133 evidence lines, 0 fabricated.
- ⛔ Nothing touched a meta, generator or the graph. `gen_kg_edges.py` NOT run (fenced).

---

## #270 — THE FIRST TWO LANES (when he says go)

1. **Roles + DESK fields into the graph** — `roles.json` providers (generate from the METAS, the ruled
   canon, never from roles.json — two homes drift), `provides`/`answers`/`shape`/`when` from
   `shapes.json` / `chart-intents.json` / `when-fields.json`. New node kinds `role:`, `intent:`,
   `shape:`; edge types providesRole / answersIntent / hasDataShape / yieldsTo. ⛔ A new edge type is
   a vocabulary change (#75) — the lane PROPOSES the schema diff, Dave ratifies, then it lands.
   `_validate_kg.py` must stay green; `_build_kg_explorer.py` regen; `_kg_history.py` after.
2. **The compose-time door** — only after his one word (G).

**Standing cautions for any #270 lane:** `model: opus`; verifier in the same wave; lane fragments in
`notes/_lanes/270/`; `_checkin.py` every ~10 turns; art-director screenshot + text diff before
presenting; `.git/index.lock` needs `allow_cowork_file_delete`; disk `/sessions` at 95.5% — run
`_gate_scratch_hygiene.py`; never `git stash`; never `gen_kg_edges.py`.

---

## STRUCTURAL REDS SEEN AT THE SEAM (from `_checkin.py`, for the wrap to heal, NOT to hide)
- Memento index stale vs GM/LS → rebuild + stage (ritual 2g).
- Boot-ceiling breach carried from #265–#267 — SHRINK-ONLY (`s240-D2`/`s241-D1`); not a wrap's to raise.
- Boot double-count in `notes/_GAUGE-LOG.md` for #243 (lines 2826/3256) and #264 (3206/3208).
- MEMORY.md over cap (3,573 vs 1,802 tape) — ADVISORY; Dave's stub rule (#242) governs.
- Uncommitted at seam: `notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl`.

**Gauge for the wrap block:** boot 78,777 real · peak FILL 374,074 real (turn 129) · throughput
1,429,640 cl100k · delegated subs ≈510K tokens across 4 lanes (A 110,564 · B 141,425 · C 119,685 ·
V 140,753).
