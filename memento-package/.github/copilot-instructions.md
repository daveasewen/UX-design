# Boot instructions — GitHub Copilot in VS Code

These instructions govern how you (Copilot) behave in this repository. Follow them exactly.

## The boot rule

On the first **"good morning"** from the user in a session, do this:

**Check for a chain.** Look for `_CHAIN.md` at the repo root.

### Arm 1 — a chain exists

Pick up the chain and continue as normal:

1. Read `_CHAIN.md`. It is generated and it is the whole contract — the header, the ★ LATEST
   banner, and the ⏱ latest delta. If you have read it, you have read what you need to orient.
2. Orient yourself from it, then get to work on whatever it points you at.
3. At the end of the session, the wrap writes the chain the next "good morning" will read. You
   do not need to do anything special to make this happen beyond following the wrap step below.

This is the ordinary case, every session after the first. Do not treat it as a special path.

### Arm 2 — no chain exists

This is a first boot. Do two things, in order:

1. **Give the orientation.** Explain what Memento is and how it works in plain language: each
   session ends by writing a short record (the chain) that the next session reads first, so
   context survives between sessions without re-reading everything every time. Mention that
   retrieval for anything beyond the chain happens on demand, not by reading files up front.
2. **Ask exactly one question, with exactly two options.** Ask it verbatim, character for
   character, including the bracketed clarifiers:

   1. *"Do you have a project you want us to work on together?"* *(one of your existing
      projects)*
   2. *"What would you like to start on today?"* *(a brand new project, not started yet)*

   If the user picks option 1: survey the existing project they name, and inscribe the first
   chain from what you find in it.

   If the user picks option 2: there is nothing to survey. Start the record from nothing, based
   on what the user tells you they want to build.

Do not skip the question and guess. Do not survey a project before the user has named it. The
chain's presence is the one thing you can detect mechanically; the user's intent is the one
thing you cannot — ask for it.

## Minimal operating rules

- **Read `_CHAIN.md` only, at boot.** Do not open `GOOD-MORNING.md` or `_LIVE-STATE.md` "just to
  check" once you've read the chain. That reflex defeats the entire point of generating a small
  chain file in the first place — you would pay the full cost of the large files every time,
  which is exactly what the chain exists to prevent.
- **Retrieval is on demand, never a reading list.** For anything beyond what the chain gives you,
  use `python3 machinery/_memento_search.py "<query>"`, then `--fetch <id>` on whatever result you
  need. Ask for what you need; do not read a file to find out whether you need it.
- **The wrap writes the chain the next session reads.** At the end of a working session, make
  sure `GOOD-MORNING.md` and `_LIVE-STATE.md` carry the session's outcome (header/★ LATEST banner
  and ⏱ latest delta respectively), then regenerate `_CHAIN.md` (see below) so the next "good
  morning" picks up a fresh, accurate record rather than a stale one.
- **`_CHAIN.md` is generated. Never hand-edit it.** It is derived entirely from
  `GOOD-MORNING.md`'s header + ★ LATEST banner and `_LIVE-STATE.md`'s ⏱ latest delta. Any
  hand-edit to `_CHAIN.md` itself will be overwritten, and will not survive a freshness check.
- **Regenerate it with `machinery/_gen_chain.py`:**
  - `python3 machinery/_gen_chain.py` — writes `_CHAIN.md` from the current state of
    `GOOD-MORNING.md` / `_LIVE-STATE.md`.
  - `python3 machinery/_gen_chain.py --check` — exits non-zero if `_CHAIN.md` is stale (does not
    match what `GOOD-MORNING.md` / `_LIVE-STATE.md` currently say). Run this before ending a
    session if you are unsure whether the chain was regenerated after your last edit.
  - `python3 machinery/_gen_chain.py --selftest` — runs the generator's own internal checks.
    Useful if something about the chain looks wrong and you want to rule out a broken generator
    before suspecting the content.

## Filenames are fixed in this version

`GOOD-MORNING.md` and `_LIVE-STATE.md` are this package's own convention for where the header,
★ LATEST banner, and ⏱ latest delta live. They are not configurable in this version — use those
exact filenames at the repo root.
