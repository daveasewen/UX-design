# Copilot instructions — Apollo, and Memento

These instructions govern how you (GitHub Copilot) behave in this workspace. Follow them exactly.

This workspace is the **Apollo — Spider** pack: a working design system, plus **Memento — Gumdrop**,
a memory discipline that lets each session pick up where the last one stopped. Your job is to help
the person here **build with the system and keep the record** — in that order.

---

## The boot rule

On the first **"good morning"** (or the first message of a session, however it is phrased), do this
before anything else:

**Look for `memento-package/_CHAIN.md`.** What you find puts you in one of three arms.

### Arm 0 — the chain is still the STARTER chain

Open it and check the first line. If it begins with the comment marker
`<!-- MEMENTO-STARTER-CHAIN:` then this pack has never been used: the chain shipped with it and
nothing has been written yet.

Do this:

1. **Give the orientation in your own words**, briefly. What Memento is: each session writes a
   short record before it ends, and the next session reads that record first, so context survives
   without re-reading the whole project every morning. Do not lecture. Three or four sentences.
2. **Point at `FIRST-SESSION.md`** at the workspace root and offer to walk them through it. It is a
   guided twenty minutes: build one thing, record one decision, close the session properly.
3. **Ask what they want to build.** If they would rather start building than do the walkthrough,
   that is a perfectly good answer — help them build, and come back to the record at the end of the
   session. Do not insist on the tour.

⛔ Do not treat the starter chain as a real record. It carries no project state, and summarising it
back to them as though it did is the exact failure this arm exists to prevent.

### Arm 1 — a real chain exists

The ordinary case, every session after the first. Read `memento-package/_CHAIN.md`. It is generated,
and it is the whole contract — the header, the ★ LATEST banner and the ⏱ latest delta. If you have
read it, you have read what you need to orient. Then get to work on whatever it points you at.

### Arm 2 — there is no chain file at all

Someone deleted it, or this is a fresh project directory. Say so plainly, then either regenerate it
(`python3 memento-package/machinery/_gen_chain.py`, if `GOOD-MORNING.md` exists) or treat the session
as a first boot and follow Arm 0.

---

## Operating rules

- **Read the chain only, at boot.** Do not open `GOOD-MORNING.md` or `_LIVE-STATE.md` "just to
  check" once you have read the chain. That reflex defeats the whole point of generating a small
  chain file — you would pay the cost of the large files every session, which is exactly what the
  chain exists to prevent.
- **Retrieval is on demand, never a reading list.** For anything beyond the chain, search:
  `python3 memento-package/machinery/_memento_search.py "<query>"`, then `--fetch <id>` on whatever
  result you actually need. Ask for what you need. Do not read a file to find out whether you needed
  it.
- **Never invent a component, a variant, a colour or an icon.** If the design system does not have
  it, say so and flag the gap. The skills below exist to make that the easy path.
- **Never hand-edit a generated file.** `memento-package/_CHAIN.md` is generated from
  `GOOD-MORNING.md` and `_LIVE-STATE.md`. `memento-package/_rulings.json` is written only by
  `_inscribe_ruling.py`. `memento-package/_state.json` is written only through `_state.py`. Anything
  typed into them by hand is either overwritten silently or rejected loudly, and the first of those
  is much worse.
- **A refusal is information, not an obstacle.** These tools fail loudly, by name, and without
  writing. When one refuses, read what it refused and why, and fix that — do not route around it.
- **Close the session.** See "The wrap", below. A session that ends without one has, from the next
  session's point of view, not happened.

---

## The skills, and when to reach for one

⚠ **These are not auto-loaded — you have to open them.** The five files under `skills/` are written
instructions, not extensions. When a request matches one of the rows below, **read that `SKILL.md`
first and then follow it.** Each is also available as a slash command (`/generate-from-canon` and so
on) via the prompt files in `.github/prompts/`.

| when the request is… | open |
|---|---|
| build a screen or component from the design system, without inventing anything | `skills/generate-from-canon/SKILL.md` |
| the system is missing something and we need a new pattern that still fits | `skills/draft-a-new-pattern/SKILL.md` |
| does this conform? where has it drifted from the system? | `skills/check-against-design-system/SKILL.md` |
| prove it mechanically — run the real checks over the work | `skills/check-with-gates/SKILL.md` |
| is this actually usable? heuristic review of a screen or flow | `skills/usability-review/SKILL.md` |

The pairing worth knowing: **`check-with-gates` measures, `check-against-design-system` judges.** Run
the gates first — they are cheaper and more certain than reading — then spend attention on what a
gate cannot see.

---

## The design system, in the order you will need it

| | |
|---|---|
| `knowledge/snippets/` | reviewed reference markup — what correct looks like. Copy from here. |
| `knowledge/components/*.meta.json` | one contract per component: props, variants, token bindings, states, anti-patterns, accessibility |
| `knowledge/tokens/` | every design token, and the four theme override sets |
| `knowledge/canon/` | `canon.css` and `type.css`, plus the generators that mint them |
| `knowledge/compliance/` | which accessibility criteria apply to which component |
| `knowledge/_RUNBOOK-*.md` | the procedures — compose from canon, gate a component, render and verify |
| `showroom/` | the live library, browsable |
| `ci-template/` | a workflow to copy into the project's own repo, so the gates run on every push |

⚠ **The canon generators can produce canon that never passed a gate.** They ship because this is the
working engine, not a baked copy of one. If a token is changed and canon re-minted, run
`python3 ci-template/run-gates.py` afterwards — that is what says whether what was just minted still
holds up.

---

## The wrap

At the end of a working session, run the sequence in
`memento-package/runbooks/_RUNBOOK-capture-ritual.md`. In short:

1. Put anything still open into the worklist (`memento-package/_state.py`), each item saying what
   would make it done.
2. Inscribe anything that got *settled* as a ruling — via
   `python3 memento-package/_inscribe_ruling.py --entry <file>.json --dry-run` first, then `--write`.
3. Update `memento-package/GOOD-MORNING.md` (where the project stands) and
   `memento-package/_LIVE-STATE.md` (what changed today).
4. Regenerate the chain: `python3 memento-package/machinery/_gen_chain.py`.
5. Confirm it is current: `python3 memento-package/machinery/_gen_chain.py --check`.

**Do not wait to be asked.** When a session has been running long enough that you are starting to
lose the thread of it, say so and offer to wrap — before the quality of the handoff starts to
suffer, not after. `memento-package/runbooks/_RUNBOOK-context-gauge.md` explains how to judge that
in this environment, and is honest about what cannot be measured here.

---

## Filenames are fixed in this version

`memento-package/GOOD-MORNING.md`, `memento-package/_LIVE-STATE.md` and
`memento-package/_CHAIN.md` are this package's convention for where the header, the ★ LATEST banner
and the ⏱ latest delta live. They are not configurable in this version — use those exact paths.
