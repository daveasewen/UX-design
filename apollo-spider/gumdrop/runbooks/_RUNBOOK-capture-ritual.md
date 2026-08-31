# Runbook — closing a session (the capture ritual)

*Memento — Gumdrop v1.0.4, for VS Code + GitHub Copilot.*
<!-- The version above is STAMPED at bake from the pack manifest's carries.version (s225-D3).
     Do not hand-edit it; a hand-typed version is what shipped the v1.0.0/v1.0.2 disagreement. -->

The capture ritual is the fixed sequence a session runs before it ends. It exists because
**tracking rots silently**: a note that said "blocked" three weeks after the blocker cleared is
worse than no note, and nobody notices until it costs a day. A ritual is a cheaper defence than
remembering.

The principle underneath it: **don't archive every transcript.** A transcript rebuilds the
haystack. Invest instead in a *reliable* end-of-session distillation, because that is where the
real risk sits.

---

## When to run it

At the end of **every** session that changed anything — a decision, a component, a document.
Skip it only for pure question-and-answer sessions that touched nothing. If in doubt, run it;
it is cheap.

Also run it **mid-session, before you run out of room** — not when you have run out. See
`_RUNBOOK-context-gauge.md` in this folder. The gauge exists precisely to fire this ritual while
there is still clean budget to write the handoff *well*. A `GOOD-MORNING.md` written at the very
end of an exhausted session is the confidently wrong handoff you most want to avoid.

---

## The steps, in order

### 1. Flush the worklist

Everything still open goes into `_state.json`, through `_state.py` — never by hand.

Each item must say **what would make it done**. The store refuses an item that does not, and
that refusal is the feature: a list of things with no finish line only ever grows, and every
session after this one pays to read it.

```
python3 - <<'PY'
import sys; sys.path.insert(0, "memento-package")
import _state
doc = _state.load()
_state.add(doc,
    id="W-02", title="<short title>", project="apollo",
    body="<what it is, and where it got to>",
    state="open", opened=1, owner="claude",
    closes_when="<the condition that would let someone close this>",
    links=[], home="<a file that exists, relative to the pack root>",
    condition="stated",
)
_state.save(doc)
PY
```

Then close anything that finished — set its `state` to `done` — and check the whole store:

    python3 memento-package/_state.py

Exit code 0 and a sane count is the receipt.

⚠ `project` accepts only `apollo` or `memento`; `owner` only `dave` or `claude`. They are a
closed list on purpose, so a filter never silently drops a row to a typo. In this version those
are the only two values — use `apollo` and `claude`.

⚠ `home` must resolve to a file that exists. A task pointing at a deleted or renamed file is a
task nobody can act on, so the store refuses it rather than carrying it forward as a ghost.

### 2. Inscribe anything that got settled

A decision you do not want quietly re-opened becomes a **ruling**. Not every choice qualifies —
the test is whether it would cost an argument or an afternoon if someone changed it back.

Two rules make rulings worth trusting, and both are enforced rather than encouraged:

- **Nothing already inscribed is ever reworded.** Change your mind by adding a new ruling that
  supersedes the old one. Both stay readable, and the trail of *why* survives.
- **You never hand-edit `_rulings.json`.** There is exactly one writer, and it refuses anything
  malformed before it writes a byte.

<!-- -->

    python3 memento-package/_inscribe_ruling.py --entry <file>.json --dry-run
    python3 memento-package/_inscribe_ruling.py --entry <file>.json --write

The dry run proves the entry would land cleanly and writes nothing. Run it first, every time.
`FIRST-SESSION.md` at the pack root has a worked example with every field explained.

**Evidence must resolve.** Three forms are legal: `chat #<n> …`, `commit <sha> …`, or a path to
a file that exists. A pointer that does not resolve is worse than no pointer, so it is refused
on arrival rather than discovered as a dead end six months later.

### 3. Write the two state files

In `memento-package/`. The chain generator finds its material by exact markers, so keep these
headings verbatim — `FIRST-SESSION.md` at the pack root carries the full skeleton for both files.

- **`GOOD-MORNING.md`** — where the project stands. A dated header line, then `> ## ★ LATEST`
  (what this session did, for someone arriving cold), then `## ⬛ DO THIS FIRST` (the open work,
  one line each). ⚠ Keep the DO-FIRST section even when it is one line: without it the chain
  reports that it cannot see your open work, and the next session has to go looking.
- **`_LIVE-STATE.md`** — what changed today. A `Last refreshed:` line and a `## ⏱` delta section.

Keep them short and keep them *current*. The next session reads a generated summary of these
two files and nothing else, so anything stale in here is stale everywhere.

**Say what is unfinished, and say it plainly.** "I did not verify X" is a useful sentence. A
handoff that reads as though everything was checked, when it was not, is the failure this whole
discipline is built against.

### 4. Regenerate the chain

    python3 memento-package/machinery/_gen_chain.py

This derives `memento-package/_CHAIN.md` entirely from the two files above. It is **generated** —
never hand-edited. Anything typed into it is silently overwritten on the next run, and a silently
overwritten note is the one kind that actively misleads.

### 5. Confirm

    python3 memento-package/machinery/_gen_chain.py --check

Exit code 0 means the chain matches what `GOOD-MORNING.md` and `_LIVE-STATE.md` currently say.
Non-zero means you edited one of them after regenerating — run step 4 again.

If the design system files were touched, also run:

    python3 ci-template/run-gates.py

A session that leaves the gates red should say so in `_LIVE-STATE.md`. A red you have declared
is a known state; a red you have not is a surprise for someone else.

---

## What "done" looks like

The worklist is current, anything settled is inscribed, the two state files describe today, the
chain regenerates clean, and the transcript is not needed by anybody. A cold session can
reconstruct the project from the chain alone, and reach for anything else on demand.

---

## What this version does not have, and the honest substitute

Apollo runs an enforcing script over its own capture ritual — it checks the dates on the state
files, the section sizes, the commit state, and it blocks a wrap that fails them. **That gate is
not in this pack**, because most of what it enforces is specific to Apollo's own repository
layout and would fail here for reasons no project of yours could fix.

The substitute is step 5, run honestly: `--check` genuinely verifies that the chain matches its
sources, which is the single most valuable thing the gate did. The rest — "is this current?",
"did I say what I did not verify?" — is on you and on Copilot to ask out loud.

**A declared gap passes; a silent one fails.** That is the rule this pack is built on. If you
skipped a step, write that down. If you are not sure a check ran, say "unproven" rather than
"verified" — the second one is a claim, and a claim that turns out to be false costs far more
than an admission ever does.

---

## The self-checks, and which of them are honest here

The machinery in this pack carries its own tests. Two are worth knowing about:

    python3 memento-package/_state.py --selftest          # fully honest here
    python3 memento-package/machinery/_gen_chain.py --selftest

`_state.py --selftest` runs clean inside this pack — every arm of it is measurable here.

`_gen_chain.py --selftest` needs a project that has had at least one session. From a fresh unzip
it reports `GOOD-MORNING.md is missing`. That is expected, not a fault: there is no project
content yet for it to check.

`_inscribe_ruling.py --selftest` is **partially repo-bound** and will report three arms as
`UNMEASURED` in this pack — they need files that only exist inside Apollo's own repository. They
are declared, not hidden, and *unmeasured is not a pass*. The check that matters for your work is
`--dry-run` on a real entry: it runs the full refusal ladder and the reconstruction proof against
your actual store.
