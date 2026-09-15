# Lane RV — READ-ONLY verification of lane RP (#275, 2026-09-15)

Verifier: lane RV. Nothing in the repo changed by me except this file — **with one
declared exception, item 19 below: re-running `_drive_page.py` (as instructed) rewrote
the committed `screenshot.png`.** No commit, no stash, no checkout, no `--land`.

Verdict in one line: **the lane's report is accurate.** 27 of 30 claims reproduce GREEN
from my own commands. Two numbers do not reproduce as stated (`60` edge-type strings,
and the `31 families` receipt) and one is an occurrence count presented as a node count.
No false attribution to Dave; no invented node or edge; nothing landed.

---

## 1. The dry run and every count, computed by me from the JSON — **GREEN**

```
$ python3 knowledge/gen_kg_principles.py --dry-run /tmp/rv.json
PARKED DUE — 1 parked item(s) are due at kg-edge-gen — python3 knowledge/_parked.py --due kg-edge-gen
DRY RUN — 145 principles · 30 polarities · 175 nodes · 111 edges
  edges: {'tensionWith': 22, 'hasParty': 68, 'explainedBy': 1, 'touches': 9, 'resolvedBy': 7, 'challengedBy': 4}
  status: {'tensionWith': 'NEW', 'hasParty': 'NEW', 'explainedBy': 'NEW', 'touches': 'NEW',
           'resolvedBy': 'NEW', 'challengedBy': 'NEW', 'inFamily': 'NEW', 'evidencedBy': 'EXISTS'}
  nodes: {'ux': 145, 'polarity': 30}  unresolved: 27
  pairwise view fresh (re-derived from polarities.json): True
  explorer reads _ux_principle_nodes.json: False
  NOT LANDED — a new node kind and a new edge type are closed-vocabulary changes (#75); --land needs --ratified sNNN-DN
```

I did not take the header's word. Counting the payload myself:

```
nodes len: 175   edges len: 111
node prefixes: {'polarity': 30, 'ux': 145}
edge types: {'tensionWith': 22, 'hasParty': 68, 'explainedBy': 1, 'touches': 9,
             'resolvedBy': 7, 'challengedBy': 4}  sum= 111
null t by type: {'hasParty': 15}  TOTAL NULL: 15
null edges carrying a note: 15 of 15
hasParty target kinds: {'ux': 51, 'NULL': 15, 'ruling': 2}  sum 68
unresolved by type: {'hasParty': 15, 'tensionWith': 12}  total 27
```

Every figure in the report's headline sentence reproduces exactly, including the
`hasParty` split "51 ux + 2 ruling resolved, 15 stubs null".

**Diff against the committed `dry-run.json` — GREEN:**

```
EQUAL after dropping corpus path: True
```

(The only difference is the absolute `corpus` path, which is machine-local and identical
here anyway.)

**"0 invented" — GREEN.** The only endpoints not in the proposal's own node set are 14
distinct `ruling:` ids; all 23 ruling refs resolve against the 578 ids in `_rulings.json`
(`UNRESOLVED ruling refs: []`). No `stub:`, `family:` or `evidence:` node is created in
the default run.

**Option runs — GREEN**, counted from the JSON myself, not from the header:

```
--family-edges --evidence-edges : nodes 260 {'evidence':53,'family':32,'polarity':30,'ux':145}
                                  edges 401 (+inFamily 145, +evidencedBy 145)  unresolved 38
--no-polarity-nodes             : nodes 145 {'ux':145}  edges 22 {'tensionWith':22}  unresolved 33
```

Matches the report's "inFamily 145 + 32 hubs, evidencedBy 145 + 53 nodes" and the RP-3(b)
cost of 33.

## 2. Freshness of the 22 pairwise edges, re-derived independently — **GREEN**

I did not use `polarity-edges.json` and did not use the generator's own self-check. I
re-derived from `polarities.json`: unordered party pairs with **different `role`** whose
refs both resolve to a `principles.json` row.

```
MY independent derivation (role-based): 22
generator tensionWith:                  22
IDENTICAL: True      only mine: []      only gen: []
VIEW (committed polarity-edges.json) == MY DERIVATION: True
```

Three-way agreement: my derivation = the generator = the committed generated view. The
"proved fresh, not a sha comparison" claim is real.

Party arithmetic also reproduces: 68 parties = 51 in `principles.json` + 15 in
`stubs.json` + 2 ruling-shaped, **0 in none of them**. 18 polarities with a derived pair,
12 without.

## 3. Selftest, 15 bites — **GREEN**

