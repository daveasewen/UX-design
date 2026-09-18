# #285 — Dave's words, verbatim, 2026-09-18

- *"Good Morning!"*
- On the #284 contact sheet, with the 4× shots: *"the scaling is wonky"* — and a pasted research note on the "lost in the middle" phenomenon: *"Is thre anything here we can use"*.
- The conductor first read the wonkiness as a contact-sheet layout bug (`transform:scale(4)` not reserving layout). **Dave corrected him with a 4× crop of the wordmark:** *"Maybe we misunderstand each other on the logo scaling, see image the word mark is distorted, look at the B"*. The conductor confirmed against `_gen_masters.py`: per-node snapping of straight segments inside curved glyphs (S, B, C) while curve controls stay unsnapped kinks the bowls. **The #284 acceptance (*"the sheet is good BTW"*) is REOPENED by Dave's own eye** — the masters are regenerated and come back for a fresh acceptance.
- On the messy-middle research: *"Okay this sound good."* — to the conductor's read that only tactic 1 (front-load rules, re-quote constraints at the tail) is usable in Cowork; output-priming is API-only; hygiene and retrieval are already the chain's rules.
- **"go on both this and: yes to the seam re-quoting the standing constraints"** — two lanes cut: (1) regenerate the 40 masters with wordmark snapping reduced to a rigid move, fix the 4× panel on the sheet, re-shoot; (2) `_seam.py` gains a standing-constraints tail block. ⚠ The constraints list is a NEW file the conductor drafts and Dave approves — nothing in it is inscribed by the lane.

- On the regenerated masters, the seam's STANDING block and the verifier's 16/16: *"excellent work!"* — ⚠ ENTHUSIASM, NOT A RULING (`s271-D4`). The masters' acceptance by eye and the `_standing.md` wording are still his words to give. The commit lane was cut on the verifier's pass, not on this line.

- **"1. go" — the showroom re-sync (108 pages stale from the `:is(`→`:where(` canon change) is cut as its own commit lane.**
- **"2. accept" — THE REGENERATED MASTERS ARE ACCEPTED BY EYE.** This replaces the #284 acceptance, which Dave reopened himself with the B crop. `W-285lm`'s eye-half is closed; registration in `_logo_nodes.json` (the `gen_kg_icons.py` fence) is still owed and still his word on HOW. The `_standing.md` wording is NOT yet ruled — "accept" was answered to the masters question only.

- *"what about the context management part?"* — the conductor's answer: the tail re-quote is done; the 80K boot is system + tools + connectors and moves only with connectors; auto-compaction fires near 1M and is not a lever. He showed the setup (connectors: Browser, Claude Docs, Claude in Chrome, GitHub; skills: dave-voice, dream-pass, swiss-design-system, gtb-brand off, docs, deep-research, import-memory; computer use OFF): *"this is how the setup stand now"* · *"I havnt touched anything and computer use is off"*.
- *"but deep research might be useful no? is it big"* — kept; a skill costs its description only (~80 tokens).
- **THE CONNECTOR ANSWER, BY ACT: he set the built-in Browser's 17 tools to BLOCKED in Tool permissions** (screenshot). The `mcp__Claude_Browser__*` server dropped out of the conductor's tool set in the same session. ⇒ **#286's opener measures boot COLD with this ONE variable changed against today's 80,863.** Skills untouched by design (second run, if the first moves).

## Still his
- The wording of the eight lines in `knowledge/_standing.md` (DRAFT).
- HOW the accepted masters get registered in `_logo_nodes.json` (the `gen_kg_icons.py` fence).
