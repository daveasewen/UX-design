# Your first session

Welcome. This walks you through the first twenty minutes with Apollo and Memento, end to end:
one thing built, one decision recorded, one session properly closed.

Work through it with Copilot open in the chat panel. Every command below is one Copilot can
run for you — you can hand it this file and say *"walk me through this"*, or run them
yourself in the VS Code terminal. Both work.

---

## What Memento is, in three sentences

An AI assistant starts every session with no memory of the last one. Memento is the discipline
that fixes that: each session writes a short record before it ends, and the next session reads
that record first — so the work continues instead of restarting.

The film it is named for is the useful part. Leonard cannot form new memories, and what saves
him is not writing everything down; it is knowing which handwriting to trust — **tattoos** for
the few things that must never be wrong, **Polaroids** for the day's working notes. His real
enemy was never forgetting. It was the confident thing written in permanent ink and read back
the next morning as truth.

So Memento keeps those two apart on purpose. A decision you have settled goes in the rulings
store and is never quietly reworded. A note about today goes in the chain and rolls away when
it stops being today. Nothing in between gets promoted by accident.

---

## Before you start

You need Python 3 and VS Code with GitHub Copilot. There is **one Python package**, and it is
recommended rather than required — see below. No account and no API key.

    pip install tiktoken

**Recommended, not required.** Step 4 of this session regenerates the chain — the file that
makes tomorrow's "good morning" work — and the generator that writes it **refuses to write
anything at all** unless it can count tokens exactly. It will not guess and then label the
guess. Without `tiktoken` it still counts exactly, with the encoder this pack carries itself,
and it says which one it used; `tiktoken` is simply several times faster.

**The encoder's data file is already inside this pack.** Normally `tiktoken` downloads it, once,
from `openaipublic.blob.core.windows.net` — a host that is blocked on plenty of corporate
laptops, and when it is blocked the chain step refuses. So the pack ships that data itself, in
`memento-package/_encoder-cache/`, and finds it on its own. **There is nothing for you to
download and no environment variable to set.** The `pip install` line above is for the `tiktoken`
package itself, which still comes from PyPI; the *data* it would otherwise fetch is already here.

Open **this pack's folder** as your VS Code workspace (File → Open Folder → the unzipped
`Apollo-Spider-v1.0.3` directory). Copilot reads `.github/copilot-instructions.md` from a
workspace automatically, and that file is what tells it how to behave here.

Quick check that everything landed — **both lines, before you start**:

    python3 memento-package/_state.py
    python3 memento-package/machinery/_encoder_home.py --check

The first should print a row of zeroes. That is your empty worklist reporting in — it is meant to
be empty, and the fact that it answers at all is the check.

The second should end with:

    ENCODER OK — engine: tiktoken cl100k_base — 4 tokens, measured with the encoder data inside this pack (no download, no environment variable to set).

It does not describe the setup, it drives it: it finds the vendored data, checks it is the right
bytes, points `tiktoken` at it, and then actually encodes a string. **It names the engine it
used**, every time — a token count whose method is unstated is the one thing this pack will not
print. **It needs no network at all** — if it passes on a machine with the internet unplugged,
that is the intended result, not a surprise. Anything else it prints starts with `ENCODER-HOME:`
and names the exact file it looked for and what it wants you to do. If it refuses, fix it here:
everything else in this session works without it, but the last step does not.

**If `tiktoken` is not installed, this check still passes** — and it will say so, naming a
different engine: `purepy cl100k_base (exact, equality-gated)`. That is the pack's own encoder,
written in plain Python over the same vendored data. It is exact, not an estimate: it runs the
same pretokenizer and the same byte-pair merges, and the pack carries the gate that proves it —

    python3 memento-package/machinery/_encoder_home.py --equality-gate

which drives both encoders over this pack's own text and refuses on the first token they
disagree about. It is a few times slower than the real library, which is why the `pip install`
line above is still the recommended path.

### One more thing to switch on — the session gauge

