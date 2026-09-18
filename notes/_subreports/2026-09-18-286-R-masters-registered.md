# #286 lane R — the masters were NOT registered, and the generator is why

**Verdict: NOTHING LANDED. `gen_kg_icons.py --land` was NOT run.** The fence Dave released is
released; the tool behind it **cannot do the job it was released for**, and running it would have
**destroyed hand-authored state** while adding **zero** master nodes. That was established
**before** any write, by the generator's own `--dry-run` — so there was nothing to revert.

⛔ **A wrong registration is worse than an open row.** Row `W-285lm` stays **open**.

---

## 1. The sanction, and exactly how far it reaches

Dave, 2026-09-18, verbatim, to an opener whose item 2 was *"How the accepted masters get
registered — the icon generator is fenced, and running it is your call"*:

> *"okay go on everything"*

Receipt: `notes/_lanes/286/DAVE-RULINGS-2026-09-18.md` (lane S), which reads it as releasing the
fence and adds, in its own words: *"HOW the registration is shaped is a lane's mechanics, not a
second ruling of his"* — and, under **Still his**: *"The shape of the master registration in
`_logo_nodes.json`, if he wants a say in it beyond releasing the fence."*

⚠ The sanction is **permission to run**, not a claim that running achieves registration. The
measurement below shows the second thing is false, so the permission was not spent.

---

## 2. What the generator reads and writes (established BEFORE running)

`notes/_lanes/277/icons-propose/gen_kg_icons.py` — 1643 lines. There is no `argparse`; `--help` is
served by a help-gate that prints the module docstring. Modes, from the docstring's own Usage block
and `main()` (`:1593`):

| mode | effect |
|---|---|
| **default / `--dry-run <dir>`** | **DRY RUN IS THE DEFAULT.** Writes `_icon_nodes.json`, `_logo_nodes.json`, `dry-run.json` into the named dir **and nothing else**. |
| `--land --ratified <id>` | Writes **`knowledge/_icon_nodes.json`** and **`knowledge/_logo_nodes.json`**. Refuses unless the id is in `RATIFIES = ("s277-D4","s277-D5","s277-D6","s277-D7")` **and** recorded in `knowledge/_rulings.json`. |
| `--prose-count`, `--selftest`, `--icons-only`, `--no-logos`, `--no-usesicon`, `--corpus <dir>` | measurement / scope options |

So the **two** files a `--land` would write are `knowledge/_icon_nodes.json` and
`knowledge/_logo_nodes.json`. A dry-run mode exists and it is the default — it was used.

### BEFORE hashes (sha256) and counts

```
9409c60144e464922d127e051484446eae3693106e8d3b2b10ab6fbacdace072  knowledge/_logo_nodes.json   19,038 B
5bc419187774b1a4f9ed8df7d36cfc982db80fb33788a675ace8370ad87f6bc7  knowledge/_icon_nodes.json
918452e676d49b8772ee27c10d3473da35ab2a6f9d305c00f48044f0fc96016e  knowledge/_state.json
```

`_logo_nodes.json` BEFORE: **8 nodes · 33 edges**, `ratified: "s277-D4"`, top-level keys
`$description, $s282-D5, $unresolved, edge_types, edges, family, generated_by, nodes, ratified,
unresolved`. The 8 nodes are the 8 top-level lockups (`hexagon-*` ×4, `masterbrand-*` ×4).

`git status --short` at lane open (no `git stash list` used):

```
 M notes/_REHEARSAL-LOG.jsonl
 M notes/_dream/_GRADE-DECISIONS.jsonl
```

(Other lanes' edits to `knowledge/_gauge_tokens.py`, `knowledge/_standing.md`,
`knowledge/_capture_gate.py`, `knowledge/_state.json` appeared during the run; none are mine except
the `_state.json` row body in §5.)

---

## 3. ⛔ THE FINDING — the generator cannot see the masters

**`gen_kg_icons.py:278`:**

```python
def logo_stems(corpus=None):
    return sorted(Path(p).stem for p in glob.glob(str(_k(corpus) / "assets" / "logos" / "*.svg")))
```

**`*.svg`, not `**/*.svg`, and no `recursive=True`.** The glob is **non-recursive**. Compare
`icons_on_disk()` twelve lines above it, which *does* use `"**" / "*.svg"` with `recursive=True` —
the asymmetry is in the source, not in my reading of it.

Measured on the live tree:

```
svgs at knowledge/assets/logos/*.svg        :  8
svgs at knowledge/assets/logos/**/*.svg     : 48   (8 lockups + 40 masters)
```

The 40 accepted masters live in **`knowledge/assets/logos/masters/`**. They are **invisible** to the
generator. Corroborating: **the string `master` does not appear anywhere in the 1643 lines** of
`gen_kg_icons.py` — there is no size/height concept in the file at all. `logo:<stem>` is parsed as
*lockup × theme × colourMode*; there is no fourth axis.

### The dry run (the generator's own default mode), run into this lane

```
python3 notes/_lanes/277/icons-propose/gen_kg_icons.py --dry-run notes/_lanes/286/R/dryrun
```
exit 0, stderr empty. stdout (`notes/_lanes/286/R/dryrun-stdout.txt`):