```
$ python3 knowledge/gen_kg_principles.py --selftest
  ok    bite 1 … bite 15        (all 15 listed ok)
SELFTEST PASS
```

15 bites present and named, one per clause, matching the report's list line for line.
The brief asked for ≥ 10.

## 4. Mutation harness, 18 mutants — **GREEN, and each mutant is a distinct clause**

```
$ python3 notes/_lanes/275/principles-kg/_mutate.py
BASELINE red=[] crashed=False — PASS
  M1 … M18  (each -> RED <bite numbers>)
ALL MUTANTS CAUGHT
```

I read `_mutate.py` rather than trusting the banner. Each of the 18 is a **distinct
one-line source substitution** against a distinct clause of the generator (I checked the
`old` anchors are 18 different strings). The harness is honest in three ways worth
recording:

- it runs a **baseline** first and refuses to interpret results if the unmutated source
  is already red;
- `SRC.count(old) != 1` is reported as `PATCH-MISS` and counted as a **survivor**, so a
  mutant that silently fails to apply cannot be scored as caught;
- a mutant that **crashes** is also counted as a survivor, not a catch.

The mutants run in an isolated `<scratch>/mutroot/knowledge/`, not the live tree, and it
is removed at the end. The report's "three bites were dead until the harness found them"
is consistent with the fixture changes visible in the harness and the generator, though
the three original dead bites are of course no longer reproducible — **UNPROVABLE but
plausible, and it is a confession, not a boast**.

## 5. Metas: 0 name a `pr-` id or the six laws — **GREEN**, with one nuance

```
$ ls knowledge/components/*.meta.json | wc -l          -> 138
$ ls knowledge/components/*.meta.json | grep -vc EXAMPLE -> 137
$ grep -o -E '"pr-[a-z0-9-]+"' knowledge/components/*.meta.json | wc -l  -> 0
$ grep -o -E '\bpr-[a-z0-9-]+'  knowledge/components/*.meta.json | wc -l  -> 0
```

Word-boundary, case-insensitive, all six laws:

```
\bfitts\b 0 · \bhick\b 0 · \bsteering\b 0 · \bklm\b 0 · \bkeystroke\b 3 ·
\bspeed-accuracy\b 0 · \bgraphical perception\b 0     (also \bvon restorff\b 0, \bdoherty\b 0)
$ grep -riE 'keystroke[ -]level' knowledge/components/*.meta.json | wc -l  -> 0
```

Two traps I walked into so the conductor does not have to:

- a naive `grep -i hick` returns **9 files** — every one is `thick` / `thickness` /
  `thickened` / `dividerThickness`. Under word boundaries it is 0. The report's claim is
  correct; a careless re-check would contradict it.