**⚠ Two different token counts live in this pack, and confusing them is the mistake to avoid.**
The check you just ran measures **a piece of text** — a file, a document, the chain. It does not
and cannot tell you **how full this session is**. That second question needs a different
instrument, and it is not one this pack computes: it is a number GitHub Copilot's own server
already reports, which you have to turn the log on to see.

This pack ships those settings for you, in **`.vscode/settings.json`** at the pack root. Opening
this folder as your workspace picks them up. They ask Copilot's agent to write its debug log to a
file — the log that carries the server's reported token usage for your session — and they set the
automatic-compaction guard at 220,000 tokens. **Reload the window once** (⇧⌘P / Ctrl+Shift+P →
*Developer: Reload Window*) so the agent starts with logging on.

⚠ **These settings are shipped on one machine's evidence, not on ours.** They were found working
on a locked-down corporate laptop; we have no Copilot to drive them in. If your Copilot version
has renamed a key, VS Code's settings editor will show it greyed out — search Settings for
`agentDebugLog` and use whatever it is called now. **If the log never appears, nothing here
breaks**: you simply do not have the reading, and you say so rather than guessing a number.

`memento-package/runbooks/_RUNBOOK-context-gauge.md` § *Taking the reading by hand* is the whole
procedure: where the log is (find it with *Developer: Open Extension Logs Folder* — the path is
undocumented and we deliberately do not write one down), what the number means, and how to use it
as an early warning that a session is going stale. Read it before your first long session, not
during one.

---

## Step 1 — build something small

Do not start with the memory system. Start with the thing you came for.

Pick one component from the library and put it on a page. Open `showroom/index.json` to see
what is in there, or just ask Copilot:

> *Show me the button component's reference markup and its contract.*

The **reference markup** (`knowledge/snippets/`) is what correct looks like — reviewed HTML you
can copy. The **contract** (`knowledge/components/*.meta.json`) is the rules that go with it:
which props exist, which variants are real, which token each part is bound to, and what the
anti-patterns are. Between them they answer most questions before you have to ask one.

Make a page. Use it. Change a colour and see what breaks. Ten minutes is plenty — you just
need something real to have an opinion about.

---

## Step 2 — your first capture

Something happened. Write it down before it evaporates.

Capture is not "save a transcript". A transcript is the haystack; capture is the needle you
pull out of it. In practice it is three questions:

1. **What is now true that was not true this morning?**
2. **What did you decide, and what did you decide against?**
3. **What is the next person — you, on Monday — going to wish they had been told?**

For now, just answer them in the chat and let Copilot draft them. They become the two short
files that Step 4 writes. You are not writing them yet; you are noticing that you have
something worth writing.

---

## Step 3 — your first ruling

A **ruling** is a decision you do not want re-opened by accident. Not every choice deserves
one. The test is simple: *would it cost me an argument, or an afternoon, if someone quietly
changed this back?* If yes, rule it.

Say your page had three different reds in it and you decided error states get exactly one.
That is a ruling.

**You never write to the rulings store by hand.** There is one way in, and it refuses anything
malformed before a single byte is written. Create the entry as a file — `my-ruling.json`,
anywhere convenient:

```json
{
  "id": "d1-D1",
  "ruled": "OUR ERROR COLOUR IS ONE COLOUR, AND IT IS NEVER USED FOR ANYTHING ELSE",
  "date": "2026-08-26",
  "by": "me",
  "says": "We picked one red for errors and one only. It does not double as a brand accent, a chart series or a hover state. If a red appears anywhere that is not an error, it is a bug.",
  "governs": ["knowledge/tokens/", "knowledge/snippets/"],
  "evidence": ["chat #1 - first session, after finding three different reds on one page"],
  "status": "ruled"
}
```

Every field earns its place:

- **`id`** — how you will cite it later. Any scheme you like, as long as it is unique. `d1-D1`
  reads as "day one, decision one"; a lot of people just number them.