```
DRY RUN — 666 icon records · 10 groups · 8 logos  ->  684 nodes · 1321 edges
  nodes: {'iconGroup': 10, 'icon': 666, 'logo': 8}
```

⬛ **`8 logos` → `logo: 8`.** A `--land` would register **0** of the 40 masters. Not 40, not 20.
Zero. The task's acceptable outcome ("the 40 masters, or the 20 masterbrand ones") **is not
reachable by this generator in its current form.**

---

## 4. Structured diff — what `--land` WOULD have done (predicted, not performed)

Both files parsed as JSON and compared (`notes/_lanes/286/R/predicted-diff.txt`).

**Nodes — the whole point of the exercise:**

| | |
|---|---|
| nodes added | **0** |
| nodes removed | 0 |
| nodes changed | 0 |

**Edges — the damage:**

| | |
|---|---|
| edges live | 33 |
| edges after a land | 27 |
| **edges removed** | **12** — every one `governedBy`, every one `$note`-marked `"HAND-AUTHORED under s282-D5"` |
| edges added | 6 — the same `governedBy` relations re-declared as `{"t": null}` stubs |

**Top-level fields lost or overwritten:**

- ⛔ **`ratified: "s277-D4"` — LOST** (the dry-run shape has no `ratified` key).
- ⛔ **`$s282-D5` — LOST ENTIRELY.** This is Dave's own 2026-09-18 ruling block, recording that the
  4 hexagon nodes bind to `rule:logo26-010` and the 4 masterbrand nodes to `rule:logo26-008` /
  `rule:logo26-009`, sourced to his export `notes/_lanes/282/logo-review/DAVE-EXPORT-2026-09-18.json`.
- `$description` — overwritten: the live text *"RATIFIED … EXCEPT the 12 `governedBy` edges, which
  s282-D5 (Dave 2026-09-18) resolved and which the generator cannot draw. Re-apply
  notes/_lanes/282/logo-land/bind.py after any regeneration."* reverts to *"PROPOSED … NOT
  RATIFIED"*.
- `edge_types.governedBy` — overwritten: `"RESOLVED 2026-09-18 by s282-D5 …"` reverts to
  `"DECLARED-NULL ONLY — never drawn, never resolved"`.
- `unresolved` — the hand-authored ledger differs.

★ **The file predicted its own destruction.** Its `$s282-D5.generatorVerdict` field already says,
from #282:

> *"gen_kg_icons.py --land --ratified s277-D4 was RUN FIRST and did not pick the new rules up:
> governedBy is in NULL_ONLY_TYPES; the regen changed 6 `why` lines only … and drew 0 edges"*

An independent receipt, written by a prior lane, that this generator both fails to add and
succeeds in subtracting. My dry-run reproduces it exactly.

**⇒ This is precisely the brief's STOP condition** — "any node removed, any hand-authored field
overwritten". It was met *before* the write, so `git checkout --` was never needed: nothing was
written. **AFTER hashes of both generator outputs are byte-identical to BEFORE:**

```
9409c60144e464922d127e051484446eae3693106e8d3b2b10ab6fbacdace072  knowledge/_logo_nodes.json
5bc419187774b1a4f9ed8df7d36cfc982db80fb33788a675ace8370ad87f6bc7  knowledge/_icon_nodes.json
```

`git diff --stat` for the generator's declared outputs: **empty — 0 files changed.**

---

## 5. Row `W-285lm` — amended through the store's own writer, left OPEN

`knowledge/_state.py` has **no amend CLI**: `--help` prints the docstring, and `__main__` only runs
`check()` / `counts()` / `--selftest`. Its writer API is the module's `load()` → mutate →
`check()` → `save()`. That path was used (`notes/_lanes/286/R/state-writer-output.txt`); the JSON
was **not** hand-edited.

**`closes_when` is UNCHANGED**, verbatim: *"Dave has looked at the 4x before/after contact sheet
and either accepted the regenerated masters by eye or named what still looks wrong"*. The body
gained the #286 finding, Dave's six words, the DAVE-RULINGS path and this report path.

⚠ **Why it is NOT closed, although its `closes_when` reads as met.** Taken literally that condition
was satisfied at #285 (Dave accepted by eye). #285 deliberately left the row open because
registration is owed, and recorded that in the `body` rather than rewriting the condition. **I held
that line and did not close it** — closing on a met condition while the work the row is about
remains undone would retire the only open handle on the registration. **The `closes_when` and the
`body` disagree about what this row is for; that disagreement is Dave's to settle, not mine.**

**What the writer said, verbatim:**

