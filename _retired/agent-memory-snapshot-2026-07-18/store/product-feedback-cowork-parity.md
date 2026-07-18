---
name: product-feedback-cowork-parity
description: "Dave's product-feedback thread — Cowork↔Code slash-command parity (double-slash idea) + 'beta cloud ran better' than the current cloud+device-bridge (which flakes)"
type: project
---

**Product feedback (Dave, 2026-07-14) — Cowork ↔ Code feature parity.**

**Firm ask:** *"we need slash commands in Cowork too."* Dave wants the Claude **Code** slash-command
surface (e.g. `/workflows` live progress view, `/model`) available in **Cowork**, because the gap is a
friction point in **transitioning from Cowork to Code**. Trigger was me suggesting he "watch live via
`/workflows`" — a Code-only feature that isn't in his Cowork UI.

**His idea (PROVISIONAL — thinking out loud, "hmmmm"):** Cowork's single `/` is already taken (it's a
**file/skill picker**, not a command runner). So maybe a **double-slash `//`** in Cowork could invoke the
Code-style slash-commands — a separate namespace that avoids colliding with the existing `/` picker.
*Don't harden this into a spec — exploratory (per [[feedback-clarify-reflect-back]]).*

**"Beta cloud ran better" (Dave, 2026-07-14, firm — repeated across sessions).** Dave's clear read is that
an **earlier beta cloud experience ran better** than the **current cloud + device-bridge** setup. The bridge
**flakes**, and it's a real productivity drag. Concrete evidence from THIS session (all bridge-related, not model):
- a backgrounded on-device build (`nohup … &` over `device_bash`) was **reaped the moment the bridge shell
  closed** → empty log, silent no-op. Backgrounding does not survive across `device_bash` calls.
- `device_commit_files` + `project_memory_write` had **dropped from the registry mid-session earlier** (reads OK) —
  the review-pass fixes + canon pack never committed until a later re-land.
- the mount **blocks `unlink`**, so `tar` can't overwrite existing files and `rm` fails — overwrites need
  `device_commit_files --force`; deletes need `mv` into `_to_delete/`.
- Dave, verbatim: *"the cloud bridge is rubbish… it's getting frustrating."* (He was gracious — *"it's not your fault pal."*)
Mitigation that worked: minimise bridge ops — **snapshot the tree into the cloud container once, work there, write back once.**

**Reality of "telling them" (be honest):** no direct pipe to Anthropic's product team from this session. Routing
channel = the **👎 thumbs-down** on a response. What I can do: (a) keep this **on record here**, (b) hand Dave a
**paste-ready blurb** for the 👎 box. Don't imply feedback was "sent" when it wasn't.

**How to apply:** when a Code-only feature comes up in Cowork, say so plainly; don't point Dave at it as if it's
his; offer the in-app equivalent or handle it myself. If Dave says "tell them," log here + offer the 👎 paste-blurb.
On bridge flakiness: proactively switch to the snapshot-once/work-in-cloud/write-back-once pattern rather than
chattering many small ops over the bridge.
