# HANDOFF #154 — #303 → #304 — THE DECK WAS FINISHED FOR FRIDAY, AND APOLLO-MCP WAS ASKED FOR

provenance: 303 · 2026-09-24
status: observed

*Written by the delegated OPUS 5.5 wrap seat at the close of #303 (conductor Opus 5.5, a CLOUD session linked to Dave's computer). Every figure here was measured at this seat unless it says otherwise; the lanes' figures are the lanes'.*

⛔ **DATE SPLIT ACROSS THREE DAYS, ONE WINDOW.** Opened Thursday 2026-09-24 13:48 BST, worked to 19:44; one question Friday 2026-09-25 12:43; Saturday 2026-09-26 13:29 to 13:47, then this ritual (`date` at this seat: `Sat Sep 26 12:50:50 UTC 2026`). Keys, filenames and the stratum carry the session date 2026-09-24 (`s294-D11`); the GM header line, the banner, the delta and the stamp carry 2026-09-26.

⛔ **NOTHING WAS INSCRIBED. `knowledge/_rulings.json` READS 638**, by `json.load` over `rulings`: newest `s295-D4`. He never said "inscribe". His words are verbatim in `notes/_lanes/303/WRAP-BRIEF.md` — **quote them; never paraphrase.** His changes to the deck and the prompt are his acts, not rulings.

⛔★ **#304'S FIRST BEAT IS THE APOLLO-MCP PROPOSAL PAGE.** He asked for it on Saturday at 13:29; the research is done and filed; the page was not written because the window was at 392,986.

⛔ **FRIDAY 2026-09-25 HAPPENED. ITS OUTCOME IS NOT IN THIS RECORD.** Ask; do not assume.

