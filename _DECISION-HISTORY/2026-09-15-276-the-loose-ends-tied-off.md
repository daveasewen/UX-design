# #276 — the loose ends tied off

provenance: 276 · 2026-09-15
status: observed

*Spine entry: `_LIVE-STATE.md` § ⏱ LATEST DELTA (#276). Ledger: `knowledge/_rulings.json`
§§ `s276-D1`…`s276-D6`. Handoff: `_HANDOFF-127-the-loose-ends-tied-off.md`. His words verbatim:
`notes/_lanes/276/DAVE-RULINGS-2026-09-15.md`. Lane record: `notes/_lanes/276/tie-off/`
(`BRIEF.md` · `REPORT.md` · `VERIFY.md` · `LAND-REPORT.md` · the review page and its export).
Written at the delegated wrap; the WHAT is in the ledger and the spine, and this file is the
WHY and HOW.*

---

## The session is not the one that was opened

The chat was titled **`Apollo - #276: icons then logos — s269-d1 step 4`**. Step 4 is the 666
icons and then the logos, and it was the obvious next move: `s269-D1` names five steps for
filling the knowledge graph's empty families, and #273, #274 and #275 had done the first three
in a row, each by the same method, each in a day.

Dave's third sentence of the day redirected it:

> *"3. edit mode can wait until we do edit mode, park it has a tripwire. 19 missing  WCAG
> criteria, I wasn't aware of this. rule→component authored the other way --- maybe we just tie
> off these loose ends first."*

Three things in one sentence, and the third of them is the session. **Step 4 was deferred by his
word, not lost to drift** — which is the distinction worth recording, because a session that ends
up somewhere else usually got there by accident and this one did not. The retrospective name is
*the loose ends tied off*; the forward name is the one the deferral makes true.

## The finding that made the session possible was a declared absence

The line that mattered is *"19 missing WCAG criteria, I wasn't aware of this"* — and the reason
he could become aware of it is a decision taken at #274. `s274-D9` ruled that the nineteen
unresolved SC citations in the guideline corpus would land as **`ref:null` with a note** rather
than as invented targets or as silently dropped edges. A graph that can say what it does not know
puts the gap on a surface; a graph that quietly omits it does not. Nineteen nulls sat in
`knowledge/_rule_nodes.json` for one session and then closed to zero.

The method of closing them is the part that could have gone wrong. `title` and `level` for
seventeen criteria are exactly the kind of fact a model will produce from memory with total
confidence. Lane TO fetched all seventeen from the W3C *Understanding WCAG 2.2* pages —
17/17 HTTP 200 — and lane TV, read-only and independent, **fetched all seventeen again itself**
and compared: 17/17 title exact, 17/17 level exact. It also caught a fact the brief had wrong:
the brief named 2.4.13 as the only level-AAA criterion in the batch, and there are **three**
(1.4.8, 2.4.13, 3.1.4). That correction turned `s276-D2` from a one-way ruling into a three-way
one before Dave ever saw it.

His note on that decision — *"and cited as best practice"* — is the whole of the reasoning for
where the AAA line lives. The rule schema is `additionalProperties: false`, so a new field was
not available; the corpus already carried the phrase for its two existing AAA rules (2.3.3 and
2.4.8), in `sources.internal_policy_ref`, and that is where the three new ones carry it too. The
corpus may HOLD a criterion above its own conformance bar without moving the bar.

## Rule → component, authored the other way round

`s274-D12` refused the machine-drawn direction: a name-match tier over prose produced *"Avatar"*
from a rule that merely mentioned avatars, and a false positive of that shape is worse than an
absent edge because it looks like knowledge. What was left owed was the **authored** direction —
a component's own meta citing the rule, with a human sentence attached.

`s276-D3` is that, and its load-bearing clause is one word: **`$why` is REQUIRED**. An `obeys`
entry with a ref and no sentence is inference wearing a ref; requiring the sentence makes the
regex route structurally unavailable rather than merely discouraged. Eighty-one entries landed
across six components, every `rule:` id taken from a **filename join** on `_rules-index.json`,
never from a match over prose. Exactly one citation crosses files — `links` obeys
`rule:ctkb-004`, the buttons-vs-links boundary — and its own `$why` says so.

Six components, not the four the brief named: the chips half of the tags spec genuinely covers
`tags-input`, and the buttons spec names icon-only as one of its three structural variations, so
`icon-button` is covered. `split-button` is not, and was not authored. The discipline that
produced six rather than four is the same one that refused a seventh.

## The gate had to learn a new grammar, and it was mutated rather than asserted

`edges.obeys` is the first edge type in the corpus whose refs point outside the component corpus.
`_validate_kg.py` failed **164 times** on first run — 83 refs it could not parse, 81 edges
carrying a `$why` key the shared `definitions/edge` did not allow. The repair was three additions:
`rule` and `ux` into the ref grammar, **resolving against the files that are already their home**
(`knowledge/guidelines/_rules-index.json`, `knowledge/_ux_principle_nodes.json`) rather than
against a second registry that would immediately start drifting; and per-edge-type property
reading, with a fallback to the shared definition so no other edge type changed shape.

Then it was **mutation-tested**: `rule:ctkt-002 → rule:ctkt-999` had to make the gate red, and
`$why → $whx` had to make it red on both arms. Both did; both were reverted immediately. A gate
extended to accept new input is a gate that might now accept anything, and the only way to know
is to break it on purpose.

## The refusal

#275 discovered a hazard nobody had planned for: two live sessions on one repo, the still-open
#274 seat committing into `notes/_lanes/275/`. It was healed by addition and deliberately left
unruled, and #276 opened with his one word on it: *"1. fix"*, read back as *make it impossible*.

The conductor took *make it impossible* literally and read back the two durable options — a seat
lock (one session holds the repo; a second cannot commit at all) or a worktree per session. He
refused both:

> *"this has gone from a patch to a hack, not sure I like this unless its not permanent"*

Both were dropped. The second read-back offered much less: an **advisory** guard that prints the
offending staged paths and blocks nothing, carrying a **removal date** — off at the next dream
pass if the tripwire never fires — with one-seat-at-a-time left as the norm it has been since his
#57 word. That drew *"go"*.

His note on the same decision stands in the ruling's own `ruled` field:

> *"Okay but I don't think this is durable, feels like we're patching just to get it done"*

It was not smoothed out, and it should not be. **`s276-D6` inscribes a guard and records a norm;
it does not make one-seat-at-a-time law**, and nothing downstream may read it as though it did.
Whether two sessions may share one repo at all is still his to say.

## The session's own defect, and why the door had to be run

`P-276-1` — *did the guard ever fire?* — shipped in the enactment commit with `at_commit`
`6beedef`. The guard itself had landed one commit EARLIER, in `8053591`. A `file-changed` trigger
baselined after the only change it watches has **nothing to find**: `_parked.py --due dream-pass`
omitted the item silently, and `s276-D6`'s removal date — the entire reason the guard was
acceptable — would have quietly never come due.

Reading the row would not have shown it. The row was well-formed. What showed it was **running
the door**: `--due dream-pass` printed five items and P-276-1 was not among them. Healed by
addition at `7cc7cd9` (`at_commit` → `3b9d89b`, the last wrap), after which the door prints
*"P-276-1 … changed in 1 commit(s) since 3b9d89b"*.

This is the [[instrument-without-a-consumer]] class in its smallest possible form, and it is the
second time in three sessions that a green-looking artefact was caught by driving it rather than
by inspecting it — #275's re-dumped `_rulings.json` was caught the same way, by a hand proof
rather than by a gate. **A parked item is only a tripwire if the register says it is due.**

## What is resolved, and what is still open

**Resolved.** The 19 declared `cites` nulls close to zero; the compliance corpus holds 55
criteria, up from 38; `edges.obeys` exists, is typed, is schema-scoped so `containedBy` still
cannot point at a rule, and resolves 81/81 through the gate; six components cite their rules with
a sentence each; `P-274-2` and `P-274-3` are closed by `s276-D1`…`s276-D4`, rows kept.

**Still open, and every one of them Dave's.** One-seat-at-a-time as law. The three chart
components `s276-D5` sends to the next lane, together with the question of whether `chart-donut`
shares the pie spec the way `icon-button` shares the buttons spec, and what to do with the 19
family-level rules in `data-visualisation.md` that sit above all three. The explorer does not yet
draw `component → rule:` / `component → ux:` from `edges.obeys` — declared by the landing lane
rather than discovered later, because the rulings did not ask for a reader. `compliance/README.md`
says 31 rules against a corpus of 55. The showroom is 108 pages stale for the fourth wrap running.
And `s269-D1` step 4 — the icons, then the logos — is exactly where it was when the day opened,
carried at age 1, deferred by his word.
