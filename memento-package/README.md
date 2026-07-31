# Memento

Memento is a lightweight memory and continuity harness for AI coding assistants. The problem it
solves: an assistant that starts every session with no memory of the last one either re-reads
everything from scratch (slow, expensive) or forgets what mattered (risky). Memento fixes this
with three small pieces working together — a **chain** (a short, generated file that carries
just the last session's header and outcome, so a cold session can orient cheaply instead of
re-reading a large project file), **retrieval** (a search tool for pulling in anything else on
demand, rather than reading a pile of files "just in case"), and **capture** (the discipline of
writing that outcome down at the end of a session, so the next one has something worth reading).
Together, each session ends by leaving a record the next one boots from.

This package is the standalone version of that harness, built for GitHub Copilot in VS Code.

## What's in the folder

```
memento-package/
├── README.md                    — this file
├── _PACKAGE-SPEC.md              — the design spec and scope boundary (background reading)
├── .github/
│   └── copilot-instructions.md   — the boot instructions Copilot reads automatically
└── machinery/
    ├── _gen_chain.py              — generates and checks the chain file (_CHAIN.md)
    ├── _capture_gate.py           — small support module _gen_chain.py needs to run
    ├── _memento_search.py         — retrieval: search + fetch anything not in the chain
    ├── _search_core.py            — shared search logic
    ├── _consult-lexicon.json      — search vocabulary
    └── _MACHINERY-MANIFEST.md     — where each file came from (background reading)
```

You shouldn't need to open anything in `machinery/` day to day — Copilot runs those scripts for
you, per the instructions in `.github/copilot-instructions.md`.

## Quick start

1. Unzip this folder somewhere on your machine and open it in VS Code, with GitHub Copilot
   running.
2. Copilot reads `.github/copilot-instructions.md` automatically — you don't need to do
   anything to wire it up, just make sure Copilot is active in this workspace.
3. Say **"good morning"** to Copilot.
4. First time in this folder, there's no chain yet, so Copilot will explain what Memento is and
   then ask you a two-option question: whether you want to work on an existing project together,
   or start something brand new. Answer either way — that's the whole first-boot flow.
5. From then on, saying "good morning" picks up wherever the last session left off.

**Optional health check:** once you've had at least one session (so the project has its
`GOOD-MORNING.md`), run `python3 machinery/_gen_chain.py --selftest` from the project root. All
bites should pass. Run from a bare, fresh unzip it will report "GOOD-MORNING.md is missing" —
that's expected, not a fault: there's no project content yet for it to check.

## What to try

- Work with it for a session, then close VS Code and come back later. Say "good morning" again
  and see whether it picks up the thread without you having to re-explain anything.
- Ask it something that isn't in the chain and watch it retrieve rather than guess — it should
  reach for `machinery/_memento_search.py` instead of reading files speculatively.
- Peek at `_CHAIN.md` after a session ends, to see what actually got carried forward.
- Try editing `GOOD-MORNING.md` or `_LIVE-STATE.md` by hand and then not regenerating the chain —
  see if Copilot notices the chain has gone stale.

## Reporting problems

This is early — if something feels off, tell us. The most useful report includes:

- **What you said** to Copilot (as close to verbatim as you can manage).
- **What it did**, including anything that looked wrong, confusing, or just didn't happen.
- **Screenshots**, if it's easier to show than describe — very welcome, not required.

Don't worry about diagnosing the cause — just describe what you saw. We'll take it from there.
