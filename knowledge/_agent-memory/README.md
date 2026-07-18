# Agent memory — repo mirror

**STANDING:** this directory is the backup of the agent's memory, which otherwise lives outside the repo
and outside every backup Dave actually runs.

## The problem this exists for

The agent's memory lives at:

```
~/Library/Application Support/Claude/local-agent-mode-sessions/<session-id>/<id>/spaces/<space-uuid>/memory/
```

That is **local, not cloud** — plain markdown files on Dave's Mac ("local-agent-mode-sessions" is literal).
Which is better than it sounds in one way and worse in another:

- ✅ It is not locked in a service. It is files, on disk, that Dave can read, copy and back up.
- ❌ It is **not in git**, **not pushed by GitHub Desktop**, **invisible to the shell and to every gate**,
  buried in `Application Support` where nobody looks, and **keyed to a space UUID** — so it is tied to
  *this* Cowork space. Reset the space and 95 memories go with it.

## What this mirror IS and IS NOT

**IS:** disaster recovery. If the space is reset or the memory directory is lost, the accumulated
working relationship — how Dave likes to be communicated with, which rules were ruled and why, which
approaches were tried and rejected — is recoverable from here.

**IS NOT:** a third place for rules to live. That would make things worse, not better — it would create
another artefact that can silently drift from both the memory and the repo, which is precisely the
failure mode that produced the `#1A1A1A` and §A incidents.

> ⚠️ **The mirror does not change the rule: memory is an accelerator, the repo is the record.** Anything
> that must survive — a rule, a rationale, a threshold, a convention — belongs in its proper repo home
> (`GOOD-MORNING.md` §A, a runbook, a guidelines rule with an `{#id}`, a decisions ledger), **not only
> here and not only in memory**. If you find yourself reading this mirror to answer a question about how
> the project works, something has already gone wrong upstream.

## Refreshing it

The agent **cannot** copy the memory directory itself — the shell sandbox cannot reach outside the
connected folder, `Glob` refuses application-internal paths, and requesting that directory as a working
folder is off-limits. So this is Dave's one command, run in Terminal from anywhere:

```bash
rsync -a --delete \
  ~/Library/Application\ Support/Claude/local-agent-mode-sessions/*/*/spaces/*/memory/ \
  ~/Documents/Claude/Projects/UX-design/knowledge/_agent-memory/store/
```

Then commit as normal. Worth doing at the end of any session that added or changed memories — the
capture ritual (step 3) flags when that happened.

If the glob matches more than one space, that is useful information in itself: it means memory is
fragmented across spaces, and the largest `store/` is the live one.

## Recovery

If memory is ever lost, hand the agent `store/MEMORY.md` and tell it to re-read the individual files it
points at. The index is the map; the files are the content.

## Entry points

`_RUNBOOK-capture-ritual.md` step 3 (the mirror instruction) · `GOOD-MORNING.md` §A (the Memento
framing — tattoos vs Polaroids, and why memory is a Polaroid despite feeling like a tattoo).