⛔ **THE FILL IS A HAND SUM, NOT A `_checkin.py` READING.** Over `/root/.claude/projects/-home-claude/2164dd10-ba27-5634-8eac-5cf4c44aa5e4.jsonl`, at this seat: **boot 128,423** · 165,150 after his 15:37 message · over 200,000 at 16:41 Thu · over 256,000 at 16:59 · **over 300,000 at 18:01 Thu** · **392,986 at 13:42:58 Sat** (the conductor's declared figure) · **402,607 at the wrap** (the message that launched this seat). Over the hard line by 102,607.

---

## ⛔ READ FIRST, IN THIS ORDER

1. **This file.** It is newer than `_CHAIN.md` and **OUTRANKS it**.
2. `_CHAIN.md` — the read contract (header → ★ LATEST banner → ⏱ LATEST delta).
3. ⛔ **It does NOT replace `_HANDOFF-130`…`-153`.** Every open item on those still stands **except the ones struck with receipts** — this wrap strikes FOUR items on `_HANDOFF-153` § OWED (addendum at its foot) and six carries in `_CARRIES.md` § `residual → #304`.
4. `notes/_lanes/303/WRAP-BRIEF.md` — his words, verbatim, in order, with the facts.
5. **For the first beat:** `notes/_subreports/2026-09-26-303-G1-genui-archaeology.md` (the repo's earlier GenUI work and what Apollo can reuse at run time) and `notes/_subreports/2026-09-26-303-G2-agent-ui-landscape.md` (the field, 40 dated sources). The June note they both start from: `notes/_VISION-contextual-dashboard_2026-06-29.md`.
6. `_CARRIES.md` § `residual → #304` when you need the bodies. Fetch the section; do not read it at boot.
7. The other reports, when the work needs them: `notes/_subreports/2026-09-24-303-P-press-animation.md` (lane P) · this wrap's `notes/_subreports/2026-09-26-303-W-wrap.md`.

---

## ⛔⛔ HIS WORDS

**They are in `notes/_lanes/303/WRAP-BRIEF.md`, verbatim, all 31 messages with their BST day and time** — too many to repeat here. The four that set #304's work:

> Sat 13:29 — Can I have this as a page, do you think we could create our own MCP-UI -- Apollo-MCP maybe or something that has the same capabilities as  Google's A2UI and MCP-UI. I think we have to come up with a proposal for this, we also did some work around Gen-UI earlier in the year, I think its time to pull these ideas together, maybe do a bit more research and get this doc together

> Fri 12:43 — so we talked in the past about how we might be able to translate what we have to generating live GenUI, can you find this or let me know how we might use parts of Apollo for realtime GenUI

> Thu 15:46 — […] these are observations that we will role into the graph at some point. If we can not make this to explicit, I don't want it to be a set of instructions as that should be part of the graph and I may share the prompt with the audience.

> Thu 15:51 — cool ill test it later.

> Sat 13:47 — wrap up :)

---

## WHAT THE SESSION FOUND

- **He had already tested the demo prompt** — the conductor's warning that a grill brief might stall was wrong, and it said so. The restructure kept every decided setting and added Common and a data-visualisation section.
- **His three observations belong in the graph, not the prompt** — his stated reason: he may share the prompt with the audience.
- **A picture-by-picture deck session crosses the hard line.** 200K at 16:41, 256K at 16:59, 300K at 18:01 on Thursday, with slide 14's rounds, two commits and the email bundle still to come.
- **The fallback face bit again.** On his screen Univers wrapped slide 14's first title where the seat's fallback did not; the conductor measured with `HSBC_MtUnivers_Latin` forced at 1440, 1728 and 2560 before committing `683f4cca`. The face is still not in the deck's `--font` stack.
- **The email bundle's pack is older than the tree** — Spider v1.0.13 (2026-09-11); seven commits since have touched components or canon.
- **Apollo-MCP has an ancestor in the record** — the July "gates as a service" idea (serve the validators as MCP tools), found by G1.

## WHAT LANDED

| File | Seat | What | Committed |
|---|---|---|---|
| `notes/_lanes/303/DEMO-PROMPT-2026-09-25-hsbc-ceo-common.md` | conductor | the demo prompt, restructured: Common, liberal data visualisation, his three observations as quality expectations | `6c881313` |
| `notes/_lanes/296/C/v14-plain-before-c.html` → `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html` (+ `build_c.py`) | conductor + lane P | 16 slides on his words; five chapters; 12 the new count; 13 "Anatomy of a smart design system" with the fly-through; 14 the 3x2 value grid; 15 "BETA to Enterprise Capability." with the ask parked; 16 the press loop | `6c881313`, `683f4cca` |
| `notes/_DEMO-SLIDES-apollo-2026-09-24-v14-plain-with-slide-11.html` | conductor | the 17-slide copy with old slide 11, at his ask | `6c881313` |
| `notes/_KG-EXPLORER.html` | conductor | rebuilt, v1.27, 4,888 nodes, 8,756 edges | `6c881313` |
| `notes/_lanes/303/P/press.html` · `notes/_subreports/2026-09-24-303-P-press-animation.md` | lane P | the press preview and report | `6c881313` (report under a declared `DOC_ROW_ACK`; row minted now) |
| `notes/_subreports/2026-09-26-303-G1-genui-archaeology.md` · `…-G2-agent-ui-landscape.md` | lanes G1, G2 | the Apollo-MCP research | with the wrap |
| `notes/_lanes/303/WRAP-BRIEF.md` | wrap seat | his words and the facts | with the wrap |
| `notes/_lanes/303/Apollo-Friday-2026-09-25.zip` · `…-without-pack.zip` | conductor | the email bundles | ⛔ never — gitignored, untracked on purpose |
| *the wrap* | wrap seat | this ritual — its sha, push and CI in § POST-WRAP below | — |

Both Thursday commits went on the DECLARED not-a-wrap path and were pushed (`5c132083..6c881313`, `6c881313..683f4cca`). CI runs `36035716214` and `36036092619`, read back by the conductor at 18:59 BST: release ✅, render ✅, gates ⛔ on the inherited six only (`[3] [13] [38] [125] [128] [136]`); logs `notes/_lanes/303/_ci-gates-*.log`, committed with this wrap.

---

## THE STRIKES — BY ADDITION, WITH THEIR RECEIPTS (`s183-D1` / `s188-D2`)

On `_HANDOFF-153` § OWED (addendum at its foot) and in `_CARRIES.md` § `residual → #304`:
- **1 — the demo prompt. STRUCK BY HIS ACT.** His 15:37 words, then 15:46, then *"cool ill test it later."* (15:51); the file is `notes/_lanes/303/DEMO-PROMPT-2026-09-25-hsbc-ceo-common.md`, committed at `6c881313`. Whether it ran is a NEW item.
- **2 — slide 15's Light headwords. STRUCK, SUPERSEDED BY HIS ACT.** He rebuilt the slide as the six-item grid (18:14) under *"Deliver more, faster, at much lower cost"* (18:35); the headwords are parked, not live.
- **4 — "judgement layer" on 13. STRUCK BY HIS ACT.** *"Ditch the large title 'The twelve types of entity in the judgement layer.'"* (15:57).
- **5 — the ask from his colleagues. STRUCK BY HIS ACT.** He gave slide 15 his own copy at 17:12, *"BETA to Enterprise Capability"*; the draft ask is parked in a comment.
⛔ **NOT STRUCK:** 3 the HSBC face in the font stack (the conductor forced it to measure; the stack still does not name it) · 6 the callipers' overrun · 7 everything on `_HANDOFF-152` § OWED.

---

## ⬛ OWED TO #304, IN ORDER — EACH WRITTEN AS THE QUESTION IT IS

1. ⬛★★★ **Write the Apollo-MCP proposal page.** His ask, Saturday 13:29. Swiss-design-system HTML, in the repo beside its sources; give him the path. Build it from G1 and G2 and the June note. The conductor's recommended headline, to put to him, not assume: **don't invent a protocol — publish Apollo as a versioned A2UI catalogue served over MCP, with MCP Apps as the fallback shell; Apollo adds when-to-use from the metas, gates run before anything renders (neither spec mandates accessibility), entitlements enforced at the tool scope, and the knowledge graph as the audit record; the first vehicle is the June note's contextual dashboard.** ⚠ Jev is ruled dev-time only (#294): any run-time judgement must be mechanical. Send long writing to a helper so the window stays clear.
2. ⬛ **Friday — what came back?** Ask at the opener. Not in the record.
3. ⬛ **Did the Common prompt run, and how?** (*"cool ill test it later."*)
4. ⬛ **His three observations into the graph** — the bento ground, components at their own size, the lightest pattern over a modal. His item, "at some point".
5. ⬛ **Which Spider pack is on his work machine?** Asked Thursday 19:44, unanswered.
6. ⬛ **Add `HSBC_MtUnivers_Latin` to the deck's font stack?** His call (`_HANDOFF-153` item 3).
7. ⬛ **The callipers overrun the frame by ~50px at the extreme orbit corner — leave, or reframe?** (`_HANDOFF-153` item 6.)
8. ⬛ **Everything still standing on `_HANDOFF-152` § OWED** — inscribe his window words? · the stop and tolerance lines under the 256K working line · which of the 26 review suggestions · `_standing.md:19`'s wording · the boot ceiling and the declared path · after Friday (the chain, the plan page's six steps and seven questions, the Mac seat) · the two stale runbook lines and the token in the remote URL · the rest of `_CARRIES.md` § `residual → #304`, each at its true age.

