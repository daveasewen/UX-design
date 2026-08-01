# Memento — Claude plugin flavour

Memento is a lightweight memory and continuity harness for AI assistants. Each session ends by
writing a short record (the chain) that the next session reads first, so context survives
between sessions without re-reading everything every time. The fuller story is in
`skills/memento-boot/references/what-memento-is.md`.

This is the **Claude plugin** flavour of the same package that ships for GitHub Copilot in
VS Code. Both flavours carry the identical boot rule and identical machinery; the only
structural difference is delivery — here, the first boot copies `machinery/` into your project,
because the scripts locate your project relative to that folder.

## Quick start

1. Install the plugin (open the `.plugin` file in Claude, press the install button).
2. Open or create a project folder in a Claude session (Cowork: select the folder).
3. Say **"good morning"**.
4. First time, there's no chain yet, so Claude explains what Memento is and asks you one
   two-option question: work on an existing project together, or start something brand new.
   Answer either way — that's the whole first-boot flow.
5. From then on, saying "good morning" picks up wherever the last session left off.

## What's inside

- `skills/memento-boot/` — the boot rule and session rules (the same ratified rule as the
  Copilot flavour, word for word).
- `machinery/` — the chain generator, retrieval search, and their support files, verbatim
  copies with their own manifest (`machinery/_MACHINERY-MANIFEST.md`).

## Reporting problems

This is early — if something feels off, tell us: what you said (as close to verbatim as you
can), what Claude did, and screenshots if easier. Don't worry about diagnosing the cause.
