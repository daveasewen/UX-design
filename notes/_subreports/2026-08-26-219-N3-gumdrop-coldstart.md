provenance: #219 lane N3 · 2026-08-26 · rulings `s219-D4` · `s219-D5` (Q1, Q4) · `s219-D8`
status: filed

# `#219`-N3 — the Memento — Gumdrop cold start: empty stores, the guided first chat, the VS Code runbooks

session: `#219` · 2026-08-26
window: lane N3 (Apollo — Spider release, crank wave)
sub index: `N3`
brief: `notes/_briefs/2026-08-25-219-crank-divvy.md`
base commit: `aa74faa` (clean tree at start)
tokens: `UNMEASURED` — no `message.usage` reader is reachable from a sub window; this lane's
spend must be read from the conductor's own panel.

## VERDICT

**DONE, and the walk found the release's biggest defect.** All six regions are enacted. The
Gumdrop cut now ships two empty, well-formed stores whose machinery was *driven* against the
empty shape rather than inspected; a starter `_CHAIN.md` that is self-identifying and is
replaced by the first wrap; a guided `FIRST-SESSION.md`; a pack-root
`.github/copilot-instructions.md` extending the memento-package precedent; and the capture-ritual
and context-gauge runbooks rewritten for VS Code + Copilot, honest about what cannot be measured
there. The first session was walked twice, literally, in staged packs — **walk 2 is green end to
end on a clean stage with no hand-holding.**

⛔ **The headline is finding 1: the packaged chain generator did not run at all.** Memento —
Gumdrop's central file, `_gen_chain.py`, died on `ModuleNotFoundError` and then on
`AttributeError` the moment a designer reached step 4 of any first session — and the
`memento-package` delta gate was **green** throughout, because it proves the shim matches its own
docstring, not that its consumer can run. This is not a Spider defect: `memento-package v0.1.1`,
already released, is broken the same way and has been since #193. Two at-cause fixes are in the
tree; the released package needs a re-cut, which is the conductor's call.

COUNTS: findings 9 · ruling-shaped 5 · UNPROVEN 3

## What was done

### Region 1 — empty stores (Q1)

- `apollo-spider/gumdrop/_state.json` — empty task store, `schema 1`, `items: []`, with a
  plain-words `_README` written for someone who has never seen it.
- `apollo-spider/gumdrop/_rulings.json` — empty rulings store, `rulings: []`, same treatment.
- `apollo-spider/gumdrop/_state.py`, `_inscribe_ruling.py`, `_governs.py`, `_helpgate.py` —
  copies of the repo originals, byte-identical, so the stores have their sanctioned writers.
- `apollo-spider/gumdrop/machinery/_could_not_ask.py` — the missing dependency (finding 1).
- `apollo-spider/gumdrop/_GUMDROP-MANIFEST.md` — provenance for every copy, why each file lands
  where it lands, the measured store verdicts, and what is owed.
- `apollo-spider/gumdrop/_CHAIN.md` — the starter chain. It carries a machine-detectable marker
  (`<!-- MEMENTO-STARTER-CHAIN:`) on line 1 so the boot rule can tell it from a real record.

**Every store was DRIVEN against the empty shape, not read:**

| probe | verdict |
|---|---|
| `_state.py` bare, empty store | exit 0, zero counts, no notes |
| `_state.py --selftest` inside the pack | 57 bites, all GREEN |
| `_inscribe_ruling.py --dry-run`, first entry | accepted, reconstruction proof PASSED |
| `_inscribe_ruling.py --write`, first entry | inscribed, 0 → 1, all other bytes identical |
| `_inscribe_ruling.py --selftest` inside the pack | runs; **3 arms declared UNMEASURED** (finding 4) |

### Region 2 — the guided first chat (Q1)

- `apollo-spider/FIRST-SESSION.md` — the walkthrough. What Memento is in three sentences with
  Dave's tattoos/Polaroids framing used gently and once; then build something small, first
  capture, first ruling through the machinery with every field explained, first wrap, come back
  tomorrow. Ends with a where-to-next table and a "if something goes wrong" note.
- Voice: guided, warm, second person, no house jargon, no ruling ids, no session numbers, no
  internal history. Where an Apollo-ism is unavoidable in the machinery (finding 5) the document
  says so plainly rather than hiding it.

