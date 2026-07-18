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

## ⚠️ WHETHER THIS DIRECTORY SHOULD EXIST AT ALL — open, raised by Dave 2026-07-18

*"why are we doing this, surely this isn't the usual way it works?"* — Dave, on being told mirror-on-write
was now automatic. **He is right, and the mirror does not survive the question well.**

- **It is not how agent memory normally works.** Memory lives where it lives; users do not back it up.
- **It has already drifted into the third source of truth its own README forbids.** Counted 2026-07-18:
  **115 files in `store/` against 110 live.** Five memories that were deleted or superseded still sit
  here, reading as current.
- **It exists because we do not trust our own rule.** The project says *"memory is an accelerator, the
  repo is the record."* If that were true, losing memory would cost nothing worth mirroring. The mirror
  is insurance against durable things living ONLY in memory — which is a **normalisation failure**, the
  same disease behind the 975-line `_LIVE-STATE` and the sixteen-month "no Univers" claim.

⇒ **Recommendation to the consolidation session: consider DELETING this mirror rather than maintaining
it.** If facts get one home each in the repo, memory becomes genuinely disposable and this directory is
pointless. A well-synced mirror is a worse outcome than no mirror, because it is another place to rot.
Everything below is interim behaviour pending that ruling.

## Refreshing it — **MIRROR-ON-WRITE (2026-07-18, PROVISIONAL)**

> ### ⚠️ The old instruction here was WRONG, and it was wrong in the way this whole project keeps
> ### getting caught: a checkable claim, written once, believed for weeks.
>
> It said *"the agent **cannot** copy the memory directory itself — the shell sandbox cannot reach
> outside the connected folder, `Glob` refuses application-internal paths"*. **Tested 2026-07-18:
> `Glob` on the memory directory returns all 109 files, and `Read`/`Write`/`Edit` operate on them
> normally.** Only the **bash sandbox** is confined to the mount; the *file tools are not*. The claim
> conflated the two, and the cost was that every memory write since has depended on Dave remembering
> a manual rsync — a durable thing hanging off a human's memory, which is the exact anti-pattern the
> Memento framing exists to name.
>
> Dave, 2026-07-18, on being told the rsync was still outstanding: *"same thing I guess."* Correct.

### The rule now: **mirror in the same pass as the write.**

**When the agent writes or edits a memory file, it writes the copy into `store/` immediately — same
turn, not batched, not deferred to the capture ritual.** A mirror that is refreshed at the same
moment as the source cannot drift, needs no reconciliation step, and cannot be forgotten because it
is not a separate step at all. Batching is what created the dependency; removing the batch removes it.

Practically: `Read` the memory file → `Write` the identical content to
`knowledge/_agent-memory/store/<name>.md`. Update `store/MEMORY.md` whenever the index changes.

### Dave's rsync — still valid, now a belt-and-braces catch-up, not the mechanism

Useful for a full reconciliation (e.g. after a session that pre-dates mirror-on-write, or to catch
anything written outside this project's conventions):

```bash
rsync -a --delete \
  ~/Library/Application\ Support/Claude/local-agent-mode-sessions/*/*/spaces/*/memory/ \
  ~/Documents/Claude/Projects/UX-design/knowledge/_agent-memory/store/
```

If the glob matches more than one space, that is useful information in itself: memory is fragmented
across spaces, and the largest `store/` is the live one.

<details><summary>superseded text (kept for the audit trail)</summary>

~~The agent **cannot** copy the memory directory itself — the shell sandbox cannot reach outside the
connected folder, `Glob` refuses application-internal paths, and requesting that directory as a working
folder is off-limits. So this is Dave's one command, run in Terminal from anywhere:~~

```bash
rsync -a --delete \
  ~/Library/Application\ Support/Claude/local-agent-mode-sessions/*/*/spaces/*/memory/ \
  ~/Documents/Claude/Projects/UX-design/knowledge/_agent-memory/store/
```

Then commit as normal.
</details>


## Recovery

If memory is ever lost, hand the agent `store/MEMORY.md` and tell it to re-read the individual files it
points at. The index is the map; the files are the content.

## Entry points

`_RUNBOOK-capture-ritual.md` step 3 (the mirror instruction) · `GOOD-MORNING.md` §A (the Memento
framing — tattoos vs Polaroids, and why memory is a Polaroid despite feeling like a tattoo).