---

## THE PLAIN DECK — HOW TO EDIT IT (now 16 slides)

`notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html`, 16 slides, **GENERATED** by `notes/_lanes/296/C/build_c.py` from the SOURCE `notes/_lanes/296/C/v14-plain-before-c.html`. Parked, not deleted: old slide 11 in `<template id="parked-s6b">`; the one- and two-slide value versions in `<template id="parked-s11-two-slides">`; the draft ask in a comment inside `#s11`. ⛔ **Edit the source, never the deck. Never run `notes/_lanes/296/E/build_e.py`.** ⚠ **The rail's chapter titles live in `build_c.py` (`PLAIN_CHAPTERS`, five chapters), not in the source.** Render on the mount in one call: `export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh; python3 <driver>` with `executable_path=$RENDER_SHELL`. ⚠ **The seat's renders fall back from Univers Next** — judge type on his screen, or force `HSBC_MtUnivers_Latin` in the driver and say so.

---

## ⚠ THINGS A COLD SEAT SHOULD KNOW BEFORE IT TOUCHES ANYTHING

- ⛔★★ **NEVER RUN `git status`**, and **`python3 knowledge/_capture_gate.py --wrap` strands `.git/index.lock` on this mount** — the seventh wrap running (#297–#303); `git reset -q` then strands `HEAD.lock` and `refs/heads/master.lock`. Move stranded locks to `notes/_lanes/_orphan-locks/` with a unique suffix, `git reset -q`, move again, then run `_git_commit.sh` ONCE. Read-only git: `git --no-optional-locks`.
- ⛔ **`device_bash` kills background jobs when the call returns** — run the gate in the foreground with the longest timeout.
- ⛔ **Project memory: none at the opener, none while the chat is live.** The note is placed only after he says he is done.
- ⛔ **The window lines: working 256,000, hard 300,000 (his, #301); stop 180,000 and tolerance 220,000 unmoved. `BOOT_CEILING_TK` 72,768:** a `--wrap` commit is refused by the wrap gate's boot-ceiling arm; the legal path is `_git_commit.sh` WITHOUT `--wrap`, DECLARED not-a-wrap in the message body.
- ⛔ **#303 ran to 402,607.** Writing a proposal page is long work: brief a helper to write it in its own window, and keep the conductor's turns short.
- ⛔ **THE FILL IS A HAND SUM over the cloud transcript** (`input_tokens + cache_creation_input_tokens + cache_read_input_tokens` per distinct `message.id`). A delegated sub shares the container and can read it.
- ⛔ **`_git_commit.sh` needs `SESSION_N=304`** and a msgfile whose line 1 has no `after #N` or `#N date —` prefix; write msgfiles with python. **The doc-row gate refuses a new report without a `_state` row** — mint the row, or pass `DOC_ROW_ACK` with the real reason, and say which. **`_state.add()` refuses a row whose `home` does not exist**; mint rows and regenerate `_CHAIN.md` BEFORE the first commit attempt.
- **`pip install tiktoken --break-system-packages` FIRST.**
- ⚠ **Other-seat paths stay dirty by declaration** (`notes/_dream/_GRADE-DECISIONS.jsonl` · `notes/_lanes/293/J7-IDEA-jev-selects-over-the-kg.md` · `notes/_lanes/294/WRAP-MEMORY-HOOK.md` · #297 lane A's report tail · `notes/_context/2026-09-24-302-context-curve-dave-paste.md` · the untracked nested `UX-design/` folder · untracked lane work under `notes/_lanes/297`–`303`, including #303's `P` work files and frames, `shots` and eight source backups); the two email zips are gitignored. Pushes go by plain `git push origin master`, DECLARED, after checking the branch and fast-forward.

---

*Filed report: `notes/_subreports/2026-09-26-303-W-wrap.md`. Dossier: `_DECISION-HISTORY/2026-09-24-303-the-deck-was-finished-for-friday-and-apollo-mcp-was-asked-for.md`. Memory hook: `notes/_lanes/303/WRAP-MEMORY-HOOK.md`. His words and the facts: `notes/_lanes/303/WRAP-BRIEF.md`.*

*Title the next chat:* `Apollo - #304: the Apollo-MCP proposal page`