- `\bkeystroke\b` matches **3 lines**, all of them accessibility prose ("announces the
  number of matches after each keystroke"). None is "Keystroke-Level", the law name.
  `keystroke[ -]level` is 0. The claim stands.

**137 vs 139 reconciled — GREEN.** `_validate_kg.py` globs two directories
(`collect_component_files`, `knowledge/_validate_kg.py:115-117`): 138 in
`knowledge/components/` **plus** `knowledge/_proforma/icon-button.meta.json` = **139**.
The lane's grep scope is 137 = 138 minus `EXAMPLE-button.meta.json`. Both numbers are
right for their own scope; neither is wrong.

## 6. s238-D6 and s237-D1 — **GREEN**, `ruled` text quoted

**s238-D6** `ruled`, verbatim:

> "RULING LINKS ON A POLARITY ARE TYPED - resolvedBy / explainedBy / challengedBy /
> touches - AND THE GENERATOR REFUSES AN UNTYPED ONE; the apollo_touch slot (four link
> types in one field, lane T finding 2) ceases to exist and is migrated row by row, with
> any row the evidence does not settle marked UNPROVEN rather than guessed. Lane T's
> question 5."

The four link types are literally named in the ruling, and the refusal of an untyped link
is the ruling's own clause. The report's "already s238-D6's typed links" is exact. I also
enumerated the live data: `polarities.json` carries exactly these four types and no others
— `{'explainedBy': 1, 'touches': 9, 'resolvedBy': 7, 'challengedBy': 4}`, 21 links total,
matching the 21 typed-link edges.

**s237-D1** `ruled`, opening clause verbatim:

> "THE EVIDENCE GRADE IS A FIELD ON EVERY PRINCIPLE NODE, AND THE FIVE GRADES ARE NAMED:
> REPLICATED (was A …) · STUDIED (was B …) · PRACTISED (was C …) · DEBUNKED (was D …) ·
> OBLIGATION (was L …)"

Grade is ruled a **field**. The report's refusal to manufacture a decision about it is
correct, and the restraint is the right call.

## 7. 18 live prefixes and the edge-type collision — **GREEN on the conclusion, RED on the integer 60**

```
$ re.findall(r'"id"\s*:\s*"([A-Za-z][\w-]*):', open('notes/_KG-EXPLORER.html').read())
distinct prefixes: 18
  evidence 873 · artefact 610 · ruling 578 · rule 470 · pattern 382 · context 232 ·
  component 137 · snippet 137 · session 92 · axe 64 · sc 38 · shape 23 · intent 14 ·
  role 12 · guideline 12 · principle 4 · standard 1 · policy 1
ux: present? False    polarity: present? False
```

**Exactly the report's 18 prefixes with exactly the report's 18 counts, and both proposed
prefixes are free.** GREEN.

The collision result is also GREEN:

```
tensionWith ABSENT · hasParty ABSENT · explainedBy ABSENT · touches ABSENT ·
resolvedBy ABSENT · challengedBy ABSENT · inFamily ABSENT
evidencedBy PRESENT 1228
```

**But the number 60 does not reproduce.** Over the same file and the same `"type"` key I
measure **62** distinct strings, by four separate regex variants (spaced, unspaced,
word-chars-only, lookahead — all 62). Of those 62, **18 are the node-kind labels**
(`artefact`, `axe`, `component`, `context`, `evidence`, `guideline`, `intent`, `pattern`,
`policy`, `principle`, `role`, `rule`, `ruling`, `sc`, `session`, `shape`, `snippet`,
`standard`), leaving **44** genuine edge types on `s`/`t` triples. Measured against
`_build_kg_explorer.py` — the file the report names — a `"type"` regex returns **0**,
because the builder does not carry the vocabulary as literals.

So the defensible numbers are **62** (all type strings in the explorer HTML) or **44**
(actual edge types). **60 is neither, and I could not construct a measurement that yields
it.** The conclusion the number supports is nevertheless independently confirmed.

## 8. The commit — **GREEN on all four sub-claims**

```
$ git show --stat 77b043f          -> 10 files changed, 6474 insertions(+)
$ git show 77b043f --name-only --pretty=format: | grep 'knowledge/'
   knowledge/gen_kg_principles.py            (the only knowledge/ path in the commit)
$ ls knowledge/_ux_principle_nodes.json      -> No such file or directory
$ git log --all --oneline -- knowledge/_ux_principle_nodes.json   -> (empty: never committed, on any branch)
$ git diff --stat -- knowledge/              -> (empty)
$ git status --short --untracked-files=all -- knowledge/   -> (empty)
```

The refusal-probe file is **absent from the working tree, absent from the commit, and
absent from all history**. The report's §7 confession checks out in every direction I can
test it. `git status` before my own drive run showed only the two pre-existing
modifications the report itself declared (`notes/_REHEARSAL-LOG.jsonl`,
`notes/_dream/_GRADE-DECISIONS.jsonl`).

## 9. The review page: text diff, recommendation order, export, nam-002

**No text dropped — GREEN.** Placeholder-aware diff of all 39 JSON text spans (headline,
title, and per decision: title, lede, why, every option) against the tag-stripped page:

```
checked: 39   FAILED: 0   (after correcting my own regex for the builder's spacing)
```

My first pass reported 5 failures; all 5 were my regex tripping on the space the builder
inserts around a substituted `<span class="n">` value (`( 22 )`, `explainedBy 1 .`). I
then read the rendered RP-2 and RP-3 blocks in full and confirmed by eye that every
option and every clause is present with the numbers filled. Nothing is dropped.

**Recommendation first — GREEN.** In the JSON the `true` flag is at index 0 for all six
decisions (`RP-1..RP-6`, options `a/b/c` or `a/b/c/d`). In the rendered page each
recommended option is the first one printed and is labelled `(a) Recommended`. The page
also states the convention: "Six decisions. The recommendation is first in each. Nothing
here is ruled."

**Export control matches RK's — GREEN, in both mechanism and format.** Same two controls
(`btnExport` "Export JSON", `btnCopy` "Copy to clipboard", same `Copied` 1600ms
restore, same clipboard-then-execCommand fallback), same `a.download="<lane>-decisions-
2026-09-15.json"`, and a byte-identical `exportObj()` but for the page name:

```
RP:  {page:"REVIEW-principles-into-graph-2026-09-15-v1.html", at:…, decisions:IDS.map(… {id,choice,note}…)}
RK:  {page:"REVIEW-rules-into-graph-2026-09-15-v1.html",      at:…, decisions:IDS.map(… {id,choice,note}…)}
```

**nam-002 — GREEN.** `text-transform:uppercase` count 0. The only ALL-CAPS runs of 3+ in
visible prose are `WCAG` ×3, `JSON`, `HTML`, and `EXPLORER` (inside the filename
`_KG-EXPLORER.html`) — acronyms and a filename, not names. The driver's own independent
check also returns `[]`.

## 10. Quote gate on every sentence attributed to Dave — **GREEN**

Two sentences on the page are attributed to Dave, exactly as the report says.

```
$ python3 knowledge/_quote_gate.py "Evidence grade is a field on every principle node."
QUOTE-GATE ADVISORY — 0 verbatim · 1 not in the record
  ❌ nearest carries:residual-275 · _CARRIES.md:46 · bigrams 7 of 8

$ python3 knowledge/_quote_gate.py "my instinct is that adopting the hyper-relationship version might pay off in the future when we really make this KG more powerful"
QUOTE-GATE ADVISORY — 0 verbatim · 1 not in the record
  ❌ nearest carries:residual-275 · _CARRIES.md:46 · bigrams 6 of 22

$ python3 knowledge/_quote_gate.py "is the edges on edges such a daft idea ???"
QUOTE-GATE ADVISORY — 1 verbatim · 0 not in the record
  ✅ gm-archive:batch-2026-09-02-240 · _GM-ARCHIVE.md:604 (+2 more)
```

Both 0s reproduce, and the ✅ on the third reproduces. **Located by hand in the source the
report cites, and both are verbatim and occur exactly once** in `knowledge/_rulings.json`:

- `"Evidence grade is a field on every principle node."` — count 1, inside the `says` of
  **s237-D1**: `"says": "Dave at #237 on R1 Q1: 'Evidence grade is a field on every
  principle node. The letters A/B/C/D/L stay working labels until you name them…'"`.
  Verbatim including the full stop, which is the sentence boundary inside his quote.
- `"my instinct is that adopting the hyper-relationship version might pay off in the
  future when we really make this KG more powerful"` — count 1, inside the `says` of
  **s238-D1**. Verbatim.

The gate's 0s are the known index gap (`says` is not indexed), not a false attribution.
The lane's decision to hold back the ✅-passing "daft idea" quote, because quoting his own
question back reads as a gotcha, is the right judgement.

The page's other Dave-facing phrases — "the ladder you named at s237-D1", "a new node kind
and a new edge type are your word", "You have ruled the shape of both halves of this" —
are paraphrase, not quotation, and each is supported by s237-D1 / s238-D1 / #75. No false
attribution found anywhere on the page or in the report.

## 11. `_validate_kg.py` — **GREEN**

```
$ python3 knowledge/_validate_kg.py
== _validate_kg.py — KG edge parse-gate (s131-D2 / s133-D1 / s135-D4) ==
metas checked: 139
ref:null + $note (declared, awaiting Dave's-eye migration): 90
resolutions consumed (s135-D4, …): 82 ruled verdicts asserted present (MERGE 5 / PROMOTE 52 / ATTACH 25)

_validate_kg.py: OK — every ref parses+resolves, every null carries a note, every meta has
provenance, edges match schema, gen_kg_edges.py is idempotent-clean, and the s135-D4
resolutions input was consumed.
```

## 12. `_drive_page.py` — **GREEN**, 11 checks, reproduced

```
$ source knowledge/_render/seat_env.sh && python3 notes/_lanes/275/principles-kg/_drive_page.py
SEAT_ENV: OK seat=dazzling-gifted-ritchie … faces=10/404 farm=10/10 libs=2
  ok  font loaded (HSBC_MtUnivers_Latin)                                    True
  ok  0 console errors / warnings / page errors                             0 console message(s), 0 bad, 0 page error(s)
  ok  descenders intact on the tight boxes                                  35 element(s) across 8 selectors · worst clip 0.00px
  ok  no element crops its own content                                      []
  ok  no text-transform:uppercase (nam-002)                                 []
  ok  no ALL-CAPS runs in visible text (nam-002)                            []
  ok  export is the RK shape {page, at, decisions:[{id, choice, note}]}     [{"id":"RP-1","choice":"a","note":""}, …]
  ok  localStorage round-trips the choice and the note across a reload      {"a":true,"n":"a note that must survive a reload", …}
  ok  390px: no horizontal scroll                                           {"s":390,"c":390}
  ok  light: accent rgb(218, 26, 0), 0 crop, 0 overflow (s151-D1)
  ok  dark:  accent rgb(246, 96, 76), 0 crop, 0 overflow (s151-D1)
DRIVE PASS
```

All 11, both themes, the two-red law values exact.

## 13. Other claims spot-checked — all **GREEN**

- grade split and fields: `145 {'A':6,'B':28,'C':75,'D':9,'L':27} 32 families`, and all
  twelve fields present on all 145 rows.
- `0 of 53 evidence URLs join a live evidence: node`: 53 proposed vs 853 distinct live —
  **intersection 0**.
- the stale-line claim: `knowledge/gen_kg_rules.py:556` hard-codes
  `"⚠ NO CONSUMER YET — _build_kg_explorer.py does not read this file (decision RK-5)."`,
  and `_build_kg_explorer.py` **does** name `_rule_nodes.json` (2 occurrences) — so that
  line is indeed stale. `gen_kg_principles.py` does **not** copy it: `explorer_reads()`
  (line 220) greps the builder at run time and prints the measured `False`. The fence the
  brief set was obeyed.
- P-274-3 is the parked item firing the advisory on every run, as claimed.
- `explorer_mb 2.7` and `payload_full_kb 123` are decimal (`/1_000_000`, `/1000`) per
  `_build_page.py:95-98`, not binary — so they are internally consistent, not errors.

---

## Not in the report — what the conductor should also know

**A. The "60 live edge-type strings" does not reproduce (item 7).** I get 62 all-type
strings, 44 genuine edge types, and 0 from the builder the report names as the source.
The finding it supports is solid; the integer should not be repeated in a wrap or a
ruling until someone can name the command that produces it.

**B. The "#269 inventory says 31 families" receipt is misattributed.**
`notes/_lanes/269/kg-gaps/A-inventory.json` contains **no literal `31` at all**
(`grep -o '\b31\b' … | wc -l` → 0). The number 31 comes from the **conductor's own
BRIEF.md**, line 5: "principles.json (145 · grades A6 B28 C75 D9 L27 · **31 families**)".
The correction to 32 is right and valuable — the brief is what needs the correction, and
the #269 inventory is wrongly blamed for it.

**C. "27 declared nulls" and "the only nulls are the 15 stubs" are both in the report and
they are different things.** 27 = 15 null-target `hasParty` edges + 12 polarities declared
as deriving no `tensionWith` pair. Only **15 edges** actually carry `t: null`. Both
statements are true in their own scope, but a reader taking "27 declared nulls" into a
ruling will overstate the null edges by 12. Worth one clarifying word if it reaches
`_rulings.json`.

**D. The 18-prefix table is occurrence counts, not distinct nodes — and one differs.**
For 17 of the 18 prefixes occurrences == distinct. For `evidence` it is **873
occurrences but 853 distinct ids**. The report presents the table as "live node
prefixes". Immaterial to every conclusion drawn from it, but "873 evidence nodes" is 20
too many.

**E. I modified a committed file, and cannot revert it.** Re-running `_drive_page.py` as
instructed rewrote `notes/_lanes/275/principles-kg/screenshot.png` (961,815 → 961,818
bytes — a fresh render of the same page, 3 bytes of PNG encoding). `git status` now shows
it modified. `git checkout` is fenced for me, so I left it. **Either restore it with
`git checkout -- notes/_lanes/275/principles-kg/screenshot.png` or amend/commit the
re-render.** The driver writes the screenshot unconditionally as part of passing, so any
future verifier re-running it will do the same — a small defect in the driver's fitness
as a re-runnable gate.

**F. The refusal probe is worse than the report frames it, and better than it looks.**
The report calls the `--land --ratified s269-D2` incident "my error, not the
generator's". That is the honest half. The other half is a real design gap the conductor
should rule on: **`--land` checks only that a ruling id EXISTS, so any of the 578 recorded
ids unlocks any land.** #75 may only ask for existence, but the same hole will be there
when the real ratification arrives, and the next lane will be one typo from landing
against the wrong ruling. A `governs`/scope check on the ratifying ruling is a one-line
decision that nobody has been asked. The lane's own stated lesson (drive probes against
the selftest's synthetic corpus) fixes the lane's behaviour, not the guard.

**G. Nothing else.** No claim in the report is unreceipted beyond the three dead bites
(inherently unreproducible once fixed, and volunteered rather than hidden), no stale line
copied from `gen_kg_rules.py`, no invented node or edge, nothing landed, and no sentence
attributed to Dave that he did not say.