- **`ruled`** — the decision in one line, loud enough to recognise at a glance.
- **`says`** — the same decision in plain words, with enough of the reasoning that future-you
  does not have to guess why.
- **`governs`** — the files this decision touches. This is the part that does the work: the
  next time anyone edits something under these paths, the decision can be put back in front
  of them instead of waiting to be remembered.
- **`evidence`** — where the decision actually happened. Three forms are accepted: `chat #<n>`,
  `commit <sha>`, or a path to a file that exists. Nothing else, and the reason is that a
  pointer which does not resolve is worse than no pointer.
- **`status`** — `ruled` for a settled one.

Prove it would land cleanly, without writing anything:

    python3 memento-package/_inscribe_ruling.py --entry my-ruling.json --dry-run

If something is wrong it says exactly what, names it, and touches nothing. When it is happy:

    python3 memento-package/_inscribe_ruling.py --entry my-ruling.json --write

Read it back — that is your record now, and it is one entry long:

    python3 -c "import json;print(json.load(open('memento-package/_rulings.json'))['rulings'][0]['ruled'])"

**A note on changing your mind.** You will. When you do, you add a *new* ruling that supersedes
the old one — you do not edit the old one. Both stay readable, and six months later the trail
of why still exists. That is the whole reason this file is written to by a tool that refuses
rewrites rather than by hand.

---

## Step 4 — your first wrap

The wrap is the part that makes tomorrow cheap. It takes a few minutes and it is not optional
in spirit: a session that ends without one has, from the next session's point of view, not
happened.

**a. Add what is still open to your worklist.** Anything unfinished goes in the task store,
and it has to say what would make it done — the tool refuses an item that does not, and that
refusal is the feature. A list of things with no finish line only ever grows.

```
python3 - <<'PY'
import sys; sys.path.insert(0, "memento-package")
import _state
doc = _state.load()
_state.add(doc,
    id="W-01",
    title="Finish the error-state page",
    project="apollo",
    body="Three reds found and one chosen; the page still uses the old two in the toast and the inline field error.",
    state="open",
    opened=1,
    owner="claude",
    closes_when="both remaining reds are replaced with the ruled error colour and the page renders clean",
    links=[],
    home="FIRST-SESSION.md",
    condition="stated",
)
_state.save(doc)
print("added")
PY
```

Two fields will look odd on day one, and the honest answer is that they are ours, not yours:
`project` accepts only `apollo` or `memento`, and `owner` only `dave` or `claude`. They are a
closed list so that filters never silently drop a row to a typo. Use `apollo` and `claude` for
now — the label is not doing anything you need it to do yet.

`home` must point at a file that actually exists, relative to the pack root. That is deliberate:
a task pointing at a file that has been deleted or renamed is a task nobody can act on, and the
store would rather tell you now.

Check it took:

    python3 memento-package/_state.py

**b. Write the two state files.** These go in `memento-package/`, and the chain generator reads
them by their exact headings — so use these skeletons rather than inventing your own. The
markers (`> ## ★ LATEST`, `## ⬛ DO THIS FIRST`, `## ⏱`) are what it looks for; the words
between them are entirely yours.

`memento-package/GOOD-MORNING.md` — where the project stands:

```markdown
# Good morning — 2026-08-26

> ## ★ LATEST — chat #1 2026-08-26
>
> What this session did, in the terms someone arriving cold would need. Two or three
> sentences. Name anything you ruled and anything you opened.

## ⬛ DO THIS FIRST

> **1. The next thing to pick up** — one line each, the open work in priority order. `W-01`.

> **TITLE THE NEXT CHAT →** `#2 — the error-state page`

# §A — standing

Things that are true about this project generally, rather than about today.
```

⚠ **Keep the `TITLE THE NEXT CHAT` line, and keep its number one ahead of `★ LATEST`.** The
generator lifts it to the very top of the chain, so tomorrow's session is told what to call
itself before it reads anything else — the chat half of the ritual is the half no gate can
check, which is why the line goes first. Get the numbers out of step (say `#5` when `★ LATEST`
is `#1`) and the generator refuses rather than publishing a wrong one: that is the *skipped
wrap* it is watching for. Leave the line out and `--selftest` reports two bites unmeasured,
which is honest but less useful than having it.