### Region 3 — customised runbooks (Q4)

- `apollo-spider/gumdrop/runbooks/_RUNBOOK-capture-ritual.md`
- `apollo-spider/gumdrop/runbooks/_RUNBOOK-context-gauge.md`

Method kept, harness stripped. The capture runbook keeps *capture at wrap*, the close-condition
refusal, the never-hand-edit rules, the "declared gap passes, silent fails" asymmetry, and the
five-step sequence; it drops Apollo's step numbering, its section growth contracts, its archive
roll rules and its enforcing gate, and says honestly that the gate is not in the pack and what
the substitute is. The gauge runbook keeps **throttle not thermometer**, price-the-job-first,
the-wrap-is-inside-the-price, the three postures and their behaviours, and the two-tier trigger;
it drops every ruled number, because those are constants measured for a different environment.

⛔ **The gauge's honest degradation is stated as its own section.** Copilot exposes no token
count to itself and the API-key machinery does not ship, so the runbook declares the gap and
gives the estimate-tier vocabulary — `measured` / `estimated` / `unknown` — with an explicit ban
on reporting an estimate as a measurement.

The repo's own runbooks were **not modified**. `git status` confirms neither
`knowledge/_RUNBOOK-capture-ritual.md` nor `knowledge/_RUNBOOK-context-gauge.md` is touched.

### Region 4 — the Copilot dialect check

See finding 6. The five R3 skills were **not rewritten**; a bridge was added:
`apollo-spider/.github/copilot-instructions.md` (indexes them with trigger phrases) and five
one-screen shims at `apollo-spider/.github/prompts/*.prompt.md` making each a slash command.

### Region 5 — the walk

Walked twice, in staged packs built through the generator's **own** `apply_seed_map()` and
`flatten_stage()` — never a hand-rolled imitation of the layout.

- Walk 1 (`/var/tmp/spider-walk/`) — found findings 1, 2, 3 and 8; three steps failed.
- Walk 2 (`/var/tmp/spider-walk2/`) — clean stage, corrected instructions, **every step green**:
  pre-flight, dry-run, write, worklist add, both state files, chain regenerate, chain `--check`.

### Region 6 — the manifest

- **Group decided: a new `gumdrop` group**, declared in the generator with its reasoning. Not
  folded into `memento-clean-cut`, because that group's cards say *"machinery only, no record"* —
  which `s219-D5(Q1)` has made false for this cut, and hiding the change inside a card stating
  the opposite is how a release ships a contradiction.
- **A seed map was added** (`SEED_PREFIXES`, `apply_seed_map()`), mapping
  `apollo-spider/gumdrop/` → `memento-package/` in the pack. See finding 3 — the placement is a
  measurement, not a preference. `pack_path()` remains the one function both the stager and
  `--check` read.
- `knowledge/_release/_pack_manifest.json` was **not hand-edited**. Manifest + probe + page regen
  is the seam's.
- Generator selftest: **149 bites, 0 fails** (was ~135; the new bites drive the seed map on a
  real stage, including its collision refusal).

## Findings

**1. ⛔ THE PACKAGED CHAIN GENERATOR DID NOT RUN. Two separate breaks, both live in the released
`memento-package v0.1.1`.**

Probe — walk 1, step 4c, in the staged pack:

```
python3 memento-package/machinery/_gen_chain.py
  ModuleNotFoundError: No module named '_could_not_ask'
```
then, after supplying it:
```
  AttributeError: module '_capture_gate' has no attribute 'measurement_tier'
```

*(a)* `_gen_chain.py` has imported `_could_not_ask` since the #193 re-sync. That module was never
copied into `memento-package/machinery/`, and `_gen_chain.py` does `sys.path.insert(0, HERE)`, so
the copy at `knowledge/_could_not_ask.py` — which the pack *does* ship — is unreachable from it.

*(b)* `_gen_chain.py` calls `cg.measurement_tier()`. The four-function shim never ported it.
Measured: `grep -oE 'cg\.[a-zA-Z_]+'` over the packaged `_gen_chain.py` returns five names;
the shim provides four of them.

**Fixes at cause, both in the tree:** `_could_not_ask.py` copied into the Gumdrop cut;
`measurement_tier` ported verbatim into **both** shim copies with its provenance declared in the
shim docstring. `_validate_package_delta.py` is green afterwards, including cross-copy identity.

