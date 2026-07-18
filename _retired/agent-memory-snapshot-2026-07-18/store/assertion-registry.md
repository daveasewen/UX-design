---
name: assertion-registry
description: THE permanent fix for stale claims — checkable environment claims carry a predicate re-tested every build; plus mirror-on-write for memory
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0ca1a754-0be4-4e9b-a84b-a28410f8f19e
---

**Dave, 2026-07-18: *"how do we fix this permanently?"*** — after a memory file asserted *"the sandbox
has NO Univers font"* for **sixteen months** while the licensed fonts sat in the repo.

## The diagnosis

That claim was **mechanically checkable the entire time** — `os.path.exists()`. It did not rot for want
of thinking. It rotted because **a checkable claim was stored as unverifiable prose**, in a place no gate
could read, with nothing to re-test it. And it had **fanned out to five places**, so correcting one would
have left four wrong.

## The fix — `knowledge/_assertions.json` + `_validate_assertions.py` (gate, wired into the build)

**RULE: every environment claim that CAN be reduced to a predicate MUST carry one, and the predicate is
re-evaluated on every build.** Rulings, judgements and preferences are deliberately OUT of scope — they
do not go stale by themselves. Facts about the world do.

- **`asserted_in` is the field that does the real work.** When a predicate flips, the gate names *every*
  document containing the now-false statement — including `memory:<slug>` entries it cannot read but can
  still name. Fan-out was the failure mode; the registry makes fan-out visible.
- **Blockers carry `recheck_days`.** A blocker stops work and therefore stops the work that would
  disprove it — highest rot risk in the system. Past its window the gate WARNS even while the predicate
  still holds.
- Predicate verbs are deliberately tiny (`path_exists`, `path_absent`, `glob_count`, `file_contains`,
  `file_lacks`), no eval. Claims that need more get a *named native check*, not a bigger language.
- Bite-tested by simulating the real failure: dropped a fake Latin `.woff2` in, gate went red and named
  all four documents. Removed it, green again.

**Complements — does not replace — [[gate-glob-scope-rule]] and `_validate_standing_instructions.py`.**
That gate is REFERENTIAL (is everything reachable). This one is VERACIOUS (is it still true). **A
document can be perfectly reachable and perfectly wrong.**

## Second half: MIRROR-ON-WRITE for memory

The memory mirror README claimed *"the agent cannot copy the memory directory — Glob refuses
application-internal paths"*. **Tested 2026-07-18: false.** `Glob` returns all 109 files;
`Read`/`Write`/`Edit` work normally. Only the **bash sandbox** is confined to the mount — the claim
conflated bash with the file tools, and the cost was that every memory write depended on Dave
remembering an rsync.

**RULE: when writing or editing a memory file, write the copy into
`knowledge/_agent-memory/store/` in the SAME PASS.** Not batched, not deferred to the capture ritual.
A mirror refreshed at the same moment as its source cannot drift and cannot be forgotten, because it is
not a separate step. Dave's rsync survives as a belt-and-braces catch-up, not the mechanism.

## The generalisation worth carrying

**Three claims rotted this session and all three were checkable.** "No Univers" (16 months), "the agent
cannot mirror memory" (weeks), "the Latin webfont is missing" (correct, but I disproved it wrongly). The
pattern: *prose that asserts a fact about the environment, with no way to re-test it.* Whenever writing
one, ask: **could a gate check this?** If yes, it belongs in the registry, not only in prose.
Related: [[memento-framing]], [[capture-ritual]], [[procedural-debt-and-method]].