`memento-package/_LIVE-STATE.md` — what changed today:

```markdown
# Live state

Last refreshed: 2026-08-26

## ⏱ LATEST DELTA — chat #1 2026-08-26

- What you built.
- What you decided, and its ruling id.
- What you opened, and its item id.
```

⚠ **Keep the `## ⬛ DO THIS FIRST` section, even when it is one line.** Without it the chain
prints a warning saying it cannot see your open work — which is correct and honest, but it
means the next session has to go looking. With it, every open item is named in the chain
automatically.

Ask Copilot to draft both from your Step 2 answers. They do not need to be long. They need to
be *current* — a beautiful handoff written from memory at the end of an exhausting session is
the confidently wrong one you most want to avoid, which is why you write them while there is
still room to write them well.

**c. Regenerate the chain.**

    python3 memento-package/machinery/_gen_chain.py

This reads those two files and writes `memento-package/_CHAIN.md`, replacing the starter chain
that shipped with the pack. From now on the chain is generated and must never be hand-edited —
anything typed into it is silently overwritten, which is exactly the confident false inscription
this whole system exists to prevent.

Confirm it is current:

    python3 memento-package/machinery/_gen_chain.py --check

⚠ **The generated chain is written in Apollo's voice.** Its wrapper text was authored for the
design system's own record and mentions decisions, sessions and file paths that belong to that
project, not to yours. Your session's words are the part between the `★ LATEST` and `⏱` markers
— that is the bit that is about you. The wrapper is scenery for now.

⚠ **This is the step that needs `tiktoken`** (§ Before you start). If it is missing, the
generator prints a MEASUREMENT REFUSAL, exits 1 and — deliberately — **writes nothing**: every
size figure it would bake into the file would have been measured on the wrong instrument, and a
file full of confidently wrong numbers is worse than no file. There is no estimate fallback. If
you see that refusal, run `pip install tiktoken`, re-run the two checks in § Before you start,
then come back here. Nothing you did in Steps 1–3 is lost.

⚠ **A blocked network is not a reason for this step to fail.** The encoder data ships inside the
pack, so this step works with the internet unplugged. If the refusal above is preceded by lines
beginning `ENCODER-HOME:`, the vendored data itself is missing or damaged — those lines name the
exact file. Restore it from a fresh copy of the pack, or point `TIKTOKEN_CACHE_DIR` at a
directory that has it; your own value for that variable is always respected.

---

## Step 5 — come back tomorrow

Close VS Code. Come back later. Open the folder and say **"good morning"**.

Copilot reads the chain, tells you where things stood, and asks what you want to do next. If
that lands — if it picks up the thread without you re-explaining anything — the system is
working, and everything after this is just doing it again.

---

## Where to go next

| you want to | open |
|---|---|
| understand the idea properly | `memento-package/WHAT-MEMENTO-IS.md` |
| close a session well, every time | `memento-package/runbooks/_RUNBOOK-capture-ritual.md` |
| know when to stop before you run out of room | `memento-package/runbooks/_RUNBOOK-context-gauge.md` |
| build a component correctly | `knowledge/_RUNBOOK-compose-from-canon.md` |
| check your work against the design system | `skills/check-against-design-system/SKILL.md` |
| run the real gates over your project | `python3 ci-template/run-gates.py` |

---

## If something goes wrong

Everything here fails loudly and by name. A tool that refuses will tell you what it refused
and why, and will not have written anything. That is the design: a silent success you cannot
verify is worse than a noisy refusal you can read.

If a message does not make sense, the most useful bug report is: what you said, what it did,
a screenshot — and two more lines that decide most of them: the lane the assistant declared
in its first reply, and the brief from `briefs/`. `cold-start/REPORT-TEMPLATE.md` is that, as
four boxes. Do not worry about diagnosing it.
