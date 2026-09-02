# #236 — LANE R2: THE AI-NATIVE SDLC PLAYBOOK — read it, then map what transfers

*Written 2026-09-02 by the Fable conductor. ONE Opus research sub (web + repo read; NO repo writes outside `notes/_subreports/`). Report files at `notes/_subreports/2026-09-02-236-R2-sdlc-playbook.md` per `s218-D7`; evidence beside it at `notes/_subreports/assets/2026-09-02-236-R2-sdlc-playbook/`; chat gets a STUB. Sibling lane: R1 (`notes/_briefs/2026-09-02-236-R1-principles-survey-brief.md`) — do not duplicate its work.*

## WHY THIS LANE EXISTS (Dave's words)

Carried since #233, PARKED AND UNREAD: *"the AI-native SDLC playbook — `https://claude.com/blog/the-ai-native-sdlc-playbook` plus its academy course. Dave watched the video and thinks it may rhyme with our playbook. Question to carry: what applies to a design-system FACTORY rather than a software product team?"*

Dave, #236 (live): *"lets think about claude's SDLC links I gave you. I think we might borrow from it for memento and for the Apollo deployments and the final Apollo product as one of a few options for the first phase of a design task."*

So there are THREE borrow targets, and the third is explicitly **one of a few options**, not the method:

1. **Memento** — the session-governance instrument: read chain, capture ritual, rulings store, gates, filed sub-reports, dream pass, recall probe.
2. **Apollo deployments** — the designer-skills packs as RELEASES (v1.0.4 ratified · v1.0.5 held · v1.0.6 in build), CI, provenance receipts, the generation chain.
3. **The Apollo product's first phase of a design task** — Apollo's framing is "lovable on rails", phases Discover / Create / Craft / Dispatch. The playbook's opening practices (spec-first, plan-first, brief before build, or whatever it actually says) may be ONE option a designer can pick for Discover.

## THE DELIVERABLE (all six, or say which is UNPROVEN and why)

1. **THE PLAYBOOK, IN OUR WORDS.** Fetch the blog post; find and fetch the academy course pages if reachable (search "Anthropic Academy AI-native SDLC"). Extract its structure: phases · practices · roles · artefacts · gates/checks · tooling it assumes. One table, our words, each row with a ≤15-word fetched quote as receipt + URL. If the course is paywalled or blocked, say so and mark `UNPROVEN: could not fetch <url>`; do not reconstruct it from memory or from the video Dave watched.

2. **THE BORROW MATRIX.** Rows = the playbook's practices. Three columns = the three targets above. Each cell = **ADOPT / ADAPT / REJECT** + one clause why + what it would replace or sit beside in Apollo (name the file, gate or ruling). Ground the Apollo side in the repo first (see below) so every "sits beside X" names a real X.

3. **WHAT DOES NOT TRANSFER, AND WHY.** A design-system factory (a generator + gates + one human ruler) is not a product team. Name the assumptions in the playbook that break here (team size, code review culture, PR flow, test pyramids, deployment targets, ownership) and what Memento already does INSTEAD.

4. **COLLISIONS WITH EXISTING RULINGS.** Where a playbook practice contradicts something already ruled — candidates: write-once / one-home (ADR-0017, `s192-D1`), generation chain not copy chain (#234, `s234-D1`…), the capture ritual being non-optional, filed sub-reports (`s218-D7`), delegation-by-default (#57), the PM topology (`s204-D1`: Fable judgment / Opus build-PM / adversarial verifier). Quote the ruling id you matched. A collision is a finding, not a defect — list it raw.

5. **THE DISCOVER OPTION, SKETCHED.** For target 3 only: sketch what "the playbook's opening move" would look like as ONE option a designer is offered at the start of a design task in Apollo — inputs, outputs, how long, what it produces for Create. Put it beside two OTHER plausible first-phase options (e.g. a brief-led route, a pattern-first route) so Dave sees it as one of a few. Sketch, not build; no UI.

6. **IDEAS FOR OTHER TASKS** the reading surfaced — Dave's standing instruction at #236: *"and ideas for other tasks, lets not miss that."* One line each, with what it depends on. Then the RULING-SHAPED QUESTIONS you could not answer.

## GROUND FIRST (~20 min, before fetching)

`knowledge/_RUNBOOK-capture-ritual.md` (first 80 lines — what the wrap does) · `MODEL-ROUTING.md` · `notes/_briefs/2026-09-02-234-v106-brief.md` (the generation-chain principle and the lanes L1–L5) · `notes/_subreports/2026-09-02-235-L1-receipt-gate.md` §VERDICT (a release gate done right) · grep `Discover` / `Create` / `Craft` / `Dispatch` and `lovable on rails` in `notes/` and `apollo-spider/` to find Apollo's product framing (quote the file you found it in) · `apollo-spider/` top level (the shipped pack) · `git log --oneline -15` (how sessions land) · the ADR index (find it: `ls | grep -i adr`, or grep `ADR-0017`).

## METHOD RULES

- **Fetched, quoted, or UNPROVEN.** No citation from memory. Quotes ≤ 15 words each, one per claim, with URL.
- **Our words** for the playbook's content; the post is Anthropic's copyright.
- **Name what you did NOT cover** in a closing section.
- **Every "Apollo already does X" carries its probe** — path:line or the command and its quoted output. An unmatched grep is not an absence.

## DO NOT RULE

No adoption decision — the matrix PROPOSES, Dave rules. No edits outside `notes/_subreports/`. No re-wording of any `s2xx-D*` or ADR. Do not touch the Apollo product framing files. Do not open or extend lane R1's registers.

## FILING

Copy `notes/_subreports/_TEMPLATE.md`; `sub index` = `R2`; `brief:` = this file. Counts line: **practices N · ADOPT/ADAPT/REJECT per target = n/n/n × 3 · non-transfers N · collisions N · first-phase options N · ideas N · UNPROVEN N.** Close with **REPLAY-THESE** (≤ 7 lines). Token spend: `UNMEASURED — no message.usage at a sub's seat`, plus the SHAPE (tool calls, fetches).

## PITFALLS (consequences replayed, #165)

- **Reconstructing the course from memory** because the page is blocked — that is a confident false inscription, the exact Memento failure. UNPROVEN instead.
- **"Rhymes with" is not "maps to"** — an ADAPT cell needs the concrete change named, or it is a REJECT you were too polite to write.
- **Borrowing a practice that a ruling already forbids** silently re-opens the ruling. Quote the id; put it in COLLISIONS.
- **Treating target 3 as THE method** — Dave said one of a few options. Always show it beside alternatives.
- **Big page dumps** — fetch with care; the sandbox call boundary is ~178 s.
- **The report is the authority; the stub copies it.**