**2. ⛔ THE DELTA GATE CANNOT SEE THIS CLASS, AND SAID GREEN THROUGHOUT.**

`_validate_package_delta.py` arm 2 checks the shim's **declared provenance** — the functions its
own docstring says it ported — by AST source-segment hashing. It never asks the only question
that matters: *does the consumer run?* So a shim can be perfectly faithful to its docstring while
the module that imports it is dead on arrival, and the gate reports success.

This is [[mutation-tests-the-clause-not-the-feature]] and [[green-tests-cannot-see-scope]] in the
same file: the gate proves the copy matches, never that the package works. The missing arm is a
one-line import probe — `python3 -c "import _gen_chain"` in an isolated copy of each machinery
folder — which would have caught both halves of finding 1 the day they landed. **Not built: it
widens a gate's scope, which is a decision.** Priced at ruling-shaped question 1.

**3. THE GUMDROP CUT'S PLACEMENT IS A MEASUREMENT, NOT A PREFERENCE.**

Every Memento module resolves its homes from where the file sits. Measured, both ways:

| module | resolves | so it must sit |
|---|---|---|
| `machinery/_gen_chain.py` | `_CHAIN.md` into its own grandparent | chain root = `memento-package/` |
| `_state.py` | `_state.json` from its own dir; `home` against the parent | one level above `machinery/` |
| `_inscribe_ruling.py` | `_rulings.json` from its own dir | one level above `machinery/` |
| `_governs.py` | an evidence PATH against its own grandparent | one level above `machinery/` |

Put the record machinery inside `machinery/` and `_governs.REPO` becomes `memento-package/`, so a
designer's ruling citing a real file (`knowledge/tokens/…`, `showroom/…`) is refused as *path
does not exist*. Measured before the seed map was written, which is why the seed map exists.

**4. THE EMPTY STORE WAS ILLEGAL ON ARRIVAL, AND THE SANCTIONED WRITER WAS THE THING THAT COULD
NOT WRITE IT.**

`_inscribe_ruling.compose()` spliced a new entry after `head.rindex("}")`. An empty
`"rulings": []` has no preceding `}` — `ValueError: substring not found`. So the one file allowed
to write a project's *first* ruling could not, and the empty store `s219-D5(Q1)` ships would have
been dead on the designer's first wrap. Exactly the brief's warning: *an empty store that the
tooling refuses is worse than none.*

⚠ **And the old line was latently wrong even when it worked.** `rindex` searched the whole head,
so on any store whose pre-`rulings` keys contain an object — a dict `_README`, a `meta` block —
it would have spliced the entry **outside** the array, with only the R3 parse check between that
and a corrupted store. The insertion point is now derived from the array's own `[`, structurally,
in both arms.

Two further at-cause fixes to the same file and to `_state.py`, both found the same way:

