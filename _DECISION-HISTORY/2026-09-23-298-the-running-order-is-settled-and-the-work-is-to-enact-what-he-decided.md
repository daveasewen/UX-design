# #298 — the running order is settled, and the work is to enact what he decided

provenance: 298 · 2026-09-23
status: observed

*Narrative dossier (capture ritual step 1b), written by the delegated Opus 5.5 wrap seat. The WHAT lives in `_LIVE-STATE.md`'s #298 ⏱ delta and `_HANDOFF-149-the-running-order-is-settled-and-the-work-is-to-enact-what-he-decided.md`; this file holds the WHY and HOW. His words are quoted from `notes/_lanes/298/DAVE-WORDS-AND-BOOT-FINDING-2026-09-23.md`, never paraphrased. Spine: `_LIVE-STATE.md` § ⏱ LATEST DELTA #298. Ledger: none — nothing was inscribed (`knowledge/_rulings.json` stays 638).*

---

## 1. The session was short, and the window was not

#298 opened on a cloud seat at 11:08 BST (the first message at 10:08:34 UTC) and the first turn already cost **127,661** real tokens. The opener did what `_HANDOFF-148` asked: it read the handoff and `_CHAIN.md`, placed #297's memory hook in the Project memory, moved #294's index line to the archive, and gave the presentation area file his *"plain"*. That took the window to **176,116** by the fourteenth message. When his first message arrived the chat had about 74K left before the hard line (256,000), and by 11:58 about 13K. **The conductor called the wrap rather than start work it could not finish.** Why that mattered: his 11:58 message was not a wrap call. It was a list of work.

## 2. Claude Docs, which he did not ask for

His first message of the session was about the tools, not the deck:

> claude docs seems to initiate every new session, this is out of order in my opinion. There is a remove button but I get this message. it seems this MCP cant be disconnected permanently. can you do some resaerch

Lane A researched it (`notes/_subreports/2026-09-23-298-A-claude-docs-connector-removal.md`). The finding, in plain words: **Claude Docs is not a connector he added.** It is one of Anthropic's own features, a document type like Slides and Design, so the Remove button on the connector list is the wrong switch. The documented off switch is **Settings > Capabilities**. The "Failed to remove server" error matches a public bug report about a different built-in server (anthropics/claude-ai-mcp #509), with no fix. **No source says the switch keeps the tools out of new sessions** — that is a test, and it is owed at #299's opener.

He asked *"would blocking the tools help?"* and set all eight to Blocked. The Docs server disconnected from the session a few minutes later. Whether his block caused that is not known.

## 3. The boot: where the jump came from

> but where did the big jump come from? we went for 72-ish to 128 in on previous session and it was 50-ish before then

> either the boot or the wrap is to blame

The conductor answered by measuring, not by guessing. Three cloud chats (#297's two, and #298) booted at **127,609**, **127,600** and **127,661** — within 61 of each other. The last desktop seat, #295, booted at **72,768**. So the step from 72K to 128K arrived with the move to the **cloud seat**. It is a fixed cost of that seat, not of the wrap.

The wrap's real share is smaller and different: the opener's reads (about 48K), and one surprise — **when the opener wrote to the memory store, the next message re-sent the whole memory listing and the skills list**, which added about 25K to a one-line message. That is a cost the opener's own design creates, and it is owed a look after Friday.

The earlier step, from about 50K to 72K, was already on file: the Cowork feature blocks of late August (`areas/boot-three-bands-293`).

*This is the conductor's reading. It is not his ruling, and what is inside the 127K is still not attributed.*

## 4. His answers to #297's open five

At 11:38 he answered, and the first thing he said was:

> Okay, this is not helpful from claude.

Then, one by one: slide 12's two lines *"this is fine"*; the laptop headlines *"lets get the structure right and then we'll deal with polish"*; the 07 count line *"do it"*; his demo-brief changes *"we'll do that last"*. On the brain he said *"I haven't seen these"* — the three readings had been made at #297 and never shown to him. They were shown inline in the chat (a PNG rendered in place, not a download, which is the first time that worked). He picked **"B"**.

**Why the 07 line needed nothing:** the #297 wrap seat had already enacted it on a reading of *"okay lets get this executed"* (`81541832`). His *"do it"* confirmed the reading. Nothing was built.

## 5. The brain turns to B

Lane B (`notes/_subreports/2026-09-23-298-B-brain-turn-B.md`) proved that reading B is exactly one constant — the brain's resting yaw, −35 → −27 — by diffing lane A's own variant file against the committed source. It changed that one line in the source, rebuilt the deck with `build_c.py`, and rendered every slide at both sizes before and after. Only slides 10 and 12 changed, and on 12 only the Judgment thumbnail, which draws from the same brain. The trade-off, which he saw before he picked: the brain's plate now sits off the parallel the other drawings share. Committed as `f54562e2`, not pushed until this wrap.

## 6. The real instruction

> the running order is fine, we just need to enact the changes I've decided, the only real change is the new chapter Evolution after Evaluation.
> we need to do all the copy changes and style changes for the diagrams

This is the most important thing #298 produced, and it is short. **The running order is settled.** The one structural change he wanted — the Evolution chapter after Evaluation — already landed at #297. What is left is to **enact the copy changes and diagram style changes he has already decided.**

The difficulty, and the reason it is #299's first job rather than a quick one: those decisions are spread across #297's record — his words file, the five lane reports and the 37-item review page — and **nobody has yet listed which are decided but not enacted.** A lane that starts enacting before that list exists will enact something he did not decide, or miss something he did. So: reconcile, show him the list, then enact.

## 7. What the wrap met

The wrap gate refused at open on one thing: `_to_delete/.DS_Store`, a Finder file written when he emptied that folder at #294, now four sessions old against his *"N+3"* rule. The gate names it and stops, because the mount cannot delete. The wrap seat asked through the delete-permission request, it was granted, and that one file was deleted. Finder will write another the next time the folder is opened. Whether the rule should ignore Finder's own files is his.

The same gate also stranded `.git/index.lock` again, as it did at #297. It is now a known lock-stranding command on this mount, like `git status`.

## Resolved, and still open

**Resolved:** the brain's pivot (B) · slide 12's lines (kept) · the 07 line (confirmed) · the running order (settled) · where the boot jump came from (the cloud seat — a reading).
**Still open:** which decided changes are not enacted, and enacting them · the ask on slide 15 · the laptop headlines (after structure) · his demo-brief changes (last) · whether his Claude Docs block holds at the next boot · the cloud-seat boot and opener cost.
