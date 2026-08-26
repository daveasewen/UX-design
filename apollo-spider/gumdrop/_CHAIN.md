<!-- MEMENTO-STARTER-CHAIN: this file ships with the pack and has never been generated.
     Copilot: if this marker is still here, nobody has finished a session yet. Go to
     FIRST-SESSION.md at the top of the pack. The first wrap replaces this file. -->

# Start here

This is the chain. It is the first thing read at the start of every session and it is the
only thing that needs to be read — a short, current note from the last session to the next
one, so work picks up where it stopped instead of starting again from nothing.

Right now it says nothing, because nothing has happened yet. **You are the first session.**

## The first move

Open **`FIRST-SESSION.md`** at the top of this pack and work through it. It takes about
twenty minutes and it ends with this file rewritten in your own project's words.

If you would rather just start building, that is fine too — say what you want to make and
get going. Come back here when you want the work to survive the end of the day.

## What is already here, empty and waiting

| | |
|---|---|
| `_state.json` | your worklist — what is open, what is blocked, what would make each thing done |
| `_rulings.json` | your decisions — the ones you do not want quietly re-opened later |
| this file | the note the next session reads first |

All three are empty on purpose. The shapes are set up and checked; the contents are yours.

## What replaces this file

The end of a working session writes two short files — `GOOD-MORNING.md` (where the project
stands) and `_LIVE-STATE.md` (what changed today) — and then regenerates this chain from
them:

    python3 memento-package/machinery/_gen_chain.py

From that point on this file is **generated**. Do not hand-edit it: anything typed here is
overwritten the next time it is regenerated, which is the one kind of note that is worse
than no note at all.

`runbooks/_RUNBOOK-capture-ritual.md`, in this folder, is the full end-of-session sequence.