```
BEFORE state: open
BEFORE closes_when: Dave has looked at the 4x before/after contact sheet and either accepted the
regenerated masters by eye or named what still looks wrong
check ok: True
  NOTE: DECLARED DEBT: 14 item(s) carry no close condition (W-0b, W-01, W-02, W-03, W-04, W-05,
W-06, W-07, W-08, W-09, W-10, W-11, W-12, W-13). Frozen set size 19 — this number may only fall.
Each needs Dave's word, not an agent's guess.
  NOTE: real-input coverage: 1 item(s) carry a deadline, 0 carry an effort; on those items the
dashboard's PROXY is REPLACED. The rest of the 589 live item(s) are still scored by prose scan /
body length.
  NOTE: project split: apollo 543 · memento 152 (of 695 items). The values written at #172 are
DEFAULTS proposed for Dave's eye, not his ruling on each item.
  NOTE: home pointers: 677 resolve by ANCHOR (rot-proof), 18 are still `path:line` (UNVERIFIABLE by
content — the #168 rot class), 0 UNRESOLVABLE. Blocking = True (Dave's dial).
SAVED
counts: {"total": 695, "live": 589, "by_state": {"open": 589, "blocked": 0, "ruled": 0, "done": 86,
"dropped": 0, "parked": 20}, "by_owner": {"dave": 305, "claude": 284}, "unconditioned": 14,
"conditioned": 681}
AFTER state: open | closes_when unchanged: True
```

`python3 knowledge/_state.py --selftest` → `_state selftest: 57 bites, all GREEN`.

`_state.json`: `918452e6…` → `6ce5812b11a942ba0979d4d6fb141ad6830a01009abf92b7ceebadb4e21f8f43`.

⚠ **Concurrency note, checked not assumed.** `git diff` of `_state.json` shows **two** rows moved:
mine (`W-285lm`, body only, still `open`) and **`W-285sc` → `done`**, which is **lane S's**, not
mine. `git show HEAD:knowledge/_state.json` has both rows `open`, so S's write landed **before** my
`load()` and was **carried through** my `save()` unmodified. **Nothing of S's was clobbered.**

---

## 6. `--check` gates (from `knowledge/_git_commit.sh`, read-only)

The commit script runs four. All were run before and the three that my write could touch again
after. **No generator was run.**

| gate | exit | result |
|---|---|---|
| `knowledge/gen_showroom.py --check` (`:316`, s191-D1) — **the `_logo_nodes.json` consumer** | **0** | `gen_showroom --check OK — 137 page(s) + index in sync` — **before and after**. My non-write keeps it green. |
| `knowledge/_validate_polarities.py --check` (`:343`, s238-D7) | **0** | `polarity gate GREEN — five refusals asked and none fired` |
| `knowledge/_build_graph_mention_map.py --check` (`:378`) | **0** | `current (102 of 102 node(s) mentioned)` |
| `knowledge/_gen_chain.py --check` (`:294`) | **1** | ⚠ `_CHAIN.md is STALE …` |

⚠ **The chain gate was ALREADY RED at lane open, before I wrote anything** — `checks-before.txt`
records it against a tree carrying only other lanes' edits. It is **not caused by this lane**, and
`_gen_chain.py` is a generator, so I did not run it. ⇒ **The commit lane must run
`python3 knowledge/_gen_chain.py` and stage the result, or `_git_commit.sh` will refuse at line 295.**

---

## 7. ⛔ RULING-SHAPED, LEFT OPEN FOR DAVE

**The fence is released and the door behind it is bricked up.** Registering the masters needs a
**change to `gen_kg_icons.py`**, and that change is a **closed-vocabulary question (#75)** — the
same class the generator's own docstring says Dave ratifies. Three shapes, and choosing one is not
a lane's call:

1. a **`size` field** (or a `sizes` array) on the existing 8 `logo:` nodes — no new ids, no new
   kind, smallest possible change;
2. **40 new nodes** `logo:<stem>-<h>` — new ids inside an existing kind, and an
   `atSize`/`masterOf` edge type to bind each to its lockup, which is a **new edge type**;
3. a **new node kind** `logoMaster:` — the largest change, and the one #75 most squarely governs.

DAVE-RULINGS-2026-09-18.md already records this as expressly still his: *"The shape of the master
registration in `_logo_nodes.json`, if he wants a say in it beyond releasing the fence."* **He may
want a say, because there is no shape to proceed with.**

⚠ **Second, and independent:** whatever shape is chosen, the regenerator **must stop eating
`s282-D5`**. The live `$description` currently instructs a human to *"Re-apply
notes/_lanes/282/logo-land/bind.py after any regeneration"* — a hand-repair step standing in for a
generator that cannot hold Dave's ruling. **Any lane that touches `gen_kg_icons.py` for the masters
should fix that in the same pass**, or the next registration attempt re-opens the same wound.

---

## Working files (all under `notes/_lanes/286/R/`, none in /tmp)

```
dryrun/_logo_nodes.json     the predicted land (8 nodes, 27 edges)
dryrun/_icon_nodes.json     the predicted icon land
dryrun/dry-run.json         the generator's own report
dryrun-stdout.txt           generator stdout, verbatim
dryrun-stderr.txt           empty
predicted-diff.txt          the structured JSON diff of §4
state-writer-output.txt     the _state.py writer's own words, verbatim
checks-before.txt           the four gates at lane open
checks-after.txt            the three re-runnable gates after the row write
```

**Net effect of this lane on tracked files: one row `body` in `knowledge/_state.json`. Nothing
else.**