- Their selftest **fixtures addressed Apollo repo paths** (`knowledge/_GOVERNING-RECORDS.md`,
  `knowledge/_inscribe_ruling.py`), which resolve only inside this repo. Run from a shipped pack
  they reported the *environment* as a store defect — [[gate-cannot-pass-in-one-environment]].
  Both fixtures are now derived from the module's own location. This also retires a home-pointer
  rot risk (#167): the typed path would have gone stale on any rename.
- `_inscribe_ruling.selftest` **crashed** on an empty store (`["rulings"][-1]` → `IndexError`) —
  a crash, not a fail [[a-crash-is-not-a-fail]]. `_tmp_copy()` now plants a seed ruling when the
  store it copies is empty, in one place, which also makes every call an implicit control on the
  empty-array insertion path.
- Three arms genuinely need Apollo's rolling files or a store with real history. They now
  **declare UNMEASURED** in the module's own honest vocabulary rather than failing for the wrong
  reason — [[refusal-names-the-first-obstacle]]. *Unmeasured is not a pass*, and the runbook says
  so and points designers at `--dry-run` as the check that is honest in their environment.

Repo-side after all four: `_inscribe_ruling --selftest` green, `_state --selftest` 57 bites green,
`knowledge/_rulings.json` **untouched** (`git status --porcelain` empty for it).

**5. THE COLD START OPENED WITH THIS REPO'S HISTORY AND DAVE'S NAME.**

Measured — `python3 memento-package/_state.py` on the shipped empty store, before the fix:

```
⚠ real-input coverage: 0 of 0 live item(s) … The fields exist and are gated; only Dave may fill them.
⚠ legacy ids retired since birth: W-0b, W-0c, W-0d, W-01, … W-16 (frozen set may shrink; …)
```

On an empty store every legacy id is trivially "retired" and the coverage note reads *0 of 0*. A
note that fires when there is nothing to measure is decoration, not a measurement — the same
argument the project-split note one line above already makes. Both are now guarded on `items` /
`live_n`. **Inside Apollo both still fire exactly as before** (verified: the live run still
prints all four notes). The cold start now reads three lines of zeroes and nothing else.

⚠ **This only fixes the empty case.** The moment a designer adds one item, `project split … the
values written at #172 are DEFAULTS proposed for Dave's eye` and the legacy-id list return. See
ruling-shaped question 2.

**6. THE FIVE SKILLS ARE INERT IN VS CODE UNTIL SOMETHING INDEXES THEM.**

R3's `SKILL.md` files use the Anthropic frontmatter shape (`name` + `description`). GitHub
Copilot in VS Code does not discover `skills/*/SKILL.md`. Its mechanisms are
`.github/copilot-instructions.md` (auto-loaded workspace-wide),
`.github/instructions/*.instructions.md` (path-scoped via an `applyTo` glob),
`.github/prompts/*.prompt.md` (user-invoked slash commands) and `AGENTS.md`.

Left alone, a designer unzips the pack and the five skills never fire — R3's own consequence note
about the pack layout applies verbatim here: *"a silent failure of the whole release."*

**The bridge, built, skills untouched:**

- `apollo-spider/.github/copilot-instructions.md` carries a trigger-phrase table naming each
  `SKILL.md` by path, with the instruction ⚠ *these are not auto-loaded — open the file and
  follow it*, and the `check-with-gates` / `check-against-design-system` pairing spelled out.
- `apollo-spider/.github/prompts/<skill>.prompt.md` ×5, `mode: agent`, each a thin shim that
  tells Copilot to read the corresponding `SKILL.md` and follow it, with `${input}` passed
  through. This makes `/generate-from-canon` and friends work as native slash commands.

The manifest group claims `apollo-spider/.github/` whole rather than the one instructions file,
so half a bridge cannot ship.

**7. THE COPILOT BOOT RULE NEEDED A THIRD ARM.**

memento-package's precedent has two: *a chain exists* / *no chain exists*. Shipping a starter
chain breaks it — arm 1 would fire and Copilot would summarise a shipped file back to the
designer as though it were their project's record. The starter chain therefore carries a
machine-detectable marker on line 1 and the instructions open with **Arm 0**: if the marker is
still there, nobody has used this pack; orient, point at `FIRST-SESSION.md`, ask what they want
to build, and ⛔ *do not treat the starter chain as a real record*. Verified in the walk: the
marker is present in the shipped file and absent after the first regeneration.

**8. THE GENERATED CHAIN IS WRITTEN IN APOLLO'S VOICE, AND ALWAYS WILL BE.**

`_gen_chain.py`'s `BANNER` is a hardcoded string. Every chain any designer ever generates
therefore carries, verbatim:

- `GM-D7-am names (CUT #33 on Dave's ruling)` — internal ruling ids and Dave's name;
- `five sessions called the chain CUT and every one of them paid full price` — this repo's history;
- `python3 knowledge/_memento_search.py "<q>"` — **a path that does not exist in the pack**;
- `QUEUE — gm:C1 strands · gm:C2 ruling batch (Dave's) · gm:C4 enact-queue`;
- on a small first chain, `-81% of it is retrieval surface` — a negative percentage.

The designer's own words come through correctly between the markers; the wrapper around them is
scenery from another project. **Not fixed here:** the banner is Apollo's chain contract, the
packaged copies must stay byte-identical to it under the delta gate, and rewriting it is not a
lane decision. `FIRST-SESSION.md` warns the designer in one short paragraph as the interim.
Ruling-shaped question 3.

**9. A PRE-EXISTING DELTA RED WAS CLEARED AS A SIDE EFFECT — flag it at the seam.**

`_validate_package_delta.py` was red on arrival: both packaged `_gen_chain.py` copies were 35
lines behind `knowledge/_gen_chain.py`, all of it inside a selftest block another #219 lane
changed this session. Verified pre-existing: `git status --porcelain` showed neither
`knowledge/_gen_chain.py` nor either copy touched by this lane before the re-sync. The gate
demands verbatim copies, so both were re-synced with `cp`; the gate is green afterwards.

⚠ **If that lane edits `knowledge/_gen_chain.py` again after this report, the re-sync must be
repeated at the seam.** It is a `cp` ×2 plus one gate run.

## RULING-SHAPED QUESTIONS

1. **Should the delta gate gain a RUN arm?** Finding 2: the gate proves each copy matches its
   source and each shim matches its docstring, and it was green while the package was
   unrunnable. (a) Add a fifth arm that imports every entry point in an isolated copy of each
   machinery folder and fails on `ImportError` / `AttributeError` — perhaps 40 lines, and it
   would have caught both halves of finding 1 on the day. (b) Leave it; treat the pack walk as
   the check. **Recommend (a)** — the whole reason `memento-package` has a gate is that a copy
   silently regressed 54 lines and nobody noticed; this is the same class one level up, and
   `_gen_chain.py` has now been broken for roughly 26 sessions in a shipped release. It widens a
   gate's glob, so it is Dave's or the conductor's, not mine.

2. **`_state.py`'s vocabulary ships as Apollo's.** `project` is a closed enum of
   `apollo | memento`; `owner` is `dave | claude`; the notes cite `#172` and *"Dave's eye"*.
   `FIRST-SESSION.md` currently tells designers the honest truth — *these are ours, not yours,
   use `apollo` and `claude`* — which is warm but odd on day one. (a) Accept it for v1.0.0 and
   say so, as now. (b) Widen the enums to include a neutral value. (c) Make the enum
   configurable per project. The code itself says widening the enum is a RULING and that an
   agent must not pick a value while adding an item, so **this lane proposes nothing and
   recommends (a) for v1.0.0** with (c) as the next release's shape.

3. **The chain banner.** Finding 8. (a) Ship as-is with the one-paragraph warning already in
   `FIRST-SESSION.md`. (b) Parameterise `BANNER` in `_gen_chain.py` — a project name and the
   retrieval path read from a small config, defaulting to Apollo's exact current wording so this
   repo's chain is byte-unchanged. (c) Give Gumdrop its own banner, accepting a declared
   divergence from the verbatim set. **Recommend (b)**, and note the size: `BANNER` is quoted by
   this repo's own gates and by `_CHAIN.md`'s freshness comparison, so it is a careful change and
   not a wave-1 one. The broken retrieval path alone is arguably enough to make (a) untenable —
   it tells every designer to run a file that is not in their pack.

4. **`memento-package v0.1.1` is broken in the wild.** Finding 1 applies to the already-released
   package, not only to Spider. (a) Re-cut it as v0.1.2 from the fixed tree. (b) Leave it and let
   Spider carry the fix forward. **Recommend (a)** if it has actually been handed to anyone — a
   package whose headline feature crashes on first use is worse than no package — but who has it
   is not something this lane can see.

5. **Voice check on `FIRST-SESSION.md`, `.github/copilot-instructions.md` and the two runbooks.**
   These are taste, and they are the first thing a designer reads. Specifically: the
   tattoos/Polaroids paragraph is used **once**, early, in Dave's own framing, and stops before
   the mechanics; the walkthrough is second person and says *"you"* throughout; the gauge runbook
   keeps the ⛔ and ★ markers because they carry emphasis usefully, but drops every ruling id and
   session number. **All four are PROPOSED text Dave can strike or rewrite line by line.**

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN: no Copilot agent has actually been driven over this.** The dialect analysis
  (finding 6) is from Copilot's documented discovery mechanisms plus the memento-package
  precedent; the prompt-file frontmatter (`mode: agent`, `description`, `${input}`) is written to
  that shape but **has not been loaded by a real VS Code + Copilot session**. Price to prove: one
  designer, one unzipped pack, fifteen minutes — and it is the single highest-value check left
  before the bake, because everything in region 4 rests on it.
- **UNPROVEN: the pack has never been baked with these files in it.** The walk used stages built
  through the generator's own `apply_seed_map()` + `flatten_stage()`, which is the real mapping,
  but a `--stage` from a named commit needs the files committed first. Price: the seam's normal
  `--manifest` + `--dry-run` cycle. The seed map's collision refusal *is* driven, in the
  generator's selftest, on a real stage.
- **UNPROVEN: `ci-template/run-gates.py` was not run inside the walk.** It is cited by
  `FIRST-SESSION.md` and by the capture runbook as the post-mint check. Its verdict is region N1's
  and is not re-measured here. Price: one run in a full stage, a few minutes.
- **CLAIMED: the source-commit column in `_GUMDROP-MANIFEST.md`.** Two of the four rows name
  pre-#219 commits for files that carry uncommitted #219 changes. The manifest says so in its own
  ⚠ line and asks for a re-stamp at the landing commit.
- **CLAIMED (declared, not hidden): there is no delta gate over the four Gumdrop copies.**
  `_validate_package_delta.py` globs `memento-package/` only and by design does not touch
  `apollo-spider/`. The copies can drift from `knowledge/` silently — the exact defect that gate
  was built to end. Priced in `_GUMDROP-MANIFEST.md` under "Owed", not done, because it widens a
  gate's scope.

## Files this lane wrote

**New — the Gumdrop cold start (all under the new `gumdrop` manifest group):**

```
apollo-spider/FIRST-SESSION.md
apollo-spider/.github/copilot-instructions.md
apollo-spider/.github/prompts/{generate-from-canon,draft-a-new-pattern,
    check-against-design-system,check-with-gates,usability-review}.prompt.md
apollo-spider/gumdrop/_CHAIN.md
apollo-spider/gumdrop/_GUMDROP-MANIFEST.md
apollo-spider/gumdrop/_rulings.json          (EMPTY)
apollo-spider/gumdrop/_state.json            (EMPTY)
apollo-spider/gumdrop/{_helpgate,_governs,_inscribe_ruling,_state}.py   (copies)
apollo-spider/gumdrop/machinery/_could_not_ask.py                       (copy — finding 1)
apollo-spider/gumdrop/runbooks/_RUNBOOK-capture-ritual.md
apollo-spider/gumdrop/runbooks/_RUNBOOK-context-gauge.md
```

**Modified — at cause, in Apollo's own files:**

```
knowledge/_inscribe_ruling.py                compose() empty-array arm; three selftest fixes
knowledge/_state.py                          derived fixture home; two notes guarded on items
knowledge/_release/_gen_pack_manifest.py     SEED_PREFIXES + apply_seed_map(); `gumdrop` group;
                                             14 new selftest bites (149 total, 0 fail)
memento-package/machinery/_capture_gate.py           measurement_tier ported + declared
memento-package/claude-plugin/…/_capture_gate.py     same, byte-identical (arm 3)
memento-package/machinery/_gen_chain.py              re-synced verbatim (finding 9)
memento-package/claude-plugin/…/_gen_chain.py        same
```

**Not touched, verified by `git status`:** `knowledge/_rulings.json`, `GOOD-MORNING.md`,
`_CHAIN.md`, `_LIVE-STATE.md`, `knowledge/_release/_pack_manifest.json`, both repo runbooks,
`apollo-spider/skills/**`, `apollo-spider/build-designer-pack.sh`.

⚠ **One thing the seam must decide, flagged not done:** the pack README written by
`apollo-spider/build-designer-pack.sh` still says of `memento-package/` — *"Memento's machinery,
and only the machinery. No chain, no rulings, no record of any kind."* `s219-D5(Q1)` has made
that false. The README is generated by that script, and the script is region N1's surface, so
this lane did not edit it. **It must be corrected before the bake** or the pack ships a README
that contradicts its own contents.

## Evidence

No evidence files. Every claim above quotes its probe inline — the two walk stages were
throwaway (`/var/tmp/spider-walk`, `/var/tmp/spider-walk2`) and are reproducible in a few minutes
from the generator's own `apply_seed_map()` + `flatten_stage()`.

REPLAY-THESE: `apollo-spider/FIRST-SESSION.md` (~2,600 tk — it is the deliverable and it is
PROPOSED text) · ruling-shaped question 1, the delta gate's missing RUN arm (~400 tk — it is the
finding most likely to recur) · `notes/_subreports/2026-08-26-219-N3-gumdrop-coldstart.md`
finding 1 + finding 9 (~900 tk — the released package is affected and the re-sync may need
repeating at the seam)
